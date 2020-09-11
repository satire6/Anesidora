#ifndef SYSINFODEFS_H
#define SYSINFODEFS_H

enum CPUType {
	CPU_X86,
	CPU_MIPS,
	CPU_Alpha,
	CPU_PPC,
	CPU_unknown
};

enum OSType {
	OS_unknown,
	OS_Win95,
	OS_Win98,
	OS_WinMe,
	OS_WinNT,   // NT  (must come after win9x stuff, order important)
	OS_Win2000, // Win2000
	OS_WinXP,   // WinXP
	OS_WinXP64, // 64-bit WinXP
	OS_WinServer2003,   // WinXP Server, essentially
	OS_WinServer2003R2,
	OS_WinPostXP,
	OS_WinLonghorn,
    OS_WinVista, 
	OS_WinPostVista,	// newer than WinVista
	OS_XCheetah,	// 10.0.x
	OS_XPuma,		// 10.1.x
	OS_XJaguar,		// 10.2.x
	OS_XPanther,	// 10.3.x
	OS_XTiger,		// 10.4.x
	OS_XLeopard,	// 10.5.x
	OS_XPostLeopard
};

enum GAPIType {
	GAPI_Unknown = 0,
	GAPI_OpenGL,
	GAPI_DirectX_3=3,
	GAPI_DirectX_5=5,
	GAPI_DirectX_6,
	GAPI_DirectX_7,
	GAPI_DirectX_8_0,
	GAPI_DirectX_8_1,
	GAPI_DirectX_9_0,
    GAPI_DirectX_10_0
};

enum CommType {
	C_modem,
	C_network_bridge,
	C_TCPIP_telnet,
	C_RS232,
	C_unspecified,
	C_unknown
};

enum GfxCheckStatus {
	Status_Unknown,
	Status_Unsupported,
	Status_Supported
};

enum GfxVendorIDs {
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
	Trident=0x1023
};

#if 0
// used to index into array of string messages used to communicate with missedReqmts.php
enum GfxCardType {
	Unknown,
	Intel_i810,
	NumCardTypes,
};
#endif

#endif
