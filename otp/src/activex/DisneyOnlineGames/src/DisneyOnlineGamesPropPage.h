#pragma once

class CDisneyOnlineGamesPropPage : public COlePropertyPage
{
	DECLARE_DYNCREATE(CDisneyOnlineGamesPropPage)
	DECLARE_OLECREATE_EX(CDisneyOnlineGamesPropPage)

// Constructor
public:
	CDisneyOnlineGamesPropPage();

// Dialog Data
	enum { IDD = IDD_PROPPAGE_DISNEYONLINEGAMES };

// Implementation
protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Message maps
protected:
	DECLARE_MESSAGE_MAP()
};

