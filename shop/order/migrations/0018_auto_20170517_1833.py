# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20170517_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simpleorder',
            name='basket',
        ),
        migrations.RemoveField(
            model_name='simpleorder',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='simpleorder',
            name='shipping_method',
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=12, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.DeleteModel(
            name='ShippingMethod',
        ),
        migrations.DeleteModel(
            name='SimpleOrder',
        ),
    ]
