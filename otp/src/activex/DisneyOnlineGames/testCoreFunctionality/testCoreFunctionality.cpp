#include "stdafx.h"

int _tmain(int argc, _TCHAR* argv[])
{
    CRunPiratesOnline * pRunPiratesOnline   = new CRunPiratesOnline ();
    ULONG   ResponseCode    = pRunPiratesOnline->Run (
        3,
        "UserPassiveToken");
    delete  pRunPiratesOnline;

    // Wait for user to read output
    fflush (stdin);
    printf ("ResponseCode=[%u]\r\n",ResponseCode);
    printf ("Press ENTER key to exit: ");
    while ('\n' != fgetc (stdin))
    //
    return  1;
}
