# -*- coding: utf-8 -*-

"""
Copyright (c) 2015, Philipp Klaus. All rights reserved.

License: GPLv3
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    LDESC = open('README.md', 'r').read()
    LDESC = pypandoc.convert(LDESC, 'rst', format='md')
except (ImportError, IOError, RuntimeError) as e:
    print("Could not create long description:")
    print(str(e))
    LDESC = ''

setup(name='opus20',
      version = '1.0.dev',
      description = 'Interface to Lufft OPUS20 devices',
      long_description = LDESC,
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
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Logging',
      ]
)


