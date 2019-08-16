# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 18:42:27 2018

@author: yoelr
"""

from setuptools import setup

setup(
      name = 'colorpalette',
      packages = ['colorpalette'],
      license='MIT',
      version = '0.2.1',
      description = 'Objects for coloring strings',
      long_description=open('README.rst').read(),
      author = 'Yoel Cortes-Pena',
      install_requires=['ansicolors', 'colorama', 'numpy'],
      package_data = {'colorpalette': []},
      platforms=["Windows"],
      author_email = 'yoelcortes@gmail.com',
      url = 'https://github.com/yoelcortes/colorpalette',
      download_url = 'https://github.com/yoelcortes/colorpalette.git'
      )
      