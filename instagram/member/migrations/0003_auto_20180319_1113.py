# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-19 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20171114_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('f', 'Facebook'), ('d', 'Django')], default='d', max_length=1),
        ),
    ]
