from pandac.PandaModules import *
import CatalogItem
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer

# Scandalous phrases not appropriate to toontown
bannedPhrases = [ 11009 ]

class CatalogChatItem(CatalogItem.CatalogItem):
    """CatalogChatItem

    This represents a particular custom menu item in the SpeedChat
    that a player may purchase.

    """
    
    def makeNewItem(self, customIndex):
        self.customIndex = customIndex
        
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 1

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        #assert avatar.onGiftOrder, "on gift order is None"
        #print avatar.onGiftOrder
        #print "self in onGiftOrder: %s" % (self in avatar.onGiftOrder)
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder \
           or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:        
            return 1
        #if avatar != localAvatar:
            #pass
            #import pdb; pdb.set_trace()   
        return avatar.customMessages.count(self.customIndex) != 0

    def getTypeName(self):
        return TTLocalizer.ChatTypeName

    def getName(self):
        return TTLocalizer.ChatItemQuotes % OTPLocalizer.CustomSCStrings[self.customIndex]

    def getDisplayName(self):
        return OTPLocalizer.CustomSCStrings[self.customIndex]

    def recordPurchase(self, avatar, optional):
        if avatar.customMessages.count(self.customIndex) != 0:
            # We already have this chat item.
            return ToontownGlobals.P_ReachedPurchaseLimit
        
        if len(avatar.customMessages) >= ToontownGlobals.MaxCustomMessages:
            # Oops, too many custom messages.
            
            # Delete the old index if so requested by the client.
            if optional >= 0 and optional < len(avatar.customMessages):
                del avatar.customMessages[optional]

            if len(avatar.customMessages) >= ToontownGlobals.MaxCustomMessages:
                # Still too many.
                return ToontownGlobals.P_NoRoomForItem
                
        avatar.customMessages.append(self.customIndex)
        avatar.d_setCustomMessages(avatar.customMessages)
        return ToontownGlobals.P_ItemAvailable
        
    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptChat
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def output(self, store = ~0):
        return "CatalogChatItem(%s%s)" % (
            self.customIndex,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.customIndex - other.customIndex

    def getHashContents(self):
        return self.customIndex

    def getBasePrice(self):
        # Special holiday-themed chat phrases (>= 10000) are a bit
        # more expensive.
        if self.customIndex >= 10000:
            return 150

        return 100

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.customIndex = di.getUint16()

        # The following will generate an exception if self.customIndex
        # is wrong.
        text = OTPLocalizer.CustomSCStrings[self.customIndex]

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.customIndex)
        
    def acceptItem(self, mailbox, index, callback):
        # Accepts the item from the mailbox.  Some items will pop up a
        # dialog querying the user for more information before
        # accepting the item; other items will accept it immediately.
    
        # This method is only called on the client.
        if (len(base.localAvatar.customMessages) < ToontownGlobals.MaxCustomMessages):
            mailbox.acceptItem(self, index, callback)
        else:
            # else make them make a choice
            self.showMessagePickerOnAccept(mailbox, index, callback)
        

    def requestPurchase(self, phone, callback):
        # make sure we have room for this in the chat menu
        if (len(base.localAvatar.customMessages) < ToontownGlobals.MaxCustomMessages):
            # if so request the purchase
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)
        else:
            # else make them make a choice
            self.showMessagePicker(phone, callback)
            
    def showMessagePicker(self, phone, callback):
        # we will need these later
        self.phone = phone
        self.callback = callback
        # pop up a toontown dialog with message picker
        import CatalogChatItemPicker
        self.messagePicker = CatalogChatItemPicker.CatalogChatItemPicker(self.__handlePickerDone,
                                                                         self.customIndex)
        self.messagePicker.show()
        

    def showMessagePickerOnAccept(self, mailbox, index, callback):
        # we will need these later
        self.mailbox = mailbox
        self.callback = callback
        self.index = index
        # pop up a toontown dialog with message picker
        import CatalogChatItemPicker
        self.messagePicker = CatalogChatItemPicker.CatalogChatItemPicker(self.__handlePickerOnAccept,
                                                                         self.customIndex)
        self.messagePicker.show()
        
    def __handlePickerOnAccept(self, status, pickedMessage=None):
        print("Picker Status%s" % (status))
        if (status == "pick"):
            # user has deleted custom phrase, so add this one now
            self.mailbox.acceptItem(self, self.index, self.callback, pickedMessage)
        else:
            print("picker canceled")
            self.callback(ToontownGlobals.P_UserCancelled, None, self.index)
            
        self.messagePicker.hide()
        self.messagePicker.destroy()
        del self.messagePicker
        del self.callback
        del self.mailbox


    def __handlePickerDone(self, status, pickedMessage=None):
        if (status == "pick"):
            # user has deleted custom phrase, so add this one now
            CatalogItem.CatalogItem.requestPurchase(self,
                                                    self.phone,
                                                    self.callback,
                                                    pickedMessage)
        self.messagePicker.hide()
        self.messagePicker.destroy()
        del self.messagePicker
        del self.callback
        del self.phone

    def getPicture(self, avatar):
        chatBalloon = loader.loadModel("phase_3/models/props/chatbox.bam")
        chatBalloon.find("**/top").setPos(1,0,5)
        chatBalloon.find("**/middle").setScale(1,1,3)
        frame = self.makeFrame()
        chatBalloon.reparentTo(frame)

        #chatBalloon.setPos(-1.92,0,-1.53)
        chatBalloon.setPos(-2.19,0,-1.74)
        chatBalloon.setScale(0.4)
        
        #bMin, bMax = chatBalloon.getTightBounds()
        #center = (bMin + bMax)/2.0
        #chatBalloon.setPos(-center[0], -center[1], -center[2])
        #corner = Vec3(bMax - center)
        #print bMin, bMax, center, corner
        #chatBalloon.setScale(1.0/corner[2])

        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)
        
        # nametag = NametagGroup()
        # nametag.setFont(ToontownGlobals.getInterfaceFont())
        # nametag.manage(base.marginManager)
        # nametag.setActive(1)
        # nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        # chatString = TTLocalizer.ChatItemQuotes % (OTPLocalizer.CustomSCStrings[self.customIndex])
        # nametag.setChat(chatString, CFSpeech)
        # nametagNodePath = NodePath(nametag.getNametag3d().upcastToPandaNode())
        # return self.makeFrameModel(nametagNodePath, spin=0)



def getChatRange(fromIndex, toIndex, *otherRanges):
    # This function returns a list of the chat items within the
    # indicated range(s).

    # Make sure we got an even number of otherRanges
    assert(len(otherRanges)%2 == 0)

    list = []

    froms = [fromIndex,]
    tos = [toIndex,]

    i = 0
    while i < len(otherRanges):
        froms.append(otherRanges[i])
        tos.append(otherRanges[i+1])
        i += 2
    
    for chatId in OTPLocalizer.CustomSCStrings.keys():
        for fromIndex, toIndex in zip(froms, tos):
            if chatId >= fromIndex and chatId <= toIndex and (chatId not in bannedPhrases):
                list.append(CatalogChatItem(chatId))
                
    return list
