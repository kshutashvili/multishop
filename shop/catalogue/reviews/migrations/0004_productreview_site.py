# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('reviews', '0003_auto_20160802_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.Site', verbose_name=b'\xd0\xa1\xd0\xb0\xd0\xb9\xd1\x82'),
        ),
    ]
