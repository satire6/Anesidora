// Filename: sysinfo.cxx
// Created by:  darren (09Jan97)
// $Id$
//
////////////////////////////////////////////////////////////////////
//
// Toontown SOFTWARE
// Copyright (c) 2001 - 2007, Disney Enterprises, Inc.  All rights reserved
//
////////////////////////////////////////////////////////////////////

// disable vc warnings
#include "pragma.h"

#include "sysinfo.h"
#include <dsound.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <wininet.h>
#include <malloc.h>
#include <time.h>
#include <tlhelp32.h>
#include <Iphlpapi.h>
#include <mmreg.h>
#include <mmsystem.h>
#include <ddraw.h>
#include <assert.h>
#include "cpudetect.h"
#include "log.h"


using namespace std;

extern void ShowErrorBox(const char *msg);

//#define ERROR_STRING_TABLE

#ifdef ERROR_STRING_TABLE
static string ConvHRErrorToString(const HRESULT &error);
#endif

#define USING_MILES_SOUND

// just want to get this once, and need it before SysInfo construction so static method can save info
SysInfo::OSType g_OSType=SysInfo::OS_unknown;
string g_OSTypeStr;  // errorLog not created yet
float  g_OSServicePackVer;

#if 0
const char *_graphics_card_type_names[SysInfo::GfxCardType::NumCardTypes];
#endif

////////////////////////////////////////////////////////////////////
// Defines
////////////////////////////////////////////////////////////////////
#define BUFSIZE 80

////////////////////////////////////////////////////////////////////
// static functions
SysInfo::GNSI SysInfo::getSystemInfoProc()
{
	GNSI pGNSI = (GNSI) GetProcAddress( GetModuleHandle(TEXT("kernel32.dll")), "GetNativeSystemInfo" );
	if (pGNSI == NULL)
		return GetSystemInfo;
	return pGNSI;
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
SysInfo::
SysInfo(void) {
  _gfx_report_str.flags(ios::fixed);
  _gfx_report_str.precision(2);
  _hPsAPI = NULL;
  _pGetProcessMemoryInfo = NULL;
  _pGetPerfInfo = NULL;
  _pGetSystemInfo = getSystemInfoProc();
  _bValidVideoDeviceID = false;
  _bDoneVidMemCheck = false;
  memset(&_VideoDeviceID,0,sizeof(_VideoDeviceID));

	g_OSType = SysInfo::OS_unknown;		// clean this environment
	g_OSTypeStr = "";

  _CPUMhz = 0;
  _NumCPUs = 1;
  _gfx_api_suggested = GAPI_Unknown;
  // _gfx_api_used = GAPI_Unknown;
  _VideoRamTotalBytes = 0;
  _VideoCardDriverDateMon = 0;
  _VideoCardDriverDateDay = 0;
  _VideoCardDriverDateYear = 0;
  _VideoCardVendorID = 0;
  _VideoCardDeviceID = 0;
  _VideoCardSubsysID = 0;
  _VideoCardRevisionID = 0;
  _numMonitors = 1;
  _IEVersionNum = 0.0f;
  _dx_level_installed = GAPI_Unknown;

  _ram_megs_total = 99999.0f;  // if check_ram fails, let people through
  _ram_megs_available = 99999.0f;

  _bNetworkIsLAN = false;
#ifdef USE_DX7
	_DX7_status = Status_Unknown;
#endif
  _DX8_status =_OpenGL_status = Status_Unknown;
#ifdef USE_DX9
	_DX9_status = Status_Unknown;
#endif

  #if 0
  // dont care about other types yet...
  _graphics_card_type = GfxCardType::Unknown;
  _graphics_card_type_names[GfxCardType::Unknown] = "Unknown";
  _graphics_card_type_names[GfxCardType::Intel_i810] = "i810";
  #endif

  time(&_startup_time);

  _bHas_custom_mousecursor_ability = true;

  errorLog.flags(ios::fixed);
  errorLog.precision(2);

  errorLog << "CHECKING CPU..." << endl;
  check_cpu();
  errorLog << "CHECKING OS..." << endl;
  check_os();
  check_mouse();
#if 0
// georges:  what's this for?? it checks scrnsize, not color depth!
//           probably dont have to worry about 8bpp scrn mode, since
//           fullscrn switches to the right mode if its available
//           may need this for users who try to do windowed 3D at unsupported desktop bitdepths

  errorLog << "CHECKING COLOR DEPTH..." << endl;
  check_colordepth();
#endif
  errorLog << "CHECKING RAM..." << endl;
  check_ram();
  errorLog << "CHECKING 3D HARDWARE..." << endl;
  check_3d_hw();
  errorLog << "CHECKING SOUND..." << endl;
  check_snd();
  check_language_info();
  errorLog << "CHECKING NET CONNECTION..." << endl;
  check_net_connection();
}

SysInfo::~SysInfo(void) {
   SAFE_FREELIB(_hPsAPI);
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::write_log_file
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
bool SysInfo::
write_log_file(const char *logfilename) {
  ofstream write_stream;
  write_stream.open(logfilename, ios::out);
  if (write_stream.fail()) {
    errorLog << "SysInfo::write_log_file() - Failed to open: " << logfilename
        << endl;
    return FALSE;
  }
  write_stream << "Operating System: " << _os_type << endl;
  write_stream << "RAM: Total: " << _ram_megs_total << " MB, Available: " << _ram_megs_available << " MB" << endl;
  write_stream << "Gfx API Suggested: " << _gfx_api_suggested << endl;
//  write_stream << "CPU: Type: " << cpu_type << " Level: " << cpu_level << " Number: " << cpu_num << endl;
  write_stream << "Mouse: Enabled: " << _mouse_enabled << " Buttons: " << _mouse_buttons << endl;
  if(!_bNetworkIsLAN) {
      write_stream << "Connection Type: " << _comm_type << " Max Baud: " << _comm_baud << endl;
  } else {
      write_stream << "Connection Type: LAN\n";
  }

  write_stream.close();
  return TRUE;
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::get_available_space
//       Access: Public
//  Description:
//    returns true on success; free_bytes == # of free bytes
//    returns false on error; free_bytes undefined
////////////////////////////////////////////////////////////////////
bool SysInfo::
get_available_space(const char *dirname, unsigned __int64 &free_bytes) {
  unsigned __int64 total_bytes;
  bool result;
  // Use GetDiskFreeSpaceEx() if it is available (win95 OSR2+)
  HINSTANCE k32 = LoadLibrary("kernel32.dll");
  if(k32) {
    typedef BOOL (WINAPI *GETDISKFREESPACEEX)(LPCTSTR lpDirectoryName,PULARGE_INTEGER lpFreeBytesAvailable,PULARGE_INTEGER lpTotalNumberOfBytes,PULARGE_INTEGER lpTotalNumberOfFreeBytes);
    GETDISKFREESPACEEX pGetDiskFreeSpcEx = (GETDISKFREESPACEEX) GetProcAddress(k32, "GetDiskFreeSpaceExA");

    if (pGetDiskFreeSpcEx!=NULL) {
      if ((*pGetDiskFreeSpcEx)(dirname, (PULARGE_INTEGER)&free_bytes,
                   (PULARGE_INTEGER)&total_bytes, NULL)) {
    result = true;
      } else {
        errorLog << "SysInfo:: GetDiskFreeSpaceEx() failed\n";
        result = false;
      }
    }
    FreeLibrary(k32);
  }
  else
  {
	// We'll have to use GetDiskFreeSpace()
	// (should only happen on win95 gold, which we probably barely support if at all. (should support it enough to say no you can run nicely, at least))
	DWORD s_per_c, b_per_s, c_free, c_total;
	if (GetDiskFreeSpace(dirname, &s_per_c, &b_per_s, &c_free, &c_total))
	{
		free_bytes = ((unsigned __int64)c_free)
			* ((unsigned __int64)s_per_c) * ((unsigned __int64)b_per_s);
		result = true;
	}
	else
	{
		errorLog << "SysInfo:: GetDiskFreeSpace() failed" << endl;
		result = false;
	}
  }
  return result;
}

// fTestInterval is in seconds
DWORD FindCPUMhz(float fTestInterval)
{
    volatile DWORD Freq, EAX_tmp, EDX_tmp;
    static DWORD savedCPUMhz=0;

    // this isnt threadsafe but who cares, it wont crash anything
    if(savedCPUMhz>0) {
        return savedCPUMhz;
    }

     int mSecs=(int)(fTestInterval*1000);
     if(mSecs<1)
       return 0;

     volatile DWORD uSecs=mSecs*1000;

     // SetThreadPriority could be temporarily used to ensure we're not swapped out
     // seems to work ok without it for now, with a slight underestimate.  Is there an
     // exact way to do this a la dxdiag.exe?

     // reads timer, sleeps for short interval, and reads timer again, divides to get mhz
    __asm {
         RDTSC
         mov  EAX_tmp, eax
         mov  EDX_tmp, edx
     }

     Sleep(mSecs);

     __asm {
         RDTSC
         mov  ecx, uSecs
         sub  eax, EAX_tmp
         sbb  edx, EDX_tmp
         div  ecx
         mov  Freq, eax        // Freq gets the frequency in MHz
     }

      savedCPUMhz = Freq;
      return Freq;
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_cpu
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
void SysInfo::
check_cpu(void) {
  SYSTEM_INFO sinfo;
  _pGetSystemInfo(&sinfo);

  _CPUMhz = FindCPUMhz(0.1f);  // tenth of a sec seems sufficient to get good reading

  if((_CPUMhz>100)||(_CPUMhz<10000)) {
      errorLog << "CPU speed: " << _CPUMhz << " Mhz\n";
  } else {
      // we dont care about stuff slower than 100 anyway, and 10 Ghz is still a few years away
      errorLog << "CPU speed: (unreliable measurement) " << _CPUMhz << endl;
  }

#if 0
    // it's all pretty much x86 now
  errorLog << "CPU type: ";
  switch (sinfo.wProcessorArchitecture) {
    case PROCESSOR_ARCHITECTURE_INTEL:
      cpu_type = CPU_X86;
      errorLog << "X86";
      break;
    case PROCESSOR_ARCHITECTURE_MIPS:
      cpu_type = CPU_MIPS;
      errorLog << "MIPS";
      break;
    case PROCESSOR_ARCHITECTURE_ALPHA:
      cpu_type = CPU_Alpha;
      errorLog << "Alpha";
      break;
    case PROCESSOR_ARCHITECTURE_PPC:
      cpu_type = CPU_PPC;
      errorLog << "PPC";
      break;
    case PROCESSOR_ARCHITECTURE_UNKNOWN:
    default:
      cpu_type = CPU_unknown;
      errorLog << "unknown";
      break;
  }
  errorLog << endl;
#endif

  _NumCPUs = sinfo.dwNumberOfProcessors;

  if(_NumCPUs>1)
      errorLog << "NumProcessors: " << _NumCPUs << endl;
  // print out the info from the AMD code
  //errorLog << "AMD CPU detection code results:" << endl;
  if(!GetCPUCaps(HAS_CPUID)) {
    errorLog << "CPUID not supported" << endl;
  }
  else
  {
    // VENDOR
    errorLog << "CPU vendor code: ";
    switch(GetCPUCaps(CPU_VENDOR)) {
      case VENDOR_AMD:
        errorLog << "AMD";
        break;
      case VENDOR_INTEL:
        errorLog << "Intel";
        break;
      case VENDOR_CYRIX:
        errorLog << "Cyrix";
        break;
      case VENDOR_CENTAUR:
        errorLog << "Centaur";
        break;
      case VENDOR_UNKNOWN:
        errorLog << "unknown";
        break;
      default:
        errorLog << "error";
        break;
    }
    errorLog << endl;

    // VENDOR STRING

    char msgbuf[50];
    char *pNameStart=msgbuf;
    memset(msgbuf,0,50);
    DWORD *str = (DWORD*)GetCPUCaps(CPU_VENDOR_STRING);
    memcpy(msgbuf, (void*)str,20);
    while(isspace(*pNameStart) && (*pNameStart!='\0'))
      pNameStart++;
    _CPUMakerStr = pNameStart;
    errorLog << "CPU vendor name: " << _CPUMakerStr << endl;

    // NAME STRING
    ZeroMemory(msgbuf,50);
    str = (DWORD*)GetCPUCaps(CPU_NAME_STRING);
    memcpy(msgbuf, (void*)str, 48);
    pNameStart=msgbuf;
    while(isspace(*pNameStart) && (*pNameStart!='\0'))
      pNameStart++;
    _CPUNameStr = pNameStart;
    errorLog << "CPU name: " << _CPUNameStr << endl;

    // TYPE
    switch(GetCPUCaps(CPU_TYPE)) {
      case AMD_Am486:
        _CPUTypeStr = "AMD Am486";
        break;
      case AMD_K5:
        _CPUTypeStr =  "AMD K5";
        break;
      case AMD_K6:
        _CPUTypeStr =  "AMD K6";
        break;
      case AMD_K6_2:
        _CPUTypeStr =  "AMD K6 2";
        break;
      case AMD_K6_3:
        _CPUTypeStr =  "AMD K6 3";
        break;
      case AMD_ATHLON:
        _CPUTypeStr =  "AMD Athlon";
        break;
      case INTEL_486DX:
        _CPUTypeStr =  "Intel 486DX";
        break;
      case INTEL_486SX:
        _CPUTypeStr =  "Intel 486SX";
        break;
      case INTEL_486DX2:
        _CPUTypeStr =  "Intel 486DX2";
        break;
      case INTEL_486SL:
        _CPUTypeStr =  "Intel 486SL";
        break;
      case INTEL_486SX2:
        _CPUTypeStr =  "Intel 486SX2";
        break;
      case INTEL_486DX2E:
        _CPUTypeStr =  "Intel 486DX2E";
        break;
      case INTEL_486DX4:
        _CPUTypeStr =  "Intel 486DX4";
        break;
      case INTEL_Pentium:
        _CPUTypeStr =  "Intel Pentium";
        break;
      case INTEL_Pentium_MMX:
        _CPUTypeStr =  "Intel Pentium MMX";
        break;
      case INTEL_Pentium_Pro:
        _CPUTypeStr =  "Intel Pentium Pro";
        break;
      case INTEL_Pentium_II:
        _CPUTypeStr =  "Intel Pentium 2";
        break;
      case INTEL_Celeron:
        _CPUTypeStr =  "Intel Celeron";
        break;
      case INTEL_Pentium_III:
        _CPUTypeStr =  "Intel Pentium 3";
        break;
      case INTEL_Pentium_4:
        _CPUTypeStr =  "Intel Pentium 4";
        break;
      case UNKNOWN:
        _CPUTypeStr =  "unknown";
        break;
      default:
        _CPUTypeStr =  "error";
        break;
    }
    errorLog << "CPU type: " << _CPUTypeStr << endl;
    errorLog << "CPU level: " << sinfo.wProcessorLevel << endl;


    // features
    errorLog << "CPU features: ";
    if(GetCPUCaps(HAS_MMX))       errorLog << "MMX, ";
    if(GetCPUCaps(HAS_MMX_EXT))   errorLog << "MMX Extensions, ";
    if(GetCPUCaps(HAS_3DNOW))     errorLog << "3DNow!, ";
    if(GetCPUCaps(HAS_3DNOW_EXT)) errorLog << "Extended 3DNow!, ";
    if(GetCPUCaps(HAS_SSE))       errorLog << "SSE, ";
    if(GetCPUCaps(HAS_SSE_MMX))   errorLog << "SSE MMX, ";
    if(GetCPUCaps(HAS_SSE_FP))    errorLog << "SSE FP, ";
    if(GetCPUCaps(HAS_SSE2))      errorLog << "SSE2, ";
    errorLog << endl;
  }
}

bool SysInfo::
IsNTAdmin(void) {
    HANDLE                   hAccessToken;
    BYTE                     *InfoBuffer;
    PTOKEN_GROUPS            ptgGroups;
    DWORD                    dwInfoBufferSize;
    PSID                     psidAdministrators;
    SID_IDENTIFIER_AUTHORITY siaNtAuthority = {SECURITY_NT_AUTHORITY};
    UINT                     i;
    static int               s_IsNtAdmin = -1;

    // save result for quick future calls.
    if(s_IsNtAdmin >= 0) {
        return (s_IsNtAdmin>0);
    }

    s_IsNtAdmin = false;

    if(!OpenProcessToken(GetCurrentProcess(),TOKEN_QUERY,&hAccessToken))
        goto cleanup;

    InfoBuffer = new BYTE[1024];
    if(!InfoBuffer)
        goto cleanup;

    BOOL bSuccess = GetTokenInformation(hAccessToken,
                                        TokenGroups,
                                        InfoBuffer,
                                        1024,
                                        &dwInfoBufferSize);
    CloseHandle(hAccessToken);

    if(!bSuccess)
        goto cleanup;

    if(!AllocateAndInitializeSid(&siaNtAuthority,
                                 2,
                                 SECURITY_BUILTIN_DOMAIN_RID,
                                 DOMAIN_ALIAS_RID_ADMINS,
                                 0,0,0,0,0,0,
                                 &psidAdministrators))
        goto cleanup;

    ptgGroups = (PTOKEN_GROUPS)InfoBuffer;

    for(i=0;i<ptgGroups->GroupCount;i++) {
        if(EqualSid(psidAdministrators,ptgGroups->Groups[i].Sid)) {
            s_IsNtAdmin = true;
            break;
        }
    }

    FreeSid(psidAdministrators);

    cleanup:
    if(InfoBuffer)
        delete [] InfoBuffer;

    return (s_IsNtAdmin>0);
}

#if 0
const char *SysInfo::
GetGraphicsCardCanonicalName(void) {
  return _graphics_card_type_names[_graphics_card_type];
}
#endif

string SysInfo::
get_gfx_api_name(GAPIType gapi) const {
   switch(gapi) {
       case GAPI_OpenGL:
          return "OpenGL";
       case GAPI_DirectX_9_0:
          return "DX 9.0";
       case GAPI_DirectX_8_1:
          return "DX 8.1";
       case GAPI_DirectX_8_0:
          return "DX 8.0";
       case GAPI_DirectX_7:
          return "DX 7";
       case GAPI_DirectX_6:
          return "DX 6";
       case GAPI_DirectX_5:
          return "DX 5";
       case GAPI_DirectX_3:
          return "DX 3";
   }

   return "Unknown";
}

string SysInfo::
get_os_namestr(void) {
  return g_OSTypeStr;
}

void SysInfo::
print_os_info(void) {
  OSType OS__type = get_os_type();
  errorLog << g_OSTypeStr << endl;

  if(OS__type>=OS_WinNT) {
      if(IsNTAdmin())
          errorLog << "User has NT Admin privileges\n";
       else errorLog << "User DOES NOT have NT Admin privileges\n";
  }
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_os
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
void SysInfo::
check_os(void) {
  _os_type = get_os_type();
  print_os_info();

  // Get IE version too
  // should I use InternetQueryOption instead, or is that less accurate?

  const char *IERegKeyName = "SOFTWARE\\Microsoft\\Internet Explorer";  //under HKEY_LOCAL_MACHINE
  HKEY hIEKey=NULL;
  ULONG retVal = RegOpenKeyEx(HKEY_LOCAL_MACHINE, IERegKeyName,0,KEY_READ,&hIEKey);
  if ((ERROR_SUCCESS != retVal) || (hIEKey==NULL)) {
    errorLog << "regOpenKey RO failed, err=" << GetLastError() << endl;
    return;
  }

  char IEverstr[100];
  DWORD dwType,dwSize=100;
  if(ERROR_SUCCESS != RegQueryValueEx(hIEKey, "Version", 0, &dwType, (LPBYTE)IEverstr,&dwSize)) {
       return;
  }
  RegCloseKey(hIEKey);
  errorLog << "IE Ver: " << IEverstr << endl;
  _IEVersionStr = IEverstr;

  DWORD VerA,VerB,VerC,VerD;
  sscanf(IEverstr,"%d.%d.%d.%d",&VerA,&VerB,&VerC,&VerD);
  //make a float that represent the version, so we can do >/< searches
  // make 5.5.2800.1111 into 5.528
  _IEVersionNum = (VerA + (VerB * 1E-1) + (VerC*1E-5) + (VerD*1E-9));
}

float SysInfo::
get_os_servicepack_version(void) {
    return g_OSServicePackVer;
}

SysInfo::OSType SysInfo::
get_os_type(void)
{
    if (g_OSType != SysInfo::OS_unknown)
        return g_OSType;

    SysInfo::OSType OS_Type = OS_unknown;

    // code derives from
    // http://msdn.microsoft.com/library/default.asp?url=/library/en-us/sysinfo/base/getting_the_system_version.asp

	static const int OSSTRLEN = 100;
	static const int SM_SERVERR2 = 89;

    char OSstrarray[OSSTRLEN];
    memset(OSstrarray, 0, sizeof(OSstrarray));

    ostringstream OSString(OSstrarray, OSSTRLEN);

    // Try calling GetVersionEx using the OSVERSIONINFOEX structure.
    //
    // If that fails, try using the OSVERSIONINFO structure.
	OSVERSIONINFOEX osvi = { sizeof(OSVERSIONINFOEX) };

    BOOL bOsVersionInfoEx = GetVersionEx((OSVERSIONINFO *) &osvi);
    if (!bOsVersionInfoEx)
	{
		// If OSVERSIONINFOEX doesn't work, try OSVERSIONINFO.
		osvi.dwOSVersionInfoSize = sizeof (OSVERSIONINFO);
		if (! GetVersionEx((OSVERSIONINFO *) &osvi) )
			return OS_unknown;
    }

	SYSTEM_INFO si = { 0 };
	GNSI pGetSystemInfo = getSystemInfoProc();
	pGetSystemInfo(&si);

    switch(osvi.dwPlatformId)
    {
    // Test for the Windows NT product family.
    case VER_PLATFORM_WIN32_NT:

        // Test for the specific product.
        if (osvi.dwMajorVersion <= 4) {
            OSString << "Microsoft Windows NT ";
            OS_Type = OS_WinNT;
        }
        else if (osvi.dwMajorVersion == 5)
        {
            switch(osvi.dwMinorVersion)
            {
            case 0:
                OSString << "Microsoft Windows 2000 ";
                OS_Type = OS_Win2000;
                break;
            case 1:
                OSString << "Microsoft Windows XP ";
                OS_Type = OS_WinXP;
                break;
            case 2:
                if (GetSystemMetrics(SM_SERVERR2)) {
                    OSString << "Microsoft Windows Server 2003 \"R2\" ";
                    OS_Type = OS_WinServer2003R2;
                }
                else if (osvi.wProductType == VER_NT_WORKSTATION
                    && si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64)
                {
                    OSString << "Microsoft Windows XP Professional x64 Edition ";
                    OS_Type = OS_WinXP64;
                }
                else
                {
                    OSString << "Microsoft Windows Server 2003, ";
                    OS_Type = OS_WinServer2003;
                }
                break;
            default:
                OSString << "Unknown Windows XP class OS ";
                OS_Type = OS_WinPostXP;
            }
       }
       else if (osvi.dwMajorVersion == 6)
       {
            switch(osvi.dwMinorVersion)
            {
            case 0:
                OSString << "Windows Vista ";
                OS_Type = OS_WinVista;
                break;
            default:
                OSString << "Windows Server \"Longhorn\" ";
                OS_Type = OS_WinLonghorn;
            }
       }
       else {
           OSString << "Microsoft Windows NT OS (Newer than Windows Vista) ";
           OS_Type = OS_WinPostVista;
       }

       // Test for specific product on Windows NT 4.0 SP6 and later
       if (bOsVersionInfoEx)
       {
           // test for the workstation type
           if (osvi.wProductType == VER_NT_WORKSTATION
               && si.wProcessorArchitecture != PROCESSOR_ARCHITECTURE_AMD64)
           {
               if (osvi.dwMajorVersion == 4)
                   OSString << "Workstation 4.0 ";
               else if (osvi.wSuiteMask & VER_SUITE_PERSONAL)
                   OSString << "Home Edition ";
               else
                   OSString <<  "Professional ";
           }
           else if (osvi.wProductType == VER_NT_SERVER
                   || osvi.wProductType == VER_NT_DOMAIN_CONTROLLER)
           {
               if (osvi.dwMajorVersion == 5)
               {
                   if (osvi.wSuiteMask & VER_SUITE_DATACENTER)
                       OSString <<  "DataCenter ";
                   else if (osvi.wSuiteMask & VER_SUITE_ENTERPRISE)
                       OSString << "Enterprise ";
                   else if (osvi.wSuiteMask & VER_SUITE_BLADE)
                       OSString << "Web ";
                   else
                       OSString << "Standard ";

                   switch (si.wProcessorArchitecture)
                   {
                   case PROCESSOR_ARCHITECTURE_AMD64:
                       OSString << "x64 "; break;
                   case PROCESSOR_ARCHITECTURE_IA64:
                       OSString << "Itanium-based "; break;
                   }

                   if (osvi.dwMinorVersion == 2)
                       OSString << "Edition ";
                   else
                       OSString << "Server ";
               }
               else     // Windows NT 4.0
               {
                   OSString << "Server 4.0";
                   if (osvi.wSuiteMask & VER_SUITE_ENTERPRISE)
                       OSString << ", Enterprise Edition";
                   else
                       OSString << " ";
               }
           }
           else     // test for specific product on Windows NT 4.0 SP5 and earlier
           {
               HKEY hKey;
               TCHAR szProductType[BUFSIZE];
               DWORD dwBufLen = BUFSIZE*sizeof(TCHAR);
               LONG lRet;

               lRet = RegOpenKeyEx( HKEY_LOCAL_MACHINE,
                              TEXT("SYSTEM\\CurrentControlSet\\Control\\ProductOptions"),
                              0, KEY_QUERY_VALUE, &hKey );
               if ( lRet == ERROR_SUCCESS )
               {
                   lRet = RegQueryValueEx( hKey, TEXT("ProductType"), NULL, NULL,
                           (LPBYTE) szProductType, &dwBufLen);
                   RegCloseKey( hKey );

                   if (lRet == ERROR_SUCCESS && dwBufLen <= BUFSIZ*sizeof(TCHAR))
                   {
                       if ( lstrcmpi( TEXT("WINNT"), szProductType) == 0)
                           OSString << "Workstation ";
                       if ( lstrcmpi( TEXT("LANMANNT"), szProductType) == 0)
                           OSString << "Server ";
                       if ( lstrcmpi( TEXT("SERVERNT"), szProductType) == 0)
                           OSString << "Advanced Server ";

                       OSString << osvi.dwMajorVersion << '.' << osvi.dwMinorVersion;
                   }
               }
            }
        }

        g_OSServicePackVer = osvi.wServicePackMajor + (osvi.wServicePackMinor/10.0f);

        // Display version, service pack (if any), and build number.
        if (osvi.dwMajorVersion <= 4)
        {
            OSString << "version " << osvi.dwMajorVersion << "." << osvi.dwMinorVersion << " "
                << osvi.szCSDVersion;
            if (lstrcmpi(osvi.szCSDVersion, TEXT("Service Pack 6") ) == 0)
            {
                HKEY hKey;
                LONG lRet;

                // Test for SP6 versus SP6a.
                lRet = RegOpenKeyEx( HKEY_LOCAL_MACHINE,
                        TEXT("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Hotfix\\Q246009"),
                        0, KEY_QUERY_VALUE, &hKey );
                if( lRet == ERROR_SUCCESS )
                    OSString << "a ";
                else // Windows NT 4.0 prior to SP6a
                    OSString << " ";
                RegCloseKey( hKey );
            }
            OSString << " (Build " << (unsigned)(osvi.dwBuildNumber & 0xFFFF) << ')';
        }
        else
            OSString << osvi.szCSDVersion;

        OSString << " (Build " << (unsigned)(osvi.dwBuildNumber & 0xFFFF) << ')';
        break;

    case VER_PLATFORM_WIN32_WINDOWS:

        if(osvi.dwMajorVersion == 4)
        {
            switch(osvi.dwMinorVersion)
            {
            case 0:
                OSString << "Microsoft Windows 95 ";
                if (osvi.szCSDVersion[1] == 'C')
                    OSString << "OSR2 ";
                OS_Type = OS_Win95;
                break;
            case 10:
                OSString << "Microsoft Windows 98 ";
                if (osvi.szCSDVersion[1] == 'A')
                    OSString << "Second Edition ";
                OS_Type = OS_Win98;
                break;
            case 90:
                OSString << "Microsoft Windows ME ";
                OS_Type = OS_WinMe;
                break;
            }
        }
        break;

    case VER_PLATFORM_WIN32s:
        OSString << "Microsoft Win32s ";  // too old for toontown
        break;
    }

    g_OSTypeStr = OSString.str();
#if defined(OSIS_VISTA)
	OS_Type = OS_WinVista;
#endif
    g_OSType = OS_Type;
    return OS_Type;
}

void SysInfo::
check_language_info(void) {
  LANGID lang_id = GetSystemDefaultLangID();
  LCID locale_id = GetUserDefaultLCID();
  char layoutname[KL_NAMELENGTH+1];
  GetKeyboardLayoutName(layoutname);
  _KeybdLayoutStr = layoutname;
  char msgbuf[15];
  sprintf(msgbuf,"0x%04X",lang_id);
  _LangIDStr = msgbuf;
  sprintf(msgbuf,"0x%04X",locale_id);
  _LocaleIDStr = msgbuf;
  errorLog  << "Keyboard Layout: " << _KeybdLayoutStr << " LangID: 0x" << _LocaleIDStr << " Locale ID: 0x" << _LocaleIDStr << endl;


}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_mouse
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
void SysInfo::
check_mouse(void) {
  _mouse_enabled = false;
  _mouse_buttons = 0;
  if (GetSystemMetrics(SM_MOUSEPRESENT)) {
    _mouse_enabled = true;
    _mouse_buttons = GetSystemMetrics(SM_CMOUSEBUTTONS);
  }

  errorLog << "Mouse " << (!_mouse_enabled ? "NOT " : "") << "detected" << endl;
}


#if 0
////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_colordepth
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
void SysInfo::
check_colordepth(void) {
  int x = GetSystemMetrics(SM_CXSCREEN);
  int y = GetSystemMetrics(SM_CYSCREEN);
}
#endif

void SysInfo::
get_country_info(HINSTANCE hKernel) {
  // doesnt work yet
#if 0
 if(_os_type<OS_WinXP) {
     // need XP
     return;
 }
 typedef int (WINAPI *GETGEOINFOAPROC)(GEOID Location,GEOTYPE GeoType,LPSTR lpGeoData,int cchData,LANGID LangId);
 GETGEOINFOAPROC pGetGeoInfoA = (GETGEOINFOAPROC) GetProcAddress(hKernel, "GetGeoInfoA");
 if(!pGetGeoInfoA) {
       errorLog << "GetProcAddr(GetGeoInfoA) failed, err=" << GetLastError() << endl;
       return;
 }
 DWORD GeoNationID;
 (*pGetGeoInfoA)(0x0,GEO_NATION,(LPSTR)&GeoNationID,sizeof(DWORD),0);

 char tmpbuf[200];
 (*pGetGeoInfoA)(GeoNationID,GEO_FRIENDLYNAME,tmpbuf,200,MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US));
 char tmpbuf2[200];
 sprintf(tmpbuf2,"%s (ID:0x%X)",tmpbuf,GeoNationID);
 _CountryNameStr = tmpbuf2;
#endif
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_ram
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////

void SysInfo::
check_ram(void) {
  if(_os_type>=OS_Win2000) {
      // must use GlobalMemoryStatusEx (only exists on XP/2000) to get higher totals than 2GB of RAM
      HINSTANCE hKernel = LoadLibrary("kernel32.dll");
      if(!hKernel) {
          errorLog << "LoadLibrary(kernel32.dll) failed, err=" << GetLastError() << endl;
          return;
      }

      get_country_info(hKernel);  // just sticking it here since kernel32.dll is already loaded here

      typedef BOOL (WINAPI *GLOBALMEMORYSTATUSEX)(LPMEMORYSTATUSEX lpBuffer);
      GLOBALMEMORYSTATUSEX pGlobMemStatusEx = (GLOBALMEMORYSTATUSEX) GetProcAddress(hKernel, "GlobalMemoryStatusEx");
      if(!pGlobMemStatusEx) {
          errorLog << "GetProcAddr(GlobMemStatEx) failed, err=" << GetLastError() << endl;
          goto cleanup;
      }

      MEMORYSTATUSEX MemStatus;
      MemStatus.dwLength = sizeof(MEMORYSTATUSEX);

      if(!(*pGlobMemStatusEx)(&MemStatus)) {
          errorLog << "GlobMemStatEx failed, err=" << GetLastError() << endl;
      }

      _ram_megs_total = (float) (MemStatus.ullTotalPhys / (double) ONE_MB_BYTES);
      _ram_megs_available = (float) (MemStatus.ullAvailPhys / (double) ONE_MB_BYTES);

      errorLog << "RAM: Total: " << _ram_megs_total << " MB, Free: " << _ram_megs_available << " MB, Utilization: " << MemStatus.dwMemoryLoad << "%\n";

     cleanup:
      FreeLibrary(hKernel);
  } else {
      MEMORYSTATUS mstat;
      mstat.dwLength = sizeof(mstat);
      GlobalMemoryStatus(&mstat);

      _ram_megs_total = (float) (mstat.dwTotalPhys / (double) ONE_MB_BYTES);
      _ram_megs_available = (float) (mstat.dwAvailPhys / (double) ONE_MB_BYTES);

      errorLog << "RAM: Total: " << _ram_megs_total << " MB, Free: " << _ram_megs_available << " MB\n";
  }
}

void SysInfo::PrintProcessMemInfo(HANDLE hProcess) {
  static bool bInitialized = false;

  time_t cur_time;
  time(&cur_time);

  float elapsed_sec = (float) difftime( cur_time,_startup_time);
  const float secs_per_hour = 3600.0f;
  const float secs_per_min = 60.0f;
  int hours = (int)(elapsed_sec/secs_per_hour);
  int minutes = (int) ((elapsed_sec-hours*secs_per_hour) / secs_per_min);
  int secs = (int) (elapsed_sec - ((hours*secs_per_hour) + (minutes*secs_per_min)));

  #define FMT_INT(XX)  (((XX) <=9) ? "0" : "") << (XX)

  errorLog << "[+" << FMT_INT(hours) << ":" << FMT_INT(minutes) << ":" << FMT_INT(secs) << "]: ";

  if(_os_type < SysInfo::OS_WinNT) {
      // this is the best we can do on win9x.  it isnt particularly accurate, since
      // another unrelated process could be hogging the memory for some reason.  inaccurate for mem > 2GB.
      MEMORYSTATUS mstat;
      mstat.dwLength = sizeof(mstat);
      GlobalMemoryStatus(&mstat);
      int perc_used = (int) (100.0f*(1.0f - (float)mstat.dwAvailPhys/(float)mstat.dwTotalPhys));
      errorLog << "RAM used by all processes: " << (float)((mstat.dwTotalPhys-mstat.dwAvailPhys)/(double)ONE_MB_BYTES) << "MB; " << perc_used << "% used\n";
      return;
  }

  if(!bInitialized) {
     bInitialized = true;

     _hPsAPI = LoadLibrary("psapi.dll");
     if(!_hPsAPI) {
         errorLog << "LoadLib(psapi) failed, err=" << GetLastError() << endl;
         return;
     }

     const char *GetProcessMemoryInfoStr = "GetProcessMemoryInfo";
     const char *GetPerfInfoStr = "GetPerformanceInfo";
     const char *ErrMsg = "GetProcAddr failed for ";

     _pGetProcessMemoryInfo = (GETPROCESSMEMORYINFO) GetProcAddress(_hPsAPI, GetProcessMemoryInfoStr);
     if(_pGetProcessMemoryInfo==NULL) {
         errorLog << ErrMsg << GetProcessMemoryInfoStr << ", err=" << GetLastError() << endl;
         return;
     }

     if(_os_type >= SysInfo::OS_WinXP) {
         // this API is on WinXP but not Win2000.  I believe you can get the same data
         // on win2k from the registry under HKEY_PERFORMANCE_DATA, but need to investigate
         _pGetPerfInfo = (GETPERFINFO) GetProcAddress(_hPsAPI, GetPerfInfoStr);
         if(_pGetPerfInfo==NULL) {
             errorLog << ErrMsg << GetPerfInfoStr << ", err=" << GetLastError() << endl;
             return;
         }
     }
  }

  if(_pGetPerfInfo!=NULL)
  {
      PERFORMANCE_INFORMATION PInfo;
      memset(&PInfo, 0, sizeof(PInfo));
      PInfo.cb = sizeof(PInfo);  // never know when somebody wants this initialized
      if(!(*_pGetPerfInfo)(&PInfo,sizeof(PInfo))) {
          errorLog << "GetPerfInfo failed - Error=" << GetLastError() << endl;
          return;
      }

      // PhysicalAvailable/Total is in Pages, not bytes
      int perc_used = (int) (100.0f*(1.0f - ((float)PInfo.PhysicalAvailable/(float)PInfo.PhysicalTotal)));
      errorLog << "Free RAM on system: " << (float)((((float)PInfo.PhysicalAvailable)*PInfo.PageSize)/(double)ONE_MB_BYTES) << "MB; " << perc_used << "% used" << endl;
  }

  if(_pGetProcessMemoryInfo!=NULL) {
      PROCESS_MEMORY_COUNTERS procCounters;
      ZeroMemory(&procCounters,sizeof(procCounters));
      procCounters.cb = sizeof(procCounters);  // never know when somebody wants this initialized
      if(!(*_pGetProcessMemoryInfo)(hProcess,&procCounters,sizeof(procCounters))) {
          errorLog << "GetProcMemInfo failed - Error=" << GetLastError() << endl;
          return;
      }
/* for some reason I dont know, stream operator crashes on winxp if you make this 1 big stream output
  (possibly because you tell <<  value is float, but pass a double??)
       errorLog << "MemUsage: " << (float)(procCounters.WorkingSetSize/MB_bytes)
                << "MB; Peak MemUsage: " << (float)(procCounters.PeakWorkingSetSize/MB_bytes)
                << "MB; PagefileUsage: " << (float)(procCounters.PagefileUsage/MB_bytes)
                << "MB; Peak PagefileUsage: " << (float)(procCounters.PeakPagefileUsage/MB_bytes)
                << "MB" << endl;
*/
       float recip_one_MB = 1.0f/(float)ONE_MB_BYTES;
       errorLog << "MemUsage: " << (procCounters.WorkingSetSize*recip_one_MB);
       errorLog << "MB; Peak MemUsage: " << (procCounters.PeakWorkingSetSize*recip_one_MB);
       errorLog << "MB; PagefileUsage: " << (procCounters.PagefileUsage*recip_one_MB);
       errorLog << "MB; Peak PagefileUsage: " << (procCounters.PeakPagefileUsage*recip_one_MB);
       errorLog << "MB" << endl;
  }
}

void MyGetFileVersion(char *FileName, ULARGE_INTEGER *pli) {
    UINT     uFfiLen;
    VS_FIXEDFILEINFO *pFfi;
    BYTE *pVerInfoBuf=NULL;

    pli->HighPart = 0;
    pli->LowPart  = 0;

    int iLength = GetFileVersionInfoSize ( FileName, 0 );
    pVerInfoBuf = new BYTE[iLength];
    if ( GetFileVersionInfo(FileName, 0, iLength, pVerInfoBuf ) == 0 ) {
            errorLog << "GetFileVersionInfo error=" << GetLastError() << endl;
            goto error;
    }

    if ( VerQueryValue (pVerInfoBuf, "\\", (void **)&pFfi,  &uFfiLen ) == 0 ) {
        errorLog << "VerQueryValue error=" << GetLastError() << endl;
        goto error;
    }

    // pFfi is set to point inside pVerInfoBuf

    // could get product version # too
    pli->HighPart = pFfi->dwFileVersionMS;
    pli->LowPart  = pFfi->dwFileVersionLS;

    error:

    if(pVerInfoBuf!=NULL)
        delete [] pVerInfoBuf;
}

void MyGetModuleVersion(HMODULE hMod, ULARGE_INTEGER *pli) {
    // sometimes this return 0.0.0.0, apparently.  no idea how.

    UINT     uFfiLen;
    VS_FIXEDFILEINFO *pFfi;
    BYTE *pVerInfoBuf=NULL;

    pli->HighPart = 0;
    pli->LowPart  = 0;

    HRSRC hRsrc = FindResource(hMod,MAKEINTRESOURCE(VS_VERSION_INFO),RT_VERSION);
    if(hRsrc==NULL) {
        errorLog << "GetVer FindResource failed, err=" << GetLastError() << endl;
        goto error;
    }

    HGLOBAL hMemRsrc = LoadResource(hMod,hRsrc);
    if(hMemRsrc==NULL) {
        errorLog << "GetVer LoadResource failed, err=" << GetLastError() << endl;
        goto error;
    }

    pVerInfoBuf = (BYTE*) LockResource(hMemRsrc);
    if(pVerInfoBuf==NULL) {
        errorLog << "GetVer LockResource failed, err=" << GetLastError() << endl;
        goto error;
    }

    if ( VerQueryValue (pVerInfoBuf, "\\", (void **)&pFfi,  &uFfiLen ) == 0 ) {
        errorLog << "VerQueryValue error=" << GetLastError() << endl;
        goto error;
    }

    // could get product version # too
    pli->HighPart = pFfi->dwFileVersionMS;
    pli->LowPart  = pFfi->dwFileVersionLS;

   error:
     // msdn says we dont have to free the locked resource?
    ;
}

// On Win2K, GetDeviceIdentifier will always return zero for the driver version,
// so this workaround must be done to manually find the driver files and get their
// version numbers
void SearchforDriverInfo(const char *driver_filename,ULARGE_INTEGER *pli,SYSTEMTIME *pDriverDate) {
    // NOTE! If this Win2k bodge-around needs to be done, ddid.guidDeviceIdentifier
    // will not tally with the updated driver version numbers. Ah well.

    // Go on a hunt for the driver file.
    char FileName[MAX_PATH];
    WIN32_FIND_DATA FileFindData;

    if(pli!=NULL)
        ZeroMemory(pli,sizeof(ULARGE_INTEGER));
    if(pDriverDate!=NULL)
        ZeroMemory(pDriverDate,sizeof(SYSTEMTIME));

    char *pDirectories[] = {"\\","\\Drivers\\","32\\Drivers\\"};
    char *pExtensions[] = {"",".dll",".vxd",".sys"};

    int iNumDirs = sizeof(pDirectories) / sizeof(char *);
    int iNumExts = sizeof(pExtensions) / sizeof(char *);

    GetSystemDirectory( FileName, MAX_PATH );
    size_t SysDirNameLen=strlen(FileName);

    // probably could optimize this to 1 FindFirstFile call by converting filename to a path containing all the dirs

    //errorLog << "iNumDirs= " << iNumDirs << " iNumExts= " << iNumExts << endl;
    HANDLE Handle = INVALID_HANDLE_VALUE;
    for ( int i = 0; ( i < iNumDirs ) && ( Handle == INVALID_HANDLE_VALUE ); i++ ) {
      for ( int j = 0; ( j < iNumExts ) && ( Handle == INVALID_HANDLE_VALUE ); j++ ) {
        FileName[SysDirNameLen]='\0';   // restart string at '%windir%\system32'
        strcat( FileName, pDirectories[i] );
        strcat( FileName, driver_filename );
        if(pExtensions[j][0]!='\0')
          strcat ( FileName, pExtensions[j] );
        Handle = FindFirstFile ( FileName,&FileFindData );
        //errorLog << "i= " << i << " and j= " << j << ". Looking at " << FileName << " Handle= " << Handle << endl;
      }
    }

    if ( Handle == INVALID_HANDLE_VALUE ) {
      // errorLog << "Couldn't find driver file '" << driver_filename << "' to retrieve driver version #" << endl;
      return;
    }

    // FAT doesnt record creation time, but NTFS does, so just take the least of all the given times

    SYSTEMTIME SysTime_1990;
    FILETIME FTime_1990, FTime_least;
    FILETIME filetimes[3];

    ZeroMemory(&SysTime_1990,sizeof(SysTime_1990));
    SysTime_1990.wYear = 1990;
    SysTime_1990.wMonth = 1;
    SysTime_1990.wDay = 1;
    SystemTimeToFileTime(&SysTime_1990,&FTime_1990);

    filetimes[0] = FileFindData.ftCreationTime;
    filetimes[1] = FileFindData.ftLastAccessTime;
    filetimes[2] = FileFindData.ftLastWriteTime;

    bool bAllDatesInvalid = true;

    // find a valid time > 1990
    for(int i=2;i>=0;i--) {
      if(CompareFileTime(&FTime_1990,&filetimes[i])!=1) {
        FTime_least = filetimes[i];
        bAllDatesInvalid = false;
      }
    }

    if(bAllDatesInvalid) {
      goto cleanup;
    }

    for(int i=0;i<3;i++) {
      if((CompareFileTime(&FTime_least,&filetimes[i])==1) &&
         (CompareFileTime(&FTime_1990,&filetimes[i])!=1))
        FTime_least = filetimes[i];
    }

    FileTimeToSystemTime(&FTime_least,pDriverDate);

/*
    #define FILETIMEtoInt64(I64,FTIME) \
        I64 = ((__int64)FTIME.dwHighDateTime<<32) | FTIME.dwLowDateTime;

    unsigned __int64 filetimes[3];

    FILETIMEtoInt64(filetimes[0],FileFindData.ftCreationTime);
    FILETIMEtoInt64(filetimes[1],FileFindData.ftLastAccessTime);
    FILETIMEtoInt64(filetimes[2],FileFindData.ftLastWriteTime);
    unsigned __int64 least_time = filetimes[0];

    // set any zero times to max time, to ignore them
    for(int i=0;i<3;i++) {
        if(filetimes[i] == 0)
            filetimes[i]=((__int64)0xFFFFFFFF << 32) | 0xFFFFFFFF;  // does it handle 64-bit constants?
    }
    unsigned __int64 leasttime=filetimes[0];
    for(int i=1;i<3;i++) {
        if(filetimes[i] < leasttime)
            leasttime=filetimes[i];
    }

    FILETIME ftLeastTime;
    ftLeastTime.dwHighDateTime = (DWORD) (leasttime >> 32);
    ftLeastTime.dwLowDateTime = (DWORD) (leasttime | 0xFFFFFFFF);
    FileTimeToSystemTime(&ftLeastTime,pDriverDate);
*/

 #if 0
    FileTimeToSystemTime(&FileFindData.ftCreationTime,&DriverDate_SysTime);
    errorLog << "CreationTime: H: " << FileFindData.ftCreationTime.dwHighDateTime << "L: " << FileFindData.ftCreationTime.dwLowDateTime << endl;
    errorLog << "Date: "<<DriverDate_SysTime.wMonth <<"/"<<DriverDate_SysTime.wDay <<"/"<<DriverDate_SysTime.wYear << endl;

    FileTimeToSystemTime(&FileFindData.ftLastAccessTime,&DriverDate_SysTime);
    errorLog << "LastAccessTime: H: " << FileFindData.ftLastAccessTime.dwHighDateTime << "L: " << FileFindData.ftLastAccessTime.dwLowDateTime << endl;
    errorLog << "Date: "<<DriverDate_SysTime.wMonth <<"/"<<DriverDate_SysTime.wDay <<"/"<<DriverDate_SysTime.wYear << endl;

    FileTimeToSystemTime(&FileFindData.ftLastWriteTime,&DriverDate_SysTime);
    errorLog << "LastWriteTime: H: " << FileFindData.ftLastWriteTime.dwHighDateTime << "L: " << FileFindData.ftLastWriteTime.dwLowDateTime << endl;
    errorLog << "Date: "<<DriverDate_SysTime.wMonth <<"/"<<DriverDate_SysTime.wDay <<"/"<<DriverDate_SysTime.wYear << endl;
  #endif

 cleanup:

    FindClose(Handle);

    if(pli==NULL)
        return;

    MyGetFileVersion(FileName, pli);
}

// returns true if version is ok
bool verify_version(const ULARGE_INTEGER &Ver,DWORD a,DWORD b,DWORD c,DWORD d) {

    unsigned __int64 x1 = (a << 16) | b;
    unsigned __int64 y1 = (c << 16) | d;
    unsigned __int64 goodver = (x1 << 32) | y1;
    unsigned __int64 curver = Ver.QuadPart;
    bool bGood=(curver >= goodver);

    if(!bGood) {
        errorLog << "Obsolete Driver Version ("<< PRINTDRIVER_VERSTR(Ver) <<") detected, requires version (" << a << "." << b << "." << c << "." << d << ")" << endl;
    }

    return bGood;
}

bool DoesSysFileExist(char *pFileName) {
      WIN32_FIND_DATA TempFindData;
      HANDLE FindFileHandle;
      char tmppath[MAX_PATH+MAX_PATH];
      tmppath[0]='\0';
      GetSystemDirectory(tmppath,MAX_PATH);
      strcat(tmppath,"\\");
      strcat(tmppath,pFileName);
      // errorLog << "searching for '" << tmppath << "'\n";
      FindFileHandle = FindFirstFile(tmppath, &TempFindData);
      if ( FindFileHandle != INVALID_HANDLE_VALUE ) {
          FindClose(FindFileHandle);
          return true;
      }

      return false;
}

const char *MS_DX_URL="http://www.microsoft.com/directx";
const char *DX_MSG_HTML_PREFIX="Also make sure you have installed the latest version of the "
                               "Microsoft DirectX Runtime from <a href=\"";
void SysInfo::
PrintNo3DHWMsg(void) {
    _gfx_report_str << "Your video card ";
    if(!_VideoCardNameStr.empty()) {
      _gfx_report_str << "(" << _VideoCardNameStr << ") ";
    }

   _gfx_report_str << "indicates it does not support Direct3D or OpenGL acceleration. "
                      "Please check your video card manufacturer's website for updated drivers if you believe this is incorrect.  "
                      "To play Toontown, you must install a video adapter that supports either Direct3D or OpenGL "
                      "3D hardware acceleration.  See <a href=\"http://play.toontown.com/faq.php#hardware\">http://play.toontown.com/faq.php</a> "
                      "for a list of graphics cards known to run Toontown successfully.  "
                   << DX_MSG_HTML_PREFIX << MS_DX_URL << "\">" << MS_DX_URL << "</a>\n";
}

const char *generic_gfx_errmsg="An error was generated during video card detection.  "
                               "Please file a bug report, and make sure you have the latest "
                               "video drivers from your manufacturer's website.";
void SysInfo::
SetGeneric3DError(char *LogErrorStr) {
    if(LogErrorStr!=NULL) {
       errorLog << LogErrorStr << endl;
    }
    _gfx_report_str << generic_gfx_errmsg
                    << DX_MSG_HTML_PREFIX << MS_DX_URL << "\">" << MS_DX_URL << "</a>\n";
}

void SysInfo::
check_3d_hw(void)
{
  _numMonitors = GetSystemMetrics(SM_CMONITORS);

  if(_DXVerStr.empty()) {
      const char *DXRegKeyName = "SOFTWARE\\Microsoft\\DirectX";  //under HKEY_LOCAL_MACHINE
      HKEY hDXKey;
      if (ERROR_SUCCESS != RegOpenKeyEx(HKEY_LOCAL_MACHINE, DXRegKeyName,0,KEY_READ,&hDXKey)) {
        errorLog << "DX reg RO failed, err=" << GetLastError() << endl;
        return;
      }

      if (hDXKey == NULL) {
        return;
      }
      char DXverstr[100];
      DWORD dwType,dwSize=100;
      if(ERROR_SUCCESS != RegQueryValueEx(hDXKey, "Version", 0, &dwType, (LPBYTE)DXverstr,&dwSize)) {
           return;
      }
      RegCloseKey(hDXKey);
      _DXVerStr = DXverstr;
      errorLog << "installed DX VerStr: " << DXverstr << endl;
  }

  _has_3d_hw = false;

  GAPIType _dx_level_installed = GAPI_Unknown;
  GAPIType preferred_api = GAPI_Unknown;
  _gfx_api_suggested = GAPI_Unknown;

  if(DoesSysFileExist("d3d9.dll")) {
    _dx_level_installed = GAPI_DirectX_9_0;
  } else if(DoesSysFileExist("dpnhpast.dll")) {
    _dx_level_installed = GAPI_DirectX_8_1;
  } else if(DoesSysFileExist("d3d8.dll")) {
    _dx_level_installed = GAPI_DirectX_8_0;
  } else if(DoesSysFileExist("d3dim700.dll")) {
    _dx_level_installed = GAPI_DirectX_7;
  } else if(DoesSysFileExist("d3dramp.dll")) {
    _dx_level_installed = GAPI_DirectX_6;
  } else if(_os_type == SysInfo::OS_Win98) {
    _dx_level_installed = GAPI_DirectX_5;
  }

  //extern void  PrintDxDiagDisplayInfo();
  // PrintDxDiagDisplayInfo();

#if defined(FORCE_OPENGL)
  _dx_level_installed=GAPI_DirectX_6;
  errorLog << "Forcing OpenGL for debugging purposes\n";
#elif defined(FORCE_DX7)
  _dx_level_installed=GAPI_DirectX_7;
  errorLog << "Forcing DX7 for debugging purposes\n";
#elif defined(FORCE_DX8)
  _dx_level_installed=GAPI_DirectX_8_1;
  errorLog << "Forcing DX8 for debugging purposes\n";
#elif defined(FORCE_DX9)
  _dx_level_installed=GAPI_DirectX_9_0;
  errorLog << "Forcing DX9 for debugging purposes\n";
#elif defined(FORCE_DX6)
  _dx_level_installed=GAPI_DirectX_6;
  errorLog << "Forcing DX6 for debugging purposes\n";
#endif

  errorLog << "DX Level Installed: " << get_gfx_api_name(_dx_level_installed) << endl;

#if defined(USE_DX9)
  if(_dx_level_installed<GAPI_DirectX_9_0) {
     _DX9_status=Status_Unsupported;
  }
#endif
  if(_dx_level_installed<GAPI_DirectX_8_0) {
     _DX8_status=Status_Unsupported;
  }

#if defined(USE_DX7)
  if(_dx_level_installed<GAPI_DirectX_7) {
     _DX7_status=Status_Unsupported;
  }
#endif

  // first determine what dx is installed.
  // then do enough to get primary card device ID using dx7, dx8 or dx9, and check if dx7, dx8 or dx9 is fully working.
  // then compare result to preferred api. if its the preferred api, return.
  // if not, check preferred api.

#if defined(USE_DX9)
  // First test DX9, since that is the most likely API and we want to minimize startup time for most people.

  // drose is turning off this test for now, so we won't suggest DX9
  // by default.  There are the following problems:

  // (1) Avoiding Test_DX8 also bypasses the check for 3-d hardware,
  // so we don't get the card and driver information in the logs, and
  // we don't filter out people who don't have sufficient 3-d
  // hardware.

  // (2) At least one person on the test server seems to be unable to
  // open a DX9 window (they get an exit with E_OUTOFMEMORY--not to be
  // confused with E_OUTOFVIDEOMEMORY).  Then Panda crashes,
  // apparently because the check for failure after CreateDevice
  // simply checks for E_OUTOFVIDEOMEMORY, and falls through
  // otherwise, allowing the code to continue after CreateDevice has
  // failed.  (Test bug #3416.  This also happens to me on my home
  // machine.)  It is not clear whether this is related to a
  // combination of low system memory on Win98, or some other problem.

  // (3) Attempting to open a DX9 window, and failing, seems to
  // prevent some users from successfully failing over to DX8 (where
  // these users would have been able to open a DX8 window
  // successfully if they'd started there).  This was made evident
  // when we had a bug that prevented the DX9 fullscreen window from
  // opening in every case, which is now fixed, but the side-effect of
  // being unable to open any window should DX9 fail still remains.  I
  // suspect this is really the same problem as (2), above.

  // (4) At least one user complains that the screen "flickers", and
  // another user complains that it's unable to match his monitor's
  // sync rate.  (Test bugs #3411 and #3431).  Both of these users
  // seem to be getting a 1280x1024 resolution mode by default,
  // so perhaps there's a new bug in pickbestres.

 test_dx9:
  if(_dx_level_installed>= GAPI_DirectX_9_0) {
    //HRESULT hr;
    if(_DX9_status==Status_Unknown) {
      Test_DX9(_dx_level_installed>=GAPI_DirectX_9_0);
      //hr = DxDiag_Init();
      //hr = PrintDxDiagDisplayInfo();
    }
    if(_DX9_status==Status_Supported) {
      if(!ValidateCardTypeandDriver()) {
        goto no_3d_hw;
      }

      if(preferred_api == GAPI_Unknown)
        preferred_api = GetPreferredGAPI();

      if((preferred_api==GAPI_DirectX_8_0)&&(_DX8_status==Status_Unknown)) {
        goto test_dx8;
      }
#ifdef USE_DX7
	  else if((preferred_api==GAPI_DirectX_7)&&(_DX7_status==Status_Unknown)) {
        goto test_dx7;
      }
#endif
      else if((preferred_api==GAPI_OpenGL)&&(_OpenGL_status==Status_Unknown)) {
        goto test_ogl;
      }

      _gfx_api_suggested=min(_dx_level_installed,GAPI_DirectX_9_0);
      goto success;
    }
  }
#endif

 test_dx8:
  if(_dx_level_installed>= GAPI_DirectX_8_0) {
    if(_DX8_status==Status_Unknown)
      Test_DX8(_dx_level_installed>=GAPI_DirectX_8_1);

    if(_DX8_status==Status_Supported) {
      if(!ValidateCardTypeandDriver()) {
        goto no_3d_hw;
      }

      if(preferred_api == GAPI_Unknown)
        preferred_api = GetPreferredGAPI();

#ifdef USE_DX7
      if((preferred_api==GAPI_DirectX_7)&&(_DX7_status==Status_Unknown)) {
        goto test_dx7;
      }
#endif
      else if((preferred_api==GAPI_OpenGL)&&(_OpenGL_status==Status_Unknown)) {
        goto test_ogl;
      }

      _gfx_api_suggested=min(_dx_level_installed,GAPI_DirectX_8_1);
      goto success;
    }
  }

#if defined(USE_DX7)
 test_dx7:
  if(_dx_level_installed >= GAPI_DirectX_7) {
    if(_DX7_status==Status_Unknown)
      Test_DX7(true);

    if(_DX7_status==Status_Supported) {
      if(!ValidateCardTypeandDriver()) {
        goto no_3d_hw;
      }

      if(preferred_api == GAPI_Unknown)
        preferred_api = GetPreferredGAPI();

      if((preferred_api==GAPI_OpenGL)&&(_OpenGL_status==Status_Unknown)) {
        goto test_ogl;
      }
      _gfx_api_suggested=GAPI_DirectX_7;
      goto success;
    }
  }
#endif

 test_ogl: {
    if(_OpenGL_status==Status_Unknown)
      Test_OpenGL();

    if(_OpenGL_status==Status_Supported) {
      if(_bValidVideoDeviceID && (!ValidateCardTypeandDriver())) {
        goto no_3d_hw;
      }

      // preferred API unimportant, since this is the last resort and all others shouldve been tested by now

      _gfx_api_suggested=GAPI_OpenGL;
      goto success;
    }
  }

 // we didnt get our 'preferred api', so just pick any one already found to be supported
 if(_DX8_status==Status_Supported) {
     _gfx_api_suggested=min(_dx_level_installed,GAPI_DirectX_8_1);
     goto success;
 }

 #ifdef USE_DX7
 if(_DX7_status==Status_Supported) {
     _gfx_api_suggested=GAPI_DirectX_7;
     goto success;
 }
#endif

 if(_OpenGL_status==Status_Supported) {
     _gfx_api_suggested=GAPI_OpenGL;
     goto success;
 }

 // if we skipped over any api tests, go back and try them before failing completely
#if defined(USE_DX7)
 if(_DX7_status==Status_Unknown)
     goto test_dx7;
#endif

 if(_DX8_status==Status_Unknown)
     goto test_dx8;

#ifdef USE_DX9
 if(_DX9_status==Status_Unknown)
     goto test_dx9;
#endif

 if(_OpenGL_status==Status_Unknown)
     goto test_ogl;

	assert(_OpenGL_status==Status_Unsupported);
#if defined(USE_DX7)
	assert(_DX7_status==Status_Unsupported);
#endif
	assert(_DX8_status==Status_Unsupported);
#if defined(USE_DX9)
    assert(_DX9_status==Status_Unsupported);
#endif

 no_3d_hw:
  _has_3d_hw = false;
  PrintNo3DHWMsg();
  return;

 success:
   errorLog << "Suggested GfxApi: " << get_gfx_api_name(_gfx_api_suggested) << endl;
   _has_3d_hw = true;
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_snd
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
typedef HRESULT (WINAPI *DSOUNDENUM_PROC)(LPDSENUMCALLBACK lpDSEnumCallback, LPVOID lpContext);
BOOL CALLBACK DSoundEnumCallback(LPGUID lpGuid, LPCSTR lpcstrDescription,
                                 LPCSTR lpcstrModule, LPVOID  lpContext) {
  static int CardNum=0;

  string *pDevStr = (string *)lpContext;
  ostringstream TmpDevDesc;

  TmpDevDesc << lpcstrDescription;

  if((lpcstrModule!=NULL) && (*lpcstrModule!='\0')) {
    SYSTEMTIME DriverDate_SysTime;
    ULARGE_INTEGER liDriverVersion;
    SearchforDriverInfo(lpcstrModule,&liDriverVersion,&DriverDate_SysTime);
    TmpDevDesc << "; file: " << lpcstrModule << "; Driver Version: (";
    if((liDriverVersion.HighPart==0)&&(liDriverVersion.LowPart==0)) {
      TmpDevDesc << "not found";
    } else {
      TmpDevDesc << PRINTDRIVER_VERSTR(liDriverVersion);
    }
    TmpDevDesc << ") Date: (";
    if(DriverDate_SysTime.wYear==0) {
      TmpDevDesc << "not found)";
    } else {
      TmpDevDesc <<DriverDate_SysTime.wMonth <<"/"
                 <<DriverDate_SysTime.wDay <<"/"
                 <<DriverDate_SysTime.wYear << ")";
    }
  }
  if(strstr(lpcstrDescription,"Primary Sound Driver")==NULL) {
    // do we want to break out the fields (driver date/ver) so they are more easily searchable?
    // how to do for multiple devices?
    if(!pDevStr->empty())
      pDevStr->append(";; ");
    pDevStr->append(TmpDevDesc.str());
  }

  errorLog << "found DirectSound driver[" << CardNum << "]: " << TmpDevDesc.str() << endl;
  CardNum++;

  return TRUE;
}

void SysInfo::
check_snd(void) {

#ifdef USING_MILES_SOUND
  _sound_enabled = true;

  // note:  miles does NOT require direct sound driver support (although perf is not as good)
#endif

  // use dsound to just print sound card info to log, for debug tracking purposes

  HINSTANCE dshinst = NULL;

  // Check for sound card
  dshinst = LoadLibrary("dsound.dll");
  if (!dshinst) {
    errorLog << "Error: LoadLibrary() failed on dsound.dll" << endl;
    goto _return;
  }

  const char *pDSEnumStr="DirectSoundEnumerateA";

  DSOUNDENUM_PROC pDsEnum = (DSOUNDENUM_PROC)GetProcAddress(dshinst, pDSEnumStr);
  if (NULL == pDsEnum) {
    errorLog << "Error: GetProcAddr failed for " << pDSEnumStr << endl;
    goto _return;
  }

  _DSoundDevicesStr.clear();

  HRESULT hr = (*pDsEnum)(DSoundEnumCallback,&_DSoundDevicesStr);
  if(FAILED(hr)) {
    errorLog << "Error: GetProcAddr failed for " << pDSEnumStr << endl;
  }

_return:
  // free dsound
  if(dshinst)
    FreeLibrary(dshinst);

  UINT nMidiDevs = midiOutGetNumDevs();
  MIDIOUTCAPS mcaps;

  _MidiOutAllDevicesStr.clear();

  for(UINT i=0;i<nMidiDevs;i++) {
      ZeroMemory(&mcaps,sizeof(mcaps));
      MMRESULT result = midiOutGetDevCaps(i,&mcaps,sizeof(mcaps));
      if(result!=MMSYSERR_NOERROR) {
          errorLog << "Error: midiOutGetDevCaps("<<i<<") failed, err=" << result << endl;
          continue;
      }

      const char *devtypestrs[8] = {"?","HW Midiport","Synth","SqWav Synth","FM Synth","MS Midi Mapper","HW Wavetable Synth","SW Synth"};
      ostringstream TmpDevDesc;

      TmpDevDesc << mcaps.szPname <<  ", Type: " << devtypestrs[mcaps.wTechnology]
                 << ", ManufID: " << mcaps.wMid << ", ProdID: " << mcaps.wPid << ", DrvVer: "
                 << HIWORD(mcaps.vDriverVersion) << "." << LOWORD(mcaps.vDriverVersion);

      if(mcaps.wVoices>0) {
        TmpDevDesc << ", Voices: " << mcaps.wVoices;
      }

      if(mcaps.wNotes>0) {
        TmpDevDesc << ", Notes: " << mcaps.wNotes;
      }

      char msgbuf1[10],msgbuf2[10];
      sprintf(msgbuf1,"0x%04X",mcaps.wChannelMask);
      sprintf(msgbuf2,"0x%02X",mcaps.dwSupport);

      TmpDevDesc << ", ChanMsk: " << msgbuf1 << ", Sflags: " << msgbuf2;

      errorLog << "MidiOut Device: " << TmpDevDesc.str() << endl;

      for(char *pCh=mcaps.szPname;(*pCh!='\0');pCh++) {
          *pCh=tolower(*pCh);
      }

      // for Config Record, stuff all the midi devices in 1 string
      // ignore the Microsoft GS Wavetable SW Synth, MS Midi Mapper, and Microsoft Synthesizer, which
      // should appear on all windows machines.
      if((mcaps.wTechnology != MOD_MAPPER) &&
         (strstr(mcaps.szPname,"microsoft gs wavetable")==NULL) &&
         (strstr(mcaps.szPname,"microsoft synthesizer")==NULL)) {

         if(!_MidiOutAllDevicesStr.empty()) {
             _MidiOutAllDevicesStr.append(";; ");
         }
         _MidiOutAllDevicesStr.append(TmpDevDesc.str());
      }
  }
}



////////////////////////////////////////////////////////////////////
//     Function: SysInfo::get_commport_baud
//       Access: Protected
//  Description:
////////////////////////////////////////////////////////////////////
int SysInfo::
get_commport_baud(const char *cportname) {
  int baudrate = 0;
  HANDLE cport = CreateFile(cportname,
                    GENERIC_READ | GENERIC_WRITE,
                    0, // Comm devices must be opened exclusive access
                    NULL, // No security attributes
                    OPEN_EXISTING,
                    0, // Not overlapped I/O
                    NULL);
  if (cport == INVALID_HANDLE_VALUE)
    return 0;

  DCB devCB;
  devCB.DCBlength = sizeof(devCB);
  if (!GetCommState(cport, &devCB))
    errorLog << "SysInfo::check_commport() - GetCommState() failed for:"
      << cportname << endl;
  else {
    switch (devCB.BaudRate) {
      case CBR_110:
      case CBR_300:
      case CBR_600:
      case CBR_1200:
      case CBR_2400:
      case CBR_4800:
      case CBR_9600:
        baudrate = 9600;
        break;
      case CBR_14400:
        baudrate = 14400;
        break;
      case CBR_19200:
        baudrate = 19200;
        break;
      case CBR_38400:
        baudrate = 38400;
        break;
      case CBR_56000:
        baudrate = 56000;
        break;
      case CBR_57600:
        baudrate = 57600;
        break;
      case CBR_115200:
        baudrate = 115200;
        break;
      case CBR_128000:
        baudrate = 128000;
        break;
      case CBR_256000:
        baudrate = 256000;
        break;
      default:
        baudrate = devCB.BaudRate;
        break;
    }
  }
  CloseHandle(cport);

  errorLog << "Baud rate: " << baudrate << endl;
  return baudrate;
}

////////////////////////////////////////////////////////////////////
//     Function: SysInfo::check_net_connection
//       Access: Protected
//  Description:
//MODEMDEVCAPS
//GetCommProperties
//GetCommConfig
//GetCommState
//GetDefaultCommConfig
////////////////////////////////////////////////////////////////////
void SysInfo::
check_net_connection(void) {
    HINSTANCE         hIPHlp = NULL;
    PIP_ADAPTER_INFO  pAdapterInfo = NULL;
    ULONG             ulSizeAdapterInfo = 0;
    DWORD             dwStatus;

    _bNetworkIsLAN = false;
    _MACAddrStr = "Unknown";
    _IPAddrStr = "Unknown";

    // iphlpapi.dll doesnt exist on w95
    hIPHlp = LoadLibrary("iphlpapi.dll");
    if(!hIPHlp) {
        errorLog << "error: Loadlib failed on iphlpapi.dll!\n";
        goto get_conn_info;
    }

    typedef DWORD (WINAPI *GETADAPTERSINFO)(PIP_ADAPTER_INFO pAdapterInfo,PULONG pOutBufLen);
    GETADAPTERSINFO pGetAdaptersInfo = (GETADAPTERSINFO) GetProcAddress(hIPHlp,"GetAdaptersInfo");
    if(!pGetAdaptersInfo)
        goto get_conn_info;

    // Find out how big our buffer needs to be to hold the data
    dwStatus = (*pGetAdaptersInfo)(NULL, &ulSizeAdapterInfo);
    if (dwStatus != ERROR_BUFFER_OVERFLOW) {
        errorLog << "GetAdaptersInfo failed, err=" << dwStatus << endl;
        goto get_conn_info;
    }

    pAdapterInfo = (PIP_ADAPTER_INFO)malloc(ulSizeAdapterInfo);
    if(!pAdapterInfo) {
        errorLog << "GetAdaptersInfo malloc failed!\n";
        goto get_conn_info;
    }

    dwStatus = (*pGetAdaptersInfo)(pAdapterInfo, &ulSizeAdapterInfo);
    if (dwStatus != ERROR_SUCCESS) {
        errorLog << "GetAdaptersInfo failed, err=" << dwStatus << endl;
        goto get_conn_info;
    }

    if (pAdapterInfo == NULL) {
       errorLog << "GetAdaptersInfo found no network adapters\n";
       goto get_conn_info;
    }

    PIP_ADAPTER_INFO pCurAdapterInfo = pAdapterInfo;

    // Step through the adapter list
    for(;pCurAdapterInfo != NULL;pCurAdapterInfo = pCurAdapterInfo->Next) {
          PIP_ADDR_STRING pAddressList = &(pCurAdapterInfo->IpAddressList);
          for(;pAddressList != NULL;pAddressList = pAddressList->Next) {
             char ipstr[17];
             ZeroMemory(ipstr,17);
             strncpy(ipstr,pAddressList->IpAddress.String,16);
             errorLog << "IP Addr: " << ipstr << endl;
             if((strncmp(ipstr,"127.0.0.1",16)==0) ||
                (strncmp(ipstr,"0.0.0.0",16)==0) ||
                (ipstr[0]=='\0')) {
                errorLog << "ignoring IP Addr\n";
                continue;
             } else {
                 // only use real ip's as official _IPAddrStr
                 _IPAddrStr = ipstr;
             }
          }

          // BUGBUG: will modem users have MAC addresses??

          #define MAC_ADDR_STRLEN (MAX_ADAPTER_ADDRESS_LENGTH*3+1)
          char mac_addr_str[MAC_ADDR_STRLEN];
          ZeroMemory(mac_addr_str,MAC_ADDR_STRLEN);
          char *pCh = mac_addr_str;
          for(DWORD i=0;i<pCurAdapterInfo->AddressLength;i++) {
            sprintf(pCh,"%02X-",pCurAdapterInfo->Address[i]);
            pCh+=3;
          }
          *(pCh-1)='\0';

          errorLog << "MAC Address: " << mac_addr_str << endl;
          _MACAddrStr = mac_addr_str;
    }

    get_conn_info:

    if(pAdapterInfo != NULL)
        free(pAdapterInfo);

    // initialize to "safe" values
    _comm_type = C_unknown;
    _comm_baud = 0;

    DWORD dwFlags;
    // check for an internet connection
    if(!InternetGetConnectedState(&dwFlags, 0)) {
        errorLog << "No Internet connection detected" << endl;
        _comm_baud = 0;
        return;
    }

    if(dwFlags & INTERNET_CONNECTION_OFFLINE) {
        errorLog << "System is currently in offline-mode" << endl;
    }

    if(dwFlags & INTERNET_CONNECTION_MODEM) {
        errorLog << "Internet connection is through a modem" << endl;

        // check for COM ports
        int baudrate[4];
        baudrate[0] = get_commport_baud("COM1");
        baudrate[1] = get_commport_baud("COM2");
        baudrate[2] = get_commport_baud("COM3");
        baudrate[3] = get_commport_baud("COM4");
        int cport = 0;
        for (int i = 0; i < 4; i++) {
          if (baudrate[i] > _comm_baud) {
            _comm_baud = baudrate[i];
            cport = i;
          }
        }
        errorLog << "Fastest baud detected: " << _comm_baud << " on comm port: " << cport << endl;

    } else if(dwFlags & INTERNET_CONNECTION_LAN) {
        _comm_baud = 100000000;  // dummy val
        //comm_type = LAN?
        errorLog << "Internet connection is through a LAN" << endl;
        _bNetworkIsLAN = true;
    }

    if(dwFlags & INTERNET_CONNECTION_PROXY)
        errorLog << "Internet connection is through a proxy server" << endl;

    if(dwFlags & INTERNET_CONNECTION_MODEM_BUSY)
        errorLog << "Internet connection: modem is busy" << endl;

    if(hIPHlp == NULL)
        FreeLibrary(hIPHlp);
}

#ifdef ERROR_STRING_TABLE
// this table is good for 40k...

static string ConvHRErrorToString(const HRESULT &error) {
  switch(error) {
    case E_FAIL:
      return "Unspecified error E_FAIL";

    case DD_OK:
      return "No error.";
    case D3DERR_BADMAJORVERSION      : // (700)
      return "D3DERR_BADMAJORVERSION";//: // (700)
    case D3DERR_BADMINORVERSION      : // (701)
      return "D3DERR_BADMINORVERSION";//: // (701)
    case D3DERR_INVALID_DEVICE   : // (705)
      return "D3DERR_INVALID_DEVICE";//: // (705)
    case D3DERR_INITFAILED       : // (706)
      return "D3DERR_INITFAILED";//: // (706)
    case D3DERR_DEVICEAGGREGATED : // (707)
      return "D3DERR_DEVICEAGGREGATED";//: // (707)
    case D3DERR_EXECUTE_CREATE_FAILED    : // (710)
      return "D3DERR_EXECUTE_CREATE_FAILED";//: // (710)
    case D3DERR_EXECUTE_DESTROY_FAILED   : // (711)
      return "D3DERR_EXECUTE_DESTROY_FAILED";//: // (711)
    case D3DERR_EXECUTE_LOCK_FAILED  : // (712)
      return "D3DERR_EXECUTE_LOCK_FAILED";//: // (712)
    case D3DERR_EXECUTE_UNLOCK_FAILED    : // (713)
      return "D3DERR_EXECUTE_UNLOCK_FAILED";//: // (713)
    case D3DERR_EXECUTE_LOCKED       : // (714)
      return "D3DERR_EXECUTE_LOCKED";//: // (714)
    case D3DERR_EXECUTE_NOT_LOCKED   : // (715)
      return "D3DERR_EXECUTE_NOT_LOCKED";//: // (715)
    case D3DERR_EXECUTE_FAILED       : // (716)
      return "D3DERR_EXECUTE_FAILED";//: // (716)
    case D3DERR_EXECUTE_CLIPPED_FAILED   : // (717)
      return "D3DERR_EXECUTE_CLIPPED_FAILED";//: // (717)
    case D3DERR_TEXTURE_NO_SUPPORT   : // (720)
      return "D3DERR_TEXTURE_NO_SUPPORT";//: // (720)
    case D3DERR_TEXTURE_CREATE_FAILED    : // (721)
      return "D3DERR_TEXTURE_CREATE_FAILED";//: // (721)
    case D3DERR_TEXTURE_DESTROY_FAILED   : // (722)
      return "D3DERR_TEXTURE_DESTROY_FAILED";//: // (722)
    case D3DERR_TEXTURE_LOCK_FAILED  : // (723)
      return "D3DERR_TEXTURE_LOCK_FAILED";//: // (723)
    case D3DERR_TEXTURE_UNLOCK_FAILED    : // (724)
      return "D3DERR_TEXTURE_UNLOCK_FAILED";//: // (724)
    case D3DERR_TEXTURE_LOAD_FAILED  : // (725)
      return "D3DERR_TEXTURE_LOAD_FAILED";//: // (725)
    case D3DERR_TEXTURE_SWAP_FAILED  : // (726)
      return "D3DERR_TEXTURE_SWAP_FAILED";//: // (726)
    case D3DERR_TEXTURE_LOCKED       : // (727)
      return "D3DERR_TEXTURE_LOCKED";//: // (727)
    case D3DERR_TEXTURE_NOT_LOCKED   : // (728)
      return "D3DERR_TEXTURE_NOT_LOCKED";//: // (728)
    case D3DERR_TEXTURE_GETSURF_FAILED   : // (729)
      return "D3DERR_TEXTURE_GETSURF_FAILED";//: // (729)
    case D3DERR_MATRIX_CREATE_FAILED : // (730)
      return "D3DERR_MATRIX_CREATE_FAILED";//: // (730)
    case D3DERR_MATRIX_DESTROY_FAILED    : // (731)
      return "D3DERR_MATRIX_DESTROY_FAILED";//: // (731)
    case D3DERR_MATRIX_SETDATA_FAILED    : // (732)
      return "D3DERR_MATRIX_SETDATA_FAILED";//: // (732)
    case D3DERR_MATRIX_GETDATA_FAILED    : // (733)
      return "D3DERR_MATRIX_GETDATA_FAILED";//: // (733)
    case D3DERR_SETVIEWPORTDATA_FAILED   : // (734)
      return "D3DERR_SETVIEWPORTDATA_FAILED";//: // (734)
    case D3DERR_INVALIDCURRENTVIEWPORT   : // (735)
      return "D3DERR_INVALIDCURRENTVIEWPORT";//: // (735)
    case D3DERR_INVALIDPRIMITIVETYPE     : // (736)
      return "D3DERR_INVALIDPRIMITIVETYPE";//: // (736)
    case D3DERR_INVALIDVERTEXTYPE        : // (737)
      return "D3DERR_INVALIDVERTEXTYPE";//: // (737)
    case D3DERR_TEXTURE_BADSIZE          : // (738)
      return "D3DERR_TEXTURE_BADSIZE";//: // (738)
    case D3DERR_INVALIDRAMPTEXTURE       : // (739)
      return "D3DERR_INVALIDRAMPTEXTURE";//: // (739)
    case D3DERR_MATERIAL_CREATE_FAILED   : // (740)
      return "D3DERR_MATERIAL_CREATE_FAILED";//: // (740)
    case D3DERR_MATERIAL_DESTROY_FAILED  : // (741)
      return "D3DERR_MATERIAL_DESTROY_FAILED";//: // (741)
    case D3DERR_MATERIAL_SETDATA_FAILED  : // (742)
      return "D3DERR_MATERIAL_SETDATA_FAILED";//: // (742)
    case D3DERR_MATERIAL_GETDATA_FAILED  : // (743)
      return "D3DERR_MATERIAL_GETDATA_FAILED";//: // (743)
    case D3DERR_INVALIDPALETTE           : // (744)
      return "D3DERR_INVALIDPALETTE";//: // (744)
    case D3DERR_ZBUFF_NEEDS_SYSTEMMEMORY : // (745)
      return "D3DERR_ZBUFF_NEEDS_SYSTEMMEMORY";//: // (745)
    case D3DERR_ZBUFF_NEEDS_VIDEOMEMORY  : // (746)
      return "D3DERR_ZBUFF_NEEDS_VIDEOMEMORY";//: // (746)
    case D3DERR_SURFACENOTINVIDMEM       : // (747)
      return "D3DERR_SURFACENOTINVIDMEM";//: // (747)
    case D3DERR_LIGHT_SET_FAILED     : // (750)
      return "D3DERR_LIGHT_SET_FAILED";//: // (750)
    case D3DERR_LIGHTHASVIEWPORT     : // (751)
      return "D3DERR_LIGHTHASVIEWPORT";//: // (751)
    case D3DERR_LIGHTNOTINTHISVIEWPORT           : // (752)
      return "D3DERR_LIGHTNOTINTHISVIEWPORT";//: // (752)
    case D3DERR_SCENE_IN_SCENE       : // (760)
      return "D3DERR_SCENE_IN_SCENE";//: // (760)
    case D3DERR_SCENE_NOT_IN_SCENE   : // (761)
      return "D3DERR_SCENE_NOT_IN_SCENE";//: // (761)
    case D3DERR_SCENE_BEGIN_FAILED   : // (762)
      return "D3DERR_SCENE_BEGIN_FAILED";//: // (762)
    case D3DERR_SCENE_END_FAILED     : // (763)
      return "D3DERR_SCENE_END_FAILED";//: // (763)
    case D3DERR_INBEGIN                  : // (770)
      return "D3DERR_INBEGIN";//: // (770)
    case D3DERR_NOTINBEGIN               : // (771)
      return "D3DERR_NOTINBEGIN";//: // (771)
    case D3DERR_NOVIEWPORTS              : // (772)
      return "D3DERR_NOVIEWPORTS";//: // (772)
    case D3DERR_VIEWPORTDATANOTSET       : // (773)
      return "D3DERR_VIEWPORTDATANOTSET";//: // (773)
    case D3DERR_VIEWPORTHASNODEVICE      : // (774)
      return "D3DERR_VIEWPORTHASNODEVICE";//: // (774)
    case D3DERR_NOCURRENTVIEWPORT        : // (775)
      return "D3DERR_NOCURRENTVIEWPORT";//: // (775)
    case D3DERR_INVALIDVERTEXFORMAT              : // (2048)
      return "D3DERR_INVALIDVERTEXFORMAT";//: // (2048)
    case D3DERR_COLORKEYATTACHED                 : // (2050)
      return "D3DERR_COLORKEYATTACHED";//: // (2050)
    case D3DERR_VERTEXBUFFEROPTIMIZED            : // (2060)
      return "D3DERR_VERTEXBUFFEROPTIMIZED";//: // (2060)
    case D3DERR_VBUF_CREATE_FAILED               : // (2061)
      return "D3DERR_VBUF_CREATE_FAILED";//: // (2061)
    case D3DERR_VERTEXBUFFERLOCKED               : // (2062)
      return "D3DERR_VERTEXBUFFERLOCKED";//: // (2062)
    case D3DERR_ZBUFFER_NOTPRESENT               : // (2070)
      return "D3DERR_ZBUFFER_NOTPRESENT";//: // (2070)
    case D3DERR_STENCILBUFFER_NOTPRESENT         : // (2071)
      return "D3DERR_STENCILBUFFER_NOTPRESENT";//: // (2071)
    case D3DERR_WRONGTEXTUREFORMAT               : // (2072)
      return "D3DERR_WRONGTEXTUREFORMAT";//: // (2072)
    case D3DERR_UNSUPPORTEDCOLOROPERATION        : // (2073)
      return "D3DERR_UNSUPPORTEDCOLOROPERATION";//: // (2073)
    case D3DERR_UNSUPPORTEDCOLORARG              : // (2074)
      return "D3DERR_UNSUPPORTEDCOLORARG";//: // (2074)
    case D3DERR_UNSUPPORTEDALPHAOPERATION        : // (2075)
      return "D3DERR_UNSUPPORTEDALPHAOPERATION";//: // (2075)
    case D3DERR_UNSUPPORTEDALPHAARG              : // (2076)
      return "D3DERR_UNSUPPORTEDALPHAARG";//: // (2076)
    case D3DERR_TOOMANYOPERATIONS                : // (2077)
      return "D3DERR_TOOMANYOPERATIONS";//: // (2077)
    case D3DERR_CONFLICTINGTEXTUREFILTER         : // (2078)
      return "D3DERR_CONFLICTINGTEXTUREFILTER";//: // (2078)
    case D3DERR_UNSUPPORTEDFACTORVALUE           : // (2079)
      return "D3DERR_UNSUPPORTEDFACTORVALUE";//: // (2079)
    case D3DERR_CONFLICTINGRENDERSTATE           : // (2081)
      return "D3DERR_CONFLICTINGRENDERSTATE";//: // (2081)
    case D3DERR_UNSUPPORTEDTEXTUREFILTER         : // (2082)
      return "D3DERR_UNSUPPORTEDTEXTUREFILTER";//: // (2082)
    case D3DERR_TOOMANYPRIMITIVES                : // (2083)
      return "D3DERR_TOOMANYPRIMITIVES";//: // (2083)
    case D3DERR_INVALIDMATRIX                    : // (2084)
      return "D3DERR_INVALIDMATRIX";//: // (2084)
    case D3DERR_TOOMANYVERTICES                  : // (2085)
      return "D3DERR_TOOMANYVERTICES";//: // (2085)
    case D3DERR_CONFLICTINGTEXTUREPALETTE        : // (2086)
      return "D3DERR_CONFLICTINGTEXTUREPALETTE";//: // (2086)
    case D3DERR_VERTEXBUFFERUNLOCKFAILED         : // (2063)
      return "D3DERR_VERTEXBUFFERUNLOCKFAILED";//: // (2063)
    case D3DERR_INVALIDSTATEBLOCK        : // (2100)
      return "D3DERR_INVALIDSTATEBLOCK";//: // (2100)
    case D3DERR_INBEGINSTATEBLOCK        : // (2101)
      return "D3DERR_INBEGINSTATEBLOCK";//: // (2101)
    case D3DERR_NOTINBEGINSTATEBLOCK     : // (2102)
      return "D3DERR_NOTINBEGINSTATEBLOCK";//: // (2102)
      //case D3DERR_INOVERLAYSTATEBLOCK      : // (2103)
      //  return "D3DERR_INOVERLAYSTATEBLOCK";//: // (2103)
    case DDERR_NOSTEREOHARDWARE       : // ( 181 )
      return "DDERR_NOSTEREOHARDWARE";//: // ( 181 )
    case DDERR_NOSURFACELEFT              : // ( 182 )
      return "DDERR_NOSURFACELEFT";//: // ( 182 )
    case DDERR_DDSCAPSCOMPLEXREQUIRED            : // ( 542 )
      return "DDERR_DDSCAPSCOMPLEXREQUIRED";//: // ( 542 )
    case DDERR_NOTONMIPMAPSUBLEVEL               : // ( 603 )
      return "DDERR_NOTONMIPMAPSUBLEVEL";//: // ( 603 )
    case DDERR_TESTFINISHED                      : // ( 692 )
      return "DDERR_TESTFINISHED";//: // ( 692 )
    case DDERR_NEWMODE                           : // ( 693 )
      return "DDERR_NEWMODE";//: // ( 693 )
      //#endif
      //case D3DERR_COMMAND_UNPARSED              : // (3000)
      /// return "case";//D3DERR_COMMAND_UNPARSED              : // (3000)

    case DDERR_ALREADYINITIALIZED     : // ( 5 )
      return "DDERR_ALREADYINITIALIZED";//: // ( 5 )
    case DDERR_CANNOTATTACHSURFACE        : // ( 10 )
      return "DDERR_CANNOTATTACHSURFACE";//: // ( 10 )
    case DDERR_CANNOTDETACHSURFACE        : // ( 20 )
      return "DDERR_CANNOTDETACHSURFACE";//: // ( 20 )
    case DDERR_CURRENTLYNOTAVAIL          : // ( 40 )
      return "DDERR_CURRENTLYNOTAVAIL";//: // ( 40 )
    case DDERR_EXCEPTION              : // ( 55 )
      return "DDERR_EXCEPTION";//: // ( 55 )
    case DDERR_HEIGHTALIGN            : // ( 90 )
      return "DDERR_HEIGHTALIGN";//: // ( 90 )
    case DDERR_INCOMPATIBLEPRIMARY        : // ( 95 )
      return "DDERR_INCOMPATIBLEPRIMARY";//: // ( 95 )
    case DDERR_INVALIDCAPS            : // ( 100 )
      return "DDERR_INVALIDCAPS";//: // ( 100 )
    case DDERR_INVALIDCLIPLIST            : // ( 110 )
      return "DDERR_INVALIDCLIPLIST";//: // ( 110 )
    case DDERR_INVALIDMODE            : // ( 120 )
      return "DDERR_INVALIDMODE";//: // ( 120 )
    case DDERR_INVALIDOBJECT          : // ( 130 )
      return "DDERR_INVALIDOBJECT";//: // ( 130 )
    case DDERR_INVALIDPIXELFORMAT     : // ( 145 )
      return "DDERR_INVALIDPIXELFORMAT";//: // ( 145 )
    case DDERR_INVALIDRECT            : // ( 150 )
      return "DDERR_INVALIDRECT";//: // ( 150 )
    case DDERR_LOCKEDSURFACES         : // ( 160 )
      return "DDERR_LOCKEDSURFACES";//: // ( 160 )
    case DDERR_NO3D               : // ( 170 )
      return "DDERR_NO3D";//: // ( 170 )
    case DDERR_NOALPHAHW              : // ( 180 )
      return "DDERR_NOALPHAHW";//: // ( 180 )
    case DDERR_NOCLIPLIST         : // ( 205 )
      return "DDERR_NOCLIPLIST";//: // ( 205 )
    case DDERR_NOCOLORCONVHW          : // ( 210 )
      return "DDERR_NOCOLORCONVHW";//: // ( 210 )
    case DDERR_NOCOOPERATIVELEVELSET      : // ( 212 )
      return "DDERR_NOCOOPERATIVELEVELSET";//: // ( 212 )
    case DDERR_NOCOLORKEY         : // ( 215 )
      return "DDERR_NOCOLORKEY";//: // ( 215 )
    case DDERR_NOCOLORKEYHW           : // ( 220 )
      return "DDERR_NOCOLORKEYHW";//: // ( 220 )
    case DDERR_NODIRECTDRAWSUPPORT        : // ( 222 )
      return "DDERR_NODIRECTDRAWSUPPORT";//: // ( 222 )
    case DDERR_NOEXCLUSIVEMODE            : // ( 225 )
      return "DDERR_NOEXCLUSIVEMODE";//: // ( 225 )
    case DDERR_NOFLIPHW               : // ( 230 )
      return "DDERR_NOFLIPHW";//: // ( 230 )
    case DDERR_NOGDI              : // ( 240 )
      return "DDERR_NOGDI";//: // ( 240 )
    case DDERR_NOMIRRORHW         : // ( 250 )
      return "DDERR_NOMIRRORHW";//: // ( 250 )
    case DDERR_NOTFOUND               : // ( 255 )
      return "DDERR_NOTFOUND";//: // ( 255 )
    case DDERR_NOOVERLAYHW            : // ( 260 )
      return "DDERR_NOOVERLAYHW";//: // ( 260 )
    case DDERR_OVERLAPPINGRECTS           : // ( 270 )
      return "DDERR_OVERLAPPINGRECTS";//: // ( 270 )
    case DDERR_NORASTEROPHW           : // ( 280 )
      return "DDERR_NORASTEROPHW";//: // ( 280 )
    case DDERR_NOROTATIONHW           : // ( 290 )
      return "DDERR_NOROTATIONHW";//: // ( 290 )
    case DDERR_NOSTRETCHHW            : // ( 310 )
      return "DDERR_NOSTRETCHHW";//: // ( 310 )
    case DDERR_NOT4BITCOLOR           : // ( 316 )
      return "DDERR_NOT4BITCOLOR";//: // ( 316 )
    case DDERR_NOT4BITCOLORINDEX          : // ( 317 )
      return "DDERR_NOT4BITCOLORINDEX";//: // ( 317 )
    case DDERR_NOT8BITCOLOR           : // ( 320 )
      return "DDERR_NOT8BITCOLOR";//: // ( 320 )
    case DDERR_NOTEXTUREHW            : // ( 330 )
      return "DDERR_NOTEXTUREHW";//: // ( 330 )
    case DDERR_NOVSYNCHW              : // ( 335 )
      return "DDERR_NOVSYNCHW";//: // ( 335 )
    case DDERR_NOZBUFFERHW            : // ( 340 )
      return "DDERR_NOZBUFFERHW";//: // ( 340 )
    case DDERR_NOZOVERLAYHW           : // ( 350 )
      return "DDERR_NOZOVERLAYHW";//: // ( 350 )
    case DDERR_OUTOFCAPS              : // ( 360 )
      return "DDERR_OUTOFCAPS";//: // ( 360 )
    case DDERR_OUTOFVIDEOMEMORY           : // ( 380 )
      return "DDERR_OUTOFVIDEOMEMORY";//: // ( 380 )
    case DDERR_OVERLAYCANTCLIP            : // ( 382 )
      return "DDERR_OVERLAYCANTCLIP";//: // ( 382 )
    case DDERR_OVERLAYCOLORKEYONLYONEACTIVE   : // ( 384 )
      return "DDERR_OVERLAYCOLORKEYONLYONEACTIVE";//: // ( 384 )
    case DDERR_PALETTEBUSY            : // ( 387 )
      return "DDERR_PALETTEBUSY";//: // ( 387 )
    case DDERR_COLORKEYNOTSET         : // ( 400 )
      return "DDERR_COLORKEYNOTSET";//: // ( 400 )
    case DDERR_SURFACEALREADYATTACHED     : // ( 410 )
      return "DDERR_SURFACEALREADYATTACHED";//: // ( 410 )
    case DDERR_SURFACEALREADYDEPENDENT        : // ( 420 )
      return "DDERR_SURFACEALREADYDEPENDENT";//: // ( 420 )
    case DDERR_SURFACEBUSY            : // ( 430 )
      return "DDERR_SURFACEBUSY";//: // ( 430 )
    case DDERR_CANTLOCKSURFACE                   : // ( 435 )
      return "DDERR_CANTLOCKSURFACE";//: // ( 435 )
    case DDERR_SURFACEISOBSCURED          : // ( 440 )
      return "DDERR_SURFACEISOBSCURED";//: // ( 440 )
    case DDERR_SURFACELOST            : // ( 450 )
      return "DDERR_SURFACELOST";//: // ( 450 )
    case DDERR_SURFACENOTATTACHED     : // ( 460 )
      return "DDERR_SURFACENOTATTACHED";//: // ( 460 )
    case DDERR_TOOBIGHEIGHT           : // ( 470 )
      return "DDERR_TOOBIGHEIGHT";//: // ( 470 )
    case DDERR_TOOBIGSIZE         : // ( 480 )
      return "DDERR_TOOBIGSIZE";//: // ( 480 )
    case DDERR_TOOBIGWIDTH            : // ( 490 )
      return "DDERR_TOOBIGWIDTH";//: // ( 490 )
    case DDERR_UNSUPPORTEDFORMAT          : // ( 510 )
      return "DDERR_UNSUPPORTEDFORMAT";//: // ( 510 )
    case DDERR_UNSUPPORTEDMASK            : // ( 520 )
      return "DDERR_UNSUPPORTEDMASK";//: // ( 520 )
    case DDERR_INVALIDSTREAM                     : // ( 521 )
      return "DDERR_INVALIDSTREAM";//: // ( 521 )
    case DDERR_VERTICALBLANKINPROGRESS        : // ( 537 )
      return "DDERR_VERTICALBLANKINPROGRESS";//: // ( 537 )
    case DDERR_WASSTILLDRAWING            : // ( 540 )
      return "DDERR_WASSTILLDRAWING";//: // ( 540 )
    case DDERR_XALIGN             : // ( 560 )
      return "DDERR_XALIGN";//: // ( 560 )
    case DDERR_INVALIDDIRECTDRAWGUID      : // ( 561 )
      return "DDERR_INVALIDDIRECTDRAWGUID";//: // ( 561 )
    case DDERR_DIRECTDRAWALREADYCREATED       : // ( 562 )
      return "DDERR_DIRECTDRAWALREADYCREATED";//: // ( 562 )
    case DDERR_NODIRECTDRAWHW         : // ( 563 )
      return "DDERR_NODIRECTDRAWHW";//: // ( 563 )
    case DDERR_PRIMARYSURFACEALREADYEXISTS    : // ( 564 )
      return "DDERR_PRIMARYSURFACEALREADYEXISTS";//: // ( 564 )
    case DDERR_NOEMULATION            : // ( 565 )
      return "DDERR_NOEMULATION";//: // ( 565 )
    case DDERR_REGIONTOOSMALL         : // ( 566 )
      return "DDERR_REGIONTOOSMALL";//: // ( 566 )
    case DDERR_CLIPPERISUSINGHWND     : // ( 567 )
      return "DDERR_CLIPPERISUSINGHWND";//: // ( 567 )
    case DDERR_NOCLIPPERATTACHED          : // ( 568 )
      return "DDERR_NOCLIPPERATTACHED";//: // ( 568 )
    case DDERR_NOHWND             : // ( 569 )
      return "DDERR_NOHWND";//: // ( 569 )
    case DDERR_HWNDSUBCLASSED         : // ( 570 )
      return "DDERR_HWNDSUBCLASSED";//: // ( 570 )
    case DDERR_HWNDALREADYSET         : // ( 571 )
      return "DDERR_HWNDALREADYSET";//: // ( 571 )
    case DDERR_NOPALETTEATTACHED          : // ( 572 )
      return "DDERR_NOPALETTEATTACHED";//: // ( 572 )
    case DDERR_NOPALETTEHW            : // ( 573 )
      return "DDERR_NOPALETTEHW";//: // ( 573 )
    case DDERR_BLTFASTCANTCLIP            : // ( 574 )
      return "DDERR_BLTFASTCANTCLIP";//: // ( 574 )
    case DDERR_NOBLTHW                : // ( 575 )
      return "DDERR_NOBLTHW";//: // ( 575 )
    case DDERR_NODDROPSHW         : // ( 576 )
      return "DDERR_NODDROPSHW";//: // ( 576 )
    case DDERR_OVERLAYNOTVISIBLE          : // ( 577 )
      return "DDERR_OVERLAYNOTVISIBLE";//: // ( 577 )
    case DDERR_NOOVERLAYDEST          : // ( 578 )
      return "DDERR_NOOVERLAYDEST";//: // ( 578 )
    case DDERR_INVALIDPOSITION            : // ( 579 )
      return "DDERR_INVALIDPOSITION";//: // ( 579 )
    case DDERR_NOTAOVERLAYSURFACE     : // ( 580 )
      return "DDERR_NOTAOVERLAYSURFACE";//: // ( 580 )
    case DDERR_EXCLUSIVEMODEALREADYSET        : // ( 581 )
      return "DDERR_EXCLUSIVEMODEALREADYSET";//: // ( 581 )
    case DDERR_NOTFLIPPABLE           : // ( 582 )
      return "DDERR_NOTFLIPPABLE";//: // ( 582 )
    case DDERR_CANTDUPLICATE          : // ( 583 )
      return "DDERR_CANTDUPLICATE";//: // ( 583 )
    case DDERR_NOTLOCKED              : // ( 584 )
      return "DDERR_NOTLOCKED";//: // ( 584 )
    case DDERR_CANTCREATEDC           : // ( 585 )
      return "DDERR_CANTCREATEDC";//: // ( 585 )
    case DDERR_NODC               : // ( 586 )
      return "DDERR_NODC";//: // ( 586 )
    case DDERR_WRONGMODE              : // ( 587 )
      return "DDERR_WRONGMODE";//: // ( 587 )
    case DDERR_IMPLICITLYCREATED          : // ( 588 )
      return "DDERR_IMPLICITLYCREATED";//: // ( 588 )
    case DDERR_NOTPALETTIZED          : // ( 589 )
      return "DDERR_NOTPALETTIZED";//: // ( 589 )
    case DDERR_UNSUPPORTEDMODE            : // ( 590 )
      return "DDERR_UNSUPPORTEDMODE";//: // ( 590 )
    case DDERR_NOMIPMAPHW         : // ( 591 )
      return "DDERR_NOMIPMAPHW";//: // ( 591 )
    case DDERR_INVALIDSURFACETYPE                : // ( 592 )
      return "DDERR_INVALIDSURFACETYPE";//: // ( 592 )
    case DDERR_NOOPTIMIZEHW                      : // ( 600 )
      return "DDERR_NOOPTIMIZEHW";//: // ( 600 )
    case DDERR_NOTLOADED                         : // ( 601 )
      return "DDERR_NOTLOADED";//: // ( 601 )
    case DDERR_NOFOCUSWINDOW                     : // ( 602 )
      return "DDERR_NOFOCUSWINDOW";//: // ( 602 )
    case DDERR_DCALREADYCREATED           : // ( 620 )
      return "DDERR_DCALREADYCREATED";//: // ( 620 )
    case DDERR_NONONLOCALVIDMEM                  : // ( 630 )
      return "DDERR_NONONLOCALVIDMEM";//: // ( 630 )
    case DDERR_CANTPAGELOCK           : // ( 640 )
      return "DDERR_CANTPAGELOCK";//: // ( 640 )
    case DDERR_CANTPAGEUNLOCK         : // ( 660 )
      return "DDERR_CANTPAGEUNLOCK";//: // ( 660 )
    case DDERR_NOTPAGELOCKED          : // ( 680 )
      return "DDERR_NOTPAGELOCKED";//: // ( 680 )
    case DDERR_MOREDATA                   : // ( 690 )
      return "DDERR_MOREDATA";//: // ( 690 )
    case DDERR_EXPIRED                           : // ( 691 )
      return "DDERR_EXPIRED";//: // ( 691 )
    case DDERR_VIDEONOTACTIVE             : // ( 695 )
      return "DDERR_VIDEONOTACTIVE";//: // ( 695 )
    case DDERR_DEVICEDOESNTOWNSURFACE         : // ( 699 )
      return "DDERR_DEVICEDOESNTOWNSURFACE";//: // ( 699 )
      /*
    case DXFILEERR_BADOBJECT                 : // (850)
    return "DXFILEERR_BADOBJECT";//: // (850)
    case DXFILEERR_BADVALUE                  : // (851)
    return "DXFILEERR_BADVALUE";//: // (851)
    case DXFILEERR_BADTYPE                   : // (852)
    return "DXFILEERR_BADTYPE";//: // (852)
    case DXFILEERR_BADSTREAMHANDLE           : // (853)
    return "DXFILEERR_BADSTREAMHANDLE";//: // (853)
    case DXFILEERR_BADALLOC                  : // (854)
    return "DXFILEERR_BADALLOC";//: // (854)
    case DXFILEERR_NOTFOUND                  : // (855)
    return "DXFILEERR_NOTFOUND";//: // (855)
    case DXFILEERR_NOTDONEYET                : // (856)
    return "DXFILEERR_NOTDONEYET";//: // (856)
    case DXFILEERR_FILENOTFOUND              : // (857)
    return "DXFILEERR_FILENOTFOUND";//: // (857)
    case DXFILEERR_RESOURCENOTFOUND          : // (858)
    return "DXFILEERR_RESOURCENOTFOUND";//: // (858)
    case DXFILEERR_URLNOTFOUND               : // (859)
    return "DXFILEERR_URLNOTFOUND";//: // (859)
    case DXFILEERR_BADRESOURCE               : // (860)
    return "DXFILEERR_BADRESOURCE";//: // (860)
    case DXFILEERR_BADFILETYPE               : // (861)
    return "DXFILEERR_BADFILETYPE";//: // (861)
    case DXFILEERR_BADFILEVERSION            : // (862)
    return "DXFILEERR_BADFILEVERSION";//: // (862)
    case DXFILEERR_BADFILEFLOATSIZE          : // (863)
    return "DXFILEERR_BADFILEFLOATSIZE";//: // (863)
    case DXFILEERR_BADFILECOMPRESSIONTYPE    : // (864)
    return "DXFILEERR_BADFILECOMPRESSIONTYPE";//: // (864)
    case DXFILEERR_BADFILE                   : // (865)
    return "DXFILEERR_BADFILE";//: // (865)
    case DXFILEERR_PARSEERROR                : // (866)
    return "DXFILEERR_PARSEERROR";//: // (866)
    case DXFILEERR_NOTEMPLATE                : // (867)
    return "DXFILEERR_NOTEMPLATE";//: // (867)
    case DXFILEERR_BADARRAYSIZE              : // (868)
    return "DXFILEERR_BADARRAYSIZE";//: // (868)
    case DXFILEERR_BADDATAREFERENCE          : // (869)
    return "DXFILEERR_BADDATAREFERENCE";//: // (869)
    case DXFILEERR_INTERNALERROR             : // (870)
    return "DXFILEERR_INTERNALERROR";//: // (870)
    case DXFILEERR_NOMOREOBJECTS             : // (871)
    return "DXFILEERR_NOMOREOBJECTS";//: // (871)
    case DXFILEERR_BADINTRINSICS             : // (872)
    return "DXFILEERR_BADINTRINSICS";//: // (872)
    case DXFILEERR_NOMORESTREAMHANDLES       : // (873)
    return "DXFILEERR_NOMORESTREAMHANDLES";//: // (873)
    case DXFILEERR_NOMOREDATA                : // (874)
    return "DXFILEERR_NOMOREDATA";//: // (874)
    case DXFILEERR_BADCACHEFILE              : // (875)
    return "DXFILEERR_BADCACHEFILE";//: // (875)
    case DXFILEERR_NOINTERNET                : // (876)
    return "DXFILEERR_NOINTERNET";//: // (876)
      */
    case E_UNEXPECTED                     :
      return "E_UNEXPECTED";
    case E_NOTIMPL                        :
      return "E_NOTIMPL";
    case E_OUTOFMEMORY                    :
      return "E_OUTOFMEMORY";
    case E_INVALIDARG                     :
      return "E_INVALIDARG or DDERR_INVALIDPARAMS";
    case E_NOINTERFACE                    :
      return "E_NOINTERFACE";
    case E_POINTER                        :
      return "E_POINTER";
    case E_HANDLE                         :
      return "E_HANDLE";
    case E_ABORT                          :
      return "E_ABORT";
      //    case E_FAIL                           :
      //    return "E_FAIL";
    case E_ACCESSDENIED                   :
      return "E_ACCESSDENIED";
    case E_PENDING                        :
      return "E_PENDING";
    case CO_E_INIT_TLS                    :
      return "CO_E_INIT_TLS";
    case CO_E_INIT_SHARED_ALLOCATOR       :
      return "CO_E_INIT_SHARED_ALLOCATOR";
    case CO_E_INIT_MEMORY_ALLOCATOR       :
      return "CO_E_INIT_MEMORY_ALLOCATOR";
    case CO_E_INIT_CLASS_CACHE            :
      return "CO_E_INIT_CLASS_CACHE";
    case CO_E_INIT_RPC_CHANNEL            :
      return "CO_E_INIT_RPC_CHANNEL";
    case CO_E_INIT_TLS_SET_CHANNEL_CONTROL :
      return "CO_E_INIT_TLS_SET_CHANNEL_CONTROL";
    case CO_E_INIT_TLS_CHANNEL_CONTROL    :
      return "CO_E_INIT_TLS_CHANNEL_CONTROL";
    case CO_E_INIT_UNACCEPTED_USER_ALLOCATOR :
      return "CO_E_INIT_UNACCEPTED_USER_ALLOCATOR";
    case CO_E_INIT_SCM_MUTEX_EXISTS       :
      return "CO_E_INIT_SCM_MUTEX_EXISTS";
    case CO_E_INIT_SCM_FILE_MAPPING_EXISTS :
      return "CO_E_INIT_SCM_FILE_MAPPING_EXISTS";
    case CO_E_INIT_SCM_MAP_VIEW_OF_FILE   :
      return "CO_E_INIT_SCM_MAP_VIEW_OF_FILE";
    case CO_E_INIT_SCM_EXEC_FAILURE       :
      return "CO_E_INIT_SCM_EXEC_FAILURE";
    case CO_E_INIT_ONLY_SINGLE_THREADED   :
      return "CO_E_INIT_ONLY_SINGLE_THREADED";
    case CO_E_CANT_REMOTE                 :
      return "CO_E_CANT_REMOTE";
    case CO_E_BAD_SERVER_NAME             :
      return "CO_E_BAD_SERVER_NAME";
    case CO_E_WRONG_SERVER_IDENTITY       :
      return "CO_E_WRONG_SERVER_IDENTITY";
    case CO_E_OLE1DDE_DISABLED            :
      return "CO_E_OLE1DDE_DISABLED";
    case CO_E_RUNAS_SYNTAX                :
      return "CO_E_RUNAS_SYNTAX";
    case CO_E_CREATEPROCESS_FAILURE       :
      return "CO_E_CREATEPROCESS_FAILURE";
    case CO_E_RUNAS_CREATEPROCESS_FAILURE :
      return "CO_E_RUNAS_CREATEPROCESS_FAILURE";
    case CO_E_RUNAS_LOGON_FAILURE         :
      return "CO_E_RUNAS_LOGON_FAILURE";
    case CO_E_LAUNCH_PERMSSION_DENIED     :
      return "CO_E_LAUNCH_PERMSSION_DENIED";
    case CO_E_START_SERVICE_FAILURE       :
      return "CO_E_START_SERVICE_FAILURE";
    case CO_E_REMOTE_COMMUNICATION_FAILURE :
      return "CO_E_REMOTE_COMMUNICATION_FAILURE";
    case CO_E_SERVER_START_TIMEOUT        :
      return "CO_E_SERVER_START_TIMEOUT";
    case CO_E_CLSREG_INCONSISTENT         :
      return "CO_E_CLSREG_INCONSISTENT";
    case CO_E_IIDREG_INCONSISTENT         :
      return "CO_E_IIDREG_INCONSISTENT";
    case CO_E_NOT_SUPPORTED               :
      return "CO_E_NOT_SUPPORTED";
    case CO_E_RELOAD_DLL                  :
      return "CO_E_RELOAD_DLL";
    case CO_E_MSI_ERROR                   :
      return "CO_E_MSI_ERROR";
    case OLE_E_OLEVERB                    :
      return "OLE_E_OLEVERB";
    case OLE_E_ADVF                       :
      return "OLE_E_ADVF";
    case OLE_E_ENUM_NOMORE                :
      return "OLE_E_ENUM_NOMORE";
    case OLE_E_ADVISENOTSUPPORTED         :
      return "OLE_E_ADVISENOTSUPPORTED";
    case OLE_E_NOCONNECTION               :
      return "OLE_E_NOCONNECTION";
    case OLE_E_NOTRUNNING                 :
      return "OLE_E_NOTRUNNING";
    case OLE_E_NOCACHE                    :
      return "OLE_E_NOCACHE";
    case OLE_E_BLANK                      :
      return "OLE_E_BLANK";
    case OLE_E_CLASSDIFF                  :
      return "OLE_E_CLASSDIFF";
    case OLE_E_CANT_GETMONIKER            :
      return "OLE_E_CANT_GETMONIKER";
    case OLE_E_CANT_BINDTOSOURCE          :
      return "OLE_E_CANT_BINDTOSOURCE";
    case OLE_E_STATIC                     :
      return "OLE_E_STATIC";
    case OLE_E_PROMPTSAVECANCELLED        :
      return "OLE_E_PROMPTSAVECANCELLED";
    case OLE_E_INVALIDRECT                :
      return "OLE_E_INVALIDRECT";
    case OLE_E_WRONGCOMPOBJ               :
      return "OLE_E_WRONGCOMPOBJ";
    case OLE_E_INVALIDHWND                :
      return "OLE_E_INVALIDHWND";
    case OLE_E_NOT_INPLACEACTIVE          :
      return "OLE_E_NOT_INPLACEACTIVE";
    case OLE_E_CANTCONVERT                :
      return "OLE_E_CANTCONVERT";
    case OLE_E_NOSTORAGE                  :
      return "OLE_E_NOSTORAGE";
    case DV_E_FORMATETC                   :
      return "DV_E_FORMATETC";
    case DV_E_DVTARGETDEVICE              :
      return "DV_E_DVTARGETDEVICE";
    case DV_E_STGMEDIUM                   :
      return "DV_E_STGMEDIUM";
    case DV_E_STATDATA                    :
      return "DV_E_STATDATA";
    case DV_E_LINDEX                      :
      return "DV_E_LINDEX";
    case DV_E_TYMED                       :
      return "DV_E_TYMED";
    case DV_E_CLIPFORMAT                  :
      return "DV_E_CLIPFORMAT";
    case DV_E_DVASPECT                    :
      return "DV_E_DVASPECT";
    case DV_E_DVTARGETDEVICE_SIZE         :
      return "DV_E_DVTARGETDEVICE_SIZE";
    case DV_E_NOIVIEWOBJECT               :
      return "DV_E_NOIVIEWOBJECT";
    case DRAGDROP_E_NOTREGISTERED         :
      return "DRAGDROP_E_NOTREGISTERED";
    case DRAGDROP_E_ALREADYREGISTERED     :
      return "DRAGDROP_E_ALREADYREGISTERED";
    case DRAGDROP_E_INVALIDHWND           :
      return "DRAGDROP_E_INVALIDHWND";
    case CLASS_E_NOAGGREGATION            :
      return "CLASS_E_NOAGGREGATION";
    case CLASS_E_CLASSNOTAVAILABLE        :
      return "CLASS_E_CLASSNOTAVAILABLE";
    case CLASS_E_NOTLICENSED              :
      return "CLASS_E_NOTLICENSED";
    case VIEW_E_DRAW                      :
      return "VIEW_E_DRAW";
    case REGDB_E_READREGDB                :
      return "REGDB_E_READREGDB";
    case REGDB_E_WRITEREGDB               :
      return "REGDB_E_WRITEREGDB";
    case REGDB_E_KEYMISSING               :
      return "REGDB_E_KEYMISSING";
    case REGDB_E_INVALIDVALUE             :
      return "REGDB_E_INVALIDVALUE";
    case REGDB_E_CLASSNOTREG              :
      return "REGDB_E_CLASSNOTREG";
    case REGDB_E_IIDNOTREG                :
      return "REGDB_E_IIDNOTREG";
    case CAT_E_CATIDNOEXIST               :
      return "CAT_E_CATIDNOEXIST";
    case CAT_E_NODESCRIPTION              :
      return "CAT_E_NODESCRIPTION";
    case CS_E_PACKAGE_NOTFOUND            :
      return "CS_E_PACKAGE_NOTFOUND";
    case CS_E_NOT_DELETABLE               :
      return "CS_E_NOT_DELETABLE";
    case CS_E_CLASS_NOTFOUND              :
      return "CS_E_CLASS_NOTFOUND";
    case CS_E_INVALID_VERSION             :
      return "CS_E_INVALID_VERSION";
    case CS_E_NO_CLASSSTORE               :
      return "CS_E_NO_CLASSSTORE";
    case CACHE_E_NOCACHE_UPDATED          :
      return "CACHE_E_NOCACHE_UPDATED";
    case OLEOBJ_E_NOVERBS                 :
      return "OLEOBJ_E_NOVERBS";
    case OLEOBJ_E_INVALIDVERB             :
      return "OLEOBJ_E_INVALIDVERB";
    case INPLACE_E_NOTUNDOABLE            :
      return "INPLACE_E_NOTUNDOABLE";
    case INPLACE_E_NOTOOLSPACE            :
      return "INPLACE_E_NOTOOLSPACE";
    case CONVERT10_E_OLESTREAM_GET        :
      return "CONVERT10_E_OLESTREAM_GET";
    case CONVERT10_E_OLESTREAM_PUT        :
      return "CONVERT10_E_OLESTREAM_PUT";
    case CONVERT10_E_OLESTREAM_FMT        :
      return "CONVERT10_E_OLESTREAM_FMT";
    case CONVERT10_E_OLESTREAM_BITMAP_TO_DIB :
      return "CONVERT10_E_OLESTREAM_BITMAP_TO_DIB";
    case CONVERT10_E_STG_FMT              :
      return "CONVERT10_E_STG_FMT";
    case CONVERT10_E_STG_NO_STD_STREAM    :
      return "CONVERT10_E_STG_NO_STD_STREAM";
    case CONVERT10_E_STG_DIB_TO_BITMAP    :
      return "CONVERT10_E_STG_DIB_TO_BITMAP";
    case CLIPBRD_E_CANT_OPEN              :
      return "CLIPBRD_E_CANT_OPEN";
    case CLIPBRD_E_CANT_EMPTY             :
      return "CLIPBRD_E_CANT_EMPTY";
    case CLIPBRD_E_CANT_SET               :
      return "CLIPBRD_E_CANT_SET";
    case CLIPBRD_E_BAD_DATA               :
      return "CLIPBRD_E_BAD_DATA";
    case CLIPBRD_E_CANT_CLOSE             :
      return "CLIPBRD_E_CANT_CLOSE";
    case MK_E_CONNECTMANUALLY             :
      return "MK_E_CONNECTMANUALLY";
    case MK_E_EXCEEDEDDEADLINE            :
      return "MK_E_EXCEEDEDDEADLINE";
    case MK_E_NEEDGENERIC                 :
      return "MK_E_NEEDGENERIC";
    case MK_E_UNAVAILABLE                 :
      return "MK_E_UNAVAILABLE";
    case MK_E_SYNTAX                      :
      return "MK_E_SYNTAX";
    case MK_E_NOOBJECT                    :
      return "MK_E_NOOBJECT";
    case MK_E_INVALIDEXTENSION            :
      return "MK_E_INVALIDEXTENSION";
    case MK_E_INTERMEDIATEINTERFACENOTSUPPORTED :
      return "MK_E_INTERMEDIATEINTERFACENOTSUPPORTED";
    case MK_E_NOTBINDABLE                 :
      return "MK_E_NOTBINDABLE";
    case MK_E_NOTBOUND                    :
      return "MK_E_NOTBOUND";
    case MK_E_CANTOPENFILE                :
      return "MK_E_CANTOPENFILE";
    case MK_E_MUSTBOTHERUSER              :
      return "MK_E_MUSTBOTHERUSER";
    case MK_E_NOINVERSE                   :
      return "MK_E_NOINVERSE";
    case MK_E_NOSTORAGE                   :
      return "MK_E_NOSTORAGE";
    case MK_E_NOPREFIX                    :
      return "MK_E_NOPREFIX";
    case MK_E_ENUMERATION_FAILED          :
      return "MK_E_ENUMERATION_FAILED";
    case CO_E_NOTINITIALIZED              :
      return "CO_E_NOTINITIALIZED";
    case CO_E_ALREADYINITIALIZED          :
      return "CO_E_ALREADYINITIALIZED";
    case CO_E_CANTDETERMINECLASS          :
      return "CO_E_CANTDETERMINECLASS";
    case CO_E_CLASSSTRING                 :
      return "CO_E_CLASSSTRING";
    case CO_E_IIDSTRING                   :
      return "CO_E_IIDSTRING";
    case CO_E_APPNOTFOUND                 :
      return "CO_E_APPNOTFOUND";
    case CO_E_APPSINGLEUSE                :
      return "CO_E_APPSINGLEUSE";
    case CO_E_ERRORINAPP                  :
      return "CO_E_ERRORINAPP";
    case CO_E_DLLNOTFOUND                 :
      return "CO_E_DLLNOTFOUND";
    case CO_E_ERRORINDLL                  :
      return "CO_E_ERRORINDLL";
    case CO_E_WRONGOSFORAPP               :
      return "CO_E_WRONGOSFORAPP";
    case CO_E_OBJNOTREG                   :
      return "CO_E_OBJNOTREG";
    case CO_E_OBJISREG                    :
      return "CO_E_OBJISREG";
    case CO_E_OBJNOTCONNECTED             :
      return "CO_E_OBJNOTCONNECTED";
    case CO_E_APPDIDNTREG                 :
      return "CO_E_APPDIDNTREG";
    case CO_E_RELEASED                    :
      return "CO_E_RELEASED";
    case CO_E_FAILEDTOIMPERSONATE         :
      return "CO_E_FAILEDTOIMPERSONATE";
    case CO_E_FAILEDTOGETSECCTX           :
      return "CO_E_FAILEDTOGETSECCTX";
    case CO_E_FAILEDTOOPENTHREADTOKEN     :
      return "CO_E_FAILEDTOOPENTHREADTOKEN";
    case CO_E_FAILEDTOGETTOKENINFO        :
      return "CO_E_FAILEDTOGETTOKENINFO";
    case CO_E_TRUSTEEDOESNTMATCHCLIENT    :
      return "CO_E_TRUSTEEDOESNTMATCHCLIENT";
    case CO_E_FAILEDTOQUERYCLIENTBLANKET  :
      return "CO_E_FAILEDTOQUERYCLIENTBLANKET";
    case CO_E_FAILEDTOSETDACL             :
      return "CO_E_FAILEDTOSETDACL";
    case CO_E_ACCESSCHECKFAILED           :
      return "CO_E_ACCESSCHECKFAILED";
    case CO_E_NETACCESSAPIFAILED          :
      return "CO_E_NETACCESSAPIFAILED";
    case CO_E_WRONGTRUSTEENAMESYNTAX      :
      return "CO_E_WRONGTRUSTEENAMESYNTAX";
    case CO_E_INVALIDSID                  :
      return "CO_E_INVALIDSID";
    case CO_E_CONVERSIONFAILED            :
      return "CO_E_CONVERSIONFAILED";
    case CO_E_NOMATCHINGSIDFOUND          :
      return "CO_E_NOMATCHINGSIDFOUND";
    case CO_E_LOOKUPACCSIDFAILED          :
      return "CO_E_LOOKUPACCSIDFAILED";
    case CO_E_NOMATCHINGNAMEFOUND         :
      return "CO_E_NOMATCHINGNAMEFOUND";
    case CO_E_LOOKUPACCNAMEFAILED         :
      return "CO_E_LOOKUPACCNAMEFAILED";
    case CO_E_SETSERLHNDLFAILED           :
      return "CO_E_SETSERLHNDLFAILED";
    case CO_E_FAILEDTOGETWINDIR           :
      return "CO_E_FAILEDTOGETWINDIR";
    case CO_E_PATHTOOLONG                 :
      return "CO_E_PATHTOOLONG";
    case CO_E_FAILEDTOGENUUID             :
      return "CO_E_FAILEDTOGENUUID";
    case CO_E_FAILEDTOCREATEFILE          :
      return "CO_E_FAILEDTOCREATEFILE";
    case CO_E_FAILEDTOCLOSEHANDLE         :
      return "CO_E_FAILEDTOCLOSEHANDLE";
    case CO_E_EXCEEDSYSACLLIMIT           :
      return "CO_E_EXCEEDSYSACLLIMIT";
    case CO_E_ACESINWRONGORDER            :
      return "CO_E_ACESINWRONGORDER";
    case CO_E_INCOMPATIBLESTREAMVERSION   :
      return "CO_E_INCOMPATIBLESTREAMVERSION";
    case CO_E_FAILEDTOOPENPROCESSTOKEN    :
      return "CO_E_FAILEDTOOPENPROCESSTOKEN";
    case CO_E_DECODEFAILED                :
      return "CO_E_DECODEFAILED";
    case CO_E_ACNOTINITIALIZED            :
      return "CO_E_ACNOTINITIALIZED";
    case OLE_S_USEREG                     :
      return "OLE_S_USEREG";
    case OLE_S_STATIC                     :
      return "OLE_S_STATIC";
    case OLE_S_MAC_CLIPFORMAT             :
      return "OLE_S_MAC_CLIPFORMAT";
    case DRAGDROP_S_DROP                  :
      return "DRAGDROP_S_DROP";
    case DRAGDROP_S_CANCEL                :
      return "DRAGDROP_S_CANCEL";
    case DRAGDROP_S_USEDEFAULTCURSORS     :
      return "DRAGDROP_S_USEDEFAULTCURSORS";
    case DATA_S_SAMEFORMATETC             :
      return "DATA_S_SAMEFORMATETC";
    case VIEW_S_ALREADY_FROZEN            :
      return "VIEW_S_ALREADY_FROZEN";
    case CACHE_S_FORMATETC_NOTSUPPORTED   :
      return "CACHE_S_FORMATETC_NOTSUPPORTED";
    case CACHE_S_SAMECACHE                :
      return "CACHE_S_SAMECACHE";
    case CACHE_S_SOMECACHES_NOTUPDATED    :
      return "CACHE_S_SOMECACHES_NOTUPDATED";
    case OLEOBJ_S_INVALIDVERB             :
      return "OLEOBJ_S_INVALIDVERB";
    case OLEOBJ_S_CANNOT_DOVERB_NOW       :
      return "OLEOBJ_S_CANNOT_DOVERB_NOW";
    case OLEOBJ_S_INVALIDHWND             :
      return "OLEOBJ_S_INVALIDHWND";
    case INPLACE_S_TRUNCATED              :
      return "INPLACE_S_TRUNCATED";
    case CONVERT10_S_NO_PRESENTATION      :
      return "CONVERT10_S_NO_PRESENTATION";
    case MK_S_REDUCED_TO_SELF             :
      return "MK_S_REDUCED_TO_SELF";
    case MK_S_ME                          :
      return "MK_S_ME";
    case MK_S_HIM                         :
      return "MK_S_HIM";
    case MK_S_US                          :
      return "MK_S_US";
    case MK_S_MONIKERALREADYREGISTERED    :
      return "MK_S_MONIKERALREADYREGISTERED";
    case CO_E_CLASS_CREATE_FAILED         :
      return "CO_E_CLASS_CREATE_FAILED";
    case CO_E_SCM_ERROR                   :
      return "CO_E_SCM_ERROR";
    case CO_E_SCM_RPC_FAILURE             :
      return "CO_E_SCM_RPC_FAILURE";
    case CO_E_BAD_PATH                    :
      return "CO_E_BAD_PATH";
    case CO_E_SERVER_EXEC_FAILURE         :
      return "CO_E_SERVER_EXEC_FAILURE";
    case CO_E_OBJSRV_RPC_FAILURE          :
      return "CO_E_OBJSRV_RPC_FAILURE";
    case MK_E_NO_NORMALIZED               :
      return "MK_E_NO_NORMALIZED";
    case CO_E_SERVER_STOPPING             :
      return "CO_E_SERVER_STOPPING";
    case MEM_E_INVALID_ROOT               :
      return "MEM_E_INVALID_ROOT";
    case MEM_E_INVALID_LINK               :
      return "MEM_E_INVALID_LINK";
    case MEM_E_INVALID_SIZE               :
      return "MEM_E_INVALID_SIZE";
    case CO_S_NOTALLINTERFACES            :
      return "CO_S_NOTALLINTERFACES";
    case DISP_E_UNKNOWNINTERFACE          :
      return "DISP_E_UNKNOWNINTERFACE";
    case DISP_E_MEMBERNOTFOUND            :
      return "DISP_E_MEMBERNOTFOUND";
    case DISP_E_PARAMNOTFOUND             :
      return "DISP_E_PARAMNOTFOUND";
    case DISP_E_TYPEMISMATCH              :
      return "DISP_E_TYPEMISMATCH";
    case DISP_E_UNKNOWNNAME               :
      return "DISP_E_UNKNOWNNAME";
    case DISP_E_NONAMEDARGS               :
      return "DISP_E_NONAMEDARGS";
    case DISP_E_BADVARTYPE                :
      return "DISP_E_BADVARTYPE";
    case DISP_E_EXCEPTION                 :
      return "DISP_E_EXCEPTION";
    case DISP_E_OVERFLOW                  :
      return "DISP_E_OVERFLOW";
    case DISP_E_BADINDEX                  :
      return "DISP_E_BADINDEX";
    case DISP_E_UNKNOWNLCID               :
      return "DISP_E_UNKNOWNLCID";
    case DISP_E_ARRAYISLOCKED             :
      return "DISP_E_ARRAYISLOCKED";
    case DISP_E_BADPARAMCOUNT             :
      return "DISP_E_BADPARAMCOUNT";
    case DISP_E_PARAMNOTOPTIONAL          :
      return "DISP_E_PARAMNOTOPTIONAL";
    case DISP_E_BADCALLEE                 :
      return "DISP_E_BADCALLEE";
    case DISP_E_NOTACOLLECTION            :
      return "DISP_E_NOTACOLLECTION";
    case DISP_E_DIVBYZERO                 :
      return "DISP_E_DIVBYZERO";
    case TYPE_E_BUFFERTOOSMALL            :
      return "TYPE_E_BUFFERTOOSMALL";
    case TYPE_E_FIELDNOTFOUND             :
      return "TYPE_E_FIELDNOTFOUND";
    case TYPE_E_INVDATAREAD               :
      return "TYPE_E_INVDATAREAD";
    case TYPE_E_UNSUPFORMAT               :
      return "TYPE_E_UNSUPFORMAT";
    case TYPE_E_REGISTRYACCESS            :
      return "TYPE_E_REGISTRYACCESS";
    case TYPE_E_LIBNOTREGISTERED          :
      return "TYPE_E_LIBNOTREGISTERED";
    case TYPE_E_UNDEFINEDTYPE             :
      return "TYPE_E_UNDEFINEDTYPE";
    case TYPE_E_QUALIFIEDNAMEDISALLOWED   :
      return "TYPE_E_QUALIFIEDNAMEDISALLOWED";
    case TYPE_E_INVALIDSTATE              :
      return "TYPE_E_INVALIDSTATE";
    case TYPE_E_WRONGTYPEKIND             :
      return "TYPE_E_WRONGTYPEKIND";
    case TYPE_E_ELEMENTNOTFOUND           :
      return "TYPE_E_ELEMENTNOTFOUND";
    case TYPE_E_AMBIGUOUSNAME             :
      return "TYPE_E_AMBIGUOUSNAME";
    case TYPE_E_NAMECONFLICT              :
      return "TYPE_E_NAMECONFLICT";
    case TYPE_E_UNKNOWNLCID               :
      return "TYPE_E_UNKNOWNLCID";
    case TYPE_E_DLLFUNCTIONNOTFOUND       :
      return "TYPE_E_DLLFUNCTIONNOTFOUND";
    case TYPE_E_BADMODULEKIND             :
      return "TYPE_E_BADMODULEKIND";
    case TYPE_E_SIZETOOBIG                :
      return "TYPE_E_SIZETOOBIG";
    case TYPE_E_DUPLICATEID               :
      return "TYPE_E_DUPLICATEID";
    case TYPE_E_INVALIDID                 :
      return "TYPE_E_INVALIDID";
    case TYPE_E_TYPEMISMATCH              :
      return "TYPE_E_TYPEMISMATCH";
    case TYPE_E_OUTOFBOUNDS               :
      return "TYPE_E_OUTOFBOUNDS";
    case TYPE_E_IOERROR                   :
      return "TYPE_E_IOERROR";
    case TYPE_E_CANTCREATETMPFILE         :
      return "TYPE_E_CANTCREATETMPFILE";
    case TYPE_E_CANTLOADLIBRARY           :
      return "TYPE_E_CANTLOADLIBRARY";
    case TYPE_E_INCONSISTENTPROPFUNCS     :
      return "TYPE_E_INCONSISTENTPROPFUNCS";
    case TYPE_E_CIRCULARTYPE              :
      return "TYPE_E_CIRCULARTYPE";
    case STG_E_INVALIDFUNCTION            :
      return "STG_E_INVALIDFUNCTION";
    case STG_E_FILENOTFOUND               :
      return "STG_E_FILENOTFOUND";
    case STG_E_PATHNOTFOUND               :
      return "STG_E_PATHNOTFOUND";
    case STG_E_TOOMANYOPENFILES           :
      return "STG_E_TOOMANYOPENFILES";
    case STG_E_ACCESSDENIED               :
      return "STG_E_ACCESSDENIED";
    case STG_E_INVALIDHANDLE              :
      return "STG_E_INVALIDHANDLE";
    case STG_E_INSUFFICIENTMEMORY         :
      return "STG_E_INSUFFICIENTMEMORY";
    case STG_E_INVALIDPOINTER             :
      return "STG_E_INVALIDPOINTER";
    case STG_E_NOMOREFILES                :
      return "STG_E_NOMOREFILES";
    case STG_E_DISKISWRITEPROTECTED       :
      return "STG_E_DISKISWRITEPROTECTED";
    case STG_E_SEEKERROR                  :
      return "STG_E_SEEKERROR";
    case STG_E_WRITEFAULT                 :
      return "STG_E_WRITEFAULT";
    case STG_E_READFAULT                  :
      return "STG_E_READFAULT";
    case STG_E_SHAREVIOLATION             :
      return "STG_E_SHAREVIOLATION";
    case STG_E_LOCKVIOLATION              :
      return "STG_E_LOCKVIOLATION";
    case STG_E_FILEALREADYEXISTS          :
      return "STG_E_FILEALREADYEXISTS";
    case STG_E_INVALIDPARAMETER           :
      return "STG_E_INVALIDPARAMETER";
    case STG_E_MEDIUMFULL                 :
      return "STG_E_MEDIUMFULL";
    case STG_E_PROPSETMISMATCHED          :
      return "STG_E_PROPSETMISMATCHED";
    case STG_E_ABNORMALAPIEXIT            :
      return "STG_E_ABNORMALAPIEXIT";
    case STG_E_INVALIDHEADER              :
      return "STG_E_INVALIDHEADER";
    case STG_E_INVALIDNAME                :
      return "STG_E_INVALIDNAME";
    case STG_E_UNKNOWN                    :
      return "STG_E_UNKNOWN";
    case STG_E_UNIMPLEMENTEDFUNCTION      :
      return "STG_E_UNIMPLEMENTEDFUNCTION";
    case STG_E_INVALIDFLAG                :
      return "STG_E_INVALIDFLAG";
    case STG_E_INUSE                      :
      return "STG_E_INUSE";
    case STG_E_NOTCURRENT                 :
      return "STG_E_NOTCURRENT";
    case STG_E_REVERTED                   :
      return "STG_E_REVERTED";
    case STG_E_CANTSAVE                   :
      return "STG_E_CANTSAVE";
    case STG_E_OLDFORMAT                  :
      return "STG_E_OLDFORMAT";
    case STG_E_OLDDLL                     :
      return "STG_E_OLDDLL";
    case STG_E_SHAREREQUIRED              :
      return "STG_E_SHAREREQUIRED";
    case STG_E_NOTFILEBASEDSTORAGE        :
      return "STG_E_NOTFILEBASEDSTORAGE";
    case STG_E_EXTANTMARSHALLINGS         :
      return "STG_E_EXTANTMARSHALLINGS";
    case STG_E_DOCFILECORRUPT             :
      return "STG_E_DOCFILECORRUPT";
    case STG_E_BADBASEADDRESS             :
      return "STG_E_BADBASEADDRESS";
    case STG_E_INCOMPLETE                 :
      return "STG_E_INCOMPLETE";
    case STG_E_TERMINATED                 :
      return "STG_E_TERMINATED";
    case STG_S_CONVERTED                  :
      return "STG_S_CONVERTED";
    case STG_S_BLOCK                      :
      return "STG_S_BLOCK";
    case STG_S_RETRYNOW                   :
      return "STG_S_RETRYNOW";
    case STG_S_MONITORING                 :
      return "STG_S_MONITORING";
    case STG_S_MULTIPLEOPENS              :
      return "STG_S_MULTIPLEOPENS";
    case STG_S_CONSOLIDATIONFAILED        :
      return "STG_S_CONSOLIDATIONFAILED";
    case STG_S_CANNOTCONSOLIDATE          :
      return "STG_S_CANNOTCONSOLIDATE";
    case RPC_E_CALL_REJECTED              :
      return "RPC_E_CALL_REJECTED";
    case RPC_E_CALL_CANCELED              :
      return "RPC_E_CALL_CANCELED";
    case RPC_E_CANTPOST_INSENDCALL        :
      return "RPC_E_CANTPOST_INSENDCALL";
    case RPC_E_CANTCALLOUT_INASYNCCALL    :
      return "RPC_E_CANTCALLOUT_INASYNCCALL";
    case RPC_E_CANTCALLOUT_INEXTERNALCALL :
      return "RPC_E_CANTCALLOUT_INEXTERNALCALL";
    case RPC_E_CONNECTION_TERMINATED      :
      return "RPC_E_CONNECTION_TERMINATED";
    case RPC_E_SERVER_DIED                :
      return "RPC_E_SERVER_DIED";
    case RPC_E_CLIENT_DIED                :
      return "RPC_E_CLIENT_DIED";
    case RPC_E_INVALID_DATAPACKET         :
      return "RPC_E_INVALID_DATAPACKET";
    case RPC_E_CANTTRANSMIT_CALL          :
      return "RPC_E_CANTTRANSMIT_CALL";
    case RPC_E_CLIENT_CANTMARSHAL_DATA    :
      return "RPC_E_CLIENT_CANTMARSHAL_DATA";
    case RPC_E_CLIENT_CANTUNMARSHAL_DATA  :
      return "RPC_E_CLIENT_CANTUNMARSHAL_DATA";
    case RPC_E_SERVER_CANTMARSHAL_DATA    :
      return "RPC_E_SERVER_CANTMARSHAL_DATA";
    case RPC_E_SERVER_CANTUNMARSHAL_DATA  :
      return "RPC_E_SERVER_CANTUNMARSHAL_DATA";
    case RPC_E_INVALID_DATA               :
      return "RPC_E_INVALID_DATA";
    case RPC_E_INVALID_PARAMETER          :
      return "RPC_E_INVALID_PARAMETER";
    case RPC_E_CANTCALLOUT_AGAIN          :
      return "RPC_E_CANTCALLOUT_AGAIN";
    case RPC_E_SERVER_DIED_DNE            :
      return "RPC_E_SERVER_DIED_DNE";
    case RPC_E_SYS_CALL_FAILED            :
      return "RPC_E_SYS_CALL_FAILED";
    case RPC_E_OUT_OF_RESOURCES           :
      return "RPC_E_OUT_OF_RESOURCES";
    case RPC_E_ATTEMPTED_MULTITHREAD      :
      return "RPC_E_ATTEMPTED_MULTITHREAD";
    case RPC_E_NOT_REGISTERED             :
      return "RPC_E_NOT_REGISTERED";
    case RPC_E_FAULT                      :
      return "RPC_E_FAULT";
    case RPC_E_SERVERFAULT                :
      return "RPC_E_SERVERFAULT";
    case RPC_E_CHANGED_MODE               :
      return "RPC_E_CHANGED_MODE";
    case RPC_E_INVALIDMETHOD              :
      return "RPC_E_INVALIDMETHOD";
    case RPC_E_DISCONNECTED               :
      return "RPC_E_DISCONNECTED";
    case RPC_E_RETRY                      :
      return "RPC_E_RETRY";
    case RPC_E_SERVERCALL_RETRYLATER      :
      return "RPC_E_SERVERCALL_RETRYLATER";
    case RPC_E_SERVERCALL_REJECTED        :
      return "RPC_E_SERVERCALL_REJECTED";
    case RPC_E_INVALID_CALLDATA           :
      return "RPC_E_INVALID_CALLDATA";
    case RPC_E_CANTCALLOUT_ININPUTSYNCCALL :
      return "RPC_E_CANTCALLOUT_ININPUTSYNCCALL ";
    case RPC_E_WRONG_THREAD               :
      return "RPC_E_WRONG_THREAD";
    case RPC_E_THREAD_NOT_INIT            :
      return "RPC_E_THREAD_NOT_INIT";
    case RPC_E_VERSION_MISMATCH           :
      return "RPC_E_VERSION_MISMATCH";
    case RPC_E_INVALID_HEADER             :
      return "RPC_E_INVALID_HEADER";
    case RPC_E_INVALID_EXTENSION          :
      return "RPC_E_INVALID_EXTENSION";
    case RPC_E_INVALID_IPID               :
      return "RPC_E_INVALID_IPID";
    case RPC_E_INVALID_OBJECT             :
      return "RPC_E_INVALID_OBJECT";
    case RPC_S_CALLPENDING                :
      return "RPC_S_CALLPENDING";
    case RPC_S_WAITONTIMER                :
      return "RPC_S_WAITONTIMER";
    case RPC_E_CALL_COMPLETE              :
      return "RPC_E_CALL_COMPLETE";
    case RPC_E_UNSECURE_CALL              :
      return "RPC_E_UNSECURE_CALL";
    case RPC_E_TOO_LATE                   :
      return "RPC_E_TOO_LATE";
    case RPC_E_NO_GOOD_SECURITY_PACKAGES  :
      return "RPC_E_NO_GOOD_SECURITY_PACKAGES";
    case RPC_E_ACCESS_DENIED              :
      return "RPC_E_ACCESS_DENIED";
    case RPC_E_REMOTE_DISABLED            :
      return "RPC_E_REMOTE_DISABLED";
    case RPC_E_INVALID_OBJREF             :
      return "RPC_E_INVALID_OBJREF";
    case RPC_E_NO_CONTEXT                 :
      return "RPC_E_NO_CONTEXT";
    case RPC_E_TIMEOUT                    :
      return "RPC_E_TIMEOUT";
    case RPC_E_NO_SYNC                    :
      return "RPC_E_NO_SYNC";
    case RPC_E_UNEXPECTED                 :
      return "RPC_E_UNEXPECTED";
    case NTE_BAD_UID                      :
      return "NTE_BAD_UID";
    case NTE_BAD_HASH                     :
      return "NTE_BAD_HASH";
    //case NTE_BAD_HASH                     :
    //  return "NTE_BAD_HASH";
    case NTE_BAD_KEY                      :
      return "NTE_BAD_KEY";
    case NTE_BAD_LEN                      :
      return "NTE_BAD_LEN";
    case NTE_BAD_DATA                     :
      return "NTE_BAD_DATA";
    case NTE_BAD_SIGNATURE                :
      return "NTE_BAD_SIGNATURE";
    case NTE_BAD_VER                      :
      return "NTE_BAD_VER";
    case NTE_BAD_ALGID                    :
      return "NTE_BAD_ALGID";
    case NTE_BAD_FLAGS                    :
      return "NTE_BAD_FLAGS";
    case NTE_BAD_TYPE                     :
      return "NTE_BAD_TYPE";
    case NTE_BAD_KEY_STATE                :
      return "NTE_BAD_KEY_STATE";
    case NTE_BAD_HASH_STATE               :
      return "NTE_BAD_HASH_STATE";
    case NTE_NO_KEY                       :
      return "NTE_NO_KEY";
    case NTE_NO_MEMORY                    :
      return "NTE_NO_MEMORY";
    case NTE_EXISTS                       :
      return "NTE_EXISTS";
    case NTE_PERM                         :
      return "NTE_PERM";
    case NTE_NOT_FOUND                    :
      return "NTE_NOT_FOUND";
    case NTE_DOUBLE_ENCRYPT               :
      return "NTE_DOUBLE_ENCRYPT";
    case NTE_BAD_PROVIDER                 :
      return "NTE_BAD_PROVIDER";
    case NTE_BAD_PROV_TYPE                :
      return "NTE_BAD_PROV_TYPE";
    case NTE_BAD_PUBLIC_KEY               :
      return "NTE_BAD_PUBLIC_KEY";
    case NTE_BAD_KEYSET                   :
      return "NTE_BAD_KEYSET";
    case NTE_PROV_TYPE_NOT_DEF            :
      return "NTE_PROV_TYPE_NOT_DEF";
    case NTE_PROV_TYPE_ENTRY_BAD          :
      return "NTE_PROV_TYPE_ENTRY_BAD";
    case NTE_KEYSET_NOT_DEF               :
      return "NTE_KEYSET_NOT_DEF";
    case NTE_KEYSET_ENTRY_BAD             :
      return "NTE_KEYSET_ENTRY_BAD";
    case NTE_PROV_TYPE_NO_MATCH           :
      return "NTE_PROV_TYPE_NO_MATCH";
    case NTE_SIGNATURE_FILE_BAD           :
      return "NTE_SIGNATURE_FILE_BAD";
    case NTE_PROVIDER_DLL_FAIL            :
      return "NTE_PROVIDER_DLL_FAIL";
    case NTE_PROV_DLL_NOT_FOUND           :
      return "NTE_PROV_DLL_NOT_FOUND";
    case NTE_BAD_KEYSET_PARAM             :
      return "NTE_BAD_KEYSET_PARAM";
    case NTE_FAIL                         :
      return "NTE_FAIL";
    case NTE_SYS_ERR                      :
      return "NTE_SYS_ERR";
    case CRYPT_E_MSG_ERROR                :
      return "CRYPT_E_MSG_ERROR";
    case CRYPT_E_UNKNOWN_ALGO             :
      return "CRYPT_E_UNKNOWN_ALGO";
    case CRYPT_E_OID_FORMAT               :
      return "CRYPT_E_OID_FORMAT";
    case CRYPT_E_INVALID_MSG_TYPE         :
      return "CRYPT_E_INVALID_MSG_TYPE";
    case CRYPT_E_UNEXPECTED_ENCODING      :
      return "CRYPT_E_UNEXPECTED_ENCODING";
    case CRYPT_E_AUTH_ATTR_MISSING        :
      return "CRYPT_E_AUTH_ATTR_MISSING";
    case CRYPT_E_HASH_VALUE               :
      return "CRYPT_E_HASH_VALUE";
    case CRYPT_E_INVALID_INDEX            :
      return "CRYPT_E_INVALID_INDEX";
    case CRYPT_E_ALREADY_DECRYPTED        :
      return "CRYPT_E_ALREADY_DECRYPTED";
    case CRYPT_E_NOT_DECRYPTED            :
      return "CRYPT_E_NOT_DECRYPTED";
    case CRYPT_E_RECIPIENT_NOT_FOUND      :
      return "CRYPT_E_RECIPIENT_NOT_FOUND";
    case CRYPT_E_CONTROL_TYPE             :
      return "CRYPT_E_CONTROL_TYPE";
    case CRYPT_E_ISSUER_SERIALNUMBER      :
      return "CRYPT_E_ISSUER_SERIALNUMBER";
    case CRYPT_E_SIGNER_NOT_FOUND         :
      return "CRYPT_E_SIGNER_NOT_FOUND";
    case CRYPT_E_ATTRIBUTES_MISSING       :
      return "CRYPT_E_ATTRIBUTES_MISSING";
    case CRYPT_E_STREAM_MSG_NOT_READY     :
      return "CRYPT_E_STREAM_MSG_NOT_READY";
    case CRYPT_E_STREAM_INSUFFICIENT_DATA :
      return "CRYPT_E_STREAM_INSUFFICIENT_DATA";
    case CRYPT_E_BAD_LEN                  :
      return "CRYPT_E_BAD_LEN";
    case CRYPT_E_BAD_ENCODE               :
      return "CRYPT_E_BAD_ENCODE";
    case CRYPT_E_FILE_ERROR               :
      return "CRYPT_E_FILE_ERROR";
    case CRYPT_E_NOT_FOUND                :
      return "CRYPT_E_NOT_FOUND";
    case CRYPT_E_EXISTS                   :
      return "CRYPT_E_EXISTS";
    case CRYPT_E_NO_PROVIDER              :
      return "CRYPT_E_NO_PROVIDER";
    case CRYPT_E_SELF_SIGNED              :
      return "CRYPT_E_SELF_SIGNED";
    case CRYPT_E_DELETED_PREV             :
      return "CRYPT_E_DELETED_PREV";
    case CRYPT_E_NO_MATCH                 :
      return "CRYPT_E_NO_MATCH";
    case CRYPT_E_UNEXPECTED_MSG_TYPE      :
      return "CRYPT_E_UNEXPECTED_MSG_TYPE";
    case CRYPT_E_NO_KEY_PROPERTY          :
      return "CRYPT_E_NO_KEY_PROPERTY";
    case CRYPT_E_NO_DECRYPT_CERT          :
      return "CRYPT_E_NO_DECRYPT_CERT";
    case CRYPT_E_BAD_MSG                  :
      return "CRYPT_E_BAD_MSG";
    case CRYPT_E_NO_SIGNER                :
      return "CRYPT_E_NO_SIGNER";
    case CRYPT_E_PENDING_CLOSE            :
      return "CRYPT_E_PENDING_CLOSE";
    case CRYPT_E_REVOKED                  :
      return "CRYPT_E_REVOKED";
    case CRYPT_E_NO_REVOCATION_DLL        :
      return "CRYPT_E_NO_REVOCATION_DLL";
    case CRYPT_E_NO_REVOCATION_CHECK      :
      return "CRYPT_E_NO_REVOCATION_CHECK";
    case CRYPT_E_REVOCATION_OFFLINE       :
      return "CRYPT_E_REVOCATION_OFFLINE";
    case CRYPT_E_NOT_IN_REVOCATION_DATABASE :
      return "CRYPT_E_NOT_IN_REVOCATION_DATABASE";
    case CRYPT_E_INVALID_NUMERIC_STRING   :
      return "CRYPT_E_INVALID_NUMERIC_STRING";
    case CRYPT_E_INVALID_PRINTABLE_STRING :
      return "CRYPT_E_INVALID_PRINTABLE_STRING";
    case CRYPT_E_INVALID_IA5_STRING       :
      return "CRYPT_E_INVALID_IA5_STRING";
    case CRYPT_E_INVALID_X500_STRING      :
      return "CRYPT_E_INVALID_X500_STRING";
    case CRYPT_E_NOT_CHAR_STRING          :
      return "CRYPT_E_NOT_CHAR_STRING";
    case CRYPT_E_FILERESIZED              :
      return "CRYPT_E_FILERESIZED";
    case CRYPT_E_SECURITY_SETTINGS        :
      return "CRYPT_E_SECURITY_SETTINGS";
    case CRYPT_E_NO_VERIFY_USAGE_DLL      :
      return "CRYPT_E_NO_VERIFY_USAGE_DLL";
    case CRYPT_E_NO_VERIFY_USAGE_CHECK    :
      return "CRYPT_E_NO_VERIFY_USAGE_CHECK";
    case CRYPT_E_VERIFY_USAGE_OFFLINE     :
      return "CRYPT_E_VERIFY_USAGE_OFFLINE";
    case CRYPT_E_NOT_IN_CTL               :
      return "CRYPT_E_NOT_IN_CTL";
    case CRYPT_E_NO_TRUSTED_SIGNER        :
      return "CRYPT_E_NO_TRUSTED_SIGNER";
    case CRYPT_E_OSS_ERROR                :
      return "CRYPT_E_OSS_ERROR";
    case CERTSRV_E_BAD_REQUESTSUBJECT     :
      return "CERTSRV_E_BAD_REQUESTSUBJECT";
    case CERTSRV_E_NO_REQUEST             :
      return "CERTSRV_E_NO_REQUEST";
    case CERTSRV_E_BAD_REQUESTSTATUS      :
      return "CERTSRV_E_BAD_REQUESTSTATUS";
    case CERTSRV_E_PROPERTY_EMPTY         :
      return "CERTSRV_E_PROPERTY_EMPTY";
      //case CERTDB_E_JET_ERROR               :
      //return "CERTDB_E_JET_ERROR";
    case TRUST_E_SYSTEM_ERROR             :
      return "TRUST_E_SYSTEM_ERROR";
    case TRUST_E_NO_SIGNER_CERT           :
      return "TRUST_E_NO_SIGNER_CERT";
    case TRUST_E_COUNTER_SIGNER           :
      return "TRUST_E_COUNTER_SIGNER";
    case TRUST_E_CERT_SIGNATURE           :
      return "TRUST_E_CERT_SIGNATURE";
    case TRUST_E_TIME_STAMP               :
      return "TRUST_E_TIME_STAMP";
    case TRUST_E_BAD_DIGEST               :
      return "TRUST_E_BAD_DIGEST";
    case TRUST_E_BASIC_CONSTRAINTS        :
      return "TRUST_E_BASIC_CONSTRAINTS";
    case TRUST_E_FINANCIAL_CRITERIA       :
      return "TRUST_E_FINANCIAL_CRITERIA";
    case TRUST_E_PROVIDER_UNKNOWN         :
      return "TRUST_E_PROVIDER_UNKNOWN";
    case TRUST_E_ACTION_UNKNOWN           :
      return "TRUST_E_ACTION_UNKNOWN";
    case TRUST_E_SUBJECT_FORM_UNKNOWN     :
      return "TRUST_E_SUBJECT_FORM_UNKNOWN";
    case TRUST_E_SUBJECT_NOT_TRUSTED      :
      return "TRUST_E_SUBJECT_NOT_TRUSTED";
    case DIGSIG_E_ENCODE                  :
      return "DIGSIG_E_ENCODE";
    case DIGSIG_E_DECODE                  :
      return "DIGSIG_E_DECODE";
    case DIGSIG_E_EXTENSIBILITY           :
      return "DIGSIG_E_EXTENSIBILITY";
    case DIGSIG_E_CRYPTO                  :
      return "DIGSIG_E_CRYPTO";
    case PERSIST_E_SIZEDEFINITE           :
      return "PERSIST_E_SIZEDEFINITE";
    case PERSIST_E_SIZEINDEFINITE         :
      return "PERSIST_E_SIZEINDEFINITE";
    case PERSIST_E_NOTSELFSIZING          :
      return "PERSIST_E_NOTSELFSIZING";
    case TRUST_E_NOSIGNATURE              :
      return "TRUST_E_NOSIGNATURE";
    case CERT_E_EXPIRED                   :
      return "CERT_E_EXPIRED";
    case CERT_E_VALIDITYPERIODNESTING     :
      return "CERT_E_VALIDITYPERIODNESTING";
    case CERT_E_ROLE                      :
      return "CERT_E_ROLE";
    case CERT_E_PATHLENCONST              :
      return "CERT_E_PATHLENCONST";
    case CERT_E_CRITICAL                  :
      return "CERT_E_CRITICAL";
    case CERT_E_PURPOSE                   :
      return "CERT_E_PURPOSE";
    case CERT_E_ISSUERCHAINING            :
      return "CERT_E_ISSUERCHAINING";
    case CERT_E_MALFORMED                 :
      return "CERT_E_MALFORMED";
    case CERT_E_UNTRUSTEDROOT             :
      return "CERT_E_UNTRUSTEDROOT";
    case CERT_E_CHAINING                  :
      return "CERT_E_CHAINING";
    case TRUST_E_FAIL                     :
      return "TRUST_E_FAIL";
    case CERT_E_REVOKED                   :
      return "CERT_E_REVOKED";
    case CERT_E_UNTRUSTEDTESTROOT         :
      return "CERT_E_UNTRUSTEDTESTROOT";
    case CERT_E_REVOCATION_FAILURE        :
      return "CERT_E_REVOCATION_FAILURE";
    case CERT_E_CN_NO_MATCH               :
      return "CERT_E_CN_NO_MATCH";
    case CERT_E_WRONG_USAGE               :
      return "CERT_E_WRONG_USAGE";
    case SPAPI_E_EXPECTED_SECTION_NAME    :
      return "SPAPI_E_EXPECTED_SECTION_NAME";
    case SPAPI_E_BAD_SECTION_NAME_LINE    :
      return "SPAPI_E_BAD_SECTION_NAME_LINE";
    case SPAPI_E_SECTION_NAME_TOO_LONG    :
      return "SPAPI_E_SECTION_NAME_TOO_LONG";
    case SPAPI_E_GENERAL_SYNTAX           :
      return "SPAPI_E_GENERAL_SYNTAX";
    case SPAPI_E_WRONG_INF_STYLE          :
      return "SPAPI_E_WRONG_INF_STYLE";
    case SPAPI_E_SECTION_NOT_FOUND        :
      return "SPAPI_E_SECTION_NOT_FOUND";
    case SPAPI_E_LINE_NOT_FOUND           :
      return "SPAPI_E_LINE_NOT_FOUND";
    case SPAPI_E_NO_ASSOCIATED_CLASS      :
      return "SPAPI_E_NO_ASSOCIATED_CLASS";
    case SPAPI_E_CLASS_MISMATCH           :
      return "SPAPI_E_CLASS_MISMATCH";
    case SPAPI_E_DUPLICATE_FOUND          :
      return "SPAPI_E_DUPLICATE_FOUND";
    case SPAPI_E_NO_DRIVER_SELECTED       :
      return "SPAPI_E_NO_DRIVER_SELECTED";
    case SPAPI_E_KEY_DOES_NOT_EXIST       :
      return "SPAPI_E_KEY_DOES_NOT_EXIST";
    case SPAPI_E_INVALID_DEVINST_NAME     :
      return "SPAPI_E_INVALID_DEVINST_NAME";
    case SPAPI_E_INVALID_CLASS            :
      return "SPAPI_E_INVALID_CLASS";
    case SPAPI_E_DEVINST_ALREADY_EXISTS   :
      return "SPAPI_E_DEVINST_ALREADY_EXISTS";
    case SPAPI_E_DEVINFO_NOT_REGISTERED   :
      return "SPAPI_E_DEVINFO_NOT_REGISTERED";
    case SPAPI_E_INVALID_REG_PROPERTY     :
      return "SPAPI_E_INVALID_REG_PROPERTY";
    case SPAPI_E_NO_INF                   :
      return "SPAPI_E_NO_INF";
    case SPAPI_E_NO_SUCH_DEVINST          :
      return "SPAPI_E_NO_SUCH_DEVINST";
    case SPAPI_E_CANT_LOAD_CLASS_ICON     :
      return "SPAPI_E_CANT_LOAD_CLASS_ICON";
    case SPAPI_E_INVALID_CLASS_INSTALLER  :
      return "SPAPI_E_INVALID_CLASS_INSTALLER";
    case SPAPI_E_DI_DO_DEFAULT            :
      return "SPAPI_E_DI_DO_DEFAULT";
    case SPAPI_E_DI_NOFILECOPY            :
      return "SPAPI_E_DI_NOFILECOPY";
    case SPAPI_E_INVALID_HWPROFILE        :
      return "SPAPI_E_INVALID_HWPROFILE";
    case SPAPI_E_NO_DEVICE_SELECTED       :
      return "SPAPI_E_NO_DEVICE_SELECTED";
    case SPAPI_E_DEVINFO_LIST_LOCKED      :
      return "SPAPI_E_DEVINFO_LIST_LOCKED";
    case SPAPI_E_DEVINFO_DATA_LOCKED      :
      return "SPAPI_E_DEVINFO_DATA_LOCKED";
    case SPAPI_E_DI_BAD_PATH              :
      return "SPAPI_E_DI_BAD_PATH";
    case SPAPI_E_NO_CLASSINSTALL_PARAMS   :
      return "SPAPI_E_NO_CLASSINSTALL_PARAMS";
    case SPAPI_E_FILEQUEUE_LOCKED         :
      return "SPAPI_E_FILEQUEUE_LOCKED";
    case SPAPI_E_BAD_SERVICE_INSTALLSECT  :
      return "SPAPI_E_BAD_SERVICE_INSTALLSECT";
    case SPAPI_E_NO_CLASS_DRIVER_LIST     :
      return "SPAPI_E_NO_CLASS_DRIVER_LIST";
    case SPAPI_E_NO_ASSOCIATED_SERVICE    :
      return "SPAPI_E_NO_ASSOCIATED_SERVICE";
    case SPAPI_E_NO_DEFAULT_DEVICE_INTERFACE :
      return "SPAPI_E_NO_DEFAULT_DEVICE_INTERFACE";
    case SPAPI_E_DEVICE_INTERFACE_ACTIVE  :
      return "SPAPI_E_DEVICE_INTERFACE_ACTIVE";
    case SPAPI_E_DEVICE_INTERFACE_REMOVED :
      return "SPAPI_E_DEVICE_INTERFACE_REMOVED";
    case SPAPI_E_BAD_INTERFACE_INSTALLSECT :
      return "SPAPI_E_BAD_INTERFACE_INSTALLSECT";
    case SPAPI_E_NO_SUCH_INTERFACE_CLASS  :
      return "SPAPI_E_NO_SUCH_INTERFACE_CLASS";
    case SPAPI_E_INVALID_REFERENCE_STRING :
      return "SPAPI_E_INVALID_REFERENCE_STRING";
    case SPAPI_E_INVALID_MACHINENAME      :
      return "SPAPI_E_INVALID_MACHINENAME";
    case SPAPI_E_REMOTE_COMM_FAILURE      :
      return "SPAPI_E_REMOTE_COMM_FAILURE";
    case SPAPI_E_MACHINE_UNAVAILABLE      :
      return "SPAPI_E_MACHINE_UNAVAILABLE";
    case SPAPI_E_NO_CONFIGMGR_SERVICES    :
      return "SPAPI_E_NO_CONFIGMGR_SERVICES";
    case SPAPI_E_INVALID_PROPPAGE_PROVIDER :
      return "SPAPI_E_INVALID_PROPPAGE_PROVIDER";
    case SPAPI_E_NO_SUCH_DEVICE_INTERFACE :
      return "SPAPI_E_NO_SUCH_DEVICE_INTERFACE";
    case SPAPI_E_DI_POSTPROCESSING_REQUIRED :
      return "SPAPI_E_DI_POSTPROCESSING_REQUIRED";
    case SPAPI_E_INVALID_COINSTALLER      :
      return "SPAPI_E_INVALID_COINSTALLER";
    case SPAPI_E_NO_COMPAT_DRIVERS        :
      return "SPAPI_E_NO_COMPAT_DRIVERS";
    case SPAPI_E_NO_DEVICE_ICON           :
      return "SPAPI_E_NO_DEVICE_ICON";
    case SPAPI_E_INVALID_INF_LOGCONFIG    :
      return "SPAPI_E_INVALID_INF_LOGCONFIG";
    case SPAPI_E_DI_DONT_INSTALL          :
      return "SPAPI_E_DI_DONT_INSTALL";
    case SPAPI_E_INVALID_FILTER_DRIVER    :
      return "SPAPI_E_INVALID_FILTER_DRIVER";
    case SPAPI_E_ERROR_NOT_INSTALLED      :
      return "SPAPI_E_ERROR_NOT_INSTALLED";

    default:
      static char buff[200];
      sprintf(buff, "Unrecognized error value: %08X\0", error);

      return buff;
  }
}
#endif

#if 0
bool GetProcessList(void) {
    bool           bRet      = false;
    PROCESSENTRY32 pe32      = {0};

    HINSTANCE hK32 = LoadLibrary("kernel32.dll");
    if(hK32 == NULL)
        return false;

    // nt4 doesnt seem to include these
    typedef HANDLE (WINAPI *CREATETOOLHELP32SNAPSHOT)(DWORD dwFlags,DWORD th32ProcessID);
    CREATETOOLHELP32SNAPSHOT pCreateToolhelp32Snapshot = (CREATETOOLHELP32SNAPSHOT) GetProcAddress(hK32, "CreateToolhelp32Snapshot");

    if(pCreateToolhelp32Snapshot == NULL) {
        errorLog << "GetPList error 1, err=" << GetLastError() << endl;
        goto cleanup;
    }

    typedef BOOL (WINAPI *PROCESS32FIRST)(HANDLE hSnapshot,LPPROCESSENTRY32 lppe);
    typedef BOOL (WINAPI *PROCESS32NEXT)(HANDLE hSnapshot,LPPROCESSENTRY32 lppe);
    PROCESS32FIRST pProcess32First = (PROCESS32FIRST) GetProcAddress(hK32, "Process32First");
    PROCESS32NEXT  pProcess32Next = (PROCESS32NEXT) GetProcAddress(hK32, "Process32Next");
    if((pProcess32First ==NULL)||(pProcess32Next ==NULL)) {
        errorLog << "GetPList error 2, err=" << GetLastError() << endl;
        goto cleanup;
    }

    //  Take a snapshot of all processes in the system (do we need the module list too, esp. for IE?)
    HANDLE hProcessSnap = (*pCreateToolhelp32Snapshot)(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) {
        errorLog << "GetPList error 3, err=" << GetLastError() << endl;
        goto cleanup;
    }

    //  Fill in the size of the structure before using it.

    pe32.dwSize = sizeof(PROCESSENTRY32);

    //  Walk the snapshot of the processes, and for each process,
    //  display information.

    if (!(*pProcess32First)(hProcessSnap, &pe32))  {
        errorLog << "GetPList error 4, err=" << GetLastError() << endl;
        goto cleanup;
    }

    errorLog << "Process List:\n";

    do {
        errorLog << "["<<pe32.th32ProcessID<<"] " << pe32.szExeFile << endl;
    } while (Process32Next(hProcessSnap, &pe32));
    bRet = true;

  cleanup:

    if(hProcessSnap!=NULL)
        CloseHandle (hProcessSnap);
    if(hK32!=NULL)
        FreeLibrary(hK32);
    return bRet;
}
#endif

DWORD SysInfo::
GetVidMemSizeFromRegistry(void) {
  DWORD VidMemSize=0;

  // I only know how to do this for NT so far, not sure if it's possible on w9x (certainly not the same way)
  if(_os_type < OS_WinNT)
      return 0;

  HKEY hDevMapKey=NULL;
  HKEY hVidDriverKey=NULL;
  const char *DevMapRegKeyName="HARDWARE\\DEVICEMAP\\VIDEO";

  ULONG retVal=RegOpenKeyEx(HKEY_LOCAL_MACHINE, DevMapRegKeyName,0,KEY_READ,&hDevMapKey);
  if ((ERROR_SUCCESS != retVal) || (hDevMapKey==NULL)) {
    errorLog << "regOpenKey RO failed for "<<DevMapRegKeyName<<", err=" << GetLastError() << endl;
    goto cleanup;
  }

  #define REGPTRSIZE 512
  char VideoDriverRegPtr[REGPTRSIZE];
  DWORD dwType,dwSize=REGPTRSIZE;
  if(ERROR_SUCCESS != RegQueryValueEx(hDevMapKey, "\\Device\\Video0", 0, &dwType, (LPBYTE)VideoDriverRegPtr,&dwSize)) {
    goto cleanup;
  }

  const char *szMachStr="Machine\\";
  char *pMachineStrEnd=strstr(VideoDriverRegPtr,szMachStr);
  if(pMachineStrEnd==NULL) {
      errorLog << "couldnt find '"<<szMachStr<< "' in VideoDrvrRegPtr!\n";
      goto cleanup;
  }

  pMachineStrEnd+=strlen(szMachStr);

  retVal=RegOpenKeyEx(HKEY_LOCAL_MACHINE, pMachineStrEnd,0,KEY_READ,&hVidDriverKey);
  if ((ERROR_SUCCESS != retVal) || (hVidDriverKey==NULL)) {
    errorLog << "regOpenKey RO failed for "<<VideoDriverRegPtr<<", err=" << GetLastError() << endl;
    goto cleanup;
  }

  const char *szHWInfo="HardwareInformation.MemorySize";
  BYTE MemSize[4];
  dwSize=4;
  if(ERROR_SUCCESS != RegQueryValueEx(hVidDriverKey, szHWInfo, 0, &dwType, (LPBYTE)MemSize,&dwSize)) {
       errorLog << "regGetVal failed for "<<szHWInfo<<", err=" << GetLastError() << endl;
       goto cleanup;
  }

  VidMemSize = *((DWORD*)&MemSize);

  const char *szDevDesc = "Device Description";
  dwSize=REGPTRSIZE;
  if(ERROR_SUCCESS != RegQueryValueEx(hVidDriverKey, "Device Description", 0, &dwType, (LPBYTE)VideoDriverRegPtr,&dwSize)) {
       errorLog << "regGetVal failed for "<<szDevDesc<<", err=" << GetLastError() << endl;
       goto cleanup;
  }

  errorLog << "GetRegVidMem returns " << (VidMemSize >> 20) << "MB for " << VideoDriverRegPtr << endl;

cleanup:

  SAFE_REGCLOSEKEY(hDevMapKey);
  SAFE_REGCLOSEKEY(hVidDriverKey);
  return VidMemSize;
}

bool SysInfo::
IsBadVidMemCheckCard(DDDEVICEIDENTIFIER2 *pDevInfo) {
  // right now, just ignore results for all intel cards (i810, etc),
  // which use system memory to supplement onboard and so work OK, but
  // report low onboard mem values.  actually i740 is probably ok, but whatever.
  return (pDevInfo->dwVendorId==GfxVendorIDs::Intel);
}

void SysInfo::
CheckForBadMouseCursorDriver(/*DDDEVICEIDENTIFIER2 *pDevInfo,const ULARGE_INTEGER *pDrvVer,SYSTEMTIME &DriverDate*/void) {

  switch(_VideoDeviceID.dwVendorId) {
      case GfxVendorIDs::ATI:
           switch(_VideoDeviceID.dwDeviceId) {
               //RADEON 8500 (R200)
               case 0x514C:
               case 0x514E:
               case 0x514F:
               case 0x4242:
               //(All-In-Wonder Radeon 8500DV)

               //RADEON 7500 (RV200)
               case 0x5157:

               //MOBILITY RADEON 7500 (M7 - RADEON 7500 based)
               case 0x4C57:

               //RADEON VE / RADEON 7000 (RV100 - low-cost RADEON, dual CRT but no TCL)
               case 0x5159:
               case 0x515A:

               //RADEON / RADEON 7200 (R100)
               case 0x5144:
               case 0x5145:
               case 0x5146:
               case 0x5147:
               //MOBILITY RADEON (M6 - RADEON VE based)
               case 0x4C59:
               case 0x4C5A:

                 if(_os_type >= SysInfo::OS_Win2000) {
                     if((LOWORD(_VideoDeviceID.liDriverVersion.LowPart)<6166) &&
                        ((_VideoDriverDate.wYear<2002) ||
                         ((_VideoDriverDate.wYear==2002) &&
                          (_VideoDriverDate.wMonth<=6)))) {
                         _bHas_custom_mousecursor_ability = false;
                     }
                 }
                 break;
           }
           break;

      case GfxVendorIDs::Intel:
           switch(_VideoDeviceID.dwDeviceId) {
              case 0x00007121:
              case 0x00007123:
              case 0x00007125: {
                 if(_os_type >= SysInfo::OS_Win2000)
                     _bHas_custom_mousecursor_ability = false;
                 break;
              }
           }
           break;

      // Trident
      case GfxVendorIDs::Trident:
           // I no longer trust any trident card to do XP cursors right, so until I know otherwise
           // no trident gets the custom cursor
           if(_os_type >= SysInfo::OS_Win2000) {
               _bHas_custom_mousecursor_ability = false;
               break;
           }

           switch(_VideoDeviceID.dwDeviceId) {
              // cyberbladeXP
              case 0x8820:
              case 0x9910:
                 if(_os_type >= SysInfo::OS_Win2000)
                     _bHas_custom_mousecursor_ability = false;
                 break;
           }
           break;
  }
}

// if pbIsBadDriver!=NULL, check for bad drivers and reject based on those too...
// DriverDate not reliable enough to reject on, must use file versions
bool SysInfo::ValidateCardTypeandDriver(void) {
  bool bIsBadCard=false;
  bool bIsBadDriver=false;
  const char *update_driver_link="Unknown";

 //#define BLOCK_OLD_I810_DRIVERS
 #ifdef BLOCK_OLD_I810_DRIVERS
  const char *INTEL_i810_URL="http://support.intel.com/support/graphics/intel810/index.htm";
 #endif

  if(!_bValidVideoDeviceID) {
      errorLog << "ValidateCardTypeandDriver: haven't retrieved valid deviceID yet, skipping\n";
      return true;
  }

  if(_bDoneVidMemCheck && (!IsBadVidMemCheckCard(&_VideoDeviceID))) {
     if((_VideoRamTotalBytes>0) && (_VideoRamTotalBytes < 2300000)) {
          // dwTotal==0 usually means driver doesnt implement GetAvailVidMem (hello FireGL2)
          // *pbTryOtherAPIs = false;
          SET_BOTH_ERROR("Your video adapter (" << _VideoDeviceID.szDescription << ") indicates it has only "
              << (_VideoRamTotalBytes/(float)ONE_MB_BYTES) << " MB. Toontown requires an adapter with at least 4MB of video memory.  If you believe this is incorrect, please reboot your system, close applications using 3D resources, and/or reduce your screen resolution to 640x480.");
          return false;
     }
  }

  // check for bad card types
  switch(_VideoDeviceID.dwVendorId) {

      case GfxVendorIDs::ATI:  {
         #if 0
           // this should catch Rage Pros, which cant
           // do transparency right.   hopefully no false positives in this range

           // actually Rage (pro) XL's can do transparency ok
           if((_VideoDeviceID.dwDeviceId>=0x4700)&&(_VideoDeviceID.dwDeviceId<=0x4800)) {
              bIsBadCard=true;
              break;
           }
         #endif

           // catch Rage Pro Mobility, but NOT Rage 128 Mobility, which has IDs like 0x4C45
           // catch older Rage II's too, even tho they'd probably be rejected for other reasons
           switch(_VideoDeviceID.dwDeviceId) {
             #if 0
               //RAGE XL definitely seem OK
               // RAGE XL (RAGE PRO based)
               case 0x474D:  // this one verified good
               case 0x474F:
               case 0x4752:

                // RAGE MOBILITY M/M1/P (RAGE PRO based)
                case 0x4C4D:
                case 0x4C52:

                // RAGE LT-PRO (RAGE PRO based)
                case 0x4C42:
                case 0x4C49:
                case 0x4C50:

                // RAGE XC (RAGE PRO based)
                case 0x474C:
                case 0x474E:

                case 0x4744:
                case 0x4749:
                case 0x4750:

               // RAGE PRO
               case 0x4742:
                  // My known bad blending '97 Rage is 0x4742, Subsys: 0x0, Revision: 0x05C
                  // user says his works, so allow this one through too
              #endif


                // RAGE LT (RAGE II based)
               case 0x4C47:

                // RAGE IIC AGP
                case 0x4757:
                case 0x4759:
                case 0x475A:

                // RAGE IIC PCI
                case 0x4756:
                case 0x5656:

                // RAGE II+
                case 0x4755:

                // RAGE II
                case 0x4754:
                   bIsBadCard=true;
           }
           break;
      }

      case GfxVendorIDs::_3DFX:  {
           // this should catch voodoo1/2, which have no cursor, and I havent tried using
           // dx8 sw cursor on (they have dx6 drivers, so theoretically it should work)
           // havent tested voodoo rush or banshee, so let them through for now
           if(_VideoDeviceID.dwDeviceId<=0x2)
              bIsBadCard=true;
           break;
      }

      case GfxVendorIDs::Trident:  {
           //  Trident 3D Image 9750 PCI/AGP (v6.45.5423a.98) has only 2MB vidmem
           if(_VideoDeviceID.dwDeviceId==0x9750)
              bIsBadCard=true;
           break;
      }

      case GfxVendorIDs::S3:  {
           // this should catch at least 1 kind of s3 virge.
           // need to do some research to find other virge dev_ids
           // not sure if we need to add the s3 laptop cards also
           if(_VideoDeviceID.dwDeviceId==0x5631)
              bIsBadCard=true;
           break;
      }

      case GfxVendorIDs::Intel: {
          switch(_VideoDeviceID.dwDeviceId) {
              // i810
              case 0x00007121:
              case 0x00007123:
              case 0x00007125: {
                  // comment out the i810 driver block for now and see what kind of problems we get
                  // dont want to frustrate users unnecessarily
                  #ifdef BLOCK_OLD_I810_DRIVERS
                    // _graphics_card_type = GfxCardType::Intel_i810;
                    unsigned majorver=6;
                    if(_os_type < SysInfo::OS_WinNT) {
                        majorver=4;
                    }

                     if(!verify_version(*pDrvVer,majorver,13,1,3196)) {
                           bBadDriver=true;
                           update_driver_link = INTEL_i810_URL;
                     }
                  #endif
                    break;
              }
          }
      }
  }

  if(bIsBadDriver) {
      errorLog << "Obsolete Driver Detected: " << _VideoDeviceID.szDescription << "\nprinting error and exiting\n";

      // ignore bPrintUserError because we wont be called again if BadDrvr is true

      // originally I was going to put the card specific links in php so
      // you wouldnt have to update the control to change the links, (that's
      // what the unused canonical card type stuff is all about) but
      // this is good enough for now
      _gfx_report_str << "Your graphics adapter (" << _VideoDeviceID.szDescription
        << ") requires an updated video driver to run Toontown without problems.  You can download and install the latest driver for your OS from <a href=\"" << update_driver_link
        << "\">"<< update_driver_link <<"</a>." << endl;
  } else if(bIsBadCard) {
      errorLog << "Bad Card Detected: " << _VideoDeviceID.szDescription << endl;
      _gfx_report_str << "Your graphics adapter (" << _VideoDeviceID.szDescription
            << ") lacks the ability to run Toontown.  See <a href=\"http://www.toontown.com/faq.php#hardware\">http://www.toontown.com/faq.php</a> "
            << "for a list of graphics cards known to run Toontown successfully.  "
            << "Most cards no more than 2 years old should work."
            << endl;
  } else {
     // dont bother unless driver is known good
     CheckForBadMouseCursorDriver(/*pDevInfo,pDrvVer,DriverDate_SysTime*/);
  }

  return !(bIsBadCard || bIsBadDriver);
}

SysInfo::GAPIType SysInfo::
GetPreferredGAPI(void) const {
  if(!_bValidVideoDeviceID) {
      errorLog << "GetPreferredAPI: haven't retrieved valid deviceID yet, skipping\n";
      return GAPI_Unknown;
  }

// dbg-only flags
#if defined(PREFER_OPENGL)
  errorLog << "Preferring OpenGL selection for debugging purposes\n";
  return GAPI_OpenGL;
#elif defined(PREFER_DX8)
  errorLog << "Preferring DX8 selection for debugging purposes\n";
  return GAPI_DirectX_8_1;
#elif defined(PREFER_DX7)
  errorLog << "Preferring DX7 selection for debugging purposes\n";
  return GAPI_DirectX_7;
#endif

  const DDDEVICEIDENTIFIER2 *pDeviceID=&_VideoDeviceID;

  GAPIType preferred_api=GAPI_DirectX_8_1;

  if((pDeviceID->dwVendorId==GfxVendorIDs::Nvidia_STB) &&
     ((pDeviceID->dwDeviceId==0x0018)||(pDeviceID->dwDeviceId==0x0019))) {
      errorLog << "Detected Nvidia Riva128, preferring OGL\n";
      preferred_api=GAPI_OpenGL;

      // bugbug: need to prefer OGL for Intel i740  which is buggy on DX too
      //         also, cards that get better perf on opengl (like GeForce2??)
  } else if((pDeviceID->dwVendorId==GfxVendorIDs::SiS) &&
            (pDeviceID->dwDeviceId==0x6326)) {
      errorLog << "Detected SiS 6326, preferring DX7\n";
      preferred_api=GAPI_DirectX_7;
  } else {
      // cvt desc str to lower case
      char desc[MAX_DDDEVICEID_STRING];
      strncpy(desc,pDeviceID->szDescription,MAX_DDDEVICEID_STRING);
      _strlwr(desc);  // cvt to lower case
      string DeviceDescStr(desc);
      if(DeviceDescStr.find("fire gl")!=string::npos) {
          errorLog << "Detected ATI Fire GL, preferring OGL\n";
          preferred_api=GAPI_OpenGL;
      }
  }

  return preferred_api;
}

void SysInfo::
SetVideoCardConfigInfo(UINT AdapterNum, DDDEVICEIDENTIFIER2 *pDeviceID,SYSTEMTIME *pDriverDate_SysTime)
{
    memcpy(&_VideoDeviceID,pDeviceID,sizeof(DDDEVICEIDENTIFIER2));
    memcpy(&_VideoDriverDate,pDriverDate_SysTime,sizeof(SYSTEMTIME));
    _bValidVideoDeviceID = true;

    errorLog << "Detected DX Card[" << AdapterNum << "]: " << pDeviceID->szDescription << endl <<
            "Driver Version: (" << PRINTDRIVER_VERSTR(pDeviceID->liDriverVersion) <<
            ") Date: (" <<_VideoDriverDate.wMonth << "/" <<_VideoDriverDate.wDay << "/"
                        <<_VideoDriverDate.wYear <<
            ") DriverName: " << pDeviceID->szDriver <<
             "; VendorID: 0x" << (void*)pDeviceID->dwVendorId <<
             "; DeviceID: 0x" << (void*)pDeviceID->dwDeviceId <<
             "; SubsysID: 0x" << (void*) pDeviceID->dwSubSysId <<
             "; Revision: 0x" << (void*) pDeviceID->dwRevision << endl;

    _VideoCardNameStr = pDeviceID->szDescription;

    char buf[50];
    sprintf(buf,"0x%X",pDeviceID->dwVendorId);
    _VideoCardVendorIDStr =  buf;
    sprintf(buf,"0x%X",pDeviceID->dwDeviceId);
    _VideoCardDeviceIDStr =  buf;
    sprintf(buf,"0x%X",pDeviceID->dwSubSysId);
    _VideoCardSubsysIDStr =  buf;
    sprintf(buf,"0x%X",pDeviceID->dwRevision);
    _VideoCardRevisionIDStr =  buf;

    _VideoCardVendorID = pDeviceID->dwVendorId;
    _VideoCardDeviceID = pDeviceID->dwDeviceId;
    _VideoCardSubsysID = pDeviceID->dwSubSysId;
    _VideoCardRevisionID = pDeviceID->dwRevision;

    LARGE_INTEGER *pDrvVer = &pDeviceID->liDriverVersion;
    sprintf(buf,"%d.%d.%d.%d",HIWORD(pDrvVer->HighPart),LOWORD(pDrvVer->HighPart),HIWORD(pDrvVer->LowPart),LOWORD(pDrvVer->LowPart));
    _VideoCardDriverVerStr = buf;
    sprintf(buf,"%d/%d/%d",_VideoDriverDate.wMonth,_VideoDriverDate.wDay,_VideoDriverDate.wYear);
    _VideoCardDriverDateStr = buf;
    _VideoCardDriverDateMon = _VideoDriverDate.wMonth;
    _VideoCardDriverDateDay = _VideoDriverDate.wDay;
    _VideoCardDriverDateYear = _VideoDriverDate.wYear;
}
