# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20170327_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclass',
            name='name_uk',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
    ]
