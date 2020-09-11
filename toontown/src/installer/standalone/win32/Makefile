
#!include <Win32.Mak>

wdig-installer.h wdig-installer_c.c wdig-installer_s.c : wdig-installer.idl wdig-installer.acf
#	midl /nologo /oldnames /Oic /win32 /D_WIN32_DCOM wdig-installer.idl
	midl /nologo /Oic /win32 /D_WIN32_DCOM wdig-installer.idl
#	midl /nologo /Oicf /win32 /D_WIN32_DCOM wdig-installer.idl
