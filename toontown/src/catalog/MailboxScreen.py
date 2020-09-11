from direct.directnotify.DirectNotifyGlobal import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject, PythonUtil
from pandac.PandaModules import *
from toontown.parties import PartyGlobals
from toontown.parties.InviteInfo import InviteInfoBase
from toontown.parties.PartyGlobals import InviteStatus
from toontown.parties.SimpleMailBase import SimpleMailBase
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toontowngui.TeaserPanel import TeaserPanel
from toontown.parties.InviteVisual import InviteVisual
from toontown.toon import GMUtils
import CatalogItem
from direct.showbase.PythonUtil import StackTrace

class MailboxScreen(DirectObject.DirectObject):
    """

    This class allows the user to accept items one at a time out of
    his or her mailbox.
    
    """
    notify = directNotify.newCategory("MailboxScreen")
    
    def __init__(self, mailbox, avatar, doneEvent = None):
        assert( MailboxScreen.notify.debug("__init__") )
        # This is the DistributedMailbox that is handling our transactions.
        self.mailbox = mailbox
        # This is the avatar we're accepting for.
        self.avatar = avatar
        self.items = self.getItems()
        # Send this when we are done so whoever made us can get a callback
        self.doneEvent = doneEvent

        self.itemIndex = 0
        self.itemPanel = None
        self.itemPicture = None
        self.ival = None
        self.itemText = None
        self.giftTag = None
        self.acceptingIndex = None
        self.numAtticAccepted = 0

        self.dialogBox = None

        self.load()
        self.hide()
        
    def show(self):
        assert( MailboxScreen.notify.debug("show") )
        self.frame.show()
        
        self.__showCurrentItem()

    def hide(self):
        assert( MailboxScreen.notify.debug("hide") )
        self.ignore("friendsListChanged")
        if hasattr(self,'frame'):
            self.frame.hide()
        else:
            self.notify.warning("hide called, but frame is deleted, self.frame deleted in:")
            if hasattr(self, "frameDelStackTrace"):
                print self.frameDelStackTrace
            self.notify.warning("current stackTrace =")
            print StackTrace()
            self.notify.warning("crash averted, but root cause unknown")
            # this will force a crash, hopefully we get the log with it
            #self.frame.hide()

    def load(self):
        assert( MailboxScreen.notify.debug("load") )
        self.accept("setMailboxContents-%s" % (base.localAvatar.doId), self.__refreshItems)
        self.accept("setAwardMailboxContents-%s" % (base.localAvatar.doId), self.__refreshItems)
        # load the buttons
        model = loader.loadModel('phase_5.5/models/gui/package_delivery_panel')

        background = model.find('**/bg')
        itemBoard = model.find('**/item_board')

        self.frame = DirectFrame(scale = 1.1, relief = DGG.FLAT,
                                 frameSize = (-0.5,0.5,-0.45,-0.05),
                                 frameColor = (0.737, 0.573, 0.345, 1.000))
        
        self.background = DirectFrame(self.frame,
                                      image = background,
                                      image_scale = 0.05,
                                      relief = None,
                                      pos = (0,1,0),
                                      )
        self.itemBoard = DirectFrame(parent = self.frame,
                                     image = itemBoard,
                                     image_scale = 0.05,
                                     image_color = (.922, 0.922, 0.753, 1),
                                     relief = None,
                                     pos = (0,1,0),
                                     )
        # shows how many items you have to browse through
        self.itemCountLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            text = self.__getNumberOfItemsText(),
            text_wordwrap = 16,
            pos = (0.0, 0.0, 0.7),
            scale = 0.09,
            )

        exitUp = model.find('**/bu_return_rollover')
        exitDown = model.find('**/bu_return_rollover')
        exitRollover = model.find('**/bu_return_rollover')
        exitUp.setP(-90)
        exitDown.setP(-90)
        exitRollover.setP(-90)
        # click this button to discard/decline an item in your mailbox
        self.DiscardButton = DirectButton(
            parent = self.frame,
            relief = None,
            image = (exitUp, exitDown, exitRollover, exitUp),
            pos = (-0.01, 1.0, -0.36),
            scale = 0.048,
            text = ("", TTLocalizer.MailBoxDiscard,
                    TTLocalizer.MailBoxDiscard, ""),
            text_scale = 1.0,
            text_pos = (0, -0.08),
            textMayChange = 1,            
            command = self.__makeDiscardInterface,
            )
            
        gui2 = loader.loadModel("phase_3/models/gui/quit_button")
        # click this button to stop interacting with the mailbox
        self.quitButton = DirectButton(
            parent = self.frame,
            relief = None,
            image = (gui2.find("**/QuitBtn_UP"),
            gui2.find("**/QuitBtn_DN"),
            gui2.find("**/QuitBtn_RLVR"),
            ),
            pos = (0.5, 1.0, -0.42),
            scale = 0.90,
            text = TTLocalizer.MailboxExitButton,
            text_font = ToontownGlobals.getSignFont(),
            text0_fg = (0.152, 0.750, 0.258, 1),
            text1_fg = (0.152, 0.750, 0.258, 1),
            text2_fg = (0.977, 0.816, 0.133, 1),
            text_scale = 0.045,
            text_pos = (0, -0.01),         
            command = self.__handleExit,
            )

        self.gettingText = DirectLabel(
            parent = self.frame,
            relief = None,
            text = '',
            text_wordwrap = 10,
            pos = (0.0, 0.0, 0.32),
            scale = 0.09,
            )
        self.gettingText.hide()
        
        # label describing who the item is from
        self.giftTagPanel = DirectLabel(
            parent = self.frame,
            relief = None,
            text = 'Gift TAG!!',
            text_wordwrap = 16,
            pos = (0.0, 0.0, 0.01),
            scale = 0.06,
            )
        self.giftTagPanel.hide()
        
        # description of the item. For invites, this might be the body of the
        # invite.
        self.itemText = DirectLabel(
            parent = self.frame,
            relief = None,
            text = '',
            text_wordwrap = 16,
            pos = (0.0, 0.0, -0.022),
            scale = 0.07,
            )
        self.itemText.hide()

        acceptUp = model.find('**/bu_check_up')
        acceptDown = model.find('**/bu_check_down')
        acceptRollover = model.find('**/bu_check_rollover')
        acceptUp.setP(-90)
        acceptDown.setP(-90)
        acceptRollover.setP(-90)
        # click this button to accept an item
        self.acceptButton = DirectButton(
            parent = self.frame,
            relief = None,
            image = (acceptUp, acceptDown, acceptRollover, acceptUp),
            image3_color = (0.8, 0.8, 0.8, 0.6),
            pos = (-0.01, 1.0, -0.16),
            scale = 0.048,
            text = ("", TTLocalizer.MailboxAcceptButton,
                    TTLocalizer.MailboxAcceptButton, ""),
            text_scale = 1.0,
            text_pos = (0, -0.09),
            textMayChange = 1,            
            command = self.__handleAccept,
            state = DGG.DISABLED,
            )

        nextUp = model.find("**/bu_next_up")
        nextUp.setP(-90)
        nextDown = model.find("**/bu_next_down")
        nextDown.setP(-90)
        nextRollover = model.find("**/bu_next_rollover")
        nextRollover.setP(-90)
        # click this button to go to the next item in my mailbox
        self.nextButton = DirectButton(
            parent = self.frame,
            relief = None,
            image = (nextUp, nextDown, nextRollover, nextUp),
            image3_color = (0.8, 0.8, 0.8, 0.6),
            pos = (0.31, 1.0, -0.26),
            scale = 0.05,
            text = ("", TTLocalizer.MailboxItemNext,
                    TTLocalizer.MailboxItemNext, ""),
            text_scale = 1,
            text_pos = (-0.2, 0.3),
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            textMayChange = 0,
            command = self.__nextItem,
            state = DGG.DISABLED,
            )

        prevUp = model.find("**/bu_previous_up")
        prevUp.setP(-90)
        prevDown = model.find("**/bu_previous_down")
        prevDown.setP(-90)
        prevRollover = model.find("**/bu_previous_rollover")
        prevRollover.setP(-90)
        # click this button to go to the previous item in my mailbox
        self.prevButton = DirectButton(
            parent = self.frame,
            relief = None,
            image = (prevUp, prevDown, prevRollover, prevUp),
            pos = (-0.35, 1, -0.26),
            scale = 0.05,
            image3_color = (0.8, 0.8, 0.8, 0.6),
            text = ("", TTLocalizer.MailboxItemPrev,
                    TTLocalizer.MailboxItemPrev, ""),
            text_scale = 1,
            text_pos = (0, 0.3),
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            textMayChange = 0,
            command = self.__prevItem,
            state = DGG.DISABLED,
            )
        self.currentItem=None
        
        self.partyInviteVisual = InviteVisual(self.frame)
        self.partyInviteVisual.setScale(0.73)
        self.partyInviteVisual.setPos(0.0, 0.0, 0.48)
        self.partyInviteVisual.stash()
        
    def unload(self):
        assert( MailboxScreen.notify.debug("unload") )
        self.__clearCurrentItem()
        if hasattr(self,"frame"):
            self.frame.destroy()
            del self.frame
            self.frameDelStackTrace = StackTrace()
        else:
            self.notify.warning("unload, no self.frame")
        if hasattr(self, "mailbox"):
            del self.mailbox
        else:
            self.notify.warning("unload, no self.mailbox")

        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None

        # Clean up all the items also.
        for item in self.items:
            if isinstance(item, CatalogItem.CatalogItem):
                item.acceptItemCleanup()
        
        self.ignoreAll()

    # button handlers
    
    def justExit(self):
        assert( MailboxScreen.notify.debug("justExit") )
        #self.__handleExit()
        self.__acceptExit()
    
    def __handleExit(self):
        assert( MailboxScreen.notify.debug("__handleExit") )
        if self.numAtticAccepted == 0:
            self.__acceptExit()
        elif self.numAtticAccepted == 1:
            self.dialogBox = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = TTLocalizer.CatalogAcceptInAttic,
                text_wordwrap = 15,
                command = self.__acceptExit,
                )
            self.dialogBox.show()
        else:
            self.dialogBox = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = TTLocalizer.CatalogAcceptInAtticP,
                text_wordwrap = 15,
                command = self.__acceptExit,
                )
            self.dialogBox.show()

    def __acceptExit(self, buttonValue = None):
        assert( MailboxScreen.notify.debug("__acceptExit") )
        if hasattr(self, 'frame'):
            self.hide()
            self.unload()
            messenger.send(self.doneEvent)
    
    def __handleAccept(self):
        assert( MailboxScreen.notify.debug("__handleAccept") )
        if self.acceptingIndex != None:
            # Ignore an extraneous click.
            return
        item = self.items[self.itemIndex]
        isAward = False
        if isinstance(item, CatalogItem.CatalogItem):
            isAward = item.isAward()
        if not base.cr.isPaid() and not (isinstance(item, InviteInfoBase) or isAward):
            # make sure free players can accept party invites or awards
            TeaserPanel(pageName='clothing')
        else:
            self.acceptingIndex = self.itemIndex
            self.acceptButton['state'] = DGG.DISABLED

            self.__showCurrentItem()

            item = self.items[self.itemIndex]
            item.acceptItem(self.mailbox, self.acceptingIndex,
                            self.__acceptItemCallback)
                        
    def __handleDiscard(self, buttonValue = None):
        assert( MailboxScreen.notify.debug("__handleDiscard") )
        #print ("Discard Button Value:%s " % (buttonValue)) 

        if self.acceptingIndex != None:
            # Ignore an extraneous click.
            return
        elif buttonValue == -1:
            if self.dialogBox:
                self.dialogBox.cleanup()
            self.dialogBox = None
            self.__showCurrentItem()

        else:
            self.acceptingIndex = self.itemIndex
            self.acceptButton['state'] = DGG.DISABLED

            self.__showCurrentItem()

            item = self.items[self.itemIndex]
            item.discardItem(self.mailbox, self.acceptingIndex,
                self.__discardItemCallback)
            
    def __discardItemCallback(self, retcode, item, index):
        assert( MailboxScreen.notify.debug("__discardItemCallback") )
        if not hasattr(self, "frame"):
            # The gui might have been closed down already by an
            # impatient user.  If so, we quietly ignore the callback.
            return
        if self.dialogBox:
            self.dialogBox.cleanup()
        self.dialogBox = None
        self.acceptingIndex = None
        self.__updateItems()
        if isinstance(item, InviteInfoBase):
            callback = self.__incIndexRemoveDialog
            self.dialogBox = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = item.getDiscardItemErrorText(retcode),
                text_wordwrap = 15,
                command = callback,
                )
            self.dialogBox.show()
        #self.__acceptOk(index)
        
    def __makeDiscardInterface(self):
        assert( MailboxScreen.notify.debug("__makeDiscardInterface") )
        if self.itemIndex >= 0 and self.itemIndex < len(self.items): #check to see if index is within range, should help with button mashing
            item = self.items[self.itemIndex]
            if isinstance(item, InviteInfoBase):
                itemText = (TTLocalizer.MailBoxRejectVerify % (self.getItemName(item)))
                yesText = TTLocalizer.MailboxReject
            else:
                itemText = (TTLocalizer.MailBoxDiscardVerify % (self.getItemName(item)))
                yesText = TTLocalizer.MailboxDiscard
            #self.notify.info("Could not take item %s: retcode %s" % (item, retcode))
            self.dialogBox = TTDialog.TTDialog(
                style = TTDialog.TwoChoiceCustom, #TwoChoice YesNo
                text = itemText, #what happens when you try to take chat from the mailbox
                text_wordwrap = 15,
                command = self.__handleDiscard,
                buttonText = [yesText, TTLocalizer.MailboxLeave],
                )
            self.dialogBox.show()
        
    def __acceptItemCallback(self, retcode, item, index):
        assert( MailboxScreen.notify.debug("__acceptItemCallback") )
        needtoUpdate = 0
        
        if self.acceptingIndex == None:
            needtoUpdate = 1
            #if the setMailboxContents call won the race back here then
            #we need to update our current item list
            
        if not hasattr(self, "frame"):
            # The gui might have been closed down already by an
            # impatient user.  If so, we quietly ignore the callback.
            return
            
        if retcode == ToontownGlobals.P_UserCancelled:
            print("mailbox screen user canceled")
            #user canceled probably for a chatitem
            self.acceptingIndex = None
            self.__updateItems()
            #self.__acceptOk(index+1)
            return

        if self.acceptingIndex != index:
            self.notify.warning("Got unexpected callback for index %s, expected %s." % (index, self.acceptingIndex))
            return
            
        self.acceptingIndex = None
       
        if retcode < 0:
            # There was some error with the accept.  Pop up an
            # appropriate dialog.
            self.notify.info("Could not take item %s: retcode %s" % (item, retcode))
            self.dialogBox = TTDialog.TTDialog(
                style = TTDialog.TwoChoiceCustom, #TwoChoice YesNo
                text = item.getAcceptItemErrorText(retcode), #what happens when you try to take chat from the mailbox
                text_wordwrap = 15,
                command = self.__handleDiscard,
                buttonText = [ TTLocalizer.MailboxDiscard, TTLocalizer.MailboxLeave]
                )
            """
            #buttonText = [TTLocalizer.MailboxOverflowButtonDicard,
            #TTLocalizer.MailboxOverflowButtonLeave]
            """
            #import pdb; pdb.set_trace()
         
            self.dialogBox.show()

        else:
            # The item was accepted successfully.
            if hasattr(item,'storedInAttic') and item.storedInAttic():
                # It's an attic item; collect these messages to
                # display just one dialog box at the end.
                self.numAtticAccepted += 1
                self.itemIndex += 1
                #self.__acceptOk(index)
                if needtoUpdate == 1:
                    self.__updateItems();

            else:
                # It's some other kind of item; display the accept
                # dialog immediately.
                #callback = PythonUtil.Functor(self.__acceptOk, index)
                
                # TODO force it to just discard the item when appropriate
                # e.g. invites to cancelled parties
                if isinstance(item, InviteInfoBase):
                    self.__updateItems();                  
                callback = self.__incIndexRemoveDialog
                # tell player that the party's host got their response
                self.dialogBox = TTDialog.TTDialog(
                    style = TTDialog.Acknowledge,
                    text = item.getAcceptItemErrorText(retcode),
                    text_wordwrap = 15,
                    command = callback,
                    )
                self.dialogBox.show()
                                  
                
    def __acceptError(self, buttonValue = None):
        assert( MailboxScreen.notify.debug("__acceptError") )
        self.dialogBox.cleanup()
        self.dialogBox = None
        self.__showCurrentItem()
        
    def __incIndexRemoveDialog(self, junk = 0):
        assert( MailboxScreen.notify.debug("__incIndexRemoveDialog") )
        self.__incIndex()
        self.dialogBox.cleanup()
        self.dialogBox = None
        self.__showCurrentItem()

    def __incIndex(self, junk = 0):
        assert( MailboxScreen.notify.debug("__incIndex") )
        self.itemIndex += 1

    def __acceptOk(self, index, buttonValue = None):
        assert( MailboxScreen.notify.debug("__acceptOk") )
        self.acceptingIndex = None
        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None

        # We have a new set of items now.
        self.items = self.getItems() 
        if self.itemIndex > index or self.itemIndex >= len(self.items):
            print("adjusting item index -1")
            self.itemIndex -= 1

        if len(self.items) < 1:
            #print("exiting due to lack of items")
            # No more items in the mailbox.
            self.__handleExit()
            return

        # Show the next item in the mailbox.
        self.itemCountLabel['text'] = self.__getNumberOfItemsText(),
        self.__showCurrentItem()
        
    def __refreshItems(self):
        assert( MailboxScreen.notify.debug("__refreshItems") )
        self.acceptingIndex = None
        self.__updateItems()
        
    def __updateItems(self):
        assert( MailboxScreen.notify.debug("__updateItems") )
        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None
            
        # We have a new set of items now.
        self.items = self.getItems()
        if self.itemIndex >= len(self.items):
            print("adjusting item index -1")
            self.itemIndex = len(self.items) - 1

        if len(self.items) == 0:
            print("exiting due to lack of items")
            # No more items in the mailbox.
            self.__handleExit()
            return

        # Show the current item in the mailbox.
        self.itemCountLabel['text'] = self.__getNumberOfItemsText(),
        self.__showCurrentItem()

    def __getNumberOfItemsText(self):
        assert( MailboxScreen.notify.debug("__getNumberOfItemsText") )
        # Returns the string displayed across the top of the panel:
        # how many items remain in the mailbox.
        if len(self.items) == 1:
            return TTLocalizer.MailboxOneItem
        else:
            return TTLocalizer.MailboxNumberOfItems % (len(self.items))

    def __clearCurrentItem(self):
        assert( MailboxScreen.notify.debug("__clearCurrentItem") )
        if self.itemPanel:
            self.itemPanel.destroy()
            self.itemPanel = None
        if self.ival:
            self.ival.finish()
            self.ival = None
        if not self.gettingText.isEmpty():
            self.gettingText.hide()
        if not self.itemText.isEmpty():
            self.itemText.hide()
        if not self.giftTagPanel.isEmpty():
            self.giftTagPanel.hide()
        if not self.acceptButton.isEmpty():
            self.acceptButton['state'] = DGG.DISABLED
        if(self.currentItem):
            if isinstance(self.currentItem, CatalogItem.CatalogItem):
                self.currentItem.cleanupPicture()
            self.currentItem = None
                    
    def checkFamily(self, doId):
        assert( MailboxScreen.notify.debug("checkFamily") )
        for familyMember in base.cr.avList:
            #print ("Family %s %s" % (familyMember.name, familyMember.id))
            if familyMember.id == doId:
                #print("found it")
                #import pdb; pdb.set_trace()
                return familyMember
        return None
                
    def __showCurrentItem(self):
        assert( MailboxScreen.notify.debug("__showCurrentItem") )
        self.__clearCurrentItem()
        if len(self.items) < 1:
            # No more items in the mailbox.
            self.__handleExit()
            return
        self.partyInviteVisual.stash()
        if (self.itemIndex + 1) > len(self.items):
            self.itemIndex = len(self.items) - 1
            
        item = self.items[self.itemIndex]

        if self.itemIndex == self.acceptingIndex:
            # We are currently waiting on the AI to accept this item.
            self.gettingText['text'] = TTLocalizer.MailboxGettingItem % (self.getItemName(item))
            self.gettingText.show()
            return

        # This item is available to be accepted.
        self.itemText['text'] = self.getItemName(item)
        assert(self.itemPanel == None and self.ival == None)
        self.currentItem=item
        # giftTag is the senders do Id
        # giftCode is the type of tag to use (added after giftTag or I would have named them differently)
        if isinstance(item, CatalogItem.CatalogItem):
            self.acceptButton['text'] = ("", TTLocalizer.MailboxAcceptButton,
                    TTLocalizer.MailboxAcceptButton, "")
            self.DiscardButton['text'] = ("", TTLocalizer.MailBoxDiscard,
                    TTLocalizer.MailBoxDiscard, "")
            if item.isAward():
                self.giftTagPanel['text'] = TTLocalizer.SpecialEventMailboxStrings[item.specialEventId]
            elif item.giftTag != None:
                # if it's a gift add the tag
                nameOfSender = self.getSenderName(item.giftTag)

                if item.giftCode == ToontownGlobals.GIFT_RAT:
                    self.giftTagPanel['text'] = TTLocalizer.CatalogAcceptRATBeans
                else:
                    self.giftTagPanel['text'] = (TTLocalizer.MailboxGiftTag % (nameOfSender))
            
            else:
                self.giftTagPanel['text'] = ""
            self.itemPanel, self.ival = item.getPicture(base.localAvatar)
        elif isinstance(item, SimpleMailBase):
            self.acceptButton['text'] = ("", TTLocalizer.MailboxAcceptButton,
                    TTLocalizer.MailboxAcceptButton, "")
            self.DiscardButton['text'] = ("", TTLocalizer.MailBoxDiscard,
                    TTLocalizer.MailBoxDiscard, "")             
            senderId = item.senderId
            nameOfSender = self.getSenderName(senderId)
            self.giftTagPanel['text'] = (TTLocalizer.MailFromTag % (nameOfSender))
            self.itemText['text'] = item.body
        elif isinstance(item, InviteInfoBase):
            self.acceptButton['text'] = ("", TTLocalizer.MailboxAcceptInvite,
                    TTLocalizer.MailboxAcceptInvite, "")
            self.DiscardButton['text'] = ("", TTLocalizer.MailBoxRejectInvite,
                    TTLocalizer.MailBoxRejectInvite, "") 
            partyInfo = None
            for party in self.avatar.partiesInvitedTo:
                if party.partyId == item.partyId:
                    partyInfo = party
                    break
            else: # could not find party info
                MailboxScreen.notify.error("Unable to find party with id %d to match invitation %s"%(item.partyId, item))
            if self.mailbox:
                if item.status == PartyGlobals.InviteStatus.NotRead:
                    self.mailbox.sendInviteReadButNotReplied(item.inviteKey)
            senderId = partyInfo.hostId
            nameOfSender = self.getSenderName(senderId)
            self.giftTagPanel['text'] = ""
            self.itemText['text'] = ""
            self.partyInviteVisual.updateInvitation(nameOfSender, partyInfo)
            self.partyInviteVisual.unstash()
            self.itemPanel = None
            self.ival = None
        else:
            self.acceptButton['text'] = ("", TTLocalizer.MailboxAcceptButton,
                    TTLocalizer.MailboxAcceptButton, "")
            self.DiscardButton['text'] = ("", TTLocalizer.MailBoxDiscard,
                    TTLocalizer.MailBoxDiscard, "")  
            self.giftTagPanel['text'] = " "
            self.itemPanel = None
            self.ival = None
        self.itemText.show()
        self.giftTagPanel.show()
        
        if self.itemPanel and (item.getTypeName() != TTLocalizer.ChatTypeName):
            # Ensure the item panel is behind any other text.
            self.itemPanel.reparentTo(self.itemBoard, -1)
            self.itemPanel.setPos(0, 0, 0.40)
            self.itemPanel.setScale(0.21)
            self.itemText['text_wordwrap'] = 16
            self.itemText.setPos(0.0, 0.0, 0.075)
        elif isinstance(item, CatalogItem.CatalogItem) and \
             (item.getTypeName() == TTLocalizer.ChatTypeName):
            # Ensure the item panel is behind any other text.
            self.itemPanel.reparentTo(self.itemBoard, -1)
            self.itemPanel.setPos(0, 0, 0.35)
            self.itemPanel.setScale(0.21)
             # Scooch the item text into the chat bubble
            self.itemText['text_wordwrap'] = 10
            self.itemText.setPos(0, 0, 0.30)
        else:
            # There's no picture for this item.  Scooch the item text
            # up to fill up the space.
            self.itemText.setPos(0, 0, 0.3)

        if self.ival:
            self.ival.loop()
        if self.acceptingIndex == None:
            self.acceptButton['state'] = DGG.NORMAL

        if self.itemIndex > 0:
            self.prevButton['state'] = DGG.NORMAL
        else:
            self.prevButton['state'] = DGG.DISABLED

        if self.itemIndex + 1 < len(self.items):
            self.nextButton['state'] = DGG.NORMAL
        else:
            self.nextButton['state'] = DGG.DISABLED

            
    def __nextItem(self):
        assert( MailboxScreen.notify.debug("__nextItem") )
        messenger.send('wakeup')
        if self.itemIndex + 1 < len(self.items):
            self.itemIndex += 1
            self.__showCurrentItem()
            
    def __prevItem(self):
        assert( MailboxScreen.notify.debug("__prevItem") )
        messenger.send('wakeup')
        if self.itemIndex > 0:
            self.itemIndex -= 1
            self.__showCurrentItem()
            
    def getItemName(self, item):
        """Return the name of the item."""
        assert( MailboxScreen.notify.debug("getItemName") )
        if isinstance(item, CatalogItem.CatalogItem):
            return item.getName()
        elif isinstance(item, str):
            return TTLocalizer.MailSimpleMail
        elif isinstance(item, InviteInfoBase):
            return TTLocalizer.InviteInvitation
        else:
            return ''
        
    def getItems(self):
        """Return the mailbox items which can be of multiple types."""
        assert( MailboxScreen.notify.debug("getItems") )
        result = []
        result = self.avatar.awardMailboxContents[:]
        result += self.avatar.mailboxContents[:]
        if self.avatar.mail:
            result += self.avatar.mail
        mailboxInvites = self.avatar.getInvitesToShowInMailbox()
        if mailboxInvites:
            result += mailboxInvites
        return result


    def getNumberOfAwardItems(self):
        """Return the number of award items in self.items."""
        # since award items go first, the index being sent to ai needs to be adjusted
        result = 0
        for item in self.items:
            if isinstance(item, CatalogItem.CatalogItem) and item.specialEventId > 0:
                result += 1
            else:
                break
        return result
            

    def getSenderName(self,avId):
        """Return the name of the toon that matches avId."""
        assert( MailboxScreen.notify.debug("getSenderName") )
        sender = base.cr.identifyFriend(avId)
        nameOfSender = ""
        if sender:
            nameOfSender = sender.getName()
        else:
            sender = self.checkFamily(avId) # check family
            if sender: 
                nameOfSender = sender.name # careful a family member returns a PotentialAvatar not a handle
            elif hasattr(base.cr, "playerFriendsManager"): # check transient toons
                sender = base.cr.playerFriendsManager.getAvHandleFromId(avId)
                if sender: 
                    nameOfSender = sender.getName()
                    
        if GMUtils.testGMIdentity(nameOfSender):
            nameOfSender = GMUtils.handleGMName(nameOfSender)

        if not sender:
            nameOfSender = TTLocalizer.MailboxGiftTagAnonymous
            if hasattr(base.cr, "playerFriendsManager"): # request the info
                base.cr.playerFriendsManager.requestAvatarInfo(avId)
                self.accept('friendsListChanged', self.__showCurrentItem) # accepts this as long as it stays up
        return nameOfSender

    

