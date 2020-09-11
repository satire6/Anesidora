#! /bin/sh

CVS='cvs -q'
SED='/bin/sed /^?.*/d'

# get some environment variable configuration
source ./toontown/src/publish/ttown-build-setup.sh

# Update all trees.  Use supplied command-line parameters as arguments
# to cvs update.
echo ${CVS} ${ROOT} update -dP $* dtool panda direct
echo -n "Updating dtool, panda, and direct "
${CVS} ${ROOT} update -dP $* dtool panda direct | ${SED} || exit

echo "Updating otp"
cd $PLAYER/otp && ${CVS} update -dP $* | ${SED} || exit

echo "Updating toontown"
cd $PLAYER/toontown && ${CVS} update -dP $* | ${SED} || exit

echo "Updating ttmodels"
cd $PLAYER/ttmodels || exit
${CVS} update -dPl $* | ${SED} || exit
${CVS} update -dPl $* src | ${SED} || exit
${CVS} update -dPl $* src/dna | ${SED} || exit
