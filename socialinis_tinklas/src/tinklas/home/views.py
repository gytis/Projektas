
# home views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def home(request):
    if request.user.is_authenticated():
        return render_to_response("home.html")    
    else:
        return HttpResponseRedirect('/login/')

