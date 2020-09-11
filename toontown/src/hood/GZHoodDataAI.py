from direct.directnotify import DirectNotifyGlobal
import HoodDataAI, ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.racing import DistributedStartingBlockAI
from pandac.PandaModules import *
from toontown.racing.RaceGlobals import *
from toontown.classicchars import DistributedGoofySpeedwayAI
from toontown.safezone import DistributedGolfKartAI
import string

if( __debug__ ):
    import pdb

class GZHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("GZHoodDataAI")

    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.GolfZone
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)


    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

        # Modularizing the Starting Blocks into DNA ( needs work )
        self.createStartingBlocks()

        # create the golf karts from the dna
        self.createGolfKarts()

        # create a temporary golf kart
        #golfKart = DistributedGolfKartAI.DistributedGolfKartAI(self.air)
        #golfKart.generateWithRequired(self.zoneId)
        #golfKart.start()
        #self.addDistObj(golfKart)
        #self.golfKart = golfKart        
        
        #Create Leader boards
        #self.cycleDuration = 10
        #self.createLeaderBoards()
        #self.__cycleLeaderBoards()

        #goofy = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
        #goofy.generateWithRequired(self.zoneId)
        #goofy.start()
        #self.addDistObj(goofy)

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
        
    def cleanup(self):
            #put away those billboards
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
        messenger.send( "GS_LeaderBoardSwap" )
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
        self.golfKartPads = []
        self.golfKartPadGroups = []

        for zone in self.air.zoneTable[ self.canonicalHoodId ]:
            zoneId = ZoneUtil.getTrueZoneId( zone[ 0 ], self.zoneId )
            dnaData = self.air.dnaDataMap.get( zone[ 0 ], None )

            if( isinstance( dnaData, DNAData ) ):
                area = ZoneUtil.getCanonicalZoneId( zoneId )
                foundRacingPads, foundRacingPadGroups = self.air.findRacingPads( dnaData, zoneId, area , overrideDNAZone=True)
                foundViewingPads, foundViewingPadGroups = self.air.findRacingPads( dnaData, zoneId, area, type='viewing_pad', overrideDNAZone=True )

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
            startingBlocks = self.air.findStartingBlocks( dnaGroup, distViewPad )
            for viewingBlock in self.viewingBlocks:
                distViewPad.addStartingBlock( viewingBlocks )

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

    def findAndCreateGolfKarts(self, dnaGroup, zoneId, area, overrideDNAZone = 0, type = 'golf_kart'):
        """Find and create golf karts from the given dna."""
        golfKarts = []
        golfKartGroups = []

        if ((isinstance(dnaGroup, DNAGroup)) and (string.find(dnaGroup.getName(), type) >= 0)):
            golfKartGroups.append(dnaGroup)
            if (type == 'golf_kart'):
                nameInfo = dnaGroup.getName().split('_')
                #pdb.set_trace()
                #print "Name Info: ", nameInfo
                #print "Race Info: ", raceInfo
                golfCourse = int(nameInfo[2])

                pos = Point3(0,0,0)
                hpr = Point3(0,0,0)
                for i in range(dnaGroup.getNumChildren()):
                    childDnaGroup = dnaGroup.at(i)
                    # TODO - check if DNAProp instance
                    if ((string.find(childDnaGroup.getName(), 'starting_block') >= 0)):
                        padLocation = dnaGroup.getName().split('_')[2]
                        pos = childDnaGroup.getPos()
                        hpr = childDnaGroup.getHpr()
                        break

                # lift the karts off the ground a bit so we can see their shadows in the tunnel
                pos += Point3(0, 0, 0.05)
                
                golfKart = DistributedGolfKartAI.DistributedGolfKartAI(self.air, golfCourse,
                                                                       pos[0], pos[1], pos[2],
                                                                       hpr[0], hpr[1], hpr[2])
            else:
                self.notify.warning('unhandled case')
            golfKart.generateWithRequired(zoneId)
            golfKarts.append(golfKart)
        else:
            if (isinstance(dnaGroup, DNAVisGroup) and not overrideDNAZone):
                zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)

            for i in range(dnaGroup.getNumChildren()):
                childGolfKarts, childGolfKartGroups = self.findAndCreateGolfKarts(dnaGroup.at(i), zoneId, area, overrideDNAZone, type)
                golfKarts += childGolfKarts
                golfKartGroups += childGolfKartGroups
        return golfKarts, golfKartGroups

    def createGolfKarts(self):
        """Create the golf karts in this hood."""
        self.golfKarts = []
        self.golfKartGroups = []
        for zone in self.air.zoneTable[ self.canonicalHoodId ]:
            zoneId = ZoneUtil.getTrueZoneId( zone[ 0 ], self.zoneId )
            dnaData = self.air.dnaDataMap.get( zone[ 0 ], None )

            if( isinstance( dnaData, DNAData ) ):
                area = ZoneUtil.getCanonicalZoneId( zoneId )
                foundKarts, foundKartGroups =  self.findAndCreateGolfKarts(dnaData, zoneId, area , overrideDNAZone=True)
                self.golfKarts += foundKarts
                self.golfKartGroups += foundKartGroups

        print self.golfKarts, self.golfKartGroups

        # Place each Golf Kart into the proper WaitEmpty State. Handle this
        # after each they have generated so that they are
        # placed in the proper active state.
        for golfKart in self.golfKarts:
            golfKart.start()
            self.addDistObj( golfKart )


    def findStartingBlocks(self, dnaRacingPadGroup, distRacePad):
        """
        Comment goes here...
        """
        startingBlocks = []
        # Search the children of the racing pad
        for i in range(dnaRacingPadGroup.getNumChildren()):
            dnaGroup = dnaRacingPadGroup.at(i)

            # TODO - check if DNAProp instance
            if ((string.find(dnaGroup.getName(), 'starting_block') >= 0)):
                padLocation = dnaGroup.getName().split('_')[2]
                pos = dnaGroup.getPos()
                hpr = dnaGroup.getHpr()

                if (isinstance(distRacePad, DistributedRacePadAI)):
                    sb = DistributedStartingBlockAI(self, distRacePad, pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2], int(padLocation))
                else:
                    sb = DistributedViewingBlockAI(self, distRacePad, pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2], int(padLocation))
                sb.generateWithRequired(distRacePad.zoneId)
                startingBlocks.append(sb)
            else:
                self.notify.debug("Found dnaGroup that is not a starting_block under a race pad group")
        return startingBlocks
