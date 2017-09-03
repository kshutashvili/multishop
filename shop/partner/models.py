from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

from oscar.apps.partner.abstract_models import AbstractStockRecord


class StockRecord(AbstractStockRecord):
    partner_sku = models.CharField(_("Partner SKU"), max_length=128,
                                   blank=True, null=True)
    partner = models.ForeignKey(
        'partner.Partner',
        on_delete=models.CASCADE,
        verbose_name=_("Partner"),
        related_name='stockrecords',
        blank=True,
        null=True)

    previous_price = models.DecimalField(
        _("Previous Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    price_updated = models.BooleanField(default=True)


from oscar.apps.partner.models import *  # noqa
