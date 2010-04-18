# -*- coding=utf-8 -*-

__version__ = 0.1
__author__ = "Shinpei Matsuura"

import math
from . import constants
from . import _geohex

class GeoHexFactory(object):
    def __init__(self, locator=constants.DEFAULT_LOCATOR):
        self.locator = locator

    def get_by_latlon(self, lat, lon, level=7):
        '''Get GeoHex Object lat, long and level'''
        return self.get_by_hexcode(_geohex._latlon2geohex(lat, lon, level, self.locator))
        
    def get_by_hexcode(self, code):
        '''Get GeoHex Object by GeoHex Code'''
        return _geohex.GeoHex(code, self.locator)

def latlon2geohex(lat, lon, level=7, locator=constants.DEFAULT_LOCATOR):
    return _geohex._latlon2geohex(lat, lon, level, locator)

def geohex2latlon(hexcode, locator=constants.DEFAULT_LOCATOR):
    return _geohex._geohex2latlon(hexcode, locator)
