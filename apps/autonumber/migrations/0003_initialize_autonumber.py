# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autonumber', '0002_autonumber_reset_by'),
        ('documents', '0001_initial'),
    ]

    operations = [
            migrations.RunSQL(
                '''
                insert into autonumber_autonumber (
                    document_type, last_number, last_date, reset_by)
                select doctype, number, issue_date, 'year' from (
                with numbers as (
                    select row_number() over (
                        partition by doctype
                        order by issue_date desc, number desc
                        ) as row_number, number, issue_date, doctype
                    from documents_document
                    ) select * from numbers where row_number = 1) x
                ''', 'delete from autonumber_autonumber'),
                ]
