// Filename: sysinfo.h
// Created by:  jimbob (09Jan97)
// $Id$
//
////////////////////////////////////////////////////////////////////
#ifndef SYSINFO_H
#define SYSINFO_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#undef WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <ddraw.h>
#include <psapi.h>
#include <string>
#include <sstream>  // stringstream easier to use than strstream, no memleaks or 'ends' reqd
using namespace std;

HRESULT DxDiag_Init(void);
HRESULT PrintDxDiagDisplayInfo(void);

////////////////////////////////////////////////////////////////////
//       Class : SysInfo
// Description :
////////////////////////////////////////////////////////////////////
class SysInfo
{
public:
  #include "sysinfodefs.h"
public:
  ostringstream _gfx_report_str;

  SysInfo(void);
  SysInfo::~SysInfo(void);
  bool write_log_file(const char *logfilename);
  static bool get_available_space(const char *dirname, unsigned __int64 &free_bytes);
//  inline OSType get_os_type(void) const { return os_type; }
  static OSType get_os_type(void);
  static float get_os_servicepack_version(void);
  string get_os_namestr(void);
//  inline CPUType get_cpu_type(void) const { return cpu_type; }
//  inline int get_cpu_level(void) const { return cpu_level; }
  inline bool get_mouse_enabled(void) const { return _mouse_enabled; }
  void check_language_info(void);
  bool has_custom_mousecursor_ability(void) const { return _bHas_custom_mousecursor_ability; }
  inline float get_ram_megs_total(void) const { return _ram_megs_total; }
  inline GAPIType get_suggested_gfx_api(void) const { return _gfx_api_suggested; }
  string get_gfx_api_name(GAPIType gapi) const;
  inline bool get_3d_hw(void) const { return _has_3d_hw; }
  inline bool get_sound_enabled(void) const { return _sound_enabled; }
  inline int get_max_baud(void) const { return _comm_baud; }
#if defined(USE_DX9)
  void Test_DX9(bool bWhatever);
#endif
  void Test_DX8(bool bIsDX81);
#if defined(USE_DX7)
  void Test_DX7(bool bPrintUserErrors);
#endif
  void Test_OpenGL(void);
  bool ValidateCardTypeandDriver(void);
  bool IsBadVidMemCheckCard(DDDEVICEIDENTIFIER2 *pDevInfo);
  DWORD GetVidMemSizeFromRegistry(void);
  void CheckForBadMouseCursorDriver(void);
  GAPIType GetPreferredGAPI(void) const;
  void PrintProcessMemInfo(HANDLE hProcess);
  // static so we dont have to do the 'run TT' path to get this info
  static void print_os_info(void);
  static bool IsNTAdmin(void);
  // const char *GetGraphicsCardCanonicalName(void);
  void SetVideoCardConfigInfo(UINT AdapterNum, DDDEVICEIDENTIFIER2 *pDeviceID,SYSTEMTIME *pDriverDate_SysTime);
  void PrintNo3DHWMsg(void);
  void SetGeneric3DError(char *LogError);

protected:
  void check_os(void);
  void check_cpu(void);
  void check_mouse(void);
  void check_ram(void);
  void check_3d_hw(void);
  void check_snd(void);
  void check_net_connection(void);
  int get_commport_baud(const char *cportname);
  void get_country_info(HINSTANCE hKernel);

public:
  string _CPUNameStr,_CPUMakerStr,_CPUTypeStr;
  DWORD _NumCPUs, _CPUMhz;

  OSType        _os_type;
  float         _OSServicePackVer;  // e.g. 3.5 if service pack 3, minor ver 5 is installed

  bool          _mouse_enabled;
  int           _mouse_buttons;
  bool          _bHas_custom_mousecursor_ability;

  float         _ram_megs_total;
  float         _ram_megs_available;

  bool          _has_3d_hw;

  bool          _forbidOpenGL;  // dbg flag
  GAPIType      _dx_level_installed;
  GAPIType      _gfx_api_suggested;  // what we tell configrc.exe
#if defined(USE_DX7)
  GfxCheckStatus _DX7_status;
#endif
  GfxCheckStatus _DX8_status,_OpenGL_status;
#if defined(USE_DX9)
  GfxCheckStatus _DX9_status;
#endif
  DDDEVICEIDENTIFIER2 _VideoDeviceID;
  SYSTEMTIME          _VideoDriverDate;
  bool                _bValidVideoDeviceID;

  // GfxCardType _graphics_card_type;
  string _DXVerStr;

  bool _sound_enabled;
  CommType _comm_type;
  int      _comm_baud;

  time_t    _startup_time;
  HINSTANCE _hPsAPI;

  bool      _bNetworkIsLAN;

  string _KeybdLayoutStr;
  string _LangIDStr;
  string _LocaleIDStr;
  string _CountryNameStr;

  string _IEVersionStr;
  double _IEVersionNum;  // float so you can represent IE 5.5, etc
  string _IPAddrStr;
  string _MACAddrStr;

  string _VideoCardNameStr;
  DWORD  _VideoCardVendorID;
  string _VideoCardVendorIDStr;
  DWORD  _VideoCardDeviceID;
  string _VideoCardDeviceIDStr;
  DWORD  _VideoCardSubsysID;
  string _VideoCardSubsysIDStr;
  DWORD  _VideoCardRevisionID;
  string _VideoCardRevisionIDStr;
  string _VideoCardDriverDateStr;
  string _VideoCardDriverVerStr;
  DWORD  _VideoCardDriverDateMon;
  DWORD  _VideoCardDriverDateDay;
  DWORD  _VideoCardDriverDateYear;
  bool   _bDoneVidMemCheck;
  DWORD  _VideoRamTotalBytes;
  DWORD  _numMonitors;

  string _OGLVendorNameStr;
  string _OGLRendererNameStr;
  string _OGLVerStr;

  /* this stuff must come from configrc via the registry
  string _ScreenModeStr;
  */
  // 1 string contains fields for all devices.  may want to break this out further l8r
  string _MidiOutAllDevicesStr;
  string _DSoundDevicesStr;

  // catch-all string for all other unanticipated data to store on stat server
  string _ExtraStr;

  // MS misspelt 'performance' in psapi.h.  duh.
  typedef BOOL (WINAPI *GETPERFINFO)(PPERFORMACE_INFORMATION pPerformanceInformation,DWORD cb);
  typedef BOOL (WINAPI *GETPROCESSMEMORYINFO)(HANDLE Process,PPROCESS_MEMORY_COUNTERS ppsmemCounters,DWORD cb);
  typedef void (WINAPI *GNSI)(LPSYSTEM_INFO si);
  GETPERFINFO _pGetPerfInfo;
  GETPROCESSMEMORYINFO _pGetProcessMemoryInfo;
  GNSI _pGetSystemInfo;

  static GNSI getSystemInfoProc();
};

#define SET_USER_ERROR(LOGSTR,USERSTR) {  \
    errorLog << LOGSTR << endl;           \
    _gfx_report_str << USERSTR << endl; }

#define ONE_MB_BYTES (1<<20)
#define SAFE_RELEASE(P) { if((P)!=NULL) { (P)->Release();  (P) = NULL; }  }
#define SAFE_FREELIB(hLIB) { if((hLIB)!=NULL) { FreeLibrary(hLIB); (hLIB) = NULL; } }
#define SAFE_DELETE(P) { if((P)!=NULL) { delete (P);  (P) = NULL; }  }
#define SAFE_DELETE_ARRAY(P) { if((P)!=NULL) { delete [] (P);  (P) = NULL; }  }
#define SAFE_REGCLOSEKEY(HKEY) { if((HKEY)!=NULL) { RegCloseKey(HKEY);  (HKEY) = NULL; }  }
#define SET_BOTH_ERROR(LOGSTR) SET_USER_ERROR(LOGSTR,LOGSTR)
extern void SearchforDriverInfo(const char *driver_filename,ULARGE_INTEGER *pli,SYSTEMTIME *pDriverDate);
extern void MyGetModuleVersion(HMODULE hMod, ULARGE_INTEGER *pli);
extern void MyGetFileVersion(char *FileName, ULARGE_INTEGER *pli);
extern HWND CreateOpenGLWindow(char *title, int pixfmtnum, PIXELFORMATDESCRIPTOR *pPFD, int x, int y, int width, int height, BYTE type, DWORD flags,HDC *hDC);
extern void ShowErrorBox(const char *msg);

// these flags are for debugging only.  might be better to use dbg-only regkeys so dont have to rebuild (but then have to include dbg code)
//#define FORBID_OPENGL
//#define FORBID_DX8
//#define FORBID_DX7

//#define FORCE_OPENGL
//#define FORCE_DX7   // skip DX8

//#define PREFER_DX7
//#define PREFER_DX8
//#define PREFER_OPENGL

#define PRINTDRIVER_VERSTR(LARGEINT_VER) HIWORD(LARGEINT_VER.HighPart) << "." << LOWORD(LARGEINT_VER.HighPart) << "." << HIWORD(LARGEINT_VER.LowPart) << "." << LOWORD(LARGEINT_VER.LowPart)
#define LARGEINT_EQUAL(LI1,LI2) ((LI1.HighPart==LI2.HighPart)&&(LI1.LowPart==LI2.LowPart))
#endif
