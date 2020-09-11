from otp.otpbase import OTPGlobals
from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from ElevatorConstants import *

from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.building import BoardingPartyBase
##from direct.showbase.PythonUtil import StackTrace

# these are array indexs
# since there are no structs
GROUPMEMBER = 0
GROUPINVITE = 1

class DistributedBoardingPartyAI(DistributedObjectAI.DistributedObjectAI, BoardingPartyBase.BoardingPartyBase):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBoardingPartyAI")
    
    def __init__(self, air, elevatorList, maxSize = 4):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        BoardingPartyBase.BoardingPartyBase.__init__(self)
        self.setGroupSize(maxSize)
        self.elevatorIdList = elevatorList # the elevators this boardingParty can send groups to
        if __debug__:
            simbase.bp = self #REMOVE ME
        self.visibleZones = [] #tells us which zones this works in, usually it's just one
        
    def delete(self):
        self.cleanup()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        for elevatorId in self.elevatorIdList:
            elevator = simbase.air.doId2do.get(elevatorId)
            elevator.setBoardingParty(self)
            
        store = simbase.air.dnaStoreMap.get(self.zoneId)
        if store:
            numVisGroups = store.getNumDNAVisGroupsAI()
            myVisGroup = None
            for index in range(numVisGroups):
                if store.getDNAVisGroupAI(index).getName() == str(self.zoneId):
                    myVisGroup = store.getDNAVisGroupAI(index)
                    
            if myVisGroup:
                numVisibles = myVisGroup.getNumVisibles()
                for index in range(numVisibles):
                    newVisible = myVisGroup.getVisibleName(index)
                    self.visibleZones.append(int(newVisible))
            else:
                self.visibleZones = [self.zoneId]
        else:
            self.visibleZones = [self.zoneId]
        
    def cleanup(self):
        BoardingPartyBase.BoardingPartyBase.cleanup(self)
        del self.elevatorIdList
        del self.visibleZones
        
    def getElevatorIdList(self):
        return self.elevatorIdList
        
    def setElevatorIdList(self, elevatorIdList):
        self.elevatorIdList = elevatorIdList
        
    def addWacthAvStatus(self, avId):
        """
        tells us when a toon has entered a battle, has changed 
        zones or disconnects. Anything that would cause them to
        leave the boardingParty, or keep the boardingParty from 
        going to a destination
        """
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.handleAvatarDisco, extraArgs=[avId])
        self.accept(self.staticGetLogicalZoneChangeEvent(avId),
                        self.handleAvatarZoneChange, extraArgs=[avId])
                        
        
        messageToonAdded = ("Battle adding toon %s" % (avId))
        self.accept(messageToonAdded, self.handleToonJoinedBattle)
        messageToonReleased = ("Battle releasing toon %s" % (avId))
        self.accept(messageToonReleased, self.handleToonLeftBattle)
        
    def handleToonJoinedBattle(self, avId):
        self.notify.debug("handleToonJoinedBattle %s" % (avId))
        
    def handleToonLeftBattle(self, avId):
        self.notify.debug("handleToonLeftBattle %s" % (avId))        
                        
    def removeWacthAvStatus(self, avId):
        self.ignore(self.air.getAvatarExitEvent(avId))
        self.ignore(self.staticGetLogicalZoneChangeEvent(avId))
    
    def requestInvite(self, inviteeId):
        self.notify.debug("requestInvite %s" % (inviteeId))
        inviterId = self.air.getAvatarIdFromSender()
        
        invitee = simbase.air.doId2do.get(inviteeId)
        # Send a reject to the inviter if the invitee is in a battle.
        if invitee and (invitee.battleId != 0):
            reason = BoardingPartyBase.BOARDCODE_BATTLE
            self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, 0])
            # Send a message to the invitee saying that inviter had tried to invite him.
            self.sendUpdateToAvatarId(inviteeId, "postMessageInvitationFailed", [inviterId])
            return
        
        # Send a reject to the inviter if the invitee is already in a boarding group.
        if self.hasActiveGroup(inviteeId):
            reason = BoardingPartyBase.BOARDCODE_DIFF_GROUP
            self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, 0])            
            # Send a message to the invitee saying that inviter had tried to invite him.
            self.sendUpdateToAvatarId(inviteeId, "postMessageInvitationFailed", [inviterId])            
            return
        
        # Send a reject to the inviter if the invitee has a pending invite.
        if self.hasPendingInvite(inviteeId):
            reason = BoardingPartyBase.BOARDCODE_PENDING_INVITE
            self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, 0])
            # Send a message to the invitee saying that inviter had tried to invite him.
            self.sendUpdateToAvatarId(inviteeId, "postMessageInvitationFailed", [inviterId])
            return
        
        # Send a reject to the inviter if the invitee has already boarded an elevator.
        if self.__isInElevator(inviteeId):
            reason = BoardingPartyBase.BOARDCODE_IN_ELEVATOR
            self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, 0])
            # Send a message to the invitee saying that inviter had tried to invite him.
            self.sendUpdateToAvatarId(inviteeId, "postMessageInvitationFailed", [inviterId])
            return
        
        inviteeOkay = self.checkBoard(inviteeId, self.elevatorIdList[0])
        reason = 0
        # Send a reject to the inviter if the invitee is not a paid member.
        if (inviteeOkay == REJECT_NOTPAID):
            reason = BoardingPartyBase.BOARDCODE_NOT_PAID
            self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, 0])
            return
        
        if len(self.elevatorIdList) == 1:
            if inviteeOkay:
                if (inviteeOkay == REJECT_MINLAFF):
                    reason = BoardingPartyBase.BOARDCODE_MINLAFF
                elif (inviteeOkay == REJECT_PROMOTION):
                    reason = BoardingPartyBase.BOARDCODE_PROMOTION
                # Send a reject to the inviter if the invitee does not qualify for the only elevator.
                self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviteeId, reason, self.elevatorIdList[0]])
                return
            else:
                inviterOkay = self.checkBoard(inviterId, self.elevatorIdList[0])
                if inviterOkay:
                    if (inviterOkay == REJECT_MINLAFF):
                        reason = BoardingPartyBase.BOARDCODE_MINLAFF
                    elif (inviterOkay == REJECT_PROMOTION):
                        reason = BoardingPartyBase.BOARDCODE_PROMOTION
                    # Send a reject to the inviter if the inviter does not qualify for the only elevator.
                    self.sendUpdateToAvatarId(inviterId, "postInviteNotQualify", [inviterId, reason, self.elevatorIdList[0]])
                    return
        
        if self.avIdDict.has_key(inviterId): #existing group
            self.notify.debug("old group")
            leaderId = self.avIdDict[inviterId]
            groupList = self.groupListDict.get(leaderId)
            if groupList:
                self.notify.debug("got group list")
                if inviterId == leaderId: #leader can unban players
                    if inviteeId in groupList[2]:
                        groupList[2].remove(inviteeId)
                        
                if (len(self.getGroupMemberList(leaderId))) >= self.maxSize:
                    self.sendUpdate("postSizeReject", [leaderId, inviterId, inviteeId])
                elif (not (inviterId in groupList[1])) and (not (inviterId in groupList[2])):
                    if not inviteeId in groupList[1]:
                        groupList[1].append(inviteeId)
                    self.groupListDict[leaderId] = groupList
                    
                    if self.avIdDict.has_key(inviteeId):
                        self.notify.warning('inviter %s tried to invite %s who already exists in the avIdDict.' %(inviterId, inviteeId))
                        self.air.writeServerEvent('suspicious: inviter', inviterId,' tried to invite %s who already exists in the avIdDict.' %inviteeId)
                    self.avIdDict[inviteeId] = leaderId
                    self.sendUpdateToAvatarId(inviteeId, "postInvite", [leaderId, inviterId])
                    # Send a message to all members in the group except the inviter that an invitation was sent out.
                    # Inviter doesn't need to get this message, because he knows that he sent out the invitation.
                    for memberId in groupList[0]:
                        if not (memberId == inviterId):
                            self.sendUpdateToAvatarId(memberId, "postMessageInvited", [inviteeId, inviterId])
                elif inviterId in groupList[2]:
                    self.sendUpdate("postKickReject", [leaderId, inviterId, inviteeId])
        else: #creating new Group with inviter as leader
            if self.avIdDict.has_key(inviteeId):
                self.notify.warning('inviter %s tried to invite %s who already exists in avIdDict.' %(inviterId, inviteeId))
                self.air.writeServerEvent('suspicious: inviter', inviterId,' tried to invite %s who already exists in the avIdDict.' %inviteeId)

            self.notify.debug("new group")
            leaderId = inviterId
            self.avIdDict[inviterId] = inviterId
            self.avIdDict[inviteeId] = inviterId
            self.groupListDict[leaderId] = [[leaderId],[inviteeId],[]]
            self.addWacthAvStatus(leaderId)
            self.sendUpdateToAvatarId(inviteeId, "postInvite", [leaderId, inviterId])
                        
    def requestCancelInvite(self, inviteeId):
        inviterId = self.air.getAvatarIdFromSender()
        if self.avIdDict.has_key(inviterId):
            leaderId = self.avIdDict[inviterId]
            groupList = self.groupListDict.get(leaderId)
            if groupList:
                self.removeFromGroup(leaderId, inviteeId)
                self.sendUpdateToAvatarId(inviteeId, "postInviteCanceled", [])
                    
    def requestAcceptInvite(self, leaderId, inviterId):
        inviteeId = self.air.getAvatarIdFromSender()
        self.notify.debug("requestAcceptInvite leader%s inviter%s invitee%s" % (leaderId, inviterId, inviteeId))
        
        if self.avIdDict.has_key(inviteeId):
            # Send reject to the invitee if the invitee is already in a boarding group
            if self.hasActiveGroup(inviteeId):
                self.sendUpdateToAvatarId(inviteeId, "postAlreadyInGroup", [])
                return
            
            # Reject this acceptance if the leader is not part of the group.
            if not self.avIdDict.has_key(leaderId) or not self.isInGroup(inviteeId, leaderId):
                self.sendUpdateToAvatarId(inviteeId, "postSomethingMissing", [])
                return
            
            memberList = self.getGroupMemberList(leaderId)
            if self.avIdDict[inviteeId]:
                # Don't do anything if the invitee already exists in the current leader's group.
                if self.avIdDict[inviteeId] == leaderId:
                    if inviteeId in memberList:
                        self.notify.debug("invitee already in group, aborting requestAcceptInvite")
                        return
                # If the invitee's leader is different, remove him from his old leader's group.
                else:
                    self.air.writeServerEvent('suspicious: ', inviteeId, " accepted a second invite from %s, in %s's group, while he was in alredy in %s's group." %(inviterId, leaderId, self.avIdDict[inviteeId]))
                    self.removeFromGroup(self.avIdDict[inviteeId], inviteeId, post = 0)
            
            # If the group has already become full, auto reject the invite
            if len(memberList) >= self.maxSize:
                self.removeFromGroup(leaderId, inviteeId)
                self.sendUpdateToAvatarId(inviterId, "postMessageAcceptanceFailed", [inviteeId, BoardingPartyBase.INVITE_ACCEPT_FAIL_GROUP_FULL])                
                self.sendUpdateToAvatarId(inviteeId, "postGroupAlreadyFull", [])
                return
        
            self.sendUpdateToAvatarId(inviterId, "postInviteAccepted", [inviteeId])
            self.addToGroup(leaderId, inviteeId)
            
        else:
            self.air.writeServerEvent('suspicious: ', inviteeId, " was invited to %s's group by %s, but the invitee didn't have an entry in the avIdDict." %(leaderId, inviterId))
            
    def requestRejectInvite(self, leaderId, inviterId):
        inviteeId = self.air.getAvatarIdFromSender()
        self.removeFromGroup(leaderId, inviteeId)
        self.sendUpdateToAvatarId(inviterId, "postInviteDelcined", [inviteeId])
        
    def requestKick(self, kickId):
        leaderId = self.air.getAvatarIdFromSender()
        if self.avIdDict.has_key(kickId):
            if self.avIdDict[kickId] == leaderId:
                self.removeFromGroup(leaderId, kickId, kick = 1)
                self.sendUpdateToAvatarId(kickId, "postKick", [leaderId])
                
    def requestLeave(self, leaderId):
        # player is leaving a group voluntarly
        memberId = self.air.getAvatarIdFromSender()
        if self.avIdDict.has_key(memberId):
            if leaderId == self.avIdDict[memberId]:
                self.removeFromGroup(leaderId, memberId)
##        else:
##            stack = StackTrace()
##            self.notify.warning('boarding_requestLeave: StackTrace: %s' %stack.compact())
                        
    def checkBoard(self, avId, elevatorId):
        """
        Checks boarding for elevator requirements and paid status.
        """
        elevator = simbase.air.doId2do.get(elevatorId)
        avatar = simbase.air.doId2do.get(avId)
        if avatar:
            if not (avatar.getGameAccess() == OTPGlobals.AccessFull):
                return REJECT_NOTPAID
            elif elevator:
                # Returns 0 if everything is OK.
                return elevator.checkBoard(avatar)
        # It'll come here only if either avatar or elevator was not found.
        return REJECT_BOARDINGPARTY
                
    def testBoard(self, leaderId, elevatorId, needSpace = 0):
        """
        tests boarding against everything, space optional depending on whether
        the leader pressed a goto button, or just got on the elevator
        """
        elevator = None
        boardOkay = BoardingPartyBase.BOARDCODE_MISSING
        avatarsFailingRequirements = []
        avatarsInBattle = []
        if elevatorId in self.elevatorIdList:
            elevator = simbase.air.doId2do.get(elevatorId)
        if elevator:
            if self.avIdDict.has_key(leaderId):
                if leaderId == self.avIdDict[leaderId]:
                    boardOkay = BoardingPartyBase.BOARDCODE_OKAY                    
                    for avId in self.getGroupMemberList(leaderId):
                        avatar = simbase.air.doId2do.get(avId)
                        if avatar: 
                            if (elevator.checkBoard(avatar) != 0):
                                if (elevator.checkBoard(avatar) == REJECT_MINLAFF):
                                    boardOkay = BoardingPartyBase.BOARDCODE_MINLAFF
                                elif (elevator.checkBoard(avatar) == REJECT_PROMOTION):
                                    boardOkay = BoardingPartyBase.BOARDCODE_PROMOTION
                                avatarsFailingRequirements.append(avId)
                            elif (avatar.battleId != 0):
                                boardOkay = BoardingPartyBase.BOARDCODE_BATTLE
                                avatarsInBattle.append(avId)
                    groupSize = len(self.getGroupMemberList(leaderId))
                    if (groupSize > self.maxSize):
                        boardOkay = BoardingPartyBase.BOARDCODE_SPACE
                    if needSpace:
                        if (groupSize > elevator.countOpenSeats()):
                            boardOkay = BoardingPartyBase.BOARDCODE_SPACE
                            
        if (boardOkay != BoardingPartyBase.BOARDCODE_OKAY):
            self.notify.debug("Something is wrong with the group board request")
            if (boardOkay == BoardingPartyBase.BOARDCODE_MINLAFF):
                self.notify.debug("An avatar did not meet the elevator laff requirements")
            if (boardOkay == BoardingPartyBase.BOARDCODE_PROMOTION):
                self.notify.debug("An avatar did not meet the elevator promotion requirements")
            elif (boardOkay == BoardingPartyBase.BOARDCODE_BATTLE):
                self.notify.debug("An avatar is in battle")
                        
        return (boardOkay, avatarsFailingRequirements, avatarsInBattle)
                
    def requestBoard(self, elevatorId):
        """
        The group leader has tried to enter the elevator, thereby requesting that 
        their group board.
        """
        wantDisableGoButton = False
        leaderId = self.air.getAvatarIdFromSender()
        elevator = None
        if elevatorId in self.elevatorIdList:
            elevator = simbase.air.doId2do.get(elevatorId)
        if elevator:
            if self.avIdDict.has_key(leaderId):
                if leaderId == self.avIdDict[leaderId]:
                    group = self.groupListDict.get(leaderId)
                    if group:
                        boardOkay, avatarsFailingRequirements, avatarsInBattle = self.testBoard(leaderId, elevatorId, needSpace = 1)    
                        if boardOkay == BoardingPartyBase.BOARDCODE_OKAY:
                            # Board the leader.
                            leader = simbase.air.doId2do.get(leaderId)
                            if leader:
                                elevator.partyAvatarBoard(leader)
                                wantDisableGoButton = True
                            # Board all the members except the leader.
                            for avId in group[0]:
                                if not (avId == leaderId): 
                                    avatar = simbase.air.doId2do.get(avId)
                                    if avatar:
                                        elevator.partyAvatarBoard(avatar, wantBoardingShow = 1)
                            self.air.writeServerEvent('boarding_elevator', self.zoneId, '%s; Sending avatars %s' %(elevatorId, group[0]))
                        else:
                            self.sendUpdateToAvatarId(leaderId, "postRejectBoard", [elevatorId, boardOkay, avatarsFailingRequirements, avatarsInBattle])
                            return
        if not wantDisableGoButton:
            self.sendUpdateToAvatarId(leaderId, "postRejectBoard", [elevatorId, BoardingPartyBase.BOARDCODE_MISSING, [], []])
    
    def testGoButtonRequirements(self, leaderId, elevatorId):
        """
        Test if the leader can take his memebers to the elevator destination.
        Return True if everything looks good.
        Send a reject to the leader and return False if somebody doesn't qualify.
        """
        if self.avIdDict.has_key(leaderId):
            if leaderId == self.avIdDict[leaderId]:
                if elevatorId in self.elevatorIdList:
                    elevator = simbase.air.doId2do.get(elevatorId)
                    if elevator:
                        boardOkay, avatarsFailingRequirements, avatarsInBattle = self.testBoard(leaderId, elevatorId, needSpace = 0)
                        if boardOkay == BoardingPartyBase.BOARDCODE_OKAY:
                            avList = self.getGroupMemberList(leaderId)
                            if 0 in avList:
                                avList.remove(0)
                            if not (leaderId in elevator.seats):
                                return True
                            else:
                                self.notify.warning('avId: %s has hacked his/her client.' %leaderId)
                                self.air.writeServerEvent('suspicious: ', leaderId, ' pressed the GO Button while inside the elevator.')
                        else:
                            self.sendUpdateToAvatarId(leaderId, "rejectGoToRequest", [elevatorId, boardOkay, avatarsFailingRequirements, avatarsInBattle])
        return False
    
    def requestGoToFirstTime(self, elevatorId):
        """
        The leader has pushed a GO Button. Do the initial check and respond only to the
        leader if everything is OK. 
        """
        callerId = self.air.getAvatarIdFromSender()
        if self.testGoButtonRequirements(callerId, elevatorId):
            self.sendUpdateToAvatarId(callerId, "acceptGoToFirstTime", [elevatorId])
                            
    def requestGoToSecondTime(self, elevatorId):
        """
        The leader has finished his GO Pre Show. Do the initial check and respond to 
        all the members of the group to start the GO show.
        """
        callerId = self.air.getAvatarIdFromSender()
        avList = self.getGroupMemberList(callerId)
        if self.testGoButtonRequirements(callerId, elevatorId):
            for avId in avList:
                self.sendUpdateToAvatarId(avId, "acceptGoToSecondTime", [elevatorId])
            THREE_SECONDS = 3.0
            taskMgr.doMethodLater(THREE_SECONDS, self.sendAvatarsToDestinationTask, 
                                  self.uniqueName('sendAvatarsToDestinationTask'), 
                                  extraArgs = [elevatorId, avList], 
                                  appendTask = True)

    def sendAvatarsToDestinationTask(self, elevatorId, avList, task):
        """
        This is the task that sends the avatars in the Boarding Group to go
        directly to the elevator destinvations after 3 seconds.
        """
        self.notify.debug('entering sendAvatarsToDestinationTask')
        if len(avList):
            if elevatorId in self.elevatorIdList:
                elevator = simbase.air.doId2do.get(elevatorId)
                if elevator:
                    self.notify.warning('Sending avatars %s' %avList)
                    boardOkay, avatarsFailingRequirements, avatarsInBattle = self.testBoard(avList[0], elevatorId, needSpace = 0)
                    if not (boardOkay == BoardingPartyBase.BOARDCODE_OKAY):
                        for avId in avatarsFailingRequirements:
                            self.air.writeServerEvent('suspicious: ', avId, ' failed requirements after the second go button request.')
                        for avId in avatarsInBattle:
                            self.air.writeServerEvent('suspicious: ', avId, ' joined battle after the second go button request.')
                    
                    self.air.writeServerEvent('boarding_go', self.zoneId, '%s; Sending avatars %s' %(elevatorId, avList))
                    elevator.sendAvatarsToDestination(avList)
        return Task.done
    
    def handleAvatarDisco(self, avId):
        self.notify.debug("handleAvatarDisco %s" % (avId))
        if self.avIdDict.has_key(avId):
            leaderId = self.avIdDict[avId]
            self.removeFromGroup(leaderId, avId)
            
    def handleAvatarZoneChange(self, avId, zoneNew, zoneOld):
        self.notify.debug("handleAvatarZoneChange %s new%s old%s bp%s" % (avId, zoneNew, zoneOld, self.zoneId))
        if zoneNew in self.visibleZones:#== self.zoneId:
            self.toonInZone(avId)
        elif self.avIdDict.has_key(avId):
            leaderId = self.avIdDict[avId] 
            self.removeFromGroup(leaderId, avId)
            
    def toonInZone(self, avId):
        """
        This should never be called, but if an avatar leaves and for some reason is 
        still in the boarding system (due to a bug), this tries to put them back in the 
        right group
        """
        #callerId = self.air.getAvatarIdFromSender()
        if self.avIdDict.has_key(avId):
            leaderId = self.avIdDict[avId]
            group = self.groupListDict.get(leaderId)
            if leaderId and group:
                self.notify.debug('Calling postGroupInfo from toonInZone')
##                self.sendUpdate("postGroupInfo", [leaderId, group[0], group[1], group[2]])

    def addToGroup(self, leaderId, inviteeId, post = 1):
        group = self.groupListDict.get(leaderId)
        if group:
            self.avIdDict[inviteeId] = leaderId
            if inviteeId in group[1]:
                group[1].remove(inviteeId)
            if not(inviteeId in group[0]):
                group[0].append(inviteeId)
                
            self.groupListDict[leaderId] = group
            
            if post:
                self.notify.debug('Calling postGroupInfo from addToGroup')
                self.sendUpdate("postGroupInfo", [leaderId, group[0], group[1], group[2]])
            self.addWacthAvStatus(inviteeId)
        else:
            #if the group wasn't found something has gone wrong
            #to mitigate this we post a group dissolve trying
            #to let the clients know that the group doesn't exist
            self.sendUpdate("postGroupDissolve",[leaderId, leaderId, [], 0])
        
    def removeFromGroup(self, leaderId, memberId, kick = 0, post = 1):
        self.notify.debug ("")
        self.notify.debug ("removeFromGroup leaderId %s memberId %s" % (leaderId, memberId))
        self.notify.debug ("Groups %s" % (self.groupListDict))
        self.notify.debug ("avDict %s" % (self.avIdDict))
        
        if not (self.avIdDict.has_key(leaderId)):
            # Dissolve the group if you can't find the leader.
            self.sendUpdate("postGroupDissolve",[memberId, leaderId, [], kick])
            if self.avIdDict.has_key(memberId):
                self.avIdDict.pop(memberId)
            return
        self.removeWacthAvStatus(memberId)
        group = self.groupListDict.get(leaderId)
        if group:
            if memberId in group[0]:
                group[0].remove(memberId)
            if memberId in group[1]:
                group[1].remove(memberId)
            if memberId in group[2]:
                group[2].remove(memberId)
                
            if kick:
                group[2].append(memberId)
        else:
##            # The group doesn't exist, something strange must have gone wrong.
##            # Remove this memberId from the avIdDict.
##            if post:
##                self.notify.debug("postGroupDissolve")
##                self.sendUpdate("postGroupDissolve",[memberId, leaderId, kick])
##            if self.avIdDict.has_key(memberId):
##                self.avIdDict.pop(memberId)
            return
        
        # Either the leader wants to leave or the group has only 1 member, so dissolve the group.
        if (memberId == leaderId) or (len(group[0]) < 2):
            if self.avIdDict.has_key(leaderId):
                self.avIdDict.pop(leaderId)
                # Remove all the pending invitees of this group from avIdDict
                for inviteeId in group[1]:
                    if self.avIdDict.has_key(inviteeId):
                        self.avIdDict.pop(inviteeId)
                        # Send a message to the invitee to remove the invitee message.
                        self.sendUpdateToAvatarId(inviteeId, "postInviteCanceled", [])
                
            dgroup = self.groupListDict.pop(leaderId)
            for dMemberId in dgroup[0]:
                if self.avIdDict.has_key(dMemberId):
                    self.avIdDict.pop(dMemberId)
            self.notify.debug("postGroupDissolve")
            # Adding the removed member to the list so that we can send this list to the clients.
            # This is done so that even the removed member is removed from the avIdDicts in all the clients.
            dgroup[0].insert(0, memberId)
            self.sendUpdate("postGroupDissolve",[memberId, leaderId, dgroup[0], kick])
        else:
            self.groupListDict[leaderId] = group
            if post:
                self.notify.debug('Calling postGroupInfo from removeFromGroup')
                self.sendUpdate("postGroupInfo", [leaderId, group[0], group[1], group[2]])
                
        if self.avIdDict.has_key(memberId):
            self.avIdDict.pop(memberId)
                                
        self.notify.debug("Remove from group END")
        self.notify.debug ("Groups %s" % (self.groupListDict))
        self.notify.debug ("avDict %s" % (self.avIdDict))
        self.notify.debug("")
        
    def informDestinationInfo(self, offset):
        '''
        This function is called from DistributedBoardingParty informing that a
        destination has been changed.
        '''
        leaderId = self.air.getAvatarIdFromSender()
        if (offset > len(self.elevatorIdList)):
            self.air.writeServerEvent('suspicious: ', leaderId, 'has requested to go to %s elevator which does not exist' %offset)
            return
        memberList = self.getGroupMemberList(leaderId)
        # Post this info to all the members.
        for avId in memberList:
            # No need to post it back to the leader.
            if (avId != leaderId):
                self.sendUpdateToAvatarId(avId, "postDestinationInfo", [offset])
                
    def __isInElevator(self, avId):
        """
        Returns True if the avatar is found in any elevator in that zone.
        Else returns False.
        """
        inElevator = False
        for elevatorId in self.elevatorIdList:
            elevator = simbase.air.doId2do.get(elevatorId)
            if elevator:
                if avId in elevator.seats:
                    inElevator = True
        return inElevator