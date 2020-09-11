from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directtools.DirectGeometry import LineNodePath

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.fishing import FishGlobals
from toontown.shtiker import FishPage
from toontown.toonbase import TTLocalizer
from toontown.quest import Quests
from direct.actor import Actor
from direct.showutil import Rope
import math
from direct.task.Task import Task
import random
import random
from toontown.fishing import FishingTargetGlobals
from toontown.fishing import FishBase
from toontown.fishing import FishPanel
from toontown.effects import Ripples
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownTimer
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel

class DistributedFishingSpot(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingSpot")

    # Parameters to control bob motion
    vZeroMax = 25.0
    angleMax = 30.0

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        assert self.notify.debugStateCall(self)
        self.lastAvId = 0
        self.lastFrame = 0
        self.avId = 0
        self.av = None
        self.placedAvatar = 0
        self.localToonFishing = 0
        self.nodePath = None
        self.collSphere = None
        self.collNode = None
        self.collNodePath = None
        self.castTrack = None
        self.pond = None

        self.guiTrack = None

        self.madeGui = 0
        self.castGui = None
        self.itemGui = None
        self.pole = None
        self.line = None
        self.poleNode = []
        self.ptop = None
        self.bob = None

        self.bobBobTask = None
        self.splashSounds = None
        self.ripples = None

        self.line = None
        self.lineSphere = None

        self.power = 0.0
        self.startAngleNP = 0
        self.firstCast = 1
        self.fishPanel = None

        self.fsm = ClassicFSM.ClassicFSM('DistributedFishingSpot',
                           [State.State('off',
                                        self.enterOff, self.exitOff,
                                        ['waiting', 'distCasting', 'fishing', 'reward', 'leaving']),
                            State.State('waiting',
                                        self.enterWaiting, self.exitWaiting,
                                        ['localAdjusting', 'distCasting', 'leaving', 'sellFish']),
                            State.State('localAdjusting',
                                        self.enterLocalAdjusting, self.exitLocalAdjusting,
                                        ['localCasting', 'leaving']),
                            State.State('localCasting',
                                        self.enterLocalCasting, self.exitLocalCasting,
                                        ['localAdjusting', 'fishing', 'leaving']),
                            # The transition to reward is kinda strange. I'm not sure
                            # exactly why that is happening in the release. Need to look
                            # into it
                            State.State('distCasting',
                                        self.enterDistCasting, self.exitDistCasting,
                                        ['fishing', 'leaving', 'reward']),
                            # Fishing needs to be able to go directly to reward
                            # for distributed toons that we are watching fish
                            State.State('fishing',
                                        self.enterFishing, self.exitFishing,
                                        ['localAdjusting', 'distCasting', 'waitForAI', 'reward', 'leaving']),
                            State.State('sellFish',
                                        self.enterSellFish, self.exitSellFish,
                                        ['waiting', 'leaving']),
                            State.State('waitForAI',
                                        self.enterWaitForAI, self.exitWaitForAI,
                                        ['reward', 'leaving']),
                            State.State('reward',
                                        self.enterReward, self.exitReward,
                                        ['localAdjusting', 'distCasting', 'leaving', 'sellFish']),
                            State.State('leaving',
                                        self.enterLeaving, self.exitLeaving,
                                        []),
                            ], 'off', 'off',)
        self.fsm.enterInitialState()

    def disable(self):
        assert self.notify.debugStateCall(self)
        self.ignore(self.uniqueName('enterFishingSpotSphere'))
        self.setOccupied(0)
        self.avId = 0
        if self.castTrack != None:
            if self.castTrack.isPlaying():
                self.castTrack.finish()
            self.castTrack = None
        if self.guiTrack != None:
            if self.guiTrack.isPlaying():
                self.guiTrack.finish()
            self.guiTrack = None        
        self.__hideBob()
        self.nodePath.detachNode()
        self.__unmakeGui()
        self.pond.stopCheckingTargets()
        self.pond = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        assert self.notify.debugStateCall(self)
        del self.pond
        del self.fsm
        if self.nodePath:
            self.nodePath.removeNode()
            del self.nodePath
        DistributedObject.DistributedObject.delete(self)
        if self.ripples:
            self.ripples.destroy()

    def generateInit(self):
        """
        This method is called when the DistributedObject is first introduced
        to the world... Not when it is pulled from the cache.
        """
        assert self.notify.debugStateCall(self)
        DistributedObject.DistributedObject.generateInit(self)
        # First, one NodePath to represent the spot itself.  This gets
        # repositioned around according to our setPos.
        self.nodePath = NodePath(self.uniqueName('FishingSpot'))
        self.angleNP = self.nodePath.attachNewNode(self.uniqueName('FishingSpotAngleNP'))
        
        # Make a collision sphere to detect when an avatar enters the
        # fishing spot.
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())

        # Make the sphere intangible, initially.
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.uniqueName('FishingSpotSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)

        self.bobStartPos = Point3(0.0, 3.0, 8.5)

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert self.notify.debugStateCall(self)
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        assert self.notify.debugStateCall(self)
        DistributedObject.DistributedObject.announceGenerate(self)
        # Now that posHpr has been set, reparent to render
        # and accept the sphere event
        # Put the fishing spot in the world
        self.nodePath.reparentTo(self.getParentNodePath())
        
        # When the localToon steps onto the fishing spot, we call
        # requestEnter.
        self.accept(self.uniqueName('enterFishingSpotSphere'),
                    self.__handleEnterSphere)

    def setPondDoId(self, pondDoId):
        assert self.notify.debugStateCall(self)
        self.pond = base.cr.doId2do[pondDoId]
        self.area = self.pond.getArea()
        self.waterLevel = FishingTargetGlobals.getWaterLevel(self.area)

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        # if we're in the estate we should use place.id
        if hasattr(place, 'id'):
            myHoodId = place.id
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            return True
        return False

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def __handleEnterSphere(self, collEntry):
        assert self.notify.debugStateCall(self)
        if self.allowedToEnter():
            # If the same toon re-enters immediately after exiting, it's
            # probably a mistake; ignore it.
            assert(self.notify.debug("__handleEnterSphere"))
            if base.localAvatar.doId == self.lastAvId and \
               globalClock.getFrameCount() <= self.lastFrame + 1:
                self.notify.debug("Ignoring duplicate entry for avatar.")
                return
            # Only toons with hp > 0 that aren't already fishing can fish
            if (base.localAvatar.hp > 0) and (base.cr.playGame.getPlace().fsm.getCurrentState().getName() != "fishing"):
                # Take them the localToon out of walk mode
                self.cr.playGame.getPlace().detectedFishingCollision()
                self.d_requestEnter()
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='fishing',
                                                  doneFunc=self.handleOkTeaser)              

    def d_requestEnter(self):
        assert self.notify.debugStateCall(self)
        self.sendUpdate("requestEnter", [])

    def rejectEnter(self):
        assert self.notify.debugStateCall(self)
        # Take them the localToon out of walk mode
        self.cr.playGame.getPlace().setState("walk")

    def d_requestExit(self):
        assert self.notify.debugStateCall(self)
        self.sendUpdate("requestExit", [])

    def d_doCast(self, power, heading):
        assert self.notify.debugStateCall(self)
        self.sendUpdate("doCast", [power, heading])

    def getSphereRadius(self):
        assert self.notify.debugStateCall(self)
        return 1.5

    def getParentNodePath(self):
        assert self.notify.debugStateCall(self)
        return render

    def setPosHpr(self, x, y, z, h, p, r):
        """
        The handler that catches the initial position and orientation
        established on the AI.
        """
        assert self.notify.debugStateCall(self)
        self.nodePath.setPosHpr(x, y, z, h, p, r)
        self.angleNP.setH(render, self.nodePath.getH(render))

    def setOccupied(self, avId):
        assert self.notify.debugStateCall(self)
        if self.av != None:
            if not self.av.isEmpty():
                self.__dropPole()
                self.av.loop('neutral')
                self.av.setParent(ToontownGlobals.SPRender)
                self.av.startSmooth()
            self.ignore(self.av.uniqueName("disable"))
            self.__hideBob()
            self.fsm.requestFinalState()
            self.__removePole()
            self.av = None
            self.placedAvatar = 0
            self.angleNP.setH(render, self.nodePath.getH(render))
        self.__hideLine()

        wasLocalToon = self.localToonFishing

        self.lastAvId = self.avId
        self.lastFrame = globalClock.getFrameCount()
        self.avId = avId
        self.localToonFishing = 0

        if self.avId == 0:
            # No one is in the fishing spot; it's available.
            self.collSphere.setTangible(0)            
        else:
            # The fishing spot is occupied; no one else may be here.
            self.collSphere.setTangible(1)
            if self.avId == base.localAvatar.doId:
                # Free up all of the nametag cells on the bottom edge
                # of the screen to leave room for the fishing gui.
                base.setCellsAvailable(base.bottomCells, 0)

                self.localToonFishing = 1

                if base.wantBingo:
                    # Set the Pond localToonSpot Reference to 'this instance' of
                    # a fishing spot because the local toon is now fishing at
                    # a spot. It was not enough to set and unset the reference
                    # when checking the fish targets because Bingo needs to be
                    # able to access the spot GUI when the local Toon is not
                    # in the 'fishing' state. (JJT - 06/23/04)
                    self.pond.setLocalToonSpot(self)

            av = self.cr.doId2do.get(self.avId)
            if av:
                self.av = av
                self.__loadStuff()
                self.placedAvatar = 0
                self.firstCast = 1
                self.acceptOnce(self.av.uniqueName("disable"), self.__avatarGone)
                # Parent it to the fishing spot
                # perhaps we need to keep smoothing on?
                self.av.stopSmooth()
                self.av.wrtReparentTo(self.angleNP)
                self.av.setAnimState("neutral", 1.0)
                self.createCastTrack()
            else:
                self.notify.warning("Unknown avatar %d in fishing spot %d" % (self.avId, self.doId))

        # If the local toon was involved but is no longer, restore
        # walk mode.  We do this down here, after we have twiddled
        # with the tangible flag, so that the toon must walk out and
        # walk back in again in order to generate the enter event
        # again.
        if wasLocalToon and not self.localToonFishing:
            self.__hideCastGui()

            if base.wantBingo:
                # Reset the Pond FishingSpot Reference to None now that the local
                # toon is no longer involved with the spot. (JJT - 06/23/04)
                self.pond.setLocalToonSpot()

            # Restore the normal nametag cells.
            base.setCellsAvailable([base.bottomCells[1], base.bottomCells[2]], 1)
            base.setCellsAvailable(base.rightCells, 1)
            # Reset to walk mode, but not if we're exiting all the way
            # out (and our place is already gone).
            place = base.cr.playGame.getPlace()
            if place:
                place.setState('walk')

    def __avatarGone(self):
        assert self.notify.debugStateCall(self)
        # Called when the avatar in the fishing spot vanishes.
        # The AI will call setOccupied(0), too, but we call it first
        # just to be on the safe side, so we don't try to access a
        # non-existent avatar.
        self.setOccupied(0)

    def setMovie(self, mode, code, itemDesc1, itemDesc2, itemDesc3, power, h):
        assert self.notify.debugStateCall(self)
        if self.av == None:
            # No avatar, no movie
            return

        if mode == FishGlobals.NoMovie:
            pass
        elif mode == FishGlobals.EnterMovie:
            self.fsm.request("waiting")
        elif mode == FishGlobals.ExitMovie:
            self.fsm.request("leaving")
        elif mode == FishGlobals.CastMovie:
            # Note: this message is only really used for dist toons
            if not self.localToonFishing:
                self.fsm.request("distCasting", [power, h])
        elif mode == FishGlobals.PullInMovie:
            self.fsm.request("reward", [code, itemDesc1, itemDesc2, itemDesc3])

    def getStareAtNodeAndOffset(self):
        # spammy: assert self.notify.debugStateCall(self)
        return self.nodePath, Point3()

    def __loadStuff(self):
        assert self.notify.debugStateCall(self)
        # The rod index is a required broadcast field on the toon, so we
        # should know what everybody's rod index is
        rodId = self.av.getFishingRod()
        rodPath = FishGlobals.RodFileDict.get(rodId)
        if not rodPath:
            self.notify.warning("Rod id: %s model not found" % (rodId))
            # Just use the 0 index rod
            rodPath = RodFileDict[0]

        self.pole = Actor.Actor()
        self.pole.loadModel(rodPath)
        # All rods use the same animation
        self.pole.loadAnims({'cast' : 'phase_4/models/props/fishing-pole-chan'})
        self.pole.pose('cast', 0)
        # Get the top of the pole.
        self.ptop = self.pole.find('**/joint_attachBill')

        if self.line == None:
            # Make a Rope object to show the fishing line.
            self.line = Rope.Rope(self.uniqueName('Line'))
            self.line.setColor(1, 1, 1, 0.4)
            self.line.setTransparency(1)
            # This is the bounding sphere that will be set on the line.
            # We don't trust the line to compute its own bounding sphere
            # since we'll be moving it around a lot (and plus it's under
            # multiple instances).
            self.lineSphere = BoundingSphere(Point3(-0.6, -2, -5), 5.5)

        if self.bob == None:
            self.bob = loader.loadModel('phase_4/models/props/fishing_bob')
            self.bob.setScale(1.5)
            self.ripples = Ripples.Ripples(self.nodePath)
            self.ripples.setScale(0.4)
            self.ripples.hide()

        if self.splashSounds == None:
            self.splashSounds = (base.loadSfx('phase_4/audio/sfx/TT_splash1.mp3'),
                                 base.loadSfx('phase_4/audio/sfx/TT_splash2.mp3'),
                                 )

    def __placeAvatar(self):
        assert self.notify.debugStateCall(self)
        # Places the avatar at the fishing spot, mainly for the
        # benefit of those who did not observe the EnterMovie.
        if not self.placedAvatar:
            self.placedAvatar = 1
            self.__holdPole()
            self.av.setPosHpr(0, 0, 0, 0, 0, 0)
        
    def __holdPole(self):
        assert self.notify.debugStateCall(self)
        if self.poleNode != []:
            self.__dropPole()
        # One node, instanced to each of the toon's three right hands,
        # will hold the pole.
        np = NodePath('pole-holder')
        hands = self.av.getRightHands()
        for h in hands:
            self.poleNode.append(np.instanceTo(h))
        self.pole.reparentTo(self.poleNode[0])

    def __dropPole(self):
        assert self.notify.debugStateCall(self)
        self.__hideBob()
        self.__hideLine()
        if self.pole != None:
            self.pole.clearMat()
            self.pole.detachNode()
        for pn in self.poleNode:
            pn.removeNode()
        self.poleNode = []

    def __removePole(self):
        assert self.notify.debugStateCall(self)
        self.pole.removeNode()
        self.poleNode = []
        self.ptop.removeNode()
        self.pole = None
        self.ptop = None

    def __showLineWaiting(self):
        assert self.notify.debugStateCall(self)
        # Show the fishing line, waiting for a nibble.
        self.line.setup(4, ((None, (0, 0, 0)), (None, (0, -2, -4)),
                            (self.bob, (0, -1, 0)), (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)

    def __showLineCasting(self):
        assert self.notify.debugStateCall(self)
        # Show the fishing line, waiting for a nibble.
        self.line.setup(2, ((None, (0, 0, 0)),
                            (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)

    def __showLineReeling(self):
        assert self.notify.debugStateCall(self)
        # Show the fishing line, waiting for a nibble.
        self.line.setup(2, ((None, (0, 0, 0)),
                            (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)

    def __hideLine(self):
        assert self.notify.debugStateCall(self)
        if self.line:
            # Hide the fishing line.
            self.line.detachNode()

    def __showBobFloat(self):
        assert self.notify.debugStateCall(self)
        # Put the bob in the water and make it gently float.
        self.__hideBob()
        self.bob.reparentTo(self.angleNP)
        # Ripple effect
        self.ripples.reparentTo(self.angleNP)
        self.ripples.setPos(self.bob.getPos())
        self.ripples.setZ(self.waterLevel + 0.025)
        self.ripples.play()
        # Splash sfx
        splashSound = random.choice(self.splashSounds)
        base.playSfx(splashSound, volume=0.8, node=self.bob)
        self.bobBobTask = taskMgr.add(self.__doBobBob, self.taskName('bob'))

    def __hideBob(self):
        assert self.notify.debugStateCall(self)
        if self.bob:
            self.bob.detachNode()
        if self.bobBobTask:
            taskMgr.remove(self.bobBobTask)
            self.bobBobTask = None
        if self.ripples:
            self.ripples.stop()
            self.ripples.detachNode()

    def __doBobBob(self, task):
        assert self.notify.debugStateCall(self)
        # Task to make the bob bounce up and down as if it is
        # floating, but has not yet had a nibble.
        z = math.sin(task.time * 1.8) * 0.08
        self.bob.setZ(self.waterLevel + z)
        return Task.cont
        
    def __userExit(self, event=None):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.fsm.request("leaving")
            self.d_requestExit()

    def __sellFish(self, result=None):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            if result == DGG.DIALOG_OK:
                # send the update to the ai, and disable the buttons
                # so they can't multi-click
                self.sendUpdate("sellFish", [])
                for button in self.sellFishDialog.buttonList:
                    button['state'] = DGG.DISABLED
            else:
                # since we only allow them to sell if their bucket is full,
                # if they cancelled, kick them out of fishing
                self.fsm.request("leaving")
                self.d_requestExit()

    def __sellFishConfirm(self, result = None):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.fsm.request("waiting", [False])

    def __showCastGui(self):
        assert self.notify.debugStateCall(self)
        self.__hideCastGui()
        self.__makeGui()
        self.castButton.show()
        self.arrow.hide()
        self.exitButton.show()
        self.timer.show()
        self.__updateFishTankGui()
        self.castGui.reparentTo(aspect2d)
        self.castButton['state'] = DGG.NORMAL
        self.jar['text'] = str(self.av.getMoney())

        self.accept(localAvatar.uniqueName("moneyChange"), self.__moneyChange)
        self.accept(localAvatar.uniqueName("fishTankChange"), self.__updateFishTankGui)

        # Hide the cannon game GUI if present
        target = base.cr.doFind("DistributedTarget")
        if target:
            target.hideGui()
        
        # Should guard this for publish
        if base.wantBingo:
            self.__setBingoCastGui()
        
        # I need to make these helper funcs because the event from bind
        # adds a mouse parameter onto the message that screws up the fsm request
        def requestLocalAdjusting(mouseEvent):
            if self.av.isFishTankFull() and self.__allowSellFish():
                self.fsm.request("sellFish")
            else:
                self.fsm.request("localAdjusting")
        def requestLocalCasting(mouseEvent):
            if not (self.av.isFishTankFull() and self.__allowSellFish()):
                self.fsm.request("localCasting")
            
        # Lets go ahead and bind both left and right mouse buttons
        # so nobody is confused
        self.castButton.bind(DGG.B1PRESS, requestLocalAdjusting)
        self.castButton.bind(DGG.B3PRESS, requestLocalAdjusting)
        self.castButton.bind(DGG.B1RELEASE, requestLocalCasting)
        self.castButton.bind(DGG.B3RELEASE, requestLocalCasting)
        if (self.firstCast and
            (len(self.av.fishCollection) == 0) and
            (len(self.av.fishTank) == 0)):
            self.__showHowTo(TTLocalizer.FishingHowToFirstTime)
        elif (base.wantBingo and 
              self.pond.hasPondBingoManager() and
              not self.av.bFishBingoTutorialDone):
            self.__showHowTo(TTLocalizer.FishBingoHelpMain)
            self.av.b_setFishBingoTutorialDone(True)
            

    def __moneyChange(self, money):
        self.jar["text"] = str(money)
   
    def __initCastGui(self):
        assert self.notify.debugStateCall(self)
        self.timer.countdown(FishGlobals.CastTimeout)
            
    def __showQuestItem(self, itemId):
        assert self.notify.debugStateCall(self)
        # Tells the user what quest item he just caught.
        self.__makeGui()
        itemName = Quests.getItemName(itemId)
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        self.itemPackage.show()
        self.itemJellybean.hide()
        self.itemBoot.hide()

    def __showBootItem(self):
        assert self.notify.debugStateCall(self)
        # Tells the user he found an old boot
        self.__makeGui()
        itemName = TTLocalizer.FishingBootItem
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        self.itemBoot.show()
        self.itemJellybean.hide()
        self.itemPackage.hide()

    #####################################################
    # Method: __setItemLabel
    # Purpose: This method sets the text of the
    #          boot item panel. If Bingo night is ongoing
    #          then it should inform the players that the
    #          boot is a positive wildcard.
    # Input: None
    # Output: None
    #####################################################
    def __setItemLabel(self):
        if self.pond.hasPondBingoManager():
            self.itemLabel['text'] = str(itemName + '\n\n' + 'BINGO WILDCARD')
        else:
            self.itemLabel['text'] = itemName

    def __showJellybeanItem(self, amount):
        assert self.notify.debugStateCall(self)
        # Tells the user what jellybean amount he just caught.
        self.__makeGui()
        itemName = TTLocalizer.FishingJellybeanItem % amount
        self.itemLabel['text'] = itemName
        self.itemGui.reparentTo(aspect2d)
        # By now, the avatar's actual money should be updated
        # So let's just query it again to update the jar text
        self.jar['text'] = str(self.av.getMoney())
        self.itemJellybean.show()
        self.itemBoot.hide()
        self.itemPackage.hide()

    def __showFishItem(self, code, fish):
        assert self.notify.debugStateCall(self)
        # Tells the user what fish item he just caught.
        self.fishPanel = FishPanel.FishPanel(fish)
        self.__setFishItemPos()
        # This is carefully placed over the window image.  Please try to keep
        # this in sync with the window position:
        # (tip: FishPicker.py uses the same bounds for its fish dialog.  OK,
        # maybe they should pull from the same variable; fix it if you like):
        #self.fishPanel.setSwimBounds(-0.29, 0.29, -0.23, 0.25)
        self.fishPanel.setSwimBounds(-0.3, 0.3, -0.235, 0.25)
        # Parchment paper background:
        self.fishPanel.setSwimColor(1.0, 1.0, 0.74901, 1.0)
        self.fishPanel.load()
        self.fishPanel.show(code)
        self.__updateFishTankGui()

    #####################################################
    # Method: __setFishItemPos
    # Purpose: This class sets the position of the Fish
    #          panel based on whether Bingo Night is
    #          occuring.
    # Input: None
    # Output: None
    #####################################################
    def __setFishItemPos(self):
        if base.wantBingo:
            if self.pond.hasPondBingoManager():
                self.fishPanel.setPos(0.65, 0, 0.4)
            else:
                self.fishPanel.setPos(0,0,0.5)
        else:
            self.fishPanel.setPos(0,0,0.5)
        
        
    def __updateFishTankGui(self):
        assert self.notify.debugStateCall(self)
        # Update our fish tank display base on the latest value we have from the AI
        fishTank = self.av.getFishTank()
        lenFishTank = len(fishTank)
        maxFishTank = self.av.getMaxFishTank()
        self.bucket['text'] = ("%s/%s" % (lenFishTank, maxFishTank))
            
    def __showFailureReason(self, code):
        assert self.notify.debugStateCall(self)
        # Tells the user why he caught nothing.
        self.__makeGui()
        reason = ""
        if code == FishGlobals.OverTankLimit:
            reason = TTLocalizer.FishingOverTankLimit
        self.failureDialog.setMessage(reason)
        self.failureDialog.show()

    def __showSellFishDialog(self):
        assert self.notify.debugStateCall(self)
        self.__makeGui()
        self.sellFishDialog.show()

    def __hideSellFishDialog(self):
        assert self.notify.debugStateCall(self)
        self.__makeGui()
        self.sellFishDialog.hide()

    def __showSellFishConfirmDialog(self, numFishCaught):
        assert self.notify.debugStateCall(self)
        self.__makeGui()
        msg = TTLocalizer.STOREOWNER_TROPHY % (numFishCaught, FishGlobals.getTotalNumFish())
        self.sellFishConfirmDialog.setMessage(msg)
        self.sellFishConfirmDialog.show()

    def __hideSellFishConfirmDialog(self):
        assert self.notify.debugStateCall(self)
        self.__makeGui()
        self.sellFishConfirmDialog.hide()

    def __showBroke(self):
        assert self.notify.debugStateCall(self)
        # Tells the user he is broke
        self.__makeGui()
        self.brokeDialog.show()
        self.castButton['state'] = DGG.DISABLED

    def __showHowTo(self, message):
        assert self.notify.debugStateCall(self)
        # Tells the user how to fish
        self.__makeGui()
        self.howToDialog.setMessage(message)
        self.howToDialog.show()

    def __hideHowTo(self, event=None):
        assert self.notify.debugStateCall(self)
        # Hid the howto gui
        self.__makeGui()
        self.howToDialog.hide()

    def __showFishTankFull(self):
        assert self.notify.debugStateCall(self)
        # Tells the user why he can't fish.
        self.__makeGui()
        self.__showFailureReason(FishGlobals.OverTankLimit)
        self.castButton['state'] = DGG.DISABLED
        
    def __hideCastGui(self):
        assert self.notify.debugStateCall(self)

        # Show the cannon game GUI if present
        target = base.cr.doFind("DistributedTarget")
        if target:
            target.showGui()
        
        if self.madeGui:
            self.timer.hide()
            self.castGui.detachNode()
            self.itemGui.detachNode()
            self.failureDialog.hide()
            self.sellFishDialog.hide()
            self.sellFishConfirmDialog.hide()
            self.brokeDialog.hide()
            self.howToDialog.hide()
            self.castButton.unbind(DGG.B1PRESS)
            self.castButton.unbind(DGG.B3PRESS)
            self.castButton.unbind(DGG.B1RELEASE)
            self.castButton.unbind(DGG.B3RELEASE)

            self.ignore(localAvatar.uniqueName("moneyChange"))
            self.ignore(localAvatar.uniqueName("fishTankChange"))

    def __itemGuiClose(self):
        assert self.notify.debugStateCall(self)
        self.itemGui.detachNode()

    def __makeGui(self):
        assert self.notify.debugStateCall(self)
        if self.madeGui:
            return

        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.hide()
        
        self.castGui = loader.loadModel("phase_4/models/gui/fishingGui")
        self.castGui.setScale(0.67)
        self.castGui.setPos(0,1,0)

        for nodeName in ("bucket", "jar", "display_bucket", "display_jar"):
            self.castGui.find("**/" + nodeName).reparentTo(self.castGui)

        self.exitButton = DirectButton(
            parent = self.castGui,
            relief = None,
            text = ("", TTLocalizer.FishingExit, TTLocalizer.FishingExit),
            text_align = TextNode.ACenter,
            text_scale = 0.1,
            text_fg = Vec4(1,1,1,1),
            text_shadow = Vec4(0,0,0,1),
            text_pos = (0.0, -0.12),
            pos = (1.75, 0, -1.33),
            textMayChange = 0,
            image = (self.castGui.find("**/exit_buttonUp"),
                     self.castGui.find("**/exit_buttonDown"),
                     self.castGui.find("**/exit_buttonRollover")),
            command = self.__userExit,
            )
        # Get rid of the model we copied from
        self.castGui.find("**/exitButton").removeNode()

        self.castButton = DirectButton(
            parent = self.castGui,
            relief = None,
            text = TTLocalizer.FishingCast,
            text_align = TextNode.ACenter,
            text_scale = (3,3*0.75,3*0.75),
            text_fg = Vec4(1,1,1,1),
            text_shadow = Vec4(0,0,0,1),
            text_pos = (0, -4),
            image = self.castGui.find("**/castButton"),
            image0_color = (1, 0, 0, 1),
            image1_color = (0, 1, 0, 1),
            image2_color = (1, 1, 0, 1),
            image3_color = (0.8, 0.5, 0.5, 1),
            pos = (0, -0.05, -0.666),
            scale = (0.036, 1, 0.048),
            )
        # Get rid of the model we copied from
        self.castGui.find("**/castButton").removeNode()

        self.arrow = self.castGui.find("**/arrow")
        self.arrowTip = self.arrow.find("**/arrowTip")
        self.arrowTail = self.arrow.find("**/arrowTail")
        self.arrow.reparentTo(self.castGui)
        self.arrow.setColorScale(0.9,0.9,0.1,0.7)
        self.arrow.hide()

        self.jar = DirectLabel(
            parent = self.castGui,
            relief = None,
            text = str(self.av.getMoney()),
            text_scale = 0.16,
            text_fg = (0.95, 0.95, 0, 1),
            text_font = ToontownGlobals.getSignFont(),
            pos = (-1.12, 0, -1.3),
            )
        self.bucket = DirectLabel(
            parent = self.castGui,
            relief = None,
            text = "",
            text_scale = 0.09,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            pos = (1.14, 0, -1.33),
            )
        self.__updateFishTankGui()

        # Vector line
        self.itemGui = NodePath('itemGui')
        self.itemFrame = DirectFrame(
            parent = self.itemGui,
            relief = None,
            geom = DGG.getDefaultDialogGeom(),
            geom_color = ToontownGlobals.GlobalDialogColor,
            geom_scale = (1, 1, 0.6),
            text = TTLocalizer.FishingItemFound,
            text_pos = (0, 0.2),
            text_scale = 0.08,
            pos = (0, 0, 0.587),
            )

        self.itemLabel = DirectLabel(
            parent = self.itemFrame,
            text = "",
            text_scale = 0.06,
            pos = (0, 0, -0.25),
            )

        # item gui close button
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.itemGuiCloseButton = DirectButton(
            parent = self.itemFrame,
            pos = (0.44, 0, -0.24),
            relief = None,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            image_scale = (0.7, 1, 0.7),
            command = self.__itemGuiClose,
            )
        buttons.removeNode()

        # Images for the item panels
        jarGui = loader.loadModel("phase_3.5/models/gui/jar_gui")
        bootGui = loader.loadModel("phase_4/models/gui/fishing_boot")
        packageGui = loader.loadModel("phase_3.5/models/gui/stickerbook_gui").find("**/package")
        self.itemJellybean = DirectFrame(
            parent = self.itemFrame,
            relief = None,
            image = jarGui,
            scale = 0.5,
            )
        self.itemBoot = DirectFrame(
            parent = self.itemFrame,
            relief = None,
            image = bootGui,
            scale = 0.2,
            )
        self.itemPackage = DirectFrame(
            parent = self.itemFrame,
            relief = None,
            image = packageGui,
            scale = 0.25,
            )
        self.itemJellybean.hide()
        self.itemBoot.hide()
        self.itemPackage.hide()
        
        self.failureDialog = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("failureDialog"),
            doneEvent = self.uniqueName("failureDialog"),
            command = self.__userExit,
            message = TTLocalizer.FishingFailure,
            style = TTDialog.CancelOnly,
            cancelButtonText = TTLocalizer.FishingExit,
            )
        self.failureDialog.hide()
        
        self.sellFishDialog = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("sellFishDialog"),
            doneEvent = self.uniqueName("sellFishDialog"),
            command = self.__sellFish,
            message = TTLocalizer.FishBingoOfferToSellFish,
            style = TTDialog.YesNo,
            )
        self.sellFishDialog.hide()
        
        self.sellFishConfirmDialog = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("sellFishConfirmDialog"),
            doneEvent = self.uniqueName("sellFishConfirmDialog"),
            command = self.__sellFishConfirm,
            message = TTLocalizer.STOREOWNER_TROPHY,
            style = TTDialog.Acknowledge,
            )
        self.sellFishConfirmDialog.hide()
        
        self.brokeDialog = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("brokeDialog"),
            doneEvent = self.uniqueName("brokeDialog"),
            command = self.__userExit,
            message = TTLocalizer.FishingBroke,
            style = TTDialog.CancelOnly,
            cancelButtonText = TTLocalizer.FishingExit,
            )
        self.brokeDialog.hide()

        self.howToDialog = TTDialog.TTGlobalDialog(
            dialogName = self.uniqueName("howToDialog"),
            doneEvent = self.uniqueName("howToDialog"),
            fadeScreen = 0,
            message = TTLocalizer.FishingHowToFailed,
            style = TTDialog.Acknowledge,
            )
        self.howToDialog['command'] = self.__hideHowTo
        self.howToDialog.setPos(-0.3,0,0.5)
        self.howToDialog.hide()

        self.madeGui = 1

    ############################################################
    # Method: __setBingoCastGui
    # Purpose: This method sets the Jar and Bucket position/scale
    #          whenever a client enters a fishing spot AFTER
    #          bingo night has begun. The client will not need
    #          to see the intro "movie" found in setCastGui
    #          since bingo night has already begun.
    # Input: None
    # Output: None
    ############################################################
    def __setBingoCastGui(self):
        if self.pond.hasPondBingoManager():
            self.notify.debug('__setBingoCastGui: Has PondBing Manager %s'%(self.pond.getPondBingoManager().getDoId()))

            bucket = self.castGui.find("**/bucket")
            self.castGui.find("**/display_bucket").reparentTo(bucket)
            self.bucket.reparentTo(bucket)

            jar = self.castGui.find("**/jar")
            self.castGui.find("**/display_jar").reparentTo(jar)
            self.jar.reparentTo(jar)

            base.setCellsAvailable(base.rightCells, 0)
            
            bucket.setScale(0.9)
            bucket.setX(-1.9)
            bucket.setZ(-.11)

            jar.setScale(0.9)
            jar.setX(-.375)
            jar.setZ(-.135)
        else:
            self.notify.debug('__setItemFramePos: Has No Pond Bingo Manager')

            # need to reset the positions and scales
            bucket = self.castGui.find("**/bucket")
            bucket.setScale(1)
            bucket.setPos(0,0,0)
            
            jar = self.castGui.find("**/jar")
            jar.setScale(1)
            jar.setPos(0,0,0)
            

    ############################################################
    # Method: resetCastGui
    # Purpose: This method resets the jar and bucket positions
    #          and scaling via an interval. When bingo night
    #          starts, the bucket moves to the left of the
    #          screen. So when bingo night ends, we must move
    #          the bucket back to its original position.
    #
    #          This sequence is done in the event that a toon
    #          continues to fish at a spot after it ends so
    #          we must gracefully reset the positions and scaling
    #          of the bucket and jar.
    # Input: None
    # Output: None
    ############################################################
    def resetCastGui(self):
        self.notify.debug('resetCastGui: Bingo Night Ends - resetting Gui')
        bucket = self.castGui.find("**/bucket")
        jar = self.castGui.find("**/jar")

        bucketPosInt = bucket.posInterval(5.0, Point3(0,0,0), startPos=bucket.getPos(), blendType='easeInOut')
        bucketScaleInt = bucket.scaleInterval(5.0, VBase3(1.0, 1.0, 1.0), startScale=bucket.getScale(), blendType='easeInOut')
        bucketTrack = Parallel( bucketPosInt, bucketScaleInt )

        jarPosInt = jar.posInterval(5.0, Point3(0,0,0), startPos=jar.getPos(), blendType='easeInOut')
        jarScaleInt = jar.scaleInterval(5.0, VBase3(1.0, 1.0, 1.0), startScale=jar.getScale(), blendType='easeInOut')
        jarTrack = Parallel( jarPosInt, jarScaleInt )

        self.guiTrack = Parallel( bucketTrack, jarTrack )
        self.guiTrack.start()

    ############################################################
    # Method: setCastGui
    # Purpose: This method creates and plays an interval for
    #          moving the cast gui to its appropriate position
    #          for Bingo Night. Originally, bucket is on the
    #          far right of the screen, but we move it to the
    #          far left as well as nudget he jar over a little
    #          too.
    #
    #          This sequence is done in the event that a toon
    #          is already fishing at a spot so we must gracefully
    #          change the positions of the jar and bucket.
    # Input: None
    # Output: None
    ############################################################
    def setCastGui(self):
        self.notify.debug('setCastGui: Bingo Night Starts - setting Gui')

        # Should probably do this up in __makeGui. Would reduce redundant code.
        # TODO: Move this up to the __makeGui.
        bucket = self.castGui.find("**/bucket")
        self.castGui.find("**/display_bucket").reparentTo(bucket)
        self.bucket.reparentTo(bucket)

        jar = self.castGui.find("**/jar")
        self.castGui.find("**/display_jar").reparentTo(jar)
        self.jar.reparentTo(jar)

        # Set up track
        bucketPosInt = bucket.posInterval(3.0, Point3(-1.9,0,-.11), startPos=bucket.getPos(), blendType='easeInOut')
        bucketScaleInt = bucket.scaleInterval(3.0, VBase3(0.9, 0.9, 0.9), startScale=bucket.getScale(), blendType='easeInOut')
        bucketTrack = Parallel( bucketPosInt, bucketScaleInt )

        jarPosInt = jar.posInterval(3.0, Point3(-.375, 0, -.135), startPos=jar.getPos(), blendType='easeInOut')
        jarScaleInt = jar.scaleInterval(3.0, VBase3(0.9, 0.9, 0.9), startScale=jar.getScale(), blendType='easeInOut')
        jarTrack = Parallel( jarPosInt, jarScaleInt )

        self.guiTrack = Parallel( bucketTrack, jarTrack )
        self.guiTrack.start()
    
    ############################################################
    # Method: setJarAmount
    # Purpose: This method sets the new jellybean count.
    # Input: amount - amount to increase current count by.
    # Output: None
    ############################################################
    def setJarAmount(self, amount):
        if self.madeGui:
            money = int(self.jar['text']) + amount
            pocketMoney = min(money, self.av.getMaxMoney())
            self.jar.setProp('text', str(pocketMoney))        

    def __unmakeGui(self):
        assert self.notify.debugStateCall(self)
        if not self.madeGui:
            return
        self.timer.destroy()
        del self.timer
        self.exitButton.destroy()
        self.castButton.destroy()
        self.jar.destroy()
        self.bucket.destroy()
        self.itemFrame.destroy()
        self.itemGui.removeNode()
        self.failureDialog.cleanup()
        self.sellFishDialog.cleanup()
        self.sellFishConfirmDialog.cleanup()
        self.brokeDialog.cleanup()
        self.howToDialog.cleanup()
        self.castGui.removeNode()
        self.madeGui = 0        

    def localAdjustingCastTask(self, state):
        assert self.notify.debugStateCall(self)
        # Get the latest mouse values for this frame
        self.getMouse()
        deltaX = self.mouseX - self.initMouseX
        deltaY = self.mouseY - self.initMouseY

        # If we are above the cast button, basically do nothing - hold still
        # You must pull down from the cast button
        if deltaY >= 0:
            if self.power == 0:
                self.arrowTail.setScale(0.075,0.075,0)
                self.arrow.setR(0)
            self.castTrack.pause()
            return Task.cont

        # Calculate the power based on how far back we have pulled the mouse
        dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        delta = (dist/0.5)
        self.power = max(min(abs(delta), 1.0), 0.0)
        
        # Based on the current power reading, pull the rod back
        # This is done by setting the T value of the track containing
        # that animation
        self.castTrack.setT(0.2 + self.power * 0.7)
        
        # Calculate the angle we are casting at
        angle = rad2Deg(math.atan(deltaX/deltaY))
        if self.power < 0.25:
            angle = angle * math.pow((self.power * 4), 3)
        if delta < 0:
            angle += 180

        # Clamp the angle and update the arrow color
        # This also updates the gui arrow if we are clamping
        minAngle = -FishGlobals.FishingAngleMax
        maxAngle = FishGlobals.FishingAngleMax
        if angle < minAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = minAngle
        elif angle > maxAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = maxAngle
        else:
            self.arrow.setColorScale(1, 1 - math.pow(self.power, 3), 0.1, 0.7)
            
        # Scale the arrow tale based on the power so it looks like you
        # are pulling the arrow out of the cast button
        self.arrowTail.setScale(0.075,0.075,self.power*0.2)
        # Also turn the arrow based on our current angle
        self.arrow.setR(angle)

        # Actually turn the avatar to the angle
        self.angleNP.setH(-angle)

        # Come back next frame
        return Task.cont

    def localAdjustingCastTaskIndAxes(self, state):
        assert self.notify.debugStateCall(self)
        self.getMouse()
        deltaX = self.mouseX - self.initMouseX
        deltaY = self.mouseY - self.initMouseY
        self.power = max(min(abs(deltaY) * 1.5, 1.0), 0.0)
        self.castTrack.setT(0.4 + self.power * 0.5)
        angle = deltaX * -180.0
        self.angleNP.setH(self.startAngleNP - angle)
        return Task.cont
        
    def getMouse(self):
        assert self.notify.debugStateCall(self)
        if (base.mouseWatcherNode.hasMouse()):
            self.mouseX = base.mouseWatcherNode.getMouseX()
            self.mouseY = base.mouseWatcherNode.getMouseY()
        else:
            self.mouseX = 0
            self.mouseY = 0

    def createCastTrack(self):
        assert self.notify.debugStateCall(self)
        self.castTrack = Sequence(ActorInterval(self.av, 'castlong', playRate=4),
                                  ActorInterval(self.av, 'cast', startFrame=20),
                                  Func(self.av.loop, 'fish-neutral'),
                                  )

    def startMoveBobTask(self):
        assert self.notify.debugStateCall(self)
        self.__showBob()
        taskMgr.add(self.moveBobTask, self.taskName('moveBobTask'))

    def moveBobTask(self, task):
        assert self.notify.debugStateCall(self)
        # Accel due to gravity
        g = 32.2
        # Elapsed time of cast
        t = task.time
        # Scale bob velocity and angle based on power of cast
        vZero = self.power * self.vZeroMax
        angle = deg2Rad(self.power * self.angleMax)
        # How far has bob moved from start point?
        deltaY = vZero * math.cos(angle) * t
        deltaZ = vZero * math.sin(angle) * t - (g * t * t)/2.0
        deltaPos = Point3(0, deltaY, deltaZ)
        # Current bob position
        self.bobStartPos = Point3(0.0, 3.0, 8.5)
        pos = self.bobStartPos + deltaPos
        self.bob.setPos(pos)
        # Have we reached end condition?
        if pos[2] < self.waterLevel:
            self.fsm.request("fishing")
            return Task.done
        else:
            return Task.cont

    def __showBob(self):
        assert self.notify.debugStateCall(self)
        self.__hideBob()
        self.bob.reparentTo(self.angleNP)
        self.bob.setPos(self.ptop, 0,0,0)
        self.av.update(0)

    def hitTarget(self):
        assert self.notify.debugStateCall(self)
        # This is called from the pond to let us know we found something
        # And we are going to try to pull it in
        assert(self.notify.debug("hitTarget"))
        self.fsm.request("waitForAI")

    def enterOff(self):
        assert self.notify.debugStateCall(self)
        pass
    
    def exitOff(self):
        assert self.notify.debugStateCall(self)
        pass

    def enterWaiting(self, doAnimation = True):
        assert self.notify.debugStateCall(self)
        self.av.stopLookAround()
        self.__hideLine()
        # The avatar walks up to the fishing spot and gets out his pole.
        self.track = Parallel()

        if doAnimation:
            # Create a sequence that runs us to the spot and takes out our pole
            toonTrack = Sequence(
                Func(self.av.setPlayRate, 1.0, "run"),
                Func(self.av.loop, 'run'),
                LerpPosHprInterval(self.av, 1.0,
                                   Point3(0, 0, 0),
                                   Point3(0, 0, 0)),
                # Bring out the fishing pole.
                Func(self.__placeAvatar),
                Parallel(ActorInterval(self.av, 'pole'),
                         Func(self.pole.pose, 'cast', 0),
                         LerpScaleInterval(self.pole,
                                           duration = 0.5,
                                           scale = 1.0,
                                           startScale = 0.01)
                         ),
                Func(self.av.loop, 'pole-neutral'),
                )

            if self.localToonFishing:
                # Move the camera to a suitable location to observe
                # the fishing. (runs parallel to toonTrack
                camera.wrtReparentTo(render)
                self.track.append(
                    LerpPosHprInterval(
                        nodePath=camera,
                        other=self.av,
                        duration=1.5,
                        pos=Point3(0, -12, 15),
                        # pos=Point3(0, -14, 14),
                        hpr=VBase3(0, -38, 0),
                        blendType="easeInOut"))
                # Pop up the gui when we've reached the fishing spot.
                toonTrack.append(Func(self.__showCastGui))
                toonTrack.append(Func(self.__initCastGui))
                if base.wantBingo:
                    self.__appendBingoMethod(toonTrack, self.pond.showBingoGui)

            self.track.append(toonTrack)
        else:
            self.__showCastGui()
        self.track.start()

    ############################################################
    # Method: __appendBingoMethod
    # Purpose: This method appends a Bingo related method to an
    #          existing interval.
    # Input: interval - the interval to append the method.
    #        callback - the method that will be called by the
    #                   interval.
    # Output: None
    ############################################################
    def __appendBingoMethod(self, interval, callback):
        interval.append(Func(callback))
    
    def exitWaiting(self):
        assert self.notify.debugStateCall(self)
        self.track.finish()
        self.track = None

    def enterLocalAdjusting(self, guiEvent=None):
        assert self.notify.debugStateCall(self)
        if self.track:
            self.track.pause()
        if self.castTrack:
            self.castTrack.pause()
        self.power = 0.0
        self.firstCast = 0
        self.castButton['image0_color'] = Vec4(0, 1, 0, 1)
        self.castButton['text'] = ""
        self.av.stopLookAround()
        self.__hideLine()
        self.__hideBob()
        self.howToDialog.hide()
        # make sure we can afford to fish
        castCost = FishGlobals.getCastCost(self.av.getFishingRod())
        if self.av.getMoney() < castCost:
            self.__hideCastGui()
            self.__showBroke()
            self.av.loop('pole-neutral')
            return
        if self.av.isFishTankFull():
            self.__hideCastGui()
            self.__showFishTankFull()
            self.av.loop('pole-neutral')
            return
        # Start task to adjust power of cast
        self.arrow.show()
        self.arrow.setColorScale(1,1,0,0.7)
        self.startAngleNP = self.angleNP.getH()
        self.getMouse()
        self.initMouseX = self.mouseX
        self.initMouseY = self.mouseY
        self.__hideBob()
        if config.GetBool('fishing-independent-axes', 0):
            taskMgr.add(self.localAdjustingCastTaskIndAxes, self.taskName('adjustCastTask'))
        else:
            taskMgr.add(self.localAdjustingCastTask, self.taskName('adjustCastTask'))

        #tell the bingo gui that a cast has begun... this is used for the tutorial
        if base.wantBingo:
            bingoMgr = self.pond.getPondBingoManager()
            if bingoMgr:
                bingoMgr.castingStarted()

    def exitLocalAdjusting(self):
        assert self.notify.debugStateCall(self)
        taskMgr.remove(self.taskName('adjustCastTask'))
        self.castButton['image0_color'] = Vec4(1, 0, 0, 1)
        self.castButton['text'] = TTLocalizer.FishingCast
        self.arrow.hide()

    def enterLocalCasting(self):
        assert self.notify.debugStateCall(self)
        assert(self.localToonFishing)
        # If the cast without any power, and they do not have any fish in
        # their collection, they probably do not know how to use the
        # interface.
        if ((self.power == 0.0) and (len(self.av.fishCollection) == 0)):
            self.__showHowTo(TTLocalizer.FishingHowToFailed)
            if self.castTrack:
                self.castTrack.pause()
            self.av.loop('pole-neutral')
            self.track = None
            return
            
        # Subtract money from jellybean jar gui (the AI does the real work)
        castCost = FishGlobals.getCastCost(self.av.getFishingRod())
        self.jar['text'] = str(max(self.av.getMoney() - castCost, 0))
        if not self.castTrack:
            self.createCastTrack()
        self.castTrack.pause()
        startT = 0.7 + (1 - self.power) * 0.3
        self.castTrack.start(startT)
        self.track = Sequence(Wait(1.2 - startT),
                              Func(self.startMoveBobTask),
                              Func(self.__showLineCasting),
                              )
        self.track.start()
        # Tell the AI we are casting now
        heading = self.angleNP.getH()
        self.d_doCast(self.power, heading)
        self.timer.countdown(FishGlobals.CastTimeout)

    def exitLocalCasting(self):
        assert self.notify.debugStateCall(self)
        taskMgr.remove(self.taskName('moveBobTask'))
        if self.track:
            self.track.pause()
            self.track = None
        if self.castTrack:
            self.castTrack.pause()
        self.__hideLine()
        self.__hideBob()
    
    def enterDistCasting(self, power, h):
        assert self.notify.debugStateCall(self)
        assert(not self.localToonFishing)
        self.av.stopLookAround()
        self.__placeAvatar()
        self.__hideLine()
        self.__hideBob()
        self.angleNP.setH(h)
        self.power = power
        self.track = Parallel(
            Sequence(ActorInterval(self.av, 'cast'),
                     Func(self.pole.pose, 'cast', 0),
                     Func(self.av.loop, 'fish-neutral'),
                     ),
            Sequence(Wait(1.0),
                     Func(self.startMoveBobTask),
                     Func(self.__showLineCasting),
                     ),
            )
        self.track.start()

    def exitDistCasting(self):
        assert self.notify.debugStateCall(self)
        self.track.finish()
        self.track = None
        taskMgr.remove(self.taskName('moveBobTask'))
        self.__hideLine()
        self.__hideBob()

    def enterFishing(self):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.track = Sequence(ActorInterval(self.av, 'cast'),
                                  Func(self.pole.pose, 'cast', 0),
                                  Func(self.av.loop, 'fish-neutral'),
                                  )
            self.track.start(self.castTrack.getT())
        else:
            self.track = None
            self.av.loop('fish-neutral')
        self.__showBobFloat()
        self.__showLineWaiting()
        if self.localToonFishing:
            self.pond.startCheckingTargets(self, self.bob.getPos(render))

    def exitFishing(self):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.pond.stopCheckingTargets()
        if self.track:
            self.track.finish()
            self.track = None

    def enterWaitForAI(self):
        assert self.notify.debugStateCall(self)
        # While we are waiting to hear back from the AI, you are not
        # allowed to fish again. This would cause too many tricky timing
        # conditions
        self.castButton['state'] = DGG.DISABLED

    def exitWaitForAI(self):
        assert self.notify.debugStateCall(self)
        self.castButton['state'] = DGG.NORMAL

    def enterReward(self, code, itemDesc1, itemDesc2, itemDesc3):
        assert self.notify.debugStateCall(self)
        self.__placeAvatar()
        self.bob.reparentTo(self.angleNP)
        self.bob.setZ(self.waterLevel)
        self.__showLineReeling()
        self.castTrack.pause()
        if self.localToonFishing:
            # Switch guis.
            self.__showCastGui()
            if code == FishGlobals.QuestItem:
                self.__showQuestItem(itemDesc1)
            elif code in (FishGlobals.FishItem,
                          FishGlobals.FishItemNewEntry,
                          FishGlobals.FishItemNewRecord,):
                genus, species, weight = itemDesc1, itemDesc2, itemDesc3
                fish = FishBase.FishBase(genus, species, weight)
                self.__showFishItem(code, fish)
                if base.wantBingo:
                    self.pond.handleBingoCatch((genus, species))
            elif code == FishGlobals.BootItem:
                # TODO: play sfx
                self.__showBootItem()
                if base.wantBingo:
                    self.pond.handleBingoCatch(FishGlobals.BingoBoot)
            elif code == FishGlobals.JellybeanItem:
                # TODO: play sfx
                amount = itemDesc1
                self.__showJellybeanItem(amount)
            elif code == FishGlobals.OverTankLimit:
                self.__hideCastGui()
            else:
                self.__showFailureReason(code)
        self.track = Sequence(
            Parallel(ActorInterval(self.av, 'reel'),
                     ActorInterval(self.pole, 'cast', startFrame=63, endFrame=127),
                     ),
            ActorInterval(self.av, 'reel-neutral'),
            Func(self.__hideLine),
            Func(self.__hideBob),
            ActorInterval(self.av, 'fish-again'),
            Func(self.av.loop, 'pole-neutral'),
            )
        self.track.start()

    def cleanupFishPanel(self):
        if self.fishPanel:
            self.fishPanel.hide()
            self.fishPanel.destroy()
            self.fishPanel = None
        
    def hideBootPanel(self):
        if self.madeGui and self.itemBoot:
            self.__itemGuiClose()
        
    def exitReward(self):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.itemGui.detachNode()
            self.cleanupFishPanel()
        self.track.finish()
        self.track = None

    def enterLeaving(self):
        assert self.notify.debugStateCall(self)
        if self.localToonFishing:
            self.__hideCastGui()
            if base.wantBingo:
                self.pond.cleanupBingoMgr()
        self.av.stopLookAround()
        self.av.startLookAround()
        self.__placeAvatar()
        self.__hideLine()
        self.__hideBob()
        self.track = Sequence(
            Parallel(ActorInterval(self.av, 'fish-end'),
                     Func(self.pole.pose, 'cast', 0),
                     LerpScaleInterval(self.pole,
                                       duration = 0.5,
                                       scale = 0.01,
                                       startScale = 1.0),
                     ),
            Func(self.__dropPole),
            Func(self.av.loop, 'neutral'),
            )
        if self.localToonFishing:
            self.track.append(Func(self.fsm.requestFinalState))
        self.track.start()
        
    def exitLeaving(self):
        assert self.notify.debugStateCall(self)
        self.track.pause()
        self.track = None

    def enterSellFish(self):
        assert self.notify.debugStateCall(self)
        self.castButton['state'] = DGG.DISABLED
        self.__showSellFishDialog()
        self.__hideHowTo()

    def exitSellFish(self):
        assert self.notify.debugStateCall(self)
        self.castButton['state'] = DGG.NORMAL
        self.__hideSellFishDialog()
        self.__hideSellFishConfirmDialog()

    # message from the ai telling us the sale is completed
    def sellFishComplete(self, trophyResult, numFishCaught):
        for button in self.sellFishDialog.buttonList:
            button['state'] = DGG.NORMAL

        if self.localToonFishing:
            if trophyResult:
                # congratulate toon
                self.__hideSellFishDialog()
                self.__showSellFishConfirmDialog(numFishCaught)
            else:
                self.fsm.request("waiting", [False])

    def __allowSellFish(self):
        if base.wantBingo:
            if self.pond.hasPondBingoManager():
                hoodId = base.cr.playGame.getPlaceId()
                if hoodId == ToontownGlobals.MyEstate:
                    return True
        return False
        
