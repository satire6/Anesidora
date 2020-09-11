#ifndef _Cars_hsv2rgbNode
#define _Cars_hsv2rgbNode
//
// Copyright (C) Disney VR Studio 
// 
// Author: Gyedo Jeon
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

 
class Cars_hsv2rgb : public MPxNode
{
public:
						Cars_hsv2rgb();
	virtual				~Cars_hsv2rgb(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual void		postConstructor();

	static  void*		creator();
	static  MStatus		initialize();

public:

	// cars_hsv2rgb input attr
	static MObject	aInSv;

    static MObject  aInH;

	// cars_hsv2rgb output attr
    static MObject  aOutRgb;

	// The typeid is a unique 32bit indentifier that describes this node.
	// It is used to save and retrieve nodes of this type from the binary
	// file format.  If it is not unique, it will cause file IO problems.
	//
	static	MTypeId		id;
};

#endif
