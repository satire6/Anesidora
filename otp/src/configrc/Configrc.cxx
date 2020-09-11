// Filename: Configrc.cxx
// $Id$
//
////////////////////////////////////////////////////////////////////

#include "settingsFile.h"
#include "dSearchPath.h"
#include "key_src.cxx"
#ifdef _WIN32
#include <windows.h>
#endif

#include "openssl/ssl.h"
#include "openssl/md5.h"

// Windows may define this macro inappropriately.
#ifdef X509_NAME
#undef X509_NAME
#endif

// hack to share enums w/installer
class SysInfo {
public:
  // MPG hack to avoid moving installer to OTP yet
  //#include "../installer/sysinfodefs.h"
  #include "sysinfodefs.h"
};

#define _str(s) #s
#define _xstr(s) _str(s)

#ifdef USE_TESTSERVER
  #define TESTSTR "Test"
  const char *activex_control_name = "tt_test.dll";
  const char *InstallerGuid="FF791555-FDAC-43ab-B792-389E4CC0A6E5";
#else
  #if defined(USE_CASTILLIAN)
    #define TESTSTR _xstr(PRODUCT_NAME)
    const char *InstallerGuid="8CD7CB6E-EDD0-4b94-A4B9-27B2E9BE2FA3";
    const char *activex_control_name = "ttinst-castillian.dll";
  #elif defined(USE_JAPANESE)
    #define TESTSTR _xstr(PRODUCT_NAME)
    const char *InstallerGuid="E76AABC4-07F4-47c3-BC55-B16119A793CF";
    const char *activex_control_name = "ttinst-japanese.dll";
  #elif defined(USE_GERMAN)
    #define TESTSTR _xstr(PRODUCT_NAME)
    const char *InstallerGuid="95BD7A59-567A-4fe1-A412-FCEC29428E42";
    const char *activex_control_name = "ttinst-german.dll";
  #elif defined(USE_PORTUGUESE)
    #define TESTSTR _xstr(PRODUCT_NAME)
    const char *InstallerGuid="31CB2F01-72C2-4cf4-B265-450E8817B039";
    const char *activex_control_name = "ttinst-portuguese.dll";
  #elif defined(USE_FRENCH)
    #define TESTSTR _xstr(PRODUCT_NAME)
    const char *InstallerGuid="63308B48-F435-42fd-AB0A-3564C7BEF9D7";
    const char *activex_control_name = "ttinst-french.dll";
  #else
    #define TESTSTR ""
    const char *activex_control_name = "ttinst.dll";
    const char *InstallerGuid="C02226EB-A5D7-4B1F-BD7E-635E46C2288D";
  #endif
#endif

const char *configrc_override_filename = "xrc";
const char *ToontownRegKeyName = "SOFTWARE\\Disney\\Disney Online\\Toontown" TESTSTR;  //under HKEY_LOCAL_MACHINE

#ifdef _WIN32
void write_opengl_hardware_info(HKEY hKeyToontown);
#endif // _WIN32

// win32 cruft
// file existance:
// if (GetFileAttributes(strFilePath) != 0xFFFFFFFF)  return true;
// file readability:
// You HAVE to try to open the file to find out if it's openable. Since files
// can be opend for either shared or exclusive access by other processes, you
// can't just check the static permissions or attributes. To test for
// openability, Open the file for readonly|sharedaccess. This way you won't
// block any other programs from accessing it.
// executable:
// if it ends in ".exe" or ".com" then you can assume it's executable. If you
// try to createprocess on it and get an error, then it was not.


#ifdef _WIN32

#include <string>
#include <vector>
using namespace std;
typedef vector<string> StrVec;

static void
filesearch(string rootpath, string pattern, bool bRecursive, bool bSearchForDirs, bool bPrintFileInfo, StrVec &files)
{
    // typical arguments:  filesearch("C:\\temp\\mview","*",true,true,sveclist);
    WIN32_FIND_DATA current_file;

    // first find all the files in the rootpath dir that match the pattern
    string searchpathpattern = rootpath + "\\" + pattern;
    HANDLE searcher = FindFirstFile(searchpathpattern.c_str(), &current_file);
    if ( searcher == INVALID_HANDLE_VALUE)
        return;
    do {
      string fileline;

      if(bSearchForDirs) {
          // save only dirs
          if ((current_file.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
              (!(current_file.cFileName[0] == '.'))) {
               fileline = rootpath + "\\" + current_file.cFileName;
               files.push_back(fileline);
          }
      } else {
          // save only files
          if(!((current_file.cFileName[0] == '.') ||
               (current_file.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))) {
                  if(bPrintFileInfo) {
                      SYSTEMTIME stime;
                      FileTimeToSystemTime(&current_file.ftCreationTime,&stime);
                      char extra_info[100];
                      sprintf(extra_info, ", (%d/%d/%d), %d bytes",stime.wMonth,stime.wDay,stime.wYear,current_file.nFileSizeLow);
                      fileline = rootpath + "\\" + current_file.cFileName + extra_info;
                  } else {
                   fileline = rootpath + "\\" + current_file.cFileName;
                  }
                  files.push_back(fileline);
          }
      }
    } while (FindNextFile(searcher, &current_file));
    FindClose(searcher);

    if (bRecursive) {
        // then call yourself recursively on all dirs in the rootpath
        string newsearchpath = rootpath + "\\*";
        HANDLE searcher = FindFirstFile(newsearchpath.c_str(), &current_file);
        if ( searcher == INVALID_HANDLE_VALUE)
            return;
        do {
            if ( current_file.cFileName[0] == '.' ||
                !(current_file.dwFileAttributes &
                         FILE_ATTRIBUTE_DIRECTORY))
                continue;
            newsearchpath = rootpath + "\\" + current_file.cFileName;
            filesearch(newsearchpath, pattern, true, bSearchForDirs, bPrintFileInfo, files);
        } while (FindNextFile(searcher, &current_file));
        FindClose(searcher);
    }
}

static void UninstallActiveX(const char *control_name,const char *control_GUID)
{
    typedef HRESULT (WINAPI *REMOVECONTROLBYNAME)(
                 LPCTSTR lpszFile,
                 LPCTSTR lpszCLSID,
                 LPCTSTR lpszTypeLibID,
                 BOOL bForceRemove,
                 DWORD dwIsDistUnit);

    HMODULE                   hMod=NULL;
    REMOVECONTROLBYNAME       pfnRemoveControl;
    HKEY hKey;
    const char *ActiveXCache_RegValName = "ActiveXCache";
    const char *InternetSettingsRegKeyStr = "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"; //under HKLM
    char activeXcontrol_filepath[512];
    DWORD bufsize = sizeof(activeXcontrol_filepath);
    string guidstr,searchpattern;
    StrVec file_list, control_list;

    if (ERROR_SUCCESS != RegOpenKeyEx(HKEY_LOCAL_MACHINE,InternetSettingsRegKeyStr,0,KEY_READ,&hKey)) {
        goto error_exit;
    }

    if(ERROR_SUCCESS != RegQueryValueEx(hKey, ActiveXCache_RegValName, NULL, NULL, (LPBYTE)activeXcontrol_filepath, &bufsize)) {
        goto error_exit;
    }

    RegCloseKey(hKey);

    hMod = LoadLibrary("occache.dll");
    if (!hMod)
      goto error_exit;

    pfnRemoveControl = (REMOVECONTROLBYNAME)GetProcAddress(hMod, "RemoveControlByName");
    if (!pfnRemoveControl)
      goto error_exit;

    // guid must be bracketed by '{}' for RemoveControlByName
    guidstr = "{" + string(control_GUID) + "}";

    char control_basename[20];
    strcpy(control_basename,control_name);
    control_basename[strlen(control_name)-4]='\0';  // assumes control_name ends in .xxx

    filesearch(activeXcontrol_filepath, control_name, true, false, false, control_list);

    for(unsigned i=0;i<control_list.size();i++) {
        HRESULT hr =  (*pfnRemoveControl)(control_list[i].c_str(),guidstr.c_str(),
                                          NULL, true, true);
    }

    FreeLibrary(hMod);

    searchpattern = string(control_basename) + "*";
    filesearch(activeXcontrol_filepath, searchpattern, true, false, false, file_list);

    for(unsigned i=0;i<file_list.size();i++) {
        // try to delete the file
        BOOL bSuccess = DeleteFile(file_list[i].c_str());
        if(!bSuccess) {
            DWORD err = GetLastError();
            if((err==ERROR_ACCESS_DENIED)||(err==ERROR_SHARING_VIOLATION)) {
                MessageBox( NULL, "Please close all Internet Explorer browser windows, then press OK to continue Toontown un-installation.", "Toontown Uninstaller", MB_OK | MB_ICONWARNING );
                DeleteFile(file_list[i].c_str());
            }
        }
    }

    return;

   error_exit:
       if(hMod!=NULL) {
           FreeLibrary(hMod);
       }
       cerr << "Error uninstalling " << control_name << "!\n";
       exit(1);
}

// fTestInterval is in seconds
static DWORD FindCPUMhz(float fTestInterval) {
 volatile DWORD Freq, EAX_tmp, EDX_tmp;
 int mSecs=(int)(fTestInterval*1000);
 if(mSecs<1)
   return 0;
 DWORD uSecs=mSecs*1000;

 // SetThreadPriority could be temporarily used to ensure we're not swapped out
 // seems to work ok without it for now

__asm {
     RDTSC
     mov  EAX_tmp, eax
     mov  EDX_tmp, edx
 }

 Sleep(mSecs);

 __asm {
     RDTSC
     mov  ecx, uSecs
     sub  eax, EAX_tmp
     sbb  edx, EDX_tmp
     div  ecx
     mov  Freq, eax        // Freq gets the frequency in MHz
 }

  return Freq;
}
#endif

static void write_const(ostream& os) {
  // write out the stuff that we always want in the configfile
  os << "#" << endl << "# constant config settings" << endl << "#" << endl
     << endl;
  os << "chan-config-sanity-check #f" << endl;
  os << "window-title Toontown" << endl;

  // We want to detect when a window does not open, and handle it in
  // ToonBase.py. Thus we don't want ShowBase to raise an exception if
  // the window fails to open.
  os << "require-window 0" << endl;

  // Set the language
#if defined(USE_ENGLISH)
  os << "language english" << endl;
//  os << "product-name DisneyOnline-US" << endl;
#elif defined(USE_CASTILLIAN)
  os << "language castillian" << endl;
  os << "product-name ES" << endl;
#elif defined(USE_JAPANESE)
  os << "language japanese" << endl;
  os << "product-name JP" << endl;
#elif defined(USE_GERMAN)
  os << "language german" << endl;
  os << "product-name T-Online" << endl;
#elif defined(USE_PORTUGUESE)
  os << "language portuguese" << endl;
  os << "product-name BR" << endl;
#elif defined(USE_FRENCH)
  os << "language french" << endl;
  os << "product-name FR" << endl;
#else
#error Unrecognized language defined
#endif // language
#ifdef IS_OSX
  os << "icon-filename toontown_mac_icon.rgb" << endl;
#else
  os << "icon-filename toontown.ico" << endl;
#endif  // IS_OSX

  os << endl;
  os << "cull-bin shadow 15 fixed" << endl;
  os << "cull-bin ground 14 fixed" << endl;
  os << "cull-bin gui-popup 60 unsorted" << endl;
  os << "default-model-extension .bam" << endl;
  os << "plugin-path ." << endl;

  os << "# downloader settings" << endl;
  os << "decompressor-buffer-size 32768" << endl;
  os << "extractor-buffer-size 32768" << endl;
  os << "patcher-buffer-size 512000" << endl;
  os << "downloader-timeout 15" << endl;
  os << "downloader-timeout-retries 4" << endl;
  os << "downloader-disk-write-frequency 4" << endl;
  // Assume we are fast until we are told otherwise
  os << "downloader-byte-rate 125000" << endl;
  os << "downloader-frequency 0.1" << endl;
  os << "want-render2dp 1" << endl;

  os << endl;
  os << "# texture settings" << endl;
  // this setting forces a panda scale-down for all textures
  // it really should be up to the gsg to make the determination
  // if the HW can support that tex size, so comment this out for now
  // os << "max-texture-dimension 256" << endl;

  // leaving this in for the benefit of screen shots, which
  // will not be pow2 when saved
  os << "textures-power-2 down" << endl;

  os << endl;
  os << "# loader settings" << endl;
  os << "load-file-type toontown" << endl;
  os << "dc-file phase_3/etc/toon.dc" << endl;
  os << "dc-file phase_3/etc/otp.dc" << endl;
#ifdef WIN32
  os << "aux-display pandadx9" << endl;
  os << "aux-display pandadx8" << endl;
#endif
  os << "aux-display pandagl" << endl;
  os << "aux-display tinydisplay" << endl;
  os << "compress-channels #t" << endl;
  os << "display-lists 0" << endl;
  os << "text-encoding utf8" << endl;

  // We don't want DirectEntries to return unicode strings for now.
  os << "direct-wtext 0" << endl;

  os << "text-never-break-before ,.-:?!;。？！、" << endl;
  os << endl;
  os << "early-random-seed 1" << endl;

  os << "verify-ssl 0" << endl;

  os << "http-preapproved-server-certificate-filename ttown4.online.disney.com:46667 gameserver.txt" << endl;

  // For now, restrict SSL communications to the cheaper RC4-MD5
  // cipher.  This should lighten the CPU load on the gameserver.
  os << "ssl-cipher-list RC4-MD5" << endl;
  os << "paranoid-clock 1" << endl;
  os << "lock-to-one-cpu 1" << endl;
  os << "collect-tcp 1" << endl;
  os << "collect-tcp-interval 0.2" << endl;
  os << "respect-prev-transform 1" << endl;
  os << endl;
  os << "# notify settings" << endl;
  // os << "notify-level-downloader debug" << endl;
  //  os << "notify-level-DistributedBattleBldg debug" << endl;
  // os << "notify-level-express debug" << endl;
  // Turn off spam from some noisy notify cats
  os << "notify-level-collide warning" << endl;
  os << "notify-level-chan warning" << endl;
  os << "notify-level-gobj warning" << endl;
  os << "notify-level-loader warning" << endl;
  os << "notify-timestamp #t" << endl;
  os << endl;

  // Give the decompressor and extractor plenty of timeslices before
  // we get the window open.
  os << "decompressor-step-time 0.5" << endl;
  os << "extractor-step-time 0.5" << endl;
  os << endl;

  os << "# Server version" << endl;

  // default settings for ENGLISH
  // sv1.0.40.25.test
  int lang = 0, build = 25;
  char *loginType = "playToken";
#if defined(USE_CASTILLIAN)
  lang = 1;		// sv1.1.33.x
  build = 0;
  loginType = "playToken";
#elif defined(USE_JAPANESE)
  lang = 2;		// sv1.2.33.x
  build = 0;
  loginType = "playToken";
#elif defined(USE_GERMAN)
  lang = 3;		// sv1.3.33.x
  build = 0;
  loginType = "playToken";
#elif defined(USE_PORTUGUESE)
  lang = 4; 	// sv1.4.33.x
  build = 0;
  loginType = "playToken";
#elif defined(USE_FRENCH)
  lang = 5;		// sv1.5.33.x
  build = 0;
  loginType = "playToken";
#endif
  os << "server-version sv1." << lang << ".40." << build << ".test" << endl;
  //os << "server-version dev" << endl;

#ifdef IS_OSX
  os << "server-version-suffix .osx" << endl;
#else
  os << "server-version-suffix " << endl;
#endif

  os << "required-login " << loginType << endl;

  os << "server-failover 80 443" << endl;
  os << "want-fog #t" << endl;
  os << "dx-use-rangebased-fog #t" << endl;
  os << "aspect-ratio 1.333333" << endl;
  // make OnScreenDebug use a font that we're already downloading
  os << "on-screen-debug-font phase_3/models/fonts/ImpressBT.ttf" << endl;

  // The current Toontown code now supports temp-hpr-fix.
  // Welcome to the future.
  os << "temp-hpr-fix 1" << endl;

  // Japanese, Korean, and Chinese clients will like to have these
  // features enabled.
  os << "ime-aware 1" << endl;
  os << "ime-hide 1" << endl;

  // There appears to be some performance issues with using vertex
  // buffers on nvidia drivers in DX8.  Probably I've screwed
  // something up in there.  For now, turn it off; we don't really
  // need (nor can Toontown take advantage of) the potential
  // performance gains anyway.
  os << "vertex-buffers 0" << endl;
  os << "dx-broken-max-index 1" << endl;

  // Temporarily disable the use of D3DPOOL_DEFAULT until we can be
  // confident it is working properly.
  os << "dx-management 1" << endl;

  // setting to determine if new login API from new website is used or not
  os << "tt-specific-login 0" << endl;

  // We don't need Toontown to be case-sensitive on the client end.
  // Clients are sometimes known to rename their system directories
  // without regard to case.
  os << "vfs-case-sensitive 0" << endl;

  // This is designed to prevent people from wedging something on a
  // keyboard button or something in an attempt to defeat the sleep
  // timeout.  After this amount of time, with no changes in keyboard
  // state, all the keys are "released".
  os << "inactivity-timeout 180" << endl;

  // Need to turn on this option to support our broken door triggers.
  os << "early-event-sphere 1" << endl;

  // This keeps the joint hierarchies for the different LOD's of an
  // Actor separate.  Seems to be necessary for the Toons--some of the
  // naked Toons seem to have slightly different skeletons for the
  // different LOD's.
  os << "merge-lod-bundles 0" << endl;

  // Keep the frame rate from going too ridiculously high.  This is
  // mainly an issue when the video driver doesn't support video sync.
  // Limiting the frame rate helps out some of the collision issues
  // that you get with a too-high frame rate (some of our trigger
  // planes require a certain amount of interpenetration to be
  // triggered), and is also just a polite thing to do in general.
  os << "clock-mode limited" << endl
     << "clock-frame-rate 120" << endl;

  // Not using parasite_buffer to speed things up in places where
  // creating this buffer seems to cause frame rate issues such
  // as the Photo Fun game.
  os << "prefer-parasite-buffer 0" << endl;

  // This turns on In Game News
  os << "want-news-page 1" << endl;

  // Temporarily turn off IGN over HTTP due to crash
  // os << "news-over-http 0" << endl;
  // os << "news-base-dir phase_3.5/models/news/" << endl;
  // os << "news-index-filename news_index.txt" << endl;

  os << "news-over-http 1" << endl;
  // os << "in-game-news-url http://download.test.toontown.com/news/" << endl;
  os << "news-base-dir /httpNews" << endl;
  os << "news-index-filename http_news_index.txt" << endl;

  // This should now be on by default
  // os << "want-new-toonhall 1" << endl;

  // need to specify audio library to use, such as Miles or FMOD etc
  os << "audio-library-name miles_audio" << endl;
}

static void write_audio(ostream& os, bool sfx_active, bool music_active, float sfx_vol,
                 float music_vol) {
  os << "#" << endl << "# audio related options" << endl << "#" << endl
     << endl;
  os << "# load the loaders" << endl;
  os << "audio-loader mp3" << endl;
  os << "audio-loader midi" << endl;
  os << "audio-loader wav" << endl;


  // This just seems like a good idea.  It doesn't appear to cost too
  // much CPU, and hardware support of midi seems to be spotty.

  // but some HW midi sounds better than the SW midi, so allow it to be configured
  os << "audio-software-midi #" << (Settings::get_force_sw_midi() ? "t" : "f") << endl;

  os << endl;
  if (sfx_active)
    os << "# turn sfx on" << endl << "audio-sfx-active #t" << endl;
  else
    os << "# turn sfx off" << endl << "audio-sfx-active #f" << endl;
  if (music_active)
    os << "# turn music on" << endl << "audio-music-active #t" << endl;
  else
    os << "# turn music off" << endl << "audio-music-active #f" << endl;
  os << endl;
  os << "audio-master-sfx-volume " << sfx_vol << endl;
  os << "audio-master-music-volume " << music_vol << endl;
}

static void write_res(ostream& os, unsigned int x, unsigned int y) {
  os << "#\n# display resolution\n#\n\n";
  os << "win-size " << x << " " << y << endl;
}

static void write_prod(ostream& os) {
  os << "#" << endl << "# server type" << endl << "#" << endl << endl;
  os << "server-type prod" << endl;
}

static void write_dev(ostream& os) {
  os << "#" << endl << "# server type" << endl << "#" << endl << endl;
  os << "server-type dev" << endl;
}

static void write_debug(ostream& os) {
  os << "#" << endl << "# server type" << endl << "#" << endl << endl;
  os << "server-type debug" << endl;
}

// stricmp() isn't standard ANSI, although it should be.  We'll use
// our own function as a quick workaround.  This is actually
// duplicated from string_utils.cxx, which we can't link with because
// of the whole Configrc-dtool linking thing.
static int
cmp_nocase(const string &s, const string &s2) {
  string::const_iterator p = s.begin();
  string::const_iterator p2 = s2.begin();

  while (p != s.end() && p2 != s2.end()) {
    if (toupper(*p) != toupper(*p2)) {
      return (toupper(*p) < toupper(*p2)) ? -1 : 1;
    }
    ++p;
    ++p2;
  }

  return (s2.size() == s.size()) ? 0 :
    (s.size() < s2.size()) ? -1 : 1;  // size is unsigned
}

static void
read_file(string &result, const Filename &filename) {
  pifstream file;
  if (!filename.open_read(file)) {
    return;
  }

  static const int buffer_size = 1024;
  char buffer[buffer_size];

  file.read(buffer, buffer_size);
  size_t count = file.gcount();
  while (count != 0) {
    result += string(buffer, buffer + count);
    file.read(buffer, buffer_size);
    count = file.gcount();
  }
  result += string(buffer, buffer + count);
}

// Look for an override file ("xrc"), verify that it has been signed
// with the expected key, and output its contents to the stream if it
// has.
static void
output_overrides(ostream &os) {
  Filename override_filename =
    Filename::binary_filename(configrc_override_filename);
  if (!override_filename.exists()) {
    return;
  }
  Filename signature_filename =
    Filename::binary_filename(override_filename);
  signature_filename.set_extension("sig");
  if (!signature_filename.exists()) {
    return;
  }

  string override, signature;
  read_file(override, override_filename);
  read_file(signature, signature_filename);

  if (override.empty() || signature.empty()) {
    return;
  }

  // Generate an MD5 hash of the override contents.
  static const int md5_len = 16;
  unsigned char md[md5_len];
  MD5((const unsigned char *)override.data(), override.length(), md);

  // Now validate the signature.  Create an in-memory BIO to read the
  // public key from the memory buffer.
  BIO *mbio = BIO_new_mem_buf((void *)pubkey, pubkey_len);
  EVP_PKEY *pkey = d2i_PUBKEY_bio(mbio, NULL);
  BIO_free(mbio);
  if (pkey == (EVP_PKEY *)NULL) {
    return;
  }

  RSA *rsa = EVP_PKEY_get1_RSA(pkey);
  EVP_PKEY_free(pkey);

  if (rsa == (RSA *)NULL) {
    return;
  }

  int keysize = RSA_size(rsa);
  char *hash = new char[keysize];

  int hashlen = RSA_public_decrypt(signature.length(),
                                   (unsigned char *)signature.data(),
                                   (unsigned char *)hash, rsa,
                                   RSA_PKCS1_PADDING);
  if (hashlen > keysize) {
    // This should never happen.  Memory overrun!
    abort();
  }
  if (hashlen <= 0) {
    delete[] hash;
    return;
  }

  /*
  cerr << hex;
  int i;
  for (i = 0; i < md5_len; i++) {
    cerr << setw(2) << setfill('0') << (unsigned int)(unsigned char)md[i];
  }
  cerr << "\n";
  for (i = 0; i < hashlen; i++) {
    cerr << setw(2) << setfill('0') << (unsigned int)(unsigned char)hash[i];
  }
  cerr << dec << "\n";
  */

  bool match = (hashlen == md5_len && memcmp(md, hash, md5_len) == 0);
  delete[] hash;
  if (!match) {
    return;
  }

  // Success!
  os.write(override.data(), override.length());
}

int main(int argc, char*argv[]) {

 Settings::DisplayDriver new_disp_type = Settings::D_NONE;
 bool bPrintHelp=false;
 bool bDontOverwriteExistingSettings=false;
 bool bWriteStdout=false;
 bool bSaveSettings=false;
 bool bSetCursor=false;
 bool bUseCustomCursor;
 bool bUninstallActiveX=false;
 bool bPickBestRes=false;
 bool bSetLowRes=false;
 bool bChangedSettings = false;
 bool bDoSetWindowedMode=false;
 bool bWindowedMode;
 bool bDoSetShowFPSMeter=false;  // dont want to change this unless user explicitly specified to
 bool bShowFPSMeter;
 bool bDoSetForceSWMidi=false;  // dont want to change this unless user explicitly specified to
 bool bForceSWMidi;

 for (int a = 1; a < argc; a++) {
    if ((argv[a] != (char*)0L) && (strlen(argv[a])>1) &&
        (argv[a][0] == '-') ||
        (argv[a][0] == '/')) {

        char *pArgStr=argv[a]+1;
        if(cmp_nocase(pArgStr,"OGL")==0) {
          new_disp_type=Settings::GL;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"DX9")==0) {
          new_disp_type=Settings::DX9;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"DX8")==0) {
          new_disp_type=Settings::DX8;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"DX7")==0) {
          // This is deprecated, but supported for historical reasons.
          // DX7 means DX8.
          new_disp_type=Settings::DX8;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"default")==0) {
          new_disp_type=Settings::D_DEFAULT;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"NoOverride")==0) {
          bDontOverwriteExistingSettings=true;
        } else if(cmp_nocase(pArgStr,"save")==0) {
          bSaveSettings=true;
        } else if(cmp_nocase(pArgStr,"lowres")==0) {
          bSaveSettings=true;
          bSetLowRes=true;
        } else if(cmp_nocase(pArgStr,"fullscreen")==0) {
          bSaveSettings=true;
          bWindowedMode=false;
          bDoSetWindowedMode=true;
        } else if(cmp_nocase(pArgStr,"windowed")==0) {
          bSaveSettings=true;
          bSetLowRes=true;  // make sure window is not bigger than desktop initially
          bWindowedMode=true;
          bDoSetWindowedMode=true;
        } else if(cmp_nocase(pArgStr,"show_fps")==0) {
          bSaveSettings=true;
          bShowFPSMeter=true;
          bDoSetShowFPSMeter=true;
        } else if(cmp_nocase(pArgStr,"hide_fps")==0) {
          bSaveSettings=true;
          bShowFPSMeter=false;
          bDoSetShowFPSMeter=true;
        } else if(cmp_nocase(pArgStr,"force_sw_midi")==0) {
          bSaveSettings=true;
          bForceSWMidi=true;
          bDoSetForceSWMidi=true;
        } else if(cmp_nocase(pArgStr,"allow_hw_midi")==0) {
          bSaveSettings=true;
          bForceSWMidi=false;
          bDoSetForceSWMidi=true;
        } else if(cmp_nocase(pArgStr,"stdout")==0) {    // this is usually hidden
          bWriteStdout=true;
        } else if(cmp_nocase(pArgStr,"cursor_on")==0) {
          bSetCursor=true;
          bUseCustomCursor=true;
          bChangedSettings = true;
        } else if(cmp_nocase(pArgStr,"cursor_off")==0) {
          bSetCursor=true;
          bUseCustomCursor=false;
          bChangedSettings = true;
      #ifdef USE_TESTSERVER
        } else if(cmp_nocase(pArgStr,"uninstall_testserver_activex")==0) {
          bUninstallActiveX=true;
      #endif
        } else if(cmp_nocase(pArgStr,"uninstall_activex")==0) {
          bUninstallActiveX=true;
        } else if(cmp_nocase(pArgStr,"pickbestres")==0) {
          bPickBestRes=true;
        } else {
          cerr << "Invalid argument: " << argv[a] << endl;
          bPrintHelp=true;
        }
    } else {
       cerr << "Invalid argument: " << argv[a] << endl;
       bPrintHelp=true;
    }
  }

  bool bDoSavedSettingsExist = Settings::doSavedSettingsExist();

  if (bChangedSettings && !bWriteStdout) {
    // If the user specified one of the -OGL etc. options, but not
    // -stdout, he probably meant to specifiy -save to save those
    // changes for the next run of Toontown.

    // note: NoOverride cancels the save if file 'useropt' exists
    bSaveSettings = true;
  }

  if(bPrintHelp) {
   cerr << "Syntax: configrc [options]\n";
   cerr << "Options:\n";
   cerr << "-OGL:         select OpenGL as the graphics rendering interface\n";
   cerr << "-DX9:         select Direct3D 9 as the graphics rendering interface\n";
   cerr << "-DX8:         select Direct3D 8 as the graphics rendering interface\n";
   cerr << "-cursor_off:  use standard windows mouse cursor\n";
   cerr << "-cursor_on:   use custom toontown mouse cursor\n";
   cerr << "-lowres:      set the startup screen resolution to 640x480\n";
   cerr << "-fullscreen:  use fullscreen mode\n";
   cerr << "-windowed:    use windowed mode\n";
   cerr << "-show_fps:    show frames/sec perf meter\n";
   cerr << "-hide_fps:    do not show frames/sec perf meter\n";
   cerr << "-force_sw_midi: force use of software-midi to play midi music\n";
   cerr << "-allow_hw_midi: allow use of midi hardware to play midi music, if it exists\n";
   cerr << "-NoOverride:  ignore new setting specifications if saved options file exists\n";

   // Let's not advertise this option; it's just for internal use and
   // telling users about it makes our config options that much easier
   // to hack
   //   cerr << "-stdout:     write new Configrc to stdout\n";

   // mostly useless to advertise since only I know what it does
   // cerr << "-pickbestres: try to pick a startup screen resolution based on vidmem size\n";


   cerr << "-save:        save settings to '" << configrc_settings_filename << "' file (default)\n";
   cerr << "-uninstall_activex: uninstall toontown activex control\n";
//   cerr << "-uninstall_testserver_activex: uninstall testserver toontown activex control\n";
   exit(1);
  }

#ifdef _WIN32
  if(bUninstallActiveX) {
      UninstallActiveX(activex_control_name,InstallerGuid);
      // dont want to generate any configrc output here
      exit(0);
  }
#endif

  // first write out any changes to the Settings object, then translate settings to a Configrc

  // this allows the user to change out of a bad scrn resolution outside of TT
  if(bSetLowRes)
      Settings::set_resolution(Settings::R640x480);

  if(bDoSetWindowedMode)
      Settings::set_windowed_mode(bWindowedMode);

  if(bDoSetShowFPSMeter)
      Settings::set_show_fpsmeter(bShowFPSMeter);

  if(bDoSetForceSWMidi)
      Settings::set_force_sw_midi(bForceSWMidi);

  if (!bDontOverwriteExistingSettings ||
      Settings::display_driver() == Settings::D_DEFAULT) {
    if(new_disp_type != Settings::D_NONE) {
      Settings::set_display_driver(new_disp_type);
    }
  }

  if(!bDontOverwriteExistingSettings) {
      if(bSetCursor)
          Settings::set_custom_mouse_cursor(bUseCustomCursor);
  }

  if(!(bDontOverwriteExistingSettings && bDoSavedSettingsExist)) {
    if(bSaveSettings)
      Settings::write_settings();
  }

#ifdef USE_OFSTREAM
  pofstream os("Configrc");
#else
  ostream& os = cout;
#endif


  if(!bWriteStdout) {
#ifdef USE_OFSTREAM
      os.close();
#endif
      return 0;
  }

  output_overrides(os);

  write_const(os);
  os << endl;

  if(Settings::want_custom_mouse_cursor()) {
    os << "cursor-filename toonmono.cur" << endl << endl;
    //  not using 256 color cursors right now due to common driver probs
    //  os << "win32-color-cursor phase_3/models/gui/toon.cur" << endl;
  }

  if(Settings::get_show_fpsmeter()) {
    os << "show-frame-rate-meter #t" << endl << endl;
  }

#if 0  // This seems to crash on dual-core CPU's, and it's not worth the trouble of fixing it.
  #ifdef WIN32_VC
    float lod_stress_factor=1.0f;

    // stupid hack 1-time adjust of lod stress factor based on CPU speed to reduce close-up
    // popping on faster machines.   this is a placeholder until we do a system that adjusts
    // lod_stress_factor dynamically based on current fps

    DWORD Mhz=FindCPUMhz(0.1f);
    // lower lods are not yet designed to be viewed closer up,
    // cant increase stress to >1 yet
     if(Mhz<1000)
        lod_stress_factor=1.0f;
     else if(Mhz<1300)
        lod_stress_factor=0.7f;
     else if(Mhz<1700)
        lod_stress_factor=0.3f;
     else lod_stress_factor=0.25f;

     os << "lod-stress-factor " << lod_stress_factor << endl << endl;
  #endif
#endif  // 0

  Settings::DisplayDriver driver_type = Settings::display_driver();
  switch (driver_type) {
      case Settings::DX7:
      case Settings::DX8:
#ifdef WIN32
        os << "load-display pandadx8" << endl;
        break;
#endif  // fall through on non-Windows case

      case Settings::DX9:
      case Settings::D_DEFAULT:
#ifdef WIN32
        os << "load-display pandadx9" << endl;
        break;
#endif  // fall through on non-Windows case

      case Settings::GL:
        os << "load-display pandagl" << endl;
        break;

      default:
        // this is an error, it must be one of the above.
        break;
  }
  os << endl;

  char fs_str[2];
  fs_str[0]=(Settings::get_windowed_mode() ? 'f' : 't');
  fs_str[1]='\0';
  os << "fullscreen #" << fs_str << "\n\n";

  write_audio(os, Settings::get_sfx(), Settings::get_music(),
              Settings::get_sfx_volume(), Settings::get_music_volume());
  os << endl;

  unsigned int xsize,ysize;
  Settings::get_resolution_sizes(Settings::get_resolution(),xsize,ysize);
  write_res(os,xsize,ysize);
  os << endl;

  if(bPickBestRes && !bDoSavedSettingsExist) {
      // right now pickbestres only works for dx9, so in case we switch to dx8/ogl we need to write
      // a win-size res as normal.

      // for now behavior is 'no-override' by default,
      // if file 'useropt' already exists, dont want to override a saved res in that
      os << "pick-best-screenres #t\n\n";
  }

  switch (Settings::server_type()) {
      case Settings::PRODUCTION:
        write_prod(os);
        break;
      case Settings::DEVELOPMENT:
        write_dev(os);
        break;
      case Settings::DEBUG:
        write_debug(os);
        break;
      default:
        // this is an error, it must be one of the above.  Emit prod by default
        cerr << "There is an error in the settings file w.r.t. the server type\n";
        write_prod(os);
  }
#ifdef USE_OFSTREAM
  os.close();
#endif

#ifdef _WIN32
  // write regkeys for installer to read and send to stat server

  HKEY hKeyToontown;
  ULONG regRetVal=RegOpenKeyEx(HKEY_LOCAL_MACHINE, ToontownRegKeyName, 0,
                               KEY_WRITE, &hKeyToontown);
  if(regRetVal!=ERROR_SUCCESS) {
     return 7;
  }

  // probably cleaner to write all these settings in a 'ConfigSettings' subkey
  DWORD bIsWindowed=Settings::get_windowed_mode();
  RegSetValueEx(hKeyToontown, "UsingWindowedMode", 0, REG_DWORD, (LPBYTE)&bIsWindowed, sizeof(bIsWindowed));
  char buf[20];
  sprintf(buf,"%dx%d",xsize,ysize);
  RegSetValueEx(hKeyToontown, "LastScreenSize", 0, REG_SZ, (LPBYTE)buf, strlen(buf));

  // we should really sync installer sysinfo.h and settings.h defs so they use the same ones and can communicate more easily
  // probably means changing settingsfilename(useropt) format to sysinfo's since it is more detailed

  SysInfo::GAPIType gapi=SysInfo::GAPI_Unknown;
  switch (driver_type) {
      case Settings::DX9:
          // installer should bump this down to 9.0 if that's all they have
          gapi=SysInfo::GAPI_DirectX_9_0;
          break;
      case Settings::DX8:
      case Settings::DX7:
          // installer should bump this down to 8.0 if that's all they have
          gapi=SysInfo::GAPI_DirectX_8_1;
          break;
      case Settings::GL:
          gapi=SysInfo::GAPI_OpenGL;
          write_opengl_hardware_info(hKeyToontown);
          break;
  }
  RegSetValueEx(hKeyToontown, "GfxApiUsed", 0, REG_DWORD, (LPBYTE)&gapi, sizeof(SysInfo::GAPIType));

  RegCloseKey(hKeyToontown);
#endif
  return 0;
}

#ifdef _WIN32
// since installer cant read useropt, only configrc.exe knows we are using ogl soon enough to get the glGetString info.
// and even if installer could read useropt, freelib(ogl32.dl) doesnt unload the driver dll, which sits around in IE
// hoggin memory, so better to do this stuff here

#include <gl/gl.h>

/* why wont this work?  always gives LNK4229 error.  waaah. just static-link for now.
#pragma comment(lib,"delayimp.lib")
#pragma comment(linker, "/DELAYLOAD:gdi32.dll")
*/

// tests opengl support by opening a new window we can set to ogl fmt
// need to do this for glGetString to work

static HWND CreateOpenGLWindow(char* title, int pixfmtnum, PIXELFORMATDESCRIPTOR *pPFD, int x, int y, int width, int height, BYTE type, DWORD flags,HDC *pHDC) {
    HWND        hWnd;
    WNDCLASS    wc;

    static HINSTANCE hInstance = 0;
    const char *pOGLWinClassName = "Test_OpenGLWndClass";
    *pHDC = NULL;

    assert(pPFD!=NULL && pHDC!=NULL);

    /* only register the window class once - use hInstance as a flag. */
    if (!hInstance) {
        hInstance = GetModuleHandle(NULL);
        if (!hInstance) {
            cerr <<  "GetModuleHandle() failed, err=" << GetLastError() <<endl;
        }

        wc.style         = CS_OWNDC;
        wc.lpfnWndProc   = (WNDPROC)DefWindowProc;
        wc.cbClsExtra    = 0;
        wc.cbWndExtra    = 0;
        wc.hInstance     = hInstance;
        wc.hIcon         = LoadIcon(NULL, IDI_WINLOGO);
        wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
        wc.hbrBackground = NULL;
        wc.lpszMenuName  = NULL;
        wc.lpszClassName = pOGLWinClassName;

        if (!RegisterClass(&wc)) {
            cerr << "OGL RegisterClass failed, err=" << GetLastError() <<endl;
            // MessageBox(NULL, "RegisterClass() failed: Cannot register window class.", "Error", MB_OK);
            return NULL;
        }
    }

    hWnd = CreateWindow(pOGLWinClassName, title,
            WS_OVERLAPPEDWINDOW | WS_CLIPSIBLINGS | WS_CLIPCHILDREN | WS_DISABLED,
            x, y, width, height, NULL, NULL, hInstance, NULL);

    if(hWnd == NULL) {
        cerr <<  "CreateWindow failed, err=" << GetLastError() <<endl;
        return NULL;
    }

    *pHDC = GetDC(hWnd);

    /* we're passing in the pixfmt to pick now
    ZeroMemory(&pfd, sizeof(pfd));
    pfd.nSize        = sizeof(pfd);
    pfd.nVersion     = 1;
    pfd.dwFlags      = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | flags;
    //pfd.iPixelType   = type;

    SetLastError(0);
    pf = ChoosePixelFormat(hDC, &pfd);
    if (pf == 0) {
        cerr << "ChoosePixelFormat(" << pf <<") failed, err=" << GetLastError() << endl;
        cerr << "trying with Pixelformat 1!\n";
        pf = 1;
    }
    */

    SetLastError(0);
    if (SetPixelFormat(*pHDC, pixfmtnum, pPFD) == FALSE) {
        cerr << "OGL SetPixelFormat(" << pixfmtnum <<") failed, err=" << GetLastError() << endl;
    }
    /*
    else {
        SetLastError(0);
        int numfmts=DescribePixelFormat(hDC, pf, sizeof(PIXELFORMATDESCRIPTOR), &pfd);
        if (numfmts==0 || pfd.cColorBits == 0)
            cerr << "DescribePixelFormat(" << pf <<") failed - assuming invalid!\n";
    }
    */

    // actually has no effect because of CS_OWNDC
    // ReleaseDC(hWnd, hDC);  caller must release DC now!
    return hWnd;
}

void write_opengl_hardware_info(HKEY hKeyToontown) {
    PIXELFORMATDESCRIPTOR pfd;
    ZeroMemory(&pfd,sizeof(PIXELFORMATDESCRIPTOR));
    pfd.nSize=sizeof(PIXELFORMATDESCRIPTOR);
    pfd.nVersion=1;

    // dont want to link statically with opengl32.dll, since wont use it for DX case and it hogs memory,
    // but we need opengl32.dll to be loaded prior to DescribePixFmt
    // doing a LoadLibrary for the extent of this test *should* be the same as linking statically, I hope
    HINSTANCE hOGL = LoadLibrary("opengl32.dll");
    if(!hOGL) {
      cerr << "LoadLib ogl32.dll failed, err=" << GetLastError() << endl;
      return;
    }

    HWND hWnd = 0;  // use DC of desktop window

    HDC winDC = GetDC(hWnd);  // will this fail if not administrator, since we're getting whole desktop DC?
    if(winDC==NULL) {
      cerr << "failed to get desktop DC!, err=" << GetLastError() << endl;
      return;
    }

    // note we are not switching fullscreen res to final res, so the pixfmt list may not
    // be completely accurate (it will reflect current desktop).

    int pfnum;
    int MaxPixFmtNum=DescribePixelFormat(winDC, 1, sizeof(PIXELFORMATDESCRIPTOR), &pfd);

    if(MaxPixFmtNum==0) {
     cerr << "failing OGL Check: DescribePixelFormat returns 0, hWnd: 0x" << (void*)hWnd << " hDC: 0x" << (void*)winDC;
     DWORD errnum=GetLastError();
     cerr << "  GetLastError=";
     if(errnum==ERROR_MOD_NOT_FOUND) {
         // this indicates the opengl32.dll was not loaded.  Most likely reason: linker did not link
         // with opengl32.lib because no gl* fns were called in code (or were eliminated by optimizer)
         // make sure gl[something] is called somewhere
         cerr << "ERROR_MOD_NOT_FOUND\n";
     } else cerr << errnum << endl;
    }

    // look for an ICD/MCD pixfmt
    for(pfnum=1;pfnum<=MaxPixFmtNum;pfnum++) {
        DescribePixelFormat(winDC, pfnum, sizeof(PIXELFORMATDESCRIPTOR), &pfd);

        if((pfd.dwFlags & PFD_GENERIC_FORMAT)!=0) {
            // drvtype = Software;
            // cerr << "skipping GL pixfmt[" << pfnum << "] due to SW fmt" << endl;
            continue;
        }

        /*else if ( pfd.dwFlags & PFD_GENERIC_ACCELERATED )
            drvtype = MCD;
        else drvtype = ICD;*/

        if(pfd.iPixelType == PFD_TYPE_COLORINDEX) {
          // cerr << "skipping GL pixfmt[" << pfnum << "] due to colorindex" << endl;
          continue;
        }

        if(pfd.cColorBits<=8) {
           // cerr << "skipping GL pixfmt[" << pfnum << "] due to cColorBits<8" << endl;
           continue;
        }

        // need z buffer for TT (but not stencil)
        if(pfd.cDepthBits==0) {
           // cerr << "skipping GL pixfmt[" << pfnum << "] due to depthbits==0" << endl;
           continue;
        }

        DWORD dwReqFlags=(PFD_SUPPORT_OPENGL | PFD_DRAW_TO_WINDOW | PFD_DOUBLEBUFFER);

        if((pfd.dwFlags & dwReqFlags)!=dwReqFlags) {
           // cerr << "skipping GL pixfmt[" << pfnum << "] due to missing flags, pfd.flags=0x" << (void*)pfd.dwFlags<< endl;
           continue;
        }

        // we've passed all the tests, go ahead and pick this fmt
        // note: could go continue looping looking for more alpha bits or more depth bits
        // so this would pick 16bpp depth buffer, probably not 24bpp

        break;
    }

    ReleaseDC(hWnd,winDC);

    if(pfnum>MaxPixFmtNum) {
        // mustve set this mode manually?
        cerr << "Error: OGL mode set, but detected no OpenGL hardware support!\n";
        goto _cleanup;
    }

    // need to get glString info, so must create context and make it current
    // might be cleaner to delay load opengl32.dll

    // Note: this method seems to waste memory because even though we FreeLib(opengl32),
    //       the OGL driver dll (e.g. nvoglnt.dll) seems to stay loaded.

    /* glGetString will always fail unless you must create a wglContext and make it current.
    only way I can think of to get info w/o creation is to use the OpenGLDrivers regkey to get driver dllname
    (e.g. nvoglnt.dll) and call glGetString directly on that dll, but I dont know how gdi picks which one of the keys
    under OpenGLDrivers\ it uses.

     // Note:  if opengl32.dll is not loaded statically or dynamically, DescribePixelFormat will fail with
     //        ERROR_MOD_NOT_FOUND on win9x

    */

    // dont static link ogl, save memory
    typedef HGLRC (WINAPI *WGLCREATECONTEXTPROC)(HDC);
    const char *pWGLCCStr="wglCreateContext";
    WGLCREATECONTEXTPROC pWglCreateContext = (WGLCREATECONTEXTPROC) GetProcAddress(hOGL, pWGLCCStr);
    if (NULL == pWglCreateContext) {
        cerr << "Error: GetProcAddr failed for " << pWGLCCStr << ", err=" << GetLastError() << endl;
        goto _cleanup;
    }
    typedef BOOL (WINAPI *WGLDELETECONTEXTPROC)(HGLRC);
    const char *pWGLDelCStr="wglDeleteContext";
    WGLDELETECONTEXTPROC pWglDeleteContext = (WGLDELETECONTEXTPROC) GetProcAddress(hOGL, pWGLDelCStr);
    if (NULL == pWglDeleteContext) {
        cerr << "Error: GetProcAddr failed for " << pWGLDelCStr << ", err=" << GetLastError() << endl;
        goto _cleanup;
    }
    typedef BOOL  (WINAPI *WGLMAKECURRENTPROC)(HDC, HGLRC);
    const char *pWGLMakeCurStr="wglMakeCurrent";
    WGLMAKECURRENTPROC pWglMakeCurrent = (WGLMAKECURRENTPROC) GetProcAddress(hOGL, pWGLMakeCurStr);
    if (NULL == pWglMakeCurrent) {
        cerr << "Error: GetProcAddr failed for " << pWGLMakeCurStr << ", err=" << GetLastError() << endl;
        goto _cleanup;
    }
    typedef const GLubyte * (WINAPI *GLGETSTRINGPROC)(GLenum name);
    const char *pGLGetStr="glGetString";
    GLGETSTRINGPROC pGlGetString = (GLGETSTRINGPROC) GetProcAddress(hOGL, pGLGetStr);
    if (NULL == pGlGetString) {
        cerr << "Error: GetProcAddr failed for " << pGLGetStr << ", err=" << GetLastError() << endl;
        goto _cleanup;
    }

    // for glGetString to work, we must create a window and do wglMakeCurrent()

    HDC hOGLWinDC=NULL;
    HWND hOGLWnd = CreateOpenGLWindow("opengl_testwindow",pfnum,&pfd,1,1,1,1,0,0x0,&hOGLWinDC);
    if(!hOGLWnd) {
        cerr << "Error: failed to create OGL test window!\n";
        goto _cleanup;
    }

    HGLRC hRC = (*pWglCreateContext)(hOGLWinDC);
    if(hRC==NULL) {
        cerr << "Error: wglCreateContext failed, err=" << GetLastError() << endl;
        goto _wndcleanup;
    }
    BOOL ret=(*pWglMakeCurrent)(hOGLWinDC, hRC);
    if(!ret) {
        cerr << "Error: wglMakeCurrent failed, err=" << GetLastError() << endl;
        goto _wndcleanup;
    }

    const char *vendStr=(const char *) (*pGlGetString)(GL_VENDOR);
    const char *rendStr=(const char *) (*pGlGetString)(GL_RENDERER);
    const char *versStr=(const char *) (*pGlGetString)(GL_VERSION);


    if(vendStr!=NULL)
       RegSetValueEx(hKeyToontown, "OGLVendor", 0, REG_SZ, (LPBYTE)vendStr, strlen(vendStr));
    if(rendStr!=NULL)
       RegSetValueEx(hKeyToontown, "OGLRenderer", 0, REG_SZ, (LPBYTE)rendStr, strlen(rendStr));
    if(versStr!=NULL)
       RegSetValueEx(hKeyToontown, "OGLVersion", 0, REG_SZ, (LPBYTE)versStr, strlen(versStr));

    /*
    cerr << "GL_VENDOR: "     << _OGLVendorNameStr
      << ", GL_RENDERER: " << _OGLRendererNameStr
      << ", GL_VERSION: "  << _OGLVerStr << endl;
    */

    _wndcleanup:
    if(hRC!=NULL) {
      (*pWglMakeCurrent)(hOGLWinDC, NULL);
      (*pWglDeleteContext)(hRC);
    }
    if(hOGLWinDC!=NULL)
      ReleaseDC(hOGLWnd,hOGLWinDC);    // actually has no effect because of CS_OWNDC flag window was created with
    if(hOGLWnd!=NULL)
      DestroyWindow(hOGLWnd);

    // BUGBUG: need to add stuff to look through all REG_SZ subkeys of
    // (w9x) [HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\OpenGLdrivers]
    // (NT) [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers]
    // (use RegEnumKey, RegEnumValue) and call SearchForDriverInfo on each non-null string,
    // and print out driver date and version for all listed drivers.  you can figure out
    // the one actually in use (at least the manufacturer anyway) from the GL_VENDOR string
    // printed by wglDisplay

  _cleanup:

  if(hOGL)
    FreeLibrary(hOGL);  //leaving it loaded in IE is of no benefit, since panda is a separate process
}
#endif
