# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table('oauth_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('oauth', ['Resource'])

        # Adding model 'ClientCredential'
        db.create_table('oauth_clientcredential', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('callback', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('oauth', ['ClientCredential'])

        # Adding model 'Nonce'
        db.create_table('oauth_nonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nonce', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.ClientCredential'])),
            ('request_token', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('oauth', ['Nonce'])

        # Adding model 'TokenType'
        db.create_table('oauth_tokentype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('oauth', ['TokenType'])

        # Adding model 'Token'
        db.create_table('oauth_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.TokenType'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.Resource'])),
            ('client_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.ClientCredential'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('oauth', ['Token'])

        # Adding model 'Realm'
        db.create_table('oauth_realm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('client_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.ClientCredential'])),
            ('access_token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth.Token'], null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal('oauth', ['Realm'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table('oauth_resource')

        # Deleting model 'ClientCredential'
        db.delete_table('oauth_clientcredential')

        # Deleting model 'Nonce'
        db.delete_table('oauth_nonce')

        # Deleting model 'TokenType'
        db.delete_table('oauth_tokentype')

        # Deleting model 'Token'
        db.delete_table('oauth_token')

        # Deleting model 'Realm'
        db.delete_table('oauth_realm')


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
        'oauth.clientcredential': {
            'Meta': {'object_name': 'ClientCredential'},
            'callback': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth.nonce': {
            'Meta': {'object_name': 'Nonce'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.ClientCredential']"}),
            'nonce': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'request_token': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'oauth.realm': {
            'Meta': {'object_name': 'Realm'},
            'access_token': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.Token']", 'null': 'True'}),
            'client_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.ClientCredential']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'oauth.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'oauth.token': {
            'Meta': {'object_name': 'Token'},
            'client_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.ClientCredential']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.Resource']"}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'token_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth.TokenType']"})
        },
        'oauth.tokentype': {
            'Meta': {'object_name': 'TokenType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['oauth']