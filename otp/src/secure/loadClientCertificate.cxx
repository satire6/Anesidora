// Filename: loadClientCertificate.cxx
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

#include "loadClientCertificate.h"
#include "httpClient.h"
#include "zStream.h"

// This file defines the actual binary data for the compressed,
// encrypted certificate.
#include "clientCertificate_src.cxx"

void
prepare_avatar(HTTPClient *http) {
  // First, decompress the certificate pair.
  string cert_pz((const char *)client_cert, (size_t)client_cert_len);
  istringstream cert_pz_strm(cert_pz);

  IDecompressStream decompr(&cert_pz_strm, false);
  string cert;

  static const int buffer_size = 1024;
  char buffer[buffer_size];

  decompr.read(buffer, buffer_size);
  size_t count = decompr.gcount();
  while (count != 0) {
    cert += string(buffer, count);
    decompr.read(buffer, buffer_size);
    count = decompr.gcount();
  }

#ifdef HAVE_OPENSSL
  // Now set the decompressed certificate pair (it's still
  // password-encrypted) on the HTTPClient.  The Python code will
  // separately set the decryption passphrase.
  http->set_client_certificate_pem(cert);
#endif  // HAVE_OPENSSL
}
