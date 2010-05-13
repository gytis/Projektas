from django import template
from django.db.models import Q
from tinklas.mail.models import Pranesimas
from tinklas.mail.models import Laiskas

register = template.Library()



@register.filter
def nauji_pranesimai(messages):
    result = messages.filter(perskaitytas=False)
    if len(result) > 4:    
        return result[:4]
    return result

@register.filter
def laiskai(user):
    result = Laiskas.objects.order_by('data').filter(gavejas=user)
    return result

@register.filter
def issiusti_laiskai(user):
    result = Laiskas.objects.filter(siuntejas = user)
    return result