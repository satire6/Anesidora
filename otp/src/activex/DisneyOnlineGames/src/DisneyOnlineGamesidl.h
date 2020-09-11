

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


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

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__


#ifndef __DisneyOnlineGamesidl_h__
#define __DisneyOnlineGamesidl_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef ___DDisneyOnlineGames_FWD_DEFINED__
#define ___DDisneyOnlineGames_FWD_DEFINED__
typedef interface _DDisneyOnlineGames _DDisneyOnlineGames;
#endif 	/* ___DDisneyOnlineGames_FWD_DEFINED__ */


#ifndef ___DDisneyOnlineGamesEvents_FWD_DEFINED__
#define ___DDisneyOnlineGamesEvents_FWD_DEFINED__
typedef interface _DDisneyOnlineGamesEvents _DDisneyOnlineGamesEvents;
#endif 	/* ___DDisneyOnlineGamesEvents_FWD_DEFINED__ */


#ifndef __DisneyOnlineGames_FWD_DEFINED__
#define __DisneyOnlineGames_FWD_DEFINED__

#ifdef __cplusplus
typedef class DisneyOnlineGames DisneyOnlineGames;
#else
typedef struct DisneyOnlineGames DisneyOnlineGames;
#endif /* __cplusplus */

#endif 	/* __DisneyOnlineGames_FWD_DEFINED__ */


#ifdef __cplusplus
extern "C"{
#endif 

void * __RPC_USER MIDL_user_allocate(size_t);
void __RPC_USER MIDL_user_free( void * ); 


#ifndef __DisneyOnlineGamesLib_LIBRARY_DEFINED__
#define __DisneyOnlineGamesLib_LIBRARY_DEFINED__

/* library DisneyOnlineGamesLib */
/* [control][helpstring][helpfile][version][uuid] */ 


EXTERN_C const IID LIBID_DisneyOnlineGamesLib;

#ifndef ___DDisneyOnlineGames_DISPINTERFACE_DEFINED__
#define ___DDisneyOnlineGames_DISPINTERFACE_DEFINED__

/* dispinterface _DDisneyOnlineGames */
/* [helpstring][uuid] */ 


EXTERN_C const IID DIID__DDisneyOnlineGames;

#if defined(__cplusplus) && !defined(CINTERFACE)

    MIDL_INTERFACE("33BDF503-F6F7-456C-B3C9-F74F294C8EB7")
    _DDisneyOnlineGames : public IDispatch
    {
    };
    
#else 	/* C style interface */

    typedef struct _DDisneyOnlineGamesVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            _DDisneyOnlineGames * This,
            /* [in] */ REFIID riid,
            /* [iid_is][out] */ void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            _DDisneyOnlineGames * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            _DDisneyOnlineGames * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            _DDisneyOnlineGames * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            _DDisneyOnlineGames * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            _DDisneyOnlineGames * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            _DDisneyOnlineGames * This,
            /* [in] */ DISPID dispIdMember,
            /* [in] */ REFIID riid,
            /* [in] */ LCID lcid,
            /* [in] */ WORD wFlags,
            /* [out][in] */ DISPPARAMS *pDispParams,
            /* [out] */ VARIANT *pVarResult,
            /* [out] */ EXCEPINFO *pExcepInfo,
            /* [out] */ UINT *puArgErr);
        
        END_INTERFACE
    } _DDisneyOnlineGamesVtbl;

    interface _DDisneyOnlineGames
    {
        CONST_VTBL struct _DDisneyOnlineGamesVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define _DDisneyOnlineGames_QueryInterface(This,riid,ppvObject)	\
    (This)->lpVtbl -> QueryInterface(This,riid,ppvObject)

#define _DDisneyOnlineGames_AddRef(This)	\
    (This)->lpVtbl -> AddRef(This)

#define _DDisneyOnlineGames_Release(This)	\
    (This)->lpVtbl -> Release(This)


#define _DDisneyOnlineGames_GetTypeInfoCount(This,pctinfo)	\
    (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo)

#define _DDisneyOnlineGames_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo)

#define _DDisneyOnlineGames_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)

#define _DDisneyOnlineGames_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)

#endif /* COBJMACROS */


#endif 	/* C style interface */


#endif 	/* ___DDisneyOnlineGames_DISPINTERFACE_DEFINED__ */


#ifndef ___DDisneyOnlineGamesEvents_DISPINTERFACE_DEFINED__
#define ___DDisneyOnlineGamesEvents_DISPINTERFACE_DEFINED__

/* dispinterface _DDisneyOnlineGamesEvents */
/* [helpstring][uuid] */ 


EXTERN_C const IID DIID__DDisneyOnlineGamesEvents;

#if defined(__cplusplus) && !defined(CINTERFACE)

    MIDL_INTERFACE("CAC95DCF-C37B-4173-901A-ED2D6EDC5177")
    _DDisneyOnlineGamesEvents : public IDispatch
    {
    };
    
#else 	/* C style interface */

    typedef struct _DDisneyOnlineGamesEventsVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            _DDisneyOnlineGamesEvents * This,
            /* [in] */ REFIID riid,
            /* [iid_is][out] */ void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            _DDisneyOnlineGamesEvents * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            _DDisneyOnlineGamesEvents * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            _DDisneyOnlineGamesEvents * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            _DDisneyOnlineGamesEvents * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            _DDisneyOnlineGamesEvents * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            _DDisneyOnlineGamesEvents * This,
            /* [in] */ DISPID dispIdMember,
            /* [in] */ REFIID riid,
            /* [in] */ LCID lcid,
            /* [in] */ WORD wFlags,
            /* [out][in] */ DISPPARAMS *pDispParams,
            /* [out] */ VARIANT *pVarResult,
            /* [out] */ EXCEPINFO *pExcepInfo,
            /* [out] */ UINT *puArgErr);
        
        END_INTERFACE
    } _DDisneyOnlineGamesEventsVtbl;

    interface _DDisneyOnlineGamesEvents
    {
        CONST_VTBL struct _DDisneyOnlineGamesEventsVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define _DDisneyOnlineGamesEvents_QueryInterface(This,riid,ppvObject)	\
    (This)->lpVtbl -> QueryInterface(This,riid,ppvObject)

#define _DDisneyOnlineGamesEvents_AddRef(This)	\
    (This)->lpVtbl -> AddRef(This)

#define _DDisneyOnlineGamesEvents_Release(This)	\
    (This)->lpVtbl -> Release(This)


#define _DDisneyOnlineGamesEvents_GetTypeInfoCount(This,pctinfo)	\
    (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo)

#define _DDisneyOnlineGamesEvents_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo)

#define _DDisneyOnlineGamesEvents_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)

#define _DDisneyOnlineGamesEvents_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)

#endif /* COBJMACROS */


#endif 	/* C style interface */


#endif 	/* ___DDisneyOnlineGamesEvents_DISPINTERFACE_DEFINED__ */


EXTERN_C const CLSID CLSID_DisneyOnlineGames;

#ifdef __cplusplus

class DECLSPEC_UUID("3DCEC959-378A-4922-AD7E-FD5C925D927F")
DisneyOnlineGames;
#endif
#endif /* __DisneyOnlineGamesLib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


