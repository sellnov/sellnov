# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0002_entry_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='invoices.SaleInvoice', null=True),
        ),
    ]
