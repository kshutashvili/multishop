# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0017_auto_20170426_1728'),
        ('config', '0003_siteconfig_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.ProductAttribute')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f',
            },
        ),
    ]
