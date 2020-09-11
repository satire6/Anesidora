#pragma once

class CDisneyOnlineGamesCtrl : public COleControl
{
	DECLARE_DYNCREATE(CDisneyOnlineGamesCtrl)

// Constructor
public:
	CDisneyOnlineGamesCtrl();

// Overrides
public:
	virtual void OnDraw(CDC* pdc, const CRect& rcBounds, const CRect& rcInvalid);
	virtual void DoPropExchange(CPropExchange* pPX);
	virtual void OnResetState();
	virtual DWORD GetControlFlags();

// Implementation
protected:
	~CDisneyOnlineGamesCtrl();

	DECLARE_OLECREATE_EX(CDisneyOnlineGamesCtrl)    // Class factory and guid
	DECLARE_OLETYPELIB(CDisneyOnlineGamesCtrl)      // GetTypeInfo
	DECLARE_PROPPAGEIDS(CDisneyOnlineGamesCtrl)     // Property page IDs
	DECLARE_OLECTLTYPE(CDisneyOnlineGamesCtrl)		// Type name and misc status

// Message maps
	DECLARE_MESSAGE_MAP()

// Dispatch maps
	DECLARE_DISPATCH_MAP()

// Event maps
	DECLARE_EVENT_MAP()

// Dispatch and event IDs
public:
	enum {
        dispidToken = 10,
        eventidonRunPiratesOnlineComplete = 1L,
        dispidResponseCode = 9,
        dispidrunPiratesOnline = 5L,
        dispidModeId = 2,
    };
protected:
    void    OnModeIdChanged(void);
    CString m_ModeId;
    void exportedmethodrunPiratesOnline(void);
    void    OnResponseCodeChanged(void);
    ULONG m_ResponseCode;
    void OnTokenChanged(void);
    CString m_Token;

    void Fire_onRunPiratesOnlineComplete(void)
    {
        FireEvent(eventidonRunPiratesOnlineComplete, EVENT_PARAM(VTS_NONE));
    }
};
