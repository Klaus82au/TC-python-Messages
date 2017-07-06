from distutils.core import setup, Extension

load_module = Extension('_load', sources=['load_wrap.c', 'load.c'])

setup(name='load', ext_modules=[load_module], py_modules=["load"])
