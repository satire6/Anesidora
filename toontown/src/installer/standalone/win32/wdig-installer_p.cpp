#include "SAstdafx.h"
#include <iostream>
#include <Rpc.h>
#include <comdef.h>

#include <set>

#ifndef RPC_IF_ALLOW_LOCAL_ONLY					// includeded SDK headers are out of date
#	define RPC_IF_ALLOW_LOCAL_ONLY				0x0020
#endif

#include "../saTT.hpp"
#include "../standalone.h"
#include "wdig-installer.h"
#include "service/win32/installer_service.h"

#include <vos/vos.hpp>
#include <vos/thread.hpp>
#include <vos/proc.hpp>
#include <vos/fs.hpp>

#include <vos/iut/vrfile.h>
#include <vos/iut/bootstrap_downloader.hpp>
#include "../shToontownInstaller.hpp"			// new Toontown Installer wrapping of Install Shell API (ISA?) utility kit

handle_t installerservice_IfHandle;
vos::registry_t serviceREG;

bool bInitialized = false;
bool bInitForRun = false;						// gate for run or status
std::set<const vchar_t *> regIntercept;

pid_t InstallerSvc_pid = 0;

ToontownInstaller app;							// re-imagined installer/updater object

using namespace std;
using namespace vos;

/*********************************************************************/
/*                 MIDL allocate and free                            */
/*********************************************************************/

#if !defined(USE_RPCINSTALLER)
void  __RPC_FAR * __RPC_USER midl_user_allocate(size_t len)
{
//	errorLog << "midl_user_allocate() asking for "<<len<<" bytes" << endl;
    return(new uint8_t[len + sizeof(_TCHAR)]);	// +n for null char
}

void __RPC_USER midl_user_free(void __RPC_FAR * ptr)
{
    delete[] ptr;
}
#endif

///////////////////////////////////////////////////////////////////////////////
// internal functions
//

int sehISPROC_shutdown();
VTHR_RET InstallerService_RPCconnect(voidp_t param);
//static ssize_t self_update();

void Shutdown()
{
	sehISPROC_shutdown();

	RPC_STATUS status;
    //errorLog << "Calling RpcMgmtStopServerListening" << endl;
    status = RpcMgmtStopServerListening(NULL);
    //errorLog << "RpcMgmtStopServerListening returned: $" << hex << status << endl;
    if (status != RPC_S_OK) {
		errorLog << "RpcMgmtStopServerListening returned: $" << hex << status << endl;
		cerr << "RpcMgmtStopServerListening returned: $" << hex << status << endl;
       //exit(status);
    }

    //errorLog << "Calling RpcServerUnregisterIf" << endl;
    status = RpcServerUnregisterIf(IWDIG_InstallerRPC_v1_1_s_ifspec, NULL, FALSE);
    if (status != RPC_S_OK) {
		errorLog << "RpcServerUnregisterIf returned $" << hex << status << endl;
		cerr << "RpcServerUnregisterIf returned $" << hex << status << endl;
       //exit(status);
    }
}

//
// downloads installer service, checksums, applies necessary patches
// returns 0 if nothing changed, 1 if file updated, else error code
//
int file_update(vos::registry_t &info)
{
    vrfile_norm_t file;
	int rv;

	rv = download_lib(file, info.str(vos::vregBOOT_URLSRC),
						info.str(vos::vregINSTALL_PATH),
						info.str(vos::vregBOOT0_DLFILE),
						info.str(vos::vregBOOT_DDB) );
	if (rv < 0) {
		// can't continue properly if this isn't up-to-date
		errorLog << "unrecoverable error updating " << info.str(vos::vregBOOT0_DLFILE) << endl;
		return -1;
	}

	errorLog << "update checks for " << info.str(vos::vregBOOT0_DLFILE) << " completed" << endl;
	return rv;		// all good
}

/*
int InstallService_update()
{
	int stat = file_update(serviceREG);
	if (stat < 0)
	{	// fatal error if couldn't download installer
		errorLog << serviceREG.str(vos::vregBOOT0_DLFILE) << " download error" << endl;
	}
	else
		errorLog << serviceREG.str(vos::vregBOOT0_DLFILE) << " available" << endl;
	InstallerSvc_avail = (stat >= 0);
	return stat;
}
*/

int HighIntegrity_enter()
{
	//int stat;
	switch(getIntegrityLevel())
	{
	case vos::il_Low:				// fix Vista BUG? where low integrity exec of requireAdmin app hangs instead of spawning elevation prompt
		errorLog << "bootstrapping InstallService from low integrity" << endl;
		return 2;

	default:						// normal kick off installer_service
		vstr_t prog = serviceREG.str(vos::vregINSTALL_PATH) + serviceREG.str(vos::vregBOOT0_DLFILE);
		rfork_params_t params;
		params.hwnd = sa.installerHWND();

		if (vos::rfork_execve(prog.c_str(), NULL, NULL, InstallerSvc_pid, params) || (InstallerSvc_pid == 0))
		{
			errorLog << "Could not start up " <<  serviceREG.str(vos::vregBOOT0_DLFILE) << endl;
			return -1;
		}

		errorLog << serviceREG.str(vos::vregBOOT0_DLFILE) << " started successfully" << endl;
	}

	return static_cast<int>(InstallerService_RPCconnect(NULL));
}

int HighIntegrity_exit()
{
/*	if (InstallerSvc_avail)
		return 0;
		//sehISPROC_shutdown();			// leave it running
	else
		return -1;*/
	return 0;
}

///////////////////////////////////////////////////////////////////////////////
// Installer Service callouts and functionality
//

// pinger to check ready status
int sehISPROC_ready()
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        return ISPROC_ready(installerservice_IfHandle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
    return ulCode;
}

VTHR_RET InstallerService_RPCconnect(voidp_t param)
{
	// connect to InstallerService RPC server for high integrity calls
	errorLog <<vos::datestamp()<< "connecting to InstallerService RPC" << endl;

    RPC_STATUS status;
    unsigned char *pszProtocolSequence    = (unsigned char *) "ncalrpc";
    unsigned char *pszEndpoint            = (unsigned char *) "wdigInstallerSvc";
    unsigned char *strBinding;  // RPC binding string

    status = RpcStringBindingCompose(NULL,  // uuid
                                     pszProtocolSequence,
                                     NULL,  // network address
                                     pszEndpoint,
                                     NULL,  // options
                                     &strBinding);
#if defined(_DEBUG)
    errorLog << "RpcStringBindingCompose returned $" << hex << status << endl;
    errorLog << "stringBinding = " << strBinding << endl;
#endif
    if (status != RPC_S_OK) {
        errorLog << "client: could not setup RPC binding string: $" << hex << status << endl;
	    return -1;
    }

    /* Set the binding handle that will be used to bind to the server. */
    status = RpcBindingFromStringBinding(strBinding, &installerservice_IfHandle);
#if defined(_DEBUG)
    errorLog << "RpcBindingFromStringBinding returned $" << hex << status << endl;
#endif

    RpcStringFree(&strBinding);      // free binding string
    if (status != RPC_S_OK) {
	    return -1;
    }

	for(size_t i = 0; i < (3*1000/100); i++)	// wait 30 seconds
	{
		if (sehISPROC_ready() == 0)
		{
			errorLog <<vos::datestamp()<< "Connected..." << endl;
			return 0;
		}
		vos::msleep(100);
	}

    return -1;
}

// installer service (not EXE RPC) shutdown callout
int sehISPROC_shutdown()
{
    unsigned int ulCode = 0;
    RpcTryExcept
    {
        return ISPROC_shutdown(installerservice_IfHandle);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
    return ulCode;
}

///////////////////////////////////////////////////////////////////////////////

#if 0
int sehISPROC_rforkexec(BSTR app_path, BSTR args, DWORD &procId, HANDLE procHandle)
{
    int retCode = 0;
    RpcTryExcept
    {
        errorLog << "calling ISPROC_rforkexec()" << endl;
		retCode = ISPROC_rforkexec(installerservice_IfHandle, app_path, args, &procId);
		errorLog << "ISPROC_rforkexec() returned with: " << retCode << endl;

        if (retCode == 0)
		{	// emulate these values to pi
			procHandle = vos::process_handle(procId);
		}
		else
		{	// default values
			procId = 0;
			procHandle = NULL;
		}
    }
    RpcExcept(1) {
        retCode = RpcExceptionCode();
        errorLog << "Runtime reported exception $" << hex << retCode << endl;
		procId = 0;
		procHandle = NULL;
    }
    RpcEndExcept

    return retCode;
}
#endif

int sehISFILE_MakeGameDir(int game, BSTR deployment)
{
    unsigned int ulCode = 0;
	ulCode = HighIntegrity_enter();
	if (ulCode) return ulCode;
    RpcTryExcept
    {
        return ISFILE_MakeGameDir(installerservice_IfHandle, game, deployment);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
	HighIntegrity_exit();
    return ulCode;
}

int sehISREG_DoMediumIntegrity(const int game, const BSTR src_path, const BSTR dest_path)
{
    unsigned int ulCode = 0;
	ulCode = HighIntegrity_enter();
	if (ulCode) return ulCode;
    RpcTryExcept
    {
        return ISREG_DoMediumIntegrity(installerservice_IfHandle, game, src_path, dest_path);
    }
    RpcExcept(1) {
        ulCode = RpcExceptionCode();
    }
    RpcEndExcept
//	HighIntegrity_exit();				// leave service running
    return ulCode;
}

//
// Installer RPC handlers
//

int __stdcall ISRPC_ready(
    /* [in] */ handle_t IDL_handle)
{
#if defined(OSIS_VISTA)
	errorLog << "hardcoded for Vista" << endl;
#endif
	return 0;			// dummy ping routine that returns 0 if RPC server is up and running
}

// if Vista, setup IE7 protected mode to allow Medium Integrity elevation of myself on next execution
//
// returns 0 if no restarted needed,
//         1 if so, otherwise some error code
int __stdcall ISRPC_DoMediumIntegrity(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ int game)
{
	using namespace vos;
	errorLog << "ISRPC_DoMediumIntegrity()" << endl;

	// get out if not a recognized game code
	switch(game)
	{
	case 0: // Toontown
		break;
	default:
		errorLog << "unrecognized game" << endl;
		return -1;
	}

	int ec = 0;
	// self-update checks
	const vstr_t &install_dir = app.install_dir();
	_bstr_t srcdir(tempdir().c_str()), destdir(install_dir.c_str());

	if (sysinfo_t::VistaOrBetter())
	{	// running under Windows Vista
		IntegrityLevel integrity_level = vos::getIntegrityLevel();
#if defined(OSIS_VISTA)
		integrity_level = il_Low;
#endif
		switch(integrity_level)
		{
		case vos::il_Medium:
			break;			// goto self-update
		default:			// fix IE setup and restart
			ec = sehISREG_DoMediumIntegrity(game, srcdir.GetBSTR(), destdir.GetBSTR());
			ec = (ec == 0) ? 1 : ec;
		}
	}

#if 0
	//
	// do self-update
	//
	ec = self_update();
	if (ec < 0)
		return ec;
	else
	{
		errorLog << "self-update() successful" << endl;
		return 1;
	}
#endif
	return ec;
}

RPC_STATUS CALLBACK ISRPC_SecurityCallback(RPC_IF_HANDLE Interface, void *Context)
{
	ULONG ulAuthnLevel;
	ULONG ulAuthnSvc;

	if (RpcBindingInqAuthClient(Context, NULL, NULL, &ulAuthnLevel, &ulAuthnSvc, NULL) != RPC_S_OK)
		return RPC_S_ACCESS_DENIED;

	// Make sure the client has adequate security measures and uses the expected
    // security provider.
	if (vos::sysinfo_t::get_os_type() >= vos::sysinfo_t::OS_Win2000)
	{	// Win2K and up
		if ((ulAuthnLevel != RPC_C_AUTHN_LEVEL_PKT_PRIVACY) || (ulAuthnSvc != RPC_C_AUTHN_WINNT))
			return RPC_S_ACCESS_DENIED;
	}
	else
	{	// WinME and down
		if ((ulAuthnLevel != RPC_C_AUTHN_LEVEL_CONNECT) || (ulAuthnSvc != RPC_C_AUTHN_WINNT))
			return RPC_S_ACCESS_DENIED;
	}

    return RPC_S_OK;
}

///////////////////////////////////////////////////////////////////////////////
//
// Primary "main"/constructor section for this program
//
///////////////////////////////////////////////////////////////////////////////

VTHR_RET InstallerStart (voidp_t param)
{
    unsigned char *protocolseq = (unsigned char *) "ncalrpc";
    //unsigned char *endpoint = (unsigned char *) "wdig_installer_exe";
    bool fDontWait = false;
	RPC_BINDING_VECTOR *pBindingVector = NULL;
    RPC_STATUS status;

/*
 *  Bring up the InstallHelper RPC interface for the ActiveX to talk to
 */

//////////
// secure interface
#if 1
	vos::sysinfo_t::OSType curr_os = vos::sysinfo_t::get_os_type();
	size_t if_flags = 0;

#ifdef USE_RPC_SECURITY
	if_flags = RPC_IF_ALLOW_SECURE_ONLY;
	if (curr_os >= vos::SysInfo::OS_WinXP)
	{	// use better security settings in XP and up
		if_flags |= RPC_IF_ALLOW_LOCAL_ONLY;
	}

	// register interface
	status = RpcServerRegisterIf2(IWDIG_InstallerRPC_v1_1_s_ifspec,
		/* uuid */ NULL, NULL, /* flags */ if_flags, /* maxcalls */ 1, /* maxrpcsize */ 1024, /* callback */ ISRPC_SecurityCallback);
#else
	status = RpcServerRegisterIf2(IWDIG_InstallerRPC_v1_1_s_ifspec,
		/* uuid */ NULL, NULL, /* flags */ if_flags, /* maxcalls */ 1, /* maxrpcsize */ 1024, /* callback */ NULL);
#endif
	if (status != RPC_S_OK) {
        errorLog << "server: could not register RPC interface: $" << hex << status << endl;
		// probably another already running
        goto get_out;
    }

	// register protocols to be used
	status = RpcServerUseProtseq(protocolseq, 1, NULL);
    if (status != RPC_S_OK) {
        errorLog << "server: could not register RPC protocol sequence: $" << hex << status << endl;
        goto get_out;
    }

	// get a vector of bindings available for the server
	status = RpcServerInqBindings(&pBindingVector);
    if (status != RPC_S_OK) {
        errorLog << "server: could not get vector to bindings available: $" << hex << status << endl;
        goto get_out;
    }

	// register rpc service using an available binding in the endpoint-map database
	status = RpcEpRegister(IWDIG_InstallerRPC_v1_1_s_ifspec, pBindingVector,
		/* uuid */ NULL, /* annotation */ (unsigned char *) "wdig_installer_exe");
    if (status != RPC_S_OK) {
        errorLog << "server: failed to register in the endpoint-map database: $" << hex << status << endl;
        goto get_out;
    }

	// generate the Server Principal Name (SPN)
//	status = DsGetSpn(

#ifdef USE_RPC_SECURITY
	// register security authentication
	status = RpcServerRegisterAuthInfo(NULL, RPC_C_AUTHN_WINNT, NULL, NULL);
    if (status != RPC_S_OK) {
        errorLog << "server: could not setup rpc authentication: $" << hex << status << endl;
        goto get_out;
    }
#endif

#else

    status = RpcServerUseProtseqEp( protocolseq, 1, endpoint, NULL );
//        status = RpcServerUseProtseq(protocolseq, 1, NULL);
    if (status != RPC_S_OK) {
        errorLog << "server: could not setup RPC protocol acceptor: $" << hex << status << endl;
        goto get_out;
    }

    // register MIDL generated RPC interface
//        status = RpcServerRegisterIf(IWDIG_InstallerRPC_ServerIfHandle, NULL, NULL);
    status = RpcServerRegisterIf(IWDIG_InstallerRPC_v1_0_s_ifspec, NULL, NULL);
	if (status != RPC_S_OK) {
        errorLog << "server: could not register RPC interface: $" << hex << status << endl;
		// probably another already running
        goto get_out;
    }

#endif

/*
 *  Setup for the "service" that will executed as needed to handle all the "high integrity" needs such as registry writing and such
 */
	// registry call intercepts for NextGen installer
	regIntercept.clear();
	regIntercept.insert("Deployment");
	regIntercept.insert("DownloadServer");
	regIntercept.insert("DownloadVersion");

	// TODO: bake this in properly
//	serviceREG.str(vos::vregBOOT_URLSRC) = "http://ttown2.online.disney.com:2421/portuguese/currentVersion/";
	serviceREG.str(vos::vregINSTALL_PATH) = app.install_dir();
	serviceREG.str(vos::vregBOOT0_DLFILE) = "wdigInstallerSvc.exe";

	bInitialized = false;						// program NOT initialized for downloads/registry access/etc
	bInitForRun = false;						// NOT initialized for exec Toontown program	
	errorLog << vos::datestamp() << "Waiting for initialization." << endl;

//
// start my RPC server listener
//
	errorLog << "RPCserver4AX successful.  Listening." << endl;
	//HANDLE ExeServer_ready = CreateMutex(NULL, FALSE, _T("tt_RPCserver4AX"));
	//errorLog << vos::last_error_str() << endl;

    status = RpcServerListen(1, 1, fDontWait);
    if (status != RPC_S_OK) {
        errorLog << "server: could not start RPC listener: $" << hex << status << endl;
        goto get_out;
    }
	//CloseHandle(ExeServer_ready);

    if (fDontWait) {
        errorLog << "server: calling RpcMgmtWaitServerListen" << endl;
        status = RpcMgmtWaitServerListen();  // wait operation
        if (status != RPC_S_OK) {
            errorLog << "server: RpcMgmtWaitServerListen returned: $" << hex << status << endl;
            goto get_out;
        }
    }
get_out:
	return status;
}

// RPC shutdown routines
void __stdcall ISRPC_Shutdown(
    /* [in] */ handle_t IDL_handle)
{
	errorLog <<vos::datestamp()<< "shutting down RPC" << endl;
	Shutdown();
}

///////////////////////////////////////////////////////////////////////////////

//
//  normal ActiveX/COM call interface
//

void __stdcall ISRPC_Init(
    /* [in] */ handle_t IDL_handle)
{
//	errorLog << "got RPC message: Init()" << endl;
	sa.init();
	bInitialized = true;
}

// SHOULD be called for JUST logfiles and registry access
// returns 0 if okay, otherwise undefined error code
//
int __stdcall ISRPC_InitForStatus( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ __int64 hwnd)
{
	HWND bhwnd = (HWND) hwnd;
	bInitialized = false;
	if (errorLog_opened)
		errorLog << "RPC InitForStatus("<<bhwnd<< ')' << endl;

//	if (sa.normalInit(bhwnd, NULL, NULL, NULL))
//	{
		bInitialized = true;
		return 0;
//	}
//	else
//		return -1;
}

// SHOULD be called before anything else
// returns 0 if okay, otherwise undefined error code
//
int __stdcall ISRPC_InitForRun( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ __int64 hwnd,
    /* [in] */ BSTR bsDeployment,
    /* [in] */ BSTR bsDownloadServer,
    /* [in] */ BSTR bsDownloadVersion)
{
	HWND bhwnd = (HWND) hwnd;
	_bstr_t deployment(bsDeployment), downloadServer(bsDownloadServer), downloadVersion(bsDownloadVersion);
	bInitForRun = bInitialized = false;
	if (errorLog_opened)
	{
		errorLog << "RPC InitForRun("<<bhwnd
			<<' '<<deployment<<' '<<downloadServer<<' '<<downloadVersion<< ')' << endl;
	}
	if (sa.normalInit(bhwnd, deployment, downloadServer, downloadVersion))
	{
		bInitForRun = bInitialized = true;
		return 0;
	}
	else
		return -1;
}

void __stdcall ISRPC_getValue( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [retval][out] */ BSTR *pVal)
{
	if (pVal == NULL) return;
	_bstr_t keyName(key);

	if (!bInitialized)
	{	// can't request values until initialized
		errorLog << vos::datestamp() << "getValue("<< keyName << ':'<<keyName.length()<<") denied because not initialized." << endl;
		_bstr_t retVal("0");
		SysReAllocString(pVal, retVal);
		return;
	}

	std::string keyValStr;
	sa.getKeyValue(keyName, keyValStr);
//	errorLog << vos::datestamp() << "getValue("<< keyName << ':'<<keyName.length()<<") got " << keyValStr << endl;

	_bstr_t retVal(keyValStr.c_str());
	SysReAllocString(pVal, retVal);
}

void __stdcall ISRPC_setValue(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [in] */ BSTR val)
{
	_bstr_t keyName(key),
		value(val);

	if (regIntercept.find(keyName) != regIntercept.end())
	{	// intercept initialization setting for NextGen Installer Shell
		if ((const vchar_t *) keyName == "Deployment")
			;//app.Deployment(val);
		else if ((const vchar_t *)keyName == "DownloadServer")
			app.DownloadServer((const vchar_t *)val, true);
		else if ((const vchar_t *)keyName == "DownloadVersion")
			app.DownloadVersion((const vchar_t *)val);

		return;
	}
	else if (!bInitialized)
	{
		errorLog << vos::datestamp() << "setValue("<< keyName << ':'<<keyName.length()<<") denied because not initialized." << endl;
		return;
	}

//	errorLog << vos::datestamp() << "got RPC setValue("<< keyName.length()<<keyName << ", " << val<<val.length() << ')' << endl;
//	errorLog << vos::datestamp() << "RPC setValue("<< keyName << ", " << value << ')' << endl;

	sa.setKeyValue(keyName, value);
}

void __stdcall ISRPC_RunInstaller(
    /* [in] */ handle_t IDL_handle)
{
	errorLog << datestamp() << "ISRPC_Run()" << endl;
	if (bInitForRun)
		sa.runInstaller();
	else
		errorLog << datestamp() << "NOT initialized for RunInstaller" << endl;
}

//
// private code
//
#if 0
static ssize_t self_update()
{
	vstr_t appname(APPNAME);
	appname += ".exe";

	registry_t update_info;
	update_info.str(vregBOOT_URLSRC) = app.urlsrc();
	update_info.str(vregINSTALL_PATH) = app.install_dir();
	update_info.str(vregBOOT0_DLFILE) = appname;

	int ec = -1;
	vstr_t orig = app.install_dir() + appname;
	vstr_t bak = app.install_dir() + appname + ".old";

	vos::remove(bak.c_str());							// remove any old copies lying around
	ec = vos::rename(orig.c_str(), bak.c_str());
	if (ec == 0)
	{
		ec = file_update(update_info);
		if (ec < 0)		// some error so rename binary back
			vos::rename(bak.c_str(), orig.c_str());
		// can only delete .old file on AFTER restart due to WIN32 mmapish locking of file image
	}
	return ec;
}
#endif
