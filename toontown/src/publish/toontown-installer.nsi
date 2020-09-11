!include "MUI.nsh"
!include LogicLib.nsh
!include FileFunc.nsh
!include "${TOONTOWN}\src\publish\installerLocalization\${LANGUAGE}.nsh"

!insertmacro GetOptions

; HM NIS Edit Wizard helper defines
!define LAUNCHER "ToontownLauncher.exe"

!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\${LAUNCHER}${PRODUCT_RELEASE}"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}${PRODUCT_RELEASE}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PROG_GROUPNAME "${PRODUCT_NAME}${PRODUCT_RELEASE}"

SetCompressor lzma

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!define MUI_WELCOMEPAGE_TITLE_3LINES
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${LICENSE_FILE}" ; EULA
; Directory page
;!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!define MUI_FINISHPAGE_RUN "$INSTDIR\${LAUNCHER}"
;!define MUI_FINISHPAGE_NOAUTOCLOSE ;un-comment to put a pause after the file installation screen
!define MUI_FINISHPAGE_TITLE_3LINES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "${LANGUAGE}"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME}${PRODUCT_VERSION}"
OutFile Toontown-setup${PRODUCT_RELEASE}.exe
InstallDir "$PROGRAMFILES\Disney\Disney Online\ToontownOnline${PRODUCT_RELEASE}"
Icon "${TOONTOWN}\src\publish\toontownInstallerIcon.ico"
UninstallIcon "${TOONTOWN}\src\publish\toontownUninstallIcon.ico"
WindowIcon on
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetShellVarContext all
  SetOutPath "$INSTDIR"
  SetOverwrite ifdiff
  File "${TLAUNCHER}\Launcher1\Toontown\${LAUNCHER}"

!if "${PRODUCT_RELEASE}" == ""
!else 
    File "${TOONTOWN}\src\publish\parameters.txt"
!endif

  CreateDirectory "$SMPROGRAMS\${PROG_GROUPNAME}"
  CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${PRODUCT_NAME_SHORT}.lnk" "$INSTDIR\${LAUNCHER}"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME_SHORT}${PRODUCT_RELEASE}.lnk" "$INSTDIR\${LAUNCHER}"
  
  # Make the directory "$INSTDIR" read write accessible by all users
  AccessControl::GrantOnFile "$INSTDIR" "(BU)" "FullAccess"
    
;  File "..\..\..\path\to\file\Example.file"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${WEBSITE_LINK_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${UNINSTALL_LINK_NAME}.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Launcher1.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${LAUNCHER}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"

# cleanup any previously installed cruft
  RMdir /r "$INSTDIR\maps"
  RMdir /r "$INSTDIR\models"
  RMdir /r "$INSTDIR\phase_3"
  RMdir /r "$INSTDIR\pmockup"
  RMdir /r "$INSTDIR\pmodels"
  RMdir /r "$INSTDIR\toplevel"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "${UNINSTALL_SUCCESS}"
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "${UNINSTALL_CONFIRM}" IDYES +2
  Abort
FunctionEnd

Function .onInstSuccess

  ${GetOptions} $CMDLINE "/DisneyOnlineGamesToken" $R0

  StrLen $0 $R0
    
  ${If} $0 > 0 
     Exec '"$INSTDIR\${LAUNCHER}" "DisneyOnlineGamesToken=$R0"'
  ${Else}
     Exec "$INSTDIR\${LAUNCHER}"
  ${EndIf}

FunctionEnd

Section Uninstall
  SetShellVarContext all

  Delete "$SMPROGRAMS\${PROG_GROUPNAME}\${UNINSTALL_LINK_NAME}.lnk"
  Delete "$SMPROGRAMS\${PROG_GROUPNAME}\${WEBSITE_LINK_NAME}.lnk"
  Delete "$DESKTOP\${PRODUCT_NAME_SHORT}${PRODUCT_RELEASE}.lnk"
  Delete "$SMPROGRAMS\${PROG_GROUPNAME}\${PRODUCT_NAME_SHORT}.lnk"

  RMDir "$SMPROGRAMS\${PROG_GROUPNAME}"
  RMDir /r "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
