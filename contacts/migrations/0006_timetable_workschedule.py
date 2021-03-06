# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 08:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contacts', '0005_auto_20170413_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekdays', models.CharField(max_length=100, verbose_name='\u0414\u043d\u0438 \u043d\u0435\u0434\u0435\u043b\u0438')),
                ('daytime', models.CharField(max_length=100, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0434\u043d\u044f')),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_type', models.CharField(choices=[('main', '\u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0435'), ('callcenter', '\u0434\u043b\u044f call center'), ('nightorders', '\u0434\u043b\u044f \u043d\u043e\u0447\u043d\u044b\u0445 \u0437\u0430\u043a\u0430\u0437\u043e\u0432')], default='main', max_length=20, verbose_name='\u0422\u0438\u043f \u0440\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='sites.Site', verbose_name='\u0421\u0430\u0439\u0442')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workschedules', to='contacts.Timetable', verbose_name='\u0420\u044b\u0431\u043d\u043e\u0435 \u043c\u0435\u0441\u0442\u043e')),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438',
            },
        ),
    ]
