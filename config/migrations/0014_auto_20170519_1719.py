# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0013_auto_20170514_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='name_uk',
            field=models.CharField(max_length=50, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
