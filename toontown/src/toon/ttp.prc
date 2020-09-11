win-size 50 50
preload-avatars         #t

default-model-extension .bam

# Mesa doesn't work under Windows - let's use Dx now

#window-type offscreen
# At the moment, pandadx does not support offscreen rendering.  Prefer
# mesadisplay, which does this well and doesn't require anyone logged
# onto the desktop.  Fall back to pandagl if something goes wrong with
# mesadisplay.
#load-display mesadisplay
#aux-display pandagl

# mesadisplay seems to crash unless you turn off vertex-arrays.
#vertex-arrays 0

load-display pandadx9
aux-display pandadx8

# Configrc for running the Robot Toon Manager

# THESE LINES ALLOW YOU TO USE DOWNLOAD MODELS INSTEAD OF TTMODELS
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_3.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_3.5.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_4.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_5.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_5.5.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_6.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_7.mf /tt 0
#vfs-mount /c/Program Files/Disney/Disney Online/Toontown/phase_8.mf /tt 0

# Use local copy of ttmodels
model-path     .
# Putting this line after ttmodels means models will be read from here first
# model-path     /tt
sound-path     .
dna-preload    phase_4/dna/storage.dna

text-encoding utf8

cull-bin shadow 15 unsorted

# Turn off noisy errors.
notify-level-chan   error

