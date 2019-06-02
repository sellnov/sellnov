# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20190602_2045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'grupa towarowa', 'verbose_name_plural': 'grupy towarowe'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Towar i us\u0142uga', 'verbose_name_plural': 'Towary i us\u0142ugi'},
        ),
    ]
