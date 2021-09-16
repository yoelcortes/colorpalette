# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:56:58 2019

@author: yoelr
"""
from colorama import Style
from .utils import rgb2hex, decode_ansi, rgb_tint, rgb_shade
import numpy as np
import colors


class Color:
    """
    Create a Color object that can color/style strings. Color objects are an 
    extension of the color function in the `ansicolors` 
    package <https://pypi.org/project/ansicolors/>`__.
    
    Parameters
    ----------
    ID: str
        Name of color.
    fg: str
        Foreground color.
    bg: str
        Background color.
    style: str
        Options include 'bold', 'underline', or None
    
    Notes
    -----
    Both *fg* and *bg* should be one of the following [-]:
        * 3-element tuple or list of int, each valued 0 to 255 (e.g. (255, 218, 185)),
        * string containing a CSS-compatible color name (e.g. 'peachpuff'),
        * string containing a CSS-style hex value (e.g. '#aaa' or '#8a2be2')
        * string containing a CSS-style RGB notation (e.g. 'rgb(102,51,153)')
        * None
    
    Examples
    --------
    :doc:`GettingStarted`
    
    """
    __slots__ = ('ID', '_ansi', '_RGB', '_RGB_bg', '_style')
    
    cached = {}
    
    def __new__(self, ID='', fg=None, bg=None, style=None):
        if ID and fg is None and bg is None and style is None:
            return self.cached[ID]
        if isinstance(fg, np.ndarray): fg = tuple([int(i) for i in fg])
        if isinstance(bg, np.ndarray): bg = tuple([int(i) for i in bg])
        ansi = colors.color('', fg, bg, style).replace(Style.RESET_ALL, '')
        return self.from_ansi(ID, ansi)
    
    def copy(self, ID=None):
        copy = super().__new__(self.__class__)
        copy.ID = self.ID if ID is None else ID
        copy._ansi = self._ansi
        return copy
        
    @property
    def ansi(self):
        """[str] Ansi color code."""
        return self._ansi
    @ansi.setter
    def ansi(self, ansi):
        self._ansi = ansi
        if hasattr(self, '_RGB'): del self._RGB
        if hasattr(self, '_RGB_bg'): del self._RGB_bg
        if hasattr(self, '_style'): del self._style
    
    @classmethod
    def from_ansi(cls, ID='', ansi=''):
        """Create a Color object with ansi color code string."""
        self = object.__new__(cls)
        self._ansi = ansi
        if ID and ID not in cls.cached: cls.cached[ID] = self
        self.ID = ID
        return self
    
    def __call__(self, string):
        return self + str(string) + Style.RESET_ALL 

    def __add__(self, string):
        return self._ansi + string
    
    def __radd__(self, string):
        return string + self._ansi

    def invert(self, ID=None):
        """Return a new Color object with their foreground and background swapped."""
        return type(self)(ID=ID or f"{self.ID}-inverted", 
                          fg=self.HEX_bg, bg=self.HEX, style=self._style)

    @property
    def RGB(self):
        """[array] Foreground color in RGB on a 0-255 scale."""
        if not hasattr(self, '_RGB'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self._ansi)
        return self._RGB
    @property
    def RGB_bg(self):
        """[array] Background color in RGB on a 0-255 scale."""
        if not hasattr(self, '_RGB_bg'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self._ansi)
        return self._RGB_bg
    @property
    def style(self):
        """[str] Font style."""
        if not hasattr(self, '_style'):
            self._RGB, self._RGB_bg, self._style = decode_ansi(self._ansi)
        return self._style
    
    @property
    def RGBn(self):
        """[array] Foreground color in RGB on a normalized 0-1 scale."""
        RGB = self.RGB
        return None if RGB is None else self.RGB/255.
    @property
    def RGBn_bg(self):
        """[array] Background color in RGB on a normalized 0-1 scale."""
        RGB_bg = self.RGB_bg
        return None if RGB_bg is None else self.RGB_bg/255.
    
    @property
    def HEX(self):
        """[str] Foreground color in HEX code."""
        RGB = self.RGB
        return None if RGB is None else rgb2hex(RGB)
    @property
    def HEX_bg(self):
        """[str] Background color in HEX code."""
        RGB_bg = self.RGB_bg
        return None if RGB_bg is None else rgb2hex(RGB_bg)

    def tint(self, percent, ID=None):
        """Return a new Color object tinted by given percent."""
        fg, bg, style = decode_ansi(self._ansi)
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
        """Return a new Color object shaded by given percent."""
        fg, bg, style = decode_ansi(self._ansi)
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
    
    def show(self):
        print(repr(self))
    _ipython_display_ = show  
    
    def __str__(self):
        return self._ansi
    
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
Color.reset = Color.from_ansi('reset', Style.RESET_ALL)
