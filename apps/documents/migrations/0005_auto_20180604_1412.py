# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20180604_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='advance_payment',
        ),
        migrations.AddField(
            model_name='line',
            name='advance_payment_gross',
            field=models.DecimalField(default=0, verbose_name=b'Zaliczka brutto', max_digits=22, decimal_places=2),
        ),
        migrations.AddField(
            model_name='line',
            name='advance_payment_net',
            field=models.DecimalField(default=0, verbose_name=b'Zaliczka', max_digits=22, decimal_places=2),
        ),
    ]
