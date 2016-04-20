from .models import BsdEvents, BsdPeople, BsdEventAttendees
from geo.models import *
import requests
import espresso

# # might be nice to move to a task but let's see how painful this becomes.
CALIFORNIA_CONGRESSIONAL_DISTRICTS = requests.get('http://googledoctoapi.forberniesanders.com/1wd-MZsG_DO5UgUHPoZjCeWfS_QlVX1-Vjz6IBWhUqW8').json()


class BsdPeopleDripType(espresso.DripBase):
    
    @classmethod
    def get_email_context(cls, item):
        return {
            'person': item,
            'email_address': item.email_address
        }

    class Meta:
        model = BsdPeople
        verbose_name = 'People'


class BsdEventHostDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'host': item.creator_cons,
            'email_address': item.creator_cons.email_address,
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Event (Send to Event Host)'


class BsdEventEveryoneDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        email_addresses = map(lambda x: x.attendee_cons.email_address, item.attendees.all())
        email_addresses.append(item.creator_cons.email_address)

        return {
            'email_address': email_addresses,
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Event (Send to Event Host AND Attendees)'


class BsdEventAttendeesDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'attendee': item.attendee_cons,
            'email_address': item.attendee_cons.email_address,
            'event': item.event,
            'rsvp': item
        }

    class Meta:
        model = BsdEventAttendees
        verbose_name = 'Event Attendees'


class BsdEventAttendeesToHostType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'attendee': item.attendee_cons,
            'email_address': item.event.creator_cons.email_address,
            'event': item.event,
            'rsvp': item
        }

    class Meta:
        model = BsdEventAttendees
        verbose_name = 'Event Attendees (Send to Host)'


class FieldStaffType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        cd = CongressionalDistricts.objects.get(geom__contains=item.geom)
        return {
            'email_address': 'jonculver@berniesanders.com',
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Events (Send to Field Staff)'