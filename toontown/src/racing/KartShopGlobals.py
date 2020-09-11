##########################################################################
# Module: KartShopGlobals.py
#   Store some needed stuff
# Date: 4/24/05
# Author: shaskell
##########################################################################

from direct.showbase import PythonUtil

class KartShopGlobals:  
        EVENTDICT = { 'guiDone' : 'guiDone', 
                      'returnKart' : 'returnKart',
                      'buyKart' : 'buyAKart',
                      'buyAccessory' : 'buyAccessory'
                     }
        KARTCLERK_TIMER = 180
        MAX_KART_ACC = 16


# NOT KARTSHOP SPECIFIC BUT A GENERAL KART GLOBALS CLASS
class KartGlobals:
        ENTER_MOVIE = 1
        EXIT_MOVIE = 2
        COUNTDOWN_TIME = 30
        BOARDING_TIME = 10.0
        ENTER_RACE_TIME = 6.0

        ERROR_CODE = PythonUtil.Enum( 'success, eGeneric, eTickets, eBoardOver, eNoKart, eOccupied, eTrackClosed, eTooLate, eUnpaid' )

        # Kart Pad Locations
        FRONT_LEFT_SPOT = 0
        FRONT_RIGHT_SPOT = 1
        REAR_LEFT_SPOT = 2
        REAR_RIGHT_SPOT = 3

        PAD_GROUP_NUM = 4

        def getPadLocation( padId ):
                return ( padId % KartGlobals.PAD_GROUP_NUM )

        getPadLocation = staticmethod( getPadLocation )
