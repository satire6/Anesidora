
class ActivityBase:
    """
    Python friendly representation of an activity.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    def __init__(self, activityId, x, y ,h):
        """Construct the activity info."""
        self.activityId = activityId # see PartyGlobals.py for a list of activity ID's
        self.x = x # int value for the x coordinate on the party grounds grid
        self.y = y # int value for the y coordinate on the party grounds grid
        self.h = h # int value representing the activity's heading in party grid space

    def __str__(self):
        """Return a useful string representation of this object."""
        string = "<ActivityBase activityId=%d, " % self.activityId
        string += "x=%d, y=%d, h=%d>" % (self.x,self.y, self.h)
        return string

    def __repr__(self):
        """Return a string used in debugging."""        
        return self.__str__()
