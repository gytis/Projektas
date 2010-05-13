"""
    Photos views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from tinklas.photos import photos_manager
from tinklas.forms.forms import AddRemoveAlbumForm, PridetiFotoIAlbuma


def rodyti_albumus(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        albumai = []
        
        albums = photos_manager.getAlbumsNames(user.username)
        try:
            albums.remove('root')
        except:
            pass
        for albumas in albums:
            nuotraukos = \
                photos_manager.get_album_photos(user.username, albumas)
            if len(nuotraukos):
                albumai.append({albumas: nuotraukos[0]})
            else:
                albumai.append({albumas: []})
        
        return render_to_response('photos/albumai.html', 
                {'user': user, 'albumai': albumai})


def rodyti_albuma(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        if request.method == 'GET':
            pavadinimas = request.GET.get('album_name', None)
            if pavadinimas is not None:
                nuotraukos = photos_manager.get_album_photos(
                                        request.user.username, 
                                        pavadinimas)
                return render_to_response('photos/albumas.html', 
                                            {'user': request.user, 
                                            'albumas': pavadinimas, 
                                            'nuotraukos': nuotraukos})
        return HttpResponseRedirect('/login/')


def sukurti_albuma(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        if request.method == 'POST':
            form = AddRemoveAlbumForm(request.POST)
            if form.is_valid():
                user = request.user
                pavadinimas = request.POST['Pavadinimas']
                if user.check_password(request.POST['Slaptazodis']):
                    if photos_manager.getAlbum(user.username, pavadinimas)\
                            is None:
                        photos_manager.createAlbum(user.username, pavadinimas)
                        return render_to_response('photos/add_remove.html', 
                                {'message': 'Albumas %s - sukurtas.' % pavadinimas})
                    else:
                        error = 'Toks albumas jau sukurtas'
                else:
                    error = 'Blogas slaptazodis'
            else:
                error = 'Blogai uzpildyta forma'
        else:
            form = AddRemoveAlbumForm()
        
        return render_to_response('photos/add_remove.html',
                {'form': form, 'error': error})

def pasalinti_albuma(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        if request.method == 'POST':
            form = AddRemoveAlbumForm(request.POST)
            if form.is_valid():
                user = request.user
                pavadinimas = request.POST['Pavadinimas']
                if user.check_password(request.POST['Slaptazodis']):
                    if photos_manager.removeAlbum(user.username, pavadinimas):
                        return render_to_response('photos/add_remove.html', 
                                {'message': 'Albumas %s - pasalintas.' % pavadinimas})
                    else:
                        error = 'Albumas nerastas'
                else:
                    error = 'Blogas slaptazodis'
            else:
                error = 'Blogai uzpildyta forma'
        else:
            form = AddRemoveAlbumForm()
        
        return render_to_response('photos/add_remove.html',
                {'form': form, 'error': error})


def prideti_foto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        error = ""
        if request.method == "POST":
            form = PridetiFotoIAlbuma(request.POST)
            if form.is_valid():
                user = request.user
                if user.check_password(request.POST['Slaptazodis']):
                    try:
                        file = photos_manager.issaugoti_nuotrauka(
                                        user.username,
                                        request.POST['Albumas'],
                                        request.FILES['Nuotrauka'])
                    except:
                        error = "Klaida ikeliant nuotrauka"
                        return render_to_response('photos/add_remove.html', 
                                {'form': form, 'error': error})
                    if file is not None:
                        return render_to_response('photos/add_remove.html', 
                                {'message': 'Nuotrauka ikelta'})
                    else:
                        error = "Blogas failo formatas"
                else:
                    error = "Blogas slaptazodis"
            else:
                error = "Blogai uzpildyta forma"
        else:
            albumas = request.GET.get('album_name', None)
            if albumas is None:
                return HttpResponseRedirect('/login/')
            form = PridetiFotoIAlbuma(initial={'Albumas': albumas})
        
        return render_to_response('photos/add_remove.html', 
                {'form': form, 'error': error})


def rodyti_foto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        nuotrauka = request.GET.get('photo', None)
        if nuotrauka is not None:
            return render_to_response('photos/nuotrauka.html', {'nuotrauka': nuotrauka})
        else:
            return HttpResponseRedirect('/login/')


def pasalinti_foto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        if request.method == 'POST':
            albumas = request.GET.get('album_name', None)
            if albumas is not None:
                nuotraukos = request.POST.getlist('trinti')
                if nuotraukos == []:
                    error = "Nepasirinkta nuotrauku"
                else:
                    klaida = False
                    for nuotrauka in nuotraukos:
                        if not photos_manager.trinti_nuotrauka(nuotrauka):
                            klaida = True
                    if klaida:
                        error = "Ne visos pasirinktos nuotraukos buvo pasalintos"                        
                    else:
                        error = "Nuotraukos pasalintos"
                        
                nuotraukos = photos_manager.get_album_photos(
                                        request.user.username, 
                                        albumas)
                return render_to_response('photos/albumas.html', 
                                            {'user': request.user, 
                                            'albumas': albumas, 
                                            'nuotraukos': nuotraukos,
                                            'error': error})
        try:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except:
            return HttpResponseRedirect('/home/')