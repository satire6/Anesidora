#ifndef __STANDALONE_TOONTOWN_H__
#define __STANDALONE_TOONTOWN_H__

#include "toontownInstaller.h"
//#include "launcherData.hpp"

class saToontownInstaller : public toontownInstaller
{
protected:
	int m_prevState;

public:
  saToontownInstaller() : m_prevState(-1) {}

  int init();

  // expose some of the functions into public for standalone use
  void Deployment(const char *dply) { toontownInstaller::Deployment(dply); };
  void DownloadServer(const char *downloadServer, bool bUpdate = false) {
      toontownInstaller::DownloadServer(downloadServer, bUpdate);
  }
  void DownloadVersion(const char *downloadVersion) { toontownInstaller::DownloadVersion(downloadVersion); }
  void GameServer(const char *gameServer) { toontownInstaller::GameServer(gameServer); }
  void AccountServer(const char *accountServer) { toontownInstaller::AccountServer(accountServer); }

  void game1IsDone() { toontownInstaller::game1IsDone(); }
  void game2IsDone() { toontownInstaller::game2IsDone(); }

  void PlayToken(const char *playToken) { toontownInstaller::PlayToken(playToken); }
  void WebAccountParams(const char *value) { toontownInstaller::WebAccountParams(value); }

  HWND installerHWND() { return toontownInstaller::_installer_hwnd; }

  // new functionality
//  bool do_login(launcherData *const);
//  bool login_error(launcherData *const);

//  int do_standalone(launcherData *const);
};

#endif // _MODE_TOONTOWN_