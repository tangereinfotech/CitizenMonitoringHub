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
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintState'])

        # Adding model 'Complaint'
        db.create_table('issuemgr_complaint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origindate', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('filedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Citizen'])),
            ('assignto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Official'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usermgr.Location'])),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintState'])),
            ('complaintno', self.gf('django.db.models.fields.IntegerField')()),
            ('complainttype', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='complainttype', null=True, to=orm['common.Attribute'])),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='department', null=True, to=orm['common.Attribute'])),
        ))
        db.send_create_signal('issuemgr', ['Complaint'])

        # Adding model 'ComplaintHistory'
        db.create_table('issuemgr_complainthistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statefrom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complainthistorystatefrom', to=orm['issuemgr.ComplaintState'])),
            ('stateto', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complainthistorystateto', to=orm['issuemgr.ComplaintState'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('changedate', self.gf('django.db.models.fields.DateField')()),
            ('complaint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'])),
        ))
        db.send_create_signal('issuemgr', ['ComplaintHistory'])


    def backwards(self, orm):

        # Deleting model 'ComplaintState'
        db.delete_table('issuemgr_complaintstate')

        # Deleting model 'Complaint'
        db.delete_table('issuemgr_complaint')

        # Deleting model 'ComplaintHistory'
        db.delete_table('issuemgr_complainthistory')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']", 'null': 'True', 'blank': 'True'})
        },
        'common.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Category']", 'null': 'True', 'blank': 'True'})
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
            'assignto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']"}),
            'complaintno': ('django.db.models.fields.IntegerField', [], {}),
            'complainttype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'complainttype'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintState']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'department'", 'null': 'True', 'to': "orm['common.Attribute']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'filedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Citizen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Location']"}),
            'origindate': ('django.db.models.fields.DateField', [], {})
        },
        'issuemgr.complainthistory': {
            'Meta': {'ordering': "['-changedate']", 'object_name': 'ComplaintHistory'},
            'changedate': ('django.db.models.fields.DateField', [], {}),
            'complaint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Complaint']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'statefrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'complainthistorystatefrom'", 'to': "orm['issuemgr.ComplaintState']"}),
            'stateto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'complainthistorystateto'", 'to': "orm['issuemgr.ComplaintState']"})
        },
        'issuemgr.complaintstate': {
            'Meta': {'object_name': 'ComplaintState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'usermgr.citizen': {
            'Meta': {'ordering': "['fname']", 'object_name': 'Citizen'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mobile': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'usermgr.location': {
            'Meta': {'ordering': "['pincode']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latdegree': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'latdir': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'latmin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'latsec': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'londegree': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'londir': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'lonmin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lonsec': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'usermgr.official': {
            'Meta': {'ordering': "['fname']", 'object_name': 'Official'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Location']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'superivor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['issuemgr']
