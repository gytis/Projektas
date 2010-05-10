"""
    Mail models
"""

from django.db import models
from django.contrib.auth.models import User


class GautasLaiskas(models.Model):
    gavejas = models.ForeignKey(User, unique=False)
    siuntejas = models.CharField(max_length=30)    
    antraste = models.CharField(max_length=100, null=True, blank=True)
    tekstas = models.CharField(max_length=1000, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    perskaitytas = models.BooleanField(default=False)

class IssiustasLaiskas(models.Model):
    siuntejas = models.ForeignKey(User, unique=False)
    gavejas = models.CharField(max_length=30)    
    antraste = models.CharField(max_length=100, null=True, blank=True)
    tekstas = models.CharField(max_length=1000, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

class Pranesimas(models.Model):
    gavejas = models.ForeignKey(User, unique=False)
    tekstas = models.CharField(max_length=100, null=True, blank=True)
    data = models.DateTimeField(auto_now=True)
    tipas = models.CharField(max_length=15)
    action_id = models.PositiveIntegerField()
