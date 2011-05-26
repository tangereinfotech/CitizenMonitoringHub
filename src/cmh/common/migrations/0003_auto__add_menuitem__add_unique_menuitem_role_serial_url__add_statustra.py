# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MenuItem'
        db.create_table('common_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.AppRole'])),
            ('serial', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('common', ['MenuItem'])

        # Adding unique constraint on 'MenuItem', fields ['role', 'serial', 'url']
        db.create_unique('common_menuitem', ['role_id', 'serial', 'url'])

        # Adding model 'StatusTransition'
        db.create_table('common_statustransition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.AppRole'], null=True, blank=True)),
            ('curstate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='curstate', to=orm['common.ComplaintStatus'])),
            ('newstate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='newstate', to=orm['common.ComplaintStatus'])),
        ))
        db.send_create_signal('common', ['StatusTransition'])

        # Adding model 'AppRole'
        db.create_table('common_approle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['AppRole'])

        # Adding M2M table for field users on 'AppRole'
        db.create_table('common_approle_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('approle', models.ForeignKey(orm['common.approle'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('common_approle_users', ['approle_id', 'user_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'MenuItem', fields ['role', 'serial', 'url']
        db.delete_unique('common_menuitem', ['role_id', 'serial', 'url'])

        # Deleting model 'MenuItem'
        db.delete_table('common_menuitem')

        # Deleting model 'StatusTransition'
        db.delete_table('common_statustransition')

        # Deleting model 'AppRole'
        db.delete_table('common_approle')

        # Removing M2M table for field users on 'AppRole'
        db.delete_table('common_approle_users')


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
        'common.approle': {
            'Meta': {'object_name': 'AppRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'common.block': {
            'Meta': {'object_name': 'Block'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'common.complaintdepartment': {
            'Meta': {'object_name': 'ComplaintDepartment'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        'common.complaintstatus': {
            'Meta': {'object_name': 'ComplaintStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'common.complainttype': {
            'Meta': {'object_name': 'ComplaintType'},
            'cclass': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'defsmsack': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'defsmsclo': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'defsmsnew': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'defsmsopen': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'defsmsres': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ComplaintDepartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'common.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'common.district': {
            'Meta': {'object_name': 'District'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.State']"})
        },
        'common.grampanchayat': {
            'Meta': {'object_name': 'GramPanchayat'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Block']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'common.menuitem': {
            'Meta': {'unique_together': "(('role', 'serial', 'url'),)", 'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.AppRole']"}),
            'serial': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'common.state': {
            'Meta': {'object_name': 'State'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'common.statustransition': {
            'Meta': {'object_name': 'StatusTransition'},
            'curstate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'curstate'", 'to': "orm['common.ComplaintStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newstate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newstate'", 'to': "orm['common.ComplaintStatus']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.AppRole']", 'null': 'True', 'blank': 'True'})
        },
        'common.village': {
            'Meta': {'object_name': 'Village'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'grampanchayat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GramPanchayat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'search': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
