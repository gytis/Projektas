#!"C:\Python26\python.exe"

import sys

sys.path[0:0] = [
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\src',
  'd:\\mokslai\\paskaitos\\3 kursas\\python\\projektas\\socialinis_tinklas\\eggs\\setuptools-0.6c11-py2.6.egg',
  ]

_interactive = True
if len(sys.argv) > 1:
    _options, _args = __import__("getopt").getopt(sys.argv[1:], 'ic:m:')
    _interactive = False
    for (_opt, _val) in _options:
        if _opt == '-i':
            _interactive = True
        elif _opt == '-c':
            exec _val
        elif _opt == '-m':
            sys.argv[1:] = _args
            _args = []
            __import__("runpy").run_module(
                 _val, {}, "__main__", alter_sys=True)

    if _args:
        sys.argv[:] = _args
        __file__ = _args[0]
        del _options, _args
        execfile(__file__)

if _interactive:
    del _interactive
    __import__("code").interact(banner="", local=globals())