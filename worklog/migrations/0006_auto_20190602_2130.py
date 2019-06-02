# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0005_auto_20190602_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='valuation',
            options={'verbose_name': 'wycena', 'verbose_name_plural': 'wyceny'},
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='notes',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
