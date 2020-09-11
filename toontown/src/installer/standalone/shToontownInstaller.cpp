//#include "SAstdafx.h"
#include "vos/vos.hpp"

#include "shToontownInstaller.hpp"

//
// Installer Shell customization
//
extern const vchar_t *ToontownRegKeyName;
extern const vchar_t *ToontownInstallDirSubTree;
extern const vchar_t *TOONTOWN_INSTALLER_LOGBASENAME;

using namespace vos;

ToontownInstaller::ToontownInstaller()
{
	RegistryData::set_rootkey(ToontownRegKeyName);			// set the base registry key
    GamelogName(TOONTOWN_INSTALLER_LOGBASENAME);

	// stuff that should be set runtime
//	DownloadServer("http://ttown2.online.disney.com:2421/");
//	DownloadServer("http://ttown2.online.disney.com:2421/", true);
//	DownloadVersion("portuguese/currentVersion/");
	InstallPath(ToontownInstallDirSubTree);					// set the install directory subtree

	// sync settings with system registry
	RegistryData::sync(*this);
}
