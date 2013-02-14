# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SavedSearch'
        db.create_table(u'mysearches_savedsearch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('feed', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='W', max_length=2)),
            ('day_of_month', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('day_of_week', self.gf('django.db.models.fields.CharField')(default='Mo', max_length=2, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mysearches', ['SavedSearch'])


    def backwards(self, orm):
        # Deleting model 'SavedSearch'
        db.delete_table(u'mysearches_savedsearch')


    models = {
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'mysearches.savedsearch': {
            'Meta': {'object_name': 'SavedSearch'},
            'day_of_month': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'day_of_week': ('django.db.models.fields.CharField', [], {'default': "'Mo'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        }
    }

    complete_apps = ['mysearches']