@echo off

set PANDA_STANDALONE=%1
if "%PANDA_STANDALONE%" == "" set PANDA_STANDALONE=I:\beta\toons\maya\panda-standalone

PATH %PANDA_STANDALONE%;%PATH%
set PRC_DIR=%PANDA_STANDALONE%
