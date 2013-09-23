# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SiteViewer.myjobs_id'
        db.delete_column(u'myanalytics_siteviewer', 'myjobs_id')

        # Adding field 'SiteViewer.user'
        db.add_column(u'myanalytics_siteviewer', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SiteViewer.myjobs_id'
        db.add_column(u'myanalytics_siteviewer', 'myjobs_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SiteViewer.user'
        db.delete_column(u'myanalytics_siteviewer', 'user_id')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'myanalytics.siteview': {
            'Meta': {'object_name': 'SiteView'},
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'goal_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']", 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'myanalytics.useragent': {
            'Meta': {'object_name': 'UserAgent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {})
        },
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'gravatar': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_response': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opt_in_employers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'password_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_completion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['myanalytics']