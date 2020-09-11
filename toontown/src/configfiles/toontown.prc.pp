//
// _toontown.prc.pp
//
// This file defines the script to auto-generate _toontown.prc at
// ppremake time.
//

#output 60_toontown.prc notouch
#### Generated automatically by $[PPREMAKE] $[PPREMAKE_VERSION] from $[SOURCEFILE].
################################# DO NOT EDIT ###########################

#if $[CTPROJS]
// If we are using the ctattach tools, append "built"--this is a VR
// Studio convention.
model-path      $TTMODELS/built
sound-path      $TTMODELS/built
#else
// Dave Schuyler sees this.
model-path      $TTMODELS
sound-path      $TTMODELS
#endif

# remove this when we integrate Toontown with the Uberdog
want-uberdog 0

dna-preload    phase_4/dna/storage.dna

load-file-type dna toontown

dc-file $TOONTOWN/src/configfiles/toon.dc

window-title Toontown
#if $[WINDOWS_PLATFORM]
icon-filename phase_3/models/gui/toontown.ico
#else
icon-filename phase_3/models/gui/toontown_mac_icon.rgb
#endif

# Set your game server and port to be localhost
game-server https://localhost:6667

ssl-certificates $OTP/src/configfiles/certificates.txt
ssl-certificates $OTP/src/configfiles/gameserver.txt

# Itemize the SSL certificates we might expect to encounter on our
# account servers.  This protects us from an imposter who happens to
# have his own VeriSign certificate (the imposter's certificate won't
# be from "Disney").
expected-ssl-server /O=Disney Enterprises/OU=WDIG/CN=account.toontown.com
expected-ssl-server /O=Disney Enterprises/OU=WDIG/CN=gameserver.toontown.com

# These two let us also accept the ttown2 certificate.  This is only
# in the dev environment; it doesn't get published.
ssl-certificates $TOONTOWN/src/configfiles/ttown2.txt
expected-ssl-server /O=Disney Enterprises/OU=WDIG/CN=ttown2.online.disney.com

# check that the quests are internally consistent
quest-sanity-check 1

# this causes pupils, etc. to be generated as separate geometry under
# their exposed joints, instead of combined with the rest of the head.
egg-rigid-geometry 1

# Toontown is designed for 4/3 aspect ratio, so let's force it to be so
aspect-ratio 1.333333

# This keeps the joint hierarchies for the different LOD's of an Actor
# separate.  Seems to be necessary for the Toons--some of the naked
# Toons seem to have slightly different skeletons for the different
# LOD's.
merge-lod-bundles 0

# Need to turn on this option to support our broken door triggers.
early-event-sphere 1

# Need to turn this on to avoid jerky movement, pirates copes with it differently
accept-clock-skew 1

# A local directory to store cached news information in dev.  (In
# production, this is set to a subdirectory within the current directory).
news-stage-dir /tmp/news

# But devs don't need to be hitting the news server every time.
news-over-http 0
news-index-filename news_index.txt

#end 60_toontown.prc
