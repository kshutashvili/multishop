# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0019_city_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='sites.Site', verbose_name='\u0421\u0430\u0439\u0442'),
        ),
    ]
