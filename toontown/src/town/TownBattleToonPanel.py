from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.toon import LaffMeter
from toontown.battle import BattleBase
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class TownBattleToonPanel(DirectFrame):
    """
    This panel shows the laff meter, and attack choice of a toon.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleToonPanel')

    def __init__(self, id):

        gui = loader.loadModel("phase_3.5/models/gui/battle_gui")
        
        DirectFrame.__init__(self,
                             relief = None,
                             image = gui.find("**/ToonBtl_Status_BG"),
                             # What color should these be?
                             image_color = Vec4(0.5,0.9,0.5,0.7),
                             )
        self.setScale(0.8)
        self.initialiseoptions(TownBattleToonPanel)
        
        # One day, this panel will be associated with an avatar
        self.avatar = None
        # The card
        # In case someone calls SOS
        self.sosText = DirectLabel(parent = self,
                                   relief = None,
                                   pos = (0.1, 0, 0.015),
                                   text = TTLocalizer.TownBattleToonSOS,
                                   text_scale = 0.06,
                                   )
        self.sosText.hide()
        
        self.fireText = DirectLabel(parent = self,
                                   relief = None,
                                   pos = (0.1, 0, 0.015),
                                   text = TTLocalizer.TownBattleToonFire,
                                   text_scale = 0.06,
                                   )
        self.fireText.hide()

        # Before you have decided
        self.undecidedText = DirectLabel(parent = self,
                                         relief = None,
                                         pos = (0.1, 0, 0.015),
                                         text = TTLocalizer.TownBattleUndecided,
                                         text_scale = 0.1,
                                         )
        
        # The text below the laff meter
        self.healthText = DirectLabel(parent = self,
                                      text = '',
                                      pos = (-0.06, 0, -0.075),
                                      text_scale = 0.055,
                                      )
        
        # The event for the health text
        self.hpChangeEvent = None

        # Create a gag node. 
        self.gagNode = self.attachNewNode('gag')
        # Set the position just so
        self.gagNode.setPos(0.1, 0, 0.03)
        # We don't have a gag yet.
        self.hasGag = 0

        # create the pass node
        passGui = gui.find("**/tt_t_gui_bat_pass")
        passGui.detachNode()
        self.passNode = self.attachNewNode('pass')
        self.passNode.setPos(0.1, 0, 0.05)
        passGui.setScale(0.2)
        passGui.reparentTo(self.passNode)
        self.passNode.hide()

        self.laffMeter = None

        # The display below the gag, that tells which suit or toon
        # has been selected.
        self.whichText = DirectLabel(parent = self,
                                     text = '',
                                     pos = (0.1, 0, -0.08),
                                     text_scale = 0.05,
                                     )

        self.hide()
        gui.removeNode()
        return

    def setLaffMeter(self, avatar):
        self.notify.debug("setLaffMeter: new avatar %s" % avatar.doId)

        # Don't set the laff meter if it is already set for this toon.
        if self.avatar == avatar:
            # Send an HP update, just in case things changed.
            messenger.send(self.avatar.uniqueName("hpChange"),
                           [avatar.hp, avatar.maxHp, 1])
            return None
        else:
            # Cleanup the previous laffMeter, if there was one
            if self.avatar:
                self.cleanupLaffMeter()
                
            self.avatar = avatar
            self.laffMeter = LaffMeter.LaffMeter(avatar.style, avatar.hp,
                                                 avatar.maxHp)
            # Connect the laff meter to the avatar
            self.laffMeter.setAvatar(self.avatar)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.06, 0, 0.05)
            self.laffMeter.setScale(0.045)
            self.laffMeter.start()

            # Set the healthText
            self.setHealthText(avatar.hp, avatar.maxHp)
            self.hpChangeEvent = self.avatar.uniqueName("hpChange")
            self.accept(self.hpChangeEvent, self.setHealthText)
        return None

    def setHealthText(self, hp, maxHp, quietly = 0):
        self.healthText['text'] = (TTLocalizer.TownBattleHealthText % {"hitPoints": hp, "maxHit": maxHp})
        return

    def show(self):
        DirectFrame.show(self)
        if self.laffMeter:
            self.laffMeter.start()
        return

    def hide(self):
        DirectFrame.hide(self)
        if self.laffMeter:
            self.laffMeter.stop()
        return

    def updateLaffMeter(self, hp):
        # Just in case this gets called before an avatar is assigned to it.
        if self.laffMeter:
            self.laffMeter.adjustFace(hp, self.avatar.maxHp)
        self.setHealthText(hp, maxHp)
        return

    def setValues(self, index, track, level=None, numTargets=None, 
                targetIndex=None, localNum=None):
        self.notify.debug(
            "Toon Panel setValues: index=%s track=%s level=%s numTargets=%s targetIndex=%s localNum=%s" %
            (index, track, level, numTargets, targetIndex, localNum))
        # Turn off all optional display items
        self.undecidedText.hide()
        self.sosText.hide()
        self.fireText.hide()
        self.gagNode.hide()
        self.whichText.hide()
        self.passNode.hide()
        if self.hasGag:
            self.gag.removeNode()
            self.hasGag = 0
        
        # Turn on the proper display items
        if (track == BattleBase.NO_ATTACK or
            track == BattleBase.UN_ATTACK):
            # Indicates pass or timeout
            self.undecidedText.show()
        elif track == BattleBase.PASS_ATTACK:
            self.passNode.show()
        elif (track == BattleBase.FIRE):
            #import pdb; pdb.set_trace()
            self.fireText.show()
            self.whichText.show()
            self.whichText['text'] = self.determineWhichText(numTargets,
                                                             targetIndex,
                                                             localNum,
                                                             index)
            pass
        elif (track == BattleBase.SOS or
            track == BattleBase.NPCSOS or
            track == BattleBase.PETSOS):
            # Indicates a call for help
            self.sosText.show()
        elif (track >= MIN_TRACK_INDEX and track <= MAX_TRACK_INDEX):
            self.undecidedText.hide()
            self.passNode.hide()
            # It must be an attack... Show a button
            self.gagNode.show()
            invButton = base.localAvatar.inventory.buttonLookup(track, level)
            self.gag = invButton.instanceUnderNode(self.gagNode, "gag")
            self.gag.setScale(0.8)
            self.gag.setPos(0, 0, 0.02)
            # We have a gag now
            self.hasGag = 1
            if ((numTargets is not None)
                and (targetIndex is not None)
                and (localNum is not None)):
                # Show who is being attacked
                self.whichText.show()
                self.whichText['text'] = self.determineWhichText(numTargets,
                                                                 targetIndex,
                                                                 localNum,
                                                                 index)
        else:
            self.notify.error("Bad track value: %s" % track)
        return None

    def determineWhichText(self, numTargets, targetIndex, localNum, index):
        assert numTargets >= 1 and numTargets <= 4
        assert localNum >= 0 and localNum <= 3
        assert index >= 0 and index <= 3
        returnStr = ""
        # We want to traverse backwards, since suits and toons are
        # numbered from right to left.
        targetList = range(numTargets)
        targetList.reverse()
        for i in targetList:
            if targetIndex == -1:
                # Indicates a group attack... All suits are targets of
                # a group attack.
                returnStr += "X"
            elif targetIndex == -2:
                # Indicates a group heal... All toons but localToon are targets
                # of a group heal.
                if i == index:
                    returnStr += "-"
                else:
                    returnStr += "X"
            elif (targetIndex >= 0) and (targetIndex <= 3):
                # A targeted attack or heal
                if i == targetIndex:
                    # Indicates a target
                    returnStr += "X"
                else:
                    # Not a target
                    returnStr += "-"
            else:
                self.notify.error("Bad target index: %s" % targetIndex)
        return returnStr

    def cleanup(self):
        self.ignoreAll()
        # Clean up the laff meter
        self.cleanupLaffMeter()
        # Clean up the gag (if there is one)
        if self.hasGag:
            self.gag.removeNode()
            del self.gag
        # Clean up the gag node
        self.gagNode.removeNode()
        del self.gagNode
        # Cleanup the rest of the panel
        DirectFrame.destroy(self)

    def cleanupLaffMeter(self):
        self.notify.debug("Cleaning up laffmeter!")
        self.ignore(self.hpChangeEvent)
        if self.laffMeter:
            self.laffMeter.destroy()
            self.laffMeter = None
        return None
