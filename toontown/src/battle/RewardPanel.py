from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownBattleGlobals
import BattleBase
from direct.directnotify import DirectNotifyGlobal
import random
import string
from toontown.quest import Quests
import copy
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import NPCToons
import math
from toontown.coghq import CogDisguiseGlobals
from toontown.shtiker import DisguisePage
import Fanfare
from otp.otpbase import OTPGlobals

class RewardPanel(DirectFrame):
    """
    This panel shows experience gained during a battle
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('RewardPanel')

    def __init__(self, name):
        DirectFrame.__init__(self,
                             relief=None,
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = ToontownGlobals.GlobalDialogColor,
                             geom_scale = TTLocalizer.RPdirectFrame,
                             pos = (0, 0, 0.587),
                             )
        self.initialiseoptions(RewardPanel)

        self.avNameLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0, 0, 0.3),
            text = name,
            text_scale = 0.08,
            )

        self.gagExpFrame = DirectFrame(
            parent = self,
            relief = None,
            pos = (-0.32, 0, 0.24),
            )

        self.itemFrame = DirectFrame(
            parent = self,
            relief = None,
            text = TTLocalizer.RewardPanelItems,
            text_pos = (0, 0.2),
            text_scale = 0.08,
            )

        self.cogPartFrame = DirectFrame(
            parent = self,
            relief = None,
            text = TTLocalizer.RewardPanelCogPart,
            text_pos = (0, 0.2),
            text_scale = 0.08,
            )

        self.missedItemFrame = DirectFrame(
            parent = self,
            relief = None,
            text = TTLocalizer.RewardPanelMissedItems,
            text_pos = (0, 0.2),
            text_scale = 0.08,
            )
        
        self.itemLabel = DirectLabel(
            parent = self.itemFrame,
            text = "",
            text_scale = 0.06,
            )

        self.cogPartLabel = DirectLabel(
            parent = self.cogPartFrame,
            text = "",
            text_scale = 0.06,
            )

        self.missedItemLabel = DirectLabel(
            parent = self.missedItemFrame,
            text = "",
            text_scale = 0.06,
            )

        self.questFrame = DirectFrame(
            parent = self,
            relief = None,
            text = TTLocalizer.RewardPanelToonTasks,
            text_pos = (0, 0.2),
            text_scale = 0.06,
            )
            
        

        self.questLabelList = []
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            label = DirectLabel(
                parent = self.questFrame,
                relief = None,
                pos = (-0.85, 0, (-0.1*i)),                
                text = (TTLocalizer.RewardPanelQuestLabel % (i)),
                text_scale = 0.05,
                text_align = TextNode.ALeft,
                )
            label.hide()
            self.questLabelList.append(label)

        self.newGagFrame = DirectFrame(
            parent = self,
            relief = None,
            pos = (0, 0, 0.24),
            text = "",
            text_wordwrap = 14.4,
            text_pos = (0, -0.46),
            text_scale = 0.06,
            )
        
        self.endTrackFrame = DirectFrame(
            parent = self,
            relief = None,
            pos = (0,0,0.24),
            text = "",
            text_wordwrap = 14.4,
            text_pos = (0,-0.46),
            text_scale = 0.06,
            )
        
        self.congratsLeft = DirectLabel(
            parent = self.newGagFrame,
            pos = (-0.2, 0, -0.1),            
            text = "",
            text_pos = (0, 0),
            text_scale = 0.06,            
            )
        self.congratsLeft.setHpr(0, 0, -30)
        self.congratsRight = DirectLabel(
            parent = self.newGagFrame,
            pos = (0.2, 0, -0.1),            
            text = "",
            text_pos = (0, 0),
            text_scale = 0.06,
            )
        self.congratsRight.setHpr(0, 0, 30)

        self.promotionFrame = DirectFrame(
            parent = self,
            relief = None,
            pos = (0, 0, 0.24),
            text = "",
            text_wordwrap = 14.4,
            text_pos = (0, -0.46),
            text_scale = 0.06,
            )

        self.trackLabels = []
        self.trackIncLabels = []
        self.trackBars = []
        self.trackBarsOffset = 0

        self.meritLabels = []
        self.meritIncLabels = []
        self.meritBars = []
        
        # loop and make all the cog merit bars
        for i in range(len(SuitDNA.suitDepts)):
            deptName = TextEncoder.upper(SuitDNA.suitDeptFullnames[SuitDNA.suitDepts[i]])

            # dept label
            self.meritLabels.append(DirectLabel(
                parent = self.gagExpFrame,
                relief = None,
                text = deptName,
                text_scale = 0.05,
                text_align = TextNode.ARight,
                pos = (TTLocalizer.RPmeritLabelXPosition, 0, (-0.09*i) - 0.125),
                text_pos = (0, -0.02),
                ))

            # increment indicator labels
            self.meritIncLabels.append(DirectLabel(
                parent = self.gagExpFrame,
                relief = None,
                text = "",
                text_scale = 0.05,
                text_align = TextNode.ALeft,
                pos = (0.7, 0, (-0.09*i) - 0.125),
                text_pos = (0, -0.02),
                ))

            # merit progress bar
            self.meritBars.append(DirectWaitBar(
                parent = self.gagExpFrame,
                relief = DGG.SUNKEN,
                frameSize = (-1, 1, -0.15, 0.15),
                borderWidth = (0.02, 0.02),
                scale = 0.25,
                frameColor = (DisguisePage.DeptColors[i][0]*0.7,
                              DisguisePage.DeptColors[i][1]*0.7,
                              DisguisePage.DeptColors[i][2]*0.7,
                              1),
                barColor = (DisguisePage.DeptColors[i][0],
                            DisguisePage.DeptColors[i][1],
                            DisguisePage.DeptColors[i][2],
                            1),
                text = "0/0 " + TTLocalizer.RewardPanelMeritBarLabels[i],
                text_scale = TTLocalizer.RPmeritBarLabels,
                text_fg = (0, 0, 0, 1),
                text_align = TextNode.ALeft,
                text_pos = (-0.96, -0.05),
                pos = (TTLocalizer.RPmeritBarsXPosition, 0, (-0.09*i) - 0.125),
                ))

        # loop and make all the track exp bars
        for i in range(len(ToontownBattleGlobals.Tracks)):
            trackName = TextEncoder.upper(ToontownBattleGlobals.Tracks[i])

            # Name of track label
            self.trackLabels.append(DirectLabel(
                parent = self.gagExpFrame,
                relief = None,
                text = trackName,
                text_scale = TTLocalizer.RPtrackLabels,
                text_align = TextNode.ARight,
                pos = (0.13, 0, -0.09*i),
                text_pos = (0, -0.02),
                ))

            # increment indicator labels
            self.trackIncLabels.append(DirectLabel(
                parent = self.gagExpFrame,
                relief = None,
                text = "",
                text_scale = 0.05,
                text_align = TextNode.ALeft,
                pos = (0.65, 0, -0.09*i),
                text_pos = (0, -0.02),
                ))

            # track exp bar
            self.trackBars.append(DirectWaitBar(
                parent = self.gagExpFrame,
                relief = DGG.SUNKEN,
                frameSize = (-1, 1, -0.15, 0.15),
                borderWidth = (0.02, 0.02),
                scale = 0.25,
                frameColor = (ToontownBattleGlobals.TrackColors[i][0]*0.7,
                              ToontownBattleGlobals.TrackColors[i][1]*0.7,
                              ToontownBattleGlobals.TrackColors[i][2]*0.7,
                              1),
                barColor = (ToontownBattleGlobals.TrackColors[i][0],
                            ToontownBattleGlobals.TrackColors[i][1],
                            ToontownBattleGlobals.TrackColors[i][2],
                            1),
                text = "0/0",
                text_scale = 0.18,
                text_fg = (0, 0, 0, 1),
                text_align = TextNode.ACenter,
                text_pos = (0, -0.05),
                pos = (0.40, 0, -0.09*i),
                ))

        return

    # Elemental operations:
    # Set track(title, curSkill, next):
    #   - Set track title
    #   - clear gags
    #   - set skill
    #   - set next
    #   - set background color

    # Add gag(gagType, i, n)
    #   - Position gag at i/n
    #   - Increment skill
    #   - play sound fx

    # Play track sequence(track, curSkill, next, gagTypeList)
    #   - Set track
    #   - for i = 1 to n, add gag (with delays between)

    # Play reward sequence(tracks, skills, nexts, gagTypeLists)
    #   - for i = 1 to n, play track sequences (with delays between)

    # Play reward sequences(sequences)
    #   - for i = 1 to n, play reward sequences

    #def clearGags(self):
    #    for gag in self.gagList:
    #        gag.removeNode()
    #    self.gagList = []
    #    return None

    def getNextExpValue(self, curSkill, trackIndex):
        """
        Return the number of total experience to get to the next
        track. If the current experience equals or exceeds the highest
        next value, the highest next value is returned.
        """
        # The last value is the default
        retVal = ToontownBattleGlobals.UberSkill
        for amount in ToontownBattleGlobals.Levels[trackIndex]:
            if curSkill < amount:
                retVal = amount
                return retVal
        return retVal
        
    def getNextExpValueUber(self, curSkill, trackIndex):
        """
        Return the number of total experience to get to the next
        track. If the current experience equals or exceeds the highest
        next value, the highest next value is returned.
        """
        # The last value is the default
        return ToontownBattleGlobals.UberSkill

    def getNextMeritValue(self, curMerits, toon, dept):
        """
        Return the number of total merits to get to the next
        cog level. If the current merits equals or exceeds the highest
        next value, the highest next value is returned.
        """
        totalMerits = CogDisguiseGlobals.getTotalMerits(toon, dept)
        # The last value is the default
        retVal = totalMerits
        if curMerits > totalMerits:
                retVal = amount
        return retVal

    def initItemFrame(self, toon):
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.hide()
        self.questFrame.hide()
        self.itemFrame.show()
        self.cogPartFrame.hide()
        self.missedItemFrame.hide()

    def initMissedItemFrame(self, toon):
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.hide()
        self.questFrame.hide()
        self.itemFrame.hide()
        self.cogPartFrame.hide()
        self.missedItemFrame.show()

    def initCogPartFrame(self, toon):
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.hide()
        self.questFrame.hide()
        self.itemFrame.hide()
        self.cogPartFrame.show()
        self.cogPartLabel['text'] = ''
        self.missedItemFrame.hide()

    def initQuestFrame(self, toon, avQuests):
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.hide()        
        self.questFrame.show()
        self.itemFrame.hide()
        self.cogPartFrame.hide()
        self.missedItemFrame.hide()

        # First hide all quest labels in case we do not fill
        # them in with our own quests (and reset the color to black)
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            questLabel = self.questLabelList[i]
            questLabel['text_fg'] = (0, 0, 0, 1)
            questLabel.hide()

        for i in range(len(avQuests)):
            questDesc = avQuests[i]
            questId, npcId, toNpcId, rewardId, toonProgress = questDesc
            quest = Quests.getQuest(questId)
            if quest:
                questString = quest.getString()
                progressString = quest.getProgressString(toon, questDesc)
                rewardString = quest.getRewardString(progressString)
                rewardString = Quests.fillInQuestNames(rewardString, toNpcId = toNpcId)
                completed = (quest.getCompletionStatus(toon, questDesc) == Quests.COMPLETE)
                questLabel = self.questLabelList[i]
                questLabel.show()

                # the reward movie looks wonky in the tutorial...
                if base.localAvatar.tutorialAck:
                    questLabel['text'] = rewardString
                    if completed:
                        questLabel['text_fg'] = (0, 0.3, 0, 1)
                else:
                    questLabel['text'] = questString + " :"

    def initGagFrame(self, toon, expList, meritList):
        self.avNameLabel['text'] = toon.getName()
        self.endTrackFrame.hide()
        self.gagExpFrame.show()
        self.newGagFrame.hide()
        self.promotionFrame.hide()
        self.questFrame.hide()
        self.itemFrame.hide()
        self.cogPartFrame.hide()
        self.missedItemFrame.hide()

        trackBarOffset = 0
        
        # Initialize the cog merit bars if enabled
        for i in range(len(SuitDNA.suitDepts)):
            meritBar = self.meritBars[i]
            meritLabel = self.meritLabels[i]
            totalMerits = CogDisguiseGlobals.getTotalMerits(toon, i)
            merits = meritList[i]
            self.meritIncLabels[i].hide()
            # if we are have a full suit then we are working on promotions
            if CogDisguiseGlobals.isSuitComplete(toon.cogParts, i):
                # if we don't show the merit bar, we must shift the skill bars left
                if not self.trackBarsOffset:
                    trackBarOffset = 0.47
                    # only do this once! :)
                    self.trackBarsOffset = 1
                meritBar.show()
                meritLabel.show()                
                meritLabel.show()
                if totalMerits:
                    meritBar["range"] = totalMerits
                    meritBar["value"] = merits
                    if merits == totalMerits:
                        meritBar["text"] = TTLocalizer.RewardPanelMeritAlert
                    else:
                        meritBar["text"] = ("%s/%s %s" % (merits,
                                                          totalMerits,
                                                          TTLocalizer.RewardPanelMeritBarLabels[i],))                    
                else:
                    # if total merits = None, this dept is maxed out
                    meritBar["range"] = 1
                    meritBar["value"] = 1
                    meritBar["text"] = TTLocalizer.RewardPanelMeritsMaxed
                self.resetMeritBarColor(i)
            else:
                meritBar.hide()                
                meritLabel.hide()

        # Initialize all the bars with the current and next exp
        for i in range(len(expList)):
            curExp = expList[i]
            trackBar = self.trackBars[i]
            trackLabel = self.trackLabels[i]            
            trackIncLabel = self.trackIncLabels[i]
            trackBar.setX(trackBar.getX() - trackBarOffset)
            trackLabel.setX(trackLabel.getX() - trackBarOffset)
            trackIncLabel.setX(trackIncLabel.getX() - trackBarOffset)
            trackIncLabel.hide()
            if toon.hasTrackAccess(i):
                trackBar.show()
                
                if curExp >= ToontownBattleGlobals.UnpaidMaxSkill and toon.getGameAccess() != OTPGlobals.AccessFull:
                    nextExp = self.getNextExpValue(curExp, i)
                    trackBar["range"] = nextExp
                    trackBar["value"] = ToontownBattleGlobals.UnpaidMaxSkill
                    trackBar["text"] = (TTLocalizer.InventoryGuestExp)
                
                elif curExp >= ToontownBattleGlobals.regMaxSkill:
                    nextExp = self.getNextExpValueUber(curExp, i)
                    trackBar["range"] = nextExp
                    uberCurrExp = curExp - ToontownBattleGlobals.regMaxSkill
                    trackBar["value"] = uberCurrExp
                    trackBar["text"] = (TTLocalizer.InventoryUberTrackExp %
                                                  {"nextExp": ToontownBattleGlobals.MaxSkill - curExp,})
                else:
                    nextExp = self.getNextExpValue(curExp, i)
                    trackBar["range"] = nextExp
                    trackBar["value"] = curExp
                    trackBar["text"] = ("%s/%s" % (curExp, nextExp))
                self.resetBarColor(i)
            else:
                trackBar.hide()

                
        return

    def incrementExp(self, track, newValue, toon):
        trackBar = self.trackBars[track]
        oldValue = trackBar["value"]
        newValue = min(ToontownBattleGlobals.MaxSkill, newValue)
        nextExp = self.getNextExpValue(newValue, track)
        
        if newValue >= ToontownBattleGlobals.UnpaidMaxSkill and toon.getGameAccess() != OTPGlobals.AccessFull:
            newValue = oldValue
            trackBar["text"] = (TTLocalizer.InventoryGuestExp)
        
        elif newValue >= ToontownBattleGlobals.regMaxSkill:
            newValue = newValue - ToontownBattleGlobals.regMaxSkill
            nextExp = self.getNextExpValueUber(newValue, track)
            trackBar["text"] = (TTLocalizer.InventoryUberTrackExp %
                                            {"nextExp": ToontownBattleGlobals.UberSkill - newValue,})
        else:
            trackBar["text"] = ("%s/%s" % (newValue, nextExp))  
        trackBar["range"] = nextExp
        trackBar["value"] = newValue
        trackBar["barColor"] = (ToontownBattleGlobals.TrackColors[track][0],
                                ToontownBattleGlobals.TrackColors[track][1],
                                ToontownBattleGlobals.TrackColors[track][2],
                                1)
        return

    def resetBarColor(self, track):
        self.trackBars[track]["barColor"] = (ToontownBattleGlobals.TrackColors[track][0]*0.8,
                                             ToontownBattleGlobals.TrackColors[track][1]*0.8,
                                             ToontownBattleGlobals.TrackColors[track][2]*0.8,
                                             1)


    def incrementMerits(self, toon, dept, newValue, totalMerits):
        meritBar = self.meritBars[dept]
        oldValue = meritBar["value"]
        # don't bother to inc if toon is maxed already
        if totalMerits:
            newValue = min(totalMerits, newValue)
            meritBar["range"] = totalMerits
            meritBar["value"] = newValue
            if newValue == totalMerits:
                meritBar["text"] = TTLocalizer.RewardPanelMeritAlert
                meritBar["barColor"] = (DisguisePage.DeptColors[dept][0],
                                        DisguisePage.DeptColors[dept][1],
                                        DisguisePage.DeptColors[dept][2],
                                        1)
            else:
                meritBar["text"] = ("%s/%s %s" % (newValue,
                                                  totalMerits,
                                                  TTLocalizer.RewardPanelMeritBarLabels[dept],))                    
        return


    def resetMeritBarColor(self, dept):
        self.meritBars[dept]["barColor"] = (DisguisePage.DeptColors[dept][0]*0.8,
                                            DisguisePage.DeptColors[dept][1]*0.8,
                                            DisguisePage.DeptColors[dept][2]*0.8,
                                            1)


    def getRandomCongratsPair(self, toon):
        congratsStrings = TTLocalizer.RewardPanelCongratsStrings

        numStrings = len(congratsStrings)
        assert(numStrings >= 2)
                           
        indexList = range(numStrings)

        index1 = random.choice(indexList)
        indexList.remove(index1)
        index2 = random.choice(indexList)

        string1 = congratsStrings[index1]
        string2 = congratsStrings[index2]

        return(string1, string2)
        
    def uberGagInterval(self, toon, track, level):
        #import pdb; pdb.set_trace()
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.show()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
        
        self.newGagFrame['text'] = (TTLocalizer.RewardPanelUberGag %
                                    {"gagName": ToontownBattleGlobals.Tracks[track].capitalize(),
                                     "exp": str(ToontownBattleGlobals.UberSkill),
                                     "avName":  toon.getName(),})
        self.congratsLeft['text'] = ("")
        self.congratsRight['text'] = ("")

        #self.gagText.setText(AvPropStrings[track][level])

        # copy a gag
        gagOriginal = base.localAvatar.inventory.buttonLookup(track, level)
        self.newGagIcon = gagOriginal.copyTo(self.newGagFrame)
        # Set position... x is x, z is y
        self.newGagIcon.setPos(0, 0, -0.25)
        # Set scale (big)
        self.newGagIcon.setScale(1.5)
        
        return

    def newGag(self, toon, track, level):
        #import pdb; pdb.set_trace()
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.show()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
        
        self.newGagFrame['text'] = (TTLocalizer.RewardPanelNewGag %
                                    {"gagName": ToontownBattleGlobals.Tracks[track].capitalize(),
                                     "avName":  toon.getName(),})
        self.congratsLeft['text'] = ("")
        self.congratsRight['text'] = ("")

        #self.gagText.setText(AvPropStrings[track][level])

        # copy a gag
        gagOriginal = base.localAvatar.inventory.buttonLookup(track, level)
        self.newGagIcon = gagOriginal.copyTo(self.newGagFrame)
        # Set position... x is x, z is y
        self.newGagIcon.setPos(0, 0, -0.25)
        # Set scale (big)
        self.newGagIcon.setScale(1.5)
        
        return

    def cleanupNewGag(self):
        self.endTrackFrame.hide()
        if self.newGagIcon:
            self.newGagIcon.removeNode()
            self.newGagIcon = None
        self.gagExpFrame.show()
        self.newGagFrame.hide()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
    
    def getNewGagIntervalList(self, toon, track, level):
        leftCongratsAnticipate = 1.0
        rightCongratsAnticipate = 1.0
        finalDelay = 1.5
        (leftString, rightString) = self.getRandomCongratsPair(toon)
        intervalList = [Func(self.newGag, toon, track, level),
                        Wait(leftCongratsAnticipate),
                        Func(self.congratsLeft.setProp, 'text', leftString),
                        Wait(rightCongratsAnticipate),
                        Func(self.congratsRight.setProp, 'text', rightString),
                        Wait(finalDelay),
                        Func(self.cleanupNewGag),
                        ]
        return intervalList
        
    def getUberGagIntervalList(self, toon, track, level):
        leftCongratsAnticipate = 1.0
        rightCongratsAnticipate = 1.0
        finalDelay = 1.5
        (leftString, rightString) = self.getRandomCongratsPair(toon)
        intervalList = [Func(self.uberGagInterval, toon, track, level),
                        Wait(leftCongratsAnticipate),
                        Func(self.congratsLeft.setProp, 'text', leftString),
                        Wait(rightCongratsAnticipate),
                        Func(self.congratsRight.setProp, 'text', rightString),
                        Wait(finalDelay),
                        Func(self.cleanupNewGag),
                        ]
        return intervalList
    
    # hides everything, used for the endtrack to make sure everything vanishes
    # so we can see the fanfare
    def vanishFrames(self):
        self.hide()
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
        self.cogPartFrame.hide()
        self.missedItemFrame.hide()
        
    def endTrack(self, toon, toonList, track):
        #import pdb; pdb.set_trace()1
        # we make the RewardPanel show up again for all toons in combat
        for t in toonList:
            if t == base.localAvatar:
                self.show()
        self.endTrackFrame.show()
        
        self.endTrackFrame['text'] = (TTLocalizer.RewardPanelEndTrack %
                                      {"gagName": ToontownBattleGlobals.Tracks[track].capitalize(),
                                       "avName": toon.getName(),})
        gagLast = base.localAvatar.inventory.buttonLookup(track, ToontownBattleGlobals.UBER_GAG_LEVEL_INDEX)
        self.gagIcon = gagLast.copyTo(self.endTrackFrame)
        self.gagIcon.setPos(0,0,-0.25)
        self.gagIcon.setScale(1.5)
        
        return
    
    # clears the icon on the endTrackFrame, just in case they happen
    # to get to the end of two tracks in one battle
    def cleanIcon(self):
        self.gagIcon.removeNode()
        self.gagIcon = None
        
    # causes all other parts to show up again
    def cleanupEndTrack(self):
        self.endTrackFrame.hide()
        self.gagExpFrame.show()
        self.newGagFrame.hide()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
    
    # shows a message frame telling the toon that they've reached the end
    # of one of the gag tracks.  Shows up after the fanfare
    def getEndTrackIntervalList(self, toon, toonList, track):
        intervalList = [Func(self.endTrack, toon, toonList, track),
                        Wait(2.0),
                        Func(self.cleanIcon),
                        ]
        return intervalList

    def showTrackIncLabel(self, track, earnedSkill, guestWaste = 0):
        if guestWaste:
            self.trackIncLabels[track]["text"] = " " + str(earnedSkill) + TTLocalizer.GuestLostExp
        elif earnedSkill > 0:
            self.trackIncLabels[track]["text"] = "+ " + str(earnedSkill)
        elif earnedSkill < 0:
            self.trackIncLabels[track]["text"] = " " + str(earnedSkill)
        self.trackIncLabels[track].show()


    def showMeritIncLabel(self, dept, earnedMerits):
        self.meritIncLabels[dept]["text"] = "+ " + str(earnedMerits)
        self.meritIncLabels[dept].show()

        
    def getTrackIntervalList(self, toon, track, origSkill, earnedSkill, hasUber, guestWaste = 0):
        """
        returns a list of intervals that, if played, will show experience
        gained for the given track.
        """
        
        #check for corruptUberList
        #import pdb; pdb.set_trace()
        if hasUber < 0:
            print(toon.doId, 'Reward Panel received an invalid hasUber from an uberList')
        
        tickDelay = 0.16
        intervalList = []
        if (origSkill + earnedSkill) >= ToontownBattleGlobals.UnpaidMaxSkill and toon.getGameAccess() != OTPGlobals.AccessFull:
            lostExp = (origSkill + earnedSkill) - ToontownBattleGlobals.UnpaidMaxSkill
            intervalList.append(Func(self.showTrackIncLabel, track, lostExp, 1))
        else:
            intervalList.append(Func(self.showTrackIncLabel, track, earnedSkill))

        # How much time should it take to increment the bar?  It
        # should take more time for a larger boost, but not linearly
        # more--the larger the boost, the faster the bar moves to get
        # there.  The total time will be logarithmic with the number
        # of points earned.  It should be small (actually, tickDelay)
        # for a one-point boost, and maybe four or five seconds for
        # 100 points.  Conveniently, this is the ratio that natural
        # log gives us.
        barTime = math.log(earnedSkill + 1)
        numTicks = int(math.ceil(barTime / tickDelay))

        for i in range(numTicks):
            t = (i + 1) / float(numTicks)
            newValue = int(origSkill + t * earnedSkill + 0.5)
            intervalList.append(Func(self.incrementExp, track, newValue, toon))
            intervalList.append(Wait(tickDelay))

        intervalList.append(Func(self.resetBarColor, track))
        intervalList.append(Wait(0.4))

        # Insert "new gag" panel here, if needed.
        nextExpValue = self.getNextExpValue(origSkill, track)
        finalGagFlag = 0
        while ((origSkill + earnedSkill >= nextExpValue) and
               (origSkill < nextExpValue) and
               (not finalGagFlag)):
            # Add the new gag interval... Look up the new gag level based on
            # the nextExpValue
            if newValue >= ToontownBattleGlobals.UnpaidMaxSkill and toon.getGameAccess() != OTPGlobals.AccessFull:
                pass
            elif nextExpValue != ToontownBattleGlobals.MaxSkill:
                intervalList += self.getNewGagIntervalList(
                    toon, track, ToontownBattleGlobals.Levels[track].index(nextExpValue))
            # Get the next value
            newNextExpValue = self.getNextExpValue(nextExpValue, track)
            # If the next value is the old one, we hit the top, and
            # have nothing more to add. Otherwise, set the nextExpValue,
            # and loop around again to see if we have another new gag
            # to show...
            if newNextExpValue == nextExpValue:
                finalGagFlag = 1
            else:
                nextExpValue = newNextExpValue
                
        #test for Uber gag
        uberIndex = ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1
        #hasUber = toon.inventory.numItem(track, uberIndex)
        
        currentSkill = origSkill + earnedSkill
        uberSkill = ToontownBattleGlobals.UberSkill + ToontownBattleGlobals.Levels[track][ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1]
        #print("Track %s hasUber %s current %s req %s" % (track, hasUber, currentSkill, uberSkill))
        if (currentSkill >= uberSkill) and not (hasUber > 0):
            #print("adding Uber track")
            intervalList += self.getUberGagIntervalList(
               toon, track, (ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1))
            intervalList.append(Wait(0.4))
            skillDiff = currentSkill - ToontownBattleGlobals.Levels[track][ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1]
            
            barTime = math.log(skillDiff + 1)
            numTicks = int(math.ceil(barTime / tickDelay))
            
            displayedSkillDiff = skillDiff
            if displayedSkillDiff > ToontownBattleGlobals.UberSkill:
                displayedSkillDiff = ToontownBattleGlobals.UberSkill
            
            intervalList.append(Func(self.showTrackIncLabel, track, -displayedSkillDiff))

            for i in range(numTicks):
                t = (i + 1) / float(numTicks)
                newValue = int(currentSkill - t * skillDiff + 0.5)
                intervalList.append(Func(self.incrementExp, track, newValue, toon))
                intervalList.append(Wait(tickDelay * 0.5))
            intervalList.append(Wait(0.4))
                
        return intervalList
            
    def getMeritIntervalList(self, toon, dept, origMerits, earnedMerits):
        """
        returns a list of intervals that, if played, will show merits
        gained for the given dept.
        """
        tickDelay = 0.08
        intervalList = []
        totalMerits = CogDisguiseGlobals.getTotalMerits(toon, dept)
        neededMerits = 0
        
        # Only show the inc value if we are not maxed
        if totalMerits and (origMerits != totalMerits):
            neededMerits = totalMerits - origMerits
            intervalList.append(Func(self.showMeritIncLabel, dept, min(neededMerits, earnedMerits)))

        # How much time should it take to increment the bar?
        barTime = math.log(earnedMerits + 1)
        numTicks = int(math.ceil(barTime / tickDelay))

        for i in range(numTicks):
            t = (i + 1) / float(numTicks)
            newValue = int(origMerits + t * earnedMerits + 0.5)
            intervalList.append(Func(self.incrementMerits, toon, dept, newValue, totalMerits))
            intervalList.append(Wait(tickDelay))

        intervalList.append(Func(self.resetMeritBarColor, dept))
        intervalList.append(Wait(0.4))

        # we don't need a promotion if we've reach level 50
        if (toon.cogLevels[dept] < ToontownGlobals.MaxCogSuitLevel):
            if neededMerits and toon.readyForPromotion(dept):
                intervalList.append(Wait(0.4))            
                intervalList += self.getPromotionIntervalList(toon, dept)

        return intervalList

    def promotion(self, toon, dept):
        self.endTrackFrame.hide()
        self.gagExpFrame.hide()
        self.newGagFrame.hide()
        self.promotionFrame.show()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()
        name = SuitDNA.suitDepts[dept]
        self.promotionFrame['text'] = (TTLocalizer.RewardPanelPromotion % (SuitDNA.suitDeptFullnames[name]))

        # copy a gag
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        if dept == 0:
            self.deptIcon = icons.find('**/CorpIcon').copyTo(self.promotionFrame)
        elif dept == 1:
            self.deptIcon = icons.find('**/LegalIcon').copyTo(self.promotionFrame)
        elif dept == 2:
            self.deptIcon = icons.find('**/MoneyIcon').copyTo(self.promotionFrame)
        elif dept == 3:
            self.deptIcon = icons.find('**/SalesIcon').copyTo(self.promotionFrame)
        icons.removeNode()
        # Set position... x is x, z is y
        self.deptIcon.setPos(0, 0, -0.225)
        # Set scale (big)
        self.deptIcon.setScale(0.33)
        return
    
    def cleanupPromotion(self):
        # protect against multiple cleanups
        if not hasattr(self, 'deptIcon'):
            return
        self.deptIcon.removeNode()
        self.deptIcon = None
        self.endTrackFrame.hide()
        self.gagExpFrame.show()
        self.newGagFrame.hide()
        self.promotionFrame.hide()        
        self.questFrame.hide()
        self.itemFrame.hide()
        self.missedItemFrame.hide()

    def getPromotionIntervalList(self, toon, dept):
        finalDelay = 2.0
        intervalList = [Func(self.promotion, toon, dept),
                        Wait(finalDelay),
                        Func(self.cleanupPromotion),
                        ]
        return intervalList
    
    def getQuestIntervalList(self, toon, deathList, toonList, origQuestsList, itemList, helpfulToonsList = []):
        # This is the battle notifying us that a toon killed some cogs
        # See if this toon has a quest on these cogs. If so, update the
        # progress.
        # Note that toonList corresponds order-wise to the bitmasks in the
        # deathList, and might have 'None' entries for toons that are no
        # longer present.

        avId = toon.getDoId()
        tickDelay = 0.2
        intervalList = []

        # create a non-ordered list of the toons (without the None entries)
        toonShortList = []
        for t in toonList:
            if t is not None:
                toonShortList.append(t)

        cogList = []
        for i in range(0, len(deathList), 4):
            cogIndex = deathList[i]
            cogLevel = deathList[i+1]
            activeToonBits = deathList[i+2]
            flags = deathList[i+3]
            activeToonIds = []
            for j in range(8):
                if activeToonBits & (1 << j):
                    if toonList[j] is not None:
                        activeToonIds.append(toonList[j].getDoId())
            isSkelecog = flags & ToontownBattleGlobals.DLF_SKELECOG
            isForeman = flags & ToontownBattleGlobals.DLF_FOREMAN
            isVP = flags & ToontownBattleGlobals.DLF_VP
            isCFO = flags & ToontownBattleGlobals.DLF_CFO
            isSupervisor = flags & ToontownBattleGlobals.DLF_SUPERVISOR
            isVirtual = flags & ToontownBattleGlobals.DLF_VIRTUAL
            hasRevives = flags & ToontownBattleGlobals.DLF_REVIVES
            if isVP or isCFO:
                cogType = None
                cogTrack = SuitDNA.suitDepts[cogIndex]
            else:
                cogType = SuitDNA.suitHeadTypes[cogIndex]
                cogTrack = SuitDNA.getSuitDept(cogType)
            cogList.append({'type': cogType,
                            'level': cogLevel,
                            'track': cogTrack,
                            'isSkelecog': isSkelecog,
                            'isForeman': isForeman,
                            'isVP': isVP,
                            'isCFO': isCFO,
                            'isSupervisor': isSupervisor,
                            'isVirtual': isVirtual,
                            'hasRevives': hasRevives,
                            'activeToons': activeToonIds,
                            })

        # It would be nice if there were some more elegant way to get the zoneId.
        try:
            zoneId = base.cr.playGame.getPlace().getTaskZoneId()
        except:
            # Maybe the local toon is just teleporting in, and we
            # haven't got a place yet.  This is a band-aid; we should
            # revisit this later.
            zoneId = 0

        
        # We could not trust the toons quests not to be updated by the AI, so now we pass in original
        # quests, just like we do original experience
        # unflatten orig quest list
        avQuests = []
        for i in range(0, len(origQuestsList), 5):
            avQuests.append(origQuestsList[i:i+5])

        # Now append intervals that will show our quests
        for i in range(len(avQuests)):
            questDesc = avQuests[i]
            questId, npcId, toNpcId, rewardId, toonProgress = questDesc
            quest = Quests.getQuest(questId)
            if quest:
                questString = quest.getString()
                progressString = quest.getProgressString(toon, questDesc)
                questLabel = self.questLabelList[i]
                earned = 0
                orig = questDesc[4] & (pow(2,16) - 1)
		num = 0

                # Did we recovered items?
                if quest.getType() == Quests.RecoverItemQuest:
                    questItem = quest.getItem()
                    if questItem in itemList:
                        earned = itemList.count(questItem)

                # Then we just defeated cogs
                else:
                    for cogDict in cogList:
                        if cogDict['isVP']:
                            num = quest.doesVPCount(avId, cogDict,
                                                    zoneId, toonShortList)
                        elif cogDict['isCFO']:
                            num = quest.doesCFOCount(avId, cogDict,
                                                     zoneId, toonShortList)
                        else:
                            num = quest.doesCogCount(avId, cogDict,
                                                     zoneId, toonShortList)
                        if num:
                            if base.config.GetBool('battle-passing-no-credit', True):
                                if avId in helpfulToonsList:
                                    earned += num
                                else:
                                    self.notify.debug('avId=%d not getting %d kill cog quest credit' % (avId,num))
                            else:
                                earned += num
                                
                # import pdb; pdb.set_trace()
                
                # if we are not in the tutorial
                if base.localAvatar.tutorialAck:
                    # make sure we still need some items before playing movie
                    if earned > 0:
                        earned = min(earned, quest.getNumQuestItems() - questDesc[4])

                if earned > 0 or (base.localAvatar.tutorialAck==0 and num==1):
                    # See getTrackIntervalList() for timing comments.
                    barTime = math.log(earned + 1)
                    numTicks = int(math.ceil(barTime / tickDelay))

                    for i in range(numTicks):
                        t = (i + 1) / float(numTicks)
                        newValue = int(orig + t * earned + 0.5)

                        # Add num to progress
                        questDesc[4] = newValue
                        progressString = quest.getProgressString(toon, questDesc)
                        str = ("%s : %s" % (questString, progressString))
                        if (quest.getCompletionStatus(toon, questDesc) == Quests.COMPLETE):
                            intervalList.append(Func(questLabel.setProp, 'text_fg', (0, 0.3, 0, 1)))
                        intervalList.append(Func(questLabel.setProp, 'text', str))
                        intervalList.append(Wait(tickDelay))                    
                
        return intervalList


    def getItemIntervalList(self, toon, itemList):
        intervalList = []
        for itemId in itemList:
            itemName = Quests.getItemName(itemId)
            intervalList.append(Func(self.itemLabel.setProp, 'text', itemName))
            intervalList.append(Wait(1))
        return intervalList

    def getCogPartIntervalList(self, toon, cogPartList):
        itemName = CogDisguiseGlobals.getPartName(cogPartList) 
        intervalList = []
        intervalList.append(Func(self.cogPartLabel.setProp, 'text', itemName))
        intervalList.append(Wait(1))
        return intervalList

    def getMissedItemIntervalList(self, toon, missedItemList):
        intervalList = []
        for itemId in missedItemList:
            itemName = Quests.getItemName(itemId)
            intervalList.append(Func(self.missedItemLabel.setProp, 'text', itemName))
            intervalList.append(Wait(1))
        return intervalList


    def getExpTrack(self, toon, origExp, earnedExp, deathList, origQuestsList, itemList,
                    missedItemList, origMeritList, meritList, partList,
                    toonList, uberEntry, helpfulToonsList):
        """
        Assumes for input:
        origExp: a list of 7 values, corresponding to current experience
        levels in each track.
        earnedExp: a list of 7 values, corresponding to amount of experience
        earned in the battle for each track.
        deathList: a list of the suits that were killed in battle the
        list will be flattened triplets of (suitIndex, level, involvedToonBits)
        suitIndex is the index of the suit in SuitDNA.suitHeadTypes.
        For example, Flunky is suitIndex 0, Yes Man is suitIndex 2.
        
        toonList is a list of toons that positionally corresponds to the
        bitmasks embedded in the deathlist; toons that are no longer
        present are represented as 'None'. Note that this might be
        different from a battle's current activeToons list if any toons
        have just recently dropped.
        """

        track = Sequence(Func(self.initGagFrame, toon, origExp, origMeritList),
                         Wait(1.0))
                         
        endTracks = [0,0,0,0,0,0,0]
        trackEnded = 0
        
        #uberField = ToontownBattleGlobals.decodeUber(uberEntry)
                
        for trackIndex in range(len(earnedExp)):
            # Create a track for each gag track in which we gained experience
            if earnedExp[trackIndex] > 0 or origExp[trackIndex] >= ToontownBattleGlobals.MaxSkill:
                track += self.getTrackIntervalList(toon, trackIndex,
                                                            origExp[trackIndex],
                                                            earnedExp[trackIndex],
                                                            ToontownBattleGlobals.getUberFlagSafe(uberEntry, trackIndex))
                # if we weren't at the end of the track yet, but we will be there
                # after experience is divvied up, make a note of it
                maxExp = ToontownBattleGlobals.MaxSkill - ToontownBattleGlobals.UberSkill
                if (origExp[trackIndex] < maxExp) and (earnedExp[trackIndex] + origExp[trackIndex] >= maxExp):
                    endTracks[trackIndex] = 1
                    trackEnded = 1
                
        for dept in range(len(SuitDNA.suitDepts)):
            # Create a track for each cog dept in which we gained merits
            if meritList[dept]:
                track += self.getMeritIntervalList(toon,
                                                   dept,
                                                   origMeritList[dept],
                                                   meritList[dept])

        track.append(Wait(1.0))

        itemInterval = self.getItemIntervalList(toon, itemList)
        if itemInterval:
            track.append(Func(self.initItemFrame, toon))
            track.append(Wait(1.0))
            track += itemInterval
            track.append(Wait(1.0))

        missedItemInterval = self.getMissedItemIntervalList(toon, missedItemList) 
        if missedItemInterval:
            track.append(Func(self.initMissedItemFrame, toon))
            track.append(Wait(1.0))
            track += missedItemInterval
            track.append(Wait(1.0))

        # debug
        self.notify.debug("partList = %s" % partList)
        
        newPart = 0
        for part in partList:
            if part != 0:
                newPart = 1
                break
        if newPart:
            partList = self.getCogPartIntervalList(toon, partList)
            if partList:
                track.append(Func(self.initCogPartFrame, toon))
                track.append(Wait(1.0))
                track += partList
                track.append(Wait(1.0))

        # Add on any quest progress intervals
        questList = self.getQuestIntervalList(toon, deathList, toonList, origQuestsList, itemList, helpfulToonsList)
        if questList:
            # We have to make a copy of the toon's quest data now,
            # when we build up the tracks, rather than later, while
            # we're playing them back.  This is because the AI will
            # send our quest progress update any moment.
            track.append(Func(self.initQuestFrame, toon, copy.deepcopy(toon.quests)))
            track.append(Wait(1.0))
            track += questList
            track.append(Wait(2.0))
        
        # if the player has reached the end of a track, queue up the frames vanishing
        # and a fanfare occurring
        if trackEnded:
            track.append(Func(self.vanishFrames))
            track.append(Fanfare.makeFanfare(0,toon)[0])
            
            # for each track we've reached the end up, create an end track interval
            for i in range(len(endTracks)):
                if endTracks[i] is 1:
                        track += self.getEndTrackIntervalList(toon,toonList,i)
                        
            # at the end, cleanup and cause all the endtrack frames to vanish
            track.append(Func(self.cleanupEndTrack))
            
        return track


    def testMovie(self, otherToons=[]):
        track = Sequence()
        # Add a show at the beginning
        track.append(Func(self.show))
        expTrack = self.getExpTrack(
            base.localAvatar, # toon
            [1999, 0, 20, 30, 10, 0, 60], # origExp
            [2, 0, 2, 6, 1, 0, 8], # earnedExp
            [3, 1, 3, 0, 2, 2, 1, 1, 30, 2, 1, 0], # deathList
            [], # origQuestsList
            [], # itemList
            [], # missedItemList
            [0, 0, 0, 0], # origMeritList            
            [0, 0, 0, 0], # meritList
            [], # cogPartList
            [base.localAvatar] + otherToons, # toonList
            )
        track.append(expTrack)
        if len(track) > 0:
            # Put a hide at the end
            track.append(Func(self.hide))
            # Put a neutral cycle at the end
            track.append(Func(base.localAvatar.loop, "neutral"))
            # Put the camera back at the end
            track.append(Func(base.localAvatar.startUpdateSmartCamera))
            # Play the track
            track.start()
            # Make localToon dance
            base.localAvatar.loop('victory')
            #base.localAvatar.avCam.stopUpdate()
            base.localAvatar.stopUpdateSmartCamera()
            camera.setPosHpr(0, 8, base.localAvatar.getHeight() * 0.66,
                             179, 15, 0)
        else:
            self.notify.debug("no experience, no movie.")
        return None
