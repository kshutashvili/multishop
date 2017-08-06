# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from solo.models import SingletonModel

from shop.catalogue.models import ProductAttribute
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class SiteConfig(models.Model):
    class TEMPLATES:
        DEFRO = 'defro'
        BLUE = 'blue'
        _CHOICES = ((DEFRO, 'Defro'),
                    (BLUE, 'Blue'),
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

    power_attribute = models.ForeignKey(ProductAttribute,
                                        on_delete=models.SET_NULL,
                                        verbose_name='Атрибут мощности котла',
                                        null=True)

    brand_attribute = models.ForeignKey(ProductAttribute,
                                        related_name='brand_config',
                                        on_delete=models.SET_NULL,
                                        verbose_name="Атрибут бренда котла",
                                        null=True)

    def __unicode__(self):
        return self.site.domain


@receiver(post_save, sender=Site)
def create_or_update_site_config(sender, instance, created, **kwargs):
    if created:
        SiteConfig.objects.create(site=instance)
    instance.config.save()


class Configuration(SingletonModel):
        undercat_block_url = models.CharField('Ссылка под каталогом',
                                              max_length=128,
                                              blank=True)
        show_calculator = models.BooleanField("Отображать калькулятор котлов?",
                                              default=False)
        show_benefits = models.BooleanField("Отображать блок 'Преимуществ'?",
                                            default=False)
        show_credit = models.BooleanField("Отображать блок 'Кредит'?",
                                          default=False)
        credit_block_text = models.CharField("Текст для блока 'Кредит'",
                                             max_length=210,
                                             blank=True)
        show_reviews = models.BooleanField("Отображать блок 'Обзоры и отзывы'?",
                                           default=False)
        show_advanced = models.BooleanField("Отображать блок 'Дополнительные услуги'?",
                                            default=False)

        class Meta:
            verbose_name = "Настройки главной страницы"


class FuelConfiguration(models.Model):
    FUEL_TYPES = (
        ('wood', 'Дрова'),
        ('pellets', 'Пеллеты'),
        ('coal', 'Каменный уголь'),
        ('brown_coal', 'Бурый уголь'),
        ('gas', 'Газ'),
        ('electricity', 'Электроэнергия'),
        ('diesel', 'Дизельное топливо')
    )
    config = models.ForeignKey(Configuration,
                               verbose_name="Настройки главной страницы",
                               related_name="fuels")
    fuel_type = models.CharField("Вид топлива",
                                 max_length=20,
                                 choices=FUEL_TYPES,
                                 default='wood')
    fuel_cost = models.DecimalField("Цена",
                                    decimal_places=2,
                                    max_digits=7)

    class Meta:
        verbose_name = 'Объем и цена топлива'
        verbose_name_plural = 'Объемы и цены топлива'

    def __unicode__(self):
        return self.fuel_type


class BenefitItem(models.Model):
    config = models.ForeignKey(Configuration,
                               verbose_name="Настройки главной страницы",
                               related_name="benefits")
    image = models.ImageField("Изображение",
                              blank=True,
                              upload_to='benefit_images')
    text = models.CharField("Текст",
                            max_length=200)

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'

    def __unicode__(self):
        return self.text


class OverviewItem(models.Model):
    config = models.ForeignKey(Configuration,
                               verbose_name="Настройки главной страницы",
                               related_name="overviews")
    link = models.CharField("Ссылка на обзор",
                             max_length=200)

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __unicode__(self):
        return self.link


class ReviewItem(models.Model):
    config = models.ForeignKey(Configuration,
                               verbose_name="Настройки главной страницы",
                               related_name="reviews")
    photo = models.ImageField("Фото",
                             blank=True)
    name = models.CharField("Имя оставившего отзыв",
                            max_length=50)
    text = models.TextField("Текст отзыва")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __unicode__(self):
        return self.name


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


class ModelMetaTag(models.Model):

    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок',
    )
    title_meta = models.CharField(
        max_length=250,
        verbose_name='Meta title',
    )
    description_meta = models.TextField(
        verbose_name='Meta description'
    )
    h1 = models.CharField(
        max_length=250,
        verbose_name='H1 заголовок',
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('product', 'category', )
        }
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = (('content_type', 'object_id'))
        verbose_name = 'Мета тегы для обьекта'
        verbose_name_plural = 'Мета тегы для обьектов'

    def __unicode__(self):
        return '{} - {}'.format(self.content_object, self.title)
