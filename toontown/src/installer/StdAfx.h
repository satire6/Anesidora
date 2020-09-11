// Filename: StdAfx.h
// Created by:
//
////////////////////////////////////////////////////////////////////
#pragma once

#if !defined(AFX_STDAFX_H__E31F5D7F_A1F7_45CE_815D_EBA2391DAD0B__INCLUDED_)
#define AFX_STDAFX_H__E31F5D7F_A1F7_45CE_815D_EBA2391DAD0B__INCLUDED_

#if _MSC_VER >= 1300

// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently,
// but are changed infrequently

#ifndef STRICT
#define STRICT
#endif

// ignore pragma packing specs warnings in atlbase.h, winnt.h
#pragma warning(disable: 4103)

// Modify the following defines if you have to target a platform prior to the ones specified below.
// Refer to MSDN for the latest info on corresponding values for different platforms.

#ifndef WINVER              // Allow use of features specific to Windows 95 and Windows NT 4 or later.
#define WINVER 0x0400       // Change this to the appropriate value to target Windows 98 and Windows 2000 or later.
#endif

#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0500 // Allow use of features specific to Windows 2000 or later
#endif

#ifndef _WIN32_WINDOWS      // Allow use of features specific to Windows 98 or later.
#define _WIN32_WINDOWS 0x0410 // Change this to the appropriate value to target Windows Me or later.
#endif

#ifndef _WIN32_IE           // Allow use of features specific to IE 4.0 or later.
#define _WIN32_IE 0x0400    // Change this to the appropriate value to target IE 5.0 or later.
#endif

#define _ATL_APARTMENT_THREADED
#define _ATL_NO_AUTOMATIC_NAMESPACE

#define _ATL_CSTRING_EXPLICIT_CONSTRUCTORS  // some CString constructors will be explicit

// turns off ATL's hiding of some common and often safely ignored warning messages
#define _ATL_ALL_WARNINGS

#include <atlbase.h>
#include <atlcom.h>
#include <atlwin.h>
#include <atltypes.h>
#include <atlctl.h>
#include <atlhost.h>

using namespace ATL;

#else
// disable "C++ exception handler used, but unwind semantics are not enabled. Specify -GX"
#pragma warning( disable: 4530 )

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#define STRICT
#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0400
#endif
#define _ATL_APARTMENT_THREADED

#include <atlbase.h>
//You may derive a class from CComModule and use it if you want to override
//something, but do not change the name of _Module
extern CComModule _Module;
#include <atlcom.h>

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif
#endif // !defined(AFX_STDAFX_H__E31F5D7F_A1F7_45CE_815D_EBA2391DAD0B__INCLUDED)
