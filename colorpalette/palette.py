# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 21:02:22 2019

@author: yoelr
"""
from .color import Color
import colorpalette

class Palette:
    """
    Create a Palette object that manages Color objects.
    
    Parameters
    ----------
        **colors: Color
            Key/Color pairs to initialize attributes.
    
    Examples
    --------
    :doc:`GettingStarted`
    
    """
    
    def __init__(self, **colors):
        for key, color in colors.items():
            if key != color.ID: color = color.copy(key)
            setattr(self, key, color)
    
    def view(self, *args, **kwargs):
        return colorpalette.view(tuple(self), *args, **kwargs)
    
    def wheel(self, keys=None):
        dct = self.__dict__
        if keys is None:
            return colorpalette.ColorWheel(dct.values())
        else:
            return colorpalette.ColorWheel([dct[i] for i in keys])
    
    def __setattr__(self, attr, new_color):
        if isinstance(new_color, Color):
            super().__setattr__(attr, new_color)
        else:
            raise TypeError(f'Attribute must be an instance of Color, not {type(new_color).__name__}')
    
    def __len__(self):
        return len(self.__dict__)
    
    def __iter__(self):
        return self.__dict__.values().__iter__()
    
    def _ipython_display_(self):
        print(repr(self))
    
    def __repr__(self):
        return f"{type(self).__name__}({', '.join([color(name) for name, color in self.__dict__.items()])})"



    
    