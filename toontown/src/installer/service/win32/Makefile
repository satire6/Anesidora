
#!include <Win32.Mak>

installer_service.h installer_service_c.c installer_service_s.c : installer_service.idl installer_service.acf
#	midl /nologo /oldnames /Oic /win32 /D_WIN32_DCOM wdig-installer.idl
	midl /nologo /Oic /win32 /D_WIN32_DCOM installer_service.idl
#	midl /nologo /Oicf /win32 /D_WIN32_DCOM wdig-installer.idl
