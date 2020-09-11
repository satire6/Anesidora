#if defined(USE_DX7)

#include "pragma.h"
#include <windows.h>
#include <ddraw.h>
#include <d3d.h>
#include <dsound.h>
#include <iostream>
#include <fstream>
#include <string>
#include <malloc.h>
#include <assert.h>
#include "log.h"
#include "sysinfo.h"

typedef HRESULT (WINAPI *DDRAWCREATEEX_PROC)(GUID FAR *,LPVOID *,REFIID, IUnknown FAR *);
typedef HRESULT (WINAPI *DDRAWCREATE_PROC)(GUID FAR *,LPDIRECTDRAW FAR *lplpDD, IUnknown FAR *pUnkOuter);
typedef HRESULT (WINAPI *DDRAWENUMEX_PROC)(LPDDENUMCALLBACKEX,LPVOID,DWORD);

//#error need to address getvidmem mode.  what msgs are printed?

//#define SET_GENERIC_3D_ERROR("SysInfo::check_3d_hw() - DirectDrawEnumerateEx() failed, hr = 0x" << (void*)hr);

// right now this is basically to look for voodoo1/2, which we dont use anyway
BOOL WINAPI DirectDrawEnumDevicesCallback(GUID FAR *lpGUID, LPSTR lpDriverDescription,
                                          LPSTR lpDriverName, LPVOID lpContext, HMONITOR hm) {
  // hm is NULL for the primary display device, 3d-only devices, and devices not attached
  // to the desktop.
  // skip all others
  if (NULL != hm)
    return 1; // continue enumeration

  // primary display driver will have NULL guid
  // ignore that and save any non-null value, which
  // indicates a secondary driver, which is usually voodoo1/2
  if(lpGUID!=NULL) {
    errorLog << "Found a 3D-only display device (voodoo1/2, etc.)" << endl;
    // copy the GUID out
    memcpy(lpContext,lpGUID,sizeof(GUID));
    return 0; // halt enumeration
  }

  return 1; // continue enumeration
}

HRESULT CALLBACK Direct3DEnumDevicesCallback(LPSTR lpDeviceDescription,
  LPSTR lpDeviceName, LPD3DDEVICEDESC7 lpD3DDeviceDesc, LPVOID lpContext) {

  if (lpD3DDeviceDesc->dwDevCaps & D3DDEVCAPS_HWRASTERIZATION) {
    (*((bool*)lpContext)) = true;
  }

  return D3DENUMRET_OK;
}

// in GetVidMemMode, no errors will be echoed to the user
void SysInfo::
Test_DX7(bool bPrintUserErrors) {
  HINSTANCE ddhinst = NULL;
  GUID driverGUID;
  GUID nullGUID;
  GUID *pDriverGUID;
  LPDIRECTDRAW7 pdd = NULL;
  LPDIRECT3D7 pd3d = NULL;
  DDRAWENUMEX_PROC ddEnumEx = NULL;
  DDRAWCREATEEX_PROC ddCreateEx = NULL;
  HRESULT hr;

  if(_DX7_status != Status_Unknown) {
      errorLog << "DX7 status already found to be " << ((_DX7_status==Status_Unsupported) ? "un":"") << "supported\n";
      return;
  }

  _DX7_status = Status_Unsupported;

  if(!bPrintUserErrors) {
      // in this case, we already should have a valid api, so dont tell user if we get errors
      errorLog << "Using DX7 to find vidmem size\n";
  }

  #ifdef FORBID_DX7
     errorLog << "Disallowing DX7 selection for debugging purposes\n";
     return;
  #endif

  //*pbTryOtherAPIs = true;    // usually true, unless we detect a bad card or driver

#define SET_GEN_3D_ERROR(LOGSTR) { \
      errorLog << LOGSTR << endl;  \
      if(bPrintUserErrors)        \
         SetGeneric3DError(NULL);  \
      }

  // apparently there is a bug in DX6/7 GetDeviceIdentifier which causes it to write 4 extra bytes
  // beyond end of DDDEVICEIDENTIFIER2 struct, so alloc space for that
  typedef struct {
      DDDEVICEIDENTIFIER2 id;
      DWORD               padding;
  } MY_DX7_DEVID;

  MY_DX7_DEVID DeviceID;
  DDDEVICEIDENTIFIER2 *pDeviceID=&DeviceID.id;
  ZeroMemory(&DeviceID, sizeof(DDDEVICEIDENTIFIER2));

  bool bEnumDevicesDetectedHWSupport = false;

  const char *szDDRAW_NAME="ddraw.dll";
  // look for DirectX 7
  ddhinst = LoadLibrary(szDDRAW_NAME);

  if (!ddhinst) {
    DWORD err=GetLastError();
    errorLog << "LoadLib "<<szDDRAW_NAME<<" failed, err=" << err << endl;

    if(err==ERROR_GEN_FAILURE) {
        // missing dlls or dll exports
        const char *errmsg="DirectX could not initialize, your DirectX installation may be corrupt.  Please reinstall DirectX from <a href=\"http://www.microsoft.com/directx\">http://www.microsoft.com/directx</a>.";
        if(bPrintUserErrors) {
            _gfx_report_str << errmsg << endl;
            ShowErrorBox(errmsg);
        }
    } else {
        if(bPrintUserErrors) {
            _gfx_report_str << "DirectX 7 or newer was not detected.  Toontown requires either DirectX 7 or newer to be installed, or OpenGL acceleration support to be provided by your video card adapter.  Please visit <a href=\"http://www.microsoft.com/directx\">http://www.microsoft.com/directx</a> to download an updated DirectX version, or check with your video card manufacturer for updated video drivers." << endl;
        }
    }

    goto _dx_cleanup;
  }

  const char *szDDCreateExStr = "DirectDrawCreateEx";
  ddCreateEx = (DDRAWCREATEEX_PROC)GetProcAddress(ddhinst, szDDCreateExStr);
  if (NULL == ddCreateEx) {
      // this is not necessarily an error, if card has OGL support its OK.
      // but we will set the _gfx_error_string anyway, in case OGL detection also fails

      errorLog << "DirectX 7 or newer was not detected in " << szDDRAW_NAME << endl;
      if(bPrintUserErrors)
           _gfx_report_str << "DirectX 7 or newer is not installed.  Toontown requires either DirectX 7 or newer to be installed, or OpenGL acceleration support to be provided by your video card adapter.  Please visit <a href=\"http://www.microsoft.com/directx\">http://www.microsoft.com/directx</a> to download an updated DirectX version, or check with your video card manufacturer for updated video drivers." << endl;
      goto _dx_cleanup;
  }

  errorLog << "DirectX 7 api's are present\n";

  // first get device info for primary adapter and check for bad drivers, later we call ddCreateEx again with final device guid we choose
  hr = (*ddCreateEx)(NULL, (void**)&pdd, IID_IDirectDraw7, NULL);
  if (hr != DD_OK) {
      errorLog << szDDCreateExStr << " failed, hr=";
      if(hr == DDERR_NODIRECTDRAWHW) {
          errorLog << "DDERR_NODIRECTDRAWHW";
      } else {
          SET_GEN_3D_ERROR("0x" << (void*)hr);
      }
      errorLog << endl;
      goto _dx_cleanup;
  }
  hr = pdd->GetDeviceIdentifier(pDeviceID, 0x0);
  SYSTEMTIME DriverDate_SysTime;

  if(FAILED(hr)) {
      errorLog << "Error in GetDeviceIdentifier: hr=0x" << (void*)hr << endl;
  } else {
      if((pDeviceID->liDriverVersion.HighPart==0) && (pDeviceID->liDriverVersion.LowPart==0)) {
          // this must always be done on win2k/NT where ddraw always returns 0 for the drvr version #
          SearchforDriverInfo(pDeviceID->szDriver,(ULARGE_INTEGER*)&pDeviceID->liDriverVersion,&DriverDate_SysTime);
      } else {
          // we already have valid version info, just need date
          SearchforDriverInfo(pDeviceID->szDriver,NULL,&DriverDate_SysTime);
      }

      // dont reset info if we're just getting vidmemsize
      if(bPrintUserErrors)
          SetVideoCardConfigInfo(0,pDeviceID,&DriverDate_SysTime);
  }

  // pick a ddraw device -- check for voodoo1/2-style 3d-only card
  // currently we're using these cards if they're present -- eventually,
  // probably want to be a bit more clever about selection of 3d device
  ZeroMemory(&driverGUID, sizeof(GUID));
  ZeroMemory(&nullGUID, sizeof(GUID));
  pDriverGUID = NULL;

  // get the func ptr for DirectDrawEnumerateEx
  const char *szDDrawEnumStr="DirectDrawEnumerateExA";
  ddEnumEx = (DDRAWENUMEX_PROC)GetProcAddress(ddhinst,szDDrawEnumStr);
  if (NULL == ddEnumEx) {
    SET_GEN_3D_ERROR("GetProcAddr(" << szDDrawEnumStr << ") failed, err= " << GetLastError());
    // use the default device on error
  } else {
    // check for voodoo-style 3d cards
    hr = (*ddEnumEx)(DirectDrawEnumDevicesCallback, &driverGUID, DDENUM_NONDISPLAYDEVICES);
    if (FAILED(hr)) {
      SET_GEN_3D_ERROR(szDDrawEnumStr << " failed, hr = 0x" << (void*)hr);
      goto _dx_cleanup;
    }

    // if driverGUID is non-null, the enum callback found a voodoo.
    if (memcmp(&driverGUID, &nullGUID, sizeof(GUID))!=0) {
      // use the voodoo's GUID.
      pDriverGUID = &driverGUID;
      bEnumDevicesDetectedHWSupport = true;
    }
  }

  if(pDriverGUID!=NULL) {
      // not creating the primary ddraw obj, so release the primary one and recreate
      SAFE_RELEASE(pdd);

      // create the final ddraw object
      hr = (*ddCreateEx)(pDriverGUID, (void**)&pdd, IID_IDirectDraw7, NULL);
      if (FAILED(hr)) {
          SET_GEN_3D_ERROR(szDDCreateExStr << " failed, hr = 0x" << (void*)hr);
          goto _dx_cleanup;
      }
  }

  // create a d3d object so we can check for 3d HW devices
  hr = pdd->QueryInterface(IID_IDirect3D7, (void**)&pd3d);
  if (FAILED(hr)) {
    SET_GEN_3D_ERROR("QI for Direct3D 7 interface failed, hr = 0x" << (void*)hr);
    goto _dx_cleanup;
  }

  hr = pd3d->EnumDevices(Direct3DEnumDevicesCallback, &bEnumDevicesDetectedHWSupport);
  if (FAILED(hr)) {
    SET_GEN_3D_ERROR("D3D7->EnumDevices failed, hr = 0x" << (void*)hr);
    goto _dx_cleanup;
  }

  if(!bEnumDevicesDetectedHWSupport) {
    errorLog << "D3D7->EnumDevices found no hardware Direct3D devices" << endl;
    goto _dx_cleanup;
  }

  // not doing this for dx8, since any dx8 card will have > 4MB.  but for stat survey, we still
  // want to get total vidram megs.  will do it in client and write to registry

  // want to fail any gfx card < 4MB, since that's not enough for TT
  // would be better to use WMI to get Win32_VideoController.AdapterRAM here, but WMI not installed on w98 by default.

  DDSCAPS2 ddsCaps;
  DWORD dwTotal,dwFree;
  ZeroMemory(&ddsCaps,sizeof(DDSCAPS2));
  ddsCaps.dwCaps = DDSCAPS_VIDEOMEMORY | DDSCAPS_LOCALVIDMEM;  // dont include AGP mem
  if(FAILED(hr = pdd->GetAvailableVidMem(&ddsCaps,&dwTotal,&dwFree))) {
      errorLog << "GetAvailableVidMem failed, hr=";
      if(hr==DDERR_NODIRECTDRAWHW) {
          errorLog <<"DDERR_NODIRECTDRAWHW\n";
      } else {
          errorLog <<"0x" << (void*)hr << endl;
      }
      goto _dx_cleanup;
  }

  _VideoRamTotalBytes = dwTotal;
  _bDoneVidMemCheck = true;

  float recip_one_MB = 1.0f/(float)ONE_MB_BYTES;
  errorLog << "GetAvailVidMem returns Total: " << (dwTotal*recip_one_MB) << "MB, Free: " << (dwFree*recip_one_MB) << "MB for " << pDeviceID->szDescription << endl;

  if(bPrintUserErrors)
      errorLog << "Detected DX7 Direct3D hardware support\n";

  _DX7_status = Status_Supported;

 _dx_cleanup:
  SAFE_RELEASE(pd3d);
  SAFE_RELEASE(pdd);
  SAFE_FREELIB(ddhinst);
}

#if 0
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
SetVideoCardConfigInfo(UINT AdapterNum, DDDEVICEIDENTIFIER2 *pDeviceID,SYSTEMTIME *pDriverDate_SysTime) {
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
#endif

#endif	// USE_DX7
