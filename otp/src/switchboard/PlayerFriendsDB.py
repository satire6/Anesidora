import MySQLdb
import _mysql_exceptions
import datetime
#from otp.distributed import OtpDoGlobals
#from direct.directnotify.DirectNotifyGlobal import directNotify
import FriendManagerService_services


class PlayerFriendsDB:
    """
    DB wrapper class for player friends!  All SQL and SOAP code for player friends should be in here.
    """
    def __init__(self,log,url):

        self.log = log
        self.url = url

        loc = FriendManagerService_services.FriendManagerServiceLocator()
        self.soapProxy = loc.getFriendManager(url=self.url)

        self.log.info("Using player friends SOAP interface at %s" % url)


    def getFriends(self,playerId):
        friends = self.soapProxy.getFriends(playerId)
        return map(lambda x:[x._friendId,x._secret],friends)

    def addFriendship(self,playerId1,playerId2,secretYesNo=1):
        self.soapProxy.makeFriends(playerId1,playerId2,secretYesNo)

    def removeFriendship(self,playerId1,playerId2):
        self.soapProxy.deleteFriend(playerId1,playerId2)

    def getToken(self,playerId,parentUsername=None,parentPassword=None):
        if parentUsername is None:
            return self.soapProxy.generateToken(playerId)
        else:
            return self.soapProxy.generateTokenParentAuth(playerId,parentUsername,parentPassword,"","","")

    def redeemToken(self,redeemingPlayerId,token,parentUsername=None,parentPassword=None):
        if parentUsername is None:
            return self.soapProxy.redeemToken(redeemingPlayerId,token)
        else:
            return self.soapProxy.redeemTokenParentAuth(playerId,token,parentUsername,parentPassword,"","","")

