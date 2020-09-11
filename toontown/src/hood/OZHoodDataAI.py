from direct.directnotify import DirectNotifyGlobal
import HoodDataAI, ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.safezone import OZTreasurePlannerAI
from toontown.racing import DistributedStartingBlockAI
from pandac.PandaModules import *
from toontown.racing.RaceGlobals import *
from toontown.classicchars import DistributedGoofySpeedwayAI
from toontown.safezone import DistributedPicnicBasketAI
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI
from toontown.distributed import DistributedTimerAI
import string

from toontown.safezone import DistributedPicnicTableAI
from toontown.safezone import DistributedChineseCheckersAI
from toontown.safezone import DistributedCheckersAI

if( __debug__ ):
    import pdb

class OZHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("OZHoodDataAI")

    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.OutdoorZone
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)


    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

        if simbase.air.config.GetBool('create-chip-and-dale', 1):
            chip = DistributedChipAI.DistributedChipAI(self.air)
            chip.generateWithRequired(self.zoneId)
            chip.start()
            self.addDistObj(chip)

            dale = DistributedDaleAI.DistributedDaleAI(self.air, chip.doId)
            dale.generateWithRequired(self.zoneId)
            dale.start()
            self.addDistObj(dale)
            chip.setDaleId(dale.doId)
        
        self.treasurePlanner = OZTreasurePlannerAI.OZTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()
        
        self.timer = DistributedTimerAI.DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.zoneId)

        # Modularizing the Starting Blocks into DNA ( needs work )
        #self.createStartingBlocks()

        # create the picnic tables from the dna
        self.createPicnicTables()
        #Code Copy Paste, create game tables from dna
        
        if simbase.config.GetBool('want-game-tables', 0):
            self.createGameTables()

	#more hacks!
        #self.board = DChineseCheckersAI.DChineseCheckersAI(self.air, 'board',65,130,.2,0,0,0)
        #self.addDistObj(self.board)

        #self.newTable = DistributedPicnicTableAI.DistributedPicnicTableAI(self.air, 6000, 'table', 50, 130, .4, 0,0,0)
        #self.addDistObj(self.newTable)

        #self.checkerboard = DistributedCheckersAI.DistributedCheckersAI(self.air, self.newTable.doId, 'chinese', self.newTable.getX(),self.newTable.getY(), self.newTable.getZ(), 0,0,0)
        #self.addDistObj(self.newTable)



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
        self.timer.delete()
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
            
    def findAndCreateGameTables(self, dnaGroup, zoneId, area, overrideDNAZone = 0, type = 'game_table'):
        """Find and create golf karts from the given dna."""
        picnicTables = []
        picnicTableGroups = []

        #pdb.set_trace()

        if ((isinstance(dnaGroup, DNAGroup)) and (string.find(dnaGroup.getName(), type) >= 0)):

            if(type == 'game_table'):
                nameInfo = dnaGroup.getName().split('_')
            
                pos = Point3(0,0,0)
                hpr = Point3(0,0,0)
                for i in range(dnaGroup.getNumChildren()):
                    childDnaGroup = dnaGroup.at(i)
                    # TODO - check if DNAProp instance
                    if ((string.find(childDnaGroup.getName(), 'game_table') >= 0)):
                        pos = childDnaGroup.getPos()
                        hpr = childDnaGroup.getHpr()
                        break
                
                picnicTable = DistributedPicnicTableAI.DistributedPicnicTableAI(self.air, zoneId, nameInfo[2],
                                                                           pos[0], pos[1], pos[2],
                                                                           hpr[0], hpr[1], hpr[2])
               # checkerboard = DistributedChineseCheckersAI.DistributedChineseCheckersAI(self.air, picnicTable.doId,  'chinese', picnicTable.getX(), picnicTable.getY(), picnicTable.getZ(), hpr[0],hpr[1],hpr[2])
                
                #picnicTable.generateWithRequired(zoneId)
                picnicTables.append(picnicTable)
                #self.chineseCheckers.append(checkerboard)
        else:
            if (isinstance(dnaGroup, DNAVisGroup) and not overrideDNAZone):
                zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)

            for i in range(dnaGroup.getNumChildren()):
                childPicnicTables = self.findAndCreateGameTables(dnaGroup.at(i), zoneId, area, overrideDNAZone, type)
                picnicTables += childPicnicTables
        return picnicTables

    def findAndCreatePicnicTables(self, dnaGroup, zoneId, area, overrideDNAZone = 0, type = 'picnic_table'):
        """Find and create golf karts from the given dna."""
        picnicTables = []
        picnicTableGroups = []

        #pdb.set_trace()
        #self.notify.debug('dnaGroup=%s' % (dnaGroup.getName()))
        #bool1 = ((isinstance(dnaGroup, DNAGroup)))
       # findresult = ((isinstance(dnaGroup, DNAGroup)))
       # import pdb; pdb.set_trace()
              
                 
        if ((isinstance(dnaGroup, DNAGroup)) and (string.find(dnaGroup.getName(), type) >= 0)):

            if(type == 'picnic_table'):
                nameInfo = dnaGroup.getName().split('_')
            
                pos = Point3(0,0,0)
                hpr = Point3(0,0,0)
                for i in range(dnaGroup.getNumChildren()):
                    childDnaGroup = dnaGroup.at(i)
                    # TODO - check if DNAProp instance
                    if ((string.find(childDnaGroup.getName(), 'picnic_table') >= 0)):
                        pos = childDnaGroup.getPos()
                        hpr = childDnaGroup.getHpr()
                        break

                picnicTable = DistributedPicnicBasketAI.DistributedPicnicBasketAI(self.air, nameInfo[2],
                                                                           pos[0], pos[1], pos[2],
                                                                           hpr[0], hpr[1], hpr[2])
                #checkerboard = DistributedChineseCheckersAI.DistributedChineseCheckersAI(self.air, picnicTable.doId, 'chinese', picnicTable.getX(), picnicTable.getY(), picnicTable.getZ(), 0,0,0)
                
                picnicTable.generateWithRequired(zoneId)

                picnicTables.append(picnicTable)
                #self.chineseCheckers.append(checkerboarD)
        else:
            if (isinstance(dnaGroup, DNAVisGroup) and not overrideDNAZone):
                zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)

            for i in range(dnaGroup.getNumChildren()):
                childPicnicTables = self.findAndCreatePicnicTables(dnaGroup.at(i), zoneId, area, overrideDNAZone, type)
                picnicTables += childPicnicTables
        return picnicTables


    def createGameTables(self):
        """Create the golf karts in this hood."""

        #pdb.set_trace()
        
        self.gameTables = []
        #self.chineseCheckers = []
        for zone in self.air.zoneTable[ self.canonicalHoodId ]:
            zoneId = ZoneUtil.getTrueZoneId( zone[ 0 ], self.zoneId )
            dnaData = self.air.dnaDataMap.get( zone[ 0 ], None )

            if( isinstance( dnaData, DNAData ) ):
                area = ZoneUtil.getCanonicalZoneId( zoneId )
                foundTables =  self.findAndCreateGameTables(dnaData, zoneId, area , overrideDNAZone=True)
                self.gameTables += foundTables

        # Place each Golf Kart into the proper WaitEmpty State. Handle this
        # after each they have generated so that they are
        # placed in the proper active state.
        for picnicTable in self.gameTables:
            #picnicTable.start() USELESS FSM Function for other picnic table
            self.addDistObj( picnicTable )
        #for chineseCheckers in self.chineseCheckers:
            #self.addDistObj( chineseCheckers )


    def createPicnicTables(self):
        """Create the golf karts in this hood."""

        #pdb.set_trace()
        
        self.picnicTables = []
        for zone in self.air.zoneTable[ self.canonicalHoodId ]:
            zoneId = ZoneUtil.getTrueZoneId( zone[ 0 ], self.zoneId )
            dnaData = self.air.dnaDataMap.get( zone[ 0 ], None )

            if( isinstance( dnaData, DNAData ) ):
                area = ZoneUtil.getCanonicalZoneId( zoneId )
                foundTables =  self.findAndCreatePicnicTables(dnaData, zoneId, area , overrideDNAZone=True)
                self.picnicTables += foundTables

        # Place each Golf Kart into the proper WaitEmpty State. Handle this
        # after each they have generated so that they are
        # placed in the proper active state.
        #print "PICNIC TABLES" ,self.picnicTables
        for picnicTable in self.picnicTables:
            picnicTable.start()
            self.addDistObj( picnicTable )


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
