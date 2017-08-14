# -*- coding: utf-8 -*-

"""
Copyright (c) 2015, Philipp Klaus. All rights reserved.

License: GPLv3
"""

from setuptools import setup

setup(name='opus20',
      version = '1.0.dev',
      description = 'Interface to Lufft OPUS20 devices',
      long_description = '',
      author = 'Philipp Klaus',
      author_email = 'klaus@physik.uni-frankfurt.de',
      url = '',
      license = 'GPL',
      packages = ['opus20', 'opus20.webapp'],
      entry_points = {
        'console_scripts': [
          'opus20_cli = opus20.opus20_cli:main',
          'opus20_web = opus20.opus20_web:main',
          'opus20_discovery = opus20.opus20_discovery:main',
          'opus20_fakeserver = opus20.opus20_fakeserver:main',
        ],
      },
      install_requires = [],
      extras_require = {
          'webserver':  ["bottle", "matplotlib", "jinja2", "pandas", "numpy", "pillow"],
      },
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


