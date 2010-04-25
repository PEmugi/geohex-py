# -*- coding=utf-8 -*-

__version__ = 0.1
__author__ = "Shinpei Matsuura"


H_KEY = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX'

DEFAULT_LOCATOR = {
                    'min_x_lon': 122930.0,
                    'min_x_lat': 24448.0,
                    'min_y_lon': 141470.0,
                    'min_y_lat': 24228.0,
                    'h_grid': 1000,
                    'h_size': 0.5,
                    'y_coe': 1.4, # 6�p�`�̒��S�����ӂւ̋����B���Z�p�`�̏ꍇ��3^2
                    'to_latlon': lambda x: x,
                    'to_unit': lambda x: x
                    }
                    
