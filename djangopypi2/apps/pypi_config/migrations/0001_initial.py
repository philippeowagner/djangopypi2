# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Classifier'
        db.create_table('pypi_config_classifier', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal('pypi_config', ['Classifier'])


    def backwards(self, orm):
        # Deleting model 'Classifier'
        db.delete_table('pypi_config_classifier')


    models = {
        'pypi_config.classifier': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Classifier'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['pypi_config']