from django.contrib import admin
from oauth.models import ClientCredential, Nonce, TokenType, Token, Resource, Realm


class ClientCredentialsOptions(admin.ModelAdmin):
    list_display = ('id', 'user', 'key', 'secret', 'name', 'callback')


class NonceOptions(admin.ModelAdmin):
    list_display = ('id', 'key', 'nonce', 'request_token', 'access_token', 'timestamp')


class TokenTypeOptions(admin.ModelAdmin):
    list_display = ('id', 'token_type')


class TokenOptions(admin.ModelAdmin):
    list_display = ('id', 'token_type', 'resource', 'client_key', 'key', 'secret', 'timestamp')


class ResourceOptions(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')


class RealmOptions(admin.ModelAdmin):
    list_display = ('name', 'client_key')


admin.site.register(ClientCredential, ClientCredentialsOptions)
admin.site.register(Nonce, NonceOptions)
admin.site.register(TokenType, TokenTypeOptions)
admin.site.register(Token, TokenOptions)
admin.site.register(Resource, ResourceOptions)
admin.site.register(Realm, RealmOptions)
