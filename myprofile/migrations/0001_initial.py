# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProfileSet'
        db.create_table(u'myprofile_profileset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
        ))
        db.send_create_signal(u'myprofile', ['ProfileSet'])

        # Adding model 'NameProfile'
        db.create_table(u'myprofile_nameprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'myprofile', ['NameProfile'])

        # Adding model 'EmailProfile'
        db.create_table(u'myprofile_emailprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myjobs.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'myprofile', ['EmailProfile'])

        # Adding model 'NameProfileMeta'
        db.create_table(u'myprofile_nameprofilemeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('display_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myprofile.NameProfile'])),
            ('profile_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myprofile.ProfileSet'])),
        ))
        db.send_create_signal(u'myprofile', ['NameProfileMeta'])

        # Adding model 'EmailProfileMeta'
        db.create_table(u'myprofile_emailprofilemeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('display_flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myprofile.EmailProfile'])),
            ('profile_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myprofile.ProfileSet'])),
        ))
        db.send_create_signal(u'myprofile', ['EmailProfileMeta'])


    def backwards(self, orm):
        
        # Deleting model 'ProfileSet'
        db.delete_table(u'myprofile_profileset')

        # Deleting model 'NameProfile'
        db.delete_table(u'myprofile_nameprofile')

        # Deleting model 'EmailProfile'
        db.delete_table(u'myprofile_emailprofile')

        # Deleting model 'NameProfileMeta'
        db.delete_table(u'myprofile_nameprofilemeta')

        # Deleting model 'EmailProfileMeta'
        db.delete_table(u'myprofile_emailprofilemeta')


    models = {
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 27, 9, 17, 10, 911025)'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'myprofile.emailprofile': {
            'Meta': {'ordering': "['-date_updated']", 'object_name': 'EmailProfile'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'myprofile.emailprofilemeta': {
            'Meta': {'object_name': 'EmailProfileMeta'},
            'display_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myprofile.EmailProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myprofile.ProfileSet']"})
        },
        u'myprofile.nameprofile': {
            'Meta': {'ordering': "['-date_updated']", 'object_name': 'NameProfile'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        },
        u'myprofile.nameprofilemeta': {
            'Meta': {'object_name': 'NameProfileMeta'},
            'display_flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myprofile.NameProfile']"}),
            'profile_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myprofile.ProfileSet']"})
        },
        u'myprofile.profileset': {
            'Meta': {'object_name': 'ProfileSet'},
            'email_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['myprofile.EmailProfile']", 'through': u"orm['myprofile.EmailProfileMeta']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['myprofile.NameProfile']", 'through': u"orm['myprofile.NameProfileMeta']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        }
    }

    complete_apps = ['myprofile']
