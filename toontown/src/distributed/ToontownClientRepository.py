import types
import time


from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import ivalMgr
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.PythonUtil import Functor, ScratchPad
from direct.showbase.InputStateGlobal import inputState

from otp.avatar import Avatar
from otp.avatar import DistributedAvatar
from otp.friends import FriendManager
from otp.login import TTAccount
from otp.login import AccountServerConstants
from otp.login import LoginScreen
from otp.login import LoginGSAccount
from otp.login import LoginGoAccount
from otp.login import LoginWebPlayTokenAccount
from otp.login import LoginTTAccount
from otp.login import HTTPUtil
from otp.distributed import OTPClientRepository
from otp.distributed import PotentialAvatar
from otp.distributed import PotentialShard
from otp.distributed import DistributedDistrict
from otp.distributed.OtpDoGlobals import *
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPLauncherGlobals


from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.launcher.DownloadForceAcknowledge import *
from toontown.distributed import DelayDelete
from toontown.friends import FriendHandle
from toontown.friends import FriendsListPanel
from toontown.friends import ToontownFriendSecret
from toontown.uberdog import TTSpeedchatRelay
from toontown.login import DateObject
from toontown.login import AccountServerDate
from toontown.login import AvatarChooser
from toontown.makeatoon import MakeAToon
from toontown.pets import DistributedPet, PetDetail, PetHandle
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toon import LocalToon
from toontown.toon import ToonDNA
from toontown.distributed import ToontownDistrictStats
# import to run module-level tests
from toontown.makeatoon import TTPickANamePattern
from toontown.parties import ToontownTimeManager
from toontown.toon import Toon, DistributedToon
from ToontownMsgTypes import *
import HoodMgr
import PlayGame
from toontown.toontowngui import ToontownLoadingBlocker



class ToontownClientRepository(OTPClientRepository.OTPClientRepository):
    """ToontownClientRepository class: handle distribution for client"""

    SupportTutorial = 1
    GameGlobalsId = OTP_DO_ID_TOONTOWN

    # this is what the TCR listens for
    SetZoneDoneEvent = 'TCRSetZoneDone'
    # this is what the rest of Toontown listens for
    # (see getNextSetZoneDoneEvent())
    EmuSetZoneDoneEvent = 'TCREmuSetZoneDone'

    SetInterest = 'Set'
    ClearInterest = 'Clear'

    ClearInterestDoneEvent = 'TCRClearInterestDone'

    KeepSubShardObjects = False
    
    def __init__(self, serverVersion, launcher=None):
        # Ancestor init
        OTPClientRepository.OTPClientRepository.__init__(
            self, serverVersion, launcher, playGame = PlayGame.PlayGame)

        self._playerAvDclass = self.dclassesByName['DistributedToon']

        # Set Interface Font to be Toontown's Font
        setInterfaceFont(TTLocalizer.InterfaceFont)
        setSignFont(TTLocalizer.SignFont)
        setFancyFont(TTLocalizer.FancyFont)
        nameTagFontIndex = 0
        for font in TTLocalizer.NametagFonts:
            setNametagFont(nameTagFontIndex, TTLocalizer.NametagFonts[nameTagFontIndex])
            nameTagFontIndex += 1

        self.toons = {}
        
        # We won't bother to check expiration dates when validating
        # SSL certificates.  Users have a funny tendency to leave the
        # dates on their computers out of whack by several years, so
        # insisting on a valid date can make the SSL connections fail
        # mysteriously, and we don't really care about the possible
        # security hazard of accepting expired certificates.
        if self.http.getVerifySsl() != HTTPClient.VSNoVerify:
            self.http.setVerifySsl(HTTPClient.VSNoDateCheck)

        # Set the client private and public certificate pair on the
        # HTTPClient object for presenting to the gameserver.  This is
        # a particularly sensitive private key: if (when) a hacker
        # successfully extracts it from the Toontown executable, he
        # will be able to negotiate a man-in-the-middle decoding of
        # the Toontown game stream, by creating a proxy that poses as
        # the game client.  He will also be able to create a denial of
        # service attack on the game server by creating a bunch of SSL
        # connections that fill the game server up with nonsense
        # requests.

        # We have to have the private key somewhere in the executable;
        # we have done our best to bury it to make it difficult to
        # find.  The function we are calling here, prepareAvatar(), is
        # deliberately misnamed; it should be called
        # loadClientCertificate().  See the comments in
        # loadClientCertificate.h.
        prepareAvatar(self.http)

        # This flag is normally zero to allow cheesy rendering
        # effects; call forbidCheesyEffects() to increment it and
        # disallow them in a particular context (e.g. in a minigame).
        self.__forbidCheesyEffects = 0

        # Set up a slot for the various object managers that exist in
        # each shard.  These will fill themselves in when they get
        # created.
        self.friendManager = None
        self.speedchatRelay = None
        self.trophyManager = None
        self.bankManager = None
        self.catalogManager = None
        self.welcomeValleyManager = None
        self.newsManager = None
        self.distributedDistrict = None
        self.partyManager = None
        self.inGameNewsMgr = None
        self.toontownTimeManager = ToontownTimeManager.ToontownTimeManager()

        self.avatarFriendsManager = self.generateGlobalObject(
            OtpDoGlobals.OTP_DO_ID_AVATAR_FRIENDS_MANAGER,
            "AvatarFriendsManager")

        self.playerFriendsManager = self.generateGlobalObject(
            OtpDoGlobals.OTP_DO_ID_PLAYER_FRIENDS_MANAGER,
            "TTPlayerFriendsManager")
            
        self.speedchatRelay = self.generateGlobalObject(
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_SPEEDCHAT_RELAY,
            "TTSpeedchatRelay")
        
        self.deliveryManager = self.generateGlobalObject(
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER,
            "DistributedDeliveryManager") 
        
        #self.partyManager = self.generateGlobalObject(
        #    OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
        #    "DistributedPartyManager")               

        #self.inGameNewsManager = self.generateGlobalObject(
        #    OtpDoGlobals.OTP_DO_ID_TOONTOWN_IN_GAME_NEWS_MANAGER,
        #    "InGameNewsMgr") 

        if config.GetBool('want-code-redemption', 1):
            self.codeRedemptionManager = self.generateGlobalObject(
                OtpDoGlobals.OTP_DO_ID_TOONTOWN_CODE_REDEMPTION_MANAGER,
                "TTCodeRedemptionMgr") 
        
        # This one is a little different, because it doesn't live in
        # the Uber zone; a different one lives in the zone for each
        # house.  But still it is similar.
        self.furnitureManager = None

        # We will store a houseDesign.ObjectManager here later, if we
        # ever go inside a house.
        self.objectManager = None

        # We'll use a map to track all of the friends on our friends
        # list, and another one to track our friends who are online
        # right now.  These are maps of doId to FriendHandle.
        self.friendsMap = {}
        self.friendsOnline = {}
        self.friendsMapPending = 0
        self.friendsListError = 0

        # We can get the friend online message before the friend list message
        # here's a hack to store it, key is avId, value is
        # (commonChatFlags, whitelistChatFlags)
        self.friendPendingChatSettings = {}

        # Create a map to track progress of elder quests that require
        # a Toon to make friends
        self.elderFriendsMap = {}

        self.__queryAvatarMap = {}

        # this might be replaced by the AccountServerDate object
        # use this object to get current-date information
        self.dateObject = DateObject.DateObject()

        self.accountServerDate = AccountServerDate.AccountServerDate()

        # The music will get passed in from ToontownStart
        self.hoodMgr = HoodMgr.HoodMgr(self)
        
        self.setZonesEmulated = 0
        # this is used to emulate the old setzone behavior
        # with set location and set interest
        self.old_setzone_interest_handle = None
        # to ensure that we get every interest-done event, we'll serialize
        # the setZone requests and queue up requests that aren't ready to
        # go out yet.
        self.setZoneQueue = Queue()
        # listen for set-zone completes
        self.accept(ToontownClientRepository.SetZoneDoneEvent,
                    self._handleEmuSetZoneDone)

        # keep track of the objects that we've manually deleted
        self._deletedSubShardDoIds = set()
        
        # stores name information about any toon we've seen
        self.toonNameDict ={}

        self.gameFSM.addState( State.State('skipTutorialRequest',
                                       self.enterSkipTutorialRequest,
                                       self.exitSkipTutorialRequest,
                                       ['playGame', 'gameOff', 'tutorialQuestion']))
        state = self.gameFSM.getStateNamed('waitOnEnterResponses')
        state.addTransition('skipTutorialRequest')
        state = self.gameFSM.getStateNamed('playGame')
        state.addTransition('skipTutorialRequest')

        self.wantCogdominiums = base.config.GetBool('want-cogdominiums', 0)

        if base.config.GetBool('tt-node-check', 0):
            # check for nodes in the models
            for species in ToonDNA.toonSpeciesTypes:
                for head in ToonDNA.getHeadList(species):
                    for torso in ToonDNA.toonTorsoTypes:
                        for legs in ToonDNA.toonLegTypes:
                            for gender in ('m', 'f'):
                                print 'species: %s, head: %s, torso: %s, legs: %s, gender: %s' % (
                                    species, head, torso, legs, gender)
                                dna = ToonDNA.ToonDNA()
                                dna.newToon((head, torso, legs, gender, ))
                                toon = Toon.Toon()
                                try:
                                    toon.setDNA(dna)
                                except Exception, e:
                                    print e
        
    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    def congratulations(self, avatarChoice):
        self.acceptedScreen = loader.loadModel(
            "phase_3/models/gui/toon_council")
        self.acceptedScreen.setScale(0.667)
        self.acceptedScreen.reparentTo(aspect2d)
        buttons = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        self.acceptedBanner = DirectLabel(parent = self.acceptedScreen,
                                          relief = None,
                                          text = OTPLocalizer.CRNameCongratulations,
                                          text_scale = 0.18,
                                          text_fg = Vec4(0.6, 0.1, 0.1, 1),
                                          text_pos = (0, 0.05),
                                          text_font = getMinnieFont(),
                                          )
        newName = avatarChoice.approvedName
        self.acceptedText = DirectLabel(parent = self.acceptedScreen,
                                        relief = None,
                                        text = OTPLocalizer.CRNameAccepted % newName,
                                        text_scale = 0.125,
                                        text_fg = Vec4(0, 0, 0, 1),
                                        text_pos = (0, -0.15),
                                        )
        self.okButton = DirectButton(parent = self.acceptedScreen,
                                     image = (buttons.find('**/ChtBx_OKBtn_UP'),
                                              buttons.find('**/ChtBx_OKBtn_DN'),
                                              buttons.find('**/ChtBx_OKBtn_Rllvr')),
                                     relief = None,
                                     text = "Ok",
                                     scale = 1.5,
                                     text_scale = 0.05,
                                     text_pos = (0.0, -0.1),
                                     pos = (0, 0, -1),
                                     command = self.__handleCongrats,
                                     extraArgs = [avatarChoice],
                                     )
        buttons.removeNode()
        base.transitions.noFade()
        
    def __handleCongrats(self, avatarChoice):
        self.acceptedBanner.destroy()
        self.acceptedText.destroy()
        self.okButton.destroy()
        self.acceptedScreen.removeNode()
        del self.acceptedScreen
        del self.okButton
        del self.acceptedText
        del self.acceptedBanner
        # Send an acception confirmed message to the server!
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_SET_WISHNAME_CLEAR)
        datagram.addUint32(avatarChoice.id)
        datagram.addUint8(1)
        # Send the message
        self.send(datagram)        
        self.loginFSM.request("waitForSetAvatarResponse", [avatarChoice])

    def betterlucknexttime(self, avList, index):
        self.rejectDoneEvent = "rejectDone"
        self.rejectDialog = TTDialog.TTGlobalDialog(
            doneEvent = self.rejectDoneEvent,
            message = TTLocalizer.NameShopNameRejected,
            style = TTDialog.Acknowledge)
        self.rejectDialog.show()
        self.acceptOnce(self.rejectDoneEvent, self.__handleReject,
                        [avList, index])
        base.transitions.noFade()

    def __handleReject(self, avList, index):
        self.rejectDialog.cleanup()
        # Send a reject confirmed message to the server!
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_SET_WISHNAME_CLEAR)
        avid = 0
        for k in avList:
            if k.position == index:
                avid = k.id
        if avid == 0:
            # Trouble!  For some reason the toon picked couldn't be found in the list
            #  of potential avatars...
            # print "The sky is falling!"
            self.notify.error("Avatar rejected not found in avList.  Index is: " +
                              str(index))
        
        datagram.addUint32(avid)
        datagram.addUint8(0)
        # Send the message
        self.send(datagram)
        self.loginFSM.request("waitForAvatarList")
        #self.goToPickAName(avList, index)

    def enterChooseAvatar(self, avList):
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        
        # Set the current avatar state to zero, just in case
        # we were playing before. I'm not completely sure this is
        # the perfect place...
        self.sendSetAvatarIdMsg(0)
        self.clearFriendState()

        # Crank up the music again if it is not already playing
        # We might have just come back from make a toon which would
        # have killed the music when it started

        if (self.music == None) and base.musicManagerIsValid:
            # Reload the music if we don't have it already.
            self.music = base.musicManager.getSound("phase_3/audio/bgm/tt_theme.mid")
            # Set the music to play immediately after we load it.  It
            # is not clear why we need to do this even though we are
            # about to call base.playMusic() below, but it appears we
            # do; if we don't do this, sometimes music doesn't play
            # when we start the app.
            if self.music:
                self.music.setLoop(1)
                self.music.setVolume(0.9)
                self.music.play()
        base.playMusic(self.music, looping = 1, volume = 0.9, interrupt = None)
        
        self.handler = self.handleMessageType
        # Display the avatar choice screen
        self.avChoiceDoneEvent = "avatarChooserDone"
        self.avChoice = AvatarChooser.AvatarChooser(
                avList, self.loginFSM, self.avChoiceDoneEvent)
        self.avChoice.load(self.isPaid())
        self.avChoice.enter()
        
        # Hang hooks for when the selection is made
        self.accept(self.avChoiceDoneEvent, self.__handleAvatarChooserDone,
                    [avList])
        
        if config.GetBool('want-gib-loader', 0):
            self.loadingBlocker = ToontownLoadingBlocker.ToontownLoadingBlocker(avList)

    def __handleAvatarChooserDone(self, avList, doneStatus):
        done = doneStatus['mode']
        if (done == "exit"):
            # if running under the standalone launcher
            if not launcher.isDummy() and launcher.VISTA:
                # if not paid, exit to purchase web page
                if not self.isPaid():
                    self.loginFSM.request("shutdown", [OTPLauncherGlobals.ExitUpsell])
                else:
                    self.loginFSM.request("shutdown")
            else:
                self.loginFSM.request("shutdown")
            return
        index = self.avChoice.getChoice()
        assert((index >= 0) and (index <= self.avatarLimit))
        for av in avList:
            if av.position == index:
                avatarChoice = av
                self.notify.info("================")
                self.notify.info("Chose avatar id: %s" % (av.id))
                self.notify.info("Chose avatar name: %s" % (av.name))
                dna = ToonDNA.ToonDNA()
                dna.makeFromNetString(av.dna)
                self.notify.info("Chose avatar dna: %s" % (dna.asTuple(),))
                self.notify.info("Chose avatar position: %s" % (av.position))
                self.notify.info("isPaid: %s" % (self.isPaid()))
                self.notify.info("freeTimeLeft: %s" % (self.freeTimeLeft()))
                self.notify.info("allowSecretChat: %s" %
                                 (self.allowSecretChat()))
                self.notify.info("================")
        if (done == "chose"):
            self.avChoice.exit()
            if avatarChoice.approvedName != "":
                self.congratulations(avatarChoice)
                avatarChoice.approvedName = ""
            elif avatarChoice.rejectedName != "":
                avatarChoice.rejectedName = ""
                self.betterlucknexttime(avList, index)
            else:
                self.loginFSM.request("waitForSetAvatarResponse",
                                      [avatarChoice])
        elif (done == "nameIt"):
            self.accept('downloadAck-response', self.__handleDownloadAck, [avList, index])
            self.downloadAck = DownloadForceAcknowledge(
                'downloadAck-response')
            self.downloadAck.enter(4)
        elif (done == "create"):
            self.loginFSM.request("createAvatar", [avList, index])
        elif (done == "delete"):
            self.loginFSM.request("waitForDeleteAvatarResponse", [avatarChoice])

    def __handleDownloadAck(self, avList, index, doneStatus):
        if (doneStatus['mode'] == 'complete'):
            self.goToPickAName(avList, index)
        else:
            # Download is not done, go back to choosing your avatar
            self.loginFSM.request("chooseAvatar", [avList])
        self.downloadAck.exit()
        self.downloadAck = None
        self.ignore("downloadAck-response")

        
    def exitChooseAvatar(self):
        self.handler = None
        self.avChoice.exit()
        self.avChoice.unload()
        self.avChoice = None
        self.ignore(self.avChoiceDoneEvent)

    ##### Gray area #####
    def goToPickAName(self, avList, index):
        self.avChoice.exit()
        self.loginFSM.request("createAvatar", [avList, index])

    ##### LoginFSM: createAvatar #####

    def enterCreateAvatar(self, avList, index, newDNA = None):
        # Stop the music that started in ToontownStart
        if self.music:
            self.music.stop()
            self.music = None

        if newDNA != None:
            # This means we've come from the billing state (see creation
            # of nameshopState below) So what we do is create a potentialavatar,
            # add it to the list, send that on to makeatoon which sees that
            # the index called already has a potential avatar and jumps into
            # NameShop!  Ta da!
            self.newPotAv = PotentialAvatar.PotentialAvatar(
                'deleteMe',
                ["","","",""],
                newDNA.makeNetString(),
                index,
                1)
            avList.append(self.newPotAv)
            
        # We need the avList in case we go back to chooseAvatar mode
        # Display the create avatar screen
        base.transitions.noFade()
        self.avCreate = MakeAToon.MakeAToon(self.loginFSM, avList,
                                            "makeAToonComplete",
                                            index, self.isPaid())
        self.avCreate.load()
        self.avCreate.enter()

        self.handler = self.handleCreateAvatar
        
        # Hang hooks for when the selection is made
        self.accept("makeAToonComplete",
                    self.__handleMakeAToon, [avList, index])
        self.accept("nameShopCreateAvatar", self.sendCreateAvatarMsg)
        self.accept("nameShopPost", self.relayMessage)

    def relayMessage(self, dg):
        #print dg.dumpHex(ostream)
        self.send(dg)
        
    def handleCreateAvatar(self, msgType, di):
        #print di.getDatagram().dumpHex(ostream)
        #Roger wants to remove this if msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        #Roger wants to remove this el
        if msgType == CLIENT_CREATE_AVATAR_RESP or \
             msgType == CLIENT_SET_NAME_PATTERN_ANSWER or \
             msgType == CLIENT_SET_WISHNAME_RESP:
            self.avCreate.ns.nameShopHandler(msgType, di)
        else:
            self.handleMessageType(msgType, di)
    
    def __handleMakeAToon(self, avList, avPosition):
        done = self.avCreate.getDoneStatus()

        if (done == 'cancel'):
            # remove the temp, half-created av from the list
            if hasattr(self, 'newPotAv'):
                if self.newPotAv in avList:
                    avList.remove(self.newPotAv)
            self.avCreate.exit()
            self.loginFSM.request("chooseAvatar", [avList])
        elif (done == 'created'):
            self.avCreate.exit()
            # We need to see if the download is done. If it is, play the game,
            # otherwise go back to chooseAvatar which has a DFA
            # If you have no launcher, just play through as if the phase is
            # complete
            if ((not base.launcher) or
                base.launcher.getPhaseComplete(3.5)):
                # The avId will have been set in handleCreateAvatarResponseMsg
                # Now we are jumping directly into the game once we create
                # a toon, so we need to find the correct avatar
                for i in avList:
                    if (i.position == avPosition):
                        newPotAv = i
                self.loginFSM.request(
                    "waitForSetAvatarResponse", [newPotAv])
            else:
                # Download is not done yet
                self.loginFSM.request("chooseAvatar", [avList])
        else:
            self.notify.error("Invalid doneStatus from MakeAToon: " + str(done))

    def exitCreateAvatar(self):
        self.ignore("makeAToonComplete")
        self.ignore("nameShopPost")
        self.ignore("nameShopCreateAvatar")
        self.avCreate.unload()
        self.avCreate = None
        self.handler = None
        if hasattr(self, 'newPotAv'):
            del self.newPotAv


    def handleAvatarResponseMsg(self, di):
        """
        This is the handler called at startup time when the server is
        telling us details about our own avatar.  A different handler,
        handleGetAvatarDetailsResp, is called in response to the
        same message received while playing the game (in which case it
        is a response to a query about someone else, not information
        about ourselves).
        """
        self.cleanupWaitingForDatabase()
        # This should be the avatar Id that we had sent
        avatarId = di.getUint32()
        # Check for a valid avatar
        returnCode = di.getUint8()
        if returnCode == 0:
            # Put this avatar into the repository, but act like it
            # is a normal distributedToon... This is weird, because
            # we are simulating a "generate", but localAvatar is very
            # special.
            dclass = self.dclassesByName["DistributedToon"]

            # Turn off the little red arrows until we get established
            # in the game.
            NametagGlobals.setMasterArrowsOn(0)

            loader.beginBulkLoad("localAvatarPlayGame", OTPLocalizer.CREnteringToontown, 400,
                                 1, TTLocalizer.TIP_GENERAL)
            localAvatar = LocalToon.LocalToon(self)
            localAvatar.dclass = dclass

            # Hang onto the variable... We'll use it in playGame.
            base.localAvatar = localAvatar
            # Create a convenient global
            __builtins__["localAvatar"] = base.localAvatar

            # Also, make it the center of our arrows now.
            NametagGlobals.setToon(base.localAvatar)

            # Set the doId
            localAvatar.doId = avatarId
            # Store it locally too in case any DistributedObjects need to know
            self.localAvatarDoId = avatarId

            # Set the required fields
            # TODO: ROGER: where should we get parentId and zoneId from?
            parentId = None
            zoneId = None
            localAvatar.setLocation(parentId, zoneId)
            localAvatar.generateInit()
            localAvatar.generate()
            localAvatar.updateAllRequiredFields(dclass, di)

            # Put the new Obj in the dictionary
            self.doId2do[avatarId] = localAvatar

            # This stuff used to happen in announceGenerate for the localToon
            localAvatar.initInterface()

            # Ask for a friends list
            self.sendGetFriendsListRequest()
            # Start playing the game
            self.loginFSM.request('playingGame')
        else:
            self.notify.error("Bad avatar: return code %d" % (returnCode))

    ######### Get avatar details #########

    def getAvatarDetails(self, avatar, func, *args):
        """getAvatarDetails(self, Avatar, func, ...)

        Asks the server to tell us more detail about the indicated
        avatar.  The avatar may or may not be logged in at the moment.

        Because the response requires a round trip to the server, it
        will not come back immediately; instead, the indicated
        function will be called (with a boolean 'true' as the first
        parameter, the avatar object as the second parameter, and any
        remaining args as second parameters) when the data is
        available.

        If func is a string, it is the name of an event that will be
        thrown, rather than a function that will be called.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pad = ScratchPad()
        pad.func = func
        # args[0] should be the name of the dclass to use
        pad.args = args
        pad.avatar = avatar
        pad.delayDelete = DelayDelete.DelayDelete(avatar, 'getAvatarDetails')
        avId = avatar.doId
        self.__queryAvatarMap[avId] = pad
        self.__sendGetAvatarDetails(avId)

    def cancelAvatarDetailsRequest(self, avatar):
        """
        Remove pending request for avatar details, if any exists

        This is to avoid errors which result from an avatar detail
        request that bridges a teleportation to a new safezone.

        The teleport would unload the avatar detail panel and delete
        the fsm, which was expected to be there to handle the response.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Remove query map from dictionary
        avId = avatar.doId
        if self.__queryAvatarMap.has_key(avId):
            pad = self.__queryAvatarMap.pop(avId)
            pad.delayDelete.destroy()

    def __sendGetAvatarDetails(self, avId):
        """
        Sends the query-object message to the server.  The return
        message will be handled by handleGetAvatarDetailsResp().
        See getAvatarDetails().
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        datagram = PyDatagram()
        avatar = self.__queryAvatarMap[avId].avatar

        datagram.addUint16(avatar.getRequestID())

        # The avId we are querying.
        datagram.addUint32(avId)
        self.send(datagram)

    def handleGetAvatarDetailsResp(self, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # This should be the avatar Id that we had sent
        avId = di.getUint32()
        # Check for a valid avatar
        returnCode = di.getUint8()

        self.notify.info("Got query response for avatar %d, code = %d." % (avId, returnCode))

        # Get the function we originally passed to queryAvatar().
        try:
            pad = self.__queryAvatarMap[avId]
        except:
            # We didn't expect information about this avatar or the
            # request has been cancelled; ignore the message.
            self.notify.warning("Received unexpected or outdated details for avatar %d." % (avId))
            return

        del self.__queryAvatarMap[avId]

        gotData = 0
        if returnCode != 0:
            self.notify.warning("No information available for avatar %d." % (avId))
        else:
            # The avatar information that we have is valid.  Look up
            # the context and update the DistributedToon we were
            # given to getAvatarDetails().
            dclassName = pad.args[0]
            dclass = self.dclassesByName[dclassName]
            """
            if str(pad.avatar.__class__) == "toontown.toon.DistributedToon.DistributedToon":
                dclass = self.dclassesByName["DistributedToon"]
            elif str(pad.avatar.__class__) == "toontown.pets.DistributedPet.DistributedPet":
                dclass = self.dclassesByName["DistributedPet"]
            else:
                self.notify.warning("This avatar type is invalid: %s" % pad.avatar.__class__)
                return
            """

            # We don't call generate() on this avatar, since it's not
            # a real avatar; instead, it's just an empty placeholder
            # for all of the fields.
            pad.avatar.updateAllRequiredFields(dclass, di)
            gotData = 1

        if isinstance(pad.func, types.StringType):
            # If the pad "function" is actually a string, send an
            # event instead of calling the function.
            messenger.send(pad.func, list((gotData, pad.avatar) + pad.args))
        else:
            # Otherwise, call the function with the handle and the
            # additional arguments supplied.
            apply(pad.func, (gotData, pad.avatar) + pad.args)

        pad.delayDelete.destroy()

    # exitWaitForSetAvatarResponse() defined in OTPClientRepository.py

    def enterPlayingGame(self, *args, **kArgs):
        OTPClientRepository.OTPClientRepository.enterPlayingGame(self, *args, **kArgs)
        # Startup the child state machine.
        # -1 because we are not teleporting to another avatar.
        # defaultShard is the shard the server thinks we should go to
        # defaultZone is the zone the server thinks we should go to.
        # We make zoneId and hoodId the same because we are entering
        # into the safe zone.
        self.gameFSM.request("waitOnEnterResponses",
                             [None,                                # shard
                              base.localAvatar.defaultZone,        # hood
                              base.localAvatar.defaultZone,        # zone
                              -1                              # avId
                              ])
        self._userLoggingOut = False

    def exitPlayingGame(self):
        # First, stop all loose intervals that are tagged with autoPause or
        # autoFinish set true.  These are intervals that the owners won't
        # necessarily stop when they get disabled.
        ivalMgr.interrupt()
        
        # Note: the object manager is not a distributed object.  We just
        # need a good place to destroy it
        if self.objectManager != None:
            self.objectManager.destroy()
            self.objectManager = None

        # Unload the global panels.
        ToontownFriendSecret.unloadFriendSecret()
        FriendsListPanel.unloadFriendsList()
        messenger.send('cancelFriendInvitation')
        
        #get rid of glitch detector
        base.removeGlitchMessage()

        # remove any tasks that might be leaking
        taskMgr.remove("avatarRequestQueueTask")        

        OTPClientRepository.OTPClientRepository.exitPlayingGame(self)

        # Now get rid of localAvatar, if there is one.
        if hasattr(base, "localAvatar"):
            # Position the camera
            camera.reparentTo(render)
            camera.setPos(0, 0, 0)
            camera.setHpr(0, 0, 0)
            # Remove localAvatar from the dictionary.
            del self.doId2do[base.localAvatar.getDoId()]
            if base.localAvatar.getDelayDeleteCount() != 0:
                self.notify.error(
                    'could not delete localAvatar, delayDeletes=%s' %
                    (base.localAvatar.getDelayDeleteNames(),))
            base.localAvatar.deleteOrDelay()
            base.localAvatar.detectLeaks()
            # Get rid of the base reference
            NametagGlobals.setToon(base.cam)
            del base.localAvatar
            del __builtins__["localAvatar"]
            
        # Interrupt the loading bar, if it's up.
        loader.abortBulkLoad()

        # On reflection, it's not a good idea to clean up the
        # RelatedObjectMgr hooks here, because that just hides the
        # underlying problem of some objects that do not properly
        # clean themselves up.
        #self.relatedObjectMgr.abortAllRequests()
        
        base.transitions.noTransitions()

        # only check for leaks if the user is logging out and may go back into the game;
        # we don't want old hooks and tasks hanging around when they go back in
        # otherwise don't spam customer service with leak exit crashes
        if self._userLoggingOut:
            self.detectLeaks(
                okTasks=[],
                okEvents=["destroy-ToontownLoadingScreenTitle",
                          "destroy-ToontownLoadingScreenTip",
                          "destroy-ToontownLoadingScreenWaitBar",
                          ])

    ##### gameFSM: gameOff #####

    def enterGameOff(self):
        OTPClientRepository.OTPClientRepository.enterGameOff(self)
        assert self.allSubShardObjectsGone()

    ##### gameFSM: waitOnEnterResponses #####

    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        # we're starting fresh now in terms of sub-shard objects
        self.resetDeletedSubShardDoIds()
        OTPClientRepository.OTPClientRepository.enterWaitOnEnterResponses(
            self, shardId, hoodId, zoneId, avId)

    ##### gameFSM: skipTutorialRequest #####
    def enterSkipTutorialRequest(self, hoodId, zoneId, avId):
        # this state currently not used
        self.handlerArgs = {"hoodId": hoodId,
                            "zoneId": zoneId,
                            "avId": avId}
        self.handler = self.handleTutorialQuestion
        self.__requestSkipTutorial(hoodId, zoneId, avId)
        

    def __requestSkipTutorial(self, hoodId, zoneId, avId):
        self.notify.debug("requesting skip tutorial")
        # Get ready for permission to begin a tutorial
        self.acceptOnce("skipTutorialAnswered",
                        self.__handleSkipTutorialAnswered,
                        [hoodId, zoneId, avId])
        # Ask the tutorial manager to put us in a tutorial
        messenger.send("requestSkipTutorial")
        self.waitForDatabaseTimeout(requestName='RequestSkipTutorial')

    def __handleSkipTutorialAnswered(self, hoodId, zoneId, avId, allOk):
        """AI responding to our request to skip the tutorial."""
        if allOk:
            hoodId = self.handlerArgs["hoodId"]
            zoneId = self.handlerArgs["zoneId"]
            avId = self.handlerArgs["avId"]
            self.gameFSM.request("playGame", [hoodId, zoneId, avId])
        else:
            self.notify.warning("allOk is false on skip tutorial, forcing the tutorial.")
            self.gameFSM.request("tutorialQuestion", [hoodId, zoneId, avId])

    def exitSkipTutorialRequest(self):
        self.cleanupWaitingForDatabase()
        self.handler = None
        self.handlerArgs = None
        self.ignore("skipTutorialAnswered")

    ##### gameFSM: tutorialQuestion #####

    # Note: This state is now poorly named. We used to pop up a dialog
    # box asking the user if they would like a tutorial during this
    # state. Now the state has been short circuted so that if the state
    # is reached, we will always do the tutorial.
    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        self.handler = self.handleTutorialQuestion
        self.__requestTutorial(hoodId, zoneId, avId)
        
    def handleTutorialQuestion(self, msgType, di):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequiredOther(di)
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_DISABLE_RESP:
            self.handleDisable(di)
        elif msgType == CLIENT_OBJECT_DELETE_RESP:
            self.handleDelete(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_RESP:
            self.handleGetFriendsList(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_EXTENDED_RESP:
            self.handleGetFriendsListExtended(di)
        elif msgType == CLIENT_FRIEND_ONLINE:
            self.handleFriendOnline(di)
        elif msgType == CLIENT_FRIEND_OFFLINE:
            self.handleFriendOffline(di)
        elif msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
            self.handleGetAvatarDetailsResp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        # Moved to handleMessageType elif msgType == CLIENT_GET_STATE_RESP:
        # Moved to handleMessageType     # HACK! This should really be handled.
        # Moved to handleMessageType     pass
        #elif msgType == CLIENT_DONE_SET_ZONE_RESP:
        #    # HACK! This should really be handled.
        #    pass
        else:
            self.handleMessageType(msgType, di)

    def __requestTutorial(self, hoodId, zoneId, avId):
        self.notify.debug("requesting tutorial")
        # Get ready for permission to begin a tutorial
        self.acceptOnce("startTutorial",
                        self.__handleStartTutorial,
                        [avId])
        # Ask the tutorial manager to put us in a tutorial
        messenger.send("requestTutorial")
        self.waitForDatabaseTimeout(requestName='RequestTutorial')

    def __handleStartTutorial(self, avId, zoneId):
        # In this case, the TutorialManager has sent us the zone we should
        # go to in order to enter the Tutorial.
        self.gameFSM.request("playGame", [Tutorial, zoneId, avId])

    def exitTutorialQuestion(self):
        self.cleanupWaitingForDatabase()
        self.handler = None
        self.handlerArgs = None
        self.ignore("startTutorial")
        taskMgr.remove("waitingForTutorial")
        
    ##### gameFSM: switchShards #####

    def enterSwitchShards(self, shardId, hoodId, zoneId, avId):
        OTPClientRepository.OTPClientRepository.enterSwitchShards(
            self, shardId, hoodId, zoneId, avId)
        # prevent any new objects from the old shard from being created.
        # see comment in enterCloseShard().
        self.handler = self.handleCloseShard

    def exitSwitchShards(self):
        OTPClientRepository.OTPClientRepository.exitSwitchShards(self)
        self.ignore(ToontownClientRepository.ClearInterestDoneEvent)
        self.handler = None

    ##### gameFSM: closeShard #####

    def enterCloseShard(self, loginState=None):
        OTPClientRepository.OTPClientRepository.enterCloseShard(self,
                                                                loginState)
        # Install a handler that prevents new objects from being created on
        # the old shard. This is to accomodate the way Toontown was
        # written. Future games should be able to handle objects being
        # created at this point, up until the time when the shard interest
        # has been closed.
        self.handler = self.handleCloseShard
        self._removeLocalAvFromStateServer()

    def handleCloseShard(self, msgType, di):
        # ignore creates for objects that are children of the old shard
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            di2 = PyDatagramIterator(di)
            parentId = di2.getUint32()
            if self._doIdIsOnCurrentShard(parentId):
                return
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            di2 = PyDatagramIterator(di)
            parentId = di2.getUint32()
            if self._doIdIsOnCurrentShard(parentId):
                return
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            di2 = PyDatagramIterator(di)
            doId = di2.getUint32()
            if self._doIdIsOnCurrentShard(doId):
                return
        self.handleMessageType(msgType, di)

    def _logFailedDisable(self, doId, ownerView):
        # intercept failed disables and don't log anything if we've manually
        # removed the object from the doId2do
        if doId not in self.doId2do and doId in self._deletedSubShardDoIds:
            return
        OTPClientRepository.OTPClientRepository._logFailedDisable(self, doId,
                                                                  ownerView)

    def exitCloseShard(self):
        OTPClientRepository.OTPClientRepository.exitCloseShard(self)
        self.ignore(ToontownClientRepository.ClearInterestDoneEvent)
        self.handler = None

    def isShardInterestOpen(self):
        return ((self.old_setzone_interest_handle is not None) or
                (self.uberZoneInterest is not None))

    def resetDeletedSubShardDoIds(self):
        # clear out the set of doIds of manually-deleted sub-shard objects
        self._deletedSubShardDoIds.clear()

    def dumpAllSubShardObjects(self):
        # This is pretty much the same thing as self._abandonShard but I want to
        # keep them separate; _abandonShard is intended for emergency shutdown,
        # this is intended for normal operation (e.g. going through the quiet
        # zone, switching shards, etc.)
        if self.KeepSubShardObjects:
            return
        isNotLive = not base.cr.isLive()
        if isNotLive:
            try:
                localAvatar
            except:
                self.notify.info('dumpAllSubShardObjects')
            else:
                self.notify.info('dumpAllSubShardObjects: defaultShard is %s' % localAvatar.defaultShard)
            # these classes are always marked 'never disable', so they will never be deleted by this method
            ignoredClasses = (
                'MagicWordManager', 'TimeManager', 'DistributedDistrict',
                'FriendManager', 'NewsManager', 'ToontownMagicWordManager',
                'WelcomeValleyManager', 'DistributedTrophyMgr', 'CatalogManager',
                'DistributedBankMgr', 'EstateManager', 'RaceManager',
                'SafeZoneManager', 'DeleteManager', 'TutorialManager',
                'ToontownDistrict', 'DistributedDeliveryManager', 'DistributedPartyManager',
                'AvatarFriendsManager', 'InGameNewsMgr', 'TTCodeRedemptionMgr')

        # give objects a chance to clean themselves up before checking for DelayDelete leaks
        messenger.send('clientCleanup')
        # cancel any outstanding avatarDetails requests (they use DelayDeletes)
        for avId, pad in self.__queryAvatarMap.items():
            pad.delayDelete.destroy()
        self.__queryAvatarMap = {}
        # some of these objects might be holding delayDeletes on others
        # track each object that is delayDeleted after it gets its change to delete,
        # and check them after all objects have had a chance to delete
        delayDeleted = []
        # get a local copy of the doIds in case the doId2do table changes while we're working
        doIds = self.doId2do.keys()
        for doId in doIds:
            obj = self.doId2do[doId]
            if isNotLive:
                ignoredClass = obj.__class__.__name__ in ignoredClasses
                if (not ignoredClass) and (obj.parentId != localAvatar.defaultShard):
                    self.notify.info('dumpAllSubShardObjects: %s %s parent %s is not defaultShard' %
                                     (obj.__class__.__name__, obj.doId, obj.parentId))
            if ((obj.parentId == localAvatar.defaultShard) and
                (obj is not localAvatar)):
                if obj.neverDisable:
                    if isNotLive:
                        if not ignoredClass:
                            self.notify.warning('dumpAllSubShardObjects: neverDisable set for %s %s' %
                                                (obj.__class__.__name__, obj.doId))
                else:
                    self.deleteObject(doId)
                    self._deletedSubShardDoIds.add(doId)
                    if obj.getDelayDeleteCount() != 0:
                        delayDeleted.append(obj)
        # now that all objects have had a chance to delete, are there any objects left
        # that are still delayDeleted?
        delayDeleteLeaks = []
        for obj in delayDeleted:
            if obj.getDelayDeleteCount() != 0:
                delayDeleteLeaks.append(obj)
        if len(delayDeleteLeaks):
            s = 'dumpAllSubShardObjects:'
            for obj in delayDeleteLeaks:
                s += ('\n  could not delete %s (%s), delayDeletes=%s' %
                      (safeRepr(obj), itype(obj), obj.getDelayDeleteNames()))
            self.notify.error(s)
        if isNotLive:
            self.notify.info('dumpAllSubShardObjects: doIds left: %s' % self.doId2do.keys())
        assert self.allSubShardObjectsGone()

    if __debug__:
        def allSubShardObjectsGone(self):
            for doId, obj in self.doId2do.items():
                if not ((obj is localAvatar) or
                        (obj.parentId != localAvatar.defaultShard) or
                        ((obj.parentId == localAvatar.defaultShard) and obj.neverDisable)):
                    return False
            return True

    # internal func, do not call. See OTPClientRepository.removeShardInterest()
    def _removeCurrentShardInterest(self, callback):
        if self.old_setzone_interest_handle is None:
            assert self.uberZoneInterest is None
            self.notify.warning('removeToontownShardInterest: no shard interest open')
            callback()
            return
        self.acceptOnce(ToontownClientRepository.ClearInterestDoneEvent,
                        Functor(self._tcrRemoveUberZoneInterest, callback))
        self._removeEmulatedSetZone(
            ToontownClientRepository.ClearInterestDoneEvent)
    # internal func, do not call
    def _tcrRemoveUberZoneInterest(self, callback):
        assert self.uberZoneInterest is not None
        self.acceptOnce(ToontownClientRepository.ClearInterestDoneEvent,
                        Functor(self._tcrRemoveShardInterestDone, callback))
        self.removeInterest(
            self.uberZoneInterest,
            ToontownClientRepository.ClearInterestDoneEvent)
    # internal func, do not call
    def _tcrRemoveShardInterestDone(self, callback):
        assert self.allSubShardObjectsGone()
        self.uberZoneInterest = None
        callback()

    def _doIdIsOnCurrentShard(self, doId):
        if doId == base.localAvatar.defaultShard:
            return True
        do = self.getDo(doId)
        if do:
            if do.parentId == base.localAvatar.defaultShard:
                return True
        return False

    ###################################################
    # Interface to get Shard Stat Details
    ###################################################
    def _wantShardListComplete(self):   
        print self.activeDistrictMap
        if self._shardsAreReady():
            self.acceptOnce(ToontownDistrictStats.EventName(), self.shardDetailStatsComplete)
            ToontownDistrictStats.refresh()                
        else:
            self.loginFSM.request("noShards")

    def shardDetailStatsComplete(self):
        self.loginFSM.request("waitForAvatarList")            

    def exitWaitForShardList(self):
        self.ignore(ToontownDistrictStats.EventName())
        OTPClientRepository.OTPClientRepository.exitWaitForShardList(self)

    ##################################################
    # Friends list management
    ##################################################

    def fillUpFriendsMap(self):
        """
        Ensure that the friendsMap has a valid entry for each friend
        on our friendsList.  If it's missing some, query the server.
        Returns true if the map is complete, or false if we have to
        wait for it.  If we have to wait, the message
        "friendsMapComplete" will be thrown when it is done.
        """
        if self.isFriendsMapComplete():
            return 1

        if not self.friendsMapPending and not self.friendsListError:
            self.notify.warning('Friends list stale; fetching new list.')
            self.sendGetFriendsListRequest()
        return 0

    def isFriend(self, doId):
        """
        Returns true if the indicated avatar is a friend of the
        LocalToon, false otherwise.
        """
        # Check in the LocalToon's friends list.  The friendsMap is
        # not the authority on this; it might be incomplete, or it
        # might include extra toons that are no longer our friends.
        for friendId, flags in base.localAvatar.friendsList:
            if friendId == doId:
                # It *is* in the friends list.  Make sure it's in the
                # friendsMap too.
                self.identifyFriend(doId)
                return 1

        return 0
        
    def isAvatarFriend(self, doId):
        """
        Returns true if the indicated avatar is a friend of the
        LocalToon, false otherwise.
        """
        # Check in the LocalToon's friends list.  The friendsMap is
        # not the authority on this; it might be incomplete, or it
        # might include extra toons that are no longer our friends.
        for friendId, flags in base.localAvatar.friendsList:
            if friendId == doId:
                # It *is* in the friends list.  Make sure it's in the
                # friendsMap too.
                self.identifyFriend(doId)
                return 1

        return 0

    def getFriendFlags(self, doId):
        """
        Returns the uint8 associated with the indicated friend, or 0
        if the doId is not a friend of the LocalToon.

        This byte specifies some additional bits of data that may be
        associated with friends.  Presently, only bit 1 is used, to
        specify that we can chat freely with the given friend.
        """
        for friendId, flags in base.localAvatar.friendsList:
            if friendId == doId:
                return flags

        return 0

    def isFriendOnline(self, doId):
        """
        Returns true if the indicated friend is currently online,
        false otherwise.
        """
        return self.friendsOnline.has_key(doId)

    def addAvatarToFriendsList(self, avatar):
        self.friendsMap[avatar.doId] = avatar
        
    def identifyFriend(self, doId, source=None):
        """
        Returns a FriendHandle telling us who the indicated friend (or
        non-friend avatar in the same zone) is.  If the avatar cannot
        be identified for some strange reason, returns None.

        Note that this cannot be used to determine whether the
        indicated avatar is or is not a friend, since it may return
        something other than None even if the avatar is not a friend.
        Use isFriend() to ask whether a particular avatar is a friend.
        """
        if self.friendsMap.has_key(doId):
            return self.friendsMap[doId]

        # Hmm, we don't know who this friend is.  Is it someone
        # we've heard about this session?
        avatar = None
        if self.doId2do.has_key(doId):
            avatar = self.doId2do[doId]
        elif self.cache.contains(doId):
            avatar = self.cache.dict[doId]
        elif self.playerFriendsManager.getAvHandleFromId(doId):
            avatar = base.cr.playerFriendsManager.getAvHandleFromId(doId)
        else:
            # Haven't got a clue.
            self.notify.warning("Don't know who friend %s is." % (doId))
            return None

        if not (isinstance(avatar, DistributedToon.DistributedToon) or
                isinstance(avatar, DistributedPet.DistributedPet)):
            self.notify.warning('friendsNotify%s: invalid friend object %s' % (
                choice(source, '(%s)' % source, ''), doId))
            return None

        if base.wantPets:
            if avatar.isPet():
                if avatar.bFake:
                    handle = PetHandle.PetHandle(avatar)
                else:
                    handle = avatar
            else:
                handle = FriendHandle.FriendHandle(doId, avatar.getName(), avatar.style, avatar.getPetId())
        else:
            handle = FriendHandle.FriendHandle(doId, avatar.getName(), avatar.style, "")

        self.friendsMap[doId] = handle        
        return handle

    def identifyPlayer(self, pId):
        return base.cr.playerFriendsManager.getFriendInfo(pId)

    def identifyAvatar(self, doId):
        """
        Returns either an avatar or a FriendHandle, whichever we can
        find, to reference the indicated doId.
        """
        if self.doId2do.has_key(doId):
            return self.doId2do[doId]
        else:
            return self.identifyFriend(doId)

    def isFriendsMapComplete(self):
        """
        Returns true if every avatar on our friends list is also
        listed in the friends map, false otherwise.
        """
        for friendId, flags in base.localAvatar.friendsList:
            if self.identifyFriend(friendId) == None:
                return 0

        if base.wantPets and base.localAvatar.hasPet():
            print str(self.friendsMap)
            print str(self.friendsMap.has_key(base.localAvatar.getPetId()))
            if self.friendsMap.has_key(base.localAvatar.getPetId()) == None:
                return 0

        return 1

    def removeFriend(self, avatarId):
        """removeFriend(self, int avatarId)

        Sends a message to the server requesting we break the
        friendship with the indicated avatar Id.  The avatar will be
        removed from our friends list, and we will be removed from his
        (or hers).
        """
        # First, send a message to the one we're de-friending.  We do
        # this by sending a message via the LocalToon, to the actual
        # destination avatar--a little bit of indirection.
        base.localAvatar.sendUpdate("friendsNotify", [base.localAvatar.doId, 1], sendToId = avatarId)

        # Now actually end the friendship.
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_REMOVE_FRIEND)
        # Add the avatar to remove
        datagram.addUint32(avatarId)
        # send the message
        self.send(datagram)

        # If the toon is at his estate went he de-friends someone, we check
        # if the ex-friend is also at his estate.  If so, the AI needs to
        # kick him out.
        self.estateMgr.removeFriend(base.localAvatar.doId, avatarId)

        # Explicitly remove the friend from our friends list now.
        # This will be done eventually by the server, but we'll do it
        # now so we'll be current.

        for pair in base.localAvatar.friendsList:
            friendId = pair[0]
            if friendId == avatarId:
                # Here's our friend entry; remove it.
                base.localAvatar.friendsList.remove(pair)
                return

    def clearFriendState(self):
        """
        Removes all the cached information about current friends,
        which friends are online, etc.  It is appropriate to do this
        only when the toon logs out.
        """
        self.friendsMap = {}
        self.friendsOnline = {}
        self.friendsMapPending = 0
        self.friendsListError = 0

    def sendGetFriendsListRequest(self):
        """
        Sends a message to the server requesting the list of our
        friends along with their names and dnas.  This will be used to
        populate the friendsMap.
        """
        self.friendsMapPending = 1
        self.friendsListError = 0

        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_GET_FRIEND_LIST)
        # send the message
        self.send(datagram)


    def cleanPetsFromFriendsMap(self):
        #this looks through the friends list for any DistributedPet
        #references hanging around and makes sure the references are gone

        for (objId, obj) in self.friendsMap.items():
            from toontown.pets import DistributedPet
            if (isinstance(obj, DistributedPet.DistributedPet)):
                print "Removing %s reference from the friendsMap" % obj.getName()
                del self.friendsMap[objId]

    def removePetFromFriendsMap(self):
        #removes the handle to the localToon's pet from the friendslist map
        doId = base.localAvatar.getPetId()

        if doId and self.friendsMap.has_key(doId):
            del self.friendsMap[doId]
        
    def addPetToFriendsMap(self, callback=None):
        #need to add the pet to the list
        doId = base.localAvatar.getPetId()

        if (not doId) or self.friendsMap.has_key(doId):
            #toon does not have a pet or the pet has already been added
            if callback:
                callback()
            return
        
        def petDetailsCallback(petAvatar):
            #self.friendsMap[doId] = petAvatar
            handle = PetHandle.PetHandle(petAvatar)
            self.friendsMap[doId] = handle
            petAvatar.disable()
            petAvatar.delete()
            if callback:
                callback()
            if self._proactiveLeakChecks:
                petAvatar.detectLeaks()

        PetDetail.PetDetail(doId, petDetailsCallback)
        
    def handleGetFriendsList(self, di):
        # Is this record in error?
        error = di.getUint8()
        if error:
            self.notify.warning("Got error return from friends list.")
            self.friendsListError = 1
        else:
            count = di.getUint16()
            for i in range(0, count):
                doId = di.getUint32()
                name = di.getString()
                dnaString = di.getString()
                dna = ToonDNA.ToonDNA()
                dna.makeFromNetString(dnaString)
                petId = di.getUint32()

                handle = FriendHandle.FriendHandle(doId, name, dna, petId)
                self.friendsMap[doId] = handle

                # Make sure our list of online friends has the most
                # current info.
                if self.friendsOnline.has_key(doId):
                    self.friendsOnline[doId] = handle

                if self.friendPendingChatSettings.has_key(doId):
                    self.notify.debug('calling setCommonAndWL %s' %
                                     str(self.friendPendingChatSettings[doId]))
                    handle.setCommonAndWhitelistChatFlags(
                        * self.friendPendingChatSettings[doId])

            if base.wantPets and base.localAvatar.hasPet():
                def handleAddedPet():
                    self.friendsMapPending = 0
                    messenger.send('friendsMapComplete')
                self.addPetToFriendsMap(handleAddedPet)
                return  #don't signal 'done' until we have the pet details

        self.friendsMapPending = 0
        messenger.send('friendsMapComplete')
        
    def handleGetFriendsListExtended(self, di):
        avatarHandleList = []
        # Is this record in error?
        error = di.getUint8()
        if error:
            self.notify.warning("Got error return from friends list extended.")
        else:
            count = di.getUint16()
            for i in range(0, count):
                abort = 0
                doId = di.getUint32()
                name = di.getString()
                if name == '':
                    abort = 1
                dnaString = di.getString()
                if dnaString == '':
                    abort = 1
                else:
                    dna = ToonDNA.ToonDNA()
                    dna.makeFromNetString(dnaString)
                petId = di.getUint32()

                if not abort:
                    handle = FriendHandle.FriendHandle(doId, name, dna, petId)
                    avatarHandleList.append(handle)
        
        if avatarHandleList:
            messenger.send('gotExtraFriendHandles', [avatarHandleList])



    def handleFriendOnline(self, di):
        doId = di.getUint32()
        commonChatFlags=0
        whitelistChatFlags=0
        if di.getRemainingSize() > 0:
            commonChatFlags = di.getUint8()
        if di.getRemainingSize() > 0:
            whitelistChatFlags = di.getUint8()
        self.notify.debug("Friend %d now online. common=%d whitelist=%d" %
                         (doId, commonChatFlags, whitelistChatFlags))

        if not self.friendsOnline.has_key(doId):
            self.friendsOnline[doId] = self.identifyFriend(doId)            
            messenger.send('friendOnline', [doId, commonChatFlags, whitelistChatFlags])
            if not self.friendsOnline[doId]:
                # we haven't received the friends list message yet
                self.friendPendingChatSettings[doId] = (commonChatFlags, whitelistChatFlags)

    def handleFriendOffline(self, di):
        doId = di.getUint32()
        self.notify.debug("Friend %d now offline." % (doId))

        try:
            del self.friendsOnline[doId]
            messenger.send('friendOffline', [doId])
        except:
            pass

    ##################################################
    # Toontown Specific Functionality
    ##################################################

    def getFirstBattle(self):
        # Return the first battle in the repository (for testing purposes)
        from toontown.battle import DistributedBattleBase
        for dobj in self.doId2do.values():
            if (isinstance(dobj,
                           DistributedBattleBase.DistributedBattleBase)):
                return dobj

    def forbidCheesyEffects(self, forbid):
        """
        If forbid is 1, increments the forbidCheesyEffects counter,
        preventing cheesy effects in the current context.  If forbid is
        0, decrements this counter.  You should always match
        increments with decrements.
        """
        wasAllowed = (self.__forbidCheesyEffects != 0)
        if forbid:
            self.__forbidCheesyEffects += 1
        else:
            self.__forbidCheesyEffects -= 1

        assert(self.__forbidCheesyEffects >= 0)
        isAllowed = (self.__forbidCheesyEffects != 0)
        if wasAllowed != isAllowed:
            # If we just changed state, reconsider everyone's
            # cheesiness.
            for av in Avatar.Avatar.ActiveAvatars:
                if hasattr(av, "reconsiderCheesyEffect"):
                    av.reconsiderCheesyEffect()

            base.localAvatar.reconsiderCheesyEffect()

    def areCheesyEffectsAllowed(self):
        return (self.__forbidCheesyEffects == 0)

    def getNextSetZoneDoneEvent(self):
        """this returns the event that will be generated when the next
        emulated setZone msg (not yet sent) completes, and we are fully
        in the new zone with all DOs in that zone"""
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return '%s-%s' % (ToontownClientRepository.EmuSetZoneDoneEvent,
                          self.setZonesEmulated+1)
    def getLastSetZoneDoneEvent(self):
        """this returns the event that will be generated when the last
        emulated setZone msg (already sent) completes, and we are fully
        in the new zone with all DOs in that zone"""
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return '%s-%s' % (ToontownClientRepository.EmuSetZoneDoneEvent,
                          self.setZonesEmulated)

    # recreate the behaviour of sendSetZoneMsg
    def sendSetZoneMsg(self, zoneId, visibleZoneList=None):
        #########################################
        # don't change this ordering
        event = self.getNextSetZoneDoneEvent()
        self.setZonesEmulated += 1
        #########################################
        parentId = base.localAvatar.defaultShard

        # move the avatar
        self.sendSetLocation(base.localAvatar.doId, parentId, zoneId)
        localAvatar.setLocation(parentId, zoneId)

        # move the interest
        interestZones = zoneId
        if visibleZoneList is not None:
            assert zoneId in visibleZoneList
            interestZones = visibleZoneList

        # We don't want more than one setInterest on the wire at
        # once. Only send it out now if there's nothing else queued up.
        # Otherwise we'll send it when the previous request completes.
        self._addInterestOpToQueue(ToontownClientRepository.SetInterest,
                                   [parentId, interestZones,
                                    "OldSetZoneEmulator"], event)

    def resetInterestStateForConnectionLoss(self):
        OTPClientRepository.OTPClientRepository.resetInterestStateForConnectionLoss(self)
        self.old_setzone_interest_handle = None
        self.setZoneQueue.clear()

    def _removeEmulatedSetZone(self, doneEvent):
        # remove any emulated-setZone interest; do this when leaving
        # a shard
        self._addInterestOpToQueue(ToontownClientRepository.ClearInterest,
                                   None, doneEvent)

    def _addInterestOpToQueue(self, op, args, event):
        # push an operation onto the setZone queue
        self.setZoneQueue.push([op, args, event])
        # are we the only one in the queue?
        if len(self.setZoneQueue) == 1:
            self._sendNextSetZone()

    def _sendNextSetZone(self):
        # send the next request in the queue, but leave it in there;
        # see _handleEmuSetZoneDone
        op, args, event = self.setZoneQueue.top()
        if op == ToontownClientRepository.SetInterest:
            parentId, interestZones, name = args
            if (self.old_setzone_interest_handle == None):
                self.old_setzone_interest_handle = self.addInterest(
                    parentId, interestZones, name,
                    ToontownClientRepository.SetZoneDoneEvent)
            else:
                self.alterInterest(
                    self.old_setzone_interest_handle,
                    parentId, interestZones, name,
                    ToontownClientRepository.SetZoneDoneEvent)
        elif op == ToontownClientRepository.ClearInterest:
            self.removeInterest(self.old_setzone_interest_handle,
                                ToontownClientRepository.SetZoneDoneEvent)
            self.old_setzone_interest_handle = None
        else:
            self.notify.error('unknown setZone op: %s' % op)

    def _handleEmuSetZoneDone(self):
        # OK, a setZone finished
        op, args, event = self.setZoneQueue.pop()
        # The message handler might queue something else up; check if the
        # queue is empty before generating the event.
        queueIsEmpty = self.setZoneQueue.isEmpty()
        if event is not None:
            if not base.killInterestResponse:
                messenger.send(event)
            else:
                if not hasattr(self, '_dontSendSetZoneDone'):
                    import random
                    if random.random() < .05:
                        self._dontSendSetZoneDone = True
                    else:
                        messenger.send(event)
        if not queueIsEmpty:
            self._sendNextSetZone()

    def _isPlayerDclass(self, dclass):
        return dclass == self._playerAvDclass
    
    def _isValidPlayerLocation(self, parentId, zoneId):
        # are we on a district?
        if not self.distributedDistrict:
            return False
        # is the toon under the district?
        if parentId != self.distributedDistrict.doId:
            return False
        # is the toon in the district's uberzone?
        if (parentId == self.distributedDistrict.doId) and (zoneId == OTPGlobals.UberZone):
            return False
        return True

    def sendQuietZoneRequest(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Send the message
        self.sendSetZoneMsg(OTPGlobals.QuietZone)

    def handleQuietZoneGenerateWithRequired(self, di):
        # Special handler for quiet zone generates -- we need to filter
        parentId = di.getUint32()
        zoneId = di.getUint32()
        assert parentId in self.doId2do
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]
        # only create 'neverDisable' objects when we're in the quiet zone
        if dclass.getClassDef().neverDisable:
            dclass.startGenerate()
            distObj = self.generateWithRequiredFields(dclass, doId, di, parentId, zoneId)
            dclass.stopGenerate()

    def handleQuietZoneGenerateWithRequiredOther(self, di):
        # Special handler for quiet zone generates -- we need to filter
        parentId = di.getUint32()
        zoneId = di.getUint32()
        assert parentId in self.doId2do
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]
        # only create 'neverDisable' objects when we're in the quiet zone
        if dclass.getClassDef().neverDisable:
            dclass.startGenerate()
            distObj = self.generateWithRequiredOtherFields(dclass, doId, di, parentId, zoneId)
            dclass.stopGenerate()

    def handleQuietZoneUpdateField(self, di):
        # Special handler for quiet zone generates -- we need to filter
        # only allow updates to objects with neverDisable set to True
        di2 = DatagramIterator(di)
        doId = di2.getUint32()
        if doId in self.deferredDoIds:
            args, deferrable, dg0, updates = self.deferredDoIds[doId]
            dclass = args[2]
            if not dclass.getClassDef().neverDisable:
                return
        else:
            # object has been generated
            do = self.getDo(doId)
            if do:
                if not do.neverDisable:
                    return
        OTPClientRepository.OTPClientRepository.handleUpdateField(self, di)

    def handleDelete(self, di):
        # Get the DO Id
        doId = di.getUint32()
        self.deleteObject(doId)

    def deleteObject(self, doId, ownerView=False):
        """
        Removes the object from the client's view of the world.  This
        should normally not be called except in the case of error
        recovery, since the server will normally be responsible for
        deleting and disabling objects as they go out of scope.

        After this is called, future updates by server on this object
        will be ignored (with a warning message).  The object will
        become valid again the next time the server sends a generate
        message for this doId.

        This is not a distributed message and does not delete the
        object on the server or on any other client.
        """
        if self.doId2do.has_key(doId):
            # If it is in the dictionary, remove it.
            obj = self.doId2do[doId]
            # Remove it from the dictionary
            del self.doId2do[doId]
            # Disable, announce, and delete the object itself...
            # unless delayDelete is on...
            obj.deleteOrDelay()
            if obj.getDelayDeleteCount() <= 0:
                obj.detectLeaks()
        elif self.cache.contains(doId):
            # If it is in the cache, remove it.
            self.cache.delete(doId)
        else:
            # Otherwise, ignore it
            ClientRepository.notify.warning(
                "Asked to delete non-existent DistObj " + str(doId))

    def _abandonShard(self):
        # simulate removal of shard interest for quick shutdown
        for doId, obj in self.doId2do.items():
            if ((obj.parentId == localAvatar.defaultShard) and
                (obj is not localAvatar)):
                self.deleteObject(doId)
                
    def askAvatarKnown(self, avId):
        if not hasattr(base, "localAvatar"):
            return 0
        for friendPair in base.localAvatar.friendsList:
            if friendPair[0] == avId:
                return 1
        return 0
 
    def requestAvatarInfo(self, avId):
        if avId == 0:
            return
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_GET_FRIEND_LIST_EXTENDED)
        datagram.addUint16(1) #number of avIds
        datagram.addUint32(avId)
        # send the message
        base.cr.send(datagram)
        
    def queueRequestAvatarInfo(self, avId):
        removeTask = 0
        if not hasattr(self, "avatarInfoRequests"):
            self.avatarInfoRequests = []

        if self.avatarInfoRequests:
            taskMgr.remove("avatarRequestQueueTask")
        if avId not in self.avatarInfoRequests:
            self.avatarInfoRequests.append(avId)  
            
        taskMgr.doMethodLater(0.1, self.sendAvatarInfoRequests, "avatarRequestQueueTask")
        
        
    def sendAvatarInfoRequests(self, task = None):
        print("Sending request Queue for AV Handles")
        if not hasattr(self, "avatarInfoRequests"):
            return
        if len(self.avatarInfoRequests) == 0:
            return
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_GET_FRIEND_LIST_EXTENDED)
        datagram.addUint16(len(self.avatarInfoRequests)) #number of avIds
        for avId in self.avatarInfoRequests:
            datagram.addUint32(avId)
        # send the message
        base.cr.send(datagram)
        
