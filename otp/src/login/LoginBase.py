"""LoginBase is the base class for LoginXXAccount classes"""


class LoginBase:
    # When, in seconds from epoch GMT, will the free play expire.
    # -1 == never, 0 == already expired
    freeTimeExpires=-1
    
    def __init__(self, cr):
        self.cr=cr
    
    def sendLoginMsg(self, loginName, password, createFlag):
        pass

    # these result-getters help to keep client code from putting
    # their grubby hands into the internals of TTAccount, which
    # in turn helps reduce problems for code that needs to
    # run under account-old-auth == 0
    def getErrorCode(self):
        return 0
    def needToSetParentPassword(self):
        return 0
    
