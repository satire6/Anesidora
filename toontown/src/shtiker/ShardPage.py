"""ShardPage module: contains the ShardPage class"""

from pandac.PandaModules import *
import ShtikerPage
from direct.task.Task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.distributed import ToontownDistrictStats
from toontown.toontowngui import TTDialog



POP_COLORS_NTT = (
    Vec4(0.,1.,0.,1.),
    Vec4(1.,1.,0.,1.),
    Vec4(1.,0.,0.,1.),
    )

POP_COLORS = (
    Vec4(0.4,0.4,1.,1.),
    Vec4(0.4,1.,0.4,1.),
    Vec4(1.,0.4,0.4,1.),
    )

class ShardPage(ShtikerPage.ShtikerPage):
    """ShardPage class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("ShardPage")

    # special methods
    def __init__(self):
        """__init__(self)
        ShardPage constructor: create the shard selector page
        """
        ShtikerPage.ShtikerPage.__init__(self)

        self.shardButtonMap = {}
        self.shardButtons = []
        self.scrollList = None
        
        self.textRolloverColor = Vec4(1,1,0,1)
        self.textDownColor = Vec4(0.5,0.9,1,1)
        self.textDisabledColor = Vec4(0.4,0.8,0.4,1)
        self.ShardInfoUpdateInterval = 5.0  # seconds

        self.lowPop, self.midPop, self.highPop = base.getShardPopLimits()
        self.showPop = config.GetBool("show-total-population", 0)
        self.noTeleport = config.GetBool("shard-page-disable", 0)
        
    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12

        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.ShardPageTitle,
            text_scale = title_text_scale,
            textMayChange = 0,
            pos = (0,0,0.6),
            )

        helpText_ycoord = 0.403

        self.helpText = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_scale = main_text_scale,
            text_wordwrap = 12,
            text_align = TextNode.ALeft,
            textMayChange = 1,
            pos = (0.058, 0, helpText_ycoord),
            )

        shardPop_ycoord = helpText_ycoord - 0.523
        totalPop_ycoord = shardPop_ycoord - 0.26

        self.totalPopulationText = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.ShardPagePopulationTotal % (1),
            text_scale = main_text_scale,
            text_wordwrap = 8,
            textMayChange = 1,
            text_align = TextNode.ACenter,
            pos = (0.38, 0, totalPop_ycoord),
            )

        if self.showPop:
            self.totalPopulationText.show()
        else:
            self.totalPopulationText.hide()

        self.gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")

        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96 
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293

        self.regenerateScrollList()

        scrollTitle = DirectFrame(
            parent = self.scrollList,
            text = TTLocalizer.ShardPageScrollTitle,
            text_scale = main_text_scale,
            text_align = TextNode.ACenter,
            relief = None,
            pos = (self.buttonXstart, 0, self.itemFrameZorigin+0.127),
            )

    def unload(self):
        self.gui.removeNode()
        del self.title
        self.scrollList.destroy()
        del self.scrollList
        del self.shardButtons
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.unload(self)

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for button in self.shardButtons:
                button.detachNode()
            self.scrollList.destroy()
            self.scrollList = None
            
        self.scrollList = DirectScrolledList(
            parent = self,
            relief = None,
            pos = (-0.5,0,0),
            # inc and dec are DirectButtons
            # incButton is on the bottom of page, decButton is on the top!
            incButton_image = (self.gui.find("**/FndsLst_ScrollUp"),
                               self.gui.find("**/FndsLst_ScrollDN"),
                               self.gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               self.gui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_scale = (self.arrowButtonScale,self.arrowButtonScale,-self.arrowButtonScale),
            incButton_pos = (self.buttonXstart,0,self.itemFrameZorigin-0.999),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.2),
            decButton_image = (self.gui.find("**/FndsLst_ScrollUp"),
                               self.gui.find("**/FndsLst_ScrollDN"),
                               self.gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               self.gui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_scale = (self.arrowButtonScale,self.arrowButtonScale,self.arrowButtonScale),
            #decButton_pos = (self.buttonXstart,0,self.itemFrameZorigin+0.127),
            decButton_pos = (self.buttonXstart,0,self.itemFrameZorigin+0.227),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.2),

            # itemFrame is a DirectFrame
            itemFrame_pos = (self.itemFrameXorigin,0,self.itemFrameZorigin),
            itemFrame_scale = 1.0,
            itemFrame_relief = DGG.SUNKEN,
            # frameSize is (minX,maxX,minZ,maxZ);  where x goes left->right neg->pos,
            # and z goes bottom->top neg->pos
            itemFrame_frameSize = (self.listXorigin,self.listXorigin+self.listFrameSizeX,
                                   self.listZorigin,self.listZorigin+self.listFrameSizeZ),
            itemFrame_frameColor = (0.85,0.95,1,1),
            itemFrame_borderWidth = (0.01,0.01),
            # each item is a button with text on it
            numItemsVisible = 15,
            # need to set height of each entry to avoid list text running off end of listbox
            forceHeight = 0.065,
            items = self.shardButtons,
            )
        self.scrollList.scrollTo(selectedIndex)

    def askForShardInfoUpdate(self, task=None):
        ToontownDistrictStats.refresh('shardInfoUpdated')                
        # repeat request several seconds in the future
        taskMgr.doMethodLater(self.ShardInfoUpdateInterval, self.askForShardInfoUpdate, 'ShardPageUpdateTask-doLater')
        return Task.done

    def makeShardButton(self, shardId, shardName, shardPop):

        shardButtonParent = DirectFrame()

        shardButtonL = DirectButton(
            parent = shardButtonParent,
            relief = None,
            text = shardName,
            text_scale = 0.06,
            text_align = TextNode.ALeft,
            text1_bg = self.textDownColor,
            text2_bg = self.textRolloverColor,
            text3_fg = self.textDisabledColor,
            textMayChange = 0,
            command = self.getPopChoiceHandler(shardPop),
            extraArgs = [shardId],
            )

        # live ops has requested a dconfig to show shard pop - so we will support both
        if self.showPop:
            popText = str(shardPop)
            if shardPop == None:
                popText = ""
            shardButtonR = DirectButton(
                parent = shardButtonParent,
                relief = None, 
                text = popText,
                text_scale = 0.06,
                text_align = TextNode.ALeft,
                text1_bg = self.textDownColor,
                text2_bg = self.textRolloverColor,
                text3_fg = self.textDisabledColor,
                textMayChange = 1,
                pos = (0.5, 0, 0),
                command = self.choseShard,
                extraArgs = [shardId],
                )
        else:
            model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
            button = model.find('**/minnieCircle')

            shardButtonR = DirectButton(
                parent = shardButtonParent,
                relief = None,
                image = button,
                image_scale = (0.3, 1, 0.3),
                image2_scale = (0.35, 1, 0.35),                
                image_color = self.getPopColor(shardPop),
                pos = (0.6, 0, 0.0125),
                text = self.getPopText(shardPop),
                text_scale = 0.06,
                text_align = TextNode.ACenter,
                text_pos = (-0.0125, -0.0125),
                # only rollover text visible on "stop lights"
                text_fg = Vec4(0,0,0,0),
                text1_fg = Vec4(0,0,0,0),
                text2_fg = Vec4(0,0,0,1),
                text3_fg = Vec4(0,0,0,0),
                command = self.getPopChoiceHandler(shardPop),
                extraArgs = [shardId],
                )

            del model
            del button

        return (shardButtonParent, shardButtonR, shardButtonL)

    def getPopColor(self, pop):
        """
        Choose the appropriate color based on the population size.
        The Japanese client is a little different from the others.
        """
        if base.cr.productName == "JP":
            if pop < self.midPop:
                color1 = POP_COLORS_NTT[0]
                color2 = POP_COLORS_NTT[1]
                popRange = self.midPop - self.lowPop
                pop = pop - self.lowPop
            else:
                color1 = POP_COLORS_NTT[1]
                color2 = POP_COLORS_NTT[2]
                popRange = self.highPop - self.midPop
                pop = pop - self.midPop
            popPercent = pop / float(popRange)
            if popPercent > 1:
                popPercent = 1
            newColor = (color2 * popPercent) + (color1 * (1 - popPercent))
        else:
            if pop <= self.lowPop:
                newColor = POP_COLORS[0]
            elif pop <= self.midPop:
                newColor = POP_COLORS[1]
            else:
                newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop):
        """
        Choose the appropriate population description text.
        """
        if pop <= self.lowPop:
            popText = TTLocalizer.ShardPageLow
        elif pop <= self.midPop:
            popText = TTLocalizer.ShardPageMed
        else:
            popText = TTLocalizer.ShardPageHigh
        return popText

    def getPopChoiceHandler(self, pop):
        """
        Returns the appropriate handler for a given shard.
        If pop is high, it does not allow the user to enter it.
        The showPop flag allows devs to see shard pops and teleport anywhere.
        The noTeleport flag allows devs to disable all shard hopping.
        The showPop flag overrides the noTeleport flag.
        """
        if base.cr.productName == "JP":
            handler = self.choseShard
        elif pop <= self.midPop:
            if self.noTeleport and not self.showPop:
                handler = self.shardChoiceReject
            else:
                handler = self.choseShard
        else:
            if self.showPop:
                # we are a dev - allow the teleport
                handler = self.choseShard
            else:
                # deny
                handler = self.shardChoiceReject
        return handler

    def getCurrentZoneId(self):
        try:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        except:
            zoneId = None
        return zoneId

    def getCurrentShardId(self):
        # Returns the user's current shard if we are not in
        # WelcomeValley, or WelcomeValleyToken if we are in
        # WelcomeValley.
        zoneId = self.getCurrentZoneId()
        if zoneId != None and ZoneUtil.isWelcomeValley(zoneId):
            return ToontownGlobals.WelcomeValleyToken
        else:
            return base.localAvatar.defaultShard

    def updateScrollList(self):
        # curShardTuples is a list of 3-item tuples (shardId, shardName, shardPopulation)
        curShardTuples = base.cr.listActiveShards()

        """
        # For testing
        curShardTuples = [(200000000, 'Shard Name 1', 0, 50),
                          (200000001, 'Shard Name 2', 16, 50),
                          (200000002, 'Shard Name 3', 32, 50),
                          (200000003, 'Shard Name 4', 48, 50),
                          (200000004, 'Shard Name 5', 64, 50),
                          (200000005, 'Shard Name 6', 80, 50),
                          (200000006, 'Shard Name 7', 96, 50),
                          (200000007, 'Shard Name 8', 112, 50),
                          (200000008, 'Shard Name 9', 128, 50),
                          (200000009, 'Shard Name 10', 144, 50),
                          (200000010, 'Shard Name 11', 160, 50),
                          (200000011, 'Shard Name 12', 176, 50),
                          (200000012, 'Shard Name 13', 192, 50),
                          (200000013, 'Shard Name 14', 208, 50),
                          (200000014, 'Shard Name 15', 224, 50),
                          (200000015, 'Shard Name 16', 240, 50),
                          (200000016, 'Shard Name 17', 256, 50),
                          (200000017, 'Shard Name 18', 272, 50),
                          (200000018, 'Shard Name 19', 288, 50),
                          (200000019, 'Shard Name 20', 304, 50),
                          (200000020, 'Shard Name 21', 404, 50),
                          (200000021, 'Shard Name 22', 808, 50),
                          ]
        """
        
        # Sort the shard list into alphabetical order before we append
        # Welcome Valley onto the end of the list.
        def compareShardTuples(a, b):
            if a[1] < b[1]:
                return -1
            elif b[1] < a[1]:
                return 1
            else:
                return 0
        curShardTuples.sort(compareShardTuples)

        if base.cr.welcomeValleyManager:
            curShardTuples.append((ToontownGlobals.WelcomeValleyToken,
                                   TTLocalizer.WelcomeValley[-1], 0, 0))

        #print "curShardTuples=",curShardTuples
        #print "self.shardButtns.keys=",self.shardButtons.keys()

        currentShardId = self.getCurrentShardId()
        actualShardId = base.localAvatar.defaultShard
        actualShardName = None

        anyChanges = 0
        totalPop = 0
        totalWVPop = 0
        currentMap = {}
        self.shardButtons = []
        for i in range(len(curShardTuples)):
            shardId, name, pop, WVPop = curShardTuples[i]
            if shardId == actualShardId:
                actualShardName = name

            totalPop += pop
            totalWVPop += WVPop

            # this is useful for shard balancing, but not machine load balancing
            #pop -= WVPop
            
            currentMap[shardId] = 1
            buttonTuple = self.shardButtonMap.get(shardId)
            if buttonTuple == None:
                # This is a new shard; add it to the list.
                buttonTuple = self.makeShardButton(shardId, name, pop)
                self.shardButtonMap[shardId] = buttonTuple
                anyChanges = 1
            else:
                # This is an existing shard; update the pop.
                if self.showPop:
                    buttonTuple[1]['text'] = str(pop)
                else:
                    buttonTuple[1]['image_color'] = self.getPopColor(pop)
                    # all but the Japanese product get the new scheme
                    if not base.cr.productName == "JP":
                        buttonTuple[1]['text'] = self.getPopText(pop)
                        buttonTuple[1]['command'] = self.getPopChoiceHandler(pop)
                        buttonTuple[2]['command'] = self.getPopChoiceHandler(pop)
                
            self.shardButtons.append(buttonTuple[0])

            # Enable or disable the button appropriately.
            if (shardId == currentShardId or self.book.safeMode):
                buttonTuple[1]['state'] = DGG.DISABLED
                buttonTuple[2]['state'] = DGG.DISABLED
            else:
                buttonTuple[1]['state'] = DGG.NORMAL
                buttonTuple[2]['state'] = DGG.NORMAL

        # Now look for shards that are no longer on the list.
        for shardId, buttonTuple in self.shardButtonMap.items():
            if shardId not in currentMap:
                # This shard should be removed.
                buttonTuple[0].destroy()
                del self.shardButtonMap[shardId]
                anyChanges = 1

        # Set the population for WelcomeValley properly, as the sum of
        # all of the WelcomeValley hoods across all shards.
        buttonTuple = self.shardButtonMap.get(ToontownGlobals.WelcomeValleyToken)
        if buttonTuple:
            if self.showPop:
                buttonTuple[1]['text'] = str(totalWVPop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(totalWVPop)
                # all but the Japanese product get the new scheme
                if not base.cr.productName == "JP":
                    buttonTuple[1]['text'] = self.getPopText(totalWVPop)
                    buttonTuple[1]['command'] = self.getPopChoiceHandler(totalWVPop)
                    buttonTuple[2]['command'] = self.getPopChoiceHandler(totalWVPop)
                    
        if anyChanges:
            self.regenerateScrollList()

        self.totalPopulationText["text"] = TTLocalizer.ShardPagePopulationTotal % (totalPop)

        helpText = TTLocalizer.ShardPageHelpIntro
        
        # Is the current shard on the list?  It should be, but
        # something might have gone wrong.
        if actualShardName:
            if currentShardId == ToontownGlobals.WelcomeValleyToken:
                helpText += (TTLocalizer.ShardPageHelpWelcomeValley % (actualShardName))
            else:
                helpText += (TTLocalizer.ShardPageHelpWhere % (actualShardName))

        if (not self.book.safeMode):
            helpText += TTLocalizer.ShardPageHelpMove

        self.helpText["text"] = helpText
        
    def enter(self):
        self.askForShardInfoUpdate()
        self.updateScrollList()

        # Center on the current shard.
        currentShardId = self.getCurrentShardId()
        buttonTuple = self.shardButtonMap.get(currentShardId)
        if buttonTuple:
            i = self.shardButtons.index(buttonTuple[0])
            self.scrollList.scrollTo(i, centered = 1)
        
        ShtikerPage.ShtikerPage.enter(self)
        self.accept('shardInfoUpdated', self.updateScrollList)

    def exit(self):
        self.ignore('shardInfoUpdated')
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.exit(self)

    def shardChoiceReject(self, shardId):
        # we have denied the user's request to move to a crowded shard
        self.confirm = TTDialog.TTGlobalDialog(
            doneEvent = "confirmDone",
            message = TTLocalizer.ShardPageChoiceReject,
            style = TTDialog.Acknowledge)
        self.confirm.show()
        self.accept("confirmDone", self.__handleConfirm)
        
    def __handleConfirm(self):
        """__handleConfirm(self)
        """
        self.ignore("confirmDone")
        self.confirm.cleanup()
        del self.confirm

    def choseShard(self, shardId):
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        currentShardId = self.getCurrentShardId()

        if shardId == currentShardId:
            return

        elif shardId == ToontownGlobals.WelcomeValleyToken:
            # This is a special case: it's really more like
            # teleporting to a neighborhood, rather than actually
            # switching shards.
            self.doneStatus = {"mode" : "teleport",
                               "hood" : ToontownGlobals.WelcomeValleyToken,
                               }
            messenger.send(self.doneEvent)

        elif shardId == base.localAvatar.defaultShard:
            # Also, going back to our original real shard is just a
            # teleport back to our canonical zone.

            self.doneStatus = {"mode" : "teleport",
                               "hood" : canonicalHoodId,
                               }
            messenger.send(self.doneEvent)
            
        else:
            try:
                place = base.cr.playGame.getPlace()
            except:
                try:
                    place = base.cr.playGame.hood.loader.place
                except:
                    place = base.cr.playGame.hood.place

            # Switching to a real shard takes you out of WelcomeValley
            # (and hence into your canonical hoodId).
            place.requestTeleport(canonicalHoodId, canonicalHoodId, shardId, -1)
        return

