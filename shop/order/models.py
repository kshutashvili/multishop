# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.order.abstract_models import AbstractOrder


class OneClickOrder(models.Model):
    class Meta:
        verbose_name = u'Заказ в один клик'
        verbose_name_plural = u'Заказы в один клик'

    when_created = models.DateTimeField(
        verbose_name=u'Когда создан',
        auto_now_add=True
    )

    product = models.ForeignKey(
        'catalogue.Product',
        verbose_name='Товар',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    basket = models.ForeignKey(
        'basket.Basket',
        verbose_name='Корзина',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон'
    )


class ShippingMethod(models.Model):
    name = models.CharField(
        verbose_name=u'Способ доставки',
        max_length=100
    )

    shipping_price = models.DecimalField(
        verbose_name=u'Стоимость доставки',
        default=0.00,
        decimal_places=2,
        max_digits=12
    )

    class Meta:
        verbose_name = u'Способ доставки'
        verbose_name_plural = u'Способы доставки'

    @property
    def shipping_incl_tax(self):
        return self.shipping_price

    @property
    def shipping_excl_tax(self):
        return self.shipping_price

    def __unicode__(self):
        return u'%s' % self.name


class PaymentMethod(models.Model):
    name = models.CharField(
        verbose_name=u'Способ оплаты',
        max_length=100
    )

    class Meta:
        verbose_name = u'Способ оплаты'
        verbose_name_plural = u'Способы оплаты'

    def __unicode__(self):
        return u'%s' % self.name


class Order(AbstractOrder):
    number = models.CharField(
        "Order number", max_length=128, db_index=True, unique=True, blank=True,
        null=True, )
    name = models.CharField(
        max_length=120,
        verbose_name=u'Имя',
    )

    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон',
    )

    comment = models.CharField(max_length=500, verbose_name=u'Комментарий',
                               blank=True, null=True)

    shipping_method = models.ForeignKey(
        'ShippingMethod',
        verbose_name='Способ доставки',
        null=True,
        on_delete=models.SET_NULL
    )
    payment_method = models.ForeignKey(
        'PaymentMethod',
        verbose_name='Способ оплаты',
        null=True,
        on_delete=models.SET_NULL
    )

    city = models.CharField(
        max_length=60,
        verbose_name=u'Город',
        blank=True,
        null=True
    )

    currency = models.CharField(
        "Currency", max_length=12, default='UAH', blank=True, null=True)

    total_excl_tax = models.DecimalField(
        _("Order total (excl. tax)"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    total_incl_tax = models.DecimalField(
        _("Order total (inc. tax)"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    shipping_incl_tax = models.DecimalField(
        _("Shipping charge (inc. tax)"), decimal_places=2, max_digits=12,
        default=0, blank=True, null=True)

    shipping_excl_tax = models.DecimalField(
        _("Shipping charge (excl. tax)"), decimal_places=2, max_digits=12,
        default=0, blank=True, null=True)

    site = models.ForeignKey(
        'sites.Site', verbose_name="Site", null=True, blank=True,
        on_delete=models.SET_NULL)

    date_placed = models.DateTimeField(db_index=True, blank=True, null=True)

    @property
    def shipping_price(self):
        return self.shipping_method.shipping_price

    @property
    def shipping_incl_tax(self):
        return self.shipping_method.shipping_price

    @property
    def shipping_excl_tax(self):
        return self.shipping_method.shipping_price

    @property
    def total_price(self):
        if self.basket.is_tax_known:
            return self.basket.total_incl_tax + self.shipping_price
        else:
            return self.basket.total_excl_tax + self.shipping_price

    @property
    def basket_total_incl_tax(self):
        return self.basket.total_incl_tax

    @property
    def basket_total_excl_tax(self):
        return self.basket.total_incl_tax

    @property
    def total_excl_tax(self):
        return self.total_price


class CallRequest(models.Model):
    class Meta:
        verbose_name = u'Заявка на звонок'
        verbose_name_plural = u'Заявки на звонки'

    name = models.CharField(max_length=120, verbose_name='Имя')
    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон'
    )
    when_created = models.DateTimeField(
        verbose_name=u'Время создания',
        auto_now_add=True,
        null=True
    )
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)


