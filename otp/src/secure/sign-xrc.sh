#! /bin/sh
#
# Run this script to digitally sign an xrc file for runtime authentication.
#

if [ x"$1" = x"" -o x"$1" = x"-h" ]; then
  echo
  echo "Run this script to digitally sign an xrc file for runtime "
  echo "authentication.  This generates a file named xrc.sig which "
  echo "must be present and correspond to the xrc file and to the current "
  echo 'xrc key in $OTP/src/secure in order for the contents '
  echo "of the xrc file to be respected."
  echo 
  echo "Usage:"
  echo "  sign-xrc.sh xrc  (to sign a particular xrc file by name)"
  echo "  sign-xrc.sh -l   (to sign the xrc file in the live directory)"
  echo "  sign-xrc.sh -t   (to sign the xrc file in the test directory)"
  echo
  exit 1
fi

case `uname` in
  Linux) PLATFORM=LINUX;;
  Darwin) PLATFORM=OSX;;
  Cygwin*) PLATFORM=WIN32;;
  CYGWIN*) PLATFORM=WIN32;;
esac

case $LANGUAGE in
  castillian)
    LIVESUFFIX=_ES ;;
  french)
    LIVESUFFIX=_FR ;;
esac

if [ "$PLATFORM" = "WIN32" ]; then
  LIVEBASE="/c/Program Files/Disney/Disney Online/Toontown${LIVESUFFIX}"
  TESTBASE="/c/Program Files/Disney/Disney Online/ToontownTest"
elif [ $PLATFORM = "OSX" ]; then
  LIVEBASE=~/"Library/Application Support/WDIG/ToontownClient.bundle/Contents/MacOS"
  TESTBASE=~/"Library/Application Support/WDIG/TestToontownClient.bundle/Contents/MacOS"
fi

xrc=$1
if [ x"$xrc" = x"-l" ]; then
  xrc="$LIVEBASE/xrc"
elif [ x"$xrc" = x"-t" ]; then
  xrc="$TESTBASE/xrc"
fi

echo "signing $xrc"
rm -f ds.md5
check_md5 -b ds.md5 "$xrc" || exit
openssl rsautl -sign -in ds.md5 -inkey $OTP/src/secure/xrc_priv.pem -out "$xrc.sig" || exit
rm -f ds.md5

