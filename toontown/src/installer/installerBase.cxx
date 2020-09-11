// Filename: installerBase.cxx
// Created by:  darren (05Dec00)
// $Id$
//
////////////////////////////////////////////////////////////////////

// this was added in an attempt to work with a Blast custom proxy
// to read content off of a CD
//#define USE_HTTP_FOR_MEM_DOWNLOAD

//#define HIT_DISK_FOR_MEM_DOWNLOAD

#include "pragma.h"
#include "installerBase.h"
#include "installerApplyPatch.h"
#include "installerVersion.h"
#include "urlencode.h"
#include <errno.h>
#include <sys/types.h>  // for _chmod
#include <sys/stat.h>
#include <io.h>
#include <wininet.h>
#include <tlhelp32.h>
#include <objidl.h>
#include <tchar.h>		// for _T()
#include <sstream>
#include <algorithm>
#include "strl.h"

#define OPTIMIZE_HTTP_SESSION_CODE

//#define USE_HTTP_FOR_MEM_DOWNLOAD
#ifdef USE_HTTP_FOR_MEM_DOWNLOAD
// ADDED: KBB
#include "installerHTTP.h"
#include <wininet.h>
// -- KBB
#endif

#include <io.h>
//#include <direct.h>

const char *InternetSettingsRegKey = "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"; //under HKEY_CURRENT_USER
const char *ActiveXCache_RegValName = "ActiveXCache";
const char *AddRemoveProgsCache="Software\\Microsoft\\Windows\\CurrentVersion\\App Management\\ARPCache"; //under HKEY_LOCAL_MACHINE
const char *UninstallProgsListRegKey="Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall"; //under HKEY_LOCAL_MACHINE

#define CHECK_MD5

#define DEFAULT_PROGRESS_FILENAME "progress"
#define DEFAULT_LAUNCHERDB_FILENAME "launcherFileDb"
#define DEFAULT_LAUNCHERDDB_FILENAME "launcherFileDb.ddb"
#define DEFAULT_INSTALL_LAUNCHER_FILENAME "InstallLauncher.exe"
#define DEFAULT_INSTALLATION_LOG_FILENAME "INSTALL.LOG"    // log created by wise InstallLauncher.exe

// strings to look for in installed progs list.  (MUST BE ALL LOWER CASE)
// firewalls, virus checkers, popupwindow stoppers, netnanny-type child filters
const char *TroublesomeInstalledProgramStrs[] = {
  "norton","alarm","blackice","mcafee",
  "firewall","symantec","virus","viper","safe",
  "pop","stop","block","filter","zap","kill","nanny",
  "child","bess","cyber","surf","block","guard","family"};
const int numTroublesomeInstalledProgramStrs = sizeof(TroublesomeInstalledProgramStrs) / sizeof(const char *);

typedef struct {
  const char *pExeName;
  const char *pFriendlyName;
} RunningProgName;

// strings to look for in running  progs list.  (MUST BE ALL LOWER CASE)
#define NUM_TROUBLESOME_RUNNING_PROGSTRS 1
RunningProgName TroublesomeRunningProgramStrs[NUM_TROUBLESOME_RUNNING_PROGSTRS] =
  { {"alg.exe","Microsoft Internet Connection Firewall"} };

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
const char *installerBase::_P3D_INSTALL_DIR_ValueName = "INSTALL_DIR";
#endif

void LogOSErrorMessage(const char *called_func) {
  //    char msgbuf[1024];
  char *pSysMsgBuf;
  DWORD errNum=GetLastError();
  FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM
          | FORMAT_MESSAGE_IGNORE_INSERTS
          | FORMAT_MESSAGE_ALLOCATE_BUFFER,
          NULL,
          errNum,
          MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), // Default language
          (LPTSTR) &pSysMsgBuf,
          0, NULL );

  errorLog << ((called_func!=NULL) ? called_func : "")
      << " returned Error " << errNum << ": " << pSysMsgBuf << endl;
}

void ShowOSErrorMessageBox(char *error_title) {
  char msgbuf[1024];
  char *pSysMsgBuf;
  DWORD errNum=GetLastError();
  FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM
          | FORMAT_MESSAGE_IGNORE_INSERTS
          | FORMAT_MESSAGE_ALLOCATE_BUFFER,
          NULL,
          errNum,
          MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), // Default language
          (LPTSTR) &pSysMsgBuf,
          0, NULL );

    sprintf(msgbuf,"%s returned Error %d: %s",(error_title!=NULL) ? error_title: "",errNum,pSysMsgBuf);
    LocalFree( pSysMsgBuf );
    MessageBox( NULL, (LPCTSTR)msgbuf, "Toontown Installer Error", MB_OK | MB_ICONWARNING );
}

installerBase::
installerBase() :
  _launcherProgress_IFilename(DEFAULT_PROGRESS_FILENAME),
  _launcherFileDB_IFilename(DEFAULT_LAUNCHERDB_FILENAME),
  _launcherDDBFile_IFilename(DEFAULT_LAUNCHERDDB_FILENAME),
  _launcherSelfExtractor_IFilename(DEFAULT_INSTALL_LAUNCHER_FILENAME),
  _launcherExtractionLogFile_IFilename(DEFAULT_INSTALLATION_LOG_FILENAME)
{

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
  _pandaRegInitialized = 0;
  strcpy(_panda3DInstallDir, "");
#endif

#ifdef USE_DOWNLOAD_TO_FILE_CALLBACK
  // clear out the download callback
  downloadToFileCallback = NULL;
#endif

  _PercentFileDownloaded=0.0f;
  _PatchSize = 0;

  time_t long_time;
  struct tm *pTm;
  time(&long_time);              /* Get time as long integer. */
  pTm = localtime( &long_time ); /* Convert to local time. */
  char time_suffix[100];
  sprintf(time_suffix,"%02d%02d%02d_%02d%02d%02d",pTm->tm_year-100,
          pTm->tm_mon+1, pTm->tm_mday, pTm->tm_hour, pTm->tm_min, pTm->tm_sec);
  _logSuffix = time_suffix;
}

installerBase::
~installerBase() {
}

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
int installerBase::
createPanda3DInstallDir() {
  int dirWasNotInRegistry = 0;
  int changeToDirFailed = 0;

  // try to get the Panda3D installation dir from the registry
  if (regGetString(_hKeyPanda3D, _P3D_INSTALL_DIR_ValueName,
                   _panda3DInstallDir, sizeof(_panda3DInstallDir)))
  {
    // installation dir not found in registry
    dirWasNotInRegistry = 1;
  }
  else {
    // add a trailing slash to the install directory
    // (it's stored in the registry without one)
    addTrailingSlash(_panda3DInstallDir);

    // try to go to that directory
    if (!SetCurrentDirectory(_panda3DInstallDir)) {
      // could not go to install directory
      changeToDirFailed = 1;
    }
  }

  // if install directory was not found in registry, or we could not go to
  // the install directory, synthesize a Panda3D install directory name
  if (dirWasNotInRegistry || changeToDirFailed)
  {

#error  Note this needs changing, see corresponding fn in toontownInstaller - georges
    const char *programFiles = getenv("ProgramFiles");

    // make a path off of the "Program Files" folder
    if(programFiles) {
      strcpy(_panda3DInstallDir, programFiles);
      addTrailingSlash(_panda3DInstallDir);
    }
    else {
      // couldn't find the user's "Program Files" folder, use default
      strcpy(_panda3DInstallDir, "C:\\Program Files\\");
    }
    strcat(_panda3DInstallDir, "Panda3D\\");

    // create the directory
    makeDir(_panda3DInstallDir);

    // set the install directory in the registry, with no trailing slash
    {
      char temp[_MAX_PATH];
      strcpy(temp, _panda3DInstallDir);
      removeTrailingSlash(temp);

      regSetString(_hKeyPanda3D, _P3D_INSTALL_DIR_ValueName, temp);
    }

    // make sure we're in the directory
    if (!SetCurrentDirectory(_panda3DInstallDir)) {
      return -1;
    }
  }

  return 0;
}

const char *installerBase::
getPanda3DInstallDir() {
  return _panda3DInstallDir;
}
#endif

// error utility methods
//
string installerBase::
GetLastErrorStr() const
{
    DWORD errorCode = GetLastError();

    string errorString;
    {
        char errorCodeBuf[64];
        errorString = _ultoa(errorCode, errorCodeBuf, 16);
    }

    if (errorCode != ERROR_SUCCESS) {
        LPVOID lpMsgBuf;
        DWORD ec = FormatMessage (
                FORMAT_MESSAGE_ALLOCATE_BUFFER |
                FORMAT_MESSAGE_FROM_SYSTEM |
                FORMAT_MESSAGE_IGNORE_INSERTS,
                NULL, errorCode,
                MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), // default language
                (LPTSTR) &lpMsgBuf,
                0, NULL);
        if (ec != 0)
        {
            errorString += ": ";
            errorString += (LPCTSTR) lpMsgBuf;
            LocalFree(lpMsgBuf);
        }
    }

    return errorString;
}

// file name methods
void installerBase::
makeFilenameInTempDir(char *dest, const char *filename)
{
  char temp_path[_MAX_PATH];

  if(!MyGetTempPath(sizeof(temp_path), temp_path)) {
    ShowErrorBox("MyGetTempPath failed!");
  }

  combinePathAndFilename(dest, temp_path, filename);
}

void installerBase::
convertFullFilenameToURL(const char *filename, char *url)
{
  // note these links dont work on IE6 Sp1, cant cross from http:// to file:// domain
  strcpy(url, "file://");
  strcat(url, filename);

  char *p;
  while(p = strchr(url, '\\')) {
    *p = '/';
  }
}

// adds a trailing slash if there isn't one already
void installerBase::
addTrailingSlash(char *filename) {
  if(filename[strlen(filename)-1] != '\\')
    strcat(filename, "\\");
}

void installerBase::
removeTrailingSlash(char *filename) {
  if(filename[strlen(filename)-1] == '\\')
    filename[strlen(filename)-1] = '\0';
}

// adds a trailing forward slash if there isn't one already
void installerBase::
addTrailingForwardSlash(char *filename) {
  if(filename[strlen(filename)-1] != '/')
    strcat(filename, "/");
}

void installerBase::
removeTrailingForwardSlash(char *filename) {
  if(filename[strlen(filename)-1] == '/')
    filename[strlen(filename)-1] = '\0';
}

// file check methods
// returns false if file does NOT exist
bool installerBase::
fileExists(const char *filename) {
  if(_access(filename, 0) == -1) {
    if(errno==ENOENT)
      return false;
  }

  return true;
}

// returns -1 if it doesnt exist, or some other problem occurs
int installerBase::
getFileSize(const char *filename) {
  WIN32_FIND_DATA TempFindData;
  HANDLE FindFileHandle = FindFirstFile(filename,&TempFindData );
  if ( FindFileHandle == INVALID_HANDLE_VALUE ) {
    errorLog << "error determining file size of " << filename << endl;
    return -1;
  }
  FindClose(FindFileHandle);
  return (int) TempFindData.nFileSizeLow;
}

void installerBase::
getFileDate(const char *filename, FILETIME *pFileTime) {
  ZeroMemory(pFileTime,sizeof(FILETIME));
  WIN32_FIND_DATA TempFindData;
  HANDLE FindFileHandle = FindFirstFile(filename,&TempFindData );
  if ( FindFileHandle == INVALID_HANDLE_VALUE ) {
    errorLog << "error determining file date of " << filename << endl;
  }
  FindClose(FindFileHandle);
  *pFileTime = TempFindData.ftCreationTime;
}

// this function should be called to remove an obsolete file
// that is about to be re-downloaded. if the file exists,
// the file is deleted and a note is made in the error log
bool installerBase::
deleteObsoleteFile(const char *filename) {
  if(!deleteFile(filename)) {
    errorLog << "Could not delete obsolete file: " << filename << endl;
    return false;
  }

  return true;
}

// returns true if file is deleted or did not exist
bool installerBase::
deleteFile(const char *filename) {
  BOOL bSuccess = SetFileAttributes(filename,FILE_ATTRIBUTE_NORMAL);
  DWORD err;

  if(!bSuccess) {
    err=GetLastError();
    if(err==ERROR_FILE_NOT_FOUND) {
      // errorLog << "deletefile('" << filename << "'): file not found\n";
      return true;
    }

    errorLog << "deletefile('" << filename << "'), SetFileAttr failed w/error: "
       << err << endl;
  }

  // try to delete the file
  bSuccess = DeleteFile(filename);
  if(bSuccess)
    return true;

  errorLog << "failed to delete '" << filename << "', error: ";

  switch(err = GetLastError()) {
  case ERROR_ACCESS_DENIED:
      errorLog << "ERROR_ACCESS_DENIED"; break;
  case ERROR_PATH_NOT_FOUND:
      errorLog << "ERROR_PATH_NOT_FOUND"; break;
  case ERROR_SHARING_VIOLATION:
      errorLog << "ERROR_SHARING_VIOLATION"; break;
  default:
      errorLog << err;
  }
  errorLog << endl;

  return false;
}

unsigned __int64 installerBase::
directorySize(const char *dir) {
  unsigned __int64 curDirSize = 0;
  char oldDir[_MAX_PATH];
  HANDLE hSearch;
  WIN32_FIND_DATA wfd;

  if(!GetCurrentDirectory(sizeof(oldDir), oldDir))
    return 0;
  if(!SetCurrentDirectory(dir))
    return 0;

  hSearch = FindFirstFile("*", &wfd);
  if(INVALID_HANDLE_VALUE != hSearch)
  {
    while(1) {
      if(wfd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
        if(strcmp(wfd.cFileName, ".") && strcmp(wfd.cFileName, ".."))
          curDirSize += directorySize(wfd.cFileName);
      }
      else {
        curDirSize += (((unsigned __int64)wfd.nFileSizeHigh) << 32) + wfd.nFileSizeLow;
      }

      if(!FindNextFile(hSearch, &wfd))
        break;
    }
  }

  SetCurrentDirectory(oldDir);

  return curDirSize;
}

bool installerBase::
makeDir(const char *filename, PSECURITY_ATTRIBUTES pSA)
{
  char fn[_MAX_PATH];
  char *slash;

  strcpy(fn, filename);

  // first replace fwd slashes w/backslashes
  for(char *p = fn;*p!='\0';p++) {
    if(*p == '/')
      *p = '\\';
  }

  slash = fn;

  // can only make 1 dir at a time, so go through and make a new dir at each '\' point
  while (*slash) {
    slash = strchr(slash, '\\');
    if (slash == NULL) {
      break;
    }
    else
	{
      // temporarily terminate string at \ point for createdir
      *slash = '\0';

      if(!SetCurrentDirectory(fn))
	  {	// assume if you cant cd there, we need to create it
        if(!CreateDirectory(fn, pSA))
		{
          DWORD errNum = GetLastError();
          if (errNum != ERROR_ALREADY_EXISTS) { // if dir already exists, thats ok
            errorLog << "Creating Directory '" << fn << "' failed, err=" << errNum << endl;
            return false;
          }
        } else {
          errorLog << "Creating Directory '" << fn << "'\n";
        }
      }

      *slash++ = '\\';
      while (*slash == '\\')
        slash++;
    }
  }
  
  return true;
}

// file downloading methods

#ifdef OPTIMIZE_HTTP_SESSION_CODE
//
// This function handles the queries more gracefully specially on allocating the buffers.
// The parameters are exactly the same as HttpQueryInfo.
//
bool handleHttpQueryInfo(HINTERNET hRequest, DWORD dwInfoLevel, LPVOID &lpvBuffer,
                         LPDWORD lpdwBufferLength, LPDWORD lpdwIndex) {
  // it assumes lpvBuffer is null
  if (lpvBuffer != NULL) {
    errorLog << "program error, expecting a null in lpvBuffer" << endl;
    return false;
  }
 
retry:
  // This call will fail on the first pass, because no buffer is allocated.
  if(!HttpQueryInfo(hRequest, dwInfoLevel, (LPVOID)lpvBuffer, lpdwBufferLength, NULL)) {
    if (GetLastError()==ERROR_HTTP_HEADER_NOT_FOUND) {
      // Code to handle the case where the header isn't available.
      return false;
    } else {
      // Check for an insufficient buffer.
      if (GetLastError()==ERROR_INSUFFICIENT_BUFFER) {
        // Allocate the necessary buffer.
        lpvBuffer = new char[*lpdwBufferLength];
        if (lpvBuffer) {
          //          errorLog << "created buffer of size : " << *lpdwBufferLength << endl;
          goto retry;          // Retry the call.
        } else {
          errorLog << "memory allocation failed : lpvBuffer of size " << *lpdwBufferLength << endl;
          return false;
        }
      } else {
        // Error handling code.
        return false;
      }
    }
  }
  //  errorLog << "returning true from func" << endl;

  return true;
}

//
// This function handles the error messages when a HTTP_StatusCode != HTTP_STATUS_OK
//
void handleHttpStatusNotOk(HINTERNET hRequest, char *pRequestHdrBuf,
                           const char **err, const char *url) {
  char *pStatusText = NULL;
  DWORD dwBufLen = 0;
  
  if(!handleHttpQueryInfo(hRequest,
                    HTTP_QUERY_STATUS_TEXT,
                    (LPVOID &)pStatusText,
                    &dwBufLen,
                    0)) {
    *err = "HttpQueryInfo StatusText";
    return;
  }
  errorLog << pStatusText << endl;

  if (pStatusText) {
    delete [] pStatusText;
    pStatusText = NULL;
  }
  
  char *pHdrBuf = NULL;
  dwBufLen=0;
      
  if(!handleHttpQueryInfo(hRequest,
                    HTTP_QUERY_RAW_HEADERS_CRLF,
                    (LPVOID &)pHdrBuf,
                    &dwBufLen,
                    0)) {
    if (pHdrBuf) {
      delete [] pHdrBuf;
      pHdrBuf = NULL;
    }
    *err = "HttpQueryInfo Reply Headers";
    return;
  }

#define GETRIDOFCRS(BUF)                      \
        for(char *pCh=BUF;*pCh!='\0'; pCh++) {    \
            if(*pCh=='\r')                            \
              *pCh=' ';                               \
        }

  const char *pMarker="=======\n";
  
  if (pHdrBuf)
    GETRIDOFCRS(pHdrBuf);
  if (pRequestHdrBuf)
    GETRIDOFCRS(pRequestHdrBuf);
  
  errorLog << "HTTP Reply Headers returned for " << url << ":\n" << pMarker << pHdrBuf << endl << pMarker;
  errorLog << "HTTP Request Headers were:\n"<< pRequestHdrBuf << pMarker;
  if (pHdrBuf) {
    delete [] pHdrBuf;
    pHdrBuf = NULL;
  }
}

#endif

//returns true on success
bool installerBase::
downloadToFile(const char *URL, const char *destFilename) {
#ifdef USE_DOWNLOAD_TO_FILE_CALLBACK
  // if there's a callback set, use that
  if (downloadToFileCallback) {
    return downloadToFileCallback(URL, destFilename);
  } else
#endif
  removeURLFromCache(URL);

// old way, unreliable
//  return (S_OK != URLDownloadToFile(NULL, URL, destFilename, 0, NULL));

  DLArgs_s *args = new DLArgs_s;
  if (NULL == args)
    return NULL;
  ZeroMemory(args,sizeof(DLArgs_s));

  args->URL = URL;
  args->destFilename = destFilename;
  args->pProxyUser=&_ProxyUserName; // this and following 2 lines added by masad
  args->pProxyPW=&_ProxyUserPassword;
  args->pDownloadPercent=&_PercentFileDownloaded;
  args->pPatchSizeSoFar = &_PatchSizeSoFar;
  args->iPatchSize = _PatchSize;

#if 0 // changed by masad
  if(!_proxy_spec.empty())
    args->pProxy=&_proxy_spec;
#endif

  // DownloadFunc frees args (does it this way since it could be called as thread)
  bool bSuccess = (DownloadFunc(args)==0);
  return bSuccess;
}

// URLOpenBlockingStream()
// URLOpenPullStream()
// URLOpenStream()
//
// IT IS UP TO THE CALLER TO CALL delete[] ON THE RETURNED POINTER

#ifdef USE_HTTP_FOR_MEM_DOWNLOAD

// ADDED: KBB
char* installerBase::
downloadToMem(const char *URL, unsigned long &bufLength)
{
  char *buf = NULL;
  int pport = 0;
  char phost[MAX_PATH];
  DWORD bufLen = sizeof(INTERNET_PROXY_INFO) + /*proxy*/ (MAX_PATH*4) + /* noproxy*/ (MAX_PATH*4);
  bufLength = 0L;
  memset(phost, 0, sizeof(phost));

#ifdef _USE_IE_PROXY
  INTERNET_PROXY_INFO *pipo = (INTERNET_PROXY_INFO*)calloc(1, bufLen);
  if (pipo == NULL)
    return NULL;

  BOOL bRet = InternetQueryOption(NULL, INTERNET_OPTION_PROXY, (LPVOID)pipo, &bufLen);
  if (bRet && pipo->dwAccessType == INTERNET_OPEN_TYPE_PROXY) {
    char *ptr = strchr(pipo->lpszProxy, ':');
    if (ptr) {
      strncpy(phost, pipo->lpszProxy, ptr - pipo->lpszProxy);
      ptr++;
      if (*ptr)
        pport = atoi(ptr);
    }
  }
  free(pipo);
#endif

  int error;
  if (error = http_download_to_buffer(URL, phost, pport, &buf, &bufLength))
  {
    errorLog << "HTTP download failed: ";
    switch(error) {
    case E_HTTP_FAIL:               errorLog << "'fail'";             break;
    case E_HTTP_URL_FORMAT_ERROR:   errorLog << "URL format error";   break;
    case E_HTTP_CONNECTION_FAILED:  errorLog << "connection failed";  break;
    case E_HTTP_INVALID_ADDRESS:    errorLog << "invalid address";    break;
      //case E_HTTP_NO_CONTENT_LENGTH:  errorLog << "no content length";  break;
    default: errorLog << "unknown error";
    }
    errorLog << endl;

    // Handle error
    return NULL;
  }
  return buf;
}

// -- KBB
#elif defined HIT_DISK_FOR_MEM_DOWNLOAD

char* installerBase::
downloadToMem(const char *URL, unsigned long &bufLength) {

  // download the file to disk, then read into memory
  const char *filename = "launcherFileDb";

  errorLog << "about to download " << filename << endl;
  if (!downloadToFile(URL, filename)) {
    return NULL;
  }
  errorLog << "download complete" << endl;

  ifstream read_stream;

  read_stream.open(filename, ios::in | ios::binary);
  if (read_stream.fail()) return NULL;

  // get the size of the database file
  read_stream.seekg(0, ios::end);
  long file_size = read_stream.tellg();
  read_stream.seekg(0, ios::beg);

  // allocate a buffer to hold the whole thing
  char *buf = new char[file_size];

  // read the file in
  read_stream.read(buf, file_size);
  if (read_stream.fail()) {
    delete [] buf;
    read_stream.close();
    _unlink(filename);
    return NULL;
  }

  read_stream.close();
  _unlink(filename);

  bufLength = (unsigned long)file_size;

  return buf;
}

#else

//returns true on success
bool installerBase::
downloadToMem(const char *URL, string &pFileBufStr) {
  IStream *pStrm = NULL;
  LARGE_INTEGER offsetLI;
  ULARGE_INTEGER bufLengthULI;
  char *pBuf=NULL;
  bool bSuccess=false;

  /*
    result = URLDownloadToCacheFile(NULL, URL, "testdlfile", strlen("testdlfile"), 0, NULL);
    errorLog << "URLDownloadToCacheFile result: " << result << ", S_OK == " << S_OK << endl;
  */

  //errorLog << "About to open URL: " << URL << endl;

  removeURLFromCache(URL);

  // Note: this will always get stuff from the local cache, unless 'never' is selected in IE options
  HRESULT hr = URLOpenBlockingStream(NULL, URL, &pStrm, 0, NULL);

  if (FAILED(hr)) {
    URL_COMPONENTS url_comp;
    ZeroMemory(&url_comp,sizeof(url_comp));
    url_comp.dwStructSize= sizeof(url_comp);
    char msgbuf[512];
    ZeroMemory(msgbuf,sizeof(msgbuf));
    url_comp.lpszHostName=msgbuf;
    url_comp.dwHostNameLength=sizeof(msgbuf);
    InternetCrackUrl(URL,sizeof(URL),0x0,&url_comp);
    errorLog << "downloadToM URLOpenBlockingStream failed: hr=";
    switch(hr) {
      // these ERROR CODES are defined in UrlMon.h!
    case INET_E_CANNOT_CONNECT:
      errorLog << "INET_E_CANNOT_CONNECT" << endl;
      break;
    case INET_E_DOWNLOAD_FAILURE:
      errorLog << "INET_E_DOWNLOAD_FAILURE" << endl;
      break;
    case INET_E_RESOURCE_NOT_FOUND:
      errorLog << "INET_E_RESOURCE_NOT_FOUND" << endl;
      break;
    default:
      errorLog << "0x" << (void*)hr << endl;
    }

    goto _cleanup;
  }

  // find out how large the file is
  offsetLI.QuadPart = 0;
  hr = pStrm->Seek(offsetLI, STREAM_SEEK_END, &bufLengthULI);
  if (FAILED(hr)) {
    errorLog << "installerBase error 0x" << (void*)hr << " calling IStream::Seek() to end of file\n";
    goto _cleanup;
  }

  // seek back to the beginning
  hr = pStrm->Seek(offsetLI, STREAM_SEEK_SET, NULL);
  if (FAILED(hr)) {
    errorLog << "installerBase error 0x" << (void*)hr << " calling IStream::Seek() to start of file\n";
    goto _cleanup;
  }

  int bufLength = bufLengthULI.LowPart;

  errorLog << "downloadToMem(): total read = " << bufLength << endl;

  // allocate a memory buffer
  pBuf = new char[bufLength];
  if (NULL == pBuf) {
    errorLog << "installerBase error allocating memory\n";
    goto _cleanup;
  }

  // copy the file into the buffer
  hr = pStrm->Read(pBuf, bufLength, NULL);
  if (FAILED(hr)) {
    errorLog << "installerBase error 0x"<<(void*)hr<<"calling IStream::Read() of " << bufLength << " bytes\n";
    goto _cleanup;
  }

  pFileBufStr.assign(pBuf, bufLength);
  //errorLog << "assigned bufLength ="  << pFileBufStr.length() << endl;

  bSuccess = true;

 _cleanup:
  // programmer, clean up after thyself
  if (pStrm)
    pStrm->Release();
  if (pBuf)
    delete[] pBuf;
  return bSuccess;
}
// want to move to this fn (away from urlmon) when jsproxy stuff works
// when jsproxy is used to get proxy, it triggers this error
// HttpSendRequest(http://download.toontown.com/sv1.1.1/launcherFileDb) failed, err: 12007, NAME_NOT_RESOLVED
// need to fix before jsproxy can be used
//returns true on success
bool installerBase::
downloadToMem_New(const char *URL, string *pFileBufStr) {
  char *pRetBuf=NULL;
  DLArgs_s *args = new DLArgs_s;
  if (NULL == args)
    return NULL;
  ZeroMemory(args,sizeof(DLArgs_s));

  args->URL = URL;
  if(!_proxy_spec.empty())
    args->pProxy=&_proxy_spec;

  args->bDoMemoryDownload = true;
  // DownloadFunc does NOT free args if bDoMemoryDwnload is specified, so we can get pStringStrm back
  bool bSuccess = (DownloadFunc(args)==0);

  if(bSuccess) {
    // copy stringstream to string object
    *pFileBufStr = args->pStringStrm->str();
  }
  if(args->pStringStrm!=NULL)
    delete args->pStringStrm;
  delete args;
  return bSuccess;
}
//
// Lets try a quick function that tests an url to determine if the server will talk to us
//
bool installerBase::
testServer(const char *URL) {
  IStream *pStrm = NULL;
  HRESULT hr = URLOpenBlockingStream(NULL, URL, &pStrm, 0, NULL);

  if (FAILED(hr)) {
    errorLog << "url:|" << URL << "| failed error 0x" << (void*)hr << endl;
    if (pStrm)
      pStrm->Release();
    return false;
  }

  // Release the stream, we don't want to read it yet
  if (pStrm) {
    LARGE_INTEGER offsetLI;
    ULARGE_INTEGER bufLengthULI;
    
    offsetLI.QuadPart = 0;
    hr = pStrm->Seek(offsetLI, STREAM_SEEK_END, &bufLengthULI);
    if (FAILED(hr)) {
      errorLog << "installerBase error 0x" << (void*)hr << " calling IStream::Seek() to end of file\n";
    } else {
      errorLog << "total read = " << (int)bufLengthULI.LowPart << endl;
    }
    pStrm->Release();
  }
  return true;
}
//
//
//
#endif

#if 0
void PrintLastWNetError(void) {
  DWORD dwWNetError;
#define ERRMSGSIZE 512
  char pErrorBuf[ERRMSGSIZE];
  char pNameBuf[ERRMSGSIZE];

  pErrorBuf[0]='\0';
  pNameBuf[0]='\0';

  DWORD retVal=WNetGetLastError(&dwWNetError,pErrorBuf,ERRMSGSIZE,pNameBuf,ERRMSGSIZE);
  if(NO_ERROR!=retVal) {
    errorLog << "WNetGetLastError failed: err=" << retVal << endl;
  } else {
    errorLog << "WNetGetLastError returns err: " << dwWNetError << " : " << pErrorBuf
             << "network provider: " << pNameBuf << endl;
  }
}
#endif

// use __stdcall since must be called by CreateThread
unsigned long __stdcall DownloadFuncStub(void *argPtr) {
  return DownloadFunc((DLArgs_s*) argPtr);
}

unsigned long DownloadFunc(DLArgs_s *args)
{
  DWORD retCode = 0;    // 0 == success

  // BUGBUG: remove this when ready to test jsproxy again
  // I thought jsproxy might be interfering with InternetOpen(PRECONFIG),
  // so I wanted to try specifying explicit proxy with InternetOpen.
  // didnt fix wininet crashes w/jsproxy, so go back to old way of always
  // using PRECONFIG for now
  args->pProxy=NULL;

  if(args->pDownloadPercent!=NULL)
    *(args->pDownloadPercent) = 0.0f;

  DeleteUrlCacheEntry(args->URL);

  if(args->bUseURLDownloadtoFile) {
    // the problem with URLDownloadtoFile is that we're running in a separate thread,
    // but we're using single-thread 'apartment' COM model that's std for ActiveX controls,
    // so we sometimes get E_NOINTERFACE errors here (I cant tell the exact circumstances)
    // should not use this if we can avoid it (if the InternetReadFile method worx)
    HRESULT hr = URLDownloadToFile(NULL, args->URL, args->destFilename, 0, NULL);
    if(FAILED(hr)) {
      errorLog << "URLDownloadToFile("<<args->URL<<","<<args->destFilename<<") returned error: 0x" << (void*)hr << endl;
      errorLog << "GetLastError returns: " << GetLastError() << endl;
      // PrintLastWNetError();
      retCode = 1;
    }
  } else {
    // hopefully wininet will not have the same COM-reentrancy problems
    // if it does, we can stop using a separate thread and instead use
    // wininet async mode w/callbacks.

    const char *errfnstr = "";
    HINTERNET  hSession = NULL;
    HINTERNET  hConnection = NULL;
    HINTERNET  hRequest = NULL;
    char *pRequestHdrBuf = NULL;
    bool bPrintINETErrMsg = false;
    char *pData = NULL;
    DWORD dwTotalBytesRead=0;
    DWORD dwBufLen;

    // dont we already know we're connected by this point?
    DWORD retVal = InternetAttemptConnect(0x0);
    if(retVal!=ERROR_SUCCESS) {
      errfnstr = "InternetAttemptConnect";
      retVal=1;
      bPrintINETErrMsg = true;
      goto cleanup;
    }

    URL_COMPONENTS url_comp;
    ZeroMemory(&url_comp,sizeof(url_comp));
    url_comp.dwStructSize = sizeof(url_comp);

    char hostnamebuf[512];
    ZeroMemory(hostnamebuf,sizeof(hostnamebuf));
    url_comp.lpszHostName=hostnamebuf;
    url_comp.dwHostNameLength=sizeof(hostnamebuf);

    char urlstrbuf[1024];;
    url_comp.lpszUrlPath = urlstrbuf;
    url_comp.dwUrlPathLength=sizeof(urlstrbuf);
    if(!InternetCrackUrl(args->URL,0,0x0,&url_comp)) {
      errfnstr = "InternetCrackUrl";
      retCode=1;
      goto cleanup;
    }

    if((url_comp.nScheme!=INTERNET_SCHEME_HTTP) && (url_comp.nScheme!=INTERNET_SCHEME_HTTPS)) {
      // due to the httpOpenRequest stuff.  should be easy to adapt if need arises tho
      errorLog << "DownloadFunc not yet designed for non-http URLs!\n";
      errfnstr = "InternetCrackUrl";
      retCode=1;
      goto cleanup;
    }

    HANDLE hFile = NULL;

    if(args->bDoMemoryDownload) {
      args->pStringStrm = new ostringstream;
      if(!args->pStringStrm) {
        errorLog << "new ostringstream failed!\n";
        retCode=1;
        goto cleanup;
      }
    } else {
      hFile = CreateFile(args->destFilename,
                         GENERIC_READ | GENERIC_WRITE,(DWORD) 0, NULL, CREATE_ALWAYS,
                         FILE_ATTRIBUTE_NORMAL, (HANDLE) NULL);
      if(!hFile) {
        errorLog << "CreateFile("<<args->destFilename<<") failed, err: " << GetLastError() << endl;
        retCode = 1;
        goto cleanup;
      }
    }

    if(args->pProxy==NULL) {
      hSession = InternetOpen("Toontown Installer",
                              INTERNET_OPEN_TYPE_PRECONFIG,  // use IE proxy info from registry
                              NULL,  // no explicit proxy
                              NULL,  // no proxy bypass
                              0x0);  // no flags
    } else {
      hSession = InternetOpen("Toontown Installer",
                              INTERNET_OPEN_TYPE_PROXY,  // use IE proxy info from registry
                              args->pProxy->c_str(),
                              NULL,  // no proxy bypass
                              0x0);  // no flags
    }

    if(!hSession) {
      errfnstr="InternetOpen";
      retCode = 1;
      goto cleanup;
    }

#if 0
    // right now this always fails with INVALID_HANDLE_TYPE even on proxy's requiring a pw,
    // so passing hSession is likely wrong, or done at the wrong time
    // removing until able to get it workin
    if((args->pProxyUser!=NULL)&&(args->pProxyPW!=NULL)) {
      char usernamebuf[512];
      DWORD err,usernamebuflen=sizeof(usernamebuf);
      HINTERNET hQueryInet = hSession;

      BOOL bRet = InternetQueryOption(hQueryInet, INTERNET_OPTION_PROXY_USERNAME, usernamebuf, &usernamebuflen);
      if(!bRet) {
        err = GetLastError();
        errorLog << "InternetQueryOption(INTERNET_OPTION_PROXY_USERNAME) failed, err=" << err << endl;
      } else {
        char pwbuf[512];
        DWORD pwbuflen=sizeof(pwbuf);
        BOOL bRet = InternetQueryOption(hQueryInet, INTERNET_OPTION_PROXY_PASSWORD, pwbuf, &pwbuflen);
        if(!bRet) {
          err = GetLastError();
          errorLog << "InternetQueryOption() 2 failed, err=" << err << endl;
        } else {
          // success!  do implicit copy of const char* to string objs
          *(args->pProxyUser) = usernamebuf;
          *(args->pProxyPW) = pwbuf;
        }
      }
    }
#endif

    INTERNET_PORT portNum = ((url_comp.nPort!=0) ? url_comp.nPort : INTERNET_DEFAULT_HTTP_PORT);
    errorLog << "Opening connection to "<<url_comp.lpszHostName<<":"<<portNum << endl;

    // this fn is expensive, should we cache hConnection across multiple calls?
    hConnection = InternetConnect(hSession,
            url_comp.lpszHostName,
            portNum,
            ((args->pProxyUser!=NULL)? args->pProxyUser->c_str() : NULL),
            ((args->pProxyPW!=NULL)? args->pProxyPW->c_str() : NULL),
            INTERNET_SERVICE_HTTP,
            INTERNET_FLAG_NO_CACHE_WRITE,
            NULL);    // No Context
    if(!hConnection) {
      errfnstr="InternetConnect";
      retCode = 1;
      goto cleanup;
    }

    const char *TypeArray[2] = { "*/*", NULL};
    /*
     */

    hRequest = HttpOpenRequest(hConnection,
            "GET",
            url_comp.lpszUrlPath,
            NULL,    // Default HTTP Version
            NULL,    // No Referrer
            TypeArray,  // Accept anything
            INTERNET_FLAG_NO_CACHE_WRITE | INTERNET_FLAG_KEEP_CONNECTION, // needed for user/pw auth??
            NULL);   // No Context
    if(!hRequest) {
      errfnstr = "HttpOpenRequest";
      retCode = 1;
      goto cleanup;
    }

    // save the request headers in case we need to print them out l8r due to an error    
#ifdef OPTIMIZE_HTTP_SESSION_CODE
    pRequestHdrBuf = NULL;
    dwBufLen = 0;
    if (!handleHttpQueryInfo(hRequest,
                             HTTP_QUERY_RAW_HEADERS_CRLF|HTTP_QUERY_FLAG_REQUEST_HEADERS,
                             (LPVOID &)pRequestHdrBuf, &dwBufLen, 0)) {
#else

#define MAX_HEADER_SIZE 10000 // hopefully the hdrs will be smaller than this
    pRequestHdrBuf = new char[MAX_HEADER_SIZE];
    dwBufLen=MAX_HEADER_SIZE;
    if(!HttpQueryInfo(hRequest,
                      HTTP_QUERY_RAW_HEADERS_CRLF|HTTP_QUERY_FLAG_REQUEST_HEADERS,
                      (LPVOID)pRequestHdrBuf,
                      &dwBufLen, 0)) {
#endif
      errfnstr = "HttpQueryInfo Request Headers";
      retCode=1;
      goto cleanup;
    }
    //    errorLog << endl<< dwBufLen << " : " << pRequestHdrBuf << endl;

    if(!HttpSendRequest(hRequest,
                        NULL,    // No extra headers
                        0,       // no extra Header length
                        NULL,    // Not sending a POST
                        0)) {    // Not sending a POST
      errfnstr = "HttpSendRequest";
      retCode = 1;
      goto cleanup;
    }

    DWORD HTTP_StatusCode=0;
    dwBufLen = sizeof(HTTP_StatusCode);

    if(!HttpQueryInfo(hRequest,
                      HTTP_QUERY_STATUS_CODE
                      | HTTP_QUERY_FLAG_NUMBER,  // HTTP_QUERY_FLAG_NUMBER tells it to return a dword, not a string
                      (LPVOID)&HTTP_StatusCode,
                      &dwBufLen,
                      NULL)) {
      errfnstr = "HttpQueryInfo Status";
      retCode=1;
      goto cleanup;
    }
    //    errorLog << dwBufLen << " : " << HTTP_StatusCode << endl;
    
    if(HTTP_StatusCode!=HTTP_STATUS_OK) {
      errorLog << "HTTP Status "<< HTTP_StatusCode << ": ";

#ifdef OPTIMIZE_HTTP_SESSION_CODE
      handleHttpStatusNotOk(hRequest, pRequestHdrBuf, &errfnstr, args->URL);
#else
      char StatusText[1024];
      dwBufLen=1024;

      if(!HttpQueryInfo(hRequest,
                        HTTP_QUERY_STATUS_TEXT,
                          (LPVOID)StatusText,
                        &dwBufLen,
                        0)) {
        errfnstr = "HttpQueryInfo StatusText";
        retCode=1;
        goto cleanup;
      }
      errorLog << StatusText << endl;

      char *pHdrBuf = new char[MAX_HEADER_SIZE];
      dwBufLen=MAX_HEADER_SIZE;

      if(!HttpQueryInfo(hRequest,
                        HTTP_QUERY_RAW_HEADERS_CRLF,
                        (LPVOID)pHdrBuf,
                        &dwBufLen,
                        0)) {
        if (pHdrBuf) {
          delete [] pHdrBuf;
          pHdrBuf = NULL;
        }
        errfnstr = "HttpQueryInfo Reply Headers";
        retCode=1;
        goto cleanup;
      }
      const char *pMarker="=======\n";

#define GETRIDOFCRS(BUF)                      \
        for(char *pCh=BUF;*pCh!='\0'; pCh++) {    \
            if(*pCh=='\r')                            \
              *pCh=' ';                               \
        }
      if (pHdrBuf)
        GETRIDOFCRS(pHdrBuf);
      if (pRequestHdrBuf)
        GETRIDOFCRS(pRequestHdrBuf);
      
      errorLog << "HTTP Reply Headers returned for " << args->URL << ":\n" << pMarker << pHdrBuf << endl << pMarker;
      errorLog << "HTTP Request Headers were:\n"<< pRequestHdrBuf << pMarker;
      if (pHdrBuf) {
        delete [] pHdrBuf;
        pHdrBuf = NULL;
      }
#endif
      errorLog << "HTTP status was not OK, failing download!\n";
      retCode = 1;
      goto cleanup;
    }

    DWORD dwContentLen=0;
    dwBufLen = sizeof(dwContentLen);
    if(!HttpQueryInfo(hRequest,
                      HTTP_QUERY_CONTENT_LENGTH
                      | HTTP_QUERY_FLAG_NUMBER,
                      (LPVOID)&dwContentLen,
                      &dwBufLen,
                      NULL)) {
      // HTTP responses dont officially require a content-length,
      // but I'm going to assume our servers will always provide one.
      // so if we fail to find one its a definite error

      // if we get here it means, proxy server removed the content length
      // until I figure out how to get the content length some other way
      // lets take a leap of faith that file will still download gracefully

#if 0
      errfnstr = "HttpQueryInfo";
      retCode=1;
      goto cleanup;
#else
      dwContentLen = 100;  // I don't care about the progress meter
#endif
    }

#define CHUNKSIZE 100000
    DWORD dwReadSize = CHUNKSIZE;

    pData = new char[dwReadSize];  // save mem, dont allocate mem for whole file
    if(!pData) {
      errorLog << "Error: could not allocate " << dwReadSize << " bytes for " << args->URL << endl;
      retCode=1;
      goto cleanup;
    }

    DWORD dwBytesRead;
    do {
      if(!InternetReadFile(hRequest, pData, dwReadSize, &dwBytesRead)) {
        errfnstr = "InternetReadFile";
        retCode = 1;
        goto cleanup;
      }

      if(dwBytesRead==0)
        continue;

      dwTotalBytesRead+=dwBytesRead;

      if(args->bDoMemoryDownload) {
        args->pStringStrm->write(pData, dwBytesRead);
      } else {
        DWORD dwBytesWritten;
        BOOL bRetVal=WriteFile(hFile,pData,dwBytesRead,&dwBytesWritten,NULL);

        if((!bRetVal) || (dwBytesRead!=dwBytesWritten)) {
          if(dwBytesRead!=dwBytesWritten)
            errorLog << "WriteFile did not write enough bytes: BytesToWrite: " << dwBytesRead << " BytesWritten: " <<dwBytesWritten << endl;
          errfnstr = "WriteFile";
          retCode = 1;
          goto cleanup;
        }
      }

      //            *(args->pDownloadPercent) = (float) dwBytesRead/(float)dwTotalBytesRead;

      if(args->pDownloadPercent!=NULL) {
        if (args->iPatchSize)
          *(args->pDownloadPercent) = (float) (dwTotalBytesRead + *args->pPatchSizeSoFar)/(float)args->iPatchSize;
        else
          *(args->pDownloadPercent) = (float) dwTotalBytesRead/(float)dwContentLen;
      }

      errorLog << args->destFilename << " % loaded " << (long)(*args->pDownloadPercent*100) << "\n";
      //      Sleep(1000);

    } while(dwBytesRead!=0);

    if(dwTotalBytesRead != dwContentLen) {
#if 0
      errorLog << "Total bytes read "<<dwTotalBytesRead<< " does not equal specified total length: "<<dwContentLen << endl;
      errfnstr = "InternetReadFile";
      retCode = 1;
      goto cleanup;
#else
      // Just trust TCP and keep going, if corrupted, it will crash somewhere
#endif
    }

  cleanup:
    if(retCode!=0) {
      errorLog << errfnstr <<"("<<args->URL<<") failed, ";
      DWORD err=GetLastError();
      if(err==ERROR_HTTP_HEADER_NOT_FOUND) {
        errorLog << "HTTP_HEADER_NOT_FOUND\n";
      } else {
        // errors that start with 12000 are in wininet.h
        errorLog << "err: " << err << endl;
      }

      if(err==ERROR_INTERNET_EXTENDED_ERROR) {
        DWORD msgbuflen;
        char msgbuf[1024];
        msgbuf[0]='\0';
        msgbuflen=sizeof(msgbuf);
        InternetGetLastResponseInfo(&err,msgbuf,&msgbuflen);
        errorLog << "InternetGetLastResponseInfo() returns error "<< err
            << " : "<< msgbuf <<endl;
      }
    } else {
      errorLog << "Downloaded '" << args->URL<< "'; Total Bytes: " << dwTotalBytesRead << endl;
      if (args->iPatchSize)
        *args->pPatchSizeSoFar += dwTotalBytesRead;
    }
    if(pData!=NULL) {
      delete [] pData;
      pData = NULL;
    }
    if(pRequestHdrBuf!=NULL) {
      delete [] pRequestHdrBuf;
      pRequestHdrBuf = NULL;
    }
    if(hRequest!=NULL)
      InternetCloseHandle(hRequest);
    if(hConnection!=NULL)
      InternetCloseHandle(hConnection);
    if(hSession!=NULL)
      InternetCloseHandle(hSession);
    if(hFile!=NULL)
      CloseHandle(hFile);
  }
  // we must free args, not caller if we execute in a seperate thread
  bool bDoExitThread=args->bDoExitThread;

  // for memory download, need to keep 'args' around since it contains pStrStrm which
  // contains the returned buffer
  if(!args->bDoMemoryDownload)
    delete args;

  if(bDoExitThread)
    ExitThread(retCode);

  return retCode;
}

HANDLE installerBase::
asyncDownloadToFile(const char *URL, const char *destFilename, bool bUseURLDownload) {
  HANDLE retHandle=NULL;

  DLArgs_s *args = new DLArgs_s;
  if (NULL == args)
    return NULL;
  ZeroMemory(args,sizeof(DLArgs_s));

  args->URL = URL;
  args->destFilename = destFilename;
  args->pProxyUser=&_ProxyUserName;
  args->pProxyPW=&_ProxyUserPassword;
  args->pDownloadPercent=&_PercentFileDownloaded;
  args->pPatchSizeSoFar = &_PatchSizeSoFar;
  args->iPatchSize = _PatchSize;
  args->bUseURLDownloadtoFile=bUseURLDownload;

#ifdef SYNCHRONOUS_DOWNLOAD
  DownloadFunc(args);
  //  Sleep(60000);   // simulate a long modem dwnload

  retHandle=(HANDLE)500;   // non-zero indicates success
#else
  args->bDoExitThread=true;
  DWORD dummy;
  retHandle = CreateThread(NULL, 0, DownloadFuncStub, (void*)args,  0, &dummy);

  if(!retHandle) {
    // normally cant free args here since DownloadFunc is still using them,
    // but if DownloadFunc didnt start, have to free args ourselves
    delete args;
  }
#endif

  return retHandle;
}

/* returns:
   0: download in progress
   1: success
   -1: error downloading file
   -2: internal error

   if download is done, threadResult is set to:
*/
int installerBase::
asyncDownloadDone(HANDLE handle) {
#ifdef SYNCHRONOUS_DOWNLOAD
  return 1;
#endif

  BOOL result;
  DWORD exitCode;

  result = GetExitCodeThread(handle, &exitCode);
  if (!result) {
    // call failed
    return -2;
  }

  if (exitCode == STILL_ACTIVE) {
    // thread is still active
    return 0;
  }

  if (exitCode)
    return -1; // download failed

  // success!
  return 1;
}

unsigned long UploadFunc(UploadArgs_s *args) {
  DWORD retCode = 0;    // 0 == success

  // BUGBUG: remove this when ready to test jsproxy again
  // I thought jsproxy might be interfering with InternetOpen(PRECONFIG),
  // so I wanted to try specifying explicit proxy with InternetOpen.
  // didnt fix wininet crashes w/jsproxy, so go back to old way of always
  // using PRECONFIG for now
  args->pProxy=NULL;

  if(args->pUploadPercent!=NULL)
    *(args->pUploadPercent) = 0.0f;

  // hopefully wininet will not have the same COM-reentrancy problems
  // if it does, we can stop using a separate thread and instead use
  // wininet async mode w/callbacks.

  const char *errfnstr = "";
  HINTERNET  hSession = NULL;
  HINTERNET  hConnection = NULL;
  HINTERNET  hRequest = NULL;
  char *pRequestHdrBuf = NULL;
  bool bPrintINETErrMsg = false;
  char *pData = NULL;
  DWORD dwTotalBytesRead=0;
  DWORD dwBufLen;

  // dont we already know we're connected by this point?
  DWORD retVal = InternetAttemptConnect(0x0);
  if(retVal!=ERROR_SUCCESS) {
    errfnstr = "InternetAttemptConnect";
    retVal=1;
    bPrintINETErrMsg = true;
    goto cleanup;
  }

  URL_COMPONENTS url_comp;
  ZeroMemory(&url_comp,sizeof(url_comp));
  url_comp.dwStructSize = sizeof(url_comp);

  char hostnamebuf[512];
  ZeroMemory(hostnamebuf,sizeof(hostnamebuf));
  url_comp.lpszHostName=hostnamebuf;
  url_comp.dwHostNameLength=sizeof(hostnamebuf);

  char urlstrbuf[1024];;
  url_comp.lpszUrlPath = urlstrbuf;
  url_comp.dwUrlPathLength=sizeof(urlstrbuf);
  if(!InternetCrackUrl(args->URL,0,0x0,&url_comp)) {
    errfnstr = "InternetCrackUrl";
    retCode=1;
    goto cleanup;
  }

  if((url_comp.nScheme!=INTERNET_SCHEME_HTTP) && (url_comp.nScheme!=INTERNET_SCHEME_HTTPS)) {
    // due to the httpOpenRequest stuff.  should be easy to adapt if need arises tho
    errorLog << "UploadFunc not yet designed for non-http URLs!\n";
    errfnstr = "InternetCrackUrl";
    retCode=1;
    goto cleanup;
  }

  DWORD DefaultProxyAccessType=INTERNET_OPEN_TYPE_PRECONFIG;  // use IE (auto)proxy info from registry
  /*
    if(strstr(args->URL,"ttown")!=NULL) {
    // HACK: ttown doesnt use proxy!  shouldnt preconfig work if you have bypass's set?  whatever.
    DefaultProxyAccessType=INTERNET_OPEN_TYPE_DIRECT;
    }
  */
  if(args->pProxy==NULL) {
    hSession = InternetOpen("Toontown Installer",
                            DefaultProxyAccessType,
                            NULL,  // no explicit proxy
                            NULL,  // no proxy bypass
                            0x0);  // no flags
  } else {
    hSession = InternetOpen("Toontown Installer",
                            INTERNET_OPEN_TYPE_PROXY,  // use IE proxy info from registry
                            args->pProxy->c_str(),
                            NULL,  // no proxy bypass
                            0x0);  // no flags
  }

  if(!hSession) {
    errfnstr="InternetOpen";
    retCode = 1;
    goto cleanup;
  }

#if 0
  // right now this always fails with INVALID_HANDLE_TYPE even on proxy's requiring a pw,
  // so passing hSession is likely wrong, or done at the wrong time
  // removing until able to get it workin
  if((args->pProxyUser!=NULL)&&(args->pProxyPW!=NULL)) {
    char usernamebuf[512];
       DWORD err,usernamebuflen=sizeof(usernamebuf);
       HINTERNET hQueryInet = hSession;

       BOOL bRet = InternetQueryOption(hQueryInet, INTERNET_OPTION_PROXY_USERNAME, usernamebuf, &usernamebuflen);
       if(!bRet) {
         err = GetLastError();
         errorLog << "InternetQueryOption(INTERNET_OPTION_PROXY_USERNAME) failed, err=" << err << endl;
       } else {
         char pwbuf[512];
         DWORD pwbuflen=sizeof(pwbuf);
         BOOL bRet = InternetQueryOption(hQueryInet, INTERNET_OPTION_PROXY_PASSWORD, pwbuf, &pwbuflen);
         if(!bRet) {
           err = GetLastError();
           errorLog << "InternetQueryOption() 2 failed, err=" << err << endl;
         } else {
           // success!  do implicit copy of const char* to string objs
           *(args->pProxyUser) = usernamebuf;
           *(args->pProxyPW) = pwbuf;
         }
       }
  }
#endif

  INTERNET_PORT portNum = ((url_comp.nPort!=0) ? url_comp.nPort : INTERNET_DEFAULT_HTTP_PORT);

#ifndef NDEBUG
  // are we gonna get config spam if I print this to log?
  errorLog << "Opening connection to "<<url_comp.lpszHostName<<":"<<portNum << endl;
#endif

  // this fn is expensive, should we cache hConnection across multiple calls?
  hConnection = InternetConnect(hSession,
                                url_comp.lpszHostName,
                                portNum,
                                ((args->pProxyUser!=NULL)? args->pProxyUser->c_str() : NULL),
                                ((args->pProxyPW!=NULL)? args->pProxyPW->c_str() : NULL),
                                INTERNET_SERVICE_HTTP,
                                INTERNET_FLAG_NO_CACHE_WRITE,
                                NULL);    // No Context
  if(!hConnection) {
    errfnstr="InternetConnect";
    retCode = 1;
    goto cleanup;
  }

  const char *TypeArray[2] = { "*/*", NULL};
  /*
   */
  hRequest = HttpOpenRequest(hConnection,
                             "POST",
                             url_comp.lpszUrlPath,
                             NULL,    // Default HTTP Version
                             NULL,    // No Referrer
                             TypeArray,  // Accept anything
                             INTERNET_FLAG_NO_CACHE_WRITE
                             | INTERNET_FLAG_KEEP_CONNECTION
                             | INTERNET_FLAG_NO_UI, // needed for user/pw auth??
                             NULL);   // No Context
  if(!hRequest) {
    errfnstr = "HttpOpenRequest";
    retCode = 1;
    goto cleanup;
  }

#if 0
    // save the request headers in case we need to print them out l8r due to an error
#define MAX_HEADER_SIZE 10000 // hopefully the hdrs will be smaller than this
  pRequestHdrBuf = new char[MAX_HEADER_SIZE];
  dwBufLen=MAX_HEADER_SIZE;
  if(!HttpQueryInfo(hRequest,
                    HTTP_QUERY_RAW_HEADERS_CRLF|HTTP_QUERY_FLAG_REQUEST_HEADERS,
                    (LPVOID)pRequestHdrBuf,
                    &dwBufLen, 0)) {
    errfnstr = "HttpQueryInfo Request Headers";
    retCode=1;
    goto cleanup;
  }
#endif

  //send the postdata along with the content-type header.
  if(!HttpSendRequest(hRequest, args->pHeaderStr, strlen(args->pHeaderStr),
              (LPVOID)args->pBuf, args->cBufSize))
  {
    errfnstr = "HttpSendRequest";
    retCode = 1;
    goto cleanup;
  }

  DWORD HTTP_StatusCode=0;
  dwBufLen = sizeof(HTTP_StatusCode);

  if(!HttpQueryInfo(hRequest,
                    HTTP_QUERY_STATUS_CODE
                    | HTTP_QUERY_FLAG_NUMBER,  // HTTP_QUERY_FLAG_NUMBER tells it to return a dword, not a string
                    (LPVOID)&HTTP_StatusCode,
                    &dwBufLen,
                    0)) {
    errfnstr = "HttpQueryInfo Status";
    retCode=1;
    goto cleanup;
  }

  if(HTTP_StatusCode!=HTTP_STATUS_OK) {
    errorLog << "HTTP Status "<< HTTP_StatusCode << ": ";

#ifdef OPTIMIZE_HTTP_SESSION_CODE
    handleHttpStatusNotOk(hRequest, pRequestHdrBuf, &errfnstr, args->URL);
#else
    char StatusText[1024];
    dwBufLen=1024;

    if(!HttpQueryInfo(hRequest,
                      HTTP_QUERY_STATUS_TEXT,
                      (LPVOID)StatusText,
                      &dwBufLen,
                      0)) {
      errfnstr = "HttpQueryInfo StatusText";
      retCode=1;
      goto cleanup;
    }
    errorLog << StatusText << endl;

    char *pHdrBuf = new char[MAX_HEADER_SIZE];
    dwBufLen=MAX_HEADER_SIZE;

    if(!HttpQueryInfo(hRequest,
                      HTTP_QUERY_RAW_HEADERS_CRLF,
                      (LPVOID)pHdrBuf,
                      &dwBufLen,
                      0)) {
      if (pHdrBuf) {
        delete [] pHdrBuf;
        pHdrBuf = NULL;
      }
      errfnstr = "HttpQueryInfo Reply Headers";
      retCode=1;
      goto cleanup;
    }
    const char *pMarker="=======\n";

#define GETRIDOFCRS(BUF)                      \
        for(char *pCh=BUF;*pCh!='\0'; pCh++) {    \
            if(*pCh=='\r')                            \
              *pCh=' ';                               \
        }
    if (pHdrBuf)
      GETRIDOFCRS(pHdrBuf);
    if (pRequestHdrBuf)
      GETRIDOFCRS(pRequestHdrBuf);

    errorLog << "HTTP Reply Headers returned for " << args->URL << ":\n" << pMarker << pHdrBuf << endl << pMarker;
    errorLog << "HTTP Request Headers were:\n"<< pRequestHdrBuf << pMarker;

    if (pHdrBuf) {
      delete [] pHdrBuf;
      pHdrBuf = NULL;
    }
#endif    
    errorLog << "HTTP status was not OK, failing upload!\n";
    retCode = 1;
    goto cleanup;
  }

 cleanup:
  if(retCode!=0) {
    errorLog << errfnstr <<"("<<args->URL<<") failed, ";
    DWORD err=GetLastError();
    if(err==ERROR_HTTP_HEADER_NOT_FOUND) {
      errorLog << "HTTP_HEADER_NOT_FOUND\n";
    } else {
      // errors that start with 12000 are in wininet.h
      errorLog << "err: " << err << endl;
    }

    if(err==ERROR_INTERNET_EXTENDED_ERROR) {
      DWORD msgbuflen;
      char msgbuf[1024];
      msgbuf[0]='\0';
      msgbuflen=sizeof(msgbuf);
      InternetGetLastResponseInfo(&err,msgbuf,&msgbuflen);
      errorLog << "InternetGetLastResponseInfo() returns error "<<err << " : "<<msgbuf<<endl;
    }
  }

  if(pData!=NULL)
    delete [] pData;
  if(pRequestHdrBuf!=NULL)
    delete [] pRequestHdrBuf;
  if(hRequest!=NULL)
    InternetCloseHandle(hRequest);
  if(hConnection!=NULL)
    InternetCloseHandle(hConnection);
  if(hSession!=NULL)
    InternetCloseHandle(hSession);

#if 0
  // we must free args, not caller if we execute in a seperate thread
  bool bDoExitThread=args->bDoExitThread;

  if(bDoExitThread)
    ExitThread(retCode);
#endif

  return retCode;
}

void installerBase::
removeURLFromCache(const char *URL) {
  if (!DeleteUrlCacheEntry(URL)) {
    if (GetLastError() == ERROR_ACCESS_DENIED) {
      errorLog << "Error removing " << URL << " from IE cache" << endl;
    }
  }
}

// process methods
int installerBase::
spawnProcess(const char *cmdLine, int show, HANDLE *phProcess, DWORD *pProcID)
{
  PROCESS_INFORMATION pi;
  STARTUPINFO si = { sizeof(si) };
  bool bResult = false;
  char commandLine[_MAX_PATH];
  int lastErrorCode = 0;

  if(pProcID != NULL)
    *pProcID = 0;
  if(phProcess != NULL)
    *phProcess = NULL;

  strlcpy(commandLine, cmdLine, _MAX_PATH);

  si.dwFlags  = STARTF_USESHOWWINDOW;
  if(SPAWN_HIDDEN == show) {
    // don't show a "feedback" mouse cursor
    si.dwFlags |= STARTF_FORCEOFFFEEDBACK;
  }
  switch(show) {
  case SPAWN_HIDDEN:
    si.wShowWindow = SW_HIDE;
    break;
  case SPAWN_NORMAL:
  default:
    si.wShowWindow = SW_SHOWNORMAL;
    break;
  }

  // here we use a SECURITY_DESCRIPTOR to specify *no DACL at all*, which should be equivalent to all RW
  // this doesnt appear to change the permissions of files created by this child process,
  // but I'll leave it in anyway

  SECURITY_DESCRIPTOR sd;
  InitializeSecurityDescriptor(&sd, SECURITY_DESCRIPTOR_REVISION);
  SetSecurityDescriptorDacl(&sd, TRUE, 0, FALSE);
  SECURITY_ATTRIBUTES sa = { sizeof(SECURITY_ATTRIBUTES), &sd, true };

  bResult = CreateProcess(NULL, commandLine, &sa, &sa, true, 0, NULL, NULL, &si, &pi) == TRUE;
  lastErrorCode = GetLastError();

  if (bResult)
  {
	CloseHandle(pi.hThread);			// not using this
	if (phProcess != NULL)
		*phProcess = pi.hProcess;
	else
		CloseHandle(pi.hProcess);		// not using so clean up

	if(pProcID != NULL)
		*pProcID = pi.dwProcessId;
  }
  else
  { // convention is to return zero on success, so invert boolean result
    errorLog << "system error " << lastErrorCode << " creating process with cmd line: " << commandLine << endl;
	return lastErrorCode ? lastErrorCode : 1;	// return error code if non-zero
  }

  return 0;
}

int installerBase::
processActive(HANDLE hProcess) {
  DWORD JunkExitCode;
  return processActive(hProcess,JunkExitCode);
}

int installerBase::
processActive(HANDLE hProcess,DWORD &exitCode) {
  exitCode=0;
  if (NULL == hProcess)
    return 0;

  if (0 == GetExitCodeProcess(hProcess, &exitCode)) {
    // GetExitCodeProcess() failed.
    return 0;
  }

  bool bActive = (STILL_ACTIVE == exitCode);

  if(!bActive && (exitCode!=0)) {
    errorLog << "ERROR: spawnedProcess returned ErrorCode " << exitCode << " (0x" <<(void*)exitCode << ")\n";
  }

  return bActive;
}

// MD5 methods
void installerBase::
calcFileMD5(const char *fname, MD5HashVal &ret) {
  md5_a_file(fname, ret);
}

// patching methods
int installerBase::
applyPatch(const char *patchFileName, const char *fileName) {
  return apply_patch(patchFileName, fileName);
}

// Panda3D utility methods

#ifdef PANDA_LOCATED_SEPARATE_FROM_TT
int installerBase::
pandaRegInit() {
  HKEY SOFTWARE_key;

  if (_pandaRegInitialized) return 0;

  if (_hKeyPanda3D = regOpenKey(HKEY_CURRENT_USER, "SOFTWARE\\Panda3D"))
  {
    _pandaRegInitialized = 1;
    return 0;
  }

  return 1;
}

void installerBase::
pandaRegShutdown() {
  if (_pandaRegInitialized)
  {
    _pandaRegInitialized = 0;
    regCloseKey(_hKeyPanda3D);
    _hKeyPanda3D = NULL;
  }
}
#endif

void installerBase::
setPandaServer(const char *pandaServerURL) {
  char temp[_MAX_PATH];

  strcpy(_pandaServerURL, pandaServerURL);
  sprintf(temp, "%s/content", _pandaServerURL);
  _launcherProgress_IFilename.setRemotePath(temp);
  _launcherFileDB_IFilename.setRemotePath(_pandaServerURL);
  _launcherDDBFile_IFilename.setRemotePath(_pandaServerURL);
  _launcherSelfExtractor_IFilename.setRemotePath(_pandaServerURL);
}

////////////////////////////////////////////////////////////////////
// getLatestLauncherFileDB - returns 0 on success
//  downloads the latest launcher file database
int installerBase::
getLatestLauncherFileDB()
{
  errorLog << "Downloading latest launcher file database..." << endl;

  const char *url = _launcherFileDB_IFilename.getFullRemoteName();
  // errorLog << "Downloading " << url << endl; // security issue??
  string lDBString;

  // BUGBUG: want to use downloadToMem_New here
  if(!downloadToMem(url,lDBString)) {
    errorLog << "Error downloading " << url << endl;
    return 1;
  }

  // create a fileDB from the buffer
  int result = _launcherFileDB.readFromString(lDBString);

  if (result) {
    errorLog << "Error reading creating launcher file database from "
             << _launcherFileDB_IFilename.getFullRemoteName() << endl;
    return 1;
  }

  // download the launcherFileDb.ddb
  url = _launcherDDBFile_IFilename.getFullRemoteName();
  // BUGBUG: want to use downloadToMem_New here
  if(!downloadToMem(url,lDBString)) {
    errorLog << "Error downloading " << url << endl;
    return 1;
  }

  // create a fileDB from the buffer
  result = _launcherDDBFile.readFromString(lDBString);

  if (result) {
    errorLog << "Error reading creating launcher file database from "
             << _launcherDDBFile_IFilename.getFullRemoteName() << endl;
    return 1;
  }

  errorLog << "done." << endl;

  // strange! if the last line of launcherFileDb doesn't have a newline/EOF
  // _launcherFileDb doesn't recognize the line above?! have to investigate
  //  launcherFileValid(_launcherSelfExtractor_IFilename);

  // 9/2/03, download the progress file that has progress meter info
  url = _launcherProgress_IFilename.getFullRemoteName();
  errorLog << "local progress " << _launcherProgress_IFilename.getFullLocalName() << endl;
  if(!downloadToFile(_launcherProgress_IFilename.getFullRemoteName(),
                     _launcherProgress_IFilename.getFullLocalName())) {
    errorLog << "Error downloading " << url << endl;
    return 1;
  }
  // TODO
  // get encrypted checksum
  // get decryption key
  // decrypt checksum
  // compute checksum of database
  // compare checksums

  return 0;
}

// since only a part of our install is done by WISE, the 'installed size' field in 2000/XP Add/Remove programs
// will be much smaller than it should be.  hack the registry to make it right.
// only call this on XP/2000!  total_size is in bytes, ARP_ProgramName must match value of program name
// displayed in Add/Remove Programs

// BUGBUG: Hmm, is this incorrectly causing the installed size to eventually be double actual size on win2k?
// Does ARP manager eventually add stuff to the existing value sometime after initial install?
// maybe it reupdates disk usage periodically, in which case this fn is not needed, so ifdef out for now.
void installerBase::
writeInstalledSizeToRegistry(const char *ARP_ProgramName,unsigned __int64 total_size) {
#if 0
  const char *szARPDataName="SlowInfoCache";
  BYTE *pBuffer = NULL;
  string ARP_RegKey=AddRemoveProgsCache;
  ARP_RegKey.append("\\");
  ARP_RegKey.append(ARP_ProgramName);

  HKEY hARPKey = regOpenKey(HKEY_LOCAL_MACHINE, ARP_RegKey.c_str());
  if(hARPKey==NULL) {
    errorLog << "Error: couldn't open Add/Rem progs regkey to change size, err=" << GetLastError() << endl;
    return;
  }

    // get size of data
  DWORD valType;
  DWORD dwBufLen=0;
  LONG retVal=RegQueryValueEx(hARPKey,szARPDataName,0,&valType,NULL,&dwBufLen);
  if(retVal == ERROR_NOT_FOUND) {
    // I dont know when SlowInfoCache is actually created (doesnt seem to be after InstallLauncher.exe is run),
    // so just exit and maybe it will be created next time this is called
    errorLog << "Mild warning: " << szARPDataName<<" doesnt exist in registry yet, cant set proper Add/Remove installed size\n";
    goto cleanup;
  }

  if(ERROR_SUCCESS!=retVal) {
    errorLog << "Error: couldn't open " << szARPDataName<<" to change size, err=" << retVal << endl;
    goto cleanup;
  }

    /*
      format of undocumented SlowInfoCache binary data is
      type
      TSlowInfoCache = record
      cbSize      : DWORD;
      HasName     : LongBool;
      InstallSize : Int64;
      LastUsed    : TFileTime;
      Frequency   : Integer;
      Name        : ARRAY[0..261] OF WideChar;
      end;
      see http://www.pcmag.com/article2/0,4149,551378,00.asp
    */

  typedef struct {
    DWORD    cbSize;
    DWORD    HasName;
    __int64  InstallSize;
    /*
      ... other junk ...
    */
    } SlowInfoCacheData;

  pBuffer= new BYTE[dwBufLen];
  SlowInfoCacheData *pSIData=(SlowInfoCacheData *)pBuffer;

  retVal=RegQueryValueEx(hARPKey,szARPDataName,0,&valType,pBuffer,&dwBufLen);
  if(ERROR_SUCCESS!=retVal) {
    errorLog << "Error: couldn't get " << szARPDataName<<" data, err=" << retVal << endl;
    goto cleanup;
  }

  pSIData->InstallSize=total_size;

  retVal=RegSetValueEx(hARPKey,szARPDataName,0,valType,pBuffer,dwBufLen);
  if(ERROR_SUCCESS!=retVal) {
    errorLog << "Error: couldn't write " << szARPDataName<<" data, err=" << GetLastError() << endl;
    goto cleanup;
  }

 cleanup:
  if(pBuffer != NULL)
    delete [] pBuffer;

  RegCloseKey(hARPKey);
#endif
}

int installerBase::
verifyFileMD5(fileDBEntry *launcherFile, bool debug) {
  fileDB_MD5 *cur_MD5 = launcherFile->_head;

  // make a full pathname for the file
  char fullName[_MAX_PATH];
  if (!launcherFile->fullPathname(fullName, _MAX_PATH)) {
    errorLog << "Launcher is invalid: error creating full name for file "
             << launcherFile->_filename << endl;
    return 0;
  }
//  else
//    errorLog << "filename: " << fullName << endl;

  // does the file exist?
  if (!fileExists(fullName)) {
    errorLog <<  fullName << " is missing and thus invalid!\n";
    return 0;
  }

  // compute checksum of file
  MD5HashVal checksum;
  ZeroMemory(&checksum,sizeof(checksum));
  calcFileMD5(fullName, checksum);

#ifdef CHECK_MD5
  // compare with checksum in database
  int badcompare = memcmp(&checksum, &cur_MD5->_hashVal, sizeof(MD5HashVal));
  if (badcompare || debug) {
    errorLog << "database checksum:   " << cur_MD5->_hashVal[0] << " "
             << cur_MD5->_hashVal[1] << " "
             << cur_MD5->_hashVal[2] << " "
             << cur_MD5->_hashVal[3] << endl;
    errorLog << "calculated checksum: " << checksum[0] << " "
             << checksum[1] << " "
             << checksum[2] << " "
             << checksum[3] << endl;
  }
  // if different, fail
  if (badcompare)
  {
    errorLog << launcherFile->_filename << " is invalid -- checksum failed on file " << fullName << endl;
    return 0;
  }
#endif

  return 1;
}

void installerBase::
badFileMD5_debug(const string &name, const string &fullpath)
{
    errorLog << name << ": ";

    DWORD attrs = GetFileAttributes(fullpath.c_str());
    if (attrs != INVALID_FILE_ATTRIBUTES)
        errorLog << attrs;                          // dump file attributes
    else
        errorLog << "no info";                      // got none
    errorLog << endl;
}

////////////////////////////////////////////////////////////////////

// this is a little hack to obviate the launcherFileDB
// to get around not being able to do synchronous downloads
// through the Blast proxy cache.
// since we need to do other synchronous downloads, this
// is irrelevant.
//#define ALWAYS_RUN_LAUNCHER

// hack to enable replacement of launcher files without having
// download overwrite them.  no patching will be done
// #define LAUNCHER_ALWAYS_VALID

////////////////////////////////////////////////////////////////////

// returns a value based on current files on user's computer
LauncherType installerBase::
launcherValid(void) {
#ifdef LAUNCHER_ALWAYS_VALID
  return LAUNCHER_VALID;
#endif

#ifdef ALWAYS_RUN_LAUNCHER
  // HACK - always invalid the first time
  static int firstTime = 1;
  if (!firstTime)
    return 1;
  firstTime = 0;
  return LAUNCHER_INVALID;
#endif

  fileDBEntry *launcherFile = _launcherFileDB.firstFile();

  errorLog << "Checking launcher files validity..." << endl;

  /*
  // make sure we're in the panda3d directory
  if (!SetCurrentDirectory(_panda3DInstallDir))
  {
  return 0;
  }
  */

  // for each file in the database
  while(launcherFile) {
    if(!verifyFileMD5(launcherFile))
    {
      // making the installer little more intelligent
      // Was this InstallLauncher.exe? if not check if InstallLauncher.exe is valid
      if (strcmp(launcherFile->_filename, _launcherSelfExtractor_IFilename.getBaseName()))
      { // not the launcher file
        if (launcherFileValid(_launcherSelfExtractor_IFilename))
        {
          // debug what's wrong with this file
          string fpn = launcherFile->fullPathname();
          badFileMD5_debug(launcherFile->_filename, fpn);

		  // attempt to delete the file manually with whatever security permissions the ActiveX is running under
          if (!DeleteFile(fpn.c_str()))
            errorLog << "Deleting "<<launcherFile->_filename<<" got "<< GetLastErrorStr() << endl;
          
          // re-extract it and check again
          return LAUNCHER_NEED_EXTRACT;
        }
        else {
          // user may have messed up local files re-download it
          return LAUNCHER_NEED_DOWNLOAD;
        }
      }
      else
      { // The launcher that is invalid, or missing, so patch/download it
        return LAUNCHER_NEED_DOWNLOAD;
      }
    }
    launcherFile = launcherFile->_next;
  }

  errorLog << "All Launcher files valid" << endl;
  return LAUNCHER_VALID;
}

// return 1 if true
int installerBase::
launcherFileValid(installerFilename &fileName) {
  const char  *pFileBaseName = fileName.getBaseName();
  errorLog << "Checking if file '"<< pFileBaseName <<"' is valid..." << endl;

  // find the MD5 for the file entry
  fileDBEntry *launcherFile = _launcherFileDB.firstFile();
  for(; launcherFile != NULL; launcherFile = launcherFile->_next) {
    //    errorLog << launcherFile->_filename << endl;
    if(strcmp(launcherFile->_filename, pFileBaseName) == 0)
      break;
  }

  if (launcherFile) {
    if (verifyFileMD5(launcherFile, true)) {
      errorLog << launcherFile->_filename << " is valid" << endl;
      return 1;
    }
  }
  else
    errorLog << "'" << pFileBaseName << "' not found in launcherFileDb!!" << endl;

  return 0;
}
//
// This function only tries to patch InstallLauncher.exe, not anything else
// returns 0 on success
//
int installerBase::
patchLauncherFiles() {
#ifdef LAUNCHER_ALWAYS_VALID
  return 0;
#endif

  int debugCounter = 0;
  int cd_index = 0;
  int numStraightDownloads = 0;

  fileDBEntry *launcherFile = NULL;

  errorLog << "Patching launcher file..." << endl;

  // before patch, find the proper patch directory to download from
  cd_index = findPatchDirectory();

  // set a registry value indicating which version of the game this is. It is helpful
  // for the Launcher.py to figure out where to download patches from
  char tmpBuff[30];
  _itoa(abs(cd_index), tmpBuff, 10);
  setKeyValue("FromCD", tmpBuff);

  if (cd_index < 0)  // checksum matched and proper launcherdb downloded
    return 0;        // no need to patch
  
  // find the patchVersion
  int patch_num,
    file_Patched,
    file_OutOfDate,
    file_Exists;
  file_Patched = file_OutOfDate = file_Exists = 0;

  patch_num = findPatchVersion(_launcherDDBFile, &launcherFile, &file_Exists, &file_OutOfDate);

  while(patch_num && file_Exists && file_OutOfDate) {
    char patchRelativeFilename[_MAX_PATH];
    char patchRemoteFilename[_MAX_PATH];

    errorLog << endl << "patchLauncherFiles pass " << debugCounter << endl;

    // OK, we know which version we have, and we
    // know that there's a patch for that version.
    
    // lets get a count of how many bytes we have to download
    // from the progress file. This is necessary only one time
    if (debugCounter == 0) {
      _PatchSize = GetPatchSize(patch_num+1);
      errorLog << "size = " << _PatchSize << endl;
    }
    
    // form the patch filename
    sprintf(patchRelativeFilename, "%s.v%i.pch", launcherFile->_filename, patch_num+1);
    
    // form the remote patch filename
    if (!cd_index) {
      sprintf(patchRemoteFilename, "%s%s", _pandaServerURL, patchRelativeFilename);
    } else {
      sprintf(patchRemoteFilename, "%sCD_%d/%s", _pandaServerURL, cd_index, patchRelativeFilename);
    }
    
    errorLog << "Downloading patch file " << patchRemoteFilename << endl;
    
    // download the patch file
    if(!downloadToFile(patchRemoteFilename, patchRelativeFilename)) {
      errorLog << "Error downloading patch file " << patchRemoteFilename << endl;
      break;
    }
    
    errorLog << "Applying patch file " << patchRelativeFilename << " to file "
             << launcherFile->_filename << endl;
    
    // apply the patch file
    if(applyPatch(patchRelativeFilename, launcherFile->_filename)) {
      errorLog << "Error applying patch file " << patchRelativeFilename
               << " to file " << launcherFile->_filename << endl;
      break;
    }
    file_Patched = 1;
    ++debugCounter;
    // start the cycle again to get the next patch
    patch_num = findPatchVersion(_launcherDDBFile, &launcherFile, &file_Exists, &file_OutOfDate);
  }
  // if file isn't there, or we didn't patch successfully,
  // download the file from scratch
  if (!file_Exists || (file_OutOfDate && !file_Patched)) {
    char remoteFilename[_MAX_PATH];

    // prevent infinite download loop
    numStraightDownloads++;
    if (numStraightDownloads > 1) {
      errorLog << "Downloaded file " << remoteFilename
               << " but it still doesn't match file database" << endl;
      _PatchSize = 0;
      return 1;
    }

    // form the remote filename
    sprintf(remoteFilename, "%s%s", _pandaServerURL, launcherFile->_filename);
    
    errorLog << "Downloading file " << remoteFilename << endl;
    
    // download the file
    _PatchSize = GetPatchSize(0);
    errorLog << "size = " << _PatchSize << endl;
    if(!downloadToFile(remoteFilename, launcherFile->_filename)) {
      errorLog << "Error downloading file " << remoteFilename << endl;
      _PatchSize = 0;
      return 1;
    }
  }

  // if file has been modified, check/patch it again
  // otherwise, move on to the next file
  if (file_Exists && !file_OutOfDate) {
    numStraightDownloads = 0;
  }
  _PatchSize = 0;
  _PatchSizeSoFar = 0;
  errorLog << "Launcher is valid" << endl;
  return 0;
}
//
// given the fileDB, find the patch version of InstallLauncher that matches
//
int installerBase::
findPatchVersion(fileDB &db, fileDBEntry **dbEntry, int *file_Exists, int *file_OutOfDate) {
  int patch_ver = 0;
  int t1, t2;
  fileDBEntry *launcherFile = db.firstFile();

  if (!file_Exists) file_Exists = &t1;
  if (!file_OutOfDate) file_OutOfDate = &t2;

  // find the InstallLauncher.exe entry in the database
  while(launcherFile) {
    if (strcmp(launcherFile->_filename, _launcherSelfExtractor_IFilename.getBaseName())) {
      launcherFile = launcherFile->_next;
      continue;
    }
    
    // make sure to return the fileDBEntry pointer
    if (dbEntry)
      *dbEntry = launcherFile;

    fileDB_MD5 *cur_MD5 = launcherFile->_head;

    // make a full pathname for the file
    char fullName[_MAX_PATH];
    if (!launcherFile->fullPathname(fullName, _MAX_PATH)) {
      errorLog << "Error patching launcher: could not create full name for file "
               << launcherFile->_filename << endl;
      return 1;
    }
    errorLog << "checking patch for: " << fullName << endl;

    *file_Exists = fileExists(fullName);
    *file_OutOfDate = 0;

    // if file exists, see if it's up-to-date
    if (*file_Exists)
    {
      // compute checksum of file
      MD5HashVal checksum;
      ZeroMemory(&checksum,sizeof(checksum));
      calcFileMD5(fullName, checksum);

      // compare with checksum in database
      // if different, fail
      if (memcmp(&checksum, &cur_MD5->_hashVal, sizeof(MD5HashVal))) {
        *file_OutOfDate = 1;
        errorLog << "Checksum failed on file " << fullName << endl;
        errorLog << "database checksum:   " << cur_MD5->_hashVal[0] << " " << cur_MD5->_hashVal[1] << " "
                 << cur_MD5->_hashVal[2] << " " << cur_MD5->_hashVal[3] << endl;
        errorLog << "calculated checksum: " << checksum[0] << " " << checksum[1] << " "
                 << checksum[2] << " " << checksum[3] << endl;

        // search through list of checksums
        // if found, DL the appropriate patch
        // if not found, scrap file and re-download
        int patch_num = 1;

        cur_MD5 = cur_MD5->_next;
        while (cur_MD5) {
          // is this the MD5 of the file we have?
          if (!memcmp(&checksum, &cur_MD5->_hashVal, sizeof(MD5HashVal))) {
            patch_ver = patch_num;
            return patch_ver;
          }
          ++patch_num;
          cur_MD5 = cur_MD5->_next;
        }
      }
      else {
        // launcher is probably valid already: special cd case
        patch_ver = -1;
      }
    }
    // couldn't find hash or already current
    return patch_ver;
  }
  return patch_ver;
}
//
// find the right patch directory (i.e. is it a CD install?). Then reload the _launcherDDBFile
// from this new directory. Redownload the progress file to rescale progress meter.
//
int installerBase::
findPatchDirectory() {
  char temp[_MAX_PATH];
  string lDBString, url;

  int cd_index = 1;
  int result, patch_ver;

  fileDB cdFileDB;

  while(1) {
    // first look in CD_n directory launcherFileDb
    sprintf(temp, "%sCD_%d/%s", _pandaServerURL, cd_index, _launcherDDBFile_IFilename.getBaseName());
    errorLog << "rollup: trying to download " << temp << endl;
    
    url = temp;

    if (!downloadToMem(url.c_str(), lDBString)) {
      errorLog << "findPatch error: " << GetLastError() << endl;
      return 0;
    }
    cdFileDB.freeDatabase();
    result = cdFileDB.readFromString(lDBString);
    if (result) {
      errorLog << "Error reading creating launcher file database from "
               << url.c_str() << endl;
      return 0;
    }
    patch_ver = findPatchVersion(cdFileDB, NULL, NULL, NULL);
    if (patch_ver) {
      // we have found the proper cd and its patch to download
      errorLog << "rollup: found patch in directory CD_" << cd_index << endl;
      // if found a match in cd directory, mark which cd
      if (patch_ver < 0)
        patch_ver = -cd_index;
      break;
    }
    ++cd_index;
  }
  
  // lets delete the current fileDB and load the fileDB from this CD_n directory
  cdFileDB.freeDatabase();
  _launcherDDBFile.freeDatabase();

  // if we have found a patch on the cd directory that matches current InstallLauncher
  // then load the _launcherDDBFile.
  result = _launcherDDBFile.readFromString(lDBString);
  if (result) {
    errorLog << "Error reading creating launcher file database from "
             << url.c_str() << endl;
    return 0;
  }

  // download the progress file as well and rescale the progress meter
  sprintf(temp, "%sCD_%d/content/%s", _pandaServerURL, cd_index, _launcherProgress_IFilename.getBaseName());
  url = temp;
  errorLog << "local progress " << _launcherProgress_IFilename.getFullLocalName() << endl;
  if(!downloadToFile(url.c_str(),
                     _launcherProgress_IFilename.getFullLocalName())) {
    errorLog << "Error downloading " << url << endl;
    return 0;
  }

  if (patch_ver < 0)  // special case that tells not to patch: InstallLauncher matched database
    return patch_ver;

  return cd_index;
}

// get installerVersionValid
const char *installerBase::
getInstallerVersionValid() {
  bool bValid = false;

  if(!_InstallerActiveXVersionURL.empty()) {
    const char *url = _launcherFileDB_IFilename.getFullRemoteName();
    // errorLog << "Downloading " << url << endl; // security issue??
    string lDBString;

    // BUGBUG: want to use downloadToMem_New here
    if(!downloadToMem(url,lDBString)) {
      errorLog << "Error downloading " << url << endl;
    }

  }
  if(bValid) {
    return "valid";
  }

  return "invalid";
}

// set the value of a particular key; returns 0 on success
int installerBase::
setKeyValue(const char *key, const char *value) {
  if (keyMatch(key, "setInstallerVersionURL")) {
    _InstallerActiveXVersionURL = value;
  } else {
    errorLog << "Unknown installer key in installerBase::setKeyValue(): "
             << key << "=" << value << endl;
    return 1;
  }

  return 0;
}

// gets the value associated with a particular key; returns false on failure
bool installerBase::
getKeyValue(const char *keyName, string &keyValue) {
  if (keyMatch(keyName, "CheckInstallerVersionValid")) {
    keyValue = getInstallerVersionValid();
  } else {
    errorLog << "Unknown installer key in installerBase::getKeyValue(): " << keyName << endl;
    return false;
  }

  return true;
}
// return true if anything suspicious found
bool installerBase::
checkForTroublesomeInstalledSoftware(stringvec &ProgNames) {
  ProgNames.clear();

  registryKey reg;
  HKEY hKey = reg.openRO(HKEY_LOCAL_MACHINE, UninstallProgsListRegKey);
  if(hKey == NULL) {
    errorLog << "failed to open proglist in checkProgs\n";
    return false;
  }

  LONG retCode = ERROR_SUCCESS;

  for (int i = 0; retCode == ERROR_SUCCESS; i++) {
    char SubKeyName[MAX_PATH];
    DWORD dwNameLen = MAX_PATH;
    FILETIME ftLastWriteTime;

    retCode = RegEnumKeyEx(hKey, i, SubKeyName, &dwNameLen, NULL, NULL, NULL, &ftLastWriteTime);

    if (retCode != ERROR_SUCCESS) {
      // reached last subkey
      break;
    }

    registryKey subKey;
    HKEY hSubKey = subKey.openRO(hKey, SubKeyName);
    if(hSubKey == NULL) {
      errorLog << "failed to open proglist subkey: " << SubKeyName << endl;
      continue;
    }

    string ProgName;
    bool bGotOneHit=false;
    string OrigStr;
    char CmpStr[_MAX_PATH];

    // it's ok to be missing DisplayName, it's probably not a user-installed prog but some OS package
    if (!subKey.getString("DisplayName", OrigStr)) {
      strlcpy(CmpStr, OrigStr.c_str(), _MAX_PATH);
      _strlwr(CmpStr);
      for(int i = 0;i < numTroublesomeInstalledProgramStrs; i++) {
        ProgName = CmpStr;
        if(ProgName.find(TroublesomeInstalledProgramStrs[i]) != string::npos) {
          ProgNames.push_back(OrigStr);
          bGotOneHit=true;
          break;  // dont need to output it > once
        }
      }
    }
    subKey.closeKey();

    if(!bGotOneHit) {
      strlcpy(CmpStr, SubKeyName, _MAX_PATH);
      _strlwr(CmpStr);
      for(int i = 0; i < numTroublesomeInstalledProgramStrs; i++) {
        ProgName = CmpStr;
        if(ProgName.find(TroublesomeInstalledProgramStrs[i])!=string::npos) {
          ProgNames.push_back(string(SubKeyName));
          bGotOneHit=true;
          break;  // dont need to output it > once
        }
      }
    }
  }

  for(unsigned i=0; i < ProgNames.size(); i++) {
    errorLog << "found potentially conflicting installed program: " << ProgNames[i] << endl;
  }

  reg.closeKey();
  return (ProgNames.size() > 0);
}

// return true if anything suspicious found
bool installerBase::
checkForTroublesomeRunningSoftware(stringvec &ProgNames) {
  // todo: would be more efficient to enumerate processes once
  ProgNames.clear();

  for(int p=0;p<NUM_TROUBLESOME_RUNNING_PROGSTRS;p++) {
    if(DoesProcessExist(TroublesomeRunningProgramStrs[p].pExeName)) {
      ProgNames.push_back(string(TroublesomeRunningProgramStrs[p].pFriendlyName));
      errorLog << "found potentially conflicting running program: " << TroublesomeRunningProgramStrs[p].pFriendlyName << endl;
    }
  }

  return (ProgNames.size()>0);
}

bool installerBase::
ProgramIsRunning(const char *progname)
{
  char lowercase_progname[MAX_PATH];
  strcpy(lowercase_progname,progname);
  _strlwr(lowercase_progname);

  return DoesProcessExist(lowercase_progname);

  /*  maybe dont need this after all, since above should work on w9x?
      HWND hWnd = FindWindow(NULL,progname);
      return (hWnd!=NULL);
  */
}

void installerBase::
getAllFilesWithPathPattern(const char *pathsearchpattern, StrVec &strVec)
{
  strVec.clear();

  // FindFile doesnt seem to return paths, only base filenames, so prepend the dir

  char FullFilePath[_MAX_PATH];
  strcpy(FullFilePath,pathsearchpattern);
  char *pAfterLastSlash=strrchr(FullFilePath,'\\')+1;

  WIN32_FIND_DATA FindFileData;
  HANDLE hFileSearch = FindFirstFile(pathsearchpattern,&FindFileData);
  if(hFileSearch != INVALID_HANDLE_VALUE)
  {
    strcpy(pAfterLastSlash,FindFileData.cFileName);
    strVec.push_back(FullFilePath);

    while(FindNextFile(hFileSearch,&FindFileData)) {
      strcpy(pAfterLastSlash,FindFileData.cFileName);
      strVec.push_back(FullFilePath);
    }

    FindClose(hFileSearch);

    if(strVec.size()>1) {
      sort(strVec.begin(), strVec.end());
      // TODO: remove this line upon detection of errorlog bug
      for (unsigned int i = 0; i < strVec.size(); ++i)
        errorLog << strVec[i] << endl;
    }
  }
}

void installerBase::
filesearch(string rootpath, string pattern, bool bRecursive, bool bSearchForDirs, bool bPrintFileInfo, StrVec &files) {
  // typical arguments:  filesearch("C:\\temp\\mview","*",true,true,sveclist);
  WIN32_FIND_DATA current_file;

  // first find all the files in the rootpath dir that match the pattern
  string searchpathpattern = rootpath + "\\" + pattern;
  HANDLE searcher = FindFirstFile(searchpathpattern.c_str(), &current_file);
  if ( searcher == INVALID_HANDLE_VALUE)
    return;
  do {
    string fileline;

    if(bSearchForDirs) {
      // save only dirs
      if ((current_file.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
          (!(current_file.cFileName[0] == '.'))) {
        fileline = rootpath + "\\" + current_file.cFileName;
        files.push_back(fileline);
      }
    } else {
      // save only files
      if(!((current_file.cFileName[0] == '.') ||
           (current_file.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))) {
        if(bPrintFileInfo) {
          SYSTEMTIME stime;
          FileTimeToSystemTime(&current_file.ftCreationTime,&stime);
          char extra_info[100];
          sprintf(extra_info, ", (%d/%d/%d), %d bytes",stime.wMonth,stime.wDay,stime.wYear,current_file.nFileSizeLow);
          fileline = rootpath + "\\" + current_file.cFileName + extra_info;
        } else {
          fileline = rootpath + "\\" + current_file.cFileName;
        }
        files.push_back(fileline);
      }
    }
  } while (FindNextFile(searcher, &current_file));
  FindClose(searcher);

  if (bRecursive) {
    // then call yourself recursively on all dirs in the rootpath
    string newsearchpath = rootpath + "\\*";
    HANDLE searcher = FindFirstFile(newsearchpath.c_str(), &current_file);
    if ( searcher == INVALID_HANDLE_VALUE)
      return;
    do {
      if ( current_file.cFileName[0] == '.' ||
           !(current_file.dwFileAttributes &
             FILE_ATTRIBUTE_DIRECTORY))
        continue;
      newsearchpath = rootpath + "\\" + current_file.cFileName;
      filesearch(newsearchpath, pattern, true, bSearchForDirs, bPrintFileInfo, files);
    } while (FindNextFile(searcher, &current_file));
    FindClose(searcher);
  }
}

void installerBase::
GetHardCodedVersion(ULARGE_INTEGER &Ver) {
  // this is the only way I now trust, somehow LoadResource screws up and can give all zero

  Ver.HighPart = (g_InstallerVersion_A << 16) | g_InstallerVersion_B;
  Ver.LowPart  = (g_InstallerVersion_C << 16) | g_InstallerVersion_D;
}

bool MyGetTempPath(DWORD path_buffer_length, char *temp_path) {
  // win9x GetTempPath uses 'current dir' if TEMP/TMP not defined.
  // this is no good, we need an absolute location.
  // so make my own version

  const char *pTempPath;

#define TRYDIR(DIRNAME) \
  pTempPath=getenv(DIRNAME); \
  if(pTempPath!=NULL) { \
      strncpy(temp_path,pTempPath,path_buffer_length); \
      return (strlen(pTempPath)<path_buffer_length); \
  }

  TRYDIR("TMP");
  TRYDIR("TEMP");
  TRYDIR("HOMEPATH");

  // could also try 'c:\' i suppose

  char DirName[_MAX_PATH];
  GetWindowsDirectory(DirName,_MAX_PATH);
  strncpy(temp_path,DirName,path_buffer_length);
  return (strlen(DirName)<path_buffer_length);
}

void ShowErrorBox(const char *msg) {
  MessageBox(NULL, msg, "Installer Error", MB_OK|MB_ICONERROR);
}


// could use this to print out all processes too...
bool DoesProcessExist(const char *process_name) {
  HANDLE         hProcessSnap = NULL;
  bool           bRet      = false;
  PROCESSENTRY32 pe32      = {0};

  //  Take a snapshot of all processes in the system.

  hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

  if (hProcessSnap == INVALID_HANDLE_VALUE)
    return false;

  //  Fill in the size of the structure before using it.
  pe32.dwSize = sizeof(PROCESSENTRY32);

  //  Walk the snapshot of the processes, and for each process,
  //  display information.

  if(Process32First(hProcessSnap, &pe32)) {
    do {
      _strlwr(pe32.szExeFile);
      string process_path=pe32.szExeFile;
      if(process_path.find(process_name)!=string::npos) {
        bRet=true;
        goto cleanup;
      }
    } while (Process32Next(hProcessSnap, &pe32));
  }

 cleanup:
  CloseHandle (hProcessSnap);
  return bRet;
}

HMODULE GetOurModuleHandle(void) {
  MEMORY_BASIC_INFORMATION mbi;
  HMODULE hMod = NULL;
  if (VirtualQuery(GetOurModuleHandle, &mbi, sizeof(mbi))) {
    hMod = (HMODULE)mbi.AllocationBase;
  }
  return hMod;
}
//
// Given the ifstream of progress, and name to look for, it returns corresponding size
//
int GetSizeFromProgress(ifstream &progressFile, char *patchFilename)
{
  char tmpBuff[MAX_PATH];
  char numString[MAX_PATH];

  int size = 0;
  string buff;
  string::size_type loc, si, ei;

  // find this name in progressFile
  while(1) {
    progressFile.getline(tmpBuff, MAX_PATH);
    buff.assign(tmpBuff);
    loc = buff.find(patchFilename);
    if (loc != string::npos) {
      // found it, then look for the number
      //      errorLog << "found " << tmpBuff << " at " << loc << endl;
      loc = buff.find_first_of(" ", loc);
      //      errorLog << "found last character of " << tmpBuff << " at " << loc << endl;
      si = loc+1;
      ei = buff.find_first_of("L", loc);
      buff.copy(numString, ei-si, si);
      numString[ei-si] = 0;
      //      errorLog << "string is " << numString << " ";
      size = atoi(numString);
      //      errorLog << patchFilename << " size = " << size << endl;
      break;
    } else if (progressFile.eof()) {
      errorLog << patchFilename << " not found in progress" << endl;
      break;
    }
  }
  return size;
}
//
// This function reads the progress file to count total
// download bytes for the patches upto highVer. if highVer is 0
// it returns the size of InstallLauncher.exe
//
int GetPatchSize(int highVer) {
  char patchFilename[MAX_PATH];
  char progressFilename[MAX_PATH];

  string buff;
  int size = 0;
  ifstream progressFile;

  sprintf(progressFilename, "progress");

  // open progress file to read
  progressFile.open(progressFilename, ifstream::in);
  if (progressFile.fail()) {
    ShowErrorBox("Couldn't read file: progress");
    return 0;
  }
  if (!highVer) { 
    // special case, want the size of launcher
    size = GetSizeFromProgress(progressFile, "InstallLauncher.exe");
  }
  else {
    
    int i=2;
    while (i<=highVer) {
      sprintf(patchFilename, "InstallLauncher.exe.v%i.pch", i);
      size += GetSizeFromProgress(progressFile, patchFilename);
      ++i;
    }
  }
  progressFile.close();

  return size;
}
//
//
//
