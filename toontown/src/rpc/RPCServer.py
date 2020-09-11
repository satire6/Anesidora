import threading,Queue
import SOAPpy
from tlslite.errors import TLSError

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.AsyncRequest import AsyncRequest
from toontown.rpc.RPCRequests import GetToonIdListRequest
from toontown.rpc.RPCRequests import GiveToonBeansRATRequest
from toontown.rpc.RPCRequests import GiveToonBeansCSRequest
from toontown.rpc.RPCRequests import GetToonPicIdRequest
from toontown.rpc.RPCRequests import GetToonDNARequest
from toontown.rpc.RPCRequests import GetToonNameRequest
from toontown.rpc.RPCRequests import TimeoutException

class RPCException(Exception):
    "Exception raised on invalid RPC arguments"
    def __init__(self,*args):
        Exception.__init__(self,*args)


class RPCServerThread(threading.Thread):
    """
    Server thread for RPCServer.
    Runs a simple RPC server forever and communicates to RPCServer through request queues.
    """
    def __init__(self,rpcip,rpcport,keyfile,certfile,allowed_ipdict):
        self.rpcip = rpcip
        self.rpcport = rpcport

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.requestQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()

        SOAPpy.Config.debug = 0
        SOAPpy.Config.dumpFaultInfo = 0


        # --- BEGIN PUBLISHED FUNCTIONS ---


        def getToonList(accountName):
            """
            Retrieve a list of toons owned by the given account.

            accountName is the account name string as stored on the OTP server.

            Returns a list of (DOID,name) tuples.
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(accountName,str):
                raise RPCException, "Argument accountName was not a string."

            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GetToonIdListRequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       accountName))
            idList = self.resultQueue.get()

            if isinstance(idList,TimeoutException):
                raise RPCException, "Request timed out."

            resultList = []
            for doid in idList:
                if doid > 0:
                    toonname = self.getToonName(doid)
                    resultList.append((doid,toonname))

            return resultList


        def getToonSlots(accountName):
            """
            Identical to getToonList, but also returns empty toon slots.
            
            Retrieve a list of toons owned by the given account.

            accountName is the account name string as stored on the OTP server.

            Returns a list of (DOID,name) tuples.
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(accountName,str):
                raise RPCException, "Argument accountName was not a string."

            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GetToonIdListRequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       accountName))
            idList = self.resultQueue.get()

            if isinstance(idList,TimeoutException):
                raise RPCException, "Request timed out."

            resultList = []
            id = 0
            for doid in idList:
                if doid > 0:
                    toonname = self.getToonName(doid)
                    resultList.append((doid,toonname))
                else:
                    resultList.append((id,"%s"%id))
                id += 1

            return resultList


        def giveToonBeansRAT(toonID,beanAmount):
            """
            Only for Recruit-a-Toon program.
            
            Give jellybeans to the toon specified.

            toonID is the DOID of the recipient toon.

            beanAmount is the number of beans to give (0 < beanAmount <= 100).

            Returns None on success, faults on failure.
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(toonID,int):
                raise RPCException, "Argument toonID was not an int."
            if not isinstance(beanAmount,int):
                raise RPCException, "Argument beanAmount was not an int."
            if toonID < 1:
                raise RPCException, "Argument toonID was non-positive."
            if beanAmount > 100:
                raise RPCException, "Attempted to give a toon more than 100 jellybeans at once"
            if beanAmount < 1:
                raise RPCException, "Attempted to give a toon a non-positive jellybean amount"


            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GiveToonBeansRATRequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       toonID, \
                                                       beanAmount))
            result = self.resultQueue.get()            
            return


        def giveToonBeansCS(toonID,beanAmount):
            """
            Only for Customer Service requests.
            
            Give jellybeans to the toon specified.

            toonID is the DOID of the recipient toon.

            beanAmount is the number of beans to give (0 < beanAmount <= 100).

            Returns None on success, faults on failure.
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(toonID,int):
                raise RPCException, "Argument toonID was not an int."
            if not isinstance(beanAmount,int):
                raise RPCException, "Argument beanAmount was not an int."
            if toonID < 1:
                raise RPCException, "Argument toonID was non-positive."
            if beanAmount > 100:
                raise RPCException, "Attempted to give a toon more than 100 jellybeans at once"
            if beanAmount < 1:
                raise RPCException, "Attempted to give a toon a non-positive jellybean amount"

            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GiveToonBeansCSRequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       toonID, \
                                                       beanAmount))
            result = self.resultQueue.get()            
            return


        def getToonPicId(toonID):
            """
            Retrieve the picture ID for a given toon.

            toonID is the toon's DOID
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(toonID,int):
                raise RPCException, "Argument toonID was not an int."
            if toonID < 1:
                raise RPCException, "Argument toonID was non-positive."

            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GetToonPicIdRequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       toonID))
            picid = self.resultQueue.get()

            if isinstance(picid,TimeoutException):
                raise RPCException, "Request timed out."

            return picid


        def getToonDNA(toonID):
            """
            Retrieve the DNA for a given toon.

            toonID is the toon's DOID
            """
            assert self.requestQueue.empty()
            assert self.resultQueue.empty()
            if not isinstance(toonID,int):
                raise RPCException, "Argument toonID was not an int."
            if toonID < 1:
                raise RPCException, "Argument toonID was non-positive."

            c = SOAPpy.GetSOAPContext()

            self.requestQueue.put(GetToonDNARequest(self.resultQueue, \
                                                       c.connection.getpeername()[0], \
                                                       toonID))
            dna = self.resultQueue.get()

            if isinstance(dna,TimeoutException):
                raise RPCException, "Request timed out."

            return dna
            

        # --- END PUBLISHED FUNCTIONS ---


        self.SOAPServer = SOAPpy.SOAPServer(addr=(self.rpcip,self.rpcport),\
                                            namespace="ToontownRPC",\
                                            key_file=keyfile,\
                                            cert_file=certfile,\
                                            allowed_ipdict=allowed_ipdict)

        self.SOAPServer.registerFunction(getToonList)
        self.SOAPServer.registerFunction(getToonSlots)
        self.SOAPServer.registerFunction(giveToonBeansRAT)
        self.SOAPServer.registerFunction(giveToonBeansCS)
        self.SOAPServer.registerFunction(getToonPicId)
        self.SOAPServer.registerFunction(getToonDNA)
        
        self.start()

    def getToonName(self,toonID):
        """
        Internal request.  Not published for RPC.
        Returns the name of the toon with given DOID.
        """
        assert self.requestQueue.empty()
        assert self.resultQueue.empty()
        self.requestQueue.put(GetToonNameRequest(self.resultQueue, \
                                                 "internal", \
                                                 toonID))
        result = self.resultQueue.get()

        if toonID < 1:
            raise RPCException, "Argument toonID was non-positive."
        if isinstance(result,TimeoutException):
            raise RPCException, "Request timed out."
        return unicode(result.decode("utf-8"))


    def run(self):
        while 1:
            try:
                self.SOAPServer.serve_forever()
            except TLSError,e:
                self.SOAPServer.logRequestQueue.put(("unknown","TLSError",e))
            except Exception,e:
                self.SOAPServer.logRequestQueue.put(("unknown","Exception",e))
    

class RPCServer(object):
    """
    Embedded RPC server for use with uberdog.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('RPCServer')
    
    def __init__(self,rpcip,rpcport,keyfile="",certfile="",allowed_ipdict={}):
        """
        rpcip is the IP to listen on.  If empty, do not listen on a specific IP.

        rpcport is the port to listen on.

        keyfile is the server's private key file for use with SSL

        certfile is the server's certificate file for use with SSL

        allowed_ipdict is a dictionary containing IP:True pairs where IP is an address being allowed to connect


        If keyfile or certfile is empty, no encryption is used.

        If allowed_ipdict is empty, any client is allowed to make requests.
        """
        self.air = uber.air
        self.notify.info("Embedded RPC server enabled.")
        self.notify.info("Starting server on %s:%u." % (rpcip,rpcport))
        if keyfile is "" or certfile is "":
            self.notify.warning("No key/cert provided, unable to use SSL.  NO ENCRYPTION ENABLED.")
        else:
            self.notify.info("Initializing SSL using TLSLite.")
            self.notify.info("Keyfile: %s" % keyfile)
            self.notify.info("Certificate file: %s" % certfile)

        if allowed_ipdict == {}:
            self.notify.warning("No allowed IP list provided.  ALLOWING ANYONE TO CONNECT.")
        else:
            self.notify.info("Allowing requests from: %s" % allowed_ipdict.keys())
      
        self.rpcip = rpcip
        self.rpcport = rpcport
        self.serverthread = RPCServerThread(rpcip,rpcport,keyfile,certfile,allowed_ipdict)

    def processLogRequest(self,clientIP,description,info):
        """
        Log an event generated by clientIP, with given description and additional info.
        """
        if description == "Unauthorized IP":
          self.notify.warning("HTTP Unauthorized Address %s" % clientIP)
          self.air.writeServerEvent("UberRPC-SecurityAlert",clientIP,"HTTP Unauthorized Address %s" % clientIP)
        elif description == "TLSError":
            self.notify.warning("Caught TLSError while serving RAT requests:\n%s\nContinuing." % info)
        elif description == "Exception":
            self.notify.warning("Caught exception while serving RAT requests:\n%s\nContinuing." % info)
        else:
            assert(False)
            pass

    def serverLoop(self):
        """
        Process a single client request and a single log request.
        """
        try:
            request = self.serverthread.requestQueue.get_nowait()
            request.submit()
        except Queue.Empty:
            pass

        try:
            clientIP,description,info = self.serverthread.SOAPServer.logRequestQueue.get_nowait()
            self.processLogRequest(clientIP,description,info)
        except Queue.Empty:
            pass




        

