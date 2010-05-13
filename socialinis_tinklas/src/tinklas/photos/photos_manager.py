"""
    Photos views
"""

from os import mkdir, listdir, rmdir, remove
from datetime import datetime
from tinklas.settings import MEDIA_ROOT


def getAlbumsNames(username):
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    
    if username not in listdir(MEDIA_ROOT):
        mkdir(user_folder)
    if "albums" not in listdir(user_folder):
        mkdir(albums_folder)
        return []
    return listdir(albums_folder)

def getAlbum(username, album):
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    album_folder = "%s/%s/%s/%s" % (MEDIA_ROOT, username, "albums", album)
    
    if username not in listdir(MEDIA_ROOT):
        mkdir(user_folder)
    if "albums" not in listdir(user_folder):
        mkdir(albums_folder)
    if album not in listdir(albums_folder):
        return None
    return album_folder

def createAlbum(username, album):
    album = tvarkyti_pavadinimus(album)
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    album_folder = "%s/%s/%s/%s" % (MEDIA_ROOT, username, "albums", album)
    
    if username not in listdir(MEDIA_ROOT):
        mkdir(user_folder)
    if "albums" not in listdir(user_folder):
        mkdir(albums_folder)
    if album not in listdir(albums_folder):
        mkdir(album_folder)
    return album_folder

def removeAlbum(username, album):
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    album_folder = "%s/%s/%s/%s" % (MEDIA_ROOT, username, "albums", album)    
    
    if username not in listdir(MEDIA_ROOT):
        mkdir(user_folder)
    if "albums" not in listdir(user_folder):
        mkdir(albums_folder)
    if album in listdir(albums_folder):
        rmdir(album_folder)
        return True
    else:
        return False

def get_album_photos(username, album):
    album_folder = getAlbum(username, album)
    if album_folder is None:
        return []
    else:
        nuotraukos = listdir(album_folder)
        rezultatas = []
        for nuotrauka in nuotraukos:
            rezultatas.append("%s/%s" % (album_folder, nuotrauka))
        return rezultatas

def issaugoti_nuotrauka(username, album, foto):
    ext4 = ('.jpg', '.gif', '.ico', '.bmp,', '.png')
    ext5 = ('.jpeg',)
    album_folder = createAlbum(username, album)
    filename = "%s/%s_%s" % (album_folder, str(datetime.now()),foto.name)
    filename = tvarkyti_pavadinimus(filename)
    if filename[len(filename)-4:].lower() in ext4 or \
            filename[len(filename)-5:].lower() in ext5:
        fd = open(filename, 'wb')
        fd.write(foto.read())
        fd.close()
        return filename
    else:
        return None

def trinti_nuotrauka(foto):
    try:
        remove(foto)
        return True
    except:
        return False

def tvarkyti_pavadinimus(pavadinimas):
    pavadinimas = pavadinimas.replace(' ', '_')
    pavadinimas = pavadinimas.replace(',', '')
    pavadinimas = pavadinimas.replace(':', '')
    pavadinimas = pavadinimas.replace(';', '')
    pavadinimas = pavadinimas.replace('\'', '')
    pavadinimas = pavadinimas.replace('\"', '')
    return pavadinimas