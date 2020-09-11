from direct.directnotify import DirectNotifyGlobal
import HoodDataAI, ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.racing import DistributedStartingBlockAI
from pandac.PandaModules import *
from toontown.racing.RaceGlobals import *
from toontown.classicchars import DistributedGoofySpeedwayAI

if( __debug__):
    import pdb

class GSHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("GSHoodDataAI")

    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.GoofySpeedway
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

        # Modularizing the Starting Blocks into DNA ( needs work )
        self.createStartingBlocks()

        #Create Leader boards
        self.cycleDuration = 10
        self.createLeaderBoards()
        self.__cycleLeaderBoards()

        self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
        self.addDistObj(self.classicChar)

        messenger.send("GSHoodSpawned", [self])

        #if( __debug__ ):
        #    racePadAI = self.air.getRacingPadList()
        #    viewPadAI = self.air.getViewPadList()

        #    sBlockAI = self.air.getStartingBlockDict()
        #    vBlockAI = self.air.getViewingBlockDict()

        #    for racePadId in racePadAI:
        #        print "RacePad %s has starting blocks %s\n" %( racePadId, sBlockAI.get( racePadId )  )

        #    for viewPadId in viewPadAI:
        #        print "viewPad %s has starting blocks %s\n" %( viewPadId, vBlockAI.get( viewPadId )  )

        #    pdb.set_trace()

    def shutdown(self):
        self.notify.debug( "shutting down GSHoodDataAI: %s" % self.zoneId )
        messenger.send("GSHoodDestroyed", [self])
        HoodDataAI.HoodDataAI.shutdown(self)

    def cleanup(self):
        # put away those billboards
        self.notify.debug( "cleaning up GSHoodDataAI: %s" % self.zoneId )
        taskMgr.removeTasksMatching( str(self)+"_leaderBoardSwitch" )
        for board in self.leaderBoards:
            board.delete()
        del self.leaderBoards

    def createLeaderBoards(self):
        #find the leader boards from the level dna
        #and add distributed object based on that

        self.leaderBoards = []
        dnaStore = DNAStorage()
        dnaData = simbase.air.loadDNAFileAI(dnaStore,
                  simbase.air.lookupDNAFileName("goofy_speedway_sz.dna"))

        if( isinstance( dnaData, DNAData ) ):
             self.leaderBoards = self.air.findLeaderBoards( dnaData, self.zoneId )


        for distObj in self.leaderBoards:
                if distObj:
                    # Set Initial Subscriptions of leader boards
                    # Python 2.2 doesn't support this string op!
                    #if( "city" in distObj.getName() ):
                    if distObj.getName().count("city"):
                        type = "city"
                    #elif( "stadium" in distObj.getName() ):
                    elif distObj.getName().count("stadium"):
                        type = "stadium"
                    #elif( "country" in distObj.getName() ):
                    elif distObj.getName().count("country"):
                        type = "country"

                    for subscription in LBSubscription[ type ]:
                        distObj.subscribeTo( subscription )

                    self.addDistObj( distObj )

    def __cycleLeaderBoards( self, task = None ):
        messenger.send( "GS_LeaderBoardSwap" + str(self.zoneId) )
        # prep for the next cycle
        #self.notify.info( "__cycleLeaderBoards: Cycling Leader Boards." )
        taskMgr.doMethodLater( self.cycleDuration, self.__cycleLeaderBoards, str(self)+"_leaderBoardSwitch" )

    def createStartingBlocks(self):
        """
        Purpose: The createStartingBlocks Method...
        Params: None
        Return: None
        """

        # Create the DistributedRacePadAI Objects
        self.racingPads = []
        self.viewingPads = []
        self.viewingBlocks = []
        self.startingBlocks = []
        self.foundRacingPadGroups = []
        self.foundViewingPadGroups = []

        for zone in self.air.zoneTable[ self.canonicalHoodId ]:
            zoneId = ZoneUtil.getTrueZoneId( zone[ 0 ], self.zoneId )
            dnaData = self.air.dnaDataMap.get( zone[ 0 ], None )

            if( isinstance( dnaData, DNAData ) ):
                area = ZoneUtil.getCanonicalZoneId( zoneId )
                foundRacingPads, foundRacingPadGroups = self.air.findRacingPads( dnaData, zoneId, area )
                foundViewingPads, foundViewingPadGroups = self.air.findRacingPads( dnaData, zoneId, area, type='viewing_pad' )

                # Maintain Lists of found racing pads and groups.
                self.racingPads += foundRacingPads
                self.foundRacingPadGroups += foundRacingPadGroups

                self.viewingPads += foundViewingPads
                self.foundViewingPadGroups += foundViewingPadGroups

        # Next, create the DistributedStartingBlockAI objects for each
        # racepad.
        self.startingBlocks = []
        for dnaGroup, distRacePad in zip( self.foundRacingPadGroups, self.racingPads ):
            startingBlocks = self.air.findStartingBlocks( dnaGroup, distRacePad )
            self.startingBlocks += startingBlocks
            for startingBlock in startingBlocks:
                distRacePad.addStartingBlock( startingBlock )

        for distObj in self.startingBlocks:
            self.addDistObj( distObj )

        for dnaGroup, distViewPad in zip( self.foundViewingPadGroups, self.viewingPads ):
            viewingBlocks = self.air.findStartingBlocks( dnaGroup, distViewPad )
            self.viewingBlocks += viewingBlocks
            for viewingBlock in viewingBlocks:
                distViewPad.addStartingBlock( viewingBlock )

        for distObj in self.viewingBlocks:
            self.addDistObj( distObj )

        for viewPad in self.viewingPads:
            self.addDistObj( viewPad )

        # Place each RacePad into the proper WaitEmpty State. Handle this
        # after each starting block has been generated so that they are
        # placed in the proper active state.
        for racePad in self.racingPads:
            racePad.request( 'WaitEmpty' )
            self.addDistObj( racePad )
