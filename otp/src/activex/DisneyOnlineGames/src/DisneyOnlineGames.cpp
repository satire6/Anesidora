#include "stdafx.h"
#include "DisneyOnlineGames.h"
#include "comcat.h"
#include "strsafe.h"
#include "objsafe.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// CLSID_SafeItem - Necessary for safe ActiveX control
// Taken from IMPLEMENT_OLECREATE_EX function in DisneyOnlineGamesCtrl.cpp

const CATID CLSID_SafeItem =
{ 0x3dcec959, 0x378a, 0x4922,{ 0xad, 0x7e, 0xfd, 0x5c, 0x92, 0x5d, 0x92, 0x7f}};

HRESULT CreateComponentCategory(CATID catid, WCHAR *catDescription)
{
    ICatRegister *pcr = NULL ;
    HRESULT hr = S_OK ;
 
    hr = CoCreateInstance(CLSID_StdComponentCategoriesMgr, 
            NULL, CLSCTX_INPROC_SERVER, IID_ICatRegister, (void**)&pcr);
    if (FAILED(hr))
        return hr;
 
    // Make sure the HKCR\Component Categories\{..catid...}
    // key is registered.
    CATEGORYINFO catinfo;
    catinfo.catid = catid;
    catinfo.lcid = 0x0409 ; // english
    size_t len;
    // Make sure the provided description is not too long.
    // Only copy the first 127 characters if it is.
    // The second parameter of StringCchLength is the maximum
    // number of characters that may be read into catDescription.
    // There must be room for a NULL-terminator. The third parameter
    // contains the number of characters excluding the NULL-terminator.
    hr = StringCchLengthW(catDescription, STRSAFE_MAX_CCH, &len);
    if (SUCCEEDED(hr))
        {
        if (len>127)
          {
            len = 127;
          }
        }   
    else
        {
          // TODO: Write an error handler;
        }
    // The second parameter of StringCchCopy is 128 because you need 
    // room for a NULL-terminator.
    hr = StringCchCopyW(catinfo.szDescription, len + 1, catDescription);
    // Make sure the description is null terminated.
    catinfo.szDescription[len + 1] = '\0';
 
    hr = pcr->RegisterCategories(1, &catinfo);
    pcr->Release();
 
    return hr;
}
 
// HRESULT RegisterCLSIDInCategory -
//      Register your component categories information
 
HRESULT RegisterCLSIDInCategory(REFCLSID clsid, CATID catid)
{
// Register your component categories information.
    ICatRegister *pcr = NULL ;
    HRESULT hr = S_OK ;
    hr = CoCreateInstance(CLSID_StdComponentCategoriesMgr, 
                NULL, CLSCTX_INPROC_SERVER, IID_ICatRegister, (void**)&pcr);
    if (SUCCEEDED(hr))
    {
       // Register this category as being "implemented" by the class.
       CATID rgcatid[1] ;
       rgcatid[0] = catid;
       hr = pcr->RegisterClassImplCategories(clsid, 1, rgcatid);
    }
 
    if (pcr != NULL)
        pcr->Release();
            
    return hr;
}
 
// HRESULT UnRegisterCLSIDInCategory - Remove entries from the registry
 
HRESULT UnRegisterCLSIDInCategory(REFCLSID clsid, CATID catid)
{
    ICatRegister *pcr = NULL ;
    HRESULT hr = S_OK ;
 
    hr = CoCreateInstance(CLSID_StdComponentCategoriesMgr, 
            NULL, CLSCTX_INPROC_SERVER, IID_ICatRegister, (void**)&pcr);
    if (SUCCEEDED(hr))
    {
       // Unregister this category as being "implemented" by the class.
       CATID rgcatid[1] ;
       rgcatid[0] = catid;
       hr = pcr->UnRegisterClassImplCategories(clsid, 1, rgcatid);
    }
 
    if (pcr != NULL)
        pcr->Release();
 
    return hr;
}

CDisneyOnlineGamesApp theApp;

const GUID CDECL BASED_CODE _tlid =
        { 0x5F6C8F0A, 0x6FE5, 0x4546, { 0x82, 0xF1, 0x9B, 0x50, 0x37, 0x3A, 0x8E, 0xBD } };
const WORD _wVerMajor = 3;
const WORD _wVerMinor = 1;

BOOL CDisneyOnlineGamesApp::InitInstance()
// DLL initialization
{
    BOOL bInit = COleControlModule::InitInstance();
    if (bInit)
    {
        // TODO: Add your own module initialization code here.
    }
    return bInit;
}

int CDisneyOnlineGamesApp::ExitInstance()
// DLL termination
{
    // TODO: Add your own module termination code here.
    return COleControlModule::ExitInstance();
}

STDAPI DllRegisterServer(void)
// Adds entries to the system registry
{
    HRESULT hr;    // HResult used by Safety Functions
 
    AFX_MANAGE_STATE(_afxModuleAddrThis);

    if (!AfxOleRegisterTypeLib(AfxGetInstanceHandle(), _tlid))
        return ResultFromScode(SELFREG_E_TYPELIB);

    if (!COleObjectFactoryEx::UpdateRegistryAll(TRUE))
        return ResultFromScode(SELFREG_E_CLASS);
 
    // Mark the control as safe for initializing.
                                             
    hr = CreateComponentCategory(CATID_SafeForInitializing, 
         L"Controls safely initializable from persistent data!");
    if (FAILED(hr))
      return hr;
 
    hr = RegisterCLSIDInCategory(CLSID_SafeItem, 
         CATID_SafeForInitializing);
    if (FAILED(hr))
        return hr;
 
    // Mark the control as safe for scripting.
 
    hr = CreateComponentCategory(CATID_SafeForScripting, 
                                 L"Controls safely  scriptable!");
    if (FAILED(hr))
        return hr;
 
    hr = RegisterCLSIDInCategory(CLSID_SafeItem, 
                        CATID_SafeForScripting);
    if (FAILED(hr))
        return hr;

    return NOERROR;
}

STDAPI DllUnregisterServer(void)
// Removes entries from the system registry
{
    HRESULT hr;    // HResult used by Safety Functions
 
    AFX_MANAGE_STATE(_afxModuleAddrThis);

    if (!AfxOleUnregisterTypeLib(_tlid, _wVerMajor, _wVerMinor))
        return ResultFromScode(SELFREG_E_TYPELIB);

    if (!COleObjectFactoryEx::UpdateRegistryAll(FALSE))
        return ResultFromScode(SELFREG_E_CLASS);
 
    // Remove entries from the registry.
 
    hr=UnRegisterCLSIDInCategory(CLSID_SafeItem, 
                     CATID_SafeForInitializing);
    if (FAILED(hr))
      return hr;
 
    hr=UnRegisterCLSIDInCategory(CLSID_SafeItem, 
                        CATID_SafeForScripting);
    if (FAILED(hr))
      return hr;

    return NOERROR;
}
