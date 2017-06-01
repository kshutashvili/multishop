# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-01 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20160107_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockrecord',
            name='previous_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Previous Price'),
        ),
    ]
