from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.distributed.ClockDelta import *
from DistributedMinigame import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task.Task import Task
from toontown.toonbase import ToontownTimer
import RaceGameGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class DistributedRaceGame(DistributedMinigame):

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.gameFSM = ClassicFSM.ClassicFSM('DistributedRaceGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['inputChoice']),
                                State.State('inputChoice',
                                            self.enterInputChoice,
                                            self.exitInputChoice,
                                            ['waitServerChoices',
                                             'moveAvatars',
                                             'cleanup']),
                                State.State('waitServerChoices',
                                            self.enterWaitServerChoices,
                                            self.exitWaitServerChoices,
                                            ['moveAvatars',
                                             'cleanup']),
                                State.State('moveAvatars',
                                            self.enterMoveAvatars,
                                            self.exitMoveAvatars,
                                            ['inputChoice', 'winMovie',
                                             'cleanup']),
                                State.State('winMovie',
                                            self.enterWinMovie,
                                            self.exitWinMovie,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                ],
                               # Initial State
                               'off',
                               # Final State
                               'cleanup',
                               )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        # New short board
        self.posHprArray = (
            ((-9.03, 0.06, 0.025, -152.90),
             (-7.43, -2.76, 0.025, -152.68),
             (-6.02, -5.48, 0.025, -157.54),
             (-5.01, -8.32, 0.025, -160.66),
             (-4.05, -11.36, 0.025, -170.22),
             (-3.49, -14.18, 0.025, -175.76),
             (-3.12, -17.15, 0.025, -177.73),
             (-3.00, -20.32, 0.025, 178.49),
             (-3.09, -23.44, 0.025, 176.59),
             (-3.43, -26.54, 0.025, 171.44),
             (-4.07, -29.44, 0.025, 163.75),
             (-5.09, -32.27, 0.025, 158.20),
             (-6.11, -35.16, 0.025, 154.98),
             (-7.57, -37.78, 0.025, 154.98),
             (-9.28, -40.65, 0.025, 150.41),
             ),
            ((-6.12, 1.62, 0.025, -152.90),
             (-4.38, -1.35, 0.025, -150.92),
             (-3.08, -4.30, 0.025, -157.90),
             (-1.85, -7.26, 0.025, -162.54),
             (-0.93, -10.49, 0.025, -167.71),
             (-0.21, -13.71, 0.025, -171.79),
             (0.21, -17.08, 0.025, -174.92),
             (0.31, -20.20, 0.025, 177.10),
             (0.17, -23.66, 0.025, 174.82),
             (-0.23, -26.91, 0.025, 170.51),
             (-0.99, -30.20, 0.025, 162.54),
             (-2.02, -33.28, 0.025, 160.48),
             (-3.28, -36.38, 0.025, 157.96),
             (-4.67, -39.17, 0.025, 154.13),
             (-6.31, -42.15, 0.025, 154.13),
             ),
            ((-2.99, 3.09, 0.025, -154.37),
             (-1.38, -0.05, 0.025, -154.75),
             (-0.19, -3.29, 0.025, -159.22),
             (1.17, -6.51, 0.025, -162.74),
             (2.28, -9.80, 0.025, -168.73),
             (3.09, -13.28, 0.025, -173.49),
             (3.46, -16.63, 0.025, -176.81),
             (3.69, -20.38, 0.025, 179.14),
             (3.61, -24.12, 0.025, 175.78),
             (3.00, -27.55, 0.025, 170.87),
             (2.15, -30.72, 0.025, 167.41),
             (1.04, -34.26, 0.025, 162.11),
             (-0.15, -37.44, 0.025, 158.59),
             (-1.64, -40.52, 0.025, 153.89),
             (-3.42, -43.63, 0.025, 153.89),
             ),
            ((0.00, 4.35, 0.025, -154.37),
             (1.52, 1.30, 0.025, -155.67),
             (3.17, -2.07, 0.025, -155.67),
             (4.47, -5.41, 0.025, -163.00),
             (5.56, -9.19, 0.025, -168.89),
             (6.22, -12.66, 0.025, -171.67),
             (6.67, -16.56, 0.025, -176.53),
             (6.93, -20.33, 0.025, 179.87),
             (6.81, -24.32, 0.025, 175.19),
             (6.22, -27.97, 0.025, 170.81),
             (5.59, -31.73, 0.025, 167.54),
             (4.48, -35.42, 0.025, 161.92),
             (3.06, -38.82, 0.025, 158.56),
             (1.40, -42.00, 0.025, 154.32),
             (-0.71, -45.17, 0.025, 153.27),
             )
            )

        self.avatarPositions = {}
        self.modelCount = 8

        self.cameraTopView = (-22.78, -41.65, 31.53, -51.55, -42.68, -2.96)

        # These are None to indicate we have not yet established a
        # timer; they are filled in as we enter the inputChoice state
        # and as the AI reports a start time, respectively.  When both
        # are filled in, the timer will be displayed.
        self.timer = None
        self.timerStartTime = None

    def getTitle(self):
        return TTLocalizer.RaceGameTitle

    def getInstructions(self):
        return TTLocalizer.RaceGameInstructions

    def getMaxDuration(self):
        # the duration of this game is really variable; fudge it
        return 60

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # Black screen
        self.raceBoard = loader.loadModel("phase_4/models/minigames/race")
        self.raceBoard.setPosHpr(0, 0, 0, 0, 0, 0)
        self.raceBoard.setScale(0.8)

        self.dice = loader.loadModel("phase_4/models/minigames/dice")
        # These are used to show what each avatar picked
        self.dice1 = self.dice.find("**/dice_button1")
        self.dice2 = self.dice.find("**/dice_button2")
        self.dice3 = self.dice.find("**/dice_button3")
        self.dice4 = self.dice.find("**/dice_button4")
        self.diceList = [self.dice1, self.dice2, self.dice3, self.dice4]

        self.music = base.loadMusic("phase_4/audio/bgm/minigame_race.mid")
        # The sound that is played when local toon gets a unique choice
        self.posBuzzer = base.loadSfx("phase_4/audio/sfx/MG_pos_buzzer.wav")
        # The sound that is played when local toon gets a bad choice
        self.negBuzzer = base.loadSfx("phase_4/audio/sfx/MG_neg_buzzer.wav")
        self.winSting = base.loadSfx("phase_4/audio/sfx/MG_win.mp3")
        self.loseSting = base.loadSfx("phase_4/audio/sfx/MG_lose.mp3")

        self.diceButtonList = []
        for i in range(1,5):
            button = self.dice.find("**/dice_button" + str(i))
            button_down = self.dice.find("**/dice_button" + str(i) + "_down")
            button_ro = self.dice.find("**/dice_button" + str(i) + "_ro")
            diceButton = DirectButton(
                image = (button, button_down, button_ro, None),
                relief = None,
                pos = (-0.9 + ((i-1)*0.2), 0.0, -0.85),
                scale = 0.25,
                command = self.handleInputChoice,
                extraArgs = [i],
                )
            diceButton.hide()
            self.diceButtonList.append(diceButton)

        self.waitingChoicesLabel = DirectLabel(
            text = TTLocalizer.RaceGameWaitingChoices,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.6, 0, -0.75),
            scale = 0.075)
        self.waitingChoicesLabel.hide()

        # load the chance card marker
        self.chanceMarker = loader.loadModel(
            "phase_4/models/minigames/question_mark")

        # load the chance card
        self.chanceCard = loader.loadModel(
            "phase_4/models/minigames/chance_card")

        # chance card text
        self.chanceCardText = OnscreenText(
            "",
            fg = (1.0, 0, 0, 1),
            scale = 0.14,
            font = ToontownGlobals.getSignFont(),
            wordwrap = 14,
            pos = (0.0, 0.2),
            mayChange = 1,
            )
        self.chanceCardText.hide()

        
        # The sound that is played when chance card is revealed
        self.cardSound = base.loadSfx(
            "phase_3.5/audio/sfx/GUI_stickerbook_turn.mp3")

        self.chanceMarkers = []

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        self.raceBoard.removeNode()
        del self.raceBoard
        self.dice.removeNode()
        del self.dice
        self.chanceMarker.removeNode()
        del self.chanceMarker
        self.chanceCardText.removeNode()
        del self.chanceCardText
        self.chanceCard.removeNode()
        del self.chanceCard
        self.waitingChoicesLabel.destroy()
        del self.waitingChoicesLabel
        del self.music
        del self.posBuzzer
        del self.negBuzzer
        del self.winSting
        del self.loseSting
        del self.cardSound
        for button in self.diceButtonList:
            button.destroy()
        del self.diceButtonList
        for marker in self.chanceMarkers:
            marker.removeNode()
            del(marker)
        del self.chanceMarkers
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.8)
        # Set the stage
        self.raceBoard.reparentTo(render)
        camera.reparentTo(render)
        p = self.cameraTopView
        camera.setPosHpr(p[0], p[1], p[2], p[3], p[4], p[5])
        base.transitions.irisIn(0.4)
        # set the background color to match the game board
        base.setBackgroundColor(0.1875, 0.7929, 0)

    def offstage(self):
        self.notify.debug("offstage")
        DistributedMinigame.offstage(self)
        # Stop music
        self.music.stop()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        self.raceBoard.reparentTo(hidden)
        self.chanceCard.reparentTo(hidden)
        self.chanceCardText.hide()
        if hasattr(self, 'chanceMarkers'):
            for marker in self.chanceMarkers:
                marker.reparentTo(hidden)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        
        self.resetPositions()
        # Make the avatars all run in
        for i in range(self.numPlayers):
            avId = self.avIdList[i]

            if(self.localAvId == avId):
                self.localAvLane = i

            # Find the actual avatar in the cr
            avatar = self.getAvatar(avId)
            if avatar:
                # Position the avatar in lane i, place 0 (the starting place)
                avatar.reparentTo(render)
                # Neutral animation cycle
                avatar.setAnimState("neutral", 1)
                self.positionInPlace(avatar, i, 0)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        self.gameFSM.request("inputChoice")

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterInputChoice(self):
        self.notify.debug("enterInputChoice")
        for button in self.diceButtonList:
            button.show()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.hide()
        if self.timerStartTime != None:
            self.startTimer()


    def startTimer(self):
        """startTimer(self)
        Starts the timer display running during the inputChoice state,
        once we have received the timerStartTime from the AI.
        """
        now = globalClock.getFrameTime()
        elapsed = now - self.timerStartTime
        self.timer.posInTopRightCorner()
        self.timer.setTime(RaceGameGlobals.InputTimeout)
        self.timer.countdown(RaceGameGlobals.InputTimeout - elapsed,
                             self.handleChoiceTimeout)
        self.timer.show()

    def setTimerStartTime(self, timestamp):
        """setTimeStartTime(self, int16 timestamp)

        This message is sent from the AI to indicate the point at
        which the timer starts (or started) counting.  It's used to
        synchronize the timer display with the actual countdown on the
        AI.
        """
        if not self.hasLocalToon: return
        self.timerStartTime = globalClockDelta.networkToLocalTime(timestamp)
        if self.timer != None:
            self.startTimer()

    def exitInputChoice(self):
        for button in self.diceButtonList:
            button.hide()

        if self.timer != None:
            self.timer.destroy()
            self.timer = None
        self.timerStartTime = None
        self.ignore("diceButton")

    def handleChoiceTimeout(self):
        # If we timeout locally, send a 0 for our choice
        self.sendUpdate("setAvatarChoice", [0])
        self.gameFSM.request("waitServerChoices")

    def handleInputChoice(self, choice):
        # The number we choose will be checked on the server to prevent hacking
        self.sendUpdate("setAvatarChoice", [choice])
        self.gameFSM.request("waitServerChoices")

    def enterWaitServerChoices(self):
        self.notify.debug("enterWaitServerChoices")
        self.waitingChoicesLabel.show()

    def exitWaitServerChoices(self):
        self.waitingChoicesLabel.hide()

    def localToonWon(self):
        localToonPosition = self.avatarPositions[self.localAvId]
        if localToonPosition >= RaceGameGlobals.NumberToWin:
            # If any single avatar won, return true
            self.notify.debug("localToon won")
            return 1
        else:
            return 0

    def anyAvatarWon(self):
        for position in self.avatarPositions.values():
            if position >= RaceGameGlobals.NumberToWin:
                # If any single avatar won, return true
                self.notify.debug("anyAvatarWon: Somebody won")
                return 1
        # If we checked all avatars and nobody won, return 0
        self.notify.debug("anyAvatarWon: Nobody won")
        return 0

    def showNumbers(self, task):
        self.notify.debug("showing numbers...")
        self.diceInstanceList = []
        for i in range(len(task.choiceList)):
            avId   = self.avIdList[i]
            choice = task.choiceList[i]
            if choice == 0:
                # Append None just to keep the list in sync
                self.diceInstanceList.append(None)
            else:
                diceInstance = self.diceList[choice - 1].copyTo(self.raceBoard)
                self.diceInstanceList.append(diceInstance)
                # Put it one position in front of the avatar
                dicePosition = self.avatarPositions[avId] + 1
                diceInstance.setScale(4.0)
                self.positionInPlace(diceInstance, i, dicePosition)
                # Correct the pitch on the dice so it is laying flat
                diceInstance.setP(-90)
                diceInstance.setZ(0.05)
        return Task.done

    def showMatches(self, task):
        self.notify.debug("showing matches...")
        for i in range(len(task.choiceList)):
            avId   = self.avIdList[i]
            choice = task.choiceList[i]
            if choice != 0:
                diceInstance = self.diceInstanceList[i]
                # See how many people chose this number
                freq = task.choiceList.count(choice)
                # Only update if the choice is unique
                if (freq == 1):
                    # Green to indicate a success
                    diceInstance.setColor(0.2,1,0.2,1)
                    if avId == self.localAvId:
                        base.playSfx(self.posBuzzer)
                else:
                    # Red to indicate a clash
                    diceInstance.setColor(1,0.2,0.2,1)
                    if avId == self.localAvId:
                        base.playSfx(self.negBuzzer)
        return Task.done

    def hideNumbers(self, task):
        self.notify.debug("hiding numbers...")
        for dice in self.diceInstanceList:
            if dice:
                dice.removeNode()
        self.diceInstanceList = []
        return Task.done

    def enterMoveAvatars(self, choiceList, positionList, rewardList):
        self.notify.debug("in enterMoveAvatars:")
        # These arrays could contain multiple turn information,
        # so unroll them one turn at a time
        tasks = []

        # Make a copy for getLongestLerpTime to stomp on
        self.avatarPositionsCopy = self.avatarPositions.copy()
        
        for i in range(0, len(choiceList)/self.numPlayers):
            startIndex = i * self.numPlayers
            endIndex = startIndex + self.numPlayers
            self.choiceList = choiceList[startIndex:endIndex]
            self.positionList = positionList[startIndex:endIndex]
            self.rewardList = rewardList[startIndex:endIndex]


            self.notify.debug("           turn: " + str(i + 1))
            self.notify.debug("     choiceList: " + str(self.choiceList))
            self.notify.debug("   positionList: " + str(self.positionList))
            self.notify.debug("     rewardList: " + str(self.rewardList))

            longestLerpTime = self.getLongestLerpTime(i > 0)

            self.notify.debug("longestLerpTime: " + str(longestLerpTime))

            # only need to do this once
            if i == 0:
                snt = Task(self.showNumbers)
                snt.choiceList = self.choiceList
                smt = Task(self.showMatches)
                smt.choiceList = self.choiceList
                tasks += [snt,
                          Task.pause(0.5),
                          smt,]

            # there may be multiple moves per turn thanks to the
            # chance cards. Concatenate all tasks into a list,
            # then make one big sequence out of the lists
            if longestLerpTime > 0.0:
                self.notify.debug("someone moved...")
                # If anybody moves, add all these task
                mat = Task(self.moveAvatars)
                mat.choiceList = self.choiceList
                mat.positionList = self.positionList
                mat.rewardList = self.rewardList
                mat.name = "moveAvatars"
                if i == 0:
                    tasks += [Task.pause(0.75),
                              # Start moving the avatars with the numbers up
                              # for just a brief time
                              mat,
                              Task.pause(0.75),
                              Task(self.hideNumbers),
                              # Wait for the walk to finish
                              Task.pause(longestLerpTime - 0.5),]
                else:
                    mat.chance = 1
                    tasks += [mat,
                              # Wait for the walk to finish
                              Task.pause(longestLerpTime),]

                # check for chance card hit in this lane
                tasks += self.showChanceRewards()
            else:
                self.notify.debug("no one moved...")
                # If nobody moves, use this sequence
                tasks += [Task.pause(1.0),
                          Task(self.hideNumbers)]

        self.notify.debug("task list : " +  str(tasks))
        
        # now make and spawn a sequence out of our compiled task list
        wdt = Task(self.walkDone)
        wdt.name = "walk done"
        tasks.append(wdt)
        moveTask = Task.sequence(*tasks)
        taskMgr.add(moveTask, "moveAvatars")


    def walkDone(self, task):
        # Clear the temp lists
        self.choiceList = []
        self.positionList = []

        # If we have checked the chance cards, see if anybody won
        if self.anyAvatarWon():
            self.gameFSM.request("winMovie")
        else:
            self.gameFSM.request("inputChoice")
        return Task.done

    def getLongestLerpTime(self, afterFirst):
        self.notify.debug("afterFirst: " + str(afterFirst))
        # The choiceList should be in lane order from the server        
        longestTime = 0.0
        for i in range(len(self.choiceList)):
            # See how many people chose this number
            freq = self.choiceList.count(self.choiceList[i])
            # Only update if the choice is unique, unless this is one
            # of the chance card movements.
            if (afterFirst or freq == 1):
                oldPosition = self.avatarPositionsCopy[self.avIdList[i]]
                newPosition = self.positionList[i]
                self.avatarPositionsCopy[self.avIdList[i]] = newPosition
                squares_walked = abs(newPosition - oldPosition)
                longestTime = max(longestTime, self.getWalkDuration(squares_walked))
        return longestTime

    def showChanceRewards(self):
        # modify avatar positions for each chance card
        tasks = []
        for reward in self.rewardList:
            self.notify.debug("showChanceRewards: reward = " + str(reward))
            index = self.rewardList.index(reward) 
            # if an actual reward is present in the list
            if (reward != -1):
                self.notify.debug("adding tasks!")
                # hide the chance marker
                hcc = Task(self.hideChanceMarker)
                hcc.chanceMarkers = self.chanceMarkers
                hcc.index = index
                # create the tasks to display the card
                sct = Task(self.showChanceCard)
                sct.chanceCard = self.chanceCard
                sct.cardSound = self.cardSound
                stt = Task(self.showChanceCardText)
                rewardEntry = RaceGameGlobals.ChanceRewards[reward]
                stt.rewardIdx = reward
                # decide if its a good or bad reward based on movement
                # might be better to flag each one individually in the defns
                if ((rewardEntry[0][0] < 0) or (rewardEntry[0][1] > 0)):
                    stt.sound = self.negBuzzer
                else:
                    stt.sound = self.posBuzzer
                stt.picker = self.avIdList[index]
                rct = Task(self.resetChanceCard)
                task = Task.sequence(
                    hcc,
                    sct,
                    Task.pause(1.0),
                    stt,
                    Task.pause(3.0),
                    rct,
                    Task.pause(0.25),)
                tasks.append(task)
        return tasks

    def showChanceCard(self, task):
        # lerp the chance card to the camera and display
        # chance card text
        base.playSfx(task.cardSound)
        self.chanceCard.reparentTo(render)
        self.chanceCard.lerpPosHpr(19.62, 13.41, 13.14,
                                   270, 0, -85.24, 1.0,
                                   other=camera,
                                   task="cardLerp")
        return Task.done

    def hideChanceMarker(self, task):
        # lerp the chance card to the camera and display
        # chance card text
        task.chanceMarkers[task.index].reparentTo(hidden)
        return Task.done

    def showChanceCardText(self, task):
        self.notify.debug("showing chance reward: " + str(task.rewardIdx))
        name = self.getAvatar(task.picker).getName()
        rewardEntry = RaceGameGlobals.ChanceRewards[task.rewardIdx]
        cardText = ""
        if(rewardEntry[1] != -1):
            rewardstr_fmt = TTLocalizer.RaceGameCardText
            if(rewardEntry[2] > 0):
                rewardstr_fmt = TTLocalizer.RaceGameCardTextBeans
            cardText = rewardstr_fmt % {'name': name, 'reward': rewardEntry[1]}
        else:
            rewardstr_fmt = TTLocalizer.RaceGameCardTextHi1
            cardText = rewardstr_fmt % {'name': name}

        base.playSfx(task.sound)
        self.chanceCardText.setText(cardText)
        self.chanceCardText.show()
        return Task.done

    def resetChanceCard(self, task):
        self.chanceCardText.hide()
        self.chanceCard.reparentTo(hidden)
        self.chanceCard.setPosHpr(0,0,0,0,0,0)
        return Task.done

    def moveCamera(self):
        # find the integer position of the avatar farthest ahead
        bestPosIdx = self.avatarPositions.values()[0]
        best_lane = 0
        cur_lane = 0
        for pos in self.avatarPositions.values():
            if pos > bestPosIdx:
                bestPosIdx = pos
                best_lane = cur_lane
            cur_lane = cur_lane + 1

        # clamp player to max game board pos
        bestPosIdx = min(RaceGameGlobals.NumberToWin, bestPosIdx)
        localToonPosition = self.avatarPositions[self.localAvId]

        # set the new parameters to determine the target HPR
        # to find the new HPR, need to use lookAt, which requires
        # temporarily resetting camera parameters
        savedCamPos = camera.getPos()
        savedCamHpr = camera.getHpr()

        # for pos1, dont go past 4th from end
        pos1_idx = min(RaceGameGlobals.NumberToWin-4, localToonPosition)
        pos1 = self.posHprArray[self.localAvLane][pos1_idx]

        # pos2 should be 4 past localAv (so you can see all the squares in front of you),
        # or 1 past the furthest av (so you can see who's in front)

        bestPosLookAtIdx = bestPosIdx + 1
        localToonLookAtIdx = localToonPosition + 4

        if (localToonLookAtIdx >= bestPosLookAtIdx):
            pos2_idx = localToonLookAtIdx
            pos2_idx = min(RaceGameGlobals.NumberToWin, pos2_idx)
            pos2 = self.posHprArray[self.localAvLane][pos2_idx]
        else:
            pos2_idx = bestPosLookAtIdx
            pos2_idx = min(RaceGameGlobals.NumberToWin, pos2_idx)
            pos2 = self.posHprArray[best_lane][pos2_idx]

        posDeltaVecX = pos2[0] - pos1[0]
        posDeltaVecY = pos2[1] - pos1[1]

        DistanceMultiplier = 0.8   # distance beyond pos2 to put camera

        camposX = pos2[0] + DistanceMultiplier * posDeltaVecX
        camposY = pos2[1] + DistanceMultiplier * posDeltaVecY

        race_fraction = bestPosIdx/float(RaceGameGlobals.NumberToWin)

        # start high, get lower so cam can see most of track at end
        CamHeight = 10.0 * race_fraction + (1.0-race_fraction) * 22.0

        CamPos = Vec3(camposX,camposY,pos2[2]+CamHeight)

        camera.setPos(CamPos)

        # HPR determination

        # do we want to factor the frontmost toon in lookat as well as the localToonPos?
        # no for now, seems to work ok just using localToonPos

        # -6 empirically determined, we dont want to go beyond that to keep things mostly onscreen
        camera_lookat_idx = min(RaceGameGlobals.NumberToWin-6, localToonPosition)
        posLookAt = self.posHprArray[self.localAvLane][camera_lookat_idx]
        camera.lookAt(posLookAt[0],posLookAt[1],posLookAt[2])

        # get the newly computed target HPR
        CamHpr = camera.getHpr()

        # put the camera back to original poshpr
        camera.setPos(savedCamPos)
        camera.setHpr(savedCamHpr)

        # set up lerp to new poshpr
        camera.lerpPosHpr(CamPos[0], CamPos[1], CamPos[2],
                          CamHpr[0], CamHpr[1], CamHpr[2], 0.75)

    def getWalkDuration(self, squares_walked):
        # Walk duration is scaled to how far you need to walk
        # which is, of course, the number you chose (choice)
        # Dividing by 1.2 seems like about the right speed

        walkDuration = abs(squares_walked/1.2)
        if(squares_walked > 4):
            walkDuration = walkDuration * 0.3   # here you will be running
        return walkDuration

    def moveAvatars(self, task):

        self.notify.debug("In moveAvatars: ")
        self.notify.debug("    choiceList: " + str(task.choiceList))
        self.notify.debug("  positionList: " + str(task.positionList))
        self.notify.debug("  rewardList: " + str(task.rewardList))

        # Move the avatars
        # The choiceList should be in lane order
        for i in range(len(self.choiceList)):
            avId   = self.avIdList[i]
            choice = task.choiceList[i]
            position = task.positionList[i]
            chance = max(0, hasattr(task, "chance"))
            if (choice != 0):
                # Update our position dict with the new pos
                oldPosition = self.avatarPositions[avId]
                self.avatarPositions[avId] = position

                # Update the camera
                self.moveCamera()

                # if this is not result of a chance card draw,
                # then ignore duplicate choices
                if ( (not chance) and (task.choiceList.count(choice) != 1) ):
                    self.notify.debug("duplicate choice!")
                else:
                    avatar = self.getAvatar(avId)
                    if avatar:
                        squares_walked = abs(position - oldPosition)  # abs() allows 'running' backward.
                        # if the choice is very large (ie chance card victory)
                        # we will need to behave differently
                        if (squares_walked > 4):
                            self.notify.debug("running")
                            avatar.setPlayRate(1.0, "run")
                            self.runInPlace(avatar, i, oldPosition, position, self.getWalkDuration(squares_walked))
                        else:
                            # set the play rate based on direction
                            if (choice > 0):
                                self.notify.debug("walking forwards")
                                avatar.setPlayRate(1.0, "walk")
                            else:
                                self.notify.debug("walking backwards")
                                avatar.setPlayRate(-1.0, "walk")
                            # Position the avatar in lane i, at position
                            self.walkInPlace(avatar, i, position, self.getWalkDuration(squares_walked))
        return Task.done

    def exitMoveAvatars(self):
        self.notify.debug("In exitMoveAvatars: removing hooks")
        taskMgr.remove("moveAvatars")
        #for lane in range(self.numPlayers):
        #    taskMgr.remove("startWalk-" + str(lane))
        #    taskMgr.remove("startRun-" + str(lane))            
        return None

    def gameOverCallback(self, task):
        self.gameOver()
        return Task.done

    def enterWinMovie(self):
        self.notify.debug("enterWinMovie")
        if (self.localToonWon()):
            base.playSfx(self.winSting)
        else:
            base.playSfx(self.loseSting)

        # For now, instead of a fancy win movie, just make the winning
        # avatar(s) jump for joy.
        for avId in self.avIdList:
            avPosition = self.avatarPositions[avId]
            if avPosition >= RaceGameGlobals.NumberToWin:
                avatar = self.getAvatar(avId)
                if avatar:
                    # be sure to stop this avatar's neutral from playing
                    lane = str(self.avIdList.index(avId))
                    taskMgr.remove("runAvatar-" + lane)
                    taskMgr.remove("walkAvatar-" + lane)
                    avatar.setAnimState("jump", 1.0)

        taskMgr.doMethodLater(4.0, self.gameOverCallback, "playMovie")

    def exitWinMovie(self):
        taskMgr.remove("playMovie")
        self.winSting.stop()
        self.loseSting.stop()

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    def positionInPlace(self, avatar, lane, place):
        # Put the avatar in lane and place specified
        # Clamp the place to the length of the lane
        place = min(place, len(self.posHprArray[lane]) - 1)
        posH = self.posHprArray[lane][place]
        avatar.setPosHpr(self.raceBoard,
                         posH[0], posH[1], posH[2], posH[3], 0, 0)

    def walkInPlace(self, avatar, lane, place, time):
        # Put the avatar in lane and place specified
        # Clamp the place to the length of the lane
        place = min(place, len(self.posHprArray[lane]) - 1)
        posH = self.posHprArray[lane][place]

        def startWalk(task):
            task.avatar.setAnimState("walk", 1)
            return Task.done
        startWalkTask = Task(startWalk, "startWalk-" + str(lane))
        startWalkTask.avatar = avatar

        def stopWalk(task, raceBoard=self.raceBoard, posH=posH):
            task.avatar.setAnimState("neutral", 1)
            if raceBoard.isEmpty():
                task.avatar.setPosHpr(0, 0, 0, 0, 0, 0)
            else:
                task.avatar.setPosHpr(raceBoard,
                                      posH[0], posH[1], posH[2],
                                      posH[3], 0, 0)
            return Task.done
        stopWalkTask = Task(stopWalk, "stopWalk-" + str(lane))
        stopWalkTask.avatar = avatar

        walkTask = Task.sequence(startWalkTask,
                                 avatar.lerpPosHpr(posH[0], posH[1], posH[2],
                                                   posH[3], 0, 0,
                                                   time, # seconds
                                                   other=self.raceBoard),
                                 stopWalkTask,
                                 )
        
        taskMgr.add(walkTask, "walkAvatar-" + str(lane))

    def runInPlace(self, avatar, lane, currentPlace, newPlace, time):
        # Put the avatar in lane and place specified
        # Clamp the place to the length of the lane
        place = min(newPlace, len(self.posHprArray[lane]) - 1)

        # we need to approximate the curve of the track
        # better by using more sample points
        step = (place - currentPlace) / 3
        pos1 = self.posHprArray[lane][currentPlace + step]
        pos2 = self.posHprArray[lane][currentPlace + 2 * step]
        pos3 = self.posHprArray[lane][place]

        def startRun(task):
            task.avatar.setAnimState("run", 1)
            return Task.done
        startRunTask = Task(startRun, "startRun-" + str(lane))
        startRunTask.avatar = avatar

        def stopRun(task, raceBoard=self.raceBoard, pos3=pos3):
            task.avatar.setAnimState("neutral", 1)
            task.avatar.setPosHpr(raceBoard,
                                  pos3[0], pos3[1], pos3[2],
                                  pos3[3], 0, 0)
            return Task.done
        stopRunTask = Task(stopRun, "stopRun-" + str(lane))
        stopRunTask.avatar = avatar

        runTask = Task.sequence(startRunTask,
                                avatar.lerpPosHpr(pos1[0], pos1[1], pos1[2],
                                                  pos1[3], 0, 0,
                                                  time / 3., # seconds
                                                  other=self.raceBoard),
                                avatar.lerpPosHpr(pos2[0], pos2[1], pos2[2],
                                                  pos2[3], 0, 0,
                                                  time / 3., # seconds
                                                  other=self.raceBoard),
                                avatar.lerpPosHpr(pos3[0], pos3[1], pos3[2],
                                                  pos3[3], 0, 0,
                                                  time / 3., # seconds
                                                  other=self.raceBoard),
                                stopRunTask,
                                )

        taskMgr.add(runTask, "runAvatar-" + str(lane))

    def setAvatarChoice(self, choice):
        # This should only be called on the server
        self.notify.error("setAvatarChoice should not be called on the client")

    def setAvatarChose(self, avId):
        if not self.hasLocalToon: return
        # The server is telling the client that this
        # avatar has finished choosing his number
        self.notify.debug("setAvatarChose: avatar: " + str(avId) + " choose a number")
        # TODO: represent this graphically

    def setChancePositions(self, positions):
        if not self.hasLocalToon: return
        # place the chance marker in the positions
        # specified by the server
        row = 0
        for pos in positions:
            marker = self.chanceMarker.copyTo(render)
            posHpr = self.posHprArray[row][pos]
            marker.setPosHpr(self.raceBoard,
                             posHpr[0], posHpr[1], posHpr[2],
                             posHpr[3] + 180, 0, 0.025)
            marker.setScale(0.7)
            self.chanceMarkers.append(marker)
            row += 1

    # TODO: don't bother sending the avIDs
    def setServerChoices(self, choices, positions, rewards):
        if not self.hasLocalToon: return
        # The server sends this when all avatars have choosen their attacks

        # clamp all positions to actual board (values may be bogus for instant-winner)
        for i in range(len(positions)):
            if(positions[i] > RaceGameGlobals.NumberToWin):
                positions[i] = RaceGameGlobals.NumberToWin
            if(positions[i] < 0):
                positions[i] = 0

        self.notify.debug("setServerChoices: %s positions: %s rewards: %s " %
                          (choices, positions, rewards))

        self.gameFSM.request("moveAvatars", [choices, positions, rewards])

    def resetPositions(self):
        # Reset all avatar positions to 0
        for avId in self.avIdList:
            self.avatarPositions[avId] = 0

