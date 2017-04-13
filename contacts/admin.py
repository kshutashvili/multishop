# -*- coding: utf-8 -*-

from django.contrib import admin

from contacts.models import PhoneNumber, SocialNetRef


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone', 'operator', 'site')
    list_filter = ('operator', 'site',)


@admin.register(SocialNetRef)
class SocialNetRefAdmin(admin.ModelAdmin):
    list_display = ('ref_type', 'reference', 'site')
    list_filter = ('site',)
