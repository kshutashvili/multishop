# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from solo.models import SingletonModel

from shop.catalogue.models import ProductAttributeValue
from oscar.apps.catalogue.models import ProductAttribute


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
    email = models.EmailField('email address', unique=True)

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
