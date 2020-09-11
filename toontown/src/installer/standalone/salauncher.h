#ifndef __SALAUNCHER_H__
#define __SALAUNCHER_H__

//#include "launcherData.hpp"

#define dDEPLOYMENT "US"

#ifdef USE_TESTSERVER
	#define dTTGSVR "https://ttown2.online.disney.com:6667"
	#define dTTACCT "https://ttown2.online.disney.com:1631"
	#define dTTDNLD "http://ttown2.online.disney.com:1620"
	#define dTTVRSN "sv1.0.20.5.test"
#else
	#define dTTGSVR "https://gameserver.toontown.com:6667"
	#define dTTACCT "account.toontown.com"
	#define dTTDNLD "http://download.toontown.com"
	#define dTTVRSN "sv1.0.19.9"
#endif
#define dTTACCTURL "https://"##dTTACCT

#if _MODE_TOONTOWN_
//	extern int launchToontown(launcherData *cb);
#else 
//	extern int launchPirates(launcherData *cb);
#endif

#endif
