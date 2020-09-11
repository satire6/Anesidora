#include "stdafx.h"

static  void    dump_env_block (void)
{
    printf ("%s: ENTER\n\n", __FUNCTION__);
    // If a pointer to the environment block for this process was returned
    LPVOID  lpvEnv;
    if (lpvEnv = GetEnvironmentStrings ())
    {
        // Variable strings are separated by NULL byte, and the block is terminated by a NULL byte
        LPTSTR  lpszVariable;
        for (lpszVariable = (LPTSTR)lpvEnv; *lpszVariable; lpszVariable += lstrlen (lpszVariable) + 1)
        {
            printf ("%s\n", lpszVariable);
        }
        // Free the environment block
        FreeEnvironmentStrings ((LPTCH)lpvEnv);
    }
    printf ("%s: LEAVE\n\n", __FUNCTION__);
}

#if defined(_DEBUG)
static  bool    create_process (char *          pszProcessFullPathname,
                                const char *    pszCommandLineArgs = NULL)
{
    CString strCommandLine (pszProcessFullPathname);
    if (pszCommandLineArgs)
    {
        strCommandLine.Append (pszCommandLineArgs);
    }
    // Create security attributes
    SECURITY_DESCRIPTOR     sd;
    InitializeSecurityDescriptor (&sd, SECURITY_DESCRIPTOR_REVISION);
    SetSecurityDescriptorDacl (&sd, TRUE, 0, FALSE);
    SECURITY_ATTRIBUTES     sa  = { sizeof(SECURITY_ATTRIBUTES), &sd, true };
    //
    dump_env_block ();
    //
    // Create child process environment block
    CString strEnvForChildProcess;
    CEnvBlock   EnvBlock ("U2FsdGVkX19W1vR0iRQVBG4VBp%2BW%2FAqGiGri5SHhJQK3NSA3yrMbrKPXp7PpBiQiRR5njCGoyRsK1f6xRlPFqMI3iSk%2B5MhrkZ6ycQOCazyNcKCc9ZtS13MEsia8cKFwjybX6%2F4BV09dGIjB47jHDD5VCs7K6bLxUZXTnLD88OU7v8FeLaI3ds%2B25bzD3k%2FGYFethATY6Fr6P6EsWKlN8FFVkPsD6Rmfm9hsGxK52cBzsZHCsJ%2BvV9Z7GQZqIoV43XwtAOeeIgC%2FeKJZ%2BTdxxWuby3pS4YEAOf2o37d68CeMLZTeQQR2Ul1APEv19erfvBAg%2FT1DXbJH78CEkxe9x99dOsDrb%2BWd91kuDy9baIkEXtFAcP6DMsP%2FUyCoC%2B2taZD5vIBMOuxIUWcdTulB3A%3D%3D");
    EnvBlock.Create ("BobJones", strEnvForChildProcess);
    //
    printf ("%s: About to write strEnvForChildProcess\n\n", __FUNCTION__);
    LPTSTR  lpszVar;
    for (lpszVar = strEnvForChildProcess.GetBuffer (); *lpszVar; lpszVar += lstrlen (lpszVar) + 1)
    {
        printf ("%s\n", lpszVar);
    }
    printf ("%s: Wrote strEnvForChildProcess\n\n", __FUNCTION__);
    //
    // Set startup information
    STARTUPINFO si;
    memset (&si, 0, sizeof (si));
    si.cb           = sizeof (si);
    si.dwFlags      = STARTF_USESHOWWINDOW;
    si.wShowWindow  = SW_SHOWNORMAL;
    // Initialize process information structure
    PROCESS_INFORMATION     pi;
    ZeroMemory (&pi, sizeof (pi));
    // Attempt to run the executable
    if (!CreateProcess (
        NULL,
        strCommandLine.GetBuffer (),
        &sa,
        &sa,
        true,
        0,
        strEnvForChildProcess.GetBuffer (),
        NULL,
        &si,
        &pi))
    {
        return  false;
    }
    return  true;
}
#endif

int main(int argc, char * argv[])
{
    printf ("%s: ENTER\n\n", __FUNCTION__);
#if defined(_DEBUG)
    char szProcessToCreate [] = "Release\\testEnvBlock.exe";
    if (!create_process (szProcessToCreate))
    {
        printf ("Unable to create process \"%s\"", szProcessToCreate);
    }
#else
    dump_env_block ();
#endif
    // Wait for user to read output
    fflush (stdin);
    printf ("\n\nPress ENTER key to exit: ");
    while ('\n' != fgetc (stdin))
    //
    printf ("%s: LEAVE\n\n", __FUNCTION__);
    return  1;
}
