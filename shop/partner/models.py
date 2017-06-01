from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

from oscar.apps.partner.abstract_models import AbstractStockRecord


class StockRecord(AbstractStockRecord):
    previous_price = models.DecimalField(
        _("Previous Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)


from oscar.apps.partner.models import *  # noqa
