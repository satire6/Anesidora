# This file will be installed on the client as
# $PANDA3D_ROOT/Config.pre.  It specifies most of the runtime config
# variables appropriate to run Toontown on the client machine (a few
# more platform-specific settings may be added explicitly within
# toontown.pdef).

# You may edit this file to add any runtime settings needed for
# Toontown game clients.

load-display pandadx9
aux-display pandadx9
aux-display pandadx8
aux-display pandagl
aux-display tinydisplay

# constant config settings
cull-bin gui-popup 60 unsorted

# We take advantage of the render2dp scene graph for things layered on
# top of everything else.
want-render2dp 1

# International characters are represented internally using the utf8
# encoding.
text-encoding utf8

# We don't want DirectEntries to return unicode strings for now.
direct-wtext 0

# Don't break a line before the following punctuation marks (including
# some Japanese punctuation marks).
text-never-break-before ,.-:?!;。？！、

# This enables in-game IME (e.g. for Japanese clients)
ime-aware 1
ime-hide 1

# Make sure textures are forced to a power-of-2 size by default, as a
# convenience.
textures-power-2 down

# This enables checking the clock against the time-of-day clock,
# mainly useful for defeating programs like Speed Gear.
paranoid-clock 1

# Set the process affinity to CPU 0 for performance reasons, and to avoid
# the QueryPerformanceCounter bug.
lock-to-one-cpu 1

# Collect consecutive small TCP packets into one big packet to reduce
# network bandwidth (at the cost of latency).  We have this turned
# on here the dev environment mainly to encourage testing of this
# feature.
collect-tcp 1
collect-tcp-interval 0.2

# The ID of the server that we are compatible with
server-version sv1.0.40.25
server-version-suffix 

cull-bin shadow 15 fixed
cull-bin ground 14 fixed 

dc-file $PANDA3D_ROOT/toon.dc
dc-file $PANDA3D_ROOT/otp.dc

plugin-path $PANDA3D_ROOT

window-title Toontown

verify-ssl 0

# For now, restrict SSL communications to the cheaper RC4-MD5
# cipher.  This should lighten the CPU load on the gameserver.
ssl-cipher-list RC4-MD5

# Itemize the SSL certificates we might expect to encounter on our
# servers.
http-preapproved-server-certificate-filename ttown4.online.disney.com:46667 $PANDA3D_ROOT/gameserver.txt


chan-config-sanity-check #f
require-window 0
language english
icon-filename $PANDA3D_ROOT/toontown.ico

# DirectX 9: DirectX will manage textures, but not vertex and index buffers
dx-management 1

tt-specific-login 1

# downloader settings
decompressor-buffer-size 32768
extractor-buffer-size 32768
patcher-buffer-size 512000
downloader-timeout 15
downloader-timeout-retries 4
downloader-disk-write-frequency 4
downloader-byte-rate 125000
downloader-frequency 0.1

# Display settings

load-display pandadx9
aux-display pandadx9
aux-display pandadx8
aux-display pandagl
aux-display tinydisplay
win-size 800 600
fullscreen #t

# loader settings
load-file-type toontown
compress-channels #t
display-lists 0

early-random-seed 1
ssl-cipher-list RC4-MD5
respect-prev-transform 1

# notify settings
notify-level-collide warning
notify-level-chan warning
notify-level-gobj warning
notify-level-loader warning
notify-timestamp #t

default-model-extension .bam

decompressor-step-time 0.5
extractor-step-time 0.5

# Server version
required-login playToken
server-failover 80 443
want-fog #t
dx-use-rangebased-fog #t
aspect-ratio 1.333333
on-screen-debug-font ImpressBT.ttf
temp-hpr-fix 1
vertex-buffers 0
dx-broken-max-index 1
vfs-case-sensitive 0
inactivity-timeout 180

# This keeps the joint hierarchies for the different LOD's of an Actor
# separate.  Seems to be necessary for the Toons--some of the naked
# Toons seem to have slightly different skeletons for the different
# LOD's.
merge-lod-bundles 0

# Need to turn on this option to support our broken door triggers.
early-event-sphere 1

# Need to turn this on to avoid jerky movement, pirates copes with it differently
accept-clock-skew 1

# Keep the frame rate from going too ridiculously high.  This is
# mainly an issue when the video driver doesn't support video sync.
# Limiting the frame rate helps out some of the collision issues
# that you get with a too-high frame rate (some of our trigger
# planes require a certain amount of interpenetration to be
# triggered), and is also just a polite thing to do in general.
clock-mode limited
clock-frame-rate 120

# Not using parasite_buffer to speed things up in places where
# creating this buffer seems to cause frame rate issues such
# as the Photo Fun game.
prefer-parasite-buffer 0

# This is client side IGN
# news-over-http 0
# news-base-dir phase_3.5/models/news/
# news-index-filename news_index.txt

# This is IGN over HTTP, going LIVE 6/2/2010 - dlo
news-over-http 1
news-base-dir /httpNews
news-index-filename http_news_index.txt

# This is now on by default.  Will be removed in next publish - dlo 05/24/2010
# want-new-toonhall 1

audio-library-name miles_audio

cursor-filename $PANDA3D_ROOT/toonmono.cur

#
# audio related options
#

# load the loaders
audio-loader mp3
audio-loader midi
audio-loader wav
audio-software-midi #t

# turn sfx on
audio-sfx-active #t
# turn music on
audio-music-active #t

audio-master-sfx-volume 1
audio-master-music-volume 1

#
# display resolution
#

#
# server type
#

server-type prod
