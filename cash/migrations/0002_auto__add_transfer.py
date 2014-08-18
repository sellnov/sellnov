# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transfer'
        db.create_table(u'cash_transfer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cash.Account'])),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cash.Operation'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'cash', ['Transfer'])


    def backwards(self, orm):
        # Deleting model 'Transfer'
        db.delete_table(u'cash_transfer')


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