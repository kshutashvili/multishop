# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.sites.models import Site
from solo.admin import SingletonModelAdmin

from .models import SiteConfig, Configuration, MenuItem, MenuCategory


class SiteConfigInline(admin.StackedInline):
    model = SiteConfig
    can_delete = False


class SiteConfigAdmin(admin.ModelAdmin):
    inlines = (SiteConfigInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(SiteConfigAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(Site)
admin.site.register(Site, SiteConfigAdmin)


@admin.register(Configuration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    list_display = ('power_attribute',)


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'show_link', 'is_active', 'site')
    list_filter = ('is_active', 'site', 'position')

    def show_link(self, obj):
        return format_html('<a href="{href}" target="_blank">{href}</a>',
                           href=obj.link)
    show_link.short_description = 'Ссылка'
