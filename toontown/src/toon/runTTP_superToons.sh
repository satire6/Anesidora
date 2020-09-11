#! /bin/sh

LD_LIBRARY_PATH=.
export LD_LIBRARY_PATH

PRC_DIR=.
export PRC_DIR

python -c 'import toontown.toon.TopToonPics' -s 0.20 -b FFFFCC -d /event_logs/superToons/

#python TopToonPics.py -s 0.20 -b FFFFCC -d /event_logs/topToonImages/`date -d yesterday +%Y_%m_%d_small`

