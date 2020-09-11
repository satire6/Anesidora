"""
OTPBase module: contains the OTPBase class
"""

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Camera, TPLow, VBase4, ColorWriteAttrib, Filename, getModelPath, NodePath
import OTPRender
import time
import math
import re

class OTPBase(ShowBase):
    def __init__(self, windowType = None):
       self.wantEnviroDR = False
       ShowBase.__init__(self, windowType = windowType)

       if config.GetBool("want-phase-checker", 0):
            from direct.showbase import Loader
            Loader.phaseChecker = self.loaderPhaseChecker
            self.errorAccumulatorBuffer = ''
            taskMgr.add(self.delayedErrorCheck, "delayedErrorCheck", priority = 10000)


       # Turn nametags on and off for video capture
       self.wantNametags = self.config.GetBool('want-nametags', 1)

       self.slowCloseShard = self.config.GetBool(
           'slow-close-shard', 0)
       self.slowCloseShardDelay = self.config.GetFloat(
           'slow-close-shard-delay', 10.)

       self.fillShardsToIdealPop = self.config.GetBool(
            'fill-shards-to-ideal-pop', 1)

       # By default, we want to use dynamic shadows.  ToonBase.py
       # turns this off.
       self.wantDynamicShadows = 1

       self.stereoEnabled = False
       self.enviroDR = None
       self.enviroCam = None
       self.pixelZoomSetup = False

       # These are mainly for reporting to the AI.  They're filled in
       # by the application at startup, and as we move from place to
       # place.
       self.gameOptionsCode = ''
       self.locationCode = ''
       self.locationCodeChanged = time.time()

       # Set the default camera to use the appropriate bitmask.
       if (base.cam):
           if(self.wantEnviroDR):
               base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
           else:
               base.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)

       taskMgr.setupTaskChain('net')

    def setTaskChainNetThreaded(self):
        """ If want-threaded-network is true, move the network tasks
        to a separate thread, so they will execute in the background. """

        # Should networking tasks run in a separate thread?
        # Hopefully, this will smooth out runtime chugs due to long
        # Python tasks that process incoming generates and whatnot.
        # On the other hand, it does mean that at least some of our
        # Python code has to be thread-savvy (use
        # direct.stdpy.threading module for this).  Currently
        # EXPERIMENTAL; enable this at your own risk!
        if base.config.GetBool('want-threaded-network', 0):
            taskMgr.setupTaskChain('net', numThreads = 1, frameBudget = 0.001,
                                   threadPriority = TPLow)

    def setTaskChainNetNonthreaded(self):
        """ Move the network tasks to the main thread, so they will
        execute in the foreground.  This is normally done during a
        loading screen. """

        taskMgr.setupTaskChain('net', numThreads = 0, frameBudget = -1)

    def toggleStereo(self):
        """ Enables or disables a red-blue stereo mode.  This can also
        potentially hook into true shutter-glass stereo, if the
        graphics hardware and driver support this, and if the
        framebuffer-stereo config variable had been set at
        startup. """

        self.stereoEnabled = not self.stereoEnabled

        if self.stereoEnabled:
            # If the window framebuffer doesn't support stereo as-is
            # (i.e. true hardware stereo), then we need to enable
            # red-blue stereo.
            if not base.win.isStereo():
                base.win.setRedBlueStereo(True, ColorWriteAttrib.CRed, ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue)

        if self.wantEnviroDR:
            # Reset the environment DR if we're using it.  This also
            # resets the main DR.
            self.setupEnviroCamera()
            return

        # If we're not using the enviroDR, at least ensure the main DR
        # is reset.
        mainDR = base.camNode.getDisplayRegion(0)
        if self.stereoEnabled:
            if not mainDR.isStereo():
                base.win.removeDisplayRegion(mainDR)
                mainDR = base.win.makeStereoDisplayRegion()
                mainDR.getRightEye().setClearDepthActive(True)
                mainDR.setCamera(base.cam)
        else:
            if mainDR.isStereo():
                base.win.removeDisplayRegion(mainDR)
                mainDR = base.win.makeMonoDisplayRegion()
                mainDR.setCamera(base.cam)

    def setupEnviroCamera(self):
        """ Set up a special DisplayRegion and camera for rendering
        environments, especially big, lush environments like the
        islands in Pirates.  It's mainly useful in conjunction with
        setupAutoPixelZoom, which then allows us to zoom down the
        resolution of this DisplayRegion, independently of the smaller
        objects in the scene like avatars and their nametags, when we
        need better frame rate (this is useful only with the
        tinydisplay software renderer). """

        clearColor = VBase4(0, 0, 0, 1)
        if self.enviroDR:
            clearColor = self.enviroDR.getClearColor()
            self.win.removeDisplayRegion(self.enviroDR)

        if not self.enviroCam:
            self.enviroCam = self.cam.attachNewNode(Camera('enviroCam'))
            

        mainDR = self.camNode.getDisplayRegion(0)
        if self.stereoEnabled:
            # If we are in stereo mode, set up the left and right eyes
            # properly w.r.t. the main display region.  We need to
            # draw both left channels, clear the depth once, then draw
            # both right channels.

            self.enviroDR = self.win.makeStereoDisplayRegion()
            if not mainDR.isStereo():
                # If the main DR isn't a stereo DisplayRegion, make it
                # one.
                self.win.removeDisplayRegion(mainDR)
                mainDR = self.win.makeStereoDisplayRegion()
                mainDR.setCamera(self.cam)
            
            ml = mainDR.getLeftEye()
            mr = mainDR.getRightEye()
            el = self.enviroDR.getLeftEye()
            er = self.enviroDR.getRightEye()

            el.setSort(-8)
            ml.setSort(-6)
            er.setSort(-4)
            er.setClearDepthActive(True)
            mr.setSort(-2)
            mr.setClearDepthActive(False)

        else:
            # If we're not in stereo mode, make sure our main DR isn't
            # either.
            self.enviroDR = self.win.makeMonoDisplayRegion()
            if mainDR.isStereo():
                self.win.removeDisplayRegion(mainDR)
                mainDR = self.win.makeMonoDisplayRegion()
                mainDR.setCamera(self.cam)

            self.enviroDR.setSort(-10)
            
        self.enviroDR.setClearColor(clearColor)
        self.win.setClearColor(clearColor)
        self.enviroDR.setCamera(self.enviroCam)
        self.enviroCamNode = self.enviroCam.node()
        self.enviroCamNode.setLens(self.cam.node().getLens())
        self.enviroCamNode.setCameraMask(OTPRender.EnviroCameraBitmask)
        render.hide(OTPRender.EnviroCameraBitmask)
        self.camList.append(self.enviroCam)
        self.backgroundDrawable = self.enviroDR

        # Texture reloads for things in the environment
        # (i.e. background objects) are the lowest priority.  Load
        # gui items, foreground object textures, and animations first.
        self.enviroDR.setTextureReloadPriority(-10)

        if self.pixelZoomSetup:
            # If we want pixel zoom, enable it for the new display
            # region.
            self.setupAutoPixelZoom()
            

    def setupAutoPixelZoom(self):
        """ Sets up the system to zoom the pixel resolution of the
        enviroCam DisplayRegion on demand.  This makes setPixelZoom()
        functional. """

        self.win.setPixelZoom(1)
        self.enviroDR.setPixelZoom(1)

        if not self.stereoEnabled:
            # Normally, we want the clear to happen in the first
            # display region, not in the window itself.  This allows
            # us to set the pixel_zoom on the display region.
            self.enviroDR.setClearColorActive(True)
            self.enviroDR.setClearDepthActive(True)
            self.win.setClearColorActive(False)
            self.win.setClearDepthActive(False)
            self.backgroundDrawable = self.enviroDR
        else:
            # In stereo mode, we want the clear to happen in the
            # window itself; we can't pixel_zoom just the display
            # region (because the pixel densities are different).
            self.enviroDR.setClearColorActive(False)
            self.enviroDR.setClearDepthActive(False)
            self.enviroDR.getRightEye().setClearDepthActive(True)
            self.win.setClearColorActive(True)
            self.win.setClearDepthActive(True)
            self.backgroundDrawable = self.win
        
        self.pixelZoomSetup = True
        self.targetPixelZoom = 1.0
        self.pixelZoomTask = None
        self.pixelZoomCamHistory = 2.0
        self.pixelZoomCamMovedList = []
        self.pixelZoomStarted = None

        flag = self.config.GetBool('enable-pixel-zoom', True)
        self.enablePixelZoom(flag)


    def enablePixelZoom(self, flag):
        """ Enables a special mode in which the display region that
        represents the background geometry (self.enviroDR) is
        de-rezzed so it renders in a blockier form when the camera is
        moving consistently.  This should achieve a better frame rate
        when using the tinydisplay software renderer, especially when
        there are lot of pixels in the background.

        It is possible that setting this on may *hurt* performance
        when the background is mostly empty.  So use with caution.

        This doesn't impact frame rate much at all when using normal
        hardware accelerated rendering, but since it checks for the
        presence of a hardware renderer and does nothing in this case,
        it is always safe to call this method. """
        
        if not self.backgroundDrawable.supportsPixelZoom():
            flag = False

        self.pixelZoomEnabled = flag
        taskMgr.remove('chasePixelZoom')
        if flag:
            taskMgr.add(self.__chasePixelZoom, 'chasePixelZoom', priority = -52)
        else:
            self.backgroundDrawable.setPixelZoom(1)

    def __chasePixelZoom(self, task):
        """ Sets the pixel zoom of the main 3D window to an
        appropriate value according to how rapidly the camera appears
        to be moving.  When the camera is stationary, this is set to
        is 1.0.  Larger numbers are coarser but render faster.  This
        only has an effect when running with the tinydisplay software
        renderer. """

        now = globalClock.getFrameTime()
        pos = base.cam.getNetTransform().getPos()
        prevPos = base.cam.getNetPrevTransform().getPos()
        d2 = (pos - prevPos).lengthSquared()
        if d2:
            d = math.sqrt(d2)
            # Add a new move report
            self.pixelZoomCamMovedList.append((now, d))

        # Delete any old move reports.
        while (self.pixelZoomCamMovedList and self.pixelZoomCamMovedList[0][0] < now - self.pixelZoomCamHistory):
            del self.pixelZoomCamMovedList[0]

        # Now set the pixel zoom according to the average feet per
        # second the camera has moved over the past history seconds.
        dist = sum(map(lambda pair: pair[1], self.pixelZoomCamMovedList))
        speed = dist / self.pixelZoomCamHistory

        if speed < 5:
            # We're stopped.
            self.backgroundDrawable.setPixelZoom(4)
            self.pixelZoomStart = None

        elif speed > 10:
            # We're running.
            if self.pixelZoomStart == None:
                self.pixelZoomStart = now
            elapsed = now - self.pixelZoomStart

            if elapsed > 10:
                self.backgroundDrawable.setPixelZoom(16)
            elif elapsed > 5:
                self.backgroundDrawable.setPixelZoom(8)

        return task.cont

    def getShardPopLimits(self):
         # returns (low, mid, high)
         # override if desired
         return 300, 600, 1200
     
    def setLocationCode(self, locationCode):
        if locationCode != self.locationCode:
            self.locationCode = locationCode
            self.locationCodeChanged = time.time()

    def delayedErrorCheck(self, task):
        if(self.errorAccumulatorBuffer):
            buffer = self.errorAccumulatorBuffer
            self.errorAccumulatorBuffer = ''
            self.notify.error("\nAccumulated Phase Errors!:\n %s"%buffer)
        return task.cont

    def loaderPhaseChecker(self, path, loaderOptions):
        # See if this path is in the phase system
        # It should look something like "phase_5/models/char/joe"

        # HACK: let's try .bam if it has no extension
        # Other way to do this: after we load the model, call model.node().getFullpath()
        if("audio/" in path):
            return 1
        file = Filename(path)
        if not file.getExtension():
            file.setExtension('bam')
        mp = getModelPath()
        path = mp.findFile(file).cStr()
        if not path:
            return

        match = re.match(".*phase_([^/]+)/", path)
        if(not match):
            if('dmodels' in path):
                return
            else:
                self.errorAccumulatorBuffer += "file not in phase (%s, %s)\n"%(file,path)
                return        

        basePhase = float(match.groups()[0])
        if(not launcher.getPhaseComplete(basePhase)):
            self.errorAccumulatorBuffer += "phase is not loaded for this model %s\n"%(path)
        #grab the model
        model = loader.loader.loadSync(Filename(path), loaderOptions)

        if(model):
            model = NodePath(model)
            for tex in model.findAllTextures():
                texPath = tex.getFullpath().cStr()
                match = re.match(".*phase_([^/]+)/", texPath)
                if(match):
                    texPhase = float(match.groups()[0])
                    if(texPhase > basePhase):
                        self.errorAccumulatorBuffer += "texture phase is higher than the models (%s, %s)\n"%(path, texPath)

    def getRepository(self):
        return self.cr

    def openMainWindow(self, *args, **kw):
        result = ShowBase.openMainWindow(self, *args, **kw)
        if result:
            self.wantEnviroDR = (not self.win.getGsg().isHardware() or config.GetBool("want-background-region",1))
            self.backgroundDrawable = self.win
            pass
        return result
