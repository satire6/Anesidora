#include "SAstdafx.h"
#include "saTT.hpp"

#include "salauncher.h"
#include "installerHTTP.h"
//#include <boost/regex.hpp>				// regular expression support

int saToontownInstaller::init()
{
	toontownInstaller::init();

// setup environmental settings
//	Deployment(dDEPLOYMENT);
//	DownloadServer(dTTDNLD, true);
//	DownloadVersion(dTTVRSN);
//	GameServer(dTTGSVR);
//	AccountServer(dTTACCTURL);

	// no flash movies but Toontown checks for these
//	game1IsDone();
//	game2IsDone();

// web login settings
//	PlayToken(dPLAYTOKEN);
//	WebAccountParams("secretsNeedsParentPassword=1&chatEligible=1");

	return 0;
}

/*
#define INSTALL_STATES	11
#define IPROGRESS(x)	((100/INSTALL_STATES) * x)

int saToontownInstaller::do_standalone(launcherData *const pldat)
{
// spin-poll "launcher" like the webcode
	int cstate, value = 0;
	string msg;
	bool gameExit = false;
//	while((cstate = statecode()) <= 120 || !gameError)		// exit  at state 120
	while(!gameExit)
	{
		cstate = statecode();
	    runInstaller();
		if (cstate != m_prevState)
		{
			switch (cstate) {
			case 0:						// :1 initialization
				pldat->status_text("Initializing");
				value = IPROGRESS(1); break;
			case 10:					// :2 check for launcher
				pldat->status_text("Checking for Launcher");
				value = IPROGRESS(2); break;
			case 13:
				pldat->status_text("Error while trying to Launch");
				value = IPROGRESS(0); break;
				gameExit = true;
				break;
			case 23:					// :3
//				pldat->text = "";
				value = IPROGRESS(3); break;
			case 53:					// :5 download launcher
				pldat->status_text("Downloading Launcher");
				value = IPROGRESS(4); break;
			case 55:					// :6
//				pldat->status_text("Downloading Launcher");
				value = IPROGRESS(5); break;
			case 60:					// :7
//				pldat->status_text("Downloading Launcher");
				value = IPROGRESS(6); break;
			case 25:					// :4 launcher valid?
//				pldat->status_text("");
				value = IPROGRESS(7); break;
			case 85:					// :8 patch launcher
				pldat->status_text("Patching Launcher");
				value = IPROGRESS(8); break;
			case 97:					// :9 run launcher
				pldat->status_text("Running Launcher");
				value = IPROGRESS(9); break;
			case 110:					// :10 wait on launcher
				value = IPROGRESS(10);
				SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_LOWEST);
				break;
			case 115:					// :11 waiting on game window to open
				pldat->status_text("Waiting on Launcher");
				value = IPROGRESS(11); break;
			case 120:					// :12 panda window up
				value = 100;
				break;
			case 130:					// game is running
				pldat->status_text("");
				value = 0;				// reset progress bar to 0
				break;
			case 140:
				gameExit = true;
				// Open a browser
				ShellExecute(pldat->_hwnd, _T("open"), "https://account.toontown.com/thanksForPlaying.php", NULL, NULL, SW_SHOWNORMAL);
				break;					// game ended
			}
			m_prevState = cstate;			// save it for next trigger

			pldat->_completion = value;
			pldat->update_progress(pldat);	// callback gui to update progress
		}
		if (cstate <= 100)
			Sleep(200);
		else
			Sleep(500);						// slower poll during app launch
	}

	SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_NORMAL);
	return 0;
}*/
