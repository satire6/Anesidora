from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from direct.distributed.ClockDelta import *
from toontown.safezone import ChineseCheckersBoard


class DistributedChineseCheckersAI(DistributedNodeAI):
    def __init__(self, air, parent, name, x, y, z, h, p, r):
        DistributedNodeAI.__init__(self,air)
        self.name = name
        self.air = air

        self.setPos(x,y,z)
        self.setHpr(h,p,r)

        self.myPos = (x,y,z)
        self.myHpr = (h,p,r)
        self.board = ChineseCheckersBoard.ChineseCheckersBoard()

        self.parent = self.air.doId2do[parent]
        self.parentDo = parent
        self.wantStart = []
        self.playersPlaying = []
        self.playersSitting = 0
        self.playersTurn = 1
        self.movesMade = 0

        #players game positions (separate from where they are sitting down
        self.playersGamePos = [None, None, None, None, None, None]
        
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
        self.startingPositions = [[0,1,2,3,4,5,6,7,8,9],
                                  [10,11,12,13,23,24,25,35,36,46],
                                  [65,75,76,86,87,88,98,99,100,101],
                                  [111,112,113,114,115,116,117,118,119,120],
                                  [74,84,85,95,96,97,107,108,109,110],
                                  [19,20,21,22,32,33,34,44,45,55]]
        self.timerStart = None


        self.fsm = ClassicFSM.ClassicFSM('ChineseCheckers',
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
        #print "PARENT -- ", self.parent
        return self.parentDo
    def delete(self):
        self.fsm.requestFinalState()
        self.board.delete()
        self.playerSeatPos = None
        del self.fsm
        #simbase.air.deallocateZone(self.zoneId)
        DistributedNodeAI.delete(self)


    def requestSeatPositions(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, "announceSeatPositions", [self.playerSeatPos])
        self.sendUpdateToAvatarId(avId, "sendTurn", [self.playersTurn +1])
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
            self.timerEnd = globalClock.getRealTime() + 60
        elif self.playersSitting > 2:
            pass
        self.sendUpdate("setTimer", [globalClockDelta.localToNetworkTime(self.timerEnd)])
        
    def informGameOfPlayerLeave(self):
        self.playersSitting -= 1
        #print "PLAYERSIT", self.playersSitting
        if self.playersSitting < 2 and self.fsm.getCurrentState().getName() == 'waitingToBegin':
            self.timerEnd = 0
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
        self.timerEnd = globalClock.getRealTime() + 60
    def setTurnCountdownTime(self):
        self.turnEnd = globalClock.getRealTime() + 60
    def getTimer(self):
        if self.timerEnd != 0:
           return 0 
           # return globalClockDelta.localToNetworkTime(self.timerEnd)
        else:
            return 0
    def getTurnTimer(self):
        return globalClockDelta.localToNetworkTime(self.turnEnd)
       # return globalClockDelta.localToNewtorkTime(self.turnTimerEnd)
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
        playerOrder = [1,4,2,5,3,6]
        if avId in self.wantStart:
            self.wantStart.remove(avId)
        playstate = self.fsm.getStateNamed('playing')
        if self.fsm.getCurrentState().getName() ==  'playing':
        #Get the players Current "player" position in Chinese Checkers
            gamePos  = self.playersGamePos.index(avId)
            self.playersGamePos[gamePos] = None
            for x in self.board.squareList:
                if x.getState() == gamePos+1:
                    x.setState(0)
            self.sendGameState( [] )
            if self.playersTurn == gamePos:
                self.advancePlayerTurn()
                self.d_sendTurn(self.playersTurn+1)
            remainingPlayers = 0
            for x in self.playersGamePos:
                if x != None:
                    remainingPlayers += 1
            if remainingPlayers == 1:
                for x in self.playersGamePos:
                    if x != None:
                        self.clearBoard()
                        self.sendGameState( [] )
                        if(self.movesMade >= self.movesRequiredToWin):
                            self.distributeLaffPoints()
                            self.fsm.request('gameOver')
                            self.parent.announceWinner("Chinese Checkers", x)
                        else:
                            self.fsm.request('gameOver')
                        
            
    def handleEmptyGame(self):
        #self.clearBoard()
        self.movesMade = 0
        self.playersPlaying = []
        self.playersTurn = 1
        self.fsm.request('waitingToBegin')
    ###############################################################
    ##Request win and distributed Laugh points
    #
    #This function explicitly tests for a player (that requested he won)
    #and checks to see if his peices equal that of his opposite
    ##
    def requestWin(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.playersGamePos:
            self.air.writeServerEvent('suspicious', avId, 'Has requested a Chinese Checkers win and is NOT playing! SeatList of  the table - %s - PlayersGamePos - %s' % (self.parent.seats, self.playersGamePos))
            return
        requestWinGamePos  = self.playersGamePos.index(avId) + 1
        checkSquares = []
        ##Grab all the tiles with his stamp on them
        for x in self.board.squareList:
            if x.getState() == requestWinGamePos:
                checkSquares.append(x.getNum())
        #explicitly check if they are ==
        if requestWinGamePos == 1:
            if(checkSquares  == self.startingPositions[3]):
                self.distributeLaffPoints()
                self.fsm.request('gameOver')
                self.parent.announceWinner( "Chinese Checkers", avId) 
                #self.sendUpdate('announceWin', [avId])
        elif requestWinGamePos == 2:
            if(checkSquares == self.startingPositions[4]):
               # self.sendUpdate('announceWin', [avId])
               self.distributeLaffPoints()
               self.fsm.request('gameOver')
               self.parent.announceWinner( "Chinese Checkers", avId) 
        elif requestWinGamePos == 3:
            if(checkSquares == self.startingPositions[5]):
                self.distributeLaffPoints()
                self.fsm.request('gameOver')
                self.parent.announceWinner("Chinese Checkers", avId) 
               # self.sendUpdate('announceWin', [avId])
        elif requestWinGamePos == 4:
            if(checkSquares   == self.startingPositions[0]):
                self.distributeLaffPoints()
                self.fsm.request('gameOver')
                self.parent.announceWinner("Chinese Checkers", avId) 
                #self.sendUpdate('announceWin', [avId])
        elif requestWinGamePos == 5:
            if(checkSquares  == self.startingPositions[1]):
                self.fsm.request('gameOver')
                self.parent.announceWinner("Chinese Checkers", avId) 
                #self.sendUpdate('announceWin', [avId])
        elif requestWinGamePos == 6:
            if(checkSquares  == self.startingPositions[2]):
                self.distributeLaffPoints()
                self.fsm.request('gameOver')
                self.parent.announceWinner("Chinese Checkers", avId) 
                 #self.sendUpdate('announceWin', [avId])
        else:
            pass #print "Player requested win, but didnt actually win! OH NOES"
        self.parent = None
            
            
        
    def distributeLaffPoints(self):
        for x in self.parent.seats:
            if x != None:
                av = self.air.doId2do.get(x)
                av.toonUp(self.winLaffPoints)

    ##################################################################
    #                 Chinese Checkers FSM
    #
    #The FSM is primarily to keep track of buttons/screen text, but also
    #serves the purpose of resetting variables upon game over ect.
    ###
    def enterWaitingToBegin(self):
        self.setGameCountdownTime()
        self.parent.isAccepting = True
        #self.clearBoard()
        pass
    def exitWaitingToBegin(self):
        self.turnEnd = 0
    def enterPlaying(self):
        self.parent.isAccepting = False
        for x in self.playersGamePos:
            if x != None:
                self.playersTurn = self.playersGamePos.index(x)
                self.d_sendTurn(self.playersTurn+1)
                break
       #self.d_sendTurn(self.playersTurn)
        self.setTurnCountdownTime()
        self.sendUpdate("setTurnTimer", [globalClockDelta.localToNetworkTime(self.turnEnd)])
        #self.playersTurn += 1 
        
        pass
    def exitPlaying(self):
        pass
    def enterGameOver(self):
        #self.playersObserving = []
        self.timerEnd = 0
        isAccepting = True
        self.playersObserving = []
        self.parent.handleGameOver()
        self.playersTurn = 1
        self.playersPlaying = []
        self.clearBoard()
        self.sendGameState( [] )
        self.movesMade = 0
        self.playersGamePos = [None, None, None, None, None, None]
        #self.parent = None
        self.fsm.request('waitingToBegin')
        
        pass
    def exitGameOver(self):
        pass

    ##################################################################
    #                    Game Start/begin logic
    #
    #Poor style with setting the player starting Positions I know, But
    #is necessary for how the game table must look if odd numbers of people
    #are playing IE (* = blank )
    #     3        4       5
    #   . * .    * . .   . . .   
    #   
    #   * . *    . . *   . . *
    #
    #
    #Request begin is sent by every avatar when either (1) they click the go button
    #or when their start timer runs out
    ###
    def requestBegin(self):
        avId = self.air.getAvatarIdFromSender()
        #av = self.air.doId2do.get(avId)
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
        ###    
            
        playerJoinOrder = [1,4,2,5,3,6]
        zz = 0
        numPlayers = 0
        #print "WANT START", self.wantStart
        #print "SEATS", self.parent.seats
        for x in self.parent.seats:
            if x != None:
                numPlayers += 1
                self.playersPlaying.append(x)
        if numPlayers == 2:
            player1 = self.playersPlaying[0] 
            self.sendUpdateToAvatarId(player1, "gameStart", [1])
            self.playersGamePos[0] = player1
            for x in self.startingPositions[0]:
                self.board.setState(x, 1)
                
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [4])
            self.playersGamePos[3] = player2
            for x in self.startingPositions[3]:
                self.board.setState(x, 4)
                
        elif numPlayers == 3:
            player1 = self.playersPlaying[0]
            self.sendUpdateToAvatarId(player1, "gameStart", [2])
            self.playersGamePos[1] = player1
            for x in self.startingPositions[1]:
                self.board.setState(x,2)
                                      
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [4])
            self.playersGamePos[3] = player2
            for x in self.startingPositions[3]:
                self.board.setState(x,4)
                
            player3 = self.playersPlaying[2]
            self.sendUpdateToAvatarId(player3, "gameStart", [6])
            self.playersGamePos[5] = player3
            for x in self.startingPositions[5]:
                self.board.setState(x,6)
                
        elif numPlayers == 4:
            player1 = self.playersPlaying[0]
            self.sendUpdateToAvatarId(player1, "gameStart", [1])
            self.playersGamePos[0] = player1
            for x in self.startingPositions[0]:
                self.board.setState(x,1)
                                      
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [4])
            self.playersGamePos[3] = player2
            for x in self.startingPositions[3]:
                self.board.setState(x,4)
                
            player3 = self.playersPlaying[2]
            self.sendUpdateToAvatarId(player3, "gameStart", [2])
            self.playersGamePos[1] = player3
            for x in self.startingPositions[1]:
                self.board.setState(x,2)

            player4 = self.playersPlaying[3]
            self.sendUpdateToAvatarId(player4, "gameStart", [5])
            self.playersGamePos[4] = player4
            for x in self.startingPositions[4]:
                self.board.setState(x,5)
        elif numPlayers == 5:
            player1 = self.playersPlaying[0]
            self.sendUpdateToAvatarId(player1, "gameStart", [1])
            self.playersGamePos[0] = player1
            for x in self.startingPositions[0]:
                self.board.setState(x,1)
                                      
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [4])
            self.playersGamePos[3] = player2
            for x in self.startingPositions[3]:
                self.board.setState(x,4)
                
            player3 = self.playersPlaying[2]
            self.sendUpdateToAvatarId(player3, "gameStart", [2])
            self.playersGamePos[1] = player3
            for x in self.startingPositions[1]:
                self.board.setState(x,2)

            player4 = self.playersPlaying[3]
            self.sendUpdateToAvatarId(player4, "gameStart", [5])
            self.playersGamePos[4] = player4
            for x in self.startingPositions[4]:
                self.board.setState(x,5)
                
            player5 = self.playersPlaying[4]
            self.sendUpdateToAvatarId(player5, "gameStart", [3])
            self.playersGamePos[2] = player5
            for x in self.startingPositions[2]:
                self.board.setState(x,3)
        elif numPlayers == 6:
            player1 = self.playersPlaying[0]
            self.sendUpdateToAvatarId(player1, "gameStart", [1])
            self.playersGamePos[0] = player1
            for x in self.startingPositions[0]:
                self.board.setState(x,1)
                                      
            player2 = self.playersPlaying[1]
            self.sendUpdateToAvatarId(player2, "gameStart", [4])
            self.playersGamePos[3] = player2
            for x in self.startingPositions[3]:
                self.board.setState(x,4)
                
            player3 = self.playersPlaying[2]
            self.sendUpdateToAvatarId(player3, "gameStart", [2])
            self.playersGamePos[1] = player3
            for x in self.startingPositions[1]:
                self.board.setState(x,2)

            player4 = self.playersPlaying[3]
            self.sendUpdateToAvatarId(player4, "gameStart", [5])
            self.playersGamePos[4] = player4
            for x in self.startingPositions[4]:
                self.board.setState(x,5)
                
            player5 = self.playersPlaying[4]
            self.sendUpdateToAvatarId(player5, "gameStart", [3])
            self.playersGamePos[2] = player5
            for x in self.startingPositions[2]:
                self.board.setState(x,3)

            player6 = self.playersPlaying[5]
            self.sendUpdateToAvatarId(player6, "gameStart", [6])
            self.playersGamePos[5] = player6
            for x in self.startingPositions[5]:
                self.board.setState(x,6)

        playerSeatPos = [ 0, 0, 0, 0, 0, 0 ] #0 == not taken 1 == green ect.
        for x in range(6):
            id = self.playersGamePos[x]
            if id != None:
                playerSeatPos[self.parent.seats.index(id)] = x+1
        self.sendUpdate("announceSeatPositions", [playerSeatPos])
        self.playerSeatPos = playerSeatPos
        #print "PLAYER SEAT POS!" , playerSeatPos
        self.sendGameState( [] )
        self.wantStart = []
        self.fsm.request('playing')
        self.parent.getTableState()
    def d_sendTurn(self,playersTurn):
        self.sendUpdate("sendTurn", [playersTurn])

    ##################################################################
    #                    Legal Move Request/Checker
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
    def advancePlayerTurn(self):
        foundNewPlayer = False
        while foundNewPlayer == False:
            self.playersTurn += 1
            if self.playersTurn > 5:
                self.playersTurn = 0
            if self.playersGamePos[self.playersTurn] != None:
                foundNewPlayer = True

                 
    def requestMove(self, moveList):
        #Check if its a legal move first
        playerOrder = [1,4,2,5,3,6]
        if(self.checkLegalMoves(moveList) == True):
            self.movesMade += 1
            self.makeMove(moveList)
            self.advancePlayerTurn()
            self.d_sendTurn(self.playersTurn + 1)
            self.setTurnCountdownTime()
            self.sendUpdate("setTurnTimer", [globalClockDelta.localToNetworkTime(self.turnEnd)])

        else:
            pass
            #broadcast to him that its not legal, probably kick him out of
            #game because hes likely cheating
    def checkLegalMoves(self, moveList):
        #check logic .. Really we are assuming client makes a legal move
        #but if he doesnt, he is likely trying to cheat
        #print moveList, "MOVELIST"
        if not moveList:
            return False
        elif self.board.squareList[moveList[0]].getState() == 0:
            return False
        
        for x in range(len(moveList)-1):
            y = self.checkLegalMove(self.board.getSquare(moveList[x]), self.board.getSquare(moveList[x+1]))
            if y == False: 
                return False
        return True
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
                    if (self.board.squareList[x].getAdjacent()[firstSquare.getAdjacent().index(x)]) == secondSquare.getNum():
                        return True
            return False
    def makeMove(self, moveList):
        spot1 = self.board.squareList[moveList[0]].getState()
        self.board.squareList[moveList[0]].setState(0)
        self.board.squareList[moveList[len(moveList)-1]].setState(spot1)
        self.sendGameState( moveList)
###################
    def getState(self):
        return self.fsm.getCurrentState().getName()
    
    def getName(self):
        return self.name                   
   
        
    def getGameState(self):
          return [self.board.getStates(), [] ]
    
    def sendGameState(self, moveList):
        gameState = self.board.getStates()
        self.sendUpdate('setGameState', [gameState, moveList])
        #self.d_setGameState(self.board.getStates())
    

    def clearBoard(self):
        for x in self.board.squareList:
            x.setState(0)
        #self.playersTurn = 0
        #self.playersPlaying = []

    def getPosHpr(self):
        return self.posHpr

    def testWin(self):
        self.clearBoard()
        for x in self.startingPositions[0]:
            self.board.squareList[x].setState(4)
        self.board.squareList[self.startingPositions[0][len(self.startingPositions[0])-1]].setState(0)
        self.board.squareList[51].setState(4)

        for x in self.startingPositions[3]:
            self.board.squareList[x].setState(1)
        self.board.squareList[120].setState(0)
        self.board.squareList[104].setState(1)

        self.sendGameState( [] )
                        
            
