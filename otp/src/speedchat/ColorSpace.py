# -*- coding: utf-8 -*-
"""ColorSpace.py: contains utility functions to convert between color spaces"""

import math

"""
 r,g,b values are from 0. to 1.
 h = [0,360], s = [0,1], v = [0,1]
 if s == 0, then h = -1 (undefined)
 'The coordinate system is cylindrical, and the colors are defined inside
 a hexcone. The hue value H runs from 0 to 360º. The saturation S is the
 degree of strength or purity and is from 0 to 1. Purity is how much white
 is added to the color, so S=1 makes the purest color (no white).
 Brightness V also ranges from 0 to 1, where 0 is the black.'
"""
def rgb2hsv(r, g, b):
    _min = float(min(r, g, b))
    _max = float(max(r, g, b))
    v = _max
    delta = _max - _min
    
    if (delta != 0.):
        s = delta / _max
    else:
        # r = g = b = N
        # s = 0, h is undefined
        s = 0.
        h = -1.
        return h,s,v
    
    if (r == _max):
        h = (g - b) / delta # between yellow & magenta
    elif (g == _max):
        h = 2. + ((b - r) / delta) # between cyan & yellow
    else:
        h = 4. + ((r - g) / delta) # between magenta & cyan
    h *= 60. # degrees
    if(h < 0.):
        h += 360.
    return h,s,v

def hsv2rgb(h, s, v):
    if(s == 0.):
        # achromatic (grey)
        return v,v,v
    
    h %= 360.
    h /= 60. # sector 0 to 5
    i = int(math.floor(h))
    f = h - i # factorial part of h
    p = v * (1. - s)
    q = v * (1. - s * f)
    t = v * (1. - s * (1. - f))
    if i == 0:
        return v,t,p
    elif i == 1:
        return q,v,p
    elif i == 2:
        return p,v,t
    elif i == 3:
        return p,q,v
    elif i == 4:
        return t,p,v
    else:
        return v,p,q

"""
 y is luminance/brightness
 u and v describe color in a non-intuitive manner
"""
def rgb2yuv(r,g,b):
    y =  .299*r + .587*g + .114*b
    u = -.169*r - .331*g + .500*b + .5
    v =  .500*r - .419*g - .081*b + .5
    return tuple(map(lambda x: min(max(x,0),1), (y,u,v)))

def yuv2rgb(y,u,v):
    r = y - 0.0009267*(u-.5) + 1.4016868*(v-.5)
    g = y - 0.3436954*(u-.5) - 0.7141690*(v-.5)
    b = y + 1.7721604*(u-.5) + 0.0009902*(v-.5)
    return tuple(map(lambda x: min(max(x,0),1), (r,g,b)))
