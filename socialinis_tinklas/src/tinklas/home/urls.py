
# home urls

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('tinklas.home.views',
    (r'^$', 'home'),    
)

urlpatterns += patterns('tinklas.login.views',
    (r'logout', 'atsijungti'),
)