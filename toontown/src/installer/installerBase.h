// Filename: installerBase.h
// Created by:  darren (05Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#ifndef INSTALLERBASE_H
#define INSTALLERBASE_H

// installer virtual base class
// encapsulates project-independent installer functionality

// This class includes utility functions that deal with file names,
// file properties, downloading files, spawning processes, reading
// from and writing to the registry, calculating MD5 checksums, and
// downloading and installing Panda.

#include <windows.h>
#include <string.h>
#include <time.h>
#include "installerFilename.h"
#include "fileDB.h"
#include "installer_md5.h"
#include "log.h"
#include "registry.h"
#include <vector>
#include <string>

using namespace std;

//#define PANDA_LOCATED_SEPARATE_FROM_TT
//#define USE_DOWNLOAD_TO_FILE_CALLBACK


#ifdef USE_DOWNLOAD_TO_FILE_CALLBACK
// this is the type for a download-to-file callback
// return zero on success
typedef int (*DLToFileCallback)(const char *URL, const char *filename);
#endif

typedef vector<string> StrVec;

typedef enum _LauncherType {
  LAUNCHER_INVALID,
  LAUNCHER_VALID,
  LAUNCHER_NEED_EXTRACT,
  LAUNCHER_NEED_DOWNLOAD,
} LauncherType;

class installerBase {
public:
  installerBase();
  virtual ~installerBase();

  // main "make it go" function. Depending on the installer, this
  // may be called once, or any number of times.
  virtual void runInstaller() = 0;

  // sets the value associated with a particular installer key;
  // returns 0 on success
  virtual int setKeyValue(const char *key, const char *value);

  // gets the value associated with a particular installer key;
  // returns false on failure
  virtual bool getKeyValue(const char *keyName, string &keyValue);

#ifdef USE_DOWNLOAD_TO_FILE_CALLBACK
  // sets a callback for 'download to file'
  // obj is sent as first argument, can be used to pass object pointer
  void setDownloadToFileCallback(DLToFileCallback cb) {
    downloadToFileCallback = cb;
  }
#endif

  float  _PercentFileDownloaded;  // 0-1.0
  int _PatchSizeSoFar;
  int _PatchSize;
protected:

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  HKEY _hKeyPanda3D;
  int _pandaRegInitialized;
#endif

  void getAllFilesWithPathPattern(const char *pathsearchpattern,StrVec &strVec);
  void filesearch(string rootpath, string pattern, bool bRecursive, bool bSearchForDirs, bool bPrintFileInfo, StrVec &files);

  // this is the in-memory representation of the launcher file database
  // the database contains a list of launcher files and their MD5 checksums
  fileDB _launcherFileDB;
  // this database contains InstallLauncher.exe and a list of its hash values
  fileDB _launcherDDBFile;

  // files from the panda server
  installerFilename _launcherFileDB_IFilename;
  installerFilename _launcherDDBFile_IFilename;
  installerFilename _launcherProgress_IFilename;
  installerFilename _launcherSelfExtractor_IFilename;

  // purely local files
  installerFilename _runLauncher_IFilename;
  installerFilename _installerLogFile_IFilename;
  installerFilename _launcherExtractionLogFile_IFilename;
  // installerFilename _gameLogFile_IFilename;    // this is now determined dynamically when needed (only at bug report time)

private:
  // registry value names
#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  static const char *_P3D_INSTALL_DIR_ValueName;
  char _panda3DInstallDir[_MAX_PATH];
#endif

  char _pandaServerURL[_MAX_PATH];

#ifdef USE_DOWNLOAD_TO_FILE_CALLBACK
  DLToFileCallback downloadToFileCallback;
#endif

protected:
  // UTILITY METHODS
  void determine_proxy_spec();

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  // Panda3D utility methods
  virtual int  createPanda3DInstallDir();
  virtual const char *getPanda3DInstallDir();
  virtual int  pandaRegInit();
  virtual void pandaRegShutdown();
#endif

  virtual void setPandaServer(const char *pandaServerURL);

  virtual int getLatestLauncherFileDB();
  virtual LauncherType launcherValid();
  int launcherFileValid(installerFilename &fileName);

  virtual int patchLauncherFiles();
  int findPatchDirectory();
  int findPatchVersion(fileDB &, fileDBEntry **, int *, int *);

  // error utility methods
  string GetLastErrorStr() const;

  // file utility methods
  void makeFilenameInTempDir(char *dest, const char *filename);
  void convertFullFilenameToURL(const char *filename, char *url);
  bool fileExists(const char *filename);
  int  getFileSize(const char *filename);
  void getFileDate(const char *filename, FILETIME *pFileTime);
  bool deleteFile(const char *filename);
  bool deleteObsoleteFile(const char *filename);

  // directory utility functions
  unsigned __int64 directorySize(const char *dir);
  bool makeDir(const char *filename, PSECURITY_ATTRIBUTES pSA);
  void addTrailingSlash(char *filename);
  void removeTrailingSlash(char *filename);
  void addTrailingForwardSlash(char *filename);
  void removeTrailingForwardSlash(char *filename);

  // file downloading utility methods
  bool downloadToFile(const char *URL, const char *destFilename);
  bool downloadToMem(const char *URL, string &pRetFileBufString);
  bool downloadToMem_New(const char *URL,string *pRetFileBufString);
  bool testServer(const char *URL);

  HANDLE asyncDownloadToFile(const char *URL, const char *destFilename, bool bUseURLDownload);
  int asyncDownloadDone(HANDLE handle);

  void removeURLFromCache(const char *URL);

  // process utility methods
  enum { SPAWN_NORMAL, SPAWN_HIDDEN };
  virtual int spawnProcess(const char *cmdLine, int show, HANDLE *phProcess, DWORD *pProcessID);
  virtual int processActive(HANDLE hProcess, DWORD &exitCode);
  virtual int processActive(HANDLE hProcess);

  void writeInstalledSizeToRegistry(const char *ARP_ProgramName, unsigned __int64 total_size);

  typedef vector<string> stringvec;
  bool checkForTroublesomeInstalledSoftware(stringvec &ProgNames);
  bool checkForTroublesomeRunningSoftware(stringvec &ProgNames);
  bool ProgramIsRunning(const char *progname);
  void GetHardCodedVersion(ULARGE_INTEGER &Ver);

  // MD5 utility methods
  void calcFileMD5(const char *fname, MD5HashVal &ret);
  int verifyFileMD5(fileDBEntry *launcherFile, bool debug = false);
  void badFileMD5_debug(const string &, const string &);

  // patching utility methods
  int applyPatch(const char *patchFileName, const char *fileName);

  // key/value pair utility methods
  // keyMatch: inline, compares two key names, returns 0 on match
  inline int keyMatch(const char *key1, const char *key2) {
    return !_stricmp(key1, key2);
  }

  inline void printSeparator() {
    errorLog << "--------------" << endl;
  }

  const char *getInstallerVersionValid(void);

  string _logSuffix;

  // proxy utility methods
  string get_proxyname_using_jsproxy(const char *pAutoProxyScriptURL);
  string _proxy_spec, _direct_hosts;
  string _InstallerActiveXVersionURL;
  string _ProxyUserName,_ProxyUserPassword;
  string _AutoProxyScriptURL;
};

typedef struct {
  const char *URL;
  const char *destFilename;
  string *pProxy;
  string *pProxyUser;
  string *pProxyPW;
  float *pDownloadPercent;
  int *pPatchSizeSoFar;
  int iPatchSize;
  bool  bUseURLDownloadtoFile;
  bool  bDoExitThread;

  // holds returned buffer containing inmemory download
  bool  bDoMemoryDownload;
  ostringstream *pStringStrm;
} DLArgs_s;

typedef struct {
  const char *URL;
  char *pHeaderStr;
  string *pProxy;
  string *pProxyUser;
  string *pProxyPW;
  float *pUploadPercent;
  //bool  bDoExitThread;
  const char *pBuf;
  DWORD cBufSize;
} UploadArgs_s;

extern unsigned long DownloadFunc(DLArgs_s *argPtr);
extern unsigned long UploadFunc(UploadArgs_s *args);
extern const char *InternetSettingsRegKey;  //under HKEY_CURRENT_USER
extern const char *ActiveXCache_RegValName;

extern void LogOSErrorMessage(const char *called_func);
extern void ShowOSErrorMessageBox(char *error_title);
extern void ShowErrorBox(const char *msg);
extern bool MyGetTempPath(DWORD path_buffer_length, char *temp_path);
extern HMODULE GetOurModuleHandle(void);

extern int GetPatchSize(int highVer);

extern bool DoesProcessExist(const char *process_name);
#endif
