# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 03:17:08 2019

@author: yoelr
"""
import numpy as np

RGBs = (np.array([0  , 0  , 0  ]), # black
        np.array([170, 0  , 0  ]), # red
        np.array([0  , 170, 0  ]), # green
        np.array([170, 170, 0  ]), # yellow
        np.array([0  , 0  , 170]), # blue
        np.array([170, 0  , 170]), # magenta
        np.array([0  , 170, 170]), # cyan
        np.array([255, 255, 255])) # white

__all__ = ('decode_ansi', 'rgb2hex', 'rgb_tint', 'rgb_shade')

def rgb2hex(rgb):
    R, G, B = rgb
    return f"#{int(R):02x}{int(G):02x}{int(B):02x}"

def rgb_tint(rgb, percent):
    """Return tinted rgb by given percent."""
    white = np.array([255, 255, 255])
    vector = white-rgb
    return rgb + vector * percent/100

def rgb_shade(rbg, percent):
    """Return shaded rgb by given percent."""
    return rbg * (100-percent)/100

def decode_ansi(ansi):
    """Return fg, bg, and style from ansi string."""
    ansi = ansi.lstrip('\x1b[')
    first, *nums = ansi[:ansi.index('m')].split(';')
    fgbgstyle = []
    for i in '34':
        if first is False:
            rgb = None
        elif first[0] == i:
            n = first[1]
            if n == '8':
                nums = nums[1:]
                rgb = np.zeros(3)
                for i, n in zip(range(3), nums): rgb[i] = n
                nums = nums[i+1:]
            elif n == '9':
                rgb = None
            else:
                rgb = RGBs[int(n)]
        else:
            rgb = None
        fgbgstyle.append(rgb)
        if nums: first, *nums = nums
        else: first = False
    n = int(first)
    if n == 0:
        fgbgstyle.append(None)
    elif n == 1:
        fgbgstyle.append('bold')
    elif n == 2:
        fgbgstyle.append('faint')
    elif n == 3:
        fgbgstyle.append('italic')
    elif n == 4:
        fgbgstyle.append('underline')
    else:
        fgbgstyle.append(None)
    return fgbgstyle


    
    
    