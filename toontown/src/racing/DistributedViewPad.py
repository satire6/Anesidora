##########################################################################
# Module: DistributedViewPad.py
# Purpose: This class provides the necessary functionality for 
# Date: 7/21/05
# Author: jjtaylor
##########################################################################

##########################################################################
# Panda Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from pandac.PandaModules import *

##########################################################################
# Toontown Import Modules
##########################################################################
from toontown.racing.DistributedKartPad import DistributedKartPad
from toontown.racing.KartShopGlobals import KartGlobals

if( __debug__ ):
    import pdb


class DistributedViewPad( DistributedKartPad ):
    """
    Purpose: Must fill out... DO NOT FORGET TO COMMENT CODE.
    """

    ######################################################################
    # Class Variables
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "DistributedViewPad" )
    #notify.setInfo(True)
    #notify.setDebug(True)
    id = 0

    def __init__( self, cr ):
        """
        COMMENT
        """

        # Initialize the KartPadAI and FSM Super Classes
        DistributedKartPad.__init__( self, cr )

        # Initialize Instance Variables
        self.id = DistributedViewPad.id
        DistributedViewPad.id += 1

        #self.av2TimestampDict = {}

    # this needs to be one message so there's no chance of out-of-order delivery
    def setLastEntered(self, timeStamp):
        self.timeStamp = timeStamp

    """
    def setAvEnterPad( self, avId, timeStamp ):
        error = "DistributedViewPad::setAvEnterTime - Avatar %s present in View Pad." % ( avId )
        assert not self.av2TimestampDict.has_key( avId ), error
        self.av2TimestampDict[ avId ] = timeStamp

    def setAvExitPad( self, avId ):
        error = "DistributedViewPad::setAvExit - Avatar %s not present in View Pad." % ( avId )
        assert self.av2TimestampDict.has_key( avId ), error
        del self.av2TimestampDict[ avId ]
    """
        
    def getTimestamp( self, avId ):
        """
        """
        #error = "DistributedViewPad::getTimestamp - Avatar %s not present in View Pad." % ( avId )
        #assert self.av2TimestampDict.has_key( avId ), error
        #return self.av2TimestampDict.get( avId )
        return self.timeStamp
    
    def addStartingBlock( self, block ):
        block.cameraPos = Point3(0, 23, 7)
        block.cameraHpr = Point3(180, -10, 0)
        DistributedKartPad.addStartingBlock(self, block)
