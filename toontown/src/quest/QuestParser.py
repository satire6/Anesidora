
import sys
import os
import tokenize
import copy

from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import AppRunnerGlobal
from pandac.PandaModules import *
from direct.showbase import DirectObject
import BlinkingArrows
from toontown.toon import ToonHeadFrame
from toontown.char import CharDNA
from toontown.suit import SuitDNA
from toontown.char import Char
from toontown.suit import Suit
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from otp.speedchat import SpeedChatGlobals
from toontown.ai import DistributedBlackCatMgr
from direct.showbase import PythonUtil
from direct.interval.IntervalGlobal import *

notify = DirectNotifyGlobal.directNotify.newCategory("QuestParser")

"""
import QuestParser
reload(QuestParser)
QuestParser.init()
npc = base.cr.doId2do[30004157]
nmp = QuestParser.NPCMoviePlayer("quest_assign_101", base.localAvatar, npc)
nmp.play()

==================================================
GRAMMAR
==================================================

# Every script must start with a unique ID string
ID scriptId

# Output a notify debug message
# Note: QuestParser notify category must have debug on to see messages
DEBUG string

# Call this scriptId, return when it is finished
CALL scriptId

# Lock the local toon down
LOCK_LOCALTOON

# Free local toon
FREE_LOCALTOON

# Load this model file and store it in variable "nodeName"
LOAD nodeName fileName [subnodeName]

LOAD_SFX sfxName fileName
# Load load sfx except conditional on language
LOAD_DIALOGUE dialogueName fileName
# Load dialogue, inserting appropriate classic char name in filename
LOAD_CC_DIALOGUE dialogueName fileName

# Load this character/suit
LOAD_CHAR name charDnaType
UNLOAD_CHAR name
LOAD_CLASSIC_CHAR name
LOAD_SUIT name suitDnaType

# Common node path manipulation tools
REPARENTTO nodeName nodeName [subnodeName]
WRTREPARENTTO nodeName nodeName [subnodeName]
SHOW nodeName
HIDE nodeName
POS nodeName x y z
HPR nodeName h p r
SCALE nodeName x y z

PLAY_SFX soundName [looping]
STOP_SFX soundName

# Common lerps (changing a node over time)
LERP_POS nodeName x y z t
LERP_HPR nodeName h p r t
LERP_SCALE nodeName x y z t
LERP_POSHPRSCALE nodeName x y z h p r sx sy sz t
LERP_COLOR nodeName r g b a r g b a t
LERP_COLOR_SCALE nodeName r g b a r g b a t

# Adjust depth write for node paths under aspect 2d
DEPTH_WRITE_ON nodeName fDepthWrite priority
DEPTH_WRITE_OFF nodeName
DEPTH_TEST_ON nodeName fDepthTest priority
DEPTH_TEST_OFF nodeName

# put nodepaths into bins
SET_BIN nodeName binName [sortOrder]
CLEAR_BIN nodeName

# Cleanup the quest movie npc
FINISH_QUEST_MOVIE

# Pause this script for <time> seconds
WAIT time

# Show two red blinking arrows on the gui at these positions
# These are useful for help mode
ARROWS_ON x y h x2 y2 h2
ARROWS_OFF

# Makes a nodepath 'throb' to a colorscale with period t
START_THROB node r g b a t
STOP_THROB

# Show this toon as a popup overlay with a head and chat window
# This is useful for tutorial instruction over top the book
# onoff is a bool 0/1 to turn it on and off
TOON_HEAD avatar x y onoff [scale]

# Make this avatar say this string
# npc and toon are predefined for you
CHAT avatar TTLocalizer.String [chatFlagString] [dialogue]

# Make this avatar clear his chat
CLEAR_CHAT avatar

# Make the npc say this string with next button confirmation
CHAT_CONFIRM avatar TTLocalizer.String [quitButton] [chatFlagString] [dialogue]
# Locally make the npc say this string with next button confirmation
# For use when the NPC is giving advice to a toon in a local context (like the Tutorial)
LOCAL_CHAT_CONFIRM avatar TTLocalizer.String [quitButton] [chatFlagString] [dialogue]
# Like LOCAL_CHAT_CONFIRM except that all occurences of '%s' in the
# string are replaced with the toAvatar's name
LOCAL_CHAT_TO_CONFIRM avatar toAvatar TTLocalizer.String [quitButton] [chatFlagString] [dialogue]

# Common actor commands
PLAY_ANIM avatar animName [playRate]
LOOP_ANIM avatar animName [playRate]

# Pause this script until we hear this event
WAIT_EVENT string

# Send this event
SEND_EVENT string

# Set a temporary variable
SET varName value

# Show and hide the Toon friends list
SHOW_FRIENDS_LIST
HIDE_FRIENDS_LIST

# Set the laffmeter
ADD_LAFFMETER maxHp
LAFFMETER hp maxHp
OBSCURE_LAFFMETER obscure

# Add <number> items to inventory at (track, level) slot
# Note that the AI does not know about this, this is purely
# for client side show
ADD_INVENTORY track level number

# Set <number> items to inventory at (track, level) slot
# Note that the AI does not know about this, this is purely
# for client side show
SET_INVENTORY track level number
# Adjust Y offset of inventory track to compensate for being in 3D
SET_INVENTORY_YPOS track level yPos

# -1 = noDetail
# 0 = hideDetail
# 1 = showDetail
SET_INVENTORY_DETAIL detailLevel

# Show a run-up of the squirt and throw gag tracks; intended to be used
# in the gag tutorial, just after first minigame
SHOW_THROW_SQUIRT_PREVIEW

# Set the volume of the activity music for the toontorial
# so it doesn't overwhelm the dialogue (currently only Japanese version)
SET_MUSIC_VOLUME level

# At the end of the movie, or if the movie times out, run this
# command, which can be almost any other quest movie command with
# the exception of commands that must wait for input
UPON_TIMEOUT <command>

"""


# Dictionary mapping ID to script
lineDict = {}

# Maps variable names to actual variables that may be useful
# for all movies to have defined
globalVarDict = {}

curId = None

def init():
    # Fill in the globalVarDict. We cannot do this at import
    # time because not all the variables have been defined
    globalVarDict.update({
        'render' : render,
        'camera' : camera,
        'hidden' : hidden,
        'aspect2d' : aspect2d,
        'localToon' : base.localAvatar,
        'laffMeter' : base.localAvatar.laffMeter,
        'inventory' : base.localAvatar.inventory,
        'bFriendsList' : base.localAvatar.bFriendsList,
        'book' : base.localAvatar.book,
        'bookPrevArrow' : base.localAvatar.book.prevArrow,
        'bookNextArrow' : base.localAvatar.book.nextArrow,
        'bookOpenButton' : base.localAvatar.book.bookOpenButton,
        'bookCloseButton' : base.localAvatar.book.bookCloseButton,
        'chatNormalButton' : base.localAvatar.chatMgr.normalButton,
        'chatScButton' : base.localAvatar.chatMgr.scButton,
        # You get one set of arrows to play with
        'arrows' : BlinkingArrows.BlinkingArrows(),
        })

def clear():
    globalVarDict.clear()

def readFile(filename):
    scriptFile = StreamReader(vfs.openReadFile(filename, 1), 1)
    gen = tokenize.generate_tokens(scriptFile.readline)
    line = getLineOfTokens(gen)
    
    while line is not None:

        # If the line is blank, get the next one
        if line == []:
            line = getLineOfTokens(gen)
            continue
        
        if (line[0] == "ID"):
            parseId(line)
        else:
            if curId is None:
                notify.error("Every script must begin with an ID")
            else:
                lineDict[curId].append(line)
        line = getLineOfTokens(gen)

def getLineOfTokens(gen):
    tokens = []
    nextNeg = 0
    token = gen.next()
    # The end of the file is special
    if token[0] == tokenize.ENDMARKER:
        return None
    # Eat tokens until you get a newline
    while (token[0] != tokenize.NEWLINE) and (token[0] != tokenize.NL):
        #if notify.getDebug():
        #    tokenize.printtoken(*token)
        # Skip comments
        if token[0] == tokenize.COMMENT:
            pass
        # Keep track of negative operators since the tokenizer
        # treats -1 as two separate tokens, '-' and '1'. We'll just
        # keep a flag here
        elif (token[0] == tokenize.OP) and (token[1] == '-'):
            nextNeg = 1
        elif token[0] == tokenize.NUMBER:
            if nextNeg:
                tokens.append(-eval(token[1]))
                nextNeg = 0
            else:
                tokens.append(eval(token[1]))
        elif token[0] == tokenize.STRING:
            tokens.append(eval(token[1]))
        elif token[0] == tokenize.NAME:
            tokens.append(token[1])
        else:
            notify.warning("Ignored token type: %s on line: %s" % (tokenize.tok_name[token[0]], token[2][0]))
        token = gen.next()
    return tokens

def parseId(line):
    assert(len(line) == 2)
    global curId
    curId = line[1]
    notify.debug("Setting current scriptId to: %s" % curId)
    if questDefined(curId):
        notify.error("Already defined scriptId: %s" % curId)
    else:
        lineDict[curId] = []

def questDefined(scriptId):
    return lineDict.has_key(scriptId)
                    

class NPCMoviePlayer(DirectObject.DirectObject):

    def __init__(self, scriptId, toon, npc):
        DirectObject.DirectObject.__init__(self)
        self.scriptId = scriptId
        self.toon = toon
        # Uh, is this localToon?
        self.isLocalToon = (self.toon == base.localAvatar)
        self.npc = npc
        self.privateVarDict = {}
        self.toonHeads = {}
        self.chars = []
        self.uniqueId = ('scriptMovie_'
                         + str(self.scriptId)
                         + '_' + str(toon.getDoId())
                         + '_' + str(npc.getDoId()))
        # All scripts get toon and npc as private variables
        self.setVar('toon', self.toon)
        self.setVar('npc', self.npc)
        # Dictionary mapping event to track list
        self.chapterDict = {}
        # Track to play when the movie is over for cleanup
        self.timeoutTrack = None
        # The track that is currently playing
        self.currentTrack = None

    # Look for this var first in the private dict, then in the global dict
    def getVar(self, varName):
        if self.privateVarDict.has_key(varName):
            return self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            return globalVarDict[varName]
        elif (varName.find('tomDialogue') > -1) or (varName.find('harryDialogue') > -1):
            notify.warning("%s getting referenced. Tutorial Ack: %d  \
                                Place: %s" %(varName, base.localAvatar.tutorialAck, base.cr.playGame.hood))
            return None
        else:
            notify.error("Variable not defined: %s" % (varName))

    def delVar(self, varName):
        if self.privateVarDict.has_key(varName):
            del self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            del globalVarDict[varName]
        else:
            notify.warning("Variable not defined: %s" % (varName))
        
    # Set a private variable
    def setVar(self, varName, var):
        self.privateVarDict[varName] = var

    def cleanup(self):
        if self.currentTrack:
            self.currentTrack.pause()
            self.currentTrack = None
        self.ignoreAll()
        taskMgr.remove(self.uniqueId)
        for toonHeadFrame in self.toonHeads.values():
            toonHeadFrame.destroy()
        while self.chars:
            self.__unloadChar(self.chars[0])
            
        del self.toonHeads
        del self.privateVarDict
        del self.chapterDict
        del self.toon
        del self.npc
        del self.timeoutTrack

    def __unloadChar(self, char):
        char.removeActive()
        if (char.style.name == 'mk' or char.style.name == 'mn'):
            char.stopEarTask()
        char.delete()
        self.chars.remove(char)

    def timeout(self, fFinish = 0):        
        if self.timeoutTrack:
            if fFinish:
                # Do a finish so that we don't leave the track hanging around
                # Hopefully this is all instantaneous stuff
                self.timeoutTrack.finish()
            else:
                self.timeoutTrack.start()

    def finishMovie(self):
        self.npc.finishMovie(self.toon, self.isLocalToon, 0.0)

    def playNextChapter(self, eventName, timeStamp = 0.0):
        trackList = self.chapterDict[eventName]
        if trackList:
            self.currentTrack = trackList.pop(0)
            self.currentTrack.start()
        else:
            notify.debug("Movie ended waiting for an event (%s)" %
                         eventName)

    def play(self):
        lineNum = 0
        self.currentEvent = 'start'
        lines = lineDict.get(self.scriptId)
        if lines is None:
            notify.error("No movie defined for scriptId: %s" % self.scriptId)

        # List of intervals for the current chapter
        chapterList = []
        # List of intervals to run upon timeout
        timeoutList = []
        
        for line in lines:
            lineNum += 1
            command = line[0]

            if command == 'UPON_TIMEOUT':
                uponTimeout = 1
                iList = timeoutList
                # Strip off the UPON_TIMEOUT token and continue
                line = line[1:]
                command = line[0]
            else:
                uponTimeout = 0
                iList = chapterList

            # These commands are processed by all Toons in the room
            if command == 'CALL':
                if uponTimeout:
                    self.notify.error("CALL not allowed in an UPON_TIMEOUT")
                iList.append(self.parseCall(line))
                continue
            elif command == 'DEBUG':
                iList.append(self.parseDebug(line))
                continue
            elif command == 'WAIT':
                if uponTimeout:
                    self.notify.error("WAIT not allowed in an UPON_TIMEOUT")
                iList.append(self.parseWait(line))
                continue
            elif command == 'CHAT':
                iList.append(self.parseChat(line))
                continue
            elif command == 'CLEAR_CHAT':
                iList.append(self.parseClearChat(line))
                continue
            elif command == 'FINISH_QUEST_MOVIE':
                # Close the final chapter, putting the cleanup func in there first
                chapterList.append(Func(self.finishMovie))
                continue
            elif command == 'CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error("CHAT_CONFIRM not allowed in an UPON_TIMEOUT")
                # Set the next current event for the next chapter
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName("doneChatPage")
                iList.append(Func(self.acceptOnce,
                                  nextEvent,
                                  self.playNextChapter,
                                  [nextEvent]))
                iList.append(self.parseChatConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                # Set the next current event for the next chapter
                self.currentEvent = nextEvent                
                continue
            elif command == 'LOCAL_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error("LOCAL_CHAT_CONFIRM not allowed in an UPON_TIMEOUT")
                # Set the next current event for the next chapter
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName("doneChatPage")
                iList.append(Func(self.acceptOnce,
                                  nextEvent,
                                  self.playNextChapter,
                                  [nextEvent]))
                iList.append(self.parseLocalChatConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                # Set the next current event for the next chapter
                self.currentEvent = nextEvent                
                continue
            elif command == 'LOCAL_CHAT_PERSIST':
                iList.append(self.parseLocalChatPersist(line))
                continue
            elif command == 'LOCAL_CHAT_TO_CONFIRM':
                if uponTimeout:
                    self.notify.error(
                        "LOCAL_CHAT_TO_CONFIRM not allowed in an UPON_TIMEOUT")
                # Set the next current event for the next chapter
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName("doneChatPage")
                iList.append(Func(self.acceptOnce,
                                  nextEvent,
                                  self.playNextChapter,
                                  [nextEvent]))
                iList.append(self.parseLocalChatToConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                # Set the next current event for the next chapter
                self.currentEvent = nextEvent                
                continue
            elif command == 'CC_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error("CC_CHAT_CONFIRM not allowed in an UPON_TIMEOUT")
                # Set the next current event for the next chapter
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName("doneChatPage")
                iList.append(Func(self.acceptOnce,
                                  nextEvent,
                                  self.playNextChapter,
                                  [nextEvent]))
                iList.append(self.parseCCChatConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                # Set the next current event for the next chapter
                self.currentEvent = nextEvent                
                continue
            elif command == 'CC_CHAT_TO_CONFIRM':
                if uponTimeout:
                    self.notify.error(
                        "CC_CHAT_TO_CONFIRM not allowed in an UPON_TIMEOUT")
                # Set the next current event for the next chapter
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName("doneChatPage")
                iList.append(Func(self.acceptOnce,
                                  nextEvent,
                                  self.playNextChapter,
                                  [nextEvent]))
                iList.append(self.parseCCChatToConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                # Set the next current event for the next chapter
                self.currentEvent = nextEvent                
                continue
            # These commands are only processed by localToon
            if self.isLocalToon:
                if command == 'LOAD':
                    self.parseLoad(line)
                elif command == 'LOAD_SFX':
                    self.parseLoadSfx(line)
                elif command == 'LOAD_DIALOGUE':
                    self.parseLoadDialogue(line)
                elif command == 'LOAD_CC_DIALOGUE':
                    self.parseLoadCCDialogue(line)
                elif command == 'LOAD_CHAR':
                    self.parseLoadChar(line)
                elif command == 'LOAD_CLASSIC_CHAR':
                    self.parseLoadClassicChar(line)
                elif command == 'UNLOAD_CHAR':
                    iList.append(self.parseUnloadChar(line))
                elif command == 'LOAD_SUIT':
                    self.parseLoadSuit(line)
                elif command == 'SET':
                    self.parseSet(line)
                elif command == 'LOCK_LOCALTOON':
                    iList.append(self.parseLockLocalToon(line))
                elif command == 'FREE_LOCALTOON':
                    iList.append(self.parseFreeLocalToon(line))
                elif command == 'REPARENTTO':
                    iList.append(self.parseReparent(line))
                elif command == 'WRTREPARENTTO':
                    iList.append(self.parseWrtReparent(line))
                elif command == 'SHOW':
                    iList.append(self.parseShow(line))
                elif command == 'HIDE':
                    iList.append(self.parseHide(line))
                elif command == 'POS':
                    iList.append(self.parsePos(line))
                elif command == 'HPR':
                    iList.append(self.parseHpr(line))
                elif command == 'SCALE':
                    iList.append(self.parseScale(line))
                elif command == 'POSHPRSCALE':
                    iList.append(self.parsePosHprScale(line))
                elif command == 'COLOR':
                    iList.append(self.parseColor(line))
                elif command == 'COLOR_SCALE':
                    iList.append(self.parseColorScale(line))
                elif command == 'ADD_LAFFMETER':
                    iList.append(self.parseAddLaffMeter(line))
                elif command == 'LAFFMETER':
                    iList.append(self.parseLaffMeter(line))
                elif command == 'OBSCURE_LAFFMETER':
                    iList.append(self.parseObscureLaffMeter(line))
                elif command == 'ARROWS_ON':
                    iList.append(self.parseArrowsOn(line))
                elif command == 'ARROWS_OFF':
                    iList.append(self.parseArrowsOff(line))
                elif command == 'START_THROB':
                    iList.append(self.parseStartThrob(line))
                elif command == 'STOP_THROB':
                    iList.append(self.parseStopThrob(line))
                elif command == 'SHOW_FRIENDS_LIST':
                    iList.append(self.parseShowFriendsList(line))
                elif command == 'HIDE_FRIENDS_LIST':
                    iList.append(self.parseHideFriendsList(line))
                elif command == 'SHOW_BOOK':
                    iList.append(self.parseShowBook(line))
                elif command == 'HIDE_BOOK':
                    iList.append(self.parseHideBook(line))
                elif command == 'ENABLE_CLOSE_BOOK':
                    iList.append(self.parseEnableCloseBook(line))
                elif command == 'OBSCURE_BOOK':
                    iList.append(self.parseObscureBook(line))
                elif command == 'OBSCURE_CHAT':
                    iList.append(self.parseObscureChat(line))
                elif command == 'ADD_INVENTORY':
                    iList.append(self.parseAddInventory(line))
                elif command == 'SET_INVENTORY':
                    iList.append(self.parseSetInventory(line))
                elif command == 'SET_INVENTORY_YPOS':
                    iList.append(self.parseSetInventoryYPos(line))
                elif command == 'SET_INVENTORY_DETAIL':
                    iList.append(self.parseSetInventoryDetail(line))
                elif command == 'PLAY_SFX':
                    iList.append(self.parsePlaySfx(line))
                elif command == 'STOP_SFX':
                    iList.append(self.parseStopSfx(line))
                elif command == 'PLAY_ANIM':
                    iList.append(self.parsePlayAnim(line))
                elif command == 'LOOP_ANIM':
                    iList.append(self.parseLoopAnim(line))
                elif command == 'LERP_POS':
                    iList.append(self.parseLerpPos(line))
                elif command == 'LERP_HPR':
                    iList.append(self.parseLerpHpr(line))
                elif command == 'LERP_SCALE':
                    iList.append(self.parseLerpScale(line))
                elif command == 'LERP_POSHPRSCALE':
                    iList.append(self.parseLerpPosHprScale(line))
                elif command == 'LERP_COLOR':
                    iList.append(self.parseLerpColor(line))
                elif command == 'LERP_COLOR_SCALE':
                    iList.append(self.parseLerpColorScale(line))
                elif command == 'DEPTH_WRITE_ON':
                    iList.append(self.parseDepthWriteOn(line))
                elif command == 'DEPTH_WRITE_OFF':
                    iList.append(self.parseDepthWriteOff(line))
                elif command == 'DEPTH_TEST_ON':
                    iList.append(self.parseDepthTestOn(line))
                elif command == 'DEPTH_TEST_OFF':
                    iList.append(self.parseDepthTestOff(line))
                elif command == 'SET_BIN':
                    iList.append(self.parseSetBin(line))
                elif command == 'CLEAR_BIN':
                    iList.append(self.parseClearBin(line))
                elif command == 'TOON_HEAD':
                    iList.append(self.parseToonHead(line))
                elif command == 'SEND_EVENT':
                    iList.append(self.parseSendEvent(line))
                elif command == 'FUNCTION':
                    iList.append(self.parseFunction(line))
                elif command == 'BLACK_CAT_LISTEN':
                    iList.append(self.parseBlackCatListen(line))
                elif command == 'SHOW_THROW_SQUIRT_PREVIEW':
                    if uponTimeout:
                        self.notify.error(
                            "SHOW_THROW_SQUIRT_PREVIEW not allowed in an UPON_TIMEOUT")
                    # Set the next current event for the next chapter
                    nextEvent = "doneThrowSquirtPreview"
                    iList.append(Func(self.acceptOnce,
                                      nextEvent,
                                      self.playNextChapter,
                                      [nextEvent]))
                    iList.append(self.parseThrowSquirtPreview(line))
                    self.closePreviousChapter(iList)
                    chapterList = []
                    # Set the next current event for the next chapter
                    self.currentEvent = nextEvent                
                elif command == 'WAIT_EVENT':
                    if uponTimeout:
                        self.notify.error("WAIT_EVENT not allowed in an UPON_TIMEOUT")
                    nextEvent = self.parseWaitEvent(line)
                    def proceed(self=self, nextEvent=nextEvent):
                        self.playNextChapter(nextEvent)
                    def handleEvent(*args):
                        # absorb any event arguments
                        # If we were to simply call proceed() here, it
                        # would evaluate to the latest definition of
                        # proceed, which would mean that every WAIT_EVENT
                        # would react as if it were the last WAIT_EVENT. We
                        # bind a current version of proceed by passing it
                        # as an extraArg to Func (and subsequently to
                        # DirectObject.acceptOnce, then Messenger.accept),
                        # then pull the proceed instance off of the start
                        # of the variable-length argument list (the
                        # position of proceed in the argument list is
                        # dependent on the implementation of
                        # Messenger.send).
                        proceed = args[0]
                        proceed()
                    iList.append(Func(self.acceptOnce,
                                      nextEvent,
                                      handleEvent,
                                      [proceed]))
                    self.closePreviousChapter(iList)
                    # Set the next current event for the next chapter
                    chapterList = []
                    self.currentEvent = nextEvent
                elif command == 'SET_MUSIC_VOLUME':
                    iList.append(self.parseSetMusicVolume(line))
                else:
                    notify.warning("Unknown command token: %s for scriptId: %s on line: %s" %
                                   (command, self.scriptId, lineNum))

        self.closePreviousChapter(chapterList)
        # Create the track for timeout
        if timeoutList:
            self.timeoutTrack = Sequence(*timeoutList)
        # Start playing at the first chapter
        self.playNextChapter('start')

    def closePreviousChapter(self, iList):
        trackList = self.chapterDict.setdefault(self.currentEvent, [])
        trackList.append(Sequence(*iList))

    def parseLoad(self, line):
        if len(line) == 3:
            token, varName, modelPath = line
            node = loader.loadModel(modelPath)
        elif len(line) == 4:
            # Load the model, then grab a subnode
            token, varName, modelPath, subNodeName = line
            node = loader.loadModel(modelPath).find("**/" + subNodeName)
        else:
            notify.error("invalid parseLoad command")
        self.setVar(varName, node)
        return

    def parseLoadSfx(self, line):
        token, varName, fileName = line
        sfx = base.loadSfx(fileName)
        self.setVar(varName, sfx)
        return

    def parseLoadDialogue(self, line):
        """ Like loadSfx except dialogue is conditional on language """
        token, varName, fileName = line
        if varName == 'tomDialogue_01':
            notify.debug("VarName tomDialogue getting added. Tutorial Ack: %d" %base.localAvatar.tutorialAck)
        if base.config.GetString("language", "english") == "japanese":
            dialogue = base.loadSfx(fileName)
        else:
            dialogue = None
        self.setVar(varName, dialogue)
        return

    def parseLoadCCDialogue(self, line):
        """ Like loadSfx except dialogue is conditional on language """
        token, varName, filenameTemplate = line
        if self.toon.getStyle().gender == 'm':
            classicChar = 'mickey'
        else:
            classicChar = 'minnie'
        filename = filenameTemplate % classicChar
        if base.config.GetString("language", "english") == "japanese":
            dialogue = base.loadSfx(filename)
        else:
            dialogue = None
        self.setVar(varName, dialogue)
        return

    def parseLoadChar(self, line):
        token, name, charType = line
        char = Char.Char()
        dna = CharDNA.CharDNA()
        dna.newChar(charType)
        char.setDNA(dna)
        # Mickey needs an ear task running
        if (charType == 'mk' or charType == 'mn'):
            char.startEarTask()
        char.nametag.manage(base.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)

    def parseLoadClassicChar(self, line):
        token, name  = line
        char = Char.Char()
        dna = CharDNA.CharDNA()
        if self.toon.getStyle().gender == 'm':
            charType = "mk"
        else:
            charType = "mn"
        dna.newChar(charType)
        char.setDNA(dna)
        # Mickey and Minnie need an ear task running
        char.startEarTask()
        char.nametag.manage(base.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)
        self.chars.append(char)

    def parseUnloadChar(self, line):
        token, name = line
        char = self.getVar(name)
        track = Sequence()
        track.append(Func(self.__unloadChar, char))
        track.append(Func(self.delVar, name))
        return track

    def parseLoadSuit(self, line):
        token, name, suitType = line
        suit = Suit.Suit()
        dna = SuitDNA.SuitDNA()
        dna.newSuit(suitType)
        suit.setDNA(dna)
        self.setVar(name, suit)

    def parseSet(self, line):
        token, varName, value = line
        self.setVar(varName, value)
        return

    def parseCall(self, line):
        token, scriptId = line
        nmp = NPCMoviePlayer(scriptId, self.toon, self.npc)
        return Func(nmp.play)

    def parseLockLocalToon(self, line):
        return Sequence(
            Func(self.toon.detachCamera),
            Func(self.toon.collisionsOff),
            Func(self.toon.disableAvatarControls),
            Func(self.toon.stopTrackAnimToSpeed),
            Func(self.toon.stopUpdateSmartCamera),
            )

    def parseFreeLocalToon(self, line):
        return Sequence(
            Func(self.toon.attachCamera),
            Func(self.toon.startTrackAnimToSpeed),
            Func(self.toon.collisionsOn),
            Func(self.toon.enableAvatarControls),
            Func(self.toon.startUpdateSmartCamera),
            )

    def parseDebug(self, line):
        token, str = line
        return Func(notify.debug, str)

    def parseReparent(self, line):
        if len(line) == 3:
            token, childNodeName, parentNodeName = line
            subNodeName = None
        elif len(line) == 4:
            token, childNodeName, parentNodeName, subNodeName = line
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return ParentInterval(childNode, parentNode)

    def parseWrtReparent(self, line):
        if len(line) == 3:
            token, childNodeName, parentNodeName = line
            subNodeName = None
        elif len(line) == 4:
            token, childNodeName, parentNodeName, subNodeName = line
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return WrtParentInterval(childNode, parentNode)

    def parseShow(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Func(node.show)

    def parseHide(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Func(node.hide)

    def parsePos(self, line):
        token, nodeName, x, y, z = line
        node = self.getVar(nodeName)
        return Func(node.setPos, x,y,z)

    def parseHpr(self, line):
        token, nodeName, h, p, r = line
        node = self.getVar(nodeName)
        return Func(node.setHpr, h,p,r)

    def parseScale(self, line):
        token, nodeName, x, y, z = line
        node = self.getVar(nodeName)
        return Func(node.setScale, x,y,z)

    def parsePosHprScale(self, line):
        token, nodeName, x, y, z, h, p, r, sx, sy, sz = line
        node = self.getVar(nodeName)
        return Func(node.setPosHprScale, x,y,z,h,p,r,sx,sy,sz)

    def parseColor(self, line):
        token, nodeName, r, g, b, a = line
        node = self.getVar(nodeName)
        return Func(node.setColor, r,g,b,a)

    def parseColorScale(self, line):
        token, nodeName, r,g,b,a = line
        node = self.getVar(nodeName)
        return Func(node.setColorScale, r,g,b,a)

    def parseWait(self, line):
        token, waitTime = line
        return Wait(waitTime)

    def parseChat(self, line):
        assert(len(line) in [3,4,5])
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval("TTLocalizer." + line[2])
        chatFlags = CFSpeech | CFTimeout
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        if extraChatFlags:
            chatFlags |= extraChatFlags
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        return Func(avatar.setChatAbsolute, chatString, chatFlags, dialogue)

    def parseClearChat(self, line):
        assert(len(line) in [2])
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatFlags = CFSpeech | CFTimeout
        return Func(avatar.setChatAbsolute, "", chatFlags)

    def parseExtraChatArgs(self, args):
        quitButton = 0
        extraChatFlags = None
        dialogueList = []
        for arg in args:
            if type(arg) == type(0):
                quitButton = arg
            elif type(arg) == type(''):
                if (len(arg) > 2) and (arg[:2] == 'CF'):
                    extraChatFlags = eval(arg)
                else:
                    dialogueList.append(self.getVar(arg))
            else:
                notify.error("invalid argument type")
        return quitButton, extraChatFlags, dialogueList

    def parseChatConfirm(self, line):
        lineLength = len(line)
        assert(len(line) in [3,4,5,6])
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval("TTLocalizer." + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setPageChat, toonId, 0, chatString, quitButton, extraChatFlags, dialogueList)

    def parseLocalChatConfirm(self, line):
        lineLength = len(line)
        assert(lineLength in [3,4,5,6])
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval("TTLocalizer." + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseLocalChatPersist(self, line):
        lineLength = len(line)
        assert(lineLength in [3,4,5,6])
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval("TTLocalizer." + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        # NOTE: override chat flags to disable timeout
        return Func(avatar.setChatAbsolute, chatString, CFSpeech, dialogue)

    def parseLocalChatToConfirm(self, line):
        lineLength = len(line)
        assert(lineLength in [4,5,6,7])
        avatarKey = line[1]
        avatar = self.getVar(avatarKey)
        toAvatarKey = line[2]
        toAvatar = self.getVar(toAvatarKey)
        # This is ugly...
        localizerAvatarName = toAvatar.getName().capitalize()
        toAvatarName = eval("TTLocalizer." + localizerAvatarName)
        chatString = eval("TTLocalizer." + line[3])
        chatString = chatString.replace('%s', toAvatarName)
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[4:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseCCChatConfirm(self, line):
        lineLength = len(line)
        assert(lineLength in [3,4,5,6])
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        if self.toon.getStyle().gender == 'm':
            chatString = eval("TTLocalizer." + (line[2] % 'Mickey'))
        else:
            chatString = eval("TTLocalizer." + (line[2] % 'Minnie'))
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseCCChatToConfirm(self, line):
        lineLength = len(line)
        assert(lineLength in [4,5,6,7])
        avatarKey = line[1]
        avatar = self.getVar(avatarKey)
        toAvatarKey = line[2]
        toAvatar = self.getVar(toAvatarKey)
        # This is ugly...
        localizerAvatarName = toAvatar.getName().capitalize()
        toAvatarName = eval("TTLocalizer." + localizerAvatarName)
        if self.toon.getStyle().gender == 'm':
            chatString = eval("TTLocalizer." + (line[3] % 'Mickey'))
        else:
            chatString = eval("TTLocalizer." + (line[3] % 'Minnie'))
        chatString = chatString.replace('%s', toAvatarName)
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[4:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parsePlaySfx(self, line):
        if len(line) == 2:
            token, sfxName = line
            looping = 0
        elif len(line) == 3:
            token, sfxName, looping = line
        else:
            notify.error("invalid number of arguments")            
        sfx = self.getVar(sfxName)
        return Func(base.playSfx, sfx, looping)

    def parseStopSfx(self, line):
        token, sfxName = line
        sfx = self.getVar(sfxName)
        return Func(sfx.stop)

    def parsePlayAnim(self, line):
        if len(line) == 3:
            token, actorName, animName = line
            playRate = 1.0
        elif len(line) == 4:
            token, actorName, animName, playRate = line
        else:
            notify.error("invalid number of arguments")
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.play, animName))

    def parseLoopAnim(self, line):
        if len(line) == 3:
            token, actorName, animName = line
            playRate = 1.0
        elif len(line) == 4:
            token, actorName, animName, playRate = line
        else:
            notify.error("invalid number of arguments")
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.loop, animName))

    def parseLerpPos(self, line):
        token, nodeName, x, y, z, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpPosInterval(node, t, Point3(x,y,z),
                            blendType="easeInOut"),
            duration = 0.0)

    def parseLerpHpr(self, line):
        token, nodeName, h, p, r, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpHprInterval(node, t, VBase3(h,p,r),
                            blendType="easeInOut"),
            duration = 0.0)

    def parseLerpScale(self, line):
        token, nodeName, x, y, z, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpScaleInterval(node, t, VBase3(x,y,z),
                              blendType="easeInOut"),
            duration = 0.0)

    def parseLerpPosHprScale(self, line):
        token, nodeName, x, y, z, h, p, r, sx, sy, sz, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpPosHprScaleInterval(node, t,
                                    VBase3(x,y,z),
                                    VBase3(h,p,r),
                                    VBase3(sx,sy,sz),
                                    blendType="easeInOut"),
            duration = 0.0)

    def parseLerpColor(self, line):
        token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpColorInterval(node, t, VBase4(er,eg,eb,ea),
                              startColorScale = VBase4(sr,sg,sb,sa),
                              blendType="easeInOut"),
            duration = 0.0)

    def parseLerpColorScale(self, line):
        token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t = line
        node = self.getVar(nodeName)
        return Sequence(
            LerpColorScaleInterval(node, t, VBase4(er,eg,eb,ea),
                                   startColorScale = VBase4(sr,sg,sb,sa),
                                   blendType="easeInOut"),
            duration = 0.0)

    def parseDepthWriteOn(self, line):
        token, nodeName, depthWrite = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.setDepthWrite, depthWrite),
            )

    def parseDepthWriteOff(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.clearDepthWrite),
            )

    def parseDepthTestOn(self, line):
        token, nodeName, depthTest = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.setDepthTest, depthTest),
            )

    def parseDepthTestOff(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.clearDepthTest),
            )

    def parseSetBin(self, line):
        if len(line) == 3:
            token, nodeName, binName = line
            sortOrder = 0
        else:
            token, nodeName, binName, sortOrder = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.setBin, binName, sortOrder)
            )

    def parseClearBin(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(
            Func(node.clearBin)
            )

    def parseWaitEvent(self, line):
        token, eventName = line
        return eventName

    def parseSendEvent(self, line):
        token, eventName = line
        return Func(messenger.send, eventName)

    def parseFunction(self, line):
        token, objectName, functionName = line
        object = self.getVar(objectName)
        cfunc = compile("object" + "." + functionName, "<string>", "eval")
        return Func(eval(cfunc))
    
    def parseAddLaffMeter(self, line):
        token, maxHpDelta = line
        newMaxHp = maxHpDelta + self.toon.getMaxHp()
        # A full heal also
        newHp = newMaxHp
        laffMeter = self.getVar("laffMeter")
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    def parseLaffMeter(self, line):
        token, newHp, newMaxHp = line
        laffMeter = self.getVar("laffMeter")
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    def parseObscureLaffMeter(self, line):
        token, val = line
        return Func(self.toon.laffMeter.obscure, val)

    def parseAddInventory(self, line):
        token, track, level, number = line
        inventory = self.getVar("inventory")
        countSound = base.loadSfx("phase_3.5/audio/sfx/tick_counter.mp3")
        return Sequence(Func(base.playSfx, countSound),
                        Func(inventory.buttonBoing, track, level),
                        Func(inventory.addItems, track, level, number),
                        Func(inventory.updateGUI, track, level),
                        )
    
    def parseSetInventory(self, line):
        token, track, level, number = line
        inventory = self.getVar("inventory")
        return Sequence(Func(inventory.setItem, track, level, number),
                        Func(inventory.updateGUI, track, level),
                        )

    def parseSetInventoryYPos(self, line):
        token, track, level, yPos = line
        inventory = self.getVar("inventory")
        button = inventory.buttons[track][level].stateNodePath[0]
        text = button.find('**/+TextNode')
        return Sequence(Func(text.setY, yPos))

    def parseSetInventoryDetail(self, line):
        if len(line) == 2:
            token, val = line
        elif len(line) == 4:
            token, val, track, level = line
        else:
            notify.error("invalid line for parseSetInventoryDetail: %s" % (line))
 
        inventory = self.getVar("inventory")
        if val == -1:
            return Func(inventory.noDetail)
        elif val == 0:
            return Func(inventory.hideDetail)
        elif val == 1:
            return Func(inventory.showDetail, track, level)
        else:
            notify.error("invalid inventory detail level: %s" % (val))

    def parseShowFriendsList(self, line):
        from toontown.friends import FriendsListPanel
        return Func(FriendsListPanel.showFriendsListTutorial)

    def parseHideFriendsList(self, line):
        from toontown.friends import FriendsListPanel
        return Func(FriendsListPanel.hideFriendsListTutorial)

    def parseShowBook(self, line):
        return Sequence(Func(self.toon.book.setPage, self.toon.mapPage),
                        Func(self.toon.book.enter),
                        Func(self.toon.book.disableBookCloseButton),
                        )

    def parseEnableCloseBook(self, line):
        return Sequence(Func(self.toon.book.enableBookCloseButton),
                        )

    def parseHideBook(self, line):
        return Func(self.toon.book.exit)

    def parseObscureBook(self, line):
        token, val = line
        return Func(self.toon.book.obscureButton, val)

    def parseObscureChat(self, line):
        token, val0, val1 = line
        return Func(self.toon.chatMgr.obscure, val0, val1)

    def parseArrowsOn(self, line):
        arrows = self.getVar("arrows")
        token, x1, y1, h1, x2, y2, h2 = line        
        return Func(arrows.arrowsOn, x1, y1, h1, x2, y2, h2)

    def parseArrowsOff(self, line):
        arrows = self.getVar("arrows")
        return Func(arrows.arrowsOff)

    def parseStartThrob(self, line):
        # TODO: allow multiple throbs via dict of node->throbIval
        token, nodeName, r, g, b, a, r2, g2, b2, a2, t = line
        node = self.getVar(nodeName)
        startCScale = Point4(r,g,b,a)
        destCScale = Point4(r2,g2,b2,a2)
        self.throbIval = Sequence(
            LerpColorScaleInterval(node, t/2.,
                                   destCScale, startColorScale=startCScale,
                                   blendType='easeInOut'),
            LerpColorScaleInterval(node, t/2.,
                                   startCScale, startColorScale=destCScale,
                                   blendType='easeInOut'),
            )
        return Func(self.throbIval.loop)

    def parseStopThrob(self, line):
        return Func(self.throbIval.finish)

    def parseToonHead(self, line):
        if len(line) == 5:
            token, toonName, x, z, toggle = line
            scale = 1.
        else:
            token, toonName, x, z, toggle, scale = line
        toon = self.getVar(toonName)
        toonId = toon.getDoId()
        toonHeadFrame = self.toonHeads.get(toonId)
        if not toonHeadFrame:
            toonHeadFrame = ToonHeadFrame.ToonHeadFrame(toon)
            toonHeadFrame.tag1Node.setActive(1)
            toonHeadFrame.hide()
            self.toonHeads[toonId] = toonHeadFrame
            # add a variable that the scripts can reference (i.e. npcToonHead)
            self.setVar('%sToonHead' % toonName, toonHeadFrame)
        if toggle:
            return Sequence(Func(toonHeadFrame.setPos, x, 0, z),
                            Func(toonHeadFrame.setScale, scale),
                            Func(toonHeadFrame.show),
                            )
        else:
            return Func(toonHeadFrame.hide)
            
    def parseToonHeadScale(self, line):
        token, toonName, scale = line
        toon = self.getVar(toonName)
        toonId = toon.getDoId()
        toonHeadFrame = self.toonHeads.get(toonId)
        return Func(toonHeadFrame.setScale, scale)

    def parseBlackCatListen(self, line):
        token, enable = line
        if enable:
            # listen for Toontastic! and throw an event if we get it
            def phraseSaid(phraseId):
                toontastic = 315
                if phraseId == toontastic:
                    messenger.send(DistributedBlackCatMgr.DistributedBlackCatMgr.ActivateEvent)
            def enableBlackCatListen():
                self.acceptOnce(SpeedChatGlobals.SCStaticTextMsgEvent,
                                phraseSaid)
            return Func(enableBlackCatListen)
        else:
            def disableBlackCatListen():
                self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
            return Func(disableBlackCatListen)

    def parseThrowSquirtPreview(self, line):
        # make this a list so that we can modify it
        oldTrackAccess = [None]
        def grabCurTrackAccess(oldTrackAccess=oldTrackAccess):
            oldTrackAccess[0] = copy.deepcopy(
                base.localAvatar.getTrackAccess())
        def restoreTrackAccess(oldTrackAccess=oldTrackAccess):
            base.localAvatar.setTrackAccess(oldTrackAccess[0])

        minGagLevel = ToontownBattleGlobals.MIN_LEVEL_INDEX+1
        maxGagLevel = ToontownBattleGlobals.MAX_LEVEL_INDEX+1
        curGagLevel = minGagLevel
        def updateGagLevel(t, curGagLevel=curGagLevel):
            newGagLevel = int(round(t))
            if newGagLevel == curGagLevel:
                return
            curGagLevel = newGagLevel
            base.localAvatar.setTrackAccess(
                [0,0,0,0,curGagLevel,curGagLevel,0])

        return Sequence(
            Func(grabCurTrackAccess),
            LerpFunctionInterval(updateGagLevel, fromData=1, toData=7, duration=.3),
            WaitInterval(3.5),
            LerpFunctionInterval(updateGagLevel, fromData=7, toData=1, duration=.3),
            Func(restoreTrackAccess),
            Func(messenger.send, 'doneThrowSquirtPreview')
            )
            
    def parseSetMusicVolume(self, line):
        if base.config.GetString("language", "english") == "japanese":
            try:
                loader = base.cr.playGame.place.loader
                type = 'music'
                duration = 0
                fromLevel = 1.0
                if len(line) == 2:
                    token, level = line
                elif len(line) == 3:
                    token, level, type = line
                elif len(line) == 4:
                    token, level, type, duration = line
                elif len(line) == 5:
                    token, level, type, duration, fromLevel = line
                # Get a handle to the appropriate music type
                if type == 'battleMusic':
                    music = loader.battleMusic
                elif type == 'activityMusic':
                    music = loader.activityMusic
                else:
                    music = loader.music
                if duration == 0:
                    return Func(music.setVolume, level)
                else:
                    def setVolume(level):
                        music.setVolume(level)
                    return LerpFunctionInterval(setVolume,
                                                fromData = fromLevel,
                                                toData = level,
                                                duration = duration)
            except AttributeError:
                pass
        else:
            return Wait(0.0)

# Look for the script file and read it in.
searchPath = DSearchPath()
if AppRunnerGlobal.appRunner:
    # In the web-publish runtime, it will always be here:
    searchPath.appendDirectory(Filename.expandFrom('$TT_3_ROOT/phase_3/etc'))
else:
    # In other environments, including the dev environment, look here:
    searchPath.appendDirectory(Filename('phase_3/etc'))
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/quest')))
    searchPath.appendDirectory(Filename.fromOsSpecific('toontown/src/quest'))
    searchPath.appendDirectory(Filename('.'))

scriptFile = Filename('QuestScripts.txt')
found = vfs.resolveFilename(scriptFile, searchPath)

if not found:
    notify.error("Could not find QuestScripts.txt file")

readFile(scriptFile)
