# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 19:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_auto_20170517_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_excl_tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_incl_tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_excl_tax',
        ),
    ]
