// Filename: toontownsymbols.h
// Created by:  drose (18Feb00)
/////////////////////////////////////////////

#ifndef TOONTOWNSYMBOLS_H
#define TOONTOWNSYMBOLS_H

/* See dtoolsymbols.h for a rant on the purpose of this file.  */

#if defined(WIN32_VC) && !defined(CPPPARSER)

#ifdef BUILDING_TOONTOWN
  #define EXPCL_TOONTOWN __declspec(dllexport)
  #define EXPTP_TOONTOWN
#else
  #define EXPCL_TOONTOWN __declspec(dllimport)
  #define EXPTP_TOONTOWN extern
#endif

#else   /* !WIN32_VC */

#define EXPCL_TOONTOWN
#define EXPTP_TOONTOWN

#endif  /* WIN32_VC */

#endif
