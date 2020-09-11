"""SuitDNA module: contains the methods and definitions for describing
multipart actors with a simple class"""

import random
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toonbase import TTLocalizer
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA

notify = directNotify.newCategory("SuitDNA")

# suit defines
suitHeadTypes = [
    #
    # warning: changes to this list will affect *Suit* methods below.
    # We also depend on this ordering in the battle exp system.
    # corporate
    "f", "p", "ym", "mm", "ds", "hh", "cr", "tbc",
    # legal
    "bf", "b", "dt", "ac", "bs", "sd", "le", "bw",
    # money
    "sc", "pp", "tw", "bc", "nc", "mb", "ls", "rb",
    # sales
    "cc", "tm", "nd", "gh", "ms", "tf", "m", "mh",
    ]

suitATypes = [ "ym", "hh", "tbc", "dt", "bs", "le", "bw", "pp", "nc",
               "rb", "nd", "tf", "m", "mh" ]

suitBTypes = [ "p", "ds", "b", "ac", "sd", "bc", "ls", "tm", "ms" ]

suitCTypes = [ "f", "mm", "cr", "bf", "sc", "tw", "mb", "cc", "gh" ]

suitDepts = [ "c", "l", "m", "s" ]
suitDeptFullnames = {"c" : TTLocalizer.Bossbot,
                     "l" : TTLocalizer.Lawbot,
                     "m" : TTLocalizer.Cashbot,
                     "s" : TTLocalizer.Sellbot,
                     }
suitDeptFullnamesP = {"c" : TTLocalizer.BossbotP,
                      "l" : TTLocalizer.LawbotP,
                      "m" : TTLocalizer.CashbotP,
                      "s" : TTLocalizer.SellbotP,
                      }
corpPolyColor = VBase4(0.95, 0.75, 0.75, 1.0)
legalPolyColor = VBase4(0.75, 0.75, 0.95, 1.0)
moneyPolyColor = VBase4(0.65, 0.95, 0.85, 1.0)
salesPolyColor = VBase4(0.95, 0.75, 0.95, 1.0)

suitsPerLevel = [1,1,1,1,1,1,1,1]
suitsPerDept = 8

goonTypes = ["pg", "sg"]

def getSuitBodyType(name):
    """getSuitBodyType(string):
    Given a suit name, return its body type (a, b, or c)
    """
    if (name in suitATypes):
        return "a"
    elif (name in suitBTypes):
        return "b"
    elif (name in suitCTypes):
        return "c"
    else:
        print "Unknown body type for suit name: ", name

def getSuitDept(name):
    """getSuitDept(string):
    Given a suit name, return its department name as a string
    """
    index = suitHeadTypes.index(name)
    if (index < suitsPerDept):
        return suitDepts[0]
    elif (index < suitsPerDept*2):
        return suitDepts[1]
    elif (index < suitsPerDept*3):
        return suitDepts[2]
    elif (index < suitsPerDept*4):
        return suitDepts[3]
    else:
        print "Unknown dept for suit name: ", name
        return None

def getDeptFullname(dept):
    """getDeptFullname(string):
    Given a dept code, return the fullname
    """
    return suitDeptFullnames[dept]

def getDeptFullnameP(dept):
    """getDeptFullnameP(string):
    Given a dept code, return the fullname (plural)
    """
    return suitDeptFullnamesP[dept]

def getSuitDeptFullname(name):
    """getSuitDept(string):
    Given a suit code, return the fullname
    """
    return suitDeptFullnames[getSuitDept(name)]

def getSuitType(name):
    """getSuitType(string):
    Given a suit name, return its type index (1..8).
    """
    index = suitHeadTypes.index(name)
    return (index % suitsPerDept) + 1

def getRandomSuitType(level, rng=random):
    """ given a suit level, return a randomly-chosen suit type """
    return random.randint(max(level-4, 1 ), min(level, 8))

def getRandomSuitByDept(dept):
    """ given a suit dept, return a randomly-chosen suit """
    deptNumber = suitDepts.index(dept)
    return suitHeadTypes[(suitsPerDept*deptNumber) + random.randint(0,7)]

class SuitDNA(AvatarDNA.AvatarDNA):
    """SuitDNA class: contains methods for describing avatars with a
    simple class. The SuitDNA class may be converted to lists of strings
    for network transmission. Also, SuitDNA objects can be constructed
    from lists of strings recieved over the network. Some examples are in
    order.

        # create a suit's dna
        dna = AvatarDNA()
        dna.newSuit()             # no args defaults to 'Downsizer'
        dna.newSuit('ym')         # make 'Yes Man' dna
        dna.newSuitRandom(3)      # make a random level 3 suit
        dna.newSuitRandom(3, 'l') # make a random level 3 legal suit
        
    """
    # special methods
    
    def __init__(self, str=None, type=None, dna=None, r=None, b=None, g=None):
        """__init__(self, string=None, string=None, string()=None, float=None,
        float=None, float=None)
        SuitDNA contructor - see class comment for usage
        """
        # have they passed in a stringified DNA object?
        if (str != None):
            self.makeFromNetString(str)
        # have they specified what type of DNA?
        elif (type != None):
            if (type == 's'):  # Suit
                self.newSuit()
            else:
                # Invalid type
                assert 0
        else:
            # mark DNA as undefined
            self.type = 'u'

    def __str__(self):
        """__str__(self)
        Avatar DNA print method
        """
        if (self.type == 's'):
            return "type = %s\nbody = %s, dept = %s, name = %s" % \
                   ("suit", self.body, self.dept, self.name)
        elif (self.type == 'b'):
            return "type = boss cog\ndept = %s" % (self.dept)
        else:
            return "type undefined"


    # stringification methods
    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if (self.type == 's'):
            dg.addFixedString(self.name, 3)
            dg.addFixedString(self.dept, 1)
        elif (self.type == 'b'):  # Boss Cog
            dg.addFixedString(self.dept, 1)
        elif (self.type == 'u'):
            notify.error("undefined avatar")
        else:
            notify.error("unknown avatar type: ", self.type)

        return dg.getMessage()

    def makeFromNetString(self, string):
        dg=PyDatagram(string)
        dgi=PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if (self.type == 's'):  # Suit
            self.name = dgi.getFixedString(3)
            self.dept = dgi.getFixedString(1)
            self.body = getSuitBodyType(self.name)
        elif (self.type == 'b'):  # Boss Cog
            self.dept = dgi.getFixedString(1)
        else:
            notify.error("unknown avatar type: ", self.type)

        return None
    
    def __defaultGoon(self):
        """__defaultChar(self)
        Make a default character dna
        """
        self.type = 'g'
        self.name = goonTypes[0]
        
    def __defaultSuit(self):
        """__defaultSuit(self)
        Make a default suit dna
        """
        self.type = 's'
        self.name = 'ds'
        self.dept = getSuitDept(self.name)
        self.body = getSuitBodyType(self.name)

    def newSuit(self, name=None):
        """newSuit(self, string=None)
        If no suit name specified, set the dna for the default suit
        else set the dna for suit specified by the given string.
        """
        if (name == None):
            self.__defaultSuit()
        else:
            self.type = "s"
            self.name = name
            self.dept = getSuitDept(self.name)
            self.body = getSuitBodyType(self.name)

    def newBossCog(self, dept):
        self.type = "b"
        self.dept = dept

    def newSuitRandom(self, level=None, dept=None):
        """newSuitRandom(self, int=None, string=None)
        Generate dna for a random suit of random level (unless level
        is specified) and random dept (again, unless specified)
        """
        self.type = "s"
        
        if (level==None):
            # pick a random level
            level = random.choice(range(1, len(suitsPerLevel)))
        else:
            # make sure supplied one is valid
            if (level < 0 or level > len(suitsPerLevel)):
                notify.error("Invalid suit level: %d" % level)                

        if (dept == None):
            # pick a random dept
            dept = random.choice(suitDepts)
        else:
            # make sure supplied one is valid
            assert dept in suitDepts
                
        # calculate range to choose from based on the level and dept
        self.dept = dept
        index = suitDepts.index(dept)
        base = index * suitsPerDept
        offset = 0
        if (level > 1):
            for i in range(1, level):
                offset = offset + suitsPerLevel[i - 1]
        bottom = base + offset
        top = bottom + suitsPerLevel[level - 1]
        self.name = suitHeadTypes[random.choice(range(bottom,top))] 
        self.body = getSuitBodyType(self.name)        

    def newGoon(self, name = None):
        """newGoon(self, type)
        Return the dna for the goon of this name.  If no name is given
        return the default goon.
        """
        if type == None:
            self.__defaultGoon()
        else:
            self.type = 'g'
            if (name in  goonTypes):
                self.name = name
            else:
                notify.error("unknown goon type: ", name)
        
    def getType(self):
        """getType(self)
        Return which type of actor this dna represents.
        """
        if (self.type == 's'):
            #suit type
            type = "suit"
        elif (self.type == 'b'):
            #boss type
            type = "boss"
        else:
            notify.error("Invalid DNA type: ", self.type)

        return type
