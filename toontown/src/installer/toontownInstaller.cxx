// Filename: toontownInstaller.cxx
// Created by:  darren (05Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////

#include "pragma.h"

// If this is defined, fail to start unless installer version is up-to-date
//#define BLOCK_OLD_INSTALLER_VERSIONS

// I need those #defines, so define XP.  I'm just gonna make us responsible for not linking directly to fns
// that dont exist on older Win platforms so we can run OK on them, instead of having _WIN32_WINNT hide defs from us
#define _WIN32_WINNT 0x0501   // WinXP

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <shlobj.h>
#include <process.h>
#include <wininet.h>
#include <string>
#include <fstream>
#include <sstream>
#include <ctype.h>
#include <winuser.h>
#include <aclapi.h>
#include <shfolder.h>
#include <assert.h>
#include <tchar.h>
#include "toontownInstaller.h"
#include "urlencode.h"
#include "popup.h"
#include "strl.h"

#if defined(_INSTALLERSERVICE_) || defined(_EXEINSTALLER_)
#   include <vos/vos.hpp>
#   if defined(_INSTALLERSERVICE_)
#	    include <vos/proc.hpp>

#	    include <comdef.h>
#	    include "service/win32/installer_service.h"
#	    if !defined(USE_RPCINSTALLER)
            extern int sehISPROC_rforkexec(BSTR app_path, BSTR args, DWORD &procId, HANDLE procHandle);
            extern int sehISFILE_MakeGameDir(int game, BSTR deployment);
#	    endif
#   endif
#endif

// define this if we are loading flash files directly from the web;
// it saves the users from having to download the files twice
#define DONT_DOWNLOAD_FLASH_FILES

#define DISK_MEGS_REQUIRED 100
#define REQUIRED_RAM_MEGS  110

const unsigned int bytesPerMeg = (1<<20);

/*
static void DBG(const char *msg) {
  MessageBox(NULL, msg, "HI", MB_OK);
}
*/

#define PREVENT_HACKERS

// To recover from wrong logs
#define PRINT_TAIL_OF_ALL_LOGS

#define HIDE_LAUNCHER_EXTRACT
#define HIDE_LAUNCHER
//#define MINIMIZE_LAUNCHER
#define WRITE_ERROR_LOG
#ifndef _EXEINSTALLER_
#	define RECURSE_FOR_SPEED
#endif
//#define DONT_PATCH_JUST_REINSTALL

const char *Installer_ProgramName="Disney's Toontown Online";  // MUST match value set in launcher.wse
#define TOTAL_INSTALLEDSIZE 113355411   // just measured TT dirsize for 1.0.19.9, approximate is good enough 4 now

// these should always be enabled, unless you are dbging
//#define SEND_CONFIGINFO_TO_STATSERVER 1	// this isn't used anymore
#define RECORD_ALL_INSTALL_ERRORS 1

#if defined(USE_TESTSERVER)
// different names allow side-by-side installations
// we wont support concurrent running of test and release though
  #define TT_CONTROL_NAME "tt_test"
  #define TESTSERVER_STR "TestServer "
  #define TESTSTR "Test"
  #define PLAYSERVER "test"
  #define CMDARG_USE_TESTSERVER 1
  #define CMDARG_USE_TESTSERVER_STR "1"
#else
  #define TT_CONTROL_NAME "ttinst"
  #define TESTSERVER_STR ""
  #define TESTSTR ""
  #define PLAYSERVER "play"
  #define CMDARG_USE_TESTSERVER 0
  #define CMDARG_USE_TESTSERVER_STR "0"
#endif

// separate out builds by language releases also

#define _str(s) #s
#define _xstr(s) _str(s)

#if defined(USE_CASTILLIAN)
  #define TT_CONTROL_EXT "-castillian"
  #undef TESTSTR
  #define TESTSTR _xstr(PRODUCT_NAME)
#elif defined(USE_JAPANESE)
  #define TT_CONTROL_EXT "-japanese"
  #undef TESTSTR
  #define TESTSTR _xstr(PRODUCT_NAME)
#elif defined(USE_GERMAN)
  #define TT_CONTROL_EXT "-german"
  #undef TESTSTR
  #define TESTSTR _xstr(PRODUCT_NAME)
#elif defined(USE_PORTUGUESE)
  #define TT_CONTROL_EXT "-portuguese"
  #undef TESTSTR
  #define TESTSTR _xstr(PRODUCT_NAME)
#elif defined(USE_FRENCH)
  #define TT_CONTROL_EXT "-french"
  #undef TESTSTR
  #define TESTSTR _xstr(PRODUCT_NAME)
#else
  #define TT_CONTROL_EXT ""
#endif

#define TT_CONTROL_BASENAME TT_CONTROL_NAME TT_CONTROL_EXT

#define TT_HOMEPAGE "http://" PLAYSERVER ".toontown.com"
#if !defined(_EXEINSTALLER_)
	const char *tt_control_name = TT_CONTROL_BASENAME ".dll";
#endif

const char *TOONTOWN_INSTALLER_LOGBASENAME="Toontown" TESTSTR "Installer";
const char *ToontownInstallDirSubTree="\\Disney\\Disney Online\\Toontown" TESTSTR "\\";
const char *ToontownRegKeyName = "SOFTWARE\\Disney\\Disney Online\\Toontown" TESTSTR;  //under HKEY_CURRENT_USER
const char *ToontownHackers = "SOFTWARE\\WDIG\\TTO" TESTSTR; //To detect hackers who are hacking for free trials

#define RUNLAUNCHER_FILENAME "Toontown.exe"
#define GAMELOG_BASEFILENAME "toontown"

// installer_window_title MUST match <TITLE> of installer.php
static const char *toontown_window_title = "Toontown";   // MUST match title of panda window

// We need to get the following strings from the Java script now
#ifndef _EXEINSTALLER_
	static string installer_window_title(_T("Going to Toontown..."));
#else
	static string installer_window_title(_T("WDIG Launcher"));
#endif
static string missed_requirements_php;
static string graphics_driver_php;

static const char *launcherProcessEndedPrematurelyErr =
  "The Launcher process ended prematurely.";
static const char *launcherExtractProcessDiedErr =
  "Launcher installation failed.\nPlease reboot your computer and try again.";
static const char *gameCrashedErr =
  "The game exited unexpectedly and did not set an error code.  Please submit a bug report.";
const char *RestartIEInstrs="Please try closing all instances and windows of Internet Explorer, restarting the browser, "
                            "returning to http://" PLAYSERVER ".toontown.com and pressing the 'Play' button again.";

#define TOONTOWN_HKEY  HKEY_CURRENT_USER

static const char *pandaErrors[] = {
  "No Error",   // 0 == no error

  // 1
  "Unable to rewrite installed Toontown files.  You must have permission to modify the files in the Toontown directory in order to update so you can run the current version of Toontown.  Check your installed file permissions.",

  // 2
  "Unable to download new files into the Toontown directory.  Either you do not have permission to write to the Toontown directory, or you do not have enough available disk space.",

  // 3
  "You are connected to the internet via a proxy, and your proxy requires a username and password to connect.  Currently, Toontown does not support connecting via a password-secured proxy.  You must disable this feature, or disconnect your proxy, in order to play Toontown.",

  // 4
  "Toontown.exe was unable to contact the Toontown download server outside Internet Explorer.  Most likely, the connection was prevented by some personal firewall software, such as Norton Personal Firewall, McAfee Firewall, BlackICE PC Protection, ZoneAlarm, or Microsoft WinXP Internet Connection Firewall.  If you have a personal firewall program such as any of these (or any similar product) installed, please ensure it is configured to allow Toontown.exe to make connections to the internet. For common firewall configurations, please click<a href=\"http://play.toontown.com/firewallConfig.php\"> here./a>",

  // 5
  //"Unable to locate the current version of the Toontown files to download.  There may be a problem with files being cached on the internet.",
  // this indicates a configrc.exe error
  "Unable to locate the current version of the Toontown files to download.  There may be a problem with files being cached on the internet. Uninstalling Toontown and redownloading may also help fix this problem.",

  // 6
  "There appears to be a problem downloading the latest version of Toontown. If you are connecting to the internet via a proxy, it may be a problem with your proxy. If you are not connecting through a proxy, it is possible that the Toontown servers are temporarily unavailable. Please try to connect again.",

  // 7
  "Unable to open a graphics window.  Make sure you have the latest drivers installed from your 3-D graphics card vendor.  If you have previously run Toontown successfully and are unable to run now, it may help to restart your computer.",

  // 8--no longer used.
  NULL,

  // 9
  "You are connecting to the internet via a proxy, and for some reason your proxy has disallowed the download request.  There may be an unusual configuration requirement with your proxy that Toontown does not understand.  It may help to disable your proxy if possible.",

  // 10
  "Toontown was unable to start its configuration program, Configrc.exe.  Perhaps you have some firewall security software, such as Norton Personal Firewall, McAfee Firewall, BlackICE PC Protection, or ZoneAlarm, configured to prevent applications like Toontown from starting other programs.  Try disabling this software if you have it installed.",

  // 11: the game got started ok, but then exited without setting an
  // error code.  This means something below the Python level shut the
  // program down, without giving Python a chance to catch it and
  // clean up.
  "The game was terminated unexpectedly because of some external problem. \n<br> It is difficult to tell what happened, but it may have been a crash in your graphics driver.\n<br>Please ensure that you have installed the latest drivers from your 3-D graphics card manufacturer.",

  // 12: the game halted with a Python exception.
  "The game encountered an unexpected condition and was forced to exit suddenly.  Please follow the instructions below to submit a bug report so we can fix this problem in the future.\n<br><br>When you have finished submitting the bug report, you can press the red \"Play\" button to go back into the game.",

  // 13: the server rejected our connection.
  "The Toontown game server is available, but did not allow you connect.  Usually this happens only when your version of the Toontown software is out of date and requires an update.  Normally, the update happens automatically when you press the red \"Play\" button, so something must have gone wrong.  Try refreshing your browser page and pressing the Play button again.",

  // 14: the graphics went haywire.
  "The game is unable to function graphics operation. \n<br>Most probable cause is problem with graphics card driver. \n<br>Please ensure that you have installed the latest driver from your 3D graphics card manufacturer.",

  // 15: the launcher files didn't pass the hash.
  "You seem to have an out-of-date version of Toontown installed.  Normally, when you press the red \"Play\" button, this should automatically update, but something must have gone wrong.  Make sure you are not already running Toontown in another window, and try pressing the Play button again.",
};
static const int numPandaErrors = sizeof(pandaErrors) / sizeof(const char *);

#if !defined(USE_RPCINSTALLER)

// string constants
const char *toontownInstaller::_INSTALL_DIR_ValueName        = "INSTALL_DIR";
const char *toontownInstaller::_LAUNCHER_EXTRACTED_ValueName = "LAUNCHER_EXTRACTED";
const char *toontownInstaller::_PERCENT_LOADED_ValueName     = "PERCENT_PHASE_COMPLETE_3";
const char *toontownInstaller::_PERCENT_OVERALL_LOADED_ValueName = "PERCENT_OVERALL_COMPLETE";
const char *toontownInstaller::_LAUNCHER_MESSAGE_ValueName   = "LAUNCHER_MESSAGE";
const char *toontownInstaller::_PANDA_WINDOW_OPEN_ValueName  = "PANDA_WINDOW_OPEN";
const char *toontownInstaller::_PANDA_ERROR_CODE_ValueName   = "PANDA_ERROR_CODE";
const char *toontownInstaller::_GREEN_ValueName              = "TOONTOWN_GREEN";
const char *toontownInstaller::_BLUE_ValueName               = "TOONTOWN_BLUE";
const char *toontownInstaller::_PLAYTOKEN_ValueName          = "TOONTOWN_PLAYTOKEN";
const char *toontownInstaller::_LAST_LOGIN_ValueName         = "LAST_LOGIN";
const char *toontownInstaller::_GAME2_DONE_ValueName         = "GAME2_DONE";
#ifndef _EXEINSTALLER_
	const char *toontownInstaller::_GAME1_VERSION_ValueName      = "GAME1_VERSION";
	const char *toontownInstaller::_MOVIE_VERSION_ValueName      = "MOVIE_VERSION";
	const char *toontownInstaller::_GAME2_VERSION_ValueName      = "GAME2_VERSION";
	const char *toontownInstaller::_MESSAGES_VERSION_ValueName   = "MESSAGES_VERSION";
	const char *toontownInstaller::_TOONTUNE_VERSION_ValueName   = "TOONTUNE_VERSION";
#endif
const char *toontownInstaller::_PROXY_SERVER_ValueName       = "PROXY_SERVER";
const char *toontownInstaller::_PROXY_DIRECT_HOSTS_ValueName = "PROXY_DIRECT_HOSTS";
const char *toontownInstaller::_PROXY_USER_ValueName         = "PROXY_USER";
const char *toontownInstaller::_PROXY_PASSWORD_ValueName     = "PROXY_PW";
const char *toontownInstaller::_USER_LOGGED_IN_ValueName     = "USER_LOGGED_IN";
const char *toontownInstaller::_PAID_USER_LOGGED_IN_ValueName= "PAID_USER_LOGGED_IN";
const char *toontownInstaller::_EXIT_PAGE_ValueName          = "EXIT_PAGE";
const char *toontownInstaller::_REFERRER_CODE_ValueName      = "REFERRER_CODE";
const char *toontownInstaller::_PREVENT_HACKERS_ValueName    = "BLOB";
const char *toontownInstaller::_PREVENT_HACKERS_ValueName2   = "BLOB2";
const char *toontownInstaller::_CHAT_ELIGIBLE_ValueName      = "CHATTERBOX"; // Deprecated
const char *toontownInstaller::_WEB_ACCT_PARAMS_ValueName    = "WEB_ACCT_PARAMS"; //new registry to record all chat related params
const char *toontownInstaller::_PATCH_FROM_CD_ValueName      = "FROM_CD";
const char *toontownInstaller::_CDROM_ValueName              = "CDROM_INSTALLATION";
const char *toontownInstaller::_DOWNLOAD_SERVER_ValueName    = "DOWNLOAD_SERVER";
const char *toontownInstaller::_GAMELOG_FILENAME_ValueName   = "GAMELOG_FILENAME";
const char *toontownInstaller::_DEPLOYMENT_ValueName         = "DEPLOYMENT";

// had to add '_' at the end due to erronenous testserver writes of the original name to client
const char *toontownInstaller::_configSubmitApprovedRegValName = "ConfigSubmitApproved_";

toontownInstaller::
toontownInstaller(void)
{
#ifndef _EXEINSTALLER_
	_game1_IFilename = "game1.swf";
	_movie_IFilename = "movie.swf";
	_game2_IFilename = "game2.swf";
	_messages_IFilename = "messages.swf";
	_toontune_IFilename = "toon_tune.swf";
#endif

    _initialized = 0;
    _reg_initialized = 0;
    _StateCode = 0;
    _pSysInfo=NULL;
    _bDoConfigInfoCollection = false;
    _bConfigSubmitApproved = false;
    _DiskSpace_Megs_Free = 0.0f;
    _bHTTPproxyIsUsed = false;

    _FinalNonErrorState = 0;
    _InstallerErrorPoint = 0;
    _LastPandaErrorCode = 0;  // -1 indicates registry entry doesnt exist

    _runLauncher_IFilename.setBaseName(RUNLAUNCHER_FILENAME);

    _installer_hwnd = NULL;

    // get a few more samples at the start before maxing out
    #define START_MEMCHECK_INTERVAL_SEC 20
    #define MAX_MEMCHECK_INTERVAL_SEC 360
    #define MEMCHECK_INTERVAL_INC 10
    _cur_memcheck_interval = START_MEMCHECK_INTERVAL_SEC;
    _lastmemcheck_time = 0;
    memset(&_liActiveXVersion,0,sizeof(_liActiveXVersion));
    memset(&_liActiveXVerReqd,0xFF,sizeof(_liActiveXVerReqd));

    char installer_logbasename[_MAX_PATH];
    char full_installer_logname[_MAX_PATH];

    // this only figures out what the log filename will be, it doesnt create the file, since we only
    // want to do that for TT runs, not bug reports

    // avoid sharing violations by giving each log a unique name
    sprintf(installer_logbasename,"%s-%s.log",TOONTOWN_INSTALLER_LOGBASENAME,_logSuffix.c_str());
    _installerLogFile_IFilename.setBaseName(installer_logbasename);
    makeFilenameInTempDir(full_installer_logname,installer_logbasename);
    _installerLogFile_IFilename.setFullLocalName(full_installer_logname);

    //DBG(installer_logbasename);

    char tmppath[_MAX_PATH],fulllogpathpattern[_MAX_PATH];
    // get path where logs are to be stored to determine log path pattern
    strcpy(tmppath,_installerLogFile_IFilename.getFullLocalName());
    char *pLastSlash=strrchr(tmppath,'\\');
    *pLastSlash='\0';

    // delete any old-style named logs that may exist
    sprintf(installer_logbasename,"%s\\%s.log",tmppath,TOONTOWN_INSTALLER_LOGBASENAME);
    deleteObsoleteFile(installer_logbasename);

    sprintf(fulllogpathpattern,"%s\\%s-*.log",tmppath,TOONTOWN_INSTALLER_LOGBASENAME);
    _installerLogPathPattern=fulllogpathpattern;
}

toontownInstaller::
~toontownInstaller(void) {
  if(_pSysInfo!=NULL) {
    delete _pSysInfo;
    _pSysInfo=NULL;
  }

  shutdown();
}

#define NUM_LOGS_TO_KEEP 5

// deletes any logs more than NUM_LOGS_TO_KEEP on disk
void toontownInstaller::
deleteOldLogs(const char *logPathPattern)
{
  StrVec LogFiles;
  getAllFilesWithPathPattern(logPathPattern,LogFiles);

  int numtodelete = LogFiles.size() - NUM_LOGS_TO_KEEP;

  if(numtodelete <= 0)
      return;

  //should be sorted oldest first due to logfilename suffix convention, so just delete the first ones

  for(int i = 0; i < numtodelete; i++)
      (void) deleteFile(LogFiles[i].c_str());
}

int toontownInstaller::
init() {
  _SWID_String[0]='\0';
  _DOWNLOAD_SERVER_String[0]='\0';
  _GAME_SERVER_String[0]='\0';
  _ACCOUNT_SERVER_String[0]='\0';
  _downloadServerURL[0]='\0';
  _downloadVersion[0]='\0';
  _downloadRootURL[0]='\0';
  _configrc_args.clear();
  int retval = 0;

  _installer_hwnd = NULL;

//  modifying process Dacl didnt seem to change new file permissions
//  if(SysInfo::get_os_type() >= SysInfo::OS_WinNT) {
//     extern bool ModifyDefaultDacl(void);
//      if(!ModifyDefaultDacl())
//          retval =1;
/*
      HANDLE TokenHandle;
      if(!OpenProcessToken(GetCurrentProcess(),TOKEN_ADJUST_DEFAULT,&TokenHandle)) {
          ShowOSErrorMessageBox("OpenProcessToken");
          return 1;
      }

      if(!SetTokenInformation(TokenHandle,TokenDefaultDacl,NULL,0)) {
          ShowOSErrorMessageBox("SetTokenInfo");
          retval=1;
      }

      CloseHandle(TokenHandle);
*/
//  }

  return retval;
}

bool toontownInstaller::
store_encoded_time(void) {
#if 0
  // comment out until we decide how Launcher.py will detect this, since
  // it doesnt have toontown.dll immediately available.  also need
  // to encode our process ID


  #define MAGIC_REGVALUENAME "L"
  #define MAGIC_BUFSIZE 16

  HKEY hKey = NULL;
  ULONG regResult = RegOpenKeyEx(TOONTOWN_HKEY,ToontownRegKeyName,
                                 0x0,KEY_SET_VALUE,&hKey);
  if(ERROR_SUCCESS != regResult)
      return false;

  time_t cur_time;
  time(&cur_time);
  srand( (unsigned)cur_time);

  BYTE buf[MAGIC_BUFSIZE];
  // mix some random garbage in with the encoded time bytes
  for(int i=0;i<sizeof(buf);i++)
      buf[i]=(BYTE)rand();

  buf[3]  = (BYTE) (((cur_time >> 24) & 0xFF) ^ 0x55);
  buf[7]  = (BYTE) (((cur_time >> 16) & 0xFF) ^ 0x99);
  buf[9]  = (BYTE) (((cur_time >>  8) & 0xFF) ^ 0xF1);
  buf[14] = (BYTE) (((cur_time >>  0) & 0xFF) ^ 0xA3);

  regResult=RegSetValueEx(hKey,MAGIC_REGVALUENAME,0x0,REG_BINARY,buf,sizeof(buf));
  RegCloseKey(hKey);
  return (ERROR_SUCCESS == regResult);
#else
  return true;
#endif
}

// stores ptrs we need to free l8r all together
struct MySecurAttrib {
    PACL pACL;
    PSID pEveryoneSID;
    PSECURITY_DESCRIPTOR pSD;
    PSECURITY_ATTRIBUTES pSA;
};


// security entry points seem to be on win9x advapi32.dll though they may not be
// functional, so should be ok to statically link to InitializeSecurityDescriptor, etc

// use for reg and file system
MySecurAttrib *makeGlobalRW_SecAttr(void)
{
    DWORD dwRes;
    EXPLICIT_ACCESS ea;
    SID_IDENTIFIER_AUTHORITY SIDAuthWorld = SECURITY_WORLD_SID_AUTHORITY;
    PACL pACL=NULL;
    PSID pEveryoneSID=NULL;
    PSECURITY_DESCRIPTOR pSD=NULL;
    HKEY hkSub = NULL;
    char *errstr=NULL;
    SECURITY_ATTRIBUTES *pSA = NULL;
    MySecurAttrib *pMySecurAttr = NULL;

    // Create a well-known SID for the Everyone group.

    if(!AllocateAndInitializeSid( &SIDAuthWorld, 1,
                     SECURITY_WORLD_RID,
                     0, 0, 0, 0, 0, 0, 0,
                     &pEveryoneSID) ) {
        errstr = "AllocateAndInitializeSid";
        goto Cleanup;
    }

    // Initialize an EXPLICIT_ACCESS structure for an ACE.
    // The ACE will allow Everyone read access to the key.

    memset(&ea, 0, sizeof(EXPLICIT_ACCESS));
    ea.grfAccessPermissions = KEY_ALL_ACCESS;
    ea.grfAccessMode = SET_ACCESS;
    ea.grfInheritance= NO_INHERITANCE;
    ea.Trustee.TrusteeForm = TRUSTEE_IS_SID;
    ea.Trustee.TrusteeType = TRUSTEE_IS_WELL_KNOWN_GROUP;
    ea.Trustee.ptstrName  = (LPTSTR) pEveryoneSID;

    // Create a new ACL that contains the new ACEs.

    dwRes = SetEntriesInAcl(1, &ea, NULL, &pACL);
    if (ERROR_SUCCESS != dwRes) {
        errstr = "SetEntriesInAcl";
        goto Cleanup;
    }

    // Initialize a security descriptor.

    pSD = (PSECURITY_DESCRIPTOR) LocalAlloc(LPTR, SECURITY_DESCRIPTOR_MIN_LENGTH);
    if (pSD == NULL) {
        errstr = "LocalAlloc";
        goto Cleanup;
    }

    if (!InitializeSecurityDescriptor(pSD, SECURITY_DESCRIPTOR_REVISION)) {
        errstr = "InitializeSecurityDescriptor";
        goto Cleanup;
    }

    // Add the ACL to the security descriptor.

    if (!SetSecurityDescriptorDacl(pSD,
            true,     // fDaclPresent flag
//            pACL,
            NULL,
            false))   // not a default DACL
    {
        errstr = "InitializeSecurityDescriptor";
        goto Cleanup;
    }

    pSA = new SECURITY_ATTRIBUTES;
    pSA->nLength = sizeof(SECURITY_ATTRIBUTES);
    pSA->bInheritHandle = true;
    pSA->lpSecurityDescriptor = pSD;


    pMySecurAttr = new MySecurAttrib;
    if(!pMySecurAttr)
        goto Cleanup;

    pMySecurAttr->pSA=pSA;
    pMySecurAttr->pACL=pACL;
    pMySecurAttr->pEveryoneSID=pEveryoneSID;
    pMySecurAttr->pSD=pSD;

    return pMySecurAttr;

Cleanup:
    if (pEveryoneSID)
        FreeSid(pEveryoneSID);
    if (pACL)
        LocalFree(pACL);
    if (pSD)
        LocalFree(pSD);
    if (pSA)
      delete pSA;

    /*
    // not sure how to handle this error.  just note it in the log for now.
    // has occurred on non-english xp, not sure if language has anything to do with it,
    // or could be some domain config the user is in
    if(GetLastError()==ERROR_NONE_MAPPED) {
//    if(vos::last_error_code()==ERROR_NONE_MAPPED) {
        errorLog << errstr << " returned ERROR_NONE_MAPPED!\n";
    } else */
    LogOSErrorMessage(errstr);
    return NULL;
}

void free_MySecAttr(MySecurAttrib *pMySA) {
    if(!pMySA)
        return;

    if (pMySA->pEveryoneSID)
        FreeSid(pMySA->pEveryoneSID);
    if (pMySA->pACL)
        LocalFree(pMySA->pACL);
    if (pMySA->pSD)
        LocalFree(pMySA->pSD);
    if (pMySA->pSA)
        delete pMySA->pSA;
    delete pMySA;
}

bool toontownInstaller::
GetInstallerVersion(ULARGE_INTEGER &Ver)
{
#ifndef _EXEINSTALLER_
   char activeXcontrol_filename[_MAX_PATH], activeXcontrol_filepath[_MAX_PATH];

   memset(&Ver,0, sizeof(Ver));

   // Get full path to std activeX control dir, so we can get file version
   registryKey internetSettings;
   if (internetSettings.openRO(TOONTOWN_HKEY, InternetSettingsRegKey) == NULL) {
     return false;
   }

   if(0 != internetSettings.getString(ActiveXCache_RegValName, activeXcontrol_filepath, sizeof(activeXcontrol_filepath))) {
     return false;
   }
   internetSettings.closeKey();

   _ActiveXFilePath = activeXcontrol_filepath;

#ifdef OLDWAY
   // this may not be accurate if 'CONFLICT' dirs exist in downlo~1 due to same filenames.
   // better to get info directly from OS using GetModuleFilename

   strcpy(activeXcontrol_filename,activeXcontrol_filepath);
   strcat(activeXcontrol_filename,"\\");
   strcat(activeXcontrol_filename,tt_control_name);
#else
   HMODULE hMod = GetOurModuleHandle();

   if(hMod==NULL) {
       errorLog << "GetOurModuleHandle failed, err=" << GetLastErrorStr() << endl;
//       errorLog << "GetOurModuleHandle failed, err=" << vos_os::last_error_str() << endl;
       return false;
   }

   if(GetModuleFileName(hMod,activeXcontrol_filename,_MAX_PATH)==0) {
       errorLog << "GetModuleFileName failed, err=" << GetLastErrorStr() << endl;
//       errorLog << "GetModuleFileName failed, err=" << vos_os::last_error_str() << endl;
       return false;
   }
#endif

#if 0
   // the file name could be wrong if there are conflict.1 dirs
   //   errorLog << "Retrieving version of module " << activeXcontrol_filename << endl;
   //   MyGetFileVersion(activeXcontrol_filename, NULL, &Ver);
#elif 0

//   MyGetModuleVersion(hMod, &Ver);  got a bug where it returns 0.0.0.0!  arggh.
#else
   errorLog << "Looking for installer module " << activeXcontrol_filename << endl;
   GetHardCodedVersion(Ver);
#endif

#endif // _EXEINSTALLER_

   return true;
}

bool toontownInstaller::
CheckInstallerVersionNum(void)
{
#ifndef _EXEINSTALLER_
    bool bValidVersion=false;
    bool bFoundVerNum=false;

    if((_liActiveXVerReqd.HighPart==0xFFFFFFFF)&&(_liActiveXVerReqd.HighPart==0xFFFFFFFF)) {
        // _liActiveXVerReqd not initialized so return true,  not sure why returning true for this case, but this is what is used to do.
        return true;
    }

    StrVec conflict_dirlist;

    // look for 'CONFLICT.[x]' dirs
    filesearch(_ActiveXFilePath, "*", true, true, false, conflict_dirlist);

    if(conflict_dirlist.size()>0) {
        StrVec control_filelist;

        // print out info on all controls to log for dbg purposes
        filesearch(_ActiveXFilePath, TT_CONTROL_BASENAME "*.dll", true, false, true, control_filelist);

        if(control_filelist.size()>1) {
            errorLog << "Found duplicate installers in the following list:\n";
            for(unsigned i=0;i<control_filelist.size();i++) {
                errorLog << control_filelist[i] << endl;
            }
        }
    }

    if(LARGEINT_EQUAL(_liActiveXVersion,_liActiveXVerReqd))
        return true;

    char activeXshortpath[_MAX_PATH];
    GetShortPathName(_ActiveXFilePath.c_str(),activeXshortpath,_MAX_PATH);
    errorLog << "Bad Installer Version "<<PRINTDRIVER_VERSTR(_liActiveXVersion) << "!  Required version is: " << PRINTDRIVER_VERSTR(_liActiveXVerReqd) << endl;

#ifndef BLOCK_OLD_INSTALLER_VERSIONS
    // pop up a MessageBox here to allow user to cancel and try to remove and force install manually?
    // could have an option to not repeat the popup until the next required-version update (store the last reqd version in registry)
    errorLog << "continuing with incorrect version anyway...\n";
    return true;
#else
    // otherwise need to print errors and suggestions

    char proxymsg[1024];
    if(!_proxyServerURL.empty()) {
        sprintf(proxymsg,"\n\nYou are connected to the internet through an HTTP proxy server (%s), " \
         "which could be caching an old version of the activeX control, which would prevent you from downloading the latest " \
         "version.  If following the above procedure does not work, try refreshing " TT_HOMEPAGE " additional times; " \
         "most proxy servers will update their cached copies within seconds or minutes, but some can take hours.",
         _proxyServerURL.c_str());
    } else {
        proxymsg[0]='\0';
    }

    char msg[3048];
    sprintf(msg,"Toontown cannot start because you have an obsolete version (%d.%d.%d.%d) of the Toontown " \
            TESTSERVER_STR "ActiveX Installer.   Version %d.%d.%d.%d is required and should have been downloaded " \
            "automatically by the Internet Explorer browser.  Try first closing all open Internet Explorer browser windows, " \
            "then manually removing the old installer by clicking on Start->Run, typing '%s', right-clicking on 'Toontown " TESTSERVER_STR "Installer " \
            "ActiveX Control' and selecting 'Remove' to force a new one to be downloaded. Then open Internet Explorer, " \
            "return to http://" PLAYSERVER ".toontown.com and press 'Play' again.  Since Internet Explorer should not be open " \
            "to this page while you are removing the Installer, you may need to cut-and-paste these instructions to a notepad window.  To do this," \
            "use Start button->Run, type 'notepad', then highlight this text with the left mouse button, press Control-C, then go to "
            "the notepad window and press Control-V to paste this text into the new window.%s",
            HIWORD(_liActiveXVersion.HighPart),LOWORD(_liActiveXVersion.HighPart),HIWORD(_liActiveXVersion.LowPart),LOWORD(_liActiveXVersion.LowPart),
            HIWORD(_liActiveXVerReqd.HighPart),LOWORD(_liActiveXVerReqd.HighPart),HIWORD(_liActiveXVerReqd.LowPart),LOWORD(_liActiveXVerReqd.LowPart),
            activeXshortpath, proxymsg);
    addUserErrorAndLog(msg);
    return false;
#endif
#else
  return true;
#endif // _EXEINSTALLER_
}

// some of this is project-independent
// - error log?
// CALL THIS IF YOU'RE GOING TO BE RUNNING THE GAME NORMALLY;
// WILL OVERWRITE THE LOG FILE
// returns true on success
#ifndef _INSTALLERSERVICE_
bool toontownInstaller::normalInit(const HWND browser_hwnd)
#else
bool toontownInstaller::
normalInit(const HWND browser_hwnd, const TCHAR *deployment, const TCHAR *downloadServer, const TCHAR *downloadVersion)
#endif
{
  static bool bAlreadyInsideNormalInit = false;
  bool retval = false;

  // prevent infinite recursion -- if we're already inside this function, return success
  if(bAlreadyInsideNormalInit)
    return true;

  if(_initialized) {
    bAlreadyInsideNormalInit=false;  // mimicking behavior that was working before.  is this necessary?
    return true;
  }

  // we are now inside the function mutex
  bAlreadyInsideNormalInit = true;

  if (browser_hwnd != NULL) _installer_hwnd = browser_hwnd;
#if defined(_INSTALLERSERVICE_)
  if (deployment != NULL) Deployment(deployment);
  if (downloadServer != NULL) DownloadServer(downloadServer, true);
  if (downloadVersion != NULL) DownloadVersion(downloadVersion);
#endif

  // until I implement disjoint lognames, most likely wont be able to open log if another TT is running, so
  // this check comes before then
  if(ProgramIsRunning("Toontown")) {
    /*
      MessageBox( NULL, "Toontown appears to be already running on your computer.  Before you can start the game again, "
      "please close all other Toontown windows and End/Close any instances of the 'Toontown.exe' process "
      "you see in the Windows Task Manager (accessible by pressing Ctrl-Alt-Delete)",
      "Toontown Installer Error", MB_OK | MB_ICONWARNING );
    */
    ShowLocalizedMessage("TIE_Toontown_Running");
    goto _return;
  }

#ifdef WRITE_ERROR_LOG
  {
    // start logging
    // each log file logs a single run

#if defined(_INSTALLERSERVICE_) || defined(USE_RPCSERVICE) || defined(_EXEINSTALLER_)
//	if (vos::errorlog_status())
    if (0)
#else
    if (openLogFile(_installerLogFile_IFilename.getFullLocalName()))
#endif
	{
      char msg[1024];
      sprintf(msg,"The Toontown installer couldn't create a new log file '%s'. %s",
              _installerLogFile_IFilename.getFullLocalName(),RestartIEInstrs);
      MessageBox( NULL, msg, "Toontown Installer Error", MB_OK | MB_ICONWARNING );
      goto _return;
    }

    // output date and time

    char tempstr[128];

    _strdate(tempstr);
    errorLog << "[" << tempstr;
    _strtime(tempstr);
    errorLog << " - " << tempstr << "]";
    errorLog << endl;
  }
#endif

#if defined(_EXEINSTALLER_) && 0
  if(ActiveXVersionToCheckFor!=NULL) {
    // ActiveXVersionToCheckFor should be string like this "1,0,8,9"
    unsigned int a,b,c,d;
    int result = sscanf(ActiveXVersionToCheckFor,"%d,%d,%d,%d",&a,&b,&c,&d);
    if (result == EOF) {
      // i.e. an empty string.
      errorLog
        << "No particular installer version specified.\n";

    } else if (result != 4) {
      // Some invalid character in the string.
      errorLog
        << "Invalid installer version specified: '"
        << ActiveXVersionToCheckFor << "'\n";

    } else {
      _liActiveXVerReqd.HighPart = (a<<16) | b;
      _liActiveXVerReqd.LowPart =  (c<<16) | d;
    }
  }

  if (GetInstallerVersion(_liActiveXVersion))
      errorLog << "Initializing installer version " << PRINTDRIVER_VERSTR(_liActiveXVersion) << endl;
  else
      errorLog << "Couldnt get installer version!\n";
#endif
  errorLog << "built: " << __DATE__ << ' ' << __TIME__ << endl;

  _StateCode = 0;
  _curDownloadThreadHandle = NULL;

#ifndef _EXEINSTALLER_
  // flash version variables
  _game1Version[0]='\0';
  _movieVersion[0]='\0';
  _game2Version[0]='\0';
  _messagesVersion[0]='\0';
  _toontuneVersion[0]='\0';
  _needToDownloadGame1 = 0;
  _needToDownloadMovie = 0;
  _needToDownloadGame2 = 0;
  _needToDownloadMessages = 0;
  _needToDownloadToontune = 0;

  _game1_Done = 0;
#endif

  _launcherInvalidCount = 0;
  _hInstallLauncherProcess = NULL;
  _LauncherProcessID = 0;
  _hLauncherProcess = NULL;
  _LauncherDownloadTryNum = 0;
  _OK_To_Kill_LauncherProcess = 0;

  if (regInit()) {
    errorLog << "Error opening registry" << endl;
    SysInfo::print_os_info();

    if((_pSysInfo->get_os_type() >= SysInfo::OS_WinNT)&&(!_pSysInfo->IsNTAdmin())) {
      addUserErrorAndLog("The Toontown Installer could not write to the Toontown area of "
                         "the Windows registry because the user does not have Administrator permissions. "
                         "Please have a user with Administrator permissions press 'Play' to install the game and/or "
                         "perform the required game software update.  After that non-Administrative accounts "
                         "should be able to play.");
    }
    retval = false;
    goto _return;
  }

  // remove some keys from the registry
  _regToontown.deleteValue(_PATCH_FROM_CD_ValueName);
  initOverallPercentLoaded();

  DWORD tmpConfigSubmitApproved = _regToontown.getDWORD(_configSubmitApprovedRegValName);
  _bConfigSubmitApproved = (tmpConfigSubmitApproved != 0);

  _initialized = 1;
  retval = true;

 _return:
  printSeparator();
  // reset the "inside" flag, since we're leaving the function
  bAlreadyInsideNormalInit = false;
  return retval;
}

// some of this is project-independent
// - killing the launcher
// - freeing the database
// etc.
void toontownInstaller::
shutdown() {
  if (!_initialized) {
    errorLog << "toontownInstaller::shutdown() called in non-initialized state" << endl;
    return;
  }

  // show the final statecode message
  _StateCode = INVALID_STATECODE;
  printStateCodeUpdates();

  printSeparator();
  errorLog << "Installer is shutting down..." << endl;

  // kill the launcher if necessary
  if(_OK_To_Kill_LauncherProcess && _hLauncherProcess) {
    if(processActive(_hLauncherProcess)) {
      errorLog << "Terminating launcher process..." << endl;
      if(0 == TerminateProcess(_hLauncherProcess, 0)) {
        errorLog << "Error terminating launcher process" << endl;
      }
    }
    _OK_To_Kill_LauncherProcess = 0;
    _hLauncherProcess = NULL;
  }
  else {
    errorLog << "Launcher process not active, no need to terminate it" << endl;
    if(_OK_To_Kill_LauncherProcess) {
      errorLog << "BUT _OK_To_Kill_LauncherProcess is non-NULL" << endl;
    }
    if(_hLauncherProcess) {
      errorLog << "BUT _hLauncherProcess is non-NULL" << endl;
    }
  }

  _launcherFileDB.freeDatabase();
  _launcherDDBFile.freeDatabase();
  regShutdown();
  errorLog.close();
  _initialized = 0;
}

void toontownInstaller::
printStateCodeUpdates() {
  // keep the log file size under control;
  // don't spew out redundant statecode statements
  static int last_stateCode = INVALID_STATECODE;
  static int rep_count = 0;

  if (_StateCode != last_stateCode) {
    if (last_stateCode != INVALID_STATECODE) {
      if (rep_count > 1) {
        errorLog << "STATECODE: " << last_stateCode <<
                    " -> " << rep_count << " reps" << endl;
      }
    }
    if (_StateCode != INVALID_STATECODE) {
      printSeparator();
      errorLog << "STATECODE: " << dec << _StateCode << endl;
    }
    rep_count = 0;
    last_stateCode = _StateCode;
  }
  rep_count++;
}

void toontownInstaller::
setErrorState(unsigned int ErrorState, InstallerErrorPoint errpnt) {
  _FinalNonErrorState = _StateCode;	// save for stat reporting purposes
  _InstallerErrorPoint = errpnt;	// would be simpler to just always pass in __LINE__, but those change as file changes
  _StateCode = ErrorState;
  errorLog << "Final Non-ErrorState: " << _FinalNonErrorState << ", Installer ErrorPnt: " << errpnt << ", Panda ErrorCode: " << _LastPandaErrorCode << endl;

  // Any error, we want to make sure that installer window is ready
  reFocusWindow(_installer_hwnd, SW_RESTORE);

#if defined(SEND_CONFIGINFO_TO_STATSERVER) && defined(RECORD_ALL_INSTALL_ERRORS)
  if(_bConfigSubmitApproved) {
      // lets record install errors and as much config info as we have so far
      CreateConfigInfoRecord();

      // eventually hope to add this for consenting release server users too
      SendConfigRecord();
  }
#endif
}
//
// This function finds the window handle given the window title and changes its
// focus by the given nCmdShow parameter
//

inline void toontownInstaller::
reFocusWindow(const HWND hwnd, const int nCmdShow)
{
	TCHAR buffer[MAX_PATH];

	if (GetWindowText(hwnd, buffer, MAX_PATH - 1))
		errorLog
#if defined(_INSTALLERSERVICE_)
            <<vos::datestamp()
#endif
            <<hex<<hwnd<<':'<<buffer;
	if (GetClassName(hwnd, buffer, MAX_PATH - 1))
		errorLog << " is an "<<buffer;
#if defined(_DEBUG)
	errorLog << "; performing " << nCmdShow;
#endif
	errorLog << endl;

#if !defined(_INSTALLERSERVICE_)
	ShowWindow(hwnd, nCmdShow);
#else
	ShowWindowAsync(hwnd, nCmdShow);
#endif
}
void toontownInstaller::
reFocusWindow(const char *window_title, const int nCmdShow)
{
  // minimize fullscreen window (couldnt find a way to do this in javascript in installer.htm)
	HWND hWnd = NULL;
    // this is unreliable if window_title isn't accurate
	if (window_title && _tcsclen(window_title))
		hWnd = FindWindow(NULL, window_title);
	else
		window_title = "";

	if (hWnd == NULL)
	{
		errorLog << "Couldn't find window '" << window_title << "' to min/maximize it, error=" << GetLastErrorStr() << endl;
	//    errorLog << "Couldn't find window '" << window_title << "' to min/maximize it, error=" << vos::last_error_str() << endl;
	}
	errorLog << "Trying with window '"<<window_title<<':'<<hWnd<<"' to min/maximize it" << endl;

    reFocusWindow(hWnd, nCmdShow);

  /*
  WINDOWPLACEMENT wpmt;
  memset(&wpmt, 0,sizeof(wpmt));
  wpmt.length=sizeof(wpmt);
  if(!GetWindowPlacement(hWnd,&wpmt)) {
    errorLog << "GetWindowPlacement failed for window '" << window_title << "', error=" << GetLastErrorStr() << endl;
//    errorLog << "GetWindowPlacement failed for window '" << window_title << "', error=" << vos::last_error_str() << endl;
    return;
  }
  wpmt.showCmd=nCmdShow;  // make sure it's not activated (as would happen w/ShowWindow), or desktop will appear
  if(!SetWindowPlacement(hWnd,&wpmt)) {
    errorLog << "SetWindowPlacement failed for window '" << window_title << "', error=" << GetLastErrorStr() << endl;
//    errorLog << "SetWindowPlacement failed for window '" << window_title << "', error=" << vos::last_error_str() << endl;
  }
  */
}
//
// This function re-extracts the InstallLauncher to retrieve some files
//
void toontownInstaller::
extractLauncher()
{
  if(startLauncherSelfExtract()) {
    errorLog << "Error extracting launcher" << endl;
    setErrorState(13, E22);
	return;
  }
  // wait for self-extract to complete
  _StateCode = 60;
}
//
//
//
void toontownInstaller::
handleCase0() {
  if (!normalInit()) {
    errorLog << "Error initializing installer." << endl;
    setErrorState(13,E1);
    return;
  }

  // choose a server from list since we SHOULD now have complete URL components
  selectDownloadServer();
  // check for valid hardware
  errorLog << "Checking for valid hardware..." << endl;
  if (!validHardware()) {
    errorLog << "Invalid hardware detected" << endl;
    setErrorState(21,E2);
    return;
  }
  // check for proxy server
  checkProxyServer();

  // proxy could cause installer version problems, so make sure that info is printed to log before crashing out
  if(!CheckInstallerVersionNum()) {
    setErrorState(13,E3);
    return;
  }
#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  // initialize Panda3D install directory
  errorLog << "Setting up in Panda3D install directory..." << endl;
  if (createPanda3DInstallDir()) {
    errorLog << "Error setting up in Panda3D install directory";
    setErrorState(13,E4);
    return;
  }
  errorLog << "Set up in " << getPanda3DInstallDir() << endl;
#endif

  // initialize Toontown install directory
  errorLog << "Setting up in Toontown directory..." << endl;
  if (!initInstallDir()) {
    errorLog << "Error setting up in install directory";
    setErrorState(13, E5);
    return;
  }
  errorLog << "Set up in " << _toontownInstallDir << endl;

  // check for disk space
  errorLog << "Checking for necessary disk space..." << endl;
  bool sufficient=false;
  if (!sufficientDiskSpace(
	  _toontownInstallDir,
	  unsigned __int64(DISK_MEGS_REQUIRED)*unsigned __int64(bytesPerMeg),
      sufficient) )
  {
    errorLog << "Error in sufficientDiskSpace()" << endl;
    setErrorState(13, E6);
    return;
  }

  if (!sufficient) {
    errorLog << "Insufficient disk space\n";
    setErrorState(20, E7);
    return;
  }

  // remove values from registry
  _regToontown.deleteValue(_PANDA_WINDOW_OPEN_ValueName);
  _regToontown.deleteValue(_PANDA_ERROR_CODE_ValueName);
  _regToontown.deleteValue(_LAUNCHER_MESSAGE_ValueName);

#ifndef _EXEINSTALLER_
  // get the flash version info from the registry
  getFlashVersionInfoFromReg(_game1Version, _GAME1_VERSION_ValueName,
                             _needToDownloadGame1);
  getFlashVersionInfoFromReg(_movieVersion, _MOVIE_VERSION_ValueName,
                             _needToDownloadMovie);
  getFlashVersionInfoFromReg(_game2Version, _GAME2_VERSION_ValueName,
                             _needToDownloadGame2);
  getFlashVersionInfoFromReg(_messagesVersion, _MESSAGES_VERSION_ValueName,
                             _needToDownloadMessages);
  getFlashVersionInfoFromReg(_toontuneVersion, _TOONTUNE_VERSION_ValueName,
                             _needToDownloadToontune);
#endif

  // get the latest launcher file database
  if (getLatestLauncherFileDB()) {
    errorLog << endl << "error downloading launcher file DB" << endl;
    setErrorState(13, E8);
    return;
  }

#if defined(USE_TESTSERVER) && defined(SEND_CONFIGINFO_TO_STATSERVER)
  if(!_bConfigSubmitApproved) {
    errorLog << "config submit not approved yet" << endl;
    // tell installer.php to open up window asking for user permission to send config data

    // create a preliminary possibly incomplete (since configrc.exe has not run)
    // config record to display to user
    CreateConfigInfoRecord();

    // make installer.php popup a confirmation dialog
    _StateCode = 7;
    return;
  }
  errorLog << "config submit approved" << endl;
#endif

  // if user has given permission to send config data, continue init process
  _StateCode = 10;
}
//
//
//
void toontownInstaller::
handleCase7() {
#if defined(USE_TESTSERVER) && defined(SEND_CONFIGINFO_TO_STATSERVER)
  if(_bConfigSubmitApproved) {
    _StateCode = 10;
    errorLog << "config submit approved" << endl;
    runInstaller();  // dont wait for js to call us again
  }
#else
  errorLog << "error: state 7 should never be reached!" << endl;
#endif
}
//
//
//
void toontownInstaller::
handleCase10() {
#ifndef _EXEINSTALLER_
  // if we don't have messages.swf, get it
  if (downloadFlashMovie(_messages_IFilename, _needToDownloadMessages,
                         _MESSAGES_VERSION_ValueName, _messagesVersion)) {
    setErrorState(13, E9);
    return;
  }
   // if we don't have toon_tune.swf, get it
  if (downloadFlashMovie(_toontune_IFilename, _needToDownloadToontune,
                         _TOONTUNE_VERSION_ValueName, _toontuneVersion)) {
    setErrorState(13, E10);
    return;
  }
#endif
   // do we have the launcher?
  if (fileExists(_launcherSelfExtractor_IFilename.getFullLocalName()) &&
      launcherHasBeenExtracted())
//  if ( vos::file::exists(_launcherSelfExtractor_IFilename.getFullLocalName())
//	   && launcherHasBeenExtracted() )
  {
    errorLog << "Launcher has already been extracted" << endl;
#ifndef _EXEINSTALLER_
    // is the movie/game2 done?
    if (game2Done())
	{ // put up "updating Toontown" message
      _StateCode = 23;
      return;
    }
	else
	{ // *** make sure we have the movie
      if (downloadFlashMovie(_movie_IFilename, _needToDownloadMovie,
                             _MOVIE_VERSION_ValueName, _movieVersion)) {
        setErrorState(13, E11);
        return;
      }
      // *** make sure we have game2
      if (downloadFlashMovie(_game2_IFilename, _needToDownloadGame2,
                             _GAME2_VERSION_ValueName, _game2Version)) {
        setErrorState(13, E12);
        return;
      }
      // start the movie
      _StateCode = 90;
    }
#else
  _StateCode = 23;
  return;
#endif
  }
  errorLog << "Launcher has not yet been installed" << endl;

#ifndef _EXEINSTALLER_
  // get rid of GAME2_DONE reg value, if present
  _regToontown.deleteValue(_GAME2_DONE_ValueName);

  // do we have the movie?
  if ( !needToDownloadFlashMovie(_movie_IFilename.getFullLocalName(), _needToDownloadMovie)
	   && !needToDownloadFlashMovie(_game2_IFilename.getFullLocalName(), _needToDownloadGame2))
  { // start the movie
    errorLog << "Starting the Flash intro movie" << endl;
    _StateCode = 50;
    return;
  } else {
    // make sure we have game1
    if (downloadFlashMovie(_game1_IFilename, _needToDownloadGame1,
                           _GAME1_VERSION_ValueName, _game1Version)) {
      setErrorState(13, E13);
      return;
    }

    // start up game1
    errorLog << "Starting game1..." << endl;
    _StateCode = 30;
  }
#else
  _StateCode = 53;				// download the launcher
#endif
}
//
//
//
void toontownInstaller::
handleCase13() {
  // we should never get here!!!
  // state 13 is the "major error" state;
  // javascript should have picked up on it and not continued to call runInstaller()
  errorLog << "runInstaller() called with \"major error\" state" << endl;

  reFocusWindow(_installer_hwnd, SW_RESTORE);
}
//
//
//
void toontownInstaller::
handleCase23() {
#ifndef _EXEINSTALLER_
  // this extra step is necessary to allow javascript to load up a flash movie
  errorLog << "Displaying \"updating Toontown\" flash movie" << endl;
#endif
  // check if the launcher is valid
  _StateCode = 25;
#ifdef RECURSE_FOR_SPEED
  // recursive -- speed things up a bit for the already-installed case
  runInstaller();
#endif
}
//
//
//
void toontownInstaller::
handleCase25() {
  LauncherType lt;
  // is the launcher valid?
  lt = launcherValid();
  if (lt == LAUNCHER_VALID) {
    // run the launcher
    _StateCode = 97;
#ifdef RECURSE_FOR_SPEED
    // recursive -- speed things up a bit for the already-installed case
    runInstaller();
#endif
  } else {
    // launcher is invalid
    if(++_launcherInvalidCount > 2) {
#ifdef DONT_PATCH_JUST_REINSTALL
      addUserErrorAndLog("Internal error: launcher is out of sync with the launcher file database");
#else
      addUserErrorAndLog("Internal error: Error updating launcher files");
#endif
      setErrorState(20, E14);
      return;
    }
    if (lt == LAUNCHER_NEED_EXTRACT) {
      extractLauncher();
    }
    else {
#ifdef DONT_PATCH_JUST_REINSTALL
      // re-download and re-install the launcher
      _StateCode = 53;
#else
      if (_launcherInvalidCount < 2) {
        _StateCode = 85;    // patch the launcher
      }
      else
        _StateCode = 53;    // try redownload and reinstall
#endif
    }
  }
}
//
//
//
void toontownInstaller::
handleCase30() {
#ifndef _EXEINSTALLER_
  // check to see if we need to download the movie
  if (!needToDownloadFlashMovie(_movie_IFilename.getFullLocalName(), _needToDownloadMovie))
  {
    // the movie is current
    _StateCode = 36;
    return;
  }
  // start downloading movie
  errorLog << "Starting movie download..." << endl;
  _curDownloadThreadHandle = asyncDownloadToFile(_movie_IFilename.getFullRemoteName(),
                                                 _movie_IFilename.getFullLocalName(),false);
  if (NULL == _curDownloadThreadHandle) {
    errorLog << "Error downloading " << _movie_IFilename.getFullRemoteName() << endl;
    setErrorState(13, E15);
    return;
  }
  // wait for download to complete
  _StateCode = 35;
#else
  _StateCode = 53;						// go straight to self-extractor
#endif
}
//
//
//
void toontownInstaller::
handleCase35()
{
#ifndef _EXEINSTALLER_
  // is movie is done downloading?
  int result = asyncDownloadDone(_curDownloadThreadHandle);
  // is there a problem?
  if ( (result < 0)
	  || ((result > 0) && !fileExists(_movie_IFilename.getFullLocalName())))
// 	  || ((result > 0) && !vos::file_exists(_movie_IFilename.getFullLocalName())) )
  {
    errorLog << "Error downloading " << _movie_IFilename.getFullRemoteName() << endl;
    setErrorState(13, E16);
  }
  else if (result > 0)
  {
    flashMovieDownloadedSuccessfully(_MOVIE_VERSION_ValueName, _movieVersion);
    errorLog << "Movie download complete" << endl;
    _StateCode = 36;
  }
#else
  _StateCode = 36;
#endif
}
//
//
//
void toontownInstaller::
handleCase36() {
#ifndef _EXEINSTALLER_
  // check to see if we need to download game2
  if (!needToDownloadFlashMovie(_game2_IFilename.getFullLocalName(), _needToDownloadGame2))
  {
    // game2 is current
    _StateCode = 38;
    return;
  }
  // start downloading game2
  errorLog << "Starting game2 download..." << endl;
  _curDownloadThreadHandle = asyncDownloadToFile(_game2_IFilename.getFullRemoteName(),
                                                 _game2_IFilename.getFullLocalName(),false);
  if (NULL == _curDownloadThreadHandle) {
    // error downloading game2
    errorLog << "Error downloading " << _game2_IFilename.getFullRemoteName() << endl;
    setErrorState(13, E17);
    return;
  }
#endif
  // wait for download to complete
  _StateCode = 37;
}
//
//
//
void toontownInstaller::
handleCase37()
{
#ifndef _EXEINSTALLER_
  // is game2 is done downloading?
  int result = asyncDownloadDone(_curDownloadThreadHandle);
  // is there a problem?
  if ( (result < 0)
	  || ((result > 0) && !fileExists(_game2_IFilename.getFullLocalName())))
//	  || ((result > 0) && !vos::file_exists(_game2_IFilename.getFullLocalName())) )
  {
    errorLog << "Error downloading " << _game2_IFilename.getFullRemoteName() << endl;
    setErrorState(13, E18);
  }
  else if (result > 0)
  {
    flashMovieDownloadedSuccessfully(_GAME2_VERSION_ValueName, _game2Version);
    errorLog << "Game2 download complete" << endl;
    // tell javascript to tell game1 that it can exit
    _StateCode = 38;
  }
#else
  _StateCode = 38;
#endif
}
//
//
//
void toontownInstaller::
handleCase38() {
  // javascript has told game1 it can exit
  errorLog << "Waiting for user to exit game1..." << endl;
  _StateCode = 40;
}
//
//
//
void toontownInstaller::
handleCase40()
{
#ifndef _EXEINSTALLER_
  // has user exited flash game1?
  if(_game1_Done)
  {
    // user has exited flash game1, start the movie
	_StateCode = 50;
  }
#else
  _StateCode = 50;
#endif
}
//
//
//
void toontownInstaller::
handleCase50() {
  // movie has been started, start downloading launcher...
  errorLog << "Starting the movie..." << endl;
  _StateCode = 53;
}
//
//
//
void toontownInstaller::
handleCase53() {
  // if from cd, then we need to validate the launcher, figure out from what cd etc.
  // returns 0 if value is not in reg
  if (_regToontown.getDWORD(_CDROM_ValueName)) {
    _StateCode = 25;
    return;
  }

  // start downloading the launcher self-extractor
  if(!deleteObsoleteFile(_launcherSelfExtractor_IFilename.getFullLocalName())) {
    addUserAccessDeniedToErrorAndLog(_launcherSelfExtractor_IFilename.getFullLocalName());
    errorLog << "aborting download\n";
    setErrorState(13, E19);
    return;
  }

#define MAX_DOWNLOAD_TRIES 4

  _LauncherDownloadTryNum++;
  // use known unreliable URLDownloadToFile as Last Resort
  bool bUseURLDownloadToFile = (_LauncherDownloadTryNum==MAX_DOWNLOAD_TRIES);

  errorLog << "Starting download of Launcher self-extractor, Attempt #" <<  _LauncherDownloadTryNum << endl;
  if(bUseURLDownloadToFile) {
    errorLog << "Using URLDownloadToFile method\n";
  }
  //DBG("Download InstallLauncher?!");
  errorLog << "Downloading " << _launcherSelfExtractor_IFilename.getFullRemoteName() << endl;
  
  _PatchSize = GetPatchSize(0);
  _PatchSizeSoFar = 0;      // reset download metering

  _curDownloadThreadHandle =  asyncDownloadToFile(
      _launcherSelfExtractor_IFilename.getFullRemoteName(),
      _launcherSelfExtractor_IFilename.getFullLocalName(),
      bUseURLDownloadToFile);
  if (NULL == _curDownloadThreadHandle) {
    // error downloading launcher
    errorLog << "Error downloading " << _launcherSelfExtractor_IFilename.getFullRemoteName() << endl;
    setErrorState(13, E20);
    return;
  }
  _StateCode = 55;
}
//
//
//
void toontownInstaller::
handleCase55() {
  // state 55 is "waiting for launcher to download"
  // is launcher done downloading?
  int result = asyncDownloadDone(_curDownloadThreadHandle);
  //DBG("Still downloading...");

  if(result == 0) // still waiting
    return;

  //DBG("Finished Downloading InstallLauncher!");

  bool bDownloadFailed=(result!=1);

  if(!bDownloadFailed)
  {
    if(!launcherFileValid(_launcherSelfExtractor_IFilename))
    {
      bDownloadFailed=true;

      // print out file size just for additional info
      // todo: read html headers to determine if it's a 404 file not found HTML error page
      // returned by server

      HANDLE hFile = CreateFile(_launcherSelfExtractor_IFilename.getFullLocalName(),
                                0x0, FILE_SHARE_WRITE|FILE_SHARE_READ, NULL, OPEN_EXISTING,
                                FILE_ATTRIBUTE_NORMAL,NULL);
      if(hFile) {
        DWORD InstallerFileSize = GetFileSize(hFile,NULL);
        errorLog << _launcherSelfExtractor_IFilename.getFullRemoteName() << " is size " << InstallerFileSize << " bytes\n";
        CloseHandle(hFile);
      }
    }
  }

  if (bDownloadFailed) {
    errorLog << "Error downloading " << _launcherSelfExtractor_IFilename.getFullRemoteName() << endl;
    if(_LauncherDownloadTryNum<MAX_DOWNLOAD_TRIES) {
      errorLog << "Retrying download\n";
      _StateCode = 53;
    }
    else {
      setErrorState(13, E21);
      return;
    }
  }
  else {
    errorLog << "Launcher self-extractor download complete" << endl;

    if(!_ProxyUserName.empty()) {
      // have to actually open an internet connection to get these values
      _regToontown.setString(_PROXY_USER_ValueName, _ProxyUserName);
      _regToontown.setString(_PROXY_PASSWORD_ValueName, _ProxyUserPassword);
    }

    // remove LAUNCHER_EXTRACTED value
    _regToontown.deleteValue(_LAUNCHER_EXTRACTED_ValueName);

    errorLog << "Running Launcher self-extractor..." << endl;

    // start self-extracting launcher; this function sets the statecode to 60 on success
    extractLauncher();
  }
}
//
//
//
void toontownInstaller::
handleCase60() {
  // if launcher self-extraction is done (check for LAUNCHER_EXTRACTED value)
  int result = launcherSelfExtractDone();
  if (result) {
    if (2 == result) {
      // an error occured during the self-extraction
      addUserErrorAndLog(launcherExtractProcessDiedErr);
      setErrorState(20, E23);
      return;
    }

    if(_pSysInfo->get_os_type() >= SysInfo::OS_Win2000) {
      // fix up the incorrect total size in Add/Remove Programs on win2000/XP
      // would be nice if I waited until it was fully downloaded, measured the dirsize,
      // and wrote that value instead of this canned one, but this is good enough 4 now
      // XP seems better than 2000 about getting this value right, maybe it periodically
      // checks the total dirsize
      writeInstalledSizeToRegistry(Installer_ProgramName,TOTAL_INSTALLEDSIZE);
    }
    // launcher self-extract has completed
    errorLog << "Launcher extraction/installation complete" << endl;
    // check that launcher is valid
    _StateCode = 25;
  }
}
//
//
//
void toontownInstaller::
handleCase85() {
  // patch the launcher
  if(patchLauncherFiles()) {
    addUserErrorAndLog("Error patching launcher files");
    setErrorState(20, E31);
    return;
  }
  // go back, check again if launcher is current now
  _StateCode = 25;
}
//
//
//
void toontownInstaller::
handleCase90() {
  // movie has been started, check if the launcher is current
  errorLog << "Starting the movie..." << endl;
  _StateCode = 25;
}
//
//
//
void toontownInstaller::
handleCase97() {
  // run launcher
  if (runLauncher()) {
    // launcher could not be run
    addUserErrorAndLog("Error running launcher");
    setErrorState(13, E24);
    return;
  }
  // and start sending it completion updates
  _StateCode = 110;
}
//
//
//
void toontownInstaller::
handleCase110() {
  // updating "percent loaded"...
  // if launcher croaked, we gots an error.
  if (launcherExitedPrematurely()) {
    // First, check for a PANDA_ERROR_CODE.
    int pErr = checkPandaError();
    if ( pErr ) {
      if ((pErr == 14) || (pErr == 11) || (pErr == 7)) {
        setErrorState(24, E32);  // 24 == graphics error page
      }
      else {
        setErrorState(20, E28);  // 20 == general error page
      }
      return;
    }

    // No PANDA_ERROR_CODE, so give 'em the generic premature-exit
    // error.
    addUserErrorAndLog(launcherProcessEndedPrematurelyErr);
    setErrorState(20, E25);
    return;
  }

  // if game2 is done, wait for panda window to open
#ifndef _EXEINSTALLER_
  if (game2Done()) {
    errorLog << "Game2 is done, waiting for panda window to come up" << endl;

    _StateCode = 115;
    return;
  }
#else
  _StateCode = 115;
#endif
}
//
//
//
void toontownInstaller::
handleCase115() {
  // if launcher croaked, we gots an error.
  if (launcherExitedPrematurely()) {
    // First, check for a PANDA_ERROR_CODE.
    int pErr = checkPandaError();
    if (pErr) {
      if ((pErr == 14) || (pErr == 11) || (pErr == 7)) {
        setErrorState(24, E33);  // 24 == graphics error page
      }
      else {
        setErrorState(20, E29);  // 20 == general error page
      }
      return;
    }

    // No PANDA_ERROR_CODE, so give 'em the generic premature-exit
    // error.
    addUserErrorAndLog(launcherProcessEndedPrematurelyErr);
    setErrorState(20, E26);
    return;
  }

  // stay in this state until panda window opens or we get an error
  if (!pandaWindowOpen())
    return;

  // if panda window has come up, transition to the next state
  errorLog << "Panda window is up" << endl;

  if(_bConfigSubmitApproved) {
    // now that configrc.exe has run, we should have all the info in registry
    // this also means we only record runs that successfully open a gfx window
    CreateConfigInfoRecord();

    // note due to init _LastPandaErrorCode will be set to 0 in the submitted record,
    // even though we havent actually exited the app at this point
    // so no valid value exists.

    // eventually hope to add this for consenting release server users too
    SendConfigRecord();
  }

  // wait until this point to delete old logs to preserve last good run?
  deleteOldLogs(_installerLogPathPattern.c_str());

  // at this point, don't kill the launcher on shutdown
  _OK_To_Kill_LauncherProcess = 0;

  _StateCode = 120;

  // set toontown window to foreground (it cant do this itself if it is not the foreground process)
  HWND hWnd = FindWindow(NULL, toontown_window_title);
  if(hWnd == NULL) {
    errorLog << "Couldnt find Toontown window '" << toontown_window_title << "' to foregnd it\n";
  }
  else {
    if(!SetForegroundWindow(hWnd))
      errorLog << "SetForegroundWin failed for main TT window\n";
  }
  reFocusWindow(_installer_hwnd, SW_SHOWMINNOACTIVE);
}
//
//
//
void toontownInstaller::
handleCase120() {
  // slow polling loop started
  _StateCode = 130;
}
//
//
//
void toontownInstaller::
handleCase130() {
  // if launcher is still running, no worries
  // hey... you awake? *nudge*
  DWORD exitCode;
  if (launcherAlive(exitCode)) {
    time_t curtime;
    time(&curtime);

    if(difftime(curtime,_lastmemcheck_time) > _cur_memcheck_interval) {
      _cur_memcheck_interval+=MEMCHECK_INTERVAL_INC;
      _lastmemcheck_time = curtime;
      _pSysInfo->PrintProcessMemInfo(_hLauncherProcess);
    }
    return;
  }

  // game has quit
  reFocusWindow(_installer_hwnd, SW_RESTORE);

  // won't be needing this anymore...
  _hLauncherProcess = NULL;

  // if PANDA_ERROR_CODE is not in registry, panda/python must have
  // crashed.  (At one time, we couldn't tell this from an Alt-F4
  // exit, but nowadays exiting by closing the window puts a normal
  // PANDA_ERROR_CODE in.)

  int pErr = checkPandaError();

  if(pErr == 0) {
    // normal exit occurred and PANDA_ERROR_CODE was set to 0
    _StateCode = 140;  // normal exit page
    return;
  }

  if (pErr) {
    if ((pErr == 14) || (pErr == 11) || (pErr == 7)) {
      setErrorState(24, E34);  // 24 == graphics error page
    }
    else {
      setErrorState(20, E30);  // 20 == general error page
    }
    return;
  }

  // comment out for the moment, until 1.5x is official
  // #define NEW_PANDA_ALTF4_HANDLING
#ifdef NEW_PANDA_ALTF4_HANDLING
  assert(pErr==-1);
  // If there's no PANDA_ERROR_CODE, we had a crash--I guess.
  // This really shouldn't happen either.  Send them to the
  // report-a-bug page.

  addUserErrorAndLog(gameCrashedErr);
  setErrorState(20, E27);  // 20 == general error page
#else
  // in old system, AltF4 allows you to leave TT without setting a PANDA_ERROR_CODE,
  // so most of the time it wont be an error
  _StateCode = 140;  // normal exit page
#endif

}
////////////////////////////////////////////////////////////////////
// this is the main installer state function.
////////////////////////////////////////////////////////////////////
void toontownInstaller::runInstaller()
{
  printStateCodeUpdates();
  switch (_StateCode) {
    // set up
  case 0: {
    handleCase0();
#ifndef _EXEINSTALLER_
    // dont wait for js to call us again
    runInstaller();
#endif
    break;
  }
    // wait for config-submit approval via SetValue method
  case 7: {
    handleCase7();
    break;
  }
   // continue init after config-submit has been approved
  case 10: {
    handleCase10();
    break;
  }
    // we should never get here!!!
  case 13: {
    handleCase13();
    break;
  }
    // this extra step is necessary to allow javascript to load up a flash movie
  case 23: {
    handleCase23();
    break;
  }
    // check launcher files
  case 25: {
    handleCase25();
    break;
  }
    // check to see if we need to download the movie
  case 30: {
    handleCase30();
    break;
  }
    // flashMovie download waiting...which one?
  case 35: {
    handleCase35();
    break;
  }
    // check to see if we need to download game2
  case 36: {
    handleCase36();
    break;
  }
    // is game2 is done downloading?
  case 37: {
    handleCase37();
    break;
  }
    // javascript has told game1 it can exit
  case 38: {
    handleCase38();
    break;
  }
    // has user exited flash game1?
  case 40: {
    handleCase40();
    break;
  }
  // movie has been started, start downloading launcher...
  case 50: {
    handleCase50();
    //break; *** FALL THROUGH ***
  }
    // start downloading the launcher self-extractor
  case 53: {
    handleCase53();
    break;
  }
    // state 55 is "waiting for launcher to download"
  case 55: {
    handleCase55();
    break;
  }
    // if launcher self-extraction is done (check for LAUNCHER_EXTRACTED value)
  case 60: {
    handleCase60();
    break;
  }
    // patch the launcher
  case 85: {
    handleCase85();
    break;
  }
    // movie has been started, check if the launcher is current
  case 90: {
    handleCase90();
    break;
  }
    // run launcher
  case 97: {
    handleCase97();
    break;
  }
    // updating "percent loaded"...
  case 110: {
    handleCase110();
    break;
  }
    // if launcher croaked, we gots an error.
  case 115: {
    handleCase115();
    break;
  }
    // slow polling loop started
  case 120: {
    handleCase120();
    break;
  }
    // if launcher is still running, no worries
  case 130: {
    handleCase130();
    break;
  }
  default:
    errorLog << "TT Installer Error: invalid StateCode " << _StateCode << endl;
  }
}

////////////////////////////////////////////////////////////////////

// This function is called when the Launcher (or the game) has exited;
// it checks for PANDA_ERROR_CODE and, if set, stores an appropriate
// message according to the nature of the error. The return value is -1 if no
// error code was found, or the error code itself (0 indicates no panda error)

// I've changed this to NOT set the statecode.  Let the caller decide which
// state to transition to, since it may not always be the same state
int toontownInstaller::
checkPandaError(void)
{
  DWORD pandaErrorCode;

  if (_regToontown.getDWORD(_PANDA_ERROR_CODE_ValueName, pandaErrorCode) != 0) {
    // Unexplained exit.
    errorLog << "No panda error code set.\n";
    _LastPandaErrorCode = -1;
    return -1;
  }

  errorLog << "Got panda error code: " << pandaErrorCode << "\n";
  _LastPandaErrorCode = pandaErrorCode;

  if (pandaErrorCode == 0) {
    // Normal exit.
    return 0;
  }

  const char *message = NULL;
  if (pandaErrorCode >= 0 && pandaErrorCode < numPandaErrors) {
    message = pandaErrors[pandaErrorCode];
  }

  if (message == NULL) {
    // Unknown error code.  This is some kind of internal error.
    char msg[100];
    sprintf(msg,"Unknown panda errorcode: %d",pandaErrorCode);
    addUserErrorAndLog(msg);
  } else {
      addUserErrorAndLog(message);
      // dump driver info for driver error
      if ((pandaErrorCode == 14) || (pandaErrorCode == 11) || (pandaErrorCode == 7)){
        addUserError("");
        addUserError("Your Graphics Card Info:");
        addUserError(_pSysInfo->_VideoCardNameStr.c_str());
        addUserError(_pSysInfo->_VideoCardDriverDateStr.c_str());
        addUserError(_pSysInfo->_VideoCardDriverVerStr.c_str());
      }
  }

  if((pandaErrorCode==4) && ((_TroublesomeInstalledPrograms.size()>0)||(_TroublesomeRunningPrograms.size()>0))) {
      addUserError("\nToontown has detected the following programs installed or running on your PC, you could try disabling them to fix connection or game startup difficulties:\n");
      for(unsigned i=0;i<_TroublesomeInstalledPrograms.size();i++) {
          addUserError(_TroublesomeInstalledPrograms[i].c_str());
      }
      for(unsigned i=0;i<_TroublesomeRunningPrograms.size();i++) {
          addUserError(_TroublesomeRunningPrograms[i].c_str());
      }
  }

  return pandaErrorCode;
}

#ifndef _EXEINSTALLER_
// these functions recieve the version strings for the flash movies
void toontownInstaller::
setFlashMovieVersion(const char *newVer, char *verStr, char *name) {
  errorLog << "Current " << name << " version is '" << newVer << "'" << endl;

  // if the version string is already set, something
  // is wrong. These version numbers should be set before
  // the installer main loop is run.
  if (strlen(verStr))
    errorLog << "WARNING: " << name << " version is already set to '"
      << verStr << "'" << endl;

  strcpy(verStr, newVer);
}

// utility functions to handle flash movies
void toontownInstaller::
getFlashVersionInfoFromReg(char *verStr, const char *key, int &needToDownload) {
  string temp;
  // if there was no version string, or the version string
  // we found doesn't match the one passed in, we have a
  // new version; set up to download the flash file
  if (_regToontown.getString(key, temp) || temp.compare(verStr)) {
    needToDownload = 1;
    errorLog << key << " '" << temp << "' is out of date, will download version '"
             << verStr << "' if needed" << endl;
  }
}

int toontownInstaller::
needToDownloadFlashMovie(const char *filename, int forceDownloadFlag) {
#ifdef DONT_DOWNLOAD_FLASH_FILES
  // never say that we need to download any flash files
  return 0;
#endif
 if (!forceDownloadFlag && fileExists(filename)) {
 //  if (!forceDownloadFlag && vos::file::exists(filename)) {
    return 0;
  }
  return 1;
}

void toontownInstaller::
flashMovieDownloadedSuccessfully(const char *regKey, const char *verStr) {
  _regToontown.setString(regKey, verStr);
}

// this will download a flash movie synchronously, but only if we need to.
// returns non-zero on failure
int toontownInstaller::
downloadFlashMovie(installerFilename &filename, int forceDownloadFlag,
                   const char *regKey, const char *version)
{
  if (needToDownloadFlashMovie(filename.getFullLocalName(),
                               forceDownloadFlag))
    {
      if(!deleteObsoleteFile(filename.getFullLocalName())) {
        errorLog << "aborting download of " <<
          filename.getFullRemoteName() << endl;
        return 1;
      }

      errorLog << "Downloading " << filename.getFullRemoteName() << "..." << endl;
      if (!downloadToFile(filename.getFullRemoteName(),
                          filename.getFullLocalName()))
        {
          // error downloading file
          errorLog << "Error downloading " << filename.getFullRemoteName() << endl;
          return 1;
        }
      flashMovieDownloadedSuccessfully(regKey, version);
    }
  return 0;
}
#endif // _EXEINSTALLER_

////////////////////////////////////////////////////////////////////
// These functions receive the Blast URL parameters
void toontownInstaller::
setSWID(const char *swid) {
  // make sure that we're initialized
  if (normalInit()) {
    strcpy(_SWID_String, swid);
  }
}
/////////////////////////////////////////////////////////////////////
// This is a generic function to open/create a registry. It takes
// RegKeyName, pointer to HKEY (value to be returned and PACL
// returns 0 on success
int toontownInstaller::
createRegistry(const char *RegKeyName, PHKEY _hKey, PACL pNewDacl)
{
  char *errstr = NULL;
  LONG regRetVal;

  // to run, we must be able to write the TT regkey.  but dont need to be able to create it,
  // unless it doesnt exist
  regRetVal=RegOpenKeyEx(TOONTOWN_HKEY, RegKeyName,0,
                           KEY_READ | KEY_WRITE, _hKey);

  if(regRetVal==ERROR_SUCCESS) {
    goto _exiting;
  }

  // ok for it to be NOT_FOUND
  if((regRetVal!=ERROR_PATH_NOT_FOUND)&&(regRetVal!=ERROR_FILE_NOT_FOUND)) {
    // errors defined in winerror.h, starting at ERROR_SUCCESS
    errorLog << "regInit RegOpenKeyEx failed, errVal=" << regRetVal << endl;
    return 1;
  }

  DWORD ActionTaken;
  regRetVal = RegCreateKeyEx(TOONTOWN_HKEY, RegKeyName,
                             0, "", REG_OPTION_NON_VOLATILE,
                             KEY_READ | KEY_WRITE, NULL, _hKey, &ActionTaken);
  if(regRetVal!=ERROR_SUCCESS) {
    errorLog << "regInit RegCreateKeyEx failed, errVal=" << regRetVal << " " << RegKeyName <<endl;
    return 1;
  }

  if((ActionTaken!=REG_CREATED_NEW_KEY) ||
     (SysInfo::get_os_type() < SysInfo::OS_WinNT)) {// this logic need to get incorporated :todo
    return 0;
  }

  // need to make sure the new TT regkey is writeable/readable by non-admin users on NT

  EXPLICIT_ACCESS expl_access;
  DWORD errval;
  // NT4 - Vista compatible
  BuildExplicitAccessWithName(&expl_access,"EVERYONE",
                              SPECIFIC_RIGHTS_ALL | STANDARD_RIGHTS_ALL,  // not sure which are needed, so give everything
                              SET_ACCESS,
                              SUB_CONTAINERS_AND_OBJECTS_INHERIT);  // both sub regkeys and values should inherit

  errval = SetEntriesInAcl(1,&expl_access,NULL,&pNewDacl);
  if(errval!=ERROR_SUCCESS) {
    errstr="SetEntriesInAcl";
    goto _exiting;
  }

  errval=SetSecurityInfo(*_hKey,SE_REGISTRY_KEY,
                         DACL_SECURITY_INFORMATION |
                         PROTECTED_SACL_SECURITY_INFORMATION, // Make sure it doesnt inherit read-only perms
                         NULL,NULL,pNewDacl,NULL);
  if(errval!=ERROR_SUCCESS) {
    errstr="SetSecurityInfo";
    goto _exiting;
  }

 _exiting:
  if(errstr!=NULL) {
    LogOSErrorMessage(errstr);
    // errstr errors are non-fatal, so let things continue
  }
  if(pNewDacl)
    LocalFree(pNewDacl);

  return 0;
}
////////////////////////////////////////////////////////////////////
// regInit() opens the Panda3D,
// "HKEY_LOCAL_MACHINE/SOFTWARE/Disney/Disney Online/Toontown"
// and "HKEY_LOCAL_MACHINE/SOFTWARE/WDIG/TTO"
// registry keys.
// Returns 0 on success.
int toontownInstaller::
regInit() {
  PACL pNewDacl=NULL;

  if (_reg_initialized)
    return 0;

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  if (pandaRegInit()) return 1;
#endif

  HKEY _hKeyToontown;
  if (createRegistry(ToontownRegKeyName, &_hKeyToontown, pNewDacl)) {
    return 1;
  }
  _regToontown.init(_hKeyToontown);
  _reg_initialized = 1;

  HKEY _hKeyHackers;
  // create the prevent hack mechanism on registry keys
  if (createRegistry(ToontownHackers, &_hKeyHackers, pNewDacl)) {
    return 1;
  }
  _regHackers.init(_hKeyHackers);
  // test, take out later
  //  setKeyValue("TrialEligible", "2");

  return 0;
}
#if 0
////////////////////////////////////////////////////////////////////
// regInit() opens the Panda3D and "HKEY_CURRENT_USER/SOFTWARE/Disney/Disney Online/Toontown"
// registry keys.
// Returns 0 on success.
int toontownInstaller::
regInit() {
  char *errstr=NULL;
  PACL pNewDacl=NULL;

  if (_reg_initialized)
    return 0;

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  if (pandaRegInit()) return 1;
#endif
  LONG regRetVal;

  // to run, we must be able to write the TT regkey.  but dont need to be able to create it,
  // unless it doesnt exist
  regRetVal=RegOpenKeyEx(TOONTOWN_HKEY, ToontownRegKeyName,0,
                         KEY_READ | KEY_WRITE, &_hKeyToontown);

  if(regRetVal==ERROR_SUCCESS) {
    goto _exiting;
  }

  // ok for it to be NOT_FOUND
  if((regRetVal!=ERROR_PATH_NOT_FOUND)&&(regRetVal!=ERROR_FILE_NOT_FOUND)) {
    // errors defined in winerror.h, starting at ERROR_SUCCESS
    errorLog << "regInit RegOpenKeyEx failed, errVal=" << regRetVal << endl;
    return 1;
  }

  DWORD ActionTaken;
  regRetVal = RegCreateKeyEx(TOONTOWN_HKEY, ToontownRegKeyName,
                             0, "", REG_OPTION_NON_VOLATILE,
                             KEY_READ | KEY_WRITE, NULL, &_hKeyToontown, &ActionTaken);
  if(regRetVal!=ERROR_SUCCESS) {
    errorLog << "regInit RegCreateKeyEx failed, errVal=" << regRetVal << endl;
    return 1;
  }

  if((ActionTaken!=REG_CREATED_NEW_KEY) ||
     (SysInfo::get_os_type() < SysInfo::OS_WinNT))
    return 0;

  // need to make sure the new TT regkey is writeable/readable by non-admin users on NT

  EXPLICIT_ACCESS expl_access;
  DWORD errval;
  // NT4 - Vista compatible
  BuildExplicitAccessWithName(&expl_access,"EVERYONE",
                              SPECIFIC_RIGHTS_ALL | STANDARD_RIGHTS_ALL,  // not sure which are needed, so give everything
                              SET_ACCESS,
                              SUB_CONTAINERS_AND_OBJECTS_INHERIT);  // both sub regkeys and values should inherit

  errval = SetEntriesInAcl(1,&expl_access,NULL,&pNewDacl);
  if(errval!=ERROR_SUCCESS) {
    errstr="SetEntriesInAcl";
    goto _exiting;
  }

  errval=SetSecurityInfo(_hKeyToontown,SE_REGISTRY_KEY,
                         DACL_SECURITY_INFORMATION |
                         PROTECTED_SACL_SECURITY_INFORMATION, // Make sure it doesnt inherit read-only perms
                         NULL,NULL,pNewDacl,NULL);
  if(errval!=ERROR_SUCCESS) {
    errstr="SetSecurityInfo";
    goto _exiting;
  }

#if 0
  // this doesnt appear to be enough to allow limited user to download a new ActiveX control
  // download of new ActiveX control still fails on init for limited user, probably because
  // they need access to other parts of HKLM registry

  //////////
  // Change the ActiveX control file perms too, so kids can download updates OK.
  // this probably wont be enough because ActiveX updates require writing admin reg areas
  HKEY hKeyInternetSettings = regOpenKey_ReadOnly(TOONTOWN_HKEY, InternetSettingsRegKey);
  if (hKeyInternetSettings == NULL) {
    errstr="regOpenKey_ReadOnly";
    goto _exiting;
  }

  char activeXcontrol_filepath[_MAX_PATH];
  if(0 != regGetString(hKeyInternetSettings, ActiveXCache_RegValName, activeXcontrol_filepath, sizeof(activeXcontrol_filepath))) {
    errstr="regGetString";
    goto _exiting;
  }

  RegCloseKey(hKeyInternetSettings);

  strcat(activeXcontrol_filepath,"\\");
  strcat(activeXcontrol_filepath,tt_control_name);
  errval=SetNamedSecurityInfo(activeXcontrol_filepath,SE_FILE_OBJECT,
                              DACL_SECURITY_INFORMATION |
                              PROTECTED_SACL_SECURITY_INFORMATION, // Make sure it doesnt inherit read-only perms
                              NULL,NULL,pNewDacl,NULL);

  if(errval!=ERROR_SUCCESS) {
    errstr="SetNamedSecurityInfo-1";
    goto _exiting;
  }

  // change ttinst.inf too
  char *pCh=strrchr(activeXcontrol_filepath,'.');
  pCh[1]='i';  pCh[2]='n';  pCh[3]='f';

  errval=SetNamedSecurityInfo(activeXcontrol_filepath, SE_FILE_OBJECT,
                              DACL_SECURITY_INFORMATION |
                              PROTECTED_SACL_SECURITY_INFORMATION, // Make sure it doesnt inherit read-only perms
                              NULL,NULL,pNewDacl,NULL);
  if(errval!=ERROR_SUCCESS) {
    errstr="SetNamedSecurityInfo-2";
    goto _exiting;
  }
#endif

 _exiting:
  if(errstr!=NULL) {
    LogOSErrorMessage(errstr);
    // errstr errors are non-fatal, so let things continue
  }
  if(pNewDacl)
    LocalFree(pNewDacl);

  _reg_initialized = 1;
  return 0;
}
#endif

// if regInit() was called, regShutdown() should be called before program exit.
void toontownInstaller::
regShutdown() {
  if (_reg_initialized) {
    _reg_initialized = 0;
    _regToontown.closeKey();
    _regHackers.closeKey();

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
    pandaRegShutdown();
#endif
  }
}

Type toontownInstaller::
validHardware(void) {
  Type retVal = HARDWARE_VALID;

  if(_pSysInfo == NULL)
    _pSysInfo = new SysInfo();

  /*
  // check CPU type
  if(sysInfo.get_cpu_type() == )
  {
    addUserError("Invalid CPU type");
    errorLog << "Invalid hardware: invalid CPU type" << endl;
    retVal = HARDWARE_VALID;
  }

  // check CPU level
  if(sysInfo.get_cpu_level() < )
  {
    addUserError("Invalid CPU level");
    errorLog << "Invalid hardware: invalid CPU level" << endl;
    retVal = HARDWARE_VALID;
  }
  */

  // check OS type
  if(_pSysInfo->get_os_type() == SysInfo::OS_unknown)
  {
    errorLog << "Invalid hardware: unknown OS; continuing anyway" << endl;
  }

  // check for mouse
  if(!_pSysInfo->get_mouse_enabled())
  {
    addUserError("No mouse detected");
    errorLog << "Invalid hardware: no mouse detected" << endl;
    retVal = HARDWARE_INVALID;
  }

  // make sure we have enough RAM
  // windows slightly under-reports the amount of RAM you have,
  // so we make our number a little bit smaller to compensate (ack pbbbt)
  //unsigned long requiredBytes = unsigned long(0.95f * (REQUIRED_RAM_MEGS * bytesPerMeg));
  if (_pSysInfo->get_ram_megs_total() < REQUIRED_RAM_MEGS) {
    char msg[1024];
    float RamMegs=_pSysInfo->get_ram_megs_total();

    // make numbers pretty for user errormsg, in case they are off by a little for whatever reason
    if((RamMegs > 30.0f) && (RamMegs <  38.0f)) {
        RamMegs=32.0f;
    } else if((RamMegs > 60.0f) && (RamMegs <  70.0f)) {
        RamMegs=64.0f;
    } else if((RamMegs > 92.0f) && (RamMegs < 100.0f)) {
        RamMegs=96.0f;
    }

    sprintf(msg, "Your computer has only %d Megabytes of RAM Memory, which is less than the minimum %d Megabytes of RAM that Toontown requires to run. (This refers to computer RAM chip memory, not disk space!)",(int)RamMegs,REQUIRED_RAM_MEGS);

    /*else {
        sprintf(msg, "Your computer has less than the minimum %d Megabytes of RAM memory that Toontown requires to run. (This refers to computer RAM chip memory, not disk space!)",REQUIRED_RAM_MEGS);
    }
    */
    errorLog << "Invalid hardware: insufficient RAM: " << _pSysInfo->get_ram_megs_total() << "MB,  required: " << REQUIRED_RAM_MEGS  << "MB\n";
    addUserErrorAndLog(msg);
    retVal = HARDWARE_INVALID;
  }

  // tells Configrc.exe to tell wdxdisplay8 to pick the best resolution based on vidmem size
  // if saved user display res does not exist
  _configrc_args.append("-pickbestres ");

  // check gfx API
  if(!_pSysInfo->get_3d_hw()) {
    string user_error=_pSysInfo->_gfx_report_str.str();
    if(!user_error.empty()) {
        addUserError(user_error.c_str());
        errorLog << user_error.c_str() << endl;
    }
    retVal = HARDWARE_INVALID_3D;

  } else {
    // Pass Configrc args to Launcher.py to suggest a particular
    // graphics API, but do not override any saved settings file the
    // user may have created
    switch (_pSysInfo->get_suggested_gfx_api()) {
    case SysInfo::GAPI_OpenGL:
      _configrc_args.append("-OGL -NoOverride ");
      break;

    case SysInfo::GAPI_DirectX_7:
#if USE_DX7
      _configrc_args.append("-DX7 -NoOverride ");
      break;
#endif

    case SysInfo::GAPI_DirectX_8_0:
    case SysInfo::GAPI_DirectX_8_1:
      _configrc_args.append("-DX8 -NoOverride ");
      break;

#if USE_DX9
    case SysInfo::GAPI_DirectX_9_0:
      _configrc_args.append("-DX9 -NoOverride ");
      break;
#endif
    }
  }

  if(!_pSysInfo->has_custom_mousecursor_ability())
     _configrc_args.append("-cursor_off ");

#if 0
  // miles does not require DirectSound.  need to recode this check
  // (we may want to require HW sound support)

   // don't bother checking on the video card/sound card if DX is not installed
  // check sound card
  if(!_pSysInfo->get_sound_enabled()) {
    /*
    addUserError("No sound card detected");
    errorLog << "Invalid hardware: sound card not detected" << endl;
    retVal = HARDWARE_VALID;
    */
  }
#endif

#if 0
  // currently we dont enforce min baud reqmt

  #define MIN_BAUD_REQUIRED 19200
  // check max baud rate
  if(_pSysInfo->get_max_baud() < MIN_BAUD_REQUIRED) {
    char msg[1024];
    sprintf(msg, "Modem may not be fast enough: %i baud detected, %d baud required",
            _pSysInfo->get_max_baud(),MIN_BAUD_REQUIRED);
    addUserError(msg);
    errorLog << msg << "   -- CONTINUING ANYWAY --" << endl;
    //retVal = 0;
  }
#endif

  // print out list of these to log,  later will use _TroublesomePrograms to warn user if we get an error
  (void) checkForTroublesomeInstalledSoftware(_TroublesomeInstalledPrograms);
  (void) checkForTroublesomeRunningSoftware(_TroublesomeRunningPrograms);

  return retVal;
}
////////////////////////////////////////////////////////////////////


#if !defined(USE_RPCINSTALLER)
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
// POTENTIALLY PROJECT-INDEPENDENT METHODS
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
// this function is called to set the name of the download server
// this can be an IP, a computer name, or a full web address
void toontownInstaller::
DownloadServer(const char *downloadServer, bool bUpdate)
{
  if (!downloadServer)
	return;
  else
  { // backwards compatibility for legacy code
	if (strchr(downloadServer, ';')) {
	  setDownloadServerList(downloadServer);
	  return;
	}
  }

  // make sure that we're initialized
  if (!normalInit())
    return;

//
// frame the server name in "http://" and "/"
//
  // form a URL
  _downloadServerURL[0]='\0';
  const char *http_prefix="http://";
  static size_t prefix_len = strlen(http_prefix);

  // does the download server URL we're given start with "http://" ?
  if (strncmp(http_prefix, downloadServer, prefix_len)) {
    // no, so start with it
    strcpy(_downloadServerURL, http_prefix);
  }
  // add the URL we're given (but don't trust its length)
  strlcat(_downloadServerURL, downloadServer, _MAX_PATH);
  // make sure there's a trailing slash
  addTrailingForwardSlash(_downloadServerURL);

  errorLog << "Download server set to " << _downloadServerURL << endl;
  // make a copy to pass to the launcher; only if needed
  if (bUpdate)
    strcpy(_DOWNLOAD_SERVER_String, _downloadServerURL);

  // since we have a new download server, re-form the download URLs
  formDownloadURLs();
}

void toontownInstaller::
setDownloadServerList(const char *downloadServerList)
{
  // make sure that we're initialized
  if (!normalInit())
    return;

  char tempString[_MAX_PATH];   // string to parse server string tokens into
  // don't trust string lengths from external sources
  strlcpy(tempString, downloadServerList, _MAX_PATH);

  // make a copy to pass to the launcher
  strcpy(_DOWNLOAD_SERVER_String, tempString);

  errorLog << "server string:" << _DOWNLOAD_SERVER_String << endl;

  // First create the list of servers: downloadServer is a ';' delimited list
  int server_count = 0;
  char *tok = strtok(tempString, ";");

  while(tok != NULL) {
    _downloadServerList[server_count] = tok;
    errorLog << "ServerList[" << server_count << "]: "
                << _downloadServerList[server_count].c_str() << endl;
    tok = strtok(NULL, ";");
    ++server_count;
    if (server_count >= _MAX_ALTERNATE_SERVER) {
      errorLog << "got more than " << _MAX_ALTERNATE_SERVER << "in serverList, so ignoring the rest" << endl;
      break;
    }
  }

  // default to first on list
  if (!_downloadServerList[0].empty())
    DownloadServer(_downloadServerList[0].c_str());
}

///////////////////////////////////////////////////////////////////////////////
// Goes through list of download servers using the FULL url (with
// downloadVersion) and selects the first working one.
//
void toontownInstaller::
selectDownloadServer()
{
  bool found = false;
  string downloadFile;

  // test each download server
  for (int i = 0; i < _MAX_ALTERNATE_SERVER; i++)
  {
	// form download file URL for test
    if (_downloadServerList[i].empty())
		continue;     // skip empty
    downloadFile = _downloadServerList[i];
    downloadFile += "/";
    downloadFile += _downloadVersion;
    errorLog << "testing: " << downloadFile << endl;
    downloadFile += "/launcherFileDb";
    if (testServer(downloadFile.c_str()))
	{  // pick first working one
	  DownloadServer(_downloadServerList[i].c_str());
	  found = true;
	  break;
    }
  }

  if (!found)
  { // if none found working, try to default to first one
    if (!_downloadServerList[0].empty())
      DownloadServer(_downloadServerList[0].c_str());
  }
}
#endif

////////////////////////////////////////////////////////////////////
// this function is called to set the download 'version'. This version
// string is used to make all file URLs unique across publishes,
// to trick proxy servers that erroneously cache old files
void toontownInstaller::
DownloadVersion(const char *downloadVersion)
{
  // make sure that we're initialized
  if (!normalInit())
      return;

  strcpy(_downloadVersion, downloadVersion);
  errorLog << "Download version set to " << _downloadVersion << endl;

  // since we have a new download version, re-form the download URLs
  formDownloadURLs();
}

////////////////////////////////////////////////////////////////////
// this function is called to set the name of the game server
// this can be either an IP or a computer name
void toontownInstaller::
GameServer(const char *gameServer)
{
  // make sure that we're initialized
  if (!normalInit())
      return;

  errorLog << "Game server set to " << gameServer << endl;

  // make a copy to pass to the launcher
  strcpy(_GAME_SERVER_String, gameServer);
}

////////////////////////////////////////////////////////////////////
// this function is called to set the name of the account server
// this can be either an IP or a computer name
void toontownInstaller::
AccountServer(const char *accountServer)
{
  // make sure that we're initialized
  if (!normalInit())
      return;

  errorLog << "Account server set to " << accountServer << endl;

  // make a copy to pass to the launcher
  strcpy(_ACCOUNT_SERVER_String, accountServer);
}

// these fns cant return NULL since they are copied to string objs
const char *toontownInstaller::
getInstallerLogFileName() {
  return _installerLogFile_IFilename.getFullLocalName();
}

// there's probably a cleaner way to organize this
const char *pNoLogName = "couldnt_form_logfilename";

const char *toontownInstaller::
getLauncherExtractionLogFileName() {
  if(formLogFileNames())
      return _launcherExtractionLogFile_IFilename.getFullLocalName();
    else return pNoLogName;
}

/*
const char *toontownInstaller::
getGameLogFileName() {
  if(formLogFileNames())
      return _gameLogFile_IFilename.getFullLocalName();
  else return pNoLogName;
}
*/

// This version looks up the string from current language
// version and appends it
void toontownInstaller::
addUserError(int error_idx) {
}

void toontownInstaller::
addUserError(const char *error) {
  if(error==NULL)  // could be if strstream has never been written to, .str() returns NULL
       return;

  _userErrorString.append(error).append("\n");
}

void toontownInstaller::
addUserAccessDeniedToErrorAndLog(const char *filename) {
  char msg[1000];
  sprintf(msg,"The Toontown Installer could not overwrite a previously created Toontown file (%s). %s",
          filename,RestartIEInstrs);
  addUserErrorAndLog(msg);
}

void toontownInstaller::
addUserErrorAndLog(const char *error) {
  if(error==NULL)  // could be if strstream has never been written to, .str() returns NULL
    return;

  addUserError(error);
  errorLog << error << endl;
}

// this function combines the download server with the download
// version string, and returns the base URL from which everything should
// be downloaded
const char* toontownInstaller::
getDownloadRootURL() {
  strcpy(_downloadRootURL, _downloadServerURL);
  strcat(_downloadRootURL, _downloadVersion);
  addTrailingForwardSlash(_downloadRootURL);
  return _downloadRootURL;
}

// form the download URLs from the download server URL and
// download version strings
void toontownInstaller::
formDownloadURLs() {
  const char* downloadRootURL = getDownloadRootURL();
#ifndef _EXEINSTALLER_
  _game1_IFilename.setRemotePath(_downloadRootURL);
  _movie_IFilename.setRemotePath(_downloadRootURL);
  _game2_IFilename.setRemotePath(_downloadRootURL);
  _messages_IFilename.setRemotePath(_downloadRootURL);
  _toontune_IFilename.setRemotePath(_downloadRootURL);
#endif
  // for now, the panda server is the download server
  setPandaServer(_downloadRootURL);
}

////////////////////////////////////////////////////////////////////
// formLogFileNames() - attempts to create full filenames for the
//  "launcher install" and "python" log files
//
// this function exists because:
//  - the control user could ask for the names of the log files at any time
//  - if we formed the log file names only after "setting up the install
//    directory", a returning user with new hardware would fail before
//    getting set up in the install directory, and these two log file
//    names would not have been formed, even though they exist and may
//    have some useful information in them
bool toontownInstaller::
formLogFileNames()
{
  char installDir[_MAX_PATH];

  installDir[0]='\0';

  _launcherExtractionLogFile_IFilename.setLocalPath(installDir);
  // _gameLogFile_IFilename.setLocalPath(installDir);

  if(_regToontown.notvalid()) {
    errorLog << "formLogFiles failed, reg not initialized!\n";
    return false;
  }

  // try to get the installation dir from the registry
  if (_regToontown.getString(_INSTALL_DIR_ValueName, installDir, sizeof(installDir))) {
    errorLog << "formLogFiles error, regGetStr couldnt find TT regkey\n";
    return false;
  }

  // add a trailing slash to the install directory
  // (it's stored in the registry without one)
  addTrailingSlash(installDir);

  // what if registry entry exists, but dir does not?  Is that a possible condition?  is initInstallDir guaranteed to have run?

  // try to go to that directory
  if (!SetCurrentDirectory(installDir)) {
    errorLog << "formLogFiles error, SetCurrentDir("<<installDir<<") failed, err=" << GetLastErrorStr() << endl;
//  if (vos::chdir(installDir)) {
//    errorLog << "formLogFiles error, SetCurrentDir("<<installDir<<") failed, err=" << vos::last_error_str() << endl;
    return false;
  }

  _launcherExtractionLogFile_IFilename.setLocalPath(installDir);
  //_gameLogFile_IFilename.setLocalPath(installDir);

  char tmpbuf[_MAX_PATH];
  sprintf(tmpbuf,"%s%s-*.log",installDir,GAMELOG_BASEFILENAME);
  _gameLogPathPattern = tmpbuf;

  /* lets wait until read time to check existence
  if (!fileExists(_launcherExtractionLogFile_IFilename.getFullLocalName()))
//  if (!vos::file_exists(_launcherExtractionLogFile_IFilename.getFullLocalName()))
    _launcherExtractionLogFile_IFilename.setFullLocalName("");

  if (!fileExists(_gameLogFile_IFilename.getFullLocalName()))
//  if (!vos::file_exists(_gameLogFile_IFilename.getFullLocalName()))
    _gameLogFile_IFilename.setFullLocalName("");
  */

  return true;
}
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
// initInstallDir - returns true on success
//  get set up with installation directory
//  if we don't have one, ask user for one
//  change current directory to install directory
bool toontownInstaller::
initInstallDir() {
  int dirWasNotInRegistry = 0;
  int changeToDirFailed = 0;

  if(_regToontown.notvalid()) {
    errorLog << "initInstallDir failed: TT regkey not initialized\n";
    //return -1;
    return false;
  }

  // try to get the installation dir from the registry
  if (_regToontown.getString(_INSTALL_DIR_ValueName, _toontownInstallDir, sizeof(_toontownInstallDir)))
  { // installation dir not found in registry (this is expected if it's the initial install!)
    errorLog << "installdir not found in registry\n";
    dirWasNotInRegistry = 1;
  }
  else
  { // add a trailing slash to the install directory
    // (it's stored in the registry without one)
    addTrailingSlash(_toontownInstallDir);

    // try to go to that directory
    if (!SetCurrentDirectory(_toontownInstallDir))
	{
      DWORD errNum = GetLastError();
      string errStr = GetLastErrorStr();
//	if (vos::chdir(_toontownInstallDir)) {
//		DWORD errNum = vos::last_error_code();
//      string errStr = vos::last_error_str();
      if(errNum!=ERROR_FILE_NOT_FOUND)
        errorLog << "SetCurrentDir("<<_toontownInstallDir<<") failed, err=" << errStr << endl;
      else
        errorLog << "'" << _toontownInstallDir << "' doesnt exist yet\n";
      changeToDirFailed = 1;
    }
  }

  // if install directory was not found in registry, or we could not
  // go to the install directory, ask the user for an install directory
//	if (1)
//	{	// always touch the installation directories to make sure they exist with proper permissions
	if(dirWasNotInRegistry || changeToDirFailed)
	{
		if(!makeInstallDir(_toontownInstallDir)) {
		return false;
    }

    // set the install directory in the registry, with no trailing slash

    char temp[_MAX_PATH];
    strcpy(temp, _toontownInstallDir);
    removeTrailingSlash(temp);

    if(_regToontown.setString(_INSTALL_DIR_ValueName, temp))
      errorLog << "couldnt set install dir in registry!\n";

    // make sure we're in the install directory
    if(!SetCurrentDirectory(_toontownInstallDir)) {
      errorLog << "SetCurrentDir("<<_toontownInstallDir<<") failed, err=" << GetLastErrorStr() << endl;
//	if(vos::chdir(_toontownInstallDir)) {
//      errorLog << "SetCurrentDir("<<_toontownInstallDir<<") failed, err=" << vos::last_error_str() << endl;
      return false;
    }
  }

  // make full pathnames
#ifndef _EXEINSTALLER_
  _game1_IFilename.setLocalPath(_toontownInstallDir);
  _movie_IFilename.setLocalPath(_toontownInstallDir);
  _game2_IFilename.setLocalPath(_toontownInstallDir);
  _messages_IFilename.setLocalPath(_toontownInstallDir);
  _toontune_IFilename.setLocalPath(_toontownInstallDir);
#endif
  _launcherFileDB_IFilename.setLocalPath(_toontownInstallDir);
  _launcherDDBFile_IFilename.setLocalPath(_toontownInstallDir);
  _launcherProgress_IFilename.setLocalPath(_toontownInstallDir);
  _launcherSelfExtractor_IFilename.setLocalPath(_toontownInstallDir);
  _runLauncher_IFilename.setLocalPath(_toontownInstallDir);
  return true;
}
////////////////////////////////////////////////////////////////////

// returns true on success
bool toontownInstaller::
makeInstallDir(char *toontownInstallDir)
{
	const char *shfolder_name = "shfolder.dll";
	char defaultDir[_MAX_PATH];
#if defined(_INSTALLERSERVICE_)
	char dataDir[_MAX_PATH];
#endif
	HRESULT hr = E_FAIL, hrData = E_FAIL;
	SysInfo::OSType curr_os = _pSysInfo->get_os_type();

	defaultDir[0]='\0';
#if defined(_INSTALLERSERVICE_)
	dataDir[0] = '\0';
#endif

	if (curr_os > SysInfo::OS_Win2000)
		shfolder_name = "shell32.dll";			// can't depend on shfolder.lib to exist for long after win9x

	// make sure this uses SHGetFolderPath from shfolder.lib, NOT shell32.lib pre-NT4
	// (SHGetFolderPath doesnt exist in older win9x shell32.dll, so MS added this
	//  dll to IE as a workaround)
	HINSTANCE hShFolder = LoadLibrary(shfolder_name);

	// if we cant load shfolder.dll, just use default location
	if (!hShFolder) {
		//    ShowOSErrorMessageBox("LoadLibrary() failed on shfolder.dll.  Is IE4+ installed?");
		goto shfolder_load_failed;
	}

	const char *shfoldergetpath="SHGetFolderPathA";

	PFNSHGETFOLDERPATHA pfnShGetFPath = (PFNSHGETFOLDERPATHA) GetProcAddress(hShFolder, shfoldergetpath);
	if (!pfnShGetFPath) {
		//    ShowOSErrorMessageBox("GetProcAddr failed on SHGetFolderPathA");
		goto shfolder_load_failed;
	}

	hr =(*pfnShGetFPath)(NULL, CSIDL_PROGRAM_FILES | CSIDL_FLAG_CREATE,  // note: only succeeds for IE 5.0+
						NULL, SHGFP_TYPE_CURRENT, defaultDir);
	if(!SUCCEEDED(hr))  {
		errorLog << shfoldergetpath << " failed, hr=0x" << (void*)hr << ", lasterr=" << GetLastError() << endl;
	//      errorLog << shfoldergetpath << " failed, hr=0x" << (void*)hr << ", lasterr=" << vos::last_error_code() << endl;
	}

#if defined(_INSTALLERSERVICE_)
	hrData =(*pfnShGetFPath)(NULL, CSIDL_LOCAL_APPDATA | CSIDL_FLAG_CREATE,  // logfiles reside in user's profile
						NULL, SHGFP_TYPE_CURRENT, dataDir);
	if(!SUCCEEDED(hrData))  {
		errorLog << shfoldergetpath << " failed, hr=0x" << (void*)hr << ", lasterr=" << GetLastError() << endl;
	//      errorLog << shfoldergetpath << " failed, hr=0x" << (void*)hr << ", lasterr=" << vos::last_error_code() << endl;
	}
	else
		errorLog << "going to create dir: " << dataDir << endl;
#endif

shfolder_load_failed:

	if(!SUCCEEDED(hr))  {
		// couldn't find the user's "Program Files" folder, use default
		strcpy(defaultDir, "C:\\Program Files");
	}
#if defined(_INSTALLERSERVICE_)
	if(!SUCCEEDED(hrData))
		strcpy(dataDir, defaultDir);
#endif

	if(hShFolder)
		FreeLibrary(hShFolder);

	strlcat(defaultDir, ToontownInstallDirSubTree, _MAX_PATH-1);
#if defined(_INSTALLERSERVICE_)
	strlcat(dataDir, ToontownInstallDirSubTree, _MAX_PATH-1);
#endif

#ifdef USE_DIRECTORY_POPUPMENU
	if (directoryPopup(defaultDir, toontownInstallDir))
		return false;  // probably want to use default location instead of failing?
#else
	strcpy(toontownInstallDir, defaultDir);
#endif

	// for NT, need to create dir with RW-all attribs
	PSECURITY_ATTRIBUTES pSA=NULL;
	MySecurAttrib *pMySA;
	if(SysInfo::get_os_type() >= SysInfo::OS_WinNT)
	{
		pMySA = makeGlobalRW_SecAttr();
		if (!pMySA) {
			errorLog << "Failed to make TT dir global-writeable!\n";
			return true;  // go ahead and return success, but note the failure in log
		}
		pSA = pMySA->pSA;
	}

#if !defined(_INSTALLERSERVICE_)
	if(!makeDir(toontownInstallDir, pSA)) {
		LogOSErrorMessage("Error creating Toontown dir");
		return false;
	}
#else
	_bstr_t GameDeployment(TESTSTR);
	if (sehISFILE_MakeGameDir(0, GameDeployment.GetBSTR()))
	{
		ostringstream o;
		o << "Error creating Toontown dir " << GameDeployment;
		LogOSErrorMessage(o.str().c_str());
		::SysFreeString(GameDeployment);
		return false;
	}
#endif

#if defined(_INSTALLERSERVICE_)
	if(!makeDir(dataDir, NULL)) {
		LogOSErrorMessage("Error creating Toontown data dir");
		return false;
	}
#endif

	if (pSA != NULL) {
		free_MySecAttr(pMySA);
	}
	return true;
}

// returns 0 if successful
int toontownInstaller::
startLauncherSelfExtract()
{
  // make all the files in the toplevel dir writeable to make sure no funny stuff is going on
  string search_str(_toontownInstallDir);
  search_str.append("\\*");

  WIN32_FIND_DATA FindFileData;
  HANDLE hFileSearch = FindFirstFile(search_str.c_str(), &FindFileData);

	if (hFileSearch != INVALID_HANDLE_VALUE)
	{
		for(;;)
		{
			if ((!(FindFileData.dwFileAttributes & FILE_ATTRIBUTE_NORMAL))
				&& (!(FindFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)))
			{
				string filename(FindFileData.cFileName);
				BOOL bSuccess = SetFileAttributes(filename.c_str(), FILE_ATTRIBUTE_NORMAL);
				if(!bSuccess) {
					// ignore any .swf, since they may be playing right now and therefore unchangeable
					if(filename.find(".swf")!=string::npos)
					errorLog << "SetFileAttr('"<< FindFileData.cFileName << "') failed, error: "<< GetLastErrorStr()<<"\n";
//					errorLog << "SetFileAttr('"<< FindFileData.cFileName << "') failed, error: "<< vos::last_error_str()<<"\n";
				}
				// errorLog << "SetFileAttr('"<< FindFileData.cFileName << "') returned " << bSuccess << endl;
			}

			if (!FindNextFile(hFileSearch,&FindFileData)) {
				DWORD err=GetLastError();
				//DWORD err=vos::last_error_code();
				if(err!=ERROR_NO_MORE_FILES)
				errorLog << "FindNextFile failed with error: "<<err<<"\n";
				break;
			}
		}
		FindClose(hFileSearch);
	}

	int ec = 0;
#if defined(_INSTALLERSERVICE_)
	bool manifest_written = false;
	bool bVistaOrBetter = vos::sysinfo_t::VistaOrBetter();
	if (bVistaOrBetter)
	{	// always manually recreate manifest file with hardcoded data
		// Manifest file keeps WISE from running elevated under Vista until we stop using WISE Installation System 9
		vstr_t manifest = vstr_t(_launcherSelfExtractor_IFilename.getFullLocalName()) + ".manifest";
		HANDLE hFile = CreateFile(manifest.c_str(), FILE_WRITE_DATA, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_READONLY, NULL);
		if (hFile)
		{	  // hardcode this to avoid having to download it
			const char manifest_data[] = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\r\n\
<assembly xmlns=\"urn:schemas-microsoft-com:asm.v1\" manifestVersion=\"1.0\">\r\n\
  <ms_asmv2:trustInfo xmlns:ms_asmv2=\"urn:schemas-microsoft-com:asm.v2\">\r\n\
    <ms_asmv2:security>\r\n\
      <ms_asmv2:requestedPrivileges>\r\n\
        <ms_asmv2:requestedExecutionLevel level=\"asInvoker\" uiAccess=\"false\" />\r\n\
      </ms_asmv2:requestedPrivileges>\r\n\
    </ms_asmv2:security>\r\n\
  </ms_asmv2:trustInfo>\r\n\
</assembly>\r\n";

			DWORD written = 0;
			if (WriteFile(hFile, manifest_data, sizeof(manifest_data) - 1, &written, NULL) == 0 || written == 0)
			{
				ec = vos::last_error_code();
				errorLog << manifest << ": data could not be written. " << vos::last_error_str(ec) << endl;
			}
			else
				manifest_written = true;
			errorLog << manifest << ": " << dec << written << " written of sizeof(" << sizeof(manifest_data) << ')' << endl;
			CloseHandle(hFile);
		}
		else
			errorLog << manifest << " could not be created. " << vos::last_error_str() << endl;
	}
#endif

	// ENV_USE_TESTSERVER is set so InstallLauncher can to check that it is being run from the test/release environment it was built for
	SetEnvironmentVariable("TT_USE_TESTSERVER",CMDARG_USE_TESTSERVER_STR);

	size_t spawn_state = SPAWN_NORMAL;
	ostringstream osCmdLine;
	osCmdLine << _launcherSelfExtractor_IFilename.getFullLocalName();

#ifdef HIDE_LAUNCHER_EXTRACT
	osCmdLine << " /s";
	spawn_state = SPAWN_HIDDEN;
#endif
	string cmdLine(osCmdLine.str().c_str());	// spawnProcess needs a stack-local string

#if defined(_INSTALLERSERVICE_)
	if (!bVistaOrBetter || manifest_written)	// # Vista-mode REALLY NEEDS a manifest to exist to keep WISE from auto-elevating
#endif
		ec = spawnProcess(cmdLine.c_str(), spawn_state, &_hInstallLauncherProcess, NULL);

	return ec;
}

// returns 0 if launcher has not been extracted,
// 1 if it has
int toontownInstaller::
launcherHasBeenExtracted() {
  DWORD Done;
  return !_regToontown.getDWORD(_LAUNCHER_EXTRACTED_ValueName, Done);
}

// returns 0 if launcher self-extract is not done
// returns 1 if launcher self-extract ended normally
// returns 2 if launcher self-extract ended prematurely
int toontownInstaller::
launcherSelfExtractDone() {
  if (!processActive(_hInstallLauncherProcess)) {
    // return 2 if value is not in reg
    if (launcherHasBeenExtracted()) {
      // self-extract completed normally
      errorLog << "launcherSelfExtractDone(): self-extract completed normally"
               << endl;
      return 1;
    }
    // self-extract was interrupted
    errorLog << "launcherSelfExtractDone(): self-extract was interrupted"
             << endl;
    return 2;
  }
  //errorLog << "launcherSelfExtractDone(): self-extract not finished"
  //         << endl;
  return 0;
}

// returns 0 if successful
int toontownInstaller::
runLauncher()
{
  char cmdLine[1024];
  int result;
  int show;

  // make sure we're in the install directory
  if (!SetCurrentDirectory(_toontownInstallDir))
//  if (vos::chdir(_toontownInstallDir))
  {
    errorLog << "SetCurrentDir("<<_toontownInstallDir<<") failed, err=" << GetLastErrorStr() << endl;
//    errorLog << "SetCurrentDir("<<_toontownInstallDir<<") failed, err=" << vos::last_error_str() << endl;
    return 1;
  }

  // clear out any existing python path in the environment
  SetEnvironmentVariable("PYTHONPATH", "");

//  #define ACCOUNTSERVER_DBG_NOCONNECT
  #ifdef ACCOUNTSERVER_DBG_NOCONNECT
  strcpy(_ACCOUNT_SERVER_String, "nowherexx");
  #endif

  //  #define GAMESERVER_DBG_NOCONNECT
#ifdef GAMESERVER_DBG_NOCONNECT
  strcpy(_GAME_SERVER_String, "nowherexx");
#endif

  //  #define DOWNLOADSERVER_DBG_NOCONNECT
#ifdef DOWNLOADSERVER_DBG_NOCONNECT
  strcpy(_DOWNLOAD_SERVER_String, "nowherexx");
#endif

  // There is a limit of 255/256 characters that you can pass at the command line
  // So we have to be careful not to exceed this limit. Since, download_server_string could
  // be very long, we are going to write it on a registry and launcher.py will read it 
  // from that registry.
  if(_regToontown.setString(_DOWNLOAD_SERVER_ValueName, _DOWNLOAD_SERVER_String)) {
    errorLog << "couldn't set download server in registry!\n";
    return 1;
  }

  // The test server flag (CMDARG_USE_TESTSERVER) for the launcher is a 0/1 bool after the account server
  sprintf(cmdLine, "\"%s\" -OO \"%s\" \"%s\" %d",
          _runLauncher_IFilename.getFullLocalName(),
          _GAME_SERVER_String, _ACCOUNT_SERVER_String, CMDARG_USE_TESTSERVER);

  if(!_configrc_args.empty()) {
    strcat(cmdLine," \"");
    strcat(cmdLine,_configrc_args.c_str());
    strcat(cmdLine,"\"");
  }

#if 0
  // put this off until hackers get serious about running TT outside IE

  // write encoded time to registry so Launcher.py can authenticate the launching process
  if(!store_encoded_time()) {
    errorLog << "Error: couldn't write registry\n";
    return 1;
  }
#endif

/*
  // delete the old toontown.log so the file creation date will reflect last run time
  const char *pGameLogName=getGameLogFileName();

  if(fileExists(pGameLogName)) {
//  if(vos::file_exists(pGameLogName)) {
	if(!deleteFile(pGameLogName)) {
		errorLog << "Warning: couldnt delete old gamelog " << pGameLogName << ", log file date warning msg may be incorrect, possible other TT instance running\n";
	}
  }
 */

  //keep only NUM_LOGS_TO_KEEP toontown.log's at a time
  if(formLogFileNames())
    deleteOldLogs(_gameLogPathPattern.c_str());

  errorLog << "Running Launcher " << endl;
#if _DEBUG
  // This is a little too useful for potential hackers
  errorLog << cmdLine << endl;
#else
  if(!_configrc_args.empty())
    errorLog << "ExtraArgs: " << _configrc_args << endl;
  errorLog << "Using TestServer: " << CMDARG_USE_TESTSERVER << endl;
  errorLog << "Download Server: " << _DOWNLOAD_SERVER_String << endl;
  errorLog << "Game Server: " <<  _GAME_SERVER_String << endl;
  errorLog << "Account Server: " <<  _ACCOUNT_SERVER_String << endl;
#endif

#ifdef HIDE_LAUNCHER
  show = SPAWN_HIDDEN;
#else
  show = SPAWN_NORMAL;
#endif

  /*
  // DO NOT SET THIS UNTIL POPEN IS FIXED IN DTOOL FOR WIN98

  // Tell configrc to run the executable, not to read the configrc file
  // We have to change the equals sign to percent signs because windows
  // does not like having multiple equals signs in the same variable
  if (!SetEnvironmentVariable("CONFIG_CONFIG", ":!:configsuffix!.exe")) {
    return 1;
  }
  */

#if defined(_INSTALLERSERVICE_)
  if ( vos::sysinfo_t::VistaOrBetter() )
//  if (1)
  {	  // if in Vista, have ActiveX spawn it in order to run in medium security integrity since Win32 SDK lacks setuid()
/*
	  _bstr_t bsAppPath(_runLauncher_IFilename.getFullLocalName()),
			bsCmdLine(cmdLine);
	  result = sehISPROC_rforkexec(bsAppPath, bsCmdLine, _LauncherProcessID, _hLauncherProcess);
	  errorLog << "sehISPROC_rforkexec() result: " << result << ' ' << _LauncherProcessID << ' ' << _hLauncherProcess << endl;
*/
	  vchar_t *args[] = { (vchar_t *) cmdLine, '\0' };
	  pid_t pid;
	  _hLauncherProcess = NULL;
	  result = vos::rfork_execve(_runLauncher_IFilename.getFullLocalName(), args, NULL, pid);
	  _LauncherProcessID = (DWORD) pid;

	  if (result == 0 && (_LauncherProcessID != 0))
		  _hLauncherProcess = vos::process_handle(_LauncherProcessID);
	  else
		  _hLauncherProcess = NULL;
  }
  else
#endif
  {	  // returns 0 on success
	  result = spawnProcess(cmdLine, show, &_hLauncherProcess,&_LauncherProcessID);
  }

  // if we succeeded, return 0
  if (result == 0) {
    // signal that we're going to kill the launcher on premature termination
    _OK_To_Kill_LauncherProcess = 1;

#if 0
    // this doesnt seem to work for some reason (AllowSetForegnd returns error 87, invalid arg
    // if we pass the pid, and ASFW_ANY definitely doesnt fix the seeing IE in TT window prob)

    // call AllowSetForeground to let the spawned process (esp. panda) set Foregnd Win
    // should only work on 2000/XP  (ME will have a non-functioning version)
    HINSTANCE hUser=LoadLibrary("user32.dll");  // this should never fail, I hope
    if(hUser) {
      typedef BOOL (WINAPI *ALLOWSETFOREGROUNDWINDOW)(DWORD dwProcessId);
      const char *pAllowStr="AllowSetForegroundWindow";

      ALLOWSETFOREGROUNDWINDOW pAllowSetFgndWin = (ALLOWSETFOREGROUNDWINDOW)GetProcAddress(hUser, pAllowStr);
      if(pAllowSetFgndWin!=NULL) {
        // this fails with invalid param for some reason, so just let anyone do SetFGndWin
        if((*pAllowSetFgndWin)(_LauncherProcessID)) {
          //             if((*pAllowSetFgndWin)(ASFW_ANY)) {
          errorLog << pAllowStr << "("<<_LauncherProcessID << ") succeeded\n";
        }
		else
          errorLog << pAllowStr << "("<<_LauncherProcessID << ") failed, err: " << GetLastErrorStr() << endl;
//          errorLog << pAllowStr << "("<<_LauncherProcessID << ") failed, err: " << vos_os::last_error_str() << endl;
      }
      FreeLibrary(hUser);
    }
#endif
  }

  return result;
}

// returns 0 if panda window is not yet open
int toontownInstaller::
pandaWindowOpen()
{
  DWORD pandaWindowOpen;
  if (_regToontown.getDWORD(_PANDA_WINDOW_OPEN_ValueName, pandaWindowOpen) != 0)
  { // return zero if value is not in reg
    return 0;
  }
  else
  { // remove value, return 1
    _regToontown.deleteValue(_PANDA_WINDOW_OPEN_ValueName);
    return 1;
  }
}

// set the value of a particular key; returns 0 on success
int toontownInstaller::
setKeyValue(const char *key, const char *value) {
  if(_regToontown.notvalid()) {
    // get that registry open, in case it isnt already (i.e. if we're called from showBugReport or submitConfig page, not installer.php)
    do_basic_init();
  }

  if (keyMatch(key, "Green")) {
    setGreen(value);
  } else if (keyMatch(key, "Blue")) {
    setBlue(value);
  } else if (keyMatch(key, "PlayToken")) {
    PlayToken(value);
  } else if (keyMatch(key, "LastLogin")) {
    setLastLogin(value);
  } else if (keyMatch(key, "SWID")) {
    setSWID(value);
  } else if (keyMatch(key, "DownloadURL")) {
    strcpy(_downloadServerURL, value);  
  } else if (keyMatch(key, "DownloadServer")) {
#if 0	// temporary code to test something
    value = "http://download.toontown.com;http://a.download.toontown.com";
    errorLog << "fake server string: " << value << endl;
#endif
    DownloadServer(value, true);
  } else if (keyMatch(key, "DownloadVersion")) {
    DownloadVersion(value);
  } else if (keyMatch(key, "GameServer")) {
    GameServer(value);
  } else if (keyMatch(key, "AccountServer")) {
    AccountServer(value);
  } else if (keyMatch(key, "StatServer")) {
    _ConfigStatsServerTargetURL=value;
  }
#ifndef _EXEINSTALLER_
  else if (keyMatch(key, "Game1_Done")) {
    game1IsDone();
  } else if (keyMatch(key, "Game2_Done")) {
    game2IsDone();
  } else if (keyMatch(key, "Game1_Version")) {
    setGame1Version(value);
  } else if (keyMatch(key, "Movie_Version")) {
    setMovieVersion(value);
  } else if (keyMatch(key, "Game2_Version")) {
    setGame2Version(value);
  } else if (keyMatch(key, "Messages_Version")) {
    setMessagesVersion(value);
  } else if (keyMatch(key, "Toontune_Version")) {
    setToontuneVersion(value);
  //} else if (keyMatch(key, "LauncherMessage")) {
  }
#endif
  else if (keyMatch(key, "AddUserErrorMessage")) {
    addUserError(value);
  } else if (keyMatch(key, "RemoteErrorPageURL")) {
    CreateErrorPage(value);
  } else if (keyMatch(key, "ReferrerCode")) {
    setReferrerCode(value);
  } else if (keyMatch(key, "ConfigSubmitApproved")) {
    DWORD newVal=1;
    if(value[0]=='0') {
      newVal=0;
    }
    _regToontown.setDWORD(_configSubmitApprovedRegValName, newVal);
    _bConfigSubmitApproved = (newVal!=0);

    /*
    // for testserver, when user accepts, move from state 7 to 10
    _StateCode = 10;  faster?
    runInstaller();
    */
  } else if (keyMatch(key,"TrialEligible")) {
    // lets set a registry variable (not in toontown install directory) to check hacking
    setPreventHack(atoi(value));
  } else if (keyMatch(key,"TrialEligible2")) {
    // lets set a registry variable (not in toontown install directory) to check hacking
    setPreventHack2(value);
  } else if (keyMatch(key,"ChatEligible")) {
    // lets set a registry variable to check paid user but no parent password
    setChatEligible(atoi(value));
  } else if (keyMatch(key,"WebAccountParams")) {
    // lets set a registry to all chat related params which the client will parse
    WebAccountParams(value);
  } else if (keyMatch(key,"FromCD")) {
    // set a registry indicating if a cd version patch
    _regToontown.setDWORD(_PATCH_FROM_CD_ValueName, atoi(value));
  } else if (keyMatch(key, "Deployment")) {
    // set a registry indicating which language version it is
	Deployment(value);
  } else if (keyMatch(key, "WindowTitle")) {
    // set the title of the launcher page
    installer_window_title.assign(value);
  } else if (keyMatch(key, "MissedRequirements")) {
    // set the title of the launcher page
    missed_requirements_php.assign(value);
  } else if (keyMatch(key, "GraphicsDriver")) {
    // set the title of the launcher page
    graphics_driver_php.assign(value);
  } else {
    // unrecognized key, hand it off to the base class
    return installerBase::setKeyValue(key, value);
  }
  return 0;
}

// get the value of a particular key; returns false on failure
bool toontownInstaller::
getKeyValue(const char *keyName, string &keyValue) {
  if(_regToontown.notvalid()) {
    // get that registry open, in case it isn't already
    // (i.e. if we're called from showBugReport or
    // submitConfig page, not installer.php)
    do_basic_init();
  }

  char tempBuf[30]; // for integer-to-ASCII conversion
  if (keyMatch(keyName, "StateCode")) {
    _itoa(statecode(), tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "PercentLoaded")) {
    _itoa(getPercentLoaded(), tempBuf, 10);
    keyValue = tempBuf;
  }
#ifndef _EXEINSTALLER_
  else if (keyMatch(keyName, "LauncherMessage")) {
    keyValue = getLauncherMessage();
  } else if (keyMatch(keyName, "Game1Filename")) {
    keyValue = getGame1Filename();
  } else if (keyMatch(keyName, "MovieFilename")) {
    keyValue = getMovieFilename();
  } else if (keyMatch(keyName, "Game2Filename")) {
    keyValue = getGame2Filename();
  } else if (keyMatch(keyName, "MessagesFilename")) {
    keyValue = getMessagesFilename();
  }
#endif
  else if (keyMatch(keyName, "InstallerLogFileName")) {
    keyValue = getInstallerLogFileName();
  } else if (keyMatch(keyName, "LauncherExtractionLogFileName")) {
    keyValue = getLauncherExtractionLogFileName();
  /*
  } else if (keyMatch(keyName, "GameLogFileName")) {
    keyValue = getGameLogFileName();
  */
  } else if (keyMatch(keyName, "UserErrorString")) {
    keyValue = _userErrorString;
  } else if (keyMatch(keyName, "ToontownNotes")) {
    keyValue = CreateErrorString();
  } else if (keyMatch(keyName, "LocalErrorPageData")) {
    keyValue = getLocalErrorPageData();
  } else if (keyMatch(keyName, "UserLoggedIn")) {
    keyValue = getUserLoggedIn();
  } else if (keyMatch(keyName, "PaidUserLoggedIn")) {
    keyValue = getPaidUserLoggedIn();
  } else if (keyMatch(keyName, "ConfigSubmitApproved")) {
    DWORD curVal = _regToontown.getDWORD(_configSubmitApprovedRegValName);
    // not found same as not approved
    _bConfigSubmitApproved = (curVal!=0);
    // convert bool flag to string '1' or '0' since all getValue returns must be strings currently
    // (maybe need to make separate GetInt() and GetString() entry points for jscript)
    char valstr[2];
    valstr[1]='\0';
    valstr[0]='0'+(int)_bConfigSubmitApproved;
    keyValue = valstr;
  } else if (keyMatch(keyName, "ConfigInfoRecord")) {
    if(_pSysInfo==NULL) {
      validHardware();
    }

    CreateConfigInfoRecord();
    keyValue = _ConfigInfo;
  } else if (keyMatch(keyName, "ExitPage")) {
    keyValue = getExitPage();
  } else if (keyMatch(keyName, "JustCheckSystemPage")) {
    // THIS VALUE SHOULD ONLY BE GET IF YOU WANT THE INSTALLER
    // TO CHECK SYSTEM AND HARDWARE AND DO NOTHING MORE
    // NO LOGGING WILL BE PERFORMED, SO THAT THE GENERATED ERROR
    // PAGE WILL CONTAIN THE LOG FILES FROM THE PREVIOUS RUN

    //DBG("calling func justCheck");
    _itoa(justCheckSystemPage(), tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "JustMakeErrorPage")) {
    // THIS VALUE SHOULD ONLY BE GET IF YOU WANT THE INSTALLER
    // TO GENERATE AN ERROR PAGE AND DO NOTHING MORE
    // NO LOGGING WILL BE PERFORMED, SO THAT THE GENERATED ERROR
    // PAGE WILL CONTAIN THE LOG FILES FROM THE PREVIOUS RUN
    _itoa(justMakeErrorPage(), tempBuf, 10);
    keyValue = tempBuf;
    //DBG(_userErrorString.c_str());
  } else if (keyMatch(keyName, "PercentLauncherDownloaded")) {
    _itoa((int)(_PercentFileDownloaded*100), tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "OverallPercentLoaded")) {
    _itoa(getOverallPercentLoaded(), tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "TrialEligible")) {
    _itoa(getPreventHack(), tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "TrialEligible2")) {
    keyValue = getPreventHack2();
  } else if (keyMatch(keyName,"CDRom")) {
    DWORD kval = _regToontown.getDWORD(_CDROM_ValueName);
    _itoa(kval, tempBuf, 10);
    keyValue = tempBuf;
  } else if (keyMatch(keyName, "Deployment")) {
    keyValue = Deployment();
  } else if (keyMatch(keyName,"PandaErrorCode")) {
    DWORD kval = _regToontown.getDWORD(_PANDA_ERROR_CODE_ValueName);
    _itoa(kval, tempBuf, 10);
    keyValue = tempBuf;
  } else {
    // unrecognized key, hand it off to the base class
    return installerBase::getKeyValue(keyName,keyValue);
  }
  return true;
}

string toontownInstaller::
getUserLoggedIn() {
  return _regToontown.getString(_USER_LOGGED_IN_ValueName);
}

string toontownInstaller::
getPaidUserLoggedIn() {
  return _regToontown.getString(_PAID_USER_LOGGED_IN_ValueName);
}

string toontownInstaller::
getExitPage() {
  return _regToontown.getString(_EXIT_PAGE_ValueName);
}

void toontownInstaller::
setReferrerCode(const char *referrerCode) {
  // if there is already a referrer code in the registry:
  //   if existing referrer code does not end in "_DUP":
  //     append "_DUP" to referrer code and re-write it
  // else:
  //   write this referrer code to registry

  string rc;
  if (0 == _regToontown.getString(_REFERRER_CODE_ValueName, rc)) {
    const string suffix("_DUP");
    size_t sufLen = suffix.length();
    if ((rc.length() <= sufLen) ||
        (rc.substr(rc.length()-sufLen, sufLen) != suffix))
    {
      rc += suffix;
      _regToontown.setString(_REFERRER_CODE_ValueName, rc);
    }
  } else {
    // put this referrer code into the registry
    _regToontown.setString(_REFERRER_CODE_ValueName, referrerCode);
  }
}

void toontownInstaller::
readLogFile(const char *header,const char *footer,const char *logFileName, ostringstream &dest, int endbytes_to_read) {
  // need to echo msgs twice since writes to errorLog after this point wont be read
  #define SHOWERROR(ERRMSG) { errorLog << ERRMSG;  dest << ERRMSG; }

  if((logFileName==NULL) || !fileExists(logFileName)) {
//	if((logFileName==NULL) || !vos::file::exists(logFileName)) {
    SHOWERROR("log file '" << logFileName << "' doesn't exist!\n");
    return;
  }

  dest << header << endl;

  unsigned __int64 logSize = getFileSize(logFileName);
//  uint64_t logSize = vos::file::size(logFileName);

  bool bReadFileTail = false;

  if((endbytes_to_read>0) && (logSize>0) && (logSize > endbytes_to_read)) {
    bReadFileTail=true;
  }

  FILE *hLogFile = fopen( logFileName, "rb" );
  if(hLogFile==NULL) {
    SHOWERROR("failed to open '"<<logFileName << endl);
    return;
  }

  if(logSize!=-1) {
    SHOWERROR("reading '"<<logFileName<<"': ");
    if(bReadFileTail) {
      SHOWERROR("last " << endbytes_to_read << " bytes\n");
    } else {
      SHOWERROR(logSize << " bytes\n");
    }
  }

  if(bReadFileTail) {
    int retVal=fseek(hLogFile,-((int)endbytes_to_read),SEEK_END);
    if(retVal!=0) {
      SHOWERROR("fseek failed, retVal = " << retVal << endl);
    }
  }

  unsigned int count=0;
  unsigned char ch = fgetc(hLogFile);

  while(!feof(hLogFile)) {
    if (isprint(ch) || isspace(ch)) {
      dest.put(ch);
    } else {
      dest.put('#');
    }
    count++;
    ch = fgetc(hLogFile);
  }
  dest << endl;
  fclose(hLogFile);

  errorLog << "read " << count << " bytes from " << logFileName << endl;
  dest << "read " << count << " bytes from " << logFileName << endl;
  dest << footer << endl;
}

//
// Test function to see if idea of showing remote string table will work
// wheeee, it works! great!
//
void toontownInstaller::
ShowLocalizedMessage(char *whatStr) {
  std::string fileStr;
  char showStr[1024], titleStr[1024];
  //char remoteURL[] = "http://ttown2.online.disney.com:4201/localizedEnglish.txt";
  char localizedFileURL[MAX_PATH];
  strcpy(localizedFileURL, _downloadServerURL);
  strcat(localizedFileURL, "localizedErrorMsg.txt");

  // download the file
  if (!downloadToMem(localizedFileURL, fileStr)) {
    errorLog << "downloadtoMem("<<localizedFileURL<<") failed!\n";
    return;
  }
  // lets parse these strings
  // first find the title of the message box
  string::size_type index = fileStr.find("Toontown_Installer_Error");
  string::size_type si, ei;
  if (index != string::npos) {
    // find the index where it's string starts and ends
    si = fileStr.find_first_of('"',index);
    si += 1;
    ei = fileStr.find_first_of('"',si);
    fileStr.copy(titleStr,ei-si,si);
    titleStr[ei-si]=0;
  }
  // then find the particular error to show in the message box
  index = fileStr.find(whatStr);
  if (index != string::npos) {
    // find the index where it's string starts and ends
    si = fileStr.find_first_of('"',index);
    si += 1;
    ei = fileStr.find_first_of('"',si);
    fileStr.copy(showStr,ei-si,si);
    fileStr[ei-si]=0;
  }
  MessageBox( NULL, showStr, titleStr, MB_OK | MB_ICONWARNING );
}

// bakes part of the presentation string to errorpages. This bakes the
// log files names, and some headers and delimeters
void toontownInstaller::
CreateLogFilesStr(ostringstream &logFilesStr)
{
  FILETIME installerlogdate,gamelogdate;
//  vos::vtime_t time_installerlog, time_gamelog;
  StrVec LogFiles;
  bool bInstallerLogExists=true;
  const char *endMarker="====";
  const char *pInstallerLogName = _installerLogFile_IFilename.getFullLocalName();

  // read the current log if written
  if (!fileExists(pInstallerLogName)) {
//  if (!vos::file::exists(pInstallerLogName)) {
    //DBG(pInstallerLogName);
    getAllFilesWithPathPattern(_installerLogPathPattern.c_str(),LogFiles);

    if(!LogFiles.empty()) {
      //should be sorted oldest first due to logfilename suffix convention, so just pick the last one
      pInstallerLogName=LogFiles[LogFiles.size()-1].c_str();
    } else {
      bInstallerLogExists=false;
      logFilesStr << "No installer logs found!\n";
    }
  }

  getFileDate(pInstallerLogName,&installerlogdate);
//  time_installerlog = vos::file::birthtime(pInstallerLogName);
  readLogFile("=== Installer Log ===",endMarker,pInstallerLogName, logFilesStr);
  logFilesStr << endl;
  
  char tempName[_MAX_PATH];
  const char *pGameLogName = NULL;
  StrVec GameLogFiles;
  bool bGameLogExists = true;

  // read the current game log if written

  if(0 == _regToontown.getString(_GAMELOG_FILENAME_ValueName, tempName, sizeof(tempName))) {
#ifdef PRINT_TAIL_OF_ALL_LOGS
    getAllFilesWithPathPattern(_gameLogPathPattern.c_str(),GameLogFiles);
#endif
    if (fileExists(tempName))
//	if (vos::file::exists(tempName))
      pGameLogName = tempName;
  }
  else  // find most recent toontown-*.log
  {
    //DBG(tempName);
    getAllFilesWithPathPattern(_gameLogPathPattern.c_str(),GameLogFiles);
    if(!GameLogFiles.empty()) {
      // suffix of toontown-[suffix].log should guarantee they are sorted oldest first,
      // want only most recent
      pGameLogName = GameLogFiles[GameLogFiles.size()-1].c_str();
    }
    else {
      bGameLogExists = false;
      logFilesStr << "=== no toontown-*.log log files found! ===\n";
    }
  }

  if (bGameLogExists) {
    string tailheaderstr = "=== Tail of Game Log ===";
    string headerstr = "=== Full Game Log ===";
    string endmarkerstr = endMarker;
      
    if(bInstallerLogExists) {
      getFileDate(pGameLogName,&gamelogdate);
      bool bOutofDateGameLog =(CompareFileTime(&installerlogdate,&gamelogdate)==1);
      if(bOutofDateGameLog) {
//		time_gamelog = vos::file::birthtime(pGameLogName);
//      if(time_installerlog > time_gamelog) {
        const char *pWarningStr="  (warning: check log dates, game log may be OLDER than installer log, so installer log errors could be more relevant!)";
        tailheaderstr.append(pWarningStr);
        headerstr.append(pWarningStr);
        endmarkerstr.append(pWarningStr);
      }
    }
    // sometimes logs get mysteriously truncated in the submission process,
    // so echo important tail of log as soon as we can
#define GAMELOG_TAILSIZE 6000
  
#ifdef PRINT_TAIL_OF_ALL_LOGS
    errorLog << "Number of game logs = " << GameLogFiles.size() << endl;
    for (int i = 0; i < (int)GameLogFiles.size(); ++i) {
      string tempstr = "=== *ignore* tail of game log " + GameLogFiles[i] + " ===";
      readLogFile(tempstr.c_str(),endmarkerstr.c_str(),GameLogFiles[i].c_str(),logFilesStr,GAMELOG_TAILSIZE);
      logFilesStr << endl;
    }
#endif
    readLogFile(tailheaderstr.c_str(),endmarkerstr.c_str(),pGameLogName,logFilesStr,GAMELOG_TAILSIZE);
    logFilesStr << endl;
    readLogFile(headerstr.c_str(),endmarkerstr.c_str(),pGameLogName,logFilesStr);
  }
}

// downloads the HTML template for the error page (usually 'reportBug.php') from remoteURL,
// replaces string markers like --userErrorString-- with actual error text, and saves the result
// as an char string of HTML text in _localErrorPageData
// This function is changed as of 12/16/2003. Instead of grabbing the most recent logs
// it now grabs the log that was written for this run of TT. This should eliminate
// the bug where wrong log (due to time change in client machine) is picked on bug reporting
void toontownInstaller::
CreateErrorPage(const char *remoteURL)
{
  (void) formLogFileNames();  // ok if some lognames cant be formed yet

  // download the help page, replace special tags
  // with user error messages and log files

  std::string fileStr;

  // download the file
  if(!downloadToMem(remoteURL,fileStr)) {
    errorLog << "downloadtoMem("<<remoteURL<<") failed!\n";
    return;
  }

  errorLog.flush();

  // load in the log files
  ostringstream logFilesStr;

  CreateLogFilesStr(logFilesStr);

  // replace the tags in the file
  const std::string userErrorStringTag("---userErrorString---");
  const std::string logFilesTag("---Toontown Notes---");
  string::size_type index;

  while (string::npos != (index = fileStr.find(userErrorStringTag))) {
    fileStr.replace(index, userErrorStringTag.length(), _userErrorString);
  }

  while (string::npos != (index = fileStr.find(logFilesTag))) {
    fileStr.replace(index, logFilesTag.length(), logFilesStr.str());
  }

  // also save the HTML data in memory as a string
  _localErrorPageData = fileStr;
}

// Instead of downloading the template, just bake replacement string
// and return it. Replaces string markers like --userErrorString--
// with actual error text.
const char *toontownInstaller::
CreateErrorString() {
  formLogFileNames();  // ok if some lognames cant be formed yet
  errorLog.flush();

  std::string fileStr;

  // load in the log files
  ostringstream logFilesStr;

  CreateLogFilesStr(logFilesStr);

  // append the tags of userErrorString and Toontown Notes
  //fileStr.append(_userErrorString);
  fileStr.append(logFilesStr.str());

  _localErrorPageData = fileStr;
  return _localErrorPageData.c_str();
}

const char *toontownInstaller::
getLocalErrorPageData() {
  // return the complete html error page
  return _localErrorPageData.c_str();
}

void toontownInstaller::
do_basic_init(void)
{
  // do init that is required for non-startup tasks like accessing the registry using getValue, etc

  // open up the registry
  if (regInit()) {
    // if we get an error, _hKeyToontown will be NULL, but
    // code below should handle that case ok and just look for
    // installer log

    // ShowErrorBox("error opening registry in JustMakeErrPg!");
  }

  // get the installation directory
  if (initInstallDir()) {
    // construct the full log file names
    formLogFileNames();
  }
}

int toontownInstaller::
justMakeErrorPage(/*const char *remoteURL*/) {
  // cant really use errorLog in this fn because log hasnt been created and we dont want to overwrite it,
  // since grabbing it is the whole point of this fn
  int exitCode = 13;

  // make sure we haven't already been initialized (this should be a programming error)
  if (_initialized) {
    ShowErrorBox("ERROR: 'JustMakeErrorPage' called with installer in normal mode of operation");
    return exitCode;
  }

  // do some renegade initialization
  do_basic_init();

  // download the template error page, fill it in with the log files,
  // and write it to disk
  //CreateErrorPage(remoteURL);

  // close the registry
  regShutdown();

  return exitCode;
}
int toontownInstaller::
justCheckSystemPage(/*const char *remoteURL*/) {
  // This function gets the system info through do_basic_init() and
  // then by calling validHardware(). If everything goes well it
  // shows the passed system check and proceeds with the installation
  // else it returns an error code so that an error page could be shown.
  int exitCode = 140;  // This matches the statecode value so that
                       // Matt can redirect to proper error page

  // make sure we haven't already been initialized (this should be a programming error)
  if (_initialized) {
    ShowErrorBox("ERROR: 'JustCheckSystemPage' called with installer in normal mode of operation");
    return exitCode;
  }

  // do some renegade initialization
  //  normalInit();
  // lets try a basic init...see if that fixes the ie crash
  do_basic_init();
  //DBG("Did basic Init");

  // download the template error page, fill it in with the log files,
  // and write it to disk

  //DBG(graphics_driver_php.c_str());
  //DBG(missed_requirements_php.c_str());

  Type retVal = validHardware();
  if (retVal != HARDWARE_VALID) {
    // DBG("Invalid hardware detected");
    setKeyValue("AddUserErrorMessage", "");
    errorLog << "Invalid hardware detected" << endl;
    if (retVal == HARDWARE_INVALID_3D) {
      exitCode = 24;
      //CreateErrorPage(graphics_driver_php.c_str());
    }
    else {
      exitCode = 21;
      //CreateErrorPage(missed_requirements_php.c_str());
    }
  }
  
  // shut down whatever normalInit started
  //shutdown();
  // basic_init only inited the registry
  regShutdown();
  return exitCode;
}

bool toontownInstaller::
set_proxy_spec(const string &proxy_spec, const string &direct_hosts)
{
  bool okflag = true;

  if (proxy_spec.empty()) {
    // if no proxy, delete any existing PROXY_SERVER value
    _regToontown.deleteValue(_PROXY_SERVER_ValueName);
  }
  else {
    // write the proxy server info to the registry
    if (!_regToontown.setString(_PROXY_SERVER_ValueName, proxy_spec))
      okflag = false;
  }

  if (direct_hosts.empty()) {
    _regToontown.deleteValue(_PROXY_DIRECT_HOSTS_ValueName);
  }
  else {
    if (!_regToontown.setString(_PROXY_DIRECT_HOSTS_ValueName, direct_hosts))
      okflag = false;
  }

  return okflag;
}


void toontownInstaller::
checkProxyServer() {
  // get rid of existing proxy server string by default
  _regToontown.deleteValue(_PROXY_SERVER_ValueName);
  // errorLog << "checking proxy settings...." << endl;
  determine_proxy_spec();
  _bHTTPproxyIsUsed = !_proxy_spec.empty();

  // if no proxy, this deletes any existing proxy regkey
  set_proxy_spec(_proxy_spec, _direct_hosts);
}

#if 0
//+     Function : ModifyDefaultDacl
//Synopsis : Add EVERYONE ACE to the process token DACL.
bool ModifyDefaultDacl(void) {
  int                      i;
  ACL_SIZE_INFORMATION     asi;
  ACCESS_ALLOWED_ACE       *pace;
  DWORD                    dwNewAclSize;
  DWORD                    dwSize            = 0;
  DWORD                    dwTokenInfoLength = 0;
  HANDLE                   hToken            = NULL;
  PACL                     pacl              = NULL;
  PSID                     psidEveryone      = NULL;
  SID_IDENTIFIER_AUTHORITY siaWorld = SECURITY_WORLD_SID_AUTHORITY;
  TOKEN_DEFAULT_DACL       tddNew;
  TOKEN_DEFAULT_DACL       *ptdd    = NULL;
  TOKEN_INFORMATION_CLASS  tic      = TokenDefaultDacl;
  char                     *errstr=NULL;

  __try {

     //
     // Obtain an access token.
     //
     if (!OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY | TOKEN_ADJUST_DEFAULT, &hToken)) {
       errstr = "OpenProcessToken";
       __leave;
     }

     // Obtain buffer size for DACL information.
     if (!GetTokenInformation(hToken, tic, (LPVOID)NULL,
                              dwTokenInfoLength, &dwSize))
     {
       if (GetLastError() == ERROR_INSUFFICIENT_BUFFER)
//       if (vos::last_error_code() == ERROR_INSUFFICIENT_BUFFER)
       {
         ptdd = (TOKEN_DEFAULT_DACL *) LocalAlloc(LPTR, dwSize);
         if (ptdd == NULL) {
           errstr = "LocalAlloc 1";
           __leave;
         }
         if (!GetTokenInformation(hToken, tic, (LPVOID)ptdd, dwSize,
                                  &dwSize)) {
           errstr = "GetTokenInformation 2";
           __leave;
         }
       }
       else {
         errstr = "GetTokenInformation 1";
         __leave;
       }
     }         //
     // Obtain ACL information.
     //
     if (!GetAclInformation(ptdd->DefaultDacl, (LPVOID)&asi,
                            (DWORD)sizeof(ACL_SIZE_INFORMATION),
                            AclSizeInformation))
     {
       errstr = "GetAclInformation";
       __leave;
     }

     // Create SID for the Everyone group.
     if (!AllocateAndInitializeSid(&siaWorld, 1, SECURITY_WORLD_RID, 0,
                                   0, 0, 0, 0, 0, 0, &psidEveryone)) {
       errstr = "AllocateAndInitializeSid";
       __leave;
     }

     // Compute the size of the new ACL.
     dwNewAclSize = asi.AclBytesInUse + sizeof(ACCESS_ALLOWED_ACE) +
                    GetLengthSid(psidEveryone) - sizeof(DWORD);

     // Allocate buffer for the new ACL.
     pacl = (PACL) LocalAlloc(LPTR, dwNewAclSize);
     if (pacl == NULL) {
       errstr = "LocalAlloc 2";
       __leave;
     }

     // Intialize the ACL.
     if (!InitializeAcl(pacl, dwNewAclSize, ACL_REVISION)) {
       errstr = "InitializeAcl";
       __leave;
     }

     // Loop through all the ACEs.
     for (i = 0; i < (int) asi.AceCount; i++) {
       // Get current ACE.
       if (!GetAce(ptdd->DefaultDacl, i, (LPVOID *)&pace)) {
         errstr = "GetAce";
         __leave;
       }

       // Build the new ACL.
       if (!AddAce(pacl, ACL_REVISION, MAXDWORD, pace,
                   ((PACE_HEADER)pace)->AceSize)) {
         errstr = "AddAce";
         __leave;
       }
     }

     // Add the new ACE.
     if (!AddAccessAllowedAce(pacl, ACL_REVISION, GENERIC_ALL,
                              psidEveryone)) {
       errstr = "AddAccessAllowedAce";
       __leave;
     }

     // Set the new Default DACL.
     tddNew.DefaultDacl = pacl;
     if (!SetTokenInformation(hToken, tic, (LPVOID)&tddNew,dwNewAclSize)) {
       errstr = "SetTokenInformation";
       __leave;
     }
  }

  __finally {
    if (psidEveryone)
      FreeSid(psidEveryone);
    if (pacl)
      LocalFree((HLOCAL)pacl);
    if (ptdd)
      LocalFree((HLOCAL)ptdd);
    if (hToken)
      CloseHandle(hToken);
  }

  if(errstr!=NULL) {
    ShowOSErrorMessageBox(errstr);
    return false;
  }

  return true;
}
#endif

// returns false on error
// 'sufficient' set to true if sufficient space, false otherwise
bool toontownInstaller::
sufficientDiskSpace(const char *dir, unsigned __int64 space_required, bool &sufficient)
{
  unsigned __int64 free_space;
  if (!SysInfo::get_available_space(dir, free_space)) {
    // get_available_space already logged an error msg
    addUserError("Internal error: unable to determine how much free space is on your hard drive");
    return false;
  }
#if defined(_INSTALLERSERVICE_) || defined(_EXEINSTALLER_)
  uint64_t dir_size = directorySize(dir);
//  uint64_t dir_size = vos::dir::size(dir);
  uint64_t adj_free_space = free_space + dir_size;
  int64_t space_to_delete = space_required - adj_free_space;
#else
  unsigned __int64 dir_size = directorySize(dir);
  unsigned __int64 adj_free_space = free_space + dir_size;
  __int64 space_to_delete = space_required - adj_free_space;
#endif

  errorLog << "Free disk space: " << free_space << endl;
  errorLog << "Toontown installation size: " << dir_size << endl;
  errorLog << "Free disk space, adjusted for previously-installed files: " <<
    adj_free_space << endl;
  errorLog << "Required free disk space: " << space_required << endl;

  float megs_reqd = space_required/1000000.0f;
  float megs_free = free_space/1000000.0f;
  float megs_to_delete= space_to_delete/1000000.0f;

  _DiskSpace_Megs_Free = megs_free;

  if (space_to_delete < 0) {
    sufficient = true;
    return true;
  }

  char msg[1024];
  char drv[4];
  strncpy(drv,dir,3);
  drv[3]='\0';
  sprintf(msg,"Installing and running Toontown requires %.1f megabytes of total free space on your %s drive, which currently has only %.1f megabytes free.  You must free up an additional %.1f megabytes; to delete unneeded temporary files try using the Disk Cleanup Tool under Start Menu->Programs->Accessories->System Tools->Disk Cleanup.",megs_reqd,drv,megs_free,megs_to_delete,drv);
  addUserError(msg);
  sufficient = false;
  return false;
}

void toontownInstaller::
CreateConfigInfoRecord(void)
{
  assert(_pSysInfo!=NULL);

  _ConfigInfo.clear();

  ostringstream ConfigStr;

  _putenv( "TZ=PST8PDT" );  // make ctime convert to pacific time so log times match our server times
  // _putenv( "TZ=EST5EDT" );   // dbg test
  _tzset();

  __int64 ltime;
  _time64( &ltime );
  char datestr[26];
  strcpy(datestr,_ctime64( &ltime ));

  struct tm Tm;
  memcpy(&Tm,_localtime64(&ltime),sizeof(struct tm));

  datestr[24]='\0';  // _ctime str is always 26 chars with 24==\n

  ConfigStr << "Date=" << datestr << " " <<  _tzname[(Tm.tm_isdst ? 1 : 0)];
  ConfigStr << "\nDateMon=" << Tm.tm_mon;
  ConfigStr << "\nDateDay=" << Tm.tm_mday;
  ConfigStr << "\nDateYear=" << Tm.tm_year+1900;
  ConfigStr << "\nDateHour=" << Tm.tm_hour;
  ConfigStr << "\nDateMin=" << Tm.tm_min;
  ConfigStr << "\nUnixDate=" << ltime;

  ConfigStr << "\nGameVer=" << _downloadVersion;
  // also write an integer game ver so we can use >/< in searches
  DWORD VerA,VerB,VerC;
  // VerA should always be 1 for Toontown, so ignore it?
  sscanf(_downloadVersion,"sv%d.%d.%d",&VerA,&VerB,&VerC);
  ConfigStr << "\nGameVerNum=" << (DWORD)((VerB << 16) | VerC);

  ConfigStr << "\nOS=" << _pSysInfo->get_os_namestr();
  ConfigStr << "\nOSID=" << (int) _pSysInfo->get_os_type();
  ConfigStr << "\nOSServicePackVersion=" << _pSysInfo->get_os_servicepack_version();
  ConfigStr << "\nUserIsAdmin=" <<  ((_pSysInfo->get_os_type()>=SysInfo::OS_WinNT)?_pSysInfo->IsNTAdmin() : true);

  ConfigStr << "\nCpuMhz=" << _pSysInfo->_CPUMhz;
  ConfigStr << "\nCpuName=" << _pSysInfo->_CPUNameStr;
  ConfigStr << "\nCpuMaker=" << _pSysInfo->_CPUMakerStr;
  ConfigStr << "\nCpuType=" << _pSysInfo->_CPUTypeStr;
  ConfigStr << "\nNumCpus=" << _pSysInfo->_NumCPUs;

  ConfigStr << "\nRamMegsTotal=" << _pSysInfo->get_ram_megs_total();
  ConfigStr << "\nDiskSpaceMegsFree=" << _DiskSpace_Megs_Free;

  ConfigStr << "\nIEVersion=" << _pSysInfo->_IEVersionStr;

  // make sure we get full precision in output (can you do this in ios:: without setting the whole stream default output fmt?)
  char msgbuf[40];
  sprintf(msgbuf,"%.15g",_pSysInfo->_IEVersionNum);
  ConfigStr << "\nIEVerNum=" << msgbuf;

  ConfigStr << "\nUsingLAN=" << _pSysInfo->_bNetworkIsLAN;
  ConfigStr << "\nUsingHTTPProxy=" << _bHTTPproxyIsUsed;
  ConfigStr << "\nIPAddr=" << _pSysInfo->_IPAddrStr;
  ConfigStr << "\nMACAddr=" << _pSysInfo->_MACAddrStr;

  ConfigStr << "\nKeyboardLayout=" << _pSysInfo->_KeybdLayoutStr;
  ConfigStr << "\nLangID=" << _pSysInfo->_LangIDStr;
  ConfigStr << "\nLocaleID=" << _pSysInfo->_LocaleIDStr;

  #if 0
    // doesnt work yet
  if(!_pSysInfo->_CountryNameStr.empty()) {
    ConfigStr << "\nCountryName=" << _pSysInfo->_CountryNameStr;
  }
  #endif

  ConfigStr << "\nDXInstalledVer=" << _pSysInfo->_DXVerStr;
  ConfigStr << "\nGfxApiSuggestedID=" << _pSysInfo->_gfx_api_suggested;
  ConfigStr << "\nGfxApiSuggested=" << _pSysInfo->get_gfx_api_name(_pSysInfo->_gfx_api_suggested);

  ConfigStr << "\nNumMonitors=" << _pSysInfo->_numMonitors;

  // without DX7 some of this may be empty strs
  // could use dx3 or dx5 interfaces to get this info too?

  // TODO: handle multiple video cards somehow?

  ConfigStr << "\nVideoCardName=" << _pSysInfo->_VideoCardNameStr;
  if(_pSysInfo->_VideoRamTotalBytes == 0) {
    // for dx9, want to use IDXDiag to get vidramsize instead of dx7?

    _pSysInfo->_VideoRamTotalBytes = _pSysInfo->GetVidMemSizeFromRegistry();
#if USE_DX7
    if(_pSysInfo->_VideoRamTotalBytes == 0) {
      //GetVidMemSizeFromRegistry() will only work on NT+, otherwise resort to more expensive dx7 getvidmem
      if(_pSysInfo->_DX7_status == SysInfo::Status_Unknown) {
        // run Test_DX7 in test-vidmem mode just to get the video memorysize
        _pSysInfo->Test_DX7(false);
      }
    }
#endif
  }
  ConfigStr << endl << "VideoRamBytes=" << _pSysInfo->_VideoRamTotalBytes
			<< endl << "VideoCardVendorIDHex=" << _pSysInfo->_VideoCardVendorIDStr
            << endl << "VideoCardDeviceIDHex=" << _pSysInfo->_VideoCardDeviceIDStr
            << endl << "VideoCardSubsysIDHex=" << _pSysInfo->_VideoCardSubsysIDStr
            << endl << "VideoCardRevisionIDHex=" << _pSysInfo->_VideoCardRevisionIDStr
            << endl << "VideoCardVendorID=" << _pSysInfo->_VideoCardVendorID
            << endl << "VideoCardDeviceID=" << _pSysInfo->_VideoCardDeviceID
            << endl << "VideoCardSubsysID=" << _pSysInfo->_VideoCardSubsysID
            << endl << "VideoCardRevisionID=" << _pSysInfo->_VideoCardRevisionID
            << endl << "VideoCardDriverDate=" << _pSysInfo->_VideoCardDriverDateStr
            << endl << "VideoCardDriverVer=" << _pSysInfo->_VideoCardDriverVerStr
            << endl << "VideoCardDriverDateMon=" << _pSysInfo->_VideoCardDriverDateMon
            << endl << "VideoCardDriverDateDay=" << _pSysInfo->_VideoCardDriverDateDay
            << endl << "VideoCardDriverDateYear=" << _pSysInfo->_VideoCardDriverDateYear;

  ConfigStr << endl << "MidiOutDevices=" << _pSysInfo->_MidiOutAllDevicesStr
            << endl << "DSoundDevices=" << _pSysInfo->_DSoundDevicesStr;

  // extra string field to put odd stuff that may come in handy later
  ConfigStr << endl << "ExtraInfo=" << _pSysInfo->_ExtraStr;

  #define TMPBUFSIZE 256
  // use values from previous login
  char pBuf[TMPBUFSIZE];
  // these regkeys are written by Launcher.py
  ConfigStr << endl << "AccountName=" << _regToontown.getString("LAST_LOGIN");

  DWORD IsPaid;
  // unfortunately Launcher.py currently writes this as REG_SZ '1', not REG_DWORD 1
  if(_regToontown.getString("PAID_USER_LOGGED_IN", pBuf, TMPBUFSIZE)) {
     #ifdef USE_TESTSERVER
      IsPaid = 1;  // testserver users are always paid
     #else
      IsPaid = 0;
     #endif
  } else {
     IsPaid = (pBuf[0]=='1');
  }

  ConfigStr << endl << "IsPaid=" << IsPaid;

  // hope to do some preprocessing on either client or server to merge records that differ only by date
  // (and tolerance on variable fields like cpumhz), where this field will be # of logins
  ConfigStr << endl << "NumLogins=" << 1;

  ///////////// these fields must be filled in after configrc.exe runs and writes this info to registry
  SysInfo::GAPIType gapi = SysInfo::GAPI_Unknown;
  if(_regToontown.getDWORD("GfxApiUsed", *((DWORD*)&gapi))) {
      gapi = SysInfo::GAPI_Unknown;
  }

  gapi = min(_pSysInfo->_dx_level_installed,gapi);    // if it says dx8.1 and all we have is 8.0, use 8.0

  ConfigStr << endl << "GfxApiUsedID=" << gapi
            << endl << "GfxApiUsedName=" << _pSysInfo->get_gfx_api_name(gapi);

  ConfigStr << endl << "LastScreenMode=";

  DWORD bIsWindowed = _regToontown.getDWORD("UsingWindowedMode");
  ConfigStr << (bIsWindowed ? "Windowed" : _regToontown.getString("LastScreensize"));

  if(gapi==SysInfo::GAPI_OpenGL) {
    ConfigStr << endl << "OGLVideoCardVendor=" << _regToontown.getString("OGLVendor");
    ConfigStr << endl << "OGLVideoCardName=" << _regToontown.getString("OGLRenderer");
    ConfigStr << endl << "OGLVer=" << _regToontown.getString("OGLVersion");
  }
  ///////////////////////////////

  ConfigStr << endl << "FinalNonErrorState=" << _FinalNonErrorState
            << endl << "InstallerErrorPnt=" << _InstallerErrorPoint
            << endl << "PandaErrorCode=" << _LastPandaErrorCode;

  ConfigStr << endl;
  _ConfigInfo = ConfigStr.str();

#ifndef NDEBUG
  errorLog << endl << "Collected Config Record:" << endl << _ConfigInfo << endl;
#endif
}

// send the config record to stat server
void toontownInstaller::
SendConfigRecord(void) {
#if !defined(_EXEINSTALLER_) || !defined(_INSTALLERSERVICE_)
  assert(!_ConfigStatsServerTargetURL.empty());

#ifndef SEND_CONFIGINFO_TO_STATSERVER
  errorLog << "sendconfig is ifdef'd out!\n";
  return;
#endif

  const char *szLastGameVersionSubmittedRegkey="LastGameVersionSubmitted";
  string szLastGameVersionSubmitted;

  // remember 0==success
  if(0 == _regToontown.getString(szLastGameVersionSubmittedRegkey, szLastGameVersionSubmitted)) {
    if(szLastGameVersionSubmitted.compare(_downloadVersion)==0) {
      // do we want to just send once per game version, or record all installer/init errors?
      // lets record all errors unless space is prohibitive
#ifdef RECORD_ALL_INSTALL_ERRORS
      if((_LastPandaErrorCode==0)&&(_InstallerErrorPoint==0)) {
        errorLog << "already sent success config for gamever: " << _downloadVersion << endl;
        return;
      }
#else
      errorLog << "already sent config for gamever: " << _downloadVersion << endl;
      return;
#endif
    }
  }

  errorLog << "sending config stats\n";
  UploadArgs_s args;
  args.URL = _ConfigStatsServerTargetURL.c_str();
  args.pProxyUser=NULL;
  args.pProxyPW=NULL;
  float percent;
  args.pUploadPercent=&percent;
  args.pHeaderStr="Content-Type: application/x-www-form-urlencoded";


  // for POST, string format must be "[fieldname]=[value]&[fieldname]=[value]&...."
  // values must be urlencoded
  // urlencoding will take extra space
  DWORD cOutputBufSize=_ConfigInfo.size()*3+1;
  char *pOutputBuf=new char[cOutputBufSize];
  const char *pIgnoreChSet="=\n";
  URLEncode(_ConfigInfo.c_str(),_ConfigInfo.size(),pOutputBuf,cOutputBufSize,pIgnoreChSet);
  char *pCh;
  for(pCh = pOutputBuf; *pCh!='\0'; pCh++) {
    if(*pCh=='\n')
      *pCh='&';
  }
  args.pBuf = pOutputBuf;
  args.cBufSize = pCh-pOutputBuf;

  DWORD retCode = UploadFunc(&args);
  if(retCode!=0) {
    errorLog << "send config failed, retcode=" << retCode << endl;
  } else {
    _regToontown.setString(szLastGameVersionSubmittedRegkey, _downloadVersion);

#ifndef NDEBUG
    errorLog << "send config succeeded!\n";
#endif
  }

  delete [] pOutputBuf;
#endif
}

#endif
