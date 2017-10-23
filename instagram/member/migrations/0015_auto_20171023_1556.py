# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_relationship_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='block',
            field=models.CharField(choices=[('Block', 'Block'), ('Friend', 'Friend'), ('Acquaintance', 'Acquaintance')], max_length=20),
        ),
    ]
