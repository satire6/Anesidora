// Filename: loadClientCertificate.h
// Created by:  drose (17Sep03)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) 2001 - 2004, Disney Enterprises, Inc.  All rights reserved
//
// All use of this software is subject to the terms of the Panda 3d
// Software license.  You should have received a copy of this license
// along with this source code; you will also find a current copy of
// the license at http://etc.cmu.edu/panda3d/docs/license/ .
//
// To contact the maintainers of this program write to
// panda3d-general@lists.sourceforge.net .
//
////////////////////////////////////////////////////////////////////

#ifndef LOADCLIENTCERTIFICATE_H
#define LOADCLIENTCERTIFICATE_H

#include "otpbase.h"

class HTTPClient;

BEGIN_PUBLISH

// This function loads the (encrypted) client certificate into the
// indicated HTTPClient.  It should be called something like
// load_client_certificate(), but that name would then be visible to a
// hacker scanning the Python code, so we call it something
// misleading just to make it a teeny bit harder to find.

void prepare_avatar(HTTPClient *http);

END_PUBLISH

#endif
