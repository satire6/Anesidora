#! /bin/sh
#
# Run this script to generate a new public and private key pair for
# authenticating xrc files.
#

if [ x"$1" = x"-h" ]; then
  echo
  echo "Run this script to generate a new public and private key pair"
  echo "for authenticating xrc files."
  echo 
  echo "Output:"
  echo '  $OTP/src/secure/xrc_priv.pem'
  echo '  $OTP/src/configfiles/key_src.c'
  echo
  exit 1
fi

cd $OTP/src/secure || exit

openssl genrsa -out xrc_priv.pem 1024 || exit
openssl rsa -in xrc_priv.pem -pubout -outform DER -out xrc_pub.bin || exit
bin2c -static -o $OTP/src/configrc/key_src.cxx -n pubkey xrc_pub.bin || exit
rm -f xrc_pub.bin
