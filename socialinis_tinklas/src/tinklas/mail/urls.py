"""
    Mail urls
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tinklas.mail.views',
    (r'^$', 'laisku_sarasas', {'gauti': True}),
    (r'^outbox', 'laisku_sarasas', {'gauti': False}),
    (r'^message_form', 'rasyti_laiska'),
    (r'^gautas_laiskas', 'gautas_laiskas', {'gautas': True}),
    (r'^issiustas_laiskas', 'issiustas_laiskas', {'gautas': False}),
    (r'^trinti_issiustus', 'trinti_laiskus', {'gautus': False}),
    (r'^trinti_gautus', 'trinti_laiskus', {'gautus': True}),
)