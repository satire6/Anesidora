#! /bin/sh
#
# Get decrypt_token from your local.par file, in the line:
#
# DECPRYPT_COMMAND=decrypt_token
#
# then pass "decrypt_token", whatever it is, as the second parameter
# to this script.
#
# The third parameter is your Config.prc file; this script will modify
# this file in-place to replace the fake-playtoken line with the newly
# generated playtoken.  If there is no fake-playtoken line already, it
# will add a new one.
#

if [ "$2" = "" ]; then
  echo 'make-playtoken.sh "account name" "decrypt_token" Config.prc'
  exit 1
fi

account="$1"
decrypt="$2"
configrc="$3"
date=`date -d 'next year' -u '+%a, %d %b %Y %H:%M:%S GMT'`

playtoken=`echo 'PlayToken name="'$account'" expires="'$date'" paid="1" chat="1" Deployment="" LogEcho="d%3DUS%26name%3D'$account'%26"' | openssl des3 -salt -pass pass:"$decrypt" -a -A`

if grep -s '^#*fake-playtoken' "$configrc" > /dev/null; then
  tmpfile=/tmp/mpt.txt
  rm -f $tmpfile
  sed -e 's:^#*fake-playtoken.*$:fake-playtoken '"$playtoken": "$configrc" >$tmpfile || exit
  mv $tmpfile "$configrc"
else
  echo "fake-playtoken $playtoken" >> "$configrc"
fi


