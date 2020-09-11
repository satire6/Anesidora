#include "stdafx.h"
#include "DisneyOnlineGames.h"
#include "DisneyOnlineGamesCtrl.h"
#include "DisneyOnlineGamesPropPage.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

IMPLEMENT_DYNCREATE(CDisneyOnlineGamesCtrl, COleControl)

// Message map

BEGIN_MESSAGE_MAP(CDisneyOnlineGamesCtrl, COleControl)
	ON_OLEVERB(AFX_IDS_VERB_EDIT, OnEdit)
	ON_OLEVERB(AFX_IDS_VERB_PROPERTIES, OnProperties)
END_MESSAGE_MAP()

// Dispatch map

BEGIN_DISPATCH_MAP(CDisneyOnlineGamesCtrl, COleControl)
    DISP_PROPERTY_NOTIFY_ID(CDisneyOnlineGamesCtrl, "ModeId",    dispidModeId,    m_ModeId,    OnModeIdChanged,    VT_BSTR)
    DISP_FUNCTION_ID(CDisneyOnlineGamesCtrl, "runPiratesOnline", dispidrunPiratesOnline, exportedmethodrunPiratesOnline, VT_EMPTY, VTS_NONE)
    DISP_PROPERTY_NOTIFY_ID(CDisneyOnlineGamesCtrl, "ResponseCode", dispidResponseCode, m_ResponseCode, OnResponseCodeChanged, VT_UI4)
    DISP_PROPERTY_NOTIFY_ID(CDisneyOnlineGamesCtrl, "Token", dispidToken, m_Token, OnTokenChanged, VT_BSTR)
END_DISPATCH_MAP()

// Event map

BEGIN_EVENT_MAP(CDisneyOnlineGamesCtrl, COleControl)
    EVENT_CUSTOM_ID("onRunPiratesOnlineComplete", eventidonRunPiratesOnlineComplete, Fire_onRunPiratesOnlineComplete, VTS_NONE)
END_EVENT_MAP()

// Property pages

// TODO: Add more property pages as needed.  Remember to increase the count!
BEGIN_PROPPAGEIDS(CDisneyOnlineGamesCtrl, 1)
	PROPPAGEID(CDisneyOnlineGamesPropPage::guid)
END_PROPPAGEIDS(CDisneyOnlineGamesCtrl)

// Initialize class factory and guid

IMPLEMENT_OLECREATE_EX(CDisneyOnlineGamesCtrl, "DISNEYONLINEGAMES.DisneyOnlineGamesCtrl.1",
	0x3dcec959, 0x378a, 0x4922, 0xad, 0x7e, 0xfd, 0x5c, 0x92, 0x5d, 0x92, 0x7f)

// Type library ID and version

IMPLEMENT_OLETYPELIB(CDisneyOnlineGamesCtrl, _tlid, _wVerMajor, _wVerMinor)

// Interface IDs

const IID BASED_CODE IID_DDisneyOnlineGames =
		{ 0x33BDF503, 0xF6F7, 0x456C, { 0xB3, 0xC9, 0xF7, 0x4F, 0x29, 0x4C, 0x8E, 0xB7 } };
const IID BASED_CODE IID_DDisneyOnlineGamesEvents =
		{ 0xCAC95DCF, 0xC37B, 0x4173, { 0x90, 0x1A, 0xED, 0x2D, 0x6E, 0xDC, 0x51, 0x77 } };

// Control type information

static const DWORD BASED_CODE _dwDisneyOnlineGamesOleMisc =
    OLEMISC_ALWAYSRUN |
	OLEMISC_SETCLIENTSITEFIRST |
    OLEMISC_INSIDEOUT |
    OLEMISC_CANTLINKINSIDE |
    OLEMISC_ACTIVATEWHENVISIBLE
    ;

IMPLEMENT_OLECTLTYPE(CDisneyOnlineGamesCtrl, IDS_DISNEYONLINEGAMES, _dwDisneyOnlineGamesOleMisc)

// CDisneyOnlineGamesCtrl::CDisneyOnlineGamesCtrlFactory::UpdateRegistry -
// Adds or removes system registry entries for CDisneyOnlineGamesCtrl

BOOL CDisneyOnlineGamesCtrl::CDisneyOnlineGamesCtrlFactory::UpdateRegistry(BOOL bRegister)
{
	// TODO: Verify that your control follows apartment-model threading rules.
	// Refer to MFC TechNote 64 for more information.
	// If your control does not conform to the apartment-model rules, then
	// you must modify the code below, changing the 6th parameter from
	// afxRegInsertable | afxRegApartmentThreading to afxRegInsertable.

	if (bRegister)
		return AfxOleRegisterControlClass(
			AfxGetInstanceHandle(),
			m_clsid,
			m_lpszProgID,
			IDS_DISNEYONLINEGAMES,
			IDB_DISNEYONLINEGAMES,
			afxRegInsertable | afxRegApartmentThreading | afxRegFreeThreading,
			_dwDisneyOnlineGamesOleMisc,
			_tlid,
			_wVerMajor,
			_wVerMinor);
	else
		return AfxOleUnregisterClass(m_clsid, m_lpszProgID);
}

// CDisneyOnlineGamesCtrl::CDisneyOnlineGamesCtrl - Constructor

CDisneyOnlineGamesCtrl::CDisneyOnlineGamesCtrl()
{
	InitializeIIDs(&IID_DDisneyOnlineGames, &IID_DDisneyOnlineGamesEvents);
}

// CDisneyOnlineGamesCtrl::~CDisneyOnlineGamesCtrl - Destructor

CDisneyOnlineGamesCtrl::~CDisneyOnlineGamesCtrl()
{
	// TODO: Cleanup your control's instance data here.
}

// CDisneyOnlineGamesCtrl::OnDraw - Drawing function

void CDisneyOnlineGamesCtrl::OnDraw(
			CDC* pdc, const CRect& rcBounds, const CRect& rcInvalid)
{
	if (!pdc)
		return;
}

// CDisneyOnlineGamesCtrl::DoPropExchange - Persistence support

void CDisneyOnlineGamesCtrl::DoPropExchange(CPropExchange* pPX)
{
	ExchangeVersion(pPX, MAKELONG(_wVerMinor, _wVerMajor));
	COleControl::DoPropExchange(pPX);

	// TODO: Call PX_ functions for each persistent custom property.
}

// CDisneyOnlineGamesCtrl::GetControlFlags -
// Flags to customize MFC's implementation of ActiveX controls.
//
DWORD CDisneyOnlineGamesCtrl::GetControlFlags()
{
	DWORD dwFlags = COleControl::GetControlFlags();
	return dwFlags;
}

// CDisneyOnlineGamesCtrl::OnResetState - Reset control to default state

void CDisneyOnlineGamesCtrl::OnResetState()
{
	COleControl::OnResetState();  // Resets defaults found in DoPropExchange

	// TODO: Reset any other control state here.
}

// CDisneyOnlineGamesCtrl message handlers

void CDisneyOnlineGamesCtrl::OnModeIdChanged(void)
{
    AFX_MANAGE_STATE(AfxGetStaticModuleState());

    // TODO: Add your property handler code here

    SetModifiedFlag();
}

void CDisneyOnlineGamesCtrl::exportedmethodrunPiratesOnline (void)
{
    AFX_MANAGE_STATE(AfxGetStaticModuleState());

#if defined(_DEBUG_TOKEN_VALUE_)
    {
        // If the request to obtain the path to temporary directory failed
        char    szTempPath  [MAX_PATH];
        if (GetTempPath (MAX_PATH, szTempPath))
        {
            // If the request to obtain a unique temporary filename failed
            char    szInstallerFullPathname  [MAX_PATH];
            if (GetTempFileName (szTempPath, NULL, 0, szInstallerFullPathname))
            {
                // If the temporary file was not successfully opened for writing
                HANDLE  hFile;
                if (INVALID_HANDLE_VALUE != (hFile = CreateFile (
                    szInstallerFullPathname,
                    GENERIC_WRITE,
                    0,
                    NULL,
                    CREATE_ALWAYS,
                    FILE_ATTRIBUTE_NORMAL,
                    NULL
                   )))
                {
                    char   szPrefix [] = "m_Token=\"";
                    char   szSuffix [] = "\"";
                    char * pszBuf = (char *)malloc (lstrlen (szPrefix) + lstrlen (m_Token) + lstrlen (szSuffix) + 1);
                    strcpy (pszBuf, szPrefix);
                    strcat (pszBuf, m_Token);
                    strcat (pszBuf, szSuffix);
                    //
                    DWORD   dwNumberOfBytesWritten;
                    WriteFile (hFile, pszBuf, lstrlen (pszBuf), &dwNumberOfBytesWritten, NULL);
                    //
                    CloseHandle (hFile);
                }
            }
        }
    }
#endif

    CRunPiratesOnline * pRunPiratesOnline   = new CRunPiratesOnline ();
    m_ResponseCode  = pRunPiratesOnline->Run (atoi (m_ModeId), m_Token);
    delete  pRunPiratesOnline;

    // If our attempt to run Pirates Online was successful
    if (RESPONSE_CODE__SUCCESS == m_ResponseCode)
    {
        CTopLevelWindowIterator     itlw (GetCurrentProcessId ());
        for (HWND hWndTopLevelWindow = itlw.First(); hWndTopLevelWindow; hWndTopLevelWindow = itlw.Next())
        {
            // Minimize the top level window that was created by this process
            ::ShowWindow (hWndTopLevelWindow, SW_MINIMIZE);
        }
    }

    // Fire response to webpage
    Fire_onRunPiratesOnlineComplete ();
}

void CDisneyOnlineGamesCtrl::OnResponseCodeChanged(void)
{
    AFX_MANAGE_STATE(AfxGetStaticModuleState());

    // TODO: Add your property handler code here

    SetModifiedFlag();
}

void CDisneyOnlineGamesCtrl::OnTokenChanged(void)
{
    AFX_MANAGE_STATE(AfxGetStaticModuleState());

    // TODO: Add your property handler code here

    SetModifiedFlag();
}
