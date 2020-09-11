!include "MUI.nsh"
!include LogicLib.nsh
!include FileFunc.nsh

; Localization Constants
!define PRODUCT_NAME "Disney Toontown Online ${PRODUCT_RELEASE}"
!define PROG_GROUPNAME "${PRODUCT_NAME}"
!define UNINSTALLER_NAME "uninst"
!define UNINSTALL_LINK_NAME "Uninstall Toontown IE Helper"
!define PRODUCT_WEB_SITE "http://www.toontown.com/"
!define PRODUCT_HELP_LINK "${PRODUCT_WEB_SITE}"

; if there's any language overrides
!if ${LANGUAGE} != ''
!include /NONFATAL "${LANGUAGE}\${LANGUAGE}.nsh"
!endif

;!insertmacro GetOptions

; HM NIS Edit Wizard helper defines
!define PROGRAM "ttinst-helper.exe"
!define PROGRAM_NAME "ttinst-setup${PRODUCT_RELEASE}.exe"

!define PRODUCT_PUBLISHER "Walt Disney Co."

!define WISE_UNINSTALL "UNWISE.EXE"

!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\${PROGRAM_NAME}"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma
RequestExecutionLevel admin
SilentInstall silent

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!define MUI_WELCOMEPAGE_TITLE_3LINES
!insertmacro MUI_PAGE_WELCOME
;!insertmacro MUI_PAGE_LICENSE "${LICENSE_FILE}" ; EULA
; Directory page
;!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!define MUI_FINISHPAGE_RUN "$INSTDIR\${PROGRAM}"
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

Name "${PRODUCT_NAME}"
OutFile ${PROGRAM_NAME}
InstallDir "$PROGRAMFILES\Disney\Disney Online\Toontown${PRODUCT_RELEASE}"
;Icon "${TOONTOWN}\src\publish\piratesInstallerIcon.ico"
;UninstallIcon "${TOONTOWN}\src\publish\piratesUninstallIcon.ico"
WindowIcon on
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetShellVarContext all
  SetOverwrite ifdiff

  SetOutPath "$INSTDIR"
  File "${TOONTOWN}\src\installer\Opt4-Cygwin-${LANGUAGE}\ttinst-helper.exe"
  File "${TOONTOWN}\src\installer\Opt4-Cygwin-${LANGUAGE}\wdigInstallerSvc.exe"

  ;CreateDirectory "$SMPROGRAMS\${PROG_GROUPNAME}"
  ;CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${PRODUCT_NAME_SHORT}.lnk" "$INSTDIR\${PROGRAM}"
  ;CreateShortCut "$DESKTOP\${PRODUCT_NAME_SHORT}${PRODUCT_RELEASE}.lnk" "$INSTDIR\${PROGRAM}"

  # Make the directory "$INSTDIR" read write accessible by all users
  AccessControl::GrantOnFile "$INSTDIR" "Administrators" "FullAccess"
  AccessControl::GrantOnFile "$INSTDIR" "(BU)" "FullAccess"
  ;AccessControl::GrantOnFile "$INSTDIR" "(BU)" "GenericRead + GenericWrite + GenericExecute + AddFile + DeleteChild"
    
SectionEnd

Section -AdditionalIcons
  ;WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  ;CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${WEBSITE_LINK_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  ;CreateShortCut "$SMPROGRAMS\${PROG_GROUPNAME}\${UNINSTALL_LINK_NAME}.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\${UNINSTALLER_NAME}.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\${PROGRAM_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\${UNINSTALLER_NAME}.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${PROGRAM_NAME}"
  ;WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "HelpLink" "${PRODUCT_HELP_LINK}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  ;MessageBox MB_ICONINFORMATION|MB_OK "${UNINSTALL_SUCCESS}"
FunctionEnd

Function un.onInit
  ExecWait "$INSTDIR\${WISE_UNINSTALL}"    ; run WISE uninstaller
;  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "${UNINSTALL_CONFIRM}" IDYES +2
;  Abort
FunctionEnd

Function .onInstSuccess
  Exec "$INSTDIR\${PROGRAM}"    ; run install helper
FunctionEnd

Section Uninstall
  SetShellVarContext all

  Delete "$INSTDIR\ttinst-helper.exe"
  Delete "$INSTDIR\wdigInstallerSvc.exe"
  Delete "$TEMP\${PROGRAM_NAME}"
  Delete "$TEMP\Low\${PROGRAM_NAME}"        ; for Vista

  ;Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"

  ;Delete "$SMPROGRAMS\${PROG_GROUPNAME}\${UNINSTALL_LINK_NAME}.lnk"
  ;Delete "$SMPROGRAMS\${PROG_GROUPNAME}\${PRODUCT_NAME_SHORT}.lnk"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"

  ;Exec "$INSTDIR\${WISE_UNINSTALL}"

  RMDir /r "$LOCALAPPDATA\Disney\Disney Online\Toontown${PRODUCT_RELEASE}"
  ;RMDir "$SMPROGRAMS\${PROG_GROUPNAME}"
  RMDir "$INSTDIR"

  SetAutoClose true
SectionEnd
