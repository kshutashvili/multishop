# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SiteConfig(models.Model):
    class TEMPLATES:
        DEFRO = 0
        _CHOICES = ((DEFRO, 'defro'),
                    )

    template = models.PositiveSmallIntegerField(verbose_name='шаблон',
                                                null=True,
                                                blank=True,
                                                choices=TEMPLATES._CHOICES,
                                                default=TEMPLATES.DEFRO)

    site = models.OneToOneField(Site, verbose_name='сайт',
                                on_delete=models.CASCADE,
                                related_name='site_config')

    def get_template(self):
        choices = dict(SiteConfig.TEMPLATES._CHOICES)
        return choices[self.template]

    def __unicode__(self):
        return self.site.domain


@receiver(post_save, sender=Site)
def create_or_update_site_config(sender, instance, created, **kwargs):
    if created:
        SiteConfig.objects.create(site=instance)
    instance.site_config.save()
