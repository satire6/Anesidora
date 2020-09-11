// Filename: sysinfo_dx9.cxx
// Created by:  masad
// $Id$
////////////////////////////////////////////////////////////////////

// I'm not satisfied this is the best way to get the vidmem info, it could be a little slow, and
// since I cant unload wbem dlls, a memhog.  move to configrc.exe?
// (although it might be the only way to get the info on win9x)
#if defined(USE_DX9)

// disable vc6.0 warning
#include "pragma.h"
#define STRICT
#include <windows.h>
#include "log.h"
#include "sysinfo.h"
#include <vector>

#include <d3d9.h>

// they didnt bother putting the dxdiag guids in dxguid.lib, so gotta define em here
#define INITGUID
#include <initguid.h>
#include <dxdiag.h>

#define SAFE_BSTR_FREE(x)    if(x) { SysFreeString( x ); x = NULL; }
#define EXPAND(x)            x, sizeof(x)/sizeof(TCHAR)

struct DxDiagDisplayInfo {
    TCHAR m_szDeviceName[100];
    TCHAR m_szDescription[200];
    TCHAR m_szKeyDeviceID[200];
    TCHAR m_szKeyDeviceKey[200];
    TCHAR m_szManufacturer[200];
    TCHAR m_szChipType[100];
    TCHAR m_szDACType[100];
    TCHAR m_szRevision[100];
    TCHAR m_szDisplayMemoryLocalized[100];
    TCHAR m_szDisplayMemoryEnglish[100];
    TCHAR m_szDisplayModeLocalized[100];
    TCHAR m_szDisplayModeEnglish[100];

    DWORD m_dwWidth;
    DWORD m_dwHeight;
    DWORD m_dwBpp;
    DWORD m_dwRefreshRate;

    TCHAR m_szMonitorName[100];
    TCHAR m_szMonitorMaxRes[100];

    TCHAR m_szDriverName[100];
    TCHAR m_szDriverVersion[100];
    TCHAR m_szDriverAttributes[100];
    TCHAR m_szDriverLanguageEnglish[100];
    TCHAR m_szDriverLanguageLocalized[100];
    TCHAR m_szDriverDateEnglish[100];
    TCHAR m_szDriverDateLocalized[100];
    LONG  m_lDriverSize;
    TCHAR m_szMiniVdd[100];
    TCHAR m_szMiniVddDateLocalized[100];
    TCHAR m_szMiniVddDateEnglish[100];
    LONG  m_lMiniVddSize;
    TCHAR m_szVdd[100];

    BOOL m_bCanRenderWindow;
    BOOL m_bDriverBeta;
    BOOL m_bDriverDebug;
    BOOL m_bDriverSigned;
    BOOL m_bDriverSignedValid;
    DWORD m_dwDDIVersion;
    TCHAR m_szDDIVersionEnglish[100];
    TCHAR m_szDDIVersionLocalized[100];

    DWORD m_iAdapter;
    TCHAR m_szVendorId[50];
    TCHAR m_szDeviceId[50];
    TCHAR m_szSubSysId[50];
    TCHAR m_szRevisionId[50];
    DWORD m_dwWHQLLevel;
    TCHAR m_szDeviceIdentifier[100];
    TCHAR m_szDriverSignDate[50];

    BOOL m_bNoHardware;
    BOOL m_bDDAccelerationEnabled;
    BOOL m_b3DAccelerationExists;
    BOOL m_b3DAccelerationEnabled;
    BOOL m_bAGPEnabled;
    BOOL m_bAGPExists;
    BOOL m_bAGPExistenceValid;

    // TCHAR m_szDXVAModes[100];
    // vector<DxDiag_DXVA_DeinterlaceCaps*> m_vDXVACaps;

    TCHAR m_szDDStatusLocalized[100];
    TCHAR m_szDDStatusEnglish[100];
    TCHAR m_szD3DStatusLocalized[100];
    TCHAR m_szD3DStatusEnglish[100];
    TCHAR m_szAGPStatusLocalized[100];
    TCHAR m_szAGPStatusEnglish[100];

    TCHAR m_szNotesLocalized[3000];
    TCHAR m_szNotesEnglish[3000];
    TCHAR m_szRegHelpText[3000];

    TCHAR m_szTestResultDDLocalized[3000];
    TCHAR m_szTestResultDDEnglish[3000];
    TCHAR m_szTestResultD3D7Localized[3000];
    TCHAR m_szTestResultD3D7English[3000];
    TCHAR m_szTestResultD3D8Localized[3000];
    TCHAR m_szTestResultD3D8English[3000];
    TCHAR m_szTestResultD3D9Localized[3000];
    TCHAR m_szTestResultD3D9English[3000];

    DWORD m_nElementCount;
};

//bool m_bCleanupCOM = false;
IDxDiagProvider*  m_pDxDiagProvider = NULL;
IDxDiagContainer* m_pDxDiagRoot = NULL;

//-----------------------------------------------------------------------------
// Name: Init()
// Desc: Connect to dxdiagn.dll and init it
//-----------------------------------------------------------------------------
HRESULT DxDiag_Init(void) {
    HRESULT       hr;

    /*
    // since we're in IE, COM should already be initialized
    hr = CoInitialize( NULL );
    m_bCleanupCOM = SUCCEEDED(hr);
    */

    hr = CoCreateInstance( CLSID_DxDiagProvider,
                           NULL,
                           CLSCTX_INPROC_SERVER,
                           IID_IDxDiagProvider,
                           (LPVOID*) &m_pDxDiagProvider);
    if( FAILED(hr) ) {
        errorLog << "DxDiag CoCreate failed, hr=0x" << (void*) hr << endl;
        goto LCleanup;
    }
    if( m_pDxDiagProvider == NULL )
    {
        errorLog << "DxDiag CoCreate returned NULL!\n";
        hr = E_POINTER;
        goto LCleanup;
    }

    // Fill out a DXDIAG_INIT_PARAMS struct and pass it to IDxDiagContainer::Initialize
    // Passing in TRUE for bAllowWHQLChecks, allows dxdiag to check if drivers are
    // digital signed as logo'd by WHQL which may connect via internet to update
    // WHQL certificates.
    DXDIAG_INIT_PARAMS dxDiagInitParam;
    ZeroMemory( &dxDiagInitParam, sizeof(DXDIAG_INIT_PARAMS) );

    dxDiagInitParam.dwSize                  = sizeof(DXDIAG_INIT_PARAMS);
    dxDiagInitParam.dwDxDiagHeaderVersion   = DXDIAG_DX9_SDK_VERSION;
    dxDiagInitParam.bAllowWHQLChecks        = /*bAllowWHQLChecks*/ false;
    dxDiagInitParam.pReserved               = NULL;

    hr = m_pDxDiagProvider->Initialize( &dxDiagInitParam );
    if( FAILED(hr) ) {
        errorLog << "DxDiagProvider Init failed, hr=0x" << (void*) hr << endl;
        goto LCleanup;
    }

    hr = m_pDxDiagProvider->GetRootContainer( &m_pDxDiagRoot );
    if( FAILED(hr) ) {
        errorLog << "DxDiagProvider GetRoot failed, hr=0x" << (void*) hr << endl;
        goto LCleanup;
    }

LCleanup:
    return hr;
}

//-----------------------------------------------------------------------------
// Name: GetStringValue()
// Desc: Get a string value from a IDxDiagContainer object
//-----------------------------------------------------------------------------
HRESULT GetStringValue( IDxDiagContainer* pObject, WCHAR* wstrName, TCHAR* strValue, int nStrLen )
{
    HRESULT hr;
    VARIANT var;
    VariantInit( &var );

    if( FAILED( hr = pObject->GetProp( wstrName, &var ) ) )
        return hr;

    if( var.vt != VT_BSTR )
        return E_INVALIDARG;

#ifdef _UNICODE
    wcsncpy( strValue, var.bstrVal, nStrLen-1 );
#else
    wcstombs( strValue, var.bstrVal, nStrLen );
#endif
    strValue[nStrLen-1] = TEXT('\0');
    VariantClear( &var );

    return S_OK;
}

//-----------------------------------------------------------------------------
// Name: GetUIntValue()
// Desc: Get a UINT value from a IDxDiagContainer object
//-----------------------------------------------------------------------------
HRESULT GetUIntValue( IDxDiagContainer* pObject, WCHAR* wstrName, DWORD* pdwValue )
{
    HRESULT hr;
    VARIANT var;
    VariantInit( &var );

    if( FAILED( hr = pObject->GetProp( wstrName, &var ) ) )
        return hr;

    if( var.vt != VT_UI4 )
        return E_INVALIDARG;

    *pdwValue = var.ulVal;
    VariantClear( &var );

    return S_OK;
}




//-----------------------------------------------------------------------------
// Name: GetIntValue()
// Desc: Get a INT value from a IDxDiagContainer object
//-----------------------------------------------------------------------------
HRESULT GetIntValue( IDxDiagContainer* pObject, WCHAR* wstrName, LONG* pnValue )
{
    HRESULT hr;
    VARIANT var;
    VariantInit( &var );

    if( FAILED( hr = pObject->GetProp( wstrName, &var ) ) )
        return hr;

    if( var.vt != VT_I4 )
        return E_INVALIDARG;

    *pnValue = var.lVal;
    VariantClear( &var );

    return S_OK;
}




//-----------------------------------------------------------------------------
// Name: GetBoolValue()
// Desc: Get a BOOL value from a IDxDiagContainer object
//-----------------------------------------------------------------------------
HRESULT GetBoolValue( IDxDiagContainer* pObject, WCHAR* wstrName, BOOL* pbValue )
{
    HRESULT hr;
    VARIANT var;
    VariantInit( &var );

    if( FAILED( hr = pObject->GetProp( wstrName, &var ) ) )
        return hr;

    if( var.vt != VT_BOOL )
        return E_INVALIDARG;

    *pbValue = ( var.boolVal != 0 );
    VariantClear( &var );

    return S_OK;
}




//-----------------------------------------------------------------------------
// Name: GetInt64Value()
// Desc: Get a ULONGLONG value from a IDxDiagContainer object
//-----------------------------------------------------------------------------
HRESULT GetInt64Value( IDxDiagContainer* pObject, WCHAR* wstrName, ULONGLONG* pullValue )
{
    HRESULT hr;
    VARIANT var;
    VariantInit( &var );

    if( FAILED( hr = pObject->GetProp( wstrName, &var ) ) )
        return hr;

    // 64-bit values are stored as strings in BSTRs
    if( var.vt != VT_BSTR )
        return E_INVALIDARG;

    *pullValue = _wtoi64( var.bstrVal );
    VariantClear( &var );

    return S_OK;
}


// Name: DestroyDxDiagDisplayInfo()
// Desc: Cleanup the display info
//-----------------------------------------------------------------------------
void
DestroyDxDiagDisplayInfo( vector<DxDiagDisplayInfo*>& vDxDiagDisplayInfo ) {
    DxDiagDisplayInfo* pDxDiagDisplayInfo;
    vector<DxDiagDisplayInfo*>::iterator iter;
    for( iter = vDxDiagDisplayInfo.begin(); iter != vDxDiagDisplayInfo.end(); iter++ )
    {
        pDxDiagDisplayInfo = *iter;

      /*  DxDiag_DXVA_DeinterlaceCaps* pDXVANode;
        vector<DxDiag_DXVA_DeinterlaceCaps*>::iterator iterDXVA;
        for( iterDXVA = pDxDiagDisplayInfo->m_vDXVACaps.begin(); iterDXVA != pDxDiagDisplayInfo->m_vDXVACaps.end(); iterDXVA++ )
        {
            pDXVANode = *iterDXVA;
            SAFE_DELETE( pDXVANode );
        }
        pDxDiagDisplayInfo->m_vDXVACaps.clear();
      */

        SAFE_DELETE( pDxDiagDisplayInfo );
    }
    vDxDiagDisplayInfo.clear();

    /*
    if( m_bCleanupCOM )
        CoUninitialize();
     */
}

//-----------------------------------------------------------------------------
// Name: GetDxDiagDisplayInfo()
// Desc: Get the display info from the dll
//-----------------------------------------------------------------------------
HRESULT GetDxDiagDisplayInfo( vector<DxDiagDisplayInfo*>& vDxDiagDisplayInfo )
{
    HRESULT           hr;
    WCHAR             wszContainer[256];
    IDxDiagContainer* pContainer      = NULL;
    IDxDiagContainer* pObject         = NULL;
    DWORD             nInstanceCount    = 0;
    DWORD             nItem             = 0;
    DWORD             nCurCount         = 0;

    // Get the IDxDiagContainer object called "DxDiag_DisplayDevices".
    // This call may take some time while dxdiag gathers the info.

    // this takes a buttload of time loading and calling psapi, d3d9, and d3d9 dlls
    if( FAILED( hr = m_pDxDiagRoot->GetChildContainer( L"DxDiag_DisplayDevices", &pContainer ) ) ) {
        errorLog << "DxDiagRoot GetChild failed, hr=0x" << (void*) hr << endl;
        goto LCleanup;
    }
    if( FAILED( hr = pContainer->GetNumberOfChildContainers( &nInstanceCount ) ) ) {
        errorLog << "Container GetNumChilds failed, hr=0x" << (void*) hr << endl;
        goto LCleanup;
    }

    for( nItem = 0; nItem < nInstanceCount; nItem++ )
    {
        nCurCount = 0;

        DxDiagDisplayInfo* pDxDiagDisplayInfo = new DxDiagDisplayInfo;
        if (pDxDiagDisplayInfo == NULL)
            return E_OUTOFMEMORY;
        ZeroMemory(pDxDiagDisplayInfo, sizeof(DxDiagDisplayInfo));

        // Add pDxDiagDisplayInfo to vDxDiagDisplayInfo
        vDxDiagDisplayInfo.push_back( pDxDiagDisplayInfo );

        hr = pContainer->EnumChildContainerNames( nItem, wszContainer, 256 );
        if( FAILED( hr ) )
            goto LCleanup;
        hr = pContainer->GetChildContainer( wszContainer, &pObject );
        if( FAILED( hr ) || pObject == NULL )
        {
            if( pObject == NULL )
                hr = E_FAIL;
            goto LCleanup;
        }

        if( FAILED( hr = GetStringValue( pObject, L"szDeviceName", EXPAND(pDxDiagDisplayInfo->m_szDeviceName) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDescription", EXPAND(pDxDiagDisplayInfo->m_szDescription) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szKeyDeviceID", EXPAND(pDxDiagDisplayInfo->m_szKeyDeviceID) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szKeyDeviceKey", EXPAND(pDxDiagDisplayInfo->m_szKeyDeviceKey) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szManufacturer", EXPAND(pDxDiagDisplayInfo->m_szManufacturer) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szChipType", EXPAND(pDxDiagDisplayInfo->m_szChipType) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDACType", EXPAND(pDxDiagDisplayInfo->m_szDACType) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szRevision", EXPAND(pDxDiagDisplayInfo->m_szRevision) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDisplayMemoryLocalized", EXPAND(pDxDiagDisplayInfo->m_szDisplayMemoryLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDisplayMemoryEnglish", EXPAND(pDxDiagDisplayInfo->m_szDisplayMemoryEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDisplayModeLocalized", EXPAND(pDxDiagDisplayInfo->m_szDisplayModeLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDisplayModeEnglish", EXPAND(pDxDiagDisplayInfo->m_szDisplayModeEnglish) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetUIntValue( pObject, L"dwWidth", &pDxDiagDisplayInfo->m_dwWidth ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetUIntValue( pObject, L"dwHeight", &pDxDiagDisplayInfo->m_dwHeight ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetUIntValue( pObject, L"dwBpp", &pDxDiagDisplayInfo->m_dwBpp ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetUIntValue( pObject, L"dwRefreshRate", &pDxDiagDisplayInfo->m_dwRefreshRate ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szMonitorName", EXPAND(pDxDiagDisplayInfo->m_szMonitorName) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szMonitorMaxRes", EXPAND(pDxDiagDisplayInfo->m_szMonitorMaxRes) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szDriverName", EXPAND(pDxDiagDisplayInfo->m_szDriverName) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverVersion", EXPAND(pDxDiagDisplayInfo->m_szDriverVersion) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverAttributes", EXPAND(pDxDiagDisplayInfo->m_szDriverAttributes) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverLanguageEnglish", EXPAND(pDxDiagDisplayInfo->m_szDriverLanguageEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverLanguageLocalized", EXPAND(pDxDiagDisplayInfo->m_szDriverLanguageLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverDateEnglish", EXPAND(pDxDiagDisplayInfo->m_szDriverDateEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverDateLocalized", EXPAND(pDxDiagDisplayInfo->m_szDriverDateLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetIntValue( pObject, L"lDriverSize", &pDxDiagDisplayInfo->m_lDriverSize ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szMiniVdd", EXPAND(pDxDiagDisplayInfo->m_szMiniVdd) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szMiniVddDateLocalized", EXPAND(pDxDiagDisplayInfo->m_szMiniVddDateLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szMiniVddDateEnglish", EXPAND(pDxDiagDisplayInfo->m_szMiniVddDateEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetIntValue( pObject, L"lMiniVddSize", &pDxDiagDisplayInfo->m_lMiniVddSize ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szVdd", EXPAND(pDxDiagDisplayInfo->m_szVdd) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetBoolValue( pObject, L"bCanRenderWindow", &pDxDiagDisplayInfo->m_bCanRenderWindow ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bDriverBeta", &pDxDiagDisplayInfo->m_bDriverBeta ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bDriverDebug", &pDxDiagDisplayInfo->m_bDriverDebug ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bDriverSigned", &pDxDiagDisplayInfo->m_bDriverSigned ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bDriverSignedValid", &pDxDiagDisplayInfo->m_bDriverSignedValid ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDeviceIdentifier", EXPAND(pDxDiagDisplayInfo->m_szDeviceIdentifier) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDriverSignDate", EXPAND(pDxDiagDisplayInfo->m_szDriverSignDate) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetUIntValue( pObject, L"dwDDIVersion", &pDxDiagDisplayInfo->m_dwDDIVersion ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDDIVersionEnglish", EXPAND(pDxDiagDisplayInfo->m_szDDIVersionEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDDIVersionLocalized", EXPAND(pDxDiagDisplayInfo->m_szDDIVersionLocalized) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetUIntValue( pObject, L"iAdapter", &pDxDiagDisplayInfo->m_iAdapter ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szVendorId", EXPAND(pDxDiagDisplayInfo->m_szVendorId) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDeviceId", EXPAND(pDxDiagDisplayInfo->m_szDeviceId) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szSubSysId", EXPAND(pDxDiagDisplayInfo->m_szSubSysId) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szRevisionId", EXPAND(pDxDiagDisplayInfo->m_szRevisionId) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetUIntValue( pObject, L"dwWHQLLevel", &pDxDiagDisplayInfo->m_dwWHQLLevel ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetBoolValue( pObject, L"bNoHardware", &pDxDiagDisplayInfo->m_bNoHardware ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bDDAccelerationEnabled", &pDxDiagDisplayInfo->m_bDDAccelerationEnabled ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"b3DAccelerationExists", &pDxDiagDisplayInfo->m_b3DAccelerationExists ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"b3DAccelerationEnabled", &pDxDiagDisplayInfo->m_b3DAccelerationEnabled ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bAGPEnabled", &pDxDiagDisplayInfo->m_bAGPEnabled ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bAGPExists", &pDxDiagDisplayInfo->m_bAGPExists ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetBoolValue( pObject, L"bAGPExistenceValid", &pDxDiagDisplayInfo->m_bAGPExistenceValid ) ) )
            goto LCleanup; nCurCount++;

        //if( FAILED( hr = GetStringValue( pObject, L"szDXVAModes", EXPAND(pDxDiagDisplayInfo->m_szDXVAModes) ) ) )
        //    goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szDDStatusLocalized", EXPAND(pDxDiagDisplayInfo->m_szDDStatusLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szDDStatusEnglish", EXPAND(pDxDiagDisplayInfo->m_szDDStatusEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szD3DStatusLocalized", EXPAND(pDxDiagDisplayInfo->m_szD3DStatusLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szD3DStatusEnglish", EXPAND(pDxDiagDisplayInfo->m_szD3DStatusEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szAGPStatusLocalized", EXPAND(pDxDiagDisplayInfo->m_szAGPStatusLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szAGPStatusEnglish", EXPAND(pDxDiagDisplayInfo->m_szAGPStatusEnglish) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szNotesLocalized", EXPAND(pDxDiagDisplayInfo->m_szNotesLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szNotesEnglish", EXPAND(pDxDiagDisplayInfo->m_szNotesEnglish) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szRegHelpText", EXPAND(pDxDiagDisplayInfo->m_szRegHelpText) ) ) )
            goto LCleanup; nCurCount++;

        if( FAILED( hr = GetStringValue( pObject, L"szTestResultDDLocalized", EXPAND(pDxDiagDisplayInfo->m_szTestResultDDLocalized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultDDEnglish", EXPAND(pDxDiagDisplayInfo->m_szTestResultDDEnglish) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D7Localized", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D7Localized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D7English", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D7English) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D8Localized", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D8Localized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D8English", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D8English) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D9Localized", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D9Localized) ) ) )
            goto LCleanup; nCurCount++;
        if( FAILED( hr = GetStringValue( pObject, L"szTestResultD3D9English", EXPAND(pDxDiagDisplayInfo->m_szTestResultD3D9English) ) ) )
            goto LCleanup; nCurCount++;

//#ifdef _DEBUG
#if 0
        // debug check to make sure we got all the info from the object
        if( FAILED( hr = pObject->GetNumberOfProps( &pDxDiagDisplayInfo->m_nElementCount ) ) )
            return hr;
        if( pDxDiagDisplayInfo->m_nElementCount != nCurCount )
            OutputDebugString( TEXT("Not all elements in pDxDiagDisplayInfo recorded") );
#endif

//        GatherDXVA_DeinterlaceCaps( pObject, pDxDiagDisplayInfo->m_vDXVACaps );

        SAFE_RELEASE( pObject );
    }

LCleanup:
    SAFE_RELEASE( pObject );
    SAFE_RELEASE( pContainer );
    return hr;
}

void SysInfo::Test_DX9(bool bWhatever) {
  if(_DX9_status != Status_Unknown) {
    errorLog << "DX9 status already found to be " << ((_DX9_status==Status_Unsupported) ? "un":"") << "supported\n";
    return;
  }
  
  _DX9_status = Status_Unsupported;

  HRESULT hr = DxDiag_Init();
  if( FAILED(hr) ) {
    errorLog << "Dx9 dxdiag failed, try other api " << endl;
    return;
  }
  vector<DxDiagDisplayInfo*> vDxDiagDisplayInfo;
  GetDxDiagDisplayInfo(vDxDiagDisplayInfo);
  DxDiagDisplayInfo *pD = vDxDiagDisplayInfo[0];

  // copy dx9 devinfo to dx7 struct
  SYSTEMTIME DriverDate_SysTime;
  int y, m, d;
  sscanf(pD->m_szDriverDateEnglish, "%d/%d/%d", &m, &d, &y);
  //errorLog << "year=" << y <<" month=" << m << " day=" << d << endl;
  DriverDate_SysTime.wYear = y;
  DriverDate_SysTime.wMonth = m;
  DriverDate_SysTime.wDay = d;

  LARGE_INTEGER li;
  DWORD hh, hl, lh, ll;
  sscanf(pD->m_szDriverVersion, "%d.%d.%d.%d", &hh, &hl, &lh, &ll);
  //errorLog << "hh=" << hh << " hl=" << hl << " lh=" << lh << " ll=" << ll << endl;
  li.HighPart = MAKELONG(hl,hh);
  li.LowPart = MAKELONG(ll,lh);
    
  DDDEVICEIDENTIFIER2 DX7_DevID;
  DX7_DevID.dwVendorId=strtol(pD->m_szVendorId, NULL, 0);
  DX7_DevID.dwDeviceId=strtol(pD->m_szDeviceId, NULL, 0);
  DX7_DevID.dwSubSysId=strtol(pD->m_szSubSysId, NULL, 0);
  DX7_DevID.dwRevision=strtol(pD->m_szRevisionId, NULL, 0);
  strncpy(DX7_DevID.szDescription,pD->m_szDescription,MAX_DEVICE_IDENTIFIER_STRING);
  strncpy(DX7_DevID.szDriver,pD->m_szDriverName,MAX_DEVICE_IDENTIFIER_STRING);
  memcpy(&DX7_DevID.liDriverVersion,&li,sizeof(LARGE_INTEGER));
  //memcpy(&DX7_DevID.guidDeviceIdentifier,&adapter_info.DeviceIdentifier,sizeof(GUID));
  
  SetVideoCardConfigInfo(0,&DX7_DevID,&DriverDate_SysTime);

  _DX9_status = Status_Supported;
}

HRESULT PrintDxDiagDisplayInfo(void) {
  HRESULT hr = DxDiag_Init();
  vector<DxDiagDisplayInfo*> vDxDiagDisplayInfo;
  GetDxDiagDisplayInfo(vDxDiagDisplayInfo);
  DxDiagDisplayInfo *pD = vDxDiagDisplayInfo[0];

  errorLog << "DxDiag::" << endl;
  errorLog << "  DeviceName=" << pD->m_szDeviceName << endl;
  errorLog << "  DeviceDescription=" << pD->m_szDescription << endl;
  errorLog << "  KeyDeviceId=" <<  pD->m_szKeyDeviceID << endl;
  errorLog << "  KeyDeviceKey=" <<  pD->m_szKeyDeviceKey << endl;
  errorLog << "  Manufacturer=" <<  pD->m_szManufacturer << endl;;
  errorLog << "  ChipType=" <<  pD->m_szChipType << endl;
  errorLog << "  DACType=" <<  pD->m_szDACType << endl;
  errorLog << "  Revision=" <<  pD->m_szRevision << endl;
  errorLog << "  DisplayMemoryLocalized=" <<  pD->m_szDisplayMemoryLocalized << endl;
  errorLog << "  DisplayMemoryEnglish=" <<  pD->m_szDisplayMemoryEnglish << endl;
  errorLog << "  DisplayModeLocalized=" <<  pD->m_szDisplayModeLocalized << endl;
  errorLog << "  DisplayModeEnglish=" <<  pD->m_szDisplayModeEnglish << endl;

  errorLog << "  Width=" <<  pD->m_dwWidth << endl;
  errorLog << "  Height=" <<  pD->m_dwHeight << endl;
  errorLog << "  Bpp=" <<  pD->m_dwBpp << endl;
  errorLog << "  RefreshRate=" <<  pD->m_dwRefreshRate << endl;

  errorLog << "  MonitorName=" <<  pD->m_szMonitorName << endl;
  errorLog << "  MonitorMaxRes=" <<  pD->m_szMonitorMaxRes << endl;
  
  errorLog << "  DriverName=" <<  pD->m_szDriverName << endl;
  errorLog << "  DriverVersion=" <<  pD->m_szDriverVersion << endl;
  errorLog << "  DriverAttributes=" <<  pD->m_szDriverAttributes << endl;
  errorLog << "  DriverLanguageEnglish=" <<  pD->m_szDriverLanguageEnglish << endl;
  errorLog << "  DriverLanguageLocalized=" <<  pD->m_szDriverLanguageLocalized << endl;
  errorLog << "  DriverDateEnglish=" <<  pD->m_szDriverDateEnglish << endl;
  errorLog << "  DriverDateLocalized=" <<  pD->m_szDriverDateLocalized << endl;
  errorLog << "  DriverSize=" <<  pD->m_lDriverSize << endl;
  errorLog << "  MiniVdd=" <<  pD->m_szMiniVdd << endl;
  errorLog << "  MiniVddDateLocalized=" <<  pD->m_szMiniVddDateLocalized << endl;
  errorLog << "  MiniVddDateEnglish=" <<  pD->m_szMiniVddDateEnglish << endl;
  errorLog << "  MiniVddSize=" <<   pD->m_lMiniVddSize << endl;
  errorLog << "  Vdd=" <<  pD->m_szVdd << endl;
  
  errorLog << "  CanRenderWindow=" <<  pD->m_bCanRenderWindow << endl;
  errorLog << "  DriverBeta=" <<  pD->m_bDriverBeta << endl;
  errorLog << "  DriverDebug=" <<  pD->m_bDriverDebug << endl;
  errorLog << "  DriverSigned=" <<  pD->m_bDriverSigned << endl;
  errorLog << "  DriverSignedValid=" <<  pD->m_bDriverSignedValid << endl;
  errorLog << "  DDIVersion=" <<  pD->m_dwDDIVersion << endl;
  errorLog << "  DDIVersionEnglish=" <<  pD->m_szDDIVersionEnglish << endl;
  errorLog << "  DDIVersionLocalized=" <<  pD->m_szDDIVersionLocalized << endl;
  
  errorLog << "  Adapter=" <<  pD->m_iAdapter << endl;
  errorLog << "  VendorId=" <<  pD->m_szVendorId << endl;
  //errorLog << "xxVendorId=" << strtol(pD->m_szVendorId,NULL,0);
  errorLog << "  DeviceId=" <<  pD->m_szDeviceId << endl;
  errorLog << "  SubSysId=" <<  pD->m_szSubSysId << endl;
  errorLog << "  RevisionId=" <<  pD->m_szRevisionId << endl;
  errorLog << "  WHQLLevel=" <<  pD->m_dwWHQLLevel << endl;
  errorLog << "  DeviceIdentifier=" <<  pD->m_szDeviceIdentifier << endl;
  errorLog << "  DriverSignDate=" <<  pD->m_szDriverSignDate << endl;
  
  errorLog << "  NoHardware=" <<  pD->m_bNoHardware << endl;
  errorLog << "  DDAccelerationEnabled=" <<  pD->m_bDDAccelerationEnabled << endl;
  errorLog << "  3DAccelerationExists=" <<  pD->m_b3DAccelerationExists << endl;
  errorLog << "  3DAccelerationEnabled=" <<  pD->m_b3DAccelerationEnabled << endl;
  errorLog << "  AGPEnabled=" <<  pD->m_bAGPEnabled << endl;
  errorLog << "  AGPExists=" <<  pD->m_bAGPExists << endl;
  errorLog << "  AGPExistenceValid=" <<  pD->m_bAGPExistenceValid << endl;
  
  // errorLog << "  =" <<  m_szDXVAModes[100];
  // vector<  _DXVA_DeinterlaceCaps*> m_vDXVACaps;
  
  errorLog << "  DDStatusLocalized=" <<  pD->m_szDDStatusLocalized << endl;
  errorLog << "  DDStatusEnglish=" <<  pD->m_szDDStatusEnglish << endl;
  errorLog << "  D3DStatusLocalized=" <<  pD->m_szD3DStatusLocalized << endl;
  errorLog << "  D3DStatusEnglish=" <<  pD->m_szD3DStatusEnglish << endl;
  errorLog << "  AGPStatusLocalized=" <<  pD->m_szAGPStatusLocalized << endl;
  errorLog << "  AGPStatusEnglish=" <<  pD->m_szAGPStatusEnglish << endl;
  
  errorLog << "  NotesLocalized=" <<  pD->m_szNotesLocalized << endl;
  errorLog << "  NotesEnglish=" <<  pD->m_szNotesEnglish << endl;
  errorLog << "  RegHelpText=" <<  pD->m_szRegHelpText << endl;
  
  errorLog << "  TestResultDDLocalized=" <<  pD->m_szTestResultDDLocalized << endl;
  errorLog << "  TestResultDDEnglish=" <<  pD->m_szTestResultDDEnglish << endl;
  errorLog << "  TestResultD3D7Localized=" <<  pD->m_szTestResultD3D7Localized << endl;
  errorLog << "  TestResultD3D7English=" <<  pD->m_szTestResultD3D7English << endl;
  errorLog << "  TestResultD3D8Localized=" <<  pD->m_szTestResultD3D8Localized << endl;
  errorLog << "  TestResultD3D8English=" <<  pD->m_szTestResultD3D8English << endl;
  errorLog << "  TestResultD3D9Localized=" <<  pD->m_szTestResultD3D9Localized << endl;
  errorLog << "  TestResultD3D9English=" <<  pD->m_szTestResultD3D9English << endl;
  
  errorLog << "  ElementCount=" <<  pD->m_nElementCount << endl;

  return hr;
}

#endif
