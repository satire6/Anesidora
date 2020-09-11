// Filename: popup.cxx
// Created by:
//
////////////////////////////////////////////////////////////////////

#include "popup.h"
#ifdef USE_DIRECTORY_POPUPMENU
// is this code tested???

#include "pragma.h"
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include <shellapi.h>
#include <string.h>
#include <shlobj.h>
//#include <shfolder.h>
#include <direct.h>

#include <iostream>
using namespace std;

int directoryPopup(const char *defaultDirectory, char *chosenDirectory)
{
  int ret_val = 1;
  LPITEMIDLIST ilist = NULL;
  char fname[MAX_PATH];
  char fpath[MAX_PATH];

  strcpy(chosenDirectory, defaultDirectory);
  make_dir(chosenDirectory);

  // Initialize COM for "apartment" threading model
  CoInitialize(NULL);

  // Instance is Desktop window by default
  HWND desktop = GetDesktopWindow();

  // Call the shell allocator to create buffers
  LPMALLOC lpmalloc;
  if (SHGetMalloc(&lpmalloc) != NOERROR)
  {
    MessageBox(NULL, "SHGetMalloc failed", "directoryPopup error", MB_OK);
    goto _fail;
  }

  // Initialize browse info structure
  BROWSEINFO binfo;
  binfo.hwndOwner = desktop;
  // This is where we can put a default value - I don't know how to create
  // a PIDL structure from a char*, though
  binfo.pidlRoot = NULL;
  binfo.pszDisplayName = fname;
  binfo.lpszTitle = "Please choose where Toontown will be installed.";
  binfo.ulFlags = BIF_EDITBOX | BIF_RETURNONLYFSDIRS;
  binfo.lpfn = NULL;
  binfo.lParam = 0;
  binfo.iImage = 0;

  ilist = SHBrowseForFolder(&binfo);
  if (ilist == NULL)
  {
    MessageBox(NULL, "SHBrowseForFolder failed", "directoryPopup error", MB_OK);
    goto _fail;
  }
  if (FALSE == SHGetPathFromIDList(ilist, fpath))
  {
    MessageBox(NULL, "SHGetPathFromIDList failed", "directoryPopup error", MB_OK);
    goto _fail;
  }
  if (fpath[0] == '\0')
  {
    MessageBox(NULL, "path is null", "directoryPopup error", MB_OK);
    goto _fail;
  }

  // make sure there's a trailing slash
  if (strlen(fpath) > 1)
  {
    if (fpath[strlen(fpath)-1] != '\\')
    {
      strcat(fpath, "\\");
    }
  }
  // add "Toontown\" on the end
  strcat(fpath, "Toontown\\");

  strcpy(chosenDirectory, fpath);
  //make_dir(fpath);

  ret_val = 0;

_fail:
  // Free memory allocated by the shell
  if(ilist) lpmalloc->Free(ilist);
  lpmalloc->Release();

  return ret_val;
}

#endif
