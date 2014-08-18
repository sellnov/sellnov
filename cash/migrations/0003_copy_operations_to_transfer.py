# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        db.execute('''insert into cash_transfer (account_id, amount, operation_id)
            select account_id, amount, id from cash_operation''')

    def backwards(self, orm):
        "Write your backwards methods here."
        db.execute('''truncate cash_transfer''')

    models = {
        u'cash.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'cash.operation': {
            'Meta': {'ordering': "('date', '-created')", 'object_name': 'Operation'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cash.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'estimated_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cash.Operation']", 'null': 'True', 'blank': 'True'}),
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
    symmetrical = True
