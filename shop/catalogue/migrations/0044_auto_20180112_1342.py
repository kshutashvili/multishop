# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-12 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0043_auto_20171107_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributeoptiongroup',
            name='name_ru',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='attributeoptiongroup',
            name='name_uk',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
    ]
