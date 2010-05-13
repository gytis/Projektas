"""
    Home views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def home(request):
    if request.user.is_authenticated():
        return render_to_response('home/home.html',
                {'user': request.user})
    else:
        return HttpResponseRedirect('/login/')
