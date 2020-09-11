from direct.directnotify import DirectNotifyGlobal

from toontown.toonbase import ToontownGlobals
from toontown.parties.PartyGlobals import InviteStatus
from toontown.toonbase import TTLocalizer

class InviteInfoBase:
    """
    Python friendly representation of a single invite a toon got.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    def __init__(self, inviteKey, partyId, status):
        """Construct the party info."""
        self.inviteKey = inviteKey
        self.partyId = partyId
        self.status = status

    def __str__(self):
        """Return a useful string representation of this object."""
        string = "inviteKey=%d " % self.inviteKey
        string += "partyId=%d " % self.partyId
        string += "status=%s" % InviteStatus.getString(self.status)
        return string

    def __repr__(self):
        """Return a string used in debugging."""
        return self.__str__()    

class InviteInfo(InviteInfoBase):
    """Client side representation of an invite.  It accesses objects such
    as localAvatar and DistributedMailbox.  In particular it handles
    the local toon accepting or rejecting an invite."""

    notify = DirectNotifyGlobal.directNotify.newCategory("InviteInfo")

    def __init__(self, inviteKey, partyId, status):
        """Construct ourself."""
        InviteInfoBase.__init__(self, inviteKey, partyId, status)

    def acceptItem(self, mailbox, acceptingIndex, callback):
        """Handle the player clicking on accept.

        Note that acceptingIndex is an index of to all the items in the
        mailbox, which includes catalog items and simple mail.
        """
        InviteInfo.notify.debug("acceptItem")
        # stolen from CatalogItem.py
        # Accepts the item from the mailbox.  Some items will pop up a
        # dialog querying the user for more information before
        # accepting the item; other items will accept it immediately.

        # In either case, the function will return immediately before
        # the transaction is finished, but the given callback will be
        # called later with three parameters: the return code (one of
        # the P_* symbols defined in ToontownGlobals.py), followed by
        # the item itself, and the supplied index number.

        # The index is the position of this item within the avatar's
        # mailboxContents list, which is used by the AI to know which
        # item to remove from the list (and also to doublecheck that
        # we're accepting the expected item).

        # This method is only called on the client.
        mailbox.acceptInvite(self,  acceptingIndex, callback)        
        
    def discardItem(self, mailbox, acceptingIndex, callback):
        """Reject an invite from the mailbox."""
        InviteInfo.notify.debug("discardItem")
        mailbox.rejectInvite(self,  acceptingIndex, callback)

    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        InviteInfo.notify.debug("getAcceptItemErrorText")
        if retcode == ToontownGlobals.P_InvalidIndex:
            return TTLocalizer.InviteAcceptInvalidError
        elif retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.InviteAcceptAllOk        
        else:
            return TTLocalizer.CatalogAcceptGeneralError % (retcode)

    def getDiscardItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        InviteInfo.notify.debug("getDiscardItemErrorText")
        if retcode == ToontownGlobals.P_InvalidIndex:
            return TTLocalizer.InviteAcceptInvalidError
        elif retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.InviteRejectAllOk        
        else:
            return TTLocalizer.CatalogAcceptGeneralError % (retcode)

    def output(self, store = ~0):
        return "InviteInfo %s" % ( str(self))    

