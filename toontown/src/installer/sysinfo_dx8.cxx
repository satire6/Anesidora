// Filename: sysinfo_dx8.cxx
// Created by:  chris
//
// Separate from sysinfo.cxx because d3d8.h and d3d.h conflict,
// difficult to include them both and have everything be defined
// properly
////////////////////////////////////////////////////////////////////

// disable vc6.0 warning
#include "pragma.h"

#include <windows.h>
#include <ddraw.h>
#include <d3d8.h>
#include "log.h"
#include "sysinfo.h"

void SysInfo::Test_DX8(bool bIsDX81) {
    bool bFoundDX8Adapter=false;
    LPDIRECT3D8 pD3D8 = NULL;
    HRESULT hr;

    if(_DX8_status != Status_Unknown) {
          errorLog << "DX8 status already found to be " << ((_DX8_status==Status_Unsupported) ? "un":"") << "supported\n";
          return;
    }

    _DX8_status = Status_Unsupported;

    #ifdef FORBID_DX8
       errorLog << "Disallowing DX8 selection for debugging purposes\n";
       return;
    #endif

    #define D3D_DLLNAME "d3d8.dll"

    HINSTANCE hD3D8_DLL = LoadLibrary(D3D_DLLNAME);
    if(hD3D8_DLL == NULL) {
        DWORD err=GetLastError();

        errorLog << "LoadLibrary(" << D3D_DLLNAME ") failed, err=";
        if(err==ERROR_GEN_FAILURE) {
            errorLog << "ERROR_GEN_FAILURE\n";
             // missing dlls or dll exports (probably win98 only, since ME/XP/2000 has system file protection)
             const char *errmsg="DirectX could not initialize, your DirectX installation may be corrupt.  Please reinstall DirectX from http://www.microsoft.com/directx.";
             _gfx_report_str << errmsg << endl;
             ShowErrorBox(errmsg);
        } else {
            errorLog << err << endl;
        }
        return;
    }

    const char *szD3DCreateStr="Direct3DCreate8";
    typedef LPDIRECT3D8 (WINAPI *Direct3DCreate8_ProcPtr)(UINT SDKVersion);
    // dont want to statically link to possibly non-existent d3d8 dll, so must call D3DCr8 indirectly
    Direct3DCreate8_ProcPtr D3DCreate8_Ptr =
        (Direct3DCreate8_ProcPtr) GetProcAddress(hD3D8_DLL, szD3DCreateStr);

    if(D3DCreate8_Ptr == NULL) {
        errorLog << "GetProcAddr "<<szD3DCreateStr<<" failed, err=" << GetLastError() << endl;
        goto exit_cleanup;
    }

// these were taken from the 8.0 and 8.1 d3d8.h SDK headers
#define D3D_SDK_VERSION_8_0  120
#define D3D_SDK_VERSION_8_1  220

    UINT SDKver = (bIsDX81 ? D3D_SDK_VERSION_8_1 : D3D_SDK_VERSION_8_0);

    pD3D8 = (*D3DCreate8_Ptr)(SDKver);

    if(pD3D8==NULL) {
        errorLog << szD3DCreateStr << " failed!, err=" << GetLastError() << endl;
        goto exit_cleanup;
    }

    UINT numAdapters = pD3D8->GetAdapterCount();

    if(numAdapters>1) {
       errorLog << "D3D8 found " << numAdapters << " Video Adapters!\n";
    }

    for(int i=numAdapters-1;i>=0;i--) {
        D3DADAPTER_IDENTIFIER8 adapter_info;
        ZeroMemory(&adapter_info,sizeof(D3DADAPTER_IDENTIFIER8));
        hr = pD3D8->GetAdapterIdentifier(i,D3DENUM_NO_WHQL_LEVEL,&adapter_info);
        if(FAILED(hr)) {
            errorLog << "D3D GetAdapterID failed for device #" << i << endl;
            continue;
        }

        errorLog << "DI.VendorId: " << adapter_info.VendorId << endl;
        errorLog << "DI.DeviceId: " << adapter_info.DeviceId << endl;
        errorLog << "DI.SubSysId: " << adapter_info.SubSysId << endl;
        errorLog << "DI.Revision: " << adapter_info.Revision << endl;
        errorLog << "DI.Driver: " << adapter_info.Driver << endl;
        errorLog << "DI.Description: " << adapter_info.Description << endl;

        errorLog << "Product: " << HIWORD(adapter_info.DriverVersion.HighPart);
        errorLog << ".Version: " << LOWORD(adapter_info.DriverVersion.HighPart);
        errorLog << ".SubVersion: " << HIWORD(adapter_info.DriverVersion.LowPart);
        errorLog << ".Build: " << LOWORD(adapter_info.DriverVersion.LowPart) << endl;


        ULARGE_INTEGER *pDrvVer=(ULARGE_INTEGER*)&adapter_info.DriverVersion;

        SYSTEMTIME DriverDate_SysTime;
        SearchforDriverInfo(adapter_info.Driver,NULL,&DriverDate_SysTime);
        DDDEVICEIDENTIFIER2 DX7_DevID;

        // copy dx8 devinfo to dx7 struct
        DX7_DevID.dwVendorId=adapter_info.VendorId;
        DX7_DevID.dwDeviceId=adapter_info.DeviceId;
        DX7_DevID.dwSubSysId=adapter_info.SubSysId;
        DX7_DevID.dwRevision=adapter_info.Revision;
        strncpy(DX7_DevID.szDescription,adapter_info.Description,MAX_DEVICE_IDENTIFIER_STRING);
        strncpy(DX7_DevID.szDriver,adapter_info.Driver,MAX_DEVICE_IDENTIFIER_STRING);
        memcpy(&DX7_DevID.liDriverVersion,&adapter_info.DriverVersion,sizeof(LARGE_INTEGER));
        memcpy(&DX7_DevID.guidDeviceIdentifier,&adapter_info.DeviceIdentifier,sizeof(GUID));

        SetVideoCardConfigInfo(i,&DX7_DevID,&DriverDate_SysTime);

        D3DCAPS8 d3dcaps;
        hr = pD3D8->GetDeviceCaps(i,D3DDEVTYPE_HAL,&d3dcaps);
        if(FAILED(hr)) {
             if((hr==D3DERR_INVALIDDEVICE)||(hr==D3DERR_NOTAVAILABLE)) {
                 errorLog << "No DirectX 8 D3D-capable 3D hardware detected for device # "<<i<<" ("<<adapter_info.Description <<  ")!\n";
             } else {
                 errorLog << "GetDeviceCaps failed for device #"<<i<<", hr=0x" << (void*) hr << endl;
             }
             continue;
        }

        HMONITOR hMon=pD3D8->GetAdapterMonitor(i);
        if(hMon==NULL) {
            errorLog << "D3D8 Adapter[" << i << "]: has no monitor, seems to be disabled, skipping it\n";
            continue;
        }

        bFoundDX8Adapter=true;
    }

    if(!bFoundDX8Adapter) {
       errorLog << "Couldnt find a DX8-capable video card!\n";
    } else {
         errorLog << "Detected DX8 support\n";
        _DX8_status = Status_Supported;
    }

 exit_cleanup:
   SAFE_RELEASE(pD3D8);
   SAFE_FREELIB(hD3D8_DLL);
}

