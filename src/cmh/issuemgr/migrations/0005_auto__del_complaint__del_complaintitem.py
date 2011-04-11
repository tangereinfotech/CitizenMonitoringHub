# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Complaint'
        db.delete_table('issuemgr_complaint')

        # Deleting model 'ComplaintItem'
        db.delete_table('issuemgr_complaintitem')


    def backwards(self, orm):
        
        # Adding model 'Complaint'
        db.create_table('issuemgr_complaint', (
            ('filedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Citizen'])),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complnaintstate', null=True, to=orm['common.Attribute'], blank=True)),
            ('complaintno', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('base', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintItem'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('assignto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complaintlocation', null=True, to=orm['common.Attribute'], blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complaintdepartment', null=True, to=orm['common.Attribute'], blank=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'], null=True, blank=True)),
        ))
        db.send_create_signal('issuemgr', ['Complaint'])

        # Adding model 'ComplaintItem'
        db.create_table('issuemgr_complaintitem', (
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'])),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintItem'])


    models = {
        
    }

    complete_apps = ['issuemgr']
