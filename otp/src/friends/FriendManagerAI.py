## from otp.ai.AIBaseGlobal import *
## from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
## from direct.directnotify import DirectNotifyGlobal
## from otp.avatar import DistributedAvatarAI

# all of this is commented out because the friend manager was moved
# to the OTP server

# we need something for the AI DC parser to load
class FriendManagerAI(DistributedObjectAI.DistributedObjectAI):
    pass
##     # These structures record the invitations currently being handled.
##     nextContext = 0
##     invites = {}
##     inviters = {}
##     invitees = {}

##     # This is the length of time, in seconds, to sit on a secret guess
##     # before processing it.  This serves to make it difficult to guess
##     # passwords at random.
##     SecretDelay = 1.0

##     # This is the length of time that should elapse before we start to
##     # forget who has declined friendships from whom.
##     DeclineFriendshipTimeout = 600.0

##     notify = DirectNotifyGlobal.directNotify.newCategory("FriendManagerAI")

##     # This subclass is used to record currently outstanding
##     # in-the-game invitation requests.
##     class Invite:
##         def __init__(self, context, inviterId, inviteeId):
##             self.context = context
##             self.inviterId = inviterId
##             self.inviteeId = inviteeId
##             self.inviter = None
##             self.invitee = None
##             self.inviteeKnows = 0
##             self.sendSpecialResponse = 0

##     def __init__(self, air):
##         DistributedObjectAI.DistributedObjectAI.__init__(self, air)

##         # We maintain two maps of toons who have declined
##         # friendships.  We add entries to map1, and every ten
##         # minutes, we roll map1 into map2.  This provides a
##         # timeout of ten to twenty minutes for a particular
##         # rejection, and also prevents the maps from growing very
##         # large in memory.
##         self.declineFriends1 = {}
##         self.declineFriends2 = {}
##         self.lastRollTime = 0

##     def generate(self):
##         DistributedObjectAI.DistributedObjectAI.generate(self)

##         # The FriendManagerAI always listens for these events, which
##         # will be sent in response to secret requests to the database,
##         # via the AIR.
##         self.accept("makeFriendsReply", self.makeFriendsReply)
##         self.accept("requestSecretReply", self.__requestSecretReply)
##         self.accept("submitSecretReply", self.__submitSecretReply)

##     def delete(self):
##         self.ignore("makeFriendsReply")
##         self.ignore("requestSecretReply")
##         self.ignore("submitSecretReply")

##         # Clean up all outstanding secret request tasks.
##         taskMgr.removeTasksMatching("secret-*")

##         DistributedObjectAI.DistributedObjectAI.delete(self)


##     ### Messages sent from inviter client to AI

##     def friendQuery(self, inviteeId):
##         """friendQuery(self, int inviterId, int inviteeId)

##         Sent by the inviter to the AI to initiate a friendship
##         request.
##         """
##         inviterId = self.air.getAvatarIdFromSender()
##         invitee = self.air.doId2do.get(inviteeId)

##         # see if the inviteeId is valid
##         if not invitee: 
##             self.air.writeServerEvent('suspicious', inviteeId, 'FriendManagerAI.friendQuery not on list')
##             return
        
##         self.notify.debug("AI: friendQuery(%d, %d)" % (inviterId, inviteeId))
##         self.newInvite(inviterId, inviteeId)

##     def cancelFriendQuery(self, context):
##         """cancelFriendQuery(self, int context)

##         Sent by the inviter to the AI to cancel a pending friendship
##         request.
##         """

##         avId = self.air.getAvatarIdFromSender()
##         self.notify.debug("AI: cancelFriendQuery(%d)" % (context))

##         try:
##             invite = FriendManagerAI.invites[context]
##         except:
##             # The client might legitimately try to cancel a context
##             # that has already been cancelled.
##             #self.air.writeServerEvent('suspicious', avId, 'FriendManagerAI.cancelFriendQuery unknown context')
##             #FriendManagerAI.notify.warning('Message for unknown context ' + `context`)
##             return

##         self.cancelInvite(invite)


##     ### Messages sent from invitee client to AI

##     def inviteeFriendConsidering(self, response, context):
##         """inviteeFriendConsidering(self, int response, int context)

##         Sent by the invitee to the AI to indicate whether the invitee
##         is able to consider the request right now.

##         The responses are:
##           0 - no
##           1 - yes
##           4 - the invitee is ignoring you.
##         """
##         self.notify.debug("AI: inviteeFriendConsidering(%d, %d)" % (response, context))
##         avId = self.air.getAvatarIdFromSender()

##         try:
##             invite = FriendManagerAI.invites[context]
##         except:
##             self.air.writeServerEvent('suspicious', avId, 'FriendManagerAI.inviteeFriendConsidering unknown context')
##             FriendManagerAI.notify.warning('Message for unknown context ' + `context`)
##             return

##         if response == 1:
##             self.inviteeAvailable(invite)
##         else:
##             self.inviteeUnavailable(invite, response)

##     def inviteeFriendResponse(self, yesNoMaybe, context):
##         """inviteeFriendResponse(self, int yesNoMaybe, int context)

##         Sent by the invitee to the AI, following an affirmative
##         response in inviteeFriendConsidering, to indicate whether or
##         not the user decided to accept the friendship.
##         """

##         self.notify.debug("AI: inviteeFriendResponse(%d, %d)" % (yesNoMaybe, context))
##         avId = self.air.getAvatarIdFromSender()

##         try:
##             invite = FriendManagerAI.invites[context]
##         except:
##             self.air.writeServerEvent('suspicious', avId, 'FriendManagerAI.inviteeFriendResponse unknown context')
##             FriendManagerAI.notify.warning('Message for unknown context ' + `context`)
##             return

##         if yesNoMaybe == 1:
##             self.makeFriends(invite)
##         else:
##             self.noFriends(invite, yesNoMaybe)

##     def inviteeAcknowledgeCancel(self, context):
##         """inviteeAcknowledgeCancel(self, int context)

##         Sent by the invitee to the AI, in response to an
##         inviteeCancelFriendQuery message.  This simply acknowledges
##         receipt of the message and tells the AI that it is safe to
##         clean up the context.
##         """

##         self.notify.debug("AI: inviteeAcknowledgeCancel(%d)" % (context))
##         avId = self.air.getAvatarIdFromSender()

##         try:
##             invite = FriendManagerAI.invites[context]
##         except:
##             # The client might legitimately try to cancel a context
##             # that has already been cancelled.
##             #self.air.writeServerEvent('suspicious', avId, 'FriendManagerAI.inviteeAcknowledgeCancel unknown context')
##             #FriendManagerAI.notify.warning('Message for unknown context ' + `context`)
##             return

##         self.clearInvite(invite)


##     ### Messages sent from AI to inviter client

##     def down_friendConsidering(self, recipient, yesNoAlready, context):
##         """friendConsidering(self, DistributedObject recipient,
##                              int yesNoAlready, int context)

##         Sent by the AI to the inviter client to indicate whether the
##         invitee is able to consider the request right now.

##         The responses are:
##         # 0 - the invitee is busy
##         # 2 - the invitee is already your friend
##         # 3 - the invitee is yourself
##         # 4 - the invitee is ignoring you.
##         # 6 - the invitee not accepting friends
##         """

##         self.sendUpdateToAvatarId(recipient, "friendConsidering", [yesNoAlready, context])
##         self.notify.debug("AI: friendConsidering(%d, %d)" % (yesNoAlready, context))

##     def down_friendResponse(self, recipient, yesNoMaybe, context):
##         """friendResponse(self, DistributedOBject recipient,
##                           int yesNoMaybe, int context)

##         Sent by the AI to the inviter client, following an affirmitive
##         response in friendConsidering, to indicate whether or not the
##         user decided to accept the friendship.
##         """

##         self.sendUpdateToAvatarId(recipient, "friendResponse", [yesNoMaybe, context])
##         self.notify.debug("AI: friendResponse(%d, %d)" % (yesNoMaybe, context))



##     ### Messages sent from AI to invitee client

##     def down_inviteeFriendQuery(self, recipient, inviterId, inviterName,
##                                 inviterDna, context):
##         """inviteeFriendQuery(self, DistributedObject recipient,
##                               int inviterId, string inviterName,
##                               AvatarDNA inviterDna, int context)

##         Sent by the AI to the invitee client to initiate a friendship
##         request from the indiciated inviter.  The invitee client
##         should respond immediately with inviteeFriendConsidering, to
##         indicate whether the invitee is able to consider the
##         invitation right now.
##         """

##         self.sendUpdateToAvatarId(recipient, "inviteeFriendQuery",
##                                [inviterId, inviterName,
##                                 inviterDna.makeNetString(), context])
##         self.notify.debug("AI: inviteeFriendQuery(%d, %s, dna, %d)" % (inviterId, inviterName, context))

##     def down_inviteeCancelFriendQuery(self, recipient, context):
##         """inviteeCancelFriendQuery(self, DistributedObject recipient,
##                                     int context)

##         Sent by the AI to the invitee client to initiate that the
##         inviter has rescinded his/her previous invitation by clicking
##         the cancel button.
##         """

##         self.sendUpdateToAvatarId(recipient, "inviteeCancelFriendQuery", [context])
##         self.notify.debug("AI: inviteeCancelFriendQuery(%d)" % (context))



##     ### Messages involving secrets

##     def requestSecret(self):
##         """requestSecret(self)

##         Sent by the client to the AI to request a new "secret" for the
##         user.
##         """
##         avId = self.air.getAvatarIdFromSender()
##         self.air.requestSecret(avId)

##     def down_requestSecretResponse(self, recipient, result, secret):
##         """requestSecret(self, int8 result, string secret)

##         Sent by the AI to the client in response to requestSecret().
##         result is one of:

##           0 - Too many secrets outstanding.  Try again later.
##           1 - Success.  The new secret is supplied.

##         """
##         self.sendUpdateToAvatarId(recipient, 'requestSecretResponse', [result, secret])

##     def submitSecret(self, secret):
##         """submitSecret(self, string secret)

##         Sent by the client to the AI to submit a "secret" typed in by
##         the user.
##         """
##         avId = self.air.getAvatarIdFromSender()

##         # We have to sit on this request for a few seconds before
##         # processing it.  This delay is solely to discourage password
##         # guessing.
##         taskName = "secret-" + str(avId)
##         taskMgr.remove(taskName)
##         if FriendManagerAI.SecretDelay:
##             taskMgr.doMethodLater(FriendManagerAI.SecretDelay,
##                                   self.continueSubmission,
##                                   taskName,
##                                   extraArgs = (avId, secret))
##         else:
##             # No delay
##             self.continueSubmission(avId, secret)

##     def continueSubmission(self, avId, secret):
##         """continueSubmission(self, avId, secret)
##         Finishes the work of submitSecret, a short time later.
##         """
##         self.air.submitSecret(avId, secret)

##     def down_submitSecretResponse(self, recipient, result, avId):
##         """submitSecret(self, int8 result, int32 avId)

##         Sent by the AI to the client in response to submitSecret().
##         result is one of:

##           0 - Failure.  The secret is unknown or has timed out.
##           1 - Success.  You are now friends with the indicated avId.
##           2 - Failure.  One of the avatars has too many friends already.
##           3 - Failure.  You just used up your own secret.

##         """
##         self.sendUpdateToAvatarId(recipient, 'submitSecretResponse', [result, avId])


##     ### Support methods

##     def newInvite(self, inviterId, inviteeId):
##         context = FriendManagerAI.nextContext
##         FriendManagerAI.nextContext += 1

##         invite = FriendManagerAI.Invite(context, inviterId, inviteeId)
##         FriendManagerAI.invites[context] = invite

##         # If the invitee has previously (recently) declined a
##         # friendship from this inviter, don't ask again.
##         previous = self.__previousResponse(inviteeId, inviterId)
##         if previous != None:
##             self.inviteeUnavailable(invite, previous + 10)
##             return

##         # If the invitee is presently being invited by someone else,
##         # we don't even have to bother him.
##         if FriendManagerAI.invitees.has_key(inviteeId):
##             self.inviteeUnavailable(invite, 0)
##             return

##         if invite.inviterId == invite.inviteeId:
##             # You can't be friends with yourself.
##             self.inviteeUnavailable(invite, 3)
##             return

##         # If the inviter is already involved in some other context,
##         # that one is now void.
##         if FriendManagerAI.inviters.has_key(inviterId):
##             self.cancelInvite(FriendManagerAI.inviters[inviterId])

##         FriendManagerAI.inviters[inviterId] = invite
##         FriendManagerAI.invitees[inviteeId] = invite

##         #self.air.queryObject(inviteeId, self.gotInvitee, invite)
##         #self.air.queryObject(inviterId, self.gotInviter, invite)
##         invite.inviter = self.air.doId2do.get(inviterId)
##         invite.invitee = self.air.doId2do.get(inviteeId)
##         if invite.inviter and invite.invitee:
##             self.beginInvite(invite)


## #    def gotInviter(self, handle, invite):
## #        if not invite.inviter:
## #            invite.inviter = handle
## #        if invite.invitee:
## #            self.beginInvite(invite)

## #    def gotInvitee(self, handle, invite):
## #        if not invite.invitee:
## #            invite.invitee = handle
## #        if invite.inviter:
## #            self.beginInvite(invite)

##     def beginInvite(self, invite):
##         # Ask the invitee if he is available to consider being
##         # someone's friend--that is, that he's not busy playing a
##         # minigame or something.

##         invite.inviteeKnows = 1
##         self.down_inviteeFriendQuery(invite.inviteeId, invite.inviterId,
##                                      invite.inviter.getName(),
##                                      invite.inviter.dna, invite.context)

##     def inviteeUnavailable(self, invite, code):
##         # Cannot make the request for one of these reasons:
##         #
##         # 0 - the invitee is busy
##         # 2 - the invitee is already your friend
##         # 3 - the invitee is yourself
##         # 4 - the invitee is ignoring you.
##         # 6 - the invitee not accepting friends
##         self.down_friendConsidering(invite.inviterId, code, invite.context)

##         # That ends the invitation.
##         self.clearInvite(invite)

##     def inviteeAvailable(self, invite):
##         # The invitee is considering our friendship request.
##         self.down_friendConsidering(invite.inviterId, 1, invite.context)


##     def noFriends(self, invite, yesNoMaybe):
##         # The invitee declined to make friends.
##         #
##         # 0 - no
##         # 2 - unable to answer; e.g. entered a minigame or something.
##         # 3 - the invitee has too many friends already.

##         if yesNoMaybe == 0 or yesNoMaybe == 3:
##             # The user explictly said no or has too many friends.
##             # Disallow this guy from asking again for the next ten
##             # minutes or so.

##             if not self.declineFriends1.has_key(invite.inviteeId):
##                 self.declineFriends1[invite.inviteeId] = {}
##             self.declineFriends1[invite.inviteeId][invite.inviterId] = yesNoMaybe

##         self.down_friendResponse(invite.inviterId, yesNoMaybe, invite.context)
##         self.clearInvite(invite)

##     def makeFriends(self, invite):
##         # The invitee agreed to make friends.
##         self.air.makeFriends(invite.inviteeId, invite.inviterId, 0,
##                              invite.context)
##         self.down_friendResponse(invite.inviterId, 1, invite.context)
##         # The reply will clear the context out when it comes in.

##     def makeSpecialFriends(self, requesterId, avId):
##         # The "requester" has typed in a codeword that successfully
##         # matches a friend in the world.  Attempt to make the
##         # friendship (with chat permission), and send back a code
##         # indicating success or failure.

##         # Get a special Invite structure just for this purpose.
##         context = FriendManagerAI.nextContext
##         FriendManagerAI.nextContext += 1

##         invite = FriendManagerAI.Invite(context, requesterId, avId)
##         FriendManagerAI.invites[context] = invite

##         invite.sendSpecialResponse = 1

##         self.air.makeFriends(invite.inviteeId, invite.inviterId, 1,
##                              invite.context)

##     def clearInvite(self, invite):
##         try:
##             del FriendManagerAI.invites[invite.context]
##         except:
##             pass

##         try:
##             del FriendManagerAI.inviters[invite.inviterId]
##         except:
##             pass

##         try:
##             del FriendManagerAI.invitees[invite.inviteeId]
##         except:
##             pass

##     def cancelInvite(self, invite):
##         if invite.inviteeKnows:
##             self.down_inviteeCancelFriendQuery(invite.inviteeId, invite.context)

##         invite.inviteeKnows = 0


##     def makeFriendsReply(self, result, context):
##         try:
##             invite = FriendManagerAI.invites[context]
##         except:
##             FriendManagerAI.notify.warning('Message for unknown context ' + `context`)
##             return

##         if result:
##             # By now, the server has OK'ed the friends transaction.
##             # Update our internal bookkeeping so we remember who's
##             # friends with whom.  This is mainly useful for correct
##             # accounting of the make-a-friend quest.
##             invitee = self.air.doId2do.get(invite.inviteeId)
##             inviter = self.air.doId2do.get(invite.inviterId)
##             if invitee != None:
##                 invitee.extendFriendsList(invite.inviterId, invite.sendSpecialResponse)
##                 self.air.questManager.toonMadeFriend(invitee, inviter)

##             #inviter = self.air.doId2do.get(invite.inviterId)
##             if inviter != None:
##                 inviter.extendFriendsList(invite.inviteeId, invite.sendSpecialResponse)
##                 self.air.questManager.toonMadeFriend(inviter, invitee)

##         if invite.sendSpecialResponse:
##             # If this flag is set, the "invite" was generated via the
##             # codeword system, instead of through the normal path.  In
##             # this case, we need to send the acknowledgement back to
##             # the client.

##             if result:
##                 # Success!  Send a result code of 1.
##                 result = 1
##             else:
##                 # Failure, some friends list problem.  Result code of 2.
##                 result = 2

##             self.down_submitSecretResponse(invite.inviterId, result,
##                                            invite.inviteeId)

##             # Also send a notification to the other avatar, if he's on.
##             avatar = DistributedAvatarAI.DistributedAvatarAI(self.air)
##             avatar.doId = invite.inviteeId
##             avatar.d_friendsNotify(invite.inviterId, 2)

##         self.clearInvite(invite)



##     def __requestSecretReply(self, result, secret, requesterId):
##         self.notify.debug("request secret result = %d, secret = '%s', requesterId = %d" % (result, secret, requesterId))
##         self.down_requestSecretResponse(requesterId, result, secret)


##     def __submitSecretReply(self, result, secret, requesterId, avId):
##         self.notify.debug("submit secret result = %d, secret = '%s', requesterId = %d, avId = %d" % (result, secret, requesterId, avId))
##         if result == 1:
##             # We successfully matched the secret, so we should do a
##             # few more sanity checks and then try to make friends.
##             if avId == requesterId:
##                 # This is the requester's own secret!
##                 result = 3
##             else:
##                 # Ok, make us special friends.
##                 self.makeSpecialFriends(requesterId, avId)

##                 # In this case, the response gets sent after the
##                 # friends transaction completes.
##                 return

##         self.down_submitSecretResponse(requesterId, result, avId)

##     def __previousResponse(self, inviteeId, inviterId):
##         # Return the previous rejection code if this invitee has
##         # previously (recently) declined a friendship from this
##         # inviter, or None if there was no previous rejection.

##         now = globalClock.getRealTime()
##         if now - self.lastRollTime >= self.DeclineFriendshipTimeout:
##             self.declineFriends2 = self.declineFriends1
##             self.declineFriends1 = {}

##         # Now, is the invitee/inviter combination present in either
##         # map?
##         previous = None
##         if self.declineFriends1.has_key(inviteeId):
##             previous = self.declineFriends1[inviteeId].get(inviterId)
##             if previous != None:
##                 return previous

##         if self.declineFriends2.has_key(inviteeId):
##             previous = self.declineFriends2[inviteeId].get(inviterId)
##             if previous != None:
##                 return previous

##         # Nope, go ahead and ask.
##         return None
