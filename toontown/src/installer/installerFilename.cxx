// Filename: installerFilename.cxx
// Created by:  darren (06Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"

#include <stdlib.h>
#include <string.h>
#include <string>

#include "installerFilename.h"
#include "installerBase.h"

void combinePathAndFilename(char *dest, const char *path, const char *filename) {
  char drive[_MAX_DRIVE];
  char dir[_MAX_DIR];
  char fname[_MAX_FNAME];
  char ext[_MAX_EXT];
  char temp_dest[_MAX_PATH];

  // _splitpath is dumb.  if the path doesnt end in '\', it assumes the final
  // part is a file when it may be a directory.  in this case we know it is in fact a dir
  // because the input is 'path'

  string pathstr = path;
  if(path[pathstr.size()-1]!='\\')
      pathstr.append("\\");

  _splitpath(pathstr.c_str(), drive, dir, NULL, NULL);
  _splitpath(filename, NULL, NULL, fname, ext);
  _makepath(temp_dest, drive, dir, fname, ext);
  const char *HTTP_prefix="http://";

  if(strncmp(temp_dest,HTTP_prefix,7)==0) {
      // switch all slashes fwd, remove double fwd slashes
      for(char *p1=temp_dest;*p1!='\0';p1++) {
          if(*p1=='\\')
            *p1='/';
      }

      char *pin=temp_dest+7;  // skip front 'http://'
      strcpy(dest,HTTP_prefix);
      char *pout=dest+7;
      bool bLastWasSlash=false;
      for(;(*pin!='\0');pin++) {
          if(!(bLastWasSlash && (*pin=='/'))) {
              *pout = *pin;
              bLastWasSlash = (*pin=='/');
              pout++;
          }
      }
      *pout='\0';
  } else {
      // remove double back slashes
      char *pin=temp_dest;
      char *pout=dest;
      bool bLastWasSlash=false;
      for(;(*pin!='\0');pin++) {
          if(!(bLastWasSlash && (*pin=='\\'))) {
              *pout = *pin;
              bLastWasSlash = (*pin=='\\');
              pout++;
          }
      }
      *pout='\0';
  }

  // ShowErrorBox(dest);
}

void combinePathAndFilename(string &destStr, const char *path, const char *filename) {
  char dest[_MAX_PATH];
  combinePathAndFilename(dest,path,filename);
  destStr = dest;
}

installerFilename::
installerFilename(const char *baseName) {
  if(baseName)
     _baseName = baseName;
}

const char *installerFilename::
getBaseName() const {
  return _baseName.c_str();
}

const char *installerFilename::
getFullLocalName() const {
  return _fullLocalName.c_str();
}

const char *installerFilename::
getFullRemoteName() const {
  return _fullRemoteName.c_str();
}

void installerFilename::
setBaseName(const char *baseName) {
  _baseName = baseName;
}

void installerFilename::
setFullLocalName(const char *fullLocalName) {
  _fullLocalName = fullLocalName;
}

void installerFilename::
setFullRemoteName(const char *fullRemoteName) {
  _fullRemoteName = fullRemoteName;
}

void installerFilename::
setRemotePath(const char *remotePath) {
  combinePathAndFilename(_fullRemoteName, remotePath, _baseName.c_str());
}

void installerFilename::
setLocalPath(const char *localPath) {
  combinePathAndFilename(_fullLocalName, localPath, _baseName.c_str());
}

