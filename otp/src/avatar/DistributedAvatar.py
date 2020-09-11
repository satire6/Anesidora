import time
import string

from pandac.PandaModules import *

from direct.distributed import DistributedNode
from direct.actor.DistributedActor import DistributedActor
from direct.task import Task
from direct.showbase import PythonUtil

from libotp import Nametag
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from otp.chat import ChatGarbler
from otp.chat import ChatManager

import random

from Avatar import Avatar
import AvatarDNA


class DistributedAvatar(DistributedActor, Avatar):
    # This is a text node used to create the numbers that appear over the
    # heads of the avatars.
    HpTextGenerator = TextNode("HpTextGenerator")

    # This is used to enable/disable the display of the hp numbers
    HpTextEnabled = 1

    # set this True so that we can start accepting nametagAmbientLightChanged in generate
    # and ignore it in disable
    ManagesNametagAmbientLightChanged = True

    def __init__(self, cr):
        """
        Handle distributed updates
        """
        try:
            self.DistributedAvatar_initialized
            return
        except:
            self.DistributedAvatar_initialized = 1

        Avatar.__init__(self)
        DistributedActor.__init__(self, cr)
        
        # The node that shows the number of hp just gained or lost
        self.hpText = None
        self.hp = None
        self.maxHp = None
        

    ### managing ActiveAvatars ###

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        try:
            del self.DistributedAvatar_announced
        except:
            return
        self.reparentTo(hidden)
        self.removeActive()
        self.disableBodyCollisions()
        self.hideHpText()
        # By setting hp to None, when the distributed avatar is "uncached",
        # and the hp gets set, it will be as if the avatar is new, and no
        # number will appear over his head. If we don't set this to None,
        # the setHp call might think that the number has changed and call
        # showHpText, which we don't want.
        self.hp = None
        self.ignore("nameTagShowAvId")
        self.ignore("nameTagShowName")
        
        DistributedActor.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        try:
            self.DistributedAvatar_deleted
        except:
            self.DistributedAvatar_deleted = 1
            Avatar.delete(self)
            DistributedActor.delete(self)

        
    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """

        DistributedActor.generate(self)
        if not self.isLocal():
            self.addActive()
            self.considerUnderstandable()

        # Initially, a DistributedAvatar is always parented to hidden
        # on generate, until we are told otherwise.
        self.setParent(OTPGlobals.SPHidden)

        # Now that we have a doId, set a tag so others who find us in
        # the collision system can figure out what avatar they hit.
        self.setTag('avatarDoId', str(self.doId))
        self.accept("nameTagShowAvId",self.__nameTagShowAvId)
        self.accept("nameTagShowName",self.__nameTagShowName)

    def announceGenerate(self):
        try:
            self.DistributedAvatar_announced
            return
        except:
            self.DistributedAvatar_announced = 1
        
        if(not self.isLocal()):
            self.initializeBodyCollisions("distAvatarCollNode-" + str(self.doId))
        
        DistributedActor.announceGenerate(self)
        
                
    def __setTags(self, extra = None):
        if hasattr(base, "idTags"):
            if base.idTags:
                self.__nameTagShowAvId()
            else:
                self.__nameTagShowName()
        
            

    ### setParent ###

    def do_setParent(self, parentToken):
        """do_setParent(self, int parentToken)

        This overrides a function defined in DistributedNode to
        reparent the node somewhere.  A DistributedAvatar wants to
        hide the onscreen nametag when the parent is hidden.
        """
        if not self.isDisabled():
            if parentToken == OTPGlobals.SPHidden:
                self.nametag2dDist &= ~Nametag.CName
            else:
                self.nametag2dDist |= Nametag.CName
            self.nametag.getNametag2d().setContents(
                self.nametag2dContents & self.nametag2dDist)
            DistributedActor.do_setParent(self, parentToken)
            self.__setTags()

    ### setHp ###

    def toonUp(self, hpGained):
        # WARNING This is extended in DistributedToon.py, please change that
        # as well if any changes are made here
        # Adjusts the avatar's hp upward by the indicated value
        # (limited by maxHp) and shows green numbers flying out of the
        # avatar's head.

        if self.hp == None or hpGained < 0:
            return

        oldHp = self.hp

        # If hp is below zero, it might mean we're at a timeout in the
        # playground, in which case we respect that it is below zero
        # until we get our head above water.  If our toonUp would
        # take us above zero, then we pretend we started at zero in
        # the first place, ignoring the timeout.
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = min(max(self.hp, 0) + hpGained, self.maxHp)

        hpGained = self.hp - max(oldHp, 0)
        if hpGained > 0:
            self.showHpText(hpGained)
            self.hpChange(quietly = 0)
        
    def takeDamage(self, hpLost, bonus=0):
        # Adjusts the avatar's hp downward by the indicated value
        # (limited by 0) and shows red numbers flying out of the
        # avatar's head.
        if self.hp == None or hpLost < 0:
            return
        
        oldHp = self.hp
        self.hp = max(self.hp - hpLost, 0)

        hpLost = oldHp - self.hp
        if hpLost > 0:
            self.showHpText(-hpLost, bonus)
            self.hpChange(quietly = 0)

            if self.hp <= 0 and oldHp > 0:
                self.died()       

    def setHp(self, hitPoints):
        # We no longer fly numbers out of the avatar's head just for
        # calling setHp().  Instead, toonUp() and takeDamage() divide
        # that responsibility, and setHp() is just used to quietly
        # reset the hp from the AI.
        
        justRanOutOfHp = (hitPoints is not None and
                          self.hp is not None and
                          self.hp - hitPoints > 0 and
                          hitPoints <= 0)

        # Store the new value.
        self.hp = hitPoints
        
        # Send events so that the hp meter and others can know about the
        # change to hp.
        self.hpChange(quietly = 1)

        if justRanOutOfHp:
            self.died()

    def hpChange(self, quietly = 0):
        # We may not have a doId yet... in which case we can't send the
        # event, and don't need to anyway.
        if hasattr(self, "doId"):
            if self.hp != None and self.maxHp != None:
                messenger.send(self.uniqueName("hpChange"), [self.hp, self.maxHp, quietly])
            if self.hp != None and self.hp > 0:
                messenger.send(self.uniqueName("positiveHP"))
        
    def died(self):
        """
        This is a hook for derived classes to do something when the
        avatar runs out of HP.  The base function doesn't do anything.
        """
        pass
    
    def getHp(self):
        return self.hp


    ### setMaxHp ###

    def setMaxHp(self, hitPoints):
        self.maxHp = hitPoints
        self.hpChange()

    def getMaxHp(self):
        return self.maxHp

    ### getName ###

    def getName(self):
        return(Avatar.getName(self))

    def setName(self, name):
        # Set the name of our top node, so it will be easy to identify
        # this avatar in the scene graph.
        try:
            self.node().setName("%s-%d" % (name, self.doId))
            self.gotName = 1
        except:
            # This might fail if the doId hasn't been set yet.
            # No big deal.
            pass
        
        
        return(Avatar.setName(self, name))

    ### hpText ####

    def showHpText(self, number, bonus=0, scale=1):
        # WARNING if this changes please also change DistributedToon.py
        if self.HpTextEnabled and not self.ghostMode:           
            # We don't show zero change.
            if number != 0:
                # Get rid of the number if it is already there.
                if self.hpText:
                    self.hideHpText()
                # Set the font
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                # Show both negative and positive signs
                if number < 0:
                    self.HpTextGenerator.setText(str(number))
                else:
                    self.HpTextGenerator.setText("+" + str(number))
                # No shadow
                self.HpTextGenerator.clearShadow()
                # Put a shadow on there
                #self.HpTextGenerator.setShadow(0.05, 0.05)
                #self.HpTextGenerator.setShadowColor(0, 0, 0, 1)
                # Center the number
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                # Red for negative, green for positive, yellow for bonus
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                elif bonus == 2:
                    r = 1.0
                    g = 0.5
                    b = 0
                    a = 1
                elif number < 0:
                    r = 0.9
                    g = 0
                    b = 0
                    a = 1
                else:
                    r = 0
                    g = 0.9
                    b = 0
                    a = 1

                self.HpTextGenerator.setTextColor(r, g, b, a)

                self.hpTextNode = self.HpTextGenerator.generate()
                
                # Put the hpText over the head of the avatar
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                # Make sure it is a billboard
                self.hpText.setBillboardPointEye()
                # Render it after other things in the scene.
                self.hpText.setBin('fixed', 100)

                # Initial position ... Center of the body... the "tan tien"
                self.hpText.setPos(0, 0, self.height/2)
                seq = Task.sequence(
                    # Fly the number out of the character
                    self.hpText.lerpPos(Point3(0, 0, self.height + 1.5),
                                            1.0,
                                            blendType = 'easeOut'),
                    # Wait 2 seconds
                    Task.pause(0.85),
                    # Fade the number
                    self.hpText.lerpColor(Vec4(r, g, b, a),
                                              Vec4(r, g, b, 0),
                                              0.1),
                    # Get rid of the number
                    Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName("hpText"))
        else:
            # Just play the sound effect.
            # TODO: Put in the sound effect!
            pass

    def showHpString(self, text, duration=0.85, scale=0.7):
        if self.HpTextEnabled and not self.ghostMode:
            # We don't show empty strings
            if text != '':
                # Get rid of text if it is already there.
                if self.hpText:
                    self.hideHpText()
                # Set the font
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                # Write the text
                self.HpTextGenerator.setText(text)
                # No shadow
                self.HpTextGenerator.clearShadow()
                # Put a shadow on there
                #self.HpTextGenerator.setShadow(0.05, 0.05)
                #self.HpTextGenerator.setShadowColor(0, 0, 0, 1)
                # Center the text
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                # Set the color and alpha scale (a)
                r = a = 1.0
                g = b = 0.0
                
                self.HpTextGenerator.setTextColor(r, g, b, a)

                self.hpTextNode = self.HpTextGenerator.generate()

                # Put the hpText over the head of the avatar
                self.hpText = self.attachNewNode(self.hpTextNode)
                # Set its scale
                self.hpText.setScale(scale)
                # Make sure it is a billboard
                self.hpText.setBillboardAxis()

                # Initial position ... Center of the body... the "tan tien"
                self.hpText.setPos(0, 0, self.height/2)
                seq = Task.sequence(
                    # Fly the number out of the character
                    self.hpText.lerpPos(Point3(0, 0, self.height + 1.5),
                                            1.0,
                                            blendType = 'easeOut'),
                    # Wait 2 seconds
                    Task.pause(duration),
                    # Fade the number
                    self.hpText.lerpColor(Vec4(r, g, b, a),
                                              Vec4(r, g, b, 0),
                                              0.1),
                    # Get rid of the number
                    Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName("hpText"))
        else:
            # Just play the sound effect.
            # TODO: Put in the sound effect!
            pass

    def hideHpTextTask(self, task):
        self.hideHpText()
        return Task.done

    def hideHpText(self):
        if self.hpText:
            taskMgr.remove(self.uniqueName("hpText"))
            self.hpText.removeNode()
            self.hpText = None

    def getStareAtNodeAndOffset(self):
        return self, Point3(0,0,self.height)
        
    def getAvIdName(self):
        # Derived classes can override the base.idTags display.
        return "%s\n%s" % (self.getName(), self.doId)
    
    def __nameTagShowAvId(self, extra = None):
        self.setDisplayName(self.getAvIdName())
        
    def __nameTagShowName(self, extra = None):
        self.setDisplayName(self.getName())
        
    def askAvOnShard(self, avId):
        #determines if a given avId in on my shard
        if base.cr.doId2do.get(avId):
            #print("Found Locally")
            messenger.send("AvOnShard%s"%(avId), [True])
        else:
            #print("asking AI")
            self.sendUpdate("checkAvOnShard", [avId])
        
    def confirmAvOnShard(self, avId, onShard = True):
        messenger.send(("AvOnShard%s"%(avId)), [onShard])
        
    ### play dialog sounds ###

    def getDialogueArray(self):
        # Inheritors should override
        return None


