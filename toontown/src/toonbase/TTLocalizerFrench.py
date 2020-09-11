import string
from LocalizerFrenchProperty import *

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
ExtraKeySanityCheck = "Ignore me"

InterfaceFont = 'phase_3/models/fonts/ImpressBT.ttf'
SuitFont = 'phase_3/models/fonts/vtRemingtonPortable.ttf'
SignFont = 'phase_3/models/fonts/MickeyFont'
MinnieFont = 'phase_3/models/fonts/MinnieFont'
BoldFont = 'phase_3/models/fonts/MickeyFont'
BoldShadow = None

# common names
Mickey = "Mickey"
Minnie = "Minnie"
Donald = "Donald"
Daisy  = "Daisy"
Goofy  = "Dingo"
Pluto  = "Pluto"
Flippy = "Flippy"

# common locations
lTheBrrrgh = 'Glagla'
lDaisyGardens = 'Jardin de Daisy'
lDaisyGardensNC = 'jardin de Daisy'
lDonaldsDock = 'Quais Donald'
lDonaldsDockNC = 'quais Donald'
lDonaldsDreamland = 'Pays des rêves de Donald'
lMinniesMelodyland = 'Pays musical de Minnie'
lToontownCentral = 'Toontown centre'
lToonHQ = 'QG des Toons'

# common strings
lCancel = 'Annuler'
lClose = 'Fermer'
lOK = 'OK'
lNext = 'Suivant'
lQuit = 'Quitter'
lYes = 'Oui'
lNo = 'Non'

lHQOfficerF = 'Officier QG'
lHQOfficerM = 'Officier QG'

MickeyMouse = "Mickey"

AIStartDefaultDistrict = "Idioville"

Cog  = "Cog"
Cogs = "Cogs"
ACog = "un Cog"
TheCogs = "Les Cogs"
theCogs = "les Cogs"
Skeleton = "Skelecog"
SkeletonP = "Skelecogs"
ASkeleton = "un Skelecog"
Foreman = "Contremaître de l'usine"
ForemanP = "Contremaîtres de l'usine"
AForeman = "un contremaître de l'usine"
CogVP = "Vice-Président " + Cog
CogVPs = "Vice-Présidents " + Cogs
ACogVP = "Un Vice-Président " + Cog

# Quests.py
TheFish = "les poissons"
AFish = "un poisson"
Level = "niveau"
QuestsCompleteString = "Terminé"
QuestsNotChosenString = "Non choisi"
Period = "."

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
                       "Puis-je t'aider?",
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
                       "Tu peux en savoir plus sur un  " + Cog + " en cliquant sur lui."
                       "Trouve des trésors sur les terrains de jeux pour remplir ton rigolmètre.",
                       "Les immeubles " + Cog + " sont dangereux! N'y va pas tout seul!",
                       "Lorsque tu perds un combat, les " + Cogs + " prennent tous tes gags."
                       "Pour avoir plus de gags, joue aux jeux du tramway!",
                       "Tu peux accumuler des rigolpoints en effectuant des défitoons.",
                       "Chaque défitoon te vaudra une récompense.",
                       "Certaines récompenses te permettent d'avoir plus de gags.",
                       "Si tu gagnes un combat, ton défitoon est crédité pour chaque " + Cog + " vaincu."
                       "Si tu regagnes un bâtiment " + Cog + ", retourne à l'intérieur pour recevoir un remerciement spécial de la part de son propriétaire!"
                       "Si tu appuies sur la touche \" page précédente \", tu peux regarder vers le haut!",
                       "Si tu appuies sur la touche de tabulation, tu peux voir différents points de vue de ce qui t'entoure!",
                       "Pour montrer à tes amis secrets ce que tu penses, entre un '.' avant ta pensée.",
                       "Si un " + Cog + " est assommé, il lui est plus difficile d'éviter les objets qui tombent."
                       "Chaque type de bâtiment " + Cog + " a un aspect différent."
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

QuestsCogNewbieQuestObjective = "Aide un nouveau Toon à vaincre %s"
QuestsCogNewbieQuestCaption = "Aide un nouveau Toon qui a %d rigolpoints ou moins"
QuestsCogNewbieQuestAux = "Tu dois vaincre :"
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
QuestsCogLevelQuestDescC = "%(count)s les Cogs de niveau %(level)s+"
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
QuestsFactoryQuestDescC = "%(count)s usines %(type)s "
QuestsFactoryQuestDescI = "des usines %(type)s"

QuestsRescueQuestProgress = "%(progress)s sur %(numToons)s sont sauvés"
QuestsRescueQuestHeadline = "SAUVER"
QuestsRescueQuestSCStringS = "Je dois sauver un Toon%(toonLoc)s."
QuestsRescueQuestSCStringP = "Je dois sauver des Toons%(toonLoc)s."
QuestsRescueQuestRescue = "Tu dois sauver %s"
QuestsRescueQuestRescueDesc = "%(numToons)s Toons"
QuestsRescueQuestToonS = "un Toon"
QuestsRescueQuestToonP = "Toons"
QuestsRescueQuestAux = "Tu dois sauver :"

QuestsRescueNewbieQuestObjective = "Aide un nouveau Toon à sauver %s"

QuestCogPartQuestCogPart = "Pièce de costume de Cog"
QuestsCogPartQuestFactories = "Usines"
QuestsCogPartQuestHeadline = "RÉCUPÉRER"
QuestsCogPartQuestProgressString = "%(progress)s sur %(num)s sont récupérés"
QuestsCogPartQuestString = "Récupérer %s"
QuestsCogPartQuestSCString = "Je dois récupérer %(objective)s%(location)s."
QuestsCogPartQuestAux = "Tu dois récupérer :"

QuestsCogPartQuestDesc = "une pièce de costume de Cog"
QuestsCogPartQuestDescC = "%(count)s pièces de costume de Cog"
QuestsCogPartQuestDescI = "des pièces de costume de Cog"

QuestsCogPartNewbieQuestObjective = 'Aide un nouveau Toon à récupérer %s'

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
QuestsRecoverItemQuestSeeHQSCString = "Je dois voir un officier du QG"
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
QuestsFriendQuestString = "Trouve un(e) ami(e)"

QuestsFriendNewbieQuestString = " Trouve %d amis de %d rigolpoints ou moins"
QuestsFriendNewbieQuestProgress = "%(progress)s sur %(numFriends)s sont trouvés"
QuestsFriendNewbieQuestObjective = "Deviens ami(e) avec %d nouveaux Toons"

QuestsTrolleyQuestHeadline = "TRAMWAY"
QuestsTrolleyQuestSCString = "Je dois faire un tour de tramway."
QuestsTrolleyQuestString = "Fais un tour de tramway"
QuestsTrolleyQuestStringShort = "Prends le tramway"

QuestsMinigameNewbieQuestString = "%d Mini-jeux"
QuestsMinigameNewbieQuestProgress = "%(progress)s sur %(numMinigames)s ont été joués"
QuestsMinigameNewbieQuestObjective = "Jouer à %d mini-jeux avec de nouveaux Toons"
QuestsMinigameNewbieQuestSCString = "Je dois jouer aux mini-jeux avec de nouveaux Toons."
QuestsMinigameNewbieQuestCaption = "Aide un nouveau Toon qui a %d rigolpoints ou moins"
QuestsMinigameNewbieQuestAux = "Tu dois jouer :"

QuestsMaxHpReward = "Ta rigo-limite a été augmentée de %s."
QuestsMaxHpRewardPoster = "Récompense : Rigol-augmentation de %s points"

QuestsMoneyRewardSingular = "Tu obtiens 1 bonbon."
QuestsMoneyRewardPlural = "Tu obtiens %s bonbons."
QuestsMoneyRewardPosterSingular = "Récompense : 1 bonbon"
QuestsMoneyRewardPosterPlural = "Récompense : %s bonbons"

QuestsMaxMoneyRewardSingular = "Tu peux maintenant avoir 1 bonbon."
QuestsMaxMoneyRewardPlural = ".Tu peux maintenant avoir %s bonbons"
QuestsMaxMoneyRewardPosterSingular = "Récompense : Tu as 1 bonbon"
QuestsMaxMoneyRewardPosterPlural = "Récompense : Tu as %s bonbons"

QuestsMaxGagCarryReward = "Tu as un %(name)s. Tu peux maintenant avoir %(num)s gags."
QuestsMaxGagCarryRewardPoster = "Récompense : (%(num)s) %(name)s"

QuestsMaxQuestCarryReward = " Tu peux maintenant avoir %s défitoons."
QuestsMaxQuestCarryRewardPoster = "Récompense : Tu as %s défitoons"

QuestsTeleportReward = "Tu peux maintenant accéder par téléportation à %s."
QuestsTeleportRewardPoster = "Récompense : Accès par téléportation à %s"

QuestsTrackTrainingReward = "Tu peux maintenant t'entraîner pour les gags \"%s\"."
QuestsTrackTrainingRewardPoster = "Récompense : Entraînement aux gags"

QuestsTrackProgressReward = "Tu as maintenant l'image %(frameNum)s de l'animation de la série %(trackName)s."
QuestsTrackProgressRewardPoster = "Récompense : image %(frameNum)s de l'animation de la série \"%(trackName)s\""

QuestsTrackCompleteReward = "Tu peux maintenant avoir et utiliser des gags \"%s\"."
QuestsTrackCompleteRewardPoster = "Récompense : Entraînement final aux séries %s"

QuestsClothingTicketReward = "Tu peux changer de vêtements"
QuestsClothingTicketRewardPoster = "Récompense : Ticket d'habillement"

QuestsCheesyEffectRewardPoster = "Récompense : %s"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "sur ce terrain de jeux"
QuestsStreetLocationThisStreet = "sur cette rue"
QuestsStreetLocationNamedPlayground = "sur le terrain de jeux de %s"
QuestsStreetLocationNamedStreet = "sur %(toStreetName)s dans %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "Le bâtiment de %s est appelé"
QuestsLocationBuildingVerb = "qui est "
QuestsLocationParagraph = "\a\"%(buildingName)s \" %(building)s...\a...%(buildingVerb)s %(street)s."
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
    2 : ["Clé", "Clés", "une "],
    3 : ["Tableau", "Tableaux", "un "],
    4 : ["Livre", "Livres", "un "],
    5 : ["Sucre d'orge", "Sucres d'orge", "un "],
    6 : ["Craie", "Craies", "une "],
    7 : ["Recette", "Recettes", "une "],
    8 : ["Note", "Notes", "une "],
    9 : ["Machine à calculer", "Machines à calculer", "une "],
    10 : ["Pneu de voiture de clown", "Pneus de voiture de clown", "un "],
    11 : ["Pompe à air", "Pompes à air ", "une "],
    12 : ["Encre de seiche", "Encres de seiche", "de l'"],
    13 : ["Paquet", "Paquets", "un "],
    14 : ["Reçu de poisson doré", "Reçus de poissons dorés", "un "],
    15 : ["Poisson doré", "Poissons dorés", "un "],
    16 : ["Huile", "Huiles", "de l'"],
    17 : ["Graisse", "Graisses", "de la "],
    18 : ["Eau", "Eaux", "de l'"],
    19 : ["Rapport de pignons", "Rapports de pignons", "un "],

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
    5012 : ["Clé du "+lDaisyGardensNC, "Clés du "+lDaisyGardensNC, "une "],
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
QuestMovieTrackChoiceCancel = "Reviens quand tu es prêt à te décider!! Salut!"
QuestMovieQuestChoice = "Choisis un défitoon." 
QuestMovieTrackChoice = "Prêt à te décider? Choisis une série, ou reviens plus tard."

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
    QUEST : "Oh, merci pour ta visite, _avName_!\a"+TheCogs+" du quartier ont effrayé mon livreur.\aJe n'ai personne pour livrer cette salade à _toNpcName_!\aPeux-tu le faire pour moi? Merci beaucoup!_where_"
    }

QuestDialog_2910 = {
    QUEST : "Déjà de retour?\aSuper travail avec le ressort.\aLe dernier article est un contrepoids.\aVa donc voir _toNpcName_ et ramène tout ce que tu peux._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "OK, maintenant je crois que nous sommes prêts pour quelque chose de plus compliqué.\aTu dois vaincre 3 Chefbots ",
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
    164 : {QUEST : "Il semble que tu as besoin de nouveaux gags.\aVa voir %s, peut-être pourra-t-il t'aider._where_" % Flippy },
    165 : {QUEST : "Salut!\aOn dirait que tu as besoin de t'entraîner à utiliser tes gags.\aChaque fois que tu atteins un Cog avec l'un de tes gags, ton expérience augmente.\aQuand tu auras assez d'expérience, tu pourras utiliser un gag encore meilleur.\aVa t'entraîner à utiliser tes gags en battant 4 Cogs."},
    166 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Chefbots."},
    167 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Loibots."},
    168 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Vendibots."},
    169 : {QUEST : "Bien joué pour avoir battu ces Cogs.\aTu sais, les Cogs sont de quatre sortes différentes.\aIl y a les Loibots, les Caissbots, les Vendibots et les Chefbots.\aTu peux les distinguer par leurs couleurs et leurs étiquettes.\aPour t'entraîner va battre 4 Caissbots.}"},
    170 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - il peut te donner des conseils avisés._where_" },
    171 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - il peut te donner des conseils avisés._where_" },
    172 : {QUEST : "Bon travail, maintenant tu connais la différence entre les 4 sortes de Cogs.\aJe crois que tu peux commencer à t'entraîner pour ta troisième série de gags.\aVa parler à_toNpcName_ pour choisir ta prochaine série de gags - elle peut te donner des conseils avisés._where_" },
    400 : {GREETING : "",
           QUEST : "Le lancer et l'éclaboussure sont super, mais tu auras besoin de plus de gags pour battre les Cogs de plus haut niveau.\aLorsque tu fais équipe avec d'autres Toons contre les Cogs, vous pouvez combiner vos attaques pour faire encore plus de dégâts.\aEssayez différentes combinaisons de gags pour voir ce qui marche le mieux.\aPour ta prochaine série, choisis entre tapage et toonique.\aTapage est particulier parce que lorsqu'il frappe, il endommage tous les Cogs.\aToonique te permet de soigner les autres Toons lors d'un combat.\aLorsque tu es prêt(e) à te décider, reviens ici faire ton choix.",
           INCOMPLETE_PROGRESS : "Déjà de retour? OK, quel est ton choix?",
           INCOMPLETE_WRONG_NPC : "Pense bien à ta décision avant de choisir.",
           COMPLETE : "Bonne décision. Maintenant tu dois t'entraîner avant de pouvoir utiliser ces gags.\aTu dois effectuer une série de défitoons pour t'entraîner.\aChaque défi te donnera une seule image de ton animation d'attaque avec les gags.\aLorsque tu auras les 15 images, tu pourras faire le dernier défi d'entraînement qui te permettra d'utiliser tes nouveaux gags.\aTu peux suivre tes progrès dans ton journal de bord.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Va voir _toNpcName_ si tu veux parcourir la ville plus facilement._where_" },
    1040 : { QUEST : "Va voir _toNpcName_ si tu veux parcourir la ville plus facilement._where_" },
    1041 : { QUEST : "Salut! Qu'est-ce qui t'amène?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes amis en utilisant la liste d'amis, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes amis.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1042 : { QUEST : "Salut! Qu'est-ce qui t'amène?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes amis en utilisant la liste d'amis, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes amis.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1043 : { QUEST : "Salut! Qu'est-ce qui t'amène?\aTout le monde utilise son trou portable pour voyager dans Toontown.\aTu peux te téléporter vers tes amis en utilisant la liste d'amis, ou vers n'importe quel quartier en utilisant la carte du journal de bord.\aBien entendu, tu dois d'abord gagner le droit de le faire!\aDisons que je peux activer ton accès à Toontown centre par téléportation si tu aides un de mes amis.\aOn dirait que les Cogs font du désordre sur l'avenue des Fondus. Va voir _toNpcName_._where_" },
    1044 : { QUEST : "Oh, merci de passer par ici. J'ai vraiment besoin d'aide.\aComme tu peux voir, je n'ai pas de clients.\aMon livre de recettes secret est perdu et personne ne vient plus dans mon restaurant.\aLa dernière fois que je l'ai vu, c'était avant que ces Cogs ne prennent mon bâtiment.\aEst-ce que tu peux m'aider à retrouver quatre de mes célèbres recettes?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as pu retrouver mes recettes?" },
    1045 : { QUEST : "Merci beaucoup!\aD'ici peu, j'aurai retrouvé toutes mes recettes et je pourrai rouvrir mon restaurant.\aOh, j'ai une petite note ici pour toi - quelque chose à propos de l'accès par téléportation?\aC'est écrit, merci d'avoir aidé mon ami et d'avoir livré ceci au quartier général des Toons. \aEh bien, merci vraiment - au revoir!",
             LEAVING : "",
             COMPLETE : "Ah oui, c'est écrit que tu as été d'une grande aide à de braves gens de l'avenue des Fondus.\aEt que tu as besoin d'un accès par téléportation à Toontown centre.\aBon, c'est comme si c'était fait.\aMaintenant tu peux revenir au terrain de jeux par téléportation depuis presque partout dans Toontown.\aOuvre simplement ta carte et clique sur "+lToontownCentral+"." },
    1046 : { QUEST : "Les Caissbots ont vraiment ennuyé la Caisse d'épargne Drôle d'argent.\aVa donc y faire un tour et vois si tu peux faire quelque chose._where_" },
    1047 : { QUEST : "Les Caissbots se sont introduits dans la banque et ont volé nos machines.\aS'il te plaît, reprends 5 machines à calculer aux Caissbots.\aPour t'éviter de faire des allers et retours, rapporte-les toutes en une seule fois.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu cherches encore des machines à calculer?" },
    1048 : { QUEST : "Oh là là! >Merci d'avoir trouvé nos machines à calculer.\aHmm... Elles ont l'air un peu abîmées.\aDis donc, pourrais-tu les amener à _toNpcName_ à son magasin, \"Machines à chatouilles\", dans cette rue?\aVoir si elle peut les réparer.",
             LEAVING : "", },
    1049 : { QUEST : "Qu'est-ce que c'est? Des machines à calculer cassées?\aDes Caissbots dis-tu?\aBon, regardons ça...\aMouais, les pignons sont cassés, mais je n'en vends pas...\aTu sais ce qui pourrait marcher - des pignons de Cog, des gros, de gros Cogs...\aDes pignons de Cog de niveau 3 devraient faire l'affaire. J'en aurai besoin de 2 pour chaque machine, donc 10 au total.\aRapporte-les moi tous ensemble et je ferai la réparation!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Souviens-toi, j'ai besoin de 10 pignons pour réparer les machines." },
    1053 : { QUEST : "Ah oui, ça devrait bien faire l'affaire.\aTout est réparé maintenant, gratuitement.\aRapporte-les à Drôle d'argent, et dis-leur bonjour de ma part.",
             LEAVING : "",
             COMPLETE : "Toutes les machines à calculer sont réparées?\aJoli travail. Je crois bien que j'ai quelque chose par là pour te récompenser..." },
    1054 : { QUEST : "_toNpcName_ a besoin d'aide pour ses voitures de clown._where_" },
    1055 : { QUEST : "Bon sang! Je n'arrive pas à trouver les pneus de cette voiture de clown!\aTu crois que tu pourrais m'aider?\aJe crois que Bob Fondu les a lancés dans la mare du terrain de jeux de Toontown centre.\aSi tu vas sur les pontons, de là tu peux essayer de repêcher les pneus.",
             GREETING : "Youhouu!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu as du mal à repêcher les 4 pneus?" },
    1056 : { QUEST : "Fanta-super-tastique! Maintenant je vais pouvoir remettre en marche cette vieille voiture de clown!\aHé, je croyais que j'avais une pompe par ici pour gonfler ces pneus...\aC'est peut-être _toNpcName_ qui l'a empruntée?\aTu peux aller lui demander de me la rendre?_where_",
             LEAVING : "" },
    1057 : { QUEST : "Salut!\aUne pompe à pneus tu dis?\aJe vais te dire - tu me nettoies les rues de quelques-uns de ces Cogs de haut niveau...\aEt je te donne la pompe à pneus.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "C'est tout ce que tu peux faire?" },
    1058 : { QUEST : "Bon travail - je savais que tu pouvais le faire.\aVoilà la pompe. Je suis certain que_toNpcName_ sera content de la récupérer.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Youpiii! Maintenant ça va marcher!\aEt dis donc, merci de m'avoir aidé.\aTiens, prends ça." },
    1059 : { QUEST : "_toNpcName_ est à court de fournitures. Tu peux peut-être lui donner un coup de main?_where_" },
    1060 : { QUEST : "Merci d'être passé par ici!\aCes Cogs ont volé mon encre ; je n'en ai presque plus.\a Pourrais-tu me pêcher de l'encre de seiche dans la mare?\aTu n'as qu'à rester sur un ponton près de la mare pour pêcher.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "{Tu as des problèmes pour pêcher?" },
    1061 : { QUEST : "Super - merci pour l'encre!\aTu sais quoi, et si tu nous débarrassais de quelques Gratte-papiers...\aJe ne serais plus en panne d'encre aussi rapidement.\aTu dois vaincre 6 Gratte-papiers dans Toontown centre pour avoir ta récompense.",
             LEAVING : "",
             COMPLETE : "Merci! Laisse-moi te récompenser pour ton aide.",
             INCOMPLETE_PROGRESS : "Je viens de voir encore d'autres Gratte-papiers." },
    1062 : { QUEST : "Super - merci pour l'encre!\aTu sais quoi, et si tu nous débarrassais de quelques Pique-au-sang...\aJe ne serais plus en panne d'encre aussi rapidement.\aTu dois vaincre 6 Pique-au-sang dans Toontown centre pour avoir ta récompense.",
             LEAVING : "",
             COMPLETE : "Merci! Laisse-moi te récompenser pour ton aide.",
             INCOMPLETE_PROGRESS : "Je viens de voir encore d'autres Pique-au-sang." },
    900 : { QUEST : "Je crois comprendre que_toNpcName_ a besoin d'aide avec un paquet._where_" },
    1063 : { QUEST : "Salut, merci d'être là.\aUn Cog a volé un paquet très important juste sous mon nez.\aPeux-tu le récupérer? Je crois que c'était un Cog de niveau 3...\aDonc, tu dois vaincre des Cogs de niveau 3 jusqu'à ce que tu retrouves mon paquet.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein?" },
    1067 : { QUEST : "C'est ça, très bien!\aOh, l'adresse est toute tachée...\aTout ce que j'arrive à lire, c'est Docteur... - le reste est brouillé.\aC'est peut-être pour_toNpcName_? Peux-tu lui porter?_where_",
             LEAVING : "" },
    1068 : { QUEST : "Je n'attendais pas de paquet. C'est peut-être pour le Dr E. Phorique?\aMon assistant doit aller le voir aujourd'hui, je me charge de lui remettre.\aEn attendant, est-ce que tu voudrais bien débarrasser ma rue de quelques Cogs?\aTu dois vaincre 10 Cogs dans Toontown centre.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mon assistant n'est pas encore revenu." },
    1069 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Caissbot l'a volé à mon assistant alors qu'il revenait.\aPourrais-tu essayer de le récupérer?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein?" },
    1070 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Vendibot l'a volé à mon assistant alors qu'il revenait.\aJe suis désolé, mais il va falloir que tu retrouves ce Vendibot pour le récupérer.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein?" },
    1071 : { QUEST : "Le Dr. E. Phorique dit qu'il n'attendait pas de paquet non plus.\aMalheureusement, un Chefbot l'a volé à mon assistant alors qu'il revenait.\aPourrais-tu essayer de le récupérer?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein?" },
    1072 : { QUEST : "Super - tu l'as retrouvé!\aTu devrais peut-être essayer _toNpcName_, cela pourrait être pour lui._where_",
             LEAVING : "" },
    1073 : { QUEST : "Oh, merci de m'avoir apporté mes paquets.\aJuste une seconde, j'en attendais deux. Pourrais-tu vérifier avec _toNpcName_ voir s'il a l'autre?",
             INCOMPLETE : "Est-ce que tu as trouvé mon autre paquet?",
             LEAVING : "" },
    1074 : { QUEST : "Il a dit qu'il y avait un autre paquet? Les Cogs l'ont peut-être aussi volé.\aTu dois vaincre des Cogs jusqu'à ce que tu trouves le second paquet. ",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas retrouvé le paquet, hein?" },
    1075 : { QUEST : "Finalement je crois qu'il y avait un second paquet!\aVa vite le porter à _toNpcName_ avec mes excuses.",
             COMPLETE : "Eh, mon paquet est là!\aPuisque tu es un Toon aussi serviable, cela devrait aider.",
             LEAVING : "" },
    1076 : { QUEST : "Il y a un problème au Ornithorynques 14 carats.\a_toNpcName_ serait sans doute content d'avoir de l'aide._where_" },
    1077 : { QUEST : "Merci d'être venu - "+theCogs+" ont volé tous mes poissons dorés.\aJe crois que les Cogs veulent les vendre pour se faire de l'argent facilement.\aCes 5 poissons ont été mes seuls compagnons dans cette petite boutique depuis tant d'années...\aSi tu pouvais me les retrouver, je t'en serais vraiment reconnaissant.\aJe suis certain qu'un des Cogs a mes poissons.\aTu dois vaincre des Cogs jusqu'à ce que tu trouves mes poissons dorés.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "S'il te plaît, ramène-moi mes poissons." },
    1078 : { QUEST : "Oh, tu as mes poissons!\aEh? Qu'est-ce que c'est que ça?\aAah, ce sont bien les Cogs, après tout.\aJe ne comprends rien à ce reçu. Peux-tu l'emmener à _toNpcName_ voir s'il peut le lire?_where_",
             INCOMPLETE : "Qu'est-ce que _toNpcName_ a dit à propos du reçu?",
             LEAVING : "" },
    1079 : { QUEST : "Mmm, laisse-moi voir ce reçu.\a...Ah oui, il dit qu'un poisson doré a été vendu à un Laquaistic.\aÇa n'a pas l'air de dire ce qui est arrivé aux 4 autres poissons.\aTu devrais peut-être essayer de trouver ce Laquaistic.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je ne crois pas que je puisse t'aider à grand-chose d'autre.\aPourquoi n'essaies-tu pas de trouver ce poisson doré?" },
    1092 : { QUEST : "Mmm, laisse-moi voir ce reçu.\a...Ah oui, il dit qu'un poisson doré a été vendu à un Gardoseille.\aÇa n'a pas l'air de dire ce qui est arrivé aux 4 autres poissons.\aTu devrais peut-être essayer de trouver ce Gardoseille.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je ne crois pas que je puisse t'aider à grand-chose d'autre.\aPourquoi n'essaies-tu pas de trouver ce poisson doré?" },
    1080 : { QUEST : "Oh, Dieu merci! Tu as trouvé Oscar - c'est mon préféré.\aQu'est-ce que c'est, Oscar? Hein, hein...ils ont quoi? ... Ils sont?\aOscar dit que les 4 autres se sont échappés dans la mare du terrain de jeux.\aPeux-tu aller me les chercher?\aTu n'as qu'à les pêcher dans la mare.",
             LEAVING : "",
             COMPLETE : "Ahh, je suis si content! Avoir retrouvé mes petits camarades!\aTu mérites une belle récompense pour cela!",
             INCOMPLETE_PROGRESS : "Tu as des problèmes pour trouver ces poissons?" },
    1081 : { QUEST : "_toNpcName_ a l'air d'être dans une situation difficile. Elle serait sûrement contente d'avoir de l'aide._where_" },
    1082 : { QUEST : "J'ai renversé de la colle à séchage rapide, et je suis collée - complètement collée!\aS'il y avait une façon de m'en sortir, je prends tout de suite.\aCela me donne une idée, si tu veux bien.\aVa vaincre quelques Vendibots et ramène-moi de l'huile.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller?" },
    1083 : { QUEST : "Bon, l'huile a fait un peu d'effet, mais je ne peux toujours pas bouger,\aQuoi d'autre pourrait m'aider? C'est difficile à dire.\aCela me donne une idée ; on peut au moins essayer.\aVa vaincre quelques Loibots et ramène-moi de la graisse.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller?" },
    1084 : { QUEST : "Non, ça n'a rien fait. Ce n'est vraiment pas drôle.\aJe mets la graisse juste là sur l'argent,\aÇa me donne une idée, avant que j'oublie.\aVa vaincre quelques Caissbots ; et rapporte de l'eau pour l'humecter.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Hourrah, je suis libérée de cette colle rapide,\aComme récompense, je te donne ce cadeau,\aTu peux rire un peu plus longtemps lorsque tu es en train de te battre, et puis...\aOh, non! Je suis de nouveau collée là!",
             INCOMPLETE_PROGRESS : "Peux-tu m'aider à me décoller?" },
    1085 : { QUEST : "_toNpcName_ est en train de faire des recherches sur les Cogs.\aVa lui parler si tu veux l'aider._where_" },
    1086 : { QUEST : "C'est cela, je fais une étude sur les Cogs.\aJe veux savoir ce qui les fait tiquer.\aCela m'aiderait certainement si tu pouvais me trouver des pignons de Cogs.\aAssure-toi qu'il s'agit de Cogs de niveau 2 au minimum, qu'ils soient assez gros pour être examinés.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu ne peux pas trouver assez de pignons?" },
    1089 : { QUEST : "OK, regardons un peu ça. Ce sont d'excellents spécimens!\aMmmm...\aOK, voilà mon rapport. Emmène-le tout de suite au quartier général des Toons.",
             INCOMPLETE : "As-tu porté mon rapport au quartier général?",
             COMPLETE : "Bon travail _avName_, on va s'occuper de ça.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ a des informations importantes pour toi._where_" },
    1091 : { QUEST : "J'ai entendu dire que le quartier général des Toons travaille sur une sorte de détecteur de Cogs.\aIl te permettra de voir où sont les Cogs afin de les repérer plus facilement.\aCette page des Cogs dans ton journal de bord en est la clé.\aEn battant assez de Cogs, tu pourras te régler sur leurs signaux et détecter leur emplacement.\aContinue à vaincre des Cogs, afin d'être prêt.",
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
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé ma chambre à air?",
             COMPLETE : "Tu as trouvé ma chambre à air! Tu es vraiment très doué. Tiens, prends ta récompense...",
             },
    2203 : { QUEST : TheCogs+" sont en train de mettre la banque sens dessus dessous.\aVa voir le Capitaine Carl et vois ce que tu peux faire._where_" },
    2204 : { QUEST : "Bienvenue à bord, moussaillon.\aGrrr! Ces fripons de Cogs ont cassé mon monocle et je n'arrive plus à compter la monnaie sans lui.\aGarde les pieds sur terre et porte cette ordonnance au Dr. Queequeg puis rapporte m'en un nouveau._where_",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "Qu'est-ce que c'est?\aOh, je voudrais bien préparer cette ordonnance mais les Cogs ont chapardé mes réserves.\aSi tu peux reprendre la monture à un Laquaistic je pourrai probablement t'aider.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Désolé. Pas de monture du Laquaistic, pas de monocle.",
             },
    2206: { QUEST : "Excellent!\aUne seconde...\aTon ordonnance est prête. Emmène tout de suite ce monocle au Capitaine Carl._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "Hisse et ho!\aTu vas finir par gagner du galon après tout.\aEt voilà.",
            },
    2207 : { QUEST : "Barbara Bernache a un Cog dans son magasin!\aIl vaudrait mieux que tu y ailles tout de suite._where_" },
    2208 : { QUEST : "Ça alors! Tu viens de le rater, mon chou.\aIl y avait un Frappedos ici. Il a pris ma grande perruque blanche.\aIl a dit que c'était pour son chef et quelque chose à propos de \" jurisprudence \".\aSi tu pouvais me la rapporter, je t'en serais toujours reconnaissante.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Tu ne l'as toujours pas trouvé?\aIl est grand avec une tête pointue",
             COMPLETE : "Tu l'as trouvé!?!?\aTu es vraiment un ange!\aTu as bien gagné ceci...",
             },
    2209 : { QUEST : "Ginette se prépare pour un voyage important.\aVas-y faire un tour et vois ce que tu peux faire pour l'aider._where_"},
    2210 : { QUEST : "Tu peux m'aider.\aLe quartier général des Toons m'a demandé de faire un voyage pour voir si je peux trouver d'où viennent les Cogs.\aJ'aurai besoin de quelques affaires pour mon bateau mais je n'ai pas beaucoup de bonbons.\aVa et ramène-moi du lest de chez Ernest. Il faudra que tu lui rendes un service pour l'avoir._where_",
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
    2213 : { QUEST : "Excellent travail. Je savais qu'il serait raisonnable.\aEnsuite il me faudra une carte marine de chez Art.\aJe ne crois pas avoir beaucoup de crédit là-bas non plus ; il faudra que tu t'arranges avec lui._where_",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Oui, j'ai la carte marine que veut Ginette.\aEt tu l'auras en échange d'un petit travail.\aJ'essaie de construire un astrolabe pour naviguer dans les étoiles.\aJ'aurais besoin de trois pignons de Cog pour le construire.\aReviens quand tu les auras trouvés.",
             INCOMPLETE_PROGRESS: "Alors ils arrivent ces pignons de Cogs?",
             GREETING : "Bienvenue!",
             LEAVING : "Bonne chance!",
             },
    2215 : { QUEST : "Ooh! Ces pignons feront très bien l'affaire.\aVoilà la carte. Donne-la à Ginette avec mes compliments._where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "Bon, on y est presque. Je suis prête à prendre la mer!\aJe t'emménerais avec moi si tu n'avais pas un teint si vert. Prends plutôt ceci.",
             },
    2901 : { QUEST : "Si tu es d'accord, Ahab a besoin d'aide, chez lui..._where_",
            },
    2902 : { QUEST : "Tu es la nouvelle recrue?\aBien, bien. Tu peux peut-être m'aider.\aJe suis en train de construire un crabe géant préfabriqué pour dérouter les Cogs.\aJe pourrais quand même utiliser une manille. Va voir Gérard et rapportes-en un, s'il te plaît._where_",
             },
    2903 : { QUEST : "Salut!\aOui, j'ai entendu parler du crabe géant qu'Ahab est en train de fabriquer.\aLa meilleure manille que j'aie est un peu sale quand même.\aSois sympa, passe chez un blanchisseur avant de la déposer._where_",
             LEAVING : "Merci!"
             },
    2904 : { QUEST : "Tu dois être la personne que Gérard a envoyée.\aJe crois que je peux faire ça assez vite.\aJuste une minute...\aEt voilà. Comme neuf!\aTu salueras Ahab de ma part._where_",
             },
    2905 : { QUEST : "Ah, c'est exactement ce que je cherchais.\aPendant que tu es là, je vais aussi avoir besoin d'un très gros ressort d'horloge.\aVa donc voir chez Crochet voir s'il en a un._where_",
             },
    2906 : { QUEST : "Un gros ressort, hein?\aJe suis désolé mais le plus gros ressort que j'aie est quand même plutôt petit.\aJe pourrais peut-être en fabriquer un avec des ressorts de gâchette de pistolet éclabousseur.\aApporte-moi trois de ces gags et je vais voir ce que je peux faire.",
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
             INCOMPLETE_PROGRESS : "Je crois qu'on est toujours pas en sécurité...",
             },
    2925 : { QUEST : "Ça y est?\aBon, je suppose qu'on est suffisamment en sécurité maintenant.\aVoilà le contrepoids pour Ahab._where_"
             },
    2926 : {QUEST : "Bon, c'est tout.\aVoyons si ça marche.\aHmmm, il y a un petit problème.\aJe n'ai plus de courant parce que ce bâtiment Cog bloque mon capteur solaire.\aPeux-tu le reprendre pour moi?",
            INCOMPLETE_PROGRESS : "Toujours pas de courant. Où en es-tu avec ce bâtiment?",
            COMPLETE : "Super! Tu es une sacrée terreur pour les Cogs! Tiens, prends ta récompense...",
            },
    3200 : { QUEST : "Je viens d'avoir un appel de _toNpcName_.\aCe n'est pas son jour. Tu pourrais peut-être l'aider.!\aVas-y faire un tour et vois ce dont il a besoin._where_" },
    3201 : { QUEST : "Oh, merci d'être là!\aJ'ai besoin de quelqu'un pour emporter cette nouvelle cravate en soie à _toNpcName_.\aEst-ce que tu peux faire ça pour moi?_where_" },
    3203 : { QUEST : "Oh, ça doit être la cravate que j'ai commandée! Merci!\aElle va avec un costume à rayures que je viens de finir, juste là.\aHé, qu'est ce qui est arrivé à ce costume?\aOh non! Les Cogs ont dû voler mon nouveau costume!\aTu dois vaincre des Cogs jusqu'à ce que tu trouves mon costume, et que tu me le rapportes.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu n'as pas encore trouvé mon costume? Je suis certain que les Cogs l'ont pris!",
             COMPLETE : "Youpii! Tu as trouvé mon nouveau costume!\aTu vois, je t'avais dit que les Cogs l'avaient! Voilà ta récompense...",
             },

    3204 : { QUEST : "_toNpcName_ vient d'appeler pour signaler un vol.\aPourquoi n'irais-tu pas voir si tu peux arranger l'affaire?_where_" },
    3205 : { QUEST : "Bonjour, _avName_! Tu es là pour m'aider?\aJe viens de chasser un Pique-au-sang de mon magasin. Houlala! C'était effrayant.\aMais maintenant je ne trouve plus mes ciseaux! Je suis certain que ce Pique-au-sang les a pris.\aTrouve-le, et ramène-moi mes ciseaux.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu cherches encore mes ciseaux?",
             COMPLETE : "Mes ciseaux! Merci beaucoup! Voilà ta récompense...",
             },

    3206 : { QUEST : "On dirait que _toNpcName_ a des problèmes avec des Cogs.\aVa voir si tu peux l'aider._where_" },
    3207 : { QUEST : "Ohé, _avName_! Merci d'être venu!\aUne bande de Charabieurs est arrivée et a volé une pile de cartes postales sur mon comptoir.\aS'il te plaît, sors vaincre tous ces Charabieurs et rapporte-moi mes cartes postales!",
             INCOMPLETE_PROGRESS : "Il n'y a pas assez de cartes postales! Continue de chercher!",
             COMPLETE : "Oh, merci! Maintenant je vais pouvoir livrer le courrier à temps! Voilà ta récompense...",
             },

    3208 : { QUEST : "Nous avons eu des plaintes des résidents récemment à propos des Cassepieds.\aEssaie de vaincre 10 Cassepieds pour aider tes camarades Toons du "+lDaisyGardens+"." },
    3209 : { QUEST : "Merci d'avoir battu ces Cassepieds!\aMais maintenant ce sont les Télévendeurs qui sont incontrôlables.\aVa vaincre 10 Télévendeurs au "+lDaisyGardens+" et reviens ici pour ta récompense." },

    3247 : { QUEST : "Nous avons eu des plaintes des résidents récemment à propos des Pique-au-sang.\aEssaie de vaincre 20 Pique-au-sang pour aider tes camarades Toons du "+lDaisyGardens+". " },


    3210 : { QUEST : "Oh non, la Fleur qui mouille, rue des Érables, n'a plus de fleurs!\aEmmène-leur dix de tes fleurs à éclabousser pour les aider.\aVérifie que tu as bien 10 fleurs à éclabousser dans ton inventaire d'abord.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "J'ai besoin de 10 fleurs à éclabousser. Tu n'en as pas assez!" },
    3211 : { QUEST : "Oh, merci beaucoup! Ces fleurs à éclabousser vont nous tirer d'embarras.\aMais j'ai peur des Cogs qui sont dehors.\aPeux-tu m'aider et vaincre quelques-uns de ces Cogs?\aReviens me voir après avoir vaincu 20 Cogs dans cette rue.",
             INCOMPLETE_PROGRESS : "Il reste encore des Cogs à vaincre par ici! Continue!",
             COMPLETE : "Oh, merci! Cela m'aide beaucoup. Ta récompense est...",
             },

    3212 : { QUEST : "_toNpcName_ a besoin d'aide pour chercher quelque chose qu'elle a perdu.\aVa la voir et vois ce que tu peux faire._where_" },
    3213 : { QUEST : "Salut, _avName_. Peux-tu m'aider?\aJe crois que j'ai égaré mon stylo. Je pense que les Cogs l'ont peut-être pris.\aVa vaincre des Cogs pour retrouver le stylo qu'ils m'ont volé.",
             INCOMPLETE_PROGRESS : "Tu n'as pas encore trouvé mon stylo?" },
    3214 : { QUEST : "Oui, c'est mon stylo! Merci beaucoup!\aMais après ton départ, j'ai réalisé que mon encrier manquait aussi.\aVa vaincre des Cogs pour retrouver mon encrier.",
             INCOMPLETE_PROGRESS : "Je cherche encore mon encrier!" },
    3215 : { QUEST : "Super! Maintenant j'ai retrouvé mon stylo et mon encrier!\aMais tu ne devineras jamais!\aMon bloc-notes a disparu! Ils ont dû le voler aussi!\aVa vaincre des Cogs pour retrouver mon bloc-notes volé, puis reviens pour ta récompense.",
             INCOMPLETE_PROGRESS : "Tu as des nouvelles de mon bloc-notes?" },
    3216 : { QUEST : "C'est mon bloc-notes! Youpii! Ta récompense est...\aHé! Mais où est-elle?\aJ'avais ta récompense là, dans le coffre de mon bureau. Mais le coffre entier a disparu!\aIncroyable! Ces Cogs ont volé ta récompense!\aVa vaincre des Cogs pour retrouver mon coffre.\aQuand tu me le ramèneras, je te donnerai ta récompense.",
             INCOMPLETE_PROGRESS : "Continue de chercher ce coffre! Ta récompense est dedans!",
             COMPLETE : "Enfin! J'avais ton nouveau sac à gags dans ce coffre. Le voilà...",
             },

    3217 : { QUEST : "Nous avons fait quelques études sur les mécanismes des Vendibots.\aNous devons encore étudier certaines pièces de plus près.\aApporte-nous un pignon de Cafteur.\aTu peux en attraper un quand le Cog explose." },
    3218 : { QUEST : "Bon travail! Maintenant, nous avons besoin d'un pignon de Passetout pour faire la comparaison.\aCes pignons sont plus difficiles à attraper, ne te décourage pas." },
    3219 : { QUEST : "Super! Maintenant on n'a plus besoin que d'un pignon en plus.\aCette fois, il nous faut un pignon de Secousse-cousse.\aTu devras peut-être chercher à l'intérieur des bâtiments Vendibots pour trouver cette sorte de Cogs.\aQuand tu en auras attrapé un, rapporte-le pour recevoir ta récompense." },

    3244 : { QUEST : "Nous avons fait quelques études sur les mécanismes des Loibots.\aNous devons encore étudier certaines pièces de plus près.\aApporte-nous un pignon de Charognard.\aTu peux en attraper un quand le Cog explose." },
    3245 : { QUEST : "Bon travail! Maintenant nous avons besoin d'un pignon de Frappedos pour faire la comparaison.\aCes pignons sont plus difficiles à attraper, ne te décourage pas." },
    3246 : { QUEST : "Super! Encore un pignon et c'est bon.\aCette fois, il nous faut un pignon de Tournegris.\aQuand tu en auras attrapé un, rapporte-le pour avoir ta récompense." },

    3220 : { QUEST : "Je viens d'apprendre que _toNpcName_ te cherchait.\aPourquoi ne vas-tu pas voir ce qu'elle veut?_where_" },
    3221 : { QUEST : "Ohé, _avName_! Et voilà!\aJ'ai entendu dire que tu étais expert(e) en éclaboussures.\aJ'ai besoin de quelqu'un pour montrer l'exemple à tous les Toons du "+lDaisyGardens+".\aUtilise tes attaques par éclaboussure pour vaincre un groupe de Cogs.\aEncourage tes amis à utiliser aussi les éclaboussures.\aLorque tu auras vaincu 20 Cogs, reviens ici pour ta récompense!" },

    3222 : { QUEST : "C'est le moment de faire preuve de ta Toonmaîtrise.\aSi tu réussis à reprendre un certain nombre de bâtiments aux Cogs, tu gagneras le droit à trois quêtes.\aD'abord, tu dois prendre deux bâtiments aux Cogs.\aN'hésite pas à demander l'aide de tes amis."},
    3223 : { QUEST : "Super travail pour ces bâtiments!\aMaintenant tu dois prendre deux bâtiments de plus.\aCes immeubles doivent faire au moins deux étages." },
    3224 : { QUEST : "Fantastique!\aMaintenant tu dois prendre deux bâtiments de plus.\aCes immeubles doivent faire au moins trois étages.\aQuand tu auras fini, reviens chercher ta récompense!",
             COMPLETE : "Tu as réussi, _avName_!\aTu as fait preuve d'une excellente Toonmaîtrise.",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ dit qu'elle a besoin d'aide.\aVa voir si tu peux donner un coup de main?_where_" },
    3235 : { QUEST : "Oh, c'est la salade que j'ai commandée!\aMerci de me l'avoir apportée.\aTous ces Cogs ont dû effrayer le livreur habituel de _toNpcName_ encore une fois.\aTu pourrais nous rendre service et vaincre quelques-uns des Cogs qui traînent par ici?\aVa vaincre 10 Cogs dans le "+lDaisyGardens+" et reviens voir _toNpcName_.",
             INCOMPLETE_PROGRESS : "Tu es en train de vaincre des Cogs pour moi?\aC'est super!! Continue comme ça!",
             COMPLETE : "Oh, merci beaucoup d'avoir vaincu ces Cogs!\aMaintenant je vais peut-être pouvoir reprendre mon programme habituel de livraisons.\aTa récompense est...",
             INCOMPLETE_WRONG_NPC : "Va raconter à _toNpcName_ tous les Cogs que tu as vaincus._where_" },

    3236 : { QUEST : "Il y a beaucoup trop de Loibots par ici.\aTu peux faire ta part de travail!\aVa vaincre 3 bâtiments Loibot." },
    3237 : { QUEST : "Super travail pour ces bâtiments Loibot!\aMais maintenant il y a beaucoup trop de Vendibots!\aVa vaincre 3 bâtiments Vendibot, puis reviens chercher ta récompense." },

    3238 : { QUEST : "Oh non! Un Cog Circulateur a volé la clé du "+lDaisyGardens+"!\aVa voir si tu peux la retrouver.\aSouviens-toi que les Circulateurs ne se trouvent que dans les bâtiments Vendibot." },
    3239 : { QUEST : "Tu as bien trouvé une clé, mais ce n'est pas la bonne!\aNous avons besoin de la clé du "+lDaisyGardens+".\aContinue de chercher! Un Cog Circulateur l'a encore!" },

    3242 : { QUEST : "Oh non! Un Cog Avocageot a volé la clé du "+lDaisyGardens+"!\aVa voir si tu peux la retrouver.\aSouviens-toi que les Avocageots ne se trouvent que dans les bâtiments Loibot." },
    3243 : { QUEST : "Tu as bien trouvé une clé, mais ce n'est pas la bonne!\aNous avons besoin de la clé du "+lDaisyGardens+".\aContinue de chercher! Un Cog Avocageot l'a encore!" },

    3240 : { QUEST : "_toNpcName_ vient de me dire qu'un Avocageot lui a volé un sac de graines pour oiseaux.\aVa vaincre des Avocageots jusqu'à ce que tu retrouves les graines pour oiseaux de Piaf, et rapporte-les lui.\aLes Avocageots ne se trouvent que dans les bâtiments Loibot._where_",
             COMPLETE : "Oh, merci beaucoup d'avoir retrouvé mes graines pour oiseaux!\aTa récompense est...",
             INCOMPLETE_WRONG_NPC : "Bien, tu as retrouvé ces graines pour oiseaux!\aMaintenant emmène-les à _toNpcName_._where_",
             },

    3241 : { QUEST : "Certains des bâtiments des Cogs deviennent beaucoup trop hauts.\aVa voir si tu peux réduire de hauteur certains des immeubles les plus hauts.\aReprends 5 immeubles de 3 étages ou plus et reviens ici pour ta récompense.",
             },

    3250 : { QUEST : "Lima, la détective de la rue du Chêne, a entendu parler d'un quartier général Vendibot. \aVa donc voir et aide-la à enquêter.",
             },
    3251 : { QUEST : "Il y a quelque chose de bizarre par ici.\aIl y a tant de Vendibots!\aJ'ai entendu dire qu'ils ont installé leur propre quartier général au bout de cette rue.\aVa au bout de la rue voir ce qu'il en est.\aTrouve des Cogs Vendibots dans leur quartier général, vaincs-en 5 et reviens me le dire.",
             },
    3252 : { QUEST : "OK, annonce la couleur\aQu'est-ce que tu dis?\aAh, le quartier général des Vendibots?? Oh non!!! Il faut faire quelque chose.\aNous devons le dire au Juge Ticot - il saura quoi faire.\aVa le voir tout de suite et dis-lui ce que tu as trouvé. Il est juste au bout de la rue.",
            },
    3253 : { QUEST : "Oui, puis-je t'aider? Je suis très occupé.\aHein? Un quartier général Cog?\aHein? Sottises. Ça n'est pas possible.\aTu dois te tromper. C'est grotesque.\aHein? Ne discute pas avec moi.\aOk, alors ramène des preuves.\aSi les Vendibots sont vraiment en train de construire ce quartier général Cog, les Cogs du quartier auront des plans sur eux.\aLes Cogs adorent la paperasserie, tu le savais?\aVa vaincre des Vendibots par là-bas jusqu'à ce que tu trouves des plans.\aRapporte-les moi, alors je te croirai peut-être.",
            },
    3254 : { QUEST : "Encore toi, hein? Des plans? Tu les as?\aLaisse-moi regarder ça! Hmmm... Une usine?\aCela doit être là qu'ils fabriquent les Vendibots... Et qu'est-ce que c'est que ça?\aOui, exactement ce que je pensais. Je le savais depuis le départ.\aIls sont en train de construire un quartier général des Cogs Vendibots.\aCe n'est pas bon signe. Je dois passer quelques appels. Très occupé. Au revoir!\aHein? Oh oui, retourne ces plans à la détective Lima.\aElle saura les lire mieux que quiconque.",
             COMPLETE : "Qu'a dit le Juge Ticot?\aOn avait raison? Oh non. Regardons ces plans.\aHmmm... On dirait que les Vendibots ont installé une usine avec l'outillage pour construire des Cogs.\aÇa a l'air très dangereux. N'y va pas tant que tu n'as pas plus de rigolpoints.\aQuand tu auras plus de rigolpoints, nous en aurons beaucoup à apprendre sur le quartier général des Vendibots.\aPour l'instant, bon travail, voilà ta récompense.",
            },


    3255 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux donner un coup de main._where_" },
    3256 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux donner un coup de main._where_" },
    3257 : { QUEST : "_toNpcName_ est en train d'enquêter sur le quartier général des Vendibots.\aVa voir si tu peux donner un coup de main._where_" },
    3258 : { QUEST : "Personne ne sait au juste ce que les Cogs sont en train de faire dans leur nouveau quartier général.\aJ'ai besoin que tu nous ramènes des informations venant directement d'eux.\aSi nous pouvons trouver quatre notes de service internes des Vendibots à l'intérieur de leur quartier général, cela mettrait un peu les choses au clair.\aRamène-moi la première note de service que tu pourras afin qu'on en sache un peu plus.",
             },
    3259 : { QUEST : "Super! Voyons ce que dit cette note de service...\a\" À l'attention des Vendibots : \aJe serai dans mon bureau tout en haut des Tours Vendibot pour faire monter en grade les Cogs. \aLorsque vous aurez gagné suffisamment de mérites, montez me voir par l'ascenseur du hall. \aLa pause est terminée - tout le monde au travail! \"\aSigné, Vice-Président des Vendibots \"\aAah.... Flippy sera content de voir ça. Je lui envoie ça tout de suite.\aVa chercher une seconde note de service et rapporte-la moi.",
             },
    3260 : { QUEST : "Oh, bien, tu es de retour. Voyons ce que tu as trouvé....\a\" À l'attention des Vendibots :\aLes Tours Vendibot ont été équipées d'un nouveau système de sécurité pour empêcher les Toons de pénétrer à l'intérieur. \aLes Toons qui seront attrapés dans les Tours Vendibot seront retenus pour interrogatoire. \aVeuillez en discuter dans le hall autour d'un apéritif. \aSigné, Le Circulateur \"\aTrès intéressant... Je communique l'information immédiatement.\aS'il te plaît, rapporte-moi une troisième note de service.",
             },
    3261 : { QUEST : "Excellent travail, _avName_! Que dit cette note de service?\a\" À l'attention des Vendibots : \aLes Toons sont parvenus à trouver une façon d'infiltrer les Tours Vendibot. \aJe vous appellerai ce soir pendant le dîner pour vous donner des détails. \aSigné, Télévendeur \"\aHmmm... Je me demande comment les Toons se sont infiltrés....\aRapporte-moi une note de service supplémentaire et je crois que nous aurons assez d'informations pour l'instant.",
             COMPLETE : "Je savais que tu pouvais le faire! OK, voilà ce que dit la note de service....\a\" À l'attention des Vendibots : \aJ'ai déjeûné avec M. Hollywood hier. \aIl dit que le Vice-Président est très occupé en ce moment. \aIl ne prendra de rendez-vous qu'avec les Cogs qui méritent une promotion. \aJ'allais oublier, Passetout joue au golf avec moi dimanche. \aSigné, Cafteur \"\aBon... _avName_, voilà qui est bien utile.\aVoilà ta récompense.",
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
    4207 : { QUEST : "Inventaire?\aComment est-ce que je pourrais faire un inventaire sans formulaire?\aVa voir Clément de sol et demande-lui s'il en a un pour moi._where_",
             INCOMPLETE_PROGRESS : "Alors, ce formulaire?",
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
             QUEST : "Merci. Ça va bien m'aider.\aVoyons...violons : 2\aÇa y est! Et voilà!",
             COMPLETE : "Bon travail, _avName_!\aJe suis sûr de pouvoir attraper ces voleurs maintenant.\aOn va pouvoir creuser cette affaire!",
             },

    4211 : { QUEST : "Dis donc, le Dr Tefaispasdebile appelle toutes les cinq minutes. Tu pourrais aller voir quel est son problème?_where_",
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

    4215 : { QUEST : "Anna a désespérément besoin de quelqu'un pour l'aider.\aPourquoi ne vas-tu pas voir ce que tu peux faire?_where_",
             },
    4216 : { QUEST : "Merci d'être là aussi vite!\aOn dirait que les Cogs sont partis avec les tickets de croisière de plusieurs de mes clients.\aYuki a dit qu'elle avait vu un Passetout sortir d'ici avec des tickets plein les mains.\aVa voir si tu peux retrouver le ticket pour l'Alaska de Jack Bûcheron.",
             INCOMPLETE_PROGRESS : "Ces Passetouts pourraient être n'importe où maintenant...",
             },
    4217 : { QUEST : "Oh, super. Tu l'as trouvé!\aPuisque je peux compter sur toi, va le porter à Jack pour moi, tu veux bien?_where_",
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

    4902 : { QUEST : "Va donc voir Léo.\aIl a besoin de quelqu'un pour porter un message._where_",
            },
    4903 : { QUEST : "Pote!\aMes castagnettes sont toutes ternies et j'ai un grand spectacle ce soir. \aEmporte-les donc à Carlos voir s'il peut me les faire reluire._where_",
             },
    4904 : { QUEST : "Voui, yé crois que yé peux réluire ça.\aMé yé bézoin d'encre de seiche bleue.",
             GREETING : "¡ Holà!",
             LEAVING : "¡ Adiós!",
             INCOMPLETE_PROGRESS : "Tou pé trrouver la seiche partout sour lé pontons de pêche.",
             },
    4905 : { QUEST : "Voui! Souperr!\aAhóra yé bézoin d'un peu de temps pour réluire ça.\aTou pé aller récoupérer un bâtiment de oun étage pendant qué yé trravaille?",
             GREETING : "¡ Holà!",
             LEAVING : "¡ Adiós!",
             INCOMPLETE_PROGRESS : "Oun pitite minute...",
             },
    4906 : { QUEST : "Trrès bien!\aVoilà les castagnettes pour Léo._where_",
             },
    4907 : { GREETING : "",
             QUEST : "Super, mon petit!\aElles sont superbes!\aMaintenant j'ai besoin que tu me rapportes une copie des paroles de \" Un Noël toon \" de chez Élise._where_",
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
             QUEST : "Excellent!\aMaintenant tu vas nous montrer ce que tu sais faire à la pêche.\aJ'ai fait tomber trois dés en peluche dans la mare hier.\aVa les pêcher et rapporte-les moi.",
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
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être venu.\aUn groupe de ces Chassetêtes est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5261 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Bifaces est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5262 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Sacasous est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5263 : { GREETING: "",
             QUEST : "Salut, _avName_. Je sais que je devrais te remercier d'être là.\aUn groupe de ces Tournegris est venu et a volé mon ballon de foot.\aLe chef m'a dit que je devais faire des économies et me l'a arraché!\aPeux-tu me rapporter mon ballon?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Est-ce que tu as retrouvé mon ballon de foot?",
             COMPLETE : "Youpiii! Tu l'as trouvé! Tiens, prends ta récompense...",
             },
    5202 : { QUEST : "Le "+lTheBrrrgh+" a été envahi par des Cogs parmi les plus robustes qu'on ait vus.\aTu auras probablement besoin d'emporter plus de gags là-bas.\aJ'ai entendu dire que _toNpcName_ pourrait te prêter un grand sac pour emporter plus de gags._where_" },
    5203 : { GREETING: "Eh? Tu es dans mon équipe de luge?",
             QUEST : "Qu'est-ce que c'est? Tu veux un sac?\aJ'en avais un par là...peut-être qu'il est dans ma luge?\aMais c'est que... Je n'ai pas vu ma luge depuis la grande course!\aPeut-être qu'un de ces Cogs l'a prise?",
             LEAVING : "As-tu vu ma luge?",
             INCOMPLETE_PROGRESS : "Rappelle-moi qui tu es? Désolé, je suis un peu étourdi depuis l'accident." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Est-ce que c'est ma luge? Je ne vois pas de sac par ici.\aJe crois que Boris Tourne était dans l'équipe...c'est peut-être lui qui l'a?_where_" },
    5205 : { GREETING : "Oooh, ma tête!",
             LEAVING : "",
             QUEST : "Hein? Ted qui? Un sac?\aAh, peut-être qu'il était dans notre équipe?\aJ'ai tellement mal à la tête que je n'arrive plus à réfléchir.\aPourrais-tu aller me pêcher des glaçons dans la mare gelée pour ma tête?",
             INCOMPLETE_PROGRESS : "Aïe, ma tête me fait mal! Tu as de la glace?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aah, ma tête va beaucoup mieux!\aAlors tu cherches le sac de Ted, hein?\aJe crois qu'il a atterri sur la tête de Sam Simiesque après l'accident._where_" },
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
             INCOMPLETE_PROGRESS : "Es-tu certain(e) d'être au point? Va donc démolir plus de Cogs. ",
             COMPLETE : "Ouah! T'es vachement chouette! C'est un sacré tas de Cogs que tu as bousillés!\aVoilà ton sac!" },

    5210 : { QUEST : "_toNpcName_ aime quelqu'un du quartier en secret.\aSi tu l'aides, elle pourrait te donner une belle récompense._where_" },
    5211 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs avec un bec me l'a dérobée.\aPeux-tu me la rapporter?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },

    5264 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs avec un aileron me l'a dérobée.\aPeux-tu me la rapporter?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5265 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs Circulateurs me l'a dérobée.\aPeux-tu me la rapporter?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5266 : { GREETING: "Bouhouhou.",
             QUEST : "J'ai passé toute la nuit dernière à écrire une lettre au chien que j'aime.\aMais avant que je puisse l'envoyer, un de ces méchants Cogs Attactics me l'a dérobée.\aPeux-tu me la rapporter?",
             LEAVING : "Bouhouhou.",
             INCOMPLETE_PROGRESS : "S'il te plaît, retrouve ma lettre." },
    5212 : { QUEST : "Oh, merci d'avoir retrouvé ma lettre!\aS'il te plaît, s'il te plaît, peux-tu la remettre au plus beau chien du quartier?",
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
             QUEST : "Qui est-ce qui t'envoie? On aime pas trop les bêcheurs, non...\aMais on aime encore moins les Cogs...\aDébarrasse-nous donc des gros et on t'aidera, oui on t'aidera." },
    5216 : { QUEST : "On t'avait bien dit qu'on t'aiderait.\aTu peux emmener cette bague à la fille.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu as encore la bague???",
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
             QUEST : "Tu sais quoi, peut-être finalement que ce ne sont pas du tout les Cogs!!!\aPourrais-tu demander à Gaëlle de me préparer une potion calmante? Ça m'aiderait peut-être...._where_" },
    5222 : { LEAVING : "",
             QUEST : "Oh, ce Harry, c'est quelqu'un!\aJe vais concocter quelque chose qui le remettra sur pied!\aBon, on dirait que je n'ai plus de moustaches de sardine...\aSois un ange et cours à la mare m'en attraper.",
             INCOMPLETE_PROGRESS : "Tu les as, ces moustaches de sardine?", },
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
    5225 : { QUEST : "Depuis l'incident avec le pain de navets, Phil Électrique est furieux après _toNpcName_.\aTu pourrais peut-être aider Paul à les réconcilier?_where_" },
    5226 : { QUEST : "Ouais, tu as sans doute entendu dire que Phil Électrique est furieux contre moi...\aJ'essayais juste d'être gentil avec ce pain de navets.\aPeut-être que tu pourrais le remettre de bonne humeur.\aPhil a horreur de ces Cogs Caissbots, surtout leurs bâtiments.\aSi tu reprends des bâtiments Caissbot, ça pourrait aider.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Peut-être quelques bâtiments de plus?", },
    5227 : { QUEST : "C'est formidable! Va dire à Phil ce que tu as fait._where_" },
    5228 : { QUEST : "Oh il a fait ça?\aCe Paul croit qu'il peut s'en tirer comme ça, hein?\aIl m'a cassé ma dent, oui, avec son fichu pain de navets!\aPeut-être que si tu amenais ma dent au Dr Marmotter, il pourrait la réparer.",
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
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent?" },
    5270 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement un Gros Blochon me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent?" },
    5271 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement M. Hollywood me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent?" },
    5272 : { GREETING: "",
             QUEST : "Je suis content que tu sois revenu(e)!\aJ'ai arrêté d'essayer de réparer cette vieille dent, et j'ai fait une nouvelle dent en or pour Phil à la place.\aMalheureusement un Chouffleur me l'a dérobée.\aTu peux peut-être le rattraper si tu cours.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu l'as retrouvée, cette dent?" },
    5231 : { QUEST : "Super, voilà la dent!\aPourquoi ne filerais-tu pas chez Phil pour lui porter?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Je parie que Phil serait content de voir sa nouvelle dent.",
             },
    5232 : { QUEST : "Oh, merci.\aMmmrrrphhhh\aÇa a l'air de quoi, hein?\aOK, tu peux dire à Paul que je lui pardonne.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Oh, bonne nouvelle.\aJe savais bien que ce vieux Phil ne pourrait pas rester fâché contre moi.\aPour prouver ma bonne volonté, je lui ai fait cuire ce pain de pommes de pin.\aPourrais-tu lui porter, s'il te plaît?",
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
             INCOMPLETE_PROGRESS : "Où est ce crapaud parlant?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Tu n'as pas encore gagné ton dessert.",
              QUEST : "Oh, c'est vraiment un crapaud parlant. Donne-le moi.\aQu'est-ce que tu dis, crapaud?\aCouac.\aCouac.\aLe crapaud a parlé. Nous avons besoin de dessert.\aRapporte-nous des cônes de glace de chez _toNpcName_.\aLe crapaud aime la glace aux haricots rouges pour une raison inconnue._where_", },
    5238 : { GREETING: "",
             QUEST : "Alors c'est le vieillard du blizzard qui t'envoie. Je dois dire qu'on vient de tomber en rupture de stock de cônes de glace aux haricots rouges.\aTu vois, un groupe de Cogs est venu et les a tous emportés.\aIls ont dit qu'ils étaient pour M. Hollywood ou quelque chose comme ça.\aJe serais ravi si tu pouvais me les rapporter.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu déjà trouvé tous mes cônes de glace?" },
    5280 : { GREETING: "",
             QUEST : "Alors c'est le vieillard du blizzard qui t'envoie. Je dois dire qu'on vient de tomber en rupture de stock de cônes de glace aux haricots rouges.\aTu vois, un groupe de Cogs est venu et les a tous emportés.\aIls ont dit qu'ils étaient pour le Gros Blochon ou quelque chose comme ça.\aJe serais ravi si tu pouvais me les rapporter.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé tous mes cônes de glace?" },
    5239 : { QUEST : "Merci de m'avoir rapporté mes cônes de glace!\aEn voilà un pour Allan Bic.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu ferais mieux de porter cette glace à Allan Bic avant qu'elle ne fonde.", },
    5240 : { GREETING: "",
             QUEST : "Très bien. Et voilà mon petit crapaud...\aSlurp, slurp...\aOK, maintenant nous sommes presque prêts.\aSi tu pouvais juste m'apporter de la poudre pour sécher mes mains.\aJe pense que ces Cogs Chouffleurs ont quelquefois de la poudre dans leurs perruques.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé de la poudre?" },
    5281 : { GREETING: "",
             QUEST : "Très bien. Et voilà mon petit crapaud...\aSlurp, slurp...\aOK, maintenant nous sommes presque prêts.\aSi tu pouvais juste m'apporter de la poudre pour sécher mes mains.\aJe crois que ces Cogs M. Hollywood ont quelquefois de la poudre pour se poudrer le nez.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "As-tu trouvé de la poudre?" },
    5241 : { QUEST : "OK.\aComme je l'ai déjà dit, pour bien lancer une tarte, tu ne dois pas la lancer avec la main...\a...mais avec ton âme.\aJe ne sais pas ce que cela veut dire, alors je vais m'asseoir et réfléchir pendant que tu récupères des bâtiments.\aReviens quand tu as terminé ton défi.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ton défi n'est pas terminé.", },
    5242 : { GREETING: "",
             QUEST : "Bien que je ne sache toujours pas de quoi je suis en train de parler, tu es vraiment quelqu'un de valeur.\aJe te donne un dernier défi...\aLe crapaud parlant voudrait une petite amie.\aTrouve un autre crapaud parlant. Le crapaud a parlé.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Où est cet autre crapaud parlant?",
             COMPLETE : "Houlala! Je suis fatigué par tous ces efforts. Je dois me reposer maintenant.\aTiens, prends ta récompense et va t'en." },

    5243 : { QUEST : "Pierre Lasueur commence à empester dans la rue.\aPeux-tu essayer de le convaincre de prendre une douche par exemple?_where_" },
    5244 : { GREETING: "",
             QUEST : "Oui, je crois que je dois commencer à transpirer pas mal.\aMmmm, peut-être que si je pouvais réparer ce tuyau qui fuit dans ma douche...\aJe crois qu'un pignon de l'un de ces tous petits Cogs ferait l'affaire.\aVa trouver un pignon de Microchef et on va essayer.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Où est ce pignon que tu étais parti chercher?" },
    5245 : { GREETING: "",
             QUEST : "Ouaip, on dirait que ça va.\aMais je me sens seul quand je prends ma douche...\aPourrais-tu aller me pêcher un canard en plastique pour me tenir compagnie?",
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
             INCOMPLETE_PROGRESS : "Alors, mon clavier?" },
    5273 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Circulateurs a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier?" },
    5274 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Usuriers a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier?" },
    5275 : { GREETING: "",
             QUEST : "Ouais, c'est bien mon micro.\aMerci de me l'avoir rapporté, mais...\aJ'ai vraiment besoin de mon clavier pour chatouiller les touches.\aJe crois qu'un de ces Avocageots a pris mon clavier.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Alors, mon clavier?" },
    5254 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont sûrement aux pieds d'un M Hollywood.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le "+lTheBrrrgh+" ce soir?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5282 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Gros Blochon.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le "+lTheBrrrgh+" ce soir?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5283 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Pillard.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le "+lTheBrrrgh+" ce soir?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },
    5284 : { GREETING: "",
             QUEST : "Tout va bien! Maintenant je peux travailler.\aSi seulement ils n'avaient pas pris mes chaussures à plate-forme...\aJe parie que mes chaussures sont aux pieds d'un Chouffleur.",
             LEAVING : "",
             COMPLETE : "Tout va bien! Je suis prêt maintenant.\aVous êtes tous prêts à mettre le feu dans le "+lTheBrrrgh+" ce soir?\aEh? Où sont-ils?\aOK, prends ça et ramène-moi des fans, d'accord?",
             INCOMPLETE_PROGRESS : "Je ne peux pas faire mon spectacle pieds nus, si?" },

    5255 : { QUEST : "On dirait que tu as besoin de plus de rigolpoints.\aPeut-être que tu pourrais passer un marché avec _toNpcName_.\aVérifie que c'est fait par écrit..._where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un marché est un marché.",
             QUEST : "Alors comme ça tu cherches des rigolpoints, hein?\aJ'ai un marché pour toi!\aOccupe-toi simplement de quelques Cogs Chefbots pour moi...\aEt je te garantis que tu n'y perdras pas." },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un marché est un marché.",
             QUEST : "Alors comme ça tu cherches des rigolpoints, hein?\aJ'ai un marché pour toi!\aOccupe-toi simplement de quelques Cogs Loibots pour moi...\aEt je te garantis que tu n'y perdras pas." },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "OK, mais je suis sûr de t'avoir dit de ramasser des Cogs Loibots.\aBon, si tu le dis, mais tu m'es redevable.",
             INCOMPLETE_PROGRESS : "Je ne crois pas que tu aies fini.",
             QUEST : "Tu dis que c'est fait? Tu as vaincu tous les Cogs?\aTu as dû mal comprendre, notre marché portait sur des Cogs Vendibots.\aJe suis certain de t'avoir dit de me vaincre des Cogs Vendibots." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "OK, mais je suis sûr de t'avoir dit de ramasser des Cogs Loibots.\aBon, si tu le dis, mais tu m'es redevable.",
             INCOMPLETE_PROGRESS : "Je ne crois pas que tu aies fini.",
             QUEST : "Tu dis que c'est fait? Tu as vaincu tous les Cogs?\aTu as dû mal comprendre, notre marché portait sur des Cogs Caissbots.\aJe suis certain de t'avoir dit de me vaincre des Cogs Caissbots." },
    }

# ChatGarbler.py
ChatGarblerDog = ["ouaf", "ouarf", "rrrgh"]
ChatGarblerCat = ["miaou", "maaou"]
ChatGarblerMouse = ["couic", "couiiic", "iiiiic"]
ChatGarblerHorse = ["hihiii", "brrr"]
ChatGarblerRabbit = ["ouic", "pouip", "plouik", "bouip"]
ChatGarblerFowl = ["coin", "couac", "coiinc"]
ChatGarblerDefault = ["bla bla"]

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

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Recherche de coordonnées pour %s."
AvatarDetailPanelFailedLookup = "Impossible d'obtenir les coordonnées de %s."
AvatarDetailPanelOnline = "District : %(district)s\nLocation: %(location)s"
AvatarDetailPanelOffline = "District : hors-ligne\nLieu : hors-ligne"

# AvatarPanel.py
AvatarPanelFriends = "Amis"
AvatarPanelWhisper = "Chuchoter"
AvatarPanelSecrets = "Secrets"
AvatarPanelGoTo = "Aller à"
AvatarPanelIgnore = "Ignorer"
#AvatarPanelCogDetail = "Dépt : %s\nNiveau: %s\n"
AvatarPanelCogLevel = "Niveau : %s"
AvatarPanelCogDetailClose = lClose

# DistributedAvatar.py
WhisperNoLongerFriend = "%s a quitté ta liste d'amis."
WhisperNowSpecialFriend = "%s est maintenant ton ami(e) secret(e)!"
WhisperComingToVisit = "%s vient te voir."
WhisperFailedVisit = "%s a essayé de venir te voir."
WhisperTargetLeftVisit = "%s est parti ailleurs. Essaie encore!"
WhisperGiveupVisit = "%s n'a pas pu te trouver parce que tu te déplaces!"
WhisperIgnored = "%s t'ignore!"
TeleportGreeting = "Salut, %s."
DialogSpecial = "ooo"
DialogExclamation = "!"
DialogQuestion = "?"
# Cutoff string lengths to determine how much barking to play
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# LocalAvatar.py
FriendsListLabel = "Amis"
WhisperFriendComingOnline = "%s se connecte!"
WhisperFriendLoggedOut = "%s s'est déconnecté."

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

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Je suis le chef."

# DistributedBattleFactory.py
FactoryBossTaunt = "Je suis le contremaître."
FactoryBossBattleTaunt = "Je te présente le contremaître."

# HealJokes.py
ToonHealJokes = [
    ["Qu'est ce qui fait PIOU-PIOU?",
     "Un poussin de 500 kilos! "],
    ["Que dit un pneu qui va voir un médecin?",
     "Docteur, je me sens crevé."],
    ["Pourquoi est-ce difficile pour un fantôme de mentir?",
     "Parce qu'il est cousu de fil blanc."],
    ["Vous connaissez l'histoire de la chaise?",
     "Dommage, elle est pliante!"],
    ["Qu'est-ce qui est vert et qui monte et qui descend?",
     "Un petit pois dans un ascenseur!"],
    ["Quel est le comble de l'électricien?",
     "De ne pas être au courant."],
    ["Que font deux chiens qui se rencontrent à Tokyo?",
     "Ils se jappent au nez."],
    ["Quel est le futur de \" je baille \"?",
     "Je dors."],
    ["Quel est l'animal le plus rapide?",
     "Le pou car il est toujours en tête!"],
    ["Quel animal n'a jamais soif?",
     "Le zébu, parce que quand zébu zé plus soif!"],
    ["Quel est le comble pour un myope?",
     "De manger des lentilles."],
    ["Pourquoi as-tu mis le journal dans le réfrigérateur?",
     "Pour avoir des nouvelles fraîches!"],
    ["Qu'est-ce qui est gris et qui t'éclabousse de confiture?",
     "Une souris qui mange un beignet."],
    ["Que demande un douanier à un cochon qui passe la frontière?",
     "Son passe-porc."],
    ["Que dit un bébé souris à sa maman quand il voit passer une chauve-souris?",
     "Maman, un ange!"],
    ["Comment appelle-t-on un ascenseur au Japon?",
     "En appuyant sur le bouton."],
    ["Comment appelle-t-on un poisson pas encore né?",
     "Un poisson pané."],
    ["Si tu fais tomber un chapeau blanc dans la mer rouge, comment ressort-il?",
     "Mouillé."],
    ["Que demande un chat qui entre dans une pharmacie?",
     "Du sirop pour matou."],
    ["Quel est le comble pour un jockey?",
     "D'être à cheval sur les principes."],
    ["Quelles sont les deux choses que tu ne peux pas prendre au petit-déjeuner?",
     "Le déjeuner et le dîner."],
    ["Qu'est ce qu'on donne à un éléphant qui a de grands pieds?",
     "De grandes chaussures."],
    ["Comment sait-on qu'un éléphant est caché dans le réfrigérateur?",
     "Aux empreintes de pattes dans le beurre."],
    ["Quelle est la différence entre un instituteur et un thermomètre?",
     "Aucune, on tremble toujours quand ils marquent zéro!"],
    ["Qu'est-ce qui est petit, carré et vert?",
     "Un petit carré vert."],
    ["Quel est le comble pour un éléphant?",
     "D'être sans défense."],
    ["Que dit le 0 au 8?",
     "Tiens, tu as mis ta ceinture!"],
    ["Qu'est ce qu'il ne faut jamais faire devant un poisson-scie?",
     "La planche!"],
    ["Pourquoi est-ce que certaines personnes travaillent la nuit?",
     "Pour mettre leur travail à jour."],
    ["Quel est le comble de la patience?",
     "Trier des petits pois avec des gants de boxe."],
    ["Qu'est ce qui voyage tout autour du monde en restant dans son coin?",
     "Un timbre."],
    ["Quel est le comble pour une souris?",
     "Avoir un chat dans la gorge."],
    ["Quel est le comble pour un canard?",
     "En avoir marre!"],
    ["Quel est le comble pour un magicien?",
     "Se nourrir d'illusions."],
    ["Quel est le comble de la clé?",
     "Se faire mettre à la porte."],
    ["Quel est le comble pour un cordonnier?",
     "Avoir les dents qui se déchaussent."],
    ["De quelle couleur sont les petits pois?",
     "Les petits poissons rouges."],
    ["Qu'est-ce qui baille et qui ne dort jamais?",
     "Une porte."],
    ["Tu sais ce que c'est un canif?",
     "C'est un p'tit fien!"],
    ["Qu'est-ce qu'un chou au fond d'une baignoire?",
     "Un choumarin!"],
    ["Quel est le comble pour le propriétaire d'un champ de pommiers?",
     "Travailler pour des prunes!"],
    ["Qu'est-ce qui est aussi grand que l'Arc de Triomphe mais ne pèse rien?",
     "Son ombre."],
    ["Comment s'appelle un boomerang qui ne revient pas?",
     "Un bout de bois."],
    ["Pourquoi est-ce que les éléphants se déplacent en troupeau compact?",
     "Parce que c'est celui du milieu qui a la radio."],
    ["De quelle couleur sont les parapluies quand il pleut?",
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
    ["Pourquoi les musiciens aiment-ils prendre le train?",
     "Parce que la voie fait ré."],
    ["Deux fourmis sont sur un âne, laquelle va doubler l'autre?",
     "Aucune, il est interdit de doubler sur un dos d'âne."],
    ["Quelle est la note la plus basse?",
     "Le sol."],
    ["Pourquoi les trains électriques vont-ils plus vite que les trains à vapeur?",
     "Parce qu'ils ont arrêté de fumer."],
    ["Qu'est ce qu'un arbuste dit à un géranium?",
     "Espèce d'empoté!"],
    ["Que recommande la maman allumette à ses enfants?",
     "Surtout, ne vous grattez pas la tête!"],
    ["Qu'est-ce qu'il y a à la fin de tout?",
     "La lettre T."],
    ["Pourquoi les poissons-chats s'ennuient-ils?",
     "Parce qu'il n'y a pas de poissons-souris."],
    ["Qu'est-ce que le vainqueur du marathon a perdu?",
     "Son souffle."],
    ["Comment appelle-t-on un spectacle qui rend propre?",
     "Un ballet."],
    ["Qu'est-ce qui fait 999 fois \" Tic \" et une fois \" Toc \"?",
     "Un mille-pattes avec une jambe de bois."],
    ["Comment reconnaît-on un écureuil d'une fourchette?",
     "En les mettant au pied d'un arbre, celui qui monte est l'écureuil."],
    ["Pourquoi les flamants roses lèvent-ils une patte en dormant?",
     "Parce qu'ils tomberaient s'ils levaient les deux."],
    ["Qu'est-ce qui est noir quand il est propre et blanc quand il est sale?",
     "Un tableau noir!"],
    ["Qu'est-ce qui fait Oh, Oh, Oh?",
     "Le Père Noël qui marche en arrière."],
    ["Qu'est-ce qui peut voyager jour et nuit sans quitter son lit?",
     "La rivière."],
    ["Quel arbre n'aime pas la vitesse?",
     "Le frêne."],
    ["Pourquoi est-ce que les dinosaures ont de longs cous?",
     "Parce que leurs pieds sentent mauvais."],
    ["Qu'est-ce qui est jaune et qui court très vite?",
     "Un citron pressé."],
    ["Pourquoi est-ce que les éléphants n'oublient jamais?",
     "Parce qu'on ne leur dit jamais rien."],
    ["Quel animal peut changer de tête facilement?",
     "Un pou."],
    ["Qu'est-ce qu'un steak caché derrière un arbre?",
     "Un steak caché."],
    ["Pourquoi est-ce que les serpents ne sont pas susceptibles?",
     "Parce qu'on ne peut pas leur casser les pieds."],
    ["Pourquoi dit-on que les boulangers travaillent rapidement?",
     "Parce qu'ils travaillent en un éclair."],
    ["Que dit un fantôme quand il est ennuyé?",
     "Je suis dans de beaux draps!"],
    ["Comment peut-on arrêter un éléphant qui veut passer dans le chas d'une aiguille?",
     "On fait un nœud à sa queue."],
    ["Pourquoi est-ce que les pompiers ont des bretelles rouges?",
     "Pour tenir leurs pantalons!"],
    ["Que prend un éléphant lorsqu'il rentre dans un bar?",
     "De la place!"],
    ["Savez-vous que votre chien aboie toute la nuit?",
     "Ça ne fait rien, il dort toute la journée!"],
    ["Savez-vous que le vétérinaire a épousé la manucure?",
     "Au bout d'un mois ils se battaient becs et ongles."],
    ["Tu sais que nous sommes sur terre pour travailler?",
     "Bon, alors plus tard je serai marin."],
    ["Quand je dis \" il pleuvait \", de quel temps s'agit-il?",
     "D'un sale temps."],
    ["À quoi reconnaît-on un motard heureux?",
     "Aux moustiques collés sur ses dents."],
    ["Son succès lui est monté à la tête.",
     "C'est normal, c'est là qu'il y avait le plus de place libre."],
    ["Qu'est-ce qui est gris, pousse de petits cris et fait 5 kilos?",
     "Une souris qui a besoin de se mettre au régime."],
    ["Que dit-on à un croque-mort qui rentre dans un café?",
     "\" Je vous sers une bière? \""],
    ["Connais-tu l'histoire du lit vertical?",
     "C'est une histoire à dormir debout."],
    ["Pourquoi est-ce que les éléphants sont gros et gris?",
     "Parce que s'ils étaient petits et jaunes ce seraient des canaris."],
    ["Combien coûte cet aspirateur?",
     "750 et des poussières."],
    ["Quel est le comble pour un juge gourmand?",
     "De manger des avocats."],
    ["Pourquoi "+ Donald + " regarde-t-il à droite et à gauche lorsqu'il rentre dans une pièce?",
     "Parce qu'il ne peut pas regarder des deux côtés à la fois."],
    ["Pourquoi est-ce que "+ Goofy + " emmène son peigne chez le dentiste?",
     "Parce qu'il a perdu toutes ses dents."],
    ["Quel bruit fait la fourmi?",
     "La fourmi cro-onde."],
    ["Si les sorties étaient surveillées, comment le voleur a-t-il pu s'échapper?",
     "Par l'entrée!"],
    ["Que dit un haut-parleur à un autre haut-parleur?",
     "Tu veux une baffle?"],
    ["Pourquoi les lézards aiment-ils les vieux murs?",
     "Parce qu'ils ont des lézardes."],
    ["Pourquoi est-ce que les moutons ont des pelages en laine?",
     "Parce qu'ils auraient l'air idiots avec des pelages en synthétique."],
    ["Où trouve-t-on le dimanche avant le jeudi?",
     "Dans le dictionnaire."],
    ["Pourquoi est-ce que "+ Pluto + " a dormi avec une peau de banane?",
     "Pour pouvoir se glisser hors de son lit le lendemain matin."],
    ["Pourquoi est-ce que la souris portait des chaussons noirs?",
     "Parce que les blancs étaient à la lessive."],
    ["Quel est le point commun entre les fausses dents et les étoiles?",
     "Elles sortent la nuit."],
    ["Pourquoi est-ce que les chats aiment se faire photographier?",
     "Parce qu'on leur dit \" souris! \"."],
    ["Pourquoi est-ce que l'archéologue a fait faillite?",
     "Parce que sa carrière était en ruines."],
    ["Qui boit l'eau sans jamais l'avaler?",
     "L'éponge."],
    ["Quelle est la couleur du virus de la grippe?",
     "Gris pâle."],
    ["Pourquoi faut-il craindre le soleil?",
     "Parce que c'est le plus grand des astres."],
    ["Quel est le comble d'un avion?",
     "C'est d'avoir un antivol."],
    ["Que dit la nappe à la table?",
     "Ne crains rien, je te couvre."],
    ["Que fait "+ Goofy + " quand il tombe dans l'eau?",
     "PLOUF!"],
    ["Quel est le comble pour un crayon?",
     "Se tailler pour avoir bonne mine."],
    ["Que dit la grosse cheminée à la petite cheminée?",
     "Tu es trop jeune pour fumer."],
    ["Que dit le tapis au carrelage?",
     "Ne t'inquiète pas, je te couvre."],
    ["Quelle est la différence entre le cancre et le premier de la classe?",
     "Quand le cancre redouble, c'est rarement d'attention."],
    ["Qu'est-ce qui fait zzzb zzzb?",
     "Une guêpe qui vole à l'envers."],
    ["Comment appelle-t-on quelqu'un qui tue son beau-frère?",
     "Un insecticide, car il tue l'époux de sa sœur."],
    ["Comment appelle-t-on un dinosaure qui n'est jamais en retard?",
     "Un promptosaure."],
    ["On ne devrait pas dire \" un chapitre \".",
     "On devrait dire \" un chat rigolo \"."],
    ["On ne devrait pas dire \" un perroquet \".",
     "On devrait dire \" mon papa est d'accord \"."],
    ["On ne devrait pas dire \" bosser à la chaîne \".",
     "On devrait dire \" travailler à la télé \"."],
    ["Pourquoi est-ce que le livre de maths était malheureux?",
     "Parce qu'il avait trop de problèmes."],
    ["On ne devrait pas dire \" un match interminable \".",
     "On devrait dire \" une rencontre de mauvais joueurs \"."],
    ["On ne devrait pas dire \" la maîtresse d'école \".",
     "On devrait dire \" l'institutrice prend l'avion \"."],
    ["Que voit-on quand deux mille-pattes se serrent la main?",
     "Une fermeture-éclair."],
    ["Comment appelle-t-on un journal publié au Sahara?",
     "Un hebdromadaire."],
    ["Que doit planter un agriculteur frileux?",
     "Un champ d'ail."],
    ["Quel est le comble du chauve?",
     "Avoir un cheveu sur la langue."],
    ["Qu'est-ce que tu trouves si tu croises un éléphant avec un corbeau?",
     "Des tas de poteaux téléphoniques cassés."],
    ["Combien gagne un fakir?",
     "Des clous!"],
    ["Quelle est la meilleure manière d'économiser l'eau?",
     "La diluer."],
    ["Quelle différence y a t il entre un horloger et une girouette?",
     "L'horloger vend des montres et la girouette montre le vent."],
    ["Pourquoi est-ce que les ordinateurs se grattent?",
     "Parce qu'ils sont pleins de puces."],
    ["Qu'est-ce qui a un chapeau et pas de tête, un pied mais pas de souliers?",
     "Un champignon."],
    ["Pourquoi est-ce que le ciel est haut?",
     "Pour éviter que les oiseaux ne se cognent la tête en volant."],
    ["Qu'est ce qui est pire qu'une girafe qui a mal à la gorge?",
     "Un mille-pattes avec des cors aux pieds."],
    ["Qu'est-ce qui fait ABC...gloups...DEF...gloups?",
     "Quelqu'un qui mange de la soupe aux pâtes alphabet."],
    ["Qu'est-ce qui est blanc et qui va vite?",
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
    ["Qu'est-ce qui est gris, fait 100 kilos et appelle \" Minou, Minou! \"?",
     "Une souris de 100 kilos."],
    ["Quel est le point commun entre un pâtissier et un ciel d'orage?",
     "Tous les deux font des éclairs."],
    ["Quel bruit font les esquimaux lorsqu'ils boivent?",
     "Iglou, iglou, iglou"],
    ["Comment appelle-t-on une chauve-souris avec une perruque?",
     "Une souris."],
    ["Pourquoi les aiguilles sont-elles moins intelligentes que les épingles?",
     "Parce qu'elles n'ont pas de tête."],
    ["Qu'est-ce qui a de la fourrure, miaule et chasse les souris sous l'eau?",
     "Un poisson-chat."],
    ["Comment fait-on aboyer un chat?",
     "Si on lui donne une tasse de lait il la boit."],
    ["Qu'est-ce qui est vert à l'extérieur et jaune à l'intérieur?",
     "Une banane déguisée en concombre."],
    ["Qu'est-ce qu'un ingrat?",
     "Le contraire d'un géant maigre."],
    ["Qu'est-ce qui pèse 4 tonnes, a une trompe et est rouge vif?",
     "Un éléphant qui a honte."],
    ["Dans un virage à 60 degrés à droite, quelle est la roue qui tourne le moins vite?",
     "La roue de secours."],
    ["Comment reconnaît-on un idiot dans un magasin de chaussures?",
     "C'est celui qui essaie les boîtes."],
    ["Que dit-on d'un enfant qui ramène le pain à la maison?",
     "C'est le petit calepin."],
    ["Que dit la cacahuète à l'éléphant?",
     "Rien, les cacahuètes ne parlent pas."],
    ["Que dit un éléphant lorsqu'il se heurte à un autre éléphant?",
     "Le monde est petit, n'est-ce pas?"],
    ["Que dit la comptable à la machine à calculer?",
     "Je compte sur toi."],
    ["Que dit la puce à une autre puce?",
     "On y va à pied ou on prend le chat?"],
    ["Que dit la grande aiguille à la petite aiguille?",
     "Attends une minute."],
    ["Que dit une poule quand elle rencontre une autre poule?",
     "Tu viens, on va prendre un ver?"],
    ["Que dit le collant à la chaussure?",
     "À plus tard, je dois filer."],
    ["Papa kangourou demande à sa fille qui rentre de l'école : \" Alors, cet examen? \"",
     "\" C'est dans la poche, pas de problème! \""],
    ["Quelle est la ville de France la plus féroce?",
     "Lyon."],
    ["Quelle est la ville de France la moins légère?",
     "Lourdes."],
    ["Pourquoi porte-t-on des vêtements?",
     "Parce qu'ils ne peuvent pas marcher tout seuls."],
    ["Que dit une pomme de terre quand elle en voit une autre se faire écraser dans la rue?",
     "\" Oh, purée! \""],
    ["Que dit un petit fakir quand il arrive en retard à l'école?",
     "\" Pardon maîtresse, je me suis endormi sur le passage clouté! \""],
    ["Que dit un marin-pêcheur s'il se dispute avec un autre marin-pêcheur?",
     "Je ne veux pas que tu me parles sur ce thon!"],
    ["Pourquoi les cultivateurs disent-ils des gros mots à leurs tomates?",
     "Pour les faire rougir."],
    ["Que disent deux vers de terre s'ils se rencontrent au milieu d'une pomme?",
     "\" Vous habitez dans le quartier? \""],
    ["Qu'est-ce que se disent deux serpents qui se rencontrent?",
     "\" Quelle heure reptile? \""],
    ["Pourquoi les mille-pattes ne peuvent-ils pas jouer au hockey?",
     "Le temps d'enfiler leurs patins, la partie est déjà terminée!"],
    ["Comment fait-on cuire un poisson dans un piano?",
     "On fait Do, Ré, La, Sol."],
    ["Connaissez-vous l'histoire du chauffeur d'autobus?",
     "Moi non plus, j'étais à l'arrière!"],
    ["Crois-tu aux girafes?",
     "Non, c'est un cou monté."],
    ["Que dit un crocodile s'il rencontre un chien?",
     "Salut, sac à puces!"],
    ["Que dit un chien quand il rencontre un crocodile?",
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
RewardPanelMeritsMaxed = "Au maximum"
RewardPanelMeritBarLabel = "Mérites"
RewardPanelMeritAlert = "Prêt pour la promotion!"

RewardPanelCogPart = "Tu as gagné un morceau de déguisement de Cog!"

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
SuitBeanCounterP = "Pince Menus"
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

SuitFaceoffTaunts = {
    'b':  ["Est-ce que tu as un don à me faire?",
           "Je vais faire de toi un mauvais perdant.",
           "Je vais te mettre à sec.",
           "Je suis \" A-Positif \", je vais gagner.",
           "Ne sois pas si \" O-Négatif \".",
           "Je suis surpris que tu m'aies trouvé, je suis très mobile.",
           "Je vais devoir te faire une addition rapide.",
           "Tu vas bientôt avoir besoin d'un en-cas.",
           "Quand j'aurai fini tu auras une grosse fatigue.",
           "Ça ne fait mal qu'un instant.",
           "Je vais te faire tourner la tête.",
           "Tu arrives à point, je suis en hypo.",
           ],
    'm':  ["Circule, y'a rien à voir.",
           "Tu fréquentes les gens comme moi?",
           "Bien, il faut être deux pour avoir de la compagnie.",
           "Allons voir la compagnie.",
           "Cela a l'air d'un bon endroit pour voir du monde.",
           "Bon, est-ce qu'on n'est pas bien ici?",
           "Tu frôles la défaite.",
           "Je vais me mêler de tes affaires.",
           "Est-ce que tu es sûr de vouloir voir du monde?",
           ],
    'ms': ["Attends-toi à une bonne secousse.",
           "Tu ferais mieux de ne pas rester dans le passage.",
           "Tu déménages ou tu perds.",
           "Je crois que c'est mon tour.",
           "Ça devrait te remuer.",
           "Prépare-toi à déménager.",
           "Ça va détonner.",
           "Attention, Toon, le terrain est instable.",
           "Ça va déménager.",
           "Je suis tout remué de te battre.",
           "Alors, tu trembles?",
           ],
    'hh': ["Je suis bien en tête.",
           "Tu t'entêtes à tort.",
           "Tu as la tête dure.",
           "Oh, bien, je te cherchais.",
           "J'aurai ta tête.",
           "Relève la tête!",
           "On dirait que tu as une tête à chercher les ennuis.",
           "Tu te payes ma tête?",
           "Un trophée parfait pour ma collection.",
           "Tu vas avoir un vrai mal de tête.",
           "Ne perds pas la tête à cause de moi.",
           ],
    'tbc': ["Attention, je vais te faire fondre.",
            "Je fais partie du gratin.",
            "Je t'ai gru, hier. Je peux être un roc fort quelquefois.",
            "Ah, finalement j'avais peur que tu en fasses tout un fromage.",
            "Je vais t'écrémer.",
            "Tu ne penses pas que je vieillis bien?",
            "Je vais te transformer en pâte à tartiner.",
            "On me dit que je suis très fort.",
            "Fais attention, je connais ta date de péremption.",
            "Fais attention, ma force est mon état menthal.",
            "Je vais te mouler à la louche.",
            ],
    'cr': ["À L'ATTAQUE!",
           "Tu n'as pas la culture d'entreprise.",
           "Prépare-toi à une descente.",
           "On dirait que tu fais l'objet d'une OPA.",
           "Ce n'est pas une tenue correcte pour l'entreprise.",
           "Tu as l'air vulnérable.",
           "Il est temps de transférer tes capitaux.",
           "Je suis engagé dans une croisade anti-Toons.",
           "Tu es sans défense face à mes idées.",
           "Calme-toi, tu verras que tout est pour le mieux.",
           ],
    'mh': ["Tu es prêt pour la prise?",
           "Lumières, action!",
           "Silence, on tourne.",
           "Aujourd'hui le rôle du Toon vaincu sera joué par - TOI!",
           "Cette scène va être coupée au montage.",
           "J'ai déjà une idée de ma motivation pour cette scène.",
           "Tu es prêt pour ta scène finale?",
           "Je suis prêt à signer ton générique de fin.",
           "Je t'ai dit de ne pas m'appeler.",
           "Que le spectacle continue!",
           "C'est un métier en or!",
           "J'espère que tu n'as pas oublié ton texte.",
           ],
    'nc': ["On dirait que ton numéro est terminé.",
           "J'espère que tu préfères les soustractions.",
           "Maintenant tu es vraiment en infériorité numérique.",
           "C'est déjà l'heure des comptes?",
           "Nous comptons sur quelque chose.",
           "Sur quoi voudrais-tu compter aujourd'hui?",
           "Ce que tu dis à de l'intérêt.",
           "Ça ne va pas être une opération facile.",
           "Vas-y, choisis un nombre.",
           "Je me contenterais d'un bon chiffre. ",
           ],
    'ls': ["C'est le moment de payer tes mensualités.",
           "Tu vis sur un emprunt.",
           "Ton prêt arrive à échéance.",
           "C'est le moment de payer.",
           "Tu as demandé une avance et elle est accordée.",
           "Tu vas payer ça cher.",
           "Il est temps de rembourser.",
           "Épargne-moi tes simagrées!",
           "C'est bien que tu sois là, je suis dans tous mes états.",
           "On en prend un pourcentage?",
           "Laisse-moi en profiter.",
           ],
    'mb': ["Par ici la monnaie.",
           "Je peux empocher ça.",
           "Papier ou plastique?",
           "Tu as ta sacoche?",
           "N'oublie pas, l'argent ne fait pas le bonheur.",
           "Attention, j'ai de la réserve.",
           "Tu vas avoir des ennuis d'argent.",
           "L'argent fait tourner le monde.",
           "Je suis trop riche pour ton cholestérol.",
           "On n'a jamais trop d'argent!",
           ],
    'rb': ["Tu t'es fait voler.",
           "Je te dépouillerai de cette victoire.",
           "Je t'ennuie royalement!",
           "Il faudra tout prendre avec le sourire.",
           "Tu devras signaler ce vol.",
           "Haut les mains.",
           "Je suis un adversaire de valeur.",
           "Je vais prendre tout ce que tu as.",
           "Tu peux appeler ça un vol de quartier.",
           "Tu devrais savoir qu'il ne faut pas parler aux étrangers.",
           ],
    'bs': ["Ne me tourne jamais le dos.",
           "Tu ne t'en retourneras pas.",
           "Tu vas me mettre à dos!",
           "Je suis bon pour réduire les frais.",
           "Je fais des choses dans ton dos.",
           "Tu as le dos au mur.",
           "Je suis le meilleur et je peux le prouver sur dossier.",
           "Allez, arrière Toon.",
           "Laisse-moi te mettre à dos.",
           "Tu vas avoir un mal de dos lancinant d'ici peu.",
           "C'est le coup parfait.",
           ],
    'bw': ["Ne me mets pas à la raie.",
           "Tu me fais friser.",
           "Je peux te faire une permanente si tu veux.",
           "On dirait que tu vas avoir des fourches.",
           "Tu ne peux pas affronter la vérité.",
           "C'est ton tour de te faire teindre.",
           "Je suis content que tu sois à l'heure pour ta coupe.",
           "Tu as de gros ennuis.",
           "Je vais me mettre un poil en colère.",
           "J'ai un gros poil sur la conscience, petit Toon.",
           ],
    'le': ["Attention, mon avocat est un peu dur.",
           "Je suis vert de rage.",
           "Je suis couvert par la loi.",
           "Tu devais savoir que j'ai des instincts meurtriers.",
           "Je vais te donner des cauchemars judiciaires.",
           "Tu ne gagneras pas ce procès.",
           "Ça devrait être interdit tellement c'est marrant.",
           "Légalement, tu es trop minuscule pour moi.",
           "Mon avidité ne connaît aucune limite.",
           "C'est une arrestation citoyenne.",
           ],
    'sd': ["Tu ne sauras jamais quand j'arrêterai de tourner.",
           "Laisse-moi te faire faire un tour.",
           "Le docteur va te voir dès qu'il aura fini sa tournée.",
           "Je vais te faire tourner.",
           "On dirait que tu as besoin d'aller faire un tour.",
           "Chacun son tour, le Toon s'en va.",
           "Tu n'aimeras pas mon tour de main.",
           "Tu vas tourner à fond.",
           "Tu veux faire quelques tours avec moi?",
           "J'ai un tour de main particulier.",
           ],
    'f': ["Je vais parler de toi au patron!",
          "Je suis peut-être juste un larbin - mais je suis un vrai dur.",
          "Je t'utilise pour monter les échelons.",
          "Tu n'aimeras pas la manière dont je travaille.",
          "Le patron compte sur moi pour te barrer la route.",
          "Tu feras bien sur mon CV.",
          "Tu devras me passer sur le corps.",
          "Voyons comment tu évalues mon rendement au travail.",
          "J'excelle dans la détoonisation.",
          "Tu ne verras jamais mon patron.",
          "Je te renvoie au terrain de jeux.",
          ],
    'p':  ["Je vais t'effacer.",
           "Tu ne peux pas me gommer.",
           "Je suis un numéro 2!",
           "Je vais te supprimer de mes listes.",
           "Je vais te l'écrire plus clairement.",
           "Allons droit au but.",
           "Dépêchons-nous, je fais rapidement des taches.",
           "Je m'inscris en faux.",
           "Tu veux t'inscrire?",
           "Tu m'as inscrit sur la liste?",
           "Attention, je peux laisser des taches.",
           ],
    'ym': ["Je suis certain que tu ne vas pas aimer ça.",
           "Je ne connais pas la signification du mot \" non \".",
           "Tu veux me voir? C'est quand tu veux.",
           "Tu as besoin d'une mise à exécution positive.",
           "Je vais te faire une impression positive.",
           "Je n'ai encore jamais eu tort.",
           "Oui, je suis prêt pour toi.",
           "C'est vraiment ce que tu veux?",
           "Je suis certain de terminer ça sur une note positive.",
           "Je confirme notre rendez-vous.",
           "Je n'accepte pas les refus.",
           ],
    'mm': ["Je vais me mêler de tes affaires!",
           "Quelquefois les gros ennuis ont l'air tout petits.",
           "Il n'y a pas de trop petit travail pour moi.",
           "Je veux que le travail soit bien fait, donc je le ferai moi-même.",
           "Tu as besoin de quelqu'un pour s'occuper de ton capital.",
           "Oh, bien, un projet.",
           "Chapeau, tu as réussi à me trouver.",
           "Je crois que tu as besoin d'un peu de gestion.",
           "Je vais m'occuper de toi dans peu de temps.",
           "Je surveille le moindre de tes mouvements.",
           "C'est vraiment ce que tu veux faire?",
           "On va faire ça à ma façon.",
           "Je vais espionner tout ce que tu fais.",
           "Je peux être très intimidant.",
           ],
    'ds': ["Tu descends!",
           "Tu as de moins en moins d'options.",
           "Attends-toi à des bénéfices en diminution.",
           "Tu viens juste de devenir réductible.",
           "Ne me demande pas de licencier.",
           "Je vais devoir faire quelques coupes claires.",
           "Les choses n'ont pas l'air d'aller bien fort pour toi.",
           "Tu as l'air tout ratatiné!",
           ],
    'cc': ["Surpris de me voir?",
           "Tu as appelé?",
           "Tu te prépares à accepter ma facture?",
           "Ce Casse-pieds ramasse toujours.",
           "Je suis un petit malin.",
           "Reste en ligne -- je suis là.",
           "Tu attendais mon appel?",
           "J'espérais que tu répondrais à mon appel.",
           "Je vais te faire une impression du diable.",
           "J'appelle toujours directement.",
           "Eh bien, ta ligne a été transférée.",
           "Cet appel va te coûter cher.",
           "Il y a de la friture sur la ligne.",
           ],
    'tm': ["Je crains que ça ne soit peu pratique pour toi.",
           "Est-ce que mon contrat d'assurance pourrait t'intéresser?",
           "Tu n'aurais pas dû répondre.",
           "Tu ne pourras pas te débarrasser de moi comme ça.",
           "Un moment difficile? Bien.",
           "J'avais l'intention de te rencontrer.",
           "Je vais t'appeler en PCV.",
           "J'ai des articles coûteux pour toi aujourd'hui.",
           "Dommage pour toi - je démarche à domicile.",
           "Je suis préparé à conclure cette affaire rapidement.",
           "Je vais utiliser une bonne partie de tes ressources.",
           ],
    'nd': ["Je vais traîner ton nom dans la boue.",
           "J'espère que tu ne m'en voudras pas si je donne ton nom.",
           "On ne s'est pas déjà rencontrés?",
           "Dépêchons-nous, je mange avec M. Hollywood.",
           "Je t'ai déjà dit que je connaissais Le Circulateur?",
           "Tu ne m'oublieras jamais.",
           "Je connais tous les gens qu'il faut pour démolir ta réputation.",
           "Je crois que je vais rester une minute.",
           "Je suis d'humeur à faire tomber des Toons.",
           "Tu le dis, je le répète.",
           ],
    'gh': ["Mets ça là, Toon.",
           "Serrons-nous la main.",
           "Ça va me plaire.",
           "Tu remarqueras que j'ai une poignée de main très ferme.",
           "Concluons ce marché.",
           "Occupons-nous des affaires que nous avons à portée de main.",
           "Je te dirais sans ménagements que tu as des ennuis.",
           "Tu te rendras compte que je suis plutôt manuel.",
           "Je peux être pratique.",
           "Je suis un gars très pratique, j'ai tout sous la main.",
           "Tu veux des vêtements de deuxième main?",
           "Laisse-moi te montrer mon travail manuel.",
           "Je crois que c'est fait main.",
           ],
    'sc': ["Je vais faire un petit échange avec toi.",
           "Tu vas avoir des ennuis d'argent.",
           "Tu vas être en surtaxe d'ici peu.",
           "Ce sera une mission de courte durée.",
           "J'en aurai bientôt fini avec toi.",
           "Tu vas bientôt te trouver à court.",
           "Arrêtons-nous tout net.",
           "Je crois que tu es un peu à court.",
           "Je ne suis pas économe avec les Toons.",
           "Tu seras bientôt sous bonne garde.",
           "Tu vas recevoir une facture d'ici peu.",
           ],
    'pp': ["Ça va piquer un peu.",
           "Je vais te donner une chance d'économiser.",
           "Tu ne veux pas garder ta chance rien que pour toi!",
           "Je vais figer ton sourire.",
           "Parfait, j'ai une ouverture pour toi.",
           "Laisse-moi ajouter mon grain de sel.",
           "On m'a demandé de faire un remplacement.",
           "Je te prouverai que tu ne rêves pas.",
           "Pile tu perds, face je gagne.",
           "Un petit sou pour tes gags.",
           ],
    'tw': ["Le budget est de plus en plus serré.",
           "C'est M. Grippesou qui te parle.",
           "Je vais réduire tes subventions.",
           "C'est ce que tu peux offrir de mieux?",
           "Ne perdons pas de temps - le temps c'est de l'argent.",
           "Tu te rendras compte que je suis plutôt économe.",
           "Tu n'as pas les coudées franches.",
           "Prépare-toi à suivre une voie difficile.",
           "J'espère que c'est dans tes moyens.",
           "Je vais mettre la pression sur le budget.",
           "Je vais faire une compression sur ton budget.",
           ],
    'bc': ["J'aime soustraire les Toons.",
           "Tu peux compter sur moi pour te faire payer.",
           "Pince qui peut.",
           "Je peux te pincer là où ça fait mal.",
           "La menue monnaie compte aussi.",
           "Ta note de frais arrive trop tard.",
           "C'est le moment de faire un audit.",
           "Allons dans mon bureau.",
           "Il y a quoi au menu?",
           "J'en pince pour toi.",
           "Tu vas te faire pincer.",
           ],
    'bf': ["On dirait que ton moral est bas.",
           "Je suis prêt à m'envoler!",
           "Je suis un pigeon pour les Toons.",
           "Oh, un vol-au-vent pour déjeuner.",
           "Ça suffira, j'ai un appétit de moineau.",
           "J'ai besoin d'un retour sur mes performances. ",
           "Parlons un peu du fond de la question.",
           "Tu te rendras compte que mes talents sont insondables.",
           "Bien, j'ai besoin d'un petit remontant.",
           "J'aimerais bien t'avoir pour déjeuner.",
           ],
    'tf': ["C'est le moment de se dévoiler!",
           "Tu ferais mieux de regarder la défaite en face.",
           "Prépare-toi à faire face à ton pire cauchemar!",
           "Regarde-le en face, je suis meilleur que toi.",
           "Deux têtes valent mieux qu'une.",
           "Il faut être deux pour danser, tu veux danser?",
           "Tu sur le chemin d'avoir deux fois plus d'ennuis.",
           "Quelle joue veux-tu tendre en premier?",
           "Je suis deux de trop pour toi.",
           "Tu ne sais pas qui tu as en face de toi.",
           "Tu te prépare à regarder ton destin en face?",
           ],
    'dt': ["Je vais te créer des ennuis incompréhensibles.",
           "Arrête-moi si tu ne comprends pas.",
           "Je suis si mystérieux.",
           "C'est le moment de parler à tort et à travers.",
           "J'envisage d'utiliser un double langage.",
           "Tu ne vas pas aimer mon double jeu.",
           "Tu devrais y réfléchir à deux fois.",
           "Attends-toi à te ne pas tout comprendre.",
           "Tu veux m'embrouiller.",
           "Garçon, la même chose!",
           ],
    'ac': ["Je vais te chasser de la ville!",
           "Tu entends la sirène?",
           "Ça va me plaire.",
           "J'aime l'ambiance de la chasse.",
           "Laisse-moi t'épuiser.",
           "Tu as une assurance?",
           "J'espère que tu as apporté une civière avec toi.",
           "Je doute que tu puisses te mesurer à moi.",
           "Ça grimpe à partir d'ici.",
           "Tu vas bientôt avoir besoin de soins.",
           "Il n'y a pas de quoi rire.",
           "Je vais te donner de quoi t'occuper.",
           ]
    }


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
    'Bite': ["Tu en veux une bouchée?",
             "Essaye d'en mordre un morceau!",
             "Tu as les yeux plus gros que le ventre.",
             "Je mords plus que je n'aboie.",
             "Avale donc ça!",
             "Attention, je pourrais mordre.",
             "Je ne fais pas que mordre quand je suis coincé.",
             "J'en veux juste une petite bouchée.",
             "Je n'ai rien avalé de la journée.",
             "Je ne veux qu'un petit morceau. C'est trop demander?",
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
                  "Tu es prêt(e) pour le grand déménagement?",
                  "J'ai les neurones en feu.",
                  "Ça casse des briques.",
                  "Rien de tel qu'un remue-méninges.",
                  ],
    'BuzzWord':["Excuse-moi si je radote.",
                "Tu connais la dernière?",
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
                  "Je peux t'aider à faire cette addition?",
                  "Tu as bien enregistré toutes tes dépenses?",
                  "D'après mes calculs, tu n'en as plus pour longtemps.",
                  "Voilà le total général.",
                  "Houlà, ton addition est bien longue.",
                  "Essaie de trafiquer ces chiffres!",
                  Cogs + " : 1 Toons : 0",
                  ],
    'Canned': ["Tu aimes quand c'est en boîte?",
               "Tu peux t'occuper des boîtes?",
               "Celui-là vient de sortir de sa boîte!",
               "Tu as déjà été attaqué par des boîtes de conserve?",
               "J'aimerais te faire un cadeau qui se conserve!",
               "Tu es prêt pour la mise en boîte?",
               "Tu crois que tu es bien conservé?",
               "Tu vas être emballé!",
               "Je me fais du Toon à l'huile pour dîner!",
               "Tu n'es pas si mangeable que ça en conserve.",
               ],
    'Chomp': ["Tu as une mine de papier mâché!",
              "Croc, croc, croc!",
              "On va pouvoir se mettre quelque chose sous la dent.",
              "Tu as besoin de grignoter quelque chose?",
              "Tu pourrais grignoter ça!",
              "Je vais te manger pour le dîner.",
              "Je me nourrirais bien de Toons!",
              ],
    'ClipOnTie': ["Il faut s'habiller pour la réunion.",
                  "Tu ne peux PAS sortir sans ta cravate.",
                  "C'est ce que portent "+theCogs+" les plus élégants."
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
               "Tu préfères tendre ou croquant?",
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
                 "Tu sais comment redescendre?",
                 "Revenons à nos affaires.",
                 "Qu'est-ce qui ne va pas? Tu as l'air d'avoir le moral dans les chaussettes.",
                 "Tu descends?",
                 "Qu'est-ce qui te chiffonne? Toi!",
                 "Pourquoi est-ce que tu choisis des gens de ma taille?",
                 "Pourquoi es-tu si terre-à-terre?",
                 "Est-ce que tu voudrais un modèle plus petit pour seulement dix cents de plus?",
                 "Essaie pour voir si la taille te va!",
                 "Ce modèle est disponible dans une plus petite taille.",
                 "C'est une attaque à taille unique!",
                 ],
    # Hmmm - where is double talker?
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
    'Filibuster':["Est-ce que je dois te barrer la route?",
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
                  "Tu n'as aucun respect pour nous les " + Cogs + ".",
                  "Il est grand temps de faire attention.",
                  "Blablablablabla.",
                  "Ne m'oblige pas à mettre fin à cette réunion.",
                  "Est-ce que je vais devoir te séparer?",
                  "On est déjà passés par là.",
                  ],
    'Fired': ["J'espère que tu as apporté des rafraîchissements.",
              "On s'embête solide.",
              "Ça va nous rafraîchir.",
              "J'espère que tu as le sang froid.",
              "J'ai la gorge sèche.",
              "Va donc nager un peu!",
              "Tu es déjà sur le départ.",
              "Encore un peu de sauce?",
              "Tu peux dire \" aïe \"?",
              "J'espère que tu sais nager.",
              "Tu es en phase de déshydratation?",
              "Je vais te liquider!",
              "Tu vas finir en bouillie.",
              "Tu n'es qu'un feu de paille.",
              "Je me trouve fondant.",
              "Je suis d'une limpidité!",
              "Et on n'en parle plus!.",
              "Un Toon à la mer!.",
              ],
    'FountainPen': ["Ça va tacher.",
                    "Mettons ça par écrit.",
                    "Prépare-toi à des ennuis indélébiles.",
                    "Tu vas avoir besoin d'un bon nettoyage à sec.",
                    "Tu devrais corriger.",
                    "Ce stylo écrit si bien.",
                    "Voilà, je prends mon crayon.",
                    "Tu peux lire mon écriture?",
                    "Et voilà la plume de l'apocalypse.",
                    "Ta performance est entachée.",
                    "Tu n'as pas envie de tout effacer?",
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
                    "Tu n'aimes pas que je te regarde?",
                    "Voilà, je te regarde.",
                    "Tu ne trouves pas que j'ai un regard expressif?",
                    "Mon regard est mon point fort.",
                    "C'est le regard qui compte.",
                    "Coucou, je te vois.",
                    "Regarde-moi dans les yeux...",
                    "Est-ce que tu voudrais voir ton avenir?",
                    ],
    'GuiltTrip': ["Tu vas vraiment te sentir coupable!",
                  "Tu te sens coupable!",
                  "C'est entièrement de ta faute!",
                  "C'est toujours ta faute.",
                  "Tu te complais dans la culpabilité!",
                  "Je ne te reparlerai plus jamais!",
                  "Tu ferais mieux de t'excuser.",
                  "Jamais je ne te pardonnerai!",
                  "Tu veux bien te faire de la bile?",
                  "Rappelle-moi quand tu ne te sentiras plus coupable.",
                  "Quand finiras-tu par te pardonner à toi-même?",
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
                   "Tu rétrécis au lavage?",
                   "Je rétrécis donc je suis.",
                   "Il n'y a pas de quoi perdre la tête.",
                   "Où as-tu la tête?",
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
              "Tu as compris ce que je voulais dire?",
              "Des mots, rien que des mots.",
              ],
    'Legalese':["Tu dois cesser d'être et renoncer.",
                "Tu vas être débouté(e), légalement parlant.",
                "Tu es au courant des implications légales?",
                "Tu n'es pas au-dessus des lois!",
                "Il devrait y avoir une loi contre toi.",
                "Il n'y a rien de postérieur aux faits!",
                "Toontown en ligne de Disney n'est pas légalement responsable des opinions exprimées dans cette attaque.",
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
                   "Est-ce que je dois mener la récession?",
                   "Tout le monde s'enfuit, tu devrais peut-être en faire autant?",
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
                    "Pourquoi est-ce que je ne trouve pas d'adversaire à ma taille? Bof.",
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
                   "Ça ne te gêne pas que ça me gêne?",
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
    'PlayHardball': ["Tu veux employer les grands moyens? ",
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
                 "Allo Toon, c'est pour toi.",
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
                  "Qui a les méga pouvoirs maintenant?",
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
              "Tu as déjà ressenti un tremblement de terre?",
              "Tu es sur un terrain instable!",
              ],
    'RazzleDazzle': ["Chante avec moi.",
                     "Tu as peur de perdre ton dentier?",
                     "Je ne suis pas charmant?",
                     "Je vais t'impressionner.",
                     "Mon dentiste fait un excellent travail.",
                     "Ils ne sont pas épatants?",
                     "Difficile de croire qu'ils ne sont pas réels.",
                     "Ils ne sont pas choquants?",
                     "Ça va décoiffer.",
                     "Je me lave les dents après tous les repas.",
                     "Dis \" Cheese! \"",
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
              "Est-ce que tu apprécies mes capacités d'organisation?",
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
                         "Pourquoi ne commençons-nous pas par les contraintes de base?"
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
                "Est-ce que c'est comme ça que je peux te contacter?",
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
               "Laisse moi m'occuper de tes zones à problèmes.",
               ],
    'Sacked':["On dirait que tu vas te faire licencier.",
              "L'affaire est dans le sac.",
              "Tu as une licence de vol?",
              "De chasse ou de pêche?",
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
              "Ce n'est pas ton dernier fragment d'espoir?",
              ],
    'Spin': ["Tu veux qu'on aille faire un tour?",
             "À quelle vitesse tournes-tu?",
             "Ça va te faire tourner la tête!",
             "C'est le tour que prennent les choses.",
             "Je vais t'emmener faire un tour.",
             "Que feras-tu quand ce sera ton tour?",
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
               "Pourquoi es-tu en colère?",
               "Essaye simplement d'éviter le danger.",
               "Scrongneugneu!",
               "Tu vas prendre la mouche à tous les coups.",
               "Tu es sur mon chemin.",
               "J'ai une bonne prise sur la situation.",
               "Attention le petit oiseau va se fâcher!",
               "Garde un œil sur moi!",
               "Ça te dérange si je joue?",
               ],
    'Tremor': ["Tu as senti ça?",
               "Tu n'as pas peur d'un petit frémissement n'est-ce pas?",
               "Au commencement était le frémissement.",
               "Tu as l'air de trembler.",
               "Je vais un peu secouer les choses!",
               "Tu te prépare à sursauter?",
               "Qu'est-ce qui ne va pas? Tu as l'air d'accuser la secousse.",
               "Crainte et tremblements!",
               "Pourquoi trembles-tu de peur?",
               ],
    'Watercooler': ["Ça devrait te rafraîchir.",
                    "Tu ne trouves pas ça rafraîchissant?",
                    "Je livre les boissons.",
                    "Directement du robinet dans ton gosier.",
                    "C'est quoi le problème, c'est juste de l'eau de source.",
                    "Ne t'inquiète pas, c'est filtré.",
                    "Ah, un autre client satisfait.",
                    "C'est l'heure de ta livraison quotidienne.",
                    "J'espère que les couleurs ne vont pas déteindre.",
                    "Tu as envie de boire?",
                    "Tout s'en va à la lessive.",
                    "C'est toi qui payes à boire.",
                    ],
    'Withdrawal': ["Je crois que tu es à découvert.",
                   "J'espère que ton compte est suffisamment approvisionné.",
                   "Prends ça, avec les intérêts.",
                   "Ton solde n'est pas en équilibre. ",
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
ElevatorHopOff = lQuit

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = ", Inc."
CogsIncModifier = "%s "+ CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Toc, toc."
DoorWhosThere = "Qui est là?"
DoorWhoAppendix = "qui?"

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

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Qui",
    "Il y a un mauvais écho par ici, n'est-ce pas?"],

    ["Douglas",
    "Douglas à la vanille ça t'intéresse?"],

    ["Geoffrey",
    "Geoffrey bien une petite sieste, laisse-moi entrer."],

    ["Justin",
    "Justin petit moment."],

    ["Adhémar",
    "Adhémar pas ta voiture?"],

    ["Annie",
    "Annie rien comprendre, pourquoi tu n'ouvres pas?"],

    ["Omer",
    "Omer veille, j'ai fini par te trouver."],

    ["Thérèse",
    "Thérèse, t'es là sans bouger depuis tout ce temps?"],

    ["Sylvie",
    "Sylvie c'est un miracle, laisse-le au moins entrer."],

    ["Aude",
    "Aude toilette à la lavande ce matin?"],

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
    "Yann-Adam le frigo je peux entrer?"],

    ["Louis",
    "Louis pas trop fine, décidément."],

    ["Mélusine",
    "Mélusine des Cogs en faillite, au lieu de dormir."],

    ["Kim",
    "Kim énerve, à ne pas ouvrir."],

    ["Ella",
    "Ella pas envie de descendre ouvrir?"],

    ["Jean",
    "Jean file un pull et j'arrive."],

    ["Roger",
    "Roger plus rien dans le frigo, tu peux aller faire les courses?"],

    ["John",
    "John Dœuf est déjà passé vendre de la mayonnaise?"],

    ["Alain",
    "Alain d'Issoire! C'est ça, bon dimanche."],

    ["Steve",
    "Steve a, j'y vais aussi."],

    ["Elvire",
    "Elvire pas sur ses gonds, ta porte."],

    ["Jean",
    "Jean, bon, je peux entrer finalement?"],

    ["Sarah",
    "Sarah fraîchit dernièrement, j'ai froid dehors."],

    ["Aïcha",
    "Aïcha fait mal aux mains de frapper à ta porte."],

    ["Sarah",
    "Sarah croche toujours au téléphone, tu ne veux vraiment pas me parler?"],

    ["Déborah",
    "Déborah, dis, qu'il y a dans ton jardin, je peux les voir?"],

    ["Eddy",
    "Eddy donc toi là-bas, tu vas finir par venir?"],

    ["Élie ",
    "Élie quoi? Le journal est déjà arrivé?"],

    ["Mandy",
    "Mandy donc tu fais quoi là? "],

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
    "Médor, Médor, mais comment veux-tu que je dorme si tu ne me laisses pas entrer?"],

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
    "Cécile est de bonne humeur qu'il vient ouvrir la porte?"],

    ["Djemila",
    "Djemila clé dans la serrure mais ça ne marche pas."],

    ["Éléonore",
    "Éléonore maintenant mais j'ai pas sa nouvelle adresse."],

    ["Huguette",
    "Huguette si quelqu'un d'autre arrive?"],

    ["Isolde",
    "Isolde pas, tout est au prix fort."],

    ["Jenny",
    "Jenny figues ni raisin, l'épicerie a déménagé."],

    ["Jérémie",
    "Jérémie le courrier à la poste, maintenant je suis rentré."],

    ["Jimmy.",
    "Jimmy ton courrier dans la boîte"],

    ["Johnny.",
    "Johnny connais rien du tout, viens donc voir ça."],

    ["Julie",
    "Julie pas très bien ce qui est écrit sur la porte."],

    ["Cathy",
    "Cathy donc dit?"],

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
    "Thor ait le temps de descendre ouvrir?"],

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
    "Célestin? Non c'est l'ouest."],

    ["Ondine",
    "Ondine où ce soir?"],

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

# ChatInputNormal.py
ChatInputNormalSayIt = "Dis-le"
ChatInputNormalCancel = lCancel
ChatInputNormalWhisper = "Chuchoter"
ChatInputWhisperLabel = "À %s"

# ChatInputSpeedChat.py
SCEmoteNoAccessMsg = "Tu n'as pas encore accès\nà cette émotion."
SCEmoteNoAccessOK = lOK

# ChatManager.py
ChatManagerChat = "Chat"
ChatManagerWhisperTo = "Chuchoter à :"
ChatManagerWhisperToName = "Chuchoter à :\n%s"
ChatManagerCancel = lCancel
ChatManagerWhisperOffline = "%s est déconnecté(e)."
OpenChatWarning = "Tu n'as pas encore d'\" amis secrets \"! Tu ne peux pas discuter avec les autres Toons s'ils ne sont pas tes amis secrets.\n\nPour devenir ami(e) secret(e) avec quelqu'un, clique sur lui ou sur elle, et sélectionne \" Secrets \" dans le panneau d'informations. Bien entendu, tu peux toujours parler à n'importe qui avec le Chat rapide."
OpenChatWarningOK = lOK
UnpaidChatWarning = "Une fois que tu es inscrit(e), tu peux utiliser ce bouton pour discuter avec tes amis à l'aide du clavier. Avant cela, tu dois discuter avec les autres Toons à l'aide du Chat rapide."
UnpaidChatWarningPay = "S'inscrire maintenant!"
UnpaidChatWarningContinue = "Continuer l'essai gratuit"
PaidNoParentPasswordWarning = "Une fois que tu as choisi un mot de passe \" parent \", tu peux utiliser ce bouton pour discuter avec tes amis à l'aide du clavier. Avant cela, tu dois discuter avec les autres Toons à l'aide du Chat rapide."
PaidNoParentPasswordWarningSet = "Établir le mot de passe \"parent\"!"
PaidNoParentPasswordWarningContinue = "Continuer à jouer"
PaidParentPasswordUKWarning = "Une fois le Chat activé vous pourrez discuter avec vos amis en utilisant le clavier. Si vous decidez de ne pas activer le Chat vous pourrez continuer à utiliser le Chat Rapide  pour discuter avec les autres Toons."
PaidParentPasswordUKWarningSet = "Activer le Chat!"
PaidParentPasswordUKWarningContinue = "Continuer à jouer."
NoSecretChatAtAllTitle = "Chat \" amis secrets \"."
NoSecretChatAtAll = "Pour discuter avec un(e) ami(e), la fonction \" amis secrets \" doit être activée. La fonction \" amis secrets \" permet à un membre de discuter avec un autre membre uniquement à l'aide d'un code secret qui doit être communiqué en dehors du jeu.\n\nPour activer cette fonction ou pour en savoir plus à propos de son fonctionnement, sortez du jeu Toontown et cliquez sur \" Options de compte \" sur la page Internet de Toontown."
NoSecretChatAtAllOK = lOK
NoSecretChatWarningTitle = "Contrôle parental"
NoSecretChatWarning = "Pour discuter avec un ami, la fonction \" amis secrets \" doit être activée. Les enfants doivent demander à leurs parents de s'identifier avec leur mot de passe \" parent \" pour en savoir plus sur la fonction \" amis secrets \" et avoir accès au contrôle parental."
NoSecretChatWarningOK = lOK
NoSecretChatWarningCancel = lCancel
NoSecretChatWarningWrongPassword = "Ce n'est pas le mot de passe correct. Veuillez entrer le mot de passe \" parent \" créé lorsque vous avez acheté ce compte. Ce mot de passe n'est pas celui utilisé pour jouer."

ActivateChat = """La fonction " amis secrets " permet à un membre de discuter avec un autre membre uniquement à l'aide d'un code secret qui doit être communiqué en dehors du jeu. Pour une description complète, cliquez ici : 

La fonction " amis secrets " n'est ni modérée ni surveillée.  Si les parents autorisent leurs enfants à utiliser leur compte avec la fonction " amis secrets " activée, nous les encourageons à surveiller leurs enfants lorsqu'ils jouent. Une fois activée, la fonction " amis secrets " est disponible jusqu'à ce qu'elle soit désactivée.

En activant la fonction " amis secrets ", vous reconnaissez qu'elle comporte des risques inhérents, que vous avez été informés de ceux-ci, et que vous acceptez lesdits risques."""

ActivateChatYes = "Activer"
ActivateChatNo = lCancel
ActivateChatMoreInfo = "Plus d'infos"
ActivateChatPrivacyPolicy = "Politique de confidentialité"

LeaveToPay = """De manière à pouvoir effectuer votre achat, vous allez automatiquement quitter le jeu et être redirigé sur le site Toontown."""
LeaveToPayYes = "Acheter"
LeaveToPayNo = lCancel

LeaveToSetParentPassword = """Afin de définir votre mot de passe " parent ", vous allez automatiquement quitter le jeu et être redirigé(e) sur le siteToontown."""
LeaveToSetParentPasswordYes = "Définir le mot de passe"
LeaveToSetParentPasswordNo = lCancel

LeaveToEnableChatUK = """ Pour activer le Chat le jeu devra quitter le site Toontown."""
LeaveToEnableChatUKYes = "Activer le Chat!"
LeaveToEnableChatUKNo = lCancel

ChatMoreInfoOK = lOK
SecretChatActivated = "La fonction \" amis secrets \" a été activée!\n\nSi vous changez d'avis et décidez de désactiver cette fonction ultérieurement, cliquez sur \" Options de compte \" sur la page Internet de Toontown."
SecretChatActivatedOK = lOK
ProblemActivatingChat = "Désolé! Nous n'avons pas pu activer la fonction de chat \" amis secrets \".n\n%s\n\nRessayez plus tard."
ProblemActivatingChatOK = lOK

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
        "Fais attention aux  " + Cogs + "."
        "On dirait que le tramway arrive!",
        "Je dois jouer à un jeu du tramway pour avoir quelques morceaux de tarte!",
        "Quelquefois, je joue aux jeux du tramway juste pour manger de la tarte aux fruits!",
        "Ouf, je viens d'arrêter un groupe de " + Cogs + ". J'ai besoin de repos!",
        "Aïe, certains de ces " + Cogs + " sont costauds!",
        "On dirait que tu t'amuses.",
        "Oh bon sang, quelle bonne journée.",
        "J'aime bien ce que tu portes.",
        "Je crois bien que je vais aller à la pêche cet après-midi.",
        "Amuse-toi bien dans mon quartier.",
        "J'espère que tu profites bien de ton séjour à Toontown!",
        "J'ai entendu dire qu'il neigeait dans le "+lTheBrrrgh+".",
        "Est-ce que tu as fait un tour de tramway aujourd'hui?",
        "J'aime bien rencontrer des nouveaux.",
        "Aïe, il y a beaucoup de " + Cogs + " dans le "+lTheBrrrgh+".",
        "J'aime bien jouer à chat. Et toi?",
        "Les jeux du tramway sont amusants.",
        "J'aime bien faire rire les gens.",
        "J'adore aider mes amis.",
        "Hum, serais-tu perdu(e)? N'oublie pas que ta carte est dans ton journal de bord.",
        "Essaie de ne pas te noyer dans la paperasserie des " + Cogs + ".",
        "J'ai entendu dire que " + Daisy + " a planté de nouvelles fleurs dans son jardin.",
        "Si tu appuies sur la touche \" page précédente \", tu peux regarder vers le haut!",
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
        "Bienvenue à "+lToontownCentral+".",
        "Salut, je m'appelle ""+Mickey+". Et toi?",
        ],
        [ # Comments
        "Dis donc, as-tu vu "+Donald+"?",
        "Je vais aller regarder le brouillard se lever sur les "+lDonaldsDockNC+".",
        "Si tu vois mon copain "+Goofy+", dis-lui bonjour de ma part.",
        "J'ai entendu dire que "+Daisy+" a planté de nouvelles fleurs dans son jardin.",
        ],
        [ # Goodbyes
        "Je vais au pays musical voir "+Minnie+"!",
        "Aïe, je suis en retard pour mon rendez-vous avec "+Minnie+"!",
        "On dirait que c'est l'heure du dîner pour "+Pluto+".",
        "Je crois que je vais aller nager aux "+lDonaldsDockNC+".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Bienvenue au Pays musical.",
        "Salut, je m'appelle "+Minnie+". Et toi?",
        ],
        [ # Comments
        "Les collines sont animées par les notes de musique!",
        "N'oublie pas d'essayer le grand manège tourne-disques!",
        "Tu as une chouette tenue, %.",
        "Dis donc, as-tu vu "+Mickey+"?",
        "Si tu vois mon ami "+Goofy+", dis-lui bonjour de ma part.",
        "Aïe, il y a beaucoup de "+Cogs+" près du Pays des rêves de "+Donald+".",
        "J'ai entendu dire qu'il y a du brouillard sur les "+lDonaldsDockNC+".",
        "N'oublie pas d'essayer le labyrinthe dans le "+lDaisyGardensNC+".",
        "Je crois bien que je vais aller chercher quelques airs de musique.",
        "Hé %, regarde donc par là-bas.",
        "J'aime bien entendre de la musique.",
        "Je parie que tu ne savais pas que le Pays musical de Minnie est aussi appelé le Haut-Bois? Hi hi!",
        "J'aime bien jouer aux imitations. Et toi?",
        "J'aime bien faire rire les gens.",
        "Oh là là, ça fait mal aux pieds de trotter toute la journée avec des talons!",
        "Belle chemise, %.",
        "Est-ce que c'est un bonbon par terre?",
        ],
        [ # Goodbyes
        "Aïe, je suis en retard pour mon rendez-vous avec %s!" % Mickey,
        "On dirait que c'est l'heure du dîner pour %s." % Pluto,
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Bienvenue au "+lDaisyGardensNC+".",
        "Salut, je m'appelle "+Goofy+". Et toi?",
        "Wof, je suis content de te voir, %!",
        ],
        [ # Comments
        "Bon sang, c'est facile de se perdre dans le labyrinthe!",
        "N'oublie pas d'essayer le labyrinthe tant que tu es ici.",
        "Je n'ai pas vu "+Daisy+" de la journée.",
        "Je me demande où se trouve " + Daisy + ".",
        "Dis donc, as-tu vu "+Donald+"?",
        "Si tu vois mon ami "+Mickey+", dis-lui bonjour de ma part.",
        "Oh! J'ai oublié le petit déjeuner de "+Mickey+"!",
        "Wof, il y a beaucoup de "+Cogs+" près des "+lDonaldsDockNC+".",
        "On dirait que "+Daisy+" a planté de nouvelles fleurs dans son jardin.",
        "À la succursale du Glagla de ma boutique à gags, les lunettes hypnotiques sont en vente pour seulement 1 bonbon!",
        "La boutique à gags de Dingo propose les meilleures blagues, astuces et chatouilles de tout Toontown!",
        "À la boutique à gags de Dingo, chaque tarte à la crème est garantie faire rire ou vos bonbons seront remboursés!"
        ],
        [ # Goodbyes
        "Je vais au Pays musical voir %s!" % Minnie,
        "Aïe, je suis en retard pour mon rendez-vous avec %s!" % Donald,
        "Je crois que je vais aller nager aux "+lDonaldsDockNC+".",
        "C'est l'heure de faire la sieste. Je vais au Pays des rêves.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Bienvenue au Pays des rêves.",
        "Salut, je m'appelle %s. Et toi?" % Donald,
        ],
        [ # Comments
        "Cet endroit me donne quelquefois la chair de poule.",
        "N'oublie pas d'essayer le labyrinthe dans le "+lDaisyGardensNC+".",
        "Oh bon sang, quelle bonne journée.",
        "Dis donc, as-tu vu "+Mickey+"?",
        "Si tu vois mon copain "+Goofy+", dis-lui bonjour de ma part."
        "Je crois bien que je vais aller à la pêche cet après-midi.",
        "Aïe, il y a beaucoup de "+Cogs+" près des "+lDonaldsDockNC+".",
        "Hé dis donc, tu n'as pas encore fait un tour de bateau avec moi aux "+lDonaldsDockNC+"?",
        "Je n'ai pas vu "+Daisy+" de la journée.",
        "J'ai entendu dire que "+Daisy+" a planté de nouvelles fleurs dans son jardin.",
        "Coin coin.",
        ],
        [ # Goodbyes
        "Je vais au Pays musical voir %s!" % Minnie,
        "Aïe, je suis en retard pour mon rendez-vous avec %s!" % Daisy,
        "Je crois que je vais aller nager près de mes quais.",
        "Je crois que je vais aller faire un tour de bateau près de mes quais.",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)


# ToontownClientRepository.py
TCRConnecting = "En cours de connexion..."
# host, port
TCRNoConnectTryAgain = "Impossible de se connecter à %s:%s. Ressayer?"
TCRNoConnectProxyNoPort = "Impossible de se connecter à %s:%s.\n\nVous êtes connecté(e) à Internet par un proxy, mais ce proxy ne permet pas les connexions par le port %s.\n\nVous devez ouvrir ce port ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'ouvrir ce port."
TCRNoDistrictsTryAgain = "Aucun district de Toontown n'est disponible. Ressayer?"
TCRLostConnection = "Votre connexion Internet à Toontown s'est inopinément interrompue."
TCRBootedReasons = {
    1: "Un problème inattendu est survenu. Votre connexion est perdue, mais vous devriez pouvoir vous reconnecter et retourner directement dans le jeu.",
    100: "Vous avez été déconnecté(e) parce que quelqu'un d'autre vient d'ouvrir une session avec votre compte sur un autre ordinateur.",
    120: "Vous avez été déconnecté du fait d'un problème avec votre autorisation d'utilisation du chat \" clavier \".",
    122: "Un problème inattendu est survenu lors de votre connexion à Toontown. Veuillez contacter le service clients de Toontown.",
    125: "Vos fichiers Toontown installés ne sont pas valides. Utilisez le bouton  \" Jouer \" sur le site officiel de Toontown pour lancer Toontown.",
    126: "Vous n'êtes pas autorisé(e) à utiliser les fonctions réservées aux administrateurs.",
    151: "Vous avez été déconnecté(e) par un administrateur travaillant sur les serveurs de Toontown.",
    153: "Le district de Toontown sur lequel vous étiez en train de jouer a été réinitialisé. Toutes les personnes jouant dans ce district ont été déconnectées. Vous devriez toutefois pouvoir vous reconnecter et revenir directement dans le jeu.",
    288: "Désolé, vous avez utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci.",
    349: "Désolé, vous avez utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci.",
    }
TCRBootedReasonUnknownCode = "Un problème inattendu s'est produit (code d'erreur %s). Votre connexion est perdue, mais vous devriez pouvoir vous reconnecter et retourner directement dans le jeu."
TCRTryConnectAgain = "\n\nEssayer de se reconnecter?"
# avName
TCRTutorialAckQuestion = "%s vient d'arriver à Toontown.\n\nEst-ce que tu voudrais que " + Mickey + " te fasse visiter?"
TCRTutorialAckOk = lYes
TCRTutorialAckCancel = lNo
TCRToontownUnavailable = "Toontown est momentanément indisponible, nouvelle tentative..."
TCRToontownUnavailableCancel = lCancel
TCRNameCongratulations = "FÉLICITATIONS!!"
TCRNameAccepted = "Ton nom a été\napprouvé par le Conseil de Toontown.\n\nÀ partir de ce jour\ntu t'appelleras\n\"%s\""
TCRServerConstantsProxyNoPort = "Impossible de contacter %s.\n\nVous êtes connecté à Internet par un proxy, mais ce proxy ne permet pas les connexions par le port %s.\n\nVous devez ouvrir ce port ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'ouvrir ce port."
TCRServerConstantsProxyNoCONNECT = "Impossible de contacter %s.\n\nVous êtes connecté(e) à Internet par un proxy, mais ce proxy ne prend pas en charge la méthode CONNECT.\n\nVous devez activer cette fonction ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'activer cette méthode."
TCRServerConstantsTryAgain = "Impossible de contacter %s.\n\nLe serveur de comptes de Toontown peut être temporairement hors service, ou votre connexion Internet est défaillante.\n\nRessayer?"
TCRServerDateTryAgain = "Impossible de trouver la date du serveur depuis %s. Ressayer?"
AfkForceAcknowledgeMessage = "Ton Toon s'est assoupi et est parti au lit."
PeriodTimerWarning = "Ta limite de temps dans Toontown pour ce mois-ci est presque atteinte!"
PeriodForceAcknowledgeMessage = "Tu as utilisé toutes tes minutes disponibles dans Toontown pour ce mois-ci. Reviens jouer de nouveau le mois prochain!"
TCREnteringToontown = "Accès à Toontown..."

# FriendInvitee.py
FriendInviteeTooManyFriends = "%s voudrait être ton ami(e) mais tu as déjà trop d'amis sur ta liste!"
FriendInviteeInvitation = "%s voudrait être ton ami(e)."
FriendInviteeOK = lOK
FriendInviteeNo = lNo

# FriendInviter.py
FriendInviterOK = lOK
FriendInviterCancel = lCancel
FriendInviterStopBeingFriends = "Arrêter d'être ami(e)."
FriendInviterYes = lYes
FriendInviterNo = lNo
FriendInviterClickToon = "Clique sur le Toon avec lequel tu voudrais devenir ami(e)."
FriendInviterTooMany = "Tu as trop d'amis sur ta liste pour pouvoir en ajouter un de plus maintenant. Tu vas devoir retirer des amis de ta liste si tu veux devenir ami(e) avec %s."
FriendInviterNotYet = "Veux-tu devenir ami(e) avec %s?"
FriendInviterCheckAvailability = "Recherche de la disponibilité de %s."
FriendInviterNotAvailable = "%s est occupé(e) en ce moment, ressaie plus tard."
FriendInviterWentAway = "%s est parti(e)."
FriendInviterAlready = "%s est déjà ton ami(e)."
FriendInviterAskingCog = "Demande à %s d'être ton ami(e)."
FriendInviterEndFriendship = "Es-tu certain de vouloir cesser d'être ami(e) avec %s?"
FriendInviterFriendsNoMore = "%s n'est plus ton ami(e)."
FriendInviterSelf = "Tu es déjà \" ami(e) \" avec toi-même!"
FriendInviterIgnored = "%s t'ignore."
FriendInviterAsking = "Demande à %s d'être ton ami(e)."
FriendInviterFriendSaidYes = "%s a dit oui!"
FriendInviterFriendSaidNo = "%s a dit non, merci."
FriendInviterFriendSaidNoNewFriends = "%s ne cherche pas de nouveaux amis pour l'instant."
FriendInviterTooMany = "%s a déjà trop d'amis!"
FriendInviterMaybe = "%s n'a pas pu répondre."
FriendInviterDown = "Ne peut pas se faire d'amis pour l'instant."

# FriendSecret.py
FriendSecretIntro = "Si tu joues à Toontown en ligne de Disney avec quelqu'un que tu connais réellement, vous pouvez devenir amis secrets. Tu peux communiquer avec tes amis secrets à l'aide du clavier. Les autres Toons ne comprendront pas ce que vous êtes en train de dire.\n\nPour cela, il faut échanger un secret. Dis le secret à ton ami(e), mais à personne d'autre. Lorsque ton ami(e) écrit ton secret sur son écran, vous pourrez être amis secrets dans Toontown!"
FriendSecretGetSecret = "Obtenir un secret"
FriendSecretEnterSecret = "Si quelqu'un t'a donné un secret, écris-le ici."
FriendSecretOK = lOK
FriendSecretCancel = lCancel
FriendSecretGettingSecret = "Recherche du secret... ."
FriendSecretGotSecret = "Voilà ton nouveau secret. N'oublie pas de l'écrire!\n\nTu ne peux donner ce secret qu'à une seule personne. Une fois que quelqu'un aura écrit ton secret, il ne pourra fonctionner pour personne d'autre. Si tu veux donner un secret à plus d'une personne, demande un autre secret.\n\nLe secret ne fonctionnera que dans les deux jours suivants. Ton ami(e) devra l'entrer sur son écran avant la fin de cette période pour qu'il puisse fonctionner.\n\nTon secret est :"
FriendSecretTooMany = "Désolé, tu ne peux plus avoir de secrets aujourd'hui. Tu en as déjà eu assez!n\nEssaie encore demain."
FriendSecretTryingSecret = "Recherche du secret..."
FriendSecretEnteredSecretSuccess = "Tu es maintenant ami(e) secret(e) avec %s!"
FriendSecretEnteredSecretUnknown = "Ce n'est le secret de personne. Es-tu certain(e) de l'avoir épelé correctement?\n\nSi tu l'as épelé correctement, il peut être périmé. Demande un nouveau secret à ton ami(e), ou prends-en un nouveau toi-même et donne-le à ton ami(e)."
FriendSecretEnteredSecretFull = "Tu ne peux pas être ami(e) avec %s parce que l'un(e) de vous a déjà trop d'amis sur sa liste."
FriendSecretEnteredSecretFullNoName = "Vous ne pouvez pas être amis parce que l'un de vous a déjà trop d'amis sur sa liste."
FriendSecretEnteredSecretSelf = "Tu viens juste d'écrire ton propre secret! Maintenant, personne d'autre ne peut plus utiliser ce secret."
FriendSecretNowFriends = "Tu es maintenant ami(e) secret(e) avec %s!"
FriendSecretNowFriendsNoName = "Vous êtes maintenant amis secrets!"

# FriendsListPanel.py
FriendsListPanelNewFriend = "Nouvel(le) ami(e)"
FriendsListPanelSecrets = "Secrets"
FriendsListPanelOnlineFriends = "AMIS\nEN LIGNE"
FriendsListPanelAllFriends = "TOUS\nLES AMIS"
FriendsListPanelIgnoredFriends = "TOONS\nIGNORÉS"

# TeaserPanel.py
TeaserTop = "  Désolé! Tu n’as pas accès à ceci pendant l’essai gratuit.\n\nInscris-toi maintenant et profite de ces super fonctions :"
TeaserOtherHoods = "Visite les 6 quartiers exceptionnels!"
TeaserTypeAName = "Inscris le nom que tu préfères pour ton Toon!"
TeaserSixToons = "Crée jusqu’à 6 Toons par compte!"
TeaserOtherGags = "Additionne 6 niveaux d’habileté\ndans 6 séries de gags différentes!"
TeaserClothing = "Achète des vêtements originaux\npour personnaliser ton Toon!"
TeaserFurniture = "Achète et dispose des meubles dans ta maison!"
TeaserCogHQ = "Infiltre des zones dangereuses sur\nle territoire des Cogs!"
TeaserSecretChat = "Échange des secrets avec tes amis\npour pouvoir discuter en ligne avec eux!"
TeaserCardsAndPosters = "Participez aux compétitions avec les autres joueurs \net devenez l’un des Top Toons! \nVotre nom apparaîtra sur www.toontown.fr"
TeaserHolidays = "Participe à des événements spéciaux et\npassionnants et à des fêtes!"
TeaserQuests = "Relève des centaines de défitoons pour sauver Toontown!"
TeaserEmotions = "Achète des émotions pour rendre ton\nToon plus expressif!"
TeaserMinigames = "Joue aux 8 sortes de mini jeux!"
TeaserSubscribe = "S’inscrire Maintenant"
TeaserContinue = "Continuer l’essai"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Désolé, tu ne peux pas avancer parce que le téléchargement de %(phase)s n'en est qu'à %(percent)s% %.\n\nRéessaie plus tard."

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "Téléchargement de: %s"
DownloadWatcherInitializing = "Initialisation du téléchargement..."

# Launcher.py
LauncherPhaseNames = {
    0   : "Initialisation",
    3   : "Faire un Toon",
    3.5 : "Toontoriel",
    4   : "Terrain de jeux",
    5   : "Rues",
    5.5 : "Domaines",
    6   : "Quartiers I",
    7   : "Bâtiments " + Cog,
    8   : "Quartiers II",
    9   : "Quartiers généraux " + Cog,
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)s (%(current)s sur %(total)s)"
LauncherStartingMessage = "Lancement de Toontown en ligne de Disney... "
LauncherDownloadFile = "Téléchargement des mises à jour: " + LauncherProgress + "..."
LauncherDownloadFileBytes = "Téléchargement des mises à jour: " + LauncherProgress + " : %(bytes)s"
LauncherDownloadFilePercent = "Téléchargement des mises à jour: " + LauncherProgress + " : %(percent)s% %"
LauncherDecompressingFile = "Décompression des mises à jour: " + LauncherProgress + "..."
LauncherDecompressingPercent = "Décompression des mises à jour: " + LauncherProgress + ". : %(percent)s% %"
LauncherExtractingFile = "Extraction des mises à jour: " + LauncherProgress + "..."
LauncherExtractingPercent = "Extraction des mises à jour: " + LauncherProgress + " : %(percent)s% %"
LauncherPatchingFile = "Application des mises à jour: " + LauncherProgress + "..."
LauncherPatchingPercent = "Application des mises à jour: " + LauncherProgress + " : %(percent)s% %"
LauncherConnectProxyAttempt = "En cours de connexion à Toontown: %s (proxy : %s) essai : %s"
LauncherConnectAttempt = "En cours de connexion à Toontown: %s essai %s"
LauncherDownloadServerFileList = "Mise à jour de Toontown..."
LauncherCreatingDownloadDb = "Mise à jour de Toontown..."
LauncherDownloadClientFileList = "Mise à jour de Toontown..."
LauncherFinishedDownloadDb = "Mise à jour de Toontown... "
LauncherStartingToontown = "Lancement de Toontown..."
LauncherRecoverFiles = "Mise à jour de Toontown. Récupération des fichiers..."
LauncherCheckUpdates = "Recherche de mises à jour pour "+ LauncherProgress
LauncherVerifyPhase = "Mise à jour de Toontown..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Faire un\nToon"
AvatarChoicePlayThisToon = "Jouer\navec ce Toon"
AvatarChoiceSubscribersOnly = "S’inscrire\n\n\n\nMaintenant!"
AvatarChoiceDelete = "Supprimer"
AvatarChoiceDeleteConfirm = "Cela va supprimer %s pour toujours."
AvatarChoiceNameRejected = "Nom\nrefusé"
AvatarChoiceNameApproved = "Nom\naccordé!"
AvatarChoiceNameReview = "En cours\nd'examen"
AvatarChoiceNameYourToon = "Donne un nom\nà ton Toon!"
AvatarChoiceDeletePasswordText = "Attention! Cela va supprimer %s pour toujours. Pour supprimer ce Toon, entre ton mot de passe."
AvatarChoiceDeleteConfirmText = "Attention! Cela va supprimer %(name)s pour toujours. Si tu es certain(e) de vouloir faire cela, entre \"%(confirm)s\" et clique sur OK."
AvatarChoiceDeleteConfirmUserTypes = "supprimer"
AvatarChoiceDeletePasswordTitle = "Supprimer le Toon?"
AvatarChoicePassword = "Mot de passe"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "Ce mot de passe ne semble pas correspondre. Pour supprimer ce Toon, entre ton mot de passe."
AvatarChoiceDeleteWrongConfirm = "Tu n'as pas entré le bon mot. Pour supprimer %(name)s, entre \"%(confirm)s\" et clique sur OK. N'entre pas les guillemets. Clique sur Annuler si tu as changé d'avis."

# AvatarChooser.py
AvatarChooserPickAToon = "Choisis un Toon pour jouer"
AvatarChooserQuit = lQuit

# MultiPageTextFrame.py
MultiPageTextFrameNext = lNext
MultiPageTextFramePrev = 'Précédent'
MultiPageTextFramePage = 'Page %s/%s'

# MemberAgreementScreen.py
MemberAgreementScreenTitle = 'Contrat de membre du service'
MemberAgreementScreenAgree = "J'accepte"
MemberAgreementScreenDisagree = 'Je refuse'
MemberAgreementScreenCancel = lCancel
MemberAgreementScreenWelcome = "Bienvenue!"
MemberAgreementScreenOnYourWay = "Vous êtes sur le point de devenir officiellement membre de"
MemberAgreementScreenToontown = "Toontown en ligne de Disney"
MemberAgreementScreenPricing = "Toontown en ligne de Disney coûte             pour\nle premier mois. Chaque mois supplémentaire coûte             .\nEt l'inscription est facile : lisez et remplissez simplement\nle formulaire d'informations ci-dessous et c'est parti!"
MemberAgreementScreenCCUpFrontPricing = "Inscrivez-vous maintenant pour votre essai GRATUIT de? jours. Vous pouvez annuler à tout moment\npendant votre période d'essai gratuit sans aucune obligation. À la fin de\nvotre période d'essai gratuit, le premier mois\nvous sera automatiquement facturé et ensuite chaque mois supplémentaire."
MemberAgreementScreenGetParents = "Vous devez avoir 18 ans ou plus pour acheter un abonnement à Toontown en ligne de Disney. Demandez de l'aide à un parent ou tuteur."
MemberAgreementScreenGetParentsUnconditional = "Vous devez avoir 18 ans ou plus pour acheter un abonnement à Toontown en ligne de Disney. Si vous avez moins de 18 ans, demandez de l'aide à un parent ou tuteur."
MemberAgreementScreenMustBeOlder = "Vous devez avoir 18 ans ou plus pour acheter un abonnement à Toontown en ligne de Disney. Demandez de l'aide à un parent ou tuteur."
MemberAgreementScreenYouMustAgree = "Pour acheter un abonnement à Toontown en ligne de Disney, vous devez accepter le contrat de membre du service."
MemberAgreementScreenYouMustAgreeOk = lOK
MemberAgreementScreenYouMustAgreeQuit = lQuit
MemberAgreementScreenAgreementTitle = "Contrat de membre du service "
MemberAgreementScreenClickNext = "Cliquez sur \""+lNext+"\" pour avancer d'une page."
# this is useful for tweaking the member agreement:
#import LocalizerEnglish; import Localizer
#reload(LocalizerEnglish);reload(Localizer);page=toonbase.tcr.memberAgreementScreen.memAgreement.getCurPage();toonbase.tcr.loginFSM.request('freeTimeInform');toonbase.tcr.loginFSM.request('memberAgreement');toonbase.tcr.memberAgreementScreen.memAgreement.setPage(page)
MemberAgreementScreenLegalText = [
"""





""" # spacing for graphics; start next section on a new line (i.e. """\nText)
"""
CONTRAT DE MEMBRE DU SERVICE TOONTOWN EN LIGNE DE DISNEY

Bienvenue sur Toontown en ligne de Disney (ci-après désigné comme le " Service "). Veuillez LIRE ATTENTIVEMENT CE CONTRAT DE MEMBRE (ci-après désigné comme le " CONTRAT ") AVANT D'UTILISER CE SERVICE. Ce Service est détenu et géré par Disney Online (ci-après désigné comme " Disney ", " nous " ou " notre société ").
""","""
Par le simple fait d'utiliser ce Service, vous acceptez ces conditions, les Conditions d'Utilisation et les Conditions Générales Disney affichées sur notre site Web. Si vous ne les acceptez pas, il est préférable que vous n'utilisiez pas ce Service. Veuillez noter que, dans ce Contrat, vous pouvez parfois être désigné comme " Membre ". De la même manière, la personne qui s'abonne initialement au Service peut être désignée comme " Compte Parent ". Par " Compte ", on entend le compte de tout Membre ouvert conformément aux modalités d'inscription au Service. Les conditions du présent Contrat s'appliquent à tous les Membres, qu'ils soient ou non Compte Parent. Le Compte Parent est tenu de porter les termes du présent Contrat à la connaissance de chacun des membres de sa famille (ainsi que de toute autre personne qu'il autorise à jouer en utilisant son Compte) et d'en assurer le respect par ces derniers. Le Compte Parent d'un Compte est entièrement responsable de toutes les activités effectuées par l'intermédiaire dudit Compte.
""","""
Nous nous réservons le droit, à tout moment et à notre entière discrétion, de changer, modifier, d'ajouter ou ôter des parties de ce Contrat. Les changements apportés à ce Contrat seront publiés sur le Service ou vous seront adressés par courrier électronique ou postal.

Si tout changement à venir dans ce Contrat vous semble inacceptable ou fait que vous ne respectez plus les termes dudit Contrat, vous pouvez résilier votre Compte. Le simple fait de continuer à utiliser le Service après la notification des changements apportés à ce Contrat (y compris les Conditions d'Utilisation et les Conditions Générales Disney) vaut acceptation desdits changements.
""","""
Nous sommes susceptibles de modifier, changer, suspendre ou d'interrompre tout aspect de ce Service à tout moment, y compris, sans que la liste soit limitative, la disponibilité de toute fonction de ce Service, l'équipement requis pour y accéder, la base de données ou le contenu, ou encore les heures de disponibilité. Nous nous réservons également le droit d'imposer des limites à certaines fonctions ou de restreindre l'accès à certaines parties du Service ou à tout le Service pendant de longues périodes, sans aucun préavis ni aucune responsabilité.

Chaque Membre est tenu de fournir l'équipement téléphonique et autre nécessaire pour accéder au Service, y compris, sans que la liste soit limitative, les modems et logiciels d'accès à Internet, et il en est seul responsable.
""","""
RESTRICTIONS SUR L'UTILISATION DES DOCUMENTS

Tous les documents publiés par Disney, y compris, sans que la liste soit limitative, les sources d'information, photographies, images, illustrations, clips audio et vidéo (désignés collectivement comme " Contenu ") sont protégés par copyright et détenus et contrôlés par Disney, sa société mère, ses filiales ou un fournisseur tiers. Vous êtes tenu de vous conformer à toutes les mentions de copyright, informations ou restrictions figurant dans tout Contenu auquel vous accédez par le biais du Service.
""","""
Ce Service est protégé par copyright en tant qu'œuvre collective et/ou compilation selon la législation américaine sur les droits d'auteur, les conventions internationales et d'autres lois sur le copyright. Aucun des documents provenant de ce Service ou d'un site Web détenu, géré, concédé ou contrôlé par Disney, ne peut être copié, reproduit, republié, téléchargé, affiché ou transmis et aucune œuvre dérivée ne peut être créée ou distribuée d'aucune manière que ce soit, sauf dans les conditions suivantes : il vous est possible de télécharger une copie des documents sur un micro-ordinateur pour votre utilisation personnelle et à des fins non commerciales, pourvu que vous conserviez intacts les copyrights et autres mentions de propriété. L'utilisation du Contenu dans un autre but constitue une infraction au copyright de Disney et à ses autres droits de propriété. Dans le cadre de l'application de ce Contrat, il vous est interdit d'utiliser tout élément de notre Contenu sur un autre site Web ou dans un environnement informatique en réseau. Vous n'êtes pas autorisé à vendre ni à mettre aux enchères des personnages ou articles Disney, ni des documents protégés par copyright.   
""","""
Si vous décidez de procéder au téléchargement à partir de ce Service, le logiciel, y compris les fichiers, les images qui y sont intégrées ou qui sont créées par lui, ainsi que les données qui l'accompagnent (tous ces éléments étant collectivement dénommés comme " Logiciel ") vous sont concédés par Disney. Par les présentes, nous vous concédons une licence d'utilisation du Logiciel non exclusive, uniquement dans le cadre de ce Service par le biais d'un Compte autorisé et intégralement payé (ou d'un essai gratuit autorisé). Le Compte Parent reconnaît, autorise et s'engage à respecter : (a) qu'aucun des documents, de quelque nature que ce soit, soumis via le Compte Parent ne pourra (i) enfreindre, plagier ou annexer les droits d'un tiers, y compris les copyrights, marques, données confidentielles ou d'autres droits individuels ou droits de propriété ; (ii) ni contenir des documents diffamatoires ou illégaux ; (b) que les données bancaires fournies à Disney sont valides, que le Compte Parent est autorisé à les utiliser et que le Compte Parent est âgé de 18 ans au moins ; (c) que Disney est autorisé à effectuer des prélèvements sur le compte bancaire dont les coordonnées lui ont été fournies, ainsi qu'il est stipulé dans la partie " Prix et paiement " ci-dessous ; et (d) que le Compte Parent et tous ses Membres respecteront toutes les dispositions du présent Contrat.  
""","""
Par les présentes, vous, le Compte Parent, vous engagez à protéger, défendre et dégager Disney, sa société mère et ses filiales, ainsi que tous les directeurs, responsables, propriétaires, agents, fournisseurs d'informations, affiliés, concédants et détenteurs de licences (collectivement dénommés les " Parties Indemnisées ") de toute responsabilité et de tous frais encourus par les Parties Indemnisées en raison de toute action résultant d'une rupture du contrat par vous ou tout autre Membre sur votre Compte. Disney ne peut être tenu pour responsable de l'exactitude ou de la fiabilité des déclarations, opinions, conseils ou autres informations, quels qu'ils soient, publiés, téléchargés ou distribués via le Service par un Membre, un fournisseur d'informations ou toute autre personne ou entité. Vous reconnaissez que la prise en considération de ces conseils, opinions, déclarations, notes ou informations se fera entièrement à vos propres risques. Disney se réserve le droit, à sa seule discrétion, de corriger toute erreur ou omission dans toute partie du Service.
""","""
DÉCHARGE

LES DOCUMENTS DE CE SERVICE SONT FOURNIS " EN L'ÉTAT " ET SANS AUCUNE GARANTIE, EXPRESSE OU TACITE. DANS TOUTE LA MESURE AUTORISÉE PAR LA LÉGISLATION APPLICABLE, DISNEY DÉCLINE TOUTES GARANTIES, EXPRESSES OU TACITES, Y COMPRIS, MAIS SANS QUE CETTE ÉNUMÉRATION SOIT LIMITATIVE, LES GARANTIES TACITES DE COMMERCIALISATION ET D'APTITUDE À UN BUT DÉTERMINÉ. DISNEY NE GARANTIT PAS QUE LES FONCTIONS CONTENUES DANS CE SERVICE SERONT ASSURÉES SANS INTERRUPTION ET SANS ERREUR, QUE LES DÉFAUTS SERONT CORRIGÉS, NI QUE CE SITE OU LE SERVEUR QUI LE MET À DISPOSITION EST EXEMPT DE VIRUS ET AUTRES COMPOSANTS DANGEREUX. DISNEY NE PREND AUCUN ENGAGEMENT ET NE PROMET AUCUNE GARANTIE EN CE QUI CONCERNE L'UTILISATION DES DOCUMENTS DE CE SERVICE NI LES RÉSULTATS DE CETTE UTILISATION, EN TERMES D'EXACTITUDE, DE PRÉCISION, DE FIABILITÉ, ETC.  
""","""
LE COÛT INTÉGRAL DES PRESTATIONS NÉCESSAIRES, DE LA RÉPARATION OU DE LA CORRECTION VOUS INCOMBE ENTIÈREMENT (ET NON À DISNEY). IL EST POSSIBLE QUE LA LÉGISLATION APPLICABLE NE PERMETTE PAS L'EXCLUSION DES GARANTIES TACITES ; IL EST DONC POSSIBLE QUE LES EXCLUSIONS CI-DESSUS NE VOUS SOIENT PAS APPLICABLES.  

SANS PRÉJUDICE DE CE QUI PRÉCÈDE, VOUS RECONNAISSEZ QUE, POUR RENDRE SERVICE AUX UTILISATEURS DE CE SERVICE DISNEY, DISNEY INCLUT DES LIENS VERS D'AUTRES SITES WEB SUR LA PORTION WORLD WIDE WEB DU RÉSEAU INTERNET ET QUE DISNEY N'EXERCE AUCUN CONTRÔLE D'AUCUNE SORTE SUR LE CONTENU OU L'ADÉQUATION DU CONTENU DE CES SITES WEB ET NE PREND AUCUN ENGAGEMENT QUEL QU'IL SOIT À CET ÉGARD. PAR LES PRÉSENTES, VOUS RENONCEZ IRRÉVOCABLEMENT À EXERCER TOUTE ACTION CONTRE DISNEY EN LIEN AVEC CES SITES WEB.   
""","""
En outre, Disney décline explicitement toute responsabilité quant à l'exactitude, le contenu et la disponibilité des informations trouvées sur les sites de tiers, non partenaires de Disney, ayant des liens vers Toontown en ligne de Disney ou depuis ce Service. Disney vous recommande la discrétion quand vous naviguez sur Internet en utilisant son Service ou celui d'un tiers. Comme certains sites utilisent des résultats de recherche automatisés ou vous relient à des sites contenant des informations qui peuvent sembler inappropriées ou choquantes, Disney ne peut être tenu pour responsable de l'exactitude, la légalité ou la décence des informations contenues dans les sites tiers, ni du respect des copyrights par ces sites. Par les présentes, vous renoncez irrévocablement à exercer toute action contre Disney en lien avec ces sites. Disney ne peut vous garantir que vous serez satisfait des produits ou services que vous achetez à des tiers disposant de liens vers ou depuis Toontown en ligne de Disney, étant donné que les autres circuits commerciaux sont détenus et gérés par des commerçants indépendants.   
""","""
Disney ne recommande aucun des articles, et n'a pas pris de mesures en vue de confirmer l'exactitude ou la fiabilité des informations contenues dans lesdits sites tiers. Disney ne fait aucune observation ni ne garantit la sécurité des informations, notamment, de façon non limitative, les cartes de crédit ou toute autre information personnelle que vous pourriez être amené à fournir à des tierces parties et par la présente se dégage de toute responsabilité concernant lesdits sites tiers. Nous vous encourageons fortement à procéder à toute recherche que vous pourriez trouver nécessaire ou adéquate avant de traiter avec lesdites tierces parties que ce soit pour des transactions en ligne ou hors-ligne.
""","""
LIMITATION DE RESPONSABILITÉ

EN AUCUNE CIRCONSTANCE, Y COMPRIS, SANS QUE CETTE PRÉCISION SOIT LIMITATIVE, LA NÉGLIGENCE, DISNEY NE POURRA ÊTRE TENU POUR RESPONSABLE DES DOMMAGES SPÉCIAUX OU INDIRECTS RÉSULTANT DE L'UTILISATION DES DOCUMENTS DE CE SERVICE OU DE TOUT AUTRE SITE (OU DE L'IMPOSSIBILITÉ DE LES UTILISER), MÊME SI DISNEY OU UN REPRÉSENTANT AUTORISÉ DE CETTE SOCIÉTÉ AVAIT ÉTÉ AVERTI DE LA POSSIBILITÉ DE TELS DOMMAGES. LA LÉGISLATION APPLICABLE PEUT INTERDIRE LA LIMITATION OU L'EXCLUSION DE RESPONSABILITÉ POUR LES DOMMAGES INDIRECTS OU SUBSÉQUENTS. IL EST DONC POSSIBLE QUE LES LIMITATIONS ET EXCLUSIONS SUSMENTIONNÉES NE VOUS SOIENT PAS APPLICABLES. EN AUCUN CAS, LA RESPONSABILITÉ FINANCIÈRE TOTALE DE DISNEY VIS-À-VIS DE VOUS, POUR LA TOTALITÉ DES DOMMAGES, PERTES ET CAUSES D'ACTION (CONTRACTUELLE, DÉLICTUELLE OU AUTRE, Y COMPRIS, MAIS SANS QUE CETTE PRÉCISION SOIT LIMITATIVE, LA NÉGLIGENCE) NE SAURAIT EXCÉDER LE PRIX PAYÉ PAR VOUS, LE CAS ÉCHÉANT, POUR AVOIR ACCÈS AU SERVICE.  
""","""
SÉCURITÉ

Dans le cadre de la procédure d'inscription, les Membres doivent choisir un mot de passe, un mot de passe parent et un nom de Membre (ci-après désigné comme " Nom de Membre "). Vous êtes tenu de fournir à Disney des informations exactes, complètes et mises à jour sur votre Compte. Le non-respect de cette disposition constitue une rupture du Contrat, qui peut entraîner la résiliation immédiate de votre Compte. Vous n'êtes pas autorisé à (i) choisir ou utiliser le Nom de Membre d'une autre personne avec l'intention d'usurper l'identité de ladite personne ; (ii) utiliser sans autorisation un nom sur lequel une autre personne a des droits ; ou (iii) utiliser un Nom de Membre que Disney juge, à sa seule discrétion, inapproprié ou choquant.
""","""
Vous vous engagez à avertir Disney, par l'envoi d'un e-mail à toontown@disneyonline.com, de toute utilisation interdite, connue ou soupçonnée, de votre Compte, quelle qu'elle soit, ou de toute infraction à la sécurité connue ou soupçonnée, y compris la perte, le vol ou la communication sans votre accord de votre mot de passe ou de votre mot de passe parent. Vous êtes tenu de protéger la confidentialité de votre mot de passe et de votre mot de passe parent.

Tout Compte Parent doit être âgé de 18 ans au moins pour ouvrir un Compte. Si Disney apprend qu'un Compte Parent a moins de 18 ans, Disney se réserve le droit d'annuler le Compte.

Toute activité frauduleuse, abusive ou illégale peut constituer un motif de résiliation de votre Compte, à la seule discrétion de Disney, et pourra être signalée aux autorités judiciaires compétentes.
""","""
PRIX ET PAIEMENT

Disney se réserve le droit à tout moment de faire payer des montants supplémentaires pour l'accès au Service. Disney se réserve le droit de changer le montant, ou la base de calcul, de tout montant ou de toute charge pour le Service, et de mettre en place de nouveaux montants ou charges effectifs après avertissement préalable des Membres. Disney se réserve le droit de permettre l'accès au Service gratuitement pour raisons promotionnelles ou autres (telles qu'un essai gratuit). 

Chaque Compte Parent accepte de payer tous les frais applicables audit Compte, y compris les taxes, conformément aux conditions de facturation en vigueur au moment où le prix et les frais deviennent exigibles. Les Comptes Parents sont tenus de fournir à Disney un numéro de carte bancaire valide au moment de la procédure d'inscription.
""","""
Disney effectue le prélèvement sur le compte bancaire du Compte Parent à la date où le Compte Parent s'abonne au Service. Ensuite, Disney renouvellera automatiquement le Compte Parent et effectuera un prélèvement sur ledit Compte Parent comme suit :

-Pour les abonnements mensuels, chaque mois pour le Service du mois suivant

-Tous les trois (3) mois à compter de la date anniversaire de la première date de facturation pour les inscriptions trimestrielles.

-Tous les six (6) mois à compter de la date anniversaire de la première date de facturation pour les inscriptions semestrielles.

-Tous les ans à compter de la date anniversaire de la première date de facturation pour les inscriptions annuelles.
""","""
Les charges de renouvellement seront égales ou inférieures au prix initial de l'inscription, sauf avertissement préalable par Disney. Vous pouvez à tout moment informer Disney de votre souhait d'annuler votre abonnement. Disney s'engage à résilier votre Compte sur réception d'une notification provenant du Compte parent, comme indiqué ci-dessous. 

Pour les inscriptions mensuelles : Si la notification d'annulation est reçue dans les 15 premiers jours suivant le premier jour de la facturation initiale, vous serez habilité à recevoir un remboursement de toutes les charges d'inscription au Service, mais serez tenu de régler toute autre charge qui s'ensuivrait. Si vous annulez l'inscription au Service plus de 15 jours après la facturation initiale, votre Compte sera annulé à la fin de la période de facturation en cours et aucun remboursement pour la période inutilisée ne sera consenti.
""","""
Pour les inscriptions trimestrielles : Si la notification d'annulation est reçue dans les 30 premiers jours suivant le premier jour de la facturation initiale, vous serez habilité à recevoir un remboursement de toutes les charges d'inscription au Service, mais serez tenu de régler toute autre charge qui s'ensuivrait. Si vous annulez l'inscription au Service plus de 30 jours après la facturation initiale, aucun remboursement pour la période inutilisée ne sera consenti.

Pour les inscriptions semestrielles : Si la notification d'annulation est reçue dans les 30 premiers jours suivant le premier jour de la facturation initiale, vous serez habilité à recevoir un remboursement de toutes les charges d'inscription au Service, mais serez tenu de régler toute autre charge qui s'ensuivrait. Si vous annulez l'inscription au Service plus de 30 jours après la facturation initiale, aucun remboursement pour la période inutilisée ne sera consenti.
""","""
Pour les inscriptions annuelles : Si la notification d'annulation est reçue dans les 30 premiers jours suivant le premier jour de la facturation initiale, vous serez habilité à recevoir un remboursement de toutes les charges d'inscription au Service, mais serez tenu de régler toute autre charge qui s'ensuivrait. Si vous annulez l'inscription au Service plus de 30 jours après la facturation initiale, aucun remboursement pour la période inutilisée ne sera consenti. 

Votre droit d'utiliser le Service est soumis à toute restriction établie par Disney ou par votre fournisseur de carte bancaire. Si le paiement ne peut pas être débité sur vote carte bancaire ou si le débit revient impayé à Disney pour quelque raison que ce soit, y compris les rejets de débits, Disney se réserve le droit de résilier votre accès et votre Compte, mettant fin par là à l'Accord et à toutes les obligations de Disney ici énumérées.
""","""
Si vous êtes redevable de sommes sur un Compte Disney, quel qu'il soit, vous acceptez que Disney puisse prélever ces sommes non réglées sur votre compte bancaire. Disney se réserve le droit de fixer une limite de crédit (le " Plafond ") pour chaque Membre. Si un Compte de Membre atteint le Plafond, Disney pourra immédiatement prélever sur la carte bancaire de ce Membre toutes les sommes encore exigibles sur son compte. Sauf avis contraire, le Plafond pour chaque Membre est fixé à 100 $.

Si vous avez des raisons de croire que votre Compte n'est plus sécurisé (par exemple, dans le cas de perte, vol, divulgation non autorisée ou utilisation de votre Nom d'utilisateur, Mot de passe ou numéro de carte de crédit, débit ou autre enregistré sur le Service), vous devez rapidement changer de Mot de passe et avertir Disney du problème (par notification décrite à la section Notice ci-dessous) afin d'éviter toute responsabilité possible concernant des charges imputées à votre Compte. 
""",""" 
ACCORD PARENTAL

Conformément au Children's Online Privacy Protection Act (" COPPA "), l'accord parental est exigé pour le recueil, l'utilisation et/ou la communication d'informations à caractère personnel en ligne, lorsque celles-ci ont été obtenues auprès d'un enfant de moins de 13 ans. Dans le cadre de la procédure d'inscription au Service, le Compte Parent sera invité à fournir un numéro de carte bancaire valide. Les parents et représentants légaux pourront créer jusqu'à 6 Toons (un Toon est un personnage que vous créez et que vous utilisez pour jouer sur le Service) sur le Compte Parent. Il faut donc qu'un des parents ou le représentant légal de l'enfant soit titulaire d'un Compte Parent pour que l'enfant puisse ensuite créer son propre Toon à l'intérieur de ce Compte Parent.
""","""
En donnant son numéro de carte bancaire, le titulaire du Compte Parent : (a) déclare et garantit qu'il est le parent ou le représentant légal de tous les enfants de moins de 13 ans autorisés à utiliser son Compte Parent ; et (b) accepte que nous puissions recueillir, utiliser et communiquer, conformément à notre charte sur le Respect de la vie privée, les informations à caractère personnel sur les enfants de moins de 13 ans autorisés à utiliser le Compte Parent par le titulaire de ce Compte Parent.

Le Service inclut une fonction interactive intitulée " Amis secrets ". Le Compte Parent a la possibilité de désactiver cette fonction Amis secrets une fois qu'il est dans le Service. Amis secrets permet à chaque membre de bavarder avec un autre membre, uniquement au moyen d'un code secret qui doit être communiqué en dehors du jeu. Amis secrets n'est ni animé ni supervisé.  
""","""
Si le Compte Parent autorise un enfant à utiliser son compte avec la fonction Amis secrets activée, nous invitons les parents à surveiller leur(s) enfant(s) pendant qu'il(s) utilise(nt) le Service. Le Compte Parent reconnaît que l'activation de la fonction Amis secrets entraîne certains risques inhérents à la fonction elle-même, qu'il a été averti desdits risques et qu'il les accepte. Vous aurez la possibilité d'obtenir davantage d'informations sur la fonction Secret Friends et de l'activer une fois que vous serez à l'intérieur du Service.
""","""
AVIS 

Le Compte Parent est tenu de soumettre et de conserver une adresse e-mail exacte et d'autres informations sur son Compte. Nous pouvons adresser des avis au Compte Parent par avertissement général publié sur le Service, par courrier électronique envoyé à l'adresse figurant dans nos informations sur le Compte ou par courrier affranchi au tarif normal et envoyé à l'adresse figurant dans nos informations sur le Compte. Vous pouvez aussi adresser des avis à Disney. Ces avis seront supposés avoir été donnés lorsqu'ils auront été reçus par Disney par e-mail sur toontown@disneyonline.com.
""","""
NON CESSIBILITÉ DE LA QUALITÉ DE MEMBRE

Disney vous accorde une licence personnelle, non exclusive, non cessible et non transférable vous permettant d'utiliser et d'afficher le Logiciel Disney sur la machine ou toutes les machines dont vous êtes le principal utilisateur. Les copies non autorisées du Logiciel ou la reproduction du Logiciel, de quelque manière que ce soit, y compris par modification, fusion ou intégration à un autre logiciel, ainsi que des documents imprimés liés au Logiciel sont expressément interdites. Vous vous engagez à ne pas sous-licencier, transférer, vendre ou céder cette licence ou le Logiciel. Toute tentative visant à sous-licencier, transférer, vendre ou céder la licence sera nulle et non avenue.
""","""
JURIDICTION

Ce Service est contrôlé et géré par Disney à partir de ses bureaux de L'État de Californie (États-Unis). Disney ne garantit pas que les documents du Service sont appropriés ou disponibles pour une utilisation dans d'autres régions. Toute personne qui choisit d'accéder au Service à partir d'une autre région le fait de sa propre initiative et sera, le cas échéant, responsable du respect de la législation locale. Le Logiciel de ce Service est donc soumis aux contrôles d'exportation des États-Unis. Aucun Logiciel de ce Service ne peut être téléchargé ni autrement exporté ou réexporté (i) dans les pays suivants (ni à un ressortissant ou un résident de ces pays) : Cuba, Irak, Libye, Corée du Nord, Iran, Syrie ni aucun autre pays sur les marchandises duquel les États-Unis ont pris une décision d'embargo ; ni (ii) à quiconque dont le nom est porté sur la liste du Département de trésorerie des États-Unis (Specially Designated Nationals) ou sur la Table of Deny Orders du Département du Commerce des États-Unis. 
""","""
En téléchargeant ou en utilisant le Logiciel, vous certifiez et vous garantissez que vous n'habitez pas dans un des pays susmentionnés, que vous ne vous trouvez pas sous son contrôle, que vous n'êtes ni un ressortissant ni un résident d'aucune de ces régions, et que vous ne faites pas partie de l'une de ces listes. Certains logiciels que les Membres installent depuis un CD-Rom ou téléchargent pour les utiliser sont classés " Restricted Computer Software ". L'utilisation, la reproduction ou la communication par le Gouvernement des États-Unis sont soumises aux restrictions définies dans ce Contrat et stipulées dans les DFARS 227.7202-1(a) et 227.7202-3(a) (1995), DFARS 252.227-7013 (octobre 1988), FAR 12.212(a) (1995), FAR 52.227-19, ou FAR 52.227-14, le cas échéant.
""","""
RÉSILIATION DU SERVICE

Ce Contrat demeure en vigueur jusqu'à sa résiliation par l'une des parties. Vous pouvez résilier ce Contrat et votre droit d'utiliser le Service à tout moment, en adressant un e-mail à toontown@disneyonline.com. Disney peut résilier votre Compte ou vos droits d'accès à ce Service immédiatement, sans avis préalable, si Disney juge, à sa seule discrétion, que vous ne respectez pas l'une des dispositions ou conditions de ce Contrat (y compris les Règles d'Utilisation et les Conditions Générales Disney). Lors de la résiliation, vous serez tenu de détruire tous les documents obtenus avec ce Service et toutes les copies de ces documents, qu'elles étaient faites selon les termes du Contrat ou autrement.
""","""
AUTRES

Cet accord sera régi et interprété conformément avec les lois de l'État de Californie, sans considération de quelque règle relative aux éventuels conflits de loi. Dans le cas où une disposition de ce contrat serait illégale, nulle ou inapplicable pour quelque raison que ce soit, elle serait considérée comme ne faisant pas partie de ce contrat et n'affecterait ni la validité ni l'application des autres dispositions. La présente constitue l'Accord complet existant entre les parties sur l'objet qui y est indiqué, il ne pourra être modifié que par un écrit conforme aux indications ci-dessous.
""","""
TOTALITÉ DE L'ACCORD

Cet Accord constitue la totalité du contrat entre les parties en ce qui touche les questions visées par les présentes ; il annule et remplace tout accord, proposition ou communication précédent ou contemporain, oral ou écrit, entre les représentants de Disney et vous. Disney peut rectifier ou modifier cet Accord ou imposer de nouvelles conditions à tout moment sur avertissement par Disney, qui vous sera communiqué de la manière décrite dans la Section intitulée " Notice " ci-dessus. Toute utilisation par vous du Service après un tel avertissement implique l'acceptation par le Membre de ces rectifications, modifications ou nouvelles conditions.

DERNIÈRE MISE À JOUR
10/18/2002
"""
]

# BillingScreen.py
BillingScreenCCTypeInitialText = 'Choisissez'
BillingScreenCreditCardTypes = ['Visa', 'American Express', 'MasterCard']
BillingScreenTitle = "Veuillez indiquer vos informations de facturation"
BillingScreenAccountName = "Nom du compte"
BillingScreenEmail = "Adresse électronique de facturation/du parent"
BillingScreenEmailConfirm = "Confirmez votre adresse électronique"
BillingScreenCreditCardType = "Type de carte de crédit"
BillingScreenCreditCardNumber = "Numéro de carte de crédit"
BillingScreenCreditCardExpires = "Date d'expiration"
BillingScreenCreditCardName = "Nom tel qu'il est indiqué sur la carte de crédit"
#BillingScreenAgreementText = """*Par le simple fait de communiquer mon numéro de carte bancaire et de cliquer sur " Acheter ", je vous autorise, conformément à mon Contrat de Membre, (1) à effectuer des prélèvements sur ma carte bancaire et (2) à recueillir, utiliser et communiquer les informations à caractère personnel sur mon/mes enfant(s) conformément à la charte sur le Respect de la vie privée."""
BillingScreenAgreementText = """Par le simple fait de cliquer sur " Acheter ", j'autorise mon/mes enfant(s) à utiliser les fonctions interactives autorisées par le Mot de Passe Parent que je créerai sur l'écran suivant, conformément à la charte sur le Respect de la vie privée."""
BillingScreenBillingAddress = "Adresse de facturation : Rue 1"
BillingScreenBillingAddress2 = "Rue 2 (si applicable)"
BillingScreenCity = "Ville"
BillingScreenCountry = "Pays"
BillingScreenState = "Département"
BillingScreenZipCode = "Code postal"
BillingScreenCAProvince = "Province ou territoire"
BillingScreenProvince = "Province (si applicable)"
BillingScreenPostalCode = "Code postal"
BillingScreenPricing = ('              pour le premier mois, puis'
                        '              par mois')
BillingScreenSubmit = "Acheter"
BillingScreenCancel = lCancel
BillingScreenConfirmCancel = "Annuler l'achat?"
BillingScreenConfirmCancelYes = lYes
BillingScreenConfirmCancelNo = lNo
BillingScreenPleaseWait = "Veuillez patienter..."
BillingScreenConnectionErrorSuffix = ".\nRessayez plus tard."
BillingScreenEnterEmail = "Indiquez votre adresse électronique."
BillingScreenEnterEmailConfirm = "Confirmez votre adresse électronique."
BillingScreenEnterValidEmail = "Entrez une adresse électronique valide."
BillingScreenEmailMismatch = "Les adresses électroniques indiquées ne correspondent pas. Ressayez."
BillingScreenEnterAddress = "Entrez votre adresse de facturation complète."
BillingScreenEnterValidState = "Entrez l'abréviation en deux lettres du nom de votre État."
BillingScreenChooseCreditCardType = "Choisissez un type de carte de crédit."
BillingScreenEnterCreditCardNumber = "Entrez votre numéro de carte de crédit."
BillingScreenEnterValidCreditCardNumber = "Vérifiez votre numéro de carte de crédit."
BillingScreenEnterValidSpecificCreditCardNumber = "Entrez un numéro de carte de crédit %s valide."
BillingScreenEnterValidCreditCardExpDate = "Entrez une date d'expiration de carte de crédit valide."
BillingScreenEnterNameOnCard = "Entrez votre nom tel qu'il apparaît sur votre carte de crédit."
BillingScreenCreditCardProblem = "Une erreur est survenue lors du traitement de votre carte de crédit."
BillingScreenTryAnotherCC = "Voulez-vous essayer une autre carte?"
# Fill in %s with phone number from account server
BillingScreenCustomerServiceHelp = "\n\nSi vous avez besoin d'aide, vous pouvez appeler le service clients au %s."
BillingScreenCCProbQuit = lQuit
BillingScreenWhySafe = "Sécurité de la carte de crédit"
BillingScreenWhySafeTitle = "Sécurité de la carte de crédit"
BillingScreenWhySafeCreditCardGuarantee = "GARANTIE DE LA CARTE DE CRÉDIT"
BillingScreenWhySafeJoin = "DEVENIR MEMBRE"
BillingScreenWhySafeToontown = "TOONTOWN EN LIGNE DE DISNEY"
BillingScreenWhySafeToday = "DÈS AUJOURD'HUI!"
BillingScreenWhySafeClose = lClose
BillingScreenWhySafeText = [
"""




Nous utilisons la technologie SSL (Secure Sockets Layer) qui chiffre vos informations de carte de crédit, préservant leur confidentialité et leur protection. Cette technologie sécurise l'entrée et la transmission de vos informations de carte de crédit sur Internet.
Cette technologie de sécurisation protège vos communications Internet avec : 

     Authentification du serveur (mise en échec des imposteurs)
     Confidentialité grâce au chiffrement (mise en échec des indiscrétions)
     Intégrité des données (mise en échec du vandalisme)

Afin de vous offrir un niveau de sécurité complémentaire, les numéros de carte de crédit sont stockés sur un ordinateur qui n'est pas connecté à Internet. Après que vous l'ayez inscrit, votre numéro de carte de crédit complet est transféré sur cet ordinateur sécurisé par l'intermédiaire d'une interface de technologie exclusive. Votre numéro de carte de crédit n'est conservé nulle part ailleurs.



Ainsi, vos informations de carte de crédit sont plus qu'en sûreté avec Toontown en ligne de Disney -- nous pouvons le garantir!
Nous couvrons toute inscription à Toontown en ligne de Disney avec notre garantie de carte de crédit. Si, bien que vous n'en soyez pas responsable, des débits non autorisés apparaissent sur votre relevé bancaire résultant directement de votre communication d'informations de carte de crédit à Toontown en ligne de Disney, nous couvrirons le montant pour lequel votre banque vous tient responsable, jusqu'à un maximum de 50 $.

Si vous suspectez un problème, suivez les procédures normales de signalement telles qu'elles sont définies par votre fournisseur de carte bancaire et contactez-nous également immédiatement. La plupart des organismes de cartes bancaires couvrent toutes les charges résultant d'un usage non autorisé, mais elles peuvent légalement vous tenir responsable pour des montants allant jusqu'à 50 $. Nous couvrirons ce montant non couvert par votre organisme de carte bancaire. 
Qu'est-ce que tout cela signifie? Cela signifie que vous pouvez avoir confiance dans la sécurité et le support relatifs à votre inscription à Toontown en ligne de Disney.

Alors, qu'attendez-vous?
""",
]
BillingScreenPrivacyPolicy = "Politique de confidentialité"
BillingScreenPrivacyPolicyClose = lClose
BillingScreenPrivacyPolicyText = [
"""
Politique de confidentialité

Q1 Quels sont les types d'informations que recueillent les sites de WDIG, et de quelle façon les recueillent-ils?

La majorité des superbes produits et services présentés sur nos sites sont proposés sans que nous recueillions d'informations à caractère personnel à votre sujet. Vous pouvez naviguer sur les sites Internet de WDIG et voir une grande partie de nos superbes contenus de manière anonyme. Par exemple, vous pouvez consulter les titres de l'actualité sur ABCNEWS.com sans fournir d'informations à caractère personnel. 

Les informations que vous fournissez
Quelques activités sur nos sites requièrent une collecte d'informations à caractère personnel. Ces activités incluent par exemple la participation à un concours ou tirage au sort, des achats ou le fait de nous contacter. Lorsque des informations à caractère personnel sont recueillies, vous le saurez puisque vous devrez remplir un formulaire. Pour la plupart des activités, nous recueillons uniquement vos nom, adresse électronique, date de naissance, sexe et code postal. Lorsque vous faites un achat, nous recueillons également vos adresses postale et de facturation, votre numéro de téléphone et vos informations de carte de crédit. En fonction du type d'achat effectué, nous devons parfois recueillir d'autres informations personnelles, telles que votre taille d'habillement.
""","""
Les informations recueillies par l'intermédiaire de la technologie
Les sites de WDIG recueillent des informations vous concernant par l'intermédiaire d'outils technologiques, de sorte que vous ne saurez pas immédiatement qu'elles sont recueillies. Par exemple, lorsque vous venez sur notre site, votre adresse IP est recueillie afin que nous puissions savoir où envoyer les informations que vous demandez. Une adresse IP est souvent associée avec la manière dont vous vous connectez à Internet, tel que votre fournisseur d'accès Internet, votre entreprise ou votre université. Ces informations ne sont pas à caractère personnel. Les sites de WDIG utilisent les informations recueillies par l'intermédiaire d'outils technologiques dans l'objectif de rendre nos sites plus intéressants et utiles pour vous. Cela inclut une aide aux annonceurs de notre site à concevoir des publicités que nos visiteurs peuvent apprécier. Nous n'associons généralement pas ce type d'informations avec des informations à caractère personnel. Cependant, nous associons ces informations avec des informations à caractère personnel afin d'identifier un visiteur dans l'objectif de faire respecter les règlements ou termes d'utilisation ou pour protéger notre service, notre site, les visiteurs ou autres.

Que sont les cookies, et de quelle manière WDIG les utilise-t-il?
Les cookies sont des informations envoyées par un site Internet à votre ordinateur lorsque vous consultez ledit site. Ces informations permettent au site Internet de mémoriser des informations importantes qui permettront d'améliorer votre usage du site. WDIG et d'autres entreprises sur Internet utilisent les cookies pour de nombreux usages. Par exemple, DisneyStore.com utilise les cookies pour mémoriser et traiter les articles de votre caddie, et tous les sites de WDIG utilisent les cookies pour s'assurer que les enfants n'accèdent pas aux salles de chat sans restriction. 

Vous pouvez choisir d'afficher un avertissement sur votre écran à chaque fois qu'un cookie est envoyé, ou vous pouvez choisir de désactiver tous les cookies. Utilisez pour cela les paramètres de votre navigateur (tel que Netscape Navigator ou Internet Explorer) Chaque navigateur est légèrement différent des autres ; consultez le menu d'aide de votre navigateur pour connaître la méthode adéquate pour modifier le comportement de vos cookies. Si vous désactivez les cookies, vous n'aurez plus accès à de nombreuses fonctions de WDIG, utilisées pour rendre votre utilisation d'Internet plus efficace - telles que les fonctions indiquées ci-dessus et certains de nos services ne fonctionneront plus correctement.
""","""
Q2 Comment est-ce que WDIG utilise les informations à caractère personnel qui ont été recueillies?

WDIG utilise les informations à caractère personnel d'une manière limitée. Nous utilisons les informations pour l'exécution des transactions. Par exemple, si vous achetez une équipe imaginaire sur ESPN.com, nous utilisons vos informations pour traiter votre commande. De même, si vous nous contactez pour demander de l'aide, nous utiliserons ces informations pour vous contacter. Nous utilisons les informations recueillies pour vous avertir si vous avez gagné un jeu ou un concours. Les informations que nous recueillons sont utilisées pour vous envoyer par courrier électronique des mises à jour et des bulletins d'informations à propos de nos sites. Nous utilisons également les informations que vous nous communiquez pour vous envoyer par courrier électronique des promotions de WDIG et des offres spéciales proposées par nos sponsors tiers. 
""","""
Q3 Est-ce que WDIG partage ses informations avec d'autres entreprises ou organisations ne faisant pas partie de la famille de sites de WDIG? 

Le capital le plus important de notre entreprise, c'est vous. Nous ne faisons pas commerce des informations concernant nos visiteurs. Cependant, si c'est dans l'intérêt de nos visiteurs, nous partagerons vos informations ou nous vous enverrons des messages de la part d'autres entreprises de la manière décrite ci-dessous. Nous pouvons aussi partager des informations pour des raisons de sécurité. 
Sociétés ayant la même position que WDIG
Parfois, nous faisons appel à d'autres sociétés pour nous aider à fournir les produits et services, à l'instar des sociétés de messagerie qui livrent des colis. Dans ce cas, nous devons partager les informations avec elles. Ces sociétés ont fondamentalement la même position que WDIG et ne sont autorisées à utiliser ces informations que pour livrer des produits ou services.
""","""
Entreprises proposant des promotions, produits ou services
Occasionnellement, nous offrons des promotions - telles que des tirages au sort ou des inscriptions gratuites - en liaison avec un sponsor. Nous partageons vos informations avec les sponsors s'ils en ont besoin pour vous envoyer un produit, tel qu'un abonnement à un magazine. Nous pouvons partager vos informations avec ces sponsors afin qu'ils puissent vous envoyer d'autres promotions particulières qu'ils proposent, mais seulement si vous nous autorisez à le faire, et nous ne les partagerons qu'avec ce sponsor particulier. De plus, WDIG envoie occasionnellement des promotions par courrier électronique à ses visiteurs de la part de sponsors tiers. Dans ce cas, nous ne communiquons pas votre identité à la partie tierce - nous nous occupons pour eux du publipostage. De la même façon, nous ne vous enverrons ces promotions que si vous nous autorisez à le faire. 

Partenaires de contenu
Sur certains de nos sites, nous proposons des contenus créés par des sites Internet partenaires tiers. Par exemple, ESPN.com propose des offres commerciales de tierces parties. Dans certains cas, les sites tiers recueillent des informations afin de faciliter la transaction ou de rendre l'utilisation de leur contenu plus productive et efficace. Dans ces circonstances, les informations recueillies sont partagées entre WDIG et nos sponsors tiers. 

Annonceurs tiers et annonceurs de réseau
Afin d'améliorer la protection de la confidentialité de nos visiteurs, WDIG autorise la publicité sur nos sites venant uniquement d'entreprises possédant leur propre politique de confidentialité. Une fois que vous avez cliqué sur une publicité et quitté les sites de WDIG, notre politique de confidentialité ne s'applique plus. Vous devez lire la politique de confidentialité de l'annonceur afin de savoir de quelle manière vos informations personnelles seront traitées sur son site.
""","""
De plus, nombre de publicités commerciales sont gérées et placées sur notre site par des sociétés tierces, que l'on appelle des " annonceurs de réseau ". Les annonceurs de réseau recueillent des informations à caractère non personnel lorsque vous balayez avec votre curseur une de leurs bannières publicitaires ou cliquez dessus. Ces informations sont recueillies à l'aide d'outils technologiques, de sorte que vous pouvez ne pas réaliser qu'elles sont recueillies. Les annonceurs de réseau recueillent ces informations afin de pouvoir afficher sur votre écran les publicités qui sont les plus adaptées et intéressantes pour vous. Pour en savoir plus à propos des annonceurs de réseau, ou si vous ne voulez pas que les annonceurs de réseau recueillent ces informations à caractère non personnel sur vous, cliquez ici.

Achat ou vente d'entreprises
Le commerce en ligne est encore à un stade de balbutiement, il change et évolue rapidement. WDIG cherche continuellement de nouvelles façons de s'améliorer, et est susceptible de vendre ou acheter une entreprise. Si nous achetons ou vendons une entreprise, les données recueillies seront probablement transférées comme faisant partie de la vente. Les informations concernant les inscrits seront incluses dans l'ensemble de la transaction. Cependant, si nous achetons une entreprise, nous honorerons les demandes faites par les clients auprès de cette entreprise concernant les communications par courrier électronique. Dans l'éventualité où nous vendrions une entreprise, nous ferons tout ce qui est en notre pouvoir pour nous assurer que les demandes que vous nous avez faites concernant les communications par courrier électronique soient respectées. 

Les organisations qui aident à protéger la sûreté et la sécurité de nos visiteurs et de nos sites.
Nous fournirons des informations personnelles si la loi nous en fait obligation, par exemple pour obéir à une ordonnance ou une assignation ; pour faire respecter nos Conditions d'utilisation, règles du jeu ; ou pour protéger la sécurité de nos visiteurs et de nos sites.
""","""
Q4 Quels sont les choix dont je dispose à propos du recueil, de l'utilisation et du partage de mes informations par WDIG?

Il vous est possible d'utiliser une grande partie de nos sites sans transmettre d'informations à caractère personnel. Lorsque vous vous inscrivez chez nous ou que vous nous fournissez des informations à caractère personnel, vous avez la possibilité au moment où nous recueillons ces informations, de limiter les communications par courrier électronique provenant de WDIG ou de nos partenaires tiers. Vous pouvez demander à tout moment que WDIG ne vous envoie plus de courrier électronique en vous désinscrivant de toute communication ou en nous contactant à memberservices@help.go.com. De plus, comme il est indiqué ci-dessus, vous pouvez limiter les informations recueillies par l'intermédiaire d'outils technologiques, bien que certaines de nos fonctions puissent ne plus être disponibles si vous décidez de procéder de la sorte.
""","""
Q5 Quel est le type de sécurité offert par WDIG?

Le souci de la sécurité pour toutes les informations à caractère personnel associées à nos visiteurs est d'une extrême importance pour nous. WDIG prend toutes les mesures de sécurité techniques, contractuelles, administratives et physiques pour protéger les informations de tous les visiteurs. Lorsque vous nous fournissez des informations bancaires, nous utilisons la technologie de chiffrement SSL (Secure Socket Layer) pour les protéger. Vous avez également la possibilité de prendre des mesures afin de protéger la sécurité de vos informations. Par exemple, ne communiquez jamais votre mot de passe, parce qu'il est utilisé pour accéder à toutes vos informations de compte. Pensez également à fermer votre compte et la fenêtre de votre navigateur lorsque vous avez terminé de naviguer sur Internet, de sorte que d'autres personnes utilisant le même ordinateur ne puissent pas avoir accès à vos informations.
""","""
Q6 Comment puis-je avoir accès aux informations de mon compte?

Vous pouvez accéder aux informations à caractère personnel que vous nous avez données pendant votre inscription auprès du centre des Options de compte, accessible depuis (http://play.toontown). Identifiez-vous avec votre nom de compte et votre mot de passe " parent ". La page de démarrage contient des instructions destinées à vous aider à récupérer votre mot de passe si vous l'avez oublié. 
Vous pouvez aussi nous contacter en cliquant sur "Contact Us" en bas de chaque page WDIG et en sélectionnant "Registration/Personalization" dans la liste déroulante, ou nous envoyer directement un courrier électronique à memberservices@help.go.com. Merci d'inclure les informations dans ce messsage qui nous aideront à identifier votre compte afin que nous puissions répondre à votre question ou votre demande.
""","""
Q7 Qui puis-je contacter pour toute question concernant cette politique de confidentialité?

Si vous avez besoin d'aide, envoyez un courrier électronique avec vos questions ou commentaires à memberservices@help.go.com
écrivez-nous à : 

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104, États-Unis

Walt Disney Internet Group est titulaire d'une licence du programme de confidentialité TRUSTe. Si vous pensez que WDIG n'a pas répondu à votre demande, ou que vous n'avez pas obtenu de réponse satisfaisante à votre demande, contactez TRUSTe http://www.truste.org/users/users_watchdog.html.
*Vous devez avoir plus de 18 ans ou obtenir la permission de votre parent ou tuteur pour composer ce numéro.
""","""
Politique de confidentialité relative aux enfants :
Nous reconnaissons la nécessité de fournir une protection de la confidentialité plus importante pour les enfants qui visitent nos sites.

Q1 Quels types d'informations les sites de WGIG recueillent-ils à propos des enfant âgés de 12 ans et moins?

Les enfants peuvent naviguer sur Disney.com et les autres sites de WDIG, visualiser des contenus et jouer à des jeux sans qu'aucune information à caractère personnel ne soit recueillie. De plus, nous hébergeons de manière occasionnelle des salles de chat modérées où aucune information à caractère personnel n'est recueillie ni postée. Cependant, dans certaines zones, il est nécessaire de recueillir des informations à caractère personnel auprès des enfants pour leur permettre de participer à une activité (comme participer à un concours) ou pour communiquer avec notre communauté (par courrier électronique ou affichage de messages). 
WDIG estime qu'il est préférable de ne pas recueillir auprès des enfants de 12 ans et moins plus d'informations à caractère personnel qu'il n'est nécessaire pour qu'ils participent à nos activités en ligne. De plus, vous devez savoir qu'il est légalement interdit par la loi à tous les sites qui sont destinés aux enfants de 12 ans et moins de recueillir plus d'informations qu'il n'est nécessaire. 

Les seules informations à caractère personnel que nous recueillons des enfants sont leur prénom, l'adresse électronique de leurs parents, et la date de naissance de l'enfant. Nous recueillons la date de naissance pour valider l'âge d'un visiteur. Nous pouvons aussi recueillir des informations à caractère personnel, telles que le nom d'un animal familier, pour aider les visiteurs à se remémorer leur nom d'utilisateur et leur mot de passe s'ils les oublient. 


Nous autorisons aussi les parents à demander à tout moment que les informations recueillies au sujet de leur enfant soient retirées de notre base de données. Si vous voulez désactiver le compte de votre enfant, envoyez un message électronique à ms_support@help.go.com indiquant le nom d'utilisateur de votre enfant et son mot de passe, demandant que son compte soit annulé.
""","""
Q2 Comment WDIG utilise et partage les informations à caractère personnel qui ont été recueillies?

Aucune information recueillie auprès de visiteurs de 12 ans et moins n'est utilisée à des fins de marketing ou de publicité quels qu'ils soient, que ce soit à l'intérieur ou à l'extérieur de la famille des sites de Walt Disney Internet Group.
Les informations recueillies auprès d'enfants de 12 ans et moins sont utilisées uniquement par les sites Web WDIG pour offrir des services (tels que des calendriers) ou organiser des jeux ou concours. Bien que les visiteurs de 12 ans et moins puissent être autorisés à participer à certains concours pour lesquels des informations sont collectées, les notifications et les prix sont envoyés à l'adresse électronique des parents ou tuteurs, fournie lors du processus d'inscription initial. La publication des nom complet, âge ou photo des gagnants des concours lorsqu'il s'agit d'individus de 12 ans et moins requiert le consentement des parents ou des tuteurs. Il arrive qu'une version non identifiable du nom de l'enfant soit publiée. Dans ce cas, les parents peuvent ne pas être contactés de nouveau pour une demande de permission. 

Nous n'autorisons pas les enfants de 12 ans et moins à participer aux chats non modérés.

Nous fournirons des informations personnelles au sujet des enfants si la loi nous en fait obligation, par exemple pour obéir à une ordonnance ou une assignation ; pour faire respecter nos Conditions d'utilisation, règles du jeu ; ou pour protéger la sécurité de nos visiteurs et de nos sites.
""","""
Q3 Est-ce que WDIG notifie les parents au sujet du recueil d'informations sur des enfants de 12 ans et moins?

À chaque fois que des enfants de 12 ans et moins s'inscrivent chez nous, nous envoyons un courrier électronique de notification à leurs parents ou tuteurs. De plus, nous demandons aux parents de donner leur permission expresse avant d'autoriser leurs enfants à utiliser le courrier électronique, les affichages de messages et autres fonctions dans le cadre desquels des informations à caractère personnel peuvent être rendues publiques sur Internet et partagées avec des utilisateurs de tous âges. 
Nous donnons aussi 48 heures aux parents pour refuser toute inscription faite par l'enfant dans le but de jouer à des jeux et des concours. Si nous n'avons pas de réponse, nous considérons que l'enfant est autorisé à s'inscrire chez nous. Une fois qu'un enfant est inscrit, il ou elle est par la suite autorisé à participer à tout jeu ou concours exigeant une inscription, et les parents ne sont pas notifiés une nouvelle fois. Dans ce cas, nous utilisons les informations recueillies uniquement pour avertir les parents lorsqu'un enfant a gagné un jeu ou concours. Nous n'utilisons pas ces informations pour aucun autre usage.
""","""
Q4 Comment les parents peuvent-ils accéder aux informations relatives à leurs enfants?

Trois méthodes permettent de visualiser les informations qui ont été recueillies à propos des enfants de 12 ans et moins. 

Lorsque les parents accordent à leurs enfants l'accès à des fonctions interactives telles que les messages affichés, il leur est demandé d'établir un compte familial. Une fois qu'un compte familial est établi, le titulaire du compte peut visionner les informations à caractère personnel de tous les comptes des membres de la famille, y compris ceux d'un enfant. Vous pouvez accéder à ces informations en ouvrant votre compte familial sur la page d'accueil, " Votre compte ". 

Si vous n'êtes membre d'aucun des sites WDIG, vous pouvez visionner les informations à caractère personnel de votre enfant en ouvrant le compte de celui-ci sur la page d'accueil des " Options de compte ". Vous aurez besoin du nom d'utilisateur et du mot de passe de votre enfant. La page " Votre compte " contient des instructions pour vous aider à récupérer le mot de passe de votre enfant s'il l'a oublié. 

Vous pouvez également contacter le Service clients pour visionner les informations qui ont été recueillies sur ou auprès de votre enfant en envoyant un courrier électronique à ms_support@help.go.com. Si vous n'avez pas encore de compte familial, vous aurez besoin du nom d'utilisateur et du mot de passe de votre enfant. Merci d'inclure les informations (nom d'utilisateur de votre enfant, adresse électronique des parents) dans le message, qui nous permettront d'identifier le compte de votre enfant afin que nous puissions répondre à votre question ou demande.
""","""
Q5 Quel est le type de sécurité offert par WDIG?

Le souci de la sécurité pour toutes les informations à caractère personnel associées à nos visiteurs est d'une extrême importance pour nous. WDIG prend toutes les mesures de sécurité techniques, contractuelles, administratives et physiques pour protéger les informations de tous les visiteurs. Lorsque vous nous fournissez des informations de carte de crédit, nous utilisons la technologie de chiffrement SSL (Secure Socket Layer) pour les protéger. Vous avez également la possibilité de prendre des mesures afin de protéger la sécurité de vos informations. Par exemple, ne communiquez jamais votre mot de passe, parce qu'il est utilisé pour accéder à toutes vos informations de compte. Pensez également à fermer votre compte et la fenêtre de votre navigateur lorsque vous avez terminé de naviguer sur Internet, de sorte que d'autres personnes utilisant le même ordinateur ne puissent pas avoir accès à vos informations.
""","""
Q6 Comment WDIG notifie les parents si la politique de confidentialité est modifiée?

Si WDIG modifie sa politique de confidentialité, nous avertissons les parents par courrier électronique.

Q7 Qui puis-je contacter pour toute question concernant cette politique de confidentialité?

Si vous avez besoin d'aide, envoyez-nous un courrier électronique avec vos questions ou commentaires à ms_support@help.go.com
écrivez-nous à : 

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104, États-Unis
ou appelez-nous au 00 1 (509) 742-4698

Walt Disney Internet Group est titulaire d'une licence du programme de confidentialité TRUSTe. Si vous pensez que WDIG n'a pas répondu à votre demande, ou que vous n'avez pas obtenu de réponse satisfaisante à votre demande, contactez TRUSTe http://www.truste.org/users/users_watchdog.html.
*Vous devez avoir plus de 18 ans ou obtenir la permission de votre parent ou tuteur pour composer ce numéro.
""",
]
BillingScreenCountryNames = {
    "US" : "États-Unis",
    "CA" : "Canada",
    "AF" : "Afghanistan",
    "AL" : "Albanie",
    "DZ" : "Algérie",
    "AS" : "Samoa Américaines",
    "AD" : "Andorre",
    "AO" : "Angola",
    "AI" : "Anguilla",
    "AQ" : "Antarctique",
    "AG" : "Antigua-et-Barbuda",
    "AR" : "Argentine",
    "AM" : "Arménie",
    "AW" : "Aruba",
    "AU" : "Australie",
    "AT" : "Autriche",
    "AZ" : "Azerbaïdjan",
    "BS" : "Bahamas",
    "BH" : "Bahreïn",
    "BD" : "Bangladesh",
    "BB" : "Barbade",
    "BY" : "Bélarus",
    "BE" : "Belgique",
    "BZ" : "Belize",
    "BJ" : "Bénin",
    "BM" : "Bermuda",
    "BT" : "Bhoutan",
    "BO" : "Bolivie",
    "BA" : "Bosnie-Herzégovine",
    "BW" : "Botswana",
    "BV" : "Île Bouvet",
    "BR" : "Brésil",
    "IO" : "Territoire britannique de l'océan Indien",
    "BN" : "Brunei Darussalam",
    "BG" : "Bulgarie",
    "BF" : "Burkina Faso",
    "BI" : "Burundi",
    "KH" : "Cambodge",
    "CM" : "Cameroun",
    "CV" : "Cap-Vert",
    "KY" : "Îles Cayman",
    "CF" : "République Centrafricaine",
    "TD" : "Tchad",
    "CL" : "Chili",
    "CN" : "Chine",
    "CX" : "Île Christmas",
    "CC" : "Îles Cocos (Keeling)",
    "CO" : "Colombie",
    "KM" : "Comores",
    "CG" : "Congo",
    "CK" : "Îles Cook",
    "CR" : "Costa Rica",
    "CI" : "Côte d'Ivoire",
    "HR" : "Croatie",
    "CU" : "Cuba",
    "CY" : "Chypre",
    "CZ" : "République Tchèque",
    "CS" : "Ex-Tchécoslovaquie",
    "DK" : "Danemark",
    "DJ" : "Djibouti",
    "DM" : "Dominique",
    "DO" : "République Dominicaine",
    "TP" : "Timor-Oriental",
    "EC" : "Équateur",
    "EG" : "Égypte",
    "SV" : "Salvador",
    "GQ" : "Guinée équatoriale",
    "ER" : "Érythrée ",
    "EE" : "Estonie",
    "ET" : "Éthiopie",
    "FK" : "Îles Malouines",
    "FO" : "Îles Féroé",
    "FJ" : "Fidji",
    "FI" : "Finlande",
    "FR" : "France",
    "FX" : "France métropolitaine",
    "GF" : "Guyane Française",
    "PF" : "Polynésie Française",
    "TF" : "Terres Australes Françaises",
    "GA" : "Gabon",
    "GM" : "Gambie",
    "GE" : "Géorgie",
    "DE" : "Allemagne",
    "GH" : "Ghana",
    "GI" : "Gibraltar",
    "GB" : "Grande-Bretagne (Royaume-Uni)",
    "GR" : "Grèce",
    "GL" : "Groenland",
    "GD" : "Grenade",
    "GP" : "Guadeloupe",
    "GU" : "Guam",
    "GT" : "Guatemala",
    "GN" : "Guinée",
    "GW" : "Guinée-Bissau",
    "GY" : "Guyana",
    "HT" : "Haïti",
    "HM" : "Îles Heard et McDonald",
    "HN" : "Honduras",
    "HK" : "Hong Kong",
    "HU" : "Hongrie",
    "IS" : "Islande",
    "IN" : "Inde",
    "ID" : "Indonésie",
    "IR" : "Iran",
    "IQ" : "Irak",
    "IE" : "Irlande",
    "IL" : "Israël",
    "IT" : "Italie",
    "JM" : "Jamaïque",
    "JP" : "Japon",
    "JO" : "Jordanie",
    "KZ" : "Kazakhstan",
    "KE" : "Kenya",
    "KI" : "Kiribati",
    "KP" : "Corée du Nord",
    "KR" : "Corée du Sud",
    "KW" : "Koweït",
    "KG" : "Kirghizistan",
    "LA" : "Laos",
    "LV" : "Lettonie",
    "LB" : "Liban",
    "LS" : "Lesotho",
    "LR" : "Libéria",
    "LY" : "Libye",
    "LI" : "Liechtenstein",
    "LT" : "Lituanie",
    "LU" : "Luxembourg",
    "MO" : "Macao",
    "MK" : "Macédoine",
    "MG" : "Madagascar",
    "MW" : "Malawi",
    "MY" : "Malaisie",
    "MV" : "Maldives",
    "ML" : "Mali",
    "MT" : "Malte",
    "MH" : "Îles Marshall",
    "MQ" : "Martinique",
    "MR" : "Mauritanie",
    "MU" : "Maurice",
    "YT" : "Mayotte",
    "MX" : "Mexique",
    "FM" : "Micronésie",
    "MD" : "Moldavie",
    "MC" : "Monaco",
    "MN" : "Mongolie",
    "MS" : "Montserrat",
    "MA" : "Maroc",
    "MZ" : "Mozambique",
    "MM" : "Myanmar (Birmanie)",
    "NA" : "Namibie",
    "NR" : "Nauru",
    "NP" : "Népal",
    "NL" : "Pays-Bas",
    "AN" : "Antilles Néerlandaises",
    "NT" : "Zone neutre",
    "NC" : "Nouvelle-Calédonie",
    "NZ" : "Nouvelle-Zélande (Aotearoa)",
    "NI" : "Nicaragua",
    "NE" : "Niger",
    "NG" : "Nigéria",
    "NU" : "Niue",
    "NF" : "Île Norfolk ",
    "MP" : "Îles Mariannes du Nord",
    "NO" : "Norvège",
    "OM" : "Oman",
    "PK" : "Pakistan",
    "PW" : "Palaos",
    "PA" : "Panama",
    "PG" : "Papouasie-Nouvelle-Guinée",
    "PY" : "Paraguay",
    "PE" : "Pérou",
    "PH" : "Philippines",
    "PN" : "Île Pitcairn",
    "PL" : "Pologne",
    "PT" : "Portugal",
    "PR" : "Puerto Rico",
    "QA" : "Qatar",
    "RE" : "Réunion",
    "RO" : "Roumanie",
    "RU" : "Fédération de Russie",
    "RW" : "Rwanda",
    "GS" : "Îles de Géorgie du Sud et Sandwich du Sud",
    "KN" : "Saint Kitts and Nevis",
    "LC" : "Sainte-Lucie",
    "VC" : "Saint-Vincent-et-les-Grenadines",
    "WS" : "Samoa",
    "SM" : "Saint-Marin",
    "ST" : "Sao Tomé et Principe",
    "SA" : "Arabie saoudite",
    "SN" : "Sénégal",
    "SC" : "Seychelles",
    "SL" : "Sierra Leone",
    "SG" : "Singapour",
    "SK" : "Slovaquie",
    "SI" : "Slovénie",
    "Sb" : "Îles Salomon",
    "SO" : "Somalie",
    "ZA" : "Afrique du Sud",
    "ES" : "Espagne",
    "LK" : "Sri Lanka",
    "SH" : "Sainte-Hélène",
    "PM" : "St-Pierre-et-Miquelon",
    "SD" : "Soudan",
    "SR" : "Surinam",
    "SJ" : "Îles Svalbard et Jan Mayen",
    "SZ" : "Swaziland",
    "SE" : "Suède",
    "CH" : "Suisse",
    "SY" : "Syrie",
    "TW" : "Taïwan",
    "TJ" : "Tadjikistan",
    "TZ" : "Tanzanie",
    "TH" : "Thaïlande ",
    "TG" : "Togo",
    "TK" : "Tokelau",
    "TO" : "Tonga",
    "TT" : "Trinidad et Tobago",
    "TN" : "Tunisie",
    "TR" : "Turquie",
    "TM" : "Turkménistan",
    "TC" : "Îles Turks et Caicos",
    "TV" : "Tuvalu",
    "UG" : "Ouganda",
    "UA" : "Ukraine",
    "AE" : "Émirats Arabes Unis",
    "UK" : "Royaume-Uni",
    "UY" : "Uruguay",
    "UM" : "Îles Mineures Américaines ",
    "SU" : "Ex-URSS",
    "UZ" : "Ouzbékistan",
    "VU" : "Vanuatu",
    "VA" : "État de la Cité du Vatican (Saint-Siège)",
    "VE" : "Venezuela",
    "VN" : "Vietnam",
    "VG" : "Îles Vierges (Britanniques)",
    "VI" : "Îles Vierges (Américaines)",
    "WF" : "Îles Wallis et Futuna",
    "EH" : "Sahara Occidental",
    "YE" : "Yémen",
    "YU" : "Yougoslavie",
    "ZR" : "Zaïre",
    "ZM" : "Zambie",
    "ZW" : "Zimbabwe",
    }
BillingScreenStateNames = {
    "AL" : "Alabama",
    "AK" : "Alaska",
    "AR" : "Arkansas",
    "AZ" : "Arizona",
    "CA" : "Californie",
    "CO" : "Colorado",
    "CT" : "Connecticut",
    "DE" : "Delaware",
    "FL" : "Floride",
    "GA" : "Géorgie",
    "HI" : "Hawaï",
    "IA" : "Iowa",
    "ID" : "Idaho",
    "IL" : "Illinois",
    "IN" : "Indiana",
    "KS" : "Kansas",
    "KY" : "Kentucky",
    "LA" : "Louisiane",
    "MA" : "Massachusetts",
    "MD" : "Maryland",
    "ME" : "Maine",
    "MI" : "Michigan",
    "MN" : "Minnesota",
    "MO" : "Missouri",
    "MS" : "Mississippi",
    "MT" : "Montana",
    "NE" : "Nebraska",
    "NC" : "Caroline du Nord",
    "ND" : "Dakota du Nord",
    "NH" : "New Hampshire",
    "NJ" : "New Jersey",
    "NM" : "Nouveau-Mexique",
    "NV" : "Nevada",
    "NY" : "New York",
    "OH" : "Ohio",
    "OK" : "Oklahoma",
    "OU" : "Oregon",
    "PA" : "Pennsylvanie",
    "RI" : "Rhode Island",
    "SC" : "Caroline du Sud",
    "SD" : "Dakota du Sud",
    "TN" : "Tennessee",
    "TX" : "Texas",
    "UT" : "Utah",
    "VA" : "Virginie",
    "VT" : "Vermont",
    "WA" : "Washington",
    "WI" : "Wisconsin",
    "WV" : "Virginie-Occidentale",
    "WY" : "Wyoming",
    "DC" : "District fédéral de Columbia",
    "AS" : "Samoa Américaines",
    "GU" : "Guam",
    "MP" : "Îles Mariannes du Nord",
    "PR" : "Puerto Rico",
    "VI" : "Îles Vierges",
    "FPO" : ["Îles Midway",
             "Kingman Reef",
             ],
    "APO" : ["Île de Wake",
             "Île Johnston",
             ],
    "MH" : "Îles Marshall",
    "PW" : "Palaos",
    "FM" : "Micronésie",
    }
BillingScreenCanadianProvinces = {
    'AB' : 'Alberta',
    'BC' : 'Colombie-Britannique',
    'MB' : 'Manitoba',
    'NB' : 'Nouveau-Brunswick',
    'NF' : 'Terre-Neuve',
    'NT' : 'Territoires du Nord-Ouest',
    'NS' : 'Nouvelle-Écosse',
    #'XX' : 'Nunavut',
    'ON' : 'Ontario',
    'PE' : 'Île du Prince-Édouard',
    'QC' : 'Québec',
    'SK' : 'Saskatchewan',
    'YT' : 'Yukon',
    }

ParentPassword = "Mot de passe parent"

# WelcomeScreen.py
WelcomeScreenHeading = "Bienvenue!"
WelcomeScreenOk = "JOUONS!"
WelcomeScreenSentence1 = "Vous êtes maintenant officiellement membre de"
WelcomeScreenToontown = "Toontown en ligne de Disney"
WelcomeScreenSentence2 = "N'oubliez pas de vérifier votre courrier électronique régulièrement pour découvrir des nouvelles palpitantes au sujet de Toontown en ligne de Disney!"

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Appelez le Service clients au %s. "
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nSi vous avez besoin d'aide, vous pouvez appeler le service clients au %s."
TTAccountIntractibleError = "Une erreur s'est produite."

# LoginScreen.py
LoginScreenUserName = "Nom du compte"
LoginScreenPassword = "Mot de passe"
LoginScreenLogin = "Ouvrir une session"
LoginScreenCreateAccount = "Créer un compte"
LoginScreenForgotPassword = "Mot de passe oublié?"
LoginScreenQuit = lQuit
LoginScreenLoginPrompt = "Entrez un nom d'utilisateur et un mot de passe."
LoginScreenBadPassword = "Mot de passe erroné.\nRessayez."
LoginScreenInvalidUserName = "Nom d'utilisateur incorrect.\nRessayez."
LoginScreenUserNameNotFound = "Utilisateur introuvable.\nRessayez ou créez un nouveau compte."
LoginScreenPeriodTimeExpired = "Désolé, vous avez déjà utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci. Revenez au début du mois prochain."
LoginScreenNoNewAccounts = "Nous sommes désolé, nous n'acceptons pas de nouveaux comptes pour le moment."
LoginScreenTryAgain = "Ressayez"

# NewPlayerScreen.py
NewPlayerScreenNewAccount = "Commencer l'essai gratuit"
NewPlayerScreenLogin = "Membre existant"
NewPlayerScreenQuit = lQuit

# FreeTimeInformScreen.py
FreeTimeInformScreenDontForget = "N'oubliez pas que votre essai gratuit\nse termine dans "
FreeTimeInformScreenNDaysLeft = FreeTimeInformScreenDontForget + "seulement %s jours!" 
FreeTimeInformScreenOneDayLeft = FreeTimeInformScreenDontForget + "1 jour!" 
FreeTimeInformScreenNHoursLeft = FreeTimeInformScreenDontForget + "seulement %s heures!" 
FreeTimeInformScreenOneHourLeft = FreeTimeInformScreenDontForget + "1 heure!" 
FreeTimeInformScreenLessThanOneHourLeft = FreeTimeInformScreenDontForget + "moins d'une heure!" 
FreeTimeInformScreenSecondSentence = "Mais il est encore temps de devenir \nofficiellement membre de Toontown en ligne de Disney!"
FreeTimeInformScreenOops = "OH LÀ LÀ"
FreeTimeInformScreenExpired = "                 , votre essai gratuit est maintenant terminé!\nVous voulez devenir officiellement membre de Toontown en ligne de Disney?\nInscrivez-vous maintenant et revenez vous amuser!"
FreeTimeInformScreenExpiredQuitText = "Ce n'est pas possible maintenant? Ne vous inquiétez pas, nous \ngardons votre Toon! Mais revenez vite! Nous \ngardons votre Toon une seule semaine à \nl'issue de votre essai gratuit."
FreeTimeInformScreenExpiredCCUF = "Vous n'avez pas encore acheté Toontown\n de Disney en ligne. Pour utiliser ce compte, \nvous devez vous inscrire avec une carte de crédit.\nInscrivez-vous maintenant et venez vous amuser!"
FreeTimeInformScreenExpiredQuitCCUFText = "Ce n'est pas possible maintenant? Ne vous inquiétez pas, nous \nnous gardons votre compte! Mais revenez vite! Nous \ngardons votre compte une seule semaine."
FreeTimeInformScreenPurchase = "Inscrivez-vous!"
FreeTimeInformScreenFreePlay = "Continuer l'essai gratuit"
FreeTimeInformScreenQuit = lQuit

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                          'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc',]
DateOfBirthEntryDefaultLabel = "Date de naissance"

# CreateAccountScreen.py
CreateAccountScreenUserName = "Nom du compte"
CreateAccountScreenPassword = "Mot de passe"
CreateAccountScreenConfirmPassword = "Confirmation du mot de passe"
CreateAccountScreenFree = "GRATUIT"
CreateAccountScreenFreeTrialLength = "Pour commencer votre essai de %s jours,n\vous devez créer un compte."
CreateAccountScreenInstructionsUsername = "Indiquez le nom de compte que vous voulez utiliser :"
CreateAccountScreenInstructionsPassword = "Entrez un mot de passe :"
CreateAccountScreenInstructionsConfirmPassword = "Confirmez votre mot de passe pour plus de sûreté :"
CreateAccountScreenInstructionsDob = "Entrez votre date de naissance :"
CreateAccountScreenCancel = lCancel
CreateAccountScreenSubmit = lNext
CreateAccountScreenConnectionErrorSuffix = ".\n\nRessayez plus tard."
CreateAccountScreenNoAccountName = "Choisissez un nom de compte."
CreateAccountScreenAccountNameTooShort = "Le nom de votre compte doit comporter au moins %s caractères. Ressayez."
CreateAccountScreenPasswordTooShort = "Votre mot de passe doit comporter au moins %s caractères. Ressayez."
CreateAccountScreenPasswordMismatch = "Les mots de passe que vous avez entrés ne sont pas identiques. Ressayez."
CreateAccountScreenInvalidDob = "Entrez votre date de naissance."
CreateAccountScreenUserNameTaken = "Ce nom d'utilisateur est déjà pris. Ressayez."
CreateAccountScreenInvalidUserName = "Nom d'utilisateur incorrect.\nRessayez."
CreateAccountScreenUserNameNotFound = "Nom d'utilisateur introuvable.\nRessayez ou créez un nouveau compte."
CreateAccountScreenEmailInstructions = "Entrez votre adresse électronique.\nPourquoi? Pour deux raisons :\n1. Si vous avez oublié votre mot de passe, nous pouvons vous l'envoyer!\n2. Nous pourrons vous envoyer les dernières nouvelles de\nToontown en ligne de Disney."
CreateAccountScreenEmailInstructionsUnder13 = "Tu as indiqué que tu as moins de 13 ans.\nPour créer un compte, nous avons besoin de l'adresse électronique d'un de tes parents ou tuteurs."
CreateAccountScreenEmailConfirm = "Confirme l'adresse électronique pour plus de sûreté :"
CreateAccountScreenEmailPanelSubmit = lNext
CreateAccountScreenEmailPanelCancel = lCancel
CreateAccountScreenInvalidEmail = "Entre l'adresse électronique complète."
CreateAccountScreenEmailMismatch = "Les adresses électroniques que tu as entrées ne correspondent pas. Essaie encore."

# SecretFriendsInfoPanel.py
SecretFriendsInfoPanelOk = lOK
SecretFriendsInfoPanelText = ["""
La fonction " Amis secrets "

La fonction " Amis secrets " permet à un membre de s'adresser directement à un autre membre sur Toontown en ligne de Disney (le " Service "), une fois que ces membres ont établi une connexion " Amis secrets ". Si votre enfant veut utiliser la fonction " Amis secrets ", nous vous demandons de nous indiquer que vous l'autorisez à utiliser cette fonction en entrant votre Mot de Passe Parent. Voici une description détaillée de la procédure permettant de créer une connexion " Amis secrets " entre deux membres, que nous avons appelés "Sally" et "Mike."
1. Les parents de Sally et de Mike activent chacun de leur côté la fonction " Amis secrets " en entrant leurs mots de passe parent respectifs, soit (a) dans les " Options de compte " du service, soit (b) lorsque celui-ci leur est demandé par une fenêtre contextuelle de contrôle parental. 
2. Sally demande un secret (décrit ci-dessous) depuis le service.
""","""
3. Le secret de Sally est communiqué à Mike en dehors du service. (Il peut lui être communiqué soit directement par Sally, soit indirectement lorsque Sally révèle son secret à une autre personne.)
4. Mike soumet le secret de Sally au service dans les 48 heures après que Sally a fait la demande du secret.
5. Le service avertit alors Mike que Sally est devenue son amie secrète. Le service avertit également Sally que Mike est devenu son ami secret. 
6. Sally et Mike peuvent alors discuter directement entre eux jusqu'à ce que l'un des deux choisisse de mettre fin à leur amitié secrète, ou que l'un des parents respectifs de Sally ou Mike mette fin à la fonction " Ami secret ". Le lien " Ami secret " peut donc être désactivé à tout moment par soit : (a) un membre désactivant son ou ses amis secrets de sa liste d'amis (comme il est décrit dans le service) ; soit, (b) le parent de ce membre désactivant la fonction " Ami secret " en allant dans la zone " Options de compte " du service et en suivant les étapes détaillées ici.
""","""
Un secret est un code aléatoire généré par ordinateur assigné à un membre particulier. Le secret doit être utilisé pour activer un lien d'ami secret dans les 48 heures à partir du moment où le membre demande le secret ; faute de quoi le secret arrive à expiration et ne peut plus être utilisé. De plus, un secret ne peut être utilisé que pour établir un seul lien d'ami secret. Pour créer d'autres liens d'amis secrets, le membre doit demander un nouveau secret pour chaque ami secret supplémentaire.

L'amitié secrète n'est pas transférable. Par exemple, si Sally devient amie secrète de Mike, et que Mike devient ami secret de Jessica, Sally ne devient pas automatiquement amie secrète de Jessica. Pour que Sally et Jessica deviennent amies secrètes, l'une d'entre elles doit demander un nouveau secret au service et le communiquer à l'autre. 
""","""
Les amis secrets communiquent entre eux par un chat interactif de forme libre. Le contenu de ce chat est rédigé directement par le membre participant et est traité par le service, qui est exploité par Walt Disney Internet Group ("WDIG"), 506 2nd Avenue, Suite 2100, Seattle, WA 98104 (téléphone 00 1 (509) 742-4698 ; courrier électronique ms_support@help.go.com). Nous conseillons à nos membres de ne pas échanger d'informations personnelles telles que leurs noms, prénoms, adresses électroniques, adresses postales ou numéros de téléphone lors de l'utilisation de la fonction " Amis secrets ". Cependant, nous ne pouvons pas garantir que ce type d'échange d'informations personnelles ne se produira pas. Bien que le chat " Amis secrets " fasse l'objet d'un filtrage automatique pour la plupart des mots grossiers, il n'est ni modéré ni supervisé par nous. Si les parents autorisent leurs enfants à utiliser leur compte avec la fonction " Amis secrets " activée, nous les encourageons à surveiller leurs enfants lorsqu'ils jouent dans le cadre de nos services. 
""","""
WDIG n'utilise le contenu du chat " Amis secrets " pour aucun autre usage que la communication de ce contenu à l'ami secret du membre, et ne révèle ce contenu à aucun tiers excepté : (1) si cela est légalement nécessaire, par exemple pour exécuter une ordonnance de tribunal ou une assignation ; (2) pour faire respecter les Conditions d'utilisation applicables au service (consultables sur la page d'accueil) ; ou (3) pour protéger la sûreté et la sécurité des membres du service et le service lui-même. Sur demande adressée à WDIG, le parent d'un enfant peut consulter et faire supprimer tout contenu de chat d'ami secret produit par cet enfant, dans la mesure où ledit contenu n'a pas déjà été supprimé des fichiers de WDIG. En vertu de la loi américaine sur la protection de la confidentialité des enfants (Children's Online Privacy Protection Act), il nous est interdit de subordonner, et nous ne subordonnons pas, la participation d'un enfant à quelque activité que ce soit (y compris les amis secrets) à la communication par l'enfant de plus d'informations qu'il n'est raisonnablement nécessaire à la participation à une telle activité.
""","""
De plus, comme il est indiqué ci-dessus, nous reconnaissons le droit d'un parent de nous refuser l'autorisation de permettre à un enfant l'utilisation de la fonction " Amis secrets ". En activant la fonction " Amis secrets ", vous reconnaissez qu'il existe des risques inhérents à la capacité des membres à discuter les uns avec les autres par la fonction " Amis secrets ", que vous avez été informés de ceux-ci, et voulez bien accepter lesdits risques. 
"""
]

# ParentPasswordScreen.py
ParentPasswordScreenTitle = "Contrôle parental"
ParentPasswordScreenPassword = "Créer un mot de passe \" parent \""
ParentPasswordScreenConfirmPassword = "Confirmer le mot de passe \" parent \""
ParentPasswordScreenSubmit = "Établir le mot de passe \" parent \""
ParentPasswordScreenConnectionErrorSuffix = ".\nRessayez plus tard."
ParentPasswordScreenPasswordTooShort = "Votre mot de passe doit comporter au moins %s caractères. Ressayez."
ParentPasswordScreenPasswordMismatch = "Les mots de passe que vous avez entrés ne sont pas identiques. Ressayez."
ParentPasswordScreenConnectionProblemJustPaid = "Un problème est survenu lors du contact avec le serveur des comptes, mais ne vous inquiétez pas ; votre achat est bien pris en compte.\n\nIl vous sera de nouveau demandé d'établir votre mot de passe \" parent \" la prochaine fois que vous vous connectez."
ParentPasswordScreenConnectionProblemJustLoggedIn = "Un problème est survenu lors du contact avec le serveur des comptes. Ressayez ultérieurement."
ParentPasswordScreenSecretFriendsMoreInfo = "Plus d'infos"
ParentPasswordScreenInstructions = """ Veuillez créer un \"mot de passe parent \" pour ce compte - le mot de passe parent vous sera demandé ultérieurement:

  1.  Quand nous vous demandons d'autoriser votre/vos enfant(s) à 
       utiliser certaines fonctions interactives de Toontown, 
       comme la fonction " Amis secrets ". Pour obtenir une 
       description complète de cette fonction et de la façon dont 
       elle permet à votre/vos enfant(s) de communiquer en ligne 
       avec d'autres membres de Toontown, cliquez sur le bouton 
       '"""+ParentPasswordScreenSecretFriendsMoreInfo+"""' ci-dessous. Votre autorisation 
       est nécessaire pour activer cette fonction.   


2. Pour mettre à jour, sur la page Web de Toontown, 
    les informations concernant votre compte et la facturation.
"""
ParentPasswordScreenAdvice = "Attention de ne pas divulguer ce Mot de Passe Parent. Il est capital que vous protégiez la confidentialité de votre Mot de Passe Parent si vous voulez contrôler l'utilisation par votre/vos enfants des fonctions interactives de votre compte."
ParentPasswordScreenPrivacyPolicy = "Respect de la vie privée"


# ForgotPasswordScreen.py
ForgotPasswordScreenTitle = "Si vous avez oublié votre mot de passe, nous pouvons vous l'envoyer!"
ForgotPasswordScreenInstructions = "Entrez votre nom de compte OU l'adresse électronique que vous nous avez fournie."
ForgotPasswordScreenEmailEntryLabel = "Adresse électronique"
ForgotPasswordScreenOr = "OU"
ForgotPasswordScreenAcctNameEntryLabel = "Nom du compte"
ForgotPasswordScreenSubmit = "Envoyer"
ForgotPasswordScreenCancel = lCancel
ForgotPasswordScreenEmailSuccess = "Votre mot de passe a été envoyé à '%s'."
ForgotPasswordScreenEmailFailure = "Adresse électronique introuvable : '%s'."
ForgotPasswordScreenAccountNameSuccess = "Votre mot de passe a été envoyé à l'adresse électronique que vous avez fournie lorsque vous avez créé votre compte."
ForgotPasswordScreenAccountNameFailure = "Compte introuvable : %s"
ForgotPasswordScreenNoEmailAddress = "Ce compte a été créé par une personne âgée de moins de 13 ans, et n'a pas d'adresse électronique. Nous ne pouvons pas vous envoyer votre mot de passe.\n\nVous pouvez créer un autre compte!"
ForgotPasswordScreenInvalidEmail = "Entrez une adresse électronique valide."

# GuiScreen.py
GuiScreenToontownUnavailable = "Toontown semble momentanément indisponible, nouvelle tentative..."
GuiScreenCancel = lCancel

# AchievePage.py
AchievePageTitle = "Réussites\n (Bientôt disponible)"

# PhotoPage.py
PhotoPageTitle = "Photo\n (Bientôt disponible)"

# BuildingPage.py
BuildingPageTitle = "Bâtiments\n (Bientôt disponible)"

# InventoryPage.py
InventoryPageTitle = "Gags"
InventoryPageDeleteTitle = "SUPPRIMER LES GAGS"
InventoryPageTrackFull = "Tu as tous les gags de la série %s. "
InventoryPagePluralPoints = "Tu auras un nouveau gag de la série \n%(trackName)s lorsque tu\nauras %(numPoints)s points de %(trackName)s en plus."
InventoryPageSinglePoint = "Tu auras un nouveau gag de la série \n%(trackName)s lorsque tu\nauras %(numPoints)s points de %(trackName)s en plus."
InventoryPageNoAccess = "Tu n'as pas encore accès à la série %s."

# NPCFriendPage.py
NPCFriendPageTitle = "SOS Toons"

# MapPage.py
MapPageTitle = "Carte"
MapPageBackToPlayground = "au terrain de jeux"
MapPageBackToCogHQ = "Retour au QG des Cogs"
MapPageGoHome = "à la maison"
# hood name, street name
MapPageYouAreHere = "Tu es à : %s\n%s"
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
OptionsPageFriendsEnabledLabel = "Demandes de nouveaux amis acceptées."
OptionsPageFriendsDisabledLabel = "Demandes de nouveaux amis non acceptées."
OptionsPageSpeedChatStyleLabel = "Couleur du Chat rapide"
OptionsPageDisplayWindowed = "dans une fenêtre"
OptionsPageSelect = "Choisir"
OptionsPageToggleOn = "Activer"
OptionsPageToggleOff = "Désactiver"
OptionsPageChange = "Modifier"
OptionsPageDisplaySettings = "Affichage : %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Affichage : %(screensize)s"
OptionsPageExitConfirm = "Quitter Toontown?"

DisplaySettingsTitle = "Réglages d'affichage"
DisplaySettingsIntro = "Les réglages suivants sont utilisés pour configurer l'affichage de Toontown sur votre ordinateur. Il n'est sans doute pas indispensable de les modifier sauf si vous avez un problème."
DisplaySettingsIntroSimple = "Vous pouvez accroître la résolution d'écran pour améliorer la lisibilité du texte et des graphiques de Toontown, mais en fonction de votre carte graphique, certaines valeurs plus élevées risquent d'affecter le bon fonctionnement du jeu, voire de l'empêcher complètement de fonctionner."

DisplaySettingsApi = "Interface graphique :"
DisplaySettingsResolution = "Résolution :"
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
TrackPageShortTitle = "Entraînement aux gags"
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
QuestPosterPlayground = "Sur le terrain de jeux "
QuestPosterAnywhere = "N'importe où"
QuestPosterAuxTo = "à :"
QuestPosterAuxFrom = "depuis :"
QuestPosterAuxFor = "pour :"
QuestPosterAuxOr = "ou :"
QuestPosterAuxReturnTo = "Retourner à :"
QuestPosterLocationIn = ""
QuestPosterLocationOn = ""
QuestPosterFun = "Juste pour s'amuser!"
QuestPosterFishing = "ALLER PÊCHER"
QuestPosterComplete = "TERMINÉ"

# ShardPage.py
ShardPageTitle = "Districts"
ShardPageHelpIntro = "Chaque district est une copie du monde de Toontown."
ShardPageHelpWhere = "Tu es actuellement dans le district de \"%s\"."
ShardPageHelpWelcomeValley = " Tu es actuellement dans le district de la  \" Vallée de la Bienvenue \", dans \"%s\"."
ShardPageHelpMove = "Pour aller dans un nouveau district, clique sur son nom."

ShardPagePopulationTotal = "Population totale de Toontown :\n%d"
ShardPageScrollTitle = "Nom Population"

# SuitPage.py
SuitPageTitle = "Galerie des Cogs"
SuitPageMystery = DialogQuestion + DialogQuestion + DialogQuestion
SuitPageQuota = "%s sur %s"
SuitPageCogRadar = "%s présents"
SuitPageBuildingRadarS = "Bâtiment %s"
SuitPageBuildingRadarP = "Bâtiments %s"

# DisguisePage.py
DisguisePageTitle = "Déguisement de " + Cog + " Disguise"
DisguisePageMeritAlert = "Prêt pour la\npromotion!"
DisguisePageCogLevel = "Niveau %s"
DisguisePageMeritFull = "Plein"
# 1_1_8_branch
DisguisePageMeritBar = "Merit Progress"
DisguisePageCogPartRatio = "%d/%d"

# FishPage.py
FishPageTitle = "Pêche"
FishPageTitleTank = "Seau de pêche"
FishPageTitleCollection = "Album de pêche"
FishPageTitleTrophy = "Trophées de pêche"
FishPageWeightStr = "Poids : "
FishPageWeightLargeS = "%d kg "
FishPageWeightLargeP = "%d kg "
FishPageWeightSmallS = "%d g"
FishPageWeightSmallP = "%d g"
FishPageWeightConversion = 16
FishPageValueS = "Valeur: %d bonbon"
FishPageValueP = "Valeur: %d bonbons"
FishPageTotalValue = ""
FishPageCollectedTotal = "Espèces de poissons pêchées: %d sur %d"
FishPageRodInfo = "Canne %s \n%d - %d livres"
FishPageTankTab = "Seau"
FishPageCollectionTab = "Album"
FishPageTrophyTab = "Trophées"

FishPickerTotalValue = "Seau : %s / %s\nValeur: %d bonbons"

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
    }

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
EmotePageDance = "Tu as construit la séquence de danse suivante :"
EmoteJump = "Saut"
EmoteDance = "Danse"
EmoteHappy = "Content(e)"
EmoteSad = "Triste"
EmoteAnnoyed = "Agacement"
EmoteSleep = "Sommeil"

# Emote.py
# List of emotes in the order they should appear in the SpeedChat.
# Must be in the same order as the function list (EmoteFunc) in Emote.py
EmoteList = [
    "Signe de la main",
    "Content(e)",
    "Triste",
    "En colère",
    "Sommeil",
    "Haussement d'épaules",
    "Danse",
    "Clin d'œil",
    "Ennuyé(e)",
    "Applaudissements",
    "Surpris(e)",
    "Désorienté(e)",
    "Moquerie",
    "Révérence",
    "Vraiment triste",
    "Grand sourire",
    "Rire",
    lYes,
    lNo,
    lOK,
    ]

EmoteWhispers = [
    "%s fait un signe de la main.",
    "%s est content(e).",
    "%s est triste.",
    "%s est en colère.",
    "%s a sommeil.",
    "%s hausse les épaules.",
    "%s danse.",
    "%s fait un clin d'œil.",
    "%s s'ennuie.",
    "%s applaudit.",
    "%s est surpris(e).",
    "%s est désorienté(e).",
    "%s se moque de toi.",
    "%s te fait une révérence.",
    "%s est vraiment triste.",
    "%s sourit.",
    "%s rit.",
    "%s dit \" "+lYes+" \".",
    "%s dit \" "+lNo+" \".",
    "%s dit \" "+lOK+" \".",
    ]

# Reverse lookup:  get the index from the name.
EmoteFuncDict = {
  "Signe de la main"   : 0,
  "Content(e)"  : 1,
  "Triste"    : 2,
  "En colère"  : 3,
  "Sommeil" : 4,
  "Haussement d'épaules"  : 5,
  "Danse"  : 6,
  "Clin d'œil"   : 7,
  "Ennuyé(e)"  : 8,
  "Applaudissements" : 9,
  "Surpris(e)" : 10,
  "Désorienté(e)"  : 11,
  "Moquerie"  : 12,
  "Révérence"    : 13,
  "Vraiment triste" : 14,
  "Grand sourire"    : 15,
  "Rire" : 16,
    lYes    : 17,
    lNo     : 18,
    lOK     : 19,
  }

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nNiveau %(level)s"

# SuitDialog.py
SuitBrushOffs = {
    'f':  ["Je suis en retard à un rendez-vous.",
           ],
    'p':  ["Dégage.",
           ],
    'ym': ['Béniouioui dit NON.',
           ],
    None: ["C'est mon jour de congé.",
           "Je crois que tu es dans le mauvais bureau.",
           "Dis à tes collaborateurs d'appeler les miens.",
           "Tu n'es pas en situation de me rencontrer.",
           "Parles-en à mon assistant."]
    }

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "Tu ne peux pas quitter le terrain de jeux tant que ton rigolmètre ne sourit pas!"

# InventoryNew.py
InventoryTotalGags = "Total des gags\n%d / %d"
InventoryDelete = "SUPPRIMER"
InventoryDone = "TERMINÉ"
InventoryDeleteHelp = "Clique sur un gag pour le SUPPRIMER."
InventorySkillCredit = "Crédit d'habileté : %s"
InventorySkillCreditNone = "Crédit d'habileté : Aucun"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Précision : %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryAffectsOneCog = "Affecte : Un "+ Cog
InventoryAffectsOneToon = "Affecte : Un Toon"
InventoryAffectsAllToons = "Affecte : Tous les Toons"
InventoryAffectsAllCogs = "Affecte : Tous les "+ Cogs
InventoryHealString = "Toonique"
InventoryDamageString = "Dommages"
InventoryBattleMenu = "MENU DU COMBAT"
InventoryRun = "COURIR"
InventorySOS = "SOS"
InventoryPass = "PASSER"
InventoryClickToAttack = "Clique sur\nun gag pour\nattaquer."

# NPCForceAcknowledge.py
#NPCForceAcknowledgeMessage = "Rend visite à " + Flippy + " pour obtenir ton premier DéfiToon avant de partir.\n\n\n\nTu peux trouver\n" + Flippy + " à l'intérieur de\nla Mairie de ToonTown."
NPCForceAcknowledgeMessage = "Tu dois faire un tour de tramway avant de partir.\n\n\n\n\nTu trouveras le tramway près de la boutique à gags de Dingo."
NPCForceAcknowledgeMessage2 = "Bien, tu as terminé ta recherche dans le tramway!\nVa voir le quartier général des Toons pour recevoir ta récompense.\n\n\n\n\n\nLe quartier général des Toons est situé près du centre du terrain de jeux."
NPCForceAcknowledgeMessage3 = "N'oublie pas de faire un tour de tramway.\n\n\n\nTu trouveras le tramway près de la boutique à gags de Dingo."
NPCForceAcknowledgeMessage4 = "Bravo! Tu as terminé ton premier défitoon!\n\n\n\n\nVa voir le quartier général des Toons pour recevoir ta récompense."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "Tu as reçu 1 point de lancer! Quand tu en auras 10, tu pourras recevoir un nouveau gag!"
MovieTutorialReward2 = "Tu as reçu 1 point d'éclaboussure! Quand tu en auras 10, tu pourras avoir un nouveau gag!"
MovieTutorialReward3 = "Bon travail! Tu as terminé ton premier défitoon!"
MovieTutorialReward4 = "Va chercher ta récompense au quartier général des Toons!"
MovieTutorialReward5 = "Amuse-toi!"

# ToontownBattleGlobals.py
BattleGlobalTracks = ['toonique', 'piège', 'leurre', 'tapage', 'lancer', 'éclaboussure', 'chute']
BattleGlobalNPCTracks = ['rechargement', 'Toons marquent', 'Cogs ratent']
BattleGlobalAvPropStrings = (
    ('Plume', 'Mégaphone', 'Tube de rouge à lèvres', 'Canne en bambou', 'Poussière de fée', 'Balles de jonglage'),
    ('Peau de banane', 'Râteau', 'Billes', 'Sable mouvant', 'Trappe', 'TNT'),
    ('Billet de 1 dollar', 'Petit aimant', 'Billet de 5 dollars', 'Gros aimant', 'Billet de 10 dollars', 'Lunettes hypnotiques'),
    ('Sonnette de vélo', 'Sifflet', 'Clairon', 'Klaxon', "Trompe d'éléphant", 'Corne de brume'),
    ('Petit gâteau', 'Tranche de tarte aux fruits', 'Tranche de tarte à la crème', 'Tarte aux fruits entière', 'Tarte à la crème entière', "Gâteau d'anniversaire"),
    ('Fleur à éclabousser', "Verre d'eau", 'Pistolet à eau', "Bouteille d'eau gazeuse", "Lance d'incendie", "Nuage d'orage"),
    ('Pot de fleurs', 'Sac de sable', 'Enclume', 'Gros poids', 'Coffre-fort', 'Piano à queue')
    )
BattleGlobalAvPropStringsSingular = (
    ('une plume', 'un mégaphone', 'un tube de rouge à lèvres', 'une canne en bambou', 'de la poussière de fée', 'un jeu de balles de jonglage'),
    ('une peau de banane', 'un râteau', 'un jeu de billes', 'un peu de sable mouvant', 'une trappe', 'du TNT'),
    ('un billet de 1 dollar', 'un petit aimant', 'un billet de 5 dollars', 'un gros aimant', 'un billet de 10 dollars', 'une paire de lunettes hypnotiques'),
    ('une sonnette de vélo', 'un sifflet', 'un clairon', 'un klaxon', "une trompe d'éléphant", 'une corne de brume'),
    ('un petit gâteau', 'une tranche de tarte aux fruits', 'une tranche de tarte à la crème', 'une tarte aux fruits entière', 'une tarte à la crème entière', "un gâteau d'anniversaire"),
    ('une fleur à éclabousser', "un verre d'eau", 'un pistolet à eau', "une bouteille d'eau gazeuse", "une lance d'incendie", "un nuage d'orage"),
    ('un pot de fleurs', 'un sac de sable', 'une enclume', 'un gros poids', 'un coffre-fort', 'un piano à queue')
    )
BattleGlobalAvPropStringsPlural = (
    ('Plumes', 'Mégaphones', 'Tubes de rouge à lèvres', 'Cannes en bambou', 'Poussières de fée', 'jeux de balles de jonglage'),
    ('Peaux de bananes', 'Râteaux', 'jeux de billes', 'morceaux de sable mouvant', 'Trappes','bâtons de TNT'),
    ('Billets de 1 dollar', 'Petits aimants', 'Billets de 5 dollars', 'Gros aimants','Billets de 10 dollars', 'Paires de lunettes hypnotiques'),
    ('Sonnettes de vélo', 'Sifflets', 'Clairons', 'Klaxons', "Trompes d'éléphants", 'Cornes de brume'),
    ('Petits gâteaux', 'Tranches de tarte aux fruits', 'Tranches de tarte à la crème','Tartes aux fruits entières', 'Tartes à la crème entières', "Gâteaux d'anniversaire"),
    ('Fleurs à éclabousser', "Verres d'eau", 'Pistolets à eau',"Bouteilles d'eau gazeuse", "Lances d'incendie", "Nuages d'orage"),
    ('Pots de fleurs', 'Sacs de sable', 'Enclumes', 'Gros poids', 'Coffres-forts','Pianos à queue')
    )
BattleGlobalAvTrackAccStrings = ("Moyen", "Parfait", "Faible", "Fort", "Moyen", "Fort", "Faible")

AttackMissed = "RATÉ"

NPCCallButtonLabel = 'APPEL'

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("vers la", "sur la",  "terrasse du Tourbillon"), # Tutorial
    1000  : ("vers le", "sur le",  "Terrain de jeux"),
    1100  : ("vers le", "sur le",  "Boulevard de la Bernache"),
    1200  : ("vers la", "sur la",  "Rue des Récifs"),
    1300  : ("vers l'", "sur l'",  "Allée des Marées"),
    2000  : ("vers le", "sur le",  "Terrain de jeux"),
    2100  : ("vers la", "sur la",  "Rue Béta"),
    2200  : ("vers l'", "sur l'",  "Avenue des Fondus"),
    2300  : ("vers la", "sur la",  "Place des Blagues"),
    3000  : ("vers le", "sur le",  "Terrain de jeux"),
    3100  : ("vers le", "sur le",  "Chemin du Marin"),
    3200  : ("vers la", "sur la",  "Rue de la Neige fondue"),
    4000  : ("vers le", "sur le",  "Terrain de jeux"),
    4100  : ("vers l'", "sur l'",  "Avenue du Contralto "),
    4200  : ("vers le", "sur le",  "Boulevard du Baryton "),
    4300  : ("vers la", "sur la",  "Terrasse des Ténors"),
    5000  : ("vers le", "sur le",  "Terrain de jeux"),
    5100  : ("vers la", "sur la",  "Rue des Ormes"),
    5200  : ("vers la", "sur la",  "Rue des Érables"),
    5300  : ("vers la", "sur la",  "Rue du Chêne"),
    9000  : ("vers le", "sur le",  "Terrain de jeux"),
    9100  : ("vers le", "sur le",  "Boulevard de la Berceuse"),
    10000 : ("vers le", "au",      "QG Chefbot"),
    10100 : ("vers le", "dans le", "hall du QG des Chefbots"),
    11000 : ("vers la", "sur la",  "cour du QG Chefbot"),
    11100 : ("vers le", "dans le", "hall du QG Vendibot"),
    11200 : ("vers l'", "à l'",   "usine Vendibot"),
    11500 : ("vers l'", "à l'",   "usine Vendibot"),
    12000 : ("vers le", "au",      "QG Caissbot"),
    12100 : ("vers le", "dans le", "hall du QG Caissbot"),
    13000 : ("vers le", "au",      "QG Loibot"),
    13100 : ("vers le", "dans le", "hall du QG Loibot"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("vers les", "sur les", lDonaldsDock)
ToontownCentral   = ("vers",     "à",      lToontownCentral)
TheBrrrgh         = ("vers",     "dans",    "le %s" % lTheBrrrgh)
MinniesMelodyland = ("vers le",  "au",      lMinniesMelodyland)
DaisyGardens      = ("vers les", "au",      lDaisyGardens)
ConstructionZone  = ("vers la",  "dans la", "Zone de construction")
FunnyFarm         = ("vers la",  "dans la", "Ferme farfelue")
GoofyStadium      = ("vers le",  "au",      "Stade Dingo")
DonaldsDreamland  = ("vers le",  "au",      lDonaldsDreamland)
BossbotHQ         = ("vers le",  "dans le", "QG des Chefbots")
SellbotHQ         = ("vers le",  "dans le", "QG Vendibot")
CashbotHQ         = ("vers le",  "dans le", "QG Caissbot")
LawbotHQ          = ("vers le",  "dans le", "QG Loibot")
Tutorial          = ("vers les", "aux",     "Travaux pratiques")
MyEstate          = ("vers",     "dans",    "ta maison")
WelcomeValley     = ("vers la",  "dans la", "Bienvenue")

Factory = 'Usine'
Headquarters = 'Quartiers généraux'
SellbotFrontEntrance = 'Entrée principale'
SellbotSideEntrance = 'Entrée latérale'

FactoryNames = {
    0 : "Maquette d'usine",
    11500 : 'Usine des Cogs Vendibots',
    }

FactoryTypeLeg = 'Jambe'
FactoryTypeArm = 'Bras'
FactoryTypeTorso = 'Torse'

# ToontownLoader.py
LoaderLabel = "Chargement..."

# PlayGame.py
HeadingToHood = "En direction %(to)s %(hood)s... " # hood name
HeadingToYourEstate = "En direction de ta propriété..."
HeadingToEstate = "En direction de la propriété de %s..."  # avatar name
HeadingToFriend = "En direction de la propriété de l'ami(e) de %s..."  # avatar name

# Hood.py
HeadingToPlayground = "En direction du terrain de jeux..."
HeadingToStreet = "En direction %(to)s %(street)s... " # Street name

# ToontownDialog.py
ToontownDialogOK = lOK
ToontownDialogCancel = lCancel
ToontownDialogYes = lYes
ToontownDialogNo = lNo

# TownBattle.py
TownBattleRun = "Revenir en courant au terrain de jeux?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "QUEL TOON?"
TownBattleChooseAvatarCogTitle = "QUEL "+ string.upper(Cog) +"?"
TownBattleChooseAvatarBack = "RETOUR"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "Pas d'amis à appeler!"
TownBattleSOSWhichFriend = "Appeler quel(le) ami(e)?"
TownBattleSOSNPCFriends = "Toons sauvés"
TownBattleSOSBack = "RETOUR"

# TownBattleToonPanel.py
TownBattleToonSOS = "SOS"
TownBattleUndecided = "?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "En attente des\nautres joueurs..."
TownSoloBattleWaitTitle = "Patiente..."
TownBattleWaitBack = "RETOUR"

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
FishingFailureAutoReel = "Le moulinet automatique n'a pas fonctionné cette fois-ci. Tourne la manivelle à la main, juste à la bonne vitesse, pour avoir les meilleures chances d'attraper quelque chose!"
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
FishPokerFullHouse = "Full"
FishPoker3OfKind = "Brelan"
FishPoker2Pair = "2 paires"
FishPokerPair = "Paire"

# DistributedTutorial.py
TutorialGreeting1 = "Salut, %s!"
TutorialGreeting2 = "Salut, %s!\nViens par ici!"
TutorialGreeting3 = "Salut, %s!\nViens par ici!\nUtilise les flèches!"
TutorialMickeyWelcome = "Bienvenue à Toontown!"
TutorialFlippyIntro = "Je te présente mon ami %s..." % Flippy
TutorialFlippyHi = "Salut, %s!"
TutorialQT1 = "Tu peux parler en utilisant ceci."
TutorialQT2 = "Tu peux parler en utilisant ceci.\nClique dessus, puis choisis \" Salut \"."
TutorialChat1 = "Tu peux parler en utilisant l'un de ces boutons."
TutorialChat2 = "Le bouton bleu te permet de chatter avec le clavier."
TutorialChat3 = "Fais attention! La plupart des autres joueurs ne comprendront pas ce que tu dis lorsque tu utilises le clavier."
TutorialChat4 = "Le bouton vert ouvre le %s."
TutorialChat5 = "Tout le monde peut te comprendre si tu utilises le %s."
TutorialChat6 = "Essaie de dire \" salut \"."
TutorialBodyClick1 = "Très bien!"
TutorialBodyClick2 = "Ravi de t'avoir rencontré! Tu veux que nous soyons amis?"
TutorialBodyClick3 = "Pour devenir ami(e) avec %s, clique sur lui..." % Flippy
TutorialHandleBodyClickSuccess = "Bon travail!"
TutorialHandleBodyClickFail = "Ce n'est pas ça. Essaie de cliquer juste sur " + Flippy + "..."
TutorialFriendsButton = "Maintenant, clique sur le bouton \" amis \" sous l'image de " + Flippy + " dans l'angle droit."
TutorialHandleFriendsButton = "Ensuite, clique sur le bouton \" oui \"."
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = "Veux-tu devenir ami(e) avec " + Flippy + "?"
TutorialFriendsPanelMickeyChat = Flippy + " veut bien être ton ami. Clique sur \" "+lOK+" \" pour terminer." 
TutorialFriendsPanelYes = Flippy + " a dit oui!" 
TutorialFriendsPanelNo = "Ça n'est pas très gentil!"
TutorialFriendsPanelCongrats = "Bravo! Tu t'es fait ton premier ami."
TutorialFlippyChat1 = "Reviens me voir quand tu seras prêt pour ton premier défitoon!"
TutorialFlippyChat2 = "Je serai à la Mairie de Toontown!"
TutorialAllFriendsButton = "Tu peux voir tous tes amis en cliquant sur le bouton \" amis \". Essaye donc..."
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

# SpeedChat

# Used several places in the game. Defined globally because
# we keep changing the name
GlobalSpeedChatName = "Chat rapide"

SCMenuEmotions  = "ÉMOTIONS"
SCMenuCustom    = "MES EXPRESSIONS"
SCMenuCog       = "COGGERIES"
SCMenuHello     = "SALUT"
SCMenuBye       = "AU REVOIR"
SCMenuHappy     = "JOYEUX"
SCMenuSad       = "TRISTE"
SCMenuFriendly  = "AMICAL"
SCMenuSorry     = "DÉSOLÉ"
SCMenuStinky    = "DÉSAGRÉABLE"
SCMenuPlaces    = "ENDROITS"
SCMenuToontasks = "DÉFITOONS"
SCMenuBattle    = "COMBAT"
SCMenuGagShop   = "BOUTIQUE À GAGS"
SCMenuFactory   = "USINE"
SCMenuFactoryMeet = "RENCONTRE"
SCMenuFriendlyYou                = "Toi..."
SCMenuFriendlyILike              = "J'aime bien..."
SCMenuPlacesLetsGo               = "Allons..."
SCMenuToontasksMyTasks           = "MES DÉFITOONS"
SCMenuToontasksYouShouldChoose   = "Je crois que tu devrais choisir..."
SCMenuBattleLetsUse              = "Utilisons..."

# These are all the standard SpeedChat phrases.
# The indices must fit into 16 bits (0..65535)
SpeedChatStaticText = {
    # top-level
    1 : lYes,
    2 : lNo,
    3 : lOK,

    # Hello
    100 : "Salut!",
    101 : "Bonjour!",
    102 : "Salut la compagnie!",
    103 : "Hé!",
    104 : "Coucou!",
    105 : "Salut tout le monde!",
    106 : "Bienvenue à Toontown!",
    107 : "Quoi de neuf?",
    108 : "Comment ça va?",
    109 : "Bonjour?",

    # Bye
    200 : "Au revoir!",
    201 : "À plus!",
    202 : "À la prochaine!",
    203 : "Bonne journée!",
    204 : "Amuse-toi!",
    205 : "Bonne chance!",
    206 : "Je reviens tout de suite.",
    207 : "Je dois m'en aller.",

    # Happy
    300 : ":-)",
    301 : "Haa!",
    302 : "Hourra!",
    303 : "Sympa!",
    304 : "Youhouu!",
    305 : "Ouais!",
    306 : "Ha ha!",
    307 : "Hi hi!",
    308 : "Oh là là!",
    309 : "Super!",
    310 : "Ouii!",
    311 : "Bon sang!",
    312 : "Youpi!",
    313 : "Génial!",
    314 : "Hop-là!",
    315 : "Toontastique!",

    # Sad
    400 : ":-(",
    401 : "Oh non!",
    402 : "Oh oh!",
    403 : "Zut!",
    404 : "Mince!",
    405 : "Aïe!",
    406 : "Ffff!",
    407 : "Non!!!",
    408 : "Aïe aïe aïe!",
    409 : "Eh?",
    410 : "J'ai besoin de plus de rigolpoints.",

    # Friendly
    500 : "Merci!",
    501 : "De rien.",
    502 : "Je t'en prie!",
    503 : "Quand tu veux!",
    504 : "Non merci.",
    505 : "Bon travail d'équipe!",
    506 : "C'était amusant!",
    507 : "Sois mon ami(e) s'il te plaît.",
    508 : "Travaillons ensemble!",
    509 : "Vous êtes super les copains!",
    510 : "Tu viens d'arriver par ici?",
    511 : "Tu as gagné?",
    512 : "Je crois que c'est trop risqué pour toi.",
    513 : "Tu veux de l'aide?",
    514 : "Peux-tu m'aider?",

    # Friendly "Toi..."
    600 : "Tu as un air gentil.",
    601 : "Tu es adorable!",
    602 : "Tu es d'enfer!",
    603 : "Tu es un génie!",

    # Friendly "J'aime bien..."
    700 : "J'aime bien ton nom.",
    701 : "J'aime bien ton look.",
    702 : "J'aime bien ta chemise.",
    703 : "J'aime bien ta jupe.",
    704 : "J'aime bien ton short.",
    705 : "J'aime bien ce jeu!",

    # Sorry
    800 : "Désolé(e)!",
    801 : "Aïe!",
    802 : "Désolé(e), je suis occupé à combattre les Cogs!",
    803 : "Désolé(e), je suis occupé à trouver des bonbons!",
    804 : "Désolé(e), je suis occupé à terminer un défitoon!",
    805 : "Désolé(e), j'ai dû partir à l'improviste.",
    806 : "Désolé(e), j'ai été retardé.",
    807 : "Désolé(e), je ne peux pas.",
    808 : "Je ne pouvais plus attendre.",
    809 : "Je ne te comprends pas.",
    810 : "Utilise le %s." % GlobalSpeedChatName,

    # Stinky
    900 : "Hé!",
    901 : "S'il te plaît va t'en!",
    902 : "Arrête ça!",
    903 : "Ce n'était pas gentil!",
    904 : "Ne sois pas méchant!",
    905 : "Tu es nul!",
    906 : "Envoie un rapport d'erreur.",
    907 : "Je suis en panne.",

    # Places
    1000 : "Allons-y!",
    1001 : "Peux-tu me téléporter?",
    1002 : "On y va?",
    1003 : "Où devons-nous aller?",
    1004 : "Par quel chemin?",
    1005 : "Par là.",
    1006 : "Suis-moi.",
    1007 : "Attends-moi!",
    1008 : "Attendons mon ami(e).",
    1009 : "Trouvons d'autres Toons.",
    1010 : "Attends ici.",
    1011 : "Attends une minute.",
    1012 : "Retrouvons-nous ici.",
    1013 : "Peux-tu venir chez moi?",

    # Places "Allons-y..."
    1100 : "Allons faire un tour de tramway!",
    1101 : "Retournons au terrain de jeux!",
    1102 : "Allons combattre les %s!" % Cogs,
    1103 : "Allons reprendre un bâtiment %s!" % Cog,
    1104 : "Allons dans l'ascenseur!",
    1105 : "Allons à "+lToontownCentral+"!",
    1106 : "Allons aux "+lDonaldsDockNC+"!",
    1107 : "Allons au "+lMinniesMelodyland+"!",
    1108 : "Allons au "+lDaisyGardensNC+"!",
    1109 : "Allons au "+lTheBrrrgh+"!",
    1110 : "Allons au "+lDonaldsDreamland+"!",
    1111 : "Allons chez moi!",

    # Toontasks
    1200 : "Sur quel défitoon est-ce que tu travailles?",
    1201 : "Travaillons là-dessus.",
    1202 : "Ce n'est pas ce que je cherche.",
    1203 : "Je vais chercher ça.",
    1204 : "Ce n'est pas dans cette rue.",
    1205 : "Je ne l'ai pas encore trouvé.",
    1299 : "Je dois avoir un défitoon.",

    # Toontasks "Je crois que tu devrais choisir..."
    1300 : "Je crois que tu devrais choisir Toonique.",
    1301 : "Je crois que tu devrais choisir Tapage.",
    1302 : "Je crois que tu devrais choisir Chute.",
    1303 : "Je crois que tu devrais choisir Piégeage.",
    1304 : "Je crois que tu devrais choisir Leurre.",

    # Battle
    1400 : "Dépêche-toi!",
    1401 : "Joli coup!",
    1402 : "Gag sympa!",
    1403 : "Manqué!",
    1404 : "Tu as réussi!",
    1405 : "On a réussi!",
    1406 : "Amène ça!",
    1407 : "Du gâteau!",
    1408 : "C'était facile!",
    1409 : "Cours!",
    1410 : "À l'aide!",
    1411 : "Ouf!",
    1412 : "On a des ennuis.",
    1413 : "J'ai besoin de plus de gags.",
    1414 : "J'ai besoin d'un Toonique.",
    1415 : "Tu devrais passer",

    # Battle "Utilisons..."
    1500 : "Utilisons un toonique!",
    1501 : "Utilisons un piège!",
    1502 : "Utilisons un leurre!",
    1503 : "Utilisons un tapage!",
    1504 : "Lançons quelque chose!",
    1505 : "Utilisons une éclaboussure!",
    1506 : "Utilisons une chute!",

    # Gag Shop
    1600 : "J'ai assez de gags.",
    1601 : "J'ai besoin de plus de bonbons.",
    1602 : "Moi aussi.",
    1603 : "Dépêche-toi!",
    1604 : "Un de plus?",
    1605 : "Rejouer?",
    1606 : "Jouons encore.",

    # Factory
    1700 : "Séparons-nous.",
    1701 : "Restons ensemble!",
    1702 : "Allons vaincre les Cogs.",
    1703 : "Marche sur le sélecteur.",
    1704 : "Passe par la porte.",

    # Sellbot Factory
    1803 : "Je suis dans l'entrée principale.",
    1804 : "Je suis dans le hall.",
    1805 : "Je suis dans le couloir devant le hall.",
    1806 : "Je suis dans le couloir devant le hall.",
    1807 : "Je suis dans la salle des pignons.",
    1808 : "Je suis dans la chaufferie.",
    1809 : "Je suis sur la passerelle est.",
    1810 : "Je suis dans le mélangeur à peinture.",
    1811 : "Je suis dans la réserve du mélangeur à peinture.",
    1812 : "Je suis sur la passerelle ouest.",
    1813 : "Je suis dans la salle des tuyaux.",
    1814 : "Je suis dans l'escalier qui mène à la salle des tuyaux.",
    1815 : "Je suis dans la salle des canalisations.",
    1816 : "Je suis dans l'entrée latérale.",
    1817 : "Je suis dans l'allée des pas perdus.",
    1818 : "Je suis à l'extérieur des sanitaires.",
    1819 : "Je suis dans les sanitaires.",
    1820 : "Je suis dans la réserve des sanitaires.",
    1821 : "Je suis sur la passerelle ouest.",
    1822 : "Je suis dans la salle du pétrole.",
    1823 : "Je suis au poste d'observation de la réserve.",
    1824 : "Je suis dans la réserve.",
    1825 : "Je suis devant le mélangeur à peinture.",
    1827 : "Je suis devant la salle du pétrole.",
    1830 : "Je suis dans la salle de contrôle du silo est.",
    1831 : "Je suis dans la salle de contrôle du silo ouest.",
    1832 : "Je suis dans la salle de contrôle du silo central.",
    1833 : "Je suis au silo est.",
    1834 : "Je suis au silo ouest.",
    1835 : "Je suis au silo central.",
    1836 : "Je suis au silo ouest.",
    1837 : "Je suis au silo est.",
    1838 : "Je suis sur la passerelle du silo est.",
    1840 : "Je suis en haut du silo ouest.",
    1841 : "Je suis en haut du silo est.",
    1860 : "Je suis dans l'ascenseur du silo ouest.",
    1861 : "Je suis dans l'ascenseur du silo est.",
    # Sellbot Factory continued
    1903 : "Retrouvons-nous à l'entrée principale.",
    1904 : "Retrouvons-nous dans le hall.",
    1905 : "Retrouvons-nous dans le couloir devant le hall.",
    1906 : "Retrouvons-nous dans le couloir devant le hall.",
    1907 : "Retrouvons-nous dans la salle des pignons.",
    1908 : "Retrouvons-nous dans la chaufferie.",
    1909 : "Retrouvons-nous sur la passerelle est.",
    1910 : "Retrouvons-nous au mélangeur à peinture.",
    1911 : "Retrouvons-nous dans la réserve du mélangeur à peinture.",
    1912 : "Retrouvons-nous sur la passerelle du silo ouest.",
    1913 : "Retrouvons-nous dans la salle des tuyaux.",
    1914 : "Retrouvons-nous dans l'escalier qui mène à la salle des tuyaux.",
    1915 : "Retrouvons-nous dans la salle des canalisations.",
    1916 : "Retrouvons-nous à l'entrée latérale.",
    1917 : "Retrouvons-nous dans l'allée des pas perdus.",
    1918 : "Retrouvons-nous devant les sanitaires.",
    1919 : "Retrouvons-nous dans les sanitaires.",
    1920 : "Retrouvons-nous dans la réserve des sanitaires.",
    1921 : "Retrouvons-nous sur la passerelle ouest.",
    1922 : "Retrouvons-nous dans la salle du pétrole.",
    1923 : "Retrouvons-nous au poste d'observation de la réserve.",
    1924 : "Retrouvons-nous dans la réserve.",
    1925 : "Retrouvons-nous devant le mélangeur à peinture.",
    1927 : "Retrouvons-nous devant la salle du pétrole.",
    1930 : "Retrouvons-nous dans la salle de contrôle du silo est.",
    1931 : "Retrouvons-nous dans la salle de contrôle du silo ouest.",
    1932 : "Retrouvons-nous dans la salle de contrôle du silo central.",
    1933 : "Retrouvons-nous au silo est.",
    1934 : "Retrouvons-nous au silo ouest.",
    1935 : "Retrouvons-nous au silo central.",
    1936 : "Retrouvons-nous au silo ouest.",
    1937 : "Retrouvons-nous au silo est.",
    1938 : "Retrouvons-nous sur la passerelle du silo est.",
    1940 : "Retrouvons-nous en haut du silo ouest.",
    1941 : "Retrouvons-nous en haut du silo est.",
    1960 : "Retrouvons-nous dans l'ascenseur du silo ouest.",
    1961 : "Retrouvons-nous dans l'ascenseur du silo est.",

    # These are used only for the style settings in the OptionsPage
    # These should never actually be spoken or listed on the real speed chat
    2000 : "Violet",
    2001 : "Bleu",
    2002 : "Cyan",
    2003 : "Bleu-gris",
    2004 : "Vert",
    2005 : "Jaune",
    2006 : "Orange",
    2007 : "Rouge",
    2008 : "Rose",
    2009 : "Brun",

    # cog phrases for disguised toons
    # (just references to cog dialog above)

    # common cog phrases
    20000 : SuitBrushOffs[None][0],
    20001 : SuitBrushOffs[None][1],
    20002 : SuitBrushOffs[None][2],
    20003 : SuitBrushOffs[None][3],
    20004 : SuitBrushOffs[None][4],

    # specific cog phrases
    20005: SuitFaceoffTaunts['bf'][0],
    20006: SuitFaceoffTaunts['bf'][1],
    20007: SuitFaceoffTaunts['bf'][2],
    20008: SuitFaceoffTaunts['bf'][3],
    20009: SuitFaceoffTaunts['bf'][4],
    20010: SuitFaceoffTaunts['bf'][5],
    20011: SuitFaceoffTaunts['bf'][6],
    20012: SuitFaceoffTaunts['bf'][7],
    20013: SuitFaceoffTaunts['bf'][8],
    20014: SuitFaceoffTaunts['bf'][9],

    20015: SuitFaceoffTaunts['nc'][0],
    20016: SuitFaceoffTaunts['nc'][1],
    20017: SuitFaceoffTaunts['nc'][2],
    20018: SuitFaceoffTaunts['nc'][3],
    20019: SuitFaceoffTaunts['nc'][4],
    20020: SuitFaceoffTaunts['nc'][5],
    20021: SuitFaceoffTaunts['nc'][6],
    20022: SuitFaceoffTaunts['nc'][7],
    20023: SuitFaceoffTaunts['nc'][8],
    20024: SuitFaceoffTaunts['nc'][9],

    20025: SuitFaceoffTaunts['ym'][0],
    20026: SuitFaceoffTaunts['ym'][1],
    20027: SuitFaceoffTaunts['ym'][2],
    20028: SuitFaceoffTaunts['ym'][3],
    20029: SuitFaceoffTaunts['ym'][4],
    20030: SuitFaceoffTaunts['ym'][5],
    20031: SuitFaceoffTaunts['ym'][6],
    20032: SuitFaceoffTaunts['ym'][7],
    20033: SuitFaceoffTaunts['ym'][8],
    20034: SuitFaceoffTaunts['ym'][9],
    20035: SuitFaceoffTaunts['ym'][10],

    20036: SuitFaceoffTaunts['ms'][0],
    20037: SuitFaceoffTaunts['ms'][1],
    20038: SuitFaceoffTaunts['ms'][2],
    20039: SuitFaceoffTaunts['ms'][3],
    20040: SuitFaceoffTaunts['ms'][4],
    20041: SuitFaceoffTaunts['ms'][5],
    20042: SuitFaceoffTaunts['ms'][6],
    20043: SuitFaceoffTaunts['ms'][7],
    20044: SuitFaceoffTaunts['ms'][8],
    20045: SuitFaceoffTaunts['ms'][9],
    20046: SuitFaceoffTaunts['ms'][10],

    20047: SuitFaceoffTaunts['bc'][0],
    20048: SuitFaceoffTaunts['bc'][1],
    20049: SuitFaceoffTaunts['bc'][2],
    20050: SuitFaceoffTaunts['bc'][3],
    20051: SuitFaceoffTaunts['bc'][4],
    20052: SuitFaceoffTaunts['bc'][5],
    20053: SuitFaceoffTaunts['bc'][6],
    20054: SuitFaceoffTaunts['bc'][7],
    20055: SuitFaceoffTaunts['bc'][8],
    20056: SuitFaceoffTaunts['bc'][9],
    20057: SuitFaceoffTaunts['bc'][10],

    20058: SuitFaceoffTaunts['cc'][0],
    20059: SuitFaceoffTaunts['cc'][1],
    20060: SuitFaceoffTaunts['cc'][2],
    20061: SuitFaceoffTaunts['cc'][3],
    20062: SuitFaceoffTaunts['cc'][4],
    20063: SuitFaceoffTaunts['cc'][5],
    20064: SuitFaceoffTaunts['cc'][6],
    20065: SuitFaceoffTaunts['cc'][7],
    20066: SuitFaceoffTaunts['cc'][8],
    20067: SuitFaceoffTaunts['cc'][9],
    20068: SuitFaceoffTaunts['cc'][10],
    20069: SuitFaceoffTaunts['cc'][11],
    20070: SuitFaceoffTaunts['cc'][12],

    20071: SuitFaceoffTaunts['nd'][0],
    20072: SuitFaceoffTaunts['nd'][1],
    20073: SuitFaceoffTaunts['nd'][2],
    20074: SuitFaceoffTaunts['nd'][3],
    20075: SuitFaceoffTaunts['nd'][4],
    20076: SuitFaceoffTaunts['nd'][5],
    20077: SuitFaceoffTaunts['nd'][6],
    20078: SuitFaceoffTaunts['nd'][7],
    20079: SuitFaceoffTaunts['nd'][8],
    20080: SuitFaceoffTaunts['nd'][9],

    20081: SuitFaceoffTaunts['ac'][0],
    20082: SuitFaceoffTaunts['ac'][1],
    20083: SuitFaceoffTaunts['ac'][2],
    20084: SuitFaceoffTaunts['ac'][3],
    20085: SuitFaceoffTaunts['ac'][4],
    20086: SuitFaceoffTaunts['ac'][5],
    20087: SuitFaceoffTaunts['ac'][6],
    20088: SuitFaceoffTaunts['ac'][7],
    20089: SuitFaceoffTaunts['ac'][8],
    20090: SuitFaceoffTaunts['ac'][9],
    20091: SuitFaceoffTaunts['ac'][10],
    20092: SuitFaceoffTaunts['ac'][11],

    20093: SuitFaceoffTaunts['tf'][0],
    20094: SuitFaceoffTaunts['tf'][1],
    20095: SuitFaceoffTaunts['tf'][2],
    20096: SuitFaceoffTaunts['tf'][3],
    20097: SuitFaceoffTaunts['tf'][4],
    20098: SuitFaceoffTaunts['tf'][5],
    20099: SuitFaceoffTaunts['tf'][6],
    20100: SuitFaceoffTaunts['tf'][7],
    20101: SuitFaceoffTaunts['tf'][8],
    20102: SuitFaceoffTaunts['tf'][9],
    20103: SuitFaceoffTaunts['tf'][10],

    20104: SuitFaceoffTaunts['hh'][0],
    20105: SuitFaceoffTaunts['hh'][1],
    20106: SuitFaceoffTaunts['hh'][2],
    20107: SuitFaceoffTaunts['hh'][3],
    20108: SuitFaceoffTaunts['hh'][4],
    20109: SuitFaceoffTaunts['hh'][5],
    20110: SuitFaceoffTaunts['hh'][6],
    20111: SuitFaceoffTaunts['hh'][7],
    20112: SuitFaceoffTaunts['hh'][8],
    20113: SuitFaceoffTaunts['hh'][9],
    20114: SuitFaceoffTaunts['hh'][10],

    20115: SuitFaceoffTaunts['le'][0],
    20116: SuitFaceoffTaunts['le'][1],
    20117: SuitFaceoffTaunts['le'][2],
    20118: SuitFaceoffTaunts['le'][3],
    20119: SuitFaceoffTaunts['le'][4],
    20120: SuitFaceoffTaunts['le'][5],
    20121: SuitFaceoffTaunts['le'][6],
    20122: SuitFaceoffTaunts['le'][7],
    20123: SuitFaceoffTaunts['le'][8],
    20124: SuitFaceoffTaunts['le'][9],

    20125: SuitFaceoffTaunts['bs'][0],
    20126: SuitFaceoffTaunts['bs'][1],
    20127: SuitFaceoffTaunts['bs'][2],
    20128: SuitFaceoffTaunts['bs'][3],
    20129: SuitFaceoffTaunts['bs'][4],
    20130: SuitFaceoffTaunts['bs'][5],
    20131: SuitFaceoffTaunts['bs'][6],
    20132: SuitFaceoffTaunts['bs'][7],
    20133: SuitFaceoffTaunts['bs'][8],
    20134: SuitFaceoffTaunts['bs'][9],
    20135: SuitFaceoffTaunts['bs'][10],

    20136: SuitFaceoffTaunts['cr'][0],
    20137: SuitFaceoffTaunts['cr'][1],
    20138: SuitFaceoffTaunts['cr'][2],
    20139: SuitFaceoffTaunts['cr'][3],
    20140: SuitFaceoffTaunts['cr'][4],
    20141: SuitFaceoffTaunts['cr'][5],
    20142: SuitFaceoffTaunts['cr'][6],
    20143: SuitFaceoffTaunts['cr'][7],
    20144: SuitFaceoffTaunts['cr'][8],
    20145: SuitFaceoffTaunts['cr'][9],

    20146: SuitFaceoffTaunts['tbc'][0],
    20147: SuitFaceoffTaunts['tbc'][1],
    20148: SuitFaceoffTaunts['tbc'][2],
    20149: SuitFaceoffTaunts['tbc'][3],
    20150: SuitFaceoffTaunts['tbc'][4],
    20151: SuitFaceoffTaunts['tbc'][5],
    20152: SuitFaceoffTaunts['tbc'][6],
    20153: SuitFaceoffTaunts['tbc'][7],
    20154: SuitFaceoffTaunts['tbc'][8],
    20155: SuitFaceoffTaunts['tbc'][9],
    20156: SuitFaceoffTaunts['tbc'][10],

    20157: SuitFaceoffTaunts['ds'][0],
    20158: SuitFaceoffTaunts['ds'][1],
    20159: SuitFaceoffTaunts['ds'][2],
    20160: SuitFaceoffTaunts['ds'][3],
    20161: SuitFaceoffTaunts['ds'][4],
    20162: SuitFaceoffTaunts['ds'][5],
    20163: SuitFaceoffTaunts['ds'][6],
    20164: SuitFaceoffTaunts['ds'][7],

    20165: SuitFaceoffTaunts['gh'][0],
    20166: SuitFaceoffTaunts['gh'][1],
    20167: SuitFaceoffTaunts['gh'][2],
    20168: SuitFaceoffTaunts['gh'][3],
    20169: SuitFaceoffTaunts['gh'][4],
    20170: SuitFaceoffTaunts['gh'][5],
    20171: SuitFaceoffTaunts['gh'][6],
    20172: SuitFaceoffTaunts['gh'][7],
    20173: SuitFaceoffTaunts['gh'][8],
    20174: SuitFaceoffTaunts['gh'][9],
    20175: SuitFaceoffTaunts['gh'][10],
    20176: SuitFaceoffTaunts['gh'][11],
    20177: SuitFaceoffTaunts['gh'][12],

    20178: SuitFaceoffTaunts['pp'][0],
    20179: SuitFaceoffTaunts['pp'][1],
    20180: SuitFaceoffTaunts['pp'][2],
    20181: SuitFaceoffTaunts['pp'][3],
    20182: SuitFaceoffTaunts['pp'][4],
    20183: SuitFaceoffTaunts['pp'][5],
    20184: SuitFaceoffTaunts['pp'][6],
    20185: SuitFaceoffTaunts['pp'][7],
    20186: SuitFaceoffTaunts['pp'][8],
    20187: SuitFaceoffTaunts['pp'][9],

    20188: SuitFaceoffTaunts['b'][0],
    20189: SuitFaceoffTaunts['b'][1],
    20190: SuitFaceoffTaunts['b'][2],
    20191: SuitFaceoffTaunts['b'][3],
    20192: SuitFaceoffTaunts['b'][4],
    20193: SuitFaceoffTaunts['b'][5],
    20194: SuitFaceoffTaunts['b'][6],
    20195: SuitFaceoffTaunts['b'][7],
    20196: SuitFaceoffTaunts['b'][8],
    20197: SuitFaceoffTaunts['b'][9],
    20198: SuitFaceoffTaunts['b'][10],
    20199: SuitFaceoffTaunts['b'][11],

    20200: SuitFaceoffTaunts['f'][0],
    20201: SuitFaceoffTaunts['f'][1],
    20202: SuitFaceoffTaunts['f'][2],
    20203: SuitFaceoffTaunts['f'][3],
    20204: SuitFaceoffTaunts['f'][4],
    20205: SuitFaceoffTaunts['f'][5],
    20206: SuitFaceoffTaunts['f'][6],
    20207: SuitFaceoffTaunts['f'][7],
    20208: SuitFaceoffTaunts['f'][8],
    20209: SuitFaceoffTaunts['f'][9],
    20210: SuitFaceoffTaunts['f'][10],

    20211: SuitFaceoffTaunts['mm'][0],
    20212: SuitFaceoffTaunts['mm'][1],
    20213: SuitFaceoffTaunts['mm'][2],
    20214: SuitFaceoffTaunts['mm'][3],
    20215: SuitFaceoffTaunts['mm'][4],
    20216: SuitFaceoffTaunts['mm'][5],
    20217: SuitFaceoffTaunts['mm'][6],
    20218: SuitFaceoffTaunts['mm'][7],
    20219: SuitFaceoffTaunts['mm'][8],
    20220: SuitFaceoffTaunts['mm'][9],
    20221: SuitFaceoffTaunts['mm'][10],
    20222: SuitFaceoffTaunts['mm'][11],
    20223: SuitFaceoffTaunts['mm'][12],
    20224: SuitFaceoffTaunts['mm'][13],

    20225: SuitFaceoffTaunts['tw'][0],
    20226: SuitFaceoffTaunts['tw'][1],
    20227: SuitFaceoffTaunts['tw'][2],
    20228: SuitFaceoffTaunts['tw'][3],
    20229: SuitFaceoffTaunts['tw'][4],
    20230: SuitFaceoffTaunts['tw'][5],
    20231: SuitFaceoffTaunts['tw'][6],
    20232: SuitFaceoffTaunts['tw'][7],
    20233: SuitFaceoffTaunts['tw'][8],
    20234: SuitFaceoffTaunts['tw'][9],
    20235: SuitFaceoffTaunts['tw'][10],

    20236: SuitFaceoffTaunts['mb'][0],
    20237: SuitFaceoffTaunts['mb'][1],
    20238: SuitFaceoffTaunts['mb'][2],
    20239: SuitFaceoffTaunts['mb'][3],
    20240: SuitFaceoffTaunts['mb'][4],
    20241: SuitFaceoffTaunts['mb'][5],
    20242: SuitFaceoffTaunts['mb'][6],
    20243: SuitFaceoffTaunts['mb'][7],
    20244: SuitFaceoffTaunts['mb'][8],
    20245: SuitFaceoffTaunts['mb'][9],

    20246: SuitFaceoffTaunts['m'][0],
    20247: SuitFaceoffTaunts['m'][1],
    20248: SuitFaceoffTaunts['m'][2],
    20249: SuitFaceoffTaunts['m'][3],
    20250: SuitFaceoffTaunts['m'][4],
    20251: SuitFaceoffTaunts['m'][5],
    20252: SuitFaceoffTaunts['m'][6],
    20253: SuitFaceoffTaunts['m'][7],
    20254: SuitFaceoffTaunts['m'][8],

    20255: SuitFaceoffTaunts['mh'][0],
    20256: SuitFaceoffTaunts['mh'][1],
    20257: SuitFaceoffTaunts['mh'][2],
    20258: SuitFaceoffTaunts['mh'][3],
    20259: SuitFaceoffTaunts['mh'][4],
    20260: SuitFaceoffTaunts['mh'][5],
    20261: SuitFaceoffTaunts['mh'][6],
    20262: SuitFaceoffTaunts['mh'][7],
    20263: SuitFaceoffTaunts['mh'][8],
    20264: SuitFaceoffTaunts['mh'][9],
    20265: SuitFaceoffTaunts['mh'][10],
    20266: SuitFaceoffTaunts['mh'][11],

    20267: SuitFaceoffTaunts['dt'][0],
    20268: SuitFaceoffTaunts['dt'][1],
    20269: SuitFaceoffTaunts['dt'][2],
    20270: SuitFaceoffTaunts['dt'][3],
    20271: SuitFaceoffTaunts['dt'][4],
    20272: SuitFaceoffTaunts['dt'][5],
    20273: SuitFaceoffTaunts['dt'][6],
    20274: SuitFaceoffTaunts['dt'][7],
    20275: SuitFaceoffTaunts['dt'][8],
    20276: SuitFaceoffTaunts['dt'][9],

    20277: SuitFaceoffTaunts['p'][0],
    20278: SuitFaceoffTaunts['p'][1],
    20279: SuitFaceoffTaunts['p'][2],
    20280: SuitFaceoffTaunts['p'][3],
    20281: SuitFaceoffTaunts['p'][4],
    20282: SuitFaceoffTaunts['p'][5],
    20283: SuitFaceoffTaunts['p'][6],
    20284: SuitFaceoffTaunts['p'][7],
    20285: SuitFaceoffTaunts['p'][8],
    20286: SuitFaceoffTaunts['p'][9],
    20287: SuitFaceoffTaunts['p'][10],

    20288: SuitFaceoffTaunts['tm'][0],
    20289: SuitFaceoffTaunts['tm'][1],
    20290: SuitFaceoffTaunts['tm'][2],
    20291: SuitFaceoffTaunts['tm'][3],
    20292: SuitFaceoffTaunts['tm'][4],
    20293: SuitFaceoffTaunts['tm'][5],
    20294: SuitFaceoffTaunts['tm'][6],
    20295: SuitFaceoffTaunts['tm'][7],
    20296: SuitFaceoffTaunts['tm'][8],
    20297: SuitFaceoffTaunts['tm'][9],
    20298: SuitFaceoffTaunts['tm'][10],

    20299: SuitFaceoffTaunts['bw'][0],
    20300: SuitFaceoffTaunts['bw'][1],
    20301: SuitFaceoffTaunts['bw'][2],
    20302: SuitFaceoffTaunts['bw'][3],
    20303: SuitFaceoffTaunts['bw'][4],
    20304: SuitFaceoffTaunts['bw'][5],
    20305: SuitFaceoffTaunts['bw'][6],
    20306: SuitFaceoffTaunts['bw'][7],
    20307: SuitFaceoffTaunts['bw'][8],
    20308: SuitFaceoffTaunts['bw'][9],

    20309: SuitFaceoffTaunts['ls'][0],
    20310: SuitFaceoffTaunts['ls'][1],
    20311: SuitFaceoffTaunts['ls'][2],
    20312: SuitFaceoffTaunts['ls'][3],
    20313: SuitFaceoffTaunts['ls'][4],
    20314: SuitFaceoffTaunts['ls'][5],
    20315: SuitFaceoffTaunts['ls'][6],
    20316: SuitFaceoffTaunts['ls'][7],
    20317: SuitFaceoffTaunts['ls'][8],
    20318: SuitFaceoffTaunts['ls'][9],
    20319: SuitFaceoffTaunts['ls'][10],

    20320: SuitFaceoffTaunts['rb'][0],
    20321: SuitFaceoffTaunts['rb'][1],
    20322: SuitFaceoffTaunts['rb'][2],
    20323: SuitFaceoffTaunts['rb'][3],
    20324: SuitFaceoffTaunts['rb'][4],
    20325: SuitFaceoffTaunts['rb'][5],
    20326: SuitFaceoffTaunts['rb'][6],
    20327: SuitFaceoffTaunts['rb'][7],
    20328: SuitFaceoffTaunts['rb'][8],
    20329: SuitFaceoffTaunts['rb'][9],

    20330: SuitFaceoffTaunts['sc'][0],
    20331: SuitFaceoffTaunts['sc'][1],
    20332: SuitFaceoffTaunts['sc'][2],
    20333: SuitFaceoffTaunts['sc'][3],
    20334: SuitFaceoffTaunts['sc'][4],
    20335: SuitFaceoffTaunts['sc'][5],
    20336: SuitFaceoffTaunts['sc'][6],
    20337: SuitFaceoffTaunts['sc'][7],
    20338: SuitFaceoffTaunts['sc'][8],
    20339: SuitFaceoffTaunts['sc'][9],
    20340: SuitFaceoffTaunts['sc'][10],

    20341: SuitFaceoffTaunts['sd'][0],
    20342: SuitFaceoffTaunts['sd'][1],
    20343: SuitFaceoffTaunts['sd'][2],
    20344: SuitFaceoffTaunts['sd'][3],
    20345: SuitFaceoffTaunts['sd'][4],
    20346: SuitFaceoffTaunts['sd'][5],
    20347: SuitFaceoffTaunts['sd'][6],
    20348: SuitFaceoffTaunts['sd'][7],
    20349: SuitFaceoffTaunts['sd'][8],
    20350: SuitFaceoffTaunts['sd'][9],
    }

# These indexes, defined above, will construct a submenu in the FACTORY menu
# to allow the user to describe all the places he might want to meet
SCFactoryMeetMenuIndexes = (1903, 1904, 1906, 1907, 1908, 1910, 1913,
                            1915, 1916, 1917, 1919, 1922, 1923,
                            1924, 1932, 1940, 1941)

# CustomSCStrings: SpeedChat phrases available for purchase.  It is
# safe to remove entries from this list, which will disable them for
# use from any toons who have already purchased them.  Note that the
# index numbers are stored directly in the database, so once assigned
# to a particular phrase, a given index number should never be
# repurposed to any other phrase.
CustomSCStrings = {
    # Series 1
    10 : "Oh, bon.",
    20 : "Pourquoi pas?",
    30 : "Naturellement!",
    40 : "C'est comme ça que je fais.",
    50 : "Tout juste!",
    60 : "Qu'est-ce qui se passe?",
    70 : "Mais bien sûr!",
    80 : "Bingo!",
    90 : "Tu plaisantes...",
    100 : "Ça m'a l'air bien.",
    110 : "C'est loufoque!",
    120 : "Atmosphérique!",
    130 : "Bon sang!",
    140 : "Ne t'en fais pas.",
    150 : "Grrrr!",
    160 : "Quoi de neuf?",
    170 : "Hé hé hé!",
    180 : "À demain.",
    190 : "À la prochaine fois.",
    200 : "À plus tard, lézard.",
    210 : "Dans un moment, caïman.",
    220 : "Je dois m'en aller d'ici peu.",
    230 : "Je n'en sais rien!",
    240 : "Tu es déjà parti!",
    250 : "Aïe, ça pique!",
    260 : "Je t'ai eu!",
    270 : "S'il te plaît!",
    280 : "Merci vraiment beaucoup!",
    290 : "Tu te débrouilles bien!",
    300 : "Excuse moi!",
    310 : "Puis-je t'aider?",
    320 : "C'est ce que je dis!",
    330 : "Si tu as peur de te brûler, évite la cuisine.",
    340 : "Mille sabords!",
    350 : "Est-ce que ne n'est pas spécial!",
    360 : "Arrête de chahuter!",
    370 : "Le chat a mangé ta langue?",
    380 : "Maintenant tu es mal vu(e)!",
    390 : "Eh bien, regarde ce qui arrive là.",
    400 : "Je dois aller voir un Toon.",
    410 : "Ne t'énerve pas!",
    420 : "Ne te dégonfle pas!",
    430 : "Tu es une proie facile.",
    440 : "Peu importe!",
    450 : "Complètement!",
    460 : "Adorable!",
    470 : "C'est super!",
    480 : "Ouais, mon chou!",
    490 : "Attrape-moi si tu peux!",
    500 : "Il faut d'abord que tu te soignes.",
    510 : "Tu as besoin de plus de rigolpoints.",
    520 : "Je reviens dans une minute.",
    530 : "J'ai faim.",
    540 : "Ouais, t'as raison!",
    550 : "J'ai sommeil.",
    560 : "Je suis prêt(e) maintenant!",
    570 : "Ça m'ennuie.",
    580 : "J'adore ça!",
    590 : "C'était sensationnel!",
    600 : "Saute!",
    610 : "Tu as des gags?",
    620 : "Qu'est-ce qui ne va pas?",
    630 : "Doucement.",
    640 : "Qui va lentement va sûrement.",
    650 : "Marqué!",
    660 : "Prêt?",
    670 : "À vos marques!",
    680 : "Partez!",
    690 : "Allons par là!",
    700 : "Tu as gagné!",
    710 : "Je vote oui.",
    720 : "Je vote non.",
    730 : "J'en suis.",
    740 : "Je n'en suis pas.",
    750 : "On ne bouge pas, je reviens.",
    760 : "C'était rapide!",
    770 : "Qu'est-ce que c'est que ça?",
    780 : "Qu'est-ce que c'est que cette odeur?",
    790 : "Ça pue!",
    800 : "Je m'en fiche.",
    810 : "C'est exactement ce qu'il fallait.",
    820 : "Commençons la fête!",
    830 : "Par ici tout le monde!",
    840 : "Quoi de neuf?",
    850 : "Le chèque est parti.",
    860 : "J'ai entendu ce que tu as dit!",
    870 : "Tu me parles?",
    880 : "Merci, je serai ici toute la semaine.",
    890 : "Hmm.",
    900 : "Je prends celui-là.",
    910 : "Je l'ai!",
    920 : "C'est à moi!",
    930 : "S'il te plaît, prends-le.",
    940 : "On ne s'approche pas, ça pourrait être dangereux.",
    950 : "Pas de soucis!",
    960 : "Oh, non!",
    970 : "Houlala!",
    980 : "Youhouuu!",
    990 : "Tout le monde à bord!",
    1000 : "Nom d'un chien!",
    1010 : "La curiosité est un vilain défaut.",
    # Series 2
    2000 : "Ne fais pas le bébé!",
    2010 : "Si je suis content(e) de te voir!",
    2020 : "Je t'en prie.",
    2030 : "Tu as évité les ennuis?",
    2040 : "Mieux vaut tard que jamais!",
    2050 : "Bravo!",
    2060 : "Sérieusement, les copains...",
    2070 : "Tu veux te joindre à nous?",
    2080 : "À plus tard!",
    2090 : "Changé d'avis?",
    2100 : "Viens le prendre!",
    2110 : "Oh là là!",
    2120 : "Ravi(e) de faire ta connaissance.",
    2130 : "Ne fais rien que je ne ferais pas!",
    2140 : "N'y pense pas!",
    2150 : "N'abandonne pas le navire!",
    2160 : "Ne retiens pas ta respiration.",
    2170 : "No comment.",
    2180 : "C'est facile à dire.",
    2190 : "Assez c'est assez!",
    2200 : "Excellent!",
    2210 : "Content de te trouver ici!",
    2220 : "Arrête un peu.",
    2230 : "Content d'entendre ça.",
    2240 : "Continue, ça m'amuse!",
    2250 : "Vas-y!",
    2260 : "Bon travail!",
    2270 : "Content de te voir!",
    2280 : "Il faut que je bouge.",
    2290 : "Il faut que je m'en aille.",
    2300 : "Attends là.",
    2310 : "Attends une seconde.",
    2320 : "Va t'éclater!",
    2330 : "Amuse-toi!",
    2340 : "Je n'ai pas toute la journée!",
    2350 : "Retiens la vapeur!",
    2360 : "Nom d'un petit bonhomme!",
    2370 : "Je n'y crois pas!",
    2380 : "J'en doute.",
    2390 : "Je t'en dois un.",
    2400 : "Je te reçois 5 sur 5.",
    2410 : "Je crois aussi.",
    2420 : "Je crois que tu devrais passer un tour.",
    2430 : "C'est moi qui voulais le dire.",
    2440 : "Je ne ferais pas ça si j'étais toi.",
    2450 : "Ce serait avec plaisir!",
    2460 : "J'aide mon ami(e).",
    2470 : "Je suis là toute la semaine.",
    2480 : "Imagine ça!",
    2490 : "Juste à temps...",
    2500 : "Tant que ce n'est pas fini, ce n'est pas fini.",
    2510 : "Je pense tout haut.",
    2520 : "On reste en contact.",
    2530 : "Quel temps de chien!",
    2540 : "Et que ça saute!",
    2550 : "Fais comme chez toi.",
    2560 : "Une autre fois peut-être.",
    2570 : "Je peux me joindre à vous?",
    2580 : "C'est sympa ici.",
    2590 : "Je suis content de te parler.",
    2600 : "Ça ne fait aucun doute.",
    2610 : "Sans blague!",
    2620 : "Ni de près ni de loin.",
    2630 : "Quel culot!",
    2640 : "OK pour moi.",
    2650 : "D'accord.",
    2660 : "Dis \" Cheese! \"",
    2670 : "Tu dis quoi?",
    2680 : "Ta-daa!",
    2690 : "Doucement.",
    2700 : "À plus!",
    2710 : "Merci, mais non.",
    2720 : "C'est le bouquet!",
    2730 : "C'est marrant.",
    2740 : "Voilà exactement ce qu'il faut!",
    2750 : "Il y a une invasion de Cogs!",
    2760 : "Salut.",
    2770 : "Fais attention!",
    2780 : "Bravo!",
    2790 : "Qu'est-ce qui se prépare?",
    2800 : "Qu'est-ce qui se passe?",
    2810 : "Ça marche pour moi.",
    2820 : "Oui monseigneur.",
    2830 : "Tu paries.",
    2840 : "Tu fais le calcul.",
    2850 : "Tu t'en vas déjà?",
    2860 : "Tu me fais rire!",
    2870 : "Ça va bien.",
    2880 : "Tu descends!",
    # Series 3
    3000 : "Tout ce que tu diras.",
    3010 : "Je pourrais venir?",
    3020 : "Vérifie, s'il te plaît.",
    3030 : "Ne sois pas trop certain.",
    3040 : "Ça ne te fait rien si je le fais.",
    3050 : "Pas de panique!",
    3060 : "Tu ne le savais pas!",
    3070 : "Ne t'occupe pas de moi.",
    3080 : "Eureka!",
    3090 : "Voyez-vous ça!",
    3100 : "Oublie ça!",
    3110 : "Tu vas dans la même direction?",
    3120 : "Content(e) pour toi!",
    3130 : "Mon Dieu!",
    3140 : "Passe un bon moment!",
    3150 : "Réfléchissons!",
    3160 : "Et ça recommence.",
    3170 : "Et voilà!",
    3180 : "Ça te plaît?",
    3190 : "Je crois aussi.",
    3200 : "Je ne crois pas.",
    3210 : "Je te recontacte.",
    3220 : "Je suis toute ouïe.",
    3230 : "Je suis occupé(e).",
    3240 : "Je ne blague pas!",
    3250 : "J'en suis baba.",
    3260 : "Garde le sourire.",
    3270 : "Tiens-moi au courant!",
    3280 : "Laisse faire!",
    3290 : "De même, certainement.",
    3300 : "Remue-toi!",
    3310 : "Oh là là, comme le temps passe.",
    3320 : "Sans commentaire.",
    3330 : "Ah, on y vient!",
    3340 : "OK pour moi.",
    3350 : "Ravi(e) de te rencontrer.",
    3360 : "D'accord.",
    3370 : "Sûrement.",
    3380 : "Merci vraiment beaucoup.",
    3390 : "C'est plutôt ça.",
    3400 : "Voilà ce qu'il faut!",
    3410 : "C'est l'heure pour moi d'aller faire un somme.",
    3420 : "Crois-moi!",
    3430 : "Jusqu'à la prochaine fois.",
    3440 : "Ne t'endors pas!",
    3450 : "C'est comme ça qu'il faut faire!",
    3460 : "Qu'est-ce qui t'amène?",
    3470 : "Qu'est-ce qui s'est passé?",
    3480 : "Et quoi maintenant?",
    3490 : "Toi d'abord.",
    3500 : "Tu prends à gauche.",
    3510 : "Tu parles!",
    3520 : "Tu es grillé(e)!",
    3530 : "Tu es trop!",
    # Series 4
    4000 : "Vive les Toons! ",
    4010 : "Les Cogs en sont baba! ",
    4020 : "Tous les Toons du monde ensemble! ",
    4030 : "Salut, mon pote! ",
    4040 : "Merci beaucoup. ",
    4050 : "Fiche le camp, l’ami. ",
    4060 : "J’en peux plus, je vais dormir. ",
    4070 : "J’en croque un morceau! ",
    4080 : "La ville n’est pas assez grande pour nous deux! ",
    4090 : "En selle! ",
    4100 : "Dégaine!!! ",
    4110 : "Y’a bon... Tout ça pour moi! ",
    4120 : "Bonne route! ",
    4130 : "Et là, je m’en vais droit vers l’horizon... ",
    4140 : "On fiche le camp! ",
    4150 : "C’est une idée fixe? ",
    4160 : "Bon sang! ",
    4170 : "Impeccable. ",
    4180 : "Je crois bien. ",
    4190 : "Taillons-nous! ",
    4200 : "Eh, va savoir! ",
    4210 : "Coucou, me revoilou! ",
    4220 : "Comme on se retrouve... ",
    4230 : "Allez, hue! ",
    4240 : "Haut les mains. ",
    4250 : "J’y compte bien",
    4260 : "Retiens la vapeur! ",
    4270 : "Je raterais un éléphant dans un couloir. ",
    4280 : "À la prochaine. ",
    4290 : "C’est vraiment impressionnant! ",
    4300 : "Ne nous dis pas que tu as la trouille. ",
    4310 : "Tu crois que tu as de la chance? ",
    4320 : "Bon sang, mais qu’est-ce qui se passe ici? ",
    4330 : "Tu peux bien rouler des mécaniques! ",
    4340 : "Eh bien ça, c’est le bouquet. ",
    4350 : "C’est un vrai régal pour les yeux! ",
    4360 : "Quel trou à rats! ",
    4370 : "Ne t’en fais pas. ",
    4380 : "Quelle tronche! ",
    4390 : "Ça t’apprendra! ",
    # Series 6
    6000 : "Je veux des friandises! ",
    6010 : "J’ai un faible pour le sucré. ",
    6020 : "Ce n’est pas assez cuit. ",
    6030 : "C’est comme faucher les jouets d’un enfant! ",
    6040 : "Et treize à la douzaine. ",
    6050 : "Ils en ont voulu, ils en auront! ",
    6060 : "C’est la cerise sur le gateau",
    6070 : "On ne peut pas avoir le beurre et l’argent du beurre. ",
    6080 : "J’ai l’impression d’être un enfant dans un magasin de bonbons. ",
    6090 : "Six de celui-là, une demi-douzaine de l’autre... ",
    6100 : "Disons-le avec des mots tendres. ",
    6110 : "Concentre-toi sur ta pâte à gâteau. ",
    6120 : "Tu voudrais que j’avale ça? ",
    6130 : "C’est mince comme du papier alu. ",
    6140 : "Fais péter les cahuètes! ",
    6150 : "Tu es un dur à cuire! ",
    6160 : "Et voilà, c’est la déconfiture. ",
    6170 : "C’est comme l’eau et l’huile. ",
    6180 : "Tu me prends pour une poire? ",
    6190 : "Avec du miel, ça passera mieux. ",
    6200 : "Tu es fait de ce que tu manges! ",
    6210 : "C’est de la tarte! ",
    6220 : "Ne fais pas l’andouille! ",
    6230 : "Du sucre, de la cannelle et ce sera nickel. ",
    6240 : "C’est de la crème! ",
    6250 : "C’est le gâteau! ",
    6260 : "Y’en aura pour tout le monde! ",
    6270 : "C’est pas la peine d’en rajouter une couche. ",
    6280 : "Toc, toc... ",
    6290 : "Qui est là? ",
    # Series 7
    7000 : "Arrête de faire des singeries! ",
    7010 : "C’est vraiment mettre des bâtons dans les roues. ",
    7020 : "Tu singes tout. ",
    7030 : "Tu deviens espiègle comme un singe. ",
    7040 : "Ça sent la monnaie de singe. ",
    7050 : "Je te cherche les poux. ",
    7060 : "Qui est-ce qui fait le singe au milieu? ",
    7070 : "Tu m’enlèves une épine du pied... ",
    7080 : "C’est plus marrant qu’une armée de singes! ",
    7090 : "Sans rire... ",
    7100 : "Je suis malin comme un singe. ",
    7110 : "Et qu’est-ce qu’il a, le pingouin? ",
    7120 : "Je n’entends rien de mal. ",
    7130 : "Je ne vois rien de mal. ",
    7140 : "Je ne dis rien de mal. ",
    7150 : "Encore un truc à la noix de coco, on se casse. ",
    7160 : "C’est la jungle par ici. ",
    7170 : "T’es au top du top.",
    7180 : "Ça c’est super! ",
    7190 : "Je deviens dingue! ",
    7200 : "Entrons dans la danse! ",
    7210 : "Ça swingue par ici! ",
    7220 : "Je vais prendre racine. ",
    7230 : "On nous tourne en bourrique. ",
    7230 : "Allez, salut la compagnie. ",
    7240 : "Les bonbons ne poussent pas sur les cocotiers! ",

    # Halloween
    10000 : "Cet endroit est une ville fantôme.",
    10001 : "Joli costume!",
    10002 : "Je crois que cet endroit est hanté.",
    10003 : "Une farce ou des friandises!",
    10004 : "Bouh!",
    10005 : "Ici trouille!",
    10006 : "Joyeux Halloween!",
    10007 : "Je vais me transformer en citrouille.",
    10008 : "Fantômtastique!",
    10009 : "Sinistre!",
    10010 : "Ça fait froid dans le dos!",
    10011 : "Je déteste les araignées!",
    10012 : "Tu as entendu ça?",
    10013 : "Tu n'as pas l'ombre d'une chance!",
    10014 : "Tu m'as fait peur!",
    10015 : "C'est sinistre!",
    10016 : "C'est effrayant!",
    10017 : "C'était étrange....",
    10018 : "Des squelettes dans ton placard?",
    10019 : "Je t'ai fait peur?",

    # Fall Festivus
    11000 : "Bah! Balivernes!",
    11001 : "Mieux vaut ne pas bouder!",
    11002 : "Brrr!",
    11003 : "Glaçant!",
    11004 : "Viens le prendre!",
    11005 : "Ne prends pas cet air glacé.",
    11006 : "À la Sainte-Catherine, tout arbre prend racine!",
    11007 : "Bon réveillon!",
    11008 : "Bonne année!",
    11009 : "Chaud les marrons!",
    11010 : "Bon appétit pour la dinde!",
    11011 : "Ho! Ho! Ho!",
    11012 : "Ce neige pas un problème.",
    11013 : "Ce neige pas un mystère.",
    11014 : "Et que ça neige!",
    11015 : "On va en faire une pelletée de neige.",
    11016 : "Meilleurs vœux!",
    11017 : "Je n'en neige aucun doute!",
    11018 : "Jusque là, la neige est bonne!",
    11019 : "Tu vas le regretter!",

    # Valentines
    12000 : "Reste avec moi!",
    12001 : "Sois mon chouchou!",
    12002 : "Bonne Saint Valentin!",
    12003 : "Ooh, comme c'est mignon.",
    12004 : "J'ai le béguin pour toi.",
    12005 : "C'est une amourette.",
    12006 : "Je t'adore!",
    12007 : "C'est la Saint Valentin?",
    12008 : "Tu es un amour!",
    12009 : "Tu es mon canard en sucre.",
    12010 : "Tu es adorable.",
    12011 : "Tu as besoin d'un câlin.",
    12012 : "Adorable!",
    12013 : "C'est si mignon!",
    12014 : "Mignonne allons voir si la rose...",
    12015 : "Qui ce matin était éclose...",
    12016 : "C'est mignon!",

    # St. Patricks Day
    13000 : "Mes salutations fleuries!",
    13001 : "Vive le printemps!",
    13002 : "Tu n'es pas très printanier!",
    13003 : "C'est la chance qui éclôt.",
    13004 : "Je suis vert d'envie.",
    13005 : "Sacré veinard!",
    13006 : "Tu es mon trèfle à quatre feuilles!",
    13007 : "Tu es mon porte-bonheur!",
    }

# indices into cog phrase arrays
SCMenuCommonCogIndices = (20000, 20004)
SCMenuCustomCogIndices = {
    'bf' : (20005, 20014),
    'nc' : (20015, 20024),
    'ym' : (20025, 20035),
    'ms' : (20036, 20046),
    'bc' : (20047, 20057),
    'cc' : (20058, 20070),
    'nd' : (20071, 20080),
    'ac' : (20081, 20092),
    'tf' : (20093, 20103),
    'hh' : (20104, 20114),
    'le' : (20115, 20124),
    'bs' : (20125, 20135),
    'cr' : (20136, 20145),
    'tbc' : (20146, 20156),
    'ds' : (20157, 20164),
    'gh' : (20165, 20177),
    'pp' : (20178, 20187),
    'b' : (20188, 20199),
    'f' : (20200, 20210),
    'mm' : (20211, 20224),
    'tw' : (20225, 20235),
    'mb' : (20236, 20245),
    'm' : (20246, 20254),
    'mh' : (20255, 20266),
    'dt' : (20267, 20276),
    'p' : (20277, 20287),
    'tm' : (20288, 20298),
    'bw' : (20299, 20308),
    'ls' : (20309, 20319),
    'rb' : (20320, 20329),
    'sc' : (20330, 20331),
    'sd' : (20341, 20350),
    }

# Playground.py
PlaygroundDeathAckMessage = TheCogs+" ont pris tous tes gags!\n\nTu es triste. Tu ne peux pas quitter le terrain de jeux avant d'avoir retrouvé la joie de vivre."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "Le contremaître de l'usine a été vaincu avant que tu ne le trouves. Tu n'as pas récupéré de pièces de Cogs."

# DistributedFactory.py
HeadingToFactoryTitle = "En direction de %s..."
ForemanConfrontedMsg = "%s est en train de combattre le contremaître de l'usine!"

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "En attente d'autres joueurs..."
MinigamePleaseWait = "Patiente un peu..."
DefaultMinigameTitle = "Nom du mini jeu"
DefaultMinigameInstructions = "Instructions du mini jeu"
HeadingToMinigameTitle = "En direction de %s..." # minigame title

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

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Tir à la corde"
TugOfWarInstructions = "Appuie alternativement sur les flèches gauche et droite à la vitesse qu'il faut pour aligner la barre verte avec la ligne rouge. N'appuie pas trop rapidement ou trop lentement, tu pourrais finir dans l'eau!"
TugOfWarGameGo = "PARTEZ!"
TugOfWarGameReady = "Prêt..."
TugOfWarGameEnd = "Bien joué!"
TugOfWarGameTie = "Égalité!"
TugOfWarPowerMeter = "Témoin de puissance"

# DistributedPatternGame.py
PatternGameTitle = "Imite %s" % Minnie
PatternGameInstructions = Minnie +" va te montrer une suite de pas de danse. " + \
                          "Essaie de reproduire la danse de "+Minnie+" comme tu la vois en utilisant les flèches!"
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

# DistributedRaceGame.py
RaceGameTitle = "Jeu de l'oie"
RaceGameInstructions = "Clique sur un nombre. Choisis bien! Tu n'avances que si personne d'autre n'a choisi le même nombre."
RaceGameWaitingChoices = "Attente du choix des autres joueurs..."
RaceGameCardText = "%(name)s tire : %(reward)s"
RaceGameCardTextBeans = "%(name)s reçoit : %(reward)s"
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

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "JOUER"

# Purchase.py
GagShopName = "La boutique à gags de Dingo"
GagShopPlayAgain = "REJOUER\n"
GagShopBackToPlayground = "RETOUR AU\nTERRAIN DE JEUX"
GagShopYouHave = "Tu as %s bonbons à dépenser"
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
#
# The voices for GenderShopQuestionMickey and Minnie should not be played simultaneously.
# Options are as follows:
# 1: Mickey first and Minnie follow in a few second.
# 2: When player moves cursor onto the character, the voice to be played.
#    But the voice shouldn't be played while other character is talking.
# Please choose whichever feasible.
#
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

MakeAToonDone = "Fini"
MakeAToonCancel = lCancel
MakeAToonNext = lNext
MakeAToonLast = "Retour"
CreateYourToon = "Clique sur les flèches pour créer ton Toon."
CreateYourToonTitle = "Crée ton Toon"
CreateYourToonHead = "Clique sur les flèches \" tête \" pour choisir différents animaux."
MakeAToonClickForNextScreen = "Clique sur la flèche ci-dessous pour aller à l'écran suivant."
PickClothes = "Clique sur les flèches pour choisir des vêtements!"
PickClothesTitle = "Choisis tes vêtements"
PaintYourToon = "Clique sur les flèches pour peindre ton Toon!"
PaintYourToonTitle = "Peins ton Toon"
MakeAToonYouCanGoBack = "Tu peux aussi retourner en arrière pour changer ton corps!"
MakeAFunnyName = "Choisis un nom amusant pour ton Toon avec le jeu Choisis un nom!"
MustHaveAFirstOrLast1 = "Ton Toon devrait avoir un prénom ou un nom de famille, tu ne penses pas?"
MustHaveAFirstOrLast2 = "Tu ne veux pas que ton Toon ait de prénom ou de nom de famille?"
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
TypeAName = "Tu n'aimes pas ces noms?\nClique ici  -->"
PickAName = "Essaie le jeu Choisis-un-nom!\nClique ici  -->"
PickANameButton = "Choisis-un-nom"
RejectNameText = "Ce nom n'est pas autorisé. Essaie encore."
WaitingForNameSubmission = "Envoi de ton nom..."

# NameShop.py
NameShopNameMaster = "NameMasterFrench.txt"
NameShopPay = "Inscris-toi!"
NameShopPlay = "Essai gratuit"
NameShopOnlyPaid = "Seuls les utilisateurs payants\npeuvent donner un nom à leurs Toons.\nJusqu'à ce que tu t'inscrives,\nton nom sera\n"
NameShopContinueSubmission = "Continuer l'envoi"
NameShopChooseAnother = "Choisir un autre nom"
NameShopToonCouncil = "Le Conseil de Toontown\nva examiner ton\nnom.  "+ \
                       "L'examen peut\nprendre quelques jours.\nPendant que tu attends,\nton nom sera\n "
PleaseTypeName = "Entre ton nom :"
AllNewNames = "Tous les noms\ndoivent être approuvés\npar le Conseil de Toontown."
NameShopNameRejected = "Le nom que tu as\nenvoyé a été refusé."
NameShopNameAccepted = "Félicitations!\nLe nom que tu as\nenvoyé a\nété accepté!"
NoPunctuation = "Tu ne peux pas utiliser de signes de ponctuation dans ton nom!"
PeriodOnlyAfterLetter = "Tu peux utiliser un point dans ton nom, mais seulement après une lettre."
ApostropheOnlyAfterLetter = "Tu peux utiliser une apostrophe dans ton nom, mais seulement après une lettre."
NoNumbersInTheMiddle = "Les caractères numériques ne peuvent pas apparaître au milieu d'un mot."
ThreeWordsOrLess = "Ton nom doit comporter trois mots maximum."
CopyrightedNames = (
    "mickey",
    "mickey mouse",
    "mickeymouse",
    "minnie",
    "minnie mouse",
    "minniemouse",
    "donald",
    "donald duck",
    "donaldduck",
    "pluto",
    "dingo",
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
    'fowl'   : 'Canard',
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
NCBadCharacter = "Ton nom ne peut pas contenir le caractère \" %s \""
NCGeneric = 'Désolé, ce nom ne pourra pas convenir.'
NCTooManyWords = 'Ton nom ne peut pas comporter plus de quatre mots.'
NCDashUsage = ("Les tirets ne peuvent être utilisés que pour relier deux mots ensemble."
               "(comme dans \" Bou-Bou \").")
NCCommaEdge = "Ton nom ne peut pas commencer ou se terminer par une virgule."
NCCommaAfterWord = "Tu ne peux pas commencer un mot par une virgule."
NCCommaUsage = ("Ce nom n'utilise pas les virgules correctement. Les virgules doivent "
                "assembler deux mots, comme dans le nom \" Dr Couac, médecin \". "
                "Les virgules doivent aussi être suivies d'un espace.")
NCPeriodUsage = ("Ce nom n'utilise pas les points correctement. Les points sont "
                 "seulement autorisés dans des mots tels que \" M. \", \" doct. \", \" prof. \", etc.")
NCApostrophes = "Ton nom a trop d'apostrophes."

# DistributedTrophyMgrAI.py
RemoveTrophy = lToonHQ+" : "+TheCogs+" ont repris un des bâtiments que tu avais sauvés!"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = 'Tu as besoin de plus de temps pour réfléchir?'
STOREOWNER_GOODBYE = 'À plus tard!'
STOREOWNER_NEEDJELLYBEANS = 'Tu dois faire un tour de tramway pour avoir des bonbons.'
STOREOWNER_GREETING = 'Choisis ce que tu veux acheter.'
STOREOWNER_BROWSING = "Tu peux regarder, mais tu auras besoin d'un ticket d'habillement pour acheter."
STOREOWNER_NOCLOTHINGTICKET = "Tu as besoin d'un ticket d'habillement pour acheter des vêtements."
# translate
STOREOWNER_NOFISH = "Reviens ici pour vendre des poissons à l'animalerie en échange de bonbons."
STOREOWNER_THANKSFISH = "Merci! L'animalerie va les adorer. Au revoir!"

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
#
QuestScriptTutorialMinnie_1 = "Toontown compte une nouvelle citoyenne! Est-ce que tu as des gags en plus?"
QuestScriptTutorialMinnie_2 = "Bien sûr, %s!"
QuestScriptTutorialMinnie_3 = "Tom Tuteur va te parler des Cogs.\aJe dois y aller!"
#

#
# If there is "\a" between the sentence, we would like to have one of the following sequence.
# 1: display 1st text with 1st voice -> when voice finished, arrow appear. -> if player pushes the arrow button, display 2nd text with 2nd voice.
# 2: display 1st text with 1st voice and altomatically display 2nd text with 2nd voice.
# 3: display 1st text and play 1st voice (arrow is displayed) -> whenever player pushes the button, the voice will be skipped and display 2nd text with 2nd voice.
# Anyway, we need to have some "Skip" rule while playing the voice because from DCV(Disney Character Voice)'s view, it is not preferrable to have voice skipped.
#

QuestScript101_1 = "Ce sont les COGS. Ce sont des robots qui essaient de prendre Toontown."
QuestScript101_2 = "Il y a différentes sortes de COGS et..."
QuestScript101_3 = "...ils transforment de bons bâtiments Toon..."
QuestScript101_4 = "...en affreuses bâtisses Cog!"
QuestScript101_5 = "Mais les COGS ne comprennent pas les blagues!"
QuestScript101_6 = "Un bon gag les arrête."
QuestScript101_7 = "Il y a des quantités de gags ; prends ceux-là pour commencer."
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
QuestScriptTutorialBlocker_2 = "Bonjour?"
QuestScriptTutorialBlocker_3 = "Oh! Tu ne sais pas utiliser le Chat rapide!"
QuestScriptTutorialBlocker_4 = "Clique sur le bouton pour dire quelque chose."
QuestScriptTutorialBlocker_5 = "Très bien!\aLà où tu vas, il y a plein de Toons à qui parler."
QuestScriptTutorialBlocker_6 = "Si tu veux chatter avec tes amis à l'aide du clavier, tu peux utiliser un autre bouton. "
QuestScriptTutorialBlocker_7 = "Ça s'appelle le bouton \" Chat \". Tu dois être officiellement citoyen de Toontown pour l'utiliser."
QuestScriptTutorialBlocker_8 = "Bonne chance! À plus tard!"

QuestScript120_1 = "Bien, tu as trouvé le tramway!\aAu fait, as-tu rencontré Bob le Banquier?\aIl aime bien les sucreries.\aPourquoi n'irais-tu pas te présenter en lui emportant ce sucre d'orge comme cadeau?"
QuestScript120_2 = "Bob le Banquier est dans la banque de Toontown."

QuestScript121_1 = "Miam, merci pour ce sucre d'orge.\aDis donc, si tu peux m'aider, je te donnerai une récompense.\aCes Cogs ont volé les clés de mon coffre. Va battre des Cogs pour trouver une clé volée.\aQuand tu auras trouvé une clé, ramène-la moi."

QuestScript130_1 = "Bien, tu as trouvé le tramway!\aPendant qu'on y est, j'ai reçu un paquet pour le Professeur Pete aujourd'hui.\aÇa doit être la nouvelle craie qu'il a commandée.\aPeux-tu lui apporter s'il te plaît?\aIl est dans l'école."

QuestScript131_1 = "Oh, merci pour la craie.\aQuoi?!?\aCes Cogs ont volé mon tableau. Va vaincre des Cogs pour retrouver le tableau qu'ils m'ont volé.\aQuand tu l'auras trouvé, ramène-le moi."

QuestScript140_1 = "Bien, tu as trouvé le tramway!\aPendant qu'on y est, j'ai un ami, Larry le Libraire, qui est un rat de bibliothèque.\aJ'ai pris ce livre pour lui la dernière fois que j'ai été aux "+lDonaldsDockNC+".\aPourrais-tu lui apporter? Il est à la bibliothèque, d'habitude."

QuestScript141_1 = "Oh, oui, ce livre complète presque ma collection.\aVoyons ça...\aAh, oh...\aMais où est-ce que j'ai mis mes lunettes?\aJe les avais juste avant que ces Cogs ne prennent mon bâtiment.\aVa vaincre des Cogs pour retrouver les lunettes qu'ils m'ont volées.\aQuand tu les auras retrouvées, reviens me voir pour avoir une récompense."

QuestScript150_1 = "Oh... le prochain défi pourrait être trop difficile pour que tu le fasses tout(e) seul(e)!"
QuestScript150_2 = "Pour te faire des amis, trouve un autre joueur et utilise le bouton Nouvel ami."
QuestScript150_3 = "Une fois que tu t'es fait un(e) ami(e), reviens ici."
QuestScript150_4 = "Certains défis sont trop difficiles pour un Toon seul!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignore me"

BossCogName = "Premier vice-président"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "En vertu des pouvoirs qui me sont conférés, tu es promu au grade de %s.  Félicitations!"
BossCogDoobersAway = { 's' : "Va! Et réalise cette vente!" }
BossCogWelcomeToons = "Bienvenue aux nouveaux Cogs!"
BossCogPromoteToons = "En vertu des pouvoirs qui me sont conférés, tu es promu au grade de %s.  Félici--"
CagedToonInterruptBoss = "Hé! Hou! Hé là bas!"
CagedToonRescueQuery = "Alors les Toons, vous êtes venus me sauver?"
BossCogDiscoverToons = "Eh? Des Toons! Déguisés!"
BossCogAttackToons = "À l'attaque!!"
CagedToonDrop = [
    "Bon travail! Tu l'épuises!",
    "Ne le lâchez pas! Il va s'enfuir!",
    "Vous êtes super les copains!",
    "Fantastique! Vous l'avez presque maintenant!",
    ]
CagedToonPrepareBattleTwo = "Attention, il essaie de s'enfuir!\aAidez-moi, tout le monde - montez jusque là et arrêtez-le!"
CagedToonPrepareBattleThree = "Youpi, je suis presque libre!\aMaintenant vous devez attaquer le vice-président des Cogs directement.\aJ'ai tout un lot de tartes que vous pouvez utiliser!\aSautez en l'air et touchez le fond de ma cage, je vous donnerai des tartes.\aAppuyez sur la touche \" Inser \" pour lancer les tartes une fois que vous les avez!"
BossBattleNeedMorePies = "Vous avez besoin de plus de tartes!"
BossBattleHowToGetPies = "Sautez en l'air pour toucher la cage et avoir des tartes."
BossBattleHowToThrowPies = "Appuyez sur la touche \" Inser \" pour lancer les tartes!"
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
    21: "Hé, %(toon)s! Utilisez la touche \" Ctrl \" pour sauter et toucher ma cage!",
    
    100: "Appuyez sur la touche \" Inser \" pour lancer une tarte!",
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

BossElevatorRejectMessage = "Tu ne peux pas monter dans cet ascenseur avant d'avoir gagné une promotion." 

# Types of catalog items
FurnitureTypeName = "Meuble"
PaintingTypeName = "Tableau"
ClothingTypeName = "Vêtement"
ChatTypeName = "Phrase de Chat rapide"
EmoteTypeName = "Leçons de comédie"
PoleTypeName = "Canne à pêche"
WindowViewTypeName = "Vue de la fenêtre"

FurnitureYourOldCloset = "ton ancienne armoire"
FurnitureYourOldBank = "ton ancienne tirelire"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py
FurnitureNames = {
  100 : "Fauteuil",
  110 : "Chaise",
  120 : "Chaise de bureau",
  130 : "Chaise en rondins",
  140 : "Chaise homard",
  145 : "Chaise de survie",
  150 : "Tabouret selle",
  160 : "Chaise locale",
  170 : "Chaise gâteau",
  200 : "Lit",
  210 : "Lit",
  220 : "Lit baignoire",
  230 : "Lit feuille",
  240 : "Lit bateau",
  250 : "Hamac cactus",
  260 : "Lit crème glacée",
  300 : "Piano mécanique",
  310 : "Orgue",
  400 : "Cheminée",
  410 : "Cheminée",
  420 : "Cheminée ronde",
  430 : "Cheminée",
  440 : "Cheminée pomme",
  500 : "Armoire",
  502 : "Armoire pour 15 vêtements",
  510 : "Armoire",
  512 : "Armoire pour 15 vêtements",
  600 : "Petite lampe",
  610 : "Lampe haute",
  620 : "Lampe de table",
  630 : "Lampe Daisy",
  640 : "Lampe Daisy",
  650 : "Lampe méduse",
  660 : "Lampe méduse",
  670 : "Lampe cow-boy",
  700 : "Chaise capitonnée",
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
  1000 : "Grand tapis",
  1010 : "Tapis rond",
  1020 : "Petit tapis",
  1030 : "Paillasson",
  1100 : "Vitrine",
  1110 : "Vitrine",
  1120 : "Bibliothèque haute",
  1130 : "Bibliothèque basse",
  1140 : "Coffre Sundae",
  1200 : "Table d'appui",
  1210 : "Petite table",
  1220 : "Table de salon",
  1230 : "Table de salon",
  1240 : "Table de plongeur",
  1250 : "Table cookie",
  1260 : "Table de chevet",
  1300 : "Tirelire de 1 000 bonbons",
  1310 : "Tirelire de 2 500 bonbons",
  1320 : "Tirelire de 5 000 bonbons",
  1330 : "Tirelire de 7 500 bonbons",
  1340 : "Tirelire de 10 000 bonbons",
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

# CatalogClothingItem.py
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
    }

# CatalogSurfaceItem.py
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

# CatalogWindowItem.py
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

NewCatalogNotify = "De nouveaux articles sont prêts à être commandés par téléphone!"
NewDeliveryNotify = "Un colis t'attend dans ta boîte aux lettres!"
CatalogNotifyFirstCatalog = "Ton premier catalogue est arrivé! Tu peux l'utiliser pour commander de nouveaux objets pour toi ou pour ta maison."
CatalogNotifyNewCatalog = "Ton catalogue N°%s est arrivé! Tu peux utiliser ton téléphone pour commander des articles dans le catalogue de Clarabelle."
CatalogNotifyNewCatalogNewDelivery = "Un colis t'attend dans ta boîte aux lettres! Ton catalogue N°%s est aussi arrivé!"
CatalogNotifyNewDelivery = "Un colis t'attend dans ta boîte aux lettres!"
CatalogNotifyNewCatalogOldDelivery = "Ton catalogue N°%s est arrivé, et des objets t'attendent encore dans ta boîte aux lettres!"
CatalogNotifyOldDelivery = "Des articles t'attendent encore dans ta boîte aux lettres!"
CatalogNotifyInstructions = "Clique sur le bouton \" Retour à la maison \" sur la carte de ton journal de bord, puis va jusqu'au téléphone qui est dans ta maison."
CatalogNewDeliveryButton = "Nouvelle\nlivraison!"
CatalogNewCatalogButton = "Nouveau\ncatalogue"

DistributedMailboxEmpty = "Ta boîte aux lettres est vide pour l'instant. Reviens ici chercher les articles que tu as commandés par téléphone quand ils seront livrés!"
DistributedMailboxWaiting = "Ta boîte aux lettres est vide pour l'instant, mais le paquet que tu as commandé est en chemin. Reviens voir plus tard!"
DistributedMailboxReady = "Ta commande est arrivée!"
DistributedMailboxNotOwner = "Désolé, ce n'est pas ta boîte aux lettres."
DistributedPhoneEmpty = "Tu peux utiliser n'importe quel téléphone pour commander des articles pour toi et pour ta maison. De nouveaux articles seront proposés dans l'avenir.\n\nAucun article n'est disponible à la commande maintenant, mais reviens voir plus tard!"

Clarabelle = "Clarabelle"
MailboxExitButton = "Fermer la boîte aux lettres"
MailboxAcceptButton = "Prends cet objet"
MailboxOneItem = "Ta boîte aux lettres contient 1 objet."
MailboxNumberOfItems = "Ta boîte aux lettres contient %s objets."
MailboxGettingItem = "Récupération de %s dans la boîte aux lettres."
MailboxItemNext = "Objet\nsuivant"
MailboxItemPrev = "Objet\nprécédent"
CatalogCurrency = "bonbons"
CatalogHangUp = "Raccrocher"
CatalogNew = "NOUVEAUTÉ"
CatalogBackorder = "PRÉ-COMMANDE"
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
CatalogPurchaseItemAvailable = "Félicitations pour ton nouvel achat! Tu peux l'utiliser immédiatement."
CatalogPurchaseItemOnOrder = "Félicitations! Ton achat sera bientôt livré dans ta boîte aux lettres."
CatalogAnythingElse = "Puis-je autre chose pour toi?"
CatalogPurchaseClosetFull = "Ton placard est plein. Tu peux acheter cet article, mais tu devras supprimer quelque chose de ton placard pour faire de la place quand il arrivera.\n\nTu veux quand même acheter cet article?"
CatalogAcceptClosetFull = "Ton placard est plein. Tu dois rentrer et supprimer quelque chose de ton placard pour faire de la place pour cet objet avant de pouvoir le sortir de la boîte aux lettres."
CatalogAcceptShirt = "Tu portes maintenant ta nouvelle chemise. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptShorts = "Tu portes maintenant ton nouveau short. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptSkirt = "Tu portes maintenant ta nouvelle jupe. Ce que tu portais avant a été mis dans ton placard."
CatalogAcceptPole = "Tu peux maintenant attraper des poissons plus gros avec ta nouvelle canne!"
CatalogAcceptPoleUnneeded = "Tu as déjà une canne meilleure que celle-ci!"
CatalogPurchaseHouseFull = "Ta maison est pleine. Tu peux acheter cet article, mais tu devras supprimer quelque chose dans ta maison pour faire de la place quand il arrivera.\n\nTu veux quand même acheter cet article?"
CatalogAcceptHouseFull = "Ta maison est pleine. Tu dois rentrer et supprimer quelque chose dans ta maison pour faire de la place pour cet objet avant de pouvoir le sortir de la boîte aux lettres."
CatalogAcceptInAttic = "Ton nouvel article est maintenant dans ton grenier. Pour le placer dans ta maison, va à l'intérieur et clique sur le bouton \" Déplacer les meubles \"."
CatalogAcceptInAtticP = "Tes nouveaux articles sont maintenant dans ton grenier. Pour les placer dans ta maison, va à l'intérieur et clique sur le bouton \" Déplacer les meubles \"."
CatalogPurchaseMailboxFull = "Ta boîte aux lettres est pleine! Tu ne peux pas acheter cet article avant d'avoir sorti des articles de ta boîte aux lettres pour y faire de la place."
CatalogPurchaseOnOrderListFull = "Tu as trop d'articles en commande actuellement. Tu ne peux pas commander d'autres articles avant que ceux que tu as déjà commandés ne soient arrivés."
CatalogPurchaseGeneralError = "L'article n'a pas pu être acheté à cause d'une erreur interne au jeu : code d'erreur %s."
CatalogAcceptGeneralError = "L'article n'a pas pu être retiré de ta boîte aux lettres à cause d'une erreur interne au jeu : code d'erreur %s."

HDMoveFurnitureButton = "Déplacer\nles meubles"
HDStopMoveFurnitureButton = "Meubles\nplacés"
HDAtticPickerLabel = "Dans le grenier"
HDInRoomPickerLabel = "Dans la pièce"
HDInTrashPickerLabel = "À la poubelle"
HDDeletePickerLabel = "Supprimer?"
HDInAtticLabel = "Grenier"
HDInRoomLabel = "Pièce"
HDInTrashLabel = "Poubelle"
HDToAtticLabel = "Mettre\nau grenier"
HDMoveLabel = "Déplacer"
HDRotateCWLabel = "Tourner vers la droite"
HDRotateCCWLabel = "Tourner vers la gauche"
HDReturnVerify = "Remettre cet objet dans le grenier?"
HDReturnFromTrashVerify = "Ressortir cet objet de la poubelle et le mettre dans le grenier?"
HDDeleteItem = "Clique sur OK pour mettre cet objet à la poubelle ou sur Annuler pour le garder."
HDNonDeletableItem = "Tu ne peux pas supprimer les objets de ce type!"
HDNonDeletableBank = "Tu ne peux pas supprimer ta tirelire!"
HDNonDeletableCloset = "Tu ne peux pas supprimer ton armoire!"
HDNonDeletablePhone = "Tu ne peux pas supprimer ton téléphone!"
HDNonDeletableNotOwner = "Tu ne peux pas supprimer les affaires de %s!"
HDHouseFull = "Ta maison est pleine. Tu dois supprimer quelque chose d'autre dans ta maison ou de ton grenier avant de pouvoir ressortir cet article de la poubelle."

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



MessagePickerTitle = "Tu as trop de phrases. Pour pouvoir acheter\n\"%s\"\n tu dois choisir une chose à retirer :"
MessagePickerCancel = lCancel
MessageConfirmDelete = "Es-tu certain de vouloir retirer \"%s\" de ton menu de Chat rapide?"


CatalogBuyText = "Acheter"
CatalogOnOrderText = "En commande"
CatalogPurchasedText = "Déjà\nacheté"
CatalogPurchasedMaxText = "Maximum\ndéjà acheté"
CatalogVerifyPurchase = "Acheter %(item)s pour %(price)s bonbons?"
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

    # Toontown Central Fisherman
    # Toontown Central
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
    2311 : "Frank O'debord",
    2312 : "Dr Sensible",
    2313 : "Lucy Boulette",
    2314 : "Ned Lafronde",
    2315 : "Valérie Deveau",
    2316 : "Cindy Ka",
    2318 : "Mac Aroni",
    2319 : "Annick",
    2320 : "Alfonse Danslebrouillard",

    # Donald's Dock
    1001 : "Willy - Vendeur",
    1002 : "Billy - Vendeur",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "Alain Térieur",
    1008 : "Vendeur d'animalerie",

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
    1123 : "Electre O'magnétique",
    1124 : "Simon Strueux",
    1125 : "Elvire Debord",

    # Seaweed Street
    1201 : "Barbara Bernache",
    1202 : "Art",
    1203 : "Ahab",
    1204 : "Rocky Roc",
    1205 : "Officier QG",
    1206 : "Officier QG",
    1207 : "Officier QG",
    1208 : "Officier QG",
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

    # The Brrrgh
    3001 : "Angèle Ici",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "Lenny - Vendeur",
    3007 : "Penny - Vendeuse",
    3008 : "Warren Fagoté",
    # NPCPêcheur
    3009 : "Vendeur d'animalerie",

    # Walrus Way
    3101 : "M. Lapin",
    3102 : "Tante Angèle",
    3103 : "Tanguy",
    3104 : "Bonnie",
    3105 : "Freddy Frigo",
    3106 : "Paul Poulemouillée",
    3107 : "Patty Toutseule",
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

    # Minnie's Melody Land
    4001 : "Molly Masson",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "Doe - Vendeur",
    4007 : "Ray - Vendeur",
    4008 : "Bernard Mony",
    4009 : "Vendeur de l'animalerie",

    # Alto Ave.
    4101 : "Tom",
    4102 : "Fifi",
    4103 : "Dr Tefaispasdebile",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "Clément de sol",
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

    # Daisy Gardens
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "Prune - Vendeuse",
    5006 : "Rose - Vendeuse",
    5007 : "Bonnie Menteuse",
    5008 : "Vendeur de l'animalerie",

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
    5114 : "Wilt",
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
    5311 : "Jonas Ticot ",
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

    # Dreamland
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
    9011 : "Vendeur de l'animalerie",

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
    2516 : ("École de Toontown", ""),
    2518 : ("Bibliothèque de Toontown", ""),
    2519 : ("Boutique à gags", ""),
    2520 : (lToonHQ, ""),
    2521 : ("Boutique de prêt-à-porter", ""),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("Tout-sourire - Réparations dentaires", ""),
    2602 : ("", ""),
    2603 : ("Mineurs Pince-sans-rire", ""),
    2604 : ("Qui vivra, verrat", ""),
    2605 : ("Usine à pancartes de Toontown", ""),
    2606 : ("", ""),
    2607 : ("Haricots sauteurs", ""),
    2610 : ("Dr Tom Lepitre", ""),
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
    2638 : ("Salle des spectacles de Toontown", ""),
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
    2663 : ("Cinérama de Toontown", ""),
    2664 : ("Les mimes marrants", ""),
    2665 : ("Le Manège - Agence de voyages", ""),
    2666 : ("Bouteilles de gaz hilarant", ""),
    2667 : ("Au bon temps", ""),
    2669 : ("Chez Gaston - ballons pas folichons", ""),
    2670 : ("Fourchettes à soupe", ""),
    2671 : ("", ""),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("Multiplex de cinéma", ""),
    2705 : ("Tony Truant - Bruits en tout genre", ""),
    2708 : ("Colle bleue", ""),
    2711 : ("Bureau de poste de Toontown", ""),
    2712 : ("Café des gloussements", ""),
    2713 : ("Café du rire", ""),
    2714 : ("Cinéplex Louftingue", ""),
    2716 : ("Drôle de soupe", ""),
    2717 : ("Boîtes en bouteille", ""),
    2720 : ("Plaies et Bosses - Réparations de voitures", ""),
    2725 : ("", ""),
    2727 : ("Bouteilles et boîtes d'eau gazeuse", ""),
    2728 : ("Crème de jour évanescente", ""),
    2729 : ("Ornithorynques 14 carats", ""),
    2730 : ("La gazette du rire", ""),
    2731 : ("", ""),
    2732 : ("Spaghettis et barbituriques", ""),
    2733 : ("Cerfs-volants en fonte", ""),
    2734 : ("Tasses et soucoupes volantes", ""),
    2735 : ("Le Pétard mouillé", ""),
    2739 : ("Réparation de fou-rires", ""),
    2740 : ("Pétards d'occasion", ""),
    2741 : ("", ""),
    2742 : ("", ""),
    2743 : ("D. Taché - Nettoyage à sec", ""),
    2744 : ("", ""),
    2747 : ("Encre visible", ""),
    2748 : ("Rions un peu", ""),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("Coussins sonores", ""),
    2802 : ("Boulets de démolition gonflables", ""),
    2803 : ("Le roi du carnaval", ""),
    2804 : ("Dr Faismarcher, chiropracteur", ""),
    2805 : ("", ""),
    2809 : ("Salle de gym Le Poids lent", ""),
    2814 : ("Théâtre de Toontown", ""),
    2818 : ("Au pâté volant", ""),
    2821 : ("", ""),
    2822 : ("Sandwiches au poulet synthétique", ""),
    2823 : ("Glaces hilarantes", ""),
    2824 : ("Cinéma des blagues", ""),
    2829 : ("Balivernes", ""),
    2830 : ("Les piques d'Annick", ""),
    2831 : ("La maison du rire du professeur Tortillard", ""),
    2832 : ("", ""),
    2833 : ("", ""),
    2834 : ("Salle des urgences des morts de rire", ""),
    2836 : ("", ""),
    2837 : ("Hardi - Séminaires", ""),
    2839 : ("À la nouille amère", ""),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : ("Boutique à gags", ""),
    1507 : ("Quartier général des Toons", ""),
    1508 : ("Boutique de prêt-à-porter", ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("Gilets de sauvetage d'occasion", ""),
    1604 : ("Costumes de bain - Nettoyage à sec", ""),
    1606 : ("Crochet - Réparation d'horloges", ""),
    1608 : ("Le Lof", ""),
    1609 : ("À l'appât rance", ""),
    1612 : ("Banque Sixsous", ""),
    1613 : ("La Pieuvre, cabinet d'avocats", ""),
    1614 : ("Toutes voiles devant - Boutique", ""),
    1615 : ("Yatch qu'à demander!", ""),
    1616 : ("Barbe Noire - Salon de beauté", ""),
    1617 : ("La mer à voir - Opticien", ""),
    1619 : ("L'écorçaire! Chirurgie arboricole", ""),
    1620 : ("Babord-tribord", ""),
    1621 : ("Salle de gym La poupe", ""),
    1622 : ("Gymnote - Électricité générale", ""),
    1624 : ("Réparation de couteaux et de peignes", ""),
    1626 : ("La perche rare - Tenues de soirée", ""),
    1627 : ("La cabane de Sam Suffit", ""),
    1628 : ("Accordeur de thons", ""),
    1629 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1200.dna
   1701 : ("École maternelle des p'tits loups", ""),
    1703 : ("Bar Accuda - Restaurant chinois", ""),
    1705 : ("Voiles à vendre", ""),
    1706 : ("La méduse médusée", ""),
    1707 : ("C'est assez - Boutique de cadeaux", ""),
    1709 : ("Gelée de méduse", ""),
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
    1729 : ("", ""),
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
    1813 : ("À mâts couverts, conseiller", ""),
    1814 : ("Le Ho Hisse", ""),
    1815 : ("Quoi de neuf dockteur?", ""),
    1818 : ("Café des sept mers", ""),
    1819 : ("Au dîner des dockers", ""),
    1820 : ("L'hameçon gobé - Farces et attrapes", ""),
    1821 : ("Chez Neptoon", ""),
    1823 : ("À la pomme de mât", ""),
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
    1835 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : ("Boutique à gags", ""),
    4504 : ("Quartier général des Toons", ""),
    4506 : ("Boutique de prêt-à-porter", ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Tom-Tom - Tambours", ""),
    4604 : ("À quatre temps", ""),
    4605 : ("Fifi - Violons d'ingre", ""),
    4606 : ("La case des castagnettes", ""),
    4607 : ("Vêtements Toon branchés", ""),
    4609 : ("Dot, Raie, Mie - Pianos", ""),
    4610 : ("Attention refrain!", ""),
    4611 : ("Diapasons à l'unisson", ""),
    4612 : ("Dr Tefaispasdebile - Dentiste", ""),
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
    4630 : ("La musique est notre forte", ""),
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
    4649 : ("", ""),
    4652 : ("Boutique des doubles-croches", ""),
    4653 : ("", ""),
    4654 : ("Haut perché - Toitures", ""),
    4655 : ("La clé de sol - École de cuisine", ""),
    4656 : ("", ""),
    4657 : ("Quatuor du barbier", ""),
    4658 : ("Pianos en chute libre", ""),
    4659 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("L'eau de rose - École de valse", ""),
    4702 : ("Timbre de bois! Fournitures pour bûcherons", ""),
    4703 : ("Gros Bizet à tous!", ""),
    4704 : ("Tina - concerts de concertina", ""),
    4705 : ("Il est déjà cithare?", ""),
    4707 : ("Studio d'effets sonores Doppler", ""),
    4709 : ("Pirouettes - Magasin d'alpinisme", ""),
    4710 : ("Polka tu roules si vite? Auto-école!", ""),
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
    4732 : ("Étude brute? Troupe de théâtre", ""),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("Soufflet pour accordéons", ""),
    4736 : ("Hyminnent - Préparatifs de mariage", ""),
    4737 : ("Harpe Hônneur", ""),
    4738 : ("Mécanique cantique - Cadeaux", ""),
    4739 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("Crêp'chignon", ""),
    4803 : ("Quelle Mezzo! Service de domestiques", ""),
    4804 : ("École myxolidienne pour serveurs de barres", ""),
    4807 : ("Massage des Brahms et des jambes", ""),
    4809 : ("C'est une cata-strophe!", ""),
    4812 : ("", ""),
    4817 : ("Magasin d'animaux ternaires", ""),
    4819 : ("Chez Yuki - Ukulélés", ""),
    4820 : ("", ""),
    4821 : ("Chez Anna - Croisières", ""),
    4827 : ("Montres Lamesure", ""),
    4828 : ("Ravel - Réveils et horloges", ""),
    4829 : ("Chez Pachelbel - Obus pour canons et fugues", ""),
    4835 : ("Ursatz pour Kool Katz", ""),
    4836 : ("Reggae royal", ""),
    4838 : ("École de kazoologie", ""),
    4840 : ("Coda Pop - Boissons musicales", ""),
    4841 : ("Lyre et Lyre", ""),
    4842 : ("Société Lasyncope", ""),
    4843 : ("", ""),
    4844 : ("Con moto - deux roues", ""),
    4845 : ("Les élégies élégantes d'Ellie", ""),
    4848 : ("De haute luth - Caisse d'épargne", ""),
    4849 : ("", ""),
    4850 : ("L'accord emprunté - Prêteur sur gages", ""),
    4852 : ("Flasques fleuris pour flûtes", ""),
    4853 : ("Chez Léo - Garde-feu", ""),
    4854 : ("Chez Wagner - Vidéos de violons voilés", ""),
    4855 : ("Réseau de radeau-diffusion", ""),
    4856 : ("", ""),
    4862 : ("Les quadrilles quintessencielles de Quentin", ""),
    4867 : ("M. Costello - Kazoos à gogo", ""),
    4868 : ("", ""),
    4870 : ("Chez Ziggy - Zoo et Zigeunermusik", ""),
    4871 : ("Chez Harry - Harmonies Harmonieuses", ""),
    4872 : ("Freddie Fastoche - Touches de piano", ""),
    4873 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : ("Boutique à gags", ""),
    5502 : (lToonHQ, ""),
    5503 : ("Boutique de prêt-à-porter", ""),
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
    5620 : ("Auberge du râteau", ""),
    5621 : ("La critique du Raisin pur", ""),
    5622 : ("La petite reine-claude - Bicyclettes", ""),
    5623 : ("Bains moussants pour oiseaux", ""),
    5624 : ("Écoute ta mère", ""),
    5625 : ("Dur de la feuille", ""),
    5626 : ("Travaux d'aiguille (de pin)", ""),
    5627 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Le bambou du tunnel", ""),
    5702 : ("Les râteaux de Jacquot", ""),
    5703 : ("Cynthia - Magasin de photosynthèses", ""),
    5704 : ("Citronelle Citron - Voitures d'occasion", ""),
    5705 : ("Meubles en herbe à puce", ""),
    5706 : ("14 carottes - Bijoutiers", ""),
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
    5719 : ("Sauge d'une nuit d'été! Détectives privés", ""),
    5720 : ("La feuille de vigne - Prêt-à-porter masculin", ""),
    5721 : ("Routabaga 66 - Restaurant", ""),
    5725 : ("Boutique du grain d'orge", ""),
    5726 : ("Bert", ""),
    5727 : ("Le trou sans fond - Caisse d'épargne", ""),
    5728 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : (lToonHQ, ""),
    5804 : ("La vase de Soisson", ""),
    5805 : ("Le cerveau lent", ""),
    5809 : ("Drôle d'oiseaux - École de clowns", ""),
    5810 : ("Ça ne rom à rain!", ""),
    5811 : ("Auberge Inn", ""),
    5815 : ("Des racines & des herbes", ""),
    5817 : ("Pommes et oranges", ""),
    5819 : ("Pantalons vert citron", ""),
    5821 : ("Centre de squash", ""),
    5826 : ("Matériel d'élevage de fourmis", ""),
    5827 : ("Terre bon marché.", ""),
    5828 : ("Meubles Molasson", ""),
    5830 : ("Vide ton sac (de patates)", ""),
    5833 : ("Bar à salades", ""),
    5835 : ("Séjour en pots chez l'habitant", ""),
    5836 : ("Salles de bain J. Boulée", ""),
    5837 : ("L'école de la vie(gne)", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Bibliothèque des berceuses", ""),
    9503 : ("Bar du roupillon", ""),
    9504 : ("Boutique à gags", ""),
    9505 : (lToonHQ, ""),
    9506 : ("Boutique de prêt-à-porter", ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Auberge des câlins", ""),
    9602 : ("Sommes au rabais", ""),
    9604 : ("Chez Ed - Edredons redondants", ""),
    9605 : ("323 Rue de la Berceuse", ""),
    9607 : ("Big Mama - Pyjamas des Bahamas", ""),
    9608 : ("Quand le chat dort, les souris dansent", ""),
    9609 : ("Roupillon pour trois ronds", ""),
    9613 : ("Horloges à nettoyer", ""),
    9616 : ("La veilleuse - Électricité générale", ""),
    9617 : ("212 Rue de la Berceuse", ""),
    9619 : ("Relax Max", ""),
    9620 : ("PJ - Service de taxi", ""),
    9622 : ("Horloges du sommeil", ""),
    9625 : ("Histoire en boucle - Salon de beauté", ""),
    9626 : ("818 Rue de la Berceuse", ""),
    9627 : ("Le tipi endormi", ""),
    9628 : ("Sam Suffit - Calendriers", ""),
    9629 : ("310 Rue de la Berceuse", ""),
    9630 : ("Marchand de sable", ""),
    9631 : ("Temps d'arrêt - Horloger", ""),
    9633 : ("Salle de projection du pays des rêves", ""),
    9634 : ("Je ronfle, donc je suis", ""),
    9636 : ("Assurance pour insomniaques", ""),
    9639 : ("Maison de l'hibernation", ""),
    9640 : ("805 Rue de la Berceuse", ""),
    9642 : ("À la sciure de mon front", ""),
    9643 : ("Les yeux clos - Optométrie", ""),
    9644 : ("Combats d'oreillers nocturnes", ""),
    9645 : ("Auberge Viensmeborder", ""),
    9647 : ("Fais ton lit! Magasin de bricolage", ""),
    9649 : ("Bonnet blanc et blanc bonnet", ""),
    9650 : ("714 Rue de la Berceuse", ""),
    9651 : ("La vie est un ronflement tranquille", ""),
    9652 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : ("Boutique à gags", ""),
    3508 : (lToonHQ, ""),
    3509 : ("Boutique de prêt-à-porter", ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("Aurore boréale - Électricité générale", ""),
    3602 : ("Bonnets de pâques", ""),
    3605 : ("", ""),
    3607 : ("Le vieillard du blizzard", ""),
    3608 : ("À en perdre la boule (de neige)!", ""),
    3610 : ("Supérette Les Mirettes", ""),
    3611 : ("M. Lapin - Chasse-neige", ""),
    3612 : ("Conception d'igloos", ""),
    3613 : ("Glaces et miroirs", ""),
    3614 : ("Fabricant de flocons d'avoine", ""),
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
    3641 : ("Chez Tanguy - Bateaux à dormir debout", ""),
    3642 : ("L'œil du cyclone - Opticien", ""),
    3643 : ("Chambre (froide) de danse", ""),
    3644 : ("Glaçons fondus", ""),
    3647 : ("Au pingouin sanguin - Magasin de smokings", ""),
    3648 : ("Glace instantanée", ""),
    3649 : ("Hambrrghers", ""),
    3650 : ("Articlités", ""),
    3651 : ("Freddy Frigo - Saucisses congelées", ""),
    3653 : ("Bijoux glacés", ""),
    3654 : ("", ""),
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
    3739 : ("", ""),
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
EstatePopupOK = "OK"
EstateTeleportFailed = "Impossible de retourner à la maison. Essaie encore!"
EstateTeleportFailedNotFriends = "Désolé, %s est chez un Toon avec qui tu n'es pas ami(e)."

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
FishTankValue = "Salut,%(name)s! Tu as %(num)s poissons dans ton seau qui valent au total %(num)s bonbons. Veux-tu tous les vendre?"

def GetPossesive(name):
    if name[-1:] == 's':
        possesive = "de " + name
    else:
        possesive = "de " + name
    return possesive

# end translate

# DistributedFireworkShow.py
FireworksInstructions = lToonHQ+" : Appuie sur la touche \" Page précédente \" pour mieux voir."

FireworksJuly4Beginning = lToonHQ+" : Feux d’artifices du 14 Juillet : Profitez du spectacle!"
FireworksJuly4Ending = lToonHQ+" : Nous espérons que vous avez profité du spectacle! Passez un excellent été!"
FireworksNewYearsEveBeginning = lToonHQ+" : Bonne année! Profitez du feu d'artifice!"
FireworksNewYearsEveEnding = lToonHQ+" : Nous espérons que vous avez profité du spectacle! Bonne année 2006!"
FireworksBeginning = lToonHQ+" : Feux d’artifices du 14 Juillet : Profitez du spectacle!"
FireworksEnding = lToonHQ+" : Nous espérons que vous avez profité du spectacle! Passez un excellent été!"

# ToontownLoadingScreen.py

TIP_NONE = 0
TIP_GENERAL = 1
TIP_STREET = 2
TIP_MINIGAME = 3
TIP_COGHQ = 4

# As of 8/5/03, ToonTips shouldn't exceed 130 characters in length
TipTitle = "ASTUCE TOON :"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Pour vérifier rapidement les progrès de ton défitoon, maintiens enfoncée la touche \" Fin \".",
    "Pour vérifier rapidement ta page de gags, maintiens enfoncée la touche \" Première page \".",
    "Pour ouvrir ta liste d'amis, appuie sur la touche \" F7 \".",
    "Pour ouvrir ou fermer ton journal de bord, appuie sur la touche \" F8 \".",
    "Pour regarder vers le haut, appuie sur la touche \" Page précédente \" ; pour regarder vers le bas, appuie sur la touche \" Page suivante \".",
    "Appuie sur la touche \" Contrôle \" pour sauter.",
    "Appuie sur la touche \" F9 \" pour faire une capture d'écran, qui sera enregistrée dans le dossier Toontown de ton ordinateur.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "Tu peux échanger des codes d'ami secret avec des personnes que tu connais en dehors de Toontown pour pouvoir chatter avec eux dans Toontown.",
    "Tu peux changer ta résolution d'écran, régler le son et d'autres options dans la page d'options du journal de bord.",
    "Essaie les vêtements de tes amis, qui sont dans les placards de leurs maisons.",
    "Tu peux rentrer chez toi grâce au bouton \" Retour à la maison \" sur ta carte.",
    "Chaque fois que tu termines un défitoon avec succès, tes rigolpoints sont automatiquement ajoutés.",
    "Tu peux voir la collection dans les boutiques de prêt-à-porter même sans ticket d'habillement.",
    "Les récompenses de certains défitoons te permettent d'avoir plus de gags et de bonbons.",
    "Tu peux avoir jusqu'à 50 amis sur ta liste d'amis.",
    "La récompense de certains défitoons te permet de te téléporter jusqu'aux terrains de jeux de Toontown par la carte du journal de bord.",
    "Augmente tes rigolpoints sur les terrains de jeux en ramassant des trésors tels que des étoiles et des cornets de glace.",
    "Si tu as besoin de te soigner rapidement après un combat difficile, va chez toi et ramasse des cornets de glace.",
    "Pour changer la visualisation de ton Toon, appuie sur la touche de tabulation.",
    "Quelquefois tu peux trouver plusieurs défitoons différents proposés pour la même récompense. Fais ton choix!",
    "Trouver des amis qui font le même défitoon est une manière amusante de progresser dans le jeu.",
    "Tu n'as jamais besoin d'enregistrer ta progression dans Toontown. Les serveurs de Toontown enregistrent toutes les informations nécessaires en continu.",
    "Tu peux parler en chuchotant à d'autres Toons en cliquant sur eux ou en les sélectionnant dans ta liste d'amis.",
    "Certaines phrases du Chat rapide provoquent une émotion animée sur ton Toon.",
    "Si tu te trouves dans une zone où il y a trop de monde, tu peux essayer de changer de district. Va à la page des districts dans le journal de bord et choisis-en un autre.",
    "Si tu sauves activement des bâtiments, une étoile de bronze, d'argent ou d'or s'affichera au-dessus de ton Toon.",
    "Si tu sauves assez de bâtiments pour avoir une étoile au-dessus de ta tête, tu pourras trouver ton nom affiché sur le tableau d'un Quartier général des Toons.",
    "Les bâtiments sauvés sont quelquefois recapturés par les Cogs. La seule façon de conserver ton étoile est d'aller sauver plus de bâtiments.",
    "Les noms de tes amis secrets apparaîtront en bleu.",
    # Fishing
    "Essaie d'avoir toutes les espèces de poisson de Toontown!",
    "Chaque mare recèle différentes sortes de poissons. Essaie-les toutes!",
    "Lorsque ton seau de pêche est plein, tu peux vendre tes poissons aux vendeurs de l'animalerie sur les terrains de jeux.",
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
    "Certains trophées de pêche te valent un rigol-augmentation.",
    "La pêche est une bonne façon de gagner plus de bonbons.",
    ),

  TIP_STREET : (
    "Il existe quatre types de Cogs : Les Loibots, les Caissbots, les Vendibots et les Chefbots.",
    "Chaque série de gags est associée à différents niveaux de précision et de dégâts.",
    "Les gags de tapage affectent tous les Cogs mais réveillent les Cogs leurrés.",
    "Battre les Cogs en ordre stratégique peut grandement augmenter tes chances de gagner les batailles.",
    "La série de gags \" toonique \" te permet de soigner les autres Toons lors d'une bataille.",
    "Les points d'expérience des gags sont doublés pendant une invasion de Cogs!",
    "Plusieurs Toons peuvent faire équipe et utiliser la même série de gags lors d'une bataille pour infliger plus de dégâts aux Cogs.",
    "Lors des batailles, les gags sont utilisés dans l'ordre affiché sur le menu des gags, de haut en bas.",
    "La rangée de lumières circulaires sur les ascenseurs des bâtiments des Cogs indiquent combien d'étages ils contiennent.",
    "Clique sur un Cog pour avoir plus de détails.",
    "L'utilisation de gags de haut niveau contre des Cogs de bas niveau ne donne pas de points d'expérience.",
    "Un gag qui donnera de l'expérience s'affiche sur fond bleu sur le menu des gags lors de la bataille.",
    "L'expérience des gags est multipliée lorsqu'ils sont utilisés à l'intérieur des bâtiments des Cogs. Les étages les plus hauts ont des coefficients de multiplication plus grands.",
    "Lorsqu'un Cog est vaincu, chacun des Toons ayant participé est crédité de la victoire sur ce Cog lorsque la bataille est terminée.",
    "Chaque rue de Toontown a différents types et niveaux de Cogs.",
    "Il n'y a pas de Cogs sur les trottoirs.",
    "Sur les rues, les portes latérales racontent des blagues lorsque tu t'en approches.",
    "Certains défitoons t'entraînent à de nouvelles séries de gags. Tu ne pourras choisir que six des sept séries de gags, alors choisis bien!",
    "Les pièges ne sont utiles que si toi ou tes amis vous accordez pour utiliser les leurres lors d'une bataille.",
    "Les leurres de plus haut niveau sont moins susceptibles de manquer leur cible.",
    "Les gags de plus bas niveau ont une précision moindre contre les Cogs de haut niveau.",
    "Les Cogs ne peuvent plus attaquer une fois qu'ils ont été leurrés lors d'un combat.",
    "Lorsque tes amis et toi aurez repris un bâtiment aux Cogs, vos portraits seront affichés à l'intérieur du bâtiment en guise de récompense.",
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
    "Il y a des mares dans toutes les rues de Toontown. Certaines rues ont des espèces de poisson uniques.",
    ),

  TIP_MINIGAME : (
    "Après avoir rempli ton pot de bonbons, tous les bonbons que tu gagnes aux jeux du tramway sont automatiquement versés dans ta tirelire.",
    "Tu peux utiliser les flèches du clavier au lieu de la souris dans le jeu du tramway \" Imite Minnie \".",
    "Dans le jeu du canon, tu peux utiliser les flèches du clavier pour déplacer ton canon et appuyer sur la touche \" Contrôle \" pour tirer.",
    "Dans le jeu des anneaux, des points supplémentaires sont attribués quand le groupe entier réussit à nager dans les anneaux.",
    "Un jeu parfait d'\" Imite Minnie \" double tes points.",
    "Dans le tir à la corde, tu reçois plus de bonbons si tu joues contre un Cog plus fort.",
    "La difficulté des jeux du tramway varie selon les quartiers, Toontown centre a les plus faciles et le Pays des rêves de Donald les plus difficiles.",
    "Certains jeux du tramway ne peuvent être joués qu'en groupe.",
    ),

  TIP_COGHQ : (
    "Tu dois terminer ton déguisement de Cog avant d'entrer dans le bâtiment du Chef.",
    "Tu peux sauter sur les gardes du corps des Cogs pour les désactiver temporairement.",
    "Additionne les mérites Cogs par tes victoires sur les Cogs.",
    "Tu obtiens plus de mérites avec des Cogs de plus haut niveau.",
    "Lorsque tu as additionné assez de mérites Cogs pour gagner une promotion, va voir le vice-président des Vendibots!",
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
          "Étoile de mer ciatous ",
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
           "Poisson nouvelle-lune",
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
           ),
    34 : ( "Raie tissante",
           ),
    }

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

