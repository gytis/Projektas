"""
    Home views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from tinklas.forms.forms import DuomenuKeitimoForma, SlaptazodzioKeitimoForma
from tinklas.forms.forms import PagrFotoKeitimoForma
from tinklas.settings import MEDIA_ROOT
from tinklas.photos.photos_manager import issaugoti_nuotrauka


def asmenine_info(request):
    if request.user.is_authenticated():
        user = request.user     
        return render_to_response("info.html", {'user': user})
    else:
        return HttpResponseRedirect('/login/')


def vartotojo_info(request):
    if request.user.is_authenticated():
        username = request.GET.get('username', None)
        if username is not None and username != request.user.username:
            user = request.user
            try:
                user_to_watch = User.objects.get(username=username)
            except ObjectDoesNotExist:
                try:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                except:
                    return HttpResponseRedirect('/home/') 
            return render_to_response('user_info.html', 
                {'user': user, 'user_to_watch': user_to_watch})  
        return HttpResponseRedirect('/home/')          
    else:
        return HttpResponseRedirect('/login/')


def redaguoti_profili(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        user = request.user       
        if request.method == 'POST':
            form = DuomenuKeitimoForma(request.POST)
            if form.is_valid():
                if len(User.objects.filter(email=request.POST['El_pastas'])) <= \
                        len(User.objects.filter(Q(username=user.username), 
                                Q(email=request.POST['El_pastas']))):
                    if request.POST['Slaptazodis'] == \
                            request.POST['Pakartoti_slaptazodi'] and \
                            user.check_password(request.POST['Slaptazodis']):
                        saugoti_pakeitimus(request)
                        return render_to_response("duomenu_keitimas.html", 
                            {'message': 'Duomenys pakeisti'})
                    else:
                        error = "Skirtingi slaptazodziai"
                else:
                    error = "Ivestas elektroninis pastas jau naudojamas"
            else:
                error = "Neteisingai uzpildyta forma"
        else:
            form = DuomenuKeitimoForma(auto_id=False, initial={
                            'Vardas': user.first_name,
                            'Pavarde': user.last_name,
                            'El_pastas': user.email,
                            'Nuotrauka': user.get_profile().nuotrauka,
                            'Gimtadienis': user.get_profile().gimtadienis,
                            'Salis': user.get_profile().salis,
                            'Miestas': user.get_profile().miestas,
                            'Adresas': user.get_profile().adresas,
                            'Vidurine_mokykla': user.get_profile().vidurine_mokykla,
                            'Aukstoji_mokykla': user.get_profile().aukstoji_mokykla,
                            'Vid_mokyklos_baigimo_metai': user.get_profile().v_mokyklos_baigimo_metai,
                            'Aukst_mokyklos_baigimo_metai': user.get_profile().a_mokyklos_baigimo_metai})
        
        return render_to_response("duomenu_keitimas.html", 
                            {'form': form, 'error': error})

def saugoti_pakeitimus(request):
    user = request.user
    duomenys = request.POST
    profilis = user.get_profile()
    
    user.first_name = duomenys['Vardas']
    user.last_name = duomenys['Pavarde']
    user.email = duomenys['El_pastas']
    user.save()
    
    profilis.gimtadienis = request.POST['Gimtadienis']
    profilis.salis = request.POST['Salis']
    profilis.miestas = request.POST['Miestas']
    profilis.adresas = request.POST['Adresas']
    profilis.vidurine_mokykla = request.POST['Vidurine_mokykla']
    profilis.aukstoji_mokykla = request.POST['Aukstoji_mokykla']    
    if request.POST['Vid_mokyklos_baigimo_metai'] == "":
        profilis.v_mokyklos_baigimo_metai = None
    else:
        profilis.v_mokyklos_baigimo_metai = \
                request.POST['Vid_mokyklos_baigimo_metai']
    
    if request.POST['Aukst_mokyklos_baigimo_metai'] == "":
        profilis.a_mokyklos_baigimo_metai = None
    else:
        profilis.a_mokyklos_baigimo_metai = \
                request.POST['Aukst_mokyklos_baigimo_metai']
    
    profilis.save()


def keisti_slaptazodi(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        user = request.user 
        if request.method == 'POST':
            form = SlaptazodzioKeitimoForma(request.POST)
            if form.is_valid():
                if user.check_password(request.POST['Senas_slaptazodis']):
                    if request.POST['Naujas_slaptazodis'] == \
                            request.POST['Pakartoti_nauja_slaptazodi']:
                        user.set_password(request.POST['Naujas_slaptazodis'])
                        user.save()
                        return render_to_response('keitimas.html', {'message': "Slaptazodis pakeistas"})
                    else:
                        error = 'Nevienodi slaptazodziai'
                else:
                    error = "Blogas senas slaptazodis"
            else:
                error = "Blogai uzpildyta forma"
        else:
            form = SlaptazodzioKeitimoForma(auto_id=False)
        return render_to_response('keitimas.html', {'form': form, 'error': error})


def keisti_foto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        user = request.user
        if request.method == 'POST':
            form = PagrFotoKeitimoForma(request.POST)
            if form.is_valid():
                if user.check_password(request.POST['Slaptazodis']):
                    profilis = user.get_profile()
                    if 'Nuotrauka' in request.FILES:
                        profilis.nuotrauka = issaugoti_nuotrauka(
                                    user.username, 
                                    "root", 
                                    request.FILES['Nuotrauka'])
                    else:
                        profilis.nuotrauka = "%s/%s" % (MEDIA_ROOT, "anonymous.gif")
                    profilis.save()
                    return render_to_response('keitimas.html', {'message': "Nuotrauka pakeista"})
                else:
                    error = "Neteisingas slaptazodis"
            else:
                error = "Blogai uzpildyta forma"
        else:
            form = PagrFotoKeitimoForma()
        return render_to_response('keitimas.html', {'form': form, 'error': error})
    
    