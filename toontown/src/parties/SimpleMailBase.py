class SimpleMailBase:
    """
    Python friendly representation of a simple mail a toon got.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    def __init__(self, msgId, senderId, year, month, day, body):
        """Construct the party info."""
        self.msgId = msgId
        self.senderId = senderId
        self.year = year
        self.month = month
        self.day = day
        self.body = body

    def __str__(self):
        """Return a useful string representation of this object."""
        string = "msgId=%d " % self.msgId
        string += "senderId=%d " % self.senderId
        string += "sent=%s-%s-%s " % (self.year, self.month, self.day)
        string += "body=%s" % self.body
        return string
