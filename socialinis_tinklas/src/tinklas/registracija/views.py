"""
    Registration views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from tinklas.settings import MEDIA_ROOT
from tinklas.info.models import Profilis
from tinklas.forms.forms import RegistrationForm
from tinklas.photos.photos_manager import issaugoti_nuotrauka


def registruoti(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:  
        error = ""
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = authenticate(
                        username = request.POST['Vartotojo_vardas'],
                        password = request.POST['Slaptazodis'])
                if user is None:
                    user = User.objects.filter(username__exact=
                                    request.POST['Vartotojo_vardas'])
                    if not user:
                        user = User.objects.filter(email__exact=
                                    request.POST['El_pastas'])
                        if not user:
                            if request.POST['Slaptazodis'] == \
                                    request.POST['Pakartoti_slaptazodi']:
                                registruoti_vartotoja(request)
                                return HttpResponseRedirect('/login/')
                            else:
                                error = "Skirtingi slaptazodziai"
                        else:
                            error = "Ivestas elektroninis pastas jau naudojamas"
                    else:
                        error = "Toks vartotojo vardas jau naudojamas"
                else:
                    error = "Toks vartotojas jau uzsiregistraves"
            else:
                error = "Neteisingai uzpildyta forma"
        else:
            form = RegistrationForm(auto_id=False)
        
        return render_to_response("anonymous/registration.html", 
                            {'form': form, 'error': error})
 
def registruoti_vartotoja(request):
    vartotojas = User.objects.create_user(
            request.POST['Vartotojo_vardas'],
            request.POST['El_pastas'],
            request.POST['Slaptazodis'])
    
    vartotojas.first_name = request.POST['Vardas']
    vartotojas.last_name = request.POST['Pavarde']
    vartotojas.save()   
    
    profilis = Profilis(user=vartotojas)    
    profilis.save()
    
    if 'Nuotrauka' in request.FILES:
        profilis.nuotrauka = issaugoti_nuotrauka(
                                    vartotojas.username, 
                                    "root", 
                                    request.FILES['Nuotrauka'])
    else:
        profilis.nuotrauka = "%s/%s" % (MEDIA_ROOT, "anonymous.gif")
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
