# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0014_flatpage_site'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flatpage',
            old_name='url',
            new_name='slug',
        ),
    ]