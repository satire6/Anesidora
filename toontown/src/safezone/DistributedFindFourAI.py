from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *



class DistributedFindFourAI(DistributedNodeAI):
    def __init__(self, air, parent, name, x, y, z, h, p, r):
        DistributedNodeAI.__init__(self,air)
        self.name = name
        self.air = air

        self.setPos(x,y,z)
        self.setHpr(h,p,r)

        self.myPos = (x,y,z)
        self.myHpr = (h,p,r)
        self.board = [ [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0] ]

        self.parent = self.air.doId2do[parent]
        self.parentDo = parent
        self.wantStart = []
        self.playersPlaying = []
        self.playersSitting = 0
        self.playersTurn = 1
        self.movesMade = 0
        self.playerNum = 1
        self.winDirection = None

        #players game positions (separate from where they are sitting down
        self.playersGamePos = [None, None]
        
        self.wantTimer = True
        self.timerEnd = 0
        self.turnEnd = 0
        
        self.playersObserving = []
        #Arbitrary numbers - can Adjust to feel
        self.winLaffPoints = 20
        self.movesRequiredToWin = 10
        
        self.zoneId = self.air.allocateZone()
        self.generateOtpObject(air.districtId, self.zoneId, optionalFields = ["setX","setY","setZ", "setH", "setP", "setR"])
        #sets the ZoneId in the parent table so when people sit down they know what zone to add
        #interest to when they sit down
        self.parent.setCheckersZoneId(self.zoneId)
        
        #parent.b_setCurrentGameId(self.doId)

        #Starting indexes inside of board for setting starting positions

        self.timerStart = None


        self.fsm = ClassicFSM.ClassicFSM('Checkers',
                                         [State.State('waitingToBegin',
                                                      self.enterWaitingToBegin,
                                                      self.exitWaitingToBegin,
                                                      ['playing']),
                                          State.State('playing',
                                                      self.enterPlaying,
                                                      self.exitPlaying,
                                                      ['gameOver']),
                                          State.State('gameOver',
                                                      self.enterGameOver,
                                                       self.exitGameOver,
                                                      ['waitingToBegin'])],
                                      #start state
                                      'waitingToBegin',
                                      #final state
                                      'waitingToBegin',
                                      )


        
        self.fsm.enterInitialState()
        #self.setGameCountownTime()

    def announceGenerate(self):
        self.parent.setGameDoId(self.doId)
    def getTableDoId(self):
        return self.parentDo
    def delete(self):
        self.fsm.requestFinalState()
        self.parent = None
        self.parentDo = None
        del self.board
        del self.fsm
        DistributedNodeAI.delete(self)


    #########################################################################
    ##Inform of player and leave
    #
    #These functions are called by the table in the event of a player leave/join
    #this is necessary so that the game may have an accurate count of who is in the table
    #as well as a function that will fire upon single "deltas" of the table state
    #
    #Table state with avId(s) will be updated via setTableState as well as this
    #function being called
    ####
    def informGameOfPlayer(self):
        self.playersSitting += 1
        if self.playersSitting < 2:
            self.timerEnd = 0
        elif self.playersSitting == 2:
            self.timerEnd = globalClock.getRealTime() + 20
            self.parent.isAccepting = False
            self.parent.sendUpdate("setIsPlaying", [1])  # 1 is true
        elif self.playersSitting > 2:
            pass
        self.sendUpdate("setTimer", [globalClockDelta.localToNetworkTime(self.timerEnd)])
        
    def informGameOfPlayerLeave(self):
        self.playersSitting -= 1
        if self.playersSitting < 2 and self.fsm.getCurrentState().getName() == 'waitingToBegin':
            self.timerEnd = 0
            self.parent.isAccepting = True
            self.parent.sendUpdate("setIsPlaying", [0])  # 1 is true
        if self.playersSitting > 2 and self.fsm.getCurrentState().getName() == 'waitingToBegin':
            pass
        else:
            self.timerEnd = 0
        if self.timerEnd != 0:
            self.sendUpdate("setTimer", [globalClockDelta.localToNetworkTime(self.timerEnd)])
        else:
            self.sendUpdate("setTimer", [0])
    ###########################################################################
    ##Timer Functions for game
    #
    #These timer functions encapsulate the "timer" functions needed for the game table.
    #   getTimer - is the timer for sitting down and beginning the game
    #   getTurnTimer - gets and sets the turn timer for players moves
    ###
    def setGameCountdownTime(self):
        self.timerEnd = globalClock.getRealTime() + 10
    def setTurnCountdownTime(self):
        self.turnEnd = globalClock.getRealTime() + 25
    def getTimer(self):
        if self.timerEnd != 0:
           return 0 
        else:
            return 0
    def getTurnTimer(self):
        return globalClockDelta.localToNetworkTime(self.turnEnd)
    def requestTimer(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, "setTimer", [globalClockDelta.localToNetworkTime(self.timerEnd)])
    ###########################################################################
    ##handlePlayerExit and handleEmptyGame
    #
    #handlePlayerExit is the mother function that gets called when a player requests to leave an "active" game
    #of chinese checkers - there are many special cases here, comments inside the function itself.
    ###    
        
    def handlePlayerExit(self, avId):
        if avId in self.wantStart:
            self.wantStart.remove(avId)
        if self.fsm.getCurrentState().getName() ==  'playing':
        #Get the players Current "player" position in Chinese Checkers
            gamePos  = self.playersGamePos.index(avId)
            self.playersGamePos[gamePos] = None
            self.fsm.request('gameOver')
            
    def handleEmptyGame(self):
        self.movesMade = 0
        self.playersPlaying = []
        self.playersTurn = 1
        self.playerNum = 1
        self.fsm.request('waitingToBegin')
        self.parent.isAccepting = True
    ###############################################################
    ##Request win and distributed Laugh points
    #
    #This function explicitly tests for a player (that requested he won)
    #and checks to see if his peices equal that of his opposite
    ##
    def requestWin(self, pieceNum):
        avId = self.air.getAvatarIdFromSender()
        playerNum = self.playersGamePos.index(avId)+1
        x = pieceNum[0]
        y = pieceNum[1]
        if self.checkWin(x,y,playerNum)  == True:
            self.sendUpdate("announceWinnerPosition",  [x,y,self.winDirection,playerNum])
            winnersSequence = Sequence(Wait(5.0), Func(self.fsm.request, 'gameOver'),Func(self.parent.announceWinner, "Find Four", avId))
            winnersSequence.start()
        else:
            self.sendUpdateToAvatarId(avId, "illegalMove", [])
    
              
        
    def distributeLaffPoints(self):
        for x in self.parent.seats:
            if x != None:
                av = self.air.doId2do.get(x)
                av.toonUp(self.winLaffPoints)

    ##################################################################
    #                 Find Four FSM
    #
    #The FSM is primarily to keep track of buttons/screen text, but also
    #serves the purpose of resetting variables upon game over ect.
    ###
    def enterWaitingToBegin(self):
        self.setGameCountdownTime()
        self.parent.isAccepting = True

    def exitWaitingToBegin(self):
        self.turnEnd = 0
    def enterPlaying(self):
        self.parent.isAccepting = False
        for x in self.playersGamePos:
            if x != None:
                self.playersTurn = self.playersGamePos.index(x)
                self.d_sendTurn(self.playersTurn+1)
                break
        
        self.setTurnCountdownTime()
        self.sendUpdate("setTurnTimer", [globalClockDelta.localToNetworkTime(self.turnEnd)])
    def exitPlaying(self):
        pass
    def enterGameOver(self):
        #self.playersObserving = []
        self.timerEnd = 0
        isAccepting = True
        self.parent.handleGameOver()
        self.playersObserving = []
        self.playersTurn = 1
        self.playerNum = 1
        self.playersPlaying = []
        #self.clearBoard()
        #self.sendGameState( [] )
        self.movesMade = 0
        self.playersGamePos = [None, None]
        self.parent.isAccepting = True
        self.fsm.request('waitingToBegin')
    def exitGameOver(self):
        pass

    ##################################################################
    #                    Game Start/begin logic
    #Game start just assigns people as player1 or player0
    #
    #Request begin is sent by every avatar when either (1) they click the go button
    #or when their start timer runs out
    ###
    def requestBegin(self):
        avId = self.air.getAvatarIdFromSender()
        if not( avId in self.wantStart ):
            self.wantStart.append(avId)
        numPlayers = 0
        for x in self.parent.seats:
            if x != None:
                numPlayers = numPlayers + 1
        if len(self.wantStart) == numPlayers and numPlayers >= 2:
            self.d_gameStart(avId)
            self.parent.sendIsPlaying()
    def d_gameStart(self,avId):
        #255 is a special value just telling the client that he is an Observer
        for x in self.playersObserving:
            self.sendUpdateToAvatarId(x, "gameStart", [255])            
        zz = 0
        numPlayers = 0
        for x in self.parent.seats:
            if x != None:
                numPlayers += 1
                self.playersPlaying.append(x)
        if numPlayers == 2:
            player1 = self.playersPlaying[0] 
            self.sendUpdateToAvatarId(player1, "gameStart", [1])
            self.playersGamePos[0] = player1

                
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [2])
            self.playersGamePos[1] = player2
     
        #self.sendGameState( [] )
        self.wantStart = []
        self.fsm.request('playing')
        self.parent.getTableState()
    def d_sendTurn(self,playersTurn):
        self.sendUpdate("sendTurn", [playersTurn])

    ##################################################################
    #                    Legal Move Request/Checker
    #
    #All this simply does is swap the players turn
    #no sense really adding and what not since it is
    #a two player game.
    ####
    def advancePlayerTurn(self):
        if self.playersTurn == 0:
            self.playersTurn = 1
            self.playerNum = 2
        else:
            self.playerNum = 1
            self.playersTurn = 0
    ###########
    ##requestMove
    #
    #this is the function that controls all of the checking of logic after the clients submit
    #moves for them to make
    #
    #read code for functionality
    ###
                 
    def requestMove(self, moveColumn):
        avId = self.air.getAvatarIdFromSender()
        turn = self.playersTurn
        if avId in self.playersGamePos: #good hes at least playing
            if self.playersGamePos.index(avId) != self.playersTurn:
                pass #if hes submitting a move not during his turn DO SOMETHING BAD IN THE FUTURE
        if self.board[0][moveColumn] != 0:
             self.sendUpdateToAvatarId(avId, "illegalMove", [])# do something bad. Hes trying to fill an alraedy full column SHOULD NEVER EVER HAPPEN the functions on the AI and the client are identical to check for legality

        #find the lowest spot in the column that is empty
        #and set the boardstate and movepos to that
        for x in range(6):
            if self.board[x][moveColumn] == 0:
                movePos = x
        self.board[movePos][moveColumn] = self.playersTurn +1

        #check for a tie, and if so distribute it and return 
        if self.checkForTie() == True:
            self.sendUpdate('setGameState', [self.board, moveColumn, movePos, turn])
            self.sendUpdate("tie", [])
            winnersSequence = Sequence(Wait(8.0), Func(self.fsm.request, 'gameOver'))
            winnersSequence.start()
            return

        self.movesMade += 1
        self.advancePlayerTurn()
        self.setTurnCountdownTime()
        self.sendUpdate("setTurnTimer", [globalClockDelta.localToNetworkTime(self.turnEnd)])
        self.d_sendTurn(self.playersTurn + 1)


        self.sendUpdate('setGameState', [self.board, moveColumn, movePos, turn])

    def checkForTie(self):
        for x in range(7):
            if self.board[0][x] == 0:
                return False
        return True

###################
    def getState(self):
        return self.fsm.getCurrentState().getName()
    
    def getName(self):
        return self.name                   
   
        
    def getGameState(self):\
          return [self.board, 0,0,0 ]
    


    def clearBoard(self):
        for x in self.board.squareList:
            x.setState(0)


    def getPosHpr(self):
        return self.posHpr

    def tempSetBoardState(self):

        self.board = [ [0,0,0,0,0,0,0],
                               [1,2,1,2,2,2,1],
                               [2,2,1,2,1,2,1],
                               [2,1,1,2,2,1,2],
                               [1,2,2,1,2,1,1],
                               [1,2,1,2,1,2,1] ]
        self.sendUpdate('setGameState', [self.board, 0,0, 1])

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
    
    def checkWin(self, rVal, cVal, playerNum):
         if  self.checkHorizontal(rVal,cVal,playerNum) == True:
             self.winDirection = 0
             return True
         elif self.checkVertical(rVal,cVal,playerNum) == True:
             self.winDirection = 1
             return True
         elif self.checkDiagonal(rVal,cVal,playerNum) == True:
             self.winDirection = 2
             return True
         else:
             self.winDirection = None
             return False
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
                     if self.board[rVal+x][cVal-x] != playerNum:
                        break
                     if self.board[rVal+x][cVal-x] == playerNum and x == 3:
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
                
