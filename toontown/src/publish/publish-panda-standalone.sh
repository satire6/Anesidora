#! /bin/sh

pubdir="$1"

cd `dirname $0` || exit
scriptdir=`pwd`
./make-panda-standalone.sh || exit

if [ "$pubdir" = "" ]; then
  pubdir=/i/beta/toons/maya/panda-standalone

  # If we're making a default publish, also copy the zip file to the
  # standard place.
  cp panda-standalone.zip /i/beta/toons
fi

cd "$pubdir" || exit

unzip -o $scriptdir/panda-standalone.zip || exit
chmod 755 *.exe *.dll *.mll *.bat || exit

