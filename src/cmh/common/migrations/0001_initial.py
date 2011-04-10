# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('common_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Category'])

        # Adding model 'Attribute'
        db.create_table('common_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Category'])),
        ))
        db.send_create_signal('common', ['Attribute'])

        # Adding M2M table for field parents on 'Attribute'
        db.create_table('common_attribute_parents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_attribute', models.ForeignKey(orm['common.attribute'], null=False)),
            ('to_attribute', models.ForeignKey(orm['common.attribute'], null=False))
        ))
        db.create_unique('common_attribute_parents', ['from_attribute_id', 'to_attribute_id'])

        # Adding model 'CodeName'
        db.create_table('common_codename', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('common', ['CodeName'])

        # Adding model 'LatLong'
        db.create_table('common_latlong', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Attribute'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('common', ['LatLong'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('common_category')

        # Deleting model 'Attribute'
        db.delete_table('common_attribute')

        # Removing M2M table for field parents on 'Attribute'
        db.delete_table('common_attribute_parents')

        # Deleting model 'CodeName'
        db.delete_table('common_codename')

        # Deleting model 'LatLong'
        db.delete_table('common_latlong')


    models = {
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
        'common.latlong': {
            'Meta': {'object_name': 'LatLong'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Attribute']"}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['common']
