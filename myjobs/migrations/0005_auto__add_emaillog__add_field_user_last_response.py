# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailLog'
        db.create_table(u'myjobs_emaillog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('received', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'myjobs', ['EmailLog'])

        # Adding field 'User.last_response'
        db.add_column(u'myjobs_user', 'last_response',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EmailLog'
        db.delete_table(u'myjobs_emaillog')

        # Deleting field 'User.last_response'
        db.delete_column(u'myjobs_user', 'last_response')


    models = {
        u'myjobs.emaillog': {
            'Meta': {'object_name': 'EmailLog'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received': ('django.db.models.fields.DateField', [], {})
        },
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'gravatar': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_response': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['myjobs']