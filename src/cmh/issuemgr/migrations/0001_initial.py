# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (('cmh.common', '0001_initial'),)

    def forwards(self, orm):

        # Adding model 'ComplaintState'
        db.create_table('issuemgr_complaintstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintState'])

        # Adding model 'ComplaintItem'
        db.create_table('issuemgr_complaintitem', (
            ('codename_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.CodeName'], unique=True, primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Department'])),
        ))
        db.send_create_signal('issuemgr', ['ComplaintItem'])

        # Adding model 'Complaint'
        db.create_table('issuemgr_complaint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintItem'], null=True, blank=True)),
            ('complaintno', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Department'], null=True, blank=True)),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintState'])),
            ('filedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Citizen'])),
            ('assignto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'], null=True, blank=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('issuemgr', ['Complaint'])


    def backwards(self, orm):

        # Deleting model 'ComplaintState'
        db.delete_table('issuemgr_complaintstate')

        # Deleting model 'ComplaintItem'
        db.delete_table('issuemgr_complaintitem')

        # Deleting model 'Complaint'
        db.delete_table('issuemgr_complaint')


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
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Attribute']", 'symmetrical': 'False'}),
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
            'base': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintItem']", 'null': 'True', 'blank': 'True'}),
            'complaintno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintState']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'filedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Citizen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']", 'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Complaint']", 'null': 'True', 'blank': 'True'})
        },
        'issuemgr.complaintitem': {
            'Meta': {'object_name': 'ComplaintItem', '_ormbases': ['common.CodeName']},
            'codename_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.CodeName']", 'unique': 'True', 'primary_key': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Department']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        'issuemgr.complaintstate': {
            'Meta': {'object_name': 'ComplaintState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'usermgr.citizen': {
            'Meta': {'object_name': 'Citizen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'usermgr.department': {
            'Meta': {'object_name': 'Department', '_ormbases': ['common.CodeName']},
            'codename_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.CodeName']", 'unique': 'True', 'primary_key': 'True'})
        },
        'usermgr.official': {
            'Meta': {'object_name': 'Official'},
            'department': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['usermgr.Department']", 'symmetrical': 'False'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location'", 'to': "orm['common.Attribute']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['issuemgr']
