#include <string>
#include <windows.h>
#include <wininet.h>
#include <urlmon.h>
#include "installerBase.h"
#include "sysinfo.h"

extern string get_proxyname_using_winhttp(bool bAutoDetection);

// if autoproxy scripts fail and autoproxy script URL contains 'disney', use this instead
#define DEFAULT_DISNEY_PROXY "http://web-proxy.disney.com:8080"

//#define GET_PROXY_FROM_REGISTRY

//ms lamos left this out of Aug02 platsdk
#ifndef PROXY_AUTO_DETECT_TYPE_DHCP
#define PROXY_AUTO_DETECT_TYPE_DHCP  1
#define PROXY_AUTO_DETECT_TYPE_DNS_A 2
#endif
/* now defined in wininet.h
typedef BOOL (WINAPI *pfnInternetInitializeAutoProxyDll)(DWORD dwVersion,LPSTR lpszDownloadedTempFile,
                                                         LPSTR lpszMime,void* lpAutoProxyCallbacks,
                                                         void* lpExtraData);
typedef BOOL (WINAPI *pfnInternetDeInitializeAutoProxyDll)(LPSTR lpszMime,DWORD dwReserved);
typedef BOOL (WINAPI *pfnInternetGetProxyInfo)(LPCSTR lpszUrl,DWORD dwUrlLength, LPSTR lpszUrlHostName,
                                               DWORD dwUrlHostNameLength,LPSTR* lplpszProxyHostName,
                                               LPDWORD lpdwProxyHostNameLength);
*/                                             
string installerBase::
get_proxyname_using_jsproxy(const char *pAutoProxyScriptURL)
{
   string proxyStr;
   const char *pJSProxyName = "jsproxy.dll";
   bool JSProxyInitialized = false;
   char *proxyStrBuf=NULL;
   DWORD dwProxyStrBufLen=0;

   HMODULE hJSProxy = LoadLibrary(pJSProxyName);
   if (hJSProxy == NULL) {
       errorLog << "LoadLib failed for " << pJSProxyName << endl;
       goto cleanup;
   }

   pfnInternetInitializeAutoProxyDll pInternetInitializeAutoProxyDll = (pfnInternetInitializeAutoProxyDll)GetProcAddress(hJSProxy,"InternetInitializeAutoProxyDll");
   pfnInternetDeInitializeAutoProxyDll pInternetDeInitializeAutoProxyDll =(pfnInternetDeInitializeAutoProxyDll)GetProcAddress(hJSProxy,"InternetDeInitializeAutoProxyDll");
   pfnInternetGetProxyInfo pInternetGetProxyInfo = (pfnInternetGetProxyInfo)GetProcAddress(hJSProxy, "InternetGetProxyInfo");

   if (!pInternetInitializeAutoProxyDll || !pInternetDeInitializeAutoProxyDll || !pInternetGetProxyInfo) {
        errorLog << "Error: GetProcAddr failed for jsproxy fns!\n";
        goto cleanup;
   }

   char TempPath[MAX_PATH];
   char TempScriptFile[MAX_PATH];

   MyGetTempPath( sizeof(TempPath)/sizeof(TempPath[0]), TempPath );
   GetTempFileName( TempPath, NULL, 0, TempScriptFile );

   /* if I use URLDownloadToFile here, it causes URLOpenBlockingStream() to fail with E_NOINTERFACE
      later in the launcherFileDb downloadToMem, so try to work around it
   HRESULT hr = URLDownloadToFile( NULL, pAutoProxyScriptURL, TempScriptFile, NULL, NULL );
   if(FAILED(hr)) {
        errorLog << "URLDownloadToFile failed in get_proxy_jsproxy, hr=" << (void*)hr << endl;
        goto cleanup;
   }
   */

   if(!downloadToFile(pAutoProxyScriptURL,TempScriptFile)) {
       errorLog << "downloadToFile of autoproxyscript url failed!\n";
       goto cleanup;
   }

   if(!(*pInternetInitializeAutoProxyDll)( 0, TempScriptFile, NULL, NULL, NULL )) {
       errorLog << "InternetInitializeAutoProxyDll failed, err=" << GetLastError() << endl;
       goto cleanup;
   }

   JSProxyInitialized = true;

   DeleteFile(TempScriptFile);

   // InternetGetProxyInfo calls the jscript fn FindProxyForURL(url, host) in the script, which looks something like this:
   /*
         function FindProxyForURL(url, host)  {
         if ((isPlainHostName(host))  ||
             (dnsDomainIs(host, ".disney.com") &&
             !localHostOrDomainIs(host, "store.disney.com") &&
             !localHostOrDomainIs(host, "www.disney.com") &&
             !localHostOrDomainIs(host, "www.disney.com.cn") &&
             !localHostOrDomainIs(host, "www.disney.com.hk")))
             return "DIRECT";
         else
             return "PROXY web-proxy.wdi.disney.com:8080";

        the spec for this is at:
             http://wp.netscape.com/eng/mozilla/2.0/relnotes/demo/proxy-live.html
             http://developer.netscape.com/docs/manuals/proxy/adminux/autoconf.htm
    url: the full URL being accessed.
    host: the hostname extracted from the URL. This is only for convenience, it is the exact same string as between :// and the first : or / after that. The port number is not included in this parameter. It can be extracted from the URL when necessary.

    */

   // in this case, just find what proxy we need to get to the TT homepage url
   const char *szURLtoTest="http://www.toontown.com";
   DWORD URLlen=strlen(szURLtoTest);

   if(!(*pInternetGetProxyInfo)((LPSTR)szURLtoTest,URLlen,
                                (LPSTR)szURLtoTest,URLlen,
                                &proxyStrBuf,&dwProxyStrBufLen)) {
       errorLog << "InternetGetProxyInfo failed, err=" << GetLastError() << endl;
       goto cleanup;
   }

   if((proxyStrBuf==NULL)||(*proxyStrBuf=='\0')) {
       errorLog << "InternetGetProxyInfo returned empty proxy string, failing!\n";
       goto cleanup;
   }

   errorLog << "InternetGetProxyInfo returns '" << proxyStrBuf << "'\n";

   // string we get back is like this: 'PROXY web-proxy.wdi.disney.com:8080'.
   // want to reformat it like this 'http://web-proxy.wdi.disney.com:8080'.

   if(_strnicmp("PROXY ",proxyStrBuf,6)==0) {
       proxyStr = "http://";
       proxyStr.append(proxyStrBuf+6);
   }

  cleanup:
      if(proxyStrBuf!=NULL) {
          // BUGBUG:
          // is it possible we are not supposed to free this memory?
          // docs say absolutely nothing on this.  could freeing be causing jsproxy/wininet crashes?

          // GlobalFree(proxyStrBuf);
      }

      // could DeInit be causing jsproxy/wininet crashes?
#if 0
      if(JSProxyInitialized)
         (*pInternetDeInitializeAutoProxyDll)(NULL,0);
#endif

      if(hJSProxy!=NULL)
          FreeLibrary(hJSProxy);
      return proxyStr;
}

// This function fills in _proxy_spec and _direct_hosts.
void installerBase::
determine_proxy_spec() {
  _proxy_spec = string();
  _direct_hosts = string();

#ifdef GET_PROXY_FROM_REGISTRY

  errorLog << "getting proxy settings from registry" << endl;

  HKEY keyInternetSettings;
  if (keyInternetSettings = regOpenKey_ReadOnly(HKEY_CURRENT_USER, InternetSettingsRegKey)) {
        DWORD proxyEnable = 0;
        // find out if there is a proxy server in use
        if (!regGetDWORD(keyInternetSettings, "ProxyEnable", proxyEnable)) {
          if (proxyEnable) {
            // get the proxy name
            char proxy[_MAX_PATH];
            if (!regGetString(keyInternetSettings, "ProxyServer", proxy, sizeof(proxy))) {
              errorLog << "Connected through a proxy: '" << proxy << "'\n";
              _proxy_spec = proxy;
            } else {
              errorLog << "failed to get proxy name string from registry\n";
            }
          } else {
            errorLog << "Connected directly, not through a proxy\n";
          }
        } else {
          errorLog << "ProxyEnable reg value not found, assuming no proxy\n";
        }
        RegCloseKey(keyInternetSettings);
  }

#else

  // the good new IE5 way, plus autoproxy support

  INTERNET_VERSION_INFO structVI;
  DWORD dwStructSize = sizeof(INTERNET_VERSION_INFO);
  InternetQueryOption (NULL, INTERNET_OPTION_VERSION,
                    (LPVOID)&structVI, &dwStructSize);

  bool bIsatleastIE5 = (((structVI.dwMajorVersion==1) && (structVI.dwMinorVersion>=2))
                        || (structVI.dwMajorVersion>1));

  // per-connection proxy interface only exists on IE5+
  if(!bIsatleastIE5) {
      char* buffer;
      DWORD length=0;

      InternetQueryOption(NULL, INTERNET_OPTION_PROXY, NULL, &length);
      buffer = new char[length];

      if (!InternetQueryOption(NULL, INTERNET_OPTION_PROXY,
                               buffer, &length)) {
        errorLog << "Error calling InternetOptionQuery to get proxy information" << endl;
        // not worth linking to another library just for WSAGetLastError
        //errorLog << "WSAGetLastError returned error code " << WSAGetLastError() << endl;
      } else {
        INTERNET_PROXY_INFO* proxyInfo;
        proxyInfo = (INTERNET_PROXY_INFO*)buffer;

        if (proxyInfo->dwAccessType == INTERNET_OPEN_TYPE_DIRECT) {
          errorLog << "Connected directly, not through a proxy" << endl;
        } else {
            errorLog << "Connected through a proxy: '" << proxyInfo->lpszProxy << "'" << endl;
            _proxy_spec = proxyInfo->lpszProxy;
        }
      }

      delete [] buffer;
  } else {

        // have to handle 3 cases:   explicit proxy specified, explicit auto-proxy script, and auto-proxy detect
        bool bUsingAutoProxyScript=false;
        bool bFoundProxy = false;
        //LPWSTR pAutoConfigUrl = NULL;

        INTERNET_PER_CONN_OPTION_LIST    List;
        INTERNET_PER_CONN_OPTION         Option[5];
        unsigned long                    nSize = sizeof(INTERNET_PER_CONN_OPTION_LIST);
        Option[0].dwOption = INTERNET_PER_CONN_AUTOCONFIG_URL;
        Option[1].dwOption = INTERNET_PER_CONN_AUTODISCOVERY_FLAGS;
        Option[2].dwOption = INTERNET_PER_CONN_FLAGS;
        Option[3].dwOption = INTERNET_PER_CONN_PROXY_BYPASS;
        Option[4].dwOption = INTERNET_PER_CONN_PROXY_SERVER;
        List.dwSize = sizeof(INTERNET_PER_CONN_OPTION_LIST);
        List.pszConnection = NULL;
        List.dwOptionCount = 5;
        List.dwOptionError = 0;
        List.pOptions = Option;
        if(!InternetQueryOption(NULL, INTERNET_OPTION_PER_CONNECTION_OPTION, &List, &nSize)) {
            char *errstr="InternetQueryOption failed!";
            errorLog << errstr << endl;
            ShowOSErrorMessageBox(errstr);
            return;
        }

        char *pAutoProxyScriptURL = Option[0].Value.pszValue;
        DWORD autoDiscFlags=Option[1].Value.dwValue;
        DWORD connFlags = Option[2].Value.dwValue;

        SysInfo::OSType os_type = SysInfo::get_os_type();

        bool bUsingExplicitAutoProxyScript = ((pAutoProxyScriptURL != NULL) &&
                                              (connFlags & PROXY_TYPE_AUTO_PROXY_URL));
        if(bUsingExplicitAutoProxyScript) {
            _AutoProxyScriptURL = pAutoProxyScriptURL;
        }

        #if 0
          // for auto-detect, we dont yet have an explicit script!

        if(os_type >= SysInfo::OS_WinNT) {
          // on win9x, seems like autoDiscFlags is always 0x0 even when auto-proxy script
          // is checked, so only do this on NT
          bUsingExplicitAutoProxyScript = (bUsingExplicitAutoProxyScript &&
                                           (autoDiscFlags & AUTO_PROXY_FLAG_USER_SET));
        }
        #endif

       // errorLog <<  "XXX  81 " << (pAutoProxyScriptURL != NULL)  << endl;
       // errorLog <<  "XXX  82 0x" << (void*)autoDiscFlags << endl;
       // errorLog <<  "XXX  83 0x" << (void*)connFlags  << endl;

        if(bUsingExplicitAutoProxyScript) {
           errorLog <<  "Using AutoProxy script: " << pAutoProxyScriptURL << endl;
           bUsingAutoProxyScript=true;
        }
/*
        if(autoDiscFlags!=0x0) {
            errorLog <<  "INTERNET_PER_CONN_AUTODISCOVERY_FLAGS: ";
            if(autoDiscFlags & AUTO_PROXY_FLAG_ALWAYS_DETECT)
                errorLog <<  "AUTO_PROXY_FLAG_ALWAYS_DETECT | ";
            if(autoDiscFlags & AUTO_PROXY_FLAG_CACHE_INIT_RUN)
                errorLog <<  "AUTO_PROXY_FLAG_CACHE_INIT_RUN | ";
            if(autoDiscFlags & AUTO_PROXY_FLAG_DONT_CACHE_PROXY_RESULT)
                errorLog <<  "AUTO_PROXY_FLAG_DONT_CACHE_PROXY_RESULT | ";
            if(autoDiscFlags & AUTO_PROXY_FLAG_MIGRATED)
                errorLog <<  "AUTO_PROXY_FLAG_MIGRATED | ";
            if(autoDiscFlags & AUTO_PROXY_FLAG_USER_SET)
                errorLog <<  "AUTO_PROXY_FLAG_USER_SET";
            errorLog << endl;
        }
*/
        bool bAutoDetect = ((Option[2].Value.dwValue & PROXY_TYPE_AUTO_DETECT)!=0);

        // BUGBUG: disabling autodetect handling for now, until final jsproxy stuff is ready
        bAutoDetect = false;

        if(bAutoDetect) {
            if(!bUsingExplicitAutoProxyScript) {
                errorLog <<  "enabling proxy auto-detection\n";
                // code to get Auto-Proxy script url using auto-detect goes here
                bUsingAutoProxyScript=true;
            } else {
                errorLog <<  "explicit auto-proxy script setting overrides auto-detect specification\n";
                bAutoDetect = false;
            }
        }

        /* this seems to always be set so it's useless
        if(Option[2].Value.dwValue & PROXY_TYPE_DIRECT)
            errorLog <<  "PROXY_TYPE_DIRECT set\n";
         */

        if((Option[3].Value.pszValue != NULL) && (Option[3].Value.pszValue[0] != '\0')) {
           errorLog <<  "INTERNET_PER_CONN_PROXY_BYPASS: " << Option[3].Value.pszValue << endl;
           _direct_hosts = Option[3].Value.pszValue;
        }

        bool bUsingExplicitProxy = ((Option[2].Value.dwValue & PROXY_TYPE_PROXY)!=0);

        // (Option[4].Value.pszValue may contain a real string, but shouldnt use it
        // unless PROXY_TYPE_PROXY was set
        if(bUsingExplicitProxy && (Option[4].Value.pszValue != NULL)) {
           char *pProxyNameStr = Option[4].Value.pszValue;
           _proxy_spec = pProxyNameStr;
           errorLog <<  "using explicit http proxy setting: " << _proxy_spec << endl;
           bFoundProxy = true;

           if(bUsingAutoProxyScript) {
               errorLog <<  "Unexpected Condition: both PROXY_SERVER and AutoProxy are specified, ignoring AutoProxy!\n";
               bUsingAutoProxyScript= false;
           }
        }

        if(bUsingAutoProxyScript) {
            // cant parse auto-proxy on win9x (without hosting the script ourselves)
            // until MS makes InternetGetProxyInfo() work in wininet.dll
#if 1
            if(os_type >= SysInfo::OS_Win2000) {
                _proxy_spec = get_proxyname_using_winhttp(bAutoDetect);
                if(!_proxy_spec.empty()) {
                    errorLog <<  "winhttp resolved auto-proxy script to proxy: " << _proxy_spec << endl;
                    bFoundProxy = true;
                    goto cleanup;
                }
            }
#endif

            // disabled jsproxy stuff until we figure out why it causes faults in wininet/urlmon calls
            // (shouldnt call jsproxy unint fn?)

#if 0

            // winhttp method failed, now try IE5 jsproxy way
            _proxy_spec = get_proxyname_using_jsproxy(pAutoProxyScriptURL);
            if(!_proxy_spec.empty()) {
                errorLog <<  "jsproxy resolved auto-proxy script to proxy: " << _proxy_spec << endl;
                bFoundProxy = true;
                goto cleanup;
            }
#endif

            // special disney corp detection hack, useful for win9x machines and win2k/XP machines
            // without the latest service pack.

            if(pAutoProxyScriptURL != NULL) {
                string autoproxstr(pAutoProxyScriptURL);
                if(autoproxstr.find("disney.com")!=string::npos) {
                    errorLog <<  "detected disney autoproxy\n";
                    _proxy_spec = DEFAULT_DISNEY_PROXY;
                    bFoundProxy = true;
                    goto cleanup;
                }

                if(os_type <= SysInfo::OS_WinMe) {
                    // to get jsproxy stuff working probably have to move it to separate process
                    // (configrc.exe) to avoid IE crashes
                    errorLog <<  "Error: installer cant process auto-proxy scripts on win9x yet!\n";
                } else {
                    errorLog <<  "Error: installer failed to process auto-proxy script\n";
                }
            }

            const char *errmsg ="Toontown can't process your http auto-proxy script, please set an explicit http proxy server in your IE settings";
            char msgbuf[512];

            strcpy(msgbuf,errmsg);
            // otherwise we cant handle the auto-proxy with this OS config
            // the errmsgs probably belong on a webpage instead, since
            // this just continues blindly and fails to connect

            if(os_type >= SysInfo::OS_Win2000) {
                sprintf(msgbuf,"%s or install the latest Windows %s Service Pack from http://windowsupdate.microsoft.com",
                        errmsg,((os_type == SysInfo::OS_Win2000) ? "2000" : "XP"));
            } else {
                sprintf(msgbuf,"%s.",errmsg);
            }
            MessageBox( NULL, (LPCTSTR)msgbuf, "Toontown Installer Error", MB_OK | MB_ICONWARNING );
        }

     cleanup:
        if(Option[0].Value.pszValue != NULL)
           GlobalFree(Option[0].Value.pszValue);
        if(Option[3].Value.pszValue != NULL)
           GlobalFree(Option[3].Value.pszValue);
        if(Option[4].Value.pszValue != NULL)
           GlobalFree(Option[4].Value.pszValue);
       // if(pAutoConfigUrl != NULL)
       //    GlobalFree(pAutoConfigUrl);
        if(!bFoundProxy) {
            errorLog <<  "found no http proxy, assuming direct connection\n";
        }
  }
#endif
}

