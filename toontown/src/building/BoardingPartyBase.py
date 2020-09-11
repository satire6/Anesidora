from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownGlobals
import copy

# elevator boarding codes

BOARDCODE_OKAY = 1
BOARDCODE_MISSING = 0
BOARDCODE_MINLAFF = -1
BOARDCODE_PROMOTION = -2
BOARDCODE_BATTLE = -3
BOARDCODE_SPACE = -4
BOARDCODE_NOT_PAID = -5
BOARDCODE_DIFF_GROUP = -6
BOARDCODE_PENDING_INVITE = -7
BOARDCODE_IN_ELEVATOR = -8

INVITE_ACCEPT_FAIL_GROUP_FULL = -1

class BoardingPartyBase:
    
    def __init__(self):
        self.groupListDict = {} #key->leaderId : [members],[invitees],[banned]
        self.avIdDict = {} #pointer from each member to a leaderId
        
    def cleanup(self):
        del self.groupListDict
        del self.avIdDict 
        
    def getGroupSize(self):
        return self.maxSize
        
    def setGroupSize(self, groupSize):
        self.maxSize = groupSize
        
    def getGroupLeader(self, avatarId):
        if self.avIdDict.has_key(avatarId):
            leaderId = self.avIdDict[avatarId]
            return leaderId
        else:
            return None
        
    def isGroupLeader(self, avatarId):
        leaderId = self.getGroupLeader(avatarId)
        if (avatarId == leaderId):
            return True
        else:
            return False
        
    def getGroupMemberList(self, avatarId):
        """
        returns the memberlist with the leader at index 0
        """
        if self.avIdDict.has_key(avatarId):
            leaderId = self.avIdDict[avatarId]
            group = self.groupListDict.get(leaderId)
            if group:
                returnList = copy.copy(group[0])
                if 0 in returnList:
                    returnList.remove(0)
                return returnList
        return []
            
    def getGroupInviteList(self, avatarId):
        if self.avIdDict.has_key(avatarId):
            leaderId = self.avIdDict[avatarId]
            group = self.groupListDict.get(leaderId)
            if group:
                returnList = copy.copy(group[1])
                if 0 in returnList:
                    returnList.remove(0)
                return returnList
        return []
            
    def getGroupKickList(self, avatarId):
        if self.avIdDict.has_key(avatarId):
            leaderId = self.avIdDict[avatarId]
            group = self.groupListDict.get(leaderId)
            if group:
                returnList = copy.copy(group[2])
                if 0 in returnList:
                    returnList.remove(0)
                return returnList
        return []
    
    def hasActiveGroup(self, avatarId):
        """
        Returns True if the avatar has an active boarding group.
        """
        memberList = self.getGroupMemberList(avatarId)
        if avatarId in memberList:
            if (len(memberList) > 1):
                return True
        return False
        
    def hasPendingInvite(self, avatarId):
        """
        This is a two-stage check:
        If the avatar is a leader just check if there is anyone in the leader's invite list.
        If the avatar is a non-leader just check if the avatar is there in it's leader's invite list.
        """
        pendingInvite = False
        if self.avIdDict.has_key(avatarId):
            leaderId = self.avIdDict[avatarId]
            leaderInviteList = self.getGroupInviteList(leaderId)
            if (leaderId == avatarId):
                # The avatar is the leader, just check if there is anybody in the invite list.
                if len(leaderInviteList):
                    pendingInvite = True
                else:
                    pendingInvite = False
            else:
                # The avatar is a non-leader, check if the avatar is there is the leader's invite list.
                if avatarId in leaderInviteList:
                    pendingInvite = True
                else:
                    pendingInvite = False
        if pendingInvite:
            return True
        else:
            return False
        
    def isInGroup(self, memberId, leaderId):
        """
        Returns True if the member is in the leader's member list or invite list.
        Else returns False.
        """
        if (memberId in self.getGroupMemberList(leaderId)) or (memberId in self.getGroupInviteList(leaderId)):
            return True
        else:
            return False