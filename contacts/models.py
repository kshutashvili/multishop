# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import phonenumbers
from ckeditor.fields import RichTextField
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

SIGN_TYPE = (
    ('w', _('Бесцветный значок')),
    ('c', _('Цветной значок')),
)


class City(models.Model):
    city_name = models.CharField(_('Город'), max_length=50)
    slug = models.SlugField(_('Название-метка для URL'), max_length=80, unique=True)
    address = models.CharField(_('Адрес'), max_length=70,
                               default=_('ул. Смелянская 159/3'))
    site = models.ForeignKey(Site,
                             verbose_name=_('Сайт'),
                             related_name='cities',
                             default=1)
    google_maps_api_key = models.CharField(_('Ключ API карт Google'), blank=True,
                                           max_length=200)

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    def __unicode__(self):
        return self.city_name

    def has_map(self):
        return bool(self.address and self.google_maps_api_key)


class PhoneNumber(models.Model):
    class OPERATOR:
        KIEVSTAR = 'kievstar'
        LIFE = 'life'
        VODAFONE = 'vodafone'
        _CHOICES = ((KIEVSTAR, _('Kievstar')),
                    (LIFE, _('Life')),
                    (VODAFONE, _('Vodafone')))

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12,15}$',
        message=_("Номер телефона должен быть введен в формате:"
                  "'+999999999999'. Допускается до 15 цифр в номере")
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
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

    city = models.ForeignKey(City,
                             verbose_name='Город',
                             related_name="phones",
                             blank=True,
                             null=True)

    class Meta:
        verbose_name = _('Номер телефона')
        verbose_name_plural = _('Номера телефонов')

    def __unicode__(self):
        return self.phone

    def get_national_format(self, country=None):
        phone_obj = phonenumbers.parse(self.phone, country)
        return phonenumbers.format_number(
            phone_obj, phonenumbers.PhoneNumberFormat.NATIONAL)


class SocialNetRef(models.Model):
    class REFTYPES:
        FACEBOOK = 'facebook'
        VKONTAKTE = 'vkontakte'
        MAILRU = 'mailru'
        TWITTER = 'twitter'
        ODNOKLASSNIKI = 'odnoklassniki'
        PINTEREST = 'pinterest'
        GOOGLE = 'google'
        YOUTUBE = 'youtube'
        _CHOICES = ((FACEBOOK, _('facebook')),
                    (VKONTAKTE, _('ВКонтакте')),
                    (MAILRU, _('mail.ru')),
                    (TWITTER, _('Twitter')),
                    (ODNOKLASSNIKI, _('Одноклассники')),
                    (PINTEREST, _('Pinterest')),
                    (GOOGLE, _('Google+')),
                    (YOUTUBE, _('YouTube')))

    ref_type = models.CharField(
        _('Оператор'),
        max_length=20,
        choices=REFTYPES._CHOICES,
        default=REFTYPES.FACEBOOK
    )
    reference = models.URLField(_('Ссылка'))
    site = models.ForeignKey(
        Site,
        verbose_name=_('Сайт'),
        related_name='socialnetrefs'
    )

    class Meta:
        verbose_name = _('Ссылка на социальную сеть')
        verbose_name_plural = _('Ссылки на социальные сети')

    def __unicode__(self):
        return '{} {}'.format(self.ref_type, self.reference)


class Timetable(models.Model):
    weekdays = models.CharField(
        _('Дни недели'),
        max_length=100
    )
    daytime = models.CharField(
        _('Время дня'),
        max_length=100
    )
    city = models.ForeignKey(City,
                             verbose_name='Город',
                             related_name="timetables",
                             blank=True,
                             null=True)

    class Meta:
        verbose_name = _('График работы')
        verbose_name_plural = _('Графики работы')

    def __unicode__(self):
        return '{} {}'.format(self.weekdays, self.daytime)


class WorkSchedule(models.Model):
    class SCHEDULETYPES:
        MAIN = 'main'
        CALLCENTER = 'callcenter'
        NIGHTORDERS = 'nightorders'
        _CHOICES = ((MAIN, _('основное')),
                    (CALLCENTER, _('для call center')),
                    (NIGHTORDERS, _('для ночных заказов')))

    schedule_type = models.CharField(
        _('Тип рассписания'),
        max_length=20,
        choices=SCHEDULETYPES._CHOICES,
        default=SCHEDULETYPES.MAIN
    )
    timetable = models.ManyToManyField(
        Timetable,
        verbose_name=_('Графики'),
        related_name='workschedules'
    )
    site = models.ForeignKey(
        Site,
        verbose_name=_('Сайт'),
        related_name='workschedules'
    )
    city = models.ForeignKey(City,
                             verbose_name='Город',
                             related_name="schedules",
                             blank=True,
                             null=True)

    class Meta:
        verbose_name = _('Рассписание работы компании')
        verbose_name_plural = _('Рассписания работы компании')

    def __unicode__(self):
        return '{} {}'.format(self.schedule_type, self.site)


class ContactMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12,15}$',
        message=_("Номер телефона должен быть введен в формате:"
                  "'+999999999999'. Допускается до 15 цифр в номере")
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
    )
    message = models.TextField()

    site = models.ForeignKey(
        Site,
        verbose_name=_('Сайт'),
        blank=True, null=True
    )


class FlatPage(models.Model):
    title = models.CharField('Название', max_length=80)
    content = RichTextField('Текст')
    slug = models.SlugField(unique=True)
    when_created = models.DateTimeField('Дата создания', auto_now_add=True)
    site = models.ManyToManyField(Site, verbose_name='Сайт', blank=True,
                                  null=True, related_name='flatpages')

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'
        db_table = 'contacts_flatpages'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flatpage_detail', kwargs={'flatpage_slug': self.slug})

