from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toonbase import ToontownGlobals
from direct.fsm import StateData
from toontown.shtiker.PurchaseManagerConstants import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from toontown.toonbase import TTLocalizer

class PurchaseBase(StateData.StateData):

    activateMode = 'purchase'

    def __init__(self, toon, doneEvent):
        """__init__(self, Toon, int, string):
        Create and display a purchase screen for
        the given Toon with the given amount of points to spend on items.
        Throw the given event name when user is finished
        """
        StateData.StateData.__init__(self, doneEvent)

        self.toon = toon
        self.fsm = ClassicFSM.ClassicFSM('Purchase',
                           [State.State('purchase',
                                        self.enterPurchase,
                                        self.exitPurchase,
                                        ['done']),
                            State.State('done',
                                        self.enterDone,
                                        self.exitDone,
                                        ['purchase']),],
                           'done',
                           'done',
                           )

        self.fsm.enterInitialState()
        return
    
    def load(self, purchaseModels=None):

        # These get passed in from Purchase.py
        if (purchaseModels == None):
            purchaseModels = loader.loadModel(
                "phase_4/models/gui/purchase_gui")

        self.music = base.loadMusic("phase_4/audio/bgm/FF_safezone.mid")

        self.jarImage = purchaseModels.find("**/Jar")
        self.jarImage.reparentTo(hidden)
        
        self.frame = DirectFrame(relief = None)
        self.frame.hide()

        self.title = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (0.0, 0.0, 0.83),
            scale = 1.2,
            image = purchaseModels.find("**/Goofys_Sign"),
            text = TTLocalizer.GagShopName,
            text_fg = (0.6,0.2,0,1),
            text_scale = 0.09,
            text_wordwrap = 10,
            text_pos = (0,0.025,0),
            text_font = ToontownGlobals.getSignFont(),
            )

        self.pointDisplay = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-1.15, 0.0, 0.16),
            text = str(self.toon.getMoney()),
            text_scale = 0.2,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_pos = (0, -0.1, 0),
            image = self.jarImage,
            text_font = ToontownGlobals.getSignFont(),            
            )

        self.statusLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.25, 0, 0.625),
            text = (TTLocalizer.GagShopYouHave % (self.toon.getMoney())),
            text_scale = TTLocalizer.PBstatusLabel,
            text_fg = (0.05, 0.14, 0.4, 1),
            )
        
        # Cover the singular Jellybean case
        if self.toon.getMoney() == 1:
            self.statusLabel['text'] = (TTLocalizer.GagShopYouHaveOne)

        self.isBroke = 0

        return
    
    def unload(self):
        self.jarImage.removeNode()
        del self.jarImage
        self.frame.destroy()
        del self.frame
        del self.title
        del self.pointDisplay
        del self.statusLabel
        del self.music
        del self.fsm
        return

    def __handleSelection(self, track, level):
        """handleSelection(self, int, int)
        If item level accessable, add purchase button to detail inv menu.
        """
        self.handlePurchase(track, level)
        
    def handlePurchase(self, track, level):
        """handlePurchase(self, track, level)
        Subtract points and add item to inv if successful.
        Print appropriate reject message otherwise.
        """
        # protect against purchases in the gag tutorial
        if self.toon.getMoney() <= 0:
            return
        ret = self.toon.inventory.addItem(track, level)

        if (ret == -2):
            text = TTLocalizer.GagShopTooManyProps
        elif (ret == -1):
            text = TTLocalizer.GagShopTooManyOfThatGag % TTLocalizer.BattleGlobalAvPropStringsPlural[track][level]
        elif (ret == 0):
            text = TTLocalizer.GagShopInsufficientSkill
        else:
            text = TTLocalizer.GagShopYouPurchased % TTLocalizer.BattleGlobalAvPropStringsSingular[track][level]
            # update the inventory display
            self.toon.inventory.updateGUI(track, level)
            # update the point total and act accordingly
            self.toon.setMoney(self.toon.getMoney() - 1)

            # Also send a message to the AI for each gag purchased.
            # We didn't always do it this way, but in the presence of
            # resistance chat phrases (in particular, jellybean
            # boosts), we need to keep the AI more in-sync with the
            # client.
            messenger.send('boughtGag')

        self.showStatusText(text)
        return

    def showStatusText(self, text):
        self.statusLabel['text'] = text
        taskMgr.remove("resetStatusText")
        taskMgr.doMethodLater(2.0, self.resetStatusText, "resetStatusText")
        return

    def resetStatusText(self, task):
        self.statusLabel['text'] = ""
        return Task.done

    def checkForBroke(self):
        money = self.toon.getMoney()
        self.pointDisplay["text"] = str(money)

        if money == 0:
            if not self.isBroke:
                # no money, no props!
                self.toon.inventory.setActivateModeBroke()
                # set the confirmation text
                taskMgr.doMethodLater(2.25, self.showBrokeMsg, "showBrokeMsgTask")
                self.isBroke = 1
            
        else:
            if self.isBroke:
                self.toon.inventory.setActivateMode(self.activateMode)
                taskMgr.remove("showBrokeMsgTask")
                self.isBroke = 0

            if money == 1:
                self.statusLabel['text'] = TTLocalizer.GagShopYouHaveOne
            else:
                self.statusLabel['text'] = TTLocalizer.GagShopYouHave % (money)
            
        return

    def showBrokeMsg(self, task):
        self.statusLabel['text'] = TTLocalizer.GagShopOutOfJellybeans
        return Task.done

    def handleDone(self, playAgain):
        #base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        messenger.send(self.doneEvent)

    # wrapper functions

    def enter(self):
        #base.playMusic(self.music, looping = 1, volume = 0.8)
        self.fsm.request("purchase")        

    def exit(self):
        self.music.stop()
        self.fsm.request("done")

    ### Purchase state functions ###

    def enterPurchase(self):
        self.frame.show()
        self.toon.inventory.enableUberGags(0)
        self.toon.inventory.show()
        self.toon.inventory.reparentTo(self.frame)
        self.toon.inventory.setActivateMode(self.activateMode)

        self.checkForBroke()
        
        self.acceptOnce("purchaseOver", self.handleDone)
        self.accept("inventory-selection", self.__handleSelection)
        self.accept(self.toon.uniqueName("moneyChange"), self.__moneyChange)
        return
        
    def exitPurchase(self):
        self.frame.hide()
        self.toon.inventory.enableUberGags(1)
        self.toon.inventory.reparentTo(hidden)
        self.toon.inventory.hide()

        self.ignore("purchaseOver")
        self.ignore("inventory-selection")
        self.ignore(self.toon.uniqueName("moneyChange"))
        taskMgr.remove("resetStatusText")
        taskMgr.remove("showBrokeMsgTask")        
        return

    def __moneyChange(self, money):
        self.checkForBroke()

    ### Done state functions ###
    def enterDone(self):
        pass

    def exitDone(self):
        pass    
