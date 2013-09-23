# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SiteViewer.aguid'
        db.alter_column(u'myanalytics_siteviewer', 'aguid', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'SiteView.site_url'
        db.alter_column(u'myanalytics_siteview', 'site_url', self.gf('django.db.models.fields.TextField')())

        # Changing field 'SiteView.search_parameters'
        db.alter_column(u'myanalytics_siteview', 'search_parameters', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'SiteViewer.aguid'
        db.alter_column(u'myanalytics_siteviewer', 'aguid', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'SiteView.site_url'
        db.alter_column(u'myanalytics_siteview', 'site_url', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'SiteView.search_parameters'
        db.alter_column(u'myanalytics_siteview', 'search_parameters', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'myanalytics.siteview': {
            'Meta': {'object_name': 'SiteView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'resolution_h': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'resolution_w': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'search_parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site_url': ('django.db.models.fields.TextField', [], {}),
            'source_codes': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myanalytics.UserAgent']"}),
            'view_source': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'viewed': ('django.db.models.fields.DateTimeField', [], {}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myanalytics.SiteViewer']"})
        },
        u'myanalytics.siteviewer': {
            'Meta': {'object_name': 'SiteViewer'},
            'aguid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
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