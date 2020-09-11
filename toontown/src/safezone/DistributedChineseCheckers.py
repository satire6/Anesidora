from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer

from direct.distributed import DistributedNode
from direct.distributed.ClockDelta import globalClockDelta
from ChineseCheckersBoard import ChineseCheckersBoard
from direct.fsm import ClassicFSM, State
from direct.fsm import StateData
from toontown.distributed import DelayDelete

from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *

from otp.otpbase import OTPGlobals


from direct.showbase import PythonUtil

class DistributedChineseCheckers(DistributedNode.DistributedNode):
    def __init__(self, cr):
        NodePath.__init__(self, "DistributedChineseCheckers")
        DistributedNode.DistributedNode.__init__(self,cr)
        self.cr = cr

        self.reparentTo(render)
        self.boardNode = loader.loadModel("phase_6/models/golf/checker_game.bam")
        self.boardNode.reparentTo(self)
        #self.boardNode.setZ(2.85)
        #self.boardNode.setZ(3.5)
        #self.boardNode.setZ(0.3)
        #self.boardNode.setZ(self.getZ())
        
        self.board = ChineseCheckersBoard()

        self.playerTags = render.attachNewNode("playerTags")
        self.playerTagList = []

        #game variables
        self.exitButton = None
        self.inGame = False
        self.waiting = True
        self.startButton = None
        self.playerNum = None
        self.turnText = None
        self.isMyTurn = False
        self.wantTimer = True
        self.leaveButton = None
        self.screenText = None
        self.turnText = None
        self.exitButton = None
        self.numRandomMoves = 0
        self.blinker = Sequence()
        self.playersTurnBlinker = Sequence()
        self.yourTurnBlinker = Sequence()
        self.moveList = []
        self.mySquares = []
        self.playerSeats = None
        ###self.playerTags = [None, None, None, None, None, None


        #Mouse picking required stuff
        self.accept('mouse1', self.mouseClick)
        self.traverser = base.cTrav
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(ToontownGlobals.WallBitmask)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.myHandler = CollisionHandlerQueue()
        self.traverser.addCollider(self.pickerNP, self.myHandler)

        self.buttonModels = loader.loadModel("phase_3.5/models/gui/inventory_gui")
        self.upButton = self.buttonModels.find("**//InventoryButtonUp")
        self.downButton = self.buttonModels.find("**/InventoryButtonDown")
        self.rolloverButton = self.buttonModels.find("**/InventoryButtonRollover")

        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()

        #[0] GREEN [1] YELLOW [2] PURPLE [3] BLUE [4] PINK [5] RED
        self.playerColors = [ Vec4(0,.90,0,1), Vec4(.9,.9,0,1), Vec4(.45,0,.45,1), Vec4(.2,.4,.8,1), Vec4(1,.45,1,1), Vec4(.8,0,0,1) ]
        self.tintConstant = Vec4(.25,.25,.25,0)
        self.ghostConstant = Vec4(0,0,0,.5)

        #starting positions are used to check and see if a player has gone into
        #his opposing players starting position, thus to tell if he won.
        self.startingPositions = [[0,1,2,3,4,5,6,7,8,9],
                                  [10,11,12,13,23,24,25,35,36,46],
                                  [65,75,76,86,87,88,98,99,100,101],
                                  [111,112,113,114,115,116,117,118,119,120],
                                  [74,84,85,95,96,97,107,108,109,110],
                                  [19,20,21,22,32,33,34,44,45,55]]
        self.nonOpposingPositions = []

      
        self.knockSound = base.loadSfx("phase_5/audio/sfx/GUI_knock_1.mp3")
        self.clickSound = base.loadSfx("phase_3/audio/sfx/GUI_balloon_popup.mp3")
        self.moveSound = base.loadSfx("phase_6/audio/sfx/CC_move.mp3")
        self.accept('stoppedAsleep', self.handleSleep)

        #base.setCellsAvailable(base.leftCells + 
                               #[base.bottomCells[0]], 0)

        #base.setCellsAvailable(base.bottomCells,0)
        

        #######################
        #Fsm and State Data
        from direct.fsm import ClassicFSM,State
        self.fsm = ClassicFSM.ClassicFSM('ChineseCheckers',
                           [State.State('waitingToBegin',
                                        self.enterWaitingToBegin,
                                        self.exitWaitingToBegin,
                                        ['playing','gameOver']),
                            State.State('playing',
                                        self.enterPlaying,
                                        self.exitPlaying,
                                       ['gameOver']),
                            State.State('gameOver',
                                        self.enterGameOver,
                                        self.exitGameOver,
                                        ['waitingToBegin'])],
                           # Initial State
                           'waitingToBegin',
                           # Final State
                           'waitingToBegin',
                           )
       
        #########################
        #Set up the Board Locators
        ##
        x = self.boardNode.find("**/locators")
        #set up the locator list so we can mess with it
        self.locatorList = x.getChildren()
        #tag the locators for "picking" ingame
        #also add colision spheres for movement
        tempList = []
        for x in range(0,121):
            self.locatorList[x].setTag("GamePeiceLocator", "%d" % x)
            tempList.append(self.locatorList[x].attachNewNode(CollisionNode("picker%d" % x)))
            tempList[x].node().addSolid(CollisionSphere(0,0,0,.115))
        for z in self.locatorList:
           y = loader.loadModel("phase_6/models/golf/checker_marble.bam")
           z.setColor(0,0,0,0)
           y.reparentTo(z)
           #y.show()
           #y.hide()

    def setName(self, name):
        self.name = name

    def announceGenerate(self): 
        DistributedNode.DistributedNode.announceGenerate(self)
        if self.table.fsm.getCurrentState().getName() != 'observing':
            if base.localAvatar.doId in self.table.tableState: # Fix for strange state #TEMP until i find the cause
                self.seatPos = self.table.tableState.index(base.localAvatar.doId)

        self.playerTags.setPos(self.getPos())
    def handleSleep(self, task = None):
        if self.fsm.getCurrentState().getName() == "waitingToBegin":
            self.exitButtonPushed()
        if task != None:
            task.done
        #task.done
    ##########
    ##setTableDoId (required broadcast ram)
    #
    #Upon construction, sets local pointer to the table, as well as
    #sets the pointer on the table to itself.
    #This is necessary to handle events that occur on the table, not
    #particularly inside of any one game.
    ###
    def setTableDoId(self, doId):
        self.tableDoId = doId
        self.table = self.cr.doId2do[doId]
        self.table.setTimerFunc(self.startButtonPushed)
        self.fsm.enterInitialState()
        self.table.setGameDoId(self.doId)
        #self.table.tempCheckers.hide()
        #self.boardNode.setP(self.table.getP())

    #########
    ##Disable/Delete
    #Must be sure to remove/delete any buttons, screen text
    #that may be on the screen in the event of a chosen ( or asynchrinous )
    #disable or deletion - Code redundance here is necessary
    #being that "disable" is called upon server crash, and delete is
    #called upon zone exit
    ###     
    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        if self.leaveButton:
            self.leaveButton.destroy()
            self.leavebutton = None
        if self.screenText:
            self.screenText.destroy()
            self.screenText = None
        if self.turnText:
            self.turnText.destroy()
            self.turnText = None
        self.clockNode.stop()
        self.clockNode.hide()
        self.ignore('mouse1')
        self.ignore('stoppedAsleep')
        self.fsm = None
        self.cleanPlayerTags()
        ###self.table = None

    def delete(self):
        DistributedNode.DistributedNode.delete(self)
        self.table.gameDoId = None
        self.table.game = None
        if self.exitButton:
            self.exitButton.destroy()
        if self.startButton  :
            self.startButton.destroy()
        self.clockNode.stop()
        self.clockNode.hide()
        self.table.startButtonPushed = None
        self.ignore('mouse1')
        self.ignore('stoppedAsleep')
        self.fsm = None
        self.table = None
        self.cleanPlayerTags()
        del self.playerTags
        del self.playerTagList
        self.playerSeats = None
        self.yourTurnBlinker.finish()

    ##########
    ##Timer Functions
    #setTimer (broadcast ram required)
    #setTurnTimer(broadcast ram required)
    #
    #setTimer() controlls the timer for game begin, which upon its timout
    #calls the startButton.
    #
    #turnTimer() does just that
    #
    #Important to note that both timers run on the same clockNode.
    ##########
    def getTimer(self):
        self.sendUpdate('requestTimer', [])
    def setTimer(self, timerEnd):
        #print "TIMEREND! ", timerEnd
        if self.fsm.getCurrentState() != None and self.fsm.getCurrentState().getName() == 'waitingToBegin' and not self.table.fsm.getCurrentState().getName() == 'observing':
            self.clockNode.stop()
            time = globalClockDelta.networkToLocalTime(timerEnd)
            timeLeft = int(time - globalClock.getRealTime() )
            if(timeLeft > 0 and timerEnd != 0):
                if timeLeft > 60:
                    timeLeft = 60
                self.clockNode.setPos(1.16, 0, -0.83)
                self.clockNode.countdown(timeLeft, self.startButtonPushed)
                self.clockNode.show()
            else:
                self.clockNode.stop()
                self.clockNode.hide()
    def setTurnTimer(self, turnEnd):
        if self.fsm.getCurrentState() != None and self.fsm.getCurrentState().getName() == 'playing':
            self.clockNode.stop()
            time = globalClockDelta.networkToLocalTime(turnEnd)
            timeLeft = int(time - globalClock.getRealTime() )
            if timeLeft > 0:
                self.clockNode.setPos(-.74, 0, -0.20)
                if self.isMyTurn:
                    self.clockNode.countdown(timeLeft, self.doRandomMove)
                else:
                    self.clockNode.countdown(timeLeft, self.doNothing)
                self.clockNode.show()
            
        
        
    ###########
    ##Game start(broadcast) and Send Turn (broadcast ram)
    #
    #IMPORTANT - 255 is the Uint8 sent to the player when a game starts
    #to dictate to him that a game is beginning and he is labeled as an observer
    #for that game - this affects the visual queues for his player color ect.
    ##########

    def gameStart(self, playerNum):
        if playerNum != 255: #observer value
            self.playerNum = playerNum
            self.playerColor = self.playerColors[playerNum-1]
            self.moveCameraForGame()

            playerPos = playerNum-1
            import copy
            self.nonOpposingPositions = copy.deepcopy(self.startingPositions)
            if playerPos == 0:
                self.nonOpposingPositions.pop(0)
                self.opposingPositions = self.nonOpposingPositions.pop(2)
            elif playerPos == 1:
                self.nonOpposingPositions.pop(1)
                self.opposingPositions = self.nonOpposingPositions.pop(3)
            elif playerPos == 2:
                self.nonOpposingPositions.pop(2)
                self.opposingPositions = self.nonOpposingPositions.pop(4)
            elif playerPos == 3:
                self.nonOpposingPositions.pop(3)
                self.opposingPositions =  self.nonOpposingPositions.pop(0)
            elif playerPos == 4:
                self.nonOpposingPositions.pop(4)
                self.opposingPositions = self.nonOpposingPositions.pop(1)
            elif playerPos == 5:
                self.nonOpposingPositions.pop(5)
                self.opposingPositions = self.nonOpposingPositions.pop(2)
                
        self.fsm.request('playing')
    def sendTurn(self,playersTurn):
        self.playersTurnBlinker.finish()
        if self.fsm.getCurrentState().getName() == 'playing':
            #print "GETTING HERE!", playersTurn - 1, " LENGTH!!!" , self.playerTagList #self.playerTagList

            if self.playerSeats == None:
                self.sendUpdate("requestSeatPositions", [])
            else:
                if playersTurn == self.playerNum:
                    self.isMyTurn = True
                self.enableTurnScreenText(playersTurn)
                self.playersTurnBlinker = Sequence()
                origColor = self.playerColors[playersTurn-1]
                self.playersTurnBlinker.append(LerpColorInterval(self.playerTagList[self.playerSeats.index(playersTurn)], .4, origColor - self.tintConstant - self.ghostConstant, origColor))
                self.playersTurnBlinker.append(LerpColorInterval(self.playerTagList[self.playerSeats.index(playersTurn)], .4,origColor, origColor - self.tintConstant - self.ghostConstant))
                self.playersTurnBlinker.loop()

    def announceSeatPositions(self, playerPos):
        #print "ANNOUNCESEATPOSITIONS!", playerPos
        self.playerSeats = playerPos
        for x in range(6):
            pos = self.table.seats[x].getPos(render)
            renderedPeice = loader.loadModel("phase_6/models/golf/checker_marble.bam")
            #renderedPeice.setColor(self.playerColors[x-1])
            renderedPeice.reparentTo(self.playerTags)
            renderedPeice.setPos(pos)
            renderedPeice.setScale(1.5)
            if x == 1:
                renderedPeice.setZ(renderedPeice.getZ() +3.3)
                renderedPeice.setScale(1.3)
            elif x == 4:
                renderedPeice.setZ(renderedPeice.getZ() +3.3)
                renderedPeice.setScale(1.45)
            else:
                renderedPeice.setZ(renderedPeice.getZ() +3.3)
            renderedPeice.hide()
        self.playerTagList = self.playerTags.getChildren()
        for x in playerPos:
            if x != 0:
                self.playerTagList[playerPos.index(x)].setColor(self.playerColors[x-1])
                self.playerTagList[playerPos.index(x)].show()

        #if game is already going
        #if self.fsm.getCurrentState().getName() == 'playing':
          #  if not self.playersTurnBlinker.isPlaying():
         #      self.playersTurnBlinker = Sequence()
          #      origColor = self.playerColors[playersTurn-1]
           #     self.playersTurnBlinker.append(LerpColorInterval(self.playerTagList[self.playerSeats.index(playersTurn)], .4, origColor - self.tintConstant - self.ghostConstant, origColor))
            #    self.playersTurnBlinker.append(LerpColorInterval(self.playerTagList[self.playerSeats.index(playersTurn)], .4,origColor, origColor - self.tintConstant - self.ghostConstant))
             #   self.playersTurnBlinker.loop()
             
    def cleanPlayerTags(self):
        for x in self.playerTagList:
            x.removeNode()
        self.playerTagList = []
        self.playerTags.removeNode()
        
    ##########
    ##Move camera
    #
    #To make camera movement not seem weird (turning 270 degrees example)
    #Must check the clients orientation between the seatPos and his current H
    # so that he turns the least possible amount for the camera orientation
    #
    #
    ##########
    def moveCameraForGame(self): 
        if self.table.cameraBoardTrack.isPlaying():
            self.table.cameraBoardTrack.finish()
        rotation = 0
        if self.seatPos >2:
            if self.playerNum == 1:
                rotation = 180 
            elif self.playerNum == 2:
                rotation = -120
            elif self.playerNum == 3:
                rotation = -60
            elif self.playerNum == 4:
                rotation = 0 
            elif self.playerNum == 5:
                rotation = 60
            elif self.playerNum == 6:
                rotation = 120
        else:
            if self.playerNum == 1:
                rotation = 0
            elif self.playerNum == 2:
                rotation = 60
            elif self.playerNum == 3:
                rotation = 120
            elif self.playerNum == 4:
                rotation = 180
            elif self.playerNum == 5:
                rotation = -120
            elif self.playerNum == 6:
                rotation = -60

        #print self.boardNode.getHpr()
        # int = LerpHprInterval(camera, 3,Vec3(camera.getH(),camera.getP(),rotation), camera.getHpr())
        #self.table.tempCheckers.hide()
        if rotation == 60 or rotation == -60:
            int  = LerpHprInterval(self.boardNode, 2.5, Vec3(rotation, self.boardNode.getP(), self.boardNode.getR()), self.boardNode.getHpr())
        elif rotation == 120 or rotation == -120:
            int  = LerpHprInterval(self.boardNode, 3.5, Vec3(rotation, self.boardNode.getP(), self.boardNode.getR()), self.boardNode.getHpr())
        else:
            int  = LerpHprInterval(self.boardNode, 4.2, Vec3(rotation, self.boardNode.getP(), self.boardNode.getR()), self.boardNode.getHpr())
            
        #self.table.tempCheckers.setHpr( Vec3(rotation, self.table.tempCheckers.getP(), self.table.tempCheckers.getR()))
        int.start()
        
    #####################
    #FSM Stuff
    ###
    def enterWaitingToBegin(self):
        if self.table.fsm.getCurrentState().getName() != 'observing':      
            self.enableExitButton()
            self.enableStartButton()

    def exitWaitingToBegin(self):
        if self.exitButton:
            self.exitButton.destroy()
            self.exitButton = None
        if self.startButton  :
            self.startButton.destroy()
            self.exitButton = None
        self.clockNode.stop()
        self.clockNode.hide()
        
    def enterPlaying(self):
        self.inGame = True
        self.enableScreenText()
        if self.table.fsm.getCurrentState().getName() != 'observing':   
            self.enableLeaveButton()

    def exitPlaying(self):
        self.inGame = False
        if self.leaveButton:
            self.leaveButton.destroy()
            self.leavebutton = None
        self.playerNum = None
        if self.screenText:
            self.screenText.destroy()
            self.screenText = None
        if self.turnText:
            self.turnText.destroy()
            self.turnText = None
        self.clockNode.stop()
        self.clockNode.hide()
        self.cleanPlayerTags()
    def enterGameOver(self):
        pass
    def exitGameOver(self):
        pass

    ##################################################
    #              Button Functions and Text
    ###
    def exitWaitCountdown(self):
        self.__disableCollisions()
        self.ignore("trolleyExitButton")
        self.clockNode.reset()

    def enableExitButton(self):
        self.exitButton = DirectButton(
            relief = None,
            text = TTLocalizer.ChineseCheckersGetUpButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.8,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (.92, 0, 0.4),
            scale = 0.15,
            command = lambda self=self: self.exitButtonPushed(),
            )
        return
    def enableScreenText(self):
        defaultPos = (-.80, -0.40)
        if self.playerNum == 1:
            message = TTLocalizer.ChineseCheckersColorG
            color = self.playerColors[0]
        elif self.playerNum == 2:
            message = TTLocalizer.ChineseCheckersColorY
            color = self.playerColors[1]
        elif self.playerNum == 3:
            message = TTLocalizer.ChineseCheckersColorP
            color = self.playerColors[2]
        elif self.playerNum == 4:
            message = TTLocalizer.ChineseCheckersColorB
            color = self.playerColors[3]
        elif self.playerNum == 5:
            message = TTLocalizer.ChineseCheckersColorPink
            color = self.playerColors[4]
        elif self.playerNum == 6:
            message = TTLocalizer.ChineseCheckersColorR
            color = self.playerColors[5]
        else:
            message = TTLocalizer.ChineseCheckersColorO
            color = Vec4(0.0,0.0,0.0,1.0)
            defaultPos = (-.80, -0.40)
        self.screenText = OnscreenText(text = message, pos = defaultPos, scale = 0.10,fg=color,align=TextNode.ACenter,mayChange=1)
    def enableStartButton(self):
        self.startButton = DirectButton(
            relief = None,
            text = TTLocalizer.ChineseCheckersStartButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.6,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (.92, 0, 0.1),
            scale = 0.15,
            command = lambda self=self: self.startButtonPushed(),
            )
        return
    def enableLeaveButton(self):
        self.leaveButton = DirectButton(
            relief = None,
            text = TTLocalizer.ChineseCheckersQuitButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.13),
            text_scale = 0.5,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (.92, 0, 0.4),
            scale = 0.15,
            command = lambda self=self: self.exitButtonPushed(),
            )
        return
    def enableTurnScreenText(self,player):
        self.yourTurnBlinker.finish()
        playerOrder = [1,4,2,5,3,6]
        message1 = TTLocalizer.ChineseCheckersIts
        if(self.turnText != None):
            self.turnText.destroy()
        #print "player ---",player
        #print "playerNum --" ,self.playerNum
        if player == self.playerNum:
            message2 = TTLocalizer.ChineseCheckersYourTurn
            color = (0,0,0,1)
        else:
              if player == 1:
                  message2 = TTLocalizer.ChineseCheckersGreenTurn
                  color = self.playerColors[0]
              elif player == 2:
                  message2 = TTLocalizer.ChineseCheckersYellowTurn
                  color = self.playerColors[1]
              elif player == 3:
                  message2 = TTLocalizer.ChineseCheckersPurpleTurn
                  color = self.playerColors[2]
              elif player == 4:
                  message2 = TTLocalizer.ChineseCheckersBlueTurn
                  color = self.playerColors[3]
              elif player  == 5:
                  message2 = TTLocalizer.ChineseCheckersPinkTurn
                  color = self.playerColors[4]
              elif player == 6:
                  message2 = TTLocalizer.ChineseCheckersRedTurn
                  color = self.playerColors[5]
        self.turnText = OnscreenText(text = message1+message2, pos = (-0.80,-0.50), scale = 0.092,fg=color,align=TextNode.ACenter,mayChange=1)
        if player == self.playerNum:
            self.yourTurnBlinker = Sequence()
            self.yourTurnBlinker.append(LerpScaleInterval(self.turnText, .6, 1.045, 1))
            self.yourTurnBlinker.append(LerpScaleInterval(self.turnText, .6, 1, 1.045))
            self.yourTurnBlinker.loop()

    #This function is called either if the player clicks on it (to begin a game)
    #or if the game begin timer runs out. (timer is in sync with server so results should be
    # + or - ~ 1 second
    def startButtonPushed(self):
        self.sendUpdate("requestBegin")
        self.startButton.hide()
        self.clockNode.stop()
        self.clockNode.hide()

    def exitButtonPushed(self):
        self.fsm.request('gameOver')
        self.table.fsm.request('off')
        self.clockNode.stop()
        self.clockNode.hide()

        self.table.sendUpdate("requestExit")
    ##########
    #Mouse Picking/clicking operations
    #
    #
    #These functions handle all of the mous clicking functions
    #Its best to look through the code for comments for it to make
    #the most sense.
    #
    #The self.blinker that is referenced in these functions, is a cosmetic
    #colorLerp that gives the player a visual feedback as to what checkers peice
    #he has (currently) selected.
    ##########
    def mouseClick(self):
        messenger.send('wakeup')
        if self.isMyTurn == True and self.inGame == True : #cant pick stuff if its not your turn
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode,mpos.getX(), mpos.getY())

            self.traverser.traverse(render)
            if self.myHandler.getNumEntries() > 0:
                self.myHandler.sortEntries()#get the closest Object
                pickedObj = self.myHandler.getEntry(0).getIntoNodePath()
                #will return the INT for the locator node closest parent 
                pickedObj = pickedObj.getNetTag("GamePeiceLocator")
                if pickedObj: #make sure something actually was "picked"
                    self.handleClicked(int(pickedObj))
    
    def handleClicked(self, index):
        #self.inOpposing = False
        self.sound = Sequence( SoundInterval(self.clickSound)) #You clicked something play the click sound
        #First Moved Square
        if self.moveList == []:
            #check if owned
            if not index in self.mySquares:
                return
            self.moveList.append(index) #put this on the movelist
            if index in self.opposingPositions:
                self.isOpposing = True
            else:
                self.isOpposing = False

            #Start blinking the new "active" peice
            self.blinker = Sequence()
            self.blinker.append(LerpColorInterval(self.locatorList[index], .7, self.playerColor - self.tintConstant, self.playerColor))
            self.blinker.append(LerpColorInterval(self.locatorList[index], .7,self.playerColor, self.playerColor - self.tintConstant))
            self.blinker.loop()
            self.sound.start()

        else:
            #Check if the square clicked is not open, if so break out not legal
            #If the Player Clicks on one of his peices after an array of clicking new peices
            #will reset his "move" and start a new movelist
            if self.board.squareList[index].getState() == self.playerNum :
                for x in self.moveList: #clear the already selected Nodes back to white
                    self.locatorList[x].setColor(1,1,1,1)
                    self.locatorList[x].hide()
                #Blinker is the color lerp for the peice "flashing" - need to stop the flashing of the old one
                self.blinker.finish()
                self.blinker = Sequence()
                self.blinker.append(LerpColorInterval(self.locatorList[index], .7, self.playerColor - self.tintConstant, self.playerColor))
                self.blinker.append(LerpColorInterval(self.locatorList[index], .7,self.playerColor, self.playerColor - self.tintConstant))
                self.blinker.loop()
                self.sound.start()
                
                #Swap back to the original peice
                #set the original node back to playercolor
                self.locatorList[self.moveList[0]].setColor(self.playerColor)
                self.locatorList[self.moveList[0]].show()
                self.moveList = [] 
                self.moveList.append(index)
                if index in self.opposingPositions:
                    self.isOpposing = True
                else:
                    self.isOpposing = False
            elif self.board.squareList[index].getState() != 0:
                return #do nothing because he clicked someone elses peice
            else:
                #Check for Explicit adjacent move
                if len(self.moveList) == 1 and self.board.squareList[index].getState() == 0:
                    #print "I AM OUTSIDE"
                    if index in self.board.squareList[self.moveList[0]].getAdjacent():
                        #print "I AM INSIDE"
                        for x in self.nonOpposingPositions:
                            if index in x:
                                return #You cannot end a move in a non opposing players square
                        self.moveList.append(index)
                        self.blinker.finish()
                        self.d_requestMove(self.moveList)
                        self.moveList = []
                        self.isMyTurn = False
                        self.sound.start()
                #Check for mid series jumps stoppage
                #print len(self.moveList), len(self.moveList)-1
                if len(self.moveList) >= 1:               
                    if index == self.moveList[len(self.moveList)-1]: #you clicked the same thing TWICE
                        for x in self.nonOpposingPositions:
                            if index in x:
                                return #Will force you to jump out ...
                        if self.existsLegalJumpsFrom(index) == True:
                            self.blinker.finish()
                            #self.locatorList[index].setColor(self.playerColor - self.tintConstant)
                            #self.locatorList[index].show()
                            self.d_requestMove(self.moveList)
                            self.moveList=[]
                            self.isMyTurn = False
                            self.sound.start()
                    #Check for Normal jump
                    #Also check if its a 'finishing jump'
                    #Therefore no jumps possible after it
                        ###print "CHECK LEGAL JUMP!", self.checkLegalMove(self.board.getSquare(self.moveList[len(self.moveList)-1]), self.board.getSquare(index)) == True
                    elif self.checkLegalMove(self.board.getSquare(self.moveList[len(self.moveList)-1]), self.board.getSquare(index)) == True:
                        #this is the part that adds moves to a series of jumps
                        ##
                        #This if statement is an Explicit check to make sure that
                        #the clicked peice, after a series of jumps
                        #is not in the middle jump adjacent, This results in a
                        #bug due to the way ive detected "legal moves"
                        #but this explicit check should fix that.
                        if not index in self.board.squareList[self.moveList[len(self.moveList)-1]].getAdjacent():
                            for x in self.nonOpposingPositions:
                                #print " LEGAL JUMPS FROM! ", self.existsLegalJumpsFrom(index)
                                if self.existsLegalJumpsFrom(index) == False:
                                    if index in x:
                                        return #He tried to JUMP into non opposing players startPos => Illegal
                            self.moveList.append(index)
                            #ghostConstant here is a small alpha offset to give it a transparent look
                            #tintConstant makes the peice a bit darker (necessary when ghosting)
                            self.locatorList[index].setColor(self.playerColor - self.tintConstant - self.ghostConstant)
                            self.locatorList[index].show()
                            self.sound.start()
                            if self.existsLegalJumpsFrom(index) == False:
                                self.blinker.finish()
                                self.d_requestMove(self.moveList)
                                self.moveList= []
                                self.isMyTurn = False
    ##################################################################
    #                    Legal Move Request/Checker
    #          (COPY PASTED FROM AI)
    #   (Logic here reflects the (NEXT) move not a series of moves, but still
    #Checks the validity of two different move peices
    #
    #This is probably the most complicated as well as most important part
    #of the chinese checkers code. To completely understand the CheckLegalMoves,
    #get out a peice of paper and try to DRAW out what the logic is doing, ill do
    #my best to explain it.
    #
    #
    #Players request moves as a list of Uint8s (already should be verified on the client side)
    #but since players are cheating bastards, we check on the server. Basically, how the logic works
    #is it takes pairs one at a time and checks for a legal move between the two, ect and traverses the
    #list.
    #
    #A move is Legal if (it is adjacent to its last move) - in a checkerboard adjacent is stored in a list
    #of 6 integers representing the other squares (see ChineseCheckerBoard.py)
    #
    #board.squareList[x].getAdjacent() visually looks like this
    #    1 2
    #   0 x 3  where those values [ ] are integers to adjacent squares.
    #    5 4
    #
    # If a adjacent square does not exist on the board, say the first square only has two adjacent,
    # the squares in the adjacent list are set to None
    #
    #A move is also legal if there exists a legal Jump from A to B. the logic here is difficult to
    #express without a picture, but for instance, say A is jumping to B
    #
    #    1 2 1 2
    #   0 A 3 B 3
    #    5 4 5 6   
    #
    # You check all of A's adjacents, and check the index of that \
    # particular one (of A's adjacents) that it sits in A,
    #if that is equal to B, there is a legal jump, if no one is found the move is illegal.
    #
    # EX. board.squareList[A].adjacent[3] == (some number to the left of b)
    #     board.squareList[that number].getAdjacent[self.board.squareList[A].index(some number)
    #
    #     in this case it equals B (draw it out, Trust me it helps)
    ####                           
    def existsLegalJumpsFrom(self,index):
        for x in self.board.squareList[index].getAdjacent():
            if x == None:
                pass
            elif x in self.moveList:
                pass
            elif self.board.getState(x) == 0:
                pass
            elif self.board.squareList[x].getAdjacent()[self.board.squareList[index].getAdjacent().index(x)] == None:
                pass
            elif self.board.getState(self.board.squareList[x].getAdjacent()[self.board.squareList[index].getAdjacent().index(x)]) == 0 and not (self.board.squareList[x].getAdjacent()[self.board.squareList[index].getAdjacent().index(x)]) in self.moveList:
                return True
        return False
    def checkLegalMove(self, firstSquare, secondSquare):
        if secondSquare.getNum() in firstSquare.getAdjacent():
            return True
        else:
            for x in firstSquare.getAdjacent():
                if x == None:
                    pass
                elif self.board.squareList[x].getState() == 0:
                    pass
                else:
                    #print " FIRSTSQUARE ADJACENT AND X -- " , firstSquare.getAdjacent(), " X == " , x
                    #print "Xs Adjacent and its Index", self.board.squareList[x].getAdjacent(), " INDEX == " , firstSquare.getAdjacent().index(x)
                    if (self.board.squareList[x].getAdjacent()[firstSquare.getAdjacent().index(x)]) == secondSquare.getNum():
                        return True
            return False

    def d_requestMove(self, moveList):
        self.sendUpdate('requestMove', [moveList])

    ##########
    ##setGameState (required broadcast ram)
    #
    #This is the function that handles the moves made after a move is parsed by the AI
    #and deemed to be valid
    #
    #If moveList is the empty List, then the player is asynchronously joining the game, (OBSERVING)
    #and just wants the board state.
    #
    #otherwise there is a series of jumps (or jump) that needs to be parsed and animated, then
    #consequently setting the board state
    #
    #after every setGameState, the client checks to see the current
    #Status of his peices (checkForWin), if he belives he won, he requests it to the server
    #########
    def setGameState(self, tableState, moveList):
        if moveList != []:
            self.animatePeice(tableState, moveList)
        else:
            self.updateGameState(tableState)
    def updateGameState(self, squares):
        self.board.setStates(squares)
        self.mySquares = []
        messenger.send('wakeup')
        for x in range(121):
            self.locatorList[x].clearColor()
            owner = self.board.squareList[x].getState()
            if owner == self.playerNum:
                self.mySquares.append(x)
            if owner == 0:
                self.locatorList[x].hide()
            else:
                self.locatorList[x].show()
            if owner == 1:
                self.locatorList[x].setColor(self.playerColors[0])
            elif owner == 2:
                self.locatorList[x].setColor(self.playerColors[1])
            elif owner == 3:
                self.locatorList[x].setColor(self.playerColors[2])
            elif owner == 4:
                self.locatorList[x].setColor(self.playerColors[3])
            elif owner == 5:
                self.locatorList[x].setColor(self.playerColors[4])
            elif owner == 6:
                self.locatorList[x].setColor(self.playerColors[5])

        self.mySquares.sort()
        self.checkForWin()
    def animatePeice(self, tableState, moveList):
        messenger.send('wakeup')
        gamePeiceForAnimation = loader.loadModel("phase_6/models/golf/checker_marble.bam")
        gamePeiceForAnimation.setColor(self.locatorList[moveList[0]].getColor())
        gamePeiceForAnimation.reparentTo(self.boardNode)
        gamePeiceForAnimation.setPos(self.locatorList[moveList[0]].getPos())

        self.locatorList[moveList[0]].hide()
        checkersPeiceTrack = Sequence()
        length = len(moveList)
        for x in range(length - 1):
            checkersPeiceTrack.append(Parallel( SoundInterval(self.moveSound),
                                                ProjectileInterval(gamePeiceForAnimation,
                                                                   endPos = self.locatorList[moveList[x+1]].getPos(),
                                                                   duration = .5 )))
        checkersPeiceTrack.append(Func(gamePeiceForAnimation.removeNode))
        checkersPeiceTrack.append(Func(self.updateGameState,  tableState))
        checkersPeiceTrack.start()
    def checkForWin(self):
        if self.playerNum == 1:
            if(self.mySquares  == self.startingPositions[3]):
                self.sendUpdate('requestWin', [])
        elif self.playerNum == 2:
            if(self.mySquares  == self.startingPositions[4]):
                self.sendUpdate('requestWin', [])
        elif self.playerNum == 3:
            if(self.mySquares  == self.startingPositions[5]):
                self.sendUpdate('requestWin', [])
        elif self.playerNum == 4:
            if(self.mySquares  == self.startingPositions[0]):
                self.sendUpdate('requestWin', [])
        elif self.playerNum == 5:
            if(self.mySquares  == self.startingPositions[1]):
                self.sendUpdate('requestWin', [])
        elif self.playerNum == 6:
            if(self.mySquares  == self.startingPositions[2]):
                 self.sendUpdate('requestWin', [])
    def announceWin(self, avId):
        self.fsm.request('gameOver')

    ###########
    ##doRandomMove
    #
    #If a clients move Timer runs out, it will calculate a random move for him
    #after 3 random moves, it kicks the client out of the game by pushing the
    #"get up" button for him.
    ###########
    def doRandomMove(self):
        if len(self.moveList) >= 2:
            self.blinker.finish()
            #self.locatorList[index].setColor(self.playerColor - self.tintConstant)
            #self.locatorList[index].show()
            self.d_requestMove(self.moveList)
            self.moveList=[]
            self.isMyTurn = False
            self.playSound = Sequence(SoundInterval(self.knockSound))
            self.playSound.start()
        else:
            import random
            move = []
            foundLegal = False
            self.blinker.pause()
            self.numRandomMoves += 1
            ###self.blinker.finish()
            while not foundLegal:
                x = random.randint(0,9)
                for y in self.board.getAdjacent(self.mySquares[x]):
                    if y != None and self.board.getState(y) == 0 :
                        for zz in self.nonOpposingPositions:
                            if not y in zz:
                                move.append(self.mySquares[x])
                                move.append(y)
                                foundLegal = True
                                break
                        break

            if move == []:
                pass
                #current flaw in the logic, but shouldnt really ever happen
                #though on live it might
                #print "random move is empty"
            playSound = Sequence(SoundInterval(self.knockSound))
            playSound.start()
            self.d_requestMove(move)
            self.moveList=[]
            self.isMyTurn = False
            if(self.numRandomMoves >= 5):
                self.exitButtonPushed()
        
                
                             
    def doNothing(self):
        pass
