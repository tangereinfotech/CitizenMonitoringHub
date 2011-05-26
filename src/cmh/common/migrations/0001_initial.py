# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('common_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Country'])

        # Adding model 'State'
        db.create_table('common_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Country'])),
        ))
        db.send_create_signal('common', ['State'])

        # Adding model 'District'
        db.create_table('common_district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.State'])),
        ))
        db.send_create_signal('common', ['District'])

        # Adding model 'Block'
        db.create_table('common_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.District'])),
        ))
        db.send_create_signal('common', ['Block'])

        # Adding model 'GramPanchayat'
        db.create_table('common_grampanchayat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Block'])),
        ))
        db.send_create_signal('common', ['GramPanchayat'])

        # Adding model 'Village'
        db.create_table('common_village', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('lattd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longd', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('grampanchayat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GramPanchayat'])),
            ('search', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal('common', ['Village'])

        # Adding model 'ComplaintDepartment'
        db.create_table('common_complaintdepartment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.District'])),
        ))
        db.send_create_signal('common', ['ComplaintDepartment'])

        # Adding model 'ComplaintType'
        db.create_table('common_complainttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.ComplaintDepartment'])),
            ('cclass', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('defsmsnew', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('defsmsack', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('defsmsopen', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('defsmsres', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('defsmsclo', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['ComplaintType'])

        # Adding model 'ComplaintStatus'
        db.create_table('common_complaintstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['ComplaintStatus'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('common_country')

        # Deleting model 'State'
        db.delete_table('common_state')

        # Deleting model 'District'
        db.delete_table('common_district')

        # Deleting model 'Block'
        db.delete_table('common_block')

        # Deleting model 'GramPanchayat'
        db.delete_table('common_grampanchayat')

        # Deleting model 'Village'
        db.delete_table('common_village')

        # Deleting model 'ComplaintDepartment'
        db.delete_table('common_complaintdepartment')

        # Deleting model 'ComplaintType'
        db.delete_table('common_complainttype')

        # Deleting model 'ComplaintStatus'
        db.delete_table('common_complaintstatus')


    models = {
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
        'common.state': {
            'Meta': {'object_name': 'State'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lattd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
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
        }
    }

    complete_apps = ['common']
