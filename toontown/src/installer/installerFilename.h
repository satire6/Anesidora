// Filename: installerFilename.h
// Created by:  darren (06Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#ifndef INSTALLERFILENAME_H
#define INSTALLERFILENAME_H

#include <stdlib.h>
#include <string>

using namespace std;

extern void combinePathAndFilename(char *dest, const char *path, const char *filename);
extern void combinePathAndFilename(string &destStr, const char *path, const char *filename);

class installerFilename {
public:
  installerFilename(const char *baseName = NULL);

  const char *getBaseName() const;
  const char *getFullLocalName() const;
  const char *getFullRemoteName() const;

  void setBaseName(const char *baseName);
  void setLocalPath(const char *localPath);
  void setFullLocalName(const char *fullLocalName);
  void setRemotePath(const char *remotePath);
  void setFullRemoteName(const char *fullRemoteName);

protected:
  string _baseName;
  string _fullLocalName;
  string _fullRemoteName;
private:
};

#endif
