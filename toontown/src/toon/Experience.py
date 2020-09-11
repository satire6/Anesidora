### Experience module: contains the Experience class"""

from pandac.PandaModules import *
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.otpbase import OTPGlobals

class Experience:

    notify = DirectNotifyGlobal.directNotify.newCategory('Experience')

    # special methods
    
    def __init__(self, expStr=None, owner=None):
        """__init__(self, netString=None)
        Create a default experience if no netString given, or
        create an experience from the given netString
        """
        self.owner = owner
        if (expStr == None):
            # create default level one inv
            self.experience = []
            for track in range(0, len(Tracks)):
                self.experience.append(StartingLevel)
        else:
            # de-stringify the one that came in
            self.experience = self.makeFromNetString(expStr)

    def __str__(self):
        """__str__(self)
        Experience print function
        """
        return str(self.experience)
        
    def makeNetString(self):
        """makeNetString(self)
        Make a network packet out of the experience
        """
        dataList = self.experience
        datagram = PyDatagram()
        for track in range(0, len(Tracks)):
            datagram.addUint16(dataList[track])
        dgi = PyDatagramIterator(datagram)
        return dgi.getRemainingBytes()
        
    def makeFromNetString(self, netString):
        """makeFromNetString(self)
        Make an experience from a network packet
        """
        dataList = []
        dg = PyDatagram(netString)
        dgi = PyDatagramIterator(dg)
        for track in range(0, len(Tracks)):
            dataList.append(dgi.getUint16())
        return dataList


    # setters and getters

    def addExp(self, track, amount=1):                        
        """addExp(self, [int | string], int=1)
        Add 'amount' (defaults to 1) of experience to the given track.
        Track may be specified by an index (ie Tracks[index]) or
        by string (ie 'drop')
        """
        # if string, convert to index
        if (type(track) == type('')):
            track = Tracks.index(track)

        self.notify.debug("adding %d exp to track %d" % (amount, track))
        if self.owner.getGameAccess() == OTPGlobals.AccessFull:
            if (self.experience[track] + amount <= MaxSkill):
                self.experience[track] += amount
            else:
                self.experience[track] = MaxSkill
        else:
            if (self.experience[track] + amount <= UnpaidMaxSkill):
                self.experience[track] += amount
            else:
                if  self.experience[track] > UnpaidMaxSkill:
                    self.experience[track] += 0 #remain unchanged
                else:
                    self.experience[track] = UnpaidMaxSkill
        
    def maxOutExp(self):
        """maxOutExp(self):
        Set all experience fields to MaxSkill
        """
        for track in range(0, len(Tracks)):
            self.experience[track] = MaxSkill - UberSkill

    def maxOutExpMinusOne(self):
        """maxOutExp(self):
        Set all experience fields to MaxSkill
        """
        for track in range(0, len(Tracks)):
            self.experience[track] = MaxSkill - 1
            
    def makeExpHigh(self):
        for track in range(0, len(Tracks)):
            self.experience[track] = Levels[track][len(Levels[track]) - 1] - 1
            
    def makeExpRegular(self):
        import random
        for track in range(0, len(Tracks)):
            rank = random.choice((0,int(random.random() * 1500.0),int(random.random() * 2000.0)))
            self.experience[track] = Levels[track][len(Levels[track]) - 1] - rank

    def zeroOutExp(self):
        """zeroOutExp(self):
        Set all experience fields to StartingLevel
        """
        for track in range(0, len(Tracks)):
            self.experience[track] = StartingLevel

    def setAllExp(self, num):
        """
        Sets all the exp to the same number.
        This is for debugging.
        """
        for track in range(0, len(Tracks)):
            self.experience[track] = num
        
    def getExp(self, track):
        """getExp(self, [int | string])
        Return the raw experience of the given track.
        Track may be specified by an index (ie Tracks[index]) or
        by string (ie 'drop')
        """
        # if string, convert to index
        if (type(track) == type('')):
            track = Tracks.index(track)

        return self.experience[track]
        
    def setExp(self, track, exp):
        """setExp(self, [int | string])
        Sets the raw experience of the given track.
        Track may be specified by an index (ie Tracks[index]) or
        by string (ie 'drop')
        """
        # if string, convert to index
        if (type(track) == type('')):
            track = Tracks.index(track)

        self.experience[track] = exp

    def getExpLevel(self, track):
        """getExpLevel(self, [int | string])
        Return the experience level (1-6) of the given track.
        Track may be specified by an index (ie Tracks[index]) or
        by string (ie 'drop')
        """
        # if string, convert to index
        if (type(track) == type('')):
            track = Tracks.index(track)

        level = 0
        for amount in Levels[track]:
            if (self.experience[track] >= amount):
                level = Levels[track].index(amount)

        return level
            
    def getTotalExp(self):
        total = 0
        for level in self.experience:
            total += level
        return total
            
    def getNextExpValue(self, track, curSkill=None):
        """
        Return the number of total experience to get to the next
        track. If the current experience equals or exceeds the highest
        next value, the highest next value is returned.
        """
        if curSkill == None:
            curSkill = self.experience[track]
        # The last value is the default
        retVal = Levels[track][len(Levels[track]) - 1]
        for amount in Levels[track]:
            if curSkill < amount:
                retVal = amount
                return retVal
        return retVal

    def getNewGagIndexList(self, track, extraSkill):
        """
        Returns a list of indices of new gags that have been earned
        During this battle. It is hard to imagine that the list will
        be longer than one item, but it might be theoretically possible one day.
        """
        retList = []
        curSkill = self.experience[track]
        nextExpValue = self.getNextExpValue(track, curSkill)
        finalGagFlag = 0
        while ((curSkill + extraSkill >= nextExpValue) and
               (curSkill < nextExpValue) and
               (not finalGagFlag)):
            retList.append(Levels[track].index(nextExpValue))
            newNextExpValue = self.getNextExpValue(track, nextExpValue)
            if newNextExpValue == nextExpValue:
                finalGagFlag = 1
            else:
                nextExpValue = newNextExpValue
        return retList
        



