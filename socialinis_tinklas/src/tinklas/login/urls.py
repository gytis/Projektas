
# login urls

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.login.views',
    (r'^$', 'prisijungti'),
)