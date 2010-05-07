
# registration views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tinklas.home.models import Vartotojo_Profilis
from tinklas.forms.forms import RegistrationForm
from tinklas.settings import MEDIA_ROOT
from tinklas.photos.photos_manager import issaugoti_nuotrauka


from django import http
from django import forms

class SimpleFileForm(forms.Form):
    #file = forms.Field(widget=forms.FileInput, required=False)
    file = forms.ImageField()

def directupload(request):
    
    template = 'fileupload.html'
    
    if request.method == 'POST':
        form = SimpleFileForm(request.POST)
        if form.is_valid():
            if 'file' in request.FILES:
                file = request.FILES['file']
                
                # Other data on the request.FILES dictionary:
                #   filesize = len(file['content'])   
                #   filetype = file['content-type'] 
                
                filename = file.name
                
                fd = open('%s/%s' % (MEDIA_ROOT, filename), 'wb')
                fd.write(file.read())
                fd.close()
                
                return render_to_response('upload_success.html', { 'message': MEDIA_ROOT })
        else:
            return render_to_response('upload_success.html', { 'message': 'nevalidi forma' })
    else:
        # display the form
        form = SimpleFileForm()
        return render_to_response(template, { 'form': form })

def registruoti(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:  
        error = ""
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = authenticate(username = request.POST['Vartotojo_vardas'],
                                    password = request.POST['Slaptazodis'])
                if user is None:
                    user = User.objects.filter(username__iexact = request.POST['Vartotojo_vardas'])
                    if not user:
                        user = User.objects.filter(email__iexact = request.POST['El_pastas'])
                        if not user:
                            if request.POST['Slaptazodis'] == request.POST['Pakartoti_slaptazodi']:
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
            form = RegistrationForm(auto_id = False)
        
        return render_to_response("registration.html", {'form': form, 'error': error})
 
def registruoti_vartotoja(request):
    vartotojas = User.objects.create_user(
            request.POST['Vartotojo_vardas'],
            request.POST['El_pastas'],
            request.POST['Slaptazodis'])
    
    vartotojas.first_name = request.POST['Vardas']
    vartotojas.last_name = request.POST['Pavarde']
    vartotojas.save()   
    
    profilis = Vartotojo_Profilis(user = vartotojas)    
    profilis.save()
    
    if 'Nuotrauka' in request.FILES:
        profilis.nuotrauka = issaugoti_nuotrauka(vartotojas.username, "root", request.FILES['Nuotrauka'])
    profilis.gimtadienis = request.POST['Gimtadienis']
    profilis.salis = request.POST['Salis']
    profilis.miestas = request.POST['Miestas']
    profilis.adresas = request.POST['Adresas']
    profilis.vidurine_mokykla = request.POST['Vidurine_mokykla']
    profilis.aukstoji_mokykla = request.POST['Aukstoji_mokykla']
    
    if request.POST['Vid_mokyklos_baigimo_metai'] == "":
        profilis.v_mokyklos_baigimo_metai = None
    else:
        profilis.v_mokyklos_baigimo_metai = request.POST['Vid_mokyklos_baigimo_metai']
    
    if request.POST['Aukst_mokyklos_baigimo_metai'] == "":
        profilis.a_mokyklos_baigimo_metai = None
    else:
        profilis.a_mokyklos_baigimo_metai = request.POST['Aukst_mokyklos_baigimo_metai']
    
    profilis.save()
