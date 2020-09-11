"""HoodMgr module: contains the HoodMgr class"""

from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.launcher import DownloadForceAcknowledge
import string
import random
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
# import pdb

class HoodMgr(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("HoodMgr")

    # We'd like first-timers to drop in with the trolley in view
    ToontownCentralInitialDropPoints = (
        [-90.7, -60.0, 0.025, 102.575, 0, 0],
        [-91.4, -40.5, -3.948, 125.763, 0, 0],
        [-107.8, -17.8, -1.937, 149.456, 0, 0],
        [-108.7, 12.8, -1.767, 158.756, 0, 0],
        [-42.1, -22.8, -1.328, -248.1, 0, 0],
        [-35.2, -60.2, 0.025, -265.639, 0, 0],
        )

    ToontownCentralHQDropPoints = (
        [-43.5, 42.6, -0.550, -100.454, 0, 0],
        [-53.0, 12.5, -2.948, 281.502, 0, 0],
        [-40.3, -18.5, -0.913, -56.674, 0, 0],
        [-1.9, -37.0, 0.025, -23.430, 0, 0],
        [1.9, -5.9, 4.0, -37.941, 0, 0],
        )

    ToontownCentralTunnelDropPoints = (
        [-28.3, 40.1, 00.25, 17.25, 0, 0],
        [-63.75, 58.96, -0.5, -23.75, 0, 0],
        [-106.93, 17.66, -2.2, 99.0, 0, 0],
        [-116.0, -21.5, -0.038, 50.0, 0, 0],
        [74.88, -115.0, 2.53, -224.41, 0, 0],
        [30.488, -101.5, 2.53, -179.23, 0, 0],
        )

    dropPoints = {
        ToontownGlobals.DonaldsDock: (
        [-28.0, -2.5, 5.8, 120.0, 0.0, 0.0],
        [-22, 13, 5.8, 155.6, 0.0, 0.0],
        [67, 47, 5.7, 134.7, 0.0, 0.0],
        [62, 19, 5.7, 97.0, 0.0, 0.0],
        [66, -27, 5.7, 80.5, 0.0, 0.0],
        [-114, -7, 5.7, -97.0, -0.0, 0.0],
        [-108, 36, 5.7, -153.8, -0.0, 0.0],
        [-116, -46, 5.7, -70.1, -0.0, 0.0],
        [-63, -79, 5.7, -41.2, -0.0, 0.0],
        [-2, -79, 5.7, 57.4, -0.0, 0.0],
        [-38, -78, 5.7, 9.1, -0.0, 0.0],
        ),
        
        ToontownGlobals.ToontownCentral: (
        [-60, -8, 1.3, -90, 0, 0],  # veranda center
        [-66, -9, 1.3, -274, 0, 0],  # veranda off-center
        [17, -28, 4.1, -44, 0, 0],  # courtyard
        [87.7, -22, 4, 66, 0, 0],
        [-9.6, 61.1, 0, 132, 0, 0],
        [-109.0, -2.5, -1.656, -90, 0, 0],  # front of bridge
        [-35.4, -81.3, 0.5, -4, 0, 0],
        [-103, 72, 0, -141, 0, 0],
        [93.5, -148.4, 2.5, 43, 0, 0],
        [25, 123.4, 2.55, 272, 0, 0],
        [48, 39, 4, 201, 0, 0],   #facing library
        [-80, -61, 0.1, -265, 0, 0],
        [-46.875, 43.68, -1.05, 124, 0, 0],
        [34, -105, 2.55, 45, 0, 0],
        [16, -75, 2.55, 56, 0, 0],
        [-27, -56, 0.1, 45, 0, 0],       

        [100, 27, 4.1, 150, 0, 0],
        [-70, 4.6, -1.9, 90, 0, 0],
        [-130.7, 50, 0.55, -111, 0, 0],
        ),

        ToontownGlobals.TheBrrrgh: (
        [35, -32, 6.2, 138, 0.0, 0.0],
        [26, -105, 6.2, -339, 0.0, 0.0],
        [-29, -139, 6.2, -385, 0.0, 0.0],
        [-79, -123, 6.2, -369, 0.0, 0.0],
        [-114, -86, 3, -54, 0.0, 0.0],
        [-136, 9, 6.2, -125, 0.0, 0.0],
        [-75, 92, 6.2, -187, 0.0, 0.0],
        [-7, 75, 6.2, -187, 0.0, 0.0],
        [-106, -42, 8.6, -111, 0.0, 0.0], # hilltop 1
        [-116, -44, 8.3, -20, 0.0, 0.0], # hilltop 2
        ),

        ToontownGlobals.MinniesMelodyland: (
        [86, 44, -13.5, 121.1, 0.0, 0.0],
        [88, -8, -13.5, 91, 0, 0],
        [92, -76, -13.5, 62.5, 0.0, 0.0],
        [53, -112, 6.5, 65.8, 0.0, 0.0],
        [-69, -71, 6.5, -67.2, 0.0, 0.0],
        [-75, 21, 6.5, -100.9, 0.0, 0.0],
        [-21, 72, 6.5, -129.5, 0.0, 0.0],
        [56, 72, 6.5, 138.2, 0.0, 0.0],
        [-41, 47, 6.5, -98.9, 0.0, 0.0],
        ),

        ToontownGlobals.DaisyGardens: (
        [0, 0, 0, -10.5, 0, 0],
        [76, 35, 1.1, -30.2, 0.0, 0.0],
        [97, 106, 0.0, 51.4, 0.0, 0.0],
        [51, 180, 10.0, 22.6, 0.0, 0.0],
        [-14, 203, 10.0, 85.6, 0.0, 0.0],
        [-58, 158, 10.0, -146.9, 0.0, 0.0],
        [-86, 128, 0.0, -178.9, 0.0, 0.0],
        [-64, 65, 0.0, 17.7, 0.0, 0.0],
        [-13, 39, 0.0, -15.7, 0.0, 0.0],
        [-12, 193, 0.0, -112.4, 0.0, 0.0],
        [87, 128, 0.0, 45.4, 0.0, 0.0],
        ),

        ToontownGlobals.DonaldsDreamland: (
        [77, 91, 0.0, 124.4, 0.0, 0.0],
        [29, 92, 0.0, -154.5, 0.0, 0.0],
        [-28, 49, -16.4, -142.0, 0.0, 0.0],
        [21, 40, -16.0, -65.1, 0.0, 0.0],
        [48, 27, -15.4, -161.0, 0.0, 0.0],
        [-2, -22, -15.2, -132.1, 0.0, 0.0],
        [-92, -88, 0.0, -116.3, 0.0, 0.0],
        [-56, -93, 0.0, -21.5, 0.0, 0.0],
        [20, -88, 0.0, -123.4, 0.0, 0.0],
        [76, -90, 0.0, 11.0, 0.0, 0.0],
        ),

        ToontownGlobals.GoofySpeedway: (
        [-0.7, 62, 0.08, 182, 0, 0],
        [-1, -30, 0.06, 183, 0, 0],
        [-13, -120, 0, 307, 0, 0],
        [16.4, -120, 0, 65, 0, 0],
        [-0.5, -90, 0, 182, 0, 0],
        [-30, -25, -0.373, 326, 0, 0],
        [29, -17, -0.373, 32, 0, 0],
        ),

        ToontownGlobals.GolfZone: (
        [-49.6, 102, 0, 162, 0, 0],
        [-22.8, 36.6, 0, 157.5, 0, 0],
        [40, 51, 0, 185, 0, 0],
        [48.3, 122.2, 0, 192, 0, 0],
        [106.3, 69.2, 0, 133, 0, 0],
        [-81.5, 47.2, 0, 183, 0, 0],
        [-80.5, -84.2, 0, 284, 0, 0],
        [73, -111, 0, 354, 0, 0],
        ),

        ToontownGlobals.OutdoorZone: (
        [-165.8, 108, 0.025, 252, 0, 0],
        [21, 130, 0.16, 170, 0, 0],
        [93, 78.5, 0.23, 112, 0, 0],
        [79, -1.6, 0.75, 163, 0, 0],
        [10, 33, 5.32, 130.379, 0, 0],
        [-200, -42, 0.025, 317.543, 0, 0],
        [-21, -65, 0.335, -18, 0, 0],
        [23, 68.5, 4.510, -22.808, 0, 0],
        ),

        ToontownGlobals.Tutorial: (
        [130.9, -8.6, -1.3, 105.5, 0, 0],
        ),
        
        ToontownGlobals.SellbotHQ:(
        [64, -128, 0.26, 36, 0, 0],
        [9, -140, 0.26, 0, 0, 0],
        [-82, -112, 0.26, -127, 0, 0],
        [-73, -213, 0.26, -23, 0, 0],
        [-20, -243, 0.26, -9, 0, 0],
        [79, -208, 0.26, 43, 0, 0],
        ),

        ToontownGlobals.CashbotHQ:(
        [102, -437, -23.439, 360, 0, 0],
        [124, -437, -23.439, 360, 0, 0],
        [110, -446, -23.439, 360, 0, 0],
        [132, -446, -23.439, 360, 0, 0],
        #[133, 512, 32.246, 360, 0, 0],  #this point is right in front of the CFO door
        ),

        ToontownGlobals.LawbotHQ:(
        [77.50, 129.13, -68.4, -166.6, 0, 0],
        [-57.70, 80.75, -68.4, -139.2, 0, 0],
        [203.30, 46.36, -68.4, -213.37, 0, 0],
        [88.2, -336.52, -68.4, -720.4, 0, 0],
        [232.77, -305.33, -68.4, -651, 0, 0],
        [-20.16, -345.76, -68.4, -777.98, 0 ,0],
        ),
        }

    hoodName2Id = {
        "dd": ToontownGlobals.DonaldsDock,
        "tt": ToontownGlobals.ToontownCentral,
        "br": ToontownGlobals.TheBrrrgh,
        "mm": ToontownGlobals.MinniesMelodyland,
        "dg": ToontownGlobals.DaisyGardens,
        "oz": ToontownGlobals.OutdoorZone,
        "ff": ToontownGlobals.FunnyFarm,
        "gs": ToontownGlobals.GoofySpeedway,
        "dl": ToontownGlobals.DonaldsDreamland,
        "bosshq": ToontownGlobals.BossbotHQ,
        "sellhq": ToontownGlobals.SellbotHQ,
        "cashhq": ToontownGlobals.CashbotHQ,
        "lawhq": ToontownGlobals.LawbotHQ,
        "gz": ToontownGlobals.GolfZone,
        }

    hoodId2Name = {
        ToontownGlobals.DonaldsDock: "dd",
        ToontownGlobals.ToontownCentral: "tt",
        # This is a hack to handle the fact that the tutorial tunnel
        # connects to the Toontown Central Playground. Maybe there is
        # a cleaner way.
        ToontownGlobals.Tutorial: "tt",
        ToontownGlobals.TheBrrrgh: "br",
        ToontownGlobals.MinniesMelodyland: "mm",
        ToontownGlobals.DaisyGardens: "dg",
        ToontownGlobals.OutdoorZone: "oz",
        ToontownGlobals.FunnyFarm: "ff",
        ToontownGlobals.GoofySpeedway: "gs",
        ToontownGlobals.DonaldsDreamland: "dl",
        ToontownGlobals.BossbotHQ: "bosshq",
        ToontownGlobals.SellbotHQ: "sellhq",
        ToontownGlobals.CashbotHQ: "cashhq",
        ToontownGlobals.LawbotHQ: "lawhq",
        ToontownGlobals.GolfZone: "gz",
        }

    DefaultDropPoint = [0, 0, 0, 0, 0, 0]

    dbgDropMode = 0     # set to 1 to debug cycle through drop points
    currentDropPoint = 0

    def __init__(self, cr):
        assert(self.notify.debug("HoodMgr()"))
        self.cr = cr

    def getDropPoint(self, dropPointList):
        if (self.dbgDropMode == 0):
             return random.choice(dropPointList)
        else:
            # step through them all sequentially for checking purposes
            droppnt = self.currentDropPoint % len(dropPointList)
            self.currentDropPoint = (self.currentDropPoint + 1) % len(dropPointList)
            return dropPointList[droppnt]

    def getAvailableZones(self):
        assert(self.notify.debug("getAvailableZones()"))
        # HACK!
        if (base.launcher == None):
            # if we don't have a launcher, assume all zones available
            return (self.getZonesInPhase(4) +
                    self.getZonesInPhase(6) +
                    self.getZonesInPhase(8) +
                    self.getZonesInPhase(9) +
                    self.getZonesInPhase(10) +
                    self.getZonesInPhase(11) +
                    self.getZonesInPhase(12) +
                    self.getZonesInPhase(13)
                    )
        else:
            zones = []
            # loop through all zones and see which are loaded
            for phase in set(ToontownGlobals.phaseMap.values()):
                if (base.launcher.getPhaseComplete(phase)):
                    # look up zones in this phase and add to list
                    zones = zones + self.getZonesInPhase(phase)
            return zones

    def getZonesInPhase(self, phase):
        assert(self.notify.debug("getZonesInPhase()"))
        # return the zone id's available in given phase
        p = []
        for i in ToontownGlobals.phaseMap.items():
            if (i[1] == phase):
                p.append(i[0])
        return p

    def getPhaseFromHood(self, hoodId):
        hoodId = ZoneUtil.getCanonicalHoodId(hoodId)
        assert(self.notify.debug("getPhaseFromHood()"))
        # return the phase that the specified zone is in
        assert(ToontownGlobals.phaseMap.has_key(hoodId))
        return ToontownGlobals.phaseMap[hoodId]

    # TODO: put these points in the dna
    def getPlaygroundCenterFromId(self, hoodId):
        """
        return the coords for the center of the safe zone.
        """
        assert(self.notify.debug("getPlaygroundCenterFromId()"))
        dropPointList = self.dropPoints.get(hoodId, None)
        if dropPointList:
            return self.getDropPoint(dropPointList)
        else:
            self.notify.warning("getPlaygroundCenterFromId: No such hood name as: " + str(hoodId))
            return self.DefaultDropPoint

    def getIdFromName(self, hoodName):
        assert(self.notify.debug("getIdFromName()"))
        id = self.hoodName2Id.get(hoodName)
        if id:
            return id
        else:
            self.notify.error("No such hood name as: %s" % hoodName)
            return None

    def getNameFromId(self, hoodId):
        assert(self.notify.debug("getNameFromId()"))
        name = self.hoodId2Name.get(hoodId)
        if name:
            return name
        else:
            self.notify.error("No such hood id as: %s" % hoodId)
            return None

    def getFullnameFromId(self, hoodId):
        assert(self.notify.debug("getFullnameFromId()"))
        hoodId = ZoneUtil.getCanonicalZoneId(hoodId)
        return ToontownGlobals.hoodNameMap[hoodId][-1]

    def addLinkTunnelHooks(self, hoodPart, nodeList, currentZoneId):
        assert(self.notify.debug("addLinkTunnelHooks()"))
        # hoodPart should be a SafeZone or a Town
        # Examine each vis group for tunnels

        # Return a list of the tunnelOriginPlaceHolders so the
        # caller can remove them when he is done with them
        tunnelOriginList = []

        for i in nodeList:
            linkTunnelNPC = i.findAllMatches("**/linktunnel*")
            for p in range(linkTunnelNPC.getNumPaths()):
                linkTunnel = linkTunnelNPC.getPath(p)
                name = linkTunnel.getName()
                # Assuming a name like: "linktunnel_mm_3456_DNARoot"
                nameParts = name.split("_")
                # Name parts will be something like ['linktunnel', 'mm', '3456', 'DNARoot']
                hoodStr = nameParts[1]
                zoneStr = nameParts[2]
                hoodId = self.getIdFromName(hoodStr)
                zoneId = int(zoneStr)
                hoodId = ZoneUtil.getTrueZoneId(hoodId, currentZoneId)
                zoneId = ZoneUtil.getTrueZoneId(zoneId, currentZoneId)
                
                # Get the actual collision sphere node
                linkSphere = linkTunnel.find("**/tunnel_trigger")
                # HACK: until cog tunnel trigger is renamed
                if linkSphere.isEmpty():
                    linkSphere = linkTunnel.find("**/tunnel_sphere")
                if not linkSphere.isEmpty():
                    # ...first time through this geometry.
                    # Rename it to make it unique
                    cnode = linkSphere.node()
                    cnode.setName("tunnel_trigger_" + hoodStr + "_" + zoneStr)
                    # It should be collidable to ghosts too
                    cnode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.GhostBitmask)
                else:
                    # ...we've been through this already (i.e. we may have
                    # gone into a building and then went out again).
                    linkSphere=linkTunnel.find("**/tunnel_trigger_"
                            + hoodStr + "_" + zoneStr)
                    if linkSphere.isEmpty():
                        self.notify.error("tunnel_trigger not found")

                # Get the actual tunnel_origin
                tunnelOrigin = linkTunnel.find("**/tunnel_origin")
                if tunnelOrigin.isEmpty():
                    self.notify.error("tunnel_origin not found")
                # Create a place holder node
                tunnelOriginPlaceHolder = render.attachNewNode(
                        'toph_' + hoodStr + '_' + zoneStr)
                tunnelOriginList.append(tunnelOriginPlaceHolder)

                # Set the pos and hpr of the place holder
                tunnelOriginPlaceHolder.setPos(tunnelOrigin.getPos(render))
                tunnelOriginPlaceHolder.setHpr(tunnelOrigin.getHpr(render))

                # Determine based on hood id and zone id which hood and which
                # branch or safe zone to go to. Add a hook so that when the avatar
                # enters the tunnel, we are informed which hood it goes to and which zone
                hood=base.localAvatar.cr.playGame.hood
                # If we are in the tutorial, we will want to
                # teleport into the safe zone. Otherwise, we will
                # want to tunnel in.
                if ZoneUtil.tutorialDict:
                    how = "teleportIn"
                    tutorialFlag = 1
                else:
                    how = "tunnelIn"
                    tutorialFlag = 0
                hoodPart.accept("enter" + linkSphere.getName(),
                                hoodPart.handleEnterTunnel,
                                [{"loader": ZoneUtil.getLoaderName(zoneId),
                                  "where": ZoneUtil.getToonWhereName(zoneId),
                                  "how": how,
                                  "hoodId": hoodId,
                                  "zoneId": zoneId,
                                  "shardId": None,
                                  "tunnelOrigin": tunnelOriginPlaceHolder,
                                  "tutorial": tutorialFlag,
                                  }]
                                )
        return tunnelOriginList

    def extractGroupName(self, groupFullName):
        assert(self.notify.debug("extractGroupName()"))
        # The Idea here is that group names may have extra flags associated
        # with them that tell more information about what is special about
        # the particular vis zone. A normal vis zone might just be "13001",
        # but a special one might be "14356:safe_zone" or
        # "345:safe_zone:exit_zone"... These are hypotheticals. The main
        # idea is that there are colon separated flags after the initial
        # zone name.
        return(string.split(groupFullName, ":", 1)[0])

    def makeLinkTunnelName(self, hoodId, currentZone):
        assert(self.notify.debug("makeLinkTunnelName() %s" %
                                 ("**/toph_" + self.getNameFromId(hoodId) + "_" + str(currentZone))  ))
        # Returns the name that the current tunnel reference frame
        # will have on the other side.
        return ("**/toph_" + self.getNameFromId(hoodId) + "_" + str(currentZone))
