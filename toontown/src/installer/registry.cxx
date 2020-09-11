//
// $Id$
//
////////////////////////////////////////////////////////////////////

#include <windows.h>
#include <string.h>
#include <errno.h>
#include "registry.h"

// setValue() is a thin layer of abstraction to the RegSetValueEx() registry function.
// sets a value of any type under a specific key
int setValue(HKEY hKey, const char *valueName, const DWORD type, LPBYTE value, const DWORD size) {
  ULONG retVal = RegSetValueEx(hKey, valueName, 0, type, value, size);
  return (ERROR_SUCCESS != retVal);
}

// getValue() is a thin layer of abstraction to the RegQueryValueEx() registry function.
// gets a value of any type under a specific key
int getValue(HKEY hKey, const char *valueName, DWORD type, LPBYTE pValue, DWORD size) {
  ULONG retVal = RegQueryValueEx(hKey, valueName, 0, &type, pValue, &size);
  return (ERROR_SUCCESS != retVal);
}

//////////////////////////////////////////////////////////////////////////////

// getDWORD() retrieves a 32-bit value under a particular key. returns 0 on success
// returnval = value if it exists, otherwise undefined
int registryKey::
_getDWORD(const char *key, DWORD &returnval) const {
  // note: if regvalue doesnt exist, do NOT touch "returnval" output var!
  DWORD tmp;
  int s = getValue(_hKey, key, REG_DWORD, (LPBYTE)&tmp, sizeof(DWORD));
  if (s == 0)
    returnval = tmp;
  return s;
}

// regSetDWORD() sets a 32-bit value under a particular key. returns 0 on success
int registryKey::
_setDWORD(const char *key, const DWORD val) const {
  return setValue(_hKey, key, REG_DWORD, (LPBYTE)&val, sizeof(DWORD));
}

//////////////////////////////////////////////////////////////////////////////

// getString() retrieves a string value under a particular key. returns 0 on success
// guarantees null string if error
int registryKey::
_getString(const char *key, char *returnstr, size_t str_len) const {
  int s = getValue(_hKey, key, REG_SZ, (LPBYTE)returnstr, str_len);
  if (s != 0)                   // error returns null string
    returnstr[0] = '\0';
  return s;
}

// setString() sets a string value under a particular key. returns 0 on success
int registryKey::
_setString(const char *key, const char *str) const {
  return setValue(_hKey, key, REG_SZ, (LPBYTE)str, strlen(str));
}

//////////////////////////////////////////////////////////////////////////////

// openKey() opens a new key under a parent key
// requires registry write permission for that key
HKEY registryKey::
openKey(const HKEY parent, const char *keyName) {
  if (ERROR_SUCCESS != RegCreateKeyEx(parent, keyName, 0, "",
              REG_OPTION_NON_VOLATILE, KEY_READ | KEY_WRITE,
              NULL, &_hKey, NULL))
  {
    _hKey = NULL;
  }
  return _hKey;
}

// openRO() opens a new key under a parent key for reading only
HKEY registryKey::
openRO(const HKEY parent, const char *keyName) {
  if (ERROR_SUCCESS != RegOpenKeyEx(parent, keyName, 0, KEY_READ, &_hKey)) {
//    errorLog << "registryKey::openRO failed, " << GetLastErrorStr() << endl;
    _hKey = NULL;
  }
  return _hKey;
}

// closeKey() closes a previously opened key; user code should only call
// closeKey() for user keys created with openKey() or openRO()
void registryKey::
closeKey() {
  if (_hKey != NULL) {
    RegCloseKey(_hKey);
    _hKey = NULL;
  }
}

//////////////////////////////////////////////////////////////////////////////

int registryKey::
getString(const char *key, char *returnstr, const size_t len) const {
  return _getString(key, returnstr, len - 1);
}

int registryKey::
getString(const char *key, string &returnstr) const {
  char tmp[_MAX_PATH];
  int s = _getString(key, tmp, sizeof(tmp) - 1);
  returnstr = tmp;
  return s;
}

string registryKey::
getString(const char *key) const {
    string s;
    getString(key, s);
    return s;
}

int registryKey::
getDWORD(const char *key, DWORD &returnval) const {
  return _getDWORD(key, returnval);
}

DWORD registryKey::
getDWORD(const char *key) const {
  DWORD v;
  if (getDWORD(key, v))
    return 0;       // problem getting value from registry, return 0
  return v;           // return valid value from registry
}

int registryKey::
setString(const char *key, const char *str) const {
  return _setString(key, str);
}

int registryKey::
setDWORD(const char *key, const DWORD val) const {
  return _setDWORD(key, val);
}

// deleteValue() deletes a value under a particular key. returns 0 on success
int registryKey::
deleteValue(const char *key) const {
  return (ERROR_SUCCESS != RegDeleteValue(_hKey, key));
}

