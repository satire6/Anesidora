
inline void toontownInstaller::
addUserError(char *error) {
  addUserError((const char *)error);
}

////////////////////////////////////////////////////////////////////
// called when game1 has finished
inline void toontownInstaller::
game1IsDone() {
  _game1_Done = 1;
}

// called when game2 has finished
inline void toontownInstaller::
game2IsDone() {
  _regToontown.setDWORD(_GAME2_DONE_ValueName, 1);
}

inline size_t toontownInstaller::
statecode() {
  return _StateCode;
}

// call to get the current "percent loaded" value
inline long toontownInstaller::
getPercentLoaded() {
  return (long) _regToontown.getDWORD(_PERCENT_LOADED_ValueName);
}

inline void toontownInstaller::
initOverallPercentLoaded()
{
  if(_regToontown.setDWORD(_PERCENT_OVERALL_LOADED_ValueName, 0))
    errorLog << "couldn't set overall percent key in registry!\n";
}

// call to get the current "overall percent loaded" value
inline long toontownInstaller::
getOverallPercentLoaded() {
  return (long) _regToontown.getDWORD(_PERCENT_OVERALL_LOADED_ValueName);
}

// call to get the current "launcher message" value
inline string toontownInstaller::
getLauncherMessage() {
  return _regToontown.getString(_LAUNCHER_MESSAGE_ValueName);
}

#ifndef _standalone_
inline string toontownInstaller::
getGame1Filename() {
  char url[_MAX_PATH];
  convertFullFilenameToURL(_game1_IFilename.getFullLocalName(), url);
  return string(url);
}

inline string toontownInstaller::
getMovieFilename() {
  char url[_MAX_PATH];
  convertFullFilenameToURL(_movie_IFilename.getFullLocalName(), url);
  return string(url);
}

inline string toontownInstaller::
getGame2Filename() {
  char url[_MAX_PATH];
  convertFullFilenameToURL(_game2_IFilename.getFullLocalName(), url);
  return string(url);
}

inline string toontownInstaller::
getMessagesFilename() {
  char url[_MAX_PATH];
  convertFullFilenameToURL(_messages_IFilename.getFullLocalName(), url);
  return string(url);
}

// returns 0 if game2 is not done
inline int toontownInstaller::
game2Done()
{
  DWORD game2Done;
  // return zero if value is not in reg
  return (!_regToontown.getDWORD(_GAME2_DONE_ValueName, game2Done));
}
#endif

// this function receives the go.com 'green' user-info data chunk
// and writes it into the registry for the launcher to pick up
inline void toontownInstaller::setGreen(const char *green) {
  _regToontown.setString(_GREEN_ValueName, green);
}

// this function receives the 'blue' user-info data chunk
// and writes it into the registry for the launcher to pick up
inline void toontownInstaller::setBlue(const char *blue) {
  _regToontown.setString(_BLUE_ValueName, blue);
}

// this function receives the account.toontown.com 'PlayToken'
// user-info data chunk and writes it into the registry for the
// launcher to pick up
inline void toontownInstaller::PlayToken(const char *playToken) {
  _regToontown.setString(_PLAYTOKEN_ValueName, playToken);
}

// this function receives the account.toontown.com user name
// and writes it into the registry.
inline void toontownInstaller::setLastLogin(const char *userName) {
  _regToontown.setString(_LAST_LOGIN_ValueName, userName);
}



#ifndef _standalone_
inline void toontownInstaller::
setGame1Version(const char *ver) {
  setFlashMovieVersion(ver, _game1Version, "game1");
}

inline void toontownInstaller::
setMovieVersion(const char *ver) {
  setFlashMovieVersion(ver, _movieVersion, "movie");
}

inline void toontownInstaller::
setGame2Version(const char *ver) {
  setFlashMovieVersion(ver, _game2Version, "game2");
}

inline void toontownInstaller::
setMessagesVersion(const char *ver) {
  setFlashMovieVersion(ver, _messagesVersion, "messages");
}

inline void toontownInstaller::
setToontuneVersion(const char *ver) {
  setFlashMovieVersion(ver, _toontuneVersion, "toontune");
}

inline void toontownInstaller::
setLauncherMessage(const char *msg) {
  _regToontown.setString(_LAUNCHER_MESSAGE_ValueName, msg);
}
#endif

// returns 0 if launcher did not exit prematurely
inline int toontownInstaller::
launcherExitedPrematurely() {
  if (_hLauncherProcess && (!processActive(_hLauncherProcess)) && (!pandaWindowOpen()))
    return 1;

  return 0;
}

// returns 0 if launcher is not alive
inline int toontownInstaller::
launcherAlive(DWORD &exitCode) {
  if (_hLauncherProcess && processActive(_hLauncherProcess,exitCode))
      return 1;

  return 0;
}
// set the registry to prevent hack
inline void toontownInstaller::
setPreventHack(DWORD value)
{
  if(_regHackers.setDWORD(_PREVENT_HACKERS_ValueName, value))
    errorLog << "couldn't set prevent hackers in registry!\n";
}
// set the registry to prevent hack
inline void toontownInstaller::
setPreventHack2(const char *value)
{
  if(_regHackers.setString(_PREVENT_HACKERS_ValueName2, value))
    errorLog << "couldn't set prevent hackers 2 in registry!\n";
}
// set the registry to chat eligible // deprecated
inline void toontownInstaller::
setChatEligible(DWORD value)
{
  if(_regToontown.setDWORD(_CHAT_ELIGIBLE_ValueName, value))
    errorLog << "couldn't set parent password key to enable chat eligible registry!\n";
}
// set the registry to chat related params
inline void toontownInstaller::
WebAccountParams(const char *value)
{
  if(_regToontown.setString(_WEB_ACCT_PARAMS_ValueName, value))
    errorLog << "couldn't set web account parameters key to enable chat registry!\n";
}
inline DWORD toontownInstaller::
getPreventHack() {
  return _regHackers.getDWORD(_PREVENT_HACKERS_ValueName);
}
inline string toontownInstaller::
getPreventHack2() {
  return _regHackers.getString(_PREVENT_HACKERS_ValueName2);
}
// country deployed to
inline string toontownInstaller::
Deployment()
{
  string deployment;
  if (_regToontown.getString(_DEPLOYMENT_ValueName, deployment))
    deployment = "US";				// default to US if none set
  return deployment;
}
inline void toontownInstaller::
Deployment(const char *deployment) {
  _regToontown.setString(_DEPLOYMENT_ValueName, deployment);
}
