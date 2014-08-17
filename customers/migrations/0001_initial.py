# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'customers_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userprofile.BusinessEntity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('nip', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('regon', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True)),
            ('www', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('custtype', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'customers', ['Customer'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'customers_customer')


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
        u'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'custtype': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'nip': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofile.BusinessEntity']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regon': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'www': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['customers']