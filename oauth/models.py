import base64
import os
from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm

class Resource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.name

class ClientCredential(models.Model):
    key = models.CharField(max_length=30, blank=True)
    secret = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=100)
    callback = models.URLField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = base64.urlsafe_b64encode(os.urandom(30))
        if not self.secret:
            self.secret = User.objects.make_random_password(length=30)
        super(ClientCredential, self).save(*args, **kwargs)

class ClientCredentialForm(ModelForm):
    class Meta:
        model = ClientCredential
        fields = ('name', 'callback' )

class Nonce(models.Model):
    nonce = models.CharField(max_length=30)
    timestamp = models.IntegerField()
    key = models.ForeignKey(ClientCredential)
    request_token = models.CharField(max_length=30, null=True)
    access_token = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.nonce

class TokenType(models.Model):
    token_type = models.CharField(max_length=10)

    def __unicode__(self):
        return self.token_type

class Token(models.Model):
    token_type = models.ForeignKey(TokenType)
    resource = models.ForeignKey(Resource)
    client_key = models.ForeignKey(ClientCredential)
    key = models.CharField(max_length=30, blank=True)
    secret = models.CharField(max_length=30, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = base64.urlsafe_b64encode(os.urandom(30))
        if not self.secret:
            self.secret = User.objects.make_random_password(length=30)
        super(Token, self).save(*args, **kwargs)

class Realm(models.Model):
    name = models.CharField(max_length=50)
    client_key = models.ForeignKey(ClientCredential)
    access_token = models.ForeignKey(Token, null=True)
    url = models.URLField(null=True)

    def __unicode__(self):
        return self.name
