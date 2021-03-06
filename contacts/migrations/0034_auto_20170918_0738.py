# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-18 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contacts', '0033_side_menu_config_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workschedule',
            options={'verbose_name': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438', 'verbose_name_plural': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438'},
        ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.SlugField(max_length=80, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435-\u043c\u0435\u0442\u043a\u0430 \u0434\u043b\u044f URL'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('site', 'slug')]),
        ),
    ]
