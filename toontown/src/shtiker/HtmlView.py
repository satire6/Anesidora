import array, sys

# import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import Texture
from pandac.PandaModules import CardMaker
from pandac.PandaModules import NodePath
from pandac.PandaModules import Point3,Vec3,Vec4,VBase4D, Point2
from pandac.PandaModules import PNMImage
from pandac.PandaModules import TextureStage
from pandac.PandaModules import Texture
from pandac.PandaModules import WindowProperties
from direct.interval.IntervalGlobal import *

#from toontown.shtiker.pawesomium import *
from pandac.PandaModules import AwWebView
from pandac.PandaModules import AwWebCore
#from pandac.PandaModules import AwWebViewListener

WEB_WIDTH_PIXELS = 784
WEB_HEIGHT_PIXELS = 451
WEB_WIDTH = 1024
WEB_HEIGHT = 512
WEB_HALF_WIDTH = WEB_WIDTH / 2

WIN_WIDTH = 800
WIN_HEIGHT = 600

GlobalWebcore = None


#class HtmlView( DirectObject, AwWebViewListener):
class HtmlView( DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("HtmlView")
    useHalfTexture = base.config.GetBool("news-half-texture", 0)
            
    def __init__(self, parent = aspect2d):        
        """Properly initialize ourself."""
        #AwWebViewListener.AwWebViewListener.__init__(self)
        self.parent = parent
        self.mx =0
        self.my = 0
        self.htmlFile = "index.html"
        self.transparency = False # this is important looks weird if it's true
        global GlobalWebcore
        if GlobalWebcore:
            # we get a C++ crash if we construct webcore a second time
            pass
        else:
            GlobalWebcore = AwWebCore(AwWebCore.LOGVERBOSE, True, AwWebCore.PFBGRA)
            GlobalWebcore.setBaseDirectory('.')
            for errResponse in xrange(400,600):
                GlobalWebcore.setCustomResponsePage(errResponse, "error.html");			
		
        self.webView = GlobalWebcore.createWebView(WEB_WIDTH, WEB_HEIGHT, self.transparency, False, 70)		
	#self.webView.setListener(self)
        #self.webView.setCallback("requestFPS");
        frameName = ''
        inGameNewsUrl = self.getInGameNewsUrl() 
        #self.webView.loadURL2(inGameNewsUrl)

        self.imgBuffer = array.array('B')
        for i in xrange(WEB_WIDTH*WEB_HEIGHT):
            self.imgBuffer.append(0)
            self.imgBuffer.append(0)
            self.imgBuffer.append(0)
            self.imgBuffer.append(255)

        if self.useHalfTexture:
            self.leftBuffer = array.array('B')
            for i in xrange(WEB_HALF_WIDTH*WEB_HEIGHT):
                self.leftBuffer.append(0)
                self.leftBuffer.append(0)
                self.leftBuffer.append(0)
                self.leftBuffer.append(255)
            self.rightBuffer = array.array('B')
            for i in xrange(WEB_HALF_WIDTH*WEB_HEIGHT):
                self.rightBuffer.append(0)
                self.rightBuffer.append(0)
                self.rightBuffer.append(0)
                self.rightBuffer.append(255)

        self.setupTexture()
        if self.useHalfTexture:
            self.setupHalfTextures()        
			
        #self.interval = LerpHprInterval(self.quad, 2, Vec3(360, 0, 0), Vec3(0, 0, 0))
			
        #self.accept("escape", sys.exit, [0])
        #self.accept("w", self.writeTex)
		
        self.accept("mouse1", self.mouseDown, [AwWebView.LEFTMOUSEBTN])
        self.accept("mouse3", self.mouseDown, [ AwWebView.RIGHTMOUSEBTN])
        self.accept("mouse1-up", self.mouseUp, [AwWebView.LEFTMOUSEBTN])
        self.accept("mouse3-up", self.mouseUp, [ AwWebView.RIGHTMOUSEBTN])
		
        #self.accept("f1", self.toggleRotation)
        #self.accept("f2", self.toggleTransparency)
        #self.accept("f3", self.reload)
        #self.accept("f4", self.zoomIn)
        #self.accept("f5", self.zoomOut)		

        #taskMgr.doMethodLater(1.0, self.update, 'HtmlViewUpdateTask')
        # we get a problem if a mid-frame hearbeat fires of this task in conjunction with igLoop
        #taskMgr.add(self.update, 'HtmlViewUpdateTask',  priority = 51)
        #taskMgr.add(self.update, 'HtmlViewUpdateTask')
        #base.newsFrame = self
                
    def getInGameNewsUrl(self):
        """Get the appropriate URL to use if we are in test, qa, or live."""
        # First if all else fails, we hard code the live news url
        result = base.config.GetString("fallback-news-url", "http://cdn.toontown.disney.go.com/toontown/en/gamenews/")
        # next check if we have an override, say they want to url to point to a file in their harddisk
        override = base.config.GetString("in-game-news-url", "")
        if override:
            self.notify.info("got an override url,  using %s for in a game news" % override)
            result = override
        else:
            try:
                launcherUrl = base.launcher.getValue("GAME_IN_GAME_NEWS_URL", "")
                if launcherUrl:                    
                    result = launcherUrl
                    self.notify.info("got GAME_IN_GAME_NEWS_URL from launcher using %s" % result)
                else:
                    self.notify.info("blank GAME_IN_GAME_NEWS_URL from launcher, using %s" % result)
                    
            except:
                self.notify.warning("got exception getting GAME_IN_GAME_NEWS_URL from launcher, using %s" % result)
        return result
                        
    def setupTexture(self):
        cm = CardMaker('quadMaker')
        cm.setColor(1.0, 1.0, 1.0, 1.0)
					
        aspect = base.camLens.getAspectRatio()
        htmlWidth = 2.0*aspect * WEB_WIDTH_PIXELS / float(WIN_WIDTH)		
        htmlHeight = 2.0*float(WEB_HEIGHT_PIXELS) / float(WIN_HEIGHT) 

        # the html area will be center aligned and vertically top aligned
        #cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, 1.0 - htmlHeight, 1.0)
        cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, - htmlHeight / 2.0, htmlHeight / 2.0)

        bottomRightX = (WEB_WIDTH_PIXELS) / float( WEB_WIDTH +1)
        bottomRightY = WEB_HEIGHT_PIXELS / float (WEB_HEIGHT+1)

        #cm.setUvRange(Point2(0,0), Point2(bottomRightX, bottomRightY))
        cm.setUvRange(Point2(0,1-bottomRightY), Point2(bottomRightX,1))
        
        card = cm.generate()
        self.quad = NodePath(card)
        self.quad.reparentTo(self.parent)	

        self.guiTex = Texture("guiTex")
        self.guiTex.setupTexture(Texture.TT2dTexture, WEB_WIDTH, WEB_HEIGHT, 1, Texture.TUnsignedByte, Texture.FRgba)
        self.guiTex.setMinfilter(Texture.FTLinear)
        self.guiTex.setKeepRamImage(True)		
        self.guiTex.makeRamImage()				
        self.guiTex.setWrapU(Texture.WMRepeat)
        self.guiTex.setWrapV(Texture.WMRepeat)

        ts = TextureStage('webTS')
        self.quad.setTexture(ts, self.guiTex)
        self.quad.setTexScale(ts, 1.0, -1.0)

        self.quad.setTransparency(0)
        self.quad.setTwoSided(True)
        self.quad.setColor(1.0, 1.0, 1.0, 1.0)
        #self.quad.setZ(0.1) # shtickerbook is moved up by 0.1

        self.calcMouseLimits()

    def setupHalfTextures(self):
        self.setupLeftTexture()
        self.setupRightTexture()
        self.fullPnmImage = PNMImage(WEB_WIDTH, WEB_HEIGHT, 4)
        self.leftPnmImage = PNMImage(WEB_HALF_WIDTH, WEB_HEIGHT, 4)
        self.rightPnmImage = PNMImage(WEB_HALF_WIDTH, WEB_HEIGHT, 4)

    def setupLeftTexture(self):
        cm = CardMaker('quadMaker')
        cm.setColor(1.0, 1.0, 1.0, 1.0)
					
        aspect = base.camLens.getAspectRatio()
        htmlWidth = 2.0*aspect * WEB_WIDTH / float(WIN_WIDTH)		
        htmlHeight = 2.0*float(WEB_HEIGHT) / float(WIN_HEIGHT) 

        # the html area will be center aligned and vertically top aligned
        #cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, 1.0 - htmlHeight, 1.0)
        cm.setFrame(-htmlWidth/2.0, 0, - htmlHeight / 2.0, htmlHeight / 2.0)
        card = cm.generate()
        self.leftQuad = NodePath(card)
        self.leftQuad.reparentTo(self.parent)	

        self.leftGuiTex = Texture("guiTex")
        self.leftGuiTex.setupTexture(Texture.TT2dTexture, WEB_HALF_WIDTH, WEB_HEIGHT, 1, Texture.TUnsignedByte, Texture.FRgba)
        self.leftGuiTex.setKeepRamImage(True)		
        self.leftGuiTex.makeRamImage()				
        self.leftGuiTex.setWrapU(Texture.WMClamp)
        self.leftGuiTex.setWrapV(Texture.WMClamp)

        ts = TextureStage('leftWebTS')
        self.leftQuad.setTexture(ts, self.leftGuiTex)
        self.leftQuad.setTexScale(ts, 1.0, -1.0)

        self.leftQuad.setTransparency(0)
        self.leftQuad.setTwoSided(True)
        self.leftQuad.setColor(1.0, 1.0, 1.0, 1.0)
        #self.quad.setZ(0.1) # shtickerbook is moved up by 0.1

    def setupRightTexture(self):
        cm = CardMaker('quadMaker')
        cm.setColor(1.0, 1.0, 1.0, 1.0)
					
        aspect = base.camLens.getAspectRatio()
        htmlWidth = 2.0*aspect * WEB_WIDTH / float(WIN_WIDTH)		
        htmlHeight = 2.0*float(WEB_HEIGHT) / float(WIN_HEIGHT) 

        # the html area will be center aligned and vertically top aligned
        #cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, 1.0 - htmlHeight, 1.0)
        cm.setFrame(0, htmlWidth/2.0, - htmlHeight / 2.0, htmlHeight / 2.0)
        card = cm.generate()
        self.rightQuad = NodePath(card)
        self.rightQuad.reparentTo(self.parent)	

        self.rightGuiTex = Texture("guiTex")
        self.rightGuiTex.setupTexture(Texture.TT2dTexture, WEB_HALF_WIDTH, WEB_HEIGHT, 1, Texture.TUnsignedByte, Texture.FRgba)
        self.rightGuiTex.setKeepRamImage(True)		
        self.rightGuiTex.makeRamImage()				
        self.rightGuiTex.setWrapU(Texture.WMClamp)
        self.rightGuiTex.setWrapV(Texture.WMClamp)

        ts = TextureStage('rightWebTS')
        self.rightQuad.setTexture(ts, self.rightGuiTex)
        self.rightQuad.setTexScale(ts, 1.0, -1.0)

        self.rightQuad.setTransparency(0)
        self.rightQuad.setTwoSided(True)
        self.rightQuad.setColor(1.0, 1.0, 1.0, 1.0)
        #self.quad.setZ(0.1) # shtickerbook is moved up by 0.1
        

    def calcMouseLimits(self):                
        ll = Point3()
        ur = Point3()
        self.quad.calcTightBounds(ll,ur)
        self.notify.debug("ll=%s ur=%s" % (ll,ur))

        # we need to get our relative position to aspect2d, since shtiker books is shifted
        offset = self.quad.getPos(aspect2d)
        self.notify.debug("offset = %s " % offset)
        ll.setZ(ll.getZ() +  offset.getZ())
        ur.setZ(ur.getZ() + offset.getZ())
                
        self.notify.debug("new LL=%s, UR=%s" % (ll,ur))

        relPointll = self.quad.getRelativePoint(aspect2d, ll)
        self.notify.debug("relPoint = %s" % relPointll)
        self.mouseLL = (aspect2d.getScale()[0] * ll[0], aspect2d.getScale()[2] * ll[2])
        self.mouseUR = (aspect2d.getScale()[0] * ur[0], aspect2d.getScale()[2] * ur[2])
        self.notify.debug("original mouseLL=%s, mouseUR=%s" % (self.mouseLL, self.mouseUR))
		
    def writeTex(self, filename = "guiText.png"):
        self.notify.debug("writing texture")
        self.guiTex.generateRamMipmapImages()
        self.guiTex.write(filename)
		
    def toggleRotation(self):
        if self.interval.isPlaying():
            self.interval.finish()
        else:
            self.interval.loop()
		
    def mouseDown(self, button):
        messenger.send('wakeup')
        self.webView.injectMouseDown(button)
		
    def mouseUp(self, button):
        self.webView.injectMouseUp(button)
	
    def reload(self):
        pass
        #self.webView.loadFile(self.htmlFile, '')		
		
    def zoomIn(self):
        self.webView.zoomIn()
		
    def zoomOut(self):
        self.webView.zoomOut()
		
    def toggleTransparency(self):
        self.transparency = not self.transparency
        self.webView.setTransparent(self.transparency)
		
    def update(self, task):
        global GlobalWebcore
        if base.mouseWatcherNode.hasMouse():
            x, y = self._translateRelativeCoordinates(base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
            #self.notify.debug('got mouse move %d %d' % (x,y))
            #self.webView.injectMouseMove(x, y)			
            
            if (self.mx - x) != 0 or (self.my - y) != 0:
                self.webView.injectMouseMove(x, y)
                #self.notify.debug('injecting mouse move %d %d' % (x,y))
                self.mx, self.my = x, y				
                
            if self.webView.isDirty():
                #self.notify.debug("webview is dirty")
                self.webView.render(self.imgBuffer.buffer_info()[0], WEB_WIDTH*4, 4)
                #Texture.setTexturesPower2(AutoTextureScale.ATSUp)
                Texture.setTexturesPower2(2)
                #self.notify.debug("about to modify ram image")
                textureBuffer = self.guiTex.modifyRamImage()
                #import pdb; pdb.set_trace()
                #self.notify.debug("about to call textureBuffer.setData")
                textureBuffer.setData(self.imgBuffer.tostring())
                #self.notify.debug("done calling setData")
                if self.useHalfTexture:
                    # TODO check with DRose, this feels inefficient
                    self.guiTex.store(self.fullPnmImage)
                    self.leftPnmImage.copySubImage(self.fullPnmImage, 0, 0, 0, 0, WEB_HALF_WIDTH, WEB_HEIGHT)
                    self.rightPnmImage.copySubImage(self.fullPnmImage, 0, 0, WEB_HALF_WIDTH, 0, WEB_HALF_WIDTH, WEB_HEIGHT)
                    self.leftGuiTex.load(self.leftPnmImage)
                    self.rightGuiTex.load(self.rightPnmImage)                    
                    self.quad.hide()
                #Texture.setTexturesPower2(AutoTextureScale.ATSDown)
                Texture.setTexturesPower2(1)
                
			
            GlobalWebcore.update()
        return Task.cont				
	
		
    def _translateRelativeCoordinates(self, x, y):
        sx = int((x - self.mouseLL[0]) / (self.mouseUR[0] - self.mouseLL[0]) * WEB_WIDTH_PIXELS)
        sy = WEB_HEIGHT_PIXELS - int((y - self.mouseLL[1]) / (self.mouseUR[1] - self.mouseLL[1]) * WEB_HEIGHT_PIXELS)
        return sx, sy

    def unload(self):
        """Clean up everything, especially the awesomium bits."""
        self.ignoreAll()
        self.webView.destroy()
        self.webView = None
        #global GlobalWebcore
        #GlobalWebcore = None
        pass

		
    # --------------------[ WebViewListener implementation ]--------------------------
    def onCallback(self, name, args):
        assert self.notify.debugStateCall(self)
        if name == "requestFPS":					
            #self.webView.setProperty( "fps", JSValue("%.1f" % (1.0 / globalClock.getDt())) )
            #self.webView.executeJavascript("updateFPS()", "")
            pass
			
    def onBeginNavigation(self, url,  frameName):
        assert self.notify.debugStateCall(self)
        pass
		
    def onBeginLoading(self, url, frameName, statusCode, mimeType):
        assert self.notify.debugStateCall(self)
        pass
		
    def onFinishLoading(self):
        assert self.notify.debugStateCall(self)
        self.notify.debug( "finished loading")
        pass
		
    def onReceiveTitle(self, title, frameName):
        assert self.notify.debugStateCall(self)
        pass
		
    def onChangeTooltip(self, tooltip):
        assert self.notify.debugStateCall(self)
        pass
		
    def onChangeCursor(self, cursor):
        assert self.notify.debugStateCall(self)
        pass
		
    def onChangeKeyboardFocus(self, isFocused):
        assert self.notify.debugStateCall(self)
        pass
		
    def onChangeTargetURL(self, url):
        assert self.notify.debugStateCall(self)
        pass
		
