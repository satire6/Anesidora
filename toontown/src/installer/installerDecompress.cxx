// Filename: installerDecompress.cxx
// Created by:  darren (18Jan01)
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"

#include "installerDecompress.h"
#include "log.h"

#include <zlib.h>

#define BUF_SIZE (16*1024)

int decompressFile(const char *filename) {
  z_stream zlibState;

  char *inBuf  = NULL;
  char *outBuf = NULL;

  inBuf  = new char[BUF_SIZE];
  if (NULL == inBuf) goto _error;
  outBuf = new char[BUF_SIZE];
  if (NULL == outBuf) goto _error;

  zlibState.opaque = Z_NULL;

  delete[] inBuf;
  delete[] outBuf;
  return 0;

_error:
  if (inBuf)  delete[] inBuf;
  if (outBuf) delete[] outBuf;
  return 1;
}
