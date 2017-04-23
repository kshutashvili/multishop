# -*-coding:utf8-*-

from django.db import models


class OneClickOrder(models.Model):
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

    phone = models.CharField(
        max_length=12,
        verbose_name=u'Телефон'
    )


from oscar.apps.order.models import *  # noqa
