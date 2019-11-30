from distutils.core import setup

file_name = 'VERSION'
with open(file_name, 'r') as f:
    VERSION = f.read()

setup(name='erasure',
      version=VERSION,
      py_modules=['erasure'],
      )
