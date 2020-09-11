import socket
import time
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.http.WebRequest import WebRequestDispatcher
from otp.otpbase import OTPLocalizer
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogItemTypes
from toontown.catalog import CatalogClothingItem
from toontown.catalog import CatalogFurnitureItem
from toontown.catalog import CatalogChatItem
from toontown.catalog import CatalogEmoteItem
from toontown.catalog import CatalogGenerator
from toontown.catalog import CatalogBeanItem
from toontown.catalog import CatalogWallpaperItem
from toontown.catalog import CatalogWindowItem
from toontown.catalog import CatalogFlooringItem
from toontown.catalog import CatalogWainscotingItem
from toontown.catalog import CatalogMouldingItem
from toontown.catalog import CatalogPetTrickItem
from toontown.catalog import CatalogRentalItem
from toontown.catalog import CatalogAnimatedFurnitureItem
from toontown.toonbase import TTLocalizer
from toontown.rpc import AwardResponses
from toontown.rpc import AwardManagerConsts
from toontown.toonbase import ToontownGlobals
from direct.distributed.AsyncRequest import AsyncRequest

WrongGenderStr = "wrong gender"
JellybeanRewardValues = (1,5,10,15,20,25,50,100,150,200,250,500,750,1000)

# How long does an Award sit on the awardOnOrder
AwardManagerDelayMinutes = uber.config.GetInt("award-delay-minutes", 30)

GiveAfterDelayTime = 1
GiveImmediately = 2
TryToRemove =3
GiveAfterOneMinute = 4
NukeAllAwards=5

SpecialCommandStrs = {
    GiveAfterDelayTime : "Give award  after 30 minutes",
    GiveImmediately : "Give award immediately",
    TryToRemove : "Try to remove the award",
    NukeAllAwards : "Nuke all awards in award mailbox and award queue",
    }

class GetToonsRequest(AsyncRequest):
    # So this is just a class to get all the toons receiving awards
    # Actually replying back to the browser is handled by 
    def __init__(self, awardManagerDo, isDcRequest, dcId, toonIdsList, catalogItem, specialEventId, browserReplyTo, specialCommands, echoBack, timeout = 4.0):
        """Construct ourself."""
        replyToChannelId = awardManagerDo.air.getSenderReturnChannel
        AsyncRequest.__init__(self, awardManagerDo.air, replyToChannelId, timeout)
        self.awardManagerDo=awardManagerDo
        self._isDcRequest = isDcRequest
        self._dcId = dcId
        self.toonIds=toonIdsList
        self.item =catalogItem
        self.specialEventId = specialEventId
        self.retcode = None
        self.browserReplyTo = browserReplyTo
        self.catalogType = None
        self.specialCommands = specialCommands
        self.echoBack = echoBack
        for toonId in self.toonIds:
           self.neededObjects[toonId] = None
        for toonId in self.toonIds:
           self.askForObject(toonId)
        
    def finish(self):
        """Report back on all the toon database objects that we got."""
        replyString = str(self.neededObjects)
        #self.browserReplyTo.respond(replyString)
        self.awardManagerDo.gotTheToons(self._isDcRequest, self._dcId, self.neededObjects, self.item, self.specialEventId, self.browserReplyTo, self.specialCommands, self.echoBack)
        AsyncRequest.finish(self)

    def timeout(self, task):
        """Report back on the toons we did get, even if some were not in the database."""
        # Unfortunately I had to copy and paste this from AsyncRequest
        # There's no concept of a callback in case the request fails
        assert AsyncRequest.notify.debugCall(
            "neededObjects: %s"%(self.neededObjects,))
        if self.numRetries > 0:
            assert AsyncRequest.notify.debug(
                'Timed out. Trying %d more time(s) : %s' %
                (self.numRetries + 1, `self.neededObjects`))
            self.numRetries -= 1
            return Task.again
        else:
            if __debug__:
               if False: # True:
                    if hasattr(self, "avatarId"):
                        print "\n\nself.avatarId =", self.avatarId
                    print "\nself.neededObjects =", self.neededObjects
                    print "\ntimed out after %s seconds.\n\n"%(task.delayTime,)
                    import pdb; pdb.set_trace()
            replyString = '"some toonIds invalid %s"' % str(self.neededObjects)
            replyString = replyString.replace('<','_')
            replyString = replyString.replace('>','_')
            #self.browserReplyTo.respond(replyString)
            self.awardManagerDo.gotTheToons(self._isDcRequest, self._dcId, self.neededObjects, self.item, self.specialEventId, self.browserReplyTo, self.specialCommands, self.echoBack) 
            self.delete()
            return task.done
        
 

class AwardManagerUD(DistributedObjectGlobalUD):
    """
    Uberdog object for making promo awards to Toons
    """
    notify = directNotify.newCategory('AwardManagerUD')

    def __init__(self, air):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)
        
        self.air = air

        self._dcRequestSerialGen = SerialNumGen(1)
        self._dcId2info = {}

        self.HTTPListenPort = uber.awardManagerHTTPListenPort

        self.numServed = 0

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("AwardManager")
        self.webDispatcher.landingPage.setDescription("AwardManager is a REST-like interface allowing in-game awards from other services.")
        self.webDispatcher.registerGETHandler('awardMgr', self.awardMgr)
        self.webDispatcher.registerGETHandler('awardGive', self.giveAward)
        self.webDispatcher.listenOnPort(self.HTTPListenPort)
        self.webDispatcher.landingPage.addTab("AwardMgr","/awardMgr")


        self.air.setConnectionName("AwardMgr")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))
        self.awardChoices = self.getAwardChoices()  # award Choices is a dict of dicts
        self.reverseDictAwardChoices = self.getReversedAwardChoices()
        
    def announceGenerate(self):
        """Start accepting http requests."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.webDispatcher.startCheckingIncomingHTTP()

    def giveAward(self, replyTo, **kw):
        """Give the award in a try block, so as not to crash uberdog if all else fails."""
        try:
            self.giveAwardActual(replyTo, **kw)
        except Exception,e:
            replyTo.respondXML(AwardResponses.awardGiveFailureXML % ("Catastrophic failure giving the award %s" % str(e)))

    def _getCatalogItemObj(self, itemType, itemIndex):
        if itemType == CatalogItemTypes.CLOTHING_ITEM:
            clothingNumber = itemIndex
            #itemObj = CatalogBeanItem.CatalogBeanItem(amount)
            # for now always the first color choice
            itemObj = CatalogClothingItem.CatalogClothingItem(clothingNumber, 0)
            itemObj.giftTag = 0
            itemObj.giftCode = 1
        elif itemType == CatalogItemTypes.FURNITURE_ITEM:
            furnitureNumber = itemIndex
            itemObj = CatalogFurnitureItem.CatalogFurnitureItem(furnitureNumber, colorOption = 0)
        elif itemType == CatalogItemTypes.CHAT_ITEM:
            chatIndex = itemIndex
            itemObj = CatalogChatItem.CatalogChatItem(chatIndex)
        elif itemType == CatalogItemTypes.EMOTE_ITEM:
            emoteIndex = itemIndex
            itemObj = CatalogEmoteItem.CatalogEmoteItem(emoteIndex)
        elif itemType == CatalogItemTypes.BEAN_ITEM:
            numBeans = itemIndex
            if not numBeans in JellybeanRewardValues:
                self.air.writeServerEvent("suspicious", replyTo.getSourceAddress(),"giving %s beans" % numBeans)
            # an assertion exception will occur so the jellybean won't get rewarded
            assert (numBeans in JellybeanRewardValues)
            itemObj = CatalogBeanItem.CatalogBeanItem(numBeans)
        elif itemType == CatalogItemTypes.WALLPAPER_ITEM:
            wallPaperNumber = itemIndex
            itemObj = CatalogWallpaperItem.CatalogWallpaperItem(wallPaperNumber, colorIndex = 0)
        elif itemType == CatalogItemTypes.WINDOW_ITEM:
            windowNumber = itemIndex
            itemObj = CatalogWindowItem.CatalogWindowItem(windowNumber,  placement = 0)
        elif itemType == CatalogItemTypes.FLOORING_ITEM:
            flooringNumber = itemIndex
            itemObj = CatalogFlooringItem.CatalogFlooringItem(flooringNumber,  colorIndex = 0)
        elif itemType == CatalogItemTypes.MOULDING_ITEM:
            mouldingNumber = itemIndex
            itemObj = CatalogMouldingItem.CatalogMouldingItem(mouldingNumber,  colorIndex = 0)
        elif itemType == CatalogItemTypes.WAINSCOTING_ITEM:
            wainscotingNumber = itemIndex
            itemObj = CatalogWainscotingItem.CatalogWainscotingItem(wainscotingNumber,  colorIndex = 0)
        elif itemType == CatalogItemTypes.PET_TRICK_ITEM:
            trickId = itemIndex
            itemObj = CatalogPetTrickItem.CatalogPetTrickItem(trickId)
        elif itemType == CatalogItemTypes.RENTAL_ITEM:
            # TODO since all we offer so far is 48 hours of cannons, values pulled for CatalogGenerator
            # do something else if we have different durations
            rentalType = itemIndex                
            itemObj = CatalogRentalItem.CatalogRentalItem(rentalType, 2880, 1000)
        elif itemType == CatalogItemTypes.ANIMATED_FURNITURE_ITEM:
            furnitureNumber = itemIndex
            itemObj = CatalogAnimatedFurnitureItem.CatalogAnimatedFurnitureItem(furnitureNumber, colorOption = 0)
        return itemObj
            
    def giveAwardActual(self, replyTo, **kw):
        """Actually give the awards."""
        
        self.notify.debug("giveAward")
        self.notify.debug("%s" % str(kw))
        # Debating if we should log invalid award requests
        # self.air.writeServerEvent('giveAward1stPass', 0, '%s %s' % (replyTo.getSourceAddress(), str(kw)))

        # TODO so many things can go wrong put a try block here
        toonIds = []
        try:
           toonIdsStr = kw['toonIds']
           individualToonIds = toonIdsStr.split('+')
           for newToonIdStr in individualToonIds:
              newToonId =  int(newToonIdStr)
              assert newToonId > 0
              assert newToonId < (1<<32)
              toonIds.append( newToonId)
        except:
           replyTo.respondXML(AwardResponses.awardGiveFailureXML % ("toonIds must be space separated 32 bit integers"))
           return

        itemType = None
        secondChoice = None
        try:            
            itemTypeStr = kw['optone']
            secondChoiceStr = kw['opttwo']

            itemType = int(itemTypeStr)
            secondChoice = int(secondChoiceStr)

            testItem = self._getCatalogItemObj(itemType, secondChoice)
                
        except Exception, e:
           replyTo.respondXML(AwardResponses.awardGiveFailureXML % ("Couldn't create catalog item itemType=%s secondChoice%s %s" % (itemType, secondChoice, str(e))))
           return
       
        
        specialEventId = 0
        try:
            specialEventId = int(kw['specialEventId'])
        except:
            replyTo.respondXML(AwardResponses.awardGiveFailureXML % ("Invalied Special EventId args received=%s" % (str(kw))))
            return

        specialCommands = 1
        try:
            specialCommands = int(kw['specialCommands'])
        except:
            replyTo.respondXML(AwardResponses.awardGiveFailureXML % ("Invalied special commands args received=%s" % (str(kw))))
            return       

        # create our echo back string
        echoBack = ""
        echoBack += "<br />Special Event = %s" % TTLocalizer.SpecialEventNames[specialEventId]
        echoBack += "<br />Item Type = %s" % TTLocalizer.CatalogItemTypeNames[itemType]
        echoBack += "<br />Item Details = %s" % self.reverseDictAwardChoices[itemType][secondChoice]
        echoBack += "<br />Special Commands = %s" % SpecialCommandStrs[specialCommands]

        self.air.writeServerEvent('giveAwardWebRequest', 0, '%s|%s|%s' % (replyTo.getSourceAddress(), echoBack, toonIds))
        print echoBack
        replyToChannel = self.air.getSenderReturnChannel()

        isDcRequest = False
        dcId = 0
        myGTR=GetToonsRequest(self, isDcRequest, dcId, toonIds, testItem, specialEventId, replyTo, specialCommands, echoBack)
        # Whether we got all the toons or not the control continues in gotTheToons

    def awardMgr(self, replyTo, **kw):
        """Handle all calls to web requests awardMgr."""
        assert self.notify.debugCall()
        
        # If no arguments are passed, assume that the main menu should
        # be displayed

        if not kw:
            function = None
            id = None
        else:
            function = "doAward"

        header = body = help = footer = ""
        if not function:
            #header,body,footer,help= self.getMainMenu()
            header,body,footer,help= self.getExperimentalMenu()
        else:
            self.notify.debug("%s" % str(kw))
            header,body,footer,help= self.getMainMenu()
            body = """<BODY><div id="contents"><center><P>got these arguments """
            body += str(kw)
            
        #self.notify.info("%s" % header + body + help + footer)
        replyTo.respond(header + body + help + footer)

    def checkGender(self, toon, catalogItem):
        """Return None if everything is ok and we don't have mismatched sex."""
        if ((catalogItem.forBoysOnly() and toon.dna.getGender() == 'f') or (catalogItem.forGirlsOnly() and toon.dna.getGender() == 'm')):
            return ToontownGlobals.P_WillNotFit
        return None

    def checkGiftable(self, toon, catalogItem ):
        """Return None if everything is ok and the item is giftable."""
        if not catalogItem.isGift():
            return ToontownGlobals.P_NotAGift
        return None

    def checkFullMailbox(self, toon, catalogItem):
        """Return None if he has space in his mailbox."""
        # TODO make this check awardMailboxContents
        rAv = toon
        result = None
        if len(rAv.awardMailboxContents) + len(rAv.onAwardOrder) >= ToontownGlobals.MaxMailboxContents:
            if len(rAv.awardMailboxContents) == 0:
                result = ToontownGlobals.P_OnAwardOrderListFull
            else:
                result = ToontownGlobals.P_AwardMailboxFull
        return result    

    def checkDuplicate(self, toon, catalogItem):
        """Return None if he doesn't have this item yet. an error code from GiveAwardErrors otherwise"""
        result = None
        checkDup = toon.checkForDuplicateItem(catalogItem)
        if checkDup == ToontownGlobals.P_ItemInMailbox :
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInMailbox
        elif checkDup == ToontownGlobals.P_ItemOnGiftOrder :
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInGiftQueue
        elif checkDup == ToontownGlobals.P_ItemOnOrder :
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInOrderedQueue
        elif checkDup == ToontownGlobals.P_ItemInCloset :
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInCloset
        elif checkDup == ToontownGlobals.P_ItemAlreadyWorn :
            result = AwardManagerConsts.GiveAwardErrors.AlreadyBeingWorn
        elif checkDup == ToontownGlobals.P_ItemInAwardMailbox:
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInAwardMailbox
        elif checkDup == ToontownGlobals.P_ItemOnAwardOrder:
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInThirtyMinuteQueue
        elif checkDup == ToontownGlobals.P_ItemInMyPhrases:
            result = AwardManagerConsts.GiveAwardErrors.AlreadyInMyPhrases
        elif checkDup == ToontownGlobals.P_ItemInPetTricks:
            result = AwardManagerConsts.GiveAwardErrors.AlreadyKnowDoodleTraining
        elif checkDup:
            # HACK: store the catalog error on self
            # this will not work properly if the error checking happens after a second call to this method
            self._catalogError = checkDup
            result = AwardManagerConsts.GiveAwardErrors.GenericAlreadyHaveError
        return result                        

    def validateItem(self, toon, catalogItem):
        """Returns (True, AwardManagerConsts.GiveAwardErrors.Success) if everything is ok, otherwise returns (False,<error reason>)"""
        retcode = None
        retcode = self.checkGender(toon, catalogItem)
        if retcode:
            return (False, AwardManagerConsts.GiveAwardErrors.WrongGender)
        retcode = self.checkGiftable(toon, catalogItem)
        if retcode:
            return (False, AwardManagerConsts.GiveAwardErrors.NotGiftable)        
        retcode= self.checkFullMailbox(toon, catalogItem)
        if retcode:
            return (False, AwardManagerConsts.GiveAwardErrors.FullAwardMailbox)
        result = self.checkDuplicate(toon, catalogItem)
        if result:
            return (False, result)
        return (True, "success")
        # add other checks here

    def giveItemToToon(self, toon, catalogItem, specialEventId, specialCommands):
        """All checks passed, give the toon the item. Returns True if all ok"""
        # Temp hack, rely on delivery manager to gift the item
        result = True
        #itemBlob = catalogItem.getBlob(store = CatalogItem.Customization)
        #uber.air.deliveryManager.giveGiftItemToAvatar(itemBlob, toon.doId)
        # first give it immediately, going directly to awardMailbox
        catalogItem.specialEventId = specialEventId
        if specialCommands == GiveImmediately:
            curItemList = toon.awardMailboxContents
            curItemList.append(catalogItem)
            newBlob = curItemList.getBlob(store = CatalogItem.Customization )
            self.air.sendUpdateToDoId(
                    "DistributedToon",
                    "setAwardMailboxContents", toon.doId, [newBlob])
        else:
            #import pdb; pdb.set_trace()
            # Get the current time in minutes.
            now = (int)(time.time() / 60 + 0.5)
            if specialCommands == GiveAfterOneMinute:
                delay = 1.
            else:
                delay = AwardManagerDelayMinutes
            future = now + delay
            curOnAwardOrderList = toon.onAwardOrder
            catalogItem.deliveryDate = future
            curOnAwardOrderList.append(catalogItem)
            newBlob = curOnAwardOrderList.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            self.air.sendUpdateToDoId(
                    "DistributedToon",
                    "setAwardSchedule", toon.doId, [newBlob])
        return result

    def tryToRemoveAward(self,toon, catalogItem, specialEventId):
        """Try to remove the item from the awardOnOrder."""
        result = (True, "award removed")
        if catalogItem in toon.onAwardOrder:
            toon.onAwardOrder.remove(catalogItem)
            newBlob = toon.onAwardOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            self.air.sendUpdateToDoId(
                    "DistributedToon",
                    "setAwardSchedule", toon.doId, [newBlob])
        else:
            result = (False,"item not in 30 minute award queue")
        return result

    def nukeAllAwards(self,toon):
        """Try to remove all awards."""
        if len(toon.onAwardOrder) ==0 and len (toon.awardMailboxContents) == 0:            
            result = (False, "no awards to remove")
        else:
            import pdb; pdb.set_trace()
            numInMailbox = len (toon.awardMailboxContents)
            numInQueue = len(toon.onAwardOrder)
            toon.awardMailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
            toon.onAwardOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)       
            newBlob = toon.onAwardOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            self.air.sendUpdateToDoId(
                    "DistributedToon",
                    "setAwardSchedule", toon.doId, [newBlob])
            newAwardBlob = toon.awardMailboxContents.getBlob(store = CatalogItem.Customization)
            self.air.sendUpdateToDoId(
                    "DistributedToon",
                    "setAwardMailboxContents", toon.doId, [newAwardBlob])
        
            result = (True,"awards nuked, in mailbox=%d, in queue=%d" % (numInMailbox, numInQueue))
        return result
        

    def gotTheToons(self, isDcRequest, dcId, toonObjDict, catalogItem, specialEventId, browserReplyTo, specialCommands, echoBack):
        """Validate then give the catalog item to the toons."""
        assert self.notify.debugStateCall(self)
        try:
            giveAwardErrors = {}
            catalogErrors = {}
            tableValues = {}
            wrongGenderToonIds = []
            if specialCommands in (GiveAfterDelayTime, GiveImmediately, GiveAfterOneMinute, ):
                for toonId in toonObjDict:
                    toon = toonObjDict[toonId]
                    if toon:
                        success, error = self.validateItem(toon, catalogItem)
                        if error == AwardManagerConsts.GiveAwardErrors.WrongGender:
                            wrongGenderToonIds.append(toonId)                        
                        if success:
                            success = self.giveItemToToon(toon, catalogItem, specialEventId, specialCommands)
                            if success:
                                giveAwardErrors[toonId] = AwardManagerConsts.GiveAwardErrors.Success
                            else:
                                giveAwardErrors[toonId] = AwardManagerConsts.GiveAwardErrors.UnknownError
                        else:
                            giveAwardErrors[toonId] = error
                            if error == AwardManagerConsts.GiveAwardErrors.GenericAlreadyHaveError:
                                catalogErrors[toonId] = self._catalogError
                    else:
                        giveAwardErrors[toonId] = AwardManagerConsts.GiveAwardErrors.UnknownToon
            elif specialCommands == TryToRemove:
                for toonId in toonObjDict:
                    toon = toonObjDict[toonId]
                    if toon:
                        success, errorStr = self.tryToRemoveAward(toon, catalogItem, specialEventId)
                        tableValues[toonId] = errorStr
            elif specialCommands == NukeAllAwards:
                for toonId in toonObjDict:
                    toon = toonObjDict[toonId]
                    if toon:
                        success, errorStr = self.nukeAllAwards(toon)
                        tableValues[toonId] = errorStr

            self.air.writeServerEvent('giveAwardResults',0,"%s|%s|%s" % (echoBack, str(catalogItem), str(giveAwardErrors))) 
                        
            if not isDcRequest:
                self.sendResultsBack(giveAwardErrors, catalogErrors, tableValues, toonObjDict, catalogItem, specialEventId, browserReplyTo, wrongGenderToonIds, echoBack)
            else:
                assert len(giveAwardErrors) == 1
                errorCode = giveAwardErrors[giveAwardErrors.keys()[0]]
                self.sendGiveAwardToToonReply(dcId, errorCode)
        except Exception,e:
            if not isDcRequest:
                browserReplyTo.respondXML(AwardResponses.awardGiveFailureXML % ("Catastrophic failure in gotTheToons %s" % str(e)))
            else:
                raise

    def sendResultsBack(self, giveAwardErrors, catalogErrors, tableValues, toonObjDict, catalogItem, specialEventId, browserReplyTo, wrongGenderToonIds, echoBack):
        """For each toon, tell if they got the item or not."""
        self.notify.debugStateCall(self)
        header,body,footer,help= self.getMainMenu()
        
        body = body = """<BODY><div id="contents"><center><P>"""
        body += echoBack
        body += """<h4>Results:</h4>
        <table border="1">
        """
        # result for each toon is either in giveAwardErrors or tableValues
        # convert error codes in giveAwardErrors into string in tableValues
        gae = AwardManagerConsts.GiveAwardErrors
        for toonId in giveAwardErrors:
            error = giveAwardErrors[toonId]
            errStr = ''
            if error == gae.GenericAlreadyHaveError:
                errStr = "unknown error description for checkDuplicate %s" % catalogErrors[toonId]
            else:
                tableValues[toonId] = AwardManagerConsts.GiveAwardErrorStrings[error]
        for toonId in tableValues:
            name = ""
            if toonObjDict[toonId]:
                name = toonObjDict[toonId].getName()
            body += "<tr><td>" + str(toonId) + "</td><td>" + tableValues[toonId] + "</td><td>" + name + "</td>"+"</tr>\n"
        body += """
        </table>
        """
        if wrongGenderToonIds:
            body += "<br />Wrong Gender Toon Ids:\n"
            for toonId in wrongGenderToonIds:
                body += "%d " % toonId
            body += "\n"
        body += """
        </body>
        """
        browserReplyTo.respond(header +body+ help+footer)

    def giveAwardToToon(self, context, replyToDoId, replyToClass, avId, awardType, awardItemId):
        self.air.writeServerEvent('giveAwardCodeRequest', avId, '%s|%s' %(str(awardType), str(awardItemId)))
        dcId = self._dcRequestSerialGen.next()
        self._dcId2info[dcId] = ScratchPad(replyToClass=replyToClass,
                                           replyToDoId=replyToDoId,
                                           context=context)
        isDcRequest = True
        catalogItem = self._getCatalogItemObj(awardType, awardItemId)
        specialEventId = 1
        browserReplyTo = None
        specialCommands = GiveAfterOneMinute
        echoBack = ''
        GetToonsRequest(self, isDcRequest, dcId, [avId], catalogItem, specialEventId, browserReplyTo,
                        specialCommands, echoBack)
        
    def sendGiveAwardToToonReply(self, dcId, result):
        info = self._dcId2info.pop(dcId)
        self.air.dispatchUpdateToGlobalDoId(info.replyToClass, "giveAwardToToonResult",
                                            info.replyToDoId, [info.context, result])

    def getMainMenu(self):
        """Create the main menu with forms for input."""
        header = """<HTML><HEAD><TITLE>Main Menu: Toontown Award  Manager</TITLE><link rel="stylesheet" type="text/css" href="/default.css">
        </HEAD>"""

        body = """<BODY><div id="contents"><center><P>"""
        body += """
            Enter Award Info
            <form>ToonIds:
            <input type="text" name="toonIds" />
            <br />
            SpecialEventId:
            <select name="specialEventId" />
              <option value="1">Fishing1</option>
              <option value="2">Fishing2</option>
              <option value="3">racing1</option>
              <option value="4">generic</option>
            </select>
            <br />
            Prize:
            <input type="text" name="prize" />
            <br />
            <input type="submit" value="Submit" />
            </form>            
            """
            
        footer = """</tbody></table></P></center></div><div id="footer">Toontown AwardManager</div></BODY></HTML>"""
        help = """<table height = "15%"></table><P><table width = "60%"><caption>Note</caption><tr><th scope=col>- Report any prizing issues to  chris.barkoff@disney.com<br>- Report any technical issues to redmond.urbino@disney.com</th></tr></table></P>"""
        return (header,body,footer,help)

    @classmethod
    def getClothingChoices(cls):
        """Return a dictionary of clothing choices. Key is the description, clothingtype are values."""
        values = {}
        for key in CatalogClothingItem.ClothingTypes.keys():
            clothingItem = CatalogClothingItem.ClothingTypes[key]
            typeOfClothes = clothingItem[0]
            styleString = clothingItem[1]
            if typeOfClothes in (CatalogClothingItem.AShirt,
                                 CatalogClothingItem.ABoysShirt, CatalogClothingItem.AGirlsShirt):
                textString = TTLocalizer.AwardMgrShirt
                # if its an exclusive boy or girl item, then say so
                if typeOfClothes == CatalogClothingItem.ABoysShirt:
                   textString += ' ' + TTLocalizer.AwardMgrBoy 
                elif typeOfClothes == CatalogClothingItem.AGirlsShirt:
                   textString += ' ' + TTLocalizer.AwardMgrGirl 
                else:
                   textString += ' ' + TTLocalizer.AwardMgrUnisex                             
                textString +=  ' ' + TTLocalizer.ShirtStylesDescriptions[styleString]
                if textString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % textString)
                values[textString] = key

        # do a 2nd for loop to ensure bottoms always goes last
        for key in CatalogClothingItem.ClothingTypes.keys():
            clothingItem = CatalogClothingItem.ClothingTypes[key]
            typeOfClothes = clothingItem[0]
            styleString = clothingItem[1]
            if typeOfClothes in (CatalogClothingItem.AShorts, CatalogClothingItem.ABoysShorts, 
                                 CatalogClothingItem.AGirlsShorts, CatalogClothingItem.AGirlsSkirt):
                textString = ""
                if typeOfClothes == CatalogClothingItem.AGirlsSkirt:
                    textString =  TTLocalizer.AwardMgrSkirt 
                else:
                    textString =  TTLocalizer.AwardMgrShorts 
                # if its an exclusive boy or girl item, then say so
                if typeOfClothes == CatalogClothingItem.ABoysShorts:
                   textString += ' ' + TTLocalizer.AwardMgrBoy
                elif typeOfClothes in (CatalogClothingItem.AGirlsShorts, CatalogClothingItem.AGirlsSkirt):
                   textString += ' ' + TTLocalizer.AwardMgrGirl
                else:
                    textString += ' ' + TTLocalizer.AwardMgrUnisex
                textString += ' ' + TTLocalizer.BottomStylesDescriptions[styleString]
                if textString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % textString)
                values[textString] = key
        return values

    @classmethod
    def getFurnitureChoices(cls):
        """Return a dictionary of furniture choices. Key is the description , values is the furniture type key"""
        values = {}
        for key in CatalogFurnitureItem.FurnitureTypes.keys():
            furnitureItem = CatalogFurnitureItem.FurnitureTypes[key]
            typeOfFurniture = key
            # we must not give animted furniture choices, the item type is wrong for it
            if typeOfFurniture in CatalogAnimatedFurnitureItem.AnimatedFurnitureItemKeys:
                continue
            descString = TTLocalizer.AwardManagerFurnitureNames[typeOfFurniture]
            if descString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getSpeedChatChoices(cls):
        """Return a dictionary of speed chat choices. Key is the description , values is the chat id"""
        values = {}
        allChatItems = CatalogGenerator.getAllChatItemsSold()
        for chatItem in allChatItems:
            speedChatKey = chatItem.customIndex
            textString = OTPLocalizer.CustomSCStrings[speedChatKey]
            # I really can't mess with the strings, I'll add the speedChatKey at the end
            keyStr = "%5d" % speedChatKey
            textString = keyStr +  " " + textString
            # javascript messes up with a " in the string
            textString = textString.replace('"',"'")
            if textString in values:
                cls.notify.error("fix duplicate %s" % textString)
            values[textString] = speedChatKey
        return values

    @classmethod
    def getEmoteChoices(cls):
        """Return a dictionary of emote choices. Key is the description , values is the emote id"""
        values = {}
        for key in OTPLocalizer.EmoteFuncDict.keys():
            descString = key
            emoteIndex = OTPLocalizer.EmoteFuncDict[key]
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = emoteIndex
        return values

    @classmethod
    def getBeanChoices(cls):
        """Return a dictionary of bean choices. Key is the description , values is the amount of beans"""
        values = {}        
        for key in JellybeanRewardValues:
            descString = "%3d" % key
            if descString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getWallpaperChoices(cls):
        """Return a dictionary of wallpaper choices. Key is the description , values is the wallpaper id"""
        values = {}
        for key in CatalogWallpaperItem.WallpaperTypes.keys():
            # the comments on CatalogWallpaperItem say 2920 to 2980 are problematic, so don't include them
            if key in (2920, 2930, 2940, 2950, 2960, 2970, 2980):
                continue
            # we have duplicate names, just add the key to be unique
            descString = "%5d " % key
            # ok it looks like some items are never offered, so if there's no name for it
            # lets not include it
            if key in TTLocalizer.WallpaperNames:
                descString += TTLocalizer.WallpaperNames[key]
                if descString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % descString)
                values[descString] = key
        return values

    @classmethod
    def getWindowViewChoices(cls):
        """Return a dictionary of window choices. Key is the description , values is the wallpaper id"""
        values = {}
        for key in CatalogWindowItem.WindowViewTypes.keys():
            descString = ""
            descString += TTLocalizer.WindowViewNames[key]
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values 

    @classmethod
    def getFlooringChoices(cls):
        """Return a dictionary of flooring choices. Key is the description , values is the wallpaper id"""
        values = {}
        for key in CatalogFlooringItem.FlooringTypes.keys():
            descString = "%5d " % key # add key to make it unique
            descString += TTLocalizer.FlooringNames[key]
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getMouldingChoices(cls):
        """Return a dictionary of moulding choices. Key is the description , values is the wallpaper id"""
        values = {}
        for key in CatalogMouldingItem.MouldingTypes.keys():
            descString = "%5d " % key # add key to make it unique
            descString += TTLocalizer.MouldingNames[key]
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values    

    @classmethod
    def getWainscotingChoices(cls):
        """Return a dictionary of wainscotting choices. Key is the description , values is the wallpaper id"""
        values = {}
        for key in CatalogWainscotingItem.WainscotingTypes.keys():
            descString = "" #%5d " % key # add key to make it unique
            descString += TTLocalizer.WainscotingNames[key]
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getPetTrickChoices(cls):
        """Return a dictionary of pet trick choices. Key is the description , values is the wallpaper id"""
        values = {}
        allTricks = CatalogPetTrickItem.getAllPetTricks()
        for oneTrick in allTricks:
            descString = "" #%5d " % key # add key to make it unique
            descString += oneTrick.getName()
            key = oneTrick.trickId
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getRentalChoices(cls):
        """Return a dictionary of pet rental choices. Key is the description , values is the wallpaper id"""
        values = {}
        allRentals = CatalogRentalItem.getAllRentalItems()
        for oneRental in allRentals:
            descString = "" #%5d " % key # add key to make it unique
            descString += oneRental.getName()
            key = oneRental.typeIndex
            if descString in values:
                cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values     

    @classmethod
    def getAnimatedFurnitureChoices(cls):
        """Return a dictionary of furniture choices. Key is the description , values is the furniture type key"""
        values = {}
        for key in CatalogAnimatedFurnitureItem.AnimatedFurnitureItemKeys:
            furnitureItem = CatalogFurnitureItem.FurnitureTypes[key]
            typeOfFurniture = key
            descString = TTLocalizer.AwardManagerFurnitureNames[typeOfFurniture]
            if descString in values:
                    cls.notify.error("Fix %s, descriptions must be unique" % descString)
            values[descString] = key
        return values

    @classmethod
    def getReversedAwardChoices(cls):
        """The key in the returned dictionaries should be catalog item numbers, the value should be desc strings."""
        if hasattr(cls, '_revAwardChoices'):
            return cls._revAwardChoices
        result = {}
        awardChoices = cls.getAwardChoices()
        for itemType in awardChoices:
            reversedDict = {}
            curDict = awardChoices[itemType]
            for descString in curDict:
                itemId = curDict[descString]
                if itemId in reversedDict:
                    cls.notify.error("item %s already in %s" % (itemId, reversedDict))
                reversedDict[itemId] = descString
            result[itemType] = reversedDict
        cls._revAwardChoices = result
        return result
                
    @classmethod
    def getAwardChoices(cls):
        """Return a tree of the choices for our drop down list."""
        # static data, cache it
        if hasattr(cls, '_awardChoices'):
            return cls._awardChoices
        result = {}
        for itemType in CatalogItemTypes.CatalogItemTypes.values():
            if itemType in (CatalogItemTypes.INVALID_ITEM, CatalogItemTypes.GARDENSTARTER_ITEM,
                            CatalogItemTypes.POLE_ITEM, CatalogItemTypes.GARDEN_ITEM,
                            CatalogItemTypes.NAMETAG_ITEM, CatalogItemTypes.TOON_STATUE_ITEM):
                # we really can't give this out as awards, so don't add them to the choices
                continue
            if itemType == CatalogItemTypes.CLOTHING_ITEM:
                values = cls.getClothingChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.FURNITURE_ITEM:
                values = cls.getFurnitureChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.CHAT_ITEM:
                values = cls.getSpeedChatChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.EMOTE_ITEM:
                values = cls.getEmoteChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.BEAN_ITEM:
                values = cls.getBeanChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.WALLPAPER_ITEM:
                values = cls.getWallpaperChoices()
                result[itemType] = values   
            elif itemType == CatalogItemTypes.WINDOW_ITEM:
                values = cls.getWindowViewChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.FLOORING_ITEM:
                values = cls.getFlooringChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.MOULDING_ITEM:
                values = cls.getMouldingChoices()
                result[itemType] = values    
            elif itemType == CatalogItemTypes.WAINSCOTING_ITEM:
                values = cls.getWainscotingChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.PET_TRICK_ITEM:
                values = cls.getPetTrickChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.RENTAL_ITEM:
                values = cls.getRentalChoices()
                result[itemType] = values
            elif itemType == CatalogItemTypes.ANIMATED_FURNITURE_ITEM:
                values = cls.getAnimatedFurnitureChoices()
                result[itemType] = values   
                
            else:
                values = {"choice1": "Unimplemented One", "choice2": "Unimplemented Two"}
                result [itemType] = values
        cls._awardChoices = result
        return result

    @staticmethod
    def getAwardTypeName(awardType):
        return TTLocalizer.CatalogItemTypeNames[awardType]

    @classmethod
    def getAwardText(cls, awardType, awardId):
        rAwardChoices = cls.getReversedAwardChoices()
        return rAwardChoices[awardType][awardId]

    def getExperimentalMenu(self):
        """Stuff to fool around with."""
        header = """
        <head>
        <TITLE>Main Menu: Toontown Award  Manager</TITLE><link rel="stylesheet" type="text/css" href="/default.css">
        <script type="text/javascript">
        function message()
        {
        alert("This alert box was called with the onload event");
        }

        function setOptions(chosen) {
        var selbox = document.myform.opttwo;
        selbox.options.length = 0;
        
        if (chosen == " ") {
          selbox.options[selbox.options.length] = new Option('Please select one of the options above first',' ');

        }\n"""

        
        for itemType in self.awardChoices:
            header += '\tif (chosen == "%s") {\n' % itemType
            secondChoices = self.awardChoices[itemType]
            sortedKeys = secondChoices.keys()
            sortedKeys.sort()
            for key in sortedKeys:
                header += "\t\tselbox.options[selbox.options.length] = new "
                header += 'Option("%s","%s");\n' % (key, secondChoices[key])
            header += '\t}\n'

        header += """
        
        }        
        </script>
        </head>
        """

        help = ""
        footer = ""
        body = """
        <html>
        <body ><center>
        <div id="contents" align="center"> 
        <form name="myform" action="awardGive">
        ToonIds:<input type="text" name="toonIds" size="50" />
            <br />
            SpecialEventId:
            <select name="specialEventId" />
            """
        for eventId in TTLocalizer.SpecialEventNames :
            body += '<option value="%d">%s</option>' % (eventId, TTLocalizer.SpecialEventNames[eventId])
        body += """    </select>
            <br />
        Item Type<select name="optone" size="1"
        onchange="setOptions(document.myform.optone.options[document.myform.optone.selectedIndex].value);">
        <option value=" " selected="selected"> </option>
        """
                
        for itemType in self.awardChoices:
           body += '<option value="%s">%s</option>\n' % (str(itemType), TTLocalizer.CatalogItemTypeNames[itemType])

        body += """
        </select><br>
        Item Details<select name="opttwo" size="1">
        <option value=" " selected="selected">Please select one of the options above first</option>
        </select>
        <br>
        Special Commands:
           <select name="specialCommands" />
        """

        commandsList = SpecialCommandStrs.keys()
        commandsList.sort()
        if uber.config.GetBool('awards-immediate'):
            commandsList.remove(GiveImmediately)
            commandsList.insert(0,GiveImmediately)
        for command in commandsList:
            body += "<option value=%d>%s</option>" %(command, SpecialCommandStrs[command])
        body +="""   </select>
        <br />
        <input type="submit" value="Submit" />
        <!--
        <input type="button" name="go" value="Value Selected"
        onclick="alert(document.myform.opttwo.options[document.myform.opttwo.selectedIndex].value);">
        -->
       
        </form>        
        </script>
        </div>
        
        """
        help = """<table height = "15%"></table><P><table width = "60%"><caption>Note</caption><tr><th scope=col>- Use give award immediately only to test the award on your own toon. Try to remove the award may fail if 30 minutes have gone by since the award was given.<br><br>- Use Nuke All Awards only if the regular players can't enter toontown.<br><br>- Report any prizing issues to  chris.barkoff@disney.com<br>- Report any issues to redmond.urbino@disney.com</th></tr></table></P>"""
        footer = """</tbody></table></P></center><div id="footer">Toontown Award Manager</div></BODY></HTML>"""
        return (header, body, footer, help)
