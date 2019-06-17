# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 20:56:58 2019

@author: yoelr
"""
from colorama import Style
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
    __slots__ = ('ID',)
    cached = {}
    
    def __new__(cls, ID=None, fg=None, bg=None, style=None):
        if not ID:
            if fg:
                ID = fg
            elif bg:
                ID = bg
            elif style:
                ID = style
        
        if ID and not any((fg, bg, style)): return cls.cached[ID]
            
        ansicolor = colors.color('', fg, bg, style).replace(Style.RESET_ALL, '')
        self = cls.ansicolor(ansicolor, ID)
        
        return self
    
    def __init__(cls, ID=None, fg=None, bg=None, style=None):
        pass # Necessary to include signature in sphinx docs
    
    @classmethod
    def ansicolor(cls, ansicolor, ID=None):
        """Create a Color object with *ansicolor* code string."""
        self = super().__new__(Color, ansicolor)
        self.ID = ID
        
        if ID and ID not in cls.cached:
            cls.cached[ID] = self
        
        return self
    
    def __call__(self, string):
        return self + str(string) + Style.RESET_ALL 
    
    def __repr__(self):
        if self.ID:
            name = self.ID
        else:
            name = type(self).__name__
        return f'{self}<{name}>{Style.RESET_ALL}'
    
Color.cached = dict((i, Color(fg=i)) for i in colors.css_colors.keys())
Color.reset = Color.ansicolor(Style.RESET_ALL, ID='reset')
