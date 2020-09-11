
class DecorBase:
    """
    Python friendly representation of a decoration.
    For now just straight up conversions of values we get from the database
    Make sure this class can be used on the AI side
    """
    def __init__(self, decorId, x, y ,h):
        """Construct the activity info."""
        self.decorId = decorId
        self.x = x
        self.y = y
        self.h = h

    def __str__(self):
        """Return a useful string representation of this object."""
        string = "decorId=%d " % self.decorId
        string += "(%d,%d,%d) " % (self.x,self.y, self.h)
        return string

    def __repr__(self):
        """Return a string used in debugging."""        
        return self.__str__()
