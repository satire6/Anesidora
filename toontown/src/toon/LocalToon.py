"""LocalToon module: contains the LocalToon class"""

#import time
import random
import math

from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
#from direct.showbase.InputStateGlobal import inputState
from direct.showbase.PythonUtil import *
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals

from pandac.PandaModules import *

from otp.avatar import LocalAvatar
from otp.login import LeaveToPayDialog
from otp.avatar import PositionExaminer
from otp.otpbase import OTPGlobals

from toontown.shtiker import ShtikerBook
from toontown.shtiker import InventoryPage
from toontown.shtiker import MapPage
from toontown.shtiker import OptionsPage
from toontown.shtiker import ShardPage
from toontown.shtiker import QuestPage
from toontown.shtiker import TrackPage
from toontown.shtiker import KartPage
from toontown.shtiker import GardenPage
from toontown.shtiker import GolfPage
from toontown.shtiker import SuitPage
from toontown.shtiker import DisguisePage
from toontown.shtiker import PhotoAlbumPage
#from toontown.shtiker import BuildingPage
from toontown.shtiker import FishPage
from toontown.shtiker import NPCFriendPage
from toontown.shtiker import EventsPage
from toontown.shtiker import TIPPage



from toontown.quest import Quests
from toontown.quest import QuestParser
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.catalog import CatalogNotifyDialog
from toontown.chat import ToontownChatManager
from toontown.chat import TTTalkAssistant
from toontown.estate import GardenGlobals
#from toontown.estate import GardenProgressMeter
from toontown.battle.BattleSounds import *
from toontown.battle import Fanfare
from toontown.parties import PartyGlobals

from toontown.toon import ElevatorNotifier
import DistributedToon
import Toon
import LaffMeter

# Checks whether we want to display the news page
# which uses Awesomium to render HTML
WantNewsPage = base.config.GetBool('want-news-page', ToontownGlobals.DefaultWantNewsPageSetting)
from toontown.toontowngui import NewsPageButtonManager
if WantNewsPage:
    from toontown.shtiker import NewsPage

AdjustmentForNewsButton = -0.275

if (__debug__):
    import pdb

class LocalToon(DistributedToon.DistributedToon, LocalAvatar.LocalAvatar):
    """LocalToon class:"""

    # The localToon should not be disabled when we enter the quiet zone
    neverDisable = 1

    # The number of seconds it takes to move the pie power meter to
    # full the first time.
    piePowerSpeed = base.config.GetDouble('pie-power-speed', 0.2)

    # The exponent that controls the factor at which the pie power
    # meter slows down over time.  Values closer to 1.0 slow down less
    # quickly.
    piePowerExponent = base.config.GetDouble('pie-power-exponent', 0.75)

    def __init__(self, cr):
        """
        Local toon constructor
        """
        try:
            self.LocalToon_initialized
        except:
            self.LocalToon_initialized = 1
            self.numFlowers = 0
            self.maxFlowerBasket = 0
            DistributedToon.DistributedToon.__init__(self, cr)
            chatMgr = ToontownChatManager.ToontownChatManager(cr, self)
            talkAssistant = TTTalkAssistant.TTTalkAssistant()
            LocalAvatar.LocalAvatar.__init__(self, cr, chatMgr, talkAssistant,passMessagesThrough = True)
            #self.setNameVisible(0)

            ### BEGIN FROM LOCAL AVATAR ##################################
            # This used to be in LocalAvatar, but it really is Toon specific

            # Note: we cannot load these phase 4 sounds in the
            # initialize function because of the phased download
            self.soundRun = base.loadSfx(
                "phase_3.5/audio/sfx/AV_footstep_runloop.wav")
            self.soundWalk = base.loadSfx(
                "phase_3.5/audio/sfx/AV_footstep_walkloop.wav")
            self.soundWhisper = base.loadSfx(
                "phase_3.5/audio/sfx/GUI_whisper_3.mp3")
            self.soundPhoneRing = base.loadSfx(
                "phase_3.5/audio/sfx/telephone_ring.mp3")
            self.positionExaminer = PositionExaminer.PositionExaminer()

            # A button to open up the Friends List.
            friendsGui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
            friendsButtonNormal = friendsGui.find("**/FriendsBox_Closed")
            friendsButtonPressed = friendsGui.find("**/FriendsBox_Rollover")
            friendsButtonRollover = friendsGui.find("**/FriendsBox_Rollover")
            newScale = oldScale = 0.8            
            if WantNewsPage:                
                newScale = oldScale * ToontownGlobals.NewsPageScaleAdjust
            self.bFriendsList = DirectButton(
                image = (friendsButtonNormal,
                     friendsButtonPressed,
                     friendsButtonRollover),
                relief = None,
                pos = (1.192, 0, 0.875),
                scale = newScale,
                text = ("", TTLocalizer.FriendsListLabel, TTLocalizer.FriendsListLabel),
                text_scale = 0.09,
                text_fg = Vec4(1,1,1,1),
                text_shadow = Vec4(0,0,0,1),
                text_pos = (0,-0.18),
                text_font = ToontownGlobals.getInterfaceFont(),
                command = self.sendFriendsListEvent,
                )
            self.bFriendsList.hide()
            self.friendsListButtonActive = 0
            self.friendsListButtonObscured = 0
            self.moveFurnitureButtonObscured = 0
            self.clarabelleButtonObscured = 0
            friendsGui.removeNode()

            self.__furnitureGui = None
            self.__clarabelleButton = None
            self.__clarabelleFlash = None
            # These flags are set by setFurnitureDirector().
            self.furnitureManager = None
            self.furnitureDirector = None

            # In case we got the catalog notify message while we were
            # still downloading phase5.5, we'll need to delay it and pop
            # it up when we actually download the phase.
            self.gotCatalogNotify = 0
            self.__catalogNotifyDialog = None
            self.accept('phaseComplete-5.5', self.loadPhase55Stuff)

            ### END FROM LOCAL AVATAR ####################################
                    
            # Init the avatar sounds
            Toon.loadDialog()

            # It variable for the Tag minigame
            # I know it is strange living in here, but it 
            # was the only way I could think of for the Distributed
            # Treasure to know if the local toon is it
            self.isIt = 0

            self.cantLeaveGame = 0

            # define these tunnel variables, just to be safe
            # these are set to real values when you exit an area
            # through a tunnel
            self.tunnelX = 0.

            self.estate = None

            # We use this to detect where our tossed pie hits.
            self.__pieBubble = None

            # And this is set if we're allowed to throw pies.
            self.allowPies = 0
            self.__pieButton = None
            self.__piePowerMeter = None
            self.__piePowerMeterSequence = None
            self.__pieButtonType = None
            self.__pieButtonCount = None
            self.tossPieStart = None
            self.__presentingPie = 0
            self.__pieSequence = 0

            self.wantBattles = base.config.GetBool('want-battles', 1)
            self.seeGhosts = base.config.GetBool("see-ghosts", 0)
            wantNameTagAvIds = base.config.GetBool('want-nametag-avids',0)
            if wantNameTagAvIds:
                # simulate doing ~idTags
                messenger.send('nameTagShowAvId', [])
                base.idTags = 1
            
            self.glitchX = 0
            self.glitchY = 0
            self.glitchZ = 0
            self.glitchCount = 0
            self.ticker = 0
            self.glitchOkay = 1
            self.tempGreySpacing = 0
            
            self.wantStatePrint = base.config.GetBool('want-statePrint', 0)

            #These items related to the gardening estates expansion
            self.__gardeningGui = None
            self.__gardeningGuiFake = None
            self.__shovelButton = None
            self.shovelRelatedDoId = 0 #this could be a garden plot, a tree
            self.shovelAbility = "" #this could be "Plant", "Pick"
            self.plantToWater = 0
            
            self.shovelButtonActiveCount = 0
            self.wateringCanButtonActiveCount = 0
            
            self.showingWateringCan = 0
            self.showingShovel = 0
            
            self.touchingPlantList = []
            
            self.inGardenAction = None
            self.guiConflict = 0
            
            self.lastElevatorLeft = 0
            
            self.elevatorNotifier = ElevatorNotifier.ElevatorNotifier()
            
            # switchboard friends messages
            
            self.accept(OTPGlobals.AvatarFriendAddEvent, self.sbFriendAdd)
            self.accept(OTPGlobals.AvatarFriendUpdateEvent, self.sbFriendUpdate)
            self.accept(OTPGlobals.AvatarFriendRemoveEvent, self.sbFriendRemove)

            self._zoneId = None
            
            self.accept("system message aknowledge", self.systemWarning)
            self.systemMsgAckGuiDoneEvent = "systemMsgAckGuiDoneEvent"
            self.accept(self.systemMsgAckGuiDoneEvent, self.hideSystemMsgAckGui)
            self.systemMsgAckGui = None
            self.createSystemMsgAckGui()
            if not hasattr(base.cr, 'lastLoggedIn'):
                # I'm not sure this will ever happen in test or on live
                # but in the dev local environment this case hits after I've just created a new toon
                # on a brand new account
                base.cr.lastLoggedIn = self.cr.toontownTimeManager.convertStrToToontownTime("")
            self.setLastTimeReadNews(base.cr.lastLoggedIn)
            
            # GMs have accepting-new-friends-default 0, which forces them to explicitly enable 
            # friend requests if they ever want it.
            self.acceptingNewFriends = Settings.getAcceptingNewFriends() and base.config.GetBool('accepting-new-friends-default', True)

    def wantLegacyLifter(self):
        return True
                        
    def startGlitchKiller(self):
        #print ("trying glitch killer %s" % (localAvatar.getZoneId()))
        if localAvatar.getZoneId() not in GlitchKillerZones:
            #print("skipping")
            return
        if __dev__:
            self.glitchMessage = "START GLITCH KILLER"
            randChoice = random.randint(0, 3)
            if randChoice == 0:
                self.glitchMessage = "START GLITCH KILLER"
            elif randChoice == 1:
                self.glitchMessage = "GLITCH KILLER ENGAGED"
            elif randChoice == 2:
                self.glitchMessage = "GLITCH KILLER GO!"
            elif randChoice == 3:
                self.glitchMessage = "GLITCH IN YO FACE FOOL!"
            else:
                pass
            
            self.notify.debug(self.glitchMessage)
        #print("starting")
        taskMgr.remove(self.uniqueName("glitchKiller"))
        taskMgr.add(self.glitchKiller, self.uniqueName("glitchKiller"))
        self.glitchOkay = 1
        
    def pauseGlitchKiller(self):
        self.tempGreySpacing = 1
        
    def unpauseGlitchKiller(self):
        self.tempGreySpacing = 0
       
    def stopGlitchKiller(self):
        if __dev__ and (hasattr(self, "glitchMessage")):
            if self.glitchMessage == "START GLITCH KILLER":
                self.notify.debug("STOP GLITCH KILLER")
            elif self.glitchMessage == "GLITCH KILLER ENGAGED":
                self.notify.debug("GLITCH KILLER DISENGAGED")
            elif self.glitchMessage == "GLITCH KILLER GO!":
                self.notify.debug("GLITCH KILLER NO GO!")
            elif self.glitchMessage == "GLITCH IN YO FACE FOOL!":
                self.notify.debug("GLITCH OFF YO FACE FOOL!")
            else:
                pass

        taskMgr.remove(self.uniqueName("glitchKiller"))
        self.glitchOkay = 1
               
    def glitchKiller(self, taskFooler = 0):
        if base.greySpacing or self.tempGreySpacing:
            return Task.cont
        self.ticker += 1 #only used for printouts
        if not self.physControls.lifter.hasContact() and not self.glitchOkay:
            self.glitchCount += 1
        else:
            self.glitchX = self.getX()
            self.glitchY = self.getY()
            self.glitchZ = self.getZ()
            self.glitchCount = 0
            if self.physControls.lifter.hasContact():
                self.glitchOkay = 0
        if hasattr(self, "physControls"):
            if self.ticker >= 10:
                self.ticker = 0
                #height = self.getPos(self.shadowPlacer.shadowNodePath)
                #height = self.physControls.determineHeight()
                #print(self.physControls.lifter.hasContact())
        if self.glitchCount >= 7:
            print("GLITCH MAXED!!! resetting pos")
            self.setX(self.glitchX - (1 * (self.getX() - self.glitchX)))
            self.setY(self.glitchY - (1 * (self.getY() - self.glitchY)))
            #self.setPos(self.glitchX, self.glitchY, self.getZ())
            self.glitchCount = 0
            
        return Task.cont
 
    def announceGenerate(self):
        # Start looking around
        self.startLookAround()

        if (base.wantNametags):
            # Manage our own nametag.
            self.nametag.manage(base.marginManager)

        DistributedToon.DistributedToon.announceGenerate(self)
        
        from otp.friends import FriendInfo
        
    
    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        self.laffMeter.destroy()
        del self.laffMeter

        if hasattr(self, 'purchaseButton'):
            self.purchaseButton.destroy()
            del self.purchaseButton

        # Clean up the book
        self.newsButtonMgr.request('Off')
        self.book.unload()
        del self.optionsPage
        del self.shardPage
        del self.mapPage
        del self.invPage
        #del self.achievePage
        del self.questPage
        del self.suitPage
        del self.sosPage
        del self.disguisePage
        del self.fishPage
        del self.gardenPage
        del self.trackPage
        #del self.buildingPage
        del self.book

        if base.wantKarts:
            if( hasattr( self, "kartPage" ) ):
                del self.kartPage

        if (base.wantNametags):
            self.nametag.unmanage(base.marginManager)

        # We shouldn't need this...
        self.ignoreAll()
        # Call down the inheritance chain
        
        DistributedToon.DistributedToon.disable(self)
        return

    def disableBodyCollisions(self):
        """
        Override DistributedAvatar because we do not have body collisions
        """
        pass

    def delete(self):
        try:
            self.LocalToon_deleted
        except:
            self.LocalToon_deleted = 1
            # Unload the avatar sounds
            Toon.unloadDialog()
            QuestParser.clear()
            DistributedToon.DistributedToon.delete(self)
            LocalAvatar.LocalAvatar.delete(self)
            self.bFriendsList.destroy()
            del self.bFriendsList
            if self.__pieButton:
                self.__pieButton.destroy()
                self.__pieButton = None
            if self.__piePowerMeter:
                self.__piePowerMeter.destroy()
                self.__piePowerMeter = None
            ### LOCAL AVATAR ###########################
            taskMgr.remove("unlockGardenButtons")
            taskMgr.remove('lerpFurnitureButton')
            if self.__furnitureGui:
                self.__furnitureGui.destroy()
            del self.__furnitureGui
            if self.__gardeningGui:
                self.__gardeningGui.destroy()
            del self.__gardeningGui
            if self.__gardeningGuiFake:
                self.__gardeningGuiFake.destroy()
            del self.__gardeningGuiFake               
            if self.__clarabelleButton:
                self.__clarabelleButton.destroy()
            del self.__clarabelleButton
            if self.__clarabelleFlash:
                self.__clarabelleFlash.finish()
            del self.__clarabelleFlash
            if self.__catalogNotifyDialog:
                self.__catalogNotifyDialog.cleanup()
            del self.__catalogNotifyDialog

    def initInterface(self):
        self.newsButtonMgr = NewsPageButtonManager.NewsPageButtonManager()
        self.newsButtonMgr.request('Hidden')
    
        # make one and only one ShtikerBook
        self.book = ShtikerBook.ShtikerBook("bookDone")
        self.book.load()
        self.book.hideButton()

        self.optionsPage = OptionsPage.OptionsPage()
        self.optionsPage.load()
        self.book.addPage(
            self.optionsPage, pageName = TTLocalizer.OptionsPageTitle)

        self.shardPage = ShardPage.ShardPage()
        self.shardPage.load()
        self.book.addPage(self.shardPage, pageName = TTLocalizer.ShardPageTitle)

        self.mapPage = MapPage.MapPage()
        self.mapPage.load()
        self.book.addPage(self.mapPage, pageName = TTLocalizer.MapPageTitle)
        
        self.invPage = InventoryPage.InventoryPage()
        self.invPage.load()
        self.book.addPage(
            self.invPage, pageName = TTLocalizer.InventoryPageTitle)

        self.questPage = QuestPage.QuestPage()
        self.questPage.load()
        self.book.addPage(
            self.questPage, pageName = TTLocalizer.QuestPageToonTasks)

        self.trackPage = TrackPage.TrackPage()
        self.trackPage.load()
        self.book.addPage(
            self.trackPage, pageName = TTLocalizer.TrackPageShortTitle)

        #self.achievePage = AchievePage.AchievePage()
        #self.achievePage.load()
        #self.book.addPage(
        # self.achievePage, pageName = TTLocalizer.AchievePageTitle)

        self.suitPage = SuitPage.SuitPage()
        self.suitPage.load()
        self.book.addPage(self.suitPage, pageName = TTLocalizer.SuitPageTitle)

        if base.config.GetBool("want-photo-album", 0):
            self.photoAlbumPage = PhotoAlbumPage.PhotoAlbumPage()
            self.photoAlbumPage.load()
            self.book.addPage(
                self.photoAlbumPage, pageName = TTLocalizer.PhotoPageTitle)

        self.fishPage = FishPage.FishPage()
        self.fishPage.setAvatar(self)
        self.fishPage.load()
        self.book.addPage(self.fishPage, pageName = TTLocalizer.FishPageTitle)

        if base.wantKarts:
            self.addKartPage()

        # The disguisePage and sosPage members are initialized to None
        # by DistributedToon.__init__().

        if self.disguisePageFlag:
            self.loadDisguisePages()

        #self.buildingPage = BuildingPage.BuildingPage()
        #self.buildingPage.load()
        #self.book.addPage(
        # self.buildingPage, pageName = TTLocalizer.BuildingPageTitle)
        
        if self.gardenStarted:
            self.loadGardenPages()

        self.addGolfPage()

        self.addEventsPage()

        if WantNewsPage:
            self.addNewsPage()
                
        # self.addTIPPage()

        self.book.setPage(self.mapPage, enterPage = False)
        
        # make a laff-o-meter for the localToon
        self.laffMeter = LaffMeter.LaffMeter(self.style,
                                             self.hp,
                                             self.maxHp)
        self.laffMeter.setAvatar(self)
        self.laffMeter.setScale(0.075)
        if self.style.getAnimal() == "monkey":
            # The monkey laff meter is slightly bigger because the
            # ears hang off to the side, so slide it over to the right
            self.laffMeter.setPos(-1.18, 0., -0.87)
        else:
            self.laffMeter.setPos(-1.2, 0., -0.87)
        self.laffMeter.stop()

        # make a purchase button for non-paid players
        if not base.cr.isPaid():
            guiButton = loader.loadModel("phase_3/models/gui/quit_button")
            self.purchaseButton = DirectButton(
                parent = aspect2d,
                relief = None,
                image = (guiButton.find("**/QuitBtn_UP"),
                         guiButton.find("**/QuitBtn_DN"),
                         guiButton.find("**/QuitBtn_RLVR"),
                         ),
                image_scale = 0.9,
                text = TTLocalizer.OptionsPagePurchase,
                text_scale = 0.05,
                text_pos = (0, -0.01),
                textMayChange = 0,
                pos = (0.885, 0, -0.94),
                command = self.__handlePurchase,
                )
            # turn of the margin cell this overlaps with
            base.setCellsAvailable([base.bottomCells[4]], 0)
        
        # We used to use the insert key for tossing pies.
        self.accept('time-insert', self.__beginTossPie)
        self.accept('time-insert-up', self.__endTossPie)

        # Nowadays we use the delete key instead, for better
        # consistency with Macs (which lack an insert key).
        self.accept('time-delete', self.__beginTossPie)
        self.accept('time-delete-up', self.__endTossPie)
        
        self.accept('pieHit', self.__pieHit)

        # These events interrupt a pie toss in progress.
        self.accept('interrupt-pie', self.interruptPie)
        self.accept('InputState-jump', self.__toonMoved)
        self.accept('InputState-forward', self.__toonMoved)
        self.accept('InputState-reverse', self.__toonMoved)
        self.accept('InputState-turnLeft', self.__toonMoved)
        self.accept('InputState-turnRight', self.__toonMoved)
        self.accept('InputState-slide', self.__toonMoved)

        QuestParser.init()

    def __handlePurchase(self):
        # confirm exit game to purchase
        """__handlePurchase(self)
        """
        self.purchaseButton.hide()
        if base.cr.isWebPlayToken() or __dev__:
            if base.cr.isPaid():
                if base.cr.productName in ['DisneyOnline-UK', 'DisneyOnline-AP',
                  'JP', 'DE', 'BR', 'FR'] :
                    paidNoParentPassword = launcher and launcher.getParentPasswordSet()
                else:
                    paidNoParentPassword = launcher and not launcher.getParentPasswordSet()
            else:
                paidNoParentPassword = 0
            self.leaveToPayDialog = LeaveToPayDialog.LeaveToPayDialog(paidNoParentPassword, self.purchaseButton.show)
            self.leaveToPayDialog.show()
        else:
            self.notify.error("You should not get here without a PlayToken")

    if base.wantKarts:
        def addKartPage( self ):
            """
            Purpose:
            
            Params: None
            Return: None
            """
            # Only show the button if the toon owns a kart.
            if( self.hasKart() ):

                if hasattr(self, "kartPage") and self.kartPage != None:
                    # The page is already loaded; never mind.
                    return
                
                if not launcher.getPhaseComplete(6):
                    # We haven't downloaded phase 6 yet; set a callback hook
                    # so the pages will load when we do get phase 6.
                    self.acceptOnce('phaseComplete-6', self.addKartPage)
                    return
                
                self.kartPage = KartPage.KartPage()
                self.kartPage.setAvatar( self )
                self.kartPage.load()
                self.book.addPage( self.kartPage,
                                   pageName = TTLocalizer.KartPageTitle )

    def setWantBattles(self, wantBattles):
        self.wantBattles = wantBattles

    def loadDisguisePages(self):
        # Load up and add the Cog disguise page and NPC SOS pages to
        # the shticker book.  This is deferred because it doesn't
        # happen for a new toon who has never been to CogHQ, and it
        # doesn't happen until we have downloaded phase 9.
        if self.disguisePage != None or self.sosPage != None:
            # The pages are already loaded; never mind.
            return

        if not launcher.getPhaseComplete(9):
            # We haven't downloaded phase 9 yet; set a callback hook
            # so the pages will load when we do get phase 9.
            self.acceptOnce('phaseComplete-9', self.loadDisguisePages)
            return

        self.disguisePage = DisguisePage.DisguisePage()
        self.disguisePage.load()
        self.book.addPage(self.disguisePage,
                          pageName = TTLocalizer.DisguisePageTitle)

        self.sosPage = NPCFriendPage.NPCFriendPage()
        self.sosPage.load()
        self.book.addPage(self.sosPage,
                          pageName = TTLocalizer.NPCFriendPageTitle)                    
        
    def loadGardenPages(self):
        if self.gardenPage != None :
            # The pages are already loaded; never mind.
            return
            
        if not launcher.getPhaseComplete(5.5):
            # We haven't downloaded phase 5.5 yet; set a callback hook
            # so the pages will load when we do get phase 5.5.
            self.acceptOnce('phaseComplete-5.5', self.loadPhase55Stuff)
            return
            
        self.gardenPage = GardenPage.GardenPage()
        self.gardenPage.load()
        self.book.addPage(self.gardenPage, pageName = TTLocalizer.GardenPageTitle)
        
    def loadPhase55Stuff(self):
        if self.gardenPage == None:
            self.gardenPage = GardenPage.GardenPage()
            self.gardenPage.load()
            self.book.addPage(self.gardenPage, pageName = TTLocalizer.GardenPageTitle)
        elif not launcher.getPhaseComplete(5.5):
            self.acceptOnce('phaseComplete-5.5', self.loadPhase55Stuff)
        self.refreshOnscreenButtons()
        
        
#    def displayWhisper(self, fromId, chatString, whisperType):
#        # We have to define this here to force the correct
#        # displayWhisper() function to be called.
#        LocalAvatar.LocalAvatar.displayWhisper(self, fromId, chatString, whisperType)
        
#    def displayWhisperPlayer(self, fromId, chatString, whisperType):
#        # We have to define this here to force the correct
#        # displayWhisper() function to be called.
#        LocalAvatar.LocalAvatar.displayWhisperPlayer(self, fromId, chatString, whisperType)

    # GM account stuff
    def setAsGM(self, state):
        self.notify.debug("Setting GM State: %s in LocalToon" %state)
        DistributedToon.DistributedToon.setAsGM(self, state)
        if self.gmState:
            if base.config.GetString('gm-nametag-string', '') != '':
                self.gmNameTagString = base.config.GetString('gm-nametag-string')
            if base.config.GetString('gm-nametag-color', '') != '':
                self.gmNameTagColor = base.config.GetString('gm-nametag-color')
            if base.config.GetInt('gm-nametag-enabled', 0):
                self.gmNameTagEnabled = 1
            self.d_updateGMNameTag()

    # Whisper
    def displayTalkWhisper(self, fromId, avatarName, rawString, mods):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This function overrides a similar function in DistributedAvatar.
        """
        sender = base.cr.identifyAvatar(fromId)
        if sender:
            chatString, scrubbed = sender.scrubTalk(rawString, mods)
        else:
            chatString,scrubbed = self.scrubTalk(rawString, mods)
        
        sender = self
        sfx = self.soundWhisper

        # MPG we need to identify the sender in a non-toontown specific way
        #sender = base.cr.identifyAvatar(fromId)
            

        chatString = avatarName + ": " + chatString
            
        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               WhisperPopup.WTNormal)

        whisper.setClickable(avatarName, fromId)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)

    def displayTalkAccount(self, fromId, senderName, rawString, mods):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This function overrides a similar function in DistributedAvatar.
        """
        sender = None
        playerInfo = None
        sfx = self.soundWhisper

        # MPG we need to identify the sender in a non-toontown specific way
        #sender = base.cr.identifyAvatar(fromId)
        #sender = idenityPlayer(fromId)
        playerInfo = base.cr.playerFriendsManager.playerId2Info.get(fromId,None)
        if playerInfo == None:
            #import pdb; pdb.set_trace()
            return
            
        senderAvId = base.cr.playerFriendsManager.findAvIdFromPlayerId(fromId)
        
        if (not senderName) and base.cr.playerFriendsManager.playerId2Info.get(fromId):
            senderName = base.cr.playerFriendsManager.playerId2Info.get(fromId).playerName
      
        senderAvatar = base.cr.identifyAvatar(senderAvId)
        if sender:
            chatString,scrubbed = senderAvatar.scrubTalk(rawString, mods)
        else:
            chatString,scrubbed = self.scrubTalk(rawString, mods)
            
        chatString = senderName + ": " + chatString
            
        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               WhisperPopup.WTNormal)
        if playerInfo != None:
            whisper.setClickable(senderName, fromId, 1)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)


    def isLocal(self):
        return 1

    def canChat(self):
        """
        Returns true if there is some point to chatting: the local
        toon has at least one secret friend, for instance, or he has
        chat permission.
        """
        if not self.cr.allowAnyTypedChat():
            return 0
        
        if self.commonChatFlags & (ToontownGlobals.CommonChat | ToontownGlobals.SuperChat):
            return 1
        
        if base.cr.whiteListChatEnabled:
            return 1

        for friendId, flags in self.friendsList:
            if flags & ToontownGlobals.FriendChat:
                return 1

        return 0

    # chat methods
    def startChat(self):
        if self.tutorialAck:
            self.notify.info("calling LocalAvatar.startchat")
            LocalAvatar.LocalAvatar.startChat(self)
            self.accept("chatUpdateSCToontask", self.b_setSCToontask)
            self.accept("chatUpdateSCResistance", self.d_reqSCResistance)
            self.accept("chatUpdateSCSinging", self.b_setSCSinging)
            self.accept("whisperUpdateSCToontask", self.whisperSCToontaskTo)
        else:
            self.notify.info("NOT calling LocalAvatar.startchat, in tutorial")

    def stopChat(self):
        LocalAvatar.LocalAvatar.stopChat(self)
        self.ignore("chatUpdateSCToontask")
        self.ignore("chatUpdateSCResistance")
        self.ignore("chatUpdateSCSinging")
        self.ignore("whisperUpdateSCToontask")

    def tunnelIn(self, tunnelOrigin):
        self.b_setTunnelIn(self.tunnelX * .8, tunnelOrigin)

    def tunnelOut(self, tunnelOrigin):
        self.tunnelX = self.getX(tunnelOrigin)
        tunnelY = self.getY(tunnelOrigin)
        self.b_setTunnelOut(self.tunnelX * .95, tunnelY, tunnelOrigin)

    def handleTunnelIn(self, startTime, endX, x, y, z, h):
        self.notify.debug("LocalToon.handleTunnelIn")

        # create a temporary tunnel origin node
        tunnelOrigin = render.attachNewNode('tunnelOrigin')
        tunnelOrigin.setPosHpr(x,y,z,h,0,0)

        self.b_setAnimState("run", self.animMultiplier)
        self.stopLookAround()
        self.reparentTo(render)
        self.runSound()

        # Pull the camera back
        camera.reparentTo(render)
        camera.setPosHpr(tunnelOrigin, 0, 20, 12, 180, -20, 0)

        # iris in
        base.transitions.irisIn(0.4)

        # lerp the toon
        toonTrack = self.getTunnelInToonTrack(endX, tunnelOrigin)

        def cleanup(self=self, tunnelOrigin=tunnelOrigin):
            self.stopSound()
            tunnelOrigin.removeNode()
            messenger.send("tunnelInMovieDone")
        
        self.tunnelTrack = Sequence(
            toonTrack,
            Func(cleanup),
            )
        self.tunnelTrack.start(globalClock.getFrameTime() - startTime)

    def handleTunnelOut(self, startTime, startX, startY, x, y, z, h):
        self.notify.debug("LocalToon.handleTunnelOut")

        # create a temporary tunnel origin node
        tunnelOrigin = render.attachNewNode('tunnelOrigin')
        tunnelOrigin.setPosHpr(x,y,z,h,0,0)

        self.b_setAnimState("run", self.animMultiplier)
        self.runSound()
        self.stopLookAround()

        tracks = Parallel()

        # Pull the camera back
        camera.wrtReparentTo(render)
        startPos = camera.getPos(tunnelOrigin)
        startHpr = camera.getHpr(tunnelOrigin)
        camLerpDur = 1.
        reducedCamH = fitDestAngle2Src(startHpr[0], 180)
        tracks.append(
            LerpPosHprInterval(camera, camLerpDur, pos=Point3(0, 20, 12),
                               hpr=Point3(reducedCamH, -20, 0),
                               startPos = startPos,
                               startHpr = startHpr,
                               other=tunnelOrigin, blendType="easeInOut",
                               name="tunnelOutLerpCamPos"),
            )

        # lerp the toon
        toonTrack = self.getTunnelOutToonTrack(startX, startY, tunnelOrigin)
        tracks.append(toonTrack)

        # iris out
        irisDur = .4
        tracks.append(Sequence(
            Wait(toonTrack.getDuration() - (irisDur + .1)),
            Func(base.transitions.irisOut, irisDur),
            ))
            
        def cleanup(self=self, tunnelOrigin=tunnelOrigin):
            self.stopSound()
            self.detachNode()
            tunnelOrigin.removeNode()
            messenger.send("tunnelOutMovieDone")
        
        self.tunnelTrack = Sequence(
            tracks,
            Func(cleanup),
            )
        self.tunnelTrack.start(globalClock.getFrameTime() - startTime)

    ### Tossing a pie (used in final Boss Battle sequence)
        
    def getPieBubble(self):
        if self.__pieBubble == None:
            bubble = CollisionSphere(0, 0, 0, 1)
            node = CollisionNode('pieBubble')
            node.addSolid(bubble)
            node.setFromCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.CameraBitmask | ToontownGlobals.FloorBitmask)
            node.setIntoCollideMask(BitMask32.allOff())
            self.__pieBubble = NodePath(node)
            self.pieHandler = CollisionHandlerEvent()
            self.pieHandler.addInPattern('pieHit')
            self.pieHandler.addInPattern('pieHit-%in')
        return self.__pieBubble

    def __beginTossPieMouse(self, mouseParam):
        self.__beginTossPie(globalClock.getFrameTime())

    def __endTossPieMouse(self, mouseParam):
        self.__endTossPie(globalClock.getFrameTime())

    def __beginTossPie(self, time):
        # The toss-pie key was pressed.
        if self.tossPieStart != None:
            # This is probably just key-repeat.
            return

        if not self.allowPies:
            return

        if self.numPies == 0:
            messenger.send('outOfPies')
            return

        if self.__pieInHand():
            return
        
        if getattr(self.controlManager.currentControls, "isAirborne", 0):
            # Can't toss a pie while we're airborne.
            return
            
        messenger.send('wakeup')
        self.localPresentPie(time)

        taskName = self.uniqueName('updatePiePower')
        taskMgr.add(self.__updatePiePower, taskName)
        
    def __endTossPie(self, time):
        if self.tossPieStart == None:
            return

        taskName = self.uniqueName('updatePiePower')
        taskMgr.remove(taskName)
        
        messenger.send('wakeup')
        # The toss-pie key was released.  Toss the pie.
        power = self.__getPiePower(time)
        self.tossPieStart = None
        
        self.localTossPie(power)

    def localPresentPie(self, time):
        import TTEmote
        from otp.avatar import Emote

        self.__stopPresentPie()
        if self.tossTrack:
            tossTrack = self.tossTrack
            self.tossTrack = None
            tossTrack.finish()

        self.interruptPie()

        self.tossPieStart = time
        self.__pieSequence = (self.__pieSequence + 1) & 0xff
        sequence = self.__pieSequence
        self.__presentingPie = 1

        pos = self.getPos()
        hpr = self.getHpr()
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits = 32)

        self.sendUpdate('presentPie', [pos[0], pos[1], pos[2],
                                       hpr[0], hpr[1], hpr[2],
                                       timestamp32])

        # We are now in pie-throwing mode, and can't move until we get
        # the end-pie event (which is thrown after our toss animation
        # completes, below).  We can, however, jump, which will
        # interrupt the pie in the air.
        Emote.globalEmote.disableBody(self)
        messenger.send('begin-pie')
        
        ival = self.getPresentPieInterval(pos[0], pos[1], pos[2],
                                          hpr[0], hpr[1], hpr[2])
        ival = Sequence(ival,
                        name = self.uniqueName('localPresentPie'))
        assert self.tossTrack == None
        self.tossTrack = ival
        ival.start()

        self.makePiePowerMeter()
        self.__piePowerMeter.show()
        self.__piePowerMeterSequence = sequence
        self.__piePowerMeter['value'] = 0

    def __stopPresentPie(self):
        if self.__presentingPie:
            import TTEmote 
            from otp.avatar import Emote
            Emote.globalEmote.releaseBody(self)        
            messenger.send('end-pie')
            self.__presentingPie = 0

        taskName = self.uniqueName('updatePiePower')
        taskMgr.remove(taskName)

    def __getPiePower(self, time):
        elapsed = max(time - self.tossPieStart, 0.0)
        t = elapsed / self.piePowerSpeed
        t = math.pow(t, self.piePowerExponent)
        power = int(t * 100) % 200
        if power > 100:
            power = 200 - power
            
        return power

    def __updatePiePower(self, task):
        if not self.__piePowerMeter:
            return Task.done
        
        self.__piePowerMeter['value'] = self.__getPiePower(globalClock.getFrameTime())
        return Task.cont

    def interruptPie(self):
        # Externally interrupt the present pie cycle (for instance,
        # because we've been hit).
        self.cleanupPieInHand()

        self.__stopPresentPie()
        if self.__piePowerMeter:
            self.__piePowerMeter.hide()

        pie = self.pieTracks.get(self.__pieSequence)
        if pie and pie.getT() < 14./24.:
            # If the pie hasn't started to fly yet, stop it prematurely.
            del self.pieTracks[self.__pieSequence]
            pie.pause()

    def __pieInHand(self):
        # Returns true if calling interruptPie() would eliminate the
        # current pie being thrown.
        pie = self.pieTracks.get(self.__pieSequence)
        return (pie and pie.getT() < 15./24.)

    def __toonMoved(self, isSet):
        if isSet:
            self.interruptPie()
            
    def localTossPie(self, power):
        if not self.__presentingPie:
            return
        
        pos = self.getPos()
        hpr = self.getHpr()
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits = 32)
        sequence = self.__pieSequence

        if self.tossTrack:
            tossTrack = self.tossTrack
            self.tossTrack = None
            tossTrack.finish()
        if self.pieTracks.has_key(sequence):
            pieTrack = self.pieTracks[sequence]
            del self.pieTracks[sequence]
            pieTrack.finish()
        if self.splatTracks.has_key(sequence):
            splatTrack = self.splatTracks[sequence]
            del self.splatTracks[sequence]
            splatTrack.finish()

        self.makePiePowerMeter()
        self.__piePowerMeter['value'] = power
        self.__piePowerMeter.show()
        self.__piePowerMeterSequence = sequence

        # Get a new instance of the pie collision bubble.
        pieBubble = self.getPieBubble().instanceTo(NodePath())

        # Define a function to call when the pie leaves our hand.
        # This will actually distribute the tossPie call.  We can't
        # distribute this early, because we might interrupt the pie
        # toss.
        def pieFlies(self = self, pos = pos, hpr = hpr, sequence = sequence,
                     power = power, timestamp32 = timestamp32,
                     pieBubble = pieBubble):
            self.sendUpdate('tossPie', [pos[0], pos[1], pos[2],
                                        hpr[0], hpr[1], hpr[2],
                                        sequence, power, timestamp32])
            if self.numPies != ToontownGlobals.FullPies:
                self.setNumPies(self.numPies - 1)
            base.cTrav.addCollider(pieBubble, self.pieHandler)

        toss, pie, flyPie = self.getTossPieInterval(
            pos[0], pos[1], pos[2],
            hpr[0], hpr[1], hpr[2],
            power,
            beginFlyIval = Func(pieFlies))

        pieBubble.reparentTo(flyPie)
        flyPie.setTag('pieSequence', str(sequence))

        toss = Sequence(toss)
        assert self.tossTrack == None
        self.tossTrack = toss
        toss.start()

        pie = Sequence(pie,
                       Func(base.cTrav.removeCollider, pieBubble),
                       Func(self.pieFinishedFlying, sequence))
        assert not self.pieTracks.has_key(sequence)
        self.pieTracks[sequence] = pie
        pie.start()

    def pieFinishedFlying(self, sequence):
        DistributedToon.DistributedToon.pieFinishedFlying(self, sequence)

        if self.__piePowerMeterSequence == sequence:
            self.__piePowerMeter.hide()

    def __finishPieTrack(self, sequence):
        if self.pieTracks.has_key(sequence):
            pieTrack = self.pieTracks[sequence]
            del self.pieTracks[sequence]
            pieTrack.finish()

    def __pieHit(self, entry):
        if not entry.hasSurfacePoint() or not entry.hasInto():
            # Not a collision solid we understand.  Weird.
            return
        if not entry.getInto().isTangible():
            # Just a trigger polygon.  Ignore it.
            return

        sequence = int(entry.getFromNodePath().getNetTag('pieSequence'))
        self.__finishPieTrack(sequence)

        if self.splatTracks.has_key(sequence):
            splatTrack = self.splatTracks[sequence]
            del self.splatTracks[sequence]
            splatTrack.finish()

        # The pie hit something solid.  Generate a distributed splat.

        # Check the thing we hit for a pieCode.  If it has one, it
        # gets passed along with the message.  This may mean something
        # different according to context (it may indicate, for
        # instance, the kind of target we hit).
        pieCode = 0
        pieCodeStr = entry.getIntoNodePath().getNetTag('pieCode')
        if pieCodeStr:
            pieCode = int(pieCodeStr)
        
        pos = entry.getSurfacePoint(render)
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits = 32)
        self.sendUpdate('pieSplat', [pos[0], pos[1], pos[2],
                                     sequence, pieCode,
                                     timestamp32])
        splat = self.getPieSplatInterval(pos[0], pos[1], pos[2], pieCode)

        splat = Sequence(splat,
                         Func(self.pieFinishedSplatting, sequence))
        assert not self.splatTracks.has_key(sequence)
        self.splatTracks[sequence] = splat
        splat.start()
                        
        messenger.send('pieSplat', [self, pieCode])
        messenger.send('localPieSplat', [pieCode, entry])

    def beginAllowPies(self):
        # Call this when entering a mode (e.g. walk) in which it is
        # allowable to toss pies, whether you have any pies or not.
        self.allowPies = 1
        self.updatePieButton()

    def endAllowPies(self):
        self.allowPies = 0
        self.updatePieButton()
        
    def makePiePowerMeter(self):
        from direct.gui.DirectGui import DirectWaitBar, DGG
        if self.__piePowerMeter == None:
            self.__piePowerMeter = DirectWaitBar(
                frameSize = (-0.2, 0.2, -0.03, 0.03),
                relief = DGG.SUNKEN,
                borderWidth = (0.005, 0.005),
                barColor = (0.4, 0.6, 1.0, 1),
                pos = (0, 0.1, 0.8),
                )

            self.__piePowerMeter.hide()

    def updatePieButton(self):
        from toontown.toonbase import ToontownBattleGlobals
        from direct.gui.DirectGui import DirectButton, DGG
        
        # Redraws the onscreen button for throwing pies.
        wantButton = 0
        if self.allowPies and self.numPies > 0:
            wantButton = 1

        if not launcher.getPhaseComplete(5):
            # If we haven't downloaded the pies yet, don't bother with
            # a pie button.
            wantButton = 0

        haveButton = (self.__pieButton != None)
        if not haveButton and not wantButton:
            return

        if haveButton and not wantButton:
            self.__pieButton.destroy()
            self.__pieButton = None
            self.__pieButtonType = None
            self.__pieButtonCount = None
            return
        
        if self.__pieButtonType != self.pieType:
            # We need a new icon.  Might as well get a whole new button.
            if self.__pieButton:
                self.__pieButton.destroy()
                self.__pieButton = None

        if self.__pieButton == None:
            inv = self.inventory

            if (self.pieType >= len(inv.invModels[ToontownBattleGlobals.THROW_TRACK])):
                gui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
                pieGui = gui.find('**/summons')
                pieScale = 0.1
            else:
                gui = None
                pieGui = inv.invModels[ToontownBattleGlobals.THROW_TRACK][self.pieType],
                pieScale = 0.85
            
            self.__pieButton = DirectButton(
                image = (inv.upButton,
                         inv.downButton,
                         inv.rolloverButton),
                geom = pieGui,
                text = "50",
                text_scale = 0.04,
                text_align = TextNode.ARight,
                geom_scale = pieScale,
                geom_pos = (-0.01, 0, 0),
                text_fg = Vec4(1, 1, 1, 1),
                text_pos = (0.07, -0.04),
                relief = None,
                image_color = (0, 0.6, 1, 1),
                pos = (0, 0.1, 0.9),
                )
            self.__pieButton.bind(DGG.B1PRESS, self.__beginTossPieMouse)
            self.__pieButton.bind(DGG.B1RELEASE, self.__endTossPieMouse)
            self.__pieButtonType = self.pieType
            self.__pieButtonCount = None
            if gui:
                del gui

        if self.__pieButtonCount != self.numPies:
            if self.numPies == ToontownGlobals.FullPies:
                self.__pieButton['text'] = ''
            else:
                self.__pieButton['text'] = str(self.numPies)
            self.__pieButtonCount = self.numPies

    ### BEGIN FROM LOCAL AVATAR ########################################

    def displayWhisper(self, fromId, chatString, whisperType):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This function overrides a similar function in DistributedAvatar.
        """
        sender = None
        sfx = self.soundWhisper

        # A message from clarabelle about the catalog
        if fromId == TTLocalizer.Clarabelle:
            chatString = TTLocalizer.Clarabelle + ": " + chatString
            # Play the phone ring sound instead of the pssst
            sfx = self.soundPhoneRing
        elif fromId != 0:
            sender = base.cr.identifyAvatar(fromId)

        if (whisperType == WhisperPopup.WTNormal or \
            whisperType == WhisperPopup.WTQuickTalker):
            if sender == None:
                return
            # Prefix the sender's name to the message.
            chatString = sender.getName() + ": " + chatString

        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               whisperType)
        if sender != None:
            whisper.setClickable(sender.getName(), fromId)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)

    def displaySystemClickableWhisper(self, fromId, chatString, whisperType):
        """displayPartyCanStartWhisper (self, int fromId, string chatString, int whisperType)

        Displays the party can start whisper message.
        """
        sender = None
        sfx = self.soundWhisper

        # A message from clarabelle about the catalog
        if fromId == TTLocalizer.Clarabelle:
            chatString = TTLocalizer.Clarabelle + ": " + chatString
            # Play the phone ring sound instead of the pssst
            sfx = self.soundPhoneRing
        elif fromId != 0:
            sender = base.cr.identifyAvatar(fromId)

        if (whisperType == WhisperPopup.WTNormal or \
            whisperType == WhisperPopup.WTQuickTalker):
            if sender == None:
                return
            # Prefix the sender's name to the message.
            chatString = sender.getName() + ": " + chatString

        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               whisperType)
        # this is the main difference, we know avId 0 (the system) is sending the whisper
        # but we force the whisper to be clickable anyway
        whisper.setClickable("", fromId)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)        

    def clickedWhisper(self, doId, isPlayer = None):
        """Overriden from LocalAvatar to handle the case of party can start whisper."""
        if doId > 0:
            LocalAvatar.LocalAvatar.clickedWhisper(self, doId, isPlayer)
        else:
            foundCanStart = False
            for partyInfo in self.hostedParties:
                if partyInfo.status == PartyGlobals.PartyStatus.CanStart:
                    foundCanStart = True
                    break
            if base.cr and base.cr.playGame and base.cr.playGame.getPlace() and base.cr.playGame.getPlace().fsm:
                fsm = base.cr.playGame.getPlace().fsm
                curState = fsm.getCurrentState().getName()
                if curState == 'walk':
                    if hasattr(self, "eventsPage"):
                        desiredMode = -1
                        if doId == -1:
                            desiredMode = EventsPage.EventsPage_Invited
                        elif foundCanStart:
                            desiredMode = EventsPage.EventsPage_Host
                        if desiredMode >= 0:
                            self.book.setPage(self.eventsPage)
                            self.eventsPage.setMode(desiredMode)
                            fsm.request("stickerBook")

    def loadFurnitureGui(self):
        # Make sure we are not already loaded
        if self.__furnitureGui:
            return
        # Related to the friends list button (at least, adjacent to
        # it) is the move-furniture button, which is only revealed
        # when the friends list button is revealed and we have a
        # global DistributedFurnitureManager available.
        guiModels = loader.loadModel('phase_5.5/models/gui/house_design_gui')
        # This consists of an attic frame
        self.__furnitureGui = DirectFrame(
            relief = None,
            pos = (-1.19, 0.00, 0.33),
            scale= 0.04,
            image = guiModels.find('**/attic')
            )
        # Add a roof
        DirectLabel(
            parent = self.__furnitureGui,
            relief = None,
            image = guiModels.find('**/rooftile')
            )
        # And a start button
        bMoveStartUp = guiModels.find('**/bu_attic/bu_attic_up')
        bMoveStartDown = guiModels.find('**/bu_attic/bu_attic_down')
        bMoveStartRollover = guiModels.find('**/bu_attic/bu_attic_rollover')
        DirectButton(
            parent = self.__furnitureGui,
            relief = None,
            image = [bMoveStartUp, bMoveStartDown,
                     bMoveStartRollover, bMoveStartUp],
            text = ["",TTLocalizer.HDMoveFurnitureButton,
                    TTLocalizer.HDMoveFurnitureButton],
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = (-0.3, 0, 9.4),
            command = self.__startMoveFurniture,
            )
        self.__furnitureGui.hide()
        guiModels.removeNode()

    def showFurnitureGui(self):
        # Presumably whoever is calling this is in the correct download phase
        self.loadFurnitureGui()
        self.__furnitureGui.show()

    def hideFurnitureGui(self):
        if self.__furnitureGui:
            self.__furnitureGui.hide()

    def loadClarabelleGui(self):
        # Make sure we are not already loaded
        if self.__clarabelleButton:
            return
        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        circle = guiItems.find('**/cover/blue_circle')
        icon = guiItems.find('**/cover/clarabelle')
        icon.reparentTo(circle)

        # This is the initial color of the blue circle.
        rgba = VBase4(0.71589, 0.784547, 0.974, 1.0)
        white = VBase4(1.0, 1.0, 1.0, 1.0)

        # Prevent the picture of Clarabelle from changing colors as we
        # monkey with the color of the circle.
        icon.setColor(white)
        claraXPos = 1.45
        newScale = oldScale = 0.5
        newPos = (claraXPos, 1.0, 0.37)
        if WantNewsPage:
            claraXPos  += AdjustmentForNewsButton
            oldPos = (claraXPos, 1.0, 0.37),
            newScale = oldScale * ToontownGlobals.NewsPageScaleAdjust
            newPos = (claraXPos - 0.1, 1.0, 0.45)
            
        self.__clarabelleButton = DirectButton(
            relief = None,
            image = circle,
            text = "",
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = 0.10,
            text_pos = (-1.06, 1.06),
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = newPos,
            scale = newScale,
            command = self.__handleClarabelleButton,
            )

        # Give it a sort of 1 so it appears on top of the
        # CatalogNotifyDialog.
        self.__clarabelleButton.reparentTo(aspect2d, 1)

        # Set up an interval to flash the circle slowly to catch the
        # player's attention.
        button = self.__clarabelleButton.stateNodePath[0]

        self.__clarabelleFlash = Sequence(
            LerpColorInterval(button, 2, white, blendType='easeInOut'),
            LerpColorInterval(button, 2, rgba, blendType='easeInOut')
            )

        # Start it looping, but pause it, so we can resume/pause it to
        # start/stop the flashing.
        self.__clarabelleFlash.loop()
        self.__clarabelleFlash.pause()

    def showClarabelleGui(self, mailboxItems):
        # Presumably whoever is calling this is in the correct download phase
        self.loadClarabelleGui()
        if mailboxItems:
            self.__clarabelleButton['text'] = ["",TTLocalizer.CatalogNewDeliveryButton,TTLocalizer.CatalogNewDeliveryButton]
        else:
            self.__clarabelleButton['text'] = ["",TTLocalizer.CatalogNewCatalogButton,TTLocalizer.CatalogNewCatalogButton]

        # double check if it's just mail
        if not self.mailboxNotify and \
           not self.awardNotify and \
           (self.catalogNotify == ToontownGlobals.OldItems) and \
           ((self.simpleMailNotify != ToontownGlobals.NoItems) or (self.inviteMailNotify != ToontownGlobals.NoItems)):
            self.__clarabelleButton['text'] = ["",TTLocalizer.MailNewMailButton,
                                               TTLocalizer.MailNewMailButton]
        
        self.__clarabelleButton.show()
        self.__clarabelleFlash.resume()

    def hideClarabelleGui(self):
        if self.__clarabelleButton:
            self.__clarabelleButton.hide()
            self.__clarabelleFlash.pause()

    def __handleClarabelleButton(self):
        place = base.cr.playGame.getPlace()
        if place == None:
            self.notify.warning("Tried to go home, but place is None.")
            return
        if self.__catalogNotifyDialog:
            self.__catalogNotifyDialog.cleanup()
            self.__catalogNotifyDialog = None
        place.goHomeNow(self.lastHood)

    def __startMoveFurniture(self):
        if self.cr.furnitureManager != None:
            self.cr.furnitureManager.d_suggestDirector(self.doId)
        elif self.furnitureManager != None:
            self.furnitureManager.d_suggestDirector(self.doId)

    def stopMoveFurniture(self):
        if self.furnitureManager != None:
            self.furnitureManager.d_suggestDirector(0)

    def setFurnitureDirector(self, avId, furnitureManager):
        # This method is called by the furniture manager.
        if avId == 0:
            # No one is the furniture director.
            if self.furnitureManager == furnitureManager:
                messenger.send('exitFurnitureMode', [furnitureManager])
                self.furnitureManager = None
                self.furnitureDirector = None

        elif avId != self.doId:
            # Someone else is the furniture director.
            if self.furnitureManager == None or \
               self.furnitureDirector != avId:
                self.furnitureManager = furnitureManager
                self.furnitureDirector = avId
                messenger.send('enterFurnitureMode', [furnitureManager, 0])

        else:  # avId == self.doId
            # We are the furniture director.
            if self.furnitureManager != None:
                messenger.send('exitFurnitureMode', [self.furnitureManager])
                self.furnitureManager = None
            self.furnitureManager = furnitureManager
            self.furnitureDirector = avId
            messenger.send('enterFurnitureMode', [furnitureManager, 1])

        self.refreshOnscreenButtons()

    def getAvPosStr(self):
        pos = self.getPos()
        hpr = self.getHpr()
        serverVersion = base.cr.getServerVersion()
        districtName = base.cr.getShardName(base.localAvatar.defaultShard)
        # See if you are in the town
        if (hasattr(base.cr.playGame.hood, "loader") and
            hasattr(base.cr.playGame.hood.loader, "place") and
            (base.cr.playGame.getPlace() != None)):
            zoneId = base.cr.playGame.getPlace().getZoneId()
        else:
            zoneId = "?"
        strPosCoordText = "X: %.3f" % pos[0] + ", Y: %.3f" % pos[1] + \
                          "\nZ: %.3f" % pos[2] + ", H: %.3f" % hpr[0] + \
                          "\nZone: %s" % str(zoneId) + ", Ver: %s, " % serverVersion + \
                          "District: %s" % districtName
        return strPosCoordText
        self.refreshOnscreenButtons()

    def thinkPos(self):
        """
        display the current position in a thought balloon
        """
        pos = self.getPos()
        hpr = self.getHpr()
        serverVersion = base.cr.getServerVersion()
        districtName = base.cr.getShardName(base.localAvatar.defaultShard)
        # See if you are in the town
        if (hasattr(base.cr.playGame.hood, "loader") and
            hasattr(base.cr.playGame.hood.loader, "place") and
            (base.cr.playGame.getPlace() != None)):
            zoneId = base.cr.playGame.getPlace().getZoneId()
        else:
            zoneId = "?"

        strPos = "(%.3f" % pos[0] + "\n %.3f" % pos[1] + "\n %.3f)" % pos[2] + \
                 "\nH: %.3f" % hpr[0] + \
                 "\nZone: %s" % str(zoneId) + ",\nVer: %s, " % serverVersion + \
                 "\nDistrict: %s" % districtName
                 # We don't really need to see the PR, and
                 # it just clutters up the display.
                 #"\nP: %.3f" % hpr[1] + "\nR: %.3f" % hpr[2]

        # print to log too
        print "Current position=",strPos.replace('\n', ', ')

        self.setChatAbsolute(strPos, CFThought | CFTimeout)

        #                             relief = None)
        # make sure it appears in front of arrows and other gui items
        #self.CoordText.setBin("gui-popup",0)

    def __placeMarker(self):
        # for treasure placement, etc.
        pos = self.getPos()
        hpr = self.getHpr()
        #print '(%d, %d, %0.1f),' % (pos[0], pos[1], pos[2])
        # print '(%0.1f, %0.1f, %0.1f, %0.1f, %0.1f, %0.1f),' % \
        #      (pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
        chest = loader.loadModel("phase_4/models/props/coffin")
        chest.reparentTo(render)
        chest.setColor(1, 0, 0, 1)
        chest.setPosHpr(pos, hpr)
        chest.setScale(0.5)

    ### Button to open up the friends list. ###

    def setFriendsListButtonActive(self, active):
        """setFriendsListButtonActive(self, bool active)

        Sets whether the friends list button should be 'active' or
        not; i.e. the game is in a state that it can accept it (like
        walk mode).  The button will be revealed only when it is both
        'active' and not obscured.
        """
        self.friendsListButtonActive = active
        self.refreshOnscreenButtons()

    def obscureFriendsListButton(self, increment):
        """obscureFriendsListButton(self, int increment)

        Increments or decrements the obscuration count for the friends
        list button.  When this count is greater than zero, the button
        is considered obscured, and will not be revealed even if it is
        active.

        The increment value is the amount to add, which should
        generally be either 1 or -1.
        """
        self.friendsListButtonObscured += increment
        self.refreshOnscreenButtons()

    def obscureMoveFurnitureButton(self, increment):
        """obscureMoveFurnitureButton(self, int increment)

        Increments or decrements the obscuration count for the
        move-furniture button.  When this count is greater than zero,
        the button is considered obscured, and will not be revealed
        even if it is active.

        The increment value is the amount to add, which should
        generally be either 1 or -1.
        """
        self.moveFurnitureButtonObscured += increment
        self.refreshOnscreenButtons()

    def obscureClarabelleButton(self, increment):
        """obscureClarabelleButton(self, int increment)

        Increments or decrements the obscuration count for the
        clarabelle button.  When this count is greater than zero, the
        button is considered obscured, and will not be revealed even
        if it is active.

        Note that the Clarabelle button is also automatically obscured
        whenever the friends list button is obscured, regardless of
        the setting of this flag.

        The increment value is the amount to add, which should
        generally be either 1 or -1.
        """
        self.clarabelleButtonObscured += increment
        self.refreshOnscreenButtons()

    def refreshOnscreenButtons(self):
        #print ("sanity")
        #print self.mailboxNotify
        self.bFriendsList.hide()
        self.hideFurnitureGui()
        self.hideClarabelleGui()
        clarabelleHidden = 1

        self.ignore(ToontownGlobals.FriendsListHotkey)
#        import pdb; pdb.set_trace()
        
        if self.friendsListButtonActive and \
           self.friendsListButtonObscured <= 0:
            self.bFriendsList.show()
            self.accept(ToontownGlobals.FriendsListHotkey, self.sendFriendsListEvent)

            if self.clarabelleButtonObscured <= 0 and self.isTeleportAllowed():
                if self.catalogNotify == ToontownGlobals.NewItems or \
                   self.mailboxNotify == ToontownGlobals.NewItems or \
                   self.simpleMailNotify == ToontownGlobals.NewItems or \
                   self.inviteMailNotify == ToontownGlobals.NewItems or \
                   self.awardNotify == ToontownGlobals.NewItems:
                    # There are new items at the phone or in the mailbox.
                    # Show a Clarabelle button we can click on to go home
                    # and check it out.
                    showClarabelle = not launcher or launcher.getPhaseComplete(5.5)
                    # also make sure we do not pop-up the panel if we are early
                    # in the game
                    for quest in self.quests:
                        if quest[0] in Quests.PreClarabelleQuestIds and \
                           ((self.mailboxNotify != ToontownGlobals.NewItems) and (self.awardNotify != ToontownGlobals.NewItems)):
                            showClarabelle = 0
                    if showClarabelle:
                        newItemsInMailbox = self.mailboxNotify == ToontownGlobals.NewItems or \
                                            self.awardNotify == ToontownGlobals.NewItems
                        self.showClarabelleGui( newItemsInMailbox)
                        clarabelleHidden = 0

        if clarabelleHidden:
            # If we have to hide the clarabelle button, then we can't
            # show the catalog notification either.
            if self.__catalogNotifyDialog:
                self.__catalogNotifyDialog.cleanup()
                self.__catalogNotifyDialog = None
        else:
            # Otherwise, show it if there's a new one.
            self.newCatalogNotify()

        if self.moveFurnitureButtonObscured <= 0:
            if self.furnitureManager != None and \
               self.furnitureDirector == self.doId:

                # We have entered furniture moving mode.  The
                # move-furniture button should be hidden (because the
                # furniture gui is there instead).

                # However, when furniture mode is done, it will scale
                # the move-furniture button back down to its normal
                # size (below).  Until then, scale it up to match the
                # scale of the furniture gui.

                # Make sure we are loaded
                self.loadFurnitureGui()

                self.__furnitureGui.setPos(-1.16,0,-0.03)
                self.__furnitureGui.setScale(0.06)

            elif self.cr.furnitureManager != None:
                # We are not in furniture moving mode, but we are
                # standing in our own house.  The move-furniture
                # button should be visible.

                self.showFurnitureGui()

                # Scale down button to default size.
                taskMgr.remove('lerpFurnitureButton')
                self.__furnitureGui.lerpPosHprScale(
                    pos = Point3(-1.19, 0.00, 0.33),
                    hpr = Vec3(0.00, 0.00, 0.00),
                    scale = Vec3(0.04, 0.04, 0.04),
                    time = 1.0, blendType = 'easeInOut',
                    task = 'lerpFurnitureButton')
        #print ("End refreshOnscreenButtons")

        if hasattr(self,'inEstate') and self.inEstate:
            self.loadGardeningGui()
            self.hideGardeningGui()
        else:
            self.hideGardeningGui()

    def setGhostMode(self, flag):
        if flag == 2:
            # ghost mode 2 indicates a magic word.
            self.seeGhosts = 1
        DistributedToon.DistributedToon.setGhostMode(self, flag)
        
    def newCatalogNotify(self):
        #print("start newCatalogNotify")
        if not self.gotCatalogNotify:
            # No undelivered catalog notify message.
            return

        hasPhase = not launcher or launcher.getPhaseComplete(5.5)
        if not hasPhase:
            # We have to wait; the phase isn't ready yet.
            return

        if not self.friendsListButtonActive or \
           self.friendsListButtonObscured > 0:
            # The friends list button is obscured or otherwise
            # unavailable, so that general region of the screen isn't
            # available yet.
            return

        # Ok, we're processing the new notify message now.
        self.gotCatalogNotify = 0

        currentWeek = self.catalogScheduleCurrentWeek - 1
        if currentWeek < 57:
            seriesNumber = currentWeek / ToontownGlobals.CatalogNumWeeksPerSeries + 1
            weekNumber = currentWeek % ToontownGlobals.CatalogNumWeeksPerSeries + 1
        # Catalog Series 5 & 6 are short. Need some special math here.
        elif currentWeek < 65: 
            seriesNumber = 6
            weekNumber = (currentWeek - 56)
        # All catalogs after 5 & 6 now need to get bumped up by
        # one since the last 13 weeks used two series numbers.
        else:
            seriesNumber = currentWeek / ToontownGlobals.CatalogNumWeeksPerSeries + 2
            weekNumber = currentWeek % ToontownGlobals.CatalogNumWeeksPerSeries + 1

        message = None
        if self.mailboxNotify == ToontownGlobals.NoItems:
            # Nothing in the mailbox.
            if self.catalogNotify == ToontownGlobals.NewItems:
                # New catalog!
                if self.catalogScheduleCurrentWeek == 1:
                    message = (TTLocalizer.CatalogNotifyFirstCatalog,
                               TTLocalizer.CatalogNotifyInstructions)
                else:
                    message = (TTLocalizer.CatalogNotifyNewCatalog % (weekNumber),)

        elif self.mailboxNotify == ToontownGlobals.NewItems:
            # A new delivery in the mailbox.
            if self.catalogNotify == ToontownGlobals.NewItems:
                # A new delivery, *and* a new catalog!
                message = (TTLocalizer.CatalogNotifyNewCatalogNewDelivery % (weekNumber),)
            else:
                # Just a new delivery.
                message = (TTLocalizer.CatalogNotifyNewDelivery,)

        elif self.mailboxNotify == ToontownGlobals.OldItems:
            # Old, unclaimed items in the mailbox.
            if self.catalogNotify == ToontownGlobals.NewItems:
                # And a new catalog!
                message = (TTLocalizer.CatalogNotifyNewCatalogOldDelivery % (weekNumber),)
            else:
                # Just a new delivery.
                message = (TTLocalizer.CatalogNotifyOldDelivery,)

        if self.awardNotify == ToontownGlobals.NoItems:
            # nothing in award mailbox
            pass
        elif self.awardNotify == ToontownGlobals.NewItems:
            # A new award delivery in the mailbox
            oldStr =''
            if message:
                oldStr = message[0] + ' '
            oldStr += TTLocalizer.AwardNotifyNewItems
            message = (oldStr,)
        elif self.awardNotify == ToontownGlobals.OldItems:
            oldStr =''
            if message:
                oldStr = message[0] + ' '
            oldStr += TTLocalizer.AwardNotifyOldItems
            message = (oldStr,)

        if ((self.simpleMailNotify == ToontownGlobals.NewItems) or (self.inviteMailNotify == ToontownGlobals.NewItems)):
            oldStr = ''
            if message:
                oldStr = message[0] + ' '
            oldStr += TTLocalizer.MailNotifyNewItems
            message = (oldStr,)

        if message == None:
            # Nothing to report.
            return

        # Create a dialog to tell the user what's up.
        if self.__catalogNotifyDialog:
            self.__catalogNotifyDialog.cleanup()
        self.__catalogNotifyDialog = CatalogNotifyDialog.CatalogNotifyDialog(message)
        base.playSfx(self.soundPhoneRing)
        #print("end newCatalogNotify")

    def allowHardLand(self):
        retval = LocalAvatar.LocalAvatar.allowHardLand(self)
        return (retval and (not self.isDisguised))
        
    def setShovelGuiLevel(self, level = 0):
        return
        
    def setWateringCanGuiLevel(self, level = 0):
        return

    def loadGardeningGui(self):
        # Make sure we are not already loaded
        if self.__gardeningGui:
            return
        # Related to the friends list button (at least, adjacent to
        # it) is the move-furniture button, which is only revealed
        # when the friends list button is revealed and we have a
        # global DistributedFurnitureManager available.
        # This consists of an attic frame
        
        gardenGuiCard = loader.loadModel("phase_5.5/models/gui/planting_gui")

        self.__gardeningGui = DirectFrame(
            relief = None,
            geom = gardenGuiCard,
            geom_color = GlobalDialogColor,
            #geom_scale = (12, 1, 3),
            geom_scale=(0.17,1.0,0.3),
            #pos = (0, 0, 0.8),
            pos = (-1.2, 0, 0.50),
            #scale = 0.1,
            scale = 1.0,

            )
        self.__gardeningGui.setName('gardeningFrame')
        
        
        self.__gardeningGuiFake = DirectFrame(
            relief = None,
            geom = None,
            geom_color = GlobalDialogColor,
            #geom_scale = (12, 1, 3),
            geom_scale=(0.17,1.0,0.3),
            #pos = (0, 0, 0.8),
            pos = (-1.2, 0, 0.50),
            #scale = 0.1,
            scale = 1.0,

            )
        self.__gardeningGuiFake.setName('gardeningFrameFake')
        
        iconScale = 1
        iconColorWhite = Vec4(1.0,1.0,1.0,1.0)   
        iconColorGrey = Vec4(0.7,0.7,0.7,1.0)
        iconColorBrown = Vec4(0.7,0.4,0.3,1.0)   
        iconColorBlue = Vec4(0.2,0.3,1.0,1.0)  
        
        shovelCardP = loader.loadModel("phase_5.5/models/gui/planting_but_shovel_P")
        shovelCardY = loader.loadModel("phase_5.5/models/gui/planting_but_shovel_Y")
        
        wateringCanCardP = loader.loadModel("phase_5.5/models/gui/planting_but_can_P")
        wateringCanCardY = loader.loadModel("phase_5.5/models/gui/planting_but_can_Y")
        
        backCard = loader.loadModel("phase_5.5/models/gui/planting_gui")
        
        iconImage = None
        iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
        iconGeom = iconModels.find('**/fish')
        
        buttonText = TTLocalizer.GardeningPlant 


        self.shovelText = ("","",buttonText,"")          
        self.__shovelButtonFake = DirectLabel(
            parent = self.__gardeningGuiFake,
            relief = None,
            #frameSize = (-0.575, 0.575, -0.575, 0.575),
            #borderWidth = (0.05,0.05),
            text = self.shovelText,
            text_align = TextNode.ALeft,
            text_pos = (0.0,-0.0),
            text_scale = 0.07,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            #image = (shovelCardP, shovelCardY, shovelCardY, shovelCardY),
            image_scale = (0.18, 1.0, 0.36),
            geom = None,
            geom_scale = iconScale,
            geom_color = iconColorWhite, 
            pos = (0.15, 0, 0.20),
            scale = 0.775,
            #command = None
            )
        self.shovelButtonFake = self.__shovelButtonFake
        

        
        self.shovelText = ("","",buttonText,"")          
        self.__shovelButton = DirectButton(
            parent = self.__gardeningGui,
            relief = None,
            #frameSize = (-0.575, 0.575, -0.575, 0.575),
            #borderWidth = (0.05,0.05),
            text = self.shovelText,
            text_align = TextNode.ACenter,
            text_pos = (0.0,-0.0),
            text_scale = 0.1,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            image = (shovelCardP, shovelCardY, shovelCardY, shovelCardY),
            image_scale = (0.18, 1.0, 0.36),
            geom = None,
            geom_scale = iconScale,
            geom_color = iconColorWhite, 
            pos = (0, 0, 0.20),
            scale = 0.775,
            command = self.__shovelButtonClicked)
        self.shovelButton = self.__shovelButton
        
        iconGeom = iconModels.find('**/teleportIcon')   
        
        buttonText = TTLocalizer.GardeningWater
        self.waterText = (buttonText,buttonText,buttonText,"")      
        
        self.__wateringCanButtonFake = DirectLabel(
            parent = self.__gardeningGuiFake,
            relief = None,
            #frameSize = (-0.575, 0.575, -0.575, 0.575),
            #borderWidth = (0.05,0.05),
            text = self.waterText,
            text_align = TextNode.ALeft,
            text_pos = (0.0,-0.0),
            text_scale = 0.07,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            #image = (wateringCanCardP, wateringCanCardY, wateringCanCardY, wateringCanCardY),
            image_scale = (0.18, 1.0, 0.36),
            geom = None,
            geom_scale = iconScale,
            geom_color = iconColorWhite, 
            pos = (0.15, 0, 0.01),
            scale = 0.775,
            #command = None
            )
        self.wateringCanButtonFake = self.__wateringCanButtonFake 


        self.__wateringCanButton = DirectButton(
            parent = self.__gardeningGui,
            relief = None,
            #frameSize = (-0.575, 0.575, -0.575, 0.575),
            #borderWidth = (0.05,0.05),
            text = self.waterText,
            text_align = TextNode.ACenter,
            text_pos = (0.0,-0.0),
            text_scale = 0.1,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            image = (wateringCanCardP, wateringCanCardY, wateringCanCardY, wateringCanCardY),
            image_scale = (0.18, 1.0, 0.36),
            geom = None,
            geom_scale = iconScale,
            geom_color = iconColorWhite, 
            pos = (0, 0, 0.01),
            scale = 0.775,
            command = self.__wateringCanButtonClicked
            )
        self.wateringCanButton = self.__wateringCanButton 
        

            
        self.basketText = ("%s / %s" % (self.numFlowers, self.maxFlowerBasket))
            
        self.basketButton = DirectLabel(
            parent = self.__gardeningGui,
            relief = None,
            #frameSize = (-0.575, 0.575, -0.575, 0.575),
            #borderWidth = (0.05,0.05),
            text = (self.basketText),
            text_align = TextNode.ALeft,
            text_pos = (0.82,-1.4),
            text_scale = 0.2,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            image = None,
            image_scale = iconScale,
            geom = None,
            geom_scale = iconScale,
            geom_color = iconColorWhite,
            pos = (-0.34, 0, 0.16),
            scale = 0.3,
            textMayChange = 1,
            )
            

        if hasattr(self, 'shovel'):
            self.setShovelGuiLevel(self.shovel)
        if hasattr(self, 'wateringCan'):
            self.setWateringCanGuiLevel(self.wateringCan)
            
        self.__shovelButton.hide()
        self.__wateringCanButton.hide()
        self.__shovelButtonFake.hide()
        self.__wateringCanButtonFake.hide()
        

    def changeButtonText(self, button, text):
        button["text"] = text
        #self.basketButton["text"] = self.basketText

    def resetWaterText(self):
        self.wateringCanButton["text"] = self.waterText
        
    def resetShovelText(self):
        self.shovelButton["text"] = self.holdShovelText

    def showGardeningGui(self):
        # Presumably whoever is calling this is in the correct download phase
        #import pdb; pdb.set_trace()
        self.loadGardeningGui()
        self.__gardeningGui.show()
        base.setCellsAvailable([base.leftCells[2]], 0)

    def hideGardeningGui(self):
        if self.__gardeningGui:
            self.__gardeningGui.hide()
            base.setCellsAvailable([base.leftCells[2]], 1)



    def showShovelButton(self, add = 0):
        """
        also make sure our parent is shown, otherwise we won't show
        """
        if add:
            self.shovelButtonActiveCount += add
        else:
            self.showingShovel = 1
        
        self.notify.debug("showing shovel %s" % (self.shovelButtonActiveCount))
        self.__gardeningGui.show()
        self.__shovelButton.show()


    def hideShovelButton(self, deduct = 0):
        self.shovelButtonActiveCount -= deduct
        if deduct == 0:
            self.showingShovel = 0
        if self.shovelButtonActiveCount < 1:
            self.shovelButtonActiveCount = 0
            if self.showingShovel == 0:
                self.__shovelButton.hide()
            self.handleAllGardeningButtonsHidden()
        self.notify.debug("hiding shovel %s" % (self.shovelButtonActiveCount))
        
    # the watering buttons needs to be merged with Pappy's code, potential conflict here
    def showWateringCanButton(self, add = 0):
        """
        also make sure our parent is shown, otherwise we won't show
        """
        if add:
            self.wateringCanButtonActiveCount += add
        else:
            self.showingWateringCan = 1
        self.__gardeningGui.show()
        self.__wateringCanButton.show()
        self.basketButton.show()

    def hideWateringCanButton(self, deduct = 0):
        #print("watering active count %s" % (self.wateringCanButtonActiveCount))
        self.wateringCanButtonActiveCount -= deduct
        if deduct == 0:
            self.showingWateringCan = 0
        if self.wateringCanButtonActiveCount < 1:
            wateringCanButtonActiveCount = 0
            if self.showingWateringCan == 0:
                self.__wateringCanButton.hide()
            self.handleAllGardeningButtonsHidden()
            
    def showWateringCanButtonFake(self, add = 0):
        self.__wateringCanButtonFake.show()

    def hideWateringCanButtonFake(self, deduct = 0):
        self.__wateringCanButtonFake.hide()
        
    def showShovelButtonFake(self, add = 0):
        self.__shovelButtonFake.show()

    def hideShovelButtonFake(self, deduct = 0):
        self.__shovelButtonFake.hide()
            
    def levelWater(self, change = 1):
        #print("level WAter")
        if change < 0:
            return
        self.showWateringCanButtonFake(1)
        #TODO fix +1 sticking around when another toon waters your plant
        #oldHideState = self.__wateringCanButton.isHidden()
        #self.wateringCanButtonActiveCount += 1
        if change < 1:
            changeString = TTLocalizer.GardeningNoSkill
        else:
            changeString = ("+%s %s" % (change, TTLocalizer.GardeningWaterSkill))
        #self.holdWateringCanText = TTLocalizer.GardeningWater#self.wateringCanButton["text"]
        self.waterTrack = Sequence(
                                Wait(0.0),
                                Func(self.changeButtonText, self.wateringCanButtonFake, changeString),
                                SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self),
                                Wait(1.0),
                                #Func(self.changeButtonText, self.wateringCanButtonFake, self.holdWateringCanText),
                                Func(self.hideWateringCanButtonFake, 1),
                                )
        #if oldHideState:
        #    pass
        self.waterTrack.start()
        
    def levelShovel(self, change = 1):
        #print("level SHovel")
        if change < 1:
            return
        self.showShovelButtonFake(1)
        #oldHideState = self.__shovelButton.isHidden()
        #self.shovelButtonActiveCount += 1
        if change < 1:
            changeString = TTLocalizer.GardeningNoSkill
        else:
            changeString = ("+%s %s" % (change, TTLocalizer.GardeningShovelSkill))
        #self.holdShovelText = self.shovelButton["text"]
        plant = base.cr.doId2do.get(self.shovelRelatedDoId)
        if plant:
                self.holdShovelText = plant.getShovelAction()
                
        #levelSound = globalBattleSoundCache.getSound('GUI_ballon_popup.mp3')
        #self.shovelTrack = Sequence()
        
        #self.shovelTrack.append(Wait(0.0))
        #self.shovelTrack.append(Func(self.changeButtonText, self.shovelButtonFake, changeString))
        #if levelSound:
        #        self.shovelTrack.append(SoundInterval(levelSound, node=self))
        #self.shovelTrack.append(Wait(1.0))
        #self.shovelTrack.append(Func(self.hideShovelButtonFake, 1))
        
        self.shovelTrack = Sequence(
                                Wait(0.0),
                                Func(self.changeButtonText, self.shovelButtonFake, changeString),
                                SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self),
                                Wait(1.0),
                                #Func(self.changeButtonText, self.shovelButtonFake, self.holdShovelText),
                                Func(self.hideShovelButtonFake, 1),
                                )
        
        #if oldHideState:
        #    pass
        self.shovelTrack.start()
        
    def setGuiConflict(self, con):
        self.guiConflict = con
        #print("setting Gui conflict %s" % (con))
        
    def getGuiConflict(self, con):
        return self.guiConflict
        
    def verboseState(self):
        self.lastPlaceState = "None"
        taskMgr.add(self.__expressState, "expressState", extraArgs = [])
        
    def __expressState(self, task = None):
        place = base.cr.playGame.getPlace()
        if place:
            state = place.fsm.getCurrentState()
            if state.getName() != self.lastPlaceState:
                #PRINT is okay in this case because this is magic word thing
                print("Place State Change From %s to %s" % (self.lastPlaceState, state.getName()))
                self.lastPlaceState = state.getName()#[:]
        return Task.cont
        
                                
    def addShovelRelatedDoId(self, doId):
        """
        because we can get the enter and exits of the garden plots
        in any order, we use the add and remove metaphors
        """
        if hasattr(base.cr.playGame.getPlace(), 'detectedGardenPlotDone'):
            place = base.cr.playGame.getPlace()
            state = place.fsm.getCurrentState()
            #print("estate state %s" % (state.getName()))
            if state.getName() == 'stopped':
                return
        
        self.touchingPlantList.append(doId)
        self.autoSetActivePlot()
        
    def removeShovelRelatedDoId(self,doId):
        #the if check is important, since we may have gotten the enter before the exit
        if doId in self.touchingPlantList:
            self.touchingPlantList.remove(doId)
        self.autoSetActivePlot()
          
    def autoSetActivePlot(self):
        if self.guiConflict:
            return
        if len(self.touchingPlantList) > 0:
            minDist = 10000
            minDistPlot = 0
            for plot in self.touchingPlantList:
                plant = base.cr.doId2do.get(plot)
                if plant:
                    if self.getDistance(plant) < minDist:
                        minDist = self.getDistance(plant)
                        minDistPlot = plot
                else:
                    self.touchingPlantList.remove(plot)
            if len(self.touchingPlantList) == 0:
                self.setActivePlot(None)
            else:                
                self.setActivePlot(minDistPlot)
        else:
            self.setActivePlot(None)        
        
    def setActivePlot(self, doId):
        #print("setActivePlot %s" % (doId))
        if not self.gardenStarted:
            return
        self.shovelRelatedDoId = doId
        plant = base.cr.doId2do.get(doId)
        if plant:
            self.startStareAt(plant, Point3(0,0,1))
            self.__shovelButton['state'] = DGG.NORMAL
            if not plant.canBePicked():
                self.hideShovelButton()
            else:                
                self.showShovelButton()
                self.setShovelAbility(TTLocalizer.GardeningPlant)
                if plant.getShovelAction():
                    self.setShovelAbility(plant.getShovelAction())
                    if plant.getShovelAction() == TTLocalizer.GardeningPick:
                        #print("action is picking")
                        if not plant.unlockPick():
                            #print(plant.unlockPick())
                            self.__shovelButton['state'] = DGG.DISABLED
                            self.setShovelAbility(TTLocalizer.GardeningFull)
                    else:
                        #print("action not is picking")
                        pass
                self.notify.debug("self.shovelRelatedDoId = %d" % self.shovelRelatedDoId)
                if plant.getShovelCommand():
                    self.extraShovelCommand = plant.getShovelCommand()
                    self.__shovelButton['command'] = self.__shovelButtonClicked
            if plant.canBeWatered():
                self.showWateringCanButton()
            else:
                self.hideWateringCanButton()
        else:
            #print("hiding GUI")
            self.stopStareAt()
            self.shovelRelatedDoId = 0
            if self.__shovelButton:
                self.__shovelButton['command'] = None
                self.hideShovelButton()
                self.hideWateringCanButton()
                self.handleAllGardeningButtonsHidden()
                if not self.inGardenAction:            
                    if hasattr(base.cr.playGame.getPlace(), 'detectedGardenPlotDone'):
                        place = base.cr.playGame.getPlace()
                        if place:
                            place.detectedGardenPlotDone()  
                
    def setPlantToWater(self, plantId):
        import pdb; pdb.set_trace()
        if self.plantToWater == None:
            self.plantToWater = plantId
            self.notify.debug("setting plant to water %s" % (plantId))
        
    def clearPlantToWater(self, plantId):
        #import pdb; pdb.set_trace()
        if not hasattr(self, "secondaryPlant"):
            self.secondaryWaterPlant = None
            
        if self.plantToWater == plantId:
            self.plantToWater = None    
            self.hideWateringCanButton()
            
    def hasPlant(self):
        if self.plantToWater != None:
            return 1
        else:
            return 0

    def handleAllGardeningButtonsHidden(self):
        """
        if all the buttons on the gardening gui are hidden, hide it too
        """
        somethingVisible = False
        if not self.__shovelButton.isHidden():
            somethingVisible = True

        if not self.__wateringCanButton.isHidden():
            somethingVisible = True

        if not somethingVisible:
            self.hideGardeningGui()
        
    def setShovelAbility(self, ability):
        self.shovelAbility = ability
        if self.__shovelButton:
            self.__shovelButton['text'] = ability

    def setFlowerBasket(self, speciesList, varietyList):
        DistributedToon.DistributedToon.setFlowerBasket(self, speciesList, varietyList)
        self.numFlowers = len(self.flowerBasket.flowerList)
        self.maxFlowerBasket
        if hasattr(self, "basketButton"):
            self.basketText = ("%s / %s" % (self.numFlowers, self.maxFlowerBasket))
            self.basketButton["text"] = self.basketText
            
    def setShovelSkill(self, skillLevel):
        if hasattr(self, 'shovelSkill') and hasattr(self, 'shovelButton'):
            if self.shovelSkill != None:
                self.levelShovel(skillLevel - self.shovelSkill)
        oldShovelSkill = self.shovelSkill
        DistributedToon.DistributedToon.setShovelSkill(self, skillLevel)
        if hasattr(self, 'shovel'):
            oldShovelPower = GardenGlobals.getShovelPower(self.shovel, oldShovelSkill)
            newShovelPower = GardenGlobals.getShovelPower(self.shovel, self.shovelSkill)
            almostMaxedSkill = GardenGlobals.ShovelAttributes[GardenGlobals.MAX_SHOVELS-1]['skillPts'] - 2
            if skillLevel >= GardenGlobals.ShovelAttributes[self.shovel]['skillPts']:
                self.promoteShovel()
            elif oldShovelSkill and (oldShovelPower < newShovelPower):
                #he reached a new number of slots                     
                self.promoteShovelSkill(self.shovel, self.shovelSkill)
            elif oldShovelSkill == almostMaxedSkill and \
                 newShovelPower == GardenGlobals.getNumberOfShovelBoxes():
                #he maxed gardening skill for the first time
                self.promoteShovelSkill(self.shovel, self.shovelSkill)
                
    def setWateringCanSkill(self, skillLevel):
        #if hasattr(base.cr.playGame.getPlace(), 'detectedGardenPlotDone'):
        #    place = base.cr.playGame.getPlace()
        #    if place:
        #        place.detectedGardenPlotDone()
        skillDelta = skillLevel - self.wateringCanSkill
        if skillDelta or 1:
            if hasattr(self, 'wateringCanSkill') and hasattr(self, 'wateringCanButton'):
                if self.wateringCanSkill != None:
                    self.levelWater(skillDelta)
            DistributedToon.DistributedToon.setWateringCanSkill(self, skillLevel)
            if hasattr(self, 'wateringCan'):
                if skillLevel >= GardenGlobals.WateringCanAttributes[self.wateringCan]['skillPts']:
                    self.promoteWateringCan()
        # done watering, turn the button back on
        #self.reactivateWater()
        
    def unlockGardeningButtons(self, task = None):
        #print("unlockingGardenButton")
        if hasattr(self, "_LocalToon__shovelButton"):
            try:
                self.__shovelButton['state'] = DGG.NORMAL
            except TypeError:
                self.notify.warning("Could not unlock the shovel button- Type Error")
        if hasattr(self, "_LocalToon__wateringCanButton"):
            try:
                self.__wateringCanButton['state'] = DGG.NORMAL
            except TypeError:
                self.notify.warning("Could not unlock the watering can button - Type Error")
        taskMgr.remove("unlockGardenButtons")
        return None

    def lockGardeningButtons(self, task = None):
        #print("unlockingGardenButton")
        if hasattr(self, "_LocalToon__shovelButton"):
            try:
                self.__shovelButton['state'] = DGG.DISABLED
            except TypeError:
                self.notify.warning("Could not lock the shovel button- Type Error")
        if hasattr(self, "_LocalToon__wateringCanButton"):
            try:
                self.__wateringCanButton['state'] = DGG.DISABLED
            except TypeError:
                self.notify.warning("Could not lock the watering can button - Type Error")
            
        self.accept("endPlantInteraction", self.__handleEndPlantInteraction)
        #taskMgr.doMethodLater(15, self.__handleEndPlantInteraction, "unlockGardenButtons")
        
        return None
        
    def reactivateShovel(self, task = None):
        #print("reactivatingShovel")
        if hasattr(self, "_LocalToon__shovelButton"):
            self.__shovelButton['state'] = DGG.NORMAL
        else:
            pass
            #import pdb; pdb.set_trace()
        taskMgr.remove("reactShovel")
        return None
                
    def reactivateWater(self, task = None):
        #print("reactivatingWater")
        if hasattr(self, "_LocalToon__wateringCanButton"):
            self.__wateringCanButton['state'] = DGG.NORMAL
        else:
            pass
            #import pdb; pdb.set_trace()
        taskMgr.remove("reactWater")
        return None
        
    def handleEndPlantInteraction(self, object = None, replacement = 0):
        #print "### LocalToon: handleEndPlantInteraction -> reactivateWater" 
        #self.unlockGardeningButtons()
        if not replacement:
            self.setInGardenAction(None, object)
            self.autoSetActivePlot()
        return None
        
    def __handleEndPlantInteraction(self, task = None):
        #print "### LocalToon: handleEndPlantInteraction -> reactivateWater" 
        #self.unlockGardeningButtons()
        self.setInGardenAction(None)
        self.autoSetActivePlot()
        return None

    def promoteShovelSkill(self, shovelLevel, shovelSkill):
        shovelName = GardenGlobals.ShovelAttributes[shovelLevel]['name']
        shovelBeans = GardenGlobals.getShovelPower(shovelLevel, shovelSkill)
        oldShovelBeans = GardenGlobals.getShovelPower(shovelLevel, shovelSkill - 1)        
        doPartyBall = False
        message = TTLocalizer.GardenShovelSkillLevelUp % {"shovel":shovelName,
                                                          "oldbeans":oldShovelBeans,
                                                          "newbeans":shovelBeans}
        if shovelBeans == GardenGlobals.getNumberOfShovelBoxes():
            if shovelSkill == GardenGlobals.ShovelAttributes[shovelLevel]['skillPts'] - 1:
                doPartyBall = True
                message = TTLocalizer.GardenShovelSkillMaxed % {"shovel":shovelName,
                                                                "oldbeans":oldShovelBeans,
                                                                "newbeans":shovelBeans}
        messagePos = Vec2(0,0.2)
        messageScale = 0.07
        image = loader.loadModel("phase_5.5/models/gui/planting_but_shovel_P")
        imagePos = Vec3(0,0,-0.13)
        imageScale = Vec3(0.28,0,0.56)
        
        if doPartyBall:
            go = Fanfare.makeFanfareWithMessageImage(0, base.localAvatar, 1, message,
                                                     Vec2(0,0.2), 0.08,
                                                     image, Vec3(0,0,-0.1), Vec3(0.35,0,0.7),
                                                     wordwrap =23)
            Sequence(go[0],
                     Func(go[1].show),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,0),
                                            colorScale=Vec4(1,1,1,1)),
                     Wait(10),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,1),
                                            colorScale=Vec4(1,1,1,0)),
                     Func(go[1].remove)).start()
        else:
            go = Fanfare.makePanel(base.localAvatar, 1)
            Fanfare.makeMessageBox(go, message, messagePos, messageScale, wordwrap = 24)
            Fanfare.makeImageBox(go.itemFrame, image, imagePos, imageScale)
            
            Sequence(Func(go.show),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,0),colorScale=Vec4(1,1,1,1)),Wait(10),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,1),colorScale=Vec4(1,1,1,0)),
                     Func(go.remove)).start()
        
                
    def promoteShovel(self, shovelLevel = 0):
        #GardenProgressMeter.GardenProgressMeter("shovel", shovelLevel)
        shovelName = GardenGlobals.ShovelAttributes[shovelLevel]['name']
        shovelBeans = GardenGlobals.getShovelPower(shovelLevel, 0)
        message = TTLocalizer.GardenShovelLevelUp % {"shovel":shovelName,
                                                     "oldbeans":shovelBeans - 1,
                                                     "newbeans":shovelBeans}
            
        messagePos = Vec2(0,0.2)
        messageScale = 0.07
        image = loader.loadModel("phase_5.5/models/gui/planting_but_shovel_P")
        imagePos = Vec3(0,0,-0.13)
        imageScale = Vec3(0.28,0,0.56)
        
        if 0: #shovelLevel >= (GardenGlobals.MAX_SHOVELS - 1):
            go = Fanfare.makeFanfareWithMessageImage(0, base.localAvatar, 1, message, Vec2(0,0.2), 0.08, image, Vec3(0,0,-0.1), Vec3(0.35,0,0.7))
            Sequence(go[0],Func(go[1].show),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,0),colorScale=Vec4(1,1,1,1)),Wait(5),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,1),colorScale=Vec4(1,1,1,0)),
                     Func(go[1].remove)).start()
        else:
            go = Fanfare.makePanel(base.localAvatar, 1)
            Fanfare.makeMessageBox(go, message, messagePos, messageScale, wordwrap = 24)
            Fanfare.makeImageBox(go.itemFrame, image, imagePos, imageScale)
            
            Sequence(Func(go.show),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,0),colorScale=Vec4(1,1,1,1)),Wait(10),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,1),colorScale=Vec4(1,1,1,0)),
                     Func(go.remove)).start()
        
    def promoteWateringCan(self, wateringCanlevel = 0):
        #GardenProgressMeter.GardenProgressMeter("wateringCan", wateringCanlevel)
        message = TTLocalizer.GardenWateringCanLevelUp + " \n" + GardenGlobals.WateringCanAttributes[wateringCanlevel]['name']
        messagePos = Vec2(0,0.2)
        messageScale = 0.08
        image = loader.loadModel("phase_5.5/models/gui/planting_but_can_P")
        imagePos = Vec3(0,0,-0.1)
        imageScale = Vec3(0.35,0,0.7)
        
        if wateringCanlevel >= (GardenGlobals.MAX_WATERING_CANS - 1):
            go = Fanfare.makeFanfareWithMessageImage(0, base.localAvatar, 1, message, Vec2(0,0.2), 0.08, image, Vec3(0,0,-0.1), Vec3(0.35,0,0.7))
            Sequence(go[0],Func(go[1].show),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,0),colorScale=Vec4(1,1,1,1)),Wait(5),
                     LerpColorScaleInterval(go[1],duration=0.5,startColorScale=Vec4(1,1,1,1),colorScale=Vec4(1,1,1,0)),
                     Func(go[1].remove)).start()
        else:
            go = Fanfare.makePanel(base.localAvatar, 1)
            Fanfare.makeMessageBox(go, message, messagePos, messageScale)
            Fanfare.makeImageBox(go.itemFrame, image, imagePos, imageScale)
            
            Sequence(Func(go.show),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,0),colorScale=Vec4(1,1,1,1)),Wait(5),
                     LerpColorScaleInterval(go,duration=0.5,startColorScale=Vec4(1,1,1,1),colorScale=Vec4(1,1,1,0)),
                     Func(go.remove)).start()
                     
    def setInGardenAction(self, actionObject, fromObject = None):
        if actionObject:
            #print("setting In Garden Action on %s" % (actionObject))
            self.lockGardeningButtons()
        elif fromObject:
            #print("setting Out of Garden Action from %s"  % (fromObject))
            self.unlockGardeningButtons()
        else:
            #print("setting Out of Garden Action from None")
            self.unlockGardeningButtons()
        self.inGardenAction = actionObject
        
    def __wateringCanButtonClicked(self):
        self.notify.debug ("wateringCanButtonClicked")
        if self.inGardenAction:
            return

        assert self.notify.debugStateCall(self)
        # We need the DistributedPlantBase or LocalToon to send the
        # water plant message to the AI, but not both.
        # Decided to make the plant send it, in case we have more stuff
        # to do client side
        
        # lock the toon down now
        plant = base.cr.doId2do.get(self.shovelRelatedDoId)
        if plant:
            if hasattr(plant, "handleWatering"):
                plant.handleWatering()

        # if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')    
        
    def __shovelButtonClicked(self):
        if self.inGardenAction:
            return
        self.notify.debug("shovelButtonClicked")
        assert self.notify.debugStateCall(self)
        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')

        thing = base.cr.doId2do.get(self.shovelRelatedDoId)
        
        if hasattr(self,"extraShovelCommand"):
            self.extraShovelCommand()
            #self.setInGardenAction(1, thing)
            #self.lockGardeningButtons()
        
    def setShovel(self, shovelId):
        DistributedToon.DistributedToon.setShovel(self, shovelId)
        if self.__gardeningGui:
            self.setShovelGuiLevel(shovelId)
        
    def setWateringCan(self, wateringCanId):
        DistributedToon.DistributedToon.setWateringCan(self, wateringCanId)
        if self.__gardeningGui:
            self.setWateringCanGuiLevel(wateringCanId)
            
    def setGardenStarted(self, bStarted):
        self.gardenStarted = bStarted
        if self.gardenStarted and (not self.gardenPage) and hasattr(self, "book"):
            self.loadGardenPages()
            
    def b_setAnimState(self, animName, animMultiplier=1.0, callback = None, extraArgs=[]):
        if self.wantStatePrint:
            print("Local Toon Anim State %s" % (animName))
        DistributedToon.DistributedToon.b_setAnimState(self, animName, animMultiplier, callback, extraArgs)
            
    def swimTimeoutAction(self):
        assert self == base.localAvatar
        self.ignore('wakeup')
        # This will check to see if we're actually wearing a suit before
        # doing anything
        self.takeOffSuit()
        base.cr.playGame.getPlace().fsm.request('final')
        self.b_setAnimState('TeleportOut', 1, self.__handleSwimExitTeleport, [0])
        return Task.done
        
        
    def __handleSwimExitTeleport(self, requestStatus):
        self.notify.info('closing shard...')
        base.cr.gameFSM.request('closeShard', ['afkTimeout'])
        
    def sbFriendAdd(self, id, info):
        print "sbFriendAdd"
        
    def sbFriendUpdate(self, id, info):
        print "sbFriendUpdate"
        
    def sbFriendRemove(self, id):
        print "sbFriendRemove"

    def addGolfPage( self ):
        """
        Purpose:
        
        Params: None
        Return: None
        """
        # Only show the button if the toon has played golf.
        if self.hasPlayedGolf():

            if hasattr(self, "golfPage") and self.golfPage != None:
                # The page is already loaded; never mind.
                return

            if not launcher.getPhaseComplete(6):
                # We haven't downloaded phase 6 yet; set a callback hook
                # so the pages will load when we do get phase 6.
                self.acceptOnce('phaseComplete-6', self.addGolfPage)
                return

            self.golfPage = GolfPage.GolfPage()
            self.golfPage.setAvatar( self )
            self.golfPage.load()
            self.book.addPage( self.golfPage,
                                   pageName = TTLocalizer.GolfPageTitle )

    def addEventsPage( self ):
        if hasattr(self, "eventsPage") and self.eventsPage != None:
            # The page is already loaded; never mind.
            return
        if not launcher.getPhaseComplete(4):
            # We haven't downloaded phase 4 yet; set a callback hook
            # so the pages will load when we do get phase 4.
            self.acceptOnce('phaseComplete-4', self.addEventsPage)
            return        
        self.eventsPage = EventsPage.EventsPage()
        self.eventsPage.load()
        self.book.addPage(self.eventsPage, pageName = TTLocalizer.EventsPageName)

    def addNewsPage(self):
        self.newsPage = NewsPage.NewsPage()
        self.newsPage.load()
        self.book.addPage(self.newsPage, pageName = TTLocalizer.NewsPageName)
        
    def addTIPPage(self):
        self.tipPage = TIPPage.TIPPage()
        self.tipPage.load()
        self.book.addPage(self.tipPage, pageName = TTLocalizer.TIPPageTitle)

    def setPinkSlips(self, pinkSlips):
         """Set the number of pink slips."""
         DistributedToon.DistributedToon.setPinkSlips(self, pinkSlips)
         self.inventory.updateTotalPropsText()

    def getAccountDays(self):
        """Return the number of days since the owning account has been created.
        
        Note the returned value is a float.
        """
        days = 0
        defaultDays = base.cr.config.GetInt('account-days', -1)
        if defaultDays >= 0:
            days = defaultDays        
        elif hasattr(base.cr, 'accountDays'):
            days = base.cr.accountDays
        return days
    
    def hasActiveBoardingGroup(self):
        if hasattr(localAvatar, "boardingParty") and localAvatar.boardingParty:
            return localAvatar.boardingParty.hasActiveGroup(localAvatar.doId)
        else:
            return False

    def getZoneId(self):
        return self._zoneId

    def setZoneId(self, value):
        if value == -1:
            # hopefully we get a stack trace with this
            self.notify.error("zoneId should not be set to -1, tell Redmond")
        self._zoneId = value
        
    zoneId = property(getZoneId, setZoneId)

    def systemWarning(self, warningText = "Acknowledge this system message."):
        """We got a system message that we must hit ok on."""
        self.createSystemMsgAckGui()
        self.systemMsgAckGui["text"] = warningText
        self.systemMsgAckGui.show()

    def createSystemMsgAckGui(self):
        """Safely create the system message ack gui."""
        if self.systemMsgAckGui == None or self.systemMsgAckGui.isEmpty():
            message = "o" * 100
            self.systemMsgAckGui = TTDialog.TTGlobalDialog(
                doneEvent = self.systemMsgAckGuiDoneEvent,
                message = message,
                style = TTDialog.Acknowledge,
                )
            self.systemMsgAckGui.hide()

    def hideSystemMsgAckGui(self):
        """Safely hide the system ack gui."""
        if self.systemMsgAckGui != None and not self.systemMsgAckGui.isEmpty():
            self.systemMsgAckGui.hide()

    def setSleepAutoReply(self, fromId):
        av = base.cr.identifyAvatar(fromId)
        if isinstance(av, DistributedToon.DistributedToon):
            base.localAvatar.setSystemMessage(0, TTLocalizer.sleep_auto_reply %av.getName(), WhisperPopup.WTToontownBoardingGroup)
        elif av is not None:
            self.notify.warning('setSleepAutoReply from non-toon %s' % fromId)


    def setLastTimeReadNews(self, newTime):
        self.lastTimeReadNews = newTime

    def getLastTimeReadNews(self):
        return self.lastTimeReadNews

    def isReadingNews(self):
        """Returns true if the toon is reading the news."""
        result = False
        if base.cr and base.cr.playGame and base.cr.playGame.getPlace() and hasattr(base.cr.playGame.getPlace(), 'fsm') and base.cr.playGame.getPlace().fsm:
            fsm = base.cr.playGame.getPlace().fsm
            curState = fsm.getCurrentState().getName()
            if curState == 'stickerBook' and WantNewsPage :
                if hasattr(self, 'newsPage'):
                    if self.book.isOnPage(self.newsPage):
                        result = True
        return result
