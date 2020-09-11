from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import FishGlobals
from toontown.fishing import DistributedPondBingoManager
from pandac.PandaModules import Vec3
from direct.task import Task

class DistributedFishingPond(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingPond")

    pollInterval = 0.5
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.notify.debug("init")
        self.targets = {}
        self.area = None
        self.localToonBobPos = None
        self.localToonSpot = None
        self.pondBingoMgr = None

        # This is necessary because we must restore the castGui bucket
        # and jar to their proper positions once Bingo Night ends.
        # We must know each spot that the localToon visited at the pond.
        self.visitedSpots = {}

    def disable(self):
        self.visitedSpots.clear()
        self.stopCheckingTargets()        
        DistributedObject.DistributedObject.disable(self)

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area

    def addTarget(self, target):
        self.notify.debug("addTarget: %s" % (target))
        self.targets[target.getDoId()] = target

    def removeTarget(self, target):
        self.notify.debug("removeTarget: %s" % (target))
        del self.targets[target.getDoId()]

    def startCheckingTargets(self, spot, bobPos):
        self.notify.debug("startCheckingTargets")
        
        if base.wantBingo:
            assert( spot.getDoId() == self.localToonSpot.getDoId() )

        self.localToonSpot = spot
        self.localToonBobPos = bobPos
        # Slight delay before checking for the first time
        taskMgr.doMethodLater(self.pollInterval * 2,
                              self.checkTargets,
                              self.taskName("checkTargets"))

    def stopCheckingTargets(self):
        self.notify.debug("stopCheckingTargets")
        
        taskMgr.remove(self.taskName("checkTargets"))
        if not base.wantBingo:
            # We don't want this to happen when fish bingo is enabled.
            self.localToonSpot = None
        self.localToonBobPos = None

    def checkTargets(self, task=None):
        """
        Do a distance check against all the targets in the pond.
        If we hit one of the targets, send an update to the AI and return 1
        Otherwise just return 0
        """
        self.notify.debug("checkTargets")
        if self.localToonSpot != None:
            for target in self.targets.values():
                targetPos = target.getPos(render)
                distVec = Vec3(targetPos - self.localToonBobPos)
                dist = distVec.length()
                if dist < target.getRadius():
                    self.notify.debug("checkTargets: hit target: %s" % (target.getDoId()))
                    self.d_hitTarget(target)
                    return Task.done
            # Check again later
            taskMgr.doMethodLater(self.pollInterval,
                                  self.checkTargets,
                                  self.taskName("checkTargets"))
        else:
            # Not sure why this is happening.
            self.notify.warning('localToonSpot became None while checking targets')
        return Task.done

    def d_hitTarget(self, target):
        self.localToonSpot.hitTarget()
        self.sendUpdate("hitTarget", [target.getDoId()])

    ############################################################
    # Method: setPondBingoManager
    # Purpose: This method sets the reference to a
    #          PondBingoManager instance.
    # Input: pondBingoMgr - The pondBingoManager object that is
    #                       associated with the pond instance.
    # Output: None
    ############################################################
    def setPondBingoManager(self, pondBingoMgr):
        self.pondBingoMgr = pondBingoMgr

    ############################################################
    # Method: removePondBingoManager
    # Purpose: This method deletes the reference to the PBMgrAI
    #          for this pond. This is called whenever Bingo
    #          Night closes and the PBMgrAI is ending.
    #          
    # Input: None
    # Output: None
    ############################################################
    def removePondBingoManager(self):
        del self.pondBingoMgr
        self.pondBingoMgr = None

    ############################################################
    # Method: getPondBingoManager
    # Purpose: This method returns the reference to a
    #          PondBingoManager instance.
    # Input: None
    # Output: pondBingoMgr - The pondBingoManager object that is
    #                        associated with the pond instance.
    ############################################################
    def getPondBingoManager(self):
        return self.pondBingoMgr

    ############################################################
    # Method:  hasPondBingoManager
    # Purpose: This method determines if the pond has a PBMgr
    #          and returns the result.
    # Input: None
    # Output: result 1 if there is a PBMgr or 0
    ############################################################
    def hasPondBingoManager(self):
        return ((self.pondBingoMgr) and [1] or [0])[0]

    ############################################################
    # Method: handleBingoCatch
    # Purpose: This method sets the last catch of the
    #          BingoManager to the last fish caught by the
    #          client.
    # Input: catch - Last Fish caught by the client.
    # Output: None
    ############################################################
    def handleBingoCatch(self, catch):
        if self.pondBingoMgr:
            self.pondBingoMgr.setLastCatch(catch)

    ############################################################
    # Method: handleBingoBoot
    # Purpose: This method calls the handleBoot method of the
    #          BingoManager because the client caught a boot.
    # Input: None
    # Output: None
    ############################################################
    def handleBingoBoot(self):
        if self.pondBingoMgr:
            self.pondBingoMgr.handleBoot()

    ############################################################
    # Method: cleanupBingoMgr
    # Purpose: This method tells the BingoManager to cleanup
    #          because the corresponding client has left the
    #          FishingSpot.
    # Input: None
    # Output: None
    ############################################################
    def cleanupBingoMgr(self):
        if self.pondBingoMgr:
            self.pondBingoMgr.cleanup()

    ############################################################
    # Method: setLocalToonSpot
    # Purpose: This method sets the fishing spot for which the
    #          the local avatar has entered.
    # Note:    Initially, this was set only when the pond
    #          needed to check for targets during the 'fishing'
    #          state 
    # Input: None
    # Output: None
    ############################################################
    def setLocalToonSpot(self, spot=None):
        self.localToonSpot = spot

        if (spot is not None) and (not self.visitedSpots.has_key(spot.getDoId())):
            self.visitedSpots[spot.getDoId()] = spot            
            
    ############################################################
    # Method: showBingoGui
    # Purpose: This method  tells the PondBingoManager to 
    #          display the Bingo GUI.
    # Input: None
    # Output: None
    ############################################################
    def showBingoGui(self):
        if self.pondBingoMgr:
            self.pondBingoMgr.showCard()

    ############################################################
    # Method: getLocalToonSpot
    # Purpose: This method returns the current localToonSpot.
    # Input: None
    # Output: localToonSpot - Fishing Spot where the local
    #                         toon of the avatar is found.
    ############################################################
    def getLocalToonSpot(self):
        return self.localToonSpot

    ############################################################
    # Method: resetSpotGui
    # Purpose: This method resets the CastGui (Bucket and Jar)
    #          for each pond that the localtoon visited during
    #          Bingo Night. During Bingo Night, the bucket and
    #          jar are moved to the far left of the screen. This
    #          resets their normal positions for normal fishing.
    # Input: None
    # Output: None
    ############################################################
    def resetSpotGui(self):
        for spot in self.visitedSpots.values():
            spot.resetCastGui()

    ############################################################
    # Method: setSpotGui
    # Purpose: This method sets the spot Cast Gui for Bingo
    #          night. This is called whenever a toon is already
    #          fishing and bingo night starts. This tells the
    #          spot to play a sequence to move the bucket and
    #          jar to the far left on the screen.
    # Input: None
    # Output: None
    ############################################################
    def setSpotGui(self):
        for spot in self.visitedSpots.values():
            spot.setCastGui()
    

    
            


    
        
