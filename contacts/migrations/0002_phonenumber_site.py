# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='phonenumbers', to='sites.Site', verbose_name='\u0421\u0430\u0439\u0442'),
            preserve_default=False,
        ),
    ]
