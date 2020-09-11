// service.cpp : Defines the entry point for the console application.
//

#include "win32/SVCstdafx.h"
#include "win32/installer_service.h"

#include <vos/vos.hpp>
#include <vos/thread.hpp>
#include <vos/proc.hpp>

#include <vos/iut/bootstrap_downloader.hpp>

using namespace vos;

ofstream errorLog;
bool errorLog_opened = false;
vos::registry_t myREG;

pid_t gttinstaller_pid;

//
// RPC server
//
VTHR_RET Installer_Service (voidp_t param)
{
	//uint8_t *protocolseq = (uint8_t*) "ncacn_np";
	//uint8_t *endpoint = (uint8_t*) "\\pipe\\wdig-inst";
	unsigned char *protocolseq = (unsigned char *) "ncalrpc";
	unsigned char *endpoint = (unsigned char *) "wdigInstallerSvc";
	//unsigned char *endpoint = NULL;
	bool fDontWait = false;

	RPC_STATUS status;
	status = RpcServerUseProtseqEp( protocolseq, 1, endpoint, NULL );
	//        status = RpcServerUseProtseq(protocolseq, 1, NULL);
	if (status != RPC_S_OK) {
		errorLog << "server: could not setup RPC protocol acceptor: 0x" << hex << status << endl;
		goto get_out;
	}

	// register MIDL generated RPC interface
	//        status = RpcServerRegisterIf(IWDIG_InstallerRPC_ServerIfHandle, NULL, NULL);
	status = RpcServerRegisterIf(IWDIG_InstallerService_v1_0_s_ifspec, NULL, NULL);

	if (status != RPC_S_OK) {
		errorLog << "server: could not register RPC interface: 0x" << hex << status << endl;
		goto get_out;
	}

	// start RPC server listener
	errorLog << "Toontown Installer Service starting up" << endl;

	status = RpcServerListen(1, 1, fDontWait);
	if (status != RPC_S_OK) {
		errorLog << "server: could not start RPC listener: 0x" << hex << status << endl;
		goto get_out;
	}

	if (fDontWait) {
		errorLog << "server: calling RpcMgmtWaitServerListen" << endl;
		status = RpcMgmtWaitServerListen();  // wait operation
		if (status != RPC_S_OK) {
			errorLog << "server: RpcMgmtWaitServerListen returned: 0x" << hex << status << endl;
			goto get_out;
		}
	}
get_out:

	return status;
}

//
// downloads main installer, [checksums], applies necessary patches
//
int update_main_installer()
{
    vrfile_norm_t file;
	int rv, tries = 0;
#if 0
	for(int tries = 0; tries < 2; tries++)
#else
	for(int tries = 0; tries < 1; tries++)
#endif
	{
		rv = download_lib(file, myREG.str(vos::vregBOOT_URLSRC),
							myREG.str(vos::vregINSTALL_PATH),
							myREG.str(vos::vregBOOT1_DLFILE),
							myREG.str(vos::vregBOOT_DDB) );
		errorLog << "update of " << myREG.str(vos::vregBOOT1_DLFILE) << ": " << rv << endl;
		if (rv < 0) {
			// can't continue properly if this isn't up-to-date
			errorLog << "unrecoverable error updating" << endl;
			return -1;
		}
	}
	return 0;		// all good
}

void checkIntegrityLevel()
{
#if !defined(OSIS_VISTA)
	if (sysinfo_t::get_os_type() < vos::sysinfo_t::OS_WinVista)
#endif
		return;

	HANDLE hToken;
	errorLog << "integrity level: ";
	if (OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY | TOKEN_QUERY_SOURCE, &hToken) == TRUE)
	{
		DWORD reqSize;
		DWORD ec;
		PTOKEN_MANDATORY_LABEL pTIL = NULL;

		GetTokenInformation(hToken, TokenIntegrityLevel, NULL, 0, &reqSize);
		ec = vos::last_error_code();
		if (ec == ERROR_INSUFFICIENT_BUFFER)
			pTIL = (PTOKEN_MANDATORY_LABEL) new uint8_t[reqSize];
		else
		{	// unrecognized error; get out
			CloseHandle(hToken);
			errorLog << vos::last_error_str(ec);
			return;
		}

		if ( pTIL && (GetTokenInformation(hToken, TokenIntegrityLevel, pTIL, reqSize, &reqSize) == TRUE) )
		{
			DWORD rid = *GetSidSubAuthority(pTIL->Label.Sid, (DWORD)(UCHAR) (*GetSidSubAuthorityCount(pTIL->Label.Sid)-1));
			switch (rid)
			{
			case SECURITY_MANDATORY_LOW_RID:
				// Low integrity process
					errorLog << "low integrity" << endl;
				break;

			case SECURITY_MANDATORY_MEDIUM_RID:
				// Medium integrity process
					errorLog << "medium integrity" << endl;
				break;

			case SECURITY_MANDATORY_HIGH_RID:
				{
				// High integrity process
					errorLog << "high integrity" << endl;
				break;
				}

			case SECURITY_MANDATORY_SYSTEM_RID:
				{
				// System integrity level
					errorLog << "system integrity" << endl;
				break;
				}
			default:
				errorLog << "no security integrity" << endl;
			}
		}
		else
		{
			CloseHandle(hToken);
			errorLog << vos::last_error_str() << endl;
			return;
		}
	}
}

int _tmain(int argc, _TCHAR* argv[])
{
	int nRetCode = 0;

	vos::errorlog_open(vos::tempdir() + "wdigInstallerSvc" + vos::log_suffix());
	checkIntegrityLevel();

	cout << "Nothing to see here. Move along." << endl;

#if 0
	myREG.str(vos::vregBOOT_URLSRC) = "http://ttown2.online.disney.com:2421/portuguese/currentVersion/";
	myREG.str(vos::vregBOOT1_DLFILE) = "tt-installer.exe";
	myREG.str(vos::vregINSTALL_PATH) = vos::tempdir();

	// download main installer
	if (update_main_installer() != 0)
	{	// could be fatal error, if couldn't download main installer
		errorLog << "Toontown Installer download error" << endl;
#if !defined(_DEBUG)	// ignore if in development mode
		return -1;
#endif
	}

// startup Installer Service RPC thread
/*
	if (vos::vthread_create(_InstallerServiceThread, Installer_Service, NULL) != )
	{	// thread didn't startup so error out
		static const vchar_t *errorstr = "Could not start up Installer RPC Service";
		errorLog << errorstr << endl;
		OSMessageBox(errorstr, "Toontown Installer Service");
		return -1;
	}
*/
//
// Run main installer
// : assume that the installer won't try to connect to this RPC server "immediately",
// : and will use the _ready() synchronization
//
	errorLog << "starting up Toontown Installer" << endl;
	vstr_t phase0exe = myREG.str(vos::vregINSTALL_PATH) + myREG.str(vos::vregBOOT1_DLFILE);
	if (vos::rfork_execve(phase0exe.c_str(), NULL, NULL, gttinstaller_pid, elHigh) != 0)
	{
		errorLog << "Toontown Installer failed to startup" << endl;
		return -1;
	}
	else
		errorLog << "Toontown Installer started successfully" << endl;
#endif

	int ec;
	// raise MY Mandatory Integrity Level to medium (Vista)
	if (ec = vos::file::set_integrity_level(argv[0], il_Medium))
	{
		errorLog << "failed setting medium mandatory integrity level for " << argv[0] << ". " << vos::last_error_str(ec) << endl;
	}

// Run Installer Service RPC
	return static_cast<ssize_t>(Installer_Service(NULL));
}
