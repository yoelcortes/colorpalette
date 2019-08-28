# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:56:58 2019

@author: yoelr
"""
from colorama import Style
from .utils import rgb2hex, decode_ansi, rgb_tint, rgb_shade
import numpy as np
import colors


class Color(str):
    """Create a Color object that can color/style strings. Color objects are an extension of the color function in the `ansicolors package <https://pypi.org/project/ansicolors/>`__.
    
    **Parameters**
    
        **ID:** [str] Name of color.
        
        **fg:** [str] Foreground color.
        
        **bg:** [str] Background color.
        
        **style:** [str] Options include 'bold', 'underline', or None
        
        Both *fg* and *bg* should be one of the following [-]:
            * 3-element tuple or list of int, each valued 0 to 255 (e.g. (255, 218, 185)),
            * string containing a CSS-compatible color name (e.g. 'peachpuff'),
            * string containing a CSS-style hex value (e.g. '#aaa' or '#8a2be2')
            * string containing a CSS-style RGB notation (e.g. 'rgb(102,51,153)')
            * None
    
    **Examples:**
    
        :doc:`GettingStarted`
    
    """
    __slots__ = ('ID', '_RGB', '_RGB_bg', '_style')
    
    cached = {}
    
    def __new__(cls, ID='', fg=None, bg=None, style=None):
        if ID and fg is None and bg is None and style is None:
            return cls.cached[ID]
        if isinstance(fg, np.ndarray): fg = tuple([int(i) for i in fg])
        if isinstance(bg, np.ndarray): bg = tuple([int(i) for i in bg])
        ansicolor = colors.color('', fg, bg, style).replace(Style.RESET_ALL, '')
        self = cls.ansicolor(ID, ansicolor)
        return self
    
    def __init__(cls, ID=None, fg=None, bg=None, style=None):
        pass # Necessary to include signature in sphinx docs
    
    @classmethod
    def ansicolor(cls, ID='', ansicolor=''):
        """Create a Color object with *ansicolor* code string."""
        self = super().__new__(cls, ansicolor)
        if ID and ID not in cls.cached: cls.cached[ID] = self
        self.ID = ID
        return self
    
    def __call__(self, string):
        return self + str(string) + Style.RESET_ALL 

    @property
    def RGB(self):
        """[array] Foreground color in RGB on a 0-255 scale."""
        if not hasattr(self, '_RGB'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self)
        return self._RGB
    @property
    def RGB_bg(self):
        """[array] Background color in RGB on a 0-255 scale."""
        if not hasattr(self, '_RGB_bg'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self)
        return self._RGB_bg
    @property
    def style(self):
        if not hasattr(self, '_style'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self)
        return self._style
    
    @property
    def RGBn(self):
        """[array] Foreground color in RGB on a normalized 0-1 scale."""
        return self.RGB/255.
    @property
    def RGBn_bg(self):
        """[array] Background color in RGB on a normalized 0-1 scale."""
        return self.RGB_bg/255.
    
    @property
    def HEX(self):
        """[str] Foreground color in HEX code."""
        return rgb2hex(self.RGB)
    @property
    def HEX_bg(self):
        """[str] Background color in HEX code."""
        return rgb2hex(self.RGB_bg)

    def tint(self, percent, ID=None):
        fg, bg, style = decode_ansi(self)
        if fg is not None:
            fg = rgb_tint(fg, percent)
        if bg is not None:
            bg = rgb_tint(bg, percent)
        if not ID:
            *previous_tint, ID = self.ID.split(' tinted ')
            if len(previous_tint) == 1:
                try:
                    p, *_ = previous_tint[0].split('%')
                    p = float(p)
                    percent = p + (100.-p)*percent/100.
                except: pass
            ID = f'{percent}% tinted {ID}'
        return Color(ID, fg, bg, style)

    def shade(self, percent, ID=None):
        fg, bg, style = decode_ansi(self)
        if fg is not None:
            fg = rgb_shade(fg, percent)
        if bg is not None:
            bg = rgb_shade(bg, percent)
        if not ID:
            *previous_shade, ID = self.ID.split(' shaded ')
            if len(previous_shade):
                try:
                    p, *_ = previous_shade[0].split('%')
                    p = float(p)
                    percent = p + (100.-p)*percent/100.
                except: pass
            ID = f'{percent}% shaded {ID}'
        return Color(ID, fg, bg, style)
    
    def _ipython_display_(self):
        print(repr(self))
    
    def __repr__(self):
        if self.ID:
            name = self.ID
        else:
            fg = self.RGB
            bg = self.RGB_bg
            style = self.style
            if isinstance(fg, np.ndarray): fg = tuple(fg)
            if isinstance(bg, np.ndarray): bg = tuple(bg)
            name = f"{type(self).__name__}(fg={fg}, bg={bg}, style={repr(style)})"
        return f'{self}{name}{Style.RESET_ALL}'
    
Color.cached = dict((i, Color(i, fg=i)) for i in colors.css_colors.keys())
Color.reset = Color.ansicolor('reset', Style.RESET_ALL)
