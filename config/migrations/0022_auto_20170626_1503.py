# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-26 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_auto_20170616_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='template',
            field=models.CharField(blank=True, choices=[('defro', 'Defro'), ('blue', 'Blue')], default='defro', max_length=20, null=True, verbose_name='\u0448\u0430\u0431\u043b\u043e\u043d'),
        ),
    ]
