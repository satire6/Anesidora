#include "stdafx.h"

void    CEnvBlock::insert_env_block_key_value_pair (CString &   strEnvForChildProcess,
                                                            int *       pInsertIdx,
                                                            char *      lpszVariable)
{
    // Insert the next environment block key=value pair, accounting for the following facts:
    //  1. There must be a terminating NULL byte ('\0') between each key=value pair
    //  2. Two NULL bytes indicate environment block end
    //---------------------------------------------------------------------------------------------
    // In other words, an environment block consists of a null-terminated block of null-terminated
    //  strings (meaning there are two null bytes at the end of the block), where each string is of
    //  the form
    //              key=value
    //---------------------------------------------------------------------------------------------
    strEnvForChildProcess.Insert (*pInsertIdx, lpszVariable);
    (*pInsertIdx)   +=  (int)strlen (lpszVariable);
    (*pInsertIdx)++;
    strEnvForChildProcess.GetBufferSetLength (*pInsertIdx);
}

void    CEnvBlock::Create  (const char *    pszEnvKeyToAddToChildProcessEnvBlock,
                            CString &       strEnvForChildProcess)
{
    // Set environment key=value pair that the executable will look for
    static  const char  szEnvKeyValuePairSeparator          []  = "=";
    CString strEnvKeyValuePairToAddToChildProcessEnvBlock;
    strEnvKeyValuePairToAddToChildProcessEnvBlock.Format (
        "%s%s%s",
        pszEnvKeyToAddToChildProcessEnvBlock,
        szEnvKeyValuePairSeparator,
        m.pszToken);
    // Ensure the string to hold the environment block for the child process is empty
    strEnvForChildProcess.GetBufferSetLength (0);
    // Initilize the child process environment block insert index
    int     InsertIdx       = 0;
    // Indicate that the key=value pair that the executable will look for has NOT yet been inserted
    bool    fAddedEnvKeyToChildProcessEnvBlock  = false;
    // If a pointer to the environment block for this process was returned
    LPVOID  lpvEnv;
    if (lpvEnv = GetEnvironmentStrings ())
    {
        // Variable strings are separated by NULL byte, and the block is terminated by a NULL byte
        LPTSTR  lpszVariable;
        for (lpszVariable = (LPTSTR)lpvEnv; *lpszVariable; lpszVariable += lstrlen (lpszVariable) + 1)
        {
            // If the key=value pair that the executable will look for has NOT yet been inserted
            if (!fAddedEnvKeyToChildProcessEnvBlock)
            {
                // If the current key=value pair from this process' environment block is greater
                //  than the key=value pair that the executable will look for
                //---------------------------------------------------------------------------------
                // NOTE: All strings in the environment block must be sorted alphabetically by name.
                //       The sort is case-insensitive, Unicode order, without regard to locale.
                //       Because the equal sign is a separator, it must not be used in the name of
                //          an environment variable.
                //---------------------------------------------------------------------------------
                if (0 > strEnvKeyValuePairToAddToChildProcessEnvBlock.CompareNoCase (lpszVariable))
                {
                    // Indicate that the key=value pair that the executable will look for has been
                    //  inserted into the environment block for the child process
                    fAddedEnvKeyToChildProcessEnvBlock  = true;
                    // Insert the next environment block key=value pair
                    insert_env_block_key_value_pair (
                        strEnvForChildProcess,
                        &InsertIdx,
                        strEnvKeyValuePairToAddToChildProcessEnvBlock.GetBuffer ());
                }
            }
            // Insert the next environment block key=value pair
            insert_env_block_key_value_pair (
                strEnvForChildProcess,
                &InsertIdx,
                lpszVariable);
        }
        // Free the environment block
        FreeEnvironmentStrings ((LPTCH)lpvEnv);
    }
    // If the key=value pair that the executable will look for has NOT yet been inserted
    if (!fAddedEnvKeyToChildProcessEnvBlock)
    {
        // Insert the next environment block key=value pair
        insert_env_block_key_value_pair (
            strEnvForChildProcess,
            &InsertIdx,
            strEnvKeyValuePairToAddToChildProcessEnvBlock.GetBuffer ());
    }
    // Insert the next environment block key=value pair
    insert_env_block_key_value_pair (
        strEnvForChildProcess,
        &InsertIdx,
        "\0");
}

