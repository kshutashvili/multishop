#from oscar.apps.partner.admin import *  # noqa
from django.contrib import admin
from .models import StockRecord


admin.site.register(StockRecord)