# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20170512_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='default_manhour_cost',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
