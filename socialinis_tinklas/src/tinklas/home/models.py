
# home models

from django.db import models
from django.contrib.auth.models import User

class Vartotojo_Profilis(models.Model):
    user = models.ForeignKey(User, unique = True)
    
    gimtadienis = models.CharField(max_length = 10, blank = True)
    
    salis = models.CharField(max_length = 30, blank = True)
    miestas = models.CharField(max_length = 30, blank = True)
    adresas = models.CharField(max_length = 40, blank = True)
    
    vidurine_mokykla = models.CharField(max_length = 30, blank = True)
    v_mokyklos_baigimo_metai = models.PositiveIntegerField(null = True, blank = True)
    aukstoji_mokykla = models.CharField(max_length = 30, blank = True)
    a_mokyklos_baigimo_metai = models.PositiveIntegerField(null = True, blank = True)