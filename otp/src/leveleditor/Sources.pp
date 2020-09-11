// In the short term, we'll just disable the installation of this
// directory unless you have the ctattach tools in effect (which
// generally indicates that you're a member of the VR Studio).

// Finally, it's moved from DIRECT to OTP

#define BUILD_DIRECTORY $[CTPROJS]

// Install scripts for building zipfiles (leveleditor and RobotToonManager)
#if $[CTPROJS]
  #define INSTALL_SCRIPTS printdir printlib copyfiles copyfiles.pl
#endif

