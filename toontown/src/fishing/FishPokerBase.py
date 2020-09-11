
import FishBase
from toontown.toonbase import TTLocalizer

CARD_INDEX = 0
LOCK_INDEX = 1

# Reward base for varios hands
# These are modified by the rarity level of the various fish
RewardDict = {
    (5,) : (100, TTLocalizer.FishPoker5OfKind),
    (4,1) : (50, TTLocalizer.FishPoker4OfKind),
    (3,2) : (25, TTLocalizer.FishPokerFullHouse),
    (3,1,1) : (10, TTLocalizer.FishPoker3OfKind),
    (2,2,1) : (5, TTLocalizer.FishPoker2Pair),
    (2,1,1,1) : (2, TTLocalizer.FishPokerPair),
    }


class FishPokerBase:

    NumSlots = 5
    
    def __init__(self):
        self.__cards = {}
        self.clear()

    def isCard(self, index):
        return (self.__cards[index][CARD_INDEX] is not None)

    def isLocked(self, index):
        return self.__cards[index][LOCK_INDEX]

    def indexAvailable(self, index):
        card, locked = self.__cards[index]
        if (card is None) or (not locked):
            return 1
        else:
            return 0

    def getFirstIndexAvailable(self):
        # First check to see if any are completely free
        for i in range(self.NumSlots):
            if (not self.isCard(i)):
                return i
        # If you got here, they must all be filled with card
        # Return the first one that is not locked
        for i in range(self.NumSlots):
            if (not self.isLocked(i)):
                return i
        # If you got here, they are all locked too
        # There are none available
        return -1

    def setLockStatus(self, index, lockStatus):
        assert (lockStatus == 0 or lockStatus == 1)
        if self.__cards[index][CARD_INDEX]:
            self.__cards[index][LOCK_INDEX] = lockStatus
            return 1
        else:
            return 0

    def cashIn(self):
        # This will only get called by the AI
        value, handName = self.getCurrentValue()
        self.clear()
        return value

    def drawCard(self, card):
        index = self.getFirstIndexAvailable()
        if index == -1:
            # All spots are taken
            return -1
        else:
            # Start it out unlocked
            self.__cards[index] = [card, 0]
            return index

    def getCurrentValue(self):
        cards = {}
        noneList = []
        for cardInfo in self.__cards.values():
            card, locked = cardInfo
            if card is None:
                noneList.append(1)
            else:
                genus = card.getGenus()
                if cards.has_key(genus):
                    cards[genus] += 1
                else:
                    cards[genus] = 1
        cardList = cards.values()
        cardList.sort()
        cardList.reverse()
        cardList.extend(noneList)
        # Convert to tuple for dictionary lookup
        cardList = tuple(cardList)
        rewardInfo = RewardDict.get(cardList, (0, ""))
        return rewardInfo

    def clear(self):
        for i in range(self.NumSlots):
            self.__cards[i] = [None, 0]

    def __str__(self):
        s = ""
        availIndex = self.getFirstIndexAvailable()
        for i in range(self.NumSlots):
            card, locked = self.__cards[i]
            if locked:
                lockedStr = "Locked"
            else:
                lockedStr = "Unlocked"
            s += ("%s : %s, %s" % (i, card, lockedStr)) 
            if (i == availIndex):
                s += " <--"
            s += "\n"
        return s
    
        
