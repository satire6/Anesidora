#! /bin/sh
#
# This script generates a suitable playtoken for logging into
# Toontown.  It is intended to aid Toontown developers in debugging
# login issues.
#
# The playtoken includes all of your login information, including
# account name, chat permissions, and whatnot.  It is then encrypted
# with a secret encryption key known only to the OTP server,
# protecting it from access by hackers.
#
# (Note that Pirates does not use exactly the same playtoken form.  It
# uses the DISL login system, which is similar, but just a little bit
# different.)
#
# You may supply this playtoken on the fake-playtoken line in your
# Config.prc file.  With the -u parameter, this script can directly
# update your Config.prc file with the new playtoken.
#
# Options:
#
#   -a "account_name"
#     Specifies the account name to synthesize.  The default is
#     $USERNAME.
#
#   -e "expire_date"
#
#     Specifies the time and date on which the playtoken expires.
#     This should be a format that is understood by the date -d
#     command.  The default is "next year".
#
#   -d "decrypt_token"
#
#     Specifies the secret encryption/decryption key known only to the
#     OTP server.  You can find this in your local.par file, with the
#     line like:
#
#     DECPRYPT_COMMAND=decrypt_token
#
#     It is usually some random string of nonsense characters.
#     Whatever the string is, specify it with the -d parameter.  If
#     you omit this parameter, the playtoken is not encrypted,
#     allowing you to inspect its value directly.
#
#   -u "Config.prc"
#
#     If you name your personal Config.prc file, this script will
#     automatically update it with the generated playtoken.  It will
#     do this by adding a new fake-playtoken line to your Config.prc
#     file.  If you already have a fake-playtoken line, it will
#     replace it with the new playtoken.
#
#     If you omit this parameter, the playtoken is simply printed to
#     standard output, and you can add it to your Config.prc file
#     yourself.
#
#   -p "paid"
#
#     Specify "1" or "0" for paid or unpaid status, respectively.  The
#     default is paid.
#
#   -c "chat"
#
#     Specify "1" or "0" for chat permission or no chat permission,
#     respectively.  The default is 1 for chat permission.
#
#ENDCOMMENT

account="$USERNAME"
expires="next year"
decrypt=""
configrc=""
paid="1"
chat="1"
while getopts a:e:d:u:p:c:h flag
do
  case $flag in
      a)  account="$OPTARG";;
      e)  expires="$OPTARG";;
      d)  decrypt="$OPTARG";;
      u)  configrc="$OPTARG";;
      p)  paid="$OPTARG";;
      c)  chat="$OPTARG";;
      h)  sed '/#ENDCOMMENT/,$d' <$0 >&2; exit 1;;
      \?) exit 1;
  esac
done
shift `expr $OPTIND - 1`

if [ ! -z "$1" ]; then
  sed '/#ENDCOMMENT/,$d' <$0 >&2; exit 1
fi

date=`date -d "$expires" -u '+%a, %d %b %Y %H:%M:%S GMT'`
if [ -z "$date" ]; then
  echo "Invalid expiration date."
  exit 1
fi

playtoken='PlayToken name="'$account'" expires="'$date'" paid="'$paid'" chat="'$chat'" Deployment="" LogEcho="d%3DUS%26name%3D'$account'%26"'

if [ ! -z "$decrypt" ]; then
  playtoken=`echo $playtoken | openssl des3 -salt -pass pass:"$decrypt" -a -A`
fi

if [ -z "$configrc" ]; then
  echo $playtoken

else
  if [ ! -f "$configrc" ]; then
    echo "File not found: $configrc"
    exit 1
  fi

  if grep -s '^#*fake-playtoken' "$configrc" > /dev/null; then
    tmpfile=/tmp/mpt.txt
    rm -f $tmpfile
    sed -e 's:^#*fake-playtoken.*$:fake-playtoken '"$playtoken": "$configrc" >$tmpfile || exit
    mv $tmpfile "$configrc"
  else
    echo "fake-playtoken $playtoken" >> "$configrc"
  fi
fi
  
  
