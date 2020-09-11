from toontown.toonbase.ToontownBattleGlobals import *

import types
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import TownBattleAttackPanel
import TownBattleWaitPanel
import TownBattleChooseAvatarPanel
import TownBattleSOSPanel
import TownBattleSOSPetSearchPanel
import TownBattleSOSPetInfoPanel
import TownBattleToonPanel
from toontown.toontowngui import TTDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattleBase
from toontown.toonbase import ToontownTimer
from direct.showbase import PythonUtil
from toontown.toonbase import TTLocalizer
from toontown.pets import PetConstants
from direct.gui.DirectGui import DGG
from toontown.battle import FireCogPanel

class TownBattle(StateData.StateData):

    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattle')

    evenPos = (0.75, 0.25, -0.25, -0.75)
    oddPos = (0.5, 0, -0.5)

    def __init__(self, doneEvent):
        """ __init__(doneEvent)
        """
        StateData.StateData.__init__(self, doneEvent)

        self.numCogs = 1
        self.creditLevel = None
        self.luredIndices = []
        self.trappedIndices = []

        self.numToons = 1
        self.toons = []
        self.localNum = 0
        self.time = 0

        self.bldg = 0
        self.track = -1
        self.level = -1

        self.target = 0

        self.toonAttacks = [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0)]

        self.fsm = ClassicFSM.ClassicFSM('TownBattle',
                        [State.State('Off',
                                     self.enterOff,
                                     self.exitOff,
                                     ['Attack']),
                         State.State('Attack',
                                     self.enterAttack,
                                     self.exitAttack,
                                     ['ChooseCog',
                                      'ChooseToon',
                                      'AttackWait',
                                      'Run',
                                      'Fire',
                                      'SOS',]),
                         State.State('ChooseCog',
                                     self.enterChooseCog,
                                     self.exitChooseCog,
                                     ['AttackWait',
                                      'Attack']),
                         State.State('AttackWait',
                                     self.enterAttackWait,
                                     self.exitAttackWait,
                                     ['ChooseCog',
                                      'ChooseToon',
                                      'Attack']),
                         State.State('ChooseToon',
                                     self.enterChooseToon,
                                     self.exitChooseToon,
                                     ['AttackWait',
                                      'Attack']),
                         State.State('Run',
                                     self.enterRun,
                                     self.exitRun,
                                     ['Attack']),
                         State.State('SOS',
                                     self.enterSOS,
                                     self.exitSOS,
                                     ['Attack',
                                      'AttackWait',
                                      'SOSPetSearch',
                                      'SOSPetInfo']),
                         State.State('SOSPetSearch',
                                     self.enterSOSPetSearch,
                                     self.exitSOSPetSearch,
                                     ['SOS',
                                      'SOSPetInfo']),
                         State.State('SOSPetInfo',
                                     self.enterSOSPetInfo,
                                     self.exitSOSPetInfo,
                                     ['SOS',
                                      'AttackWait']),
                         State.State('Fire',
                                     self.enterFire,
                                     self.exitFire,
                                     ['Attack',
                                      'AttackWait',]),
                         ],
                        # Initial state
                        'Off',
                        # Final state
                        'Off',
                        )

        self.runPanel = TTDialog.TTDialog(
            dialogName = "TownBattleRunPanel",
            text = TTLocalizer.TownBattleRun,
            style = TTDialog.TwoChoice,
            command = self.__handleRunPanelDone,
            )
        self.runPanel.hide()

        self.attackPanelDoneEvent = 'attack-panel-done'
        self.attackPanel = TownBattleAttackPanel.TownBattleAttackPanel(
            self.attackPanelDoneEvent)

        self.waitPanelDoneEvent = 'wait-panel-done'
        self.waitPanel = TownBattleWaitPanel.TownBattleWaitPanel(
            self.waitPanelDoneEvent)

        self.chooseCogPanelDoneEvent = 'choose-cog-panel-done'
        self.chooseCogPanel = \
                            TownBattleChooseAvatarPanel.TownBattleChooseAvatarPanel(
            self.chooseCogPanelDoneEvent, 0)

        self.chooseToonPanelDoneEvent = 'choose-toon-panel-done'
        self.chooseToonPanel = \
                             TownBattleChooseAvatarPanel.TownBattleChooseAvatarPanel(
            self.chooseToonPanelDoneEvent, 1)

        self.SOSPanelDoneEvent = 'SOS-panel-done'
        self.SOSPanel = TownBattleSOSPanel.TownBattleSOSPanel(
            self.SOSPanelDoneEvent)

        self.SOSPetSearchPanelDoneEvent = 'SOSPetSearch-panel-done'
        self.SOSPetSearchPanel = TownBattleSOSPetSearchPanel.TownBattleSOSPetSearchPanel(self.SOSPetSearchPanelDoneEvent)

        self.SOSPetInfoPanelDoneEvent = 'SOSPetInfo-panel-done'
        self.SOSPetInfoPanel = TownBattleSOSPetInfoPanel.TownBattleSOSPetInfoPanel(self.SOSPetInfoPanelDoneEvent)
        
        
        
        self.fireCogPanelDoneEvent = 'fire-cog-panel-done'
        self.FireCogPanel = FireCogPanel.FireCogPanel(
            self.fireCogPanelDoneEvent)
            
        self.cogFireCosts = [None, None, None, None]
        
        
        

        # These are not StateDatas, so they have no doneEvents
        self.toonPanels = (TownBattleToonPanel.TownBattleToonPanel(0),
                           TownBattleToonPanel.TownBattleToonPanel(1),
                           TownBattleToonPanel.TownBattleToonPanel(2),
                           TownBattleToonPanel.TownBattleToonPanel(3))

        self.timer = ToontownTimer.ToontownTimer()
        self.timer.setPos(1.182, 0, 0.842)
        self.timer.setScale(0.4)
        self.timer.hide()
        return

    def cleanup(self):
        """ cleanup()
        """
        self.ignore(self.attackPanelDoneEvent)
        self.unload()
        del self.fsm
        self.runPanel.cleanup()
        del self.runPanel
        del self.attackPanel
        del self.waitPanel
        del self.chooseCogPanel
        del self.chooseToonPanel
        del self.SOSPanel
        del self.FireCogPanel
        del self.SOSPetSearchPanel
        del self.SOSPetInfoPanel
        for toonPanel in self.toonPanels:
            toonPanel.cleanup()
        del self.toonPanels
        self.timer.destroy()
        del self.timer
        del self.toons
        return

    def enter(self, event, parentFSMState, bldg=0, creditMultiplier=1,
              tutorialFlag=0):
        """ enter(event)
        """
        self.parentFSMState = parentFSMState
        self.parentFSMState.addChild(self.fsm)

        if (not self.isLoaded):
            self.load()
        print("Battle Event %s" % (event))
        self.battleEvent = event
        self.fsm.enterInitialState()
        base.localAvatar.laffMeter.start()
        self.numToons = 1
        self.numCogs = 1
        self.toons = [base.localAvatar.doId]
        self.toonPanels[0].setLaffMeter(base.localAvatar)
        self.bldg = bldg
        self.creditLevel = None
        self.creditMultiplier = creditMultiplier
        self.tutorialFlag = tutorialFlag
        base.localAvatar.inventory.setBattleCreditMultiplier(self.creditMultiplier)
        base.localAvatar.inventory.setActivateMode(
            'battle', heal=0, bldg=bldg, tutorialFlag=tutorialFlag)
        self.SOSPanel.bldg = bldg

    def exit(self):
        """ exit()
        """
        base.localAvatar.laffMeter.stop()
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        base.localAvatar.inventory.setBattleCreditMultiplier(1)

    def load(self):
        """ load()
        """
        if (self.isLoaded):
            return
        self.attackPanel.load()
        self.waitPanel.load()
        self.chooseCogPanel.load()
        self.chooseToonPanel.load()
        self.SOSPanel.load()
        self.SOSPetSearchPanel.load()
        self.SOSPetInfoPanel.load()
        self.isLoaded = 1

    def unload(self):
        """ unload()
        """
        if (not self.isLoaded):
            return
        self.attackPanel.unload()
        self.waitPanel.unload()
        self.chooseCogPanel.unload()
        self.chooseToonPanel.unload()
        self.FireCogPanel.unload()
        self.SOSPanel.unload()
        self.SOSPetSearchPanel.unload()
        self.SOSPetInfoPanel.unload()
        self.isLoaded = 0

    def setState(self, state):
        """ setState(state)
        """
        # The distributed battle does some set states after the
        # localtoon has left the battle and this fsm has been deleted
        if hasattr(self, 'fsm'):
            self.fsm.request(state)

    def updateTimer(self, time):
        """ updateTimer(time)
        """
        self.time = time
        self.timer.setTime(time)
        return None

    def __enterPanels(self, num, localNum):
        """ __enterPanels(num, localNum)
        """
        self.notify.debug('enterPanels() num: %d localNum: %d' % \
                          (num, localNum))
        # Hide all the toon panels, and position them low on the screen
        for toonPanel in self.toonPanels:
            toonPanel.hide()
            # toonPanel.setPos(0, 0, -0.58)
            toonPanel.setPos(0, 0, -0.9)

        if num == 1:
            self.toonPanels[0].setX(self.oddPos[1])
            self.toonPanels[0].show()
        elif num == 2:
            self.toonPanels[0].setX(self.evenPos[1])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.evenPos[2])
            self.toonPanels[1].show()
        elif num == 3:
            self.toonPanels[0].setX(self.oddPos[0])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.oddPos[1])
            self.toonPanels[1].show()
            self.toonPanels[2].setX(self.oddPos[2])
            self.toonPanels[2].show()
        elif num == 4:
            self.toonPanels[0].setX(self.evenPos[0])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.evenPos[1])
            self.toonPanels[1].show()
            self.toonPanels[2].setX(self.evenPos[2])
            self.toonPanels[2].show()
            self.toonPanels[3].setX(self.evenPos[3])
            self.toonPanels[3].show()
        else:
            self.notify.error("Bad number of toons: %s" % num)
        return None

    def updateChosenAttacks(self, battleIndices, tracks, levels, targets):
        """ updateChosenAttacks(tracks, levels, targets, toons)
        toonIndices: The battle indices for these parallel arrays
        tracks: An array of four tracks, one for each player
        levels: An array of four levels, one for each player
        targets: An array for four indices, either toon or suit, depending
        """
        self.notify.debug("updateChosenAttacks bi=%s tracks=%s levels=%s targets=%s"
                          % (battleIndices, tracks, levels, targets))
        for i in range(4):
            # Determine the number of possible targets for this attack,
            # and whether it is a group attack
            if battleIndices[i] == -1:
                pass
            else:
                if tracks[i] == BattleBase.NO_ATTACK:
                    numTargets = 0
                    target = -2
                elif tracks[i] == BattleBase.PASS_ATTACK:
                    numTargets = 0
                    target = -2
                elif (tracks[i] == BattleBase.SOS or
                      tracks[i] == BattleBase.NPCSOS or
                      tracks[i] == BattleBase.PETSOS):
                    numTargets = 0
                    target = -2
                elif tracks[i] == HEAL_TRACK:
                    # A heal
                    numTargets = self.numToons
                    if self.__isGroupHeal(levels[i]):
                        # -2 means group heal
                        target = -2
                    else:
                        target = targets[i]
                else:
                    # An attack
                    numTargets = self.numCogs
                    if self.__isGroupAttack(tracks[i], levels[i]):
                        # -1 means group attack
                        target = -1
                    else:
                        target = targets[i]
                        if target == -1:
                            # We haven't chosen a target yet.
                            numTargets = None
                    
                self.toonPanels[battleIndices[i]].setValues(battleIndices[i],
                      tracks[i], levels[i], numTargets, target, self.localNum)

        return None

    def chooseDefaultTarget(self):
        """ chooseDefaultTarget()
        """
        if (self.track > -1):
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.target
            messenger.send(self.battleEvent, [response])
            return 1
        return 0

    def updateLaffMeter(self, toonNum, hp):
        """ updateLaffMeter(toonNum, hp)
        """
        self.toonPanels[toonNum].updateLaffMeter(hp)

    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    def enterOff(self):
        if (self.isLoaded):
            # Hide the toon panels
            for toonPanel in self.toonPanels:
                toonPanel.hide()
        self.toonAttacks = [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0)]
        self.target = 0
        # Hide the timer
        if hasattr(self, "timer"):
            self.timer.hide()
        return None

    def exitOff(self):
        if (self.isLoaded):
            self.__enterPanels(self.numToons, self.localNum)
        # Show the timer
        self.timer.show()
        # Clear the attack values
        self.track = -1
        self.level = -1
        self.target = 0
        return None

    ##### Attack state #####

    def enterAttack(self):
        self.attackPanel.enter()
        self.accept(self.attackPanelDoneEvent, self.__handleAttackPanelDone)
        # Clear the attack choices for all four toon panels
        # TODO: do not reset all the panels - some Toons may have chosen their attack
        # and you are going back and choosing a new attack
        for toonPanel in self.toonPanels:
            toonPanel.setValues(0, BattleBase.NO_ATTACK)
        return None

    def exitAttack(self):
        self.ignore(self.attackPanelDoneEvent)
        self.attackPanel.exit()
        return None

    def __handleAttackPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        self.notify.debug('doneStatus: %s' % doneStatus)
        mode = doneStatus['mode']
        if (mode == 'Inventory'):
            self.track = doneStatus['track']
            self.level = doneStatus['level']

            # Update your own toon panel
            self.toonPanels[self.localNum].setValues(self.localNum, self.track, self.level)

            if (self.track == HEAL_TRACK):
                if self.__isGroupHeal(self.level):
                    # For group heals, no choice needs to be made, and no
                    # target is required.
                    response = {}
                    response['mode'] = 'Attack'
                    response['track'] = self.track
                    response['level'] = self.level
                    response['target'] = self.target
                    messenger.send(self.battleEvent, [response])
                    self.fsm.request('AttackWait')
                else:
                    # For single heals, we may ask the user for a choice.
                    if ((self.numToons == 3) or (self.numToons == 4)):
                        # If there are 3 or 4 toons, a choice must be made.
                        self.fsm.request('ChooseToon')
                    elif (self.numToons == 2):
                        # If there are only two toons, then the other toon
                        # is the default target
                        response = {}
                        response['mode'] = 'Attack'
                        response['track'] = self.track
                        response['level'] = self.level
                        # Figure out the index of the other guy
                        if self.localNum == 0:
                            response['target'] = 1
                        elif self.localNum == 1:
                            response['target'] = 0
                        else:
                            self.notify.error("Bad localNum value: %s" %
                                              self.localNum)
                        messenger.send(self.battleEvent, [response])
                        self.fsm.request('AttackWait')
                    else:
                        # You can't heal yourself, so only 2, 3, and 4 are valid
                        # values.
                        self.notify.error(
                            "Heal was chosen when number of toons is %s" %
                            self.numToons)
            else:
                # If it isn't heal, then it is an attack.
                if self.__isCogChoiceNecessary():
                    self.notify.debug("choice needed")
                    self.fsm.request('ChooseCog')

                    # Now we send an Attack message anyway, so other
                    # toons in the battle are notified of our choice
                    # of track, even before we choose a target.  The
                    # AI will know this doesn't count as a full choice
                    # yet.
                    response = {}
                    response['mode'] = 'Attack'
                    response['track'] = self.track
                    response['level'] = self.level
                    response['target'] = -1
                    messenger.send(self.battleEvent, [response])

                else:
                    self.notify.debug("no choice needed")
                    self.fsm.request('AttackWait')
                    response = {}
                    response['mode'] = 'Attack'
                    response['track'] = self.track
                    response['level'] = self.level
                    # If there is only one cog, then the target is cog 0
                    response['target'] = 0
                    messenger.send(self.battleEvent, [response])

        elif (mode == 'Run'):
            self.fsm.request('Run')
        elif (mode == 'SOS'):
            self.fsm.request('SOS')
        elif (mode == 'Fire'):
            self.fsm.request('Fire')
        elif (mode == 'Pass'):
            response = {}
            response['mode'] = 'Pass'
            response['id'] = -1
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        else:
            self.notify.warning('unknown mode: %s' % mode)

    ##### ChooseCog state #####

    def checkHealTrapLure(self):
        # Assume you can do all of these, then check each case

        self.notify.debug('numToons: %s, numCogs: %s, lured: %s, trapped: %s' %
                          (self.numToons, self.numCogs, self.luredIndices, self.trappedIndices))

        # If everybody is trapped or lured, you cannot trap
        if (len(PythonUtil.union(self.trappedIndices, self.luredIndices)) == self.numCogs):
            canTrap = 0
        else:
            canTrap = 1

        # If all cogs are lured, no trap or lure
        if (len(self.luredIndices) == self.numCogs):
            canLure = 0
            canTrap = 0
        else:
            canLure = 1

        # If there is only one toon in battle, he cannot heal
        if self.numToons == 1:
            canHeal = 0
        else:
            canHeal = 1

        return canHeal, canTrap, canLure

    def adjustCogsAndToons(self, cogs, luredIndices, trappedIndices, toons):
        numCogs = len(cogs)
        assert numCogs > 0

        self.notify.debug('adjustCogsAndToons() numCogs: %s self.numCogs: %s' %
                          (numCogs, self.numCogs))
        self.notify.debug('adjustCogsAndToons() luredIndices: %s self.luredIndices: %s' %
                          (luredIndices, self.luredIndices))
        self.notify.debug('adjustCogsAndToons() trappedIndices: %s self.trappedIndices: %s' %
                          (trappedIndices, self.trappedIndices))
        toonIds = map(lambda toon: toon.doId, toons)
        self.notify.debug('adjustCogsAndToons() toonIds: %s self.toons: %s' %
                          (toonIds, self.toons))

        # Determine the maximum level attack item we'll get credit
        # for, based on the suits in the battle.  This is the same as
        # the highest level suit we're currently facing.
        maxSuitLevel = 0
        cogFireCostIndex = 0
        for cog in cogs:
            maxSuitLevel = max(maxSuitLevel, cog.getActualLevel())
            self.cogFireCosts[cogFireCostIndex] = 1#cog.getActualLevel()
            cogFireCostIndex += 1
        creditLevel = maxSuitLevel

        # If nothing changed, we do not need to reactivate the gui
        if ((numCogs == self.numCogs) and
            (creditLevel == self.creditLevel) and
            (luredIndices == self.luredIndices) and
            (trappedIndices == self.trappedIndices) and
            (toonIds == self.toons)):
            resetActivateMode = 0
        else:
            resetActivateMode = 1

        self.notify.debug('adjustCogsAndToons() resetActivateMode: %s' %
                          (resetActivateMode))

        self.numCogs = numCogs
        self.creditLevel = creditLevel
        self.luredIndices = luredIndices
        self.trappedIndices = trappedIndices
        self.toons = toonIds
        self.numToons = len(toons)
        self.localNum = toons.index(base.localAvatar)
        currStateName = self.fsm.getCurrentState().getName()


        if resetActivateMode:
            self.__enterPanels(self.numToons, self.localNum)
            # New toons means an adjustment to the laff meters.
            for i in range(len(toons)):
                self.toonPanels[i].setLaffMeter(toons[i])

            # If we are picking a cog or a toon, those panels need to be adjusted
            if (currStateName == 'ChooseCog'):
                self.chooseCogPanel.adjustCogs(self.numCogs, self.luredIndices,
                                               self.trappedIndices, self.track)
            elif (currStateName == 'ChooseToon'):
                self.chooseToonPanel.adjustToons(self.numToons, self.localNum)

            canHeal, canTrap, canLure = self.checkHealTrapLure()
            base.localAvatar.inventory.setBattleCreditMultiplier(self.creditMultiplier)
            base.localAvatar.inventory.setActivateMode(
                'battle', heal=canHeal, trap=canTrap, lure=canLure,
                bldg=self.bldg, creditLevel=self.creditLevel,
                tutorialFlag=self.tutorialFlag)
        return

    def enterChooseCog(self):
        self.cog = 0
        self.chooseCogPanel.enter(self.numCogs,
                                  luredIndices = self.luredIndices,
                                  trappedIndices = self.trappedIndices,
                                  track = self.track)
        self.accept(self.chooseCogPanelDoneEvent,
                                self.__handleChooseCogPanelDone)
        return None

    def exitChooseCog(self):
        self.ignore(self.chooseCogPanelDoneEvent)
        self.chooseCogPanel.exit()
        return None

    def __handleChooseCogPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Back'):
            self.fsm.request('Attack')
        elif (mode == 'Avatar'):
            self.cog = doneStatus['avatar']
            self.target = self.cog
            self.fsm.request('AttackWait')
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.cog
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

    ##### AttackWait state #####

    def enterAttackWait(self, chosenToon=-1):
        self.accept(self.waitPanelDoneEvent, self.__handleAttackWaitBack)
        self.waitPanel.enter(self.numToons)

    def exitAttackWait(self):
        self.waitPanel.exit()
        self.ignore(self.waitPanelDoneEvent)

    def __handleAttackWaitBack(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Back'):
            if (self.track == HEAL_TRACK):
                # If a heal was chosen, go back to choose toon if there are
                # more than 2 toons, otherwise go to the attack panel.
                # Nope! That doesn't happen anymore. Now, if you have chosen
                # a heal, it always makes you go back to the attack panel. This
                # is the cowardly way of handling the situation where the selected
                # healee flees the battle.
                #if self.numToons > 2:
                #    self.fsm.request('ChooseToon')
                #else:
                self.fsm.request('Attack')
            elif (self.track == BattleBase.NO_ATTACK):
                # Must have come back from passing, show them the attack panel again
                self.fsm.request('Attack')
            else:
                # An attack was chosen. Go back to choose a cog or to choose
                # an attack, appropriately.
                if self.__isCogChoiceNecessary():
                    self.fsm.request('ChooseCog')
                else:
                    self.fsm.request('Attack')
            # Clear out whatever attack choice was sent to the server
            response = {}
            response['mode'] = 'UnAttack'
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.error('unknown mode: %s' % mode)

    ##### ChooseToon state #####

    def enterChooseToon(self):
        self.toon = 0
        self.chooseToonPanel.enter(self.numToons,
                                   localNum = self.localNum)
        self.accept(self.chooseToonPanelDoneEvent,
                                self.__handleChooseToonPanelDone)
        return None

    def exitChooseToon(self):
        self.ignore(self.chooseToonPanelDoneEvent)
        self.chooseToonPanel.exit()
        return None

    def __handleChooseToonPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Back'):
            self.fsm.request('Attack')
        elif (mode == 'Avatar'):
            self.toon = doneStatus['avatar']
            self.target = self.toon
            self.fsm.request('AttackWait', [self.toon])
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.toon
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

    ##### Run state #####

    def enterRun(self):
        self.runPanel.show()

    def exitRun(self):
        self.runPanel.hide()

    def __handleRunPanelDone(self, doneStatus):
        if (doneStatus == DGG.DIALOG_OK):
            response = {}
            response['mode'] = 'Run'
            messenger.send(self.battleEvent, [response])
        else:
            self.fsm.request('Attack')
            
            
    ##### Fire state #####

    def enterFire(self):
        canHeal, canTrap, canLure = self.checkHealTrapLure()
        #import pdb; pdb.set_trace()
        self.FireCogPanel.enter(self.numCogs,
                                  luredIndices = self.luredIndices,
                                  trappedIndices = self.trappedIndices,
                                  track = self.track, fireCosts = self.cogFireCosts)
        self.accept(self.fireCogPanelDoneEvent, self.__handleCogFireDone)
        return None

    def exitFire(self):
        self.ignore(self.fireCogPanelDoneEvent)
        self.FireCogPanel.exit()
        return None
        
        
    def __handleCogFireDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Back'):
            self.fsm.request('Attack')
        elif (mode == 'Avatar'):
            self.cog = doneStatus['avatar']
            self.target = self.cog
            self.fsm.request('AttackWait')
            response = {}
            response['mode'] = 'Fire'
            response['target'] = self.cog
            #import pdb; pdb.set_trace()
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

            

    ##### SOS state #####

    def enterSOS(self):
        canHeal, canTrap, canLure = self.checkHealTrapLure()
        self.SOSPanel.enter(canLure, canTrap)
        self.accept(self.SOSPanelDoneEvent, self.__handleSOSPanelDone)
        return None

    def exitSOS(self):
        self.ignore(self.SOSPanelDoneEvent)
        self.SOSPanel.exit()
        return None

    def __handleSOSPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Friend'):
            doId  = doneStatus['friend']
            # TODO: Something must be done with this handle... I think we are
            # supposed to use it for something...
            # self.fsm.request('SOSWait', [handle])
            response = {}
            response['mode'] = 'SOS'
            response['id'] = doId
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        elif (mode == 'Pet'):
            self.petId = doneStatus['petId']
            self.petName = doneStatus['petName']
            self.fsm.request('SOSPetSearch')
        elif (mode == 'NPCFriend'):
            doId  = doneStatus['friend']
            response = {}
            response['mode'] = 'NPCSOS'
            response['id'] = doId
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        elif (mode == 'Back'):
            self.fsm.request('Attack')

    ##### SOSPetSearch state #####

    def enterSOSPetSearch(self):
        response = {}
        response['mode'] = 'PETSOSINFO'
        response['id'] = self.petId
        self.SOSPetSearchPanel.enter(self.petId, self.petName)
        self.proxyGenerateMessage = 'petProxy-%d-generated' % self.petId
        self.accept(self.proxyGenerateMessage, self.__handleProxyGenerated)
        self.accept(self.SOSPetSearchPanelDoneEvent, self.__handleSOSPetSearchPanelDone)
        messenger.send(self.battleEvent, [response])
        return None

    def exitSOSPetSearch(self):
        self.ignore(self.proxyGenerateMessage)
        self.ignore(self.SOSPetSearchPanelDoneEvent)
        self.SOSPetSearchPanel.exit()
        return None

    def __handleSOSPetSearchPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'Back'):
            self.fsm.request('SOS')
        else:
            self.notify.error("invalid mode in handleSOSPetSearchPanelDone")

    def __handleProxyGenerated(self):
        self.fsm.request('SOSPetInfo')

    ##### SOSPetInfo state #####

    def enterSOSPetInfo(self):
        self.SOSPetInfoPanel.enter(self.petId)
        self.accept(self.SOSPetInfoPanelDoneEvent, self.__handleSOSPetInfoPanelDone)
        return None

    def exitSOSPetInfo(self):
        self.ignore(self.SOSPetInfoPanelDoneEvent)
        self.SOSPetInfoPanel.exit()
        return None

    def __handleSOSPetInfoPanelDone(self, doneStatus):
        assert doneStatus.has_key('mode')
        mode = doneStatus['mode']
        if (mode == 'OK'):
            response = {}
            response['mode'] = 'PETSOS'
            response['id'] = self.petId
            response['trickId'] = doneStatus['trickId']
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
            # We've requested that our pet do a trick. This is going to
            # change its mood in the DB, so flag our mood as 'dirty' so
            # that the pet panel will query the game server and not use
            # old cached mood data.
            bboard.post(PetConstants.OurPetsMoodChangedKey, True)
        elif (mode == 'Back'):
            self.fsm.request('SOS')

    def __isCogChoiceNecessary(self):
        # If there is more than one cog, and a non-group attack
        # has been selected, a cog choice needs to be made.
        if ((self.numCogs > 1) and (not self.__isGroupAttack(self.track,
                                                             self.level))):
            return 1
        else:
            return 0

    def __isGroupAttack(self, trackNum, levelNum):
        """
        Lets you know if the given attack is a group attack.
        """
        # Sanity checks
        assert isinstance(trackNum, types.IntType)
        assert isinstance(levelNum, types.IntType)
        assert((trackNum >= MIN_TRACK_INDEX) and (trackNum <= MAX_TRACK_INDEX) or
               (trackNum == BattleBase.NO_ATTACK) or
               (trackNum == BattleBase.SOS) or
               (trackNum == BattleBase.NPCSOS) or
               (trackNum == BattleBase.PETSOS) or
               (trackNum == BattleBase.FIRE))
        assert ((levelNum >= MIN_LEVEL_INDEX) and (levelNum <= MAX_LEVEL_INDEX) or
                (trackNum == BattleBase.FIRE) and (levelNum == -1))

        
        #RAU 2006/08/02 for uber gags, we consult BattleBase.AttackAffectsGroup
        
        # Sound attacks are group attacks
        #if trackNum == SOUND_TRACK:
        #    return 1
        # Odd numbered lure attacks are group attacks
        #elif ((trackNum == LURE_TRACK) and
        #      (levelNum % 2)):
        #    return 1
        #else:
        #    return 0

        retval = BattleBase.attackAffectsGroup(trackNum, levelNum)
        return retval
        
        

    def __isGroupHeal(self, levelNum):
        # Odd numbered heals are group heals JML- not any more
        #if levelNum % 2:
        #    return 1
        #else:
        #    return 0
        retval = BattleBase.attackAffectsGroup(HEAL_TRACK, levelNum)
        return retval

