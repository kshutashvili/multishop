# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator

import redis
from unidecode import unidecode
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.core.management import call_command
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.template import Context
from django.utils import six
from django.utils.translation import ugettext_lazy as _, get_language
from django.template.loader import get_template
from oscar.apps.catalogue.abstract_models import (
    AbstractProduct, AbstractProductAttributeValue, AbstractProductClass,
    AbstractProductCategory, AbstractCategory, AbstractAttributeOptionGroup,
    AbstractAttributeOption, ProductManager, BrowsableProductManager, AbstractProductAttribute
)
from oscar.core.loading import get_class
from redis.exceptions import ConnectionError
from treebeard.mp_tree import MP_NodeManager
from solo.models import SingletonModel
from contacts.models import PhoneNumber, SocialNetRef

order_placed = get_class('order.signals', 'order_placed')


class EmailOnOrder(SingletonModel):

    message = models.CharField(
        max_length=250,
        verbose_name=_('Сообщение'),
        default='Кто-то оставил коментарий на ваш отзыв. Что бы просмотреть этот коментарий \n перейдите, пожалуйста, по ссылке http://{0}/{1}'
    )
    email_subject = models.CharField(
        max_length=250,
        verbose_name=_('Оповещение'),
        default='Оповещение об ответе на ваш отзыв'
    )
    subject_order = models.CharField(
        max_length=250,
        verbose_name=_('Оповещение заказа'),
        default='Order notification'
    )

    class Meta:
        verbose_name = _("Текст емеил")

    def __unicode__(self):
        return u"{}".format(self.message)



class Product(AbstractProduct):
    site = models.ForeignKey(Site, verbose_name=_('Сайт'), blank=True, null=True,
                             on_delete=models.CASCADE)

    new = models.BooleanField(verbose_name=_('Новинка'), default=False)
    top_sale = models.BooleanField(verbose_name=_('Хит продаж'), default=False)
    recommended = models.BooleanField(verbose_name=_('Рекомендуем'), default=False)
    super_price = models.BooleanField(verbose_name=_('Суперцена'), default=False)
    special_offer = models.BooleanField(verbose_name=_('Акция'), default=False)
    gift = models.BooleanField(verbose_name=_('+Подарок'), default=False)
    free_shipping = models.BooleanField(verbose_name=_('Бесплатная доставка'),
                                        default=False)

    description = RichTextField(_('Description'), blank=True)

    product_class = models.ForeignKey(
        'catalogue.ProductClass',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Product type'), related_name="products",
        help_text=_("Choose what type of product this is"))

    objects = ProductManager()
    browsable = BrowsableProductManager()

    def change_similar_products(self, recent_products):
        try:
            r = self.get_or_create_redis_connection()
            key = self.get_product_key()
            recent_product_ids = [p.id for p in recent_products]
            if r.exists(key):
                for product in recent_product_ids:
                    r.hincrby(key, product,
                              1)  # if there is no key, it will be created
            elif recent_products:
                r.hmset(key, dict.fromkeys(recent_product_ids, 1))
        except ConnectionError:
            return

    def get_similar_products(self):
        try:
            r = self.get_or_create_redis_connection()
            key = self.get_product_key()
            products = r.hgetall(key)
        except ConnectionError:
            return None
        if products:
            products = [k for k, v in
                        sorted(products.items(), key=operator.itemgetter(1),
                               reverse=True)][
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
            Product.pool = redis.ConnectionPool(host='localhost', port=6379,
                                                db=0)
            Product.redis = redis.Redis(connection_pool=Product.pool)
            return Product.redis

    def get_absolute_url(self):
        if self.categories.all().exists():
            cat = self.categories.all().first()
            slug = cat._slug_separator.join((cat.slug, self.slug))
        else:
            slug = self.slug
        return reverse('catalogue:product_or_category',
                       kwargs={'slug': slug})

    @property
    def full_slug(self):
        """Combined slug of product and it's category"""

        if self.categories.all().exists():
            cat = self.categories.all().first()
            slug = cat._slug_separator.join((cat.slug, self.slug))
        else:
            slug = self.slug

        return slug


class ProductClass(AbstractProductClass):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to='product_classes',
                              blank=True,
                              null=True, max_length=255)

    def get_absolute_url(self):
        return ''.join((reverse('catalogue:index'),
                        '?selected_facets=product_class_exact:', self.name))


class ProductCategory(AbstractProductCategory):
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True,
                             on_delete=models.CASCADE)


class Category(AbstractCategory):
    site = models.ForeignKey(
        Site,
        verbose_name=_('Сайт'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    description_title = models.CharField(
        verbose_name=_('Название статьи (описания)'),
        max_length=255,
        blank=True
    )
    description = RichTextField(
        _('Description'),
        blank=True
    )
    name_in_side_menu = models.CharField(
        _('Название в боковом меню'),
        max_length=255,
        blank=True
    )

    objects = MP_NodeManager()

    def get_absolute_url(self):
        return reverse('catalogue:product_or_category',
                       kwargs={'slug': self.full_slug})

    @property
    def side_menu_name(self):
        return self.name_in_side_menu or self.name


class ProductAttribute(AbstractProductAttribute):
    order = models.PositiveIntegerField(
        _("Порядковый номер"),
        default=0
    )

    class Meta:
        app_label = 'catalogue'
        ordering = ['order']
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.product_class.name)

    def _validate_text(self, value):
        if isinstance(value, tuple):
            # validate individual values
            for v in value:
                if v is None:
                    if self.required:
                        raise ValidationError(
                            _("%(attr)s attribute cannot be blank") %
                            {'attr': self.code})
                else:
                    self._validate_text(v)

            return

        if not isinstance(value, six.string_types):
            raise ValidationError(_("Must be str or unicode"))

    _validate_richtext = _validate_text


class ProductAttributeValue(AbstractProductAttributeValue):
    _localizable = ["text",
                    "richtext"]  # types of fields, that need to be localized

    order = models.PositiveIntegerField(_("Порядковый номер"),
                                        default=0)

    class Meta:
        app_label = 'catalogue'
        ordering = ['order']
        unique_together = ('attribute', 'product')
        verbose_name = _('Product attribute value')
        verbose_name_plural = _('Product attribute values')

    def _get_value(self):
        if self.attribute.type in ProductAttributeValue._localizable:
            return getattr(self, 'value_%s_ru' % self.attribute.type), getattr(
                self,
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
            value = getattr(self, property_name, self.value_as_text)[index]
            return value

    value = property(_get_value, AbstractProductAttributeValue._set_value)


class ExtraImage(models.Model):
    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')

    image = models.ImageField(
        _('Изображение'),
        upload_to='products/images'
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('Товар'),
        related_name='extra_images'
    )

    def __unicode__(self):
        return self.image.name


class Video(models.Model):
    class Meta:
        verbose_name = _('Видео')
        verbose_name_plural = _('Видео')

    video = models.URLField(_('Видео'), help_text=_('Вставьте url'))
    product = models.ForeignKey(
        Product,
        verbose_name=_('Товар'),
        related_name='videos'
    )

    def __unicode__(self):
        return self.video


class AttributeOptionGroup(AbstractAttributeOptionGroup):
    site = models.ForeignKey(Site, verbose_name=_('Сайт'), blank=True, null=True,
                             on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{}'.format(self.name)

    def get_name_code(self):
        return unidecode(self.name).replace(' ', '_').replace("'", '')

    def get_filter_param(self):
        return 'group_filter_{}'.format(self.get_name_code())


class AttributeOption(AbstractAttributeOption):

    def __unicode__(self):
        return '{}'.format(self.option)


class FilterDescription(models.Model):
    filter_url = models.CharField(verbose_name='URL', max_length=255)
    title = models.CharField(verbose_name=_('Заголовок'), max_length=255, blank=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True)

    class Meta:
        verbose_name = _('Статья для фильтров')
        verbose_name_plural = _('Статьи для фильтров')

    def __unicode__(self):
        return self.filter_url


@receiver(order_placed)
def on_order_create(order, user, **kwargs):
    if not order.guest_email:
        return

    plaintext = get_template('defro/order_notification.txt')
    template = get_template('defro/order_notification.html')

    order_site = order.site
    site_config = order_site.config

    context = Context({
        'order': order,
        'lines': order.basket.lines.all(),
        'cities': order_site.cities.all(),
        'site_logo': site_config.logo,
        'site_email': site_config.email,
        'social_networks_refs': SocialNetRef.objects.filter(
            site_id=order_site.id
        )
    })
    subject = _(EmailOnOrder.objects.first().subject_order)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = order.guest_email
    text_content = plaintext.render(context)
    html_content = template.render(context)
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send(fail_silently=False)
    except Exception as e:
        mail_admins('Email error', unicode(e), fail_silently=True)


def update_catalogue(sender, instance, created, **kwargs):
    if not hasattr(instance, '_no_index'):
        if created:
            call_command('rebuild_index', interactive=False)
        else:
            call_command('update_index', interactive=False)


post_save.connect(update_catalogue, Product)
post_save.connect(update_catalogue, ProductCategory)
post_save.connect(update_catalogue, Category)


from oscar.apps.catalogue.models import *
