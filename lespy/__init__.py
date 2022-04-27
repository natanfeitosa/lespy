"""
A small and robust micro Python framework for building simple and solid web apps.
"""


from lespy.confs import *
from lespy.core import *
from lespy.http.request import *
from lespy.http.response import *
from lespy.server import run

__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))
__author__ = 'Natan Santos'
__email__ = 'natansantosapps@gmail.com'
__description__ = 'A small and robust micro Python framework for building simple and solid web apps.'
