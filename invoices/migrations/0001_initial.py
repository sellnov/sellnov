# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
            ],
            options={
                'verbose_name': 'Faktura zakupu',
                'proxy': True,
                'verbose_name_plural': 'Faktury zakupu',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='SaleInvoice',
            fields=[
            ],
            options={
                'verbose_name': 'Faktura sprzeda\u017cy',
                'proxy': True,
                'verbose_name_plural': 'Faktury sprzeda\u017cy',
            },
            bases=('documents.document',),
        ),
    ]
