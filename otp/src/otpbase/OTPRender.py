
from pandac.PandaModules import *

# global bitmasks for cameras
MainCameraBitmask = BitMask32.bit(0)
ReflectionCameraBitmask = BitMask32.bit(1)
ShadowCameraBitmask = BitMask32.bit(2)
SkyReflectionCameraBitmask = BitMask32.bit(3)
GlowCameraBitmask = BitMask32.bit(4)
EnviroCameraBitmask = BitMask32.bit(5)

# sample using global camera bitmasks and how to turn off rendering of an object depending on a certain camera
#
#   # import
#   from otp.otpbase import OTPRender
#
#   # camera setup
#   reflection_camera = Camera ('reflection_camera')
#   reflection_camera.setCameraMask (OTPRender.ReflectionCameraBitmask)
#
#   # don't render "node_path" for all cameras that have the OTPRender.ReflectionCameraBitmask
#   OTPRender.setCameraBitmask (False, node_path, OTPRender.ReflectionCameraBitmask, 'object_name', tag_function, context):
#

# default = boolean value to specify the default behavior
#   True = render reflection, False = do not render reflection
# node_path = Panda NodePath object
# camera_bitmask = bitmask used to hide/show objects from the camera
# tag = optional name of object/nodepath
# tag_function = an optional application specific callback to
#   override default render behavior. For example, a game may have an
#   option to have an object reflected or not. The callback helps makes
#   code more friendly since all decision logic should be the callback.
#   if the tag_function is not used, then pass in None as the parameter.
#   The function prototype is "tag_function (default, tag, context)".
#   Sample function,
#      def my_tag_function (default, tag, context)
#          show = default
#          if (tag == 'my_object'):
#              show = False
#          return show
#
# context = optional context object

def setCameraBitmask (default, node_path, camera_bitmask, tag = None, tag_function = None, context = None):
    if (node_path):
        show = default
        if (tag_function):
            show = tag_function (default, tag, context)
        if (show):
            node_path.show (camera_bitmask)
        else:
            node_path.hide (camera_bitmask)
#    print "setCameraBitmask", tag

# shortcut function just for reflections
def renderReflection (default, node_path, tag = None, tag_function = None, context = None):
    setCameraBitmask (default, node_path, ReflectionCameraBitmask, tag, tag_function, context)
    
# similar shortcut function for shadows
def renderShadow (default, node_path, tag = None, tag_function = None, context = None):
    setCameraBitmask (default, node_path, ShadowCameraBitmask, tag, tag_function, context)

# shortcut function just for sky reflections
def renderSkyReflection (default, node_path, tag = None, tag_function = None, context = None):
    setCameraBitmask (default, node_path, SkyReflectionCameraBitmask, tag, tag_function, context)

# shortcut functions for glow
def renderGlow (default, node_path, tag = None, tag_function = None, context = None):
    setCameraBitmask (default, node_path, GlowCameraBitmask, tag, tag_function, context)

# shortcut function for additive blend effects
def setAdditiveEffect (node_path, tag = None, bin_name = None, lighting_on = False, reflect = False):
    if (node_path):
        # additive blend states
        node_path.setTransparency (True)
        node_path.setDepthWrite (False)
        node_path.node ( ).setAttrib (ColorBlendAttrib.make (ColorBlendAttrib.MAdd))

        # do not light
        if (lighting_on == False):
            node_path.setLightOff ( )

        # disable writes to destination alpha, write out rgb colors only
        node_path.setAttrib (ColorWriteAttrib.make (ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue));

        # do not display in reflections
        if (reflect == False):
            renderReflection (False, node_path, tag, None)

        if (bin_name):
            node_path.setBin(bin_name, 0)
