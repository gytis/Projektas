"""
    Mail views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.contrib.auth.models import User

from tinklas.mail.models import GautasLaiskas, IssiustasLaiskas, Pranesimas
from tinklas.forms.forms import LaiskoForma


def laisku_sarasas(request, gauti):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        user = request.user
        if gauti:
            user.pranesimas_set.filter(tipas='new_mail').delete()
            return render_to_response("gauti_laiskai.html",
                        {'user': request.user})
        else:
            return render_to_response("issiusti_laiskai.html",
                        {'user': user})


def gautas_laiskas(request, gautas):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        try:
            laiskas = GautasLaiskas.objects.get(id=request.GET['id'])
            if laiskas.gavejas == request.user:
                laiskas.perskaitytas = True;
                laiskas.save()
                return render_to_response("laiskas.html",
                        {'laiskas': laiskas, 'gautas': gautas})
            else:
                return HttpResponseRedirect('/home/')
        except ObjectDoesNotExist:
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect('/home/')

def issiustas_laiskas(request, gautas):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        try:
            laiskas = IssiustasLaiskas.objects.get(id=request.GET['id'])
            if laiskas.siuntejas == request.user:
                return render_to_response("laiskas.html",
                        {'laiskas': laiskas, 'gautas': gautas})
            else:
                return HttpResponseRedirect('/home/')
        except ObjectDoesNotExist:
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect('/home/')


def trinti_laiskus(request, gautus):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        if gautus:
            GautasLaiskas.objects.filter(gavejas = request.user).delete()
            return HttpResponseRedirect('/mail/')
        else:
            IssiustasLaiskas.objects.filter(siuntejas = request.user).delete()
            return HttpResponseRedirect('/mail/outbox/')


def rasyti_laiska(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        error = ""
        if request.method == "POST":
            form = LaiskoForma(request.POST)
            if form.is_valid():
                siuntejas = request.user
                try:
                    gavejas = User.objects.get(
                            username__iexact = 
                                request.POST['Gavejo_vartotojo_vardas'])
                except:
                    error = "Vartotojas nerastas" 
                if error == "":
                    try:
                        siuntejas.friend_set.get(Q(draugas=gavejas.username),
                                Q(patvirtinta=True))
                    except ObjectDoesNotExist:
                        error = "Laiskus galima siusti tik draugams"
                    if error == "":
                        laiskas = GautasLaiskas(
                                siuntejas = siuntejas.username, 
                                gavejas = gavejas, 
                                antraste = request.POST['Antraste'], 
                                tekstas = request.POST['Tekstas'])
                        laiskas.save()
                        action_id = laiskas.id
                        laiskas = IssiustasLaiskas(
                                gavejas = gavejas.username,
                                siuntejas = siuntejas,
                                antraste = request.POST['Antraste'], 
                                tekstas = request.POST['Tekstas'])
                        laiskas.save()
                        siusti_pranesima(
                            request.POST['Gavejo_vartotojo_vardas'],
                            "Laiskas nuo vartotojo %s" % siuntejas.username,
                            "new_mail",
                            action_id)
                        return render_to_response("message_form.html", 
                                {'message': "Laiskas issiustas"})
            else:
                error = "Neteisingai uzpildyta forma"
        else:            
            try:
                if request.GET['username']:
                    form = LaiskoForma(initial={'Gavejo_vartotojo_vardas': request.GET['username']})
                else:
                    form = LaiskoForma()
            except:
                form = LaiskoForma()
        
        return render_to_response("message_form.html", 
                                {'form': form, 'error': error})


def siusti_pranesima(username, tekstas, tipas, action_id):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return False    
    pranesimas = Pranesimas(gavejas=user, tekstas=tekstas,
                    tipas=tipas, action_id=action_id)
    pranesimas.save()
    return True

def pasalinti_pranesima(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        if request.method == "GET":
            id = request.GET.get('id', None)
            if id is not None:
                request.user.pranesimas_set.filter(id=id).delete()
        try:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except:
            return HttpResponseRedirect('/home/')
