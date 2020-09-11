from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject
from toontown.toon import ToonDNA
from direct.fsm import ClassicFSM, State, StateData
import ClosetGUI
from direct.task.Task import Task
import ClosetGlobals
import DistributedFurnitureItem
from toontown.toonbase import TTLocalizer

class DistributedCloset(DistributedFurnitureItem.DistributedFurnitureItem):
    # DistributedCloset class: handles all the distributed aspects of a closet,
    # such as setting the toons DNA, deciding whether a friend can try on your
    # clothes, etc.
    notify = directNotify.newCategory("DistributedCloset")

    def __init__(self, cr):
        DistributedFurnitureItem.DistributedFurnitureItem.__init__(self, cr)
        self.notify.debug("__init__")
        self.lastAvId = 0
        self.hasLocalAvatar = 0
        self.lastTime = 0
        self.av = None
        self.closetGUI = None
        self.closetModel = None
        self.closetSphere = None
        self.closetSphereNode = None
        self.closetSphereNodePath = None
        self.topList = []
        self.botList = []
        self.oldTopList = []
        self.oldBotList = []
        self.oldStyle = None
        self.button = None
        self.topTrashButton = None
        self.bottomTrashButton = None
        self.isLocalToon = None
        self.popupInfo = None
        self.isOwner = 0
        self.ownerId = 0
        self.customerId = 0
        self.purchaseDoneEvent = ""
        self.swapEvent = ""
        self.locked = 0
        self.gender = None
        self.topDeleted = 0
        self.bottomDeleted = 0
        self.closetTrack = None
        self.avMoveTrack = None
        self.scale = 1.0
        self.fsm = ClassicFSM.ClassicFSM('Closet',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['ready', 'open','closed',]),
                            State.State('ready',
                                        self.enterReady,
                                        self.exitReady,
                                        ['open','closed',]),
                            State.State('closed',
                                        self.enterClosed,
                                        self.exitClosed,
                                        ['open','off']),
                            State.State('open',
                                        self.enterOpen,
                                        self.exitOpen,
                                        ['closed','off'])],
                            # Initial State
                            'off',
                            # Final State
                            'off',
                           )
        self.fsm.enterInitialState()

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedFurnitureItem.DistributedFurnitureItem.generate(self)
        
    def announceGenerate(self):
        self.notify.debug("announceGenerate")
        DistributedFurnitureItem.DistributedFurnitureItem.announceGenerate(self)        
        # This is called when the closet is completely created, so we know
        # that we have all the info we need to get a proper trigger event.

        # listen for closet collision event
        # for now the DistributedHouseInterior manually sets up the collision
        # sphere for the closet.  SDN: remove that code when we have the closet model
        self.load()
        self.setupCollisionSphere()
        self.fsm.request("ready")

    def load(self):
        # Temporary hack around lack of a double-sided flag in Maya.
        # Remove this when the models are fixed.
        self.setTwoSided(1)
        
        # reparent the doors to the rotate nodes
        lNode = self.find("**/door_rotate_L")
        lDoor = self.find("**/closetdoor_L")
        if lNode.isEmpty() or lDoor.isEmpty():
            self.leftDoor = None
        else:
            lDoor.wrtReparentTo(lNode)
            self.leftDoor = lNode
        
        rNode = self.find("**/door_rotate_R")
        rDoor = self.find("**/closetdoor_R")
        if rNode.isEmpty() or rDoor.isEmpty():
            self.rightDoor = None
        else:
            rDoor.wrtReparentTo(rNode)
            self.rightDoor = rNode

        # determine scale of closet so we can make the appropriate size trigger sphere
        if not lNode.isEmpty():
            self.scale = lNode.getScale()[0]
            
    def setupCollisionSphere(self):
        if self.ownerId:
            # Establish a collision sphere. 
            self.closetSphereEvent = self.uniqueName("closetSphere")
            self.closetSphereEnterEvent = "enter"+self.closetSphereEvent
            # we need to make a bigger trigger sphere for the 15 item closet
            self.closetSphere = CollisionSphere(0, 0, 0, self.scale * 2.125)
            self.closetSphere.setTangible(0)
            self.closetSphereNode = CollisionNode(self.closetSphereEvent)
            self.closetSphereNode.setIntoCollideMask(WallBitmask)
            self.closetSphereNode.addSolid(self.closetSphere)
            self.closetSphereNodePath = self.attachNewNode(
                self.closetSphereNode)
        
    def disable(self):
        self.notify.debug("disable")
        self.ignore(self.closetSphereEnterEvent)
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupChangeClothesGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        taskMgr.remove(self.uniqueName('lerpToon'))
        if self.closetTrack:
            self.closetTrack.finish()
            self.closetTrack = None
        if self.closetGUI:
            self.closetGUI.resetClothes(self.oldStyle)
            self.resetCloset()
        if self.hasLocalAvatar:
            self.freeAvatar()
        self.ignoreAll()
        DistributedFurnitureItem.DistributedFurnitureItem.disable(self)

    def delete(self):
        self.notify.debug("delete")
        DistributedFurnitureItem.DistributedFurnitureItem.delete(self)
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.av:
            del self.av
        del self.gender
        del self.closetSphere
        del self.closetSphereNode
        del self.closetSphereNodePath
        del self.closetGUI
        del self.fsm
        
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterReady(self):
        if self.ownerId:
            self.accept(self.closetSphereEnterEvent,  self.handleEnterSphere)

    def exitReady(self):
        pass

    def enterOpen(self):
        # swing the doors open
        if self.ownerId:
            self.ignore(self.closetSphereEnterEvent)
            self.__openDoors()
            
            if self.customerId == base.localAvatar.doId:
                # move camera to the back left
                camera.wrtReparentTo(self)
                camera.lerpPosHpr(
                    -7.58, -6.02, 6.90, 286.3, 336.8, 0, 1,
                    #other=render,
                    other = self,
                    blendType="easeOut",
                    task=self.uniqueName('lerpCamera'))
                camera.setPosHpr(
                    self,
                    -7.58, -6.02, 6.90, 286.3, 336.8, 0)
                
            # Move the avatar:
            if self.av:
                if self.avMoveTrack:
                    self.avMoveTrack.finish()
                self.av.stopSmooth()
                self.avMoveTrack = Sequence(Parallel(Func(self.av.play, 'walk'),
                                                     LerpPosHprInterval(nodePath=self.av,
                                                                        other=self,
                                                                        duration=1.0,
                                                                        pos=Vec3(1.67, -3.29, 0.025),
                                                                        hpr=Vec3(112, 0, 0),
                                                                        blendType="easeOut")),
                                            Func(self.av.loop, 'neutral'),
                                            Func(self.av.startSmooth),
                                            )
                                            
                self.avMoveTrack.start()

    def exitOpen(self):
        # swing the doors closed
        if self.ownerId:
            self.__closeDoors()

    def enterClosed(self):
        if self.ownerId:
            self.accept(self.closetSphereEnterEvent,  self.handleEnterSphere)

    def exitClosed(self):
        pass
    
    def handleEnterSphere(self, collEntry):
        if self.smoothStarted:
            # Ignore any sphere enter events while the object is
            # moving around.  It doesn't count if someone moves the
            # object into an avatar!
            return

        # If the same toon re-enters immediately after exiting, it's
        # probably a mistake; ignore it.
        if base.localAvatar.doId == self.lastAvId and \
           globalClock.getFrameTime() <= self.lastTime + 0.5:
            self.notify.info("Ignoring duplicate entry for avatar.")
            return

        if self.hasLocalAvatar:
            self.freeAvatar()
        
        self.notify.debug("Entering Closet Sphere....%s" % self.closetSphereEnterEvent)

        if self.cr.playGame.getPlace() == None:
            # If we don't have a place yet, we can't open the closet,
            # so don't try.
            self.notify.info("Not opening closet before place is defined.")
            return

        # don't let other toons open the closet now,
        # this will help handle the case when two toons hit the sphere
        # at the same time
        self.ignore(self.closetSphereEnterEvent)


        # Test for restrictions.  Concievably, someday the user
        # can lock their closet.  For now self.locked == 0
        if not self.locked:
            # Tell the server
            self.cr.playGame.getPlace().fsm.request('closet')
            self.accept("closetAsleep", self.__handleCancel)
            self.sendUpdate("enterAvatar", [])
            self.hasLocalAvatar = 1
        else: # not our own house
            # is it safe to just ignore this message?
            pass

    def setState(self, mode,
                 avId, ownerId,
                 gender,
                 topList, botList):
        self.notify.debug("setState, mode=%s, avId=%s, ownerId=%d" % (mode, avId, ownerId))
        self.isOwner = (avId == ownerId)
        self.ownerGender = gender
        
        if mode == ClosetGlobals.CLOSED:
            # the closet is closed, do nothing
            self.fsm.request('closed')
            return
        elif mode == ClosetGlobals.OPEN:
            self.customerId = avId
            self.av = self.cr.doId2do.get(self.customerId, None)
            if self.av:
                if (base.localAvatar.getDoId() == self.customerId):

                    # popup the interface if we are the local toon
                    self.gender = self.av.style.gender
                    self.topList = topList
                    self.botList = botList
                    # save a copy of these lists
                    self.oldTopList = self.topList[0:]
                    self.oldBotList = self.botList[0:]

                    # print out our clothes and closet information before we start
                    print ("-----------Starting closet interaction-----------")
                    print "customerId: %s, gender: %s, ownerId: %s" % (self.av.doId, self.av.style.gender, ownerId)
                    print "current top = %s,%s,%s,%s and  bot = %s,%s," % (self.av.style.topTex, self.av.style.topTexColor,
                                                                           self.av.style.sleeveTex, self.av.style.sleeveTexColor,
                                                                           self.av.style.botTex, self.av.style.botTexColor)
                    print "topsList = %s" % self.av.getClothesTopsList()
                    print "bottomsList = %s" % self.av.getClothesBottomsList()
                    print ("-------------------------------------------------")
                    
                    if not self.isOwner:
                        # first popup a panel explaining that
                        # you aren't the owner of the closet
                        self.__popupNotOwnerPanel()
                    else:
                        taskMgr.doMethodLater(.5, self.popupChangeClothesGUI,
                                              self.uniqueName('popupChangeClothesGUI'))
                self.fsm.request('open')


    def __revertGender(self):
        #self.av.swapToonTorso(self.oldTorso)
        if self.gender:
            self.av.style.gender = self.gender
            self.av.loop('neutral')

    def popupChangeClothesGUI(self, task):
        self.notify.debug("popupChangeClothesGUI")
        # this task only gets called if we are the local toon

        #self.setChatAbsolute('', CFSpeech)
        self.purchaseDoneEvent = self.uniqueName('purchaseDone')
        self.swapEvent = self.uniqueName('swap')
        self.cancelEvent = self.uniqueName('cancel')
        self.accept(self.purchaseDoneEvent, self.__proceedToCheckout)
        self.accept(self.swapEvent, self.__handleSwap)
        self.accept(self.cancelEvent, self.__handleCancel)
        # special buttons if we own the closet
        self.deleteEvent = self.uniqueName('delete')
        if (self.isOwner):
            self.accept(self.deleteEvent, self.__handleDelete)
        
        if not self.closetGUI:
            self.closetGUI = ClosetGUI.ClosetGUI(self.isOwner,
                                                 self.purchaseDoneEvent, self.cancelEvent,
                                                 self.swapEvent, self.deleteEvent,
                                                 self.topList, self.botList)
            self.closetGUI.load()
            if (self.gender != self.ownerGender):
                self.closetGUI.setGender(self.ownerGender)
            self.closetGUI.enter(base.localAvatar)
            self.closetGUI.showButtons()
    
            # save old clothes so we can revert back
            style = self.av.getStyle()
            self.oldStyle = ToonDNA.ToonDNA()
            self.oldStyle.makeFromNetString(style.makeNetString())
        
        return Task.done

    def resetCloset(self):
        assert(self.notify.debug('resetCloset'))
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupChangeClothesGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        taskMgr.remove(self.uniqueName('lerpToon'))
        if self.closetGUI:
            self.closetGUI.hideButtons()
            self.closetGUI.exit()
            self.closetGUI.unload()
            self.closetGUI = None
            del self.av

        # save old clothes
        self.av = base.localAvatar
        style = self.av.getStyle()
        self.oldStyle = ToonDNA.ToonDNA()
        self.oldStyle.makeFromNetString(style.makeNetString())
        self.topDeleted = 0
        self.bottomDeleted = 0
        
        return Task.done

    def __handleButton(self):
        messenger.send('next')

    def __handleCancel(self):
        if self.oldStyle:
            self.d_setDNA(self.oldStyle.makeNetString(), 1)
        else:
            self.notify.info('avoided crash in handleCancel')
            self.__handlePurchaseDone()           
        if self.closetGUI:
            self.closetGUI.resetClothes(self.oldStyle)

        # get rid of the popupinfo if it exists
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
        
    def __handleSwap(self):
        self.d_setDNA(self.av.getStyle().makeNetString(), 0)

    def __handleDelete(self, t_or_b):
        # Delete the current set of clothes, and put us in our
        # original clothes (when we walked up to the closet).
        # If we are deleting what we were originally wearing, put 
        # the toon in the next set of clothes.

        if t_or_b == ClosetGlobals.SHIRT:
            itemList = self.closetGUI.tops
            trashIndex = self.closetGUI.topChoice
            swapFunc = self.closetGUI.swapTop
            removeFunc = self.closetGUI.removeTop
            self.topDeleted = self.topDeleted | 1
            def setItemChoice(i):
                self.closetGUI.topChoice = i
        else:
            itemList = self.closetGUI.bottoms
            trashIndex = self.closetGUI.bottomChoice
            swapFunc = self.closetGUI.swapBottom
            removeFunc = self.closetGUI.removeBottom
            self.bottomDeleted = self.bottomDeleted | 1
            def setItemChoice(i):
                self.closetGUI.bottomChoice = i

        # First check that we have some replacement clothes:
        if len(itemList) > 1:
            # trashed clothes
            # our currently selected clothes
            trashDNA = ToonDNA.ToonDNA()
            trashItem = self.av.getStyle().makeNetString() 
            trashDNA.makeFromNetString(trashItem)
            if trashIndex == 0:
                # put on next item
                swapFunc(1)
            else:
                # put on prev item
                swapFunc(-1)
                
            # remove item from local list
            removeFunc(trashIndex)
            # remove from server's list
            self.sendUpdate("removeItem", [trashItem, t_or_b])
            
            # update the scrollbuttons
            swapFunc(0)
            self.closetGUI.updateTrashButtons()
        else:
            self.notify.warning("cant delete this item(type = %s), since we don't have a replacement" % t_or_b)


    def resetItemLists(self):
        # called by the AI:
        # revert tops and bottoms lists back to original state
        # (means a delete has been cancelled)
        self.topList = self.oldTopList[0:]
        self.botList = self.oldBotList[0:]
        self.closetGUI.tops = self.topList
        self.closetGUI.bottoms = self.botList
        self.topDeleted = 0
        self.bottomDeleted = 0

    def __proceedToCheckout(self):
        assert(self.notify.debug('proceedToCheckout()'))
        # This functions sole purpose is to warn the user that
        # he has deleted some clothes, and ask if he's sure
        # he want's to permanently delete them.  If no clothes
        # have been deleted, pass through
        if (self.topDeleted or self.bottomDeleted):
            self.__popupAreYouSurePanel()
        else:
            self.__handlePurchaseDone()
        
        
    def __handlePurchaseDone(self, timeout = 0):
        """
        This is the callback from the Purchase object
        Cleanup the gui and send the message to the AI
        """
        assert(self.notify.debug('handlePurchaseDone()'))
        if (timeout == 1):
            # The client really does not need to send the DNA here
            # since the server is keeping track of it
            self.d_setDNA(self.oldStyle.makeNetString(), 1)
        else:
            # The client really does not need to send the DNA here
            # since the server is keeping track of it

            # Check if we ever changed the shorts or shirt
            # create a bit string that identifies which items
            # have been changed
            # bit 0 = shirts
            # bit 1 = shorts
            # bit 2...unused
            
            which = 0
            if hasattr(self.closetGUI, 'topChoice') and hasattr(self.closetGUI, 'bottomChoice'):
                if self.closetGUI.topChoice != 0 or self.topDeleted:
                    which = which | 0x1
                if self.closetGUI.bottomChoice != 0 or self.bottomDeleted:
                    which = which | 0x2
            self.d_setDNA(self.av.getStyle().makeNetString(), 2, which)

    def d_setDNA(self, dnaString, finished, whichItems=3):
        # Report our DNA to the server
        self.sendUpdate('setDNA', [dnaString, finished, whichItems])

    def setCustomerDNA(self, avId, dnaString):
        assert(self.notify.debug("setCustomerDNA"))
        # The AI doesn't set the DNA on swaps (finished=0) anymore.
        # This is to avoid bugged clothes on AI crashes while browsing.  Now the AI
        # just tells the clients the correct DNA for the current customer
        # and lets the clients set the value directly on the distributed
        # toon. The AI will still do a DNA change on purchase.

        # the av might be gone, so check first
        if avId and avId != base.localAvatar.doId:
            av = base.cr.doId2do.get(avId, None)
            if av:
                if self.av == base.cr.doId2do[avId]:
                    self.av.style.makeFromNetString(dnaString)
                    self.av.generateToonClothes()    
            
    def setMovie(self, mode, avId, timestamp):
        # See if this is the local toon
        self.isLocalToon = (avId == base.localAvatar.doId)

        if avId != 0:
            self.lastAvId = avId
        self.lastTime = globalClock.getFrameTime()

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == ClosetGlobals.CLOSET_MOVIE_CLEAR):
            assert(self.notify.debug('CLOSET_MOVIE_CLEAR'))
            return
        elif (mode == ClosetGlobals.CLOSET_MOVIE_COMPLETE):
            assert(self.notify.debug('CLOSET_MOVIE_COMPLETE'))
            if self.isLocalToon:
                self.__revertGender()
                
                # print out our clothes and closet information before we start
                print ("-----------ending closet interaction-----------")
                print "avid: %s, gender: %s" % (self.av.doId, self.av.style.gender)
                print "current top = %s,%s,%s,%s and  bot = %s,%s," % (self.av.style.topTex, self.av.style.topTexColor,
                                                                       self.av.style.sleeveTex, self.av.style.sleeveTexColor,
                                                                       self.av.style.botTex, self.av.style.botTexColor)
                print "topsList = %s" % self.av.getClothesTopsList()
                print "bottomsList = %s" % self.av.getClothesBottomsList()
                print ("-------------------------------------------------")
                
                self.resetCloset()
                self.freeAvatar()
                return
        elif (mode == ClosetGlobals.CLOSET_MOVIE_TIMEOUT):
            assert(self.notify.debug('CLOSET_MOVIE_TIMEOUT'))
            # In case the GUI hasn't popped up yet
            taskMgr.remove(self.uniqueName('lerpCamera'))
            taskMgr.remove(self.uniqueName('lerpToon'))
            # Stop listening for the GUI
            if (self.isLocalToon):
                self.ignore(self.purchaseDoneEvent)
                self.ignore(self.swapEvent)
                # See if a button was pressed first
                if self.closetGUI:
                    self.closetGUI.resetClothes(self.oldStyle)
                    self.__handlePurchaseDone(timeout = 1)
                    self.resetCloset()
                self.__popupTimeoutPanel()
                self.freeAvatar()

    def freeAvatar(self):
        """
        This is a message from the AI used to free the avatar from
        movie mode.  It is also triggered locally by cleanup.
        """
        self.notify.debug("freeAvatar()")
        if self.hasLocalAvatar:
            base.localAvatar.posCamera(0,0)
            place = base.cr.playGame.getPlace()
            if place:
                place.setState("walk")
            self.ignore("closetAsleep")
            base.localAvatar.startLookAround()
            self.hasLocalAvatar = 0

        self.lastTime = globalClock.getFrameTime()
            
    def setOwnerId(self, avId):
        self.ownerId = avId
        
    def __popupTimeoutPanel(self):
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
        
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr'))
        # Popup a message saying why the emote entry is disabled
        self.popupInfo = DirectFrame(
            parent = hidden,
            relief = None,
            state = 'normal',
            text = TTLocalizer.ClosetTimeoutMessage,
            frameSize = (-1,1,-1,1),
            geom = DGG.getDefaultDialogGeom(),
            geom_color = ToontownGlobals.GlobalDialogColor,
            geom_scale = (.88, 1, .45),
            geom_pos = (0,0,-.08),
            text_scale = .08,
            )
        DirectButton(self.popupInfo,
                     image = okButtonImage,
                     relief = None,
                     text = TTLocalizer.ClosetPopupOK,
                     text_scale = 0.05,
                     text_pos = (0.0, -0.1),
                     textMayChange = 0,
                     pos = (0.0, 0.0, -0.16),
                     command = self.__handleTimeoutMessageOK)
        buttons.removeNode()
        
        # Show the popup info (i.e. "Sorry you ran out of time")
        self.popupInfo.reparentTo(aspect2d)
    
    def __handleTimeoutMessageOK(self):
        self.popupInfo.reparentTo(hidden)

    def __popupNotOwnerPanel(self):
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None
               
        self.purchaseDoneEvent = self.uniqueName('purchaseDone')
        self.swapEvent = self.uniqueName('swap')
        self.cancelEvent = self.uniqueName('cancel')

        self.accept(self.purchaseDoneEvent, self.__proceedToCheckout)
        self.accept(self.swapEvent, self.__handleSwap)
        # register this cancel event in case we fall asleep
        self.accept(self.cancelEvent, self.__handleCancel)
        # special buttons if we own the closet
        self.deleteEvent = self.uniqueName('delete')
        if (self.isOwner):
            self.accept(self.deleteEvent, self.__handleDelete)
                
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr'))

        self.popupInfo = DirectFrame(
            parent = hidden,
            relief = None,
            state = 'normal',
            text = TTLocalizer.ClosetNotOwnerMessage,
            frameSize = (-1,1,-1,1),
            text_wordwrap = 10,
            geom = DGG.getDefaultDialogGeom(),
            geom_color = ToontownGlobals.GlobalDialogColor,
            geom_scale = (.88, 1, .55),
            geom_pos = (0,0,-.08),
            text_scale = .08,
            text_pos = (0, 0.06),
            )
        DirectButton(self.popupInfo,
                     image = okButtonImage,
                     relief = None,
                     text = TTLocalizer.ClosetPopupOK,
                     text_scale = 0.05,
                     text_pos = (0.0, -0.1),
                     textMayChange = 0,
                     pos = (0.0, 0.0, -0.21),
                     command = self.__handleNotOwnerMessageOK)
        buttons.removeNode()
        
        # Show the popup info (i.e. "Sorry you ran out of time")
        self.popupInfo.reparentTo(aspect2d)

    def __handleNotOwnerMessageOK(self):
        self.popupInfo.reparentTo(hidden)
        taskMgr.doMethodLater(.1, self.popupChangeClothesGUI,
                              self.uniqueName('popupChangeClothesGUI'))
            

    def __popupAreYouSurePanel(self):
        # Are you sure you want to permanently delete your clothes?
        if self.popupInfo != None:
            self.popupInfo.destroy()
            self.popupInfo = None

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelButtonImage = (buttons.find('**/CloseBtn_UP'),
                             buttons.find('**/CloseBtn_DN'),
                             buttons.find('**/CloseBtn_Rllvr'))

        self.popupInfo = DirectFrame(
            parent = hidden,
            relief = None,
            state = 'normal',
            text = TTLocalizer.ClosetAreYouSureMessage,
            frameSize = (-1,1,-1,1),
            text_wordwrap = 10,
            geom = DGG.getDefaultDialogGeom(),
            geom_color = ToontownGlobals.GlobalDialogColor,
            geom_scale = (.88, 1, .55),
            geom_pos = (0,0,-.08),
            text_scale = .08,
            text_pos = (0, 0.08),
            )
        DirectButton(self.popupInfo,
                     image = okButtonImage,
                     relief = None,
                     text = TTLocalizer.ClosetPopupOK,
                     text_scale = 0.05,
                     text_pos = (0.0, -0.1),
                     textMayChange = 0,
                     pos = (-0.10, 0.0, -0.21),
                     command = self.__handleYesImSure)
        DirectButton(self.popupInfo,
                     image = cancelButtonImage,
                     relief = None,
                     text = TTLocalizer.ClosetPopupCancel,
                     text_scale = 0.05,
                     text_pos = (0.0, -0.1),
                     textMayChange = 0,
                     pos = (0.10, 0.0, -0.21),
                     command = self.__handleNotSure)
        buttons.removeNode()
        
        # Show the popup info (i.e. "Are you sure?")
        self.popupInfo.reparentTo(aspect2d)

    def __handleYesImSure(self):
        # deletion? lets do this
        self.popupInfo.reparentTo(hidden)
        self.__handlePurchaseDone()

    def __handleNotSure(self):
        # deletion? uhmm....no maybe not
        self.popupInfo.reparentTo(hidden)

    def __openDoors(self):
        if self.closetTrack:
            self.closetTrack.finish()
        leftHpr = Vec3(-110,0,0)
        rightHpr = Vec3(110,0,0)

        self.closetTrack = Parallel()
        if self.rightDoor:
            self.closetTrack.append(self.rightDoor.hprInterval(.5, rightHpr))
        if self.leftDoor:
            self.closetTrack.append(self.leftDoor.hprInterval(.5, leftHpr))
        self.closetTrack.start()

    def __closeDoors(self):
        if self.closetTrack:
            self.closetTrack.finish()
        leftHpr = Vec3(0,0,0)
        rightHpr = Vec3(0,0,0)

        self.closetTrack = Parallel()
        if self.rightDoor:
            self.closetTrack.append(self.rightDoor.hprInterval(.5, rightHpr))
        if self.leftDoor:
            self.closetTrack.append(self.leftDoor.hprInterval(.5, leftHpr))
        self.closetTrack.start()
    
