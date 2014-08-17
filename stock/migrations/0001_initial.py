# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table(u'stock_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'stock', ['Unit'])

        # Adding model 'Tax'
        db.create_table(u'stock_tax', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal(u'stock', ['Tax'])

        # Adding model 'Product'
        db.create_table(u'stock_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userprofile.BusinessEntity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('price_net', self.gf('django.db.models.fields.DecimalField')(max_digits=22, decimal_places=2)),
            ('price_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=22, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Tax'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Unit'])),
            ('service', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pkwiu', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'stock', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Unit'
        db.delete_table(u'stock_unit')

        # Deleting model 'Tax'
        db.delete_table(u'stock_tax')

        # Deleting model 'Product'
        db.delete_table(u'stock_product')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stock.product': {
            'Meta': {'object_name': 'Product'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofile.BusinessEntity']"}),
            'pkwiu': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'price_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '22', 'decimal_places': '2'}),
            'price_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '22', 'decimal_places': '2'}),
            'service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Tax']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Unit']"})
        },
        u'stock.tax': {
            'Meta': {'object_name': 'Tax'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        u'stock.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'userprofile.businessentity': {
            'Meta': {'object_name': 'BusinessEntity'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'employers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'works_in'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'iban': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'nip': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regon': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['stock']