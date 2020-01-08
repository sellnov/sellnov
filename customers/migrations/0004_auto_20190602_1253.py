# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_default_manhour_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='default_manhour_cost',
            new_name='default_manhour_price',
        ),
    ]
