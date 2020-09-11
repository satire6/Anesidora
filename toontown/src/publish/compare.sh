#!/bin/sh

PYFILELOC=$TOONTOWN/src/publish
PYFILENAME="compare.py"

cd $TOONTOWN
cvs st | grep "Repository revision" | grep .py | sort > $PYFILELOC/cvsout.txt
cd $OTP
cvs st | grep "Repository revision" | grep .py | sort >> $PYFILELOC/cvsout.txt
cd $DIRECT
cvs st | grep "Repository revision" | grep .py | sort >> $PYFILELOC/cvsout.txt
cd $PYFILELOC

echo "##############################"
echo "Python files in CVS that are not in the filelist and are not __init__.py files or files with AI or UD in them:"
echo "##############################"

python $PYFILENAME $PYFILELOC $TOONTOWN

rm cvsout.txt
