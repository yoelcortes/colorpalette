# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 21:02:22 2019

@author: yoelr
"""
from .palette import Palette
from math import floor, ceil
from .color import Color
from .utils import view

class ColorWheel:
    """
    Create a ColorWheel object that cycles through Color objects.
    
    Parameters
    ----------
        colors: tuple[Color]
            Colors to cycle through.
    
    Examples
    --------
    :doc:`GettingStarted`
    
    """
    __slots__ = ('colors', 'index')
    
    def __init__(self, colors):
        self.colors = tuple(colors)
        self.restart()

    def view(self, *args, **kwargs):
        return view(self.colors, *args, **kwargs)

    def interpolate(self, x):
        colors = self.colors
        y = x * (len(colors) - 1)
        lb = int(floor(y))
        ub = int(ceil(y))
        s = y - lb
        return Color(
            fg = (1 - s) * colors[lb].RGB + s * colors[ub].RGB
        )
    
    def restart(self):
        self.index = 0
    
    def __getitem__(self, index):
        return self.colors[index % len(self.colors)]
    
    def next(self):
        colors = self.colors
        index = self.index
        color = colors[index]
        self.index = (index + 1) % len(colors)
        return color
    
    __repr__ = Palette.__repr__
    _ipython_display_ = Palette._ipython_display_