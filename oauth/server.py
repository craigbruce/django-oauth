from django.core.exceptions import ObjectDoesNotExist
from oauthlib.common import safe_string_equals
from oauthlib.oauth1.rfc5849 import Server
from oauth.models import ClientCredential, Nonce, Token, Realm, Resource


class OAuthServer(Server):

    @property
    def dummy_client(self):
        return u'dummy_client'

    @property
    def dummy_request_token(self):
        return u'dummy_request_token'

    @property
    def dummy_access_token(self):
        return u'dummy_access_token'

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce,
                                     request_token=None, access_token=None):

        try:
            c = ClientCredential.objects.get(key=client_key)
        except ObjectDoesNotExist:
            return False
        n = Nonce.objects.filter(key=c)
        if n.exists():
            #client_key has been used before
            matches = n.filter(nonce=nonce, timestamp=timestamp, request_token=request_token,
                               access_token=access_token)
            if matches.exists():
                #nonce/timestamp/request_token/access_token combo have been used before
                return False

        Nonce.objects.create(nonce=nonce, timestamp=timestamp, key=c, request_token=request_token,
                             access_token=access_token)

        key = None
        if request_token:
            key = request_token
        elif access_token:
            key = access_token

        return client_key, timestamp, nonce, key

    def validate_client_key(self, client_key):

        try:
            c = ClientCredential.objects.get(key=client_key)
            return c.key
        except ObjectDoesNotExist:
            return False

    def validate_request_token(self, client_key, request_token):

        try:
            t = Token.objects.filter(client_key__key=client_key, key=request_token, token_type=1)
        except ObjectDoesNotExist:
            return False

        if t.exists():
            return True
        else:
            return False

    def validate_access_token(self, client_key, access_token):

        try:
            t = Token.objects.filter(client_key__key=client_key, key=access_token, token_type=2)
        except ObjectDoesNotExist:
            return False

        if t.exists():
            return True
        else:
            return False

    def validate_redirect_uri(self, client_key, redirect_uri):

        try:
            c = ClientCredential.objects.filter(key=client_key, callback=redirect_uri)
        except ObjectDoesNotExist:
            return False

        if c.exists():
            return True
        else:
            return False

    def validate_realm(self, client_key, access_token, uri=None, required_realm=None):

        if required_realm:
            try:
                r = Realm.objects.filter(client_key__key=client_key, access_token=access_token, name=required_realm)
            except ObjectDoesNotExist:
                return False

            if r.exists():
                return required_realm
            else:
                return False
        else:
            try:
                r = Realm.objects.filter(url=uri)
            except ObjectDoesNotExist:
                return False

            if r.exists():
                return r[0].url
            else:
                return False

    def validate_requested_realm(self, client_key, realm):

        try:
            r = Realm.objects.filter(name=realm, client_key__key=client_key)
        except ObjectDoesNotExist:
            return False

        if r.exists():
            return realm
        else:
            return False

#    def validate_verifier(self, client_key, access_token, verifier):
#
#        return safe_string_equals(verifier, (client_key, access_token))

    def get_client_secret(self, client_key):

        try:
            c = ClientCredential.objects.filter(key=client_key)
        except ObjectDoesNotExist:
            return False

        if c.exists():
            return c[0].secret
        else:
            False

    def get_request_token_secret(self, client_key, request_token):

        try:
            t = Token.objects.filter(client_key__key=client_key, key=request_token, token_type=1)
        except ObjectDoesNotExist:
            return False

        if t.exists():
            return t[0].secret
        else:
            False

    def get_access_token_secret(self, client_key, access_token):

        try:
            t = Token.objects.filter(client_key__key=client_key, key=access_token, token_type=2)
        except ObjectDoesNotExist:
            return False

        if t.exists():
            return t[0].secret
        else:
            False
