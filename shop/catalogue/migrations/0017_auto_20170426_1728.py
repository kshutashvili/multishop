# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_category_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.URLField(help_text=b'\xd0\x92\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd1\x8c\xd1\x82\xd0\xb5 url', verbose_name=b'\xd0\x92\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe'),
        ),
    ]
