# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='advance_payment',
            field=models.DecimalField(default=0, max_digits=22, decimal_places=2),
            preserve_default=False,
        ),
    ]
