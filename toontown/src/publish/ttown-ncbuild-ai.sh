#! /bin/sh

# get some environment variable configuration
source ./toontown/src/publish/ttown-build-setup.sh

export ROOT="-d :ext:$1@panda3d.cvs.sourceforge.net:/cvsroot/panda3d"

# you can control-c past cvs updating
$PLAYER/toontown/src/publish/ttown-cvsupdate-ai.sh $2 $3

/usr/bin/find $PLAYER/install \! -name '*.crt' -type f | xargs /bin/rm

# Rebuild dtool
echo "Building dtool"
(cd $PLAYER/dtool && ppremake && make -j install) || exit

# Rebuild panda
echo "Building panda"
(cd $PLAYER/panda && ppremake && make -j install) || exit

# Rebuild direct
echo "Building direct"
(cd $PLAYER/direct && ppremake && make -j install) || exit

# Rebuild otp
echo "Building otp"
(cd $PLAYER/otp && ppremake && make -j install) || exit

# Rebuild toontown
echo "Building toontown"
(cd $PLAYER/toontown && ppremake && make -j install) || exit

# Rebuild ttmodels
echo "Building ttmodels"
(cd $PLAYER/ttmodels && ppremake && make -j install-dna) || exit

# generate python code
(cd $PLAYER && install/bin/genPyCode -nO) || exit

