# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy

from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview
from django.contrib.sites.models import Site
from oscar.core import validators
from shop.catalogue.models import Product


class ProductReview(AbstractProductReview):
    title = models.CharField(
        verbose_name=pgettext_lazy(u"Product review title", u"Title"),
        max_length=255,
        validators=[validators.non_whitespace],
        blank=True
    )
    site = models.ForeignKey(Site, verbose_name='Сайт', blank=True, null=True)
    advantage = models.TextField('Преимущества', blank=True)
    disadvantage = models.TextField('Недостатки', blank=True)
    get_notification = models.BooleanField(
        'Получать уведомления об ответах',
        default=False
    )
    reply_to = models.ForeignKey('self', blank=True, null=True)


@receiver(post_save, sender=ProductReview)
def on_review_create(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        review = sender.objects.get(pk=instance.reply_to,
                                    get_notification=True)
    except ObjectDoesNotExist:
        return
    to_email = review.email or review.user.email
    message = 'Your review has been commented, please follow the reference' \
              'to see the the comment http://{0}/{1}'.format(
                  instance.site, instance.product.get_absolute_url)
    send_mail('Notification about your review',
              message,
              settings.DEFAULT_FROM_EMAIL,
              [to_email],
              fail_silently=True)


class ProductQuestion(models.Model):
    class Meta:
        verbose_name = 'Вопрос о товаре'
        verbose_name_plural = 'Вопросы о товаре'
    product = models.ForeignKey(Product,
                                verbose_name="Товар",
                                on_delete=models.CASCADE)
    when_created = models.DateTimeField('Дата и время создания',
                                        auto_now_add=True)
    name = models.CharField('Имя', max_length=128)
    email = models.EmailField('Почта', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=10)
    text = models.TextField('Вопрос')

    def __unicode__(self):
        return u'{} - {}'.format(self.name, self.when_created)

from oscar.apps.catalogue.reviews.models import *  # noqa
