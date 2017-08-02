# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-02 06:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0031_removed_translated_slug_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phonenumbers', to='sites.Site', verbose_name='\u0421\u0430\u0439\u0442'),
        ),
    ]
