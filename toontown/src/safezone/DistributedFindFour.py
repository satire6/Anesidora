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
#from direct.distributed import DelayDelete

from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *

from otp.otpbase import OTPGlobals


from direct.showbase import PythonUtil
#from direct.task import Task

class DistributedFindFour(DistributedNode.DistributedNode):
    def __init__(self, cr):
        NodePath.__init__(self, "DistributedFindFour")
        DistributedNode.DistributedNode.__init__(self,cr)
        self.cr = cr

        self.reparentTo(render)
        self.boardNode = loader.loadModel("phase_6/models/golf/findfour_game.bam")
        self.boardNode.reparentTo(self)
        #self.boardNode.setScale(.05)

        
        self.board = [ [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0] ]





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
        self.winningSequence = Sequence()
        self.moveSequence = Sequence()
        self.moveList = []
        self.mySquares = []
        self.playerSeats = None
        self.moveCol = None


        self.move = None
        ###self.playerTags = [None, None, None, None, None, None


        #Mouse picking required stuff
        self.accept('mouse1', self.mouseClick)
        self.traverser = base.cTrav
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32(0x1000))
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

        self.tintConstant = Vec4(.25,.25,.25,0)
        self.ghostConstant = Vec4(0,0,0,.5)

      
        self.knockSound = base.loadSfx("phase_5/audio/sfx/GUI_knock_1.mp3")
        self.clickSound = base.loadSfx("phase_3/audio/sfx/GUI_balloon_popup.mp3")
        self.moveSound = base.loadSfx("phase_6/audio/sfx/CC_move.mp3")
        self.accept('stoppedAsleep', self.handleSleep)



        
        

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
        startLoc = self.boardNode.find("**/locators")
        self.locatorList = startLoc.getChildren()

        self.startingPositions = self.locatorList.pop(0)
        self.startingPositions = self.startingPositions.getChildren()


        instancePiece = self.boardNode.find("**/pieces")

        #tag the locators for "picking" ingame
        #also add colision spheres for movement
        tempList = []

        #Start Position locators
        #Up above the board
        for x in range(7):
            self.startingPositions[x].setTag("StartLocator", "%d" % x)
            collNode = CollisionNode("startpicker%d" %x)
            collNode.setIntoCollideMask(BitMask32(0x1000))
            tempList.append(self.startingPositions[x].attachNewNode(collNode))
            tempList[x].node().addSolid(CollisionTube(0,0,.23,0,0,-.23,.2))
        for z in self.startingPositions:
            y = instancePiece.copyTo(z)
            for val in y.getChildren():
                val.hide()
                                           
        tempList = []
        #the peices themselves inside of the board.
        for x in range(42):
            self.locatorList[x].setTag("GamePeiceLocator", "%d" % x)
            collNode = CollisionNode("startpicker%d" %x)
            collNode.setIntoCollideMask(BitMask32(0x1000))
            tempList.append(self.locatorList[x].attachNewNode(collNode))
            tempList[x].node().addSolid(CollisionSphere(0,0,0,.2))
        for z in self.locatorList:
            y = instancePiece.copyTo(z)
            for val in y.getChildren():
                val.hide()


        dummyHide = instancePiece.getParent().attachNewNode("DummyHider")
        instancePiece.reparentTo(dummyHide)
        dummyHide.hide()

    def setName(self, name):
        self.name = name

    def announceGenerate(self): 
        DistributedNode.DistributedNode.announceGenerate(self)
        if self.table.fsm.getCurrentState().getName() != 'observing':
            if base.localAvatar.doId in self.table.tableState: # Fix for strange state #TEMP until i find the cause
                #got to rotate all the peices so that they are facing the side the player is sitting in,
                #this is a byproduct of backface culling && polygon optimization
                self.seatPos = self.table.tableState.index(base.localAvatar.doId)
                if self.seatPos <= 2:
                    for x in self.startingPositions:
                        x.setH(0)
                    for x in self.locatorList:
                        x.setH(0)
                else:
                    for x in self.startingPositions:
                        x.setH(180)
                    for x in self.locatorList:
                        x.setH(180)
            self.moveCameraForGame()
        else:
            self.seatPos = self.table.seatBumpForObserve
            if self.seatPos > 2:
                for x in self.startingPositions:
                    x.setH(180)
                for x in self.locatorList:
                    x.setH(180)
            self.moveCameraForGame()
                
        
    def handleSleep(self, task = None):
        if self.fsm.getCurrentState().getName() == "waitingToBegin":
            self.exitButtonPushed()
        if task != None:
            task.done

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
        taskMgr.remove('playerTurnTask')
        #self.table = None

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
        self.winningSequence.finish()
        taskMgr.remove('playerTurnTask')

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
                self.clockNode.setPos(.64, 0, -0.27)
                self.clockNode.countdown(timeLeft, self.doRandomMove)
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
                self.playerColorString = "Red"
            else:
                self.playerColorString = "Yellow"
            self.moveCameraForGame()
        self.fsm.request('playing')
    def sendTurn(self,playersTurn):
        if self.fsm.getCurrentState().getName() == 'playing':
            if playersTurn == self.playerNum:
                self.isMyTurn = True
                taskMgr.add(self.turnTask, "playerTurnTask")
            self.enableTurnScreenText(playersTurn)

    def illegalMove(self):
        self.exitButtonPushed()
        
    ##########
    ##Move camera
    #
    #Got to move the camera to the specific location in the 3d environment so that the
    #nametags ect do not collide with the gameboard itself.

    #also half to do some if statements on the camera itself so that the camera will not (for instance)
    #rotate 350 degrees when rather it could rotate -10 degrees to get its finishing location
    ##########
    def moveCameraForGame(self): 
        if self.table.cameraBoardTrack.isPlaying():
            self.table.cameraBoardTrack.pause()
        rotation = 0
        if self.seatPos <= 2:
            position = self.table.seats[1].getPos()
            position = position + Vec3(0,-8,12.8)
            int  = LerpPosHprInterval(camera, 2, position, Vec3(0, -38, 0), camera.getPos(), camera.getHpr())
        else:
            position = self.table.seats[4].getPos()
            position = position + Vec3(0,-8,12.8)
            if camera.getH() < 0 :
                int  = LerpPosHprInterval(camera, 2, position, Vec3(-180, -20, 0), camera.getPos(), camera.getHpr())
            else:
                int  = LerpPosHprInterval(camera, 2, position, Vec3(180, -20, 0), camera.getPos(), camera.getHpr())
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
            pos = (.92, 0, 0.80),
            scale = 0.15,
            command = lambda self=self: self.exitButtonPushed(),
            )
        return
    def enableScreenText(self):
        defaultPos = (-.7, -0.29)
        if self.playerNum == 1:
            message = "You are Red"
            color = Vec4(1,0,0,1)
        elif self.playerNum == 2:
            message = "You are Yellow"
            color = Vec4(1,1,0,1)
        else:
            message = TTLocalizer.CheckersObserver
            color = Vec4(0,0,0,1)
            #defaultPos = (-.80, -0.25)
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
            pos = (.92, 0, 0.57),
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
            pos = (.92, 0, 0.8),
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
                  message2 = "Red's Turn"
                  color = (1,0,0,1)
              elif player == 2:
                  message2 = "Yellow's Turn"
                  color = (1,1,0,1)
        self.turnText = OnscreenText(text = message1+message2, pos = (-0.7, -0.39), scale = 0.092,fg=color,align=TextNode.ACenter,mayChange=1)

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
    #These functions handle all of the mouse clicking functions
    #Its best to look through the code for comments for it to make
    #the most sense.
    #
    #The self.blinker that is referenced in these functions, is a cosmetic
    #colorLerp that gives the player a visual feedback as to what checkers peice
    #he has (currently) selected.
    #
    #
    #mouseClick is just an extention to the Task that is generated whenever it is your turn -
    #mouseClick simply commits the move that you have been deciding upon inside of the 'playerTurnTask"
    ##########
    def mouseClick(self):
        messenger.send('wakeup')
        if self.isMyTurn == True and self.inGame == True and not self.moveSequence.isPlaying(): #cant pick stuff if its not your turn
            if self.moveCol != None:
                self.d_requestMove(self.moveCol)
                self.moveCol = None
                self.isMyTurn = False
                taskMgr.remove('playerTurnTask')
            
    def handleClicked(self, index):
        pass

    #This is the wonderul task that handles the magic for the selecting of the game piece
    #it is important to note that this task gets spawned up whenever it is deemed your turn
    #by the sendTurn stuff

    #I had to make some optimizations to not make this task completely bogg down the computer
    #(1) set the bit masks for the collision traverser so that it will not even test anything that
    #is not a collision sphere for the findFour Game
    def turnTask(self, task):

        if base.mouseWatcherNode.hasMouse() == False:
            return task.cont
        if self.isMyTurn == False:
            return task.cont
        if self.moveSequence.isPlaying():
            return task.cont


        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode,mpos.getX(), mpos.getY())
        
        self.traverser.traverse(render)
        if self.myHandler.getNumEntries() > 0:
            self.myHandler.sortEntries()#get the closest Object
            pickedObj = self.myHandler.getEntry(0).getIntoNodePath()
            #will return the INT for the locator node closest parent 
            pickedObj = pickedObj.getNetTag("StartLocator")
            if pickedObj: #make sure something actually was "picked"
                colVal = int(pickedObj)
                if colVal == self.moveCol:
                    return task.cont
                if self.board[0][colVal] == 0: #it is a legal move
                    if self.moveCol != None:
                        for x in self.startingPositions[self.moveCol].getChild(1).getChildren(): #hide the old peices
                            x.hide()
                    self.moveCol = colVal
                    if self.playerNum == 1:
                        self.startingPositions[self.moveCol].getChild(1).getChild(2).show()
                    elif self.playerNum == 2:
                        self.startingPositions[self.moveCol].getChild(1).getChild(3).show()
        return task.cont
                     
  
    def d_requestMove(self, moveCol):
        self.sendUpdate('requestMove', [moveCol])

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
    def setGameState(self, tableState, moveCol, movePos, turn):
        messenger.send('wakeup')

        ##Funny if statement #1
        #This slew of statements is to handle a specific case that looks funny
        #when a client joins the game (to observe) after the game has begun
        #
        #If you notice, you will see that the movePos and the MoveCol are parts
        #of the game state (required RAM), so when a client joins this game asynchrinously
        #they too will see the last moves animation as they are sitting down at the table.
        #
        # These slew of if statements are to handle that fact, by testing the state of the
        #current game board, as well as the state of the board that was handed to the client
        #through the DC message.
        if self.table.fsm.getCurrentState().getName() == 'observing':
            isBlank = True
            for x in range(7):
                if self.board[5][x] != 0:
                    isBlank = False
                    break

            gameBlank = True
            for x in range(7):
                if tableState[5][x] != 0:
                    gameBlank = False
                    break

            if isBlank == True and gameBlank == False:
                for x in range(6):
                    for y in range(7):
                        self.board[x][y] = tableState[x][y]
                self.updateGameState()
                return
        ###

        #This if statement really doesnt apply unless the board is completely blank!
        if moveCol == 0 and movePos == 0 and turn == 0: #Someones coming in after a Move
            for x in range(6):
                for y in range(7):
                    self.board[x][y] = tableState[x][y]
            self.updateGameState() 
        else: #need to animate because a movePos was given in the Ram Field
            self.animatePeice(tableState, moveCol, movePos, turn)

        #Clients all check if they won in this game, where the AI
        #verifies - to save cycles on the AI server
        didIWin = self.checkForWin()
        if didIWin != None:
            self.sendUpdate("requestWin", [didIWin])
            
    ############################################
    ##UpdateGameState
    #
    #For the games (visual) state, it is important to note that child 0 and child1
    #are the pieces that have been copied and reparented to that node.
    #Really, i just have 2 peices that are in the model, and i hide/show them
    #instead of instantiating them on the fly.
    ##
        
    def updateGameState(self):
        for x in range(6):
            for y in range(7):
                for z in self.locatorList[(x*7)+y].getChild(1).getChildren():
                    z.hide()
        for x in range(6):
            for y in range(7):
                state = self.board[x][y]
                if state == 1:
                    self.locatorList[(x*7) + y ].getChild(1).getChild(0).show()
                elif state == 2:
                    self.locatorList[(x*7) + y ].getChild(1).getChild(1).show()

    ##########
    ##CheckForWin
    #
    #This function is pretty self explanitory, it checks all of the directions for
    #all of the pieces on the players current boardState to check for a win.
    #
    #this is needed because programming wise it would be a disgusting case to test
    #for a win if a peice is in the middle of a (4) piece run - Rather it is easier
    #to simply test all the pieces whether or not they are on the Edge of a win,
    #thus making the code 1000% easier to read and understand.
    ###
    def checkForWin(self):
        for x in range(6):
            for y in range(7):
                if self.board[x][y] == self.playerNum:
                     if  self.checkHorizontal(x,y,self.playerNum) == True:
                         return [x,y]
                     elif self.checkVertical(x,y,self.playerNum) == True:
                         return [x,y]
                     elif self.checkDiagonal(x,y,self.playerNum) == True:
                         return [x,y]
        return None
    ###########
    ##AnnounceWinnerPosition
    #
    #Fancy function that is called after the AI determines the players' request was
    #in deed a true win.
    #
    #This function does all of the animations for the blinking after a person wins
    #
    #Also - Note that there are two separate functions for finding/checking a win.
    #
    #check(direction) - returns true or false
    #find(direction) - returns the list of 4 ints if win and [] for no win
    ###
    def announceWinnerPosition(self, x, y, winDirection,playerNum):
        self.isMyturn = False
        if self.turnText:
            self.turnText.hide()
        self.clockNode.stop()
        self.clockNode.hide()
        
        if winDirection == 0:
            blinkList = self.findHorizontal(x,y,playerNum)
        elif winDirection == 1:
            blinkList = self.findVertical(x,y,playerNum)
        elif winDirection == 2:
            blinkList = self.findDiagonal(x,y,playerNum)

        if blinkList != []:
            print blinkList
            val0 = (x*7) + y
            
            x = blinkList[0][0]
            y = blinkList[0][1]
            val1 = (x *7) + y

            x = blinkList[1][0]
            y = blinkList[1][1]
            val2 = (x *7) + y

            x = blinkList[2][0]
            y = blinkList[2][1]
            val3 = (x *7) + y



            self.winningSequence = Sequence()
            downBlinkerParallel = Parallel( LerpColorInterval(self.locatorList[val0], .3, Vec4(.5,.5,.5,.5), Vec4(1,1,1,1)),
                                                                LerpColorInterval(self.locatorList[val1], .3, Vec4(.5,.5,.5,.5), Vec4(1,1,1,1)),
                                                                LerpColorInterval(self.locatorList[val2], .3, Vec4(.5,.5,.5,.5), Vec4(1,1,1,1)),
                                                                LerpColorInterval(self.locatorList[val3], .3, Vec4(.5,.5,.5,.5), Vec4(1,1,1,1)))
            upBlinkerParallel = Parallel( LerpColorInterval(self.locatorList[val0], .3, Vec4(1,1,1,1), Vec4(.5,.5,.5,.5)),
                                                            LerpColorInterval(self.locatorList[val1], .3, Vec4(1,1,1,1), Vec4(.5,.5,.5,.5)),
                                                            LerpColorInterval(self.locatorList[val2], .3, Vec4(1,1,1,1), Vec4(.5,.5,.5,.5)),
                                                            LerpColorInterval(self.locatorList[val3], .3, Vec4(1,1,1,1), Vec4(.5,.5,.5,.5)))
                                                               
            
            self.winningSequence.append(downBlinkerParallel)
            self.winningSequence.append(upBlinkerParallel)
            self.winningSequence.loop()
    ##########
    ##Tie
    #
    #This is the function that sends the tie message, and animates the whole board in a fun way such that
    #dictates that a tie has occurred
    ###
    def tie(self):
        self.tieSequence = Sequence(autoFinish = 1)
        self.clockNode.stop()
        self.clockNode.hide()
        self.isMyTurn = False
        self.moveSequence.finish()

        if self.turnText:
            self.turnText.hide()
        for x in range(41):
            self.tieSequence.append(Parallel(LerpColorInterval(self.locatorList[x],.15, Vec4(.5,.5,.5,.5), Vec4(1,1,1,1)),
                                                                    LerpColorInterval(self.locatorList[x],.15,Vec4(1,1,1,1), Vec4(.5,.5,.5,.5))))

        whisper = WhisperPopup("This Find Four game has resulted in a Tie!",
                                       OTPGlobals.getInterfaceFont(),
                                       WhisperPopup.WTNormal)
        whisper.manage(base.marginManager)
        self.tieSequence.start()
        
       
    def hideChildren(self, nodeList):
        pass
    ##########
    ##animatePiece
    #
    #Function that handles the animation of the next move, as well as sets the current
    #view of the board so that the player can see it
    def animatePeice(self, tableState, moveCol, movePos, turn):
        messenger.send('wakeup')

        #update the board state from DC parent function
        for x in range(6):
            for y in range(7):
                self.board[x][y] = tableState[x][y]

        #show  the column piece that was selected for the move
        pos = self.startingPositions[moveCol].getPos()
        if turn == 0:
            peice = self.startingPositions[moveCol].getChild(1).getChildren()[2]
            peice.show()
        elif turn == 1:
            peice = self.startingPositions[moveCol].getChild(1).getChildren()[3]
            peice.show()
            
        #animate the thing
        self.moveSequence = Sequence()
        startPos = self.startingPositions[moveCol].getPos()
        arrayLoc = (movePos * 7) + moveCol
        self.moveSequence.append(LerpPosInterval(self.startingPositions[moveCol], 1.5, self.locatorList[arrayLoc].getPos(self), startPos))

        self.moveSequence.append(Func(peice.hide))
        self.moveSequence.append(Func(self.startingPositions[moveCol].setPos, startPos))
        self.moveSequence.append(Func(self.updateGameState))
        self.moveSequence.start()
        
        
       
    def announceWin(self, avId):
        self.fsm.request('gameOver')
    ##########
    ##doRandomMove
    #
    #For this game, doRandom move will as well fire when the turnTimer runs out - but will also,
    #(if the player has been debating pieces with his cursor), will commite the last selected piece
    #by the 'playerTurnTask'
    #
    #It is also smart enough to not randomly commit an illegal move :)
    ###########
    def doRandomMove(self):
        if self.isMyTurn:
            if self.moveCol != None:
                self.d_requestMove(self.moveCol)
                self.moveCol = None
                self.isMyTurn = False
                taskMgr.remove('playerTurnTask')
            else:
                hasfound = False
                while hasfound == False:
                    from random import *
                    x = randint(0,6)
                    if self.board[0][x] == 0:
                        self.d_requestMove(x)
                        self.moveCol = None
                        self.isMyTurn = False
                        taskMgr.remove('playerTurnTask')
                        hasfound = True
                             
    def doNothing(self):
        pass

    ##########
    ##Large slew of check/find Functions
    #
    #I would suggest getting out paper to analyze how these things work, but hopefully
    #with a bit of ASCII art and some explaining it wont be too bad.
    #
    # Game board is represented as such in memory (as you see it in real life):
    # |0 0 0 0 0 0 0 |   0 1 2 3 4 5 6
    # |0 0 0 0 0 0 0 | 0 . . . . . . .
    # |0 0 0 0 0 0 0 | 1 . . . . . . .
    # |0 0 0 0 0 0 0 | 2 . . . . . . .
    # |0 0 0 0 0 0 0 | 3 . . . . . . .
    # |0 0 0 0 0 0 0 | 4 . . . . . . .
    #                  5 . . . . . . .
    #
    #
    # as you can see, (0,0) is in the top left corner, and just makes things easier to write about
    #because the locators, and lists seem to function well in this sense
    # board state looks like [ [0,0,0,0,0,0,0],
    #                          [0,0,0,0,0,0,0],
    #                          [0,0,0,0,0,0,0],
    #                          [0,0,0,0,0,0,0],
    #                          [0,0,0,0,0,0,0],
    #                          [0,0,0,0,0,0,0] ]
    #
    #
    #So when looking at this code just keep in mind this is how the board is working in memory
    #
    #Also, important to see that there are two types of functions here
    #(1) the check(direction) functions who return true or false whether or not they detect
    #    a win in that direction
    #(2) the find(direction) functions who return the list of where they detected a win
    #    or [ ] if they found nothing.
    ##

    def checkHorizontal(self, rVal, cVal, playerNum):
        if cVal == 3:
            for x in range(1,4):
                if self.board[rVal][cVal-x] != playerNum:
                    break
                if self.board[rVal][cVal-x] == playerNum and x == 3:
                    return True     
            for x in range(1,4):
                if self.board[rVal][cVal + x] != playerNum:
                    break
                if self.board[rVal][cVal+x] == playerNum and x == 3:
                    return True
            return False
        elif cVal == 2:
            for x in range(1,4):
                if self.board[rVal][cVal + x] != playerNum:
                    break
                if self.board[rVal][cVal+x] == playerNum and x == 3:
                    return True
            return False
        elif cVal == 4:
            for x in range(1,4):
                if self.board[rVal][cVal-x] != playerNum:
                    break
                if self.board[rVal][cVal-x] == playerNum and x == 3:
                    return True
            return False
        else:
            return False
    def checkVertical(self, rVal, cVal, playerNum):
        if rVal == 2:
            for x in range(1,4):
                if self.board[rVal+x][cVal] != playerNum:
                    break
                if self.board[rVal+x][cVal] == playerNum and x == 3:
                    return True
            return False
        elif rVal == 3:
             for x in range(1,4):
                if self.board[rVal-x][cVal] != playerNum:
                    break
                if self.board[rVal-x][cVal] == playerNum and x == 3:
                    return True
             return False
        else:
            return False
    def checkDiagonal(self, rVal, cVal, playerNum):
        if cVal <= 2: #Cannot have Left Diagonals
            if rVal == 2:#cannot have upper Diagonal
                for x in range(1,4):
                    if self.board[rVal+x][cVal+x] != playerNum:
                        break
                    if self.board[rVal+x][cVal+x] == playerNum and x == 3:
                        return True
                return False
            elif rVal == 3: #cannot have downard diagonal
                for x in range(1,4):
                     if self.board[rVal-x][cVal+x] != playerNum:
                        break
                     if self.board[rVal-x][cVal+x] == playerNum and x == 3:
                         return True
                return False
        elif cVal >= 4:
            if rVal == 2:#cannot have upper Diagonal
                for x in range(1,4):
                    if self.board[rVal+x][cVal-x] != playerNum:
                        break
                    if self.board[rVal+x][cVal-x] == playerNum and x == 3:
                        return True
                return False
            elif rVal == 3: #cannot have downard diagonal
                for x in range(1,4):
                     if self.board[rVal-x][cVal-x] != playerNum:
                        break
                     if self.board[rVal-x][cVal-x] == playerNum and x == 3:
                         return True
                return False
        else: #we are in column 3
            if rVal == 3 or rVal == 4 or rVal == 5: #we have 2 upward Diagonals
                for x in range(1,4):#Up left
                     if self.board[rVal-x][cVal-x] != playerNum:
                        break
                     if self.board[rVal-x][cVal-x] == playerNum and x == 3:
                         return True
                for x in range(1,4):
                     if self.board[rVal-x][cVal-x] != playerNum:
                        break
                     if self.board[rVal-x][cVal-x] == playerNum and x == 3:
                         return True
                return False
            elif rVal == 0 or rVal == 1 or rVal == 2:
                for x in range(1,4):#down left
                     if self.board[rVal+x][cVal-x] != playerNum:
                        break
                     if self.board[rVal+x][cVal-x] == playerNum and x == 3:
                         return True
                for x in range(1,4):
                     if self.board[rVal+x][cVal+x] != playerNum:
                        break
                     if self.board[rVal+x][cVal+x] == playerNum and x == 3:
                         return True
                return False
        return False
#######################################

    def findHorizontal(self, rVal, cVal, playerNum):
        if cVal == 3:
            retList = []
            for x in range(1,4):
                retList.append([rVal, cVal-x])
                if self.board[rVal][cVal-x] != playerNum:
                    retList = []
                    break
                if self.board[rVal][cVal-x] == playerNum and x == 3:
                    return retList
            for x in range(1,4):
                retList.append([rVal, cVal+x])
                if self.board[rVal][cVal + x] != playerNum:
                    retList = []
                    break
                if self.board[rVal][cVal+x] == playerNum and x == 3:
                    return retList
            return []
        elif cVal == 2:
            retList = []
            for x in range(1,4):
                retList.append([rVal, cVal+x])
                if self.board[rVal][cVal + x] != playerNum:
                    retList = []
                    break
                if self.board[rVal][cVal+x] == playerNum and x == 3:
                    return retList
            return []
        elif cVal == 4:
            retList = []
            for x in range(1,4):
                retList.append([rVal, cVal-x])
                if self.board[rVal][cVal-x] != playerNum:
                    retList = []
                    break
                if self.board[rVal][cVal-x] == playerNum and x == 3:
                    return retList
            return []
        else:
            return []
    def findVertical(self, rVal, cVal, playerNum):
        if rVal == 2:
            retList = []
            for x in range(1,4):
                retList.append([rVal+x, cVal])
                if self.board[rVal+x][cVal] != playerNum:
                    retList = []
                    break
                if self.board[rVal+x][cVal] == playerNum and x == 3:
                    return retList
            return []
        elif rVal == 3:
            retList = []
            for x in range(1,4):
                retList.append([rVal-x, cVal])
                if self.board[rVal-x][cVal] != playerNum:
                    retList = []
                    break
                if self.board[rVal-x][cVal] == playerNum and x == 3:
                    return retList
            return []
        else:
            return []
    def findDiagonal(self, rVal, cVal, playerNum):
        retList = []
        if cVal <= 2: #Cannot have Left Diagonals
            if rVal == 2:#cannot have upper Diagonal
                for x in range(1,4):
                    retList.append([rVal+x , cVal+x])
                    if self.board[rVal+x][cVal+x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal+x][cVal+x] == playerNum and x == 3:
                        return retList
                return []
            elif rVal == 3: #cannot have downard diagonal
                for x in range(1,4):
                    retList.append([rVal-x , cVal+x])
                    if self.board[rVal-x][cVal+x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal-x][cVal+x] == playerNum and x == 3:
                        return retList
                return []
        elif cVal >= 4:
            if rVal == 2:#cannot have upper Diagonal
                for x in range(1,4):
                    retList.append([rVal+x , cVal-x])
                    if self.board[rVal+x][cVal-x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal+x][cVal-x] == playerNum and x == 3:
                        return retList
                return []
            elif rVal == 3: #cannot have downard diagonal
                for x in range(1,4):
                    retList.append([rVal-x , cVal-x])
                    if self.board[rVal-x][cVal-x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal-x][cVal-x] == playerNum and x == 3:
                        return retList
                return []
        else: #we are in column 3
            if rVal == 3 or rVal == 4 or rVal == 5: #we have 2 upward Diagonals
                for x in range(1,4):#Up left
                    retList.append([rVal-x , cVal-x])
                    if self.board[rVal-x][cVal-x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal-x][cVal-x] == playerNum and x == 3:
                        return retList
                for x in range(1,4):
                    retList.append([rVal+x , cVal-x])
                    if self.board[rVal+x][cVal-x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal+x][cVal-x] == playerNum and x == 3:
                        return retList
                return []
            elif rVal == 0 or rVal == 1 or rVal == 2:
                for x in range(1,4):#down left
                    retList.append([rVal+x , cVal-x])
                    if self.board[rVal+x][cVal-x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal+x][cVal-x] == playerNum and x == 3:
                        return retList
                for x in range(1,4):
                    retList.append([rVal+x , cVal+x])
                    if self.board[rVal+x][cVal+x] != playerNum:
                        retList = []
                        break
                    if self.board[rVal+x][cVal+x] == playerNum and x == 3:
                        return retList
                return []
        return []
