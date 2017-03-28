# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone', 'operator')
    list_filter = ('operator',)
