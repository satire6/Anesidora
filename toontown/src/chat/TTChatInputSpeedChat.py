"""TTChatInputSpeedChat module: contains the TTChatInputSpeedChat class"""

"""
from toontown.chat import TTChatInputSpeedChat;from otp.otpbase import OTPLocalizerEnglish;from otp.otpbase import OTPLocalizer;from otp.speedchat import SCStaticTextTerminal
reload(TTChatInputSpeedChat);reload(OTPLocalizerEnglish);reload(OTPLocalizer);reload(SCStaticTextTerminal);base.localAvatar.chatMgr.chatInputSpeedChat.createSpeedChat();base.localAvatar.chatMgr.chatInputSpeedChat.handleSpeedChatStyleChange()
"""

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.speedchat.SpeedChatTypes import *
from toontown.speedchat.TTSpeedChatTypes import *
from otp.speedchat.SpeedChat import SpeedChat
from otp.speedchat import SpeedChatGlobals
from toontown.speedchat import TTSpeedChatGlobals
from toontown.speedchat import TTSCSingingTerminal
from toontown.speedchat import TTSCIndexedTerminal
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from toontown.shtiker.OptionsPage import speedChatStyles
from toontown.toonbase import TTLocalizer
from toontown.parties.PartyGlobals import ActivityIds, DecorationIds
from toontown.toonbase import ToontownGlobals

###### see SpeedChat.py for the format of this structure ######
scStructure = [
    [OTPLocalizer.SCMenuHello,
     {100:0},{101:0},{102:0},{103:0},{104:0},{105:0},106,107,108,109],     

    [OTPLocalizer.SCMenuBye,
     # 208: put "I'll be back later" under "I'll be right back"
     # 209: put "I'll need to go soon" before "I need to go"
     # NOTE: "I need to go soon" is already a cattlelog phrase, but
     # it seems like a very useful phrase that everyone should have...
     {200:0},{201:0},{202:0},203,204,205,206,208,209,207],

    [OTPLocalizer.SCMenuHappy,
     {300:1},{301:1},{302:1},303,{304:1},305,306,307,308,
     309,310,311,{312:1},{313:1},{314:1},315],

    [OTPLocalizer.SCMenuSad,
     {400:2},{401:2},{402:2},403,404,405,406,407,408,409,410],

    [OTPLocalizer.SCMenuFriendly,
     [OTPLocalizer.SCMenuFriendlyYou,   600,601,602,603],
     [OTPLocalizer.SCMenuFriendlyILike, 700,701,702,703,704,705],
     # Have you been here before? (515) after Are you new here?
     500,501,502,503,504,505,506,507,508,509,510,515,511,512,513,514],

    [OTPLocalizer.SCMenuSorry,
     # Put oops (801) in front of sorry (800) - it looks better. Also add
     # Sorry I'm busy fishing (811) next to the other "Sorry I'm busy..."
     # phrases
     # "Sorry, I'm in a building" and "Sorry, I'm helping a friend" (812/813)
     # below "Sorry I'm busy..." phrases
     801,800,802,803,804,811,814,815,817,812,813,818,805,806,807,816,808,{809:5},810],

    [OTPLocalizer.SCMenuStinky,
     {900:3},{901:3},{902:3},{903:3},904,{905:3},907],

    [OTPLocalizer.SCMenuPlaces,
#      [OTPLocalizer.SCMenuPlacesLetsGo, 1100,1101,1111,1102,1103,1104,1105,1106,
#                                     1107,1108,1109,1110],
      [OTPLocalizer.SCMenuPlacesPlayground, 1100,1101,1105,1106,1107,1108,1109,1110,1111,1117,1125,1126],
      [OTPLocalizer.SCMenuPlacesCogs, 1102,1103,1104,1114,1115,1116,1119,1120,1121,1122,1123,1124,1127,1128,1129],
      [OTPLocalizer.SCMenuPlacesEstate, 1112,1113,1013,1118,1016],
      [OTPLocalizer.SCMenuParties, 5300, 5301, 5302, 5303],
      [OTPLocalizer.SCMenuPlacesWait, 1015,1007,1008,1010,1011,1014,1017],
     1000,1001,1002,1003,1004,1005,1006,1009,1012],

    [OTPLocalizer.SCMenuToontasks,
     [TTSCToontaskMenu, OTPLocalizer.SCMenuToontasksMyTasks],
     [OTPLocalizer.SCMenuToontasksYouShouldChoose, 1300,1301,1302,1303,1304],
     # This isn't what you need (1208) after This isn't what I'm looking for
     # I found what you need (1209) after I'm going to look for that
     [OTPLocalizer.SCMenuToontasksINeedMore, 1206,1210,1211,1212,1207,1213,1214,1215],
     1200,1201,1202,1208,1203,1209,1204,1205,],
    
    [OTPLocalizer.SCMenuBattle,
     [OTPLocalizer.SCMenuBattleGags, 1500,1501,1502,1503,1504,1505,1506,
      1401,1402,1413,],
     # put Piece of cake! and That was easy! (1407/1408) at the end
     [OTPLocalizer.SCMenuBattleTaunts, 1403,1406,1520,1521,1522,1523,
      1524,1525,1526,1407,1408,],
     [OTPLocalizer.SCMenuBattleStrategy, 1414,1550,1551,1552,1415,1553,1554,
      1555,1556,1557,1558,1559,],
     # "We can do it" (1416) before "You did it" (1404)
     1400,1416,1404,1405,1409,1410,1411,1412,],

    [OTPLocalizer.SCMenuGagShop,
     1600,1601,1602,1603,1604,1605,1606],

    {1:17}, # Yes
    {2:18}, # No
    3, # Ok
    #4 whiteList,
    ]

if hasattr(base, 'wantPets') and base.wantPets:
    scPetMenuStructure = [
        [OTPLocalizer.SCMenuPets,
         [TTSCPetTrickMenu, OTPLocalizer.SCMenuPetTricks],
         21000,21001,21002,21003,21004,21005,21006]
        ]

cfoMenuStructure = [
    [OTPLocalizer.SCMenuCFOBattleCranes,
     2100,2101,2102,2103,2104,2105,2106,2107,2108,2109,2110],
    [OTPLocalizer.SCMenuCFOBattleGoons,
     2120,2121,2122,2123,2124,2125,2126],
    2130,2131,2132,2133,1410,
    ]

cjMenuStructure = [
    2200,2201,2202,2203,2204,2205,2206,2207,2208,2209,2210,
    ]

ceoMenuStructure = [
    2300,2301,2302,2303,2304,2305,2306,2307,2312,2313,2314,2315,
    2308,2309,2310,2311,2316,2317,
    ]
    
class TTChatInputSpeedChat(DirectObject.DirectObject):
    """TTChatInputSpeedChat class: controls the SpeedChat, and generates
    SpeedChat messages"""

    DefaultSCColorScheme = SCColorScheme()

    # special methods
    def __init__(self, chatMgr):
        self.chatMgr = chatMgr

        self.whisperAvatarId = None
        self.toPlayer = 0

        # create the panel that tells the user that they don't have
        # access to an emotion yet
        buttons = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.emoteNoAccessPanel = DirectFrame(
            parent = hidden,
            relief = None,
            state = 'normal',
            text = OTPLocalizer.SCEmoteNoAccessMsg,
            frameSize = (-1,1,-1,1),
            geom = DGG.getDefaultDialogGeom(),
            geom_color = OTPGlobals.GlobalDialogColor,
            geom_scale = (.92, 1, .6),
            geom_pos = (0,0,-.08),
            text_scale = .08,
            )
        self.okButton = DirectButton(
            parent = self.emoteNoAccessPanel,
            image = okButtonImage,
            relief = None,
            text = OTPLocalizer.SCEmoteNoAccessOK,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            textMayChange = 0,
            pos = (0.0, 0.0, -0.2),
            command = self.handleEmoteNoAccessDone)

        self.insidePartiesMenu = None
        self.createSpeedChat()
        self.whiteList = None
        self.allowWhiteListSpeedChat = base.config.GetBool('white-list-speed-chat', 0)
        if self.allowWhiteListSpeedChat: 
            self.addWhiteList()

        self.factoryMenu = None
        self.kartRacingMenu = None
        self.cogMenu = None
        self.cfoMenu = None
        self.cjMenu = None
        self.ceoMenu = None
        self.golfMenu = None
        self.boardingGroupMenu = None
        self.singingGroupMenu = None
        self.aprilToonsMenu = None          
        self.carolMenu = None
        self.victoryPartiesMenu = None
        self.sillyPhaseOneMenu = None
        self.sillyPhaseTwoMenu = None
        self.sillyPhaseThreeMenu = None
        self.sillyPhaseFourMenu = None
        self.sillyPhaseFiveMenu = None
                
        if __debug__:
            base.speedChat = self.speedChat

        # listen for selection messages
        def listenForSCEvent(eventBaseName, handler, self=self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)
        listenForSCEvent(SpeedChatGlobals.SCTerminalLinkedEmoteEvent,
                         self.handleLinkedEmote)
        listenForSCEvent(SpeedChatGlobals.SCStaticTextMsgEvent,
                         self.handleStaticTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCCustomMsgEvent,
                         self.handleCustomMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteMsgEvent,
                         self.handleEmoteMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteNoAccessEvent,
                         self.handleEmoteNoAccess)
        listenForSCEvent(TTSpeedChatGlobals.TTSCToontaskMsgEvent,
                         self.handleToontaskMsg)
        listenForSCEvent(TTSpeedChatGlobals.TTSCResistanceMsgEvent,
                         self.handleResistanceMsg)
        listenForSCEvent(TTSCSingingTerminal.TTSCSingingMsgEvent,
                         self.handleSingingMsg)
        listenForSCEvent("SpeedChatStyleChange",
                         self.handleSpeedChatStyleChange)
        listenForSCEvent(TTSCIndexedTerminal.TTSCIndexedMsgEvent,
                         self.handleStaticTextMsg)
        
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['active']),
                            State.State('active',
                                        self.enterActive,
                                        self.exitActive,
                                        ['off']),
                            ],
                           # Initial state
                           'off',
                           # Final state
                           'off',
                           )
        self.fsm.enterInitialState()

    def delete(self):
        self.ignoreAll()
        self.removeWhiteList()
        self.okButton.destroy()
        self.emoteNoAccessPanel.destroy()
        del self.emoteNoAccessPanel
        self.speedChat.destroy()
        del self.speedChat
        del self.fsm
        del self.chatMgr

    def show(self, whisperAvatarId = None, toPlayer = 0):
        self.whisperAvatarId = whisperAvatarId
        self.toPlayer = toPlayer
        self.fsm.request("active")

    def hide(self):
        self.fsm.request("off")

    def createSpeedChat(self):
        # If we have them configed on, add some menus to the top of the
        # speedchat.
        structure = []
        if (launcher and not launcher.isTestServer()) or __dev__:
            # menu title will be overwritten
            structure.append([TTSCPromotionalMenu, OTPLocalizer.SCMenuPromotion])
        structure.append([SCEmoteMenu, OTPLocalizer.SCMenuEmotions])
        structure.append([SCCustomMenu, OTPLocalizer.SCMenuCustom])
        structure.append([TTSCResistanceMenu, OTPLocalizer.SCMenuResistance])
        if hasattr(base, 'wantPets') and base.wantPets:
            structure += scPetMenuStructure
        structure += scStructure
        self.createSpeedChatObject(structure)

    ### ClassicFSM STATE HANDLERS
    # 'off' state
    def enterOff(self):
        pass
    def exitOff(self):
        pass

    # 'active' state
    def enterActive(self):
        # if they click anywhere else, close up
        def handleCancel(self=self):
            self.chatMgr.fsm.request("mainMenu")
        self.accept('mouse1', handleCancel)

        # listen for any selection event from the SpeedChat menu
        def selectionMade(self=self):
            self.chatMgr.fsm.request("mainMenu")
        self.terminalSelectedEvent = self.speedChat.getEventName(
            SpeedChatGlobals.SCTerminalSelectedEvent)
        if base.config.GetBool('want-sc-auto-hide', 1):
            # We're not hiding the whole speedchat after a single phrase is selected.
            # Hence, we're not accepting self.terminalSelectedEvent any more.
            self.accept(self.terminalSelectedEvent, selectionMade)

        # set up the menu
        self.speedChat.reparentTo(aspect2dp, DGG.FOREGROUND_SORT_INDEX)
        scZ = .96
        self.speedChat.setPos(-1.05, 0, scZ)
        self.speedChat.setWhisperMode(self.whisperAvatarId != None)
        self.speedChat.enter()

    def exitActive(self):
        self.ignore('mouse1')
        self.ignore(self.terminalSelectedEvent)

        self.speedChat.exit()
        self.speedChat.reparentTo(hidden)

        self.emoteNoAccessPanel.reparentTo(hidden)

    # these handle selection messages coming from the speedchat object 
    def handleLinkedEmote(self, emoteId):
        # don't do the emote if we're whispering
        if self.whisperAvatarId is None:
            lt = base.localAvatar
            lt.b_setEmoteState(emoteId, animMultiplier=lt.animMultiplier)

    def handleStaticTextMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCChatMessage(textId)
        else:
            self.chatMgr.sendSCWhisperMessage(textId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0

    def handleSingingMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCSingingChatMessage(textId)
        else:
            self.chatMgr.sendSCSingingWhisperMessage(textId)
        self.toPlayer = 0
    
    def handleCustomMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCCustomChatMessage(textId)
        else:
            self.chatMgr.sendSCCustomWhisperMessage(textId,
                                                    self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0

    def handleEmoteMsg(self, emoteId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCEmoteChatMessage(emoteId)
        else:
            self.chatMgr.sendSCEmoteWhisperMessage(emoteId,
                                                   self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0

    def handleEmoteNoAccess(self):
        if self.whisperAvatarId is None:
            self.emoteNoAccessPanel.setPos(0,0,0)
        else:
            self.emoteNoAccessPanel.setPos(.37,0,0)
        self.emoteNoAccessPanel.reparentTo(aspect2d)

    def handleEmoteNoAccessDone(self):
        self.emoteNoAccessPanel.reparentTo(hidden)

    def handleToontaskMsg(self, taskId, toNpcId, toonProgress, msgIndex):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCToontaskChatMessage(
                taskId, toNpcId, toonProgress, msgIndex)
        else:
            self.chatMgr.sendSCToontaskWhisperMessage(
                taskId, toNpcId, toonProgress, msgIndex, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0

    def handleResistanceMsg(self, textId):
        self.chatMgr.sendSCResistanceChatMessage(textId)

    def handleSpeedChatStyleChange(self):
        # get the color scheme information
        nameKey, arrowColor, rolloverColor, frameColor = \
              speedChatStyles[base.localAvatar.getSpeedChatStyleIndex()]
        # create the new color scheme object
        newSCColorScheme = SCColorScheme(
            arrowColor=arrowColor,
            rolloverColor=rolloverColor,
            frameColor=frameColor,
            )
        # set the new color scheme
        self.speedChat.setColorScheme(newSCColorScheme)

    def createSpeedChatObject(self, structure):
        if hasattr(self, 'speedChat'):
            self.speedChat.exit()
            self.speedChat.destroy()
            del self.speedChat

        # get a speedchat object
        self.speedChat = SpeedChat(
            structure=structure,
            backgroundModelName='phase_3/models/gui/ChatPanel',
            guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChat.setScale(TTLocalizer.CISCspeedChat)
        self.speedChat.setBin('gui-popup',0)
        self.speedChat.setTopLevelOverlap(TTLocalizer.CISCtopLevelOverlap)
        self.speedChat.setColorScheme(self.DefaultSCColorScheme)
        # tell the speedchat to generate the gui elements for the entire
        # tree, so that the menu won't be chuggy the first time it's used
        self.speedChat.finalizeAll()
        
    def addFactoryMenu(self):
        if self.factoryMenu == None:
            menu = TTSCFactoryMenu()
            self.factoryMenu = SCMenuHolder(OTPLocalizer.SCMenuFactory, menu=menu)
            self.speedChat[2:2] = [self.factoryMenu]
        
    def removeFactoryMenu(self):
        if self.factoryMenu:
            i = self.speedChat.index(self.factoryMenu)
            del self.speedChat[i] 
            self.factoryMenu.destroy()
            self.factoryMenu = None

    # methods for creating Kart Racing speed chat menus
    def addKartRacingMenu(self):
        if self.kartRacingMenu == None:
            menu = TTSCKartRacingMenu()
            self.kartRacingMenu = SCMenuHolder(OTPLocalizer.SCMenuKartRacing, menu=menu)
            self.speedChat[2:2] = [self.kartRacingMenu]
        
    def removeKartRacingMenu(self):
        if self.kartRacingMenu:
            i = self.speedChat.index(self.kartRacingMenu)
            del self.speedChat[i] 
            self.kartRacingMenu.destroy()
            self.kartRacingMenu = None
            
    def addCogMenu(self, indices):
        if self.cogMenu == None:
            menu = TTSCCogMenu(indices)
            self.cogMenu = SCMenuHolder(OTPLocalizer.SCMenuCog, menu=menu)
            self.speedChat[2:2] = [self.cogMenu]
        
    def removeCogMenu(self):
        if self.cogMenu:
            i = self.speedChat.index(self.cogMenu)
            del self.speedChat[i] 
            self.cogMenu.destroy()
            self.cogMenu = None

    def addCFOMenu(self):
        if self.cfoMenu == None:
            menu = SCMenu()
            menu.rebuildFromStructure(cfoMenuStructure)
            self.cfoMenu = SCMenuHolder(OTPLocalizer.SCMenuCFOBattle, menu=menu)
            self.speedChat[2:2] = [self.cfoMenu]

    def removeCFOMenu(self):
        if self.cfoMenu:
            i = self.speedChat.index(self.cfoMenu)
            del self.speedChat[i] 
            self.cfoMenu.destroy()
            self.cfoMenu = None

    def addCJMenu(self, bonusWeight = -1):
        """
        If bonusWeight is -1, don't show the bonus weight option at all
        """
        if self.cjMenu == None:
            menu = SCMenu()
            myMenuCopy = cjMenuStructure[:]
            if bonusWeight >= 0:
                myMenuCopy.append(2211 + bonusWeight)
            menu.rebuildFromStructure(myMenuCopy)
            self.cjMenu = SCMenuHolder(OTPLocalizer.SCMenuCJBattle, menu=menu)
            self.speedChat[2:2] = [self.cjMenu]

    def removeCJMenu(self):
        if self.cjMenu:
            i = self.speedChat.index(self.cjMenu)
            del self.speedChat[i] 
            self.cjMenu.destroy()
            self.cjMenu = None

    def addCEOMenu(self):
        if self.ceoMenu == None:
            menu = SCMenu()
            menu.rebuildFromStructure(ceoMenuStructure)
            self.ceoMenu = SCMenuHolder(OTPLocalizer.SCMenuCEOBattle, menu=menu)
            self.speedChat[2:2] = [self.ceoMenu]

    def removeCEOMenu(self):
        if self.ceoMenu:
            i = self.speedChat.index(self.ceoMenu)
            del self.speedChat[i] 
            self.ceoMenu.destroy()
            self.ceoMenu = None


    def addInsidePartiesMenu(self):
        """Add the  party phrases that can be said inside a party."""
        def isActivityInParty(activityId):
            activityList = base.distributedParty.partyInfo.activityList
            for activity in activityList:
                if (activity.activityId == activityId):
                    return True
            return False
        
        def isDecorInParty(decorId):
            decorList = base.distributedParty.partyInfo.decors
            for decor in decorList:
                if (decor.decorId == decorId):
                    return True
            return False
        
        # This is the basic parties speedchat list.
        insidePartiesMenuStructure =  [ 5305, 5306, 5307, 5308, 5309 ]
        
        if self.insidePartiesMenu == None:
            menu = SCMenu()
            # Add elements to the basic list on a case by case basic.
            if hasattr(base, 'distributedParty') and base.distributedParty:
                # Add host specific speedchat elements.
                if (base.distributedParty.partyInfo.hostId == localAvatar.doId):
                    insidePartiesMenuStructure.insert(0, 5304)
                # Add Jukebox specific speedchat elements.
                if isActivityInParty(0):
                    insidePartiesMenuStructure.extend([5310, 5311])
                # Add Cannons specific speedchat elements.
                if isActivityInParty(1):
                    insidePartiesMenuStructure.append(5312)
                # Add Trampolines specific speedchat elements.
                if isActivityInParty(2):
                    insidePartiesMenuStructure.extend([5313, 5314])
                # Add Catch Game specific speedchat elements.
                if isActivityInParty(3):
                    insidePartiesMenuStructure.append(5315)
                # Add Dance Floor specific speedchat elements.
                if isActivityInParty(4):
                    insidePartiesMenuStructure.extend([5316, 5317])
                # Add Tug of War specific speedchat elements.
                if isActivityInParty(5):
                    insidePartiesMenuStructure.append(5318)
                # Add Fireworks specific speedchat elements.
                if isActivityInParty(6):
                    insidePartiesMenuStructure.extend([5319, 5320])
                # Add Decoration specific speedchat elements.
                if len(base.distributedParty.partyInfo.decors):
                    insidePartiesMenuStructure.append(5321)
                    
                    # Add Birthday Cake specific speedchat elements.
                    if isDecorInParty(3):
                        insidePartiesMenuStructure.append(5322)
                
            menu.rebuildFromStructure(insidePartiesMenuStructure)
            self.insidePartiesMenu = SCMenuHolder(OTPLocalizer.SCMenuParties, menu=menu)
            self.speedChat[2:2] =  [self.insidePartiesMenu]

    def removeInsidePartiesMenu(self):
        """Remove party phrases that can be said inside a party."""
        if self.insidePartiesMenu:
            i = self.speedChat.index(self.insidePartiesMenu)
            del self.speedChat[i] 
            self.insidePartiesMenu.destroy()
            self.insidePartiesMenu = None                    

    # methods for creating Golf speed chat menus
    def addGolfMenu(self):
        if self.golfMenu == None:
            menu = TTSCGolfMenu()
            self.golfMenu = SCMenuHolder(OTPLocalizer.SCMenuGolf, menu=menu)
            self.speedChat[2:2] = [self.golfMenu]
        
    def removeGolfMenu(self):
        if self.golfMenu:
            i = self.speedChat.index(self.golfMenu)
            del self.speedChat[i] 
            self.golfMenu.destroy()
            self.golfMenu = None
            
    # Methods for creating Boarding Group chat menus
    def addBoardingGroupMenu(self, zoneId):
        if (self.boardingGroupMenu == None):
            menu = TTSCBoardingMenu(zoneId)
            self.boardingGroupMenu = SCMenuHolder(OTPLocalizer.SCMenuBoardingGroup, menu = menu)
            self.speedChat[2:2] = [self.boardingGroupMenu]
            
    def removeBoardingGroupMenu(self):
        if self.boardingGroupMenu:
            i = self.speedChat.index(self.boardingGroupMenu)
            del self.speedChat[i]
            self.boardingGroupMenu.destroy()
            self.boardingGroupMenu = None
            
    # Methods for creating Singing chat menus
    def addSingingGroupMenu(self):
        if (self.singingGroupMenu == None):
            menu = TTSCSingingMenu()
            self.singingGroupMenu = SCMenuHolder(OTPLocalizer.SCMenuSingingGroup, menu = menu)
            self.speedChat[2:2] = [self.singingGroupMenu]
    
    def removeSingingMenu(self):
        if self.singingGroupMenu:
            i = self.speedChat.index(self.singingGroupMenu)
            del self.speedChat[i]
            self.singingGroupMenu.destroy()
            self.singingGroupMenu = None
                        
    # Methods for creating April toons' chat menus
    def addAprilToonsMenu(self):
        if (self.aprilToonsMenu == None):
            menu = TTSCAprilToonsMenu()
            self.aprilToonsMenu = SCMenuHolder(OTPLocalizer.SCMenuAprilToons, menu = menu)
            self.speedChat[3:3] = [self.aprilToonsMenu]
            
    def removeAprilToonsMenu(self):
        if self.aprilToonsMenu:
            i = self.speedChat.index(self.aprilToonsMenu)
            del self.speedChat[i]
            self.aprilToonsMenu.destroy()
            self.aprilToonsMenu = None
            
    def addSillyPhaseOneMenu(self):
        if (self.sillyPhaseOneMenu == None):
            menu = TTSCSillyPhaseOneMenu()
            self.sillyPhaseOneMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu = menu)
            self.speedChat[3:3] = [self.sillyPhaseOneMenu]
            
    def removeSillyPhaseOneMenu(self):
        if self.sillyPhaseOneMenu:
            i = self.speedChat.index(self.sillyPhaseOneMenu)
            del self.speedChat[i]
            self.sillyPhaseOneMenu.destroy()
            self.sillyPhaseOneMenu = None
    
    def addSillyPhaseTwoMenu(self):
        if (self.sillyPhaseTwoMenu == None):
            menu = TTSCSillyPhaseTwoMenu()
            self.sillyPhaseTwoMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu = menu)
            self.speedChat[3:3] = [self.sillyPhaseTwoMenu]
            
    def removeSillyPhaseTwoMenu(self):
        if self.sillyPhaseTwoMenu:
            i = self.speedChat.index(self.sillyPhaseTwoMenu)
            del self.speedChat[i]
            self.sillyPhaseTwoMenu.destroy()
            self.sillyPhaseTwoMenu = None
    
    def addSillyPhaseThreeMenu(self):
        if (self.sillyPhaseThreeMenu == None):
            menu = TTSCSillyPhaseThreeMenu()
            self.sillyPhaseThreeMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu = menu)
            self.speedChat[3:3] = [self.sillyPhaseThreeMenu]
            
    def removeSillyPhaseThreeMenu(self):
        if self.sillyPhaseThreeMenu:
            i = self.speedChat.index(self.sillyPhaseThreeMenu)
            del self.speedChat[i]
            self.sillyPhaseThreeMenu.destroy()
            self.sillyPhaseThreeMenu = None     

    def addSillyPhaseFourMenu(self):
        if (self.sillyPhaseFourMenu == None):
            menu = TTSCSillyPhaseFourMenu()
            self.sillyPhaseFourMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu = menu)
            self.speedChat[3:3] = [self.sillyPhaseFourMenu]
            
    def removeSillyPhaseFourMenu(self):
        if self.sillyPhaseFourMenu:
            i = self.speedChat.index(self.sillyPhaseFourMenu)
            del self.speedChat[i]
            self.sillyPhaseFourMenu.destroy()
            self.sillyPhaseFourMenu = None
            
    def addSillyPhaseFiveMenu(self):
        if (self.sillyPhaseFiveMenu == None):
            menu = TTSCSillyPhaseFiveMenu()
            self.sillyPhaseFiveMenu = SCMenuHolder(OTPLocalizer.SCMenuSillyHoliday, menu = menu)
            self.speedChat[3:3] = [self.sillyPhaseFiveMenu]
            
    def removeSillyPhaseFiveMenu(self):
        if self.sillyPhaseFiveMenu:
            i = self.speedChat.index(self.sillyPhaseFiveMenu)
            del self.speedChat[i]
            self.sillyPhaseFiveMenu.destroy()
            self.sillyPhaseFiveMenu = None
         
    def addCarolMenu(self):
        if (self.carolMenu == None):
            if base.cr.isPaid():
                menu = TTSCCarolMenu()
                self.carolMenu = SCMenuHolder(OTPLocalizer.SCMenuCarol, menu = menu)
                self.speedChat[3:3] = [self.carolMenu]
                
    def removeCarolMenu(self):
        if self.carolMenu:
            i = self.speedChat.index(self.carolMenu)
            del self.speedChat[i]
            self.carolMenu.destroy()
            self.carolMenu = None                
            
    def addVictoryPartiesMenu(self):
        if self.victoryPartiesMenu == None:
            menu = TTSCVictoryPartiesMenu()
            self.victoryPartiesMenu = SCMenuHolder(OTPLocalizer.SCMenuVictoryParties, menu = menu)
            self.speedChat[3:3] = [self.victoryPartiesMenu]
    
    def removeVictoryPartiesMenu(self):
        if self.victoryPartiesMenu:
            i = self.speedChat.index(self.victoryPartiesMenu)
            del self.speedChat[i]
            self.victoryPartiesMenu.destroy()
            self.victoryPartiesMenu = None
            
    # methods for creating White List chat menus
    def addWhiteList(self):
        if self.whiteList == None:
            from toontown.chat.TTSCWhiteListTerminal import TTSCWhiteListTerminal
            self.whiteList = TTSCWhiteListTerminal(4, self)
            #menu = TTSCWhiteListMenu()
            #self.whiteListMenu = SCMenuHolder(OTPLocalizer.SCMenuWhiteList, menu=menu)
            self.speedChat[1:1] = [self.whiteList]
        
    def removeWhiteList(self):
        if self.whiteList:
            i = self.speedChat.index(self.whiteList)
            del self.speedChat[i] 
            self.whiteList.destroy()
            self.whiteList = None
