//
// Copyright (C) Disney VR Studio 
// 
// Author: Gyedo Jeon
//

#include "Cars_hsv2rgbNode.h"

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

MStatus initializePlugin( MObject obj )
//
//	Description:
//		this method is called when the plug-in is loaded into Maya.  It 
//		registers all of the services that this plug-in provides with 
//		Maya.
//
//	Arguments:
//		obj - a handle to the plug-in object (use MFnPlugin to access it)
//
{ 
	const MString UserClassify( "utility/color" );
	MString command( "if( `window -exists createRenderNodeWindow` )  {refreshCreateRenderNodeWindow(\"" );

	MFnPlugin plugin( obj, "Disney VR Studio", "1.0", "Any");
	plugin.registerNode( "cars_hsv2rgb", Cars_hsv2rgb::id, 
                         Cars_hsv2rgb::creator, Cars_hsv2rgb::initialize,
                         MPxNode::kDependNode, &UserClassify );
	command += UserClassify;
	command += "\");}\n";

	MGlobal::executeCommand(command);
	
	return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj)
//
//	Description:
//		this method is called when the plug-in is unloaded from Maya. It 
//		deregisters all of the services that it was providing.
//
//	Arguments:
//		obj - a handle to the plug-in object (use MFnPlugin to access it)
//
{
	MStatus   status;
	const MString UserClassify( "utility/color" );
	MString command( "if( `window -exists createRenderNodeWindow` )  {refreshCreateRenderNodeWindow(\"" );

	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( Cars_hsv2rgb::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	command += UserClassify;
	command += "\");}\n";

	MGlobal::executeCommand(command);

	return status;
}
