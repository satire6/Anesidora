// Filename: get_fingerprint.h
// Created by:  drose (19May10)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#ifndef GET_FINGERPRINT_H
#define GET_FINGERPRINT_H

#include "otpbase.h"

BEGIN_PUBLISH

// This function returns a string that should be unique to each
// computer (currently, it returns the MAC address).  As with
// loadClientCertificate, it should be named get_fingerprint(), but we
// call it something misleading instead to distract curious
// code-browsers.

string preload_cache();

END_PUBLISH

#endif
