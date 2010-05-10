"""
    Friends views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from tinklas.mail.views import siusti_pranesima
from tinklas.friends.models import Friend


def show_friends(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        draugystes = request.user.friend_set.filter(patvirtinta=True)
        rezultatas = []
        for i in draugystes:
            try:
                draugas = User.objects.get(username=i.draugas)
            except ObjectDoesNotExist:
                continue
            rezultatas.append(draugas)
        return render_to_response('search_results.html', {'user': request.user, 'rezultatas': rezultatas, 'title': 'Draugu sarasas'})


def siulyti_draugyste(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        username = request.GET.get('username', None)
        if username is not None:
            if not user.friend_set.filter(draugas=username):
                try:
                    user_to_ask = User.objects.get(username=username)
                except ObjectDoesNotExist:
                    return HttpResponseRedirect('/home/')            
                friendship = Friend(user=user, draugas=username)
                friendship.save()
                siusti_pranesima(username, 
                        'Draugystes prasymas nuo %s' % user.username,
                        'friend_request',
                        friendship.id)
                return HttpResponseRedirect('/info/user/?username=%s' % username)
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect('/home/')        
        return HttpResponseRedirect('/home/')

def priimti_draugyste(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        username = request.GET.get('username', None)
        if username is not None:
            try:
                friend = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/home/')
            
            try:
                friend_draugyste = friend.friend_set.get(draugas=user.username)
            except ObjectDoesNotExist:   # jei is tikro nebuvo pasiulyta draugyste
                return HttpResponseRedirect('/home/')
            
            if friend_draugyste.patvirtinta:
                return HttpResponseRedirect('/home/')   # jei draugyste jau patvirtinta
            
            try:
                user_draugyste = user.friend_set.get(draugas=username)
            except ObjectDoesNotExist:
                user_draugyste = Friend(user=user, draugas=friend.username)
            
            user_draugyste.patvirtinta = True
            user_draugyste.save()
            friend_draugyste.patvirtinta = True
            friend_draugyste.save()
            
            user.pranesimas_set.filter(Q(tipas='friend_request'), 
                                Q(action_id=friend_draugyste.id)).delete()
                
            return HttpResponseRedirect('/info/user/?username=%s' % username)
        return HttpResponseRedirect('/home/')

def atmesti_draugyste(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        username = request.GET.get('username', None)
        if username is not None:
            try:
                friend = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/home/') 
            
            try:
                friend_draugyste = friend.friend_set.get(draugas=user.username)
            except ObjectDoesNotExist:   # jei is tikro nebuvo pasiulyta draugyste
                return HttpResponseRedirect('/home/')
            
            if friend_draugyste.patvirtinta:
                return HttpResponseRedirect('/home/')   # jei draugyste jau patvirtinta
            
            user.pranesimas_set.filter(Q(tipas='friend_request'), 
                                Q(action_id=friend_draugyste.id)).delete()
            
            user.friend_set.filter(draugas=friend.username).delete()
            friend.friend_set.filter(draugas=user.username).delete()
            
        return HttpResponseRedirect('/home/')


def atsaukti_draugyste(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        username = request.GET.get('username', None)
        if username is not None:
            try:
                friend = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/home/')
            
            try:
                user_draugyste = user.friend_set.get(draugas=friend.username)
            except ObjectDoesNotExist:   # jei is tikro nebuvo pasiulyta draugyste
                return HttpResponseRedirect('/home/')
            
            if user_draugyste.patvirtinta:
                return HttpResponseRedirect('/home/')   # jei draugyste jau patvirtinta
            
            friend.pranesimas_set.filter(Q(tipas='friend_request'), 
                                Q(action_id=user_draugyste.id)).delete()
            
            user.friend_set.filter(draugas=friend.username).delete()
            friend.friend_set.filter(draugas=user.username).delete()
            
        return HttpResponseRedirect('/home/')


def pasalinti_drauga(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        username = request.GET.get('username', None)
        if username is not None:
            try:
                friend = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/home/')
            
            user.friend_set.filter(draugas=friend.username).delete()
            friend.friend_set.filter(draugas=user.username).delete()
            
        return HttpResponseRedirect('/home/')

def paieska(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        if request.method == "POST":
            raktas = request.POST["raktas"]
            if raktas != "" and raktas != "Paieska...":
                rezultatas = User.objects.filter(
                            Q(username__contains=raktas) |
                            Q(first_name__contains=raktas) |
                            Q(last_name__contains=raktas))                
                return render_to_response("search_results.html", 
                        {'user': request.user, 'rezultatas': rezultatas, 'title': 'Paieskos rezultatai'})
            else:
                try:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                except KeyError:
                    return HttpResponseRedirect('/home/')
        else:
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect('/home/')                
