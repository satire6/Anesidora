class SingleReply:
    """
    Python friendly representation of a single replyt to a party you're hosting.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """

    def __init__(self, inviteeId, status):
        """Construct the single reply."""
        self.inviteeId = inviteeId
        self.status = status

class PartyReplyInfoBase:
    """
    Python friendly representation of the replies for one party you're hosting.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    def __init__(self, partyId, partyReplies):
        """Construct the party info."""
        self.partyId = partyId
        self.replies = []
        for oneReply in partyReplies:
            self.replies.append( SingleReply(*oneReply))


    def __str__(self):
        """Return a useful string representation of this object."""
        string = "partyId=%d " % self.partyId
        for reply in self.replies:
            string+= "(%d:%d) " % (reply.inviteeId, reply.status)
        return string
