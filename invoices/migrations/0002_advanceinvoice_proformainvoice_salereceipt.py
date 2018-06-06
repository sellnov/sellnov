# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_line_advance_payment'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvanceInvoice',
            fields=[
            ],
            options={
                'verbose_name': 'Faktura zaliczkowa',
                'proxy': True,
                'verbose_name_plural': 'Faktury zaliczkowe',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='ProFormaInvoice',
            fields=[
            ],
            options={
                'verbose_name': 'Faktura ProForma',
                'proxy': True,
                'verbose_name_plural': 'Faktury ProForma',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='SaleReceipt',
            fields=[
            ],
            options={
                'verbose_name': 'Paragon',
                'proxy': True,
                'verbose_name_plural': 'Paragony',
            },
            bases=('documents.document',),
        ),
    ]
