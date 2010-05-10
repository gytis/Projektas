"""
    home urls
"""
from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.home.views',
    (r'^$', 'home'),
)