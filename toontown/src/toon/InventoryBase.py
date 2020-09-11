### InventoryBase module: contains the InventoryBase class"""

from pandac.PandaModules import *
from toontown.toonbase.ToontownBattleGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class InventoryBase(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("InventoryBase")

    # special methods
    def __init__(self, toon, invStr=None):
        """__init__(self, toon, netString=None)
        Create a default inv if no netString given, or
        create an inv from the given netString. We need the
        experience object of the toon to determine max number
        of an item and the maxHp to determine the total number
        of items. We get these both from the toon.
        """
        self.toon = toon
        # check to see if config overrides exp
        if (invStr == None):
            # create default lvl one inv
            self.inventory = []
            for track in range(0, len(Tracks)):
                level = []
                for thisLevel in range(0, len(Levels[track])):
                    level.append(0)
                self.inventory.append(level)
        else:
            # de-stringify the one that came in
            self.inventory = self.makeFromNetString(invStr)
            
        self.calcTotalProps()

    def unload(self):
        del self.toon

    def __str__(self):
        """__str__(self):
        Inventory print function
        """
        retStr = 'totalProps: %d\n' % (self.totalProps)
        for track in range(0, len(Tracks)):
            retStr += Tracks[track] + " = " + \
                      str(self.inventory[track]) + "\n"
        return retStr

    def updateInvString(self, invString):
        inventory = self.makeFromNetString(invString)
        self.updateInventory(inventory)
        return None

    def updateInventory(self, inv):
        self.inventory = inv
        self.calcTotalProps()

    def makeNetString(self):
        """makeNetString(self)
        Make a network packet out of the inventory
        """
        dataList = self.inventory
        datagram = PyDatagram()
        for track in range(0, len(Tracks)):
            for level in range(0, len(Levels[track])):
                datagram.addUint8(dataList[track][level])
        dgi = PyDatagramIterator(datagram)
        return dgi.getRemainingBytes()
    
    def makeFromNetString(self, netString):
        """makeFromNetString(self)
        Make an inventory from a network packet
        """
        dataList = []
        dg = PyDatagram(netString)
        dgi = PyDatagramIterator(dg)
        for track in range(0, len(Tracks)):
            subList = []
            for level in range(0, len(Levels[track])):
                if dgi.getRemainingSize() > 0:
                    value = dgi.getUint8()
                else:
                    value = 0
                subList.append(value)
            dataList.append(subList)
        return dataList
        
    def makeFromNetStringForceSize(self, netString, numTracks, numLevels):
        """makeFromNetString(self)
        Make an inventory from a network packet
        """
        dataList = []
        dg = PyDatagram(netString)
        dgi = PyDatagramIterator(dg)
        for track in range(0, numTracks):
            subList = []
            for level in range(0, numLevels):
                if dgi.getRemainingSize() > 0:
                    value = dgi.getUint8()
                else:
                    value = 0
                subList.append(value)
            dataList.append(subList)
        return dataList


    # setters and getters

    def addItem(self, track, level):
        """addItem(self, [int | string], int):
        Add an item to the given track and level
        """
        return self.addItems(track, level, 1)
        
    def addItems(self, track, level, amount):
        """addItems(self, [int | string], int, int)
        Add amount of an item to the given track and level. Returns total
        items in given level and track if successful, 0 if insufficient
        skill level, -1 if over item max, -2 if over total max.
        """
        if (type(track) == type('')):
            track = Tracks.index(track)

        max = self.getMax(track, level)

        # check against current skill level
        if hasattr(self.toon,"experience") and hasattr(self.toon.experience, "getExpLevel"):
                if (self.toon.experience.getExpLevel(track) >= level) and (self.toon.hasTrackAccess(track)):
                    # check current against max
                    if ( self.numItem(track,level) <= (max - amount) ):
                        #ubergags not limited by gag bag size
                        if (self.totalProps + amount <= self.toon.getMaxCarry()) or (level > LAST_REGULAR_GAG_LEVEL):
                            self.inventory[track][level] += amount
                            self.totalProps += amount
                            return self.inventory[track][level]
                        else:
                            # over total max
                            return -2
                    else:
                        # over item max
                        return -1
                else:
                    # insufficient skill or no access to track
                    return 0
        else:
            # deleted object
            return 0

    def addItemWithList(self, track, levelList):
        """
        This is for adding one new item for each of the new gags you earned
        on a track during a reward sequence. Generally, levelList will only
        contain one level, or no levels.
        """
        for level in levelList:
            self.addItem(track, level)
            
    def numItem(self, track, level):
        """numItem(self, [int | string], int)
        Return the number of items in the given track and level
        """
        if (type(track) == type('')):
            track = Tracks.index(track)
        if track > (len(Tracks) - 1) or level > (len(Levels) - 1):
            self.notify.warning("%s is using a gag that doesn't exist %s %s!" % (self.toon.doId, track, level))
            return -1
        return self.inventory[track][level]
        
    def useItem(self, track, level):
        """useItem(self, [int | string], int)
        If possible, use one item of given track and level
        """
        if type(track) == type(''):
            track = Tracks.index(track)

        if self.numItem(track, level) > 0:
            self.inventory[track][level] -= 1
            self.calcTotalProps()
        elif self.numItem(track, level) == -1: #check for cheaters
            return -1
        
    def setItem(self, track, level, amount):
        """setItem(self, [int | string], int, int)
        Set the number of items directly
        We should check validity here probably
        """
        #print("Setting Item")
        if (type(track) == type('')):
            track = Tracks.index(track)

        max = self.getMax(track, level)
        curAmount = self.numItem(track,level)

        # check against current skill level
        if (self.toon.experience.getExpLevel(track) >= level):
            # check current against max
            if (amount <= max):
                if (self.totalProps - curAmount + amount <= self.toon.getMaxCarry()):
                    self.inventory[track][level] = amount
                    self.totalProps = self.totalProps - curAmount + amount
                    return self.inventory[track][level]
                else:
                    # over total max
                    return -2
            else:
                # over item max
                return -1
        else:
            # insufficient skill
            return 0

    def getMax(self, track, level):
        """getMax(self, [int | string], int)
        Return the maximum of an item of given track and level
        """
        if (type(track) == type('')):
            track = Tracks.index(track)

        # find max for this track/level
        maxList = CarryLimits[track]

        #RAU we create a dummy DistributedToonAI when we abort from a building battle
        #so experience may still be None, if so, just return 0
        if self.toon.experience:
            return maxList[self.toon.experience.getExpLevel(track)][level]
        else:
            return 0
        

    def getTrackAndLevel(self, propName):
        """getTrackAndLevel(self, string):
        Given a prop name string, return its track and level or
        -1, -1 if not found
        """
        for track in range(0, len(Tracks)):
            if (AvProps[track].count(propName)):
                return tracks, AvProps[track].index(propName)

        # else, not found
        return -1, -1
    
    def calcTotalProps(self):
        """calcTotalProps(self):
        Tally the current total number of props
        """
        self.totalProps = 0
        for track in range(0, len(Tracks)):
            for level in range(0, len(Levels[track])):
                if level <= LAST_REGULAR_GAG_LEVEL:
                    self.totalProps += self.numItem(track, level)

        return None

    def countPropsInList(self, invList):
        totalProps = 0
        for track in range(len(Tracks)):
            for level in range(len(Levels[track])):
                if level <= LAST_REGULAR_GAG_LEVEL:
                    totalProps += invList[track][level]
        return(totalProps)

    
    #def getMaxTotalProps(self):
    #    """findMaxTotalProps(self):
    #    Based on maxHp, determine the total number of props we can carry
    #    """
    #    maxTotalProps = 0
    #    for level in range(0, len(MaxProps)):
    #        if (self.toon.maxHp >= MaxProps[level][0]):
    #            maxTotalProps = MaxProps[level][1]
    #    return maxTotalProps

    def setToMin(self, newInventory):
        """setToMin(self, newInventory):
        Given a new proposed inventory, set each value of the current inventory
        to new value, only if it is lower. This is used by the AI when players
        attempt to delete items, to prevent cheating.
        """
        for track in range(len(Tracks)):
            for level in range(len(Levels[track])):
                self.inventory[track][level] = min(self.inventory[track][level],
                                                   newInventory[track][level])

        self.calcTotalProps()
        return None

    def validateItemsBasedOnExp(self, newInventory, allowUber = 0):
        #tempInventory = InventoryBase(none, newInventory)
        if type(newInventory) == type("String"):
            tempInv = self.makeFromNetString(newInventory)
        else:
            tempInv = newInventory
        for track in range(len(Tracks)):
            for level in range(len(Levels[track])):
                #print("Track: %s Level: %s" % (track, level))
                if tempInv[track][level] > self.getMax(track, level):
                    #print("invalid norm %s" % (tempInv[track][level] ))
                    #import pdb; pdb.set_trace()
                    return 0
                #UBER no buying of the ubergags
                if (level > LAST_REGULAR_GAG_LEVEL) and (tempInv[track][level] > self.inventory[track][level]) or allowUber:
                    #print("invalid uber")
                    return 0
        return 1

    def getMinCostOfPurchase(self, newInventory):
        # BUG : check items deleted
        return self.countPropsInList(newInventory) - self.totalProps

    def validatePurchase(self, newInventory, currentMoney, newMoney):
        """validatePurchase(self, newInventory):
        Given a new proposed inventory, and the number of money
        that was presumably used to purchase this new inventory, test for
        the validity of the purchase. If it is valid, then update the inventory
        and new money balance appropriately.
        """

        # Sanity check, you should not be able to make money during the purchase screen
        if (newMoney > currentMoney):
            self.notify.warning("Somebody lied about their money! Rejecting purchase.")
            return 0

        # First, check to make sure the user didn't overspend
        newItemTotal = self.countPropsInList(newInventory)
        oldItemTotal = self.totalProps

        # Then, make sure that the user is allowed to purchase the items
        # he has chosen.
        if (newItemTotal > (oldItemTotal + currentMoney)):
            self.notify.warning("Somebody overspent! Rejecting purchase.")
            return 0

        # Make sure they did not buy more items than the new money is
        # reporting Note: they could have ended up with no more items
        # than they started with but less money if they deleted 10
        # items then bought 10 others. In this case They will have the
        # same item total, but 10 less money. There is a hack here
        # where a hacked client could delete 10 items, buy 10 others,
        # but report no money was spent and we would not catch them,
        # but unless we verify each individual buy/delete transation
        # with the server, I see no way to prevent this and it is not
        # that bad anyways.
        if (newItemTotal - oldItemTotal) > (currentMoney - newMoney):
            self.notify.warning("Too many items based on money spent! Rejecting purchase.")
            return 0

        # Make sure they did not exceed their maximum carry amount.
        if (newItemTotal > self.toon.getMaxCarry()):
            self.notify.warning("Cannot carry %s items! Rejecting purchase." % (newItemTotal))
            return 0
            
        if self.validateItemsBasedOnExp(newInventory):
            # The purchase is valid.
            self.updateInventory(newInventory)
            return 1
        else:
            self.notify.warning("Somebody is trying to buy forbidden items! " +
                                "Rejecting purchase.")
            return 0

    def maxOutInv(self, filterUberGags = 0):
        """maxInv(self):
        Iterate over all the props we might be able to use, and keep
        adding props until we have reached our max. This is for debugging.
        """
        #print("Filter Uber Gags? %s" % (filterUberGags))

        # First, add at least one gag at each level.
        for track in range(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                for level in range (len(Levels[track])):
                    if ((level <= LAST_REGULAR_GAG_LEVEL) or (not filterUberGags)):
                        self.addItem(track, level)

        # Now, add from the top level down, so we end up with mostly
        # higher-level gags.
        addedAnything = 1
        while addedAnything:
            addedAnything = 0

            for track in range(len(Tracks)):
                if self.toon.hasTrackAccess(track):
                    level = len(Levels[track]) - 1
                    if level > LAST_REGULAR_GAG_LEVEL and filterUberGags:
                        level = LAST_REGULAR_GAG_LEVEL
                    result = self.addItem(track, level)
                    level -= 1
                    while result <= 0 and level >= 0:
                        result = self.addItem(track, level)
                        level -= 1
                    if result > 0:
                        addedAnything = 1

        self.calcTotalProps()
        return None

    def NPCMaxOutInv(self, targetTrack = -1):
        """NPCMaxOutInv(self):
        Iterate over all the props we might be able to use, and keep
        adding props until we have reached our max.
        """

        # Go through the highest level(s) of gags and add
        # as many as possible, then move down to the next
        # highest
        for level in range(5, -1, -1):
            anySpotsAvailable = 1
            while (anySpotsAvailable == 1):
                anySpotsAvailable = 0
                trackResults = []
                for track in range(len(Tracks)):
                    if (targetTrack != -1 and targetTrack != track):
                        continue 
                    result = self.addItem(track, level) 
                    #print "track: %d level: %d result: %d" % (track, level, result)
                    trackResults.append(result)
                    if (result == -2):
                        break
                # See if we need to make another pass
                for res in trackResults:
                    if (res > 0):
                        anySpotsAvailable = 1
            if (result == -2):
                break

        self.calcTotalProps()
        return None
    
    def zeroInv(self, killUber = 0):
        """maxInv(self):
        Erase all our props.
        #uber gags are excluded from this prop reset
        """
        for track in range(len(Tracks)):
            for level in range(UBER_GAG_LEVEL_INDEX):# (len(Levels[track])):
                self.inventory[track][level] = 0
            if killUber:
               self.inventory[track][UBER_GAG_LEVEL_INDEX] = 0
            if self.inventory[track][UBER_GAG_LEVEL_INDEX] > 1:
               self.inventory[track][UBER_GAG_LEVEL_INDEX] = 1 
        self.calcTotalProps()
        return None 
