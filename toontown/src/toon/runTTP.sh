#! /bin/sh

LD_LIBRARY_PATH=.
export LD_LIBRARY_PATH

PRC_DIR=.
export PRC_DIR

python -c 'import toontown.toon.TopToonPics' -s 0.20 -b FFFFFF -d /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d`

