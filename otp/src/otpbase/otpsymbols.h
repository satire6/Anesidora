// Filename: otpsymbols.h
// Created by:  drose (18Feb00)
/////////////////////////////////////////////

#ifndef OTPSYMBOLS_H
#define OTPSYMBOLS_H

/* See dtoolsymbols.h for a rant on the purpose of this file.  */

#if defined(WIN32_VC) && !defined(CPPPARSER)

#ifdef BUILDING_OTP
  #define EXPCL_OTP __declspec(dllexport)
  #define EXPTP_OTP
#else
  #define EXPCL_OTP __declspec(dllimport)
  #define EXPTP_OTP extern
#endif

#else   /* !WIN32_VC */

#define EXPCL_OTP
#define EXPTP_OTP

#endif  /* WIN32_VC */

#endif
