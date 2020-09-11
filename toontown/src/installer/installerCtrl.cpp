// installerCtrl.cpp : Implementation of CWDI_InstallerCtrl
#include "stdafx.h"
#include "installer.h"
#include "installerCtrl.h"

#include <comdef.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef USE_IE_ASYNC_DOWNLOAD
#include "log.h"

void initDownloadCallback(CWDI_InstallerCtrl*, toontownInstaller*);
#endif

#if defined(_EXEINSTALLER_) || defined(USE_RPCINSTALLER)
#   include <vos/vos.hpp>
#   include <vos/proc.hpp>
#	include <vos/thread.hpp>

#   ifdef USE_RPCINSTALLER	// ONLY
#		include <Rpc.h>
#		include "standalone/win32/wdig-installer.h"

#		include <vos/sysinfo.hpp>
#		include <vos/iut/vrfile.h>
#		include <vos/iut/bootstrap_downloader.hpp>

		int installer_service_update();
		vos::registry_t myREG;

#		include "standalone/shToontownInstaller.hpp"
		ToontownInstaller ttapp;

        ofstream errorLog;
		bool errorLog_opened = false;

		typedef vrfile_adaptor_t<checksum_md5hex, compress_null, archive_null, alternate_null> md5hex_vrfile_t;

//#	define USE_RPC_SECURITY

#   endif // USE_RPCINSTALLER
#endif  // _EXEINSTALLER_

#if defined(USE_RPCINSTALLER)

#define _str(s) #s
#define _xstr(s) _str(s)

#if defined(USE_JAPANESE) || defined(USE_PORTUGUESE) || defined(USE_FRENCH)
  #undef DEPLOYMENT
  #define DEPLOYMENT _xstr(PRODUCT_NAME)
#endif

static int sehISRPC_ready(handle_t IDL_handle)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        return ISRPC_ready(IDL_handle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_DoMediumIntegrity(handle_t IDL_handle)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        return ISRPC_DoMediumIntegrity(IDL_handle, 0);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_Init(handle_t IDL_handle)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "calling RPC_Init()" << endl;
        ISRPC_Init(IDL_handle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(RPC_Init) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_InitForStatus(handle_t IDL_handle, HWND bhwnd)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "calling RPC_InitForRun()" << endl;
        return ISRPC_InitForStatus(IDL_handle, (__int64) bhwnd);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(RPC_InitForStatus) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_InitForRun(handle_t IDL_handle, HWND bhwnd, BSTR deployment, BSTR downloadServer, BSTR downloadVersion)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "calling RPC_InitForRun()" << endl;
        return ISRPC_InitForRun(IDL_handle, (__int64) bhwnd, deployment, downloadServer, downloadVersion);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(RPC_InitForRun) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_RunInstaller(handle_t IDL_handle)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "calling RPC_RunInstaller()" << endl;
        ISRPC_RunInstaller(IDL_handle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(RunInstaller) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_getValue(handle_t IDL_handle, BSTR key, BSTR *pVal)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "calling RPC_getValue()" << endl;
        ISRPC_getValue(IDL_handle, key, pVal);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(getValue) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

static int sehISRPC_setValue(handle_t IDL_handle, BSTR key, BSTR val)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        //errorLog << "RPC_setValue("<<hex<<kn<<keyName<<", "<<hex<<v<<value<<')' << endl;
		//errorLog << "calling RPC_setValue("<<hex<<size_t(keyName)<<", "<<hex<<size_t(value)<<')' << endl;
        ISRPC_setValue(IDL_handle, key, val);
   }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(setValue) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
    return ulCode;
}

void sehISRPC_Shutdown(handle_t IDL_handle)
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
		errorLog << "RPC_Shutdown()" << endl;
        ISRPC_Shutdown(IDL_handle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
        errorLog << "(Shutdown) Runtime reported exception 0x" << hex << ulCode << endl;
    }
    RpcEndExcept
}

#endif

/////////////////////////////////////////////////////////////////////////////
// CWDI_InstallerCtrl

STDMETHODIMP CWDI_InstallerCtrl::Init()
{
/*
 * Meat uplift
 *
 * Vista's steps:
 * 1) Make sure NSIS Installer file exists
 * 2) Make sure InstallerHelper/Svc file exists otherwise use NSIS Installer to reinstall it
 * 3) bring InstallHelper online and establish RPC interface between it and browser-plugin (ActiveX)
 * 4) once RPC interface is verified to be up, call DoMediumIntegrity() to do Vista-only security fixups
 *
 */

#ifndef USE_RPCINSTALLER
  ttInstaller->init();

#   ifdef USE_IE_ASYNC_DOWNLOAD
  // set up for the download callback
  initDownloadCallback(this, ttInstaller);
#   endif
#else

	//errorLog << "Init()" << endl;
#if 0
	std::stringstream debug;
	debug << _wdiginstaller_IfHandle << ' ' << ie_window << endl;
	::MessageBox(NULL, debug.str().c_str(), NULL, 0);
#endif
//    sehISRPC_Init(_wdiginstaller_IfHandle);
#endif

  return S_OK;
}

#ifdef USE_RPCINSTALLER
STDMETHODIMP CWDI_InstallerCtrl::InitForStatus(/*[out,retval]*/int *pInitSucceeded)
{
	*pInitSucceeded = 0;		// assumes pInitSucceeded is always non-null because IDL will prevent it
	errorLog << vos::datestamp() << "InitForStatus()" << endl;
	return InitForRun(NULL, NULL, NULL, pInitSucceeded);
}

#endif

// do initialization that prepares for an actual TT run
// (setup log, etc)
#ifndef USE_RPCINSTALLER
STDMETHODIMP CWDI_InstallerCtrl::InitForRun(/*[in]*/BSTR activeXversion_str, /*[out,retval]*/int *pInitSucceeded)
#else
STDMETHODIMP CWDI_InstallerCtrl::InitForRun(/*[in]*/BSTR bsDeployment, BSTR bsDownloadServer, BSTR bsDownloadVersion, /*[out,retval]*/int *pInitSucceeded)
#endif
{
	*pInitSucceeded = 0;		// assumes pInitSucceeded is always non-null because IDL will prevent it

	// _bstr_t class has auto-conversion to const char *, whereas BSTR doesnt
#ifndef USE_RPCINSTALLER
	if ( ttInstaller->normalInit(browser_hwnd()))
#else
	enum bsState
	{
		bsDownload_bootstrap,
		bsChecksum_components,
		bsRun_bootstrap,
		bsRun_helper,
		bsSetup_RPC,
		bsFatalError,
		bsDone,
	};
	bsState state = bsDownload_bootstrap;
	_bstr_t deployment(bsDeployment), downloadServer(bsDownloadServer), downloadVersion(bsDownloadVersion);
	bool bStatusOnly = (deployment.length() == 0) && (downloadServer.length() == 0) && (downloadVersion.length() == 0);

	errorLog << vos::datestamp() << "InitForRun()" << endl;
	if (!bStatusOnly)
	{	// update mode
		state = bsDownload_bootstrap;

		//ttapp.Deployment(deployment);
		ttapp.DownloadServer(downloadServer, true);
		ttapp.DownloadVersion(downloadVersion);
		errorLog << "DOWNLOAD URL is: "<<ttapp.urlsrc() << endl;
		myREG.str(vos::vregBOOT_URLSRC) = ttapp.urlsrc();
	}
	else
	{	// status mode
		state = bsRun_helper;

		ttapp.DownloadServer("", true);
		ttapp.DownloadVersion("");
		myREG.str(vos::vregBOOT_URLSRC) = "";
	}

	myREG.str(vos::vregINSTALL_PATH) = ttapp.install_dir();
	errorLog << "INSTALL DIR is: "<<ttapp.install_dir() << endl;

	static const vstr_t setup_file = "ttinst-setup" DEPLOYMENT ".exe";
    static const vstr_t helper_file = "ttinst-helper.exe";
	static const vstr_t svc_file = "wdigInstallerSvc.exe";

	vstr_t Setup_path, Helper_path;
	bool errorState = true;
	size_t setup_rpc_count = 0, tries = 2;

	Helper_path = ttapp.install_dir() + helper_file;
	Setup_path = vos::tempdir() + setup_file;

	myREG.str(vos::vregINSTALL_PATH) = vos::tempdir();
	myREG.str(vos::vregBOOT1_DLFILE) = setup_file;

	for(bool done = false; !done;)
	{
		switch(state)
		{
		case bsDownload_bootstrap:
			{	// download file with checksum checks
				md5hex_vrfile_t bootstrap;
				int ec = download_file(bootstrap, ttapp.urlsrc(), vos::tempdir(), setup_file, _T("bootstrap.db"));
				switch(ec)
				{
				case 0:			// no changes brute force execute helper
					state = bsChecksum_components;
					errorLog << vos::datestamp() << "Bootstrap up-to-date." << endl;
					break;
				case 1:			// download/update occurred, so rerun installer
					state = bsRun_bootstrap;
					errorLog << vos::datestamp() << "Bootstrap update detected." << endl;
					break;
				default:
					state = bsFatalError;
					errorLog << vos::datestamp() << "Error downloading "<<setup_file<<endl;
				}
			}
			break;
		case bsChecksum_components:
			{
				md5hex_vrfile_t helper, svc;
				helper.src(ttapp.urlsrc() + helper_file, ttapp.install_dir(), _T("bootstrap.db"));
				svc.src(ttapp.urlsrc() + svc_file, ttapp.install_dir(), _T("bootstrap.db"));
				if (helper.checksum_quick() || svc.checksum_quick())
				{
					state = bsRun_bootstrap;
					errorLog << vos::datestamp() << "Detected Helper/Svc out-of-date." << endl;
				}
				else
					state = bsRun_helper;
			}
			break;
		case bsRun_bootstrap:
			if ( vos::rfork_execve(Setup_path.c_str(), NULL, NULL, _bootstrap_pid) || _bootstrap_pid == 0)
			{
				state = bsFatalError;
				errorLog << vos::datestamp() << "Setup download failed." << endl;
			}
			else
				state = bsSetup_RPC;
			break;			// Setup runs Helper so no need to double up
		case bsRun_helper:
			if ( (errno = vos::rfork_execve(Helper_path.c_str(), NULL, NULL, _helper_pid)) || _helper_pid == 0)
			{
				state = bsFatalError;
				errorLog << "Couldn't startup Install Helper ("<<Helper_path<<") "<<errno<<"!" << endl;
			}
			else
			{
				state = bsSetup_RPC;
				errorLog << "Install Helper OK" << endl;
			}
			break;
		case bsSetup_RPC:	// RPC connect to Install Helper broker
			if (setup_rpc_count < tries)
			{
 				switch(RPCstartup(setup_rpc_count++ == 0))			// set medium integrity only on first RPC startup
				{
				case 0:
					errorLog << "Installer Helper started successfully" << endl;
					state = bsDone;
					break;
				case 1:		// medium integrity set up, try again
					sehISRPC_Shutdown(_wdiginstaller_IfHandle);		// kill it here instead of letting it auto-die to avoid side-effects
					errorLog << vos::datestamp() << "restarting Install Helper" << endl;
					state = bsRun_helper;
					break;
				default:
					errorLog << "Connection to Installer Helper was not established" << endl;
					state = bsFatalError;
				}
			}
			else
			{				// more than try times connecting to RPC
				state = bsFatalError;
			}
			break;
		case bsDone:
			errorState = false;
		case bsFatalError:
			done = true;
			break;
		}	// end switch
	}	// end for

	if (errorState)
	{
		pInitSucceeded = 0;
		return S_OK;			// Installer Helper isn't available
	}

	// init here instead of ::Init()
    sehISRPC_Init(_wdiginstaller_IfHandle);

	HWND bhwnd = browser_hwnd();
	if (bStatusOnly)
	{
		if (sehISRPC_InitForStatus(_wdiginstaller_IfHandle, bhwnd) == 0)
		{
			*pInitSucceeded = 1;
			errorLog <<vos::datestamp()<< "InitForStatus() success" << endl;
		}
	}
	else if (sehISRPC_InitForRun(_wdiginstaller_IfHandle, bhwnd, deployment, downloadServer, downloadVersion) == 0)
#endif
	{
		*pInitSucceeded = 1;
		errorLog
#if defined(USE_RPCINSTALLER)
            <<vos::datestamp()
#endif
            << "InitForRun() success" << endl;
	}
	return S_OK;
}

STDMETHODIMP CWDI_InstallerCtrl::RunInstaller()
{
#ifndef USE_RPCINSTALLER
  ttInstaller->runInstaller();
#else
	sehISRPC_RunInstaller(_wdiginstaller_IfHandle);
#endif
  return S_OK;
}

STDMETHODIMP CWDI_InstallerCtrl::getValue(BSTR key, BSTR *pVal)
{
	_bstr_t keyName(key);
#ifndef USE_RPCINSTALLER
  string keyValStr;

  // COM design means returning something other than S_OK will crash the script,
  // so indicate failure by returning the empty string in pVal
  ttInstaller->getKeyValue(keyName,keyValStr);

  _bstr_t retVal(keyValStr.c_str());
  SysReAllocString(pVal, retVal);
#else
	sehISRPC_getValue(_wdiginstaller_IfHandle, key, pVal);
	_bstr_t val;
	char *tval = "";
	if (pVal && *pVal) {
	val = *pVal;
	tval = val;
	}
	//errorLog << "getValue("<<keyName<<") got: " << tval << endl;
#endif

  return S_OK;
}

STDMETHODIMP CWDI_InstallerCtrl::setValue(BSTR key, BSTR value)
{
#ifndef USE_RPCINSTALLER
  _bstr_t keyName(key);
  _bstr_t val(value);

  ttInstaller->setKeyValue(keyName, val);
#else
  sehISRPC_setValue(_wdiginstaller_IfHandle, key, value);
#endif

  return S_OK;
}

#ifdef USE_IE_ASYNC_DOWNLOAD
void CWDI_InstallerCtrl::
OnData(COurBindStatusCallback<CWDI_InstallerCtrl>* pbsc, DWORD grfBSCF, BYTE* pBytes, DWORD dwSize)
{
	if (grfBSCF == 0)
	{
		// Done. cleanup
		return;
	}

	DWORD dwActuallyRead = pbsc->m_dwTotalRead + dwSize;
	// If this is the first piece of data
	// make sure the buffer is empty
	if ( BSCF_FIRSTDATANOTIFICATION & grfBSCF ) {
        OnDownloadBegin();
	}

	// If we actually received some data
	// append it to our buffer
	if ( dwSize )
	{
		if (pbsc->m_dwAvailableToRead) {
			OnDownloadProgress();
		}
		// Append
	}

	// We have received all of the data
	// Inform the control (and user) that it
	// can now draw safely
	if ( BSCF_LASTDATANOTIFICATION & grfBSCF ) {
		OnDownloadComplete(pbsc->m_dwAvailableToRead, pBytes);
	}
}

static CWDI_InstallerCtrl *downloadControl = 0;
static const char *dlURL;
static const char *dlDestFilename;
static FILE* dlFilePtr;
volatile static int dlDone;
static int dlResult; // 0 == success

void CWDI_InstallerCtrl::
StartDownload(const char *URL)
{
  _bstr_t bURL(URL);
  COurBindStatusCallback<CWDI_InstallerCtrl>::Download(this, OnData,bURL, m_spUnkSite, FALSE);
}

void CWDI_InstallerCtrl::
OnDownloadBegin() {
  errorLog << "OnDownloadBegin" << endl;
}

void CWDI_InstallerCtrl::
OnDownloadProgress() {
  errorLog << "OnDownloadProgress" << endl;
}

void CWDI_InstallerCtrl::
OnDownloadComplete(DWORD availableToRead, BYTE* pBytes)
{
  errorLog << "OnDownloadComplete" << endl;

  errorLog << "opening " << dlDestFilename << " for write" << endl;
  // open the file
  dlFilePtr = fopen(dlDestFilename, "wb");
  if (!dlFilePtr) {
    errorLog << "error opening file" << endl;
    dlResult = -1;
    dlDone = 1;
  }

  if (fwrite(pBytes, availableToRead, 1, dlFilePtr) != 1) {
    errorLog << "error writing to " << dlDestFilename << endl;
    dlResult = -1;
    dlDone = 1;
  }

  // close the file
  fclose(dlFilePtr);
  dlFilePtr = NULL;

  dlResult = 0;
  dlDone = 1;
}

int downloadToFile_callback(const char* URL, const char* destFilename)
{
  if (0 == downloadControl) return -1;

  dlURL = URL;
  dlDestFilename = destFilename;
  dlDone = 0;
  dlResult = -1;

  errorLog << "starting the download of " << dlURL << endl;
  // kick off the download
  downloadControl->StartDownload(dlURL);

  // wait for the download to finish
  //while (!dlDone) {
    Sleep(3 * 1000);
  //}

  errorLog << "file download result: " << dlResult << endl;
  return dlResult;
}

void initDownloadCallback(CWDI_InstallerCtrl* obj, toontownInstaller* installer)
{
  downloadControl = obj;
  installer->setDownloadToFileCallback(downloadToFile_callback);
}
#endif

HWND CWDI_InstallerCtrl::browser_hwnd()
{
	HWND ie_window = NULL, parent = NULL;
	IOleWindow *pOleWindow;
	if (SUCCEEDED(GetSite(IID_IOleWindow, (LPVOID*)&pOleWindow)))
	{
		pOleWindow->GetWindow(&ie_window);
		pOleWindow->Release();
	}

	CWindow wnd(ie_window);
	ie_window = wnd.GetTopLevelParent();
#if 0
	// move from Internet Explorer_Server -> Shell DocObject View -> IEFrame (or the most ancestor)
	while(ie_window != NULL)
	{	// can't use GetAncestor() because it's WINVER 0x500 and later
		last_hwnd = ie_window;
		ie_window = GetParent(ie_window);
	}
	ie_window = parent;
#endif

	if (ie_window)
	{	// see if it's an IEFrame
		TCHAR classname[MAX_PATH];
		if ((GetClassName(ie_window, classname, MAX_PATH - 1) == 0)
			|| _tcsncmp(_T("IEFrame"), classname, MAX_PATH) )
		{   // If it's not a IEFrame, then I can't use it so blow it.
			errorLog << hex << ie_window << " isn't IEFrame. It's a "<<classname<<". Not using it." << endl;
			ie_window = NULL;
		}
	}

#if 0
	std::stringstream debug;
	debug << ie_window;
	::MessageBox(NULL, debug.str().c_str(), NULL, 0);
#endif
	errorLog << "IE hwnd: " << hex << ie_window << endl;

	return ie_window;
}

#if defined(USE_RPCINSTALLER)

// composes the RPC connection identifier for external Installer Helper
int CWDI_InstallerCtrl::RPCstartup(bool setMediumIntegrity)
{
	// setup RPC connection to external Install helper
	RPC_STATUS status;
	unsigned char *pszUuid                = (unsigned char *) "976e0c58-26ec-457e-9540-7b4c2a6dbcf2";
    unsigned char *pszProtocolSequence    = (unsigned char *) "ncalrpc";
	unsigned char *pszEndpoint            = NULL;
    unsigned char *strBinding;  // RPC binding string

    status = RpcStringBindingCompose(pszUuid,  // uuid
                                     pszProtocolSequence,
                                     NULL,  // network address
                                     pszEndpoint,
                                     NULL,  // options
                                     &strBinding);
#if defined(_DEBUG)
    errorLog << "RpcStringBindingCompose returned $" << hex << status << endl;
#endif
    //errorLog << "stringBinding = " << strBinding << endl;
    if (status != RPC_S_OK) {
        errorLog << "client: RPC binding compose failed: $" << hex << status << endl;
	    return -1;
    }

    /* Set the binding handle that will be used to bind to the server. */
    status = RpcBindingFromStringBinding(strBinding,
                                         &_wdiginstaller_IfHandle);
    //errorLog << "RpcBindingFromStringBinding returned $" << hex << status << endl;
    RpcStringFree(&strBinding);      // free binding string
    if (status != RPC_S_OK) {
    	errorLog << "rpc binding failed $" << hex << status << endl;
	    return -1;
    }
	else
		errorLog <<vos::datestamp()<< "rpc binding OK" << endl;

#ifdef USE_RPC_SECURITY
	// setup RPC security
	RPC_SECURITY_QOS SecurityQOS_oldOS = {
		RPC_C_SECURITY_QOS_VERSION,
		RPC_C_QOS_CAPABILITIES_MUTUAL_AUTH,
		RPC_C_QOS_IDENTITY_DYNAMIC,
		RPC_C_IMP_LEVEL_IMPERSONATE
	};
	RPC_SECURITY_QOS_V2 SecurityQOS = {
		RPC_C_SECURITY_QOS_VERSION_2,
		RPC_C_QOS_CAPABILITIES_MUTUAL_AUTH,
		RPC_C_QOS_IDENTITY_DYNAMIC,
		RPC_C_IMP_LEVEL_IMPERSONATE,
		0, 0
	};
	RPC_SECURITY_QOS *pSecurityQOS = (RPC_SECURITY_QOS *) &SecurityQOS;

	unsigned long AuthnLevel = RPC_C_AUTHN_LEVEL_PKT_PRIVACY;
	// Win9X only supports RPC_C_AUTHN_LEVEL_CONNECT
	if (_sysinfo.get_os_type() < vos::sysinfo_t::OS_Win2000) {
		AuthnLevel = RPC_C_AUTHN_LEVEL_CONNECT;
		pSecurityQOS = &SecurityQOS_oldOS;
	}

	//RpcBindingInqAuthInfo(_wdiginstaller_IfHandle, spn, authnl, authns, NULL,
	//TODO: fix error 87 for Vista
	status = RpcBindingSetAuthInfoEx(_wdiginstaller_IfHandle, /* SPN */ NULL,
		/* AuthnLevel */ AuthnLevel, /* AuthnSvc */ /*RPC_C_AUTHN_WINNT*/ RPC_C_AUTHN_DEFAULT,
		/* AuthIdentity */ NULL, /* AuthzSvc */ RPC_C_AUTHZ_NONE, pSecurityQOS);
    if (status != RPC_S_OK) {
        errorLog << "rpc binding authentication: " << status << endl;
	    return -1;
    }
#endif

	errorLog << "setup to InstallHelper server complete" << endl;

	// wait for external InstallHelper server to startup
	const size_t wait_time = 100;
	const size_t wait_loops = (100*1000)/wait_time;		// wait 60 seconds
	for(size_t wait = 0; wait < wait_loops; wait++)
	{
		if (sehISRPC_ready(_wdiginstaller_IfHandle) == 0) {
			goto RPC_avail;
		}
		vos::msleep(wait_time);
	}
	errorLog << "RPC connection to InstallHelper timed out" << endl;
	return -1;

RPC_avail:
	if (setMediumIntegrity)
	{	// make sure it's running in medium integrity outside Protected Mode sandbox
		// WARNING: has side-effect of performing self-update so need to always run it once
		//
		int ec = sehISRPC_DoMediumIntegrity(_wdiginstaller_IfHandle);
		switch(ec)
		{
		case 0:         // it didn't need to self-update so continue
        case 1:         // try restart because it moved or self-updated
			return ec;
		default:
			errorLog <<vos::datestamp()<< "failed to setup InstallHelper for runtime use. " << dec << vos::last_error_str(ec) << endl;
			return -1;
		}
	}

	return 0;
}

HRESULT CWDI_InstallerCtrl::FinalConstruct()
{
	vos::errorlog_open(vos::tempdir() + "WDIGiehelperX" + vos::log_suffix());
	errorLog << "built: " << __DATE__ << ' ' << __TIME__ << endl;

	return S_OK;
}

void CWDI_InstallerCtrl::FinalRelease()
{
//	RPC_Shutdown();
    sehISRPC_Shutdown(_wdiginstaller_IfHandle);  // shut down the server side

    vos::errorlog_close();
    RPC_STATUS status = RpcBindingFree(&_wdiginstaller_IfHandle);   // remote calls done; unbind
}

#if 0
//
// downloads installer service, checksums, applies necessary patches
//
int installer_service_update()
{
    vrfile_norm_t file;
	int rv;

	rv = download_lib(file, myREG.str(vos::vregBOOT_URLSRC),
						myREG.str(vos::vregINSTALL_PATH),
						myREG.str(vos::vregBOOT1_DLFILE),
						myREG.str(vos::vregBOOT_DDB) );
	if (rv < 0) {
		// can't continue properly if this isn't up-to-date
		errorLog << "unrecoverable error updating boot1 Install Helper" << endl;
		return -1;
	}

	errorLog << "update checks for boot1 completed" << endl;
	return 0;		// all good
}
#endif

/*********************************************************************/
/*                 MIDL allocate and free                            */
/*********************************************************************/

void  __RPC_FAR * __RPC_USER midl_user_allocate(size_t len)
{
    return(new uint8_t[len+ sizeof(_TCHAR)]);
}

void __RPC_USER midl_user_free(void __RPC_FAR * ptr)
{
    delete[] ptr;
}

#endif  // USE_RPCINSTALLER

