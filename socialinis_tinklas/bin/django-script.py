#!"C:\Python26\python.exe"

import sys
sys.path[0:0] = [
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\src',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\djangorecipe-0.20-py2.6.egg',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\zc.recipe.egg-1.2.2-py2.6.egg',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\zc.buildout-1.4.3-py2.6.egg',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\setuptools-0.6c11-py2.6.egg',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\parts\\django',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas',
  ]

import djangorecipe.manage

if __name__ == '__main__':
    djangorecipe.manage.main('tinklas.settings')
