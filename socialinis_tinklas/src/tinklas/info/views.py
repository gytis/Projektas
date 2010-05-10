"""
    Home views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from tinklas.forms.forms import DuomenuKeitimoForma


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
            user_to_watch = User.objects.get(username=username)
            #patikrinti ar daraugas  
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
            form = RegistrationForm(request.POST)
            if form.is_valid():
                users = User.objects.filter(email=
                            request.POST['El_pastas'])
                if len(users) <= 1:
                    if len(users) == 1:
                        if request.POST['El_pastas'] == user.email:
                            if request.POST['Slaptazodis'] == \
                                    request.POST['Pakartoti_slaptazodi']:
                                saugoti_pakeitimus(request)
                                return HttpResponseRedirect('/info/')
                            else:
                                error = "Skirtingi slaptazodziai"
                        else:
                            error = "Ivestas elektroninis pastas jau naudojamas"
                    else:
                        if request.POST['Slaptazodis'] == \
                                request.POST['Pakartoti_slaptazodi']:
                            saugoti_pakeitimus(request)
                            return HttpResponseRedirect('/info/')
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