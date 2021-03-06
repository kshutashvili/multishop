# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0039_auto_20170905_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productattributevalue',
            options={'ordering': ['order'], 'verbose_name': 'Product attribute value', 'verbose_name_plural': 'Product attribute values'},
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440'),
        ),
    ]
