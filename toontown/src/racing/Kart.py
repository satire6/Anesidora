##########################################################################
# Module: Kart.py
# Purpose: This class overseas the loading of the Kart Module based on the
#          the specified DNA. test
# Date: 4/25/05
# Author: jjtaylor
##########################################################################

##########################################################################
# Panda Import Modules
##########################################################################
#from direct.directbase import DirectStart
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.avatar import ShadowCaster                          

##########################################################################
# Toontown Import Modules
##########################################################################
from toontown.racing.KartDNA import *
from toontown.toonbase import TTLocalizer
"""
Use this class to create a kart that just sits there
and looks pretty.  Use DistributedVehicle, however,
to create a phsyics-based, movable/controllable one.
"""

class Kart(NodePath, ShadowCaster.ShadowCaster): 

    ######################################################################
    # Class Variable Definitions
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory("Kart")
    #notify.setDebug(1)
    
    index = 0
    baseScale = 2.0

    RFWHEEL = 0
    LFWHEEL = 1
    RRWHEEL = 2
    LRWHEEL = 3
    
    wheelData = [{'node' : "wheel*Node2",},
                 {'node' : "wheel*Node1",},
                 {'node' : "wheel*Node3",},
                 {'node' : "wheel*Node4",},
              ]
    
    ShadowScale = 2.5#Point3(1.3, 2, 1)
    
    SFX_BaseDir = "phase_6/audio/sfx/"
    SFX_KartStart = SFX_BaseDir + "KART_Engine_start_%d.mp3"
    SFX_KartLoop = SFX_BaseDir + "KART_Engine_loop_%d.wav"

    def __init__( self ):
        """
        Purpose: The __init__ Method provides for the initial construction
        of the Kart instance.

        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)

        # pretend we are an actor
        an = ActorNode("vehicle-test")
        anp = NodePath(an)
        NodePath.assign(self, anp)
        self.actorNode = an

        ShadowCaster.ShadowCaster.__init__(self, False)

        Kart.index += 1

        # DNA and Model Information
        self.updateFields = []
        self.kartDNA = [ -1 ] * ( getNumFields() )
        self.kartAccessories = { KartDNA.ebType : None, KartDNA.spType : None,
                                 KartDNA.fwwType : (None,None), KartDNA.bwwType : (None,None) }
        self.texCount = 1
        
    def delete( self ):
        assert self.notify.debugStateCall(self)
        self.__stopWheelSpin()
        del self.kartDNA, self.updateFields

        self.kartLoopSfx.stop()

        NodePath.removeNode( self )
        ShadowCaster.ShadowCaster.delete(self)

    def getKartBounds(self):
        return self.geom[0].getTightBounds()

    def generateKart(self, forGui = 0):
        #create a NodePath to base everything on

        # If there is currently a geometry for the kart, then
        # this kart has already been generated once. Likely case is that
        # it merely needs a call to updateKart.
        assert not hasattr( self, 'geom' ), "Kart::generateKart - Kart has already been generated."
        assert self.kartDNA != [ -1 ] * ( getNumFields() ), "Kart::generateKart - attempt to generate Kart before DNA has been set."
        assert checkKartDNAValidity( self.kartDNA ), "Kart::generateKart - attempt to generate Kart based on bad DNA %s" % ( self.kartDNA )

        # We need LOD for these karts, oh yeah.
        self.LODnode = FadeLODNode( "lodNode" )
        self.LODpath = self.attachNewNode( self.LODnode )
        self.LODnode.setFadeTime( 0.15 )

        # Keep pointer to all kart instances
        self.geom = {}
        self.pitchNode = {}
        self.toonNode = {}
        self.rotateNode = self.attachNewNode('rotate')

        # LOD Switch Levels
        levelIn = [ base.config.GetInt( "lod1-in", 30 ), base.config.GetInt( "lod2-in", 80 ), base.config.GetInt( "lod2-in", 200 ) ]
        levelOut = [ base.config.GetInt( "lod1-out", 0 ), base.config.GetInt( "lod2-out", 30 ), base.config.GetInt( "lod2-out", 80 ) ]

        # figure out how many LOD levels we want, default to 3
        lodRequired = 3
        if( forGui ):
            lodRequired = 1
            # set in and out to min and max so kart shows up
            levelIn[ 0 ] = base.config.GetInt( "lod1-in", 2500 )
            levelIn[ 1 ] = base.config.GetInt( "lod1-out", 0 )

        self.toonSeat = NodePath("toonSeat")
        
        for level in range( lodRequired ):
            self.__createLODKart( level )
            self.LODnode.addSwitch( levelIn[ level ], levelOut[ level ] )

        self.setScale(self.baseScale)
        self.flattenMedium()

        for level in range( lodRequired ):
            self.toonSeat = self.toonSeat.instanceTo(self.toonNode[level])
        
        self.LODpath.reparentTo( self.rotateNode )

        # Geometry Accessory Scale
        tempNode = NodePath( "tempNode" )
        self.accGeomScale = tempNode.getScale( self.pitchNode[ 0 ] ) * self.baseScale
        #print self.accGeomScale
        tempNode.removeNode()
        
        # self.geom.flattenLight()

        self.__applyBodyColor()
        self.__applyEngineBlock()
        self.__applySpoiler()
        self.__applyFrontWheelWells()
        self.__applyBackWheelWells()
        self.__applyRims()
        self.__applyDecals()
        self.__applyAccessoryColor()

        #axis.reparentTo(self.pitchNode)
        #self.pitchNode.setH(270)

        # Create the wheelCenters (center of the wheel)
        self.wheelCenters = []
        self.wheelBases = []
        for wheel in self.wheelData:
            center = self.geom[0].find('**/' + wheel['node'])
            self.wheelCenters.append(center)

            wheelBase = center.getParent().attachNewNode('wheelBase')
            wheelBase.setPos(center.getPos())
            wheelBase.setZ(0)
            self.wheelBases.append(wheelBase)

        self.wheelBaseH = self.wheelCenters[0].getH()

        self.__startWheelSpin()
        self.setWheelSpinSpeed(0)

        if( not forGui ):
            self.shadowJoint = self.geom[0]
            self.initializeDropShadow()
            self.setActiveShadow()
            self.dropShadow.setScale(self.ShadowScale)
        else:
            #different shadow for GUI
            self.shadowJoint = self.LODpath
            self.initializeDropShadow()
            self.setActiveShadow()
            self.dropShadow.setScale(1.3, 3, 1)

        kartType = self.kartDNA[KartDNA.bodyType]
        self.kartStartSfx = base.loadSfx(self.SFX_KartStart % kartType)
        self.kartLoopSfx = base.loadSfx(self.SFX_KartLoop % kartType)
        self.kartLoopSfx.setLoop()


    def __createLODKart( self, level ):
        # Load Kart Model based on the body type of the dna.
        kartBodyPath = getKartModelPath( self.kartDNA[ KartDNA.bodyType ], level )
        self.geom[level] = loader.loadModel( kartBodyPath )
        self.geom[level].reparentTo( self.LODpath )
        self.geom[level].setH(180)
        #self.geom[level].setPos(0.0, 2.8, 0.025)
        self.geom[level].setPos(0.0, 0, 0.025)
        self.pitchNode[level] = self.geom[level].find("**/suspensionNode")
        self.toonNode[level] = self.geom[level].find("**/toonNode")

        # invert the values of the pitchNode on the toonNode... that
        # way, the toon won't need to be adjusted when he is
        # reparented
        scale = 1.0/self.pitchNode[level].getScale()[0]
        scale /= self.baseScale
        self.toonNode[level].setScale(scale)

        h = (180 + self.pitchNode[level].getH()) % 360
        self.toonNode[level].setH(h)

        #pos = -1 * self.pitchNode[level].getPos(render)
        # this position takes in to account the offset due to the 'sit'
        # animation
        pos = Point3(0, -1.3, -7)
        self.toonNode[level].setPos(pos)

    def resetGeomPos( self ):
        for level in self.geom.keys():
            self.geom[ level ].setPos( 0, 0, 0.025 )
        
    def __update( self ):
        """
        Purpose: The __update Method handles the visual update of the
        kart instance.

        Params: None
        Return: None        
        """
        for field in self.updateFields:
            if( field == KartDNA.bodyType ):
                if( hasattr( self, 'geom' ) ):
                    for kart in self.geom:
                        self.geom[ kart ].removeNode()
                        self.__createLODKart( kart )
                        self.geom[ kart ].reparentTo( self.rotateNode )

                    self.__applyBodyColor()
                    self.__applyEngineBlock()
                    self.__applySpoiler()
                    self.__applyFrontWheelWells()
                    self.__applyRims()
                    self.__applyDecals()
                    self.__applyAccessoryColor()
                else:
                    raise StandardError, "Kart::__update - Has this method been called before generateKart?"

            elif( field == KartDNA.bodyColor ):
                self.__applyBodyColor()
            elif( field == KartDNA.accColor ):
                self.__applyAccessoryColor()
            elif( field == KartDNA.ebType ):
                if( self.kartAccessories[ KartDNA.ebType ] != None ):
                    name = self.kartAccessories[ KartDNA.ebType ].getName()
                    for key in self.geom.keys():
                        # Remove node found in geom lod
                        self.geom[ key ].find( "**/%s" % ( name ) ).removeNode()

                    self.kartAccessories[ KartDNA.ebType ].removeNode()
                    self.kartAccessories[ KartDNA.ebType ] = None
                self.__applyEngineBlock()
            elif( field == KartDNA.spType ):
                if( self.kartAccessories[ KartDNA.spType ] != None ):
                    name = self.kartAccessories[ KartDNA.spType ].getName()
                    for key in self.geom.keys():
                        # Remove node found in geom lod
                        self.geom[ key ].find( "**/%s" % ( name ) ).removeNode()

                    self.kartAccessories[ KartDNA.spType ].removeNode()
                    self.kartAccessories[ KartDNA.spType ] = None
                self.__applySpoiler()
            elif( field == KartDNA.fwwType ):
                if( self.kartAccessories[ KartDNA.fwwType ] != (None,None) ):
                    left, right = self.kartAccessories[ KartDNA.fwwType ]
                    for key in self.geom.keys():
                        # Remove node found in geom lod
                        self.geom[ key ].find( "**/%s" % ( left.getName() ) ).removeNode()
                        self.geom[ key ].find( "**/%s" % ( right.getName() ) ).removeNode()

                    left.removeNode()
                    right.removeNode()
                    self.kartAccessories[ KartDNA.fwwType ] = (None, None)
                self.__applyFrontWheelWells()
            elif( field == KartDNA.bwwType ):
                if( self.kartAccessories[ KartDNA.bwwType ] != (None,None) ):
                    left, right = self.kartAccessories[ KartDNA.bwwType ]
                    for key in self.geom.keys():
                        # Remove node found in geom lod
                        self.geom[ key ].find( "**/%s" % ( left.getName() ) ).removeNode()
                        self.geom[ key ].find( "**/%s" % ( right.getName() ) ).removeNode()

                    left.removeNode()
                    right.removeNode()
                    self.kartAccessories[ KartDNA.bwwType ] = (None, None)
                self.__applyBackWheelWells()
            else:
                if( field == KartDNA.rimsType ):
                    self.__applyRims()
                elif( field == KartDNA.decalType ):
                    self.__applyDecals()
                else:
                    pass

                self.__applyAccessoryColor()

        self.updateFields = []

    def updateDNAField( self, field, fieldValue ):
        """
        Purpose: The updateDNAField Method properly updates the desired
        dna field with the field value that is 

        Params: field - dna field that should be updated.
                fieldValue - new value of the dna field.
        Return: None

        Note: Used for updating a single dna field. Also, validity
        checks are not performed at this point. It is assumed that they
        are handled elsewhere. ( This may change in the future )
        """
        if( field == KartDNA.bodyType ):
            self.setBodyType( fieldValue )
        elif( field  == KartDNA.bodyColor ):
            self.setBodyColor( fieldValue )
        elif( field == KartDNA.accColor ):
            self.setAccessoryColor( fieldValue )
        elif( field == KartDNA.ebType ):
            self.setEngineBlockType( fieldValue )
        elif( field == KartDNA.spType ):
            self.setSpoilerType( fieldValue )
        elif( field == KartDNA.fwwType ):
            self.setFrontWheelWellType( fieldValue )
        elif( field == KartDNA.bwwType ):
            self.setBackWheelWellType( fieldValue )
        elif( field == KartDNA.rimsType ):
            self.setRimType( fieldValue )
        elif( field == KartDNA.decalType ):
            self.setDecalType( fieldValue )
        else:
            pass

        self.updateFields.append( field )
        self.__update()
        

    def __applyBodyColor( self ):
        """
        """

        # If the bodyColor has not been set,  then apply the
        # default color (which has been designated as white).
        if( self.kartDNA[ KartDNA.bodyColor ] == InvalidEntry ):
            bodyColor = getDefaultColor()
        else:
            bodyColor = getAccessory( self.kartDNA[ KartDNA.bodyColor ] )

        for kart in self.geom:
            # Find the chasse node within the geometry
            kartBody = self.geom[ kart ].find( "**/chasse" )

            # Now apply the actual color to the geometry node
            kartBody.setColorScale( bodyColor )

    def __applyAccessoryColor( self ):
        """
        """

        # Set Decal Color
        if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
            accColor = getDefaultColor()
        else:
            accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )

        for kart in self.geom:
            # Handle Decals 
            hoodDecal = self.geom[kart].find( "**/hoodDecal" )
            rightSideDecal = self.geom[kart].find( "**/rightSideDecal" )
            leftSideDecal = self.geom[kart].find( "**/leftSideDecal" )
            hoodDecal.setColorScale( accColor )
            rightSideDecal.setColorScale( accColor )
            leftSideDecal.setColorScale( accColor )

        # Apply to engine block
        for type in [ KartDNA.ebType, KartDNA.spType ]:
            model = self.kartAccessories.get( type, None )
            if( model != None and not model.find( "**/vertex" ).isEmpty() ):
                if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
                    accColor = getDefaultColor()
                else:
                    accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )
                model.find( "**/vertex" ).setColorScale( accColor )
 
        for type in [ KartDNA.fwwType, KartDNA.bwwType ]:
            lModel, rModel = self.kartAccessories.get( type, ( None, None ) )
            if( lModel != None and not lModel.find( "**/vertex" ).isEmpty() ):
                if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
                    accColor = getDefaultColor()
                else:
                    accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )
                lModel.find( "**/vertex" ).setColorScale( accColor )
                rModel.find( "**/vertex" ).setColorScale( accColor )

    def __applyEngineBlock( self ):
        """
        """
        ebType = self.kartDNA[ KartDNA.ebType ]
        if( ebType == InvalidEntry ):
            return

        ebPath = getAccessory( ebType )
        attachNode = getAccessoryAttachNode( ebType )
        assert attachNode != None, "Kart::__applyEngineBlock - invalid attach node for accessory %s" % (ebType,)

        model = loader.loadModel( ebPath )
        self.kartAccessories[ KartDNA.ebType ] = model
        model.setScale( self.accGeomScale )

        if( not model.find( "**/vertex" ).isEmpty() ):
            if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
                accColor = getDefaultColor()
            else:
                accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )
   
            model.find( "**/vertex" ).setColorScale( accColor )

        for kart in self.geom:
            engineBlockNode = self.geom[kart].find( "**/%s" % ( attachNode ) )
            model.setPos( engineBlockNode.getPos( self.pitchNode[kart] ) )
            model.setHpr( engineBlockNode.getHpr( self.pitchNode[kart] ) )
            model.instanceTo(self.pitchNode[kart]) 
        
    def __applySpoiler( self ):
        """
        """
        spType = self.kartDNA[ KartDNA.spType ]
        if( spType == InvalidEntry ):
            return

        spPath = getAccessory( spType )
        attachNode = getAccessoryAttachNode( spType )
        assert attachNode != None, "Kart::__applySpoiler - invalid attach node for accessory %s" % (sbType,)

        model = loader.loadModel( spPath )
        self.kartAccessories[ KartDNA.spType ] = model
        model.setScale( self.accGeomScale )

        for kart in self.geom:
            spoilerNode = self.geom[kart].find( "**/%s" % ( attachNode ) )
            model.setPos( spoilerNode.getPos( self.pitchNode[kart] ) )
            model.setHpr( spoilerNode.getHpr( self.pitchNode[kart] ) )
            model.instanceTo(self.pitchNode[kart])

    def __applyRims( self ):
        """
        """
        
        # if the rim type has not been set, then apply the default
        # rims to the kart.
        if( self.kartDNA[ KartDNA.rimsType ] == InvalidEntry ):
            rimTexPath = getAccessory( getDefaultRim() )
        else:
            rimTexPath = getAccessory( self.kartDNA[ KartDNA.rimsType ] )

        rimTex = loader.loadTexture( "%s.jpg" % ( rimTexPath ), "%s_a.rgb" % ( rimTexPath ) )

        for kart in self.geom:
            # Obtain the Rim nodes from the geometry.   
            leftFrontWheelRim = self.geom[kart].find( "**/leftFrontWheelRim" )
            rightFrontWheelRim = self.geom[kart].find( "**/rightFrontWheelRim" )
            leftRearWheelRim = self.geom[kart].find( "**/leftRearWheelRim" )
            rightRearWheelRim = self.geom[kart].find( "**/rightRearWheelRim" )

            # set the mipmaps
            rimTex.setMinfilter(Texture.FTLinearMipmapLinear)

            # Now apply the actual rim to each of the rim nodes.
            leftFrontWheelRim.setTexture( rimTex, self.texCount )
            rightFrontWheelRim.setTexture( rimTex, self.texCount )
            leftRearWheelRim.setTexture( rimTex, self.texCount )
            rightRearWheelRim.setTexture( rimTex, self.texCount )

        self.texCount += 1

    def __applyFrontWheelWells( self ):
        """
        """

        fwwType = self.kartDNA[ KartDNA.fwwType ]
        if( fwwType == InvalidEntry ):
            return

        fwwPath = getAccessory( fwwType )
        attachNode = getAccessoryAttachNode( fwwType )
        assert attachNode != None, "Kart::__applyFrontWheelWeels - invalid attach node for accessory %s" %(fwwType,)

        leftAttachNode = attachNode % ( "left" )
        rightAttachNode = attachNode % ( "right" )

        # Add models to the dictionary, must use tuple because they are
        # mirrored on each side of the kart.
        leftModel = loader.loadModel( fwwPath )
        rightModel = loader.loadModel( fwwPath )
        self.kartAccessories[ KartDNA.fwwType ] = ( leftModel, rightModel )
   
        # Set the Accessory color
        if( not leftModel.find( "**/vertex" ).isEmpty() ):
            if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
                accColor = getDefaultColor()
            else:
                accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )
            leftModel.find( "**/vertex" ).setColorScale( accColor )
            rightModel.find( "**/vertex" ).setColorScale( accColor )
   
        #leftModel = {}
        #rightModel = {}
        for kart in self.geom:
            #leftModel[kart] = loader.loadModel( fwwPath )
            #rightModel[kart] = loader.loadModel( fwwPath )
            leftNode = self.geom[kart].find( "**/%s"  % ( leftAttachNode ) )
            rightNode = self.geom[kart].find( "**/%s" % ( rightAttachNode ) )
            
            
            leftNodePath = leftModel.instanceTo( self.pitchNode[ kart ] )
            leftNodePath.setPos( rightNode.getPos( self.pitchNode[ kart ] ) )
            leftNodePath.setHpr( rightNode.getHpr( self.pitchNode[ kart ] ) )
            leftNodePath.setScale( self.accGeomScale )
            
            # Negate the scaling of the accessory in the x direction and set
            # the geometry to two-sided to make it symmetrical.
            leftNodePath.setSx( -1.0 * leftNodePath.getSx() )
            leftNodePath.setTwoSided( True )
 
            rightNodePath = rightModel.instanceTo( self.pitchNode[ kart ] )
            rightNodePath.setPos( leftNode.getPos( self.pitchNode[ kart ] ) )
            rightNodePath.setHpr( leftNode.getHpr( self.pitchNode[ kart ] ) )
            rightNodePath.setScale( self.accGeomScale )
            
            #leftModel[kart].reparentTo( self.pitchNode[kart] )
            #leftModel[kart].setPos( rightNode.getPos( self.pitchNode[kart] ) )
            #leftModel[kart].setHpr( rightNode.getHpr( self.pitchNode[kart] ) )
            #leftModel[kart].setScale( self.accGeomScale  )             
            
            # Negate the Scaling of the Accessory in the x direction and
            # set the geometry to two-sided to make it symmetrical.
            
            #leftModel[kart].setScale( -1.0 * leftModel.getSx() )
            #leftModel[kart].setTwoSided( True )
            
            
            #rightModel[kart].reparentTo( self.pitchNode[kart] )
            #rightModel[kart].setPos( leftNode.getPos( self.pitchNode[kart] ) )
            #rightModel[kart].setHpr( leftNode.getHpr( self.pitchNode[kart] ) )
            #rightModel[kart].setScale( self.accGeomScale )

    def __applyBackWheelWells( self ):
        """
        """

        bwwType = self.kartDNA[ KartDNA.bwwType ]
        if( bwwType == InvalidEntry ):
            return

        bwwPath = getAccessory( bwwType )
        attachNode = getAccessoryAttachNode( bwwType )
        assert attachNode != None, "Kart::__applyBackWheelWells - invalid attach node for accessory %s" % (bwwType,)

        leftAttachNode = attachNode % ( "left" )
        rightAttachNode = attachNode % ( "right" )

        # Add models to the dictionary, must use tuple because they are
        # mirrored on each side of the kart.
        leftModel = loader.loadModel( bwwPath )
        rightModel = loader.loadModel( bwwPath )
        self.kartAccessories[ KartDNA.bwwType ] = ( leftModel, rightModel )
   
        # Set the Accessory color
        if( not leftModel.find( "**/vertex" ).isEmpty() ):
            if( self.kartDNA[ KartDNA.accColor ] == InvalidEntry ):
                accColor = getDefaultColor()
            else:
                accColor = getAccessory( self.kartDNA[ KartDNA.accColor ] )
            leftModel.find( "**/vertex" ).setColorScale( accColor )
            rightModel.find( "**/vertex" ).setColorScale( accColor )
  
        #leftModele = {}
        #rightModel = {}
        for kart in self.geom:
            leftNode = self.geom[kart].find( "**/%s" % ( leftAttachNode ) )
            rightNode = self.geom[kart].find( "**/%s" % ( rightAttachNode ) )
            #leftModel[kart] = loader.loadModel( bwwPath )
            #rightModel[kart] = loader.loadModel( bwwPath )
 
            leftNodePath = leftModel.instanceTo( self.pitchNode[ kart ] )
            leftNodePath.setPos( rightNode.getPos( self.pitchNode[ kart ] ) )
            leftNodePath.setHpr( rightNode.getHpr( self.pitchNode[ kart ] ) )
            leftNodePath.setScale( self.accGeomScale )
            
            # Negate the scaling of the accessory in the x direction and set
            # the geometry to two-sided to make it symmetrical.
            leftNodePath.setSx( -1.0 * leftNodePath.getSx() )
            leftNodePath.setTwoSided( True )
            
            rightNodePath = rightModel.instanceTo( self.pitchNode[ kart ] )
            rightNodePath.setPos( leftNode.getPos( self.pitchNode[ kart ] ) )
            rightNodePath.setHpr( leftNode.getHpr( self.pitchNode[ kart ] ) )
            rightNodePath.setScale( self.accGeomScale )
   
            # Handle Models
            #leftModel[kart].reparentTo( self.pitchNode[kart] )
            #leftModel[kart].setPos( rightNode.getPos( self.pitchNode[kart] ) )
            #leftModel[kart].setHpr( rightNode.getHpr( self.pitchNode[kart] ) )
            #leftModel[kart].setScale( self.accGeomScale )
            
            #rightModel[kart].reparentTo( self.pitchNode[kart] )
            #rightModel[kart].setPos( leftNode.getPos( self.pitchNode[kart] ) )
            #rightModel[kart].setHpr( leftNode.getHpr( self.pitchNode[kart] ) )
            #rightModel[kart].setScale( self.accGeomScale )

    def __applyDecals( self ):
        """
        """

        if( self.kartDNA[ KartDNA.decalType ] != InvalidEntry ):
            decalId = getAccessory( self.kartDNA[ KartDNA.decalType ] )
            kartDecal = getDecalId( self.kartDNA[ KartDNA.bodyType ]  )

            hoodDecalTex = loader.loadTexture( "phase_6/maps/%s_HoodDecal_%s.jpg" % ( kartDecal, decalId ),
                                               "phase_6/maps/%s_HoodDecal_%s_a.rgb" % ( kartDecal, decalId ) )
            sideDecalTex = loader.loadTexture( "phase_6/maps/%s_SideDecal_%s.jpg" % ( kartDecal, decalId ),
                                               "phase_6/maps/%s_SideDecal_%s_a.rgb" % ( kartDecal, decalId ) )

            # set the mipmaps
            hoodDecalTex.setMinfilter(Texture.FTLinearMipmapLinear)
            sideDecalTex.setMinfilter(Texture.FTLinearMipmapLinear)

            for kart in self.geom:
                # Obtain the hood nodes from the geometry 
                hoodDecal = self.geom[kart].find( "**/hoodDecal" )
                rightSideDecal = self.geom[kart].find( "**/rightSideDecal" )
                leftSideDecal = self.geom[kart].find( "**/leftSideDecal" )
                
                hoodDecal.setTexture( hoodDecalTex, self.texCount )
                rightSideDecal.setTexture( sideDecalTex, self.texCount )
                leftSideDecal.setTexture( sideDecalTex, self.texCount )

                hoodDecal.show()
                rightSideDecal.show()
                leftSideDecal.show()
        else:
            for kart in self.geom:
                # Obtain the hood nodes from the geometry 
                hoodDecal = self.geom[kart].find( "**/hoodDecal" )
                rightSideDecal = self.geom[kart].find( "**/rightSideDecal" )
                leftSideDecal = self.geom[kart].find( "**/leftSideDecal" )
                
                hoodDecal.hide()
                rightSideDecal.hide()
                leftSideDecal.hide()

        self.texCount += 1        

    def rollSuspension(self, roll):
        for kart in self.pitchNode:
            self.pitchNode[kart].setR(roll)

        
    def pitchSuspension(self, pitch):
        for kart in self.pitchNode:
            self.pitchNode[kart].setP(pitch)

    def getDNA( self ):
        """
        Purpose: The getDNA Method retrieves the Kart instance's
        current DNA.
        
        Params: None
        Return: [] - List of DNA Values
        """
        return self.kartDNA

    def setDNA( self, dna ):
        """
        Purpose: The setDNA Method sets the Kart DNA for this object
        and generates the appropriate models.

        Params: dna - a tuple consisting of the kart DNA
        return: None
        """

        # Check the validity of the DNA. Also, check that there is a
        # valid kart body.
        assert checkKartDNAValidity(dna), "Kart::setDNA - INVALID DNA %s" % (dna,)

        if( self.kartDNA != [ -1 ] * getNumFields() ):
            for field in xrange( len( self.kartDNA ) ):
                if( dna[ field ] != self.kartDNA[ field ] ):
                    self.updateDNAField( field, dna[ field ] )
            return

        # The DNA passed the validity check, thus set it accordingly.
        self.kartDNA = dna

    def setBodyType( self, bodyType ):
        """
        Purpose: The setBodyType Method sets the local AI side
        body type of the kart that the toon currently owns.
        
        
        Params: bodyType - the body type of the kart which the toon
        currently owns.
        Return: None
        """
        self.kartDNA[ KartDNA.bodyType ] = bodyType

    def getBodyType( self ):
        """
        Purpose: The getBodyType Method obtains the local client side
        body type of the kart that the toon currently owns.
        
        Params: None
        Return: bodyType - the body type of the kart.
        """
        return self.kartDNA[ KartDNA.bodyType ]

    def setBodyColor( self, bodyColor ):
        """
        Purpose: The setBodyColor Method appropriately sets
        the body color of the lient on the ai side by updating the
        local kart dna.
        
        Params: bodyColor - the color of the kart body.
        Return: None
        """
        self.kartDNA[ KartDNA.bodyColor ] = bodyColor

    def getBodyColor( self ):
        """
        Purpose: The getBodyColor Method obtains the current
        body color of the kart.
        
        Params: None
        Return: bodyColor - the color of the kart body.
        """
        return self.kartDNA[ KartDNA.bodyColor ]

    def setAccessoryColor( self, accColor ):
        """
        Purpose: The setAccessoryColor Method appropriately sets
        the accessory color of the local ai side by updating the kart
        dna.

        Params: accColor - the color of the accessories.
        Return: None
        """
        self.kartDNA[ KartDNA.accColor ] = accColor

    def getAccessoryColor( self ):
        """
        Purpose: The getAccessoryColor Method obtains the
        accessory color for the kart.
        
        Params: None
        Return: accColor - the color of the accessories
        """
        return self.kartDNA[ KartDNA.accColor ]

    def setEngineBlockType( self, ebType ):
        """
        Purpose: The setEngineBlockType Method sets the engine
        block type accessory for the kart by updating the Kart DNA.
        
        Params: ebType - the type of engine block accessory.
        Return: None
        """
        self.kartDNA[ KartDNA.ebType ] = ebType

    def getEngineBlockType( self ):
        """
        Purpose: The getEngineBlockType Method obtains the engine
        block type accessory for the kart by accessing the
        current Kart DNA.
        
        Params: None
        Return: ebType - the type of engine block accessory.
        """
        return self.kartDNA[ KartDNA.ebType ]

    def setSpoilerType( self, spType ):
        """
        Purpose: The setSpoilerType Method sets the spoiler
        type accessory for the kart by updating the Kart DNA.
        
        Params: spType - the type of spoiler accessory
        Return: None
        """
        self.kartDNA[ KartDNA.spType ] = spType

    def getSpoilerType( self ):
        """
        Purpose: The getSpoilerType Method obtains the spoiler
        type accessory for the kart by accessing the current Kart DNA.
        
        Params: None
        Return: spType - the type of spoiler accessory 
        """
        return self.kartDNA[ KartDNA.spType ]

    def setFrontWheelWellType( self, fwwType ):
        """
        Purpose: The setFrontWheelWellType Method sets the
        front wheel well accessory for the kart updating the
        Kart DNA.
        
        Params: fwwType - the type of Front Wheel Well accessory
        Return: None
        """
        self.kartDNA[ KartDNA.fwwType ] = fwwType

    def getFrontWheelWellType( self ):
        """
        Purpose: The getFrontWheelWellType Method obtains the
        front wheel well accessory for the kart accessing the
        Kart DNA.
        
        Params: None
        Return: fwwType - the type of Front Wheel Well accessory
        """
        return self.kartDNA[ KartDNA.fwwType ]

    def setBackWheelWellType( self, bwwType ):
        """
        Purpose: The setWheelWellType Method sets the Back
        Wheel Wheel accessory for the kart by updating the Kart DNA.
        
        Params: bwwType - the type of Back Wheel Well accessory.
        Return: None
        """
        self.kartDNA[ KartDNA.bwwType ] = bwwType

    def getBackWheelWellType( self ):
        """
        Purpose: The getWheelWellType Method gets the Back
        Wheel Wheel accessory for the kart by updating the Kart DNA.
        
        Params: bwwType - the type of Back Wheel Well accessory.
        Return: None
        """
        return self.kartDNA[ KartDNA.bwwType ]

    def setRimType( self, rimsType ):
        """
        Purpose: The setRimType Method sets the rims accessory
        for the karts tires by updating the Kart DNA.
        
        Params: rimsType - the type of rims for the kart tires.
        Return: None
        """
        self.kartDNA[ KartDNA.rimsType ] = rimsType

    def getRimType( self ):
        """
        Purpose: The setRimType Method gets the rims accessory
        for the karts tires by accessing the Kart DNA.
        
        Params: None
        Return: rimsType - the type of rims for the kart tires.
        """
        return self.kartDNA[ KartDNA.rimsType ]

    def setDecalType( self, decalType ):
        """
        Purpose: The setDecalType Method sets the decal
        accessory of the kart by updating the Kart DNA.
        
        Params: decalType - the type of decal set for the kart.
        Return: None
        """
        self.kartDNA[ KartDNA.decalType ] = decalType

    def getDecalType( self ):
        """
        Purpose: The getDecalType Method obtains the decal
        accessory of the kart by accessing the Kart DNA.
        
        Params: None
        Return: decalType - the type of decal set for the kart.
        """
        return self.kartDNA[ KartDNA.decalType ]
        
    def getGeomNode(self):
       return self.geom[0]


    def spinWheels(self, amount):
        newSpin = (self.oldSpinAmount + amount) % 360

        for wheelNode in self.wheelCenters:
            wheelNode.setP(newSpin)
            
        self.oldSpinAmount = newSpin
        
    def setWheelSpinSpeed(self, speed):
        pass
    
    def __startWheelSpin(self):
        self.oldSpinAmount = 0
    
    def __stopWheelSpin(self):
        pass
    
    def turnWheels(self, amount):
        amount += self.wheelBaseH
        node = self.wheelCenters[self.RFWHEEL]
        node.setH(amount)
        
        node = self.wheelCenters[self.LFWHEEL]
        node.setH(amount)
        

    def generateEngineStartTrack(self):
        length = self.kartStartSfx.length()
        def printVol():
            print self.kartLoopSfx.getVolume()
            
        track = Parallel(
            SoundInterval(self.kartStartSfx),
            Func(self.kartLoopSfx.play),
            LerpFunctionInterval(self.kartLoopSfx.setVolume, fromData = 0, toData = 0.4, duration = length),
            )


        return Sequence(track,Func(printVol))
                            
    def generateEngineStopTrack(self, duration = 0):
        track = Parallel(
            LerpFunctionInterval(self.kartLoopSfx.setVolume, fromData = 0.4, toData = 0, duration = duration),
            )
        return track
