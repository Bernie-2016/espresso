from .models import BsdEvents, BsdPeople
import espresso


class BsdEventsDripType(espresso.DripBase):

    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item.creator_cons,
            'email_address': item.creator_cons.email_addresses.order_by('is_primary').first().email,
            'event': item
        }

    class Meta:
        model = BsdEvents
        verbose_name = 'Event'


class BsdPeopleDripType(espresso.DripBase):
    
    @classmethod
    def get_email_context(cls, item):
        return {
            'user': item,
            'email_address': item.email_addresses.order_by('is_primary').first().email
        }

    class Meta:
        model = BsdPeople
        verbose_name = 'People'