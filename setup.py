# -*- coding: utf-8 -*-

"""
Copyright (c) 2015, Philipp Klaus. All rights reserved.

License: GPLv3
"""

from setuptools import setup

setup(name='opus20',
      version = '0.9.6',
      description = 'Interface to Lufft OPUS20 devices',
      long_description = '',
      author = 'Philipp Klaus',
      author_email = 'klaus@physik.uni-frankfurt.de',
      url = '',
      license = 'GPL',
      packages = ['opus20', 'opus20.webapp'],
      scripts = ['scripts/opus20_cli', 'scripts/opus20_web', 'scripts/opus20_discovery'],
      include_package_data = True,
      zip_safe = True,
      platforms = 'any',
      keywords = 'Lufft Opus20',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GPL License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Logging',
      ]
)


