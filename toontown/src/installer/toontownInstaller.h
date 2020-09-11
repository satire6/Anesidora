// Filename: toontownInstaller.h
// Created by:  darren (05Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////
//
// The Toontown Installer is executed in a web browser, as an ActiveX
// control, or Netscape plugin, etc. It alternates control with Javascript
// running from the web page, using a master "StateCode" number to track the
// current state. This alternation is necessary because Javascript is
// needed to control flash movies that are played in the browser, while
// the Installer is busy downloading the Launcher (the first Panda3D phase),
// and then while the Launcher downloadins Panda3D (second phase), etc.,
// up until the point when Panda3D takes over in fullscreen mode and
// the game begins.

// The alternation between the installer and javascript continues
// throughout the execution of the game, so that the installer can keep
// tabs on the game and notify the user appropriately if the game crashes.

#ifndef TOONTOWNINSTALLER_H
#define TOONTOWNINSTALLER_H

#define _MAX_ALTERNATE_SERVER 7

#include "installerBase.h"
#include "sysinfo.h"

  // the following enumeration is to report specific installation problem
  // add the problem that you like to report here in the future
enum Type {
  HARDWARE_INVALID,
  HARDWARE_VALID,
  HARDWARE_INVALID_3D,
};

class toontownInstaller : public installerBase
{
public:
  toontownInstaller();
  virtual ~toontownInstaller();

  int init();
#ifndef _INSTALLERSERVICE_
  bool normalInit(const HWND installer_hwnd=NULL);
#else
  bool normalInit(const HWND installer_hwnd=NULL, const TCHAR *deployment=NULL, const TCHAR *downloadServer=NULL, const TCHAR *downloadVersion=NULL);
#endif

  // standard installer interface
  void runInstaller();
  int setKeyValue(const char *key, const char *value);
  bool getKeyValue(const char *keyName, string &keyValue);

protected:
  size_t statecode();
  long getPercentLoaded();
  long getOverallPercentLoaded();
  void initOverallPercentLoaded();
  int  checkPandaError();

  void setGreen(const char * green);
  void setBlue(const char * blue);
  void PlayToken(const char * playToken);
  void setLastLogin(const char * userName);
  void setSWID(const char * swid);

  void selectDownloadServer();
  void DownloadServer(const char * downloadServer, bool bUpdate = false);
  void setDownloadServerList(const char * downloadServerList);

  void DownloadVersion(const char * downloadVersion);
  void GameServer(const char * gameServer);
  void AccountServer(const char * accountServer);
  void setReferrerCode(const char * referrerCode);

  void game1IsDone();
  void game2IsDone();

#ifndef _EXEINSTALLER_
  string getGame1Filename();
  string getMovieFilename();
  string getGame2Filename();
  string getMessagesFilename();
#endif

  // perhaps these should be part of standard installer interface?
  const char *getInstallerLogFileName();
  const char *getLauncherExtractionLogFileName();
  // const char *getGameLogFileName();
  // const char *getUserErrorString();
  string getLauncherMessage();
  string getUserLoggedIn();
  string getPaidUserLoggedIn();

  string getExitPage();

  void readLogFile(const char *header,
                   const char *footer,
                   const char *logFileName,
                   ostringstream &dest,
                   int endbytes_to_read = 0);

#if !defined(_INSTALLERSERVICE_) && !defined(USE_RPCSERVICE)  && !defined(_EXEINSTALLER)
protected:
#endif
  void shutdown();

  int createRegistry(const char *RegKeyName, PHKEY _hKey, PACL pNewDacl);
  int  regInit();
  void regShutdown();

  Type validHardware();

  void checkProxyServer();

  void addUserError(int error_idx);
  void addUserError(const char *error);
  void addUserError(char *error);
  void addUserErrorAndLog(const char *error);
  void addUserAccessDeniedToErrorAndLog(const char *filename);

  // get the URL to download things from
  const char* getDownloadRootURL();
  void formDownloadURLs();

  bool formLogFileNames();

  void ShowLocalizedMessage(char *whatStr);

  const char *CreateErrorString();
  void CreateErrorPage(const char *remoteURL);
  void CreateLogFilesStr(ostringstream &logFilesStr);
  const char *getLocalErrorPageData();

  int justMakeErrorPage();
  int justCheckSystemPage();

  //bool TestHKLMWriteable(void);

  bool initInstallDir();
  bool makeInstallDir(char *installDir);

#ifndef _EXEINSTALLER_
  int game2Done();
#endif

  bool sufficientDiskSpace(const char *dir, unsigned __int64 space,
                           bool &sufficient);

  int startLauncherSelfExtract();
  int launcherHasBeenExtracted();
  int launcherSelfExtractDone();

  // TODO: make functions out of all the cases and put them here
  void extractLauncher();
  void handleCase0();
  void handleCase7();
  void handleCase10();
  void handleCase13();
  void handleCase23();
  void handleCase25();
  void handleCase30();
  void handleCase35();
  void handleCase36();
  void handleCase37();
  void handleCase38();
  void handleCase40();
  void handleCase50();
  void handleCase53();
  void handleCase55();
  void handleCase60();
  void handleCase85();
  void handleCase90();
  void handleCase97();
  void handleCase110();
  void handleCase115();
  void handleCase120();
  void handleCase130();

  int runLauncher();
  int launcherExitedPrematurely();
  int launcherAlive(DWORD &exitCode);
  int pandaWindowOpen();

#ifndef _EXEINSTALLER_
  void setGame1Version(const char *ver);
  void setMovieVersion(const char *ver);
  void setGame2Version(const char *ver);
  void setMessagesVersion(const char *ver);
  void setToontuneVersion(const char *ver);

  void setLauncherMessage(const char *msg);
#endif

  void deleteOldLogs(const char *logPathPattern);

  void setPreventHack(DWORD value);
  DWORD getPreventHack();
  void setPreventHack2(const char *value);
  string getPreventHack2();
  void setChatEligible(DWORD value);  // Deprecated
  void WebAccountParams(const char *value);

  string Deployment();
  void Deployment(const char *);

#ifndef _EXEINSTALLER_
  void getFlashVersionInfoFromReg(char *verStr, const char *key,
                  int &needToDownload);
  void setFlashMovieVersion(const char *newVer, char *verStr, char *name);
  int needToDownloadFlashMovie(const char *filename, int downloadFlag);
  void flashMovieDownloadedSuccessfully(const char *regKey, const char *verStr);
  int downloadFlashMovie(installerFilename &filename, int downloadFlag,
                         const char *regKey, const char *version);
#endif

  void reFocusWindow(const HWND, const int nCmdShow);
  void reFocusWindow(const char *window_title, const int nCmdShow);

  bool set_proxy_spec(const string &proxy_spec, const string &direct_hosts);
  bool CheckInstallerVersionNum(void);
  bool GetInstallerVersion(ULARGE_INTEGER &Ver);
#ifndef _EXEINSTALLER_
  string _ActiveXFilePath;
#endif  
  void CreateConfigInfoRecord(void);
  void SendConfigRecord(void);
  void do_basic_init(void);

#if !defined(_INSTALLERSERVICE_) && !defined(USE_RPCSERVICE) && !defined(_EXEINSTALLER_) 
protected:
#endif
  // These allow us to mark the exact place where the install bombed out for statistical purposes.
  // To make old logs consistent w/new ones, never use one of these IDs more than once,
  // or reuse unused old ones.  Always create a new one at the end.
  typedef enum {
        E1=1,E2,E3,E4,E5,E6,E7,E8,E9,E10,
        E11,E12,E13,E14,E15,E16,E17,E18,E19,E20,
        E21,E22,E23,E24,E25,E26,E27,E28,E29,E30,
        E31,E32,E33,E34
  } InstallerErrorPoint;

  void setErrorState(unsigned int ErrorState, InstallerErrorPoint errpnt);

  unsigned int _StateCode;
  unsigned int _FinalNonErrorState;
  unsigned int _InstallerErrorPoint;
           int _LastPandaErrorCode;

  int _initialized;
  int _game1_Done;
  float _DiskSpace_Megs_Free;
  bool  _bHTTPproxyIsUsed;
  bool  _bDoConfigInfoCollection;
  bool  _bConfigSubmitApproved;

  registryKey _regToontown;
  registryKey _regHackers;

  HANDLE _curDownloadThreadHandle;

  // this counts the number of times we've re-downloaded the installer and
  // failed the "installer valid" check
  int _launcherInvalidCount;

  // handle to launcher self-extract/installation process
  HANDLE _hInstallLauncherProcess;

  // handle to launcher process
  HANDLE _hLauncherProcess;
  DWORD  _LauncherProcessID;
  DWORD  _LauncherDownloadTryNum;
  int _OK_To_Kill_LauncherProcess;
  time_t _lastmemcheck_time;
  time_t _cur_memcheck_interval;  // in secs

  // "user error" - holds the list of errors shown to the user on the help web page
  string _userErrorString;
  string _systemErrorString;

  char _toontownInstallDir[_MAX_PATH];

  // registry value names
  static const char *_INSTALL_DIR_ValueName;
  static const char *_LAUNCHER_EXTRACTED_ValueName;
  static const char *_PERCENT_LOADED_ValueName;
  static const char *_PERCENT_OVERALL_LOADED_ValueName;
  static const char *_LAUNCHER_MESSAGE_ValueName;
  static const char *_PANDA_WINDOW_OPEN_ValueName;
  static const char *_PANDA_ERROR_CODE_ValueName;
  static const char *_GREEN_ValueName;
  static const char *_BLUE_ValueName;
  static const char *_PLAYTOKEN_ValueName;
  static const char *_LAST_LOGIN_ValueName;
  static const char *_GAME2_DONE_ValueName;
#ifndef _EXEINSTALLER_
  static const char *_GAME1_VERSION_ValueName;
  static const char *_MOVIE_VERSION_ValueName;
  static const char *_GAME2_VERSION_ValueName;
  static const char *_MESSAGES_VERSION_ValueName;
  static const char *_TOONTUNE_VERSION_ValueName;
#endif
  static const char *_PROXY_SERVER_ValueName;
  static const char *_PROXY_DIRECT_HOSTS_ValueName;
  static const char *_PROXY_USER_ValueName;
  static const char *_PROXY_PASSWORD_ValueName;  // password for user
  static const char *_USER_LOGGED_IN_ValueName;
  static const char *_PAID_USER_LOGGED_IN_ValueName;
  static const char *_EXIT_PAGE_ValueName;
  static const char *_REFERRER_CODE_ValueName;
  static const char *_configSubmitApprovedRegValName;
  static const char *_PREVENT_HACKERS_ValueName;
  static const char *_PREVENT_HACKERS_ValueName2;
  static const char *_CHAT_ELIGIBLE_ValueName;   // Deprecated
  static const char *_WEB_ACCT_PARAMS_ValueName; //new registry to record all chat related params
  static const char *_PATCH_FROM_CD_ValueName;
  static const char *_CDROM_ValueName;
  static const char *_DOWNLOAD_SERVER_ValueName;
  static const char *_GAMELOG_FILENAME_ValueName;
  static const char *_DEPLOYMENT_ValueName;

  //////////////////////////////////
  //// these are passed as arguments to python
  // this is the full URL of the download server
  char _DOWNLOAD_SERVER_String[_MAX_PATH];

  // this is the IP/computer name of the game server
  char _GAME_SERVER_String[_MAX_PATH];

  // this is the IP/computer name of the account server
  char _ACCOUNT_SERVER_String[_MAX_PATH];

  // arguments to configrc.exe
  string _configrc_args;
  string _ConfigInfo;

  // Blast info
  char _SWID_String[256];
  //////////////////////////////////

  // this is the URL of the download server
  char _downloadServerURL[_MAX_PATH];

  // maximum of _MAX_ALTERNATE_SERVER servers to try to download from
  string _downloadServerList[_MAX_ALTERNATE_SERVER];

  // this is the download 'version', used to get around
  // proxy caches that incorrectly hold on to old versions
  // of files
  char _downloadVersion[_MAX_PATH];
  // this is used to hold the combination of the download server
  // and the download version
  char _downloadRootURL[_MAX_PATH];

  string _ConfigStatsServerTargetURL;

#ifndef _EXEINSTALLER_
  // files from the download server
  installerFilename _game1_IFilename;
  installerFilename _movie_IFilename;
  installerFilename _game2_IFilename;
  installerFilename _messages_IFilename;
  installerFilename _toontune_IFilename;

  // these strings hold the version strings of the flash movies
  // that are currently downloaded
  char _game1Version[_MAX_PATH];
  char _movieVersion[_MAX_PATH];
  char _game2Version[_MAX_PATH];
  char _messagesVersion[_MAX_PATH];
  char _toontuneVersion[_MAX_PATH];

  // these flags are set if the flash movies have to be downloaded
  int _needToDownloadGame1;
  int _needToDownloadMovie;
  int _needToDownloadGame2;
  int _needToDownloadMessages;
  int _needToDownloadToontune;
#endif // _EXEINSTALLER_

  int _reg_initialized;
  SysInfo *_pSysInfo;

  enum { INVALID_STATECODE = -999 };
  void printStateCodeUpdates();
  bool store_encoded_time(void);

  // should be part of installerBase
  ULARGE_INTEGER _liActiveXVersion,_liActiveXVerReqd;

  std::string _localErrorPageData;
  std::string _installerLogPathPattern;
  std::string _gameLogPathPattern;
  stringvec _TroublesomeRunningPrograms,_TroublesomeInstalledPrograms;

  HWND _installer_hwnd;

private:
};

#include "toontownInstaller.I.h"

#endif
