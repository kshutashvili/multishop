# -*-coding:utf8-*-

from django.db import models


class OneClickOrder(models.Model):
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

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


class SimpleOrder(models.Model):
    STATUS_CHOICES = (
        (1, u'Отменен'),
        (2, u'В стадии обработки'),
        (3, u'На производстве'),
        (4, u'Огружен'),
        (5, u'Выполнен'),
    )

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

    when_created = models.DateTimeField(
        verbose_name=u'Время создания',
        auto_now_add=True,
    )
    basket = models.ForeignKey(
        'basket.Basket',
        verbose_name=u'Корзина',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    order_status = models.IntegerField(
        verbose_name=u'Статус',
        choices=STATUS_CHOICES,
        default=2
    )

    name = models.CharField(
        max_length=50,
        verbose_name=u'Имя'
    )
    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон',
    )
    comment = models.TextField(blank=True, null=True,
                               verbose_name=u'Коментарий')

    email = models.EmailField(
        max_length=50,
        verbose_name=u'E-mail',
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=60,
        verbose_name=u'Город',
        blank=True,
        null=True
    )
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

    @property
    def shipping_price(self):
        return self.shipping_method.shipping_price

    @property
    def total_price(self):
        if self.basket.is_tax_known:
            return self.basket.total_incl_tax + self.shipping_price
        else:
            return self.basket.total_excl_tax + self.shipping_price

    def __unicode__(self):
        return '%s %s' % (self.when_created, self.order_status)


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


from oscar.apps.order.models import *  # noqa
