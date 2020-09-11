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
from GameTutorials import *
from GameMenu import GameMenu
from direct.fsm import ClassicFSM, State
from direct.fsm import StateData
from toontown.distributed import DelayDelete

from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.toonbase import ToontownGlobals


from direct.showbase import PythonUtil
from otp.otpbase import OTPGlobals


class DistributedPicnicTable(DistributedNode.DistributedNode):
    def __init__(self, cr):
        self.cr = cr
        NodePath.__init__(self, "DistributedPicnicTable")
        DistributedNode.DistributedNode.__init__(self,cr)
        
        self.reparentTo(render)
        self.picnicTable = loader.loadModel("phase_6/models/golf/game_table.bam")
        self.picnicTable.reparentTo(self)


        self.picnicTableSphereNodes = []
        self.numSeats = 6
        self.seats = []
        self.jumpOffsets = []
        self.inGame = False
        self.requestSeat = None
        self.gameState = None
        #self.mypos = self.getPos()
        self.cameraBoardTrack = Func(self.doNothing)
        self.seatBumpForObserve = 0
        self.winTrack = Sequence()
        self.outTrack = Sequence()
        self.joinButton = None
        self.observeButton = None
        self.tutorialButton = None
        self.exitButton = None
        self.isPlaying = False
        self.gameMenu = None
        self.game = None
        self.gameZone = None
        self.tutorial = None
        


        self.timerFunc = None
        self.gameDoId = None
        #self.game = None
        self.gameWantTimer = False

        self.tableState = [None, None, None, None, None, None]
        self.haveAnimated = []
        self.winSound = base.loadSfx("phase_6/audio/sfx/KART_Applause_1.mp3")
        self.happyDance = base.loadSfx("phase_5/audio/sfx/AA_heal_happydance.mp3")

        #Seems like these functions BOTH are required
        #To intercept the sleep event.
        #Important to take action when GUI elements are up to turn
        #them off when the avatar goes to sleep otherwise the wakeup will allow
        #him to run around with the gui up.
        self.accept('stoppedAsleep', self.handleSleep)
        base.localAvatar.startSleepWatch(self.handleSleep)

        self.__toonTracks = {}

        self.fsm = ClassicFSM.ClassicFSM('PicnicTable',
                                         [State.State('off',
                                                      self.enterOff,
                                                      self.exitOff,
                                                      ['chooseMode','observing']),
                                          State.State('chooseMode',
                                                      self.enterChooseMode,
                                                      self.exitChooseMode,
                                                      ['sitting','off', 'observing']),
                                          State.State('sitting',
                                                      self.enterSitting,
                                                      self.exitSitting,
                                                      ['off']),
                                          State.State('observing',
                                                      self.enterObserving,
                                                      self.exitObserving,
                                                      ['off'])],
                                      #start state
                                      'off',
                                      #final state`
                                      'off',
                                      )
        self.fsm.enterInitialState()

        #Go find all of the locators for seats and jumpout locators
        for i in range(self.numSeats):
            self.seats.append(self.picnicTable.find("**/*seat%d" % (i+1)))
            self.jumpOffsets.append(self.picnicTable.find("**/*jumpOut%d" % (i+1)))
        self.tableCloth = self.picnicTable.find("**/basket_locator")


        #Stops you from walking on the table
        self.tableclothSphereNode = self.tableCloth.attachNewNode(CollisionNode('tablecloth_sphere'))
        self.tableclothSphereNode.node().addSolid(CollisionSphere(0, 0, -2, 5.5))

        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()
        
    def announceGenerate(self):
        
        DistributedNode.DistributedNode.announceGenerate(self)
          #Set up the collision spheres for the seats
        for i in range(self.numSeats):
            self.picnicTableSphereNodes.append(self.seats[i].attachNewNode(
                CollisionNode('picnicTable_sphere_%d_%d' % (self.getDoId(), i))))
            self.picnicTableSphereNodes[i].node().addSolid(
                CollisionSphere(0, 0, 0, 2))

        #sit everyone down
        self.tableState = [None, None, None, None, None, None]

        self.requestTableState()


        

        self.buttonModels = loader.loadModel("phase_3.5/models/gui/inventory_gui")
        self.upButton = self.buttonModels.find("**//InventoryButtonUp")
        self.downButton = self.buttonModels.find("**/InventoryButtonDown")
        self.rolloverButton = self.buttonModels.find("**/InventoryButtonRollover")


        #self.picnicTable.setScale(.030)
        #Preprocessing for Jump into seat Arcs (bad to do at runtime)
        angle = self.getH()
        angle -= 90
        radAngle = deg2Rad(angle)
        unitVec = Vec3( math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 30.0
        self.endPos =  self.getPos() + unitVec

        dist = Vec3(self.endPos - self.getPos()).length()
        wheelAngle = dist/(0.5 * 1.4 * math.pi ) * 360

        self.__enableCollisions()
    def handleSleep(self, task = None):
       #print "GETTING TO SLEEP!!!"
       if self.fsm.getCurrentState().getName() == "chooseMode":
           self.cancelButtonPushed()
       elif self.fsm.getCurrentState().getName() == "sitting":
           self.sendUpdate("requestExit", [])
       if self.gameMenu != None:
           self.gameMenu.removeButtons()
           self.gameMenu.picnicFunction = None
           self.gameMenu = None
       if task != None:
           task.done
       #task.done
       
    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        self.ignore('stoppedAsleep')
        self.clearToonTracks()
        self.__disableCollisions()
        self.disableChoiceButtons()
        #del self.picnicTableSphereNodes
        self.picnicTable.removeNode()
        self.cameraBoardTrack = None
        #self.fsm = None
        #self.winTrack.finish()
        #self.outTrack.finish()
        #self.outTrack = None
        
    def delete(self):
        self.__disableCollisions()
        self.ignore('stoppedAsleep')
        DistributedNode.DistributedNode.delete(self)
        self.disableChoiceButtons()
        self.cameraBoardTrack = None
        #self.winTrack.finish()
        #self.outTrack.finish()
        #self.winTrack = None
        #self.outTrack = None
        del self.winTrack
        del self.outTrack
        self.fsm = None
        self.gameZone = None
        self.clearToonTracks()
        self.cameraBoardTrack = None
        #self.clearToonTrack()
        #print " I AM DELETEING \n\n\n\n\n\n\n\n\n"
        #self.outTrack = None
        #del self

    def setName(self, name):
        self.name = name
    ################
    ##SetGameDoID -
    # This function is called by the child game after it is generated, in order
    #to set up the cross references that are needed to handle certain events
    #IE (getting up, erroneous disconnects ect.)
    def setGameDoId(self, doId):
        self.gameDoId = doId
        self.game = self.cr.doId2do[doId]
        self.game.setHpr(self.getHpr())
        self.gameWantTimer = self.game.wantTimer
        if self.gameState == 1:
            self.game.fsm.request('playing')
    ##########
    ##Timer Functions
    #setTimer (required broadcast ram)
    #
    #These are the timer functions that dictate movement and visual timer
    #feedback in the game table and chinese checkers.
    #
    ##########
    def setTimerFunc(self, function):
        self.timerFunc = function
    def setTimer(self, timerEnd):
        self.clockNode.stop()
        time = globalClockDelta.networkToLocalTime(timerEnd)
        self.timeLeft = int(time - globalClock.getRealTime() )
        if self.gameWantTimer and self.game != None:
            self.showTimer()
    def showTimer(self):
        #important to stop the timer before you reset it, otherwise it may still be running
        self.clockNode.stop()
        self.clockNode.countdown(self.timeLeft, self.timerFunc)
        self.clockNode.show()
    
    ##########
    #setTableState (required ram broadcast)
    #
    #This functions primary purpose is to handle asynchrinous joins of the zone
    #if an avatar teleports in, he needs to have a state of the table so he
    #can animate the toons to be sitting down in their corresponding seats
    ##########
    def requestTableState(self):
        self.sendUpdate("requestTableState", [])
    
    def setTableState(self, tableStateList, isplaying):
        y = 0
        print "SET TABLE STATE"
        if isplaying == 0:
            self.isPlaying = False
        else:
            self.isPlaying = True
        for x in tableStateList:
            if x != 0:
                # If we are to sit him down, make sure that he has not already been animated by fillslot
                # (deltas are handled by that function)
                if not x in self.tableState and self.cr.doId2do.has_key(x) and x not in self.haveAnimated:
                    seatIndex = tableStateList.index(x)
                    toon = self.cr.doId2do[x]
                    toon.stopSmooth()
                    toon.setAnimState( "Sit", 1.0)

                    
                    dest = self.seats[seatIndex].getPos(self.tableCloth)
                    hpr = self.seats[seatIndex].getHpr(render)
                    toon.setHpr(hpr)

                    if(seatIndex  > 2):
                        toon.setH(self.getH()+180)
                    toon.wrtReparentTo(self)
                    toon.setPos(dest)
                    toon.setZ(toon.getZ()+1.35)

                    if(seatIndex  > 2):
                        toon.setY(toon.getY()-1.0)
                    else:
                        toon.setY(toon.getY()+1.0)
                        
                    
            if x != 0:
                self.tableState[y] = x
            else:
                self.tableState[y] = None
            
            y = y + 1

        ###Handle the game menu stuffs
        numPlayers = 0
        for x in self.tableState:
            if x != None:
                numPlayers += 1
        #check for a game menu up
        print " GETTING 2", self.gameMenu, numPlayers
        if self.gameMenu:
            if numPlayers > 2:
                print " GETTING HERE!!"
                self.gameMenu.FindFour.setColor(.7,.7,.7,.7)
                self.gameMenu.FindFour['command'] = self.doNothing
                self.gameMenu.findFourText['fg'] = (.7,.7,.7,.7)

                self.gameMenu.Checkers.setColor(.7,.7,.7,.7)
                self.gameMenu.Checkers['command'] = self.doNothing
                self.gameMenu.checkersText['fg'] = (.7,.7,.7,.7)
            
    def setIsPlaying(self, isPlaying):
        if isPlaying == 0:
            self.isPlaying = False
        elif isPlaying == 1:
            self.isPlaying = True
    ##########
    ##announceWinner (broadcast)
    #
    #Obvious, simply just sets the whisper message
    ##########
    def announceWinner(self, winString, avId):
        if avId == base.localAvatar.getDoId():
            sound = Sequence(Wait(2.0), Parallel( SoundInterval(self.winSound), SoundInterval(  self.happyDance)))
            sound.start()
            base.cr.playGame.getPlace().setState('walk') #To stop Cohesion between EmptySlot and AnnounceWin
            if winString == "Chinese Checkers":
                whisper = WhisperPopup(TTLocalizer.ChineseCheckersYouWon,
                                       OTPGlobals.getInterfaceFont(),
                                       WhisperPopup.WTNormal)
            elif winString == "Checkers":
                whisper = WhisperPopup(TTLocalizer.RegularCheckersYouWon,
                                       OTPGlobals.getInterfaceFont(),
                                       WhisperPopup.WTNormal)
            elif winString == "Find Four":
                whisper = WhisperPopup("You won a game of Find Four!",
                                       OTPGlobals.getInterfaceFont(),
                                       WhisperPopup.WTNormal)
                
        else:
            if self.cr.doId2do.has_key(avId):
                stateString = self.fsm.getCurrentState().getName()
                if stateString == "sitting" or stateString == "observing" :
                    base.cr.playGame.getPlace().setState('walk') #To stop Cohesion between EmptySlot and AnnounceWin
                av = self.cr.doId2do[avId]
                if winString == "Chinese Checkers":
                    whisper = WhisperPopup(av.getName()  + TTLocalizer.ChineseCheckersGameOf + TTLocalizer.ChineseCheckers,
                                             OTPGlobals.getInterfaceFont(),
                                             WhisperPopup.WTNormal)
                elif winString == "Checkers":
                    whisper = WhisperPopup(av.getName()  + TTLocalizer.RegularCheckersGameOf + TTLocalizer.RegularCheckers,
                                             OTPGlobals.getInterfaceFont(),
                                             WhisperPopup.WTNormal)
                elif winString == "Find Four":
                    whisper = WhisperPopup(av.getName()  + " has won a game of" + " Find Four!" ,
                                           OTPGlobals.getInterfaceFont(),
                                           WhisperPopup.WTNormal)

        if self.cr.doId2do.has_key(avId):
            # If the toon exists, look it up
            toon = self.cr.doId2do[avId]
            #self.winTrack.finish() 
            self.winTrack = Sequence(autoFinish = 1)
            if self.outTrack.isPlaying(): #If toon is jumping out Wait a
                self.winTrack.append(Wait(2.0)) # duration till his anim is over to begin
                
            if avId == base.localAvatar.getDoId():
                #stop him from walking locally
                #otherwise he will animate around while moving on other clients
                self.winTrack.append(Func(self.stopToWalk))
            self.winTrack.append(ActorInterval(toon, 'happy-dance'))
            if avId == base.localAvatar.getDoId():
               self.winTrack.append(Func(self.allowToWalk))
            self.winTrack.start()
        #Display the whisper message
        whisper.manage(base.marginManager)
        
                
                
    ##########
    #handleEnterPicnicTableSphere
    #
    #This is the function that via the messenger, handles the collision
    #with one of the six collision spheres on a picnic table
    ##########
    def handleEnterPicnicTableSphere(self, i, collEntry):
        assert self.notify.debugStateCall(self)
        #print "COLLISION!!!"
        self.notify.debug("Entering Picnic Table Sphere.... %s" % self.getDoId())


        #if self.requestSeat == None:
        self.requestSeat = i
        self.seatBumpForObserve = i
        self.fsm.request('chooseMode')
    ##########
    #Button Logic (handled by handleEnterPicnicTableSphere, and self.fsm
    ###

    def enableChoiceButtons(self):
        if self.tableState[self.seatBumpForObserve] == None and self.isPlaying == False:   
            self.joinButton = DirectButton(
            relief = None,
            text = TTLocalizer.PicnicTableJoinButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.8,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (0, 0, .8),
            scale = 0.15,
            command = lambda self=self: self.joinButtonPushed(),
            )
        if self.isPlaying == True:
            self.observeButton = DirectButton(
             relief = None,
            text = TTLocalizer.PicnicTableObserveButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.8,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (0, 0, 0.6),
            scale = 0.15,
            command = lambda self=self: self.observeButtonPushed(),
            )
        self.exitButton = DirectButton(
            relief = None,
            text = TTLocalizer.PicnicTableCancelButton,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.8,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (1, 0, 0.6),
            scale = 0.15,
            command = lambda self=self: self.cancelButtonPushed(),
            )
        self.tutorialButton = DirectButton(
            relief = None,
            text = TTLocalizer.PicnicTableTutorial,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (-.05, -.13),
            text_scale = 0.55,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (-1, 0, 0.6),
            scale = 0.15,
            command = lambda self=self: self.tutorialButtonPushed(),
            )
        base.cr.playGame.getPlace().setState('stopped')
    def tutorialButtonPushed(self):
        #print "GETTING HERE!!!"
        self.disableChoiceButtons()
        #self.tutorial = ChineseTutorial(self.tutorialDone)
        self.gameMenu = GameMenu(self.tutorialFunction, 1) # 1 == Tutorial Num
        #self.tutorialFunction(1)
        self.tutorialButton.destroy()
        self.tutorialButton = None
    def tutorialFunction(self, tutVal):
        if tutVal == 1:
            self.tutorial = ChineseTutorial(self.tutorialDone)
        elif tutVal == 2:
            self.tutorial = CheckersTutorial(self.tutorialDone)
        self.gameMenu.picnicFunction = None
        self.gameMenu = None
    def tutorialDone(self):
        #del self.tutorial
        self.requestSeat = None
        self.fsm.request('off')
        self.tutorial = None
        #del self.tutorial
    def joinButtonPushed(self):
        toon = base.localAvatar
        self.sendUpdate("requestJoin",
                        [self.requestSeat, toon.getX(), toon.getY(), toon.getZ(),
                         toon.getH(), toon.getP(), toon.getR()])
        self.requestSeat = None
        self.fsm.request('sitting')
        
    def rejectJoin(self):
        self.fsm.request('off')
        self.allowToWalk()
        
    def cancelButtonPushed(self):
        base.cr.playGame.getPlace().setState('walk')
        self.requestSeat = None
        self.fsm.request('off')
    def disableChoiceButtons(self):
        if self.joinButton:
            self.joinButton.destroy()
        if self.observeButton:
            self.observeButton.destroy()
        if self.exitButton:
            self.exitButton.destroy()
        if self.tutorialButton:
            self.tutorialButton.destroy()

    ##########
    #Distributed fillSlot Functions (broadcasT)
    #
    #These functions are the distributed functions that the ai sends to tell
    #the client if its ok for people to picnic table, and then animates them
    ##########
    def pickFunction(self, gameNum):
        #print "SENDING PICK!"
        if gameNum == 1: #Chinese Checkers
            self.sendUpdate('requestPickedGame', [gameNum])
        elif gameNum == 2:
            self.sendUpdate('requestPickedGame', [gameNum])
        elif gameNum == 3:
            self.sendUpdate('requestPickedGame' , [gameNum])
    def allowPick(self):
        self.gameMenu = GameMenu(self.pickFunction, 2) # 2 == pick Num for TTlocalizer
        #elf.pickFunction(1)

    def setZone(self, zoneId):
        #import pdb; pdb.set_trace()
        #print "ZONE iD == " , zoneId
        #print "CURRENT SATE?!?!? == ", self.fsm.getCurrentState().getName()
        #if self.fsm.getCurrentState().getName() == "chooseMode" or self.fsm.getCurrentState().getName() == "sitting":
        if self.fsm.getCurrentState().getName() == "sitting" or self.fsm.getCurrentState().getName() == "observing" :
            if self.tutorial == None:
                self.gameZone = base.cr.addInterest(base.localAvatar.defaultShard, zoneId, 'gameBoard')
                if self.gameMenu != None:
                    self.gameMenu.removeButtons()
                    self.gameMenu.picnicFunction = None
                    self.gameMenu = None
    def fillSlot(self, avId,index,  x, y, z, h, p, r, timestamp, parentDoId):
        assert self.notify.debugStateCall(self)
        self.notify.debug( "fill Slot: %d for %d" % (index, avId) )
        if not avId in self.haveAnimated:
            self.haveAnimated.append(avId)

        if avId == base.localAvatar.getDoId():
            if self.inGame == True:
                return #in a game therefore we dont animate
            else:
                self.inGame = True
                self.seatPos = index
                pass #not in a game but need to animate into the game

        if self.cr.doId2do.has_key(avId):
            toon = self.cr.doId2do[avId]

            toon.stopSmooth()
            toon.wrtReparentTo(self.tableCloth)
            sitStartDuration = toon.getDuration("sit-start")
            jumpTrack = self.generateToonJumpTrack(toon, index)
            
            track = Sequence(autoFinish = 1)
            if avId == base.localAvatar.getDoId():
                if not base.cr.playGame.getPlace() == None:
                    self.moveCamera(index)
                    track.append(Func(self.__disableCollisions))
                    #self.gameZone = base.cr.addInterest(base.localAvatar.defaultShard, boardZoneId, 'chineseBoard')
            track.append(jumpTrack)
            track.append(Func(toon.setAnimState, "Sit", 1.0))
            track.append(Func(self.clearToonTrack, avId))
            self.storeToonTrack(avId, track)
            track.start()

    ##########
    #Empty Slot Distributed Functions (broadcast)
    #
    #Distributed functions that manage the toons getting off of the picnic
    #tables
    ##########
    def emptySlot(self, avId, index, timestamp):
        self.notify.debug( "### seat %s now empty" % index)
        
        ##Player told to exit is an OBSERVER
        if index == 255 and self.game != None:
            self.stopObserveButtonPushed()
            return


               
           #self.fullSeat[index] = self.seatState.Empty
        if avId in self.haveAnimated:
               self.haveAnimated.remove(avId)
           # self.fullSeat[index] = self.seatState.Empty
        if self.cr.doId2do.has_key(avId):
            if avId == base.localAvatar.getDoId():
                if self.gameZone:
                    base.cr.removeInterest(self.gameZone)
                if self.inGame == True: #are in a game
                    self.inGame = False
                else:
                    return #dont animate because we are NOT in a game
            toon = self.cr.doId2do[avId]
            toon.stopSmooth()
            sitStartDuration = toon.getDuration("sit-start")
            jumpOutTrack = self.generateToonReverseJumpTrack(toon, index)
            #self.outTrack.finish()
            self.outTrack = Sequence(jumpOutTrack)

            if base.localAvatar.getDoId() == avId:
                self.outTrack.append(Func(self.__enableCollisions))
                self.outTrack.append(Func(self.allowToWalk)) #temp until i can stop the
                                                             #camera from jerking
                #self.outTrack.append(Func(self.fsm.request, 'off'))
                self.fsm.request('off')
                #self.outTrack.append(Func(self.tempCheckers.setHpr, 0, self.tempCheckers.getP(), self.tempCheckers.getR()))

            val = self.jumpOffsets[index].getPos(render)
            #self.storeToonTrack(avId, self.outTrack)

            self.outTrack.append(Func(toon.setPos, val))
            self.outTrack.append(Func(toon.startSmooth))
            self.outTrack.start()
            #self.outTrack = Sequence()
    def stopToWalk(self):
        base.cr.playGame.getPlace().setState("stopped")
    def allowToWalk(self):
       #if not self.winTrack.isPlaying():
       base.cr.playGame.getPlace().setState("walk")
       #self.winTrack.finish()
           #self.winTrack = None

    ##########
    #Camera manipulations
    ##########
    def moveCamera(self,seatIndex):
        self.oldCameraPos = camera.getPos()
        self.oldCameraHpr = camera.getHpr()
        camera.wrtReparentTo(self.picnicTable)
        heading = PythonUtil.fitDestAngle2Src( camera.getH(), 90)
        #Need to check the seat index so the cameras *down
        #is towards the player so he is not facing his own character
        #rather he feels he is a bit above him
        if seatIndex < 3:
            self.cameraBoardTrack = LerpPosHprInterval(camera, 2.0,
                                                   Point3(0,0, 17),
                                                   Point3(0,-90,0))
        else:
            #needed for camera orientation
            #If test is not here, the camera may often flip around
            #spinning ~340 degrees to the destination
            #instead of turning the 20 degrees towards the table
            if(camera.getH() < 0):#(turned left)
                self.cameraBoardTrack = LerpPosHprInterval(camera, 2.0,
                                                   Point3(0,0, 17),
                                                   Point3(-180,-90,0))
                                                  
            else:#(turned right)
                self.cameraBoardTrack = LerpPosHprInterval(camera, 2.0,
                                                   Point3(0,0, 17),
                                                   Point3(180,-90,0))
    
        self.cameraBoardTrack.start()
    def moveCameraBack(self):
        self.cameraBoardTrack = LerpPosHprInterval(camera, 2.5,
                                                   self.oldCameraPos,
                                                   self.oldCameraHpr)
        self.cameraBoardTrack.start()
    ##########
    # Enable and Disable Collisions
    #
    #Turn on and off the collisions for the seat and table collision spheres for
    #boarding and unboarding, thus to actaully allow the toons to sit down, animate ect.
    ##########
    def __enableCollisions(self):
        # start listening for toons to enter.
        assert self.notify.debugStateCall(self)
        for i in range(self.numSeats): 
            self.accept('enterpicnicTable_sphere_%d_%d' % (self.getDoId(), i), self.handleEnterPicnicTableSphere, [i])
            #self.accept('enterPicnicTableOK_%d_%d' % (self.getDoId(), i), self.handleEnterPicnicTable, [i])        
            self.picnicTableSphereNodes[i].setCollideMask(ToontownGlobals.WallBitmask)
        self.tableclothSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def __disableCollisions(self):
        assert self.notify.debugStateCall(self)
        #self.ignore('tableClothSphereNode')
        for i in range(self.numSeats): 
            self.ignore('enterpicnicTable_sphere_%d_%d' % (self.getDoId(), i))
            self.ignore('enterPicnicTableOK_%d_%d' % (self.getDoId(), i))
        for i in range(self.numSeats):
            self.picnicTableSphereNodes[i].setCollideMask(BitMask32(0))     
        self.tableclothSphereNode.setCollideMask(BitMask32(0))

    ##########
    #FSM stuff
    ##########
    
    def enterOff(self):
        base.setCellsAvailable(base.leftCells + 
                               base.bottomCells, 0)
    def exitOff(self):
        base.setCellsAvailable(base.bottomCells,0)
    def enterChooseMode(self):
        #self.requestTableState()
        self.winTrack = Sequence(autoFinish = 1)
        self.enableChoiceButtons()
    def exitChooseMode(self):
        self.disableChoiceButtons()
    def enterObserving(self):
        self.enableStopObserveButton()
        self.moveCamera(self.seatBumpForObserve)
        #track.append(Func(self.__disableCollisions))
        self.sendUpdate('requestGameZone')
        #self.gameZone = base.cr.addInterest(base.localAvatar.defaultShard, boardZoneId, 'chineseBoard')
    def exitObserving(self):
         #self.__enableCollisions
         if self.cameraBoardTrack.isPlaying():
            self.cameraBoardTrack.pause()
         self.allowToWalk() #temp until i can stop the
                                                             #camera from jerking
         self.stopObserveButton.destroy()
    def enterSitting(self):
        pass
        #self.tempCheckers.hide()
    def exitSitting(self):
        self.gameMenu = None
        #self.winTrack = None
        #self.tempCheckers.show()
        #self.suxButton.destroy()
        #self.sendUpdate('requestExit', [])
    ##########
    #Observer  Functions setGameZone (broadcast)
    #
    #Need these because you are not "filling" a slot by observing
    #
    #For this case - When it sends a 1 or a zero with the setGameZone, This is to account for the fact
    #an observer can (and will) come into games halfway through, somehow that client needs to know
    #about the current state of the game.
    #
    #
    #1 == Playing
    #0 == Not Playing
    ##########
    def setGameZone(self, zoneId, gamestate):
        self.gameZone = base.cr.addInterest(base.localAvatar.defaultShard, zoneId, 'gameBoard')
        self.gameState = gamestate
    def observeButtonPushed(self):
        #base.cr.playGame.getPlace().setState('walk')
        self.requestSeat = None
        self.fsm.request('observing')
    def enableStopObserveButton(self):
        self.stopObserveButton = DirectButton(
            relief = None,
            text = "Stop Observing",
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -.23),
            text_scale = 0.45,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (.92, 0, 0.4),
            scale = 0.15,
            command = lambda self=self: self.stopObserveButtonPushed(),
            )
    def stopObserveButtonPushed(self):
        self.sendUpdate("leaveObserve", [])
        self.gameState = None
        if self.game:
            self.game.fsm.request('gameOver')
            base.cr.removeInterest(self.gameZone)
        self.fsm.request('off')
    
    ##########
    #Generators for jumps
    #
    #And the storage/deletion functions for
    #handling them.
    ##########
        
    def generateToonReverseJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping out of the golf kart."""        
        self.notify.debug("av.getH() = %s" % av.getH())
        def getToonJumpTrack( av, destNode ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = destNode):
                dest = node.getPos(self.tableCloth)
                dest += self.jumpOffsets[seatIndex].getPos(self.tableCloth)
                return dest

            def getJumpHpr(av = av, node = destNode):
                hpr = node.getHpr(av.getParent())
                hpr.setX( hpr.getX() + 180)
                angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                hpr.setX(angle)
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                  Wait( 0.1), #43 ),
                  Parallel( #LerpHprInterval( av,
                            #                 hpr = getJumpHpr,
                            #                 duration = .9 ),
                            ProjectileInterval( av,
                                                endPos = getJumpDest,
                                                duration = .9 ) )
                  )
                )  
            return toonJumpTrack

        toonJumpTrack = getToonJumpTrack( av, self.tableCloth)
                                          #self.seats[seatIndex])
        jumpTrack = Sequence(
            toonJumpTrack,
            Func( av.loop, 'neutral' ),
            Func( av.wrtReparentTo, render ),
            #Func( self.av.setPosHpr, self.exitMovieNode, 0,0,0,0,0,0 ),
            )
        return jumpTrack

    def generateToonJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping into the golf kart."""
        # Maintain a reference to Parent and Scale of avatar in case they
        # exit from the kart.
        #base.sb = self

        av.pose('sit', 47)
        hipOffset = av.getHipsParts()[2].getPos(av)
        
        def getToonJumpTrack( av, seatIndex ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = self.tableCloth):
                dest = Vec3(self.tableCloth.getPos(av.getParent()))
                seatNode = self.picnicTable.find("**/seat" + str(seatIndex + 1))
                dest += seatNode.getPos(self.tableCloth)
                dna = av.getStyle()
                dest -= hipOffset
                if(seatIndex  > 2):
                    dest.setY(dest.getY() - 2.0)
                if(seatIndex == 1):
                    dest.setY(dest.getY()-.5)
                #dest.setY( dest.getY() + 2 * hipOffset.getY())
                #dest.setY(dest.getY())
                dest.setZ(dest.getZ() + 0.2)

                return dest

            def getJumpHpr(av = av, node = self.tableCloth):
                hpr = self.seats[seatIndex].getHpr(av.getParent())
                if(seatIndex < 3):
                    hpr.setX( hpr.getX())
                else:
                    if(av.getH() < 0):
                        hpr.setX( hpr.getX()-180)
                    else:
                        hpr.setX(hpr.getX()+180)
               
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                   Wait( 0.43 ),
                   Parallel( LerpHprInterval( av,
                                              hpr = getJumpHpr,
                                              duration = 1 ),
                             ProjectileInterval( av,
                                                 endPos = getJumpDest,
                                                 duration = 1 )
                             ),
                   )
                )
            return toonJumpTrack


        def getToonSitTrack( av ):
            toonSitTrack = Sequence(

                    ActorInterval( av, 'sit-start' ),
                    Func( av.loop, 'sit' )
                    )
            return toonSitTrack

        toonJumpTrack = getToonJumpTrack( av, seatIndex )
        toonSitTrack = getToonSitTrack( av )

        jumpTrack = Sequence(
            Parallel(toonJumpTrack,
                    Sequence( Wait(1),
                              toonSitTrack,
                              ),
                    ),
            Func( av.wrtReparentTo, self.tableCloth ),            
                )

        return jumpTrack
    def storeToonTrack(self, avId, track):
        # Clear out any currently playing tracks on this toon
        self.clearToonTrack(avId)
        # Store this new one
        self.__toonTracks[avId] = track

    def clearToonTrack(self, avId):
        # Clear out any currently playing tracks on this toon
        oldTrack = self.__toonTracks.get(avId)
        if oldTrack:
            oldTrack.pause()
            cleanupDelayDeletes(oldTrack)
            #del self.__toonTracks[avId]

    def clearToonTracks(self):
        #We can't use an iter because we are deleting keys
        keyList = []
        for key in self.__toonTracks:
            keyList.append(key)
            
        for key in keyList:
            if self.__toonTracks.has_key(key):
                self.clearToonTrack(key)

    def doNothing(self):
        pass


    
    

