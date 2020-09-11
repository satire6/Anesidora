import Pyro.util
import Pyro.core
import Pyro.naming
import sys
import getopt
import cherrypy

import sbConfig
from sbLog import sbLog

from LastSeenDB import LastSeenDB
from sbMaildb import sbMaildb

class sbMonitor(object):
    def __init__(self):
        loc = Pyro.naming.NameServerLocator()
        if sbConfig.nsHost is None:
            self.ns  = loc.getNS()
        else:
            self.ns = loc.getNS(host=sbConfig.nsHost,port=sbConfig.nsPort)

        self.printlog = sbLog("SBMonitor","localhost",12345)

        self.menu = {"Index":"/",
                     "Log":"/log",
                     "Stats":"/stats",
                     "Database":"/db",
                     "Console":"/console"}

        self.nodeNames = set()

        self.rowCount = 0

        self.lastSeenDB = LastSeenDB(log=self.printlog,
                                     host=sbConfig.lastSeenDBhost,
                                     port=sbConfig.lastSeenDBport,
                                     user=sbConfig.lastSeenDBuser,
                                     passwd=sbConfig.lastSeenDBpasswd,
                                     dbname=sbConfig.lastSeenDBdb)

        self.mailDB = sbMaildb(log=self.printlog,
                               host=sbConfig.mailDBhost,
                               port=sbConfig.mailDBport,
                               user=sbConfig.mailDBuser,
                               passwd=sbConfig.mailDBpasswd,
                               db=sbConfig.mailDBdb)

        

    def getRowClassString(self):
        res = ""
        if self.rowCount % 2 == 0:
            res = ""
        else:
            res = " class=\"odd\""
        self.rowCount += 1
        return res

    def header(self,current):
        pageText = '''
<html><head>
<title>Switchboard Monitor</title>
<style>
  body
  {
  margin: 0;
  padding: 0;
  font-size: 90%;
  font-family: Verdana, sans-serif;
  background-color: #fff;
  color: #333;
  }

  p
  {
  margin: 0;
  padding: 10px;
  background-color: #eee;
  }

  h2
  {
  font-size: 140%;
  color: #666;
  background-color: #fff;
  width: 22em;
  margin-left: 150px;
  margin-top: 0px;
  }

  h3
  {
  padding-top: 10px;
  margin-top: 0px;
  margin-left: 20px;
  }

  pre
  {
  margin-left: 20px;
  margin-bottom: 0px;
  padding-bottom: 10px;
  }
  
  a
  {
  text-decoration: none;
  color: #333;
  }
  
  a:hover
  {
  text-decoration: underline;
  }

  #header
  {
  margin: 0;
  padding: 0;
  background-color: #fff;
  }

  #footer
  {
  margin: 0;
  padding: 3px;
  text-align: right;
  background-color: #fff;
  border-top: 1px solid #778;
  font: 10px Verdana, sans-serif;
  }

  #contents
  {
  margin: 0;
  padding: 25;
  background-color: #eee;
  min-height:600px;
  height:auto !important;
  height:600px;
  }

  <!-- Tab menu -->

  #navcontainer
  {
  margin:0;
  padding: 0;
  }

  #navlist
  {
  padding: 3px 0;
  margin-left: 0;
  margin: 0;
  border-bottom: 1px solid #778;
  font: bold 12px Verdana, sans-serif;
  background-color: transparent;
  }

  #navlist li
  {
  list-style: none;
  margin: 0;
  display: inline;
  }

  #navlist li a
  {
  padding: 3px 0.5em;
  margin-left: 3px;
  border: 1px solid #778;
  border-bottom: none;
  background: #DDE;
  text-decoration: none;
  }

  #navlist li a:link { color: #448; }
  #navlist li a:visited { color: #667; }

  #navlist li a:hover
  {
  color: #000;
  background: #AAE;
  border-color: #227;
  }

  #navlist li a#current
  {
  background: #eee;
  border-bottom: 1px solid #eee;
  }

  #navlist li.first
  {
  margin-left: 150px;
  }

  <!-- Table formatting -->

  table
  {
  border-spacing:1px;
  background:#E7E7E7;
  color:#333;
  }
  
  caption
  {
  border: #666666;
  border-bottom: 2px solid #666666;
  margin-left: 2px;
  margin-right: 2px;
  padding: 10px;
  background: #cfcfdf;
  font: 15px 'Verdana', Arial, Helvetica, sans-serif;
  font-weight: bold;
  }
  
  td, th
  {
  font:13px 'Courier New',monospace;
  padding: 4px;
  }
  
  thead th
  {
  text-align: center;
  background: #dde;
  color: #666666;
  border: 1px solid #ffffff;
  text-transform: uppercase;
  }
  
  tbody th
  {
  font-weight: bold;
  }

  tbody tr
  {
  background: #efeffc;
  text-align: left;
  }
  
  tbody tr.odd
  {
  background: #ffffff;
  border-top: 1px solid #ffffff;
  }
  
  tbody th a:hover
  {
  color: #009900;
  }
  
  tbody tr td
  {
  text-align: left
  height: 30px;
  background: #ffffff;
  border: 1px solid #ffffff;
  color: #333;
  }
  
  tbody tr.odd td
  {
  background: #efeffc;
  border-top: 1px solid #ffffff;
  }
  
  tbody tr.dead td
  {
  background:#ff0000;
  border-top: 1px solid #ffffff;
  }

  table td a:link, table td a:visited
  {
  display: block;
  padding: 0px;
  margin: 0px;
  width: 100%;
  text-decoration: none;
  color: #333;
  }
  
  html>body #navcontainer li a { width: auto; }
  
  table td a:hover
  {
  color: #000000;
  background: #aae;
  }
  
  tfoot th, tfoot td
  {
  background: #dfdfdf;
  padding: 3px;
  text-align: center;
  font: 14px 'Verdana', Arial, Helvetica, sans-serif;
  font-weight: bold;
  border-bottom: 1px solid #cccccc;
  border-top: 1px solid #DFDFDF;
  }  
</style>
</head>

<body>
<div id="header">
<h2>Switchboard Monitor</h2>
<div id="navcontainer">
<ul id="navlist">
'''

        linkNum = 0
        for link in self.menu.keys():
            if linkNum == 0:
                if link == current:
                    pageText += "<li id=\"active\" class=\"first\"><a href=\"%s\" id=\"current\">%s</a></li>\n" % \
                                (self.menu[link],link)
                else:
                    pageText += "<li class=\"first\"><a href=\"%s\">%s</a></li>\n" % \
                                (self.menu[link],link)
            else:
                if link == current:
                    pageText += "<li id=\"active\"><a href=\"%s\" id=\"current\">%s</a></li>\n" % \
                                (self.menu[link],link)
                else:
                    pageText += "<li><a href=\"%s\">%s</a></li>\n" % \
                                (self.menu[link],link)
            linkNum += 1
        

        pageText += '''</ul>
</div>
</div>
<div id="contents">
<center>
'''

        return pageText

    def footer(self):
        return '''</center>
</div>
<div id="footer">
Contact: M. Ian Graham - ian.graham@dig.com - 818-623-3219
</div>
</body>
</html>
'''

    def checkNameServer(self):
        try:
            loc = Pyro.naming.NameServerLocator()
            if sbConfig.nsHost is None:
                ns = loc.getNS()
            else:
                ns = loc.getNS(host=sbConfig.nsHost,port=sbConfig.nsPort)
            ns.ping()
            return True
        except:
            return False
    
    def serverStatusString(self,name,prefix):
        uri = self.ns.resolve(prefix + name)
        healthy = False
        try:
            proxy = Pyro.core.getProxyForURI(uri)
            proxy._setTimeout(0.5)
            healthy = proxy.healthCheck()
        except:
            healthy = False

        if healthy:
            pageText = "<tr%s><td>:)</td>" % self.getRowClassString()
        else:
            pageText = "<tr class=\"dead\"><td bgcolor=ff0000>:(</td>"

        pageText += "<td><a href=\"log?target=%s%s\">%s%s</a></td><td>%s</td><td>%d</td>" % (prefix,name,prefix,name,uri.address,uri.port)

        if healthy:
            pageText += "<td></td></tr>\n"
        else:
            pageText += "<td>Not responding</td></tr>\n"

        return pageText

    def orphanWedgeString(self,name,prefix):
        uri = self.ns.resolve(prefix + name)
        return "<tr%s><td>?</td><td>%s%s</td><td>%s</td><td>%d</td><td>Orphaned</td></tr>\n" % \
               (self.getRowClassString(),prefix,name,uri.address,uri.port)

    def nodeTable(self):
        self.rowCount = 0
        pageText = "<P>"
        pageText += "<table>\n<caption>nodes</caption>\n<thead>\n"
        pageText += "<tr><th scope=col>?</th><th scope=col>Name</th><th scope=col>Host</th><th scope=col>Port</th><th scope=col>Notes</th></tr>\n"
        pageText += "</thead>\n\n"
        pageText += "<tbody>\n"
        nodeList = self.ns.list(":sb.node")
        for node in nodeList:
            assert node[1] == 1,"whoa, someone put a subgroup in :sb.node!"
            self.nodeNames.add(node[0])
            pageText += self.serverStatusString(node[0],":sb.node.")

        pageText += "</tbody></table></P>\n"

        return pageText

    def wedgeTable(self):
        self.rowCount = 0
        pageText = "<P>"
        #pageText += "<font size=-1 face=monospace>\n"
        pageText += "<table>\n<caption>wedges</caption>\n<thead>\n"
        pageText += "<tr><th scope=col>?</th><th scope=col>Name</th><th scope=col>Host</th><th scope=col>Port</th><th scope=col>Notes</th></tr>\n"
        pageText += "</thead>\n<tbody>\n"
        wedgeList = self.ns.list(":sb.wedge")
        for wedge in wedgeList:
            assert wedge[1] == 1,"whoa, someone put a subgroup in :sb.wedge!"
            if wedge[0] in self.nodeNames:
                pageText += self.serverStatusString(wedge[0],":sb.wedge.")
            else:
                pageText+= self.orphanWedgeString(wedge[0],":sb.wedge.")

        pageText += "</tbody></table></font></P>\n"

        return pageText

    def dbTable(self,dbName,tables):
        self.rowCount = 0
        pageText = "<P>" 
        pageText += "<font size=-1 face=monospace>\n"
        pageText += "<table>\n<caption>%s</caption>\n<thead>\n" % dbName
        pageText += "<tr><th scope=col>Table Name</th><th scope=col>Engine</th><th scope=col>Rows</th><th scope=col>Data Length</th><th scope=col>Avg Row Length</th></tr>\n"
        pageText += "</thead>\n<tbody>\n"
        for table in tables:
            pageText += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (table['Name'],table['Engine'],table['Rows'],table['Data_length'],table['Avg_row_length'])

        pageText += "</tbody></table></font></P>\n"

        return pageText          
        
    def index(self):
        pageText = self.header("Index")

        if self.checkNameServer():
            pageText += self.nodeTable()
            pageText += self.wedgeTable()
        else:
            pageText += "<font size=+1 color=ff0000>Name server not found!</font>\n"

        pageText += self.footer()

        return pageText
        
    def db(self):
        pageText = self.header("Database")

        tableStatus = self.lastSeenDB.getTableStatus()

        pageText += self.dbTable("switchboard",tableStatus)

        pageText += self.footer()

        return pageText

    def log(self,target=None):
        pageText = self.header("Log")
        
        pageText += "<div align=left><h3>%s</h3>\n<pre width=130>\n" % target
        
        if 1:
            uri = self.ns.resolve(target)
            proxy = Pyro.core.getProxyForURI(uri)
            proxy._setTimeout(0.5)
            pageText += proxy.getLogTail()
        #except:
        #    pageText += "Error retrieving log!\n"

        pageText += "\n</pre></div>\n"

        pageText += self.footer()

        return pageText

    def stats(self,target=None):
        pageText = self.header("Stats")

        if target is None:
            nodeList = self.ns.list(":sb.node")
            wedgeList = self.ns.list(":sb.wedge")
            for node in nodeList:
                self.printlog.debug("Getting stats for sb.node.%s" % node[0])
                uri = self.ns.resolve(":sb.node." + node[0])
                proxy = Pyro.core.getProxyForURI(uri)
                proxy._setTimeout(1)
                pageText += "<div align=left><h3>sb.node.%s</h3>\n<pre>\n" % node[0]
                try:
                    stats = proxy.statCheck()
                    pageText += str(stats)
                except:
                    pageText += "<font color=ff0000>Unreachable!</font>"
                pageText += "\n</pre></div>\n"
            for wedge in wedgeList:
                if wedge[0] in self.nodeNames:
                    self.printlog.debug("Getting stats for sb.wedge.%s" % wedge[0])
                    uri = self.ns.resolve(":sb.wedge." + wedge[0])
                    proxy = Pyro.core.getProxyForURI(uri)
                    proxy._setTimeout(1)
                    pageText += "<div align=left><h3>sb.wedge.%s</h3>\n<pre>\n" % wedge[0]
                    try:
                        self.printlog.debug("Enter statCheck")
                        stats = proxy.statCheck()
                        pageText += str(stats)
                    except:
                        pageText += "<font color=ff0000>Unreachable!</font>"
                    pageText += "\n</pre></div>\n"
                    self.printlog.debug("done statCheck")
        else:
            pageText += "<div align=left><h3>%s</h3>\n<pre>\n" % target

            uri = self.ns.resolve(target)            
            proxy = Pyro.core.getProxyForURI(uri)
            proxy._setTimeout(1)
            pageText += str(proxy.statCheck())

            pageText += "\n</pre></div>\n"             

        pageText += self.footer()

        return pageText 


    index.exposed = True
    stats.exposed = True
    log.exposed = True
    db.exposed = True
    #console.exposed = True

mon = sbMonitor()

conf = {'server.socket_port' : sbConfig.webMonitorPort,
        'engine.autoreload_on' : False}  


cherrypy.config.update(conf)

cherrypy.tree.mount(root=mon)
cherrypy.server.quickstart()
cherrypy.engine.start()
