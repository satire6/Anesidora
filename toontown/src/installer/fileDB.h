// Filename: fileDB.h
// Created by:  darren (08Nov00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#ifndef FILEDB_H
#define FILEDB_H

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#include "installer_md5.h"

class fileDB_MD5 {
public:
  MD5HashVal _hashVal;
  fileDB_MD5 *_next;

  int init(MD5HashVal *hashVal, fileDB_MD5 *next);
};

class fileDBEntry {
public:
  char *_filename;
  fileDB_MD5 *_head;
  fileDBEntry *_next;

  fileDBEntry();
  ~fileDBEntry();

  int init(const char *filename, fileDBEntry *next);
  int addMD5(MD5HashVal &hashVal);
  bool fullPathname(char *, const size_t) const;
  string fullPathname() const;
};

class fileDB {
public:
  fileDB();
  ~fileDB();

  int readFromFile(const char *filename);
  int readFromMem(char *buf, unsigned long bufLen);
  int readFromString(string &bufstr);

  void freeDatabase();

  fileDBEntry *firstFile();

protected:
  fileDBEntry *_head;

  void addDBEntry(fileDBEntry &entry);
  void deleteDBEntry(fileDBEntry **entry);

  static const char *whitespace;
  int extractMD5(string &line, size_t pos_start, size_t &pos_end, MD5HashVal &output);
};

#endif
