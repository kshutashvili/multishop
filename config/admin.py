# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin

from .models import (SiteConfig, Configuration, MenuItem, MenuCategory,
                     TextOne, TextTwo, TextThree, TextFour, MetaTag, ModelMetaTag,
                     FuelConfiguration, BenefitItem, OverviewItem, ReviewItem,
                     DeliveryAndPay)


admin.site.register(ModelMetaTag)


class SiteConfigInline(admin.StackedInline):
    model = SiteConfig
    can_delete = False


class SiteConfigAdmin(admin.ModelAdmin):
    inlines = (SiteConfigInline,)
    change_list_template = 'admin/change_list.html'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(SiteConfigAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(Site)
admin.site.register(Site, SiteConfigAdmin)


class TextOneAdminForm(forms.ModelForm):
    class Meta:
        model = TextOne
        widgets = {
            'text': CKEditorWidget(),
        }
        fields = '__all__'


class TextTwoAdminForm(forms.ModelForm):
    class Meta:
        model = TextTwo
        widgets = {
            'text': CKEditorWidget(),
        }
        fields = '__all__'


class TextThreeAdminForm(forms.ModelForm):
    class Meta:
        model = TextThree
        widgets = {
            'text': CKEditorWidget(),
        }
        fields = '__all__'


class TextFourAdminForm(forms.ModelForm):
    class Meta:
        model = TextFour
        widgets = {
            'text': CKEditorWidget(),
        }
        fields = '__all__'


class MenuItemAdminForm(forms.ModelForm):
    class Meta:
        model = MenuItem

        exclude = ('name',)


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ('type', )


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    pass


@admin.register(TextOne)
class TextOneAdmin(admin.ModelAdmin):
    list_display = ('text', 'site', 'is_active')
    form = TextOneAdminForm


@admin.register(TextTwo)
class TextTwoAdmin(admin.ModelAdmin):
    list_display = ('text', 'site', 'is_active')
    form = TextTwoAdminForm


@admin.register(TextThree)
class TextThreeAdmin(admin.ModelAdmin):
    list_display = ('text', 'site', 'is_active')
    form = TextThreeAdminForm


@admin.register(TextFour)
class TextFourAdmin(admin.ModelAdmin):
    list_display = ('text', 'site', 'is_active')
    form = TextFourAdminForm


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    fields = ('name_ru', 'name_uk', 'order')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'show_link', 'is_active', 'site')
    list_filter = ('is_active', 'site', 'position')
    form = MenuItemAdminForm

    def show_link(self, obj):
        return format_html('<a href="{href}" target="_blank">{href}</a>',
                           href=obj.link)

    show_link.short_description = 'Ссылка'


@admin.register(FuelConfiguration)
class FuelConfigurationAdmin(admin.ModelAdmin):
    list_display = ('fuel_type', 'fuel_cost')


@admin.register(BenefitItem)
class BenefitItemAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(OverviewItem)
class OverviewItemAdmin(admin.ModelAdmin):
    list_display = ('link',)


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'created')


class DeliveryAndPayAdminForm(forms.ModelForm):
    class Meta:
        model = DeliveryAndPay
        widgets = {
            'text': CKEditorWidget(),
        }
        fields = '__all__'


@admin.register(DeliveryAndPay)
class DeliveryAndPayAdmin(admin.ModelAdmin):
    list_display = ('for_block', 'title')
