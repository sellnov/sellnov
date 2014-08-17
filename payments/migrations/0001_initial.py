# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentType'
        db.create_table(u'payments_paymenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transfer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('due_days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'payments', ['PaymentType'])


    def backwards(self, orm):
        # Deleting model 'PaymentType'
        db.delete_table(u'payments_paymenttype')


    models = {
        u'payments.paymenttype': {
            'Meta': {'object_name': 'PaymentType'},
            'due_days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transfer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['payments']