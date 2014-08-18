# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute('''create view cash_transfer_with_balance_view as
            select extract(year from date) as year, extract(month from date) as month,
                cash_transfer.*, sum(amount) over (order by date,created desc, amount) as balance 
            from cash_transfer 
            inner join cash_operation on operation_id = cash_operation.id 
            order by date,created desc, amount
            ''')

    def backwards(self, orm):
        db.execute('drop view cash_transfer_with_balance_view')

    models = {
        u'cash.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'cash.operation': {
            'Meta': {'ordering': "('date', '-created')", 'object_name': 'Operation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'estimated_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'cash.transfer': {
            'Meta': {'object_name': 'Transfer'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cash.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cash.Operation']"})
        }
    }

    complete_apps = ['cash']
