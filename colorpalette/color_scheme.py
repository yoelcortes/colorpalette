# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 21:02:22 2019

@author: yoelr
"""
from .color import Color

class Palette:
    """Create a Palette object that manages Color objects.
    
    **Parameters**
    
        ****colors:** Key/Color pairs to initialize attributes.
    
    **Examples:**
    
        :doc:`GettingStarted`
    
    """
    
    def __init__(self, **colors):
        for key, color in colors.items():
            setattr(self, key, color)
    
    def __setattr__(self, attr, new_color):
        if isinstance(new_color, Color):
            super().__setattr__(attr, new_color)
        else:
            raise TypeError(f'Attribute must be an instance of Color, not {type(new_color).__name__}')
    
    def __iter__(self):
        return (color for color in self.__dict__.values())
    
    def __repr__(self):
        out = f'<{type(self).__name__}: '
        for attr, color in self.__dict__.items():
            out += color(attr) + ', ' 
        return out[:-2] + '>'