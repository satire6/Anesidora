// Filename: fileDB.cxx
// Created by:  darren (08Nov00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"

#include "fileDB.h"
#include "log.h"

#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include "strl.h"

using namespace std;

const char *fileDB::whitespace = "\r\n\t ";

fileDBEntry::
fileDBEntry() {
  _filename = NULL;
  _head = NULL;
}

fileDBEntry::
~fileDBEntry() {
  free(_filename);

  // delete the list of MD5 values
  fileDB_MD5 *p = _head;
  while(p) {
    fileDB_MD5 *temp = p;
    p = p->_next;
    delete temp;
  }
}

int fileDBEntry::
init(const char *filename, fileDBEntry *next) {
  _filename = _strdup(filename);
  if (!_filename) return -1;
  _next = next;
  return 0;
}

int fileDBEntry::
addMD5(MD5HashVal &hashVal) {
  fileDB_MD5 *newEntry = new fileDB_MD5;

  memcpy(newEntry->_hashVal, &hashVal, sizeof(MD5HashVal));

  // find the end of the list, to maintain ordered list. yech.
  fileDB_MD5 **ptrptr = &_head;

  while(*ptrptr) {
    ptrptr = &((*ptrptr)->_next);
  }

  *ptrptr = newEntry;
  newEntry->_next = NULL;
  return 0;
}

bool fileDBEntry::
fullPathname(char *buffer, const size_t maxsize) const
{
  return (_fullpath(buffer, _filename, maxsize-1) != NULL);
}

string fileDBEntry::
fullPathname() const
{
  char fullNameBuf[_MAX_PATH];
  string fullName;
  if (fullPathname(fullNameBuf, sizeof(fullNameBuf)) )
    return string(fullNameBuf);
  return string("");
}

fileDB::
fileDB() {
  _head = NULL;
}

fileDB::
~fileDB() {
  freeDatabase();
}

// reads an MD5 value from a string, starting at a given offset.
// the four values of the MD5 are represented as consecutive
// whitespace-delimited decimal integers.
//
// function has three return values:
//  pos_end is set to the offset of the end of the hash value
//  output is set to the MD5 value
//  function returns 0 on success
//    on failure, output may contain a partial value
int fileDB::
extractMD5(string &line, size_t pos_start, size_t &pos_end, MD5HashVal &output) {
  // this should make it pretty obvious when things don't get read in right
  output[0] = 0;
  output[1] = 0;
  output[2] = 0;
  output[3] = 0;

  pos_end = pos_start;

  for (int i = 0; i < 4; i++) {
    pos_start = line.find_first_not_of(whitespace, pos_end);
    if (string::npos == pos_start)
    {
      return -1;
    }
    //errorLog << "fileDB::extractMD5(): pos_start=" << pos_start;
    
    pos_end = line.find_first_of(whitespace, pos_start);
    if (string::npos == pos_end)
    {
      return -1;
    }

    //errorLog << "; pos_end=" << pos_end << endl;

    string number = line.substr(pos_start, pos_end - pos_start);

    output[i] = strtoul((const char*)number.c_str(), NULL, 10);
  }
  return 0;
}

int fileDB::
readFromFile(const char *filename)
{
  ifstream read_stream;
  int retVal;

  read_stream.open(filename, ios::in | ios::binary);
  if (read_stream.fail()) {
    errorLog << "fileDB::readFile - Failed to open: " << filename << endl;
    return -1;
  }

  // get the size of the database file
  read_stream.seekg(0, ios::end);
  long file_size = read_stream.tellg();
  read_stream.seekg(0, ios::beg);

  // allocate a buffer to hold the whole thing
  char *buf = new char[file_size];

  // read the file in
  read_stream.read(buf, file_size);
  if (read_stream.fail()) {
    errorLog << "fileDB::readFile - Failed to read: " << filename << endl;
    return -1;
  }

  read_stream.close();

  retVal = readFromMem(buf, file_size);

  delete[] buf;

  return retVal;
}

int fileDB::
readFromMem(char *buf, unsigned long bufLen) {
  //errorLog << "readFromMem" << endl;
  string bufstr((char*)buf, bufLen);
  return readFromString(bufstr);
}

int fileDB::
readFromString(string &bufstr) {
  MD5HashVal md5_hash;

  freeDatabase();

  size_t p = 0;
  errorLog << "fileDB::readFromString(): " << "bufLength=" << bufstr.length() << endl;
  while (p < bufstr.length()) {
    //errorLog << "fileDB::readFromString(): " << "p=" << p;
    // get the next line of the file
    size_t nl = bufstr.find("\n", p);
    if (string::npos == nl)
      break;

    //errorLog<< "; nl=" << nl << endl;

    string line = bufstr.substr(p, nl - p);

    // grab the filename
    size_t begin_fn = line.find_first_not_of(whitespace, 0);
    if (string::npos == begin_fn)
      break;

    //errorLog << "fileDB::readFromString(): " << "begin_fn=" << begin_fn;

    size_t end_fn = line.find_first_of(whitespace, begin_fn);
    if (string::npos == end_fn)
      break;

    //errorLog << "; end_fn=" << end_fn << endl;

    string fname = line.substr(begin_fn, end_fn - begin_fn);

    //errorLog << "fileDB::readFromString(): " << fname << endl;

    // read in the MD5 checksums
    int error_occurred = 0;
    size_t pos_start = end_fn;
    size_t pos_end = pos_start;

    // read in the checksum of the current version
    if(extractMD5(line, pos_start, pos_end, md5_hash)) {
      // something went wrong... we definitely need to able to read this in.
      errorLog << "fileDB::readFromString() - extractMD5 encountered incomplete md5\n";
      return 1;  // If bad md5 found, report it.
      //break;
    }

    /*
    errorLog << md5_hash[0] << " "
             << md5_hash[1] << " "
             << md5_hash[2] << " "
             << md5_hash[3] << endl;
    */

    // allocate the entry structure
    fileDBEntry *entry = new fileDBEntry();
    entry->init(fname.c_str(), NULL);
    if(entry->addMD5(md5_hash)) {
      delete entry;
      break;
    }

    // read the rest of the MD5s in
    while(1) {
      // start at the end of the previous MD5
      pos_start = pos_end;

      if(extractMD5(line, pos_start, pos_end, md5_hash)) {
        //errorLog << "line size:" << line.size() << " and pos_start:" << pos_start << endl;
        if (line.size()-1 != pos_start)
          errorLog << "fileDB::readFromString() - extractMD5 missing md5's\n";
        break;
      }
      /*
      errorLog << md5_hash[0] << " "
               << md5_hash[1] << " "
               << md5_hash[2] << " "
               << md5_hash[3] << endl;
      */

      if(entry->addMD5(md5_hash)) {
        break;
      }
    }

    addDBEntry(*entry);

    p = nl + 1;
  }

  return 0;
}

void fileDB::
addDBEntry(fileDBEntry &entry) {
  // find the end of the list, to maintain ordered list. yech.
  fileDBEntry **ptrptr = &_head;

  while(*ptrptr) {
    ptrptr = &((*ptrptr)->_next);
  }

  *ptrptr = &entry;
  entry._next = NULL;
}

void fileDB::
freeDatabase() {
  deleteDBEntry(&_head);
}

void fileDB::
deleteDBEntry(fileDBEntry **entry)
{
  if (*entry)
  {
    deleteDBEntry(&((*entry)->_next));
    delete *entry;
    *entry = NULL;
  }
}

fileDBEntry *fileDB::
firstFile() {
  return _head;
}
