#! /bin/sh
#
# Run this script to generate a new private key and self-signed
# certificate for the game client.
#

if [ x"$1" = x"" -o x"$1" = x"-h" ]; then
  echo
  echo "Run this script to generate a new private key and self-signed"
  echo "certificate for the game client."
  echo
  echo "One parameter: the passphrase with which to encrypt the"
  echo "private key pem file.  This must match the string defined"
  echo "within allocateDcFile() in ToontownClientRepository.py."
  echo
  echo "Output:"
  echo '  $TOONTOWN/src/secure/clientCertificate_src.cxx'
  echo '  $TOONTOWN/src/secure/clientCertificate.pem'
  echo
  exit 1
fi

cd $TOONTOWN/src/secure || exit

# The actual passphrase is the hex-encoded md5 of the supplied string.
# This matches what ToontownClientRepository.py does.
passphrase=`check_md5 -i "$1"`

rm -f gameclient_priv.pem pem.conf
rm -f gameclient.pem clientCertificate.pem

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
CN=toontown.com
emailAddress=toontown@disneyonline.com
EOF

openssl genrsa -des3 -out gameclient_priv.pem -passout pass:"$passphrase" 1024 || exit
openssl req -config pem.conf -new -x509 -key gameclient_priv.pem -passin pass:"$passphrase" -out gameclient.pem -days 3653 || exit

cat gameclient_priv.pem gameclient.pem >clientCertificate.pem
rm -f pem.conf

pcompress clientCertificate.pem
bin2c -n client_cert -static -o clientCertificate_src.cxx clientCertificate.pem.pz
rm -f clientCertificate.pem.pz

cat gameserver_priv.pem gameserver.pem gameclient.pem >clientagent.pem
cat ttown2_priv.pem ttown2.pem gameclient.pem >clientagent_ttown2.pem
