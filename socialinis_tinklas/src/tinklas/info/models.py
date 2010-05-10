"""
Home models
"""

from django.db import models
from django.contrib.auth.models import User
from tinklas.settings import MEDIA_ROOT

class Profilis(models.Model):
    """
        Papildomi vartotojo duomenys
    
    """
    
    user = models.ForeignKey(User, unique=True)
    
    gimtadienis = models.CharField(max_length=10, blank=True)
    
    salis = models.CharField(max_length=30, blank=True)
    miestas = models.CharField(max_length=30, blank=True)
    adresas = models.CharField(max_length=40, blank=True)
    
    nuotrauka = models.FileField(upload_to='/%s' % MEDIA_ROOT, null=True)
    
    vidurine_mokykla = models.CharField(max_length=30, blank=True)
    v_mokyklos_baigimo_metai = models.PositiveIntegerField(null=True, 
                                                            blank=True)
    aukstoji_mokykla = models.CharField(max_length=30, blank=True)
    a_mokyklos_baigimo_metai = models.PositiveIntegerField(null=True,
                                                            blank=True)