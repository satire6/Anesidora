#include "sysinfo.h"
#include "log.h"
#include <string>
#include <malloc.h>
#include <gl/gl.h>
#include <assert.h>

// decided to let configrc.exe get full ogl info instead, because otherwise ogl drvr dll stays loaded in IE,
// and we dont have access to 'useropt' settings anyway, and usually ogl will be user-forced rather than installer-suggested
//#define GET_FULL_OGL_INFO 1


// tests opengl support by opening a new window we can set to ogl fmt
// need to do this for glGetString to work

#ifdef GET_FULL_OGL_INFO
HWND CreateOpenGLWindow(char* title, int pixfmtnum, PIXELFORMATDESCRIPTOR *pPFD, int x, int y, int width, int height, BYTE type, DWORD flags,HDC *pHDC) {
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
            errorLog <<  "GetModuleHandle() failed, err=" << GetLastError() <<endl;
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
            errorLog << "OGL RegisterClass failed, err=" << GetLastError() <<endl;
            // MessageBox(NULL, "RegisterClass() failed: Cannot register window class.", "Error", MB_OK);
            return NULL;
        }
    }

    hWnd = CreateWindow(pOGLWinClassName, title,
            WS_OVERLAPPEDWINDOW | WS_CLIPSIBLINGS | WS_CLIPCHILDREN | WS_DISABLED,
            x, y, width, height, NULL, NULL, hInstance, NULL);

    if(hWnd == NULL) {
        errorLog <<  "CreateWindow failed, err=" << GetLastError() <<endl;
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
        errorLog << "ChoosePixelFormat(" << pf <<") failed, err=" << GetLastError() << endl;
        errorLog << "trying with Pixelformat 1!\n";
        pf = 1;
    }
    */

    SetLastError(0);
    if (SetPixelFormat(*pHDC, pixfmtnum, pPFD) == FALSE) {
        errorLog << "OGL SetPixelFormat(" << pixfmtnum <<") failed, err=" << GetLastError() << endl;
    }
    /*
    else {
        SetLastError(0);
        int numfmts=DescribePixelFormat(hDC, pf, sizeof(PIXELFORMATDESCRIPTOR), &pfd);
        if (numfmts==0 || pfd.cColorBits == 0)
            errorLog << "DescribePixelFormat(" << pf <<") failed - assuming invalid!\n";
    }
    */

    // actually has no effect because of CS_OWNDC
    // ReleaseDC(hWnd, hDC);  caller must release DC now!
    return hWnd;
}
#else
HWND CreateOpenGLWindow(char* title, int pixfmtnum, PIXELFORMATDESCRIPTOR *pPFD, int x, int y, int width, int height, BYTE type, DWORD flags,HDC *hDC) {
    return NULL;
}
#endif

void SysInfo::
Test_OpenGL(void) {
  typedef enum {Software, MCD, ICD} OGLDriverType;
  OGLDriverType drvtype;
//  bool bRet = false;

  if(_OpenGL_status != Status_Unknown) {
     errorLog << "OpenGL status already found to be " << ((_OpenGL_status==Status_Unsupported) ? "un":"") << "supported\n";
     return;
  }

  _OpenGL_status = Status_Unsupported;

/*
  if(pGfx_api_suggested!=NULL)
     *pGfx_api_suggested=GAPI_unknown;

  if(_has_opengl_support!=UnChecked)
    return (_has_opengl_support==Supported);

  _has_opengl_support=Unupported;
*/

  #ifdef FORBID_OPENGL
     errorLog << "Disallowing OpenGL selection for debugging purposes\n";
     return;
  #endif

  PIXELFORMATDESCRIPTOR pfd;
  ZeroMemory(&pfd,sizeof(PIXELFORMATDESCRIPTOR));
  pfd.nSize=sizeof(PIXELFORMATDESCRIPTOR);
  pfd.nVersion=1;

  SetLastError(0);

  // dont want to link statically with opengl32.dll, since wont use it for DX case and it hogs memory,
  // but we need opengl32.dll to be loaded prior to DescribePixFmt
  // doing a LoadLibrary for the extent of this test *should* be the same as linking statically, I hope
  HINSTANCE hOGL = LoadLibrary("opengl32.dll");
  if(!hOGL) {
      errorLog << "LoadLib(opengl32.dll) failed, err" << GetLastError() << endl;
      SetGeneric3DError(NULL);
      return;
  }

  HWND hWnd = 0;  // use DC of desktop window

  HDC winDC = GetDC(hWnd);  // will this fail if not administrator, since we're getting whole desktop DC?
  if(winDC==NULL) {
      errorLog << "Test_OGL: GetDC(0x"<<(void*)hWnd<<") failed, err=" << GetLastError() << endl;
      SetGeneric3DError(NULL);
      return;
  }

  // note we are not switching fullscreen res to final res, so the pixfmt list may not
  // be completely accurate (it will reflect current desktop).

  int pfnum;
  int MaxPixFmtNum=DescribePixelFormat(winDC, 1, sizeof(PIXELFORMATDESCRIPTOR), &pfd);

  if(MaxPixFmtNum==0) {
     errorLog << "failing OGL Check: DescribePixelFormat returns 0, hWnd: 0x" << (void*)hWnd << " hDC: 0x" << (void*)winDC;
     DWORD errnum=GetLastError();
     errorLog << "  GetLastError=";
     if(errnum==ERROR_MOD_NOT_FOUND) {
         // this indicates the opengl32.dll was not loaded.  Most likely reason: linker did not link
         // with opengl32.lib because no gl* fns were called in code (or were eliminated by optimizer)
         // make sure gl[something] is called somewhere
         errorLog << "ERROR_MOD_NOT_FOUND\n";
     } else errorLog << errnum << endl;
  }

  // look for an ICD/MCD pixfmt
  for(pfnum=1;pfnum<=MaxPixFmtNum;pfnum++) {
    DescribePixelFormat(winDC, pfnum, sizeof(PIXELFORMATDESCRIPTOR), &pfd);

    if((pfd.dwFlags & PFD_GENERIC_FORMAT)!=0) {
        drvtype = Software;
        // errorLog << "skipping GL pixfmt[" << pfnum << "] due to SW fmt" << endl;
        continue;
    } else if ( pfd.dwFlags & PFD_GENERIC_ACCELERATED )
        drvtype = MCD;
    else drvtype = ICD;

    if(pfd.iPixelType == PFD_TYPE_COLORINDEX) {
      // errorLog << "skipping GL pixfmt[" << pfnum << "] due to colorindex" << endl;
      continue;
    }

    if(pfd.cColorBits<=8) {
       // errorLog << "skipping GL pixfmt[" << pfnum << "] due to cColorBits<8" << endl;
       continue;
    }

    // need z buffer for TT (but not stencil)
    if(pfd.cDepthBits==0) {
       // errorLog << "skipping GL pixfmt[" << pfnum << "] due to depthbits==0" << endl;
       continue;
    }

    DWORD dwReqFlags=(PFD_SUPPORT_OPENGL | PFD_DRAW_TO_WINDOW | PFD_DOUBLEBUFFER);

    if((pfd.dwFlags & dwReqFlags)!=dwReqFlags) {
       // errorLog << "skipping GL pixfmt[" << pfnum << "] due to missing flags, pfd.flags=0x" << (void*)pfd.dwFlags<< endl;
       continue;
    }

    // we've passed all the tests, go ahead and pick this fmt
    // note: could go continue looping looking for more alpha bits or more depth bits
    // so this would pick 16bpp depth buffer, probably not 24bpp

    break;
  }

  ReleaseDC(hWnd,winDC);
  winDC=NULL;

  if(pfnum<=MaxPixFmtNum) {
     errorLog << "Detected OpenGL hardware support (" << ((drvtype == ICD) ? "ICD" : "MCD") << ")\n";
     _OpenGL_status = Status_Supported;
     //bRet = true;

 #ifdef GET_FULL_OGL_INFO
     // need to get glString info, so must create context and make it current
     // might be cleaner to delay load opengl32.dll

     // Note: this method seems to waste memory because even though we FreeLib(opengl32),
     //       the OGL driver dll (e.g. nvoglnt.dll) seems to stay loaded.  Possible workarounds:
     //       find OGL driver name and unload explictly if still loaded, or do the glGetStrings in configrc.exe
     //       which will not remain in the background while playing game

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
       errorLog << "Error: GetProcAddr failed for " << pWGLCCStr << ", err=" << GetLastError() << endl;
       goto _cleanup;
     }
     typedef BOOL (WINAPI *WGLDELETECONTEXTPROC)(HGLRC);
     const char *pWGLDelCStr="wglDeleteContext";
     WGLDELETECONTEXTPROC pWglDeleteContext = (WGLDELETECONTEXTPROC) GetProcAddress(hOGL, pWGLDelCStr);
     if (NULL == pWglDeleteContext) {
       errorLog << "Error: GetProcAddr failed for " << pWGLDelCStr << ", err=" << GetLastError() << endl;
       goto _cleanup;
     }
     typedef BOOL  (WINAPI *WGLMAKECURRENTPROC)(HDC, HGLRC);
     const char *pWGLMakeCurStr="wglMakeCurrent";
     WGLMAKECURRENTPROC pWglMakeCurrent = (WGLMAKECURRENTPROC) GetProcAddress(hOGL, pWGLMakeCurStr);
     if (NULL == pWglMakeCurrent) {
       errorLog << "Error: GetProcAddr failed for " << pWGLMakeCurStr << ", err=" << GetLastError() << endl;
       goto _cleanup;
     }
     typedef const GLubyte * (WINAPI *GLGETSTRINGPROC)(GLenum name);
     const char *pGLGetStr="glGetString";
     GLGETSTRINGPROC pGlGetString = (GLGETSTRINGPROC) GetProcAddress(hOGL, pGLGetStr);
     if (NULL == pGlGetString) {
       errorLog << "Error: GetProcAddr failed for " << pGLGetStr << ", err=" << GetLastError() << endl;
       goto _cleanup;
     }


     // for glGetString to work, we must create a window and do wglMakeCurrent()

     HDC hOGLWinDC=NULL;
     HWND hOGLWnd = CreateOpenGLWindow("opengl_testwindow",pfnum,&pfd,1,1,1,1,0,0x0,&hOGLWinDC);
     if(!hOGLWnd) {
       errorLog << "Error: failed to create OGL test window!\n";
       goto _cleanup;
     }

     HGLRC hRC = (*pWglCreateContext)(hOGLWinDC);
     if(hRC==NULL) {
       errorLog << "Error: wglCreateContext failed, err=" << GetLastError() << endl;
       goto _wndcleanup;
     }
     BOOL ret=(*pWglMakeCurrent)(hOGLWinDC, hRC);
     if(!ret) {
       errorLog << "Error: wglMakeCurrent failed, err=" << GetLastError() << endl;
       goto _wndcleanup;
     }

     const char *vendStr=(const char *) (*pGlGetString)(GL_VENDOR);
     const char *rendStr=(const char *) (*pGlGetString)(GL_RENDERER);
     const char *versStr=(const char *) (*pGlGetString)(GL_VERSION);

     if(vendStr!=NULL)
         _OGLVendorNameStr = vendStr;
     if(rendStr!=NULL)
         _OGLRendererNameStr = rendStr;
     if(versStr!=NULL)
         _OGLVerStr = versStr;

      errorLog << "GL_VENDOR: "     << _OGLVendorNameStr
               << ", GL_RENDERER: " << _OGLRendererNameStr
               << ", GL_VERSION: "  << _OGLVerStr << endl;

   _wndcleanup:
      if(hRC!=NULL) {
          (*pWglMakeCurrent)(hOGLWinDC, NULL);
          (*pWglDeleteContext)(hRC);
      }
      if(hOGLWinDC!=NULL)
          ReleaseDC(hOGLWnd,hOGLWinDC);    // actually has no effect because of CS_OWNDC flag window was created with
      if(hOGLWnd!=NULL)
          DestroyWindow(hOGLWnd);
     #endif

     // BUGBUG: need to add stuff to look through all REG_SZ subkeys of
     // (w9x) [HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\OpenGLdrivers]
     // (NT) [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers]
     // (use RegEnumKey, RegEnumValue) and call SearchForDriverInfo on each non-null string,
     // and print out driver date and version for all listed drivers.  you can figure out
     // the one actually in use (at least the manufacturer anyway) from the GL_VENDOR string
     // printed by wglDisplay.  maybe this will be unnecessary since we get the driver date from DX

     goto _cleanup;
  } else {
      errorLog << "Found no OpenGL hardware support\n";
  }

  _cleanup:

  if(winDC!=NULL)
     ReleaseDC(hWnd,winDC);

  SAFE_FREELIB(hOGL);  //leaving it loaded in IE is of no benefit, since panda is a separate process

  return;
}
