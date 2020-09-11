"""DistributedCCharBase module: contains the DistributedCCharBase class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.avatar import Avatar
from libotp import CFQuicktalker
from toontown.char import CharDNA
from toontown.char import DistributedChar
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.controls.ControlManager import CollisionHandlerRayStart
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.TTLocalizer import Donald, DonaldDock, WesternPluto, Pluto
from toontown.effects import DustCloud
import CCharChatter
import CCharPaths

import string
import copy

class DistributedCCharBase(DistributedChar.DistributedChar):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCCharBase")

    def __init__(self, cr, name, dnaName):
        try:
            self.DistributedCCharBase_initialized
            return
        except:
            self.DistributedCCharBase_initialized = 1
        DistributedChar.DistributedChar.__init__(self, cr)

        dna = CharDNA.CharDNA()
        dna.newChar(dnaName)
        self.setDNA(dna)
        self.setName(name)
        self.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.colorScaleInterval( 0.5, Vec4(1, 1, 1, 1),
                                               startColorScale = Vec4(1, 1, 1, 0),
                                               blendType = 'easeInOut')
        fadeIn.start()
        # Where is the character walking?
        self.diffPath = None
        self.transitionToCostume = 0
        self.__initCollisions()

    def __initCollisions(self):
        self.cSphere = CollisionSphere(0., 0., 0., 8.)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode(self.getName() + 'BlatherSphere')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

        self.acceptOnce("enter" + self.cSphereNode.getName(),
                        self.__handleCollisionSphereEnter)

        # Set up the collison ray
        # This is a ray cast from your head down to detect floor polygons
        # and is only turned on during specific parts of the character's path
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode(self.getName() + "cRay")
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())

        # set up floor collision mechanism
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        # NOTE:  a height of 10 is high, but seems to allow Minnie to walk
        # through the horns in Melodyland without weird floor collision things
        # happening, this can cause problems if a character tries to walk
        # under an opening that has a floor within 10ft above.
        self.lifter.setReach(10.0)

        # Limit our rate-of-fall with the lifter.
        # 0 means we don't want to limit the velocity, this seems
        # to help when the ray is conflicting with a pos lerp which, for
        # example, moves this character down a ramp in DaisyGardens.
        self.lifter.setMaxVelocity(0.0)
        self.lifter.addCollider(self.cRayNodePath, self)

        # now use the local toon's collision traverser to handle
        # updating collision info
        #
        self.cTrav = base.localAvatar.cTrav

    def __deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath

        # floor collision stuff
        #
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None
        self.cTrav = None

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        self.stopBlink()
        self.ignoreAll()
        self.chatTrack.finish()
        del self.chatTrack
        if self.chatterDialogue:
            self.chatterDialogue.stop()
        del self.chatterDialogue
        DistributedChar.DistributedChar.disable(self)
        self.stopEarTask()

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        try:
            self.DistributedCCharBase_deleted
        except:
            self.setParent(NodePath("Temp"))
            self.DistributedCCharBase_deleted = 1
            self.__deleteCollisions()
            DistributedChar.DistributedChar.delete(self)

    def generate(self, diffPath = None):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedChar.DistributedChar.generate(self)

        if diffPath==None:
            self.setPos(CCharPaths.getNodePos(
                CCharPaths.startNode,
                CCharPaths.getPaths(self.getName(), self.getCCLocation())))
        else:
            self.setPos(CCharPaths.getNodePos(
                CCharPaths.startNode,
                CCharPaths.getPaths(diffPath, self.getCCLocation())))

        self.setHpr(0,0,0)
        
        # The characters can be immediately parented to render.
        self.setParent(ToontownGlobals.SPRender)

        # hmm. does this character ever blink?
        self.startBlink()
        self.startEarTask()

        # the character's chat track
        self.chatTrack = Sequence()

        # Currently playing dialog
        self.chatterDialogue = None

        # listen for the collision sphere enter event
        self.acceptOnce("enter" + self.cSphereNode.getName(),
                        self.__handleCollisionSphereEnter)

        # listen for safe zone exit event
        self.accept("exitSafeZone", self.__handleExitSafeZone)

    def __handleExitSafeZone(self):
        # local avatar is leaving the safe zone

        # tell the server that the local toon is leaving,
        # regardless of whether or not the toon was close
        # to this character
        self.__handleCollisionSphereExit(None)

    # collision sphere
    def __handleCollisionSphereEnter(self, collEntry):
        self.notify.debug("Entering collision sphere...")
        # tell the server that the local toon has come
        # within blathering range
        self.sendUpdate("avatarEnter", [])

        # listen for chat events
        self.accept('chatUpdate', self.__handleChatUpdate)
        self.accept('chatUpdateSC', self.__handleChatUpdateSC)
        self.accept('chatUpdateSCCustom', self.__handleChatUpdateSCCustom)
        self.accept('chatUpdateSCToontask', self.__handleChatUpdateSCToontask)
        
        # put nametag in the transparent layer so toon nametags can render on top of it.
        self.nametag3d.setBin('transparent',100)        
        
        # listen for the exit event
        self.acceptOnce("exit" + self.cSphereNode.getName(),
                        self.__handleCollisionSphereExit)

    def __handleCollisionSphereExit(self, collEntry):
        self.notify.debug("Exiting collision sphere...")
        # tell the server that the local toon has left
        # blathering range
        self.sendUpdate("avatarExit", [])

        # stop listening for chat events
        self.ignore('chatUpdate')
        self.ignore('chatUpdateSC')
        self.ignore('chatUpdateSCCustom')
        self.ignore('chatUpdateSCToontask')

        # listen for the enter event
        self.acceptOnce("enter" + self.cSphereNode.getName(),
                        self.__handleCollisionSphereEnter)

    # someday, classic characters might respond in some way to
    # *what* you're saying.
    def __handleChatUpdate(self, msg, chatFlags):
        self.sendUpdate("setNearbyAvatarChat", [msg])

    def __handleChatUpdateSC(self, msgIndex):
        self.sendUpdate('setNearbyAvatarSC', [msgIndex])

    def __handleChatUpdateSCCustom(self, msgIndex):
        self.sendUpdate('setNearbyAvatarSCCustom', [msgIndex])

    def __handleChatUpdateSCToontask(self,
                                     taskId, toNpcId, toonProgress, msgIndex):
        self.sendUpdate('setNearbyAvatarSCToontask',
                        [taskId, toNpcId, toonProgress, msgIndex])

    # network messages from the server
    def makeTurnToHeadingTrack(self, heading):
        curHpr = self.getHpr()
        destHpr = self.getHpr()
        destHpr.setX(heading)

        # make sure the dest heading is not more than 180
        # degrees from the cur heading
        if ((destHpr[0] - curHpr[0]) > 180.):
            destHpr.setX(destHpr[0] - 360)
        elif ((destHpr[0] - curHpr[0]) < -180.):
            destHpr.setX(destHpr[0] + 360)

        # figure out how long it should take for the character to turn
        turnSpeed = 180. # degrees/sec
        time = abs(destHpr[0] - curHpr[0])/turnSpeed

        # create a track
        turnTracks = Parallel()
        # don't animate if we don't need to turn much (or at all)
        if time > 0.2:
            turnTracks.append(
                Sequence(Func(self.loop, 'walk'),
                         Wait(time),
                         Func(self.loop, 'neutral'))
                )
        turnTracks.append(
            LerpHprInterval(self, time, destHpr,
                            name="lerp" + self.getName() + "Hpr")
            )
        return turnTracks

    def setChat(self, category, msg, avId):
        if self.cr.doId2do.has_key(avId):
            avatar = self.cr.doId2do[avId]
            chatter = CCharChatter.getChatter(self.getName(), self.getCCChatter())
            if category >= len(chatter):
                self.notify.debug("Chatter's changed")
                return
            elif len(chatter[category]) <= msg:
                self.notify.debug("Chatter's changed")
                return
            str = chatter[category][msg]
            if '%' in str:
                # make our own copy of the message
                str = copy.deepcopy(str)
                # get the avatar's name
                avName = avatar.getName()
                # slap it in
                str = string.replace(str, '%', avName)

            track = Sequence()

            # Character doesn't bother to turn to you when saying goodbye
            if category != CCharChatter.GOODBYE:
                # turn to face the avatar
                # calculate the destination hpr
                curHpr = self.getHpr()
                self.headsUp(avatar)
                destHpr = self.getHpr()
                self.setHpr(curHpr)
                track.append(self.makeTurnToHeadingTrack(destHpr[0]))

            #Change the animation for vampire mickey
            #if self == base.cr.doFind("vampire_mickey"):
            #    self.loop('chat')

            # chat flags are different for DL Donald
            if self.getName() == Donald or self.getName() == WesternPluto or self.getName() == Pluto:
                chatFlags = CFThought | CFTimeout
                
                # Make Pluto talk during April Toons' Week.
                if hasattr(base.cr, "newsManager") and base.cr.newsManager:
                    holidayIds = base.cr.newsManager.getHolidayIdList()
                    if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                        if self.getName() == Pluto:
                            chatFlags = CFTimeout | CFSpeech
                
            elif self.getName() == DonaldDock:
                chatFlags = CFTimeout | CFSpeech
                self.nametag3d.hide()
            else:
                chatFlags = CFTimeout | CFSpeech
                
            # Figure out appropriate audio file here, which will get used
            # in setChatAbsolute below
            # getChatterDialogue defined in Char.py so that chatter can
            # be loaded simultaneously with default char dialogue
            self.chatterDialogue = self.getChatterDialogue(category, msg)

            # make a track to say the message
            track.append(
                Func(self.setChatAbsolute, str, chatFlags, self.chatterDialogue)
                )

            self.chatTrack.finish()
            self.chatTrack = track
            self.chatTrack.start()

    def setWalk(self, srcNode, destNode, timestamp):
        # meant to be over-ridden by children that need walk notifications
        pass

    def walkSpeed(self):
        return 0.1

    def enableRaycast(self, enable=1):
        """
        enable/disable raycast, useful for when we know
        when the char will change elevations
        """
        if (not self.cTrav
                or not hasattr(self, "cRayNode")
                or not self.cRayNode):
            self.notify.debug("raycast info not found for " + self.getName())
            return

        self.cTrav.removeCollider(self.cRayNodePath)
        if enable:
            if self.notify.getDebug():
                self.notify.debug("enabling raycast for " + self.getName())
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        else:
            if self.notify.getDebug():
                self.notify.debug("disabling raycast for " + self.getName())

    def getCCLocation(self):
        return 0

    def getCCChatter(self):
        self.handleHolidays()
        return self.CCChatter
        
    def handleHolidays(self):           
        """        
        Handle Holiday specific behaviour        
        """         
        self.CCChatter = 0        
        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.CRASHED_LEADERBOARD in holidayIds:            
                self.CCChatter = ToontownGlobals.CRASHED_LEADERBOARD 
            elif ToontownGlobals.CIRCUIT_RACING_EVENT in holidayIds:            
                self.CCChatter = ToontownGlobals.CIRCUIT_RACING_EVENT  
            elif ToontownGlobals.WINTER_CAROLING in holidayIds:
                self.CCChatter = ToontownGlobals.WINTER_CAROLING
            elif ToontownGlobals.WINTER_DECORATIONS in holidayIds:
                self.CCChatter = ToontownGlobals.WINTER_DECORATIONS
            elif ToontownGlobals.VALENTINES_DAY in holidayIds:
                self.CCChatter = ToontownGlobals.VALENTINES_DAY
            elif ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                self.CCChatter = ToontownGlobals.APRIL_FOOLS_COSTUMES
            elif ToontownGlobals.SILLY_CHATTER_ONE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_ONE
            elif ToontownGlobals.SILLY_CHATTER_TWO in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_TWO
            elif ToontownGlobals.SILLY_CHATTER_THREE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_THREE
            elif ToontownGlobals.SILLY_CHATTER_FOUR in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.SILLY_CHATTER_FIVE in holidayIds:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR

    def fadeAway(self):
        fadeOut = self.colorScaleInterval( 0.5, Vec4(1, 1, 1, 0.5),
                                               startColorScale = Vec4(1, 1, 1, 1),
                                               blendType = 'easeInOut')
        fadeOut.start()
        self.loop("neutral")
        if(self.fsm):
            self.fsm.addState(State.State('TransitionToCostume',
                                            self.enterTransitionToCostume,
                                            self.exitTransitionToCostume,
                                            ['Off']))
            self.fsm.request("TransitionToCostume", force=1)
        self.ignoreAll()

    def enterTransitionToCostume(self):
        def getDustCloudIval():
            dustCloud = DustCloud.DustCloud(fBillboard=0,wantSound=1)
            dustCloud.setBillboardAxis(2.)
            dustCloud.setZ(4)
            dustCloud.setScale(0.6)
            dustCloud.createTrack()
            return Sequence(
                Func(dustCloud.reparentTo, self),
                dustCloud.track,
                Func(dustCloud.destroy),
                name = 'dustCloadIval'
                )

        dust = getDustCloudIval()
        dust.start()

    def exitTransitionToCostume(self):
        pass
