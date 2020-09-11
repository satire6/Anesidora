// Filename: winhttp.cxx
// Created by:  cxgeorge (05Dec00)
//
////////////////////////////////////////////////////////////////////

// need separate file because winhttp.h and wininet.h have conflicting defns
// thanks MS!

#include "pragma.h"
#include <stdlib.h>
#include <string>
#include <windows.h>
#include <winhttp.h>
#include <assert.h>
#include "log.h"

// return string on success, NULL on failure
// must call delete [] on returned string
string get_proxyname_using_winhttp(bool bAutoDetection)
{
    const char *szWinHttpGetIEProxyConfigForCurrentUser="WinHttpGetIEProxyConfigForCurrentUser";
    const char *szWinHttpGetProxyForUrl="WinHttpGetProxyForUrl";
    const char *ErrGetProcAddr = "GetProcAddr failed on ";
    const char *ErrRetStr = " returned error ";

    string returnedProxyStr;

    HINSTANCE hWinHTTP = LoadLibrary("winhttp.dll");
    if(!hWinHTTP) {
      errorLog <<  "WinHttp.dll not found\n";
      return returnedProxyStr;
    }

    char *pProxyStr = NULL;
    LPWSTR pAutoConfigUrl = NULL;
    // new fns in winhttp 5.1 (and only on win2k/XP, not 9x), dont want to statically link to them

    if(!bAutoDetection) {
       // would just pass the string in from wininet, but winhttp likes widechar strings
       typedef BOOL (WINAPI *PFN_WinHttpGetIEProxyConfigForCurrentUser)(WINHTTP_CURRENT_USER_IE_PROXY_CONFIG *pProxyConfig);
       PFN_WinHttpGetIEProxyConfigForCurrentUser pfWinHttpGetIEProxyConfigForCurrentUser;
       pfWinHttpGetIEProxyConfigForCurrentUser = (PFN_WinHttpGetIEProxyConfigForCurrentUser) GetProcAddress(hWinHTTP,szWinHttpGetIEProxyConfigForCurrentUser);
       if(!pfWinHttpGetIEProxyConfigForCurrentUser) {
           errorLog <<  ErrGetProcAddr << szWinHttpGetIEProxyConfigForCurrentUser << endl;
           goto cleanup;
       }

       WINHTTP_CURRENT_USER_IE_PROXY_CONFIG UserProxyConfig;
       ZeroMemory(&UserProxyConfig,sizeof(UserProxyConfig));
       if(!(*pfWinHttpGetIEProxyConfigForCurrentUser)(&UserProxyConfig)) {
            errorLog << szWinHttpGetIEProxyConfigForCurrentUser << ErrRetStr << GetLastError() << endl;
            goto cleanup;
       }
       if(UserProxyConfig.lpszProxyBypass!=NULL)
           GlobalFree(UserProxyConfig.lpszProxyBypass);
       if(UserProxyConfig.lpszProxy!=NULL) {
           GlobalFree(UserProxyConfig.lpszProxy);
           // if we get here, it should mean an explict proxy has been specified in IE, which
           // but winhttp proxy settings and IE proxy settings are separate
           errorLog << szWinHttpGetIEProxyConfigForCurrentUser << "returned a proxy, huh?\n";
       }
       pAutoConfigUrl = UserProxyConfig.lpszAutoConfigUrl;
       if(pAutoConfigUrl == NULL) {
            errorLog << szWinHttpGetIEProxyConfigForCurrentUser << "returned a null str!\n";
            goto cleanup;
       }
    }

    typedef BOOL (WINAPI *PFN_WinHttpGetProxyForUrl)(HINTERNET hSession,LPCWSTR lpcwszUrl,
                                                    WINHTTP_AUTOPROXY_OPTIONS *pAutoProxyOptions,
                                                    WINHTTP_PROXY_INFO *pProxyInfo);

    PFN_WinHttpGetProxyForUrl pfWinHttpGetProxyForUrl =
                    (PFN_WinHttpGetProxyForUrl)GetProcAddress(hWinHTTP,szWinHttpGetProxyForUrl);

    if(!pfWinHttpGetProxyForUrl) {
      errorLog <<  ErrGetProcAddr << szWinHttpGetProxyForUrl << endl;
      goto cleanup;
    }

    const char *szWinHttpOpen="WinHttpOpen";

    typedef HINTERNET (WINAPI *PFN_WinHttpOpen)(LPCWSTR pwszUserAgent,DWORD dwAccessType,LPCWSTR pwszProxyName,
                                                LPCWSTR pwszProxyBypass,DWORD dwFlags);
    PFN_WinHttpOpen pfWinHttpOpen = (PFN_WinHttpOpen) GetProcAddress(hWinHTTP, szWinHttpOpen);
    if(!pfWinHttpOpen) {
      errorLog <<  ErrGetProcAddr << szWinHttpOpen << endl;
      goto cleanup;
    }

    const char *szWinHttpCloseHandle="WinHttpCloseHandle";

    typedef BOOL (WINAPI *PFN_WinHttpCloseHandle)(HINTERNET hInternet);

    PFN_WinHttpCloseHandle pfWinHttpCloseHandle = (PFN_WinHttpCloseHandle) GetProcAddress(hWinHTTP, szWinHttpCloseHandle);
    if(!pfWinHttpCloseHandle) {
      errorLog <<  ErrGetProcAddr << szWinHttpCloseHandle << endl;
      goto cleanup;
    }

    HINTERNET hHttpSession = NULL;
    hHttpSession = (*pfWinHttpOpen)( L"Toontown Loader",
                              WINHTTP_ACCESS_TYPE_NO_PROXY,
                              WINHTTP_NO_PROXY_NAME,
                              WINHTTP_NO_PROXY_BYPASS,0x0);
    if( !hHttpSession ) {
        errorLog <<  szWinHttpOpen << ErrRetStr << GetLastError() << endl;
        goto cleanup;
    }

    WINHTTP_AUTOPROXY_OPTIONS autoProxyOpts;
    ZeroMemory(&autoProxyOpts,sizeof(autoProxyOpts));
    autoProxyOpts.fAutoLogonIfChallenged = true;
    if(bAutoDetection) {
      autoProxyOpts.dwFlags = WINHTTP_AUTOPROXY_AUTO_DETECT;
      autoProxyOpts.dwAutoDetectFlags = WINHTTP_AUTO_DETECT_TYPE_DHCP | WINHTTP_AUTO_DETECT_TYPE_DNS_A;
      errorLog << "doing winhttp proxy script autodetect\n";
    } else {
      autoProxyOpts.dwFlags = WINHTTP_AUTOPROXY_CONFIG_URL;
      autoProxyOpts.lpszAutoConfigUrl=pAutoConfigUrl;
      errorLog << "using winhttp to process auto-proxy script\n";
    }

    WINHTTP_PROXY_INFO ProxyInfo;

    BOOL bRetVal = (*pfWinHttpGetProxyForUrl)(hHttpSession,L"http://www.toontown.com",
                                              &autoProxyOpts, &ProxyInfo);
    if(!bRetVal) {
       DWORD errval = GetLastError();
       errorLog <<  szWinHttpGetProxyForUrl << ErrRetStr;
       switch(errval) {
           case ERROR_WINHTTP_AUTODETECTION_FAILED:
              errorLog << "ERROR_WINHTTP_AUTODETECTION_FAILED";
              break;
           case ERROR_WINHTTP_BAD_AUTO_PROXY_SCRIPT:
              errorLog << "ERROR_WINHTTP_BAD_AUTO_PROXY_SCRIPT";
              break;
           case ERROR_WINHTTP_INCORRECT_HANDLE_TYPE:
              errorLog << "ERROR_WINHTTP_INCORRECT_HANDLE_TYPE";
              break;
           case ERROR_WINHTTP_INVALID_URL:
              errorLog << "ERROR_WINHTTP_INVALID_URL";
              break;
           case ERROR_WINHTTP_LOGIN_FAILURE:
              errorLog << "ERROR_WINHTTP_LOGIN_FAILURE";
              break;
           case ERROR_WINHTTP_UNABLE_TO_DOWNLOAD_SCRIPT:
              errorLog << "ERROR_WINHTTP_UNABLE_TO_DOWNLOAD_SCRIPT";
              break;
           case ERROR_WINHTTP_UNRECOGNIZED_SCHEME:
              errorLog << "ERROR_WINHTTP_UNRECOGNIZED_SCHEME";
              break;
           default:
             errorLog << errval;
       }
       errorLog << endl;
       goto cleanup;
    }

    if(ProxyInfo.lpszProxy==NULL) {
       errorLog << szWinHttpGetProxyForUrl <<" failed to return proxy str!\n";
       goto cleanup;
    }

    // need 2 convert stupid widechar str to regular one that toontown can read out of registry
    #define MAXNAMELEN 512
    DWORD proxynamelen = wcslen(ProxyInfo.lpszProxy);
    pProxyStr = new char[MAXNAMELEN];
    assert(proxynamelen+1 < MAXNAMELEN);
    wsprintf(pProxyStr,"%lS",ProxyInfo.lpszProxy);
    const char *httpStr="http://";
    GlobalFree(ProxyInfo.lpszProxy);
    if(_strnicmp(httpStr,pProxyStr,7)!=0) {
        //prepend 'http://' to pProxyStr
        char tmpbuf[MAXNAMELEN];
          strcpy(tmpbuf,httpStr);
          strcat(tmpbuf,pProxyStr);
          strcpy(pProxyStr,tmpbuf);
    }

    returnedProxyStr = pProxyStr;
    delete [] pProxyStr;

  cleanup:
    if(pAutoConfigUrl != NULL)
       GlobalFree(pAutoConfigUrl);
    if(hHttpSession != NULL)
       (*pfWinHttpCloseHandle)(hHttpSession);
    if(hWinHTTP != NULL)
        FreeLibrary(hWinHTTP);
    return returnedProxyStr;
}