from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.task.Task import Task

from pandac.PandaModules import *

from otp.avatar import DistributedAvatar
from toontown.toon import GMUtils

from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.distributed.ToontownMsgTypes import *
from toontown.minigame import Purchase

from toontown.parties import PartyLoader
from toontown.parties import PartyGlobals

from toontown.hood import SkyUtil
from toontown.hood import Hood
from toontown.hood import ZoneUtil

class PartyHood(Hood.Hood):
    """
    This was originally copied from EstateHood.py
    
    This is a subclass from hood, you need to define a Town, a SafeZone, a storage
    DNA file, a sky model file, and an id.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("PartyHood")

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
        self.id = PartyHood
        # Create the safe zone state data
        self.safeZoneLoaderClass = PartyLoader.PartyLoader
        
        self.partyActivityDoneEvent = "partyActivityDone"
        
        self.storageDNAFile = "phase_13/dna/storage_party_sz.dna"
        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {WINTER_DECORATIONS : ['phase_5.5/dna/winter_storage_estate.dna']}
        self.skyFile = "phase_3.5/models/props/TT_sky"
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
        self.accept(PartyGlobals.KICK_TO_PLAYGROUND_EVENT, self.kickToPlayground)
        self.fsm.request(requestStatus["loader"], [requestStatus])

    def exit(self):
        assert(self.notify.debug("exit()"))
        if self.loader:
            self.loader.exit()
            self.loader.unload()
            del self.loader
        Hood.Hood.exit(self)


    # Handle being kicked back to the playground when the party ends
    def kickToPlayground(self, retCode):
        if retCode == 0:
            # we are just being warned
            msg = TTLocalizer.PartyOverWarningNoName
            if hasattr(base, 'distributedParty') and base.distributedParty:
                name = base.distributedParty.hostName
                msg = TTLocalizer.PartyOverWarningWithName % TTLocalizer.GetPossesive(name)
            self.__popupKickoutMessage(msg)
            base.localAvatar.setTeleportAvailable(0)
        if retCode == 1:
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

    def __popupKickoutMessage(self, msg):
        # Popup warning that we are being kicked out of the party
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
            text_scale = .08,
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

    def handlePartyActivityDone(self):
        """
        Ok, activitys are over
        """
        return None

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
        # This functionality is moved to DistributedParty.spawnTitleText()
        # we need host name which we don't have here        
        return

    def hideTitleTextTask(self, task):
        # This functionality is moved to DistributedParty.spawnTitleText()
        # we need host name which we don't have here        
        return

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)
        if base.cloudPlatformsEnabled:
            self.loader.startCloudPlatforms()
        
    def stopSky(self):
        assert(self.notify.debug("stopSky"))
        Hood.Hood.stopSky(self)
        self.loader.stopCloudPlatforms()
        
