# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_product_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='notes',
            field=models.CharField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
