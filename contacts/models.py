# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


SIGN_TYPE = (
    ('w', _('Бесцветный значок')),
    ('c', _('Цветной значок')),
)


class PhoneNumber(models.Model):
    class OPERATOR:
        KIEVSTAR = 'kievstar'
        LIFE = 'life'
        VODAFONE = 'vodafone'
        _CHOICES = ((KIEVSTAR, _('Kievstar')),
                    (LIFE, _('Life')),
                    (VODAFONE, _('Vodafone')))

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Номер телефона должен быть введен в формате: '+999999999'. "
                  "Допускается до 15 цифр в номере")
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        blank=True
    )
    operator = models.CharField(
        _('Оператор'),
        max_length=20,
        choices=OPERATOR._CHOICES,
        default=OPERATOR.KIEVSTAR
    )
    sign = models.CharField(max_length=1, choices=SIGN_TYPE, default='c')
    site = models.ForeignKey(
        Site,
        verbose_name=_('Сайт'),
        related_name='phonenumbers'
    )

    def __unicode__(self):
        return self.phone
