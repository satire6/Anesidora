"""SuitPage module: contains the SuitPage class"""

import ShtikerPage
from direct.task.Task import Task
import SummonCogDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.suit import SuitDNA
from toontown.suit import Suit
from toontown.battle import SuitBattleGlobals
from CogPageGlobals import *

# how much to scale the cog panel on rollover
SCALE_FACTOR = 1.5

# how slowly the radar screen updates
RADAR_DELAY = 0.2

# positions for the building radar labels
BUILDING_RADAR_POS = (0.375, 0.065 ,-0.225, -0.5)

PANEL_COLORS = (
    Vec4(0.8, 0.78, 0.77, 1),
    Vec4(0.75, 0.78, 0.8, 1),
    Vec4(0.75, 0.82, 0.79, 1),
    Vec4(0.825, 0.76, 0.77, 1)
    )

# TODO: get art to replace these simple color swaps...
PANEL_COLORS_COMPLETE1 = (
    Vec4(0.7, 0.725, 0.545, 1),
    Vec4(0.625, 0.725, 0.65, 1),
    Vec4(0.6, 0.75, 0.525, 1),
    Vec4(0.675, 0.675, 0.55, 1)
    )

PANEL_COLORS_COMPLETE2 = (
    Vec4(0.9, 0.725, 0.32, 1),
    Vec4(0.825, 0.725, 0.45, 1),
    Vec4(0.8, 0.75, 0.325, 1),
    Vec4(0.875, 0.675, 0.35, 1)
    )

# the shadows must be carefully positioned behind the heads
SHADOW_SCALE_POS = (
    # scale, x pos, y pos, z pos
    # corp
    (1.225, 0, 10, -0.03),
    (0.9, 0, 10, 0),
    (1.125, 0, 10, -0.015),
    (1.0, 0, 10, -0.02),    
    (1.0, -0.02, 10, -0.01),
    (1.05, 0, 10, -0.0425),
    (1.0, 0, 10, -0.05),
    (0.9, -0.0225, 10, -0.025),
    # legal
    (1.25, 0, 10, -0.03),
    (1.0, 0, 10, -0.01),
    (1.0, 0.005, 10, -0.01),
    (1.0, 0, 10, -0.01),    
    (0.9, 0.005, 10, -0.01),
    (0.95, 0, 10, -0.01),
    (1.125, 0.005, 10, -0.035), 
    (0.85, -0.005, 10, -0.035),
    # money
    (1.2, 0, 10, -0.01), 
    (1.05, 0, 10, 0),
    (1.1, 0, 10, -0.04),
    (1.0, 0, 10, 0),
    (0.95, 0.0175, 10, -0.015),
    (1.0, 0, 10, -0.06),
    (0.95, 0.02, 10, -0.0175),
    (0.9 , 0, 10, -0.03),
    # sales
    (1.15, 0, 10, -0.01),
    (1.0, 0, 10, 0),
    (1.0, 0, 10, 0),
    (1.1, 0, 10, -0.04),
    (0.93, 0.005, 10, -0.01),
    (0.95, 0.005, 10, -0.01),
    (1.0, 0, 10, -0.02),
    (0.9, 0.0025, 10, -0.03),    
    )

class SuitPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)

        # suit page gui
        frameModel = loader.loadModel('phase_3.5/models/gui/suitpage_frame')
        frameModel.setScale(0.03375, 1, 0.045)
        frameModel.setPos(0, 10, -0.575)
        
        # make some nodes to help organize the things
        self.guiTop = NodePath('guiTop')
        self.guiTop.reparentTo(self)
        self.frameNode = NodePath('frameNode')
        self.frameNode.reparentTo(self.guiTop)
        self.panelNode = NodePath('panelNode')
        self.panelNode.reparentTo(self.guiTop)
        self.iconNode = NodePath('iconNode')
        self.iconNode.reparentTo(self.guiTop)                 
        self.enlargedPanelNode = NodePath('enlargedPanelNode')
        self.enlargedPanelNode.reparentTo(self.guiTop)                 

        # make sure all this stuff draws in the correct order:
        #
        #  - frame on bottom
        #  - panels over frame
        #  - title, icons and screws over panels
        #  - enlarged panels over everything
        #
        frame = frameModel.find('**/frame')
        frame.wrtReparentTo(self.frameNode)
        screws = frameModel.find('**/screws')
        screws.wrtReparentTo(self.iconNode)
        icons = frameModel.find('**/icons')
        del frameModel

        # make the title
        self.title = DirectLabel(
            parent = self.iconNode,
            relief = None,
            text = TTLocalizer.SuitPageTitle,
            text_scale = 0.1,
            text_pos = (0.04, 0),
            textMayChange = 0,            
            )        

        # make the radar buttons
        self.radarButtons = []
        icon = icons.find('**/corp_icon')
        self.corpRadarButton = DirectButton(
            parent = self.iconNode,
            relief = None,
            state = DGG.DISABLED,
            image = icon,
            image_scale = (0.03375, 1, 0.045),
            # stand in for rollover art
            image2_color = Vec4(1.0,1.0,1.0,0.75),
            pos = (-0.2, 10, -0.575),
            command = self.toggleRadar,
            extraArgs = [0],                        
            )
        self.radarButtons.append(self.corpRadarButton)
        icon = icons.find('**/legal_icon')
        self.legalRadarButton = DirectButton(
            parent = self.iconNode,
            relief = None,
            state = DGG.DISABLED,
            image = icon,
            image_scale = (0.03375, 1, 0.045),
            # stand in for rollover art
            image2_color = Vec4(1.0,1.0,1.0,0.75),
            pos = (-0.2, 10, -0.575),
            command = self.toggleRadar,
            extraArgs = [1],                        
            )
        self.radarButtons.append(self.legalRadarButton)
        icon = icons.find('**/money_icon')
        self.moneyRadarButton = DirectButton(
            parent = self.iconNode,
            relief = None,
            state = DGG.DISABLED,            
            image = (icon, icon, icon),
            image_scale = (0.03375, 1, 0.045),
            # stand in for rollover art
            image2_color = Vec4(1.0,1.0,1.0,0.75),
            pos = (-0.2, 10, -0.575),
            command = self.toggleRadar,
            extraArgs = [2],
            )
        self.radarButtons.append(self.moneyRadarButton)
        icon = icons.find('**/sales_icon')
        self.salesRadarButton = DirectButton(
            parent = self.iconNode,
            relief = None,
            state = DGG.DISABLED,            
            image = (icon, icon, icon),
            image_scale = (0.03375, 1, 0.045),
            # stand in for rollover art
            image2_color = Vec4(1.0,1.0,1.0,0.75),
            pos = (-0.2, 10, -0.575),
            command = self.toggleRadar,
            extraArgs = [3],            
            )
        self.radarButtons.append(self.salesRadarButton)

        # this field will let us know when the builing radar is activated
        for radarButton in self.radarButtons:
            radarButton.building = 0
            radarButton.buildingRadarLabel = None
        
        # make panels for the suit heads
        gui = loader.loadModel('phase_3.5/models/gui/suitpage_gui')

        # load the panel art work
        self.panelModel = gui.find('**/card')
        
        # load the shadows for the suit heads
        self.shadowModels = []
        # put them in order for easy retrieval
        for index in range(1, len(SuitDNA.suitHeadTypes) + 1):
            self.shadowModels.append(gui.find('**/shadow' + str(index)))

        del gui
        
        # make the individual panels for each suit
        self.makePanels()

        # keep some state
        self.radarOn = [0, 0, 0, 0]
        
        # scoot everything up
        self.guiTop.setZ(0.625)

    def unload(self):
        # clean up our DirectGui elements
        self.title.destroy()
        self.corpRadarButton.destroy()
        self.legalRadarButton.destroy()
        self.moneyRadarButton.destroy()
        self.salesRadarButton.destroy()        
        # clean up our other gui elements
        for panel in self.panels:
            panel.destroy()
        del self.panels
        # clean up our master copies
        for shadow in self.shadowModels:
            shadow.removeNode()
        self.panelModel.removeNode()
        # call parent class unload
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        # make sure we reflect current cog status
        self.updatePage()
        self.bigPanel = None
        self.nextPanel = None
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        # remove any do-later hooks
        taskMgr.remove('buildingListResponseTimeout-later')
        taskMgr.remove('suitListResponseTimeout-later')
        taskMgr.remove('showCogRadarLater')
        taskMgr.remove('showBuildingRadarLater')
        # turn off any radars that are on and reset the button status
        for index in range(0, len(self.radarOn)):
            if self.radarOn[index]:
                self.toggleRadar(index)
                self.radarButtons[index]['state'] = DGG.NORMAL                    
        ShtikerPage.ShtikerPage.exit(self)
        

    #
    # callbacks
    #

    def grow(self, panel, pos):
        #don't grow if there's already a big panel
        if self.bigPanel:
            print "setting next panel - " + str(panel)
            self.nextPanel = panel
            self.nextPanelPos = pos
            return

        print "big panel - " + str(panel)
        self.bigPanel = panel
        # make sure it draws on top of other frames
        panel.reparentTo(self.enlargedPanelNode)
        # make the panel enlarge upon rollover
        panel.setScale(panel.getScale() * SCALE_FACTOR)
        if panel.summonButton:
            panel.summonButton.show()
            panel.summonButton['state'] = DGG.NORMAL

    def shrink(self, panel, pos):
        print 'trying to shrink - ' + str(panel)
        # calling shrink on a panel that's not enlarged
        if panel != self.bigPanel:
            self.nextPanel = None
            return

        print 'shrink panel - ' + str(panel)
        self.bigPanel = None
        # make the panel shrink on rollover exit
        panel.setScale(panel.scale)
        # draw it normally with respect to the others
        panel.reparentTo(self.panelNode)
        if panel.summonButton:
            panel.summonButton.hide()
            panel.summonButton['state'] = DGG.DISABLED

        if self.nextPanel:
            self.grow(self.nextPanel, self.nextPanelPos)



    def toggleRadar(self, deptNum):
        messenger.send('wakeup')

        # toggle the cog/building radar display
        if self.radarOn[deptNum]:
            self.radarOn[deptNum] = 0
        else:
            self.radarOn[deptNum] = 1

        # figure out which panels are effected
        deptSize = SuitDNA.suitsPerDept
        panels = self.panels[deptSize*deptNum:SuitDNA.suitsPerDept*(deptNum+1)]

        if self.radarOn[deptNum]:
            # if we have a handle to the suit planner
            if hasattr(base.cr, 'currSuitPlanner'):
                # make sure we are on a street w/ a suit planner
                if base.cr.currSuitPlanner != None:
                    # ask the suit planner for a list of suits
                    base.cr.currSuitPlanner.d_suitListQuery()
                    # wait for the repsonse to come back from the suit planner
                    self.acceptOnce('suitListResponse', self.updateCogRadar,
                                    extraArgs=[deptNum, panels])
                    # start a timeout in case we never hear back from the suit planner
                    taskMgr.doMethodLater(1.0, self.suitListResponseTimeout,
                                          'suitListResponseTimeout-later',
                                          extraArgs = (deptNum, panels))
                    # if building radar is also enabled
                    if self.radarButtons[deptNum].building:
                        # ask the suit planner for a list of buildings
                        base.cr.currSuitPlanner.d_buildingListQuery()
                        # wait for the repsonse to come back from the suit planner
                        self.acceptOnce('buildingListResponse', self.updateBuildingRadar,
                                        extraArgs=[deptNum])
                        # start a timeout in case we never hear back from the suit planner
                        taskMgr.doMethodLater(1.0, self.buildingListResponseTimeout,
                                              'buildingListResponseTimeout-later',
                                              extraArgs = (deptNum,))
                else:
                    # we must be in a building, put in zeros
                    self.updateCogRadar(deptNum, panels)
                    self.updateBuildingRadar(deptNum)
            else:
                # in a safezone, put zeroes in for the number of suits
                self.updateCogRadar(deptNum, panels)
                self.updateBuildingRadar(deptNum)

            # don't let us hit the button again while updating
            self.radarButtons[deptNum]['state'] = DGG.DISABLED
        else:
            # turn off the radar
            self.updateCogRadar(deptNum, panels)
            self.updateBuildingRadar(deptNum)            


    def suitListResponseTimeout(self, deptNum, panels):
        # ai is not responding, put zeroes in for the number of suits
        self.updateCogRadar(deptNum, panels, 1)

    def buildingListResponseTimeout(self, deptNum):
        # ai is not responding, put zeroes in for the number of buildings
        self.updateBuildingRadar(deptNum, 1)
        
    #
    # util
    #
    def makePanels(self):
        self.panels = []
        base.panels = []
        xStart = -0.66
        yStart = -0.18
        xOffset = 0.199
        yOffset = 0.284
        # for each department
        for dept in range(0, len(SuitDNA.suitDepts)):
            row = []
            # set the color of the panel per dept
            color = PANEL_COLORS[dept]
            # for each type of suit in a dept
            for type in range(0, SuitDNA.suitsPerDept):
                # make a panel
                panel = DirectLabel(
                    parent = self.panelNode,
                    pos = (xStart + (type * xOffset),
                           0.0,
                           yStart - (dept * yOffset)),
                    relief = None,
                    state = DGG.NORMAL,
                    image = self.panelModel,
                    image_scale = (1, 1, 1),
                    image_color = color,
                    text = TTLocalizer.SuitPageMystery,
                    text_scale = 0.045,
                    text_fg = (0, 0, 0, 1),
                    text_pos = (0, 0.185, 0),
                    text_font = ToontownGlobals.getSuitFont(),
                    text_wordwrap = 7
                    )
                # add our special scaling functions
                #panel.bind(DGG.WITHIN, self.grow, extraArgs=[panel])
                #panel.bind(DGG.WITHOUT, self.shrink, extraArgs=[panel])
                #panel.bind(DGG.ENTER, self.grow, extraArgs=[panel])
                #panel.bind(DGG.EXIT, self.shrink, extraArgs=[panel])
                panel.scale = 0.6
                panel.setScale(panel.scale)

                # these will be added as we progress
                panel.quotaLabel = None
                panel.head = None
                panel.shadow = None
                panel.count = 0
                panel.summonButton = None

                # this one which is added now to avoid display timing anomalies 
                self.addCogRadarLabel(panel)
                
                # add the panel to our master list
                self.panels.append(panel)
                base.panels.append(panel)

    def addQuotaLabel(self, panel):
        # figure out the current quota
        index = self.panels.index(panel)
        count = str(base.localAvatar.cogCounts[index])
        if base.localAvatar.cogs[index] < COG_COMPLETE1:
            quota = str(COG_QUOTAS[0][index % SuitDNA.suitsPerDept]) 
        else:
            quota = str(COG_QUOTAS[1][index % SuitDNA.suitsPerDept])
            
        # add the current quota
        quotaLabel = DirectLabel(
            parent = panel,
            pos = (0.0, 0.0, -0.215),
            relief = None,
            state = DGG.DISABLED,
            text = TTLocalizer.SuitPageQuota % (count, quota),
            text_scale = 0.045,
            text_fg = (0, 0, 0, 1),
             text_font = ToontownGlobals.getSuitFont(),
            )
        panel.quotaLabel = quotaLabel

    def addSuitHead(self, panel, suitName):
        panelIndex = self.panels.index(panel)        

        # add the shadow model
        shadow = panel.attachNewNode('shadow')        
        shadowModel = self.shadowModels[panelIndex]
        #shadowModel.setTransparency(0.5)
        shadowModel.copyTo(shadow)
        coords = SHADOW_SCALE_POS[panelIndex]
        shadow.setScale(coords[0])
        shadow.setPos(coords[1], coords[2], coords[3])
        panel.shadow = shadow

        # add the suit head to the panel
        panel.head = Suit.attachSuitHead(panel, suitName)

    def addCogRadarLabel(self, panel):
        # make a label to show cog radar results
        cogRadarLabel = DirectLabel(
            parent = panel,
            pos = (0.0, 0.0, -0.215),
            relief = None,
            state = DGG.DISABLED,
            text = '',
            text_scale = 0.05,
            text_fg = (0, 0, 0, 1),
            text_font = ToontownGlobals.getSuitFont(),
            )
        panel.cogRadarLabel = cogRadarLabel

    def addSummonButton(self, panel):
        # make a button for summoning this cog
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        #okButton = buttons.find('**/ChtBx_OKBtn_UP')
        okButtonList = (buttons.find('**/ChtBx_OKBtn_UP'),
                       buttons.find('**/ChtBx_OKBtn_DN'),
                       buttons.find('**/ChtBx_OKBtn_Rllvr'))
        gui = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
        iconGeom = gui.find('**/summons')
        summonButton = DirectButton(
            parent = panel,
            #pos = (0.1, 0.0, 0.1),
            pos = (0.1, 0.0, -0.13),
            scale = 0.1,
            relief = None,
            state = DGG.NORMAL,
            image = okButtonList,
            image_scale = 13.0,
            geom = iconGeom,
            geom_scale = 0.7,
            text = ("", TTLocalizer.IssueSummons,
                    TTLocalizer.IssueSummons, ""),
            text_scale = 0.4,
            #text_pos = (-0.7, -0.7),
            text_pos = (-1.1, -0.4),
            command = self.summonButtonPressed,
            extraArgs = [panel]
            )
        panel.summonButton = summonButton

    def summonButtonPressed(self, panel):
        panelIndex = self.panels.index(panel)
        self.summonDialog = SummonCogDialog.SummonCogDialog(panelIndex)
        self.summonDialog.load()
        self.accept(self.summonDialog.doneEvent, self.summonDone, extraArgs=[panel])
        self.summonDialog.enter()

    def summonDone(self, panel):
        if self.summonDialog:
            self.summonDialog.unload()
            self.summonDialog = None
        # if there are no summons left, hide the button
        index = self.panels.index(panel)
        if not base.localAvatar.hasCogSummons(index):
            panel.summonButton.hide()
            
    def addBuildingRadarLabel(self, button):
        # make a label to show building radar results
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        # determine where to place it
        zPos = BUILDING_RADAR_POS[self.radarButtons.index(button)]
        buildingRadarLabel = DirectLabel(
            parent = button,
            relief = None,
            pos = (0.225, 0.0, zPos),
            state = DGG.DISABLED,
            image = gui.find('**/avatar_panel'),
            image_hpr = (0, 0, 90),
            image_scale = (0.05, 1, 0.1),
            image_pos = (0, 0, 0.015),
            text = TTLocalizer.SuitPageBuildingRadarP % '0',
            text_scale = 0.05,
            text_fg = (1, 0, 0, 1),
            text_font = ToontownGlobals.getSuitFont(),
            )
        gui.removeNode()
        button.buildingRadarLabel = buildingRadarLabel

    def resetPanel(self, dept, type):
        panel = self.panels[(dept * SuitDNA.suitsPerDept) + type]
        # reset the panel to unseen status
        panel['text'] = TTLocalizer.SuitPageMystery
        if panel.cogRadarLabel:
            panel.cogRadarLabel.hide()
        if panel.quotaLabel:
            panel.quotaLabel.hide()
        if panel.head:
            panel.head.hide()
        if panel.shadow:
            panel.shadow.hide()
        if panel.summonButton:
            panel.summonButton.hide()
            #panel.head.setScale(1.25)
            #panel.shadow.setScale(1.25)
        # set the color of the panel per dept
        color = PANEL_COLORS[dept]
        panel['image_color'] = color
        # hide any building radar labels
        for button in self.radarButtons:
            if button.buildingRadarLabel:
                button.buildingRadarLabel.hide()

    def setPanelStatus(self, panel, status):
        index = self.panels.index(panel)
        if (status == COG_UNSEEN):
            # show nothing but question marks
            panel['text'] = TTLocalizer.SuitPageMystery
        elif (status == COG_BATTLED):
            # show cog name and quota
            suitName = SuitDNA.suitHeadTypes[index]
            suitFullName = SuitBattleGlobals.SuitAttributes[suitName]['name']
            panel['text'] = suitFullName
            # make or show the quota label
            if panel.quotaLabel:
                panel.quotaLabel.show()
            else:
                self.addQuotaLabel(panel)
            # make or show the cog's head
            if panel.head and panel.shadow:
                panel.head.show()
                panel.shadow.show()
            else:
                self.addSuitHead(panel, suitName)
            #make or show the 'issue summons' button
            if base.localAvatar.hasCogSummons(index):
                if panel.summonButton:
                    panel.summonButton.show()
                else:
                    self.addSummonButton(panel)
                # shrink the head slightly
                #panel.head.setScale(panel.head.getScale()*0.75)
                #panel.shadow.setScale(panel.shadow.getScale()*0.75)
        elif status == COG_DEFEATED:
            # update count
            count = str(base.localAvatar.cogCounts[index])
            # determine which quota we are working on
            if base.localAvatar.cogs[index] < COG_COMPLETE1:
                quota = str(COG_QUOTAS[0][index % SuitDNA.suitsPerDept]) 
            else:
                quota = str(COG_QUOTAS[1][index % SuitDNA.suitsPerDept])
            panel.quotaLabel['text'] = TTLocalizer.SuitPageQuota % (count, quota)
        elif status == COG_COMPLETE1:
            # if first quota met show green frame
            panel['image_color'] = PANEL_COLORS_COMPLETE1[(index / SuitDNA.suitsPerDept)]
        elif status == COG_COMPLETE2:
            # if second quota met show gold frame
            panel['image_color'] = PANEL_COLORS_COMPLETE2[index / SuitDNA.suitsPerDept]


    #
    # update calls
    #
    
    def updateAllCogs(self, status):
        # for testing!
        for index in range(0, len(base.localAvatar.cogs)):
            base.localAvatar.cogs[index] = status
        self.updatePage()
        
    def updatePage(self):
        index = 0
        cogs = base.localAvatar.cogs
        # loop through and call updateCogStatus for each cog
        for dept in range(0, len(SuitDNA.suitDepts)):
            for type in range(0, SuitDNA.suitsPerDept):
                self.updateCogStatus(dept, type, cogs[index])
                index += 1
        self.updateCogRadarButtons(base.localAvatar.cogRadar)
        self.updateBuildingRadarButtons(base.localAvatar.buildingRadar)

    def updateCogStatus(self, dept, type, status):
        # make sure they passed in something reasonable
        if ((dept < 0) or (dept > len(SuitDNA.suitDepts))):
             print 'ucs: bad cog dept: ', dept
        elif ((type < 0) or (type > SuitDNA.suitsPerDept)):
            print 'ucs: bad cog type: ', type
        elif ((status < COG_UNSEEN) or (status > COG_COMPLETE2)):
            print 'ucs: bad status: ', status            
        else:
            # go ahead and reset the panel to make sure we can 
            # gracefully switch from one state to any other state
            self.resetPanel(dept, type)
            panel = self.panels[(dept * SuitDNA.suitsPerDept) + type]
            if (status == COG_UNSEEN):
                self.setPanelStatus(panel, COG_UNSEEN)
            elif (status == COG_BATTLED):
                self.setPanelStatus(panel, COG_BATTLED)
            elif status == COG_DEFEATED:
                # this state is a cumulative one
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)                
            elif status == COG_COMPLETE1:
                # this state is a cumulative one
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE1)
            elif status == COG_COMPLETE2:                
                # this state is a cumulative one
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE2)


    def updateCogRadarButtons(self, radars):
        # turn on the appropriate radar button based on 'radars' list
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index]['state'] = DGG.NORMAL            

    def updateCogRadar(self, deptNum, panels, timeout=0):
        # remove timeout task
        taskMgr.remove('suitListResponseTimeout-later')
        # if we haven't timed out get the current suit list
        if (not timeout and hasattr(base.cr, 'currSuitPlanner')
            and base.cr.currSuitPlanner != None):
            cogList = base.cr.currSuitPlanner.suitList
        else:
            cogList = []

        # reset the cog counts for this dept
        for panel in panels:
            panel.count = 0

        # get the latest counts from the suit planner info
        for cog in cogList:
            # the cogs names and panels are 1 to 1 mapping
            self.panels[cog].count  += 1

        # update the cog radar label text for the dept in question
        for panel in panels:
            # update the label text
            panel.cogRadarLabel['text'] = TTLocalizer.SuitPageCogRadar % panel.count
            # case 1: show the radar, hide the quota
            if self.radarOn[deptNum]:
                panel.quotaLabel.hide()
                def showLabel(label):
                    label.show()
                taskMgr.doMethodLater(RADAR_DELAY * panels.index(panel),
                                      showLabel,
                                      'showCogRadarLater',
                                      extraArgs = (panel.cogRadarLabel,))
                def activateButton(s = self, index = deptNum):
                    self.radarButtons[index]['state'] = DGG.NORMAL
                    return Task.done

                if not self.radarButtons[deptNum].building:
                    # If we don't have building radar, we need to
                    # reactivate the button when we're done
                    # displaying. (If we *do* have building radar, the
                    # updateBuildingRadar function will take care of
                    # this.)
                    taskMgr.doMethodLater(RADAR_DELAY * len(panels),
                                          activateButton, 'activateButtonLater')
            # case 2: hide the radar, show the quota
            else:
                panel.cogRadarLabel.hide()
                panel.quotaLabel.show()


    def updateBuildingRadarButtons(self, radars):
        # turn on the appropriate radar ability based on 'radars' list
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index].building = 1            
        
    def updateBuildingRadar(self, deptNum, timeout=0):
        # remove timeout task
        taskMgr.remove('buildingListResponseTimeout-later')
        if (not timeout and hasattr(base.cr, 'currSuitPlanner')
            and base.cr.currSuitPlanner != None):
            buildingList = base.cr.currSuitPlanner.buildingList
        else:
            buildingList = [0, 0, 0, 0]

        # figure out the current number of buildings of this type on this street
        button = self.radarButtons[deptNum]
        if button.building:
            # make sure we have a buildingRadarLabel first
            if not button.buildingRadarLabel:
                self.addBuildingRadarLabel(button)
            # case 1: show the radar (after a delay)
            if self.radarOn[deptNum]:
                num = buildingList[deptNum]
                if num == 1:
                    button.buildingRadarLabel['text'] = TTLocalizer.SuitPageBuildingRadarS % num
                else:
                    button.buildingRadarLabel['text'] = TTLocalizer.SuitPageBuildingRadarP % num
                def showLabel(button):
                    button.buildingRadarLabel.show()
                    # last but not least, turn the radar button back on
                    button['state'] = DGG.NORMAL
                taskMgr.doMethodLater(RADAR_DELAY * SuitDNA.suitsPerDept,
                                      showLabel,
                                      'showBuildingRadarLater',
                                      extraArgs = (button,))
            # case 2: hide the radar
            else:
                button.buildingRadarLabel.hide()





