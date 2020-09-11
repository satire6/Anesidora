#! /bin/sh

# get some environment variable configuration
source ~/player/toontown/src/publish/ttown-build-setup.sh

export ROOT=
# you can control-c past cvs updating
~/player/toontown/src/publish/ttown-cvsupdate-ai.sh $*

# Rebuild dtool
echo "Building dtool"
(cd ~/player/dtool && ppremake && make -j clean install) || exit

# Rebuild panda
echo "Building panda"
(cd ~/player/panda && ppremake && make -j clean-igate clean install) || exit

# Rebuild clean direct
echo "Building direct"
(cd ~/player/direct && ppremake && make -j clean-igate clean install) || exit

# Rebuild clean otp
echo "Building otp"
(cd ~/player/otp && ppremake && make -j clean-igate clean install) || exit

# Rebuild clean toontown
echo "Building toontown"
(cd ~/player/toontown && ppremake && make -j clean-igate clean install) || exit

# Rebuild ttmodels
echo "Building ttmodels"
(cd $PLAYER/ttmodels && ppremake && make -j install-dna) || exit

# generate python code
(cd ~/player && install/bin/genPyCode -nO) || exit

