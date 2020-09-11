from direct.showbase import ExceptionVarDump
import base64

def _doPrint(s):
    print base64.b64encode(s)

def install():
    # make sure DIRECT print func is installed
    ExceptionVarDump.install()
    # and hook up to it
    ExceptionVarDump.setOutputFunc(_doPrint)
