# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from solo.models import SingletonModel

from shop.catalogue.models import ProductAttribute


class SiteConfig(models.Model):
    class TEMPLATES:
        DEFRO = 'defro'
        _CHOICES = ((DEFRO, 'Defro'),
                    )

    template = models.CharField(verbose_name='шаблон',
                                max_length=20,
                                null=True,
                                blank=True,
                                choices=TEMPLATES._CHOICES,
                                default=TEMPLATES.DEFRO)

    site = models.OneToOneField(Site, verbose_name='сайт',
                                on_delete=models.CASCADE,
                                related_name='config')
    email = models.EmailField('email адрес')

    copyright = models.CharField(verbose_name='Copyright',
                                 max_length=100,
                                 null=True,
                                 blank=True)

    logo = models.ImageField('Логотип', blank=True, null=True)

    def __unicode__(self):
        return self.site.domain


@receiver(post_save, sender=Site)
def create_or_update_site_config(sender, instance, created, **kwargs):
    if created:
        SiteConfig.objects.create(site=instance)
    instance.config.save()


class Configuration(SingletonModel):
        class Meta:
            verbose_name = "Конфигурация"
        power_attribute = models.ForeignKey(ProductAttribute,
                                            on_delete=models.SET_NULL,
                                            verbose_name="Мощность котла",
                                            null=True)
        brand_attribute = models.ForeignKey(ProductAttribute,
                                            related_name='brand_config',
                                            on_delete=models.SET_NULL,
                                            verbose_name="Поле бренда котла",
                                            null=True)
        undercat_block_url = models.CharField('Ссылка под каталогом',
                                              max_length=128,
                                              blank=True)


class MenuCategory(models.Model):
    class Meta:
        verbose_name = 'Категория меню'
        verbose_name_plural = 'Категории меню'
    name = models.CharField('Название', max_length=50)
    order = models.IntegerField('Порядок', default=0)

    def __unicode__(self):
        return self.name


class MenuItemQuerySet(models.QuerySet):
    def active(self, *args, **kwargs):
        kwargs['is_active'] = True
        return self.filter(*args, **kwargs).order_by('order')

    def in_header(self, *args, **kwargs):
        kwargs['position'] = MenuItem.POSITION.HEADER
        return self.filter(*args, **kwargs)

    def in_footer(self, *args, **kwargs):
        kwargs['position'] = MenuItem.POSITION.FOOTER
        return self.filter(*args, **kwargs)


class MenuItem(models.Model):
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    class POSITION:
        HEADER = 'header'
        FOOTER = 'footer'
        _CHOICES = ((HEADER, 'Header'),
                    (FOOTER, 'Footer'))

    position = models.CharField('Расположение', max_length=128,
                                default=POSITION.HEADER,
                                choices=POSITION._CHOICES)
    name = models.CharField('Название', max_length=50)
    link = models.CharField('Ссылка', max_length=255, blank=True)
    order = models.IntegerField('Порядок', default=0)
    category = models.ForeignKey(MenuCategory, verbose_name='Категория',
                                 on_delete=models.CASCADE,
                                 max_length=255, blank=True, null=True)
    site = models.ForeignKey(Site, verbose_name='Сайт',
                             on_delete=models.CASCADE,
                             max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Отображается на сайте', default=True)

    objects = MenuItemQuerySet.as_manager()

    def __unicode__(self):
        return self.name


class UndercatText(models.Model):
    class Meta:
        abstract = True
    text = models.TextField('Текст')
    site = models.ForeignKey(Site, verbose_name='Сайт',
                             on_delete=models.CASCADE,
                             max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Отображается на сайте', default=True)

    def __unicode__(self):
        return self.text

    def to_show(self, site_obj):
        if self.is_active and ((self.site == site_obj) or self.site is None):
            return self.text
        else:
            return ''


class TextOne(UndercatText):
    class Meta:
        verbose_name = 'Текст 1'
        verbose_name_plural = 'Тексты 1'


class TextTwo(UndercatText):
    class Meta:
        verbose_name = 'Текст 2'
        verbose_name_plural = 'Тексты 2'


class TextThree(UndercatText):
    class Meta:
        verbose_name = 'Текст 3'
        verbose_name_plural = 'Тексты 3'


class TextFour(UndercatText):
    class Meta:
        verbose_name = 'Текст 4'
        verbose_name_plural = 'Тексты 4'


class MetaTag(models.Model):
    MAIN_PAGE = 'MP'
    SECTION = 'SC'
    SUB_SECTION = 'SS'
    CATEGORY = 'CA'
    BRAND = 'BR'
    BRAND_FILTER = 'BF'
    PRODUCT = 'PD'
    FLAT_PAGE = 'FP'

    META_TYPE_CHOICES = (
        (MAIN_PAGE, 'Главная страница'),
        (SECTION, 'Раздел'),
        (SUB_SECTION, 'Подраздел'),
        (CATEGORY, 'Категория'),
        (BRAND, 'Бренд'),
        (BRAND_FILTER, 'Бренд + фильтр'),
        (PRODUCT, 'Товар'),
        (FLAT_PAGE, 'Статистическая страница')
    )
    title = models.CharField(
        max_length=250,
        default='[title]',
        verbose_name='Заголовок',
    )
    title_meta = models.CharField(
        max_length=250,
        default='[title]',
        verbose_name='Meta title',
    )
    description_meta = models.TextField(
        default='[title]',
        verbose_name='Meta description'
    )
    h1 = models.CharField(
        max_length=250,
        default='[title]',
        verbose_name='H1 заголовок',
    )
    type = models.CharField(
        max_length=2,
        choices=META_TYPE_CHOICES,
        verbose_name='Тип страницы',
        unique=True,
    )

    class Meta:
        verbose_name = "Мета тег"
        verbose_name_plural = "Мета теги"

    def __unicode__(self):
        return u"{} - {}".format(self.get_type_display(), self.title)
