# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview
from django.contrib.sites.models import Site
from oscar.core import validators


class ProductReview(AbstractProductReview):
    title = models.CharField(
        verbose_name=pgettext_lazy(u"Product review title", u"Title"),
        max_length=255,
        validators=[validators.non_whitespace],
        blank=True
    )
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)
    advantage = models.TextField(_("Advantage"), blank=True)
    disadvantage = models.TextField(_("Disadvantage"), blank=True)

from oscar.apps.catalogue.reviews.models import *  # noqa
