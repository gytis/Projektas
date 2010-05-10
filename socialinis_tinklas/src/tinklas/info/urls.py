"""
    Info urls
"""

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('tinklas.info.views',
    (r'^$', 'asmenine_info'),
    (r'^user/', 'vartotojo_info'),
    (r'^redaguoti/', 'redaguoti_profili'),
    (r'^keisti_slaptazodi/', 'keisti_slaptazodi'),
    (r'^keisti_foto/', 'keisti_foto'),
)