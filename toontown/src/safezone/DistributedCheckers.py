from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer

from direct.distributed import DistributedNode
from direct.distributed.ClockDelta import globalClockDelta
from CheckersBoard import CheckersBoard
from direct.fsm import ClassicFSM, State
from direct.fsm import StateData
#from toontown.distributed import DelayDelete

from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *

from otp.otpbase import OTPGlobals


from direct.showbase import PythonUtil

class DistributedCheckers(DistributedNode.DistributedNode):
    def __init__(self, cr):
        NodePath.__init__(self, "DistributedCheckers")
        DistributedNode.DistributedNode.__init__(self,cr)
        self.cr = cr

        self.reparentTo(render)
        self.boardNode = loader.loadModel("phase_6/models/golf/regular_checker_game.bam")
        self.boardNode.reparentTo(self)
        
        self.board = CheckersBoard()

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
        self.moveList = []
        self.mySquares = []
        self.myKings = []
        self.isRotated = False


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
        self.playerColors = [ Vec4(0,0,1,1), Vec4(0,1,0,1) ]
        self.tintConstant = Vec4(.25,.25,.25,.5)
        self.ghostConstant = Vec4(0,0,0,.8)

        #starting positions are used to check and see if a player has gone into
        #his opposing players starting position, thus to tell if he won.
        self.startingPositions = [[0,1,2,3,4,5,6,7,8,9,10,11], [20,21,22,23,24,25,26,27,28,29,30,31]]
                                  

      
        self.knockSound = base.loadSfx("phase_5/audio/sfx/GUI_knock_1.mp3")
        self.clickSound = base.loadSfx("phase_3/audio/sfx/GUI_balloon_popup.mp3")
        self.moveSound = base.loadSfx("phase_6/audio/sfx/CC_move.mp3")
        self.accept('stoppedAsleep', self.handleSleep)
        

        #######################
        #Fsm and State Data
       # from direct.fsm import ClassicFSM,State
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
        x = self.boardNode.find("**/locator*")
        #set up the locator list so we can mess with it
        self.locatorList = x.getChildren()
        #tag the locators for "picking" ingame
        #also add colision spheres for movement
        tempList = []
        for x in range(0,32):
            self.locatorList[x].setTag("GamePeiceLocator", "%d" % x)
            tempList.append(self.locatorList[x].attachNewNode(CollisionNode("picker%d" % x)))
            tempList[x].node().addSolid(CollisionSphere(0,0,0,.39))
        for z in self.locatorList:
           y = loader.loadModel("phase_6/models/golf/regular_checker_piecewhite.bam")
           y.find("**/checker_k*").hide()
           zz = loader.loadModel("phase_6/models/golf/regular_checker_pieceblack.bam")
           zz.find("**/checker_k*").hide()
           y.reparentTo(z)
           y.hide()
           zz.reparentTo(z)
           zz.hide()

    def setName(self, name):
        self.name = name

    def announceGenerate(self): 
        DistributedNode.DistributedNode.announceGenerate(self)
        if self.table.fsm.getCurrentState().getName() != 'observing':
            if base.localAvatar.doId in self.table.tableState: # Fix for strange state #TEMP until i find the cause
                self.seatPos = self.table.tableState.index(base.localAvatar.doId)
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
                    self.clockNode.countdown(timeLeft, self.doNothing)
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
            if self.playerNum == 1:
                self.playerColorString = "white"
            else:
                self.playerColorString = "black"
            self.playerColor = self.playerColors[playerNum-1]
            self.moveCameraForGame()
        self.fsm.request('playing')
    def sendTurn(self,playersTurn):
        if self.fsm.getCurrentState().getName() == 'playing':
            if playersTurn == self.playerNum:
                self.isMyTurn = True
            self.enableTurnScreenText(playersTurn)

    def illegalMove(self):
        self.exitButtonPushed()
        
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
                rotation = 0
            for x in self.locatorList:
                    x.setH(180)
            self.isRotated = True
        else:
            if self.playerNum == 1:
                rotation = 0
            elif self.playerNum == 2:
                rotation = 180
                for x in self.locatorList:
                    x.setH(180)
                self.isRotated = True
        int  = LerpHprInterval(self.boardNode, 4.2, Vec3(rotation, self.boardNode.getP(), self.boardNode.getR()), self.boardNode.getHpr())
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
        #print "IM IN PLAYING?????!?!?!"
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
            message = TTLocalizer.CheckersColorWhite
            color = Vec4(1,1,1,1)
        elif self.playerNum == 2:
            message = TTLocalizer.CheckersColorBlack
            color = Vec4(0,0,0,1)
        else:
            message = TTLocalizer.CheckersObserver
            color = Vec4(0,0,0,1)
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
        playerOrder = [1,4,2,5,3,6]
        message1 = TTLocalizer.CheckersIts
        if(self.turnText != None):
            self.turnText.destroy()
        if player == self.playerNum:
            message2 = TTLocalizer.ChineseCheckersYourTurn
            color = (0,0,0,1)
        else:
              if player == 1:
                  message2 = TTLocalizer.CheckersWhiteTurn
                  color = (1,1,1,1)
              elif player == 2:
                  message2 = TTLocalizer.CheckersBlackTurn
                  color = (0,0,0,1)
        self.turnText = OnscreenText(text = message1+message2, pos = (-0.80,-0.50), scale = 0.092,fg=color,align=TextNode.ACenter,mayChange=1)

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
        self.sound = Sequence( SoundInterval(self.clickSound)) #You clicked something play the click sound
        #First Moved Square
        if self.moveList == []:
            #check if owned
            if not index in self.mySquares and not index in self.myKings:
                return #you clicked on nothing or an opposing peice
            self.moveList.append(index) #put this on the movelist
            type = self.board.squareList[index].getState()
            if type == 3 or type == 4:
                self.moverType = "king"
            else:
                self.moverType = "normal"

            #Start blinking the new "active" peice
            self.blinker = Sequence()
            col = self.locatorList[index].getColor()
            self.blinker.append(LerpColorInterval(self.locatorList[index], .7,self.tintConstant, col))
            self.blinker.append(LerpColorInterval(self.locatorList[index], .7, col ,self.tintConstant))
            self.blinker.loop()
            self.sound.start()
        else:
            if index in self.mySquares or index in self.myKings: #selected a new peice
                for x in self.moveList: #the nodes from
                    self.locatorList[x].setColor(1,1,1,1)
                    self.locatorList[x].hide()
                self.blinker.finish()
                self.blinker = Sequence()
                col = self.locatorList[index].getColor()
                self.blinker.append(LerpColorInterval(self.locatorList[index], .7,self.tintConstant, col))
                self.blinker.append(LerpColorInterval(self.locatorList[index], .7, col ,self.tintConstant))
                self.blinker.loop()
                self.sound.start()
                #Swap back to the original peice
                #set the original node back to playercolor
                #self.locatorList[self.moveList[0]].setColor(self.playerColor)
                self.locatorList[self.moveList[0]].show()
                self.moveList = [] 
                self.moveList.append(index)
                type = self.board.squareList[index].getState()
                if type == 3 or type == 4:
                    self.moverType = "king"
                else:
                    self.moverType = "normal"
            else: #item is either BLANK or the opposing players (checkJump will validate if it is opposing players)
                self.currentMove = index
                lastItem = self.board.squareList[self.moveList[len(self.moveList)-1]]
                thisItem = self.board.squareList[index]
                if self.mustJump == True:
                    if lastItem.getNum() == index: #selected the same item twice
                        self.blinker.finish()
                        self.d_requestMove(self.moveList)
                        self.isMyTurn = False
                        self.moveList= []
                        return
                    #print "CHECK LEGAL JUMP", self.checkLegalJump(lastItem, thisItem, self.moverType), "TYPE == ", self.moverType
                    if self.checkLegalJump(lastItem, thisItem, self.moverType) == True: #There is a Legal Jump
                        #ghostConstant here is a small alpha offset to give it a transparent look
                        #tintConstant makes the peice a bit darker (necessary when ghosting)
                        col = self.locatorList[index].getColor()
                        self.locatorList[index].show()
                        self.sound.start()
                        if self.existsLegalJumpsFrom(index, self.moverType) == False: #No more Series of jumps => Commit the move
                            self.moveList.append(index)
                            self.blinker.finish()
                            self.d_requestMove(self.moveList)
                            self.moveList= []
                            self.isMyTurn = False
                        else:
                            self.moveList.append(index)
                            if self.playerColorString == "white":
                                x = self.locatorList[index].getChildren()[1]
                                x.show()
                            else:
                                x = self.locatorList[index].getChildren()[2]
                                x.show()
                            if self.moverType == "king":
                                x.find("**/checker_k*").show()
                            #self.locatorList[index].ls()
                            self.locatorList[index].setColor(Vec4(.5,.5,.5,.5))
                else: #must do an adjacent move!
                    if self.checkLegalMove(lastItem, thisItem, self.moverType) == True: #there exists a legal move
                        self.moveList.append(index)
                        #ghostConstant here is a small alpha offset to give it a transparent look
                        #tintConstant makes the peice a bit darker (necessary when ghosting)
                        col = self.locatorList[index].getColor()
                        #self.locatorList[index].setColor(col - self.tintConstant - self.ghostConstant)
                        self.locatorList[index].show()
                        self.sound.start()
                        self.blinker.finish()
                        self.d_requestMove(self.moveList)
                        self.moveList= []
                        self.isMyTurn = False
                
                                
    def existsLegalJumpsFrom(self,index, peice):
        if peice == "king":
            for x in range(4):
                if self.board.squareList[index].getAdjacent()[x] != None and self.board.squareList[index].getJumps()[x] != None: # Off the board
                    adj = self.board.squareList[self.board.squareList[index].getAdjacent()[x]]
                    jump = self.board.squareList[self.board.squareList[index].getJumps()[x]]
                    if adj.getState() == 0:
                        pass
                    elif adj.getState() == self.playerNum or adj.getState() == self.playerNum+2:
                        pass
                    elif jump.getState() == 0: #peice is owned by other dude and its a legal jump
                        if not index in self.moveList and not jump.getNum() in self.moveList:
                            return True
                    else:
                        pass
            return False
        elif peice == "normal":
            if self.playerNum == 1:
                moveForward = [1,2]
            elif self.playerNum == 2:
                moveForward = [0,3]
            for x in moveForward:
                if self.board.squareList[index].getAdjacent()[x] != None and self.board.squareList[index].getJumps()[x] != None:
                    adj = self.board.squareList[self.board.squareList[index].getAdjacent()[x]]
                    jump = self.board.squareList[self.board.squareList[index].getJumps()[x]]
                    if adj.getState() == 0:
                        pass
                    elif adj.getState() == self.playerNum or adj.getState() == self.playerNum+2:
                        pass
                    else:
                        if jump.getState() == 0:
                            if not index in self.moveList:
                                return True
            return False

    def existsLegalMovesFrom(self,index, peice):
        if peice == "king":
            for x in self.board.squareList[index].getAdjacent():
                if x != None:
                    if self.board.squareList[x].getState() == 0:
                        return True
            return False
        elif peice == "normal":
            if self.playerNum == 1:
                moveForward = [1,2]
            elif self.playerNum == 2:
                moveForward = [0,3]
            for x in moveForward:
                if self.board.squareList[index].getAdjacent()[x] != None:
                    adj = self.board.squareList[self.board.squareList[index].getAdjacent()[x]]
                    if adj.getState() == 0:
                        return True
            return False
                
    def checkLegalMove(self, firstSquare, secondSquare, peice):
        if (not firstSquare.getNum() in self.mySquares) and (not firstSquare.getNum() in self.myKings):
            return False
        if self.playerNum == 1:
                moveForward = [1,2]
        else: #self.playerNum == 2:
                moveForward = [0,3]
        if peice == "king":
            for x in range(4):
                if firstSquare.getAdjacent()[x] != None:
                    if self.board.squareList[firstSquare.getAdjacent()[x]].getState() == 0 and secondSquare.getNum() in firstSquare.getAdjacent():
                        return True
            return False
        elif peice == "normal":
            for x in moveForward:
                if firstSquare.getAdjacent()[x] != None and secondSquare.getNum() in firstSquare.getAdjacent():
                    if self.board.squareList[firstSquare.getAdjacent()[x]].getState() == 0 and firstSquare.getAdjacent().index(secondSquare.getNum()) == x:
                        return True
            return False
    def checkLegalJump(self, firstSquare, secondSquare, peice):
        if (not firstSquare.getNum() in self.mySquares) and (not firstSquare.getNum() in self.myKings) and len(self.moveList) == 1:
            return False
        if self.playerNum == 1:
                moveForward = [1,2]
                opposingPeices = [2,4]
        else: #self.playerNum == 2:
                moveForward = [0,3]
                opposingPeices = [1,3]
        if peice == "king":
            if secondSquare.getNum() in firstSquare.getJumps():
                index = firstSquare.getJumps().index(secondSquare.getNum())
                if self.board.squareList[firstSquare.getAdjacent()[index]].getState() in opposingPeices:
                    return True
                else:
                    return False
        elif peice == "normal":
            if secondSquare.getNum() in firstSquare.getJumps():
                index = firstSquare.getJumps().index(secondSquare.getNum())
                if index in moveForward:
                    if self.board.squareList[firstSquare.getAdjacent()[index]].getState() in opposingPeices: #is the peice jumping over yours or his
                        return True
                    else:
                        return False 
                else:
                    return False
            else:
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
            if self.board.squareList[moveList[0]].getState() == 1 or self.board.squareList[moveList[0]].getState() == 3:
                playerColor = "white"
            else:
                playerColor = "black"
            if self.board.squareList[moveList[0]].getState() <= 2:
                self.animatePeice(tableState, moveList, "normal", playerColor)
            else:
                self.animatePeice(tableState, moveList, "king", playerColor)
        else:
            self.updateGameState(tableState)
    def updateGameState(self, squares):
        self.board.setStates(squares) #set the board state 
        self.mySquares = []
        self.myKings = []
        messenger.send('wakeup')

        #Because i designed this poorly, Must do a temporary playerNum
        #for observers, and set it back to None when i am done.
        isObserve = False
        if self.playerNum == None:
            self.playerNum = 1
            self.playerColorString = "white"
            isObserve = True
            
            
        #Need to traverse the list to do the showing of peices ect
        for xx in range(32):
            #self.hideChildren(self.locatorList[xx].getChildren()) # Hide all off the pieces
            for blah in self.locatorList[xx].getChildren():
                blah.hide()
                if self.locatorList[xx].getChildren().index(blah) != 0:
                    blah1 = blah.find("**/checker_k*")
            owner = self.board.squareList[xx].getState() #Get the State of that square
            #print owner
            # This means it is MY Peice
            if owner == self.playerNum:
                #need to see what color i am
                if self.playerColorString == "white":
                    x = self.locatorList[xx].getChildren()[1] # white
                    x.show()
                    x.find("**/checker_k*").hide()
                else:
                    x = self.locatorList[xx].getChildren()[2] # black
                    x.show()
                    x.find("**/checker_k*").hide()
                    
                self.mySquares.append(xx)
            #######################
            elif owner == 0: # blank Tile
                self.hideChildren(self.locatorList[xx].getChildren()) # Hide all off the pieces
            #######################
            elif owner == self.playerNum + 2: #its MY peice but its a KING
                 if self.playerColorString == "white":
                    x = self.locatorList[xx].getChildren()[1] # white
                    x.show()
                    x.find("**/checker_k*").show()
                 else:
                     x = self.locatorList[xx].getChildren()[2] # black
                     x.show()
                     x.find("**/checker_k*").show()
                 self.myKings.append(xx)
            ########################
            else: # opposing player peice
                if owner <= 2: #Opposing player Non king
                    if self.playerColorString == "white":
                        #we are white so show the black piece
                        x = self.locatorList[xx].getChildren()[2]
                        x.show()
                        x.find("**/checker_k*").hide()
                    else:
                        x = self.locatorList[xx].getChildren()[1]
                        x.show()
                        x.find("**/checker_k*").hide()
                else: #the peice is an opposing players KING
                    if self.playerColorString == "white":
                        x = self.locatorList[xx].getChildren()[2]
                        x.show()
                        x.find("**/checker_k*").show()
                    else:
                        x = self.locatorList[xx].getChildren()[1]
                        x.show()
                        x.find("**/checker_k*").show()
            ###########################

        if isObserve == True:
            self.playerNum = None
            self.playerColorString = None
            return
        
        ######
        #A player MUST move if he has a legal jump
        #This will flag the bool making him do so
        ######
        self.mustJump = False
        self.hasNormalMoves = False
        for x in self.myKings:
            if self.existsLegalJumpsFrom(x, "king") == True:
                self.mustJump = True
                break
            else:
                self.mustJump = False
        if self.mustJump == False:
            for x in self.mySquares:
                if self.existsLegalJumpsFrom(x, "normal") == True:
                    self.mustJump = True
                    break
                else:
                    self.mustJump = False
        #############
        #if i dont have any jumps, Must check to see if i have any legal moves
        #If i dont, then the game is over.
        ###
        if self. mustJump != True: #Check for legal moves and possibly LOSS
            for x in self.mySquares:
                if self.existsLegalMovesFrom(x, "normal") == True:
                    self.hasNormalMoves = True
                    break
                else:
                    self.hasNormalMoves = False
                if self.hasNormalMoves == False: #make sure to not overRide a True
                    for x in self.myKings:
                        if self.existsLegalMovesFrom(x, "king") == True:
                            self.hasNormalMoves = True
                            break
                        else:
                            self.hasNormalMoves = False
        if self.mustJump == False and self.hasNormalMoves == False:
            pass #Server is calculating everything

    def hideChildren(self, nodeList):
        for x in range (1,2):
            nodeList[x].hide()

    def animatePeice(self, tableState, moveList,type, playerColor):
        messenger.send('wakeup')
        ###for x in self.locatorList:
            #x.show()
        if playerColor == "white":
            gamePeiceForAnimation = loader.loadModel("phase_6/models/golf/regular_checker_piecewhite.bam")
        else:
            gamePeiceForAnimation = loader.loadModel("phase_6/models/golf/regular_checker_pieceblack.bam")
        if type == "king":
            gamePeiceForAnimation.find("**/checker_k*").show()
        else:
            gamePeiceForAnimation.find("**/checker_k*").hide()
           

        gamePeiceForAnimation.reparentTo(self.boardNode)
        gamePeiceForAnimation.setPos(self.locatorList[moveList[0]].getPos())
        if self.isRotated == True:
            gamePeiceForAnimation.setH(180)

        #self.hideChildren(self.locatorList[moveList[0]].getChildren())
        #self.locatorList[moveList[0]].hide()
        for x in self.locatorList[moveList[0]].getChildren():
            x.hide()
        
        checkersPeiceTrack = Sequence()
        length = len(moveList)
        for x in range(length - 1):
            checkersPeiceTrack.append(Parallel( SoundInterval(self.moveSound),
                                                ProjectileInterval(gamePeiceForAnimation,
                                                                   endPos = self.locatorList[moveList[x+1]].getPos(),
                                                                   duration = .5 )))
        checkersPeiceTrack.append(Func(gamePeiceForAnimation.removeNode))
        checkersPeiceTrack.append(Func(self.updateGameState,  tableState))
        checkersPeiceTrack.append(Func(self.unAlpha, moveList))

        checkersPeiceTrack.start()     
    def announceWin(self, avId):
        self.fsm.request('gameOver')
    
    def unAlpha(self, moveList):
        for x in moveList:
            self.locatorList[x].setColorOff()
    ###########
    ##doRandomMove
    #
    #If a clients move Timer runs out, it will calculate a random move for him
    #after 3 random moves, it kicks the client out of the game by pushing the
    #"get up" button for him.
    ###########
    def doRandomMove(self):
        import random
        move = []
        foundLegal = False
        self.blinker.pause()
        self.numRandomMoves += 1
        while not foundLegal:
            x = random.randint(0,9)
            for y in self.board.getAdjacent(self.mySquares[x]):
                if y != None and self.board.getState(y) == 0:
                    move.append(self.mySquares[x])
                    move.append(y)
                    foundLegal = True
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




