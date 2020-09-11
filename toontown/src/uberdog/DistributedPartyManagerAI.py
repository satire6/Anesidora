import random
import sys
import time
from sets import Set

from direct.showbase.PythonUtil import Functor
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from otp.distributed import OtpDoGlobals
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyAI import DistributedPartyAI
from toontown.parties.PartyInfo import PartyInfoAI
from toontown.ai import RepairAvatars
from toontown.toonbase import ToontownGlobals

class DistributedPartyManagerAI(DistributedObjectAI):
    """AI side class for the party manager."""
    
    notify = directNotify.newCategory("DistributedPartyManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)    
        self.accept("avatarEntered", self.handleAvatarEntered)        
        
        self.allowUnreleased= False
        self.canBuy = True # change this to True when boarding has had time on test
        self.avIdToPartyZoneId = {}
        self.hostAvIdToPartiesRunning = {} # hostAvId to DistributedPartyAIs
        self.hostAvIdToAllPartiesInfo = {} # hostAvId to ( public party start time, shardId, zoneId, isPrivate, number of toons there, hostName, activityIds, partyId)
        self.avIdEnteringPartyToHostIdZoneId = {} # avIds of toons entering a party to (hostId, zoneId)
        self.zoneIdToGuestAvIds = {} # zoneId to list of guest avIds at that party
        self.zoneIdToHostAvId = {} # Zone id's mapped to party host Id's
        self.hostAvIdToClosingPartyZoneId = {}
        self.hostIdToPlanningPartyZoneId = {} # Used for security checks when freeing zones that were used for planning

        # Number of seconds between spontaneous heals
        self.healFrequency = 30 # seconds

    def generate(self):
        """We have zone info but not required fields, register for the special."""
        # PARTY_MANAGER_UD_TO_ALL_AI will arrive on this channel
        self.air.registerForChannel(OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER)
        DistributedObjectAI.generate(self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        # tell uberdog we are starting up, so we can get info on the currently running public parties
        # do whatever other sanity checks is necessary here
        self.air.sendUpdateToDoId("DistributedPartyManager",
                                  'partyManagerAIStartingUp',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                   [self.doId, self.air.districtId]
                                  )
        goingDownDg = self.air.createDgUpdateToDoId("DistributedPartyManager",
                                  'partyManagerAIGoingDown',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                   [self.doId, self.air.districtId]
                                  )
        if goingDownDg:
            self.air.addPostSocketClose(goingDownDg)

            

    def handleAvatarEntered(self, avatar):
        """A toon just logged in, check his party information."""
        DistributedPartyManagerAI.notify.debug( "handleAvatarEntered" )
        #self.air.sendUpdateToDoId("DistributedPartyManager",
        #                      'avatarLoggedIn',
        #                      OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
        #                      [avatar.doId])

    def partyUpdate(self, avId):
        """Force uberdog to resend all party related info from databases."""
        DistributedPartyManagerAI.notify.debug( "partyUpdate" )
        self.sendUpdate('avatarLoggedIn', [avId])

    def sendAddParty(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds, costOfParty):
        """Pass add party request up to uberdog."""
        DistributedPartyManagerAI.notify.debug( "sendAddParty" )
        self.air.sendUpdateToDoId("DistributedPartyManager",
                              'addParty',
                              OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                              [self.doId, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds, costOfParty])
        # Set up a failsafe incase uberdog has crashed...
        taskMgr.doMethodLater(
            5.0,
            self.addPartyResponseUdToAi,
            "NoResponseFromUberdog_%d_%d"%(self.doId,hostId),
            [hostId,PartyGlobals.AddPartyErrorCode.DatabaseError,0]
        )   
            
    def addPartyRequest(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        """Add a new party."""
        DistributedPartyManagerAI.notify.debug( "addPartyRequest" )
        validPartyRequest = True
        senderId = self.air.getAvatarIdFromSender()
        toonSender = simbase.air.doId2do.get(senderId)
        if not toonSender:
            # the toon is not on our district, let the party manager on that district handle it
            DistributedPartyManagerAI.notify.debug('addPartyRequest toon %d is not in our district' % senderId)
            return
        
        if hostId != senderId:
            # really bad, potential hacker
            self.air.writeServerEvent('suspicious', senderId,
                                      'trying to create party but not host : hostId = %d' % hostId)
            validPartyRequest = False

        if validPartyRequest:
            validPartyRequest, costOfPartyOrError = self.validatePartyAndReturnCost(hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds)

        # assuming all is well, send this to uberdog, otherwise respond back immediately
        if validPartyRequest:
            actList = []
            for actTuple in activities:
                actList.append(actTuple[0])
            decList = []
            for decTuple in decorations:
                decList.append(decTuple[0])
            self.air.writeServerEvent("party_buy_attempt", hostId, "act=%s dec=%s" % ( str(actList), str(decList)))
            self.sendAddParty(hostId, startTime,endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds, costOfPartyOrError)
        else:
            DistributedPartyManagerAI.notify.debug('inValid party because : %s' % costOfPartyOrError)
            self.sendAddPartyResponse(hostId, PartyGlobals.AddPartyErrorCode.ValidationError)

    def validatePartyAndReturnCost(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        DistributedPartyManagerAI.notify.debug( "validatePartyAndReturnCost" )
        # First, check to see if this is his only party that isn't cancelled or
        # finished.
        host = simbase.air.doId2do[hostId]
        if not host.canPlanParty():
            return (False,"Other Parties")                
        
        # TODO-parties : We need to validate startTime and endTime to make sure
        #                they are valid strings, or will sql do that?
        try:
            startTm = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            if PartyGlobals.MaxPlannedYear < startTm.tm_year:
                return (False,"Start time too far in the future")
            elif startTm.tm_year < PartyGlobals.MinPlannedYear:
                return (False,"Start time too far in the future")
        except ValueError:
            return (False, "Can't parse startTime")

        try:
            endTm = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            if PartyGlobals.MaxPlannedYear < endTm.tm_year:
                return (False,"End time too far in the future")
            elif endTm.tm_year < PartyGlobals.MinPlannedYear:
                return (False,"End time too far in the future")
        except ValueError:
            return (False, "Can't parse endTime")        
        
        if isPrivate not in (0,1):
            return (False,"Invalid isPrivate %s" % isPrivate)
        
        if inviteTheme not in PartyGlobals.InviteTheme:
            return (False,"Invalid inviteTheme %s" % inviteTheme)
            
        if hasattr(simbase.air, "holidayManager"):
            if ToontownGlobals.VALENTINES_DAY not in simbase.air.holidayManager.currentHolidays:           
                if inviteTheme == PartyGlobals.InviteTheme.Valentoons:
                    return (False,"Invalid inviteTheme %s" % inviteTheme)
            if ToontownGlobals.VICTORY_PARTY_HOLIDAY not in simbase.air.holidayManager.currentHolidays:           
                if inviteTheme == PartyGlobals.InviteTheme.VictoryParty:
                    return (False,"Invalid inviteTheme %s" % inviteTheme)

        costOfParty = 0
        activitiesUsedDict = {}
        usedGridSquares = {} # key is a tuple (x,y), value isn't that important
        actSet = Set([])
        for activityTuple in activities:
            if activityTuple[0] not in PartyGlobals.ActivityIds:
                return (False,"Invalid activity id %s"%activityTuple[0])
            
            activityId = activityTuple[0]

            # Check for holiday restrictions.
            if activityId in PartyGlobals.VictoryPartyActivityIds:
                if not simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.VICTORY_PARTY_HOLIDAY):
                    return (False, "Can't add activity %s during Victory Party " %activityId)
            if activityId in PartyGlobals.VictoryPartyReplacementActivityIds:
                if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.VICTORY_PARTY_HOLIDAY):
                    return (False, "Can't add activity %s during Victory Party " %activityId)
            
            actSet.add(activityTuple[0])
            if activitiesUsedDict.has_key(activityTuple[0]):
                activitiesUsedDict[activityTuple[0]] += 1
            else:
                activitiesUsedDict[activityTuple[0]] = 1
            costOfParty += PartyGlobals.ActivityInformationDict[activityTuple[0]]["cost"]
            if activityTuple[1] < 0 or activityTuple[1] >= PartyGlobals.PartyEditorGridSize[0]:
                return (False,"Invalid activity x %s"%activityTuple[1])
            if activityTuple[2] < 0 or activityTuple[2] >= PartyGlobals.PartyEditorGridSize[1]:
                return (False,"Invalid activity y %s"%activityTuple[2])
            if activityTuple[3] < 0 or activityTuple[3] > 255:
                return (False,"Invalid activity h %s"%activityTuple[3])
            # check for unreleased activity
            if activityTuple[0] in PartyGlobals.UnreleasedActivityIds:
                self.air.writeServerEvent('suspicious', hostId, "trying to buy unreleased activity %s" %
                                          PartyGlobals.ActivityIds.getString(activityTuple[0]))
                self.notify.warning("%d trying to buy unreleased activity %s" %
                                    (hostId, PartyGlobals.ActivityIds.getString(activityTuple[0])))
                if not self.allowUnreleasedServer():
                    return (False, "Activity %s is not released" %
                            PartyGlobals.ActivityIds.getString(activityTuple[0]))
                
            # check if the grid squares are valid
            gridSize = PartyGlobals.ActivityInformationDict[activityId]["gridsize"]
            centerGridX = activityTuple[1]
            centerGridY = activityTuple[2]
            # y has 14 at the north side (top) of the party editor
            yRange = self.computeGridYRange(centerGridY, gridSize[1])
            xRange = self.computeGridXRange(centerGridX, gridSize[0])
            for curGridY in yRange:
                for curGridX in xRange:
                    squareToTest = (curGridX, curGridY)
                    if squareToTest in usedGridSquares:
                        self.notify.debug("activitities=%s decor=%s usedGridSquares=%s" %
                                          (str(activities),
                                           str(decorations),
                                           str(usedGridSquares)))
                        return (False, "Grid Square %s is used twice by %s and %s" %
                                (str(squareToTest),
                                 str(activityId),
                                 str(usedGridSquares[squareToTest])))
                    else:
                        usedGridSquares[squareToTest]="activity-%d"%activityId
        
        # Check to see if an activity is used too many times
        for id in PartyGlobals.ActivityIds:
            if activitiesUsedDict.has_key(id):
                if activitiesUsedDict[id] > PartyGlobals.ActivityInformationDict[id]["limitPerParty"]:
                    return (False,"Too many of activity %s"%id)

        # Check for mutually exclusive activities
        for mutuallyExclusiveTuples in PartyGlobals.MutuallyExclusiveActivities:
            mutSet = Set(mutuallyExclusiveTuples)
            inter = mutSet.intersection(actSet)
            if len(inter) > 1:
                return (False, "Mutuallly exclusive activites %s" % str(inter))

        decorationsUsedDict = {}
        for decorationTuple in decorations:
            decorId = decorationTuple[0]
            if decorId not in PartyGlobals.DecorationIds:
                return (False,"%s is not a valid decoration" % decorId)
            # Check if decorId is a holiday specific decoration.
            decorName = PartyGlobals.DecorationIds.getString(decorId)
            if (decorName == "HeartTarget") \
            or (decorName == "HeartBanner") \
            or (decorName == "FlyingHeart"):
                if not simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.VALENTINES_DAY):
                    return (False, "Can't add ValenToons decoration %s" % decorId)
            if decorId in PartyGlobals.VictoryPartyDecorationIds:
                if not simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.VICTORY_PARTY_HOLIDAY):
                    return (False, "Can't add Victory Party decoration %s" % decorId)
            elif decorId in PartyGlobals.VictoryPartyReplacementDecorationIds:
                if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.VICTORY_PARTY_HOLIDAY):
                    return (False, "Can't add decoration during Victory Party %s" % decorId)
            
            if decorationsUsedDict.has_key(decorationTuple[0]):
                decorationsUsedDict[decorationTuple[0]] += 1
            else:
                decorationsUsedDict[decorationTuple[0]] = 1
            costOfParty += PartyGlobals.DecorationInformationDict[decorationTuple[0]]["cost"]
            if decorationTuple[1] < 0 or decorationTuple[1] >= PartyGlobals.PartyEditorGridSize[0]:
                return (False,"Invalid decoration X %s" % decorationTuple[1])
            if decorationTuple[2] < 0 or decorationTuple[2] >= PartyGlobals.PartyEditorGridSize[1]:
                return (False,"Invalid decoration Y %s" % decorationTuple[2])
            if decorationTuple[3] < 0 or decorationTuple[3] > 255:
                return (False,"Invalid decoration H %s" % decorationTuple[3])
            # check for unreleased decoration
            if decorationTuple[0] in PartyGlobals.UnreleasedDecorationIds:
                self.air.writeServerEvent('suspicious', hostId, "trying to buy unreleased decoration %s" %
                                          PartyGlobals.DecorationIds.getString(decorationTuple[0]))
                self.notify.warning("%d trying to buy unreleased decoration %s" %
                                    (hostId, PartyGlobals.DecorationIds.getString(decorationTuple[0])))
                if not self.allowUnreleasedServer():
                    return (False, "Decoration %s is not released" %
                            PartyGlobals.DecorationIds.getString(decorationTuple[0]))
            # check if the grid squares are valid
            gridSize = PartyGlobals.DecorationInformationDict[decorId]["gridsize"]
            centerGridX = decorationTuple[1]
            centerGridY = decorationTuple[2]
            # y has 14 at the north side (top) of the party editor
            yRange = self.computeGridYRange(centerGridY, gridSize[1])
            xRange = self.computeGridXRange(centerGridX, gridSize[0])
            for curGridY in yRange:
                for curGridX in xRange:
                    squareToTest = (curGridX, curGridY)
                    if squareToTest in usedGridSquares:
                        self.notify.debug("activitities=%s decor=%s usedGridSquares=%s" %
                                          (str(activities),
                                           str(decorations),
                                           str(usedGridSquares)))
                        return (False, "decor Grid Square %s is used twice" % str(squareToTest))
                    else:
                        usedGridSquares[squareToTest]="decor-%d"%decorId
            
        # Check to see if a decoration is used too many times
        for id in PartyGlobals.DecorationIds:
            if decorationsUsedDict.has_key(id):
                if decorationsUsedDict[id] > PartyGlobals.DecorationInformationDict[id]["limitPerParty"]:
                    return (False,"Decoration %s used too many times." % id)

        # Can I afford this party, really?
        if costOfParty > host.getTotalMoney():
            return (False,"Party too expensive, cost = %d"%costOfParty)
        
        # Can't have parties that have 0 empty grid squares.
        if len(usedGridSquares) >= PartyGlobals.AvailableGridSquares:
            return (False,"Party uses %s grid squares." % len(usedGridSquares))
        
        # Wow, you passed all the tests I can think of, ship it!
        return (True, costOfParty)
    
    ####
    ## Grid range computation note:
    ## We must round with negative values otherwise for center=0, size=3, the 
    ## result will be [1, 0] when we expect [1, 0, -1].
    ##   The range without rounding: range(int(1.5), int(-1.5), -1)
    ##   The range with rounding:    range(int(1.5), int(-2), -1)
    ## Not a problem with center>=2 in this example:
    ##   The range without rounding: range(int(3.5), int(0.5), -1)
    ##   The range with rounding:    range(int(3.5), int(0), -1)
    ####
    
    def computeGridYRange(self, centerGridY, size):
        result = []
        if size == 1:
            result = [centerGridY]
        else:
            result =  range(int(centerGridY + size/2.0),
                            int(centerGridY - round(size/2.0)),
                            -1)

        # The result list should be the same size as given.
        assert len(result) == size, "Bad result range: c=%s s=%s result=%s" % (centerGridY, size, result)
        
        return result

    def computeGridXRange(self, centerGridX, size):
        result = []
        if size == 1:
            result = [centerGridX]
        else:
            result = range(int(centerGridX + size/2.0),
                           int(centerGridX - round(size/2.0)),
                           -1
                           )
        
        # The result list should be the same size as given.
        assert len(result) == size, "Bad result range: c=%s s=%s result=%s" % (centerGridX, size, result)
        
        return result
    

    def sendAddPartyResponse(self, hostId, errorCode):
        """Tell the client if he's add party request got accepted."""
        self.sendUpdateToAvatarId(hostId, "addPartyResponse", [hostId, errorCode])

    def markInviteReadButNotReplied(self, inviteKey):
        """Just flag the invite as read in the database."""
        self.air.sendUpdateToDoId("DistributedPartyManager",
                                  'markInviteAsReadButNotReplied',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                  [self.doId, inviteKey]
                                  )          

    def respondToInviteFromMailbox(self, context, inviteKey, newStatus, mailboxDoId):
        """Send invite response to uberdog."""
        DistributedPartyManagerAI.notify.debug( "respondToInvite" )
        senderId = self.air.getAvatarIdFromSender()
        toonSender = simbase.air.doId2do.get(senderId)
        if not toonSender:
            # the toon is not on our district, let the party manager on that district handle it
            DistributedPartyManagerAI.notify.debug('respondToInviteFromMailbox toon %d is not in our district' % senderId)
            return
        self.air.sendUpdateToDoId("DistributedPartyManager",
                                  'respondToInvite',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                  [self.doId, mailboxDoId, context, inviteKey, newStatus]
                                  )        

    def respondToInviteResponse(self, mailboxDoId, context, inviteKey,  retcode, newStatus):
        """UD responding to our invite change."""
        DistributedPartyManagerAI.notify.debug( "respondToInviteResponse" )
        mailboxAI = simbase.air.doId2do.get(mailboxDoId)
        if mailboxAI:
            if newStatus == PartyGlobals.InviteStatus.Rejected:
                mailboxAI.respondToRejectInviteCallback(context, inviteKey, retcode)
            else:
                mailboxAI.respondToAcceptInviteCallback(context, inviteKey, retcode)

    def addPartyResponseUdToAi(self, hostId, errorCode, costOfParty):
        """Handle uberdog responding to our addParty message."""
        taskMgr.remove("NoResponseFromUberdog_%d_%d"%(self.doId,hostId))
        if errorCode == PartyGlobals.AddPartyErrorCode.AllOk:
            host = simbase.air.doId2do.get(hostId)
            self.air.writeServerEvent("party_buy", hostId,"%d" % costOfParty)
            if host :
                host.takeMoney(costOfParty, bUseBank = True)
            else:
                #  Woah, did he just get a free party?  Someone
                # bought a party, and while the uberdog was putting it in the
                # database, they logged out... how can we make sure the money
                # gets taken out?
                self.deductMoneyFromOfflineToon(hostId, costOfParty)
                
        self.sendAddPartyResponse(hostId, errorCode)

    def changePrivateRequest(self, partyId, newPrivateStatus):
        """Handle the client requesting to make a party public/private."""
        senderId = self.air.getAvatarIdFromSender()
        toonSender = simbase.air.doId2do.get(senderId)
        if not toonSender:
            # the toon is not on our district, let the party manager on that district handle it
            DistributedPartyManagerAI.notify.debug('changePrivateRequest toon %d is not in our district' % senderId)
            return
        
        errorCode = self.partyFieldChangeValidate(partyId)
        if errorCode != PartyGlobals.ChangePartyFieldErrorCode.AllOk:
            # immediately say we have an error then return
            self.sendUpdateToAvatarId(senderId,'changePrivateResponse',
                            [partyId, newPrivateStatus, errorCode])
            return

        # do whatever other sanity checks is necessary here        
        self.air.sendUpdateToDoId("DistributedPartyManager",
                                  'changePrivateRequestAiToUd',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                   [self.doId, partyId, newPrivateStatus]
                                  )

    def partyFieldChangeValidate(self, partyId):
        """Do common validation when changing private and status fields for a party."""
        senderId = self.air.getAvatarIdFromSender()
        errorCode = PartyGlobals.ChangePartyFieldErrorCode.AllOk
        toon = simbase.air.doId2do.get(senderId)
        if not toon:
            # we don't have the toon for some reason
            errorCode = PartyGlobals.ChangePartyFieldErrorCode.ValidationError
            return errorCode

        hostingThisParty = False
        for party in toon.hostedParties:
            if partyId == party.partyId:
                hostingThisParty = True
                break
            
        if not hostingThisParty:
            # the toon is not hosting this partyId
            # really bad, potential hacker
            self.air.writeServerEvent('suspicious', senderId,
                                      'trying to change field of party %s but not the host' % partyId)            
            errorCode = PartyGlobals.ChangePartyFieldErrorCode.ValidationError
            return errorCode

        if party.hostId != senderId:
            # really bad, potential hacker
            self.air.writeServerEvent('suspicious', senderId,
                                      'trying to change field of party %s but not the host' % partyId)
            errorCode = PartyGlobals.ChangePartyFieldErrorCode.ValidationError
            return errorCode

        return errorCode

    def changePrivateResponseUdToAi(self, hostId, partyId, newPrivateStatus, errorCode):
        """Handle the Uberdog telling us if the change private succeeded or not."""
        if errorCode == PartyGlobals.ChangePartyFieldErrorCode.AllOk:
            if self.air.doId2do.has_key(hostId):
                av = self.air.doId2do[hostId]
                for partyInfo in av.hostedParties:
                    if partyInfo.partyId == partyId:
                        partyInfo.isPrivate = newPrivateStatus
            if self.hostAvIdToAllPartiesInfo.has_key(hostId):
                self.hostAvIdToAllPartiesInfo[hostId][3] = newPrivateStatus
        
        self.sendUpdateToAvatarId(hostId, "changePrivateResponse", [partyId, newPrivateStatus, errorCode])
        
    def changePartyStatusRequest(self, partyId, newPartyStatus):
        """Handle the client requesting to change the party status."""
        senderId = self.air.getAvatarIdFromSender()
        toonSender = simbase.air.doId2do.get(senderId)
        if not toonSender:
            # the toon is not on our district, let the party manager on that district handle it
            DistributedPartyManagerAI.notify.debug('changePartyStatusRequest toon %d not in our district' % senderId)
            return                
        errorCode = self.partyFieldChangeValidate(partyId)
        if errorCode != PartyGlobals.ChangePartyFieldErrorCode.AllOk:
            # immediately say we have an error then return
            self.sendUpdateToAvatarId(senderId,'changePartyStatusResponse',
                            [partyId, newPartyStatus, errorCode, 0])
            return

        # do whatever other sanity checks is necessary here        
        self.air.sendUpdateToDoId("DistributedPartyManager",
                                  'changePartyStatusRequestAiToUd',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                                   [self.doId, partyId, newPartyStatus]
                                  )    
                                   
    def changePartyStatusResponseUdToAi(self, hostId, partyId, newPartyStatus, errorCode):
        """Handle the Uberdog telling us if the change partyStatus succeeded or not."""
        beansRefunded = 0
        if self.air.doId2do.has_key(hostId):
            av = self.air.doId2do[hostId]
            for partyInfo in av.hostedParties:
                if partyInfo.partyId == partyId:
                    partyInfo.status = newPartyStatus
                    if newPartyStatus == PartyGlobals.PartyStatus.Cancelled:
                        beansRefunded = self.getCostOfParty(partyInfo)
                        beansRefunded = int(PartyGlobals.PartyRefundPercentage * beansRefunded)
                        av.addMoney(beansRefunded)
                        self.air.writeServerEvent("party_cancel", hostId, "%d|%d|%d|%d" % (beansRefunded, partyId, newPartyStatus, errorCode))
        self.sendUpdateToAvatarId(hostId, "changePartyStatusResponse", [partyId, newPartyStatus, errorCode, beansRefunded])

    def getCostOfParty(self, partyInfo):
        newCost = 0
        for activityBase in partyInfo.activityList:
            newCost += PartyGlobals.ActivityInformationDict[activityBase.activityId]["cost"]
        for decorBase in partyInfo.decors:
            newCost += PartyGlobals.DecorationInformationDict[decorBase.decorId]["cost"]
        return newCost

    def getAllPublicParties(self):
        allParties = self.hostAvIdToAllPartiesInfo.values()
        allParties.sort()
        returnParties = []
        curGmTime = time.time()
        for partyInfo in allParties:
            # If the party is private, just continue, don't append it.
            if partyInfo[3]:
                continue
            # We want to return a list that has positive time and isPrivate
            minLeft = int( (PartyGlobals.DefaultPartyDuration *60)  - ( curGmTime - partyInfo[0]) / 60.0)
            if minLeft <= 0:
                continue
            returnParties.append(partyInfo[1:3] + partyInfo[4:7] + [minLeft]) 
        DistributedPartyManagerAI.notify.debug("getAllPublicParties : %s" % returnParties)
        return returnParties
    
    def updateToPublicPartyCountUdToAllAi(self, hostId, newCount):
        """
        The count has changed on a public party.
        """
        DistributedPartyManagerAI.notify.debug("updateToPublicPartyCountUdToAllAi : hostId=%s newCount=%s"%(hostId, newCount))
        if self.hostAvIdToAllPartiesInfo.has_key(hostId):
            self.hostAvIdToAllPartiesInfo[hostId][4] = newCount
    
    def partyHasFinishedUdToAllAi(self, hostId):
        """
        This party has finished, it may not have been mine, so just update my
        public party information.
        """
        if self.hostAvIdToAllPartiesInfo.has_key(hostId):
            del self.hostAvIdToAllPartiesInfo[hostId]

    def updateToPublicPartyInfoUdToAllAi(self, hostId, time, shardId, zoneId, isPrivate, numberOfGuests, hostName, activityIds, partyId):
        """
        There is an update to a public party, might not be on this AI so just
        update the public party information.
        """
        DistributedPartyManagerAI.notify.debug("updateToPublicPartyInfoUdToAllAi : hostId=%s time=%s shardId=%s zoneId=%s isPrivate=%s numberOfGuests=%s hostName=%s"%(hostId, time, shardId, zoneId, isPrivate, numberOfGuests, hostName))
        self.hostAvIdToAllPartiesInfo[hostId] = [time, shardId, zoneId, isPrivate, numberOfGuests, hostName, activityIds, partyId]

    def delete(self):
        DistributedPartyManagerAI.notify.debug("BASE: delete: deleting DistributedPartyManagerAI object")
        self.ignoreAll()
        DistributedObjectGlobalAI.DistributedObjectGlobalAI.delete(self)
        for party in self.hostAvIdToPartiesRunning.values():
            party.requestDelete()
        del self.avIdToPartyZoneId
        del self.hostAvIdToPartiesRunning
        del self.hostAvIdToAllPartiesInfo
        del self.avIdEnteringPartyToHostIdZoneId
        del self.zoneIdToGuestAvIds
        del self.zoneIdToHostAvId
        del self.hostAvIdToClosingPartyZoneId
        del self.hostIdToPlanningPartyZoneId

    ## -----------------------------------------------------------
    ## Zone allocation and enter code
    ## -----------------------------------------------------------

    # Gets the party zone based on the host's avatar ID
    def getPartyZone(self, hostId, zoneId, planningParty):
        DistributedPartyManagerAI.notify.debug("getPartyZone: hostId=%s zoneId=%s planningParty=%s" % (hostId, zoneId, planningParty))
        # Get the party the avatar is in.
        # If the party is running in this ai, and sender is allowed to go
        # (public or invited, and not full), then return the party zone.
        # If no party is running right now, and the sender is the avatar
        # Then look for the party info and check if he's the owner.
        # If he's the owner, then create the party, and return the created party zone
        # If he's not the owner, maybe he's got a valid zone already and he's
        # looking to join a party coming from a public party gate
        # Otherwise fail
        
        senderId = self.air.getAvatarIdFromSender()

        # If we're planning a party, we need to give them a zone to plan in, but
        # we don't need to create a DistributedParty/AI and add them to all the
        # dictionaries.
        if planningParty:
            if hostId != senderId:
                self.air.writeServerEvent('suspicious', senderId, 'trying to plan party but not host : hostId = %d' % hostId)
                self.__sendNoPartyZoneToClient(senderId)
                return
            # let's allocate a zone for the client to plan the party in
            zoneId = self.air.allocateZone()
            # We'll need to free it later, and we want to make sure we're freeing
            # the right zone, so let's remember it.
            self.hostIdToPlanningPartyZoneId[senderId] = zoneId
            DistributedPartyManagerAI.notify.debug("getPartyZone : Avatar %s is planning party in zone %s" % (senderId, zoneId))
            self.sendUpdateToAvatarId(senderId, "receivePartyZone", [senderId, 0, zoneId])
            return
        
        # If they have a zoneId, that means they came from a public party gate
        # or they are teleporting directly to a toon in a party or they are the
        # host returning to their own party.
        if zoneId > 0 :
            if zoneId not in self.zoneIdToHostAvId:
                # this party is gone, you'cant go to it
                self.notify.warning("Trying to go to a party that is gone. zoneId=%s" % zoneId)
                self.__sendNoPartyZoneToClient(senderId)
                return
            
            partyHostId = self.zoneIdToHostAvId[zoneId]
            if self.hostAvIdToClosingPartyZoneId.has_key(partyHostId):
                # This party is closing, you can't go to it.
                self.notify.warning("Trying to go to a party that is closing. hostId=%s" % partyHostId)
                self.__sendNoPartyZoneToClient(senderId)
                return
            
            if partyHostId != senderId:
                # If I'm not the host, check to see if the party is private
                if self.hostAvIdToPartiesRunning[partyHostId].partyInfo.isPrivate:
                    # This is a private party, check the invitee list
                    if senderId not in self.hostAvIdToPartiesRunning[partyHostId].inviteeIds:
                        # The senderId is not on the invitee list of a private party
                        # so they can't attend, sorry.
                        self.__sendNoPartyZoneToClient(senderId)
                        return
            self.__addReferences(senderId, partyHostId)
            self.__waitForToonToEnterParty(senderId, partyHostId, zoneId)
            self.__sendPartyZoneToClient(senderId, partyHostId)
            return
            
        self.__enterParty(senderId, hostId)
        
        avPartyZoneId = self.avIdToPartyZoneId.get(hostId)
        senderPartyZoneId = self.avIdToPartyZoneId.get(senderId)
        
        isSenderHost = False
        isHostStartingParty = False
        
        # Else if sender is host, then toon might be starting a party
        if senderId == hostId:
            isSenderHost = True

            # If the host got here and there's no party for him, then start a party.
            # TODO-parties: Double check on the party shard dict to make sure that toon's party is not happening somewhere else.
            if (
                (not self.hostAvIdToPartiesRunning.has_key(senderId)) and
                (not self.hostAvIdToClosingPartyZoneId.has_key(senderId))
               ):
                # The host is starting a party, let's clear him out of the avIdToPartyZoneId
                #self.clearPartyZoneId(senderId) # this doesn't clear him out of guests
                self.__exitParty(senderId)
                isHostStartingParty = True
        # Else sender is visiting or attending a party at this shard:
        else:
            # The party we are visiting is not in this shard
            if avPartyZoneId is None:
                self.notify.warning("Avatar is not at a party in this shard.")
                # SDN: tell the client and do something more graceful
                # make sure we don't give this guy toonups
                try:
                    # stop tooning up this visitor, he hasn't reached the party yet
                    av = self.air.doId2do[senderId]
                    av.stopToonUp()
                except:
                    DistributedPartyManagerAI.notify.debug("couldn't stop toonUpTask for av %s" % self.air.getAvatarIdFromSender())
                self.__sendNoPartyZoneToClient(senderId)
                return
            
        # If sender was at a party:
        if senderPartyZoneId is not None:
            # Check if toon is teleporting somewhere else in the same party:
            # No need to update the party zone information in this case.
            try:
                if senderPartyZoneId == avPartyZoneId and not isHostStartingParty:
                    DistributedPartyManagerAI.notify.debug("We are staying in the same zone %s, don't delete." % senderPartyZoneId)
                    self.__sendPartyZoneToClient(senderId, hostId)
                    return
                else:
                    DistributedPartyManagerAI.notify.debug("Sender is goint to a different party. Party av zone = %s, sender zone = %s." % (avPartyZoneId, senderPartyZoneId))
            except:
                DistributedPartyManagerAI.notify.debug("Sender is not teleporting to the same party.")
            
            # At this point, toon is at a party and is going/creating a different party
            if senderPartyZoneId != avPartyZoneId:
                if self.hostAvIdToClosingPartyZoneId.has_key(hostId):
                    # This party is closing, you can't go to it.
                    self.notify.warning("Trying to go to a party that is closing. hostId=%s" % hostId)
                    self.__sendNoPartyZoneToClient(senderId)
                    return
                else:
                    self.notify.debug("644 calling exitParty for %s" % senderId)
                    self.__exitParty(senderId)

        # Sender is host and he's starting a party, then start the party:
        if isSenderHost and isHostStartingParty:
            if self.checkHostHasPartiesThatCanStart(hostId):
                # We need to ask DistributedPartyManagerUD for the party information
                # self.partyInfoOfHostResponseUdToAi will be called with the response
                self.notify.debug("starting party Asking uberdog for party ifnromation hostId=%d" % hostId)
                self.air.sendUpdateToDoId(
                    "DistributedPartyManager",
                    'partyInfoOfHostRequestAiToUd',
                    OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                    [self.doId, hostId]
                )
                taskMgr.doMethodLater(
                    3.0,
                    self.partyInfoOfHostFailedResponseUdToAi,
                    "UberdogTimedOut_%d"%hostId,
                    [hostId]
                    )
            else:
                # save a round trip asking the uberdog, fail immediately
                self.air.writeServerEvent('suspicious', senderId,
                                      'trying to start a party when none can start %d' % senderId)
                self.notify.warning('suspicious %d trying to start a party when none can start' % senderId)
                self.__sendNoPartyZoneToClient(senderId)
                return


        # We have a toon visiting another toon's party or a host visiting an
        # already started party, update dicts
        else:
            # Note: hostId is host of the party sender is trying to go to
            if self.hostAvIdToClosingPartyZoneId.has_key(hostId):
                # This party is closing, you can't go to it.
                self.notify.warning("Trying to go to a party that is closing. hostId=%s" % hostId)
                self.__sendNoPartyZoneToClient(senderId)
                return
            self.__addReferences(senderId, hostId)
            zoneId = self.avIdToPartyZoneId[hostId]
            self.__waitForToonToEnterParty(senderId, hostId, zoneId)
            self.__sendPartyZoneToClient(senderId, hostId)

    def checkHostHasPartiesThatCanStart(self, hostId):
        """Return True if the host has any party that can start."""
        result = False
        toon = simbase.air.doId2do.get(hostId)
        if toon:
            hostedParties = toon.hostedParties
            for partyInfo in hostedParties:
                # it must not be cancelle or finished
                if partyInfo.status in (PartyGlobals.PartyStatus.Cancelled,
                                        PartyGlobals.PartyStatus.Finished):
                    continue
                curServerTime = self.air.toontownTimeManager.getCurServerDateTimeForComparison()
                if curServerTime < partyInfo.startTime:
                    # the party is still in the future
                    continue
                if partyInfo.endTime < curServerTime:
                    # party end time has passed
                    continue
                # if we get here we have at least 1 party that could start
                result = True
                break
        else:
            result = True
            self.notify.warning("checkHostedParties could not find toon %d " % hostId)
        return result
        

    def getAvEnterEvent(self):
        return 'avatarEnterParty'
    
    def getAvExitEvent(self, avId=None):
        # listen for all exits or a particular exit
        # event args:
        #  if avId given: none
        #  if avId not given: avId, hostId, zoneId
        if avId is None:
            return 'avatarExitParty'
        else:
            return 'avatarExitParty-%s' % avId

    def __enterParty(self, avId, hostId):
        # Tasks that should always get called when entering a party

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

    def __waitForToonToEnterParty(self, avId, hostId, zoneId):
        if avId in self.avIdEnteringPartyToHostIdZoneId:
            self.notify.warning(
                '__waitForToonToEnterParty(avId=%s, ownerId=%s, zoneId=%s): '
                '%s already in avIdToPendingEnter. overwriting' % (
                avId, hostId, zoneId, avId))
        self.avIdEnteringPartyToHostIdZoneId[avId] = (hostId, zoneId)
        self.accept(DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId),
                    Functor(self.__toonChangedZone, avId))

    def __toonLeftBeforeArrival(self, avId):
        if avId not in self.avIdEnteringPartyToHostIdZoneId:
            self.notify.warning('__toonLeftBeforeArrival: av %s not in table' %
                                avId)
            return
        hostId, zoneId = self.avIdEnteringPartyToHostIdZoneId[avId]
        self.notify.warning(
            '__toonLeftBeforeArrival: av %s left server before arriving in '
            'party (host=%s, zone=%s)' % (avId, hostId, zoneId))
        del self.avIdEnteringPartyToHostIdZoneId[avId]

    # When toon changes zone, check if toon has finally entered party
    def __toonChangedZone(self, avId, newZoneId, oldZoneId):
        #DistributedPartyManagerAI.notify.debug('_toonChangedZone(avId=%s, newZoneId=%s, oldZoneId=%s)' % (avId, newZoneId, oldZoneId))
        if avId not in self.avIdEnteringPartyToHostIdZoneId:
            self.notify.warning('__toonChangedZone: av %s not in table' %
                                avId)
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.notify.warning('__toonChangedZone(%s): av not present' % avId)
            return
        hostId, zoneId = self.avIdEnteringPartyToHostIdZoneId[avId]
        if newZoneId == zoneId:
            del self.avIdEnteringPartyToHostIdZoneId[avId]
            self.ignore(DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId))
            self.announceToonEnterPartyZone(avId, hostId, zoneId)
        
    def announceToonEnterPartyZone(self, avId, hostId, zoneId):
        """
        announce to the rest of the system that a toon is entering a party
        """
        DistributedPartyManagerAI.notify.debug('announceToonEnterPartyZone: %s %s %s' % (avId, hostId, zoneId))

        av = self.air.doId2do[avId]

        # Toonup
        av.startToonUp(self.healFrequency)

        if avId == hostId:
            # We have to tell the uberdog that we've started a new party so it can
            # update all the other AIs with public party info (but only host does this)            
            if not self.hostAvIdToAllPartiesInfo.has_key(avId):
                self.air.sendUpdateToDoId(
                    "DistributedPartyManager",
                    'partyHasStartedAiToUd',
                    OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                    [self.doId, self.hostAvIdToPartiesRunning[hostId].partyInfo.partyId, self.air.districtId, zoneId, av.getName()]
                )
                
                # tell host to whisper all his guests that the party has started.
                # We have the host do this as host already has access to guest list.
                av.sendUpdate( "announcePartyStarted", [self.hostAvIdToPartiesRunning[hostId].partyInfo.partyId] )
        
        messenger.send(self.getAvEnterEvent(), [avId, hostId, zoneId])
        # Tell the uberdog about the new count
        self.air.sendUpdateToDoId(
            "DistributedPartyManager",
            'toonHasEnteredPartyAiToUd',
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
            [hostId],
        )

    def announceToonExitPartyZone(self, avId, hostId, zoneId):
        """ announce to the rest of the system that a toon is exiting
        a party """
        EstateManagerAI.notify.debug('announceToonExitPartyZone: %s %s %s' %
                                     (avId, hostId, zoneId))
        messenger.send(self.getAvExitEvent(avId))
        messenger.send(self.getAvExitEvent(), [avId, hostId, zoneId])

    # Return a running distributed party based on the Zone id:
    def getRunningPartyFromZoneId(self, zoneId):
        hostId = self.zoneIdToHostAvId.get(zoneId)
        if hostId:
            return self.hostAvIdToPartiesRunning.get(hostId)
        return None

    # Send Party Zone information back to the client
    def __sendPartyZoneToClient(self, avId, hostId):
        self.notify.warning("__sendPartyZoneToClient called with avId=%d, hostId=%d" % (avId, hostId))
        try:
            zoneId = self.avIdToPartyZoneId[avId]
            partyId = self.hostAvIdToPartiesRunning[hostId].partyInfo.partyId            
            self.sendUpdateToAvatarId(avId, "receivePartyZone", [hostId, partyId, zoneId])
        except:
            self.notify.warning("__sendPartyZoneToClient : zone did not exist for party host %d, and visitor %d" % (hostId, avId)) 
            self.sendUpdateToAvatarId(avId, "receivePartyZone", [0, 0, 0])
    
    # Send empty Party Zone information back to the client
    # This is called, for example, in case a toon teleports to a party not
    # running on this shard or if the uberdog doesn't think this party can be
    # created.
    def __sendNoPartyZoneToClient(self, avId):
        self.notify.warning("__sendNoPartyZoneToClient : not sending avId %d to a party." % avId) 
        self.sendUpdateToAvatarId(avId, "receivePartyZone", [0, 0, 0])

    def partyInfoOfHostFailedResponseUdToAi(self, hostId):
        """
        A host tried to create a party that it wasn't time to create, ie,
        something fishy went down.  Reply that the party creation failed.
        If you want to test parties using magic words, be sure to set
        allow-random-party-creation 1 in your config overrides.
        """
        self.notify.warning("Host with avId %d tried to create a party it wasn't time for." % hostId)
        taskMgr.remove("UberdogTimedOut_%d"%hostId)
        self.__sendNoPartyZoneToClient(hostId)

    def partyInfoOfHostResponseUdToAi(self, partyInfoTuple, inviteeIds):
        """ 
        Called by UD after it has gathered the relevant information for this
        party. 
        """
        assert self.notify.debugStateCall(self)
        taskMgr.remove("UberdogTimedOut_%d"%partyInfoTuple[1])
        # Note this method will send the zone info back to the client 
        # after it creates the party
        partyInfo = PartyInfoAI(*partyInfoTuple)
        # request an available zone to have this party in
        zoneId = self.air.allocateZone()

        # remove any references to host in parties he's currently attending
        # in case he start a party within another party
        self.__exitParty(partyInfo.hostId)
        
        # Host is attending the party, too
        self.setPartyZoneId(partyInfo.hostId, zoneId)
        
        # start a ref count for this zone id
        self.zoneIdToGuestAvIds[zoneId] = []
        self.zoneIdToHostAvId[zoneId] = partyInfo.hostId
        self.handleGetPartyInfo(partyInfo, inviteeIds)

    def __addReferences(self, senderId, hostId):
        DistributedPartyManagerAI.notify.debug("__addReferences : senderId = %s  hostId = %s" % (senderId, hostId))
        party = self.hostAvIdToPartiesRunning.get(hostId)
        if party is not None:
            self.setPartyZoneId(senderId, party.zoneId)
            ref = self.zoneIdToGuestAvIds.get(party.zoneId)
            if ref is not None:
                if not senderId in ref:
                    ref.append(senderId)
            else:
                self.zoneIdToGuestAvIds[party.zoneId] = [senderId]
                
    def __removeReferences(self, avId, zoneId):
        try:
            self.clearPartyZoneId(avId)
            self.zoneIdToGuestAvIds[zoneId].remove(avId)
        except:
            DistributedPartyManagerAI.notify.debug("we weren't in the zoneIdToGuestAvIds for %s." % zoneId)
            pass

    def setPartyZoneId(self, avId, zoneId):
        self.avIdToPartyZoneId[avId] = zoneId
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        DistributedPartyManagerAI.notify.debug("%s(%s):Added %s:%s" % (defName, lineno, avId, zoneId))
        
    def clearPartyZoneId(self, avId, zoneIdFromClient = None):
        """Clear avId to partyzoneId dict, if zoneIdFromClient is not none, do it only if they match."""
        if not self.avIdToPartyZoneId.has_key(avId):
            return
        zoneId = self.avIdToPartyZoneId[avId]
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        removeFromDict = False
        if zoneIdFromClient != None:
            if zoneId == zoneIdFromClient:
                removeFromDict =True
            else:
                self.notify.debug("zoneIdFromClient=%s  AI thinks he's at zone %s, not removing" %
                                  (zoneIdFromClient, zoneId))
        else:
            removeFromDict = True

        if removeFromDict:
            DistributedPartyManagerAI.notify.debug("%s(%s):Removed %s:%s" % (defName, lineno, avId, self.avIdToPartyZoneId[avId]))
            del self.avIdToPartyZoneId[avId]
   
    def handleGetPartyInfo(self, partyInfo, inviteeIds):
        DistributedPartyManagerAI.notify.debug("handleGetPartyInfo for host %s" % partyInfo.hostId)
        # this function is called after the party data is pulled
        # from the database.  the DistributedPartyAI object is initialized
        # here

        # Note:  this function is only called by the host of the party.

        # there is a chance that the owner will already have left (by
        # closing the window).  We need to handle that gracefully.
        if not self.avIdToPartyZoneId.has_key(partyInfo.hostId):
            self.notify.warning("Party Zone info was requested, but the guest left before it could be recived: %d" % estateId)
            return

        # create the DistributedPartyAI object for this hostId
        if self.hostAvIdToPartiesRunning.has_key(partyInfo.hostId):
            self.notify.warning("Already have distobj %s, not generating again" % (partyInfo.partyId))
        else:
            self.notify.info('start party %s init, owner=%s, frame=%s' %
                             (partyInfo.partyId, partyInfo.hostId, globalClock.getFrameCount()))
            
            partyZoneId = self.avIdToPartyZoneId[partyInfo.hostId]                
            partyAI = DistributedPartyAI(self.air, partyInfo.hostId, partyZoneId, partyInfo, inviteeIds)
            
            partyAI.generateOtpObject(
                parentId=self.air.districtId,
                zoneId=partyZoneId,
            )
            partyAI.initPartyData()
            self.hostAvIdToPartiesRunning[partyInfo.hostId] = partyAI

            self.__addReferences(partyInfo.hostId, partyInfo.hostId)
            
            # We need to kick guests out when the party is closing and not allow
            # anyone else in.  Send a message to guests to leave
            # Also, alert uberdog.
            taskMgr.doMethodLater(
                PartyGlobals.DefaultPartyDuration * 3600.0,
                self.__setPartyEnded,
                "DistributedPartyManagerAI_PartyEnding_%d" % partyZoneId,
                [partyInfo.hostId,partyZoneId]
                )

            # Boot the guests
            taskMgr.doMethodLater(
                PartyGlobals.DefaultPartyDuration * 3600.0 + PartyGlobals.DelayBeforeAutoKick,
                self.__bootGuests,
                "DistributedPartyManagerAI_BootGuests_%d" % partyZoneId,
                [partyInfo.hostId,partyZoneId]
                )

            # We need to clean this party up after everybody is gone
            taskMgr.doMethodLater(
                PartyGlobals.DefaultPartyDuration * 3600.0 + PartyGlobals.DelayBeforeAutoKick + 10.0,
                self.__cleanupParty,
                "DistributedPartyManagerAI_CleanUpPartyZone_%d" % partyZoneId,
                [partyInfo.hostId,partyZoneId]
                )
            
            self.notify.info('Finished creating party : partyId %s init, host = %s' % (partyInfo.partyId, partyInfo.hostId))

        # Now that the zone is set up, send the notification back to
        # the client.
        zoneId = self.avIdToPartyZoneId[partyInfo.hostId]
        self.__sendPartyZoneToClient(partyInfo.hostId, partyInfo.hostId)
        self.__waitForToonToEnterParty(partyInfo.hostId, partyInfo.hostId, zoneId)

    def requestShardIdZoneIdForHostId(self, hostId):
        """
        Request from either a host of an already started party or a guest of
        a party for the shardId and zoneId of that host's party.
        """
        senderId = self.air.getAvatarIdFromSender()
        if self.hostAvIdToAllPartiesInfo.has_key(hostId):
            shardId = self.hostAvIdToAllPartiesInfo[hostId][1]
            zoneId = self.hostAvIdToAllPartiesInfo[hostId][2]
            self.sendUpdateToAvatarId(senderId, 'sendShardIdZoneIdToAvatar', [shardId, zoneId])
        else:
            # The host's id is not in our dictionary... that most likely means
            # that the AI server has crashed, send back 0
            self.sendUpdateToAvatarId(senderId, 'sendShardIdZoneIdToAvatar', [0, 0])

    ## -----------------------------------------------------------
    ## Cleanup and exit functions
    ## -----------------------------------------------------------

    def exitParty(self, zoneId):
        senderId = self.air.getAvatarIdFromSender()
        DistributedPartyManagerAI.notify.debug("exitParty(%s)" % senderId)
        # This function is called from client in the normal case,
        # such as teleporting out, door out, exiting the game, etc
        self.__exitParty(senderId, zoneId)
        
    def __handleUnexpectedExit(self, avId):
        DistributedPartyManagerAI.notify.debug("we got an unexpected exit on av: %s:  deleting." % avId)
        taskMgr.remove("estateToonUp-" + str(avId))
        if avId in self.avIdEnteringPartyToHostIdZoneId:
            self.__toonLeftBeforeArrival(avId)
        if self.avIdToPartyZoneId.has_key(avId):
            self.__exitParty(avId)
        else:
            DistributedPartyManagerAI.notify.debug("unexpected exit and %s is not in avIdToPartyZoneId" % avId)
        return None

    def __exitParty(self, avId, zoneIdFromClient = None):
        DistributedPartyManagerAI.notify.debug("__exitParty(%d)" % avId)
        DistributedPartyManagerAI.notify.info("__exitParty(%d)" % avId)
        # This is called whenever avId leaves a party.
        # Just remove references of avId from the party
        avZoneId = self.avIdToPartyZoneId.get(avId)
        if zoneIdFromClient != None:
            # We get a very weird case when you're starting a party from another party
            if avZoneId != zoneIdFromClient:
                self.notify.debug("overriding avZoneId to %s" % zoneIdFromClient)
            avZoneId = zoneIdFromClient
            
        partyId = -1
        isPlanning = True
        if avZoneId is not None:
            isPlanning = False
            self.clearPartyZoneId(avId, zoneIdFromClient)
            if self.zoneIdToGuestAvIds.has_key(avZoneId):
                if avId in self.zoneIdToGuestAvIds[avZoneId]:
                    self.notify.debug("removing guest %d from zone %d" % (avId, avZoneId))
                    self.zoneIdToGuestAvIds[avZoneId].remove(avId)
                else:
                    DistributedPartyManagerAI.notify.debug("wasn't in zoneIdToGuestAvIds list: %s, %s" % (avZoneId, avId))
            else:
                DistributedPartyManagerAI.notify.debug("wasn't in zoneIdToGuestAvIds: %s, %s" % (avZoneId, avId))
            # Tell the uberdog that this host's party has lost a guest
            hostAvId = self.zoneIdToHostAvId.get(avZoneId)
            if hostAvId:
                self.air.sendUpdateToDoId(
                    "DistributedPartyManager",
                    'toonHasExitedPartyAiToUd',
                    OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                    [self.zoneIdToHostAvId[avZoneId]]
                    )
                info = self.hostAvIdToAllPartiesInfo.get(hostAvId)
                if info:
                    partyId = info[7]
                
            else:
                self.notify.warning("__exitParty() avZoneId=%d not in self.zoneIdToHostAvId" % avZoneId)
            
        else:
            DistributedPartyManagerAI.notify.debug("__exitParty can't find zone for %d" % avId)

        totalMoney = -1
        # stop the healing
        if self.air.doId2do.has_key(avId):
            # Find the avatar
            av = self.air.doId2do[avId]
            # Stop healing them
            av.stopToonUp()
            totalMoney = av.getTotalMoney()

        if not isPlanning:
            self.air.writeServerEvent("party_exit", partyId,"%d|%d" % (avId, totalMoney))

    def freeZoneIdFromPlannedParty(self, hostId, zoneId):
        """ Free a zone that was allocated for the planning of a party """
        senderId = self.air.getAvatarIdFromSender()
        if senderId != hostId:
            self.air.writeServerEvent('suspicious', senderId, 'someone else trying to free a zone for this avatar: hostId = %d' % hostId)
            return
        if self.hostIdToPlanningPartyZoneId.has_key(hostId):
            DistributedPartyManagerAI.notify.debug("freeZoneIdFromPlannedParty : freeing zone : hostId = %d, zoneId = %d" % (hostId, zoneId))
            self.air.deallocateZone(self.hostIdToPlanningPartyZoneId[hostId])
            del self.hostIdToPlanningPartyZoneId[hostId]
            return
        else:
            self.notify.warning('suspicious senderId=%d trying to free a zone that this avatar did not allocate: hostId = %d' % (senderId,hostId))
            self.air.writeServerEvent('suspicious', senderId, 'trying to free a zone that this avatar did not allocate: hostId = %d' % hostId)
            return
        
    def __cleanupParty(self, hostId, zoneId):
        DistributedPartyManagerAI.notify.debug("__cleanupParty hostId = %d, zoneId = %d" % (hostId, zoneId))
        
        self.clearPartyZoneId(hostId)
        if self.hostAvIdToClosingPartyZoneId.has_key(hostId):
            del self.hostAvIdToClosingPartyZoneId[hostId]
        if self.zoneIdToHostAvId.has_key(zoneId):
            del self.zoneIdToHostAvId[zoneId]

        # give our zoneId back to the air
        self.air.deallocateZone(zoneId)

        # delete party grounds from state server
        self.__deleteParty(hostId)

        # stop listening for unexpectedExit
        self.ignore(self.air.getAvatarExitEvent(hostId))

        if self.zoneIdToGuestAvIds.has_key(zoneId):
            del self.zoneIdToGuestAvIds[zoneId]

    def __deleteParty(self, hostId):
        # remove all our objects from the stateserver
        DistributedPartyManagerAI.notify.debug("__deleteParty(hostId=%s)" % hostId)

        # delete from state server
        if self.hostAvIdToPartiesRunning.has_key(hostId):
            if self.hostAvIdToPartiesRunning[hostId] != None:
                self.hostAvIdToPartiesRunning[hostId].destroyPartyData()
                DistributedPartyManagerAI.notify.debug('DistributedPartyAI requestDelete, doId=%d' % getattr(self.hostAvIdToPartiesRunning[hostId], 'doId'))
                self.hostAvIdToPartiesRunning[hostId].requestDelete()
                del self.hostAvIdToPartiesRunning[hostId]

    def __bootGuests(self, hostId, zoneId):
        DistributedPartyManagerAI.notify.debug("__bootGuests (hostId=%s  zoneId=%s)" % (hostId,zoneId))
        try:
            # we need a copy of the list, otherwise we skip some people in booting out
            visitors = self.zoneIdToGuestAvIds[zoneId][:]
            for avId in visitors:
                # people get left behind in the party if we boot the host first
                if avId == hostId:
                    continue
                self.notify.debug("booting %d from zone %d host=%d" %(avId, zoneId, hostId))
                self.__bootAv(avId, zoneId, hostId)
            if hostId in visitors:
                self.__bootAv(hostId, zoneId, hostId)
                self.notify.debug("booting %d from zone %d host=%d" %(avId, zoneId, hostId))
        except:
            # refCount might have already gotten deleted
            pass
    
    def __bootAv(self, avId, zoneId, hostId):
        # Let anyone who might be doing something with this avatar in the party
        assert self.notify.debugStateCall(self)
        messenger.send("bootAvFromParty-"+str(avId))
        self.__exitParty(avId)
        # Pass the message to the client, who will pass it to the PartyHood
        self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, 1]) # 0 is a warning, 1 is final

    def getPartyEndedEvent(self, hostId):
        return 'partyEnded-%s' % hostId

    def __setPartyEnded(self, hostId, zoneId):
        """
        This party has ended, so no one can go to it, and we'll
        warn people there to get out!
        """
        DistributedPartyManagerAI.notify.debug("__setPartyEnded (hostId=%s  zoneId=%s)" % (hostId,zoneId))
        # Tell uberdog about it so it can update hostAvIdToAllPartiesInfo
        self.air.sendUpdateToDoId(
            "DistributedPartyManager",
            'changePartyStatusRequestAiToUd',
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
            [self.doId, self.hostAvIdToPartiesRunning[hostId].partyInfo.partyId, PartyGlobals.PartyStatus.Finished]
        )
        
        self.hostAvIdToClosingPartyZoneId[hostId] = zoneId

        messenger.send(self.getPartyEndedEvent(hostId))
        
        # Warn guests they have to leave
        guests = self.zoneIdToGuestAvIds.get(zoneId)
        if guests:
            for avId in guests:
                # Pass the message to the client, who will pass it to the PartyHood
                self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, 0]) # 0 is a warning, 1 is final                

        self.hostAvIdToPartiesRunning[hostId].b_setPartyState(True)        

    def testMsgUdToAllAi(self):
        """Try receiving a UD to all AI msg."""
        self.notify.debugStateCall(self)
        pass

    def forceCheckStart(self):
        """Force the uberdog party manager to do an immediate check for which parties can start."""
        self.air.sendUpdateToDoId(
            "DistributedPartyManager",
            'forceCheckStart',
            OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
            []
        )        

    def allowUnreleasedServer(self):
        """Return do we allow player to buy unreleased activities and decorations on the client."""
        return self.allowUnreleased
        
    def setAllowUnreleaseServer(self, newValue):
        """Set if we allow player to buy unreleased activities and decorations on the client."""
        self.allowUnreleased = newValue

    def toggleAllowUnreleasedServer(self):
        """Toggle allow unreleased on the client, then return the new value."""
        self.allowUnreleased = not self.allowUnreleased
        return self.allowUnreleased

    def canBuyParties(self):
        """Return do we allow player to buy parties."""
        return self.canBuy
        
    def setCanBuyParties(self, newValue):
        """Set if we allow player to buy unreleased activities and decorations on the client."""
        self.canBuy= newValue

    def toggleCanBuyParties(self):
        """Toggle allow unreleased on the client, then return the new value."""
        self.canBuy= not self.canBuy
        return self.canBuy
    
    def partyManagerUdStartingUp(self):
        """The uberdog is restarting, tell it about parties running on this district."""
        for hostId in self.hostAvIdToAllPartiesInfo:
            if hostId not in self.hostAvIdToPartiesRunning:
                self.notify.warning('hostId %d is in self.hostAvIdToAllPartiesInfo but not in self.hostAvIdToPartiesRunning' % hostId)
                # really check we have a DistributedPartyAI for the host
                continue
            partyInfo = self.hostAvIdToAllPartiesInfo[hostId]
            shardId = partyInfo[1]
            if shardId == self.air.districtId:
                startTime = partyInfo[0]
                zoneId = partyInfo[2]
                isPrivate = partyInfo[3]
                numberOfGuests = partyInfo[4]
                hostName = partyInfo[5]
                activityIds = partyInfo[6]
                partyId = partyInfo[7]
                
                self.air.sendUpdateToDoId(
                    "DistributedPartyManager",
                    'updateAllPartyInfoToUd',
                    OtpDoGlobals.OTP_DO_ID_TOONTOWN_PARTY_MANAGER,
                    [hostId, startTime, shardId, zoneId, isPrivate, numberOfGuests,
                     hostName, activityIds, partyId]
                )
                        

    def magicWordEnd(self, senderId):
        """End the party prematurely as the sender said a magic word."""
        # first test if we are hosting a party
        partyZoneId = self.avIdToPartyZoneId.get(senderId)
        if not partyZoneId:
            return "%d not in self.avIdToPartyZoneId" % senderId
        
        hostId = self.zoneIdToHostAvId.get(partyZoneId)
        if hostId != senderId:
            return "sender %d is not host (%d is)" % (senderId, hostId)

        # nuke the old tasks
        taskMgr.remove("DistributedPartyManagerAI_PartyEnding_%d"%partyZoneId)
        taskMgr.remove("DistributedPartyManagerAI_BootGuests_%d"%partyZoneId)
        taskMgr.remove("DistributedPartyManagerAI_CleanUpPartyZone_%d"%partyZoneId)

        # now start up new tasks to end the party right now
        taskMgr.doMethodLater(0.1, self.__setPartyEnded, "DistributedPartyManagerAI_PartyEnding_%d"%partyZoneId, [hostId,partyZoneId])
        kickDelay = simbase.config.GetInt("party-kick-delay",PartyGlobals.DelayBeforeAutoKick)
        taskMgr.doMethodLater(0.1 + kickDelay, self.__bootGuests, "DistributedPartyManagerAI_BootGuests_%d"%partyZoneId, [hostId,partyZoneId])
        taskMgr.doMethodLater(0.1 + kickDelay + 10.0, self.__cleanupParty, "DistributedPartyManagerAI_CleanUpPartyZone_%d"%partyZoneId, [hostId,partyZoneId])
        
        return ("Party Zone %d Ending Soon" % partyZoneId)
        

    def deductMoneyFromOfflineToon(self, toonId, cost):
        """Deduct the cost of the party from an offline toon."""
        # it's possible for someone to alt f4 out in between the time it takes for
        # the uberdog to respond to AI that buying the party was a success
        ag = RepairAvatars.AvatarGetter(self.air)
        event = 'gotOfflineToon-%s' % toonId
        ag.getAvatar(toonId, fields=['setName', 'setMaxHp',
                                               'setMaxMoney',
                                               'setMaxBankMoney',
                                     'setMoney',
                                     'setBankMoney'],
                     event = event)
        self.acceptOnce(event, Functor(self.gotOfflineToon, cost = cost, toonId = toonId))        
        
    def gotOfflineToon(self, toon, cost, toonId):
        """Handle a response to our request to get an offline toon, deduct the money from him."""
        if toon is None:
            # prevent mem leak
            self.notify.warning("gotOfflineToon - toon %s not found. buying a party for free!cost=%s"
                                % (toonId, cost))
            self.air.writeServerEvent('suspicious', toonId,
                                      "gotOfflineToon - toon %s not found. buying a party for free!cost=%s"
                                      % (toonId, cost))
            return

        totalMoney = toon.getTotalMoney()
        result = toon.takeMoney(cost, bUseBank = True)
        if result:
            newTotalMoney = toon.getTotalMoney()
            self.notify.info("gotOfflineToon - deducting %s from offline toon %s newTotalMoney=%s"
                             % (cost, toonId,newTotalMoney))
        else:
            self.notify.warning("gotOfflineToon - Host %s got away with buying a party he can't afford! totalMoney=%s cost=%s"
                                % (toonId,totalMoney, cost))
            self.air.writeServerEvent('suspicious', toonId,
                                      "gotOfflineToon - Host %s got away with buying a party he can't afford! totalMoney=%s cost=%s"
                                      % (toonId,totalMoney, cost))


        # takeMoney is doing a b_setMoney, so that gets written into the otp database
        # db = DatabaseObject.DatabaseObject(self.air, toon.doId)
        # db.storeObject(toon, ["setMoney", "setBankMoney"])
            
        # prevent mem leak
        # as far as I can tell we don't need this, ~aigarbage reports 0 cycles
        # toon.patchDelete()
