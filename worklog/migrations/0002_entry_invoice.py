# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_advanceinvoice_proformainvoice_salereceipt'),
        ('worklog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='invoice',
            field=models.ForeignKey(blank=True, to='invoices.SaleInvoice', null=True),
        ),
    ]
