// Filename: installerCtrl.h
// Created by:
// $Id$
//
////////////////////////////////////////////////////////////////////

#ifndef __INSTALLERCTRL_H_
#define __INSTALLERCTRL_H_

#include "resource.h"       // main symbols
#include <atlctl.h>

#include "exdisp.h"

//#define USE_IE_ASYNC_DOWNLOAD

#include "toontownInstaller.h"

#ifdef USE_IE_ASYNC_DOWNLOAD
#include "bindstatuscallback.h"
#endif

#if defined(_EXEINSTALLER_) || defined(USE_RPCINSTALLER)
#   include <vos/vos.hpp>
#   include <vos/thread.hpp>
#endif

/////////////////////////////////////////////////////////////////////////////
// CWDI_InstallerCtrl
class ATL_NO_VTABLE CWDI_InstallerCtrl :
  public CComObjectRootEx<CComSingleThreadModel>,
  public CComCoClass<CWDI_InstallerCtrl, &CLSID_WDI_InstallerCtrl>,
  public IObjectWithSiteImpl<CWDI_InstallerCtrl>,
  public IDispatchImpl<IWDI_InstallerCtrl, &IID_IWDI_InstallerCtrl, &LIBID_WDI_INSTALLERLib>,
  public IObjectSafetyImpl<CWDI_InstallerCtrl,
          INTERFACESAFE_FOR_UNTRUSTED_CALLER | INTERFACESAFE_FOR_UNTRUSTED_DATA>
{
public:
  CWDI_InstallerCtrl()
  {
#ifndef USE_RPCINSTALLER
    ttInstaller = new toontownInstaller();
#else
    _bootstrap_pid = _helper_pid = 0;
	_initialized = false;
#endif
  }

  ~CWDI_InstallerCtrl()
  {
#ifndef USE_RPCINSTALLER
    delete ttInstaller;
#endif
  }

DECLARE_REGISTRY_RESOURCEID(IDR_INSTALLERCTRL)

DECLARE_PROTECT_FINAL_CONSTRUCT()

#ifdef USE_RPCINSTALLER
    HRESULT FinalConstruct();
    void FinalRelease();
#endif

BEGIN_COM_MAP(CWDI_InstallerCtrl)
  COM_INTERFACE_ENTRY(IWDI_InstallerCtrl)
  COM_INTERFACE_ENTRY(IDispatch)
  COM_INTERFACE_ENTRY(IObjectWithSite)
END_COM_MAP()

BEGIN_CATEGORY_MAP(CWDI_InstallerCtrl)
  IMPLEMENTED_CATEGORY(CATID_SafeForScripting)
  IMPLEMENTED_CATEGORY(CATID_SafeForInitializing)
END_CATEGORY_MAP()

// IWDI_InstallerCtrl

// shouldnt at least part of this be auto-generated from the .idl?
public:
  STDMETHOD(getValue)(/*[in]*/ BSTR key, /*[out, retval]*/ BSTR *pVal);
  STDMETHOD(setValue)(/*[in]*/ BSTR key, /*[in]*/ BSTR value);
#if defined(USE_RPCINSTALLER)
  STDMETHOD(InitForRun)(/*[in]*/BSTR deployment, /*[in]*/BSTR downloadServer, /*[in]*/BSTR downloadVersion, /*[out,retval]*/ int *pInitSucceeded);
  STDMETHOD(InitForStatus)(/*[out,retval]*/ int *pInitSucceeded);
#else
  STDMETHOD(InitForRun)(/*[in]*/ BSTR activex_version_str,/*[out,retval]*/ int *pInitSucceeded);
#endif
  STDMETHOD(Init)();
  STDMETHOD(RunInstaller)();

#ifdef USE_IE_ASYNC_DOWNLOAD
  // hack functions to allow for async downloading
  void OnData(COurBindStatusCallback<CWDI_InstallerCtrl>* pbsc,
              DWORD grfBSCF, BYTE* pBytes, DWORD dwSize);

  void StartDownload(const char *URL);
  void OnDownloadBegin();
  void OnDownloadProgress();
  void OnDownloadComplete(DWORD availableToRead, BYTE* pBytes);

  int downloadToFile(const char* URL, const char* destFilename);
#endif

#if defined(USE_RPCINSTALLER)
	handle_t _wdiginstaller_IfHandle;	// EXE RPC interface handle

	int RPCstartup(bool setMediumIntegrity = false);
#endif

private:
#ifndef USE_RPCINSTALLER
	toontownInstaller *ttInstaller;
#else
    pid_t _bootstrap_pid, _helper_pid;
	bool _initialized;
	vos::sysinfo_t _sysinfo;
#endif
	HWND browser_hwnd();
};

#endif //__INSTALLERCTRL_H_
