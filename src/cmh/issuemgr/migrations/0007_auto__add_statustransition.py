# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StatusTransition'
        db.create_table('issuemgr_statustransition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='curstate', to=orm['common.Attribute'])),
        ))
        db.send_create_signal('issuemgr', ['StatusTransition'])

        # Adding M2M table for field newstates on 'StatusTransition'
        db.create_table('issuemgr_statustransition_newstates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('statustransition', models.ForeignKey(orm['issuemgr.statustransition'], null=False)),
            ('attribute', models.ForeignKey(orm['common.attribute'], null=False))
        ))
        db.create_unique('issuemgr_statustransition_newstates', ['statustransition_id', 'attribute_id'])


    def backwards(self, orm):
        
        # Deleting model 'StatusTransition'
        db.delete_table('issuemgr_statustransition')

        # Removing M2M table for field newstates on 'StatusTransition'
        db.delete_table('issuemgr_statustransition_newstates')


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
        'common.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'common.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Category']", 'null': 'True', 'blank': 'True'})
        },
        'common.codename': {
            'Meta': {'object_name': 'CodeName'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'issuemgr.complaint': {
            'Meta': {'object_name': 'Complaint'},
            'assignto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'base': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complaintbase'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'complaintno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complnaintstate'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complaintdepartment'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'filedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Citizen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complaintlocation'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'logdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Complaint']", 'null': 'True', 'blank': 'True'})
        },
        'issuemgr.complaintitem': {
            'Meta': {'object_name': 'ComplaintItem', '_ormbases': ['common.CodeName']},
            'codename_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.CodeName']", 'unique': 'True', 'primary_key': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        'issuemgr.statustransition': {
            'Meta': {'object_name': 'StatusTransition'},
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'curstate'", 'to': "orm['common.Attribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newstates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'newstates'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['common.Attribute']"})
        },
        'usermgr.citizen': {
            'Meta': {'object_name': 'Citizen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'usermgr.official': {
            'Meta': {'object_name': 'Official'},
            'department': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'department_official'", 'symmetrical': 'False', 'to': "orm['common.Attribute']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_official'", 'to': "orm['common.Attribute']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['issuemgr']
