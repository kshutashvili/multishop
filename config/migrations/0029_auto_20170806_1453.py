# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-06 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0028_remove_fuelconfiguration_fuel_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewitem',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='configuration',
            name='credit_block_text',
            field=models.CharField(blank=True, max_length=220, verbose_name="\u0422\u0435\u043a\u0441\u0442 \u0434\u043b\u044f \u0431\u043b\u043e\u043a\u0430 '\u041a\u0440\u0435\u0434\u0438\u0442'"),
        ),
    ]