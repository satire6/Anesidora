"""AvatarChooser module: contains the AvatarChooser class"""

from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import AvatarChoice
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.launcher import DownloadForceAcknowledge
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import DisplayOptions
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
#import pdb
import random


MAX_AVATARS = 6              
POSITIONS = ( Vec3(-0.840167, 0, 0.359333), Vec3(0.00933349, 0, 0.306533), Vec3(0.862, 0, 0.3293),
              Vec3(-0.863554, 0, -0.445659), Vec3(0.00999999, 0, -0.5181), Vec3(0.864907, 0, -0.445659))
              
COLORS = ( Vec4(0.917, 0.164, 0.164, 1), Vec4(0.152, 0.750, 0.258, 1), Vec4(0.598, 0.402, 0.875, 1),
           Vec4(0.133, 0.590, 0.977, 1), Vec4(0.895, 0.348, 0.602, 1), Vec4(0.977, 0.816, 0.133, 1)  )

# initialize once here to avoid recreating category every time object is created
chooser_notify = DirectNotifyGlobal.directNotify.newCategory("AvatarChooser")

class AvatarChooser(StateData.StateData):
    """
    AvatarChooser class: display a list of avatars and return the user's
    choice or let the user make a new avatar
    """

    # special methods    
    def __init__(self, avatarList, parentFSM, doneEvent):
        """
        Set-up the login screen interface and prompt for a user name
        """
        StateData.StateData.__init__(self, doneEvent)

        self.choice = None
        self.avatarList = avatarList
        self.displayOptions = None
        self.fsm = ClassicFSM.ClassicFSM('AvatarChooser',
                        [State.State('Choose',
                                self.enterChoose,
                                self.exitChoose,
                                ['CheckDownload']),
                        State.State('CheckDownload',
                                self.enterCheckDownload,
                                self.exitCheckDownload,
                                ['Choose'])],
                        # Initial state
                        'Choose',
                        # Final state
                        'Choose',
                        )
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getCurrentState().addChild(self.fsm)
        
        if __debug__:
            base.avChooser = self

    def enter(self):
        assert(chooser_notify.debug("enter()"))
        self.notify.info("AvatarChooser.enter")
        if not self.displayOptions:
            self.displayOptions = DisplayOptions.DisplayOptions()
        self.notify.info("calling self.displayOptions.restrictToEmbedded(False)")
        if base.appRunner:
            self.displayOptions.loadFromSettings()
            self.displayOptions.restrictToEmbedded(False)

        if self.isLoaded == 0:
            self.load()

        # turn off any user control
        base.disableMouse()

        # set-up screen title
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        if base.cr.loginInterface.supportsRelogin():
            self.logoutButton.show()

        # We need to put *something* in the 3-d scene graph to keep
        # the Voodoo drivers from crashing.  We'll use the background
        # panel, cleverly parenting it to the camera (instead of
        # aspect2d) at a suitable distance.
        self.pickAToonBG.reparentTo(base.camera)

        choice = base.config.GetInt("auto-avatar-choice", -1)
        
        # hang the choice panel hooks
        for panel in self.panelList:
            panel.show()
            self.accept(panel.doneEvent, self.__handlePanelDone)
            if panel.position == choice and panel.mode == AvatarChoice.AvatarChoice.MODE_CHOOSE:
                self.__handlePanelDone("chose", panelChoice=choice)

    def exit(self):
        """
        Remove event hooks and restore display
        """
        assert(chooser_notify.debug("enter()"))
        if self.isLoaded == 0:
            return None

        for panel in self.panelList:
            panel.hide()

        # remove all hooks
        self.ignoreAll()

        # reset display
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.logoutButton.hide()
        
        self.pickAToonBG.reparentTo(hidden)

    def load(self, isPaid):
        assert(chooser_notify.debug("load()"))
        if self.isLoaded == 1:
            return None

        self.isPaid = isPaid

        gui = loader.loadModel("phase_3/models/gui/pick_a_toon_gui")
        gui2 = loader.loadModel("phase_3/models/gui/quit_button")
        newGui = loader.loadModel("phase_3/models/gui/tt_m_gui_pat_mainGui")
        self.pickAToonBG = newGui.find("**/tt_t_gui_pat_background")
        self.pickAToonBG.reparentTo(hidden)
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1, 1, 1)
        
        # set-up screen title
        self.title = OnscreenText(TTLocalizer.AvatarChooserPickAToon,
                                  scale = TTLocalizer.ACtitle,
                                  parent = hidden,
                                  font = ToontownGlobals.getSignFont(),
                                  fg = (1,0.9,0.1,1),
                                  pos = (0.0, 0.82))

        quitHover = gui.find("**/QuitBtn_RLVR")
        
        self.quitButton = DirectButton(
##            image = (gui.find("**/QuitBtn_UP"), gui.find("**/QuitBtn_DN"), gui.find("**/QuitBtn_RLVR")),
            image = (quitHover, quitHover, quitHover),
            relief = None,
            text = TTLocalizer.AvatarChooserQuit,
            text_font = ToontownGlobals.getSignFont(),
##            text0_fg = (0.152, 0.750, 0.258, 1),
##            text1_fg = (0.152, 0.750, 0.258, 1),
##            text2_fg = (0.977, 0.816, 0.133, 1),
            text_fg = (0.977, 0.816, 0.133, 1),
            text_pos = (0, TTLocalizer.ACquitButton_pos),
            text_scale = TTLocalizer.ACquitButton,
            image_scale = 1,
            image1_scale = 1.05,
            image2_scale = 1.05,
            scale = 1.05,
##            pos = (0, 0, -0.924),
            pos = (1.08, 0, -0.907),
            command = self.__handleQuit,
            )

        self.logoutButton = DirectButton(
            relief = None,
            image = (quitHover, quitHover, quitHover),
##            image_scale = 1.15,
            text = TTLocalizer.OptionsPageLogout,
            text_font = ToontownGlobals.getSignFont(),
            text_fg = (0.977, 0.816, 0.133, 1),
##            text0_fg = (0.152, 0.750, 0.258, 1),
##            text1_fg = (0.152, 0.750, 0.258, 1),
##            text2_fg = (0.977, 0.816, 0.133, 1),
            text_scale = TTLocalizer.AClogoutButton,
            text_pos = (0,-0.035),
##            pos = (1.105,0,-0.924),
            pos = (-1.17,0,-0.914),
            image_scale = 1.15,
            image1_scale = 1.15,
            image2_scale = 1.18,
            scale = 0.5,
            command = self.__handleLogoutWithoutConfirm,
            )
        # initially this is hidden since it might be invisible if we
        # are logging in with a "blue" (and therefore can't log out to
        # a different user).
        self.logoutButton.hide()
        
        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()

        # create the av panels w/ avatars
        self.panelList = []
        used_position_indexs = []
        
        for av in self.avatarList:
            # decide whether or not to lock out all but one of the toon positions
            # is this a paid account?
            if base.cr.isPaid():
                okToLockout = 0
            else:
                okToLockout = 1
                # grandfather in old two toon trialers...
                if av.position in AvatarChoice.AvatarChoice.OLD_TRIALER_OPEN_POS:
                    okToLockout = 0

            panel = AvatarChoice.AvatarChoice(
                av, position = av.position, paid = isPaid,
                okToLockout = okToLockout)
            panel.setPos(POSITIONS[av.position])
            used_position_indexs.append(av.position)
            self.panelList.append(panel)

        # create the av panels w/o avatars
        for panelNum in range(0, MAX_AVATARS):
            if panelNum not in used_position_indexs:
                panel = AvatarChoice.AvatarChoice(position = panelNum, paid = isPaid)
                panel.setPos(POSITIONS[panelNum])
##                panel['image_color'] = COLORS[panelNum]
                self.panelList.append(panel)

        if(len(self.avatarList)>0):
            self.initLookAtInfo()        
        self.isLoaded = 1

        # self.avatarList not updated on av deletion, but it doesnt have to be, since on 
        # deletion or creation of a single AvatarChoice, the whole AvatarChooser obj is unloaded 
        # and re-created in ToontownClientRepository.py

    def getLookAtPosition(self, toonHead, toonidx):
        lookAtChoice = random.random()

        if(len(self.used_panel_indexs)==1):
            lookFwdPercent = 0.33
            lookAtOthersPercent = 0
        else:
            lookFwdPercent = 0.20

            if(len(self.used_panel_indexs)==2):
                lookAtOthersPercent = 0.4
            else:
                lookAtOthersPercent = 0.65

        #for i in range(MAX_AVATARS):
        #    print "[",i,"] present: ",(self.panelList[i].dna!=None),", posn: ",self.panelList[i].position

        lookRandomPercent = 1.0 - lookFwdPercent - lookAtOthersPercent

        if(lookAtChoice < lookFwdPercent):
            self.IsLookingAt[toonidx] = "f"
            return Vec3(0, 1.5, 0)
        elif(lookAtChoice < (lookRandomPercent + lookFwdPercent) or (len(self.used_panel_indexs)==1)):
            self.IsLookingAt[toonidx] = "r"
            return toonHead.getRandomForwardLookAtPoint()
        else:
            # look at other people

            # is anyone looking at me?
            other_toon_idxs = []
            for i in range(len(self.IsLookingAt)):
                if(self.IsLookingAt[i] == toonidx):
                    other_toon_idxs.append(i)

            if(len(other_toon_idxs)==1):
                IgnoreStarersPercent = 0.4
            else:
                IgnoreStarersPercent = 0.2

            NoticeStarersPercent = 0.5
            bStareTargetTurnsToMe = 0

            # if no one looking at me or rand<IgnoreStarers, look at anyone else instead of someone looking at me
            if((len(other_toon_idxs)==0) or (random.random()<IgnoreStarersPercent)):
                # delete me from the list of possible tgts
                other_toon_idxs = []
                for i in self.used_panel_indexs:
                    if(i != toonidx):
                        other_toon_idxs.append(i)

                if(random.random()<NoticeStarersPercent):
                    bStareTargetTurnsToMe = 1


            # if list of other toons empty, look foward
            if (len(other_toon_idxs)==0):
                return toonHead.getRandomForwardLookAtPoint()
            # otherwise, pick one at random toon to look at
            else:
                lookingAtIdx = random.choice(other_toon_idxs)

            if(bStareTargetTurnsToMe):
                self.IsLookingAt[lookingAtIdx] = toonidx
                otherToonHead = None
                # panelList idx is not the same idx as panel.position & toonidx !!
                # could I precompute the panel.position->panelList idx map at loadtime, 
                # or does the panelList panel order change?
                for panel in self.panelList:
                    if(panel.position == lookingAtIdx):
                        otherToonHead = panel.headModel
                otherToonHead.doLookAroundToStareAt(otherToonHead, self.getLookAtToPosVec(lookingAtIdx, toonidx))

            self.IsLookingAt[toonidx] = lookingAtIdx  
            return self.getLookAtToPosVec(toonidx,lookingAtIdx)

    def getLookAtToPosVec(self, fromIdx, toIdx):
        # for some reason 'x' component subtraction needs to be inverted, so do vec subtract manually
        x = -(POSITIONS[toIdx][0]-POSITIONS[fromIdx][0])
        y = POSITIONS[toIdx][1]-POSITIONS[fromIdx][1]
        z = POSITIONS[toIdx][2]-POSITIONS[fromIdx][2]
        return Vec3(x,y,z)

    def initLookAtInfo(self):
        self.used_panel_indexs = []

        for panel in self.panelList:
            # Note:  panel.position is NOT the same as its index in self.panelList!
            if(panel.dna != None):
                self.used_panel_indexs.append(panel.position)

        if(len(self.used_panel_indexs)==0):
            return

        # start out looking at nothing (-1)
        # "r" indicates nowhere in particular
        # "f" indicates fwd
        self.IsLookingAt = []
        for i in range(MAX_AVATARS):
            self.IsLookingAt.append("f")

        for panel in self.panelList:
            if(panel.dna != None):
                panel.headModel.setLookAtPositionCallbackArgs((self,panel.headModel,panel.position))

    def unload(self):
        assert(chooser_notify.debug("unload()"))
        if self.isLoaded == 0:
            return None

        # make sure any dialog boxes are cleaned up
        cleanupDialog("globalDialog")

        for panel in self.panelList:
            panel.destroy()
        del self.panelList

        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton

        self.logoutButton.destroy()
        del self.logoutButton

        self.pickAToonBG.removeNode()
        del self.pickAToonBG
        
        del self.avatarList

        self.parentFSM.getCurrentState().removeChild(self.fsm)
        del self.parentFSM
        del self.fsm

        self.ignoreAll()
        self.isLoaded = 0

        ModelPool.garbageCollect()
        TexturePool.garbageCollect()

    def __handlePanelDone(self, panelDoneStatus, panelChoice=0):
        """
        Take appropriate action based on panel action (choose, delete,
        or create)
        """
        assert(chooser_notify.debug("__handlePanelDone(panelDoneStatus=%s, panelChoice=%s)"%(
                panelDoneStatus, panelChoice)))
        self.doneStatus = {}
        self.doneStatus['mode'] = panelDoneStatus
        self.choice = panelChoice
        if (panelDoneStatus == 'chose'):
            self.__handleChoice()
        elif (panelDoneStatus == 'nameIt'):
            self.__handleCreate()
        elif (panelDoneStatus == 'delete'):
            self.__handleDelete()
        elif (panelDoneStatus == 'create'):
            self.__handleCreate()

    def getChoice(self):
        return self.choice

    def __handleChoice(self):
        """
        Process the choice returned from the pick list
        """
        assert(chooser_notify.debug("__handleChoice()"))
        self.fsm.request("CheckDownload")

    def __handleCreate(self):
        base.transitions.fadeOut(finishIval = EventInterval(self.doneEvent,
                                                            [self.doneStatus]))

    def __handleDelete(self):
        """
        Handle create or delete buttons
        """
        messenger.send(self.doneEvent, [self.doneStatus])

    def __handleQuit(self):
        cleanupDialog("globalDialog")
        self.doneStatus = {'mode': "exit"}
        messenger.send(self.doneEvent, [self.doneStatus])
        
    # Specific State functions

    #### Choose state ####

    def enterChoose(self):
        pass

    def exitChoose(self):
        pass

    #### CheckDownload state ####

    def enterCheckDownload(self):
        self.accept('downloadAck-response', self.__handleDownloadAck)
        self.downloadAck = DownloadForceAcknowledge.DownloadForceAcknowledge(
            'downloadAck-response')
        # We are going to check phase 4 here, even though strictly speaking
        # a new toon only has to wait for 3.5 to get into the tutorial. Most
        # new toons should go directly to the tutorial though, not come back here
        self.downloadAck.enter(4)

    def exitCheckDownload(self):
        self.downloadAck.exit()
        self.downloadAck = None
        self.ignore("downloadAck-response")

    def __handleDownloadAck(self, doneStatus):
        if (doneStatus['mode'] == 'complete'):
            base.transitions.fadeOut(finishIval = EventInterval(self.doneEvent,
                                                                [self.doneStatus]))
        else:
            # Download is not done, go back to choosing your avatar
            self.fsm.request("Choose")

    def __handleLogoutWithoutConfirm(self):
        # For exiting from the avatar chooser to the login screen.
        base.cr.loginFSM.request("login")
