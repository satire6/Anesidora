#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Oct 2008
#
# Purpose: PartyEditorListElements hold details of activities and decorations
#          that populate the scrolled list of the party editor.  When clicked
#          they spawn PartyEditorGridElements
#-------------------------------------------------------------------------------

from pandac.PandaModules import Vec3

from direct.gui.DirectGui import DirectButton, DirectLabel
from direct.gui import DirectGuiGlobals

from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
from toontown.parties.PartyEditorGridElement import PartyEditorGridElement
from toontown.parties.PartyUtils import getPartyActivityIcon

class PartyEditorListElement(DirectButton):
    """
    PartyEditorListElements are descriptions of activities and decorations that
    when clicked spawn PartyEditorGridElements
    """
    notify = directNotify.newCategory("PartyEditorListElement")
    
    def __init__(self, partyEditor, id, isDecoration=False, **kw):        
        self.partyEditor = partyEditor
        self.id = id
        self.isDecoration = isDecoration
        self.unreleased = self.calcUnreleased(id)
        self.comingSoonTextScale = 1.0

        # Change the name and the up, down, rollover, and disabled colors
        if self.isDecoration:
            self.name = TTLocalizer.PartyDecorationNameDict[self.id]["editor"]
            colorList = ( (1.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 1.0, 1.0), (0.5, 0.5, 0.5, 1.0))
            assetName = PartyGlobals.DecorationIds.getString(self.id)
            if assetName == "Hydra":
                assetName = "StageSummer"
            geom = self.partyEditor.decorationModels.find("**/partyDecoration_%s"%assetName)
            if geom.isEmpty() or self.unreleased:
                # we give to much away as the icon looks exactly like the decr
                helpGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_help')
                helpImageList = (helpGui.find('**/tt_t_gui_brd_helpUp'),
                             helpGui.find('**/tt_t_gui_brd_helpDown'),
                             helpGui.find('**/tt_t_gui_brd_helpHover'),
                             helpGui.find('**/tt_t_gui_brd_helpDown'),)
                geom = helpImageList[2]
                geom3_color = (0.5, 0.5, 0.5, 1.0)
                scale = Vec3(2.5, 2.5, 2.5)
                geom_pos = (0.0, 0.0, 0.0)
                # coming soon text scale is higly dependent on the icon scale
                self.comingSoonTextScale = 0.035
            else:
                geom_pos = (0.0, 0.0, -3.0)
                geom3_color = (0.5, 0.5, 0.5, 1.0)
                scale = Vec3(0.06, 0.0001, 0.06)
                
                # Give these tall icons a bit more head room.
                if self.id in [PartyGlobals.DecorationIds.CogStatueVictory, 
                               PartyGlobals.DecorationIds.TubeCogVictory,
                               PartyGlobals.DecorationIds.cogIceCreamVictory]:
                    geom_pos = (0.0, 0.0, -3.9)
                    scale = Vec3(0.05, 0.0001, 0.05)
                
        else:
            self.name = TTLocalizer.PartyActivityNameDict[self.id]["editor"]
            colorList = ( (0.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.5, 0.5, 0.5, 1.0))
            iconString = PartyGlobals.ActivityIds.getString(self.id)
            if self.id == PartyGlobals.ActivityIds.PartyJukebox40:
                iconString = PartyGlobals.ActivityIds.getString(PartyGlobals.ActivityIds.PartyJukebox)
            elif self.id == PartyGlobals.ActivityIds.PartyDance20:
                iconString = PartyGlobals.ActivityIds.getString(PartyGlobals.ActivityIds.PartyDance)
            
            geom = getPartyActivityIcon(self.partyEditor.activityIconsModel, iconString)

            scale = 0.35
            geom3_color = (0.5, 0.5, 0.5, 1.0)
            geom_pos = (0.0, 0.0, 0.0)
            # coming soon text scale is higly dependent on the icon scale
            self.comingSoonTextScale = 0.25

        #self.icon.setPos(self.partyEditor.partyPlanner.gui.find("**/step_05_activitiesIcon_locator").getPos())
        #self.icon.reparentTo(self.partyEditor.parent)
        #self.icon.stash()

        optiondefs = (
            ('geom', geom, None),
            ('geom3_color', geom3_color, None),
            ('geom_pos', geom_pos, None),
            ('relief', None, None),
        )
        
        # Merge keyword options with default options, plus, this call makes
        # DirectButton work... that and the initializeoptions below... without
        # those two calls, strange... and I mean hard to debug, stuff happens.
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self,self.partyEditor.elementList)
        self.initialiseoptions(PartyEditorListElement)
        self.setName("%sListElement"%self.name)

        self.setScale(scale)

        # Since normal buttons only call their command methods upon release
        # of the mouse button, we will not specify a command method and
        # instead bind our own methods to press and release.
        self.bind(DirectGuiGlobals.B1PRESS, self.clicked)
        self.bind(DirectGuiGlobals.B1RELEASE, self.released)
        
        self.partyEditorGridElements = []
        if self.isDecoration:
            for i in range(PartyGlobals.DecorationInformationDict[self.id]["limitPerParty"]):
                self.partyEditorGridElements.append(PartyEditorGridElement(self.partyEditor, self.id, self.isDecoration, self.checkSoldOutAndPaidStatusAndAffordability))
        else:
            for i in range(PartyGlobals.ActivityInformationDict[self.id]["limitPerParty"]):
                self.partyEditorGridElements.append(PartyEditorGridElement(self.partyEditor, self.id, self.isDecoration, self.checkSoldOutAndPaidStatusAndAffordability))
        self.activeGridElementIndex = -1

               
        
        self.adjustForUnreleased()

    def calcUnreleased(self, id):
        """Calculate if we are presented as unreleased."""
        if base.cr.partyManager.allowUnreleasedClient():
            # a magic word is forcing all items to be available
            self.unreleased = False
        else:
            if self.isDecoration:
                self.unreleased = (id in PartyGlobals.UnreleasedDecorationIds)
            else:
                self.unreleased = (id in PartyGlobals.UnreleasedActivityIds)

        return self.unreleased

    def adjustForUnreleased(self):
        """If we are unreleased, change state and text."""
        if self.unreleased:
            textScale = self.comingSoonTextScale
            comingSoon = DirectLabel(
                parent = self,
                text = TTLocalizer.PartyPlannerComingSoon,
                text_scale = textScale,
                text_fg = (1.0, 0, 0, 1.0),
                text_shadow = (0, 0, 0, 1),
                relief = None,
                )
            self["state"] = DirectGuiGlobals.DISABLED
            
 
    def clearPartyGrounds(self):
        for gridElement in self.partyEditorGridElements:
            gridElement.removeFromGrid()
            
    def elementSelectedFromList(self):
        """
        This element has been scrolled to in the list, replace the price and
        description text with it's own
        """
        PartyEditorListElement.notify.debug("Element %s clicked" % self.name)
        if self.isDecoration:
            self.partyEditor.partyPlanner.elementDescriptionNode.setText(TTLocalizer.PartyDecorationNameDict[self.id]["description"])
            self.partyEditor.partyPlanner.elementPriceNode.setText("%d %s" % ( PartyGlobals.DecorationInformationDict[self.id]["cost"], TTLocalizer.PartyPlannerBeans))
            self.partyEditor.partyPlanner.elementTitleLabel["text"] = self.name
        else:
            self.partyEditor.partyPlanner.elementDescriptionNode.setText(TTLocalizer.PartyActivityNameDict[self.id]["description"])
            self.partyEditor.partyPlanner.elementPriceNode.setText("%d %s" % ( PartyGlobals.ActivityInformationDict[self.id]["cost"], TTLocalizer.PartyPlannerBeans))
            self.partyEditor.partyPlanner.elementTitleLabel["text"] = self.name
        self.checkSoldOutAndPaidStatusAndAffordability()

    def checkSoldOutAndPaidStatusAndAffordability(self):
        # Only set my state visually if I'm the currently selected element
        if self.partyEditor.currentElement != self:
            if self.partyEditor.currentElement is not None:
                self.partyEditor.currentElement.checkSoldOutAndPaidStatusAndAffordability()
            return

        if self.isDecoration:
            infoDict = PartyGlobals.DecorationInformationDict
        else:
            infoDict = PartyGlobals.ActivityInformationDict
        
        # First check to see if they are allowed to get it based on whether they
        # are a paying customer or not.
        if not base.cr.isPaid() and infoDict[self.id]["paidOnly"]:
            self.setOffLimits()
            return

        # Then check to see if they can afford it given the current state of
        # the party they are planning.
        if infoDict[self.id]["cost"] > self.partyEditor.partyPlanner.totalMoney - self.partyEditor.partyPlanner.totalCost:
            self.setTooExpensive(True)
            tooExpensive = True
        else:
            self.setTooExpensive(False)
            tooExpensive = False

        # Finally, see if the darn thing is sold out or not.
        for i in range(len(self.partyEditorGridElements)):
            if not self.partyEditorGridElements[i].overValidSquare:
                if not tooExpensive:
                    self.setSoldOut(False)
                return
        # If we got this far, then all the elements have been used up
        self.setSoldOut(True)

    def setOffLimits(self):
        self["state"] = DirectGuiGlobals.DISABLED
        self.partyEditor.partyPlanner.elementBuyButton["text"] = TTLocalizer.PartyPlannerPaidOnly
        self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.DISABLED
        self.partyEditor.partyPlanner.elementBuyButton["text_scale"] = 0.04

    def setTooExpensive(self, value):
        self.partyEditor.partyPlanner.elementBuyButton["text"] = TTLocalizer.PartyPlannerBuy
        if value:
            self["state"] = DirectGuiGlobals.DISABLED
            self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.DISABLED
        else:
            self["state"] = DirectGuiGlobals.NORMAL
            self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.NORMAL

    def setSoldOut(self, value):
        if value:
            self["state"] = DirectGuiGlobals.DISABLED
            self.partyEditor.partyPlanner.elementBuyButton["text"] = TTLocalizer.PartyPlannerSoldOut
            self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.DISABLED
        else:
            self["state"] = DirectGuiGlobals.NORMAL
            self.partyEditor.partyPlanner.elementBuyButton["text"] = TTLocalizer.PartyPlannerBuy
            self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.NORMAL

        # unreleased overrides this
        if self.unreleased:
            self["state"] = DirectGuiGlobals.DISABLED
            self.partyEditor.partyPlanner.elementBuyButton["text"] = TTLocalizer.PartyPlannerCantBuy
            self.partyEditor.partyPlanner.elementBuyButton["state"] = DirectGuiGlobals.DISABLED

    def clicked(self, mouseEvent):
        PartyEditorListElement.notify.debug("Element %s's icon was clicked" % self.name)
        self.partyEditor.listElementClicked()
        for i in range(len(self.partyEditorGridElements)):
            if not self.partyEditorGridElements[i].overValidSquare:
                self.partyEditorGridElements[i].attach(mouseEvent)
                self.activeGridElementIndex = i
                return

    def buyButtonClicked(self, desiredXY=None):
        for i in range(len(self.partyEditorGridElements)):
            if not self.partyEditorGridElements[i].overValidSquare:
                if self.partyEditorGridElements[i].placeInPartyGrounds(desiredXY):
                    self.activeGridElementIndex = i
                    return True
                else:
                    self.checkSoldOutAndPaidStatusAndAffordability()
                    return False

    def released(self, mouseEvent):
        PartyEditorListElement.notify.debug("Element %s's icon was released" % self.name)
        self.partyEditor.listElementReleased()
        if self.activeGridElementIndex != -1:
            self.partyEditorGridElements[self.activeGridElementIndex].detach(mouseEvent)

    def destroy(self):
        self.unbind(DirectGuiGlobals.B1PRESS)
        self.unbind(DirectGuiGlobals.B1RELEASE)
        for partyEditorGridElement in self.partyEditorGridElements:
            partyEditorGridElement.destroy()
        del self.partyEditorGridElements
        # break the cycle to clean up properly
        self.partyEditor = None
        DirectButton.destroy(self)

        
