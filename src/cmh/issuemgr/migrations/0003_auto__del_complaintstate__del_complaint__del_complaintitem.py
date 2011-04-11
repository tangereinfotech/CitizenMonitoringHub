# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ComplaintState'
        db.delete_table('issuemgr_complaintstate')

        # Deleting model 'Complaint'
        db.delete_table('issuemgr_complaint')

        # Deleting model 'ComplaintItem'
        db.delete_table('issuemgr_complaintitem')


    def backwards(self, orm):
        
        # Adding model 'ComplaintState'
        db.create_table('issuemgr_complaintstate', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintState'])

        # Adding model 'Complaint'
        db.create_table('issuemgr_complaint', (
            ('filedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Citizen'])),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintState'])),
            ('complaintno', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('base', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintItem'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('assignto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'], null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Department'], null=True, blank=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'], null=True, blank=True)),
        ))
        db.send_create_signal('issuemgr', ['Complaint'])

        # Adding model 'ComplaintItem'
        db.create_table('issuemgr_complaintitem', (
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Department'])),
            ('codename_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.CodeName'], unique=True, primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintItem'])


    models = {
        
    }

    complete_apps = ['issuemgr']
