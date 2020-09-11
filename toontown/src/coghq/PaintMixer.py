"""PaintMixer module: contains the PaintMixer class"""

import PlatformEntity

class PaintMixer(PlatformEntity.PlatformEntity):
    def start(self):
        PlatformEntity.PlatformEntity.start(self)
        model = self.platform.model
        shaft = model.find('**/PaintMixerBase1')
        shaft.setSz(self.shaftScale)
        # we can't flatten out the scale unless we remove the DCS
        shaft.node().setPreserveTransform(0)
        # there's another node with DCS/preserve transform underneath
        shaftChild = shaft.find('**/PaintMixerBase')
        shaftChild.node().setPreserveTransform(0)
        model.flattenMedium()
        """ this doesn't seem to do anything.
        # incorporate the mixer's overall scale, and flatten all scales
        model.setScale(self.getScale())
        self.setScale(1)
        model.flattenMedium()
        """
        
