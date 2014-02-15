
from setuptools import setup, find_packages

setup(
      name = 'pyHopeEngine',
      version = '0.1',
      packages = find_packages('src'),
      package_dir = {'' : 'src'},
      
      author = 'Devon Arrington',
      author_email = 'devon.arrington@gmail.com',
      description = 'Game engine built on pygame',
      keywords = 'game engine pyhope pygame',
      url = 'None at the moment' 
)