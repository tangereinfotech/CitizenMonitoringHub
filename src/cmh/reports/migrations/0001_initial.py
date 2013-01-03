# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IssuesDataReport'
        db.create_table('reports_issuesdatareport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('complaintno', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('filed_on', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('last_updated', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('filed_by', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('latest_update', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('accepted_by', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_updated_by', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('complaint_status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('attachments', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal('reports', ['IssuesDataReport'])

        # Adding model 'ReminderReport'
        db.create_table('reports_reminderreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comp_report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.IssuesDataReport'])),
            ('comp_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('reminder', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('reports', ['ReminderReport'])


    def backwards(self, orm):
        # Deleting model 'IssuesDataReport'
        db.delete_table('reports_issuesdatareport')

        # Deleting model 'ReminderReport'
        db.delete_table('reports_reminderreport')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reports.issuesdatareport': {
            'Meta': {'object_name': 'IssuesDataReport'},
            'accepted_by': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'attachments': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'complaint_status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'complaintno': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'filed_by': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'filed_on': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'latest_update': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'reports.reminderreport': {
            'Meta': {'object_name': 'ReminderReport'},
            'comp_report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reports.IssuesDataReport']"}),
            'comp_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminder': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['reports']