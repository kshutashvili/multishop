# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-18 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0024_auto_20170618_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPageTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('slug', models.SlugField(unique=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contacts.FlatPage')),
            ],
            options={
                'managed': True,
                'db_table': 'contacts_flatpages_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': '\u0421\u0442\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flatpagetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]