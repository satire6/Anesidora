""" SuitPlannerBase module:  contains common code that both the server
    and client use when managing a collection of suits."""

# AI code should not import ShowBaseGlobal because it creates a graphics window
# If you need panda classes use PandaModules instead
# from ShowBaseGlobal import *
from pandac.PandaModules import *

import random
import string
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.hood import HoodUtil

class SuitPlannerBase:
    """
    /////////////////////////////////////////////////////////////////////////
    //
    // SuitPlannerBase class:  manages all suits which exist within a single
    //  neighborhood (or street), this base version contains general code
    //  that both the server and client can use, such as path generation
    //  code, dna storage, path point type storage
    //
    /////////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SuitPlannerBase')

    def __init__( self ):

        # initialize some values that we will be using
        #
        self.suitWalkSpeed = ToontownGlobals.SuitWalkSpeed

        # now load up the dna file for the neighborhood that this suit
        # planner is created for
        #
        self.dnaStore = None

        # keep a map of point indexes and the actual point so when
        # suits need to look up information from a point's index, they
        # can do it quickly without having to ask the dnaStore
        #
        self.pointIndexes = {}

        return None

    def setupDNA( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    load up DNA information for the neighborhood that
        //              this suit planner is in control of.  the DNA
        //              contains suit path information as well as vis
        //              group (zone) informations
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """

        if self.dnaStore:
            return None

        self.dnaStore = DNAStorage()
        dnaFileName = self.genDNAFileName()
        try:
            simbase.air.loadDNAFileAI( self.dnaStore, dnaFileName)
        except:
            loader.loadDNAFileAI( self.dnaStore, dnaFileName)
            

        # now create vis group (zone) information
        self.initDNAInfo()

    def genDNAFileName( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    determines the name of the DNA file that should
        //              be loaded for the neighborhood that this suit
        //              planner manages
        // Parameters:  none
        // Changes:     none
        ////////////////////////////////////////////////////////////////////
        """
        # This code might run on the AI or on the client.
        try:
            return simbase.air.genDNAFileName(self.getZoneId())

        except:
            # do some number manipulation of my zone id already given
            # to me and figure out which dna file to load

            zoneId = ZoneUtil.getCanonicalZoneId(self.getZoneId())
            hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
            hood = ToontownGlobals.dnaMap[hoodId]
            phase = ToontownGlobals.streetPhaseMap[hoodId]
            if hoodId == zoneId:
                zoneId = "sz"

            return "phase_%s/dna/%s_%s.dna" % (phase, hood, zoneId)


    def getZoneId( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    intended to be overridden by any inheriting suit
        //              planner class, and that class should be a
        //              distributed object or at least have an attribute
        //              named 'zoneId'
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        return self.zoneId

    def setZoneId( self, zoneId ):
        self.notify.debug( "setting zone id for suit planner" )
        self.zoneId = zoneId
        self.setupDNA()

    def extractGroupName(self, groupFullName):
        # The Idea here is that group names may have extra flags associated
        # with them that tell more information about what is special about
        # the particular vis zone. A normal vis zone might just be "13001",
        # but a special one might be "14356:safe_zone" or
        # "345:safe_zone:exit_zone"... These are hypotheticals. The main
        # idea is that there are colon separated flags after the initial
        # zone name.
        return(string.split(groupFullName, ":", 1)[0])

    def initDNAInfo( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    load up vis group information into a dictionary
        //              copied from HoodMgr.py
        // Parameters:  dnaStore, the dna storage structure to use
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        numGraphs = self.dnaStore.discoverContinuity()
        if numGraphs != 1:
            self.notify.info("zone %s has %s disconnected suit paths." % (self.zoneId, numGraphs))
        
        # Construct a dictionary of zone ids to battle cell center points
        self.battlePosDict = {}
        self.cellToGagBonusDict = {}
        #self.dnaStore.printSuitPointStorage()
        for i in range(self.dnaStore.getNumDNAVisGroupsAI()):
            vg = self.dnaStore.getDNAVisGroupAI(i)
            zoneId = int(self.extractGroupName(vg.getName()))
            # There is only 1 battle cell per zone
            if (vg.getNumBattleCells() == 1):
                battleCell = vg.getBattleCell(0)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            elif (vg.getNumBattleCells() > 1):
                self.notify.warning('multiple battle cells for zone: %d' % zoneId)
                # Just pick the first one
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            if True:
                # lets find the interactive props connected to this battle cell
                for i in range(vg.getNumChildren()):
                    childDnaGroup = vg.at(i)
                    if (isinstance(childDnaGroup, DNAInteractiveProp)):
                        self.notify.debug("got interactive prop %s" % childDnaGroup)
                        battleCellId = childDnaGroup.getCellId()
                        if battleCellId == -1:
                            self.notify.warning(                                
                                "interactive prop %s  at %s not associated with a a battle" %
                                (childDnaGroup, zoneId))
                        elif battleCellId == 0:
                            if self.cellToGagBonusDict.has_key(zoneId):
                                self.notify.error(
                                    "FIXME battle cell at zone %s has two props %s %s linked to it" %
                                    (zoneId, self.cellToGagBonusDict[zoneId], childDnaGroup))
                            else:
                                # based on the name of the prop, figure out which gag track bonus
                                name = childDnaGroup.getName()
                                propType = HoodUtil.calcPropType(name)
                                if propType in ToontownBattleGlobals.PropTypeToTrackBonus:
                                    trackBonus = ToontownBattleGlobals.PropTypeToTrackBonus[propType]
                                    self.cellToGagBonusDict[zoneId] = trackBonus

        # Now that we have extracted the vis groups we do not need
        # the dnaStore to keep them around
        self.dnaStore.resetDNAGroups()
        self.dnaStore.resetDNAVisGroups()
        self.dnaStore.resetDNAVisGroupsAI()

        # now load up the suit path points, separate them into types
        #
        self.streetPointList = []
        self.frontdoorPointList = []
        self.sidedoorPointList = []
        self.cogHQDoorPointList = []

        numPoints = self.dnaStore.getNumSuitPoints()
        for i in range(numPoints):
            point = self.dnaStore.getSuitPointAtIndex(i)
            if (point.getPointType() == DNASuitPoint.FRONTDOORPOINT):
                self.frontdoorPointList.append(point)
            elif (point.getPointType() == DNASuitPoint.SIDEDOORPOINT):
                self.sidedoorPointList.append(point)
            elif (point.getPointType() == DNASuitPoint.COGHQINPOINT or \
                  point.getPointType() == DNASuitPoint.COGHQOUTPOINT):
                self.cogHQDoorPointList.append(point)
            else:
                self.streetPointList.append(point)

            self.pointIndexes[ point.getIndex() ] = point

        # perform a simple path test to make sure we can properly
        # generate a path from two points given to us by the DNAStorage
        #
#        self.performPathTest()
        
        return None


    def performPathTest( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    test out path generation as well as travel time
        //              calculation for the current dnaStore information
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """

        if not self.notify.getDebug():
            return None
        
        #self.notify.debug( 'street points: ' + str( self.streetPointList ) )
        #self.notify.debug( 'front door points: ' +
        #                   str( self.frontdoorPointList ) )
        #self.notify.debug( 'side door points: ' +
        #                   str( self.sidedoorPointList ) )

        # create a simple path which will be only used for
        # testing the getSuitPath function of the dnaStorage
        #
        startAndEnd = self.pickPath()
        if not startAndEnd:
            return None

        startPoint = startAndEnd[ 0 ]
        endPoint = startAndEnd[ 1 ]

        path = self.dnaStore.getSuitPath( startPoint, endPoint )

#        print path

        # now print out travel time for each edge in the resulting path
        # as well as which zone each edge is in
        #
        numPathPoints = path.getNumPoints()
        for i in range( numPathPoints - 1 ):
            zone = self.dnaStore.getSuitEdgeZone(
                                   path.getPointIndex(i),
                                   path.getPointIndex(i+1) )
            travelTime = self.dnaStore.getSuitEdgeTravelTime(
                                   path.getPointIndex(i),
                                   path.getPointIndex(i+1),
                                   self.suitWalkSpeed )
            self.notify.debug(
                'edge from point ' + `i` +
                ' to point ' + `i+1` +
                ' is in zone: ' + `zone` +
                ' and will take ' + `travelTime` +
                ' seconds to walk.' )

        return None


    def genPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    generate a path using the local dnaStorage given
        //              the start and end points
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        return self.dnaStore.getSuitPath(startPoint, endPoint, minPathLen, maxPathLen)

    def getDnaStore( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    get the dnaStore from the suit planner, create the
        //              dnaStore if it has not already been loaded
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
#        if self.dnaStore == None:
#            self.setupDNA()
        return self.dnaStore

# history
#
# 12Feb01    jlbutler    created.
#


































