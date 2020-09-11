import sys
import time
import socket
import Queue
from toontown.uberdog import PartiesUdConfig

class partiesUdLog:
    def __init__(self,name,clHost=None,clPort=6060):
        self.name = name
        self.clHost = clHost
        self.clPort = clPort

        self.inMemLog = Queue.Queue()

        if clHost:
            # init UDP stuff
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def timeString(self):
        tup = time.localtime()
        return "%d-%02d-%02d %02d:%02d:%02d" % (tup[0],tup[1],tup[2],tup[3],tup[4],tup[5])

    def output(self,level,msg):
        str = "%s %s(%s): %s"%(self.timeString(),self.name,level,msg)
        print str
        self.memLog(str)
        sys.stdout.flush()

    def chatoutput(self,msg):
        str = "%s %s(chat): %s"%(self.timeString(),self.name,msg)
        print str
        self.memLog(str)
        sys.stdout.flush()

    def memLog(self,str):
        self.inMemLog.put(str)
        while self.inMemLog.qsize() > PartiesUdConfig.logMaxLinesInMemory:
            self.inMemLog.get()

    def getMemLog(self):
        res = ""
        for i in xrange(self.inMemLog.qsize()):
            s = self.inMemLog.get()
            res += s + "\n"
            self.inMemLog.put(s)
        return res

    def remoteLog(self,
                  eventName,
                  sourceSys,
                  sourceAcctId,
                  sourceAvId,
                  destSys,
                  destAcctId,
                  destAvId,
                  chatType,
                  filtered,
                  chatText):
        assert self.clHost is not None
        outstr = "%s|%s|%d|%d|%s|%d|%d|%s|%s|%s" % (eventName,sourceSys,sourceAcctId,sourceAvId,
                                                    destSys,destAcctId,destAvId,chatType,filtered,
                                                    chatText)
        self.debug("Remote log entry sent: %s"%outstr)
        self.sock.sendto(outstr,(self.clHost,self.clPort))

    def fatal(self,message):
        if PartiesUdConfig.logFatal:
            self.output("FATAL",message)

    def error(self,message):
        if PartiesUdConfig.logError:
            self.output("ERROR",message)

    def security(self,message):
        if PartiesUdConfig.logSecurity:
            self.output("SECURITY",message)

    def warning(self,message):
        if PartiesUdConfig.logWarning:
            self.output("warning",message)

    def log(self,message):
        if PartiesUdConfig.logLog:
            self.output("log",message)

    def info(self,message):
        if PartiesUdConfig.logInfo:
            self.output("info",message)

    def debug(self,message):
        if PartiesUdConfig.logDebug:
            self.output("debug",message)

    def chat(self,dest,sender,msg):
        if PartiesUdConfig.logChat:
            self.chatoutput("WHISPER %d->%d: %s" % (sender,dest,msg))
        if self.clHost:
            self.remoteLog("Client Chat",self.name,sender,-1,"",dest,-1,"PEER","N",msg)

    def mail(self,dest,sender,msg):
        if PartiesUdConfig.logChat:
            self.chatoutput("MAIL %d->%d: %s" % (sender,dest,msg))
        if self.clHost:
            self.remoteLog("Client Chat",self.name,sender,-1,"",dest,-1,"MAIL","N",msg)
        
    def badChat(self,dest,sender,msg):
        if PartiesUdConfig.logChat:
            self.chatoutput("DIRTYCHAT %d->%d: %s" % (sender,dest,msg))
        if self.clHost:
            self.remoteLog("Client Chat",self.name,sender,-1,"",dest,-1,"PEER","Y",msg)

    def badMail(self,dest,sender,msg):
        if PartiesUdConfig.logChat:
            self.chatoutput("DIRTYMAIL %d->%d: %s" % (sender,dest,msg))
        if self.clHost:
            self.remoteLog("Client Chat",self.name,sender,-1,"",dest,-1,"MAIL","Y",msg)
