// standalone.cpp : Defines the entry point for the console application.
//

#include "SAstdafx.h"

#include "vos/vos.hpp"
#include "vos/proc.hpp"
#include "vos/thread.hpp"

#include <Rpc.h>
#include "wdig-installer.h"
#include "service/win32/installer_service.h"

#include "saTT.hpp"
#include "standalone.h"

#include <vos/iut/bootstrap_downloader.hpp>

extern VTHR_RET InstallerStart (voidp_t param);

#if !defined(USE_RPCINSTALLER)
	ofstream errorLog;
	bool errorLog_opened = false;
#endif
saToontownInstaller sa;				// old installer object

using namespace std;
using namespace vos;

#if 0
struct launcherData
{
// parent section
    DWORD ppid;

// child section
    HANDLE hParent;

// shared section
    size_t download_progress;
    size_t test_numbers;
};

HANDLE ghLauncherData;
launcherData *gpLauncherData;

void *createDataShare(HANDLE &hMap, const size_t size)
{
    // this section is basically mmap()
    // TODO: abstract it into vos with a POSIX API
    //
//	SECURITY_DESCRIPTOR sd;
//	InitializeSecurityDescriptor(&sd, SECURITY_DESCRIPTOR_REVISION);
//	SetSecurityDescriptorDacl(&sd, TRUE, 0, FALSE);
    SECURITY_ATTRIBUTES sa =
        { sizeof(SECURITY_ATTRIBUTES),
            NULL, // fill this in for Vista maybe?
            true };
    LPVOID pdata = NULL;

    hMap = CreateFileMapping(INVALID_HANDLE_VALUE,
        &sa, PAGE_READWRITE, 0, size, "tt-installer.share");
    // TODO: round up to a multiple of a 4096 page

    if (hMap != NULL)
    {
        pdata = MapViewOfFile(hMap, FILE_MAP_WRITE, 0, 0, 0);
        if (pdata == NULL) {
            cerr << "createDataShare: Failed to map shared memory because: " << vos::last_error_str() << endl;
            return NULL;
        }
    }
    else
    {
        cerr << "createDataShare: Failed to allocate shared memory because: " << vos::last_error_str() << endl;
        return NULL;
    }
    return pdata;
}

void closeDataShare(HANDLE &hMap, void *p)
{
    UnmapViewOfFile(hMap);
    CloseHandle(p);
}
#endif

#if defined(_DEBUG)
int _tmain(int argc, _TCHAR* argv[], TCHAR* envp[])
#else
int WINAPI _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
#endif
{
	// open the log file
	vstr_t log_dir = vos::tempdir(), logname(APPNAME);
	vos::errorlog_open(log_dir + logname + vos::log_suffix());

	if (vos::sysinfo_t::VistaOrBetter())
	{	// running under Windows Vista
		IntegrityLevel integrity_level = vos::getIntegrityLevel();
		errorLog << "Integrity Level: ";
		switch(integrity_level)
		{
		case vos::il_Low:
			errorLog << "Low";
			break;
		case vos::il_Medium:
			errorLog << "Medium";
			break;
		case vos::il_High:
			errorLog << "High";
			break;
		case vos::il_System:
			errorLog << "System";
			break;
		default:
			errorLog << "Unknown";
		}
		errorLog << endl;
	}
	int status = InstallerStart(NULL);

#if 0
	if (argc == 1)
    {
        // allocate shared memory
        gpLauncherData = (launcherData*) createDataShare(ghLauncherData, sizeof(launcherData));
        if (gpLauncherData != NULL)
        {
            gpLauncherData->ppid = GetCurrentProcessId();

            // spawn child and test shared memory
            char *installer_argv[] = {
                "1",
                NULL,
            };
            pid_t installer_pid = vos::rfork_execve("Debug\\tt-installer.exe", installer_argv);

            while(1)
            {
                errorLog << "parent: " << gpLauncherData->download_progress << endl;
                gpLauncherData->download_progress = (gpLauncherData->download_progress + 1) % 100;
                vos::msleep(1000);
            }
        }
        closeDataShare(ghLauncherData, gpLauncherData);
    }
    else
    {
        ghLauncherData = OpenFileMapping(FILE_MAP_ALL_ACCESS, false, "tt-installer.share");
        gpLauncherData = (launcherData *) MapViewOfFile(ghLauncherData, FILE_MAP_WRITE, 0, 0, 0);

        if (gpLauncherData != NULL)
        {
            gpLauncherData->hParent = OpenProcess(SYNCHRONIZE, false, gpLauncherData->ppid);

            int waitfordebugger = 1;
            while(waitfordebugger)
            {
                vos::msleep(1000);
            }

            // wait for parent process to die
            WaitForSingleObject(gpLauncherData->hParent, INFINITE);

            while(1)
            {
                errorLog << "child: " << gpLauncherData->download_progress << endl;
                vos::msleep(1000);
            }
        }
    }
get_out:
#endif

	return status;
}
