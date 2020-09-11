#! /bin/sh
#
# Run this script to generate a new private key and self-signed
# certificate for the in-house ttown2 server.
#

if [ "$1" = "" -o x"$1" = x"-h" ]; then
  echo
  echo "Run this script to generate a new private key and self-signed"
  echo "certificate for the in-house ttown2 server."
  echo 
  echo "One parameter, which is ignored.  (The private key is not"
  echo "encrypted.)"
  echo
  echo "Output:"
  echo '  $TOONTOWN/src/secure/clientagent_ttown2.pem'
  echo '  $TOONTOWN/src/configfiles/ttown.txt'
  echo
  exit 1
fi

cd $TOONTOWN/src/secure || exit

passphrase="$1"

rm -f ttown2.pem ttown2_priv.pem pem.conf

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
CN=ttown2.online.disney.com
emailAddress=toontown@disneyonline.com
EOF

openssl genrsa -out ttown2_priv.pem 1024 || exit
openssl req -config pem.conf -new -x509 -key ttown2_priv.pem -out ttown2.pem -days 1095 || exit

cp ttown2.pem ../configfiles/ttown.txt
rm -f pem.conf

cat ttown2_priv.pem ttown2.pem gameclient.pem >clientagent_ttown2.pem
