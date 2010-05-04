#!"C:\Python26\python.exe"

import sys
sys.path[0:0] = [
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\setuptools-0.6c11-py2.6.egg',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\zc.buildout-1.4.3-py2.6.egg',
  ]

import zc.buildout.buildout

if __name__ == '__main__':
    zc.buildout.buildout.main()
