from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.avatar import Avatar

"""
instantiate this class with an avatar Id and a callback,
and the callback will be called when the avatar is loaded.
NOTE: if there is a problem, the avatar will be "None"!
"""

class AvatarDetail:
    notify = directNotify.newCategory("AvatarDetail")
    #notify.setDebug(True)

    def __init__(self, doId, callWhenDone):
        #print("Getting avatar detail for %s from the DB" % doId)
        self.id = doId
        self.callWhenDone = callWhenDone
        self.enterQuery()

    def isReady(self):
        return true

    def getId(self):
        return self.id

    ##### Query state #####

    # We are waiting for detailed information on the avatar to return
    # from the server.
    
    def enterQuery(self):
        # We need to get a DistributedObject handle for the indicated
        # avatar.  Maybe we have one already, if the avatar is
        # somewhere nearby.
        self.avatar = base.cr.doId2do.get(self.id)
        if self.avatar != None and not self.avatar.ghostMode:
            self.createdAvatar = 0
            dclass=self.getDClass()
            self.__handleResponse(True, self.avatar, dclass)
        else:
            # Otherwise, we have to make one up just to hold the
            # detail query response.  This is less than stellar,
            # because it means we'll do a lot of extra work we don't
            # need (like loading up models and binding animations,
            # etc.), but it's not *too* horrible.
            self.avatar = self.createHolder()
            self.createdAvatar = 1
            self.avatar.doId = self.id

            # Now ask the server to tell us more about this avatar.
            dclass = self.getDClass()
            base.cr.getAvatarDetails(self.avatar, self.__handleResponse, dclass)
        
    def exitQuery(self):
        return true

    def createHolder(self):
        assert 0, "This must be defined by the subclass!"

    def getDClass(self):
        assert 0, "This must be defined by the subclass!"

    def __handleResponse(self, gotData, avatar, dclass):
        if (avatar != self.avatar):
            # This may be a query response coming back from a previous
            # request.  Ignore it.
            self.notify.warning("Ignoring unexpected request for avatar %s" % (avatar.doId))
            return
            
        if gotData:
            # We got a valid response.
            self.callWhenDone(self.avatar)
            del self.callWhenDone
        else:
            # No information available about the avatar.  This is an
            # unexpected error condition, but we go out of our way to
            # handle it gracefully.
            self.callWhenDone(None)
            del self.callWhenDone

