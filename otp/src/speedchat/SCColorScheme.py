"""SCColorScheme.py: contains the SCColorScheme class"""

from ColorSpace import *

class SCColorScheme:
    """ SCColorScheme is a class that holds all the information
    that a SpeedChat tree needs to display itself with a particular
    color scheme.

    This object is intentionally immutable; if you want to change the
    color scheme of a SpeedChat tree, create a new SCColorScheme object.
    """
    def __init__(self,
                 arrowColor=(.5,.5,1),
                 rolloverColor=(.53,.9,.53),
                 # derived from arrowColor
                 frameColor=None,
                 # derived from rolloverColor
                 pressedColor=None,
                 menuHolderActiveColor=None,
                 emoteIconColor=None,
                 textColor=(0,0,0),
                 emoteIconDisabledColor=(.5,.5,.5),
                 textDisabledColor=(.4,.4,.4),
                 alpha=.95,
                 ):
        def scaleColor(color, s):
            y,u,v = rgb2yuv(*color)
            return yuv2rgb(y*s,u,v)
        def scaleIfNone(color, srcColor, s):
            if color is not None:
                return color
            else:
                return scaleColor(srcColor, s)
            
        self.__arrowColor = arrowColor
        self.__rolloverColor = rolloverColor

        self.__frameColor = frameColor
        if self.__frameColor is None:
            # the frame color should be a whited-out version of the
            # arrow color; reduce the saturation
            h,s,v = rgb2hsv(*arrowColor)
            self.__frameColor = hsv2rgb(h,.2*s,v)

        # TEMP
        # there seems to be a change to the Panda/DirectGui (alpha?)
        # behavior, where the speedchat frame is darker than it used to
        # be. This is problem because the rollover color no longer
        # contrasts; see 'blue' as an example.
        # Brighten up the frame color so that it's close to what it used to
        # be.
        h,s,v = rgb2hsv(*self.__frameColor)
        self.__frameColor = hsv2rgb(h,.5*s,v)

        # pressed and menuHolderActive are rollover with slightly
        # (and progressively) lower luminance
        self.__pressedColor = scaleIfNone(pressedColor,
                                          self.__rolloverColor, .92)
        self.__menuHolderActiveColor = scaleIfNone(menuHolderActiveColor,
                                                   self.__rolloverColor, .84)

        self.__emoteIconColor = emoteIconColor
        if self.__emoteIconColor is None:
            # base the emote icon color off of the rollover color
            # max out the saturation to get a deep color
            # bring the value down slightly
            h,s,v = rgb2hsv(*self.__rolloverColor)
            self.__emoteIconColor = hsv2rgb(h,1.,.8*v)
        self.__emoteIconDisabledColor = emoteIconDisabledColor

        self.__textColor = textColor
        self.__textDisabledColor = textDisabledColor
        self.__alpha = alpha

    def getArrowColor(self):
        return self.__arrowColor
    def getRolloverColor(self):
        return self.__rolloverColor
    def getFrameColor(self):
        return self.__frameColor
    def getPressedColor(self):
        return self.__pressedColor
    def getMenuHolderActiveColor(self):
        return self.__menuHolderActiveColor
    def getEmoteIconColor(self):
        return self.__emoteIconColor
    def getTextColor(self):
        return self.__textColor
    def getEmoteIconDisabledColor(self):
        return self.__emoteIconDisabledColor
    def getTextDisabledColor(self):
        return self.__textDisabledColor
    def getAlpha(self):
        return self.__alpha

    def __str__(self):
        members = ('arrowColor',
                   'rolloverColor',
                   'frameColor',
                   'pressedColor',
                   'menuHolderActiveColor',
                   'emoteIconColor',
                   'textColor',
                   'emoteIconDisabledColor',
                   'textDisabledColor',
                   'alpha')
        result = ''
        for member in members:
            result += '%s = %s' % (member, self.__dict__[
                '_%s__%s' % (self.__class__.__name__, member)])
            if member is not members[-1]:
                result += '\n'
        return result

    def __repr__(self):
        return str(self)
