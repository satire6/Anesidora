// Filename: settingsFile.h
// Created by:  cary (14Dec00)
//
////////////////////////////////////////////////////////////////////

#ifndef __SETTINGSFILE_H__
#define __SETTINGSFILE_H__

#include "dtoolbase.h"
#include "filename.h"

extern const char *configrc_settings_filename;

#define CONFIGRC_MAJOR_VERSION 1
#define CONFIGRC_MINOR_VERSION 7

// this is awful.  We can't include toontownbase.h because it will cause
// a build circularity.  So we have to define EXPCL_TOONTOWN on our own.

#if defined(WIN32_VC) && !defined(CPPPARSER)

#define EXPCL_TOONTOWN __declspec(dllexport)
#define EXPTP_TOONTOWN

#else   /* !WIN32_VC */

#define EXPCL_TOONTOWN
#define EXPTP_TOONTOWN

#endif  /* PENV_WIN32 */

class Settings {
PUBLISHED:
  // The DisplayDriver option is written to the useropt file by value.
  // Don't reorder or remove items from this list, and add all new
  // options to the end, unless you are prepared to remap the old
  // options to the new options based on the useropt file version
  // number.
  enum DisplayDriver { 
    GL, 
    DX7,        // We don't support DX7 any more.  This maps to DX8.
    D_DEFAULT,  // Formerly DX8
    DX9, 
    D_NONE,
    DX8, 
  };
  enum ServerType { PRODUCTION, DEVELOPMENT, DEBUG, S_NONE };

// it would be simpler to just store the actual res sizes, but abstracting them makes
// it harder to crash with a bad resolution
  enum Resolution { R640x480, R800x600, R1024x768, R1280x1024, R1600x1200, R_NONE };

  virtual ~Settings(void);

  static INLINE bool get_sfx(void);
  static INLINE bool get_toon_chat_sounds(void);
  static INLINE bool get_music(void);
  static INLINE bool get_force_sw_midi(void);
  static INLINE bool get_windowed_mode(void);
  static INLINE bool want_chat_log(void);
  static INLINE bool get_show_fpsmeter(void);
  static INLINE bool want_custom_mouse_cursor(void);
  static INLINE float get_sfx_volume(void);
  static INLINE float get_music_volume(void);
  static INLINE DisplayDriver display_driver(void);
  static INLINE Resolution get_resolution(void);
  static INLINE ServerType server_type(void);
  static INLINE bool get_accepting_new_friends(void);
  static INLINE bool get_embedded_mode(void);

  static INLINE void set_sfx(bool);
  static INLINE void set_toon_chat_sounds(bool);
  static INLINE void set_music(bool);
  static INLINE void set_force_sw_midi(bool);
  static INLINE void set_custom_mouse_cursor(bool);
  static INLINE void set_chat_log(bool);
  static INLINE void set_windowed_mode(bool);
  static INLINE void set_sfx_volume(float);
  static INLINE void set_music_volume(float);
  static INLINE void set_display_driver(DisplayDriver);
  static INLINE void set_resolution(Resolution);
  static void set_resolution_dimensions(unsigned int xsize,unsigned int ysize);
  static INLINE void set_server_type(ServerType);
  static INLINE void set_accepting_new_friends(bool);
  static INLINE void set_embedded_mode(bool);

  static INLINE void set_show_fpsmeter(bool);
  static INLINE bool doSavedSettingsExist(void);  // does the saved settings file exist?
  static INLINE void write_settings(void);
  static INLINE void read_settings(void);
public:
  static string get_config_path(void);
  static void   get_resolution_sizes(Resolution r, unsigned int &xsize,unsigned int &ysize);
private:
  Settings(void);

  static INLINE Settings* get_ptr(void);

  INLINE bool ns_doSavedSettingsExist(void);
  INLINE bool ns_get_sfx(void);
  INLINE bool ns_get_toon_chat_sounds(void);
  INLINE bool ns_get_music(void);
  INLINE bool ns_get_force_sw_midi(void);
  INLINE bool ns_get_windowed_mode(void);
  INLINE bool ns_get_show_fpsmeter(void);
  INLINE bool ns_want_chat_log(void);
  INLINE bool ns_want_custom_mouse_cursor(void);
  INLINE float ns_get_sfx_volume(void);
  INLINE float ns_get_music_volume(void);
  INLINE DisplayDriver ns_display_driver(void);
  INLINE Resolution ns_get_resolution(void);
  INLINE ServerType ns_server_type(void);
  INLINE bool ns_get_accepting_new_friends(void);
  INLINE bool ns_get_embedded_mode(void);

  INLINE void ns_set_show_fpsmeter(bool);
  INLINE void ns_set_sfx(bool);
  INLINE void ns_set_toon_chat_sounds(bool);
  INLINE void ns_set_music(bool);
  INLINE void ns_set_custom_mouse_cursor(bool);
  INLINE void ns_set_chat_log(bool);
  INLINE void ns_set_force_sw_midi(bool);
  INLINE void ns_set_windowed_mode(bool);
  INLINE void ns_set_sfx_volume(float);
  INLINE void ns_set_music_volume(float);
  INLINE void ns_set_display_driver(DisplayDriver);
  INLINE void ns_set_resolution(Resolution);
  INLINE void ns_set_server_type(ServerType);
  INLINE void ns_set_accepting_new_friends(bool);
  INLINE void ns_set_embedded_mode(bool);
  void ns_write_settings(void);
  void ns_read_settings(void);
  void read_file(Filename);

  static Settings* _singleton;

  // actual state data
  Filename _fname;
  bool _sfx;
  bool _toon_chat_sounds;
  bool _music;
  bool _bForceSWMidi;
  bool _custom_mousecursor_enabled;
  bool _chat;
  bool _bReadSavedData;
  bool _bUseWindowedMode;
  bool _bShowFpsMeter;
  bool _accepting_new_friends;
  bool _embedded_mode;
  float _sfx_vol;
  float _music_vol;
  DisplayDriver _driver;
  Resolution _res;
  ServerType _stype;
};

#include "settingsFile.I"

#endif /* __SETTINGSFILE_H__ */
