from toontown.toonbase import ToontownGlobals

# make sure that the methods here can work on the AI and the client

def calcPropType( node):
    """Calculate if we are hydrant, mailbox, trashcan, or unknown."""
    propType = ToontownGlobals.AnimPropTypes.Unknown
    fullString = str(node)
    if "hydrant" in fullString:
        propType = ToontownGlobals.AnimPropTypes.Hydrant
    elif "trashcan" in fullString:
        propType = ToontownGlobals.AnimPropTypes.Trashcan
    elif "mailbox" in fullString:
        propType = ToontownGlobals.AnimPropTypes.Mailbox
    return propType
