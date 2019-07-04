from __future__ import print_function
import os
from model import *

__author__ = 'Roy Marco Yali Samaniego'
__copyright__ = 'INGEMMET 2019'
__credits__ = ['Roy Yali S.', 'Daniel Aguado H.']
__version__ = '1.2'
__maintainer__ = 'Roy Yali S.'
__mail__ = 'ryali93@gmail.com'
__status__ = 'Development'

BASE_DIR = os.path.dirname(__file__)
STATIC = os.path.join(BASE_DIR, "static")
TBX = os.path.join(BASE_DIR, "tbx\\PotencialMinero.tbx")

CONN = os.path.join(BASE_DIR, "conn\\bdgeocat_publ_gis.sde")

LYR = os.path.join(STATIC, "lyr\\RasterSimbologia.lyr")
gdb = os.path.join(STATIC, 'gdb')
manual = os.path.join(STATIC, 'pdf\\PotencialMinero_guideuser.pdf')

URL = "http://www.ingemmet.gob.pe/"
password = "password.txt"
