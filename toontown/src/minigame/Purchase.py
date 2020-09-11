from PurchaseBase import *
from direct.task.Task import Task
from toontown.toon import ToonHead
from toontown.toonbase import ToontownTimer
from direct.gui import DirectGuiGlobals as DGG
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import Functor
from toontown.minigame import TravelGameGlobals
from toontown.distributed import DelayDelete

COUNT_UP_RATE = 0.15
DELAY_BEFORE_COUNT_UP = 1.25
DELAY_AFTER_COUNT_UP = 1.75
COUNT_DOWN_RATE = 0.075
DELAY_AFTER_COUNT_DOWN = 0.0
DELAY_AFTER_CELEBRATE = 3.0

class Purchase(PurchaseBase):

    notify = DirectNotifyGlobal.directNotify.newCategory("Purchase")

    def __init__(self, toon, pointsArray, playerMoney, ids, states, remain, doneEvent,
                 metagameRound = -1, votesArray = None):
        """__init__(self, Toon, int, string):
        Create and display a reward screen and then a purchase screen for
        the given Toon with the given amount of points to spend on items.
        Throw the given event name when user is finished
        """
        assert self.notify.debugStateCall(self)
        PurchaseBase.__init__(self, toon, doneEvent)
        self.ids = ids
        self.pointsArray = pointsArray
        self.playerMoney = playerMoney
        self.states = states
        self.remain = remain
        self.tutorialMode = 0
        self.metagameRound = metagameRound
        self.votesArray = votesArray
        self.voteMultiplier = 1
        assert self.notify.debug('self.votesArray = %s' % self.votesArray)

        self.fsm.addState(State.State('reward',
                                        self.enterReward,
                                        self.exitReward,
                                        ['purchase']))
        doneState = self.fsm.getStateNamed('done')
        doneState.addTransition('reward')

        self.unexpectedEventNames = []
        self.unexpectedExits = [] # list of avIds who have disconnected
        self.setupUnexpectedExitHooks()
    
    def load(self):
        purchaseModels = loader.loadModel("phase_4/models/gui/purchase_gui")

        PurchaseBase.load(self, purchaseModels)

        # This may change back to 4 when we get a real tutorial interior
        interiorPhase = 3.5
        
        self.bg = loader.loadModel("phase_%s/models/modules/toon_interior" % interiorPhase)
        self.bg.setPos(0., 5., -1.)

        self.wt = self.bg.find("**/random_tc1_TI_wallpaper")
        wallTex = loader.loadTexture("phase_%s/maps/wall_paper_a5.jpg" % interiorPhase)
        self.wt.setTexture(wallTex, 100)
        self.wt.setColorScale(0.800, 0.670, 0.549, 1.0)

        self.bt = self.bg.find("**/random_tc1_TI_wallpaper_border")
        wallTex = loader.loadTexture("phase_%s/maps/wall_paper_a5.jpg" % interiorPhase)
        self.bt.setTexture(wallTex, 100)
        self.bt.setColorScale(0.800, 0.670, 0.549, 1.0)

        self.wb = self.bg.find("**/random_tc1_TI_wainscotting")
        wainTex = loader.loadTexture("phase_%s/maps/wall_paper_b4.jpg" % interiorPhase)
        self.wb.setTexture(wainTex, 100)
        self.wb.setColorScale(0.473, 0.675, 0.488, 1.0)

        # make a play again button
        self.playAgain = DirectButton(
            parent = self.frame,
            relief = None,
            scale = 1.04,
            pos = (0.72, 0, -0.24),
            image = (purchaseModels.find("**/PurchScrn_BTN_UP"),
                     purchaseModels.find("**/PurchScrn_BTN_DN"),
                     purchaseModels.find("**/PurchScrn_BTN_RLVR"),
                     purchaseModels.find("**/PurchScrn_BTN_UP"),
                     ),
            text = TTLocalizer.GagShopPlayAgain,
            text_fg = (0, 0.1, 0.7, 1),
            text_scale = 0.05,
            text_pos = (0,0.015,0),
            # darken disabled button
            image3_color = Vec4(.6,.6,.6,1),
            text3_fg = Vec4(0, 0, .4, 1),
            command = self.__handlePlayAgain,
            )

        # make a Back to Playground button
        self.backToPlayground = DirectButton(
            parent = self.frame,
            relief = None,
            scale = 1.04,
            #pos = (0.66, 0, -0.045),
            pos = (0.72, 0, -0.045),
            image = (purchaseModels.find("**/PurchScrn_BTN_UP"),
                     purchaseModels.find("**/PurchScrn_BTN_DN"),
                     purchaseModels.find("**/PurchScrn_BTN_RLVR"),
                     purchaseModels.find("**/PurchScrn_BTN_UP"),
                     ),
            text = TTLocalizer.GagShopBackToPlayground,
            text_fg = (0, 0.1, 0.7, 1),
            text_scale = 0.05,
            text_pos = (0, 0.015, 0),
            # darken disabled button
            image3_color = Vec4(.6,.6,.6,1),
            text3_fg = Vec4(0, 0, .4, 1),
            command = self.__handleBackToPlayground,
            )

        # The timer
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self.frame)
        self.timer.posInTopRightCorner()

        # make the character panels
        numAvs = 0
        count = 0
        localToonIndex = 0
        for index in range(len(self.ids)):
            avId = self.ids[index]
            if avId == base.localAvatar.doId:
                localToonIndex = index
            if ((self.states[index] != PURCHASE_NO_CLIENT_STATE) and
                (self.states[index] != PURCHASE_DISCONNECTED_STATE)):
                numAvs = numAvs + 1
        
        # Determine which panels should be filled
        layoutList = (None, (0,), (0,2), (0,1,3), (0,1,2,3))
        layout = layoutList[numAvs]
        # And where they will be positioned
        headFramePosList = (Vec3(0.105, 0, -0.384),
                            Vec3(0.105, 0, -0.776),
                            Vec3(0.85, 0, -0.555),
                            Vec3(-0.654, 0, -0.555))
        
        # An array of avatars, layout positions, and indices into the
        # states array. Localtoon is listed first.
        AVID_INDEX = 0
        LAYOUT_INDEX = 1
        TOON_INDEX = 2
        self.avInfoArray = [ (base.localAvatar.doId, headFramePosList[0], localToonIndex) ]

        pos = 1
        for index in range(len(self.ids)):
            avId = self.ids[index]
            if ((self.states[index] != PURCHASE_NO_CLIENT_STATE) and
                (self.states[index] != PURCHASE_DISCONNECTED_STATE)):
                if avId != base.localAvatar.doId:
                    # Do not add the doId if they are not in the doId
                    if base.cr.doId2do.has_key(avId):
                        self.avInfoArray.append( (avId, headFramePosList[layout[pos]], index) )
                        pos = pos + 1

        self.headFrames = []
        for avInfo in self.avInfoArray:
            av = base.cr.doId2do.get(avInfo[AVID_INDEX])
            if av:
                headFrame = PurchaseHeadFrame(av, purchaseModels)
                headFrame.setAvatarState(self.states[avInfo[TOON_INDEX]])
                headFrame.setPos(avInfo[LAYOUT_INDEX])
                self.headFrames.append((avInfo[AVID_INDEX], headFrame))

        # clean up the root node
        purchaseModels.removeNode()

        #
        # reward screen stuff
        #

        # background buildings
        self.foreground = loader.loadModel("phase_3.5/models/modules/TT_A1")
        self.foreground.setPos(12.5, -20, -5.5)
        self.foreground.setHpr(180, 0, 0)
        self.backgroundL = loader.loadModel("phase_3.5/models/modules/TT_A1")
        self.backgroundL.setPos(-12.5, -25, -5)
        self.backgroundL.setHpr(180, 0, 0)
        self.backgroundR = self.backgroundL.copyTo(hidden)
        self.backgroundR.setPos(20, -25, -5)

        streets = loader.loadModel("phase_3.5/models/modules/street_modules")
        sidewalk = streets.find("**/street_sidewalk_40x40")
        self.sidewalk = sidewalk.copyTo(hidden)
        self.sidewalk.setPos(-20, -25, -5.5)
        self.sidewalk.setColor(0.9, 0.6, 0.4)
        streets.removeNode()

        doors = loader.loadModel("phase_4/models/modules/doors")
        door = doors.find("**/door_single_square_ur_door")
        self.door = door.copyTo(hidden)
        self.door.setH(180)
        self.door.setPos(0, -16.75, -5.5)
        self.door.setScale(1.5, 1.5, 2.0)
        self.door.setColor(1.0, 0.8, 0, 1)
        doors.removeNode()

        self.convertingVotesToBeansLabel = DirectLabel(
            text = TTLocalizer.TravelGameConvertingVotesToBeans,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (0.0, 0, -0.65),
            scale = 0.075)
        self.convertingVotesToBeansLabel.hide()

        self.countSound = base.loadSfx("phase_3.5/audio/sfx/tick_counter.mp3")
        self.overMaxSound = base.loadSfx("phase_3.5/audio/sfx/AV_collision.mp3")
        self.celebrateSound = base.loadSfx("phase_4/audio/sfx/MG_win.mp3")


    def unload(self):
        PurchaseBase.unload(self)
        self.cleanupUnexpectedExitHooks()
        self.bg.removeNode()
        del self.bg
        self.notify.debug('destroying head frames')
        for headFrame in self.headFrames:
            if not headFrame[1].isEmpty():
                headFrame[1].reparentTo(hidden)
                headFrame[1].destroy()
        del self.headFrames
        self.playAgain.destroy()
        del self.playAgain
        self.backToPlayground.destroy()
        del self.backToPlayground
        # timer will get destroyed because it is in frame
        self.timer.stop()
        del self.timer
        for counter in self.counters:
            counter.destroy()
            del counter
        del self.counters
        for total in self.totalCounters:
            total.destroy()
            del total
        del self.totalCounters
        loader.unloadModel("phase_3.5/models/modules/TT_A1")
        loader.unloadModel("phase_3.5/models/modules/street_modules")
        loader.unloadModel("phase_4/models/modules/doors")
        self.foreground.removeNode()
        del self.foreground
        self.backgroundL.removeNode()
        del self.backgroundL
        self.backgroundR.removeNode()
        del self.backgroundR
        self.sidewalk.removeNode()
        del self.sidewalk
        self.door.removeNode()
        del self.door
        self.collisionFloor.removeNode()
        del self.collisionFloor
        del self.countSound
        del self.celebrateSound
        self.convertingVotesToBeansLabel.removeNode()
        del self.convertingVotesToBeansLabel
        return

    def showStatusText(self, text):
        self.statusLabel['text'] = text
        taskMgr.remove("resetStatusText")
        taskMgr.doMethodLater(2.0, self.resetStatusText, "resetStatusText")
        return

    def resetStatusText(self, task):
        self.statusLabel['text'] = ""
        return Task.done

    def __handlePlayAgain(self):
        for headFrame in self.headFrames:
            headFrame[1].wrtReparentTo(aspect2d)
        self.toon.inventory.reparentTo(hidden)
        self.toon.inventory.hide()
        taskMgr.remove("resetStatusText")
        taskMgr.remove("showBrokeMsgTask")        
        self.statusLabel['text'] = TTLocalizer.GagShopWaitingOtherPlayers
        #self.statusLabel.setPos(0,0,0.1)
        messenger.send("purchasePlayAgain")
        return

    def handleDone(self, playAgain):
        base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        if playAgain:
            self.doneStatus = {
                    "loader": "minigame",
                    "where": "minigame"}
        else:
            self.doneStatus = {
                    "loader": "safeZoneLoader",
                    "where": "playground"}
        messenger.send(self.doneEvent)

    def __handleBackToPlayground(self):
        self.toon.inventory.reparentTo(hidden)
        self.toon.inventory.hide()
        messenger.send("purchaseBackToToontown")
        return

    def __timerExpired(self):
        # do something
        messenger.send("purchaseTimeout")
        return

    def findHeadFrame(self, id):
        for headFrame in self.headFrames:
            if headFrame[0] == id:
                return headFrame[1]
        return None

    def __handleStateChange(self, playerStates):
        self.states = playerStates
        for avInfo in self.avInfoArray:
            index = avInfo[2]
            headFrame = self.findHeadFrame(avInfo[0])
            state = self.states[index]
            headFrame.setAvatarState(state)

    # wrapper functions

    # Override PurchaseBase.enter() to go to reward state

    def enter(self):
        assert self.notify.debugStateCall(self)           
        base.playMusic(self.music, looping = 1, volume = 0.8)
        self.fsm.request("reward")        

    ### Reward state functions ###

    def enterReward(self):
        assert self.notify.debugStateCall(self)           
        numToons = 0
        toonLayouts = ( (2,), (1,3), (0,2,4), (0,1,3,4), )
        toonPositions = ( 5.0, 1.75, -0.25, -1.75, -5.0 )
        self.toons = []
        self.toonsKeep = []
        self.counters = []
        self.totalCounters = []

        # put the camera in a reasonable position
        camera.reparentTo(render)
        base.camLens.setFov(ToontownGlobals.DefaultCameraFov)
        camera.setPos(0, 16.0, 2.0)
        camera.lookAt(0, 0, 0.75)
        base.transitions.irisIn(0.4)
        
        # show background elements
        self.title.reparentTo(aspect2d)
        self.foreground.reparentTo(render)
        self.backgroundL.reparentTo(render)
        self.backgroundR.reparentTo(render)
        self.sidewalk.reparentTo(render)        
        self.door.reparentTo(render)

        # The backdrop in this scene is not really under our feet - it is a
        # bit of an optical illusion. So to make the physics behave a bit
        # better, we'll actually put a floor directly under the toons so
        # they stay put and their shadows stay put
        size = 20
        z = -2.5
        floor = CollisionPolygon(
            Point3(-size,-size,z),
            Point3(size,-size,z),
            Point3(size,size,z),
            Point3(-size,size,z))
        floor.setTangible(1)
        floorNode = CollisionNode("collision_floor")
        floorNode.addSolid(floor)
        self.collisionFloor = render.attachNewNode(floorNode)

        # the bean counters take up a lot of real estate: clamp the whisper bubbles
        NametagGlobals.setOnscreenChatForced(1)
        
        # find out how many toons there are, make point counters for
        # them and get their models
        for index in range(len(self.ids)):
            avId = self.ids[index]
            if ((self.states[index] != PURCHASE_NO_CLIENT_STATE) and
                (self.states[index] != PURCHASE_DISCONNECTED_STATE) and
                (avId in base.cr.doId2do)):
                numToons += 1
                toon = base.cr.doId2do[avId]
                toon.stopSmooth()
                self.toons.append(toon)
                self.toonsKeep.append(DelayDelete.DelayDelete(toon, 'Purchase.enterReward'))
                # counter for beans won
                counter = DirectLabel(
                    parent = hidden,
                    relief = None,
                    pos = (0.0, 0.0, 0.0),
                    text = str(0),
                    text_scale = 0.2,
                    text_fg = (0.95, 0.95, 0, 1),
                    text_pos = (0, -0.1, 0),
                    text_font = ToontownGlobals.getSignFont(),
                )
                counter['image'] = DGG.getDefaultDialogGeom()
                counter['image_scale'] = (0.33, 1, 0.33)                
                counter.setScale(0.5)
                counter.count = 0
                counter.max = self.pointsArray[index]
                self.counters.append(counter)

                # counter for total beans carried
                money = self.playerMoney[index]
                totalCounter = DirectLabel(
                    parent = hidden,
                    relief = None,
                    pos = (0.0, 0.0, 0.0),
                    text = str(money),
                    text_scale = 0.2,
                    text_fg = (0.95, 0.95, 0, 1),
                    text_pos = (0, -0.1, 0),
                    text_font = ToontownGlobals.getSignFont(),
                    image = self.jarImage,
                )
                totalCounter.setScale(0.5)
                totalCounter.count = money
                totalCounter.max = toon.getMaxMoney()
                self.totalCounters.append(totalCounter)
                
        # add a hook when user unexpectedly closes toontown window
        self.accept('clientCleanup', self._handleClientCleanup)

        # display the toons and jars
        pos = 0
        toonLayout = toonLayouts[numToons - 1]
        for toon in self.toons:
            thisPos = toonPositions[toonLayout[pos]]
            toon.setPos(Vec3(thisPos, 1.0, -2.5))
            toon.setHpr(Vec3(0, 0, 0))
            toon.setAnimState("neutral", 1)
            toon.setShadowHeight(0)
            if not toon.isDisabled():
                toon.reparentTo(render)
            self.counters[pos].setPos( thisPos * -0.17,
                                       0,
                                       toon.getHeight() / 10 + 0.25)
            self.counters[pos].reparentTo(aspect2d)
            self.totalCounters[pos].setPos( thisPos * -0.17,
                                            0,
                                            -0.825)
            self.totalCounters[pos].reparentTo(aspect2d)
            pos += 1

        # find the max points won 
        self.maxPoints = max(self.pointsArray)

        #find the maxVotes left
        if self.votesArray:
            self.maxVotes = max(self.votesArray)
            numToons = len(self.toons)
            self.voteMultiplier = TravelGameGlobals.PercentOfVotesConverted[numToons] / 100.0
            self.maxBeansFromVotes = int (self.voteMultiplier * self.maxVotes)
        else:
            self.maxVotes = 0
            self.maxBeansFromVotes = 0
        

        def reqCountUp(state):
            self.countUp()
            return Task.done

        countUpDelay = DELAY_BEFORE_COUNT_UP
        taskMgr.doMethodLater(countUpDelay, reqCountUp, "countUpTask")

        def reqCountDown(state):
            self.countDown()
            return Task.done
        
        countDownDelay = (countUpDelay +
                          self.maxPoints * COUNT_UP_RATE +
                          DELAY_AFTER_COUNT_UP)
        taskMgr.doMethodLater(countDownDelay, reqCountDown, "countDownTask")

        # play the jump animation for the winner(s)
        def celebrate(task):
            # hide the counters before we jump!
            for counter in task.counters:
                counter.hide()
            winningPoints = max(task.pointsArray)
            for i in range(len(task.ids)):
                if task.pointsArray[i] == winningPoints:
                    avId = task.ids[i]
                    if base.cr.doId2do.has_key(avId):
                        toon = base.cr.doId2do[avId]
                        toon.setAnimState("jump", 1.0)
                        
            base.playSfx(task.celebrateSound)            
            return Task.done     
        
        celebrateDelay = (countDownDelay +
                          self.maxPoints * COUNT_DOWN_RATE +
                          DELAY_AFTER_COUNT_DOWN)
        celebrateTask = taskMgr.doMethodLater(celebrateDelay, celebrate, "celebrate")
        celebrateTask.counters = self.counters
        celebrateTask.pointsArray = self.pointsArray
        celebrateTask.ids = self.ids
        celebrateTask.celebrateSound = self.celebrateSound

        def reqCountVotesUp(state):
            self.countVotesUp()
            return Task.done

        def reqCountVotesDown(state):
            self.countVotesDown()
            return Task.done        

        # show the player the votes left being converted to beans
        if self.metagameRound == TravelGameGlobals.FinalMetagameRoundIndex:
            countVotesUpDelay = celebrateDelay + DELAY_AFTER_CELEBRATE
            taskMgr.doMethodLater(countVotesUpDelay, reqCountVotesUp, "countVotesUpTask")
            
            countVotesUpTime = (self.maxVotes * COUNT_UP_RATE) + DELAY_AFTER_COUNT_UP
            countVotesDownDelay = countVotesUpDelay + countVotesUpTime
            taskMgr.doMethodLater(countVotesDownDelay, reqCountVotesDown, "countVotesDownTask")                                  
            celebrateDelay += countVotesUpTime + \
                              (self.maxVotes * COUNT_DOWN_RATE) + DELAY_AFTER_COUNT_DOWN
            
        # transition to the purchase after the countup is finished
        def reqPurchase(state):
            self.fsm.request("purchase")
            return Task.done
        purchaseDelay = (celebrateDelay +
                         DELAY_AFTER_CELEBRATE)
        taskMgr.doMethodLater(purchaseDelay,
                              reqPurchase,
                              "purchase-trans")

        if base.skipMinigameReward:
            self.fsm.request('purchase')
        
    def countUp(self):
        totalDelay = 0
        
        def delayAdd(state):
            # count the beans won counter up
            state.counter.count += 1
            state.counter['text'] = str(state.counter.count)
            if (state.toonId == base.localAvatar.doId):
                # play the counting sound
                base.playSfx(state.countSound)
            return Task.done

        # loop through all the counters and count down
        for count in range(0, self.maxPoints):
            for counter in self.counters:
                index = self.counters.index(counter)
                # change the display after COUNT_UP_RATE seconds
                if count < counter.max:
                    addTask = taskMgr.doMethodLater(totalDelay, delayAdd, "delayAdd")
                    addTask.counter = counter
                    # find out who's counter this is
                    addTask.toonId = self.ids[index]
                    addTask.countSound = self.countSound
            # keep track of the total delay so we know
            # when the beans are done tallying
            totalDelay += COUNT_UP_RATE
            
    def countDown(self):
        totalDelay = 0
        
        def delaySubtract(state):
            # count the beans won counter down and the total counter up
            state.counter.count -= 1
            state.counter['text'] = str(state.counter.count)
            state.total.count += 1
            # only update the total display if under max
            if state.total.count <= state.total.max:
                state.total['text'] = str(state.total.count)
            # if we have reached the max color the counter red
            if state.total.count == state.total.max + 1:
                state.total['text_fg'] = (1, 0, 0, 1)
            if (state.toonId == base.localAvatar.doId):
                # play the counting sound
                if state.total.count <= state.total.max:
                    base.playSfx(state.countSound)
                # or the over max sound
                else:
                    base.playSfx(state.overMaxSound)
            return Task.done

        # loop through all the counters and count down
        for count in range(0, self.maxPoints):
            for counter in self.counters:
                # if not zero change the display after COUNT_DOWN_RATE seconds
                if count < counter.max: 
                    index = self.counters.index(counter)
                    subtractTask = taskMgr.doMethodLater(totalDelay, delaySubtract, "delaySubtract")
                    subtractTask.counter = counter
                    subtractTask.total = self.totalCounters[index]
                    # find out who's counter this is
                    subtractTask.toonId = self.ids[index]
                    subtractTask.countSound = self.countSound
                    subtractTask.overMaxSound = self.overMaxSound                
            # keep track of the total delay so we know
            # when the beans are done tallying
            totalDelay += COUNT_DOWN_RATE

    def countVotesUp(self):
        totalDelay = 0
        self.convertingVotesToBeansLabel.show()

        # first reset self.counters.count to zero
        assert self.notify.debug('countVotesUp, resetting counters')
        counterIndex = 0
        for index in range(len(self.ids)):
            avId = self.ids[index]
            if ((self.states[index] != PURCHASE_NO_CLIENT_STATE) and
                (self.states[index] != PURCHASE_DISCONNECTED_STATE) and
                (avId in base.cr.doId2do)):
                self.counters[counterIndex].count = 0
                self.counters[counterIndex].max = self.votesArray[index]
                self.counters[counterIndex].show()
                counterIndex += 1
        
        def delayAdd(state):
            # count the votes left counter up
            state.counter.count += 1
            state.counter['text'] = str(state.counter.count)
            assert self.notify.debug('setting counter to %d' % state.counter.count)
            if (state.toonId == base.localAvatar.doId):
                # play the counting sound
                base.playSfx(state.countSound)
            return Task.done

        # loop through all the counters and count down
        for count in range(0, self.maxVotes):
            for counter in self.counters:
                index = self.counters.index(counter)
                # change the display after COUNT_UP_RATE seconds
                if count < counter.max:
                    addTask = taskMgr.doMethodLater(totalDelay, delayAdd, "delayAdd")
                    addTask.counter = counter
                    # find out who's counter this is
                    addTask.toonId = self.ids[index]
                    addTask.countSound = self.countSound
            # keep track of the total delay so we know
            # when the beans are done tallying
            totalDelay += COUNT_UP_RATE


    def countVotesDown(self):
        totalDelay = 0
        
        def delaySubtract(state):
            # count the beans won counter down and the total counter up
            state.counter.count -= 1
            state.counter['text'] = str(state.counter.count)
            state.total.count += (1 * self.voteMultiplier)
            # only update the total display if under max
            if state.total.count <= state.total.max:
                state.total['text'] = str(int(state.total.count))
            # if we have reached the max color the counter red
            if state.total.count == state.total.max + 1:
                state.total['text_fg'] = (1, 0, 0, 1)
            if (state.toonId == base.localAvatar.doId):
                # play the counting sound
                if state.total.count <= state.total.max:
                    base.playSfx(state.countSound)
                # or the over max sound
                else:
                    base.playSfx(state.overMaxSound)
            return Task.done

        # loop through all the counters and count down
        for count in range(0, self.maxVotes):
            for counter in self.counters:
                # if not zero change the display after COUNT_DOWN_RATE seconds
                if count < counter.max: 
                    index = self.counters.index(counter)
                    subtractTask = taskMgr.doMethodLater(totalDelay, delaySubtract, "delaySubtract")
                    subtractTask.counter = counter
                    subtractTask.total = self.totalCounters[index]
                    # find out who's counter this is
                    subtractTask.toonId = self.ids[index]
                    subtractTask.countSound = self.countSound
                    subtractTask.overMaxSound = self.overMaxSound                
            # keep track of the total delay so we know
            # when the beans are done tallying
            totalDelay += COUNT_DOWN_RATE
                        
            
    def exitReward(self):
        self.ignore('clientCleanup')
        taskMgr.remove("countUpTask")
        taskMgr.remove("countVotesUpTask")                
        taskMgr.remove("countDownTask")
        taskMgr.remove("countVotesDownTask")                        
        taskMgr.remove("celebrate")
        taskMgr.remove("purchase-trans")
        taskMgr.remove("delayAdd")        
        taskMgr.remove("delaySubtract")                
        # hide the toons
        for toon in self.toons:
            toon.detachNode()
        del self.toons
        if hasattr(self, 'toonsKeep'):
            for delayDelete in self.toonsKeep:
                delayDelete.destroy()
            del self.toonsKeep
        # hide the jelly bean jars
        for counter in self.counters:
            counter.reparentTo(hidden)
        for total in self.totalCounters:
            total.reparentTo(hidden)
        # hide the background elements
        self.foreground.reparentTo(hidden)
        self.backgroundL.reparentTo(hidden)
        self.backgroundR.reparentTo(hidden)
        self.sidewalk.reparentTo(hidden)
        self.door.reparentTo(hidden)
        self.title.reparentTo(self.frame)
        self.convertingVotesToBeansLabel.hide()
        # free the whisper bubbles
        NametagGlobals.setOnscreenChatForced(0)

    def _handleClientCleanup(self):
        """Handle the user unexpectedly closing the toontown window."""
        assert self.notify.debugStateCall(self)
        if hasattr(self, 'toonsKeep'):
            for delayDelete in self.toonsKeep:
                delayDelete.destroy()
            del self.toonsKeep        
        self.ignore('clientCleanup')
        pass
        
    ### Purchase state functions ###

    def enterPurchase(self):
        assert self.notify.debugStateCall(self)   
        PurchaseBase.enterPurchase(self)
        self.convertingVotesToBeansLabel.hide()
        self.bg.reparentTo(render)

        # Make the background light blue
        base.setBackgroundColor(0.05, 0.14, 0.4)
        
        # Listen for other toons changing state
        self.accept("purchaseStateChange", self.__handleStateChange)

        self.playAgain.reparentTo(self.toon.inventory.purchaseFrame)
        self.backToPlayground.reparentTo(self.toon.inventory.purchaseFrame)
        self.pointDisplay.reparentTo(self.toon.inventory.purchaseFrame)
        self.statusLabel.reparentTo(self.toon.inventory.purchaseFrame)
        

        for headFrame in self.headFrames:
            headFrame[1].show()
            headFrame[1].reparentTo(self.toon.inventory.purchaseFrame)

        # If the period timer expired while we were playing the last
        # minigame, honor it now.  We don't bother to continue to
        # listen to it expiring while we're shopping, however.
        if base.cr.periodTimerExpired:
            base.cr.loginFSM.request("periodTimeout")
            return

        if not self.tutorialMode:
            # Start the timer countdown
            if not config.GetBool('disable-purchase-timer', 0):
                self.timer.countdown(self.remain, self.__timerExpired)

            if config.GetBool('metagame-disable-playAgain',0):
                if self.metagameRound > -1:
                    self.disablePlayAgain()
            
        else:
            # set up for the tutorial
            self.timer.hide()
            self.disablePlayAgain()
            self.accept('disableGagPanel', Functor(
                self.toon.inventory.setActivateMode, 'gagTutDisabled',
                gagTutMode=1))
            self.accept('disableBackToPlayground', self.disableBackToPlayground)
            self.accept('enableGagPanel', self.handleEnableGagPanel)
            self.accept('enableBackToPlayground', self.enableBackToPlayground)
            # only show the headFrame of the noob
            for avId, headFrame in self.headFrames:
                if avId != self.newbieId:
                    headFrame.hide()
        
        messenger.send('gagScreenIsUp')

        if base.autoPlayAgain or self.doMetagamePlayAgain():
            base.transitions.fadeOut(0)
            self.__handlePlayAgain()

    def exitPurchase(self):
        assert self.notify.debugStateCall(self)        
        PurchaseBase.exitPurchase(self)
        self.ignore('disableGagPanel')
        self.ignore('disableBackToPlayground')
        self.ignore('enableGagPanel')
        self.ignore('enableBackToPlayground')
        self.bg.reparentTo(hidden)
        self.playAgain.reparentTo(self.frame)
        self.backToPlayground.reparentTo(self.frame)
        self.pointDisplay.reparentTo(self.frame)
        self.statusLabel.reparentTo(self.frame)
        self.ignore('purchaseStateChange')
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

        if base.autoPlayAgain or self.doMetagamePlayAgain():
            base.transitions.fadeIn()

    def disableBackToPlayground(self):
        self.backToPlayground['state'] = DGG.DISABLED
    def enableBackToPlayground(self):
        self.backToPlayground['state'] = DGG.NORMAL

    def disablePlayAgain(self):
        self.playAgain['state'] = DGG.DISABLED
    def enablePlayAgain(self):
        self.playAgain['state'] = DGG.NORMAL

    def enterTutorialMode(self, newbieId):
        # this will be set before we've entered the 'purchase' state;
        # set a flag and let purchase react to it
        self.tutorialMode = 1
        self.newbieId = newbieId

    def handleEnableGagPanel(self):
        # tutorial is now ready for gag to be purchased
        self.toon.inventory.setActivateMode('purchase', gagTutMode=1)
        self.checkForBroke()
        
    def handleGagTutorialDone(self):
        self.enableBackToPlayground()


    def doMetagamePlayAgain(self):
        """Return true if we should play again due to playing the metagame."""
        if hasattr(self, 'metagamePlayAgainResult'):
            assert self.notify.debug('doMetagamePlayAgain 1 returning %s' % self.metagamePlayAgainResult)
            return self.metagamePlayAgainResult

        # count how many toons are still connected
        numToons = 0
        for avId in self.ids:
            if base.cr.doId2do.has_key(avId) and \
               avId not in self.unexpectedExits:
                numToons +=1
                assert self.notify.debug('found avId=%s numToons=%s' % (avId, numToons))

        self.metagamePlayAgainResult = False
        if numToons > 1:
            if self.metagameRound > -1 and \
               self.metagameRound < TravelGameGlobals.FinalMetagameRoundIndex:
                self.metagamePlayAgainResult = True

        assert self.notify.debug('doMetagamePlayAgain 2 returning %s' % self.metagamePlayAgainResult)
        return self.metagamePlayAgainResult
        

    def setupUnexpectedExitHooks(self):
        """Setup hooks to inform us when other toons exit unexpectedly."""
        for avId in self.ids:
            if base.cr.doId2do.has_key(avId):
                toon = base.cr.doId2do[avId]
                eventName = toon.uniqueName('disable')
                self.accept(eventName,
                        self.__handleUnexpectedExit, extraArgs=[avId])
                self.unexpectedEventNames.append(eventName)

    def cleanupUnexpectedExitHooks(self):
        """Cleanup the unexpected exit hooks."""
        for eventName in self.unexpectedEventNames:
            self.ignore(eventName)

    def __handleUnexpectedExit(self, avId):
        """Add the disconnected avId to our list of unexpected exits."""
        assert self.notify.debugStateCall(self)
        self.unexpectedExits.append(avId)

        
class PurchaseHeadFrame(DirectFrame):

    notify = DirectNotifyGlobal.directNotify.newCategory("Purchase")
    
    def __init__(self, av, purchaseModels):
        DirectFrame.__init__(
            self,
            relief = None,
            image = purchaseModels.find("**/Char_Pnl"),
            )
        self.initialiseoptions(PurchaseHeadFrame)

        self.statusLabel = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_scale = TTLocalizer.PstatusLabel,
            text_wordwrap = 7.5,
            text_fg = (0.05, 0.14, 0.4, 1),
            text_pos = (0.1,0,0),
            )

        self.av = av
        # Do not allow the avatar to be deleted now
        # because we made a chat bubble and nametag on him
        # and try to delete them when we exit
        self.avKeep = DelayDelete.DelayDelete(av, 'PurchaseHeadFrame.av')
        self.accept('clientCleanup', self._handleClientCleanup)
        
        self.head = self.stateNodePath[0].attachNewNode('head', 20)
        self.head.setPosHprScale(-0.22, 10.0, -0.1,
                                 180., 0., 0.,
                                 0.1, 0.1, 0.1)
        
        self.headModel = ToonHead.ToonHead()
        self.headModel.setupHead(self.av.style, forGui = 1)
        self.headModel.reparentTo(self.head)

        # Make a nametag to display just the name.
        self.tag2Node = NametagFloat2d()
        self.tag2Node.setContents(Nametag.CName)
        self.av.nametag.addNametag(self.tag2Node)

        self.tag2 = self.attachNewNode(self.tag2Node.upcastToPandaNode())
        self.tag2.setPosHprScale(-0.22, 10.0, 0.12,
                                 0,0,0,
                                 0.046,0.046,0.046)

        # And another nametag for the chat balloon.  This gets
        # parented in after the above nametag, so the chat balloon
        # will be on top of the name if it needs to be.
        self.tag1Node = NametagFloat2d()
        self.tag1Node.setContents(Nametag.CSpeech | Nametag.CThought)
        self.av.nametag.addNametag(self.tag1Node)

        self.tag1 = self.attachNewNode(self.tag1Node.upcastToPandaNode())
        self.tag1.setPosHprScale(-0.15,0,-0.1,
                                 0,0,0,
                                 0.046,0.046,0.046)

        self.hide()
        
    def destroy(self):
        assert self.notify.debugStateCall(self)
        DirectFrame.destroy(self)
        del self.statusLabel
        self.headModel.delete()
        del self.headModel
        self.head.removeNode()
        del self.head
        self.av.nametag.removeNametag(self.tag1Node)
        self.av.nametag.removeNametag(self.tag2Node)
        self.tag1.removeNode()
        self.tag2.removeNode()
        del self.tag1
        del self.tag2
        del self.tag1Node
        del self.tag2Node
        del self.av
        self.removeAvKeep()

    def setAvatarState(self, state):
        #print "setavatarstate: ", self.av.doId, state
        if state == PURCHASE_DISCONNECTED_STATE:
            self.statusLabel['text'] = TTLocalizer.GagShopPlayerDisconnected % self.av.getName()
            self.statusLabel['text_pos'] = (0.015, 0.072, 0)
            self.head.hide()
            self.tag1.hide()
            self.tag2.hide()
        elif state == PURCHASE_EXIT_STATE:
            self.statusLabel['text'] = TTLocalizer.GagShopPlayerExited % self.av.getName()
            self.statusLabel['text_pos'] = (0.015, 0.072, 0)
            self.head.hide()
            self.tag1.hide()
            self.tag2.hide()
        elif state == PURCHASE_PLAYAGAIN_STATE:
            self.statusLabel['text'] = TTLocalizer.GagShopPlayerPlayAgain
            self.statusLabel['text_pos'] = (0.1, -0.12, 0)
        elif state == PURCHASE_WAITING_STATE:
            self.statusLabel['text'] = TTLocalizer.GagShopPlayerBuying
            self.statusLabel['text_pos'] = (0.1, -0.12, 0)
        elif state == PURCHASE_NO_CLIENT_STATE:
            # this may occur if we're in the gag purchase tutorial
            Purchase.notify.warning(
                "setAvatarState('no client state'); "
                "OK for gag purchase tutorial")
        else:
            Purchase.notify.warning('unknown avatar state: %s' % state)

    def _handleClientCleanup(self):
        """Handle the user unexpectedly closing the toontown window."""
        assert self.notify.debugStateCall(self)
        self.destroy()

    def removeAvKeep(self):
        """Safely remove our delay delete."""
        if hasattr(self,'avKeep'):
            self.notify.debug('destroying avKeep %s' % self.avKeep)
            self.avKeep.destroy()
            
            del self.avKeep
        self.ignore('clientCleanup')
