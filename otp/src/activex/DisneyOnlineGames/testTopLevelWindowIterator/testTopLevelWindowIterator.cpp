#include "stdafx.h"

int main(int argc, char* argv[])
{
    DWORD   dwProcessId = 0;
    CTopLevelWindowIterator itlw (dwProcessId);
    for (HWND hwndTopLevelWindow = itlw.First (); hwndTopLevelWindow; hwndTopLevelWindow = itlw.Next())
    {
        ::ShowWindow (hwndTopLevelWindow, SW_MINIMIZE);
    }
	return  0;
}
