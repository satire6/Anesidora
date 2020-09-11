//
// otp.prc.pp
//
// This file defines the script to auto-generate otp.prc at
// ppremake time.
//

#output 50_otp.prc notouch
#### Generated automatically by $[PPREMAKE] $[PPREMAKE_VERSION] from $[notdir $[THISFILENAME]].
################################# DO NOT EDIT ###########################

dc-file $OTP/src/configfiles/otp.dc

# We don't contact any account servers or otherwise in-game, so we
# don't need strict SSL certificate validation--and this makes it easier
# to contact a local gameserver without fussing about certificate names.
verify-ssl 0

# We compress animation files by default.
compress-channels 1

# We take advantage of the render2dp scene graph for things layered on
# top of everything else.
want-render2dp 1

# We would like our developers to use correct case; this is
# particularly important for the publish.  Therefore, we set this
# variable to have Panda insist on the correct case for all of its
# file accesses.
vfs-case-sensitive 1

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

# Let's keep an eye on those messages.
notify-level-clock debug

# Collect consecutive small TCP packets into one big packet to reduce
# network bandwidth (at the cost of latency).  We have this turned
# on here the dev environment mainly to encourage testing of this 
# feature.
collect-tcp 1
collect-tcp-interval 0.2

# We want to use the previous transform by default.
respect-prev-transform 1

# We don't need to hear about all the silly problems with tiff files.
notify-level-tiff error

# The ID of the server that we are compatible with

# For users in the dev environment, we don't care that much about
# enforcing this, and it's easier to keep it always the same than to
# have people constantly having to update their pirates.par files.
server-version dev

# Also, users in the dev environment want this set.
want-dev 1

# The current Toontown code now supports temp-hpr-fix.
# Welcome to the future.
temp-hpr-fix 1


# Custom ObjectTypes for OTP.
# "barrier" means a vertical wall, with bitmask 0x01
# "floor" means a horizontal floor, with bitmask 0x02
# "camera-collide" means things that the camera should avoid, with bitmask 0x04
egg-object-type-barrier         <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend }
egg-object-type-floor           <Scalar> collide-mask { 0x02 } <Collide> { Polyset descend level }
egg-object-type-dupefloor       <Scalar> collide-mask { 0x02 } <Collide> { Polyset keep descend level }
egg-object-type-trigger         <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend intangible }
egg-object-type-planebarrier    <Scalar> collide-mask { 0x01 } <Collide> { Plane descend }
egg-object-type-planefloor      <Scalar> collide-mask { 0x02 } <Collide> { Plane descend }
egg-object-type-sphere          <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend }
egg-object-type-tube            <Scalar> collide-mask { 0x01 } <Collide> { Tube descend }
egg-object-type-camcollide      <Scalar> collide-mask { 0x04 } <Collide> { Polyset descend }
egg-object-type-camtransparent  <Scalar> collide-mask { 0x08 } <Collide> { Polyset descend }
egg-object-type-cambarrier      <Scalar> collide-mask { 0x05 } <Collide> { Polyset descend }
egg-object-type-camtransbarrier <Scalar> collide-mask { 0x09 } <Collide> { Polyset descend }
egg-object-type-pet             <Scalar> collide-mask { 0x08 } <Collide> { Polyset descend }
egg-object-type-ouch1           <Tag> ouch { 1 }
egg-object-type-ouch2           <Tag> ouch { 2 }
egg-object-type-ouch3           <Tag> ouch { 3 }
egg-object-type-ouch4           <Tag> ouch { 4 }
egg-object-type-ouch5           <Tag> ouch { 5 }

# surface attributes
egg-object-type-dirt-surface    <Tag> surface { dirt }
egg-object-type-gravel-surface  <Tag> surface { gravel }
egg-object-type-grass-surface   <Tag> surface { grass }
egg-object-type-asphalt-surface <Tag> surface { asphalt }
egg-object-type-wood-surface    <Tag> surface { wood }
egg-object-type-water-surface   <Tag> surface { water }
egg-object-type-snow-surface    <Tag> surface { snow }
egg-object-type-ice-surface     <Tag> surface { ice }
egg-object-type-sticky-surface  <Tag> surface { sticky }


# These are deprecated.  It's now possible to combine two of the above
# to achieve the same as any of these.
egg-object-type-trigger-sphere  <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend intangible }
egg-object-type-camera-barrier  <Scalar> collide-mask { 0x05 } <Collide> { Polyset descend }
egg-object-type-camera-barrier-sphere  <Scalar> collide-mask { 0x05 } <Collide> { Sphere descend }
egg-object-type-camera-collide-sphere  <Scalar> collide-mask { 0x04 } <Collide> { Sphere descend }
egg-object-type-camera-collide  <Scalar> collide-mask { 0x04 } <Collide> { Polyset descend }

# The modelers occasionally put <ObjectType> { model } instead of
# <Model> { 1 }.  Let's be accommodating.
egg-object-type-model           <Model> { 1 }
egg-object-type-dcs             <DCS> { 1 }

# Define a "shadow" object type, so we can render all shadows in their
# own bin and have them not fight with each other (or with other
# transparent geometry).
egg-object-type-shadow          <Scalar> bin { shadow } <Scalar> alpha { blend-no-occlude }
cull-bin shadow 15 fixed

# We must currently set this to avoid messing up some of
# the suits' faces.
egg-retesselate-coplanar 0

# Define a "ground" type, for rendering ground surfaces immediately
# behind the drop shadows.
egg-object-type-shground        <Scalar> bin { ground } <Tag> cam { shground }
egg-object-type-ground          <Scalar> bin { ground } <Tag> cam { shground }
egg-object-type-shadow-ground   <Scalar> bin { ground } <Tag> cam { shground }
cull-bin ground 14 fixed

# Whenever we load models implicitly, convert them to feet.
ptloader-units ft

# Allow loading model files without an extension.
default-model-extension .bam

# Allow devs to run without chat filtering.  DO NOT ENABLE IN PRODUCTION.
allow-unfiltered-chat 1

#end 50_otp.prc
