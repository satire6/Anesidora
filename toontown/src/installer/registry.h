//
// $Id$
//
////////////////////////////////////////////////////////////////////

#pragma once
#ifndef __REGISTRY_H__
#define __REGISTRY_H__

#include <string>
using namespace std;

int getValue(HKEY, const char *key, DWORD type, LPBYTE buffer, DWORD size);
int setValue(HKEY, const char *key, const DWORD type, LPBYTE buffer, const DWORD size);

class registryKey {
  HKEY _hKey;

  int _getDWORD(const char *key, DWORD &returnval) const;
  int _setDWORD(const char *key, const DWORD val) const;
  int _getString(const char *key, char *returnstr, size_t len) const;
  int _setString(const char *key, const char *str) const;

public:
  registryKey() : _hKey(NULL) {}
  ~registryKey() { closeKey(); }

  HKEY openKey(const HKEY parent, const char *keyName);
  HKEY openRO(const HKEY parent, const char *keyName);
  void closeKey();

  void init(const HKEY key) {
    _hKey = key;
  }

  int getString(const char *key, char *returnstr, const size_t len) const;
  int getString(const char *key, string &returnstr) const;
  int getString(const string &key, const string &returnstr) const {
    return getString(key.c_str(), returnstr);
  }
  int getDWORD(const char *key, DWORD &returnval) const;

  // guarantees string or empty string
  string getString(const char *key) const;
  string getString(const string &key) const {
      return getString(key.c_str());
  }
  // guarantees value or 0
  DWORD getDWORD(const char *key) const;
  DWORD getDWORD(const string &key) const {
      return getDWORD(key.c_str());
  }

  int setString(const char *key, const char *str) const ;
  int setString(const char *key, const string &str) const {
    return setString(key, str.c_str());
  }
  int setString(const string &key, const string &str) const {
    return setString(key.c_str(), str.c_str());
  }
  int setDWORD(const char *key, const DWORD val) const;
  int setDWORD(const char *key, const int val) const {
    return setDWORD(key, (DWORD) val);
  }

  int deleteValue(const char *) const;
  int deleteValue(const string &str) const {
      return deleteValue(str.c_str());
  }

  bool notvalid() const {
    return _hKey == NULL;
  }
};

#endif
