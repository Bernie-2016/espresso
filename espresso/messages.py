from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.utils.html import strip_tags

# from drip.models import SentDrip, SentEventDrip
# from ground_control.models import BsdEvents


class DripMessage(object):

    def __init__(self, drip_base):
        self.drip_base = drip_base
        self._context = None
        self._subject = None
        self._body = None
        self._plain = None
        self._message = None

    def set_context(self, data):
        self._context = Context(data)
        return self

    @property
    def from_email(self):
        return self.drip_base.from_email

    @property
    def from_email_name(self):
        return self.drip_base.from_email_name

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
                self.subject, self.plain, from_, [self.context['email_address']])

            # check if there are html tags in the rendered template
            if len(self.plain) != len(self.body):
                self._message.attach_alternative(self.body, 'text/html')
        return self._message