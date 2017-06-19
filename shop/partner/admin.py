#from oscar.apps.partner.admin import *  # noqa
from django.contrib import admin
from .models import StockRecord


class StockRecordAdmin(admin.ModelAdmin):

    exclude = ('price_updated',)


admin.site.register(StockRecord, StockRecordAdmin)
