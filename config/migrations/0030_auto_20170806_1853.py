# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-06 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0029_auto_20170806_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefititem',
            name='text_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0422\u0435\u043a\u0441\u0442'),
        ),
        migrations.AddField(
            model_name='benefititem',
            name='text_uk',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0422\u0435\u043a\u0441\u0442'),
        ),
    ]
