#!/usr/bin/env python

from distutils.core import setup
from glulxe.interface import __version__

setup(name='python-glulxe',
      version=__version__,
      description='Python interface to glulxe and Inform 7 interactive fiction interpreter ',
      author='AILab@FOI',
      author_email='markus.schatten@foi.hr',
      url='https://github.com/AILab-FOI/python-glulxe',
      packages=['glulxe'],
     )
