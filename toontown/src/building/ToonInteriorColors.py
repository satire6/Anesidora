
from toontown.toonbase.ToontownGlobals import *

wainscottingBase = [
    #   (    r,     g,     b,   a)
    Vec4(0.800, 0.500, 0.300, 1.0),
    Vec4(0.699, 0.586, 0.473, 1.0),
    Vec4(0.473, 0.699, 0.488, 1.0),
]

wallpaperBase = [
    #   (    r,     g,     b,   a)
    Vec4(1.0, 1.0, 0.7, 1.0),
    Vec4(0.8, 1.0, 0.7, 1.0),
    Vec4(0.4, 0.5, 0.4, 1.0),
    Vec4(0.5, 0.7, 0.6, 1.0),
#    Vec4(1.000, 0.820, 0.699, 1.0),
]

wallpaperBorderBase = [
    #   (    r,     g,     b,   a)
    Vec4(1.0, 1.0, 0.7, 1.0),
    Vec4(0.8, 1.0, 0.7, 1.0),
    Vec4(0.4, 0.5, 0.4, 1.0),
    Vec4(0.5, 0.7, 0.6, 1.0),
#    Vec4(1.000, 1.000, 0.700, 1.0),
#    Vec4(0.789, 1.000, 0.699, 1.0),
#    Vec4(1.000, 0.820, 0.699, 1.0),
]

doorBase = [
    #   (    r,     g,     b,   a)
    Vec4(1.000, 1.000, 0.700, 1.0),
]

floorBase = [
    #   (    r,     g,     b,   a)
    Vec4(0.746, 1.000, 0.477, 1.0),
    Vec4(1.000, 0.684, 0.477, 1.0),
]


baseScheme = {
    "TI_wainscotting":wainscottingBase,
    "TI_wallpaper":wallpaperBase,
    "TI_wallpaper_border":wallpaperBorderBase,
    "TI_door":doorBase,
    "TI_floor":floorBase,
}


colors={
    DonaldsDock:{
        "TI_wainscotting":wainscottingBase,
        "TI_wallpaper":wallpaperBase,
        "TI_wallpaper_border":wallpaperBorderBase,
        "TI_door":doorBase,
        "TI_floor":floorBase,
    },
    # NOTE: If you change ToontownCentral, change the Tutorial, too.
    ToontownCentral:{
        "TI_wainscotting":wainscottingBase,
        "TI_wallpaper":wallpaperBase,
        "TI_wallpaper_border":wallpaperBorderBase,
        "TI_door":doorBase+[
            Vec4(0.8, 0.5, 0.3, 1.0),
        ],
        "TI_floor":floorBase,
    },
    TheBrrrgh:baseScheme,
    MinniesMelodyland:baseScheme,
    DaisyGardens:baseScheme,
    #ConstructionZone:baseScheme,
    #FunnyFarm:baseScheme,
    GoofySpeedway:baseScheme,
    DonaldsDreamland:{
        "TI_wainscotting":wainscottingBase,
        "TI_wallpaper":wallpaperBase,
        "TI_wallpaper_border":wallpaperBorderBase,
        "TI_door":doorBase,
        "TI_floor":floorBase,
    },
    # The tutorial is a cut and paste of Toontown Central
    Tutorial:{
        "TI_wainscotting":wainscottingBase,
        "TI_wallpaper":wallpaperBase,
        "TI_wallpaper_border":wallpaperBorderBase,
        "TI_door":doorBase+[
            Vec4(0.8, 0.5, 0.3, 1.0),
        ],
        "TI_floor":floorBase,
    },
    MyEstate:baseScheme,
    #BossbotHQ:baseScheme,
    #SellbotHQ:baseScheme,
    #CashbotHQ:baseScheme,
    #LawbotHQ:baseScheme,
}
