from pandac.PandaModules import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import NPCToons
from direct.task.Task import Task
import TailorClothesGUI
from toontown.toonbase import TTLocalizer
import ToonDNA
from toontown.estate import ClosetGlobals

class DistributedNPCTailor(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.clothesGUI = None
        self.av = None
        self.oldStyle = None
        self.browsing = 0
        self.roomAvailable = 0
        self.button = None
        self.popupInfo = None
            
    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.clothesGUI:
            self.clothesGUI.exit()
            self.clothesGUI.unload()
            self.clothesGUI = None
            if (self.button != None):
                self.button.destroy()
                del self.button
            self.cancelButton.destroy()
            del self.cancelButton
            del self.gui
            self.counter.show()
            del self.counter
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        self.av = None
        self.oldStyle = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        # Lock down the avatar for purchase mode
        base.cr.playGame.getPlace().fsm.request('purchase')
        # Tell the server
        self.sendUpdate("avatarEnter", [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        self.oldStyle = None

    def resetTailor(self):
        assert self.notify.debug('resetTailor')
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.clothesGUI:
            self.clothesGUI.hideButtons()
            self.clothesGUI.exit()
            self.clothesGUI.unload()
            self.clothesGUI = None
            if (self.button != None):
                self.button.destroy()
                del self.button
            self.cancelButton.destroy()
            del self.cancelButton
            del self.gui
            self.counter.show()
            del self.counter
            self.show()
        self.startLookAround()
        self.detectAvatars()
        # Reset the NPC back to original pos hpr in case he had to
        # turn all the way around to talk to the toon
        # TODO: make this a lerp
        self.clearMat()
        # If we are the local toon and we have simply taken too long
        # to read through the chat balloons, just free us
        if (self.isLocalToon):
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        """
        This is a message from the AI describing a movie between this NPC
        and a Toon that has approached us. 
        """
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp

        self.npcId = npcId

        # See if this is the local toon
        self.isLocalToon = (avId == base.localAvatar.doId)
            
        assert(self.notify.debug("setMovie: %s %s %s %s" %
                          (mode, avId, timeStamp, self.isLocalToon)))

        # This is an old movie in the server ram that has been cleared.
        # Just return and do nothing
        if (mode == NPCToons.PURCHASE_MOVIE_CLEAR):
            assert self.notify.debug('PURCHASE_MOVIE_CLEAR')
            return

        if (mode == NPCToons.PURCHASE_MOVIE_TIMEOUT):
            assert self.notify.debug('PURCHASE_MOVIE_TIMEOUT')
            # In case the GUI hasn't popped up yet
            taskMgr.remove(self.uniqueName('lerpCamera'))
            # Stop listening for the GUI
            if (self.isLocalToon):
                self.ignore(self.purchaseDoneEvent)
                self.ignore(self.swapEvent)
                # hide the popupInfo
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)
            # See if a button was pressed first
            if self.clothesGUI:
                self.clothesGUI.resetClothes(self.oldStyle)
                self.__handlePurchaseDone(timeout = 1)
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                                                CFSpeech | CFTimeout)
            self.resetTailor()

        elif (mode == NPCToons.PURCHASE_MOVIE_START or
              mode == NPCToons.PURCHASE_MOVIE_START_BROWSE or
              mode == NPCToons.PURCHASE_MOVIE_START_NOROOM):
            assert self.notify.debug('PURCHASE_MOVIE_START')

            if (mode == NPCToons.PURCHASE_MOVIE_START):
                self.browsing = 0
                self.roomAvailable = 1
            elif (mode == NPCToons.PURCHASE_MOVIE_START_BROWSE):
                self.browsing = 1
                self.roomAvailable = 1
            elif (mode == NPCToons.PURCHASE_MOVIE_START_NOROOM):
                self.browsing = 0
                self.roomAvailable = 0
                
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return
            else:
                self.accept(self.av.uniqueName('disable'),
                                        self.__handleUnexpectedExit)

            style = self.av.getStyle()
            self.oldStyle = ToonDNA.ToonDNA()
            self.oldStyle.makeFromNetString(style.makeNetString())
            self.setupAvatars(self.av)

            if (self.isLocalToon):
                camera.wrtReparentTo(render)
                camera.lerpPosHpr(-5, 9, self.getHeight()-0.5, -150, -2, 0, 1,
                                  other=self,
                                  blendType="easeOut",
                                  task=self.uniqueName('lerpCamera'))

            if (self.browsing == 0):
                if (self.roomAvailable == 0):
                    self.setChatAbsolute(TTLocalizer.STOREOWNER_NOROOM,
                                         CFSpeech | CFTimeout)
                else:
                    self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING,
                                         CFSpeech | CFTimeout)
            else:
                self.setChatAbsolute(TTLocalizer.STOREOWNER_BROWSING,
                                     CFSpeech | CFTimeout)

            if (self.isLocalToon):
                taskMgr.doMethodLater(3.0, self.popupPurchaseGUI,
                                       self.uniqueName('popupPurchaseGUI'))
                # print out our clothes and closet information before we start
                print ("-----------Starting tailor interaction-----------")
                print "avid: %s, gender: %s" % (self.av.doId, self.av.style.gender)
                print "current top = %s,%s,%s,%s and  bot = %s,%s," % (self.av.style.topTex, self.av.style.topTexColor,
                                                                       self.av.style.sleeveTex, self.av.style.sleeveTexColor,
                                                                       self.av.style.botTex, self.av.style.botTexColor)
                print "topsList = %s" % self.av.getClothesTopsList()
                print "bottomsList = %s" % self.av.getClothesBottomsList()
                print ("-------------------------------------------------")

            
        elif (mode == NPCToons.PURCHASE_MOVIE_COMPLETE):
            assert self.notify.debug('PURCHASE_MOVIE_COMPLETE')
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                                                CFSpeech | CFTimeout)

            if self.av and self.isLocalToon:
                # print out our clothes and closet information before we start
                print ("-----------ending tailor interaction-----------")
                print "avid: %s, gender: %s" % (self.av.doId, self.av.style.gender)
                print "current top = %s,%s,%s,%s and  bot = %s,%s," % (self.av.style.topTex, self.av.style.topTexColor,
                                                                       self.av.style.sleeveTex, self.av.style.sleeveTexColor,
                                                                       self.av.style.botTex, self.av.style.botTexColor)
                print "topsList = %s" % self.av.getClothesTopsList()
                print "bottomsList = %s" % self.av.getClothesBottomsList()
                print ("-------------------------------------------------")
                
            self.resetTailor()

        elif (mode == NPCToons.PURCHASE_MOVIE_NO_MONEY):
            self.notify.warning('PURCHASE_MOVIE_NO_MONEY should not be called')
            self.resetTailor()

        return

    def popupPurchaseGUI(self, task):
        assert self.notify.debug('popupPurchaseGUI()')
        self.setChatAbsolute('', CFSpeech)
        self.purchaseDoneEvent = 'purchaseDone'
        self.swapEvent = 'swap'
        self.acceptOnce(self.purchaseDoneEvent, self.__handlePurchaseDone)
        self.accept(self.swapEvent, self.__handleSwap)
        self.clothesGUI = TailorClothesGUI.TailorClothesGUI(self.purchaseDoneEvent,
                                                             self.swapEvent, self.npcId)
        self.clothesGUI.load()
        self.clothesGUI.enter(self.av)
        self.clothesGUI.showButtons()

        self.gui = loader.loadModel("phase_3/models/gui/create_a_toon_gui")
        # Only bring up the purchase button if there's a clothing ticket

        if self.browsing == 0:
            self.button = DirectButton(
                relief = None,
                image = (self.gui.find("**/CrtAtoon_Btn1_UP"),
                     self.gui.find("**/CrtAtoon_Btn1_DOWN"),
                     self.gui.find("**/CrtAtoon_Btn1_RLLVR"),
                     ),
                pos = (-0.15, 0, -0.85),
                command = self.__handleButton,
                text = ("", TTLocalizer.MakeAToonDone,
                    TTLocalizer.MakeAToonDone),
                text_font = ToontownGlobals.getInterfaceFont(),
                text_scale = 0.08,
                text_pos = (0,-0.03),
                text_fg = (1,1,1,1),
                text_shadow = (0,0,0,1),
                )
        else:
            self.button = None

        self.cancelButton = DirectButton(
            relief = None,
            image = (self.gui.find("**/CrtAtoon_Btn2_UP"),
                     self.gui.find("**/CrtAtoon_Btn2_DOWN"),
                     self.gui.find("**/CrtAtoon_Btn2_RLLVR"),
                     ),
            pos = (0.15, 0, -0.85),
            command = self.__handleCancel,
            text = ("", TTLocalizer.MakeAToonCancel,
                    TTLocalizer.MakeAToonCancel),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_scale = 0.08,
            text_pos = (0,-0.03),
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            )

        camera.setPosHpr(base.localAvatar,
                         -4.16, 8.25, 2.47, -152.89, 0.00, 0.00)
        # Ugly: find counter so you can hide it from toon's view
        self.counter = render.find('**/*mo1_TI_counter')
        self.counter.hide()

        # Hide the tailor, who will likely block the view of
        # ourselves.
        self.hide()

        return Task.done

    def __handleButton(self):
        messenger.send('next')

    def __handleCancel(self):
        self.clothesGUI.resetClothes(self.oldStyle)
        messenger.send('last')

    def __handleSwap(self):
        assert self.notify.debug("__handleSwap")
        self.d_setDNA(self.av.getStyle().makeNetString(), 0)

    def __handlePurchaseDone(self, timeout = 0):
        """
        This is the callback from the Purchase object
        Cleanup the gui and send the message to the AI
        """
        assert self.notify.debug('handlePurchaseDone()')
        if (self.clothesGUI.doneStatus == 'last' or timeout == 1):
            # The client really does not need to send the DNA here
            # since the server is keeping track of it
            self.d_setDNA(self.oldStyle.makeNetString(), 1)
        else:
            # The client really does not need to send the DNA here
            # since the server is keeping track of it

            # check if we ever changed the shorts or shirt
            # create a bit string that identifies which items
            # have been changed
            # bit 0 = shirts
            # bit 1 = shorts
            # bit 2...unused
            
            which = 0
            if self.clothesGUI.topChoice != -1:
                which = which | ClosetGlobals.SHIRT
            if self.clothesGUI.bottomChoice != -1:
                which = which | ClosetGlobals.SHORTS
            print "setDNA: which = %d, top = %d, bot = %d" % (which, self.clothesGUI.topChoice, self.clothesGUI.bottomChoice)
            # if the closet is full or almost full, confirm that we want to lose the
            # clothes we are wearing
            if self.roomAvailable == 0:
                if (self.isLocalToon):
                    if (self.av.isClosetFull() or 
                        (which & ClosetGlobals.SHIRT and which & ClosetGlobals.SHORTS)):
                        # the closet is at max capacity
                        # or it's almost full and we are changing both our top and bottom
                        self.__enterConfirmLoss(2, which)
                        self.clothesGUI.hideButtons()
                        self.button.hide()
                        self.cancelButton.hide()
                    else:
                        self.d_setDNA(self.av.getStyle().makeNetString(), 2, which) 
            else:
                self.d_setDNA(self.av.getStyle().makeNetString(), 2, which)

    def __enterConfirmLoss(self, finished, which):
        if self.popupInfo == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                             buttons.find('**/ChtBx_OKBtn_DN'),
                             buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (buttons.find('**/CloseBtn_UP'),
                                 buttons.find('**/CloseBtn_DN'),
                                 buttons.find('**/CloseBtn_Rllvr'))
            # Popup a message warning that you will lose current clothes
            self.popupInfo = DirectFrame(
                parent = hidden,
                relief = None,
                state = 'normal',
                text = TTLocalizer.STOREOWNER_CONFIRM_LOSS,
                text_wordwrap = 10,
                textMayChange = 0,
                frameSize = (-1,1,-1,1),
                text_pos = (0, -0.05),
                geom = DGG.getDefaultDialogGeom(),
                geom_color = ToontownGlobals.GlobalDialogColor,
                geom_scale = (.88, 1, .55),
                geom_pos = (0,0,-.18),
                text_scale = .08,
                )
            DirectButton(self.popupInfo,
                         image = okButtonImage,
                         relief = None,
                         text = TTLocalizer.STOREOWNER_OK,
                         text_scale = 0.05,
                         text_pos = (0.0, -0.1),
                         textMayChange = 0,
                         pos = (-0.08, 0.0, -0.31),
                         command = self.__handleConfirmLossOK,
                         extraArgs = [finished, which])
            DirectButton(self.popupInfo,
                         image = cancelButtonImage,
                         relief = None,
                         text = TTLocalizer.STOREOWNER_CANCEL,
                         text_scale = 0.05,
                         text_pos = (0.0, -0.1),
                         textMayChange = 0,
                         pos = (0.08, 0.0, -0.31),
                         command = self.__handleConfirmLossCancel)
            buttons.removeNode()
        # Show the confim loss popup
        self.popupInfo.reparentTo(aspect2d)
        
    def __handleConfirmLossOK(self, finished, which):
        self.d_setDNA(self.av.getStyle().makeNetString(), finished, which)
        self.popupInfo.reparentTo(hidden)
        
    def __handleConfirmLossCancel(self):
        self.d_setDNA(self.oldStyle.makeNetString(), 1)
        self.popupInfo.reparentTo(hidden)
        
    
    def d_setDNA(self, dnaString, finished, whichItems = ClosetGlobals.SHIRT | ClosetGlobals.SHORTS):
        # Report our DNA to the server
        self.sendUpdate('setDNA', [dnaString, finished, whichItems])

            
    def setCustomerDNA(self, avId, dnaString):
        assert self.notify.debug("setCustomerDNA")
        # The AI doesn't set the DNA on swaps (finished=0) anymore.
        # This is to avoid bugged clothes on AI crashes while browsing.  Now the AI
        # just tells the clients the correct DNA for the current customer
        # and lets the clients set the value directly on the distributed
        # toon. The AI will still do a DNA change on purchase.

        # the av might be gone, so check first
        if avId != base.localAvatar.doId:
            av = base.cr.doId2do.get(avId, None)
            if av:
                if self.av == av:
                    self.av.style.makeFromNetString(dnaString)
                    self.av.generateToonClothes()
