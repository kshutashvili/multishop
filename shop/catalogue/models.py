# -*- coding: utf-8 -*-
import operator

import redis
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import get_language
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductAttributeValue, AbstractProductClass, \
    AbstractProductCategory, AbstractCategory


class Product(AbstractProduct):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)

    def change_similar_products(self, recent_products):
        r = self.get_or_create_redis_connection()
        key = self.get_product_key()
        recent_product_ids = [p.id for p in recent_products]
        if r.exists(key):
            for product in recent_product_ids:
                r.hincrby(key, product, 1)  # if there is no key, it will be created
        else:
            r.hmset(key, dict.fromkeys(recent_product_ids, 1))

    def get_similar_products(self):
        r = self.get_or_create_redis_connection()
        key = self.get_product_key()
        products = r.hgetall(key)
        if products:
            products = [k for k, v in sorted(products.items(), key=operator.itemgetter(1), reverse=True)][
                       :10]  # 10 the most popular products similar to current one
            return Product.objects.filter(id__in=products)
        else:
            return None

    def get_product_key(self):
        return '{}_similar_products'.format(self.id)

    def get_or_create_redis_connection(self):
        try:
            connection = Product.redis
            return connection
        except AttributeError:
            Product.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            Product.redis = redis.Redis(connection_pool=Product.pool)
            return Product.redis


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
