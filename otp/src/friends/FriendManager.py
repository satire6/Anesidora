from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals

class FriendManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendManager")

    # We should never disable this guy.
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.__available = 0
        
        # used for flexible request processing
        # in toontown we are keeping a queue of friends requests and processing them
        # once the avatar is available again
        self.gameSpecificFunction = None

    ### Interface methods ###

    def setAvailable(self, available):
        """setAvailable(self, bool available)

        Sets the 'available' flag.  When this is true, the client is
        deemed to be available to consider friendship requests, and
        they will be allowed through.  When this is false, the client
        is deemed to be too busy to consider friendship requests, and
        they will be sent back.
        """
        self.__available = available
        if self.__available and self.gameSpecificFunction:
            self.gameSpecificFunction()

    def getAvailable(self):
        return self.__available
        
    def setGameSpecificFunction(self, function):
        self.gameSpecificFunction = function
        
    def executeGameSpecificFunction(self):
        if self.__available and self.gameSpecificFunction:
            self.gameSpecificFunction()
        


    ### DistributedObject methods ###

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        if base.cr.friendManager != None:
            base.cr.friendManager.delete()
        base.cr.friendManager = self
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        #self.notify.warning("Hey!  The FriendManager was disabled!")
        base.cr.friendManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        #self.notify.warning("Hey!  The FriendManager was deleted!")
        self.gameSpecificFunction = None
        base.cr.friendManager = None
        DistributedObject.DistributedObject.delete(self)


    ### Messages sent from inviter client to AI

    def up_friendQuery(self, inviteeId):
        """friendQuery(self, int inviteeId)

        Sent by the inviter to the AI to initiate a friendship
        request.
        """
        self.sendUpdate('friendQuery', [inviteeId])
        self.notify.debug("Client: friendQuery(%d)" % (inviteeId))

    def up_cancelFriendQuery(self, context):
        """cancelFriendQuery(self, int context)

        Sent by the inviter to the AI to cancel a pending friendship
        request.
        """

        self.sendUpdate('cancelFriendQuery', [context])
        self.notify.debug("Client: cancelFriendQuery(%d)" % (context))


    ### Messages sent from invitee client to AI

    def up_inviteeFriendConsidering(self, yesNo, context):
        """inviteeFriendConsidering(self, bool yesNo, int context)

        Sent by the invitee to the AI to indicate whether the invitee
        is able to consider the request right now.

        The responses are:
          0 - no
          1 - yes
          4 - the invitee is ignoring you.
          6 - invitee not accepting new friends
        """

        self.sendUpdate('inviteeFriendConsidering', [yesNo, context])
        self.notify.debug("Client: inviteeFriendConsidering(%d, %d)" % (yesNo, context))

    def up_inviteeFriendResponse(self, yesNoMaybe, context):
        """inviteeFriendResponse(self, int yesNoMaybe, int context)

        Sent by the invitee to the AI, following an affirmitive
        response in inviteeFriendConsidering, to indicate whether or
        not the user decided to accept the friendship.

        The responses are:
          0 - no
          1 - yes
          2 - unable to answer; e.g. entered a minigame or something.
          3 - the invitee has too many friends already.
        """

        self.sendUpdate('inviteeFriendResponse', [yesNoMaybe, context])
        self.notify.debug("Client: inviteeFriendResponse(%d, %d)" % (yesNoMaybe, context))

    def up_inviteeAcknowledgeCancel(self, context):
        """inviteeAcknowledgeCancel(self, int context)

        Sent by the invitee to the AI, in response to an
        inviteeCancelFriendQuery message.  This simply acknowledges
        receipt of the message and tells the AI that it is safe to
        clean up the context.
        """

        self.sendUpdate('inviteeAcknowledgeCancel', [context])
        self.notify.debug("Client: inviteeAcknowledgeCancel(%d)" % (context))



    ### Messages sent from AI to inviter client

    def friendConsidering(self, yesNoAlready, context):
        """friendConsidering(self, int yesNoAlready, int context)

        Sent by the AI to the inviter client to indicate whether the
        invitee is able to consider the request right now.

        The responses are:
          0 - no
          1 - yes
          2 - the invitee is already your friend
          3 - attempt to befriend yourself
          4 - the invitee is ignoring you.
          6 - the invitee is not accepting friends.
        """

        self.notify.info("Roger Client: friendConsidering(%d, %d)" % (yesNoAlready, context))

        messenger.send('friendConsidering', [yesNoAlready, context])

    def friendResponse(self, yesNoMaybe, context):
        """friendResponse(self, bool yesNoMaybe, int context)

        Sent by the AI to the inviter client, following an affirmitive
        response in friendConsidering, to indicate whether or not the
        user decided to accept the friendship.

        The responses are:
          0 - no
          1 - yes
          2 - unable to answer; e.g. entered a minigame or something.
          3 - the invitee has too many friends already.
        """

        self.notify.debug("Client: friendResponse(%d, %d)" % (yesNoMaybe, context))
        messenger.send('friendResponse', [yesNoMaybe, context])



    ### Messages sent from AI to invitee client

    def inviteeFriendQuery(self, inviterId, inviterName, inviterDna, context):
        """inviteeFriendQuery(self, int inviterId, inviterName, inviterDna,
                              int context)

        Sent by the AI to the invitee client to initiate a friendship
        request from the indiciated inviter.  The invitee client
        should respond immediately with inviteeFriendConsidering, to
        indicate whether the invitee is able to consider the
        invitation right now.
        """

        self.notify.debug("Client: inviteeFriendQuery(%d, %s, dna, %d)" % (inviterId, inviterName, context))

        # Immediately send a response back that indicates whether we
        # can consider the invitation.

        if not hasattr(base, "localAvatar"):
            # client is closing down... tell the AI 'no'
            self.up_inviteeFriendConsidering(0, context)
            return

        if inviterId in base.localAvatar.ignoreList:
            # We're ignoring this naughty person
            self.up_inviteeFriendConsidering(4, context)
            return

        if (not base.localAvatar.acceptingNewFriends):
            self.up_inviteeFriendConsidering(6, context)
            return

        self.up_inviteeFriendConsidering(self.__available, context)

        # And consider the invitation if we can.
        if self.__available:
            messenger.send('friendInvitation', [inviterId, inviterName,
                                                inviterDna, context])

    def inviteeCancelFriendQuery(self, context):
        """inviteeCancelFriendQuery(self, int context)

        Sent by the AI to the invitee client to initiate that the
        inviter has rescinded his/her previous invitation by clicking
        the cancel button.
        """

        self.notify.debug("Client: inviteeCancelFriendQuery(%d)" % (context))
        messenger.send('cancelFriendInvitation', [context])
        self.up_inviteeAcknowledgeCancel(context)


    ### Messages involving secrets

    def up_requestSecret(self):
        """
        Sent by the client to the AI to request a new "secret" for the
        user.
        """
        self.notify.warning("Sending Request")        
        self.sendUpdate('requestSecret', [])

    def requestSecretResponse(self, result, secret):
        """requestSecret(self, int8 result, string secret)

        Sent by the AI to the client in response to requestSecret().
        result is one of:

          0 - Too many secrets outstanding.  Try again later.
          1 - Success.  The new secret is supplied.

        """
        messenger.send('requestSecretResponse', [result, secret])


    def up_submitSecret(self, secret):
        """submitSecret(self, string secret)

        Sent by the client to the AI to submit a "secret" typed in by
        the user.
        """
        self.sendUpdate('submitSecret', [secret])

    def submitSecretResponse(self, result, avId):
        """submitSecret(self, int8 result, int32 avId)

        Sent by the AI to the client in response to submitSecret().
        result is one of:

          0 - Failure.  The secret is unknown or has timed out.
          1 - Success.  You are now friends with the indicated avId.
          2 - Failure.  One of the avatars has too many friends already.
          3 - Failure.  You just used up your own secret.

        """
        messenger.send('submitSecretResponse', [result, avId])
        
    # Be invited by another avatar to be their friend.

