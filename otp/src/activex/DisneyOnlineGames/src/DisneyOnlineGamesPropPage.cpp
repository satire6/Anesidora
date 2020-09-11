#include "stdafx.h"
#include "DisneyOnlineGames.h"
#include "DisneyOnlineGamesPropPage.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


IMPLEMENT_DYNCREATE(CDisneyOnlineGamesPropPage, COlePropertyPage)



// Message map

BEGIN_MESSAGE_MAP(CDisneyOnlineGamesPropPage, COlePropertyPage)
END_MESSAGE_MAP()



// Initialize class factory and guid

IMPLEMENT_OLECREATE_EX(CDisneyOnlineGamesPropPage, "DISNEYONLINEGAMES.DisneyOnlineGamesPropPage.1",
	0xe314aa7, 0x9a00, 0x4db3, 0xb0, 0x23, 0x7a, 0xda, 0x8d, 0xdf, 0x7d, 0x26)



// CDisneyOnlineGamesPropPage::CDisneyOnlineGamesPropPageFactory::UpdateRegistry -
// Adds or removes system registry entries for CDisneyOnlineGamesPropPage

BOOL CDisneyOnlineGamesPropPage::CDisneyOnlineGamesPropPageFactory::UpdateRegistry(BOOL bRegister)
{
	if (bRegister)
		return AfxOleRegisterPropertyPageClass(AfxGetInstanceHandle(),
			m_clsid, IDS_DISNEYONLINEGAMES_PPG);
	else
		return AfxOleUnregisterClass(m_clsid, NULL);
}



// CDisneyOnlineGamesPropPage::CDisneyOnlineGamesPropPage - Constructor

CDisneyOnlineGamesPropPage::CDisneyOnlineGamesPropPage() :
	COlePropertyPage(IDD, IDS_DISNEYONLINEGAMES_PPG_CAPTION)
{
}



// CDisneyOnlineGamesPropPage::DoDataExchange - Moves data between page and properties

void CDisneyOnlineGamesPropPage::DoDataExchange(CDataExchange* pDX)
{
	DDP_PostProcessing(pDX);
}



// CDisneyOnlineGamesPropPage message handlers
