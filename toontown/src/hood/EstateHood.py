
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.distributed.ToontownMsgTypes import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.minigame import Purchase
from otp.avatar import DistributedAvatar
import SkyUtil
from direct.task.Task import Task
import Hood
from toontown.estate import EstateLoader
from toontown.estate import HouseGlobals
import ZoneUtil

class EstateHood(Hood.Hood):
    """
    The base class for toon neighborhoods
    Every neighborhood should have a *Hood subclass to implement
    neighborhood specific things like fog

    To subclass from hood, you need to define a Town, a SafeZone, a storage
    DNA file, a sky model file, and an id.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("EstateHood")

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        assert(self.notify.debug("__init__(parentFSM="+str(parentFSM)
                +", doneEvent="+str(doneEvent)
                +", dnaStore="+str(dnaStore)+")"))
        Hood.Hood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)

        self.fsm = ClassicFSM.ClassicFSM('Hood',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['safeZoneLoader']),
                            State.State('safeZoneLoader',
                                        self.enterSafeZoneLoader,
                                        self.exitSafeZoneLoader,
                                        ['quietZone',
                                         ]),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['safeZoneLoader',
                                         ]),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        [])
                            ],
                           'start',
                           'final',
                           )

        self.fsm.enterInitialState()
        self.id = MyEstate
        # Create the safe zone state data
        self.safeZoneLoaderClass = EstateLoader.EstateLoader
        self.storageDNAFile = "phase_5.5/dna/storage_estate.dna"
        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {WINTER_DECORATIONS : ['phase_5.5/dna/winter_storage_estate.dna'],
                                       HALLOWEEN_PROPS : ['phase_5.5/dna/halloween_props_storage_estate.dna']}
                                       
        self.skyFile = "phase_3.5/models/props/TT_sky"
        self.spookySkyFile = "phase_3.5/models/props/BR_sky"
        
        self.popupInfo = None
        
    def load(self):
        assert(self.notify.debug("load()"))
        Hood.Hood.load(self)

    def unload(self):
        """
        unload the hood models and dna storage
        """
        del self.safeZoneLoaderClass
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        Hood.Hood.unload(self)

    def enter(self, requestStatus):
        """
        enter this hood and start the state machine
        -- don't call Hood.enter until we can implement the titleText for estates
        """
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        # accept messages from the AI saying we have been kicked out
        self.accept("kickToPlayground", self.kickToPlayground)
        self.fsm.request(requestStatus["loader"], [requestStatus])

    def exit(self):
        assert(self.notify.debug("exit()"))
        if self.loader:
            self.loader.exit()
            self.loader.unload()
            del self.loader
        Hood.Hood.exit(self)
        
    # SafeZoneLoader state

    # Defined in Hood.py

    # final state

    # Defined in Hood.py

    # quietZone state

    # Defined in Hood.py

    def loadLoader(self, requestStatus):
        assert(self.notify.debug("loadLoader(requestStatus="
                                 +str(requestStatus)+")"))
        loaderName = requestStatus["loader"]
        #if loaderName=="estateLoader":
        if loaderName=="safeZoneLoader":
            self.loader = self.safeZoneLoaderClass(self, 
                    self.fsm.getStateNamed("safeZoneLoader"), 
                    self.loaderDoneEvent)
            self.loader.load()
        else:
            assert(self.notify.debug("  unknown loaderName: "+str(loaderName)))

    # Don't show title text when going to the estate
    # (This is TBD. We have to do some special case stuff for
    #  "Your Estate" vs. "Fat Tooter's Estate" etc.)
    def spawnTitleText(self, zoneId):
        return

    def hideTitleTextTask(self, task):
        return Task.done

    # Handle being kicked back to the playground when Estate owner exits
    def kickToPlayground(self, retCode):
        if retCode == 0:
            # we are just being warned
            msg = TTLocalizer.EstateOwnerLeftMessage % HouseGlobals.BOOT_GRACE_PERIOD
            self.__popupKickoutMessage(msg)
        elif retCode == 1:
            # our timer has run out, go back to playground
            zoneId = base.localAvatar.lastHood
            self.doneStatus = {
                "loader": ZoneUtil.getBranchLoaderName(zoneId),
                "where": ZoneUtil.getToonWhereName(zoneId),
                "how" : "teleportIn",
                "hoodId" : zoneId,
                "zoneId" : zoneId,
                "shardId" : None,
                "avId" : -1,
                }
            messenger.send(self.doneEvent)
            
        elif retCode == 2:
            # we have been booted from the estate.  this only
            # happens if we have been de-friended by the owner,
            # in the future, we could give the owners a way to
            # boot people without de-friending them

            zoneId = base.localAvatar.lastHood
            self.doneStatus = {
                "loader": ZoneUtil.getBranchLoaderName(zoneId),
                "where": ZoneUtil.getToonWhereName(zoneId),
                "how" : "teleportIn",
                "hoodId" : zoneId,
                "zoneId" : zoneId,
                "shardId" : None,
                "avId" : -1,
                }
            messenger.send(self.doneEvent)
        else:
            self.notify.error("unknown reason for exiting estate")

    def __popupKickoutMessage(self, msg):
        # Popup warning that we are being kicked out of the estate
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr'))

        self.popupInfo = DirectFrame(
            parent = hidden,
            relief = None,
            state = 'normal',
            text =  msg,
            frameSize = (-1,1,-1,1),
            text_wordwrap = 10,
            geom = DGG.getDefaultDialogGeom(),
            geom_color = GlobalDialogColor,
            geom_scale = (.88, 1, .75),
            geom_pos = (0,0,-.08),
            text_scale = TTLocalizer.EHpopupInfo,
            text_pos = (0, 0.1),
            )
        DirectButton(self.popupInfo,
                     image = okButtonImage,
                     relief = None,
                     text = TTLocalizer.EstatePopupOK,
                     text_scale = 0.05,
                     text_pos = (0.0, -0.1),
                     textMayChange = 0,
                     pos = (0.0, 0.0, -0.30),
                     command = self.__handleKickoutOk)
        buttons.removeNode()
        
        # Show the popup info (i.e. "Sorry, the owner has left...")
        self.popupInfo.reparentTo(aspect2d)
        
    def __handleKickoutOk(self):
        # hide the popup
        self.popupInfo.reparentTo(hidden)


    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        
        # we have the wrong sky; load in the regular sky
        if not (self.sky.getTag("sky") == "Regular"):
            self.endSpookySky()
            
        SkyUtil.startCloudSky(self)
        if base.cloudPlatformsEnabled:
            self.loader.startCloudPlatforms()
        
    def stopSky(self):
        assert(self.notify.debug("stopSky"))
        Hood.Hood.stopSky(self)
        self.loader.stopCloudPlatforms()
        
    def startSpookySky(self):
        if hasattr(self, "loader") and self.loader \
        and hasattr(self.loader, "cloudTrack") and self.loader.cloudTrack:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag("sky", "Halloween")
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5,0.5,0.5,1)
        self.sky.setBin("background", 100)
        self.sky.setFogOff()
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