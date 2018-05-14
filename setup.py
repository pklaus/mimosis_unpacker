# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    LDESC = open('README.md', 'r').read()
    LDESC = pypandoc.convert(LDESC, 'rst', format='md')
except (ImportError, IOError, RuntimeError) as e:
    print("(Minor problem) Could not transform the long description for this package:")
    print(str(e))
    LDESC = ''

setup(name='mimosis_unpacker',
      version = '0.8.dev0',
      description = 'Unpacker for MIMOSIS CMOS Monolithic Active Pixel Sensors',
      long_description = LDESC,
      author = 'Philipp Klaus',
      author_email = 'klaus@physik.uni-frankfurt.de',
      url = 'https://github.com/pklaus/python_colorscale',
      license = 'GPL',
      packages = ['mimosis_unpacker'],
      entry_points = {
          'console_scripts': [
              'mimosis_unpacker = mimosis_unpacker.cli:main',
          ],
      },
      include_package_data = False,
      zip_safe = True,
      platforms = 'any',
      install_requires = [
          "click",
          "numpy",
          "matplotlib",
          "scipy",
          "pillow>=3.3.0",
          "colorscale",
      ],
      keywords = 'Unpacker MIMOSIS CMOS MAPS CPS s-curve',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Visualization',
      ]
)
