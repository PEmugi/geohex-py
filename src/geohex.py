# -*- coding=utf-8 -*-

__version__ = 0.1
__author__ = "Shinpei Matsuura"


__H_KEY = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX'

__DEFAULT_LOCATOR = {
                    min_x_lon: 122930.0,
                    min_x_lat: 24448.0,
                    min_y_lon: 141470.0,
                    min_y_lat: 24228.0,
                    h_grid: 1000,
                    h_size: 0.5
                    }

import math

class GeoHexFactory(object):
    def __init__(self, locator=__DEFAULT_LOCATOR):
        self.locator = locator

    def get_by_latlon(self, lon, lat, level=7):
        '''Get GeoHex Object lat, long and level'''
        pass

    def get_by_hexcode(self, code):
        '''Get GeoHex Object by GeoHex Code'''
        pass

    def __get_hexcode(self, lon, lat, level=7):
        h_size = level * self.locator['h_size']
        lon_grid = lon * self.locator['h_grid']
        lat_grid = lat * self.locator['h_grid']
        unit_x = 6 * h_size
        unit_y = 2.8 * h_size
        h_k = (round((1.4/3) * self.locator['h_grid']))/self.locator['h_grid']
        base_x = math.floor((self.locator['min_x_lon'] + self.locator['min_x_lat'] / h_k) / unit_x)
        base_y = math.floor((self.locator['min_y_lat'] - h_k * self.locator['min_y_lon']) / unit_y)
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

        h_x_100 = math.floor(h_x / 3600.0)
        h_x_10 = math.floor(h_x % 3600.0) / 60.0
        h_x_1 = math.floor(h_x % 3600.0) % 60.0
        h_y_100 = math.floor(h_y / 3600.0)
        h_y_10 = math.floor(h_y % 3600.0) / 60.0
        h_y_1 = math.floor(h_y % 3600.0) % 60.0

        if level:
            if level < 7:
                hexcode = __H_KEY[level%60] + __H_KEY[int(h_x_100)] + __H_KEY[int(h_y_100)] + __H_KEY[int(h_x_10)] + __H_KEY[int(h_y_10)] + __H_KEY[int(h_x_1)] + __H_KEY[int(h_y_1)]
            else:
                hexcode = __H_KEY[level%60] + __H_KEY[int(h_x_10)] + __H_KEY[int(h_y_10)] + __H_KEY[int(h_x_1)] + __H_KEY[int(h_y_1)]
        else:
            hexcode = __H_KEY[int(h_x_10)] + __H_KEY[int(h_y_10)] + __H_KEY[int(h_x_1)] + __H_KEY[int(h_y_1)]

        return hexcode

    def get_latlon(self, hexcode):
        pass

    def __hex2hyhx(self, hexcode):
        pass


class GeoHex(object):
    pass






#utility methods

#def latlon2geohex(lat, lon, level=7, locator=__DEFAULT_LOCATOR):
#    h_size = level * locator['h_size']
#    lon_grid = lon * locator['h_grid']
#    lat_grid = lat * locator['h_grid']
#    unit_x = 6 * locator['h_size']
#    unit_y = 2.8 * locator['h_size']
#    h_k = (round((1.4/3) * locator['h_grid']))/locator['h_grid']
#    base_x = math.floor((locator['min_x_lon'] + locator['min_x_lat'] / h_k) / unit_x)
#    base_y = math.floor((locator['min_y_lat'] - h_k * locator['min_y_lon']) / unit_y)
#    h_pos_x = (lon_grid + lat_grid/h_k) / unit_x - base_x
#    h_pos_y = (lat_grid - h_k * lon_grid) / unit_y - base_y
#    h_x_0 = math.floor(h_pos_x)
#    h_y_0 = math.floor(h_pos_y)
#    h_x_q = math.floor((h_pos_x - h_x_0) * 100.0) / 100.0
#    h_y_q = math.floor((h_pos_y - h_y_0) * 100.0) / 100.0
#    h_x = round(h_pos_x)
#    h_y = round(h_pos_y)
#
#    if h_y_q > -h_x_q+1:
#        if (h_y_q < 2*h_x_q) and (h_y_q>0.5*h_x_q):
#            h_x = h_x_0 + 1
#            h_y = h_y_0 + 1
#
#    elif h_y_q < -h_x_q+1:
#        if (h_y_q > 2*h_x_q-1) and (h_y_q < 0.5*h_x_q+0.5):
#            h_x = h_x_0
#            h_y = h_y_0
#
#    h_x_100 = math.floor(h_x / 3600.0)
#    h_x_10 = math.floor(h_x % 3600.0) / 60.0
#    h_x_1 = math.floor(h_x % 3600.0) % 60.0
#    h_y_100 = math.floor(h_y / 3600.0)
#    h_y_10 = math.floor(h_y % 3600.0) / 60.0
#    h_y_1 = math.floor(h_y % 3600.0) % 60.0
#
#    if level:
#        if level < 7:
#            hexcode = h_key[level%60] + h_key[int(h_x_100)] + h_key[int(h_y_100)] + h_key[int(h_x_10)] + h_key[int(h_y_10)] + h_key[int(h_x_1)] + h_key[int(h_y_1)]
#        else:
#            hexcode = h_key[level%60] + h_key[int(h_x_10)] + h_key[int(h_y_10)] + h_key[int(h_x_1)] + h_key[int(h_y_1)]
#    else:
#        hexcode = h_key[int(h_x_10)] + h_key[int(h_y_10)] + h_key[int(h_x_1)] + h_key[int(h_y_1)]
#
#    return hexcode
