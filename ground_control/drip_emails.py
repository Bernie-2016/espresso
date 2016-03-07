from .models import BsdEvents, BsdPeople, BsdEventAttendees
import espresso


class BsdEventHostDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item.creator_cons,
            'email_address': item.creator_cons.email_address,
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Event (Send to Event Host)'


class BsdPeopleDripType(espresso.DripBase):
    
    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item,
            'email_address': item.email_address
        }

    class Meta:
        model = BsdPeople
        verbose_name = 'People'


class BsdEventAttendeesDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item.attendee_cons,
            'email_address': item.attendee_cons.email_address,
            'event': item.event
        }

    class Meta:
        model = BsdEventAttendees
        verbose_name = 'Event Attendees'


class BsdEventAttendeesToHostType(BsdEventAttendeesDripType):

    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item.attendee_cons,
            'email_address': item.event.creator_cons.email_address
        }

    class Meta:
        model = BsdEventAttendees
        verbose_name = 'Event Attendees (Send to Host)'


class BsdEventEveryoneDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        email_address = map(lambda x: x.attendee_cons.email_addresses, item.attendees)
        email_addresses.append(item.creator_cons.email_addresses)

        return {
            'email_address': email_addresses
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Event (Send to Event Host AND Attendees)'