# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_document_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='advance_payment',
            field=models.DecimalField(default=0, max_digits=22, decimal_places=2),
        ),
    ]
