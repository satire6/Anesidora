#! /bin/bash

scriptdir=`dirname $0`

rm -f panda-standalone.zip

for packageDef in $CTPROJS; do
  packageVar=`echo $packageDef | sed 's/:.*$//'`
  dir=${!packageVar}
  if [ ! -z "$dir" ]; then
    filelist=`\ls $dir/built/lib/*.[md]ll $dir/built/bin/*.exe $dir/built/etc/*.prc 2>/dev/null`
    if [ ! -z "$filelist" ]; then
      zip -j panda-standalone.zip $filelist || exit
    fi
  fi
done

zip -j panda-standalone.zip $WINTOOLS/sdk/python/Python-2.4.1/PCbuild/*.dll || exit

zip -j panda-standalone.zip $scriptdir/standalone.prc || exit

rm -f /tmp/setup.bat /tmp/runmaya.bat
cp $scriptdir/standalone-setup.bat /tmp/setup.bat || exit
zip -j -m panda-standalone.zip /tmp/setup.bat || exit
cp $scriptdir/standalone-runmaya.bat /tmp/runmaya.bat || exit
zip -j -m panda-standalone.zip /tmp/runmaya.bat || exit

echo Success!

