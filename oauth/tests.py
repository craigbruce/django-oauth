from django.contrib.auth.models import User
from django.test import TestCase
from oauth.models import ClientCredential, Nonce, Token, Realm
from oauth.server import OAuthServer


class OAuthServerTest(TestCase):
    fixtures = ['test_user.json', 'test_entries.json']

    def setUp(self):
        super(OAuthServerTest, self).setUp()

        # Credentials
        self.user = User.objects.get(pk=1)

        # Object to test on
        self.clientcredentials = ClientCredential.objects.get(pk=1)
        self.oauthserver = OAuthServer()

        # Nose setting for long diffs
        #self.maxDiff = None

    def test_validate_timestamp_and_nonce(self):
        self.nonce = Nonce.objects.get(pk=1)
        #Credentials already used
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key, self.nonce.timestamp,
            self.nonce.nonce))
        #New timestamp
        self.assertEquals(
            self.oauthserver.validate_timestamp_and_nonce(
                self.clientcredentials.key, 987654322,
                self.nonce.nonce),
            (self.clientcredentials.key, 987654322,
             self.nonce.nonce, None))
        #New nonce
        self.assertEquals(
            self.oauthserver.validate_timestamp_and_nonce(
                self.clientcredentials.key,
                self.nonce.timestamp, 'abc'),
            (self.clientcredentials.key, self.nonce.timestamp,
                'abc', None))
        #Incorrect client key
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            'm7UQ0_n8M0vUNmdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=',
            self.nonce.timestamp, self.nonce.nonce))

    def test_validate_timestamp_and_nonce_request_token(self):
        self.nonce_request_token = Nonce.objects.get(pk=2)
        #Credentials already used
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_request_token.timestamp,
            self.nonce_request_token.nonce,
            self.nonce_request_token.request_token))
        #New timestamp
        self.assertEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key, 987654322,
            self.nonce_request_token.nonce,
            self.nonce_request_token.request_token),
            (self.clientcredentials.key, 987654322,
             self.nonce_request_token.nonce,
             self.nonce_request_token.request_token))
        self.assertNotEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key, 987654323,
            self.nonce_request_token.nonce,
            self.nonce_request_token.request_token),
            (self.clientcredentials.key, 987654323,
             self.nonce_request_token.nonce, None))
        #New nonce
        self.assertEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_request_token.timestamp,
            'abc', self.nonce_request_token.request_token),
            (self.clientcredentials.key,
             self.nonce_request_token.timestamp,
             'abc', self.nonce_request_token.request_token))
        self.assertNotEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_request_token.timestamp,
            'abc', self.nonce_request_token.request_token),
            (self.clientcredentials.key,
             self.nonce_request_token.timestamp,
             'abc', None))
        #Incorrect client key
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            'm7UQ0_n8M0vUNmdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=',
            self.nonce_request_token.timestamp,
            self.nonce_request_token.nonce,
            self.nonce_request_token.request_token))

    def test_validate_timestamp_and_nonce_access_token(self):
        self.nonce_access_token = Nonce.objects.get(pk=3)
        #Credentials already used
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_access_token.timestamp,
            self.nonce_access_token.nonce,
            None, self.nonce_access_token.access_token))
        #New timestamp
        self.assertEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key, 987654322,
            self.nonce_access_token.nonce, None,
            self.nonce_access_token.access_token),
            (self.clientcredentials.key, 987654322,
             self.nonce_access_token.nonce,
             self.nonce_access_token.access_token))
        self.assertNotEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key, 987654323,
            self.nonce_access_token.nonce, None,
            self.nonce_access_token.access_token),
            (self.clientcredentials.key, 987654323,
             self.nonce_access_token.nonce, None))
        #New nonce
        self.assertEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_access_token.timestamp,
            'abc', None, self.nonce_access_token.access_token),
            (self.clientcredentials.key,
             self.nonce_access_token.timestamp,
             'abc', self.nonce_access_token.access_token))
        self.assertNotEquals(self.oauthserver.validate_timestamp_and_nonce(
            self.clientcredentials.key,
            self.nonce_access_token.timestamp,
            'abc', None,
            self.nonce_access_token.access_token),
            (self.clientcredentials.key,
             self.nonce_access_token.timestamp,
             'abc', None))
        #Incorrect client key
        self.assertFalse(self.oauthserver.validate_timestamp_and_nonce(
            'm7UQ0_n8M0vUNmdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=',
            self.nonce_access_token.timestamp,
            self.nonce_access_token.nonce,
            None, self.nonce_access_token.access_token))

    def test_validate_client_key(self):
        self.assertEquals(
            self.oauthserver.validate_client_key(self.clientcredentials.key),
            self.clientcredentials.key)
        self.assertFalse(self.oauthserver.validate_client_key('notavalidkey'))

    def test_validate_request_token(self):
        self.token = Token.objects.get(pk=1)
        self.assertTrue(
            self.oauthserver.validate_request_token(
                self.clientcredentials.key, self.token.key))
        self.assertFalse(
            self.oauthserver.validate_request_token(
                'mdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=', self.token.key))
        self.assertFalse(
            self.oauthserver.validate_request_token(
                self.clientcredentials.key, 'm7UQ0_n8M0vUNmd'))

    def test_validate_access_token(self):
        self.token = Token.objects.get(pk=2)
        self.assertTrue(
            self.oauthserver.validate_access_token(
                self.clientcredentials.key, self.token.key))
        self.assertFalse(
            self.oauthserver.validate_access_token(
                'mdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=', self.token.key))
        self.assertFalse(
            self.oauthserver.validate_access_token(
                self.clientcredentials.key, 'm7UQ0_n8M0vUNmd'))

    def test_validate_redirect_uri(self):
        self.assertTrue(
            self.oauthserver.validate_redirect_uri(
                self.clientcredentials.key,
                self.clientcredentials.callback))
        self.assertFalse(
            self.oauthserver.validate_redirect_uri(
                'mdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=',
                self.clientcredentials.callback))
        self.assertFalse(
            self.oauthserver.validate_redirect_uri(
                self.clientcredentials.key,
                'http://www.example.com/ready'))

    def test_validate_realm(self):
        self.realm = Realm.objects.get(pk=2)
        self.assertEquals(
            self.oauthserver.validate_realm(
                self.clientcredentials.key,
                self.realm.access_token,
                None, self.realm.name),
            self.realm.name)
        self.realm = Realm.objects.get(pk=3)
        self.assertEquals(
            self.oauthserver.validate_realm(
                self.clientcredentials.key,
                self.realm.access_token,
                self.realm.url, None),
            self.realm.url)

    def test_validate_requested_realm(self):
        self.realm = Realm.objects.get(pk=1)
        self.assertEquals(
            self.oauthserver.validate_requested_realm(
                self.clientcredentials.key, self.realm.name),
            self.realm.name)
        self.assertFalse(
            self.oauthserver.validate_requested_realm(
                'mdwCgQ4kMCRAfO5A7l6pN4QEOePAE4=', self.realm.name))
        self.assertFalse(
            self.oauthserver.validate_requested_realm(
                self.clientcredentials.key, 'wrong_realm_name'))

#    def test_validate_verifier(self):
#        self.token = Token.objects.get(pk=2)
#        self.assertEquals(
#           self.oauthserver.validate_verifier(
#               self.clientcredentials.key,
#               self.token.key,
#               'dfg'),
#           'dfg')

    def test_get_client_secret(self):
        self.assertEquals(
            self.oauthserver.get_client_secret(self.clientcredentials.key),
            self.clientcredentials.secret)
        self.assertFalse(
            self.oauthserver.get_client_secret('Vc_89DGdxcBShDhXGkDKJuc8='))

    def test_get_request_token_secret(self):
        self.token = Token.objects.get(pk=1)
        self.assertEquals(
            self.oauthserver.get_request_token_secret(
                self.clientcredentials.key, self.token.key),
            self.token.secret)
        self.assertFalse(
            self.oauthserver.get_request_token_secret(
                'Vc_89DGdxcBShDhXGkDKJuc8=', self.token.key))
        self.assertFalse(
            self.oauthserver.get_request_token_secret(
                self.clientcredentials.key, 'QhYz2iCdGS8xYwUegfSUHF'))

    def test_get_access_token_secret(self):
        self.token = Token.objects.get(pk=2)
        self.assertEquals(self.oauthserver.get_request_token_secret(
            self.clientcredentials.key, self.token.key),
            self.token.secret)
        self.assertFalse(self.oauthserver.get_request_token_secret(
            'Vc_89DGdxcBShDhXGkDKJuc8=', self.token.key))
        self.assertFalse(self.oauthserver.get_request_token_secret(
            self.clientcredentials.key, 'QhYz2iCdGS8xYwUegfSUHF'))

#class TemporaryCredentialsRequestTest(TestCase):
#    fixtures = ['test_entries.json']
#
#    def setUp(self):
#        super(TemporaryCredentialsRequestTest, self).setUp()
#
#        # Credentials
#        self.username = 'testuser'
#        self.password = 'pass'
#        self.user = User.objects.create_user(
#           self.username,
#           'test@eyesopen.com',
#           self.password
#           )
#
#        # Object to test on
#        self.clientcredentials = ClientCredential.objects.get(pk=1)
#
#        # Nose setting for long diffs
#        self.maxDiff = None
#
#    def testStuff(self):
#
#        c = Client(
#           self.clientcredentials.key,
#           callback_uri=self.clientcredentials.callback
#           )
#
#        uri, headers, body = c.sign(u'http://127.0.0.1:8001/initiate/')

#        #TODO nonce/timestamp/signature will change
#        self.assertEqual(
#            headers,
#            {
#                u'Authorization': u'OAuth oauth_nonce='
#                                  u'"110880830699442379541341263567",'
#                u'oauth_timestamp="1341263567", oauth_version="1.0",'
#                u'oauth_signature_method="HMAC-SHA1",'
#                u'oauth_consumer_key=self.clientcredentials.key,'
#                u'oauth_callback=self.clientcredentials.callback,'
#                u'oauth_signature="1emEeMqMx1vgjKEwdwyrz57%2FyTE%3D"',
#            }
#        )

#        s = OAuthServer()
#        self.assertTrue(s.verify_request(uri, body=body, headers=headers))

#        dc = DjClient()
#        response = dc.post(
#            '/oauth/initiate/',
#            HTTP_AUTHORIZATION=headers['Authorization']
#        )
#        print response.status_code
#        print response.content

        #c = Client()

#        response = c.post('/oauth/initiate/', {
#            'realm': 'test',
#            'oauth_consumer_key': self.client.key,
#            'oauth_signature_method': 'HMAC-SHA1',
#            'oauth_timestamp': now,
#            'oauth_nonce': nonce,
#            'oauth_callback': self.client.callback,
#            'oauth_signature': 'sign',
#            'oauth_version': '1.0',
#        }, Authorization='OAuth')
#
#        print response.status_code
#        print response.content
