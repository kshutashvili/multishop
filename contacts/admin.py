# -*- coding: utf-8 -*-

from parler.admin import TranslatableAdmin

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage as DjangoFlatPage

from contacts.models import PhoneNumber, SocialNetRef, WorkSchedule, Timetable, \
    ContactMessage
from .models import FlatPage, City

admin.site.register(Timetable)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone', 'operator', 'site', 'city')
    list_filter = ('operator', 'site',)


@admin.register(SocialNetRef)
class SocialNetRefAdmin(admin.ModelAdmin):
    list_display = ('ref_type', 'reference', 'site')
    list_filter = ('site',)


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ('timetable',)
    list_display = ('schedule_type', 'site', 'city')
    list_filter = ('schedule_type', 'site')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('created', 'phone', 'site',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'address')
    prepopulated_fields = {"slug": ("city_name",)}


admin.site.unregister(DjangoFlatPage)
@admin.register(FlatPage)
class FlatPageAdmin(TranslatableAdmin):
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


# admin.site.unregister(DjangoFlatPage)
# admin.site.register(FlatPage)
