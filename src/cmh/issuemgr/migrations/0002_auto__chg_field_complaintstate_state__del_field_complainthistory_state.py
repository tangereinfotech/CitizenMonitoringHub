# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ComplaintState.state'
        db.alter_column('issuemgr_complaintstate', 'state', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Deleting field 'ComplaintHistory.stateto'
        db.delete_column('issuemgr_complainthistory', 'stateto_id')

        # Deleting field 'ComplaintHistory.statefrom'
        db.delete_column('issuemgr_complainthistory', 'statefrom_id')

        # Changing field 'ComplaintHistory.description'
        db.alter_column('issuemgr_complainthistory', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'Complaint.assignto'
        db.alter_column('issuemgr_complaint', 'assignto_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official'], null=True))

        # Changing field 'Complaint.complaintno'
        db.alter_column('issuemgr_complaint', 'complaintno', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Complaint.location'
        db.alter_column('issuemgr_complaint', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'], null=True))


    def backwards(self, orm):
        
        # Changing field 'ComplaintState.state'
        db.alter_column('issuemgr_complaintstate', 'state', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Adding field 'ComplaintHistory.stateto'
        db.add_column('issuemgr_complainthistory', 'stateto', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='complainthistorystateto', to=orm['issuemgr.ComplaintState']), keep_default=False)

        # Adding field 'ComplaintHistory.statefrom'
        db.add_column('issuemgr_complainthistory', 'statefrom', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='complainthistorystatefrom', to=orm['issuemgr.ComplaintState']), keep_default=False)

        # Changing field 'ComplaintHistory.description'
        db.alter_column('issuemgr_complainthistory', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Complaint.assignto'
        db.alter_column('issuemgr_complaint', 'assignto_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official']))

        # Changing field 'Complaint.complaintno'
        db.alter_column('issuemgr_complaint', 'complaintno', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Complaint.location'
        db.alter_column('issuemgr_complaint', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Location']))


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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Category']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'issuemgr.complaint': {
            'Meta': {'ordering': "['curstate']", 'object_name': 'Complaint'},
            'assignto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'complaintno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'complainttype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complainttype'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintState']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'department'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'filedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Citizen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']", 'null': 'True', 'blank': 'True'}),
            'origindate': ('django.db.models.fields.DateField', [], {})
        },
        'issuemgr.complainthistory': {
            'Meta': {'ordering': "['-changedate']", 'object_name': 'ComplaintHistory'},
            'changedate': ('django.db.models.fields.DateField', [], {}),
            'complaint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Complaint']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'usermgr.location': {
            'Meta': {'ordering': "['pincode']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'address'", 'unique': 'True', 'null': 'True', 'to': "orm['common.Attribute']"}),
            'country': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'country'", 'unique': 'True', 'to': "orm['common.Attribute']"}),
            'district': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'district'", 'unique': 'True', 'null': 'True', 'to': "orm['common.Attribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'state'", 'unique': 'True', 'null': 'True', 'to': "orm['common.Attribute']"}),
            'town': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'town'", 'unique': 'True', 'null': 'True', 'to': "orm['common.Attribute']"})
        },
        'usermgr.official': {
            'Meta': {'object_name': 'Official'},
            'department': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Attribute']", 'symmetrical': 'False'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Location']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['issuemgr']
