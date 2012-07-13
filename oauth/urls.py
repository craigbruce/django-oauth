from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register/$', 'oauth.views.register'),
    url(r'^initiate/$', 'oauth.views.temporary_credentials_request'),
    url(r'^authorize/$', 'oauth.views.user_authorization'),
    url(r'^token/$', 'oauth.views.token_request'),
)