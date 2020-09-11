from direct.gui.DirectGui import *
from pandac.PandaModules import *
import Quests
from toontown.toon import NPCToons
from toontown.toon import ToonHead
from toontown.toon import ToonDNA
from toontown.suit import SuitDNA
from toontown.suit import Suit
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import string, types
from toontown.toon import LaffMeter
from toontown.toonbase.ToontownBattleGlobals import AvPropsNew
from toontown.toontowngui.TeaserPanel import TeaserPanel

IMAGE_SCALE_LARGE = 0.2
IMAGE_SCALE_SMALL = 0.15
POSTER_WIDTH = 0.7
TEXT_SCALE = TTLocalizer.QPtextScale
TEXT_WORDWRAP = TTLocalizer.QPtextWordwrap

class QuestPoster(DirectFrame):
    colors = {
        'white' : (1,1,1,1),
        'blue' : (.45,.45,.8,1),
        'lightBlue' : (0.420, 0.671, 1.000, 1.000),
        'green' : (.45,.8,.45,1),
        'lightGreen' : (0.784, 1, 0.863, 1),
        'red' : (.8,.45,.45,1),
        'rewardRed' : (.8, .3, .3, 1),
        'brightRed' : (1.0, 0.16, 0.16, 1.0),
        'brown' : (.52,.42,.22,1),
        }
    normalTextColor = (0.3,0.25,0.2,1)

    def __init__(self, parent = aspect2d, **kw):
        # NOTE: Quest card has about +/- 0.35 units of usable space (0.7 units total)
        # Need to calc width of quest info string width = font.calcWidth(string)
        # text scale is equal to 0.7/width
        # wordwrap should be set to width + pad (0.05)
        # For text at scale 0.045, max width = 15.55, set wordwrap to 15.5
        # Load gui images
        bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
        questCard = bookModel.find("**/questCard")
        # Define options
        optiondefs = (
            ('relief',        None,             None),
            ('reverse',       0,                None),
            ('image',         questCard,        None),
            ('image_scale',   (0.8,1.0,0.58),   None),
            # So we get enter and exit events
            ('state',         DGG.NORMAL,           None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclass
        DirectFrame.__init__(self, relief = None)
        # Initialize instance
        self.initialiseoptions(QuestPoster)

        # Single frame to hold everything on the quest poster
        self.questFrame = DirectFrame(parent = self, relief = None)

        # Main headline
        self.headline = DirectLabel(
            parent = self.questFrame,
            relief = None,
            text = '',
            text_font = ToontownGlobals.getMinnieFont(),
            text_fg = self.normalTextColor,
            text_scale = 0.05,
            text_align = TextNode.ACenter,
            text_wordwrap = 12.0,
            textMayChange = 1,
            # 0.165
            pos = (0,0,0.23),
            )

        # Detail information about the quest
        self.questInfo = DirectLabel(
            parent = self.questFrame,
            relief = None,
            text = '', 
            text_fg = self.normalTextColor,
            text_scale = TEXT_SCALE,
            text_align = TextNode.ACenter,
            text_wordwrap = TEXT_WORDWRAP,
            textMayChange = 1,
            pos = (0, 0, -0.0625)
            )

        # Detail information about the quest
        self.rewardText = DirectLabel(
            parent = self.questFrame,
            relief = None,
            text = '', 
            text_fg = self.colors['rewardRed'],
            text_scale = 0.0425,
            text_align = TextNode.ALeft,
            text_wordwrap = 17.0,
            textMayChange = 1,
            pos = (-0.36,0,-0.26),
            )
        self.rewardText.hide()

        # there are at most two pictureFrames on a quest poster
        # create them both up-front
        self.lPictureFrame = DirectFrame(
            parent = self.questFrame,
            relief = None,
            image = bookModel.find("**/questPictureFrame"),
            image_scale = IMAGE_SCALE_SMALL,
            text = '', 
            text_pos = (0,-0.11),
            text_fg = self.normalTextColor,
            text_scale = TEXT_SCALE,
            text_align = TextNode.ACenter,
            text_wordwrap = 11.0, # was 8
            textMayChange = 1,
            )
        self.lPictureFrame.hide()
        self.rPictureFrame = DirectFrame(
            parent = self.questFrame,
            relief = None,
            image = bookModel.find("**/questPictureFrame"),
            image_scale = IMAGE_SCALE_SMALL,
            text = '',             
            text_pos = (0,-0.11),
            text_fg = self.normalTextColor,
            text_scale = TEXT_SCALE,
            text_align = TextNode.ACenter,
            text_wordwrap = 11.0, # was 8
            textMayChange = 1,
            pos = (0.18,0, 0.13),
            )
        self.rPictureFrame.hide()

        # DirectFrames to hold pictures/models of quest items
        self.lQuestIcon = DirectFrame(
            parent = self.lPictureFrame,
            relief = None,
            text = ' ', 
            text_font = ToontownGlobals.getSuitFont(),
            text_pos = (0,-0.03),
            text_fg = self.normalTextColor,
            text_scale = 0.13,
            text_align = TextNode.ACenter,
            text_wordwrap = 13.0,
            textMayChange = 1,
            )
        # Make sure icon doesn't inherit parent's color
        self.lQuestIcon.setColorOff(-1)
        self.rQuestIcon = DirectFrame(
            parent = self.rPictureFrame,
            relief = None,
            text = ' ', 
            text_font = ToontownGlobals.getSuitFont(),
            text_pos = (0,-0.03),
            text_fg = self.normalTextColor,
            text_scale = 0.13,
            text_align = TextNode.ACenter,
            text_wordwrap = 13.0,
            textMayChange = 1,
            )
        # Make sure icon doesn't inherit parent's color
        self.rQuestIcon.setColorOff(-1)

        # Helper word
        self.auxText = DirectLabel(
            parent = self.questFrame,
            relief = None,
            text = '',
            text_scale = TTLocalizer.QPauxText,
            text_fg = self.normalTextColor,
            text_align = TextNode.ACenter,
            textMayChange = 1,
            )
        self.auxText.hide()

        # Progress bar for multi-item quests
        self.questProgress = DirectWaitBar(
            parent = self.questFrame,
            relief = DGG.SUNKEN,
            frameSize = (-0.95,0.95,-0.1,0.12),
            borderWidth = (0.025,0.025),
            scale = 0.2,
            frameColor = (0.945, 0.875, 0.706, 1.000),
            barColor = (0.5,0.7,0.5,1),
            text = "0/0",
            text_scale = 0.19,
            text_fg = (0.05, 0.14, 0.4, 1),
            text_align = TextNode.ACenter,
            text_pos = (0,-0.04),
            pos = (0,0,-0.195),
            )
        self.questProgress.hide()

        # Optional quest indicator
        self.funQuest = DirectLabel(
            parent = self.questFrame,
            relief = None,
            text = TTLocalizer.QuestPosterFun,
            text_fg = (0.000, 0.439, 1.000, 1.000),
            text_shadow = (0,0,0,1),
            #pos = (-0.28, 0, 0.19),
            pos = (-0.2825, 0, 0.20),            
            scale = 0.03
            )
        self.funQuest.setR(-30)
        self.funQuest.hide()

        # Free up model
        bookModel.removeNode()

        # reverse the poster graphic if necessary
        self.reverseBG(self['reverse'])

        # For use by newbie quests
        self.laffMeter = None

    def destroy(self):
        # make sure any toon heads get cleaned up
        for icon in (self.lQuestIcon, self.rQuestIcon):
            geom = icon['geom']
            if geom:
                # I know, ugly...
                if hasattr(geom, 'delete'):
                    geom.delete()

        DirectFrame.destroy(self)

    def reverseBG(self, reverse=0):
        # reverse the poster image (for right-hand page in shticker
        # book, for example)
        try:
            self.initImageScale
        except AttributeError:
            self.initImageScale = self['image_scale']
            if reverse:
                self.initImageScale.setX(-abs(self.initImageScale[0]))
                self.questFrame.setX(0.015)
            else:
                self.initImageScale.setX(abs(self.initImageScale[0]))
            self['image_scale'] = self.initImageScale

    def mouseEnterPoster(self, event):
        # Make sure you're on the top
        self.reparentTo(self.getParent())
        # Make the scroll longer
        sc = Vec3(self.initImageScale)
        sc.setZ(sc[2] + 0.07)
        self['image_scale'] = sc
        # Adjust contents
        self.questFrame.setZ(0.03)
        self.rewardText.show()

    def mouseExitPoster(self, event):
        self['image_scale'] = self.initImageScale
        self.questFrame.setZ(0)
        self.rewardText.hide()

    def createNpcToonHead(self, toNpcId):
        # Given an NPC id create a toon head suitable for framing
        npcInfo = NPCToons.NPCToonDict[toNpcId]
        dnaList = npcInfo[2]
        gender = npcInfo[3]
        if dnaList == 'r':
            dnaList = NPCToons.getRandomDNA(toNpcId, gender)
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties(*dnaList)
        head = ToonHead.ToonHead()
        head.setupHead(dna, forGui = 1)
        # Insert xform with gets head to uniform size
        self.fitGeometry(head, fFlip = 1)
        return head

    def createLaffMeter(self, hp):
        lm = LaffMeter.LaffMeter(base.localAvatar.style, hp, hp)
        lm.adjustText()
        return lm 

    def createSuitHead(self, suitName):
        # Given an suit name create a toon head suitable for framing
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit(suitName)
        suit = Suit.Suit()
        suit.setDNA(suitDNA)
        headParts = suit.getHeadParts()
        head = hidden.attachNewNode('head')
        for part in headParts:
            copyPart = part.copyTo(head)
            # turn on depth write and test.
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)
        # Insert xform with gets head to uniform size
        self.fitGeometry(head, fFlip = 1)
        suit.delete()
        suit = None
        return head

    def loadElevator(self, building, numFloors):
        # Load up an elevator and parent it the given building
        elevatorNodePath = hidden.attachNewNode("elevatorNodePath")
        elevatorModel = loader.loadModel("phase_4/models/modules/elevator")
        # Put up a display to show the current floor of the elevator
        floorIndicator=[None, None, None, None, None]
        npc=elevatorModel.findAllMatches("**/floor_light_?;+s")
        for i in range(npc.getNumPaths()):
            np=npc.getPath(i)
            # Get the last character, and make it zero based:
            floor=int(np.getName()[-1:])-1
            floorIndicator[floor]=np
            if floor < numFloors:
                np.setColor(Vec4(0.5, 0.5, 0.5, 1.0))
            else:
                np.hide()
        elevatorModel.reparentTo(elevatorNodePath)
        # Find the door origin
        suitDoorOrigin = building.find("**/*_door_origin")
        assert(not suitDoorOrigin.isEmpty())
        # Put the elevator under the door origin
        elevatorNodePath.reparentTo(suitDoorOrigin)
        elevatorNodePath.setPosHpr(0, 0, 0, 0, 0, 0)

    def fitGeometry(self, geom, fFlip = 0, dimension = 0.8):
        # Insert an xform which centers geometry on origin and scales it
        # to +/-0.8 in size
        p1 = Point3()
        p2 = Point3()
        geom.calcTightBounds(p1, p2)
        if fFlip:
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = dimension/biggest
        # find midpoint
        mid = (p1 + d/2.0) * s
        geomXform = hidden.attachNewNode('geomXform')
        for child in geom.getChildren():
            child.reparentTo(geomXform)
        geomXform.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2],
                                 180, 0, 0,
                                 s, s, s)
        geomXform.reparentTo(geom)
    
    def clear(self):
        self['image_color'] = Vec4(*self.colors['white'])
        # clear out the poster text
        self.headline['text'] = ""
        self.headline['text_fg'] = self.normalTextColor
        self.questInfo['text'] = ""
        self.questInfo['text_fg'] = self.normalTextColor
        self.rewardText['text'] = ""
        self.auxText['text'] = ""
        self.auxText['text_fg'] = self.normalTextColor
        self.funQuest.hide()
        # Hide picture frames
        self.lPictureFrame.hide()
        self.rPictureFrame.hide()
        # Hide progress bar
        self.questProgress.hide()
        # Delete choose button if one exists
        if hasattr(self, 'chooseButton'):
            self.chooseButton.destroy()
            del self.chooseButton
        if (self.laffMeter != None):
            self.laffMeter.reparentTo(hidden)
            self.laffMeter.destroy()
            self.laffMeter = None

    def showChoicePoster(self, questId, fromNpcId, toNpcId, rewardId,
                         callback):
        # Create a quest poster and add a button used to choose that quest
        self.update((questId, fromNpcId, toNpcId, rewardId, 0))
        quest = Quests.getQuest(questId)
        # Move reward text up and show it on the choice poster
        self.rewardText.show()
        self.rewardText.setZ(-0.205)
        # And hide progress bar
        self.questProgress.hide()
        # Add a choose button
        if not hasattr(self, 'chooseButton'):
            # Add a choose button to select this quest
            guiButton = loader.loadModel("phase_3/models/gui/quit_button")
            self.chooseButton = DirectButton(
                parent = self.questFrame,
                relief = None,
                image = (guiButton.find("**/QuitBtn_UP"),
                         guiButton.find("**/QuitBtn_DN"),
                         guiButton.find("**/QuitBtn_RLVR"),
                         ),
                image_scale = (0.7,1,1),
                text = TTLocalizer.QuestPageChoose,
                text_scale = 0.06,
                text_pos = (0,-0.02),
                pos = (0.285,0,0.245),
                scale = 0.65,
                )
            guiButton.removeNode()

        npcZone = NPCToons.getNPCZone(toNpcId)
        hoodId = ZoneUtil.getCanonicalHoodId(npcZone)

        # Don't allow trialers to get DD quests
        if not base.cr.isPaid() and (((hasattr(quest, 'getLocation')) and (quest.getLocation() == 1000)) or (hoodId == 1000)):
            def showTeaserPanel():
                TeaserPanel(pageName='quests')
            self.chooseButton['command'] = showTeaserPanel
        # trailers can't get new gag tracks
        elif not base.cr.isPaid() and ((questId >= 900) and questId <= 907):
            def showTeaserPanel():
                TeaserPanel(pageName='quests')
            self.chooseButton['command'] = showTeaserPanel
        else:
            self.chooseButton['command'] = callback
            self.chooseButton['extraArgs'] = [questId]


        # For choice posters we con't want popup behavior
        self.unbind(DGG.WITHIN)
        self.unbind(DGG.WITHOUT)

        # if we have moved the reward up, we should move the quest info up too
        # (unless this is track choice)
        if not (quest.getType() == Quests.TrackChoiceQuest):        
            self.questInfo.setZ(-0.0625)
        
    def update(self, questDesc):
        # Update quest poster to reflect details about given quest
        # Extract details about the quest
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        quest = Quests.getQuest(questId)
        if quest == None:
            print "Tried to display poster for unknown quest %s" % (questId)
            return
        # Update reward info
        if rewardId == Quests.NA:
            finalReward = Quests.getFinalRewardId(questId, fAll = 1)
            transformedReward = Quests.transformReward(finalReward, base.localAvatar)
            reward = Quests.getReward(transformedReward)
        else:
            reward = Quests.getReward(rewardId)
        #if reward:
        # HACK: don't show the tutorial quest reward...
        if reward and not (questId in Quests.NoRewardTierZeroQuests):
            rewardString = reward.getPosterString()
        else:
            rewardString = ""
        self.rewardText['text'] = rewardString
        self.fitLabel(self.rewardText)
        # Is reward optional
        questEntry = Quests.QuestDict.get(questId)
        if questEntry:
            tier = questEntry[0]
            fOptional = Quests.isRewardOptional(tier, rewardId)
        else:
            fOptional = 0
        if fOptional:
            self.funQuest.show()
        else:
            self.funQuest.hide()
        # Is quest complete?
        fComplete = (quest.getCompletionStatus(base.localAvatar, questDesc) == Quests.COMPLETE)
        # Names and IDs
        fromNpcName = NPCToons.getNPCName(fromNpcId)
        npcZone = NPCToons.getNPCZone(fromNpcId)
        hoodId = ZoneUtil.getCanonicalHoodId(npcZone)
        branchId = ZoneUtil.getCanonicalBranchZone(npcZone)
        # Is this in the Toon HQ or in the hoods
        if fromNpcId == Quests.ToonHQ:
            locationName = TTLocalizer.QuestPosterHQLocationName
            buildingName = TTLocalizer.QuestPosterHQBuildingName
            streetName = TTLocalizer.QuestPosterHQStreetName
        elif fromNpcId == Quests.ToonTailor:
            locationName = TTLocalizer.QuestPosterTailorLocationName
            buildingName = TTLocalizer.QuestPosterTailorBuildingName
            streetName = TTLocalizer.QuestPosterTailorStreetName
        else:
            locationName = base.cr.hoodMgr.getFullnameFromId(hoodId)
            buildingName = NPCToons.getBuildingTitle(npcZone)
            streetName = ZoneUtil.getStreetName(branchId)

        if toNpcId == Quests.ToonHQ:
            toNpcName = TTLocalizer.QuestPosterHQOfficer
            toNpcBuildingName = TTLocalizer.QuestPosterHQBuildingName
            toNpcStreetName = TTLocalizer.QuestPosterHQStreetName
            toNpcLocationName = TTLocalizer.QuestPosterHQLocationName
        elif toNpcId == Quests.ToonTailor:
            toNpcName = TTLocalizer.QuestPosterTailor
            toNpcBuildingName = TTLocalizer.QuestPosterTailorBuildingName
            toNpcStreetName = TTLocalizer.QuestPosterTailorStreetName
            toNpcLocationName = TTLocalizer.QuestPosterTailorLocationName
        else:
            toNpcName = NPCToons.getNPCName(toNpcId)
            toNpcZone = NPCToons.getNPCZone(toNpcId)
            toNpcHoodId = ZoneUtil.getCanonicalHoodId(toNpcZone)
            toNpcLocationName = base.cr.hoodMgr.getFullnameFromId(
                toNpcHoodId)
            toNpcBuildingName = NPCToons.getBuildingTitle(toNpcZone)
            toNpcBranchId = ZoneUtil.getBranchZone(toNpcZone)
            toNpcStreetName = ZoneUtil.getStreetName(toNpcBranchId)
        # Set initial state
        lPos = Vec3(0,0,0.13)
        lIconGeom = None
        lIconGeomScale = 1
        rIconGeom = None
        rIconGeomScale = 1
        infoText = ""
        infoZ = TTLocalizer.QPinfoZ
        auxText = None
        auxTextPos = Vec3(0,0,0.12)
        headlineString = quest.getHeadlineString()
        objectiveStrings = quest.getObjectiveStrings()
        assert type(objectiveStrings) in (types.ListType, types.TupleType)
        captions = map(string.capwords,quest.getObjectiveStrings())
        imageColor = Vec4(*self.colors['white'])        
        # Adjust poster for the particular quest type
        if ((quest.getType() == Quests.DeliverGagQuest) or
            (quest.getType() == Quests.DeliverItemQuest)):
            frameBgColor = 'red'
            # Create item icon
            if quest.getType() == Quests.DeliverGagQuest:
                # Load inventory models
                invModel = loader.loadModel(
                    "phase_3.5/models/gui/inventory_icons")
                track,item = quest.getGagType()
                lIconGeom = invModel.find("**/" + AvPropsNew[track][item])
                invModel.removeNode()
            else:
                bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                lIconGeom = bookModel.find("**/package")
                lIconGeomScale = 0.12
                bookModel.removeNode()
            if not fComplete:
                # Need to know who this is going to
                captions.append(toNpcName)
                # Adjust poster items
                auxText = TTLocalizer.QuestPosterAuxTo
                auxTextPos.setZ(0.12)
                lPos.setX(-0.18)
                infoText = (TTLocalizer.QuestPageDestination %
                            (toNpcBuildingName,
                             toNpcStreetName,
                             toNpcLocationName))
                # Create a toon head
                rIconGeom = self.createNpcToonHead(toNpcId)
                rIconGeomScale = IMAGE_SCALE_SMALL
        elif (quest.getType() == Quests.RecoverItemQuest):
            frameBgColor = 'green'
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/package")
            lIconGeomScale = 0.12
            bookModel.removeNode()
            if not fComplete:
                # Adjust poster items
                # Same as pictureFrame image_scale
                rIconGeomScale = IMAGE_SCALE_SMALL
                # Create icom for holder
                holder = quest.getHolder()
                holderType = quest.getHolderType()
                if holder == Quests.Any:
                    # Any Cog
                    cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                    rIconGeom = cogIcons.find('**/cog')
                    cogIcons.removeNode()
                    lPos.setX(-0.18)
                    auxText = TTLocalizer.QuestPosterAuxFrom
                elif holder == Quests.AnyFish:
                    headlineString = TTLocalizer.QuestPosterFishing
                    auxText = TTLocalizer.QuestPosterAuxFor
                    auxTextPos.setX(-0.18)
                    captions = captions[:1]
                else:
                    if (holderType == 'track'):
                        # Load up appropriate cog icon
                        cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                        if (holder == 'c'):
                            icon = cogIcons.find('**/CorpIcon')
                        elif (holder == 's'):
                            icon = cogIcons.find('**/SalesIcon')
                        elif (holder == 'l'):
                            icon = cogIcons.find('**/LegalIcon')
                        elif (holder == 'm'):
                            icon = cogIcons.find('**/MoneyIcon')
                        rIconGeom = icon.copyTo(hidden)
                        rIconGeom.setColor(
                            Suit.Suit.medallionColors[holder])
                        rIconGeomScale = 0.12
                        cogIcons.removeNode()
                    elif (holderType == 'level'):
                        # Use a generic cog icon
                        cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                        rIconGeom = cogIcons.find('**/cog')
                        rIconGeomScale = IMAGE_SCALE_SMALL
                        cogIcons.removeNode()
                    else:
                        rIconGeom = self.createSuitHead(holder)
                    lPos.setX(-0.18)
                    auxText = TTLocalizer.QuestPosterAuxFrom                    
                # Display location conditions for quest
                infoText = string.capwords(quest.getLocationName())
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.VisitQuest):
            frameBgColor = 'brown'
            # Who do you visit?
            captions[0] = "%s" % toNpcName
            # Create an appropriate toon head
            lIconGeom = self.createNpcToonHead(toNpcId)
            lIconGeomScale = IMAGE_SCALE_SMALL
            if not fComplete:
                # Adjust poster items
                # Show location of toNpc
                infoText = (TTLocalizer.QuestPageDestination %
                            (toNpcBuildingName,
                             toNpcStreetName,
                             toNpcLocationName))
        elif (quest.getType() == Quests.TrackChoiceQuest):
            frameBgColor = 'green'
            # Get a representative icon for each track
            invModel = loader.loadModel("phase_3.5/models/gui/inventory_icons")
            track1,track2 = quest.getChoices()
            lIconGeom = invModel.find("**/" + AvPropsNew[track1][1])
            if not fComplete:
                # Adjust poster items
                auxText = TTLocalizer.QuestPosterAuxOr
                lPos.setX(-0.18)
                rIconGeom = invModel.find("**/" + AvPropsNew[track2][1])
                infoText = (TTLocalizer.QuestPageNameAndDestination %
                            (toNpcName,
                             toNpcBuildingName,
                             toNpcStreetName,
                             toNpcLocationName))
                infoZ = -0.02
            invModel.removeNode()
        elif (quest.getType() == Quests.BuildingQuest):
            frameBgColor = 'blue'
            # Determine track and number of floors
            track = quest.getBuildingTrack()
            numFloors = quest.getNumFloors()
            # Get the appropriate icon
            # Use loadModelCopy since fitGeometry munges hierarchy
            if track == 'c':
                lIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_corp')
            elif track == 'l':
                lIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_legal')
            elif track == 'm':
                lIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_money')
            elif track == 's':
                lIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_sales')
            else:
                # Use a generic building icon
                bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                lIconGeom = bookModel.find("**/COG_building")
                bookModel.removeNode()
            # Add in an elevator to fill up the hole
            if lIconGeom and (track != Quests.Any):
                self.loadElevator(lIconGeom, numFloors)
                lIconGeom.setH(180)
                # Make sure it all fits
                self.fitGeometry(lIconGeom, fFlip = 0)
                lIconGeomScale = IMAGE_SCALE_SMALL
            else:
                lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.BuildingNewbieQuest):
            frameBgColor = 'blue'
            # Determine track and number of floors
            track = quest.getBuildingTrack()
            numFloors = quest.getNumFloors()
            # Get the appropriate icon
            # Use loadModelCopy since fitGeometry munges hierarchy
            if track == 'c':
                rIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_corp')
            elif track == 'l':
                rIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_legal')
            elif track == 'm':
                rIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_money')
            elif track == 's':
                rIconGeom = loader.loadModel('phase_4/models/modules/suit_landmark_sales')
            else:
                # Use a generic building icon
                bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                rIconGeom = bookModel.find("**/COG_building")
                bookModel.removeNode()
            # Add in an elevator to fill up the hole
            if rIconGeom and (track != Quests.Any):
                self.loadElevator(rIconGeom, numFloors)
                rIconGeom.setH(180)
                # Make sure it all fits
                self.fitGeometry(rIconGeom, fFlip = 0)
                rIconGeomScale = IMAGE_SCALE_SMALL
            else:
                rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.FactoryQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/factoryIcon2")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.FactoryNewbieQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/factoryIcon2")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.MintQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/CashBotMint")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.MintNewbieQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/CashBotMint")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.CogPartQuest):
            frameBgColor = 'green'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/CogArmIcon2")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.CogPartNewbieQuest):
            frameBgColor = 'green'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/CogArmIcon2")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogPartQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif ((quest.getType() == Quests.ForemanQuest) or
              (quest.getType() == Quests.SupervisorQuest)):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/skelecog5")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif ((quest.getType() == Quests.ForemanNewbieQuest) or
              (quest.getType() == Quests.SupervisorNewbieQuest)):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/skelecog5")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.VPQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/BossHead3Icon")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.VPNewbieQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/BossHead3Icon")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.CFOQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/CashBotBossHeadIcon")
            bookModel.removeNode()
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.CFONewbieQuest):
            frameBgColor = 'blue'
            # Get the appropriate icon
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = bookModel.find("**/CashBotBossHeadIcon")
            bookModel.removeNode()
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsCogNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.RescueQuest):
            frameBgColor = 'blue'
            # Use any toon head
            lIconGeom = self.createNpcToonHead(2001)
            lIconGeomScale = 0.13
            if not fComplete:
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.RescueNewbieQuest):
            frameBgColor = 'blue'
            # Use any toon head
            rIconGeom = self.createNpcToonHead(2001)
            rIconGeomScale = 0.13
            if not fComplete:
                headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                captions = [quest.getCaption()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsRescueQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
                # Where is (are) the building(s)
                infoText = quest.getLocationName()
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        elif (quest.getType() == Quests.FriendQuest):
            frameBgColor = 'brown'
            # Show them the friends button icon
            gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
            lIconGeom = gui.find('**/FriendsBox_Closed')
            lIconGeomScale = 0.45
            gui.removeNode()
            infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.FriendNewbieQuest):
            frameBgColor = 'brown'
            # Show them the friends button icon
            gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
            lIconGeom = gui.find('**/FriendsBox_Closed')
            lIconGeomScale = 0.45
            gui.removeNode()
            infoText = TTLocalizer.QuestPosterAnywhere
        elif (quest.getType() == Quests.TrolleyQuest):
            frameBgColor = 'lightBlue'
            # Show them the trolley
            gui = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = gui.find('**/trolley')
            lIconGeomScale = 0.13
            gui.removeNode()
            infoText = TTLocalizer.QuestPosterPlayground
        elif (quest.getType() == Quests.MailboxQuest):
            frameBgColor = 'lightBlue'
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/package")
            lIconGeomScale = 0.12
            bookModel.removeNode()
            infoText = TTLocalizer.QuestPosterAtHome
        elif (quest.getType() == Quests.PhoneQuest):
            frameBgColor = 'lightBlue'
            bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            lIconGeom = bookModel.find("**/clarabelleCow")
            lIconGeomScale = 0.12
            bookModel.removeNode()
            infoText = TTLocalizer.QuestPosterOnPhone
        elif (quest.getType() == Quests.MinigameNewbieQuest):
            frameBgColor = 'lightBlue'
            # Show them the trolley
            gui = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
            rIconGeom = gui.find('**/trolley')
            rIconGeomScale = 0.13
            gui.removeNode()
            infoText = TTLocalizer.QuestPosterPlayground
            if not fComplete:
                captions = [TTLocalizer.QuestsMinigameNewbieQuestCaption % quest.getNewbieLevel()]
                captions.append(map(string.capwords, quest.getObjectiveStrings()))
                auxText = TTLocalizer.QuestsMinigameNewbieQuestAux
                lPos.setX(-0.18)
                self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                self.laffMeter.setScale(0.04)
                lIconGeom = None
            else:
                lIconGeom = rIconGeom
                rIconGeom = None
                lIconGeomScale = rIconGeomScale
                rIconGeomScale = 1
        else:
            # The Cog Quests (or Skelecog!)
            frameBgColor = 'blue'
            # cog quests
            if (quest.getType() == Quests.CogTrackQuest):
                # Load up appropriate cog icon
                dept = quest.getCogTrack()
                cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                lIconGeomScale = 0.13
                if dept == 'c':
                    icon = cogIcons.find('**/CorpIcon')
                elif dept == 's':
                    icon = cogIcons.find('**/SalesIcon')
                elif dept == 'l':
                    icon = cogIcons.find('**/LegalIcon')
                elif dept == 'm':
                    icon = cogIcons.find('**/MoneyIcon')
                lIconGeom = icon.copyTo(hidden)
                lIconGeom.setColor(Suit.Suit.medallionColors[dept])
                cogIcons.removeNode()
            elif (quest.getType() == Quests.CogQuest):
                # Show a suit head, or generic cog icon
                if quest.getCogType() != Quests.Any:
                    # Create a suit head
                    lIconGeom = self.createSuitHead(quest.getCogType())
                    # Same as pictureFrame image_scale
                    lIconGeomScale = IMAGE_SCALE_SMALL
                else:
                    cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                    lIconGeom = cogIcons.find('**/cog')
                    lIconGeomScale = IMAGE_SCALE_SMALL
                    cogIcons.removeNode()
            elif (quest.getType() == Quests.CogLevelQuest):
                # Use a generic cog icon
                cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                lIconGeom = cogIcons.find('**/cog')
                lIconGeomScale = IMAGE_SCALE_SMALL
                cogIcons.removeNode()
            elif (quest.getType() == Quests.CogNewbieQuest):
                # Show a suit head, or generic cog icon
                if quest.getCogType() != Quests.Any:
                    # Create a suit head
                    rIconGeom = self.createSuitHead(quest.getCogType())
                    # Same as pictureFrame image_scale
                    rIconGeomScale = IMAGE_SCALE_SMALL
                else:
                    cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                    rIconGeom = cogIcons.find('**/cog')
                    rIconGeomScale = IMAGE_SCALE_SMALL
                    cogIcons.removeNode()
                if not fComplete:
                    headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                    captions = [quest.getCaption()]
                    captions.append(map(string.capwords, quest.getObjectiveStrings()))
                    auxText = TTLocalizer.QuestsCogNewbieQuestAux
                    lPos.setX(-0.18)
                    self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                    self.laffMeter.setScale(0.04)
                    lIconGeom = None
                else:
                    lIconGeom = rIconGeom
                    rIconGeom = None
                    lIconGeomScale = rIconGeomScale
                    rIconGeomScale = 1
            # skelecog quests
            elif (quest.getType() == Quests.SkelecogTrackQuest):
                # Load up appropriate cog icon
                dept = quest.getCogTrack()
                cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                lIconGeomScale = 0.13
                if dept == 'c':
                    icon = cogIcons.find('**/CorpIcon')
                elif dept == 's':
                    icon = cogIcons.find('**/SalesIcon')
                elif dept == 'l':
                    icon = cogIcons.find('**/LegalIcon')
                elif dept == 'm':
                    icon = cogIcons.find('**/MoneyIcon')
                lIconGeom = icon.copyTo(hidden)
                lIconGeom.setColor(Suit.Suit.medallionColors[dept])
                cogIcons.removeNode()
            elif (quest.getType() == Quests.SkelecogQuest):
                # Show a skelecog head
                cogIcons = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
                lIconGeom = cogIcons.find('**/skelecog5')
                lIconGeomScale = IMAGE_SCALE_SMALL
                cogIcons.removeNode()
            elif (quest.getType() == Quests.SkelecogLevelQuest):
                # Show a skelecog head
                cogIcons = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
                lIconGeom = cogIcons.find('**/skelecog5')
                lIconGeomScale = IMAGE_SCALE_SMALL
                cogIcons.removeNode()
            elif (quest.getType() == Quests.SkelecogNewbieQuest):
                # Show a skelecog head
                cogIcons = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                rIconGeom = cogIcons.find("**/skelecog5")
                rIconGeomScale = IMAGE_SCALE_SMALL
                cogIcons.removeNode()
                if not fComplete:
                    headlineString = TTLocalizer.QuestsNewbieQuestHeadline
                    captions = [quest.getCaption()]
                    captions.append(map(string.capwords, quest.getObjectiveStrings()))
                    auxText = TTLocalizer.QuestsCogNewbieQuestAux
                    lPos.setX(-0.18)
                    self.laffMeter = self.createLaffMeter(quest.getNewbieLevel())
                    self.laffMeter.setScale(0.04)
                    lIconGeom = None
                else:
                    lIconGeom = rIconGeom
                    rIconGeom = None
                    lIconGeomScale = rIconGeomScale
                    rIconGeomScale = 1
            elif (quest.getType() == Quests.SkeleReviveQuest):
                # Show a skelecog head
                cogIcons = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
                lIconGeom = cogIcons.find('**/skelecog5')
                lIconGeomScale = IMAGE_SCALE_SMALL
                cogIcons.removeNode()
                    
            if not fComplete:
                # Show the location of the cog/item
                infoText = string.capwords(quest.getLocationName())
                if infoText == '':
                    infoText = TTLocalizer.QuestPosterAnywhere
                
        if fComplete:
            # Make text and background green to show it is complete
            textColor = (0,0.3,0,1)
            imageColor = Vec4(*self.colors['lightGreen'])
            lPos.setX(-0.18)
            # Create a toon head
            rIconGeom = self.createNpcToonHead(toNpcId)
            rIconGeomScale = IMAGE_SCALE_SMALL
            # Only show on picture frame
            captions = captions[:1]
            captions.append(toNpcName)
            auxText = TTLocalizer.QuestPosterAuxReturnTo
            headlineString = TTLocalizer.QuestPosterComplete
            infoText = (TTLocalizer.QuestPageDestination %
                        (toNpcBuildingName, toNpcStreetName,
                         toNpcLocationName))
            if (self.laffMeter != None):
                self.laffMeter.reparentTo(hidden)
                self.laffMeter.destroy()
                self.laffMeter = None
        else:
            textColor = self.normalTextColor            
        # Show thyself
        self.show()
        # Update color
        self['image_color'] = imageColor
        # Update the headline string and text color
        self.headline['text_fg'] = textColor
        self.headline['text'] = headlineString
        # Update picture frame captions and locations
        self.lPictureFrame.show()
        self.lPictureFrame.setPos(lPos)
        self.lPictureFrame['text_scale'] = TEXT_SCALE        
        # scale down the text if left picture is not centered
        if (lPos[0] != 0):
            self.lPictureFrame['text_scale'] = 0.0325
        self.lPictureFrame['text'] = captions[0]
        #self.lPictureFrame.setColor(*self.colors[frameBgColor])
        self.lPictureFrame['image_color'] = Vec4(*self.colors[frameBgColor])
        if len(captions) > 1:
            self.rPictureFrame.show()
            self.rPictureFrame['text'] = captions[1]
            self.rPictureFrame['text_scale'] = 0.0325             
            #self.rPictureFrame.setColor(*self.colors[frameBgColor])
            self.rPictureFrame['image_color'] =Vec4(*self.colors[frameBgColor])
        else:
            self.rPictureFrame.hide()
        # Update quest icons
        self.lQuestIcon['geom'] = lIconGeom
        self.lQuestIcon['geom_pos'] = (0,10,0)
        if lIconGeom:
            self.lQuestIcon['geom_scale'] = lIconGeomScale
        if (self.laffMeter != None):
            self.laffMeter.reparentTo(self.lQuestIcon)
        self.rQuestIcon['geom'] = rIconGeom
        self.rQuestIcon['geom_pos'] = (0,10,0)
        if rIconGeom:
            self.rQuestIcon['geom_scale'] = rIconGeomScale
            
        # Display auxiliary text if necessary
        if auxText:
            self.auxText.show()
            self.auxText['text'] = auxText
            self.auxText.setPos(auxTextPos)
        else:
            self.auxText.hide()
        # Display quest progress (if any)
        self.bind(DGG.WITHIN, self.mouseEnterPoster)
        self.bind(DGG.WITHOUT, self.mouseExitPoster)
        numQuestItems = quest.getNumQuestItems()
        if fComplete or (numQuestItems <= 1):
            self.questProgress.hide()
            # if bar is not shown (and not complete track choice) make more room for other text
            if not (quest.getType() == Quests.TrackChoiceQuest):
                infoZ = -0.075
        else:
            self.questProgress.show()
            self.questProgress['value'] = toonProgress  & (pow(2,16) - 1)
            self.questProgress['range'] = numQuestItems
            self.questProgress['text'] = quest.getProgressString(base.localAvatar, questDesc)

        # Display quest Info (if any), adjust wordwrap if necessary
        self.questInfo['text'] = infoText
        self.questInfo.setZ(infoZ)
        self.fitLabel(self.questInfo)

    def fitLabel(self, label, lineNo = 0):
        text = label['text']
        label['text_scale'] = TEXT_SCALE
        label['text_wordwrap'] = TEXT_WORDWRAP
        if len(text) > 0:
            lines = text.split('\n')

            # We pass in the string to textNode.calcWidth, instead of
            # using textNode.getWidth(), because we don't want to
            # consider the wordwrapping in this calculation.
            lineWidth = label.component('text0').textNode.calcWidth(lines[lineNo])
            # Do not divide by zero on an empty line
            if lineWidth > 0:
                textScale = POSTER_WIDTH/lineWidth
                label['text_scale'] = min(TEXT_SCALE, textScale)
                label['text_wordwrap'] = max(TEXT_WORDWRAP, lineWidth + 0.05)
