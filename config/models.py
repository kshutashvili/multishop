# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SiteConfig(models.Model):
    class TEMPLATES:
        TEMP = 0
        _CHOICES = ((TEMP, '/path/to/template'),
                    )

    template = models.PositiveSmallIntegerField(verbose_name='шаблон',
                                                null=True,
                                                blank=True,
                                                choices=TEMPLATES._CHOICES,
                                                default=TEMPLATES.TEMP)
    site = models.OneToOneField(Site, verbose_name='сайт',
                                on_delete=models.CASCADE,
                                related_name='site_config')

    def __unicode__(self):
        return self.site.domain


@receiver(post_save, sender=Site)
def create_or_update_site_config(sender, instance, created, **kwargs):
    if created:
        SiteConfig.objects.create(site=instance)
    instance.site_config.save()
