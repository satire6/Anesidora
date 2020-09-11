//
// Copyright (C) Disney VR Studio 
// 
// Author: Gyedo Jeon
//

#include "Cars_hsv2rgbNode.h"

#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MFloatVector.h>
#include <maya/MGlobal.h>
#include <math.h>

// Local functions
void RGBtoHSV( float r, float g, float b, float *h, float *s, float *v );
void HSVtoRGB( float *r, float *g, float *b, float h, float s, float v );

// this id should be unique
MTypeId     Cars_hsv2rgb::id( 0x00000000 );

void Cars_hsv2rgb::postConstructor( )
{
	setMPSafe(true);
}

// Class attributes
// 
MObject Cars_hsv2rgb::aInSv;
MObject Cars_hsv2rgb::aInH;
MObject Cars_hsv2rgb::aOutRgb;

#define MAKE_INPUT(attr)						\
    CHECK_MSTATUS(attr.setKeyable(true));  		\
	CHECK_MSTATUS(attr.setStorable(true));		\
    CHECK_MSTATUS(attr.setReadable(true)); 		\
	CHECK_MSTATUS(attr.setWritable(true));

#define MAKE_OUTPUT(attr)						\
    CHECK_MSTATUS(attr.setKeyable(false)); 		\
	CHECK_MSTATUS(attr.setStorable(false));		\
    CHECK_MSTATUS(attr.setReadable(true)); 		\
	CHECK_MSTATUS(attr.setWritable(false));


Cars_hsv2rgb::Cars_hsv2rgb() {}
Cars_hsv2rgb::~Cars_hsv2rgb() {}

MStatus Cars_hsv2rgb::compute( const MPlug& plug, MDataBlock& data )
//
//	Description:
//		This method computes the value of the given output plug based
//		on the values of the input attributes.
//
//	Arguments:
//		plug - the plug to compute
//		data - object that provides access to the attributes for this node
//
{
	// outColor or individial R, G, B channel
    if((plug != aOutRgb) && (plug.parent() != aOutRgb))
		return MS::kUnknownParameter;

    MFloatVector resultColor;
    MFloatVector & inSv = data.inputValue(aInSv).asFloatVector();
    MFloatVector & inH = data.inputValue(aInH).asFloatVector();

	float r;
	float g;
	float b;

	float h;
	float s;
	float v;

	// convert inH RGB to HSV to get input H
	RGBtoHSV(inH.x, inH.y, inH.z, &h, &s, &v);
	
	// get input S from inversed inSv's R
	s = 1 - inSv.x;
	
	// get input V from inSv's B
	v = inSv.z;

	HSVtoRGB(&r, &g, &b, h, s, v);
    resultColor[0] = r;
    resultColor[1] = g;
    resultColor[2] = b;

	// set ouput color attribute
    MDataHandle outColorHandle = data.outputValue( aOutRgb );
    MFloatVector& outColor = outColorHandle.asFloatVector();
    outColor = resultColor;
    outColorHandle.setClean();

    return MS::kSuccess;
}

void* Cars_hsv2rgb::creator()
//
//	Description:
//		this method exists to give Maya a way to create new objects
//      of this type. 
//
//	Return Value:
//		a new object of this type
//
{
	return new Cars_hsv2rgb();
}

MStatus Cars_hsv2rgb::initialize()
//
//	Description:
//		This method is called to create and initialize all of the attributes
//      and attribute dependencies for this node type.  This is only called 
//		once when the node type is registered with Maya.
//
//	Return Values:
//		MS::kSuccess
//		MS::kFailure
//		
{
    MFnNumericAttribute    nAttr; 

    // Create input attributes

	aInSv = nAttr.createColor("inSv", "isv");
	MAKE_INPUT(nAttr);

	aInH = nAttr.createColor("inH", "ih");
	MAKE_INPUT(nAttr);

	// Create output attributes
    aOutRgb = nAttr.createColor("outRgb", "o");
	MAKE_OUTPUT(nAttr);

    /* Plug inputs and outputs
    ---------------------------*/
    CHECK_MSTATUS(addAttribute(aInSv));
    CHECK_MSTATUS(addAttribute(aInH));
    CHECK_MSTATUS(addAttribute(aOutRgb));

    /* Build dependancies
    ----------------------*/
    CHECK_MSTATUS(attributeAffects(aInSv,    aOutRgb));
    CHECK_MSTATUS(attributeAffects(aInH, aOutRgb));

    return MS::kSuccess;
}

// r,g,b values are from 0 to 1
// h = [0,360], s = [0,1], v = [0,1]
//		if s == 0, then h = -1 (undefined)
void RGBtoHSV( float r, float g, float b, float *h, float *s, float *v )
{
	float min, max, delta;
	if (r > g)
	{
		if (g > b)
		{
			max = r;
			min = b;
		}
		else // b > g
		{
			if (r > b)
			{
				max = r;
				min = g;
			}
			else // b > r
			{
				max = b;
				min = g;
			}
		}
	}
	else // g > r
	{
		if (g > b)
		{
			max = g;
			if (r > b)
			{
				min = b;
			}
			else // b > r
			{
				min = r;
			}
		}
		else // b > g
		{
			max = b;
			min = r;
		}
	}

	*v = max;				// v
	delta = max - min;
	if( max != 0 )
		*s = delta / max;		// s
	else {
		// r = g = b = 0		// s = 0, v is undefined
		*s = 0;
		*h = -1;
		return;
	}
	if( r == max )
		*h = ( g - b ) / delta;		// between yellow & magenta
	else if( g == max )
		*h = 2 + ( b - r ) / delta;	// between cyan & yellow
	else
		*h = 4 + ( r - g ) / delta;	// between magenta & cyan
	*h *= 60;				// degrees
	if( *h < 0 )
		*h += 360;
}

void HSVtoRGB( float *r, float *g, float *b, float h, float s, float v )
{
	int i;
	float f, p, q, t;
	if( s == 0 ) {
		// achromatic (grey)
		*r = *g = *b = v;
		return;
	}
	h /= 60;			// sector 0 to 5
	i = floor( h );
	f = h - i;			// factorial part of h
	p = v * ( 1 - s );
	q = v * ( 1 - s * f );
	t = v * ( 1 - s * ( 1 - f ) );
	switch( i ) {
		case 0:
			*r = v;
			*g = t;
			*b = p;
			break;
		case 1:
			*r = q;
			*g = v;
			*b = p;
			break;
		case 2:
			*r = p;
			*g = v;
			*b = t;
			break;
		case 3:
			*r = p;
			*g = q;
			*b = v;
			break;
		case 4:
			*r = t;
			*g = p;
			*b = v;
			break;
		default:		// case 5:
			*r = v;
			*g = p;
			*b = q;
			break;
	}
}