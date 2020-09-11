#!/bin/sh

INSTALLERDIR=$TOONTOWN/src/installer
OBJDIR=Opt4-Cygwin-${LANGUAGE}
TARGETDIR=$INSTALLERDIR/$OBJDIR

#FILES="$TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-portuguese.cab $TOONTOWN/src/installer/service/win32/Debug/ttinst_helper.exe $TOONTOWN/src/installer/standalone/win32/Debug/tt-installer.exe"
#FILES="$TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-portuguese.cab $TOONTOWN/src/installer/service/win32/Release/ttinst_helper.exe $TOONTOWN/src/installer/standalone/win32/Release/tt-installer.exe"

#FILES="$TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-portuguese.cab $TOONTOWN/src/installer/standalone/win32/Debug/ttinst-helper.exe $TOONTOWN/src/installer/service/win32/Debug/wdigInstallerSvc.exe"
#FILES="$TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-portuguese.cab $TOONTOWN/src/installer/standalone/win32/Release/ttinst-helper.exe $TOONTOWN/src/installer/service/win32/Release/wdigInstallerSvc.exe"

#FILES="$TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-portuguese.cab $TOONTOWN/src/installer/Opt4-Cygwin-portuguese/ttinst-helper.exe $TOONTOWN/src/installer/Opt4-Cygwin-portuguese/wdigInstallerSvc.exe"

FILES="$TARGETDIR/ttinst-${LANGUAGE}.cab $TARGETDIR/ttinst-setup_*.exe $TARGETDIR/bootstrap.db"

#echo $FILES

if [ $LANGUAGE = 'japanese' ]; then
TUSER=toonjp
TSERIES=2200
elif [ $LANGUAGE = 'portuguese' ]; then
TUSER=toonbr
TSERIES=2400
elif [ $LANGUAGE = 'french' ]; then
TUSER=toonfr
TSERIES=2500
fi

scp $FILES $TUSER@ttown2:/toontown/$TSERIES/download/$LANGUAGE/currentVersion/
