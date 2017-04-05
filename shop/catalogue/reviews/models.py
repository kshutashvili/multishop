# -*- coding: utf-8 -*-

from django.db import models

from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview
from django.contrib.sites.models import Site


class ProductReview(AbstractProductReview):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ProductReview(AbstractProductReview):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)

from oscar.apps.catalogue.reviews.models import *  # noqa
