import NameCheck

def checkNames(names, goodFlags=None):
    if goodFlags:
        # make sure they're the same length
        assert len(names) == len(goodFlags)
    for i in range(len(names)):
        name = names[i]
        # the game does the strip() in NameShop.py
        problem = NameCheck.checkName(name.strip())
        if problem:
            print '   user msg: ' + problem
        if goodFlags:
            # make sure our results are consistent
            if problem:
                assert not goodFlags[i], "good name was rejected: '%s'" % name
            else:
                assert goodFlags[i], "bad name was accepted: '%s'" % name
                
goodNames = [
    "foo",
    "foo-bar",
    "little-bunny-foo-foo",
    "little bunny foo foo",
    "McQuack",
    "Dr. J.T. McQuack, MD",
    "Cuddles 'n Hugs",
    "ribbit",
    "name, name",
    "Mrs. Bunny",
    "J.T.",
    "name.",
    "Schrodinger's Cat",
    "Schrodinger's Cat's Dog",
    "Schrodinger's Cat's Dog's Mouse",
    ]
badNames = [
    "MiXeD CaSe",
    "MiCkeY MoUsE",
    "ALLCAPS",
    "MICKEY MOUSE",
    "a",
    "A",
    "Mickey_Mouse!",
    "Flippy",
    "yppilf",
    "Kwee Kwee the Rainbow Kitten",
    "too many gosh darn words",
    "     ",
    "",
    "ndssmvwls",
    "eeeeeeeeeeeee",
    "...",
    ",,,",
    "..,,'',,..",
    "bad -hyphen",
    "also- bad",
    "-pre",
    "post-",
    "another--bad one",
    ",name",
    " ,name",
    "name,",
    "name, ",
    "name,name",
    "name ,name",
    "name , name",
    "name.name",
    "JT..",
    "foo .",
    "w'o'r'd",
    "bob's dog's cat's mouse's",
    ]
# these are names that currently are not handled correctly
testNames = [
    ]

def runTest():
    print 'CHECKING GOOD NAMES'
    checkNames(goodNames, [1] * len(goodNames))
    print 'CHECKING BAD NAMES'
    checkNames(badNames, [0] * len(badNames))
    print '*** all tests passed'

    checkNames(testNames)
