"""SuitBase module: contains the SuitBase class"""

# AI code should not import ShowBaseGlobal because it creates a graphics window
# from ShowBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *

import math
import random
from pandac.PandaModules import Point3
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
import SuitTimings
import SuitDNA
from toontown.toonbase import TTLocalizer

# extra time to add (in seconds) to any time calculations for path movement
# for each leg
#
TIME_BUFFER_PER_WPT = 0.25
TIME_DIVISOR        = 100

# spread out the creation of this suit's task, helps to prevent
# slowdowns, but causes suits to take longer to get moving
#
DISTRIBUTE_TASK_CREATION = 0

class SuitBase:
    """
    ////////////////////////////////////////////////////////////////////////
    // SuitBase class:  a 'bad guy' which contains common functionality
    //                  that both a client side and a server side suit can
    //                  use
    //
    // Attributes:
    //
    ////////////////////////////////////////////////////////////////////////
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitBase')
    def __init__(self):
        self.dna = None
        self.level = 0
        # This gets initialized to real value in d_setLevel()
        self.maxHP = 10
        self.currHP = 10
        self.isSkelecog = 0

    def delete(self):
        return

    def getStyleName(self):
        if (hasattr(self, "dna") and self.dna):
            return self.dna.name
        else:
            self.notify.error('called getStyleName() before dna was set!')
            return 'unknown'

    def getStyleDept(self):
        if (hasattr(self, "dna") and self.dna):
            return SuitDNA.getDeptFullname(self.dna.dept)
        else:
            self.notify.error('called getStyleDept() before dna was set!')
            return 'unknown'

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level
        nameWLevel = TTLocalizer.SuitBaseNameWithLevel % {"name":  self.name,
                                                        "dept":  self.getStyleDept(),
                                                        "level": self.getActualLevel(),}
        self.setDisplayName( nameWLevel )
        # Compute maxHP based on level
        attributes = SuitBattleGlobals.SuitAttributes[self.dna.name]
        self.maxHP = attributes['hp'][self.level]
        self.currHP = self.maxHP

    def getSkelecog(self):
        return self.isSkelecog
        
    def setSkelecog(self, flag):
        self.isSkelecog = flag

    def getActualLevel( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   from the suit's 'relative' level (relative to the
        //             type of suit that this guy is) figure out the suit's
        //             actual level (1-12)
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        if hasattr(self, "dna"):
            return SuitBattleGlobals.getActualFromRelativeLevel(
                self.getStyleName(),
                self.level ) + 1
        else:
            self.notify.warning('called getActualLevel with no DNA, returning 1 for level')
            return 1

    def setPath( self, path ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    set the path to be used by this suit, this function
        //              is called by the SuitPlannerAI
        // Parameters:  path, the path that this suit should use
        // Changes:     none
        ////////////////////////////////////////////////////////////////////
        """
        self.path = path
        self.pathLength = self.path.getNumPoints()

    def getPath( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    set the path to be used by this suit, this function
        //              is called by the SuitPlannerAI
        // Parameters:  path, the path that this suit should use
        // Changes:     none
        ////////////////////////////////////////////////////////////////////
        """
        return self.path

    def printPath( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    print out this suit's current path
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # print out the path
        #
        print "%d points in path" % self.pathLength
#        print self.path
        for currPathPt in range( self.pathLength ):
            indexVal = self.path.getPointIndex( currPathPt )
            print "\t", self.sp.dnaStore.getSuitPointWithIndex( indexVal )

    def makeLegList(self):
        """makeLegList(self)

        Fills up self.legList with a list of SuitLeg objects that
        reflect the path previously set via setPath().  See
        suitLegList.h.
        """

        self.legList = SuitLegList(self.path, self.sp.dnaStore,
                                   self.sp.suitWalkSpeed,
                                   SuitTimings.fromSky,
                                   SuitTimings.toSky,
                                   SuitTimings.fromSuitBuilding,
                                   SuitTimings.toSuitBuilding,
                                   SuitTimings.toToonBuilding)


# history
#
# 14Feb01       jlbutler        created
#


