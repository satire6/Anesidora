import Toon
from toontown.suit import Suit
from toontown.pets import Pet
from otp.avatar import Avatar
import NPCToons
import ToonDNA
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals
import math
import types
import __builtin__
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from random import *
from direct.distributed.PyDatagram import PyDatagram

try:
    __builtin__.launcher
except AttributeError:
    __builtin__.launcher = None

class RobotAvatarBase:
    # Base class for robot toons and robot suits
    # Not meant to be instantiated by itself
    def __init__(self, parent = render,
                 startPos = Point3(0), startHpr = Point3(0),
                 endPos = Point3(0,1,0), endHpr = Point3(0),
                 state = 'neutral'):
        self.setTag('robotAvatar', '1')
        # Place robot within world
        self.reparentTo(parent)
        self.setStartPos(startPos)
        self.setStartHpr(startHpr)
        self.setEndPos(endPos)
        self.setEndHpr(endHpr)
        self.setPosHpr(self.startPos, self.startHpr)
        self.ival = self.victoryIval = None
        if not base.config.GetBool('want-new-anims',1):        
            self.updateWalkIval()
            self.accept('playVictoryIval', lambda: self.setAnimState('victory'))
            self.accept('playRTMWalkIval', lambda: self.setAnimState('walk'))
            self.accept('playRTMRunIval', lambda: self.setAnimState('run'))
        self.setAnimState(state)        
        self.state = state
    def convertServerDNAString(self, serverString, type = 't'):
        # Strip out blank space and take last 30 characters
        serverString = serverString.replace(' ', '')
        if type == 't':
            stringLen = 30
        else:
            stringLen = 6
        serverString = serverString[-stringLen:]
        # Create a datagram from server string
        dg = PyDatagram()
        for i in range(0,len(serverString),2):
            eval('dg.addUint8(0x%s)' % serverString[i:i+2])
        return dg.getMessage()
    def setAnimState(self,state):
        self.stopIvals()
        self.state = state
        if not base.config.GetBool('want-new-anims',1):     
            if state == 'victory':
                if self.victoryIval != None:
                    self.victoryIval.start()
                    return
            elif state in ['run', 'walk', 'sad-walk']:
                if state == 'run':
                    self.ival.loop()
                elif state == 'walk':
                    self.ival.loop(playRate = 0.25)
                elif state == 'sad-walk':
                    self.ival.loop(playRate = 0.0625)
            else:
                self.setPosHpr(self.startPos, self.startHpr)
        self.loop(state)
    def setStartPos(self, pos):
        self.startPos = Point3(pos)
    def setEndPos(self, pos):
        self.endPos = Point3(pos)
    def setStartHpr(self, hpr):
        self.startHpr = Point3(hpr)
    def setEndHpr(self, hpr):
        self.endHpr = Point3(hpr)
    def updateStartPos(self, pos):
        self.setStartPos(pos)
        self.updateWalkIval()
        if self.state == 'neutral':
            self.setAnimState('walk')
        else:
            self.setAnimState(self.state)
    def updateEndPos(self, pos):
        self.setEndPos(pos)
        self.updateWalkIval()
        if self.state == 'neutral':
            self.setAnimState('walk')
        else:
            self.setAnimState(self.state)
    def updateWalkIval(self):
        self.stopIvals()
        start2Stop = Vec3(self.endPos - self.startPos)
        dist = start2Stop.length()
        walkDuration = dist/ToontownGlobals.ToonForwardSpeed
        angleVec = Vec3(start2Stop)
        angleVec.setZ(0)
        angleVec.normalize()
        dotProd = angleVec.dot(Vec3(0,1,0))
        angle = rad2Deg(math.acos(dotProd))
        if angleVec[0] >= 0:
            angle *= -1
        if angle > 0:
            backAngle = angle - 180.0
        else:
            backAngle = angle + 180.0
        backAngle = (angle + 180.0)
        self.ival = Sequence(
            Func(self.setHpr, angle, 0, 0),
            self.posInterval(duration = walkDuration, pos = self.endPos,
                             startPos = self.startPos),
            self.hprInterval(duration = 1, hpr = Vec3(backAngle,0,0),
                             startHpr = Vec3(angle,0,0)),
            self.posInterval(duration = walkDuration, pos = self.startPos,
                             startPos = self.endPos),
            self.hprInterval(duration = 1, hpr = Vec3(angle,0,0),
                             startHpr = Vec3(backAngle,0,0)),
            )
        vDuration = self.getDuration('victory')
        if vDuration:
            vRemainder = (walkDuration % vDuration)
            vWait = vDuration - vRemainder
            self.victoryIval = Sequence(
                # Jitter by up to 2 frames
                Wait(randint(0,2) * (1/24.0)),
                Func(self.setPosHpr, self.startPos, Vec3(angle,0,0)),
                Func(self.loop,'neutral'),
                Func(self.loop,'run'),
                self.posInterval(duration = walkDuration, pos = self.endPos,
                                 startPos = self.startPos),
                Parallel(
                Sequence(ActorInterval(self, 'victory', startTime = vRemainder)),
                Sequence(
                Wait(vWait),
                Func(self.loop,'victory')
                )
                )
                )
        else:
            # doodle don't have a victory anim
            self.victoryIval = None
    def stopIvals(self):
        if self.ival != None:
            self.ival.finish()
        if self.victoryIval != None:
            self.victoryIval.finish()
    def destroy(self):
        self.stopIvals()
        self.stop()
        self.ignore('playVictoryIval')
        self.removeNode()

class RobotToon(Toon.Toon, RobotAvatarBase):
    # Default is flippy
    def __init__(self, description = None, parent = render,
                 startPos = Point3(0), startHpr = Point3(0),
                 endPos = Point3(0,1,0), endHpr = Point3(0),
                 state = 'neutral'):
        # Initialize superclasses
        Toon.Toon.__init__(self)
        self.customMessages = []
        self.setCogLevels([1,1,1,1])
        self.updateDNA(description)
        RobotAvatarBase.__init__(self, parent, startPos, startHpr,
                                 endPos, endHpr, state)
        self.showHiRes()
        
    def updateDNA(self, description):
        # Create dna
        if isinstance(description, ToonDNA.ToonDNA):
            dna = description
        else:
            dna = ToonDNA.ToonDNA()
            if (isinstance(description, types.ListType) or
                isinstance(description, types.TupleType)):
                # Assume it is a property list
                dna.newToonFromProperties(*description)
            elif isinstance(description, Datagram):
                # Create dna straight from datagram
                dna.makeFromNetString(description)
            elif isinstance(description, types.StringType):
                # Assume it is a server string description
                # Convert to datagram then create dna
                dna.makeFromNetString(self.convertServerDNAString(description))
            elif isinstance(description, types.IntType):
                # Assume it is an NPC id
                npcInfo = NPCToons.NPCToonDict[description]
                properties = npcInfo[2]
                if properties == 'r':
                    gender = npcInfo[3]
                    properties = NPCToons.getRandomDNA(description, gender)
                dna.newToonFromProperties(*properties)
            else:
                if random() < 0.5:
                    gender = 'm'
                else:
                    gender = 'f'
                dna.newToonRandom(gender = gender)
        if not self.style:
            # New toon, need to initialize style
            self.setDNA(dna)
        else:
            # Just jump straight to the update function
            self.updateToonDNA(dna,fForce = 1)

    def setCogLevels(self, levels):
        self.cogLevels = levels

    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages

    def showHiRes(self, switchIn = 10000):
        lodNames = self.getLODNames()
        if lodNames:
            maxLOD = int(lodNames[0])
            self.setLOD(maxLOD, switchIn,0)
            for lod in lodNames[1:]:
                self.setLOD(int(lod), switchIn + 10, switchIn)
                switchIn += 10

class RobotSuit(Suit.Suit, RobotAvatarBase):
    # Default is flippy
    def __init__(self, description = None, parent = render,
                 startPos = Point3(0), startHpr = Point3(0),
                 endPos = Point3(0,1,0), endHpr = Point3(0),
                 state = 'neutral'):
        # Initialize superclasses
        Suit.Suit.__init__(self)
        self.updateDNA(description)
        RobotAvatarBase.__init__(self, parent, startPos, startHpr,
                                 endPos, endHpr, state)
    def updateDNA(self, description):
        # Create dna
        if isinstance(description, ToonDNA.ToonDNA):
            dna = description
        else:
            dna = SuitDNA.SuitDNA()
            if isinstance(description, types.StringType):
                # Assume it is a suit specification
                dna.newSuit(description)
            elif isinstance(description, types.IntType):
                # Assume it specifies suit level
                dna.newSuitRandom(description)
            elif (isinstance(description, types.ListType) or
                isinstance(description, types.TupleType)):
                # Assume it is a (level,track) list
                dna.newSuitRandom(description[0], description[1])
            else:
                level = randint(0,7)
                trackVal = random()
                if trackVal < 0.25:
                    track = 'c'
                elif trackVal < 0.5:
                    track = 's'
                elif trackVal < 0.75:
                    track = 'l'
                else:
                    track = 'm'
                dna.newSuitRandom(level, track)
        self.setDNA(dna)

class RobotDoodle(Pet.Pet, RobotAvatarBase):
    def __init__(self, description = None, parent = render,
                 startPos = Point3(0), startHpr = Point3(0),
                 endPos = Point3(0,1,0), endHpr = Point3(0),
                 state = 'neutral'):
        # Initialize superclasses
        Pet.Pet.__init__(self)
        self.updateDNA(description)
        RobotAvatarBase.__init__(self, parent, startPos, startHpr,
                                 endPos, endHpr, state)
    def updateDNA(self, description):
        # doodle dna is an array of the form: [head, ears, nose, tail, body, color, partColor, eyes, gender]
        if (isinstance(description, types.ListType) or isinstance(description, types.TupleType)):
            self.setDNA(description)

