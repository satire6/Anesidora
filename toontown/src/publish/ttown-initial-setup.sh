#! /bin/sh

# set up player directory and check out all trees
mkdir ~/player
cd ~/player || exit

# Get these trees from sourceforge
cvs -d :pserver:anonymous@nit:/cvsroot/panda3d co dtool || exit
cvs -d :pserver:anonymous@nit:/cvsroot/panda3d co panda || exit
cvs -d :pserver:anonymous@nit:/cvsroot/panda3d co direct || exit
cvs -d :pserver:anonymous@nit:/cvsroot/panda3d co ppremake || exit

# Get these trees from dimbo
cvs -d :pserver:anonymous@dimbo:/fit/cvs co otp || exit
cvs -d :pserver:anonymous@dimbo:/fit/cvs co toontown || exit
cvs -d :pserver:anonymous@dimbo:/fit/cvs co ttmodels/src/dna || exit

# get some environment variable configuration
source ~/player/toontown/src/publish/ttown-build-setup.sh

# build and install ppremake
cd ~/player/ppremake || exit
aclocal || exit
autoheader || exit
automake --foreign -a || exit
autoconf || exit
./configure --prefix=$HOME/player/install || exit
make install || exit


# build and install dtool
cd ~/player/dtool || exit
ppremake || exit
make install || exit


# build and install panda
cd ~/player/panda || exit
ppremake || exit
make install || exit


# build and install direct
cd ~/player/direct || exit
ppremake || exit
make install || exit

# build and install otp
cd ~/player/otp || exit
ppremake || exit
make install || exit

# build and install toontown
cd ~/player/toontown || exit
ppremake || exit
make install || exit


# generate python code
cd ~/player || exit
genPyCode install libtoontown || exit


