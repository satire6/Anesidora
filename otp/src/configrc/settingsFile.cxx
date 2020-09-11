// Filename: settingsFile.cxx
// Created by:  cary (14Dec00)
//
////////////////////////////////////////////////////////////////////

#include "settingsFile.h"
#include "dSearchPath.h"
#include "executionEnvironment.h"
#include "serialization.h"

const char *configrc_settings_filename = "useropt";
const char *configrc_debug_filename = "readlog.txt";
Settings* Settings::_singleton = (Settings*)0L;

Settings::~Settings(void) {
  _singleton = (Settings*)0L;
}

static void CropString(string& S) {
  size_t i = S.find_first_not_of(" \t\r\f\n");
  if (i != string::npos) {
    size_t j = S.find_last_not_of(" \t\r\f\n");
    if (j != string::npos)
      S = S.substr(i, j-i+1);
    else
      S = S.substr(i, string::npos);
  } else
    S.erase(0, string::npos);
}

string Settings::get_config_path(void) {
  // this code is lifted from configTable.cxx.  But since this code cannot
  // use config in any way (otherwise it might recurse), we have to dup the
  // logic here.
  static string ret = "";  // lets please only do this once

  if (!(ret.empty()))
    return ret;

  // ok, this'll be fun.  Start by processing the CONFIG_CONFIG environment
  bool cpth = false;
  string cpath;
  string cc = ExecutionEnvironment::get_environment_variable("CONFIG_CONFIG");
  if ((!cc.empty()) && (cc.length() > 1)) {
    string configconfig(cc);
    string assign = "=";
    string sep = configconfig.substr(0, 1);
    typedef pvector<string> strvec;
    typedef Serialize::Deserializer<strvec, Serialize::StdExt<string> > deser;
    configconfig.erase(0, 1);
    deser ds(configconfig, sep);
    strvec sv = ds;
    for (strvec::iterator i=sv.begin(); i!=sv.end(); ++i) {
      if ((*i).length() == 1) {
        // new assignment character
        assign += *i;
        continue;
      }
      size_t j = (*i).find_first_of(assign);
      if (j != string::npos) {
        string tok = (*i).substr(0, j);
        string rest = (*i).substr(j+1, string::npos);
        if (tok == "configpath") {
          if (cpth)
            cpath += " " + rest;
          else
            cpath = rest;
          cpth = true;
        }
      }
    } // for
  }
  if (!cpth) {
    // nothing in CONFIG_CONFIG, pull a default
#ifdef PENV_PS2
    cpath = "";
#else /* PENV_PS2 */
    cpath = "CONFIG_PATH";
#endif /* PENV_PS2 */
  }
  if (cpath.empty()) {
#ifdef PENV_PS2
#ifndef CONFIG_PATH
#define CONFIG_PATH "."
#endif /* CONFIG_PATH */
    cpath = CONFIG_PATH;
#else /* PENV_PS2 */
    cpath = ".";
#endif /* PENV_PS2 */
  } else {
    string S;
    while (!cpath.empty()) {
      int i = cpath.find_first_of(" ");
      string stmp = cpath.substr(0, i);
      if (ExecutionEnvironment::has_environment_variable(stmp)) {
        S += " ";
        S += ExecutionEnvironment::get_environment_variable(stmp);
      }
      cpath.erase(0, i);
      CropString(cpath);
    }
    if (S.empty())
      S = ".";
    CropString(S);
    cpath = S;
  }
  ret = cpath;
  return ret;
}

Settings::Settings(void) {
  string path = get_config_path();
  DSearchPath setting_search(path);
  DSearchPath::Results setting_files;

  setting_search.find_all_files(configrc_settings_filename, setting_files);
  int n = setting_files.get_num_files();
  if (n != 0) {
    for (int i=n-1; i>=0; --i) {
      Filename setting_file = setting_files.get_file(i);
      setting_file.set_binary();
      read_file(setting_file);
    }
    _bReadSavedData=true;
  } else {
    // no settings file
#if 0
    // This is silly.  Just put it in the current directory.
    string foo = setting_search.get_directory(0).c_str();
    foo += "/";
    foo += configrc_settings_filename;
    _fname = foo;
#else
    _fname = configrc_settings_filename;
#endif
    _fname.set_binary();
    _sfx = true;
    _music = true;
    _chat = true;
    _sfx_vol = 1.0f;
    _music_vol = 1.0f;
    _driver = D_DEFAULT;
    _res = R800x600;
    _stype = PRODUCTION;
    _bUseWindowedMode=true;
    _bShowFpsMeter=false;
    _bReadSavedData=false;
    _custom_mousecursor_enabled = true;
    _accepting_new_friends = true;
    _embedded_mode=false;
  }
}

inline void write_nibble(ostream& os, unsigned char n) {
  switch (n) {
  case 0:
    cerr << "0";
    break;
  case 1:
    cerr << "1";
    break;
  case 2:
    cerr << "2";
    break;
  case 3:
    cerr << "3";
    break;
  case 4:
    cerr << "4";
    break;
  case 5:
    cerr << "5";
    break;
  case 6:
    cerr << "6";
    break;
  case 7:
    cerr << "7";
    break;
  case 8:
    cerr << "8";
    break;
  case 9:
    cerr << "9";
    break;
  case 10:
    cerr << "A";
    break;
  case 11:
    cerr << "B";
    break;
  case 12:
    cerr << "C";
    break;
  case 13:
    cerr << "D";
    break;
  case 14:
    cerr << "E";
    break;
  case 15:
    cerr << "F";
    break;
  default:
    cerr << "*";
    break;
  }
}

inline void write_byte(ostream& os, unsigned char b) {
  unsigned char b1 = (b >> 4);
  unsigned char b2 = (b & 0x0f);
  write_nibble(os, b1);
  write_nibble(os, b2);
}

void Settings::ns_write_settings(void) {
  pofstream ofs;
    
  string path = get_config_path();
  DSearchPath setting_search(path);
  string dir = setting_search.get_directory(0);
  Filename f2 = dir + "/" + configrc_settings_filename;
  f2.set_binary();

  //cerr << "Settings Path " << configrc_settings_filename << " " << _fname << endl;
  int canWrite = 0;

  if (f2.open_write(ofs)) {
      canWrite = 1;
  }
  else{
    if (_fname.open_write(ofs)) {
        canWrite = 1;
    }
  }
  if (canWrite == 0){
      cerr << "could not open '" << _fname << "' or '" << f2 << "' for writing"
           << endl;
      return;
  }
  // to add new fields, increment version number, write backward-compatible read_settings (so field
  // is set to suitable default for all version #'s and field is not read off disk if version too old),
  // and add new fields to write_settings

  // header
  ofs << "UserSettings";
  //  cerr << "wrote 'UserSettings'" << endl;
  // major version
  ofs << (unsigned char)CONFIGRC_MAJOR_VERSION;
  //  cerr << "wrote 0x01" << endl;
  // minor version
  ofs << (unsigned char)CONFIGRC_MINOR_VERSION;
  //  cerr << "wrote 0x00" << endl;
  // data
  ofs << (_sfx?((unsigned char)1):((unsigned char)0)) ;
  //  cerr << "wrote 0x" << (_sfx?"01":"00") << endl;
  ofs << (_music?((unsigned char)1):((unsigned char)0)) ;
  //  cerr << "wrote 0x" << (_music?"01":"00") << endl;
  ofs << (_chat?((unsigned char)1):((unsigned char)0)) ;
  //  cerr << "wrote 0x" << (_chat?"01":"00") << endl;
  unsigned char* b;
  float ftmp = _sfx_vol;
  unsigned int cnt = sizeof(float);
  //  cerr << "wrote 0x";
  for (unsigned int i=0; i<cnt; ++i) {
    b = (unsigned char*)(&ftmp);
    b += i;
    ofs << (unsigned char)(*b);
    //    write_byte(cerr, *b);
  }
  //  cerr << endl;
  ftmp = _music_vol;
  //  cerr << "wrote 0x";
  for (unsigned int j=0; j<cnt; ++j) {
    b = (unsigned char*)(&ftmp);
    b += j;
    ofs << (unsigned char)(*b);
    //    write_byte(cerr, *b);
  }
  //  cerr << endl;
  ofs << (unsigned char)_driver;
  //  cerr << "wrote 0x";
  //  write_byte(cerr, (unsigned char)_driver);
  //  cerr << endl;
  ofs << (unsigned char)_res;
  //  cerr << "wrote 0x";
  //  write_byte(cerr, (unsigned char)_res);
  //  cerr << endl;
  ofs << (unsigned char)_stype;
  //  cerr << "wrote 0x";
  //  write_byte(cerr, (unsigned char)_stype);
  //  cerr << endl;

  ofs << (unsigned char)_custom_mousecursor_enabled;
  ofs << (unsigned char)_bUseWindowedMode;
  ofs << (unsigned char)_bShowFpsMeter;
  ofs << (unsigned char)_bForceSWMidi;
  ofs << (unsigned char)_toon_chat_sounds;
  ofs << (unsigned char)_accepting_new_friends;
  ofs << (unsigned char)_embedded_mode;
}


void Settings::ns_read_settings(void) {
    Filename userSettings = configrc_settings_filename;
    userSettings.set_binary(); 
    read_file(userSettings);
}

void Settings::read_file(Filename fname) {
  pifstream ifs;
  pofstream ofs;
  Filename outname = configrc_debug_filename;
  outname.set_binary();
    
  if (outname.open_write(ofs))
  {
      ofs << "Trying to read standard file: " << fname << endl;
  }

  int readOkay = 0;
  //  cerr << "*** in read_file ***" << endl;
  if (fname.open_read(ifs)){
      readOkay = 1;
      ofs << "opened standard file for reading: " << fname << endl;
  }
  else
  {
    string path = get_config_path();
    DSearchPath setting_search(path);
    string dir = setting_search.get_directory(0);
    Filename f2 = dir + "/" + configrc_settings_filename;
    cerr << "f2 = " << f2 << "\n";
    f2.set_binary();
    ofs << "Trying to read auxiliary file: " << f2 << endl;
    if (f2.open_read(ifs)){
        readOkay = 1;
        ofs << "opened auxiliary file for reading: " << fname << endl;
    }
    else
    {
        ofs << "no file could be read" << endl;
    }
      
  }
  if (readOkay == 1)   {
    unsigned char b;
    string header;
    int i;
    

    _fname = fname;
    for (i=0; i<12; ++i) {
      ifs >> b;
      header += b;
    }
    if (!(header == "UserSettings")) {
      // set some defaults, most of these will generate error messages in the
      // output
      //      cerr << "header ('" << header << "') != 'User Settings'" << endl;
      ofs << "Invalid Header: " << header << endl;
      _sfx = true;
      _music = true;
      _chat = true;
      _sfx_vol = 1.0f;
      _music_vol = 1.0f;
      _driver = D_NONE;
      _res = R_NONE;
      _stype = S_NONE;
      return;
    }
    //    cerr << "read '" << header << "'" << endl;
    int major, minor;
    ifs >> b;
    //    cerr << "read 0x";
    //    write_byte(cerr, b);
    //    cerr << endl;
    major = b;
    ofs << "major: " << major << endl;
    ifs >> b;
    //    cerr << "read 0x";
    //    write_byte(cerr, b);
    //    cerr << endl;
    minor = b;
    ofs << "minor: " << major << endl;
    switch (major) {
        case 0:
          ofs << "case 0" << endl;
          ifs >> b;
          _sfx = _music = (b != 0);
          ofs << "_sfx: " << _sfx << endl;
          ifs >> b;
          _driver = (DisplayDriver)b;
          ofs << "_driver: " << _driver << endl;
          ifs >> b;
          _res = (Resolution)b;
          ofs << "_res: " << _res << endl;
          ifs >> b;
          _stype = (ServerType)b;
          ofs << "_stype: " << _stype << endl;
          // things not covered in this version
          _sfx_vol = _music_vol = 1.0f;
          ofs << "_sfx_vol: " << _sfx_vol << endl;
          _chat = true;
          _custom_mousecursor_enabled = true;

          break;
        case 1:
          ofs << "case 1" << endl;
          ifs >> b;
          //      cerr << "read 0x";
          //      write_byte(cerr, b);
          //      cerr << endl;
          _sfx = (b != 0);
          ofs << "_sfx: " << _sfx << endl;
          ifs >> b;
          //      cerr << "read 0x";
          //      write_byte(cerr, b);
          //      cerr << endl;
          _music = (b != 0);
          ofs << "_music: " << _music << endl;
          ifs >> b;
          //      cerr << "read 0x";
          //      write_byte(cerr, b);
          //      cerr << endl;
          _chat = (b != 0);
          ofs << "_chat: " << _chat << endl;
          {
            float ftmp = 0.0f;
            unsigned int cnt = sizeof(float);
            //      cerr << "read 0x";
            for (unsigned int i=0; i<cnt; ++i) {
              ifs >> b;
              //      write_byte(cerr, b);
              unsigned char* a = (unsigned char*)(&ftmp);
              a += i;
              *a = b;
            }
            //      cerr << endl;
            _sfx_vol = ftmp;
            ofs << "_sfx_vol: " << _sfx_vol << endl;
            ftmp = 0.0f;
            //      cerr << "read 0x";
            for (unsigned int j=0; j<cnt; ++j) {
              ifs >> b;
              //      write_byte(cerr, b);
              unsigned char* a = (unsigned char*)(&ftmp);
              a += j;
              *a = b;
            }
            //      cerr << endl;
            _music_vol = ftmp;
            ofs << "_music_vol: " << _music_vol << endl;
          }
      ifs >> b;
      //      cerr << "read 0x";
      //      write_byte(cerr, b);
      //      cerr << endl;
      _driver = (DisplayDriver)b;
      ofs << "_driver: " << _driver << endl;
      ifs >> b;
      //      cerr << "read 0x";
      //      write_byte(cerr, b);
      //      cerr << endl;
      _res = (Resolution)b;
      ofs << "_res: " << _res << endl;    
      ifs >> b;
      //      cerr << "read 0x";
      //      write_byte(cerr, b);
      //      cerr << endl;
      _stype = (ServerType)b;
      ofs << "_stype: " << _stype << endl;    

      if(minor>=1) {
          ifs >> b;
          _custom_mousecursor_enabled = (b!=false);
      } else _custom_mousecursor_enabled = true;
      ofs << "_custom_mousecursor_enabled: " << _custom_mousecursor_enabled << endl;

      if(minor>=2) {
          ifs >> b;
          _bUseWindowedMode = (b!=false);
      } else _bUseWindowedMode = false;
      ofs << "_bUseWindowedMode: " << _bUseWindowedMode << endl;

      if(minor>=3) {
          ifs >> b;
          _bShowFpsMeter = (b!=false);
      } else _bShowFpsMeter = false;
      ofs << "_bShowFpsMeter: " << _bShowFpsMeter << endl;

      if(minor>=4) {
          ifs >> b;
          _bForceSWMidi = (b!=false);
      } else _bForceSWMidi = true;
      ofs << "_bForceSWMidi: " << _bForceSWMidi << endl;
      if(minor>=5) {
          ifs >> b;
          _toon_chat_sounds = (b!=false);
      } else _toon_chat_sounds = true;
      ofs << "_toon_chat_sounds: " << _toon_chat_sounds << endl;

      if(minor>=6) {
          ifs >> b;
          _accepting_new_friends = (b!=false);
      } else _accepting_new_friends = true;
      ofs << "_accepting_new_friends: " << _accepting_new_friends << endl;

      if(minor>=7) {
          ifs >> b;
          _embedded_mode = (b!=false);
      } else _embedded_mode = false;
      ofs << "_embedded_mode: " << _embedded_mode << endl;

      break;
    default:
      ofs << "default" << endl;
      // unknown major #, spit out some 'defaults'
      _sfx = _music = _chat = true;
      _custom_mousecursor_enabled = true;
      _bUseWindowedMode = true;
      _bShowFpsMeter = false;
      _bForceSWMidi = true;
      _sfx_vol = _music_vol = 1.0f;
      _driver = D_NONE;
      _res = R_NONE;
      _stype = S_NONE;
      _toon_chat_sounds = true;
      _accepting_new_friends = true;
      _embedded_mode = false;
    }
    ifs.close();
  }
    //  } else
    //    cerr << "**** CANNOT READ FILE ****" << endl;
}

// it would be simpler to just store the actual res sizes, but abstracting them makes
// it harder to crash with a bad resolution

// this array must match:  enum Resolution { R640x480, R800x600, R1024x768, R1280x1024, R1600x1200, R_NONE };
const unsigned int resolution_dimensions[Settings::R_NONE][2] = {{640,480}, {800,600}, {1024,768}, {1280,1024}, {1600,1200}};

void Settings::
get_resolution_sizes(Resolution r, unsigned int &xsize, unsigned int &ysize) {
  xsize=resolution_dimensions[r][0];
  ysize=resolution_dimensions[r][1];
}

void Settings::
set_resolution_dimensions(unsigned int xsize,unsigned int ysize) {
  unsigned int r;
  for(r=Resolution(0);r<R_NONE;r++) {
      if((xsize==resolution_dimensions[r][0]) && (ysize==resolution_dimensions[r][1]))
          break;
  }

  if(r>=R_NONE) {
      cerr << "set_res failed, Enum Resolution does not contain " << xsize << "x" << ysize << endl;
      return;
  }
  get_ptr()->ns_set_resolution((Resolution)r);
}

