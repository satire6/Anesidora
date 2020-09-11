from direct.gui.DirectGui import *
from pandac.PandaModules import *
import QuestPoster
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class QuestChoiceGui(DirectFrame):
    def __init__(self):
        DirectFrame.__init__(self,
                             relief = None,
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = Vec4(0.8,0.6,0.4,1),
                             geom_scale = (1.85,1,0.9),
                             geom_hpr = (0,0,-90),
                             pos = (-0.85,0,0),
                             )
        self.initialiseoptions(QuestChoiceGui)
        self.questChoicePosters = []
        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        self.cancelButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (0.7,1,1),
            text = TTLocalizer.QuestChoiceGuiCancel,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.chooseQuest,
            extraArgs = [0],
            )
        guiButton.removeNode()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.3)

        # Reserve the left edge of the screen for the gui.
        base.setCellsAvailable(base.leftCells, 0)
        base.setCellsAvailable([base.bottomCells[0], base.bottomCells[1]], 0)

        # Don't put this gui on top of everything else; that's risky
        # because popups might get lost under it.  However, we will
        # make an effort to make sure that things *should* be hidden
        # below it.
        #self.setBin('gui-popup', 10)
        
    def setQuests(self, quests, fromNpcId, timeout):
        # The quest list is flattened. Every three elements is a quest
        for i in range(0, len(quests), 3):
            questId, rewardId, toNpcId = quests[i:i+3]
            qp = QuestPoster.QuestPoster()
            qp.reparentTo(self)
            qp.showChoicePoster(questId, fromNpcId, toNpcId, rewardId,
                                self.chooseQuest)
            self.questChoicePosters.append(qp)
        # Space the posters across the screen
        if len(quests) == 1*3:
            self['geom_scale'] = (1,1,.9)
            self.questChoicePosters[0].setPos(0,0,0.1)
            self.cancelButton.setPos(0.15,0,-0.375)
            self.timer.setPos(-0.2,0,-0.35)
        elif len(quests) == 2*3:
            self['geom_scale'] = (1.5,1,.9)
            self.questChoicePosters[0].setPos(0,0,-0.2)
            self.questChoicePosters[1].setPos(0,0,0.4)
            self.cancelButton.setPos(0.15,0,-0.625)
            self.timer.setPos(-0.2,0,-0.6)
        elif len(quests) == 3*3:
            self['geom_scale'] = (1.85,1,0.9)
            map(lambda x: x.setScale(0.95), self.questChoicePosters)
            self.questChoicePosters[0].setPos(0,0,-0.4)
            self.questChoicePosters[1].setPos(0,0,0.125)
            self.questChoicePosters[2].setPos(0,0,0.65)
            self.cancelButton.setPos(0.15,0,-0.8)
            self.timer.setPos(-0.2,0,-0.775)
        self.timer.countdown(timeout, self.timeout)

    def chooseQuest(self, questId):
        # Restore the left edge of the screen to the nametags.
        base.setCellsAvailable(base.leftCells, 1)
        base.setCellsAvailable([base.bottomCells[0], base.bottomCells[1]], 1)
        self.timer.stop()
        messenger.send("chooseQuest", [questId])

    def timeout(self):
        # Timeout is the same as a cancel
        messenger.send("chooseQuest", [0])
