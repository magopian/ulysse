# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Partner.url'
        db.alter_column('partenaires_partner', 'url', self.gf('django.db.models.fields.CharField')(default=0, max_length=200))


    def backwards(self, orm):
        
        # Changing field 'Partner.url'
        db.alter_column('partenaires_partner', 'url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))


    models = {
        'partenaires.partner': {
            'Meta': {'object_name': 'Partner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'presentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['partenaires']
