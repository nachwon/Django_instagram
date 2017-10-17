# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 02:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20171017_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(related_name='post_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
