# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ComplaintHistory'
        db.delete_table('issuemgr_complainthistory')

        # Adding model 'Block'
        db.create_table('issuemgr_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('distt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.District'])),
        ))
        db.send_create_signal('issuemgr', ['Block'])

        # Adding model 'Department'
        db.create_table('issuemgr_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('issuemgr', ['Department'])

        # Adding model 'GramPanchayat'
        db.create_table('issuemgr_grampanchayat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Block'])),
        ))
        db.send_create_signal('issuemgr', ['GramPanchayat'])

        # Adding model 'District'
        db.create_table('issuemgr_district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.State'])),
        ))
        db.send_create_signal('issuemgr', ['District'])

        # Adding model 'Village'
        db.create_table('issuemgr_village', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('gp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.GramPanchayat'])),
        ))
        db.send_create_signal('issuemgr', ['Village'])

        # Adding model 'State'
        db.create_table('issuemgr_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('issuemgr', ['State'])

        # Adding model 'ComplaintItem'
        db.create_table('issuemgr_complaintitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Department'])),
        ))
        db.send_create_signal('issuemgr', ['ComplaintItem'])

        # Deleting field 'Complaint.complainttype'
        db.delete_column('issuemgr_complaint', 'complainttype_id')

        # Deleting field 'Complaint.origindate'
        db.delete_column('issuemgr_complaint', 'origindate')

        # Adding field 'Complaint.base'
        db.add_column('issuemgr_complaint', 'base', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.ComplaintItem'], null=True, blank=True), keep_default=False)

        # Adding field 'Complaint.original'
        db.add_column('issuemgr_complaint', 'original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'], null=True, blank=True), keep_default=False)

        # Adding field 'Complaint.created'
        db.add_column('issuemgr_complaint', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2011, 4, 7, 14, 41, 29, 421734), blank=True), keep_default=False)

        # Changing field 'Complaint.location'
        db.alter_column('issuemgr_complaint', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Village'], null=True))

        # Changing field 'Complaint.department'
        db.alter_column('issuemgr_complaint', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Department'], null=True))


    def backwards(self, orm):
        
        # Adding model 'ComplaintHistory'
        db.create_table('issuemgr_complainthistory', (
            ('complaint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issuemgr.Complaint'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('changedate', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('issuemgr', ['ComplaintHistory'])

        # Deleting model 'Block'
        db.delete_table('issuemgr_block')

        # Deleting model 'Department'
        db.delete_table('issuemgr_department')

        # Deleting model 'GramPanchayat'
        db.delete_table('issuemgr_grampanchayat')

        # Deleting model 'District'
        db.delete_table('issuemgr_district')

        # Deleting model 'Village'
        db.delete_table('issuemgr_village')

        # Deleting model 'State'
        db.delete_table('issuemgr_state')

        # Deleting model 'ComplaintItem'
        db.delete_table('issuemgr_complaintitem')

        # Adding field 'Complaint.complainttype'
        db.add_column('issuemgr_complaint', 'complainttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='complainttype', null=True, to=orm['common.Attribute'], blank=True), keep_default=False)

        # Adding field 'Complaint.origindate'
        db.add_column('issuemgr_complaint', 'origindate', self.gf('django.db.models.fields.DateField')(default=None), keep_default=False)

        # Deleting field 'Complaint.base'
        db.delete_column('issuemgr_complaint', 'base_id')

        # Deleting field 'Complaint.original'
        db.delete_column('issuemgr_complaint', 'original_id')

        # Deleting field 'Complaint.created'
        db.delete_column('issuemgr_complaint', 'created')

        # Changing field 'Complaint.location'
        db.alter_column('issuemgr_complaint', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'], null=True))

        # Changing field 'Complaint.department'
        db.alter_column('issuemgr_complaint', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['common.Attribute']))


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'issuemgr.block': {
            'Meta': {'object_name': 'Block'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'distt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'issuemgr.complaint': {
            'Meta': {'object_name': 'Complaint'},
            'assignto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Official']", 'null': 'True', 'blank': 'True'}),
            'base': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintItem']", 'null': 'True', 'blank': 'True'}),
            'complaintno': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.ComplaintState']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'filedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['usermgr.Citizen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Village']", 'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Complaint']", 'null': 'True', 'blank': 'True'})
        },
        'issuemgr.complaintitem': {
            'Meta': {'object_name': 'ComplaintItem'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Department']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'issuemgr.complaintstate': {
            'Meta': {'object_name': 'ComplaintState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'issuemgr.department': {
            'Meta': {'object_name': 'Department'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'issuemgr.district': {
            'Meta': {'object_name': 'District'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.State']"})
        },
        'issuemgr.grampanchayat': {
            'Meta': {'object_name': 'GramPanchayat'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.Block']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'issuemgr.state': {
            'Meta': {'object_name': 'State'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'issuemgr.village': {
            'Meta': {'object_name': 'Village'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issuemgr.GramPanchayat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
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
