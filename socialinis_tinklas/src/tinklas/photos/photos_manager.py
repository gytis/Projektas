
"""
    photos views
"""

from os import mkdir, listdir
from tinklas.settings import MEDIA_ROOT

def getAlbum(username, album):
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    album_folder = "%s/%s/%s/%s" % (MEDIA_ROOT, username, "albums", album)
    
    if username not in listdir(MEDIA_ROOT):
        return None
    if "albums" not in listdir(user_folder):
        return None
    if album not in listdir(albums_folder):
        return None    
    return album_folder

def createAlbum(username, album):
    user_folder = "%s/%s" % (MEDIA_ROOT, username)
    albums_folder = "%s/%s/%s" % (MEDIA_ROOT, username, "albums")
    album_folder = "%s/%s/%s/%s" % (MEDIA_ROOT, username, "albums", album)
    
    if username not in listdir(MEDIA_ROOT):
        mkdir(user_folder)
        mkdir(albums_folder)
        mkdir(album_folder)
        return album_folder
    
    elif "albums" not in listdir(user_folder):
        mkdir(albums_folder)
        mkdir(album_folder)
        return album_folder
    
    elif album not in listdir(albums_folder):
        mkdir(album_folder)
        return album_folder
    
    return album_folder

def issaugoti_nuotrauka(username, album, foto):
    album_folder = createAlbum(username, album)
    filename = "%s/%s" % (album_folder, foto.name)
    fd = open(filename, 'wb')
    fd.write(foto.read())
    fd.close()
    return filename