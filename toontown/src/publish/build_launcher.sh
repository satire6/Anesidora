#!/bin/bash
#
# A script to build the Launcher application
# 
# Takes no arguments. Just builds the launcher :)

test "$TLAUNCHER"  || { echo 'Not attached to TLAUNCHER';  exit; }

# determine OS
case `uname` in
  C[yY][gG][wW][iI][nN]*)
	PLATFORM=WIN32;;
  Darwin) 
    PLATFORM=OSX;;
  Linux) 
    PLATFORM=LINUX;;
  *) echo Unknown platform.  Fix the script.; exit 1;;
esac

echo "PLATFORM = " $PLATFORM
echo "DXSDK_DIR = " $DXSDK_DIR


if [ $PLATFORM = WIN32 ]; then
    cd $TLAUNCHER/Launcher1

    # build the launcher. If it fails, set status=failure
    devenv Launcher1.sln /rebuild Toontown || STATUS='failure'

    if [ -z $STATUS ] ; then
        echo "build succeeded"

        echo "compressing launcher executable"
        upx -9 --force `cygpath -m $TLAUNCHER/Launcher1/Toontown/ToontownLauncher.exe`
        
    else
        echo "build failed"

        # cat the log file and strip the html tags
        cat $TLAUNCHER/Launcher1/Toontown/BuildLog.htm | perl -e'while($line=<STDIN>){ $line =~ s/<.+?>//g; print $line; }'

    fi

elif [ $PLATFORM = OSX ]; then
    echo "OSX"
    cd $TLAUNCHER/Launcher-Mac
    xcodebuild -target=Release
else
    echo "unsupported platform. Fix the script."; exit 1;
fi



