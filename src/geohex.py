# -*- coding=utf-8 -*-

__version__ = 0.1
__author__ = "Shinpei Matsuura"


_H_KEY = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX'

_DEFAULT_LOCATOR = {
                    'min_x_lon': 122930.0,
                    'min_x_lat': 24448.0,
                    'min_y_lon': 141470.0,
                    'min_y_lat': 24228.0,
                    'h_grid': 1000,
                    'h_size': 0.5
                    }

import math

class GeoHexFactory(object):
    def __init__(self, locator=_DEFAULT_LOCATOR):
        self.locator = locator

    def get_by_latlon(self, lat, lon, level=7):
        '''Get GeoHex Object lat, long and level'''
        return self.get_by_hexcode(latlon2geohex(lat, lon, level, self.locator))
        
    def get_by_hexcode(self, code):
        '''Get GeoHex Object by GeoHex Code'''
        pass

class GeoHex(object):
    def __init__(self, hexcode, locator):
        self.hexcode = hexcode
        self._locator = locator
        self._latlon_info = geohex2latlon(self.hexcode, locator)

    def _get_polygon(self):
        lat = self._latlon_info[0]
        lon = self._latlon_info[1]
        level = self._latlon_info[2]
        d = level * self._locator['h_size'] / self._locator['h_grid']

        return (
                (lat, lon - 2.0 * d),
                (lat + 1.4 * d, lon - 1.0 * d),
                (lat + 1.4 * d, lon + 1.0 * d),
                (lat, lon + 2.0 * d),
                (lat - 1.4 * d, lon + 1.0 * d),
                (lat - 1.4 * d, lon - 1.0 * d),
                (lat, lon - 2.0 * d)
                ) 

#internal methods
def _hex2level(hexcode):
    code_length = len(hexcode)

    if code_length > 4:
        level = _H_KEY.index(hexcode[0])
        hexcode = hexcode[1:]
        if level < 0:
            raise Exception('Code format is something wrong')

        level = 60 if level == 0 else level
    else:
        level = 7

    return level, code_length, hexcode



def _hex2hyhx(hexcode):
    level, code_length, code = _hex2level(hexcode)

    if code_length > 5:
        h_x = _H_KEY.find(code[0]) * 3600 + _H_KEY.find(code[2]) *  60 + _H_KEY.find(code[4])
        h_y = _H_KEY.find(code[1]) * 3600 + _H_KEY.find(code[3]) *  60 + _H_KEY.find(code[5])
    else:
        h_x = _H_KEY.find(code[0]) * 60 + _H_KEY.find(code[2])
        h_y = _H_KEY.find(code[1]) * 60 + _H_KEY.find(code[3])

    return h_y, h_x, level

def _hyhx2hex(h_y, h_x, level=None):
    h_x_100 = math.floor(h_x / 3600.0)
    h_x_10 = math.floor(h_x % 3600.0) / 60.0
    h_x_1 = math.floor(h_x % 3600.0) % 60.0
    h_y_100 = math.floor(h_y / 3600.0)
    h_y_10 = math.floor(h_y % 3600.0) / 60.0
    h_y_1 = math.floor(h_y % 3600.0) % 60.0

    if level:
        if level < 7:
            hexcode = _H_KEY[level%60] + _H_KEY[int(h_x_100)] + _H_KEY[int(h_y_100)] + _H_KEY[int(h_x_10)] + _H_KEY[int(h_y_10)] + _H_KEY[int(h_x_1)] + _H_KEY[int(h_y_1)]
        elif level == 7:
            hexcode = _H_KEY[int(h_x_10)] + _H_KEY[int(h_y_10)] + _H_KEY[int(h_x_1)] + _H_KEY[int(h_y_1)]
        else:
            hexcode = _H_KEY[level%60] + _H_KEY[int(h_x_10)] + _H_KEY[int(h_y_10)] + _H_KEY[int(h_x_1)] + _H_KEY[int(h_y_1)]
        

    return hexcode



#utility methods
def latlon2geohex(lat, lon, level=7, locator=_DEFAULT_LOCATOR):
    h_size = level * locator['h_size']
    lon_grid = lon * locator['h_grid']
    lat_grid = lat * locator['h_grid']
    unit_x = 6.0 * h_size
    unit_y = 2.8 * h_size
    h_k = (round((1.4/3) * locator['h_grid'])) / locator['h_grid']
    base_x = math.floor((locator['min_x_lon'] + locator['min_x_lat'] / h_k) / unit_x)
    base_y = math.floor((locator['min_y_lat'] - h_k * locator['min_y_lon']) / unit_y)
    h_pos_x = (lon_grid + lat_grid/h_k) / unit_x - base_x
    h_pos_y = (lat_grid - h_k * lon_grid) / unit_y - base_y
    h_x_0 = math.floor(h_pos_x)
    h_y_0 = math.floor(h_pos_y)
    h_x_q = math.floor((h_pos_x - h_x_0) * 100.0) / 100.0
    h_y_q = math.floor((h_pos_y - h_y_0) * 100.0) / 100.0
    h_x = round(h_pos_x)
    h_y = round(h_pos_y)

    if h_y_q > -h_x_q+1:
        if (h_y_q < 2*h_x_q) and (h_y_q>0.5*h_x_q):
            h_x = h_x_0 + 1
            h_y = h_y_0 + 1

    elif h_y_q < -h_x_q+1:
        if (h_y_q > 2*h_x_q-1) and (h_y_q < 0.5*h_x_q+0.5):
            h_x = h_x_0
            h_y = h_y_0

    return _hyhx2hex(h_y, h_x, level)

def geohex2latlon(hexcode, locator=_DEFAULT_LOCATOR):
    h_y, h_x, level = _hex2hyhx(hexcode)

    h_size = level * locator['h_size']
    unit_x = 6.0 * h_size
    unit_y = 2.8 * h_size
    h_k = (round((1.4/3.0) * locator['h_grid'])) / locator['h_grid']
    base_x = math.floor((locator['min_x_lon'] + locator['min_x_lat'] / h_k) / unit_x)
    base_y = math.floor((locator['min_y_lat'] - h_k * locator['min_y_lon']) / unit_y)

    lat_grid = (h_k * (h_x + base_x) * unit_x + (h_y + base_y) * unit_y) / 2.0
    lon_grid = (lat_grid - (h_y + base_y) * unit_y) / h_k

    return lat_grid / locator['h_grid'], lon_grid / locator['h_grid'], level
