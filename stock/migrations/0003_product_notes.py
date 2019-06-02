# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='notes',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
