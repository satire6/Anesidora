import cherrypy
import atexit

class SnapshotWebServer(object):
    def __init__(self,requestQueue):
        config = "C:\\cygwin\\home\\igraham\\player\\otp\\src\\snapshot\\cherrypy.conf"

        self.requestQueue = requestQueue

        atexit.register(self.stopThreads)

        cherrypy._global_conf_alias.update(config)
        cherrypy.tree.mount(self,"",config)
        cherrypy.server.quickstart()
        cherrypy.engine.start(blocking=False)

    def stopThreads(self):
        cherrypy.engine.stop()
        cherrypy.server.stop()

    @cherrypy.expose
    def getSnapshot(self,avatarId):
        """
        Render this avatar's picture and give me the location (URL) of the image.
        Accessed via an HTTP query.
        """
        try:
            avatarId = int(avatarId)
        except:
            return "Error parsing argument avatarId.  Gimme an integer!"
        
        print "getSnapshot %s" % avatarId

        self.requestQueue.put_nowait(avatarId)

        return "%s" % avatarId
