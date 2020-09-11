

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 6.00.0361 */
/* at Mon Oct 06 18:44:55 2008
 */
/* Compiler settings for wdig-installer.idl:
    Oic, W1, Zp8, env=Win32 (32b run)
    protocol : dce , ms_ext, c_ext
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
//@@MIDL_FILE_HEADING(  )

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 440
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __wdig2Dinstaller_h__
#define __wdig2Dinstaller_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

/* header files for imported files */
#include "wtypes.h"

#ifdef __cplusplus
extern "C"{
#endif 

void * __RPC_USER MIDL_user_allocate(size_t);
void __RPC_USER MIDL_user_free( void * ); 

#ifndef __IWDIG_InstallerRPC_INTERFACE_DEFINED__
#define __IWDIG_InstallerRPC_INTERFACE_DEFINED__

/* interface IWDIG_InstallerRPC */
/* [explicit_handle][strict_context_handle][unique][version][uuid] */ 

#pragma optimize ("g", off)
typedef unsigned char *STR;

int __stdcall ISRPC_ready( 
    /* [in] */ handle_t IDL_handle);

int __stdcall ISRPC_DoMediumIntegrity( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ int game);

void __stdcall ISRPC_Init( 
    /* [in] */ handle_t IDL_handle);

int __stdcall ISRPC_InitForStatus( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ __int64 hwnd);

int __stdcall ISRPC_InitForRun( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ __int64 hwnd,
    /* [in] */ BSTR bsDeployment,
    /* [in] */ BSTR bsDownloadServer,
    /* [in] */ BSTR bsDownloadVersion);

void __stdcall ISRPC_getValue( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [retval][out] */ BSTR *pVal);

void __stdcall ISRPC_setValue( 
    /* [in] */ handle_t IDL_handle,
    /* [in] */ BSTR key,
    /* [in] */ BSTR val);

void __stdcall ISRPC_RunInstaller( 
    /* [in] */ handle_t IDL_handle);

void __stdcall ISRPC_Shutdown( 
    /* [in] */ handle_t IDL_handle);



extern RPC_IF_HANDLE IWDIG_InstallerRPC_v1_1_c_ifspec;
extern RPC_IF_HANDLE IWDIG_InstallerRPC_v1_1_s_ifspec;
#endif /* __IWDIG_InstallerRPC_INTERFACE_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

unsigned long             __RPC_USER  BSTR_UserSize(     unsigned long *, unsigned long            , BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserMarshal(  unsigned long *, unsigned char *, BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserUnmarshal(unsigned long *, unsigned char *, BSTR * ); 
void                      __RPC_USER  BSTR_UserFree(     unsigned long *, BSTR * ); 

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


