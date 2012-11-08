# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'User.opt_in_dotjobs'
        db.delete_column(u'app_user', 'opt_in_dotjobs')

        # Deleting field 'User.public_headline'
        db.delete_column(u'app_user', 'public_headline')

        # Deleting field 'User.enable_public_profile'
        db.delete_column(u'app_user', 'enable_public_profile')

        # Deleting field 'User.public_summary'
        db.delete_column(u'app_user', 'public_summary')


    def backwards(self, orm):
        
        # Adding field 'User.opt_in_dotjobs'
        db.add_column(u'app_user', 'opt_in_dotjobs', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'User.public_headline'
        db.add_column(u'app_user', 'public_headline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'User.enable_public_profile'
        db.add_column(u'app_user', 'enable_public_profile', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'User.public_summary'
        db.add_column(u'app_user', 'public_summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    models = {
        u'app.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 8, 10, 30, 37, 510168)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['app']
