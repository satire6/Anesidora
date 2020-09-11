

/* this ALWAYS GENERATED file contains the IIDs and CLSIDs */

/* link this file in with the server and any clients */


 /* File created by MIDL compiler version 6.00.0361 */
/* at Wed Jun 06 15:59:25 2007
 */
/* Compiler settings for .\DisneyOnlineGames.idl:
    Oicf, W1, Zp8, env=Win32 (32b run)
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
//@@MIDL_FILE_HEADING(  )

#if !defined(_M_IA64) && !defined(_M_AMD64)


#pragma warning( disable: 4049 )  /* more than 64k source lines */


#ifdef __cplusplus
extern "C"{
#endif 


#include <rpc.h>
#include <rpcndr.h>

#ifdef _MIDL_USE_GUIDDEF_

#ifndef INITGUID
#define INITGUID
#include <guiddef.h>
#undef INITGUID
#else
#include <guiddef.h>
#endif

#define MIDL_DEFINE_GUID(type,name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8) \
        DEFINE_GUID(name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8)

#else // !_MIDL_USE_GUIDDEF_

#ifndef __IID_DEFINED__
#define __IID_DEFINED__

typedef struct _IID
{
    unsigned long x;
    unsigned short s1;
    unsigned short s2;
    unsigned char  c[8];
} IID;

#endif // __IID_DEFINED__

#ifndef CLSID_DEFINED
#define CLSID_DEFINED
typedef IID CLSID;
#endif // CLSID_DEFINED

#define MIDL_DEFINE_GUID(type,name,l,w1,w2,b1,b2,b3,b4,b5,b6,b7,b8) \
        const type name = {l,w1,w2,{b1,b2,b3,b4,b5,b6,b7,b8}}

#endif !_MIDL_USE_GUIDDEF_

MIDL_DEFINE_GUID(IID, LIBID_DisneyOnlineGamesLib,0x5F6C8F0A,0x6FE5,0x4546,0x82,0xF1,0x9B,0x50,0x37,0x3A,0x8E,0xBD);


MIDL_DEFINE_GUID(IID, DIID__DDisneyOnlineGames,0x33BDF503,0xF6F7,0x456C,0xB3,0xC9,0xF7,0x4F,0x29,0x4C,0x8E,0xB7);


MIDL_DEFINE_GUID(IID, DIID__DDisneyOnlineGamesEvents,0xCAC95DCF,0xC37B,0x4173,0x90,0x1A,0xED,0x2D,0x6E,0xDC,0x51,0x77);


MIDL_DEFINE_GUID(CLSID, CLSID_DisneyOnlineGames,0x3DCEC959,0x378A,0x4922,0xAD,0x7E,0xFD,0x5C,0x92,0x5D,0x92,0x7F);

#undef MIDL_DEFINE_GUID

#ifdef __cplusplus
}
#endif



#endif /* !defined(_M_IA64) && !defined(_M_AMD64)*/

