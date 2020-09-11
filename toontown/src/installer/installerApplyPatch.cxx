// Filename: installerApplyPatch.cxx
// Created by:  darren (03Jan01)
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"

#include "installerApplyPatch.h"
#include "log.h"

typedef unsigned long  AP_uint32;
typedef signed   long  AP_int32;
typedef unsigned short AP_uint16;
typedef signed   short AP_int16;
typedef unsigned char  AP_uint8;

#define BUFFER_LENGTH (8*1024)

#define V0_MAGIC_NUMBER  0xfeebfaab
#define MAGIC_NUMBER  0xfeebfaac

////////////////////////////////////////////////////////////////////
/// THESE FUNCTIONS ARE ENDIAN-DEPENDENT
static void readUint32(ifstream &readStream, AP_uint32 &dest) {
  readStream.read((char*)&dest, sizeof(AP_uint32));
}

static void readInt32(ifstream &readStream, AP_int32 &dest) {
  readStream.read((char*)&dest, sizeof(AP_int32));
}

static void readUint16(ifstream &readStream, AP_uint16 &dest) {
  readStream.read((char*)&dest, sizeof(AP_uint16));
}

static void readInt16(ifstream &readStream, AP_int16 &dest) {
  readStream.read((char*)&dest, sizeof(AP_int16));
}
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: apply_patch
//       Access: Public
//  Description: Apply the patch to the file (original
//     file and patch are destroyed in the process).
//     returns 0 on success
// THIS IS A REPRODUCTION OF THE FUNCTIONALITY OF THREE MEMBER
// FUNCTIONS OF Patchfile (from $PANDA/express):
// initiate(), run(), and apply()
////////////////////////////////////////////////////////////////////
int apply_patch(const char *patchFileName, const char *fileName) {
  const int _header_length = sizeof(AP_uint32) + sizeof(AP_uint32) + sizeof(AP_int32);
  char tempFileName[_MAX_PATH];
  ifstream patchFileReadStream;
  ifstream origFileReadStream;
  ofstream tempFileWriteStream;
  AP_uint8 *buffer;

  // not sure what this buffer is, but will find out soon
  buffer = (AP_uint8*)malloc(BUFFER_LENGTH);
  if (NULL == buffer) {
    errorLog << "applyPatch(): Failed to allocate buffer" << endl;
    return -1;
  }

  // Open the patch file for read
  patchFileReadStream.open(patchFileName, ios::in | ios::binary);
  if (patchFileReadStream.fail()) {
    errorLog << "applyPatch(): Failed to open patch file: " << patchFileName << endl;
    return -1;
  }

  // Open the original file for read
  origFileReadStream.open(fileName, ios::in | ios::binary);
  if (patchFileReadStream.fail()) {
    errorLog << "applyPatch(): Failed to open original file: " << fileName << endl;
    return -1;
  }

  // Create a temp file name
  {
    char *tempname = _tempnam(".", "pf");
    if (NULL == tempname) {
      errorLog << "applyPatch(): Failed to create temp file name, using default" << endl;
      strcpy(tempFileName, "patcher_temp_file");
    } else {
      strcpy(tempFileName, tempname);
      //      errorLog << "applyPatch(): created temp file " << tempFileName << endl;
      free(tempname);
    }
  }

  // Open the temp file for write
  tempFileWriteStream.open(tempFileName, ios::out | ios::binary);
  if (tempFileWriteStream.fail()) {
    errorLog << "applyPatch(): Failed to open output file: " << tempFileName << endl;
    return -1;
  }

  /////////////
  // read header, make sure the patch file is valid

  // check the magic number
  AP_uint32 magic_number;
  readUint32(patchFileReadStream, magic_number);
  if (magic_number != MAGIC_NUMBER && magic_number != V0_MAGIC_NUMBER) {
    errorLog << "applyPatch(): invalid patch file: " << patchFileName << endl;
    return -1;
  }
  //  errorLog << "applyPatch: magic number " << magic_number << endl;

  AP_uint16 version_number = 0;
  if (magic_number != V0_MAGIC_NUMBER) {
    readUint16(patchFileReadStream, version_number);
  }
  //  errorLog << "applyPatch: version_number " << version_number << endl;

  if (version_number >= 1) {
    // Skip past the length and MD5 of the source file.
    patchFileReadStream.seekg(4 + 16, ios::cur);
  }

  // get the length of the patched result file
  AP_uint32 result_file_length;
  readUint32(patchFileReadStream, result_file_length);

  //  errorLog << "applyPatch: result_file_length " << result_file_length << endl;

  // Skip past the MD5 of the resultant file
  patchFileReadStream.seekg(16, ios::cur);

#if 0
  // check the filename
  // this is a bit hackish
  AP_int32 name_length;
  readInt32(patchFileReadStream, name_length);

  errorLog << "name_length = " << name_length << endl;

  patchFileReadStream.read((char*)buffer, name_length);
  buffer[name_length] = 0x00;
  if ((name_length > (AP_int32)strlen(fileName)) ||
      strcmp((const char*)buffer, (const char*)&fileName[strlen(fileName)-name_length]))
  {
    errorLog << "applyPatch(): patch intended for file: " << (char*)buffer
      << ", not file: " << fileName << endl;
    return -1;
  }
#endif
  errorLog << "applyPatch(): valid patchfile for file: " << fileName << endl;

  // Now patch the file using the given buffer
  AP_uint16 ADD_length;
  AP_uint16 COPY_length;
  AP_int32 COPY_offset;

  while (!patchFileReadStream.eof() && !patchFileReadStream.fail()) {
    ///////////
    // read # of ADD bytes
    readUint16(patchFileReadStream, ADD_length);

    // if there are bytes to add, read them from patch file and write them to output
    if (0 != ADD_length) {
      AP_uint32 bytes_left = (AP_uint32)ADD_length;

      while (bytes_left > 0) {
        AP_uint32 bytes_this_time = ((int)bytes_left < BUFFER_LENGTH) ? bytes_left : BUFFER_LENGTH;
        patchFileReadStream.read((char*)buffer, bytes_this_time);
        tempFileWriteStream.write((char*)buffer, bytes_this_time);
        bytes_left -= bytes_this_time;
      }
    }

    ///////////
    // read # of COPY bytes
    readUint16(patchFileReadStream, COPY_length);

    // if there are bytes to copy, read them from original file and write them to output
    if (0 != COPY_length) {
      // read copy offset
      readInt32(patchFileReadStream, COPY_offset);

      // seek to the offset
      if (version_number < 2) {
        origFileReadStream.seekg(COPY_offset, ios::beg);
      } else {
        origFileReadStream.seekg(COPY_offset, ios::cur);
      }

      // read the copy bytes from original file and write them to output
      AP_uint32 bytes_left = (AP_uint32)COPY_length;

      while (bytes_left > 0) {
        AP_uint32 bytes_this_time = ((int)bytes_left < BUFFER_LENGTH) ? bytes_left : BUFFER_LENGTH;
        origFileReadStream.read((char*)buffer, bytes_this_time);
        tempFileWriteStream.write((char*)buffer, bytes_this_time);
        bytes_left -= bytes_this_time;
      }
    }

    // if we got a pair of zero-length ADD and COPY blocks, we're done
    if ((0 == ADD_length) && (0 == COPY_length)) {
      break;
    }
  }

  free(buffer);

  // close files
  patchFileReadStream.close();
  origFileReadStream.close();
  tempFileWriteStream.close();

  // delete the patch file and the original file
  remove(patchFileName);
  remove(fileName);

  // rename the temp file
  if (rename(tempFileName, fileName)) {
    errorLog << "applyPatch(): failed to rename temp file " << tempFileName <<
      " to: " << fileName << endl;
    return -1;
  }

  return 0;
}

