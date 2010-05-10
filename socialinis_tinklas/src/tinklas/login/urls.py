"""
    Login urls
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.login.views',
    (r'^$', 'prisijungti'),
    (r'/logout', 'atsijungti'),
)