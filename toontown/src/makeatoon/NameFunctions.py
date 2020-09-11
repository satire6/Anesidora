
import string

class NameFunctions:

    boyTitles = ["Baron", "Duke", "King", "Master",
                 "Mister", "Prince", "Sir",
                 ]
    
    girlTitles = ["Lady", "Miss", "Princess",
                  "Queen", "Granny", "Aunt",
                  ]
    
    neutralTitles = ["Big", "Captain", "Cool", "Colonel", "Crazy",
                     "Deputy", "Dippy", "Doctor", "Fat",
                     "Good ol'",
                     "Little", "Loopy", "Loud",
                     "Noisy", "Prof.",
                     "Sheriff", "Skinny", "Silly",
                     "Super", "Ugly", "Weird"]
    # First Names
    boyFirsts = ["Alvin",
                 "Barney", "Beppo", "Bert", "Bonzo",
                 "Buford", "Bunky", "Buster",
                 "Butch", "Buzz",
                 "Cecil", "Chester", "Chip", "Chipper", "Clancy", "Clarence",
                 "Cliff", "Clyde",
                 "Dudley", "Duke", "Ernie",
                 #"Fenimore",
                 "Fritz", "Graham", "Harvey", "Hector",
                 "Huey", "Jacques", "Jake",
                 "Knuckles",
                 "Lancelot", "Leroy", "Lionel", "Lloyd", "Louie",
                 "Mac", "Max", "Moe", "Monty", "Milton", "Ned",
                 "Orville", "Oscar", "Oswald", "Ozzie",
                 "Pierre",
                 #"Poindexter",
                 "Reggie", "Ricky",
                 "Rocco", "Rollie", "Romeo", "Rusty", "Sammie",
                 "Skip", "Skipper", "Skippy", "Spike", "Stinky",
                 #"Thaddeus",
                 "Tom",
                 "Waldo", "Wally", "Wilbur",
                 ]
    girlFirsts = ["Bonnie", "Bubbles",
                  #"Buttercup",
                  "Candy",
                  #"Cinnamon",
                  "Clover",
                  "Cuddles",
                  "Daffodil",
                  #"Dandelion",
                  "Daphne", "Dee Dee",
                  "Dottie", "Ginger", "Gwen", "Ladybug", "Lily",
                  "Marigold", "Maxie",
                  "Melody", "Mo Mo",
                  #"Moonbeam",
                  "Nutmeg",
                  "Peaches", "Pearl", "Penny", "Petunia",
                  #"Penelope",
                  "Rainbow", "Raven", "Robin", "Rosie", "Roxy",
                  "Sadie", "Sally", "Sandy",
                  #"Snowflake",
                  #"Sunflower",
                  "Taffy", "Trixie",
                  "Ursula", "Violet", "Vicky",
                  ]
    neutralFirsts = ["B.D.", "Banjo", "Batty", "Beany", "Bebop", "Bingo",
                     "Binky", "Biscuit", "Bongo", "Boo Boo", "Bonkers", "Bizzy",
                     "Blinky", "Bumpy", "C.J.", "C.W.", "Chirpy",
                     "Chunky", "Coconut", "Comet", "Corky", "Corny", "Cranky", "Crazy",
                     #"Creampuff",
                     "Cricket", "Crumbly", "Curly", "Cuckoo",
                     "Daffy",
                     #"Dingdong",
                     "Dinky", "Dizzy",
                     "Domino", "Drippy", "Droopy",
                     "Dusty", "Fancy", "Fangs", "Fireball",
                     "Fleabag", "Flapjack", "Flappy",
                     "Flip", "Fluffy", "Freckles", "Frizzy", "Furball",
                     "Goopy",
                     #"Gumdrop",
                     #"Harebrain",
                     "Huddles", "J.C.",
                     #"Jellybean",
                     "Jellyroll",
                     "Kippy", "Lefty", "Lollipop", "Loony", "Loopy",
                     "Mildew",
                     #"Mumbles",
                     "Murky", "Nutty", "Pancake", "Peanut",
                     #"Peppermint",
                     "Peppy", "Pickles",
                     "Pinky", "Popcorn", "Poppy",
                     "Rhubarb",
                     "Salty", "Scooter",
                     #"Scratchy",
                     "Skids", "Skimpy", "Soupy",
                     "Slappy", "Slippy", "Slumpy", "Smirky", "Snappy",
                     "Sniffy", "Snuffy",
                     "Spiffy", "Spotty", "Spunky", "Stripey",
                     "Stubby",
                     "Tricky", "Tubby",
                     "Von",
                     "Wacky", "Wacko",
                     #"Whiskers",
                     "Winky",
                     "Yippie",
                     "Z.Z.", "Zany", "Ziggy", "Zilly",
                     "Zippy", "Zippety", "Zowie",
                     ]
    # Last name prefixes
    
    # Prefixes that will require suffix capitalization
    capPrefixes = ["Mc", "Mac"]
    
    lastPrefixes = ["Bagel", "Banana", "Bean", "Beanie", "Biggen",
                    "Bizzen", "Blubber", "Boingen",
                    "Bumber", "Bumble", "Bumpen",
                    "Cheezy", "Crinkle",
                    "Crumble", "Crunchen", "Crunchy",
                    "Dandy", "Dingle",
                    "Dizzen", "Dizzy",
                    "Doggen", "Dyno", "Electro",
                    "Feather", "Fiddle",
                    "Frinkel", "Fizzle", "Flippen",
                    "Flipper",
                    "Fumble", "Funny", "Fuzzy",
                    "Giggle", "Google", "Huckle", "Hula",
                    "Jabber", "Jeeper", "Jumble", "Kooky", "Lemon",
                    "Loopen", "Mac", "Mc", "Mega",
                    "Mizzen", "Nickel", "Nutty", "Octo", "Paddle", "Pale",
                    "Pedal", "Pepper", "Petal", "Pickle", "Pinker",
                    "Poodle", "Precious", "Purple", "Poppen",
                    "Rhino", "Rocken", "Ruffle",
                    "Sniffle", "Snorkel", "Sour", "Sparkle", "Super",
                    "Spackle", "Thunder", "Toppen",
                    "Tricky", "Twiddle", "Twinkle",
                    "Wacky", "Weasel", "Whisker",
                    "Whistle", "Wild", "Wonder", "Wrinkle",
                    "Ziller", "Zippen", "Zooble",
                    ]
    lastSuffixes = ["bee", "berry", "blabber", "bocker", "boing", "boom",
                    "bounce", "bouncer", "brains", "bubble",
                    "bumble", "bump", "bumper", "burger",
                    "chomp", "corn", "crash", "crumbs",
                    "crump", "crunch",
                    "doodle", "dorf",
                    "face", "fidget", "fish", "flap", "fuddy",
                    "flapper", "fink",
                    "flinger", "flip", "flipper",
                    "foot", "fussen",
                    "gadget", "gargle", "glop", "gloop",
                    "goober", "goose",
                    "grooven", "hoffer", "hopper",
                    "jinks", "klunk", "knees",
                    "marble", "mash", "monkey", "mooch", "mouth",
                    "muddle", "muffin", "mush",
                    "nerd", "noodle", "nose", "nugget",
                    "phew", "phooey", "pocket", "pop", "pow", "pretzel",
                    "pounce", "poof", "quack",
                    "roni",
                    "scooter", "screech", "seed",
                    "smirk", "snoop", "snooker", "snout", "socks",
                    "speed", "spinner", "splat", "sticks", "stink", "swirl",
                    "teeth", "thud", "toes", "ton", "toon", "tooth", "twist",
                    "whip", "wig", "woof",
                    "zaner", "zap", "zapper", "zilla",
                    ]
    
    header = ["# This file contains all the possible names used in toon name generation.",
              "# Each name has a unique id and a category:",
              "#                                     0 - boyTitle",
              "#                                     1 - girlTitle",
              "#                                     2 - neutralTitle",
              "#                                     3 - boyFirst",
              "#                                     4 - girlFirst",
              "#                                     5 - neutralFirst",
              "#                                     6 - capPrefix",
              "#                                     7 - lastPrefix",
              "#                                     8 - lastSuffix"]
    
    def __init__(self):
        return
    
    def writeNameMaster(self):
        print "Writing Name Master"
        output = open('NameMasterEnglish.txt', 'w')
        for x in self.header:
            output.write(x+'\n')

        categoryNames = [self.boyTitles, self.girlTitles, self.neutralTitles,
                         self.boyFirsts, self.girlFirsts, self.neutralFirsts,
                         self.capPrefixes, self.lastPrefixes, self.lastSuffixes]

        uniqueID = 0
        for cat in range(0,9):
            print "Working on list " + str(cat) + ".  UniqueID is up to " + str(uniqueID)
            for name in categoryNames[cat]:
                output.write(str(uniqueID) + "*" + str(cat) + "*" + name + '\n')
                uniqueID += 1
        output.close()


    def readNameMaster(self):
        self.nameDictionary = {}
        try:
            input = open('NameMasterEnglish.txt1', 'r')
        except:
            print "NameFunctions: Error opening list text file."
            return
        for currentLine in input.xreadlines():
            if currentLine.lstrip()[0:1] != '#':
                a1 = currentLine.find('*')
                a2 = currentLine.find('*', a1+1)
                self.nameDictionary[int(currentLine[0:a1])]=(int(currentLine[a1+1:a2]),
                                                             currentLine[a2+1:len(currentLine)-1])
        masterList = [[],[],[],[],[],[],[],[],[]]
        for tu in self.nameDictionary.values():
            masterList[tu[0]].append(tu[1])

        self.nboyTitles = masterList[0]
        self.ngirlTitles = masterList[1]
        self.nneutralTitles = masterList[2]
        self.nboyFirsts = masterList[3]
        self.ngirlFirsts = masterList[4]
        self.nneutralFirsts = masterList[5]
        self.ncapPrefixes = masterList[6]
        self.nlastPrefixes = masterList[7]
        self.nlastSuffixes = masterList[8]

        print self.boyTitles
        print self.nboyTitles




