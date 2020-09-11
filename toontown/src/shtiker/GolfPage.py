##########################################################################
# Module: GolfPage.py
##########################################################################

##########################################################################
# Panda Import Modules
##########################################################################
#from direct.directbase import DirectStart
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import PythonUtil
from direct.task import Task

##########################################################################
# Toontown Import Modules
##########################################################################
from toontown.fishing.FishPhoto import DirectRegion
from toontown.shtiker.ShtikerPage import ShtikerPage
from toontown.toonbase import ToontownGlobals, TTLocalizer
from FishPage import FishingTrophy
from toontown.golf import GolfGlobals

##########################################################################
# Python Import Modules
##########################################################################
if( __debug__ ):
    import pdb

##########################################################################
# Global Variables and Enumerations 
##########################################################################
PageMode = PythonUtil.Enum( "Records, Trophy" )

class GolfPage( ShtikerPage ):
            
    """
    Purpose: The GolfPage class provides the basic functionality for
    switching between the different pages like records, and trophies.

    Note: The GolfPage is a singleton object because only one instance of
    the page should exist at a time.
    """

    ######################################################################
    # Class variables 
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    notify = DirectNotifyGlobal.directNotify.newCategory( "GolfPage" )
    
    def __init__( self ):
        """
        Purpose: The __init__ Method provides the intial construction
        of the GolfPage object as well as constructing the ShtikerPage
        superclass.

        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        ShtikerPage.__init__( self )

        self.avatar = None
        self.mode = PageMode.Trophy

    def enter( self ):
        """
        Purpose: The enter Method.

        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)

        # If the Page has not already been loaded, do so now before
        # the page mode.
        if( not hasattr( self, "title" ) ):
            self.load()
        self.setMode( self.mode, 1 )
            
        # Make the call to the superclass enter method.
        ShtikerPage.enter( self )

    def exit( self ):
        """
        Purpose: The exit Method.

        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)

        self.golfTrophies.hide()
        self.golfRecords.hide()
            
        # Make the call to the superclass exit method.
        ShtikerPage.exit( self )

    def setAvatar( self, av ):
        """
        Purpose: The setAvatar Method sets the current avatar who is
        looking at the GolfPage of the Shtiker book.

        Params: av - The avatar who is looking at the page.
        Return: None
        """

        self.avatar = av
        
    def getAvatar( self ):
        """
        Purpose: The getAvatar Method retrieves the current avatar who is
        looking at the GolfPage of the Shtiker book.

        Params: None
        Return: Avatar - The avatar looking at the page.
        """

        return self.avatar

    def load( self ):
        """
        Purpose: The load Method is to properly load the appropriate
        GUI for the GolfPage of the Shtiker Book.

        Params: None
        Return: None
        """
        
        assert self.notify.debugStateCall(self)
        ShtikerPage.load( self )

        # Load the Records Page GUI
        self.golfRecords = GolfingRecordsUI( self.avatar, self )
        self.golfRecords.hide()
        self.golfRecords.load()

        # Load the Trophy Page GUI
        self.golfTrophies = GolfTrophiesUI( self.avatar, self )
        self.golfTrophies.hide()
        self.golfTrophies.load()
        
        # Page Title
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_scale = 0.1,
            pos = ( 0, 0, 0.65 ),
            )

        # The blue and yellow colors are trying to match the
        # rollover and select colors on the options page:
        normalColor = (1, 1, 1, 1)
        clickColor = (.8, .8, 0, 1)
        rolloverColor = (0.15, 0.82, 1.0, 1)
        diabledColor = (1.0, 0.98, 0.15, 1)
        
        # Load the Fish Page to borrow its tabs
        gui = loader.loadModel( "phase_3.5/models/gui/fishingBook" )


        self.recordsTab = DirectButton(
            parent = self,
            relief = None,
            text = TTLocalizer.GolfPageRecordsTab,
            text_scale = TTLocalizer.GFPRecordsTabTextScale,
            text_align = TextNode.ALeft,
            image = gui.find("**/tabs/polySurface2"),
            image_pos = (0.12,1,-0.91),
            image_hpr = (0,0,-90),
            image_scale = (0.033,0.033,0.035),
            image_color = normalColor,
            image1_color = clickColor,
            image2_color = rolloverColor,
            image3_color = diabledColor,
            text_fg = Vec4(0.2,0.1,0,1),
            command = self.setMode,
            extraArgs = [ PageMode.Records ],
            pos = TTLocalizer.GFPRecordsTabPos,
            )
        self.trophyTab = DirectButton(
            parent = self,
            relief = None,
            text = TTLocalizer.GolfPageTrophyTab,
            text_scale = TTLocalizer.GFPTrophyTabTextScale,
            text_pos = TTLocalizer.GFPRecordsTabTextPos,
            text_align = TextNode.ALeft,
            image = gui.find("**/tabs/polySurface3"),
            image_pos = (-0.28,1,-0.91),
            image_hpr = (0,0,-90),
            image_scale = (0.033,0.033,0.035),
            image_color = normalColor,
            image1_color = clickColor,
            image2_color = rolloverColor,
            image3_color = diabledColor,
            text_fg = Vec4(0.2,0.1,0,1),
            command = self.setMode,
            extraArgs = [ PageMode.Trophy ],
            pos = TTLocalizer.GFPRTrophyTabPos,
            )

        self.recordsTab.setPos(-0.13,0,0.775)
        self.trophyTab.setPos(0.28,0,0.775)
        adjust = -0.20
        self.recordsTab.setX(self.recordsTab.getX() + adjust)
        self.trophyTab.setX(self.trophyTab.getX() + adjust)

        gui.removeNode()
        
    def unload( self ):
        """
        Purpose: The unload Method performs the necessary unloading of
        the GolfPage.

        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        self.avatar = None # break the garbage cycle
        ShtikerPage.unload( self )

    def setMode( self, mode, updateAnyways = 0 ):
        """
        Purpose: The setMode Method sets the current mode of the GolfPage
        of the Shtiker Book.

        Params: mode - the new mode.
                updateAnyways - update the page based on the mode.
        Return: None
        """

        messenger.send( 'wakeup' )

        if( not updateAnyways ):
            if( self.mode == mode ):
                return
            else:
                self.mode = mode

        if( mode == PageMode.Records ):
            self.title[ 'text' ] = TTLocalizer.GolfPageTitleRecords
            self.recordsTab[ 'state' ] = DGG.DISABLED
            self.trophyTab[ 'state' ] = DGG.NORMAL
            
        elif( mode == PageMode.Trophy ):
            self.title[ 'text' ] = TTLocalizer.GolfPageTitleTrophy
            self.recordsTab[ 'state' ] = DGG.NORMAL
            self.trophyTab[ 'state' ] = DGG.DISABLED
            
        else:
            raise StandardError, "GolfPage::setMode - Invalid Mode %s" % ( mode )

        self.updatePage()

    def updatePage( self ):
        """
        Purpose: The updatePage Method updates the GolfPage of the
        ShtikerBook.

        Params: None
        Return: None
        """

        if( self.mode == PageMode.Records ):
            self.golfTrophies.hide()
            self.golfRecords.show()
        elif( self.mode == PageMode.Trophy ):
            self.golfTrophies.show()
            self.golfRecords.hide()
        else:
            raise StandardError, "GolfPage::updatePage - Invalid Mode %s" % ( self.mode )


class GolfingRecordsUI( DirectFrame ):
    """
    Purpose: The GolfingRecordsUI class initializes the user interface for
    displaying the personal best times earned by a toon.
    """

    ######################################################################
    # Class Variables
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    notify = DirectNotifyGlobal.directNotify.newCategory( "GolfingRecordsUI" )

    def __init__( self, avatar, parent = aspect2d ):
        """
        Purpose: The __init__ Method provides the initial construction of
        the GolfingRecordsUI object.

        Params: None
        Return: None
        """

        # Initialize instance variables
        self.avatar = avatar
        self.bestDisplayList = []
        self.lastHoleBest = []
        self.lastCourseBest = []
        self.scrollList = None
        
        # Construct the super class object
        DirectFrame.__init__(
            self,
            parent = parent,
            relief = None,
            pos = ( 0.0, 0.0, 0.0 ),
            scale = ( 1.0, 1.0, 1.0 ),
            )

    def destroy( self ):
        """
        Purpose: The destroy Method properly handles the destruction of
        the GolfingRecordsUI instance by handling appropriate reference
        cleanup.

        Params: None
        Return: None
        """

        # Remove references to UI Components and instance variables for
        # garbage collection purposes.
        self.gui.removeNode()
        self.scrollList.destroy()
        del self.avatar,  self.lastHoleBest, self.lastCourseBest, self.bestDisplayList, self.scrollList
        
        # Destroy the DirectFrame super class.
        DirectFrame.destroy( self )

    def load( self ):
        """
        Purpose: The load Method handles the construction of the specific
        UI components that make up the RaceRecordsUI object.

        Params: None
        Return: None
        """
        self.gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")

        self.listXorigin = -0.5
        self.listFrameSizeX = 1.5
        self.listZorigin = -0.9 
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.labelXstart = self.itemFrameXorigin + 0.293

        self.scrollList = DirectScrolledList(
            parent = self,
            relief = None,
            pos = (0, 0, 0),
            # inc and dec are DirectButtons
            # incButton is on the bottom of page, decButton is on the top!
            incButton_image = (self.gui.find("**/FndsLst_ScrollUp"),
                               self.gui.find("**/FndsLst_ScrollDN"),
                               self.gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               self.gui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_scale = (self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale),
            incButton_pos = (self.labelXstart, 0, self.itemFrameZorigin - 0.999),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1, 1, 1, 0.2),
            decButton_image = (self.gui.find("**/FndsLst_ScrollUp"),
                               self.gui.find("**/FndsLst_ScrollDN"),
                               self.gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               self.gui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_scale = (self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale),
            decButton_pos = (self.labelXstart, 0, self.itemFrameZorigin + 0.227),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1, 1, 1, 0.2),
            
            # itemFrame is a DirectFrame
            itemFrame_pos = (self.itemFrameXorigin, 0, self.itemFrameZorigin),
            itemFrame_scale = 1.0,
            itemFrame_relief = DGG.SUNKEN,
            # frameSize is (minX,maxX,minZ,maxZ);  where x goes left->right neg->pos,
            # and z goes bottom->top neg->pos
            itemFrame_frameSize = (self.listXorigin, self.listXorigin + self.listFrameSizeX,
                                   self.listZorigin, self.listZorigin + self.listFrameSizeZ),
            itemFrame_frameColor = (0.85, 0.95, 1, 1),
            itemFrame_borderWidth = (0.01, 0.01),
            # each item is a button with text on it
            numItemsVisible = 12,
            # need to set height of each entry to avoid list text running off end of listbox
            forceHeight = 0.083,
            items = [],
            )

        # course bests
        for courseId in GolfGlobals.CourseInfo:
            courseName = GolfGlobals.getCourseName(courseId)
            frame = DirectFrame(
                parent = self.scrollList,
                relief = None)
            courseNameDisplay = DirectLabel(
                parent = frame,
                relief = None,
                pos = (-0.475, 0, 0.05),
                text = courseName,
                text_align = TextNode.ALeft,
                text_scale = 0.075,
                text_fg = (0.85, 0.64, 0.13, 1.0),
                text_shadow = (0, 0, 0, 1),
                text_font = ToontownGlobals.getSignFont()
                )
            bestScoreDisplay = DirectLabel(
                parent = frame,
                relief = None,
                pos = (0.9, 0, 0.05),
                text = TTLocalizer.KartRace_Unraced,
                text_scale = 0.06,
                text_fg = (0.0, 0.0, 0.0, 1.0),
                text_font = ToontownGlobals.getToonFont()
                )
            # save this one for updating
            self.bestDisplayList.append(bestScoreDisplay)
            # add to scrolled list
            self.scrollList.addItem(frame)
            
        # hole bests
        for holeId in GolfGlobals.HoleInfo:
            holeName = GolfGlobals.getHoleName(holeId)
            frame = DirectFrame(
                parent = self.scrollList,
                relief = None)
            holeNameDisplay = DirectLabel(
                parent = frame,
                relief = None,
                pos = (-0.475, 0, 0.05),
                text = holeName,
                text_align = TextNode.ALeft,
                text_scale = 0.075,
                text_fg = (0.95, 0.95, 0.0, 1.0),
                text_shadow = (0, 0, 0, 1),
                text_font = ToontownGlobals.getSignFont()
                )
            bestScoreDisplay = DirectLabel(
                parent = frame,
                relief = None,
                pos = (0.9, 0, 0.05),
                text = TTLocalizer.KartRace_Unraced,
                text_scale = 0.06,
                text_fg = (0.0, 0.0, 0.0, 1.0),
                text_font = ToontownGlobals.getToonFont()
                )
            # save this one for updating
            self.bestDisplayList.append(bestScoreDisplay)            
            # add to scrolled list
            self.scrollList.addItem(frame)

    def show( self ):
        # update personal best times
        bestHoles = self.avatar.getGolfHoleBest()
        bestCourses = self.avatar.getGolfCourseBest()
        # but only if they have changed
        if bestHoles != self.lastHoleBest or bestCourses != self.lastCourseBest:
            numCourse = len(GolfGlobals.CourseInfo.keys())
            numHoles = len(GolfGlobals.HoleInfo.keys())
            for i in xrange(numCourse):
                score = bestCourses[i]
                if score != 0:
                    # use their best score
                    self.bestDisplayList[i]['text'] = str(score),
                else:
                    self.bestDisplayList[i]['text'] = TTLocalizer.KartRace_Unraced
            for i in xrange(numHoles):
                score = bestHoles[i]
                if score != 0:
                    self.bestDisplayList[i+numCourse]['text'] = str(score)
                else:
                    self.bestDisplayList[i+numCourse]['text'] = TTLocalizer.KartRace_Unraced
        self.lastHoleBest = bestHoles[:]
        self.lastCourseBest = bestCourses[:]
        DirectFrame.show( self )
        
    def regenerateScrollList(self):
        print "### regen scroll"
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for label in self.bestDisplayList:
                label.detachNode()
            self.scrollList.destroy()
            self.scrollList = None
            
        self.scrollList.scrollTo(selectedIndex)

        
class GolfTrophiesUI( DirectFrame ):
    """
    Purpose: The GolfTrophiesUI class initializes the user interface for
    displaying the golfing trophies earned by a toon.
    """

    ######################################################################
    # Class Variables
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    notify = DirectNotifyGlobal.directNotify.newCategory( "GolfTrophiesUI" )

    def __init__( self, avatar, parent = aspect2d ):
        """
        Purpose: The __init__ Method provides the initial construction of
        the RacingTrophiesUI object.

        Params: None
        Return: None
        """

        # Initialize instance variables
        self.avatar = avatar
        self.trophyPanels = []
        self.cupPanels = []
        self.trophies = None
        self.cups = None
        self.trophyTextDisplay = None
        
        # Construct the super class object
        DirectFrame.__init__(
            self,
            parent = parent,
            relief = None,
            pos = ( 0.0, 0.0, 0.0 ),
            scale = ( 1.0, 1.0, 1.0 ),
            )

    def destroy( self ):
        """
        Purpose: The destroy Method properly handles thepass                 destruction of
        the RacingTrophiesUI instance by handling appropriate reference
        cleanup.

        Params: None
        Return: None
        """
        for panel in self.trophyPanels:
            panel.destroy()
        for panel in self.cupPanels:
            panel.destroy()            
        self.currentHistory.destroy()
        self.trophyTextDisplay.destroy()
        
        # Remove references to UI Components and instance variables for
        # garbage collection purposes.
        del self.avatar, self.currentHistory, self.trophyPanels, self.trophies, self.trophyTextDisplay, self.cups, self.cupPanels
        
        # Destroy the DirectFrame super class.
        DirectFrame.destroy( self )

    def load( self ):
        """pass                
        Purpose: The load Method handles the construction of the specific
        UI components that make up the RacingTrophiesUI object.

        Params: None
        Return: None
        """
        self.trophies = base.localAvatar.getGolfTrophies()[:]
        self.cups = base.localAvatar.getGolfCups()[:]

        xStart = -0.76
        yStart = 0.475
        xOffset = 0.17
        yOffset = 0.23
        # display the trophies a toon has
        for j in range(GolfGlobals.NumCups):
            for i in range(GolfGlobals.TrophiesPerCup):
                trophyPanel = DirectLabel(
                    parent = self,
                    relief = None,
                    pos = (xStart + (i * xOffset),
                           0.0,
                           yStart - (j * yOffset)),
                    state = DGG.NORMAL,
                    image = DGG.getDefaultDialogGeom(),
                    image_scale = (0.75, 1, 1),
                    image_color = (0.8, 0.8, 0.8, 1),
                    text = TTLocalizer.SuitPageMystery[0],
                    text_scale = 0.45,
                    text_fg = (0, 0, 0, 1),
                    text_pos = (0, 0, -0.25),
                    text_font = ToontownGlobals.getInterfaceFont(),
                    text_wordwrap = 5.5
                    )

                trophyPanel.scale = 0.2
                trophyPanel.setScale(trophyPanel.scale)

                # add to master list
                self.trophyPanels.append(trophyPanel)

        xStart = -0.25
        yStart = -0.38
        xOffset = 0.25
        for i in range(GolfGlobals.NumCups):
            cupPanel = DirectLabel(
                parent = self,
                relief = None,
                pos = (xStart + (i * xOffset), 0.0, yStart),
                state = DGG.NORMAL,
                image = DGG.getDefaultDialogGeom(),
                image_scale = (0.75, 1, 1),
                image_color = (0.8, 0.8, 0.8, 1),
                text = TTLocalizer.SuitPageMystery[0],
                text_scale = 0.45,
                text_fg = (0, 0, 0, 1),
                text_pos = (0, 0, -0.25),
                text_font = ToontownGlobals.getInterfaceFont(),
                text_wordwrap = 5.5
                )
            cupPanel.scale = 0.3
            cupPanel.setScale(cupPanel.scale)
            self.cupPanels.append(cupPanel)

        # display the current number of tickets a toon has
        self.currentHistory = DirectLabel(
            parent = self,
            relief = None,
            #image = loader.loadModel('phase_6/models/karting/tickets'),
            #image_pos = (0.2,0,-0.635),
            #image_scale = 0.2,
            text = '', #TTLocalizer.KartPageTickets + str(self.avatar.getTickets()),
            text_scale = 0.05,
            text_fg = ( 0, 0, 0.95, 1.0 ),
            text_pos = ( 0, -0.65),
            #text_font = ToontownGlobals.getSignFont()
            )
        
        # display the text description of a moused over trophy
        self.trophyTextDisplay = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_scale = 0.07,
            text_fg = ( 1, 0, 0, 1 ),
            text_shadow = ( 0, 0, 0, 0 ),
            text_pos = ( 0.0, -0.175 ),
            text_font = ToontownGlobals.getInterfaceFont()
            )

        self.updateTrophies()
        
    def grow(self, index, pos):
        self.trophyPanels[index]['image_color'] = Vec4(1.0, 1.0, 0.8, 1.0)
        if index < GolfGlobals.NumTrophies:
            self.trophyTextDisplay['text'] = TTLocalizer.GolfTrophyTextDisplay % \
                                             {'number': index +1,
                                              'desc' : TTLocalizer.GolfTrophyDescriptions[index]}
            # update the current history
            historyIndex = GolfGlobals.getHistoryIndexForTrophy(index)
            if historyIndex >= 0:
                self.currentHistory['text'] = TTLocalizer.GolfCurrentHistory % \
                                    {'historyDesc' : TTLocalizer.GolfHistoryDescriptions[historyIndex],
                                     'num' : self.avatar.getGolfHistory()[historyIndex]}
                                     

    def shrink(self, index, pos):
        self.trophyPanels[index]['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
        self.trophyTextDisplay['text'] = ""
        self.currentHistory['text']=''

    def growCup(self, index, pos):
        self.cupPanels[index]['image_color'] = Vec4(1.0, 1.0, 0.8, 1.0)
        if index < GolfGlobals.NumTrophies:
            self.trophyTextDisplay['text'] = TTLocalizer.GolfCupTextDisplay % \
                                             {'number': index +1,
                                              'desc' : TTLocalizer.GolfCupDescriptions[index]}
    def shrinkCup(self, index, pos):
        self.cupPanels[index]['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
        self.trophyTextDisplay['text'] = ""            
    
    def show( self ):
        # update current history
        self.currentHistory['text'] = ''
        # see if the any new trophies need to be displayed
        if self.trophies != base.localAvatar.getGolfTrophies():
            self.trophies = base.localAvatar.getGolfTrophies()
            self.cups = base.localAvatar.getGolfCups()
            self.updateTrophies()
        DirectFrame.show( self )
        
    def updateTrophies( self ):
        for t in range(len(self.trophyPanels)):
            if self.trophies[t]:
                # add our special scaling functions
                trophyPanel = self.trophyPanels[t]
                trophyPanel['text'] = ""
                # get a trophy
                #trophyModel = RacingTrophy(t / RaceGlobals.TrophiesPerCup)
                golfTrophy = trophyPanel.find('**/*GolfTrophy*')
                if golfTrophy.isEmpty():
                    trophyModel = GolfTrophy(t)
                    trophyModel.reparentTo(trophyPanel)
                    trophyModel.nameLabel.hide()
                    trophyModel.setPos(0,0,-0.4)
                trophyPanel['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
                trophyPanel.bind(DGG.ENTER, self.grow, extraArgs=[t])
                trophyPanel.bind(DGG.EXIT, self.shrink, extraArgs=[t])
            else:
                # handle going backward
                trophyPanel = self.trophyPanels[t]
                toBeNukedGolfTrophy = trophyPanel.find('**/*GolfTrophy*')
                if not toBeNukedGolfTrophy.isEmpty():
                    toBeNukedGolfTrophy.removeNode()
                trophyPanel['text'] = TTLocalizer.SuitPageMystery[0]
                trophyPanel['image_color'] = Vec4(0.8, 0.8, 0.8, 1)
                trophyPanel.unbind(DGG.ENTER)
                trophyPanel.unbind(DGG.EXIT)
                pass
        for t in range(len(self.cupPanels)):
            if self.cups[t]:
                # add our special scaling functions
                cupPanel = self.cupPanels[t]
                cupPanel['text'] = ""
                # get a cup
                #cupModel = RacingCup(t / RaceGlobals.TrophiesPerCup)
                cupTrophy = cupPanel.find('**/*GolfTrophy*')
                if cupTrophy.isEmpty():
                    cupModel = GolfTrophy(t + GolfGlobals.NumTrophies)
                    cupModel.reparentTo(cupPanel)
                    cupModel.nameLabel.hide()
                    cupModel.setPos(0,0,-0.4)
                cupPanel['image_color'] = Vec4(1.0, 1.0, 1.0, 1.0)
                cupPanel.bind(DGG.ENTER, self.growCup, extraArgs=[t])
                cupPanel.bind(DGG.EXIT, self.shrinkCup, extraArgs=[t])
            else:
                cupPanel = self.cupPanels[t]
                toBeNukedGolfCup = cupPanel.find('**/*GolfTrophy*')
                if not toBeNukedGolfCup.isEmpty():
                    toBeNukedGolfCup.removeNode()
                cupPanel['text'] = TTLocalizer.SuitPageMystery[0]
                cupPanel['image_color'] = Vec4(0.8, 0.8, 0.8, 1)
                cupPanel.unbind(DGG.ENTER)
                cupPanel.unbind(DGG.EXIT)                

class GolfTrophy(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory("GolfTrophy")

    def __init__(self, level, *args, **kwargs):
        # Don't init the fishing trophy class.
        opts = {'relief':None}
        opts.update(kwargs)
        DirectFrame.__init__(self,*args,**opts)
        
        # This is a temporary location for this model
        self.trophy = loader.loadModel("phase_6/models/golf/golfTrophy")
        self.trophy.reparentTo(self)
        # Fix the model
        self.trophy.setPos(0,1,0)
        self.trophy.setScale(0.1)
        self.base = self.trophy.find("**/trophyBase")
        self.column = self.trophy.find("**/trophyColumn")
        self.top = self.trophy.find("**/trophyTop")
        self.topBase = self.trophy.find("**/trophyTopBase")
        self.statue = self.trophy.find("**/trophyStatue")
        # Give the base a nice marble look
        self.base.setColorScale(1,1,0.8,1)
        self.topBase.setColorScale(1,1,0.8,1)
        
        self.greyBowl = loader.loadModel("phase_6/models/gui/racingTrophyBowl2")
        self.greyBowl.reparentTo(self)
        self.greyBowl.setPos(0,.5,0)
        self.greyBowl.setScale(2.0)

        self.goldBowl = loader.loadModel("phase_6/models/gui/racingTrophyBowl")
        self.goldBowl.reparentTo(self)
        self.goldBowl.setPos(0,.5,0)
        self.goldBowl.setScale(2.0)
        self.goldBowlBase = self.goldBowl.find("**/fishingTrophyBase")
        self.goldBowlBase.hide()

        self.nameLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0,0,-0.15),
            text = "",
            text_scale = 0.125,
            text_fg = Vec4(0.9,0.9,0.4,1),
            )
        
        self.shadow = loader.loadModel("phase_3/models/props/drop_shadow")
        self.shadow.reparentTo(self)
        self.shadow.setColor(1,1,1,0.2)
        self.shadow.setPosHprScale(0,1,0.35, 0,90,0, 0.1,0.14,0.1)
        
        self.setLevel(level)

    def setLevel(self, level):
        assert self.notify.debugStateCall(self)
        self.level = level
        if level == -1:
            self.trophy.hide()
            self.greyBowl.hide()
            self.goldBowl.hide()
            self.nameLabel.hide()
        # Trophies are all a mix-and-match of different attributes.
        else:
            # Always show the name label.
            self.nameLabel.show()
            # Show the correct bowl/trophy.
            if level >= 30:
                self.trophy.hide()
                self.greyBowl.hide()
                self.goldBowl.show()
                self.goldBowlBase.hide()
            # For all other trophies, show the trophy graphic.
            else:
                self.trophy.show()
                self.goldBowl.hide()
                self.greyBowl.hide()
            # Set the heights for the last three trophies.
            # Why they would scale at different rates is beyond me.
            if level == 30:
                self.goldBowl.setScale(4.4,3.1,3.1)
                #self.column.setScale(1.3229, 1.26468, 2.11878)
                #self.top.setPos(0,0,0.5)
            elif level == 31:
                #self.column.setScale(1.3229, 1.26468, 2.61878)
                #self.top.setPos(0,0,0.5)
                self.goldBowl.setScale(3.6,3.5,3.5)
            elif level >= 32:
                #self.column.setScale(1.3229, 1.26468, 3.11878)
                #self.top.setPos(0,0,0.5)
                self.goldBowl.setScale(5.6,3.9,3.9)
            # Set the color.
            if (level ) % 3 == 0:
                self.column.setScale(1.3229, 1.26468, 1.11878)
                self.top.setPos(0,0,-1)
                self.__bronze()
            elif (level ) % 3 == 1:
                self.column.setScale(1.3229, 1.26468, 1.61878)
                self.top.setPos(0,0,-.5)
                self.__silver()
            elif (level ) % 3 == 2:
                self.column.setScale(1.3229, 1.26468, 2.11878)
                self.top.setPos(0,0,0)
                self.__gold()
            # Set the column color.
            if level < 10:
                self.__tealColumn()
            elif level < 20:
                self.__purpleColumn()
            elif level < 30:
                self.__blueColumn()
            else:
                self.__redColumn()

    # Methods to color the trophy statue
    def __bronze(self):
        assert self.notify.debugStateCall(self)
        self.statue.setColorScale(0.9,0.6,0.33,1)

    def __silver(self):
        assert self.notify.debugStateCall(self)
        self.statue.setColorScale(0.9,0.9,1,1)

    def __gold(self):
        assert self.notify.debugStateCall(self)
        self.statue.setColorScale(1,0.95,0.1,1)

    def __platinum(self):
        assert self.notify.debugStateCall(self)
        self.statue.setColorScale(1,0.95,0.1,1)

    # Methods to color the trophy column
    def __tealColumn(self):
        assert self.notify.debugStateCall(self)
        self.column.setColorScale(.5,1.2,.85,1)

    def __purpleColumn(self):
        assert self.notify.debugStateCall(self)
        self.column.setColorScale(1,.7,.95,1)

    def __redColumn(self):
        assert self.notify.debugStateCall(self)
        self.column.setColorScale(1.2,.6,.6,1)

    def __yellowColumn(self):
        assert self.notify.debugStateCall(self)
        self.column.setColorScale(1,1,.8,1)

    def __blueColumn(self):
        assert self.notify.debugStateCall(self)
        self.column.setColorScale(.6,.75,1.2,1)

    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.trophy.removeNode()
        self.goldBowl.removeNode()
        self.greyBowl.removeNode()
        self.shadow.removeNode()
        DirectFrame.destroy(self)
