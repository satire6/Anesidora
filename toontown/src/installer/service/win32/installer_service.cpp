#include "SVCstdafx.h"
#include "installer_service.h"

#include <vos/vos.hpp>
#include <vos/proc.hpp>

#include <comdef.h>

#include <shlobj.h>
#include <shfolder.h>

#include <Accctrl.h>
#include <Aclapi.h>

using namespace vos;

#define _str(s) #s
#define _xstr(s) _str(s)

#if defined(USE_JAPANESE) || defined(USE_PORTUGUESE) || defined(USE_FRENCH)
  #undef DEPLOYMENT
  #define DEPLOYMENT _xstr(PRODUCT_NAME)
#endif


// stores ptrs we need to free l8r all together
struct MySecurAttrib {
    PACL pACL;
    PSID pEveryoneSID;
    PSECURITY_DESCRIPTOR pSD;
    PSECURITY_ATTRIBUTES pSA;
};

// security entry points seem to be on win9x advapi32.dll though they may not be
// functional, so should be ok to statically link to InitializeSecurityDescriptor, etc

// use for reg and file system
static MySecurAttrib *makeGlobalRW_SecAttr(void)
{
    DWORD dwRes;
    EXPLICIT_ACCESS ea;
    SID_IDENTIFIER_AUTHORITY SIDAuthWorld = SECURITY_WORLD_SID_AUTHORITY;
    PACL pACL=NULL;
    PSID pEveryoneSID=NULL;
    PSECURITY_DESCRIPTOR pSD=NULL;
    HKEY hkSub = NULL;
    char *errstr=NULL;
    SECURITY_ATTRIBUTES *pSA = NULL;
    MySecurAttrib *pMySecurAttr = NULL;

    // Create a well-known SID for the Everyone group.

    if(!AllocateAndInitializeSid( &SIDAuthWorld, 1,
                     SECURITY_WORLD_RID,
                     0, 0, 0, 0, 0, 0, 0,
                     &pEveryoneSID) ) {
        errstr = "AllocateAndInitializeSid";
        goto Cleanup;
    }

    // Initialize an EXPLICIT_ACCESS structure for an ACE.
    // The ACE will allow Everyone read access to the key.

    memset(&ea, 0, sizeof(EXPLICIT_ACCESS));
    ea.grfAccessPermissions = KEY_ALL_ACCESS;
    ea.grfAccessMode = SET_ACCESS;
    ea.grfInheritance= NO_INHERITANCE;
    ea.Trustee.TrusteeForm = TRUSTEE_IS_SID;
    ea.Trustee.TrusteeType = TRUSTEE_IS_WELL_KNOWN_GROUP;
    ea.Trustee.ptstrName  = (LPTSTR) pEveryoneSID;

    // Create a new ACL that contains the new ACEs.

    dwRes = SetEntriesInAcl(1, &ea, NULL, &pACL);
    if (ERROR_SUCCESS != dwRes) {
        errstr = "SetEntriesInAcl";
        goto Cleanup;
    }

    // Initialize a security descriptor.

    pSD = (PSECURITY_DESCRIPTOR) LocalAlloc(LPTR, SECURITY_DESCRIPTOR_MIN_LENGTH);
    if (pSD == NULL) {
        errstr = "LocalAlloc";
        goto Cleanup;
    }

    if (!InitializeSecurityDescriptor(pSD, SECURITY_DESCRIPTOR_REVISION)) {
        errstr = "InitializeSecurityDescriptor";
        goto Cleanup;
    }

    // Add the ACL to the security descriptor.

    if (!SetSecurityDescriptorDacl(pSD,
            true,     // fDaclPresent flag
//            pACL,
            NULL,
            false))   // not a default DACL
    {
        errstr = "InitializeSecurityDescriptor";
        goto Cleanup;
    }

    pSA = new SECURITY_ATTRIBUTES;
    pSA->nLength = sizeof(SECURITY_ATTRIBUTES);
    pSA->bInheritHandle = true;
    pSA->lpSecurityDescriptor = pSD;


    pMySecurAttr = new MySecurAttrib;
    if(!pMySecurAttr)
        goto Cleanup;

    pMySecurAttr->pSA=pSA;
    pMySecurAttr->pACL=pACL;
    pMySecurAttr->pEveryoneSID=pEveryoneSID;
    pMySecurAttr->pSD=pSD;

    return pMySecurAttr;

Cleanup:
    if (pEveryoneSID)
        FreeSid(pEveryoneSID);
    if (pACL)
        LocalFree(pACL);
    if (pSD)
        LocalFree(pSD);
    if (pSA)
      delete pSA;

    /*
    // not sure how to handle this error.  just note it in the log for now.
    // has occurred on non-english xp, not sure if language has anything to do with it,
    // or could be some domain config the user is in
    if(GetLastError()==ERROR_NONE_MAPPED) {
//    if(vos::last_error_code()==ERROR_NONE_MAPPED) {
        errorLog << errstr << " returned ERROR_NONE_MAPPED!\n";
    } else */
    //LogOSErrorMessage(errstr);
    return NULL;
}

static void free_MySecAttr(MySecurAttrib *pMySA) {
    if(!pMySA)
        return;

    if (pMySA->pEveryoneSID)
        FreeSid(pMySA->pEveryoneSID);
    if (pMySA->pACL)
        LocalFree(pMySA->pACL);
    if (pMySA->pSD)
        LocalFree(pMySA->pSD);
    if (pMySA->pSA)
        delete pMySA->pSA;
    delete pMySA;
}

/*********************************************************************/
/*                 MIDL allocate and free                            */
/*********************************************************************/

void  __RPC_FAR * __RPC_USER midl_user_allocate(size_t len)
{
//	errorLog << "midl_user_allocate() asking for "<<len<<" bytes" << endl;
    return(new uint8_t[len + sizeof(_TCHAR)]);	// +n for null char
}

void __RPC_USER midl_user_free(void __RPC_FAR * ptr)
{
    delete[] ptr;
}

//
// process control
//

// ping function to test RPC server availability
int __stdcall ISPROC_ready(
    /* [in] */ handle_t IDL_handle)
{
#if defined(OSIS_VISTA)
	errorLog << "hardcoded for Vista" << endl;
#endif
	return 0;
}

int __stdcall ISPROC_shutdown(
    /* [in] */ handle_t IDL_handle)
{
	errorLog << vos::datestamp() << "ISPROC_shutdown()" << endl;

	RPC_STATUS status;
    //errorLog << "Calling RpcMgmtStopServerListening" << endl;
    status = RpcMgmtStopServerListening(NULL);
    //errorLog << "RpcMgmtStopServerListening returned: 0x" << hex << status << endl;
    if (status != RPC_S_OK) {
		errorLog << "RpcMgmtStopServerListening returned: 0x" << hex << status << endl;
		cerr << "RpcMgmtStopServerListening returned: 0x" << hex << status << endl;
       //exit(status);
    }

    //errorLog << "Calling RpcServerUnregisterIf" << endl;
    status = RpcServerUnregisterIf(NULL, NULL, FALSE);
    if (status != RPC_S_OK) {
		errorLog << "RpcServerUnregisterIf returned 0x" << hex << status << endl;
		cerr << "RpcServerUnregisterIf returned 0x" << hex << status << endl;
       //exit(status);
    }
	return 0;
}

#if 0
int __stdcall ISPROC_rforkexec(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR app_path,
    /* [in] */ BSTR args,
    /* [out] */ DWORD *pProcID)
{
	_bstr_t bs_app_path(app_path),
		bs_args(args);
	vchar_t *argarr[] = { bs_args, NULL };
	pid_t pid;
	int ec = vos::rfork_execve(bs_app_path, argarr, NULL, pid, elMedium);
	*pProcID = (DWORD) pid;

	// Vista weirdly has an error code here (1816?) when XP doesn't
	return (pid == 0 ? ec : 0);
}
#endif

//
// file access
//

static int makeGameDir_setup()
{
}

static int makeGameDir_Toontown(const vstr_t &deployment)
{
	static const char *ToontownInstallDirSubTree = "Disney\\Disney Online\\Toontown";
	vstr_t toontownInstallDir;
	int error_state = 0;
	vos::sysinfo_t::OSType curr_os = sysinfo_t::get_os_type();

	vstr_t default_dir;
	if (error_state = vos::folder_path(default_dir, vos::fldProgramFiles, FLD_CREATE))
	{
		errorLog << "folder_path() failed: " << vos::last_error_str(error_state) << endl;
		default_dir = "C:\\Program Files";
	}

	toontownInstallDir = default_dir;
	toontownInstallDir += ToontownInstallDirSubTree;
	if (deployment.length())
		toontownInstallDir += deployment;
	vos::dir::normalize(toontownInstallDir);

	// for NT, need to create dir with RW-all attribs
	PSECURITY_ATTRIBUTES pSA = NULL;
	MySecurAttrib *pMySA = NULL;
	if(curr_os >= vos::sysinfo_t::OS_WinNT)
	{
		pMySA = makeGlobalRW_SecAttr();
		if (!pMySA)
		{	// continue, but note the failure in log
			errorLog << datestamp() <<"Failed to make game dir global-writeable. " << vos::last_error_str() << endl;
		}
		else
			pSA = pMySA->pSA;
	}

	error_state = vos::mkdir(toontownInstallDir, pSA);
	if (error_state)
	{
		//LogOSErrorMessage("Error creating Toontown dir");
		//error_state = vos::last_error_code();
		errorLog << datestamp() << "Failed to make game directory. " << vos::last_error_str(error_state) << endl;
	}

	if (pSA != NULL) {
		free_MySecAttr(pMySA);
	}
	return error_state;
}

// internal version of ISFILE_MakeGameDir()
//
static int int_MakeGameDir(const int game, const vstr_t &vsDeployment)
{
	errorLog << "creating game dir with deployment " << vsDeployment << endl;
	bool allowed = false;
	static vchar_t *knownDeployments[] = {
		"_JP", "_BR", "_FR"
	};
	// TODO: make the loop autoconfig based on size of array
	for(size_t i = 0; i < 3; i++)
	{
		if (vsDeployment == knownDeployments[i]) {
			allowed = true;
			break;
		}
	}
	if (allowed)
	{
		switch(game)
		{
		case 0: return makeGameDir_Toontown(vsDeployment); break;
		default:;
		}
	}
	else
		errorLog << "installer_service(MakeGameDir): unrecognized deployment" << endl;
	return -1;
}

// service that should have Windows ADMIN privileges to create the main game directory and make it world writable
//
// returns 0 on success; -1 or error code on failure
//
int __stdcall ISFILE_MakeGameDir(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ int game,
    /* [in] */ BSTR deployment)
{
	vstr_t vsDeployment((vchar_t *) _bstr_t(deployment));
	vos::toupper(vsDeployment);
	return int_MakeGameDir(game, vsDeployment);
}

#if 0
//
// registry access
//
vos::registry system_registry;

int __stdcall ISREG_init(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key)
{
}

void __stdcall ISREG_getstring(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [retval][out] */ BSTR *pVal)
{
}

void __stdcall ISREG_getbin32(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [retval][out] */ int *pVal)
{
}
#endif

// Sets up IE7 protected-mode bypass in the Registry
//
// Service should have Windows ADMIN/HighIntegrity privileges to create the game directory
// in Program Files and make it world writable, besides write into the registry
//
// returns 0 on success; -1 or error code on failure
//
int __stdcall ISREG_DoMediumIntegrity(
    /* [in] */ handle_t IDL_handle,
    /* [in] */ int game,
    /* [in] */ BSTR src_path,
    /* [in] */ BSTR dest_path)
{
	vstr_t reg_key = "SOFTWARE\\Microsoft\\Internet Explorer\\Low Rights\\ElevationPolicy\\",
		app_name;

	_bstr_t bsAppPathSrc(src_path);
	if (bsAppPathSrc.length() > 128 && bsAppPathSrc.length() < 0)
		return -1;		// if string is too long; buffer overflow attempt?

	_bstr_t bsAppPathDest(dest_path);
	if (bsAppPathDest.length() > 128 && bsAppPathDest.length() < 0)
		return -1;		// if string is too long; buffer overflow attempt?

	switch(game)
	{
	case 0:	// toontown
		reg_key += "{e52d0e33-28f4-474f-922f-c2906b4678e5}";	// policy guid
		app_name = "ttinst-helper.exe";
		break;
	default:
		errorLog << vos::datestamp() << "dmi(): not recognized!" << endl;
		return -1;
	}

	// I AM high integrity service

	// move program out of Internet Low security zone to INSTALL_DIR
//	int ec;
	vstr_t appPathSrc(bsAppPathSrc);
	vos::dir::normalize(appPathSrc);
//	vstr_t original = appPathSrc + app_name;

	vstr_t appPathDest(bsAppPathDest);
	vos::dir::normalize(appPathDest);
//	vstr_t dest = appPathDest + app_name;

	if (vos::sysinfo_t::VistaOrBetter())
	{	// setup registry for silent elevate of Installer broker process
		// as per http://msdn2.microsoft.com/en-us/library/Bb250462.aspx#wpm_elebp
		vos::registry elevation_policy;
		vreg_h hReg = elevation_policy.open(HKEY_LOCAL_MACHINE, reg_key.c_str());
		if (hReg)
		{
			// 3 = silent launch protected mode broker as a medium integrity process (process can then use UAC to elevate to high integrity)
			elevation_policy.set_bin32("Policy", 3);
			elevation_policy.set_string("AppName", app_name);
			elevation_policy.set_expand_string("AppPath", "%ProgramFiles%\\Disney\\Disney Online\\Toontown" DEPLOYMENT);
			errorLog << "dmi(): elevation policy updated in registry" << endl;

			VLIBD ief;
			typedef HRESULT (*pIERefreshElevationPolicy)(VOID);
			pIERefreshElevationPolicy fIERefreshElevationPolicy;
			if ( (ief = dlopen(_T("ieframe.dll")))
				&& (fIERefreshElevationPolicy = (pIERefreshElevationPolicy) dlfunc(ief, "IERefreshElevationPolicy")) )
			{
				errorLog << vos::datestamp() << "dmi(): refresh IE = " << (fIERefreshElevationPolicy() == S_OK) << endl;
				return 0;
			}
			else
			{
				errorLog << vos::datestamp() << "dmi(): IE not refreshed for changed policy" << endl;
	#if defined(OSIS_VISTA)
				return 0;
	#endif
			}
		}
		else
			errorLog << vos::datestamp() << "dmi(): couldn't setup broker elevation" << endl;
		return -1;
	}

	return 0;
}
