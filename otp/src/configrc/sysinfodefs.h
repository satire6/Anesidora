#ifndef SYSINFODEFS_H
#define SYSINFODEFS_H

typedef enum {
    CPU_Intel,
    CPU_MIPS,
    CPU_Alpha,
    CPU_PPC,
    CPU_unknown
  } CPUType;

  typedef enum {
    OS_unknown,
    OS_Win95,
    OS_Win98,
    OS_WinMe,
    OS_WinNT,   // NT  (must come after win9x stuff, order important)
    OS_Win2000, // Win2000
    OS_WinXP,   // WinXP
    OS_WinServer2003,   // WinXP Server, essentially
    OS_WinPostXP, // newer than WinXP
  } OSType;

  typedef enum {
    GAPI_Unknown = 0,
    GAPI_OpenGL     ,
    GAPI_DirectX_3=3,
    GAPI_DirectX_5=5,
    GAPI_DirectX_6,
    GAPI_DirectX_7,
    GAPI_DirectX_8_0,
    GAPI_DirectX_8_1,
    GAPI_DirectX_9_0,
  } GAPIType;

  typedef enum {
    C_modem,
    C_network_bridge,
    C_TCPIP_telnet,
    C_RS232,
    C_unspecified,
    C_unknown
  } CommType;

  typedef enum {
    Status_Unknown,
    Status_Unsupported,
    Status_Supported,
  } GfxCheckStatus;

  typedef enum {
    UnknownVendor=0,
    _3DFX=0x121A,
    _3DLabs=0x3D3D,
    ATI=0x1002,
    Intel=0x8086,
    Matrox=0x102B,
    Nvidia=0x10DE,
    Nvidia_STB=0x12D2,
    PowerVR=0x1023,
    S3=0x5333,
    SiS=0x1039,
    Trident=0x1023,
  } GfxVendorIDs;

#if 0
  // used to index into array of string messages used to communicate with missedReqmts.php
  typedef enum {
    Unknown,
    Intel_i810,
    NumCardTypes,
  } GfxCardType;
#endif

#endif
