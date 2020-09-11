#! /bin/sh
#
# Run this script to generate a new private key and self-signed
# certificate for the live game server.
#

if [ x"$1" = x"" -o x"$1" = x"-h" ]; then
  echo
  echo "Run this script to generate a new private key and self-signed"
  echo "certificate for the live game server."
  echo 
  echo "One parameter: the passphrase with which to encrypt the"
  echo "private key pem file.  This must match the string defined"
  echo "by PRIVATE_KEY_PASSPHRASE= in the toontown.par file."
  echo
  echo "Output:"
  echo '  $TOONTOWN/src/secure/clientagent.pem'
  echo '  $TOONTOWN/src/configfiles/gameserver.txt'
  echo
  exit 1
fi

cd $TOONTOWN/src/secure || exit

passphrase="$1"

rm -f gameserver.pem gameserver_priv.pem pem.conf

cat >pem.conf <<EOF
[ req ]
prompt=no
distinguished_name=req_distinguished_name

[ req_distinguished_name ]
C=US
ST=California
L=North Hollywood
O=Disney Enterprises
OU=WDIG
CN=gameserver.toontown.com
emailAddress=toontown@disneyonline.com
EOF

openssl genrsa -des3 -out gameserver_priv.pem -passout pass:"$passphrase" 1024 || exit
openssl req -config pem.conf -new -x509 -key gameserver_priv.pem -passin pass:"$passphrase" -out gameserver.pem -days 3653 || exit

cp gameserver.pem ../configfiles/gameserver.txt
rm -f pem.conf

cat gameserver_priv.pem gameserver.pem gameclient.pem >clientagent.pem
