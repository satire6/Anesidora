@echo off

set PANDA_STANDALONE=%1
if "%PANDA_STANDALONE%" == "" (
  set PANDA_STANDALONE=I:/beta/toons/maya/panda-standalone
)

if "%MAYA_LOCATION%" == "" (
  set MAYA_LOCATION=%2
)

rem we will enforce the specific MAYA_LOCATION value, instead of
rem inheriting from the environment.

rem it seems to be important to spell out "Program Files" and not to
rem use the abbreviated form for Maya.
set MAYA_LOCATION=C:/Program Files/Alias/Maya6.0


rem It seems that the default path is now searched even if it is not listed.
rem if "%MAYA_PLUG_IN_PATH%" == "" (
rem  set MAYA_PLUG_IN_PATH=%MAYA_LOCATION%/bin/plug-ins
rem )
set MAYA_PLUG_IN_PATH=%PANDA_STANDALONE%;%MAYA_PLUG_IN_PATH%

call %PANDA_STANDALONE%/setup.bat %PANDA_STANDALONE%
"%MAYA_LOCATION%/bin/maya"
