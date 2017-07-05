from distutils.core import setup, Extension

foo_module = Extension('_read', sources=['read_wrap.c', 'read.c'])

setup(name='read', ext_modules=[read_module], py_modules=["read"])
