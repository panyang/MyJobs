# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteViewer'
        db.create_table(u'myanalytics_siteviewer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('aguid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('myjobs_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'myanalytics', ['SiteViewer'])

        # Adding model 'SiteView'
        db.create_table(u'myanalytics_siteview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('viewed', self.gf('django.db.models.fields.DateTimeField')()),
            ('site_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('search_parameters', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_codes', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('view_source', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('resolution_w', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('resolution_h', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('viewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myanalytics.SiteViewer'])),
            ('user_agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myanalytics.UserAgent'])),
        ))
        db.send_create_signal(u'myanalytics', ['SiteView'])

        # Adding model 'UserAgent'
        db.create_table(u'myanalytics_useragent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'myanalytics', ['UserAgent'])


    def backwards(self, orm):
        # Deleting model 'SiteViewer'
        db.delete_table(u'myanalytics_siteviewer')

        # Deleting model 'SiteView'
        db.delete_table(u'myanalytics_siteview')

        # Deleting model 'UserAgent'
        db.delete_table(u'myanalytics_useragent')


    models = {
        u'myanalytics.siteview': {
            'Meta': {'object_name': 'SiteView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'resolution_h': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'resolution_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'search_parameters': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'site_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_codes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myanalytics.UserAgent']"}),
            'view_source': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'viewed': ('django.db.models.fields.DateTimeField', [], {}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myanalytics.SiteViewer']"})
        },
        u'myanalytics.siteviewer': {
            'Meta': {'object_name': 'SiteViewer'},
            'aguid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'myjobs_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'myanalytics.useragent': {
            'Meta': {'object_name': 'UserAgent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['myanalytics']