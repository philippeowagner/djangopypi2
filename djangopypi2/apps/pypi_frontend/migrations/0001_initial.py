# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Classifier'
        db.create_table('pypi_frontend_classifier', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal('pypi_frontend', ['Classifier'])

        # Adding model 'Package'
        db.create_table('pypi_frontend_package', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, primary_key=True)),
            ('auto_hide', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('pypi_frontend', ['Package'])

        # Adding M2M table for field owners on 'Package'
        db.create_table('pypi_frontend_package_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm['pypi_frontend.package'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pypi_frontend_package_owners', ['package_id', 'user_id'])

        # Adding M2M table for field maintainers on 'Package'
        db.create_table('pypi_frontend_package_maintainers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm['pypi_frontend.package'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pypi_frontend_package_maintainers', ['package_id', 'user_id'])

        # Adding model 'Release'
        db.create_table('pypi_frontend_release', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['pypi_frontend.Package'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('metadata_version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=64)),
            ('package_info', self.gf('djangopypi2.apps.pypi_frontend.models.PackageInfoField')()),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('pypi_frontend', ['Release'])

        # Adding unique constraint on 'Release', fields ['package', 'version']
        db.create_unique('pypi_frontend_release', ['package_id', 'version'])

        # Adding model 'Distribution'
        db.create_table('pypi_frontend_distribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='distributions', to=orm['pypi_frontend.Release'])),
            ('content', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('md5_digest', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('filetype', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('pyversion', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('pypi_frontend', ['Distribution'])

        # Adding unique constraint on 'Distribution', fields ['release', 'filetype', 'pyversion']
        db.create_unique('pypi_frontend_distribution', ['release_id', 'filetype', 'pyversion'])

        # Adding model 'Review'
        db.create_table('pypi_frontend_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['pypi_frontend.Release'])),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pypi_frontend', ['Review'])

        # Adding model 'MasterIndex'
        db.create_table('pypi_frontend_masterindex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('pypi_frontend', ['MasterIndex'])

        # Adding model 'MirrorLog'
        db.create_table('pypi_frontend_mirrorlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['pypi_frontend.MasterIndex'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default='now')),
        ))
        db.send_create_signal('pypi_frontend', ['MirrorLog'])

        # Adding M2M table for field releases_added on 'MirrorLog'
        db.create_table('pypi_frontend_mirrorlog_releases_added', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mirrorlog', models.ForeignKey(orm['pypi_frontend.mirrorlog'], null=False)),
            ('release', models.ForeignKey(orm['pypi_frontend.release'], null=False))
        ))
        db.create_unique('pypi_frontend_mirrorlog_releases_added', ['mirrorlog_id', 'release_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Distribution', fields ['release', 'filetype', 'pyversion']
        db.delete_unique('pypi_frontend_distribution', ['release_id', 'filetype', 'pyversion'])

        # Removing unique constraint on 'Release', fields ['package', 'version']
        db.delete_unique('pypi_frontend_release', ['package_id', 'version'])

        # Deleting model 'Classifier'
        db.delete_table('pypi_frontend_classifier')

        # Deleting model 'Package'
        db.delete_table('pypi_frontend_package')

        # Removing M2M table for field owners on 'Package'
        db.delete_table('pypi_frontend_package_owners')

        # Removing M2M table for field maintainers on 'Package'
        db.delete_table('pypi_frontend_package_maintainers')

        # Deleting model 'Release'
        db.delete_table('pypi_frontend_release')

        # Deleting model 'Distribution'
        db.delete_table('pypi_frontend_distribution')

        # Deleting model 'Review'
        db.delete_table('pypi_frontend_review')

        # Deleting model 'MasterIndex'
        db.delete_table('pypi_frontend_masterindex')

        # Deleting model 'MirrorLog'
        db.delete_table('pypi_frontend_mirrorlog')

        # Removing M2M table for field releases_added on 'MirrorLog'
        db.delete_table('pypi_frontend_mirrorlog_releases_added')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pypi_frontend.classifier': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Classifier'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'pypi_frontend.distribution': {
            'Meta': {'unique_together': "(('release', 'filetype', 'pyversion'),)", 'object_name': 'Distribution'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filetype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_digest': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'pyversion': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'distributions'", 'to': "orm['pypi_frontend.Release']"}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'pypi_frontend.masterindex': {
            'Meta': {'object_name': 'MasterIndex'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'pypi_frontend.mirrorlog': {
            'Meta': {'object_name': 'MirrorLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': "'now'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': "orm['pypi_frontend.MasterIndex']"}),
            'releases_added': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'mirror_sources'", 'blank': 'True', 'to': "orm['pypi_frontend.Release']"})
        },
        'pypi_frontend.package': {
            'Meta': {'ordering': "['name']", 'object_name': 'Package'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auto_hide': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'maintainers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'packages_maintained'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'primary_key': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'packages_owned'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'pypi_frontend.release': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('package', 'version'),)", 'object_name': 'Release'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '64'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['pypi_frontend.Package']"}),
            'package_info': ('djangopypi2.apps.pypi_frontend.models.PackageInfoField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'pypi_frontend.review': {
            'Meta': {'object_name': 'Review'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['pypi_frontend.Release']"})
        }
    }

    complete_apps = ['pypi_frontend']