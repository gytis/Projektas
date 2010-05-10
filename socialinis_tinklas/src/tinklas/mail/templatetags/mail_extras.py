from django import template
from tinklas.mail.models import Pranesimas
from tinklas.mail.models import GautasLaiskas, IssiustasLaiskas

register = template.Library()


@register.filter
def nauji_pranesimai(messages):
    result = messages.filter(perskaitytas=False)
    if len(result) > 4:    
        return result[:4]
    return result

@register.filter
def nauji_laiskai(letters):
    result = letters.order_by('data').filter(perskaitytas=False)
    return result

@register.filter
def seni_laiskai(letters):
    result = letters.order_by('data').filter(perskaitytas=True)
    return result

@register.filter
def issiusti_laiskai(user):
    result = IssiustasLaiskas.objects.filter(siuntejas = user)
    return result