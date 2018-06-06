# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_line_advance_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='parent',
            field=models.ForeignKey(verbose_name=b'Dokument powi\xc4\x85zany (nadrz\xc4\x99dny)', blank=True, to='documents.Document', null=True),
        ),
    ]
