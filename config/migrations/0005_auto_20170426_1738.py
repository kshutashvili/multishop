# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_configuration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='power_attribute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.ProductAttribute', verbose_name='\u041c\u043e\u0449\u043d\u043e\u0441\u0442\u044c \u043a\u043e\u0442\u043b\u0430'),
        ),
    ]
