from oscar.apps.catalogue.reviews.admin import *  # noqa

from django.contrib import admin

from .models import ProductQuestion, ReviewAnswer


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ('when_created', 'product', 'name', 'phone')


admin.site.register(ReviewAnswer)
