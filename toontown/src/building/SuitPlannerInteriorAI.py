""" SuitPlannerInteriorAI module:  contains the SuitPlannerInteriorAI
    class which handles management of all suits within a suit building."""

# AI code should not import ShowBaseGlobal because it creates a graphics window
# Use AIBaseGlobal instead
from otp.ai.AIBaseGlobal import *

import random
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedSuitAI
import SuitBuildingGlobals
import types

class SuitPlannerInteriorAI:
    """
    // SuitPlannerInteriorAI class:  manages all suits which exist within
    //  a single suit building.  This object only exists on the server AI.
    //
    // Attributes:
    //    none
    """

    # load a config file value to see if we should print out information
    # about this suit while it is thinking
    #
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'SuitPlannerInteriorAI')

    def __init__( self, numFloors, bldgLevel, bldgTrack, zone ):
        # when the suit planner interior is created, create information
        # about all suits that will exist in this building
        #

        self.dbg_4SuitsPerFloor = config.GetBool("4-suits-per-floor", 0)
        self.dbg_1SuitPerFloor = config.GetBool("1-suit-per-floor", 0)  # formerly called 'wuss-suits'

        self.zoneId = zone
        self.numFloors = numFloors

        # By default, if an invasion is in progress we only generate
        # suits of that kind.  Set this false to turn off this
        # behavior.
        self.respectInvasions = 1

        # This dbg var forces the creations of all 1 suit type (overrides level/type restrictions)
        dbg_defaultSuitName = simbase.config.GetString('suit-type', 'random')
        if (dbg_defaultSuitName == 'random'):
            self.dbg_defaultSuitType = None
        else:
            self.dbg_defaultSuitType = SuitDNA.getSuitType(dbg_defaultSuitName)

        if (isinstance(bldgLevel, types.StringType)):
            self.notify.warning('bldgLevel is a string!')
            bldgLevel = int(bldgLevel)
        self._genSuitInfos( numFloors, bldgLevel, bldgTrack )
        assert(len(self.suitInfos) > 0)

    def __genJoinChances( self, num ):
        joinChances = []
        for currChance in range( num ):
            joinChances.append( random.randint( 1, 100 ) )
        joinChances.sort( cmp )
        return joinChances

    def _genSuitInfos( self, numFloors, bldgLevel, bldgTrack ):
        """
        // Function:   create information about all suits that will exist
        //             in this building
        // Parameters: numFloors, number of floors in the building
        //             bldgLevel, how difficult the building is, based on
        //                        the suit that initially took the building
        //             bldgTrack, the track of the building, based on the
        //                        track that initially took the building
        // Changes:
        """
        self.suitInfos = []
        self.notify.debug( "\n\ngenerating suitsInfos with numFloors (" +
                           str( numFloors ) +
                           ") bldgLevel (" +
                           str( bldgLevel ) +
                           "+1) and bldgTrack (" +
                           str( bldgTrack ) + ")" )

        assert(bldgLevel >= 0 and 
               bldgLevel < len(SuitBuildingGlobals.SuitBuildingInfo))
        assert(numFloors > 0)

        # process each floor in the building and create all active and
        # reserve suits
        #
        for currFloor in range(numFloors):
            infoDict = {}
            lvls = self.__genLevelList(bldgLevel, currFloor, numFloors)

            # now randomly decide how many suits will be active and how
            # many will be in reserve, create the active suit objects
            # create the active suits in order of highest level to lowest
            # this is only because we want to make sure the highest level
            # active suit is in the first position in the list
            #
            activeDicts = []

            if (self.dbg_4SuitsPerFloor):
                numActive = 4
            else:
                numActive = random.randint( 1, min( 4, len( lvls ) ) )

            if ((currFloor + 1) == numFloors and len(lvls) > 1):
                # Make the boss be suit 1 (unless there is only 1 active suit)
                origBossSpot = len(lvls) - 1
                if (numActive == 1):
                    newBossSpot = numActive - 1
                else:
                    newBossSpot = numActive - 2
                tmp = lvls[newBossSpot]
                lvls[newBossSpot] = lvls[origBossSpot]
                lvls[origBossSpot] = tmp
                
            bldgInfo = SuitBuildingGlobals.SuitBuildingInfo[ bldgLevel ]  
            if len(bldgInfo) > SuitBuildingGlobals.SUIT_BLDG_INFO_REVIVES:
                revives = bldgInfo[ SuitBuildingGlobals.SUIT_BLDG_INFO_REVIVES ][0]
            else:
                revives = 0
            for currActive in range( numActive - 1, -1, -1 ):
                level = lvls[ currActive ]
                type = self.__genNormalSuitType( level )
                activeDict = {}
                activeDict['type'] = type
                activeDict['track'] = bldgTrack 
                activeDict['level'] = level
                activeDict['revives'] = revives
                activeDicts.append(activeDict)
            infoDict['activeSuits'] = activeDicts

            # now create the reserve suit objects, also assign each a
            # % join restriction, this indicates when the reserve suit
            # should join the battle based on how much damage has been
            # done to the suits currently in the battle
            #
            reserveDicts = []
            numReserve = len( lvls ) - numActive
            joinChances = self.__genJoinChances( numReserve )
            for currReserve in range( numReserve ):
                level = lvls[ currReserve + numActive ]
                type = self.__genNormalSuitType( level )
                reserveDict = {}
                reserveDict['type'] = type
                reserveDict['track'] = bldgTrack
                reserveDict['level'] = level
                reserveDict['revives'] = revives
                reserveDict['joinChance'] = joinChances[currReserve]
                reserveDicts.append(reserveDict)
            infoDict['reserveSuits'] = reserveDicts

            self.suitInfos.append(infoDict)

        #self.print()

    def __genNormalSuitType( self, lvl ):
        """
        // Function:   generate info for a normal suit that we might find
        //             in this particular building
        // Parameters: none
        // Changes:
        // Returns:    list containing the suit level, type, and track
        """
        # there is a similar formula in DistributedSuitPlannerAI used for
        # picking suit types for the streets, based on the suit level we
        # need to make sure we pick a valid suit type that can actually
        # be this level (each suit type can be 1 of 5 levels)
        #
        # TODO: track this formula down and make it use
        # SuitDNA.getRandomSuitType

        if (self.dbg_defaultSuitType != None):
            return self.dbg_defaultSuitType

        return SuitDNA.getRandomSuitType(lvl)

    def __genLevelList( self, bldgLevel, currFloor, numFloors ):
        """
        // Function:   based on a few parameters from the building, create
        //             a list of suit levels for a specific floor
        // Parameters: bldgLevel, the level of the current building (the
        //                        level of the suit that took it over, this
        //                        value is 0-based)
        //             currFloor, the current floor that we are calculating
        //             numFloors, the total number of floors in this bldg
        // Changes:
        // returns:    list of suit levels
        """
        assert(self.notify.debug('genLevelList(): floor: %d numFloors: %d' % \
                (currFloor + 1, numFloors)))
        bldgInfo = SuitBuildingGlobals.SuitBuildingInfo[ bldgLevel ]

        # For quick building battles during debug.
        if (self.dbg_1SuitPerFloor):
            return [1]    # 1 suit of max level 1
        elif (self.dbg_4SuitsPerFloor):
            return [5,6,7,10]  # a typical level with a higher level boss (must be at end)

        lvlPoolRange = bldgInfo[ SuitBuildingGlobals.SUIT_BLDG_INFO_LVL_POOL ]
        maxFloors =  bldgInfo[ SuitBuildingGlobals.SUIT_BLDG_INFO_FLOORS ][1]

        # now figure out which level pool multiplier to use
        #
        lvlPoolMults = bldgInfo[
            SuitBuildingGlobals.SUIT_BLDG_INFO_LVL_POOL_MULTS ]
        floorIdx = min(currFloor, maxFloors - 1)

        # now adjust the min and max level pool range based on the multipliers
        # we just got
        #
        lvlPoolMin = lvlPoolRange[ 0 ] * lvlPoolMults[ floorIdx ]
        lvlPoolMax = lvlPoolRange[ 1 ] * lvlPoolMults[ floorIdx ]

        # now randomly choose a level pool between the max and min
        #
        lvlPool = random.randint( int(lvlPoolMin), int(lvlPoolMax) )

        # find the min and max possible suit levels that we can create
        # for this level of building
        #
        lvlMin = bldgInfo[ SuitBuildingGlobals.SUIT_BLDG_INFO_SUIT_LVLS ][ 0 ]
        lvlMax = bldgInfo[ SuitBuildingGlobals.SUIT_BLDG_INFO_SUIT_LVLS ][ 1 ]

        # now randomly generate levels within our min and max, pulling
        # from our pool until we run out
        #
        self.notify.debug( "Level Pool: " + str( lvlPool ) )
        lvlList = []
        while lvlPool >= lvlMin:
            newLvl =  random.randint( lvlMin, min( lvlPool, lvlMax ) )
            lvlList.append( newLvl )
            lvlPool -= newLvl

        # now if we are on the top floor of the building, make sure to
        # add in a slot for the building boss
        #
        if currFloor + 1 == numFloors:
            bossLvlRange=bldgInfo[SuitBuildingGlobals.SUIT_BLDG_INFO_BOSS_LVLS]
            newLvl = random.randint( bossLvlRange[ 0 ], bossLvlRange[ 1 ] )
            assert(self.notify.debug('boss level: %d' % newLvl))
            lvlList.append( newLvl )
            

        lvlList.sort( cmp )
        self.notify.debug( "LevelList: " + repr( lvlList ) )
        return lvlList


    def __setupSuitInfo( self, suit, bldgTrack, suitLevel, suitType ):
        """
        create dna information for the given suit with the given track
        and suit type
        """
        suitName, skeleton = simbase.air.suitInvasionManager.getInvadingCog()
        if suitName and self.respectInvasions:
            # Override the suit type
            suitType = SuitDNA.getSuitType(suitName)
            # Override the building track
            bldgTrack = SuitDNA.getSuitDept(suitName)
            # if our type is already specified, we might need to
            # constrain the level to fit.
            suitLevel = min(max(suitLevel, suitType), suitType + 4)
        
        dna = SuitDNA.SuitDNA()
        dna.newSuitRandom( suitType, bldgTrack )
        suit.dna = dna
        self.notify.debug("Creating suit type " + suit.dna.name +
                          " of level " + str( suitLevel ) +
                          " from type " + str( suitType ) +
                          " and track " + str( bldgTrack ) )
        suit.setLevel( suitLevel )

        # We can't make a suit a skeleton until after generate.
        # Pass this info back so we know whether to do it or not
        return skeleton


    def __genSuitObject(self, suitZone, suitType, bldgTrack, suitLevel, revives = 0):
        """
        // Function:   generate a distributed suit object
        // Parameters:
        // Changes:
        // Returns:    the suit object created
        """
        newSuit = DistributedSuitAI.DistributedSuitAI( simbase.air, None )
        skel = self.__setupSuitInfo( newSuit, bldgTrack, suitLevel, suitType )
        if skel:
            newSuit.setSkelecog(1)
        newSuit.setSkeleRevives(revives)
        newSuit.generateWithRequired( suitZone )

        # Fill in the name so we can tell one suit from another in printouts.
        newSuit.node().setName('suit-%s' % (newSuit.doId))
        return newSuit

    def myPrint(self):
        """
        // Function:   print suit infos structure to see what and which
        //             suits exist on each floor of this building
        // Parameters: suitInfos, structure containing all suits in this
        //                        building
        // Changes:
        """
        self.notify.info("Generated suits for building: ")
        for currInfo in suitInfos:
            whichSuitInfo = suitInfos.index( currInfo ) + 1
            self.notify.debug( " Floor " + str( whichSuitInfo ) +
                               " has " +
                               str( len( currInfo[ 0 ] ) ) +
                               " active suits." )
            for currActive in range( len( currInfo [ 0 ] ) ):
                self.notify.debug( "  Active suit " +
                                   str( currActive + 1 ) +
                                   " is of type " +
                                   str( currInfo[ 0 ][ currActive ][ 0 ] ) +
                                   " and of track " +
                                   str( currInfo[ 0 ][ currActive ][ 1 ] ) +
                                   " and of level " +
                                   str( currInfo[ 0 ][ currActive ][ 2 ] ) )
                                                           
            self.notify.debug( " Floor " + str( whichSuitInfo ) +
                               " has " +
                               str( len( currInfo[ 1 ] ) ) +
                               " reserve suits." )
            for currReserve in range( len( currInfo[ 1 ] ) ):
                self.notify.debug( "  Reserve suit " +
                                   str( currReserve + 1 ) +
                                   " is of type " +
                                   str( currInfo[ 1 ][ currReserve ][ 0 ] ) +
                                   " and of track " +
                                   str( currInfo[ 1 ][ currReserve ][ 1 ] ) +
                                   " and of lvel " +
                                   str( currInfo[ 1 ][ currReserve ][ 2 ] ) +
                                   " and has " +
                                   str( currInfo[ 1 ][ currReserve ][ 3 ] ) +
                                   "% join restriction." )

    def genFloorSuits(self, floor):
        """
        """
        assert(floor < len(self.suitInfos))
        assert(self.notify.debug('generating suits for floor: %d' % floor))
        suitHandles = {}
        floorInfo = self.suitInfos[floor] 

        activeSuits = []
        for activeSuitInfo in floorInfo['activeSuits']:
            suit = self.__genSuitObject(self.zoneId,
                                activeSuitInfo['type'],
                                activeSuitInfo['track'],        
                                activeSuitInfo['level'],
                                activeSuitInfo['revives'])
  
            activeSuits.append(suit)
        assert(len(activeSuits) > 0)
        suitHandles['activeSuits'] = activeSuits

        reserveSuits = []
        for reserveSuitInfo in floorInfo['reserveSuits']:
            suit = self.__genSuitObject(self.zoneId,
                                reserveSuitInfo['type'],
                                reserveSuitInfo['track'],        
                                reserveSuitInfo['level'],
                                reserveSuitInfo['revives'])
            reserveSuits.append((suit, reserveSuitInfo['joinChance']))
        suitHandles['reserveSuits'] = reserveSuits

        return suitHandles

    def genSuits( self ):
        """
        // Function:   for each floor, create a list of active and reserve
        //             suits that should exist inside of a suit building
        // Parameters: none
        // Changes:
        // Returns:    a map 
        """
        assert(self.notify.debug('genSuits() for zone: %d' % self.zoneId))

        suitHandles = []
        # process each floor in the building and create all active and
        # reserve suits
        #
        for floor in range(len(self.suitInfos)):
            floorSuitHandles = self.genFloorSuits(floor)
            suitHandles.append(floorSuitHandles)

        return suitHandles


# History
#
# 13Aug01   jlbutler   created.
# 14Aug01   jlbutler   modified to have two separate steps, the first is done
#                      automatically when the SuitPlannerInteriorAI is created,
#                      which creates all suit information for the building (this way
#                      the same suits will be in this building until it is taken back
#                      by toons), the second step is done when genSuits is called, this
#                      creates the actual suit objects for the entire building (only
#                      needed to be done when a toon enters the building)
