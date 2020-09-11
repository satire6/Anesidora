// Filename: chatFlags.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef CHATFLAGS_H
#define CHATFLAGS_H

#include "otpbase.h"

BEGIN_PUBLISH
////////////////////////////////////////////////////////////////////
//        Enum : ChatFlags
// Description : This enumerated type defines the bits associated with
//               the kinds of chat messages we may have.
////////////////////////////////////////////////////////////////////
enum ChatFlags {
  CF_speech         = 0x0001,
  CF_thought        = 0x0002,
  CF_quicktalker    = 0x0004,
  CF_timeout        = 0x0008,
  CF_page_button    = 0x0010,
  CF_quit_button    = 0x0020,
  CF_reversed       = 0x0040,
  CF_snd_openchat   = 0x0080,
  CF_no_quit_button = 0x0100,
};
END_PUBLISH

#endif
