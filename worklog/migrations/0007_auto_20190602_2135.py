# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0006_auto_20190602_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='valuationitem',
            options={'verbose_name': 'element wyceny', 'verbose_name_plural': 'elementy wyceny'},
        ),
        migrations.AlterField(
            model_name='valuation',
            name='date',
            field=models.DateField(verbose_name=b'data wyceny'),
        ),
        migrations.AlterField(
            model_name='valuation',
            name='expiration_date',
            field=models.DateField(verbose_name='wa\u017cno\u015b\u0107 wyceny'),
        ),
        migrations.AlterField(
            model_name='valuation',
            name='title',
            field=models.CharField(max_length=128, verbose_name='tytu\u0142 oferty'),
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='max_hours',
            field=models.PositiveIntegerField(verbose_name=b'max godziny'),
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='min_hours',
            field=models.PositiveIntegerField(verbose_name=b'min godziny'),
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='notes',
            field=models.CharField(max_length=255, verbose_name=b'uwagi', blank=True),
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='role',
            field=models.ForeignKey(
                verbose_name=b'rola', to='userprofile.Role',
                on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name='valuationitem',
            name='valuation',
            field=models.ForeignKey(
                verbose_name=b'wycena', to='worklog.Valuation',
                on_delete=models.CASCADE),
        ),
    ]
