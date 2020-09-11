"""
AvatarDNA module: contains the methods and definitions for describing
multipart actors with a simple class
"""

#import whrandom
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

notify = directNotify.newCategory("AvatarDNA")

class AvatarDNA:
    """
    Contains methods for describing avatars with a
    simple class. The AvatarDNA class may be converted to lists of strings
    for network transmission. Also, AvatarDNA objects can be constructed
    from lists of strings recieved over the network. Some examples are in
    order.

        # create a toon from a network packet (list of strings)
        dna = AvatarDNA()
        dna.makeFromNetString(networkPacket)

    """
    # special methods
    
    def __str__(self):
        """
        Avatar DNA print method
        """
        return "avatar parent class: type undefined"

    # stringification methods
    def makeNetString(self):
        notify.error("called makeNetString on avatarDNA parent class")

    def printNetString(self):
        string = self.makeNetString()
        dg = PyDatagram(string)
        dg.dumpHex(ostream)
    
    def makeFromNetString(self, string):
        notify.error("called makeFromNetString on avatarDNA parent class")
    
    # dna methods

    def getType(self):
        """
        Return which type of actor this dna represents.
        """
        notify.error("Invalid DNA type: ", self.type)
        return type
