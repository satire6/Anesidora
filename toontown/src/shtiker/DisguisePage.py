"""DisguisePage module: contains the DisguisePage class"""

import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.suit import SuitDNA
from toontown.battle import SuitBattleGlobals
from toontown.minigame import MinigamePowerMeter
from toontown.coghq import CogDisguiseGlobals

# colors for cog background panels
DeptColors = (
    # bossbots
    Vec4(0.647, 0.608, 0.596, 1.000),
    # lawbots
    Vec4(0.588, 0.635, 0.671, 1.000),
    # cashbots
    Vec4(0.596, 0.714, 0.659, 1.000),
    # sellbots
    Vec4(0.761, 0.678, 0.690, 1.000),
    )
    
NumParts = max(CogDisguiseGlobals.PartsPerSuit)

PartNames = (
    "lUpleg", "lLowleg", "lShoe",
    "rUpleg", "rLowleg", "rShoe",
    "lShoulder", "rShoulder", "chest", "waist", "hip",
    "lUparm", "lLowarm", "lHand",
    "rUparm", "rLowarm", "rHand",
    )

class DisguisePage(ShtikerPage.ShtikerPage):

    meterColor = Vec4(0.87, 0.87, 0.827, 1.0)
    meterActiveColor = Vec4(0.7,0.3,0.3,1)

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        # default to bossbot info
        self.activeTab = 0
        self.progressTitle = None
        
    def load(self):
        ShtikerPage.ShtikerPage.load(self)

        # load the gui
        gui = loader.loadModel("phase_9/models/gui/cog_disguises")
        
        # make a frame for the background
        self.frame = DirectFrame(
            parent = self,
            relief = None,
            scale = 0.47,
            pos = (0.02,1,0),
            )

        # Add a background panel
        self.bkgd = DirectFrame(
            parent = self.frame,
            geom = gui.find('**/base'),
            relief = None,
            scale = (0.98,1,1),
            )
        # Dont use texture's color
        self.bkgd.setTextureOff(1)

        # make the tab text
        self.tabs = []
        self.pageFrame = DirectFrame(parent = self.frame, relief = None)
        
        for dept in SuitDNA.suitDepts:
            if dept == 'c':
                # Bossbot
                tabIndex = 1
                textPos = (1.57,0.75)
            elif dept == 'l':
                # Lawbot
                tabIndex = 2
                textPos = (1.57,0.12)
            elif dept == 'm':
                # Cashbot
                tabIndex = 3
                textPos = (1.57,-0.47)
            elif dept == 's':
                # Sellbot
                tabIndex = 4
                textPos = (1.57,-1.05)

            pageGeom = gui.find('**/page%d' % tabIndex)
            tabGeom = gui.find('**/tab%d' % tabIndex)

            tab = DirectButton(
                parent = self.pageFrame,
                relief = None,
                geom = tabGeom,
                geom_color = DeptColors[tabIndex-1],
                text = SuitDNA.suitDeptFullnames[dept],
                text_font = ToontownGlobals.getSuitFont(),
                text_pos = textPos,
                text_roll = -90,
                text_scale = TTLocalizer.DPtab,
                text_align = TextNode.ACenter,
                # Press
                text1_fg = Vec4(1,0,0,1),
                # Highlight
                text2_fg = Vec4(0.5,0.4,0.4,1),
                # Disabled
                text3_fg = Vec4(0.4,0.4,0.4,1),
                command = self.doTab,
                extraArgs = [len(self.tabs)],
                # Don't scale down tab on press
                pressEffect = 0,
                )
            self.tabs.append(tab)

            page = DirectFrame(
                parent = tab,
                relief = None,
                geom = pageGeom,
                )

        self.deptLabel = DirectLabel(
            parent = self.frame,
            text = '',
            text_font = ToontownGlobals.getSuitFont(),
            text_scale = TTLocalizer.DPdeptLabel,
            text_pos = (-0.1, 0.8),
            )

        # Pipes surrounding gui
        DirectFrame(
            parent = self.frame,
            relief = None,
            geom = gui.find("**/pipe_frame"),
            )

        # HACK - these don't need to be stored locally (just for debugging)
        self.tube = DirectFrame(
            parent = self.frame,
            relief = None,
            geom = gui.find("**/tube"),
            )
        
        # Suit's Face
        DirectFrame(
            parent = self.frame,
            relief = None,
            geom = gui.find("**/robot/face"),
            )

        # Title for title bar
        DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_cog_disguises'),
            geom_pos = (0,.1,0),
            )

        # Title for Merit progress readout (sellbot)
        self.meritTitle = DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_merit_progress'),
            geom_pos = (0,.1,0),
            )
        self.meritTitle.hide()

        # Title for Cogbuck progress readout (cashbot)
        self.cogbuckTitle = DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_cashbuck_progress'),
            geom_pos = (0,.1,0),
            )
        self.cogbuckTitle.hide()

        # Title for Jury Notice progress readout (lawbot)
        self.juryNoticeTitle = DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_jury_notice_progress'),
            geom_pos = (0,.1,0),
            )
        self.juryNoticeTitle.hide()

        # Title for Stock Option progress readout (bossbot)
        self.stockOptionTitle = DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_stock_option_progress'),
            geom_pos = (0,.1,0),
            )
        self.stockOptionTitle.hide()

        # will need two more 'merit' progress titles eventually
        self.progressTitle = self.meritTitle
        
        self.promotionTitle = DirectLabel(
            parent = self.frame,
            relief = None,
            geom = gui.find('**/text_ready4promotion'),
            geom_pos = (0,.1,0),
            )

        # make the cog name label
        self.cogName = DirectLabel(
            parent = self.frame,
            relief = None,
            text = "",
            text_font = ToontownGlobals.getSuitFont(),
            text_scale = TTLocalizer.DPcogName,
            text_align = TextNode.ACenter,
            pos = (-0.948, 0, -1.15),
            )

        # make the cog level label
        self.cogLevel = DirectLabel(
            parent = self.frame,
            relief = None,
            text = "",
            text_font = ToontownGlobals.getSuitFont(),
            text_scale = 0.09,
            text_align = TextNode.ACenter,
            pos = (-0.91, 0, -1.02),            
            )

        # this will let us globally scale and position the various parts
        self.partFrame = DirectFrame(
            parent = self.frame,
            relief = None,
            )

        # these are the cog parts when present
        self.parts = []
        for partNum in range(0, NumParts):
            self.parts.append(
                DirectFrame(
                    parent = self.partFrame,
                    relief = None,
                    geom = gui.find("**/robot/" + PartNames[partNum]),
                    )
                )

            #self.parts[partNum].hide()

        # these are the holes when the cog parts are absent
        self.holes = []
        for partNum in range(0, NumParts):
            self.holes.append(
                DirectFrame(
                    parent = self.partFrame,
                    relief = None,
                    geom = gui.find("**/robot_hole/" + PartNames[partNum]),
                    )
                )
        
        # make the cog part label
        self.cogPartRatio = DirectLabel(
            parent = self.frame,
            relief = None,
            text = "",
            text_font = ToontownGlobals.getSuitFont(),
            text_scale = 0.08,
            text_align = TextNode.ACenter,
            pos = (-0.91, 0, -0.82),            
            )

        # make the cog part label
        self.cogMeritRatio = DirectLabel(
            parent = self.frame,
            relief = None,
            text = "",
            text_font = ToontownGlobals.getSuitFont(),
            text_scale = 0.08,
            text_align = TextNode.ACenter,
            pos = (0.45, 0, -0.36),
            )

        meterFace = gui.find('**/meter_face_whole')
        meterFaceHalf = gui.find('**/meter_face_half')

        self.meterFace = DirectLabel(parent = self.frame,
                                     relief = None,
                                     geom = meterFace,
                                     color = self.meterColor,
                                     pos = (0.455, 0.00, 0.04))
        self.meterFaceHalf1 = DirectLabel(parent = self.frame,
                                          relief = None,
                                          geom = meterFaceHalf,
                                          color = self.meterActiveColor,
                                          pos = (0.455, 0.00, 0.04))
        self.meterFaceHalf2 = DirectLabel(parent = self.frame,
                                          relief = None,
                                          geom = meterFaceHalf,
                                          color = self.meterColor,
                                          pos = (0.455, 0.00, 0.04))

        self.frame.hide()
        # Start with Sellbot page visible for first factory
        self.activeTab = 3
        self.updatePage()
        
    def unload(self):
        # call parent class unload
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        self.frame.show()
        ShtikerPage.ShtikerPage.enter(self)
        
    def exit(self):
        self.frame.hide()        
        ShtikerPage.ShtikerPage.exit(self)

    # updates
        
    def updatePage(self):
        self.doTab(self.activeTab)

    def updatePartsDisplay(self, index, numParts, numPartsRequired):
        # we cleverly made the part gui elements in the same order as
        # as the parts bitmask so we can simply loop over them as so:
        partBitmask = 1
        # the groupingBitmask helps us map smaller numbers of cog parts
        # onto the full cog parts display. The bitmask works as such:
        #
        #    left leg upper = 001
        #    left leg lower = 010
        #    left leg foot  = 100
        #
        # so if the grouping bit mask read 001 it would indicate that
        # if "left leg upper" is present consider it a whole leg. Thus
        # effectively mapping one part onto three. If it read 011, it would
        # mean that this is a two part leg (consider the foot part of the
        # lower leg). Etc.
        #
        groupingBitmask = CogDisguiseGlobals.PartsPerSuitBitmasks[index]             
        # previous part helps us map smaller numbers of cog parts onto the
        # full cog parts displays. It determines if the only part we really
        # care about (a 1 in the groupingBitmask) was present and what
        # it's status was.
        #
        # 0 = no previous part was present
        # 1 = previous part present
        previousPart = 0

        for part in self.parts:
            groupingBit = groupingBitmask & partBitmask

            #print "not groupingBit and previousPart = %d and %d = %d" % (not groupingBit,
            #                                                             previousPart,
            #                                                             (not groupingBit and previousPart))
            #print "(%d & %d) & %d = \n %d & %d = %d" % (numParts, partBitmask, groupingBit,
            #                                            (numParts & partBitmask), groupingBit,
            #                                            (numParts & partBitmask) & groupingBit)

            # if we have the part
            if (numParts & partBitmask)& groupingBit:
                part.show()
                self.holes[self.parts.index(part)].hide()
                # mark the previous part as present
                if groupingBit:
                    previousPart = 1
            # if we don't have the part, but the part is a don't care
            elif (not groupingBit and previousPart):
                part.show()
                self.holes[self.parts.index(part)].hide()                
            # else we don't have the part
            else:
                self.holes[self.parts.index(part)].show()                
                part.hide()
                previousPart = 0

            #print "previousPart = ", previousPart
            
            # shift the mask to look at the next bit
            partBitmask = partBitmask << 1

    def updateMeritBar(self, dept):
        # Update guage
        merits = base.localAvatar.cogMerits[dept]
        totalMerits = CogDisguiseGlobals.getTotalMerits(
            base.localAvatar, dept)
        if totalMerits == 0:
            progress = 1
        else:
            progress = min(merits/float(totalMerits), 1)
        self.updateMeritDial(progress)

        if base.localAvatar.readyForPromotion(dept):
            self.cogMeritRatio['text'] = TTLocalizer.DisguisePageMeritFull
            self.promotionTitle.show()
            self.progressTitle.hide()
        else:
            self.cogMeritRatio['text'] = "%d/%d" % (merits, totalMerits)
            self.promotionTitle.hide()
            self.progressTitle.show()

    def updateMeritDial(self, progress):
        # Progress from 0 to 1
        if (progress == 0):
            # Show empty dial
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
            self.meterFace.setColor(self.meterColor)
        elif (progress == 1):
            # Show completely full dial
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
            self.meterFace.setColor(self.meterActiveColor)
        else:
            # Show partially full dial
            self.meterFaceHalf1.show()
            self.meterFaceHalf2.show()
            self.meterFace.setColor(self.meterColor)
            if progress < 0.5:
                self.meterFaceHalf2.setColor(self.meterColor)
            else:
                self.meterFaceHalf2.setColor(self.meterActiveColor)
                progress = progress - 0.5
            # Turn dial accordingly
            self.meterFaceHalf2.setR(180 * (progress/0.5))

    ## CALLBACKS
    def doTab(self, index):
        self.activeTab = index
        self.tabs[index].reparentTo(self.pageFrame)
        # update the tab buttons
        for i in range(len(self.tabs)):
            tab = self.tabs[i]
            if i == index:
                tab['text0_fg'] = (1, 0, 0, 1)
                tab['text2_fg'] = (1, 0, 0, 1)
            else:
                tab['text0_fg'] = (0, 0, 0, 1)
                tab['text2_fg'] = (0.5,0.4,0.4,1)
        # Set background color
        self.bkgd.setColor(DeptColors[index])
        # Update the label
        self.deptLabel['text'] = SuitDNA.suitDeptFullnames[
            SuitDNA.suitDepts[index]],
        # determine the offset in head array for this dept
        cogIndex = (base.localAvatar.cogTypes[index] +
                    (SuitDNA.suitsPerDept * index))
        cog = SuitDNA.suitHeadTypes[cogIndex]
        # update the gui
        self.progressTitle.hide()
        if SuitDNA.suitDepts[index] == 'm':
            self.progressTitle = self.cogbuckTitle
        elif SuitDNA.suitDepts[index] == 'l':
            self.progressTitle = self.juryNoticeTitle
        elif SuitDNA.suitDepts[index] == 'c':
            self.progressTitle = self.stockOptionTitle
        else:
            self.progressTitle = self.meritTitle
        self.progressTitle.show()
        self.cogName['text'] = SuitBattleGlobals.SuitAttributes[cog]['name']
        cogLevel = base.localAvatar.cogLevels[index]        
        self.cogLevel['text'] = (TTLocalizer.DisguisePageCogLevel  %
                                 str(cogLevel + 1))
        numParts = base.localAvatar.cogParts[index]
        numPartsRequired = CogDisguiseGlobals.PartsPerSuit[index]
        self.updatePartsDisplay(index, numParts, numPartsRequired)
        self.updateMeritBar(index)
        self.cogPartRatio['text'] = (
            "%d/%d" %
            (CogDisguiseGlobals.getTotalParts(numParts), numPartsRequired))
        

