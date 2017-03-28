# -*- coding: utf-8 -*-
from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.contrib.sites.models import Site


class Product(AbstractProduct):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ExtraImage(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    image = models.ImageField(
        'Изображение',
        upload_to=('products/images')
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='extra_images'
    )

    def __unicode__(self):
        return self.image.name


class Video(models.Model):
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    video = models.URLField()
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='videos'
    )

    def __unicode__(self):
        return self.video


from oscar.apps.catalogue.models import *
