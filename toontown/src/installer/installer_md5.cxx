// Filename: installer_md5.cxx
// Created by:  darren (09Nov00)
// $Id$
////////////////////////////////////////////////////////////////////

#include "pragma.h"

#include "installer_md5.h"

#include <iostream>
#include <fstream>
#include <sstream>

#include <string>

#include "openssl/md5.h"

using namespace std;

void
md5_a_file(const char *fname, MD5HashVal &ret) {
  ifstream in(fname, ios::in | ios::binary);

  unsigned char md[16];

  MD5_CTX ctx;
  MD5_Init(&ctx);

  static const int buffer_size = 1024;
  char buffer[buffer_size];

  in.read(buffer, buffer_size);
  size_t count = in.gcount();
  while (count != 0) {
    MD5_Update(&ctx, buffer, count);
    in.read(buffer, buffer_size);
    count = in.gcount();
  }

  MD5_Final(md, &ctx);

  // Store the individual bytes as big-endian ints, from historical
  // convention.
  ret[0] = (md[0] << 24) | (md[1] << 16) | (md[2] << 8) | (md[3]);
  ret[1] = (md[4] << 24) | (md[5] << 16) | (md[6] << 8) | (md[7]);
  ret[2] = (md[8] << 24) | (md[9] << 16) | (md[10] << 8) | (md[11]);
  ret[3] = (md[12] << 24) | (md[13] << 16) | (md[14] << 8) | (md[15]);
}
