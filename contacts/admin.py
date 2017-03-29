# -*- coding: utf-8 -*-

from django.contrib import admin

from contacts.models import PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone', 'operator', 'site')
    list_filter = ('operator', 'site',)
