// Filename: settingsFile.I
// Created by:  cary (14Dec00)
//
////////////////////////////////////////////////////////////////////

INLINE bool Settings::get_sfx(void) {
  return get_ptr()->ns_get_sfx();
}

INLINE bool Settings::get_toon_chat_sounds(void) {
  return get_ptr()->ns_get_toon_chat_sounds();
}

INLINE bool Settings::get_music(void) {
  return get_ptr()->ns_get_music();
}

INLINE bool Settings::get_force_sw_midi(void) {
  return get_ptr()->ns_get_force_sw_midi();
}

INLINE bool Settings::want_chat_log(void) {
  return get_ptr()->ns_want_chat_log();
}

INLINE bool Settings::get_windowed_mode(void) {
  return get_ptr()->ns_get_windowed_mode();
}

INLINE bool Settings::get_show_fpsmeter(void) {
  return get_ptr()->ns_get_show_fpsmeter();
}

INLINE bool Settings::want_custom_mouse_cursor(void) {
  return get_ptr()->ns_want_custom_mouse_cursor();
}

INLINE float Settings::get_sfx_volume(void) {
  return get_ptr()->ns_get_sfx_volume();
}

INLINE float Settings::get_music_volume(void) {
  return get_ptr()->ns_get_music_volume();
}

INLINE Settings::DisplayDriver Settings::display_driver(void) {
  return get_ptr()->ns_display_driver();
}

INLINE Settings::Resolution Settings::get_resolution(void) {
  return get_ptr()->ns_get_resolution();
}

INLINE Settings::ServerType Settings::server_type(void) {
  return get_ptr()->ns_server_type();
}

INLINE bool Settings::get_accepting_new_friends(void) {
  return get_ptr()->ns_get_accepting_new_friends();
}

INLINE bool Settings::get_embedded_mode(void) {
  return get_ptr()->ns_get_embedded_mode();
}

INLINE void Settings::set_sfx(bool active) {
  get_ptr()->ns_set_sfx(active);
}

INLINE void Settings::set_toon_chat_sounds(bool active) {
  get_ptr()->ns_set_toon_chat_sounds(active);
}

INLINE void Settings::set_windowed_mode(bool bUseWindowedMode) {
  get_ptr()->ns_set_windowed_mode(bUseWindowedMode);
}

INLINE void Settings::set_music(bool active) {
  get_ptr()->ns_set_music(active);
}

INLINE void Settings::set_force_sw_midi(bool bForceSWMidi) {
  get_ptr()->ns_set_force_sw_midi(bForceSWMidi);
}

INLINE void Settings::set_show_fpsmeter(bool bShowFpsMeter) {
  get_ptr()->ns_set_show_fpsmeter(bShowFpsMeter);
}

INLINE void Settings::set_chat_log(bool active) {
  get_ptr()->ns_set_chat_log(active);
}

INLINE void Settings::set_custom_mouse_cursor(bool cursor_enabled) {
  get_ptr()->ns_set_custom_mouse_cursor(cursor_enabled);
}

INLINE void Settings::set_sfx_volume(float vol) {
  get_ptr()->ns_set_sfx_volume(vol);
}

INLINE void Settings::set_music_volume(float vol) {
  get_ptr()->ns_set_music_volume(vol);
}

INLINE void Settings::set_display_driver(Settings::DisplayDriver driver) {
  get_ptr()->ns_set_display_driver(driver);
}

INLINE void Settings::set_resolution(Settings::Resolution res) {
  get_ptr()->ns_set_resolution(res);
}

INLINE void Settings::set_server_type(Settings::ServerType serve) {
  get_ptr()->ns_set_server_type(serve);
}

INLINE void Settings::set_accepting_new_friends(bool afr) {
  get_ptr()->ns_set_accepting_new_friends(afr);
}

INLINE void Settings::set_embedded_mode(bool afr) {
  get_ptr()->ns_set_embedded_mode(afr);
}

INLINE void Settings::write_settings(void) {
  get_ptr()->ns_write_settings();
}

INLINE void Settings::read_settings(void) {
  get_ptr()->ns_read_settings();
}

INLINE bool Settings::ns_doSavedSettingsExist(void) {
  // does the saved settings file exist?
  return _bReadSavedData;
}

INLINE bool Settings::doSavedSettingsExist(void) {
  return get_ptr()->ns_doSavedSettingsExist();
}

INLINE Settings* Settings::get_ptr(void) {
  if (_singleton == (Settings*)0L)
    _singleton = new Settings;
  return _singleton;
}

INLINE bool Settings::ns_get_sfx(void) {
  return _sfx;
}

INLINE bool Settings::ns_get_toon_chat_sounds(void) {
  return _toon_chat_sounds;
}

INLINE bool Settings::ns_get_music(void) {
  return _music;
}

INLINE bool Settings::ns_get_force_sw_midi(void) {
  return _bForceSWMidi;
}

INLINE bool Settings::ns_get_windowed_mode(void) {
  return _bUseWindowedMode;
}

INLINE bool Settings::ns_get_show_fpsmeter(void) {
  return _bShowFpsMeter;
}

INLINE bool Settings::ns_want_chat_log(void) {
  return _chat;
}

INLINE bool Settings::ns_want_custom_mouse_cursor(void) {
  return _custom_mousecursor_enabled;
}

INLINE float Settings::ns_get_sfx_volume(void) {
  return _sfx_vol;
}

INLINE float Settings::ns_get_music_volume(void) {
  return _music_vol;
}

INLINE Settings::DisplayDriver Settings::ns_display_driver(void) {
  return _driver;
}

INLINE Settings::Resolution Settings::ns_get_resolution(void) {
  return _res;
}

INLINE Settings::ServerType Settings::ns_server_type(void) {
  return _stype;
}

INLINE bool Settings::ns_get_accepting_new_friends(void) {
  return _accepting_new_friends;
}

INLINE bool Settings::ns_get_embedded_mode(void) {
  return _embedded_mode;
}

INLINE void Settings::ns_set_sfx(bool active) {
  _sfx = active;
}

INLINE void Settings::ns_set_toon_chat_sounds(bool active) {
  _toon_chat_sounds = active;
}

INLINE void Settings::ns_set_windowed_mode(bool bUseWindowedMode) {
  _bUseWindowedMode = bUseWindowedMode;
}

INLINE void Settings::ns_set_music(bool active) {
  _music = active;
}

INLINE void Settings::ns_set_force_sw_midi(bool bForceSWMidi) {
  _bForceSWMidi = bForceSWMidi;
}

INLINE void Settings::ns_set_show_fpsmeter(bool bShowFpsMeter) {
  _bShowFpsMeter = bShowFpsMeter;
}

INLINE void Settings::ns_set_chat_log(bool active) {
  _chat = active;
}

INLINE void Settings::ns_set_custom_mouse_cursor(bool cursor_enabled) {
  _custom_mousecursor_enabled = cursor_enabled;
}

INLINE void Settings::ns_set_sfx_volume(float vol) {
  _sfx_vol = vol;
}

INLINE void Settings::ns_set_music_volume(float vol) {
  _music_vol = vol;
}

INLINE void Settings::ns_set_display_driver(Settings::DisplayDriver driver) {
  _driver = driver;
}

INLINE void Settings::ns_set_resolution(Settings::Resolution res) {
  _res = res;
}

INLINE void Settings::ns_set_server_type(Settings::ServerType stype) {
  _stype = stype;
}

INLINE void Settings::ns_set_accepting_new_friends(bool afr) {
  _accepting_new_friends = afr;
}

INLINE void Settings::ns_set_embedded_mode(bool afr) {
  _embedded_mode = afr;
}
