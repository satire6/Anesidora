#include "StdAfx.h"

#define INITIAL_NUM_WINDOW_HANDLES          10
#define NUM_WINDOW_HANDLE_ARRAY_INCREMENT   5

CTopLevelWindowIterator::CTopLevelWindowIterator (DWORD dwProcessId)
{
    ZeroMemory (&m, sizeof (m));
    m.dwProcessId   = dwProcessId;
    m.dwNumAlloced  = INITIAL_NUM_WINDOW_HANDLES;
    m.paHWND        = new HWND [m.dwNumAlloced];
}

CTopLevelWindowIterator::~CTopLevelWindowIterator()
{
    delete [] m.paHWND;
}

HWND CTopLevelWindowIterator::First()
{
    // Enumerate all top-level windows
    ::EnumWindows(EnumProc, (LPARAM)this);

    // Reset the HWND array current index
    m.dwCurrIdx = 0;

    // Return the first top level window created by the specified process
    return  Next();
}

HWND CTopLevelWindowIterator::Next()
{
    if (m.paHWND && (m.dwCurrIdx < m.dwNumUsed))
    {
        return  m.paHWND[m.dwCurrIdx++];
    }
    return  NULL;
}

BOOL CALLBACK CTopLevelWindowIterator::EnumProc (HWND hwnd, LPARAM lp)
{
    return  ((CTopLevelWindowIterator*)lp)->OnEnumProc(hwnd);
}

BOOL CTopLevelWindowIterator::OnEnumProc (HWND hwnd)
{
    // If the given top level window is visible
    if (WS_VISIBLE & GetWindowLong (hwnd, GWL_STYLE))
    {
        // Retrieve the identifier of the process that created the given top level window
        DWORD   dwWindowThreadProcessId;
        GetWindowThreadProcessId (hwnd, &dwWindowThreadProcessId);

        // If the given top level window was created by the specified process
        if (dwWindowThreadProcessId == m.dwProcessId)
        {
            if (m.dwNumUsed >= m.dwNumAlloced)
            {
                HWND * paHWND = new HWND [m.dwNumAlloced + NUM_WINDOW_HANDLE_ARRAY_INCREMENT];
                memcpy (paHWND, m.paHWND, sizeof (HWND) * m.dwNumAlloced);
                delete [] m.paHWND;
                m.paHWND = paHWND;
                m.dwNumAlloced += NUM_WINDOW_HANDLE_ARRAY_INCREMENT;
            }
            m.paHWND[m.dwNumUsed++]  = hwnd;
        }
    }
    return  TRUE; // keep looking
}
