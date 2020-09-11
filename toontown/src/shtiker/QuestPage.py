from pandac.PandaModules import *
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.quest import Quests
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.quest import QuestPoster

class QuestPage(ShtikerPage.ShtikerPage):

    # special methods
    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        # quests maps page index to (questId, npcId)
        self.quests = { 0 : None,
                        1 : None,
                        2 : None,
                        3 : None,
                        }
        self.textRolloverColor = Vec4(1,1,0,1)
        self.textDownColor = Vec4(0.5,0.9,1,1)
        self.textDisabledColor = Vec4(0.4,0.8,0.4,1)
        self.onscreen = 0
        self.lastQuestTime = globalClock.getRealTime()
        
    def load(self):
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.QuestPageToonTasks,
            text_scale = 0.12,
            textMayChange = 0,            
            pos = (0,0,0.6),
            )

        # Throw in a little random roll and scale variations for interest
        #questFramePlaceList = ((-0.45,0,0.25,0,0,2,1.04, 1.09, 1.09),
        #                       (-0.45,0,-0.35,0,0,-2,1.077, 1.077, 1.023),
        #                       (0.45,0,0.25,0,0,3,1.08, 1.102, 1.08),
        #                       (0.45,0,-0.35,0,0,0,1.095, 1.095, 1.07),
        #                       )
        # The random roll does not look so good with the new artwork
        # and progress bars (they alias badly). Scale looks bad without the roll
        questFramePlaceList = ((-0.45,0,0.25,0,0,0),
                               (-0.45,0,-0.35,0,0,0),
                               (0.45,0,0.25,0,0,0),
                               (0.45,0,-0.35,0,0,0),
                               )
        
        self.questFrames = []

        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            # reverse the poster graphic on the right-hand page
            frame = QuestPoster.QuestPoster(reverse=(i>1))
            frame.reparentTo(self)
            frame.setPosHpr(*questFramePlaceList[i])
            frame.setScale(1.06)
            self.questFrames.append(frame)

    def acceptOnscreenHooks(self):        
        self.accept(ToontownGlobals.QuestsHotkeyOn, self.showQuestsOnscreen)
        self.accept(ToontownGlobals.QuestsHotkeyOff, self.hideQuestsOnscreen)

    def ignoreOnscreenHooks(self):        
        self.ignore(ToontownGlobals.QuestsHotkeyOn)
        self.ignore(ToontownGlobals.QuestsHotkeyOff)

    def unload(self):
        del self.title
        del self.quests
        del self.questFrames
        loader.unloadModel("phase_3.5/models/gui/stickerbook_gui")
        ShtikerPage.ShtikerPage.unload(self)

    def clearQuestFrame(self, index):
        self.questFrames[index].clear()
        self.quests[index] = None

    def fillQuestFrame(self, questDesc, index):
        self.questFrames[index].update(questDesc)
        self.quests[index] = questDesc
        
    def getLowestUnusedIndex(self):
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if self.quests[i] == None:
                return i
        return -1

    def updatePage(self):
        newQuests = base.localAvatar.quests
        carryLimit = base.localAvatar.getQuestCarryLimit()

        # Color the frames you can have quests in blue
        # Color the frames you cannot use yet alpha
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if i < carryLimit:
                self.questFrames[i].show()
            else:
                self.questFrames[i].hide()
        
        # This is annoying - the newQuests are lists (not tuples) but
        # the keys to the page's quest dict must be tuples (not lists)
        # so they are immutable hashable keys. Convert where appropriate.
        for index, questDesc in self.quests.items():
            if ((questDesc is not None) and (list(questDesc) not in newQuests)):
                # Must be an old quest we have completed
                self.clearQuestFrame(index)
                
        # Add new quests
        for questDesc in newQuests:
            newQuestDesc = tuple(questDesc)
            if newQuestDesc not in self.quests.values():
                index = self.getLowestUnusedIndex()
                self.fillQuestFrame(newQuestDesc, index)

        # Always update friend quests to see if they have changed
        for i in self.quests.keys():
            questDesc = self.quests[i]
            if questDesc:
                questId = questDesc[0]
                if (Quests.getQuestClass(questId) == Quests.FriendQuest):
                    self.questFrames[i].update(questDesc)

    def enter(self):
        """enter(self)
        """
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        """exit(self)
        """
        ShtikerPage.ShtikerPage.exit(self)

    def showQuestsOnscreenTutorial(self):
        self.setPos(0, 0, -0.2)
        self.showQuestsOnscreen()
        
    def showQuestsOnscreen(self):
        messenger.send('wakeup')
        timedif = globalClock.getRealTime() - self.lastQuestTime  
        if timedif < 0.7:
            return
        self.lastQuestTime = globalClock.getRealTime()
        if self.onscreen or base.localAvatar.invPage.onscreen:
            return
        self.onscreen = 1
        self.updatePage()
        self.reparentTo(aspect2d)
        self.title.hide()
        self.show()

    def hideQuestsOnscreenTutorial(self):
        self.setPos(0, 0, 0)
        self.hideQuestsOnscreen()
        
    def hideQuestsOnscreen(self):
        if not self.onscreen:
            return
        self.onscreen = 0
        self.reparentTo(self.book)
        self.title.show()
        self.hide()
              
