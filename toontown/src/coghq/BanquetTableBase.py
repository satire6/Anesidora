class BanquetTableBase:
    """Hold methods and constants shared in client and AI versions."""
    # states of the diners
    HUNGRY = 1
    DEAD = 0
    EATING =2 # distance between each food node
    ANGRY = 3 # haven't been fed in a while, resets to 0
    HIDDEN = 4 # we don't show him in the scene
    INACTIVE = 5 # just sitting in the chair, waiting for battle two to start
