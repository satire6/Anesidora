"""BodyShop module: contains the BodyShop class"""

from pandac.PandaModules import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from MakeAToonGlobals import *
import random
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TeaserPanel
import ShuffleButton

class BodyShop(StateData.StateData):
    """
    BodyShop class: contains methods for changing the Avatar's
    head, torso, and legs via user input
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("BodyShop")

    def __init__(self, doneEvent):
        """
        Set-up the body shop interface to change body parts on the
        given toon
        """
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.torsoChoice = 0
        self.legChoice = 0
        self.headChoice = 0
        self.speciesChoice = 0

    def enter(self, toon, shopsVisited=[]):
        # turn off any user control
        base.disableMouse()

        # load up the given toon
        self.toon = toon
        self.dna = self.toon.getStyle()
        gender = self.toon.style.getGender()
        
        self.speciesStart = self.getSpeciesStart()
        self.speciesChoice = self.speciesStart
        self.headStart = 0
        self.headChoice = ToonDNA.toonHeadTypes.index(self.dna.head) - ToonDNA.getHeadStartIndex(self.species)
        self.torsoStart = 0
        self.torsoChoice = ToonDNA.toonTorsoTypes.index(self.dna.torso) % 3        
        self.legStart = 0
        self.legChoice = ToonDNA.toonLegTypes.index(self.dna.legs)

        if CLOTHESSHOP in shopsVisited:
            self.clothesPicked = 1
        else:
            self.clothesPicked = 0
        self.clothesPicked = 1
            
        if (gender == 'm' or 
            ToonDNA.GirlBottoms[self.dna.botTex][1] == ToonDNA.SHORTS):
            torsoStyle = 's'
            torsoPool = ToonDNA.toonTorsoTypes[:3]
        else:
            torsoStyle = 'd'
            torsoPool = ToonDNA.toonTorsoTypes[3:6]
        
        # update the clothes and eye lashes, just in case
        self.__swapSpecies(0)
        self.__swapHead(0)
        self.__swapTorso(0)
        self.__swapLegs(0)
            
        choicePool = [ToonDNA.toonHeadTypes, torsoPool, ToonDNA.toonLegTypes]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeBody)

        # set up the "last" button
        self.acceptOnce("last", self.__handleBackward)
        # set up the "next" button
        self.accept("next", self.__handleForward)
        
        self.acceptOnce("MAT-newToonCreated", self.shuffleButton.cleanHistory)

        # possibly override the last hook
        self.restrictHeadType(self.dna.head)

    def getSpeciesStart(self):
        """
        Gives the start of the species scroll list. The start should be the
        species it started with.
        """
        for species in ToonDNA.toonSpeciesTypes:
            if (species == self.dna.head[0]):
                self.species = species
                return ToonDNA.toonSpeciesTypes.index(species)

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()
        self.memberButton.hide()
        
    def exit(self):
        """
        Remove events and restore display
        """
        try:
            del self.toon
        except:
            self.notify.warning("BodyShop: toon not found")
            
        self.hideButtons()
        
        self.ignore("last")
        self.ignore("next")
        self.ignore("enter")
        self.ignore(self.shuffleFetchMsg)

    def load(self):
        # Create the Body Room
        self.gui = loader.loadModel("phase_3/models/gui/tt_m_gui_mat_mainGui")
        guiRArrowUp = self.gui.find("**/tt_t_gui_mat_arrowUp")
        guiRArrowDown = self.gui.find("**/tt_t_gui_mat_arrowDown")
        guiRArrowRollover = self.gui.find("**/tt_t_gui_mat_arrowUp")
        guiRArrowDisabled = self.gui.find("**/tt_t_gui_mat_arrowDisabled")
        
        shuffleFrame = self.gui.find("**/tt_t_gui_mat_shuffleFrame")
        shuffleArrowUp = self.gui.find("**/tt_t_gui_mat_shuffleArrowUp")
        shuffleArrowDown = self.gui.find("**/tt_t_gui_mat_shuffleArrowDown")
        shuffleArrowRollover = self.gui.find("**/tt_t_gui_mat_shuffleArrowUp")
        shuffleArrowDisabled = self.gui.find("**/tt_t_gui_mat_shuffleArrowDisabled")
        
        self.upsellModel = loader.loadModel("phase_3/models/gui/tt_m_gui_ups_mainGui")
        upsellTex = self.upsellModel.find("**/tt_t_gui_ups_banner")
        
        # Create an emtpy frame which houses all the option buttons including the shuffle button.
        self.parentFrame = DirectFrame(
            relief = DGG.RAISED,
            pos = (0.98, 0, 0.416),
            frameColor = (1, 0, 0, 0),
            )
        
        # Create the Species Frame.
        self.speciesFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.073),
            hpr = (0, 0, 0),
            scale = 1.3,
            frameColor = (1, 1, 1, 1),
            text = "Species",
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.speciesLButton = DirectButton(
            parent = self.speciesFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapSpecies,
            extraArgs = [-1],
            )
            
        self.speciesRButton = DirectButton(
            parent = self.speciesFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapSpecies,
            extraArgs = [1],
            )
        
        # Create the Head Frame.
        self.headFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.3),
            hpr = (0, 0, 2),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.BodyShopHead,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.headLButton = DirectButton(
            parent = self.headFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapHead,
            extraArgs = [-1],
            )
            
        self.headRButton = DirectButton(
            parent = self.headFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapHead,
            extraArgs = [1],
            )

        # Create the Body Frame.
        self.bodyFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonScale,
            relief = None,
            pos = (0, 0, -0.5),
            hpr = (0, 0, -2),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.BodyShopBody,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.torsoLButton = DirectButton(
            parent = self.bodyFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapTorso,
            extraArgs = [-1],
            )

        self.torsoRButton = DirectButton(
            parent = self.bodyFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapTorso,
            extraArgs = [1],
            )

        # Create the Legs Frame.
        self.legsFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.7),
            hpr = (0, 0, 3),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.BodyShopLegs,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.legLButton = DirectButton(
            parent = self.legsFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapLegs,
            extraArgs = [-1],
            )

        self.legRButton = DirectButton(
            parent = self.legsFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapLegs,
            extraArgs = [1],
            )
            
        self.memberButton = DirectButton(
            relief = None,
            image = (upsellTex, upsellTex, upsellTex, upsellTex),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            scale = 0.9,
            pos = (0, 0, -0.84),
            command = self.__restrictForward,
            )

        self.parentFrame.hide()
        self.memberButton.hide()
        
        self.shuffleFetchMsg = 'BodyShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)

    def unload(self):
        self.gui.removeNode()
        del self.gui
        
        self.upsellModel.removeNode()
        del self.upsellModel

        self.parentFrame.destroy()
        self.speciesFrame.destroy()
        self.headFrame.destroy()
        self.bodyFrame.destroy()
        self.legsFrame.destroy()
        self.speciesLButton.destroy()
        self.speciesRButton.destroy()
        self.headLButton.destroy()
        self.headRButton.destroy()
        self.torsoLButton.destroy()
        self.torsoRButton.destroy()
        self.legLButton.destroy()
        self.legRButton.destroy()
        self.memberButton.destroy()

        del self.parentFrame
        del self.speciesFrame
        del self.headFrame
        del self.bodyFrame
        del self.legsFrame
        del self.speciesLButton
        del self.speciesRButton
        del self.headLButton
        del self.headRButton
        del self.torsoLButton
        del self.torsoRButton
        del self.legLButton
        del self.legRButton
        del self.memberButton
        
        self.shuffleButton.unload()
        self.ignore("MAT-newToonCreated")

    # event handlers

    def __swapTorso(self, offset):
        # if this is the first time through only choose from naked torsos
        # (they are at 6-8)
        gender = self.toon.style.getGender()
        if not (self.clothesPicked):
            length = len(ToonDNA.toonTorsoTypes[6:])
            torsoOffset =  6
        # otherwise use either the male or female clothed torsos
        else:
            # Note: we need to correct colors that are not cross-gender
            # male (0-2)
            if (gender == 'm'):
                length = len(ToonDNA.toonTorsoTypes[:3])
                torsoOffset = 0
                if self.dna.armColor not in ToonDNA.defaultBoyColorList:
                    self.dna.armColor = ToonDNA.defaultBoyColorList[0]
                if self.dna.legColor not in ToonDNA.defaultBoyColorList:
                    self.dna.legColor = ToonDNA.defaultBoyColorList[0]
                if self.dna.headColor not in ToonDNA.defaultBoyColorList:
                    self.dna.headColor = ToonDNA.defaultBoyColorList[0]
                # Make sure the topTex, sleeveTex, and botTex are all within
                # valid index range for boys in case we're switching gender
                if (self.toon.style.topTex not in ToonDNA.MakeAToonBoyShirts):
                    randomShirt = ToonDNA.getRandomTop(gender, ToonDNA.MAKE_A_TOON)
                    shirtTex, shirtColor, sleeveTex, sleeveColor = randomShirt                    
                    self.toon.style.topTex = shirtTex
                    self.toon.style.topTexColor = shirtColor
                    self.toon.style.sleeveTex = sleeveTex
                    self.toon.style.sleeveTexColor = sleeveColor
                # Only use the boy shorts used in MakeAToon
                if (self.toon.style.botTex not in ToonDNA.MakeAToonBoyBottoms):
                    # Pick one randomly
                    botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON)
                    self.toon.style.botTex = botTex
                    self.toon.style.botTexColor = botTexColor
                    
            # female (0-5)
            else:
                length = len(ToonDNA.toonTorsoTypes[3:6])
                if (self.toon.style.torso[1] == 'd'):
                    torsoOffset = 3
                else:
                    torsoOffset = 0
                if self.dna.armColor not in ToonDNA.defaultGirlColorList:
                    self.dna.armColor = ToonDNA.defaultGirlColorList[0]
                if self.dna.legColor not in ToonDNA.defaultGirlColorList:
                    self.dna.legColor = ToonDNA.defaultGirlColorList[0]
                if self.dna.headColor not in ToonDNA.defaultGirlColorList:
                    self.dna.headColor = ToonDNA.defaultGirlColorList[0]
                # Make sure the topTex, sleeveTex, and botTex are all within
                # valid index range for girls in case we're switching gender
                if (self.toon.style.topTex not in ToonDNA.MakeAToonGirlShirts):
                    randomShirt = ToonDNA.getRandomTop(gender, ToonDNA.MAKE_A_TOON)
                    shirtTex, shirtColor, sleeveTex, sleeveColor = randomShirt                    
                    self.toon.style.topTex = shirtTex
                    self.toon.style.topTexColor = shirtColor
                    self.toon.style.sleeveTex = sleeveTex
                    self.toon.style.sleeveTexColor = sleeveColor
                # Only use the girl bottoms used in MakeAToon
                if (self.toon.style.botTex not in ToonDNA.MakeAToonGirlBottoms):
                    if (self.toon.style.torso[1] == 'd'):
                        botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON,
                                                                      girlBottomType = ToonDNA.SKIRT)
                        self.toon.style.botTex = botTex
                        self.toon.style.botTexColor = botTexColor
                        torsoOffset = 3
                    else:
                        botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON,
                                                                      girlBottomType = ToonDNA.SHORTS)
                        self.toon.style.botTex = botTex
                        self.toon.style.botTexColor = botTexColor
                        torsoOffset = 0
                
        assert(self.notify.debug('torsoChoice before: %d' % self.torsoChoice))
        self.torsoChoice = (self.torsoChoice + offset) % length
        assert(self.notify.debug('new torsoChoice: %d offset: %d length: %d torsoOffset: %d torsoStart: %d' % (self.torsoChoice, offset, length, torsoOffset, self.torsoStart)))
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.torsoChoice, length, self.torsoStart,
                                   self.torsoLButton, self.torsoRButton)
        torso = ToonDNA.toonTorsoTypes[torsoOffset + self.torsoChoice]
        assert(self.notify.debug('torso start: %d new torso: %s old torso: %s botTex: %d' % (self.torsoStart, torso, self.dna.torso, self.toon.style.botTex)))
        self.dna.torso = torso
        self.toon.swapToonTorso(torso)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)
        
    def __swapLegs(self, offset):
        length = len(ToonDNA.toonLegTypes)
        self.legChoice = (self.legChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.notify.debug("self.legChoice=%d, length=%d, self.legStart=%d" % (self.legChoice, length, self.legStart))
        self.__updateScrollButtons(self.legChoice, length, self.legStart,
                                   self.legLButton, self.legRButton)
        newLeg = ToonDNA.toonLegTypes[self.legChoice]
        self.dna.legs = newLeg
        self.toon.swapToonLegs(newLeg)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)

    def __swapHead(self, offset):
        self.headList = ToonDNA.getHeadList(self.species)
        length = len(self.headList)
        self.headChoice = (self.headChoice + offset) % length
        self.__updateHead()

    def __swapSpecies(self, offset):
        length  = len(ToonDNA.toonSpeciesTypes)
        self.speciesChoice = (self.speciesChoice + offset) % length
        # Ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.speciesChoice, length, self.speciesStart,
                                   self.speciesLButton, self.speciesRButton)
        self.species = ToonDNA.toonSpeciesTypes[self.speciesChoice]
        self.headList = ToonDNA.getHeadList(self.species)
        self.__changeSpeciesName(self.species)
        # Change the head choice to correct it, depending on the species chosen.
        # This is primarily for the mouse, which has only 2 heads.
        # When mouse is selected, if the headChoice index is greater than 1, it changes it to 1.
        maxHeadChoice = len(self.headList) - 1
        if (self.headChoice > maxHeadChoice):
            self.headChoice = maxHeadChoice
        
        self.__updateHead()        
    
    def __updateHead(self):
        self.__updateScrollButtons(self.headChoice, len(self.headList), self.headStart,
                                   self.headLButton, self.headRButton)
        headIndex = ToonDNA.getHeadStartIndex(self.species) + self.headChoice
        newHead = ToonDNA.toonHeadTypes[headIndex]
        self.dna.head = newHead
        self.toon.swapToonHead(newHead)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)
        self.restrictHeadType(newHead)

    def __updateScrollButtons(self, choice, length, start, lButton, rButton):
        # ghost the pickers if at the end of the 'wheel'
        if choice == (start - 1) % length:
            rButton['state'] = DGG.DISABLED
        elif choice != (start - 1) % length:
            rButton['state'] = DGG.NORMAL
        if choice == start % length:
            lButton['state'] = DGG.DISABLED
        elif choice != start % length:
            lButton['state'] = DGG.NORMAL

        #RAU guard code against both buttons getting disabled, unable to reproduce, but
        #screen shot shows it can happen,  bug 15281
        if (lButton['state']==DGG.DISABLED) and (rButton['state']==DGG.DISABLED):
            self.notify.info("Both buttons got disabled! Doing fallback code. choice%d, length=%d, start=%d, lButton=%s, rButton=%s" % (choice, length, start, lButton, rButton))
            if (choice == start % length):
                lButton['state']=DGG.DISABLED
                rButton['state']=DGG.NORMAL
            elif choice == (start-1) % length:
                lButton['state']=DGG.NORMAL
                rButton['state']=DGG.DISABLED
            else:
                lButton['state']=DGG.NORMAL
                rButton['state']=DGG.NORMAL
            
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def restrictHeadType(self, head):
        # restrict free players from choose Monkey, Bear or Horse
        if not base.cr.isPaid():
            if head[0] in ('h', 'p', 'b'):
                # intercept the "next" button event
                self.accept("next", self.__restrictForward)
            else:
                # reset the "next" button event
                self.accept("next", self.__handleForward)
           
    def __restrictForward(self):
        TeaserPanel.TeaserPanel(pageName='species')

    def changeBody(self):
        """
        This method is called when we need to display a new body because player
        pressed the shuffle button.
        """
        newChoice = self.shuffleButton.getCurrChoice()
        newHead = newChoice[0]
        newSpeciesIndex = ToonDNA.toonSpeciesTypes.index(ToonDNA.getSpecies(newHead))
        newHeadIndex = ToonDNA.toonHeadTypes.index(newHead) - ToonDNA.getHeadStartIndex(ToonDNA.getSpecies(newHead))
        newTorsoIndex = ToonDNA.toonTorsoTypes.index(newChoice[1])
        newLegsIndex = ToonDNA.toonLegTypes.index(newChoice[2])
        
        oldHead = self.toon.style.head
        oldSpeciesIndex = ToonDNA.toonSpeciesTypes.index(ToonDNA.getSpecies(oldHead))
        oldHeadIndex = ToonDNA.toonHeadTypes.index(oldHead) - ToonDNA.getHeadStartIndex(ToonDNA.getSpecies(oldHead))
        oldTorsoIndex = ToonDNA.toonTorsoTypes.index(self.toon.style.torso)
        oldLegsIndex = ToonDNA.toonLegTypes.index(self.toon.style.legs)
        
        self.__swapSpecies(newSpeciesIndex - oldSpeciesIndex)
        self.__swapHead(newHeadIndex - oldHeadIndex)
        self.__swapTorso(newTorsoIndex - oldTorsoIndex)
        self.__swapLegs(newLegsIndex - oldLegsIndex)
        
    def getCurrToonSetting(self):
        """
        This method is called by ShuffleButton to get the current setting of the toon.
        The ShuffleButton saves this setting for it's history.
        """
        return [self.toon.style.head, self.toon.style.torso, self.toon.style.legs]

    def __changeSpeciesName(self, species):
        '''
        Change the name of the display text of the Species frame.
        Show the member button only for the paid toons, hide for all others.
        '''
        if (species == 'd'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['dog']
            self.memberButton.hide()
        elif (species == 'c'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['cat']
            self.memberButton.hide()
        elif (species == 'm'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['mouse']
            self.memberButton.hide()
        elif (species == 'h'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['horse']
            self.memberButton.show()
        elif (species == 'r'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['rabbit']
            self.memberButton.hide()
        elif (species == 'f'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['duck']
            self.memberButton.hide()
        elif (species == 'p'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['monkey']
            self.memberButton.show()
        elif (species == 'b'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['bear']
            self.memberButton.show()
        elif (species == 's'):
            self.speciesFrame['text'] = TTLocalizer.AnimalToSpecies['pig']
            self.memberButton.hide()
            
        if base.cr.isPaid():
            self.memberButton.hide()
