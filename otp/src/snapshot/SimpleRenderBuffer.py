import direct
from pandac.PandaModules import *

class SimpleRenderBuffer:

    """ Opens an offscreen buffer for simple, lightweight rendering
    without adversely impacting other code (much). """
    
    def __init__(self, xsize, ysize):
        # Get the graphics pipe.
        selection = GraphicsPipeSelection.getGlobalPtr()

        # Use tinydisplay for software rendering.
        # Moving away from Mesa due to general bugginess.
        pipeList = [
            ('TinyOffscreenGraphicsPipe', 'tinydisplay'),
            ]

        for pipeName, libname in pipeList:
            self.pipe = selection.makePipe(pipeName, libname)
            if self.pipe:
                break

        if not self.pipe:
            self.pipe = selection.makeDefaultPipe()
            
        assert self.pipe

        # Create a GraphicsEngine to manage rendering.  It might be
        # better if we shared this with other GraphicsEngines.
        self.graphicsEngine = GraphicsEngine()

        # Open an offscreen buffer.
        props = WindowProperties.getDefault()
        props.setSize(xsize, ysize)
        fbprops = FrameBufferProperties(FrameBufferProperties.getDefault())
        fbprops.setBackBuffers(0)
        flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BFRefuseWindow

        self.buffer = self.graphicsEngine.makeOutput(
            self.pipe, 'buffer', 0, fbprops, props, flags)
        assert self.buffer

        # Crank up the texture filtering quality for tinydisplay
        self.buffer.getGsg().setTextureQualityOverride(Texture.QLBest)

        # Require all the textures to be available now.
        self.buffer.getGsg().setIncompleteRender(False)
        
        # Now create a scene, and a camera, and a DisplayRegion.
        self.render = NodePath('render')
        self.camera = self.render.attachNewNode('camera')
        self.camNode = Camera('cam')
        self.camLens = self.camNode.getLens()
        self.cam = self.camera.attachNewNode(self.camNode)

        dr = self.buffer.makeDisplayRegion()
        dr.setCamera(self.cam)

    def renderFrame(self):
        """ Renders a single frame of whatever's parented to self.render. """
        self.graphicsEngine.renderFrame()

    def cleanup(self):
        self.graphicsEngine.removeWindow(self.buffer)
        
