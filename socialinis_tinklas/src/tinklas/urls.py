""" 
    Base urls
"""

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^soc_tinklas/', include('soc_tinklas.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$',  include('tinklas.home.urls')),
    (r'^home/', include('tinklas.home.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^registration/', include('tinklas.registracija.urls')),
    (r'^info/', include('tinklas.info.urls')),
    (r'^login/', 'tinklas.login.views.prisijungti'),
    (r'^logout/', 'tinklas.login.views.atsijungti'),
    (r'^mail/', include('tinklas.mail.urls')),
    (r'^friends/', include('tinklas.friends.urls')),
    (r'^styles/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'src/tinklas/templates/styles'}),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'files/'})
)
