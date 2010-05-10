"""
    Login views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.contrib.auth import authenticate, login, logout

from tinklas.forms.forms import LoginForm


def prisijungti(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')        
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                            username=request.POST['Vartotojo_vardas'],
                            password=request.POST['Slaptazodis'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/home/')
                    else:
                        return render_to_response("login.html",
                                {'form': form, 
                                'error': "Vartotojas uzblokuotas"})
                else:
                    return render_to_response("login.html",
                                {'form': form, 
                                'error': "Neteisingas vartotojo vardas \
                                            arba slaptazodis"}) 
        else:
            form = LoginForm()        
        return render_to_response("login.html", {'form': form})


def atsijungti(request):
    logout(request)
    return HttpResponseRedirect('/login/')

