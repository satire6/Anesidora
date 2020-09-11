import string
import time
from toontown.toonbase.french.TTLocalizer_Property import *

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

# Product prefix
ProductPrefix = 'TT'

# common names
Mickey = "Mickey"
Minnie = "Minnie"
Donald = "Donald"
Daisy  = "Daisy"
Goofy  = "Dingo"
Pluto  = "Pluto"
Flippy = "Flippy"
Chip   = "Tic"
Dale   = "Tac"

# common locations
lTheBrrrgh = 'Le Glagla'
lDaisyGardens = 'Le Jardin de Daisy'
lDonaldsDock = "Quais Donald"
lDonaldsDreamland = "Le Pays des Rêves de Donald"
lMinniesMelodyland = "Le Pays Musical de Minnie"
lToontownCentral = 'Toontown Centre'
lToonHQ = 'QG des Toons'
lOutdoorZone = "Forêt de glands de Tic et Tac"
lGoofySpeedway = "Circuit Dingo"
lGolfZone = "Minigolf de Tic et Tac"

lGagShop = 'Gag Shop'
lClothingShop = 'En tant que magasin de marchandises sèches'
lPetShop = 'Pet Shop'

# common strings
lBack = 'Retour'
lCancel = 'Annuler'
lClose = 'Fermer'
lOK = 'OK'
lNext = 'Suivant'
lQuit = 'Quitter'
lYes = 'Oui'
lNo = 'Non'
lHQ = ''

lHQOfficerF = 'Officier QG'
lHQOfficerM = 'Officier QG'

MickeyMouse = "Mickey"

AIStartDefaultDistrict = "Idioville"

Cog  = "Cog"
Cogs = "Cogs"
ACog = "un Cog"
TheCogs = "les Cogs"
ASkeleton = "un Skelecog"
Skeleton = "Skelecog"
SkeletonP = "Skelecogs"
Av2Cog = "a Version 2.0 Cog"
v2Cog = "Version 2.0 Cog"
v2CogP = "Version 2.0 Cogs"
Foreman = "Contremaître de l'usine"
ForemanP = "Contremaîtres de l'usine"
AForeman = "un contremaître de l'usine"
CogVP = "Vice-\nPrésident " + Cog
CogVPs = "Vice-\nPrésidents Cogs"
ACogVP = "Un Vice-\nPrésident " + Cog
Supervisor = "Superviseur de la Fabrique à Sous"
SupervisorP = "Superviseurs de la Fabrique à Sous"
ASupervisor = "un Superviseur de la Fabrique à Sous"
CogCFO = Cog + " Vice-\nPrésident"
CogCFOs = "Vice-\nPrésidents Cog"
ACogCFO = ACog + " Vice-\nPrésident"

# AvatarDNA.py
Bossbot = "Chefbot"
Lawbot = "Loibot"
Cashbot = "Caissbot"
Sellbot = "Vendibot"
BossbotS = "un Chefbot"
LawbotS = "un Loibot"
CashbotS = "un Caissbot"
SellbotS = "un Vendibot"
BossbotP = "des Chefbots"
LawbotP = "des Loibots"
CashbotP = "des Caissbots"
SellbotP = "des Vendibots"
BossbotSkelS = "un Chefbot Skelecog"
LawbotSkelS = "un Loibot Skelecog"
CashbotSkelS = "un Caissbot Skelecog"
SellbotSkelS = "un Vendibot Skelecog"
BossbotSkelP = "des Chefbots Skelecogs"
LawbotSkelP = "des Loibots Skelecogs"
CashbotSkelP = "des Caissbots Skelecogs"
SellbotSkelP = "des Vendibots Skelecogs"

#lToonHQ = 'トゥーン'+lHQ #check
lBossbotHQ = Bossbot+lHQ
lLawbotHQ = Lawbot+lHQ
lCashbotHQ = Cashbot+lHQ
lSellbotHQ = Sellbot+lHQ

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("vers la",     "sur la",     "terrasse du Tourbillon"), # Tutorial
    1000  : ("vers le", "sur le", "Terrain de jeux"),
    1100  : ("vers le",     "sur le",     "Boulevard de la Bernache"),
    1200  : ("vers la",     "sur la",     "Rue des Récifs"),
    1300  : ("vers l'",     "sur l'",     "Allée des Marées"),
    2000  : ("vers le", "sur le", "Terrain de jeux"),
    2100  : ("vers la",     "sur la",     "Rue Béta"),
    2200  : ("vers l'",     "sur l'",     "Avenue des Fondus"),
    2300  : ("vers la",     "sur la",     "Place des Blagues"),
    3000  : ("vers le", "sur le", "Terrain de jeux"),
    3100  : ("vers le",     "sur le",     "Chemin du Marin"),
    3200  : ("vers la",     "sur la",     "Rue de la Neige fondue"),
    3300  : ("vers la",     "sur la",     "Place Polaire"),
    4000  : ("vers le", "sur le", "Terrain de jeux"),
    4100  : ("vers l'",     "sur l'",     "Avenue du Contralto"),
    4200  : ("vers le",     "sur le",     "Boulevard du Baryton"),
    4300  : ("vers la",     "sur la",     "Terrasse des Ténors"),
    5000  : ("vers le", "sur le", "Terrain de jeux"),
    5100  : ("vers la",     "sur la",     "Rue des Ormes"),
    5200  : ("vers la",     "sur la",     "Rue des Érables"),
    5300  : ("vers la",     "sur la",     "Rue du Chêne"),
    9000  : ("vers le", "sur le", "Terrain de jeux"),
    9100  : ("vers le",     "sur le",     "Boulevard de la Berceuse"),
    9200  : ("", "", "Place de la Couette"),
    10000 : ("vers le",     "au",     "QG Chefbot"),
    10100 : ("vers le", "dans le", "hall du QG des Chefbots"),
    10200 : ("à", "dans", "Le Clubhouse"),
    10500 : ("à", "dans", "Les trois premiers à l'avant"),
    10600 : ("à", "dans", "Les six du milieu"),
    10700 : ("à", "dans", "Les neuf du fond"),
    11000 : ("vers la", "sur la", "cour du QG Vendibot"),
    11100 : ("vers le", "dans le", "hall du QG Vendibot"),
    11200 : ("vers l'", "à l'", "usine Vendibot"),
    11500 : ("vers l'", "à l'", "usine Vendibot"),
    12000 : ("vers le",     "au",     "QG Caissbot"),
    12100 : ("vers le", "dans le", "hall du QG Caissbot"),
    12500 : ("", "", "Fabrique à Sous Caissbot"),
    12600 : ("", "", "Fabrique à Euros Caissbot"),
    12700 : ("", "", "Fabrique à Lingots Caissbot"),
    13000 : ("vers le",     "au",     "QG Loibot"),
    13100 : ("vers le", "dans le", "hall du QG Loibot"),
    13200 : ("vers le", "au", "hall du bureau du Procureur"),
    13300 : ("vers le", "au", "bureau Loibot A"),
    13400 : ("vers le", "au", "bureau Loibot B"),
    13500 : ("vers le", "au", "bureau Loibot C"),
    13600 : ("vers le", "au", "bureau Loibot D"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("vers les",     "sur les",     "Quais Donald")
ToontownCentral   = ("vers",     "à",     "Toontown centre")
TheBrrrgh         = ("vers",     "dans",     "le Glagla")
MinniesMelodyland = ("vers le",     "au",     "Pays musical de Minnie")
DaisyGardens      = ("vers les",     "au",     "Jardins de Daisy")
ConstructionZone  = ("vers la", "dans la", "Zone de construction")
OutdoorZone       = ("",     "",     lOutdoorZone)
FunnyFarm         = ("vers la", "dans la", "Ferme farfelue")
GoofySpeedway      = ("vers le",     "au",     "Circuit Dingo")
DonaldsDreamland  = ("vers le",     "au",     "Pays des rêves de Donald")
BossbotHQ         = ("vers le",     "dans le",     "QG des Chefbots")
SellbotHQ         = ("vers le",     "dans le",     "QG Vendibot")
CashbotHQ         = ("vers le",     "dans le",     "QG Caissbot")
LawbotHQ          = ("vers le",     "dans le",     "QG Loibot")
Tutorial          = ("vers les", "aux", "Travaux pratiques")
MyEstate          = ("vers",     "dans",     "ta maison")
WelcomeValley     = ("vers la",     "dans la",     "Bienvenue")
GolfZone          = ("à", "dans", lGolfZone)

Factory = 'Usine'
Headquarters = 'Quartiers généraux'
SellbotFrontEntrance = 'Entrée principale'
SellbotSideEntrance = 'Entrée latérale'
Office = 'Officier'

FactoryNames = {
    0 : "Maquette d'usine",
    11500 : 'Usine des Cogs Vendibots',
    13300 : 'Bureau des Cogs Loibot', #remove me JML
    }

FactoryTypeLeg = 'Jambe'
FactoryTypeArm = 'Bras'
FactoryTypeTorso = 'Torse'

MintFloorTitle = 'Étage %s'

# Quests.py
TheFish = "les poissons"
AFish = "un poisson"
Level = "niveau"
QuestsCompleteString = "Terminé"
QuestsNotChosenString = "Non choisi"
Period = "."

Laff = "Rigolpoints"

QuestInLocationString = " %(inPhrase)s %(location)s"

# _avName_ gets replaced with the avatar (player's) name
# _toNpcName_ gets replaced with the npc's name we are being sent to
# _where_ gets replaced with a description of where to find the npc, with a leading \a
QuestsDefaultGreeting = ("Bonjour, _avName_!",
                         "Ohé, _avName_!",
                         "Coucou, _avName_!",
                         "Eh, _avName_!",
                         "Bienvenue, _avName_!",
                         "Salut, _avName_!",
                         "Comment ça va, _avName_?",
                         "Quoi de neuf, _avName_?",
                         )
QuestsDefaultIncomplete = ("Comment est-ce que ce défi se présente, _avName_?",
                           "On dirait que tu as encore du travail à faire pour ce défi!",
                           "Continue à bien travailler, _avName_!",
                           "Essaie de finir ce défi. Je sais que tu peux le faire!",
                           "Essaie de terminer ce défi, nous comptons sur toi!",
                           "Continue à travailler sur ce défitoon!",
                           )
QuestsDefaultIncompleteProgress = ("Tu es au bon endroit, mais tu dois d'abord finir ton défitoon.",
                                   "Quand tu auras terminé ton défitoon, reviens ici.",
                                   "Reviens quand tu auras terminé ton défitoon.",
                                   )
QuestsDefaultIncompleteWrongNPC = ("Joli travail pour ce défitoon. Tu devrais aller voir _toNpcName_._where_",
                                   "On dirait que tu as presque fini ton défitoon. Va voir _toNpcName_._where_.",
                                   "Va voir _toNpcName_ pour finir ton défitoon._where_",
                                   )
QuestsDefaultComplete = ("Bon travail! Voilà ta récompense...",
                         "Super boulot, _avName_! Prends cette récompense...",
                         "Excellent boulot, _avName_! Voilà ta récompense...",
                         )
QuestsDefaultLeaving = ("Salut!",
                        "Au revoir!",
                        "Bon vent, _avName_!",
                        "À plus, _avName_!",
                        "Bonne chance!",
                        "Amuse-toi bien à Toontown!",
                        "À plus tard!",
                        )
QuestsDefaultReject = ("Bonjour.",
                       "Puis-je t'aider ?",
                       "Comment ça va?",
                       "Bien le bonjour.",
                       "Je suis un peu occupé là, _avName_.",
                       "Oui?",
                       "Salut, _avName_!",
                       "Bienvenue, _avName_!",
                       "Hé, _avName_! Comment ça va?",
                       # Game Hints
                       "Sais-tu que tu peux ouvrir ton journal de bord en appuyant sur la touche F8?",
                       "Tu peux utiliser ta carte pour te téléporter jusqu'au terrain de jeux!",
                       "Tu peux devenir ami(e) avec les autres joueurs en cliquant sur eux.",
                       "Tu peux en savoir plus sur un  " + Cog + " en cliquant sur lui.",
                       "Trouve des trésors sur les terrains de jeux pour remplir ton rigolmètre.",
                       "Les immeubles " + Cog + " sont dangereux! N'y va pas tout seul!",
                       "Lorsque tu perds un combat, les " + Cogs + " prennent tous tes gags.",
                       "Pour avoir plus de gags, joue aux jeux du tramway!",
                       "Tu peux accumuler des rigolpoints en effectuant des défitoons.",
                       "Chaque défitoon te vaudra une récompense.",
                       "Certaines récompenses te permettent d'avoir plus de gags.",
                       "Si tu gagnes un combat, ton défitoon est crédité pour chaque " + Cog + " vaincu.",
                       "Si tu regagnes un bâtiment " + Cog + ", retourne à l'intérieur pour recevoir un remerciement spécial de la part de son propriétaire!",
                       "Si tu appuies sur la touche \"page précédente\", tu peux regarder vers le haut!",
                       "Si tu appuies sur la touche de tabulation, tu peux voir différents points de vue de ce qui t'entoure!",
                       "Pour montrer à tes amis ce que tu penses, entre un '.' avant ta pensée.",
                       "Si un " + Cog + " est assommé, il lui est plus difficile d'éviter les objets qui tombent.",
                       "Chaque type de bâtiment " + Cog + " a un aspect différent.",
                       "Tu obtiens plus de récompenses d'habileté si tu vaincs des " + Cogs + " aux plus hauts étages des bâtiments."
                       )
QuestsDefaultTierNotDone = ("Bonjour, _avName_! Tu dois terminer tes défitoons commencés avant d'en obtenir un autre.",
                            "Salut! Tu dois terminer les défitoons sur lesquels tu es en train de travailler pour en obtenir un nouveau.",
                            "Ohé, _avName_! Pour que je puisse te donner un autre défitoon, tu dois finir ceux que tu as déjà.",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("J'ai entendu dire que _toNpcName_ te cherchait._where_",
                                 "Arrête-toi voir _toNpcName_ quand tu pourras._where_",
                                 "Va donc voir _toNpcName_ la prochaine fois que tu passes par là-bas._where_",
                                 "Si tu peux, arrête-toi dire bonjour à _toNpcName_._where_",
                                 "_toNpcName_ va te donner ton prochain défitoon._where_",
                                 )
# Quest dialog
QuestsLocationArticle = ""
def getLocalNum(num):
	if (num <=9):
		return str(num) + ""
	else:
		return str(num)
QuestsItemNameAndNum = "%(num)s %(name)s"

QuestsCogQuestProgress = "%(progress)s sur %(numCogs)s sont vaincus"
QuestsCogQuestHeadline = "RECHERCHE"
QuestsCogQuestSCStringS = "Je dois vaincre %(cogName)s%(cogLoc)s"
QuestsCogQuestSCStringP = "Je dois vaincre quelques %(cogName)s%(cogLoc)s"
QuestsCogQuestDefeat = "Tu dois vaincre %s"
QuestsCogQuestDefeatDesc = "%(numCogs)s %(cogName)s"

QuestsCogNewNewbieQuestObjective = "Aide un nouveau Toon à vaincre %s"
QuestsCogNewNewbieQuestCaption = "Aide un nouveau Toon qui a %d rigolpoints ou moins"
QuestsCogOldNewbieQuestObjective = "Aide un Toon avec %(laffPoints)d rigolpoints ou moins à vaincre %(objective)s"
QuestsCogOldNewbieQuestCaption = "Aide un Toon avec %d rigolpoints ou moins"
QuestsCogNewbieQuestAux = "Tu dois\nvaincre:"
QuestsNewbieQuestHeadline = "APPRENTI"

QuestsCogTrackQuestProgress = "%(progress)s sur %(numCogs)s sont vaincus"
QuestsCogTrackQuestHeadline = "RECHERCHE"
QuestsCogTrackQuestSCStringS = "Je dois vaincre %(cogText)s%(cogLoc)s"
QuestsCogTrackQuestSCStringP = "Je dois vaincre quelques %(cogText)s%(cogLoc)s."
QuestsCogTrackQuestDefeat = "Tu dois vaincre %s"
QuestsCogTrackDefeatDesc = "%(numCogs)s %(trackName)s"

QuestsCogLevelQuestProgress = "%(progress)s sur %(numCogs)s sont vaincus"
QuestsCogLevelQuestHeadline = "RECHERCHE"
QuestsCogLevelQuestDefeat = "Tu dois vaincre %s"
QuestsCogLevelQuestDesc = "un Cog de niveau %(level)s+"
QuestsCogLevelQuestDescC = "%(count)s Cogs de niveau %(level)s+"
QuestsCogLevelQuestDescI = "des Cogs de niveau %(level)s+"
QuestsCogLevelQuestSCString = "Je dois vaincre %(objective)s%(location)s."

QuestsBuildingQuestFloorNumbers = ('', 'deux+', 'trois+', 'quatre+', 'cinq+')
QuestsBuildingQuestBuilding = "Bâtiment"
QuestsBuildingQuestBuildings = "Bâtiments"
QuestsBuildingQuestHeadline = "VAINCRE"
QuestsBuildingQuestProgressString = "%(progress)s sur %(num)s sont vaincus"
QuestsBuildingQuestString = "Tu dois vaincre %s"
QuestsBuildingQuestSCString = "Je dois vaincre %(objective)s%(location)s."

QuestsBuildingQuestDesc = "un bâtiment %(type)s"
QuestsBuildingQuestDescF = "un bâtiment %(type)s de %(floors)s étages"
QuestsBuildingQuestDescC = "%(count)s bâtiments %(type)s "
QuestsBuildingQuestDescCF = "%(count)s bâtiments %(type)s de %(floors)s étages"
QuestsBuildingQuestDescI = "des bâtiments %(type)s"
QuestsBuildingQuestDescIF = "des bâtiments %(type)s de %(floors)s étages"

QuestFactoryQuestFactory = "Usine"
QuestsFactoryQuestFactories = "Usines"
QuestsFactoryQuestHeadline = "VAINCRE"
QuestsFactoryQuestProgressString = "%(progress)s sur%(num)s sont vaincus"
QuestsFactoryQuestString = "Tu dois vaincre %s"
QuestsFactoryQuestSCString = "Je dois vaincre %(objective)s%(location)s."

QuestsFactoryQuestDesc = "une usine %(type)s"
QuestsFactoryQuestDescC = "%(count)s usines %(type)s"
QuestsFactoryQuestDescI = "des usines %(type)s"

QuestMintQuestMint = "Fabrique à Sous"
QuestsMintQuestMints = "Fabriques à Sous"
QuestsMintQuestHeadline = "VAINCRE"
QuestsMintQuestProgressString = "%(progress)s de %(num)s vaincus"
QuestsMintQuestString = "Vaincre %s"
QuestsMintQuestSCString = "Je dois vaincre %(objective)s%(location)s."

QuestsMintQuestDesc = "une Fabrique à Sous Cog"
QuestsMintQuestDescC = "%(count)s Fabriques à Sous Cog"
QuestsMintQuestDescI = "des Fabriques à Sous Cog"

QuestsRescueQuestProgress = "%(progress)s sur %(numToons)s sont sauvés"
QuestsRescueQuestHeadline = "SAUVER"
QuestsRescueQuestSCStringS = "Je dois sauver un Toon%(toonLoc)s."
QuestsRescueQuestSCStringP = "Je dois sauver des Toons%(toonLoc)s."
QuestsRescueQuestRescue = "Tu dois sauver %s"
QuestsRescueQuestRescueDesc = "%(numToons)s Toons"
QuestsRescueQuestToonS = "un Toon"
QuestsRescueQuestToonP = "Toons"
QuestsRescueQuestAux = "Tu dois sauver:"

QuestsRescueNewNewbieQuestObjective = "Aide un nouveau Toon à sauver %s"
QuestsRescueOldNewbieQuestObjective = "Aide un Toon avec %(laffPoints)d rigolpoints ou moins à vaincre %(objective)s"

QuestCogPartQuestCogPart = "Pièce de costume de Cog"
QuestsCogPartQuestFactories = "Usines"
QuestsCogPartQuestHeadline = "RÉCUPÉRER"
QuestsCogPartQuestProgressString = "%(progress)s sur %(num)s sont récupérés"
QuestsCogPartQuestString = "Récupérer %s"
QuestsCogPartQuestSCString = "Je dois récupérer %(objective)s%(location)s."
QuestsCogPartQuestAux = "Tu dois récupérer:"

QuestsCogPartQuestDesc = "une pièce de costume de Cog"
QuestsCogPartQuestDescC = "%(count)s pièces de costume de Cog"
QuestsCogPartQuestDescI = "des pièces de costume de Cog"

QuestsCogPartNewNewbieQuestObjective = 'Aide un nouveau Toon à récupérer %s'
QuestsCogPartOldNewbieQuestObjective = 'Aide un Toon avec %(laffPoints)d rigolpoints ou moins à vaincre %(objective)s'

QuestsDeliverGagQuestProgress = "%(progress)s sur %(numGags)s sont livrés"
QuestsDeliverGagQuestHeadline = "LIVRER"
QuestsDeliverGagQuestToSCStringS = "Je dois livrer %(gagName)s."
QuestsDeliverGagQuestToSCStringP = "Je dois livrer des %(gagName)s."
QuestsDeliverGagQuestSCString = "Je dois faire une livraison."
QuestsDeliverGagQuestString = "Tu dois livrer %s"
QuestsDeliverGagQuestStringLong = "Tu dois livrer %s à _toNpcName_."
QuestsDeliverGagQuestInstructions = "Tu pourras acheter ce gag à la Boutique à gags une fois que tu en auras gagné le droit."

QuestsDeliverItemQuestProgress = ""
QuestsDeliverItemQuestHeadline = "LIVRER"
QuestsDeliverItemQuestSCString = "Je dois livrer %(article)s%(itemName)s."
QuestsDeliverItemQuestString = "Tu dois livrer %s"
QuestsDeliverItemQuestStringLong = "Tu dois livrer %s à _toNpcName_."

QuestsVisitQuestProgress = ""
QuestsVisitQuestHeadline = "VISITER"
QuestsVisitQuestStringShort = "Tu dois rendre visite"
QuestsVisitQuestStringLong = "Rends visite à _toNpcName_"
QuestsVisitQuestSeeSCString = "Je dois voir %s."

QuestsRecoverItemQuestProgress = "%(progress)s sur %(numItems)s sont repris"
QuestsRecoverItemQuestHeadline = "REPRENDRE"
QuestsRecoverItemQuestSeeHQSCString = "Je dois voir un officier du QG."
QuestsRecoverItemQuestReturnToHQSCString = "Je dois rendre %s à un officier du QG."
QuestsRecoverItemQuestReturnToSCString = "Je dois rendre %(item)s à %(npcName)s."
QuestsRecoverItemQuestGoToHQSCString = "Je dois aller à un QG des Toons."
QuestsRecoverItemQuestGoToPlaygroundSCString = "Je dois aller au terrain de jeux de %s."
QuestsRecoverItemQuestGoToStreetSCString = "Je dois aller %(to)s %(street)s dans %(hood)s."
QuestsRecoverItemQuestVisitBuildingSCString = "Je dois rendre visite à %s%s."
QuestsRecoverItemQuestWhereIsBuildingSCString = "Où est %s%s?"
QuestsRecoverItemQuestRecoverFromSCString = "Je dois reprendre %(item)s à %(holder)s%(loc)s."
QuestsRecoverItemQuestString = "Reprendre %(item)s à %(holder)s"
QuestsRecoverItemQuestHolderString = "%(level)s %(holder)d+ %(cogs)s"

QuestsTrackChoiceQuestHeadline = "CHOISIR"
QuestsTrackChoiceQuestSCString = "Je dois choisir entre %(trackA)s et %(trackB)s."
QuestsTrackChoiceQuestMaybeSCString = "Je devrais peut-être choisir %s."
QuestsTrackChoiceQuestString = "Choisis entre %(trackA)s et %(trackB)s."

QuestsFriendQuestHeadline = "AMI"
QuestsFriendQuestSCString = "Je dois trouver un(e) ami(e)."
QuestsFriendQuestString = "Trouve un(e) ami(e)."

QuestsMailboxQuestHeadline = "COURRIER"
QuestsMailboxQuestSCString = "Je dois vérifier mon courrier."
QuestsMailboxQuestString = "Vérifie ton courrier."

QuestsPhoneQuestHeadline = "CLARABELLE"
QuestsPhoneQuestSCString = "Je dois appeler Clarabelle."
QuestsPhoneQuestString = "Appelle Clarabelle."

QuestsFriendNewbieQuestString = " Trouve %d contacts de %d rigolpoints ou moins"
QuestsFriendNewbieQuestProgress = "%(progress)s sur %(numFriends)s sont trouvés."
QuestsFriendNewbieQuestObjective = "Deviens ami(e) avec %d nouveaux Toons."

QuestsTrolleyQuestHeadline = "TRAMWAY"
QuestsTrolleyQuestSCString = "Je dois faire un tour de tramway."
QuestsTrolleyQuestString = "Fais un tour de tramway."
QuestsTrolleyQuestStringShort = "Prends le tramway."

QuestsMinigameNewbieQuestString = "%d Mini jeux"
QuestsMinigameNewbieQuestProgress = "%(progress)s sur %(numMinigames)s ont été joués."
QuestsMinigameNewbieQuestObjective = "Jouer à %d mini jeux avec de nouveaux Toons"
QuestsMinigameNewbieQuestSCString = "Je dois jouer aux mini jeux avec de nouveaux Toons."
QuestsMinigameNewbieQuestCaption = "Aide un nouveau Toon qui a %d rigolpoints ou moins."
QuestsMinigameNewbieQuestAux = "Tu dois jouer:"

QuestsMaxHpReward = "Ta rigo-limite a été augmentée de %s."
QuestsMaxHpRewardPoster = "Récompense: Rigol-augmentation de %s point(s)"

QuestsMoneyRewardSingular = "Tu obtiens 1 bonbon."
QuestsMoneyRewardPlural = "Tu obtiens %s bonbons."
QuestsMoneyRewardPosterSingular = "Récompense: 1 bonbon"
QuestsMoneyRewardPosterPlural = "Récompense: %s bonbons"

QuestsMaxMoneyRewardSingular = "Tu peux maintenant avoir 1 bonbon."
QuestsMaxMoneyRewardPlural = "Tu peux maintenant avoir %s bonbons."
QuestsMaxMoneyRewardPosterSingular = "Récompense: Tu as 1 bonbon."
QuestsMaxMoneyRewardPosterPlural = "Récompense: Tu as %s bonbons."

QuestsMaxGagCarryReward = "Tu as un %(name)s. Tu peux maintenant avoir %(num)s gags."
QuestsMaxGagCarryRewardPoster = "Récompense: (%(num)s) %(name)s"

QuestsMaxQuestCarryReward = " Tu peux maintenant avoir %s défitoons."
QuestsMaxQuestCarryRewardPoster = "Récompense: Tu as %s défitoons"

QuestsTeleportReward = "Tu peux maintenant accéder par téléportation à %s."
QuestsTeleportRewardPoster = "Récompense: Accès par téléportation à %s"

QuestsTrackTrainingReward = "Tu peux maintenant t'entraîner pour les gags \"%s\"."
QuestsTrackTrainingRewardPoster = "Récompense: Entraînement aux gags"

QuestsTrackProgressReward = "Tu as maintenant l'image %(frameNum)s de l'animation de la série %(trackName)s."
QuestsTrackProgressRewardPoster = "Récompense: image %(frameNum)s de l'animation de la série \"%(trackName)s\""

QuestsTrackCompleteReward = "Tu peux maintenant avoir et utiliser des gags \"%s\"."
QuestsTrackCompleteRewardPoster = "Récompense: Entraînement final aux séries %s"

QuestsClothingTicketReward = "Tu peux changer de vêtements."
QuestsClothingTicketRewardPoster = "Récompense: Ticket d'habillement"

QuestsCheesyEffectRewardPoster = "Récompense: %s"

QuestsCogSuitPartReward = "Tu as maintenant une %(cogTrack)s %(part)s pièce de costume de Cog."
QuestsCogSuitPartRewardPoster = "Récompense: %(cogTrack)s %(part)s pièce"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "sur ce terrain de jeux"
QuestsStreetLocationThisStreet = "sur cette rue"
QuestsStreetLocationNamedPlayground = "sur le terrain de jeux de %s"
QuestsStreetLocationNamedStreet = "sur %(toStreetName)s dans %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "Le bâtiment de %s est appelé"
QuestsLocationBuildingVerb = "qui est"
QuestsLocationParagraph =  "\a %(building)s \"%(buildingName)s \"...\a...%(buildingVerb)s %(street)s."
QuestsGenericFinishSCString = "Je dois terminer un défitoon."

# MaxGagCarryReward names
QuestsMediumPouch = "Bourse moyenne"
QuestsLargePouch = "Grande bourse"
QuestsSmallBag = "Petit sac"
QuestsMediumBag = "Sac moyen"
QuestsLargeBag = "Grand sac"
QuestsSmallBackpack = "Petit sac à dos"
QuestsMediumBackpack = "Sac à dos moyen"
QuestsLargeBackpack = "Grand sac à dos"
QuestsItemDict = {
    1 : ["Paire de lunettes", "Paires de lunettes", "une"],
    2 : ["Clé", "Clés", "une"],
    3 : ["Tableau", "Tableaux", "un"],
    4 : ["Livre", "Livres", "un"],
    5 : ["Sucre d'orge", "Sucres d'orge", "un"],
    6 : ["Craie", "Craies", "une"],
    7 : ["Recette", "Recettes", "une"],
    8 : ["Note", "Notes", "une"],
    9 : ["Machine à calculer", "Machines à calculer", "une"],
    10 : ["Pneu de voiture de clown", "Pneus de voiture de clown", "un"],
    11 : ["Pompe à air", "Pompes à air", "une"],
    12 : ["Encre de seiche", "Encres de seiche", "de l'"],
    13 : ["Paquet", "Paquets", "un "],
    14 : ["Reçu de poisson doré", "Reçus de poissons dorés", "un "],
    15 : ["Poisson doré", "Poissons dorés", "un "],
    16 : ["Huile", "Huiles", "de l'"],
    17 : ["Graisse", "Graisses", "de la "],
    18 : ["Eau", "Eaux", "de l'"],
    19 : ["Rapport de pignons", "Rapports de pignons", "un "],
    20 : ["Brosse à Tableaux", "Brosses à Tableaux", "une "],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    1000 : ["Ticket d'habillement", "Tickets d'habillement", "un "],

    # Donald's Dock quest items
    2001 : ["Chambre à air", "Chambres à air", "une "],
    2002 : ["Ordonnance de monocle", "Ordonnances de monocles", "une "],
    2003 : ["Monture de monocle", "Montures de monocles", "une "],
    2004 : ["Monocle", "Monocles", "un "],
    2005 : ["Grande perruque blanche", "Grandes perruques blanches", "une "],
    2006 : ["Boisseau de lest", "Boisseaux de lest", "un "],
    2007 : ["Équipement de Cog", "Équipements de Cog", "un "],
    2008 : ["Carte marine", "Cartes marines", "une "],
    2009 : ["Manille crado", "Manilles crados", "un "],
    2010 : ["Manille propre", "Manilles propres", "un "],
    2011 : ["Ressort d'horloge", "Ressorts d'horloge", "un "],
    2012 : ["Contrepoids", "Contrepoids", "un "],

    # Minnie's Melodyland quest items
    4001 : ["Inventaire de Tina", "Inventaires de Tina", ""],
    4002 : ["Inventaire de Yuki", "Inventaires de Yuki", ""],
    4003 : ["Formulaire d'inventaire", "Formulaires d'inventaire", "un "],
    4004 : ["Inventaire de Fifi", "Inventaires de Fifi", ""],
    4005 : ["Ticket de Jack Bûcheron", "Tickets de Jack Bûcheron", ""],
    4006 : ["Ticket de Tabatha", "Tickets de Tabatha", ""],
    4007 : ["Ticket de Barry", "Tickets de Barry", ""],
    4008 : ["Castagnette ternie", "Castagnettes ternies", ""],
    4009 : ["Encre de seiche bleue", "Encre de seiche bleue", "de l'"],
    4010 : ["Castagnette brillante", "Castagnettes brillantes", "une "],
    4011 : ["Paroles de Léo", "Paroles de Léo", ""],

    # Daisy's Gardens quest items
    5001 : ["Cravate en soie", "Cravates en soie", "une "],
    5002 : ["Costume à rayures", "Costumes à rayures", "un "],
    5003 : ["Paire de ciseaux", "Paires de ciseaux", "une "],
    5004 : ["Carte postale", "Cartes postales", "une "],
    5005 : ["Crayon", "Crayons", "un "],
    5006 : ["Encrier", "Encriers", "un "],
    5007 : ["Bloc-notes", "Blocs-notes", "un "],
    5008 : ["Coffre de bureau", "Coffres de bureau", "un "],
    5009 : ["Sac de graines pour oiseaux", "Sacs de graines pour oiseaux", "un "],
    5010 : ["Pignon", "Pignons", "un "],
    5011 : ["Salade", "Salades", "une "],
    5012 : ["Clé du jardin de Daisy", "Clés du jardin de Daisy", "une "],
    5013 : ["Plans du QG Vendibot", "Plans du QG Vendibot", "des "],
    5014 : ["Note de service du QG Vendibot", "Notes de service du QG Vendibot", "une "],
    5015 : ["Note de service du QG Vendibot", "Notes de service du QG Vendibot", "une "],
    5016 : ["Note de service du QG Vendibot", "Notes de service du QG Vendibot", "une "],
    5017 : ["Note de service du QG Vendibot", "Notes de service du QG Vendibot", "une "],

    # The Brrrgh quests
    3001 : ["Ballon de foot", "Ballons de foot", "un "],
    3002 : ["Luge", "Luges", "une "],
    3003 : ["Glaçon", "Glaçons", "un "],
    3004 : ["Lettre d'amour", "Lettres d'amour", "une "],
    3005 : ["Teckel", "Teckels", "un "],
    3006 : ["Bague de fiançailles", "Bagues de fiançailles", "une "],
    3007 : ["Moustaches de sardine", "Moustaches de sardines", "des "],
    3008 : ["Potion calmante", "Potions calmantes", "une "],
    3009 : ["Dent cassée", "Dents cassées", "une "],
    3010 : ["Dent en or", "Dents en or", "une "],
    3011 : ["Pain aux pommes de pin", "Pains aux pommes de pin", "un "],
    3012 : ["Fromage grumeleux", "Fromages grumeleux", "du "],
    3013 : ["Cuillère ordinaire", "Cuillères ordinaires", "une "],
    3014 : ["Crapaud parlant", "Crapauds parlants", "un "],
    3015 : ["Cône de glace", "Cônes de glace", "un "],
    3016 : ["Poudre à perruque", "Poudres à perruques", "de la "],
    3017 : ["Canard en plastique", "Canards en plastique", "un "],
    3018 : ["Dés en peluche", "Dés en peluche", "des "],
    3019 : ["Micro", "Micros", "un "],
    3020 : ["Clavier électrique", "Claviers électriques", "un "],
    3021 : ["Chaussures à plate-forme", "Chaussures à plate-forme", "des "],
    3022 : ["Caviar", "Caviar", "du "],
    3023 : ["Poudre de maquillage", "Poudres de maquillage", "de la "],
    3024 : ["Fil", "Fil", "du " ],
    3025 : ["Aiguille à tricoter", "Aiguilles à tricoter", "une "],
    3026 : ["Alibi", "Alibis", "un "],
    3027 : ["Thermomètre extérieur", "Thermomètres extérieurs", "un "],

    #Dreamland Quests
    6001 : ["Plans du QG Caissbot ", "Plans du QG Caissbot ", "des "],
    6002 : ["Tige", "Tiges", "une "],
    6003 : ["Courroie", "Courroies", "une "],
    6004 : ["Tenaille", "Tenailles", "une "],
    6005 : ["Lampe de lecture", "Lampes de lecture", "une "],
    6006 : ["Cithare", "Cithares", "une "],
    6007 : ["Surfaceuse", "Surfaceuses", "une "],
    6008 : ["Coussin zèbre", "Coussins zèbre", "un "],
    6009 : ["Zinnia", "Zinnias", "quelques "],
    6010 : ["Disques de Zydeco", "Disques de Zydeco", "des "],
    6011 : ["Courgette", "Courgettes", "une "],
    6012 : ["Costume de zazou", "Costumes de zazou", "un "],

    #Dreamland+1 quests
    7001 : ["Lit ordinaire", "Lits ordinaires", "un "],
    7002 : ["Lit fantaisie", "Lits fantaisie", "un "],
    7003 : ["Dessus-de-lit bleu", "Dessus-de-lit bleus", "un "],
    7004 : ["Dessus-de-lit motif cachemire", "Dessus-de-lit motif cachemire", "un "],
    7005 : ["Oreillers", "Oreillers", "des "],
    7006 : ["Oreillers durs", "Oreillers durs", "des "],
    7007 : ["Pyjama", "Pyjamas", "un "],
    7008 : ["Grenouillère", "Grenouillères", "une "],
    7009 : ["Grenouillère puce", "Grenouillères puce", "une "],
    7010 : ["Grenouillère fuchsia", "Grenouillères fuchsia", "une "],
    7011 : ["Corail chou-fleur", "Coraux chou-fleur", "du "],
    7012 : ["Algue gluante", "Algues gluantes", "de l'"],
    7013 : ["Pilon", "Pilons", "un "],
    7014 : ["Pot de crème antirides", "Pots de crème antirides", "un "],
    }
QuestsHQOfficerFillin = lHQOfficerM
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = lToonHQ
QuestsHQLocationNameFillin = "dans n'importe quel quartier"

QuestsTailorFillin = "Tailleur" 
QuestsTailorWhereFillin = "" 
QuestsTailorBuildingNameFillin = "Boutique de prêt-à-porter" 
QuestsTailorLocationNameFillin = "dans n'importe quel quartier" 
QuestsTailorQuestSCString = "J'ai besoin de voir un tailleur."

QuestMovieQuestChoiceCancel = "Reviens plus tard si tu as besoin d'un défitoon! Salut!" 
QuestMovieTrackChoiceCancel  = "Reviens quand tu es prêt à te décider!! Salut!" 
QuestMovieQuestChoice = "Choisis un défitoon." 
QuestMovieTrackChoice = "Prêt à te décider ? Choisis une série, ou reviens plus tard." 

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
    QUEST : "Maintenant tu es prêt(e).\aSors et fais un tour avant de décider quelle série tu voudras choisir.\aChoisis bien, parce que c'est ta dernière série.\aQuand tu auras décidé, reviens me voir.",
    INCOMPLETE_PROGRESS : "Choisis bien.",
    INCOMPLETE_WRONG_NPC : "Choisis bien.",
    COMPLETE : "Choix très sage!",
    LEAVING : "Bonne chance. Reviens me voir quand tu as maîtrisé ta nouvelle habileté.",
    }

QuestDialog_3225 = {
    QUEST : "Oh, merci pour ta visite, _avName_!\aLes Cogs du quartier ont effrayé mon livreur.\aJe n'ai personne pour livrer cette salade à _toNpcName_!\aPeux-tu le faire pour moi? Merci beaucoup!_where_"
    }

QuestDialog_2910 = {
    QUEST : "Déjà de retour ?\aSuper travail avec le ressort.\aLe dernier article est un contrepoids.\aVa donc voir _toNpcName_ et ramène tout ce que tu peux._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "OK, maintenant je crois que nous sommes prêts pour quelque chose de plus compliqué.\aTu dois vaincre 3 Chefbots.",
           INCOMPLETE_PROGRESS : "Les "+ Cogs + " sont dans les rues, dans les tunnels.",
           INCOMPLETE_WRONG_NPC : "Bien, tu as battu ces Chefbots! Maintenant, va au quartier général des Toons pour recevoir ta récompense!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "OK, maintenant je crois que nous sommes prêts pour quelque chose de plus compliqué.\aTu dois vaincre 3 Loibots.",
           INCOMPLETE_PROGRESS : "Les "+ Cogs + " sont dans les rues, dans les tunnels.",
           INCOMPLETE_WRONG_NPC : "Bien, tu as battu ces Loibots! Maintenant, va au quartier général des Toons pour recevoir ta récompense!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    162 : {GREETING : "",
           QUEST : "OK, maintenant je crois que nous sommes prêts pour quelque chose de plus compliqué.\aTu dois vaincre 3 Caissbots.",
           INCOMPLETE_PROGRESS : "Les " + Cogs + " sont dans les rues, dans les tunnels.",
           INCOMPLETE_WRONG_NPC : "Bien, tu as battu ces Caissbots! Maintenant, va au quartier général des Toons pour recevoir ta récompense!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    163 : {GREETING : "",
           QUEST : "OK, maintenant je crois que nous sommes prêts pour quelque chose de plus compliqué.\aTu dois vaincre 3 Vendibots.",
           INCOMPLETE_PROGRESS : "Les " + Cogs + " sont dans les rues, dans les tunnels.",
           INCOMPLETE_WRONG_NPC : "Bien, tu as battu ces Vendibots! Maintenant, va au quartier général des Toons pour recevoir ta récompense!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    164 : {QUEST : "Il semble que tu as besoin de nouveaux gags.\aVa voir Flippy, peut-être pourra-t-il t'aider._where_" },
    165 : {QUEST : "Salut!\aOn dirait que tu as besoin de t'entraîner à utiliser tes gags.\aChaque fois que tu atteins un Cog avec l'un de tes gags, ton expérience augmente.\aQuand tu auras assez d'expérience, tu pourras utiliser un gag encore meilleur.\aVa t'entraîner à utiliser tes gags en battant 4 Cogs."},
    166 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Chefbots."},
    167 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Loibots."},
    168 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Vendibots."},
    169 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Caissbots."},
    170 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - il peut te donner des conseils avisés._where_" },
    171 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - il peut te donner des conseils avisés._where_" },
    172 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - elle peut te donner des conseils avisés._where_" },

    175 : {GREETING : "",
           QUEST : "Est-ce que tu savais que tu as une maison Toon à toi?\aClarabelle la vache s'occupe d'un catalogue par téléphone ou tu peux commander des meubles pour décorer ta maison.\aTu peux aussi y acheter des mots de Chat rapide, des vêtements et d'autres choses amusantes!\aJe vais dire à Clarabelle de t'envoyer ton premier catalogue maintenant.\aTu recevras un catalogue avec les nouveaux articles chaque semaine!\aRentre a la maison et appelle Clarabelle avec ton téléphone.",
           INCOMPLETE_PROGRESS : "Rentre à la maison et appelle Clarabelle avec ton téléphone.",
           COMPLETE : "J'espère que tu t'amuses en commandant des choses chez Clarabelle!\aJe viens tout juste de redécorer ma maison. Elle est toontastique!\aContinue à relever les défitoons pour avoir plus de récompenses!",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "Le lancer et l'éclaboussure sont super, mais tu auras besoin de plus de gags pour battre les Cogs de plus haut niveau.\aLorsque tu fais équipe avec d'autres Toons contre les Cogs, vous pouvez combiner vos attaques pour faire encore plus de dégâts.\aEssayez différentes combinaisons de gags pour voir ce qui marche le mieux.\aPour ta prochaine série, choisis entre tapage et toonique.\aTapage est particulier parce que lorsqu'il frappe, il endommage tous les Cogs.\aToonique te permet de soigner les autres Toons lors d'un combat.\aLorsque tu es prêt(e) à te décider, reviens ici faire ton choix.",
           INCOMPLETE_PROGRESS : "Déjà de retour ? OK, quel est ton choix?",
           INCOMPLETE_WRONG_NPC : "Pense bien à ta décision avant de choisir.",
           COMPLETE : "Bonne décision. Maintenant tu dois t'entraîner avant de pouvoir utiliser ces gags.\aTu dois effectuer une série de défitoons pour t'entraîner.\aChaque défi te donnera une seule image de ton animation d'attaque avec les gags.\aLorsque tu auras les 15 images, tu pourras faire le dernier défi d'entraînement qui te permettra d'utiliser tes nouveaux gags.\aTu peux suivre tes progrès dans ton journal de bord.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Va voir _toNpcName_ si tu veux parcourir la ville plus facilement._where_" },
    1040 : { QUEST : "Va voir _toNpcName_ si tu veux parcourir la ville plus facilement._where_" },
    1041 : { QUEST : "Salut! Qu'est-ce qui t'amène ?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes contacts en utilisant la liste d'contacts, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes contacts.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1042 : { QUEST : "Salut! Qu'est-ce qui t'amène ?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes contacts en utilisant la liste d'contacts, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes contacts.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1043 : { QUEST : "Salut! Qu'est-ce qui t'amène ?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes contacts en utilisant la liste d'contacts, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes contacts.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1044 : { QUEST : "Oh, merci de passer par ici. J'ai vraiment besoin d'aide.\aComme tu peux voir, je n'ai pas de clients.\aMon livre de recettes secret est perdu et personne ne vient plus dans mon restaurant.\aLa dernière fois que je l'ai vu, c'était avant que ces Cogs ne prennent mon bâtiment.\aEst-ce que tu peux m'aider à retrouver quatre de mes célèbres recettes?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as pu retrouver mes recettes?" },
    1045 : { QUEST : "Merci beaucoup!\aD'ici peu, j'aurai retrouvé toutes mes recettes et je pourrai rouvrir mon restaurant.\aOh, j'ai une petite note ici pour toi - quelque chose à propos de l'accès par téléportation ?\aC'est écrit, merci d'avoir aidé mon ami et d'avoir livré ceci au quartier général des Toons. \aEh bien, merci vraiment - au revoir!",
             LEAVING : "",
             COMPLETE : "Ah oui, c'est écrit que tu as été d'une grande aide à de braves gens de l'avenue des Fondus.\aEt que tu as besoin d'un accès par téléportation à Toontown centre.\aBon, c'est comme si c'était fait.\aMaintenant tu peux revenir au terrain de jeux par téléportation depuis presque partout dans Toontown.\aOuvre simplement ta carte et clique sur Toontown centre." },
    1046 : { QUEST : "Les Caissbots ont vraiment ennuyé la Caisse d'épargne Drôle d'argent.\aVa donc y faire un tour et vois si tu peux faire quelque chose._where_" },
    1047 : { QUEST : "Les Caissbots se sont introduits dans la banque et ont volé nos machines.\aS'il te plaît, reprends 5 machines à calculer aux Caissbots.\aPour t'éviter de faire des allers et retours, rapporte-les toutes en une seule fois.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu cherches encore des machines à calculer ?" },
    1048 : { QUEST : "Oh là là! >Merci d'avoir trouvé nos machines à calculer.\aHmm... Elles ont l'air un peu abîmées.\aDis donc, pourrais-tu les amener à _toNpcName_ à son magasin, \"Machines à chatouilles\", dans cette rue ?\aVoir si elle peut les réparer.",
             LEAVING : "", },
    1049 : { QUEST : "Qu'est-ce que c'est ? Des machines à calculer cassées?\aDes Caissbots dis-tu?\aBon, regardons ça...\aMouais, les pignons sont cassés, mais je n'en vends pas...\aTu sais ce qui pourrait marcher - des pignons de Cog, des gros, de gros Cogs...\aDes pignons de Cog de niveau 3 devraient faire l'affaire. J'en aurai besoin de 2 pour chaque machine, donc 10 au total.\aRapporte-les moi tous ensemble et je ferai la réparation!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Souviens-toi, j'ai besoin de 10 pignons pour réparer les machines." },
    1053 : { QUEST : "Ah oui, ça devrait bien faire l'affaire.\aTout est réparé maintenant, gratuitement.\aRapporte-les à Drôle d'argent, et dis-leur bonjour de ma part.",
             LEAVING : "",
             COMPLETE : "Toutes les machines à calculer sont réparées?\aJoli travail. Je crois bien que j'ai quelque chose par là pour te récompenser..." },
    1054 : { QUEST : "_toNpcName_ a besoin d'aide pour ses voitures de clown._where_" },
    1055 : { QUEST : "Bon sang! Je n'arrive pas à trouver les pneus de cette voiture de clown!\aTu crois que tu pourrais m'aider ?\aJe crois que Bob Fondu les a lancés dans la mare du terrain de jeux de Toontown centre.\aSi tu vas sur les pontons, de là tu peux essayer de repêcher les pneus.",
             GREETING : "Youhouu!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu as du mal à repêcher les 4 pneus?" },
    1056 : { QUEST : "Fanta-super-tastique! Maintenant je vais pouvoir remettre en marche cette vieille voiture de clown!\aHé, je croyais que j'avais une pompe par ici pour gonfler ces pneus...\aC'est peut-être _toNpcName_ qui l'a empruntée ?\aTu peux aller lui demander de me la rendre ?_where_",
             LEAVING : "" },
    1057 : { QUEST : "Salut!\aUne pompe à pneus tu dis?\aJe vais te dire - tu me nettoies les rues de quelques-uns de ces Cogs de haut niveau...\aEt je te donne la pompe à pneus.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "C'est tout ce que tu peux faire ?" },
    1058 : { QUEST : "Bon travail - je savais que tu pouvais le faire.\aVoilà la pompe. Je suis certain que_toNpcName_ sera content de la récupérer.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Youpiii! Maintenant ça va marcher!\aEt dis donc, merci de m'avoir aidé.\aTiens, prends ça." },
    1059 : { QUEST : "_toNpcName_ est à court de fournitures. Tu peux peut-être lui donner un coup de main ?_where_" },
    1060 : { QUEST : "Merci d'être passé par ici!\aCes Cogs ont volé mon encre je n'en ai presque plus.\a Pourrais-tu me pêcher de l'encre de seiche dans la mare ?\aTu n'as qu'à rester sur un ponton près de la mare pour pêcher.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "{Tu as des problèmes pour pêcher ?" },
    1061 : { QUEST : "Super - merci pour l'encre!\aTu sais quoi, et si tu nous débarrassais de quelques Gratte-papiers...\aJe ne serais plus en panne d'encre aussi rapidement.\aTu dois vaincre 6 Gratte-papiers dans Toontown centre pour avoir ta récompense.",
             LEAVING : "",
             COMPLETE : "Merci! Laisse-moi te récompenser pour ton aide.",
             INCOMPLETE_PROGRESS : "Je viens de voir encore d'autres Gratte-papiers." },
    1062 : { QUEST : "Super - merci pour l'encre!\aTu sais quoi, et si tu nous débarrassais de quelques Pique-au-sang...\aJe ne serais plus en panne d'encre aussi rapidement.\aTu dois vaincre 6 Pique-au-sang dans Toontown centre pour avoir ta récompense.",
             LEAVING : "",
             COMPLETE : "Merci! Laisse-moi te récompenser pour ton aide.",
             INCOMPLETE_PROGRESS : "Je viens de voir encore d'autres Pique-au-sang." },
    900 : { QUEST : "Je crois comprendre que_toNpcName_ a besoin d'aide avec un paquet._where_" },
    1063 : { QUEST : "Salut, merci d'être là.\aUn Cog a volé un paquet très important juste sous mon nez.\aPeux-tu le récupérer ? Je crois que c'était un Cog de niveau 3...\aDonc, tu dois vaincre des Cogs de niveau 3 jusqu'à ce que tu retrouves mon paquet.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein ?" },
    1067 : { QUEST : "C'est ça, très bien!\aOh, l'adresse est toute tachée...\aTout ce que j'arrive à lire, c'est Docteur... - le reste est brouillé.\aC'est peut-être pour_toNpcName_? Peux-tu lui porter ?_where_",
             LEAVING : "" },
    1068 : { QUEST : "Je n'attendais pas de paquet. C'est peut-être pour le Dr E. Phorique ?\aMon assistant doit aller le voir aujourd'hui, je me charge de lui remettre.\aEn attendant, est-ce que tu voudrais bien débarrasser ma rue de quelques Cogs?\aTu dois vaincre 10 Cogs dans Toontown centre.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mon assistant n'est pas encore revenu." },
    1069 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Caissbot l'a volé à mon assistant alors qu'il revenait.\aPourrais-tu essayer de le récupérer ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein ?" },
    1070 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Vendibot l'a volé à mon assistant alors qu'il revenait.\aJe suis désolé, mais il va falloir que tu retrouves ce Vendibot pour le récupérer.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein ?" },
    1071 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Chefbot l'a volé à mon assistant alors qu'il revenait.\aPourrais-tu essayer de le récupérer ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein ?" },
    1072 : { QUEST : "Super - tu l'as retrouvé!\aTu devrais peut-être essayer _toNpcName_, cela pourrait être pour lui._where_",
             LEAVING : "" },
    1073 : { QUEST : "Oh, merci de m'avoir apporté mes paquets.\aJuste une seconde, j'en attendais deux. Pourrais-tu vérifier avec _toNpcName_ voir s'il a l'autre ?",
             INCOMPLETE : "Est-ce que tu as trouvé mon autre paquet ?",
             LEAVING : "" },
    1074 : { QUEST : "Il a dit qu'il y avait un autre paquet ? Les Cogs l'ont peut-être aussi volé.\aTu dois vaincre des Cogs jusqu'à ce que tu trouves le second paquet.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein ?" },
    1075 : { QUEST : "Finalement je crois qu'il y avait un second paquet!\aVa vite le porter à _toNpcName_ avec mes excuses.",
             COMPLETE : "Eh, mon paquet est là!\aPuisque tu es un Toon aussi serviable, cela devrait aider.",
             LEAVING : "" },
    1076 : { QUEST : "Il y a un problème au Ornithorynques 14 carats.\a_toNpcName_ serait sans doute content d'avoir de l'aide._where_" },
    1077 : { QUEST : "Merci d'être venu - les Cogs ont volé tous mes poissons dorés.\aJe crois que les Cogs veulent les vendre pour se faire de l'argent facilement.\aCes 5 poissons ont été mes seuls compagnons dans cette petite boutique depuis tant d'années...\aSi tu pouvais me les retrouver, je t'en serais vraiment reconnaissant.\aJe suis certain qu'un des Cogs a mes poissons.\aTu dois vaincre des Cogs jusqu'à ce que tu trouves mes poissons dorés.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "S'il te plaît, ramène-moi mes poissons." },
    1078 : { QUEST : "Oh, tu as mes poissons!\aEh? Qu'est-ce que c'est que ça?\aAah, ce sont bien les Cogs, après tout.\aJe ne comprends rien à ce reçu. Peux-tu l'emmener à _toNpcName_ voir s'il peut le lire ?_where_",
             INCOMPLETE : "Qu'est-ce que _toNpcName_ a dit à propos du reçu?",
             LEAVING : "" },
    1079 : { QUEST : "Mmm, laisse-moi voir ce reçu.\a...Ah oui, il dit qu'un poisson doré a été vendu à un Laquaistic.\aÇa n'a pas l'air de dire ce qui est arrivé aux 4 autres poissons.\aTu devrais peut-être essayer de trouver ce Laquaistic.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je ne crois pas que je puisse t'aider à grand-chose d'autre.\aPourquoi n'essaies-tu pas de trouver ce poisson doré?" },
    1092 : { QUEST : "Mmm, laisse-moi voir ce reçu.\a...Ah oui, il dit qu'un poisson doré a été vendu à un Gardoseille.\aÇa n'a pas l'air de dire ce qui est arrivé aux 4 autres poissons.\aTu devrais peut-être essayer de trouver ce Gardoseille.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je ne crois pas que je puisse t'aider à grand-chose d'autre.\aPourquoi n'essaies-tu pas de trouver ce poisson doré?" },
    1080 : { QUEST : "Oh, Dieu merci! Tu as trouvé Oscar - c'est mon préféré.\aQu'est-ce que c'est, Oscar ? Hein, hein...ils ont quoi? ... Ils sont ?\aOscar dit que les 4 autres se sont échappés dans la mare du terrain de jeux.\aPeux-tu aller me les chercher ?\aTu n'as qu'à les pêcher dans la mare.",
             LEAVING : "",
             COMPLETE : "Ahh, je suis si content! Avoir retrouvé mes petits camarades!\aTu mérites une belle récompense pour cela!",
             INCOMPLETE_PROGRESS : "Tu as des problèmes pour trouver ces poissons?" },
    1081 : { QUEST : "_toNpcName_ a l'air d'être dans une situation difficile. Elle serait sûrement contente d'avoir de l'aide._where_" },
    1082 : { QUEST : "J'ai renversé de la colle à séchage rapide, et je suis collée - complètement collée!\aSi seuleument je trouvais une façon de m'en sortir...\aCela me donne une idée, si tu veux bien.\aVa vaincre quelques Vendibots et ramène-moi de l'huile.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller ?" },
    1083 : { QUEST : "Bon, l'huile a fait un peu d'effet, mais je ne peux toujours pas bouger.\aQu'est-ce qui pourrait bien m'aider ? C'est difficile à dire.\aCela me donne une idée on peut au moins essayer.\aVa vaincre quelques Loibots et ramène-moi de la graisse.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller ?" },
    1084 : { QUEST : "Non, ça n'a rien fait. Ce n'est vraiment pas drôle.\aJ'ai pourtant mis de la graisse partout.\aÇa me donne une idée, avant que j'oublie.\aVa vaincre quelques Caissbots et rapporte de l'eau pour l'humecter.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Hourrah, je suis libérée de cette colle rapide.\aComme récompense, je te donne ce cadeau.\aTu peux rire un peu plus longtemps lorsque tu es en train de te battre, et puis...\aOh, non! Je suis de nouveau collée là!",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller ?" },
    1085 : { QUEST : "_toNpcName_ est en train de faire des recherches sur les Cogs.\aVa lui parler si tu veux l'aider._where_" },
    1086 : { QUEST : "C'est cela, je fais une étude sur les Cogs.\aJe veux savoir ce qui les fait tiquer.\aCela m'aiderait certainement si tu pouvais me trouver des pignons de Cogs.\aAssure-toi qu'il s'agit de Cogs de niveau 2 au minimum, qu'ils soient assez gros pour être examinés.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu ne peux pas trouver assez de pignons?" },
    1089 : { QUEST : "OK, regardons un peu ça. Ce sont d'excellents spécimens!\aMmmm...\aOK, voilà mon rapport. Emmène-le tout de suite au quartier général des Toons.",
             INCOMPLETE : "As-tu porté mon rapport au quartier général?",
             COMPLETE : "Bon travail _avName_, on va s'occuper de ça.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ a des informations importantes pour toi._where_" },
    1091 : { QUEST : "J'ai entendu dire que le quartier général des Toons travaille sur une sorte de détecteur de Cogs.\aIl te permettra de voir où sont les Cogs afin de les repérer plus facilement.\aLa page des Cogs dans ton journal de bord en est la clé.\aEn battant assez de Cogs, tu pourras te régler sur leurs signaux et détecter leur emplacement.\aContinue à vaincre des Cogs, afin d'être prêt.",
             COMPLETE : "Bon travail! Tu pourras probablement utiliser ceci...",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "Tu peux maintenant choisir la prochaine série de gags que tu veux apprendre.\aPrends ton temps pour te décider, et reviens quand tu auras choisi.",
           INCOMPLETE_PROGRESS : "Pense bien à ta décision avant de choisir.",
           INCOMPLETE_WRONG_NPC : "Pense bien à ta décision avant de choisir.",
           COMPLETE : "Une sage décision...",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "Ces faux-jetons de Cogs font encore des leurs.\a_toNpcName_ vient de signaler un autre objet disparu. Va voir si tu peux régler cela._where_" },
    2202 : { QUEST : "Salut, _avName_. Dieu merci, tu es là. Un Radino à l'air méchant était là à l'instant et il est parti avec une chambre à air.\aJe crains qu'ils ne l'utilisent pour leurs sombres desseins.\aS'il te plaît, essaie de le retrouver et ramène-la moi.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé ma chambre à air ?",
             COMPLETE : "Tu as trouvé ma chambre à air! Tu es vraiment très doué. Tiens, prends ta récompense...",
             },
    2203 : { QUEST : "Les Cogs sont en train de mettre la banque sens dessus dessous.\aVa voir le Capitaine Carl et vois ce que tu peux faire._where_" },
    2204 : { QUEST : "Bienvenue à bord, moussaillon.\aGrrr! Ces fripons de Cogs ont cassé mon monocle et je n'arrive plus à compter la monnaie sans lui.\aGarde les pieds sur terre et porte cette ordonnance au Dr. Queequeg puis rapporte m'en un nouveau._where_",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "Qu'est-ce que c'est ?\aOh, je voudrais bien préparer cette ordonnance mais les Cogs ont chapardé mes réserves.\aSi tu peux reprendre la monture à un Laquaistic je pourrai probablement t'aider.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Désolé. Pas de monture du Laquaistic, pas de monocle.",
             },
    2206: { QUEST : "Excellent!\aUne seconde...\aTon ordonnance est prête. Emmène tout de suite ce monocle au Capitaine Carl._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "Hisse et ho!\aTu vas finir par gagner du galon après tout.\aEt voilà.",
            },
    2207 : { QUEST : "Barbara Bernache a un Cog dans son magasin!\aIl vaudrait mieux que tu y ailles tout de suite._where_" },
    2208 : { QUEST : "Ça alors! Tu viens de le rater, mon chou.\aIl y avait un Frappedos ici. Il a pris ma grande perruque blanche.\aIl a dit que c'était pour son chef et quelque chose à propos de \"jurisprudence\".\aSi tu pouvais me la rapporter, je t'en serais toujours reconnaissante.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Tu ne l'as toujours pas trouvé?\aIl est grand avec une tête pointue.",
             COMPLETE : "Tu l'as trouvé!?!?\aTu es vraiment un ange!\aTu as bien mérité ceci...",
             },
    2209 : { QUEST : "Ginette se prépare pour un voyage important.\aVa y faire un tour et vois ce que tu peux faire pour l'aider._where_"},
    2210 : { QUEST : "Tu peux m'aider.\aLe quartier général des Toons m'a demandé de faire un voyage pour voir si je peux trouver d'où viennent les Cogs.\aJ'aurais besoin de quelques affaires pour mon bateau mais je n'ai pas beaucoup de bonbons.\aVa et ramène-moi du lest de chez Ernest. Il faudra que tu lui rendes un service pour l'avoir._where_",
             GREETING : "Salut, _avName_",
             LEAVING : "",
             },
    2211 : { QUEST : "Comme ça, Ginette veut du lest, n'est-ce pas?\aElle me doit encore de l'argent pour le dernier boisseau.\aJe te le donnerai si tu peux faire partir cinq Microchefs de ma rue.",
             INCOMPLETE_PROGRESS : "Non, idiot! J'ai dit CINQ Microchefs...",
             GREETING : "Que puis-je faire pour toi?",
             LEAVING : "",
             },
    2212 : { QUEST : "Un marché est un marché.\aVoilà ton lest pour cette pingre de Ginette._where_",
             GREETING : "Eh bien, regarde ce qui arrive là...",
             LEAVING : "",
             },
    2213 : { QUEST : "Excellent travail. Je savais qu'il serait raisonnable.\aEnsuite il me faudra une carte marine de chez Art.\aJe ne crois pas avoir beaucoup de crédit là-bas non plus il faudra que tu t'arranges avec lui._where_",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Oui, j'ai la carte marine que veut Ginette.\aEt tu l'auras en échange d'un petit travail.aJ'essaie de construire un astrolabe pour naviguer dans les étoiles.aJ'aurais besoin de trois pignons de Cog pour le construire.\aReviens quand tu les auras trouvés.",
             INCOMPLETE_PROGRESS: "Alors ils arrivent ces pignons de Cogs?",
             GREETING : "Bienvenue!",
             LEAVING : "Bonne chance!",
             },
    2215 : { QUEST : "Ooh! Ces pignons feront très bien l'affaire.\aVoilà la carte. Donne-la à Ginette avec mes compliments._where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "Bon, on y est presque. Je suis prête à prendre la mer!\aJe t'emmènerais avec moi si tu n'avais pas un teint si vert. Prends plutôt ceci.",
             },
    901 : { QUEST : "Si tu es d'accord, Ahab a besoin d'aide, chez lui..._where_",
            },
    2902 : { QUEST : "Tu es la nouvelle recrue ?\aBien, bien. Tu peux peut-être m'aider.\aJe suis en train de construire un crabe géant préfabriqué pour dérouter les Cogs.\aJe pourrais quand même utiliser une manille. Va voir Gérard et rapportes-en une, s'il te plaît._where_",
             },
    2903 : { QUEST : "Salut!\aOui, j'ai entendu parler du crabe géant qu'Ahab est en train de fabriquer.\aLa meilleure manille que j'aie est un peu sale quand même.\aSois sympa, passe chez un blanchisseur avant de la déposer._where_",
             LEAVING : "Merci!"
             },
    2904 : { QUEST : "Tu dois être la personne que Gérard a envoyée.\aJe crois que je peux faire ça assez vite.\aJuste une minute...\aEt voilà. Comme neuf!\aTu salueras Ahab de ma part._where_",
             },
    2905 : { QUEST : "Ah, c'est exactement ce que je cherchais.\aPendant que tu es là, je vais aussi avoir besoin d'un très gros ressort d'horloge.\aVa donc chez Crochet voir s'il en a un._where_",
             },
    2906 : { QUEST : "Un gros ressort, hein ?\aJe suis désolé mais le plus gros ressort que j'aie est quand même plutôt petit.\aJe pourrais peut-être en fabriquer un avec des ressorts de gâchette de pistolet éclabousseur.\aApporte-moi trois de ces gags et je vais voir ce que je peux faire.",
             },
    2907 : { QUEST : "Regardons ça...\aGénial. Vraiment génial.\aQuelquefois je me surprends moi-même.\aEt voilà : un gros ressort pour Ahab!_where_",
             LEAVING : "Bonne route!",
             },
    2911 : { QUEST : "Je serais très content de pouvoir aider, _avName_.\aMalheureusement, les rues ne sont plus sûres.\aVa donc éliminer quelques Cogs Caissbots et on pourra parler.",
             INCOMPLETE_PROGRESS : "Je crois que tu peux rendre les rues encore plus sûres.",
             },
    2916 : { QUEST : "Oui, j'ai un contrepoids que je pourrais donner à Ahab.\aJe crois que ce serait plus sûr si tu pouvais vaincre deux Vendibots d'abord.",
             INCOMPLETE_PROGRESS : "Pas encore. Tu dois vaincre plus de Vendibots.",
             },
    2921 : { QUEST : "Hmmm, je pensais que je pourrais me débarrasser d'un poids.\aJe me sentirais bien mieux s'il n'y avait pas autant de Cogs Chefbots à rôder par ici.\aVa donc en vaincre six et reviens me voir.",
             INCOMPLETE_PROGRESS : "Je crois qu'on n'est toujours pas en sécurité...",
             },
    2925 : { QUEST : "Ça y est ?\aBon, je suppose qu'on est suffisamment en sécurité maintenant.\aVoilà le contrepoids pour Ahab._where_"
             },
    2926 : {QUEST : "Bon, c'est tout.\aVoyons si ça marche.\aHmmm, il y a un petit problème.\aJe n'ai plus de courant parce que ce bâtiment Cog bloque mon capteur solaire.\aPeux-tu le reprendre pour moi?",
            INCOMPLETE_PROGRESS : "Toujours pas de courant. Où en es-tu avec ce bâtiment ?",
            COMPLETE : "Super! Tu es une sacrée terreur pour les Cogs! Tiens, prends ta récompense...",
            },
    3200 : { QUEST : "Je viens d'avoir un appel de _toNpcName_.\aCe n'est pas son jour. Tu pourrais peut-être l'aider.!\aVa y faire un tour et vois ce dont il a besoin._where_" },
    3201 : { QUEST : "Oh, merci d'être là!\aJ'ai besoin de quelqu'un pour emporter cette nouvelle cravate en soie à _toNpcName_.\aEst-ce que tu peux faire ça pour moi?_where_" },
    3203 : { QUEST : "Oh, ça doit être la cravate que j'ai commandée! Merci!\aElle va avec un costume à rayures que je viens de finir, juste là.\aHé, qu'est ce qui est arrivé à ce costume ?\aOh non! Les Cogs ont dû voler mon nouveau costume!\aTu dois vaincre des Cogs jusqu'à ce que tu trouves mon costume, et que tu me le rapportes.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas encore trouvé mon costume ? Je suis certain que les Cogs l'ont pris!",
             COMPLETE : "Youpii! Tu as trouvé mon nouveau costume!\aTu vois, je t'avais dit que les Cogs l'avaient! Voilà ta récompense...",
             },

    3204 : { QUEST : "_toNpcName_ vient d'appeler pour signaler un vol.\aPourquoi n'irais-tu pas voir si tu peux arranger l'affaire ?_where_" },
    3205 : { QUEST : "Bonjour, _avName_! Tu es là pour m'aider ?\aJe viens de chasser un Pique-au-sang de mon magasin. Houlala! C'était effrayant.\aMais maintenant je ne trouve plus mes ciseaux! Je suis certain que ce Pique-au-sang les a pris.\aTrouve-le, et ramène-moi mes ciseaux.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu cherches encore mes ciseaux?",
             COMPLETE : "Mes ciseaux! Merci beaucoup! Voilà ta récompense...",
             },

    3206 : { QUEST : "On dirait que _toNpcName_ a des problèmes avec des Cogs.\aVa voir si tu peux l'aider._where_" },
    3207 : { QUEST : "Ohé, _avName_! Merci d'être venu!\aUne bande de Charabieurs est arrivée et a volé une pile de cartes postales sur mon comptoir.\aS'il te plaît, sors vaincre tous ces Charabieurs et rapporte-moi mes cartes postales!",
             INCOMPLETE_PROGRESS : "Il n'y a pas assez de cartes postales! Continue de chercher!",
             COMPLETE : "Oh, merci! Maintenant je vais pouvoir livrer le courrier à temps! Voilà ta récompense...",
             },

    3208 : { QUEST : "Nous avons eu des plaintes des résidents récemment à propos des Cassepieds.\aEssaie de vaincre 10 Cassepieds pour aider tes camarades Toons du Jardin de Daisy." },
    3209 : { QUEST : "Merci d'avoir battu ces Cassepieds!\aMais maintenant ce sont les Télévendeurs qui sont incontrôlables.\aVa vaincre 10 Télévendeurs au Jardin de Daisy et reviens ici pour ta récompense." },

    3247 : { QUEST : "Nous avons eu des plaintes des résidents récemment à propos des Pique-au-sang.\aEssaie de vaincre 20 Pique-au-sang pour aider tes camarades Toons du Jardin de Daisy." },


    3210 : { QUEST : "Oh non, la Fleur qui mouille, rue des Érables, n'a plus de fleurs!\aEmmène-leur dix de tes fleurs à éclabousser pour les aider.\aVérifie que tu as bien 10 fleurs à éclabousser dans ton inventaire d'abord.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "J'ai besoin de 10 fleurs à éclabousser. Tu n'en as pas assez!" },
    3211 : { QUEST : "Oh, merci beaucoup! Ces fleurs à éclabousser vont nous tirer d'embarras.\aMais j'ai peur des Cogs qui sont dehors.\aPeux-tu m'aider et vaincre quelques-uns de ces Cogs?\aReviens me voir après avoir vaincu 20 Cogs dans cette rue.",
             INCOMPLETE_PROGRESS : "Il reste encore des Cogs à vaincre par ici! Continue!",
             COMPLETE : "Oh, merci! Cela m'aide beaucoup. Ta récompense est...",
             },

    3212 : { QUEST : "_toNpcName_ a besoin d'aide pour chercher quelque chose qu'elle a perdu.\aVa la voir et vois ce que tu peux faire._where_" },
    3213 : { QUEST : "Salut, _avName_. Peux-tu m'aider ?\aJe crois que j'ai égaré mon stylo. Je pense que les Cogs l'ont peut-être pris.\aVa vaincre des Cogs pour retrouver le stylo qu'ils m'ont volé.",
             INCOMPLETE_PROGRESS : "Tu n'as pas encore trouvé mon stylo?" },
    3214 : { QUEST : "Oui, c'est mon stylo! Merci beaucoup!\aMais après ton départ, j'ai réalisé que mon encrier manquait aussi.\aVa vaincre des Cogs pour retrouver mon encrier.",
             INCOMPLETE_PROGRESS : "Je cherche encore mon encrier!" },
    3215 : { QUEST : "Super! Maintenant j'ai retrouvé mon stylo et mon encrier!\aMais tu ne devineras jamais!\aMon bloc-notes a disparu! Ils ont dû le voler aussi!\aVa vaincre des Cogs pour retrouver mon bloc-notes volé, puis reviens pour ta récompense.",
             INCOMPLETE_PROGRESS : "Tu as des nouvelles de mon bloc-notes?" },
    3216 : { QUEST : "C'est mon bloc-notes! Youpii! Ta récompense est...\aHé! Mais où est-elle ?\aJ'avais ta récompense là, dans le coffre de mon bureau. Mais le coffre entier a disparu!\aIncroyable! Ces Cogs ont volé ta récompense!\aVa vaincre des Cogs pour retrouver mon coffre.\aQuand tu me le ramèneras, je te donnerai ta récompense.",
             INCOMPLETE_PROGRESS : "Continue de chercher ce coffre! Ta récompense est dedans!",
             COMPLETE : "Enfin! J'avais ton nouveau sac à gags dans ce coffre. Le voilà...",
             },

    3217 : { QUEST : "Nous avons fait quelques études sur les mécanismes des Vendibots.\aNous devons encore étudier certaines pièces de plus près.\aApporte-nous un pignon de Cafteur.\aTu peux en attraper un quand le Cog explose." },
    3218 : { QUEST : "Bon travail! Maintenant, nous avons besoin d'un pignon de Passetout pour faire la comparaison.\aCes pignons sont plus difficiles à attraper, ne te décourage pas." },
    3219 : { QUEST : "Super! Maintenant on n'a plus besoin que d'un pignon en plus.\aCette fois, il nous faut un pignon de Secousse-cousse.\aTu devras peut-être chercher à l'intérieur des bâtiments Vendibots pour trouver cette sorte de Cogs.\aQuand tu en auras attrapé un, rapporte-le pour recevoir ta récompense." },

    3244 : { QUEST : "Nous avons fait quelques études sur les mécanismes des Loibots.\aNous devons encore étudier certaines pièces de plus près.\aApporte-nous un pignon de Charognard.\aTu peux en attraper un quand le Cog explose." },
    3245 : { QUEST : "Bon travail! Maintenant nous avons besoin d'un pignon de Frappedos pour faire la comparaison.\aCes pignons sont plus difficiles à attraper, ne te décourage pas." },
    3246 : { QUEST : "Super! Encore un pignon et c'est bon.\aCette fois, il nous faut un pignon de Tournegris.\aQuand tu en auras attrapé un, rapporte-le pour avoir ta récompense." },

    3220 : { QUEST : "Je viens d'apprendre que _toNpcName_ te cherchait.\aPourquoi ne vas-tu pas voir ce qu'elle veut ?_where_" },
    3221 : { QUEST : "Ohé, _avName_! Et voilà!\aJ'ai entendu dire que tu étais expert(e) en éclaboussures.\aJ'ai besoin de quelqu'un pour montrer l'exemple à tous les Toons du Jardin de Daisy.\aUtilise tes attaques par éclaboussure pour vaincre un groupe de Cogs.\aEncourage tes contacts à utiliser aussi les éclaboussures.\aLorque tu auras vaincu 20 Cogs, reviens ici pour ta récompense!" },

    3222 : { QUEST : "C'est le moment de faire preuve de ta Toonmaîtrise.\aSi tu réussis à reprendre un certain nombre de bâtiments aux Cogs, tu gagneras le droit à trois quêtes.\aD'abord, tu dois prendre deux bâtiments aux Cogs.\aN'hésite pas à demander l'aide de tes contacts."},
    3223 : { QUEST : "Super travail pour ces bâtiments!\aMaintenant tu dois prendre deux bâtiments de plus.\aCes immeubles doivent faire au moins deux étages." },
    3224 : { QUEST : "Fantastique!\aMaintenant tu dois prendre deux bâtiments de plus.\aCes immeubles doivent faire au moins trois étages.\aQuand tu auras fini, reviens chercher ta récompense!",
             COMPLETE : "Tu as réussi, _avName_!\aTu as fait preuve d'une excellente Toonmaîtrise.",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ dit qu'elle a besoin d'aide.\aVa voir si tu peux lui donner un coup de main ?_where_" },
    3235 : { QUEST : "Oh, c'est la salade que j'ai commandée!\aMerci de me l'avoir apportée.\aTous ces Cogs ont dû effrayer le livreur habituel de _toNpcName_ encore une fois.\aTu pourrais nous rendre service et vaincre quelques-uns des Cogs qui traînent par ici?\aVa vaincre 10 Cogs dans le Jardin de Daisy et reviens voir _toNpcName_.",
             INCOMPLETE_PROGRESS : "Tu es en train de vaincre des Cogs pour moi?\aC'est super!! Continue comme ça!",
             COMPLETE : "Oh, merci beaucoup d'avoir vaincu ces Cogs!\aMaintenant je vais peut-être pouvoir reprendre mon programme habituel de livraisons.\aTa récompense est...",
             INCOMPLETE_WRONG_NPC : "Va raconter à _toNpcName_ tous les Cogs que tu as vaincus._where_" },

    3236 : { QUEST : "Il y a beaucoup trop de Loibots par ici.\aTu peux faire ta part de travail!\aVa vaincre 3 bâtiments Loibot." },
    3237 : { QUEST : "Super travail pour ces bâtiments Loibot!\aMais maintenant il y a beaucoup trop de Vendibots!\aVa vaincre 3 bâtiments Vendibot, puis reviens chercher ta récompense." },

    3238 : { QUEST : "Oh non! Un Cog Circulateur a volé la clé du Jardin de Daisy!\aVa voir si tu peux la retrouver.\aSouviens-toi que les Circulateurs ne se trouvent que dans les bâtiments Vendibot." },
    3239 : { QUEST : "Tu as bien trouvé une clé, mais ce n'est pas la bonne!\aNous avons besoin de la clé du Jardin de Daisy.\aContinue de chercher! Un Cog Circulateur l'a encore!" },

    3242 : { QUEST : "Oh non! Un Cog Avocageot a volé la clé du Jardin de Daisy!\aVa voir si tu peux la retrouver.\aSouviens-toi que les Avocageots ne se trouvent que dans les bâtiments Loibot." },
    3243 : { QUEST : "Tu as bien trouvé une clé, mais ce n'est pas la bonne!\aNous avons besoin de la clé du Jardin de Daisy.\aContinue de chercher! Un Cog Avocageot l'a encore!" },

    3240 : { QUEST : "_toNpcName_ vient de me dire qu'un Avocageot lui a volé un sac de graines pour oiseaux.\aVa vaincre des Avocageots jusqu'à ce que tu retrouves les graines pour oiseaux de Piaf, et rapporte-les lui.\aLes Avocageots ne se trouvent que dans les bâtiments Loibot._where_",
             COMPLETE : "Oh, merci beaucoup d'avoir retrouvé mes graines pour oiseaux!\aTa récompense est...",
             INCOMPLETE_WRONG_NPC : "Bien, tu as retrouvé ces graines pour oiseaux!\aMaintenant apporte-les à _toNpcName_._where_",
             },

    3241 : { QUEST : "Certains des bâtiments des Cogs deviennent beaucoup trop hauts.\aVa voir si tu peux réduire de hauteur certains des immeubles les plus hauts.\aReprends 5 immeubles de 3 étages ou plus et reviens ici pour ta récompense.",
             },

    3250 : { QUEST : "Lima, la détective de la rue du Chêne, a entendu parler d'un quartier général Vendibot. \aVa donc la voir et aide-la à enquêter.",
             },
    3251 : { QUEST : "Il y a quelque chose de bizarre par ici.\aIl y a tant de Vendibots!\aJ'ai entendu dire qu'ils ont installé leur propre quartier général au bout de cette rue.\aVa au bout de la rue voir ce qu'il en est.\aTrouve des Cogs Vendibots dans leur quartier général, vaincs-en 5 et reviens me le dire.",
             },
    3252 : { QUEST : "OK, annonce la couleur\aQu'est-ce que tu dis?\aAh, le quartier général des Vendibots?? Oh non!!! Il faut faire quelque chose.\aNous devons le dire au Juge Ticot - il saura quoi faire.\aVa le voir tout de suite et dis-lui ce que tu as trouvé. Il est juste au bout de la rue.",
            },
    3253 : { QUEST : "Oui, puis-je t'aider ? Je suis très occupé.\aHein ? Un quartier général Cog?\aHein ? Sottises. Ça n'est pas possible.\aTu dois te tromper. C'est grotesque.\aHein ? Ne discute pas avec moi.\aOk, alors ramène des preuves.\aSi les Vendibots sont vraiment en train de construire ce quartier général Cog, les Cogs du quartier auront des plans sur eux.\aLes Cogs adorent la paperasserie, tu le savais?\aVa vaincre des Vendibots par là-bas jusqu'à ce que tu trouves des plans.\aRapporte-les moi, alors je te croirai peut-être.",
            },
    3254 : { QUEST : "Encore toi, hein ? Des plans? Tu les as?\aLaisse-moi regarder ça! Hmmm... Une usine ?\aCe doit être là qu'ils fabriquent les Vendibots... Et qu'est-ce que c'est que ça?\aOui, exactement ce que je pensais. Je le savais depuis le départ.\aIls sont en train de construire un quartier général des Cogs Vendibots.\aCe n'est pas bon signe. Je dois passer quelques appels. Très occupé. Au revoir!\aHein ? Oh oui, retourne ces plans à la détective Lima.\aElle saura les lire mieux que quiconque.",
             COMPLETE : "Qu'a dit le Juge Ticot ?\aOn avait raison ? Oh non. Regardons ces plans.\aHmmm... On dirait que les Vendibots ont installé une usine avec l'outillage pour construire des Cogs.\aÇa a l'air très dangereux. N'y va pas tant que tu n'as pas plus de rigolpoints.\aQuand tu auras plus de rigolpoints, nous en aurons beaucoup à apprendre sur le quartier général des Vendibots.\aPour l'instant, bon travail, voilà ta récompense.",
            },


    3255 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux donner un coup de main._where_" },
    3256 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux donner un coup de main._where_" },
    3257 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux lui donner un coup de main._where_" },
    3258 : { QUEST : "Personne ne sait au juste ce que les Cogs sont en train de faire dans leur nouveau quartier général.\aJ'ai besoin que tu nous ramènes des informations venant directement d'eux.\aSi nous pouvons trouver quatre notes de service internes des Vendibots à l'intérieur de leur quartier général, cela mettrait un peu les choses au clair.\aRamène-moi la première note de service que tu pourras afin qu'on en sache un peu plus.",
             },
    3259 : { QUEST : "Super! Voyons ce que dit cette note de service...\a\"À l'attention des Vendibots :\aJe serai dans mon bureau tout en haut des Tours Vendibot pour faire monter en grade les Cogs. \aLorsque vous aurez gagné suffisamment de mérites, montez me voir par l'ascenseur du hall.\aLa pause est terminée - tout le monde au travail!\"\aSigné, Vice-Président des Vendibots\"\aAah.... Flippy sera content de voir ça. Je lui envoie ça tout de suite.\aVa chercher une seconde note de service et rapporte-la moi.",
             },
    3260 : { QUEST : "Oh, bien, tu es de retour. Voyons ce que tu as trouvé....\a\"À l'attention des Vendibots :\aLes Tours Vendibot ont été équipées d'un nouveau système de sécurité pour empêcher les Toons de pénétrer à l'intérieur.\aLes Toons qui seront attrapés dans les Tours Vendibot seront retenus pour interrogatoire.\aVeuillez en discuter dans le hall autour d'un apéritif.\aSigné, Le Circulateur \"\aTrès intéressant... Je communique l'information immédiatement.\aS'il te plaît, rapporte-moi une troisième note de service.",
             },
    3261 : { QUEST : "Excellent travail, _avName_! Que dit cette note de service ?\a\"À l'attention des Vendibots :\aLes Toons sont parvenus à trouver une façon d'infiltrer les Tours Vendibot.\aJe vous appellerai ce soir pendant le dîner pour vous donner des détails.\aSigné, Télévendeur\"\aHmmm... Je me demande comment les Toons se sont infiltrés....\aRapporte-moi une note de service supplémentaire et je crois que nous aurons assez d'informations pour l'instant.",
             COMPLETE : "Je savais que tu pouvais le faire! OK, voilà ce que dit la note de service....\a\"À l'attention des Vendibots :\aJ'ai déjeûné avec M. Hollywood hier.\aIl dit que le Vice-Président est très occupé en ce moment.\aIl ne prendra de rendez-vous qu'avec les Cogs qui méritent une promotion.\aJ'allais oublier, Passetout joue au golf avec moi dimanche.\aSigné, Cafteur\"\aBon... _avName_, voilà qui est bien utile.\aVoilà ta récompense.",
             },

    3262 : { QUEST : "_toNpcName_ a de nouvelles informations à propos de l'usine du quartier général Vendibot.\aVa donc voir ce que c'est._where_" },
    3263 : { GREETING : "Salut, mon pote!",
             QUEST : "Je suis Zucchini l'entraîneur, mais tu peux simplement m'appeler Coach Z.\aJe mets la gomme sur le squash et les étirements, si tu vois ce que je veux dire.\aÉcoute, les Vendibots ont terminé une énorme usine qui sort des Vendibots 24 heures sur 24.\aPrends une équipe de potes Toons et va me réduire cette usine à néant!\aÀ l'intérieur du quartier général Vendibot, cherche le tunnel qui mène à l'usine puis monte par l'ascenseur de l'usine.\aVérifie que tu as fait le plein de gags, de rigolpoints et que tu as quelques Toons costauds comme guides.\aVa vaincre le contremaître dans l'usine pour ralentir la progression des Vendibots.\aCe sera une vraie séance d'entraînement, si tu vois ce que je veux dire.",
             LEAVING : "À plus, mon pote!",
             COMPLETE : "Hé mon pote, bon boulot pour cette usine!\aOn dirait que tu as trouvé un morceau de costume de Cog.\aIl doit venir de la chaîne de fabrication des Cogs.\aÇa peut être pratique. Continue à en ramasser quand tu as du temps de libre.\aPeut-être que si tu récupères un costume de Cog complet, ça pourrait être utile à quelque chose....",
             },

    4001 : {GREETING : "",
            QUEST : "Tu peux maintenant choisir la prochaine série de gags que tu veux apprendre.\aPrends ton temps pour te décider, et reviens quand tu auras choisi.",
            INCOMPLETE_PROGRESS : "Pense bien à ta décision avant de choisir.",
            INCOMPLETE_WRONG_NPC : "Pense bien à ta décision avant de choisir.",
            COMPLETE : "Une sage décision...",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "Tu peux maintenant choisir la prochaine série de gags que tu veux apprendre.\aPrends ton temps pour te décider, et reviens quand tu auras choisi.",
            INCOMPLETE_PROGRESS : "Pense bien à ta décision avant de choisir.",
            INCOMPLETE_WRONG_NPC : "Pense bien à ta décision avant de choisir.",
            COMPLETE : "Une sage décision...",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "Je parie que Tom aimerait de l'aide pour ses recherches._where_",
             },
    4201 : { GREETING: "Salut!",
             QUEST : "Je suis très embêté au sujet d'une vague de vols d'instruments.\aJe fais une enquête parmi mes confrères commerçants.\aJe vais peut-être pouvoir trouver une constante qui me permettra de résoudre ce cas.\aVa voir Tina et demande-lui un inventaire des concertinas._where_",
             },
    4202 : { QUEST : "Oui, j'ai parlé à Tom ce matin.\aJ'ai l'inventaire ici.\aTu vas lui apporter tout de suite, ok?_where_"
             },
    4203 : { QUEST : "Super! Et de un...\aMaintenant va chercher celui de Yuki._where_",
             },
    4204 : { QUEST : "Oh! L'inventaire!\aJ'avais complètement oublié.\aJe parie que je peux le faire le temps que tu aies vaincu 10 Cogs.\aRepasse après ça et je promets que ce sera prêt.",
             INCOMPLETE_PROGRESS : "31, 32... OUPS!\aTu m'as fait perdre mon compte!",
             GREETING : "",
             },
    4205 : { QUEST : "Ah, et voilà.\aMerci de m'avoir laissé un peu de temps.\aEmmène ça à Tom et dis-lui bonjour de ma part._where_",
             },
    4206 : { QUEST : "Hmm, très intéressant.\aÇa commence à ressembler à quelque chose.\aOK, le dernier inventaire est celui de Fifi._where_",
             },
    4207 : { QUEST : "Inventaire ?\aComment est-ce que je pourrais faire un inventaire sans formulaire ?\aVa voir Clément de sol et demande-lui s'il en a un pour moi._where_",
             INCOMPLETE_PROGRESS : "Alors, ce formulaire ?",
             },
    4208 : { QUEST : "Ah ça oui j'ai un formulaire d'inventaire!\aMais c'est pas gratuit, tu vois.\aJe vais te dire. Je te le vends pour une tarte à la crème entière.",
             GREETING : "Allez, mon petit!",
             LEAVING : "Chouette...",
             INCOMPLETE_PROGRESS : "Une seule tranche c'est pas assez.\aJ'ai faim, mon petit! Je veux la tarte TOUTE ENTIÈRE.",
             },
    4209 : { GREETING : "",
             QUEST : "Mmmm...\aSuper bon!\aVoilà ton formulaire pour Fifi._where_",
             },
    4210 : { GREETING : "",
             QUEST : "Merci. Ça va bien m'aider.\aVoyons...violons: 2\aÇa y est! Et voilà!",
             COMPLETE : "Bon travail, _avName_!\aJe suis sûr de pouvoir attraper ces voleurs maintenant.\aOn va pouvoir creuser cette affaire!",
             },

    4211 : { QUEST : "Dis donc, le Dr Tefaispasdebile appelle toutes les cinq minutes. Tu pourrais aller voir quel est son problème ?_where_",
             },
    4212 : { QUEST : "Houlala! Je suis content que le quartier général des Toons ait fini par envoyer quelqu'un.\aÇa fait des jours que je n'ai pas vu un client.\aCe sont ces satanés Gobechiffres qui sont partout.\aJe crois qu'ils enseignent une mauvaise hygiène buccale à nos résidents.\aVa donc en vaincre dix et nous verrons si les affaires reprennent.",
             INCOMPLETE_PROGRESS : "Toujours pas de patients. Mais continue!",
             },
    4213 : { QUEST : "Tu sais après tout peut-être que ce n'était pas les Gobechiffres.\aPeut-être que ce sont simplement les Caissbots en général.\aDébarrasse-nous de vingt d'entre eux et j'espère que quelqu'un viendra au moins pour un bilan de santé.",
             INCOMPLETE_PROGRESS : "Je sais que vingt ça fait beaucoup. Mais je suis certain que ça va rapporter des tonnes.",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Je ne comprends rien du tout!\aToujours pas un SEUL client.\aPeut-être qu'on devrait remonter jusqu'à la source.\aEssaie de reprendre un bâtiment Cog Caissbot.\aÇa devrait faire l'affaire...",
             INCOMPLETE_PROGRESS : "Oh, s'il te plaît! Juste un tout petit bâtiment...",
             COMPLETE : "Toujours personne.\aMais tu vois, maintenant que j'y pense.\aJe n'avais pas non plus de clients avant l'invasion des Cogs!\aJe te remercie quand même beaucoup pour ton aide.\aCela devrait te rendre service."
             },

    4215 : { QUEST : "Anna a désespérément besoin de quelqu'un pour l'aider.\aPourquoi ne vas-tu pas voir ce que tu peux faire ?_where_",
             },
    4216 : { QUEST : "Merci d'être là aussi vite!\aOn dirait que les Cogs sont partis avec les tickets de croisière de plusieurs de mes clients.\aYuki a dit qu'elle avait vu un Passetout sortir d'ici avec des tickets plein les mains.\aVa voir si tu peux retrouver le ticket pour l'Alaska de Jack Bûcheron.",
             INCOMPLETE_PROGRESS : "Ces Passetouts pourraient être n'importe où maintenant...",
             },
    4217 : { QUEST : "Oh, super. Tu l'as trouvé!\aPuisque je peux compter sur toi, va le porter à Jack pour moi, tu veux bien ?_where_",
             },
    4218 : { QUEST : "Tralala!\aAlaska, me voilà!\aJe ne peux plus supporter ces Cogs infernaux.\aDis donc, je crois qu'Anna a encore besoin de toi._where_",
             },
    4219 : { QUEST : "Ouais, tu as deviné.\aJ'aurais besoin que tu secoues ces satanés Passetouts pour récupérer le ticket de Tabatha pour la fête du Jazz.\aTu sais comment ça marche...",
               INCOMPLETE_PROGRESS : "Il y en a d'autres qui rôdent...",
             },
    4220 : { QUEST : "Adorable!\aTu peux lui emmener ça pour moi aussi?_where_",
             },
    4221 : { GREETING : "",
             LEAVING : "Sois sympa...",
             QUEST : "Super, mon petit!\aMaintenant je suis à la fête, _avName_.\aAvant de partir, tu ferais mieux d'aller voir Anna Banane encore une fois..._where_",
             },
    4222 : { QUEST : "C'est la dernière fois, je te promets!\aMaintenant tu vas chercher le ticket de Barry pour le concours de chant.",
             INCOMPLETE_PROGRESS : "Allez, _avName_.\aBarry compte sur toi.",
             },
    4223 : { QUEST : "Ça devrait redonner le sourire à Barry._where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "Bonjour, Bonjour, BONJOUR!\aSuper!\aJe suis sûr que les gars et moi on a va ramasser le gros lot cette année.\aAnna demande que tu repasses la voir pour récupérer ta récompense._where_\aAu revoir, au revoir, AU REVOIR!",
             COMPLETE : "Merci pour toute ton aide, _avName_.\aTu es vraiment un atout pour nous à Toontown.\aEn parlant d'atouts...",
             },

    902 : { QUEST : "Va donc voir Léo.\aIl a besoin de quelqu'un pour porter un message._where_",
            },
    4903 : { QUEST : "Pote!\aMes castagnettes sont toutes ternies et j'ai un grand spectacle ce soir. \aEmporte-les donc à Carlos voir s'il peut me les faire reluire._where_",
             },
    4904 : { QUEST : "Voui, yé crois que yé peux réluire ça.\aMé yé bézoin d'encre de seiche bleue.",
             GREETING : "¡Holà!",
             LEAVING : "¡Adiós!",
             INCOMPLETE_PROGRESS : "Tou pé trrouver la seiche partout sour lé pontons de pêche.",
             },
    4905 : { QUEST : "Voui! Souperr!\aAhóra yé bézoin d'un peu de temps pour réluire ça.\aTou pé aller récoupérer un bâtiment de oun étage pendant qué yé trravaille ?",
             GREETING : "¡Holà!",
             LEAVING : "¡Adiós!",
             INCOMPLETE_PROGRESS : "Oun pitite minute...",
             },
    4906 : { QUEST : "Trrès bien!\aVoilà les castagnettes pour Léo._where_",
             },
    4907 : { GREETING : "",
             QUEST : "Super, mon petit!\aElles sont superbes!\aMaintenant j'ai besoin que tu me rapportes une copie des paroles de \"Un Noël toon\" de chez Élise._where_",
             },
    4908 : { QUEST: "Holà par ici!\aHmmm, je n'ai pas de copie de cette chanson.\aSi tu me laisses un peu de temps je pourrai la retranscrire de mémoire.\aPourquoi tu n'irais pas faire un tour et reprendre un bâtiment de deux étages pendant que j'écris?",
             },
    4909 : { QUEST : "Je suis désolée.\aMa mémoire est un peu floue.\aSi tu vas reprendre un bâtiment de trois étages, je suis sûre que ce sera fait quand tu reviendras...",
             },
    4910 : { QUEST : "Ça y est!\aDésolée d'avoir mis si longtemps.\aRapporte-ça à Léo._where_",
             GREETING : "",
             COMPLETE : "Génial, mon petit!\aMon concert va casser la baraque!\aÀ propos de casser, tu pourras utiliser ça sur quelques Cogs..."
             },
    5247 : { QUEST : "Le quartier est assez chaud...\aTu pourrais avoir besoin d'apprendre quelques nouveaux trucs.\a_toNpcName_ m'a appris tout ce que je sais, il peut peut-être t'aider aussi._where_" },
    5248 : { GREETING : "Ahh, oui.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu as l'air d'avoir des difficultés avec cette mission.",
             QUEST : "Aah, bienvenue, nouvel apprenti.\aJe sais tout ce qu'on peut savoir à propos du jeu de tartes.\aMais avant qu'on ne commence ton entraînement, une petite démonstration s'impose.\aVa donc faire un tour et vaincre dix des plus gros Cogs." },
    5249 : { GREETING: "Mmmmm.",
             QUEST : "Excellent!\aMaintenant tu vas nous montrer ce que tu sais faire à la pêche.\aJ'ai fait tomber trois dés en peluche dans la mare hier.\aVa-les pêcher et rapporte-les moi.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "On dirait que tu n'es pas si habile avec la canne et le moulinet." },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah! Ces dés auront l'air super, accrochés au rétroviseur de ma bagnole!\aMaintenant, montre-moi que tu peux distinguer tes ennemis les uns des autres.\aReviens quand tu auras repris deux des plus grands bâtiments Loibot.",
             INCOMPLETE_PROGRESS : "Est-ce que tu as des difficultés avec ces bâtiments?", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah! Ces dés auront l'air super, accrochés au rétroviseur de ma bagnole!\aMaintenant, montre-moi que tu peux distinguer tes ennemis les uns des autres.\aReviens quand tu auras repris deux des plus grands bâtiments Chefbot.",
             INCOMPLETE_PROGRESS : "Est-ce que tu as des difficultés avec ces bâtiments?", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah! Ces dés auront l'air super, accrochés au rétroviseur de ma bagnole!\aMaintenant, montre-moi que tu peux distinguer tes ennemis les uns des autres.\aReviens quand tu auras repris deux des plus grands bâtiments Caissbot.",
             INCOMPLETE_PROGRESS : "Est-ce que tu as des difficultés avec ces bâtiments?", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah! Ces dés auront l'air super, accrochés au rétroviseur de ma bagnole!\aMaintenant, montre-moi que tu peux distinguer tes ennemis les uns des autres.\aReviens quand tu auras repris deux des plus grands bâtiments Vendibot.",
             INCOMPLETE_PROGRESS : "Est-ce que tu as des difficultés avec ces bâtiments?", },
    5200 : { QUEST : "Ces faux-jetons de Cogs font encore des leurs.\a_toNpcName_ vient de signaler un autre objet disparu. Va voir si tu peux régler cela._where_" },
    5201 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être venu.\aUn groupe de ces Chassetêtes est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot ?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5261 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Bifaces est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot ?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5262 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Sacasous est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot ?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5263 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Tournegris est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot ?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5202 : { QUEST : "Le Glagla a été envahi par des Cogs parmi les plus robustes qu'on ait vus.\aTu auras probablement besoin d'emporter plus de gags là-bas.\aJ'ai entendu dire que _toNpcName_ pourrait te prêter un grand sac pour emporter plus de gags._where_" },
    5203 : { GREETING: "Eh? Tu es dans mon équipe de luge ?",
             QUEST : "Qu'est-ce que c'est ? Tu veux un sac?\aJ'en avais un par là...peut-être qu'il est dans ma luge ?\aMais c'est que... Je n'ai pas vu ma luge depuis la grande course!\aPeut-être qu'un de ces Cogs l'a prise ?",
             LEAVING : "As-tu vu ma luge ?",
             INCOMPLETE_PROGRESS : "Rappelle-moi qui tu es? Désolé, je suis un peu étourdi depuis l'accident." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Est-ce que c'est ma luge ? Je ne vois pas de sac par ici.\aJe crois que Boris Tourne était dans l'équipe...c'est peut-être lui qui l'a?_where_" },
    5205 : { GREETING : "Oooh, ma tête!",
             LEAVING : "",
             QUEST : "Hein ? Ted qui? Un sac?\aAh, peut-être qu'il était dans notre équipe ?\aJ'ai tellement mal à la tête que je n'arrive plus à réfléchir.\aPourrais-tu aller me pêcher des glaçons dans la mare gelée pour ma tête ?",
             INCOMPLETE_PROGRESS : "Aïe, ma tête me fait mal! Tu as de la glace ?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah, ma tête va beaucoup mieux!\aAlors tu cherches le sac de Ted, hein ?\aJe crois qu'il a atterri sur la tête de Sam Simiesque après l'accident._where_" },
    5207 : { GREETING : "Hé-ho!",
             LEAVING : "",
             QUEST : "Quoi c'est ça un sac? Qui c'est ça Bouris?\aMoi avoir peur bâtiments! Toi battre bâtiments, moi te donner sac!",
             INCOMPLETE_PROGRESS : "Encore bâtiments! Moi encore peur!",
             COMPLETE : "Ooooh! Moi t'aime!" },
    5208 : { GREETING : "",
             LEAVING : "Hein!",
             QUEST : "Ooooh! Moi t'aime!\aVa Atelier de ski. Sac là-bas." },
    5209 : { GREETING : "Pote!",
             LEAVING : "'plus!",
             QUEST : "Bon sang, ce Sam Simiesque est fou!\aSi tu es aussi malade que Sam, je te donne ton sac.\aVa démolir des Cogs pour ton sac, mon pote! Salut!",
             INCOMPLETE_PROGRESS : "Es-tu certain(e) d'être au point ? Va donc démolir plus de Cogs.",
             COMPLETE : "Ouah! T'es vachement chouette! C'est un sacré tas de Cogs que tu as bousillés!\aVoilà ton sac!" },

    5210 : { QUEST : "_toNpcName_ aime quelqu'un du quartier en secret.\aSi tu l'aides, elle pourrait te donner une belle récompense._where_" },
    5211 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs avec un bec me l'a dérobée.\aPeux-tu me la rapporter ?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5264 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs avec un aileron me l'a dérobée.\aPeux-tu me la rapporter ?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5265 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs Circulateurs me l'a dérobée.\aPeux-tu me la rapporter ?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5266 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs Attactics me l'a dérobée.\aPeux-tu me la rapporter ?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5212 : { QUEST : "Oh, merci d'avoir retrouvé ma lettre!\aS'il te plaît, peux-tu la remettre au plus beau chien du quartier ?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas remis ma lettre, n'est-ce pas?",
             },
    5213 : { GREETING : "Charmé, certainement.",
             QUEST : "Je ne peux pas m'occuper de ta lettre, tu vois.\aTous mes chiots m'ont été pris!\aSi tu les ramènes, peut-être qu'on pourra parler.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mes pauvres petits chiots!" },
    5214 : { GREETING : "",
             LEAVING : "Youhouuu!",
             QUEST : "Merci de m'avoir rapporté mes petits choux.\aRegardons cette lettre maintenant...Mmmm, il semblerait que j'ai une autre admiratrice secrète.\aIl est temps de rendre visite à mon cher ami Carl.\aTu l'aimeras beaucoup, c'est certain._where_" },
    5215 : { GREETING : "Hé, hé...",
             LEAVING : "Reviens, oui, oui.",
             INCOMPLETE_PROGRESS : "Il y en a encore des gros par ici. Reviens nous voir quand il n'y en aura plus.",
             QUEST : "Qui est-ce qui t'envoie ? On aime pas trop les bêcheurs, non...\aMais on aime encore moins les Cogs...\aDébarrasse-nous donc des gros et on t'aidera, oui on t'aidera." },
    5216 : { QUEST : "On t'avait bien dit qu'on t'aiderait.\aTu peux emmener cette bague à la fille.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu as encore la bague ???",
             COMPLETE : "Oh, tu es un amour!!! Merci!!!\aOh, et j'ai quelque chose de spécial pour toi aussi.",
             },
    5217 : { QUEST : "On dirait que _toNpcName_ pourrait avoir besoin d'aide._where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je crois bien qu'il y a d'autres Circulateurs par ici.",
             QUEST : "À l'aide!!! À l'aide!!! Je n'en peux plus!\aCes Circulateurs me rendent dingue!!!" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ce n'est pas possible qu'il n'y ait que ça. Je viens d'en voir un!!!",
             QUEST : "Oh, merci, mais maintenant ce sont les Attactics!!!\aIl faut que tu m'aides!!!" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Non, non, il y en avait un juste là!",
             QUEST : "Je réalise maintenant que ce sont les Usuriers!!!\aJe croyais que tu allais me sauver!!!" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "Tu sais quoi, peut-être finalement que ce ne sont pas du tout les Cogs!!!\aPourrais-tu demander à Gaëlle de me préparer une potion calmante ? Ça m'aiderait peut-être...._where_" },
    5222 : { LEAVING : "",
             QUEST : "Oh, ce Harry, c'est quelqu'un!\aJe vais concocter quelque chose qui le remettra sur pied!\aBon, on dirait que je n'ai plus de moustaches de sardine...\aSois un ange et cours à la mare m'en attraper.",
             INCOMPLETE_PROGRESS : "Tu les as, ces moustaches de sardine ?", },
    5223 : { QUEST : "OK. Merci, mon ange.\aVoilà, maintenant porte ça à Harry. Ça devrait le calmer tout de suite.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vas-y maintenant, emporte la potion à Harry.",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu vas attraper ces Avocageots pour moi, n'est-ce pas?",
             QUEST : "Oh merci mon Dieu tu es de retour!\aDonne-moi la potion, vite!!!\aGlou, glou, glou...\aBerk, c'est dégoûtant!!\aMais tu sais quoi? Je me sens bien plus calme. Maintenant que j'ai les idées claires, je réalise que...\aC'est les Avocageots qui me rendaient malade pendant tout ce temps!!!",
             COMPLETE : "Bon sang! Maintenant je peux me détendre!\aJ'ai sûrement quelque chose à te donner. Oh, prends ça!" },
    5225 : { QUEST : "Depuis l'incident avec le pain de navets, Phil Électrique est furieux après _toNpcName_.\aTu pourrais peut-être aider Paul à les réconcilier ?_where_" },
    5226 : { QUEST : "Ouais, tu as sans doute entendu dire que Phil Électrique est furieux contre moi...\aJ'essayais juste d'être gentil avec ce pain de navets.\aPeut-être que tu pourrais le remettre de bonne humeur.\aPhil a horreur de ces Cogs Caissbots, surtout leurs bâtiments.\aSi tu reprends des bâtiments Caissbot, ça pourrait aider.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Peut-être quelques bâtiments de plus?", },
    5227 : { QUEST : "C'est formidable! Va dire à Phil ce que tu as fait._where_" },
    5228 : { QUEST : "Oh il a fait ça?\aCe Paul croit qu'il peut s'en tirer comme ça, hein ?\aIl m'a cassé ma dent, oui, avec son fichu pain de navets!\aPeut-être que si tu amenais ma dent au Dr Marmotter, il pourrait la réparer.",
             GREETING : "Mmmmrrphh.",
             LEAVING : "Grrr, grrr.",
             INCOMPLETE_PROGRESS : "Encore toi? Je pensais que tu allais faire réparer ma dent.",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je suis encore en train de travailler sur la dent. Ça va être un peu plus long.",
             QUEST : "Ah oui, cette dent est en mauvais état, c'est sûr.\aJe peux peut-être faire quelque chose, mais ça va mettre un moment.\aTu pourrais peut-être profiter de ce temps-là pour débarrasser les rues de quelques Cogs Caissbots?\aIls effraient mes clients." },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je suis encore en train de travailler sur la dent. Ça va être un peu plus long.",
             QUEST : "Ah oui, cette dent est en mauvais état, c'est sûr.\aJe peux peut-être faire quelque chose, mais ça va mettre un moment.\aTu pourrais peut-être profiter de ce temps-là pour débarrasser les rues de quelques Cogs Vendibots?\aIls effraient mes clients." },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je suis encore en train de travailler sur la dent. Ça va être un peu plus long.",
             QUEST : "Ah oui, cette dent est en mauvais état, c'est sûr.\aJe peux peut-être faire quelque chose, mais ça va mettre un moment.\aTu pourrais peut-être profiter de ce temps-là pour débarrasser les rues de quelques Cogs Loibots?\aIls effraient mes clients." },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je suis encore en train de travailler sur la dent. Ça va être un peu plus long.",
             QUEST : "Ah oui, cette dent est en mauvais état, c'est sûr.\aJe peux peut-être faire quelque chose, mais ça va mettre un moment.\aTu pourrais peut-être profiter de ce temps-là pour débarrasser les rues de quelques Cogs Chefbots?\aIls effraient mes clients." },
    5230 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement un Pillard me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent ?" },
    5270 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement un Gros Blochon me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent ?" },
    5271 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement M. Hollywood me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent ?" },
    5272 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement un Chouffleur me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent ?" },
    5231 : { QUEST : "Super, voilà la dent!\aPourquoi ne filerais-tu pas chez Phil pour lui porter ?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je parie que Phil serait content de voir sa nouvelle dent.",
             },
    5232 : { QUEST : "Oh, merci.\aMmmrrrphhhh\aÇa a l'air de quoi, hein ?\aOK, tu peux dire à Paul que je lui pardonne.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Oh, bonne nouvelle.\aJe savais bien que ce vieux Phil ne pourrait pas rester fâché contre moi.\aPour prouver ma bonne volonté, je lui ai fait cuire ce pain de pommes de pin.\aPourrais-tu lui porter, s'il te plaît ?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Presse-toi donc. Le pain de pommes de pin est meilleur chaud.",
             COMPLETE : "Oh, qu'est-ce que c'est que ça? Pour moi?\aGromp, gromp...\aAïïïaïïe! Ma dent! Ce Paul Poulemouillée!\aOh, après tout ce n'est pas ta faute. Voilà, prends ça pour ta peine.",
             },
    903 : { QUEST : "Tu dois te préparer à voir _toNpcName_ le vieillard du blizzard pour ton test final._where_", },
    5234 : { GREETING: "",
             QUEST : "Aha, te revoilà.\aAvant de commencer, nous devons manger.\aApporte-nous du fromage grumeleux pour notre bouillon.\aLe fromage grumeleux ne se trouve que sur les Cogs Gros Blochons.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Nous avons encore besoin de fromage grumeleux." },
    5278 : { GREETING: "",
             QUEST : "Aha, te revoilà.\aAvant de commencer, nous devons manger.\aApporte-nous du caviar pour notre bouillon.\aLe caviar ne se trouve que dans les Cogs M. Hollywood.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Nous avons encore besoin de caviar." },
    5235 : { GREETING: "",
             QUEST : "Un homme ordinaire mange avec une cuillère ordinaire.\aUn Cog a pris ma cuillère ordinaire, donc je ne peux tout simplement pas manger.\aRamène-moi ma cuillère, je crois qu'un Pillard l'a prise.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "J'ai tout simplement besoin de ma cuillère." },
    5279 : { GREETING: "",
             QUEST : "Un homme ordinaire mange avec une cuillère ordinaire.\aUn Cog a pris ma cuillère ordinaire, donc je ne peux tout simplement pas manger.\aRamène-moi ma cuillère, je crois qu'un Chouffleur l'a prise.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "J'ai tout simplement besoin de ma cuillère." },
    5236 : { GREETING: "",
             QUEST : "Merci beaucoup.\aSlurp, slurp...\aAhhh, maintenant tu dois attraper un crapaud parlant. Essaie d'en pêcher dans la mare.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Où est ce crapaud parlant ?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Tu n'as pas encore gagné ton dessert.",
              QUEST : "Oh, c'est vraiment un crapaud parlant. Donne-le moi.\aQu'est-ce que tu dis, crapaud?\aCouac.\aCouac.\aLe crapaud a parlé. Nous avons besoin de dessert.\aRapporte-nous des cônes de glace de chez _toNpcName_.\aLe crapaud aime la glace aux haricots rouges pour une raison inconnue._where_", },
    5238 : { GREETING: "",
             QUEST : "Alors c'est le vieillard du blizzard qui t'envoie. Je dois dire qu'on vient de tomber en rupture de stock de cônes de glace aux haricots rouges.\aTu vois, un groupe de Cogs est venu et les a tous emportés.\aIls ont dit qu'ils étaient pour M. Hollywood ou quelque chose comme ça.\aJe serais ravi si tu pouvais me les rapporter.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu déjà trouvé tous mes cônes de glace ?" },
    5280 : { GREETING: "",
             QUEST : "Alors c'est le vieillard du blizzard qui t'envoie. Je dois dire qu'on vient de tomber en rupture de stock de cônes de glace aux haricots rouges.\aTu vois, un groupe de Cogs est venu et les a tous emportés.\aIls ont dit qu'ils étaient pour le Gros Blochon ou quelque chose comme ça.\aJe serais ravi si tu pouvais me les rapporter.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé tous mes cônes de glace ?" },
    5239 : { QUEST : "Merci de m'avoir rapporté mes cônes de glace!\aEn voilà un pour Allan Bic.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu ferais mieux de porter cette glace à Allan Bic avant qu'elle ne fonde.", },
    5240 : { GREETING: "",
             QUEST : "Très bien. Et voilà mon petit crapaud...\aSlurp, slurp...\aOK, maintenant nous sommes presque prêts.\aSi tu pouvais juste m'apporter de la poudre pour sécher mes mains.\aJe pense que ces Cogs Chouffleurs ont quelquefois de la poudre dans leurs perruques.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé de la poudre ?" },
    5281 : { GREETING: "",
             QUEST : "Très bien. Et voilà mon petit crapaud...\aSlurp, slurp...\aOK, maintenant nous sommes presque prêts.\aSi tu pouvais juste m'apporter de la poudre pour sécher mes mains.\aJe crois que ces Cogs M. Hollywood ont quelquefois de la poudre pour se poudrer le nez.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé de la poudre ?" },
    5241 : { QUEST : "OK.\aComme je l'ai déjà dit, pour bien lancer une tarte, tu ne dois pas la lancer avec la main...\a...mais avec ton âme.\aJe ne sais pas ce que cela veut dire, alors je vais m'asseoir et réfléchir pendant que tu récupères des bâtiments.\aReviens quand tu as terminé ton défi.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ton défi n'est pas terminé.", },
    5242 : { GREETING: "",
             QUEST : "Bien que je ne sache toujours pas de quoi je suis en train de parler, tu es vraiment quelqu'un de valeur.\aJe te donne un dernier défi...\aLe crapaud parlant voudrait une petite amie.\aTrouve un autre crapaud parlant. Le crapaud a parlé.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Où est cet autre crapaud parlant ?",
             COMPLETE : "Houlala! Je suis fatigué par tous ces efforts. Je dois me reposer maintenant.\aTiens, prends ta récompense et va t'en." },

    5243 : { QUEST : "Pierre Lasueur commence à empester dans la rue.\aPeux-tu essayer de le convaincre de prendre une douche par exemple ?_where_" },
    5244 : { GREETING: "",
             QUEST : "Oui, je crois que je dois commencer à transpirer pas mal.\aMmmm, peut-être que si je pouvais réparer ce tuyau qui fuit dans ma douche...\aJe crois qu'un pignon de l'un de ces tous petits Cogs ferait l'affaire.\aVa trouver un pignon de Microchef et on va essayer.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Où est ce pignon que tu étais parti chercher ?" },
    5245 : { GREETING: "",
             QUEST : "Ouaip, on dirait que ça va.\aMais je me sens seul quand je prends ma douche...\aPourrais-tu aller me pêcher un canard en plastique pour me tenir compagnie ?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors ce canard?" },
    5246 : { QUEST : "Le canard en plastique est génial, mais...\aTous ces bâtiments tout autour me rendent nerveux.\aJe me sentirais beaucoup plus détendu s'il y avait moins de bâtiments.",
             LEAVING : "",
             COMPLETE : "Ok, je vais prendre ma douche maintenant. Et voilà aussi quelque chose pour toi.",
             INCOMPLETE_PROGRESS : "Je suis toujours embêté au sujet des bâtiments.", },
    5251 : { QUEST : "Sébastien Toutseul est censé faire un concert ce soir.\aJ'ai entendu dire qu'il pourrait avoir des problèmes avec son matériel._where_" },
    5252 : { GREETING: "",
             QUEST : "Oh ouais! Sûr que j'aurais besoin d'aide.\aCes Cogs sont arrivés et ont piqué tout mon matériel pendant que je déchargeais la camionnette.\aTu pourrais me donner un coup de main pour retrouver mon micro?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hé mon pote, je ne peux pas chanter sans micro." },
    5253 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Attactics a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier ?" },
    5273 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Circulateurs a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier ?" },
    5274 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Usuriers a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier ?" },
    5275 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Avocageots a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier ?" },
    5254 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont sûrement aux pieds d'un M Hollywood.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le Glagla ce soir ?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5282 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Gros Blochon.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le Glagla ce soir ?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5283 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Pillard.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le Glagla ce soir ?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5284 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Chouffleur.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le Glagla ce soir ?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },

    5255 : { QUEST : "On dirait que tu as besoin de plus de rigolpoints.\aPeut-être que tu pourrais passer un marché avec _toNpcName_.\aVérifie que c'est fait par écrit..._where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un marché est un marché.",
             QUEST : "Alors comme ça tu cherches des rigolpoints, hein ?\aJ'ai un marché pour toi!\aOccupe-toi simplement de quelques Cogs Chefbots pour moi...\aEt je te garantis que tu n'y perdras pas." },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un marché est un marché.",
             QUEST : "Alors comme ça tu cherches des rigolpoints, hein ?\aJ'ai un marché pour toi!\aOccupe-toi simplement de quelques Cogs Loibots pour moi...\aEt je te garantis que tu n'y perdras pas." },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "OK, mais je suis sûr de t'avoir dit de ramasser des Cogs Loibots.\aBon, si tu le dis, mais tu m'es redevable.",
             INCOMPLETE_PROGRESS : "Je ne crois pas que tu aies fini.",
             QUEST : "Tu dis que c'est fait ? Tu as vaincu tous les Cogs?\aTu as dû mal comprendre, notre marché portait sur des Cogs Vendibots.\aJe suis certain de t'avoir dit de me vaincre des Cogs Vendibots." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "OK, mais je suis sûr de t'avoir dit de ramasser des Cogs Loibots.\aBon, si tu le dis, mais tu m'es redevable.",
             INCOMPLETE_PROGRESS : "Je ne crois pas que tu aies fini.",
             QUEST : "Tu dis que c'est fait ? Tu as vaincu tous les Cogs?\aTu as dû mal comprendre, notre marché portait sur des Cogs Caissbots.\aJe suis certain de t'avoir dit de me vaincre des Cogs Caissbots." },

    # Eddie the will give you laff point for helping him
    5301 : { QUEST : "Je ne peux pas t'aider pour les rigolpoints, mais peut-être que _toNpcName_ pourra t'arranger.\aAttention: il est un peu caractériel..._where_" },
    5302 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Je t'ai dit quoi?!?!\aMerci bien! Voilà ton rigolpoint!",
             INCOMPLETE_PROGRESS : "Salut!\aQu'est-ce que tu fais encore là?!",
             QUEST : "Un rigolpoint? Je ne crois pas!\aSans problème, mais il va d'abord falloir que tu me débarrasses de quelques-uns de ces fichus Loibots." },

    # Johnny Cashmere will knit you a large bag if...
    5303 : { QUEST : lTheBrrrgh+" est envahi de Cogs très dangereux.\aSi j'étais toi, j'irais là-bas avec plus de gags.\aJ'ai entendu dire que _toNpcName_ peut te faire un grand sac si tu n'as pas peur de marcher._where_" },
    5304 : { GREETING: "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Il devrait y avoir plein de Loibots par là-bas.\aAlors, vas-y!" ,
             QUEST : "Un sac plus grand?\aJe pourrais sûrement t'en coudre un en vitesse.\aMais je vais avoir besoin de fil.\aDes Loibots m'ont volé le mien hier matin." },
    5305 : { GREETING : "Coucou!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Va donc chercher quelques Cogs de plus.\aLa couleur n'a pas encore pris.",
             QUEST : "En voilà du beau fil!\aBon, ce n'est pas ma couleur préférée.\aÉcoute-moi bien...\aTu vas là-bas et tu bousilles quelques-uns des Cogs les plus costauds...\aEt pendant ce temps-là, je vais teindre ton fil." },
    5306 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ils doivent bien être quelque part par là...",
             QUEST : "Voilà, le fil est teint. Mais nous avons un petit problème.\aJe n'arrive pas à trouver mes aiguilles à tricoter.\aLa dernière fois que je les ai vues, c'était près de la mare."  },
    5307 : { GREETING : "",
             LEAVING : "Merci beaucoup!",
             INCOMPLETE_PROGRESS : "Rome ne s'est pas tricoté en un jour!" ,
             QUEST : "Ce sont bien mes aiguilles.\aPendant que je tricote, va faire un peu de nettoyage de Cogs dans ces grands bâtiments.",
             COMPLETE : "Excellent travail!\aEt en parlant de bon travail...\aVoilà ton nouveau sac!" },

    # March Harry can also give you max quest = 4. 
    5308 : { GREETING : "",
             LEAVING : "",
             QUEST : "J'ai entendu dire que _toNpcName_ a des problèmes avec la justice.\aEst-ce que tu pourrais aller le voir et lui demander?_where_"  },
    5309 : { GREETING : "Je suis content de te voir...",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Dépêche-toi! La rue en est envahie!",
             QUEST : "Les Loibots ont vraiment pris le pouvoir dans le quartier.\aJ'ai bien peur qu'ils ne me traînent en justice.\aTu pourrais pas les faire dégager de cette rue?"  },
    5310 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je crois que je les entends qui viennent me chercher...",
             QUEST : "Merci. Je me sens un peu mieux.\a Mais il y a autre chose...\aEst-ce que tu pourrais passer chez _toNpcName_ pour me trouver un alibi?_where_"  },
    5311 : { GREETING : "HOUAAA!!!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je ne peux pas l'aider si tu n'en trouves pas!",
             QUEST : "Un alibi?! Génial!\aTu n'en as pas une autre comme ça?\aJe parie qu'un Avocageot aurait..."  },
    5312 : { GREETING : "Enfin!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "",
             COMPLETE : "Houlala! Je suis vraiment soulagé d'avoir ça.\aVoilà ta récompense...",
             QUEST : "Super! Tu ferais mieux de rapporter ça en vitesse à _toNpcName_!"  },

    # Powers Erge, though forgetful, will give you an LP boost
    # if you'll defeat some Cogs for him
    6201 : { QUEST : "Ali Mentation a besoin d'aide. Peux-tu y faire un saut et lui donner un coup de main ?_where_",
             },
    6202 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, un client! Super! Que puis-je faire pour toi?\aComment ça, que peux-tu faire pour moi? OH! Tu n'es pas un client.\aJe m'en souviens maintenant. Tu es là pour m'aider avec ces affreux Cogs.\aEh bien, ton aide me sera certainement bien utile, même si tu n'es pas un client.\aSi tu nettoies un peu les rues, je te réserve un petit quelque chose.",
             INCOMPLETE_PROGRESS : "Si tu ne veux pas d'électricité, je ne peux rien faire pour toi tant que tu n'as pas vaincu ces Cogs.",
             COMPLETE : "Bon boulot avec ces Cogs, _avName_.\aTu es vraiment sûr(e) que tu n'as pas besoin d'électricité? Ça pourrait t'être utile...\aNon ? OK, comme tu voudras.\aQuoi? Ah oui, je me souviens. Et voilà. Ça te sera sûrement utile contre ces méchants Cogs.\aContinue à bien travailler!",
             },

    # Susan Siesta wants to get rich but the Cogs are interfering.
    # Take out some Cog buildings and she'll give you the small backpack
    6206 : { QUEST : "Eh bien, _avName_, je n'ai rien pour toi pour le moment.\aAttends! Je crois que Susan Sieste cherchait de l'aide. Pourquoi n'irais-tu pas la voir ?_where_",
             },
    6207 : { GREETING : "",
             LEAVING : "",
             QUEST : "Je ne serai jamais riche avec ces satanés Cogs qui ruinent mes affaires!\aIl faut que tu m'aides, _avName_.\aNettoie quelques bâtiments Cog pour le bien de tout le voisinage et je te rendrai plus riche.",
             INCOMPLETE_PROGRESS : "Pauvre de moi! Tu ne peux pas te débarrasser de ces bâtiments?",
             COMPLETE : "À moi la fortune! Je vois ça d'ici!\aJe passerai tout mon temps à la pêche. Maintenant, laisse-moi t'enrichir un peu.\aEt voilà!",
             },

    # Lawful Linda is fixing her answering machine.
    # Help her & she'll give you a 2LP reward.
    6211 : { QUEST : "Hé _avName_! J'ai entendu dire que Linda Kapok te cherchait.\aTu devrais passer lui rendre visite._where_",
             },
    6212 : { GREETING : "",
             LEAVING : "",
             QUEST : "Bonjour! Waouh, ce que je suis contente de te voir!\aJ'ai passé mon temps à réparer ce répondeur pendant mon temps libre mais il me manque des pièces.\aJ'ai besoin de trois tiges supplémentaires et celles des Pince Menus ont l'air de bien marcher.\aPourrais-tu m'en trouver quelques-unes?",
             INCOMPLETE_PROGRESS : "Toujours en train de chercher ces tiges?",
             },
    6213 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, ces tiges iront très bien.\aC'est drôle. J'étais sûre d'avoir une courroie de rechange quelque part mais je n'arrive pas à la trouver.\aPourrais-tu m'en rapporter une de chez Sacasous, s'il te plaît ? Merci!",
             INCOMPLETE : "Non, je ne peux pas t'aider avant d'avoir cette courroie.",
             },
    6214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Voilà, c'est ça. Maintenant ça devrait marcher comme sur des roulettes.\aOù sont passées mes pinces? Je ne peux pas fixer ça sans mes pinces.\aPeut-être qu'une tenaille de Radino ferait l'affaire ?\aSi tu vas m'en chercher une, je te donnerai un petit quelque chose qui t'aidera contre les Cogs.",
             INCOMPLETE_PROGRESS : "Toujours pas de tenaille, hein ? Continue à chercher.",
             COMPLETE : "Génial! Maintenant il ne me reste plus qu'à fixer tout ça.\aÇa a l'air de marcher maintenant. Me voilà de retour aux affaires!\aEuh, sauf que nous n'avons pas de téléphone. Mais merci quand même de ton aide.\aJe pense que ça t'aidera contre les Cogs. Bonne chance!",
             },

    # Scratch Rocco's back and he'll scratch yours.
    # In fact, he'll give you a 3 LP bonus.
    6221 : { QUEST : "J'ai entendu dire que Rocco avait besoin d'aide. Va voir ce que tu peux faire pour lui._where_",
             },
    6222 : { GREETING : "",
             LEAVING : "",
             QUEST : "Yo! Tu tombes à pic. Moi, ça va pas mieux.\aOuais, j'aurais besoin d'un coup de main avec ces Cogs. Ils sont tout le temps là, à essayer de me donner des leçons.\aSi tu pouvais mettre hors d'état de nuire certains de ces Chefbots, je f'rais en sorte que t'aies pas perdu ton temps.",
             INCOMPLETE_PROGRESS : "Eh, _avName_, qu'est-ce que tu fiches?\aFaut qu'tu fasses la chasse à ces Chefbots. On a un accord, tu te rappelles?\aRocco tient toujours sa parole.",
             COMPLETE : "Yo, _avName_! Toi, t'es OK pour moi.\aCes Chefbots ils font moins les malins maintenant, pas vrai?\aEh voilà! Un bon petit coup de boost. Maintenant, évite les ennuis, t'entends?",
             },

    # Nat & PJ will get you acquainted with the new
    # HQ. And they'll give you your first suit part
    6231 : { QUEST : "Place de la couette, Plume a entendu des rumeurs à propos du quartier général Caissbot.\aVa y faire un tour et vois si tu peux l'aider._where_",
             },
    6232 : { GREETING : "",
             LEAVING : "",
             QUEST : "J'ai entendu dire qu'il se passait de drôles de choses.\aBon, c'est peut-être un coup des puces mais il se passe quelque chose de toute façon.\aTous ces Caissbots!\aIJe pense qu'ils ont installé un nouveau quartier général tout près de la Place de la Couette.\aP.J. connaît bien le coin.\aVa voir _toNpcName_ _where_ Demande-lui s'il a entendu quelque chose.",
             INCOMPLETE_PROGRESS : "Tu n'as pas encore vu P.J.? Qu'est-ce qui t'en empêche ?\aAh, ces satanées puces!",
             },
    6233 : { GREETING : "",
             LEAVING : "",
             QUEST : "Salut _avName_, où vas-tu?\aUn quartier général Caissbot ?? Je n'ai rien vu.\aTu pourrais aller au bout de la place de la Couette et voir si c'est vrai?\aTrouve quelques Caissbots dans leur quartier général, bats-en quelques-uns et reviens me le dire.",
             INCOMPLETE_PROGRESS : "Pas encore trouvé le QG? Tu dois y aller, vaincre des Caissbots et voir ce qui s'y passe.",
             },
    6234 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quoi?! Il y a DÉJÀ un QG Caissbot ?\aTu ferais mieux d'aller tout de suite le dire à Plume!\aQui aurait pu deviner qu'il y aurait un QG Cog à deux pas de sa rue ?",
             INCOMPLETE_PROGRESS : "Qu'est-ce que Plume t'a dit ? Tu ne l'as pas encore vu?",
             },
    6235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Je suis impatient de savoir ce que P.J. a dit.\aHmm... on a besoin de plus d'informations sur cette affaire de Cogs mais je dois me débarrasser de ces puces!\aJe sais! TOI, tu peux essayer d'en savoir plus!\aVa vaincre des Caissbots au QG jusqu'à ce que tu trouves des plans. Après, tu reviens me voir!",
             INCOMPLETE_PROGRESS : "Toujours pas de plans? Continue à chercher les Cogs!\aIls doivent avoir des plans!",
             COMPLETE : "Tu as les plans?\aGénial! Voyons voir ce qu'ils disent.\aJe vois... Les Caissbots ont construit une Fabrique à Sous pour fabriquer des euros Cog.\aÇa doit être PLEIN de Caissbots. On devrait essayer d'en savoir plus.\aPeut-être que si tu avais un déguisement... Hmmm... attends! Je crois que j'ai une pièce de costume de Cog quelque part par là....\aLa voilà! Prends-la en récompense de tes efforts! Merci encore de ton aide!",
             },

    # The Countess can't concentrate on counting her sheep with all 
    # these Cogs around. Clean up a bit and she'll reward you handsomely.
    # Reward: MaxMoneyReward 705 - 150 jellybeans
    6241 : { QUEST : "La comtesse te cherchait partout! S'il te plaît, va lui rendre visite, comme ça elle arrêtera d'appeler._where_",
             },
    6242 : { GREETING : "",
             LEAVING : "",
             QUEST : "_avName_, je compte sur toi pour m'aider!\aTu vois, ces Cogs font tellement de bruit que je ne peux tout simplement pas me concentrer.\aJe n'arrête pas de perdre le compte de mes moutons!\aSi tu fais diminuer ce bruit, je t'aiderai aussi! Tu peux compter là-dessus!\aBon, où en étais-je ? C'est ça, cent trente-six, cent trente-sept...",
             INCOMPLETE_PROGRESS : "Quatre cent quarante-deux... quatre cent quarante-trois...\aQuoi? Tu es déjà de retour ? Mais il y a toujours trop de bruit!\aAh non, j'ai encore perdu le compte.\a Un...deux...trois...",
             COMPLETE : "Cinq cent quatre-vingt-treize... cinq cent quatre-vingt-quatorze..\aHello! Ah, je savais que je pouvais compter sur toi! C'est beaucoup plus calme maintenant.\aEt voilà, pour tous ces Gobechiffres.\aLe nombre ? Maintenant il faut que je recommence à compter depuis le début! Un...deux....",
             },

    # Zari needs you to run some errands for her and maybe
    # wipe out some Cogs along the way. She'll make it worthwhile
    # though, she'll give you 4 LP if you run the gauntlet.
    6251 : { QUEST : "Ce pauvre père San a cassé son zipper et maintenant il ne peut plus livrer ses clients. Ton aide lui sera certainement utile._where_",
             },
    6252 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, bonjour _avName_. Tu es là pour m'aider à faire mes livraisons?\aC'est génial! Avec ce zipper cassé, c'est difficile de se déplacer.\aVoyons voir... OK, ça devrait être facile. Ron Chonneau a commandé une cithare la semaine dernière.\aPourrais-tu la lui apporter ? _where_",
             INCOMPLETE_PROGRESS : "Ah, salut! Tu as oublié quelque chose ? Ron Chonneau attend sa cithare.",
             },
    6253 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ma cithare! Enfin! Bon sang, je suis impatient d'en jouer.\aVa dire au père San que je le remercie, tu veux?",
             INCOMPLETE_PROGRESS : "Merci encore pour la cithare. Le père San n'a pas d'autres livraisons pour toi?",
             },
    6254 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quelle rapidité! Quelle est la prochaine livraison sur ma liste ?\aBon. Mike Mac a commandé une surfaceuse. Quel drôle de type.\aTu peux la lui apporter, s'il te plaît ?_where_",
             INCOMPLETE_PROGRESS : "Cette surfaceuse est pour Mike Mac._where_",
             },
    6255 : { GREETING : "",
             LEAVING : "",
             QUEST : "Super! La surfaceuse que j'avais commandée!\aMaintenant, si seulement il n'y avait pas autant de Cogs dans les environs, je pourrais avoir le temps de m'en servir.\aSois sympa et occupe-toi de certains de ces Caissbots pour moi, tu veux?",
             INCOMPLETE_PROGRESS : "Ces Caissbots résistent, hein ? Avec eux, pas facile d'essayer ma surfaceuse.",
             },
    6256 : { GREETING : "",
             LEAVING : "",
             QUEST : "Excellent! Maintenant je peux essayer ma surfaceuse.\aS'il te plaît, dis au père San que je viendrai la semaine prochaine passer ma prochaine commande.",
             INCOMPLETE_PROGRESS : "C'est tout ce dont j'ai besoin pour le moment. Est-ce que le père San n'est pas en train de t'attendre ?"
             },
    6257 : { GREETING : "",
             LEAVING : "",
             QUEST : "Alors, est-ce que Mike Mac a été content de sa surfaceuse ? Génial.\aÀ qui le tour ? Ah, Olivier Daure a commandé un coussin zèbre.\aLe voilà! Pourrais-tu faire un saut chez lui, s'il te plaît ?_where_",
             INCOMPLETE_PROGRESS : "Je crois qu'Olivier Daure a besoin de ce coussin pour méditer.",
             },
    6258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, mon coussin, enfin. Maintenant je peux méditer.\aComment se concentrer avec un tel vacarme ? Tous ces Cogs!\aComme tu es là, peut-être que tu pourrais t'occuper de certains de ces Cogs?\aAprès ça je pourrai utiliser mon coussin en paix.",
             INCOMPLETE_PROGRESS : "Il y a toujours tellement de bruit avec ces Cogs! Comment se concentrer ?",
             },
    6259 : { GREETING : "",
             LEAVING : "",
             QUEST : "La paix et le calme, enfin. Merci, _avName_.\aS'il te plaît, va dire au père San que je suis très content. OMMM....",
             INCOMPLETE_PROGRESS : "Le père San t'as appelé. Tu devrais aller voir ce qu'il veut.",
             },
    6260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Je suis heureux de voir qu'Olivier Daure est content de son coussin zèbre.\aOh, ces zinnias viennent juste d'arriver pour Eva Sandor-Mir.\aComme tu as l'air d'être un livreur zélé, peut-être que tu pourrais les lui apporter ?_where_",
             INCOMPLETE_PROGRESS : "Ces zinnias vont faner si tu ne les livres pas rapidement.",
             },
    6261 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quels jolis zinnias! Ca c'est sûr, le père San s'y connaît en livraison.\aOh, eh bien, je suppose que c'est TOI qui fais les livraisons, _avName_. Tu remercieras le père San pour moi!",
             INCOMPLETE_PROGRESS : "N'oublie pas de remercier le père San pour les zinnias!",
             },
    6262 : { GREETING : "",
             LEAVING : "",
             QUEST : "Te voilà de retour, _avName_. Tu es sacrément rapide.\aVoyons... Quelle est la prochaine livraison sur ma liste ? Des disques de Zydeco pour Thérèse Eveillé._where_",
             INCOMPLETE_PROGRESS : "Je suis sûr que Thérèse Eveillé attend ses disques de Zydeco.",
             },
    6263 : { GREETING : "",
             LEAVING : "",
             QUEST : "Des disques de Zydeco? Je ne me rappelle pas avoir commandé de disques de Zydeco.\aOh, je parie que c'est Lou Laberceuse qui les a commandés._where_",
             INCOMPLETE_PROGRESS : "Non, ces disques de Zydeco sont pour Lou Laberceuse._where_",
             },
    6264 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, enfin, mes disques de Zydeco! Je pensais que le père San avait oublié.\aPourrais-tu lui apporter cette courgette ? Il trouvera bien quelqu'un qui en veut une. Merci!",
             INCOMPLETE_PROGRESS : "Oh, j'ai déjà plein de courgettes. Apporte-la au père San.",
             },
    6265 : { GREETING : "",
             LEAVING : "",
             QUEST : "Une courgette ? Hmm. Eh bien, je trouverai sûrement quelqu'un qui en voudra.\aOK, nous avons presque fini ma liste. Plus qu'une livraison à faire.\aBébé MacDougal a commandé un costume zazou._where_",
             INCOMPLETE_PROGRESS : "Si tu ne livres pas ce costume zazou à Bébé MacDougal,\a il va être tout froissé.",
             },
    6266 : { GREETING : "",
             LEAVING : "",
             QUEST : "Il était une fois... oh! Tu n'es pas là pour écouter une histoire, hein ?\aTu es là pour me livrer mon costume zazou? Super! Waouh, c'est quelque chose.\aEh, tu pourrais transmettre un message au père San pour moi? J'aurais besoin de boutons de manchette en zircon pour aller avec le costume. Merci!",
             INCOMPLETE_PROGRESS : "Tu as transmis mon message au père San ?",
             COMPLETE : "Des boutons de manchette en zircon, hein ? Eh bien, je vais voir ce que je peux faire pour lui.\aBon, tu m'as été d'une aide précieuse et je ne peux pas te laisser partir sans rien.\aVoici un GROS coup de boost pour t'aider à zapper ces Cogs!",
             },

    # Drowsy Dave will give you teleport access to DL
    # if he can stay awake long enough for you to finish.
    6271 : { QUEST : "Dave Bigleau a des problèmes et tu peux peut-être l'aider. Pourquoi ne pas passer à sa boutique ?_where_",
             },
    6272 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quoi? Hein ? Oh, j'ai dû m'endormir.\aTu sais, ces bâtiments Cog sont remplis de machines qui me donnent vraiment sommeil.\aJe les entends ronronner toute la journée et...\aHein ? Ah, ouais, d'accord. Si tu pouvais te débarrasser de certains de ces bâtiments Cog, je pourrais rester éveillé.",
             INCOMPLETE_PROGRESS : "Zzzzz...hein ? Oh, c'est toi, _avName_.\aDéjà de retour ? Je faisais juste une petite sieste.\aReviens quand tu en auras fini avec ces bâtiments.",
             COMPLETE : "Quoi? Je me suis juste assoupi une minute.\aMaintenant que ces bâtiments Cog ont disparu, je peux enfin me détendre.\aMerci de ton aide, _avName_.\aA plus tard! Je crois que je vais faire un petit somme.",
             },

    # Teddy Blair has a piece of a cog suit to give you if you will
    # clear out some cogs. Of course, his ear plugs make it tough.
    6281 : { QUEST : "Va voir Teddy Blaireau. Il a un boulot pour toi._where_",
             },
    6282 : { GREETING : "",
             LEAVING : "",
             QUEST : "Qu'est-ce que tu dis? Non, je n'ai pas de goulot pour toi.\aOh, un boulot! Pourquoi ne pas l'avoir dit plus tôt ? Il faudrait que tu parles plus fort.\aAvec ces Cogs, ce n'est pas facile d'hiberner. Si tu ramènes un peu de calme au Pays des Rêves,\aje te donnerai un petit quelque chose.",
             INCOMPLETE_PROGRESS: "Tu as vaincu les bogs? Quels bogs?\aOh, les Cogs! Pourquoi ne pas l'avoir dit plus tôt ?\aHmm, il y a encore pas mal de bruit. Pourquoi ne pas en vaincre quelques autres?",
             COMPLETE : "Tu t'es bien amusé? Hein ? Oh!\aTu as fini! Super. C'est sympa de ta part de donner un coup de main comme ça.\aJ'ai trouvé ça dans la pièce du fond mais ça ne m'est d'aucune utilité.\aPeut-être que tu pourras en faire quelque chose. À plus, _avName_!",
             },

    # William Teller needs help! Those darn Cashbots swiped his 3
    # money bags to use in the Mint! Retrieve them and he'll give you
    # another cog Suit piece
    6291 : { QUEST : "Les Cogs ont pénétré dans la Banque du Doudou d'Or! Va voir Laurent Lauronpat et vois si tu peux l'aider.",
             },
    6292 : { QUEST : "Ah ces satanés Caissbots! Ils ont volé mes lampes de lecture!\aJ'en ai besoin tout de suite. Tu peux aller les chercher ?\aSi tu me rapportes mes lampes de lecture, je pourrai peut-être t'aider à rencontrer le Vice-Président.\aFais vite!",
             INCOMPLETE_PROGRESS : "Il me faut ces lampes. Continue de les chercher!",
             COMPLETE : "Te voilà revenu! Et tu as mes lampes!\aJe ne peux pas te remercier comme il le faudrait mais je peux te donner ça.",
             },

    # Help Nina Nightlight get a bed in stock -
    # she'll give you a suit part
    7201 : { QUEST : "Nina Lamparo te cherchait, _avName_. Elle a besoin d'aide._where_",
             },
    7202 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah! Je suis si contente de te voir, _avName_. J'aurais bien besoin d'aide!\aCes fichus Cogs ont chassé les livreurs et je n'ai plus aucun lit en stock.\aPeux-tu aller voir Amédé Brouilletoitoutseul et me rapporter un lit ?_where_",
             INCOMPLETE_PROGRESS : "Amédé n'avait pas de lit ? J'étais sûre qu'il en avait un.",
             COMPLETE : "",
             },
    7203 : { GREETING : "",
             LEAVING : "",
             QUEST : "Un lit ? Bien sûr, en voilà un de prêt.\aApporte-le-lui pour boi, tu veux? Tu as compris? Pour \a\" BOIS \"? Hi-hi!\aTrès drôle, non ? Eh bien, amène-le quand même là-bas s'il te plaît.",
             INCOMPLETE_PROGRESS : "Est-ce que le lit a plu à Nina?",
             COMPLETE : "",
             },
    7204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ce lit ne convient pas. Il est beaucoup trop ordinaire.\aVa voir s'il a quelque chose de plus fantaisie, tu veux?\aJe suis sûre que ça ne te prendra qu'une minute.",
             INCOMPLETE_PROGRESS : "Je suis sûre qu'Amédé a un lit plus fantaisie.",
             COMPLETE : "",
             },
    7205 : { GREETING : "",
             LEAVING : "",
             QUEST : "On n'est pas tombé pile avec ce lit, hein ? J'en ai un ici qui devrait faire l'affaire.\aMais il y a un petit problème - il faut d'abord l'assembler.\aPendant que je m'en charge avec mon marteau, pourrais-tu te débarrasser de certains des Cogs, là-dehors?\aCes affreux Cogs ruinent mon travail.\aReviens quand tu auras fini et le lit sera prêt.",
             INCOMPLETE_PROGRESS : "Je n'ai pas tout à fait fini d'assembler le lit.\aQuand tu en auras fini avec les Cogs, il sera prêt.",
             COMPLETE : "",
             },
    7206 : { GREETING : "",
             LEAVING : "",
             QUEST : "Salut _avName_!\aTu as fait du sacré bon boulot avec ces Cogs.\aLe lit est prêt. Pourrais-tu le livrer pour moi?\aMaintenant que tous ces Cogs sont partis, les affaires vont reprendre!",
             INCOMPLETE_PROGRESS : "Je pense que Nina attend la livraison de ce lit.",
             COMPLETE : "Quel joli lit!\aMaintenant mes clients vont être contents. Merci, _avName_.\aTiens, ceci pourra peut-être t'être utile. Quelqu'un l'a laissé ici.",
             },
    7209 : { QUEST : "Va voir Rosée de Lune. Elle a besoin d'aide._where_",
             },
    7210 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh! Comme je suis contente de te voir, _avName_. J'ai vraiment besoin d'aide!\aJe n'ai pas eu mon compte de sommeil depuis bien longtemps. Tu vois, les Cogs m'ont volé mon dessus-de-lit.\aTu pourrais faire un saut voir si Ed n'aurait rien dans les tons bleus?_where_",
             INCOMPLETE_PROGRESS : "Qu'est-ce qu'Ed a dit à propos de ce dessus-de-lit bleu?",
             COMPLETE : "",
             },
    7211 : { GREETING : "",
             LEAVING : "",
             QUEST : "Alors comme ça, Rosée veut un dessus-de-lit, hein ?\aDe quelle couleur ? BLEU?!\aEh bien, je vais devoir le fabriquer spécialement pour elle. Tout ce que j'ai, c'est du rouge.\aTu sais quoi? Si tu vas t'occuper de certains des Cogs là-dehors, je fabriquerai un dessus-de-lit bleu spécialement pour elle.\aDes dessus-de-lit bleus... et puis quoi encore ?",
             INCOMPLETE_PROGRESS : "Je travaille toujours sur ce dessus-de-lit bleu, _avName_. Continue de t'occuper de ces Cogs!",
             COMPLETE : "",
             },
    7212 : { GREETING : "",
             LEAVING : "",
             QUEST : "Content de te revoir. J'ai quelque chose pour toi!\aVoilà le dessus-de-lit et il est bleu. Elle va l'adorer.",
             INCOMPLETE_PROGRESS : "Est-ce que Rosée a aimé le dessus-de-lit ?",
             COMPLETE : "",
             },
    7213 : { GREETING : "",
             LEAVING : "",
             QUEST : "C'est mon dessus-de-lit ? Non, ça ne va pas.\aC'est un tissu ÉCOSSAIS! Qui pourrait dormir avec un motif aussi CRIARD?\aTu vas devoir le rapporter et m'en ramener un autre.\aJe suis sûre qu'il en a d'autres.",
             INCOMPLETE_PROGRESS : "Il est hors de question que j'accepte un dessus-de-lit écossais. Va voir ce qu'Ed peut faire.",
             COMPLETE : "",
             },
    7214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quoi? Elle n'aime pas l'ÉCOSSAIS?\aHmm... Voyons ce que nous avons par ici.\aÇa va prendre un certain temps. Pourquoi tu n'irais pas t'occuper de quelques Cogs pendant que j'essaie de trouver autre chose ?\aJ'aurai trouvé quand tu reviendras.",
             INCOMPLETE_PROGRESS : "Je suis toujours en train de chercher un autre dessus-de-lit. Comment ça se passe avec les Cogs?",
             COMPLETE : "",
             },
    7215 : { GREETING : "",
             LEAVING : "",
             QUEST : "Hé, bon travail avec ces Cogs!\aEt voilà, il est bleu et il n'est pas écossais.\aReste à espérer qu'elle aime le cachemire.\aApporte ce dessus-de-lit à Rosée.",
             INCOMPLETE_PROGRESS : "C'est tout ce que j'ai pour toi pour l'instant.\aS'il te plaît, va apporter ce dessus-de-lit à Rosée.",
             COMPLETE : "Oh! Que c'est joli! Le cachemire me va vraiment bien.\aIl est temps pour moi de prendre un peu de repos! À plus tard, _avName_.\aQuoi? Tu es encore là? Tu ne vois pas que j'essaie de dormir ?\aTiens, prends ça et laisse-moi me reposer. Je dois être à faire peur!",
             },

    7218 : { QUEST : "Daphné Puisé aurait bien besoin d'un coup de main._where_",
             },
    7219 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, _avName_, je suis contente de te voir! Les Cogs ont pris mes oreillers.\aPourrais-tu aller voir si Pierrot en a?_where_\aJe suis sûre qu'il peut m'aider.",
             INCOMPLETE_PROGRESS : "Est-ce que Pierrot a des oreillers pour moi ?",
             COMPLETE : "",
             },
    7220 : { GREETING : "",
             LEAVING : "",
             QUEST : "Salut! Daphné a besoin d'oreillers, hein ? Eh bien, tu as frappé à la bonne porte, partenaire!\aIl y a plus d'oreillers ici que d'épines sur un cactus.\aEt voilà, _avName_. Apporte-les à Daphné, avec mes compliments.\aToujours heureux de donner un coup de main à une demoiselle.",
             INCOMPLETE_PROGRESS : "Ces oreillers sont-ils assez doux pour cette jeune dame ?",
             COMPLETE : "",
             },
    7221 : { GREETING : "",
             LEAVING : "",
             QUEST : "Tu as les oreillers! Génial!\aEh, attends une seconde! Ces oreillers sont affreusement mous.\aBeaucoup trop mous pour moi. J'ai besoin d'oreillers plus durs.\aRamène-les à Pierrot et vois ce qu'il a d'autre. Merci.",
             INCOMPLETE_PROGRESS : "Non! Trop mous. Demande d'autres oreillers à Pierrot.",
             COMPLETE : "",
             },
    7222 : { GREETING : "",
             LEAVING : "",
             QUEST : "Trop mous, hein ? Eh bien, laisse-moi voir ce que j'ai d'autre....\aHmm... Il me semblait que j'avais un bon paquet d'oreillers durs. Où sont-ils passés?\aOh! Je me rappelle. Je pensais les renvoyer, donc ils sont à l'entrepôt.\aPourquoi tu ne nettoierais pas quelques bâtiments Cog là-dehors pendant que je les sors de l'entrepôt, partenaire ?",
             INCOMPLETE_PROGRESS : "Dur, dur les bâtiments Cog. C'est pas comme ces oreillers.\aContinue à chercher.",
             COMPLETE : "",
             },
    7223 : { GREETING : "",
             LEAVING : "",
             QUEST : "Déjà de retour ? Eh bien, c'est parfait. Tu vois, j'ai trouvé les oreillers que Daphné voulait.\aMaintenant, va les lui apporter. Ils sont tellement durs qu'on s'y casserait les dents!",
             INCOMPLETE_PROGRESS : "Ouais, ces oreillers sont bien durs. J'espère qu'ils plairont à Daphné.",
             COMPLETE : "Je savais bien que Pierrot aurait des oreillers plus durs.\aAh oui, ils sont parfaits. Bien durs, juste comme je les aime.\aTu aurais besoin de cette pièce de costume de Cog? Tu n'as qu'à la prendre.",
             },

    # Sandy Sandman lost her pajamas but Big Mama
    # and Cat can help her out. If you hang in there,
    # you'll get another Cog Suit part.
    7226 : { QUEST : "Passe voir Sandie Marchand. Elle a perdu son pyjama._where_",
             },
    7227 : { GREETING : "",
             LEAVING : "",
             QUEST : "Je n'ai plus de pyjama! Je ne le trouve plus!\aQu'est-ce que je vais faire ? Oh! Je sais!\aVa voir Big Mama. Elle aura sûrement un pyjama pour moi._where_",
             INCOMPLETE_PROGRESS : "Est-ce que Big Mama a un pyjama pour moi?",
             COMPLETE : "",
             },
    7228 : { GREETING : "",
             LEAVING : "",
             QUEST : "Te voilà, petit Toon! Big Mama a les plus beaux pyjamas des Bahamas.\aOh, quelque chose pour Sandie Marchand, hein ? Bon, voyons voir ce que j'ai.\aVoilà un petit quelque chose. Maintenant elle peut dormir en toute élégance!\aVoudrais-tu courir le lui apporter pour moi? Je ne peux pas quitter la boutique pour l'instant.\aMerci, _avName_. À plus tard!",
             INCOMPLETE_PROGRESS : "Tu dois apporter ce pyjama à Sandie._where_",
             COMPLETE : "",
             },
    7229 : { GREETING : "",
             LEAVING : "",
             QUEST : "C'est Big Mama qui me l'envoie ? Oh...\aEst-ce qu'elle n'a pas de pyjama avec des pieds?\aJe porte toujours des pyjamas avec des pieds. Comme tout le monde, non ?\aRamène celui-là et demande-lui de m'en trouver un avec des pieds.",
             INCOMPLETE_PROGRESS : "Mon pyjama doit avoir des pieds. Va voir si Big Mama peut m'aider.",
             COMPLETE : "",
             },
    7230 : { GREETING : "",
             LEAVING : "",
             QUEST : "Des pieds? Laisse-moi réfléchir....\aAttends un peu! J'ai ce qu'il te faut!\aTa-dam! Un pyjama avec des pieds. Une jolie grenouillère bleue avec des pieds. La meilleure de toutes les îles.\aS'il te plaît, va-la-lui porter, tu veux? Merci!",
             INCOMPLETE_PROGRESS : "Est-ce que Sandie a aimé la grenouillère bleue ?",
             COMPLETE : "",
             },
    7231 : { GREETING : "",
             LEAVING : "",
             QUEST : "OK, elle a EFFECTIVEMENT des pieds, mais je ne peux pas porter une grenouillère bleue!\aDemande à Big Mama si elle n'a pas une autre couleur.",
             INCOMPLETE_PROGRESS : "Je suis sûre que Big Mama a une grenouillère d'une autre couleur.",
             COMPLETE : "",
             },
    7232 : { GREETING : "",
             LEAVING : "",
             QUEST : "Quel dommage. C'est la seule grenouillère que j'aie.\aOh, j'ai une idée. Va demander à Tartine. Elle aura peut-être des pyjamas avec des pieds._where_",
             INCOMPLETE_PROGRESS : "Non, ce sont les seuls pyjamas que j'aie. Va voir si Tartine en a._where_",
             COMPLETE : "",
             },
    7233 : { GREETING : "",
             LEAVING : "",
             QUEST : "Des pyjamas avec des pieds? Bien sûr.\aQu'est-ce que tu veux dire, il est bleu? Elle n'aime pas le bleu?\aOh, alors là, c'est plus compliqué. Tiens, essaie ça.\aIl n'est pas bleu et il A des pieds.",
             INCOMPLETE_PROGRESS : "Moi j'adore la couleur puce, pas toi?\aJ'espère que Sandie l'aimera....",
             COMPLETE : "",
             },
    7234 : { GREETING : "",
             LEAVING : "",
             QUEST : "Non, il n'est pas bleu mais personne avec mon teint ne peut porter de couleur puce.\aAbsolument impossible. Retourne là-bas et rapporte-le! Va voir ce que Tartine a d'autre.",
             INCOMPLETE_PROGRESS : "Tartine doit avoir d'autres pyjamas. La couleur puce, hors de question pour moi!",
             COMPLETE : "",
             },
    7235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Pas de puce non plus. Hmm....\aPar ma barbe, je sais que j'en ai d'autres.\aIl va me falloir un moment pour les trouver. Faisons un marché.\aJe cherche d'autres grenouillères si tu te débarrasses de quelques bâtiments Cog. Ils sont vraiment gênants.\aLa grenouillère sera prête quand tu reviendras, _avName_.",
             INCOMPLETE_PROGRESS : "Tu dois éliminer d'autres bâtiments Cog pendant que je cherche d'autres grenouillères.",
             COMPLETE : "",
             },
    7236 : { GREETING : "",
             LEAVING : "",
             QUEST : "Tu as fait de l'excellent travail avec ces Cogs! Merci!\aJ'ai trouvé cette grenouillère pour Sandie, j'espère que ça lui plaira.\aApporte-la-lui. Merci.",
             INCOMPLETE_PROGRESS : "Sandie attend sa grenouillère, _avName_.",
             COMPLETE : "Une grenouillère fuchsia! Parr-fait!\aAh, maintenant je suis parfaitement bien. Voyons voir....\aOh, je suppose que je devrais te donner quelque chose pour te remercier de ton aide.\aPeut-être que ceci te sera utile. Quelqu'un l'a laissé ici.",
             },

    # Smudgy Mascara needs Wrinkle Cream but
    # 39's missing ingredients. Help them out
    # and get a piece of Cog suit
    7239 : { QUEST : "Va voir Emma Scara. Elle demande de l'aide._where_",
             },
    7240 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ces satanés Cogs ont pris ma crème antirides!\aMes clients DOIVENT absolument avoir de la crème antirides quand je m'occupe d'eux.\aVa voir Honoré et demande-lui s'il a toujours ma recette spéciale en stock._where_",
             INCOMPLETE_PROGRESS : "Je refuse de m'occuper de quelqu'un qui n'a pas de crème antirides.\aVa voir si Honoré en a.",
             },
    7241 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, cette Emma n'est pas facile. Elle ne se contente pas de ma recette habituelle.\aCe qui veut dire que je vais avoir besoin de corail chou-fleur, mon ingrédient spécial ultrasecret. Mais je n'en ai pas en stock.\aPourrais-tu aller m'en pêcher dans l'étang? Dès que tu auras le corail, je préparerai un mélange de crème pour Emma.",
             INCOMPLETE_PROGRESS : "J'ai besoin de corail chou-fleur pour préparer ma crème antirides.",
             },
    7242 : { GREETING : "",
             LEAVING : "",
             QUEST : "Waouh, quel beau corail chou-fleur!\aOk, voyons voir... Un peu de ceci et une petite giclée de cela... Et maintenant, une cuillerée d'algues.\aHé, où sont les algues? On dirait que je suis aussi à court d'algues.\aPeux-tu faire un saut à l'étang et me ramasser une belle algue gluante ?",
             INCOMPLETE_PROGRESS : "Plus un brin d'algue gluante dans cette boutique.\aImpossible de préparer la crème sans algue.",
             },
    7243 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oooh! Voilà une algue gluante à souhait, _avName_.\aMaintenant, je vais juste écraser quelques perles dans le mortier avec le pilon.\aHum, où est mon pilon ? À quoi sert un mortier sans un pilon ?\aJe parie que ce fichu Usurier l'a pris quand il est venu ici!\aIl faut que tu m'aides à le trouver! Il se dirigeait vers le QG Caissbot!",
             INCOMPLETE_PROGRESS : "Je ne peux tout simplement pas écraser mes perles sans un pilon.\aFichus Usuriers!",
             },
    7244 : { GREETING : "",
             LEAVING : "",
             QUEST : "Parfait! Tu as mon pilon!\aMaintenant on va pouvoir travailler. Écraser ça... Touiller un peu et...\aÇa y est! Va dire à Emma que c'est de la bonne crème, fraîchement préparée.",
             INCOMPLETE_PROGRESS : "Tu devrais apporter cette crème à Emma tant qu'elle est encore fraîche.\aC'est une cliente très difficile.",
             COMPLETE : "Honoré n'avait pas un pot de crème antirides plus gros que ça? Non ?\aEh bien, je suppose qu'il faudra simplement que j'en recommande quand je n'en aurai plus.\aÀ un de ces quatre, _avName_.\aQuoi? Tu es toujours là? Tu ne vois pas que j'essaie de travailler ?\aTiens, prends ça.",
             },

# Lawbot HQ part quests
    11000 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu es intéressé par les pièces de déguisement de Loibot, tu devrais aller voir _toNpcName_.\aJ'ai entendu dire qu'il a grand besoin d'aide pour ses recherches météorologiques._where_",
              },
    11001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Oui, oui. J'ai des pièces de déguisement de Loibot.\aMais elles sont sans intérêt pour moi.\aMes recherches portent sur les fluctuations de la température ambiante de Toontown.\aJ'échangerais volontiers des pièces de déguisement contre des sondes de température Cog.\aTu peux commencer par aller voir %s." % GlobalStreetNames[2100][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu as essayé de chercher sur %s?" % GlobalStreetNames[2100][-1],
              COMPLETE : "Ah, parfait!\aC'est ce que je craignais...\aOh, oui! Voilà ta pièce de déguisement.",
             },

    11002 : { GREETING : "",
              LEAVING : "",
              QUEST : "Pour obtenir d'autres pièces de déguisement de Loibot, tu devrais retourner voir _toNpcName_.\aJ'ai entendu dire qu'il avait besoin d'assistants de recherche._where_",
              },
    11003 : { GREETING : "",
              LEAVING : "",
              QUEST : "Plus de pièces de déguisement de Loibot?\aBon, si tu insistes...\amais j'ai besoin d'une autre sonde de température Cog.\aCette fois-ci, va sur %s." % GlobalStreetNames[2200][-1],
              INCOMPLETE_PROGRESS : "Tu cherches bien sur %s ?" % GlobalStreetNames[2200][-1],
              COMPLETE : "Merci!\aVoilà ta pièce de déguisement.",
             },
    11004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu as besoin de pièces de déguisement Loibot supplémentaires, tu devrais retourner voir _toNpcName_.\aApparemment, il a toujours besoin d'aide pour ses recherches météorologiques._where_",
              },
    11005 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu sais te montrer utile!\aEst-ce que tu peux aller jeter un oeil sur %s?" % GlobalStreetNames[2300][-1],
              INCOMPLETE_PROGRESS : " Tu es bien en train de chercher sur %s ?" % GlobalStreetNames[2300][-1],
              COMPLETE : "Hmmm, je n'aime pas trop ça...\amais voici ta pièce de déguisement...",
             },
    11006 : { GREETING : "",
              LEAVING : "",
              QUEST : " Qui-tu-sais a besoin de relevés de température supplémentaires.\aPasse le voir si tu veux une autre pièce de déguisement._where_",
              },
    11007 : { GREETING : "",
              LEAVING : "",
              QUEST : "Encore toi?\aTu as vraiment envie de travailler...\aLa prochaine destination, c'est %s." % GlobalStreetNames[1100][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu as essayé de chercher sur %s?" % GlobalStreetNames[1100][-1],
              COMPLETE : "Bon! On dirait que tu t'en sors plutôt bien!\aTa pièce de déguisement...",
             },
    11008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu as envie d'une autre pièce de déguisement de Loibot..._where_",
              },
    11009 : { GREETING : "",
              LEAVING : "",
              QUEST : "Content de te trouver ici!\aMaintenant, j'ai besoin de relevés sur %s." % GlobalStreetNames[1200][-1],
              INCOMPLETE_PROGRESS : "Tu cherches bien sur %s ?" % GlobalStreetNames[1200][-1],
              COMPLETE : "Merci beaucoup!\aTu n'es probablement pas loin d'avoir tout ton déguisement...",
             },
    11010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je crois que _toNpcName_ a encore du travail pour toi._where_",
              },
    11011 : { GREETING : "",
              LEAVING : "",
              QUEST : " Content de te revoir, _avName_!\aEst-ce que tu peux faire un relevé sur %s?" % GlobalStreetNames[1300][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu as essayé de chercher sur %s?" % GlobalStreetNames[1300][-1],
              COMPLETE : "Super boulot!\aVoici ta récompense. Tu l'as bien méritée!",
             },
    11012 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu sais ce qu'il faut faire._where_",
              },
    11013 : { GREETING : "",
              LEAVING : "",
              QUEST : "_avName_, mon ami!\aEst-ce que tu pourrais aller à %s et me trouver une autre sonde de température?" % GlobalStreetNames[5100][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu es vraiment en train de chercher sur %s?" % GlobalStreetNames[5100][-1],
              COMPLETE : "Excellent!\aGrâce à ton aide, mes recherches avancent très vite!\aVoici ta récompense.",
             },
    11014 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a parlé de toi.aOn dirait que tu as fait une sacrée impression!_where_",
              },
    11015 : { GREETING : "",
              LEAVING : "",
              QUEST : "Content de te revoir!\aJe t'attendais.\aLe prochain relevé dont j'ai besoin, c'est sur %s." % GlobalStreetNames[5200][-1],
              INCOMPLETE_PROGRESS : "Tu cherches bien sur %s ?" % GlobalStreetNames[5200][-1],
              COMPLETE : "Merci!\aVoici ta récompense.",
             },
    11016 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu as besoin de terminer ton déguisement de Loibot...\a_toNpcName_ peut t'aider._where_",
              },
    11017 : { GREETING : "",
              LEAVING : "",
              QUEST : "Salut, jeune chercheur!\aNous avons encore besoin de relevés de %s." % GlobalStreetNames[5300][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu as essayé de chercher sur %s?" % GlobalStreetNames[5300][-1],
              COMPLETE : "Excellent travail!\aVoilà ton machin de Loibot...",
             },
    11018 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a un autre travail pour toi.\aSi tu n'en as pas assez de le voir..._where_",
              },
    11019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Bon, très bien.\aTu te sens d'attaque pour aller chercher autre chose?\aCette fois-ci, essaie %s." % GlobalStreetNames[4100][-1],
              INCOMPLETE_PROGRESS : "Tu es bien en train de chercher sur %s ?" % GlobalStreetNames[4100][-1],
              COMPLETE : "Et un de plus!\aQuelle efficacité!",
             },
    11020 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu es toujours à la recherche de pièces de déguisement de Loibot?_where_",
              },
    11021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu as sans doute déjà deviné...\amais j'ai besoin de relevés de %s." % GlobalStreetNames[4200][-1],
              INCOMPLETE_PROGRESS : "Tu cherches bien sur %s ?" % GlobalStreetNames[4200][-1],
              COMPLETE : "On y est presque!\aEt voilà...",
             },
    11022 : { GREETING : "",
              LEAVING : "",
              QUEST : "J'ai presque honte de le dire, mais..._where_",
              },
    11023 : { GREETING : "",
              LEAVING : "",
              QUEST : "Qu'est-ce que tu penses de %s? Est-ce que tu crois que tu pourrais aller chercher une sonde là-bas aussi?" % GlobalStreetNames[4300][-1],
              INCOMPLETE_PROGRESS : "Est-ce que tu as essayé de chercher sur %s?" % GlobalStreetNames[4300][-1],
              COMPLETE : "Encore du bon travail, _avName_",
             },
    11024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Va voir le Professeur, si tu as encore besoin de pièces de déguisement._where_",
              },
    11025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je crois qu'on a encore besoin d'un relevé de %s." % GlobalStreetNames[9100][-1],
              INCOMPLETE_PROGRESS : "Tu es bien en train de chercher sur %s ?" % GlobalStreetNames[9100][-1],
              COMPLETE : "Bon travail!\aJe crois qu'on se rapproche...",
             },
    11026 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a une dernière mission pour toi._where_",
              },
    11027 : { GREETING : "",
              LEAVING : "",
              QUEST : "Déjà de retour?\aLe dernier relevé est sur %s." % GlobalStreetNames[9200][-1],
              INCOMPLETE_PROGRESS : "Tu cherches bien sur %s ?" % GlobalStreetNames[9200][-1],
              COMPLETE : "Ça y est enfin!\aMaintenant, tu vas pouvoir t'introduire dans le bureau du Procureur et ramasser des convocations du jury.\aBonne chance et merci pour ton aide!",
             },
    12000 : { GREETING : "",
              LEAVING : "",
              QUEST : "If you are interested in Bossbot disguise parts you should visit _toNpcName_._where_",
              },
    12001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Oui, je peux te trouver des pièces de Chefbot.\aMais tu devras m'aider à terminer ma collection de Chefbot.\aVa défier un Laquaistic.",
              INCOMPLETE_PROGRESS : "Tu n'as pas trouvé de Laquaistic ? Quel dommage&nbsp;!",
              COMPLETE : "Tu n'as pas été recalé j'espère ?\aVoici ta première pièce de déguisement.",
             },
    12002 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a encore besoin d'aide, si ça te dit._where_",
              },
    12003 : { GREETING : "",
              LEAVING : "",
              QUEST : "Une autre pièce de déguisement ?\aAbsolument...\amais seulement si tu parviens à vaincre un Gratte-papier.",
              INCOMPLETE_PROGRESS : "Les Gratte-papiers sont dans les rues.",
              COMPLETE : "Un vrai jeu d'enfant !\aVoici ta seconde pièce de déguisement.",
             },
    12004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Il y a vraiment un seul endroit où trouver des pièces de Chefbot._where_",
              },
    12005 : { GREETING : "",
              LEAVING : "",
              QUEST : "Maintenant j'ai besoin d'un Béniouioui...",
              INCOMPLETE_PROGRESS : "Les Béniouiouis sont dans les rues.",
              COMPLETE : "Super, l'ami, tu es bon.\aVoici ta troisième pièce de déguisement.",
             },
    12006 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a d'autres pièces pour toi...",
              },
    12007 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu triomphes d'un Microchef, je te donnerai une autre pièce de déguisement.",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[1100][-1],
              COMPLETE : "Tu t'es bien défendu !\aVoici ta quatrième pièce de déguisement.",
             },
    12008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Rends-toi dans..._where_",
              },
    12009 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je suis à la recherche d'un Touptisseur maintenant...",
              INCOMPLETE_PROGRESS : "Des problèmes ? Va voir dans %s" % GlobalStreetNames[3100][-1],
              COMPLETE : "Quelle terrible défaite !\aVoici ta cinquième pièce de déguisement.",
             },
    12010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je pense que tu sais où aller maintenant..._where_",
              },
    12011 : { GREETING : "",
              LEAVING : "",
              QUEST : "Prochain sur ma liste : un Chassetête.",
              INCOMPLETE_PROGRESS : "Tu auras peut-être plus de chance en allant faire un tour dans les bâtiments.",
              COMPLETE : "Je vois que tu n'as eu aucun mal à en trouver un.\aVoici ta sixième pièce de déguisement.",
             },
    12012 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ a besoin de plus de Chefbots.",
              },
    12013 : { GREETING : "",
              LEAVING : "",
              QUEST : "À présent, j'ai besoin que tu me déniches un Attactic.",
              INCOMPLETE_PROGRESS : "Tu auras peut-être plus de chance en allant faire un tour dans les bâtiments.",
              COMPLETE : "Tu fais un excellent chasseur !\aVoici ta septième pièce de déguisement.",
             },
    12014 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu souhaites obtenir plus de pièces de déguisement, va dans..._where_",
              },
    12015 : { GREETING : "",
              LEAVING : "",
              QUEST : "Et maintenant, le coup de grâce : le Gros Blochon !",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Je savais que je pouvais compter sur toi pour...\apeu importe !\aVoici une autre pièce de déguisement.",
             },
    12016 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ était à ta recherche...",
              },
    12017 : { GREETING : "",
              LEAVING : "",
              QUEST : "À présent, j'aimerais que tu t'attaques à l'un des nouveaux Cogs Chefbot, qui sont plus dangereux.",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Ils sont plus forts qu'ils en ont l'air, hein&nbsp;?\aEnfin, je te dois quand même une pièce de déguisement.",
             },
    12018 : { GREETING : "",
              LEAVING : "",
              QUEST : "Pourrais-tu aller faire un tour à..._where_",
              },
    12019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ces Cogs version 2.0 sont très intéressants.\aS'il te plaît, va en attaquer un autre.",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Merci !\aUne autre pièce de déguisement pour toi.",
             },
    12020 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tu peux, arrête-toi et va voir _toNpcName_.",
              },
    12021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je me demande s'ils peuvent se régénérer...",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "J'imagine que non.\aVoici ta pièce de déguisement...",
             },
    12022 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu sais..._where_",
              },
    12023 : { GREETING : "",
              LEAVING : "",
              QUEST : "Peut-être que ce ne sont pas des Chefbots du tout...",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Finalement, je crois bien que ce sont des Chefbots.\aChoisis une autre pièce de déguisement.",
             },
    12024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu sais sans doute déjà ce que je vais te dire...",
              },
    12025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Peut-être que d'une certaine manière, ils sont parents avec les Skelecogs...",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Ce fut peu concluant...\aVoici ta pièce de déguisement.",
             },
    12026 : { GREETING : "",
              LEAVING : "",
              QUEST : "S'il te plaît, retourne voir _toNpcName_.",
              },
    12027 : { GREETING : "",
              LEAVING : "",
              QUEST : "Je ne suis toujours pas convaincu qu'il ne s'agit pas d'une espèce de Skelecog...",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Peut-être pas.\aVoici une autre pièce de déguisement.",
             },
    12028 : { GREETING : "",
              LEAVING : "",
              QUEST : "C'est sans doute l'endroit où tu as le moins envie d'aller, mais...",
              },
    12029 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ces nouveaux Cogs me laissent vraiment perplexe.\aPourrais-tu aller en attaquer un autre, s'il te plaît&nbsp;?",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Vraiment fascinant.\aUne pièce de déguisement pour te remercier de tes efforts.",
             },
    12030 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_  commence à sonner comme un disque rayé ...",
              },
    12031 : { GREETING : "",
              LEAVING : "",
              QUEST : "J'ai presque trouvé ce que sont ces Cogs.\aJuste encore un...",
              INCOMPLETE_PROGRESS : "Va voir dans %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Oui, je crois que je suis sur la bonne voie.\aAh oui.\aÇa, c'est pour toi...",
             },
    12032 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tu dois aller raconter tout ça à Flippy...",
              INCOMPLETE_PROGRESS : "Flippy se trouve dans Toon Hall",
              COMPLETE : "Une nouvelle espèce de Cog !\aBon travail !\aVoici ta dernière pièce de déguisement.",
              },
 }

# ChatGarbler.py
ChatGarblerDog = ["ouaf", "ouarf", "rrrgh"]
ChatGarblerCat = ["miaou", "maaou"]
ChatGarblerMouse = ["couic", "couiiic", "iiiiic"]
ChatGarblerHorse = ["hihiii", "brrr"]
ChatGarblerRabbit = ["ouic", "pouip", "plouik", "bouip"]
ChatGarblerDuck = ["coin", "couac", "coiinc"]
ChatGarblerMonkey = ["oh", "hou", "ah"]
ChatGarblerBear = ["grrr", "grrr"]
ChatGarblerPig = ["rrrrr", "ouing", "ouing"]
ChatGarblerDefault = ["blabla"]

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Recherche de coordonnées pour %s."
AvatarDetailPanelFailedLookup = "Impossible d'obtenir les coordonnées de %s."
AvatarDetailPanelPlayer = "Joueur : %(player)s\nMonde : %(world)s"
AvatarDetailPanelPlayerShort = "%(player)s\nMonde : %(world)s\nLieu : %(location)s"
AvatarDetailPanelRealLife = "Hors ligne"
AvatarDetailPanelOffline = "District: hors-ligne\nLieu : hors-ligne"
AvatarDetailPanelOnline = "District : %(district)s\nLieu : %(location)s"
AvatarDetailPanelOnlinePlayer = "District : %(district)s\nLieu : %(location)s\nJoueur : %(player)s"
AvatarDetailPanelOffline = "District: hors-ligne\nLieu : hors-ligne"
AvatarShowPlayer = "Montrer joueur"
OfflineLocation = "Hors ligne"

#PlayerDetailPanel
PlayerToonName = "Toon : %(toonname)s"
PlayerShowToon = "Montrer Toon"
PlayerPanelDetail = "Informations joueur"


# AvatarPanel.py
AvatarPanelFriends = "Contacts"
AvatarPanelWhisper = "Chuchoter"
AvatarPanelSecrets = "Secrets"
AvatarPanelGoTo = "Aller à"
AvatarPanelPet = "Montrer le Doudou"
AvatarPanelIgnore = "Ignorer"
AvatarPanelIgnoreCant = "OK"
AvatarPanelStopIgnoring = "Arrête d'ignorer"
AvatarPanelReport = "Signaler"
#AvatarPanelCogDetail = "Dépt : %s\nNiveau: %s\n"
AvatarPanelCogLevel = "Niveau: %s"
AvatarPanelCogDetailClose = lClose
AvatarPanelDetail = "Détails du Toon"
AvatarPanelGroupInvite = "Inviter dans le groupe"
AvatarPanelGroupRetract = "Retirer invitation"
AvatarPanelGroupMember = "Déjà dans le groupe"
AvatarPanelGroupMemberKick = "Kick Out"

# grouping messages
groupInviteMessage = "%s aimerait que tu rejoignes son groupe"


# Report Panel
ReportPanelTitle = "Signaler un joueur"
ReportPanelBody = "Cette fonction permet d'envoyer un rapport complet à un modérateur. Au lieu d'envoyer un rapport, tu peux opter pour l'une des options suivantes&nbsp;:\n\n - Te téléporter dans un autre district\n - Utiliser \" Ignorer \" sur le panneau de commande du Toon\n\nSouhaites-tu vraiment signaler %s à un modérateur ?"
ReportPanelBodyFriends = "Cette fonction permet d'envoyer un rapport complet à un modérateur. Au lieu d'envoyer un rapport, tu peux opter pour l'une des options suivantes&nbsp;:\n\n - Te téléporter dans un autre district \n - Rompre votre amitié\n\n Souhaites-tu vraiment signaler %s à un modérateur ?\n\n(Cela rompra également votre amitié)"
ReportPanelCategoryBody = "Tu es sur le point de signaler %s. Un modérateur sera alerté de ta plainte et prendra les mesures appropriées envers toute personne ayant enfreint nos règles. Sélectionne la raison pour laquelle tu signales %s:"
ReportPanelBodyPlayer = "Cette fonction est en cours de développement et sera bientôt disponible. En attendant, tu peux :\n\n - Te rendre dans DXD pour rompre votre amitié.\n - Raconter ce qui s'est passé à un parent."

ReportPanelCategoryLanguage = "Propos grossiers"
ReportPanelCategoryPii = "Partage ou demande d'informations personnelles"
ReportPanelCategoryRude = "Impoli ou méchant"
ReportPanelCategoryName = "Mauvais nom"

ReportPanelConfirmations = (
    "Tu es sur le point de signaler que %s a utilisé des propos obscènes, sectaires ou sexuellement explicites.",
    "Tu es sur le point de signaler que %s n'est pas prudent, et donne ou demande un numéro de téléphone, une adresse, un nom de famille, une adresse e-mail, un mot de passe ou un nom de compte.",
    "Tu es sur le point de signaler que %s tyrannise, harcèle ou manifeste un comportement extrême pour perturber le jeu.",
    "Tu es sur le point de signaler que %s a créé un nom qui n'est pas conforme aux Règles du jeu de Disney.",
    )

# Put on confirmation screen!
ReportPanelWarning = "Nous prenons les rapports très au sérieux. Ton rapport sera examiné par un modérateur, qui prendra les mesures appropriées envers toute personne ayant enfreint nos règles. S'il s'avère que ton compte a lui-même enfreint les règles, ou si tu fais de faux signalements ou utilises la fonction «&nbsp;Signaler un joueur&nbsp;» de manière abusive, un modérateur pourrait prendre des mesures contre ton compte. Es-tu sûr de vouloir signaler ce joueur&nbsp;?"

ReportPanelThanks = "Merci. Ton rapport a été envoyé à un modérateur qui se chargera de son examen. Tu n'as pas besoin de nous contacter à nouveau concernant cet incident. L'équipe chargée de la modération prendra les mesures qui s'imposent à l'encontre de tout joueur ayant enfreint nos règles."

ReportPanelRemovedFriend = "Nous avons automatiquement supprimé %s de ta Liste d'amis."

ReportPanelAlreadyReported = "Tu as déjà signalé %s durant cette session. Un modérateur se chargera d'examiner ton précédent rapport."

# Report Panel
IgnorePanelTitle = "Ignorer un joueur"
IgnorePanelAddIgnore = "Veux-tu ignorer %s pour le reste de cette session ?"
IgnorePanelIgnore = "À présent, tu ignores %s."
IgnorePanelRemoveIgnore = "Veux-tu arrêter d'ignorer %s ?"
IgnorePanelEndIgnore = "Tu n'ignores plus %s."
IgnorePanelAddFriendAvatar = "%s est ton ami(e). Tu ne peux pas l'ignorer tant que vous êtes amis. %s (%s) est ton ami(e). Tu ne peux pas l'ignorer tant que vous êtes amis."
IgnorePanelAddFriendPlayer = ""

# PetAvatarPanel.py
PetPanelFeed = "Nourrir"
PetPanelCall = "Appeler"
PetPanelGoTo = "Aller à"
PetPanelOwner = "Montrer le propriétaire"
PetPanelDetail = "Détails de l'animalerie"
PetPanelScratch = "Cajoler"

# PetDetailPanel.py
PetDetailPanelTitle = "Apprentissage des tours"
# NOTE: these are replicated from OTPLocalizerEnglish sans "!"
PetTrickStrings = {
    0: 'Saute',
    1: 'Fais le beau',
    2: 'Fais le mort',
    3: 'Fais une roulade',
    4: 'Saute en arrière',
    5: 'Danse',
    6: 'Parle',
    }

# PetMood.py
PetMoodAdjectives = {
    'neutral': 'neutre',
    'hunger': 'affamé',
    'boredom': "s'ennuie",
    'excitement': 'excité',
    'sadness': 'triste',
    'restlessness': 'agité',
    'playfulness': 'joueur',
    'loneliness': 'solitaire',
    'fatigue': 'fatigué',
    'confusion': 'perplexe',
    'anger': 'en colère',
    'surprise': 'surpris',
    'affection': 'affectueux',
    }

# DistributedAvatar.py
DialogQuestion = '?'

# LocalAvatar.py
FriendsListLabel = "Contacts"

# TeleportPanel.py
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = "Essaie d'aller à %s."
TeleportPanelNotAvailable = "%s est occupé(e) en ce moment, ressaie plus tard."
TeleportPanelIgnored = "%s t'ignore"
TeleportPanelNotOnline = "%s n'est pas en ligne en ce moment."
TeleportPanelWentAway = "%s est parti(e)."
TeleportPanelUnknownHood = "Tu ne sais pas aller jusqu'à %s!"
TeleportPanelUnavailableHood = "%s est occupé(e) en ce moment, ressaie plus tard."
TeleportPanelDenySelf = "Tu ne peux pas aller te voir toi-même!"
TeleportPanelOtherShard = "%(avName)s est dans le district %(shardName)s, et tu es dans le district %(myShardName)s. Veux-tu aller à %(shardName)s?"
TeleportPanelBusyShard = "%(avName)s se trouve dans un district qui affiche complet. Jouer dans un district complet peut considérablement ralentir les performances de jeu. Es-tu sûr de vouloir changer de district ?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Je suis le chef."

# DistributedBattleFactory.py
FactoryBossTaunt = "Je suis le contremaître."
FactoryBossBattleTaunt = "Je te présente le contremaître."
MintBossTaunt = "Je suis le Superviseur."
MintBossBattleTaunt = "Vous devez parler au Superviseur."
StageBossTaunt = "Ma justice n'est pas aveugle"
StageBossBattleTaunt = "Je suis au-dessus des lois"
CountryClubBossTaunt = "Je suis le Président du Club."
CountryClubBossBattleTaunt = "Tu dois t'adresser au Président du Club."
ForcedLeaveCountryClubAckMsg = "Le Président du Club a été vaincu avant que tu n'arrives jusqu'à lui. Tu n'as pas récupéré d'actions."

# HealJokes.py
ToonHealJokes = [
    ["Qu'est ce qui fait PIOU-PIOU?",
     "Un poussin de 500 kilos!"],
    ["Que dit un pneu qui va voir un médecin ?",
     "Docteur, je me sens crevé."],
    ["Pourquoi est-ce difficile pour un fantôme de mentir ?",
     "Parce qu'il est cousu de fil blanc."],
    ["Vous connaissez l'histoire de la chaise ?",
     "Dommage, elle est pliante!"],
    ["Qu'est-ce qui est vert et qui monte et qui descend?",
     "Un petit pois dans un ascenseur!"],
    ["Quel est le comble de l'électricien ?",
     "De ne pas être au courant."],
    ["Que font deux chiens qui se rencontrent à Tokyo?",
     "Ils se jappent au nez."],
    ["Quel est le futur de \"je baille\"?",
     "Je dors."],
    ["Quel est l'animal le plus rapide ?",
     "Le pou car il est toujours en tête!"],
    ["Quel animal n'a jamais soif?",
     "Le zébu, parce que quand zébu zé plus soif!"],
    ["Quel est le comble pour un myope ?",
     "De manger des lentilles."],
    ["Pourquoi as-tu mis le journal dans le réfrigérateur ?",
     "Pour avoir des nouvelles fraîches!"],
    ["Qu'est-ce qui est gris et qui t'éclabousse de confiture ?",
     "Une souris qui mange un beignet."],
    ["Que demande un douanier à un cochon qui passe la frontière ?",
     "Son passe-porc."],
    ["Que dit un bébé souris à sa maman quand il voit passer une chauve-souris?",
     "Maman, un ange!"],
    ["Comment appelle-t-on un ascenseur au Japon ?",
     "En appuyant sur le bouton."],
    ["Comment appelle-t-on un poisson pas encore né?",
     "Un poisson pané."],
    ["Si tu fais tomber un chapeau blanc dans la mer rouge, comment ressort-il?",
     "Mouillé."],
    ["Que demande un chat qui entre dans une pharmacie ?",
     "Du sirop pour matou."],
    ["Quel est le comble pour un jockey?",
     "D'être à cheval sur les principes."],
    ["Quelles sont les deux choses que tu ne peux pas prendre au petit-déjeuner ?",
     "Le déjeuner et le dîner."],
    ["Qu'est ce qu'on donne à un éléphant qui a de grands pieds?",
     "De grandes chaussures."],
    ["Comment sait-on qu'un éléphant est caché dans le réfrigérateur ?",
     "Aux empreintes de pattes dans le beurre."],
    ["Quelle est la différence entre un instituteur et un thermomètre ?",
     "Aucune, on tremble toujours quand ils marquent zéro!"],
    ["Qu'est-ce qui est petit, carré et vert ?",
     "Un petit carré vert."],
    ["Quel est le comble pour un éléphant ?",
     "D'être sans défense."],
    ["Que dit le 0 au 8?",
     "Tiens, tu as mis ta ceinture!"],
    ["Qu'est ce qu'il ne faut jamais faire devant un poisson-scie ?",
     "La planche!"],
    ["Pourquoi est-ce que certaines personnes travaillent la nuit ?",
     "Pour mettre leur travail à jour."],
    ["Quel est le comble de la patience ?",
     "Trier des petits pois avec des gants de boxe."],
    ["Qu'est ce qui voyage tout autour du monde en restant dans son coin ?",
     "Un timbre."],
    ["Quel est le comble pour une souris?",
     "Avoir un chat dans la gorge."],
    ["Quel est le comble pour un canard?",
     "En avoir marre!"],
    ["Quel est le comble pour un magicien ?",
     "Se nourrir d'illusions."],
    ["Quel est le comble de la clé?",
     "Se faire mettre à la porte."],
    ["Quel est le comble pour un cordonnier ?",
     "Avoir les dents qui se déchaussent."],
    ["De quelle couleur sont les petits pois?",
     "Les petits poissons rouges."],
    ["Qu'est-ce qui baille et qui ne dort jamais?",
     "Une porte."],
    ["Tu sais ce que c'est un canif?",
     "C'est un p'tit fien!"],
    ["Qu'est-ce qu'un chou au fond d'une baignoire ?",
     "Un choumarin!"],
    ["Quel est le comble pour le propriétaire d'un champ de pommiers?",
     "Travailler pour des prunes!"],
    ["Qu'est-ce qui est aussi grand que l'Arc de Triomphe mais ne pèse rien ?",
     "Son ombre."],
    ["Comment s'appelle un boomerang qui ne revient pas?",
     "Un bout de bois."],
    ["Pourquoi est-ce que les éléphants se déplacent en troupeau compact ?",
     "Parce que c'est celui du milieu qui a la radio."],
    ["De quelle couleur sont les parapluies quand il pleut ?",
     "Ils sont tout verts."],
    ["Quel est le comble du torero?",
     "Que le taureau soit vache."],
    ["Quel est l'animal le plus heureux?",
     "Le hibou, parce que sa femme est chouette."],
    ["Que dit un vitrier à son fils?",
     "Tiens-toi à carreau si tu veux une glace."],
    ["Comment appelle-t-on un chien sans pattes?",
     "On ne l'appelle pas, on va le chercher."],
    ["Qu'ont les girafes que n'ont pas les autres animaux?",
     "Des bébés girafes."],
    ["Un chameau peut-il avoir 3 bosses?",
     "Oui, s'il se cogne la tête contre le mur."],
    ["Pourquoi les musiciens aiment-ils prendre le train ?",
     "Parce que la voie fait ré."],
    ["Deux fourmis sont sur un âne, laquelle va doubler l'autre ?",
     "Aucune, il est interdit de doubler sur un dos d'âne."],
    ["Quelle est la note la plus basse ?",
     "Le sol."],
    ["Pourquoi les trains électriques vont-ils plus vite que les trains à vapeur ?",
     "Parce qu'ils ont arrêté de fumer."],
    ["Qu'est ce qu'un arbuste dit à un géranium?",
     "Espèce d'empoté!"],
    ["Que recommande la maman allumette à ses enfants?",
     "Surtout, ne vous grattez pas la tête!"],
    ["Qu'est-ce qu'il y a à la fin de tout ?",
     "La lettre T."],
    ["Pourquoi les poissons-chats s'ennuient-ils?",
     "Parce qu'il n'y a pas de poissons-souris."],
    ["Qu'est-ce que le vainqueur du marathon a perdu?",
     "Son souffle."],
    ["Comment appelle-t-on un spectacle qui rend propre ?",
     "Un ballet."],
    ["Qu'est-ce qui fait 999 fois \"Tic\" et une fois \"Toc\"?",
     "Un mille-pattes avec une jambe de bois."],
    ["Comment reconnaît-on un écureuil d'une fourchette ?",
     "En les mettant au pied d'un arbre, celui qui monte est l'écureuil."],
    ["Pourquoi les flamants roses lèvent-ils une patte en dormant ?",
     "Parce qu'ils tomberaient s'ils levaient les deux."],
    ["Qu'est-ce qui est noir quand il est propre et blanc quand il est sale ?",
     "Un tableau noir!"],
    ["Qu'est-ce qui fait Oh, Oh, Oh?",
     "Le Père Noël qui marche en arrière."],
    ["Qu'est-ce qui peut voyager jour et nuit sans quitter son lit ?",
     "La rivière."],
    ["Quel arbre n'aime pas la vitesse ?",
     "Le frêne."],
    ["Pourquoi est-ce que les dinosaures ont de longs cous?",
     "Parce que leurs pieds sentent mauvais."],
    ["Qu'est-ce qui est jaune et qui court très vite ?",
     "Un citron pressé."],
    ["Pourquoi est-ce que les éléphants n'oublient jamais?",
     "Parce qu'on ne leur dit jamais rien."],
    ["Quel animal peut changer de tête facilement ?",
     "Un pou."],
    ["Qu'est-ce qu'un steak caché derrière un arbre ?",
     "Un steak caché."],
    ["Pourquoi est-ce que les serpents ne sont pas susceptibles?",
     "Parce qu'on ne peut pas leur casser les pieds."],
    ["Pourquoi dit-on que les boulangers travaillent rapidement ?",
     "Parce qu'ils travaillent en un éclair."],
    ["Que dit un fantôme quand il est ennuyé?",
     "Je suis dans de beaux draps!"],
    ["Comment peut-on arrêter un éléphant qui veut passer dans le chas d'une aiguille ?",
     "On fait un nœud à sa queue."],
    ["Pourquoi est-ce que les pompiers ont des bretelles rouges?",
     "Pour tenir leurs pantalons!"],
    ["Que prend un éléphant lorsqu'il rentre dans un bar ?",
     "De la place!"],
    ["Savez-vous que votre chien aboie toute la nuit ?",
     "Ça ne fait rien, il dort toute la journée!"],
    ["Savez-vous que le vétérinaire a épousé la manucure ?",
     "Au bout d'un mois ils se battaient becs et ongles."],
    ["Tu sais que nous sommes sur terre pour travailler ?",
     "Bon, alors plus tard je serai marin."],
    ["Quand je dis \"il pleuvait\", de quel temps s'agit-il?",
     "D'un sale temps."],
    ["À quoi reconnaît-on un motard heureux?",
     "Aux moustiques collés sur ses dents."],
    ["Son succès lui est monté à la tête.",
     "C'est normal, c'est là qu'il y avait le plus de place libre."],
    ["Qu'est-ce qui est gris, pousse de petits cris et fait 5 kilos?",
     "Une souris qui a besoin de se mettre au régime."],
    ["Que dit-on à un croque-mort qui rentre dans un café?",
     "\"Je vous sers une bière ?\""],
    ["Connais-tu l'histoire du lit vertical?",
     "C'est une histoire à dormir debout."],
    ["Pourquoi est-ce que les éléphants sont gros et gris?",
     "Parce que s'ils étaient petits et jaunes ce seraient des canaris."],
    ["Combien coûte cet aspirateur ?",
     "750 et des poussières."],
    ["Quel est le comble pour un juge gourmand?",
     "De manger des avocats."],
    ["Pourquoi"+ Donald + " regarde-t-il à droite et à gauche lorsqu'il rentre dans une pièce ?",
     "Parce qu'il ne peut pas regarder des deux côtés à la fois."],
    ["Pourquoi est-ce que"+ Goofy + " emmène son peigne chez le dentiste ?",
     "Parce qu'il a perdu toutes ses dents."],
    ["Quel bruit fait la fourmi?",
     "La fourmi cro-onde."],
    ["Si les sorties étaient surveillées, comment le voleur a-t-il pu s'échapper ?",
     "Par l'entrée!"],
    ["Que dit un haut-parleur à un autre haut-parleur ?",
     "Tu veux une baffle ?"],
    ["Pourquoi les lézards aiment-ils les vieux murs?",
     "Parce qu'ils ont des lézardes."],
    ["Pourquoi est-ce que les moutons ont des pelages en laine ?",
     "Parce qu'ils auraient l'air idiots avec des pelages en synthétique."],
    ["Où trouve-t-on le dimanche avant le jeudi?",
     "Dans le dictionnaire."],
    ["Pourquoi est-ce que"+ Pluto + " a dormi avec une peau de banane ?",
     "Pour pouvoir se glisser hors de son lit le lendemain matin."],
    ["Pourquoi est-ce que la souris portait des chaussons noirs?",
     "Parce que les blancs étaient à la lessive."],
    ["Quel est le point commun entre les fausses dents et les étoiles?",
     "Elles sortent la nuit."],
    ["Pourquoi est-ce que les chats aiment se faire photographier ?",
     "Parce qu'on leur dit \"souris!\"."],
    ["Pourquoi est-ce que l'archéologue a fait faillite ?",
     "Parce que sa carrière était en ruine."],
    ["Qui boit l'eau sans jamais l'avaler ?",
     "L'éponge."],
    ["Quelle est la couleur du virus de la grippe ?",
     "Gris pâle."],
    ["Pourquoi faut-il craindre le soleil?",
     "Parce que c'est le plus grand des astres."],
    ["Quel est le comble d'un avion ?",
     "C'est d'avoir un antivol."],
    ["Que dit la nappe à la table ?",
     "Ne crains rien, je te couvre."],
    ["Que fait"+ Goofy + " quand il tombe dans l'eau?",
     "PLOUF!"],
    ["Quel est le comble pour un crayon ?",
     "Se tailler pour avoir bonne mine."],
    ["Que dit la grosse cheminée à la petite cheminée ?",
     "Tu es trop jeune pour fumer."],
    ["Que dit le tapis au carrelage ?",
     "Ne t'inquiète pas, je te couvre."],
    ["Quelle est la différence entre le cancre et le premier de la classe ?",
     "Quand le cancre redouble, c'est rarement d'attention."],
    ["Qu'est-ce qui fait zzzb zzzb?",
     "Une guêpe qui vole à l'envers."],
    ["Comment appelle-t-on quelqu'un qui tue son beau-frère ?",
     "Un insecticide, car il tue l'époux de sa sœur."],
    ["Comment appelle-t-on un dinosaure qui n'est jamais en retard?",
     "Un promptosaure."],
    ["On ne devrait pas dire \"un chapitre\".",
     "On devrait dire \"un chat rigolo\"."],
    ["On ne devrait pas dire \"un perroquet\".",
     "On devrait dire \"mon papa est d'accord\"."],
    ["On ne devrait pas dire \"bosser à la chaîne\".",
     "On devrait dire \"travailler à la télé\"."],
    ["Pourquoi est-ce que le livre de maths était malheureux?",
     "Parce qu'il avait trop de problèmes."],
    ["On ne devrait pas dire \"un match interminable\".",
     "On devrait dire \"une rencontre de mauvais joueurs\"."],
    ["On ne devrait pas dire \"la maîtresse d'école\".",
     "On devrait dire \"l'institutrice prend l'avion\"."],
    ["Que voit-on quand deux mille-pattes se serrent la main ?",
     "Une fermeture-éclair."],
    ["Comment appelle-t-on un journal publié au Sahara?",
     "Un hebdromadaire."],
    ["Que doit planter un agriculteur frileux?",
     "Un champ d'ail."],
    ["Quel est le comble du chauve ?",
     "Avoir un cheveu sur la langue."],
    ["Qu'est-ce que tu trouves si tu croises un éléphant avec un corbeau?",
     "Des tas de poteaux téléphoniques cassés."],
    ["Combien gagne un fakir ?",
     "Des clous!"],
    ["Quelle est la meilleure manière d'économiser l'eau?",
     "La diluer."],
    ["Quelle différence y a-t-il entre un horloger et une girouette ?",
     "L'horloger vend des montres et la girouette montre le vent."],
    ["Pourquoi est-ce que les ordinateurs se grattent ?",
     "Parce qu'ils sont pleins de puces."],
    ["Qu'est-ce qui a un chapeau et pas de tête, un pied mais pas de souliers?",
     "Un champignon."],
    ["Pourquoi est-ce que le ciel est haut ?",
     "Pour éviter que les oiseaux ne se cognent la tête en volant."],
    ["Qu'est ce qui est pire qu'une girafe qui a mal à la gorge ?",
     "Un mille-pattes avec des cors aux pieds."],
    ["Qu'est-ce qui fait ABC...gloups...DEF...gloups?",
     "Quelqu'un qui mange de la soupe aux pâtes alphabet."],
    ["Qu'est-ce qui est blanc et qui va vite ?",
     "Un frigo de course."],
    ["Quel est le fruit que les poissons n'aiment pas?",
     "La pêche!"],
    ["Comment font les éléphants pour traverser un étang?",
     "Ils sautent de nénuphar en nénuphar."],
    ["Qu'est-ce qui est noir et blanc à pois rouges?",
     "Un Dalmatien qui a la rougeole."],
    ["Qu'est-ce qu'un chalumeau?",
     "Un drolumadaire à 2 bosses."],
    ["Pourquoi les éléphants sont-ils gris?",
     "Pour ne pas les confondre avec les fraises."],
    ["Qu'est-ce qui est gris, fait 100 kilos et appelle \"Minou, Minou!\"?",
     "Une souris de 100 kilos."],
    ["Quel est le point commun entre un pâtissier et un ciel orageux?",
     "Tous les deux font des éclairs."],
    ["Quel bruit font les esquimaux lorsqu'ils boivent ?",
     "Iglou, iglou, iglou"],
    ["Comment appelle-t-on une chauve-souris avec une perruque ?",
     "Une souris."],
    ["Pourquoi les aiguilles sont-elles moins intelligentes que les épingles?",
     "Parce qu'elles n'ont pas de tête."],
    ["Qu'est-ce qui a de la fourrure, miaule et chasse les souris sous l'eau?",
     "Un poisson-chat."],
    ["Comment fait-on aboyer un chat ?",
     "Si on lui donne une tasse de lait il la boit."],
    ["Qu'est-ce qui est vert à l'extérieur et jaune à l'intérieur ?",
     "Une banane déguisée en concombre."],
    ["Qu'est-ce qu'un ingrat ?",
     "Le contraire d'un géant maigre."],
    ["Qu'est-ce qui pèse 4 tonnes, a une trompe et est rouge vif?",
     "Un éléphant qui a honte."],
    ["Dans un virage à 60 degrés à droite, quelle est la roue qui tourne le moins vite ?",
     "La roue de secours."],
    ["Comment reconnaît-on un idiot dans un magasin de chaussures?",
     "C'est celui qui essaie les boîtes."],
    ["Que dit-on d'un enfant qui ramène le pain à la maison ?",
     "C'est le petit calepin."],
    ["Que dit la cacahuète à l'éléphant ?",
     "Rien, les cacahuètes ne parlent pas."],
    ["Que dit un éléphant lorsqu'il se heurte à un autre éléphant ?",
     "Le monde est petit, n'est-ce pas?"],
    ["Que dit la comptable à la machine à calculer ?",
     "Je compte sur toi."],
    ["Que dit la puce à une autre puce ?",
     "On y va à pied ou on prend le chat ?"],
    ["Que dit la grande aiguille à la petite aiguille ?",
     "Attends une minute."],
    ["Que dit une poule quand elle rencontre une autre poule ?",
     "Tu viens, on va prendre un ver ?"],
    ["Que dit le collant à la chaussure ?",
     "À plus tard, je dois filer."],
    ["Papa kangourou demande à sa fille qui rentre de l'école: \"Alors, cet examen ?\"",
     "\"C'est dans la poche, pas de problème!\""],
    ["Quelle est la ville de France la plus féroce ?",
     "Lyon."],
    ["Quelle est la ville de France la moins légère ?",
     "Lourdes."],
    ["Pourquoi porte-t-on des vêtements?",
     "Parce qu'ils ne peuvent pas marcher tout seuls."],
    ["Que dit une pomme de terre quand elle en voit une autre se faire écraser dans la rue ?",
     "\"Oh, purée!\""],
    ["Que dit un petit fakir quand il arrive en retard à l'école ?",
     "\"Pardon maîtresse, je me suis endormi sur le passage clouté!\""],
    ["Que dit un marin-pêcheur s'il se dispute avec un autre marin-pêcheur ?",
     "Je ne veux pas que tu me parles sur ce thon!"],
    ["Pourquoi les cultivateurs disent-ils des gros mots à leurs tomates?",
     "Pour les faire rougir."],
    ["Que disent deux vers de terre s'ils se rencontrent au milieu d'une pomme ?",
     "\"Vous habitez dans le quartier ?\""],
    ["Qu'est-ce que se disent deux serpents qui se rencontrent ?",
     "\"Quelle heure reptile ?\""],
    ["Pourquoi les mille-pattes ne peuvent-ils pas jouer au hockey?",
     "Le temps d'enfiler leurs patins, la partie est déjà terminée!"],
    ["Comment fait-on cuire un poisson dans un piano?",
     "On fait Do, Ré, La, Sol."],
    ["Connaissez-vous l'histoire du chauffeur d'autobus?",
     "Moi non plus, j'étais à l'arrière!"],
    ["Crois-tu aux girafes?",
     "Non, c'est un cou monté."],
    ["Que dit un crocodile s'il rencontre un chien ?",
     "Salut, sac à puces!"],
    ["Que dit un chien quand il rencontre un crocodile ?",
     "Salut, sac à main!"],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("hmm","hou","ha","rhaa")
MovieHealLaughterHits1= ("Ha ha ha","Hi hi","Hé hé","Ha ha")
MovieHealLaughterHits2= ("OUARF OUARF OUARF!","HO HO HO!","HA HA HA!")

# MovieSOS.py
MovieSOSCallHelp = "%s À L'AIDE!"
MovieSOSWhisperHelp = "%s a besoin d'aide pour un combat!"
MovieSOSObserverHelp = "À L'AIDE!"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "Salut, %s! C'est un plaisir de pouvoir t'aider!"
MovieNPCSOSGoodbye = "À plus tard!"
MovieNPCSOSToonsHit = "Les Toons font toujours mouche!"
MovieNPCSOSCogsMiss = "Les Cogs ratent toujours leurs cibles!"
MovieNPCSOSRestockGags = "En train de faire le plein de gags %s!"
MovieNPCSOSHeal = "Guérison"
MovieNPCSOSTrap = "Piégeage"
MovieNPCSOSLure = "Leurre"
MovieNPCSOSSound = "Tapage"
MovieNPCSOSThrow = "Lancer"
MovieNPCSOSSquirt = "Éclaboussure"
MovieNPCSOSDrop = "Chute"
MovieNPCSOSAll = "Tout"

# MoviePetSOS.py
MoviePetSOSTrickFail = "Soupir"
MoviePetSOSTrickSucceedBoy = "Bon garçon!"
MoviePetSOSTrickSucceedGirl = "Brave fifille!"

# MovieSuitAttacks.py
MovieSuitCancelled = "ANNULÉ\nANNULÉ\nANNULÉ"

# RewardPanel.py
RewardPanelToonTasks = "Défitoons"
RewardPanelItems = "Objets récupérés"
RewardPanelMissedItems = "Objets non récupérés"
RewardPanelQuestLabel = "Quête %s"
RewardPanelCongratsStrings = ["Ouais!", "Bravo!", "Ouah!",
                              "Sympa!", "Atmosphérique!", "Toontastique!"]
RewardPanelNewGag = "Nouveau gag %(gagName)s pour %(avName)s!"
RewardPanelUberGag = "%(avName)s earned the %(gagName)s gag with %(exp)s experience points!"
RewardPanelEndTrack = "Haa! %(avName)s a atteint la fin de la série de gags %(gagName)s!"
RewardPanelMeritsMaxed = "Au maximum"
RewardPanelMeritBarLabels = [ "Avis de licenciement", "Citations à comparaître", "Euros Cog", "Mérites" ]
RewardPanelMeritAlert = "Prêt pour la promotion!"

RewardPanelCogPart = "Tu as gagné un morceau de déguisement de Cog!"
RewardPanelPromotion = "Préparez pour la promotion %s voie!"

# Cheesy effect descriptions: (short desc, sentence desc)
CheesyEffectDescriptions = [
    ("Toon normal", "tu seras normal(e)"),
    ("Grosse tête", "tu auras une grosse tête"),
    ("Petite tête", "tu auras une petite tête"),
    ("Grosses jambes", "tu auras de grosses jambes"),
    ("Petites jambes", "tu auras de petites jambes"),
    ("Gros Toon", "tu seras un peu plus gros(se)"),
    ("Petit Toon", "tu seras un peu plus petit(e)"),
    ("À plat", "tu seras en deux dimensions"),
    ("Profil plat", "tu seras en deux dimensions"),
    ("Transparent", "tu seras transparent(e)"),
    ("Sans couleur", "tu seras incolore"),
    ("Toon invisible", "tu seras invisible"),
    ]
CheesyEffectIndefinite = "Jusqu'à ce que tu choisisses un autre effet, %(effectName)s%(whileIn)s."
CheesyEffectMinutes = "Pendant les %(time)s prochaines minutes, %(effectName)s%(whileIn)s."
CheesyEffectHours = "Pendant les %(time)s prochaines heures, %(effectName)s%(whileIn)s."
CheesyEffectDays = "Pendant les %(time)s prochains jours, %(effectName)s%(whileIn)s."
CheesyEffectWhileYouAreIn = " pendant que tu es dans %s"
CheesyEffectExceptIn = ", excepté dans %s"


# SuitBattleGlobals.py
SuitFlunky = "Laquaistic"
SuitPencilPusher = "Gratte-\npapier"
SuitYesman = "Béniouioui"
SuitMicromanager = "Micro\3chef"
SuitDownsizer = "Touptisseur"
SuitHeadHunter = "Chassetête"
SuitCorporateRaider = "Attactic"
SuitTheBigCheese = "Gros Blochon"
SuitColdCaller = "Cassepied"
SuitTelemarketer = "Télé\3vendeur"
SuitNameDropper = "Cafteur"
SuitGladHander = "Passetout"
SuitMoverShaker = "Secousse-\ncousse"
SuitTwoFace = "Biface"
SuitTheMingler = "Le Circulateur"
SuitMrHollywood = "M. Hollywood"
SuitShortChange = "Gardoseille"
SuitPennyPincher = "Radino"
SuitTightwad = "Grippesou"
SuitBeanCounter = "Pince Menu"
SuitNumberCruncher = "Gobechiffre"
SuitMoneyBags = "Sacasous"
SuitLoanShark = "Usurier"
SuitRobberBaron = "Pillard"
SuitBottomFeeder = "Volebas"
SuitBloodsucker = "Pique-\nau-sang"
SuitDoubleTalker = "Charabieur"
SuitAmbulanceChaser = "Charognard"
SuitBackStabber = "Frappedos"
SuitSpinDoctor = "Tournegris"
SuitLegalEagle = "Avocageot"
SuitBigWig = "Chouffleur"

# Singular versions (indefinite article)
SuitFlunkyS = "un Laquaistic"
SuitPencilPusherS = "un Gratte-Papier"
SuitYesmanS = "un Béniouioui"
SuitMicromanagerS = "un Microchef"
SuitDownsizerS = "un Touptisseur"
SuitHeadHunterS = "un Chassetête"
SuitCorporateRaiderS = "un Attactic"
SuitTheBigCheeseS = "un Gros Blochon"
SuitColdCallerS = "un Cassepied"
SuitTelemarketerS = "un Télévendeur"
SuitNameDropperS = "un Cafteur"
SuitGladHanderS = "un Passetout"
SuitMoverShakerS = "un Secousse-cousse"
SuitTwoFaceS = "un Biface"
SuitTheMinglerS = "un Circulateur"
SuitMrHollywoodS = "un M. Hollywood"
SuitShortChangeS = "un Gardoseille"
SuitPennyPincherS = "un Radino"
SuitTightwadS = "un Grippesou"
SuitBeanCounterS = "un Pince-Menu"
SuitNumberCruncherS = "un Gobechiffre"
SuitMoneyBagsS = "un Sacasous"
SuitLoanSharkS = "un Usurier"
SuitRobberBaronS = "un Pillard"
SuitBottomFeederS = "un Volebas"
SuitBloodsuckerS = "un Pique-au-sang"
SuitDoubleTalkerS = "un Charabieur"
SuitAmbulanceChaserS = "un Charognard"
SuitBackStabberS = "un Frappedos"
SuitSpinDoctorS = "un Tournegris"
SuitLegalEagleS = "un Avocageot"
SuitBigWigS = "un Chouffleur"

# Plural versions
SuitFlunkyP = "Laquaistics"
SuitPencilPusherP = "Gratte-Papiers"
SuitYesmanP = "Béniouiouis"
SuitMicromanagerP = "Microchefs"
SuitDownsizerP = "Touptisseurs"
SuitHeadHunterP = "Chassetêtes"
SuitCorporateRaiderP = "Attactics"
SuitTheBigCheeseP = "Gros Blochons"
SuitColdCallerP = "Cassepieds"
SuitTelemarketerP = "Télévendeurs"
SuitNameDropperP = "Cafteurs"
SuitGladHanderP = "Passetouts"
SuitMoverShakerP = "Secousse-cousses"
SuitTwoFaceP = "Bifaces"
SuitTheMinglerP = "Les Circulateurs"
SuitMrHollywoodP = "MM. Hollywood"
SuitShortChangeP = "Gardoseilles"
SuitPennyPincherP = "Radinos"
SuitTightwadP = "Grippesous"
SuitBeanCounterP = "Pince-Menus"
SuitNumberCruncherP = "Gobechiffres"
SuitMoneyBagsP = "Sacasous"
SuitLoanSharkP = "Usuriers"
SuitRobberBaronP = "Pillards"
SuitBottomFeederP = "Volebas"
SuitBloodsuckerP = "Pique-au-sang"
SuitDoubleTalkerP = "Charabieurs"
SuitAmbulanceChaserP = "Charognards"
SuitBackStabberP = "Frappedos"
SuitSpinDoctorP = "Tournegris"
SuitLegalEagleP = "Avocageots"
SuitBigWigP = "Chouffleurs"

SuitFaceOffDefaultTaunts = ['Bouh!']

SuitAttackDefaultTaunts = ['Prends ça!', 'Garde des notes là-dessus!']

SuitAttackNames = {
  'Audit' : 'Audit!',
  'Bite' : 'Morsure!',
  'BounceCheck' : 'Chèque refusé!',
  'BrainStorm' : 'Remue-méninges!',
  'BuzzWord' : 'Mot à la mode!',
  'Calculate' : 'Évaluation!',
  'Canned' : 'En conserve!',
  'Chomp' : 'Mastication!',
  'CigarSmoke' : 'Fumée de cigare!',
  'ClipOnTie' : 'Cravate toute faite!',
  'Crunch' : 'Écrasement!',
  'Demotion' : 'Rétrogradation!',
  'Downsize' : 'Rapetissement!',
  'DoubleTalk' : 'Charabia!',
  'EvictionNotice' : "Ordre d'expulsion!",
  'EvilEye' : 'Mauvais œil!',
  'Filibuster' : 'Obstruction!',
  'FillWithLead' : 'Plombage!',
  'FiveOClockShadow' : "Barbe naissante!",
  'FingerWag' : 'Montré du doigt!',
  'Fired' : 'Liquidé!',
  'FloodTheMarket' : 'Invasion du marché!',
  'FountainPen' : 'Stylo-plume!',
  'FreezeAssets' : 'Capital gelé!',
  'Gavel' : 'Adjugé!',
  'GlowerPower' : 'Regard furieux!',
  'GuiltTrip' : 'Culpabilisation!',
  'HalfWindsor' : 'Nœud de cravate!',
  'HangUp' : 'Interruption!',
  'HeadShrink' : 'Rétrécissement de la tête!',
  'HotAir' : 'Air chaud!',
  'Jargon' : 'Jargon!',
  'Legalese' : 'Expression juridique!',
  'Liquidate' : 'Liquidation!',
  'MarketCrash' : 'Krach boursier!',
  'MumboJumbo' : 'Baragouinage!',
  'ParadigmShift' : 'Changement radical!',
  'PeckingOrder' : 'Hiérarchie!',
  'PickPocket' : 'Vol à la tire!',
  'PinkSlip' : 'Avis de licenciement!',
  'PlayHardball' : 'Grands moyens!',
  'PoundKey' : 'Touche dièse!',
  'PowerTie' : 'Cravate rayée!',
  'PowerTrip' : 'Mégalomanie!',
  'Quake' : 'Tremblement!',
  'RazzleDazzle' : 'Bringue!',
  'RedTape' : 'Paperasserie!',
  'ReOrg' : 'Réorganisation!',
  'RestrainingOrder' : 'Injonction!',
  'Rolodex' : 'Fichier rotatif!',
  'RubberStamp' : 'Tampon!',
  'RubOut' : 'Effacement!',
  'Sacked' : 'Licenciement!',
  'SandTrap' : 'Ensablement!',
  'Schmooze' : 'Jacasserie!',
  'Shake' : 'Secousse!',
  'Shred' : 'Déchiquetage!',
  'SongAndDance' : 'Couplet habituel!',
  'Spin' : 'Tournoiement!',
  'Synergy' : 'Synergie!',
  'Tabulate' : 'Tabulation!',
  'TeeOff' : 'Fâcherie!',
  'ThrowBook' : 'Maximum!',
  'Tremor' : 'Frémissement!',
  'Watercooler' : 'Boissons fraîches!',
  'Withdrawal' : 'Retrait!',
  'WriteOff' : 'Pertes et profits!',
  }

SuitAttackTaunts = {
    'Audit': ["Je crois que ton bilan n'est pas équilibré.",
              "On dirait que tu es dans le rouge.",
              "Laisse-moi t'aider à faire ta comptabilité.",
              "Tes débits sont beaucoup trop élevés.",
              "Vérifions ton capital",
              "Tu vas avoir des dettes.",
              "Regardons de plus près ce que tu dois.",
              "Cela devrait mettre ton compte à sec.",
              "Il est temps que tu comptabilises tes dépenses.",
              "J'ai trouvé une erreur dans ton bilan.",
              ],
    'Bite': ["Tu en veux une bouchée ?",
             "Essaye d'en mordre un morceau!",
             "Tu as les yeux plus gros que le ventre.",
             "Je mords plus que je n'aboie.",
             "Avale donc ça!",
             "Attention, je pourrais mordre.",
             "Je ne fais pas que mordre quand je suis coincé.",
             "J'en veux juste une petite bouchée.",
             "Je n'ai rien avalé de la journée.",
             "Je ne veux qu'un petit morceau. C'est trop demander ?",
             ],
    'BounceCheck': ["Dommage, tu n'as pas d'humour.",
                    "Tu as une échéance de retard.",
                    "Je crois que ce chèque est à toi.",
                    "Tu m'es redevable.",
                    "Je recouvre cette créance.",
                    "Ce chèque ne va pas être un cadeau.",
                    "Tu vas être facturé pour ça.",
                    "Vérifie ce chèque.",
                    "Ça va te coûter cher.",
                    "J'aimerais bien encaisser ça.",
                    "Je vais simplement te renvoyer ton chèque.",
                    "Voilà une facture salée.",
                    "Je déduis des frais de service.",
                    ],
    'BrainStorm':["Je prévois des perturbations.",
                  "J'adore les casse-tête.",
                  "Je voudrais t'éclairer.",
                  "Qu'est-ce que tu penserais de la CHUTE de tes facultés?",
                  "Que de médiocrité!",
                  "Tu es prêt(e) pour le grand déménagement ?",
                  "J'ai les neurones en feu.",
                  "Ça casse des briques.",
                  "Rien de tel qu'un remue-méninges.",
                  ],
    'BuzzWord':["Excuse-moi si je radote.",
                "Tu connais la dernière ?",
                "Tu peux piger ça?",
                "Toonicoton!",
                "Laisse-moi en placer une.",
                "Je serai incontournablement clair.",
                "Tu as dit un mot de trop.",
                "Voyons si tu te situes en transversalité.",
                "Fais attention, ça va être ringard.",
                "Je crois que tu vas faire de l'urticaire.",
                ],
    'Calculate': ["Le compte est bon!",
                  "Tu comptais là-dessus?",
                  "Ajoutes-en un peu, tu es en train de diminuer.",
                  "Je peux t'aider à faire cette addition ?",
                  "Tu as bien enregistré toutes tes dépenses?",
                  "D'après mes calculs, tu n'en as plus pour longtemps.",
                  "Voilà le total général.",
                  "Houlà, ton addition est bien longue.",
                  "Essaie de trafiquer ces chiffres!",
                  Cogs + " : 1 Toons: 0",
                  ],
    'Canned': ["Tu aimes quand c'est en boîte ?",
               "Tu peux t'occuper des boîtes?",
               "Celui-là vient de sortir de sa boîte!",
               "Tu as déjà été attaqué par des boîtes de conserve ?",
               "J'aimerais te faire un cadeau qui se conserve!",
               "Tu es prêt pour la mise en boîte ?",
               "Tu crois que tu es bien conservé?",
               "Tu vas être emballé!",
               "Je me fais du Toon à l'huile pour dîner!",
               "Tu n'es pas si mangeable que ça en conserve.",
               ],
    'Chomp': ["Tu as une mine de papier mâché!",
              "Croc, croc, croc!",
              "On va pouvoir se mettre quelque chose sous la dent.",
              "Tu as besoin de grignoter quelque chose ?",
              "Tu pourrais grignoter ça!",
              "Je vais te manger pour le dîner.",
              "Je me nourrirais bien de Toons!",
              ],
    'ClipOnTie': ["Il faut s'habiller pour la réunion.",
                  "Tu ne peux PAS sortir sans ta cravate.",
                  "C'est ce que portent les " + Cogs + " les plus élégants.",
                  "Essaie pour voir si la taille te va.",
                  "Tu devrais mieux t'habiller pour réussir.",
                  "On ne sert que les clients portant une cravate.",
                  "Tu as besoin d'aide pour enfiler ça?",
                  "Rien n'est plus flatteur qu'une belle cravate.",
                  "Voyons si ça te va.",
                  "Ça va te bouleverser.",
                  "Il va falloir que tu t'habilles avant de SORTIR.",
                  "Je crois que je vais te faire un nœud de cravate.",
                  ],
    'Crunch': ["On dirait que tu es écrasé(e) par les événements.",
               "C'est l'heure d'en écraser!",
               "Je vais te donner quelque chose à pulvériser.",
               "Je vais broyer tout ça.",
               "J'ai tout écrasé.",
               "Tu préfères tendre ou croquant ?",
               "J'espère que tu aimes les croque-monsieur.",
               "On dirait que tu es en train de te faire écraser!",
               "Je vais te réduire en miettes."
               ],
    'Demotion': ["Tu descends sur l'échelle de la hiérarchie.",
                 "Je te renvoie à trier le courrier.",
                 "Il est temps de rendre tes galons.",
                 "Tu descends, petit clown!",
                 "On dirait qu'il y a un blocage.",
                 "Tu progresses lentement.",
                 "Tu es dans une voie sans issue.",
                 "Tu n'iras nulle part dans l'immédiat.",
                 "Tu ne vas nulle part.",
                 "Cela sera porté sur ta fiche d'assiduité.",
                 ],
    'Downsize': ["Redescends donc de là!",
                 "Tu sais comment redescendre ?",
                 "Revenons à nos affaires.",
                 "Qu'est-ce qui ne va pas? Tu as l'air d'avoir le moral dans les chaussettes.",
                 "Tu descends?",
                 "Qu'est-ce qui te chiffonne ? Toi!",
                 "Pourquoi est-ce que tu choisis des gens de ma taille ?",
                 "Pourquoi es-tu si terre-à-terre ?",
                 "Est-ce que tu voudrais un modèle plus petit pour seulement dix cents de plus?",
                 "Essaie pour voir si la taille te va!",
                 "Ce modèle est disponible dans une plus petite taille.",
                 "C'est une attaque à taille unique!",
                 ],
    # Hmmm - where is double talker ?
    'EvictionNotice': ["C'est l'heure de partir!",
                       "Fais tes bagages, Toon.",
                       "C'est le moment d'aller habiter ailleurs.",
                       "Disons que ton bail est terminé.",
                       "Tu as un loyer de retard.",
                       "Cela va être très déstabilisant.",
                       "Tu vas être déraciné d'ici peu.",
                       "Je vais t'envoyer sous les ponts.",
                       "Tu n'es pas à ta place.",
                       "Prépare-toi à une délocalisation.",
                       "Tu vas subir un placement d'office.",
                       ],
    'EvilEye': ["Je te donne le mauvais œil.",
                "Tu peux donner un coup d'œil à ça pour moi?",
                "Attends. J'ai quelque chose dans l'œil.",
                "J'ai l'œil sur toi!",
                "Tu pourrais garder un œil sur ça?",
                "J'ai vraiment l'œil pour voir ce qui cloche.",
                "Je vais te taper dans l'œil.",
                "J'ai le regard méchant!",
                "Tu vas te retrouver dans l'œil du cyclone!",
                "Je te regarde en roulant des yeux.",
                ],
    'Filibuster':["Est-ce que je dois te barrer la route ?",
                  "Ça va nous bloquer pendant un moment.",
                  "Je pourrais rester coincé là toute la journée.",
                  "Je n'ai même pas besoin de respirer.",
                  "J'avance et j'avance et j'avance.",
                  "Je ne m'en fatigue jamais.",
                  "On ne peut pas m'arrêter de parler.",
                  "Tu peux te boucher les oreilles?",
                  "Je crois que je vais te tenir la jambe.",
                  "Je finis toujours par placer un mot.",
                  ],
    'FingerWag': ["Ça fait mille fois que je te le répète!",
                  "Regarde bien là, Toon.",
                  "Ne me fais pas rire.",
                  "Ne m'oblige pas à y aller.",
                  "J'en ai assez de répéter la même chose.",
                  "Je crois qu'on en a déjà parlé.",
                  "Tu n'as aucun respect pour nous les" + Cogs + ".",
                  "Il est grand temps de faire attention.",
                  "Blablablablabla.",
                  "Ne m'oblige pas à mettre fin à cette réunion.",
                  "Est-ce que je vais devoir te séparer ?",
                  "On est déjà passés par là.",
                  ],
    'Fired': ["J'espère que tu as apporté des rafraîchissements.",
              "On s'embête solide.",
              "Ça va nous rafraîchir.",
              "J'espère que tu as le sang froid.",
              "J'ai la gorge sèche.",
              "Va donc nager un peu!",
              "Tu es déjà sur le départ.",
              "Encore un peu de sauce ?",
              "Tu peux dire \"aïe\"?",
              "J'espère que tu sais nager.",
              "Tu es en phase de déshydratation ?",
              "Je vais te liquider!",
              "Tu vas finir en bouillie.",
              "Tu n'es qu'un feu de paille.",
              "Je me trouve fondant.",
              "Je suis d'une limpidité!",
              "Et on n'en parle plus !",
              "Un Toon à la mer !",
              ],
    'FountainPen': ["Ça va tacher.",
                    "Mettons ça par écrit.",
                    "Prépare-toi à des ennuis indélébiles.",
                    "Tu vas avoir besoin d'un bon nettoyage à sec.",
                    "Tu devrais corriger.",
                    "Ce stylo écrit si bien.",
                    "Voilà, je prends mon crayon.",
                    "Tu peux lire mon écriture ?",
                    "Et voilà la plume de l'apocalypse.",
                    "Ta performance est entachée.",
                    "Tu n'as pas envie de tout effacer ?",
                    ],
    'FreezeAssets': ["Ton capital est le mien.",
                     "Tu ne sens pas un appel de fonds?",
                     "J'espère que tu n'as pas de projets.",
                     "Cela devrait te mettre sur la paille.",
                     "Le fond de l'air est frais.",
                     "L'hiver va venir tôt cette année.",
                     "Tu as froid?",
                     "Je vais geler mes projets.",
                     "Tu vas trouver ça froid.",
                     "Tu vas avoir des engelures.",
                     "J'espère que tu aimes la viande froide.",
                     "Je garde mon sang-froid.",
                     ],
    'GlowerPower': ["Tu me regardes?",
                    "On me dit que j'ai une vue perçante.",
                    "J'aime bien que tu sois à portée de mon regard.",
                    "Tu n'aimes pas que je te regarde ?",
                    "Voilà, je te regarde.",
                    "Tu ne trouves pas que j'ai un regard expressif?",
                    "Mon regard est mon point fort.",
                    "C'est le regard qui compte.",
                    "Coucou, je te vois.",
                    "Regarde-moi dans les yeux...",
                    "Est-ce que tu voudrais voir ton avenir ?",
                    ],
    'GuiltTrip': ["Tu vas vraiment te sentir coupable!",
                  "Tu te sens coupable!",
                  "C'est entièrement de ta faute!",
                  "C'est toujours ta faute.",
                  "Tu te complais dans la culpabilité!",
                  "Je ne te reparlerai plus jamais!",
                  "Tu ferais mieux de t'excuser.",
                  "Jamais je ne te pardonnerai!",
                  "Tu veux bien te faire de la bile ?",
                  "Rappelle-moi quand tu ne te sentiras plus coupable.",
                  "Quand finiras-tu par te pardonner à toi-même ?",
                  ],
    'HalfWindsor': ["Tu ne t'es encore jamais fait cravater comme ça!",
                    "Essaye de ne pas trop faire de nœuds.",
                    "Tu es dans une situation inextricable.",
                    "Tu as de la chance, j'aurais pu faire un nœud plus serré.",
                    "Cette cravate est trop chère pour toi.",
                    "Je crois que tu n'as jamais même VU de nœud de cravate!",
                    "Cette cravate est trop chère pour toi.",
                    "Cette cravate serait gâchée, sur toi.",
                    "Tu ne vaux même pas la moitié du prix de cette cravate!",
                  ],
    'HangUp': ["Tu as été déconnecté(e).",
               "Au revoir!",
               "C'est l'heure de mettre fin à notre conversation.",
               "...et ne me rappelle pas!",
               "Clic!",
               "La conversation est terminée.",
               "Je vais couper cette ligne.",
               "Je crois que nous allons être coupés.",
               "On dirait que la ligne est défectueuse.",
               "Ton forfait est terminé.",
               "J'espère que tu m'entends clairement.",
               "Tu as fait le mauvais numéro.",
               ],
    'HeadShrink': ["On dirait que tu as besoin de te faire soigner la tête.",
                   "Chérie, j'ai rétréci le Toon.",
                   "J'espère que ça ne t'est pas monté à la tête.",
                   "Tu rétrécis au lavage ?",
                   "Je rétrécis donc je suis.",
                   "Il n'y a pas de quoi perdre la tête.",
                   "Où as-tu la tête ?",
                   "Relève la tête! Ou plutôt, mets-la par terre.",
                   "Les choses sont parfois plus grandes qu'elles ne paraissent.",
                   "Les bons Toons se vendent par petits paquets.",
                   ],
    'HotAir':["Nous avons de chaudes discussions.",
              "Tu subis une vague de chaleur.",
              "J'ai atteint mon point d'ébullition.",
              "Cela pourrait te brûler.",
              "Je détesterais te passer au gril, mais...",
              "N'oublie pas qu'il n'y a pas de fumée sans feu.",
              "Tu m'as l'air un peu grillé(e).",
              "C'est encore un écran de fumée.",
              "C'est le moment de mettre de l'huile sur le feu.",
              "Allumons le feu de l'amitié.",
              "J'ai des remarques brûlantes à te faire.",
              "Air chaud!",
              ],
    'Jargon':["Quel non-sens.",
              "Regarde si tu peux trouver du sens à tout ça.",
              "J'espère que tu m'entends clairement.",
              "On dirait que je vais devoir élever la voix.",
              "J'ai vraiment mon mot à dire.",
              "J'ai mon franc-parler.",
              "Je vais pontifier sur ce sujet.",
              "Tu sais, les mots peuvent faire mal.",
              "Tu as compris ce que je voulais dire ?",
              "Des mots, rien que des mots.",
              ],
    'Legalese':["Tu dois cesser d'être et renoncer.",
                "Tu vas être débouté(e), légalement parlant.",
                "Tu es au courant des implications légales?",
                "Tu n'es pas au-dessus des lois!",
                "Il devrait y avoir une loi contre toi.",
                "Il n'y a rien de postérieur aux faits!",
                "Toontown Online de Disney n'est pas légalement responsable des opinions exprimées dans cette attaque.",
                "Nous ne serons pas tenus responsables des dommages subis suite à cette attaque.",
                "Les résultats de cette attaque peuvent différer.",
                "Cette attaque est nulle là où elle n'est pas autorisée.",
                "Tu ne rentres pas dans mon système législatif.",
                "Tu ne peux pas gérer les questions juridiques.",
                ],
    'Liquidate':["J'aime bien que les choses restent fluides.",
                 "As-tu des problèmes de liquidités?",
                 "Je dois purger ton capital.",
                 "Il est temps pour toi de suivre le flux monétaire.",
                 "N'oublie pas que ça glisse quand c'est mouillé.",
                 "Il y a des fuites dans ta comptabilité.",
                 "Tu as l'air de perdre pied.",
                 "Tout te tombe dessus.",
                 "Je crois que tu vas subir une dilution.",
                 "Tu es lessivé(e).",
                 ],
    'MarketCrash':["Tu vas avoir un choc.",
                   "Tu ne survivras pas au choc.",
                   "C'est plus que la bourse ne peut en supporter.",
                   "J'ai un traitement de choc pour toi!",
                   "Maintenant je vais te faire un choc.",
                   "Je m'attends à un choc boursier.",
                   "On dirait que le marché est sur la pente descendante.",
                   "Il vaudrait mieux que tu te retires du jeu!",
                   "Vends! Vends! Vends!",
                   "Est-ce que je dois mener la récession ?",
                   "Tout le monde s'enfuit, tu devrais peut-être en faire autant ?",
                   ],
    'MumboJumbo':["Que ce soit parfaitement clair.",
                  "C'est aussi simple que ça.",
                  "C'est comme cela que nous allons procéder.",
                  "Laisse-moi te l'écrire en grosses lettres.",
                  "C'est du jargon technique.",
                  "Ma parole est d'argent.",
                  "J'en ai plein la bouche.",
                  "On dit que je suis grandiloquent.",
                  "Je vais interjeter ça.",
                  "Je crois que ce sont les mots adéquats.",
                   ],
    'ParadigmShift':["Fais attention! Je suis plutôt changeant.",
                     "Prépare-toi pour un changement radical!",
                     "Voilà donc des substitutions intéressantes.",
                     "Tu n'es pas à ta place.",
                     "C'est ton tour de changer de place.",
                     "Ton temps de présence est terminé.",
                     "Tu n'as encore jamais autant changé dans ta vie.",
                     "Voilà qui est radical!",
                     "La lumière est changeante!",
                     ],
    'PeckingOrder':["Pauvre sous-fifre!",
                    "Tu vas te retrouver le bec dans l'eau.",
                    "Tu vas te retrouver en bas de l'échelle.",
                    "Ce n'est pas une attaque de débutant.",
                    "Tu es tout en bas de la hiérarchie.",
                    "Je vaux bien plus cher que toi!",
                    "La hiérarchie, il n'y a que ça de vrai!",
                    "Pourquoi est-ce que je ne trouve pas d'adversaire à ma taille ? Bof.",
                    "À moi le pouvoir!",
                    ],
    'PickPocket': ["Laisse-moi vérifier tes valeurs.",
                   "Eh, c'est quoi par ici?",
                   "C'est comme faucher les jouets d'un enfant.",
                   "C'est du vol.",
                   "Je te garde ça.",
                   "Ne lâche pas mes mains des yeux.",
                   "Mes mains sont plus rapides que tes yeux.",
                   "Je n'ai rien dans la manche.",
                   "La direction n'est pas responsable des objets perdus.",
                   "Qui trouve garde.",
                   "Tu ne le verras jamais revenir.",
                   "Tout pour moi, rien pour toi.",
                   "Ça ne te gêne pas que ça me gêne ?",
                   "Tu n'en auras plus besoin...",
                   ],
    'PinkSlip': ["On n'a pas besoin de ton avis.",
                 "Tu as peur de cette vague de licenciements?.",
                 "Celui-là va sûrement être d'un avis contraire.",
                 "Oh, tu as une licence de quoi?",
                 "Fais attention, si tu veux mon avis!",
                 "N'oublie pas que ça glisse à mon avis.",
                 "Je vais juste te renvoyer celui-là.",
                 "Tu ne te fâcheras pas si je te donne mon avis?",
                 "Tu ne vois pas l'avis en rose.",
                 "Tu peux sortir, je te licencie.",
                 ],
    'PlayHardball': ["Tu veux employer les grands moyens?",
                     "N'essaie pas d'employer tous les moyens avec moi.",
                     "Ne prends pas tes grands airs!",
                     "Tu es vraiment moyen(ne).",
                     "Et voilà le bon moyen...",
                     "Tu vas avoir besoin d'un bon moyen pour t'en sortir.",
                     "Je vais te chasser d'ici à grande vitesse.",
                     "Une fois que je t'aurai touché(e), tu rentreras en courant chez toi.",
                     "C'est ton grand départ!",
                     "Ton jeu est très moyen.",
                     "Je vais tout faire pour que tu sortes.",
                     "Je t'envoie promener dans les grandes largeurs!",
                    ],
    'PoundKey': ["Il est temps que je réponde à quelques appels.",
                 "J'aimerais faire un appel en PCV.",
                 "Dring dring, c'est pour toi!",
                 "Je vais bien toucher quelque chose.",
                 "Je devais te rappeler.",
                 "Cela devrait provoquer une sonnerie.",
                 "Je vais juste faire ce numéro.",
                 "Je t'appelle pour te faire une surprise.",
                 "Je vais t'appeler.",
                 "Allô Toon, c'est pour toi.",
                 ],
    'PowerTie': ["Je t'appellerai plus tard, tu as l'air d'avoir un nœud à l'estomac.",
                 "Tu te prépares à faire un trait là-dessus?",
                 "Tu vas te faire cravater.",
                 "Tu ferais mieux d'apprendre à faire un nœud de cravate.",
                 "Je vais te nouer la langue!",
                 "Tu n'as encore jamais vu quelqu'un se faire cravater comme ça!",
                 "Tu fais attention aux rayures?",
                 "Je vais te rayer de la carte!",
                 "Je rayonne!",
                 "Par les pouvoirs qui me sont conférés, je te raie de la liste.",
                 ],
    'PowerTrip': ["Fais tes valises, on fait un méga voyage.",
                  "Tu n'as pas perdu tes manies?",
                  "C'est une manie que tu as de partir en vacances.",
                  "Comment se sont passées les vacances?",
                  "C'est une vraie manie!",
                  "Ça a l'air méga ennuyeux.",
                  "Maintenant tu vois qui est le plus puissant!",
                  "Je suis bien plus puissant que toi.",
                  "Qui a les méga pouvoirs maintenant ?",
                  "Tu ne peux pas te battre contre ma puissance.",
                  "La puissance est corrompue, en particulier dans mon cas.",
                  ],
    'Quake': ["Tremblons, mes frères.",
              "J'ai la tremblote!",
              "Je te vois trembler dans tes chaussures.",
              "Voilà la terre qui tremble!",
              "Celui-ci est en-dehors de l'échelle de Richter.",
              "La terre va trembler!",
              "Hé, qu'est-ce qui tremble comme ça? Toi!",
              "Tu as déjà ressenti un tremblement de terre ?",
              "Tu es sur un terrain instable!",
              ],
    'RazzleDazzle': ["Chante avec moi.",
                     "Tu as peur de perdre ton dentier ?",
                     "Je ne suis pas charmant ?",
                     "Je vais t'impressionner.",
                     "Mon dentiste fait un excellent travail.",
                     "Ils ne sont pas épatants?",
                     "Difficile de croire qu'ils ne sont pas réels.",
                     "Ils ne sont pas choquants?",
                     "Ça va décoiffer.",
                     "Je me lave les dents après tous les repas.",
                     "Dis \"Cheese!\"",
                     ],
    'RedTape': ["Ça va être bien emballé.",
                "Tu vas rester collé(e) là un bon moment.",
                "J'en ai un plein rouleau.",
                "On va voir si tu peux y couper.",
                "Ça va devenir collant.",
                "J'espère que tu es claustrophobe.",
                "Tu es d'un tempérament collant!",
                "Je vais t'occuper un peu.",
                "Essaie donc de sortir de là.",
                "On va voir si ça colle entre nous.",
                ],
    'ReOrg': ["Tu n'aimes pas la manière dont j'ai réorganisé les choses?",
              "Peut-être qu'un peu plus d'organisation serait de mise.",
              "Tout n'est pas si mauvais, tu as juste un peu besoin de réorganisation.",
              "Est-ce que tu apprécies mes capacités d'organisation ?",
              "J'essaye juste de donner un nouvel aspect aux choses.",
              "Tu dois t'organiser!",
              "Tu m'as l'air de faire dans la désorganisation.",
              "Reste là pendant que je te réorganise.",
              "Je vais attendre que tu aies le temps de t'organiser.",
              "Ça ne te dérange pas si je réorganise un peu?",
              ],
    'RestrainingOrder': ["Tu devrais faire la jonction.",
                         "Je t'assène une injonction!",
                         "Tu n'as pas le droit de t'approcher à moins de deux mètres de moi.",
                         "Tu ferais peut-être mieux de garder tes distances.",
                         "Tu devrais avoir une injonction.",
                         Cogs + "! Maîtrisez ce Toon!"
                         "Essaie de te maîtriser.",
                         "J'espère que je ne suis pas trop une contrainte pour toi.",
                         "Voyons si tu peux te libérer de ces contraintes!",
                         "Je te donne l'injonction de te maîtriser!",
                         "Pourquoi ne commençons-nous pas par les contraintes de base ?"
                         ],
    'Rolodex': ["Ta fiche est quelque part là-dedans.",
                "Voilà la fiche de la chasse aux nuisibles.",
                "Je vais te donner une fiche.",
                "Ton numéro est juste là.",
                "Je te couvre de A à Z.",
                "Tu vas avoir la tête qui tourne.",
                "Va donc faire un tour.",
                "Attention aux bouts de papier.",
                "J'ai des doigts pour trier.",
                "Est-ce que c'est comme ça que je peux te contacter ?",
                "Je voudrais être certain que nous allons rester en contact.",
                ],
    'RubberStamp': ["Je fais toujours bonne impression.",
                    "Il est important de bien appuyer.",
                    "Une impression parfaite à chaque fois.",
                    "Je voudrais que tu imprimes.",
                    "Tu dois être RETOURNÉ à L'ENVOYEUR.",
                    "Tu es dans la pile ANNULÉ.",
                    "Tu es en livraison PRIORITAIRE.",
                    "Je voudrais être certain que tu as REÇU mon message!",
                    "Tu ne vas nulle part - tu es en PORT PAYÉ par le DESTINATAIRE.",
                    "Je veux une réponse URGENTE.",
                    ],
    'RubOut': ["Et maintenant un acte de disparition.",
               "J'ai l'impression de t'avoir perdu quelque part.",
               "J'ai décidé de te gommer.",
               "Je gomme toujours tous les obstacles.",
               "Je vais simplement effacer cette erreur.",
               "Je peux faire disparaître tous les ennuis.",
               "J'aime les choses nettes et propres.",
               "Essaie de mettre la gomme.",
               "Je te vois...je ne te vois plus.",
               "Cela va finir par pâlir.",
               "Je vais éliminer le problème.",
               "Laisse-moi m'occuper de tes zones à problèmes.",
               ],
    'Sacked':["On dirait que tu vas te faire licencier.",
              "L'affaire est dans le sac.",
              "Tu as une licence de vol?",
              "De chasse ou de pêche ?",
              "Mes ennemis vont être à la porte!",
              "J'ai le record de Toontown pour les licenciements.",
              "On n'a plus besoin de toi ici.",
              "Tu as passé assez de temps ici, tu es renvoyé(e)!",
              "Laisse-moi te mettre en boîte.",
              "Tu ne peux pas te défendre si je veux te mettre dehors!",
              ],
    'Schmooze':["Tu ne verras jamais ça venir.",
                "Ça fera bien sur toi.",
                "Tu as gagné ça.",
                "Je ne voulais pas baver.",
                "La flatterie mène partout.",
                "Je vais en rajouter une couche.",
                "C'est le moment d'en rajouter.",
                "Je vais me mettre de ton bon côté!",
                "Ça mérite une bonne tape dans le dos.",
                "Je vais chanter tes louanges.",
                "Je suis navré de te faire tomber de ton piédestal, mais...",
                ],
    'Shake': ["Tu es juste à l'épicentre.",
              "Tu es juste sur une faille.",
              "Ça va secouer.",
              "Je crois que c'est une catastrophe naturelle.",
              "C'est un désastre de proportions sismiques.",
              "Celui-ci est en dehors de l'échelle de Richter.",
              "C'est le moment de se mettre à l'abri.",
              "Tu as un air troublé.",
              "Attention la secousse!",
              "Je vais te secouer, pas te faire tourner.",
              "Ça devrait te secouer.",
              "J'ai un bon plan pour s'échapper.",
              ],
    'Shred': ["Je dois me débarrasser de quelques déchets.",
              "J'augmente ma capacité de traitement.",
              "Je crois que je vais me débarrasser de toi maintenant.",
              "On va pouvoir détruire les preuves.",
              "Il n'y a plus aucune façon de prouver ça maintenant.",
              "Vois si tu peux assembler toutes les pièces.",
              "Cela devrait te remettre à la bonne taille.",
              "Je vais jeter cette idée.",
              "Il ne faut pas que ça tombe entre de mauvaises mains.",
              "Vite venu, vite parti.",
              "Ce n'est pas ton dernier fragment d'espoir ?",
              ],
    'Spin': ["Tu veux qu'on aille faire un tour ?",
             "À quelle vitesse tournes-tu?",
             "Ça va te faire tourner la tête!",
             "C'est le tour que prennent les choses.",
             "Je vais t'emmener faire un tour.",
             "Que feras-tu quand ce sera ton tour ?",
             "Surveille-moi ça. Je ne voudrais pas que ça tourne trop vite!",
             "Tu vas tourner longtemps comme ça?",
             "Mes attaques vont te donner le tournis!",
             ],
    'Synergy': ["Je transmets cela au comité.",
                "Ton projet a été annulé.",
                "Ton budget a été réduit.",
                "Nous allons restructurer ton service.",
                "J'ai mis ça au vote et tu as perdu.",
                "Je viens de recevoir l'accord final.",
                "Il n'y a pas de problèmes, il n'y a que des solutions.",
                "Je te recontacte à ce sujet.",
                "Revenons à cette affaire.",
                "Considère que c'est un manque de synergie.",
                ],
    'Tabulate': ["Ça ne s'additionne pas!",
                 "Si je compte bien, tu as perdu.",
                 "Tu comptes bien toutes les colonnes.",
                 "Je te fais le total dans un instant.",
                 "Tu es prêt(e) à compter tout ça?",
                 "Ta facture est payable dès maintenant.",
                 "Il est temps de faire une estimation.",
                 "J'aime bien mettre les choses en ordre.",
                 "Et les résultats au pointage sont...",
                 "Ces chiffres devraient être très puissants.",
                 ],
    'TeeOff': ["Tu ne fais pas le poids.",
               "Gare à toi!",
               "Je suis vexé.",
               "Pourquoi es-tu en colère ?",
               "Essaye simplement d'éviter le danger.",
               "Scrongneugneu!",
               "Tu vas prendre la mouche à tous les coups.",
               "Tu es sur mon chemin.",
               "J'ai une bonne prise sur la situation.",
               "Attention le petit oiseau va se fâcher!",
               "Garde un œil sur moi!",
               "Ça te dérange si je joue ?",
               ],
    'Tremor': ["Tu as senti ça?",
               "Tu n'as pas peur d'un petit frémissement n'est-ce pas?",
               "Au commencement était le frémissement.",
               "Tu as l'air de trembler.",
               "Je vais un peu secouer les choses!",
               "Tu te prépare à sursauter ?",
               "Qu'est-ce qui ne va pas? Tu as l'air d'accuser la secousse.",
               "Crainte et tremblements!",
               "Pourquoi trembles-tu de peur ?",
               ],
    'Watercooler': ["Ça devrait te rafraîchir.",
                    "Tu ne trouves pas ça rafraîchissant ?",
                    "Je livre les boissons.",
                    "Directement du robinet dans ton gosier.",
                    "C'est quoi le problème, c'est juste de l'eau de source.",
                    "Ne t'inquiète pas, c'est filtré.",
                    "Ah, un autre client satisfait.",
                    "C'est l'heure de ta livraison quotidienne.",
                    "J'espère que les couleurs ne vont pas déteindre.",
                    "Tu as envie de boire ?",
                    "Tout s'en va à la lessive.",
                    "C'est toi qui paies à boire.",
                    ],
    'Withdrawal': ["Je crois que tu es à découvert.",
                   "J'espère que ton compte est suffisamment approvisionné.",
                   "Prends ça, avec les intérêts.",
                   "Ton solde n'est pas en équilibre.",
                   "Tu vas bientôt devoir faire un dépôt.",
                   "Tu as souffert de la récession économique.",
                   "Je crois que tu as un passage à vide.",
                   "Tes finances sont sur le déclin.",
                   "Je prévois une baisse définitive.",
                   "C'est un revers de fortune.",
                   ],
    'WriteOff': ["Laisse-moi augmenter tes pertes.",
                 "Profitons d'une mauvaise affaire.",
                 "C'est l'heure d'équilibrer les comptes.",
                 "Ça ne va pas faire bien dans ton bilan.",
                 "Je suis à la recherche de quelques dividendes.",
                 "Tu dois tenir compte de tes pertes.",
                 "Tu peux oublier les bonus.",
                 "Je vais mélanger tes comptes.",
                 "Tu vas avoir quelques pertes.",
                 "Ça va te faire mal au solde.",
                 ],
    }

# DistributedBuilding.py
BuildingWaitingForVictors = "En attente des autres joueurs...",

# Elevator.py
ElevatorHopOff = "Quitter"
ElevatorStayOff = "Si tu descends, tu devras attendre \nque l'ascenseur se vide ou parte"
ElevatorLeaderOff = "Seul ton chef peut décider du moment où descendre."
ElevatorHoppedOff = "Tu dois attendre le prochain ascenseur"
ElevatorMinLaff = "Il te faut %s rigolpoints pour prendre cet ascenseur"
ElevatorHopOK = "OK"
ElevatorGroupMember = "Seul le chef de ton groupe peut\n décider quand monter"

# DistributedCogKart.py
KartMinLaff = "Il te faut %s rigolpoints pour monter dans ce kart"

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = " SA"
CogsIncModifier = "%s"+ CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Toc, toc."
DoorWhosThere = "Qui est là?"
DoorWhoAppendix = "qui?"
DoorNametag = "Porte"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "Tu as besoin de gags! Va en parler à Tom Tuteur!"
FADoorCodes_DEFEAT_FLUNKY_HQ = "Reviens ici quand tu auras vaincu le Laquaistic!"
FADoorCodes_TALK_TO_HQ = "Va chercher ta récompense auprès d'Harry au QG!"
FADoorCodes_WRONG_DOOR_HQ = "Mauvaise porte! Prends l'autre porte pour aller au terrain de jeux!"
FADoorCodes_GO_TO_PLAYGROUND = "Mauvais chemin! Tu dois aller au terrain de jeux!"
FADoorCodes_DEFEAT_FLUNKY_TOM = "Marche jusqu'à ce Laquaistic pour te battre avec lui!"
FADoorCodes_TALK_TO_HQ_TOM = "Va chercher ta récompense au QG des Toons!"
FADoorCodes_SUIT_APPROACHING = None  # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "Fais attention! Il y a un COG là-dedans!"
FADoorCodes_DISGUISE_INCOMPLETE = "Tu vas te faire attraper si tu rentres là-dedans habillé en Toon! Tu dois d'abord terminer ton déguisement de Cog!n\nConstruis ton déguisement de Cog avec des pièces de l'usine."
FADoorCodes_SB_DISGUISE_INCOMPLETE = "Tu vas te faire attraper si tu rentres là-dedans habillé en Toon! Tu dois d'abord terminer ton déguisement de Cog!n\nConstruis ton déguisement de Cog avec des pièces de l'usine."
FADoorCodes_CB_DISGUISE_INCOMPLETE = "Tu vas te faire prendre si tu entres ici en Toon! Tu dois d'abord terminer ton déguisement de Caissbot!\n\nTermine ton déguisement de Caissbot en réussissant des défitoons au Pays des Rêves."
FADoorCodes_LB_DISGUISE_INCOMPLETE = "Tu vas te faire attraper si tu rentres là-dedans habillé en Toon! Tu dois d'abord terminer ton déguisement de Loibot !\n\nAssemble ton déguisement de Loibot en terminant les défitoons qui sont après le Pays des Rêves de Donald."

# KnockKnock joke contest winners
KnockKnockContestJokes = {
    2100 : ["Tank",
            "Tank il ne regarde pas, lance-lui un gâteau!"],

    2200 : ["Audrey",
            "Audrey mieux sortir d'ici, voilà les Cogs qui arrivent!"],

    2300: ["Hadrien",
           "Hadrien que quelques pièces Cog et on y va!"],

    # Polar Place has multiple jokes so they are in a dict keyed of the propId of the door
    3300: { 10: ["Aladdin",
                   "Aladdin mauvais goût..."],
            6 : ["Bidule",
                 "Bidule sais pas, d'où ils viennent tous ces Cogs?"],
            30 : ["Jambon",
                  "Jambon, ils sont même très bons ces gâteaux pour les Cogs."],
            28: ["Isaïe",
                 "Isaïe à la gare pour aller faire un tour de tramway."],
            12: ["Jules",
                 "Jules aurait parié, tu vas me laisser entrer dans un bâtiment Cog et je te donnerai un toonique."],
            },
    }

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Qui",
    "Il y a un mauvais écho par ici, n'est-ce pas?"],

    ["Douglas",
    "Douglas à la vanille ça t'intéresse ?"],

    ["Geoffrey",
    "Geoffrey bien une petite sieste, laisse-moi entrer."],

    ["Justin",
    "Justin petit moment."],

    ["Adhémar",
    "Adhémar pas ta voiture ?"],

    ["Annie",
    "Annie rien comprendre, pourquoi tu n'ouvres pas?"],

    ["Omer",
    "Omer veille, j'ai fini par te trouver."],

    ["Thérèse",
    "Thérèse, t'es là sans bouger depuis tout ce temps?"],

    ["Sylvie",
    "Sylvie c'est un miracle, laisse-le au moins entrer."],

    ["Aude",
    "Aude toilette à la lavande ce matin ?"],

    ["Alex",
    "Alex Térieur, j'ai froid dehors."],

    ["Alain",
    "Alain Térieur, je voudrais entrer!"],

    ["Justine",
    "Justine petite minute, je n'en ai pas pour longtemps."],

    ["Vincent",
    "Vincent rien, et repart sans rien."],

    ["Jean",
    "Jean ai marre que tu n'ouvres pas cette porte!"],

    ["Firmin",
    "Firmin peu la radio tu m'entendrais mieux."],

    ["Geoffroy",
    "Geoffroy dehors laisse-moi entrer."],

    ["Jessica",
    "Jessica difficiles à traiter, dépêche-toi un peu."],

    ["Djamila",
    "Djamila clé sous la porte."],

    ["Emma",
    "Emma claqué la porte au nez!!"],

    ["Nicole",
    "Nicole rien du tout ça doit rester propre."],

    ["Yann-Adam",
    "Yann-Adam le frigo je peux entrer ?"],

    ["Louis",
    "Louis pas trop fine, décidément."],

    ["Mélusine",
    "Mélusine des Cogs en faillite, au lieu de dormir."],

    ["Kim",
    "Kim énerve, à ne pas ouvrir."],

    ["Ella",
    "Ella pas envie de descendre ouvrir ?"],

    ["Jean",
    "Jean file un pull et j'arrive."],

    ["Roger",
    "Roger plus rien dans le frigo, tu peux aller faire les courses?"],

    ["John",
    "John Dœuf est déjà passé vendre de la mayonnaise ?"],

    ["Alain",
    "Alain d'Issoire! C'est ça, bon dimanche."],

    ["Steve",
    "Steve a, j'y vais aussi."],

    ["Elvire",
    "Elvire pas sur ses gonds, ta porte."],

    ["Jean",
    "Jean, bon, je peux entrer finalement ?"],

    ["Sarah",
    "Sarah fraîchit dernièrement, j'ai froid dehors."],

    ["Aïcha",
    "Aïcha fait mal aux mains de frapper à ta porte."],

    ["Sarah",
    "Sarah croche toujours au téléphone, tu ne veux vraiment pas me parler ?"],

    ["Déborah",
    "Déborah, dis, qu'il y a dans ton jardin, je peux les voir ?"],

    ["Eddy",
    "Eddy donc toi là-bas, tu vas finir par venir ?"],

    ["Élie",
    "Élie quoi? Le journal est déjà arrivé?"],

    ["Mandy",
    "Mandy donc tu fais quoi là?"],

    ["Yvon",
    "Yvon pas revenir plus tard si tu n'ouvres pas!"],

    ["Isabelle",
    "Isabelle toujours à n'importe quelle heure."],

    ["Robin",
    "Robin, dis donc, c'est maintenant que tu arrives?"],

    ["Oscar",
    "Oscar, il n'est jamais à l'heure, je prendrai le train la prochaine fois."],

    ["Léonard",
    "Léonard j'aime pas, j'aime mieux les langoustines - merci quand même pour ton invitation."],

    ["Gérard",
    "Gérard, mais rarement vu ça."],

    ["Théa",
    "Théa l'heure, pour une fois?"],

    ["Médor",
    "Médor, Médor, mais comment veux-tu que je dorme si tu ne me laisses pas entrer ?"],

    ["Stella",
    "Stella mais c'est plus là."],

    ["Isidore",
    "Isidore que la nuit, il est parti à l'heure qu'il est."],

    ["Élodie",
    "Élodie, donc? C'est pas fini?"],

    ["Julien",
    "Julien du tout à te donner."],

    ["Yvan",
    "Yvan quoi? J'ai besoin de rien."],

    ["Eugène",
    "Eugène pas du tout, prend ton temps."],

    ["Sultan",
    "Sultan de travail, je ne peux pas dormir."],

    ["André",
    "Mais André donc."],

    ["Alphonse",
    "Alphonse pas dans l'escalier en venant ouvrir."],

    ["Amélie",
    "Amélie donc ce qui est écrit au lieu de redemander."],

    ["Angèle",
    "Angèle pas du tout, il ne fait pas froid."],

    ["Aubin",
    "Aubin dis donc, quand est-ce que tu arrives?"],

    ["Cécile",
    "Cécile est de bonne humeur qu'il vient ouvrir la porte ?"],

    ["Djemila",
    "Djemila clé dans la serrure mais ça ne marche pas."],

    ["Éléonore",
    "Éléonore maintenant mais j'ai pas sa nouvelle adresse."],

    ["Huguette",
    "Huguette si quelqu'un d'autre arrive ?"],

    ["Isolde",
    "Isolde pas, tout est au prix fort."],

    ["Jenny",
    "Jenny figues ni raisin, l'épicerie a déménagé."],

    ["Jérémie",
    "Jérémie le courrier à la poste, maintenant je suis rentré."],

    ["Jimmy",
    "Jimmy ton courrier dans la boîte"],

    ["Johnny",
    "Johnny connais rien du tout, viens donc voir ça."],

    ["Julie",
    "Julie pas très bien ce qui est écrit sur la porte."],

    ["Cathy",
    "Cathy donc dit ?"],

    ["Léo",
    "Léo lit encore à cette heure-là?"],

    ["Léon",
    "Léon-dit, ça ne m'intéresse pas. Je préfère que tu me dises la vérité."],

    ["Maël",
    "Maël dit toujours la même chose!"],

    ["Marin",
    "Marin du tout, je veux juste te dire bonjour."],

    ["Quentin",
    "Quentin est là, on ouvre."],

    ["Sacha",
    "Sacha pas, demande-lui directement."],

    ["Stella",
    "Stella tu ouvres. Réponds!"],

    ["Théophile",
    "Théophile encore une fois, tu ne fais que téléphoner."],

    ["Tudor",
    "Tudor tout le temps quand je passe te voir."],

    ["Véra",
    "Véra bien qui c'est si tu descends ouvrir."],

    ["Xavier",
    "Xavier pas une sonnette la dernière fois?"],

    ["Yann",
    "Yann a plus, y'en aura la prochaine fois."],

    ["Yvon",
    "Yvon bien, merci de prendre des nouvelles!"],

    ["Odyssée",
    "Odyssée quoi toutes ces questions?"],

    ["Thor",
    "Thor ait le temps de descendre ouvrir ?"],

    ["Édith",
    "Édith a vu l'heure, il est bien temps d'arriver."],

    ["Jean-Aymar",
    "Jean-Aymar d'attendre."],

    ["Aubin",
    "Aubin dis donc, tu en mets un temps!"],

    ["Ahmed",
    "Ahmed dépens, j'ai fini par comprendre."],

    ["Henri",
    "Henri encore, de ta dernière blague."],

    ["Aude",
    "Aude désespoir, ô rage."],

    ["Ali",
    "Ali qu'a tort, comme d'habitude."],

    ["Gilles",
    "Gilles est de sauvetage aujourd'hui."],

    ["Hans",
    "Hans qui me concerne, j'aimerais bien que tu ouvres la porte."],

    ["Roméo",
    "Roméo lendemain ce que tu ne peux pas faire aujourd'hui."],

    ["Hildéphonse",
    "Hildéphonse la porte."],

    ["Helmut",
    "Helmut le pain de la bouche!"],

    ["Hercule",
    "Hercule la voiture au fond de la cour."],

    ["Mylène",
    "Mylène, mi-coton."],

    ["Célestin",
    "Célestin ? Non c'est l'ouest."],

    ["Ondine",
    "Ondine où ce soir ?"],

    ["Laurent",
    "Laurent-Outang, je cherche le zoo?"],

    ["Anne",
    "Anne pas dire."],

    ["Edgar",
    "Edgar pas là, tu gênes."],

    ["José",
    "José pas le dire."],

    ["Samira",
    "Samira pas c'est trop petit."],

    ["Humphrey",
    "Humphrey peur celui-là!"],

    ["Saturnin",
    "Saturnin peu trop vite."],

    ["Juste",
    "Juste pour voir."],

    ["Aziza",
    "Aziza pouvait durer!"],

    ["Jonathan",
    "Jonathan que toi."],

    ["Aubin",
    "Aubin, ça alors! Je ne comptais pas sur toi."],

    ["Yamamoto",
    "Yamamoto qu'a dérapé, je cherche un garage."],

    ["Stanislav",
    "Stanislav tous les matins sous sa douche."],

    ["Yvan-Dédé",
    "Yvan-Dédé, voitures d'occasion."],

    ["Céline",
    "Céline évitable."],

    ["Jean-Philémon",
    "Jean-Philémon blouson et je viens."],
]

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "Salut, %!",
        "Youhouu %,\nravi de te voir.",
        "Je suis content que tu sois là aujourd'hui!",
        "Bien le bonjour, %.",
        ]

SharedChatterComments = [
        "C'est un super nom, %.",
        "J'aime bien ton nom.",
        "Fais attention aux" + Cogs + "."
        "On dirait que le tramway arrive!",
        "Je dois jouer à un jeu du tramway pour avoir quelques morceaux de tarte!",
        "Quelquefois, je joue aux jeux du tramway juste pour manger de la tarte aux fruits!",
        "Ouf, je viens d'arrêter un groupe de" + Cogs + ". J'ai besoin de repos!",
        "Aïe, certains de ces" + Cogs + " sont costauds!",
        "On dirait que tu t'amuses.",
        "Oh bon sang, quelle bonne journée.",
        "J'aime bien ce que tu portes.",
        "Je crois bien que je vais aller à la pêche cet après-midi.",
        "Amuse-toi bien dans mon quartier.",
        "J'espère que tu profites bien de ton séjour à Toontown!",
        "J'ai entendu dire qu'il neigeait dans le Glagla.",
        "Est-ce que tu as fait un tour de tramway aujourd'hui?",
        "J'aime bien rencontrer des nouveaux.",
        "Aïe, il y a beaucoup de " + Cogs + " dans le Glagla.",
        "J'aime bien jouer à chat. Et toi ?",
        "Les jeux du tramway sont amusants.",
        "J'aime bien faire rire les gens.",
        "J'adore aider mes contacts.",
        "Hum, serais-tu perdu(e)? N'oublie pas que ta carte est dans ton journal de bord.",
        "Essaie de ne pas te noyer dans la paperasserie des " + Cogs + ".",
        "J'ai entendu dire que " + Daisy + " a planté de nouvelles fleurs dans son jardin.",
        "Si tu appuies sur la touche \"page précédente\", tu peux regarder vers le haut!",
        "Si tu aides à reprendre des bâtiments aux Cogs, tu peux gagner une étoile de bronze!",
        "Si tu appuies sur la touche de tabulation, tu peux voir différents points de vue de ce qui t'entoure!",
        "Si tu appuies sur la touche Ctrl, tu peux sauter!",
        ]

SharedChatterGoodbyes = [
        "Je dois partir maintenant, au revoir!",
        "Je crois que je vais aller faire un jeu du tramway.",
        "Eh bien, au revoir. À bientôt, %!",
        "Il vaudrait mieux que je me dépêche et que je m'occupe d'arrêter ces " + Cogs + ".",
        "C'est l'heure d'y aller.",
        "Désolé, je dois partir.",
        "Au revoir.",
        "À plus tard,%!",
        "Je crois que je vais aller m'entraîner à lancer des petits gâteaux.",
        "Je vais me joindre à un groupe et arrêter des " + Cogs + ".",
        "Je suis content(e) de t'avoir vu(e) aujourd'hui, %.",
        "J'ai beaucoup de choses à faire. Je ferais mieux de m'y mettre.",
        ]

# Lines specific to each character.
# If a talking char is mentioned, it cant be shared among them all

MickeyChatter = (
        [ # Greetings specific to Mickey
        "Bienvenue à Toontown centre.",
        "Salut, je m'appelle " + Mickey + ". Et toi ?",
        ],
        [ # Comments
        "Dis donc, as-tu vu " + Donald + "?",
        "Je vais aller regarder le brouillard se lever sur les quais " + Donald + ".",
        "Si tu vois mon copain " + Goofy + ", dis-lui bonjour de ma part.",
        "J'ai entendu dire que " + Daisy + " a planté de nouvelles fleurs dans son jardin.",
        ],
        [ # Goodbyes
        "Je vais au pays musical voir " + Minnie + "!",
        "Aïe, je suis en retard pour mon rendez-vous avec " + Minnie +"!",
        "On dirait que c'est l'heure du dîner pour " + Pluto + ".",
        "Je crois que je vais aller nager aux quais " + Donald + ".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Bienvenue au Pays musical.",
        "Salut, je m'appelle " + Minnie + ". Et toi ?"
        ],
        [ # Comments
        "Les collines sont animées par les notes de musique!",
        # the merry no longer goes round
        #"N'oublie pas d'essayer le grand manège tourne-disques!",
        "Tu as une chouette tenue, %.",
        "Dis donc, as-tu vu " + Mickey + "?",
        "Si tu vois mon ami " + Goofy + ", dis-lui bonjour de ma part.",
        "Aïe, il y a beaucoup de " + Cogs + " près du Pays des rêves de " + Donald + ".",
        "J'ai entendu dire qu'il y a du brouillard sur les quais " + Donald + ".",
        "N'oublie pas d'essayer le labyrinthe dans le jardin de " + Daisy + ".",
        "Je crois bien que je vais aller chercher quelques airs de musique.",
        "Hé %, regarde donc par là-bas.",
        "J'aime bien entendre de la musique.",
        "Je parie que tu ne savais pas que le Pays musical de Minnie est aussi appelé le Haut-Bois? Hi hi!",
        "J'aime bien jouer aux imitations. Et toi ?",
        "J'aime bien faire rire les gens.",
        "Oh là là, ça fait mal aux pieds de trotter toute la journée avec des talons!",
        "Belle chemise, %.",
        "Est-ce que c'est un bonbon par terre ?",
        ],
        [ # Goodbyes
        "Aïe, je suis en retard pour mon rendez-vous avec " + Mickey + "!",
        "On dirait que c'est l'heure du dîner pour " + Pluto + ".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

DaisyChatter = (
        [ # Greetings
        "Bienvenue dans mon jardin!",
        "Bonjour, je m'appelle"+Daisy+". Comment t'appelles-tu?",
        "Ravi de faire ta connaissance, %!",
        ],
        [ # Comments
        "Ma fleur qui a gagné le prix est au milieu du labyrinthe.",
        "J'adore me promener dans le labyrinthe.",
        "Je n'ai pas vu"+Goofy+" de la journée.",
        "Je me demande où"+Goofy+" se trouve.",
        "As-tu vu"+Donald+"?Il est introuvable.",
        "Si tu vois mon ami"+Minnie+", dis-lui \"Bonjour\" de ma part.",
        "Meilleurs sont tes outils de jardinage, et plus belles seront tes plantes.",
        "Il y a beaucoup trop de"+Cogs+" par ici"+lDonaldsDock+".",
        "Tu feras le bonheur de tes plantes si tu les arroses tous les jours.",
        "Pour faire pousser une pâquerette rose, plante un bonbon jaune et un bonbon rouge ensemble.",
        "C'est facile de faire pousser une pâquerette jaune, tu n'as qu'à planter un bonbon jaune.",
        "Si tu vois du sable sous une plante, c'est qu'elle a besoin d'eau - faute de quoi elle va se faner!"
        ],
        [ # Goodbyes
        "Je vais au Pays musical pour voir %s!" % Minnie,
        "Je suis en retard pour mon pique-nique avec %s!" % Donald,
        "Je crois que je vais aller nager à"+lDonaldsDock+".",
        "Oh, je commence à avoir sommeil. Je crois que je vais aller au Pays des Rêves",
        ]
    )

ChipChatter = (
        [ # Greetings
        "Bienvenue dans %s !" % lOutdoorZone,
        "Bonjour, je m'appelle" + Chip + ". Et toi, comment t'appelles-tu ?",
        "Non, je suis" + Chip + ".",
        "Je suis content de te voir % !",
        "Nous sommes Tic et Tac !",
        ],
        [ # Comments
        "J'aime le golf.",
        "Nous avons les meilleurs glands de Toontown.",
        "Les trous de golf dotés de volcans sont les plus difficiles pour moi.",
        ],
        [ # Goodbyes
        "Nous allons dans le" + lTheBrrrgh +"pour jouer avec %s." % Pluto,
        "Nous rendrons visite à %s et pourrons le réparer." % Donald,
        "Je crois que je vais aller me baigner dans" + lDonaldsDock + ".",
        "Oh, j'ai un peu sommeil. Je pense que je vais aller au Pays des Rêves.",
        ]
    )

# Warning Dale's chatter is dependent on on Chip's, they should match up
DaleChatter = (
        [ # Greetings
        "Je suis content de te voir % !",
        "Bonjour, je m'appelle" + Dale + ". Et toi, comment t'appelles-tu ?",
        "Salut, je suis" + Chip + ".",
        "Bienvenue dans %s !" % lOutdoorZone,
        "Nous sommes Tic et Tac !",
        ],
        [ # Comments
        "J'aime les pique-niques.",
        "Les glands sont délicieux. Goûte.",
        "Ces moulins à vent sont difficiles aussi.",
        ],
        [ # Goodbyes
        "Hihihi" + Pluto + "est un compagnon de jeu amusant.",
        "D'accord, réparons %s." % Donald,
        "Une baignade. Quelle idée rafraîchissante&nbsp;!",
        "Je suis de plus en plus fatigué et ferais bien une petite sieste.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Bienvenue au jardin de " + Daisy + ".",
        "Salut, je m'appelle " + Goofy + ". Et toi ?",
        "Wof, je suis content de te voir, %!",
        ],
        [ # Comments
        "Bon sang, c'est facile de se perdre dans le labyrinthe!",
        "N'oublie pas d'essayer le labyrinthe tant que tu es ici.",
        "Je n'ai pas vu " + Daisy + " de la journée.",
        "Je me demande où se trouve " + Daisy + ".",
        "Dis donc, as-tu vu " + Donald + "?",
        "Si tu vois mon ami " + Mickey + ", dis-lui bonjour de ma part.",
        "Oh! J'ai oublié le petit déjeuner de " + Mickey + "!",
        "Wof, il y a beaucoup de " + Cogs + " près des quais " + Donald + ".",
        "On dirait que " + Daisy + " a planté de nouvelles fleurs dans son jardin.",
        "À la succursale du Glagla de ma boutique à gags, les lunettes hypnotiques sont en vente pour seulement 1 bonbon!",
        "La boutique à gags de Dingo propose les meilleurs blagues, astuces et chatouilles de tout Toontown!",
        "À la boutique à gags de Dingo, chaque tarte à la crème est garantie faire rire ou tes bonbons te seront remboursés!"
        ],
        [ # Goodbyes
        "Je vais au Pays musical voir " + Minnie + "!",
        "Aïe, je suis en retard pour mon rendez-vous avec " + Donald + "!",
        "Je crois que je vais aller nager aux quais " + Donald + ".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

GoofySpeedwayChatter = (
        [ # Greetings
        "Bienvenue au "+lGoofySpeedway+".",
        "Salut, je m'appelle "+Goofy+". Et toi ?",
        "Ouah, sympa de te voir %!",
        ],
        [ # Comments
        "Bon sang, j'ai vu une super course tout à l'heure.",
        "Attention aux peaux de banane sur la piste!",
        "Est-ce que tu as fait des améliorations sur ton kart récemment ?",
        "Nous venons d'acheter de nouvelles jantes dans le magasin de karts.",
        "Dis-donc, tu as vu "+Donald+"?",
        "Si tu vois mon ami "+Mickey+", dis-lui bonjour de ma part.",
        "Oh! J'ai oublié de préparer le petit déjeuner de "+Mickey+"!",
        "Bon sang, c'est vrai qu'il y a un tas de "+Cogs+" sur les "+lDonaldsDock+".",
        "À la succursale du Glagla de ma boutique à gags, les lunettes hypnotiques sont en vente pour seulement 1 bonbon!",
        "La boutique à gags de Dingo propose les meilleurs blagues, astuces et chatouilles de tout Toontown!",
        "À la boutique à gags de Dingo, chaque tarte à la crème est garantie de te faire rire ou tes bonbons te seront remboursés !"
        ],
        [ # Goodbyes
        "Je vais au Pays Musical pour voir %s!" % Mickey,
        "Aïe, je suis en retard pour mon rendez-vous avec %s!" % Donald,
        "Je crois que je vais aller nager aux "+lDonaldsDock+".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Bienvenue au Pays des rêves.",
        "Salut, je m'appelle " + Donald + ". Et toi ?"
        ],
        [ # Comments
        "Cet endroit me donne quelquefois la chair de poule.",
        "N'oublie pas d'essayer le labyrinthe dans le jardin de" + Daisy + ".",
        "Oh, bon sang! Quelle bonne journée.",
        "Dis donc, as-tu vu" + Mickey + "?",
        "Si tu vois mon copain" + Goofy + ", dis-lui bonjour de ma part."
        "Je crois bien que je vais aller à la pêche cet après-midi.",
        "Aïe, il y a beaucoup de " + Cogs + " près des quais " + Donald + ".",
        "Hé dis donc, tu n'as pas encore fait un tour de bateau avec moi aux quais " + Donald + "?"
        "Je n'ai pas vu " + Daisy + " de la journée.",
        "J'ai entendu dire que " + Daisy + " a planté de nouvelles fleurs dans son jardin."
        "Coin coin.",
        ],
        [ # Goodbyes
        "Je vais au Pays musical voir " + Minnie + "!",
        "Aïe, je suis en retard pour mon rendez-vous avec " + Daisy + "!",
        "Je crois que je vais aller nager près de mes quais.",
        "Je crois que je vais aller faire un tour de bateau près de mes quais.",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)

# FriendsListPanel.py
FriendsListPanelNewFriend = "Nouvel(le) ami(e)"
FriendsListPanelSecrets = "Secrets"
FriendsListPanelOnlineFriends = "CONTACTS\nEN LIGNE"
FriendsListPanelAllFriends = "TOUS\nLES CONTACTS"
FriendsListPanelIgnoredFriends = "TOONS\nIGNORÉS"
FriendsListPanelPets = "ANIMAUX FAMILIERS\nA PROXIMITÉ"
FriendsListPanelPlayers = "TOUS LES AMIS\nDU JOUEUR"
FriendsListPanelOnlinePlayers = "AMIS DU JOUEUR\nEN LIGNE"

FriendInviterClickToon = "Clique sur le Toon avec lequel tu souhaites devenir ami.\n\n(Tu as %s amis)"

# Support DISL account friends
FriendInviterToon = "Toon"
FriendInviterThatToon = "Ce Toon"
FriendInviterPlayer = "Joueur"
FriendInviterThatPlayer = "Ce joueur"
FriendInviterBegin = "Quel genre d'ami aimerais-tu te faire ?"
FriendInviterToonFriendInfo = "Un ami seulement dans Toontown"
FriendInviterPlayerFriendInfo = "Un ami à travers le réseau Disney.com"
FriendInviterToonTooMany = "Tu as trop d'amis Toon pour pouvoir en ajouter un nouveau. Tu devras supprimer des amis Toon si tu veux devenir ami avec %s. Tu pourrais aussi essayer de t'en faire un ami de jeu."
FriendInviterPlayerTooMany = "Tu as trop d'amis de jeu pour pouvoir en ajouter un nouveau. Tu devras supprimer des amis de jeu si tu veux devenir ami avec %s. Tu pourrais aussi essayer de t'en faire un ami Toon."
FriendInviterToonAlready = "%s est déjà ton ami Toon."
FriendInviterPlayerAlready = "%s est déjà ton ami de jeu."
FriendInviterStopBeingToonFriends = "Cesser d'être ami Toon"
FriendInviterStopBeingPlayerFriends = "Cesser d'être ami de jeu"
FriendInviterEndFriendshipToon = "Es-tu sûr de vouloir cesser d'être ami Toon avec %s ?"
FriendInviterEndFriendshipPlayer = "Es-tu sûr de vouloir cesser d'être ami de jeu avec %s ?"
FriendInviterRemainToon = "\n(Tu resteras néanmoins ami Toon avec %s)"
FriendInviterRemainPlayer = "\n(Tu resteras néanmoins ami de jeu avec %s)"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Désolé, tu ne peux pas avancer parce que le téléchargement de %(phase)s n'en est qu'à %(percent)s% %.\n\nRéessaie plus tard."

# TeaserPanel.py
TeaserTop = "Désolé! Tu n'as pas accès à ceci pendant l'essai gratuit.\n\nInscris-toi maintenant et profite de ces super fonctionnalités :"
TeaserBottom = "Subscribe now and enjoy these great features:"
TeaserOtherHoods = "Visite les 6 quartiers exceptionnels!"
TeaserTypeAName = "Inscris le nom que tu préfères pour ton Toon!"
TeaserSixToons = "Crée jusqu'à 6 Toons par compte!"
TeaserOtherGags = "Additionne 6 niveaux d'habileté\ndans 6 séries de gags différentes!"
TeaserClothing = "Achète des vêtements originaux\npour personnaliser ton Toon!"
TeaserFurniture = "Achète et dispose des meubles dans ta maison!"
TeaserCogHQ = "Infiltre des zones dangereuses sur\nle territoire des Cogs!"
TeaserSecretChat = "Échange des secrets avec tes contacts\npour pouvoir discuter en ligne avec eux!"
TeaserCardsAndPosters = "Participe aux concours et compétitions gagne des trophées et \naugmente ta reserve des rigolpoints! \nTon nom apparaîtra sur www.toontown.fr"
TeaserHolidays = "Participe à des événements spéciaux et\npassionnants et à des fêtes!"
TeaserQuests = "Relève des centaines de défitoons pour sauver Toontown!"
TeaserEmotions = "Achète des émotions pour rendre ton\nToon plus expressif!"
TeaserMinigames = "Joue aux 8 sortes de mini jeux!"
TeaserKarting = "Fais la course contre d'autres Toons dans de super karts!"
TeaserKartingAccessories = " Personnaliseton kart avec des accessoiressuper cool."
TeaserTricks = " Entraîne ton Doudouà faire des tourspour\nqu'il t'aide dans les combats !"
TeaserGardening = "Plante des fleurs, des statues et des arbres à gags pour embellir\n ta propriété."
TeaserRental = "Loue des articles de fête amusants pour ta propriété !"
TeaserBigger = "Achète des articles Toon meilleurs et plus gros !"
TeaserTricks = "Entraîne ton Doudou à faire des tours pour t'aider dans le combat !"
TeaserSpecies = "Crée des Toons singe, cheval et ours, et joue avec !"
TeaserFishing = "Collectionne toutes les espèces de poissons !"
TeaserGolf = "Joue sur des terrains de golf complètement dingues !"
TeaserSubscribe = "S'inscrire maintenant"
TeaserContinue = "Continuer l'essai"

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "Téléchargement de: %s"
DownloadWatcherInitializing = "Initialisation du téléchargement..."

# Launcher.py
LauncherPhaseNames = {
    0   : "Initialisation",
    1   : "Panda",
    2   : "Moteur",
    3   : "Faire un Toon",
    3.5 : "Toontoriel",
    4   : "Terrain de jeux",
    5   : "Rues",
    5.5 : "Domaines",
    6   : "Quartiers I",
    7   : "Bâtiments" + Cog,
    8   : "Quartiers II",
    9   : "QG Vendibot",
    10  : "QG Caissbot",
    11  : lLawbotHQ,
    12  : Bossbot + " HQ",
    13  : "Parties",
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)s (%(current)s sur %(total)s)"
LauncherStartingMessage = "Lancement de Toontown en ligne de Disney..."
LauncherDownloadFile = "Téléchargement des mises à jour:" + LauncherProgress + "..."
LauncherDownloadFileBytes = "Téléchargement des mises à jour:" + LauncherProgress + " : %(bytes)s"
LauncherDownloadFilePercent = "Téléchargement des mises à jour:" + LauncherProgress + " : %(percent)s% %"
LauncherDecompressingFile = "Décompression des mises à jour:" + LauncherProgress + "..."
LauncherDecompressingPercent = "Décompression des mises à jour:" + LauncherProgress + ". : %(percent)s% %"
LauncherExtractingFile = "Extraction des mises à jour:" + LauncherProgress + "..."
LauncherExtractingPercent = "Extraction des mises à jour:" + LauncherProgress + " : %(percent)s% %"
LauncherPatchingFile = "Application des mises à jour:" + LauncherProgress + "..."
LauncherPatchingPercent = "Application des mises à jour:" + LauncherProgress + " : %(percent)s% %"
LauncherConnectProxyAttempt = "En cours de connexion à Toontown: %s (proxy : %s) essai : %s"
LauncherConnectAttempt = "En cours de connexion à Toontown: %s essai %s"
LauncherDownloadServerFileList = "Mise à jour de Toontown..."
LauncherCreatingDownloadDb = "Mise à jour de Toontown..."
LauncherDownloadClientFileList = "Mise à jour de Toontown..."
LauncherFinishedDownloadDb = "Mise à jour de Toontown..."
LauncherStartingToontown = "Lancement de Toontown..."
LauncherStartingGame = "Lancement de Toontown..."
LauncherRecoverFiles = "Mise à jour de Toontown. Récupération des fichiers..."
LauncherCheckUpdates = "Recherche de mises à jour pour "+ LauncherProgress
LauncherVerifyPhase = "Mise à jour de Toontown..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Faire un\nToon"
AvatarChoicePlayThisToon = "Jouer\navec ce Toon"
AvatarChoiceSubscribersOnly = "S'inscrire\n\n\n\nMaintenant!"
AvatarChoiceDelete = "Supprimer"
AvatarChoiceDeleteConfirm = "Cela va supprimer %s pour toujours."
AvatarChoiceNameRejected = "Nom\nrefusé"
AvatarChoiceNameApproved = "Nom\naccordé!"
AvatarChoiceNameReview = "En cours\nd'examen"
AvatarChoiceNameYourToon = "Donne un nom\nà ton Toon!"
AvatarChoiceDeletePasswordText = "Attention! Cela va supprimer %s pour toujours. Pour supprimer ce Toon, entre ton mot de passe."
AvatarChoiceDeleteConfirmText = "Attention! Cela va supprimer %(name)s pour toujours. Si tu es certain(e) de vouloir faire cela, entre \"%(confirm)s\" et clique sur OK."
AvatarChoiceDeleteConfirmUserTypes = "supprimer"
AvatarChoiceDeletePasswordTitle = "Supprimer le Toon ?"
AvatarChoicePassword = "Mot de passe"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "Ce mot de passe ne semble pas correspondre. Pour supprimer ce Toon, entre ton mot de passe."
AvatarChoiceDeleteWrongConfirm = "Tu n'as pas entré le bon mot. Pour supprimer %(name)s, entre \"%(confirm)s\" et clique sur OK. N'entre pas les guillemets. Clique sur Annuler si tu as changé d'avis."

# AvatarChooser.py
AvatarChooserPickAToon = "Choisis un Toon pour jouer"
AvatarChooserQuit = lQuit

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Appelez le Service clients au %s. "
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nSi vous avez besoin d'aide, vous pouvez appeler le service clients au %s."
TTAccountIntractibleError = "Une erreur s'est produite."

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                          'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc',]
DateOfBirthEntryDefaultLabel = "Date de naissance"


# AchievePage.py
AchievePageTitle = "Réussites\n (Bientôt disponible)"

# PhotoPage.py
PhotoPageTitle = "Photo\n (Bientôt disponible)"

# BuildingPage.py
BuildingPageTitle = "Bâtiments\n (Bientôt disponible)"

# InventoryPage.py
InventoryPageTitle = "Gags"
InventoryPageDeleteTitle = "SUPPRIMER LES GAGS"
InventoryPageTrackFull = "Tu as tous les gags de la série %s."
InventoryPagePluralPoints = "Tu auras un nouveau gag de la série \n%(trackName)s lorsque tu\nauras %(numPoints)s points de %(trackName)s en plus."
InventoryPageSinglePoint = "Tu auras un nouveau gag de la série \n%(trackName)s lorsque tu\nauras %(numPoints)s points de %(trackName)s en plus."
InventoryPageNoAccess = "Tu n'as pas encore accès à la série %s."

# NPCFriendPage.py
NPCFriendPageTitle = "Toons SOS"

# NPCFriendPanel.py
NPCFriendPanelRemaining = "Restant %s"
# PartiesPage.py
PartiesPageTitle = "Fêtes"
PartiesPageHostTab = "Organiser"
PartiesPageInvitedTab = "Invitations"
PartiesPageTitleHost = "Ma prochaine fête"
PartiesPageTitleInvited = "Invitations pour la fête"

# MapPage.py
MapPageTitle = "Carte"
MapPageBackToPlayground = "au terrain de jeux"
MapPageBackToCogHQ = "Retour au QG des Cogs"
MapPageGoHome = "à la maison"
# hood name, street name
MapPageYouAreHere = "Tu es à: %s\n%s"
MapPageYouAreAtHome = "Tu es dans\nta propriété."
MapPageYouAreAtSomeonesHome = "Tu es chez %s."
MapPageGoTo = "Aller chez\n%s."

# OptionsPage.py
OptionsPageTitle = "Options"
OptionsPagePurchase = "S'inscrire!"
OptionsPageLogout = "Se déconnecter"
OptionsPageExitToontown = "Quitter Toontown"
OptionsPageMusicOnLabel = "Musique activée."
OptionsPageMusicOffLabel = "Musique désactivée."
OptionsPageSFXOnLabel = "Effets sonores activés."
OptionsPageSFXOffLabel = "Effets sonores désactivés."
OptionsPageFriendsEnabledLabel = "Demandes de nouveaux contacts acceptées."
OptionsPageFriendsDisabledLabel = "Demandes de nouveaux contacts non acceptées."
OptionsPageSpeedChatStyleLabel = "Couleur du Chat rapide"
OptionsPageDisplayWindowed = "dans une fenêtre"
OptionsPageSelect = "Choisir"
OptionsPageToggleOn = "Activer"
OptionsPageToggleOff = "Désactiver"
OptionsPageChange = "Modifier"
OptionsPageDisplaySettings = "Affichage: %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Affichage: %(screensize)s"
OptionsPageExitConfirm = "Quitter Toontown ?"

DisplaySettingsTitle = "Réglages d'affichage"
DisplaySettingsIntro = "Les réglages suivants sont utilisés pour configurer l'affichage de Toontown sur votre ordinateur. Il n'est sans doute pas indispensable de les modifier sauf si vous avez un problème."
DisplaySettingsIntroSimple = "Vous pouvez accroître la résolution d'écran pour améliorer la lisibilité du texte et des graphiques de Toontown, mais en fonction de votre carte graphique, certaines valeurs plus élevées risquent d'affecter le bon fonctionnement du jeu, voire de l'empêcher complètement de fonctionner."

DisplaySettingsApi = "Interface graphique:"
DisplaySettingsResolution = "Résolution:"
DisplaySettingsWindowed = "Dans une fenêtre"
DisplaySettingsFullscreen = "Plein écran"
DisplaySettingsApply = "Appliquer"
DisplaySettingsCancel = lCancel
DisplaySettingsApplyWarning = "Lorsque vous cliquez sur OK, les réglages d'affichage sont modifiés. Si la nouvelle configuration ne s'affiche pas correctement sur votre ordinateur, l'affichage revient automatiquement à sa configuration d'origine après %s secondes."
DisplaySettingsAccept = "Cliquez sur OK pour conserver les nouveaux réglages ou sur Annuler pour revenir aux valeurs précédentes. Si vous ne cliquez sur rien, les réglages reviennent automatiquement aux valeurs précédentes après %s secondes."
DisplaySettingsRevertUser = "Vos précédents réglages d'affichage ont été restaurés."
DisplaySettingsRevertFailed = "Les réglages d'affichage sélectionnés ne peuvent pas fonctionner sur votre ordinateur. Vos précédents réglages d'affichage ont été restaurés."

# TrackPage.py
TrackPageTitle = "Entraînement à une série de gags"
TrackPageShortTitle = "Entraînement\naux gags"
TrackPageSubtitle = "Termine des défitoons pour apprendre à utiliser de nouveaux gags!"
TrackPageTraining = "Tu t'entraînes pour utiliser les gags %s. \nLorsque tu auras terminé les 16 défis, tu\npourras utiliser les gags %s lors des combats."
TrackPageClear = "Tu ne t'entraînes pour aucune série de gags actuellement."
TrackPageFilmTitle = "Entraînement\naux gags %s\n."
TrackPageDone = "FIN"

# QuestPage.py
QuestPageToonTasks = "Défitoons"
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
QuestPageChoose = "Choisis"
QuestPageLocked = "Locked"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = lHQOfficerM
QuestPosterHQBuildingName = lToonHQ
QuestPosterHQStreetName = "Une rue"
QuestPosterHQLocationName = "Un quartier"

QuestPosterTailor = "Tailleur"
QuestPosterTailorBuildingName = "Boutique de prêt-à-porter"
QuestPosterTailorStreetName = "Un terrain de jeux"
QuestPosterTailorLocationName = "Un quartier"
QuestPosterPlayground = "Sur le terrain de jeux"
QuestPosterAtHome = "Chez toi"
QuestPosterInHome = "Dans ta maison"
QuestPosterOnPhone = "Sur ton téléphone"
QuestPosterEstate = "Dans ta propriété"
QuestPosterAnywhere = "N'importe où"
QuestPosterAuxTo = "à:"
QuestPosterAuxFrom = "depuis:"
QuestPosterAuxFor = "pour:"
QuestPosterAuxOr = "ou:"
QuestPosterAuxReturnTo = "Retourner à:"
QuestPosterLocationIn = " à"
QuestPosterLocationOn = " à"
QuestPosterFun = "Juste pour s'amuser!"
QuestPosterFishing = "ALLER PÊCHER"
QuestPosterComplete = "TERMINÉ"

# ShardPage.py
ShardPageTitle = "Districts"
ShardPageHelpIntro = "Chaque district est une copie du monde de Toontown."
ShardPageHelpWhere = " Tu es actuellement dans le district de \"%s\"."
ShardPageHelpWelcomeValley = " Tu es actuellement dans le district de la \"Vallée de la Bienvenue\", dans \"%s\"."
ShardPageHelpMove = " Pour aller dans un nouveau district, clique sur son nom."

ShardPagePopulationTotal = "Population totale de Toontown:\n%d"
ShardPageScrollTitle = "Nom Population"
ShardPageLow = "Calme"
ShardPageMed = "Idéal"
ShardPageHigh = "Complet"
ShardPageChoiceReject = "Désolé, ce district est complet. Merci d'en essayer un autre."

# SuitPage.py
SuitPageTitle = "Galerie des Cogs"
SuitPageMystery = "???"
SuitPageQuota = "%s sur %s"
SuitPageCogRadar = "%s présents"
SuitPageBuildingRadarS = "Bâtiment %s"
SuitPageBuildingRadarP = "Bâtiments %s"

# DisguisePage.py
DisguisePageTitle = "Déguisement de\n" + Cog
DisguisePageMeritBar = "Avancement au mérite"
DisguisePageMeritAlert = "Prêt pour la\npromotion!"
DisguisePageCogLevel = "Niveau %s"
DisguisePageMeritFull = "Plein"
DisguisePageMeritBar = "Avancement au mérite"
DisguisePageCogPartRatio = "%d/%d"

# FishPage.py
FishPageTitle = "Pêche"
FishPageTitleTank = "Seau de pêche"
FishPageTitleCollection = "Album de pêche"
FishPageTitleTrophy = "Trophées de pêche"
FishPageWeightStr = "Poids:"
FishPageWeightLargeS = "%dkg"
FishPageWeightLargeP = "%dkg"
FishPageWeightSmallS = " %dg"
FishPageWeightSmallP = " %dg"
FishPageWeightConversion = 16
FishPageValueS = "Valeur: %d bonbon"
FishPageValueP = "Valeur: %d bonbons"
FishPageTotalValue = ""
FishPageCollectedTotal = "Espèces de poissons pêchées: %d sur %d"
FishPageRodInfo = "Canne %s \n%d - %d livres"
FishPageTankTab = "Seau"
FishPageCollectionTab = "Album"
FishPageTrophyTab = "Trophées"

FishPickerTotalValue = "Seau: %s / %s\nValeur: %d bonbons"

UnknownFish = "???"

FishingRod = "Canne %s"
FishingRodNameDict = {
    0 : "Brindille",
    1 : "Bambou",
    2 : "Bois dur",
    3 : "Acier",
    4 : "Or",
    }
FishTrophyNameDict = {
    0 : "Guppy",
    1 : "Vairon",
    2 : "Poisson",
    3 : "Poisson volant",
    4 : "Requin",
    5 : "Espadons",
    6 : "Épaulard",
    }

# GardenPage.py
GardenPageTitle = "Gardening"
GardenPageTitleBasket = "Panier de fleurs"
GardenPageTitleCollection = "Album de fleurs"
GardenPageTitleTrophy = "Trophées de jardinage"
GardenPageTitleSpecials = "Offres spéciales jardinage"
GardenPageBasketTab = "Panier"
GardenPageCollectionTab = "Album"
GardenPageTrophyTab = "Trophées"
GardenPageSpecialsTab = "Offres spéciales"
GardenPageCollectedTotal = "Variétés de fleurs rassemblées: %d sur %d"
GardenPageValueS = "Valeur: %d bonbon"
GardenPageValueP = "Valeur: %d bonbons"
FlowerPickerTotalValue = "Panier: %s / %s\nValeur: %d bonbons"
GardenPageShovelInfo = "%s Pelle: %d / %d\n"
GardenPageWateringCanInfo = "%s Arrosoir: %d / %d"

# KartPage.py
KartPageTitle = "Karts"
KartPageTitleCustomize = "Customiser mon kart"
KartPageTitleRecords = "Meilleurs records personnels"
KartPageTitleTrophy = "Trophées de course"
KartPageCustomizeTab = "Customiser"
KartPageRecordsTab = "Records"
KartPageTrophyTab = "Trophée"
KartPageTrophyDetail = "Trophée %s : %s"
KartPageTickets = "Tickets:"
KartPageConfirmDelete = "Supprimer l'accessoire ?"

#plural
KartShtikerDelete = "Supprimer"
KartShtikerSelect = "Choisir une catégorie"
KartShtikerNoAccessories = "Aucun accessoire acheté"
KartShtikerBodyColors = "Couleurs du kart"
KartShtikerAccColors = "Couleurs des accessoires"
KartShtikerEngineBlocks = "Accessoires du capot"
KartShtikerSpoilers = "Accessoires du coffre"
KartShtikerFrontWheelWells = "Accessoires des roues avant"
KartShtikerBackWheelWells = "Accessoires des roues arrière"
KartShtikerRims = "Accessoires des jantes"
KartShtikerDecals = "Accessoires décalcomanie"
#singluar
KartShtikerBodyColor = "Couleur du kart"
KartShtikerAccColor = "Couleur de l'accessoire"
KartShtikerEngineBlock = "Capot"
KartShtikerSpoiler = "Coffre"
KartShtikerFrontWheelWell = "Roue avant"
KartShtikerBackWheelWell = "Roue arrière"
KartShtikerRim = "Jante"
KartShtikerDecal = "Décalcomanie"

KartShtikerDefault = "%s par défaut"
KartShtikerNo = "Aucun accessoire de %s"

# QuestChoiceGui.py
QuestChoiceGuiCancel = lCancel

# TrackChoiceGui.py
TrackChoiceGuiChoose = "Choisir"
TrackChoiceGuiCancel = lCancel
TrackChoiceGuiHEAL = "Toonique te permet de soigner les autres Toons lors d'une bataille."
TrackChoiceGuiTRAP = "Les pièges sont des gags puissants qui doivent être utilisés avec les leurres."
TrackChoiceGuiLURE = "Utilise les leurres pour assommer les Cogs ou les attirer dans des pièges."
TrackChoiceGuiSOUND = "Les gags de tapage affectent tous les Cogs mais ne sont pas très puissants."
TrackChoiceGuiDROP = "Les gags de chute font beaucoup de dégâts mais ne sont pas très précis."

# EmotePage.py
EmotePageTitle = "Expressions / Émotions"
EmotePageDance = "Tu as construit la séquence de danse suivante:"
EmoteJump = "Saut"
EmoteDance = "Danse"
EmoteHappy = "Content(e)"
EmoteSad = "Triste"
EmoteAnnoyed = "Agacement"
EmoteSleep = "Sommeil"

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nNiveau %(level)s"

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "Tu ne peux pas quitter le terrain de jeux tant que ton rigolmètre ne sourit pas!"

# InventoryNew.py
InventoryTotalGags = "Total des gags\n%d / %d"
InventroyPinkSlips = "%s Avis de licenciement"
InventroyPinkSlip = "1 Avis de licenciement"
InventoryDelete = "SUPPRIMER"
InventoryDone = "TERMINÉ"
InventoryDeleteHelp = "Clique sur un gag pour le SUPPRIMER."
InventorySkillCredit = "Crédit d'habileté: %s"
InventorySkillCreditNone = "Crédit d'habileté: Aucun"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Précision : %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryUberTrackExp = "%(nextExp)s à terminer !"
InventoryGuestExp = "Nombre maxi d'invités"
GuestLostExp = "Plus que le nombre maxi d'invités"
InventoryAffectsOneCog = "Affecte : Un"+ Cog
InventoryAffectsOneToon = "Affecte : Un Toon"
InventoryAffectsAllToons = "Affecte : tous les Toons"
InventoryAffectsAllCogs = "Affecte : tous les"+ Cogs
InventoryHealString = "Toonique"
InventoryDamageString = "Dommages"
InventoryBattleMenu = "MENU DU COMBAT"
InventoryRun = "COURIR"
InventorySOS = "SOS"
InventoryPass = "PASSER"
InventoryFire = "FIRE"
InventoryClickToAttack = "Clique sur\nun gag pour\nattaquer."
InventoryDamageBonus = "(+%d)"

# NPCForceAcknowledge.py
NPCForceAcknowledgeMessage = "Tu dois faire un tour de tramway avant de partir.\n\n\n\n\n\n\nTu trouveras le tramway près de la boutique à gags de Dingo."
NPCForceAcknowledgeMessage2 = "Bien, tu as terminé ta recherche dans le tramway!\nVa voir le quartier général des Toons pour recevoir ta récompense.\n\n\n\n\n\n\n\nLe quartier général des Toons est situé près du centre du terrain de jeux."
NPCForceAcknowledgeMessage3 = "N'oublie pas de faire un tour de tramway.\n\n\n\n\n\nTu trouveras le tramway près de la boutique à gags de Dingo."
NPCForceAcknowledgeMessage4 = "Bravo! Tu as terminé ton premier défitoon!\n\n\n\n\n\n\nVa voir le quartier général des Toons pour recevoir ta récompense."
NPCForceAcknowledgeMessage5 = "N'oublie pas ton défitoon!\n\n\n\n\n\n\n\n\n\n\nTu peux trouver des Cogs a vaincre de l'autre côté de tunnels comme celui-ci."
NPCForceAcknowledgeMessage6 = "Félicitations pour avoir vaincu ces Cogs!\n\n\n\n\n\n\n\n\n\nReviens au quartier général des Toons aussi vite que possible."
NPCForceAcknowledgeMessage7 = "N'oublie pas de te faire un(e) ami(e)!\n\n\n\n\n\n\n\nClique sur un autre joueur et utilise le bouton Nouvel(le) ami(e)."
NPCForceAcknowledgeMessage8 = "Super! Tu t'es fait un(e) nouvel(le) ami(e)!\n\n\n\n\n\n\n\n\nTu dois retourner au quartier général des Toons maintenant."
NPCForceAcknowledgeMessage9 = "Tu as bien utilisé le téléphone!\n\n\n\n\n\n\n\n\nRetourne au quartier général des Toons pour demander ta récompense."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "Tu as reçu 1 point de lancer! Quand tu en auras 10, tu pourras recevoir un nouveau gag!"
MovieTutorialReward2 = "Tu as reçu 1 point d'éclaboussure! Quand tu en auras 10, tu pourras avoir un nouveau gag!"
MovieTutorialReward3 = "Bon travail! Tu as terminé ton premier défitoon!"
MovieTutorialReward4 = "Va chercher ta récompense au quartier général des Toons!"
MovieTutorialReward5 = "Amuse-toi!"

# BattleBase.py
Battle_Input_Timeout = 50.0

# ToontownBattleGlobals.py
BattleGlobalTracks = ['toonique', 'piège', 'leurre', 'tapage', 'lancer', 'éclaboussure', 'chute']
BattleGlobalNPCTracks = ['rechargement', 'Toons marquent', 'Cogs ratent']
BattleGlobalAvPropStrings = (
    ('Plume', 'Mégaphone', 'Tube de rouge à lèvres', 'Canne en bambou', 'Poussière de fée', 'Balles de jonglage', 'Plongeon'),
    ('Peau de banane', 'Râteau', 'Billes', 'Sable mouvant', 'Trappe', 'TNT', 'Chemin de fer'),
    ('Billet de 1 euro', 'Petit aimant', 'Billet de 5 euros', 'Gros aimant', 'Billet de 10 euros', 'Lunettes hypnotiques', 'Présentation'),
    ('Sonnette de vélo', 'Sifflet', 'Clairon', 'Klaxon', "Trompe d'éléphant", 'Corne de brume', 'Chanteuse d’opéra'),
    ('Petit gâteau', 'Tranche de tarte aux fruits', 'Tranche de tarte à la crème', 'Tarte aux fruits entière', 'Tarte à la crème entière', "Gâteau d'anniversaire", 'Gâteau de mariage'),
    ('Fleur à éclabousser', "Verre d'eau", 'Pistolet à eau', "Bouteille d'eau gazeuse", "Lance d'incendie", "Nuage d'orage", 'Geyser'),
    ('Pot de fleurs', 'Sac de sable', 'Enclume', 'Gros poids', 'Coffre-fort', 'Piano à queue', 'Toontanic')
    )
BattleGlobalAvPropStringsSingular = (
    ('une plume', 'un mégaphone', 'un tube de rouge à lèvres', 'une canne en bambou', 'de la poussière de fée', 'un jeu de balles de jonglage', 'un Plongeon'),
    ('une peau de banane', 'un râteau', 'un jeu de billes', 'un peu de sable mouvant', 'une trappe', 'du TNT', 'un Chemin de fer'),
    ('un billet de 1 euro', 'un petit aimant', 'un billet de 5 euros', 'un gros aimant', 'un billet de 10 euros', 'une paire de lunettes hypnotiques', 'une Présentation'),
    ('une sonnette de vélo', 'un sifflet', 'un clairon', 'un klaxon', "une trompe d'éléphant", 'une corne de brume', 'une Chanteuse d’opéra'),
    ('un petit gâteau', 'une tranche de tarte aux fruits', 'une tranche de tarte à la crème', 'une tarte aux fruits entière', 'une tarte à la crème entière', "un gâteau d'anniversaire", 'un Gâteau de mariage'),
    ('une fleur à éclabousser', "un verre d'eau", 'un pistolet à eau', "une bouteille d'eau gazeuse", "une lance d'incendie", "un nuage d'orage", 'un Geyser'),
    ('un pot de fleurs', 'un sac de sable', 'une enclume', 'un gros poids', 'un coffre-fort', 'un piano à queue', 'le Toontanic')
    )
BattleGlobalAvPropStringsPlural = (
    ('Plumes', 'Mégaphones', 'Tubes de rouge à lèvres', 'Cannes en bambou', 'Poussières de fée', 'jeux de balles de jonglage', 'Plongeons'),
    ('Peaux de bananes', 'Râteaux', 'jeux de billes', 'morceaux de sable mouvant', 'Trappes','bâtons de TNT', 'Chemins de fer'),
    ('Billets de 1 euro', 'Petits aimants', 'Billets de 5 euros', 'Gros aimants','Billets de 10 euros', 'Paires de lunettes hypnotiques', 'Présentations'),
    ('Sonnettes de vélo', 'Sifflets', 'Clairons', 'Klaxons', "Trompes d'éléphants", 'Cornes de brume', 'Chanteuses d’opéra'),
    ('Petits gâteaux', 'Tranches de tarte aux fruits', 'Tranches de tarte à la crème','Tartes aux fruits entières', 'Tartes à la crème entières', "Gâteaux d'anniversaire", 'Gâteaux de mariage'),
    ('Fleurs à éclabousser', "Verres d'eau", 'Pistolets à eau',"Bouteilles d'eau gazeuse", "Lances d'incendie", "Nuages d'orage", 'Geysers'),
    ('Pots de fleurs', 'Sacs de sable', 'Enclumes', 'Gros poids', 'Coffres-forts','Pianos à queue', 'Paquebots')
    )
BattleGlobalAvTrackAccStrings = ("Moyenne", "Parfaite", "Faible", "Forte", "Moyenne", "Forte", "Faible")
BattleGlobalLureAccLow = "Faible"
BattleGlobalLureAccMedium = "Moyen"

AttackMissed = "RATÉ"

NPCCallButtonLabel = 'APPEL'

# ToontownLoader.py
LoaderLabel = "Chargement..."

# PlayGame.py
HeadingToHood = "En route %(to)s %(hood)s..." # hood name
HeadingToYourEstate = "En direction de ta propriété..."
HeadingToEstate = "En direction de la propriété de %s..."  # avatar name
HeadingToFriend = "En direction de la propriété de l'ami(e) de %s..."  # avatar name

# Hood.py
HeadingToPlayground = "En direction du terrain de jeux..."
HeadingToStreet = "En route %(to)s %(street)s..." # Street name

# TownBattle.py
TownBattleRun = "Revenir en courant au terrain de jeux?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "QUEL TOON ?"
TownBattleChooseAvatarCogTitle = "QUEL "+ string.upper(Cog) + "?"
TownBattleChooseAvatarBack = "RETOUR"

#firecogpanel
FireCogTitle = "PINK SLIPS LEFT:%s\nFIRE WHICH COG?"
FireCogLowTitle = "PINK SLIPS LEFT:%s\nNOT ENOUGH SLIPS !"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "Pas d'contacts à appeler!"
TownBattleSOSWhichFriend = "Appeler quel(le) ami(e)?"
TownBattleSOSNPCFriends = "Toons sauvés"
TownBattleSOSBack = "RETOUR"

# TownBattleToonPanel.py
TownBattleToonSOS = "SOS"
TownBattleToonFire = "Fire"
TownBattleUndecided = "?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "En attente des\nautres joueurs..."
TownSoloBattleWaitTitle = "Patiente..."
TownBattleWaitBack = "RETOUR"

# TownBattleSOSPetSearchPanel.py
TownBattleSOSPetSearchTitle = "Recherche du Doudou\n%s..."

# TownBattleSOSPetInfoPanel.py
TownBattleSOSPetInfoTitle = "%s est %s"
TownBattleSOSPetInfoOK = lOK

# Trolley.py
TrolleyHFAMessage = "Tu ne peux pas monter dans le tramway avant que ton rigolmètre ne sourie."
TrolleyTFAMessage = "Tu ne peux pas monter dans le tramway avant que " + Mickey + " ne te le dise."
TrolleyHopOff = lQuit

# DistributedFishingSpot.py
FishingExit = "Sortie"
FishingCast = "Lancer"
FishingAutoReel = "Moulinet automatique"
FishingItemFound = "Tu as attrapé :"
FishingCrankTooSlow = "Trop\nlent"
FishingCrankTooFast = "Trop\nrapide"
FishingFailure = "Tu n'as rien attrapé!"
FishingFailureTooSoon = "Ne commence pas à faire remonter ta ligne avant de voir une touche. Attends que ton flotteur se mette à s'enfoncer et à remonter rapidement!"
FishingFailureTooLate = "Remonte bien ta ligne avant que le poisson ne se décroche!"
FishingFailureAutoReel = "Le moulinet automatique n'a pas fonctionné cette fois-ci. Tourne la manivelle à la main, juste à la bonne vitesse, pour avoir les meilleurs chances d'attraper quelque chose!"
FishingFailureTooSlow = "Tu as tourné la manivelle trop lentement. Certains poissons sont plus rapides que d'autres. Essaie de conserver la ligne de vitesse au centre!"
FishingFailureTooFast = "Tu as tourné la manivelle trop rapidement. Certains poissons sont plus lents que d'autres. Essaie de conserver la ligne de vitesse au centre!"
FishingOverTankLimit = "Ton seau de pêche est plein. Va vendre tes poissons au vendeur de l'animalerie et reviens."
FishingBroke = "Tu n'as plus de bonbons pour appâter! Va faire un tour de tramway ou vends des poissons aux vendeurs de l'animalerie pour avoir d'autres bonbons."
FishingHowToFirstTime = "Clique sur le bouton de lancer et déplace le curseur vers le bas. Plus tu glisses vers le bas, plus ton lancer sera fort. Ajuste ton angle pour atteindre les poissons.\n\n Essaie maintenant!"
FishingHowToFailed = "Clique sur le bouton de lancer et déplace le curseur vers le bas. Plus tu glisses vers le bas, plus ton lancer sera fort. Ajuste ton angle pour atteindre les poissons.\n\n Essaie encore maintenant!"
FishingBootItem = "Une vieille chaussure"
FishingJellybeanItem = "%s bonbons"
FishingNewEntry = "Nouvelle espèce!"
FishingNewRecord = "Nouveau record!"

# FishPoker
FishPokerCashIn = "Encaisser\n%s\n%s"
FishPokerLock = "Bloquer"
FishPokerUnlock = "Débloquer"
FishPoker5OfKind = "5 identiques"
FishPoker4OfKind = "Carré"
FishPokerFullHouse = "Plein"
FishPoker3OfKind = "Brelan"
FishPoker2Pair = "2 paires"
FishPokerPair = "Paire"

# DistributedTutorial.py
TutorialGreeting1 = "Salut,%s!"
TutorialGreeting2 = "Salut,%s!\nViens par ici!"
TutorialGreeting3 = "Salut,%s!\nViens par ici!\nUtilise les flèches!"
TutorialMickeyWelcome = "Bienvenue à Toontown!"
TutorialFlippyIntro = "Je te présente mon ami " + Flippy + "..."
TutorialFlippyHi = "Salut,%s!"
TutorialQT1 = "Tu peux parler en utilisant ceci."
TutorialQT2 = "Tu peux parler en utilisant ceci.\nClique dessus, puis choisis \"Salut\"."
TutorialChat1 = "Tu peux parler en utilisant l'un de ces boutons."
TutorialChat2 = "Le bouton bleu te permet de chatter avec le clavier."
TutorialChat3 = "Fais attention! La plupart des autres joueurs ne comprendront pas ce que tu dis lorsque tu utilises le clavier."
TutorialChat4 = "Le bouton vert ouvre le %s."
TutorialChat5 = "Tout le monde peut te comprendre si tu utilises le %s."
TutorialChat6 = "Essaie de dire \"salut\"."
TutorialBodyClick1 = "Très bien!"
TutorialBodyClick2 = "Ravi de t'avoir rencontré! Tu veux que nous soyons contacts?"
TutorialBodyClick3 = "Pour devenir ami(e) avec " + Flippy + ", clique sur lui..."
TutorialHandleBodyClickSuccess = "Bon travail!"
TutorialHandleBodyClickFail = "Ce n'est pas ça. Essaie de cliquer juste sur " + Flippy + "..."
TutorialFriendsButton = "Maintenant, clique sur le bouton \"contacts\" sous l'image de " + Flippy + " dans l'angle droit."
TutorialHandleFriendsButton = "Ensuite, clique sur le bouton \"oui\"."
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = "Veux-tu devenir ami(e) avec " + Flippy + "?"
TutorialFriendsPanelMickeyChat = Flippy + " veut bien être ton ami. Clique sur \"OK\" pour terminer." 
TutorialFriendsPanelYes = Flippy + " a dit oui!" 
TutorialFriendsPanelNo = "Ça n'est pas très gentil!"
TutorialFriendsPanelCongrats = "Bravo! Tu t'es fait ton premier ami."
TutorialFlippyChat1 = "Reviens me voir quand tu seras prêt pour ton premier défitoon!"
TutorialFlippyChat2 = "Je serai à la Mairie de Toontown!"
TutorialAllFriendsButton = "Tu peux voir tous tes contacts en cliquant sur le bouton \"contacts\". Essaye donc..."
TutorialEmptyFriendsList = "Pour l'instant, ta liste est vide parce que " + Flippy + " n'est pas véritablement un joueur."
TutorialCloseFriendsList = "Clique sur le bouton \" Fermer \"\npour faire disparaître la liste."
TutorialShtickerButton = "Le bouton dans l'angle inférieur droit ouvre ton journal de bord. Essaye-le..."
TutorialBook1 = "Le journal contient de nombreuses informations utiles comme cette carte de Toontown."
TutorialBook2 = "Tu peux aussi y voir les progrès de tes défitoons."
TutorialBook3 = "Lorsque tu as fini, clique de nouveau sur le bouton représentant un livre pour le fermer."
TutorialLaffMeter1 = "Tu as aussi besoin de ça..."
TutorialLaffMeter2 = "Tu as aussi besoin de ça...\nC'est ton rigolmètre."
TutorialLaffMeter3 = "Lorsque les " + Cogs + " t'attaquent, il baisse."
TutorialLaffMeter4 = "Lorsque tu es sur les terrains de jeux comme celui-ci, il remonte."
TutorialLaffMeter5 = "Lorsque tu finis des défitoons, tu reçois des récompenses, comme l'augmentation de ta rigo-limite."
TutorialLaffMeter6 = "Fais attention! Si les " + Cogs + " te battent, tu perds tous tes gags."
TutorialLaffMeter7 = "Pour avoir plus de gags, joue aux jeux du tramway."
TutorialTrolley1 = "Suis-moi jusqu'au tramway!"
TutorialTrolley2 = "Monte à bord!"
TutorialBye1 = "Joue à des jeux!"
TutorialBye2 = "Joue à des jeux!\nAchète des gags!"
TutorialBye3 = "Va voir " + Flippy + " quand tu auras fini!"

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "Tu vas dans le mauvais sens! Va trouver " + Mickey + "!"

PetTutorialTitle1 = "Le panneau des Doudous"
PetTutorialTitle2 = "Chat rapide des Doudous"
PetTutorialTitle3 = "Catalogue des Doudous"
PetTutorialNext = "Page suivante"
PetTutorialPrev = "Page précédente"
PetTutorialDone = "Terminé"
PetTutorialPage1 = "Clique sur un Doudou pour afficher le panneau des Doudous. Là tu pourras nourrir, cajoler et appeler le Doudou."
PetTutorialPage2 = "Utilise la nouvelle zone 'Animaux familiers' dans le menu de Chat rapide pour que le Doudou fasse un tour. S'il le fait, récompense-le et il s'améliorera!"
PetTutorialPage3 = "Achète de nouveaux tours pour les Doudous dans le catalogue de Clarabelle. De meilleures tours donnent de meilleures tooniques!"
def getPetGuiAlign():
	from pandac.PandaModules import TextNode
	return TextNode.ACenter

GardenTutorialTitle1 = "Jardinage"
GardenTutorialTitle2 = "Fleurs"
GardenTutorialTitle3 = "Arbres"
GardenTutorialTitle4 = "Comment faire"
GardenTutorialTitle5 = "Statues"
GardenTutorialNext = "Page suivante"
GardenTutorialPrev = "Page précédente"
GardenTutorialDone = "Terminé"
GardenTutorialPage1 = "Embellis ta propriété avec un jardin! Tu peux y planter des fleurs, y faire pousser des arbres, y récolter des gags super puissants et le décorer avec des statues!"
GardenTutorialPage2 = "Les fleurs sont délicates et demandent des recettes très particulières à base de bonbons. Une fois qu'elles ont poussé, tu peux les mettre dans une brouette pour aller les vendre et faire gonfler ton rigolmètre."
GardenTutorialPage3 = "Utilise un gag que tu as dans ton inventaire pour planter un arbre. Après quelques jours, ce gag sera encore plus puissant! N'oublie pas d'en prendre soin, ou tu perdras l'augmentation de puissance."
GardenTutorialPage4 = "Marche jusqu'à ces endroits pour planter, arroser, bêcher ou faire la cueillette dans ton jardin."
GardenTutorialPage5 = "Les statues sont vendues dans le Catalogue vachement branché de Clarabelle. Améliore ton habileté pour avoir accès aux statues les plus extravagantes!"

# Playground.py
PlaygroundDeathAckMessage = "Les " + Cogs + " ont pris tous tes gags!\n\nTu es triste. Tu ne peux pas quitter le terrain de jeux avant d'avoir retrouvé la joie de vivre."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "Le contremaître de l'usine a été vaincu avant que tu ne le trouves. Tu n'as pas récupéré de pièces de Cogs."

# MintInterior
ForcedLeaveMintAckMsg = "Le Superviseur de cet étage de la Fabrique à Sous a été vaincu avant que tu ne puisses l'atteindre. Tu n'as pas récupéré de euros Cog."

# DistributedFactory.py
HeadingToFactoryTitle = "En route %s..."
ForemanConfrontedMsg = "%s est en train de combattre le contremaître de l'usine!"

# DistributedMint.py
MintBossConfrontedMsg = "%s est en train de combattre le Superviseur!"

# DistributedStage.py
StageBossConfrontedMsg = "%s se bat contre le juriste!"
stageToonEnterElevator = "%s \nest maintenant dans l'ascenseur"
ForcedLeaveStageAckMsg = "Le juriste a été vaincu avant que tu ne le trouves. Tu n'as pas récupéré de convocations du jury."

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "En attente d'autres joueurs..."
MinigamePleaseWait = "Patiente un peu..."
DefaultMinigameTitle = "Nom du mini jeu"
DefaultMinigameInstructions = "Instructions du mini jeu"
HeadingToMinigameTitle = "En route vers: %s..." # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "Témoin de puissance"
MinigamePowerMeterTooSlow = "Trop\nlent"
MinigamePowerMeterTooFast = "Trop\nrapide"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "Modèle de mini jeu"
MinigameTemplateInstructions = "C'est un modèle de mini jeu. Utilise-le pour créer des mini jeux."

# DistributedCannonGame.py
CannonGameTitle = "Jeu du canon"
CannonGameInstructions = "Envoie ton Toon dans le château d'eau aussi vite que tu peux. Utilise les flèches du clavier ou la souris pour diriger le canon. Sois rapide et gagne une belle récompense pour tout le monde!"
CannonGameReward = "RÉCOMPENSE"

# DistributedTwoDGame.py
TwoDGameTitle = "Toon Escape"
TwoDGameInstructions = "Echappe-toi de cette" + Cog + "tannière dès que possible. Utilise les flèches du clavier pour courir/sauter et la touche Ctrl pour faire gicler un" + Cog + ". Ramasse" + Cog + "les trésors pour gagner encore plus de points."
TwoDGameElevatorExit = "SORTIE"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Tir à la corde"
TugOfWarInstructions = "Appuie alternativement sur les flèches gauche et droite à la vitesse qu'il faut pour aligner la barre verte avec la ligne rouge. N'appuie pas trop rapidement ou trop lentement, tu pourrais finir dans l'eau!"
TugOfWarGameGo = "PARTEZ!"
TugOfWarGameReady = "Prêt..."
TugOfWarGameEnd = "Bien joué!"
TugOfWarGameTie = "Égalité!"
TugOfWarPowerMeter = "Témoin de puissance"

# DistributedPatternGame.py
PatternGameTitle = "Imite "+ Minnie
PatternGameInstructions = Minnie +" va te montrer une suite de pas de danse. "+ \
                          "Essaie de reproduire la danse de "+ Minnie + " comme tu la vois en utilisant les flèches!"
PatternGameWatch   = "Regarde ces pas de danse..."
PatternGameGo      = "PARTEZ!"
PatternGameRight   = "Bien, %s!"
PatternGameWrong   = "Aïe!"
PatternGamePerfect = "C'était parfait, %s!"
PatternGameBye     = "Merci d'avoir joué!"
PatternGameWaitingOtherPlayers = "En attente d'autres joueurs..."
PatternGamePleaseWait = "Patiente un peu..."
PatternGameFaster = "Tu as été\nplus rapide!"
PatternGameFastest = "Tu as été\nle(la) plus rapide!"
PatternGameYouCanDoIt = "Allez!\nTu peux y arriver!"
PatternGameOtherFaster = "\na été plus rapide!"
PatternGameOtherFastest = "\na été le(la) plus rapide!"
PatternGameGreatJob = "Bon travail!"
PatternGameRound = "Partie %s!" # Round 1! Round 2! ..
PatternGameImprov = "Bien joué ! Maintenant monte !"

# DistributedRaceAI.py
WaitingForJoin = 90

# DistributedRaceGame.py
RaceGameTitle = "Jeu de l'oie"
RaceGameInstructions = "Clique sur un nombre. Choisis bien! Tu n'avances que si personne d'autre n'a choisi le même nombre."
RaceGameWaitingChoices = "Attente du choix des autres joueurs..."
RaceGameCardText = "%(name)s tire: %(reward)s"
RaceGameCardTextBeans = "%(name)s reçoit: %(reward)s"
RaceGameCardTextHi1 = "%(name)s est un Toon fabuleux!"  # this category might eventually have secret game hints, etc

# RaceGameGlobals.py
RaceGameForwardOneSpace    = " avance d'une case"
RaceGameForwardTwoSpaces   = " avance de 2 cases"
RaceGameForwardThreeSpaces = " avance de 3 cases"
RaceGameBackOneSpace    = " recule d'une case"
RaceGameBackTwoSpaces   = " recule de 2 cases"
RaceGameBackThreeSpaces = " recule de 3 cases"
RaceGameOthersForwardThree = " tous les autres avancent\nde 3 cases"
RaceGameOthersBackThree = "tous les autres reculent\nde 3 cases"
RaceGameInstantWinner = "Gagnant!"
RaceGameJellybeans2 = "2 bonbons"
RaceGameJellybeans4 = "4 bonbons"
RaceGameJellybeans10 = "10 bonbons!"

# DistributedRingGame.py
RingGameTitle = "Jeu des anneaux"
# color
RingGameInstructionsSinglePlayer = "Essaie de nager en passant dans autant d'anneaux %s que tu pourras. Utilise les flèches pour nager."
# color
RingGameInstructionsMultiPlayer = "Essaie de nager en passant dans les anneaux %s. Les autres joueurs essaieront de passer les anneaux des autres couleurs. Utilise les flèches pour nager."
RingGameMissed = "RATÉ"
RingGameGroupPerfect = "GROUPE\nPARFAIT!!"
RingGamePerfect = "PARFAIT!"
RingGameGroupBonus = "BONUS DE GROUPE"

# RingGameGlobals.py
ColorRed = "rouges"
ColorGreen = "verts"
ColorOrange = "orange"
ColorPurple = "violets"
ColorWhite = "blancs"
ColorBlack = "noirs"
ColorYellow = "jaunes"

# DistributedDivingGame.py
DivingGameTitle = "Chasse aux trésors aquatique"
# color
DivingInstructionsSinglePlayer = "Les trésors apparaissent au fond du lac. Utilise les flèches du clavier pour nager. Évite les poissons et rapporte les trésors dans le bateau."
# color
DivingInstructionsMultiPlayer = "Les trésors apparaissent au fond du lac. Utilise les flèches de ton clavier pour nager. Travailler ensemble pour rapporter les trésors dans le bateau."
DivingGameTreasuresRetrieved = "Recherché Trésors"

#Distributed Target Game
TargetGameTitle = "Jeu du parapluie"
TargetGameInstructionsSinglePlayer = "Atterris sur les cibles pour marquer des points"
TargetGameInstructionsMultiPlayer = "Atterris sur les cibles pour marquer des points"
TargetGameBoard = "Manche %s - Garder le meilleur score"
TargetGameCountdown = "Lancement forcé dans %s secondes"
TargetGameCountHelp = "Touche dièse et flèches droite et gauche pour allumer, stop pour lancer"
TargetGameFlyHelp = "Appuyer pour ouvrir le parapluie"
TargetGameFallHelp = "Utilise les flèches du clavier pour atterrir sur les cibles"
TargetGameBounceHelp = "En rebondissant, tu peux t'écarter de la cible"

#Distributed Photo Game
PhotoGameScoreTaken = "%s: %s\nToi : %s"
PhotoGameScoreBlank = "Score : %s"
PhotoGameScoreOther = ""#"Score: %s\n%s"
PhotoGameScoreYou = "\nMeilleur bonus !"


# DistributedTagGame.py
TagGameTitle = "Jeu du chat"
TagGameInstructions = "Récupère les trésors. Tu ne peux pas récupérer les trésors quand tu es chat!"
TagGameYouAreIt = "Tu es chat!"
TagGameSomeoneElseIsIt = "%s est chat!"

# DistributedMazeGame.py
MazeGameTitle = "Jeu du labyrinthe"
MazeGameInstructions = "Récupère les trésors. Essaie de les avoir tous, mais fais attention aux " + Cogs + "!"

# DistributedCatchGame.py
CatchGameTitle = "Jeu du verger"
CatchGameInstructions = "Attrape des %(fruit)s, autant que tu peux. Attention aux " + Cogs + ", et essaie de ne pas attraper des %(badThing)s!"
CatchGamePerfect = "PARFAIT!"
CatchGameApples      = 'pommes'
CatchGameOranges     = 'oranges'
CatchGamePears       = 'poires'
CatchGameCoconuts    = 'noix de coco'
CatchGameWatermelons = 'pastèques'
CatchGamePineapples  = 'ananas'
CatchGameAnvils      = 'enclumes'

# DistributedPieTossGame.py
PieTossGameTitle = "Jeu du lancer de tartes"
PieTossGameInstructions = "Envoie des tartes dans les cibles."

# DistributedPhotoGame.py
PhotoGameInstructions = "Prends des photos correspondant aux Toons apparaissant en bas. Oriente l'appareil photo avec la souris et fais un clic gauche pour prendre une photo. Appuie sur la touche Ctrl pour faire un zoom avant/arrière, et déplace-toi avec les flèches du clavier. Les photos les mieux classées rapportent le plus de points."
PhotoGameTitle = "Délire photo"
PhotoGameFilm = "FILM"
PhotoGameScore = "Score par équipe : %s\n\nMeilleures photos: %s\n\nScore total : %s"

# DistributedCogThiefGame.py
CogThiefGameTitle = Cog + "Voleur"
CogThiefGameInstructions = "Empêche-le" + Cogs + "de voler nos tonneaux de gags ! Appuie sur la touche Ctrl pour lancer une tarte. Utilise les flèches du clavier pour te déplacer. Astuce : tu peux te déplacer en diagonale."
CogThiefBarrelsSaved = "%(num)d Tonneaux\nsauvés !"
CogThiefBarrelSaved = "%(num)d Tonneaux\nsauvés !"
CogThiefNoBarrelsSaved = "Aucun tonneau\nsauvé"
CogThiefPerfect = "PARFAIT !"

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "JOUER"

# Purchase.py
GagShopName = "La boutique à gags de Dingo"
GagShopPlayAgain = "REJOUER\n"
GagShopBackToPlayground = "RETOUR AU\nTERRAIN DE JEUX"
GagShopYouHave = "Tu as %s à dépenser"
GagShopYouHaveOne = "Tu as 1 bonbon à dépenser"
GagShopTooManyProps = "Désolé, tu as trop d'accessoires"
GagShopDoneShopping = "ACHATS\n TERMINÉS"
# name of a gag
GagShopTooManyOfThatGag = "Désolé, tu as déjà assez de %s"
GagShopInsufficientSkill = "Tu n'es pas encore assez habile pour cela"
# name of a gag
GagShopYouPurchased = "Tu as acheté %s"
GagShopOutOfJellybeans = "Désolé, tu n'as plus de bonbons!"
GagShopWaitingOtherPlayers = "En attente des autres joueurs..."
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%s est déconnecté(e)"
GagShopPlayerExited = "%s est parti(e)"
GagShopPlayerPlayAgain = "Jouer encore"
GagShopPlayerBuying = "Achat en cours"

# MakeAToon.py
GenderShopQuestionMickey = "Pour faire un garçon Toon, clique ici!"
GenderShopQuestionMinnie = "Pour faire une fille Toon, clique ici!"
GenderShopFollow = "Suis-moi!"
GenderShopSeeYou = "À plus tard!"
GenderShopBoyButtonText = "Garçon"
GenderShopGirlButtonText = "Fille"

# BodyShop.py
BodyShopHead = "Tête"
BodyShopBody = "Corps"
BodyShopLegs = "Jambes"

# ColorShop.py
ColorShopHead = "Tête"
ColorShopBody = "Corps"
ColorShopLegs = "Jambes"
ColorShopToon = "Toon"
ColorShopParts = "Parties"
ColorShopAll = "Tout"

# ClothesShop.py
ClothesShopShorts = "Short"
ClothesShopShirt = "Chemise"
ClothesShopBottoms = "Bas"

# MakeAToon
MakeAToonDone = "Fini"
MakeAToonCancel = lCancel
MakeAToonNext = lNext
MakeAToonLast = "Retour"
CreateYourToon = "Clique sur les flèches pour créer ton Toon."
CreateYourToonTitle = "Crée ton Toon"
CreateYourToonHead = "Clique sur les flèches \"tête\" pour choisir différents animaux."
MakeAToonClickForNextScreen = "Clique sur la flèche ci-dessous pour aller à l'écran suivant."
PickClothes = "Clique sur les flèches pour choisir des vêtements!"
PickClothesTitle = "Choisis tes vêtements"
PaintYourToon = "Clique sur les flèches pour peindre ton Toon!"
PaintYourToonTitle = "Peins ton Toon"
MakeAToonYouCanGoBack = "Tu peux aussi retourner en arrière pour changer ton corps!"
MakeAFunnyName = "Choisis un nom amusant pour ton Toon!"
MustHaveAFirstOrLast1 = "Ton Toon devrait avoir un prénom ou un nom de famille, tu ne penses pas?"
MustHaveAFirstOrLast2 = "Tu ne veux pas que ton Toon ait de prénom ou de nom de famille ?"
ApprovalForName1 = "C'est ça, ton Toon mérite un super nom!"
ApprovalForName2 = "Les noms Toon sont les meilleurs noms!"
MakeAToonLastStep = "Dernière étape avant d'aller à Toontown!"
PickANameYouLike = "Choisis un nom que tu aimes!"
NameToonTitle = "Donne un nom à ton Toon"
TitleCheckBox = "Titre"
FirstCheckBox = "Prénom"
LastCheckBox = "Nom"
RandomButton = "Aléatoire"
NameShopSubmitButton = "Envoyer"
TypeANameButton = "Entre un nom"
TypeAName = "Tu n'aimes pas ces noms?\nClique ici -->"
PickAName = "Essaie le jeu Choisis-un-nom!\nClique ici -->"
PickANameButton = "Choisis un nom"
RejectNameText = "Ce nom n'est pas autorisé. Essaie encore."
WaitingForNameSubmission = "Envoi de ton nom..."

# PetshopGUI.py
PetNameMaster = "PetNameMaster_french.txt"
PetshopUnknownName = "Nom:???"
PetshopDescGender = "Sexe:\t%s"
PetshopDescCost = "Coûte:\t%s bonbons"
PetshopDescTrait = "Caractère:\t%s"
PetshopDescStandard = "Standard"
PetshopCancel = lCancel
PetshopSell = "Vendre tes poissons"
PetshopAdoptAPet = "Adopter un Doudou"
PetshopReturnPet = "Rapporter ton Doudou"
PetshopAdoptConfirm = "Adopter %s pour %d bonbons?"
PetshopGoBack = "Retourner"
PetshopAdopt = "Adopter"
PetshopReturnConfirm = "Rapporter %s?"
PetshopReturn = "Rapporter"
PetshopChooserTitle = "LES DOUDOUS DU JOUR"
PetshopGoHomeText = 'Est-ce que tu veux aller dans ta propriété pour jouer avec ton nouveau Doudou?'

# NameShop.py
NameShopNameMaster = "NameMaster_french.txt"
NameShopPay = "Inscris-toi!"
NameShopPlay = "Essai gratuit"
NameShopOnlyPaid = "Seuls les utilisateurs payants\npeuvent donner un nom à leurs Toons.\nJusqu'à ce que tu t'inscrives,\nton nom sera\n"
NameShopContinueSubmission = "Continuer l'envoi"
NameShopChooseAnother = "Choisir un autre nom"
NameShopToonCouncil = "Le Conseil de Toontown\nva examiner ton\nnom.  "+ \
                       "L'examen peut\nprendre quelques jours.\nPendant que tu attends,\nton nom sera\n "
PleaseTypeName = "Entre ton nom:"
AllNewNames = "Tous les noms\ndoivent être approuvés\npar le Conseil de Toontown."
NameMessages = "Be creative and remember:\nno Disney-related names, please."
NameShopNameRejected = "Le nom que tu as\nenvoyé a été refusé."
NameShopNameAccepted = "Félicitations!\nLe nom que tu as\nenvoyé a\nété accepté!"
NoPunctuation = "Tu ne peux pas utiliser de signes de ponctuation dans ton nom!"
PeriodOnlyAfterLetter = "Tu peux utiliser un point dans ton nom, mais seulement après une lettre."
ApostropheOnlyAfterLetter = "Tu peux utiliser une apostrophe dans ton nom, mais seulement après une lettre."
NoNumbersInTheMiddle = "Les caractères numériques ne peuvent pas apparaître au milieu d'un mot."
ThreeWordsOrLess = "Ton nom doit comporter trois mots maximum."
CopyrightedNames = (
    "Mickey",
    "Mickey Mouse",
    "Mickey Mouse",
    "Minnie Mouse",
    "Minnie",
    "Minnie Mouse",
    "Minnie Mouse",
    "Donald",
    "Donald Duck",
    "Donald Duck",
    "Pluto",
    "Dingo",
    )
NumToColor = ['Blanc', 'Pêche', 'Rouge vif', 'Rouge', 'Bordeaux',
              'Terre de Sienne', 'Brun', 'Brun clair', 'Corail', 'Orange',
              'Jaune', 'Crème', 'Jaune-vert', 'Citron vert', 'Vert marin',
              'Vert', 'Bleu clair', 'Turquoise', 'Bleu',
              'Pervenche', 'Bleu roi', 'Bleu ardoise', 'Violet',
              'Lavande', 'Rose']
AnimalToSpecies = {
    'dog'    : 'Chien',
    'cat'    : 'Chat',
    'mouse'  : 'Souris',
    'horse'  : 'Cheval',
    'rabbit' : 'Lapin',
    'duck'   : 'Canard',
    'monkey'   : 'Singe',
    'bear'   : 'Ours',
    'pig'    : 'Cochon'
    }
NameTooLong = "Ce nom est trop long. Essaie encore."
ToonAlreadyExists = "Tu as déjà un Toon qui s'appelle %s!"
NameAlreadyInUse = "Ce nom est déjà utilisé!"
EmptyNameError = "Tu dois indiquer un nom d'abord."
NameError = "Désolé. Ce nom ne pourra pas convenir."

# NameCheck.py
NCTooShort = 'Ce nom est trop court.'
NCNoDigits = 'Ton nom ne peut pas contenir de chiffres.'
NCNeedLetters = 'Chaque mot de ton nom doit contenir des lettres.'
NCNeedVowels = 'Chaque mot de ton nom doit contenir des voyelles.'
NCAllCaps = 'Ton nom ne peut pas être entièrement en majuscules.'
NCMixedCase = 'Ton nom a trop de majuscules.'
NCBadCharacter = "Ton nom ne peut pas contenir le caractère \"%s\""
NCGeneric = 'Désolé, ce nom ne pourra pas convenir.'
NCTooManyWords = 'Ton nom ne peut pas comporter plus de quatre mots.'
NCDashUsage = ("Les tirets ne peuvent être utilisés que pour relier deux mots ensemble."
               "(comme dans \"Bou-Bou\").")
NCCommaEdge = "Ton nom ne peut pas commencer ou se terminer par une virgule."
NCCommaAfterWord = "Tu ne peux pas commencer un mot par une virgule."
NCCommaUsage = ("Ce nom n'utilise pas les virgules correctement. Les virgules doivent"
                "assembler deux mots, comme dans le nom \"Dr Couac, médecin\"."
                "Les virgules doivent aussi être suivies d'un espace.")
NCPeriodUsage = ("Ce nom n'utilise pas les points correctement. Les points sont"
                 "seulement autorisés dans des mots tels que \"M.\",\"doct.\",\"prof.\", etc.")
NCApostrophes = "Ton nom a trop d'apostrophes."

# DistributedTrophyMgrAI.py
RemoveTrophy = lToonHQ+" : Les " + Cogs + " ont repris un des bâtiments que tu avais sauvés!"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = 'Tu as besoin de plus de temps pour réfléchir ?'
STOREOWNER_GOODBYE = 'À plus tard!'
STOREOWNER_NEEDJELLYBEANS = 'Tu dois faire un tour de tramway pour avoir des bonbons.'
STOREOWNER_GREETING = 'Choisis ce que tu veux acheter.'
STOREOWNER_BROWSING = "Tu peux regarder, mais tu auras besoin d'un ticket d'habillement pour acheter."
STOREOWNER_NOCLOTHINGTICKET = "Tu as besoin d'un ticket d'habillement pour acheter des vêtements."
# translate
STOREOWNER_NOFISH = "Reviens ici pour vendre des poissons à l'animalerie en échange de bonbons."
STOREOWNER_THANKSFISH = "Merci! L'animalerie va les adorer. Au revoir!"
STOREOWNER_THANKSFISH_PETSHOP = "Ce sont de beaux spécimens! Merci."
STOREOWNER_PETRETURNED = "Ne t'inquiete pas. Nous trouverons une bonne maison pour ton Doudou."
STOREOWNER_PETADOPTED = "Félicitations pour ton nouveau Doudou! Tu peux jouer avec lui dans ta propriété."
STOREOWNER_PETCANCELED = "N'oublie pas: si tu vois un Doudou qui te plaît, adopte-le avant que quelqu'un d'autre ne le fasse!"

STOREOWNER_NOROOM = "Hmm...tu devrais faire de la place dans ton placard avant d'acheter de nouveaux vêtements.\n"
STOREOWNER_CONFIRM_LOSS = "Ton placard est plein. Tu vas perdre les vêtements que tu portais."
STOREOWNER_OK = lOK
STOREOWNER_CANCEL = lCancel
STOREOWNER_TROPHY = "Oh là là! Tu as trouvé %s sur %s poissons. Ça mérite un trophée et une rigol-augmentation!"
# end translate

# NewsManager.py
SuitInvasionBegin1 = lToonHQ+": Une invasion de Cogs a commencé!!!"
SuitInvasionBegin2 = lToonHQ+": Les %s ont pris Toontown!!!"
SuitInvasionEnd1 = lToonHQ+": L'invasion des %s est terminée!!!"
SuitInvasionEnd2 = lToonHQ+": Les Toons nous ont sauvés une fois de plus!!!"
SuitInvasionUpdate1 = lToonHQ+": L'invasion de Cogs en est à %s Cogs!!!"
SuitInvasionUpdate2 = lToonHQ+": Nous devons battre ces %s!!!"
SuitInvasionBulletin1 = lToonHQ+": Il y a une invasion de Cogs en cours!!!"
SuitInvasionBulletin2 = lToonHQ+": Les %s ont pris Toontown!!!"

# DistributedHQInterior.py
LeaderboardTitle = "Armée de Toons"
# QuestScript.txt
QuestScriptTutorialMickey_1 = "Toontown compte un nouveau citoyen! Est-ce que tu as des gags en plus?"
QuestScriptTutorialMickey_2 = "Bien sûr, %s!"
QuestScriptTutorialMickey_3 = "Tom Tuteur va te parler des Cogs.\aJe dois y aller!"
QuestScriptTutorialMickey_4 = "Viens ici! Utilise les flèches pour te déplacer."

# These are needed to correspond to the Japanese gender specific phrases
QuestScriptTutorialMinnie_1 = "Toontown compte une nouvelle citoyenne! Est-ce que tu as des gags en plus?"
QuestScriptTutorialMinnie_2 = "Bien sûr, %s!"
QuestScriptTutorialMinnie_3 = "Tom Tuteur va te parler des Cogs.\aJe dois y aller!"

QuestScript101_1 = "Ce sont les COGS. Ce sont des robots qui essaient de prendre Toontown."
QuestScript101_2 = "Il y a différentes sortes de COGS et..."
QuestScript101_3 = "...ils transforment de bons bâtiments Toon..."
QuestScript101_4 = "...en affreuses bâtisses Cog!"
QuestScript101_5 = "Mais les COGS ne comprennent pas les blagues!"
QuestScript101_6 = "Un bon gag les arrête."
QuestScript101_7 = "Il y a des quantités de gags; prends ceux-là pour commencer."
QuestScript101_8 = "Oh! Tu as aussi besoin d'un rigolmètre!"
QuestScript101_9 = "Si ton rigolmètre descend trop bas, tu seras triste!"
QuestScript101_10 = "Un Toon heureux est un Toon en bonne santé!"
QuestScript101_11 = "OH NON! Il y a un COG devant ma boutique!"
QuestScript101_12 = "AIDE-MOI, S'IL TE PLAÎT! Va vaincre ce COG!"
QuestScript101_13 = "Voilà ton premier défitoon!"
QuestScript101_14 = "Dépêche-toi! Va battre ce Laquaistic!"

QuestScript110_1 = "Bon travail pour avoir vaincu ce Laquaistic. Je vais te donner un journal de bord..."
QuestScript110_2 = "Ce journal est plein de choses intéressantes."
QuestScript110_3 = "Ouvre-le, et je vais te montrer."
QuestScript110_4 = "La carte montre où tu as été."
QuestScript110_5 = "Tourne la page pour voir tes gags..."
QuestScript110_6 = "Oh oh! Tu n'as pas de gags! Je vais te donner un défi."
QuestScript110_7 = "Tourne la page pour voir tes défis."
QuestScript110_8 = "Fais un tour de tramway, et gagne des bonbons pour acheter des gags!"
QuestScript110_9 = "Pour aller jusqu'au tramway, sors par la porte qui est derrière moi et va jusqu'au terrain de jeux."
QuestScript110_10 = "Maintenant, ferme le livre et trouve le tramway!"
QuestScript110_11 = "Retourne au QG des Toons quand tu as fini. Au revoir!"

QuestScriptTutorialBlocker_1 = "Bien le bonjour!"
QuestScriptTutorialBlocker_2 = "Bonjour ?"
QuestScriptTutorialBlocker_3 = "Oh! Tu ne sais pas utiliser le Chat rapide!"
QuestScriptTutorialBlocker_4 = "Clique sur le bouton pour dire quelque chose."
QuestScriptTutorialBlocker_5 = "Très bien!\aLà où tu vas, il y a plein de Toons à qui parler."
QuestScriptTutorialBlocker_6 = "Si tu veux chatter avec tes contacts à l'aide du clavier, tu peux utiliser un autre bouton."
QuestScriptTutorialBlocker_7 = "Ça s'appelle le bouton \"Chat\". Tu dois être officiellement citoyen de Toontown pour l'utiliser."
QuestScriptTutorialBlocker_8 = "Bonne chance! À plus tard!"

"""
GagShopTut

Tu gagneras aussi la possibilité d'utiliser d'autres types de gags.

"""

QuestScriptGagShop_1 = "Bienvenue à la Boutique à gags!"
QuestScriptGagShop_1a = "C'est là que viennent les Toons pour acheter des gags qu'ils utiliseront contre les Cogs."
#QuestScriptGagShop_2 = "Ce pot indique combien de bonbons tu as."
#QuestScriptGagShop_3 = "Pour acheter un gag, clique sur le bouton " Gag ". Essaie maintenant!"
QuestScriptGagShop_3 = "Pour acheter des gags, clique sur les boutons de gag. Essaie d'en avoir maintenant!"
QuestScriptGagShop_4 = "Super! Tu peux utiliser ces gags lors des combats contre les Cogs."
QuestScriptGagShop_5 = "Voila un aperçu des gags avancés de lancer et d'éclaboussure..."
QuestScriptGagShop_6 = "Quand tu as fini d'acheter des gags, clique sur ce bouton pour retourner au terrain de jeu."
QuestScriptGagShop_7 = "Normalement, tu peux utiliser ce bouton pour jouer à un autre jeu du tramway..."
QuestScriptGagShop_8 = "...mais tu n'as pas le temps de faire un autre jeu maintenant. On t'attend au quartier général des Toons!"

QuestScript120_1 = "Bien, tu as trouvé le tramway!\aAu fait, as-tu rencontré Bob le Banquier ?\aIl aime bien les sucreries.\aPourquoi n'irais-tu pas te présenter en lui emportant ce sucre d'orge comme cadeau?"
QuestScript120_2 = "Bob le Banquier est dans la banque de Toontown."

QuestScript121_1 = "Miam, merci pour ce sucre d'orge.\aDis donc, si tu peux m'aider, je te donnerai une récompense.\aCes Cogs ont volé les clés de mon coffre. Va battre des Cogs pour trouver une clé volée.\aQuand tu auras trouvé une clé, ramène-la moi."

QuestScript130_1 = "Bien, tu as trouvé le tramway!\aPendant qu'on y est, j'ai reçu un paquet pour le Professeur Pete aujourd'hui.\aÇa doit être la nouvelle craie qu'il a commandée.\aPeux-tu lui apporter s'il te plaît ?\aIl est dans l'école."

QuestScript131_1 = "Oh, merci pour la craie.\aQuoi?!?\aCes Cogs ont volé mon tableau. Va vaincre des Cogs pour retrouver le tableau qu'ils m'ont volé.\aQuand tu l'auras trouvé, ramène-le moi."

QuestScript140_1 = "Bien, tu as trouvé le tramway!\aPendant qu'on y est, j'ai un ami, Larry le Libraire, qui est un rat de bibliothèque.\aJ'ai pris ce livre pour lui la dernière fois que j'ai été aux quais Donald.\aPourrais-tu lui apporter ? Il est à la bibliothèque, d'habitude."

QuestScript141_1 = "Oh, oui, ce livre complète presque ma collection.\aVoyons ça...\aAh, oh...\aMais où est-ce que j'ai mis mes lunettes?\aJe les avais juste avant que ces Cogs ne prennent mon bâtiment.\aVa vaincre des Cogs pour retrouver les lunettes qu'ils m'ont volées.\aQuand tu les auras retrouvées, reviens me voir pour avoir une récompense."

QuestScript145_1 = "Je vois que tu n'as pas eu de problèmes avec le tramway!\aÉcoute, les Cogs ont volé notre brosse à tableaux.\aVa dans les rues et combats les Cogs jusqu'a ce que tu retrouves la brosse.\aPour atteindre les rues, passe par un des tunnels comme celui-ci :"
QuestScript145_2 = "Quand tu auras retrouvé notre brosse, ramene-la ici.\aN'oublie pas : si tu as besoin de gags, va faire un tour de tramway.\aDe meme, si tu as besoin de récupérer des rigolpoints, ramasse des cônes de glace sur le terrain de jeu."

QuestScript150_1 = "Oh... le prochain défi pourrait être trop difficile pour que tu le fasses tout(e) seul(e)!"
QuestScript150_2 = "Pour te faire des contacts, trouve un autre joueur et utilise le bouton Nouvel ami."
QuestScript150_3 = "Une fois que tu t'es fait un(e) ami(e), reviens ici."
QuestScript150_4 = "Certains défis sont trop difficiles pour un Toon seul!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignorer"

SellbotBossName = "Premier Vice-\nPrésident"
CashbotBossName = "Vice-\nPrésident"
LawbotBossName = "Chief Justice"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "En vertu des pouvoirs qui me sont conférés, tu es promu au grade %s. Félicitations!"
BossCogDoobersAway = { 's' : "Va! Et réalise cette vente!" }
BossCogWelcomeToons = "Bienvenue aux nouveaux Cogs!"
BossCogPromoteToons = "En vertu des pouvoirs qui me sont conférés, tu es promu au grade %s. Félicitations!"
CagedToonInterruptBoss = "Hé! Hou! Hé là-bas!"
CagedToonRescueQuery = "Alors les Toons, vous êtes venus me sauver ?"
BossCogDiscoverToons = "Eh? Des Toons! Déguisés!"
BossCogAttackToons = "À l'attaque!!"
CagedToonDrop = [
    "Bon travail! Tu l'épuises!",
    "Ne le lâchez pas! Il va s'enfuir!",
    "Vous êtes super les copains!",
    "Fantastique! Vous l'avez presque maintenant!",
    ]
CagedToonPrepareBattleTwo = "Attention, il essaie de s'enfuir!\aAidez-moi, tout le monde - montez jusque là et arrêtez-le!"
CagedToonPrepareBattleThree = "Youpi, je suis presque libre!\aMaintenant vous devez attaquer le vice-président des Cogs directement.\aJ'ai tout un lot de tartes que vous pouvez utiliser!\aSautez en l'air et touchez le fond de ma cage, je vous donnerai des tartes.\aAppuyez sur la touche \"Inser\" pour lancer les tartes une fois que vous les avez!"
BossBattleNeedMorePies = "Vous avez besoin de plus de tartes!"
BossBattleHowToGetPies = "Sautez en l'air pour toucher la cage et avoir des tartes."
BossBattleHowToThrowPies = "Appuyez sur la touche \"Inser\" pour lancer les tartes!"
CagedToonYippee = "Génial!"
CagedToonThankYou = "C'est super d'être libre!\aMerci pour toute votre aide!\aJe suis à votre service.\aSi jamais vous avez besoin d'aide pour un combat, vous pouvez m'appeler!\aCliquez simplement sur le bouton SOS pour m'appeler."
CagedToonPromotion = "\aDis donc - ce vice-président Cog a laissé derrière lui les papiers de ta promotion.\aJe vais les envoyer pour toi en sortant, pour que tu aies ta promotion!"
CagedToonLastPromotion = "\aWaou, tu as atteint le niveau %s sur ton costume de Cog!\aLes Cogs ne montent pas en grade plus haut que ça.\aTu ne peux plus monter ton costume de Cog en grade, mais tu peux évidemment continuer à sauver des Toons!"
CagedToonHPBoost = "\aTu as sauvé beaucoup de Toons dans ce QG.\aLe Conseil de Toontown a décidé de te donner un autre rigolpoint. Félicitations!"
CagedToonMaxed = "\aJe vois que tu as un costume de Cog de niveau %s. Très impressionnant!\aDe la part du Conseil de Toontown, merci d'être revenu(e) sauver encore plus de Toons!"
CagedToonGoodbye = "À la prochaine!"


CagedToonBattleThree = {
    10: "Joli saut, %(toon)s. Voilà quelques tartes!",
    11: "Salut, %(toon)s! Prenez des tartes!",
    12: "Hé là,%(toon)s! Vous avez des tartes maintenant!",
    
    20: "Hé, %(toon)s! Sautez jusqu'à ma cage et prenez des tartes à lancer!",
    21: "Hé, %(toon)s! Utilisez la touche \"Ctrl\" pour sauter et toucher ma cage!",
    
    100: "Appuyez sur la touche \"Inser\" pour lancer une tarte!",
    101: "Le compteur bleu montre à quelle hauteur ta tarte va monter.",
    102: "Essaie d'abord de lancer une tarte sous son châssis pour bousiller son mécanisme.",
    103: "Attends que la porte s'ouvre, et lance une tarte à l'intérieur.",
    104: "Lorsqu'il est étourdi, frappe-le au visage ou au torse pour le renverser!",
    105: "Tu sauras que tu l'as frappé comme il faut quand tu verras une tache de couleur.",
    106: "Si tu frappes un Toon avec une tarte, cela donne à ce Toon un rigolpoint!",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

CashbotBossHadEnough = "Ça suffit. J'en ai assez de ces Toons si énervants!"
CashbotBossOuttaHere = "J'ai un train à prendre!"
ResistanceToonName = "Inès Pionne"
ResistanceToonCongratulations = "Tu y es arrivé(e)! Félicitations!\aTu es un membre de valeur de la Résistance!\aVoici une phrase très spéciale que tu peux utiliser en cas de situation difficile :\a%s\aQuand tu la prononces, %s.\aMais tu ne peux l'utiliser qu'une seule fois, alors choisis bien ton moment!"
ResistanceToonToonupInstructions = "Tous les Toons qui sont près de toi vont gagner %s rigolpoints."
ResistanceToonToonupAllInstructions = "Tous les Toons qui sont près de toi vont gagner un renouvellement de tout leur stock de rigolpoints."
ResistanceToonMoneyInstructions = "Tous les Toons qui sont près de toi vont gagner %s bonbons."
ResistanceToonMoneyAllInstructions = "Tous les Toons qui sont près de toi vont remplir leurs pots de bonbons."
ResistanceToonRestockInstructions = "Tous les Toons qui sont près de toi vont compléter leur stock de \"%s\" gags."
ResistanceToonRestockAllInstructions = "Tous les Toons qui sont près de toi vont compléter entièrement leur stock de gags."

ResistanceToonLastPromotion = "\aWaouh, tu as atteint le niveau %s de ton costume de Cog!\aLes Cogs ne vont jamais plus haut que ce niveau.\aTu ne peux plus rien ajouter à ton costume de Cog mais tu peux bien sûr continuer à travailler pour la Résistance!"
ResistanceToonHPBoost = "\aTu as beaucoup fait pour la Résistance.\aLe Conseil des Toons a décidé de te donner un autre rigolpoint. Félicitations!"
ResistanceToonMaxed = "\aJe vois que tu as un costume de Cog de niveau %s. Très impressionnant!\aDe la part du Conseil des Toons, merci d'être revenu pour secourir encore plus de Toons!"

CashbotBossCogAttack = "Attrapez-les!!!"
ResistanceToonWelcome = "Ça y est, tu y es arrivé! Suis-moi jusqu'au coffre-fort principal avant que le Vice-Président ne nous trouve!"
ResistanceToonTooLate = "Zut alors! Nous arrivons trop tard!"
CashbotBossDiscoverToons1 = "Ah-AH!"
CashbotBossDiscoverToons2 = "Il me semblait bien que ça sentait le Toon par ici! Imposteurs!"
ResistanceToonKeepHimBusy = "Occupe-le! Je vais préparer un piège!"
ResistanceToonWatchThis = "Regarde ça!"
CashbotBossGetAwayFromThat = "Eh! Ne touche pas à ça!"
ResistanceToonCraneInstructions1 = "Prends le contrôle d'un aimant en montant sur un podium."
ResistanceToonCraneInstructions2 = "Utilise les flèches de ton clavier pour déplacer la grue et appuie sur la touche Ctrl pour attraper un objet."
ResistanceToonCraneInstructions3 = "Attrape un coffre-fort avec un aimant et fais tomber le casque de sécurité du Vice-Président."
ResistanceToonCraneInstructions4 = "Une fois que le casque est tombé, prends un goon désactivé et frappe-le à la tête!"
ResistanceToonGetaway = "Eek! Courons!"
CashbotCraneLeave = "Quitter la grue"
CashbotCraneAdvice = "Utilise les flèches de ton clavier pour déplacer la grue au-dessus."
CashbotMagnetAdvice = "Maintiens la touche Ctrl enfoncée pour attraper des objets."
CashbotCraneLeaving = "En train de quitter la grue"

MintElevatorRejectMessage = "Tu ne peux pas entrer dans les Fabriques à Sous avant d'avoir complété ton %s costume de Cog."
BossElevatorRejectMessage = "Tu ne peux pas monter dans cet ascenseur avant d'avoir gagné une promotion."
NotYetAvailable = "Cet ascenseur n'est pas encore disponible."

# Types of catalog items--don't translate yet.
FurnitureTypeName = "Meuble"
PaintingTypeName = "Tableau"
ClothingTypeName = "Vêtement"
ChatTypeName = "Phrase de Chat rapide"
EmoteTypeName = "Leçons de comédie"
BeanTypeName = "Bonbons"
PoleTypeName = "Canne à pêche"
WindowViewTypeName = "Vue de la fenêtre"
PetTrickTypeName = "Entraînement du Doudou"
GardenTypeName = "Matériaux de jardinage"
RentalTypeName = "Article à louer"
GardenStarterTypeName = "Kit de jardinage"
NametagTypeName = "Badge"

#rental names
RentalHours = "Heures"
RentalOf = "De"
RentalCannon = "Canons !"
RentalGameTable = "Table de jeu !"
RentalTime = "Heures de"

EstateCannonGameEnd = "La location du jeu du canon est terminée."
GameTableRentalEnd = "La location de la table de jeu est terminée."

MessageConfirmRent = "Commencer à louer? Annule pour enregistrer la location pour plus tard"
MessageConfirmGarden = "Veux-tu vraiment commencer un jardin?"

#nametag Names
NametagPaid = "Badge Citoyen"
NametagAction = "Badge Action"
NametagFrilly = "Badge à fanfreluches"

FurnitureYourOldCloset = "ton ancienne armoire"
FurnitureYourOldBank = "ton ancienne tirelire"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py--don't translate yet.
FurnitureNames = {
  100 : "Fauteuil",
  105 : "Fauteuil",
  110 : "Chaise",
  120 : "Chaise de bureau",
  130 : "Chaise en rondins",
  140 : "Chaise homard",
  145 : "Chaise de survie",
  150 : "Tabouret selle",
  160 : "Chaise locale",
  170 : "Chaise gâteau",
  200 : "Lit",
  205 : "Lit",
  210 : "Lit",
  220 : "Lit baignoire",
  230 : "Lit feuille",
  240 : "Lit bateau",
  250 : "Hamac cactus",
  260 : "Lit crème glacée",
  270 : "Olivia Erin & Cat's Bed",
  300 : "Piano mécanique",
  310 : "Orgue",
  400 : "Cheminée",
  410 : "Cheminée",
  420 : "Cheminée ronde",
  430 : "Cheminée",
  440 : "Cheminée pomme",
  450 : "Erin's Fireplace",
  500 : "Armoire",
  502 : "Armoire pour 15 vêtements",
  504 : "Armoire 20 articles",
  506 : "Armoire 25 articles",
  510 : "Armoire",
  512 : "Armoire pour 15 vêtements",
  514 : "Armoire 20 articles",
  516 : "Armoire 25 articles",
  600 : "Petite lampe",
  610 : "Lampe haute",
  620 : "Lampe de table",
  625 : "Lampe de table",
  630 : "Lampe Daisy",
  640 : "Lampe Daisy",
  650 : "Lampe méduse",
  660 : "Lampe méduse",
  670 : "Lampe cow-boy",
  700 : "Chaise capitonnée",
  705 : "Chaise capitonnée",
  710 : "Divan",
  715 : "Divan",
  720 : "Divan foin",
  730 : "Divan sablé",
  800 : "Bureau",
  810 : "Bureau en rondins",
  900 : "Porte-parapluie",
  910 : "Portemanteau",
  920 : "Poubelle",
  930 : "Champignon rouge",
  940 : "Champignon jaune",
  950 : "Portemanteau",
  960 : "Étal onneau",
  970 : "Cactus",
  980 : "Tipi",
  990 : "Juliette's Fan",
  1000 : "Grand tapis",
  1010 : "Tapis rond",
  1015 : "Tapis rond",
  1020 : "Petit tapis",
  1030 : "Paillasson",
  1100 : "Vitrine",
  1110 : "Vitrine",
  1120 : "Bibliothèque haute",
  1130 : "Bibliothèque basse",
  1140 : "Coffre Sundae",
  1200 : "Table d'appui",
  1210 : "Petite table",
  1215 : "Petite table",
  1220 : "Table de salon",
  1230 : "Table de salon",
  1240 : "Table de plongeur",
  1250 : "Table cookie",
  1260 : "Table de chevet",
  1300 : "Tirelire de 1000 bonbons",
  1310 : "Tirelire de 2500 bonbons",
  1320 : "Tirelire de 5000 bonbons",
  1330 : "Tirelire de 7500 bonbons",
  1340 : "Tirelire de 10000 bonbons",
  1399 : "Téléphone",
  1400 : "Toon Cézanne",
  1410 : "Fleurs",
  1420 : "Mickey contemporain",
  1430 : "Toon Rembrandt",
  1440 : "Paysage Toon",
  1441 : "Cheval de Whistler",
  1442 : "Étoile Toon",
  1443 : "Pas une tarte",
  1500 : "Radio",
  1510 : "Radio",
  1520 : "Radio",
  1530 : "Télévision",
  1600 : "Vase bas",
  1610 : "Vase haut",
  1620 : "Vase bas",
  1630 : "Vase haut",
  1640 : "Vase bas",
  1650 : "Vase bas",
  1660 : "Vase corail",
  1661 : "Vase coquillage",
  1700 : "Chariot de pop-corn",
  1710 : "Coccinelle",
  1720 : "Fontaine",
  1725 : "Machine à laver",
  1800 : "Aquarium",
  1810 : "Aquarium",
  1900 : "Poisson-scie",
  1910 : "Requin-marteau",
  1920 : "Cornes porte-manteau",
  1930 : "Sombrero classique",
  1940 : "Sombrero fantaisie",
  1950 : "Attrapeur de rêves",
  1960 : "Fer à cheval",
  1970 : "Portrait de bison",
  2000 : "Balançoire bonbon",
  2010 : "Toboggan gâteau",
  3000 : "Baignoire Banana Split",
  10000 : "Petite citrouille",
  10010 : "Grande citrouille",
  }

# CatalogClothingItem.py--don't translate yet.
ClothingArticleNames = (
    "Chemise",
    "Chemise",
    "Chemise",
    "Short",
    "Short",
    "Jupe",
    "Short",
    )

ClothingTypeNames = {
    1400 : "Chemise de Mathieu",
    1401 : "Chemise de Jessica",
    1402 : "Chemise de Marissa",
    1600 : "Tenue Piège",
    1601 : "Tenue Tapage",
    1602 : "Tenue Leurre",
    1603 : "Tenue Piège",
    1604 : "Tenue Tapage",
    1605 : "Tenue Leurre",
    1606 : "Tenue Piège",
    1607 : "Tenue Tapage",
    1608 : "Tenue Leurre",
    }

# CatalogSurfaceItem.py--don't translate yet.
SurfaceNames = (
    "Papier peint",
    "Moulures",
    "Revêtement de sol",
    "Lambris",
    "Bordure",
    )

WallpaperNames = {
    1000 : "Parchemin",
    1100 : "Milan",
    1200 : "Douvres",
    1300 : "Victoria",
    1400 : "Newport",
    1500 : "Pastoral",
    1600 : "Arlequin",
    1700 : "Lune",
    1800 : "Étoiles",
    1900 : "Fleurs",
    2000 : "Jardin de printemps",
    2100 : "Jardin classique",
    2200 : "Jour de course",
    2300 : "Marqué!",
    2400 : "Nuage 9",
    2500 : "Vigne vierge",
    2600 : "Printemps",
    2700 : "Kokeshi",
    2800 : "Petits bouquets",
    2900 : "Poisson ange",
    3000 : "Bulles",
    3100 : "Bulles",
    3200 : "À la pêche",
    3300 : "Poisson stop",
    3400 : "Hippocampe",
    3500 : "Coquillages",
    3600 : "Sous l'eau",
    3700 : "Bottes",
    3800 : "Cactus",
    3900 : "Chapeau de cow-boy",
    10100 : "Chats",
    10200 : "Chauve-souris",
    11000 : "Flocons de neige",
    11100 : "Houx",
    11200 : "Bonhomme de neige",
    13000 : "Trèfle",
    13100 : "Trèfle",
    13200 : "Arc-en-ciel",
    13300 : "Trèfle",
    }

FlooringNames = {
    1000 : "Parquet",
    1010 : "Moquette",
    1020 : "Carrelage losange",
    1030 : "Carrelage losange",
    1040 : "Pelouse",
    1050 : "Briques beiges",
    1060 : "Briques rouges",
    1070 : "Carrelage carré",
    1080 : "Pierre",
    1090 : "Bois",
    1100 : "Terre",
    1110 : "Pavage de bois",
    1120 : "Carrelage",
    1130 : "Nid d'abeilles",
    1140 : "Eau",
    1150 : "Carrelage plage",
    1160 : "Carrelage plage",
    1170 : "Carrelage plage",
    1180 : "Carrelage plage",
    1190 : "Sable",
    10000 : "Glaçon",
    10010 : "Igloo",
    11000 : "Trèfle",
    11010 : "Trèfle",
    }

MouldingNames = {
    1000 : "Noueux",
    1010 : "Peint",
    1020 : "Denté",
    1030 : "Fleurs",
    1040 : "Fleurs",
    1050 : "Coccinelle",
    }

WainscotingNames = {
    1000 : "Peint",
    1010 : "Panneau de bois",
    1020 : "Bois",
    }

# CatalogWindowItem.py--don't translate yet.
WindowViewNames = {
    10 : "Grand jardin",
    20 : "Jardin sauvage",
    30 : "Jardin grec",
    40 : "Paysage urbain",
    50 : "Far West",
    60 : "Sous l'océan",
    70 : "Île tropicale",
    80 : "Nuit étoilée",
    90 : "Lagon Tiki",
    100 : "Frontière gelée",
    110 : "Pays fermier",
    120 : "Camp local",
    130 : "Grand rue",
    }

# don't translate yet
NewCatalogNotify = "De nouveaux articles sont prêts à être commandés par téléphone!"
NewDeliveryNotify = "Un colis t'attend dans ta boîte aux lettres!"
CatalogNotifyFirstCatalog = "Ton premier catalogue est arrivé! Tu peux l'utiliser pour commander de nouveaux objets pour toi ou pour ta maison."
CatalogNotifyNewCatalog = "Ton catalogue N°%s est arrivé! Tu peux utiliser ton téléphone pour commander des articles dans le catalogue de Clarabelle."
CatalogNotifyNewCatalogNewDelivery = "Un colis t'attend dans ta boîte aux lettres! Ton catalogue N°%s est aussi arrivé!"
CatalogNotifyNewDelivery = "Un colis t'attend dans ta boîte aux lettres!"
CatalogNotifyNewCatalogOldDelivery = "Ton catalogue N°%s est arrivé, et des objets t'attendent encore dans ta boîte aux lettres!"
CatalogNotifyOldDelivery = "Des articles t'attendent encore dans ta boîte aux lettres!"
CatalogNotifyInstructions = "Clique sur le bouton \"Retour à la maison\" sur la carte de ton journal de bord, puis va jusqu'au téléphone qui est dans ta maison."
CatalogNewDeliveryButton = "Nouvelle\nlivraison!"
CatalogNewCatalogButton = "Nouveau\ncatalogue"
CatalogSaleItem = "Vente!"

# don't translate yet
DistributedMailboxEmpty = "Ta boîte aux lettres est vide pour l'instant. Reviens ici chercher les articles que tu as commandés par téléphone quand ils seront livrés!"
DistributedMailboxWaiting = "Ta boîte aux lettres est vide pour l'instant, mais le paquet que tu as commandé est en chemin. Reviens voir plus tard!"
DistributedMailboxReady = "Ta commande est arrivée!"
DistributedMailboxNotOwner = "Désolé, ce n'est pas ta boîte aux lettres."
DistributedPhoneEmpty = "Tu peux utiliser n'importe quel téléphone pour commander des articles pour toi et pour ta maison. De nouveaux articles seront proposés dans l'avenir.\n\nAucun article n'est disponible à la commande maintenant, mais reviens voir plus tard!"

# don't translate yet
Clarabelle = "Clarabelle"
MailboxExitButton = "Fermer boîte\naux lettres"
MailboxAcceptButton = "Accepter"
MailBoxDiscard = "Refuser"
MailboxAcceptInvite = "Accept this invite"
MailBoxRejectInvite = "Reject this invite"
MailBoxDiscardVerify = "Es-tu sûr de vouloir rejeter %s ?"
MailboxOneItem = "Ta boîte aux lettres contient 1 objet."
MailboxNumberOfItems = "Ta boîte aux lettres contient %s objets."
MailboxGettingItem = "Récupération de %s dans la boîte aux lettres."
MailboxGiftTag = "Cadeau de : %s"
MailboxGiftTagAnonymous = "Anonyme"
MailboxItemNext = "Objet\nsuivant"
MailboxItemPrev = "Objet\nprécédent"
MailboxDiscard = "Rejeter"
MailboxLeave = "Accepter"
CatalogCurrency = "bonbons"
CatalogHangUp = "Raccrocher"
CatalogNew = "NOUVEAUTÉ"
CatalogBackorder = "PRÉ-COMMANDE"
CatalogLoyalty = "SPECIAL"
CatalogPagePrefix = "Page"
CatalogGreeting = "Bonjour! Merci d'avoir appelé le catalogue de Clarabelle. Que puis-je pour toi?"
CatalogGoodbyeList = ["Au revoir!",
                      "Rappelle bientôt!",
                      "Merci de ton appel!",
                      "OK, au revoir!",
                      "Au revoir!",
                      ]
CatalogHelpText1 = "Tourne la page pour voir les articles qui sont en vente."
CatalogSeriesLabel = "Série %s"
CatalogGiftFor = "Acheter un cadeau pour :"
CatalogGiftTo = "Pour : %s"
CatalogGiftToggleOn = "Arrêter d'acheter\ndes cadeaux"
CatalogGiftToggleOff = "Acheter des\ncadeaux"
CatalogGiftToggleWait = "En train d'essayer!..."
CatalogGiftToggleNoAck = "Indisponible"
CatalogPurchaseItemAvailable = "Parfait ! Peut commencer à utiliser ton cadeau dès maintenant."
CatalogPurchaseGiftItemAvailable = "Parfait ! Ton cadeau pour %s sera livré dans sa boîte aux lettres."
CatalogPurchaseItemOnOrder = "Félicitations! Ton achat sera bientôt livré dans ta boîte aux lettres."
CatalogPurchaseGiftItemOnOrder = " Parfait ! Ton cadeau pour %s sera livré dans sa boîte aux lettres."
CatalogAnythingElse = "Puis-je autre chose pour toi?"
CatalogPurchaseClosetFull = "Ton placard est plein. Tu peux acheter cet article, mais tu devras supprimer quelque chose de ton placard pour faire de la place quand il arrivera.\n\nTu veux quand même acheter cet article ?"
CatalogAcceptClosetFull = "Ton placard est plein. Tu dois rentrer et supprimer quelque chose de ton placard pour faire de la place pour cet objet avant de pouvoir le sortir de la boîte aux lettres."
CatalogAcceptShirt = "Tu portes maintenant ta nouvelle chemise. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptShorts = "Tu portes maintenant ton nouveau short. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptSkirt = "Tu portes maintenant ta nouvelle jupe. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptPole = "Tu peux maintenant attraper des poissons plus gros avec ta nouvelle canne!"
CatalogAcceptPoleUnneeded = "Tu as déjà une canne meilleure que celle-ci!"
CatalogAcceptChat = "Tu possèdes maintenant une nouvelle phrase de Chat rapide."
CatalogAcceptEmote = "Tu possèdes maintenant une nouvelle émotion  !"
CatalogAcceptBeans = "Tu as reçu des bonbons  !"
CatalogAcceptRATBeans = "Ta récompense de recrue Toon est arrivée !"

CatalogAcceptNametag = "Your new name tag has arrived !"
CatalogAcceptGarden = "Tes matériaux de jardinage sont arrivés !"
CatalogAcceptPet = "Tu possèdes maintenant un nouveau tour pour ton Doodle  !"
CatalogPurchaseHouseFull = "Ta maison est pleine. Tu peux acheter cet article, mais tu devras supprimer quelque chose dans ta maison pour faire de la place quand il arrivera.\n\nTu veux quand même acheter cet article ?"
CatalogAcceptHouseFull = "Ta maison est pleine. Tu dois rentrer et supprimer quelque chose dans ta maison pour faire de la place pour cet objet avant de pouvoir le sortir de la boîte aux lettres."
CatalogAcceptInAttic = "Ton nouvel article est maintenant dans ton grenier. Pour le placer dans ta maison, va à l'intérieur et clique sur le bouton \"Déplacer les meubles\"."
CatalogAcceptInAtticP = "Tes nouveaux articles sont maintenant dans ton grenier. Pour les placer dans ta maison, va à l'intérieur et clique sur le bouton \"Déplacer les meubles\"."
CatalogPurchaseMailboxFull = "Ta boîte aux lettres est pleine! Tu ne peux pas acheter cet article avant d'avoir sorti des articles de ta boîte aux lettres pour y faire de la place."
CatalogPurchaseGiftMailboxFull = "La boîte aux lettres de %s est pleine ! Tu ne peux pas acheter cet article."
CatalogPurchaseOnOrderListFull = "Tu as trop d'articles en commande actuellement. Tu ne peux pas commander d'autres articles avant que ceux que tu as déjà commandés ne soient arrivés."
CatalogPurchaseGiftOnOrderListFull = "%s a actuellement trop d'articles en commande."
CatalogPurchaseGeneralError = "L'article n'a pas pu être acheté à cause d'une erreur interne au jeu: code d'erreur %s."
CatalogPurchaseGiftGeneralError = "Le cadeau n'a pas pu être offert à ton(tes) %(friend) en raison d'une erreur interne %(error) au jeu."
CatalogPurchaseGiftNotAGift = "Cet article n'a pas pu être envoyé à %s parce qu'il n'est pas assez avancé dans le jeu."
CatalogPurchaseGiftWillNotFit = "Cet article n'a pas pu être envoyé à %s parce qu'il ne lui correspond pas."
CatalogPurchaseGiftLimitReached = "Cet article n'a pas pu être envoyé à %s parce qu'il le possède déjà."
CatalogPurchaseGiftNotEnoughMoney = "Cet article n'a pas pu être envoyé à %s parce que tu n'as pas les moyens de l'acheter."
CatalogAcceptGeneralError = "L'article n'a pas pu être retiré de ta boîte aux lettres à cause d'une erreur interne au jeu: code d'erreur %s."
CatalogAcceptRoomError = "Tu n'as pas de place pour mettre cet article. Tu vas devoir te débarasser de quelquechose."
CatalogAcceptLimitError = "Tu possèdes déjà beaucoup d'exemplaires de cet article. Tu vas devoir te débarasser de quelquechose."
CatalogAcceptFitError = "Cela ne t'ira pas ! Tu dois en faire don à un toon qui en a besoin."
CatalogAcceptInvalidError = "Cet article n'est plus à la mode. Tu dois en faire don à un toon qui en a besoin."

MailboxOverflowButtonDicard = "Supprimer"
MailboxOverflowButtonLeave = "Garder"

# don't translate yet
HDMoveFurnitureButton = "Déplacer\nles meubles"
HDStopMoveFurnitureButton = "Meubles\nplacés"
HDAtticPickerLabel = "Dans le grenier"
HDInRoomPickerLabel = "Dans la pièce"
HDInTrashPickerLabel = "À la poubelle"
HDDeletePickerLabel = "Supprimer ?"
HDInAtticLabel = "Grenier"
HDInRoomLabel = "Pièce"
HDInTrashLabel = "Poubelle"
HDToAtticLabel = "Mettre\nau grenier"
HDMoveLabel = "Déplacer"
HDRotateCWLabel = "Tourner vers la droite"
HDRotateCCWLabel = "Tourner vers la gauche"
HDReturnVerify = "Remettre cet objet dans le grenier ?"
HDReturnFromTrashVerify = "Ressortir cet objet de la poubelle et le mettre dans le grenier ?"
HDDeleteItem = "Clique sur OK pour mettre cet objet à la poubelle ou sur Annuler pour le garder."
HDNonDeletableItem = "Tu ne peux pas supprimer les objets de ce type!"
HDNonDeletableBank = "Tu ne peux pas supprimer ta tirelire!"
HDNonDeletableCloset = "Tu ne peux pas supprimer ton armoire!"
HDNonDeletablePhone = "Tu ne peux pas supprimer ton téléphone!"
HDNonDeletableNotOwner = "Tu ne peux pas supprimer les affaires de %s!"
HDHouseFull = "Ta maison est pleine. Tu dois supprimer quelque chose d'autre dans ta maison ou ton grenier avant de pouvoir ressortir cet article de la poubelle."

HDHelpDict = {
    "DoneMoving" : "Terminer la décoration de la pièce.",
    "Attic" : "Voir la liste des objets qui sont au grenier. Les objets qui ne sont pas dans ta pièce sont au grenier.",
    "Room" : "Voir la liste des objets qui sont dans la pièce. Utile pour retrouver des objets perdus.",
    "Trash" : "Voir les objets qui sont dans la poubelle. Les objets les plus anciens sont supprimés après un temps ou si la poubelle déborde.",
    "ZoomIn" : "Agrandir la vue de la pièce.",
    "ZoomOut" : "Éloigner la vue de la pièce.",
    "SendToAttic" : "Stocker le meuble actuel dans le grenier.",
    "RotateLeft" : "Tourner vers la gauche.",
    "RotateRight" : "Tourner vers la droite.",
    "DeleteEnter" : "Passer en mode suppression.",
    "DeleteExit" : "Sortir du mode suppression.",
    "FurnitureItemPanelDelete" : "Mettre %s à la poubelle.",
    "FurnitureItemPanelAttic" : "Mettre %s dans la pièce.",
    "FurnitureItemPanelRoom" : "Remettre %s au grenier.",
    "FurnitureItemPanelTrash" : "Remettre %s au grenier.",
    }

# don't translate yet
MessagePickerTitle = "Tu as trop de phrases. Pour pouvoir acheter\n\"%s\"\n tu dois choisir une chose à retirer:"
MessagePickerCancel = lCancel
MessageConfirmDelete = "Es-tu certain de vouloir retirer \"%s\" de ton menu de Chat rapide ?"

# don't translate yet
CatalogBuyText = "Acheter"
CatalogRentText = "Louer"
CatalogGiftText = "Cadeau"
CatalogOnOrderText = "En commande"
CatalogPurchasedText = "Déjà\nacheté"
CatalogGiftedText = "Offert\nà toi"
CatalogPurchasedGiftText = "Déjà\nPossédé"
CatalogMailboxFull = "Pas de place"
CatalogNotAGift = "N'est pas un cadeau"
CatalogNoFit = "ne va pas"
CatalogMembersOnly = "Réservé aux membres\n  !"
CatalogSndOnText = "Connecté"
CatalogSndOffText = "Non connecté"

CatalogPurchasedMaxText = "Maximum\ndéjà acheté"
CatalogVerifyPurchase = "Acheter %(item)s pour %(price)s bonbons?"
CatalogVerifyRent = "Louer %(item)s pour le prix de %(price)s bonbons?"
CatalogVerifyGift = "Acheter %(item)s pour %(price)s bonbons comme cadeau pour %(friend)s?"
CatalogOnlyOnePurchase = "Tu ne peux avoir qu'un de ces articles à la fois. Si tu achètes celui-là, il remplacera %(old)s.\n\nEs-tu certain(e) de vouloir acheter %(item)s pour %(price)s bonbons?"

CatalogExitButtonText = "Raccrocher"
CatalogCurrentButtonText = "Articles actuels"
CatalogPastButtonText = "Articles précédents"

TutorialHQOfficerName = "Harry du QG"

# NPCToons.py
NPCToonNames = {
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : "Tom Tuteur",
    999 : "Toon Tailleur",
    1000 : lToonHQ,
    20001 : Flippy,

    #
    # Toontown Central
    #

    # Toontown Central Playground

    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "Bob le Banquier",
    2003 : "Professeur Pete",
    2004 : "Tammy le Tailleur",
    2005 : "Larry le Libraire",
    2006 : "Vincent - Vendeur",
    2011 : "Véronique - Vendeuse",
    2007 : lHQOfficerM,
    2008 : lHQOfficerM,
    2009 : lHQOfficerF,
    2010 : lHQOfficerF,
    # NPCFisherman
    2012 : "Vendeur de l'animalerie",
    # NPCPetClerks
    2013 : "M. Vacarme",
    2014 : "Melle Vadrouille",
    2015 : "M. Vagabond",
    # NPCPartyPerson
    2016 : "Party Planner Pete",
    2017 : "Party Planner Penny",

    # Silly Street
    2101 : "Daniel le Dentiste",
    2102 : "Sherry le Shérif",
    2103 : "Kitty Lerhume",
    2104 : lHQOfficerM,
    2105 : lHQOfficerM,
    2106 : lHQOfficerF,
    2107 : lHQOfficerF,
    2108 : "Canary Minederien",
    2109 : "Souffle douleur",
    2110 : "A. Fiche",
    2111 : "Diego Ladanse",
    2112 : "Dr Tom",
    2113 : "Rollo le Magnifique",
    2114 : "Rose Dévent",
    2115 : "Dédé Coupage",
    2116 : "Costaud McDougal",
    2117 : "Madame Putride",
    2118 : "Jesse Jememoque",
    2119 : "Meryl Semarre",
    2120 : "Professeur Morderire",
    2121 : "Madame Marrante",
    2122 : "Harry Lesinge",
    2123 : "Emile Esime",
    2124 : "Gaëtan Pipourtoi",
    2125 : "Lazy Mut",
    2126 : "Professeur Lagaffe",
    2127 : "Woody Troissous",
    2128 : "Loulou Fifou",
    2129 : "Frank Fort",
    2130 : "Sylvie Brateur",
    2131 : "Jeanne Laplume",
    2132 : "Daffy Don",
    2133 : "Dr E. Phorique",
    2134 : "Simone Silence-on-tourne",
    2135 : "Marie Satourne",
    2136 : "Sal Amandre",
    2137 : "Heureux Kikomulisse",
    2138 : "Gaston",
    2139 : "Bernard Bavunpeu",
    2140 : "Billy le pêcheur",

    # Loopy Lane
    2201 : "Pierre le Postier",
    2202 : "Paul Ochon",
    2203 : lHQOfficerM,
    2204 : lHQOfficerM,
    2205 : lHQOfficerF,
    2206 : lHQOfficerF,
    2207 : "Tony Truant",
    2208 : "Nicole Lacolle",
    2209 : "Henri Gole",
    2210 : "Valérie Golotte",
    2211 : "Sally Salive",
    2212 : "Max Imum",
    2213 : "Lucy Rustine",
    2214 : "Dino Zore",
    2215 : "Jean Aimarre",
    2216 : "Lady Sparue",
    2217 : "Jones Requin",
    2218 : "Fanny Larant",
    2219 : "Lanouille",
    2220 : "Louis Leroc",
    2221 : "Tina Pachangé",
    2222 : "Electre O'Cardiogramme",
    2223 : "Sasha Touille",
    2224 : "Joe Lefumeux",
    2225 : "Toumou le pêcheur",

    # Punchline Place
    2301 : "Dr Faismarcher",
    2302 : "Professeur Tortillard",
    2303 : "Nancy Nanny",
    2304 : lHQOfficerM,
    2305 : lHQOfficerM,
    2306 : lHQOfficerF,
    2307 : lHQOfficerF,
    2308 : "Nancy Gaz",
    2309 : "Gros Bruce",
    2311 : "Frank O'Debord",
    2312 : "Dr Sensible",
    2313 : "Lucy Boulette",
    2314 : "Ned Lafronde",
    2315 : "Valérie Deveau",
    2316 : "Cindy Ka",
    2318 : "Mac Aroni",
    2319 : "Annick",
    2320 : "Alfonse Danslebrouillard",
    2321 : "Vif le pêcheur",

    #
    # Donald's Dock
    #

    # Donald's Dock Playground
    1001 : "Willy - Vendeur",
    1002 : "Billy - Vendeur",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "Alain Térieur",
    # NPCFisherman
    1008 : "Vendeur de l'animalerie",
    # NPCPetClerks
    1009 : "M. Ouahouah",
    1010 : "Melle Ronron",
    1011 : "Mme Glouglou",
    # NPCPartyPerson
    1012 : "Party Planner Phil",
    1013 : "Party Planner Patty",

    # Barnacle Boulevard
    1101 : "Sam Suffit",
    1102 : "Capitaine Carl",
    1103 : "Frank L'écaille",
    1104 : "Docteur Squale",
    1105 : "Amiral Crochet",
    1106 : "Mme Amidon",
    1107 : "Jim Nastic",
    1108 : lHQOfficerM,
    1109 : lHQOfficerF,
    1110 : lHQOfficerM,
    1111 : lHQOfficerF,
    1112 : "Gary Glouglou",
    1113 : "Anna-Lise Deussan",
    1114 : "Mick Robe",
    1115 : "Sheila Seiche, Avocate",
    1116 : "Bernard Bernache",
    1117 : "Capitaine Hautlecoeur",
    1118 : "Choppy McDougal",
    1121 : "Marthe Aupiqueur",
    1122 : "Petit Salé",
    1123 : "Electre O'Magnétique",
    1124 : "Simon Strueux",
    1125 : "Elvire Debord",
    1126 : "Barnabé le pêcheur",

    # Seaweed Street
    1201 : "Barbara Bernache",
    1202 : "Art",
    1203 : "Ahab",
    1204 : "Rocky Roc",
    1205 : lHQOfficerM,
    1206 : lHQOfficerF,
    1207 : lHQOfficerM,
    1208 : lHQOfficerF,
    1209 : "Professeur Planche",
    1210 : "Yaka Sauté",
    1211 : "Sarah Lenti",
    1212 : "Loulou Languedebois",
    1213 : "Dante Dauphin",
    1214 : "Aimé Duse",
    1215 : "Jean Peuplu",
    1216 : "Seymour Linet",
    1217 : "Cécile Savet",
    1218 : "Tim Pacifique",
    1219 : "Yvon Alot",
    1220 : "Minnie Stair",
    1221 : "McKee Labulle",
    1222 : "A. Marre",
    1223 : "Sid Seiche",
    1224 : "Anna Conda",
    1225 : "Bonzo Boitrop",
    1226 : "Ho Hisse",
    1227 : "Coral",
    1228 : "Rozo le pêcheur",

    # Lighthouse Lane
    1301 : "Ernest",
    1302 : "Ginette",
    1303 : "Gérard",
    1304 : "Hillary Varien",
    1305 : lHQOfficerM,
    1306 : lHQOfficerF,
    1307 : lHQOfficerM,
    1308 : lHQOfficerF,
    1309 : "Ecume de mer",
    1310 : "Ted Tentacule",
    1311 : "Jean Reveux",
    1312 : "Gaëtan Coque",
    1313 : "Gérard Timon",
    1314 : "Ralph Rouillé",
    1315 : "Docteur Dérive",
    1316 : "Elodie Toire",
    1317 : "Paule Pylone",
    1318 : "Barnabé Bouée",
    1319 : "David Bienosec",
    1320 : "Aldo Plate",
    1321 : "Dinah Esservi",
    1322 : "Peter Coussin",
    1323 : "Ned Savon",
    1324 : "Perle Démer",
    1325 : "Ned Setter",
    1326 : "G. Lafritte",
    1327 : "Cindy Nosore",
    1328 : "Sam Ouraille",
    1329 : "Shelly Beaucoup",
    1330 : "Icare Bonize",
    1331 : "Guy Rlande",
    1332 : "Martin le pêcheur",

    #
    # The Brrrgh
    #

    # The Brrrgh Playground
    3001 : "Angèle Ici",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "Lenny - Vendeur",
    3007 : "Penny - Vendeuse",
    3008 : "Warren Fagoté",
    # NPCPêcheur
    3009 : "Vendeur de l'animalerie",
    # NPCPetClerks
    3010 : "M. Cabo",
    3011 : "Melle Cabriole",
    3012 : "M. Cadichon",
    # NPCPartyPerson
    3013 : "Party Planner Paul",
    3014 : "Party Planner Polly",

    # Walrus Way
    3101 : "M. Lapin",
    3102 : "Tante Angèle",
    3103 : "Tanguy",
    3104 : "Bonnie",
    3105 : "Freddy Frigo",
    3106 : "Paul Poulemouillée",
    3107 : "Patty Touteseule",
    3108 : "Ted Tobogan",
    3109 : "Patricia",
    3110 : "Jack Pot",
    3111 : "O. Tain",
    3112 : "Allan Bic",
    3113 : "Harry Hystérique",
    3114 : "Nathan Pastrop",
    3115 : lHQOfficerM,
    3116 : lHQOfficerF,
    3117 : lHQOfficerM,
    3118 : lHQOfficerM,
    3119 : "Carl Magne",
    3120 : "Mike Mouffles",
    3121 : "Joe Courant",
    3122 : "Lucy Luge",
    3123 : "Nicole Apon",
    3124 : "Lance Iceberg",
    3125 : "Colonel Mâchetout",
    3126 : "Colette Erol",
    3127 : "Alex Térieur",
    3128 : "George Lacolle",
    3129 : "Brigitte Boulanger",
    3130 : "Sandy",
    3131 : "Pablo Paresseux",
    3132 : "Braise Cendrar",
    3133 : "Dr Jevoismieux",
    3134 : "Sébastien Toutseul",
    3135 : "Nelly Quéfié",
    3136 : "Claude Iqué",
    3137 : "M. Gel",
    3138 : "M. Empoté",
    3139 : "Virginie Aimaitropaul",
    3140 : "Lucile la pêcheuse",

    # Sleet Street
    3201 : "Tante Artique",
    3202 : "Tremblotte",
    3203 : "Walt",
    3204 : "Dr Ivan Deslunettes",
    3205 : "Boris Tourne",
    3206 : "Victoire Alarraché",
    3207 : "Dr Marmotter",
    3208 : "Phil Electrique",
    3209 : "Geoffroy Auxmains",
    3210 : "Sam Simiesque",
    3211 : "Gaelle Segèle",
    3212 : "Freddy Frigo",
    3213 : lHQOfficerM,
    3214 : lHQOfficerF,
    3215 : lHQOfficerM,
    3216 : lHQOfficerM,
    3217 : "Pierre Lasueur",
    3218 : "Lou Minaire",
    3219 : "Tom Tandem",
    3220 : "G. Ternue",
    3221 : "Nelly Neige",
    3222 : "Moricette Decuisine",
    3223 : "Chappy",
    3224 : "Agnes Kimo",
    3225 : "Frimas Ladouce",
    3226 : "Prospère Noël",
    3227 : "Ray Ondesoleil",
    3228 : "Maurice Quetout",
    3229 : "Hernie Discale",
    3230 : "Benjy Boule-à-zéro",
    3231 : "Choppy",
    3232 : "Albert le pêcheur",

 #Polar Place
    3301 : "Cathou Coupet",
    3302 : "Bjorn Bord",
    3303 : "Dr Flic-Flac",
    3304 : "Eddie le Yéti",
    3305 : "Mac Ramée",
    3306 : "Paul Hère",
    # NPC Fisherman
    3307 : "Pêcheuse Frédérique",
    3308 : "Marcel Glassault",
    3309 : "Théo Citron",
    3310 : "Professeur Flocon",
    3311 : "Cella Glasse",
    3312 : "J. Boulet de Mars",
    3313 : lHQOfficerM,
    3314 : lHQOfficerF,
    3315 : lHQOfficerM,
    3316 : lHQOfficerF,
    3317 : "Chris Crisse",
    3318 : "Alan Sthiver",
    3319 : "Bo Nedlaine",
    3320 : "Lisette Frisquette",
    3321 : "Cédric Piolet",
    3322 : "Corinne Za",
    3323 : "Aurore Beau-Réal",
    3324 : "Mandra Gore",
    3325 : "Alban Quise",
    3326 : "Blanche",
    3327 : "J. Gault",
    3328 : "Rémi Taine",
    3329 : "Isaure Betière",

    #
    # Minnie's Melody Land
    #

    # Minnie's Melody Land Playground
    4001 : "Molly Masson",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "Doe - Vendeur",
    4007 : "Ray - Vendeur",
    4008 : "Bernard Mony",
    # NPCFisherman
    4009 : "Vendeur de l'animalerie",
    # NPCPetClerks
    4010 : "M. Chris",
    4011 : "M. Neil",
    4012 : "Melle Western",
    # NPCPartyPerson
    4013 : "Party Planner Preston",
    4014 : "Party Planner Penelope",

    # Alto Ave.
    4101 : "Tom",
    4102 : "Fifi",
    4103 : "Dr Tefaispasdebile",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "Clément de Sol",
    4109 : "Carlos",
    4110 : "Métro Gnome",
    4111 : "Adam Levent",
    4112 : "Fa",
    4113 : "Madame Manière",
    4114 : "Eric Ochet",
    4115 : "Labelle Decadix",
    4116 : "Piccolo",
    4117 : "Mandy Lynn",
    4118 : "André Sansfrapper",
    4119 : "Moe Zart",
    4120 : "Viola Coussin",
    4121 : "Ray Mineur",
    4122 : "Armanthe Réglisse",
    4123 : "Ted l'éclair",
    4124 : "Riff Iffifi",
    4125 : "Mélodie Dantan",
    4126 : "Bel Canto",
    4127 : "Amédé Chausson",
    4128 : "Luciano Lescoop",
    4129 : "Terry Golo",
    4130 : "Rémi Crophone",
    4131 : "Abraham Armoire",
    4132 : "Sally Tristounet",
    4133 : "D. Taché",
    4134 : "Dave Disco",
    4135 : "Séraphin Ducompte",
    4136 : "Patty Pause",
    4137 : "Tony Doiseau",
    4138 : "Rémi Depain",
    4139 : "Harmony Ka",
    4140 : "Ned Maladroit",
    4141 : "Jojo le pêcheur",

    # Baritone Blvd.
    4201 : "Tina",
    4202 : "Barry",
    4203 : "Jack Bûcheron",
    4204 : lHQOfficerM,
    4205 : lHQOfficerF,
    4206 : lHQOfficerF,
    4207 : lHQOfficerF,
    4208 : "Elise",
    4209 : "Mo Végou",
    4211 : "Carl Concerto",
    4212 : "Funeste Funèbre",
    4213 : "Fran Chement",
    4214 : "Tina Crampon",
    4215 : "Tim Rouletroprès",
    4216 : "K. Outchouc",
    4217 : "Anton Beaugarçon",
    4218 : "Vanessa Vapasdutout",
    4219 : "Sid Sonate",
    4220 : "Jean-Bière",
    4221 : "Moe Madrigal",
    4222 : "John Deuf",
    4223 : "Penny Souffleur",
    4224 : "Jim Jongle",
    4225 : "Holly Stérie",
    4226 : "Georgina Gorge",
    4227 : "Francesca Taphonique",
    4228 : "August Ave",
    4229 : "June Comprendsrien",
    4230 : "Julius Césure",
    4231 : "Steffi Nalise",
    4232 : "Marie Toivite",
    4233 : "Charlie Lacarpe",
    4234 : "Guy Tare",
    4235 : "Larry le pêcheur",

    # Tenor Terrace
    4301 : "Yuki",
    4302 : "Anna",
    4303 : "Léo",
    4304 : lHQOfficerM,
    4305 : lHQOfficerF,
    4306 : lHQOfficerF,
    4307 : lHQOfficerF,
    4308 : "Tabatha",
    4309 : "Mémé Chignon",
    4310 : "Marthe Ingale",
    4311 : "Charlie Mande",
    4312 : "Ma Sage",
    4313 : "Muget Muet",
    4314 : "Dino Dodo",
    4315 : "Karen Rouages",
    4316 : "Tim Tango",
    4317 : "Sue Bitto",
    4318 : "Bob Marlin",
    4319 : "K. Zou",
    4320 : "Camille Cloda",
    4321 : "Luky Luth",
    4322 : "Henry Thme",
    4323 : "Hanna Purna",
    4324 : "Ellie",
    4325 : "Braque Labanque",
    4326 : "Jonathan Plurien",
    4327 : "Flim Flam",
    4328 : "Wagner",
    4329 : "Tyler Prompteur",
    4330 : "Quentin",
    4331 : "M. Costello",
    4332 : "Ziggy",
    4333 : "Harry",
    4334 : "Freddie Fastoche",
    4335 : "Serge le pêcheur",

    #
    # Daisy Gardens
    #

    # Daisy Gardens Playground
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "Prune - Vendeuse",
    5006 : "Rose - Vendeuse",
    5007 : "Bonnie Menteuse",
    # NPCFisherman
    5008 : "Vendeur de l'animalerie",
    # NPCPetClerks
    5009 : "Mme Flore Halie",
    5010 : "M. Tom Hatte",
    5011 : "M. Ray Glisse",
    # NPCPartyPerson
    5012 : "Party Planner Pierce",
    5013 : "Party Planner Peggy",

    # Elm Street
    5101 : "Eugène",
    5102 : "Susan",
    5103 : "Piaf",
    5104 : "Parpaillon",
    5105 : "Jack",
    5106 : "Bjorn le Barbier",
    5107 : "Felipe le Postier",
    5108 : "Janette l'Aubergiste",
    5109 : lHQOfficerM,
    5110 : lHQOfficerM,
    5111 : lHQOfficerF,
    5112 : lHQOfficerF,
    5113 : "Dr Lacouenne",
    5114 : "Affaiblissement",
    5115 : "Rosée Dumatin",
    5116 : "R. Noncule",
    5117 : "Pétale",
    5118 : "Victor Nemuse",
    5119 : "Barry Dicule",
    5120 : "La taupe",
    5121 : "Paula Roïd",
    5122 : "A. Masse",
    5123 : "Diane Avecnouscesoir",
    5124 : "Chen Avélo",
    5125 : "A. Sperge",
    5126 : "Madame Mère",
    5127 : "Polly Pollène",
    5128 : "Salma Range",
    5129 : "Sally la pêcheuse",

    # Maple Street
    5201 : "Jacquot",
    5202 : "Cynthia",
    5203 : "Citronelle",
    5204 : "Bert",
    5205 : "Omar Souin",
    5206 : "Ray Zainblanc",
    5207 : "Sophie Stiquée",
    5208 : "Samantha Pir",
    5209 : lHQOfficerM,
    5210 : lHQOfficerM,
    5211 : lHQOfficerF,
    5212 : lHQOfficerF,
    5213 : "Gros Balourd",
    5214 : "Sam Gratte",
    5215 : "Henry Chisson",
    5216 : "Jim Lassenteur",
    5217 : "Walter Ego",
    5218 : "Rocky Groseille",
    5219 : "Mo Viette",
    5220 : "Adam Telle",
    5221 : "Flamant rose",
    5222 : "Pétronille Hiliste",
    5223 : "Marc Assin",
    5224 : "Oncle Balourd",
    5225 : "Pamela Asaplace",
    5226 : "Pierre Mousse",
    5227 : "B. Gonia",
    5228 : "Avi Dité",
    5229 : "Lili la pêcheuse",

    # Oak street
    5301 : lHQOfficerM,
    5302 : lHQOfficerM,
    5303 : lHQOfficerM,
    5304 : lHQOfficerM,
    5305 : "Crystelle",
    5306 : "S. Cargot",
    5307 : "Cyril Semarre",
    5308 : "Nell Ronchon",
    5309 : "Romaine",
    5310 : "Thimothé",
    5311 : "Jonas Ticot",
    5312 : "Eugène",
    5313 : "Zucchini l'entraîneur",
    5314 : "Merlin Sect",
    5315 : "Oncle Boueux",
    5316 : "Oncle Patapouf",
    5317 : "Lima, détective",
    5318 : "César",
    5319 : "Rose",
    5320 : "J. Boulée",
    5321 : "Professeur Chèvrefeuille",
    5322 : "Rose la pêcheuse",

    #
    # Goofy's Speedway
    #

    #default  area
    #kart clerk
    8001 : "Benjamin Salor",
    8002 : "Yvon Affond-Lacaisse",
    8003 : "Emma Nicourt",
    8004 : "Phil Assent",

    #
    # Dreamland
    #

    # Dreamland Playground
    9001 : "Mélusine Enfaillite",
    9002 : "Tom Pouce",
    9003 : "Denis Doiseau",
    9004 : lHQOfficerF,
    9005 : lHQOfficerF,
    9006 : lHQOfficerM,
    9007 : lHQOfficerM,
    9008 : "Jill - Vendeuse",
    9009 : "Phil - Vendeur",
    9010 : "U. Zure",
    # NPCFisherman
    9011 : "Vendeur de l'animalerie",
    # NPCPetClerks
    9012 : "Melle Isabelle Bulle",
    9013 : "Mme Dorothée Dor",
    9014 : "M. Pierre Pionce",
    # NPCPartyPerson
    9015 : "Party Planner Patrick",
    9016 : "Party Planner Pearl",

    # Lullaby Lane
    9101 : "Ed",
    9102 : "Big Mama",
    9103 : "P. J.",
    9104 : "Fay Debeauxrêves",
    9105 : "Professeur Baillebeaucoup",
    9106 : "Max",
    9107 : "Câline",
    9108 : "Matt Heula",
    9109 : "Daphné Puisé",
    9110 : "Kathy Mini",
    9111 : "Ali Mentation",
    9112 : "Lou Laberceuse",
    9113 : "Jacques Horloge",
    9114 : "Emma Scara",
    9115 : "Bébé MacDougal",
    9116 : "Celui qui danse avec les moutons",
    9117 : "Sam Suffit",
    9118 : "Stella Lune",
    9119 : "Rocco",
    9120 : "Aron Flebeaucoup",
    9121 : "Serena Dàlanuitombée",
    9122 : "Serge Souslesyeux",
    9123 : "Teddy Blaireau",
    9124 : "Nina Lamparo",
    9125 : "Dr Chassieux",
    9126 : "Thérèse Eveillé",
    9127 : "Tabby Tude",
    9128 : "Amédé Brouilletoitoutseul",
    9129 : "Amélie Decamp",
    9130 : "Paul Potdechambre",
    9131 : "Susan Sieste",
    9132 : lHQOfficerF,
    9133 : lHQOfficerF,
    9134 : lHQOfficerF,
    9135 : lHQOfficerF,
    9136 : "Titine la pêcheuse",

    # Pajama Place
    9201 : "Nesdor",
    9202 : "Orville",
    9203 : "Plume",
    9204 : "Claire de Moune",
    9205 : "Olivier Daure",
    9206 : "Phèdre Don",
    9207 : "Sacha Lumea",
    9208 : "Dave Bigleau",
    9209 : "Dr Drin",
    9210 : "Mike Mac",
    9211 : "Aurore",
    9212 : "Phœbe Lancre",
    9213 : "Fortuné Dargent",
    9214 : "Dr Ouffe",
    9215 : "Honoré",
    9216 : "Tartine",
    9217 : "Linda Kapok",
    9218 : "Rita Thasse",
    9219 : "La comtesse",
    9220 : "Matt Thuvu",
    9221 : "Père San",
    9222 : "Ron Chonneau",
    9223 : "Fay Dodeau",
    9224 : "Sandie Marchand",
    9225 : "Élodie Dont",
    9226 : "Laurent Lauronpat",
    9227 : "Édouard Sagrate",
    9228 : "Michu Chotte",
    9229 : "Eva Sandor-Mir",
    9230 : "Pierrot",
    9231 : "Léo Galleau",
    9232 : "Rosée de Lune",
    9233 : lHQOfficerM,
    9234 : lHQOfficerM,
    9235 : lHQOfficerM,
    9236 : lHQOfficerM,
    9237 : "S. André",

    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# These building titles are output from the DNA files
# Run ppython $TOONTOWN/src/dna/DNAPrintTitles.py to generate this list
# DO NOT EDIT THE ENTRIES HERE -- EDIT THE ORIGINAL DNA FILE
zone2TitleDict = {
    # titles for: phase_4/dna/toontown_central_sz.dna
    2513 : ("Mairie de Toontown", ""),
    2514 : ("Banque de Toontown", ""),
    2516 : ("Ecole de Toontown", ""),
    2518 : ("Bibliothèque de Toontown", ""),
    2519 : ("Boutique à gags", ""),
    2520 : ("Quartier Général des Toons", ""),
    2521 : ("Boutique de prêt-à-porter", ""),
    2522 : ("ANIMALERIE", ""),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("Tout-sourire - Réparations dentaires", ""),
    2602 : ("", ""),
    2603 : ("Mineurs Pince-sans-rire", ""),
    2604 : ("Qui vivra, verrat", ""),
    2605 : ("Usine à pancartes de Toontown", ""),
    2606 : ("", ""),
    2607 : ("Haricots sauteurs", ""),
    2610 : ("Dr. Tom Lepitre", ""),
    2611 : ("", ""),
    2616 : ("Barbefolle - Déguisements", ""),
    2617 : ("Cascades Comiques", ""),
    2618 : ("Nouba & Co", ""),
    2621 : ("Avions en papier", ""),
    2624 : ("Aux joyeux hooligans", ""),
    2625 : ("La maison du pâté raté", ""),
    2626 : ("Chez Jesse - Réparation de blagues", ""),
    2629 : ("Le coin du rire", ""),
    2632 : ("L'école des clowns", ""),
    2633 : ("Thé-hier - Salon de thé", ""),
    2638 : ("Théâtre de Toontown", ""),
    2639 : ("Monnaie de singe", ""),
    2643 : ("Bouteilles en boîte", ""),
    2644 : ("Farces farcies", ""),
    2649 : ("Magasin de jeux", ""),
    2652 : ("", ""),
    2653 : ("", ""),
    2654 : ("Leçons de rire", ""),
    2655 : ("Drôle d'argent - Caisse d'épargne", ""),
    2656 : ("Voitures de clown d'occasion", ""),
    2657 : ("Pirouettes de Pierrette", ""),
    2659 : ("L'univers des vibrateurs", ""),
    2660 : ("Machines à chatouilles", ""),
    2661 : ("Daffy Taffy", ""),
    2662 : ("Dr E. Phorique", ""),
    2663 : ("Théâtre de Toontown", ""),
    2664 : ("Les mimes marrants", ""),
    2665 : ("Le Manège - Agence de voyages", ""),
    2666 : ("Bouteilles de gaz hilarant", ""),
    2667 : ("Au bon temps", ""),
    2669 : ("Chez Gaston - ballons pas folichons", ""),
    2670 : ("Fourchettes à soupe", ""),
    2671 : ("Quartier Général des Toons", ""),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("Théâtre de Toontown", ""),
    2705 : ("Tony Truant - Bruits en tout genre", ""),
    2708 : ("Colle bleue", ""),
    2711 : ("Bureau de poste de Toontown", ""),
    2712 : ("Café des gloussements", ""),
    2713 : ("Café du rire", ""),
    2714 : ("Théâtre de Toontown", ""),
    2716 : ("Dr Ãle de soupe", ""),
    2717 : ("Boîtes en bouteille", ""),
    2720 : ("Plaies et Bosses - Réparations de voitures", ""),
    2725 : ("", ""),
    2727 : ("Bouteilles et boîtes Selter", ""),
    2728 : ("Crème de jour évanescente", ""),
    2729 : ("Ornithorynques 14 carats", ""),
    2730 : ("La gazette du rire", ""),
    2731 : ("", ""),
    2732 : ("Spaghettis et barbituriques", ""),
    2733 : ("Cerf-volants en fonte", ""),
    2734 : ("Tasses et soucoupes volantes", ""),
    2735 : ("Le Pétard mouillé", ""),
    2739 : ("Réparation de fous rires", ""),
    2740 : ("Pétards d'occasion", ""),
    2741 : ("", ""),
    2742 : ("Quartier Général des Toons", ""),
    2743 : ("", ""),
    2744 : ("", ""),
    2747 : ("Encre visible", ""),
    2748 : ("Rions un peu", ""),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("Coussins sonores", ""),
    2802 : ("Boulets de démolition gonflables", ""),
    2803 : ("Théâtre de Toontown", ""),
    2804 : ("Dr. Faismarcher, chiropracteur", ""),
    2805 : ("", ""),
    2809 : ("Salle de gym Le Poids lent", ""),
    2814 : ("Théâtre de Toontown", ""),
    2818 : ("Au pâté volant", ""),
    2821 : ("", ""),
    2822 : ("Sandwichs au poulet synthétique", ""),
    2823 : ("Glaces hilarantes", ""),
    2824 : ("Cinéma des blagues", ""),
    2829 : ("Balivernes", ""),
    2830 : ("Les piques d'Annick", ""),
    2831 : ("La maison du rire du professeur Tortillard", ""),
    2832 : ("Quartier Général des Toons", ""),
    2833 : ("", ""),
    2834 : ("Salle des urgences des morts de rire", ""),
    2836 : ("", ""),
    2837 : ("Hardi - Séminaires", ""),
    2839 : ("A la nouille amère", ""),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : ("Boutique à gags", ""),
    1507 : ("Quartier Général des Toons", ""),
    1508 : ("Boutique de prêt-à-porter", ""),
    1510 : ("ANIMALERIE", ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("Gilets de sauvetage d'occasion", ""),
    1604 : ("Costumes de bain - Nettoyage à sec", ""),
    1606 : ("Crochet - Réparation d'horloges", ""),
    1608 : ("Le Lof", ""),
    1609 : ("A l'appât rance", ""),
    1612 : ("Banque Sixsous", ""),
    1613 : ("La Pieuvre, cabinet d'avocats", ""),
    1614 : ("Toutes voiles devant - Boutique", ""),
    1615 : ("Yatch qu'à demander!", ""),
    1616 : ("Barbe Noire - Salon de beauté", ""),
    1617 : ("La mer à voir - Opticien", ""),
    1619 : ("L'écorcaire - Chirurgie arboricole", ""),
    1620 : ("Babord-tribord", ""),
    1621 : ("Salle de gym La poupe", ""),
    1622 : ("Gymnote - Electricité générale", ""),
    1624 : ("Réparation de couteaux et de peignes", ""),
    1626 : ("La perche rare - Tenues de soirée", ""),
    1627 : ("La cabane de Sam Suffit", ""),
    1628 : ("Accordeur de thons", ""),
    1629 : ("Quartier Général des Toons", ""),
    # titles for: phase_6/dna/donalds_dock_1200.dna
    1701 : ("Ecole maternelle des p'tits loups", ""),
    1703 : ("Bar Accuda - Restaurant chinois", ""),
    1705 : ("Voiles à vendre", ""),
    1706 : ("La méduse médusée", ""),
    1707 : ("C'est assez - Boutique de cadeaux", ""),
    1709 : ("Gélée de méduse", ""),
    1710 : ("La belle bernache", ""),
    1711 : ("Restaurant de la pleine mer", ""),
    1712 : ("Salle de gymnote", ""),
    1713 : ("Chez Art - Cartes en tous genres", ""),
    1714 : ("Auberge du moulinet", ""),
    1716 : ("Maillots de bains pour sirènes", ""),
    1717 : ("Mi pacifique, mi raisin", ""),
    1718 : ("Société de taxi le Naufrage", ""),
    1719 : ("Société Je m'cache à l'eau", ""),
    1720 : ("Au requin malin", ""),
    1721 : ("Tout pour la mer", ""),
    1723 : ("Au royaume des algues", ""),
    1724 : ("Au mérou amoureux", ""),
    1725 : ("J'en pince pour toi - Crabes frais", ""),
    1726 : ("Bière à flots", ""),
    1727 : ("Je rame pour vous", ""),
    1728 : ("Limules porte-bonheur", ""),
    1729 : ("Quartier Général des Toons", ""),
    # titles for: phase_6/dna/donalds_dock_1300.dna
    1802 : ("Les petits péchés", ""),
    1804 : ("Salle de gym Les mollusques", ""),
    1805 : ("Un petit ver pour le déjeuner", ""),
    1806 : ("Toucoule - Chapelier", ""),
    1807 : ("Coûte que soute", ""),
    1808 : ("Appât si vite!", ""),
    1809 : ("Seaux rouillés", ""),
    1810 : ("L'ancre noire", ""),
    1811 : ("Mérou tu vas chercher tout ça?", ""),
    1813 : ("A mâts couverts, conseiller", ""),
    1814 : ("Le Ho Hisse", ""),
    1815 : ("Quoi de neuf dockteur ?", ""),
    1818 : ("Café des sept mers", ""),
    1819 : ("Au dîner des dockers", ""),
    1820 : ("L'hameçon gobé - Farces et attrapes", ""),
    1821 : ("Chez Neptoon", ""),
    1823 : ("A la pomme de mât", ""),
    1824 : ("Au chien pas gai", ""),
    1825 : ("Le hareng sort! Marché aux poissons", ""),
    1826 : ("Le placard de Gérard", ""),
    1828 : ("Palais du lest d'Ernest", ""),
    1829 : ("Merlan l'enchanteur", ""),
    1830 : ("O sole et mio - Objets trouvés", ""),
    1831 : ("Une perle à domicile", ""),
    1832 : ("Supérette La Goélette", ""),
    1833 : ("Costumes pour gaillards d'avant", ""),
    1834 : ("Tranchement ridicule!", ""),
    1835 : ("Quartier Général des Toons", ""),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : ("Boutique à gags", ""),
    4504 : ("Quartier Général des Toons", ""),
    4506 : ("Boutique de prêt-à-porter", ""),
    4508 : ("ANIMALERIE", ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Tom-Tom - Tambours", ""),
    4604 : ("A quatre temps", ""),
    4605 : ("Fifi - Violons d'Ingres", ""),
    4606 : ("La case des castagnettes", ""),
    4607 : ("Vêtements Toon branchés", ""),
    4609 : ("Dot, Raie, Mie - Pianos", ""),
    4610 : ("Attention refrain!", ""),
    4611 : ("Diapasons à l'unisson", ""),
    4612 : ("Dr. Tefaispasdebile - Dentiste", ""),
    4614 : ("On rase gratis pour une chanson", ""),
    4615 : ("Pizzéria chez Piccolo", ""),
    4617 : ("La mandoline joyeuse", ""),
    4618 : ("Salles des césures", ""),
    4619 : ("En avant la musique!", ""),
    4622 : ("Oreillers à mentonnière", ""),
    4623 : ("Bémols à la dièse", ""),
    4625 : ("Tuba de dentifrice", ""),
    4626 : ("Notations", ""),
    4628 : ("Assurance accidentelle", ""),
    4629 : ("Riff - Assiettes en papier", ""),
    4630 : ("La musique est notre force", ""),
    4631 : ("Canto de vous connaître!", ""),
    4632 : ("Boutique de la danse des heures", ""),
    4635 : ("Le quotidien des cantatrices", ""),
    4637 : ("Pour la bonne mesure", ""),
    4638 : ("Boutique Hard Rock", ""),
    4639 : ("Les quatre saisons - Antiquités", ""),
    4641 : ("L'actualité du yéyé", ""),
    4642 : ("D. Taché - Nettoyage à sec", ""),
    4645 : ("Club 88", ""),
    4646 : ("", ""),
    4648 : ("Le Toon siffleur - Déménageurs", ""),
    4649 : ("Quartier Général des Toons", ""),
    4652 : ("Boutique des doubles-croches", ""),
    4653 : ("", ""),
    4654 : ("Haut perché - Toitures", ""),
    4655 : ("La clé de sol - Ecole de cuisine", ""),
    4656 : ("", ""),
    4657 : ("Quatuor du barbier", ""),
    4658 : ("Pianos en chute libre", ""),
    4659 : ("Quartier Général des Toons", ""),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("L'eau de rose - Ecole de valse", ""),
    4702 : (" Timbre de bois - Fournitures pour bûcherons", ""),
    4703 : ("Gros Bizet à tous!", ""),
    4704 : ("Tina - Concerts de concertina", ""),
    4705 : ("Il est déjà cithare ?", ""),
    4707 : ("Studio d'effets sonores Doppler", ""),
    4709 : ("Pirouettes - Magasin d'alpinisme", ""),
    4710 : ("Polka tu routes si vite ? Auto-école", ""),
    4712 : ("Mets un bémol! Réparation de pneus", ""),
    4713 : ("Dos dièse - Vêtements de luxe pour hommes", ""),
    4716 : ("Harmonicas à quatre voix", ""),
    4717 : ("Sonate pas ta faute! Assurance automobile", ""),
    4718 : ("Chopins de bière et autres ustensiles de cuisine", ""),
    4719 : ("Camping-cars Madrigal", ""),
    4720 : ("Le bon Toon", ""),
    4722 : ("Doublures pour ouvertures", ""),
    4723 : ("Bach à toi! Jeux et balançoires", ""),
    4724 : ("(Cale)sons blancs pour filles et garçons", ""),
    4725 : ("Le barbier baryton", ""),
    4727 : ("Cordes vocales tressées", ""),
    4728 : ("Chante en sourdine!", ""),
    4729 : ("Librairie J'aime lyre", ""),
    4730 : ("Lettre à un pou", ""),
    4731 : ("Des Toons de bon ton", ""),
    4732 : ("Etude brute ? Troupe de théâtre", ""),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("Soufflet pour accordéons", ""),
    4736 : ("Hyminent - Préparatifs de mariage", ""),
    4737 : ("Harpe Hônneur", ""),
    4738 : ("Mécanique cantique - Cadeaux", ""),
    4739 : ("Quartier Général des Toons", ""),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("Crêp'chignon", ""),
    4803 : ("Quelle Mezzo! Service de domestiques", ""),
    4804 : ("Ecole myxolidienne pour serveurs de barres", ""),
    4807 : ("Massage des Brahms et des jambes", ""),
    4809 : ("C'est une cata-strophe!", ""),
    4812 : ("", ""),
    4817 : ("Magasin d'animaux ternaires", ""),
    4819 : ("Chez Yuki - Ukélélés", ""),
    4820 : ("", ""),
    4821 : ("Chez Anna - Croisières", ""),
    4827 : ("Montres Lamesure", ""),
    4828 : ("Ravel - Réveils et horloges", ""),
    4829 : ("Chez Pachelbel - Obus pour canons et fugues", ""),
    4835 : ("Ursatz pour Kool Katz", ""),
    4836 : ("Reggae royal", ""),
    4838 : ("Ecole de kazoologie", ""),
    4840 : ("Coda Pop - Boissons musicales", ""),
    4841 : ("Lyre et Lyre", ""),
    4842 : ("Société Lasyncope", ""),
    4843 : ("", ""),
    4844 : ("Moto - deux roues", ""),
    4845 : ("Les élégies élégantes d'Ellie", ""),
    4848 : ("De haute luth - Caisse d'épargne", ""),
    4849 : ("", ""),
    4850 : ("L'accord emprunté - Prêteur sur gages", ""),
    4852 : ("Flasques fleuries pour flûtes", ""),
    4853 : ("Chez Léo - Garde-feu", ""),
    4854 : ("Chez Wagner - Vidéos de violons voilés", ""),
    4855 : ("Réseau de radeau-diffusion", ""),
    4856 : ("", ""),
    4862 : ("Les quadrilles quintessencielles de Quentin", ""),
    4867 : ("M. Costello - Kazoos à gogo", ""),
    4868 : ("", ""),
    4870 : ("Chez Ziggy - Zoo et Zigeunermusik", ""),
    4871 : ("Chez Harry - Harmonies harmonieuses", ""),
    4872 : ("Freddie Fastoche - Touches de piano", ""),
    4873 : ("Quartier Général des Toons", ""),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : ("Boutique à gags", ""),
    5502 : ("Quartier Général des Toons", ""),
    5503 : ("Boutique de prêt-à-porter", ""),
    5505 : ("ANIMALERIE", ""),
    # titles for: phase_8/dna/daisys_garden_5100.dna
    5601 : ("L'œil de bouillon - Optométrie", ""),
    5602 : ("Eugène Coulissant - Cravates", ""),
    5603 : ("Arrête tes salades!", ""),
    5604 : ("Gai, gai, marions-les!", ""),
    5605 : ("Sols et meubles", ""),
    5606 : ("Pétales", ""),
    5607 : ("Bureau de composte", ""),
    5608 : ("Pop corn yéyé", ""),
    5609 : ("La baie au trésor", ""),
    5610 : ("L'œil au beurre noir - Cours de boxe", ""),
    5611 : ("Les gags de la Taupe", ""),
    5613 : ("La meule à zéro - Barbier", ""),
    5615 : ("Chez Piaf - Graines pour oiseaux", ""),
    5616 : ("Auberge de la goutte", ""),
    5617 : ("Chez Parpaillon - Papillons", ""),
    5618 : ("Deux pois deux mesures", ""),
    5619 : ("Chez Jack - Haricots géants", ""),
    5620 : ("Auberge du rateau", ""),
    5621 : ("La critique du Raisin pur", ""),
    5622 : ("La petite reine - claude - Bicyclettes", ""),
    5623 : ("Bains moussants pour oiseaux", ""),
    5624 : ("Ecoute ta mère", ""),
    5625 : ("Dur de la feuille", ""),
    5626 : ("Travaux d'aiguille (de pin)", ""),
    5627 : ("Quartier Général des Toons", ""),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Le bambou du tunnel", ""),
    5702 : ("Les rateaux de Jacquot", ""),
    5703 : ("Cynthia - Magasin de photosynthèses", ""),
    5704 : ("Citronelle Citron - Voitures d'occasion", ""),
    5705 : ("Meubles en herbe à puce", ""),
    5706 : (" 14 carottes - Bijoutiers", ""),
    5707 : ("Fruit musical", ""),
    5708 : ("Sans soucis - Agence de voyages", ""),
    5709 : ("Astroturf - Tondeuses", ""),
    5710 : ("Gym des narcisses", ""),
    5711 : ("Bonneterie de jardin", ""),
    5712 : ("Statues squottes", ""),
    5713 : ("Buis clos", ""),
    5714 : ("Bouteilles d'eau de roche", ""),
    5715 : ("La Meule nouvelle", ""),
    5716 : ("Qui s'y frotte s'y pique - Prêteur sur gages", ""),
    5717 : ("La fleur qui mouille", ""),
    5718 : ("Le chèvre-feuille - Animalerie", ""),
    5719 : ("Sauge d'une nuit d'été - Détective privé", ""),
    5720 : ("La feuille de vigne - Prêt-à-porter masculin", ""),
    5721 : ("Routabaga 66 - Restaurant", ""),
    5725 : ("Boutique du grain d'orge", ""),
    5726 : ("Bert", ""),
    5727 : ("Le trou sans fond - Caisse d'épargne", ""),
    5728 : ("Quartier Général des Toons", ""),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : ("Quartier Général des Toons", ""),
    5804 : ("La vase de Soisson", ""),
    5805 : ("Le cerveau lent", ""),
    5809 : ("Drôle d'oiseau - Ecole de clowns", ""),
    5810 : ("Ca ne rom à rain!", ""),
    5811 : ("Auberge Inn", ""),
    5815 : ("Des racines & des herbes", ""),
    5817 : ("Pommes et oranges", ""),
    5819 : ("Pantalons vert citron", ""),
    5821 : ("Centre de squash", ""),
    5826 : ("Matériel d'élevage de fourmis", ""),
    5827 : ("Terre bon marché", ""),
    5828 : ("Meubles Molasson", ""),
    5830 : ("Vide ton sac (de patates)", ""),
    5833 : ("Bar à salades", ""),
    5835 : ("Séjour en pots chez l'habitant", ""),
    5836 : ("Salles de bain J. Boulée", ""),
    5837 : ("L'école de la vigne", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Bibliothèque des berceuses", ""),
    9503 : ("Bar du roupillon", ""),
    9504 : ("Boutique à gags", ""),
    9505 : ("Quartier Général des Toons", ""),
    9506 : ("Boutique de prêt-à-porter", ""),
    9508 : ("ANIMALERIE", ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Auberge des câlins", ""),
    9602 : ("Sommes au rabais", ""),
    9604 : ("Chez Ed - Edredons redondants", ""),
    9605 : ("Confection de bonnets de nuit", ""),
    9607 : ("Big Mama - Pyjamas des Bahamas", ""),
    9608 : ("Quand le chat dort, les souris dansent", ""),
    9609 : ("Roupillon pour trois ronds", ""),
    9613 : ("Théâtre du pays des rêves", ""),
    9616 : ("La veilleuse - Electricité générale", ""),
    9617 : ("L'enfant do - Petites musiques de nuit", ""),
    9619 : ("Relax Max", ""),
    9620 : ("PJ - Service de taxi", ""),
    9622 : ("Horloges du sommeil", ""),
    9625 : ("Histoire en boucle - Salon de beauté", ""),
    9626 : ("Histoiries Dodo", ""),
    9627 : ("Le tipi endormi", ""),
    9628 : ("Sam Suffit - Calendriers", ""),
    9629 : ("À l'édredon d'argent", ""),
    9630 : ("Marchand de sable", ""),
    9631 : ("Temps d'arrêt - Horloger", ""),
    9633 : ("Théâtre du pays des réves", ""),
    9634 : ("Je ronfle, donc je suis", ""),
    9636 : ("Assurance pour insomniaques", ""),
    9639 : ("Maison de l'hibernation", ""),
    9640 : ("Nous meublons vos rêves", ""),
    9642 : ("A la sciure de mon front", ""),
    9643 : ("Les yeux clos - Optométrie", ""),
    9644 : ("Combats d'oreillers nocturnes", ""),
    9645 : ("Auberge Viensmeborder", ""),
    9647 : ("Fais ton lit! Magasin de bricolage", ""),
    9649 : ("Bonnet blanc et blanc bonnet", ""),
    9650 : ("Réparateur de soupirs", ""),
    9651 : ("La vie est un ronflement tranquille", ""),
    9652 : ("Quartier Général des Toons", ""),
    # titles for: phase_8/dna/donalds_dreamland_9200.dna
    9703 : ("Agence de voyages Vol de Nuit", ""),
    9704 : ("Animalerie du Hibou", ""),
    9705 : ("Garage de la Panne d'Oreiller", ""),
    9706 : ("Cabinet dentaire La Petite Souris", ""),
    9707 : ("Jardinerie de La Bâillerie", ""),
    9708 : ("Le Lys Douillet - Fleuriste", ""),
    9709 : ("Au Sommeil de Plomb - Plombier", ""),
    9710 : ("Rev'optique", ""),
    9711 : ("Service de réveil par téléphone", ""),
    9712 : ("Nous comptons les moutons pour vous!", ""),
    9713 : ("Roupille & Pionce, Avocats", ""),
    9714 : ("Croisière de rêve - Accastillage", ""),
    9715 : ("Banque du Doudou d'Or", ""),
    9716 : ("Le Lit en Cathédrale, farces at attrapes", ""),
    9717 : ("Pâtisserie du Croissant de Lune", ""),
    9718 : ("Sandwiches du Marchand de Sable", ""),
    9719 : ("Tout pour l'Oreiller", ""),
    9720 : ("Cours d'élocution pour somnambules", ""),
    9721 : ("Tapis du Loir", ""),
    9722 : ("Les Yeux Fermés - Spectacles en tous genres", ""),
    9725 : ("Pyjamas du Chat", ""),
    9727 : ("Ronflé, perdu", ""),
    9736 : ("Agence pour l'emploi Métiers de Rêve", ""),
    9737 : ("Au Tutu qui dort - École de danse", ""),
    9738 : ("Maison Ronflon", ""),
    9740 : ("Le Sabre Nocturne - Salle d'armes", ""),
    9741 : ("À l'Acarien Vorace - Destructeur de nuisibles", ""),
    9744 : ("Crème antirides Hicule", ""),
    9752 : ("Carburants Soporifiques", ""),
    9753 : ("Crèmes de Luna Glacées", ""),
    9754 : ("Randonnées équestres - Poney de Nuit", ""),
    9755 : ("Cinéma La Ronflette", ""),
    9756 : ("", ""),
    9759 : ("Institut de beauté du Bois - Dormant", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : ("Boutique à gags", ""),
    3508 : ("Quartier général des Toons", ""),
    3509 : ("Boutique de prêt-à-porter", ""),
    3511 : ("ANIMALERIE", ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("Aurore boréale - Electricité générale", ""),
    3602 : ("Bonnets de pâques", ""),
    3605 : ("", ""),
    3607 : ("Le vieillard du blizzard", ""),
    3608 : ("A en perdre la boule (de neige)!", ""),
    3610 : ("Supérette Les Mirettes", ""),
    3611 : ("M. Lapin - Chasse-neige", ""),
    3612 : ("Conception d'igloos", ""),
    3613 : ("Glaces et miroirs", ""),
    3614 : ("Fabriquant de flocons d'avoine", ""),
    3615 : ("Omelettes norvégiennes", ""),
    3617 : ("Voyages en ballon à air froid", ""),
    3618 : ("Boule de neige! Gestion de crise", ""),
    3620 : ("Atelier de ski", ""),
    3621 : ("Glacier La fonte des neiges", ""),
    3622 : ("", ""),
    3623 : ("Croque-monsieur", ""),
    3624 : ("Sandwichs froids", ""),
    3625 : ("Tante Angèle - Radiateurs", ""),
    3627 : ("Chenil St Bernard", ""),
    3629 : ("La soupe aux pois - Café", ""),
    3630 : ("Agence de voyage Laglisse", ""),
    3634 : ("Télésièges rembourrés", ""),
    3635 : ("Bois de chauffage d'occasion", ""),
    3636 : ("Chair de poule bon marché", ""),
    3637 : ("Les patins de Patricia", ""),
    3638 : ("Hêtre ou ne pas hêtre", ""),
    3641 : ("Chez Tanguy - Bâteaux à dormir debout", ""),
    3642 : ("L'œil du cyclone - Opticien", ""),
    3643 : ("Chambre (froide) de danse", ""),
    3644 : ("Glaçons fondus", ""),
    3647 : ("Au pingouin sanguin - Magasin de smokings", ""),
    3648 : ("Glace instantanée", ""),
    3649 : ("Hambrrghers", ""),
    3650 : ("Articlités", ""),
    3651 : ("Freddy Frigo - Saucisses congelées", ""),
    3653 : ("Bijoux glacés", ""),
    3654 : ("Quartier général des Toons", ""),
    # titles for: phase_8/dna/the_burrrgh_3200.dna
    3702 : ("Stockage hivernal", ""),
    3703 : ("", ""),
    3705 : ("Glaçons pour deux", ""),
    3706 : ("Babas au rhume", ""),
    3707 : ("Mon igloo est mon royaume", ""),
    3708 : ("Chez Pluto", ""),
    3710 : ("Restaurant en chute libre", ""),
    3711 : ("", ""),
    3712 : ("Au royaume du déluge", ""),
    3713 : ("Les dents qui claquent - Dentiste polaire", ""),
    3715 : ("Les bonnes soupes de Tante Artique", ""),
    3716 : ("Salage et poivrage des routes", ""),
    3717 : ("Juneau sais pas ce que vous voulez dire", ""),
    3718 : ("Inventeur de chambres à air", ""),
    3719 : ("Glaçon en cornet", ""),
    3721 : ("Aux bonnes affaires glissantes", ""),
    3722 : ("Boutique d'après-ski", ""),
    3723 : ("Chez Tremblotte - globes des neiges", ""),
    3724 : ("La chronique des rhumeurs", ""),
    3725 : ("Alluge-toi un instant", ""),
    3726 : ("Couvertures solaires", ""),
    3728 : ("Chasse-neige à la pelle", ""),
    3729 : ("", ""),
    3730 : ("Achat et vente de bonhommes de neige", ""),
    3731 : ("Cheminées portatives", ""),
    3732 : ("Au nez gelé", ""),
    3734 : ("Regards glacés - Optométrie", ""),
    3735 : ("Calottes glaciaires", ""),
    3736 : ("Cubes de glace bon marché", ""),
    3737 : ("Restaurant de la pente", ""),
    3738 : ("Chaud devant!", ""),
    3739 : ("Quartier général des Toons", ""),
# titles for: phase_8/dna/the_burrrgh_3300.dna
    3801 : (lToonHQ, ""),
    3806 : ("Croisières Tartiflette", ""),
    3807 : ("Nuages d'occasion", ""),
    3808 : ("Gîte Gilet", ""),
    3809 : ("Glaces de découverte", ""),
    3810 : ("Pelisses Municipales", ""),
    3811 : ("L'Ange Neige", ""),
    3812 : ("Chaussons pour chatons", ""),
    3813 : ("Après-skis biodégradables", ""),
    3814 : ("Pailles à glaçons", ""),
    3815 : ("Chalet Frisquet", ""),
    3816 : ("Au gui tout neuf", ""),
    3817 : ("Club Le Verglas", ""),
    3818 : ("La pelle des cîmes", ""),
    3819 : ("Ramonage et dégivrage", ""),
    3820 : ("Blanchisserie de neige", ""),
    3821 : ("Sports d'hibernation", ""),
    3823 : ("Fondation des Pluies", ""),
    3824 : ("Froids les marrons!", ""),
    3825 : ("Chapeaux tout frais", ""),
    3826 : ("Saperlichaussette!", ""),
    3827 : ("Couronnes de gui", ""),
    3828 : ("Le potager du bonhomme de neige", ""),
    3829 : ("Frigo Déco", ""),
    3830 : ("Voyons Voir, dégivrage de monocles", ""),
    }

# translate
# DistributedCloset.py
ClosetTimeoutMessage = "Désolé, tu n'as plus\n le temps."
ClosetNotOwnerMessage = "Ce n'est pas ton placard, mais tu peux essayer les vêtements."
ClosetPopupOK = lOK
ClosetPopupCancel = lCancel
ClosetDiscardButton = "Supprimer"
ClosetAreYouSureMessage = "Tu as supprimé des vêtements. Veux-tu vraiment les supprimer?"
ClosetYes = lYes
ClosetNo = lNo
ClosetVerifyDelete = "Vraiment supprimer %s?"
ClosetShirt = "cette chemise"
ClosetShorts = "ce short"
ClosetSkirt = "cette jupe"
ClosetDeleteShirt = "Supprimer\nchemise"
ClosetDeleteShorts = "Supprimer\nshort"
ClosetDeleteSkirt = "Supprimer\njupe"

# EstateLoader.py
EstateOwnerLeftMessage = "Désolé, le(la) propriétaire de cette maison est parti(e). Retour au terrain de jeux dans %s secondes"
EstatePopupOK = lOK
EstateTeleportFailed = "Impossible de retourner à la maison. Essaie encore!"
EstateTeleportFailedNotFriends = "Désolé, %s est chez un Toon avec qui tu n'es pas ami(e)."

# DistributedTarget.py
EstateTargetGameStart = "Le jeu des cibles tooniques a commencé!"
EstateTargetGameInst = "Plus tu tires dans la cible rouge, et plus tu remportes de tooniques."
EstateTargetGameEnd = "le jeu des cibles tooniques est maintenant terminé..."

# DistributedCannon.py
EstateCannonGameEnd = "La location du jeu de canon est terminée."

# DistributedHouse.py
AvatarsHouse = "Maison %s\n"

# BankGui.py
BankGuiCancel = lCancel
BankGuiOk = lOK

# DistributedBank.py
DistributedBankNoOwner = "Désolé, ce n'est pas ta tirelire."
DistributedBankNotOwner = "Désolé, ce n'est pas ta tirelire."

# FishSellGui.py
FishGuiCancel = lCancel
FishGuiOk = "Tout vendre"
FishTankValue = "Salut,%(name)s! Tu as %(num)s poisson(s) dans ton seau pour une valeur totale de %(value)s bonbon(s). Veux-tu vendre le tout ?"

#FlowerSellGui.py
FlowerGuiCancel = lCancel
FlowerGuiOk = "Tout vendre"
FlowerBasketValue = "%(name)s, tu as %(num)s fleurs dans ton panier d'une valeur totale de %(value)s bonbons. Veux-tu toutes les vendre?"


def GetPossesive(name):
    if name[-1:] == 's':
        possesive = "de " + name
    else:
        possesive = "de " + name
    return possesive

# PetTraits
# VERY_BAD, BAD, GOOD, VERY_GOOD
PetTrait2descriptions = {
    'hungerThreshold' : ('A toujours faim', 'A souvent faim',
                        'A quelquefois faim', 'A rarement faim',),
    'boredomThreshold' : ("S'ennuie toujours", "S'ennuie souvent",
                         "S'ennuie quelquefois", "S'ennuie rarement",),
    'angerThreshold' : ('Toujours ronchon', 'Souvent ronchon',
                       'Quelquefois ronchon', 'Rarement ronchon',),
    'forgetfulness' : ('Oublie toujours', 'Oublie souvent',
                      'Oublie quelquefois', 'Oublie rarement',),
    'excitementThreshold' : ('Très calme', 'Plutôt calme',
                            'Plutôt excité', 'Très excité',),
    'sadnessThreshold' : ('Toujours triste', 'Souvent triste',
                         'Quelquefois triste', 'Rarement triste',),
    'restlessnessThreshold' : ('Toujours agité', 'Souvent agité',
                         'Quelquefois agité', 'Rarement agité',),
    'playfulnessThreshold' : ('Rarement joueur', 'Quelquefois joueur',
                         'Souvent joueur', 'Toujours joueur',),
    'lonelinessThreshold' : ('Toujours solitaire', 'Souvent solitaire',
                         'Quelquefois solitaire', 'Rarement solitaire',),
    'fatigueThreshold' : ('Toujours fatigué', 'Souvent fatigué',
                         'Quelquefois fatigué', 'Rarement fatigué',),
    'confusionThreshold' : ('Toujours perplexe', 'souvent perplexe',
                         'Quelquefois perplexe', 'Rarement perplexe',),
    'surpriseThreshold' : ('Toujours surpris', 'souvent surpris',
                         'Quelquefois surpris', 'Rarement surpris',),
    'affectionThreshold' : ('Rarement affectueux', 'Quelquefois affectueux',
                         'Souvent affectueux', 'Toujours affectueux',),
    }

# end translate

# DistributedFireworkShow.py
FireworksInstructions = lToonHQ+": Appuie sur la touche \"Page précédente\" pour mieux voir."

FireworksJuly4Beginning = lToonHQ+": Welcome to summer fireworks! Enjoy the show!"
FireworksJuly4Ending = lToonHQ+": Hope you enjoyed the show! Have a great summer!"
FireworksFebruary14Beginning = lToonHQ+": Joyeuse Saint Valentin à tous les amoureux!"
FireworksFebruary14Ending = lToonHQ+": Joyeuse Saint Valentin à tous les amoureux!"
FireworksJuly14Beginning = lToonHQ+": Feux d'artifices du 14 Juillet: Profitez du spectacle!"
FireworksJuly14Ending = lToonHQ+": Nous espérons que vous avez profité du spectacle!"
FireworksOctober31Beginning = lToonHQ+": Bons feux d'artifice!"
FireworksOctober31Ending = lToonHQ+": Nous espérons que vous avez aimé les feux d'artifice!"
FireworksNewYearsEveBeginning = lToonHQ+": Bonne année! Profitez du feu d'artifice!"
FireworksNewYearsEveEnding = lToonHQ+": Nous espérons que vous avez profité du spectacle! Bonne année!"
FireworksBeginning = lToonHQ+": Bons feux d'artifice!"
FireworksEnding = lToonHQ+": Nous espérons que vous avez aimé les feux d'artifice!"

# ToontownLoadingScreen.py

TIP_NONE = 0
TIP_GENERAL = 1
TIP_STREET = 2
TIP_MINIGAME = 3
TIP_COGHQ = 4
TIP_ESTATE = 5
TIP_KARTING = 6
TIP_GOLF = 7

# As of 8/5/03, ToonTips shouldn't exceed 130 characters in length
TipTitle = "ASTUCE TOON:"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Pour vérifier rapidement les progrès de ton défitoon, maintiens enfoncée la touche \"Fin\".",
    "Pour vérifier rapidement ta page de gags, maintiens enfoncée la touche \"Première page\".",
    "Pour ouvrir ta liste d'contacts, appuie sur la touche \"F7\".",
    "Pour ouvrir ou fermer ton journal de bord, appuie sur la touche \"F8\".",
    "Pour regarder vers le haut, appuie sur la touche \"Page précédente\"; pour regarder vers le bas, appuie sur la touche \"Page suivante\".",
    "Appuie sur la touche \"Contrôle\" pour sauter.",
    "Appuie sur la touche \"F9\" pour faire une capture d'écran qui sera enregistrée dans le dossier Toontown de ton ordinateur.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "Tu peux échanger des codes d'ami secret avec des personnes que tu connais en dehors de Toontown pour pouvoir chatter avec eux dans Toontown.",
    "Tu peux changer ta résolution d'écran, régler le son et d'autres options dans la page d'options du journal de bord.",
    "Essaie les vêtements de tes contacts, qui sont dans les placards de leur maison.",
    "Tu peux rentrer chez toi grâce au bouton \"Retour à la maison\" sur ta carte.",
    "Chaque fois que tu termines un défitoon avec succès, tes rigolpoints sont automatiquement ajoutés.",
    "Tu peux voir la collection dans les boutiques de prêt-à-porter même sans ticket d'habillement.",
    "Les récompenses de certains défitoons te permettent d'avoir plus de gags et de bonbons.",
    "Tu peux avoir jusqu'à 50 contacts sur ta liste d'contacts.",
    "La récompense de certains défitoons te permet de te téléporter jusqu'aux terrains de jeux de Toontown par la carte du journal de bord.",
    "Récupère tes rigolpoints sur les terrains de jeux en ramassant des trésors tels que des étoiles et des cornets de glace.",
    "Si tu as besoin de te soigner rapidement après un combat difficile, va chez toi et ramasse des cornets de glace.",
    "Pour changer la visualisation de ton Toon, appuie sur la touche de tabulation.",
    "Quelquefois tu peux trouver plusieurs défitoons différents proposés pour la même récompense. Fais ton choix!",
    "Trouver des contacts qui font le même défitoon que toi est une manière amusante de progresser dans le jeu.",
    "Tu n'as jamais besoin d'enregistrer ta progression dans Toontown. Les serveurs de Toontown enregistrent toutes les informations nécessaires en continu.",
    "Tu peux parler en chuchotant à d'autres Toons en cliquant sur eux ou en les sélectionnant dans ta liste d'contacts.",
    "Certaines phrases du Chat rapide provoquent une émotion animée sur ton Toon.",
    "Si tu te trouves dans une zone où il y a trop de monde, tu peux essayer de changer de district. Va à la page des districts dans le journal de bord et choisis-en un autre.",
    "Si tu sauves activement des bâtiments, une étoile de bronze, d'argent ou d'or s'affichera au-dessus de ton Toon.",
    "Si tu sauves assez de bâtiments pour avoir une étoile au-dessus de la tête, tu pourras trouver ton nom affiché sur le tableau d'un Quartier Général des Toons.",
    "Les bâtiments sauvés sont quelquefois recapturés par les Cogs. La seule façon de conserver ton étoile est d'aller sauver plus de bâtiments.",
    "Les noms de tes amis apparaîtront en bleu.",
    # Fishing
    "Essaie d'avoir toutes les espèces de poisson de Toontown!",
    "Chaque mare recèle différentes sortes de poissons. Essaie-les toutes!",
    "Lorsque ton seau de pêche est plein, tu peux vendre tes poissons aux vendeurs de l'animalerie sur les terrains de jeux.",
    "Tu peux vendre tes poissons au vendeur de l'animalerie, près des mares ou dans les animaleries même.",
    "Les cannes à pêche plus solides attrapent de plus gros poissons mais requièrent plus de bonbons.",
    "Tu peux acheter des cannes à pêche plus solides dans le catalogue.",
    "Les plus gros poissons valent plus de bonbons à l'animalerie.",
    "Les poissons plus rares valent plus de bonbons à l'animalerie.",
    "Tu peux quelquefois trouver des sacs de bonbons en pêchant.",
    "Certains défitoons nécessitent de pêcher des objets dans les mares.",
    "Les mares des terrains de jeux ont des poissons différents de ceux des mares des rues.",
    "Certains poissons sont vraiment rares. Continue à pêcher jusqu'à ce que tu les aies tous!",
    "La mare que tu as chez toi contient des poissons qui ne peuvent pas être trouvés ailleurs.",
    "À chaque fois que tu as attrapé 10 espèces, tu gagnes un trophée de pêche!",
    "Tu peux voir quels poissons tu as pêchés dans ton journal de bord.",
    "Certains trophées de pêche te valent une rigol-augmentation.",
    "La pêche est une bonne façon de gagner plus de bonbons.",
    # Doudous
    "Adopte un Doudou au magasin d'animaux!",
    "Les magasins d'animaux ont de nouveaux Doudous à vendre tous les jours.",
    "Rends-toi dans les magasins d'animaux tous les jours pour voir quels nouveaux Doudous ils ont.",
    "Dans les différents quartiers, il y a des Doudous différents à adopter.",
    # Karting
    "Fais chauffer ton super moteur et mets un coup de turbo à ta rigo-limite.",
    "Rends-toi dans le Circuit Dingo par le tunnel en forme de pneu qui se trouve dans Toontown Central.",
    "Gagne des rigolpoints au Circuit Dingo.",
    "Le Circuit Dingo a six pistes de course différentes."
    ),

  TIP_STREET : (
    "Il existe quatre types de Cogs : les Loibots, les Caissbots, les Vendibots et les Chefbots.",
    "Chaque série de gags est associée à différents niveaux de précision et de dégâts.",
    "Les gags de tapage affectent tous les Cogs mais réveillent les Cogs leurrés.",
    "Battre les Cogs en ordre stratégique peut grandement augmenter tes chances de gagner les batailles.",
    "La série de gags \"toonique\" te permet de soigner les autres Toons lors d'une bataille.",
    "Les points d'expérience des gags sont doublés pendant une invasion de Cogs!",
    "Plusieurs Toons peuvent faire équipe et utiliser la même série de gags lors d'une bataille pour infliger plus de dégâts aux Cogs.",
    "Lors des batailles, les gags sont utilisés dans l'ordre affiché sur le menu des gags, de haut en bas.",
    "La rangée de points lumineux sur les ascenseurs des bâtiments des Cogs indiquent combien d'étages ils contiennent.",
    "Clique sur un Cog pour avoir plus de détails.",
    "L'utilisation de gags de haut niveau contre des Cogs de bas niveau ne donne pas de points d'expérience.",
    "Un gag qui donnera de l'expérience s'affiche sur fond bleu sur le menu des gags lors de la bataille.",
    "L'expérience des gags est multipliée lorsqu'ils sont utilisés à l'intérieur des bâtiments des Cogs. Les étages les plus hauts ont des coefficients de multiplication plus grands.",
    "Lorsqu'un Cog est vaincu, chacun des Toons ayant participé est crédité de la victoire sur ce Cog lorsque la bataille est terminée.",
    "Chaque rue de Toontown a différents types et niveaux de Cogs.",
    "Il n'y a pas de Cogs sur les trottoirs.",
    "Dans les rues, tu peux entendre des blagues en t'approchant des portes latérales.",
    "Certains défitoons t'entraînent à de nouvelles séries de gags. Tu ne pourras choisir que six des sept séries de gags, alors choisis bien!",
    "Les pièges ne sont utiles que si toi ou tes contacts vous mettez d'accord pour utiliser les leurres lors d'une bataille.",
    "Les leurres de plus haut niveau sont moins susceptibles de manquer leur cible.",
    "Les gags de plus bas niveau ont une précision moindre contre les Cogs de haut niveau.",
    "Les Cogs ne peuvent plus attaquer une fois qu'ils ont été leurrés lors d'un combat.",
    "Lorsque tes contacts et toi aurez repris un bâtiment aux Cogs, vos portraits seront affichés à l'intérieur du bâtiment en guise de récompense.",
    "L'utilisation d'un gag toonique sur un Toon qui a un rigolmètre au maximum ne donne pas d'expérience toonique.",
    "Les Cogs sont brièvement assommés lorsqu'ils sont frappés par un gag. Cela augmente la chance que les autres gags du même tour le frappent.",
    "Les gags de chute ont de faibles chances d'atteindre leur but, mais la précision est accrue lorsque les Cogs ont auparavant été frappés par un autre gag lors du même tour.",
    "Lorsque tu as vaincu suffisamment de Cogs, tu peux utiliser le détecteur de Cogs en cliquant sur les icônes du détecteur sur la page de la galerie des Cogs dans ton journal de bord.",
    "Pendant une bataille, les tirets (-) et les X indiquent quel Cog tes équipiers sont en train d'attaquer.",
    "Pendant une bataille, un voyant lumineux sur les Cogs indique leur état de santé : vert signifie en bonne santé, rouge au bord de la destruction.",
    "Un maximum de quatre Toons peuvent combattre simultanément.",
    "Dans la rue, les Cogs prendront plus facilement part à une bataille contre plusieurs Toons qu'à une bataille contre un seul Toon.",
    "Les deux Cogs les plus difficiles de chaque type ne se trouvent que dans les bâtiments.",
    "Les gags de chute ne fonctionnent jamais contre les Cogs leurrés.",
    "Les Cogs ont tendance à attaquer le Toon qui leur a causé le plus de dégâts.",
    "Les gags de tapage ne donnent pas de bonus contre les Cogs leurrés.",
    "Si tu attends trop longtemps avant d'attaquer un Cog leurré, il se réveille. Les leurres de plus haut niveau durent plus longtemps.",
    "Il y a des mares dans toutes les rues de Toontown. Certaines rues ont des espèces de poissons uniques.",
    ),

  TIP_MINIGAME : (
    "Après avoir rempli ton pot de bonbons, tous les bonbons que tu gagnes aux jeux du tramway sont automatiquement versés dans ta tirelire.",
    "Tu peux utiliser les flèches du clavier au lieu de la souris dans le jeu du tramway \"Imite Minnie\".",
    "Dans le jeu du canon, tu peux utiliser les flèches du clavier pour déplacer ton canon et appuyer sur la touche \"Contrôle\" pour tirer.",
    "Dans le jeu des anneaux, des points supplémentaires sont attribués quand le groupe entier réussit à nager dans les anneaux.",
    "Un jeu parfait d'\"Imite Minnie\" double tes points.",
    "Dans le tir à la corde, tu reçois plus de bonbons si tu joues contre un Cog plus fort.",
    "La difficulté des jeux du tramway varie selon les quartiers, Toontown centre a les plus faciles et le Pays des rêves de Donald les plus difficiles.",
    "Certains jeux du tramway ne peuvent être joués qu'en groupe.",
    ),

  TIP_COGHQ : (
    "Tu dois terminer ton déguisement de Cog avant d'entrer dans le bâtiment du Chef.",
    "Tu peux sauter sur les gardes du corps des Cogs pour les désactiver temporairement.",
    "Tu dois faire entièrement ton déguisement Loibot avant d'aller voir le Juge.",
    "Additionne les mérites Cogs par tes victoires sur les Cogs.",
    "Tu obtiens plus de mérites avec des Cogs de plus haut niveau.",
    "Lorsque tu as additionné assez de mérites Cogs pour gagner une promotion, va voir le vice-président des Vendibots !",
    "Tu peux parler comme un Cog lorsque tu portes ton déguisement de Cog.",
    "Jusqu'à huit Toons peuvent faire équipe pour combattre le vice-président des Vendibots.",
    "Le vice-président des Vendibots est tout en haut du quartier général des Cogs.",
    "À l'intérieur des usines des Cogs, monte les escaliers pour arriver jusqu'au contremaître.",
    "Chaque fois que tu te bats dans l'usine, tu gagnes une pièce de ton déguisement de Cog.",
    "Tu peux visualiser le progrès de ton déguisement de Cog dans ton journal de bord.",
    "Tu peux visualiser le progrès de tes mérites sur ta page de déguisements dans ton journal de bord.",
    "Assure-toi d'avoir suffisamment de gags et un rigolmètre au maximum avant d'aller voir le vice-président.",
    "Si tu as une promotion, ton déguisement de Cog est mis à jour.",
    "Tu dois vaincre le contremaître de l'usine pour récupérer une pièce du déguisement de Cog.",
    "Récupère des Convocations du Jury en défiant des Loibots.",
    "Tu reçois plus de Mérites, d'euros Cog ou de Convocations du Jury en combattant des Cogs de plus haut niveau.", 
    "Quand tu as récupéré assez de Convocations du Jury pour gagner une promotion, va voir le Juge  !",
    "Tu dois faire entièrement ton déguisement Loibot avant d'aller voir le Juge.",
    "Jusqu'à huit Toons peuvent combattre ensemble le Juge Loibot.",
    "Cela paie d'être perplexe : Les Cogs virtuels dans le QG Loibot ne t'accableront pas de Convocations du Jury.",
    " Gagne des pièces de costume de Caissbot comme récompense en terminant les défitoons qui sont proposés dans le Pays des Rêves de Donald.",
    " Les Caissbots fabriquent et font circuler leur argent, les euros Cogs, à partir de trois Fabriques à Sous - Pièce, Euro et Lingot.",
    " Attends que le directeur financier soit étourdi avant de lui lancer un coffre dessus, ou il pourrait l'utiliser comme casque. Frapper le casque avec un autre coffre est la seule manière de le faire tomber.",
    " Gagne des pièces de costume de Loibot comme récompense en terminant les défitoons pour le professeur Flocon.",
    " Ca paie de résoudre les problèmes : les Cogs virtuels du QG Loibot ne vont pas te récompenser avec des notices du jury.",
    ),
  TIP_ESTATE : (
  # Doodles
    "Les Doudous peuvent comprendre certaines expressions de Chat rapide. Essaie-les!",
    "Utilise le menu \"Animaux familiers\" du Chat rapide pour demander à ton Doudou de faire des tours.",
    "Tu peux apprendre des tours aux Doudous avec les leçons du catalogue vachement branché de Clarabelle.",
    "Récompense ton Doudou quand il fait des tours.",
    "Si tu te rends chez un ami, ton Doudou viendra aussi.",
    "Donne un bonbon à ton Doudou quand il a faim.",
    "Clique sur un Doudou pour afficher un menu grâce auquel tu pourras le nourrir, le cajoler et l'appeler.",
    "Les Doudous aiment la compagnie. Invite tes contacts à venir jouer!",
    "Chaque Doudou a une personnalité unique.",
    "Tu peux rapporter ton Doudou et en adopter un nouveau à l'animalerie.",
    "Quand un Doudou fait un tour, les Toons qui sont aux alentours sont soignés.",
    "Les Doudous font leurs tours de mieux en mieux avec de l'entraînement. Un peu de persévérance!",
    "Les tours plus avancés des Doudous soignent plus vite les Toons.",
    "Les Doudous expérimentés peuvent faire plus de tours avant de se fatiguer.",
    "Tu peux voir une liste des Doudous qui sont à proximité dans ta liste d'contacts.",
    # Furniture / Cattlelog
    "Achète des fournitures dans le catalogue de Clarabelle pour décorer ta maison.",
    "La tirelire de ta maison contient des bonbons supplémentaires.",
    "Le placard de ta maison contient des vêtements supplémentaires.",
    "Rends-toi dans la maison de ton ami et essaie ses vêtements.",
    "Achète de meilleures cannes à pêche dans le catalogue de Clarabelle.",
    "Achète de plus grandes tirelires dans le catalogue de Clarabelle.",
    "Appelle Clarabelle avec le téléphone qui est dans ta maison.",
    "Clarabelle vend un placard plus grand qui contient plus de vêtements.",
    "Fais de la place dans ton placard avant d'utiliser un ticket d'habillement.",
    "Clarabelle vend tout ce dont tu as besoin pour décorer ta maison.",
    "Vérifie ta boîte aux lettres pour trouver ta livraison après avoir commandé chez Clarabelle.",
    "Les vêtements du catalogue de Clarabelle sont livrés dans l'heure.",
    "Le papier peint et le revêtement de sol du catalogue de Clarabelle sont livrés dans l'heure.",
    "Les meubles du catalogue de Clarabelle sont livrés un jour plus tard.",
    "Stocke plus de meubles dans ton grenier.",
    "Tu seras averti(e) par Clarabelle quand un nouveau catalogue sera prêt.",
    "Tu seras averti(e) par Clarabelle quand un nouveau catalogue sera prêt.",
    "Les nouveaux catalogues sont livrés chaque semaine.",
    "Cherche les articles de vacances en édition limitée dans le catalogue.",
    "Mets les meubles dont tu ne veux plus à la poubelle.",
    # Fish
    "Certains poissons, comme le hareng saur, sont plus communs dans les propriétés des Toons.",
    # Misc
    "Tu peux inviter tes contacts sur ta propriété en utilisant le Chat rapide.",
    "Est-ce que tu savais que la couleur de ta maison est assortie à celle de ton panneau Choisis un Toon ?",
    ),
   TIP_KARTING : (
    # Goofy Speedway zone specific
        "Achète un Roadster, un Utilitoon ou une Berline au Centre Auto Dingo.", 
        "Customise ton kart avec des autocollants, des baguettes et plein d'autres déco au Centre Auto Dingo.", 
    "Gagne des tickets en faisant la course sur le Circuit Dingo.",
    "Les tickets sont la seule monnaie acceptée par le Centre Auto Dingo.",
        " Tu dois déposer des tickets pour pouvoir faire la course.",
    "Une page spéciale de ton journal de bord te permet de customiser ton kart.", 
    "Une page spéciale de ton journal de bord te permet de consulter tes scores sur chaque piste.", 
    "Une page spéciale de ton journal de bord te permet d'afficher tes trophées.", 
    "Le Colisée Tortillé est la piste la plus facile du Circuit Dingo.", 
        " Les Landes Légères est la piste qui a le plus de collines et de bosses du Circuit Dingo.", 
    "Le Boulevard du Blizzard est la piste la plus excitante du Circuit Dingo.", 
    ),
    TIP_GOLF: (
    # Golfing specific
    "Appuie sur la touche de tabulation pour obtenir une vue de dessus du terrain de golf.",
    "Appuie sur la flèche de déplacement vers le haut pour t'orienter vers le trou.",
    "Faire un swing avec un club, c'est comme un peu comme lancer une tarte.",
    ),
    }

FishGenusNames = {
    0 : "Baudruche",
    2 : "Poisson-chat",
    4 : "Poisson-clown",
    6 : "Poisson surgelé",
    8 : "Étoile de mer",
    10 : "Hareng saur",
    12 : "Poisson chien",
    14 : "Anguille douce",
    16 : "Requin nourrice",
    18 : "Crabe-roi",
    20 : "Poisson-lune",
    22 : "Hippocampe",
    24 : "Requin d'eau douce",
    26 : "Bar à coudas",
    28 : "Truite coupe-gorge",
    30 : "Thon tonléon",
    32 : "Méduse médusée",
    34 : "Raie tissante",
    }

FishSpeciesNames = {
    0 : ( "Poisson baudruche",
          "Baudruche à air chaud",
          "Baudruche météo",
          "Baudruche à eau",
          "Baudruche rouge",
          ),
    2 : ( "Poisson-chat",
          "Poisson-chat siamois",
          "Poisson-chat piteau",
          "Poisson-chat de gouttière",
          "Poisson matou",
          ),
    4 : ( "Poisson-clown",
          "Poisson-clown triste",
          "Poisson-pitre",
          "Poisson-cirque",
          ),
    6 : ( "Poisson surgelé",
          ),
    8 : ( "Étoile de mer",
          "Étoile de mer lu",
          "Étoile de mer sédès",
          "Étoile de mer credi",
          "Étoile de mer ciatous",
          ),
    10 : ( "Hareng saur",
           ),
    12 : ( "Poisson chien",
           "Poisson-chien de traîneau",
           "Poisson-chien-chien",
           "Poisson dalmatien",
           "Poisson chiot",
           ),
    14 : ( "Anguille douce",
           "Anguille rette électrique",
           ),
    16 : ( "Requin nourrice",
           "Requin nourrice tique",
           "Requin nourrice tourne",
           ),
    18 : ( "Crabe-roi",
           "Crabe roi d'Alaska",
           "Vieux crabe roi",
           ),
    20 : ( "Poisson-lune",
           "Poisson pleine lune",
           "Poisson demi-lune",
           "Poisson nouvelle lune",
           "Poisson croissant de lune",
           "Poisson équinoxe",
           ),
    22 : ( "Hippocampe",
           "Hippocampe oscillant",
           "Hippocampe percheron",
           "Hippocampe oriental",
           ),
    24 : ( "Requin d'eau douce",
           "Requin de baignoire",
           "Requin de piscine",
           "Requin olympique",
           ),
    26 : ( "Bar tabba",
           "Bar amine",
           "Bar ratin",
           "Bar ricade",
           "Bar sovie",
           "Bar racé",
           "Bar cadaire",
           "Bar bouillé",
           ),
    28 : ( "Truite coupe-gorge",
           "Truite capitaine",
           "Truite scorbut",
           ),
    30 : ( "Thon tonléon",
           "Thon-clave",
           "Thon-suret",
           "Thon bola",
           "Thon durasé",
           ),
    32 : ( "Méduse médusée",
           "Poisson-cacahuète",
           "Poisson pané",
           "Poisson fraise",
           "Poisson raisin",
           ),
    34 : ( "Raie tissante",
           ),
    }

CogPartNames = (
    "Cuisse gauche", "Tibia gauche", "Pied gauche",
    "Cuisse droite", "Tibia droit", "Pied droit",
    "Épaule gauche",  "Épaule droite", "Poitrine", "Compteur de santé", "Bassin",
    "Bras gauche",  "Avant-bras gauche", "Main gauche",
    "Bras droit", "Avant-bras droit", "Main droite",
    )

CogPartNamesSimple = (
    "Haut du torse",
    )

FishFirstNames = (
    "",
    "Angéline",
    "Arctique",
    "Bébé",
    "Bermuda",
    "Grand",
    "Fontaine",
    "Bubule",
    "Buster",
    "Candy",
    "Capitaine",
    "Ciboulette",
    "Choupette",
    "Corail",
    "Docteur",
    "Toussale",
    "Empereur",
    "Mâchefer",
    "Gros",
    "Filou",
    "Palmyre",
    "Polochon",
    "Totoche",
    "Doudou",
    "Jack",
    "Roi",
    "P'tit",
    "Marin",
    "Mamzelle",
    "Monsieur",
    "Pomme",
    "Petit-Doigt",
    "Prince",
    "Princesse",
    "Professeur",
    "Bouboule",
    "Reine",
    "Mirage",
    "Ray",
    "Rosie",
    "Robert",
    "Poivre",
    "Nicole",
    "Sandy",
    "Écaille",
    "Dent d'or",
    "Sire",
    "Sacha",
    "Pantoufle",
    "Chipeur",
    "Mini",
    "Sébastien",
    "P'tit-Pois",
    "Étoile",
    "Sucre d'orge",
    "Super",
    "Tigre",
    "Microbe",
    "Moustache",
    )

FishLastPrefixNames = (
    "",
    "Laplage",
    "Noir",
    "Bleu",
    "Marcassin",
    "Lavache",
    "Minou",
    "Aufond",
    "Double",
    "Est",
    "Chichi",
    "Écaille",
    "Plat",
    "Frais",
    "Géant",
    "Dorpur",
    "Doré",
    "Gris",
    "Vert",
    "Goinfre",
    "Jacasse",
    "Gelée",
    "Dame",
    "Cuir",
    "Citron",
    "Long",
    "Nord",
    "Océan",
    "Octo",
    "Huile",
    "Perle",
    "Mousse",
    "Rouge",
    "Ruban",
    "Fleuve",
    "Roc",
    "Rubis",
    "Barre",
    "Sel",
    "Mer",
    "Argent",
    "Tuba",
    "Semelle",
    "Sud",
    "Hérisse",
    "Surf",
    "Sabre",
    "Tigre",
    "Triple",
    "Tropical",
    "Thon",
    "Coucou",
    "Faible",
    "Ouest",
    "Blanc",
    "Jaune",
    )

FishLastSuffixNames = (
    "",
    "balle",
    "basse",
    "ventre",
    "punaise",
    "vole",
    "beurre",
    "dents",
    "botte",
    "crabe",
    "ronchon",
    "tambour",
    "palme",
    "poisson",
    "nette",
    "nageoire",
    "flou",
    "grogne",
    "tête",
    "veste",
    "saut",
    "sardine",
    "lune",
    "bouche",
    "mulet",
    "cou",
    "nez",
    "perche",
    "rauque",
    "coureur",
    "voile",
    "requin",
    "coquille",
    "soie",
    "bave",
    "vif",
    "pue",
    "queue",
    "crapaud",
    "truite",
    "eau",
    )


CogPartNames = (
    "Cuisse gauche", "Tibia gauche", "Pied gauche",
    "Cuisse droite", "Tibia droit", "Pied droit",
    "Épaule gauche",  "Épaule droite", "Poitrine", "Compteur de santé", "Bassin",
    "Bras gauche",  "Avant-bras gauche", "Main gauche",
    "Bras droit", "Avant-bras droit", "Main droite",
    )

CogPartNamesSimple = (
    "Haut du torse",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "Entrée principale"
SellbotLegFactorySpecLobby = "Accueil"
SellbotLegFactorySpecLobbyHallway = "Couloir de l'accueil"
SellbotLegFactorySpecGearRoom = "Salle des pignons"
SellbotLegFactorySpecBoilerRoom = "Chaufferie"
SellbotLegFactorySpecEastCatwalk = "Passerelle est"
SellbotLegFactorySpecPaintMixer = "Mélangeur à peinture"
SellbotLegFactorySpecPaintMixerStorageRoom = "Réserve du mélangeur à peinture"
SellbotLegFactorySpecWestSiloCatwalk = "Passerelle du silo ouest"
SellbotLegFactorySpecPipeRoom = "Salle des tuyaux"
SellbotLegFactorySpecDuctRoom = "Salle des canalisations"
SellbotLegFactorySpecSideEntrance = "Entrée latérale"
SellbotLegFactorySpecStomperAlley = "Allée des pas perdus"
SellbotLegFactorySpecLavaRoomFoyer = "Accueil des sanitaires"
SellbotLegFactorySpecLavaRoom = "Sanitaires"
SellbotLegFactorySpecLavaStorageRoom = "Réserve des sanitaires"
SellbotLegFactorySpecWestCatwalk = "Passerelle ouest"
SellbotLegFactorySpecOilRoom = "Salle du pétrole"
SellbotLegFactorySpecLookout = "Poste d'observation"
SellbotLegFactorySpecWarehouse = "Réserve"
SellbotLegFactorySpecOilRoomHallway = "Entrée de la salle du pétrole"
SellbotLegFactorySpecEastSiloControlRoom = "Salle de contrôle du silo est"
SellbotLegFactorySpecWestSiloControlRoom = "Salle de contrôle du silo ouest"
SellbotLegFactorySpecCenterSiloControlRoom = "Salle de contrôle du silo central"
SellbotLegFactorySpecEastSilo = "Silo est"
SellbotLegFactorySpecWestSilo = "Silo ouest"
SellbotLegFactorySpecCenterSilo = "Silo central"
SellbotLegFactorySpecEastSiloCatwalk = "Passerelle du silo est"
SellbotLegFactorySpecWestElevatorShaft = "Puits de l'ascenseur ouest"
SellbotLegFactorySpecEastElevatorShaft = "Puits de l'ascenseur est"

#FISH BINGO
FishBingoBingo = "BINGO!"
FishBingoVictory = "VICTOIRE!!"
FishBingoJackpot = "JACKPOT!"
FishBingoGameOver = "JEU TERMINÉ"
FishBingoIntermission = "La pause\nse termine dans :"
FishBingoNextGame = "Le prochain jeu\ncommence dans :"
FishBingoTypeNormal = "Classique"
FishBingoTypeCorners = "Quatre coins"
FishBingoTypeDiagonal = "Diagonales"
FishBingoTypeThreeway = "Trois voies"
FishBingoTypeBlockout = "GRILLE ENTIERE!"
FishBingoStart = "C'est l'heure du loto des poissons! Rends-toi sur n'importe quel ponton libre pour jouer!"
FishBingoOngoing = ""
FishBingoEnd = "J'espère que le loto des poissons t'a plu."
FishBingoHelpMain = "Bienvenue au loto des poissons de Toontown! Tout le monde à la mare s'active pour remplir la grille avant la fin du temps imparti."
FishBingoHelpFlash = "Quand tu attrapes un poisson, clique sur un des carrés clignotants pour marquer la grille."
FishBingoHelpNormal = "C'est une grille de loto classique. Tu gagnes si tu remplis n'importe quel rangée verticalement, horizontalement ou diagonalement."
FishBingoHelpDiagonals = "Remplis les deux diagonales pour gagner."
FishBingoHelpCorners = "Une grille de coins facile. Remplis les quatre coins pour gagner."
FishBingoHelpThreeway = "Trois voies. Remplis les deux diagonales et la rangée du milieu pour gagner. Ça n'est pas facile!"
FishBingoHelpBlockout = "Grille entière! Remplis la grille entière pour gagner. Tu joues contre toutes les autres mares pour remporter un énorme jackpot!"
FishBingoOfferToSellFish = "Ton seau est plein de poissons. Est-ce que tu voudrais en vendre ?"
FishBingoJackpot = "Gain: %s bonbons!"
FishBingoJackpotWin = "Gain: %s bonbons!"

# ResistanceSCStrings: SpeedChat phrases rewarded for defeating the CFO.
# It is safe to remove entries from this list, which will disable them
# for use from any toons who have already purchased them.  Note that the
# index numbers are stored directly in the database, so once assigned
# to a particular phrase, a given index number should never be
# repurposed to any other phrase.
ResistanceToonupMenu = "Toonique"
ResistanceToonupItem = "%s Toonique"
ResistanceToonupItemMax = "Max"
ResistanceToonupChat = "Toons du Monde entier, Toonique!"
ResistanceRestockMenu = "À vos gags"
ResistanceRestockItem = "À vos gags %s"
ResistanceRestockItemAll = "Tous"
ResistanceRestockChat = "Toons du Monde entier, à vos gags!"
ResistanceMoneyMenu = "Bonbons"
ResistanceMoneyItem = "%s bonbons"
ResistanceMoneyChat = "Toons du Monde entier, dépensez avec sagesse!"

# Resistance Emote NPC chat phrases
ResistanceEmote1 = NPCToonNames[9228] + ": Bienvenue dans la résistance!"
ResistanceEmote2 = NPCToonNames[9228] + ": Utilise ton nouvel émoticone pour t'identifier auprès des autres membres."
ResistanceEmote3 = NPCToonNames[9228] + ": Bonne chance!"

# Kart racing
KartUIExit = "Laisser le kart"
KartShop_Cancel = lCancel
KartShop_BuyKart = "Acheter un kart"
KartShop_BuyAccessories = "Acheter des accessoires"
KartShop_BuyAccessory = "Acheter un accessoire"
KartShop_Cost = "Prix: %d tickets"
KartShop_ConfirmBuy = "Acheter cette %s pour %d tickets?"
KartShop_NoAvailableAcc = "Aucun accessoire de ce type n'est disponible."
KartShop_FullTrunk = "Ton coffre est plein."
KartShop_ConfirmReturnKart = "Tu veux vraiment rendre ton kart actuel?"
KartShop_ConfirmBoughtTitle = "Bravo!"
KartShop_NotEnoughTickets = "Pas assez de tickets!"

KartView_Rotate = "Faire tourner"
KartView_Right = "Droite"
KartView_Left = "Gauche"

# starting block
StartingBlock_NotEnoughTickets = "Tu n'as pas assez de tickets! Fais plutôt une course d'entraînement."
StartingBlock_NoBoard = "Les inscriptions sont terminées pour cette course. Tu dois attendre que la prochaine course commence."
StartingBlock_NoKart = "Il te faut d'abord un kart! Va donc voir un des vendeurs du magasin de kart."
StartingBlock_Occupied = "Ce plot de départ est actuellement occupé! Essaie un autre endroit."
StartingBlock_TrackClosed = "Nous sommes désolés, cette piste est fermée pour cause de réfection."
StartingBlock_EnterPractice = "Tu veux participer à une course d'entraînement ?"
StartingBlock_EnterNonPractice = "Veux-tu participer à une course %s pour %s tickets?"
StartingBlock_EnterShowPad = "Veux-tu garer ta voiture ici?"
StartingBlock_KickSoloRacer = "Les combats de Toons et les Grands Prix requièrent deux pilotes ou plus."
StartingBlock_Loading = "Allons à la course!"

#stuff for leader boards
LeaderBoard_Time = "Temps"
LeaderBoard_Name = "Nom du pilote"
LeaderBoard_Daily = "Scores quotidiens"
LeaderBoard_Weekly = "Scores hebdomadaires"
LeaderBoard_AllTime = "Meilleurs scores de tous les temps"

RecordPeriodStrings = [
    LeaderBoard_Daily,
    LeaderBoard_Weekly,
    LeaderBoard_AllTime,
    ]

KartRace_RaceNames = [
    "Entraînement",
    "Combat de Toons",
    "Tournoi",
    ]

from toontown.racing import RaceGlobals

KartRace_Go = "Partez!"
KartRace_Reverse = " Inversé"

#needed for leader boards
KartRace_TrackNames = {
  RaceGlobals.RT_Speedway_1     : "Stade Cinglette",
  RaceGlobals.RT_Speedway_1_rev : "Stade Cinglette" + KartRace_Reverse,
  RaceGlobals.RT_Rural_1        : "Piste Champêtre",
  RaceGlobals.RT_Rural_1_rev    : "Piste Champêtre" + KartRace_Reverse,
  RaceGlobals.RT_Urban_1        : "Circuit de la Ville",
  RaceGlobals.RT_Urban_1_rev    : "Circuit de la Ville" + KartRace_Reverse,
  RaceGlobals.RT_Speedway_2     : "Colisée Tortillé",
  RaceGlobals.RT_Speedway_2_rev : "Colisée Tortillé" + KartRace_Reverse,
  RaceGlobals.RT_Rural_2        : "Landes Légères",
  RaceGlobals.RT_Rural_2_rev    : "Landes Légères" + KartRace_Reverse,
  RaceGlobals.RT_Urban_2        : "Bld du Blizzard",
  RaceGlobals.RT_Urban_2_rev    : "Bld du Blizzard" + KartRace_Reverse,
  }

KartRace_Unraced = "S/O"

KartDNA_KartNames = {
    0:"Berline",
    1:"Roadster",
    2:"Utilitoon"
    }

KartDNA_AccNames = {
    #engine block accessory names
    1000: "Filtre à air",
    1001: "Carburateur quadruple",
    1002: "Aigle en vol",
    1003: "Cornes de bœuf",
    1004: "Six cylindres en ligne",
    1005: "Petit déflecteur",
    1006: "Arbre à cames simple",
    1007: "Déflecteur moyen",
    1008: "Carburateur monocorps",
    1009: "Klaxon à soufflet",
    1010: "Déflecteur rayé",
    #spoiler accessory names
    2000: "Aileron espace",
    2001: "Roue de secours avec rustines",
    2002: "Arceau de sécurité",
    2003: "Ailette simple",
    2004: "Double aileron",
    2005: "Aileron simple",
    2006: "Roue de secours standard",
    2007: "Ailette simple",
    2008: "sp9",
    2009: "sp10",
    #front wheel well accessory names
    3000: "Klaxon 2 tons",
    3001: "Pare-chocs de Freddie",
    3002: "Bas de caisse Cobalt",
    3003: "Pots latéraux Cobra",
    3004: "Pots latéraux droits",
    3005: "Pare-chocs dentelés",
    3006: "Bas de caisse carbone",
    3007: "Bas de caisse bois",
    3008: "fw9",
    3009: "fw10",
    #rear wheel well accessory names (twisty twisty)
    4000: "Pots arrières courbés",
    4001: "Pare-chocs Splash",
    4002: "Double échappement",
    4003: "Doubles ailettes simples",
    4004: "Bavettes simples",
    4005: "Échappement de quad",
    4006: "Doubles élargisseurs de caisse",
    4007: "Méga échappement",
    4008: "Doubles ailettes rayées",
    4009: "Doubles ailettes bulle",
    4010: "Bavettes rayées",
    4011: "Bavettes Mickey",
    4012: "Bavettes dentelées",
    #rim accessoKartRace_Exit = "Leave Race"ry names
    5000: "Turbo",
    5001: "Lune",
    5002: "Roue avec rustine",
    5003: "Trois rayons",
    5004: "Couvercle peinture",
    5005: "Cœur",
    5006: "Mickey",
    5007: "Cinq boulons",
    5008: "Daisy",
    5009: "Basket-ball",
    5010: "Hypno",
    5011: "Tribal",
    5012: "Pierre précieuse",
    5013: "Cinq rayons",
    5014: "Pacotille",
    #decal accessory names
    6000: "Numéro cinq",
    6001: "Éclaboussure",
    6002: "Damiers",
    6003: "Flammes",
    6004: "Cœurs",
    6005: "Bulles",
    6006: "Tigre",
    6007: "Fleurs",
    6008: "Éclair",
    6009: "Ange",
    #paint accessory names
    7000: "Vertanis",
    7001: "Pêche",
    7002: "Rouge vif",
    7003: "Rouge",
    7004: "Bordeaux",
    7005: "Sienne",
    7006: "Marron",
    7007: "Havane",
    7008: "Corail",
    7009: "Orange",
    7010: "Jaune",
    7011: "Crème",
    7012: "Citrine",
    7013: "Citron vert",
    7014: "Vert marin",
    7015: "Vert",
    7016: "Bleu clair",
    7017: "Bleuaqua",
    7018: "Bleu",
    7019: "Bleupervenche",
    7020: "Bleu roi",
    7021: "Bleu ardoise",
    7022: "Violet",
    7023: "Lavande",
    7024: "Rose",
    7025: "Gris",
    7026: "Noir",
    }

RaceHoodSpeedway = "Circuit"
RaceHoodRural = "Champêtre"
RaceHoodUrban = "Ville"
RaceTypeCircuit = "Tournoi"
RaceQualified = "Tu es qualifié(e)"
RaceSwept = "Tu les as balayés"
RaceWon = "Tu as gagné"
Race = "parcours"
Races = "parcours"
Total = "total"
GrandTouring = "Grand Tour"

def getTrackGenreString(genreId):
    genreStrings = [ "Circuit",
                     "Pays",
                     "Ville" ]
    return genreStrings[genreId].lower()

def getTunnelSignName(trackId, padId):
    # hack for bad naming!
    if trackId == 2 and padId == 0:
        return "panneau ville1_tunnel"
    elif trackId == 1 and padId == 0:
        return "panneau campagne_tunnel1"
    else:
        genreId = RaceGlobals.getTrackGenre(trackId)
        return "panneau %s_%stunnel" % (padId + 1, RaceGlobals.getTrackGenreString(genreId))

# Kart Trophy Descriptions
KartTrophyDescriptions = [
    # qualified race trophies
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceHoodSpeedway,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceHoodSpeedway,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceHoodSpeedway,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceHoodRural,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceHoodRural,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceHoodRural,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceHoodUrban,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceHoodUrban,
    RaceQualified + " pour " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceHoodUrban,
    RaceQualified + " pour " + str(RaceGlobals.TotalQualifiedRaces) + " " + Races + " au " + Total,
    # won race trophies
    RaceWon + " " +  str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceHoodSpeedway,
    RaceWon + " " +  str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceHoodSpeedway,
    RaceWon + " " +  str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceHoodSpeedway, 
    RaceWon + " " +  str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceHoodRural,
    RaceWon + " " +  str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceHoodRural,
    RaceWon + " " +  str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceHoodRural, 
    RaceWon + " " +  str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceHoodUrban,
    RaceWon + " " +  str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceHoodUrban,
    RaceWon + " " +  str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceHoodUrban, 
    RaceWon + " " + str(RaceGlobals.TotalWonRaces) + " " + Races + " au " + Total,
    #qualified circuit races
    RaceQualified + " pour " + str(RaceGlobals.WonCircuitRaces[0]) + " " + Race + " " + RaceTypeCircuit,
    RaceQualified + " pour " + str(RaceGlobals.WonCircuitRaces[1]) + " " + Races + " " + RaceTypeCircuit,
    RaceQualified + " pour " + str(RaceGlobals.WonCircuitRaces[2]) + " " + Races + " " + RaceTypeCircuit,
    # won circuit race trophies
    RaceWon + " " + str(RaceGlobals.WonCircuitRaces[0]) + " " + Race + " " +  RaceTypeCircuit,
    RaceWon + " " + str(RaceGlobals.WonCircuitRaces[1]) + " " + Races + " " +  RaceTypeCircuit,
    RaceWon + " " + str(RaceGlobals.WonCircuitRaces[2]) + " " + Races + " " +  RaceTypeCircuit,
    # swept circuit races
    RaceSwept + " dans " + str(RaceGlobals.SweptCircuitRaces[0]) + " " + Race + " " + RaceTypeCircuit,
    RaceSwept + " dans " + str(RaceGlobals.SweptCircuitRaces[1]) + " " + Races + " " + RaceTypeCircuit,
    RaceSwept + " dans " + str(RaceGlobals.SweptCircuitRaces[2]) + " " + Races + " " + RaceTypeCircuit,
    # NOTE: to be added
    GrandTouring,
    # cups (+1 laff each)
    str(RaceGlobals.TrophiesPerCup) + " Trophées gagnés aux courses de kart! Rigol-augmentation!",
    str(RaceGlobals.TrophiesPerCup * 2) + " Trophées gagnés aux courses de kart! Rigol-augmentation!",
    str(RaceGlobals.TrophiesPerCup * 3) + " Trophées gagnés aux courses de kart! Rigol-augmentation!",
    ]

KartRace_TitleInfo = "Prépare-toi pour la course"
KartRace_SSInfo = "Bienvenue au stade Cinglette!\nPied au plancher, et on s'accroche. Ça va secouer!\n"
KartRace_CoCoInfo = "Bienvenue au Colisée Tortillé ! Utilise l'inclinaison des virages pour maintenir ta vitesse !\n"
KartRace_RRInfo = "Bienvenue sur la piste Champêtre!\nAttention aux animaux, reste bien sur la piste!\n"
KartRace_AAInfo = "Bienvenue aux Landes légères ! Tiens bien ton chapeau ! Ça a l'air d'être plein de bosses par ici...\n"
KartRace_CCInfo = "Bienvenue sur le circuit de la Ville!\nAttention aux piétons quand tu fonces à travers la ville!\n"
KartRace_BBInfo = "Bienvenue au Boulevard du Blizzard ! Attention à ta vitesse. Il se peut qu'il y ait de la glace par là-bas.\n"
KartRace_GeneralInfo = "Utilise la touche Contrôle pour lancer les gags que tu ramasses sur la piste, et les flèches pour diriger ton kart."

KartRace_TrackInfo = {
  RaceGlobals.RT_Speedway_1     : KartRace_SSInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Speedway_1_rev : KartRace_SSInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Speedway_2     : KartRace_CoCoInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Speedway_2_rev : KartRace_CoCoInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Rural_1        : KartRace_RRInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Rural_1_rev    : KartRace_RRInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Rural_2        : KartRace_AAInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Rural_2_rev    : KartRace_AAInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Urban_1        : KartRace_CCInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Urban_1_rev    : KartRace_CCInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Urban_2        : KartRace_BBInfo + KartRace_GeneralInfo,
  RaceGlobals.RT_Urban_2_rev    : KartRace_BBInfo + KartRace_GeneralInfo,
  }

KartRecordStrings = {
    RaceGlobals.Daily : 'quotidien',
    RaceGlobals.Weekly : 'hebdomadaire',
    RaceGlobals.AllTime : 'de tous les temps',
    }

KartRace_FirstSuffix = 'er'
KartRace_SecondSuffix = 'ème'
KartRace_ThirdSuffix = ' rd'
KartRace_FourthSuffix = ' th'
KartRace_WrongWay = 'Sens\ninterdit!'
KartRace_LapText = "Tour %s"
KartRace_FinalLapText = "Dernier tour!"
KartRace_Exit = "Sortir de la course"
KartRace_NextRace = "Course suivante"
KartRace_Leave = "Quitter la course"
KartRace_Qualified = "Qualifié(e)!"
KartRace_Record = "Record!"
KartRace_RecordString = 'Tu as établi un nouveau %s record pour %s! Ton bonus est de %s tickets.'
KartRace_Tickets = " Tickets"
KartRace_Exclamations = "!"
KartRace_Deposit = "Dépôt"
KartRace_Winnings = "Gains"
KartRace_Bonus = "Bonus"
KartRace_RaceTotal = "Total course"
KartRace_CircuitTotal = "Circuit entier"
KartRace_Trophies = "Trophées"
KartRace_Zero = "0"
KartRace_Colon = ":"
KartRace_TicketPhrase = "%s" + KartRace_Tickets
KartRace_DepositPhrase = KartRace_Deposit + KartRace_Colon + "\n"
KartRace_QualifyPhrase = "Qualifié:\n"
KartRace_RaceTimeout = "Tu as fini après la fin de la course. Tes tickets ont été remboursés. Essaie encore!"
KartRace_RaceTimeoutNoRefund = "Tu as mis trop de temps à finir la course. Tes tickets n'ont pas été remboursés parce que le Grand Prix a déjà commencé. Essaie à nouveau !"
KartRace_RacerTooSlow = "Tu as mis trop de temps à finir la course. Tes tickets ne te sont pas remboursés. Fais une autre course !"
KartRace_PhotoFinish = "Photo à l'arrivée"
KartRace_CircuitPoints = "Score"

CircuitRaceStart = "Le Grand Prix Toontown au Circuit Dingo va commencer  ! Pour gagner la compétition, remporte le maximum de points en trois courses consécutives  !"
CircuitRaceOngoing = "Bienvenue ! Le Grand Prix de Toontown bat son plein."
CircuitRaceEnd = "Le Grand Prix Toontown est terminé pour aujourd'hui. Rendez-vous lundi prochain pour une nouvelle édition."

# Trick-or-Treat holiday
TrickOrTreatMsg = "Tu as déjà\ntrouvé cette friandise."

#temp lawbot boss dialog text
LawbotBossTempIntro0 = "Bon, on a quoi au registre aujourd'hui ?"
LawbotBossTempIntro1 = "Ha, on a le procès d'un Toon !"
LawbotBossTempIntro2 = "L'accusation a de bonnes cartes."
LawbotBossTempIntro3 = "Et voilà les avocats commis d'office."
LawbotBossTempIntro4 = "Attendez une minute... Vous êtes des Toons !"
LawbotBossTempJury1 = "La sélection du jury va maintenant commencer."
LawbotBossHowToGetEvidence = "Touche la barre des témoins pour obtenir des preuves."
LawbotBossTrialChat1 = "La séance est ouverte."
LawbotBossHowToThrowPies = "Appuie sur la touche « Inser » pour envoyer les preuves\n sur les avocats ou dans la balance !"
LawbotBossNeedMoreEvidence = "Il te faut plus de preuves !"
LawbotBossDefenseWins1 = "Ce n'est pas possible ! La défense a gagné ?"
LawbotBossDefenseWins2 = "Non. Je déclare le procès nul ! Un nouveau procès va être programmé."
LawbotBossDefenseWins3 = "Hmmmpfff. Je serai dans mon cabinet !"
LawbotBossProsecutionWins = "Je suis en faveur du plaignant"
LawbotBossReward = "Je décerne une promotion et le pouvoir de convoquer des Cogs"
LawbotBossLeaveCannon = "Laisse le canon"
LawbotBossPassExam = "Alors comme ça, tu as réussi le concours du barreau."
LawbotBossTaunts = [
    "%s, je te trouve coupable d'outrage à la cour !",
    "Objection accordée !",
    "Rayez ça du procès-verbal.",
    "Ton appel a été rejeté. Je te condamne à la tristesse !",
    "Silence dans l'audience !",
    ]
LawbotBossAreaAttackTaunt = "Vous êtes tous coupables d'outrage à la cour!"
WitnessToonName = "Bumpy Bourdonnette"
WitnessToonPrepareBattleTwo = "Oh non! Il n'y a que des Cogs dans le jury!\aVite, utilise les canons et tire sur des jurés Toons sur le banc des jurés.\aNous avons besoin de %d pour équilibrer la balance."
WitnessToonNoJuror = "Oh là là, aucun juré Toon. Ça va être un procès difficile."
WitnessToonOneJuror = "Super! Il y a 1Toon parmi les jurés!"
WitnessToonSomeJurors = "Super! Il y a %d Toons parmi les jurés!"
WitnessToonAllJurors = "Fantastique! Tous les jurés sont des Toons!"
WitnessToonPrepareBattleThree = "Dépêche-toi de toucher la barre des témoins pour obtenir des preuves.\aAppuie sur la touche «Inser» pour envoyer les preuves sur les avocats ou sur la défense."
WitnessToonCongratulations = "Tu as réussi! Merci pour cette défense spectaculaire!\aPrends ces papiers que le Juge a oubliés.\aAvec ça, tu pourras convoquer des Cogs à partir de ta page de Galerie de Cogs."
WitnessToonLastPromotion = "\aWow, tu as atteint le niveau %s sur ton costume de Cog!\aC'est la plus haute promotion que peuvent atteindre les Cogs.\aTu ne peux plus monter ton costume de Cog en grade, mais tu peux évidemment continuer à travailler pour la résistance!"
WitnessToonHPBoost = "\aTu as fait beaucoup de travail pour la résistance.\aLe Conseil des Toons a décidé de te donner un autre rigolpoint. Félicitations!"
WitnessToonMaxed = "\aJe vois que tu as un costume de Cog de niveau %s. Très impressionnant!\aLe Conseil des Toons te remercie d'être revenu défendre encore plus de Toons!"
WitnessToonBonus = "Merveilleux! Tous les avocats sont étourdis. Le poids de tes preuves est %s fois plus lourd pendant %s secondes."

WitnessToonJuryWeightBonusSingular = {
  6: "C'est un cas difficile. Tu as %d juré Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
  7: "C'est un cas très difficile. Tu as %d juré Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
  8: "C'est le cas le plus difficile. Tu as %d juré Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
}

WitnessToonJuryWeightBonusPlural = {
  6: "C'est un cas difficile. Tu as %d jurés Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
  7: "C'est un cas très difficile. Tu as %d jurés Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
  8: "C'est le cas le plus difficile. Tu as %d jurés Toon. Par conséquent, tes preuves ont un bonus de poids de %d.",
}

# Cog Summons stuff
IssueSummons = "Convocation"
SummonDlgTitle = "Convoquer un Cog"
SummonDlgButton1 = "Convoquer un Cog"
SummonDlgButton2 = "Assigner un bâtiment Cog"
SummonDlgButton3 = "Convoquer une invasion de Cogs"
SummonDlgSingleConf = "Veux-tu convoquer un %s?"
SummonDlgBuildingConf = "Veux-tu convoquer un %s à se rendre dans un bâtiment Toon à proximité?"
SummonDlgInvasionConf = "Veux-tu convoquer une invasion de %s?"
SummonDlgNumLeft = "Il t'en reste %s."
SummonDlgDelivering = "Envoi des convocations..."
SummonDlgSingleSuccess = "Tu as réussi à convoquer le Cog."
SummonDlgSingleBadLoc = "Malheureusement, les Cogs ne sont pas autorisés à entrer ici. Essaie un autre endroit."
SummonDlgBldgSuccess = "Tu as réussi à convoquer les Cogs. %s a accepté de les laisser prendre provisoirement le contrôle de %s!"
SummonDlgBldgSuccess2 = "Tu as réussi à convoquer les Cogs. Un commerçant a accepté de les laisser prendre provisoirement le contrôle de son magasin!"
SummonDlgBldgBadLoc = "Malheureusement, il n'y a aucun bâtiment Toon à proximité que les Cogs peuvent prendre."
SummonDlgInvasionSuccess = "Tu as réussi à convoquer les Cogs. C'est une invasion!"
SummonDlgInvasionBusy = "On ne trouve pas de %s pour l'instant. Essaie à nouveau quand l'invasion de Cogs sera terminée."
SummonDlgInvasionFail = "Désolé. L'invasion de Cogs a échoué."
SummonDlgShopkeeper = "Le commerçant"

# Polar Place cheesy effect chat phrases
PolarPlaceEffect1 = NPCToonNames[3306] + ": Bienvenue à la Place Polaire!"
PolarPlaceEffect2 = NPCToonNames[3306] + ": Essaie pour voir si la taille te va."
PolarPlaceEffect3 = NPCToonNames[3306] + ": Ton nouveau look ne marchera que" + lTheBrrrgh + "."

# LaserGrid game Labels
LaserGameMine = "Recherche de crâne!"
LaserGameRoll = "Correspondance"
LaserGameAvoid = "Évite les crânes"
LaserGameDrag = "Mets en trois de la même\ncouleur sur une rangée"
LaserGameDefault = "Jeu inconnu"

# Pinball text
#PinballHiScore = "High Score: %d %s\n"
#PinballYourBestScore = "Your Best Score: %d\n"
#PinballScore = "Score: %d x %d : %d"
PinballHiScore = "Score élevé: %s\n"
PinballHiScoreAbbrev = "..."
PinballYourBestScore = "Ton meilleur score:\n"
PinballScore = "Score: %d x %d ="
PinballScoreHolder = "%s\n"


# Gardening text
GagTreeFeather = "Arbre à gags à plumes"
GagTreeJugglingBalls = "Arbre à gags à balles de jonglage"
StatuaryFountain = "Fontaine"
StatuaryToonStatue = "Statue de Toon"
StatuaryDonald = "Statue de Donald"
StatuaryMinnie = "Statue de Minnie"
StatuaryMickey1 = "Statue de Mickey"
StatuaryMickey2 = "Fontaine de Mickey"
StatuaryToonStatue = "Statue de Toon"
StatuaryToon = "Toon Statue"
StatuaryToonWave = "Statue Toon Geste"
StatuaryToonVictory = "Statue Toon Victoire"
StatuaryToonCrossedArms = 'Statue Toon Autorité'
StatuaryToonThinking = 'Statue Toon Étreinte'
StatuaryMeltingSnowman = 'Melting Snowman'
StatuaryGardenAccelerator = "Engrais Pousse-Instantanée"
#see GardenGlobals.py for corresponding FlowerColors
FlowerColorStrings = ['Rouge','Orange','Violet','Bleu','Rose','Jaune','Blanc','Vert']
#see GardenGlobals.py for PlantAttributes, keys must match
FlowerSpeciesNames = {
    49: 'Pâquerette',
    50: 'Tulipe',
    51: 'Œillet',
    52: 'Lys',
    53: 'Jonquille',
    54: 'Pensée',
    55: 'Pétunia',
    56: 'Rose',
    }
#see GardenGlobals.py for PlantAttributes, keys must match, varieties must match
FlowerFunnyNames = {
    49: ("Pâquerette d'école",
         'Pâquerette paresseuse',
         "Pâquerette d'été",
         'Pâquerette frisquette',
         'Pâquerette houplàlà',
         'Pâquerette guillerette',
         'Pâquerette follette',
         'Pâquerette brumette',
         ),
    50: ('Unelipe',
          'Tulipe',
          'Trilipe',
          ),
    51: ('Œillet myope',
         'Œillet rapide',
         'Œillet hybride',
         'Œillet louche',
         'Œillet modèle',
          ),
    52: ('Mugatine',
         'Lys téria',
         'Lys tigri',
         'Lys poire',
         'Lys pique',
         'Pneu-lys',
         'Lys tère',
         'Lys bis',
         ),
    53: ('Jonquirille',
         'Jonquifolle',
         'Jonquirafe',
         'Jonquipasse',
         ),
    54: ('Pensée à rien',
         'Chim-pensée',
         'Pensée zy',
         'Pensargarine',
         'Pensée folle'
         ),
    55: ('Pétugniagnian',
         'Régitunia',
         ),
    56: ("Rose estivale",
         'Rose des blés',
         'Rose colorante',
         'Rose malodorante',
         'Rose distillée',
         ),
    }
FlowerVarietyNameFormat = "%s %s"
FlowerUnknown = "????"
ShovelNameDict = {
    0 : "Étain",
    1 : "Bronze",
    2 : "Argent",
    3 : "Or",
    }
WateringCanNameDict = {
    0 : "Petit",
    1 : "Moyen",
    2 : "Grand",
    3 : "Énorme",
    }
GardeningPlant = "Plante"
GardeningWater = "Eau"
GardeningRemove = "Retirer"
GardeningPick = "Cueillir"
GardeningFull = "Full"
GardeningSkill = "Habileté"
GardeningWaterSkill = "Habileté à arroser"
GardeningShovelSkill = "Habileté avec la pelle"
GardeningNoSkill = "Pas d'habileté améliorée"
GardeningPlantFlower = "Plante\nFleur"
GardeningPlantTree = "Plante\nArbre"
GardeningPlantItem = "Plante\nArticle"
PlantingGuiOk = "Plante"
PlantingGuiCancel = "Annuler"
PlantingGuiReset = "Tout effacer"
GardeningChooseBeans = "Choisis les bonbons que tu veux planter"
GardeningChooseBeansItem  = "Choisis les bonbons que tu veux planter."
GardeningChooseToonStatue = "Choisis le Toon dont tu veux créer la statue."
GardenShovelLevelUp = "Félicitations, tu as gagné une pelle %(shovel)s ! Tu as maîtrisé les fleurs de %(oldbeans)d bonbons ! Pour avancer, tu dois cueillir des fleurs de %(newbeans)d bonbons."
GardenShovelSkillLevelUp = "Félicitations ! Tu as maîtrisé les fleurs de %(oldbeans)d bonbons ! Pour avancer, tu dois cueillir des fleurs de %(newbeans)d bonbons."
GardenShovelSkillMaxed = "Extraordinaire ! Tu as explosé ton habileté avec la pelle !"

GardenWateringCanLevelUp = "Félicitations, tu as gagné un nouvel arrosoir!"
GardenMiniGameWon = "Félicitations, tu as arrosé la plante!"
ShovelTin = "Pelle d'étain"
ShovelSteel = "Pelle de bronze"
ShovelSilver = "Pelle d'argent"
ShovelGold = "Pelle d'or"
WateringCanSmall = "Petit arrosoir"
WateringCanMedium = "Arrosoir moyen"
WateringCanLarge = "Grand arrosoir"
WateringCanHuge = "Énorme arrosoir"
#make sure it matches GardenGlobals.BeanColorLetters
BeanColorWords = ('rouge', 'vert', 'orange','violet','bleu','rose','jaune',
                  'bleu de cyan','argenté')
PlantItWith = " Plante avec %s."
MakeSureWatered = " Prends d'abord soin d`arroser toutes tes plantes."
UseFromSpecialsTab = "Utilise les onglets spéciaux de ta page de jardinage."
UseSpecial = "Utilise l'outil spécial"
UseSpecialBadLocation = 'Tu ne peux utiliser cela que dans ton jardin.'
UseSpecialSuccess = 'Bravo! Les plantes que tu as arrosées viennent de pousser.'
ConfirmWiltedFlower = "Le plant de %(plant)s est fané. Veux-tu vraiment le retirer? Ce plant n'ira pas dans ton panier de fleurs, et ton habileté n'augmentera pas."
ConfirmUnbloomingFlower = "Le plant de %(plant)s ne fleurit pas. Veux-tu vraiment le retirer? Ce plant n'ira pas dans ton panier de fleurs, et ton habileté n'augmentera pas."
ConfirmNoSkillupFlower = "Veux-tu vraiment cueillir le plant de %(plant)s? Ce plant ira dans ton panier de fleurs, mais ton habileté n'augmentera PAS."
ConfirmSkillupFlower = "Veux-tu vraiment cueillir le plant de %(plant)s? Il ira dans ton panier de fleurs. Ton habileté augmentera aussi."
ConfirmMaxedSkillFlower = "Veux-tu vraiment cueillir le plant de %(plant)s? Il ira dans ton panier de fleurs. Ton habileté n'augmentera PAS car elle est déjà au maximum."
ConfirmBasketFull = "Ton panier de fleurs est plein. Tu dois d'abord vendre des fleurs."
ConfirmRemoveTree = "Veux-tu vraiment retirer le pied de %(tree)s?"
ConfirmWontBeAbleToHarvest = " Si tu retires cet arbre, tu ne pourras pas récolter de gags dans les arbres de plus haut niveau."
ConfirmRemoveStatuary = "Veux-tu vraiment supprimer définitivement le plant de %(plant)s?"
ResultPlantedSomething  = "Félicitations ! Tu viens de planter un %s."
ResultPlantedSomethingAn  = "Félicitations ! Tu viens de mettre en terre un plant de %s."
ResultPlantedNothing = "Ça n'a pas marché. Essaie une nouvelle combinaison de bonbons."

GardenGagTree = "Arbre à gags"
GardenUberGag = "Über Gag"

def getRecipeBeanText(beanTuple):
    """
    given a bean tuple, e.g (0,6) return a text version of it to
    be displayed to the user. e.g( a red and yellow jellybean)
    """
    #first check if all the beans are the same, so we can say something
    #like 7 red jellybeans
    retval = ""
    if not beanTuple:
        return retval
    allTheSame = True
    for index in range(len( beanTuple)):
        if index + 1 < len(beanTuple):
            if not beanTuple[index] == beanTuple[index+1]:
                allTheSame = False
                break

    if allTheSame:
        if len(beanTuple) > 1:
            retval = "%d bonbons %s" % (len(beanTuple),
                                           BeanColorWords[beanTuple[0]])
        else:
            retval = "un bonbon %s" % BeanColorWords[beanTuple[0]]
    else:
        retval += 'un'
        maxBeans = len(beanTuple)
        for index in range(maxBeans):
            if index == maxBeans - 1:
                retval += " et un bonbon %s" % BeanColorWords[beanTuple[index]]
            elif index == 0:
                retval += " %s" % BeanColorWords[beanTuple[index]]
            else:
                retval += ", %s" % BeanColorWords[beanTuple[index]]

    return retval

GardenTextMagicBeans = "Bonbons magiques"
GardenTextMagicBeansB = "Quelques autres bonbons"
GardenSpecialDiscription = "Ce texte doit expliquer comment utiliser un certain outil spécial pour le jardin"
GardenSpecialDiscriptionB = "Ce texte doit expliquer comment utiliser un certain outil spécial pour le jardin, en pleine face !"
GardenTrophyAwarded = "Oh là là! Tu as cueilli %s sur %s fleurs. Ça mérite un trophée et une rigol-augmentation!"
GardenTrophyNameDict = {
    0 : "Brouette",
    1 : "Pelles",
    2 : "Fleur",
    3 : "Arrosoir",
    4 : "Requin",
    5 : "Poisson-scie",
    6 : "Orque",
    }
SkillTooLow = "Habileté\ntrop faible"
NoGarden = "Pas de\njardi"

def isVowelStart(str):
    """
    A utility function to return true if the first letter in the str is a vowel
    """
    retval = False
    if str and len(str)>0:
        vowels = ['A','E','I','O','U']
        firstLetter = str.upper()[0:1]
        if firstLetter in vowels:
            retval = True
    return retval

def getResultPlantedSomethingSentence( flowerName):
    """
    Returns a gramatically correct sentence when you've successfully planted something
    """
    if isVowelStart(flowerName):
        retval = ResultPlantedSomethingAn % flowerName
    else:
        retval = ResultPlantedSomething % flowerName

    return retval


#Stuff for trolley metagame
TravelGameTitle = "Les Jeudis du Tramway"
TravelGameInstructions = "Clique vers le haut ou vers le bas pour définir ton nombre de votes. Clique sur le bouton pour voter. Atteins ton objectif secret pour remporter des bonus de bonbons. Gagne plus de votes en obtenant de bons résultats dans les autres jeux."
TravelGameRemainingVotes = "Votes restants :"
TravelGameUse = "Utiliser"
TravelGameVotesWithPeriod = "votes."
TravelGameVotesToGo = "votes restants"
TravelGameVoteToGo = "votes restants"
TravelGameUp = ""
TravelGameDown = "BAS."
TravelGameVoteWithExclamation = "Vote !"
TravelGameWaitingChoices = "Attendre que les autres joueurs votent..."
# cross the bridge later when the first choice is different for each node,
# e.g. NorthWest, NorthEast, etc.
TravelGameDirections = ['HAUT', 'BAS']
TravelGameTotals = 'Totaux'
TravelGameReasonVotesPlural = 'Le tramway se dirige vers le %(dir)s, avec une avance de %(numVotes)d votes.'
TravelGameReasonVotesSingular = 'Le tramway se dirige vers le %(dir)s, avec une avance de %(numVotes)d vote.'
TravelGameReasonPlace = '%(name)s brise le lien. Le tramway se dirige vers le %(dir)s.'
TravelGameReasonRandom = 'Le tramway se dirige de manière aléatoire vers le %(dir)s.'
TravelGameOneToonVote =   "%(name)s a utilisé %(numVotes)s votes restants %(dir)s\n"
TravelGameBonusBeans = "%(numBeans)d Bonbons"
TravelGamePlaying = 'Ensuite, le %(game)s Jeu du Tramway.'
TravelGameGotBonus = '%(name)s a obtenu un bonus de %(numBeans)s bonbons !'
TravelGameNoOneGotBonus = "Personne n'a atteint son objectif secret. Chacun remporte 1 bonbon."
TravelGameConvertingVotesToBeans = ""
TravelGameGoingBackToShop ="Il reste un seul joueur. En route pour la boutique à gags de Dingo."

PairingGameTitle = "Jeu de mémoire Toon"
PairingGameInstructions = "Appuie sur Effacer pour ouvrir une carte. Pour remporter un point, il faut assortir deux cartes. Fais une combinaison avec l'éclat bonus et remporte un point en plus. Remporte des points supplémentaires en effectuant de petits lancers."
PairingGameInstructionsMulti = "Appuie sur Effacer pour ouvrir une carte. Appuie sur Ctrl pour demander à un autre joueur d'ouvrir une carte. Pour remporter un point, il faut assortir deux cartes. Fais une combinaison avec l'éclat bonus et remporte un point en plus. Remporte des points supplémentaires en effectuant de petits lancers."
PairingGamePerfect = 'PARFAIT !'
PairingGameFlips = 'Lancers :'
PairingGamePoints = 'Points :'

TrolleyHolidayStart = "Les Jeudis du Tramway est sur le point de commencer. Pour jouer, monte à bord de n'importe quel tramway contenant au moins deux Toons."
TrolleyHolidayOngoing = "Bienvenue ! Les Jeudis du Tramway est en cours d'exécution."
TrolleyHolidayEnd = "Les Jeudis du Tramway est terminé pour aujourd'hui. À la semaine prochaine !"

TrolleyWeekendStart = "Le Weekend du Tramway est sur le point de commencer ! Pour jouer, monte à bord de n'importe quel tramway contenant au moins deux Toons."
TrolleyWeekendEnd = "Le Weekend du Tramway est terminé pour aujourd'hui."

VineGameTitle = "Jeu des Lianes"
VineGameInstructions = "Atteins la liane la plus à droite à temps. Appuie sur les flèches Haut ou Bas du clavier pour grimper le long de la liane. Appuie sur les flèches Droite ou Gauche pour changer de direction et sauter. Plus tu es en bas de la liane, plus il est facile de sauter. Ramasse les bananes si tu peux, mais évite les chauves-souris et les araignées."

# Make sure the golf text matches up with GolfGlobals.py
GolfCourseNames = {
    0: "Marche dans le Par",
    1: "Trou joyeux",
    2: "Trou ce qu'il faut et plus encore"
    }

GolfHoleNames = {
    0: 'Trou-en-Un',
    1: 'Putt à choux',
    2: 'Cul sec',
    3: 'Ver de green',
    4: 'Liens chauds',
    5: 'Putter Pan',
    6: 'Club de Swing',
    7: 'A P Tee',
    8: 'Planter de Tee',
    9: 'Rock And Roll',
    10: 'Trou de boguey',
    11: 'Amor Tee',
    12: 'Tee Sage',
    13: 'Par Deux Nez',
    14: 'Au Drive In',
    15: 'Cours de Swing',
    16: "Terrain d'entraînement",
    17: 'Second Souffle',
    18: 'Trou-en-Un-2',
    19: 'Putt à choux -2',
    20: 'Cul sec-2',
    21: 'Ver de green-2',
    22: 'Liens chauds-2',
    23: 'Putter Pan-2',
    24: 'Club de Swing-2',
    25: 'A P Tee-2',
    26: 'Planter de Tee-2',
    27: 'Rock And Roll -2',
    28: 'Trou de boguey-2',
    29: 'Amor Tee-2',
    30: 'Tee Sage-2',
    31: 'Par Deux Nez-2',
    32: 'Au Drive In-2',
    33: 'Cours de Swing-2',
    34: "Terrain d'entraînement-2",
    35: 'Second Souffle-2',
    }

GolfHoleInOne = "Trou-en-un"
GolfCondor = "Condor" # four Under Par
GolfAlbatross = "Albatros" # three under par
GolfEagle = "Aigle" # two under par
GolfBirdie = "Birdie" # one under par
GolfPar = "Par"
GolfBogey = "Boguey" # one over par
GolfDoubleBogey = "Double Bougey" # two over par
GolfTripleBogey = "Triple Boguey" # three over par

GolfShotDesc = {
    -4: GolfCondor,
    -3: GolfAlbatross,
    -2: GolfEagle,
    -1: GolfBirdie,
    0: GolfPar,
    1: GolfBogey,
    2: GolfDoubleBogey,
    3: GolfTripleBogey,
    }


from toontown.golf import GolfGlobals

CoursesCompleted = "Parcours terminés"
CoursesUnderPar = "Parcours sous par"
HoleInOneShots = "Trous-en-un"
EagleOrBetterShots = "Aigle ou meilleurs tirs"
BirdieOrBetterShots = "Birdie ou meilleurs tirs"
ParOrBetterShots = "Par ou meilleurs tirs"
MultiPlayerCoursesCompleted = "Parcours multijoueurs terminés"
TwoPlayerWins = "Victoires à deux joueurs"
ThreePlayerWins = "Victoires à trois joueurs"
FourPlayerWins = "Victoires à quatre joueurs"
CourseZeroWins = GolfCourseNames[0] + " Victoires"
CourseOneWins = GolfCourseNames[1] + " Victoires"
CourseTwoWins = GolfCourseNames[2] + " Victoires"

GolfHistoryDescriptions = [
    CoursesCompleted,
    CoursesUnderPar,
    HoleInOneShots,
    EagleOrBetterShots,
    BirdieOrBetterShots,
    ParOrBetterShots,
    MultiPlayerCoursesCompleted,
    CourseZeroWins,
    CourseOneWins,
    CourseTwoWins,
    ]

GolfTrophyDescriptions = [
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesCompleted][0]) + ' ' + CoursesCompleted,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesCompleted][1]) + ' ' + CoursesCompleted,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesCompleted][2]) + ' ' + CoursesCompleted,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesUnderPar][0]) + ' ' + CoursesUnderPar,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesUnderPar][1]) + ' ' + CoursesUnderPar,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CoursesUnderPar][2]) + ' ' + CoursesUnderPar,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.HoleInOneShots][0]) + ' ' + HoleInOneShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.HoleInOneShots][1]) + ' ' + HoleInOneShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.HoleInOneShots][2]) + ' ' + HoleInOneShots,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.EagleOrBetterShots][0]) + ' ' + EagleOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.EagleOrBetterShots][1]) + ' ' + EagleOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.EagleOrBetterShots][2]) + ' ' + EagleOrBetterShots,



    str(GolfGlobals.TrophyRequirements[GolfGlobals.BirdieOrBetterShots][0]) + ' ' + BirdieOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.BirdieOrBetterShots][1]) + ' ' + BirdieOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.BirdieOrBetterShots][2]) + ' ' + BirdieOrBetterShots,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.ParOrBetterShots][0]) + ' ' + ParOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.ParOrBetterShots][1]) + ' ' + ParOrBetterShots,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.ParOrBetterShots][2]) + ' ' + ParOrBetterShots,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.MultiPlayerCoursesCompleted][0]) + ' ' + MultiPlayerCoursesCompleted,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.MultiPlayerCoursesCompleted][1]) + ' ' + MultiPlayerCoursesCompleted,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.MultiPlayerCoursesCompleted][2]) + ' ' + MultiPlayerCoursesCompleted,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseZeroWins][0]) + ' ' + CourseZeroWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseZeroWins][1]) + ' ' + CourseZeroWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseZeroWins][2]) + ' ' + CourseZeroWins,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseOneWins][0]) + ' ' + CourseOneWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseOneWins][1]) + ' ' + CourseOneWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseOneWins][2]) + ' ' + CourseOneWins,

    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseTwoWins][0]) + ' ' + CourseTwoWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseTwoWins][1]) + ' ' + CourseTwoWins,
    str(GolfGlobals.TrophyRequirements[GolfGlobals.CourseTwoWins][2]) + ' ' + CourseTwoWins,

]

GolfCupDescriptions = [
    str(GolfGlobals.TrophiesPerCup) + " Trophées remportés",
    str(GolfGlobals.TrophiesPerCup * 2) + " Trophées remportés",
    str(GolfGlobals.TrophiesPerCup * 3) + " Trophées remportés",
]

GolfAvReceivesHoleBest = "%(name)s a établi un nouveau record de parcours au  %(hole)s !"
GolfAvReceivesCourseBest = "%(name)s a établi un nouveau record de parcours au %(course)s !"
GolfAvReceivesCup = "%(name)s remporte la %(cup)s coupe ! Rigol-augmentation !"
GolfAvReceivesTrophy = "%(name)s remporte le %(award)s trophée !"
GolfRanking = "Classement : \n"
GolfPowerBarText = "%(power)s%%"
GolfChooseTeeInstructions = "Appuie sur la flèche gauche ou droite pour changer la position du tee.\nAppuie sur Ctrl pour sélectionner."
GolfWarningMustSwing = "Avertissement : tu dois appuyer sur la touche Ctrl lors de ton prochain swing."
GolfAimInstructions = "Appuie sur la flèche gauche ou droite pour viser.\nAppuie sur la touche Ctrl et maintiens-la enfoncée pour faire ton swing."
GolferExited = "%s a quitté le terrain de golf."
GolfPowerReminder = "Maintiens la touche Ctrl enfoncée plus longtemps pour \nEnvoyer la balle plus loin"


# GolfScoreBoard.py
GolfPar = "Par"
GolfHole = "Trou"
GolfTotal = "Total"
GolfExitCourse = "Quitter parcours"
GolfUnknownPlayer = "???"

# GolfPage.py
GolfPageTitle = "Golf"
GolfPageTitleCustomize = "Personnaliseur de golf"
GolfPageTitleRecords = "Meilleurs records personnels"
GolfPageTitleTrophy = "Trophées de golf"
GolfPageCustomizeTab = "Personnaliser"
GolfPageRecordsTab = "Records"
GolfPageTrophyTab = "Trophée"
GolfPageTickets = "Tickets :"
GolfPageConfirmDelete = "Effacer un accessoire&nbsp;?"
GolfTrophyTextDisplay = "Trophée %(number)s : %(desc)s"
GolfCupTextDisplay = "Coupe %(number)s : %(desc)s"
GolfCurrentHistory = "Actuel %(historyDesc)s : %(num)s"
GolfTieBreakWinner = "%(name)s remporte le jeu décisif aléatoire !"
GolfSeconds = " - %(time))2f secondes"
GolfTimeTieBreakWinner = "%(name)s remporte le jeu décisif de temps de visée total !!!"



RoamingTrialerWeekendStart = "Visiter Toontown va commencer ! Les joueurs libres peuvent à présent se rendre dans n'importe quel quartier !"
RoamingTrialerWeekendOngoing = "Bienvenue dans Visiter Toontown ! Les joueurs libres peuvent à présent se rendre dans n'importe quel quartier !"
RoamingTrialerWeekendEnd = "Visiter Toontown est maintenant terminé."

# change double if ToontownBattleGlobals.getMoreXpHolidayMultiplier() changes
MoreXpHolidayStart = "Bonne nouvelle ! L'expérience exclusive de double gag Test Toon a commencé."
MoreXpHolidayOngoing = "Bienvenue ! L'expérience exclusive de double gag Test Toon est en cours."
MoreXpHolidayEnd = "L'expérience exclusive de double gag Test Toon est terminée. Merci de nous avoir aidé à tester des trucs !"


LogoutForced = "Tu as fait une erreur\n et as été automatiquement déconnecté(e).\n Il se peut également que ton compte soit gelé.\n Sors et va faire une balade. C'est amusant."

# DistributedCountryClub.py
CountryClubToonEnterElevator = "%s \na sauté dans la voiturette de golf."
CountryClubBossConfrontedMsg = "%s se bat contre le Président du Club !"

# DistributedElevatorFSM.py
ElevatorBlockedRoom = "Tous les adversaires doivent être vaincus."

# DistributedMolefield.py
MolesLeft = "Taupes restantes : %d"
MolesInstruction = "Écrasement de taupes !\nSaute sur les taupes rouges !"
MolesFinished = "Écrasement de taupe réussi !"
MolesRestarted = "Écrasement de taupe manqué ! Recommence..."

# DistributedGolfGreenGame.py
BustACogInstruction = "Retirer la balle de Cog !"
BustACogExit = "Quitter pour le moment"
BustACogHowto = "Comment jouer"
BustACogFailure = "Temps expiré !"
BustACogSuccess = "Bien joué !"

# bossbot golf green games
GolfGreenGameScoreString = "Énigmes restantes : %s"
GolfGreenGamePlayerScore = "Résolu %s"
GolfGreenGameBonusGag = "Tu as gagné %s !"
GolfGreenGameGotHelp = "%s a résolu une énigme !"

GolfGreenGameDirections = "Lance les balles à l'aide de la souris\n\n\nSi tu parviens à regrouper trois balles de la même couleur, les balles tombent\n\n\nFais disparaître toutes les balles de Cog du tableau"

# DistributedMaze.py
enterHedgeMaze = "Retrouve vite la sortie du labyrinthe\n pour obtenir un bonus de rigolpoints !"
toonFinishedHedgeMaze = "%s \n a fini en %s position !"
hedgeMazePlaces = ["première","deuxième","troisième","quatrième"]
mazeLabel = "Le jeu du labyrinthe !"

# Boarding Party
BoardingPartyReadme = "グループを設定する？"
BoardingGroupHide = 'Hide'
BoardingGroupShow = 'Show Boarding Group'
BoardingPartyInform = "他のトゥーンをクリックして、一緒にエレベーターに乗るグループのメンバーに招待しよう。\nメンバーは%s人までだよ。"
BoardingPartyTitle = 'Boarding Group'
QuitBoardingPartyLeader = 'Disband'
QuitBoardingPartyNonLeader = 'Leave'
QuitBoardingPartyConfirm = 'Are you sure you want to quit this Boarding Group?'
BoardcodeMissing = 'Your group cannot board because something was missing.'
BoardcodeMinLaffLeader = 'Your group cannot board because you have less than %s laff points.'
BoardcodeMinLaffNonLeaderSingular = 'Your group cannot board because %s has less than %s laff points.'
BoardcodeMinLaffNonLeaderPlural = 'Your group cannot board because %s have less than %s laff points.'
BoardcodePromotionLeader = 'Your group cannot board because you do not have enough promotion merits.'
BoardcodePromotionNonLeaderSingular = 'Your group cannot board because %s does not have enough promotion merits.'
BoardcodePromotionNonLeaderPlural = 'Your group cannot board because %s do not have enough promotion merits.'
BoardcodeSpace = 'Your group cannot board because there is not enough space.'
BoardcodeBattleLeader = 'Your group cannot board beacause you are in battle.'
BoardcodeBattleNonLeaderSingular = 'Your group cannot board beacause %s is in battle.'
BoardcodeBattleNonLeaderPlural = 'Your group cannot board beacause %s are in battle.'
BoardingInviteMinLaffInviter = 'You need %s Laff Points before being a member of this Boarding Group.'
BoardingInviteMinLaffInvitee = '%s needs %s Laff Points before being a member of this Boarding Group.'
BoardingInvitePromotionInviter = 'You need to earn a promotion before being a member of this Boarding Group.'
BoardingInvitePromotionInvitee = '%s needs to earn a promotion before being a member of this Boarding Group.'
BoardingGo = 'GO'
And = 'and'
BoardingGoingTo = 'Going To:'

# DistributedBossbotBoss.py
BossbotBossName = "DirecteurDirecteur"
BossbotRTWelcome = "Tes Toons auront besoin de différents déguisements."
BossbotRTRemoveSuit = "Tout d'abord, enlève les costumes de Cog"
BossbotRTFightWaiter = "puis attaque les serveurs."
BossbotRTWearWaiter = "Bon travail ! À présent, enfile les vêtements du serveur."
BossbotBossPreTwo1 = "Pourquoi mets-tu autant de temps ?"
BossbotBossPreTwo2 = "Dépêche-toi et sers mon banquet !"
BossbotRTServeFood1 = "Hé, sers les plats que je pose sur ces tapis déroulants."
BossbotRTServeFood2 = "Si tu sers un Cog trois fois de suite, il explose."
BossbotResistanceToonName = "Ce bon vieux Gilles Giggles"
BossbotPhase3Speech1 = "Qu'est-ce qui se passe ici ?!"
BossbotPhase3Speech2 = "Ces serveurs sont des Toons !"
BossbotPhase3Speech3 = "Attrapez-les !!!"
BossbotPhase4Speech1 = "Si je veux que le travail soit bien fait"
BossbotPhase4Speech2 = "je le fais moi-même."
BossbotRTPhase4Speech1 = "Bon travail ! À présent, éclabousse le Directeur avec l'eau placée sur les tables..."
BossbotRTPhase4Speech2 = "ou utilise des balles de golf pour le ralentir."
BossbotPitcherLeave = "Laisser bouteille"
BossbotPitcherLeaving = "Laisse bouteille"
BossbotPitcherAdvice = "Utilise les flèches droite et gauche pour pivoter.\nMaintiens la touche Ctrl pour augmenter la puissance.\nRelâche la touche Ctrl pour tirer."
BossbotGolfSpotLeave = "Laisser balle de golf"
BossbotGolfSpotLeaving = "Laisse balle de golf\nUtilise les flèches droite et gauche pour pivoter.\nCtrl pour tirer."
BossbotGolfSpotAdvice = " "
BossbotRewardSpeech1 = "Non ! Le Président ne va pas apprécier."
BossbotRewardSpeech2 = "Arrrggghhh !!!"
BossbotRTCongratulations = "Tu as réussi. Tu a rétrogradé le Directeur !\aTiens, prends ces Avis de licenciement oubliés par le Directeur.\aTu pourras les utiliser pour licencier les Cogs durant un combat."""
BossbotRTLastPromotion = "\aOuah, tu as atteint le niveau %s de costume de Cog !\aLes Cogs ne peuvent pas monter plus en grade. \aTu ne peux plus mettre ton costume de Cog à niveau mais tu peux continuer de travailler pour la Résistance !"""
BossbotRTHPBoost = "\aTu as fait beaucoup pour la Résistance.\aLe Conseil des Toons a décidé de te donner un autre rigolpoint. Félicitations !"""
BossbotRTMaxed = "\aJe vois que tu as un costume de Cog de niveau %s. Très impressionnant !\aLe Conseil des Toons te remercie de revenir pour défendre d'autres Toons !"""
GolfAreaAttackTaunt = "Attention !"
OvertimeAttackTaunts = [ "Il est temps de nous réorganiser.",
                        "Réduisons les effectifs."]

#ElevatorDestination Names
ElevatorBossBotBoss = "Combat Directeur"
ElevatorBossBotCourse = "Parcour de Golf Cog"
ElevatorBossBotCourse0 = "The Front Three"
ElevatorBossBotCourse1 = "The Middle Six"
ElevatorBossBotCourse2 = "The Back Nine"
ElevatorCashBotBoss = "C.F.O Battle"
ElevatorCashBotMint0 = "Coin Mint"
ElevatorCashBotMint1 = "Dollar Mint"
ElevatorCashBotMint2 = "Bullion Mint"
ElevatorSellBotBoss = "Sellbot Battle"
ElevatorSellBotFactory0 = "Front Entrance"
ElevatorSellBotFactory1 = "Back Entrance"
ElevatorLawBotBoss = "Chief Justice Battle"
ElevatorLawBotCourse0 = "Office A"
ElevatorLawBotCourse1 = "Office B"
ElevatorLawBotCourse2 = "Office C"
ElevatorLawBotCourse3 = "Office D"


# CatalogNameTagItem.py
DaysToGo = "Attendre\n%s Jours"

# DistributedIceGame.py
IceGameTitle = "Glissade sur glace"
IceGameInstructions = "Rapproche-toi le plus possible du centre vers la fin de la seconde manche. Utilise les flèches du clavier pour changer de direction et de puissance. Appuie sur la touche Ctrl pour propulser ton Toon. Touche les tonneaux pour remporter des points supplémentaires et évite le TNT&nbsp;!"
IceGameInstructionsNoTnt = "Rapproche-toi le plus possible du centre vers la fin de la seconde manche. Utilise les flèches du clavier pour changer de direction et de puissance. Appuie sur la touche Ctrl pour propulser ton Toon. Touche les tonneaux pour remporter des points supplémentaires."
IceGameWaitingForPlayersToFinishMove = "En attente des autres joueurs..."
IceGameWaitingForAISync = "En attente des autres joueurs..."
IceGameInfo= "Match %(curMatch)d/%(numMatch)d, Manche %(curRound)d/%(numRound)d"
IceGameControlKeyWarning="N'oublie pas d'appuyer sur la touche Ctrl !"


#DistributedPicnicTable.py
PicnicTableJoinButton = "Rejoindre"
PicnicTableObserveButton = "Observer"
PicnicTableCancelButton = "Annnuler"
PicnicTableTutorial = "Comment jouer"
PicnicTableMenuTutorial = "À quel jeu veux-tu apprendre à jouer ?"
PicnicTableMenuSelect = "À quel jeu veux-tu jouer ?\nSe lever"

#DistributedChineseCheckers.py
ChineseCheckersGetUpButton = " "
ChineseCheckersStartButton = "Commencer jeu"
ChineseCheckersQuitButton = "Quitter jeu"
ChineseCheckersIts = "C'est"

ChineseCheckersYourTurn = "Ton tour"
ChineseCheckersGreenTurn = "Le tour des verts"
ChineseCheckersYellowTurn = "Le tour des jaunes"
ChineseCheckersPurpleTurn = "Le tour des violets"
ChineseCheckersBlueTurn = "Le tour des bleus"
ChineseCheckersPinkTurn = "Le tour des roses"
ChineseCheckersRedTurn = "Le tour des rouges"

ChineseCheckersColorG = "Tu es vert"
ChineseCheckersColorY = "Tu es jaune"
ChineseCheckersColorP = "Tu es violet"
ChineseCheckersColorB = "Tu es bleu"
ChineseCheckersColorPink = "Tu es rose"
ChineseCheckersColorR = "Tu es rouge"
ChineseCheckersColorO = "Tu observes"

ChineseCheckersYouWon = "Tu viens de remporter une partie de dames chinoises !"
ChineseCheckers = "Dames chinoises."
ChineseCheckersGameOf = "vient de remporter une partie de"

#GameTutorials.py
ChineseTutorialTitle1 = "But"
ChineseTutorialTitle2 = "Comment jouer"
ChineseTutorialPrev = "Page précédente"
ChineseTutorialNext = "Page suivante"
ChineseTutorialDone = "Terminé"
ChinesePage1 = "Le but du jeu des dames chinoises est d'être le premier joueur à déplacer toutes ses billes du triangle en bas du tableau vers le triangle en haut du tableau. Le premier joueur qui réussit a gagné. \n"
ChinesePage2 = "Chacun à son tour, les joueurs déplacent une bille de leur couleur. Celle-ci peut être placée dans un trou adjacent ou sauter par-dessus d'autres billes. Les sauts doivent passer au-dessus d'une bille et atterrir dans un trou vide. Il est possible d'enchaîner des sauts pour des mouvements plus longs."

CheckersPage1 = "Le but du jeu de dames est de coincer l'adversaire pour qu'il ne puisse plus bouger. Pour ce faire, tu peux capturer toutes ses pièces ou les bloquer de manière à ce qu'il soit coincé et ne puisse plus bouger."
CheckersPage2 = "Chacun leur tour, les joueurs déplacent une pièce de leur couleur. Celle-ci peut être déplacée en diagonale ou vers l'avant. Elle peut uniquement avancer sur un carré ne contenant pas de pièce. Les règles sont les mêmes pour les dames, mais elles peuvent aller en arrière."
CheckersPage3 = "Pour capturer la pièce d'un adversaire, tu dois sauter par-dessus en diagonale et te placer dans le carré vide de l'autre côté. Si tu as la possibilité de faire des sauts durant un tour, tu dois exécuter l'un d'entre eux. Tu peux enchaîner les sauts, dans la mesure où tu utilises la même pièce."
CheckersPage4 = "Une pièce devient dame lorsqu'elle atteint la dernière rangée du tableau. Une pièce qui vient de devenir dame doit attendre le prochain tour pour pouvoir sauter. En outre, les dames ont le droit de se déplacer dans toutes les directions et peuvent changer de direction durant un saut."



#DistributedCheckers.py
CheckersGetUpButton = "Se lever"
CheckersStartButton = "Commencer jeu"
CheckersQuitButton = "Quitter jeu"
CheckersIts = "C'est"
CheckersYourTurn = "Ton tour"
CheckersWhiteTurn = "Le tour des blancs"
CheckersBlackTurn = "Le tour des noirs"

CheckersColorWhite = "Tu es blanc"
CheckersColorBlack = "Tu es noir"
CheckersObserver = "Tu observes"
RegularCheckers = "Jeu de dames."
RegularCheckersGameOf = "vient de remporter une partie de"
RegularCheckersYouWon = "Tu viens de remporter une partie de dames !"

MailNotifyNewItems = "Tu as reçu un e-mail !"
MailNewMailButton = "E-mail"
MailSimpleMail = "Note"
MailFromTag = "Note de : %s"

# MailboxScreen.py
InviteInvitation = "the invitation"
InviteAcceptInvalidError = "L'invitation n'est plus valide."
InviteAcceptPartyInvalid = "La fête a été annulée."
InviteAcceptAllOk = "L'hôte a été informé de ta réponse"
InviteRejectAllOk = "The host has been informed that you declined the invitation."


# Note Months is 1 based, to correspond to datetime
Months = {
 1: "JANUARY",
 2: "FEBRUARY",
 3: "MARCH",
 4: "APRIL",
 5: "MAY",
 6: "JUNE",
 7: "JULY",
 8: "AUGUST",
 9: "SEPTEMBER",
10: "OCTOBER",
11: "NOVEMBER",
12: "DECEMBER"
}

# Note 0 for Monday to match datetime
DayNames = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DayNamesAbbrev = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

# numbers must match holiday ids in ToontownGlobals
HolidayNamesInCalendar = {
    1: ("Summer Fireworks", "Celebrate Summer with a fireworks show every hour in each playground!"),
    2: ("New Year Fireworks", "Happy New Year! Enjoy a fireworks show every hour in each playground!"),
    3: ("Bloodsucker Invasion", "Happy Halloween! Stop the Bloodsucker Cogs from invading Toontown!"),
    4: ("Winter Holidays Decor", "Celebrate the Winter Holidays with Toontastic trees and streetlights!"),
    5: ("Skelecog Invasion", "Stop the Skelecogs from invading Toontown!"),
    6: ("Mr. Hollywood Invasion", "Stop the Mr. Hollywood Cogs from invading Toontown!"),
    7: ("Fish Bingo", "Fish Bingo Wednesday! Everyone at the pond works together to complete the card before time runs out."),
    8: ("Toon Species Election", "Vote on the new Toon species! Will it be Goat? Will it be Pig?"),
    9: ("Black Cat Day", "Happy Halloween! Create a Toontastic Black Cat Toon - Today Only!"),
   13: ("Trick or Treat", "Happy Halloween! Trick or treat throughout Toontown to get a nifty Halloween pumpkin head reward!"),
   14: ("Grand Prix", "Grand Prix Monday at Goofy Speedway! To win, collect the most points in three consecutive races!"),
   17: ("Trolley Tracks", "Trolley Tracks Thursday! Board any Trolley with two or more Toons to play."),
   19: ("Silly Saturdays", "Saturdays are silly with Fish Bingo, Grand Prix, and Trolley Tracks throughout the day!"),
   24: ("Ides of March", "Beware the Ides of March! Stop the Backstabber Cogs from invading Toontown!"),
   26: ("Halloween Decor", "Celebrate Halloween as spooky trees and streetlights transform Toontown!"),
    }
UnknownHoliday = "Unknown Holiday %d" 
