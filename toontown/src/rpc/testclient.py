#!/home/igraham/player/wintools/sdk/python/Python-2.4.1/PCbuild/python

import SOAPpy
import sys

SOAPpy.Config.debug = 0

connectTo = "http://localhost:8080"
acctName = "mrhead"
toondoid = 100000006
numqueries = 1000


server = SOAPpy.SOAPProxy(connectTo,namespace="ToontownRPC")


print "Running %d queries..." % numqueries
sys.stdout.flush()


for i in range(numqueries):
  heyalist = server.getToonList(accountName=acctName)
  #print server.giveToonBeansRAT(toonID=toondoid,beanAmount=10)
  #print server.giveToonBeansCS(toonID=toondoid,beanAmount=10)
  #print server.getToonPicId(toonID=toondoid)


print "DONE"


