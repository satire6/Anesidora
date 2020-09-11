#! /bin/sh

install=~/player/install
export PATH=$PATH:$install/bin
export LD_LIBRARY_PATH=$install/lib
export PYTHONPATH=direct/src/showbase:$install/lib:$install/lib/py

echo $PATH
cd ~/player

autorestart -l log/restart_ai.log ppython toontown/src/ai/AIServiceStart.py --mdip=localhost --mdport=6665 --logpath=log/ --district_number=200000000 --district_name="Kooky_Summit" --ssid=20100000 --min_objid=30000000 --max_objid=39999999
