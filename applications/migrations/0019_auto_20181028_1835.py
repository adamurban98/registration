# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-10-28 17:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0018_ambassador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambassador',
            name='phone_number',
            field=models.CharField(default='+000000000', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+#########'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='phone_number',
            field=models.CharField(default='+000000000', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:                                                                   '+#########'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
            preserve_default=False,
        ),
    ]
