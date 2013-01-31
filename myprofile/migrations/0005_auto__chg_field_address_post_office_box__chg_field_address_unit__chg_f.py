# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Address.post_office_box'
        db.alter_column(u'myprofile_address', 'post_office_box', self.gf('django.db.models.fields.CharField')(max_length=60, null=True))

        # Changing field 'Address.unit'
        db.alter_column(u'myprofile_address', 'unit', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'Address.address_line_two'
        db.alter_column(u'myprofile_address', 'address_line_two', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Name.display_name'
        db.alter_column(u'myprofile_name', 'display_name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True))

        # Changing field 'Telephone.extension'
        db.alter_column(u'myprofile_telephone', 'extension', self.gf('django.db.models.fields.CharField')(max_length=5, null=True))

        # Changing field 'Telephone.country_dialing'
        db.alter_column(u'myprofile_telephone', 'country_dialing', self.gf('django.db.models.fields.IntegerField')(max_length=3))

        # Changing field 'EmploymentHistory.description'
        db.alter_column(u'myprofile_employmenthistory', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'EmploymentHistory.end_date'
        db.alter_column(u'myprofile_employmenthistory', 'end_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'EmploymentHistory.industry_code'
        db.alter_column(u'myprofile_employmenthistory', 'industry_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'EmploymentHistory.onet_code'
        db.alter_column(u'myprofile_employmenthistory', 'onet_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'EmploymentHistory.job_category_code'
        db.alter_column(u'myprofile_employmenthistory', 'job_category_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'EmploymentHistory.country_code'
        db.alter_column(u'myprofile_employmenthistory', 'country_code', self.gf('django.db.models.fields.CharField')(max_length=3, null=True))

        # Changing field 'EmploymentHistory.city_name'
        db.alter_column(u'myprofile_employmenthistory', 'city_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'SecondaryEmail.email'
        db.alter_column(u'myprofile_secondaryemail', 'email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True))

        # Changing field 'SecondaryEmail.label'
        db.alter_column(u'myprofile_secondaryemail', 'label', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'Education.degree_name'
        db.alter_column(u'myprofile_education', 'degree_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Education.end_date'
        db.alter_column(u'myprofile_education', 'end_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Education.education_score'
        db.alter_column(u'myprofile_education', 'education_score', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Education.country_sub_division_code'
        db.alter_column(u'myprofile_education', 'country_sub_division_code', self.gf('django.db.models.fields.CharField')(max_length=5, null=True))

        # Changing field 'Education.city_name'
        db.alter_column(u'myprofile_education', 'city_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Education.start_date'
        db.alter_column(u'myprofile_education', 'start_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Education.degree_minor'
        db.alter_column(u'myprofile_education', 'degree_minor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


    def backwards(self, orm):
        
        # Changing field 'Address.post_office_box'
        db.alter_column(u'myprofile_address', 'post_office_box', self.gf('django.db.models.fields.CharField')(default='', max_length=60))

        # Changing field 'Address.unit'
        db.alter_column(u'myprofile_address', 'unit', self.gf('django.db.models.fields.CharField')(default='', max_length=25))

        # Changing field 'Address.address_line_two'
        db.alter_column(u'myprofile_address', 'address_line_two', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Name.display_name'
        db.alter_column(u'myprofile_name', 'display_name', self.gf('django.db.models.fields.CharField')(default='', max_length=60))

        # User chose to not deal with backwards NULL issues for 'Telephone.extension'
        raise RuntimeError("Cannot reverse this migration. 'Telephone.extension' and its values cannot be restored.")

        # Changing field 'Telephone.country_dialing'
        db.alter_column(u'myprofile_telephone', 'country_dialing', self.gf('django.db.models.fields.IntegerField')(max_length=1))

        # Changing field 'EmploymentHistory.description'
        db.alter_column(u'myprofile_employmenthistory', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # User chose to not deal with backwards NULL issues for 'EmploymentHistory.end_date'
        raise RuntimeError("Cannot reverse this migration. 'EmploymentHistory.end_date' and its values cannot be restored.")

        # Changing field 'EmploymentHistory.industry_code'
        db.alter_column(u'myprofile_employmenthistory', 'industry_code', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'EmploymentHistory.onet_code'
        db.alter_column(u'myprofile_employmenthistory', 'onet_code', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'EmploymentHistory.job_category_code'
        db.alter_column(u'myprofile_employmenthistory', 'job_category_code', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'EmploymentHistory.country_code'
        db.alter_column(u'myprofile_employmenthistory', 'country_code', self.gf('django.db.models.fields.CharField')(default='', max_length=3))

        # Changing field 'EmploymentHistory.city_name'
        db.alter_column(u'myprofile_employmenthistory', 'city_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'SecondaryEmail.email'
        db.alter_column(u'myprofile_secondaryemail', 'email', self.gf('django.db.models.fields.EmailField')(default='', max_length=255))

        # Changing field 'SecondaryEmail.label'
        db.alter_column(u'myprofile_secondaryemail', 'label', self.gf('django.db.models.fields.CharField')(default='', max_length=30))

        # Changing field 'Education.degree_name'
        db.alter_column(u'myprofile_education', 'degree_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # User chose to not deal with backwards NULL issues for 'Education.end_date'
        raise RuntimeError("Cannot reverse this migration. 'Education.end_date' and its values cannot be restored.")

        # Changing field 'Education.education_score'
        db.alter_column(u'myprofile_education', 'education_score', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Education.country_sub_division_code'
        db.alter_column(u'myprofile_education', 'country_sub_division_code', self.gf('django.db.models.fields.CharField')(default='', max_length=5))

        # Changing field 'Education.city_name'
        db.alter_column(u'myprofile_education', 'city_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # User chose to not deal with backwards NULL issues for 'Education.start_date'
        raise RuntimeError("Cannot reverse this migration. 'Education.start_date' and its values cannot be restored.")

        # Changing field 'Education.degree_minor'
        db.alter_column(u'myprofile_education', 'degree_minor', self.gf('django.db.models.fields.CharField')(default='', max_length=255))


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'myjobs.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 25, 13, 14, 53, 753158)'}),
            'opt_in_myjobs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'myprofile.address': {
            'Meta': {'object_name': 'Address', '_ormbases': [u'myprofile.ProfileUnits']},
            'address_line_one': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_line_two': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'country_sub_division_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'post_office_box': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        u'myprofile.education': {
            'Meta': {'object_name': 'Education', '_ormbases': [u'myprofile.ProfileUnits']},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'country_sub_division_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'degree_date': ('django.db.models.fields.DateField', [], {}),
            'degree_major': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'degree_minor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'degree_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'education_level_code': ('django.db.models.fields.IntegerField', [], {}),
            'education_score': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'myprofile.employmenthistory': {
            'Meta': {'object_name': 'EmploymentHistory', '_ormbases': [u'myprofile.ProfileUnits']},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'country_sub_division_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'current_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 25, 13, 14, 39, 572494)', 'null': 'True', 'blank': 'True'}),
            'industry_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'job_category_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'onet_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'myprofile.name': {
            'Meta': {'object_name': 'Name', '_ormbases': [u'myprofile.ProfileUnits']},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'myprofile.profile': {
            'Meta': {'unique_together': "(('name', 'user'),)", 'object_name': 'Profile'},
            'display_order': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'profile_units': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['myprofile.ProfileUnits']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        },
        u'myprofile.profileunits': {
            'Meta': {'object_name': 'ProfileUnits'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myjobs.User']"})
        },
        u'myprofile.secondaryemail': {
            'Meta': {'object_name': 'SecondaryEmail', '_ormbases': [u'myprofile.ProfileUnits']},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'myprofile.telephone': {
            'Meta': {'object_name': 'Telephone', '_ormbases': [u'myprofile.ProfileUnits']},
            'area_dialing': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'channel_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'country_dialing': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'profileunits_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['myprofile.ProfileUnits']", 'unique': 'True', 'primary_key': 'True'}),
            'use_code': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['myprofile']
