# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TextMessage'
        db.create_table('smsgateway_textmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('smsgateway', ['TextMessage'])


    def backwards(self, orm):
        
        # Deleting model 'TextMessage'
        db.delete_table('smsgateway_textmessage')


    models = {
        'smsgateway.textmessage': {
            'Meta': {'object_name': 'TextMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['smsgateway']
