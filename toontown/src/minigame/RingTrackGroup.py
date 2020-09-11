"""RingTrackGroup.py: contains RingTrackGroup functions"""

class RingTrackGroup:
    """RingTrackGroups are groupings of ring tracks to be used with
    RingGroup objects."""
    def __init__(self, tracks, period,
                 trackTOffsets=None, reverseFlag=0, tOffset=0.):
        """
        tracks: list of RingTracks
        period: playback period of all ringTracks, in seconds
        trackTOffsets: list of 0..1 delays for RingTracks
        reverseFlag: reverses all tracks
        tOffset: 0..1 time delay (scaled to period) for entire group
                 allows ring groups to be out-of-phase w/ each other
        """
        assert(len(tracks) >= 1 and len(tracks) <= 4)
        assert(period >= 0.)
        # create a default set of track time offsets if none provided
        if trackTOffsets == None:
            trackTOffsets = [0] * len(tracks)
        assert(len(tracks) == len(trackTOffsets))

        self.tracks = tracks
        self.period = period
        self.trackTOffsets = trackTOffsets
        self.reverseFlag = reverseFlag
        self.tOffset = tOffset
