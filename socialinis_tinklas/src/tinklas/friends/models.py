"""
    Friends models
"""

from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user = models.ForeignKey(User)
    draugas = models.CharField(max_length=30)
    patvirtinta = models.BooleanField(default=False)
    draugas_nuo = models.DateTimeField(auto_now_add=True)
