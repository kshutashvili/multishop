# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0022_auto_20170617_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpage',
            name='slug_ru',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='flatpage',
            name='slug_uk',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
