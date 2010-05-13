"""
    Photos urls
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.photos.views',
    (r'^$', 'rodyti_albumus'),
    (r'^album', 'rodyti_albuma'),
    (r'^create_album', 'sukurti_albuma'),
    (r'^remove_album', 'pasalinti_albuma'),
    (r'^add_photo', 'prideti_foto'),
    (r'^show_photo', 'rodyti_foto'),
    (r'^remove_photo', 'pasalinti_foto'),
)