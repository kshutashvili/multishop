from django.contrib import admin
from oscar.apps.catalogue.admin import ProductAdmin as OscarProductAdmin

from .models import ExtraImage, Product, Video


class ExtraImageInline(admin.TabularInline):
    model = ExtraImage
    extra = 0


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


admin.site.unregister(Product)


@admin.register(Product)
class ProductAdmin(OscarProductAdmin):
    inlines = OscarProductAdmin.inlines + [ExtraImageInline, VideoInline]


from oscar.apps.catalogue.admin import *  # noqa
