import string
from toontown.toonbase.TTLocalizer_german_Property import *

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
ExtraKeySanityCheck = "Ignore me"

InterfaceFont = 'phase_3/models/fonts/ImpressBT.ttf'
ToonFont = 'phase_3/models/fonts/ImpressBT.ttf'
SuitFont = 'phase_3/models/fonts/vtRemingtonPortable.ttf'
SignFont = 'phase_3/models/fonts/MickeyFont'
MinnieFont = 'phase_3/models/fonts/MinnieFont'
BuildingNametagFont = 'phase_3/models/fonts/MickeyFont'
BuildingNametagShadow = None

# common names
Mickey = "Micky"
Minnie = "Minnie"
Donald = "Donald"
Daisy  = "Daisy"
Goofy  = "Goofy"
Pluto  = "Pluto"
Flippy = "Flippy"

# common locations
lTheBrrrgh = 'Das Brrr'
lDaisyGardens = 'Daisys Gärten'
lDonaldsDock = "Donalds Dock"
lDonaldsDreamland = "Donalds Traumland"
lMinniesMelodyland = "Minnies Melodienland"
lToontownCentral = 'Toontown Mitte'
lToonHQ = 'Toontown-\nZentrale'

# common strings
lCancel = 'Abbrechen'
lClose = 'Schließen'
lOK = 'OK'
lNext = 'Weiter'
lNo = 'Nein'
lQuit = 'Beenden'
lYes = 'Ja'

lHQOfficerF = 'Mitarbeiter der Zentrale'
lHQOfficerM = 'Mitarbeiter der Zentrale'

MickeyMouse = "Micky Maus"

AIStartDefaultDistrict = "Maushöhe"

Cog  = "Bot"
Cogs = "Bots"
ACog = "ein Bot"
TheCogs = "den Bots"
Skeleton = "Skeletobot"
SkeletonP = "Skeletobots"
ASkeleton = "ein Skeletobot"
Foreman = "Vorarbeiter"
ForemanP = "Vorarbeiter"
AForeman = "ein Vorarbeiter"
CogVP = "Bot-VP "
CogVPs = "Bot-VPs"
ACogVP = "ein Bot-VP"

# Quests.py
TheFish = "der Fisch"
AFish = "ein Fisch"
Level = "Level "
QuestsCompleteString = "Beendet "
QuestsNotChosenString = "Nicht ausgewählt"
Period = "."

QuestInLocationString = " %(inPhrase)s %(location)s"

# _avName_ gets replaced with the avatar (player's) name
# _toNpcName_ gets replaced with the npc's name we are being sent to
# _where_ gets replaced with a description of where to find the npc, with a leading \a
QuestsDefaultGreeting = ("Hallo, _avName_!",
                         "Hi, _avName_!",
                         "Na du, _avName_!",
                         "Wie steht's, _avName_!",
                         "Willkommen, _avName_!",
                         "Tag, _avName_!",
                         "Wie geht's, _avName_?",
                         "Guten Tag _avName_!",
                         )
QuestsDefaultIncomplete = ("Wie geht's mit der Aufgabe voran, _avName_?",
                           "Sieht aus, als müsstest du an dieser Aufgabe noch etwas arbeiten!",
                           "Weiter so, _avName_!",
                           "Bleib weiter an dieser Aufgabe dran. Ich weiß, du schaffst das!",
                           "Versuch weiter, diese Aufgabe zu lösen, wir zählen auf dich!",
                           "Arbeite weiter an dieser Toon-Aufgabe!",
                           )
QuestsDefaultIncompleteProgress = ("Du bist zum richtigen Ort gekommen, aber du musst erst noch deine Toon-Aufgabe lösen!",
                                   "Komm wieder her, wenn du mit deiner Toon-Aufgabe fertig bist.",
                                   "Komm wieder, wenn du mit deiner Toon-Aufgabe fertig bist.",
                                   )
QuestsDefaultIncompleteWrongNPC = ("Gut gelöst, diese Toon-Aufgabe. Du solltest mal _toNpcName_ besuchen._where_",
                                   "Sieht aus, als wärst du gleich mit deiner Toon-Aufgabe fertig. Besuch mal _toNpcName_._where_.",
                                   "Besuche _toNpcName_ um deine Toon-Aufgabe zu lösen._where_",
                                   )
QuestsDefaultComplete = ("Gute Arbeit! Hier deine Belohnung ...",
                         "Gut gemacht, _avName_! Nimm das hier als Belohnung ...",
                         "Spitzenleistung, _avName_! Hier deine Belohnung ...",
                         )
QuestsDefaultLeaving = ("Tschüss!",
                        "Auf Wiedersehen!",
                        "Mach's gut, _avName_.",
                        "Bis bald, _avName_!",
                        "Viel Glück!",
                        "Viel Spaß in Toontown!",
                        "Bis demnächst!",
                        )
QuestsDefaultReject = ("Hallo!",
                       "Kann ich helfen?",
                       "Wie geht's?",
                       "Na du!",
                       "Hab grad zu tun, _avName_.",
                       "Ja?",
                       "Tag, _avName_!",
                       "Willkommen, _avName_!",
                       "Hi, _avName_! Wie steht's?",
                       # Game Hints
                       "Weißt du schon, dass du mit F8 dein Sticker-Buch öffnen kannst? ",
                       "Du kannst dich mit deinem Stadtplan wieder zum Spielplatz teleportieren!",
                       "Du kannst mit anderen Spielern Freundschaft schließen, indem du sie anklickst.",
                       "Du kannst mehr über einen " + Cog + " erfahren, indem du ihn anklickst.",
                       "Sammle Schätze auf den Spielplätzen, um dein Lach-O-Meter zu füllen.",
                       Cog +"-Gebäude sind gefährlich! Geh nicht alleine rein!",
                       "Wenn du einen Kampf verlierst, nehmen dir die " + Cogs + " alle Gags ab.",
                       "Fahr mit dem Toon-Express zum Spielplatz, verdiene beim Spielen Jellybeans, um Gags zu kaufen.!",
                       "Du kannst noch mehr Lach-Punkte gewinnen, indem du Toon-Aufgaben löst.",
                       "Für jede gelöste Toon-Aufgabe erhältst du eine Belohnung.",
                       "Einige Belohnungen helfen dir, mehr Gags mit dir zu führen.",
                       "Wenn du einen Kampf gewinnst, bekommst du für jeden vertriebenen " + Cog +  " eine Gutschrift für erledigte Toon-Aufgaben.",
                       "Wenn du ein "+ Cog +  "-Gebäude zurückeroberst, geh wieder hinein und schau nach, was der Besitzer dir als spezielles Dankeschön hinterlassen hat!",
                       "Mit der Taste 'Bild Hoch' kannst du nach oben schauen!",
                       "Mit der Tab-Taste kannst du verschiedene Ansichten deiner Umgebung sehen!",
                       "Um geheimen Freunden zu zeigen, was du gerade denkst, gib vor deinem Gedanken ein '.' ein.",
                       " Wenn ein" + Cog + " angeschlagen ist, fällt es ihm schwerer, herunterfallenden Gegenständen auszuweichen.. ",
                       "Jede Art von "+ Cog +  "-Gebäude hat ein eigenes Aussehen.",
                       "Wenn du "+ Cogs +  " auf den höheren Stockwerken eines Gebäudes besiegst, bringt dir das höhere Geschicklichkeitspunkte ein.",
                       )
QuestsDefaultTierNotDone = ("Hallo, _avName_! Du musst erst deine derzeitigen Toon-Aufgaben lösen, bevor du eine neue bekommst.",
                            "Hallo! Du musst erst die Toon-Aufgaben lösen, an denen du gerade arbeitest, um eine neue zu bekommen.",
                            "Hi, _avName_! Bevor ich dir eine neue Toon-Aufgabe geben kann, musst du erst die lösen, die du schon hast.",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("Ich habe gehört, _toNpcName_ sucht dich._where_",
                                 "Schau mal bei _toNpcName_ rein, wenn du kannst._where_",
                                 "Besuche mal _toNpcName_ , wenn du das nächste Mal in der Nähe bist._where_",
                                 "Schau mal bei Gelegenheit bei _toNpcName_._where_ vorbei",
                                 "_toNpcName_ wird dir deine nächste Toon-Aufgabe geben._where_",
                                 )
# Quest dialog
QuestsLocationArticle = ""
def getLocalNum(num):
	if (num <=9):
		return str(num) + ""
	else:
		return str(num)
QuestsItemNameAndNum = "%(num)s %(name)s"

QuestsCogQuestProgress = "%(progress)s von %(numCogs)s vertrieben"
QuestsCogQuestHeadline = "GESUCHT"
QuestsCogQuestSCStringS = "Ich muss %(cogName)s%(cogLoc)s erledigen."
QuestsCogQuestSCStringP = "Ich muss ein paar %(cogName)s%(cogLoc)s vertreiben."
QuestsCogQuestDefeat = "%s vertreiben"
QuestsCogQuestDefeatDesc = "%(numCogs)s %(cogName)s"

QuestsCogNewNewbieQuestObjective = "Hilf einem neuen Toon %s zu vertreiben"
QuestsCogNewNewbieQuestCaption = "Hilf einem neuen Toon %d Lach oder weniger"
QuestsCogOldNewbieQuestObjective = "Hilf einem Toon mit %(laffPoints)d Lachpunkten oder weniger im Kampf gegen %(objective)s"
QuestsCogOldNewbieQuestCaption = "Hilf einem Toon mit <%d Lachpunkten"
QuestsCogNewbieQuestAux = "Vertreiben"
QuestsNewbieQuestHeadline = "LEHRLING"

QuestsCogTrackQuestProgress = "%(progress)s von %(numCogs)s vertrieben"
QuestsCogTrackQuestHeadline = "GESUCHT"
QuestsCogTrackQuestSCStringS = "Ich muss %(cogText)s%(cogLoc)s vertreiben."
QuestsCogTrackQuestSCStringP = "Ich muss ein paar %(cogText)s%(cogLoc)s vertreiben."
QuestsCogTrackQuestDefeat = "%s vertreiben"
QuestsCogTrackDefeatDesc = "%(numCogs)s %(trackName)s"

QuestsCogLevelQuestProgress = "%(progress)s von %(numCogs)s vertrieben"
QuestsCogLevelQuestHeadline = "GESUCHT"
QuestsCogLevelQuestDefeat = "%s vertreiben"
QuestsCogLevelQuestDesc = "ein Level %(level)s+ %(name)s"
QuestsCogLevelQuestDescC = "%(count)s Level %(level)s+ %(name)s"
QuestsCogLevelQuestDescI = "ein Level %(level)s+ %(name)s "
QuestsCogLevelQuestSCString = "Ich muss %(objective)s%(location)s vertreiben."

QuestsBuildingQuestFloorNumbers = ('', '> zwei', '> drei', '> vier', '> fünf')
QuestsBuildingQuestBuilding = "Gebäude"
QuestsBuildingQuestBuildings = "Gebäude"
QuestsBuildingQuestHeadline = "ERLEDIGEN"
QuestsBuildingQuestProgressString = "%(progress)s von %(num)s erledigt"
QuestsBuildingQuestString = "%s erledigen"
QuestsBuildingQuestSCString = "Ich muss %(objective)s%(location)s erledigen."

QuestsBuildingQuestDesc = "ein %(type)s -Gebäude"
QuestsBuildingQuestDescF = "ein %(floors)s-stöckiges %(type)s-Gebäude"
QuestsBuildingQuestDescC = "%(count)s %(type)s Gebäude"
QuestsBuildingQuestDescCF = "%(count)s %(floors)s-stöckige %(type)s Gebäude"
QuestsBuildingQuestDescI = "einige %(type)s -Gebäude"
QuestsBuildingQuestDescIF = "einige %(floors)s-stöckige %(type)s-Gebäude"

QuestFactoryQuestFactory = "Fabrik"
QuestsFactoryQuestFactories = "Fabriken"
QuestsFactoryQuestHeadline = "ERLEDIGEN"
QuestsFactoryQuestProgressString = "%(progress)s von %(num)s erledigt"
QuestsFactoryQuestString = "%s erledigen"
QuestsFactoryQuestSCString = "Ich muss %(objective)s%(location)s erledigen."

QuestsFactoryQuestDesc = "eine %(type)s -Fabrik"
QuestsFactoryQuestDescC = "%(count)s %(type)s -Fabriken"
QuestsFactoryQuestDescI = "einige %(type)s-Fabriken"

QuestsRescueQuestProgress = "%(progress)s von %(numToons)s gerettet"
QuestsRescueQuestHeadline = "RETTEN"
QuestsRescueQuestSCStringS = "Ich muss einen Toon%(toonLoc)s retten."
QuestsRescueQuestSCStringP = "Ich muss ein paar Toons%(toonLoc)s retten."
QuestsRescueQuestRescue = "%s retten"
QuestsRescueQuestRescueDesc = "%(numToons)s Toons"
QuestsRescueQuestToonS = "ein Toon"
QuestsRescueQuestToonP = "Toons"
QuestsRescueQuestAux = "Retten:"

QuestsRescueNewNewbieQuestObjective = "Hilf einem neuen Toon beim Retten von %s"
QuestsRescueOldNewbieQuestObjective = "Help a Toon with %(laffPoints)d Laff or less rescue %(objective)s"

QuestCogPartQuestCogPart = "Bot-Anzugteil"
QuestsCogPartQuestFactories = "Fabriken"
QuestsCogPartQuestHeadline = "ZURÜCKHOLEN"
QuestsCogPartQuestProgressString = "%(progress)s von %(num)s zurückgeholt"
QuestsCogPartQuestString = "%s zurückholen"
QuestsCogPartQuestSCString = "Ich muss %(objective)s%(location)s zurückholen."
QuestsCogPartQuestAux = "Zurückholen:"

QuestsCogPartQuestDesc = "ein Bot-Anzugteil"
QuestsCogPartQuestDescC = "%(count)s Bot-Anzugteile"
QuestsCogPartQuestDescI = "einige Bot-Anzugteile"

QuestsCogPartNewbieQuestObjective = 'Hilf einem neuen Toon beim Zurückholen von %s'
QuestsCogPartOldNewbieQuestObjective = 'Help a Toon with %(laffPoints)d Laff or less retrieve %(objective)s'

QuestsDeliverGagQuestProgress = "%(progress)s von %(numGags)s abgeliefert"
QuestsDeliverGagQuestHeadline = "ABLIEFERN"
QuestsDeliverGagQuestToSCStringS = "Ich muss %(gagName)s abliefern."
QuestsDeliverGagQuestToSCStringP = "Ich muss ein paar %(gagName)s abliefern."
QuestsDeliverGagQuestSCString = "Ich muss etwas abliefern."
QuestsDeliverGagQuestString = "%s abliefern"
QuestsDeliverGagQuestStringLong = "%s an _toNpcName_ abliefern."
QuestsDeliverGagQuestInstructions = "Du kannst diesen Gag im Gag-Shop kaufen, wenn du dir den Zugang verdient hast."

QuestsDeliverItemQuestProgress = ""
QuestsDeliverItemQuestHeadline = "ABLIEFERN"
QuestsDeliverItemQuestSCString = "Ich muss %(article)s%(itemName)s abliefern."
QuestsDeliverItemQuestString = "%s abliefern"
QuestsDeliverItemQuestStringLong = "%s an _toNpcName_ abliefern."

QuestsVisitQuestProgress = ""
QuestsVisitQuestHeadline = "BESUCHEN"
QuestsVisitQuestStringShort = "Besuchen"
QuestsVisitQuestStringLong = "_toNpcName_ besuchen"
QuestsVisitQuestSeeSCString = "Ich muss %s besuchen."

QuestsRecoverItemQuestProgress = "%(progress)s von %(numItems)s zurückgeholt"
QuestsRecoverItemQuestHeadline = "ZURÜCKHOLEN"
QuestsRecoverItemQuestSeeHQSCString = "Ich muss einen Mitarbeiter in der Toontown-Zentrale aufsuchen"
QuestsRecoverItemQuestReturnToHQSCString = "Ich muss %s zu einem Mitarbeiter in Toontown-Zentrale zurückgeben."
QuestsRecoverItemQuestReturnToSCString = "Ich muss %(npcName)s %(item)s zurückgeben."
QuestsRecoverItemQuestGoToHQSCString = "Ich muss zur Toontown-Zentrale gehen."
QuestsRecoverItemQuestGoToPlaygroundSCString = "Ich muss zum %s -Spielplatz."
QuestsRecoverItemQuestGoToStreetSCString = "Ich muss %(to)s %(street)s in %(hood)s gehen."
QuestsRecoverItemQuestVisitBuildingSCString = "Ich muss %s%s besuchen."
QuestsRecoverItemQuestWhereIsBuildingSCString = "Wo ist %s%s?"
QuestsRecoverItemQuestRecoverFromSCString = "Ich muss %(item)s von %(holder)s%(loc)s abholen."
QuestsRecoverItemQuestString = "%(item)s von %(holder)s abholen."
QuestsRecoverItemQuestHolderString = "%(level)s %(holder)d+ %(cogs)s"

QuestsTrackChoiceQuestHeadline = "WÄHLEN"
QuestsTrackChoiceQuestSCString = "Ich muss zwischen %(trackA)s und %(trackB)s wählen."
QuestsTrackChoiceQuestMaybeSCString = "Vielleicht sollte ich %s wählen."
QuestsTrackChoiceQuestString = "Wähle zwischen %(trackA)s und %(trackB)s"

QuestsFriendQuestHeadline = "FREUND"
QuestsFriendQuestSCString = "Ich muss einen Freund gewinnen."
QuestsFriendQuestString = "Einen Freund gewinnen"

QuestsMailboxQuestHeadline = "POST"
QuestsMailboxQuestSCString = "Ich muss mal nach meiner Post schauen."
QuestsMailboxQuestString = "In den Briefkasten schauen"

QuestsPhoneQuestHeadline = "KLARABELLA"
QuestsPhoneQuestSCString = "Ich muss Klarabella anrufen."
QuestsPhoneQuestString = "Klarabella anrufen"

QuestsFriendNewbieQuestString = "Gewinne %d Freunde %d Lach oder weniger "
QuestsFriendNewbieQuestProgress = "%(progress)s von %(numFriends)s gewonnen"
QuestsFriendNewbieQuestObjective = "Mit %d neuen Toons anfreunden"

QuestsTrolleyQuestHeadline = "TOON-EXPRESS"
QuestsTrolleyQuestSCString = "Ich muss mit dem Toon-Express fahren."
QuestsTrolleyQuestString = "Mit dem Toon-Express fahren."
QuestsTrolleyQuestStringShort = "Toon-Express fahren"

QuestsMinigameNewbieQuestString = "%d Minigames"
QuestsMinigameNewbieQuestProgress = "%(progress)s von %(numMinigames)s gespielt"
QuestsMinigameNewbieQuestObjective = "%d Minigames mit neuen Toons gespielt"
QuestsMinigameNewbieQuestSCString = "Ich muss mit neuen Toons Minigames spielen."
QuestsMinigameNewbieQuestCaption = "Hilf einem neuen Toon mit %d Lach oder weniger"
QuestsMinigameNewbieQuestAux = "Spielen:"

QuestsMaxHpReward = "Deine Lachstärke hat sich um %s erhöht."
QuestsMaxHpRewardPoster = "Belohnung: %s Punkt mehr Lachstärke"

QuestsMoneyRewardSingular = "Du bekommst 1 Jelly Bean."
QuestsMoneyRewardPlural = "Du bekommst %s Jelly Beans."
QuestsMoneyRewardPosterSingular = "Belohnung: 1 Jelly Bean"
QuestsMoneyRewardPosterPlural = "Belohnung: %s Jelly Beans"

QuestsMaxMoneyRewardSingular = "Du kannst jetzt 1 Jelly Bean mit dir führen."
QuestsMaxMoneyRewardPlural = "Du kannst jetzt %s Jelly Beans mit dir führen."
QuestsMaxMoneyRewardPosterSingular = "Belohnung: 1 Jelly Bean mit dir führen."
QuestsMaxMoneyRewardPosterPlural = "Belohnung: %s Jelly Beans mit dir führen."

QuestsMaxGagCarryReward = "Du bekommst %(name)s. Du kannst jetzt %(num)s Gags mit dir führen."
QuestsMaxGagCarryRewardPoster = "Belohnung: %(name)s (%(num)s)"

QuestsMaxQuestCarryReward = "Du kannst jetzt %s Toon-Aufgaben bekommen."
QuestsMaxQuestCarryRewardPoster = "Belohnung: %s Toon-Aufgaben mit dir führen."

QuestsTeleportReward = "Du hast jetzt Teleport-Zugang zu %s."
QuestsTeleportRewardPoster = "Belohnung: Teleport-Zugang zu %s"

QuestsTrackTrainingReward = "Du kannst jetzt für \"%s\" Gags trainieren."
QuestsTrackTrainingRewardPoster = "Belohnung: Ein Gag-Training"

QuestsTrackProgressReward = "Du hast jetzt Bild %(frameNum)s der %(trackName)s Ablauf-Animation."
QuestsTrackProgressRewardPoster = "Belohnung: \"%(trackName)s\" Ablauf-Animationsbild %(frameNum)s"

QuestsTrackCompleteReward = "Du darfst jetzt \"%s\" Gags mit dir führen und benutzen."
QuestsTrackCompleteRewardPoster = "Belohnung: %s -Ablauf-Abschlusstraining"

QuestsClothingTicketReward = "Du darfst deine Kleidung wechseln"
QuestsClothingTicketRewardPoster = "Belohnung: Eine Kleidermarke"

QuestsCheesyEffectRewardPoster = "Belohnung: %s"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "auf diesem Spielplatz"
QuestsStreetLocationThisStreet = "in dieser Straße"
QuestsStreetLocationNamedPlayground = "auf dem Spielplatz %s "
QuestsStreetLocationNamedStreet = "auf %(toStreetName)s in %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "%s's Gebäude heißt"
QuestsLocationBuildingVerb = "und das ist"
QuestsLocationParagraph = "\a%(building)s \"%(buildingName)s\"...\a...%(buildingVerb)s %(street)s."
QuestsGenericFinishSCString = "Ich muss eine Toon-Aufgabe lösen."

# MaxGagCarryReward names
QuestsMediumPouch = "einen mittelgroßer Beutel"
QuestsLargePouch = "einen großer Beutel"
QuestsSmallBag = "eine kleine Tasche"
QuestsMediumBag = "eine mittelgroße Tasche"
QuestsLargeBag = "eine große Tasche"
QuestsSmallBackpack = "ein kleiner Rucksack"
QuestsMediumBackpack = "ein mittelgroßer Rucksack"
QuestsLargeBackpack = "ein großer Rucksack"
QuestsItemDict = {
    1 : ["Brille", "Brillen", "eine "],
    2 : ["Schlüssel", "Schlüssel", "einen "],
    3 : ["Tafel", "Tafeln", "eine "],
    4 : ["Buch", "Bücher", "ein "],
    5 : ["Lutscher", "Lutscher", "einen "],
    6 : ["Kreide", "Kreiden", "eine "],
    7 : ["Rezept", "Rezepte", "ein "],
    8 : ["Notiz", "Notizen", "eine "],
    9 : ["Rechenmaschine", "Rechenmaschinen", "eine "],
    10 : ["Clownautoreifen", "Clownautoreifen", "einen"],
    11 : ["Luftpumpe ", "Luftpumpen", "eine "],
    12 : ["Tintenfischtinte", "Tintenfischtinten", "irgendeine "],
    13 : ["Paket", "Pakete", "ein "],
    14 : ["Goldfischquittung", "Goldfischquittungen", "eine "],
    15 : ["Goldfisch", "Goldfische", "einen "],
    16 : ["Öl", "Öle", "etwas "],
    17 : ["Fett", "Fette", "etwas "],
    18 : ["Wasser", "Wasser", "etwas "],
    19 : ["Getriebebericht", "Getriebeberichte", "einen "],
    20 : ["Schwamm", "Schwämme", "einen "],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    1000 : ["Kleidermarke", "Kleidermarken", "eine "],

    # Donald's Dock quest items
    2001 : ["Schlauch", "Schläuche", "einen "],
    2002 : ["Monokelrezept", "Monokelrezepte", "ein "],
    2003 : ["Brillengestell", "Brillengestelle", "irgendein "],
    2004 : ["Monokel", "Monokel", "einen "],
    2005 : ["große weiße Perücke", "große weiße Perücken", "eine "],
    2006 : ["Ballastbündel", "Ballastbündel", "ein "],
    2007 : ["Bot-Zahnrad", "Bot-Zahnräder", "ein "],
    2008 : ["Seekarte", "Seekarten", "eine "],
    2009 : ["verschmutzten Webeleinstek", "verschmutzte Webeleinsteke", "einen "],
    2010 : ["sauberen Webeleinstek", "saubere Webeleinsteke", "einen "],
    2011 : ["Uhrfeder", "Uhrfedern", "eine "],
    2012 : ["Gegengewicht", "Gegengewichte", "ein "],

    # Minnie's Melodienland quest items
    4001 : ["Tinas Inventarliste", "Tinas Inventarlisten", ""],
    4002 : ["Yukis Inventarliste", "Yukis Inventarlisten", ""],
    4003 : ["Inventarlistenformular", "Inventarlistenformulare", "ein "],
    4004 : ["Fifis Inventarliste", "Fifis Inventarlisten", ""],
    4005 : ["Holzmichels Ticket", "Holzmichels Tickets", ""],
    4006 : ["Tabithas Ticket", "Tabithas Tickets", ""],
    4007 : ["Grizzlys Ticket", "Grizzlys Tickets", ""],
    4008 : ["Matte Kastagnette", "Matte Kastagnetten", "eine "],
    4009 : ["Blaue Tintenfischtinte", "Blaue Tintenfischtinte", "irgendeine "],
    4010 : ["glänzende Kastagnette", "glänzende Kastagnetten", "eine "],
    4011 : ["Leos Reim", "Leos Reime", ""],

    # Daisy's Garden quest items
    5001 : ["Seidenkrawatte", "Seidenkrawatten", "eine "],
    5002 : ["Nadelstreifenanzug", "Nadelstreifenanzüge", "einen "],
    5003 : ["Schere", "Scheren", "eine "],
    5004 : ["Postkarte", "Postkarten", "eine "],
    5005 : ["Stift", "Stifte", "einen "],
    5006 : ["Tintenfass", "Tintenfässer", "ein "],
    5007 : ["Schreibblock", "Schreibblöcke", "einen "],
    5008 : ["verschließbare Kassette", "verschließbare Kassetten", "eine "],
    5009 : ["Tüte mit Vogelfutter", "Tüten mit Vogelfutter", "eine "],
    5010 : ["Kettenradzahn", "Kettenradzähne", "einen "],
    5011 : ["Salat", "Salate", "einen "],
    5012 : ["Schlüssel zu Daisys Gärten", "Schlüssel zu Daisys Gärten", "einen "],
    5013 : ["Blaupause des Schachermat-Hauptquartiers", "Blaupausen des Schachermat-Hauptquartiers", "irgendeine "],
    5014 : ["Memo des Schachermat-Hauptquartier", "Memo des Schachermat-Hauptquartiers", "ein "],
    5015 : ["Memo des Schachermat-Hauptquartier", "Memo des Schachermat-Hauptquartiers", "ein "],
    5016 : ["Memo des Schachermat-Hauptquartier", "Memo des Schachermat-Hauptquartiers", "ein "],
    5017 : ["Memo des Schachermat-Hauptquartier", "Memo des Schachermat-Hauptquartiers", "ein "],

    # The Brrrgh quests
    3001 : ["Fußball", "Fußbälle", "einen "],
    3002 : ["Rodelschlitten", "Rodelschlitten", "einen "],
    3003 : ["Eiswürfel", "Eiswürfel", "einen "],
    3004 : ["Liebesbrief", "Liebesbriefe", "einen "],
    3005 : ["Wiener Würstchen", "Wiener Würstchen", "ein "],
    3006 : ["Verlobungsring", "Verlobungsringe", "einen "],
    3007 : ["Stein des Weisen", "Steine des Weisen", "einen "],
    3008 : ["Beruhigungstrank", "Beruhigungstrank", "einen "],
    3009 : ["kaputten Zahn", "kaputte Zähne", "einen "],
    3010 : ["Goldzahn", "Goldzähne", "einen "],
    3011 : ["Kiefernzapfenbrot", "Kiefernzapfenbrote", "einen "],
    3012 : ["Krümelkäse", "Krümelkäse", "irgendeinen "],
    3013 : ["einfachen Löffel", "einfache Löffel", "einen "],
    3014 : ["sprechende Kröte", "sprechende Kröten", "eine "],
    3015 : ["Eistüte", "Eistüten", "eine "],
    3016 : ["Perückenpuder", "Perückenpuder", "irgendein "],
    3017 : ["Quietschentchen", "Quietschentchen", "ein "],
    3018 : ["Fellwürfel", "Fellwürfel", "irgendeinen "],
    3019 : ["Mikrofon", "Mikrofone", "ein "],
    3020 : ["elektrisches Keyboard", "elektrische Keyboards", "ein "],
    3021 : ["Plateauschuhe", "Plateauschuhe", "etwas "],
    3022 : ["Kaviar", "Kaviar", "etwas "],
    3023 : ["Make-up-Puder", "Make-up-Puder", "irgendein "],
    }
QuestsHQOfficerFillin = "Mitarbeiter in der Zentrale"
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = "Toontown-Zentrale"
QuestsHQLocationNameFillin = "In einer beliebigen Gegend"

QuestsTailorFillin = "Schneider"
QuestsTailorWhereFillin = ""
QuestsTailorBuildingNameFillin = "Bekleidungsgeschäft"
QuestsTailorLocationNameFillin = "In einer beliebigen Gegend"
QuestsTailorQuestSCString = "Ich muss zu einem Schneider."

QuestMovieQuestChoiceCancel = "Komm später wieder, wenn du eine neue Toon-Aufgabe brauchst! Tschüss!"
QuestMovieTrackChoiceCancel = "Komm wieder, wenn du dich entscheiden kannst! Tschüss!"
QuestMovieQuestChoice = "Wähle eine Toon-Aufgabe."
QuestMovieTrackChoice = "Bereit zum Wählen? Wähle einen Ablauf oder komm später wieder."

# Constants used in Quests.py, globally defined here
GREETING = 0
QUEST = 1
INCOMPLETE = 2
INCOMPLETE_PROGRESS = 3
INCOMPLETE_WRONG_NPC = 4
COMPLETE = 5
LEAVING = 6

TheBrrrghTrackQuestDict = {
    GREETING : "",
    QUEST : "Jetzt bist du fertig.\aZiehe nun in die Welt und wandere umher, bis du weißt, welchen Ablauf du wählen möchtest.\aWähle klug, denn dies ist dein letzter Track.\aWenn du dir sicher bist, kehre zu mir zurück.",
    INCOMPLETE_PROGRESS : "Wähle mit Verstand.",
    INCOMPLETE_WRONG_NPC : "Wähle mit Verstand.",
    COMPLETE : "Sehr kluge Entscheidung!",
    LEAVING : "Viel Glück! Komm wieder zu mir, wenn du deine neue Fähigkeit beherrschst.",
    }

QuestDialog_3225 = {
    QUEST : "Oh, danke, dass du gekommen bist, _avName_!\aDie Bots in dieser Gegend haben mein Lieferanten verschreckt.\aIch habe niemanden, der diesen Salat an _toNpcName_ausliefert!\aKannst du das für mich tun? Hab vielen Dank!_where_"
    }

QuestDialog_2910 = {
    QUEST : "Schon wieder da?\aDas mit der Feder hast du gut gemacht.\aDer letzte Gegenstand ist ein Gegengewicht.\aSchau mal bei _toNpcName_ vorbei und bring alles mit, was du kriegen kannst._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "OK, jetzt bist du wohl für etwas Interessanteres bereit.\aWenn du 3 Chefomaten vertreiben kannst, bekommst du von mir ein kleines Extra.",
           INCOMPLETE_PROGRESS : "Die "+ Cogs +  " sind draußen auf der Straße, durch die Tunnel.",
           INCOMPLETE_WRONG_NPC : "Tolle Leistung, dein Sieg über die Chefomaten. Geh jetzt zur Toontown-Zentrale, um deine Belohnung abzuholen.",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "OK, jetzt bist du wohl bereit für etwas Interessanteres.\aKomm wieder her, wenn du 3 Rechtomaten vertrieben hast - dann hab ich ein kleines Geschenk für dich.",
           INCOMPLETE_PROGRESS : "Die "+ Cogs +  " sind draußen auf der Straße, durch die Tunnel.",
           INCOMPLETE_WRONG_NPC : "Tolle Leistung, dein Sieg über die Rechtomaten. Geh jetzt zur Toontown-Zentrale, um deine Belohnung abzuholen!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
 162 : {GREETING : "",
           QUEST : "OK, jetzt bist du wohl bereit für etwas Interessanteres.\aBesiege 3 Monetomaten und komm wieder her, um deine Prämie einzufordern.",
           INCOMPLETE_PROGRESS : "Die "+ Cogs +  " sind draußen auf der Straße, durch die Tunnel.",
           INCOMPLETE_WRONG_NPC : "Tolle Leistung, dein Sieg über die Monetomaten. Geh jetzt zu eine Toontown-Zentrale, um deine Belohnung abzuholen!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
 163 : {GREETING : "",
           QUEST : "OK, jetzt bist du wohl bereit für etwas Interessanteres.\aKomm wieder her, wenn du 3 Schachermaten vertrieben hast, und du bekommst eine Belohnung und eine neue Aufgabe.",
           INCOMPLETE_PROGRESS : "Die "+ Cogs +  " sind draußen auf der Straße, durch die Tunnel.",
           INCOMPLETE_WRONG_NPC : "Tolle Leistung, dein Sieg über die Schachermaten. Geh jetzt zur Toontown-Zentrale, um deine Belohnung abzuholen!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },

    164 : {QUEST : "Du siehst aus, als könntest du ein paar neue Gags gebrauchen.\aGeh mal zu Flippy, der kann dir vielleicht aushelfen._where_" },
    165 : {QUEST : "Hallo!\aSieht aus, als müsstest du deine Gags mal in der Praxis trainieren.\aJedes Mal, wenn du einem Bot einen deiner Gags um die Ohren haust, wächst deine Erfahrung.\aWenn du genug Erfahrung hast, kannst du dann einen noch besseren Gag einsetzen.\aGeh deine Gags üben und vertreibe dabei 4 Bots."},
    166 : {QUEST : "Toll, wie du diese Bots vertrieben hast!\aWeißt du, es gibt vier Arten von Bots.\aRechtomaten, Monetomaten, Schachermaten und Chefomaten.\aDu kannst sie an ihrer Färbung und ihren Namensschildern erkennen.\aGeh mal los und besiege zur Übung 4 Chefomaten."},
    167 : {QUEST : "Toll, wie du diese Bots vertrieben hast!\aWeißt du, es gibt vier Arten von Bots.\a Rechtomaten, Monetomaten, Schachermaten und Chefomaten.\aDu kannst sie an ihrer Färbung und ihren Namensschildern erkennen.\aGeh mal los und besiege zur Übung 4 Rechtomaten."},
    168 : {QUEST : "Toll, wie du diese Bots vertrieben hast!\aWeißt du, es gibt vier Arten von Bots.\a Rechtomaten, Monetomaten, Schachermaten und Chefomaten.\aDu kannst sie an ihrer Färbung und ihren Namensschildern erkennen.\aGeh mal los und besiege zur Übung 4 Schachermaten."},
    169 : {QUEST : "Toll, wie du diese Bots vertrieben hast!\aWeißt du, es gibt vier Arten von Bots.\a Rechtomaten, Monetomaten, Schachermaten und Chefomaten.\aDu kannst sie an ihrer Färbung und ihren Namensschildern erkennen.\aGeh mal los und besiege zur Übung 4 Monetomaten."},
    170 : {QUEST : "Toll, jetzt kennst du den Unterschied zwischen den 4 Bot-Arten.\aIch glaube, du kannst jetzt für deinen dritten Gag-Ablauf trainieren.\aSprich mal mit _toNpcName_, bevor du deinen nächsten Gag-Ablauf wählst - er kann dich fachkundig beraten._where_" },
    171 : {QUEST : "Toll, jetzt kennst du den Unterschied zwischen den 4 Bot-Arten.\aIch glaube, du kannst jetzt für deinen dritten Gag-Ablauf trainieren.\aSprich mal mit _toNpcName_, bevor du deinen nächsten Gag-Ablauf wählst - er kann dich fachkundig beraten._where_" },
    172 : {QUEST : "Toll, jetzt kennst du den Unterschied zwischen den 4 Bot-Arten.\aIch glaube, du kannst jetzt für deinen dritten Gag-Ablauf trainieren.\aSprich mal mit _toNpcName_, bevor du deinen nächsten Gag-Ablauf wählst - sie kann dich fachkundig beraten._where_" },

    175 : {GREETING : "",
           QUEST : "Wusstest du schon, dass du dein eigenes Toon-Haus besitzt?\aKlarabella Kuh betreibt einen Katalog, aus dem du per Telefon Möbel zum Einrichten deines Hauses bestellen kannst.\aDu kannst aber auch Schnell-Chat-Sprüche, Kleidung und andere lustige Dinge kaufen.\aIch sage Klarabella, dass sie dir sofort deinen ersten Katalog schicken soll.\aJede Woche erhältst du einen Katalog mit neuen Gegenständen!\aGeh in dein Haus und rufe von dort aus Klarabella an.",
           INCOMPLETE_PROGRESS : "Geh nach Hause und rufe von dort Klarabella an.",
           COMPLETE : "Es macht dir bestimmt Spaß, bei Klarabella etwas zu bestellen!\aIch habe gerade mein Haus neu eingerichtet. Es sieht toontastisch aus!\aLöse weiterhin Toon-Aufgaben, um noch mehr Belohnungen zu bekommen!",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "Werfen und Spritzen ist toll, aber du wirst noch mehr Gags brauchen, wenn du gegen höhere Bots kämpfen willst.\aWenn du dich mit anderen Toons gegen die Bots zusammenschließt, dann könnt ihr die Angriffe kombinieren und dadurch noch mehr Schaden anrichten.\aProbiert verschiedene Gag-Kombinationen aus, um herauszufinden, was am besten funktioniert.\aWähle für deinen nächsten Ablauf zwischen Volldröhnen und Aufheitern.\aVolldröhnen ist etwas Besonders, weil alle Bots beschädigt werden, wenn es trifft.\aMit Aufheitern kannst du andere Toons im Kampf heilen.\aWenn du für deine Entscheidung bereit bist, komm wieder her und wähle.",
           INCOMPLETE_PROGRESS : "Schon wieder hier? Okay, bist du zum Auswählen bereit?",
           INCOMPLETE_WRONG_NPC : "Denke gut nach, ehe du wählst.",
           COMPLETE : "Gute Wahl. Bevor du nun diese Gags einsetzen kannst, musst du dafür trainieren.\aDazu musst du eine Reihe von Toon-Aufgaben lösen.\aBei jeder Aufgabe erhältst du ein Bild deines Gag-Ablaufs.\aWenn du alle 15 sammelst, kannst du die Aufgabe für das Gag-Abschlusstraining erhalten, bei der du alle deine neuen Gags einsetzen kannst.\aDeine Fortschritte kannst du im Sticker-Buch sehen.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Besuche _toNpcName_, wenn du dich leichter durch die Stadt bewegen willst._where_" },
    1040 : { QUEST : "Besuche _toNpcName_, wenn du dich leichter durch die Stadt bewegen willst._where_" },
    1041 : { QUEST : "Hi! Was führt dich hierher?\aAlle benutzen ihr tragbares Loch, um sich durch die Stadt zu bewegen.\aAlso, du kannst dich mit der Freunde-Liste zu deinen Freunden teleportieren oder auch mit dem Stadtplan im Sticker-Buch in jede andere Gegend.\aNatürlich musst du dir das erst verdienen!\aHör mal, ich kann deinen Teleport-Zugang zu Toontown Mitte einschalten, wenn du einem Freund von mir hilfst.\aAnscheinend machen die Bots drüben in der Hohlgasse Ärger. Geh mal zu _toNpcName_._where_" },
    1042 : { QUEST : "Hi! Was führt dich hierher?\aAlle benutzen ihr tragbares Loch, um sich durch die Stadt zu bewegen.\aAlso, du kannst dich mit der Freunde-Liste zu deinen Freunden teleportieren oder auch mit dem Stadtplan im Sticker-Buch in jede andere Gegend.\aNatürlich musst du dir das erst verdienen!\aHör mal, ich kann deinen Teleport-Zugang zu Toontown Mitte einschalten, wenn du einem Freund von mir hilfst.\aAnscheinend machen die Bots drüben in der Hohlgasse Ärger. Geh mal zu _toNpcName_._where_" },
    1043 : { QUEST : "Hi! Was führt dich hierher?\aAlle benutzen ihr tragbares Loch, um sich durch die Stadt zu bewegen.\aAlso, du kannst dich mit der Freunde-Liste zu deinen Freunden teleportieren oder auch mit dem Stadtplan im Sticker-Buch in jede andere Gegend.\aNatürlich musst du dir das erst verdienen!\aHör mal, ich kann deinen Teleport-Zugang zu Toontown Mitte einschalten, wenn du einem Freund von mir hilfst.\aAnscheinend machen die Bots drüben in der Hohlgasse Ärger. Geh mal zu _toNpcName_._where_" },
    1044 : { QUEST : "Oh, danke, dass du vorbeikommst. Ich brauche wirklich Hilfe.\aWie du sehen kannst, habe ich keine Kunden.\aMein geheimes Rezeptbuch ist weg und keiner kommt mehr in mein Restaurant.\aIch habe es zuletzt kurz bevor diese Bots mein Gebäude übernahmen gesehen.\aKannst du mir helfen und vier meiner berühmten Rezepte zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hattest du schon Glück mit meinen Rezepten?" },
    1045 : { QUEST : "Herzlichen Dank!\aBald werde ich die gesamte Sammlung zurückhaben und mein Restaurant wieder aufmachen.\aOh, ich habe hier eine Nachricht für dich - irgendwas über Teleport-Zugang?\aDa steht - danke, dass du meinem Freund geholfen hast, gib das hier jetzt in Toontown-Zentrale ab.\aAlso wirklich vielen Dank - Tschüss!",
             LEAVING : "",
             COMPLETE : "Ach ja, es heißt hier, dass du den netten Leute in der Hohlgasse einen großen Dienst erwiesen hast.\aDa steht, dass du einen Teleport-Zugang nach Toontown Mitte brauchst.\aAlso, du kannst das als erledigt betrachten.\aDu kannst dich jetzt von fast überall aus Toontown zum Spielplatz zurück teleportieren.\aSchlag einfach deinen Stadtplan auf und klicke auf Toontown Mitte." },
    1046 : { QUEST : "Die Monetomaten belästigen die ganze Zeit die Spielgeld-Bausparkasse.\aSchau mal dort vorbei und sieh zu, ob du irgendetwas tun kannst._where_" },
    1047 : { QUEST : "Monetomaten haben sich immer wieder in die Bank geschlichen und unsere Maschinen gestohlen.\aBitte hole 5 Rechenmaschinen von den Monetomaten zurück.\aDamit du nicht immer hin und zurück rennen musst, bring sie einfach alle auf einmal zurück.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Suchst du immer noch Rechenmaschinen?" },
    1048 : { QUEST : "Wow! Danke, dass du unsere Rechenmaschinen gefunden hast.\aHm ... Die sehen ein bißchen beschädigt aus.\aSag mal, könntest du sie rüber zu _toNpcName_ bringen, in ihren Laden \"Kitzelmaschinen\" hier in der Straße?\aVielleicht bekommt sie die wieder hin.",
             LEAVING : "", },
    1049 : { QUEST : "Was ist denn das? Kaputte Rechenmaschinen? \aMonetomaten, sagst du?\aNaja, woll'n mal nachsehen...\aTja, Getriebe rausgenommen, aber ich hab diese Teile nicht mehr ...\aWeißt du, was gehen könnte - ein paar Bot-Zahnräder, große, von größeren Bots ...\aBot-Zahnräder von Level 3 müssten gehen. Ich brauch 2 für jede Maschine, also insgesamt 10.\aBring sie alle auf einmal her, dann mach ich die Dinger klar!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Denk dran, ich brauch 10 Zahnräder, um die Maschinen zu reparieren." },
    1053 : { QUEST : "Ah ja, das dürfte jetzt klappen.\aAlles fertig, und das kostenlos.\aNimm sie wieder mit zu Spielgeld und sag ihnen `nen schönen Gruß von mir.",
             LEAVING : "",
             COMPLETE : "Rechenmaschinen alle repariert?\aGut gemacht. Ich bin sicher, dass ich hier irgendwo was habe, womit ich dich belohnen kann ... " },
    1054 : { QUEST : "_toNpcName_ braucht Hilfe bei seinen Clownautos._where_" },
    1055 : { QUEST : "Mannomann! Kann die Reifen zu diesem komischen Clownauto nicht finden!\aMeinste, du könntest mir mal helfen?\aDussel-Bob hat sie wohl in den Teich auf'm Spielplatz von Toontown Mitte geschmissen.\aWenn du dich da auf so'n Dock stellst, kannst du die Reifen vielleicht für mich rausfischen.",
             GREETING : "Huhu!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du Probleme, alle 4 Reifen rauszufischen?" },
    1056 : { QUEST : "Fan-kuchen-tastisch! Jetzt krieg ich dieses olle Clownauto wieder ins Rollen!\aHey, ich dachte, ich hätte hier mal `ne Luftpumpe gehabt, um diese Reifen aufzupumpen ...\aVielleicht hat _toNpcName_ sie sich ausgeliehen?\aKönntest du mal hingehen und sie für mich zurückholen?_where_",
             LEAVING : "" },
    1057 : { QUEST : "Tag.\aEine Reifenpumpe, sagst du?\aIch hab `ne Idee - du hilfst mir, ein paar von diesen höheren Bots von der Straße zu räumen ...\aUnd ich geb dir die Reifenpumpe.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Besser geht's nicht?" },
    1058 : { QUEST : "Gute Arbeit - ich wusste, dass du das schaffst.\aHier ist die Pumpe. Ich bin sicher, _toNpcName_ wird sich freuen, sie wieder zurück zu bekommen.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Jippieh! Jetzt kann's losgehen!\aÜbrigens vielen Dank für deine Hilfe.\aHier, nimm das." },
    1059 : { QUEST : "_toNpcName_ gehen die Vorräte aus. Vielleicht kannst du ihm mal helfen?_where_" },
    1060 : { QUEST : "Danke, dass du vorbeikommst!\aDiese Bots haben meine Tinte gestohlen, jetzt geht sie mir fast aus.\aKönntest du für mich etwas Tintenfischtinte aus dem Teich fischen?\aStell dich zum Fischen einfach auf ein Dock am Teich.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du ein Problem beim Fischen?" },
    1061 : { QUEST : "Große Klasse - danke für die Tinte!\aWeißt du was, wenn du vielleicht ein paar von diesen Griffelschiebern aus dem Weg räumen könntest ...\aDann würde mir die Tinte nicht wieder so schnell ausgehen.\aFür deine Belohnung musst du 6 Griffelschieber in Toontown Mitte besiegen.",
             LEAVING : "",
             COMPLETE : "Danke! Ich möchte dich für deine Hilfe belohnen.",
             INCOMPLETE_PROGRESS : "Ich hab grad noch ein paar Griffelschieber gesehen." },
    1062 : { QUEST : "Große Klasse - danke für die Tinte!\aWeißt du was, wenn du vielleicht ein paar von diesen Blutsaugern aus dem Weg räumen könntest ...\aDann würde mir die Tinte nicht wieder so schnell ausgehen.\aFür deine Belohnung musst du 6 Blutsauger in Toontown Mitte besiegen.",
             LEAVING : "",
             COMPLETE : "Danke! Ich möchte dich für deine Hilfe belohnen.",
             INCOMPLETE_PROGRESS : "Ich hab grad noch ein paar Blutsauger gesehen. " },
    900 : { QUEST : "Ich habe gehört, _toNpcName_ braucht Hilfe mit einem Paket._where_" },
    1063 : { QUEST : "Hi - danke, dass du rein gekommen bist. Ein Bot hat mir ein sehr wichtiges Paket direkt unter der Nase weg gestohlen.\aBitte sieh doch mal zu, ob du es zurückholen kannst. Ich glaube, es war einer von Level 3 ...\aAlso erledige Bots von Level 3, bis du mein Paket findest.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Erfolg bei der Suche nach meinem Paket, was?" },
    1067 : { QUEST : "Na, da ist es ja!\aHey, die Adresse ist verschmiert ...\aIch kann nur noch entziffern, dass es für einen Dr. ist - der Rest ist unleserlich.\aVielleicht ist es für _toNpcName_? Könntest du es zu ihm bringen?_where_",
             LEAVING : "" },
    1068 : { QUEST : "Ich erwarte kein Paket. Vielleicht ist es für Dr. B. Geistert?\aMein Assistent geht sowieso heute rüber, da lasse ich ihn das für dich klären.\aWärst du vielleicht so nett, ein paar von den Bots in meiner Straße zu verjagen?\aVertreibe 10 Bots in Toontown Mitte.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mein Assistent ist noch nicht zurück." },
    1069 : { QUEST : "Dr. B. Geistert sagt, er erwarte auch kein Paket.\aLeider hat ein Monetomat es meinem Assistenten auf dem Rückweg weggenommen.\aKönntest du versuchen, es zurückzubekommen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Erfolg bei der Suche nach dem Paket, was?" },
    1070 : { QUEST : "Dr. B. Geistert sagt, er erwarte auch kein Paket.\aLeider hat ein Schachermat es meinem Assistenten auf dem Rückweg weggenommen.\aTut mir leid, aber du wirst diesen Schachermaten finden und das Paket zurückholen müssen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Erfolg bei der Suche nach dem Paket, was?" },
    1071 : { QUEST : "Dr. B. Geistert sagt, er erwarte auch kein Paket.\aLeider hat ein Chefomat es meinem Assistenten auf dem Rückweg weggenommen.\aKönntest du versuchen, es zurückzubekommen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Erfolg bei der Suche nach dem Paket, was?" },
    1072 : { QUEST : "Großartig - du hast es wieder!\aVielleicht solltest du es mal bei _toNpcName_ versuchen, es könnte für ihn sein._where_",
             LEAVING : "" },
    1073 : { QUEST : "Oh, danke, dass du mir meine Pakete bringst.\aWarte mal, ich habe zwei erwartet. Könntest du mal bei _toNpcName_ nachprüfen, ob er vielleicht das andere hat?",
             INCOMPLETE : "Hast du mein anderes Paket finden können?",
             LEAVING : "" },
    1074 : { QUEST : "Er hat gesagt, dass es noch ein Paket gab? Vielleicht haben das auch die Bot gestohlen.\aErledige Bots, bis du das zweite Paket findest.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Erfolg bei der Suche nach dem anderen Paket, was?" },
    1075 : { QUEST : "Offenbar gab es nun doch ein zweites Paket!\aBringe es schnell rüber zu _toNpcName_ und sage ihm, es täte mir Leid.",
             COMPLETE : "Hey, da ist ja mein Paket!\aDa du anscheinend ein sehr hilfsbereiter Toon bist, wirst du das hier brauchen können.",
             LEAVING : "" },
    1076 : { QUEST : "Drüben beim 14-Karat-Goldfisch hat es Ärger gegeben.\a_toNpcName_ könnte wahrscheinlich Hilfe gebrauchen._where_" },
    1077 : { QUEST : "Danke, dass du gekommen bist - die Bots haben alle meine Goldfische gestohlen.\aIch vermute, die Bots möchten sie verkaufen, um schnell Kohle zu machen.\aDiese 5 Fische waren so viele Jahre lang meine einzige Gesellschaft in diesem winzigen Laden ...\aWenn du sie für mich zurückholen könntest, wäre ich dir wirklich sehr dankbar.\aIch bin sicher, dass einer der Bots meine Fische hat.\aVerjage Bots, bis du meine Goldfische findest.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Bitte bring mir meine Goldfische wieder." },
    1078 : { QUEST : "Oh, du hast meine Fische!\aHä? Was ist das - eine Quittung?\aSeufz, naja, am Ende handelt es sich ja um Bots.\aIch werd aus dieser Quittung einfach nicht schlau. Könntest du sie mal zu _toNpcName_ bringen, vielleicht kann er sie lesen?_where_",
             INCOMPLETE : "Was hat _toNpcName_ zu der Quittung gesagt?",
             LEAVING : "" },
    1079 : { QUEST : "Mmh, lass mich mal diese Quittung sehen.\a...Ah ja, hier steht, dass 1 Goldfisch an einen gewissen Kriecher verkauft wurde.\aDie anderen 4 Fische werden aber anscheinend nicht erwähnt.\aVielleicht solltest du versuchen, diesen Kriecher zu finden.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich glaube nicht, dass es noch etwas gibt, womit ich dir helfen kann.\aWarum versuchst du nicht, diesen Goldfisch zu finden?" },
    1092 : { QUEST : "Mmh, lass mich mal diese Quittung sehen.\a...Ah ja, hier steht, dass 1 Goldfisch an einen gewissen Keinmünz verkauft wurde.\aDie anderen 4 Fische werden aber anscheinend nicht erwähnt.\aVielleicht solltest du versuchen, diesen Keinmünz zu finden.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich glaube nicht, dass es noch etwas gibt, womit ich dir helfen kann.\aWarum versuchst du nicht, diesen Goldfisch zu finden?" },
    1080 : { QUEST : "Oh, dem Himmel sei Dank! Du hast Oscar gefunden - er ist mein Liebling.\aWas sagst du, Oscar? Aha ... wirklich? ... da sind sie?\aOscar sagt, die anderen 4 sind in den Teich auf dem Spielplatz entwischt.\aKönntest du sie für mich einfangen?\aFische sie einfach aus dem Teich.",
             LEAVING : "",
             COMPLETE : "Ach, ich bin ja sooo froh! Wieder vereint zu sein mit meinen kleinen Freunden!\aDafür verdienst du eine hübsche Belohnung!",
             INCOMPLETE_PROGRESS : "Hast du Probleme, diese Fische zu finden?" },
    1081 : { QUEST : "_toNpcName_ scheint festzusitzen. Sie könnte bestimmt eine helfende Hand gebrauchen._where_" },
    1082 : { QUEST : "Ich hab Kleber verkleckert und jetzt steck ich fest - ei, der Daus!\aIch würd alles drum geben, käm ich hier raus.\aIch hab `ne Idee, vielleicht hilfst du mir'n Stück.\aSchlag ein paar Schachermaten und komm mit Öl zurück.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Kannst du mir helfen, mich zu entkleben?" },
    1083 : { QUEST : "Öl war schon gut, doch komm ich nicht los.\aWas würde noch helfen, was mach ich denn bloß?\aIch hab `ne Idee, wärst du wohl so nett.\aSchlag ein paar Rechtomaten und bringe mir Fett.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Kannst du mir helfen, mich zu entkleben?" },
    1084 : { QUEST : "Nö, keine Chance - nichts hat sich bewegt.\aIch hab das Fett auf die Moneten gelegt.\aApropos Moneten, wir machen es nasser.\aSchlag ein paar Monetomaten und bringe mir Wasser.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Hurra, ich bin frei von diesem Leim!\aZur Belohnung wird dies Geschenk jetzt dein,\aDu kannst länger lachen beim Kampfe, und dann ...\aOh nein! Ich kleb ja schon wieder an!",
             INCOMPLETE_PROGRESS : "Kannst du mir helfen, mich zu entkleben?" },
    1085 : { QUEST : "_toNpcName_ führt Forschungen über die Bots durch.\aWenn du helfen willst, geh hin und sprich mal mit ihm._where_" },
    1086 : { QUEST : "Das ist richtig, ich führe eine Studie zu den Bots durch.\aIch möchte wissen, was sie in Gang setzt.\aEs würde mir auf jeden Fall helfen, wenn du ein paar Bot-Zahnräder sammeln könntest.\aAchte darauf, dass sie mindestens von Bots des Level 2 sind, damit sie für die Untersuchung groß genug sind.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kannst du nicht genügend Zahnräder auftreiben?" },
    1089 : { QUEST : "Okay, da wollen wir mal sehen. Das sind ja hervorragende Exemplare!\aMmm...\aOkay, hier ist mein Bericht. Bringe ihn gleich zur Toontown-Zentrale.",
             INCOMPLETE : "Hast du meinen Bericht in Toontown-Zentrale gebracht?",
             COMPLETE : "Gute Arbeit, _avName_, wir übernehmen jetzt.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ hat nützliche Informationen für dich._where_" },
    1091 : { QUEST : "Ich habe gehört, dass die Toontown-Zentrale an einer Art Bot-Radar arbeitet.\aDamit sieht man, wo sich die Bots aufhalten, so dass man sie leichter finden kann.\aDie Bot-Seite in deinem Sticker-Buch ist der Schlüssel dazu.\aWenn du genügend Bots bezwingst, kannst du ihre Signale empfangen und verfolgen, wo sie sind.\aBesiege weiterhin Bots, dann bist du dafür bereit.",
             COMPLETE : "Gute Arbeit! Das hier kannst du wahrscheinlich brauchen ...",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "Jetzt kannst du den nächsten Gag-Ablauf auswählen, den du lernen möchtest.\aNimm dir Zeit für die Entscheidung und komm zurück, wenn du bereit bist zu wählen.",
           INCOMPLETE_PROGRESS : "Denke gut nach, ehe du wählst.",
           INCOMPLETE_WRONG_NPC : "Denke gut nach, ehe du wählst.",
           COMPLETE : "Eine kluge Entscheidung ...",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "Diese hinterlistigen Bots haben wieder zugeschlagen.\a_toNpcName_ hat einen weiteren verschwundenen Gegenstand gemeldet. Schau mal dort vorbei, ob du das regeln kannst._where_" },
    2202 : { QUEST : "Hi, _avName_. Gott sei Dank bist du hier. Ein gemeiner Pfennigfuchser kam grad hier rein und machte sich mit einem Schlauch davon.\aIch habe den Verdacht, dass sie den für ihre üblen Zwecke verwenden wollen.\aBitte versuche ihn zu finden und bring den Schlauch zurück.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du meinen Schlauch schon gefunden?",
             COMPLETE : "Du hast meinen Schlauch gefunden! Du BIST gut! Hier, deine Belohnung ...",
             },
    2203 : { QUEST : "Die Bots verursachen drüben in der Bank das totale Chaos.\aSuche Käpt'n Karl auf und schau mal, was du tun kannst._where_" },
    2204 : { QUEST : "Willkommen an Bord, Kamerad!\aMist! Diese Halunken von Bots haben mein Monokel zerschmissen und ich kann so mein Kleingeld nicht sortieren. \aSei eine nette Landratte und bring dieses Rezept zu Dr. Queequeg und hol mir ein neues._where_",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "Was ist das?\aAch, ich würde das Rezept ja gern einlösen, aber die Bots haben mein Lager geplündert.\aWenn du mir das Brillengestell von einem Kriecher bringst, kann ich vielleicht helfen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tut mir Leid. Kein Kriechergestell, kein Monokel.",
             },
    2206: { QUEST : "Ausgezeichnet!\aEinen Moment ...\aDein Rezept ist hiermit eingelöst. Bitte nimm dieses Monokel gleich mit zu Käpt'n Karl._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "Fest!\aDa verdienst du dir ja tatsächlich deine Seefestigkeit.\aHier hast du.",
            },
    2207 : { QUEST : "Bernikel-Barbara hat einen Bot in ihrem Laden!\aDu solltest mal rübergehen, und zwar pronto._where_" },
    2208 : { QUEST : "Menschenskind! Du hast ihn genau verpasst, Schätzchen.\aEs war ein Heimtücker hier. Er nahm meine große weiße Perücke mit.\aEr sagte, sie sei für seinen Chef, und irgendwas von 'Präzedenzfall.'\aWenn du sie zurückbringen könntest, wäre ich dir ewig dankbar.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Hast du ihn immer noch nicht gefunden?\aEr ist groß und hat einen Eierkopf.",
             COMPLETE : "Gefunden!?!?\aDu bist ein echter Schatz!\aDu hast dir das hier mehr als verdient ...",
             },
    2209 : { QUEST : "Melville bereitet sich auf eine wichtige Reise vor.\aGeh hin und sieh mal, wie du ihm helfen kannst._where_"},
    2210 : { QUEST : "Ich kann deine Hilfe brauchen.\aDie Toon-Zentrale hat mich gebeten, eine Reise zu machen und herauszufinden, woher die Bots kommen.\aIch brauch ein paar Sachen für mein Schiff, aber ich habe nicht viele Jelly Beans.\aGeh mal zu Alice und hol etwas Ballast. Du wirst ihr einen Gefallen tun müssen, damit du ihn bekommst._where_",
             GREETING : "Wie geht's, wie steht's, _avName_",
             LEAVING : "",
             },
    2211 : { QUEST : "Melville will also Ballast?\aEr schuldet mir noch was für das letzte Bündel.\aIch geb's dir aber, wenn du fünf Mikromanager aus meiner Straße entfernen kannst.",
             INCOMPLETE_PROGRESS : "Nein, Dummchen! Ich sagte FÜNF Mikromanager ...",
             GREETING : "Was kann ich für dich tun?",
             LEAVING : "",
             },
    2212 : { QUEST : "Abgemacht ist abgemacht.\aHier ist dein Ballast für diesen Geizhals Melville._where_",
             GREETING : "Na, wer kommt denn da ...",
             LEAVING : "",
             },
    2213 : { QUEST : "Hervorragende Arbeit. Ich wusste, dass sie vernünftig sein wird.\aAls nächstes brauche ich eine Seekarte von Art.\aIch glaube, mit meinem Kredit sieht es dort auch nicht so günstig aus. Du wirst wohl was mit ihm aushandeln müssen._where_",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Ja, ich habe die Seekarte, die Melville braucht.\aUnd wenn du bereit bist, dafür zu arbeiten, bekommst du sie auch.\aIch versuche gerade, ein Astrolabium zu bauen, um mich an den Sternen zu orientieren.\aIch könnte dafür drei Bot-Zahnräder gebrauchen.\aKomm wieder, wenn du sie hast.",
             INCOMPLETE_PROGRESS: "Wie steht's mit den Bot-Zahnrädern?",
             GREETING : "Willkommen!",
             LEAVING : "Viel Glück!",
             },
    2215 : { QUEST : "Oha! Diese Zahnräder sind wirklich gut geeignet.\aHier ist die Karte. Gib sie Melville mit freundlichen Grüßen._where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "Nun, damit hätten wir's. Ich bin fertig zum Ablegen!\aWenn du nicht so grün wärst, würde ich dich mitnehmen. Nimm stattdessen das hier.",
             },
    901 : { QUEST : "Wenn du meinst du kannst das - Ahab könnte drüben bei sich ein bisschen Unterstützung gebrauchen ..._where_",
            },
    2902 : { QUEST : "Bist du der Neue?\aGut, gut. Vielleicht kannst du mir helfen.\aIch baue gerade eine riesige fabelhafte Seekrabbe, um die Bots zu verwirren.\aIch könnte allerdings noch einen Webeleinstek brauchen. Geh mal bitte zu Gert und bring einen mit._where_",
             },
    2903 : { QUEST : "Tagchen!\aJa, ich habe von der Riesenkrabbe gehört, an der Ahab arbeitet.\aDer beste Webeleinstek, den ich habe, ist aber ein wenig angeschmuddelt.\aSei so nett und lass ihn erst reinigen, bevor du ihn dort abgibst._where_",
             LEAVING : "Danke!"
             },
    2904 : { QUEST : "Du musst der sein, den Gert geschickt hat.\aIch denke, ich kann das schnell reinigen.\aEinen Moment ...\aBitte schön. So gut wie neu!\aSag Ahab schönen Gruß von mir._where_",
             },
    2905 : { QUEST : "Ah, das ist ja genau, was ich suche.\aDa du einmal hier bist, ich brauche auch noch eine sehr große Uhrfeder.\aSpazier doch mal rüber zu Hook und frag ihn, ob er eine hat._where_",
             },
    2906 : { QUEST : "Eine große Sprungfeder, was?\aTut mir leid, aber die größte Feder, die ich habe, ist immer noch ziemlich klein.\aVielleicht könnte ich eine aus Spritzpistolenabzugsfedern zusammenbauen.\aBring mir drei von diesen Gagdingern, und ich seh zu, was ich tun kann.",
             },
    2907 : { QUEST : "Na, woll'n mal schauen ...\aToll. Einfach toll.\aManchmal bin ich von mir selbst überrascht.\aBitteschön: Eine große Sprungfeder für Ahab!_where_",
             LEAVING : "Bon Voyage!",
             },
     2911 : { QUEST : "Ich würde ja gern was für die gute Sache tun, _avName_.\aAber ich fürchte, die Straßen sind nicht mehr sicher.\aWarum bezwingst du nicht ein paar Monetomaten-Bots, dann reden wir drüber.",
             INCOMPLETE_PROGRESS : "Ich glaube immer noch, du musst die Straßen sicherer machen.",
             },
    2916 : { QUEST : "Ja, ich habe ein Gewicht, das Ahab haben kann.\aAber ich denke, es wäre sicherer, wenn du erst ein paar Schachermaten vertreibst.",
             INCOMPLETE_PROGRESS : "Noch nicht. Erledige erst noch ein paar Schachermaten.",
             },
    2921 : { QUEST : "Hmmm, ich denke, ich könnte ein Gewicht abgeben.\aIch hätte aber ein besseres Gefühl dabei, wenn hier nicht so viele Chefomaten herumschleichen würden.\aBezwinge sechs und komm dann wieder zu mir.",
             INCOMPLETE_PROGRESS : "Ich glaube nicht, dass es schon sicher ist ... ",
             },
    2925 : { QUEST : "Fertig?\aNa, ich denke, jetzt ist es sicher genug.\aHier ist das Gegengewicht für Ahab._where_"
             },
    2926 : {QUEST : "Nun, das ist alles.\aWoll'n mal sehen, ob es jetzt geht.\aHmmm, noch ein kleines Problem.\aIch habe keinen Strom, weil das Bot-Gebäude meine Solarzellen blockiert.\aKannst du es für mich zurückerobern?",
            INCOMPLETE_PROGRESS : "Immer noch kein Strom. Was ist mit dem Gebäude?",
            COMPLETE : "Super! Du bist ja ein echter Bot-Zerstörer! Hier, nimm das als Belohnung ...",
            },
    3200 : { QUEST : "Ich hab grad einen Anruf von _toNpcName_ bekommen.\aEr hat einen schweren Tag. Vielleicht kannst du ihm helfen!\aGeh mal hin und schau, was er braucht._where_" },
    3201 : { QUEST : "Oh, danke, dass du gekommen bist!\aIch brauche jemanden, der diese neue Seidenkrawatte zu _toNpcName_ bringt.\aKönntest du das für mich tun?_where_" },
    3203 : { QUEST : "Oh, das muss die Krawatte sein, die ich bestellt habe! Danke!\aSie passt zu einem Nadelstreifenanzug, den ich gerade fertiggestellt habe, da drüben.\aHe, was ist denn mit dem Anzug passiert?\aOch nein! Die Bots müssen meinen neuen Anzug gestohlen haben!\aJage Bots, bis du meinen Anzug findest, und bring ihn zu mir zurück.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du meinen Anzug schon gefunden? Ich bin sicher, dass die Bots ihn geholt haben!",
             COMPLETE : "Hurra! Du hast meinen neuen Anzug gefunden!\aSiehste, ich hab dir doch gesagt, dass die Bots ihn haben! Hier ist deine Belohnung ... ",
             },

    3204 : { QUEST : "_toNpcName_ hat grad angerufen, um einen Diebstahl zu melden.\aGeh doch mal rüber und schau, ob du die Sache wieder in Ordnung bringen kannst?_where_" },
    3205 : { QUEST : "Hallo, _avName_! Willst du mir helfen?\aIch habe gerade einen Blutsauger aus meinem Laden gejagt. Hui, das war vielleicht gruselig!\aAber jetzt kann ich meine Schere nirgends finden! Ich bin sicher, der Blutsauger hat sie genommen.\aFinde den Blutsauger und erobere mir meine Schere zurück.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Suchst du noch nach meiner Schere?",
             COMPLETE : "Meine Schere! Hab vielen Dank! Hier ist deine Belohnung ... ",
             },

    3206 : { QUEST : "Es klingt, als hätte _toNpcName_ gerade ein Problem mit ein paar Bots.\aSchau mal nach, ob du ihm helfen kannst._where_" },
    3207 : { QUEST : "Hi, _avName_! Danke für's Herkommen!\aEin paar Dummschwätzer sind grad bei mir eingebrochen und haben einen Stapel Postkarten von meiner Theke geklaut.\aBitte geh los und jag alle Dummschwätzer meine Postkarten zurück bekomme!",
             INCOMPLETE_PROGRESS : "Das sind noch nicht alle Postkarten! Such weiter!",
             COMPLETE : "Oh, danke! Jetzt kann ich die Post pünktlich ausliefern! Hier ist deine Belohnung ... ",
             },

    3208 : { QUEST : "Wir bekommen in letzter Zeit Beschwerden von den Anwohnern über diese ganzen Aufschwatzer.\aSieh mal zu, ob du 10 Aufschwatzer vertreiben kannst, um deinen Mit-Toons in Daisys Gärten zu helfen." },
    3209 : { QUEST : "Danke, dass du dich um diese Aufschwatzer gekümmert hast!\aJetzt sind aber die Telemarketer außer Kontrolle geraten.\aErledige 10 Telemarketer in Daisys Gärten und komm wieder her, um deine Belohnung abzuholen." },

    3247 : { QUEST : "Wir bekommen in letzter Zeit Beschwerden von den Anwohnern über diese ganzen Blutsauger.\aSieh mal zu, ob du 20 Blutsauger vertreiben kannst, um deinen Mit-Toons in Daisys Gärten zu helfen." },


    3210 : { QUEST : "Oh nein, der Spritzblume in der Ahornstraße sind gerade die Blumen ausgegangen!\aBring ihnen zehn von deinen eigenen Spritzblumen hin, um ihnen zu helfen.\aDu musst aber erst 10 Spritzblumen in deinem Lager haben.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "Ich brauche 10 Spritzblumen. Du hast nicht genug!" },
    3211 : { QUEST : "Oh, vielen Dank! Diese Spritzblumen sind unsere Rettung.\aAber ich fürchte mich vor den Bots da draußen.\aKannst du mir helfen und ein paar von den Bots vertreiben?\aKomm wieder zu mir, wenn du 20 Bots in dieser Straße erledigt hast.",
             INCOMPLETE_PROGRESS : "Es sind da draußen immer noch Bots übrig! Mach weiter!",
             COMPLETE : "Oh, vielen Dank! Das ist eine große Hilfe. Deine Belohnung ist ...",
             },

    3212 : { QUEST : "_toNpcName_ hat etwas verloren und braucht Hilfe bei der Suche.\aGeh mal hin und schau, was du tun kannst._where_" },
    3213 : { QUEST : "Hi, _avName_. Kannst du mir helfen?\aIch habe anscheinend meinen Stift verlegt. Möglicherweise haben ihn die Bots weggenommen.\aVertreibe Bots, bis du meinen gestohlenen Stift wiederfindest.",
             INCOMPLETE_PROGRESS : "Hast du meinen Stift schon gefunden?" },
    3214 : { QUEST : "Ja, das ist mein Stift! Vielen Dank!\aAls du weg warst, habe ich aber gemerkt, dass auch mein Tintenfass fehlt.\aVertreibe Bots, um mein Tintenfass zu finden.",
             INCOMPLETE_PROGRESS : "Ich suche immer noch nach meinem Tintenfass!" },
    3215 : { QUEST : "Großartig! Jetzt habe ich meinen Stift und mein Tintenfass wieder.\aAber weißt du was?\aJetzt ist mein Schreibblock weg! Sie müssen ihn auch gestohlen haben!\aSuche die Bots, um meinen gestohlenen Schreibblock zu finden, und dann bringe ihn zu mir zurück und hole dir deine Belohnung ab.",
             INCOMPLETE_PROGRESS : "Irgendetwas Neues vom Schreibblock? " },
    3216 : { QUEST : "Das ist mein Schreibblock! Hurra! Deine Belohnung ist ...\aHe! Wo ist sie denn hin?\aIch hatte deine Belohnung direkt hier in meiner verschließbaren Kassette. Aber die Kassette ist weg!\aDas ist doch nicht zu glauben! Diese Bots haben deine Belohnung gestohlen!\aJage die Bots und hole meine Kassette zurück.\aWenn du sie mir zurückbringst, gebe ich dir deine Belohnung.",
             INCOMPLETE_PROGRESS : "Such weiter nach dieser Kassette! Da ist deine Belohnung drin!",
             COMPLETE : "Na endlich! Ich hatte deine neue Gagtasche in der Kassette. Hier ist sie ...",
             },

    3217 : { QUEST : "Wir haben ein paar Studien zur Schachermat-Mechanik durchgeführt.\aWir müssen uns einige Teile noch näher ansehen.\aBring uns einen Kettenradzahn von einem Wichtigtuer.\aDu kannst dir eins holen, wenn der Bot explodiert." },
    3218 : { QUEST : "Gute Arbeit! Wir brauchen jetzt zum Vergleich einen Zahn von einem Glückshändchen.\aDiese Zähne sind schwerer zu holen, aber lass dich nicht entmutigen." },
    3219 : { QUEST : "Großartig! Jetzt brauchen wir nur noch einen Zahn.\aDiesmal brauchen wir einen von einem Aufbauscher.\aDu musst möglicherweise in ein paar Schachermat-Gebäude hineinschauen, um diese Bots zu finden.\aWenn du einen Zahn hast, bring ihn her und hol dir deine Belohnung ab." },

    3244 : { QUEST : "Wir haben ein paar Studien zur Rechtomat-Mechanik durchgeführt.\aWir müssen uns einige Teile noch näher ansehen.\aBring uns einen Kettenradzahn von einem Unfallabzocker.\aDu kannst dir eins holen, wenn der Bot explodiert." },
    3245 : { QUEST : "Gute Arbeit! Wir brauchen jetzt zum Vergleich einen Zahn von einem Heimtücker.\aDiese Zähne sind schwerer zu holen, aber lass dich nicht entmutigen." },
    3246 : { QUEST : "Großartig! Jetzt brauchen wir nur noch einen Zahn.\aDiesmal brauchen wir einen von einem Schönredner.\aWenn du einen hast, bring ihn her und hol dir deine Belohnung ab." },

    3220 : { QUEST : "Ich habe gerade gehört, dass _toNpcName_ überall nach dir gefragt hat.\aWarum gehst du nicht mal hin und fragst, was sie will?_where_" },
    3221 : { QUEST : "Hi, _avName_! Da bist du ja!\aIch habe gehört, dass du ein ziemlicher Experte für Spritzattacken sein sollst.\aIch brauche jemanden, der allen Toons in Daisys Gärten mal ein gutes Beispiel gibt.\aSetz deine Spritzattacken ein, um ein paar Bots zu vertreiben.\aErmutige auch deine Freunde, mit zu spritzen.\aWenn du 20 Bots vertreiben hast, komm wieder her und hol dir deine Belohnung ab!" },

    3222 : { QUEST : "Es ist höchste Zeit, deine Toonhaftigkeit unter Beweis zu stellen.\aWenn du erfolgreich eine Reihe von Bot-Gebäuden zurückholst, erwirbst du dir das Recht, drei Aufgaben zu tragen.\aErobere zunächst zwei beliebige Bot-Gebäude.\aDu darfst deine Freunde um Hilfe bitten."},
    3223 : { QUEST : "Das mit den Gebäuden hast du gut gemacht!\aErobere nun zwei weitere Gebäude.\aDiese Gebäude müssen mindestens zwei Stockwerke hoch sein." },
    3224 : { QUEST : "Fantastisch!\aJetzt brauchst du nur noch zwei weitere Gebäude erkämpfen.\aDiese Gebäude müssen mindestens drei Stockwerke hoch sein.\aWenn du fertig bist, komm zurück und hol dir deine Belohnung ab!",
             COMPLETE : "Du hast es geschafft, _avName_!\aDu hast deine überaus große Toonhaftigkeit bewiesen.",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ sagt, dass sie Hilfe braucht.\aGeh doch mal hin und frag, wie du ihr helfen kannst?_where_" },
    3235 : { QUEST : "Oh, das ist der Salat, den ich bestellt habe!\aDanke, dass du ihn mir bringst.\aDiese Bots haben wohl _toNpcName_s eigentliches Lieferanten wieder mal vergrault.\aTu uns doch einen Gefallen und verjage ein paar von den Bots da draußen.\aBezwinge 10 Bots in Daisys Gärten und melde dich dann wieder bei _toNpcName_.",
             INCOMPLETE_PROGRESS : "Du bist noch dabei, Bots für mich zu vertreiben?\aDas ist großartig! Mach so weiter!",
             COMPLETE : "Oh, vielen Dank, dass du diese Bots vertrieben hast!\aJetzt kann ich vielleicht meinen normalen Lieferplan einhalten.\aDeine Belohnung ist ... ",
             INCOMPLETE_WRONG_NPC : "Geh mal zu _toNpcName_ und berichte von den Bots, die du vertrieben hast._where_" },

    3236 : { QUEST : "Es gibt viel zu viele Rechtomaten da draußen.\aDu kannst deinen Teil zur Rettung beitragen!\aErobere 3 Rechtomaten-Gebäude." },
    3237 : { QUEST : "Das mit den Rechtomaten-Gebäuden hast du gut gemacht!\aJetzt gibt es aber zu viele Schachermaten!\aErobere 3 Schachermaten-Gebäude, dann komm zurück und hol dir deine Belohnung ab." },

    3238 : { QUEST : "Oh nein! Ein 'Einmischer'-Bot hat den Schlüssel zu Daisys Gärten gestohlen!\aVersuche doch, ihn zurückzuholen.\aDenk dran, den Einmischer kann man nur in Schachermaten-Gebäuden finden." },
    3239 : { QUEST : "Du hast zwar einen Schlüssel gefunden, aber es ist nicht der richtige!\aWir brauchen den Schlüssel zu Daisys Gärten.\aSuche weiter! Ein \"Einmischer\"-Bot hat ihn noch!" },

    3242 : { QUEST : "Oh nein! Ein Prozessgeier-Bot hat den Schlüssel zu Daisys Gärten gestohlen!\aVersuche mal, ihn zurückzuholen.\aDenk daran, Prozessgeier kann man nur in Rechtomaten-Gebäuden finden. " },
    3243 : { QUEST : "Du hast zwar einen Schlüssel gefunden, aber es ist nicht der richtige!\aWir brauchen den Schlüssel zu Daisys Gärten.\aSuche weiter! Ein Prozessgeier-Bot hat ihn noch!" },

    3240 : { QUEST : "Ich habe grad von _toNpcName_ gehört, dass ein Prozessgeier eine Tüte Vogelfutter gestohlen hat.\aVertreibe Prozessgeier, bis du Volkers Vogelfutter zurückgeholt hast, und bringe es ihm dann.\aProzessgeier findet man nur in Rechtomaten-Gebäuden._where_",
             COMPLETE : "Oh, vielen Dank, dass du mein Vogelfutter gefunden hast!\aDeine Belohnung ist ... ",
             INCOMPLETE_WRONG_NPC : "Das mit dem Vogelfutter hast du gut gemacht!\aBring es jetzt zu _toNpcName_._where_",
             },

    3241 : { QUEST : "Ein paar von den Bot-Gebäuden da draußen werden höher, als uns lieb ist.\aSieh mal zu, ob du ein paar von den höchsten Gebäuden erobern kannst.\aErobere 5 Gebäude mit drei oder mehr Stockwerken und komm´dann wieder, um dir deine Belohnung abzuholen.",
             },

    3250 : { QUEST : "Detektivin Lima drüben in der Eichenstraße hat Meldungen über ein Schachermat-Hauptquartier erhalten.\aSpring mal rüber und hilf ihr bei den Untersuchungen.",
             },
    3251 : { QUEST : "Hier geht etwas Seltsames vor.\aEs gibt hier so viele Schachermaten!\aIch habe gehört, dass sie eine eigene Toontown-Zentrale am Ende dieser Straße eingerichtet haben.\aGeh mal die Straße runter und schau, ob du was rauskriegen kannst.\aFinde Schachermaten-Bots in ihrem Hauptquartier, besiege 5 und melde dich zurück.",
             },
    3252 : { QUEST : "OK, spuck's aus.\aWas sagst du da?\aSchachermaten-Hauptquartier?? Ach du Schreck!!! Es muss was passieren.\aWir müssen Richterin McIntosh Bescheid geben - sie wird wissen, was zu tun ist.\aGeh sofort los und erzähle ihr, was du herausgefunden hast. Du findest sie weiter die Straße runter.",
            },
    3253 : { QUEST : "Ja, kann ich helfen? Ich bin sehr beschäftigt.\aWas? Bot-Zentrale?\aWas? Unsinn. Das könnte nie passieren.\aDu musst dich irren. Völlig absurd.\aWas? Widersprich mir nicht.\aNa gut, dann bring mir Beweise.\aWenn Schachermaten wirklich dieses Bot-Zentrale bauen, dann trägt jeder Bot dort Blaupausen mit sich herum.\aBots lieben Papierkram, weißt du?\aJage Schachermaten, bis du Blaupausen findest.\aBring sie her, dann glaube ich dir vielleicht.",
            },
    3254 : { QUEST : "Du schon wieder, was? Blaupausen? Du hast sie?\aLass mich mal sehen! Hmmm... Eine Fabrik?\aDort bauen sie wohl die Schachermaten ... Und was ist das?\aJa, genau wie ich vermutete. Ich hab's ja immer gewusst.\aSie bauen ein Schachermaten-Bot-Hauptquartier.\aDas ist nicht gut. Muss telefonieren. Sehr viel zu tun. Auf Wiedersehen!\aWas? Ach ja, nimm diese Blaupausen mit zu Detektivin Lima.\aSie kann mehr damit anfangen.",
             COMPLETE : "Was hat Richterin McIntosh gesagt?\aWir hatten Recht? Oh nein. Lass mal diese Blaupausen sehen.\aHmmm... Sieht aus, als würden die Schachermaten eine Fabrik mit Maschinen zur Herstellung von Bots bauen.\aKlingt sehr gefährlich. Halte dich raus, bis du mehr Lach-Punkte hast.\aWenn du mehr Lach-Punkte hast, müssen wir noch viel mehr über das Schachermaten-Hauptquartier rauskriegen.\aBisher aber gut gemacht, hier ist deine Belohnung.",
            },


    3255 : { QUEST : "_toNpcName_ untersucht das Schachermaten-Hauptquartier.\aSchau mal, ob du helfen kannst._where_" },
    3256 : { QUEST : "_toNpcName_ untersucht das Schachermaten-Hauptquartier.\aSchau mal, ob du helfen kannst._where_" },
    3257 : { QUEST : "_toNpcName_ untersucht das Schachermaten-Hauptquartier.\aSchau mal, ob du helfen kannst._where_" },
    3258 : { QUEST : "Es gibt verschiedenste Vermutungen darüber, was die Bots in ihrem neuen Hauptquartier vorhaben.\aIch möchte, dass du direkt von ihnen ein paar Informationen holst.\aWenn wir vier interne Memos von Schachermaten aus ihrem Hauptquartiers bekommen können, dann werden wir klarer sehen.\aBringe dein erstes Memo zu mir, damit wir mehr erfahren.",
             },
    3259 : { QUEST : "Großartig! Lass mal sehen, was in dem Memo steht ... \a\"An alle Schachermaten:\aIch sitze in meinem Büro oben im Schachermat Tower und befördere Bots.\aWer genügend Verdienste gesammelt hat, steige in den Fahrstuhl in der Lobby und komme zu mir.\aDie Ferien sind vorbei - nun wieder an die Arbeit!\aUnterschrift: Schachermat VP\"\aAha ... das wird Flippy interessieren. Ich lasse es ihm sofort zukommen.\aBitte hole jetzt dein zweites Memo und bring es her.",
             },
    3260 : { QUEST : "Ach, gut, dass du zurückkommst. Mal sehen, was du gefunden hast ...\a\"An alle Schachermaten:\aSchachermat Towers hat ein neues Sicherheitssystem installiert, um die Toons fern zu halten.\aWenn Toons in Schachermat Towers aufgegriffen werden, werden sie zum Verhör festgehalten.\aAlles weitere kann in der Lobby bei einem Aperitif besprochen werden.\aUnterschrift: Einmischer\"\aSehr interessant ... Ich gebe diese Information sofort weiter.\aBitte bringe ein drittes Memo her.",
             },
    3261 : { QUEST : "Ausgezeichnete Arbeit, _avName_! Was steht da drin?\a\'An alle Schachermaten:\aToons haben einen Weg gefunden, um in Schachermat Towers einzudringen.\aIch werde Sie heute Abend beim Essen anrufen und Ihnen die Einzelheiten mitteilen.\aUnterschrift:Telemarketer'\aHmmm... ich frage mich, wie Toons da einbrechen ...\aBitte bring noch ein Memo, dann wissen wir erstmal genug, denke ich.",
             COMPLETE : "Ich wusste, dass du es schaffen würdest! OK, in dem Memo heißt es ...\a\"An alle Schachermaten:\aIch war gestern mit Mr. Hollywood beim Lunch.\aEr berichtete, dass der VP zur Zeit sehr beschäftigt ist.\aEr macht nur Termine mit Bots, die eine Beförderung verdienen.\aNoch was vergessen: Glückshändchen spielt am Sonntag mit mir Golf.\aUnterschrift: Wichtigtuer\"\aAlso ... _avName_, das war sehr hilfreich.\aHier ist deine Belohnung.",
             },

    3262 : { QUEST : "_toNpcName_ hat neue Informationen über die Fabrik des Schachermaten-Hauptquartier.\aGeh mal hin und schau, was er hat._where_" },
    3263 : { GREETING : "Hi Sportsfreund!",
             QUEST : "Ich bin Trainer Bemoost, aber du kannst Trainer B. zu mir sagen.\aVon mir stammen die Flechten in Hauen und Flechten, aber auch das Hauen, wenn du weißt, was ich meine.\aHör mal, die Schachermaten haben eine riesige Fabrik fertiggestellt, die 24 Stunden am Tag Schachermaten ausspuckt.\aHol mal ein paar Toon-Sportsfreunde zusammen und hau denen eins drauf!\aIhr müsst im Schachermaten-Hauptquartier nach dem Tunnel zur Fabrik Ausschau halten, und dann den Fabrikfahrstuhl nehmen.\aAchtet darauf, dass ihr volle Gags, volle Lach-Punkte und ein paar starke Toons als Führer habt.\aBesiegt den Vorarbeiter in der Fabrik, um das Vorankommen der Schachermaten aufzuhalten.\aKlingt wie `ne schweißtreibende Angelegenheit, wenn du weißt, was ich meine.",
             LEAVING : "Mach's gut, Sportsfreund!",
             COMPLETE : "He Sportsfreund, gute Arbeit da in der Fabrik!\aSieht aus, als hättest du da ein  Bot-Anzugteil gefunden.\aDer muss wohl bei ihrer Bot-Herstellung übrig geblieben sein.\aDer kann noch gute Dienste leisten. Wenn du mal zu viel Zeit hast, sammle mehr von denen.\aWenn du einen ganzen Bot-Anzug zusammen hast, kann der vielleicht noch zu irgend etwas gut sein ...",
             },

        4001 : {GREETING : "",
            QUEST : "Du kannst jetzt den nächsten Gag-Alauf wählen, den du erlernen möchtest.\aNimm dir Zeit für die Entscheidung und komm zurück, wenn du bereit zum Wählen bist.",
            INCOMPLETE_PROGRESS : "Denke gut nach, ehe du wählst.",
            INCOMPLETE_WRONG_NPC : "Denke gut nach, ehe du wählst.",
            COMPLETE : "Eine kluge Entscheidung ...",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "Du kannst jetzt den nächsten Gag-Ablauf wählen, den du erlernen möchtest.\aNimm dir Zeit für die Entscheidung und komm zurück, wenn du bereit zum Wählen bist.",
            INCOMPLETE_PROGRESS : "Denke gut nach, ehe  du wählst.",
            INCOMPLETE_WRONG_NPC : "Denke gut nach, ehe du wählst.",
            COMPLETE : "Eine kluge Entscheidung ...",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "Ich wette, Tom könnte bei seinen Forschungen etwas Hilfe gebrauchen._where_",
             },
    4201 : { GREETING: "Wie geht's, wie steht's?",
             QUEST : "Ich bin sehr besorgt über eine Flut von Instrumentendiebstählen.\aIch mache gerade eine Umfrage bei meinen Händlerkollegen.\aVielleicht kann ich ein Muster erkennen, das mir beim Knacken dieses Falls hilft.\aGeh mal rüber zu Tina und frag sie nach einer Konzertina-Inventarliste._where_",
             },
    4202 : { QUEST : "Ja, ich habe heute früh mit Tom gesprochen.\aIch hab die Inventarliste hier.\aBring sie ihm gleich rüber, ja?_where_"
             },
    4203 : { QUEST : "Großartig! Eine weniger ...\aJetzt spring mal rüber und hole die von Yuki._where_",
             },
    4204 : { QUEST : "Oh! Die Inventarliste!\aHab ich ja völlig vergessen.\aIch wette, ich hab sie fertig, bis du 10 Bots vertrieben hast.\aKomm danach wieder rein, und ich verspreche dir, dass ich dann fertig bin.",
             INCOMPLETE_PROGRESS : "31, 32... MI-st!\aWegen dir hab ich mich verzählt!",
             GREETING : "",
             },
    4205 : { QUEST : "Ah, da bist du ja.\aDanke, dass du mir etwas Zeit gegeben hast.\aNimm das hier mit zu Tom und grüß ihn schön von mir._where_",
             },
    4206 : { QUEST : "Hmmm, sehr interessant.\aJetzt kommen wir doch langsam voran.\aOK, die letzte Inventarliste ist die von Fifi._where_",
             },
    4207 : { QUEST : "Inventarliste?\aWie soll ich denn eine Inventarliste schreiben, wenn ich kein Formular habe?\aGeh mal zu Quint und frag ihn, ob er eins für mich hat._where_",
             INCOMPLETE_PROGRESS : "Schon was Neues in Sachen Formular?",
             },
    4208 : { QUEST : "Nu, klar `abe isch Inventarformular!\aAber du musse bezahlen, weisstu?\aIsch mach dir Vorschlag. Isch tausche Formular für ganze Sahnetorte.",
             GREETING : "Hey, was' los, man!",
             LEAVING : "Hey, cool, man.",
             INCOMPLETE_PROGRESS : "Ein Stücke reiche nischt.\aIsch 'abe sehr hungrig, man. Isch brauche GANZES Torte!",
             },
    4209 : { GREETING : "",
             QUEST : "Mmmm...\aDas ist serrr gutt!\aHier deine Formular für Fifi._where_",
             },
    4210 : { GREETING : "",
             QUEST : "Danke. Das ist eine große Hilfe.\aWolln mal sehen ...Fiedeln: 2\aSchon fertig! Bitteschön!",
             COMPLETE : "Gute Arbeit, _avName_.\aIch bin sicher, dass ich diesen Diebstählen jetzt auf den Grund komme.\aKümmer du dich doch um das hier!",
             },

    4211 : { QUEST : "Sag mal, Dr. Unsauber ruft alle fünf Minuten an. Kannst du mal hingehen und nachsehen, was er für ein Problem hat?_where_",
             },
    4212 : { QUEST : "Ui! Ich bin froh, dass die Toontown-Zentrale endlich jemanden geschickt hat.\aIch habe seit Tagen keine Kundschaft mehr.\aEs sind diese nervigen Erbsenzähler überall.\aIch glaube, die bringen unseren Einwohnern eine schlechte Mundhygiene bei.\aVertreibe zehn von ihnen, dann wollen wir doch mal sehen, ob das Geschäft wieder läuft.",
             INCOMPLETE_PROGRESS : "Immer noch keine Kundschaft. Aber mach weiter!",
             },
    4213 : { QUEST : "Vielleicht waren es ja am Ende gar nicht die Erbsenzähler.\aVielleicht sind es die Monetomaten überhaupt.\aNimm dir mal zwanzig von ihnen vor, und dann kommt hoffentlich mal jemand wenigstens zur Kontrolle rein.",
             INCOMPLETE_PROGRESS : "Ich weiß, zwanzig sind eine ganze Menge. Aber ich bin sicher, dass es sich mit Zins und Zinseszins auszahlen wird.",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ich verstehe das einfach nicht!\aImmer noch kein EINZIGER Patient!\aVielleicht müssen wir das Übel an der Wurzel anpacken.\aVersuche, ein Monetomaten-Bot-Gebäude zu erobern.\aDas dürfte funktionieren.",
             INCOMPLETE_PROGRESS : "Ach, bitte! Nur ein ganz kleines Gebäude ...",
             COMPLETE : "Immer noch kein Mensch hier.\aAber wenn ich es mir recht überlege ...\aIch hatte ja auch keine Kundschaft, bevor die Bots hier eingedrungen sind!\aIch bin dir für deine Hilfe wirklich dankbar.\aDas hier dürfte dir ein bisschen weiterhelfen."
             },

    4215 : { QUEST : "Anna braucht dringend HIlfe.\aGeh doch mal rüber und schau, was du tun kannst._where_",
             },
    4216 : { QUEST : "Danke, dass du so schnell gekommen bist!\aEs scheint so, als hätten sich die Bots mit ein paar Kreuzfahrttickets meiner Kunden davongemacht.\aYuki sagt, sie hätte ein Glückshändchen gesehen, der hier rauskam und in seinen Glückshändchen lauter Tickets hatte.\aSchau doch mal, ob du Holzmichels Fahrkarte für Alaska zurückholen kannst.",
             INCOMPLETE_PROGRESS : "Diese Glückshändchen können ja inzwischen sonstwo sein ...",
             },
    4217 : { QUEST : "Oh, großartig! Du hast es gefunden!\aJetzt sei so nett und flitz schnell zum Michel rüber, ja?_where_",
             },
    4218 : { QUEST : "Großer Goglmohsch!\aAlaska, ich komme!\aIch halte diese teuflischen Bots nicht mehr aus.\aDu, ich glaube, Anna braucht dich nochmal._where_",
             },
    4219 : { QUEST : "Jawoll, erraten.\aIch brauch dich, um diese vermaledeiten Glückshändchen nochmal zu filzen - wegen Tabithas Ticket zum Jazzfest.\aDu weißt ja jetzt, wie's geht ... ",
               INCOMPLETE_PROGRESS : "Irgendwo ist da noch mehr ... ",
             },
    4220 : { QUEST : "Süß!\aKönntest du das auch noch bei ihm abgeben? _where_",
             },
    4221 : { GREETING : "",
             LEAVING : "Bleib cool ...",
             QUEST : "Cool, Daddy!\aJetzt bin ich wieder voll dabei, _avName_.\aBevor du abhaust, solltest du nochmal bei Anna Banana reinschauen ..._where_",
             },
    4222 : { QUEST : "Das ist das letzte Mal, Ehrenwort!\aJetzt suchst du nach Grizzlys Ticket für den großen Gesangswettbewerb.",
             INCOMPLETE_PROGRESS : "Ach, komm schon, _avName_.\aGrizzly zählt auf dich.",
             },
    4223 : { QUEST : "Das dürfte ein Lächeln auf Grizzlys Gesicht zaubern._where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "Hallo, Hallo, HALLO!\aKlasse!\aIch weiß, dass die Jungs und ich dieses Jahr groß abräumen werden.\aAnna sagt, du sollst vorbeikommen und deine Belohnung holen._where_\aWiedersehen, Wiedersehn, WIEDER-WIEDERSEHN!",
             COMPLETE : "Danke für deine große Hilfe, _avName_.\aDu bist wirklich ein Gewinn für Toontown.\aApropos Gewinn ...",
             },

    902 : { QUEST : "Geh mal zu Leo.\aEr braucht jemanden, der für ihn eine Nachricht überbringt._where_",
            },
    4903 : { QUEST : "Alter!\aMeine Kastagnetten sehen ganz matt aus und ich habe heute einen großen Auftritt.\aBring sie zu Carlos, der kann sie vielleicht aufpolieren._where_",
             },
    4904 : { QUEST : "Ja, isch glaubä isch kann dissä polieren.\aAbbär isch brauchä das blauä Tintä aus Tintänfischä.",
             GREETING : "Hola!",
             LEAVING : "Adios!",
             INCOMPLETE_PROGRESS : "Du kannst Tintänfischä findän, wo Angälstäg ist.",
             },
    4905 : { QUEST : "Ja! Dass gutt!\aNun ich brauchä biesschen Zeit für Polierän dissä.\aDu kannst gehän ein Einstockgebäudä übärnähmän, während isch arbeitä, gutt? ",
             GREETING : "Hola!",
             LEAVING : "Adios!",
             INCOMPLETE_PROGRESS : "Eino Momento ...",
             },
    4906 : { QUEST : "Särr gutt!\aHier sind Kastagnättän für Läo._where_",
             },
    4907 : { GREETING : "",
             QUEST : "Cool, Alter!\aDie sehen echt kastanig aus!\aJetzt musst du mal noch bei Hedy den Text von 'Beat nun ist Weihnachtszeit' für mich holen._where_",
             },
    4908 : { QUEST: "Tag!\aHmmm, ich hab das Lied grad nicht zur Hand.\aWenn du mir einen Moment Zeit gibst, notiere ich es aus dem Gedächtnis.\aDu könntest doch mal losgehen und ein zweistöckiges Gebäude eroberst, während ich schreibe!",
             },
    4909 : { QUEST : "Tut mir Leid.\aMein Gedächtnis lässt ein bisschen zu wünschen übrig.\aWenn du noch ein dreistöckiges Gebäude zurück eroberst, bin ich bestimmt fertig, wenn du zurückkommst ...",
             },
    4910 : { QUEST : "Fertig!\aTut mir Leid, dass es so lange gedauert hat.\aNimm das hier mit zu Leo._where_",
             GREETING : "",
             COMPLETE : "Klasse, Alter!\aMein Konzert wird dermaßen rocken, dass es alle umhaut!\aApropos umhauen, hiermit kannst du ein paar Bots umhauen ... "
             },
    5247 : { QUEST : "Diese Gegend ist schon ziemlich heftig ...\aVielleicht magst du ein paar neue Tricks lernen.\a_toNpcName_ hat mir alles Notwendige beigebracht; vielleicht kann er dir auch helfen._where_" },
    5248 : { GREETING : "Ahh, ja.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Du scheinst ein Problem mit meiner Anweisung zu haben?",
             QUEST : "Ahh, also willkommen, neuer Lehrling.\aIch weiß alles, was man über die Sache mit den Torten wissen muss.\aBevor wir aber mit deinem Training anfangen, ist eine kleine Demonstration vonnöten.\aGehe hinaus und erledige zehn von den größten Bots." },
    5249 : { GREETING: "Mmmmm.",
             QUEST : "Ausgezeichnet!\aNun beweise noch deine Fähigkeiten als Angler.\aIch habe gestern drei Fellwürfel in den Teich geworfen.\aFisch sie raus und bring sie mir. ",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Anscheinend stellst du dich mit Rute und Rolle nicht ganz so geschickt an." },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aha! Diese Würfel werden sich am Rückspiegel meines Ochsenkarrens gut machen!\aJetzt zeige mir doch noch, dass du deine Feinde unterscheiden kannst.\aKomm wieder her, wenn du zwei der größten Rechtomaten-Gebäude zurückgeholt hast.",
             INCOMPLETE_PROGRESS : "Gibt's Probleme mit den Gebäuden?", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aha! Diese Würfel werden sich am Rückspiegel meines Ochsenkarrens gut machen!\aJetzt zeige mir doch noch, dass du deine Feinde unterscheiden kannst.\aKomm wieder her, wenn du zwei der größten Chefomaten-Gebäude zurückgeholt hast.",
             INCOMPLETE_PROGRESS : "Gibt's Probleme mit den Gebäuden?", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aha! Diese Würfel werden sich am Rückspiegel meines Ochsenkarrens gut machen!\aJetzt zeige mir doch noch, dass du deine Feinde unterscheiden kannst.\aKomm wieder her, wenn du zwei der größten Monetomaten-Gebäude zurückgeholt hast.",
             INCOMPLETE_PROGRESS : "Gibt's Probleme mit den Gebäuden?", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aha! Diese Würfel werden sich am Rückspiegel meines Ochsenkarrens gut machen!\aJetzt zeige mir doch noch, dass du deine Feinde unterscheiden kannst.\aKomm wieder her, wenn du zwei der größten Schachermaten-Gebäude zurückgeholt hast.",
             INCOMPLETE_PROGRESS : "Gibt's Probleme mit den Gebäuden?", },
    5200 : { QUEST : "Diese hinterlistigen Bots haben wieder zugeschlagen.\a_toNpcName_ hat noch einen verschwundenen Gegenstand gemeldet. Schau mal dort vorbei, ob du das regeln kannst._where_" },
    5201 : { GREETING: "",
             QUEST : "Hi, _avName_. Ich schätze, ich sollte dir für dein Kommen danken.\aEin paar von diesen Köpfchenjägern kamen hier rein und stahlen meinen Fußball.\aDer Anführer meinte zu mir, ich müsste ein paar Abstriche machen, und dann riss er ihn mir einfach aus der Hand!\aKannst du meinen Ball zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Na schon irgendein Erfolg bei der Suche nach meinem Fußball?",
             COMPLETE : "Jippieh! Du hast ihn gefunden! Hier, nimm deine Belohnung ...",
             },
    5261 : { GREETING: "",
             QUEST : "Hi, _avName_. Ich schätze, ich sollte dir für dein Kommen danken.\aEin paar von diesen Falschgesichtern kamen hier rein und stahlen meinen Fußball.\aDer Anführer meinte zu mir, ich müsste ein paar Abstriche machen, und dann riss er ihn mir einfach aus der Hand!\aKannst du meinen Ball zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Na schon irgendein Erfolg bei der Suche nach meinem Fußball?",
             COMPLETE : "Jippieh! Du hast ihn gefunden! Hier, nimm deine Belohnung ...",
             },
    5262 : { GREETING: "",
             QUEST : "Hi, _avName_. Ich schätze, ich sollte dir für dein Kommen danken.\aEin paar von diesen Geldsäcken kamen hier rein und stahlen meinen Fußball.\aDer Anführer meinte zu mir, ich müsste ein paar Abstriche machen, und dann riss er ihn mir einfach aus der Hand!\aKannst du meinen Ball zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Na schon irgendein Erfolg bei der Suche nach meinem Fußball?",
             COMPLETE : "Jippieh! Du hast ihn gefunden! Hier, nimm deine Belohnung ...",
             },
    5263 : { GREETING: "",
             QUEST : "Hi, _avName_. Ich schätze, ich sollte dir für dein Kommen danken.\aEin paar von diesen Schönrednern kamen hier rein und stahlen meinen Fußball.\aDer Anführer meinte zu mir, ich müsste ein paar Abstriche machen, und dann riss er ihn mir einfach aus der Hand!\aKannst du meinen Ball zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Na schon irgendein Erfolg bei der Suche nach meinem Fußball?",
             COMPLETE : "Jippieh! Du hast ihn gefunden! Hier, nimm deine Belohnung ...",
             },
    5202 : { QUEST : "Einige der härtesten Bots, die wir bisher kennengelernt haben, sind in Das Brrr eingefallen.\aDu solltest hier wahrscheinlich lieber ein paar mehr Gags bei dir tragen.\aIch habe gehört, dass _toNpcName_ vielleicht eine große Tasche hat, die du dafür verwenden kannst._where_" },
    5203 : { GREETING: "Hä? Bist du von meiner Schlittenmannschaft?",
             QUEST : "Was ist los? Du willst eine Tasche?\aIch hatte hier irgendwo eine ... vielleicht ist sie in meinem Schlitten?\aNur ... ich hab meinen Schlitten seit dem großen Rennen nicht mehr gesehen!\aVielleicht hat ihn einer von diesen Bots mitgenommen?",
             LEAVING : "Hast du meinen Schlitten gesehen?",
             INCOMPLETE_PROGRESS : "Wer bist du nochmal? Tut mir Leid, ich bin noch etwas wirr im Kopf von dem Zusammenstoß." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ist das mein Schlitten? Ich seh hier keine Tasche.\aIch glaube, Huckelberry Schlitzauge war in der Mannschaft ... vielleicht hat er sie?_where_" },
    5205 : { GREETING : "Ooooh, mein Kopf!",
             LEAVING : "",
             QUEST : "Hä? Schorsch wer? Eine Tasche?\aOh, vielleicht war er in unserer Schlittenmannschaft?\aMein Kopf tut so weh, dass ich nicht klar denken kann..\aKönntest du aus dem zugefrorenen Teich ein paar Eiswürfel für meinen Kopf fischen?",
             INCOMPLETE_PROGRESS : "Auuu, mein Kopf bringt mich noch um! Hast du Eis?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahhh, das ist schon viel besser!\aDu suchst also nach Schorschs Tasche, hm?\aIch glaube, die ist nach dem Zusammenstoß auf Halbaffen-Sams Kopf gelandet._where_" },
    5207 : { GREETING : "Iiiiiip!",
             LEAVING : "",
             QUEST : "Was Tasche? Wer Hockelberry?\aIch Angst vor Gebäude! Du hauen Gebäude, ich geben dir Tasche!",
             INCOMPLETE_PROGRESS : "Mehr Gebäude! Ich noch Angst!",
             COMPLETE : "Ooooh! Ich haben dich gern!" },
    5208 : { GREETING : "",
             LEAVING : "Iiiiik!",
             QUEST : "Ooooh! Ich haben dich gern!\aGehen zu Schiklinik. Tasche dort." },
    5209 : { GREETING : "Alter!",
             LEAVING : "Bis später!",
             QUEST : "Mann, dieser Halbaffen-Sam ist vielleicht verrückt!\aWenn du nur halb so verrückt bist wie Sam, geb ich dir die Tasche, Mann.\aHau mal paar Bots für deine Tasche in die Tasche, Mann! Na los!",
             INCOMPLETE_PROGRESS : "Bist du sicher, dass das extrem genug war? Hau noch ein paar Bots in die Tasche.",
             COMPLETE : "He, du bist ja ganz schön verrückt! Das war vielleicht ein Haufen Bots, die du da eingetütet hast!\aHier ist deine Tasche!" },

    5210 : { QUEST : "_toNpcName_ ist heimlich in jemanden aus der Nachbarschaft verliebt.\aWenn du ihr hilfst, bekommst du vielleicht eine hübsche Belohnung._where_" },
    5211 : { GREETING: "Huu-huuu.",
             QUEST : "Ich hab die ganze letzte Nacht einen Brief an den Burschen, den ich liebe, geschrieben.\aDoch bevor ich ihn hinbringen konnte, kam einer dieser hässlichen Bots mit Schnabel und nahm ihn weg.\aKannst du ihn für mich zurückholen?",
             LEAVING : "Huu-huuu.",
             INCOMPLETE_PROGRESS : "Bitte finde meinen Brief." },

    5264 : { GREETING: "Huu-huuu.",
             QUEST : "Ich hab die ganze letzte Nacht einen Brief an den Burschen, den ich liebe, geschrieben.\aDoch bevor ich ihn hinbringen konnte, kam einer dieser hässlichen Bots mit Flosse und nahm ihn weg.\aKannst du ihn für mich zurückholen?",
             LEAVING : "Huu-huuu.",
             INCOMPLETE_PROGRESS : "Bitte finde meinen Brief." },
    5265 : { GREETING: "Huu-huuu",
             QUEST : "Ich hab die ganze letzte Nacht einen Brief an den Burschen, den ich liebe, geschrieben.\aDoch bevor ich ihn hinbringen konnte, kam einer dieser hässlichen Einmischer-Bots und nahm ihn weg.\aKannst du ihn für mich zurückholen?",
             LEAVING : "Huu-huuu.",
             INCOMPLETE_PROGRESS : "Bitte finde meinen Brief." },
    5266 : { GREETING: "Huu-huuu.",
             QUEST : "Ich hab die ganze letzte Nacht einen Brief an den Burschen, den ich liebe, geschrieben.\aDoch bevor ich ihn hinbringen konnte, kam einer dieser hässlichen Unternehmensräuber mit Schnabel und nahm ihn weg.\aKannst du ihn für mich zurückholen?",
             LEAVING : "Huu-huuu.",
             INCOMPLETE_PROGRESS : "Bitte finde meinen Brief." },
    5212 : { QUEST : "Oh, danke, dass du meinen Brief gefunden hast!\aBitte, bitte, bitte, könntest du ihn zum hübschesten Burschen der Gegend bringen?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Du hast meinen Brief noch nicht abgegeben, oder?",
             },
    5213 : { GREETING : "Entzückend, natürlich.",
             QUEST : "Ich hab jetzt keinen Nerv für deinen Brief.\aMir hat jemand all meine Hündchen weggenommen!\aWenn du sie zurückbringst, können wir nochmal drüber reden.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Meine armen kleinen Hündchen!" },
    5214 : { GREETING : "",
             LEAVING : "Tudelu!",
             QUEST : "Danke, dass du meine kleinen Schönen zurückgebracht hast.\aDann wollen wir uns mal deinen Brief ansehen ... \a Mmmm, es scheint, als hätte ich noch eine heimliche Verehrerin.\aDa ist wohl ein Besuch bei meinem lieben Freund Karl angesagt.\aIch bin sicher, du wirst ihn unheimlich mögen._where_" },
    5215 : { GREETING : "Hehe ...",
             LEAVING : "Komm wieder, jaja.",
             INCOMPLETE_PROGRESS : "Da sind immer noch ein paar Große unterwegs. Komm zu uns zurück, wenn die weg sind.",
             QUEST : "Wer hat dich zu uns geschickt? Wir mögen Schnautzies nicht besonders, nein, nein ...\aAber wir tun Bots noch weniger mögen ...\aTu du die Großen vertreiben und wir helfen dir, ja, ja." },
    5216 : { QUEST : "Wir haben dir ja gesagt, dass wir dir helfen tun.\aAlso tu diesen Ring zu dem Mädel bringen.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Du tust diesen Ring immer noch haben???",
             COMPLETE : "Oh Liiiiebling!!! Danke!!!\aOh, und ich habe auch etwas Besonderes für dich.",
             },
    5217 : { QUEST : "Es klingt, als könnte _toNpcName_ Hilfe gebrauchen._where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich bin sicher, dass da irgendwo noch mehr Einmischer unterwegs sind.",
             QUEST : "Hilfe!!! Hilfe!!! Ich kann nicht mehr!\aDiese Einmischer machen mich wahnsinnig!!!" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Das können nicht alle gewesen sein. Ich habe gerade einen gesehen!!!",
             QUEST : "Oh, danke, aber jetzt sind es die Unternehmensräuber!!!\aDu musst mir helfen!!!" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Nein, nein, nein, es war grad einer hier!",
             QUEST : "Ich merke jetzt, dass es diese Kredithaie sind!!!\aIch dachte, du wolltest mich retten!!!" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "Weißt du was, vielleicht sind es gar nicht die Bots!\aKönntest du Fanny bitten, mir einen Beruhigungstrank zu mixen? Vielleicht hilft das ... _where_" },
    5222 : { LEAVING : "",
             QUEST : "Oh, dieser Harry, der ist schon ein Spaßvogel!\aIch mix was zusammen, das ihm hilft!\aOh, anscheinend habe ich keinen Stein des Weisen mehr...\aSei so lieb, lauf runter zum Teich und hol mir was.",
             INCOMPLETE_PROGRESS : "Hast du schon einen Stein des Weisen für mich?", },
    5223 : { QUEST : "Okay. Danke, Schatz.\aHier, bring das zu Harry. Das dürfte ihn voll beruhigen.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Nun geh schon, bring den Trank zu Harry.",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Los, schnapp dir diese Prozessgeier für mich, ja?",
             QUEST : "Oh, Gott sei dank Du bist zurück!\aGib mir den Trank, schnell!!!\aGluckgluckgluck ...\aScheußlich!\aAber weißt du was? Ich bin schon viel ruhiger. Jetzt, da ich klar denken kann, merke ich ...\aEs waren die Prozessgeier, die mich die ganze Zeit verrückt gemacht haben!",
             COMPLETE : "Jungejunge! Jetzt kann ich mich entspannen!\aIch bin sicher, dass es hier irgend etwas gibt, was ich dir geben kann. Oh, nimm das!" },
    5225 : { QUEST : "Seit dem Vorfall mit dem Rübenbrot ist Phil Mürrisch stinksauer auf _toNpcName_.\aVielleicht kannst du Gert helfen, die Sache zwischen ihnen ins Lot zu bringen?_where_" },
    5226 : { QUEST : "Ja, du hast ja vielleicht gehört, dass Phil Mürrisch stinkesauer auf mich ist...\aIch wollte ja nur nett sein mit dem Rübenbrot.\aVielleicht kannst du mir helfen, ihn aufzumuntern.\aPhil hasst diese Monetomaten-Bots, besonders ihre Gebäude.\aWenn du ein paar Monetomaten-Gebäude zurückholst, hilft das vielleicht.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vielleicht noch ein paar Gebäude?", },
    5227 : { QUEST : "Das ist unglaublich! Geh zu Phil und erzähle ihm, was du getan hast._where_" },
    5228 : { QUEST : "Ach, das hat er getan, ja?\aDieser Gert denkt wohl, er kommt so einfach davon, was?\aIch hab mir ja nur einen Zahn abgebrochen an seinem blöden Rübenbrot!\aVielleicht könntest du meinen Zahn zu Dr. Mummelgesicht bringen, damit der ihn wieder hinkriegt.",
             GREETING : "Mmmmrrrfff.",
             LEAVING : "Grummelgrummel.",
             INCOMPLETE_PROGRESS : "Du schon wieder? Ich dachte, du wolltest meinen Zahn reparieren lassen.",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich arbeite noch an dem Zahn. Es dauert noch etwas.",
             QUEST : "Ja, dieser Zahn sieht wirklich ziemlich bös aus, hihi.\aVielleicht kann ich ja was machen, aber das wird etwas dauern.\aVielleicht kannst du ja währenddessen ein paar von diesen Monetomaten-Bots von der Straße räumen?\aDie verschrecken meine Kundschaft." },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich arbeite noch an dem Zahn. Es dauert noch etwas.",
             QUEST : "Ja, dieser Zahn sieht wirklich ziemlich bös aus, hihi.\aVielleicht kann ich ja was machen, aber das wird etwas dauern.\aVielleicht kannst du ja währenddessen ein paar von diesen Schachermaten-Bots von der Straße räumen?\aDie verschrecken meine Kundschaft." },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich arbeite noch an dem Zahn. Es dauert noch etwas.",
             QUEST : "Ja, dieser Zahn sieht wirklich ziemlich bös aus, hihi.\aVielleicht kann ich ja was machen, aber das wird etwas dauern.\aVielleicht kannst du ja währenddessen ein paar von diesen Rechtomaten-Bots von der Straße räumen?\aDie verschrecken meine Kundschaft." },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich arbeite noch an dem Zahn. Es dauert noch etwas.",
             QUEST : "Ja, dieser Zahn sieht wirklich ziemlich bös aus.\aVielleicht kann ich ja was machen, aber das wird etwas dauern.\aVielleicht kannst du ja währenddessen ein paar von diesen Chefomaten-Bots von der Straße räumen?\aDie verschrecken meine Kundschaft." },
    5230 : { GREETING: "",
             QUEST : "Ich bin froh, dass du wieder da bist!\aIch hab es aufgegeben, diesen alten Zahn zu reparieren, und habe Phil dafür einen neuen Goldzahn gemacht.\aLeider kam ein Ausbeuter herein und nahm in mir ab.\aDu holst ihn vielleicht noch ein, wenn du dich beeilst.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du den Zahn schon gefunden?" },
    5270 : { GREETING: "",
             QUEST : "Ich bin froh, dass du wieder da bist!\aIch hab es aufgegeben, diesen alten Zahn zu reparieren, und habe Phil dafür einen neuen Goldzahn gemacht.\aLeider kam ein Großhirn herein und nahm in mir ab.\aDu holst es vielleicht noch ein, wenn du dich beeilst.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du den Zahn schon gefunden?" },
    5271 : { GREETING: "",
             QUEST : "Ich bin froh, dass du wieder da bist!\aIch hab es aufgegeben, diesen alten Zahn zu reparieren, und habe Phil dafür einen neuen Goldzahn gemacht.\aLeider kam Mr. Hollywood herein und nahm in mir ab.\aDu holst ihn vielleicht noch ein, wenn du dich beeilst.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du den Zahn schon gefunden?" },
    5272 : { GREETING: "",
             QUEST : "Ich bin froh, dass du wieder da bist!\aIch hab es aufgegeben, diesen alten Zahn zu reparieren, und habe Phil dafür einen neuen Goldzahn gemacht.\aLeider kam ein Großkotz herein und nahm in mir ab.\aDu holst ihn vielleicht noch ein, wenn du dich beeilst.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du den Zahn schon gefunden?" },
    5231 : { QUEST : "Großartig, das ist der Zahn, hihi!\aBring ihn doch für mich zu Phil rüber, ja?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich wette, Phil möchte seinen neuen Zahn sehen.",
             },
    5232 : { QUEST : "Oh, danke.\aMmmrrrfff.\aWie sieht das aus, hm?\aOkay, du kannst Gert sagen, dass ich ihm verzeihe.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Oh, das freut mich zu hören.\aIch dachte mir schon, dass der alte Phil nicht ewig auf mich sauer sein kann.\aAls Geste des guten Willens hab ich ihm dieses Kiefernzapfenbrot gebacken.\aKönntest du es zu ihm rüberbringen?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mach lieber schnell. Kiefernzapfenbrot ist besser, wenn es noch warm ist.",
             COMPLETE : "Oh, was ist das denn? Für mich?\aMampf-mampf...\aAuuuu! Mein Zahn! Dieser Gert Gänsburger!\aNaja, ist ja nicht deine Schuld. Hier, du kannst das für deine Mühe haben.",
             },
    903 : { QUEST : "Du bist jetzt vielleicht soweit, _toNpcName_ den Schnee-Weisen wegen deiner Abschlussprüfung aufzusuchen._where_", },
    5234 : { GREETING: "",
             QUEST : "Aha, da bist du ja wieder.\aBevor wir anfangen, müssen wir was essen.\aBring uns etwas Krümelkäse für unsere Brühe.\aKrümelkäse kann man nur von Großhirn-Bots holen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Wir brauchen immer noch Krümelkäse. " },
    5278 : { GREETING: "",
             QUEST : "Aha, da bist du ja wieder.\aBevor wir anfangen, müssen wir was essen.\aBring uns etwas Kaviar für unsere Brühe.\aKaviar kann man nur von Mr.-Hollywood-Bots holen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Wir brauchen immer noch Kaviar." },
    5235 : { GREETING: "",
             QUEST : "Ein einfacher Mann isst mit einem einfachen Löffel.\aEin Bot hat mir meinen einfachen Löffel weggenommen, also kann ich nicht essen.\aBring mir meinen Löffel wieder. Ich glaube, ein Ausbeuter hat ihn weggenommen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich muss einfach meinen Löffel haben." },
    5279 : { GREETING: "",
             QUEST : "Ein einfacher Mann isst mit einem einfachen Löffel.\aEin Bot hat mir meinen einfachen Löffel weggenommen, also kann ich nicht essen.\aBring mir meinen Löffel wieder. Ich glaube, ein Großkotz hat ihn weggenommen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ich muss einfach meinen Löffel haben." },
    5236 : { GREETING: "",
             QUEST : "Vielen Dank.\aSchlürf-schlürf...\aAhhh, nun musst du eine sprechende Kröte einfangen. Versuche mal, im Teich zu fischen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Wo ist die sprechende Kröte?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Du hast noch keinen Nachtisch geholt.",
              QUEST : "Oh, das ist tatsächlich eine sprechende Kröte. Gib sie mir mal.\aWas sagst du da, Kröte?\aAha.\aAha...\aDie Kröte hat gesprochen. Wir brauchen Nachtisch.\aBring uns ein paar Eistüten von _toNpcName_.\aDie Kröte möchte aus irgendwelchen Gründen Eistüten mit Rote-Bohnen-Geschmack._where_", },
    5238 : { GREETING: "",
             QUEST : "Der Weise hat dich also geschickt. Es tut mir Leid, aber wir haben seit kurzem keine Eistüten mit Rote-Bohnen-Geschmack mehr.\aWeißt du, ein paar Bots kamen rein und nahmen alle mit.\aSie sagten, sie wären für Mr. Hollywood, oder irgend so einen Quatsch.\aIch wäre sehr froh, wenn du sie mir zurückholen könntest.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du schon alle meine Eistüten gefunden?" },
    5280 : { GREETING: "",
             QUEST : "Der Weise hat dich also geschickt. Es tut mir Leid, aber wir haben seit kurzem keine Eistüten mit Rote-Bohnen-Geschmack mehr.\aWeißt du, ein paar Bots kamen rein und nahmen alles mit.\aSie sagten, sie wären für das Großhirn, oder irgend so einen Quatsch.\aIch wäre sehr froh, wenn du sie mir zurückholen könntest.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du schon alle meine Eistüten gefunden?" },
    5239 : { QUEST : "Danke, dass du meine Eistüten zurückgebracht hast!\aHier ist eine für Lil Altmann.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Bring das Eis lieber zu Lil Altmann, bevor es schmilzt.", },
    5240 : { GREETING: "",
             QUEST : "Sehr gut. Hier, für dich, Kröte ...\aSchlürf-schlürf ...\aOkay, jetzt sind wir fast fertig.\aWenn du mir nur noch etwas Puder bringen könntest, um meine Hände zu trocknen.\aIch denke, dass diese Großkotze manchmal Puder von ihren Perücken haben könnten.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du Puder gefunden?" },
    5281 : { GREETING: "",
             QUEST : "Sehr gut. Hier, für dich, Kröte ...\aSchlürf-schlürf ...\aOkay, jetzt sind wir fast fertig.\aWenn du mir nur noch etwas Puder bringen könntest, um meine Hände zu trocknen.\aIch denke, dass diese Mr.-Hollywood-Bots manchmal Puder für ihre Nasen dabei haben.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hast du Puder gefunden?" },
    5241 : { QUEST : "Okay.\aWie ich einmal sagte, um wirklich eine Torte zu werfen, darf man nicht mit der Hand werfen ...\a... sondern mit der Seele.\aIch weiß nicht, was das bedeutet, und deshalb werde ich hier sitzen und darüber nachdenken, während du Gebäude zurück eroberst.\aKomm wieder her, wenn du deine Aufgabe abgeschlossen hast.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Deine Aufgabe ist noch nicht abgeschlossen.", },
    5242 : { GREETING: "",
             QUEST : "Obgleich ich immer noch nicht weiß, wovon ich rede, bist du wahrhaft würdig.\aIch gebe dir eine letzte Aufgabe ...\aDie sprechende Kröte ist ein Er und sucht eine Freundin.\aFinde ein weitere sprechende Kröte. Die Kröte hat gesprochen.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Wo ist die andere sprechende Kröte?",
             COMPLETE : "Hui! Ich bin müde von all diesen Anstrengungen. Ich muss jetzt ruhen.\aHier, nimm deine Belohnung und hebe dich hinweg." },

    5243 : { QUEST : "Schwitze-Peter fängt schon an, die ganze Straße hinauf zu stinken.\aKannst du ihn vielleicht überreden, mal zu duschen oder so?_where_" },
    5244 : { GREETING: "",
             QUEST : "Ja, ich komm hier drin anscheinend ganz schön ins Schwitzen.\aMmmm, wenn ich vielleicht das undichte Rohr in meiner Dusche reparieren könnte ...\aIch glaube, ein Zahnrad von einem dieser winzigen Bots könnte helfen.\aGeh los und suche ein Zahnrad von einem Mikromanager, dann versuchen wir's.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Wo ist das Zahnrad, das du holen wolltest?" },
    5245 : { GREETING: "",
             QUEST : "Jau, das scheint zu funktionieren.\aAber ich fühle mich so allein, wenn ich dusche ...\aKönntest du mir vielleicht ein Quietschentchen fischen gehen, damit es mir Gesellschaft leistet?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Kein Talentchen für das Entchen?" },
    5246 : { QUEST : "Das Entchen ist toll, aber ...\aDiese ganzen Gebäude hier machen mich nervös.\aIch wäre viel entspannter, wenn es weniger Gebäude gäbe.",
             LEAVING : "",
             COMPLETE : "Okay, ich dusch mich jetzt mal. Und hier ist auch was für dich.",
             INCOMPLETE_PROGRESS : "Ich hab immer noch ein Problem mit Gebäuden.", },
    5251 : { QUEST : "Ladewig Mädelsturm soll heute Abend auftreten.\aIch habe gehört, dass er irgendein Problem mit seinem Equipment hat._where_" },
    5252 : { GREETING: "",
             QUEST : "Oh yeah! Ich kann Hilfe gut gebrauchen.\aDiese Bots kamen rein und klauten mein ganzes Zeug, als ich den Transporter auslud.\aKannst du mir helfen und mein Mikrofon zurückholen?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "He Mann, ich kann ohne mein Mikro nicht singen!" },
    5253 : { GREETING: "",
             QUEST : "Yeah, das ist mein Mikrofon.\aDanke, dass du es besorgt hast, aber...\aIch brauch echt noch mein Keyboard, um in die Tasten zu hauen.\aIch glaube, einer von diesen Unternehmensräubern hat mein Keyboard.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Noch keinen Erfolg mit meinem Keyboard?" },
    5273 : { GREETING: "",
             QUEST : "Yeah, das ist mein Mikrofon.\aDanke, dass du es besorgt hast, aber...\aIch brauch echt noch mein Keyboard, um in die Tasten zu hauen.\aIch glaube, einer von diesen Einmischern hat mein Keyboard.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Noch keinen Erfolg mit meinem Keyboard?" },
    5274 : { GREETING: "",
             QUEST : "Yeah, das ist mein Mikrofon.\aDanke, dass du es besorgt hast, aber...\aIch brauch echt noch mein Keyboard, um in die Tasten zu hauen.\aIch glaube, einer von diesen Kredithaien hat mein Keyboard.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Noch keinen Erfolg mit meinem Keyboard?" },
    5275 : { GREETING: "",
             QUEST : "Yeah, das ist mein Mikrofon.\aDanke, dass du es besorgt hast, aber...\aIch brauch echt noch mein Keyboard, um in die Tasten zu hauen.\aIch glaube, einer von diesen Prozessgeiern hat mein Keyboard.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Noch keinen Erfolg mit meinem Keyboard?" },
    5254 : { GREETING: "",
             QUEST : "Okay! Jetzt bin ich wieder voll dabei.\aWenn die nur nicht meine Plateauschuhe mitgenommen hätten ...\aDiese Schuhe sind wahrscheinlich bei einem Mr. Hollywood gelandet, wenn du mich fragst.",
             LEAVING : "",
             COMPLETE : "Okay! Jetzt geht's los.\aHallo Brrr!!!\aHä? Wo sind die denn alle?\aOkay, nimm das hier und trommle ein paar Fans für mich zusammen, ja?",
             INCOMPLETE_PROGRESS : "Ich kann ja wohl nicht barfuß auftreten, oder!?" },
    5282 : { GREETING: "",
             QUEST : "Okay! Jetzt bin ich wieder voll dabei.\aWenn die nur nicht meine Plateauschuhe mitgenommen hätten ...\aDiese Schuhe sind wahrscheinlich bei einem Großhirn gelandet, wenn du mich fragst.",
             LEAVING : "",
             COMPLETE : "Okay!! Jetzt geht's los.\aHallo Brrr!!!\aHä? Wo sind die denn alle?\aOkay, nimm das hier und trommle ein paar Fans für mich zusammen, ja?",
             INCOMPLETE_PROGRESS : "Ich kann ja wohl nicht barfuß auftreten, oder!?" },
    5283 : { GREETING: "",
             QUEST : "Okay! Jetzt bin ich wieder voll dabei.\aWenn die nur nicht meine Plateauschuhe mitgenommen hätten ...\aDiese Schuhe sind wahrscheinlich bei einem Ausbeuter gelandet, wenn du mich fragst.",
             LEAVING : "",
             COMPLETE : "Okay!! Jetzt geht's los.\aHallo Brrr!!!\aHä? Wo sind die denn alle?\aOkay, nimm das hier und trommle ein paar Fans für mich zusammen, ja?",
             INCOMPLETE_PROGRESS : "Ich kann ja wohl nicht barfuß auftreten, oder!?" },
    5284 : { GREETING: "",
             QUEST : "Okay! Jetzt bin ich wieder voll dabei.\aWenn die nur nicht meine Plateauschuhe mitgenommen hätten ...\aDiese Schuhe sind wahrscheinlich bei einem Großkotz gelandet, wenn du mich fragst.",
             LEAVING : "",
             COMPLETE : "Okay!! Jetzt geht's los.\aHallo Brrr!!!\aHä? Wo sind die denn alle?\aOkay, nimm das hier und trommle ein paar Fans für mich zusammen, ja?",
             INCOMPLETE_PROGRESS : "Ich kann ja wohl nicht barfuß auftreten, oder!?" },

    5255 : { QUEST : "Du siehst aus, als könntest du mehr Lach-Punkte gebrauchen.\aVielleicht macht dir _toNpcName_ ein gutes Angebot.\aLass es dir aber schriftlich geben ..._where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Abgemacht ist abgemacht.",
             QUEST : "Du brauchst also Lach-Punkte, was?\aKlar hab ich'n Deal für dich!\aKümmere dich einfach für mich um ein paar Chefomaten-Bots ...\aUnd ich sorge dafür, dass es sich für dich lohnt." },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Abgemacht ist abgemacht.",
             QUEST : "Du brauchst also Lach-Punkte, was?\aKlar hab ich'n Deal für dich!\aKümmere dich einfach für mich um ein paar Rechtomaten-Bots ...\aUnd ich sorge dafür, dass es sich für dich lohnt." },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Okay, aber ich bin mir sicher, dass ich dir gesagt hatte, du sollst ein paar Rechtomaten-Bots zusammentreiben.\aTja, wenn du das sagst, aber du hast dich nicht dran gehalten. ",
             INCOMPLETE_PROGRESS : "Ich glaube nicht, dass du fertig bist.",
             QUEST : "Du sagst, du bist fertig? Alle Bots vertrieben?\aDu hast da was falsch verstanden. Unsere Abmachung galt für Schachermaten-Bots.\aIch bin sicher, dass ich gesagt habe, du sollst ein paar Schachermaten-Bots für mich vertreiben." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Okay, aber ich bin mir sicher, dass ich dir gesagt hatte, du sollst ein paar Rechtomaten-Bots zusammentreiben.\aTja, wenn du das sagst, aber du hast dich nicht dran gehalten.",
             INCOMPLETE_PROGRESS : "Ich glaube nicht, dass du fertig bist.",
             QUEST : "Du sagst, du bist fertig? Alle Bots vertrieben?\aDu hast da was falsch verstanden. Unsere Abmachung galt für Monetomaten-Bots.\aIch bin sicher, dass ich gesagt habe, du sollst ein paar Monetomaten-Bots für mich vertreiben." },
    }

# ChatGarbler.py
ChatGarblerDog = ["wuff", "blaff", "rrr-wuff"]
ChatGarblerCat = ["miau", "muh"]
ChatGarblerMouse = ["quiek", "pieps", "quiekquiek"]
ChatGarblerHorse = ["wieher", "brrr"]
ChatGarblerRabbit = ["iiik", "schnuff", "schnuffschnuff", "trommel"]
ChatGarblerDuck = ["quak", "schnatter", "quakquak"]
ChatGarblerMonkey = ["ooh", "ooo", "ahh"]
ChatGarblerDefault = ["blah"]

# AvatarDNA.py
Bossbot = "Chefomat"
Lawbot = "Rechtomat"
Cashbot = "Monetomat"
Sellbot = "Schachermat"
BossbotS = "ein Chefomat"
LawbotS = "ein Rechtomat"
CashbotS = "ein Monetomat"
SellbotS = "ein Schachermat"
BossbotP = "Chefomaten"
LawbotP = "Rechtomaten"
CashbotP = "Monetomaten"
SellbotP = "Schachermaten"
BossbotSkelS = "ein Chefomat Skeletobot"
LawbotSkelS = "ein Rechtomat Skeletobot"
CashbotSkelS = "ein Monetomat Skeletobot"
SellbotSkelS = "ein Schachermat Skeletobot"
BossbotSkelP = "Chefomat Skeletobots"
LawbotSkelP = "Rechtomat Skeletobots"
CashbotSkelP = "Monetomat Skeletobots"
SellbotSkelP = "Schachermat Skeletobots"

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Details zu %s werden gesucht."
AvatarDetailPanelFailedLookup = "Kann keine Deteils zu %s finden."
AvatarDetailPanelOnline = "Bezirk: %(district)s\nLocation: %(location)s"
AvatarDetailPanelOffline = "Bezirk: offline\nOrt: offline"

# AvatarPanel.py
AvatarPanelFriends = "Freunde"
AvatarPanelWhisper = "Flüstern"
AvatarPanelSecrets = "Geheimnisse"
AvatarPanelGoTo = "Gehe zu"
AvatarPanelPet = "Doodle zeigen"
AvatarPanelIgnore = "Ignorieren"
#AvatarPanelCogDetail = "Dept: %s\nLevel: %s\n"
AvatarPanelCogLevel = "Level: %s"
AvatarPanelCogDetailClose = lClose

# PetAvatarPanel.py
PetPanelFeed = "Füttern"
PetPanelCall = "Rufen"
PetPanelGoTo = "Gehe zu"
PetPanelOwner = "Besitzer zeigen"
PetPanelScratch = "Kraulen"

# PetMood.py
PetMoodAdjectives = {
    'neutral': 'neutral',
    'hunger': 'hungrig',
    'boredom': 'gelangweilt',
    'excitement': 'aufgeregt',
    'sadness': 'traurig',
    'restlessness': 'unruhig',
    'playfulness': 'verspielt',
    'loneliness': 'einsam',
    'fatigue': 'müde',
    'confusion': 'verwirrt',
    'anger': 'ärgerlich',
    'surprise': 'überrascht',
    'affection': 'zärtlich',
    }

# LocalAvatar.py
FriendsListLabel = "Freunde"

# TeleportPanel.py
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = "Versuche zu %s zu gehen."
TeleportPanelNotAvailable = "%s ist gerade beschäftigt, versuche es später noch einmal."
TeleportPanelIgnored = "%s ignoriert dich."
TeleportPanelNotOnline = "%s ist zur Zeit nicht online."
TeleportPanelWentAway = "%s ist weggegangen."
TeleportPanelUnknownHood = "Du weißt nicht, wie du zu %s kommst! "
TeleportPanelUnavailableHood = "%s ist zur Zeit nicht erreichbar, versuche es später noch einmal."
TeleportPanelDenySelf = "Du kannst nicht zu dir selbst gehen!"
TeleportPanelOtherShard = "%(avName)s ist im Bezirk %(shardName)s, und du bist im Bezirk %(myShardName)s. Möchtest du nach %(shardName)s wechseln?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Ich bin der Chef."

# DistributedBattleFactory.py
FactoryBossTaunt = "Ich bin der Vorarbeiter."
FactoryBossBattleTaunt = "Ich möchte dich mit dem Vorarbeiter bekannt machen."

# HealJokes.py
ToonHealJokes = [
    ["Was hängt an der Wand und macht TICK-TOCK-TICK-TOCK-TICK-TOCK ...?",
     "Eine Spinne mit Stöckelschuhen. "],
    ["Was steht im Wald und macht Muh?",
     "Ein Hirsch, der Fremdspachen lernt."],
    ["Warum kann ein Gespenst schlecht lügen?",
     "Weil man es so gut durchschauen kann."],
    ["Wie kommt eine Ameise über den Fluss?",
     "Sie nimmt das A weg und fliegt rüber."],
    ["Welcher Vogel ist meistens traurig?",
     "Der Pechvogel."],
    ["Wo schmeckt der Apfelsaft am besten?",
     "Beim Trinken."],
    ["Was hat ein Mensch noch nie erzählt?",
     "Dass er gestorben ist."],
    ["Warum leben Eskimos länger?",
     "Weil sie nicht ins Gras beißen können."],
    ["Was spielen sportliche Schafe?",
     "Wolle-Ball."],
    ["Welche Biere schäumen am meisten?",
     "Die Bar-Biere."],
    ["Warum ging das Gerippe nicht über die Straße?",
     "Weil es nicht den Nerv dazu hatte."],
    ["Wie heißt das Reh mit Vornamen?",
     "Kartoffelpü."],
    ["Was ist grau und spritzt mit Marmelade?",
     "Eine Maus, die einen Pfannkuchen frisst."],
    ["In welchem Fall ist zwei mal zwei sechs?",
     "In gar keinem Fall."],
    ["Was kann man von einem Dreieck verwenden?",
     "Das Ei, der Rest ist Dreck!"],
    ["Wer hat es besser, der Kaffee oder der Tee?",
     "Der Kaffee; er darf sich setzen, der Tee muss ziehen."],
    ["Wie konnten die Leute im Mittelalter ohne Fernseher überleben?",
     "Gar nicht, sie leben ja nicht mehr."],
    ["Was passiert, wenn man einen weißen Hut ins Rote Meer taucht?",
     "Er wird nass."],
    ["Welche Zeiten sind die schönsten?",
     "Die Mahlzeiten."],
    ["Welches Spiel soll man immer anderen geben?",
     "Das Beispiel."],
    ["Was kann man nicht zum Frühstück essen?",
     "Mittag und Abendbrot."],
    ["Was gibt man einem Elefanten mit großen Füßen?",
     "Große Schuhe."],
    ["Was macht man, wenn man tiefer schlafen will?",
     "Man sägt die Beine vom Bett ab."],
    ["Welcher Satz hat keine Wörter?",
     "Der Kaffeesatz."],
    ["Was ergibt drei mal sieben?",
     "Feinen Sand."],
    ["Welchen Hang sollte man nicht hochsteigen?",
     "Den Vorhang."],
    ["Warum sind die Busse in Ostfriesland 10 Meter breit und 2 Meter lang?",
     "Weil alle vorn sitzen wollen."],
    ["Welche Hunde treten zu Weltmeisterschaften an?",
     "Boxer."],
    ["Was sagt man zu einem Gorilla mit Ohrenschützern?",
     "Alles, was man will, er kann es sowieso nicht hören."],
    ["Was mögen Katzen und Schwimmer?",
     "Das Kraulen."],
    ["Was reist um die ganze Welt und bleibt doch in der Ecke?",
     "Eine Briefmarke."],
    ["Was steht in der Mitte vom Stadion?",
     "Das d."],
    ["Wie lieben sich Igel?",
     "Gaaanz vorsichtig!"],
    ["Was ist schlimmer als ein tollwütiger Fuchs?",
     "Zwei tollwütige Füchse."],
    ["Was hängt mit verbranntem Hintern an der Wand?",
     "Die Bratpfanne."],
    ["Bei welchen Fischen stehen die Augen am engsten zusammen?",
     "Bei den kleinen."],
    ["Was steht mitten im Rhein und tutet?",
     "Ein Elefant im Urlaub."],
    ["In welche Richtung geht der Rauch einer E-Lok, die mit 100 kmh nach Westen fährt?",
     "Eine E-Lok macht gar keinen Rauch!"],
    ["Warum schauen die Schotten über den Rand ihrer Brille?",
     "Damit sich die Gläser nicht so schnell abnutzen."],
    ["Was ist am tiefsten, Bach Oder Tümpel?",
     "Die Oder."],
    ["Was passiert mit einem Engel, wenn er in einen Misthaufen fällt?",
     "Er bekommt Kotflügel."],
    ["Was hindert einen Reiter daran, auf dem Pferd zu sitzen?",
     "Der Sattel."],
    ["Wie sieht ein Anhalter aus, der Glück hatte?",
     "Mitgenommen."],
    ["Wie kriegt man einen Löwen in den Kühlschrank?",
     "Tür auf, Löwe rein, Tür zu."],
    ["Warum sieht man keine Elefanten auf Kirschbäumen?",
     "Weil sie sich gut getarnt haben."],
    ["Was kommt heraus, wenn man eine Katze mit einem Hund kreuzt?",
     "Ein Tier, das sich selbst jagt."],
    ["Worunter leiden Luftballons?",
     "Platzangst."],
    ["Woran merkt man, dass Ebbe ist?",
     "Wenn es beim Rudern staubt."],
    ["Warum ist Rätselraten gefährlich?",
     "Weil man sich den Kopf zerbricht."],
    ["Was haben nur Giraffen und andere Tiere nicht?",
     "Giraffenbabys."],
    ["Warum schlug der Mann die Uhr?",
     "Weil die Uhr zuerst schlug."],
    ["Welcher Peter macht den meisten Krach?",
     "Der Trompeter."],
    ["Was kommt heraus, wenn man einen Papagei mit einem Monster kreuzt?",
     "Ein Wesen, das immer einen Keks bekommt, wenn es einen verlangt."],
    ["Was sieht aus wie eine Katze, ist aber keine?",
     "Ein Kater."],
    ["Wann sagt ein Chinese Guten Morgen?",
     "Wenn er Deutsch gelernt hat."],
    ["Wo geht nachts das Licht hin?",
     "Schau mal im Kühlschrank nach!"],
    ["Wie hoch ist der höchste Berg?",
     "Höher als alle anderen."],
    ["Was ist das Ende von Allem?",
     "Der Buchstabe M."],
    ["Was liegt zwischen Berg und Tal?",
     "Und."],
    ["Womit würfeln die Eskimos?",
     "Mit Eiswürfeln."],
    ["Wohin fliegt die Wolke, wenn es sie juckt?",
     "Zum Wolkenkratzer."],
    ["Was hat sechs Augen und kann doch nicht sehen?",
     "Drei blinde Mäuse."],
    ["Was arbeitet nur, wenn es gefeuert wird?",
     "Eine Rakete."],
    ["Was macht der Wurm im Salat?",
     "Er schmeißt die Schnecken raus."],
    ["Was ist weiß und hüpft von Baum zu Baum?",
     "Tarzan im Nachthemd."],
    ["Was kommt heraus, wenn man einen Pinguin mit einem Tausendfüßler kreuzt?",
     "Tausend kalte Füße."],
    ["Wie viele Erbsen gehen in einen Topf?",
     "Erbsen können gar nicht gehen!"],
    ["Was ist beim Elefanten klein und beim Floh groß?",
     "Das F."],
    ["Warum haben Dinosaurier so einen langen Hals?",
     "Weil ihre Füße riechen."],
    ["Warum können Nilpferde nicht Fahrrad fahren?",
     "Weil sie keinen Daumen zum Klingeln haben."],
    ["Warum vergessen Elefanten nie etwas?",
     "Weil ihnen nie jemand etwas erzählt."],
    ["Woher wissen wir, dass die Erde rund ist?",
     "Weil wir uns die Sohlen schief laufen."],
    ["Warum hat der Elefant rote Augen?",
     "Damit er sich besser im Kirschbaum verstecken kann."],
    ["Warum hat der Schwan so einen langen Hals?",
     "Damit er bei Hochwasser nicht ertrinkt."],
    ["Kennst du den Sekundenwitz?",
     "Schon vorbei."],
    ["Was ist das älteste Instrument?",
     "Das Akkordeon, es hat die meisten Falten."],
    ["Wie verhindert man, dass ein Elefant durch ein Nadelöhr geht?",
     "Man macht einen Knoten in seinen Schwanz."],
    ["Was macht Ha-ha-ha-peng?",
     "Jemand, der sich kaputt lacht."],
    ["Warum legen Hühner Eier?",
     "Wenn sie sie werfen würden, würden sie kaputt gehen."],
    ["Warum sind die Fußstapfen vom Elefanten so groß?",
     "Weil sonst seine Füße nicht reinpassen!"],
    ["Was essen Elektriker zu Mittag?",
     "Kabelsalat."],
    ["Warum zieht der Wellensittich beim Schlafen ein Bein hoch?",
     "Wenn er beide hochzieht, fällt er von der Stange."],
    ["Woran erkennt man, dass ein Elefant im Kühlschrank war?",
     "Am Fußabdruck in der Butter."],
    ["Was ist der Unterschied zwischen einem Bäcker und einem Teppich?",
     "Der Bäcker muss um 3 aufstehen, der Teppich kann liegen bleiben."],
    ["Welchen Satz hört der Hai am liebsten?",
     "Mann über Bord!"],
    ["Was ist grau, wiegt 10 Pfund und quiekt?",
     "Eine Maus, die dringend mal Diät halten muss."],
    ["Welchen Vogel kann man mit zwei Buchstaben schreiben?",
     "NT"],
    ["Wie erpresst ein Hase einen Schneemann?",
     "Möhre her, sonst Fön!"],
    ["Warum sind Elefanten groß und grau?",
     "Wenn sie klein und gelb wären, wären sie Kanarienvögel."],
    ["Wann ist es gefährlich, in den Garten zu gehen?",
     "Wenn der Salat schießt."],
    ["Welche Tomaten kann man nicht essen?",
     "Die Automaten."],
    ["Warum hat "+ Donald +  " Zucker auf sein Kopfkissen gestreut?",
     "Er wollte süße Träume haben."],
    ["Warum brachte "+ Goofy +  " seinen Kamm zum Zahnarzt?",
     "Weil er alle Zähne verloren hatte."],
    ["Warum ließ "+ Goofy +  " das Gartentor offen?",
     "Damit die Blumen frische Luft kriegen."],
    ["Wie heißt die Frau vom Papagei?",
     "Mamagei."],
    ["Was hat Flügel, läuft aber lieber?",
     "Die Nase."],
    ["Warum duschte der Einbrecher?",
     "Um einen sauberen Abgang zu haben."],
    ["Was brennt Tag und Nacht?",
     "Die Brennnessel."],
    ["Was ist, wenn ein Schornsteinfeger in den Schnee fällt?",
     "Winter."],
    ["Warum ging "+ Pluto +  " mit einem Stein und Streichhölzern ins Bett?",
     "Mit dem Stein schmiss er das Licht aus, dann schaute er nach, ob es aus ist."],
    ["Was macht man, wenn man in der Wüste eine Schlange sieht?",
     "Man stellt sich hinten an."],
    ["Warum sind falsche Zähne wie Sterne?",
     "Beide kommen nachts heraus."],
    ["Was kann in der Hosentasche sein, selbst wenn nichts drin ist?",
     "Ein Loch."],
    ["Welches Tier ist das lustigste?",
     "Das Pferd, es veräppelt die Straße."],
    ["Welcher Bus überquerte als erster den Atlantik?",
     "Kolumbus."],
    ["Was ist schwarz und dreht sich immer im Kreis?",
     "Ein Maulwurf beim Hammerwerfen."],
    ["Was ist schwarz und hüpft auf einem Bein?",
     "Ein Maulwurf, dem beim Hammerwerfen der Hammer auf den Fuß fiel."],
    ["Warum sollte man nachts nicht in den Urwald gehen?",
     "Weil dann die Elefanten Fallschirmspringen üben."],
    ["Was ist der Unterschied zwischen einem Wasserfall?",
     "Je höher desto plumps."],
    ["Warum nahm "+ Goofy +  " eine Semmel mit aufs Klo?",
     "Um die WC-Ente zu füttern."],
    ["Warum trinken Katzen so gerne?",
     "Damit sie einen Kater kriegen."],
    ["Was sagte der große Schornstein zum kleinen Schornstein?",
     "Du bist doch zum Rauchen noch zu klein!"],
    ["Was ist schwarz-weiß gestreift und wird rot?",
     "Ein Zebra, das sich schämt."],
    ["Was ist der Unterschied zwischen einem Knochen und Schule?",
     "Der Knochen ist für den Hund und Schule für die Katz."],
    ["Was macht mmus-mmus?",
     "Eine Fliege, die rückwärts fliegt."],
    ["Was macht der Glaser, wenn er kein Glas mehr hat?",
     "Er trinkt aus der Flasche."],
    ["Was ist ein Anto?",
     "Ein Druckfehler, es sollte Auto heißen."],
    ["Was kommt heraus, wenn man einen Bären und ein Stinktier kreuzt?",
     "Puh der Bär."],
    ["Wie macht man eine Tuba sauber?",
     "Mit Tuben-Zahnpasta."],
    ["Was war am 6. Dezember 1924?",
     "Nikolaus."],
    ["Was ist klein, grün und dreieckig?",
     "Ein kleines grünes Dreieck."],
    ["Es hängt an der Wand und wenn's runterfällt, geht die Tür auf. Was ist das?",
     "Zufall."],
    ["Warum heißen Teigwaren Teigwaren?",
     "Weil sie einmal Teig waren."],
    ["Wie sagt man 'Postbote' ohne o?",
     "Briefträger."],
    ["Was kommt heraus, wenn man eine Kamera mit einem Krokodil kreuzt?",
     "Ein Schnappschuss."],
    ["Was ist braun und rennt durch den Wald?",
     "Ein ferngesteuertes Rennschnitzel."],
    ["Wo fängt ein Kreis an?",
     "Beim K."],
    ["Was kommt heraus, wenn man einen Elefanten mit einer Krähe kreuzt?",
     "Massenhaft umgeknickte Telefonmasten."],
    ["Schon mal einen Kühlschrank durch den Wald rennen sehen?",
     "Nein? Siehste, so schnell sind die!"],
    ["Was ist eine Karotte?",
     "Eine Kartoffel mit zu hohem Blutdruck."],
    ["Was ist weiß und hat sechs Ecken?",
     "Ist doch einfach! Ein Pingpongklötzchen."],
    ["Was ist grün, laut und gefährlich?",
     "Eine herandonnernde Herde Gurken."],
    ["Was ist, wenn sich zwei Jäger treffen?",
     "Dann sind beide tot."],
    ["Ein Elefant sitzt auf einem Ahornblatt. Wie kommt er wieder runter?",
     "Er wartet bis im Herbst sein Blatt abfällt."],
    ["Was ist schlimmer dran als eine Giraffe mit Halsweh?",
     "Ein Tausendfüßler mit Fußpilz."],
    ["Was macht ABC...schlürf...DEF...schlürf?",
     "Jemand, der Buchstabensuppe isst."],
    ["Wann hoppelt ein Hase über einen Baum?",
     "Wenn der Baum gefällt ist."],
    ["Was ist ein eisernes Abführmittel?",
     "Handschellen."],
    ["Was ist eine gesellige Hülsenfrucht?",
     "Eine Kontaktlinse."],
    ["Was ist weiß mit schwarzen und roten Punkten?",
     "Ein Dalmatiner, der die Masern hat."],
    ["Was sind Früchte des Zorns?",
     "Ohrfeigen."],
    ["Was macht ein Kaugummi, wenn er um die Ecke geht?",
     "Er bleibt kleben."],
    ["Was ist grau, wiegt 200 Pfund und sagt: Na, Miez-Miez-Miez?",
     "Eine 200-Pfund-Maus. "],
    ["Wie fängt man am besten ein Reh?",
     "Man schleicht sich an und streut ihm Salz auf den Schwanz."],
    ["Wie fängt man am besten ein Kaninchen?",
     "Man hockt sich hinter einen Busch und macht ein Geräusch wie ein Salatblatt. "],
    ["Wo kommt der Juli vor dem Juni?",
     "Im Duden."],
    ["Welches Tier dreht sich nach seinem Tod noch 150 Mal?",
     "Das Grillhähnchen."],
    ["Was hat ein Fell, miaut und jagt Mäuse unter Wasser?",
     "Ein Katzenfisch."],
    ["Monikas Vater hat fünf Töchter. Sie heißen Lala, Lele, Lili und Lulu. Wie heißt die fünfte?",
     "Na, Monika!"],
    ["Was ist außen grün und innen gelb?",
     "Eine als Gurke verkleidete Banane."],
    ["Was macht ein Ostfriese, der mit einem Messer auf dem Deich steht?",
     "Er sticht in See."],
    ["Was wiegt 4 Tonnen, hat einen Rüssel und ist leuchtend rot?",
     "Ein Elefant, dem etwas peinlich ist."],
    ["Was ist, wenn ein Schwein ums Eck geht?",
     "Es ist weg."],
    ["Was wird eine Tomate, wenn sie auf die Straße geht?",
     "Ketchup."],
    ["Was ist ein Cowboy, der sein Pferd verloren hat?",
     "Ein Sattelschlepper."],
    ["Was sagt die Erdnuss zum Elefanten?",
     "Gar nichts. Erdnüsse können nicht reden."],
    ["Was sagen Elefanten, wenn sie aufeinanderprallen?",
     "Die Welt ist klein, was?"],
    ["Was ist groß, grau, und telefoniert aus Afrika?",
     "Ein Telefant."],
    ["Was sagt der eine Floh zum anderen?",
     "Sollen wir laufen oder eine Katze nehmen?"],
    ["Was ist grün, glücklich, und hüpft von Grashalm zu Grashalm?",
     "Eine Freuschrecke."],
    ["Was ist schlimmer, als ein Wurm in dem Apfel zu finden, in den man gerade gebissen hat?",
     "Einen halben Wurm zu finden."],
    ["Was fängt mit Z an und kann schwimmen?",
     "Zwei Enten."],
    ["Was kommt heraus, wenn man eine Brieftaube mit einem Papagei kreuzt?",
     "Ein Vogel, der beim Fliegen nach dem Weg fragen kann."],
    ["Was ist der Unterschied zwischen einem Briefkasten und einem Elefanten?",
     "Schon mal versucht, einen Brief in einen Elefanten einzuwerfen?"],
    ["Was ist der Unterschied zwischen einem Sack Mehl und einem Saxofon?",
     "Blas mal rein!"],
    ["Was machst du, damit dein Computer nicht abstürzt?",
     "Ihn auf den Boden stellen."],
    ["Warum laufen Dudelsackspieler beim Spielen hin und her?",
     "Sie versuchen, den Tönen zu entkommen."],
    ["Warum tragen Elefanten Turnschuhe?",
     "Damit es nicht so plumpst, wenn sie aus den Bäumen springen."],
    ["Warum ist Ostfriesland so flach?",
     "Damit die Ostfriesen schon am Mittwoch sehen, wer Sonntag zu Besuch kommt."],
    ["Warum flog Aschenputtel aus dem Basketballteam?",
     "Es lief immer vom Ball weg."],
    ["Warum heißt der Löwe Löwe?",
     "Weil er durch die Wüste löwt."],
    ["Warum heißt die Haut Haut?",
     "Weil man drauf haut."],
    ["Warum macht der Hahn beim Krähen die Augen zu? ",
     "Er will die Hühner damit beeindrucken, dass er es auswendig kann."],
    ["Was sagt ein Papst zum anderen?",
     "Es gibt immer nur einen Papst ..."],
    ["Was sagt ein Magnet zum anderen?",
     "Ich finde dich echt anziehend ..."],
    ["Wie alt kann man in Japan werden?",
     "Mitsubishi Glück wird man Honda."],
    ["Was sagt ein Japaner zu seiner Frau, nachdem sie einen Sohn geboren hat?",
     "Its a Sony."],
    ["Warum ist "+ MickeyMouse +  " ins Weltall geflogen?",
     "Er wollte "+ Pluto +  "finden."],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("hmm","he","ha","Höhö")
MovieHealLaughterHits1= ("Hahaha","Hihi","Kicher","Ha Ha")
MovieHealLaughterHits2= ("MUA-HA-HA!","HO HO HO!","HA HA HA!")

# MovieSOS.py
MovieSOSCallHelp = "%s HILFE!"
MovieSOSWhisperHelp = "%s braucht Hilfe im Kampf!"
MovieSOSObserverHelp = "HILFE!"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "Hi %s! Ich helfe gern!"
MovieNPCSOSGoodbye = "Bis später!"
MovieNPCSOSToonsHit = "Toons Treffen Immer!"
MovieNPCSOSCogsMiss = "Bots Hauen Immer Daneben!"
MovieNPCSOSRestockGags = "%s Gags werden aufgefüllt!"
MovieNPCSOSHeal = "Heilen"
MovieNPCSOSTrap = "Fallen stellen"
MovieNPCSOSLure = "Ködern"
MovieNPCSOSSound = "Volldröhnen"
MovieNPCSOSThrow = "Werfen"
MovieNPCSOSSquirt = "Spritzen"
MovieNPCSOSDrop = "Fallen lassen"
MovieNPCSOSAll = "Alle"

# MovieSuitAttacks.py
MovieSuitCancelled = "ABGEBROCHEN\nABGEBROCHEN\nABGEBROCHEN"

# RewardPanel.py
RewardPanelToonTasks = "Toon-Aufgaben"
RewardPanelItems = "Zurückeroberte Gegenstände"
RewardPanelMissedItems = "Nicht zurückeroberte Gegenstände"
RewardPanelQuestLabel = "Aufgabe %s"
RewardPanelCongratsStrings = ["Yeah!", "Glückwunsch!", "Wow!",
                              "Cool!", "Toll!", "Toon-tastisch!"]
RewardPanelNewGag = "Neuer %(gagName)s Gag für %(avName)s!"
RewardPanelMeritsMaxed = "Maximal"
RewardPanelMeritBarLabel = "Verdienste"
RewardPanelMeritAlert = "Beförderungsfähig!"

RewardPanelCogPart = "Du hast ein Teil eines Bot-Kostüms erhalten!"
RewardPanelPromotion = "Im Ablauf %s, Beförderungsfähig!"

# Cheesy effect descriptions: (short desc, sentence desc)
CheesyEffectDescriptions = [
    ("Normaler Toon", "du wirst normal"),
    ("Großer Kopf", "du bekommst einen großen Kopf"),
    ("Kleiner Kopf", "du bekommst einen kleinen Kopf"),
    ("Große Beine", "du bekommst große Beine"),
    ("Kleine Beine", "du bekommst kleine Beine"),
    ("Großer Toon", "du wirst etwas größer"),
    ("Kleiner Toon ", "du wirst etwas kleiner"),
    ("Flachporträt", "du wirst zweidimensional"),
    ("Flachprofil", "du wirst zweidimensional"),
    ("Durchsichtig", "du wirst durchsichtig"),
    ("Keine Farbe", "du wirst farblos"),
    ("Unsichtbarer Toon", "du wirst unsichtbar"),
    ]
CheesyEffectIndefinite = "Bis du einen anderen Effekt wählst, %(effectName)s%(whileIn)s."
CheesyEffectMinutes = "Die nächsten %(time)s Minuten, %(effectName)s%(whileIn)s."
CheesyEffectHours = "Die nächsten %(time)s Stunden, %(effectName)s%(whileIn)s."
CheesyEffectDays = "Dieie nächsten %(time)s Tage, %(effectName)s%(whileIn)s."
CheesyEffectWhileYouAreIn = " während du in %s bist"
CheesyEffectExceptIn = ", außer in %s"


# SuitBattleGlobals.py
SuitFlunky = "Kriecher"
SuitPencilPusher = "Griffel\3schieber"
SuitYesman = "Jasager"
SuitMicromanager = "Mikro\3manager"
SuitDownsizer = "Niedermacher"
SuitHeadHunter = "Köpfchen\3jäger"
SuitCorporateRaider = "Unternehmens\3räuber"
SuitTheBigCheese = "Großhirn"
SuitColdCaller = "Aufschwatzer"
SuitTelemarketer = "Tele\3marketer"
SuitNameDropper = "Wichtig\3tuer"
SuitGladHander = "Glücks\3händchen"
SuitMoverShaker = "Aufbauscher"
SuitTwoFace = "Falsch\3gesicht"
SuitTheMingler = "Einmischer"
SuitMrHollywood = "Mr. Hollywood"
SuitShortChange = "Keinmünz"
SuitPennyPincher = "Pfennig\3fuchser"
SuitTightwad = "Geizhals"
SuitBeanCounter = "Kieszähler"
SuitNumberCruncher = "Erbsen\3zähler"
SuitMoneyBags = "Geldsack"
SuitLoanShark = "Kredithai"
SuitRobberBaron = "Ausbeuter"
SuitBottomFeeder = "Schnäppchen\3jäger"
SuitBloodsucker = "Blut\3sauger"
SuitDoubleTalker = "Dumm\3schwätzer"
SuitAmbulanceChaser = "Unfall\3abzocker"
SuitBackStabber = "Heimtücker"
SuitSpinDoctor = "Schönredner"
SuitLegalEagle = "Prozessgeier"
SuitBigWig = "Großkotz"

# Singular versions (indefinite article)
SuitFlunkyS = "einen Kriecher"
SuitPencilPusherS = "einen Griffelschieber"
SuitYesmanS = "einen Jasager"
SuitMicromanagerS = "einen Mikromanager"
SuitDownsizerS = "einen Niedermacher"
SuitHeadHunterS = "einen Köpfchenjäger"
SuitCorporateRaiderS = "einen Unternehmensräuber"
SuitTheBigCheeseS = "einen Großhirn"
SuitColdCallerS = "einen Aufschwatzer"
SuitTelemarketerS = "einen Telemarketer"
SuitNameDropperS = "einen Wichtigtuer"
SuitGladHanderS = "eine Glückshändchen"
SuitMoverShakerS = "einen Aufbauscher"
SuitTwoFaceS = "einem Falschgesicht"
SuitTheMinglerS = "einen Einmischer"
SuitMrHollywoodS = "einen Mr. Hollywood"
SuitShortChangeS = "eine Keinmünz"
SuitPennyPincherS = "einen Pfennigfuchser"
SuitTightwadS = "einen Geizhals"
SuitBeanCounterS = "einen Kieszähler"
SuitNumberCruncherS = "einen Erbsenzähler"
SuitMoneyBagsS = "einen Geldsack"
SuitLoanSharkS = "einen Kredithai"
SuitRobberBaronS = "einen Ausbeuter"
SuitBottomFeederS = "einen Schnäppchenjäger"
SuitBloodsuckerS = "einen Blutsauger"
SuitDoubleTalkerS = "einen Dummschwätzer"
SuitAmbulanceChaserS = "einen Unfallabzocker"
SuitBackStabberS = "einem Heimtücker"
SuitSpinDoctorS = "einen Schönredner"
SuitLegalEagleS = "einen Prozessgeier"
SuitBigWigS = "einem Großkotz"

# Plural versions
SuitFlunkyP = "Kriecher"
SuitPencilPusherP = "Griffelschieber"
SuitYesmanP = "Jasager"
SuitMicromanagerP = "Mikromanager"
SuitDownsizerP = "Niedermacher"
SuitHeadHunterP = "Köpfchenjäger"
SuitCorporateRaiderP = "Unternehmensräuber"
SuitTheBigCheeseP = "Großhirne"
SuitColdCallerP = "Aufschwatzer"
SuitTelemarketerP = "Telemarketer"
SuitNameDropperP = "Wichtigtuer"
SuitGladHanderP = "Glückshändchen"
SuitMoverShakerP = "Aufbauscher"
SuitTwoFaceP = "Falschgesichter"
SuitTheMinglerP = "Einmischer"
SuitMrHollywoodP = "Mr. Hollywoods"
SuitShortChangeP = "Keinmünze"
SuitPennyPincherP = "Pfennigfuchser"
SuitTightwadP = "Geizhälse"
SuitBeanCounterP = "Kieszähler"
SuitNumberCruncherP = "Erbsenzähler"
SuitMoneyBagsP = "Geldsack"
SuitLoanSharkP = "Kredithaie"
SuitRobberBaronP = "Ausbeuter"
SuitBottomFeederP = "Schnäppchenjäger"
SuitBloodsuckerP = "Blutsauger"
SuitDoubleTalkerP = "Dummschwätzer"
SuitAmbulanceChaserP = "Unfallabzocker"
SuitBackStabberP = "Heimtücker"
SuitSpinDoctorP = "Schönredner"
SuitLegalEagleP = "Prozessgeier"
SuitBigWigP = "Großkotze"

SuitFaceOffDefaultTaunts = ['Huh!']

SuitAttackDefaultTaunts = ['Da hast du\'s!', 'Aufschreiben!']

SuitAttackNames = {
  'Audit' : 'Buchprüfung!',
  'Bite' : 'Beißen!',
  'BounceCheck' : 'Geplatzter Scheck',
  'BrainStorm' : 'Brainstorm!',
  'BuzzWord' : 'Schlagwort!',
  'Calculate' : 'Kalkulieren!',
  'Canned' : 'Rausgeschmissen!',
  'Chomp' : 'Mampfen!',
  'CigarSmoke' : 'Zigarrenrauch!',
  'ClipOnTie' : 'Ansteckkrawatte!',
  'Crunch' : 'Zermalmen!',
  'Demotion' : 'Zurückversetzung!',
  'Downsize' : 'Niedermachen!',
  'DoubleTalk' : 'Dummschwätzen!',
  'EvictionNotice' : 'Zwangsräumung!',
  'EvilEye' : 'Böser Blick!',
  'Filibuster' : 'Verschleppungstaktik!',
  'FillWithLead' : 'Mit Blei füllen!',
  'FiveOClockShadow' : "Augenringe!",
  'FingerWag' : 'Tz-Tz!',
  'Fired' : 'Gefeuert!',
  'FloodTheMarket' : 'Markt überfluten!',
  'FountainPen' : 'Füllfederhalter!',
  'FreezeAssets' : 'Vermögen einfrieren!',
  'Gavel' : 'Hammer!',
  'GlowerPower' : 'Finsterblick!',
  'GuiltTrip' : 'Bußgang!',
  'HalfWindsor' : 'Einfacher Windsor!',
  'HangUp' : 'Auflegen!',
  'HeadShrink' : 'Irrenarzt!',
  'HotAir' : 'Heiße Luft!',
  'Jargon' : 'Fachchinesisch!',
  'Legalese' : 'Juristenjargon!',
  'Liquidate' : 'Liquidieren!',
  'MarketCrash' : 'Börsenkrach!',
  'MumboJumbo' : 'Fauler Zauber!',
  'ParadigmShift' : 'Paradigmenwechsel!',
  'PeckingOrder' : 'Hackordnung!',
  'PickPocket' : 'Taschendieb!',
  'PinkSlip' : 'Blauer Brief!',
  'PlayHardball' : 'Hart durchgreifen!',
  'PoundKey' : 'Tasten drücken!',
  'PowerTie' : 'Kräfte messen!',
  'PowerTrip' : 'Ego-Trip!',
  'Quake' : 'Beben!',
  'RazzleDazzle' : 'Tamtam!',
  'RedTape' : 'Bürokratie!',
  'ReOrg' : 'Re-Org!',
  'RestrainingOrder' : 'Einstweilige Verfügung!',
  'Rolodex' : 'Rolodex!',
  'RubberStamp' : 'Abstempeln!',
  'RubOut' : 'Ausradieren!',
  'Sacked' : 'Entlassen!',
  'SandTrap' : 'Bunker!',
  'Schmooze' : 'Schmus!',
  'Shake' : 'Schütteln!',
  'Shred' : 'Shreddern!',
  'SongAndDance' : 'Getue!',
  'Spin' : 'Schönreden!',
  'Synergy' : 'Synergie!',
  'Tabulate' : 'Tabellarisieren!',
  'TeeOff' : 'Loslegen!',
  'ThrowBook' : 'Verurteilen!',
  'Tremor' : 'Schaudern!',
  'Watercooler' : 'Wasserkühler!',
  'Withdrawal' : 'Abhebung!',
  'WriteOff' : 'Abschreiben!',
  }

SuitAttackTaunts = {
    'Audit': ["Ich glaube, deine Bilanz stimmt nicht.",
              "Du bist wohl in den roten Zahlen.",
              "Lass mich mal bei der Buchhaltung helfen.",
              "Deine Sollseite ist viel zu hoch.",
              "Wir wollen mal dein Vermögen prüfen.",
              "Damit hast du jetzt Schulden.",
              "Sehen wir uns mal an, wie hoch die Forderungen sind.",
              "Damit dürfte dein Konto leer sein.",
              "Höchste Zeit, mal deine Ausgaben abzurechnen.",
              "Ich habe einen Fehler in deinen Büchern gefunden.",
              ],
    'Bite': ["Möchtest du einen Bissen?",
             "Versuch mal einen Bissen hiervon!",
             "Du beißt mehr ab, als du schlucken kannst.",
             "Hunde die beißen, bellen nicht.",
             "Da wirst du dir die Zähne dran ausbeißen.",
             "Achtung, ich beiße!",
             "Ich beiße nicht nur, wenn man mich in die Enge treibt.",
             "Ich hol mir nur schnell einen Bissen. ",
             "Ich habe den ganzen Tag noch keinen Bissen gegessen.",
             "Ich möchte nur ein Bissen essen. Ist das zuviel verlangt?",
             ],
    'BounceCheck': ["Ach, zu blöd, du bist witzlos.",
                    "Von dir steht noch eine Zahlung aus.",
                    "Ich glaube, das ist dein Scheck.",
                    "Du schuldest mir was.",
                    "Ich treibe diese Forderung ein.",
                    "Dieser Scheck ist kein gültiges Zahlungsmittel.",
                    "Man wird dir das in Rechnung stellen",
                    "Bezahle das.",
                    "Das wird dich was kosten.",
                    "Ich möchte das in bar kassieren.",
                    "Das fällt dir wieder auf die Füße.",
                    "Das ist ein falscher Fuffziger.",
                    "Ich ziehe eine Bearbeitungsgebühr ab.",
                    ],
    'BrainStorm':["Ich habe Regen vorhergesagt.",
                  "Hoffentlich hast du deinen Schirm dabei.",
                  "Ich möchte dich erleuchten.",
                  "Vielleicht fällt ja was vom Himmel?",
                  "Na, du strahlst ja gar nicht mehr, Toon?",
                  "Fertig für einen ordentlichen Guss?",
                  "Ich werde dich im Sturm nehmen.",
                  "Das nenn ich eine Blitzattacke.",
                  "Ich verteile gern kalte Duschen.",
                  ],
    'BuzzWord':["Entschuldigung, wenn ich weiter auf dich einhämmere.",
                "Hast du das Neueste schon gehört?",
                "Kannst du da mithalten?",
                "Kannst du es schon auswendig, Toon?",
                "Soll ich ein gutes Wort für dich einlegen?",
                "Jeder Schlag ein Treffer.",
                "Du solltest schlagende Argumente sammeln.",
                "Versuch mal, diesem Schlag auszuweichen.",
                "Pass auf, sonst kriegst du eins auf's Dach.",
                "Du hast anscheinend einen Schlaganfall.",
                ],
    'Calculate': ["Diese Zahlen ergeben doch einen Sinn!",
                  "Hast du darauf gezählt?",
                  "Wenn wir alles zusammenzählen, geht's abwärts mit dir.",
                  "Ich helfe dir mal, eins und eins zusammenzuzählen.",
                  "Hast du alle Ausgaben eingetragen?",
                  "Nach meiner Kalkulation wirst du dich nicht mehr lange halten können.",
                  "Hier ist das Endergebnis",
                  "Wow, deine Rechnung wird immer höher.",
                  "Versuch bloß nicht, diese Zahlen zu manipulieren! ",
                  Cogs +" : 1 Toons: 0",
                  ],
    'Canned': ["Na, wie sieht's draußen aus?",
               "Du kannst dich gleich wegschmeißen.",
               "Frisch rausgeschmissen ist halb verloren.",
               "Du schmeißt mit dem Schinken nach der Wurst.",
               "Der Rausschmiss lauert überall.",
               "Mensch, ärgere dich nicht.",
               "Eene-meene-maus, und du bist raus.",
               "Ich schmeiß dich raus!",
               "Ich schmeiß dich raus und mach mir nichts draus!",
               "Raus!!",
               ],
    'Chomp': ["Schau dir diese Raffzähne an!",
              "Mampf-mampf-mampf!",
              "Hier ist was zu mampfen.",
              "Suchst du nach was zu mampfen?",
              "Da wirst du ordentlich dran zu kauen haben.",
              "Dich verspeis ich zum Abendessen.",
              "Ich fress gern kleine Toons!",
              ],
    'ClipOnTie': ["Du solltest dich für unser Treffen lieber warm anziehen.",
                  "Ohne deinen Schlips kommst du nicht RAUS.",
                  "Die elegantesten "+ Cogs +  " tragen sowas.",
                  "Probier mal die Größe.",
                  "Für den Erfolg musst du dich gut anziehen.",
                  "Keine Krawatte, keine Bedienung.",
                  "Brauchst du Hilfe beim Anlegen?",
                  "Nichts strahlt so viel Macht aus wie eine gute Krawatte.",
                  "Schaun wir, mal, ob diese passt.",
                  "Die wird dir die Luft abdrücken.",
                  "Du solltest dich gut anziehen, bevor du RAUS gehst.",
                  "Ich denke, ich ziehe jetzt mal den Knoten fest.",
                  ],
    'Crunch': ["Du reibst dich wohl gerade auf.",
               "Malmzeit!",
               "Ich gebe dir mal was zu kauen!",
               "Hier, zermalm das mal!",
               "Da kann gut zermalmen.",
               "Magst du es lieber weich oder bissfest?",
               "Ich hoffe, du bist bereit für die Malmzeit.",
               "Siehst aus, als solltest du zermalmt werden!",
               "Ich zermalm dich wie einen Käfer."
               ],
    'Demotion': ["Du steigst auf der Karriereleiter ab.",
                 "Ich schick dich zurück in die Poststelle.",
                 "Gib dein Namensschild zurück.",
                 "Ab geht er, der Peter!",
                 "Du sitzt wohl fest.",
                 "Geh dorthin zurück, woher du gekommen bist.",
                 "Du sitzt in einer Sackgasse.",
                 "In nächster Zeit wird sich bei dir gar nichts bewegen.",
                 "Du kommst nirgendwo mehr hin.",
                 "Das wird ein schwarzer Fleck in deiner Personalakte.",
                 ],
    'Downsize': ["Komm runter!",
                 "Weißt du, wie du runter kommst?",
                 "Da wollen wir uns doch mal dran machen.",
                 "Was ist los? Du siehst so niedergeschlagen aus.",
                 "Geht's bergab?",
                 "Was geht nieder? Du!",
                 "Ich nehme mir gern Leute vor, die niedriger stehen als ich.",
                 "Warum mach ich dich nicht einfach fertig, um nicht zu sagen, nieder?",
                 "Wart ab, bis ich niederfahre!",
                 "Wirf dich nieder, du Wurm!",
                 "Du wirst gleich was Niederschmetterndes erleben.",
                 "Dieser Angriff macht alles nieder, was sich bewegt!",
                 ],
    # Hmmm - where is double talker?
    'EvictionNotice': ["Zeit für einen Umzug.",
                       "Pack deine Taschen, Toon.",
                       "Du solltest mal über eine neue Umgebung nachdenken.",
                       "Betrachte dich als abserviert.",
                       "Du bist mit der Miete im Rückstand.",
                       "Das wird extrem ungemütlich werden.",
                       "Ich werde dich mit der Wurzel ausgraben.",
                       "Ich schicke dich Packen.",
                       "Du bist hier fehl am Platz.",
                       "Bereite dich auf eine Verlegung vor.",
                       "Du bist reif für die Insel.",
                       ],
    'EvilEye': ["Dich trifft gleich mein böser Blick.",
                "Augenblick mal.",
                "Wart mal. Ich habe was im Auge.",
                "Ich lasse dich nicht aus den Augen!",
                "Könntest du das mal für mich im Auge behalten?",
                "Ich habe einen Blick für das Böse.",
                "Ich hau dir eins auf's Auge!",
                "Ich bin so bösartig, wie's nur geht!",
                "Ich pack dich direkt ins Auge des Sturms!",
                "Sieh dich vor, ich rolle schon mit den Augen!",
                ],
    'Filibuster':["Soll ich vollmachen?",
                  "Das hier wird eine Weile dauern.",
                  "Ich könnte den ganzen Tag damit zubringen.",
                  "Ich muss noch nicht mal zwischendurch Luft holen.",
                  "Es läuft und läuft und läuft ... ",
                  "Davon kann ich gar nicht genug kriegen.",
                  "Ich kann reden, bis dir schwarz vor Augen wird.",
                  "Ich kann reden, bis dir die Ohren abfallen?",
                  "Dann werd ich mal loslegen.",
                  "Ich krieg immer noch das eine oder andere Wort dazwischen.",
                  ],
    'FingerWag': ["Ich hab dir's schon tausend Mal gesagt.",
                  "Reiß dich zusammen, Toon.",
                  "Das ist nicht zum Lachen.",
                  "Ich komme gleich rüber!",
                  "Ich hab's satt, mich ständig zu wiederholen.",
                  "Ich denke doch, wir hatten das schon mal.",
                  "Du hast keinen Respekt vor uns"+ Cogs +  ".",
                  "Jetzt pass mal auf.",
                  "Bla-bla-bla-bla-bla.",
                  "Lege es nicht darauf an, dieses Treffen abzubrechen.",
                  "Muss ich selbst dazwischen gehen?",
                  "Wir haben das alles schon mal besprochen.",
                  ],
    'Fired': ["Ich hoffe, du hast was zum Naschen mitgebracht.",
              "Hier wird's gleich ziemlich warm werden.",
              "Das dürfte dir ein wenig einheizen.",
              "Ich hoffe, du bist kaltblütig.",
              "Heiß, heißer, am heißesten.",
              "Spiel lieber nicht mit dem Feuer.",
              "Wage es, die Glut zu schüren!",
              "Das feuert vielleicht!",
              "Kannst du noch Aua sagen?",
              "Ich hoffe, du hattest Sonnenschutz drauf.",
              "Jetzt kommst du dir wohl verbraten vor?",
              "Du wirst in Flammen aufgehen.",
              "Du wirst direkt in der Hölle landen.",
              "Du bist nichts als ein Strohfeuer.",
              "Ich glaube, ich kriege grad die flammende Wut.",
              "Gleich funkt's!",
              "Na, da brat mir einer'n Storch!",
              "Ich mach dir ordentlich Feuer unter'm Hintern.",
              ],
    'FountainPen': ["Das wird böse Spuren hinterlassen.",
                    "Jetzt wollen wir dich mal in die Tinte reiten.",
                    "Ich steck dich kopfüber ins Tintenfass.",
                    "Du wirst eine gute Reinigung nötig haben.",
                    "Du solltest dich mal umziehen.",
                    "Es sprudelt so schön aus diesem Füllfederhalter.",
                    "Hier, ich nehme meinen Stift.",
                    "Kannst du meine Schrift lesen?",
                    "Ich nenne das die Feder des Schicksals.",
                    "Deine Akte ist ein wenig befleckt ... ",
                    "Du sitzt ganz schön in der Tinte, was?",
                    ],
    'FreezeAssets': ["Dein Vermögen ist meins.",
                     "Kriegst du schon kalte Füße?",
                     "Ich hoffe, du hast keine Pläne.",
                     "Damit bist du erst mal auf Eis gelegt.",
                     "Es weht ein kalter Wind.",
                     "Der Winter schlägt diesjahr zeitig zu.",
                     "Das lässt mich völlig kalt.",
                     "Mein Plan hat sich jetzt herauskristallisiert.",
                     "Es wird dich ganz kalt erwischen.",
                     "Geh lieber nicht auf dem Eis tanzen.",
                     "Ich hoffe, du magst Kalte Platte.",
                     "Ich bewahre kühles Blut.",
                     ],
    'GlowerPower': ["Schaust du mich an?",
                    "Man sagt, ich hätte einen stechenden Blick.",
                    "Ich riskiere gern mal einen Blick.",
                    "Finster, finster, Nachtgespinster!",
                    "Schau mir in die Augen, Kleines!",
                    "Was hältst du von diesen ausdrucksvollen Augen?",
                    "Meine Augen sind das Beste an mir.",
                    "Diese Augen haben was.",
                    "Kuckuck, ich seh dich!",
                    "Sieh mich an ...",
                    "Wollen wir mal einen Blick auf deine Zukunft werfen?",
                    ],
    'GuiltTrip': ["Ich werde dir einen Bußgang verordnen!",
                  "Fühlst du dich schuldig?",
                  "Das ist alles deine Schuld!",
                  "Für mich bist du immer der Schuldige!",
                  "Wate im Sumpf deiner eigenen Schuld!",
                  "Ich spreche nie wieder mit dir!",
                  "Du solltest lieber sagen, dass es dir Leid tut.",
                  "Du hast es mit mir verdorben bis in die Steinzeit und zurück!",
                  "Fertig zum Gehen?",
                  "Ruf mich an, wenn du von deinem Gang zurück bist.",
                  "Wann kommst du von deinem Gang zurück?",
                  ],
    'HalfWindsor': ["Das ist die modischste Krawatte, die dir je unterkommen wird! ",
                    "Versuch mal, dich nicht zu verknoten.",
                    "Das ist erst der Anfang vom Ende.",
                    "Du hast Glück, dass ich nicht noch einen doppelten Windsor habe!",
                    "Diese Krawatte kannst du dir gar nicht leisten. ",
                    "Ich wette, du hast einen einfachen Windsor noch nicht mal GESEHEN! ",
                    "Diese Krawatte ist nicht in deiner Liga.",
                    "Diese Krawatte wäre bei dir reine Verschwendung.",
                    "Du bist noch nicht mal die Hälfte dieser Krawatte wert!",
                  ],
    'HangUp': ["Deine Verbindung ist unterbrochen worden.",
               "Auf Wiederhören!",
               "Es ist Zeit, dass ich unsere Verbindung beende.",
               "... und ruf mich ja nicht zurück!",
               "Klick!",
               "Dieses Gespräch ist beendet.",
               "Ich trenne diese Verbindung.",
               "Bei dir legen wohl die meisten wieder auf.",
               "Anscheinend hast du eine schwache Verbindung.",
               "Deine Zeit ist abgelaufen.",
               "Ich hoffe, dass das klar und deutlich bei dir ankommt.",
               "Falsch verbunden.",
               ],
    'HeadShrink': ["Du siehst ein wenig irre aus.",
                   "Schatz, ich hab den Toon verarztet.",
                   "Ärztlichen Glückwunsch.",
                   "Irren, bis der Arzt kommt.",
                   "Ich irre, daher bin ich.",
                   "Darüber musst du doch den Kopf nicht verlieren.",
                   "Bist du jetzt ganz verrückt geworden?",
                   "Kopf hoch! Oder lieber runter?",
                   "Manche Dinge sind verrückter, als sie scheinen.",
                   "Gute Toons kommen und irren.",
                   ],
    'HotAir':["Wir haben grad eine heiße Diskussion.",
              "Du hast wohl eine Hitzewallung.",
              "Ich koche gleich über.",
              "Nichts wird so heiß gegessen, wie es gekocht wird.",
              "Ess wäre besser für dich, du hättest heiße Neuigkeiten ...",
              "Immer dran denken, wo Rauch ist, ist auch Feuer.",
              "Du siehst ein bisschen ausgebrannt aus.",
              "Da löst sich wieder eine Versammlung in Rauch auf.",
              "Jetzt sollte ich wohl noch etwas Benzin ins Feuer gießen.",
              "Ich werde die Beziehung am Köcheln halten.",
              "Ich hab ein paar heiße Tipps für dich.",
              "Luftangriff!!!",
              ],
    'Jargon':["Was für ein Unsinn.",
              "Schau mal, ob du das kapierst.",
              "Ich hoffe, ich drücke mich klar und deutlich aus.",
              "Ich werde wohl lauter sprechen müssen.",
              "Ich bestehe darauf, meine Meinung zu sagen!",
              "Ich bin sehr direkt.",
              "Zu diesem Thema muss ich meine alleingültige Meinung ausführlich darstellen.",
              "Siehst du, Worte können doch verletzen.",
              "Verstehst du, was ich meine?",
              "Worte, Worte, nichts als Worte.",
              ],
    'Legalese':["Ich habe eine Unterlassungsanordnung für dich.",
                "Du wirst rechtlich gesehen verlieren.",
                "Bist du dir über die gesetzlichen Folgen im Klaren?",
                "Du stehst nicht über dem Gesetz!",
                "Du solltest gesetzlich verboten werden.",
                "Bei mir gibt's kein rückwirkendes Strafgesetz!",
                "Die Meinungen in diesem Schlagabtausch sind nicht die von Disneys Toontown Online.",
                "Wir haften nicht für Schäden, die durch diesen Schlagabtausch entstehen.",
                "Die Ergebnisse dieses Schlagabtauschs können unterschiedlich sein.",
                "Dieser Schlagabtausch verliert seine Gültigkeit soweit ein Verbot vorhanden ist.",
                "Du passt nicht in mein Rechtssystem!",
                "Du kannst mit Rechtsangelegenheiten nicht umgehen.",
                ],
    'Liquidate':["Ich halte die Dinge gern im Fluss.",
                 "Hast du vielleicht gerade Liquiditätsprobleme?",
                 "Ich werde dein Vermögen etwas bereinigen müssen.",
                 "Höchste Zeit, mit dem Strom zu schwimmen.",
                 "Denk dran, wenn es nass ist, rutscht man leicht aus.",
                 "Deine Zahlen schwimmen davon.",
                 "Du scheinst wegzurutschen.",
                 "Es fällt dir alles auf die Füße.",
                 "Ich würde sagen, deine Sache wird wässrig.",
                 "Du wirst weggespült.",
                 ],
    'MarketCrash':["Ich werde es hier mächtig krachen lassen.",
                   "Du wirst den Krach nicht überleben.",
                   "Ich bin mehr, als der Aktienmarkt vertragen kann.",
                   "Ich habe einen echten Crashkurs für dich!",
                   "Jetzt komme ich herabgestürzt!",
                   "Ich wüte wie ein Bulle.",
                   "Sieht aus, als würde die Börse krachen.",
                   "Du solltest lieber aussteigen!",
                   "Verkaufen! Schnell verkaufen!",
                   "Soll ich die Rezession anführen?",
                   "Alle steigen aus, solltest du das nicht auch tun?",
                   ],
    'MumboJumbo':["Ich will das mal ganz deutlich sagen.",
                  "So einfach ist das.",
                  "Genau so machen wir's.",
                  "Ich werde das mal für dich aufblasen.",
                  "Du sagst vielleicht Technikgelaber dazu.",
                  "Hier sind meine unbescheidenen Worte.",
                  "Junge, du nimmst den Mund vielleicht voll!",
                  "Manche nennen mich bombastisch.",
                  "Ich will nur mal was einwerfen.",
                  "Ich denke, das sind die richtigen Worte.",
                   ],
    'ParadigmShift':["Sieh dich vor! Ich bin ziemlich wechselhaft.",
                     "Bereite dich darauf vor, dass dein Paradigma ausgewechselt wird.",
                     "Das ist doch mal ein interessantes Paradigma.",
                     "Du wirst einfach ausgewechselt werden.",
                     "Ich glaube, jetzt musst du wechseln.",
                     "Dein Wechsel ist geplatzt!",
                     "Du hast in deinem ganzen Leben noch keinen solchen Wechsel erlebt! ",
                     "Ich wechsle dich aus wie nichts.",
                     "Der Wechsel ist perfekt, ob du's glaubst oder nicht.",
                     ],
    'PeckingOrder':["Da lachen ja die Hühner!",
                    "Mit dir habe ich noch ein Hühnchen zu rupfen.",
                    "Ich mach mit dir nicht viel Federlesen.",
                    "Ich werde ganz sicher den Vogel abschießen!",
                    "Du stehst in der Hackordnung ganz unten.",
                    "Lieber einen Vogel in meiner Hand als zehn auf deinem Dach!",
                    "Wir schrägen Vögel müssen zusammenhalten! ",
                    "Warum ich nicht auf jemandem rumhacke, der genauso groß ist wie ich? Nö.",
                    "Eine Krähe hackt der anderen kein Auge aus, dann schon lieber dir!",
                    ],
    'PickPocket': ["Ich möchte mal deine Wertsachen prüfen.",
                   "Guck mal, was ist denn das da drüben?",
                   "Als würde man einem Baby den Schnuller wegnehmen.",
                   "Was für ein Diebstahl!",
                   "Ich halte das mal für dich.",
                   "Behalte meine Hände immer gut im Auge.",
                   "Die Hand ist schneller als das Auge.",
                   "In meinem Ärmel ist gar nichts.",
                   "Die Geschäftsleitung übernimmt keine Verantwortung für verlorene Gegenstände.",
                   "Wer's findet, dem gehörts auch.",
                   "Du wirst überhaupt nichts merken.",
                   "Eins für mich, keins für dich.",
                   "Ich bin so frei.",
                   "Das wirst du nicht mehr brauchen ...",
                   ],
    'PinkSlip': ["Mach nur nicht blau.",
                 "Ist dir kalt? Du bist ganz blau.",
                 "Du wirst dein blaues Wunder erleben.",
                 "Na hoppla, bist du blau?",
                 "Pass nur auf, dass du nicht blau wirst!",
                 "Ich geb's dir mit Brief und Siegel!",
                 "Ich hau dich grün und blau.",
                 "Das hast du doch verbrieft, oder.",
                 "Blau steht dir nicht.",
                 "Hier ist dein blauer Brief, verschwinde hier!",
                 ],
    'PlayHardball': ["Du willst es also darauf anlegen?",
                     "Ich rate dir, dich nicht mit mir anzulegen.",
                     "Härte zeigen!",
                     "Na schlag doch, los!",
                     "Durch dich kann ich doch durchgreifen ...",
                     "Ich schaff hier gleich mal Ordnung.",
                     "Hart, aber gerecht.",
                     "Benimm dich, sonst fliegst du raus.",
                     "Wenn's hart auf hart kommt, verlierst du!",
                     "Wird ganz schön hart für dich!",
                     "Bist du hart im Nehmen?",
                     "Ich geb dir eine harte Nuss zu knacken!",
                    ],
    'PoundKey': ["Höchste Zeit für ein paar Rückrufe.",
                 "Verdrück dich!",
                 "Diese Sache wird dich unter Druck setzen.",
                 "Da will jemand die Preise drücken.",
                 "Ich habe eine Menge Druck zu bieten.",
                 "Jetzt bin ich am Drücker!",
                 "Ich geb nur mal diese Zahl ein.",
                 "Gleich mach ich dir Druck.",
                 "Du hast überhaupt keinen Tastsinn.",
                 "OK, Toon, ich drück dich an die Wand.",
                 ],
    'PowerTie': ["Ich komm später nochmal, du siehst ziemlich kraftlos aus.",
                 "Fertig zum Armdrücken?",
                 "Meine Damen und Herren, es steht unentschieden!",
                 "Du solltest lernen, deine Kräfte richtig zu messen.",
                 "Pass auf, ich nehme Maß!",
                 "Gleich ist das Maß voll!",
                 "Was maßt du dir an!?",
                 "Das gibt eine kräftige Abreibung!",
                 "Kraft meiner Wassersuppe werde ich dich erledigen!",
                 "Ich bin ein Teil von jener Kraft, die das Böse will und das Böse schafft!",
                 ],
    'PowerTrip': ["Pack deine Sachen, wir machen einen kleinen Trip.",
                  "Guter Trip?",
                  "Wie geht's dem Ego?",
                  "Wie war der Trip?",
                  "Lass dich nicht aufhalten!",
                  "Außer Spesen nichts gewesen.",
                  "Warum denn in die Ferne schweifen!",
                  "Besser schlecht gefahren als gut gelaufen. ",
                  "Mein Ego hält das aus.",
                  "Ego ist Ego.",
                  "Mein Ego ist größer als deins!",
                  ],
    'Quake': ["Beben und beben lassen.",
              "Hier bebt eine ganze Menge!",
              "Ich sehe dich in deinen Schuhen erbeben.",
              "Da kommt es schon, und es ist gewaltig!",
              "Das sprengt die Richter-Skala.",
              "Jetzt wird die Erde beben!",
              "He, was zittert da? Du!",
              "Schon mal ein Erdbeben erlebt?",
              "Du bewegst dich auf unsicherem Boden!",
              ],
    'RazzleDazzle': ["Viel Lärm um nichts.",
                     "Heute haun wir auf die Pauke!",
                     "Du kannst schon mal alle zusammentrommeln.",
                     "Ich mache gleich einen riesigen Aufriß!",
                     "Du wirst nach meiner Trommel tanzen!",
                     "Jetzt wird ein Fass aufgemacht.",
                     "Dir wird Hören und Sehen vergehen.",
                     "Wer wird denn hier so ein TamTam machen!",
                     "Willst du das an die große Glocke hängen?",
                     "Klappern gehört zum Handwerk.",
                     "Du wirst mit Pauken und Trompeten durchfallen!",
                     ],
    'RedTape': ["Besser Bürokratie als nie.",
                "Ich werde dich ein wenig aufhalten.",
                "Das geht alles seinen geregelten Gang.",
                "Ein Stempelchen gefällig?",
                "Dein Vorgang kommt in die Ablage P.",
                "Je länger, je lieber.",
                "Was lange währt, wird gut.",
                "Ich werde dich schon beschäftigen.",
                "Versuch nur mal, dich da durchzukämpfen.",
                "Du hast vergessen das Formular auszufüllen.",
                ],
    'ReOrg': ["Dir gefällt nicht, wie ich hier reorganisiert habe?",
              "Ein bisschen Reorganisation muss sein.",
              "Du bist ja gar nicht so schlecht, du musst nur umorganisiert werden.",
              "Gefallen dir meine organisatorischen Fähigkeiten?",
              "Ich dachte mir, ich sollte die Dinge mal anders aussehen lassen.",
              "Du musst dich besser organisieren!",
              "Du siehst ein bisschen desorganisiert aus.",
              "Halt mal still, während ich deine Gedanken reorganisiere. ",
              "Ich warte nur, bis du dich mal ein bisschen organisiert hast.",
              "Du hast doch nichts dagegen, wenn ich nur mal ein bisschen reorganisiere?",
              ],
    'RestrainingOrder': ["Ist ja nur einstweilig. ",
                         "Ich hau dir eine Einstweilige Verfügung um die Ohren!",
                         "Du darfst dich mir nicht mal auf zwei Meter nähern.",
                         "Vielleicht solltest du dich lieber fern halten.",
                         "Man sollte über dich verfügen.",
                         Cogs +" ! Haltet diesen Toon zurück!",
                         "Versuch doch mal, dich zurückzuhalten.",
                         "Ich hoffe, dass ich eine starke Verfügung bin für dich.",
                         "Probier mal, ob du diese Verfügung aufheben kannst!",
                         "Ich verfüge, dass du dich einstweilen zurückhalten sollst!",
                         "Warum fangen wir nicht mit einer Grundausbildung im Zusammenreißen an?"
                         ],
    'Rolodex': ["Deine Karte ist hier irgendwo drin.",
                "Hier ist die Nummer eines Schädlingsbekämpfers.",
                "Ich möchte dir meine Karte geben.",
                "Ich habe deine Nummer immer dabei.",
                "Ich habe alle Informationen über dich.",
                "Organisation ist alles.",
                "Schluss mit der Zettelwirtschaft!",
                "Pass auf, dass du nicht aus meiner Rotationskartei fliegst!",
                "Deine Schutzhülle nützt dir gar nichts.",
                "Kann ich dich so kontaktieren?",
                "Ich möchte sichergehen, dass wir in Verbindung bleiben.",
                ],
    'RubberStamp': ["Ich hinterlasse stets einen guten Eindruck.",
                    "Es ist wichtig, einen festen und gleichmäßigen Druck auszuüben.",
                    "Jedes Mal ein perfekter Abdruck.",
                    "Ich möchte dich abstempeln.",
                    "Du wirst ZURÜCK AN DEN ABSENDER geschickt.",
                    "Du wurdest für UNGÜLTIG erklärt.",
                    "Du wirst per EXPRESS verschickt.",
                    "Ich sorge dafür, dass du meine Mitteilung ERHALTEN wirst.",
                    "Du wirst dich nirgendwo hin verdrücken - erst die NACHNAHME bezahlen.",
                    "Ich brauche eine Antwort - es EILT! ",
                    ],
    'RubOut': ["Hokuspokus, Verschwindibus!",
               "Ich habe das Gefühl, dass du irgendwie weg bist.",
               "Ich habe beschlossen, dich auszulassen.",
               "Ich radiere immer aus, was mir nicht passt.",
               "Ich radiere nur mal diesen kleinen Fehler weg.",
               "Wenn ich will, verschwindet alles Störende.",
               "Ich gern alles schön sauber und ordentlich.",
               "Aus den Augen, aus dem Sinn!",
               "Grad sah ich dich noch, schon bist du weg ... ",
               "Schon wirst du blass und blässer ...",
               "Ich werde das Problem eliminieren.",
               "Ich werde mich mal um deine Problemzonen kümmern.",
               ],
    'Sacked':["Sieht aus, als würdest du entlassen werden.",
              "Und ab dafür.",
              "Du fliegst in hohem Bogen raus.",
              "Nimm deine Papiere und marschiere ab.",
              "Meine Feinde werden entlassen!",
              "Ich halte den Toontown-Rekord im Entlassen.",
              "Du wirst hier nicht mehr gebraucht.",
              "Deine Zeit ist um, du bist entlassen!",
              "Meinem Entlassungsangriff kann keine Verteidigung standhalten.",
              "Wieder einer weniger.",
              ],
    'Schmooze':["Du wirst das gar nicht merken.",
                "Das wird dir gut stehen.",
                "Das hast du dir verdient.",
                "Ich meine das ganz ehrlich.",
                "Mit Schmeicheleien komme ich überall hin.",
                "Ein Lob der Torheit!",
                "Jetzt wird aber richtig dick aufgetragen.",
                "Ich werde mich über deine guten Seiten auslassen.",
                "Dafür sollte man dir ordentlich auf die Schulter klopfen.",
                "Ich werd dir Loblieder singen, dass dir die Ohren klingen.",
                "Ich will dich ja nicht vom Sockel hauen, aber ... ",
                ],
    'Shake': ["Pass auf, ich schüttel gleich mit deinem Kopf!",
              "Bist du schüttelfest?",
              "Das wird eine Schüttel-Tour.",
              "Du wirst durch mein Schüttelsieb fallen.",
              "Muss man dich vor Gebrauch schütteln?",
              "Ich bin der Schüttler vom Dienst.",
              "Höchste Zeit in Deckung zu gehen.",
              "Du scheinst etwas zerschüttelt.",
              "Fertig zum Hände schütteln?",
              "Ich werde dich schütteln, nicht rühren!",
              "Das wird dich ordentlich durchschütteln.",
              "An meiner Macht lass ich nicht schütteln! ",
              ],
    'Shred': ["Ich muss ein paar gefährliche Dinge loswerden.",
              "Ich erhöhe meinen Durchsatz.",
              "Ich glaube, ich werde dich gleich mal entsorgen.",
              "Dadurch werden Beweise vernichtet.",
              "Jetzt kann man nichts mehr beweisen.",
              "Schau mal, ob du dir das wieder zusammensetzen kannst.",
              "Das dürfte dich auf eine angemessene Größe bringen.",
              "Ich werde diese Idee in Stücke reißen.",
              "Wir wollen doch nicht, dass das in falsche Hände gerät.",
              "Wie gewonnen, so zerronnen.",
              "Da fährt dein letztes Schnipselchen Hoffnung dahin!",
              ],
    'Spin': ["Wie wär's mit einer kleinen Redetour?",
             "Das kannst auch du nicht schönreden!",
             "Das wird ganz schön wehtun!",
             "Ich sag's dir mal vor.",
             "Pass auf. Das sind nur schöne Worte.",
             "Meinem Redeschwall ist keiner gewachsen!",
             "Da läuft dir ja die Zunge über ...",
             "Schön, dass du noch sprechen kannst.",
             "Nichts als Worte - aber schön.",
             ],
    'Synergy': ["Ich werde das vor den Ausschuss bringen.",
                "Dein Projekt ist gestrichen worden.",
                "Dein Budget wurde gekürzt.",
                "Wir strukturieren deine Abteilung um.",
                "Ich lasse darüber abstimmen, und du verlierst.",
                "Ich habe gerade die endgültige Zustimmung erhalten.",
                "Ein gutes Team kann sich jedes Problems entledigen.",
                "Ich komme wegen dieser Sache wieder auf dich zurück.",
                "Dann fangen wir mal an. ",
                "Betrachte das als Synergiekrise.",
                ],
    'Tabulate': ["Diese Zahlen ergeben keinen Sinn.",
                 "Nach meiner Rechnung verlierst du.",
                 "Jetzt wird tabula rasa gemacht.",
                 "Deine Rechnung geht nicht auf.",
                 "Bist du für diese Zahlen bereit?",
                 "Jetzt kriegst du die Quittung.",
                 "Zeit für die Endabrechnung.",
                 "Ich bringe die Dinge gern in Ordnung.",
                 "Und der aktuelle Stand ist ...",
                 "Diese Zahlen dürften sich als ziemlich wirksam erweisen.",
                 ],
    'TeeOff': ["Du bist noch nicht bereit.",
               "Jetzt geht's los!",
               "Jetzt fang ich erst mal richtig an.",
               "Hol schon mal den Wagen, Harry.",
               "Nichts überstürzen!",
               "Sieben auf einen Schlag!",
               "Der Sieg ist gewiss.",
               "Du stehst mir im Weg.",
               "Pass auf, wie ich Anlauf nehme ...",
               "Auch der längste Weg beginnt mit dem ersten Schritt.",
               "Aller Anfang ist schwer.",
               "Das ist der Anfang vom Ende.",
               ],
    'Tremor': ["Hast du das gespürt?",
               "Du hast doch keine Angst vor einem kleinen Zittern, oder?",
               "Das Zittern ist erst der Anfang.",
               "Du siehst zittrig aus.",
               "Ein kleines Beben hat noch niemandem geschadet.",
               "Bist du bereit zu zittern und zu zagen?",
               "Was ist los? Du siehst erschüttert aus.",
               "Das schaudert's dich, was?",
               "Was zitterst du vor Furcht?",
               ],
    'Watercooler': ["Das sollte dich abkühlen.",
                    "Ist das nicht erfrischend?",
                    "Das ist Wasser auf meine Mühlen.",
                    "Wasser gepredigt und Wein getrunken.",
                    "Mach keine Panik, das ist doch nur Mineralwasser.",
                    "Keine Angst, es ist gereinigt.",
                    "Aha, noch ein zufriedener Kunde.",
                    "Ich denke, dein Plan wird ins Wasser fallen.",
                    "Ich hoffe, deine Farben laufen nicht weg.",
                    "Kleine Abkühlung gefällig?",
                    "Das wäscht sich aus!",
                    "Die nächste Runde zahlst du.",
                    ],
    'Withdrawal': ["Ich glaube, du hast überzogen.",
                   "Ich hoffe, dass dein Kontostand hierfür ausreicht.",
                   "Das geht auf mein Konto.",
                   "Dein Konto ist gesperrt.",
                   "Du wirst bald was einzahlen müssen.",
                   "Du hast einen wirtschaftlichen Zusammenbruch erlitten.",
                   "Ich glaube, du steckst in der Krise.",
                   "Deine Finanzen sind abgestürzt.",
                   "Ich sehe eine absolute Talfahrt voraus.",
                   "Das Glück wendet sich.",
                   ],
    'WriteOff': ["Lass mich deine Verluste vergrößern.",
                 "Wir wollen aus einem schlechten Deal das Beste machen.",
                 "Es ist Zeit, die Bücher abzuschließen.",
                 "Das wird sich in deinen Büchern nicht gut ausnehmen.",
                 "Ich hoffe auf Dividenden.",
                 "Du musst deine Verluste nachweisen.",
                 "Einen Bonus kannst du vergessen.",
                 "Ich werde deine Zahlen ein wenig hin und her schieben.",
                 "Du wirst ein paar Verluste erleiden.",
                 "Das wird deinen Gewinn beeinträchtigen.",
                 ],
    }

# DistributedBuilding.py
BuildingWaitingForVictors = "Auf andere Spieler warten ...",

# Elevator.py
ElevatorHopOff = "Aussteigen"

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = ", AG "
CogsIncModifier = "%s"+ CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Poch-poch."
DoorWhosThere = "Wer da?"
DoorWhoAppendix = " wer?"
DoorNametag = "Tür"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "Du brauchst Gags! Sprich mal mit Einweiser Eddie!"
FADoorCodes_DEFEAT_FLUNKY_HQ = "Komm wieder her, wenn du den Kriecher vertreiben hast!"
FADoorCodes_TALK_TO_HQ = "Hol dir deine Belohnung bei Mitarbeiter Harry!"
FADoorCodes_WRONG_DOOR_HQ = "Falsche Tür! Nimm die andere Tür zum Spielplatz!"
FADoorCodes_GO_TO_PLAYGROUND = "Falsch! Du musst doch zum Spielplatz!"
FADoorCodes_DEFEAT_FLUNKY_TOM = "Geh zu diesem Kriecher hin und schlage ihn!"
FADoorCodes_TALK_TO_HQ_TOM = "Hol dir deine Belohnung aus der Toontown-Zentrale!"
FADoorCodes_SUIT_APPROACHING = None  # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "Pass auf! Da ist ein BOT drin!"
FADoorCodes_DISGUISE_INCOMPLETE = "Man wird dich schnappen, wenn du da als Toon reingehst! Du musst erst deine Verkleidung als Bot vervollständigen!\n\nStelle deine Bot-Verkleidung aus Teilen aus der Fabrik zusammen."

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Leiter",
    "Leiter ist heute geschlossen."],

    ["Albert",
    "Albert hier jemand rum?"],

    ["Andre",
    "Andre Tür, hier bist du falsch."],

    ["Anke",
    "Anke-tten schützt vor Fahrraddiebstahl."],

    ["Anna",
    "Anna-nas essen macht Spaß!"],

    ["Armin",
    "Armin-Arm gehen sie durch den Park."],

    ["Axel",
    "Axel Schweiß stinkt."],

    ["Basti",
    "Na, Basti Hose?"],

    ["Benno",
    "Wie soll dein Lehrer denn das Benno-ten?"],

    ["Ben",
    "Ben-zin wird auch immer teurer."],

    ["Boris",
    "Boris mir heiß!!"],

    ["Britt",
    "Gib mir mal deinen Britt-Stift zum Kleben!"],

    ["Clair",
    "Mein Bruder ist in die Clair-Grube gefallen."],

    ["Cindy",
    "Oh, Perlen - Cindy echt?"],

    ["Connie",
    "Habt ihr auch Connie-feren vorm Haus?"],

    ["Cora",
    "Cora-llenriffe gibt's in der Südsee."],

    ["Diana",
    "Ich war das nicht - Diana-re wars."],

    ["Dieter",
    "Dieter-miten zerfressen ganze Häuser."],

    ["Dirk",
    "Dirk-laubt sowieso keiner mehr was."],

    ["Ellen",
    "Ellen-bogenschützer sind gut für Skater."],

    ["Erich",
    "Erichten wir hier wollen wir unser Lager."],

    ["Ernst",
    "Ernst-haft, ich heiße wirklich "+ Flippy +  "."],

    ["Duck",
    Donald +" Duck-uckst du, was!"],

    ["Max",
    "Maxtu noch was essen?"],

    ["Ernest",
    "Ernest noch ins Bett!!"],

    ["Amos",
    "Amos-kito hat mich gestochen."],

    ["Alma",
    "Almaufwärts sieht's noch schöner aus."],

    ["Ernie",
    "Ernie-ste laut und heftig."],

    ["Esra",
    "Esra-icht nicht, was ich eingekauft habe."],

    ["Frank",
    "Du musst den Brief noch Frank-ieren."],

    ["Franz",
    "Franz-ösisch kann ich auch!"],

    ["Gerrit",
    "Er Gerrit dazwischen."],

    ["Ida",
    "W-Idas denn!"],

    ["Gitta",
    "Gitta-stäbe biegt man nicht so leicht auf."],

    ["Holger",
    "Ich Holger-ne ein Eis für euch."],

    ["Kaviar",
    "Kaviar keene Zähne mehr."],

    ["Kasimir",
    "Kasimir alle ausjeschlagen."],

    ["Inga",
    "Die Luftpumpe ist grad Inga-brauch."],

    ["Ingolf",
    "Ingolf bin ich ganz gut."],

    ["Iris",
    "Iris schlecht vom Essen."],

    ["Isolde",
    "Isolde baden, bin ganz dreckig."],

    ["Jan",
    "Janeinweißnicht."],

    ["Joe Kurt",
    "Joe-Kurt ess ich für mein Leben gern!"],

    ["Lasse",
    "Lasse reinfalln!"],

    ["Karl",
    "Muss mal auf den Karl-ender schauen."],

    ["Keith",
    "Kies kommt aus der Keith-Grube."],

    ["Thea",
    "Thea-terkarten sind ausverkauft."],

    ["Knut",
    "Knut-schen verboten!"],

    ["Lars",
    "Lars gut sein, ich hol's mir selber."],

    ["Lotte",
    "Lotte-rielose gibt's am Kiosk."],

    ["Marga",
    "Marga-rine ist keine mehr da."],

    ["Marina",
    "Machst du noch die Marina-de für das Fleisch?"],

    ["Martha",
    "Wenn du frech wirst, kommst du an den Martha-Pfahl!"],

    ["Moni",
    "Wie lange sitzt du schon vor dem Moni-tor?"],

    ["Naomi",
    "Naomi, müde?"],

    ["Neal",
    "Fahr doch mit ins Neal-Delta!"],

    ["Nick",
    "Papa las Zeitung und Nick-te ein."],

    ["Paul",
    "Wo ist denn auf diese Baustelle die Paul-eitung?"],

    ["Pepe",
    "Vorsicht, da sind Pepe-roni dran!"],

    ["Peter",
    "Peter-silie wächst im Garten."],

    ["Polly",
    "Polly-zei! Hilfe!"],

    ["Rainer",
    "Rainer Zufall, dass wir uns treffen."],

    ["Rosi",
    "Rosi-nen ess ich nicht."],

    ["Rudi",
    "Rudi-ch erst mal aus!"],

    ["Ruth",
    "Ruth ruth sich auch aus."],

    ["Sarah",
    "Er flog in den Schlamm und Sarah-benschwarz aus."],

    ["Steve",
    "Ist das dein richtiger Vater oder dein Steve-Vater?"],

    ["Sue",
    "Kommste mit in den Sue-permarkt?"],

    ["Theo",
    "Mein Theo-dorant wirkt nicht mehr!"],

    ["Tom",
    "Schmeiß nicht mit Tom-aten."],

    ["Till",
    "Till-siter schmeckt lecker, aber stinkt."],

    ["Vince",
    "So ein Vince-ling!"],

    ["Du",
    "Du - wer! Ist hier etwa jemand?"],

    ["Walter",
    "Walter-beiter arbeiten im Wald."],

    ["Wanda",
    "Da geht's steil runter, bleib lieber auf dem Wanda-Weg."],

    ["Wayne",
    "Na und, Wayne stört's?"],

    ["Werner",
    "Werner-vt hier?"],

    ["Willi",
    "Und bist du nicht Willi-g ..."],

    ["Wotan",
    "Wotan-nen wachsen, fallen Tannenzapfen."],

    ["Evi",
    "Evi eklig!!"],

    ["Izmir",
    "Izmir schlecht!"],

    ["Mitsubishi!",
    "Gesundheit!"],

    ["Komma",
    "Komma schnell rein!"],

    ["Fenster",
    "Fenster Lehrer merkt, kriegste Ärger!"],

    ["Eintritt",
    "Eintrittel davon reicht."],

    ["Purzel",
    "Du benimmst dich wie ein Elefant im Purzelanladen."],

    ["Tank",
    "Bitte schön."],

    ["Reh",
    "Iss schnell dein Erbsenpü-Reh."],

    ["Pizza",
    "Ich hab schon pizzahlt."],

    ["Denken",
    "Denken ich doch?"],

    ["Schaf",
    "Mann, das ist aber schaf gewürzt!"],

    ["Fahrrad",
    "Fahrrad ich dir nicht."],

    ["Lamm",
    "Lammentier hier nicht rum!"],

    ["Zunge",
    "Zunge, komm bald wieder ..."],

    ["Q",
    "Du blöde Q!"],

    ["Chris",
    "Chris du nicht mit, wer ich bin?"],

    ["Acht",
    "Achtung, ich komm jetzt rein."],

    ["Eishockey",
    "Eishockey mit dir?"],

    ["Kanufahrn",
    "Ich hab nichts, getrunken, ich kanufahrn."],

    ["Wirsing",
    "Machs gut und Auf Wirsing."],

    ["X",
    "Xtreme Temperaturen habt ihr hier."],

    ["Haydn",
    "Das macht `nen Haydnspaß."],

    ["Ente",
    "Enteweder - oder."],

    ["Feder",
    "Wenn die Feder mit ihren Söhnen ..."],

    ["Arm",
    "Lieber arm dran als Arm ab."],

    ["Nachname",
    "Schick das Paket per Nachname."],

    ["Gans",
    "Du bist gans schön frech!"],

    ["Ekel",
    "Schon mal so'n fetten Blutekel gesehen?"],

    ["Halligen",
    "Tolles Auto mit Halligen-Scheinwerfern!"],

    ["Schwein",
    "Schwein' ja garnicht mehr."],

    ["Fass",
    "Fass mich bloß nicht an!"],

    ["Welke Blume",
    "Welke Blume hättest du denn gern?"],

    ["Agatha",
    "Ich hab uns was schönes Agathat."],

    ["Ungarn",
    "Ich geb dir mein Fahrrad nur Ungarn."],

    ["Polen",
    "Du musst das Gerät umpolen."],

    ["Kanada ",
    "Tut mir Leid, Kanada."],

    ["Mrs.",
    "Mrs. Sippi und Miss Ouri"],

    ["Rhein",
    "Das war vielleicht ein Rheinfall!"],
]

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "Hi, %!",
        "Huhu %, schön dich zu sehen.",
        "Ich freue mich, dass du heute da bist!",
        "Na hallo, %.",
        ]

SharedChatterComments = [
        "Das ist ein toller Name, %.",
        "Dein Name gefällt mir.",
        "Nimm dich in Acht vor den "+ Cogs +  ".",
        "Ach da kommt ja der Toon-Express!",
        "Ich muss ein Spiel der Toon-Express Spiel spielen machen, um ein paar Torten zu bekommen!",
        "Manchmal spiele ich ein Spiel der Toon-Express Spiele, nur um die Obsttorte zu essen!",
        "Puh, ich hab grad ein paar "+ Cogs +  " aufgehalten. Ich muss mich ausruhen!",
        "Ihh, manche von diesen "+ Cogs +  " sind ganz schön groß!",
        "Du siehst aus, als würde es dir Spaß machen.",
        "Oh Mann, ich mach mir grad `nen schönen Tag.",
        "Gefällt mir, was du da anhast.",
        "Ich glaube, ich gehe heute Nachmittag angeln.",
        "Viel Spaß in meiner Gegend.",
        "Ich hoffe, du genießt deinen Aufenthalt in Toontown.",
        "Wie ich höre, schneit es im Brrr.",
        "Bist du heute schon mit dem Toon-Express gefahren?",
        "Ich treffe gern neue Leute.",
        "Wow, da sind ja massenhaft "+ Cogs +  " im Brrr.",
        "Ich spiele gern Fangen. Du auch?",
        "Spiele beim Toon-Express machen Spaß.",
        "Ich bring gern andere zum Lachen.",
        "Es macht mir Spaß meinen Freunden zu helfen.",
        "Ähem, hast du dich verlaufen? Denk dran, dein Stadtplan befindet sich in deinem Sticker-Buch.",
        "Versuche, dich nicht in der Bürokratie der "+ Cogs +  " zu verheddern.",
        "Ich habe gehört, "+ Daisy +  " hat ein paar neue Blumen in ihren Garten gepflanzt.",
        "Wenn du die Taste 'Bild-Hoch' drückst, kannst du nach oben schauen!",
        "Wenn du bei der Übernahme von Bot-Gebäuden hilfst, kannst du dir einen Bronze-Stern verdienen!",
        "Wenn du die Tab-Taste drückst, kannst du verschiedene Ansichten deiner Umgebung sehen!",
        "Wenn du die Strg-Taste drückst, kannst du springen!",
        ]

SharedChatterGoodbyes = [
        "Ich muss jetzt weg, tschüss!",
        "Ich werde wohl mal ein Toon-Express Spiel spielen gehen.",
        "Also mach's gut bis später, %!",
        "Ich mach mich mal lieber an die Arbeit, diese "+ Cogs +  " zu stoppen.",
        "Jetzt muss ich mich mal in Bewegung setzen.",
        "Entschuldige, muss leider weg.",
        "Auf Wiedersehen.",
        "Bis später, %!",
        "Ich werde jetzt mal Napfkuchen werfen üben.",
        "Ich werde mich einer Gruppe anschließen und ein paar "+ Cogs +  " stoppen.",
        "War schön, dass ich dich heute getroffen habe, %.",
        "Ich hab heute viel zu tun. Da fang ich mal lieber an.",
        ]

# Lines specific to each character.
# If a talking char is mentioned, it cant be shared among them all

MickeyChatter = (
        [ # Greetings specific to Mickey
        "Willkommen in Toontown Mitte.",
        "Hi, ich heiße "+ Mickey +  ". Und du?",
        ],
        [ # Comments
        "Hey, hast du "+ Donald +  " gesehen?",
        "Ich seh mir mal an, wie der Nebel bei "+ Donald +  "s Dock hereinzieht.",
        "Wenn du meinen Kumpel "+ Goofy +  " siehst, grüß ihn von mir.",
        "Ich habe gehört "+ Daisy +  " hat ein paar neue Blumen in ihren Garten gepflanzt.",
        ],
        [ # Goodbyes
        "Ich gehe zum Melodienland, " + Minnie + " besuchen!",
        "Mensch, ich komme zu spät zu meiner Verabredung mit "+ Minnie +  "!",
        "Scheint Zeit zu sein für "+ Pluto +  "s Dinner.",
        "Ich denke, ich werde bei "+ Donald +  "s Dock schwimmen gehen.",
        "Es ist Zeit für ein Nickerchen. Ich gehe ins Traumland.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Willkommen im Melodienland.",
        "Hi, ich heiße "+ Minnie +  ". Und du?",
        ],
        [ # Comments
        "Der Klang der Musik hallt von den Bergen wider!",
        "Du musst unbedingt mal auf dem großen Plattenteller-Karussell fahren!",
        "Du hast ein cooles Outfit, %.",
        "Hey, hast du "+ Mickey +  " gesehen?",
        "Wenn du meinen Freund  "+ Goofy +  " siehst, Gruß ihn von mir.",
        "Wow, da sind massenhaft "+ Cogs +  " in der Nähe von "+ Donald +  "s Traumland.",
        "Ich habe gehört, dass es bei "+ Donald +  "s Dock sehr neblig sein soll.",
        "Du musst unbedingt das Labyrinth in "+ Daisy +  "s Gärten ausprobieren.",
        "Ich glaube, ich geh mal ein paar Melodien einfangen.",
        "Hey %, schau mal da drüben.",
        "Ich liebe den Klang der Musik.",
        "Ich wette, du hast nicht gewusst, dass Melodienland auch manchmal Ton-Town genannt wird! Hihi!",
        "Ich spiele sehr gern das Pantomime-Spiel. Du auch?",
        "Ich bringe gern andere zum Kichern.",
        "Junge, den ganzen Tag in Pumps herumlaufen geht vielleicht auf die Füße!",
        "Hübsches Oberteil, %.",
        "Ist das da auf dem Boden ein Jelly Bean?",
        ],
        [ # Goodbyes
        "Mensch, ich komme zu spät zu meiner Verabredung mit "+ Mickey +  "!",
        "Scheint Zeit zu sein für "+ Pluto +  "s Dinner.",
        "Es ist Zeit für ein Nickerchen. Ich gehe ins Traumland.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Willkommen in "+ Daisy +  "s Gärten.",
        "Hi, ich heiße "+ Goofy +  ". Und du?",
        "Möönsch, schön dich zu sehen %!",
        ],
        [ # Comments
        "Junge, in diesem Gartenlabyrinth kann man sich ganz schön leicht verlaufen! ",
        "Probier auf jeden Fall mal das Labyrinth hier aus. ",
        "Ich habe "+ Daisy +  " den ganzen Tag nicht gesehen.",
        "Ich frage mich, wo "+ Daisy +  " ist.",
        "Hey, hast du "+ Donald +  " gesehen?",
        "Wenn du meinen Freund "+ Mickey +  " siehst, grüß ihn von mir.",
        "Oje! Ich hab vergessen "+ Mickey +  " sein Frühstück hinzustellen!",
        "Möönsch da sind ja wirklich massenhaft "+ Cogs +  " in der Nähe von "+ Donald +  "s Dock.",
        "Es sieht aus, als ob "+ Daisy +  " ein paar neue Blumen in ihrem Garten gepflanzt hat.",
        "In der Brrr-Zweigstelle meines Gag-Ladens gibt es Hypno-Brillen im Angebot für nur 1 Jelly Bean!",
        "Goofys Gag-Läden bieten die besten Witze, Tricks und Zwerchfellkitzler von ganz Toontown!",
        "In Goofys Gag-Läden bringt jede Torte im Gesicht garantiert einen Lacher, oder du bekommst deine Jelly Beans zurück!"
        ],
        [ # Goodbyes
        "Ich gehe zum Melodienland, um " + Minnie + " zu besuchen!",
        "Mensch, ich komme zu spät zu meinem Spiel mit "+ Donald +  "!",
        "Ich glaube, ich werde bei "+ Donald +  "s Dock schwimmen gehen.",
        "Es ist Zeit für ein Nickerchen. Ich gehe ins Traumland.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Willkommen im Traumland.",
        "Hi, ich heiße "+ Donald +  ". Und du?",
        ],
        [ # Comments
        "Manchmal läuft es mir hier kalt den Rücken hinunter.",
        "Probier auf jeden Fall das Labyrinth in "+ Daisy +  "s Gärten aus.",
        "Junge, geht's mir heute gut.",
        "Hey, hast du "+ Mickey +  " gesehen?",
        "Wenn du meinen Kumpel "+ Goofy +  " siehst, grüß ihn von mir.",
        "Ich werde wohl heute Nachmittag angeln gehen.",
        "Wow, da sind massenhaft "+ Cogs +  " bei "+ Donald +  "s Dock.",
        "Hey, habe ich dich nicht mal bei "+ Donald +  "s Dock mit dem Boot mitgenommen?",
        "Ich habe "+ Daisy +  " den ganzen Tag nicht gesehen.",
        "Ich habe gehört, dass "+ Daisy +  " ein paar neue Blumen in ihren Garten gepflanzt hat.",
        "Quak.",
        ],
        [ # Goodbyes
        "Ich gehe zum Melodienland, um " + Minnie + " zu besuchen!",
        "Mensch, ich komme zu spät zu meiner Verabredung mit "+ Daisy +  "!",
        "Ich glaube, ich werde bei meinem Dock schwimmen gehen.",
        "Ich glaube, ich kurve ein bisschen mit meinem Boot bei meinem Dock rum.",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)


# FriendsListPanel.py
FriendsListPanelNewFriend = "Neuer Freund"
FriendsListPanelSecrets = "Geheimnisse"
FriendsListPanelOnlineFriends = "FREUNDE\nONLINE"
FriendsListPanelAllFriends = "ALLE\nFREUNDE"
FriendsListPanelIgnoredFriends = "IGNORIERTE\nTOONS"
FriendsListPanelPets = "NAHE\nHAUSTIERE"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Du kannst leider nicht weitergehen, weil der Download vom %(phase)s erst zu %(percent)s%% abgeschlossen ist.\n\nBitte versuch es später noch einmal."

# TeaserPanel.py
TeaserTop = "Leider ist das im Rahmen des Test-Zugangs nicht möglich.\nWenn du jetzt abonnierst, kannst du diese coolen Features nutzen:"
TeaserOtherHoods = "Besuche alle sechs einzigartigen Stadtteile!"
TeaserTypeAName = "Nimm teil an toontastischen Wettbewerben!"
TeaserSixToons = "Baue dir mit einem einzigen Account bis zu sechs Toons!"
TeaserOtherGags = "Erwirb sechs Fähigkeitsstufen für sechs verschiedene Gag-Tracks!"
TeaserClothing = "Entwirf spezielle Kleidungsstücke für\ndeinen ganz persönlichen Toon!"
TeaserFurniture = "Kaufe Möbelstücke und richte damit dein Haus ein!"
TeaserCogHQ = "Dringe heimlich in gefährliche von\nBots beherrschte Bereiche vor!"
TeaserSecretChat = "Tausche mit Freunden Geheimnisse aus,\ndamit du mit ihnen online chatten kannst!"
TeaserCardsAndPosters = "Als offizieller Einwohner erhältst du den Toontown Willkommensbrief\nmit einem coolen Bot-Poster und schicken Toontown Aufklebern!"
TeaserHolidays = "Nimm an tollen Events der Stadt teil!"
TeaserQuests = "Löse Hunderte von Toon-Aufgaben, um Toontown mit zu retten!"
TeaserEmotions = "Kaufe Emotionen, damit dein Toon mehr Ausdruck bekommt!"
TeaserMinigames = "Spiele alle 8 Minigames!"
TeaserSubscribe = "Jetzt abonnieren"
TeaserContinue = "Probezeit fortsetzen"

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "%s wird heruntergeladen "
DownloadWatcherInitializing = "Download wird vorbereitet ..."

# Launcher.py
LauncherPhaseNames = {
    0   : " Vorbereitung",
    3   : " Toon Kreieren",
    3.5 : " Anleitung",
    4   : " Spielplatz",
    5   : " Straße",
    5.5 : " Grundstück",
    6   : " Viertel I",
    7   : Cog + "-Gebäude",
    8   : " Viertel II",
    9   : " Bot-Hauptquartier",
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)s (%(current)s von %(total)s)"
LauncherStartingMessage = "Disneys Toontown Online wird gestartet ... "
LauncherDownloadFile = "Update für "+ LauncherProgress + " wird heruntergeladen ..."
LauncherDownloadFileBytes = "Update für "+ LauncherProgress + " wird heruntergeladen: %(bytes)s"
LauncherDownloadFilePercent = "Update für "+ LauncherProgress + " wird heruntergeladen: %(percent)s%%"
LauncherDecompressingFile = "Update für "+ LauncherProgress + " wird entkomprimiert ..."
LauncherDecompressingPercent = "Update für "+ LauncherProgress + " wird entkomprimiert: %(percent)s%%"
LauncherExtractingFile = "Update für "+ LauncherProgress + " wir extrahiert ..."
LauncherExtractingPercent = "Update für "+ LauncherProgress + " wird extrahiert: %(percent)s%%"
LauncherPatchingFile = "Update für "+ LauncherProgress + " wird implementiert ..."
LauncherPatchingPercent = "Update für "+ LauncherProgress + " wird implementiert: %(percent)s%%"
LauncherConnectProxyAttempt = "Verbindung zu Toontown: %s (Proxy: %s) Versuch: %s"
LauncherConnectAttempt = "Verbindung zu Toontown: %s Versuch %s"
LauncherDownloadServerFileList = "Update Toontown läuft ..."
LauncherCreatingDownloadDb = "Update Toontown läuft ..."
LauncherDownloadClientFileList = "UpdateToontown läuft ..."
LauncherFinishedDownloadDb = "Update Toontown läuft ... "
LauncherStartingToontown = "Toontown wird gestartet ..."
LauncherRecoverFiles = "Update Toontown läuft. Dateien werden wiederhergestellt ..."
LauncherCheckUpdates = "Updates für" + LauncherProgress
LauncherVerifyPhase = "Update Toontown läuft ..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Toon\nkreieren"
AvatarChoicePlayThisToon = "Toon\neinsetzen"
AvatarChoiceSubscribersOnly = " Jetzt\n\n\n\n\nabonnieren!" 
AvatarChoiceDelete = "Löschen"
AvatarChoiceDeleteConfirm = "Hiermit wird %s für immer gelöscht."
AvatarChoiceNameRejected = "Name\nabgewiesen"
AvatarChoiceNameApproved = "Name\nbestätigt!"
AvatarChoiceNameReview = "Wird\ngeprüft"
AvatarChoiceNameYourToon = "Gib\ndeinem Toon einen Namen!"
AvatarChoiceDeletePasswordText = "Achtung! Damit wird %s für immer gelöscht. Gib dein Passwort ein um diesen Toon zu löschen."
AvatarChoiceDeleteConfirmText = "Achtung! Damit wird %(name)s für immer gelöscht. Wenn du sicher bist, dass du dies tun willst, gib \"%(confirm)s\" ein und klicke auf OK."
AvatarChoiceDeleteConfirmUserTypes = "Löschen"
AvatarChoiceDeletePasswordTitle = "Toon löschen?"
AvatarChoicePassword = "Passwort"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "Das Passwort scheint nicht richtig zu sein. Gib dein Passwort ein um diesen Toon zu löschen."
AvatarChoiceDeleteWrongConfirm = "Du hast nicht das Richtige eingegeben. Um %(name)s zu löschen gib \"%(confirm)s\" ein und klicke auf OK. Die Anführungszeichen nicht tippen. Klicke auf Abbrechen, wenn du es dir anders überlegt hast."

# AvatarChooser.py
AvatarChooserPickAToon = "Such dir einen Toon zum Spielen aus"
AvatarChooserQuit = lQuit

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Bitte Kundendienst anrufen unter %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nWenn du Hilfe brauchst, ruf bitte den Kundendienst an unter %s."
TTAccountIntractibleError = "Es ist ein Fehler aufgetreten."

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Jan.', 'Febr.', 'März', 'Apr.', 'Mai', 'Juni',
                          'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.',]
DateOfBirthEntryDefaultLabel = "Geburtsdatum"


# AchievePage.py
AchievePageTitle = "Erfolge\n(Demnächst)"

# PhotoPage.py
PhotoPageTitle = "Foto\n(Demnächst)"

# BuildingPage.py
BuildingPageTitle = "Gebäude\n(Demnächst)"

# InventoryPage.py
InventoryPageTitle = "Gags"
InventoryPageDeleteTitle = "GAGS LÖSCHEN"
InventoryPageTrackFull = "Du hast alle Gags im Ablauf %s."
InventoryPagePluralPoints = "Du bekommst einen neuen %(trackName)s-Gag, \nwenn du noch %(numPoints)s\n%(trackName)s-Punkte machst."
InventoryPageSinglePoint = "Du bekommst einen neuen\n%(trackName)s-Gag, wenn du noch\n%(numPoints)s %(trackName)s-Punkte machst."
InventoryPageNoAccess = "Du hast noch keinen Zugang zu Ablauf %s."

# NPCFriendPage.py
NPCFriendPageTitle = "SOS Toons"

# NPCFriendPanel.py
NPCFriendPanelRemaining = "Bleiben %s"

# MapPage.py
MapPageTitle = "Stadtplan"
MapPageBackToPlayground = "Zurück zum Spielplatz"
MapPageBackToCogHQ = "Zurück zum Bot-Hauptquartier"
MapPageGoHome = "Nach Hause"
# hood name, street name
MapPageYouAreHere = "Du bist in: %s\n%s"
MapPageYouAreAtHome = "Du bist auf\ndeinem Grundstück"
MapPageYouAreAtSomeonesHome = "Du bist auf dem Grundstück von %s "
MapPageGoTo = "Gehe zu\n%s"

# OptionsPage.py
OptionsPageTitle = "Optionen"
OptionsPagePurchase = "Jetzt abonnieren!"
OptionsPageLogout = "Logout"
OptionsPageExitToontown = "Toontown verlassen"
OptionsPageMusicOnLabel = "Musik an."
OptionsPageMusicOffLabel = "Musik aus."
OptionsPageSFXOnLabel = "Soundeffekte an."
OptionsPageSFXOffLabel = "Soundeffekte aus."
OptionsPageFriendsEnabledLabel = "Anfragen neuer Freunde akzeptieren."
OptionsPageFriendsDisabledLabel = "Anfragen neuer Freunde nicht akzeptieren."
OptionsPageSpeedChatStyleLabel = "Schnell-Chat-Farbe"
OptionsPageDisplayWindowed = "Im Fenster"
OptionsPageSelect = "Auswählen"
OptionsPageToggleOn = "Einschalten"
OptionsPageToggleOff = "Ausschalten"
OptionsPageChange = "Wechseln"
OptionsPageDisplaySettings = "Bildschirm: %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Bildschirm: %(screensize)s"
OptionsPageExitConfirm = "Toontown verlassen?"

DisplaySettingsTitle = "Anzeigeeinstellungen"
DisplaySettingsIntro = "Mit den folgenden Einstellungen kannst du die Darstellung von Toontown auf deinem Computer konfigurieren. Wenn bei dir keine Probleme auftreten, müssen sie wahrscheinlich nicht geändert werden."
DisplaySettingsIntroSimple = "Du kannst die Bildschirmauflösung auf einen höheren Wert einstellen, damit Text und Bild in Toontown deutlicher dargestellt werden. Bei manchen Grafikkarten kann dies aber dazu führen, dass das Spiel nicht so gut läuft oder überhaupt nicht funktioniert."

DisplaySettingsApi = "Grafik-API:"
DisplaySettingsResolution = "Auflösung:"
DisplaySettingsWindowed = "In einem Fenster"
DisplaySettingsFullscreen = "Ganzer Bildschirm"
DisplaySettingsApply = "Verwenden"
DisplaySettingsCancel = lCancel
DisplaySettingsApplyWarning = "Wenn du OK drückst, ändern sich die Einstellungen für die Anzeige. Wenn die neue Konfiguration für deinen Computer nicht geeignet ist, kehrt die Anzeige nach %s Sekunden zur ursprünglichen Konfiguration zurück."
DisplaySettingsAccept = "Drücke OK, um die neuen Einstellungen zu behalten, oder Abbrechen, um sie rückgängig zu machen. Wenn du gar nichts tust, gehen die Einstellungen nach %s Sekunden automatisch zurück."
DisplaySettingsRevertUser = "Deine vorherigen Anzeigeeinstellungen wurden wiederhergestellt."
DisplaySettingsRevertFailed = "Die gewählten Anzeigeeinstellungen funktionieren auf deinem Computer nicht. Deine vorherigen Anzeigeeinstellungen wurden wiederhergestellt."


# TrackPage.py
TrackPageTitle = "Gag-Ablauf Training"
TrackPageShortTitle = "Gag-Training"
TrackPageSubtitle = "Löse Toon-Aufgaben um zu lernen, wie man neue Gags einsetzt!"
TrackPageTraining = "Du übst das Einsetzen von %s Gags.\nWenn du alle 16 Aufgaben bewältigst, wirst du\nin der Lage sein, %s Gags im Kampf einzusetzen."
TrackPageClear = "Du übst im Moment keinen Gag-Typ."
TrackPageFilmTitle = "%s\nTraining\nFilm"
TrackPageDone = "ENDE"

# QuestPage.py
QuestPageToonTasks = "Toon-Aufgaben"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageDelivery = "%s\nTo: %s\n  %s\n  %s\n  %s\n\nFrom: %s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageVisit = "%s %s\n  %s\n  %s\n  %s\n\nFrom: %s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName
# Choose between trackA and trackB.
#
# To choose, go see:
#   Flippy
#   Town Hall
#   Playground
#   Toontown Central
#QuestPageTrackChoice = "%s\n\nTo choose, go see:\n  %s\n  %s\n  %s\n  %s"
# questName, npcName, buildingName, streetName, locationName
QuestPageChoose = "Wählen"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = "Mitarbeiter in der Zentrale"
QuestPosterHQBuildingName = "Toontown-Zentrale"
QuestPosterHQStreetName = "In irgendeiner Straße"
QuestPosterHQLocationName = "In irgendeinem Viertel"

QuestPosterTailor = "Schneider"
QuestPosterTailorBuildingName = "Bekleidungsgeschäft"
QuestPosterTailorStreetName = "Irgendwo auf dem Spielplatz"
QuestPosterTailorLocationName = "In irgendeinem Viertel"
QuestPosterPlayground = "Auf dem Spielplatz"
QuestPosterAtHome = "Bei deinem Haus"
QuestPosterInHome = "In deinem Haus"
QuestPosterOnPhone = "An deinem Telefon"
QuestPosterEstate = "Auf deinem Grundstück"
QuestPosterAnywhere = "Irgendwo in den\nStraßen der Stadt"
QuestPosterAuxTo = "nach:"
QuestPosterAuxFrom = "von:"
QuestPosterAuxFor = "für:"
QuestPosterAuxOr = "oder:"
QuestPosterAuxReturnTo = "Zurückkehren\nzu:"
QuestPosterFun = "Nur so zum Spaß!"
QuestPosterFishing = "ANGELN GEHEN"
QuestPosterComplete = "Komplett"

# ShardPage.py
ShardPageTitle = "Bezirke"
ShardPageHelpIntro = "Jeder Bezirk ist ein Abbild der Toontown-Welt."
ShardPageHelpWhere = "Du bist zurzeit im Bezirk \"%s\"."
ShardPageHelpWelcomeValley = "Du bist zurzeit im Bezirk 'Willkommens-Tal' in \"%s\"."
ShardPageHelpMove = "Um zu einem anderen Bezirk zu kommen, klicke auf seinen Namen."

ShardPagePopulationTotal = "Gesamtbevölkerung Toontown:\n%d"
ShardPageScrollTitle = "Bezirk Bevölkerungszahl"

# SuitPage.py
SuitPageTitle = "Bot-Galerie"
SuitPageMystery = "???"
SuitPageQuota = "%s von %s"
SuitPageCogRadar = "%s anwesend"
SuitPageBuildingRadarS = "%s Gebäude"
SuitPageBuildingRadarP = "%s Gebäude"

# DisguisePage.py
DisguisePageTitle = "Bot-Verkleidung"
DisguisePageMeritAlert = "Bereit zur\nBeförderung!"
DisguisePageCogLevel = "Level %s"
DisguisePageMeritFull = "Voll"

# FishPage.py
FishPageTitle = "Angeln"
FishPageTitleTank = "Fischeimer"
FishPageTitleCollection = "Fischalbum"
FishPageTitleTrophy = "Angeltrophäen"
FishPageWeightStr = "Gewicht: "
FishPageWeightLargeS = "%d kg"
FishPageWeightLargeP = "%d kg "
FishPageWeightSmallS = "%d g"
FishPageWeightSmallP = "%d g"
FishPageWeightConversion = 16
FishPageValueS = "Wert: %d Jelly Bean"
FishPageValueP = "Wert: %d Jelly Beans"
FishPageTotalValue = ""
FishPageCollectedTotal = "Gesammelte Fischarten: %d von %d"
FishPageRodInfo = "%s Angelrute\n%d - %d Pfund"
FishPageTankTab = "Eimer"
FishPageCollectionTab = "Album"
FishPageTrophyTab = "Trophäen"

FishPickerTotalValue = "Fische: %s / %s\nWert: %d Jelly Beans"

UnknownFish = "???"

FishingRod = "%s Angelrute"
FishingRodNameDict = {
    0 : "Zweig",
    1 : "Bambus",
    2 : "Hartholz",
    3 : "Stahl",
    4 : "Gold",
    }
FishTrophyNameDict = {
    0 : "Guppy",
    1 : "Elritze",
    2 : "Fisch",
    3 : "Fliegender Fisch",
    4 : "Hai",
    5 : "Swordfish",
    6 : "Killer Whale",
    }

# QuestChoiceGui.py
QuestChoiceGuiCancel = lCancel

# TrackChoiceGui.py
TrackChoiceGuiChoose = "Auswählen"
TrackChoiceGuiCancel = lCancel
TrackChoiceGuiHEAL = 'Durch Aufheitern kannst du andere Toons im Kampf heilen.'
TrackChoiceGuiTRAP = 'Fallen Stellen sind mächtige Gags, die zusammen mit einem Köder verwendet werden müssen.'
TrackChoiceGuiLURE = 'Du kannst Köder verwenden, um Bots zu betäuben oder in Fallen Stellen zu locken.'
TrackChoiceGuiSOUND = 'Sound-Gags wirken bei allen Bots, aber nicht besonders stark.'
TrackChoiceGuiDROP = "Fall-Gags richten viel Schaden an, sind jedoch nicht besonders genau."

# EmotePage.py
EmotePageTitle = "Ausdrucksmöglichkeiten / Gefühle"
EmotePageDance = "Du hast die folgende Tanzfolge aufgestellt:"
EmoteJump = "Springen"
EmoteDance = "Tanzen"
EmoteHappy = "Glücklich"
EmoteSad = "Traurig"
EmoteAnnoyed = "Verärgert"
EmoteSleep = "Schläfrig"

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nLevel %(level)s"

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "Du kannst den Spielplatz erst verlassen, wenn dein Lach-O-Meter lächelt!"

# InventoryNew.py
InventoryTotalGags = "Gags insgesamt\n%d / %d"
InventoryDelete = "LÖSCHEN"
InventoryDone = "FERTIG"
InventoryDeleteHelp = "Klicke auf einen Gag um ihn zu LÖSCHEN."
InventorySkillCredit = "Erfahrung Punkte: %s"
InventorySkillCreditNone = "Erfahrung Punkte: Keine"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Genauigkeit: %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryAffectsOneCog = "Wirkt auf: Einen "+ Cog
InventoryAffectsOneToon = "Wirkt auf: Einen Toon"
InventoryAffectsAllToons = "Wirkt auf: Alle Toons"
InventoryAffectsAllCogs = "Wirkt auf: Alle "+ Cogs
InventoryHealString = "AUFHEITERN"
InventoryDamageString = "Schaden"
InventoryBattleMenu = "KAMPFMENÜ "
InventoryRun = "RENNEN"
InventorySOS = "SOS"
InventoryPass = "AUSSETZEN"
InventoryClickToAttack = "Klick auf einen\nGag um\nanzugreifen"

# NPCForceAcknowledge.py
NPCForceAcknowledgeMessage = "Du musst mit dem Toon-Express fahren, ehe du gehst.\n\n\n\n\n\nDu findest den Toon-Express neben Goofys Gag-Laden."
NPCForceAcknowledgeMessage2 = "Du hast die Suche nach dem Toon-Express wirklich hervorragend gemeistert!\nMelde dich nun in der Toontown-Zentrale zurück.\n\n\n\n\n\nDie Toontown-Zentrale befindet sich in der Nähe der Spielplatzmitte."
NPCForceAcknowledgeMessage3 = "Vergiss nicht, mit dem Toon-Express zu fahren.\n\n\n\n\n\nDu findest ihn neben Goofys Gag-Laden."
NPCForceAcknowledgeMessage4 = "Glückwunsch! Du hast den Toon-Express gefunden und bist damit gefahren!\n\n\n\n\n\nMelde dich nun in der Toontown-Zentrale zurück."
NPCForceAcknowledgeMessage5 = "Vergiss deine Toon-Aufgabe nicht!\n\n\n\n\n\n\n\n\n\n\nAuf der anderen Seite von Tunnels wie diesem findest du Bots, gegen die du kämpfen kannst."
NPCForceAcknowledgeMessage6 = "Toll, wie du diese Bots erledigt hast!\n\n\n\n\n\n\n\n\nGehe nun so schnell wie möglich zurück zur Toontown-Zentrale."
NPCForceAcknowledgeMessage7 = "Vergiss nicht, Freundschaft zu schließen!!\n\n\n\n\n\n\nKlicke auf einen anderen Spieler und auf die Schaltfläche Neuer Freund."
NPCForceAcknowledgeMessage8 = "Prima! Du hast jetzt einen neuen Freund!\n\n\n\n\n\n\n\n\nJetzt solltest du zur Toontown-Zentrale zurückgehen."
NPCForceAcknowledgeMessage9 = "Gut, dass du das Telefon benutzt hast!\n\n\n\n\n\n\n\n\nGehe nun zur Toontown-Zentrale zurück, um dir deine Belohnung abzuholen."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "Du hast 1 Wurfpunkt erhalten! Wenn du 10 hast, bekommst du einen neuen Gag!"
MovieTutorialReward2 = "Du hast 1 Spritzpunkt erhalten! Wenn du 10 hast, bekommst du einen neuen Gag!"
MovieTutorialReward3 = "Gute Arbeit! Gut gemacht! Du hast deine erste Toon-Aufgabe erledigt!"
MovieTutorialReward4 = "Gehe zur Toontown-Zentrale, um deine Belohnung abzuholen!"
MovieTutorialReward5 = "Viel Spaß!"

# ToontownBattleGlobals.py
BattleGlobalTracks = ['Aufheitern', 'Fallen Stellen', 'Ködern', 'Volldröhnen', 'Werfen', 'Spritzen', 'Fallenlassen']
BattleGlobalNPCTracks = ['neu auffüllen', 'Toons treffen', 'Bots verfehlen']
BattleGlobalAvPropStrings = (
    ('Feder', 'Megafon', 'Lippenstift', 'Bambusrohr', 'Zauberpuder', 'Jonglierbälle'),
    ('Bananenschale', 'Harke', 'Murmeln', 'Treibsand', 'Falltür', 'TNT'),
    ('1-Euro-Schein', 'Kleiner Magnet', '5-Euro-Schein', 'Großer Magnet', '10-Euro-Schein', 'Hypno-Brille'),
    ('Motorradhupe', 'Trillerpfeife', 'Signalhorn', 'Auugah', 'Elefantenrüssel', 'Nebelhorn'),
    ('Napfkuchen', 'Obsttortenstück', 'Kremtortenstück', 'Ganze Obsttorte', 'Ganze Kremtorte', 'Geburtstagstorte'),
    ('Spritzblume', 'Glas Wasser', 'Spritzpistole', 'Seltersflasche', 'Feuerwehrschlauch', 'Sturmwolke'),
    ('Blumentopf', 'Sandsack', 'Amboss', 'Großes Gewicht', 'Safe', 'Konzertflügel')
    )
BattleGlobalAvPropStringsSingular = (
    ('eine Feder', 'ein Megafon', 'ein Lippenstift', 'ein Bambusrohr', 'ein Zauberpuder', 'ein Satz Jonglierbälle '),
    ('eine Bananenschale', 'eine Harke', 'ein Satz Murmeln', 'eine Treibsandstelle', 'eine Falltür', 'ein TNT'),
    ('ein 1-Euro-Schein', 'ein kleiner Magnet', 'ein 5-Euro-Schein', 'ein großer Magnet', 'ein 10-Euro-Schein', 'eine Hypno-Brille'),
    ('eine Motorradhupe', 'eine Trillerpfeife', 'ein Signalhorn', 'ein Auugah', 'ein Elefantenrüssel', 'ein Nebelhorn'),
    ('ein Napfkuchen', 'ein Obsttortenstück', 'ein Kremtortenstück', 'eine ganze Obsttorte', 'eine ganze Kremtorte', 'eine Geburtstagstorte'),
    ('eine Spritzblume', 'ein Glas Wasser', 'eine Spritzpistole', 'eine Seltersflasche', 'ein Feuerwehrschlauch', 'eine Sturmwolke'),
    ('ein Blumentopf', 'ein Sandsack', 'ein Amboss', 'ein großes Gewicht', 'ein Safe', 'ein Konzertflügel')
    )
BattleGlobalAvPropStringsPlural = (
    ('Federn', 'Megafone', 'Lippenstifte', 'Bambusrohre', 'Zauberpuders', 'Jonglierballsätze'),
    ('Bananenschalen', 'Harken', 'Murmelsätze', 'Treibsandstellen', 'Falltüren','TNTs'),
    ('1-Euro-Scheine', 'Kleine Magneten', '5-Euro-Scheine', 'Große Magneten','10-Euro-Scheine', 'Hypno-Brillen'),
    ('Motorradhupen', 'Trillerpfeifen', 'Signalhörner', 'Auugahs', 'Elefantenrüssel', 'Nebelhörner'),
    ('Napfkuchen', 'Obsttortenstücke', 'Kremtortenstücke','Ganze Obsttorten', 'Ganze Kremtorten', 'Geburtstagstorten '),
    ('Spritzblumen', 'Gläser mit Wasser', 'Spritzpistolen','Seltersflaschen', 'Feuerwehrschläuche', 'Sturmwolken'),
    ('Blumentöpfe', 'Sandsäcke', 'Ambosse', 'Große Gewichte', 'Safes','Konzertflügel')
    )
BattleGlobalAvTrackAccStrings = ("Mittel", "Perfekt", "Niedrig", "Hoch", "Mittel", "Hoch", "Niedrig")

AttackMissed = "VORBEI"

NPCCallButtonLabel = 'RUFEN'

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("zur",     "in der",     "Einweisungsgasse"), # Tutorial
    1000  : ("zum", "auf dem", "Spielplatz"),
    1100  : ("zum",     "auf dem",     "Muschel-Boulevard"),
    1200  : ("zur",     "in der",     "Seetangstraße"),
    1300  : ("zur",     "auf der",     "Leuchtturmgasse"),
    2000  : ("zum", "auf dem", "Spielplatz"),
    2100  : ("zur",     "in der",     "Albernstraße"),
    2200  : ("zur",     "in der",     "Hohlgasse"),
    2300  : ("zum",     "auf dem",     "Kasperwinkel"),
    3000  : ("zum", "auf dem", "Spielplatz"),
    3100  : ("zum",     "im",     "Walrossweg"),
    3200  : ("zur",     "in der",     "Schneestraße"),
    4000  : ("zum", "auf dem", "Spielplatz"),
    4100  : ("zur",     "auf der",     "Sopran-Allee"),
    4200  : ("zum",     "auf dem",     "Bass-Promenade"),
    4300  : ("zur",     "auf der",     "Tenor-Terrasse"),
    5000  : ("zum", "auf dem", "Spielplatz"),
    5100  : ("zur",     "in der",     "Ulmenstraße"),
    5200  : ("zur",     "in der",     "Ahornstraße"),
    5300  : ("zur",     "in der",     "Eichenstraße"),
    9000  : ("zum", "auf dem", "Spielplatz"),
    9100  : ("zur",     "in der",     "Schlafliedgasse"),
    10000 : ("zum",     "im",     "Chefomat-Hauptquartier"),
    10100 : ("zur", "in der", "Chefomat-Hauptquartier-Lobby"),
    11000 : ("zum", "auf dem", "Schachermat-HQ-Hof"),
    11100 : ("zur", "in der", "Schachermat-HQ-Lobby"),
    11200 : ("zur", "in der", "Schachermat-Fabrik"),
    11500 : ("zur", "in der", "Schachermat-Fabrik"),
    12000 : ("zum",     "im",     "Monetomat-Hauptquartier"),
    12100 : ("zur", "in der", "Monetomat-Hauptquartier-Lobby"),
    13000 : ("zum",     "im",     "Gesetzomat-Hauptquartier"),
    13100 : ("zur", "in der", "Gesetzomat-Hauptquartier-Lobby"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("zu",     "in",     "Donalds Dock")
ToontownCentral   = ("nach",     "in",     "Toontown Mitte")
TheBrrrgh         = ("zu",     "in",     "Das Brrr")
MinniesMelodyland = ("zu",     "in",     "Minnies Melodienland")
DaisyGardens      = ("zu",     "in",     "Daisys Gärten")
ConstructionZone  = ("zur", "in der", "Bauzone")
FunnyFarm         = ("zur", "auf der", "Spaßfarm")
GoofyStadium      = ("zum",     "im",     "Goofy-Stadion")
DonaldsDreamland  = ("zu",     "in",     "Donalds Traumland")
BossbotHQ         = ("zum",     "im",     "Chefomat-Hauptquartier")
SellbotHQ         = ("zum",     "im",     "Schachermat-HQ")
CashbotHQ         = ("zum",     "im",     "Monetomat-Hauptquartier")
LawbotHQ          = ("zum",     "im",     "Gesetzomat-Hauptquartier")
Tutorial          = ("zur", "in der ", "Einweisung")
MyEstate          = ("zu",     "in",     "Dein Haus")
WelcomeValley     = ("zum",     "im",     "Willkommens-Tal")

Factory = 'Fabrik'
Headquarters = 'Toontown-Zentrale'
SellbotFrontEntrance = 'Vordereingang'
SellbotSideEntrance = 'Seiteneingang'

FactoryNames = {
    0 : 'Fabrik-Nachbildung',
    11500 : 'Schachermat-Bot-Fabrik',
    }

FactoryTypeLeg = 'Bein'
FactoryTypeArm = 'Arm'
FactoryTypeTorso = 'Oberkörper'

# ToontownLoader.py
LoaderLabel = "Laden ..."

# PlayGame.py
HeadingToHood = "Läuft %(to)s %(hood)s..." # hood name
HeadingToYourEstate = "Läuft zu deinem Grundstück ..."
HeadingToEstate = "Läuft zu %ss Grundstück ..."  # avatar name
HeadingToFriend = "Läuft zum Grundstück von %ss Freund ..."  # avatar name

# Hood.py
HeadingToPlayground = "Läuft zum Spielplatz ..."
HeadingToStreet = "Läuft %(to)s %(street)s..." # Street name

# TownBattle.py
TownBattleRun = "Den ganzen Weg zurück zum Spielplatz rennen?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "WELCHER TOON?"
TownBattleChooseAvatarCogTitle = "WELCHER "+ string.upper(Cog) +  "?"
TownBattleChooseAvatarBack = "ZURÜCK"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "Es sind keine Freunde da!"
TownBattleSOSWhichFriend = "Welchen Freund rufen?"
TownBattleSOSNPCFriends = "Gerettete Toons"
TownBattleSOSBack = "ZURÜCK"

# TownBattleToonPanel.py
TownBattleToonSOS = "SOS"
TownBattleUndecided = "?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "Warten auf\nandere Spieler ..."
TownSoloBattleWaitTitle = "Bitte warten ..."
TownBattleWaitBack = "ZURÜCK"

TownBattleSOSPetInfoOK = lOK

# Trolley.py
TrolleyHFAMessage = "Du darfst erst in den Toon-Express einsteigen, wenn dein Lach-O-Meter lächelt."
TrolleyTFAMessage = "Du darfst erst in den Toon-Express einsteigen, wenn" + Mickey + " es sagt."
TrolleyHopOff = "Aussteigen"

# DistributedFishingSpot.py
FishingExit = "Ausgang"
FishingCast = "Werfen"
FishingAutoReel = "Automatik-Rolle"
FishingItemFound = "Du hast was gefangen"
FishingCrankTooSlow = "Zu\nlangsam"
FishingCrankTooFast = "Zu\nschnell"
FishingFailure = "Du hast nichts gefangen!"
FishingFailureTooSoon = "Hol die Schnur nicht ein, ehe etwas angebissen hat. Warte, bis der Schwimmer sich schnell rauf und runter bewegt!"
FishingFailureTooLate = "Achte darauf die Schnur einzuholen, während der Fisch noch knabbert!"
FishingFailureAutoReel = "Die Automatik-Rolle hat diesmal nicht funktioniert. Dreh die Kurbel mit der Hand, genau mit der richtigen Geschwindigkeit, damit du etwas fängst!"
FishingFailureTooSlow = "Du hast die Kurbel zu langsam gedreht. Einige Fische sind schneller als andere. Versuche, den Geschwindigkeitsanzeiger in der Mitte zu halten!"
FishingFailureTooFast = "Du hast die Kurbel zu schnell gedreht. Einige Fische sind langsamer als andere. Versuche, den Geschwindigkeitsanzeiger in der Mitte zu halten!"
FishingOverTankLimit = "Dein Fischeimer ist voll. Verkaufe deine Fische an die Tierhandlung und komm zurück."
FishingBroke = "Du hast keine Jelly Beans mehr als Ködern! Fahr mit dem Toon-Express oder verkaufe Fische an die Tierhandlung und verdiene dir dadurch mehr Jelly Beans."
FishingHowToFirstTime = "Die Schaltfläche Werfen anklicken und herunterziehen. Je weiter du nach unten ziehst, desto kräftiger ist dein Wurf. Stell deine Angel so ein, dass du die Fischziele triffst.\n\nVersuch's mal!"
FishingHowToFailed = "Die Schaltfläche Werfen anklicken und herunterziehen. Je weiter du nach unten ziehst, desto kräftiger ist dein Wurf. Stell deine Angel so ein, dass du die Fischziele triffst.\n\nVersuch's nochmal!"
FishingBootItem = "Ein alter Stiefel"
FishingJellybeanItem = "%s Jelly Beans"
FishingNewEntry = "Neue Art!"
FishingNewRecord = "Neuer Rekord!"

# FishPoker
FishPokerCashIn = "Kassiere\n%s\n%s"
FishPokerLock = "Sperren"
FishPokerUnlock = "Freigeben"
FishPoker5OfKind = "5 von einer Sorte"
FishPoker4OfKind = "4 von einer Sorte"
FishPokerFullHouse = "Full House"
FishPoker3OfKind = "3 von einer Sorte"
FishPoker2Pair = "2 Paar"
FishPokerPair = "Paar"

# DistributedTutorial.py
TutorialGreeting1 = "Hi %s!"
TutorialGreeting2 = "Hi %s!\nKomm mal her!"
TutorialGreeting3 = "Hi %s!\nKomm mal her!\nVerwende dazu die Pfeil-Tasten!"
TutorialMickeyWelcome = "Willkommen in Toontown!"
TutorialFlippyIntro = "Ich möchte dir meinen Freund"+ Flippy +  " vorstellen ..."
TutorialFlippyHi = "Hi, %s!"
TutorialQT1 = "Zum Sprechen kannst du das hier benutzen."
TutorialQT2 = "Zum Sprechen kannst du das hier benutzen.\nKlick darauf und wähle dann 'Hi'."
TutorialChat1 = "Zum Sprechen kannst einen von diesen Schaltflächen benutzen."
TutorialChat2 = "Die blaue Schaltfläche erlaubt dir, über die Tastatur chatten."
TutorialChat3 = "Vorsicht! Die meisten Mitspieler werden dich nicht verstehen, wenn du die Tastatur benutzt."
TutorialChat4 = "Die grüne Schaltfläche öffnet den %s."
TutorialChat5 = "Jeder kann dich verstehen, wenn du den %s benutzt."
TutorialChat6 = "Versuch mal, 'Hi' zu sagen."
TutorialBodyClick1 = "Sehr gut!"
TutorialBodyClick2 = "Ich freue mich, dich kennen zu lernen. Wollen wir Freunde werden?"
TutorialBodyClick3 = "Wenn du mit"+ Flippy +  "Freundschaft schließen willst, klicke ihn an ..."
TutorialHandleBodyClickSuccess = "Gut gemacht!"
TutorialHandleBodyClickFail = "Knapp daneben. Versuche mal, direkt auf"+ Flippy +  "zu klicken ..."
TutorialFriendsButton = "Nun klicke auf die Schaltfläche 'Freunde' unter"+ Flippy +  "s Bild in der rechten Ecke."
TutorialHandleFriendsButton = "Und dann klicke auf die Schaltfläche 'Ja'."
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = "Möchtest du gern mit "+ Flippy +  " Freundschaft schließen?"
TutorialFriendsPanelMickeyChat = Flippy +" ist einverstanden, dein Freund zu sein. Klicke auf 'OK', um abzuschließen."
TutorialFriendsPanelYes = Flippy +" hat Ja gesagt!"
TutorialFriendsPanelNo = "Das ist nicht besonders freundlich!"
TutorialFriendsPanelCongrats = "Glückwunsch! Du hast deinen ersten Freund."
TutorialFlippyChat1 = "Komm mich besuchen, wenn du für deine erste Toon-Aufgabe bereit bist!"
TutorialFlippyChat2 = "Ich bin in der Toonhalle!"
TutorialAllFriendsButton = "Du kannst alle deine Freunde sehen, wenn du auf die Schaltfläche 'Freunde' klickst. Probiere es aus ... "
TutorialEmptyFriendsList = "Im Moment ist deine Liste leer, weil "+ Flippy +  " kein richtiger Mitspieler ist."
TutorialCloseFriendsList = "Klicke auf den die Schaltfläche 'Schließen', damit die\nListe verschwindet"
TutorialShtickerButton = "Die Schaltfläche in der Ecke rechts unten öffnet dein Sticker-Buch. Probier es aus ..."
TutorialBook1 = "Das Buch enthält viele nützliche Informationen, zum Beispiel diesen Stadtplan von Toontown."
TutorialBook2 = "Du kannst auch die Fortschritte bei deinen Toon-Aufgaben kontrollieren."
TutorialBook3 = "Wenn du fertig bist, klicke wieder auf die Buch-Schaltfläche, damit es sich schließt."
TutorialLaffMeter1 = "Auch das hier wirst du brauchen ..."
TutorialLaffMeter2 = "Auch das hier wirst du brauchen ...\nEs ist dein Lach-O-Meter."
TutorialLaffMeter3 = "Wenn dich"+ Cogs +  " angreifen, sinkt er."
TutorialLaffMeter4 = "Wenn du auf einem Spielplatz wie diesem hier bist, geht er wieder nach oben."
TutorialLaffMeter5 = "Wenn du Toon-Aufgaben löst, bekommst du Belohnungen, wie zum Beispiel eine Erhöhung deiner Lachstärke."
TutorialLaffMeter6 = "Pass gut auf! Wenn die "+ Cogs +  " dich besiegen, verlierst du alle deine Gags."
TutorialLaffMeter7 = "Um mehr Gags zu bekommen, musst du die Toon-Express Spiele spielen."
TutorialTrolley1 = "Folge mir zum Toon-Express!"
TutorialTrolley2 = "Spring auf!"
TutorialBye1 = "Spiel ein paar Spiele!"
TutorialBye2 = "Spiel ein paar Spiele!\nKaufe ein paar Gags!"
TutorialBye3 = "Geh zu "+ Flippy +  ", wenn du fertig bist!"

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "Du gehst in die falsche Richtung! Suche"+ Mickey +  "!"

PetTutorialTitle1 = "Das Doodle-Menü"
PetTutorialTitle2 = "Doodle-Schnell-Chat"
PetTutorialTitle3 = "Doodle-Kuhtalog"
PetTutorialNext = "Nächste Seite"
PetTutorialPrev = "Vorherige Seite"
PetTutorialDone = "Fertig"
PetTutorialPage1 = "Wenn du auf ein Doodle klickst, wird das Doodle-Menü angezeigt. Von dort aus kannst du das Doodle füttern, kraulen und rufen."
PetTutorialPage2 = "Mit dem neuen Bereich 'Haustiere' im Schnell-Chat kannst du ein Doodle dazu bringen, einen Trick vorzuführen. Wenn es das tut, gib ihm eine Belohnung, dann wird es noch besser!"
PetTutorialPage3 = "Kaufe neue Doodle-Tricks aus Klarabellas Kuhtalog. Bessere Tricks bringen besseres Toonen!"
def getPetGuiAlign():
	from pandac.PandaModules import TextNode
	return TextNode.ACenter 

# Playground.py
PlaygroundDeathAckMessage = "Die "+ Cogs +  " haben all deine Gags weggenommen!\n\nDu bist traurig. Du darfst den Spielplatz nicht verlassen, bis du fröhlich bist."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "Der Vorarbeiter war erledigt, bevor du ihn erreichen konntest. Du hast keine Bot-Teile erbeuten können."

# DistributedFactory.py
HeadingToFactoryTitle = "Auf dem Weg zu %s..."
ForemanConfrontedMsg = "%s kämpft gegen den Vorarbeiter!"

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "Warte auf andere Spieler ..."
MinigamePleaseWait = "Bitte warten ..."
DefaultMinigameTitle = "Minigame-Name"
DefaultMinigameInstructions = "Minigame-Anleitungen"
HeadingToMinigameTitle = "Auf dem Weg zu %s..." # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "Kraftmesser"
MinigamePowerMeterTooSlow = "Zu\nlangsam"
MinigamePowerMeterTooFast = "Zu\nschnell"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "Minigame-Vorlage"
MinigameTemplateInstructions = "Das ist eine Mustervorlage für ein Minigame. Verwende sie, um neue Minigames zu erfinden."

# DistributedCannonGame.py
CannonGameTitle = "Kanonen-Spiel"
CannonGameInstructions = "Schieße deinen Toon so schnell du kannst in den Wasserturm. Zum Zielen kannst du die Maus oder die Pfeiltasten verwenden. Sei schnell, dann gewinnst du eine große Belohnung für alle!"
CannonGameReward = "BELOHNUNG"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Tauziehen"
TugOfWarInstructions = "Tippe abwechselnd auf die linke und rechte Pfeiltaste. Versuche das genau so schnell zu machen, dass der grüne Strich auf gleicher Höhe mit der roten Linie liegt. Wenn du zu schnell oder zu langsam tippst, landest du im Wasser!"
TugOfWarGameGo = "LOS!"
TugOfWarGameReady = "Fertig ..."
TugOfWarGameEnd = "Gut gespielt!"
TugOfWarGameTie = "Unentschieden!"
TugOfWarPowerMeter = "Kraftmesser"

# DistributedPatternGame.py
PatternGameTitle = "Vorbild "+ Minnie
PatternGameInstructions = Minnie +" wird dir einen Tanz vormachen. "+ \
                          "Versuche "+ Minnie +  "s Tanz mit den Pfeiltasten genau so zu wiederholen, wie du ihn siehst!"
PatternGameWatch   = "Achte genau auf die Tanzschritte ..."
PatternGameGo      = "LOS!"
PatternGameRight   = "Gut, %s!"
PatternGameWrong   = "Hoppla!"
PatternGamePerfect = "Das war ausgezeichnet, %s!"
PatternGameBye     = "Danke für's Mitspielen!"
PatternGameWaitingOtherPlayers = "Warte auf andere Spieler ..."
PatternGamePleaseWait = "Bitte warten ..."
PatternGameFaster = "Du warst\nschneller!"
PatternGameFastest = "Du warst\nam schnellsten!"
PatternGameYouCanDoIt = "Na los!\nDu kannst das!"
PatternGameOtherFaster = "\nwar schneller!"
PatternGameOtherFastest = "\nwar am schnellsten!"
PatternGameGreatJob = "Gut gemacht!"
PatternGameRound = "Runde %s!" # Round 1! Round 2! ..

# DistributedRaceGame.py
RaceGameTitle = "Renn-Spiel"
RaceGameInstructions = "Klicke auf eine Zahl. Wähle klug! Du kommst nur voran, wenn niemand anders dieselbe Zahl gewählt hat."
RaceGameWaitingChoices = "Warten, bis die Mitspieler gewählt haben ..."
RaceGameCardText = "%(name)s gewinnt: %(reward)s"
RaceGameCardTextBeans = "%(name)s erhält: %(reward)s"
RaceGameCardTextHi1 = "%(name)s ist ein toller Toon!"  # this category might eventually have secret game hints, etc

# RaceGameGlobals.py
RaceGameForwardOneSpace    = " 1 Feld vorwärts"
RaceGameForwardTwoSpaces   = " 2 Felder vorwärts"
RaceGameForwardThreeSpaces = " 3 Felder vorwärts"
RaceGameBackOneSpace    = " 1 Feld zurück"
RaceGameBackTwoSpaces   = " 2 Felder zurück"
RaceGameBackThreeSpaces = " 3 Felder zurück"
RaceGameOthersForwardThree = " alle anderen \n3 Felder vorwärts"
RaceGameOthersBackThree = " alle anderen \n3 Felder zurück"
RaceGameInstantWinner = "Sieger auf einen Schlag!"
RaceGameJellybeans2 = "2 Jelly Beans"
RaceGameJellybeans4 = "4 Jelly Beans"
RaceGameJellybeans10 = "10 Jelly Beans!"

# DistributedRingGame.py
RingGameTitle = "Ringe-Spiel"
# color
RingGameInstructionsSinglePlayer = "Versuche, durch so viele der %s Ringe zu schwimmen, wie du kannst. Benutze zum Schwimmen die Pfeiltasten."
# color
RingGameInstructionsMultiPlayer = "Versuche, durch die %s Ringe zu schwimmen. Andere Spieler werden es mit den Ringen in anderen Farben versuchen. Benutze zum Schwimmen die Pfeiltasten."
RingGameMissed = "VORBEI"
RingGameGroupPerfect = "GRUPPE\nPERFEKT!!"
RingGamePerfect = "PERFEKT!"
RingGameGroupBonus = "GRUPPENBONUS"

# RingGameGlobals.py
ColorRed = "roten"
ColorGreen = "grünen"
ColorOrange = "orangen"
ColorPurple = "violetten"
ColorWhite = "weißen"
ColorBlack = "schwarzen"
ColorYellow = "gelben"

# DistributedTagGame.py
TagGameTitle = "Fangen-Spiel"
TagGameInstructions = "Sammle die Münzen. Du kannst keine Münze einsammeln, wenn du fangen musst."
TagGameYouAreIt = "Du bist dran!"
TagGameSomeoneElseIsIt = "%s ist dran!"

# DistributedMazeGame.py
MazeGameTitle = "Labyrinth-Spiel"
MazeGameInstructions = "Sammle die Münzen. Versuche, sie alle zu bekommen, aber hüte dich vor den "+ Cogs +  "!"

# DistributedCatchGame.py
CatchGameTitle = "Achtung Fallobst"
CatchGameInstructions = "Fange so viele %(fruit)s auf, wie du kannst. Hüte dich vor den "+ Cogs +  " und fang möglichst keine %(badThing)s!"
CatchGamePerfect = "PERFEKT!"
CatchGameApples      = 'Äpfel'
CatchGameOranges     = 'Orangen'
CatchGamePears       = 'Birnen'
CatchGameCoconuts    = 'Kokosnüsse'
CatchGameWatermelons = 'Wassermelonen'
CatchGamePineapples  = 'Ananas'
CatchGameAnvils      = 'Ambosse'

# DistributedPieTossGame.py
PieTossGameTitle = "Tortenwurf-Spiel"
PieTossGameInstructions = "Wirf mit Torten nach den Zielen."

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "SPIELEN"

# Purchase.py
GagShopName = "Goofys Gag-Laden"
GagShopPlayAgain = "NOCHMAL\nSPIELEN"
GagShopBackToPlayground = "ZURÜCK ZUM\nSPIELPLATZ"
GagShopYouHave = "Du hast %s Jelly Beans zur Verfügung"
GagShopYouHaveOne = "Du hast 1 Jelly Bean zur Verfügung"
GagShopTooManyProps = "Entschuldige, du hast zu viele Hilfsmittel"
GagShopDoneShopping = "EINKAUF\nFERTIG"
# name of a gag
GagShopTooManyOfThatGag = "Entschuldige, du hast schon genug %s"
GagShopInsufficientSkill = "Dafür bist du noch nicht geschickt genug"
# name of a gag
GagShopYouPurchased = "Du hast %s gekauft"
GagShopOutOfJellybeans = "Entschuldige, du hast keine Jelly Beans mehr!"
GagShopWaitingOtherPlayers = "Warte auf andere Spieler ..."
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%s hat die Verbindung abgebrochen."
GagShopPlayerExited = "%s hat das Spiel verlassen"
GagShopPlayerPlayAgain = "Nochmal spielen"
GagShopPlayerBuying = "Kaufen"

# MakeAToon.py
GenderShopQuestionMickey = "Klicke auf mich, um einen männlichen Toon zu erstellen!"
GenderShopQuestionMinnie = "Klicke auf mich, um einen weiblichen Toon zu erstellen!"
GenderShopFollow = "Folge mir!"
GenderShopSeeYou = "Bis später!"
GenderShopBoyButtonText = "Junge"
GenderShopGirlButtonText = "Mädchen"

# BodyShop.py
BodyShopHead = "Kopf"
BodyShopBody = "Körper"
BodyShopLegs = "Beine"

# ColorShop.py
ColorShopHead = "Kopf"
ColorShopBody = "Körper"
ColorShopLegs = "Beine"
ColorShopToon = "Farbe"
ColorShopParts = "Teile"
ColorShopAll = "Alle"

# ClothesShop.py
ClothesShopShorts = "Shorts"
ClothesShopShirt = "Oberteil"
ClothesShopBottoms = "Unterteil"

# MakeAToon
MakeAToonDone = "Fertig"
MakeAToonCancel = lCancel
MakeAToonNext = lNext
MakeAToonLast = "Zurück"
CreateYourToon = "Drücke auf die Pfeile, um deinen Toon zu erstellen."
CreateYourToonTitle = "Deinen Toon erstellen"
CreateYourToonHead = "Klicke auf die 'Kopf'-Pfeile, um verschiedene Tiere auszusuchen."
MakeAToonClickForNextScreen = "Klicke auf den Pfeil unten, um auf die nächste Seite zu gelangen."
PickClothes = "Drücke auf die Pfeile, um dir die Kleidungsstücke für deinen Toon auszusuchen!"
PickClothesTitle = "Suche deine Kleidung aus"
PaintYourToon = "Klicke auf die Pfeile, um deinen Toon zu färben!"
PaintYourToonTitle = "Deinen Toon färben"
MakeAToonYouCanGoBack = "Du kannst auch zurückgehen, um den Körper zu ändern!"
MakeAFunnyName = "Suche dir mit meiner Maschine einen lustigen Namen aus!"
MustHaveAFirstOrLast1 = "Dein Toon sollte einen Vor- oder Nachnamen haben, meinst du nicht?"
MustHaveAFirstOrLast2 = "Möchtest du nicht, dass dein Toon einen Vor- oder Nachnamen hat?"
ApprovalForName1 = "Genau, dein Toon hat einen tollen Namen verdient!"
ApprovalForName2 = "Toon-Namen sind die besten Namen von allen!"
MakeAToonLastStep = "Letzter Schritt vor dem Besuch von Toontown!"
PickANameYouLike = "Wähle einen Namen, der dir gefällt!"
NameToonTitle = "Gib deinem Toon einen Namen"
TitleCheckBox = "Titel"
FirstCheckBox = "Vorname"
LastCheckBox = "Nachname"
RandomButton = "Beliebig"
NameShopSubmitButton = "Absenden"
TypeANameButton = "Namenseingabe"
TypeAName = "Dir gefallen diese Namen nicht?\nHier klicken -->"
PickAName = "Probier's mit dem Namenwahl-Spiel!\nHier klicken -->"
PickANameButton = "Namenwahl"
RejectNameText = "Dieser Name ist nicht zulässig. Versuch's bitte noch einmal."
WaitingForNameSubmission = "Namen absenden ..."

# PetshopGUI.py
PetNameMaster = "PetNameMaster_german.txt"
PetshopUnknownName = "Name: ???"
PetshopDescGender = "Geschlecht:\t%s"
PetshopDescCost = "Preis:\t%s Jelly Beans"
PetshopDescTrait = "Charakter:\t%s"
PetshopDescStandard = "Standard"
PetshopCancel = lCancel
PetshopSell = "Fisch verkaufen"
PetshopAdoptAPet = "Ein Doodle aufnehmen"
PetshopReturnPet = "Doodle zurückbringen"
PetshopAdoptConfirm = "%s für %d Jelly Beans aufnehmen?"
PetshopGoBack = "Zurückgehen"
PetshopAdopt = "Aufnehmen"
PetshopReturnConfirm = "%s zurückbringen?"
PetshopReturn = "Zurückbringen"
PetshopChooserTitle = "DOODLE DES TAGES"
PetshopGoHomeText = 'Möchtest du auf dein Grundstück gehen und mit deinem neuen Doodle spielen?'

# NameShop.py
NameShopNameMaster = "NameMaster_german.txt"
NameShopPay = "Jetzt abonnieren!"
NameShopPlay = "Kostenlose Probezeit"
NameShopOnlyPaid = "Nur Benutzer, die bezahlt haben,\ndürfen ihren Toons selbst Namen geben.\nBis du dich für ein Abonnement entschieden hast, wird\ndein Toon folgenden Namen haben:\n"
NameShopContinueSubmission = "Weiter absenden"
NameShopChooseAnother = "Anderen Namen wählen"
NameShopToonCouncil = "Der Rat von Toontown\nwird deinen\nNamen prüfen. "+ \
                      "Die Prüfung kann\nein paar Tage dauern.\nInzwischen bekommst\ndu folgenden Namen zugeteilt:\n "
PleaseTypeName = "Bitte gib deinen Namen ein:"
AllNewNames = "Alle neuen Namen\nbedürfen der Genehmigung\ndurch den Rat von Toontown."
NameShopNameRejected = "Der Name, den du\nbeantragt hast,\nwurde abgelehnt."
NameShopNameAccepted = "Glückwunsch!\nDer Name, den du\nbeantragt hast,\nwurde angenommen!"
NoPunctuation = "Du kannst in deinem Namen keine Satzzeichen verwenden!"
PeriodOnlyAfterLetter = "Du kannst einen Punkt in deinem Namen verwenden, aber nur nach einem Buchstaben."
ApostropheOnlyAfterLetter = "Du kannst einen Apostroph in deinem Namen verwenden, aber nur nach einem Buchstaben."
NoNumbersInTheMiddle = "In der Mitte eines Wortes dürfen keine Ziffern erscheinen."
ThreeWordsOrLess = "Dein Name darf nur aus höchstens drei Wörtern bestehen."
CopyrightedNames = (
    "micky",
    "micky maus",
    "mickymaus",
    "minnie",
    "minnie maus",
    "minniemaus",
    "donald",
    "donald duck",
    "donaldduck",
    "pluto",
    "goofy",
    )
NumToColor = ['Weiß', 'Pfirsichorange', 'Hellrot', 'Rot', 'Kastanienbraun',
              'Ockergelb', 'Braun', 'Hautfarben', 'Korallenrot', 'Orange',
              'Gelb', 'Cremeweiß', 'Zitronengelb', 'Lindgrün', 'Meergrün',
              'Grün', 'Hellblau', 'Blaugrün', 'Blau',
              'Immergrün', 'Königsblau', 'Schieferblau', 'Lila',
              'Lavendellila', 'Pink']
AnimalToSpecies = {
    'dog'    : 'Hund',
    'cat'    : 'Katze',
    'mouse'  : 'Maus',
    'horse'  : 'Pferd',
    'rabbit' : 'Kaninchen',
    'duck'   : 'Ente',
    'fowl'   : 'Ente',
    }
NameTooLong = "Der Name ist zu lang. Bitte versuche es noch einmal."
ToonAlreadyExists = "Du hast schon einen Toon namens %s!"
NameAlreadyInUse = "Der Name ist schon vergeben!"
EmptyNameError = "Du musst erst einen Namen eingeben."
NameError = "Dieser Name geht leider nicht."

# NameCheck.py
NCTooShort = 'Dieser Name ist zu kurz.'
NCNoDigits = 'Dein Name darf keine Zahlen enthalten.'
NCNeedLetters = 'Jedes Wort in deinem Namen muss mehrere Buchstaben enthalten.'
NCNeedVowels = 'Jedes Wort in deinem Namen muss einige Vokale (Selbstlaute) enthalten.'
NCAllCaps = 'Dein Name darf nicht nur aus Großbuchstaben bestehen.'
NCMixedCase = 'Dieser Name hat zu viele Großbuchstaben.'
NCBadCharacter = "Dein Name darf das Zeichen '%s' nicht enthalten."
NCGeneric = 'Dieser Name geht leider nicht.'
NCTooManyWords = 'Dein Name darf nicht mehr als vier Wörter lang sein.'
NCDashUsage = ("Bindestriche dürfen nur verwendet werden, um zwei Wörter zu verbinden"
               "(wie bei 'Klaus-Dieter').")
NCCommaEdge = "Dein Name darf nicht mit einem Komma beginnen oder enden."
NCCommaAfterWord = "Du darfst ein Wort nicht mit einem Komma beginnen lassen."
NCCommaUsage = ('In diesem Namen sind Kommas nicht richtig eingesetzt. Kommas müssen zeigen,'
                'dass zwei Wörter zusammengehören, wie in dem Namen "Quiselda Quittung, RA". '
                'Nach Kommas muss ein Leerzeichen folgen.')
NCPeriodUsage = ('In diesem Namen sind Punkte nicht richtig eingesetzt. Punkte sind'
                 'nur gestattet in Wörtern wie "Dr.", "Frl.", "J.T." usw.')
NCApostrophes = 'Dieser Name hat zu viele Apostrophe.'

# DistributedTrophyMgrAI.py
RemoveTrophy = "Toontown-Zentrale: Die " + Cogs + " haben eines der von dir geretteten Gebäude eingenommen!"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = 'Brauchst du mehr Zeit zum Nachdenken?'
STOREOWNER_GOODBYE = 'Bis später!'
STOREOWNER_NEEDJELLYBEANS = 'Du musst mit dem Toon-Express fahren, dann bekommst du in paar Jelly Beans.'
STOREOWNER_GREETING = 'Wähle aus, was du kaufen möchtest.'
STOREOWNER_BROWSING = 'Du kannst stöbern, aber zum Kaufen brauchst du eine Kleidermarke.'
STOREOWNER_NOCLOTHINGTICKET = 'Du brauchst eine Kleidermarke, um Kleidung zu kaufen.'
# translate
STOREOWNER_NOFISH = 'Komm wieder her, um der Tierhandlung gegen Jelly Beans Fische zu verkaufen.'
STOREOWNER_THANKSFISH = 'Danke! Die Tierhandlung wird sich freuen. Tschüss!'
STOREOWNER_THANKSFISH_PETSHOP = "Das sind aber ein paar schöne Exemplare! Danke."
STOREOWNER_PETRETURNED = "Keine Sorge. Wir finden ein schönes Zuhause für dein Doodle."
STOREOWNER_PETADOPTED = "Glückwunsch zu deinem neuen Doodle! Du kannst auf deinem Grundstück mit ihm spielen."
STOREOWNER_PETCANCELED = "Denk daran: Wenn du ein Doodle siehst, das dir gefällt, solltest du es aufnehmen, bevor es jemand anders tut!"

STOREOWNER_NOROOM = "Hmm... du solltest vielleicht in deinem Schrank erst etwas Platz schaffen, bevor du neue Kleidung kaufst.\n"
STOREOWNER_CONFIRM_LOSS = "Dein Schrank ist voll. Du wirst die Kleidung verlieren, die du gerade trägst."
STOREOWNER_OK = lOK
STOREOWNER_CANCEL = lCancel
STOREOWNER_TROPHY = "Wow! Du hast %s von %s Fischen gesammelt. Dafür verdienst du eine Trophäe und eine Lach-Spritze!"
# end translate

# NewsManager.py
SuitInvasionBegin1 = "Toontown-\nZentrale: Eine Bot-Invasion hat begonnen!!!"
SuitInvasionBegin2 = "Toontown-\nZentrale: %s haben Toontown eingenommen!!!"
SuitInvasionEnd1 = "Toontown-\nZentrale: Die %s-Invasion ist beendet!!!"
SuitInvasionEnd2 = "Toontown-\nZentrale: Die Toons haben wieder einmal gesiegt!!!"
SuitInvasionUpdate1 = "Toontown-\nZentrale: Die Bot-Invasion liegt jetzt bei %s Bots!!!"
SuitInvasionUpdate2 = "Toontown-\nZentrale: Wir müssen sie besiegen, diese %s!!!"
SuitInvasionBulletin1 = "Toontown-\nZentrale: Es ist eine Bot-Invasion im Gange!!!"
SuitInvasionBulletin2 = "Toontown-\nZentrale: %s haben Toontown eingenommen!!!"

# DistributedHQInterior.py
LeaderboardTitle = "Toon-Aufgebot"
# QuestScript.txt
QuestScriptTutorialMickey_1 = "Toontown hat einen neuen Einwohner! Hast du ein paar Extra-Gags?"
QuestScriptTutorialMickey_2 = "Klar, %s!"
QuestScriptTutorialMickey_3 = "Einweiser Ede wird dir alles über die Bots erzählen.\aIch muss jetzt los! Tschüss!"
QuestScriptTutorialMickey_4 = "Komm bitte näher! Verwende die Pfeiltasten, um dich zu bewegen."

# These are needed to correspond to the Japanese gender specific phrases
QuestScriptTutorialMinnie_1 = "Toontown hat einen neuen Einwohner! Hast du ein paar Extra-Gags?"
QuestScriptTutorialMinnie_2 = "Klar, %s!"
QuestScriptTutorialMinnie_3 = "Einweise Ede wird dir alles über die Bots erzählen.\aIch muss jetzt los! Tschüss!"

QuestScript101_1 = "Das hier sind BOTS. BOTS sind Roboter, die versuchen Toontown einzunehmen. "
QuestScript101_2 = "Es gibt viele verschiedene Arten von BOTS und ..."
QuestScript101_3 = "... sie verwandeln fröhliche Toon-Gebäude ..."
QuestScript101_4 = "... in hässliche Bot-Gebäude!"
QuestScript101_5 = "Aber BOTS vertragen keinen Spaß!"
QuestScript101_6 = "Ein guter Gag stoppt sie."
QuestScript101_7 = "Es gibt viele Gags, aber nimm für den Anfang erst mal diese."
QuestScript101_8 = "Ach ja! Du brauchst auch noch ein Lach-O-Meter!"
QuestScript101_9 = "Wenn dein Lach-O-Meter zu weit absinkt, wirst du traurig!"
QuestScript101_10 = "Nur ein fröhlicher Toon ist ein gesunder Toon!"
QuestScript101_11 = "OH NEIN! Vor meinem Laden steht ein BOT!"
QuestScript101_12 = "BITTE HILF MIR! Besiege diesen Bot!"
QuestScript101_13 = "Hier ist deine erste Toon-Aufgabe!"
QuestScript101_14 = "Beeil dich! Gehe los und besiege diesen Kriecher!"

QuestScript110_1 = "Gute Arbeit, wie du diesen Kriecher besiegt hast. Ich werde dir dafür ein Sticker-Buch geben ... "
QuestScript110_2 = "In dem Buch sind lauter nützliche Sachen."
QuestScript110_3 = "Öffne es, dann zeig ich sie dir."
QuestScript110_4 = "Der Stadtplan zeigt, wo du warst."
QuestScript110_5 = "Blättere um, dann siehst du deine Gags ..."
QuestScript110_6 = "Oje du hast keine Gags! Ich gebe dir eine Aufgabe."
QuestScript110_7 = "Blättere um, dann siehst du deine Aufgaben."
QuestScript110_8 = "Gehe zum Toon-Express, spiele Spiele und verdiene Jelly Beans, um dir Gags zu kaufen. "
QuestScript110_9 = "Zum Toon-Express kommst du, wenn du durch die Tür hinter mir zum Spielplatz gehst."
QuestScript110_10 = "Mache bitte nun das Buch zu und suche den Toon-Express!"
QuestScript110_11 = "Komm bitte wieder zurück zur Toontown-Zentrale, wenn du fertig bist. Tschüss!"

QuestScriptTutorialBlocker_1 = "Na hallo!"
QuestScriptTutorialBlocker_2 = "Hallo?"
QuestScriptTutorialBlocker_3 = "Oh, du weißt nicht, wie man den Schnell-Chat benutzt!"
QuestScriptTutorialBlocker_4 = "Klicke auf die Schaltfläche, um etwas zu sagen."
QuestScriptTutorialBlocker_5 = "Sehr gut!\aDort, wo du hingehst, sind viele Toons, mit denen man sich unterhalten kann."
QuestScriptTutorialBlocker_6 = "Wenn du mit deinen Freunden über die Tastatur chatten willst, kannst du eine andere Schaltfläche benutzen."
QuestScriptTutorialBlocker_7 = "Sie heißt 'Chat'-Schaltfläche. Du musst offizieller Einwohner von Toontown sein, um sie zu benutzen."
QuestScriptTutorialBlocker_8 = "Viel Glück! Bis später!"

"""
GagShopTut

Du wirst auch die Fähigkeit erwerben, andere Gag-Arten einzusetzen.
"""

QuestScriptGagShop_1 = "Willkommen im Gag-Laden!"
QuestScriptGagShop_1a = "Hier kaufen die Toons die Gags, mit denen sie gegen die Bots kämpfen können."
#QuestScriptGagShop_2 = "Dieses Gefäß zeigt, wie viele Jelly Beans du hast."
#QuestScriptGagShop_3 = "Klicke auf eine Gag-Schaltfläche, um einen Gag zu kaufen. Versuche es gleich einmal!"
QuestScriptGagShop_3 = "Klicke auf die Gag-Schaltflächen, um Gags zu kaufen. Versuche gleich mal, welche zu bekommen!"
QuestScriptGagShop_4 = "Gut! Du kannst diese Gags im Kampf gegen die Bots einsetzen."
QuestScriptGagShop_5 = "Hier kannst du einen Blick auf die höheren Wurf- und Spritzgags werfen ..."
QuestScriptGagShop_6 = "Wenn du genug Gags gekauft hast, klicke diese Schaltfläche an um zum Spielplatz zurückzukehren."
QuestScriptGagShop_7 = "Normalerweise kannst du diese Schaltfläche verwenden, um noch ein Toon-Express-Spiel zu spielen ..."
QuestScriptGagShop_8 = "... aber im Moment ist gerade keine Zeit für ein weiteres Spiel. Man braucht dich in der Toontown-Zentrale!"

QuestScript120_1 = "Klasse, du hast den Toon-Express gut gefunden!\aÜbrigens, kennst du Bankier Bob schon?\aEr ist ein ziemlicher Naschkater.\aFühr dich doch bei ihm gleich mal gut ein, indem du ihm diesen Schokoriegel als kleines Geschenk mitbringst."
QuestScript120_2 = "Bankier Bob sitzt drüben in der Toontown Bank."

QuestScript121_1 = "Mmh, danke für den Schokoriegel.\aHör mal, wenn du mir helfen kannst, geb ich dir eine Belohnung.\aDiese Bots haben die Schlüssel zu meinem Safe gestohlen. Erledige Bots, um einen gestohlenen Schlüssel zu finden.\aWenn du einen Schlüssel findest, bring ihn wieder her zu mir."
QuestScript130_1 = " Klasse, du hast den Toon-Express gut gefunden!\aÜbrigens habe ich heute ein Paket für Professor Peter erhalten.\aEs muss wohl die neue Kreide sein, die er bestellt hat.\aKannst du es ihm bitte bringen?\aEr ist drüben in der Schule."

QuestScript131_1 = "Oh, danke für die Kreide.\aWas?!?\aDiese Bots haben meine Tafel gestohlen. Erledige Bots, um meine gestohlene Tafel zu finden.\aWenn du sie findest, bring sie wieder her zu mir."

QuestScript140_1 = " Klasse, du hast den Toon-Express gut gefunden!\aÜbrigens habe ich da einen Freund, Bibliothekar Bertie, der ein ziemlicher Bücherwurm ist.\aIch habe letztens dieses Buch für ihn gefunden, als ich drüben in Donalds Dock war.\aKönntest du es ihm bringen? Er ist normalerweise in der Bibliothek."

QuestScript141_1 = "Oh ja, mit diesem Buch ist meine Sammlung fast vollständig.\aLass mal sehen ...\aÄhm, öh ...\aWo hab ich denn jetzt meine Brille hingelegt?\aIch hatte sie noch, kurz bevor diese Bots mein Gebäude einnahmen.\aErledige Bots, um meine gestohlene Brille zu finden.\aWenn du sie findest, bring sie wieder her zu mir und du bekommst eine Belohnung."

QuestScript145_1 = "Wie ich sehe, hattest du kein Problem mit dem Toon-Express!\aHör mal, die Bots haben unseren Schwamm gestohlen.\aGeh raus auf die Straße und kämpfe gegen Bots, bis du den Schwamm zurückgeholt hast.\aZur Straße gelangst du so durch einen der Tunnel:"
QuestScript145_2 = "Wenn du unseren Schwamm findest, bring ihn hierher zurück.\aVergiss nicht: Wenn du Gags brauchst, fahr mit dem Toon-Express.\aUnd wenn du deine Lach-Punkte nachfüllen musst, sammle Eistüten auf dem Spielplatz."

QuestScript150_1 = "Großartige Arbeit!\aDie nächste Aufgabe ist vielleicht für dich alleine zu schwer ..."
QuestScript150_2 = "Suche einen Mitspieler, mit dem du dich anfreunden kannst, und benutze die Schaltfläche 'Neuer Freund'."
QuestScript150_3 = "Wenn du einen Freund gefunden hast, komm wieder her."
QuestScript150_4 = "Manche Aufgaben sind für einen allein zu schwierig!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignorier mich"

BossCogName = "Vize\npräzident"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "Ihr werdet hiermit zu richtigen %s ernannt. Glückwunsch!"
BossCogDoobersAway = { 's' : "Geh los! Und erledige das Geschäft!" }
BossCogWelcomeToons = "Willkommen, neue Bots!"
BossCogPromoteToons = "Ihr werdet hiermit zu richtigen %s ernannt. Glück ..."
CagedToonInterruptBoss = "He! Hallo! He, ihr da!"
CagedToonRescueQuery = "Seid ihr Toons also gekommen, um mich zu befreien?"
BossCogDiscoverToons = "Was? Toons! Getarnt!"
BossCogAttackToons = "Angriff!!"
CagedToonDrop = [
    "Großartig! Ihr macht ihn fertig!",
    "Bleibt ihm auf den Fersen! Er flüchtet!",
    "Ihr macht das prima!",
    "Fantastisch! Jetzt habt ihr ihn gleich!",
    ]
CagedToonPrepareBattleTwo = "Passt auf, er versucht, zu entwischen!\aHelft mir mal alle - kommt hier rauf und haltet ihn auf!"
CagedToonPrepareBattleThree = "Hurra, ich bin fast frei!\aJetzt musst du den Bot-VP direkt angreifen.\aIch hab einen ganzen Stapel Torten, die du nehmen kannst!\aSpring hoch und berühre den Boden meines Käfigs, dann gebe ich dir ein paar Torten.\aDrück die Taste Einfg., um Torten zu werfen, wenn du sie hast!"
BossBattleNeedMorePies = "Du brauchst mehr Torten!"
BossBattleHowToGetPies = "Spring hoch und berühre den Käfig, um Torten zu bekommen."
BossBattleHowToThrowPies = "Drücke die Taste Einfg., um Torten zu werfen!"
CagedToonYippee = "Jippieh!"
CagedToonThankYou = "Es ist toll, frei zu sein!\aDanke für deine Hilfe!\aIch stehe in deiner Schuld.\aWenn du jemals Hilfe im Kampf brauchst, ruf mich einfach!\aKlicke einfach auf die Schaltfläche SOS, um mich zu rufen."
CagedToonPromotion = "\aHör mal - dieser Bot-VP hat deine Beförderungspapiere zurückgelassen.\aIch reiche sie auf dem Weg nach draußen für dich ein, damit du befördert wirst!"
CagedToonLastPromotion = "\aWow, du hast auf deinem Bot-Anzug der Stufe %s erreicht!\aHöher wird kein Bot befördert.\aDu kannst keinen höheren Bot-Anzug mehr erreichen, aber du kannst auf jeden Fall weiter Toons retten!"
CagedToonHPBoost = "\aDu hast viele Toons aus diesem HQ gerettet.\aDer Rat von Toontown hat beschlossen, dir noch einen Lach-Punkt zu geben. Herzlichen Glückwunsch!"
CagedToonMaxed = "\aIch sehe, dass du einen Bot-Anzug der Stufe %s hast. Sehr beeindruckend!\aIm Namen des Rates von Toontown vielen Dank dafür, dass du zurückgekommen bist, um noch mehr Toons zu retten!"
CagedToonGoodbye = "Bis dann!"


CagedToonBattleThree = {
    10: "Gut gesprungen, %(toon)s. Hier sind ein paar Torten!",
    11: "Hi, %(toon)s! Nimm dir ein paar Torten!",
    12: "He, %(toon)s! Du hast jetzt ein paar Torten!",

    20: "He, %(toon)s! Spring zu meinem Käfig hoch und hol dir ein paar Torten zum Werfen!",
    21: "Hi, %(toon)s!  Benutze die Strg.-Taste, um hochzuspringen und meinen Käfig zu berühren!",

    100: "Drücke die Einfg-Taste, um eine Torte zu werfen.",
    101: "Der blaue Kraftmesser zeigt an, wie hoch deine Torte fliegt.",
    102: "Versuche zuerst, eine Torte in sein Fahrgestell zu schmettern, um seinen Antrieb außer Gefecht zu setzen.",
    103: "Warte, bis die Tür aufgeht, und wirf eine Torte direkt hinein.",
    104: "Wenn er benommen ist, wirf sie in sein Gesicht oder gegen seine Brust, um ihn umzuschmeißen!",
    105: "Einen guten Treffer erkennst du daran, dass der Platscher farbig ist.",
    106: "Wenn du einen Toon mit einer Torte triffst, erhält der Toon dadurch einen Lach-Punkt!",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

BossElevatorRejectMessage = "Du kannst erst in diesen Aufzug einsteigen, wenn du dir eine Beförderung verdient hast." 

# Types of catalog items--don't translate yet.
FurnitureTypeName = "Möbel"
PaintingTypeName = "Gemälde"
ClothingTypeName = "Kleidung"
ChatTypeName = "Schnell-Chat\3Wendung"
EmoteTypeName = "Schauspiel\3Unterricht"
PoleTypeName = "Angelrute"
WindowViewTypeName = "Aussicht"
PetTrickTypeName = "Doodle-Training"

FurnitureYourOldCloset = "dein alter Kleiderschrank"
FurnitureYourOldBank = "deine alte Sparbüchse"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py--don't translate yet.
FurnitureNames = {
  100 : "Sessel",
  105 : "Sessel",
  110 : "Stuhl",
  120 : "Schreibtischsessel",
  130 : "Blockstuhl",
  140 : "Hummerstuhl",
  145 : "Rettungswesten\3Stuhl",
  150 : "Sattelstuhl",
  160 : "Eingeborenenstuhl",
  170 : "Kuchenstuhl",
  200 : "Bett",
  205 : "Bett",
  210 : "Bett",
  220 : "Badewannenbett ",
  230 : "Laubbett",
  240 : "Bootbett",
  250 : "Kaktushängematte",
  260 : "Eiskrembett",
  300 : "Altes Klavier",
  310 : "Orgel mit Pfeifen",
  400 : "Kamin",
  410 : "Kamin",
  420 : "Runder Kamin",
  430 : "Kamin",
  440 : "Apfelkamin",
  500 : "Kleiderschrank",
  502 : "Schrank f. 15 Kleidungsstücken",
  510 : "Kleiderschrank",
  512 : "Schrank f. 15 Kleidungsstücken",
  600 : "Niedrige Lampe",
  610 : "Hohe Lampe",
  620 : "Tischlampe",
  625 : "Tischlampe",
  630 : "Blumenlampe ",
  640 : "Blumenlampe",
  650 : "Quallenlampe",
  660 : "Quallenlampe",
  670 : "Cowboylampe",
  700 : "Polstersessel",
  705 : "Polstersessel",
  710 : "Couch",
  715 : "Couch",
  720 : "Heucouch",
  730 : "Kuchensofa",
  800 : "Schreibtisch",
  810 : "Blockschreibtisch",
  900 : "Schirmständer",
  910 : "Garderobe",
  920 : "Mülltonne",
  930 : "Roter Pilz",
  940 : "Gelber Pilz",
  950 : "Garderobe",
  960 : "Fassständer",
  970 : "Kaktuspflanze",
  980 : "Tipi",
  1000 : "Großer Teppisch",
  1010 : "Runder Teppich",
  1015 : "Runder Teppich",
  1020 : "Kleiner Teppich",
  1030 : "Laubmatte",
  1100 : "Vitrine",
  1110 : "Vitrine",
  1120 : "Hohes Bücherregal",
  1130 : "Niedriges Regal",
  1140 : "Eisbechertruhe",
  1200 : "Beistelltisch",
  1210 : "Kleiner Tisch",
  1215 : "Kleiner Tisch",
  1220 : "Couchtisch",
  1230 : "Couchtisch",
  1240 : "Schnorchlertisch",
  1250 : "Kekstisch",
  1260 : "Nachttisch",
  1300 : "Büchse f. 1000 Jelly Beans",
  1310 : "Büchse f. 2500 Jelly Beans",
  1320 : "Büchse f. 5000 Jelly Beans",
  1330 : "Büchse f. 7500 Jelly Beans",
  1340 : "Büchse f. 10000 Jelly Beans",
  1399 : "Telefon",
  1400 : "Cezanne-Toon",
  1410 : "Blumen",
  1420 : "Moderner Micky",
  1430 : "Rembrandt-Toon",
  1440 : "Toonschaft",
  1441 : "Whistlers Pferd",
  1442 : "Toon-Stern",
  1443 : "Keine Torte",
  1500 : "Radio",
  1510 : "Radio",
  1520 : "Radio",
  1530 : "Fernseher",
  1600 : "Niedrige Vase",
  1610 : "Hohe Vase",
  1620 : "Niedrige Vase",
  1630 : "Hohe Vase",
  1640 : "Niedrige Vase",
  1650 : "Niedrige Vase",
  1660 : "Korallenvase",
  1661 : "Muschelvase",
  1700 : "Popcorn-Wagen",
  1710 : "Marienkäfer",
  1720 : "Springbrunnen",
  1725 : "Waschmaschine",
  1800 : "Aquarium",
  1810 : "Aquarium",
  1900 : "Schwertfisch",
  1910 : "Hammerhai",
  1920 : "Hängende Hörner",
  1930 : "Einfacher Sombrero",
  1940 : "Schicker Sombrero",
  1950 : "Traumfänger",
  1960 : "Hufeisen",
  1970 : "Bisonporträt",
  2000 : "Zuckerschaukel",
  2010 : "Kuchenrutsche",
  3000 : "Bananensplit-Wanne",
  10000 : "Kleiner Kürbis",
  10010 : "Großer Kürbis",
  }

# CatalogClothingItem.py--don't translate yet.
ClothingArticleNames = (
    "Oberteil",
    "Oberteil",
    "Oberteil",
    "Hosen",
    "Hosen",
    "Rock",
    "Hosen",
    )

ClothingTypeNames = {
    1400 : "Matthias Hemd",
    1401 : "Jessicas Bluse",
    1402 : "Marissas Bluse",
    }

# CatalogSurfaceItem.py--don't translate yet.
SurfaceNames = (
    "Tapete",
    "Zierleiste",
    "Bodenbelag",
    "Wandvertäfelung",
    "Einfassung",
    )

WallpaperNames = {
    1000 : "Pergament",
    1100 : "Mailand",
    1200 : "Dover",
    1300 : "Victoria",
    1400 : "Newport",
    1500 : "Idylle",
    1600 : "Harlekin",
    1700 : "Mond",
    1800 : "Sterne",
    1900 : "Blumen",
    2000 : "Garten im Frühling",
    2100 : "Architektonischer Garten",
    2200 : "Renntag",
    2300 : "Treffer!",
    2400 : "7. Himmel",
    2500 : "Kletterranke",
    2600 : "Frühling",
    2700 : "Kokeshi-Puppe",
    2800 : "Sträußchen",
    2900 : "Engelhai",
    3000 : "Blasen",
    3100 : "Blasen",
    3200 : "Go-Fisch",
    3300 : "Stoppfisch",
    3400 : "Seepferdchen",
    3500 : "Meeresmuscheln",
    3600 : "Unterwasser",
    3700 : "Stiefel",
    3800 : "Kaktus",
    3900 : "Cowboyhut",
    10100 : "Katzen",
    10200 : "Fledermäuse",
    11000 : "Schneeflocken",
    11100 : "Stechpalmenblatt",
    11200 : "Schneemann",
    13000 : "Kleeblatt",
    13100 : "Kleeblatt",
    13200 : "Regenbogen",
    13300 : "Kleeblatt",
    }

FlooringNames = {
    1000 : "Hartholzboden",
    1010 : "Teppich",
    1020 : "Rhombische Fliese",
    1030 : "Rhombische Fliese",
    1040 : "Gras",
    1050 : "Beige Ziegel",
    1060 : "Rote Ziegel",
    1070 : "Quadratische Fliese",
    1080 : "Stein",
    1090 : "Plankenweg",
    1100 : "Schotterstraße",
    1110 : "Holzplatte",
    1120 : "Fliese",
    1130 : "Wabe",
    1140 : "Wasser",
    1150 : "Strandplatte",
    1160 : "Strandplatte",
    1170 : "Strandplatte",
    1180 : "Strandplatte",
    1190 : "Sand",
    10000 : "Eiswürfel",
    10010 : "Iglu",
    11000 : "Kleeblatt",
    11010 : "Kleeblatt",
    }

MouldingNames = {
    1000 : "Knorrig",
    1010 : "Angestrichen",
    1020 : "Gebiss", 
    1030 : "Blumen ",
    1040 : "Blumen",
    1050 : "Marienkäfer",
    }

WainscotingNames = {
    1000 : "Angestrichen",
    1010 : "Holzpaneel",
    1020 : "Holz",
    }

# CatalogWindowItem.py--don't translate yet.
WindowViewNames = {
    10 : "Großer Garten",
    20 : "Wilder Garten",
    30 : "Griechischer Garten",
    40 : "Stadtlandschaft",
    50 : "Wilder Westen",
    60 : "Unter Wasser",
    70 : "Tropische Insel",
    80 : "Sternenhimmel",
    90 : "Tiki-Pool",
    100 : "Eisige Grenze",
    110 : "Farmland",
    120 : "Eingeborenenlager",
    130 : "Hauptstraße",
    }

# don't translate yet
NewCatalogNotify = "Bei deinem Telefon gibt es neue Artikel zu bestellen!"
NewDeliveryNotify = "Eine neue Lieferung ist in deinem Briefkasten angekommen!"
CatalogNotifyFirstCatalog = "Dein erster Kuhtalog ist eingetroffen! Du kannst damit neue Sachen für dich oder dein Haus bestellen."
CatalogNotifyNewCatalog = "Dein Kuhtalog Nr. %s ist eingetroffen! Du kannst jetzt zu deinem Telefon gehen und Artikel aus diesem Kuhtalog bestellen."
CatalogNotifyNewCatalogNewDelivery = "Eine neue Lieferung ist in deinem Briefkasten angekommen! Und dein Kuhtalog Nr. %s ist auch eingetroffen!"
CatalogNotifyNewDelivery = "Eine neue Lieferung ist in deinem Briefkasten angekommen!"
CatalogNotifyNewCatalogOldDelivery = "Dein Kuhtalog Nr. %s ist eingetroffen und es warten immer noch Artikel in deinem Briefkasten!"
CatalogNotifyOldDelivery = "In deinem Briefkasten warten immer noch ein paar Artikel darauf, dass du sie abholst!"
CatalogNotifyInstructions = "Klicke auf der Stadtplanseite in deinem Sticker-Buch auf die Schaltfläche 'Nach Hause' und geh dann zum Telefon in deinem Haus."
CatalogNewDeliveryButton = "Neue\nLieferung!"
CatalogNewCatalogButton = "Neuer\nKuhtalog"
CatalogSaleItem = "Ausverkauf! "

# don't translate yet
DistributedMailboxEmpty = "Dein Briefkasten ist derzeit leer. Komm wieder her, um nach Lieferungen zu sehen, wenn du von deinem Telefon aus eine Bestellung aufgegeben hast!"
DistributedMailboxWaiting = "Dein Briefkasten ist derzeit noch leer, aber das von dir bestellte Paket ist unterwegs. Schau später nochmal nach!"
DistributedMailboxReady = "Deine Bestellung ist angekommen!"
DistributedMailboxNotOwner = "Entschuldige, das ist nicht dein Briefkasten."
DistributedPhoneEmpty = "Du kannst von jedem Telefon aus spezielle Artikel für dich und dein Haus bestellen. Im Laufe der Zeit werden neue Artikel zur Bestellung angeboten.\n\nIm Moment gibt es für dich keine Artikel zu bestellen, aber schau später nochmal nach!"

# don't translate yet
Clarabelle = "Klarabella"
MailboxExitButton = "Briefkasten schließen"
MailboxAcceptButton = "Diesen Artikel nehmen"
MailboxOneItem = "Dein Briefkasten enthält 1 Artikel."
MailboxNumberOfItems = "Dein Briefkasten enthält %s Artikel."
MailboxGettingItem = "%s wird aus dem Briefkasten genommen."
MailboxItemNext = "Nächster\nArtikel"
MailboxItemPrev = "Vorheriger\nArtikel"
CatalogCurrency = "Jelly Beans"
CatalogHangUp = "Auflegen"
CatalogNew = "NEU"
CatalogBackorder = "LIEFERRÜCKSTAND"
CatalogPagePrefix = "Seite"
CatalogGreeting = "Hallo! Danke für deinen Anruf bei Klarabellas Kuhtalog. Kann ich dir helfen?"
CatalogGoodbyeList = ["Wiederhören!",
                      "Bis zum nächsten Mal!",
                      "Vielen Dank für deinen Anruf!",
                      "OK, tschüss dann!",
                      "Tschüss!",
                      ]
CatalogHelpText1 = "Blättere um, dann kommst du zu den Verkaufsartikeln."
CatalogSeriesLabel = "Serie %s"
CatalogPurchaseItemAvailable = "Herzlichen Glückwunsch zum Neuerwerb! Du kannst ihn sofort benutzen."
CatalogPurchaseItemOnOrder = "Herzlichen Glückwunsch! Die gekauften Artikel werden demnächst an deinen Briefkasten geliefert."
CatalogAnythingElse = "Kann ich noch etwas für dich tun?"
CatalogPurchaseClosetFull = "Dein Schrank ist voll. Du kannst diesen Artikel trotzdem kaufen, aber dann wirst du etwas aus deinem Schrank entfernen müssen, damit er dann hineinpasst.\n\nMöchtest du diesen Artikel immer noch kaufen? "
CatalogAcceptClosetFull = "Dein Schrank ist voll. Du musst hinein gehen und etwas aus deinem Schrank entfernen, damit dieser Artikel Platz hat. Erst dann kannst du ihn aus dem Briefkasten holen."
CatalogAcceptShirt = "Du trägst jetzt dein neues Oberteil. Was du vorher anhattest, wurde in deinen Schrank verschoben."
CatalogAcceptShorts = "Du trägst jetzt deine neuen Hosen. Was du vorher anhattest, wurde in deinen Schrank verschoben."
CatalogAcceptSkirt = "Du trägst jetzt deinen neuen Rock. Was du vorher anhattest, wurde in deinen Schrank verschoben."
CatalogAcceptPole = "Mit deiner neuen Angelrute kannst du jetzt größere Fische angeln gehen!"
CatalogAcceptPoleUnneeded = "Du hast schon eine bessere Angelrute als diese hier! "
CatalogPurchaseHouseFull = "Dein Haus ist voll. Du kannst diesen neuen Artikel trotzdem kaufen, aber dann wirst du etwas aus deinem Haus entfernen müssen, damit er dann hineinpasst.\n\nMöchtest du diesen Artikel immer noch kaufen?"
CatalogAcceptHouseFull = "Dein Haus ist voll. Du musst hinein gehen und etwas aus deinem Haus entfernen, damit dieser Artikel Platz hat. Erst dann kannst du ihn aus dem Briefkasten holen."
CatalogAcceptInAttic = "Dein neuer Artikel ist jetzt auf deinem Dachboden. Du kannst ihn ins Haus holen, indem du hinein gehst und auf die Schaltfläche 'Möbel rücken' klickst."
CatalogAcceptInAtticP = "Deine neuen Artikel sind jetzt auf deinem Dachboden. Du kannst sie in deinem Haus aufstellen, indem du hinein gehst und auf die Schaltfläche 'Möbel rücken' klickst."
CatalogPurchaseMailboxFull = "Dein Briefkasten ist voll! Du kannst diesen Artikel erst kaufen, wenn du ein paar Artikel aus deinem Briefkasten herausgenommen hast."
CatalogPurchaseOnOrderListFull = "Du hast zur Zeit zu viele Bestellungen auf deiner Liste. Du kannst erst dann weitere Artikel bestellen, wenn einige der bereits bestellten eingetroffen sind."
CatalogPurchaseGeneralError = "Der Artikel konnte wegen eines spielinternen Fehlers nicht gekauft werden: Fehlercode %s."
CatalogAcceptGeneralError = "Der Artikel konnte wegen eines spielinternen Fehlers nicht aus deinem Briefkasten entfernt werden: Fehlercode %s."

# don't translate yet
HDMoveFurnitureButton = "Möbel\nrücken"
HDStopMoveFurnitureButton = "Rücken\nfertig"
HDAtticPickerLabel = "Auf dem Dachboden"
HDInRoomPickerLabel = "Im Zimmer"
HDInTrashPickerLabel = "Im Müll"
HDDeletePickerLabel = "Löschen?"
HDInAtticLabel = "Dachboden"
HDInRoomLabel = "Zimmer"
HDInTrashLabel = "Müll"
HDToAtticLabel = "Auf den Dachboden\nstellen"
HDMoveLabel = "Rücken"
HDRotateCWLabel = "Drehung rechts"
HDRotateCCWLabel = "Drehung links"
HDReturnVerify = "Diesen Artikel wieder auf den Dachboden stellen?"
HDReturnFromTrashVerify = "Diesen Artikel aus dem Müll wieder auf den Dachboden stellen?"
HDDeleteItem = "OK anklicken, um diesen Artikel in den Müll zu befördern, oder Abbrechen, um ihn zu behalten."
HDNonDeletableItem = "Du kannst diese Teile nicht löschen!"
HDNonDeletableBank = "Du kannst deine Sparbüchse nicht löschen!"
HDNonDeletableCloset = "Du kannst deinen Kleiderschrank nicht löschen!"
HDNonDeletablePhone = "Du kannst dein Telefon nicht löschen!"
HDNonDeletableNotOwner = "Du kannst %s's Sachen nicht löschen!"
HDHouseFull = "Dein Haus ist voll. Du musst noch etwas aus deinem Haus oder von deinem Dachboden löschen, bevor du diesen Artikel wieder aus dem Müll holen kannst."

HDHelpDict = {
    "DoneMoving" : "Zimmer einrichten beenden.",
    "Attic" : "Liste der Gegenstände auf dem Dachboden anzeigen. Auf dem Dachboden werden Gegenstände aufbewährt, die nicht in deinem Zimmer sind.",
    "Room" : "Liste der Gegenstände im Zimmer anzeigen. Nützlich, um verlorene Gegenstände zu finden.",
    "Trash" : "Gegenstände im Müll anzeigen. Die ältesten Gegenstände werden nach einer Weile oder wenn der Müll überquillt, gelöscht.",
    "ZoomIn" : "Zimmeransicht vergrößern.",
    "ZoomOut" : "Zimmeransicht verkleinern.",
    "SendToAttic" : "Das aktuelle Möbelstück zum Lagern auf den Dachboden schicken.",
    "RotateLeft" : "Nach links.",
    "RotateRight" : "Nach rechts.",
    "DeleteEnter" : "Zum Löschen-Modus wechseln.",
    "DeleteExit" : "Löschen-Modus verlassen.",
    "FurnitureItemPanelDelete" : "%s in den Müll werfen.",
    "FurnitureItemPanelAttic" : "%s in das Zimmer stellen.",
    "FurnitureItemPanelRoom" : "%s wieder auf den Dachboden stellen.",
    "FurnitureItemPanelTrash" : "%s wieder auf den Dachboden stellen.",
    }



# don't translate yet
MessagePickerTitle = "Du hast zu viele Redewendungen. Um \n\"%s\"\n zu kaufen, musst du eine zum Entfernen auswählen:"
MessagePickerCancel = lCancel
MessageConfirmDelete = "Bist du sicher, dass du \"%s\" aus deinem Schnell-Chat-Menü entfernen möchtest?"


# don't translate yet
CatalogBuyText = "Kaufen"
CatalogOnOrderText = "Bestellt"
CatalogPurchasedText = "Schon\ngekauft"
CatalogPurchasedMaxText = "Schon\nMaximum gekauft"
CatalogVerifyPurchase = "%(item)s für %(price)s Jelly Beans kaufen?"
CatalogOnlyOnePurchase = "Du kannst nur jeweils einen dieser Artikel haben. Wenn du diesen kaufst, ersetzt er %(old)s.\n\nBist du sicher, dass du %(item)s für %(price)s Jelly Beans kaufen willst?"

# don't translate yet
CatalogExitButtonText = "Auflegen"
CatalogCurrentButtonText = "Zu aktuellen Artikeln"
CatalogPastButtonText = "Zu früheren Artikeln"

TutorialHQOfficerName = "Mitarbeiter Harry"

# NPCToons.py
NPCToonNames = {
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : "Einweiser-Ede",
    999 : "Toon-Schneider",
    1000 : "Toontown-Zentrale",
    20001 : Flippy,

    #
    # Toontown Central
    #
    
    # Toontown Central Playground

    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "Bankier Bob",
    2003 : "Professor Peter",
    2004 : "Schneiderin Flicka",
    2005 : "Bibliothekar Berti",
    2006 : "Angestellter Angelo",
    2011 : "Angestellte Angela",
    2007 : lHQOfficerM,
    2008 : lHQOfficerM,
    2009 : lHQOfficerF,
    2010 : lHQOfficerF,
    # NPCFisherman
    2012 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    2013 : "Angestellter Bimmel",
    2014 : "Angestellte Bammel",
    2015 : "Angestellter Bummel",

    # Silly Street
    2101 : "Zahnarzt Zacharias",
    2102 : "Sheriff Sherry",
    2103 : "Nies-Kitty",
    2104 : lHQOfficerM,
    2105 : lHQOfficerM,
    2106 : lHQOfficerF,
    2107 : lHQOfficerF,
    2108 : "Kanarienvogel Kohlengrube",
    2109 : "Barbera Blubber",
    2110 : "Eddi Kett",
    2111 : "Dancing Diego",
    2112 : "Dr. Hein",
    2113 : "Rollo der Erstaunliche",
    2114 : "Drees Rum",
    2115 : "Sheila Scherenschnitt",
    2116 : "Haumichblau MacDougal",
    2117 : "Mutter Eklig",
    2118 : "Kaspar Kasper",
    2119 : "Hanni Haha",
    2120 : "Professor Pünktchen",
    2121 : "Madam Gicker",
    2122 : "Harry Afferei",
    2123 : "Spamonia Biggels",
    2124 : "T.P. Rolle",
    2125 : "Paul Felz",
    2126 : "Professor Lachsalv",
    2127 : "Hellwig Heller",
    2128 : "Bert Bekloppt",
    2129 : "Frank Furter",
    2130 : "Schöna Spötter",
    2131 : "Federa Wedel",
    2132 : "Bartel Dös",
    2133 : "Dr. B. Geistert",
    2134 : "Stille Simone",
    2135 : "Maria",
    2136 : "Pit Prust",
    2137 : "Heikyung Glücklich",
    2138 : "Maldon",
    2139 : "Thoralf Tropf",
    2140 : "Fischer Billy",

    # Loopy Lane
    2201 : "Postmeister Peter",
    2202 : "Mira Spaß",
    2203 : lHQOfficerM,
    2204 : lHQOfficerM,
    2205 : lHQOfficerF,
    2206 : lHQOfficerF,
    2207 : "Willy Weisacker",
    2208 : "Kleb Endreim",
    2209 : "Chlodewig Gluckser",
    2210 : "Tee Hee",
    2211 : "Sally Spuck",
    2212 : "Sebastian Seltsam",
    2213 : "Alla Rad",
    2214 : "Felix Fleck",
    2215 : "Sid Selters",
    2216 : "Verigissmein Machsgut",
    2217 : "Hainer Fressdich",
    2218 : "Isja Lustig",
    2219 : "Chefkoch Schafskopf",
    2220 : "Edwin Eisenmann",
    2221 : "Hanna Haft",
    2222 : "Kurtzi Schluss",
    2223 : "Zelina Zerfetzdich",
    2224 : "Qualm-Ede",
    2225 : "Fischer Droopy",

    # Punchline Place
    2301 : "Dr. Verdreht",
    2302 : "Professor Krümmdich",
    2303 : "Schwester Stefanie",
    2304 : lHQOfficerM,
    2305 : lHQOfficerM,
    2306 : lHQOfficerF,
    2307 : lHQOfficerF,
    2308 : "Nancy Gas",
    2309 : "Blau Fleck",
    2311 : "Franz Schwellader",
    2312 : "Dr. Sensibel",
    2313 : "Lucy Hemdenklecks",
    2314 : "Schleuder-Ned",
    2315 : "Kauma Bröckchen",
    2316 : "Cindy Streusel",
    2318 : "Tony Maroni",
    2319 : "Beppo",
    2320 : "Alfredo Hartgekocht",
    2321 : "Fischer Punchy",

    #
    # Donald's Dock
    #
    
    # Donald's Dock Playground
    1001 : "Angestellter Willi",
    1002 : "Angestellter Billy",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "Jacko Buxehude",
    # NPCFisherman
    1008 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    1009 : "Angestellter Kleff",
    1010 : "Angestellte Schnurr",
    1011 : "Angestellter Pieps",

    # Barnacle Blvd.
    1101 : "Kalle Kiel",
    1102 : "Käpt'n Karl",
    1103 : "Frank Fischtran",
    1104 : "Doktor Weitblick",
    1105 : "Admiral Hook",
    1106 : "Frau Bleiche",
    1107 : "Herr Robiks",
    1108 : lHQOfficerM,
    1109 : lHQOfficerF,
    1110 : lHQOfficerM,
    1111 : lHQOfficerF,
    1112 : "Gary Gluckgluck",
    1113 : "Bärbel Backbord",
    1114 : "Charlie Schluck",
    1115 : "Quiselda Quittung, RA",
    1116 : "Bernikel-Bessie",
    1117 : "Käpt'n Igitt",
    1118 : "Hacker Haarig",
    1121 : "Linde Rinde",
    1122 : "Seebär Stan",
    1123 : "Elektra Egel",
    1124 : "Schlappo Docknagel",
    1125 : "Eileen Überbord",
    1126 : "Fischer Barney",

    # Seaweed Street
    1201 : "Bernikel-Barbara",
    1202 : "Adalbert",
    1203 : "Achim",
    1204 : "Sturmi See",
    1205 : lHQOfficerM,
    1206 : lHQOfficerF,
    1207 : lHQOfficerM,
    1208 : lHQOfficerF,
    1209 : "Professor Planke",
    1210 : "Geng Wei",
    1211 : "Wind Beutel",
    1212 : "Zeko Zungenbrenner",
    1213 : "Dante Delfin",
    1214 : "Stürmische Kate",
    1215 : "Unda Wassa",
    1216 : "Rod Rolle",
    1217 : "Meerlinde Tang",
    1218 : "Stiller Tim",
    1219 : "G. Strandet",
    1220 : "Karla Kanal",
    1221 : "Blasius McKee",
    1222 : "Chef Ahoi",
    1223 : "Cal Kalmar",
    1224 : "Aaltje Ritter",
    1225 : "Lobgott Lenzpumpe",
    1226 : "Hauke Ruck",
    1227 : "Cora Llenriff",
    1228 : "Fischer Reed",

    # Lighthouse Lane
    1301 : "Alice",
    1302 : "Mark",
    1303 : "Gerts",
    1304 : "Swetlana",
    1305 : lHQOfficerM,
    1306 : lHQOfficerF,
    1307 : lHQOfficerM,
    1308 : lHQOfficerF,
    1309 : "Gischt",
    1310 : "Max Made",
    1311 : "Florentina Schwipps",
    1312 : "Elmar Kiel",
    1313 : "Willie Woge",
    1314 : "Ralph Rostig",
    1315 : "Doktor Drift",
    1316 : "Wilma Wehr",
    1317 : "Paula Proporz",
    1318 : "Stephan Schlauchboot",
    1319 : "Trutz Trockendock",
    1320 : "Ted Stillsee",
    1321 : "Dina Docker",
    1322 : "Anka Kette",
    1323 : "Ned Stinktopf",
    1324 : "Perlchen Taucher",
    1325 : "Nobu Netz",
    1326 : "Felicia Chips",
    1327 : "Coralie Platsch",
    1328 : "Fred Flunder",
    1329 : "Shelly Seetang",
    1330 : "Porter Hohl",
    1331 : "Rudi Ruder",
    1332 : "Fischer Shane",

    #
    # The Brrrgh
    #

    # The Brrrgh Playground
    3001 : "Betty Friert",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "Angestellter Lenny",
    3007 : "Angestellte Penny",
    3008 : "Kord Hose",
    # NPCFisherman
    3009 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    3010 : "Angestellter Hoppel",
    3011 : "Angestellte Poppel",
    3012 : "Angestellter Moppel",

    # Walrus Way
    3101 : "Herr Krug",
    3102 : "Tante Frostbeule",
    3103 : "Fred",
    3104 : "Huta",
    3105 : "Feinfrost-Freddy",
    3106 : "Gert Gänseburger",
    3107 : "Patty Passport",
    3108 : "Schlitten-Schorsch",
    3109 : "Kate",
    3110 : "Hähnchenjung",
    3111 : "Großschnauz Gandalf",
    3112 : "Lil Altmann",
    3113 : "Hysterie-Harry",
    3114 : "Gerald der Gefährliche",
    3115 : lHQOfficerM,
    3116 : lHQOfficerF,
    3117 : lHQOfficerM,
    3118 : lHQOfficerM,
    3119 : "Gruselkurt",
    3120 : "Mike Mück",
    3121 : "Joe Shocker",
    3122 : "Rudi Rödel",
    3123 : "Frank Lloyd Ice",
    3124 : "Egon Eisberg",
    3125 : "Oberst Oberlecker",
    3126 : "Colestra Belle",
    3127 : "Ichvall Duvällst",
    3128 : "George Klebrig",
    3129 : "Bäckers Brigitte",
    3130 : "Sandy",
    3131 : "Lorenzo Faulus",
    3132 : "Brennda",
    3133 : "Dr. Stuntbild",
    3134 : "Salomon Salonlöwe",
    3135 : "Nele Durchweicht",
    3136 : "Gilda Glücklich",
    3137 : "Herr Frier",
    3138 : "Chefkoch Pfuschsuppe",
    3139 : "Oma Eisstrumpf",
    3140 : "Fischerin Lucille",

    # Sleet Street
    3201 : "Tante Arktis",
    3202 : "Schütti",
    3203 : "Walter",
    3204 : "Dr. K.-Ann Gutsehen",
    3205 : "Huckelberry Schlitzauge",
    3206 : "Vitalia Wucht",
    3207 : "Dr. Mummelgesicht",
    3208 : "Felix Mürrisch",
    3209 : "Guido Kichererbs",
    3210 : "Halbaffen-Sam",
    3211 : "Fanny Friert",
    3212 : "Fred Frost",
    3213 : lHQOfficerM,
    3214 : lHQOfficerF,
    3215 : lHQOfficerM,
    3216 : lHQOfficerM,
    3217 : "Schwitze-Peter",
    3218 : "Blanka Blau",
    3219 : "Tom Tandemfrost",
    3220 : "Herr Schneuz",
    3221 : "Nell Schnee",
    3222 : "Mindy Kaltwind",
    3223 : "Chappy",
    3224 : "Frieda Frostbiss",
    3225 : "Glatt Eis",
    3226 : "Nico Laus",
    3227 : "Sonny Strahl",
    3228 : "Wynn Stoß",
    3229 : "Hernie Gurt",
    3230 : "Glatzen-Günthi",
    3231 : "Eisbrecher",
    3232 : "Fischer Albert",

    #
    # Minnie's Melody Land
    #

    # Minnie's Melody Land Playground
    4001 : "Molly Molloy",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "Angestellte Fa",
    4007 : "Angestellter Ray",
    4008 : "Schneiderin Harmony",
    # NPCFisherman
    4009 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    4010 : "Angestellter Chris",
    4011 : "Angestellter Max",
    4012 : "Angestellte Mädchen für Alles",

    # Alto Ave.
    4101 : "Tom",
    4102 : "Fifi",
    4103 : "Dr. Karies",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "Quint",
    4109 : "Carlos",
    4110 : "Metra Gnom",
    4111 : "Tom Summ",
    4112 : "Tina",
    4113 : "Madam Benimm",
    4114 : "Der Verstimmte Erik",
    4115 : "Barbara Sevilla",
    4116 : "Piccolo",
    4117 : "Mandy Liehne",
    4118 : "Toilettenwart Tobi",
    4119 : "Moe Zart",
    4120 : "Viola Polster",
    4121 : "Gis Dur",
    4122 : "Minzie Bass",
    4123 : "Blitz-Ted",
    4124 : "Einar Tönig",
    4125 : "Melodie Weber",
    4126 : "Mel Canto",
    4127 : "Fulminante Füße",
    4128 : "Luciano Knüller",
    4129 : "Zenzi Zwiefacher",
    4130 : "Metal-Mike",
    4131 : "Abraham Armoire",
    4132 : "Louise Louise",
    4133 : "Scott Poplin",
    4134 : "Disco-Dave",
    4135 : "Beinhart Singvogel",
    4136 : "Patty Pause",
    4137 : "Tony Taub",
    4138 : "Violino Schlüssel",
    4139 : "Harmony Süßlich",
    4140 : "Ned Plump",
    4141 : "Fischer Jed",

    # Baritone Blvd.
    4201 : "Tina",
    4202 : "Barry",
    4203 : "Holz-Michel",
    4204 : lHQOfficerM,
    4205 : lHQOfficerF,
    4206 : lHQOfficerF,
    4207 : lHQOfficerF,
    4208 : "Hediheda",
    4209 : "Alma Abgedroschen",
    4211 : "Carl Concerto",
    4212 : "Detektiv Klagelied",
    4213 : "Tizia Tinnitus",
    4214 : "Fina Fußangel",
    4215 : "Veit Vibrato",
    4216 : "Gummy Pfeiffer",
    4217 : "Anton Schönherr",
    4218 : "Willma Pusten",
    4219 : "Abi Andante",
    4220 : "Kurt Finger",
    4221 : "Michi Madrigal",
    4222 : "Johann Doon",
    4223 : "Terry Taktstock",
    4224 : "Dschungel-Jim",
    4225 : "Zewa Zisch",
    4226 : "Herta Halslanger",
    4227 : "Die Stille Fancesca",
    4228 : "Susi Stimmt",
    4229 : "Belinda Blöd",
    4230 : "Julius Joculator",
    4231 : "Karla Quetschkommode",
    4232 : "Hedi Musi",
    4233 : "Karli Karpfen",
    4234 : "Johann Sträußchen",
    4235 : "Fischer Larry",

    # Tenor Terrace
    4301 : "Yuki",
    4302 : "Anna",
    4303 : "Leo",
    4304 : lHQOfficerM,
    4305 : lHQOfficerF,
    4306 : lHQOfficerF,
    4307 : lHQOfficerF,
    4308 : "Tabitha",
    4309 : "Marshall",
    4310 : "Martha Mopp",
    4311 : "Shanty Sänger",
    4312 : "Martin Satch",
    4313 : "Tauber Rudolf",
    4314 : "Dana Gander",
    4315 : "Undine Uhrwerk",
    4316 : "Tim Tango",
    4317 : "Dicky Zehe",
    4318 : "Bob Marlin",
    4319 : "Rinky Dink",
    4320 : "Cammy Coda",
    4321 : "Laurel Laute",
    4322 : "Randy Rhythmus",
    4323 : "Hanna Hogg",
    4324 : "Elli",
    4325 : "Bankier Bert",
    4326 : "Brenda Brett",
    4327 : "Flim Flam",
    4328 : "Wagner",
    4329 : "Nele Prompter",
    4330 : "Quentin",
    4331 : "Fabulo Costello",
    4332 : "Ziggy",
    4333 : "Harry",
    4334 : "Fast Freddie",
    4335 : "Fischer Walden",

    #
    # Daisy Gardens
    #
    
    # Daisy Gardens Playground
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "Angestellte Anemone",
    5006 : "Angestellter Camillo",
    5007 : "Rosa Blüte",
    # NPCFisherman
    5008 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    5009 : "Angestellte Ann Genehm",
    5010 : "Angestellter Tom A. Te",
    5011 : "Angestellter Johannes Beere",

    # Elm Street
    5101 : "Artie",
    5102 : "Susan",
    5103 : "Volker",
    5104 : "Schmetterding",
    5105 : "Jack",
    5106 : "Barbier Björn",
    5107 : "Postbote Felipe",
    5108 : "Gastwirtin Gastrinde",
    5109 : lHQOfficerM,
    5110 : lHQOfficerM,
    5111 : lHQOfficerF,
    5112 : lHQOfficerF,
    5113 : "Dr. Keim",
    5114 : "Welk",
    5115 : "Schleia Kraut",
    5116 : "Werner Vegetaro",
    5117 : "Früchtchen",
    5118 : "Pop Corn",
    5119 : "Grizzly Beer",
    5120 : "Gopher",
    5121 : "Erika Erbsschot",
    5122 : "Oswald Haufen",
    5123 : "Edda Ecker",
    5124 : "Pops Wund",
    5125 : "Pelikano Platsch",
    5126 : "Madam Mund",
    5127 : "Polly Pollen",
    5128 : "Susanna Setzling",
    5129 : "Fischerin Sally",

    # Maple Street
    5201 : "Hake",
    5202 : "Erika",
    5203 : "Lisa",
    5204 : "Bert",
    5205 : "Leopold Löwenzahn",
    5206 : "Rebert Grün",
    5207 : "Sofie Spritzer",
    5208 : "Silke Such",
    5209 : lHQOfficerM,
    5210 : lHQOfficerM,
    5211 : lHQOfficerF,
    5212 : lHQOfficerF,
    5213 : "Big Bauersmann",
    5214 : "Jukenda Ausschlag",
    5215 : "Karola Knolle",
    5216 : "Stinke-Jim",
    5217 : "Greg Gründaumen",
    5218 : "Rocky Rhododendron",
    5219 : "Lars Bizeps",
    5220 : "Lauf-Mascha",
    5221 : "Rosa Flamingo",
    5222 : "Heul-Suse",
    5223 : "Pfützen-Paule",
    5224 : "Onkel Landmann",
    5225 : "Pamela Pfanda",
    5226 : "Torf Moss",
    5227 : "Begonia Buddelbier",
    5228 : "Grabo Schmutzfink",
    5229 : "Fischerin Lily",

    # Oak street
    5301 : "Mitarbeiter der Zentrale",
    5302 : "Mitarbeiter der Zentrale",
    5303 : "Mitarbeiter der Zentrale",
    5304 : "Mitarbeiter der Zentrale",
    5305 : "Crystal",
    5306 : "B. Last",
    5307 : "Tiffany Lache",
    5308 : "Nelly Nörgel",
    5309 : "Ru Kola",
    5310 : "Timotheus",
    5311 : "Richterin McIntosh",
    5312 : "Bienhart",
    5313 : "Trainer Bemoost",
    5314 : "A. Meisenhügel",
    5315 : "Onkel Hollunder",
    5316 : "Onkel Keim",
    5317 : "Detektivin Lima",
    5318 : "Cäsar",
    5319 : "Rose",
    5320 : "April",
    5321 : "Professor Tausendschön",
    5322 : "Fischerin Rose",

    #
    # Dreamland
    #
    
    # Dreamland Playground
    9001 : "Susan Dämmerts",
    9002 : "Tom Tiefschlaf",
    9003 : "Dennis Dösig",
    9004 : lHQOfficerF,
    9005 : lHQOfficerF,
    9006 : lHQOfficerM,
    9007 : lHQOfficerM,
    9008 : "Angestellte Jill",
    9009 : "Angestellter Phil",
    9010 : "Abigail Abgetragen",
    # NPCFisherman
    9011 : "Tierhandlungs-\nAngestellter",
    # NPCPetClerks
    9012 : "Angestellte Sarah Bande",
    9013 : "Angestellte Anne Mone",
    9014 : "Angestellter Steve Mütterchen",

    # Lullaby Lane
    9101 : "Ed",
    9102 : "Big Mama",
    9103 : "PJ",
    9104 : "Süße Schlummerei",
    9105 : "Professor Gähn",
    9106 : "Maxim",
    9107 : "Kuschel",
    9108 : "Zwinky Zwirbel",
    9109 : "Traum-Daphne",
    9110 : "Kathy Minz",
    9111 : "Feler Suche",
    9112 : "Wiegenlied-Wiegand",
    9113 : "Uri Uhrwerk",
    9114 : "Lida Schatten",
    9115 : "Babyface MacDougal",
    9116 : "Der Mit Den Schafen Tanzt",
    9117 : "Sissy Feierabend",
    9118 : "Klara Nacht",
    9119 : "Steini",
    9120 : "Sarah Schlummer",
    9121 : "Zuzanna Zukurzdeck",
    9122 : "Dickie Augen",
    9123 : "Teddy Behr",
    9124 : "Nina Nachtlicht",
    9125 : "Dr. Unscharf",
    9126 : "Hella Wach",
    9127 : "Betty Bettdeck",
    9128 : "Hartmut Hammer",
    9129 : "Bertha Bettschwein",
    9130 : "Nathaniel Nachttopf",
    9131 : "Susan Siesta",
    9132 : lHQOfficerF,
    9133 : lHQOfficerF,
    9134 : lHQOfficerF,
    9135 : lHQOfficerF,
    9136 : "Fischer Taylor",

    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# These building titles are output from the DNA files
# Run ppython $TOONTOWN/src/dna/DNAPrintTitles.py to generate this list
# DO NOT EDIT THE ENTRIES HERE -- EDIT THE ORIGINAL DNA FILE
zone2TitleDict = {
    # titles for: phase_4/dna/toontown_central_sz.dna
    2513 : ("Toontown Rathaus", ""),
    2514 : ("Toontown Bank", ""),
    2516 : ("Toontown Schule", ""),
    2518 : ("Bibliothek Toontown", ""),
    2519 : ("Gag-Laden", ""),
    2520 : ("Toontown Zentrale", ""),
    2521 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("Zahnklempnerei Breites Lächeln", ""),
    2602 : ("", ""),
    2603 : ("Eingleis-Bergbau", ""),
    2604 : ("Quatschwasch & Reinigung", ""),
    2605 : ("Toontown Schilderfabrik", ""),
    2606 : ("", ""),
    2607 : ("Springende Bohnen", ""),
    2610 : ("Dr. Hein Faltspinsel", ""),
    2611 : ("", ""),
    2616 : ("Kostümverleih Falschbart", ""),
    2617 : ("Verrückte Stunts", ""),
    2618 : ("Drehrumbum", ""),
    2621 : ("Papierflugzeuge", ""),
    2624 : ("Lustige Rowdys", ""),
    2625 : ("Haus des Schlechten Geschmacks", ""),
    2626 : ("Kaspars Witzreparaturen", ""),
    2629 : ("Der Lachplatz", ""),
    2632 : ("Clownschule", ""),
    2633 : ("Hehe-Tee-Laden", ""),
    2638 : ("Toontown Spielhaus", ""),
    2639 : ("Affereien", ""),
    2643 : ("Dosenflaschen", ""),
    2644 : ("Unpraktische Witze", ""),
    2649 : ("Spiel- und Spaßladen", ""),
    2652 : ("", ""),
    2653 : ("", ""),
    2654 : ("Lachlektionen", ""),
    2655 : ("Spielgeld-Bausparkasse", ""),
    2656 : ("Gebrauchte Clownautos", ""),
    2657 : ("Franks Faxen", ""),
    2659 : ("Freude Schöner Spötterfunken", ""),
    2660 : ("Kitzelmaschinen", ""),
    2661 : ("Dösbartel", ""),
    2662 : ("Dr. B. Geistert", ""),
    2663 : ("Toontown Cinerama", ""),
    2664 : ("Die Lustigen Mimen", ""),
    2665 : ("Reisebüro Hin & Weg", ""),
    2666 : ("Lachtankstelle", ""),
    2667 : ("Glückliche Zeiten", ""),
    2669 : ("Maldons Hohle Ballone", ""),
    2670 : ("Suppengabeln", ""),
    2671 : ("", ""),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("Multiplex-Kino", ""),
    2705 : ("Weisackers Krachmacher", ""),
    2708 : ("Schleimleim", ""),
    2711 : ("Toontown Postamt", ""),
    2712 : ("Gluckscafé", ""),
    2713 : ("Café Lachtniezu", ""),
    2714 : ("Spinners Cineplex", ""),
    2716 : ("Suppen und Beknacktes", ""),
    2717 : ("Flaschendosen", ""),
    2720 : ("Autoreparaturen Zerschmeißdich", ""),
    2725 : ("", ""),
    2727 : ("Seltersflaschen und -dosen", ""),
    2728 : ("Verschwindcreme", ""),
    2729 : ("14-Karat-Goldfisch", ""),
    2730 : ("Nachrichten zum Aufrichten", ""),
    2731 : ("", ""),
    2732 : ("Spaghetti und Blödhammel", ""),
    2733 : ("Gußeisendrachen", ""),
    2734 : ("Saugnäpfe und -teller", ""),
    2735 : ("Die Kawummerei", ""),
    2739 : ("Kaputtlacher-Flickerei", ""),
    2740 : ("Gebrauchte Feuerwerkskörper", ""),
    2741 : ("", ""),
    2742 : ("", ""),
    2743 : ("Die fetzige Reinigung", ""),
    2744 : ("", ""),
    2747 : ("Sichtbare Tinte", ""),
    2748 : ("Du machst mir Spaß!", ""),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("Sofa-Rubbeldiekatz-Kissen", ""),
    2802 : ("Aufblasbare Abbruchkugeln", ""),
    2803 : ("Karneval Kid", ""),
    2804 : ("Dr. Verdreht, Chiropraktiker", ""),
    2805 : ("", ""),
    2809 : ("Sportstudio Schwitzeria", ""),
    2814 : ("Toontown Theater", ""),
    2818 : ("Die Fliegende Torte", ""),
    2821 : ("", ""),
    2822 : ("Gummiadler-Sandwiches", ""),
    2823 : ("Eiskrem zum fröhlichen Eisbechern", ""),
    2824 : ("Kinopalast Sparwitz", ""),
    2829 : ("Blödes Geschwafel", ""),
    2830 : ("Beppos Blödeleien", ""),
    2831 : ("Professor Krümmdichs Lachhaus", ""),
    2832 : ("", ""),
    2833 : ("", ""),
    2834 : ("Lachanfall Notaufnahme", ""),
    2836 : ("", ""),
    2837 : ("Hartmuts Haha-Seminare", ""),
    2839 : ("Ungenießbare Pasta", ""),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : ("Gag-Laden", ""),
    1507 : ("Toontown Zentrale", ""),
    1508 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("Gebrauchte Rettungswesten", ""),
    1604 : ("Regenjacken-Trockenreinigung", ""),
    1606 : ("Hooks Uhrenreparaturen", ""),
    1608 : ("Steuerbord & Backröhre", ""),
    1609 : ("Jedermanns Köder", ""),
    1612 : ("Heller und Kreuzer Bank", ""),
    1613 : ("Quitt Pro Quo, Rechtsanwälte", ""),
    1614 : ("Streich die Nägel Boutique", ""),
    1615 : ("Yacht nix, Leute!", ""),
    1616 : ("Schwarzbarts Schönheitssalon", ""),
    1617 : ("Land-In-Sicht-Optik", ""),
    1619 : ("Baumchirurgie & Piratung", ""),
    1620 : ("Von Bug bis Heck", ""),
    1621 : ("Verpeildeck-Sporthalle", ""),
    1622 : ("Schalter und Strömlinge Elektrogeschäft", ""),
    1624 : ("Hechtledersohlen-Schnellreparatur", ""),
    1626 : ("Edelfeine Bekleidung für festliche Anlässe", ""),
    1627 : ("Kalle Kiels Kaufrausch-Kompasshaus", ""),
    1628 : ("Kaviarstimmer", ""),
    1629 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1200.dna
    1701 : ("Kindergarten ", ""),
    1703 : ("China-Imbiss Wok 8, Achtern Strom", ""),
    1705 : ("Gaumensegelverkauf", ""),
    1706 : ("Erdnussbutter und Quallengelee", ""),
    1707 : ("Geschenkideen mit Riff", ""),
    1709 : ("Karavellbonbons und Marzipan", ""),
    1710 : ("Bernikel-Billigschnäppchen", ""),
    1711 : ("Tiefsee-Kneipe", ""),
    1712 : ("Sporthalle Volle Kraft", ""),
    1713 : ("Adalberts Smarter Seekarten-Markt", ""),
    1714 : ("Hol-Sie-Inn", ""),
    1716 : ("Meerjungfrau-Badebekleidung", ""),
    1717 : ("Sei Stiller Ozean-Ansichten", ""),
    1718 : ("Taxiservice Gestrandet", ""),
    1719 : ("Ducks Stilles Wasser GmbH", ""),
    1720 : ("Angelruten-Rudi", ""),
    1721 : ("Nautisch um jeden Preis", ""),
    1723 : ("Kalmars Seetang", ""),
    1724 : ("Ritters Aalverkauf", ""),
    1725 : ("Achims Fabelhaftes Seekrabben-Center", ""),
    1726 : ("Flüssiggersteladungen", ""),
    1727 : ("Dies Ruder Das", ""),
    1728 : ("Pfiffige Pfeilschwanzkrebse", ""),
    1729 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1300.dna
    1802 : ("Nautisch, aber nett", ""),
    1804 : ("Muckibude", ""),
    1805 : ("Frühstück aus der Köderbüchse", ""),
    1806 : ("Hutgeschäft Fesche Schlagseite", ""),
    1807 : ("Kiel-Deals", ""),
    1808 : ("Knot am Mann!", ""),
    1809 : ("Rosteimer", ""),
    1810 : ("Anker-Management", ""),
    1811 : ("Nicht zu überbooten!", ""),
    1813 : ("Anlegestellenberatung", ""),
    1814 : ("Ahoi-Shop", ""),
    1815 : ("Is' Was, Dock?", ""),
    1818 : ("Café Sieben Meere", ""),
    1819 : ("Dockers-Kneipe", ""),
    1820 : ("Haken, Schnur und Senkbleischmuckladen", ""),
    1821 : ("König Neptuns Konservenfabrik", ""),
    1823 : ("Speiselokal Muschelauflauf", ""),
    1824 : ("Hundepaddel", ""),
    1825 : ("Fischmarkt Absolut Makrelig", ""),
    1826 : ("Gerts Gewebeleinstek-Gewänder", ""),
    1828 : ("Alices Ballastpalast", ""),
    1829 : ("Möwenstatuenmarkt", ""),
    1830 : ("Verloren und Geflundern", ""),
    1831 : ("Klar Schiff!", ""),
    1832 : ("Marks Massiv-Marssegel-Markt", ""),
    1833 : ("Maßanzüge Ein Mann wie ein Mastbaum", ""),
    1834 : ("Jollig lächerlich!", ""),
    1835 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : ("Gag-Laden", ""),
    4504 : ("Toontown Zentrale", ""),
    4506 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Tom-Toms Trommeln", ""),
    4604 : ("Im Vier-Viertel-Takt", ""),
    4605 : ("Fifis Fiedeln", ""),
    4606 : ("Casa De Castanets", ""),
    4607 : ("Aparte Liedbekleidung", ""),
    4609 : ("Ta-Ke-Ti-Nasten-Pianotasten", ""),
    4610 : ("Bitte benimm' dich!", ""),
    4611 : ("Stimmgabeln und -löffel", ""),
    4612 : ("Dr. Karies Zahnarztpraxis", ""),
    4614 : ("Rasieren und Haarschneiden für ein Lied", ""),
    4615 : ("Piccolos Pizza", ""),
    4617 : ("Lustige Mandolinen", ""),
    4618 : ("Notendurft-Räume", ""),
    4619 : ("Mehr Punkte", ""),
    4622 : ("Kinnstütz-Kissen", ""),
    4623 : ("Entfernen von Kreuzen", ""),
    4625 : ("Zahnpasta in der Tuba", ""),
    4626 : ("Notationen", ""),
    4628 : ("Schlechte-Vorzeichen-Versicherung", ""),
    4629 : ("Buntlose Papierteller", ""),
    4630 : ("Musik ist unsere Lautstärke", ""),
    4631 : ("Canto mir helfen?", ""),
    4632 : ("Tanz rund um die Uhr-Macherei", ""),
    4635 : ("Tenor-Times", ""),
    4637 : ("Singende Schneiderei", ""),
    4638 : ("Hard Rock Shop", ""),
    4639 : ("Antiquitäten zum Viertel-Preis", ""),
    4641 : ("Blues News", ""),
    4642 : ("Die fetzige Reinigung", ""),
    4645 : ("Club 88", ""),
    4646 : ("", ""),
    4648 : ("Umzugsfirma Tonträger", ""),
    4649 : ("", ""),
    4652 : ("Große-Pause-Laden ", ""),
    4653 : ("", ""),
    4654 : ("Perfekte Ton-Dächer", ""),
    4655 : (" Kochschule des Notenschüssel-Kochs ", ""),
    4656 : ("", ""),
    4657 : ("Barbershop-Quartett", ""),
    4658 : ("Plumpsende Pianos", ""),
    4659 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("Die Schmalzwalzer-Tanzschule", ""),
    4702 : ("Holzmichelbedarf Singende Säge", ""),
    4703 : ("Ein Feines Händel für Gepäck", ""),
    4704 : ("Tinas Konzertinakonzerte", ""),
    4705 : ("Weder Klavier noch dort", ""),
    4707 : ("Dopplers Soundeffekt-Studio", ""),
    4709 : ("Hohes C Kletterbedarf", ""),
    4710 : ("Fahrschule Tempo, Kutscherpolka!", ""),
    4712 : ("Reparatur für punktierte Reifen", ""),
    4713 : ("Dissis Modische Herrenbekleidung", ""),
    4716 : ("Vier-Seiten-Mundharmonikas", ""),
    4717 : ("Auto-Rabattversicherung Schuld war der Andantere!", ""),
    4718 : ("Bachmaterial und anderes Küchenzubehör", ""),
    4719 : ("Madrigal Wohnmobile", ""),
    4720 : ("Der richtige Toon", ""),
    4722 : ("Ouvertüren-Untersuchungen", ""),
    4723 : ("Spielplatzbedarf Verspiel Dich", ""),
    4724 : ("Rauschen beim Anziehen und Plauschen", ""),
    4725 : ("Der Baritonbarbier", ""),
    4727 : ("Flechten von Stimmbändern", ""),
    4728 : ("Sing solo, wir hören Dich nicht", ""),
    4729 : ("Buchladen Leere Saite", ""),
    4730 : ("Törichte Texte", ""),
    4731 : ("Toon-Töne", ""),
    4732 : ("Theaterkompanie Etude Brute?", ""),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("Akkordeons, beim Eintreten nicht balgen!", ""),
    4736 : ("Hochzeitsplaner Auf in die Zitherwochen", ""),
    4737 : ("Harfenschoner", ""),
    4738 : ("Geschäft für Kunstmusik und Kunstgewerbe", ""),
    4739 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("Marshalls Plattenstapel", ""),
    4803 : ("Dienstmädchenschule Mezzoprächtig", ""),
    4804 : ("Mixolydische Schule für Barkeeper", ""),
    4807 : ("Entspann den Bach", ""),
    4809 : ("Ich Nix Verstanza!", ""),
    4812 : ("", ""),
    4817 : ("Tierhandlung Basstölpel", ""),
    4819 : ("Yukis Ukulelen", ""),
    4820 : ("", ""),
    4821 : ("Annas Kreuzfahrten", ""),
    4827 : ("Tabulatuhren", ""),
    4828 : ("Schumanns Schuhe für den Mann", ""),
    4829 : ("Pachelbels Kanonenkugeln", ""),
    4835 : ("Ursatz für Kool Katz", ""),
    4836 : ("Reggae-Regale", ""),
    4838 : ("Musikschule für Kazoologie", ""),
    4840 : ("Coda Pop musikalische Getränke", ""),
    4841 : ("Lyra, Lyra, nix berühra!", ""),
    4842 : ("Die Synkopenierung Unternehmung", ""),
    4843 : ("", ""),
    4844 : ("Con-Moto-Räder", ""),
    4845 : ("Katrins kunterbunte Klagelieder", ""),
    4848 : ("Massenhaft Noten Bausparkasse", ""),
    4849 : ("", ""),
    4850 : ("Pfandhaus Leihakkord", ""),
    4852 : ("Verblümtes Flötenvlies", ""),
    4853 : ("Leos Fender", ""),
    4854 : ("Wagners Wohlerdachte Violinen-Videos", ""),
    4855 : ("Das Tele-Caster-Netzwerk", ""),
    4856 : ("", ""),
    4862 : ("Quentins Quintessenzielle Quadrillen", ""),
    4867 : ("Mr. Costellos Fabulöse Cellos", ""),
    4868 : ("", ""),
    4870 : ("Ziggys Zoo der Zigeunermusik", ""),
    4871 : ("Harrys Haus der Harmonischen Humbucker", ""),
    4872 : ("Fast Freddies Verbundlose Fingergriffbretter", ""),
    4873 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : ("Gag-Laden", ""),
    5502 : ("Toontown Zentrale", ""),
    5503 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_8/dna/daisys_garden_5100.dna
    5601 : ("Kartoffelauge Sehkraftprüfung", ""),
    5602 : ("Artie Schocks Krawatten", ""),
    5603 : ("Da haben wir den Salat", ""),
    5604 : ("Schleierkraut Hochzeitsausstatter", ""),
    5605 : ("Vege-stabile Tische und Stühle", ""),
    5606 : ("Blüten", ""),
    5607 : ("Kompostamt", ""),
    5608 : ("Rock und Pop Corn", ""),
    5609 : ("Verbirkene Schätze", ""),
    5610 : ("Susan Matschauges Boxunterricht", ""),
    5611 : ("Gophers Gags", ""),
    5613 : ("Kahlschlag-Barbiere", ""),
    5615 : ("Volkers Vogelfutter", ""),
    5616 : ("Zaungasthaus", ""),
    5617 : ("Schmetterdings Schmetterlinge", ""),
    5618 : ("Kletten und Etiketten", ""),
    5619 : ("Jacks Bohnenstangen", ""),
    5620 : ("Gasthaus Ohne Harken und Ösen", ""),
    5621 : ("Buchweizen für Leseratten", ""),
    5622 : (" Drahtesel für Grünlandfahrer    ", ""),
    5623 : ("Vogel-Schaumbäder", ""),
    5624 : ("Mund Halten!", ""),
    5625 : ("Lass es Wein!", ""),
    5626 : ("Fichtennadelarbeiten", ""),
    5627 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Von Anfang bis Ernte", ""),
    5702 : ("Hakes Marken-Harken", ""),
    5703 : ("Foto-Erikas Kameraladen ", ""),
    5704 : ("Lisa Limones Gebrauchtwagen", ""),
    5705 : ("Giftefeu-Möbel", ""),
    5706 : ("14-Karotten-Juweliere", ""),
    5707 : ("Musikalische Früchtchen", ""),
    5708 : ("Reisebüro Wäre Weg", ""),
    5709 : ("Astroturf-Mäher", ""),
    5710 : ("Sportstudio Beerenstarke Jungs", ""),
    5711 : ("Glühstrumpfwaren", ""),
    5712 : ("Komische Statuen", ""),
    5713 : ("Lot und Leiden", ""),
    5714 : ("Springbrunnen-Seltersflaschen", ""),
    5715 : ("Scheunen-Nachrichten", ""),
    5716 : ("Pfandhaus Nimms oder Lassos", ""),
    5717 : ("Die Spritzblume", ""),
    5718 : ("Löwenzahn Exoten-Tierhandlung", ""),
    5719 : ("Privatdetektei Hermit die Wahrheit!", ""),
    5720 : ("Reben und Gecken Herrenbekleidung", ""),
    5721 : ("Rute 66 Speiserestaurant", ""),
    5725 : ("Gerste-, Hopfen- und Malzgeschäft", ""),
    5726 : ("Berts Dreck", ""),
    5727 : ("Vergissmeingeldnicht Bausparkasse", ""),
    5728 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : ("Toontown Zentrale ", ""),
    5804 : ("Glas mal Sehen", ""),
    5805 : ("Schneckenpost ", ""),
    5809 : ("Clownschule Tiefe Lache", ""),
    5810 : ("Männertreu ist hier neu ", ""),
    5811 : ("Gasthaus Freundliche Einsaladung ", ""),
    5815 : ("Graswurzel", ""),
    5817 : ("Äpfel und Birnen", ""),
    5819 : ("Flotte-Bienen-Jeans ", ""),
    5821 : ("Sporthalle Hauen und Flechten", ""),
    5826 : ("Ameisenzuchtzubehör ", ""),
    5827 : ("Hollunder Wunderangebote", ""),
    5828 : ("Faulpelz Möbel", ""),
    5830 : ("Spuck's Aus", ""),
    5833 : ("Die Salatbar", ""),
    5835 : ("Blumenbed & Breakfast", ""),
    5836 : ("Aprilregenwasserduschen", ""),
    5837 : ("Schule der blumigen Künste ", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Schlafliedbibliothek", ""),
    9503 : ("Die Dämmer-Bar", ""),
    9504 : ("Gag-Laden", ""),
    9505 : ("Toontown Zentrale", ""),
    9506 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Kuschel Dich 'Inn", ""),
    9602 : ("Vierzigmal Zwinkern zum Preis von zwanzig", ""),
    9604 : ("Eds Bettlaken", ""),
    9605 : ("Schlafliedgasse 323", ""),
    9607 : ("Big Mamas Bahama-Pyjama", ""),
    9608 : ("Katzenminz' für Katzenschlummer", ""),
    9609 : ("Tiefschlaf mit Schaf", ""),
    9613 : ("Die Uhrenreiniger", ""),
    9616 : ("Elektrofirma Licht Aus", ""),
    9617 : ("Schlafliedgasse 212", ""),
    9619 : ("Maximale Entspannung", ""),
    9620 : (" PJs Taxiservice", ""),
    9622 : ("Schlafens-Zeiteisen", ""),
    9625 : ("Schönheitssalon Roll Dich Ein", ""),
    9626 : ("Schlafliedgasse 818", ""),
    9627 : ("Das Schlaftipi", ""),
    9628 : ("Sis-Feierahmd-Kalender", ""),
    9629 : ("Schlafliedgasse 310", ""),
    9630 : ("Schlafen-wie-ein-Stein-Bruch", ""),
    9631 : ("Auszeit Uhrenreparaturen", ""),
    9633 : ("Traumland-Kinosaal", ""),
    9634 : ("Ratzematratze", ""),
    9636 : ("Schlaflos-Versicherung", ""),
    9639 : ("Haus des Winterschlafs", ""),
    9640 : ("Schlafliedgasse 805", ""),
    9642 : ("Säge-Schlummerbretter", ""),
    9643 : ("Augen-Zu Sehprüfung", ""),
    9644 : ("Kissenschlacht jede Nacht", ""),
    9645 : ("Gasthaus Zur Warmen Bettdecke", ""),
    9647 : ("Eisenwarenhandlung Mach dein Bett!", ""),
    9649 : ("Schnarchkapsel", ""),
    9650 : ("Schlafliedgasse 714", ""),
    9651 : ("Für Reicher und Schnarcher", ""),
    9652 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : ("Gag-Laden", ""),
    3508 : ("Toontown Zentrale", ""),
    3509 : ("Bekleidungsgeschäft", ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("Elektrofirma Nordlicht ", ""),
    3602 : ("Nordoster-Hüte", ""),
    3605 : ("", ""),
    3607 : ("Der Schnee-Weise", ""),
    3608 : ("Nichts zu Rodeln", ""),
    3610 : ("Mikes Mordsmäßiger Mukluk-Mart", ""),
    3611 : ("Herrn Krugs Schneepflugs", ""),
    3612 : ("Iglu Design", ""),
    3613 : ("Blitzeisgefahrräder", ""),
    3614 : ("Schneeflocken-Müsli-Firma", ""),
    3615 : ("Gefrosteter Kalter Hund", ""),
    3617 : ("Kaltluftballonfahrten", ""),
    3618 : ("Kein Schneema! Krisenmanagement", ""),
    3620 : ("Schiklinik", ""),
    3621 : ("Schmelz-Eisbar", ""),
    3622 : ("", ""),
    3623 : ("Umtoste Toastbrot-Firma", ""),
    3624 : ("Unter Null Sandwichladen", ""),
    3625 : ("Tante Frostbeules Heizkörper", ""),
    3627 : ("Bernhardinerhüttenclub", ""),
    3629 : ("Café Dicke Suppe", ""),
    3630 : ("(R)Eis(e)büro London-Frost, Frost-Frankreich", ""),
    3634 : ("Schaukelstuhllifte", ""),
    3635 : ("Gebrauchtes Feuerholz", ""),
    3636 : ("Gänsehaut für Jedermann", ""),
    3637 : ("Kates Skates", ""),
    3638 : ("Ins Ungewisse Schlitten", ""),
    3641 : ("Freds Geschätzte Schlittenbetten", ""),
    3642 : ("Sturmauge Optik", ""),
    3643 : ("Schneeballsaal", ""),
    3644 : ("Geschmolzene Eiswürfel", ""),
    3647 : ("Smokinggeschäft Heiterer Pinguin", ""),
    3648 : ("Pulverisiertes Trockeneis", ""),
    3649 : ("Hambrrrger", ""),
    3650 : ("Antarktische Antiquitäten", ""),
    3651 : ("Feinfrost-Freddys Gefrostete Frankfurter", ""),
    3653 : ("Kühlhaus-Schmuck", ""),
    3654 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3200.dna
    3702 : ("Winterlagerung", ""),
    3703 : ("", ""),
    3705 : ("Eisgefahrräder für zwei", ""),
    3706 : ("Schüttelfrost-Shakes", ""),
    3707 : ("Zu Hause ist es am schneesten", ""),
    3708 : ("Plutos Laden", ""),
    3710 : ("Speiserestaurant Fallende Grade ", ""),
    3711 : ("", ""),
    3712 : ("Schwimm mit dem Eisstrom", ""),
    3713 : ("Klappernde Zähne, Unter-Null-Zahnarzt", ""),
    3715 : ("Tante Arktis' Suppenküche", ""),
    3716 : ("Streusalz und -pfeffer", ""),
    3717 : ("Verschneen Sie, was ich meine??", ""),
    3718 : ("Designer-Schlauchseelen", ""),
    3719 : ("Eiswürfel am Stiel", ""),
    3721 : ("Schlitzauges Schlitten-Schnäppchen", ""),
    3722 : ("Schneehasen-Skigeschäft", ""),
    3723 : ("Schüttis Schneekugeln", ""),
    3724 : ("Die Bibberchronik", ""),
    3725 : ("Zu erschlittern", ""),
    3726 : ("Sonnenenergie-Bettdecken", ""),
    3728 : ("Müde Schneepflüge ", ""),
    3729 : ("", ""),
    3730 : ("Schneemänner An- und Verkauf", ""),
    3731 : ("Transportable Kamine", ""),
    3732 : ("Die Frostnase", ""),
    3734 : ("Sehkraftprüfungen Ich sehe was, was du nicht siehst ", ""),
    3735 : ("Polereiskappen", ""),
    3736 : ("Würfeleis zum Schleuderpreis", ""),
    3737 : ("Gasthof Bergab", ""),
    3738 : ("Hitze - Hol sie dir, solange sie heiß ist ", ""),
    3739 : ("", ""),
    }

# translate
# DistributedCloset.py
ClosetTimeoutMessage = "Entschuldige, deine\n Zeit ist abgelaufen."
ClosetNotOwnerMessage = "Das ist zwar nicht dein Schrank, aber du darfst die Sachen anprobieren."
ClosetPopupOK = lOK
ClosetPopupCancel = lCancel
ClosetDiscardButton = "Entfernen"
ClosetAreYouSureMessage = "Du hast einige Kleidungsstücke gelöscht. Möchtest du sie wirklich löschen?"
ClosetYes = lYes
ClosetNo = lNo
ClosetVerifyDelete = "%s wirklich löschen?"
ClosetShirt = "dieses Oberteil"
ClosetShorts = "diese Shorts"
ClosetSkirt = "diesen Rock"
ClosetDeleteShirt = "Oberteil\nlöschen"
ClosetDeleteShorts = "Shorts\nlöschen"
ClosetDeleteSkirt = "Rock\nlöschen"

# EstateLoader.py
EstateOwnerLeftMessage = "Leider ist der Eigentümer dieses Grundstückes nicht da. Du wirst in %s Sekunden zum Spielplatz zurück geschickt."
EstatePopupOK = lOK
EstateTeleportFailed = "Du konntest nicht nach Hause gehen. Versuche es nochmal!"
EstateTeleportFailedNotFriends = "Leider ist %s auf dem Grundstück eines Toons, mit dem du nicht befreundet bist."

# DistributedHouse.py
AvatarsHouse = "%s\n Haus"

# BankGui.py
BankGuiCancel = lCancel
BankGuiOk = lOK

# DistributedBank.py
DistributedBankNoOwner = "Entschuldige, das ist nicht deine Sparbüchse."
DistributedBankNotOwner = "Entschuldige, das ist nicht deine Sparbüchse."

# FishSellGui.py
FishGuiCancel = lCancel
FishGuiOk = "Alles verkaufen"
FishTankValue = "Hi, %(name)s! Du hast %(num)s Fische in deinem Eimer, die insgesamt %(value)s Jelly Beans wert sind. Möchtest du sie alle verkaufen?"

def GetPossesive(name):
    if name[-1:] == 's':
        possesive = name +" '"
    else:
        possesive = name + "s"
    return possesive

# PetTraits
# VERY_BAD, BAD, GOOD, VERY_GOOD
PetTrait2descriptions = {
    'hungerThreshold': ('Immer hungrig', 'Oft hungrig',
                        'Manchmal hungrig', 'Selten hungrig',),
    'boredomThreshold': ('Immer gelangweilt', 'Oft gelangweilt',
                         'Manchmal gelangweilt', 'Selten gelangweilt',),
    'angerThreshold': ('Immer knurrig', 'Oft knurrig',
                       'Manchmal knurrig', 'Selten knurrig'),
    'forgetfulness': ('Vergisst immer', 'Vergisst oft',
                      'Vergisst manchmal', 'Vergisst selten',),
    'excitementThreshold': ('Sehr ruhig', 'Ziemlich ruhig',
                            'Ziemlich erregbar', 'Sehr erregbar',),
    'sadnessThreshold': ('Immer traurig', 'Oft traurig',
                         'Manchmal traurig', 'Selten traurig',),
    'restlessnessThreshold': ('Immer unruhig', 'Oft unruhig',
                         'Manchmal unruhig', 'Selten unruhig',),
    'playfulnessThreshold': ('Selten verspielt', 'Manchmal verspielt',
                         'Oft verspielt', 'Immer verspielt',),
    'lonelinessThreshold': ('Immer einsam', 'Oft einsam',
                         'Manchmal einsam', 'Selten einsam',),
    'fatigueThreshold': ('Immer müde', 'Oft müde',
                         'Manchmal müde', 'Selten müde',),
    'confusionThreshold': ('Immer verwirrt', 'Oft verwirrt',
                         'Manchmal verwirrt', 'Selten verwirrt',),
    'surpriseThreshold': ('Immer überrascht', 'Oft überrascht',
                         'Manchmal überrascht', 'Selten überrascht',),
    'affectionThreshold': ('Selten Zärtlich', 'Manchmal zärtlich',
                         'Oft zärtlich', 'Immer zärtlich',),
    }
    

# end translate

# DistributedFireworkShow.py
FireworksInstructions = "Toontown-\nZentrale: Drücke die Taste 'Bild Hoch', um besser zu sehen."

FireworksJuly4Beginning = "Toontown-\nZentrale: Frohes Tag der deutschen Einheit Feuerwerk! Viel Spaß!"
FireworksJuly4Ending = "Toontown-\nZentrale: Wir hoffen, es hat dir gefallen!"
FireworksOctober31Beginning = "Toontown-\nZentrale: Happy Halloween!"
FireworksOctober31Ending = "Toontown-\nZentrale: Wir hoffen, es hat dir gefallen!"
FireworksNovember19Beginning = "Toontown-\nZentrale: Happy Birthday! Toontown wird 1 Jahr alt!"
FireworksNovember19Ending = "Toontown-\nZentrale: Wir hoffen, es hat dir gefallen!"
FireworksNewYearsEveBeginning = "Toontown-\nZentrale: Frohes neues Jahr! Viel Spaß beim Feuerwerk!"
FireworksNewYearsEveEnding = "Toontown-\nZentrale: Wir hoffen, es hat dir gefallen! Ein frohes Jahr 2006!"

# ToontownLoadingScreen.py

TIP_NONE = 0
TIP_GENERAL = 1
TIP_STREET = 2
TIP_MINIGAME = 3
TIP_COGHQ = 4
TIP_ESTATE = 5

# As of 8/5/03, ToonTips shouldn't exceed 130 characters in length
TipTitle = "TOON-TIPP:"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Wenn du deinen Spielstand bei den Toon-Aufgaben schnell kontrollieren willst, halte einfach die Taste 'Ende' gedrückt. ",
    "Wenn du deine Gag-Seite schnell kontrollieren willst, halte einfach Taste 'Pos1' gedrückt.",
    "Drücke die Taste 'F7', um deine Freunde-Liste zu öffnen.",
    "Drücke die Taste 'F8', um dein Sticker-Buch zu öffnen oder zu schließen. ",
    "Wenn du die Taste 'Bild Hoch' drückst, kannst du nach oben schauen, mit der Taste 'Bild Runter' nach unten.",
    "Wenn du springen willst, drücke die Taste 'Strg'.",
    "Drücke die Taste 'F9' um einen Screenshot, also eine Bildschirmansicht in deinem Toontown-Ordner auf deinem Computer zu speichern.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "You can exchange Secret Friend Codes with somebody you know outside Toontown to enable open chat with them in Toontown.",
    "Auf der Seite Optionen in deinem Sticker-Buch kannst du die Bildschirmauflösung ändern sowie Audio und andere Optionen einstellen und steuern.",
    "Probiere die Kleidung deines Freundes vor dem Schrank in seinem Haus an.",
    "Mit der Schaltfläche 'Nach Hause gehen' auf deinem Stadtplan kommst du zu deinem Haus.",
    "Immer, wenn du eine gelöste Toon-Aufgabe abgibst, werden deine Lach-Punkte automatisch aufgefüllt.",
    "Im Angebot von Bekleidungsgeschäften kannst du auch ohne Kleidermarke stöbern.",
    "Die Belohnung für manche Toon-Aufgaben ermöglicht dir, mehr Gags und Jelly Beans bei dir zu tragen.",
    "Du kannst bis zu 50 Freunde auf deiner Freunde-Liste haben.",
    "Einige Belohnungen für erledigte Toon-Aufgaben ermöglichen dir, dich mit Hilfe der Stadtplanseite im Sticker-Buch zu Spielplätzen zu teleportieren.",
    "Erhöhe deine Lach-Punkte auf den Spielplätzen, indem du Schätze wie Sterne und Eistüten sammelst.",
    "Wenn du nach einem harten Kampf schnell heilen musst, geh zu deinem Grundstück und sammle Eistüten.",
    "Mit der Tab-Taste kannst du zwischen verschiedenen Ansichten deines Toons wechseln.",
    "Manchmal werden verschiedene Toon-Aufgaben für dieselbe Belohnung angeboten. Vergleiche die Angebote!",
    "Das Spiel kann noch mehr Spaß machen, wenn du dir Freunde mit ähnlichen Toon-Aufgaben suchst.",
    "Du brauchst deinen Spielstand nicht zu speichern. Die Toontown-Server speichern fortwährend alle notwendigen Informationen.",
    "Du kannst anderen Toons etwas zuflüstern, indem du sie entweder anklickst oder sie in deiner Freunde-Liste auswählst.",
    "Manche Schnell-Chat-Wendungen zeigen die Gefühle deines Toons als Animation.",
    "Wenn die Gegend, in der du dich befindest, überfüllt ist, versuche den Bezirk zu wechseln. Gehe zur Bezirksseite in deinem Sticker-Buch und wähle einen anderen.",
    "Wenn du aktiv Gebäude rettest, erhältst du einen Stern in Bronze, Silber oder Gold über deinem Toon.",
    "Wenn du so viele Gebäude rettest, dass du einen Stern über deinem Kopf erhältst, findest du deinen Name wahrscheinlich auf der Tafel in eine Toontown-Zentrale.",
    "Gerettete Gebäude werden manchmal von den Bots zurückerobert. Wenn du deinen Stern behalten willst, musst du loszuziehen und weitere Gebäude retten!",
    "Die Namen deiner Geheimen Freunde erscheinen in Blau.",
    # Fishing
    "Versuche, alle Fische in Toontown zu fangen!",
    "In verschiedenen Teichen schwimmen verschiedene Fische. Versuche es überall! ",
    "Wenn dein Fischeimer voll ist, verkaufe deine Fische an die Tierhandlungs- Angestellten auf den Spielplätzen.",
    "Du kannst deine Fische an die Tierhandlungen oder an die Tierhandlungs-Angestellten verkaufen.",
    "Stärkere Angelruten fangen schwerere Fische, ihre Benutzung kostet aber mehr Jelly Beans. ",
    "Du kannst stärkere Angelruten im Kuhtalog kaufen.",
    "Schwerere Fische sind in der Tierhandlung mehr Jelly Beans wert.",
    "Seltene Fische sind in der Tierhandlung mehr Jelly Beans wert.",
    "Manchmal kann man beim Fischen Beutel mit Jelly Beans finden.",
    "Bei manchen Toon-Aufgaben muss man Dinge aus den Teichen fischen.",
    "In den Fischteichen auf den Spielplätzen gibt es andere Fische als in Teichen an Straßen.",
    "Manche Fische sind überaus selten. Angle weiter, bis du alle gesammelt hast!",
    "In dem Teich bei deinem Grundstück gibt es Fische, die man nur dort findet.",
    "Für jeweils 10 Arten, die du fängst, erhältst du eine Angeltrophäe!",
    "In deinem Sticker-Buch kannst du sehen, welche Fische du gesammelt hast.",
    "Bei manchen Angeltrophäen bekommst du eine Lach-Spritze.",
    "Angeln ist eine gute Möglichkeit, sich noch mehr Jelly Beans zu verdienen.",
    # Doodles
        "Nimm ein Doodle von der Tierhandlung auf!",
    "Tierhandlungen bekommen täglich neue Doodles zum Verkauf herein.",
    "Besuche täglich die Tierhandlungen um zu sehen, was sie an neuen Doodles da haben.",
    "In den verschiedenen Stadtteilen sind verschiedene Doodles im Angebot.",
    ),

  TIP_STREET : (
    "Es gibt vier Arten von Bots: Gesetzomaten, Monetomaten, Schachermaten und Chefomaten.",
    "Jeder Gag-Ablauf hat einen anderen Grad an Genauigkeit und schädlicher Wirkung.",
    "Sound-Gags wirken auf alle Bots, wecken aber geköderter Bots auf.",
    "Bots in einer strategischen Folge zu bekämpfen erhöht die Chancen, Kämpfe zu gewinnen.",
    "Mit dem Gag-Ablauf Aufheitern kannst du andere Toons im Kampf heilen.",
    "Während einer Bot-Invasion verdoppeln sich die Gag-Erfahrungspunkte!",
    "Mehrere Toons können sich zusammenschließen und denselben Gag-Ablauf im Kampf verwenden, um zusätzlichen Schaden bei den Bots anzurichten.",
    "Im Kampf werden Gags von oben nach untern in der Reihenfolge benutzt, wie sie auf dem Gag-Menü erscheinen.",
    "Die Reihe runder Lichter über den Aufzügen in Bot-Gebäuden zeigt an, wie viele Stockwerke es drinnen gibt.",
    "Klicke auf einen Bot, um Einzelheiten zu sehen.",
    "Die Verwendung von Gags höherer Level gegen Bots niedrigerer Level bringt keine Erfahrungspunkte ein.",
    "Gags, die Erfahrungspunkte einbringen, haben im Kampf auf dem Gag-Menü einen blauen Hintergrund.",
    "Die Gag-Erfahrung multipliziert sich beim Einsatz des Gags im Inneren von Gebäuden. Höhere Stockwerke haben höhere Multiplikationsfaktoren.",
    "Wenn ein Bot besiegt wird, wird er nach dem Kampf jedem Toon in dieser Runde angerechnet.",
    "Jede Straße in Toontown hat verschiedene Bot-Level und -Arten.",
    "Fußwege sind frei von Bots.",
    "Auf den Straßen geben die Seitentüren lustige Sprüche von sich, wenn man sich ihnen nähert.",
    "Manche Toon-Aufgaben sind ein Training für neue Gag-Abläufe. Du darfst nur sechs der sieben Gag-Tracks auswählen. Wähle daher sorgfältig!",
    "Fallen Stellen sind nur nützlich, wenn du oder deine Freunde sich beim Einsatz von Ködern im Kampf koordiniert.",
    "Bei Köder-Gags höherer Level ist ein Versagen weniger wahrscheinlich.",
    "Gags niedrigerer Level haben gegen Bots höherer Level eine geringere Genauigkeit.",
    "Bots können nicht angreifen, wenn sie im Kampf geködert wurden.",
    "Wenn du mit deinen Freunden ein Bot-Gebäude erobert hast, dann werdet ihr mit Porträts im geretteten Toon-Gebäude belohnt.",
    "Die Anwendung eines Tooning-Gags auf einen Toon mit vollem Lach-O-Meter bringt keine Tooning-Erfahrung.",
    "Bots sind kurz betäubt, wenn sie von einem Gag getroffen werden. Das erhöht die Trefferwahrscheinlichkeit für andere Gags in derselben Runde.",
    "Fallen lassen-Gags haben eine geringe Trefferwahrscheinlichkeit, aber die Genauigkeit wird erhöht, wenn Bots in derselben Runde zuerst von einem anderen Gag getroffen werden.",
    "Wenn du genügend Bots besiegt hast, verwende den 'Bot-Radar', indem du die Bot-Symbole auf der Bot-Galerie-Seite in deinem Sticker-Buch anklickst.",
    "Während eines Kampfes kannst du an den Strichen (-) und X-en sehen, welchen Bot deine Teamkameraden gerade angreifen.",
    "Im Kampf zeigt bei den Bots ein Licht ihren Gesundheitszustand an: Grün bedeutet gesund, Rot bedeutet fast zerstört.",
    "Es können maximal vier Toons auf einmal kämpfen.",
    "Auf der Straße treten Bots eher in einen Kampf gegen mehrere Toons als gegen nur einen Toon ein.",
    "Die beiden schwierigsten Bot jeder Art findet man nur innerhalb von Gebäuden.",
    "Fallen lassen-Gags wirken niemals gegen geköderte Bots.",
    "Bots greifen meist den Toon an, der ihnen den größten Schaden zugefügt hat.",
    "Sound-Gags richten bei geköderten Bots keinen zusätzlichen Schaden an.",
    "Wenn du allzu lange mit dem Angriff auf einen geköderten Bot wartest, wacht er wieder auf. Der Köder wirkt auf höheren Leveln länger.",
    "Jede Straße in Toontown hat einen Fischteich. Manche Straßen haben einzigartige Fische, die es nur dort gibt.",
    ),

  TIP_MINIGAME : (
    "Wenn du dein Jelly Beans-Glas aufgefüllt hast, werden alle Jelly Beans, die du bei den kleinen Spielen des Toon-Expresses gewinnst, automatisch in deine Sparbüchse in deinem Haus transferiert.",
    "Im Spiel 'Minnies Tanzstunde' kannst du anstelle der Maus auch die Pfeiltasten benutzen.",
    "Im Kanonen-Spiel kannst du die Kanone mit den Pfeiltasten bewegen und mit der 'Strg'- Taste abfeuern.",
    "Im Ringspiel werden Bonuspunkte vergeben, wenn die ganze Gruppe erfolgreich durch ihre Ringe schwimmt.",
    "Ein fehlerloser Durchlauf von Minnies Tanzstunde verdoppelt deine Punkte.",
    "Beim Tauziehen erhältst du mehr Jelly Beans, wenn du gegen einen stärkeren Bot spielst.",
    "Der Schwierigkeitsgrad der Spiele, die man mit dem Toon-Express erreicht, hängt von der Gegend ab: Toontown Mitte hat die leichtesten und Donalds Traumland die schwersten.",
    "Bestimmte Spiele, die man mit dem Toon-Express erreicht, kann man nur in einer Gruppe spielen.",
    ),

  TIP_COGHQ : (
    "Du musst deine Bot-Verkleidung vervollständigen, bevor du ein Chef-Gebäude betrittst.",
    "Du kannst auf Bot-Schläger springen, um sie vorübergehend außer Gefecht zu setzen.",
    "Sammle Bot-Verdienste, indem du Bots im Kampf besiegst.",
    "Bots höherer Level bringen mehr Verdienste ein.",
    "Wenn du genügend Bot-Verdienste für eine Beförderung gesammelt hast, suche den Schachermat-VP auf!",
    "Wenn du deine Bot-Verkleidung trägst, kannst du wie ein Bot reden. ",
    "Bis zu acht Toons können sich zusammenschließen, um gegen den Schachermat-VP zu kämpfen.",
    "Der Schachermat-VP sitzt ganz oben im Bot-Hauptquartier.",
    "Folge in Bot-Fabriken den Treppen nach oben, um zum Vorarbeiter zu gelangen.",
    "Jedes Mal, wenn du dich durch die Fabrik durchkämpfst, erhältst du ein Stück deiner Bot-Verkleidung.",
    "Den aktuellen Stand deiner Bot-Verkleidung kannst du in deinem Sticker-Buch nachsehen.",
    "Den aktuellen Stand deiner Verdienste kannst du auf der Verkleidungsseite in deinem Sticker-Buch nachsehen.",
    "Achte darauf, dass du eine volle Ladung Gags und einen vollem Lach-O-Meter hast, bevor du zum VP gehst.",
    "Wenn du befördert wirst, wird deine Bot-Verkleidung auf den aktuellen Stand gebracht. ",
    "Du musst den Vorarbeiter der Fabrik besiegen, um ein Stück der Bot-Verkleidung zu erbeuten.",
    ),
  TIP_ESTATE : (
    # Doodles
    "Doodles können manche Schnell-Chat-Sprüche verstehen. Probiere es aus!",
    "Mit dem \"Haustier\"-Menü im Schnell-Chat kannst du dein Doodle dazu bringen, Tricks zu zeigen.",
    "Mit Trainingslektionen aus Klarabellas Kuhtalog kannst du Doodles Tricks beibringen.",
    "Belohne dein Doodle für gezeigte Tricks.",
    "Wenn du einen Freund zu Hause besuchst, kommt dein Doodle immer mit.",
    "Gib deinem Doodle eine Jelly Bean, wenn es Hunger hat.",
    "Wenn du auf ein Doodle klickst, erscheint ein Menü, mit dem du es füttern, rufen und kraulen kannst.",
    "Doodles sind gern in Gesellschaft. Lade deine Freunde zum Spielen ein!",
    "Jedes Doodle hat eine einzigartige Persönlichkeit.",
    "Du kannst dein Doodle zur Tierhandlung zurückbringen und dir ein neues holen.",
    "Wenn ein Doodle einen Trick zeigt, werden die Toons in seiner Nähe geheilt.",
    "Je mehr die Doodle einen Trick üben, desto besser werden sie. Also schön weiterüben!",
    "Schwierigere Doodle-Tricks heilen Toons schneller.",
    "Erfahrene Doodles können mehr Tricks zeigen, bevor sie ermüden.",
    "Du findest in deiner Freunde-Liste eine Liste der Doodles in deiner Nähe.",
    # Furniture / Cattlelog
    "Kaufe Möbel aus Klarabellas Kuhtalog, um dein Haus einzurichten.",
    "In der Sparbüchse in deinem Haus sind zusätzliche Jelly Beans.",
    "Im Schrank in deinem Haus sind zusätzliche Kleidungsstücke.",
    "Gehe zum Haus deines Freundes und probiere seine Sachen an.",
    "Kaufe bessere Angelruten aus Klarabellas Kuhtalog.",
    "Kaufe größere Sparbüchsen aus Klarabellas Kuhtalog.",
    "Rufe Klarabella von dem Telefon in deinem Haus aus an.",
    "Klarabella hat einen größeren Schrank im Angebot, in den mehr Kleidungsstücke passen.",
    "Schaffe erst Platz in deinem Kleiderschrank, bevor du eine Kleidermarke einlöst.",
    "Klarabella hat alles im Angebot, was du brauchst, um dein Haus einzurichten.",
    "Schau in deinem Briefkasten nach, wenn du bei Klarabella bestellt hast.",
    "Die Lieferzeit für Kleidungsstücke aus Klarabellas Kuhtalog beträgt eine Stunde.",
    "Die Lieferzeit für Tapeten und Fußbodenbeläge aus Klarabellas Kuhtalog beträgt eine Stunde.",
    "Die Lieferzeit für Möbel aus Klarabellas Kuhtalog beträgt einen Tag.",
    "Bewahre zusätzliche Möbel auf dem Dachboden auf.",
    "Klarabella wird dich benachrichtigen, wenn ein neuer Kuhtalog da ist.", 
    "Klarabella wird dich benachrichtigen, wenn eine Kuhtalog-Lieferung eintrifft.",
    "Jede Woche werden neue Kuhtaloge geliefert.",
    "Halte im Kuhtalog Ausschau nach limitierten Urlaubsgegenständen.",
    "Wirf Möbel, die du nicht brauchst, in die Mülltonne.",
    # Fish
    "Manche Fische, zum Beispiel die Heilige Makrele, kommen auf Toon-Grundstücken häufiger vor.",
    # Misc
    "Du kannst mit dem Schnell-Chat deine Freunde auf dein Grundstück einladen.",
    "Wusstest du schon, dass die Farbe deines Hauses der Farbe deines Toon-Auswahl-Menüs entspricht?",
    ),
    }

FishGenusNames = {
    0 : "Ballonfisch",
    2 : "Katzenfisch",
    4 : "Clownfisch",
    6 : "Gefrierfisch",
    8 : "Seestern",
    10 : "Löchrige Makrele",
    12 : "Hundshai",
    14 : "Amoraal",
    16 : "Ammenhai",
    18 : "Königskrabbe",
    20 : "Mondfisch",
    22 : "Seepferdchen",
    24 : "Beckenhai",
    26 : "Bäracuda",
    28 : "Mordforelle",
    30 : "Kaviarstimmer",
    32 : "Geleequalle",
    34 : "Teufelsrochen",
    }

FishSpeciesNames = {
    0 : ( "Ballonfisch",
          "Heißluftballonfisch",
          "Wetterballonfisch",
          "Wasserballonfisch",
          "Roter Ballonfisch",
          ),
    2 : ( "Katzenfisch",
          "Siamesischer Katzenfisch",
          "Streunender Katzenfisch",
          "Tigerkatzenfisch",
          "Katerfisch",
          ),
    4 : ( "Clownfisch",
          "Trauriger Clownfisch",
          "Partyclownfisch",
          "Zirkusclownfisch",
          ),
    6 : ( "Gefrierfisch",
          ),
    8 : ( "Seestern",
          "Fünf-Stern",
          "Schlagersternchen",
          "Leuchtender Seestern",
          "Nord-Seestern",
          ),
    10 : ( "Löchrige Makrele",
           ),
    12 : ( "Hundshai",
           "Bulldoggenhai",
           "Hotdoghai",
           "Dalmatinerhai",
           "Welpenhai",
           ),
    14 : ( "Amoraal",
           "Elektrischer Amoraal",
           ),
    16 : ( "Ammenhai",
           "Hebammenhai",
           "Zündflammenhai",
           ),
    18 : ( "Königskrabbe",
           "Alaska-Königskrabbe",
           "Altkönigskrabbe",
           ),
    20 : ( "Mondfisch",
           "Vollmondfisch",
           "Halbmondfisch",
           "Neumondfisch",
           "Zunehmender Mondfisch",
           "Wonnemondfisch",
           ),
    22 : ( "Seepferdchen",
           "Schaukel-Seepferdchen",
           "Lipizzaner-Seepferdchen",
           "Araber-Seepferdchen",
           ),
    24 : ( "Beckenhai",
           "Planschbeckenhai",
           "Schwimmbeckenhai",
           "Olympiabeckenhai",
           ),
    26 : ( "Braunbäracuda",
           "Schwarzbäracuda",
           "Koalabäracuda",
           "Honigbäracuda",
           "Eisbäracuda",
           "Pandabäracuda",
           "Lippenbäracuda",
           "Grizzlybäracuda",
           ),
    28 : ( "Mordforelle",
           "Piratenkapitänforelle",
           "Gemeine Mordforelle",
           ),
    30 : ( "Klavierstint",
           "Konzertflügelstint",
           "Flügelstint",
           "Pianostint",
           "Mechanischer Klavierstint",
           ),
    32 : ( "Geleequalle",
           "Quittengeleequalle",
           "Grobe Geleequalle",
           "Erdbeergeleequalle",
           "Traubengeleequalle",
           ),
    34 : ( "Teufelsrochen",
           ),
    }

FishFirstNames = (
    "",
    "Angelo",
    "Arktis",
    "Baby",
    "Bermuda",
    "Big",
    "Dorsch",
    "Bläschen",
    "Meister",
    "Zuckerle",
    "Käpt'n",
    "Winzig",
    "Döbel",
    "Korall",
    "Doktor",
    "Körnchen",
    "Kaiser",
    "Beißer",
    "Dick",
    "Forelli",
    "Flipper",
    "Flunder",
    "Tüpfel",
    "Schatzi",
    "Hans",
    "König",
    "Kleini",
    "Wels",
    "Fräulein",
    "Herr",
    "Pippi",
    "Rosa",
    "Prinz",
    "Prinzessin",
    "Professor",
    "Schnapp",
    "Königin",
    "Regenbogen",
    "Rochen",
    "Rosi",
    "Ruben",
    "Salzer",
    "Scholle",
    "Sandy",
    "Schupp",
    "Haichen",
    "Sir",
    "Hüpfer",
    "Schleicher",
    "Schnapper",
    "Pünktchen",
    "Stachel",
    "Schecki",
    "Star",
    "Sugar",
    "Super",
    "Tiger",
    "Winzling",
    "Bartel",
    )

FishLastPrefixNames = (
    "",
    "Strand",
    "Schwarz",
    "Blau",
    "Keiler",
    "Bulle",
    "Katze",
    "Tief",
    "Doppel",
    "Ost",
    "Fantasie",
    "Flockig",
    "Flach",
    "Frisch",
    "Riesen",
    "Gold",
    "Golden",
    "Grau",
    "Grün",
    "Schwein",
    "Geplapper",
    "Gelee",
    "Dame",
    "Leder",
    "Zitrone",
    "Lang",
    "Nord",
    "Ozean",
    "Okto",
    "Öl",
    "Perle",
    "Bausch",
    "Rot",
    "Band",
    "Fluss",
    "Fels",
    "Rubin",
    "Ruder",
    "Salz",
    "Meer",
    "Silber",
    "Schnorchel",
    "Seezunge",
    "Süd",
    "Spitz",
    "Gischt",
    "Schwert",
    "Tiger",
    "Dreifach",
    "Tropisch",
    "Tunfisch",
    "Welle",
    "Schwach",
    "West",
    "Weiß",
    "Gelb",
    )

FishLastSuffixNames = (
    "",
    "ball",
    "flussbarsch",
    "bauch",
    "wanze ",
    "dieb",
    "butter",
    "klaue",
    "pfuscher",
    "krabbe",
    "unker",
    "trommel",
    "finne",
    "fisch",
    "platscher",
    "flosse",
    "geist",
    "grunzer",
    "kopf",
    "schnorchler",
    "springer",
    "makrele",
    "mond",
    "maul ",
    "barbe",
    "hals",
    "nase",
    "barsch",
    "grobian",
    "läufer",
    "segel",
    "hai",
    "muschel",
    "seide",
    "schleim",
    "schnäpper",
    "gestank",
    "schwanz",
    "kröte",
    "forelle",
    "wasser",
    )


CogPartNames = (
    "Linker Oberschenkel", "Linker Unterschenkel", "Linker Fuß",
    "Rechter Oberschenkel", "Rechter Unterschenkel", "Rechter Fuß",
    "Linke Schulter",  "Rechte Schulter", "Brust", "Gesundheitsmesser", "Becken",
    "Linker Oberarm",  "Linker Unterarm", "Linke Hand",
    "Rechter Oberarm", "Rechter Unterarm", "Rechte Hand",
    )

CogPartNamesSimple = (
    "Oberkörper",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "Haupteingang"
SellbotLegFactorySpecLobby = "Lobby"
SellbotLegFactorySpecLobbyHallway = "Korridor Lobby"
SellbotLegFactorySpecGearRoom = "Getrieberaum"
SellbotLegFactorySpecBoilerRoom = "Kesselraum"
SellbotLegFactorySpecEastCatwalk = "Östlicher Laufsteg"
SellbotLegFactorySpecPaintMixer = "Farbmischer"
SellbotLegFactorySpecPaintMixerStorageRoom = "Farbmischer-Lagerraum"
SellbotLegFactorySpecWestSiloCatwalk = "Westsilo-Laufsteg"
SellbotLegFactorySpecPipeRoom = "Rohrleitungsraum"
SellbotLegFactorySpecDuctRoom = "Leitungskanalraum"
SellbotLegFactorySpecSideEntrance = "Seiteneingang"
SellbotLegFactorySpecStomperAlley = "Stampfer-Gang"
SellbotLegFactorySpecLavaRoomFoyer = "Foyer Lava-Raum "
SellbotLegFactorySpecLavaRoom = "Lava-Raum"
SellbotLegFactorySpecLavaStorageRoom = "Lava-Lagerraum"
SellbotLegFactorySpecWestCatwalk = "Westlicher Laufsteg"
SellbotLegFactorySpecOilRoom = "Ölraum"
SellbotLegFactorySpecLookout = "Beobachtungsstand"
SellbotLegFactorySpecWarehouse = "Lagerhaus"
SellbotLegFactorySpecOilRoomHallway = "Korridor Ölraum"
SellbotLegFactorySpecEastSiloControlRoom = "Ostsilo-Kontrollraum"
SellbotLegFactorySpecWestSiloControlRoom = "Westsilo-Kontrollraum"
SellbotLegFactorySpecCenterSiloControlRoom = "Mittelsilo-Kontrollraum"
SellbotLegFactorySpecEastSilo = "Ostsilo"
SellbotLegFactorySpecWestSilo = "Westsilo"
SellbotLegFactorySpecCenterSilo = "Mittelsilo"
SellbotLegFactorySpecEastSiloCatwalk = "Ostsilo-Laufsteg"
SellbotLegFactorySpecWestElevatorShaft = "West-Aufzugs-Schacht"
SellbotLegFactorySpecEastElevatorShaft = "Ost-Aufzugs-Schacht"

#FISH BINGO
FishBingoBingo = "BINGO!"
FishBingoVictory = "GEWONNEN!"
FishBingoJackpot = "JACKPOT!"
FishBingoGameOver = "SPIEL VORBEI!"
FishBingoIntermission = "Pause\nendet in:"
FishBingoNextGame = "Nächstes Spiel\nbeginnt in:"
FishBingoTypeNormal = "Klassisch"
FishBingoTypeCorners = "Vier Ecken"
FishBingoTypeDiagonal = "Diagonalen"
FishBingoTypeThreeway = "Drei Wege"
FishBingoTypeBlockout = "BLOCKOUT!"
FishBingoStart = "Es ist Zeit für Fisch-Bingo! Gehe zum Spielen zu einem beliebigen freien Steg!"
FishBingoEnd = "Wir hoffen, es hat dir Spaß gemacht, Fisch-Bingo zu spielen."
FishBingoHelpMain = "Willkommen beim Toontown-Fisch-Bingo. Alle am Teich arbeiten beim Ausfüllen der Karte vor Ablauf der Zeit zusammen."
FishBingoHelpFlash = "Wenn du einen Fisch fängst, klicke auf eines der blinkenden Kästchen, um die Karte auszufüllen."
FishBingoHelpNormal = "Das ist eine klassische Bingo-Karte. Markiere eine beliebige Reihe senkrecht, waagerecht oder diagonal, um zu gewinnen."
FishBingoHelpDiagonals = "Markiere beide Diagonalen, um zu gewinnen."
FishBingoHelpCorners = "Eine leichte Ecken-Karte. Markiere alle vier Ecken, um zu gewinnen."
FishBingoHelpThreeway = "Drei Wege. Markiere beide Diagonalen und die mittlere Reihe, um zu gewinnen. Diese Aufgabe ist nicht leicht!"
FishBingoHelpBlockout = "Blockout! Markiere die gesamte Karte, um zu gewinnen. Du trittst gegen alle anderen Teiche an, um einen gewaltigen Jackpot zu gewinnen!"
FishBingoOfferToSellFish = "Dein Fischeimer ist voll. Möchtest du deine Fische verkaufen?"
FishBingoJackpot = "Gewinne %s Jelly Beans!"
