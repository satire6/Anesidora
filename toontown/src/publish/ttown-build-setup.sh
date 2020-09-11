if [ -z "$PLAYER" ]; then
  if [ `uname -i` = "x86_64" ]; then
    PLAYER=`pwd`
  else
    PLAYER=~/player
  fi
  export PLAYER
fi

install=$PLAYER/install
PPREMAKE_CONFIG=$PLAYER/toontown/src/publish/ttown-build-Config.pp
PATH=$PATH:$install/bin:$PLAYER/ppremake
LD_LIBRARY_PATH=$install/lib
PYTHONPATH=$install/lib:$PLAYER

export PPREMAKE_CONFIG
export PATH
export LD_LIBRARY_PATH
export PYTHONPATH
export ETC_PATH

