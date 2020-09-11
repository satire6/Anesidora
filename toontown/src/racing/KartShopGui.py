 
##########################################################################
# Module: KartShopGuiMgr.py
# Purpose: The KartShopGuiMgr Module provides the implementation for the
#          various UI Menu Dialogs that are needed for purchasing a kart
#          and accessories.
# Date: 4/12/05
# Author: jjtaylor
##########################################################################

##########################################################################
# Panda Import Modules
##########################################################################
if __name__ == "__main__":
        from direct.directbase import DirectStart
from pandac.PandaModules import *    
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject, PythonUtil

##########################################################################
# Toontown Import Modules
##########################################################################
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
from KartShopGlobals import *
from toontown.racing.Kart import Kart
from toontown.shtiker.KartPage import KartViewer
from KartDNA import *
from toontown.toontowngui.TeaserPanel import TeaserPanel

##########################################################################
# Python Import Modules
##########################################################################
if( __debug__ ):
    import pdb

##########################################################################
# KartShopGui Globals
##########################################################################
MENUS = PythonUtil.Enum( 'MainMenu, BuyKart, BuyAccessory, ReturnKart, ConfirmBuyAccessory, ConfirmBuyKart, BoughtKart, BoughtAccessory, TeaserPanel' )
MM_OPTIONS  = PythonUtil.Enum( 'Cancel, BuyAccessory, BuyKart',-1 )
BK_OPTIONS  = PythonUtil.Enum( 'Cancel, BuyKart',-1 )
BA_OPTIONS  = PythonUtil.Enum( 'Cancel, BuyAccessory',-1 )
RK_OPTIONS  = PythonUtil.Enum( 'Cancel, ReturnKart',-1 )
CBK_OPTIONS = PythonUtil.Enum( 'Cancel, BuyKart',-1 )
CBA_OPTIONS = PythonUtil.Enum( 'Cancel, BuyAccessory',-1)
BTK_OPTIONS = PythonUtil.Enum( 'Ok',-1)  #options for "you bought this kart" dialogue
BTA_OPTIONS = PythonUtil.Enum( 'Ok',-1)  #options for "you bought this accessory" dialogue

KS_TEXT_SIZE_BIG = TTLocalizer.KSGtextSizeBig
KS_TEXT_SIZE_SMALL = TTLocalizer.KSGtextSizeSmall

class KartShopGuiMgr( object, DirectObject.DirectObject ):
    """
    Purpose: The KartShopGuiMgr provides a high level interface for
    managing the GUI Dialog Menus that are required for purchasing a
    kart and accessories.

    Note: The KartShopGuiMgr is based on the Singleton pattern, meaning
    that there can be ONE AND ONLY ONE instance available at a time.
    """

    ######################################################################
    # Enable Class as a Singleton
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    
    ######################################################################
    # Class Variable Definitions
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr" )

    ######################################################################
    # Inner Class UI Definitions
    ######################################################################
    class MainMenuDlg( DirectFrame ):
        """
        Purpose: The MainMenuDlg provides the functionality and graphical
        component of the Main Menu interface that allows the player to
        decide whether s/he wants to purchase a new kart or buy accessories for an existing kart.
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.MainMenuDlg" )

        def __init__( self, doneEvent ):
            """
            Purpose: The __init__ Method provides for the initial
            construction of the MainMenuDlg instance, including the
            loading of models.

            params: doneEvent - Event thrown when Menu is closed.
            return: None
            """

            # Load the Model that will be used for UI element
            model = loader.loadModel( 'phase_6/models/gui/Kart_MainMenuPanel' )
            self.modelScale = .75 
            

            
            DirectFrame.__init__( self,
                                  relief = None,
                                  state = 'normal',
                                  geom = model,
                                  text_scale = 0.10,
                                  geom_scale = self.modelScale,
                                  pos = (0, 0, -.01 ),
                                  frameSize = (-1,1,-1,1) )
            
            self.initialiseoptions( KartShopGuiMgr.MainMenuDlg )

            # Initialize Menu Buttons
            self.cancelButton = DirectButton(
                parent = self,
                relief = None,
                geom = model.find( '**/CancelIcon' ),
                image = ( model.find( '**/CancelButtonUp' ),
                          model.find( '**/CancelButtonDown' ),
                          model.find( '**/CancelButtonRollover' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ MM_OPTIONS.Cancel ] ) )
                )
           
            self.buyKartButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/BuyKartButtonUp' ),
                          model.find( '**/BuyKartButtonDown' ),
                          model.find( '**/BuyKartButtonRollover' ),
                          model.find( '**/BuyKartButtonDisabled' )
                          ),
                scale = self.modelScale,
                geom = model.find( '**/BuyKartIcon' ),
                text = TTLocalizer.KartShop_BuyKart,
                text_scale = KS_TEXT_SIZE_BIG,
                text_pos = ( -0.20, 0.34),
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ MM_OPTIONS.BuyKart ] ) )
                )
            
            self.buyAccessoryButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/BuyAccessoryButtonUp' ),
                          model.find( '**/BuyAccessoryButtonDown' ),
                          model.find( '**/BuyAccessoryButtonRollover' ),
                          model.find( '**/BuyAccessoryButtonDisabled' )
                          ),
                geom = model.find( '**/BuyAccessoryIcon' ),
                image3_color = Vec4( 0.6, 0.6, 0.6, 1 ),
                scale = self.modelScale,
                text = TTLocalizer.KartShop_BuyAccessories,
                text_scale = KS_TEXT_SIZE_BIG,
                text_pos = ( -0.1, 0.036),
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ MM_OPTIONS.BuyAccessory ] ) )
                )

                    
            #We won't disable the accessory button here because we do want players
            #to be able to window shop even if they have no room for an accessory

            self.updateButtons()

        def updateButtons(self):
            # but you can't window shop with no kart to view the accessories on
            if not base.localAvatar.hasKart():
                self.buyAccessoryButton['state'] = DGG.DISABLED
            else:
                self.buyAccessoryButton['state'] = DGG.NORMAL

        def show(self):
            # make the buttons update every time we show menu
            self.updateButtons()
            DirectFrame.DirectFrame.show(self)
            
    class BuyKartDlg( DirectFrame ):
        """
        Purpose: The BuyKartDlg provides the functionality and graphical
        component that allows the player to decide which type of Kart s/he
        would like to purchase and provide statistics such as the cost.
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.BuyKartDlg" )

        def __init__( self, doneEvent ):
            """
            Purpose: The __init__ Method provides the initial construction
            of the BuyKartDlg by loading appropriate models and textures before
            it constructs the necessary Direct GUI elements.

            params: doneEvent - Event thrown when the Dlg is closed.
            return: None
            """
            self.modelScale = 1
            model = loader.loadModel( 'phase_6/models/gui/BuyKartPanel' )
            
            #create list of karts not owned by player
            self.unownedKartList = KartDict.keys()
            if base.localAvatar.hasKart():
                k = base.localAvatar.getKartBodyType()
                if k in self.unownedKartList:
                        self.unownedKartList.remove(k)

            #number of unownded karts available 
            self.numKarts = len(self.unownedKartList)
            #index of currently selected kart in the list of unowned karts
            self.curKart =  0       
            
            DirectFrame.__init__(
                self,
                relief = None,
                state = 'normal',
                geom = model,
                geom_scale = self.modelScale,
                frameSize = ( -1, 1, -1, 1 ),
                pos = ( 0, 0, -0.01),
                text_wordwrap = 26,
                text_scale = KS_TEXT_SIZE_BIG,
                text_pos = ( 0, 0 )
                )
            self.initialiseoptions( KartShopGuiMgr.BuyKartDlg )

            self.ticketDisplay = DirectLabel(
                parent = self,
                relief = None,
                text = str(base.localAvatar.getTickets()),
                text_scale = KS_TEXT_SIZE_SMALL,
                text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                text_shadow = ( 0, 0, 0, 1 ),
                text_pos = ( 0.44, -0.55 ),
                text_font = ToontownGlobals.getSignFont()
            )
            
   
            
            self.buyKartButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/BuyKartButtonUp' ),
                          model.find( '**/BuyKartButtonDown' ),
                          model.find( '**/BuyKartButtonRollover' ),
                          model.find( '**/BuyKartButtonDisabled' )
                          ),
                
                scale = self.modelScale,
                #TODO: finalize this text
                text = TTLocalizer.KartShop_BuyKart,
                text_scale = KS_TEXT_SIZE_BIG,
                text_pos = ( 0, -.534),
                pressEffect = False,                           
                command = ( lambda : messenger.send( doneEvent, [ self.unownedKartList[self.curKart] ] )        )
                )
 
            self.cancelButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/CancelButtonUp' ),
                          model.find( '**/CancelButtonDown' ),
                          model.find( '**/CancelButtonRollover' ) ),
                geom = model.find( '**/CancelIcon' ),
                scale = self.modelScale,
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ BK_OPTIONS.Cancel ] ) )
                )
            #-------------- Arrows ---------------
            self.arrowLeftButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/ArrowLeftButtonUp' ),
                          model.find( '**/ArrowLeftButtonDown' ),
                          model.find( '**/ArrowLeftButtonRollover' ),
                          model.find( '**/ArrowLeftButtonInactive' )
                          ),
                scale = self.modelScale,
                pressEffect = False,
                command =  self.__handleKartChange,
                extraArgs = [-1]
                )
                
            self.arrowRightButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/ArrowRightButtonUp' ),
                          model.find( '**/ArrowRightButtonDown' ),
                          model.find( '**/ArrowRightButtonRollover' ),
                          model.find( '**/ArrowRightButtonInactive') 
                          ),
                scale = self.modelScale,
                #frameSize = ( 1, -1, 1, -1 ),
                pressEffect = False,
                command =  self.__handleKartChange,
                extraArgs = [1]
                )
                
   
            self.kartView = KartViewer([self.curKart,-1,-1,-1,-1,-1,-1,-1,-1], parent = self)
            self.kartView.setPos( model.find( "**/KartViewerFrame" ).getPos())
            self.kartView.load( model, "KartViewerFrame", ["rotate_right_up","rotate_right_down","rotate_right_roll","rotate_right_down", (.255,-.054)], ["rotate_left_up","rotate_left_down","rotate_left_roll","rotate_left_down", (-.24,-.054)], (0,-.055) )
            self.kartView.setBounds( -0.38, 0.38, .0035, 0.53 )   
            self.kartView.setBgColor( 1.0, 1.0, 0.8, 1.0 )
            
            self.showKart()

            self.initialize = True
            model.removeNode()
                

        def showKart(self):
            #as long as some karts exist
            self.buyKartButton.configure(text=TTLocalizer.KartShop_BuyKart)
            self.buyKartButton.configure(text_scale = KS_TEXT_SIZE_BIG)     
            if self.numKarts > 0:
                info =  getKartTypeInfo(self.unownedKartList[self.curKart])
                description = info[KartInfo.name]
                cost = TTLocalizer.KartShop_Cost % (info[KartInfo.cost])
                self.kartDescription = DirectButton(
                            parent = self,
                            relief = None,
                            scale = self.modelScale,
                            text = description,
                            text_pos = (0,-.29),
                            text_scale = KS_TEXT_SIZE_SMALL,
                            pressEffect = False,
                            textMayChange = True,
                            )
                self.kartCost = DirectButton(
                            parent = self,
                            relief = None,
                            scale = self.modelScale,
                            text = cost,
                            text_pos = (0,-.365),
                            text_scale = KS_TEXT_SIZE_SMALL,
                            pressEffect = False,
                            textMayChange = True,
                            )
                self.buyKartButton['state'] = DGG.NORMAL

                #should arrows be active?               
                self.arrowRightButton['state'] = DGG.DISABLED
                self.arrowLeftButton['state'] = DGG.DISABLED
                if self.numKarts > self.curKart + 1:
                        self.arrowRightButton['state'] = DGG.NORMAL
                if self.curKart > 0:
                        self.arrowLeftButton['state'] = DGG.NORMAL

                #does the player have enough tickets to buy this kart?
                if info[KartInfo.cost] > base.localAvatar.getTickets():
                        #disable buy button
                        self.buyKartButton['state'] = DGG.DISABLED
                        self.buyKartButton.configure(text_scale = KS_TEXT_SIZE_SMALL*.75)
                        self.buyKartButton.configure(text=TTLocalizer.KartShop_NotEnoughTickets)
                        #Put cost in red to indicate you can't affor to buy this
                        self.kartCost.configure(text_fg=(0.95, 0, 0.0, 1.0 ))

                #finally load kart
                #TODO: convert to kartviewer
                self.kartView.refresh([self.unownedKartList[self.curKart],-1,-1,-1,-1,-1,-1,-1,-1])
                self.kartView.show()

        
            
        def __handleKartChange(self, nDir):
            self.curKart = (self.curKart + nDir) % self.numKarts 
            self.kartDescription.destroy()
            self.kartCost.destroy()
            #messenger.send("RESET_KARTSHOP_TIMER")
            self.showKart()
            return
                
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BuyKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:
                    self.kartView.destroy()
                    DirectFrame.destroy(self)

   
    class ReturnKartDlg( DirectFrame ):
        """
        Purpose: The ReturnKartDlg provides the functionality and graphical
        component that allows the player to decide whether or not to return
        his/her currently owned kart. 
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.ReturnKartDlg" )
        
        def __init__( self, doneEvent ):
                """
                Purpose: The __init__ Method provides the initial construction
                of the ReturnKartDlg by loading appropriate models and textures before
                it constructs the necessary Direct GUI elements.
                params: doneEvent - Event thrown when the Dlg is closed.
                return: None
                """
        
                self.modelScale = 1
                model = loader.loadModel( 'phase_6/models/gui/ReturnKartPanel' )
                   
                DirectFrame.__init__(
                    self,
                    relief = None,
                    state = 'normal',
                    geom = model,
                    geom_scale = self.modelScale,
                    frameSize = ( -1, 1, -1, 1 ),
                    pos = ( 0, 0, -0.01 ),
                    text = TTLocalizer.KartShop_ConfirmReturnKart,
                    text_wordwrap = 11,
                    text_scale = KS_TEXT_SIZE_SMALL*.9,
                    text_pos = ( 0, -0.26 )
                    )
                self.initialiseoptions( KartShopGuiMgr.ReturnKartDlg )
           
                self.cancelButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CancelButtonUp' ),
                              model.find( '**/CancelButtonDown' ),
                              model.find( '**/CancelButtonRollover' ) ),
                    geom = model.find( '**/CancelIcon' ),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda : messenger.send( doneEvent, [ RK_OPTIONS.Cancel ] ) )
                    )
                    
                self.okButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CheckButtonUp'),
                              model.find( '**/CheckButtonDown' ),
                              model.find( '**/CheckButtonRollover' ) ),
                    geom = model.find('**/CheckIcon'),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda: messenger.send(doneEvent, [ RK_OPTIONS.ReturnKart ]) ), 
                    )   
                            
                oldDNA = list(base.localAvatar.getKartDNA()) 
                    
                #show kart without any accessories and only default rims
                for d in range(len(oldDNA)):
                        if d == KartDNA.bodyType:
                                continue
                        else:
                                oldDNA[d] = InvalidEntry
                                    
                self.kartView = KartViewer(oldDNA, parent = self)
                self.kartView.setPos( model.find( "**/KartViewerFrame" ).getPos() )
                self.kartView.load( model, "KartViewerFrame", [], [], None )
                self.kartView.setBounds( -0.38, 0.38, -.04, 0.49 )  
                self.kartView.setBgColor( 1.0, 1.0, 0.8, 1.0 )
                self.kartView.show()
            
            

                # Remove the redundant node from the scenegraph
                model.removeNode()
                self.initialize = True
                
                
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BuyKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:                     
                    self.kartView.destroy()
            DirectFrame.destroy( self )


    class BoughtKartDlg( DirectFrame ):
        """
        Purpose: The BoughtKartDlg confirms to the player that their purchase was
        successful and points them towards the sticker book.
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.BoughtKartDlg" )
        
        def __init__( self, doneEvent, kartID ):
                """
                Purpose: The __init__ Method provides the initial construction
                of the BoughtKartDlg by loading appropriate models and textures before
                it constructs the necessary Direct GUI elements.
                params: doneEvent - Event thrown when the Dlg is closed.
                        kartID - which kart the player just bought
                return: None
                """
        
                self.modelScale = 1
                model = loader.loadModel( 'phase_6/models/gui/BoughtKartPanel' )
                
                kartInfo = getKartTypeInfo( kartID)
                name = kartInfo[KartInfo.name]
            
                   
                DirectFrame.__init__(
                    self,
                    relief = None,
                    state = 'normal',
                    geom = model,
                    geom_scale = self.modelScale,
                    frameSize = ( -1, 1, -1, 1 ),
                    pos = ( 0, 0, -0.01 ),
                    text = TTLocalizer.KartShop_ConfirmBoughtTitle,
                    text_wordwrap = 26,
                    text_scale = KS_TEXT_SIZE_SMALL,
                    text_pos = ( 0, -0.26 )
                    )
                self.initialiseoptions( KartShopGuiMgr.BoughtKartDlg )
                self.ticketDisplay = DirectLabel(
                        parent = self,
                        relief = None,
                        text = str(base.localAvatar.getTickets()),
                        text_scale = KS_TEXT_SIZE_SMALL,
                        text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                        text_shadow = ( 0, 0, 0, 1 ),
                        text_pos = ( 0.43, -0.5 ),
                        text_font = ToontownGlobals.getSignFont()
                 )
                self.okButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CheckButtonUp' ),
                              model.find( '**/CheckButtonDown' ),
                              model.find( '**/CheckButtonRollover' ) ),
                    geom = model.find( '**/CheckIcon' ),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda : messenger.send( doneEvent, [ BTK_OPTIONS.Ok ] ) )
                    )
                    
                self.kartView = KartViewer([kartID,-1,-1,-1,-1,-1,-1,-1,-1], parent = self)
                self.kartView.setPos( model.find( "**/KartViewerFrame" ).getPos() )
                self.kartView.load( model, "KartViewerFrame", [], [] )
                self.kartView.setBounds( -0.38, 0.38, -.0425, 0.49 )   
                self.kartView.setBgColor( 1.0, 1.0, 0.8, 1.0 )            
                self.kartView.show()
                    
          
                model.removeNode()
                self.initialize = True
                
                
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BoughtKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:                     
                    self.kartView.destroy()
            DirectFrame.destroy( self )


                
    class ConfirmBuyKartDlg( DirectFrame ):
        """
        Purpose: The ConfirmBuyKartDlg provides the functionality and graphical
        component that allows the player confirm a decision to buy a kart. 
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.ConfirmBuyKartDlg" )

        def __init__( self, doneEvent, kartNum ):
            """
            Purpose: The __init__ Method provides the initial construction
            of the ReturnKartDlg by loading appropriate models and textures before
            it constructs the necessary Direct GUI elements.

            params: doneEvent - Event thrown when the Dlg is closed.
            return: None
            """
            
            
            #the id of the kart selected for purchase
            self.kartNum = kartNum
            self.modelScale = 1
            model = loader.loadModel( 'phase_6/models/gui/ConfirmBuyKartPanel' )
            kartInfo = getKartTypeInfo( kartNum)
            name = kartInfo[KartInfo.name]
            cost = kartInfo[KartInfo.cost]
            
            DirectFrame.__init__(
                self,
                relief = None,
                state = 'normal',
                geom = model,
                geom_scale = self.modelScale,
                frameSize = ( -1, 1, -1, 1 ),
                pos = ( 0, 0, -0.01 ),
                text = TTLocalizer.KartShop_ConfirmBuy % (name, cost),
                text_wordwrap = 11,
                text_scale = KS_TEXT_SIZE_SMALL,
                text_pos = ( 0, -0.26 )
                )
            
            self.initialiseoptions( KartShopGuiMgr.ConfirmBuyKartDlg )
            
            
            self.ticketDisplay = DirectLabel(
                parent = self,
                relief = None,
                text = str(base.localAvatar.getTickets()),
                text_scale = KS_TEXT_SIZE_SMALL,
                text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                text_shadow = ( 0, 0, 0, 1 ),
                text_pos = ( 0.43, -0.5 ),
                text_font = ToontownGlobals.getSignFont()
            )
            
            self.cancelButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/CancelButtonUp' ),
                          model.find( '**/CancelButtonDown' ),
                          model.find( '**/CancelButtonRollover' ) ),
                geom = model.find( '**/CancelIcon' ),
                scale = self.modelScale,
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ CBK_OPTIONS.Cancel ] ) )
                )
            
            self.okButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CheckButtonUp'),
                          model.find( '**/CheckButtonDown' ),
                          model.find( '**/CheckButtonRollover' ) ),
                    geom = model.find( '**/CheckIcon' ),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda: messenger.send(doneEvent, [ CBK_OPTIONS.BuyKart ]) ), 
                    )                
            
            self.kartView = KartViewer([self.kartNum,-1,-1,-1,-1,-1,-1,-1,-1], parent = self)
            self.kartView.setPos( model.find( "**/KartViewerFrame" ).getPos() )
            self.kartView.load( model, "KartViewerFrame", [], [], None )
            self.kartView.setBounds( -0.38, 0.38, -.0425, 0.49 )   
            self.kartView.setBgColor( 1.0, 1.0, 0.8, 1.0 )            
            
            self.initialize = True
            self.kartView.show()
            
  
            model.removeNode()

            
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BuyKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:                    
                   self.kartView.destroy()
                   DirectFrame.destroy( self )
                   
    class BuyAccessoryDlg( DirectFrame ):
        """
        Purpose: The BuyAccessorytDlg provides the functionality and graphical
        component that allows the player to choose accessories for his/her kart. 
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.buyAccessoryDlg" )

        def __init__( self, doneEvent ):
            """
            Purpose: The __init__ Method provides the initial construction
            of the BuyAccessoryDlg by loading appropriate models and textures before
            it constructs the necessary Direct GUI elements.
            
            params: doneEvent - Event thrown when the Dlg is closed.
            return: None
            """
            
            self.modelScale = 1
            model = loader.loadModel( 'phase_6/models/gui/BuyAccessoryPanel' )
            self.doneEvent = doneEvent
                       
            DirectFrame.__init__(
                self,
                relief = None,
                state = 'normal',
                geom = model,
                geom_scale = self.modelScale,
                frameSize = ( -1, 1, -1, 1 ),
                pos = ( 0, 0, -0.01 ),
                text_wordwrap = 26,
                text_scale = 0.10,
                text_fg = Vec4( 0.36, 0.94, 0.93, 1.0 ),
                text_pos = ( 0, 0)
                )
            self.initialiseoptions( KartShopGuiMgr.BuyAccessoryDlg )
            
            self.ticketDisplay = DirectLabel(
                parent = self,
                relief = None,
                text = str(base.localAvatar.getTickets()),
                text_scale = KS_TEXT_SIZE_SMALL,
                text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                text_shadow = ( 0, 0, 0, 1 ),
                text_pos = ( 0.42, -0.6 ),
                text_font = ToontownGlobals.getSignFont()
            )
            
            self.arrowLeftButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/ArrowLeftButtonUp' ),
                          model.find( '**/ArrowLeftButtonDown' ),
                          model.find( '**/ArrowLeftButtonRollover' ),
                          model.find( '**/ArrowLeftButtonInactive' )
                           ),
                scale = self.modelScale,
                text_pos = ( 0, 0 ),
                text_scale = 0.1,
                pressEffect = False,
                command = self.__handleAccessoryChange,
                extraArgs = [-1]
                )
                
            self.arrowRightButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/ArrowRightButtonUp' ),
                          model.find( '**/ArrowRightButtonDown' ),
                          model.find( '**/ArrowRightButtonRollover' ),
                          model.find( '**/ArrowRightButtonInactive' ) 
                          ),
                scale = self.modelScale,
                #frameSize = ( 1, -1, 1, -1 ),
                text_pos = ( 0, 0 ),
                text_scale = 0.1,
                pressEffect = False,
                command = self.__handleAccessoryChange,
                extraArgs = [1]
                )

            self.cancelButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/CancelButtonUp' ),
                          model.find( '**/CancelButtonDown' ),
                          model.find( '**/CancelButtonRollover' ) ),
                geom = model.find( '**/CancelIcon' ),
                scale = self.modelScale,
                command = ( lambda : messenger.send( doneEvent, [ BA_OPTIONS.Cancel ] ) ),
                pressEffect = False
                
                )
                
            self.decalAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/DecalButtonUp' ),
                          model.find( '**/DecalButtonDown' ),
                          model.find( '**/DecalButtonRollover'),
                          model.find( '**/DecalButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.decalType]
                )
                
            self.spoilerAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/SpoilerButtonUp' ),
                          model.find( '**/SpoilerButtonDown' ),
                          model.find( '**/SpoilerButtonRollover' ),
                          model.find( '**/SpoilerButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.spType]
                )
                
            self.eBlockAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/EBlockButtonUp' ),
                          model.find( '**/EBlockButtonDown' ),
                          model.find( '**/EBlockButtonRollover' ),
                          model.find( '**/EBlockButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.ebType]
                )
                
            self.rearAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/RearButtonUp' ),
                          model.find( '**/RearButtonDown' ),
                          model.find( '**/RearButtonRollover' ),
                          model.find( '**/RearButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.bwwType]
                )
                
            self.frontAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/FrontButtonUp' ),
                          model.find( '**/FrontButtonDown' ),
                          model.find( '**/FrontButtonRollover' ),
                          model.find( '**/FrontButtonDown' ) ),
                scale = self.modelScale,
                #text = ("",TTLocalizer.KartShop_Cancel),
                text_pos = ( 0, 0 ),
                text_scale = 0.1,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.fwwType]
                )
                
                
            self.rimAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/RimButtonUp' ),
                          model.find( '**/RimButtonDown' ),
                          model.find( '**/RimButtonRollover' ),
                          model.find( '**/RimButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.rimsType]
                )
                
                
            self.paintAccButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/PaintButtonUp' ),
                          model.find( '**/PaintButtonDown' ),
                          model.find( '**/PaintButtonRollover' ),
                          model.find( '**/PaintButtonDown' ) ),
                scale = self.modelScale,
                pressEffect = False,
                command = self.__handleAccessoryTypeChange,
                extraArgs = [KartDNA.bodyColor]
                )
  
            #Put buttons into list so we disable/enable them easily
            self.accButtonsDict = {
                    KartDNA.ebType    : self.eBlockAccButton,
                    KartDNA.spType    : self.spoilerAccButton,
                    KartDNA.fwwType   : self.frontAccButton,
                    KartDNA.bwwType   : self.rearAccButton,
                    KartDNA.rimsType  : self.rimAccButton,
                    KartDNA.decalType : self.decalAccButton,
                    KartDNA.bodyColor : self.paintAccButton
                    }
            
            self.buyAccessoryButton = DirectButton(
                            parent = self,
                            relief = None,
                            image = ( model.find( '**/BuyAccessoryButtonUp'),
                                  model.find( '**/BuyAccessoryButtonDown' ),
                                  model.find( '**/BuyAccessoryButtonRollover' ),
                                  model.find( '**/BuyAccessoryButtonDisabled' ) ),
                            scale = self.modelScale,
                            text = TTLocalizer.KartShop_BuyAccessory,
                            text_pos = (0,-.57),
                            text_scale = KS_TEXT_SIZE_SMALL,
                            pressEffect = False,
                            command = self.__handleBuyAccessory
                            )  
                                          
            # Only paid members can purchase karting accessories
            if not base.cr.isPaid():
                    def showTeaserPanel():
                            TeaserPanel(pageName='kartingAccessories')
                    self.buyAccessoryButton['command'] = showTeaserPanel
            
            #get a list of accessories currently owned by the player                
            self.ownedAccList = base.localAvatar.getKartAccessoriesOwned()
            #strip out the -1s (the empty slots)
            while -1 in self.ownedAccList:
                self.ownedAccList.remove(-1)
                
            self.unownedAccDict = getAccessoryDictFromOwned(self.ownedAccList)
                
            #variables to keep track of stuff
            self.curAccType = KartDNA.ebType
            
            #the index of this accessory in the accessory type list
            self.curAccIndex = {}
            for type in self.unownedAccDict:
                #start out at the first accessory in each type list
                self.curAccIndex[type] = 0
                
            #view of kart
            self.kartView = KartViewer(list(base.localAvatar.getKartDNA()), parent = self)
            self.kartView.setPos( model.find( "**/KartViewerFrame" ).getPos() )
            self.kartView.load( model, "KartViewerFrame", ["rotate_right_up","rotate_right_down","rotate_right_roll","rotate_right_down", (.255,0)], ["rotate_left_up","rotate_left_down","rotate_left_roll","rotate_left_down", (-.24,0)], (0,0) )
            self.kartView.setBounds( -0.38, 0.38, .044, 0.58 )     
            self.kartView.setBgColor( 1.0, 1.0, 0.87, 1.0 )
            
           
            self.initialize = True
            #view of kart
            
            self.showAccessory()
            # Remove the redundant node from the scenegraph
            model.removeNode()
            
                
                                 
        def __handleBuyAccessory(self):
            """
            Purpose: The __handleBuyAccessory Method announces the purchase of a kart accessory,
            and refreshes the ticket and accessory displays to (hopefully) reflect new database values

            params: None
            return: None
            """
            #messenger.send("RESET_KARTSHOP_TIMER")
            accessoryID = self.unownedAccDict[self.curAccType][self.curAccIndex[self.curAccType]]
            
            #update owned accessories list locally
            self.ownedAccList.append(accessoryID)
            self.unownedAccDict = getAccessoryDictFromOwned(self.ownedAccList)
            self.__handleAccessoryChange(0)
            messenger.send(self.doneEvent, [accessoryID])
            
        def __handleAccessoryChange(self, nDir):
            #do some checking here as we may have invalidated our current index from
            #buying an accessory?
            
            
            if len(self.unownedAccDict[self.curAccType]) < 1: #we own ALL these accesories
                self.curAccIndex[self.curAccType] = -1
            else:
                 self.curAccIndex[self.curAccType] = (self.curAccIndex[self.curAccType] + nDir) % len(self.unownedAccDict[self.curAccType]) 
            
            #messenger.send("RESET_KARTSHOP_TIMER")
            
            if hasattr(self, 'accDescription'):
                    self.accDescription.destroy()
                    self.accCost.destroy()
            self.showAccessory()
            return
            
        def __handleAccessoryTypeChange(self, type):
            self.curAccType = type
            #messenger.send("RESET_KARTSHOP_TIMER")
            try:
                self.accDescription.destroy()
                self.accCost.destroy()
            except:
                pass #already deleted
                
            #by default turn all accessory buttons on
            for b in self.accButtonsDict:
                self.accButtonsDict[b]['state'] = DGG.NORMAL
            
            #now disable current type
            self.accButtonsDict[self.curAccType]['state'] = DGG.DISABLED
            
            self.showAccessory()
            return
            
        def showAccessory(self):
            #disable everything by default
            self.arrowRightButton['state'] = DGG.DISABLED
            self.arrowLeftButton['state'] = DGG.DISABLED
            self.buyAccessoryButton['state'] = DGG.DISABLED
                    
            #we need these no matter what so just declare first
            self.accDescription = DirectButton(
                parent = self,
                relief = None,
                scale = self.modelScale,
                text = "",
                text_pos = (0,-.33),
                text_scale = KS_TEXT_SIZE_SMALL,
                pressEffect = False,
		text_wordwrap = TTLocalizer.KSGaccDescriptionWordwrap,
                textMayChange = True,
                )  

            self.buyAccessoryButton.configure(text_fg=(0, 0, 0.0, 1.0 ))
            self.buyAccessoryButton.configure(text = TTLocalizer.KartShop_BuyAccessory)
            self.buyAccessoryButton.configure(text_scale = KS_TEXT_SIZE_SMALL)
            self.buyAccessoryButton['state'] = DGG.NORMAL    

        
            #------------------------------
                
            #if there are no accessories of this type
            if len(self.unownedAccDict[self.curAccType]) < 1: 
                #set kart viewer dna to none & display
                #this will set up color space
                self.kartView.setDNA(None)
                self.kartView.hide()            
                #put up message that there's no available accessories of this type
                #TODO: make this localized
                self.accDescription.configure(text=TTLocalizer.KartShop_NoAvailableAcc)
                #disable the buy button
                self.buyAccessoryButton['state'] = DGG.DISABLED              
            #else if there's at least one accessory    
            else:
                #should arrows be active?               
                if self.curAccIndex[self.curAccType] +1 < len(self.unownedAccDict[self.curAccType]):
                        self.arrowRightButton['state'] = DGG.NORMAL
                if self.curAccIndex[self.curAccType] > 0:
                        self.arrowLeftButton['state'] = DGG.NORMAL
                                
                #load kart dna without any accessories and only default rims
                curDNA = None
                curDNA = list(base.localAvatar.getKartDNA()) 
            
                for d in range(len(curDNA)):
                        if d == KartDNA.bodyType or d == KartDNA.accColor or d == KartDNA.bodyColor:
                                continue
                        else:
                                curDNA[d] = -1
                
                curAcc = self.unownedAccDict[self.curAccType][self.curAccIndex[self.curAccType]]
                
                #now update the selected accessory dna element
                curDNA[self.curAccType] = curAcc                
                
                #now set kartviewer dna
                self.kartView.refresh(curDNA)
                
                
                #setup descriptions and cost text
                self.accDescription.configure(text=AccessoryDict[curAcc][KartInfo.name])
                cost = TTLocalizer.KartShop_Cost % (AccessoryDict[curAcc][KartInfo.cost])
                self.accCost = DirectButton(
                           parent = self,
                           relief = None,
                           scale = self.modelScale,
                           text = cost,
                           text_pos = (0,-.40),
                           text_scale = KS_TEXT_SIZE_SMALL,
                           text_fg=(0, 0, 0.0, 1.0 ),
                           pressEffect = False,
                           textMayChange = True,
                           )                
                if AccessoryDict[curAcc][KartInfo.cost] > base.localAvatar.getTickets():
                        self.buyAccessoryButton['state'] = DGG.DISABLED
                        self.buyAccessoryButton.configure(text_scale = KS_TEXT_SIZE_SMALL*.75)
                        self.buyAccessoryButton.configure(text=TTLocalizer.KartShop_NotEnoughTickets)

                        #Put cost in red to indicate you can't buy this
                        self.accCost.configure(text_fg=(0.95, 0, 0.0, 1.0 ))
        
            if len(base.localAvatar.getKartAccessoriesOwned()) >= KartShopGlobals.MAX_KART_ACC:
                #player has too many acc. can't buy more
                self.buyAccessoryButton['state'] = DGG.DISABLED
                self.buyAccessoryButton.configure(text_fg=(0.95, 0, 0.0, 1.0 ))
                self.buyAccessoryButton.configure(text_scale = KS_TEXT_SIZE_SMALL*.8)
                self.buyAccessoryButton.configure(text=TTLocalizer.KartShop_FullTrunk)
                
            #no matter what we do this
            self.kartView.show()
            
            
                 

                        

        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BuyKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:
                    try:
                        self.accDescription.destroy()
                    except:
                        pass #already deleted
                    try:
                        self.kartView.destroy()
                    except:
                        pass #already deleted
                    DirectFrame.destroy( self )
 
 
    class BoughtAccessoryDlg( DirectFrame ):
        """
        Purpose: The BoughtAccessoryDlg confirms to the player that their purchase was
        successful and points them towards the sticker book.
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.BoughtAccessoryDlg" )
        
        def __init__( self, doneEvent, accID ):
                """
                Purpose: The __init__ Method provides the initial construction
                of the BoughtAccessoryDlg by loading appropriate models and textures before
                it constructs the necessary Direct GUI elements.
                params: doneEvent - Event thrown when the Dlg is closed.
                        accID - which accessory the player just bought
                return: None
                """
        
                self.modelScale = 1
                model = loader.loadModel( 'phase_6/models/gui/BoughtAccessoryPanel' )
                accInfo = getAccessoryInfo(accID)
                name = accInfo[AccInfo.name]
                           
                DirectFrame.__init__(
                    self,
                    relief = None,
                    state = 'normal',
                    geom = model,
                    geom_scale = self.modelScale,
                    frameSize = ( -1, 1, -1, 1 ),
                    pos = ( 0, 0, -0.01 ),
                    text = TTLocalizer.KartShop_ConfirmBoughtTitle,
                    text_wordwrap = 26,
                    text_scale = KS_TEXT_SIZE_SMALL,
                    text_pos = ( 0, -0.28 )
                    )
                self.initialiseoptions( KartShopGuiMgr.BoughtAccessoryDlg )
                self.ticketDisplay = DirectLabel(
                        parent = self,
                        relief = None,
                        text = str(base.localAvatar.getTickets()),
                        text_scale = KS_TEXT_SIZE_SMALL,
                        text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                        text_shadow = ( 0, 0, 0, 1 ),
                        text_pos = ( 0.43, -0.5 ),
                        text_font = ToontownGlobals.getSignFont()
                        )
                self.okButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CheckButtonUp' ),
                              model.find( '**/CheckButtonDown' ),
                              model.find( '**/CheckButtonRollover' ) ),
                    geom = model.find( '**/CheckIcon' ),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda : messenger.send( doneEvent, [ BTA_OPTIONS.Ok ] ) )
                    )
                    
                #We just want to show the accessory at this point
                self.kartView = DirectFrame(
                        parent = self,
                        relief = None,
                        geom = model.find( "**/KartViewerFrame" ),
                        scale = 1.0,
                        )
                bounds = self.kartView.getBounds()
                radius =  (bounds[3] - bounds[2])/2
                xCenter = self.kartView.getCenter()[0] 
                cm = CardMaker( "accViewer" )
                    
                #Make it square
                cm.setFrame( xCenter - radius, xCenter + radius, bounds[ 2 ], bounds[ 3 ] )
                self.kartView[ 'geom' ] = NodePath( cm.generate() )
                self.kartView.component( 'geom0' ).setColorScale( 1.0, 1.0, 0.8, 1.0 )
                self.kartView.component( 'geom0' ).setTransparency( True )
                    
                accType = getAccessoryType(accID)
                texNodePath = None
                tex = None      
                    
                if( accType in [ KartDNA.ebType, KartDNA.spType, KartDNA.fwwType, KartDNA.bwwType ] ):
                        texNodePath = getTexCardNode( accID )
                        tex = loader.loadTexture( "phase_6/maps/%s.jpg" % ( texNodePath ),
                                                  "phase_6/maps/%s_a.rgb" % ( texNodePath ) )
                elif( accType == KartDNA.rimsType ):
                        if( accID == InvalidEntry ):
                                # THIS WILL LIKELY NEED TO BE FIXED WHEN NEW RIM
                                # IS ADDED TO COMPENSATE FOR LOSS OF DEFAULT RIM
                                # IN KART SELECTION.
                                texNodePath = getTexCardNode( getDefaultRim() )
                        else:                
                                texNodePath = getTexCardNode( accID )
                        tex = loader.loadTexture( "phase_6/maps/%s.jpg" % ( texNodePath ),
                                                  "phase_6/maps/%s_a.rgb" % ( texNodePath ) )            
                elif( accType in [ KartDNA.bodyColor, KartDNA.accColor ] ):
                        tex = loader.loadTexture( "phase_6/maps/Kartmenu_paintbucket.jpg",
                                                  "phase_6/maps/Kartmenu_paintbucket_a.rgb" )
                        # Obtain the default color if the item is -1, handle this similar to the
                        # rims.
                        if( accID == InvalidEntry ):
                                self.kartView.component( 'geom0' ).setColorScale( getDefaultColor() )
                        else:
                                self.kartView.component( 'geom0' ).setColorScale( getAccessory( accID ) )
                elif( accType == KartDNA.decalType ):
                        #pdir(base.localAvatar)
                        kartDecal = getDecalId( base.localAvatar.getKartBodyType() )
                        texNodePath = getTexCardNode( accID )
                        tex = loader.loadTexture( "phase_6/maps/%s.jpg" % (texNodePath) % ( kartDecal ),
                                                 "phase_6/maps/%s_a.rgb" % (texNodePath) % ( kartDecal ) )
                else:
                        tex = loader.loadTexture( "phase_6/maps/NoAccessoryIcon3.jpg",
                                                  "phase_6/maps/NoAccessoryIcon3_a.rgb" )


                # set the mipmaps
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                
                self.kartView.component( 'geom0' ).setTexture( tex, 1 )

                #model.removeNode()
                self.initialize = True
                
                
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BoughtKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:                     
                DirectFrame.destroy( self )


                
    class ConfirmBuyAccessoryDlg( DirectFrame ):
        """
        Purpose: The ConfirmBuyAccessoryDlg provides the functionality and graphical
        component that allows the player confirm a decision to buy a accessory. 
        """

        ##################################################################
        # Class Variable Definitions
        ##################################################################
        notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopGuiMgr.ConfirmBuyAccessoryDlg" )

        def __init__( self, doneEvent, accID ):
            """
            Purpose: The __init__ Method provides the initial construction
            of the ReturnKartDlg by loading appropriate models and textures before
            it constructs the necessary Direct GUI elements.

            params: doneEvent - Event thrown when the Dlg is closed.
                    accID - ID of accessory that's being bought
            return: None
            """
            #the id of the kart selected for purchase
            self.accID = accID
            self.modelScale = 1
            model = loader.loadModel( 'phase_6/models/gui/ConfirmBuyAccessory' )
            accInfo = getAccessoryInfo(accID)
            cost = accInfo[AccInfo.cost]
            name = accInfo[AccInfo.name]
            DirectFrame.__init__(
                self,
                relief = None,
                state = 'normal',
                geom = model,
                geom_scale = self.modelScale,
                frameSize = ( -1, 1, -1, 1 ),
                pos = ( 0, 0, -0.01 ),
                text = TTLocalizer.KartShop_ConfirmBuy % (name, cost),
                text_wordwrap = 14,
                text_scale = KS_TEXT_SIZE_SMALL,
                text_pos = ( 0, -0.25 )
                )
           
            self.initialiseoptions( KartShopGuiMgr.ConfirmBuyAccessoryDlg )
            self.ticketDisplay = DirectLabel(
                parent = self,
                relief = None,
                text = str(base.localAvatar.getTickets()),
                text_scale = KS_TEXT_SIZE_SMALL,
                text_fg = ( 0.95, 0.95, 0.0, 1.0 ),
                text_shadow = ( 0, 0, 0, 1 ),
                text_pos = ( 0.43, -0.5 ),
                text_font = ToontownGlobals.getSignFont()
            )
            self.cancelButton = DirectButton(
                parent = self,
                relief = None,
                image = ( model.find( '**/CancelButtonUp' ),
                          model.find( '**/CancelButtonDown' ),
                          model.find( '**/CancelButtonRollover' ) ),
                geom = model.find( '**/CancelIcon' ),
                scale = self.modelScale,
                pressEffect = False,
                command = ( lambda : messenger.send( doneEvent, [ CBA_OPTIONS.Cancel ] ) )
                )
            
            self.okButton = DirectButton(
                    parent = self,
                    relief = None,
                    image = ( model.find( '**/CheckButtonUp'),
                          model.find( '**/CheckButtonDown' ),
                          model.find( '**/CheckButtonRollover' ) ),
                    geom = model.find( '**/CheckIcon' ),
                    scale = self.modelScale,
                    pressEffect = False,
                    command = ( lambda: messenger.send(doneEvent, [ CBA_OPTIONS.BuyAccessory ]) ), 
                    )                
            
            #We just want to show the accessory at this point
            self.kartView = DirectFrame(
                parent = self,
                relief = None,
                geom = model.find( "**/KartViewerFrame" ),
                scale = 1.0,
                )
            bounds = self.kartView.getBounds()
            radius =  (bounds[3] - bounds[2])/3
            xCenter, yCenter = self.kartView.getCenter() 
            cm = CardMaker( "accViewer" )
            
            #Make it square
            cm.setFrame( xCenter - radius, xCenter + radius, yCenter - radius, yCenter + radius )
            self.kartView[ 'geom' ] = NodePath( cm.generate() )
            self.kartView.component( 'geom0' ).setColorScale( 1.0, 1.0, 0.8, 1.0 )
            self.kartView.component( 'geom0' ).setTransparency( True )
            
            accType = getAccessoryType(accID)
            texNodePath = None
            tex = None  
            
            if( accType in [ KartDNA.ebType, KartDNA.spType, KartDNA.fwwType, KartDNA.bwwType ] ):
                texNodePath = getTexCardNode( accID )
                tex = loader.loadTexture( "phase_6/maps/%s.jpg" % ( texNodePath ),
                                          "phase_6/maps/%s_a.rgb" % ( texNodePath ) )
            elif( accType == KartDNA.rimsType ):
                if( accID == InvalidEntry ):
                        # THIS WILL LIKELY NEED TO BE FIXED WHEN NEW RIM
                        # IS ADDED TO COMPENSATE FOR LOSS OF DEFAULT RIM
                        # IN KART SELECTION.
                        texNodePath = getTexCardNode( getDefaultRim() )
                else:                
                        texNodePath = getTexCardNode( accID )
                tex = loader.loadTexture( "phase_6/maps/%s.jpg" % ( texNodePath ),
                                          "phase_6/maps/%s_a.rgb" % ( texNodePath ) )            
            elif( accType in [ KartDNA.bodyColor, KartDNA.accColor ] ):
                tex = loader.loadTexture( "phase_6/maps/Kartmenu_paintbucket.jpg",
                                          "phase_6/maps/Kartmenu_paintbucket_a.rgb" )
                # Obtain the default color if the item is -1, handle this similar to the
                # rims.
                if( accID == InvalidEntry ):
                        self.kartView.component( 'geom0' ).setColorScale( getDefaultColor() )
                else:
                        self.kartView.component( 'geom0' ).setColorScale( getAccessory( accID ) )
            elif( accType == KartDNA.decalType ):
                #pdir(base.localAvatar)
                kartDecal = getDecalId( base.localAvatar.getKartBodyType() )
                texNodePath = getTexCardNode( accID )
                tex = loader.loadTexture( "phase_6/maps/%s.jpg" % (texNodePath) % ( kartDecal ),
                                          "phase_6/maps/%s_a.rgb" % (texNodePath) % ( kartDecal ) )
            else:
                tex = loader.loadTexture( "phase_6/maps/NoAccessoryIcon3.jpg",
                                          "phase_6/maps/NoAccessoryIcon3_a.rgb" )

            # set the mipmaps
            tex.setMinfilter(Texture.FTLinearMipmapLinear)

            self.kartView.component( 'geom0' ).setTexture( tex, 1 )
            
            


            self.initialize = True
            
            #model.removeNode()

            
        def destroy( self ):
            """
            Purpose: The destroy Method provides the destruction of the
            BuyKartDlg instance, its base class instance, and all of the
            instantiated UI entities that are managed by the instance.

            params: None
            return: None
            """
            if self.initialize:                    
                   #self.kartView.destroy()
                   DirectFrame.destroy( self )


#================= 
 
    def __init__( self, eventDict ):
        """
        Purpose: The __init__ Method provides the initial construction of
        the KartShopGuiMgr instance.

        params: None
        return: None
        """

        # Provide Main
        self.dialog = None
        self.dialogStack = []
        self.eventDict = eventDict
        self.dialogEventDict = { MENUS.MainMenu      : ("MainMenuGuiDone", self.__handleMainMenuDlg, self.MainMenuDlg),
                                 MENUS.BuyKart       : ("BuyKartGuiDone", self.__handleBuyKartDlg, self.BuyKartDlg),
                                 MENUS.BuyAccessory  : ("BuyAccessoryGuiDone", self.__handleBuyAccessoryDlg, self.BuyAccessoryDlg ),
                                 MENUS.ReturnKart    : ("ReturnKartGuiDone", self.__handleReturnKartDlg, self.ReturnKartDlg),
                                 MENUS.ConfirmBuyKart: ("ConfirmBuyKartGuiDone", self.__handleConfirmBuyKartDlg, self.ConfirmBuyKartDlg),
                                 MENUS.ConfirmBuyAccessory : ("ConfirmBuyAccessoryGuiDone", self.__handleConfirmBuyAccessoryDlg, self.ConfirmBuyAccessoryDlg),
                                 MENUS.BoughtKart    :  ( "BoughtKartGuiDone", self.__handleBoughtKartDlg, self.BoughtKartDlg),
                                 MENUS.BoughtAccessory : ( "BoughtAccessoryGuiDone", self.__handleBoughtAccessoryDlg, self.BoughtAccessoryDlg),
                                 MENUS.TeaserPanel : ( "UnpaidPurchaseAttempt", self.__handleTeaserPanelDlg, TeaserPanel),
                                 
                                 }

        self.kartID = -1
        self.accID = -1
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.accept("RESET_KARTSHOP_TIMER", self.__resetTimer)
        #TODO: Change countdown to kartracer constant
        self.timer.countdown(KartShopGlobals.KARTCLERK_TIMER, self.__timerExpired)
        
        self.__doDialog( MENUS.MainMenu ) 

    def __resetTimer(self):
        if hasattr(self, "timer") and self.timer:
                #self.timer.destroy()
                #self.timer = ToontownTimer.ToontownTimer()
                #self.timer.reparentTo(aspect2d)
                #self.timer.posInTopRightCorner()
                #self.timer.accept("RESET_KARTSHOP_TIMER", self.__resetTimer)
                self.timer.stop()
                self.timer.countdown(KartShopGlobals.KARTCLERK_TIMER, self.__timerExpired)
    
    def __isActive(self, dlgName):
        #if this dlg type is in the current stack then return true
        for d in self.dialogStack:
            if d == dlgName: return True
        return False

    def __timerExpired(self):
        messenger.send(self.eventDict['guiDone'], [True]) 
        
        

    def destroy( self ):
        """
        Purpose: The destroy Method provides the destruction of the
        KartShopGuiMgr instance and all instantiated UI entities that are
        managed by the instance.

        params: None
        return: None
        """

        # Destroy the current Dialog Menu.
        self.__destroyDialog()
        
        # Destroy timer
        self.ignoreAll()
        self.timer.destroy()
        del self.timer

        # Ignore all events
        for event in self.dialogEventDict.values():
            self.ignore( event )

        self.dialogEventDict = None

    def __destroyDialog( self):
        """
        Purpose: The __destroyDialog Method destroys the current dialog
        menu that is available to the player.

        params: None
        return: None
        """
        if hasattr(self, "timer"):
            self.ignoreAll()
        if( self.dialog != None ):
            self.dialog.destroy()
            self.dialog = None


    def __removeDialog(self, dlgName=None ): 
        if( self.dialog != None ):
            if dlgName != None:
                for d in self.dialogStack:
                    if d == dlgName: self.dialogStack.remove(d)
                        
    def __popDialog( self):
        """
        Purpose: The __popDialog Method removes the current Dialog menu
        from the stack and replaces it with the underlying Dialog menu.

        params: None
        return: None
        """
        if( self.dialog != None ):
            if dlgName != None:
                for d in self.dialogStack:
                    if d == dlgName: self.dialogStack.remove(d)
            else:
                d = self.dialogStack.pop()
                #remove listening for this event too
                event = self.dialogEventDict.get( d )
                eventType = event[0]
                self.ignore( eventType )
                if self.dialogStack: #if there's any left
                        self.__doDialog( self.dialogStack[-1] )

        
        
    def __doLastMenu( self ):
            self.__doDialog( self.lastMenu )

    def __doDialog( self, dialogType ):
        """
        Purpose: The __doDialog Method constructs the desired Dialog Menu
        and sets it to be the current Dialog for the KartShopGuiMgr.

        params: dialogType - type of Dialog to generate.
        return: None
        """
        
        # Destroy the current Dialog (it's still in the stack don't forget!)
        self.__destroyDialog()
        
        #push the new dialog type onto
        # the dialog stack.

        #self.dialogStack.append( dialogType )

        # the user has updated the gui, he must be awake
        messenger.send('wakeup')
        
        event = self.dialogEventDict.get( dialogType )
        eventType = event[0]
        eventHandler = event[1]
        eventDlg = event[2]
        self.acceptOnce( eventType, eventHandler )
        if dialogType == MENUS.ConfirmBuyKart:
                self.dialog = eventDlg(eventType, self.kartID)
        elif dialogType == MENUS.BoughtKart:
                self.dialog = eventDlg(eventType, self.kartID)
        elif dialogType == MENUS.ConfirmBuyAccessory:
                self.dialog = eventDlg(eventType, self.accID)
        elif dialogType == MENUS.BoughtAccessory:
                self.dialog = eventDlg(eventType, self.accID)
        elif dialogType == MENUS.TeaserPanel:
                self.dialog = eventDlg(pageName="karting", doneFunc=self.__doLastMenu)  
        else: 
                self.dialog = eventDlg(eventType)

        # Do not reset lastMenu if we are going to the TeaserPanel - it needs to know the last
        if not dialogType == MENUS.TeaserPanel:
                self.lastMenu = dialogType

      
    def __handleMainMenuDlg( self, exitType, args=[] ):
        self.notify.debug( "__handleMainMenuDlg: Handling MainMenu Dialog Selection." )
        if( exitType == MM_OPTIONS.Cancel ):
            messenger.send( self.eventDict[ 'guiDone' ] )
        elif( exitType == MM_OPTIONS.BuyKart ):
            #messenger.send("RESET_KARTSHOP_TIMER")
            self.__doDialog( MENUS.BuyKart )
        elif( exitType == MM_OPTIONS.BuyAccessory ):
            #messenger.send("RESET_KARTSHOP_TIMER")
            self.__doDialog( MENUS.BuyAccessory )


    def __handleBoughtKartDlg(self, exitType):
        """
        """
        self.notify.debug("__handleBoughtKartDlg: Telling the player their purchase was successful")
        #messenger.send("RESET_KARTSHOP_TIMER")
        # add kart page if not here already
        if not hasattr(base.localAvatar, "kartPage"):
            base.localAvatar.addKartPage()
        #reset kart id
        self.kartID = -1
        #really, there's only one exit type here
        #self.__popDialog()
        self.__doDialog( MENUS.MainMenu )
        
    
    def __handleBoughtAccessoryDlg(self, exitType):
        """
        """
        self.notify.debug("__handleBoughtAccessoryDlg: Telling the player their purchase was successful")
        #messenger.send("RESET_KARTSHOP_TIMER")
        #really, there's only one exit type here
        self.accID = -1 
        #self.__popDialog()
        self.__doDialog( MENUS.BuyAccessory )

    def __handleTeaserPanelDlg(self):
        """
        """
        #messenger.send("RESET_KARTSHOP_TIMER")
        self.__doDialog( MENUS.TeaserPanel )
        
    def __handleBuyKartDlg( self, exitType, args=[] ):
        """
        Purpose: The __handleBuyKartDlg Method provides callback functionality
        for handling the BuyKartDlg Menu selections.

        params: exitType - The ChooseKartDlg menu selection.
        return: None
        """
        self.notify.debug( "__handleBuyKartDlg: Handling BuyKart Dialog Selection." )
        #messenger.send("RESET_KARTSHOP_TIMER")
        if( exitType == BK_OPTIONS.Cancel ):
            #self.__popDialog() #pop the buy kart dialog off the stack, leaving main.
            self.__doDialog( MENUS.MainMenu )
        else: #exitType is the id for a Kart # (exitType == BK_OPTIONS.BuyKart):
            #player is buyin the Kart
            #self.__popDialog()
	    self.kartID = exitType
	    if base.localAvatar.hasKart():
	        self.__doDialog(MENUS.ReturnKart)
	    else:
	        self.__doDialog(MENUS.ConfirmBuyKart)
        
    def __handleBuyAccessoryDlg( self, exitType, args=[] ):
        """
        Purpose: The __handleBuyKartDlg Method provides callback functionality
        for handling the BuyKartDlg Menu selections.

        params: exitType - The ChooseKartDlg menu selection.
        return: None
        """
        self.notify.debug( "__handleBuyKartDlg: Handling BuyKart Dialog Selection." )

        if( exitType == BA_OPTIONS.Cancel ):
            #messenger.send("RESET_KARTSHOP_TIMER")
            #self.__popDialog()
            self.__doDialog( MENUS.MainMenu )
            #elif (exitType == BA_OPTIONS.BuyAccessory):
            #player is buyin the accessory
            #self.__popDialog()
            #TODO: add stuff to actually go through with purchase accessory
            #messenger.send(self.eventDict['buyAccessory'], [self.selectedKartID, self.selectedKartNameIndex])
            #messenger.send(self.eventDict['guiDone'])
        else: #exitType is the id for an accessory # (exitType == BK_OPTIONS.BuyKart):
            #player is buyin the Kart    
	    self.accID = exitType
	    self.__doDialog( MENUS.ConfirmBuyAccessory )
            
    def __handleReturnKartDlg( self, exitType, args=[] ):
        """
        Purpose: The __handleReturnKartDlg Method provides callback functionality
        for handling the ReturnKartDlg Menu selections. This is basically just a confirmation
        clickthrough as nothing actually happens unless player buys a new kart to 
        replace the one they returned

        params: exitType - The ReturnKartDlg menu selection.
        return: None
        """
        #messenger.send("RESET_KARTSHOP_TIMER")
        self.notify.debug( "__handleReturnKartDlg: Handling ReturnKart Dialog Selection." )

        if( exitType == RK_OPTIONS.Cancel ):
            self.__doDialog( MENUS.BuyKart)
            #self.__popDialog()
        elif( exitType == RK_OPTIONS.ReturnKart ):
            #returning kart
            #self.__popDialog()
            self.__doDialog( MENUS.ConfirmBuyKart )
            
                

    def __handleConfirmBuyAccessoryDlg( self, exitType, args=[] ):
        """
        Purpose: The __handleConfirmAccessoryKartDlg Method provides callback functionality
        for confirming player purchase of Accessory.

        params: exitType - The ConfirmBuyAccessoryDlg menu selection.
        return: None
        """
        #messenger.send("RESET_KARTSHOP_TIMER")
        self.notify.debug( "__handleConfirmBuyAccessoryDlg: Handling ConfirmBuyAccessory Dialog Selection." )

        if( exitType == CBA_OPTIONS.Cancel ):
            #self.__popDialog()
            #reset kartID
            self.__doDialog( MENUS.BuyAccessory )
            self.accID = -1
        elif( exitType == CBA_OPTIONS.BuyAccessory ):
            #yes buy Accessory
            #self.__popDialog()           
            if (self.accID != -1):
                    messenger.send(self.eventDict['buyAccessory'], [self.accID])
            #messenger.send(self.eventDict['guiDone'])
            #self.__doDialog( MENUS.BoughtAccessory )
            # Deduct tickets locally because gui displays before distributed message makes round trip.
            # The AI will set again to same amount: no harm, no foul.
            oldTickets = base.localAvatar.getTickets()
            accInfo = getAccessoryInfo(self.accID)
            cost = accInfo[AccInfo.cost]
            base.localAvatar.setTickets(oldTickets - cost)

            #also update the loacl toon's owned accessories list
            accList = base.localAvatar.getKartAccessoriesOwned()
            accList.append(self.accID)
            base.localAvatar.setKartAccessoriesOwned(accList)
            
            self.accID = -1     
            #self.__popDialog()
            self.__doDialog( MENUS.BuyAccessory )    
            



    def __handleConfirmBuyKartDlg( self, exitType, args=[] ):
        """
        Purpose: The __handleConfirmBuyKartDlg Method provides callback functionality
        for handling the ReturnKartDlg Menu selections.

        params: exitType - The ConfirmButKartDlg menu selection.
        return: None
        """
        #messenger.send("RESET_KARTSHOP_TIMER")
        self.notify.debug( "__handleConfirmBuyKartDlg: Handling ConfirmBuyKart Dialog Selection." )

        if( exitType == CBK_OPTIONS.Cancel ):
            #self.__popDialog()
            self.__doDialog( MENUS.BuyKart )
            #reset kartID
            self.kartID = -1
        elif( exitType == CBK_OPTIONS.BuyKart ):
            #yes buy kart!
            #self.__popDialog(MENUS.BuyKart)
            #self.__popDialog()       
            if (self.kartID != -1):
                messenger.send(self.eventDict['buyKart'], [self.kartID])
            self.__doDialog( MENUS.BoughtKart )


               
        if __name__ == "__main__":
                class Main( DirectObject.DirectObject ):
                    def __init__( self ):
                        
                        self.acceptOnce( '1', self.__popupKartShopGui )
                        self.accept( KartShopGlobals.EVENTDICT["buyAccessory"], self.__handleBuyAccessory )
                        self.accept( KartShopGlobals.EVENTDICT["buyKart"], self.__handleBuyKart )
                
                    def __popupKartShopGui( self ):
                        if not hasattr(self, 'kartShopGui') or self.kartShopGui == None:
                            self.acceptOnce(  KartShopGlobals.EVENTDICT[ 'guiDone' ], self.__handleGuiDone )
                            self.kartShopGui = KartShopGuiMgr( KartShopGlobals.EVENTDICT )
                
                    def __handleGuiDone( self, args=[] ):
                        if hasattr(self, 'kartShopGui') and self.kartShopGui != None:
                            self.ignoreAll() # self.eventDict[ 'guiDone' ])
                            self.kartShopGui.destroy()
                            del self.kartShopGui
                            self.acceptOnce( '1', self.__popupKartShopGui )
                            
                    def __handleBuyAccessory(self, accID=-1):
                        requestAddOwnedAccessory( self, accID )
                    def __handleBuyKart(self, kartID=-1):        
                        pass
                
                m = Main()
                run()
        
