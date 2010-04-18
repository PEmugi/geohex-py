# -*- coding=utf-8 -*-

__version__ = 0.1
__author__ = "Shinpei Matsuura"


import math
from . import constants

class GeoHex(object):
    def __init__(self, hexcode, locator=constants.DEFAULT_LOCATOR):
        self._hexcode = hexcode
        self._locator = locator
        self._latlon_info = _geohex2latlon(self._hexcode, locator)

    @property
    def hexcode(self):
        return self._hexcode

    def get_polygon(self):
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

    def distance(self, another_hex):
        h_y, h_x, level = _hex2hyhx(self._hexcode)
        h_y2, h_x2, level2 = _hex2hyhx(another_hex.hexcode)

        if level != level2:
            raise Exception("Level of codes must be same value")

        dh_y = h_y - h_y2
        dh_x = h_x - h_x2
        ah_y = abs(dh_y)
        ah_x = abs(dh_x)

        if dh_y * dh_x > 0:
            distance = ah_x if ah_x > ah_y else ah_y
        else:
            distance = ah_x + ah_y

        return distance

    def get_neighbors(self, distance):
        h_y, h_x, level = _hex2hyhx(self._hexcode)
        result = []
        for d_y in range(-1 * distance, distance + 1):
            dmn_x = -1 * distance + d_y if d_y > 0 else -1 * distance
            dmx_x = distance + d_y if d_y < 0 else distance

            for d_x in range(dmn_x, dmx_x + 1):
                if d_y == 0 and d_x == 0:
                    continue
                result.append(GeoHex(_hyhx2hex(h_y+d_y, h_x+d_x, level), self._locator))

        return result

    def get_latlon(self):
        return _geohex2latlon(self._hexcode, self._locator)


#internal methods
def _hex2level(hexcode):
    code_length = len(hexcode)

    if code_length > 4:
        level = constants.H_KEY.index(hexcode[0])
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
        h_x = constants.H_KEY.find(code[0]) * 3600 + constants.H_KEY.find(code[2]) *  60 + constants.H_KEY.find(code[4])
        h_y = constants.H_KEY.find(code[1]) * 3600 + constants.H_KEY.find(code[3]) *  60 + constants.H_KEY.find(code[5])
    else:
        h_x = constants.H_KEY.find(code[0]) * 60 + constants.H_KEY.find(code[2])
        h_y = constants.H_KEY.find(code[1]) * 60 + constants.H_KEY.find(code[3])

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
            hexcode = constants.H_KEY[level%60] + constants.H_KEY[int(h_x_100)] + constants.H_KEY[int(h_y_100)] + constants.H_KEY[int(h_x_10)] + constants.H_KEY[int(h_y_10)] + constants.H_KEY[int(h_x_1)] + constants.H_KEY[int(h_y_1)]
        elif level == 7:
            hexcode = constants.H_KEY[int(h_x_10)] + constants.H_KEY[int(h_y_10)] + constants.H_KEY[int(h_x_1)] + constants.H_KEY[int(h_y_1)]
        else:
            hexcode = constants.H_KEY[level%60] + constants.H_KEY[int(h_x_10)] + constants.H_KEY[int(h_y_10)] + constants.H_KEY[int(h_x_1)] + constants.H_KEY[int(h_y_1)]

    return hexcode

def _latlon2geohex(lat, lon, level=7, locator=constants.DEFAULT_LOCATOR):
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

def _geohex2latlon(hexcode, locator=constants.DEFAULT_LOCATOR):
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
