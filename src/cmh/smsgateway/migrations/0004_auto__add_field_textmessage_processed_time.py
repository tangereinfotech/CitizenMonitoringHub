# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TextMessage.processed_time'
        db.add_column('smsgateway_textmessage', 'processed_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TextMessage.processed_time'
        db.delete_column('smsgateway_textmessage', 'processed_time')


    models = {
        'smsgateway.ignoredtextmessage': {
            'Meta': {'object_name': 'IgnoredTextMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
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
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['smsgateway']