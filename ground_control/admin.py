from django.contrib import admin
from .models import *



@admin.register(BsdPeople)
class BsdPeopleAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdAddresses)
class BsdAddressesAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdEmails)
class BsdEmailsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdEventAttendees)
class BsdEventAttendeesAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdEventShifts)
class BsdEventShiftsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdEventTypes)
class BsdEventTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdEvents)
class BsdEventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_dt', 'venue_city', 'venue_state_cd', 'creator_cons']
    raw_id_fields = ['creator_cons']


@admin.register(BsdGroups)
class BsdGroupsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdPersonBsdGroups)
class BsdPersonBsdGroupsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdPhones)
class BsdPhonesAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdSubscriptions)
class BsdSubscriptionsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdSurveyFields)
class BsdSurveyFieldsAdmin(admin.ModelAdmin):
    pass


@admin.register(BsdSurveys)
class BsdSurveysAdmin(admin.ModelAdmin):
    pass


@admin.register(Communications)
class CommunicationsAdmin(admin.ModelAdmin):
    pass


@admin.register(FastFwdRequest)
class FastFwdRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(ZipCodes)
class ZipCodesAdmin(admin.ModelAdmin):
    pass
