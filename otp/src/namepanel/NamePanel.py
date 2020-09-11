##################################################################
# NAME PANEL CLASS
# Creates the Panel for PickAName and TypeAName 
##################################################################

from pandac.PandaModules import *

from otp.avatar import Avatar
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.fsm import StateData
#import whrandom
import random
from direct.task import Task
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.gui import OnscreenText

from otp.distributed import PotentialAvatar
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.namepanel import NameCheck
from otp.namepanel import NameTumbler
import re
import string


# Length of Name before it Wraps around to Second Line in Name Result
MAX_NAME_WIDTH = 8


###########################################
# Name Panel Class
###########################################
class NamePanel(StateData.StateData):
    """NamePanel class"""
    
    def __init__(self, listOfNames, doneEvent, usedNames):
        StateData.StateData.__init__(self, doneEvent)
            
        self.listOfNames = listOfNames
        self.doneEvent = doneEvent
        self.avId = -1

        self.tumblerList = {}

        # Keep Track of Used Names
        self.usedNames = usedNames
        
        # Get Appropriate Font
        self.interfaceFont = OTPGlobals.getInterfaceFont()
        self.signFont = OTPGlobals.getSignFont()
        self.nameEntryFont = OTPGlobals.getInterfaceFont()
          
        # Stores the Current Name String
        self.name = ""
        self.nameIsChecked = 0

        # nameAction is used later in NameShop
        # 0 = DefaultName Mode
        # 1 = PickAName Mode
        # 2 = TypeAName Mode
        self.nameAction = 0
        
        # Add an fsm to NameShop to handle PayState, PickAName, TypeAName,
        #   NameAccepted, NameRejected, and NameCouncil
        self.fsm = ClassicFSM.ClassicFSM(
            'NameShop',
            [State.State('Init',
                    self.enterInit,
                    self.exitInit,
                    ['PickAName']),
            State.State('PickAName',
                    self.enterPickANameState,
                    self.exitPickANameState,
                    ['TypeAName', 'Done']),
            State.State('TypeAName',
                    self.enterTypeANameState,
                    self.exitTypeANameState,
                    ['PickAName', 'Done']),
            State.State('Done',
                    self.enterDone,
                    self.exitDone,
                    ['Init'])],
            # Initial state
            'Init',
            # Final state
            'Done',
            )


    #---------------------------------------#
    # Main Enter and Leave Shop Functions
    #---------------------------------------#
    # Enter Shop
    def start(self):
        # Used for TypeAName
        self.avExists = 0

        # Load Interface
        self.loadInterfaceGUI()

        # Enforces Pick-A-Name's name Format
        self.accept("CheckTumblerPriority", self.__checkPriority)
        self.accept("CheckTumblerLinkage", self.__checkLinkage)
        
        # Handle Done Events
        self.accept("updateNameResult", self.__updateNameResult)

        # Enter Initial State
        self.fsm.enterInitialState()
        self.fsm.request("PickAName")
             
    # Exit Shop and Send to...
    def exit(self):
        self.ignore("CheckTumblerPriority")
        self.ignore("CheckTumblerLinkage")
            
        # Ignore Done Events
        self.ignore("updateNameResult")
        self.ignore("rejectDone")
        
        # Unload the Room
        self.unloadInterfaceGUI()
        
        
    #---------------------------------------#
    # Load Interface GUI
    #---------------------------------------#
    
    # Loads the NameShop Specific GUI Objects
    def loadInterfaceGUI(self):
        # Create Dummy Frame to Hold Everything
        # This Object gets Hidden/Shown
        self.interface = DirectFrame(
            parent = aspect2d,
            relief = 'flat',
            scale = 0.9,
            state = 'disabled',
            frameColor = (1,1,1,0),
            pos = (0, 0, 0),
            )
        self.PickAName = DirectFrame(
            parent = aspect2d,
            relief = 'flat',
            scale = 0.9,
            state = 'disabled',
            frameColor = (1,1,1,0),
            pos = (0, 0, 0),
            )
        self.PickAName.reparentTo(self.interface)
        self.TypeAName = DirectFrame(
            parent = aspect2d,
            relief = 'flat',
            scale = 0.9,
            state = 'disabled',
            frameColor = (1,1,1,0),
            pos = (0, 0, 0),
            )
        self.TypeAName.reparentTo(self.interface)
        
        # set-up name selector
        nameBalloon = loader.loadModel("phase_3/models/props/chatbox_input")
        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
      
        gui = loader.loadModel("phase_3/models/gui/nameshop_gui")
        typePanel = gui.find("**/typeNamePanel")
        
        # Random Button
        self.randomButton = DirectButton(
            parent = aspect2d,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (1,1,1),
            scale = (1, 1, 1),
            pos = (0.01, 0, -0.4),
            text = OTPLocalizer.RandomButton,
            text_scale = 0.06,
            text_pos = (0, -0.02),
            command = self.randomName,
            )
        self.randomButton.reparentTo(self.PickAName)
          
        # Button for Type-A-Name
        self.typeANameButton = DirectButton(
            parent = aspect2d,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (1,1,1),
            pos = (0.01, 0, -0.55),
            scale = (1,1,1),
            text = OTPLocalizer.TypeANameButton,
            text_scale = 0.06,
            text_pos = (0, -0.02),
            command = self.toggleNameMode,
            )
        self.typeANameButton.reparentTo(self.interface)
        
        # Displays Current Name Combo
        self.nameResult = DirectLabel(
            parent = aspect2d,
            relief = None,
            scale = 0.12,
            pos = (0, 0, 0.6),
            text = " \n ",
            text_scale = 0.8,
            text_align = TextNode.ACenter,
            text_wordwrap = MAX_NAME_WIDTH,
            )
        self.nameResult.reparentTo(self.PickAName)
        
        # Create 4 scrolled lists with different colors
        for i in range(len(self.listOfNames)):
            tPos = (i*0.4) - ((len(self.listOfNames)/2.0)*0.4) + 0.8
            self.tumblerList[i] = NameTumbler.NameTumbler(
                self.listOfNames[i][0],
                self.listOfNames[i][1], self.listOfNames[i][2],
                self.listOfNames[i][3], (1,0.80,0.80,1))
            self.tumblerList[i].tumbler.reparentTo(self.PickAName)
            self.tumblerList.setPos(tPos, 0, -0.1)
            
        #### GUI Elements for TypeAName ####      
        self.nameLabel = OnscreenText.OnscreenText(
            OTPLocalizer.PleaseTypeName,
            parent = aspect2d,
            style = OnscreenText.ScreenPrompt,
            pos = (0, 0.53))
        self.nameLabel.reparentTo(self.TypeAName)
        
        self.typeNotification = OnscreenText.OnscreenText(
            OTPLocalizer.AllNewNames,
            parent = aspect2d,
            style = OnscreenText.ScreenPrompt,
            pos = (0, 0.15))
        self.typeNotification.reparentTo(self.TypeAName)
        
        self.nameEntry = DirectEntry(
            parent = aspect2d,
            relief = None,
            scale = 0.08,
            entryFont = self.nameEntryFont,
            width = MAX_NAME_WIDTH,
            numLines = 2,
            focus = 0,
            cursorKeys = 1,
            pos = (0.0, 0.0, 0.39),
            text_align = TextNode.ACenter,
            command = self.toggleNameMode,
            )
        self.nameEntry.reparentTo(self.TypeAName)
        
        self.submitButton = DirectButton(
            parent = aspect2d,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (1.2,0,1.1),
            pos = (-0.01, 0, -0.25),
            text = OTPLocalizer.NameShopSubmitButton,
            text_scale = 0.06,
            text_pos = (0, -0.02),
            command = self.submitName,
            )
        self.submitButton.reparentTo(self.TypeAName)
        
        # Remove GUI Node
        gui.removeNode()
        nameBalloon.removeNode()
        
        # Start with a Random Name
        self.randomName()
        
    def unloadInterfaceGUI(self):
        for i in range(len(self.tumblerList)):
            self.tumblerList[i].unloadTumblerGUI()
            del self.tumblerList[i]
        self.randomButton.destroy()
        del self.randomButton
        self.typeANameButton.destroy()
        del self.typeANameButton
        self.nameResult.destroy()
        del self.nameResult
        self.nameLabel.destroy()
        del self.nameLabel
        self.typeNotification.destroy()
        del self.typeNotification
        self.nameEntry.destroy()
        del self.nameEntry
        self.submitButton.destroy()
        del self.submitButton
        self.PickAName.destroy()
        del self.PickAName
        self.TypeAName.destroy()
        del self.TypeAName
        self.interface.destroy()
        del self.interface
               
    # Toggles TypeAName Mode and PickAName Mode
    def toggleNameMode(self):
        if self.fsm.getCurrentState().getName() == 'TypeAName':
            self.typeANameButton['text'] = OTPLocalizer.TypeANameButton
            self.fsm.request("PickAName")
        else:
            self.typeANameButton['text'] = OTPLocalizer.PickANameButton
            self.fsm.request("TypeAName")

   
    #---------------------------------------#
    # Get Random Name Function
    #---------------------------------------#

    # Randomizes all the Name Tumblers and Harvests the Results
    def randomName(self):
        # Randomize Each Tumbler
        for i in range(len(self.tumblerList)):
            self.tumblerList[i].getRandomResult()
        
        # Update NameResult
        self.__updateNameResult()

        
    #---------------------------------------#
    # Update Name Result
    #---------------------------------------#

    def __updateNameResult(self):
        # Put the name in the result label
        self.nameResult['text'] = ""

        # Iterate through Tumblers and Fetch Name Values
        for i in range(len(self.tumblerList)):
            self.nameResult['text'] += self.tumblerList[i].getName()

            # Puts a space in Name Tumblers without Linkage
            if (i != len(self.tumblerList)) and (self.listOfNames[i][3] <= 0):
               self.nameResult['text'] += " "
        self.name = self.nameResult['text']

    
    #---------------------------------------#
    # Enforce Name Format in Pick-a-Name
    #---------------------------------------#

    def __checkPriority(self, category):
        value = 0
        # Check Number of Priority Names Active
        for i in self.tumblerList:
            # Count number of Active Priority Names
            if (self.tumblerList[i].priority == 1):
                value += self.tumblerList[i].isActive

        # If more than 1 Priority Name Active, permit Shutoff
        if (value > 1):
            # Figure out which Tumbler player had wanted to Deactivate
            # and shut it down
            for i in self.tumblerList:
                if (self.tumblerList[i].priority == 1) and (category == self.tumblerList[i].category):
                    self.tumblerList[i].deactivateTumbler()


    # Deactivate or Activate all Linked Tumblers
    def __checkLinkage(self, category):
        linkageValue = 0
        isActive = 0
        # Figure out which Tumbler was Interacted with
        for i in self.tumblerList:
            if (category == self.tumblerList[i].category):
                linkageValue = self.tumblerList[i].linkage
                isActive = self.tumblerList[i].isActive

        # Activate or Deactivate the Linked Tumblerlist 
        for i in self.tumblerList:
            if (self.tumblerList[i].linkage == linkageValue):
                if isActive:
                    self.tumblerList[i].activateTumbler()
                else:
                    self.tumblerList[i].deactivateTumbler()

        
    #---------------------------------------#
    # Type-A-Name Functions
    #---------------------------------------#

    def submitName(self, *args):
        self.notify.debug('__submitName')
        self.nameEntry['focus'] = 0
        self.nameIsChecked = 1
        
        # strip leading/trailing whitespace
        name = self.nameEntry.get()
        # make sure we're able to recognize unicode whitespace
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.nameEntry.enterText(name)

        # do local name checks first
        problem = self.nameIsValid(self.nameEntry.get())
        if problem:
            self.rejectName(problem)
            return
        if not self.avExists:
            self.nameAction = 2
            # Create Avatar
            messenger.send("namePanel-Done")
        else:
            self.checkNameTyped()


    # Checks to see if Submitted Name is ok Locally    
    def nameIsValid(self, name):
        """nameIsValid(self, string name)
        Checks the name for legitimacy according to our various
        Toontown rules.  If it violates any of those rules, returns a
        string explaining the objection; otherwise, returns None
        indicating the name is acceptable.
        """
        self.notify.debug('nameIsValid')
        if (name in self.usedNames):
            return OTPLocalizer.ToonAlreadyExists % (name)

        problem = NameCheck.checkName(name, font=self.nameEntry.getFont())
        if problem:
            return problem

        # name has passed local checks
        return None

    
    #---------------------------------------#
    # Reject Name Functions
    #---------------------------------------#
    
    def rejectName(self, str):
        self.notify.debug('rejectName')
        self.name = ""
        self.nameIsChecked = 0
        # OTPDialog crashes when imported because it cannot find
        # gui geometry.  Instead, inherit from NamePanel and override this.
        #self.rejectDialog = OTPDialog.GlobalDialog(
        #    doneEvent = "rejectDone",
        #    message = str,
        #    style = OTPDialog.Acknowledge)
        #self.rejectDialog.show()
        self.acceptOnce("rejectDone", self.__handleReject)

    def __handleReject(self):
        self.rejectDialog.cleanup()
        self.nameEntry['focus'] = 1

        
    #---------------------------------------#
    # Define FSM
    #---------------------------------------#
    
    # Specific State functions
    ##### Init state #####
    def enterInit(self):
        self.notify.debug('enterInit')
        self.TypeAName.hide()
        self.PickAName.hide()
    def exitInit(self):
        pass
    
    ##### PickAName state #####
    def enterPickANameState(self):
        self.notify.debug('enterPickANameState')
        self.nameAction = 1
        self.PickAName.show()
        self.randomName()

    def exitPickANameState(self):
        self.PickAName.hide()
        
    ##### TypeAName state ##### 
    def enterTypeANameState(self):
        self.notify.debug('enterTypeANameState')
        self.TypeAName.show()
        self.nameEntry.set("")
        self.nameEntry['focus'] = 1
        
    def exitTypeANameState(self):
        self.TypeAName.hide()
        
    ##### Done state #####
    def enterDone(self):
        self.notify.debug('enterDone')

    def exitDone(self):
        pass
