# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy

from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview
from django.contrib.sites.models import Site
from oscar.core import validators


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
        return None
    if instance.reply_to:
        review = sender.objects.get_object_or_404(pk=instance.reply_to)
        if review.get_notification:
            if instance.email:
                email_from = instance.email
            else:
                email_from = instance.user.email
            if review.email:
                email_to = review.email
            else:
                email_to = review.user.email
            send_mail('Notification about your review',
                      'Your review has been commented',
                      email_from,
                      [email_to],
                      fail_silently=False)

from oscar.apps.catalogue.reviews.models import *  # noqa
