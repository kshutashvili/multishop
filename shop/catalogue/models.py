# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductAttributeValue, AbstractProductClass, \
    AbstractProductCategory, AbstractCategory
from django.utils.translation import get_language


class Product(AbstractProduct):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ProductClass(AbstractProductClass):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ProductCategory(AbstractProductCategory):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)

class Category(AbstractCategory):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


class ProductAttributeValue(AbstractProductAttributeValue):
    _localizable = ["text", "richtext"]  # types of fields, that need to be localized

    def _get_value(self):
        if self.attribute.type in ProductAttributeValue._localizable:
            return getattr(self, 'value_%s_ru' % self.attribute.type), getattr(self,
                                                                               'value_%s_uk' % self.attribute.type)
        else:
            return getattr(self, 'value_%s' % self.attribute.type)

    @property
    def value_as_html(self):
        """
        Returns a HTML representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_html property and
        return e.g. an <img> tag.  Defaults to the _as_text representation.
        """
        if self.attribute.type not in ProductAttributeValue._localizable:
            property_name = '_%s_as_html' % self.attribute.type
            return getattr(self, property_name, self.value_as_text)
        else:
            property_name = '_%s_as_html' % self.attribute.type
            locales = {'ru': 0, 'uk': 1}
            index = locales[get_language()]
            value = eval(getattr(self, property_name, self.value_as_text))[index]
            return value

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
