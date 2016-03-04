# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class BsdPeople(models.Model):
    cons_id = models.AutoField(primary_key=True)
    prefix = models.CharField(max_length=16, blank=True)
    firstname = models.CharField(max_length=256, blank=True)
    middlename = models.CharField(max_length=128, blank=True)
    lastname = models.CharField(max_length=256, blank=True)
    suffix = models.CharField(max_length=16, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    birth_dt = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=128, blank=True)
    employer = models.CharField(max_length=128, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bsd_people'
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    @classmethod
    def get_drip_select_related(self):
        return ['email_addresses', 'addresses', 'phone_numbers']

    def get_email_address(self):
        return self.email_addresses.filter(is_primary=True).first().email

    def __unicode__(self):
        return "%(firstname)s %(lastname)s <%(email)s>" % \
                    {'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email_addresses.first().email}


class BsdAddresses(models.Model):
    cons_addr_id = models.BigIntegerField(primary_key=True)
    cons = models.ForeignKey(BsdPeople, related_name='addresses')
    is_primary = models.NullBooleanField()
    addr1 = models.CharField(max_length=300, blank=True)
    addr2 = models.CharField(max_length=300, blank=True)
    addr3 = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state_cd = models.CharField(max_length=200, blank=True)
    zip = models.CharField(max_length=30, blank=True)
    zip_4 = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    geom = models.TextField(blank=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bsd_addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class BsdEmails(models.Model):
    cons_email_id = models.BigIntegerField(primary_key=True)
    cons = models.ForeignKey(BsdPeople, related_name='email_addresses')
    is_primary = models.BooleanField()
    email = models.CharField(max_length=255)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bsd_emails'
        verbose_name = 'Email Address'
        verbose_name_plural = 'Email Addresses'


class BsdEventTypes(models.Model):
    event_type_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'bsd_event_types'
        verbose_name = 'Event Type'


class BsdEvents(models.Model):
    event_id = models.BigIntegerField(primary_key=True)
    event_id_obfuscated = models.CharField(max_length=16, blank=True)
    flag_approval = models.BooleanField()
    name = models.CharField(max_length=256)
    description = models.TextField()
    venue_name = models.CharField(max_length=300)
    venue_zip = models.CharField(max_length=16, blank=True)
    venue_city = models.CharField(max_length=128)
    venue_state_cd = models.CharField(max_length=100)
    venue_addr1 = models.CharField(max_length=255)
    venue_addr2 = models.CharField(max_length=255, blank=True)
    venue_country = models.CharField(max_length=2)
    venue_directions = models.TextField(blank=True)
    start_tz = models.CharField(max_length=40, blank=True)
    start_dt = models.DateTimeField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    capacity = models.BigIntegerField()
    attendee_volunteer_show = models.BigIntegerField()
    attendee_volunteer_message = models.TextField(blank=True)
    is_searchable = models.BigIntegerField()
    public_phone = models.BooleanField()
    contact_phone = models.CharField(max_length=25, blank=True)
    host_receive_rsvp_emails = models.BooleanField()
    rsvp_use_reminder_email = models.BooleanField()
    rsvp_email_reminder_hours = models.BigIntegerField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    creator_cons = models.ForeignKey(BsdPeople, related_name='events_created')
    event_type = models.ForeignKey(BsdEventTypes, related_name='events')
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    geom = models.TextField(blank=True)  # This field type is a guess.
    is_official = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'bsd_events'
        verbose_name = 'Event'

    def __unicode__(self):
        return self.name


class BsdEventAttendees(models.Model):
    event_attendee_id = models.BigIntegerField(primary_key=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    attendee_cons = models.ForeignKey(BsdPeople, related_name='rsvps')
    event = models.ForeignKey(BsdEvents, related_name='attendees')

    class Meta:
        managed = False
        db_table = 'bsd_event_attendees'
        verbose_name = 'RSVP'


class BsdEventShifts(models.Model):
    event_shift_id = models.BigIntegerField(blank=True, null=True)
    event = models.ForeignKey(BsdEvents, related_name='shifts')
    start_time = models.TimeField(blank=True, null=True)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)
    capacity = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsd_event_shifts'
        verbose_name = 'Event Shift'


class BsdGroups(models.Model):
    cons_group_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bsd_groups'
        verbose_name = 'Group'


class BsdPersonBsdGroups(models.Model):
    cons = models.ForeignKey(BsdPeople, related_name='groups')
    cons_group = models.ForeignKey(BsdGroups, related_name='memberships')

    class Meta:
        managed = False
        db_table = 'bsd_person_bsd_groups'
        verbose_name = 'Group Membership'


class BsdPersonGcBsdGroups(models.Model):
    cons = models.ForeignKey(BsdPeople)
    gc_bsd_group_id = models.IntegerField()
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    id = models.IntegerField(primary_key=True)  # AutoField?

    class Meta:
        managed = False
        db_table = 'bsd_person_gc_bsd_groups'


class BsdPhones(models.Model):
    cons_phone_id = models.BigIntegerField(primary_key=True)
    cons = models.ForeignKey(BsdPeople, related_name='phone_numbers')
    is_primary = models.BooleanField()
    phone = models.CharField(max_length=30)
    isunsub = models.NullBooleanField()
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bsd_phones'
        verbose_name = 'Phone'


class BsdSubscriptions(models.Model):
    cons_email_chapter_subscription_id = models.BigIntegerField(blank=True, null=True)
    cons_email = models.ForeignKey(BsdEmails, related_name='subscriptions')
    cons = models.ForeignKey(BsdPeople, related_name='email_subscriptions')
    chapter_id = models.BigIntegerField(blank=True, null=True)
    isunsub = models.NullBooleanField()
    unsub_dt = models.DateTimeField(blank=True, null=True)
    modified_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bsd_subscriptions'
        verbose_name = 'Subscription'


class BsdSurveys(models.Model):
    signup_form_id = models.BigIntegerField(primary_key=True)
    signup_form_slug = models.CharField(max_length=100, blank=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bsd_surveys'
        verbose_name = 'Survey'


class BsdSurveyFields(models.Model):
    signup_form_field_id = models.BigIntegerField(primary_key=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    signup_form = models.ForeignKey(BsdSurveys, related_name='fields')
    stg_signup_column_name = models.CharField(max_length=64, blank=True)
    format = models.IntegerField()
    label = models.CharField(max_length=20000, blank=True)
    display_order = models.IntegerField()
    is_shown = models.BooleanField()
    is_required = models.BooleanField()
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'bsd_survey_fields'
        verbose_name = 'Survey Field'


class Communications(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    person_id = models.IntegerField()
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'communications'
        verbose_name = 'Communication'


class FastFwdRequest(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    event = models.ForeignKey(BsdEvents, related_name='fast_fwd_requests')
    host_message = models.TextField()
    email_sent_dt = models.DateTimeField(blank=True, null=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fast_fwd_request'
        verbose_name = 'FastFwd Request'


class ZipCodes(models.Model):
    id = models.BigIntegerField(primary_key=True)
    modified_dt = models.DateTimeField()
    create_dt = models.DateTimeField()
    zip = models.CharField(unique=True, max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone_offset = models.IntegerField()
    has_dst = models.BooleanField()
    geom = models.TextField(blank=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'zip_codes'