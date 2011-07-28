# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ReceivedTextMessage'
        db.create_table('smsgateway_receivedtextmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('smsgateway', ['ReceivedTextMessage'])

        # Adding model 'SenderBlacklist'
        db.create_table('smsgateway_senderblacklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('smsgateway', ['SenderBlacklist'])


    def backwards(self, orm):
        
        # Deleting model 'ReceivedTextMessage'
        db.delete_table('smsgateway_receivedtextmessage')

        # Deleting model 'SenderBlacklist'
        db.delete_table('smsgateway_senderblacklist')


    models = {
        'smsgateway.receivedtextmessage': {
            'Meta': {'object_name': 'ReceivedTextMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'smsgateway.senderblacklist': {
            'Meta': {'object_name': 'SenderBlacklist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
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
