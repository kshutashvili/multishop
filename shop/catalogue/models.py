# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductAttributeValue


class Product(AbstractProduct):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ProductAttributeValue(AbstractProductAttributeValue):
    _localizable = ["text", "richtext"]  # types of fields, that need to be localized

    def _get_value(self):
        if self.attribute.type in ProductAttributeValue._localizable:
            return getattr(self, 'value_%s_ru' % self.attribute.type), getattr(self,
                                                                               'value_%s_uk' % self.attribute.type)
        else:
            return getattr(self, 'value_%s' % self.attribute.type)

    value = property(_get_value, AbstractProductAttributeValue._set_value)


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
