"""This file exists so we can switchably include these files, which
are not imported or shipped in production code, but are handy in the
development environment. """

if __dev__:
    from direct.directutil import DistributedLargeBlobSenderAI
    import DistributedInGameEditorAI
