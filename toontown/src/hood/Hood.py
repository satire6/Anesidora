
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.distributed.ToontownMsgTypes import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.task.Task import Task
from toontown.minigame import Purchase
from direct.gui import OnscreenText
from otp.avatar import DistributedAvatar
from toontown.building import SuitInterior
import QuietZoneState
import ZoneUtil
from toontown.toonbase import TTLocalizer

class Hood(StateData.StateData):
    """
    The base class for the Hood State Data
    Every neighborhood should have a Hood subclass to implement
    neighborhood specific things like fog

    To subclass from hood, you need to define a Town, a SafeZone, a storage
    DNA file, and an id.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("Hood")

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        assert(self.notify.debug("__init__(parentFSM="+str(parentFSM)
                +", doneEvent="+str(doneEvent)
                +", dnaStore="+str(dnaStore)+")"))
        StateData.StateData.__init__(self, doneEvent)

        self.parentFSM = parentFSM
        self.dnaStore = dnaStore
        
        # The event for safe zone loader or town loader done
        self.loaderDoneEvent = "loaderDone"

        # The canonical id of the current hood.  This will be filled
        # in by the derived class.  This is always the same for a
        # particular kind of hood.
        self.id = None

        # The actual zoneId in which this particular hood's safezone
        # can be found, if this makes sense.  This is normally the
        # same as the above, but it may differ when we are in
        # WelcomeValley.
        self.hoodId = hoodId

        self.titleText = None
        # Title color should be overridden in base class
        self.titleColor = (1,1,1,1)

        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Updated in each of the neighborhood specific Hood files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {}
        
        #For the holiday sky
        self.spookySkyFile = None
        self.halloweenLights = []

    def enter(self, requestStatus):
        """
        enter this hood and start the state machine
        """
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]

        hoodText = self.getHoodText(zoneId)

        self.titleText = OnscreenText.OnscreenText(
            hoodText,
            fg = self.titleColor,
            font = getSignFont(),
            pos = (0,-0.5),
            scale = TTLocalizer.HDenterTitleTextScale,
            drawOrder = 0,
            mayChange = 1,
            )
        
        self.fsm.request(requestStatus["loader"], [requestStatus])

    def getHoodText(self, zoneId):
        hoodText = base.cr.hoodMgr.getFullnameFromId(self.id)

        # If we are in the safezone, but not the Tutorial, add
        # Playground under the hood name
        if (self.id != Tutorial):
            streetName = StreetNames.get(ZoneUtil.getCanonicalBranchZone(zoneId))
            if streetName:
                hoodText = hoodText + "\n" + streetName[-1]

        return hoodText
        
    def spawnTitleText(self, zoneId):
        hoodText = self.getHoodText(zoneId)
        self.doSpawnTitleText(hoodText)

    def doSpawnTitleText(self, text):
        self.titleText.setText(text)
        self.titleText.show()
        self.titleText.setColor(Vec4(*self.titleColor))
        self.titleText.clearColorScale()
        self.titleText.setFg(self.titleColor)
        seq = Task.sequence(
            # HACK! Let a pause go by to cover the loading pause
            # This tricks the taskMgr
            Task.pause(0.1),
            Task.pause(6.0),
            self.titleText.lerpColorScale(
            Vec4(1.0, 1.0, 1.0, 1.0),
            Vec4(1.0, 1.0, 1.0, 0.0),
            0.5),
            Task(self.hideTitleTextTask))
        taskMgr.add(seq, "titleText")

    def hideTitleTextTask(self, task):
        assert(self.notify.debug("hideTitleTextTask()"))
        self.titleText.hide()
        return Task.done

    def hideTitleText(self):
        """
        This gets called from the town and safe zone to cleanup
        the title text if we leave walk mode for instance
        """
        assert(self.notify.debug("hideTitleText()"))
        if self.titleText:
            self.titleText.hide()

    def exit(self):
        """
        exit this hood
        """
        assert(self.notify.debug("exit()"))
        taskMgr.remove("titleText")
        if self.titleText:
            self.titleText.cleanup()
            self.titleText = None
        base.localAvatar.stopChat()

    def load(self):
        """
        load the hood models and dna storage
        """
        assert(self.notify.debug("load()"))
        # Load the neighborhood specific models and textures
        if self.storageDNAFile:
            loader.loadDNAFile(self.dnaStore, self.storageDNAFile)
        # Overwrite dna storage with holiday specific models
        # We might not have a newsManager if we are running in the dev
        # environment without an AI server.
        newsManager = base.cr.newsManager
        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            for holiday in holidayIds:
                for storageFile in self.holidayStorageDNADict.get(
                    holiday,[]):
                    loader.loadDNAFile(self.dnaStore, storageFile)
            if (ToontownGlobals.HALLOWEEN_COSTUMES not in holidayIds) or (not self.spookySkyFile):
                # Load the sky model so we will have it in memory for the entire hood
                self.sky = loader.loadModel(self.skyFile)
                self.sky.setTag("sky","Regular")
                self.sky.setScale(1.0)
                self.sky.setFogOff()
            else:
                self.sky = loader.loadModel(self.spookySkyFile)
                self.sky.setTag("sky","Halloween")
        if not newsManager:
            # Load the sky model so we will have it in memory for the entire hood
            self.sky = loader.loadModel(self.skyFile)
            self.sky.setTag("sky","Regular")
            self.sky.setScale(1.0)
            # Normally, fog is turned off for the sky.  This will prevent
            # the sky from being contaminated by the trolley tunnel shadow
            # if we jump on the trolley.  Hoods like DD that require fog
            # will specifically turn fog on for the sky.
            self.sky.setFogOff()

    def unload(self):
        """
        unload the hood models and dna storage
        """
        assert(self.notify.debug("unload()"))

        # The loader should have been cleaned up by the appropriate
        # exitTownLoader or exitSafezoneLoader state transition, but
        # because we actually load these before we enter those states,
        # it's possible we never even got there, so it might still be
        # hanging around.  If so, clean it up now.
        if hasattr(self, "loader"):
            self.notify.info("Aggressively cleaning up loader: %s" % (self.loader))
            self.loader.exit()
            self.loader.unload()
            del self.loader

        del self.fsm
        del self.parentFSM
            
        # Remove all references to the neighborhood models and textures
        self.dnaStore.resetHood()
        del self.dnaStore
            
        # I'm leaving the world, disable all items but localtoon in the
        # doId2do and doId2cdc
        #base.cr.disableAllButLocalToon()
        self.sky.removeNode()
        del self.sky
        
        self.ignoreAll()
        # Get rid of any references to the models or textures from this hood
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def enterStart(self):
        assert(self.notify.debug("enterStart()"))

    def exitStart(self):
        assert(self.notify.debug("exitStart()"))
    
    # Done Status #
    
    def isSameHood(self, status):
        """return true if the request status is in the same hood"""
        return status["hoodId"] == self.hoodId and \
               status["shardId"] == None

    # final state

    def enterFinal(self):
        """enterFinal(self)
        """
        assert(self.notify.debug("enterFinal()"))

    def exitFinal(self):
        """exitFinal(self)
        """
        assert(self.notify.debug("exitFinal()"))

    # quietZone state

    def enterQuietZone(self, requestStatus):
        assert(self.notify.debug("enterQuietZone(requestStatus = %s)" % (requestStatus)))
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.acceptOnce("enterWaitForSetZoneResponse", self.handleWaitForSetZoneResponse)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
                self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        assert(self.notify.debug("exitQuietZone()"))
        self.ignore(self.quietZoneDoneEvent)
        self.ignore("enterWaitForSetZoneResponse")
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def loadLoader(self, requestStatus):
        # Pure virtual : overriden by subclass
        pass

    def handleWaitForSetZoneResponse(self, requestStatus):
        assert(self.notify.debug("handleWaitForSetZoneResponse(requestStatus="
                +str(requestStatus)+")"))
        loaderName = requestStatus["loader"]
        if loaderName=="safeZoneLoader":
            if not loader.inBulkBlock:
                loader.beginBulkLoad("hood", TTLocalizer.HeadingToPlayground,
                                     safeZoneCountMap[self.id], 1, TTLocalizer.TIP_GENERAL)
            self.loadLoader(requestStatus)
            loader.endBulkLoad("hood")
        #elif loaderName=="suitInterior":
            # TODO: loading bar
        #    self.loadLoader(requestStatus)
        elif loaderName=="townLoader":
            if not loader.inBulkBlock:
                zoneId = requestStatus["zoneId"]
                toPhrase = StreetNames[ZoneUtil.getCanonicalBranchZone(zoneId)][0]
                streetName = StreetNames[ZoneUtil.getCanonicalBranchZone(zoneId)][-1]
                loader.beginBulkLoad("hood", (TTLocalizer.HeadingToStreet % {'to':toPhrase, 'street':streetName}),
                                     townCountMap[self.id], 1, TTLocalizer.TIP_STREET)
            self.loadLoader(requestStatus)
            loader.endBulkLoad("hood")
        elif loaderName=="minigame":
            pass
        elif loaderName=="cogHQLoader":
            print "should be loading HQ"
        else:
            assert(self.notify.debug("  unknown loaderName="+loaderName))

    def handleQuietZoneDone(self):
        assert(self.notify.debug("handleQuietZoneDone()"))
        status=self.quietZoneStateData.getRequestStatus()
        self.fsm.request(status["loader"], [status])

    # SafeZoneLoader state

    def enterSafeZoneLoader(self, requestStatus):
        """enterSafeZoneLoader(self)
        """
        assert(self.notify.debug("enterSafeZoneLoader()"))
        # By now the subclass should have defined a sz
        self.accept(self.loaderDoneEvent, self.handleSafeZoneLoaderDone)
        self.loader.enter(requestStatus)
        self.spawnTitleText(requestStatus['zoneId'])

    def exitSafeZoneLoader(self):
        """exitSafeZoneLoader(self)
        """
        assert(self.notify.debug("exitSafeZoneLoader()"))
        taskMgr.remove("titleText")
        self.hideTitleText()
        self.ignore(self.loaderDoneEvent)
        self.loader.exit()
        self.loader.unload()
        del self.loader

    def handleSafeZoneLoaderDone(self):
        assert(self.notify.debug("handleSafeZoneLoaderDone()"))
        doneStatus = self.loader.getDoneStatus()
        if (self.isSameHood(doneStatus) and doneStatus["where"] != "party") or doneStatus["loader"]=="minigame":
            self.fsm.request("quietZone", [doneStatus])
        else:
            # ...we're leaving the hood.
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    def startSky(self):
        # Parent the sky to our camera, the task will counter rotate it
        self.sky.reparentTo(camera)
        # Nowadays we use a CompassEffect to counter-rotate the sky
        # automatically at render time, rather than depending on a
        # task to do this just before the scene is rendered.
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        # Since we are using a CompassEffect, we don't have to spawn a
        # task.  Some hoods may spawn a task anyway, to do some
        # additional work (like rotating clouds).

    def stopSky(self):
        # Remove the sky task just in case it was spawned.
        taskMgr.remove("skyTrack")
        self.sky.reparentTo(hidden)
        
    def startSpookySky(self):
        if not self.spookySkyFile:
            return
        if hasattr(self, "sky") and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag("sky","Halloween")
        self.sky.setColor(0.5,0.5,0.5,1)
        self.sky.reparentTo(camera)
        
        #fade the sky in
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval( 1.5, Vec4(1, 1, 1, 1),
                                               startColorScale = Vec4(1, 1, 1, 0.25),
                                               blendType = 'easeInOut')
        fadeIn.start()

        # Nowadays we use a CompassEffect to counter-rotate the sky
        # automatically at render time, rather than depending on a
        # task to do this just before the scene is rendered.
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

    def endSpookySky(self):
        if hasattr(self, "sky") and self.sky:
            self.sky.reparentTo(hidden)
        if hasattr(self, "sky"):
            self.sky = loader.loadModel(self.skyFile)
            self.sky.setTag("sky","Regular")
            self.sky.setScale(1.0)
            self.startSky()
