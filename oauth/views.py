from django.http import HttpResponse
from oauthlib.oauth1.rfc5849.utils import urlencode #Django also has an urlencode method
from oauth.server import OAuthServer

def temporary_credentials_request(request):

    if request.META['HTTP_AUTHORIZATION']:
        t = 'Auth present'
    else:
        t = 'missing'


#    response = urlencode({
#        'realm': 1,
#        'oauth_consumer_key': 2,
#        'oauth_signature_method': 3,
#        'oauth_timestamp': 4,
#        'oauth_nonce': 5,
#        'oauth_callback': 6,
#        'oauth_signature': 7
#    })

    authorized = OAuthServer.verify_request(request.build_absolute_uri(), request.method, request.body, request.META, require_resource_owner=False)
    #authorized = OAuthServer.verify_request(uri, http_method, body, headers, require_resource_owner=False)

#    response = urlencode({
#        'oauth_token': 1,
#        'oauth_token_secret': 2,
#        'oauth_callback_confirmed': 'true'
#    })

    #response = "%s %s" % request.META['Authorization'], request.META['QUERY_STRING']
    response = "%s" % t


    return HttpResponse(response)#, content_type='application/x-www-form-urlencoded')
    #return HttpResponse(response, content_type='application/x-www-form-urlencoded')

def user_authorization(request):
    pass

def token_request(request):
    pass