# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0017_auto_20171024_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='none', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('f', 'Facebook'), ('d', 'Django')], max_length=1),
        ),
    ]
