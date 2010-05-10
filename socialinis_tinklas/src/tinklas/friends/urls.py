
"""
    Friends urls
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.friends.views',
    (r'^$', 'show_friends'),
    (r'^search', 'paieska'),
    (r'^request', 'siulyti_draugyste'),
    (r'^priimti', 'priimti_draugyste'),
    (r'^atmesti', 'atmesti_draugyste'),
    (r'^atsaukti', 'atsaukti_draugyste'),
    (r'^pasalinti', 'pasalinti_drauga'),
)