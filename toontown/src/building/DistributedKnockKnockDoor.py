"""
DistributedKnockKnockDoor module: contains the DistributedKnockKnockDoor
class, the client side representation of a DistributedKnockKnockDoorAI.
"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from KnockKnockJokes import *

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
import DistributedAnimatedProp
from toontown.distributed import DelayDelete
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil


class DistributedKnockKnockDoor(DistributedAnimatedProp.DistributedAnimatedProp):
    """
    The client side representation of a knock, knock door.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedKnockKnockDoor')

    def __init__(self, cr):
        """
        cr is a ClientRepository.
        constructor for the DistributedKnockKnockDoor
        """
        assert(self.debugPrint("__init()"))
        DistributedAnimatedProp.DistributedAnimatedProp.__init__(self, cr)
        self.fsm.setName('DistributedKnockKnockDoor')
        # self.generate will be called automatically.
        self.rimshot = None
        self.knockSfx = None

    def generate(self):
        """
        This method is called when the DistributedAnimatedProp is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        DistributedAnimatedProp.DistributedAnimatedProp.generate(self)
        self.avatarTracks=[]
        self.avatarId=0

    def announceGenerate(self):
        assert(self.debugPrint("announceGenerate()"))
        DistributedAnimatedProp.DistributedAnimatedProp.announceGenerate(self)
        self.accept("exitKnockKnockDoorSphere_"+str(self.propId),
                    self.exitTrigger)
        self.acceptAvatar()

    def disable(self):
        assert(self.debugPrint("disable()"))
        self.ignore("exitKnockKnockDoorSphere_"+str(self.propId))
        self.ignore("enterKnockKnockDoorSphere_"+str(self.propId))
        DistributedAnimatedProp.DistributedAnimatedProp.disable(self)
        assert(len(self.avatarTracks)==0)
        # self.delete() will automatically be called.

    def delete(self):
        assert(self.debugPrint("delete()"))
        DistributedAnimatedProp.DistributedAnimatedProp.delete(self)
        if self.rimshot:
            self.rimshot = None
        if self.knockSfx:
            self.knockSfx = None

    def acceptAvatar(self):
        self.acceptOnce(
            "enterKnockKnockDoorSphere_"+str(self.propId),
            self.enterTrigger)

    def setAvatarInteract(self, avatarId):
        assert(self.debugPrint("setAvatarInteract(avatarId=%s)" %(avatarId,)))
        DistributedAnimatedProp.DistributedAnimatedProp.setAvatarInteract(self, avatarId)

    def avatarExit(self, avatarId):
        assert(self.debugPrint("avatarExit(avatarId=%s)"%(avatarId,)))
        if avatarId == self.avatarId:
            for track in self.avatarTracks:
                track.finish()
                DelayDelete.cleanupDelayDeletes(track)
            self.avatarTracks=[]

    def knockKnockTrack(self, avatar, duration):
        if avatar == None:
            return None

        # NOTE: the use of this rimshot sfx (which is in phase_5)
        # means we better not have any knock knock doors in phase_4,
        # which is true now.
        self.rimshot = base.loadSfx("phase_5/audio/sfx/AA_heal_telljoke.mp3")
        self.knockSfx = base.loadSfx("phase_5/audio/sfx/GUI_knock_3.mp3")

        joke = KnockKnockJokes[self.propId%len(KnockKnockJokes)]

        # For a marketing contest we are putting user-submitted knock knock jokes on
        # the first side doors (on the left) of the three TTC streets.
        place = base.cr.playGame.getPlace()
        if place:
            zone = place.getZoneId()
            branch = ZoneUtil.getBranchZone(zone)

            if branch == ToontownGlobals.SillyStreet:
                if self.propId == 44:
                    joke = KnockKnockContestJokes[ToontownGlobals.SillyStreet]
            elif branch == ToontownGlobals.LoopyLane:
                if self.propId in KnockKnockContestJokes[ToontownGlobals.LoopyLane].keys():
                    joke = KnockKnockContestJokes[ToontownGlobals.LoopyLane][self.propId]
            elif branch == ToontownGlobals.PunchlinePlace:
                if self.propId == 1:
                    joke = KnockKnockContestJokes[ToontownGlobals.PunchlinePlace]
            elif branch == ToontownGlobals.PolarPlace:
                if self.propId in KnockKnockContestJokes[ToontownGlobals.PolarPlace].keys():
                    joke = KnockKnockContestJokes[ToontownGlobals.PolarPlace][self.propId]

        self.nametag = None
        self.nametagNP = None

        doorNP=render.find("**/KnockKnockDoorSphere_"+str(self.propId)+";+s")
        if doorNP.isEmpty():
            self.notify.warning("Could not find KnockKnockDoorSphere_%s" % (self.propId))
            return None

        self.nametag = NametagGroup()
        self.nametag.setAvatar(doorNP)
        self.nametag.setFont(ToontownGlobals.getToonFont())
        # nametag.setName must come after setFont().
        self.nametag.setName(TTLocalizer.DoorNametag)
        # Do not allow user to click on door nametag
        self.nametag.setActive(0)
        self.nametag.manage(base.marginManager)
        self.nametag.getNametag3d().setBillboardOffset(4)
        nametagNode = self.nametag.getNametag3d().upcastToPandaNode()
        self.nametagNP=render.attachNewNode(nametagNode)
        self.nametagNP.setName("knockKnockDoor_nt_"+str(self.propId))
        pos=doorNP.node().getSolid(0).getCenter()
        self.nametagNP.setPos(pos+Vec3(0, 0, avatar.getHeight()+2))
        d=duration*0.125
        track=Sequence(
                Parallel(
                    Sequence(Wait(d * 0.5), SoundInterval(self.knockSfx)),
                    Func(self.nametag.setChat, TTLocalizer.DoorKnockKnock, CFSpeech),
                    Wait(d)
                    ),
                Func(avatar.setChatAbsolute, TTLocalizer.DoorWhosThere, CFSpeech | CFTimeout,
                     openEnded = 0),
                Wait(d),
                Func(self.nametag.setChat, joke[0], CFSpeech),
                Wait(d),
                Func(avatar.setChatAbsolute, joke[0]+TTLocalizer.DoorWhoAppendix,
                     CFSpeech | CFTimeout,
                     openEnded = 0),
                Wait(d),
                Func(self.nametag.setChat, joke[1], CFSpeech),
                Parallel(
                    SoundInterval(self.rimshot, startTime = 2.0),
                    Wait(d*4),
                    ),
                Func(self.cleanupTrack)
                )
        track.delayDelete = DelayDelete.DelayDelete(avatar, 'knockKnockTrack')
        return track

    def cleanupTrack(self):
        avatar = self.cr.doId2do.get(self.avatarId, None)
        if avatar:
            avatar.clearChat()
        if self.nametag:
            self.nametag.unmanage(base.marginManager)
            self.nametagNP.removeNode()
        self.nametag = None
        self.nametagNP = None

    ##### off state #####

    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
        DistributedAnimatedProp.DistributedAnimatedProp.enterOff(self)

    def exitOff(self):
        assert(self.debugPrint("exitOff()"))
        DistributedAnimatedProp.DistributedAnimatedProp.exitOff(self)

    ##### attract state #####

    def enterAttract(self, ts):
        assert(self.debugPrint("enterAttract()"))
        DistributedAnimatedProp.DistributedAnimatedProp.enterAttract(self, ts)
        self.acceptAvatar()

    def exitAttract(self):
        assert(self.debugPrint("exitAttract()"))
        DistributedAnimatedProp.DistributedAnimatedProp.exitAttract(self)

    ##### playing state #####

    def enterPlaying(self, ts):
        assert(self.debugPrint("enterPlaying()"))
        DistributedAnimatedProp.DistributedAnimatedProp.enterPlaying(self, ts)
        if self.avatarId:
            # Start animation at time stamp:
            avatar = self.cr.doId2do.get(self.avatarId, None)
            track=self.knockKnockTrack(avatar, 8)
            if track != None:
                track.start(ts)
                self.avatarTracks.append(track)

    def exitPlaying(self):
        assert(self.debugPrint("exitPlaying()"))
        DistributedAnimatedProp.DistributedAnimatedProp.exitPlaying(self)
        for track in self.avatarTracks:
            track.finish()
            DelayDelete.cleanupDelayDeletes(track)
        self.avatarTracks=[]
        self.avatarId=0
