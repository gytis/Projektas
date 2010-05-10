"""
    Registion urls
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.registracija.views',
    (r'^$', 'registruoti'),
)