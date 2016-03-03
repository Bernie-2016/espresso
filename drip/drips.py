import operator
import functools

from django.conf import settings
from django.db.models import Q
from django.template import Context, Template
from django.utils.importlib import import_module
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from drip.models import SentDrip
from drip.utils import get_user_model

try:
    from django.utils.timezone import now as conditional_now
except ImportError:
    from datetime import datetime
    conditional_now = datetime.now


import logging


def configured_message_classes():
    conf_dict = getattr(settings, 'DRIP_MESSAGE_CLASSES', {})
    if 'default' not in conf_dict:
        conf_dict['default'] = 'drip.drips.DripMessage'
    return conf_dict


def message_class_for(name):
    path = configured_message_classes()[name]
    mod_name, klass_name = path.rsplit('.', 1)
    mod = import_module(mod_name)
    klass = getattr(mod, klass_name)
    return klass


class DripMessage(object):

    def __init__(self, drip_base, **kwargs):
        self.drip_base = drip_base
        self._context = context
        self._subject = None
        self._body = None
        self._plain = None
        self._message = None
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @property
    def from_email(self):
        return self.drip_base.from_email

    @property
    def from_email_name(self):
        return self.drip_base.from_email_name

    @classmethod
    def get_context(self, item):
        return {}

    @property
    def context(self):
        return self._context

    @property
    def subject(self):
        if not self._subject:
            self._subject = Template(self.drip_base.subject_template).render(self.context)
        return self._subject

    @property
    def body(self):
        if not self._body:
            self._body = Template(self.drip_base.body_template).render(self.context)
        return self._body

    @property
    def plain(self):
        if not self._plain:
            self._plain = strip_tags(self.body)
        return self._plain

    @property
    def message(self):
        if not self._message:
            if self.drip_base.from_email_name:
                from_ = "%s <%s>" % (self.drip_base.from_email_name, self.drip_base.from_email)
            else:
                from_ = self.drip_base.from_email

            self._message = EmailMultiAlternatives(
                self.subject, self.plain, from_, [self.user.get_email_address()])

            # check if there are html tags in the rendered template
            if len(self.plain) != len(self.body):
                self._message.attach_alternative(self.body, 'text/html')
        return self._message


class DripBase(object):
    """
    A base object for defining a Drip.

    You can extend this manually, or you can create full querysets
    and templates from the admin.
    """
    #: needs a unique name
    name = None
    subject_template = None
    body_template = None
    from_email = None
    from_email_name = None

    def __init__(self, drip_model, *args, **kwargs):
        self.drip_model = drip_model

        self.name = kwargs.pop('name', self.name)
        self.from_email = kwargs.pop('from_email', self.from_email)
        self.from_email_name = kwargs.pop('from_email_name', self.from_email_name)
        self.subject_template = kwargs.pop('subject_template', self.subject_template)
        self.body_template = kwargs.pop('body_template', self.body_template)

        if not self.name:
            raise AttributeError('You must define a name.')

        self.now_shift_kwargs = kwargs.get('now_shift_kwargs', {})


    #########################
    ### DATE MANIPULATION ###
    #########################

    def now(self):
        """
        This allows us to override what we consider "now", making it easy
        to build timelines of who gets what when.
        """
        return conditional_now() + self.timedelta(**self.now_shift_kwargs)

    def timedelta(self, *a, **kw):
        """
        If needed, this allows us the ability to manipuate the slicing of time.
        """
        from datetime import timedelta
        return timedelta(*a, **kw)

    def walk(self, into_past=0, into_future=0):
        """
        Walk over a date range and create new instances of self with new ranges.
        """
        walked_range = []
        for shift in range(-into_past, into_future):
            kwargs = dict(drip_model=self.drip_model,
                          name=self.name,
                          now_shift_kwargs={'days': shift})
            walked_range.append(self.__class__(**kwargs))
        return walked_range

    def apply_queryset_rules(self, qs):
        """
        First collect all filter/exclude kwargs and apply any annotations.
        Then apply all filters at once, and all excludes at once.
        """
        clauses = {
            'filter': [],
            'exclude': []}

        for rule in self.drip_model.queryset_rules.all():

            clause = clauses.get(rule.method_type, clauses['filter'])

            kwargs = rule.filter_kwargs(qs, now=self.now)
            clause.append(Q(**kwargs))

            qs = rule.apply_any_annotation(qs)

        if clauses['exclude']:
            qs = qs.exclude(functools.reduce(operator.or_, clauses['exclude']))
        qs = qs.filter(*clauses['filter'])

        return qs

    ##################
    ### MANAGEMENT ###
    ##################

    def get_user(self, item):
        return item

    def get_queryset(self):
        try:
            return self._queryset
        except AttributeError:
            self._queryset = self.apply_queryset_rules(self.queryset())\
                                 .distinct()
            return self._queryset

    def run(self):
        """
        Get the queryset, prune sent people, and send it.
        """
        if not self.drip_model.enabled:
            return None

        self.prune()
        count = self.send()

        return count

    def prune(self):
        """
        Do an exclude for all Users who have a SentDrip already.
        """
        target_user_ids = self.get_queryset().values_list('pk', flat=True)
        exclude_user_ids = SentDrip.objects.filter(date__lt=conditional_now(),
                                                   drip=self.drip_model,
                                                   user__id__in=target_user_ids)\
                                           .values_list('user_id', flat=True)
        self._queryset = self.get_queryset().exclude(pk__in=exclude_user_ids)

    def send(self):
        """
        Send the message to each user on the queryset.

        Create SentDrip for each user that gets a message.

        Returns count of created SentDrips.
        """

        if not self.from_email:
            self.from_email = getattr(settings, 'DRIP_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
        MessageClass = message_class_for(self.drip_model.message_class)

        count = 0
        for item in self.get_queryset():
            context = MessageClass.get_context(item)
            if not context:
                context = {'user': self.get_user(item)}
            context['drip_base'] = self
            message_instance = MessageClass(Context(**MessageClass.context))
            try:
                print "not sending for now"
                # result = message_instance.message.send()
                result = False
                print message_instance.subject
                print message_instance.body
                print '-' * 60
                if result:
                    SentDrip.objects.create(
                        drip=self.drip_model,
                        user=context['user'],
                        from_email=self.from_email,
                        from_email_name=self.from_email_name,
                        subject=message_instance.subject,
                        body=message_instance.body
                    )
                    count += 1
            except Exception as e:
                logging.error("Failed to send drip %s to user %s: %s" % (self.drip_model.id, user, e))

        return count


    ####################
    ### USER DEFINED ###
    ####################

    def queryset(self):
        """
        Returns a queryset of auth.User who meet the
        criteria of the drip.

        Alternatively, you could create Drips on the fly
        using a queryset builder from the admin interface...
        """
        User = get_user_model()
        return User.objects.select_related(*User.get_drip_select_related())


class EventDripBase(DripBase):

    def get_user(self, item):
        return item.creator_cons

    def queryset(self):
        return BSDEvent.objects.select_related(*BSDEvent.get_drip_select_related())


class EventDripMessage(DripMessage):

    @property
    def context(self, item):
        return {'event': item}