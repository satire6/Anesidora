import string
import time
from toontown.toonbase.TTLocalizer_portuguese_Property import *

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
ExtraKeySanityCheck = "Ignore-me"

InterfaceFont = 'phase_3/models/fonts/ImpressBT.ttf'
ToonFont = 'phase_3/models/fonts/ImpressBT.ttf'
SuitFont = 'phase_3/models/fonts/vtRemingtonPortable.ttf'
SignFont = 'phase_3/models/fonts/MickeyFont'
MinnieFont = 'phase_3/models/fonts/MinnieFont'
FancyFont = 'phase_3/models/fonts/Comedy'
NametagFonts = ('phase_3/models/fonts/AnimGothic',      #0 *
                'phase_3/models/fonts/Aftershock',      #1 *
                'phase_3/models/fonts/JiggeryPokery',   #2 *
                'phase_3/models/fonts/Ironwork',        #3 *
                'phase_3/models/fonts/HastyPudding',    #4 *
                'phase_3/models/fonts/Comedy',          #5 *
                'phase_3/models/fonts/Humanist',        #6 *
                'phase_3/models/fonts/Portago',         #7 *
                'phase_3/models/fonts/Musicals',        #8 *
                'phase_3/models/fonts/Scurlock',        #9 *
                'phase_3/models/fonts/Danger',          #10 *
                'phase_3/models/fonts/Alie',            #11 *
                'phase_3/models/fonts/OysterBar',       #12 *
                'phase_3/models/fonts/RedDogSaloon',    #13 *
                )
NametagFontNames = ('Usuário',      #0 *
                'Tremido',         #1 *
                'Arrepiante',      #2 *
                'Exorbitante',     #3 *
                'Bobo',            #4 *
                'Doido',           #5 *
                'Pratico',         #6 *
                'Nautico',         #7 *
                'Caprichoso',      #8 *
                'Estremecer',      #9 *
                'Ação',            #10 *
                'Poético',         #11 *
                'Passeio',         #12 *
                'Ocidental',       #13 *
                )

NametagLabel = "Nome"

UnpaidNameTag = "Basico"

BuildingNametagFont = 'phase_3/models/fonts/MickeyFont'
BuildingNametagShadow = None

# Product prefix
ProductPrefix = 'TT'

# common names
Mickey = "Mickey"
VampireMickey = "VampireMickey"
Minnie = "Minnie"
WitchMinnie = "WitchMinnie"
Donald = "Donald"
DonaldDock = "DonaldDock"
Daisy  = "Margarida"
Goofy  = "Pateta"
SuperGoofy = "SuperGoofy"
Pluto  = "Pluto"
WesternPluto = "WesternPluto"
Flippy = "Flippy"
Chip   = "Tico"
Dale   = "Teco"

# common locations
lTheBrrrgh = 'O Brrrgh'
lDaisyGardens = 'Jardim da Margarida'
lDonaldsDock = "Porto do Donald"
lDonaldsDreamland = "Sonholândia do Donald"
lMinniesMelodyland = "Melodilândia da Minnie"
lToontownCentral = 'Centro de Toontown'
lToonHQ = 'Quartel dos Toons'
lSellbotHQ = 'Sellbot HQ'
lGoofySpeedway = "Autódromo do Pateta"
lOutdoorZone = "Bosque de Bolotas de Tico e Teco"
lGolfZone = "Minigolfe de Tico e Teco"
lPartyHood = "Party Grounds"

lGagShop = 'Loja de Piadas'
lClothingShop = 'Loja de Roupas'
lPetShop = 'Loja de Animais'

# common strings
lCancel = 'Cancelar'
lClose = 'Fechar'
lOK = 'OK'
lNext = 'Próximo'
lQuit = 'Sair'
lYes = 'Sim'
lNo = 'Não'
lBack = 'Voltar'

sleep_auto_reply = "%s is sleeping right now"
lHQ = 'Oficial'

lHQOfficerF = 'Oficial do Quartel'
lHQOfficerM = 'Oficial do Quartel'

MickeyMouse = "Mickey Mouse"

AIStartDefaultDistrict = "Vila dos Idiotas"

Cog  = "Cog"
Cogs = "Cogs"
ACog = "um Cog"
TheCogs = "os Cogs"
ASkeleton = "um Esqueletocog"
Skeleton = "Esqueletocogs"
SkeletonP = "Esqueletocogs"
Av2Cog = "um Cog Versão 2.0"
v2Cog = "Cog Versão 2.0"
v2CogP = "Cogs Versão 2.0"
ASkeleton = "um Esqueletocog"
Foreman = "Supervisor da fábrica"
ForemanP = "Supervisores da fábrica"
AForeman = "um Supervisor da fábrica"
CogVP = Cog + " VP"
CogVPs = "Cogs VPs"
ACogVP = ACog + " VP"
Supervisor = "Supervisor da Casa da Moeda"
SupervisorP = "Supervisores da Casa da Moeda"
ASupervisor = "um Supervisor da Casa da Moeda"
CogCFO = Cog + "Diretor Financeiro"
CogCFOs = "Diretores Financeiros Cogs"
ACogCFO = ACog + "Diretor Financeiro"

# AvatarDNA.py
Bossbot = "Robô-chefe"
Lawbot = "Robô da Lei"
Cashbot = "Robô Mercenário"
Sellbot = "Robô Vendedor"
BossbotS = "um Robô-chefe"
LawbotS = "um Robô da Lei"
CashbotS = "um Robô Mercenário"
SellbotS = "um Robô Vendedor"
BossbotP = "Robôs-chefe"
LawbotP = "Robôs da Lei"
CashbotP = "Robôs Mercenários"
SellbotP = "Robôs Vendedores"
BossbotSkelS = "um Esqueletocog %s" % (Bossbot)
LawbotSkelS = "um Esqueletocog %s" % (Lawbot)
CashbotSkelS = "um Esqueletocog %s" % (Cashbot)
SellbotSkelS = "um Esqueletocog %s" % (Sellbot)
BossbotSkelP = "Esqueletocogs %s" % (BossbotP)
LawbotSkelP = "Esqueletocogs %s" % (LawbotP)
CashbotSkelP = "Esqueletocogs %s" % (CashbotP)
SellbotSkelP = "Esqueletocogs %s" % (SellbotP)
SkeleRevivePostFix = " v2.0"

lBossbotHQ = 'Quartel do Robô-chefe'
lLawbotHQ = 'Quartel do Robô da Lei'
lCashbotHQ = 'Quartel do Robô Mercenário'
lSellbotHQ = 'Quartel do Robô Vendedor'
lTutorial = 'Toon-torial'
lMyEstate = 'sua casa'
lWelcomeValley = 'Vale Boas-vindas'

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("para o",  "no", "Terraço do Tutorial"), # Tutorial
    1000  : ("para o",  "no", "Parque"),
    1100  : ("para o",  "no", "Boulevard das Cracas"),
    1200  : ("para a",  "na", "Rua da Alga Marinha"),
    1300  : ("para a",  "na", "Travessa do Farol"),
    2000  : ("para o",  "no", "Parque"),
    2100  : ("para a",  "na", "Rua da Bobeira"),
    2200  : ("para a",  "na", "Travessa dos Tontos"),
    2300  : ("para o",  "no", "Largo do Auge da Graça"),
    3000  : ("para o",  "no", "Parque"),
    3100  : ("para a",  "na", "Via dos Leões Marinhos"),
    3200  : ("para a",  "na", "Rua da Chuva de Neve"),
    3300  : ("para o",  "no", "Lugar Polar"),
    4000  : ("para o",  "no", "Parque"),
    4100  : ("para a",  "na", "Avenida do Tom Alto"),
    4200  : ("para o",  "no", "Boulevard do Barítono"),
    4300  : ("para o",  "no", "Terraço do Tenor"),
    5000  : ("para o",  "no", "Parque"),
    5100  : ("para a",  "na", "Rua das Nogueiras"),
    5200  : ("para a",  "na", "Rua das Amendoeiras"),
    5300  : ("para a",  "na", "Rua dos Carvalhos"),
    9000  : ("para o",  "no", "Parque"),
    9100  : ("para a",  "na", "Travessa da Canção de Ninar"),
    9200  : ("para o",  "no", "Pedaço do Pijama"),
    10000 : ("","", ""),
    10100 : ("para o",  "no", "Salão do "+lBossbotHQ),
    10200 : ("para a", "na", "Sede do Clube"),
    10500 : ("para o", "no", "Três da Frente"),
    10600 : ("para o", "no", "Seis do Meio"),
    10700 : ("para o", "no", "Nove de Trás"),
    11000 : ("","", ""),
    11100 : ("para o",  "no", "Salão do "+lSellbotHQ),
    11200 : ("para a",  "na", "Fábrica do "+Sellbot),
    11500 : ("para a",  "na", "Fábrica do "+Sellbot),
    12000 : ("","", ""),
    12100 : ("para o",  "no", "Salão do "+lCashbotHQ),
    12500 : ("para a",  "na", "Casa da Moeda"),
    12600 : ("para a",  "na", "Casa da Moeda de Dólar"),
    12700 : ("para a",  "na", "Casa da Moeda de Barras de Ouro"),
    13000 : ("","", ""),
    13100 : ("para o",  "no", "Salão do "+lLawbotHQ),
    13200 : ("para o", "no", "Lobby do Escritório do Promotor"),
    13300 : ("para o", "no", "Escritório da Lei A"),
    13400 : ("para o", "no", "Escritório da Lei B"),
    13500 : ("para o", "no", "Escritório da Lei C"),
    13600 : ("para o", "no", "Escritório da Lei D"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("para o",  "no",    lDonaldsDock)
ToontownCentral   = ("para o",  "no",    lToontownCentral)
TheBrrrgh         = ("para",    "em",    lTheBrrrgh)
MinniesMelodyland = ("para a",  "na",    lMinniesMelodyland)
DaisyGardens      = ("para os", "nos",   lDaisyGardens)
OutdoorZone       = ("para a",  "na",    lOutdoorZone)
FunnyFarm         = ("para a",  "na",    "Fazenda Divertida")
GoofySpeedway     = ("para o",  "no",    lGoofySpeedway)
DonaldsDreamland  = ("para a",  "na",    lDonaldsDreamland)
BossbotHQ         = ("para o",  "no",    lBossbotHQ)
SellbotHQ         = ("para o",  "no",    lSellbotHQ)
CashbotHQ         = ("para o",  "no",    lCashbotHQ)
LawbotHQ          = ("para o",  "no",    lLawbotHQ)
Tutorial          = ("para o",  "no",    lTutorial)
MyEstate          = ("para a",  "na",    lMyEstate)
WelcomeValley     = ("para o",  "no",    lWelcomeValley)
GolfZone          = ("para a",  "na",    lGolfZone)
PartyHood         = ("to the", "in the", lPartyHood)

Factory = 'Fábrica'
Headquarters = 'Quartel'
SellbotFrontEntrance = 'Entrada principal'
SellbotSideEntrance = 'Entrada lateral'
Office = 'Escritório'

FactoryNames = {
    0 : 'Molde da fábrica',
    11500 : 'Fábrica do Cog '+Sellbot,
    13300 : 'Escritório de Cogs Policiais', #remove me JML
    }

FactoryTypeLeg = 'Perna'
FactoryTypeArm = 'Braço'
FactoryTypeTorso = 'Busto'

MintFloorTitle = 'Andar %s'

# Quests.py
TheFish = "o Peixe"
AFish = "um peixe"
Level = "nível"
QuestsCompleteString = "Concluir"
QuestsNotChosenString = "Não escolhido"
Period = "."

Laff = "Risada"

QuestInLocationString = " %(inPhrase)s %(location)s"

# _avName_ gets replaced with the avatar (player's) name
# _toNpcName_ gets replaced with the npc's name we are being sent to
# _where_ gets replaced with a description of where to find the npc, with a leading \a
QuestsDefaultGreeting = ("Olá, _avName_!",
                         "Oi, _avName_!",
                         "E aí, _avName_?",
                         "Diga aí, _avName_!",
                         "Bem-vindo, _avName_!",
                         "Tudo certo, _avName_?",
                         "Como vai você, _avName_?",
                         "Olá _avName_!",
                         )
QuestsDefaultIncomplete = ("Como está indo aquela tarefa, _avName_?",
                           "Parece que você ainda tem mais trabalho a fazer naquela tarefa!",
                           "Continue com o bom trabalho, _avName_!",
                           "Continue tentando concluir aquela tarefa. Eu sei que você consegue!",
                           "Continue tentando concluir a tarefa. Contamos com você!",
                           "Continue trabalhando naquela Tarefa Toon!",
                           )
QuestsDefaultIncompleteProgress = ("Você veio ao lugar certo, mas, primeiramente, precisa concluir sua Tarefa Toon.",
                                   "Ao terminar a Tarefa Toon, volte aqui.",
                                   "Volte quando tiver terminado sua Tarefa Toon.",
                                   )
QuestsDefaultIncompleteWrongNPC = ("Bom trabalho naquela Tarefa Toon. Você deveria visitar _toNpcName_._where_",
                                   "Parece que você está pronto para concluir sua Tarefa Toon. Vá ver _toNpcName_._where_.",
                                   "Vá ver _toNpcName_ para concluir sua Tarefa Toon._where_",
                                   )
QuestsDefaultComplete = ("Bom trabalho! Aqui está a sua recompensa...",
                         "Ótimo trabalho, _avName_! Tome esta recompensa...",
                         "Excelente trabalho, _avName_! Aqui está a sua recompensa...",
                         )
QuestsDefaultLeaving = ("Tchau!",
                        "Até logo!",
                        "Até mais, _avName_.",
                        "Te vejo por aí, _avName_!",
                        "Boa sorte!",
                        "Divirta-se em Toontown!",
                        "Vejo você depois!",
                        )
QuestsDefaultReject = ("Olá.",
                       "Posso ajudar?",
                       "Como vai você?",
                       "E aí, pessoal?",
                       "Estou um pouco ocupado agora, _avName_.",
                       "Sim?",
                       "Tudo certo, _avName_!",
                       "Bem-vindo, _avName_!",
                       "Ei, _avName_! Tudo bem?",
                       # Game Hints
                       "Você sabia que pode abrir seu Álbum Toon clicando em F8?",
                       "Você pode usar seu mapa para se teletransportar de volta ao pátio!",
                       "Você pode ficar amigo de outros jogadores clicando neles.",
                       "Você pode descobrir mais sobre um "+ Cog +" clicando nele.",
                       "Junte tesouros nos pátios para encher seu Risômetro.",
                       "Os edifícios " + Cog + " são lugares perigosos! Não entre neles sozinho!",
                       "Quando você perde uma batalha, os "+ Cogs +" tomam todas as suas piadas.",
                       "Para obter mais piadas, jogue no Bondinho!",
                       "Você pode obter mais Pontos de risadas completando as Tarefas Toon.",
                       "Toda Tarefa Toon dá uma recompensa a você.",
                       "Algumas recompensas permitem que você carregue consigo mais Piadas.",
                       "Se você vencer uma batalha, ganhará créditos de Tarefa Toon para cada "+ Cog +" derrotado.",
                       "Se você recuperar um edifício "+ Cog +", entre e verá um agradecimento especial do proprietário!",
                       "Se pressionar a tecla Page Up, poderá ver acima de você!",
                       "Se você pressionar a tecla Tab, poderá ver os arredores sob diversos ângulos!",
                       "Para mostrar aos amigos secretos o que está pensando, coloque '.' antes do pensamento.",
                       "Se um "+ Cog +" estiver atordoado, será mais difícil para ele desviar de objetos cadentes.",
                       "Cada tipo de edifício "+ Cog +" possui um visual diferente.",
                       "Derrotar os "+ Cogs +" nos andares mais altos de um edifício dará a você maiores recompensas de habilidade.",
                       )
QuestsDefaultTierNotDone = ("Olá, _avName_! Você deve concluir sua Tarefa Toon atual antes de começar uma nova.",
                            "E aí? Você precisa concluir suas Tarefas Toon atuais antes de começar uma nova.",
                            "Oi, _avName_! Para que eu possa dar a você uma nova Tarefa Toon, você precisa terminar as que você tem.",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("Ouvi falar que _toNpcName_ está procurando por você._where_",
                                 "Passe por lá e visite _toNpcName_ quando tiver um tempinho._where_",
                                 "Visite _toNpcName_ da próxima vez em que estiver passando por aquele caminho._where_",
                                 "Se tiver um tempinho, pare e diga olá para _toNpcName_._where_",
                                 "_toNpcName_ dará a você sua nova Tarefa Toon._where_",
                                 )
# Quest dialog
QuestsLocationArticle = ""
def getLocalNum(num):
	if (num <=9):
		return str(num) + ""
	else:
		return str(num)
QuestsItemNameAndNum = "%(num)s %(name)s"

QuestsCogQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogQuestHeadline = "PROCURADO"
QuestsCogQuestSCStringS = "Eu preciso derrotar %(cogName)s%(cogLoc)s"
QuestsCogQuestSCStringP = "Eu preciso derrotar alguns %(cogName)s%(cogLoc)s."
QuestsCogQuestDefeat = "Derrotar %s"
QuestsCogQuestDefeatDesc = "%(numCogs)s %(cogName)s"

QuestsCogNewNewbieQuestObjective = "Ajude um novo Toon a derrotar %s"
QuestsCogNewNewbieQuestCaption = "Ajude um novo Toon que tenha %d risadas ou menos que isso"
QuestsCogOldNewbieQuestObjective = "Ajude um Toon com %(laffPoints)d risadas, ou menos, a dominar %(objective)s"
QuestsCogOldNewbieQuestCaption = "Ajude um Toon com %d risadas, ou menos"
QuestsCogNewbieQuestAux = "Derrotar:"
QuestsNewbieQuestHeadline = "APRENDIZ"

QuestsCogTrackQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogTrackQuestHeadline = "PROCURADO"
QuestsCogTrackQuestSCStringS = "Eu preciso derrotar %(cogText)s%(cogLoc)s."
QuestsCogTrackQuestSCStringP = "Eu preciso derrotar alguns %(cogText)s%(cogLoc)s."
QuestsCogTrackQuestDefeat = "Derrotar %s"
QuestsCogTrackDefeatDesc = "%(numCogs)s %(trackName)s"

QuestsCogLevelQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogLevelQuestHeadline = "PROCURADO"
QuestsCogLevelQuestDefeat = "Derrotar %s"
QuestsCogLevelQuestDesc = "um Nível %(level)s+ Cog"
QuestsCogLevelQuestDescC = "%(count)s Nível %(level)s+ Cogs"
QuestsCogLevelQuestDescI = "algum Nível %(level)s+ Cogs"
QuestsCogLevelQuestSCString = "Eu preciso derrotar %(objective)s%(location)s."

QuestsBuildingQuestFloorNumbers = ('','dois+','três+','quatro+','cinco+')
QuestsBuildingQuestBuilding = "Edifício"
QuestsBuildingQuestBuildings = "Edifícios"
QuestsBuildingQuestHeadline = "DERROTAR"
QuestsBuildingQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsBuildingQuestString = "Derrotar %s"
QuestsBuildingQuestSCString = "Eu preciso derrotar %(objective)s%(location)s."

QuestsBuildingQuestDesc = "um Edifício %(type)s"
QuestsBuildingQuestDescF = "um Edifício %(type)s de %(floors)s andares"
QuestsBuildingQuestDescC = "%(count)s Edifícios %(type)s"
QuestsBuildingQuestDescCF = "%(count)s Edifícios %(type)s de %(floors)s andares"
QuestsBuildingQuestDescI = "alguns Edifícios %(type)s"
QuestsBuildingQuestDescIF = "alguns Edifícios %(type)s de %(floors)s andares"

QuestFactoryQuestFactory = "Fábrica"
QuestsFactoryQuestFactories = "Fábricas"
QuestsFactoryQuestHeadline = "DERROTAR"
QuestsFactoryQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsFactoryQuestString = "Derrotar %s"
QuestsFactoryQuestSCString = "Eu preciso derrotar %(objective)s%(location)s."

QuestsFactoryQuestDesc = "uma Fábrica %(type)s"
QuestsFactoryQuestDescC = "%(count)s Fábricas %(type)s"
QuestsFactoryQuestDescI = "algumas Fábricas %(type)s"

QuestMintQuestMint = "Casa da Moeda"
QuestsMintQuestMints = "Casas da Moeda"
QuestsMintQuestHeadline = "DERROTAR"
QuestsMintQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsMintQuestString = "Derrotar %s"
QuestsMintQuestSCString = "Preciso derrotar %(objective)s%(location)s."

QuestsMintQuestDesc = "uma Casa da Moeda dos Cogs"
QuestsMintQuestDescC = "%(count)s Casas da Moeda dos Cogs"
QuestsMintQuestDescI = "algumas Casas da Moeda dos Cogs"

QuestsRescueQuestProgress = "%(progress)s de %(numToons)s salvos"
QuestsRescueQuestHeadline = "SALVAMENTO"
QuestsRescueQuestSCStringS = "Preciso salvar um Toon%(toonLoc)s."
QuestsRescueQuestSCStringP = "Preciso salvar alguns Toons%(toonLoc)s."
QuestsRescueQuestRescue = "Salvar %s"
QuestsRescueQuestRescueDesc = "%(numToons)s Toons"
QuestsRescueQuestToonS = "um Toon"
QuestsRescueQuestToonP = "Toons"
QuestsRescueQuestAux = "Salvar:"

QuestsRescueNewNewbieQuestObjective = "Ajudar um novo Toon a salvar %s"
QuestsRescueOldNewbieQuestObjective = "Ajude um Toon com %(laffPoints)de risadas, ou menos, a resgatar %(objective)s"

QuestCogPartQuestCogPart = "Parte do Processo Cog"
QuestsCogPartQuestFactories = "Fábricas"
QuestsCogPartQuestHeadline = "RECUPERAR"
QuestsCogPartQuestProgressString = "%(progress)s de %(num)s recuperados"
QuestsCogPartQuestString = "Recuperar %s"
QuestsCogPartQuestSCString = "Preciso recuperar %(objective)s%(location)s."
QuestsCogPartQuestAux = "Recuperar:"

QuestsCogPartQuestDesc = "uma Parte do Processo Cog"
QuestsCogPartQuestDescC = "%(count)s Parte(s) do Processo Cog"
QuestsCogPartQuestDescI = "algumas Partes do Processo Cog"

QuestsCogPartNewNewbieQuestObjective = "Ajude um novo Toon a recuperar %s"
QuestsCogPartOldNewbieQuestObjective = 'Ajude um Toon com %(laffPoints)de risadas, ou menos, a recuperar %(objective)s'

QuestsDeliverGagQuestProgress = "%(progress)s de %(numGags)s entregues"
QuestsDeliverGagQuestHeadline = "ENTREGAR"
QuestsDeliverGagQuestToSCStringS = "Preciso entregar %(gagName)s."
QuestsDeliverGagQuestToSCStringP = "Preciso entregar algumas %(gagName)s."
QuestsDeliverGagQuestSCString = "Preciso fazer uma entrega."
QuestsDeliverGagQuestString = "Entregar %s"
QuestsDeliverGagQuestStringLong = "Entregar %s a _toNpcName_."
QuestsDeliverGagQuestInstructions = "Você pode comprar esta piada na Loja de Piadas quando tiver acesso a ela."

QuestsDeliverItemQuestProgress = ""
QuestsDeliverItemQuestHeadline = "ENTREGAR"
QuestsDeliverItemQuestSCString = "Preciso entregar %(article)s%(itemName)s."
QuestsDeliverItemQuestString = "Entregar %s"
QuestsDeliverItemQuestStringLong = "Entregar %s a _toNpcName_."

QuestsVisitQuestProgress = ""
QuestsVisitQuestHeadline = "VISITAR"
QuestsVisitQuestStringShort = "Visitar"
QuestsVisitQuestStringLong = "Visitar _toNpcName_"
QuestsVisitQuestSeeSCString = "Preciso ver %s."

QuestsRecoverItemQuestProgress = "%(progress)s de %(numItems)s recuperados"
QuestsRecoverItemQuestHeadline = "RECUPERAR"
QuestsRecoverItemQuestSeeHQSCString = "Preciso ver um "+lHQOfficerM+"."
QuestsRecoverItemQuestReturnToHQSCString = "Preciso devolver %s para um "+lHQOfficerM+"."
QuestsRecoverItemQuestReturnToSCString = "Preciso devolver %(item)s para %(npcName)s."
QuestsRecoverItemQuestGoToHQSCString = "Preciso ir a um Quartel dos Toons."
QuestsRecoverItemQuestGoToPlaygroundSCString = "Preciso ir ao Pátio %s."
QuestsRecoverItemQuestGoToStreetSCString = "Preciso ir %(to)s %(street)s em %(hood)s."
QuestsRecoverItemQuestVisitBuildingSCString = "Preciso visitar %s%s."
QuestsRecoverItemQuestWhereIsBuildingSCString = "Onde é %s%s?"
QuestsRecoverItemQuestRecoverFromSCString = "Preciso recuperar %(item)s de %(holder)s%(loc)s."
QuestsRecoverItemQuestString = "Recuperar %(item)s de %(holder)s"
QuestsRecoverItemQuestHolderString = "%(level)s %(holder)d+ %(cogs)s"

QuestsTrackChoiceQuestHeadline = "ESCOLHER"
QuestsTrackChoiceQuestSCString = "Preciso escolher entre %(trackA)s e %(trackB)s."
QuestsTrackChoiceQuestMaybeSCString = "Talvez eu deva escolher %s."
QuestsTrackChoiceQuestString = "Escolha entre %(trackA)s e %(trackB)s"

QuestsFriendQuestHeadline = "AMIGO"
QuestsFriendQuestSCString = "Preciso fazer um amigo."
QuestsFriendQuestString = "Fazer um amigo"

QuestsMailboxQuestHeadline = "CORRESPONDÊNCIA"
QuestsMailboxQuestSCString = "Preciso verificar minha correspondência."
QuestsMailboxQuestString = "Verificar sua correspondência"

QuestsPhoneQuestHeadline = "CLARABELA"
QuestsPhoneQuestSCString = "Preciso ligar para Clarabela."
QuestsPhoneQuestString = "Ligar para Clarabela"

QuestsFriendNewbieQuestString = "Faça %d amigos %d risadas ou menos"
QuestsFriendNewbieQuestProgress = "%(progress)s de %(numFriends)s feitos"
QuestsFriendNewbieQuestObjective = "Faça amizade com %d novos Toons"

QuestsTrolleyQuestHeadline = "BONDINHO"
QuestsTrolleyQuestSCString = "Preciso pegar o bondinho."
QuestsTrolleyQuestString = "Andar no bondinho"
QuestsTrolleyQuestStringShort = "Pegar o bondinho"

QuestsMinigameNewbieQuestString = "%d Minijogos"
QuestsMinigameNewbieQuestProgress = "%(progress)s de %(numMinigames)s jogados"
QuestsMinigameNewbieQuestObjective = "Divirta-se com %d minijogos com a ajuda de novos Toons"
QuestsMinigameNewbieQuestSCString = "Preciso participar de minijogos com novos Toons."
QuestsMinigameNewbieQuestCaption = "Ajude um novo Toon %d risadas ou menos"
QuestsMinigameNewbieQuestAux = "Jogar:"

QuestsMaxHpReward = "Seu Limite de risadas foi aumentado em %s."
QuestsMaxHpRewardPoster = "Recompensa: %s ponto de Acréscimo de risadas"

QuestsMoneyRewardSingular = "Você ganha 1 balinha."
QuestsMoneyRewardPlural = "Você ganha %s balinhas."
QuestsMoneyRewardPosterSingular = "Recompensa: 1 balinha"
QuestsMoneyRewardPosterPlural = "Recompensa: %s balinhas"

QuestsMaxMoneyRewardSingular = "Agora, você pode carregar 1 balinha."
QuestsMaxMoneyRewardPlural = "Agora, você pode carregar %s balinhas."
QuestsMaxMoneyRewardPosterSingular = "Recompensa: Carregue 1 balinha"
QuestsMaxMoneyRewardPosterPlural = "Recompensa: Carregue %s balinhas"

QuestsMaxGagCarryReward = "Você ganha %(name)s. Agora, você pode carregar %(num)s piadas."
QuestsMaxGagCarryRewardPoster = "Recompensa: %(name)s (%(num)s)"

QuestsMaxQuestCarryReward = "Agora, você pode ter %s Tarefas Toon."
QuestsMaxQuestCarryRewardPoster = "Recompensa: Carregue %s Tarefas Toon"

QuestsTeleportReward = "Agora, você tem acesso por teletransporte a %s."
QuestsTeleportRewardPoster = "Recompensa: Acesso por teletransporte a %s"

QuestsTrackTrainingReward = "Agora, você pode treinar para \"%s\" piadas."
QuestsTrackTrainingRewardPoster = "Recompensa: Treinamento de piadas"

QuestsTrackProgressReward = "Agora, você tem o quadro %(frameNum)s da animação do tipo %(trackName)s."
QuestsTrackProgressRewardPoster = "Recompensa: \"Quadro %(frameNum)s da animação do tipo %(trackName)s\""

QuestsTrackCompleteReward = "Agora, você pode carregar e usar \"%s\" piadas."
QuestsTrackCompleteRewardPoster = "Recompensa: Treinamento final do tipo %s"

QuestsClothingTicketReward = "Você pode trocar de roupa"
QuestsClothingTicketRewardPoster = "Recompensa: Bilhete de roupas"

QuestsCheesyEffectRewardPoster = "Recompensa: %s"

TIPQuestsClothingTicketReward = "Você pode trocar sua camisa por uma camisa DICA"
TIPQuestsClothingTicketRewardPoster = "Recompensa: Bilhete de Roupa DICA"

QuestsCogSuitPartReward = "Agora, você tem uma %(cogTrack)s %(part)s peça de vestimenta de Cog."
QuestsCogSuitPartRewardPoster = "Recompensa: %(cogTrack)s %(part)s Peça"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "neste pátio"
QuestsStreetLocationThisStreet = "nesta rua"
QuestsStreetLocationNamedPlayground = "no pátio %s"
QuestsStreetLocationNamedStreet = "na %(toStreetName)s em %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "O edifício de %s's chama-se"
QuestsLocationBuildingVerb = "o qual é"
QuestsLocationParagraph = "\a%(building)s \"%(buildingName)s\"...\a...%(buildingVerb)s %(street)s."
QuestsGenericFinishSCString = "Preciso terminar uma Tarefa Toon."

# MaxGagCarryReward names
QuestsMediumPouch = "Sacola média"
QuestsLargePouch = "Sacola grande"
QuestsSmallBag = "Bolsa pequena"
QuestsMediumBag = "Bolsa média"
QuestsLargeBag = "Bolsa grande"
QuestsSmallBackpack = "Mochila pequena"
QuestsMediumBackpack = "Mochila média"
QuestsLargeBackpack = "Mochila grande"
QuestsItemDict = {
    1 : ["Par de óculos", "Pares de óculos", "um "],
    2 : ["Chave", "Chaves", "uma "],
    3 : ["Quadro-negro", "Quadros-negros", "um "],
    4 : ["Livro", "Livros", "um "],
    5 : ["Chocolate", "Chocolates", "um "],
    6 : ["Pedaço de giz", "Pedaços de giz", "um "],
    7 : ["Receita", "Receitas", "uma "],
    8 : ["Nota", "Notas", "uma "],
    9 : ["Calculadora", "Calculadoras", "uma "],
    10 : ["Pneu de carro de palhaço", "Pneus de carro de palhaço", "um "],
    11 : ["Bomba de ar", "Bombas de ar", "uma "],
    12 : ["Tinta de polvo", "Tintas de polvo", "uma "],
    13 : ["Pacotes", "Pacotes", "um "],
    14 : ["Recibo de peixe dourado", "Recibos de peixe dourado", "um "],
    15 : ["Peixe dourado", "Peixe dourado", "um "],
    16 : ["Óleo", "Óleos", "um pouco de "],
    17 : ["Graxa", "Graxas", "um pouco de "],
    18 : ["Água", "Águas", "uma "],
    19 : ["Relatório de engrenagens", "Relatórios de engrenagens", "um "],
    20 : ["Apagador de quadro-negro", "Apagadores de quadro-negro", "a "],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    110 : ["Bilhete de Roupa DICA", "Bilhetes de Roupa", "um"],
    1000 : ["Bilhete de roupas", "Bilhetes de roupas", "um "],

    # Donald's Dock quest items
    2001 : ["Câmara de ar", "Câmaras de ar", "uma "],
    2002 : ["Receita de monóculo", "Receita de monóculo", "uma "],
    2003 : ["Armação de óculos", "Armações de óculos", "algumas "],
    2004 : ["Monóculo", "Monóculos", "um "],
    2005 : ["Grande peruca branca", "Grandes perucas brancas", "uma "],
    2006 : ["Alqueire de cascalho", "Alqueires de cascalho", "um "],
    2007 : ["Engrenagem Cog", "Engrenagens de Cog", "uma "],
    2008 : ["Carta marinha", "Cartas marinhas", "uma "],
    2009 : ["Braçadeira suja", "Braçadeiras sujas", "uma "],
    2010 : ["Braçadeira limpa", "Braçadeiras limpas", "uma "],
    2011 : ["Mola de relógio", "Molas de relógio", "uma "],
    2012 : ["Contrapeso", "Contrapesos", "um "],

    # Minnie's Melodyland quest items
    4001 : ["Estoque da Tina", "Estoques da Tina", ""],
    4002 : ["Estoque da Cavaca", "Estoques da Cavaca", ""],
    4003 : ["Formulário de estoque", "Formulários de estoque", "um "],
    4004 : ["Estoque da Fifi", "Estoques da Fifi", ""],
    4005 : ["Passagem do Alê Nhador", "Passagens do Alê Nhador", ""],
    4006 : ["Passagem da Tábata", "Passagens da Tábata", ""],
    4007 : ["Passagem do Barry", "Passagens do Barry", ""],
    4008 : ["Castanhola fosca", "Castanholas foscas", ""],
    4009 : ["Tinta de lula azul", "Tintas de lula azul", "obter "],
    4010 : ["Castanhola polida", "Castanholas polidas", "uma "],
    4011 : ["Letra de música do Léo", "Letras de músicas do Léo", ""],

    # Daisy's Gardens quest items
    5001 : ["Gravata de seda", "Gravatas de seda", "uma "],
    5002 : ["Terno listrado", "Ternos listrados", "um "],
    5003 : ["Tesoura", "Tesouras", "uma "],
    5004 : ["Cartão-postal", "Cartões-postais", "um "],
    5005 : ["Caneta", "Canetas", "uma "],
    5006 : ["Tinteiro", "Tinteiros", "um "],
    5007 : ["Bloco de notas", "Blocos de notas", "um "],
    5008 : ["Cofre de escritório", "Cofres de escritório", "um "],
    5009 : ["Saco de ração para pássaros", "Sacos de ração para pássaros", "um "],
    5010 : ["Roda dentada", "Rodas dentadas", "uma "],
    5011 : ["Salada", "Saladas", "uma "],
    5012 : ["Chave para os Jardins da Margarida", "Chaves para os Jardins da Margarida", "uma "],
    5013 : ["Mapa do "+lSellbotHQ, "Mapas do "+lSellbotHQ, "alguns "],
    5014 : ["Memorando do "+lSellbotHQ, "Memorandos do "+lSellbotHQ, "um "],
    5015 : ["Memorando do "+lSellbotHQ, "Memorandos do "+lSellbotHQ, "um "],
    5016 : ["Memorando do "+lSellbotHQ, "Memorandos do "+lSellbotHQ, "um "],
    5017 : ["Memorando do "+lSellbotHQ, "Memorandos do "+lSellbotHQ, "um "],

    # The Brrrgh quests
    3001 : ["Bola de futebol", "Bolas de futebol", "uma "],
    3002 : ["Tobogã", "Tobogãs", "um "],
    3003 : ["Cubo de gelo", "Cubos de gelo", "um "],
    3004 : ["Carta de amor", "Cartas de amor", "uma "],
    3005 : ["Cão-linguiça", "cães-linguiça", "um "],
    3006 : ["Anel de noivado", "Anéis de noivado", "um "],
    3007 : ["Bigode de sardinha", "Bigodes de sardinhas", "um pouco de "],
    3008 : ["Poção calmante", "Poções calmantes", "uma "],
    3009 : ["Dente quebrado", "Dentes quebrados", "um "],
    3010 : ["Dente de ouro", "Dentes de ouro", "um "],
    3011 : ["Pão de pinha", "Pães de pinha", "um "],
    3012 : ["Coco em pedaços", "Cocos em pedaços", "um pouco de "],
    3013 : ["Colher simples", "Colheres simples", "uma "],
    3014 : ["Sapo falante", "Sapos falantes", "um "],
    3015 : ["Casquinha de sorvete", "Casquinhas de sorvete", "uma "],
    3016 : ["Pó de peruca", "Pós de perucas", "um pouco de "],
    3017 : ["Patinho de borracha", "Patinhos de borracha", "um "],
    3018 : ["Dados de pelúcia", "Dados de pelúcia", "alguns "],
    3019 : ["Microfone", "Microfones", "um "],
    3020 : ["Teclado elétrico", "Teclados elétricos", "um "],
    3021 : ["Sapatos de plataforma", "Sapatos de plataforma", "alguns "],
    3022 : ["Caviar", "Caviar", "um pouco de "],
    3023 : ["Pó de arroz", "Pó de arroz", "um pouco de "],
    3024 : ["Fio", "Fios", "alguns " ],
    3025 : ["Agulha de Tricô", "Agulhas de Tricô", "uma "],
    3026 : ["Álibi", "Álibis", "um "],
    3027 : ["Termômetro Externo", "Termômetros Externos", "um "],
    
    #Dreamland Quests
    6001 : ["Plano do "+lCashbotHQ, "Planos do "+lCashbotHQ, "algum "],
    6002 : ["Vara de pescar", "Varas de pescar", "uma "],
    6003 : ["Cinto de segurança", "Cintos de segurança", "um "],
    6004 : ["Par de pinças", "Pares de pinças", "um "],
    6005 : ["Abajur de leitura", "Abajures de leitura", "um "],
    6006 : ["Cítara", "Cítaras", "uma "],
    6007 : ["Zamboni", "Zambonis", "uma "],
    6008 : ["Zabuton de zebra", "Zabutons de zebra", "uma "],
    6009 : ["Zinnias", "Zinnias", "alguns "],
    6010 : ["Discos de forró", "Discos de forró", "algum "],
    6011 : ["Abobrinha", "Abobrinhas", "uma "],
    6012 : ["Paletó zoot", "Paletós zoot", "um "],

    #Dreamland+1 quests
    7001 : ["Cama comum", "Camas comuns", "uma "],
    7002 : ["Cama elegante", "Camas elegantes", "uma "],
    7003 : ["Colcha azul", "Colchas azuis", "uma "],
    7004 : ["Colcha estampada", "Colchas estampadas ", "uma"],
    7005 : ["Travesseiros", "Travesseiros", "alguns "],
    7006 : ["Travesseiros duros", "Travesseiros duros ", "um"],
    7007 : ["Pijamas", "Pijamas", "um par de "],
    7008 : ["Pijamas com pés", "Pijamas com pés", "um par de "],
    7009 : ["Pijamas com pés marrons", "Pijamas com pés marrons", "um par de "],
    7010 : ["Pijamas com pés fúcsia", "Pijamas com pés fúcsia", "um par de "],
    7011 : ["Coral de couve-flor", "Coral de couve-flor", "algumas "],
    7012 : ["Alga-marinha viscosa", "Alga-marinha viscosa", "um "],
    7013 : ["Pilão", "Pilões", "um "],
    7014 : ["Pote de creme para rugas", "Potes de creme para rugas", "um "],
    }

QuestsHQOfficerFillin = lHQOfficerM
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = lToonHQ
QuestsHQLocationNameFillin = "em qualquer bairro"

QuestsTailorFillin = "Costureiro"
QuestsTailorWhereFillin = ""
QuestsTailorBuildingNameFillin = "Loja de Roupas"
QuestsTailorLocationNameFillin = "em qualquer bairro"
QuestsTailorQuestSCString = "Preciso ir ao Costureiro."

QuestMovieQuestChoiceCancel = "Volte mais tarde se precisar de uma Tarefa Toon! Tchau!"
QuestMovieTrackChoiceCancel = "Volte quando já tiver decidido o que fazer! Tchau!"
QuestMovieQuestChoice = "Escolha uma Tarefa Toon."
QuestMovieTrackChoice = "Já decidiu o que escolher? Escolha um tipo ou volte mais tarde."

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
    QUEST : "Agora, você está pronto.\aSaia e refresque a cabeça até descobrir que tipo você gostaria de escolher.\aEscolha bem, pois você não poderá mudar.\aQuando tiver certeza, volte aqui.",
    INCOMPLETE_PROGRESS : "Escolha bem.",
    INCOMPLETE_WRONG_NPC : "Escolha bem.",
    COMPLETE : "Ótima escolha!",
    LEAVING : "Boa sorte. Volte aqui quando tiver dominado sua nova habilidade.",
    }

QuestDialog_3225 = {
    QUEST : "Puxa, obrigado por vir, _avName_!\aOs Cogs que estão no bairro assustaram o rapaz que faz as entregas.\aEu não tenho quem entregue esta salada para _toNpcName_!\aVocê poderia fazer isso por mim? Muitíssimo obrigado!_where_"
    }

QuestDialog_2910 = {
    QUEST : "De volta tão rápido assim?\aÓtimo trabalho com aquela mola.\aO último item é um contrapeso.\aPasse lá, veja com _toNpcName_ e traga o que você conseguir._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "Ok, agora acho que você está pronto para um desafio maior.\aDerrote 3 Robôs-chefe.",
           INCOMPLETE_PROGRESS : "Os "+ Cogs +" estão soltos pelas ruas e pelos túneis.",
           INCOMPLETE_WRONG_NPC : "Bom trabalho com os Robôs-chefe. Vá agora para o Quartel dos Toons para receber sua recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "Ok, agora acho que você está pronto para um desafio maior.\aDerrote 3 Robôs da Lei.",
           INCOMPLETE_PROGRESS : "Os "+ Cogs +" estão soltos pelas rua e pelos túneis.",
           INCOMPLETE_WRONG_NPC : "Bom trabalho com os Robôs da Lei. Vá agora para o Quartel dos Toons para receber sua recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    162 : {GREETING : "",
           QUEST : "Ok, agora acho que você está pronto para um desafio maior.\aDerrote 3 Robôs Mercenários.",
           INCOMPLETE_PROGRESS : "Os "+ Cogs +" estão soltos pelas ruas e pelos túneis.",
           INCOMPLETE_WRONG_NPC : "Bom trabalho com os Robôs Mercenários. Vá agora para o Quartel dos Toons para receber sua recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    163 : {GREETING : "",
           QUEST : "Ok, agora acho que você está pronto para um desafio maior.\aDerrote 3 Robôs Vendedores.",
           INCOMPLETE_PROGRESS : "Os "+ Cogs +" estão soltos pelas ruas e pelos túneis.",
           INCOMPLETE_WRONG_NPC : "Bom trabalho com os Robôs Vendedores. Vá agora para o Quartel dos Toons para receber sua recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    164 : {QUEST : "Parece que você precisa de novas piadas.\aVisite o Flippy, talvez ele possa ajudá-lo._where_" },
    165 : {QUEST : "Olá.\aParece que você precisa praticar suas piadas.\aToda vez que você atinge um Cog com uma de suas piadas, sua experiência aumenta.\aQuando tiver experiência suficiente, você será capaz de usar uma piada ainda melhor.\aVá praticar suas piadas derrotando 4 Cogs."},
    166 : {QUEST : "Bom trabalho com aqueles Cogs.\aSabia que existem quatro tipos diferentes de Cogs?\aEles são os Robôs da Lei, os Robôs Mercenários, os Robôs Vendedores e os Robôs-chefe.\aVocê pode diferenciá-los pela cor e pelas etiquetas com os nomes.\aPara praticar, derrote 4 Robôs-chefe."},
    167 : {QUEST : "Bom trabalho com aqueles Cogs.\aSabia que existem quatro tipos diferentes de Cogs?\aEles são os Robôs da Lei, os Robôs Mercenários, os Robôs Vendedores e os Robôs-chefe.\aVocê pode diferenciá-los pela cor e pelas etiquetas com os nomes.\aPara praticar, derrote 4 Robôs da Lei."},
    168 : {QUEST : "Bom trabalho com aqueles Cogs.\aSabia que existem quatro tipos diferentes de Cogs?\aEles são os Robôs da Lei, os Robôs Mercenários, os Robôs Vendedores e os Robôs-chefe.\aVocê pode diferenciá-los pela cor e pelas etiquetas com os nomes.\aPara praticar, derrote 4 Robôs Vendedores."},
    169 : {QUEST : "Bom trabalho com aqueles Cogs.\aSabia que existem quatro tipos diferentes de Cogs?\aEles são os Robôs da Lei, os Robôs Mercenários, os Robôs Vendedores e os Robôs-chefe.\aVocê pode diferenciá-los pela cor e pelas etiquetas com os nomes.\aPara praticar, derrote 4 Robôs Mercenários."},
    170 : {QUEST : "Bom trabalho; agora você sabe a diferença entre os 4 tipos de Cogs.\aAcho que você está pronto para começar a treinar o seu terceiro tipo de piada.\aFale com _toNpcName_ para escolher o seu próximo tipo de piada - ele pode dar alguns conselhos especiais para você._where_" },
    171 : {QUEST : "Bom trabalho; agora você sabe a diferença entre os 4 tipos de Cogs.\aAcho que você está pronto para começar a treinar o seu terceiro tipo de piada.\aFale com _toNpcName_ para escolher o seu próximo tipo de piada - ele pode dar alguns conselhos especiais para você._where_" },
    172 : {QUEST : "Bom trabalho; agora você sabe a diferença entre os 4 tipos de Cogs.\aAcho que você está pronto para começar a treinar o seu terceiro tipo de piada.\aFale com _toNpcName_ para escolher o seu próximo tipo de piada - ela pode dar alguns conselhos especiais para você._where_" },

    175 : {GREETING : "",
           QUEST : "Você sabia que possui sua própria casa Toon?\aA vaca Clarabela administra um catálogo telefônico no qual você pode escolher e encomendar móveis para decorar sua casa.\aVocê também pode comprar frases do Chat Rápido, roupas e outras coisas muito legais!\aPedirei à Clarabela para enviar agora a você seu primeiro catálogo.\aVocê receberá um catálogo com novos itens toda semana!\aVá para sua casa e use o seu telefone para ligar para Clarabela.",
           INCOMPLETE_PROGRESS : "Vá para casa e use o seu telefone para ligar para Clarabela.",
           COMPLETE : "Espero que você se divirta fazendo encomendas com Clarabela!\a Acabei de redecorar minha casa. Está Toontástica!\aContinue com as Tarefas Toon para ganhar mais recompensas!",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "Lançamento e Esguicho são tipos ótimos, mas você vai precisar de mais piadas para lutar com Cogs de níveis mais altos.\aQuando você se juntar com outros Toons para enfrentar os Cogs, pode combinar ataques para conseguir danos maiores ao inimigo.\aTente diferentes combinações de Piadas para ver o que funciona melhor.\aPara o seu próximo tipo, escolha as Sonoras ou Toonar.\aAs Sonoras são especiais, pois quando atingem algum Cog, todos os outros também sofrem danos.\aAs Toonar permitem curar outros Toons durante a batalha.\aQuando estiver pronto para decidir, venha aqui e escolha uma.",
           INCOMPLETE_PROGRESS : "De volta tão rápido? Ok, você está pronto para escolher?",
           INCOMPLETE_WRONG_NPC : "Pense bem sobre sua decisão antes de escolher.",
           COMPLETE : "Boa decisão. Agora, antes de usar estas piadas, você deve treinar.\aVocê deve completar uma série de Tarefas Toon como treinamento.\aCada tarefa dará a você um único quadro da animação do seu ataque de piadas.\aQuando você coletar todas as 15, poderá obter a tarefa Treinamento final de piadas, que lhe permitirá usar suas novas piadas.\aVocê pode verificar seu progresso no Álbum Toon.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Visite _toNpcName_ se desejar transitar pela cidade com mais facilidade._where_" },
    1040 : { QUEST : "Visite _toNpcName_ se desejar transitar pela cidade com mais facilidade._where_" },
    1041 : { QUEST : "Oi! O que o traz aqui?\aTodo mundo usa o buraco portátil para andar por Toontown.\aÉ, você pode se teletransportar até seus amigos, usando a Lista de amigos, ou até qualquer bairro, usando o mapa no Álbum Toon.\aÉ claro que você precisa consegui-lo!\aOlha, eu posso ativar seu acesso por teletransporte até o Centro de Toontown se você ajudar um amigo meu.\aParece que os Cogs estão dando problema na Travessa dos Tontos. Visite _toNpcName_._where_" },
    1042 : { QUEST : "Oi! O que o traz aqui?\aTodo mundo usa o buraco portátil para andar por Toontown.\aÉ, você pode se teletransportar até seus amigos, usando a Lista de amigos, ou até qualquer bairro, usando o mapa no Álbum Toon.\aÉ claro que você precisa consegui-lo!\aOlha, eu posso ativar seu acesso por teletransporte até o Centro de Toontown se você ajudar um amigo meu.\aParece que os Cogs estão dando problema na Travessa dos Tontos. Visite _toNpcName_._where_" },
    1043 : { QUEST : "Oi! O que o traz aqui?\aTodo mundo usa o buraco portátil para andar por Toontown.\aÉ, você pode se teletransportar até seus amigos, usando a Lista de amigos, ou até qualquer bairro, usando o mapa no Álbum Toon.\aÉ claro que você precisa consegui-lo!\aOlha, eu posso ativar seu acesso por teletransporte até o Centro de Toontown se você ajudar um amigo meu.\aParece que os Cogs estão dando problema na Travessa dos Tontos. Visite _toNpcName_._where_" },
    1044 : { QUEST : "Puxa, obrigado por passar por aqui. Eu realmente preciso de ajuda.\aComo você pode ver, eu não tenho clientes.\aO meu livro de receitas secreto está perdido e ninguém mais vem ao meu restaurante.\aA última vez que eu o vi foi pouco antes de os Cogs tomarem meu edifício.\aVocê pode me ajudar recuperando quatro de minhas receitas favoritas?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu recuperar minhas receitas?" },
    1045 : { QUEST : "Valeu mesmo!\aLogo terei de volta minha coleção completa e poderei reabrir meu restaurante.\aAh, há uma nota aqui para você - algo sobre acesso por teletransporte?\aDiz: \"obrigado por ajudar meu amigo e, por favor, entregue isto ao Quartel dos Toons\".\aBem, valeu mesmo - tchau!",
             LEAVING : "",
             COMPLETE : "Ah, sim, aqui diz que você foi de grande ajuda para alguns dos caras mais legais da Travessa dos Tontos.\aDiz também que você precisa de acesso por teletransporte para o Centro de Toontown.\aBem, considere concedido.\aAgora, você pode se teletransportar de volta para o pátio, de praticamente qualquer lugar de Toontown.\aBasta abrir o seu mapa e clicar em Centro de Toontown." },
    1046 : { QUEST : "Os Robôs Mercenários têm importunado bastante a Financeira Dinheiro Feliz.\aPasse por lá e veja se há algo que você possa fazer._where_" },
    1047 : { QUEST : "Os Robôs Mercenários têm se infiltrado no banco e roubado nossas calculadoras.\aRecupere 5 calculadoras dos Robôs Mercenários.\aPara evitar que você fique indo para lá e para cá, traga-as todas de uma vez.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda procurando pelas calculadoras?" },
    1048 : { QUEST : "Uau! Valeu mesmo por encontrar nossas calculadoras.\aHumm... Elas parecem danificadas.\aVocê poderia levá-las para a loja de _toNpcName_, \"Máquinas de Cosquinhas\", nesta rua?\aVeja se podem consertá-las.",
             LEAVING : "", },
    1049 : { QUEST : "O que é isto? Calculadoras quebradas?\aRobôs Mercenários?\aBem, vamos dar uma olhada...\aÉ, as engrenagens estão partidas mas eu estou sem essa peça...\aSabe o que poderia dar jeito? Algumas engrenagens de Cog, das grandes, dos Cogs maiores...\aEngrenagens de Cogs de nível 3 devem servir. Precisarei de 2 para cada máquina, 10 no total.\aTraga-as todas de uma vez e eu as consertarei!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Lembre-se, eu preciso de 10 engrenagens para consertar as máquinas." },
    1053 : { QUEST : "Ah sim, isto deve servir.\aTudo consertado agora, grátis.\aLeve-as de volta para a Dinheiro Feliz e diga olá a ela por mim.",
             LEAVING : "",
             COMPLETE : "Calculadoras consertadas?\aBom trabalho. Tenho certeza de que tenho algo por aqui para recompensar você..." },
    1054 : { QUEST : "_toNpcName_ precisa de alguma ajuda com seus carros de palhaço._where_" },
    1055 : { QUEST : "Oláááá! Eu não consigo encontrar os pneus para este carro de palhaço em lugar nenhum!\aVocê acha que pode me ajudar?\aEu acho que o Tito Tonto pode ter jogado os pneus no lago do pátio do Centro de Toontown.\aSe você ficar em um dos cais de lá, poderá tentar pescar os pneus para mim.",
             GREETING : "Iuhuu!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você está tendo problemas para pescar os 4 pneus?" },
    1056 : { QUEST : "Demorôô! Agora, este velho carro de palhaço vai poder voltar às ruas!\aEi, eu pensei que tivesse uma bomba de ar aqui para inflar estes pneus...\aAcho que _toNpcName_ pegou emprestado.\aVocê poderia pedir de volta para mim?_where_",
             LEAVING : "" },
    1057 : { QUEST : "E aí?\aUma bomba de pneus?\aVamos fazer o seguinte: você me ajuda a retirar das ruas alguns desses Cogs de alto nível...\aE, então, darei a você a bomba de pneus.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Isso é o melhor que você pode fazer?" },
    1058 : { QUEST : "Bom trabalho! Eu sabia que você conseguiria.\aAqui está a bomba. Estou certo de que _toNpcName_ ficará feliz em recebê-la de volta.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Dez! Agora está tudo certo!\aPor falar nisso, obrigado por me ajudar.\aAqui, tome isto." },
    1059 : { QUEST : "_toNpcName_ está com poucos suprimentos. Quem sabe você pode ajudá-lo?_where_" },
    1060 : { QUEST : "Valeu mesmo por passar aqui!\aOs Cogs roubam sempre a minha tinta e, por isso, ela está quase no fim.\aVocê poderia pescar um pouco de tinta de polvo para mim no lago?\aPara pescar, basta ficar parado em um cais perto do lago.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você está tendo problemas para pescar?" },
    1061 : { QUEST : "Ótimo, valeu pela tinta!\aSabe de uma coisa, se você eliminasse alguns daqueles Ratos de Escritório...\aAí minha tinta não acabaria tão rápido.\aDerrote 6 Ratos de Escritório no Centro de Toontown para receber sua recompensa.",
             LEAVING : "",
             COMPLETE : "Valeu! Vou recompensar você pela sua ajuda.",
             INCOMPLETE_PROGRESS : "Eu acabei de ver mais alguns Ratos de Escritório." },
    1062 : { QUEST : "Ótimo, valeu pela tinta!\aSabe de uma coisa? Se você eliminasse alguns daqueles Sanguessugas...\aAí minha tinta não acabaria tão rápido.\aDerrote 6 Sanguessugas no Centro de Toontown para receber sua recompensa.",
             LEAVING : "",
             COMPLETE : "Valeu! Vou recompensar você pela sua ajuda.",
             INCOMPLETE_PROGRESS : "Eu acabei de ver mais alguns Sanguessugas." },
    900 : { QUEST : "Fiquei sabendo que _toNpcName_ precisa de ajuda com um pacote._where_" },
    1063 : { QUEST : "Olá! Legal você ter vindo.\aUm Cog roubou um pacote muito importante bem debaixo do meu nariz.\aVeja se você consegue recuperá-lo. Eu acho que ele era de nível 3...\aEntão, derrote Cogs de nível 3 até encontrar meu pacote.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não teve sorte de encontrar o pacote, né?" },
    1067 : { QUEST : "É ele mesmo, está tudo certo!\aEi, o endereço está borrado...\aTudo o que eu posso ler é que é para um Dr. - o resto está ilegível.\aTalvez seja para _toNpcName_? Você pode levar para ele?_where_",
             LEAVING : "" },
    1068 : { QUEST : "Eu não estava esperando um pacote. Talvez seja para o Dr. E.U. Fórico.\aMeu assistente ia passar mesmo lá hoje, então pedirei a ele que verifique para você.\aNesse meio tempo, você se importaria de se livrar de alguns dos Cogs que estão na minha rua?\aDerrote 10 Cogs no Centro de Toontown.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Meu assistente ainda não voltou." },
    1069 : { QUEST : "O Dr. Fórico disse que também não estava esperando nenhum pacote.\aInfelizmente um Robô Mercenário roubou o pacote de meu assistente no caminho de volta.\aVocê poderia tentar pegá-lo de volta?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não teve sorte de encontrar o pacote, né?" },
    1070 : { QUEST : "O Dr. Fórico disse que também não estava esperando nenhum pacote.\aInfelizmente um Robô Vendedor roubou o pacote de meu assistente no caminho de volta.\aSinto muito, mas você terá que encontrar esse Robô Vendedor para pegá-lo de volta.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não teve sorte de encontrar o pacote, né?" },
    1071 : { QUEST : "O Dr. Fórico disse que também não estava esperando nenhum pacote.\aInfelizmente um Robô-chefe roubou o pacote de meu assistente no caminho de volta.\aVocê poderia tentar pegá-lo de volta?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não teve sorte de encontrar o pacote, né?" },
    1072 : { QUEST : "Ótimo, você o pegou de volta!\aTalvez você deva tentar entregá-lo a _toNpcName_, pode ser para ele._where_",
             LEAVING : "" },
    1073 : { QUEST : "Puxa, obrigado por trazer meus pacotes para mim.\aEspere um segundo, eu estava esperando dois. Você poderia verificar com _toNpcName_ e ver se ele está com o outro?",
             INCOMPLETE : "Conseguiu encontrar meu outro pacote?",
             LEAVING : "" },
    1074 : { QUEST : "Ele disse que havia outro pacote? Talvez os Cogs o tenham roubado também.\aDerrote Cogs até encontrar o segundo pacote.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não teve sorte de encontrar o outro pacote, né?" },
    1075 : { QUEST : "No final das contas, acho que não havia um segundo pacote!\aCorra e leve-o para _toNpcName_, com minhas desculpas.",
             COMPLETE : "Ei, meu pacote está aqui!\aJá que você parece ser um Toon tão prestativo, isto vai ser fichinha.",
             LEAVING : "" },
    1076 : { QUEST : "Houve alguns problemas na Peixinhos Dourados Ki-late.\a_toNpcName_ provavelmente podem precisar de você._where_" },
    1077 : { QUEST : "Legal você ter vindo. Os Cogs roubaram todos os meus peixes dourados.\aEu acho que os Cogs querem vendê-los para ganhar dinheiro fácil.\aHá muitos anos, aqueles 5 peixes têm sido minhas únicas companhias nesta pequena loja ...\aSe você pudesse recuperá-los, eu agradeceria muito.\aTenho certeza de que os Cogs estão com meus peixes.\aDerrote Cogs até encontrar meus peixes dourados.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Consiga meus peixes dourados de volta." },
    1078 : { QUEST : "Puxa, você recuperou meus peixes!\aHã? O que é isto - um recibo?\aAi, ai... Acho que eles são Cogs mesmo.\aEu não consigo decifrar este recibo. Você poderia levá-lo para _toNpcName_ e ver se ele consegue lê-lo?_where_",
             INCOMPLETE : "O que _toNpcName_ disse sobre o recibo?",
             LEAVING : "" },
    1079 : { QUEST : "Humm, deixe-me ver este recibo.\a...Ah, sim, diz que 1 peixe dourado foi vendido para um Puxa-saco.\aO recibo não menciona o que aconteceu com os outros 4 peixes.\aTalvez você deva tentar encontrar esse Puxa-saco.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Acho que não há mais nada em que eu possa ajudar.\aPor que você não tenta encontrar aquele peixe dourado?" },
    1092 : { QUEST : "Humm, deixe-me ver este recibo.\a...Ah, sim, diz que 1 peixe dourado foi vendido para um Farsante.\aO recibo não menciona o que aconteceu com os outros 4 peixes.\aTalvez você deva tentar encontrar esse Farsante.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Acho que não há mais nada em que eu possa ajudar.\aPor que você não tenta encontrar aquele peixe dourado?" },
    1080 : { QUEST : "Ah, graças aos céus! Você encontrou Oscar - ele é o meu favorito.\aO que foi, Oscar? Hã-hã... Verdade? ... Estão?\aOscar diz que os outros 4 escaparam para dentro do lago no pátio.\aVocê poderia reuni-los para mim?\aÉ só pescá-los no lago.",
             LEAVING : "",
             COMPLETE : "Nossa, estou tããão feliz! Estou junto com meus companheiros novamente!\aVocê merece uma bela recompensa por isso!",
             INCOMPLETE_PROGRESS : "Você está tendo problemas para pescar esses peixes?" },
    1081 : { QUEST : "_toNpcName_ parece estar numa situação grudenta. Ela, com certeza, apreciaria alguma ajuda._where_" },
    1082 : { QUEST : "Eu derramei supercola e estou presa - presa pra valer!\aSe houver uma maneira de sair, eu gostaria de saber.\aIsso me dá uma ideia; abra os olhos.\aDerrote alguns Robôs Vendedores e traga de volta um pouco de óleo.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Você pode me ajudar a descolar daqui?" },
    1083 : { QUEST : "Bem, o óleo ajudou um pouco, mas eu ainda não consigo me mexer.\aO que mais poderia ajudar? É difícil dizer.\aIsso me dá uma ideia; vale a pena tentar.\aDerrote alguns Robôs da Lei e me traga graxa.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Você pode me ajudar a descolar daqui?" },
    1084 : { QUEST : "Não, isso não ajudou. Isso realmente não é engraçado.\aEu coloquei a graxa bem ali,\aIsso me dá uma ideia, não me deixe esquecer.\aDerrote alguns Robôs Mercenários e traga água para umedecer.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "Oba! Estou livre da supercola,\aComo recompensa, dou este presente a você.\aVocê pode rir um pouco mais enquanto luta e, então...\aAh, não! Já estou presa aqui novamente!",
             INCOMPLETE_PROGRESS : "Você pode me ajudar a descolar daqui?" },
    1085 : { QUEST : "_toNpcName_ está fazendo uma pesquisa sobre os Cogs.\aVá falar com ele para ver se ele precisa da sua ajuda._where_" },
    1086 : { QUEST : "É verdade, estou fazendo um estudo sobre os Cogs.\aEu quero aprender sobre o comportamento deles.\aCom certeza ajudaria se você pudesse reunir algumas engrenagens de Cogs.\aMas elas têm que ser de Cogs de nível 2, pelo menos, para serem grandes o suficiente para o exame visual.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não conseguiu encontrar engrenagens suficientes?" },
    1089 : { QUEST : "Certo, vamos dar uma olhada. Estas são amostras excelentes!\aHummm...\aCerto, aqui está meu relatório. Leve isto de volta imediatamente para o Quartel dos Toons.",
             INCOMPLETE : "Você entregou meu relatório no Quartel?",
             COMPLETE : "Bom trabalho _avName_, nós assumiremos a partir daqui.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ tem informações úteis para você._where_" },
    1091 : { QUEST : "Fiquei sabendo que o Quartel dos Toons está trabalhando em uma espécie de Radar de Cogs.\aEle permite ver onde os Cogs estão, para que seja mais fácil encontrá-los.\aA Página de Cogs em seu Álbum Toon é a chave.\aAo derrotar Cogs suficientes, você pode sintonizar os sinais deles e rastrear onde estão.\aContinue derrotando Cogs para ficar pronto.",
             COMPLETE : "Bom trabalho! Você provavelmente vai poder fazer uso disso...",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "Agora, você tem que escolher o próximo tipo de piada que deseja aprender.\aDecida e depois volte aqui quando estiver pronto para escolher.",
           INCOMPLETE_PROGRESS : "Pense bem sobre sua decisão antes de escolher.",
           INCOMPLETE_WRONG_NPC : "Pense bem sobre sua decisão antes de escolher.",
           COMPLETE : "Uma boa decisão...",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "Aqueles cogs traiçoeiros estão envolvidos nisto novamente.\a_toNpcName_ reportou outro item ausente. Pare um pouco aqui e veja se consegue acertar isso._where_" },
    2202 : { QUEST : "Oi, _avName_. Ainda bem que você está aqui. Um Mão de vaca de má aparência acabou de passar por aqui e saiu com uma câmara de ar.\aTemo que ele possa usá-la para seus planos diabólicos.\aVeja se você consegue encontrá-la e trazê-la de volta.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu achar minha câmara de ar?",
             COMPLETE : "Você encontrou minha câmara de ar! Você é legal MESMO! Olha aqui, tome a sua recompensa...",
             },
    2203 : { QUEST : "Os cogs estão espalhando o caos no banco.\aVá até o Capitão Carlão e veja o que você pode fazer._where_" },
    2204 : { QUEST : "Bem-vindo a bordo, colega.\aDroga! Aqueles cogs patifes quebraram meu monóculo e eu não vivo sem ele.\aSeja um bom marujo e leve esta receita para o Dr. Quiqueres para trazer um novo para mim._where_",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "O que é isso?\aPuxa, eu adoraria poder trabalhar nesta receita, mas os cogs têm furtado meus suprimentos.\aSe você pegasse a armação dos óculos de um Puxa-saco eu provavelmente poderia ajudá-lo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sinto muito. Sem armações de Puxa-saco, não tem monóculo!",
             },
    2206: { QUEST : "Excelente!\aSó um segundo...\aSua receita está pronta. Leve este monóculo diretamente ao Capitão Carlão._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "Alto!\aVocê vai ganhar sua condecoração, afinal de contas.\aAqui está.",
            },
    2207 : { QUEST : "Há um Cog na loja da Craca Bárbara!\aÉ melhor você ir para lá imediatamente._where_" },
    2208 : { QUEST : "Droga! Você se desencontrou dele, gracinha.\aHavia um Golpe Sujo aqui. Ele levou a minha grande peruca branca.\aEle disse que era para o chefe dele e mencionou algo como \"precedente legal\".\aSe você puder pegá-la de volta, ficarei eternamente grata.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "Ainda não o encontrou?\aEle é alto e tem uma cabeça pontuda.",
             COMPLETE : "Você a encontrou!?!?\aVocê é uma gracinha!\aSua recompensa é mais do que merecida...",
             },
    2209 : { QUEST : "Moby está se preparando para uma viagem importante.\aVisite-o e veja o que pode fazer para ajudá-lo._where_"},
    2210 : { QUEST : "Sua ajuda será bem-vinda.\aO Quartel dos Toons me pediu para fazer uma viagem e ver se consigo descobrir de onde os cogs estão vindo.\aPrecisarei de algumas coisas para o meu navio, mas não tenho muitas balinhas.\aPasse pela loja da Alice e pegue um pouco de cascalho para mim. Você terá que fazer um favor para ela para poder pegar o cascalho._where_",
             GREETING : "E aí, _avName_",
             LEAVING : "",
             },
    2211 : { QUEST : "Então, o Moby quer cascalho, né?\aEle ainda está me devendo por aquele último alqueire.\aEu lhe darei se você conseguir eliminar cinco Microempresários na minha rua.",
             INCOMPLETE_PROGRESS : "Não, seu bobinho! Eu disse CINCO microempresários...",
             GREETING : "O que posso fazer por você?",
             LEAVING : "",
             },
    2212 : { QUEST : "Trato é trato.\aAqui está o cascalho para aquele fominha do Moby._where_",
             GREETING : "Ora, ora, o que temos aqui...",
             LEAVING : "",
             },
    2213 : { QUEST : "Excelente trabalho. Eu sabia que ela encontraria uma saída.\aAgora, eu preciso pegar uma carta de navegação com o Mário.\aAcho que meu crédito lá também não é tão bom, portanto, você vai ter que negociar com ele._where_",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Sim, eu tenho a carta de navegação que o Moby quer.\aE se você estiver disposto a trabalhar para consegui-la, eu a darei para você.\aEstou tentando construir um astrolábio para navegar pelas estrelas.\aPreciso de três engrenagens de Cog para construí-la.\aVolte aqui quando encontrá-las.",
             INCOMPLETE_PROGRESS: "Como está indo com aquelas engrenagens de Cog?",
             GREETING : "Bem-vindo!",
             LEAVING : "Boa sorte!",
             },
    2215 : { QUEST : "Oh! Essas engrenagens vão ser úteis mesmo.\aAqui está a carta. Leve para o Moby, com meus cumprimentos._where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "Bem, agora sim. Estou pronto para zarpar!\aEu o levaria comigo se você não fosse novato. Leve isto, então.",
             },
    901 : { QUEST : "Se estiver disposto, o Salgado está precisando de ajuda na loja dele..._where_",
            },
    2902 : { QUEST : "Você é o novo recruta?\aBom, bom. Talvez você possa me ajudar.\aEstou construindo um caranguejo pré-fabricado gigante para confundir os cogs.\aEu vou precisar de uma braçadeira. Visite o Mário e me traga uma._where_",
             },
    2903 : { QUEST : "Olá!\aSim, eu ouvi falar no caranguejo gigante que Salgado está construindo.\aA melhor braçadeira que tenho está meio suja.\aSeja gentil e passe pela lavanderia antes de levá-la para ele._where_",
             LEAVING : "Valeu!"
             },
    2904 : { QUEST : "Você deve ser o amigo do Mário.\aAcho que posso limpar isso rapidinho.\aSó um minuto...\aAqui está. Nova em folha!\aDiga olá ao Salgado por mim._where_",
             },
    2905 : { QUEST : "Ah, era exatamente o que eu queria.\aJá que você está aqui, eu também vou precisar de uma mola de relógio de corda bem grande.\aVá até a loja do Gancho e veja se ele tem uma._where_",
             },
    2906 : { QUEST : "Uma mola bem grande?\aSinto muito, mas a maior que tenho ainda é pequena.\aTalvez eu consiga montar uma com as molas do gatilho de revólver de água.\aTraga-me três dessas piadas e eu vou ver o que posso fazer.",
             },
    2907 : { QUEST : "Vamos dar uma olhada...\aArrasou. Simplesmente arrasou.\aAlgumas vezes eu surpreendo até a mim mesmo.\aAqui está: uma mola grande para o Salgado!_where_",
             LEAVING : "Bon Voyage!",
             },
     2911 : { QUEST : "Ficaria feliz em ajudar nisso, _avName_.\aMas temo que as ruas não estejam mais tão seguras.\aPor que você não vai derrotar alguns Robôs Mercenários? Depois a gente conversa.",
             INCOMPLETE_PROGRESS : "Eu ainda acho que você precisa fazer que as ruas fiquem mais seguras.",
             },
    2916 : { QUEST : "Sim, eu tenho um peso para o Salgado.\aNo entanto, acho que seria mais seguro se você derrotasse alguns Robôs Vendedores primeiro.",
             INCOMPLETE_PROGRESS : "Ainda não. Derrote mais alguns Robôs Vendedores.",
             },
    2921 : { QUEST : "Humm, acho que poderia ceder um peso.\aMas eu me sentiria melhor se não houvesse tantos Robôs-chefe por aí.\aDerrote seis deles e volte aqui.",
             INCOMPLETE_PROGRESS : "Acho que ainda não está seguro...",
             },
    2925 : { QUEST : "Tudo pronto?\aBem, acho que agora está suficientemente seguro.\aAqui está o contrapeso para o Salgado._where_"
             },
    2926 : {QUEST : "Bem, isso é tudo.\aDeixe-me ver se funciona.\aHumm, um pequeno problema.\aNão estou conseguindo obter energia, pois aquele edifício Cog está bloqueando meu painel solar.\aVocê poderia dominá-lo para mim?",
            INCOMPLETE_PROGRESS : "Ainda sem energia. E aquele edifício?",
            COMPLETE : "Súper! Você é um destruidor de cogs e tanto! Tome isto aqui como recompensa...",
            },
    3200 : { QUEST : "Acabo de receber uma ligação do _toNpcName_.\aEle está tendo um dia difícil. Talvez você possa ajudá-lo!\aPasse por lá e veja do que ele precisa._where_" },
    3201 : { QUEST : "Puxa, obrigado por vir!\aPreciso de alguém para levar esta nova gravata de seda para _toNpcName_.\aVocê poderia fazer isso para mim?_where_" },
    3203 : { QUEST : "Ah, esta deve ser a gravata que eu pedi! Obrigado!\aEla combina com o terno listrado que acabei de terminar, logo ali.\aEi, o que aconteceu com o terno?\aOh, não! Os Cogs devem ter roubado meu terno novo!\aDerrote Cogs até encontrar meu terno e traga-o de volta para mim.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você já encontrou meu terno? Tenho certeza de que os Cogs o pegaram!",
             COMPLETE : "Legal! Você encontrou meu terno novo!\aViu, eu disse que os Cogs estavam com ele! Aqui está a sua recompensa...",
             },

    3204 : { QUEST : "_toNpcName_ acabou de ligar para informar um roubo.\aPor que você não passa por lá e vê se consegue resolver as coisas?_where_" },
    3205 : { QUEST : "Olá, _avName_! Você veio me ajudar?\aAcabei de expulsar um Sanguessuga de minha loja. Puxa! Foi horrível.\aMas agora não encontro minha tesoura em lugar nenhum! Tenho certeza de que o Sanguessuga a levou.\aEncontre-o e recupere minha tesoura.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você ainda está procurando minha tesoura?",
             COMPLETE : "Minha tesoura! Valeu mesmo, viu? Aqui está a sua recompensa...",
             },

    3206 : { QUEST : "Parece que _toNpcName_ está tendo problemas com alguns Cogs.\aVá ver se você pode ajudá-lo._where_" },
    3207 : { QUEST : "Oi, _avName_! Obrigado por vir!\aUm monte de Duplos Sentidos invadiu minha loja e roubou uma pilha de cartões-postais de meu balcão.\aVá e derrote todos os Duplos Sentidos e recupere meus cartões-postais!",
             INCOMPLETE_PROGRESS : "Não há cartões-postais suficientes! Continue procurando!",
             COMPLETE : "Ah, valeu! Agora eu posso entregar a correspondência na hora certa! Aqui está a sua recompensa...",
             },

    3208 : { QUEST : "Ultimamente temos recebido reclamações dos moradores sobre os Reis da Incerta.\aVeja se consegue derrotar 10 Reis da Incerta para ajudar nossos colegas Toons nos Jardins da Margarida." },
    3209 : { QUEST : "Valeu mesmo por derrotar os Reis da Incerta!\aMas agora os Operadores de Telemarketing ficaram fora de controle.\aDerrote 10 Operadores de Telemarketing nos Jardins da Margarida e volte aqui para pegar sua recompensa." },

    3247 : { QUEST : "Ultimamente, temos recebido reclamações dos moradores sobre os Sanguessugas.\aVeja se consegue derrotar 20 Sanguessugas para ajudar nossos colegas Toons nos Jardins da Margarida." },


    3210 : { QUEST : "Oh, não, a Seivas Florais da Rua das Amendoeiras está sem flores!\aPara ajudar, leve dez de suas flores com esguicho.\aMas veja primeiramente se tem realmente 10 flores com esguicho em seu estoque.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "Preciso ter 10 flores com esguicho. Você não tem o suficiente!" },
    3211 : { QUEST : "Puxa, valeu mesmo, viu? Estas flores com esguicho vão salvar a pátria.\aMas estou com medo daqueles Cogs lá fora.\aVocê pode me ajudar e derrotar alguns desses Cogs?\aVolte aqui depois de derrotar 20 Cogs nesta rua.",
             INCOMPLETE_PROGRESS : "Ainda há Cogs lá fora para serem derrotados! Continue trabalhando!",
             COMPLETE : "Ah, valeu! Isso ajudou muito. Sua recompensa é...",
             },

    3212 : { QUEST : "_toNpcName_ precisa de ajuda para procurar por algo que ela perdeu.\aVá visitá-la e veja o que pode fazer._where_" },
    3213 : { QUEST : "Oi, _avName_. Você pode me ajudar?\aNão sei onde coloquei minha caneta. Acho que alguns Cogs pegaram-na.\aDerrote Cogs para encontrar minha caneta roubada.",
             INCOMPLETE_PROGRESS : "Você já encontrou minha caneta?" },
    3214 : { QUEST : "Sim, é a minha caneta! Valeu!\aMas, enquanto você estava fora, eu percebi que meu tinteiro também desapareceu.\aDerrote Cogs para encontrar meu tinteiro.",
             INCOMPLETE_PROGRESS : "Ainda estou procurando meu tinteiro!" },
    3215 : { QUEST : "Demais! Agora tenho minha caneta e meu tinteiro de volta!\aMas você nem vai acreditar!\aMeu bloco de notas sumiu! Eles devem tê-lo roubado também!\aDerrote Cogs para encontrar meu bloco de notas roubado e, então, traga-o de volta para ter sua recompensa.",
             INCOMPLETE_PROGRESS : "E meu bloco de notas?" },
    3216 : { QUEST : "É o meu bloco de notas! Maneiro! Sua recompensa é...\aEi! Onde ela está?\aSua recompensa estava bem aqui no cofre de meu escritório. Mas o cofre inteiro sumiu!\aDá para acreditar? Aqueles cogs roubaram sua recompensa!\aDerrote Cogs para recuperar meu cofre.\aQuando você o trouxer de volta, eu lhe darei sua recompensa.",
             INCOMPLETE_PROGRESS : "Continue procurando o cofre! Sua recompensa está lá dentro!",
             COMPLETE : "Finalmente! Seu novo saco de piadas está dentro daquele cofre. Aqui está...",
             },

    3217 : { QUEST : "Temos feito alguns estudos sobre a mecânica dos Robôs Vendedores.\aNós ainda precisamos estudar algumas peças de forma mais detalhada.\aTraga-nos uma roda dentada de algum Dr. Sabe-com-quem-está-falando.\aVocê poderá conseguir uma quando o Cog estiver explodindo." },
    3218 : { QUEST : "Muito bom! Agora precisamos de uma roda dentada de um Amigo da Onça.\aEstas são mais difíceis de conseguir, portanto, continue tentando." },
    3219 : { QUEST : "Demais! Agora precisamos de apenas mais uma roda dentada.\aDesta vez, precisamos de uma de um Agitador.\aTalvez você precise procurar esses Cogs nos edifícios dos Robôs Vendedores.\aQuando achar a roda, traga-a aqui para receber sua recompensa." },

    3244 : { QUEST : "Temos feito alguns estudos sobre a mecânica dos Robôs da Lei.\aNós ainda precisamos estudar algumas peças de forma mais detalhada.\aTraga-nos uma roda dentada de algum Perseguidor de Ambulâncias.\aVocê poderá conseguir uma quando o Cog estiver explodindo." },
    3245 : { QUEST : "Muito bom! Agora precisamos de uma roda dentada de um Golpe Sujo.\aEstas são mais difíceis de conseguir, portanto, continue tentando." },
    3246 : { QUEST : "Demais! Agora precisamos de apenas mais uma roda dentada.\aDesta vez, de um Relações Públicas.\aQuando pegá-la, traga-a aqui para conseguir sua recompensa." },

    3220 : { QUEST : "Acabei de saber que _toNpcName_ estava perguntando por você.\aPor que você não passa por lá e vê o que ela quer?_where_" },
    3221 : { QUEST : "Oi, _avName_! Aí está você!\aOuvi dizer que você é especialista em ataques com esguicho.\aPreciso de alguém para dar um bom exemplo a todos os Toons nos Jardins da Margarida.\aUse seus ataques com esguicho para derrotar vários Cogs.\aIncentive seus amigos a usarem o esguicho também.\aQuando tiver derrotado 20 Cogs, volte aqui para pegar sua recompensa!" },

    3222 : { QUEST : "É hora de demonstrar sua Toonmizade.\aSe você recuperar, com sucesso, um número de edifícios de Cogs, ganhará o direito de fazer três buscas.\aPrimeiramente, derrote dois edifícios de Cogs.\aSinta-se à vontade para chamar seus amigos para ajudá-lo."},
    3223 : { QUEST : "Bom trabalho naqueles edifícios!\aAgora, derrote mais dois.\aOs edifícios devem ter, pelo menos, dois andares." },
    3224 : { QUEST : "Fantástico!\aAgora é só derrotar mais dois edifícios.\aEles devem ter, pelo menos, três andares.\aQuando terminar, volte para pegar sua recompensa!",
             COMPLETE : "Você conseguiu, _avName_!\aVocê demonstrou uma elevada Toonmizade.",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ diz que precisa de ajuda.\aPor que você não vai até lá e vê o que pode fazer para ajudá-la?_where_" },
    3235 : { QUEST : "Ah, esta é a salada que pedi!\aObrigada por trazê-la para mim.\aTodos esses Cogs devem ter amedrontado novamente o entregador de _toNpcName_ .\aPor que você não nos faz um favor e derrota alguns desses Cogs lá fora?\aDerrote 10 Cogs nos Jardins da Margarida e, então, vá até _toNpcName_.",
             INCOMPLETE_PROGRESS : "Você está trabalhando na eliminação de Cogs para mim?\aIsto é maravilhoso! Continue com o bom trabalho!",
             COMPLETE : "Oh, muito obrigada por derrotar aqueles Cogs!\aAgora, acho que poderei manter minha escala normal de entregas.\aSua recompensa é...",
             INCOMPLETE_WRONG_NPC : "Vá contar a _toNpcName_ sobre os Cogs que você derrotou._where_" },

    3236 : { QUEST : "Há muitos Robôs da Lei por aí.\aVocê pode fazer sua parte para ajudar!\aDerrote 3 edifícios de Robôs da Lei." },
    3237 : { QUEST : "Bom trabalho naqueles edifícios de Robôs da Lei!\aMas agora há muitos Robôs Vendedores!\aDerrote 3 edifícios de Robôs Vendedores e volte para buscar sua recompensa." },

    3238 : { QUEST : "Ah não! Um Cog \"Amizade Fácil\" roubou a Chave para os Jardins da Margarida!\aVeja se você consegue recuperá-la.\aLembre-se, o Amizade Fácil só pode ser encontrado dentro dos edifícios de Robôs Vendedores." },
    3239 : { QUEST : "Você achou uma chave, tudo bem, mas esta não é a correta!\aPrecisamos da chave dos Jardins da Margarida.\aContinue de olho! Ela ainda está com algum Cog \"Amizade Fácil\"!" },

    3242 : { QUEST : "Ah não! Um Cog Macaco velho roubou a Chave para os Jardins da Margarida!\aVeja se você consegue recuperá-la.\aLembre-se, os Macacos-velhos só podem ser encontrados dentro dos edifícios de Robôs da Lei." },
    3243 : { QUEST : "Você achou uma chave, tudo bem, mas esta não é a correta!\aPrecisamos da chave dos Jardins da Margarida.\aContinue de olho! Ela ainda está com algum Cog Macaco velho!" },

    3240 : { QUEST : "Acabei de saber que um Macaco velho roubou um saco de ração para pássaros de _toNpcName_ .\aDerrote Macacos velhos até recuperar a ração para pássaros do Florêncio e levá-la de volta para ele.\aOs Macacos velhos só são encontrados dentro de edifícios de Robôs da Lei._where_",
             COMPLETE : "Ah, muito obrigado por encontrar minha ração para pássaros!\aSua recompensa é...",
             INCOMPLETE_WRONG_NPC : "Bom trabalho na recuperação da ração para pássaros!\aAgora, leve-a para _toNpcName_._where_",
             },

    3241 : { QUEST : "Alguns dos edifícios de Cogs estão ficando altos demais e isso já está incomodando.\aVeja se você consegue derrubar alguns dos edifícios mais altos.\aRecupere 5 edifícios de 3 andares, ou mais altos, e volte para pegar sua recompensa.",
             },

    3250 : { QUEST : "A Detetive Linda da Rua dos Carvalhos recebeu informações sobre um Quartel de Robôs Vendedores.\aVá até lá e ajude-a a investigar.",
             },
    3251 : { QUEST : "Há algo estranho acontecendo por aqui.\aHá tantos Robôs Vendedores!\aOuvi dizer que eles organizaram seu próprio quartel no final desta rua.\aVá até lá e veja o que consegue descobrir.\aEncontre Cogs Robôs Vendedores em seu quartel, derrote 5 deles e volte aqui.",
             },
    3252 : { QUEST : "Ok, desembucha.\aO que você disse?\aQuartel de Robôs Vendedores?? Ah não!!! Algo tem que ser feito.\aDevemos avisar a Juíza Gala. Ela saberá o que fazer.\aVá até lá e conte a ela o que descobrimos. É só descer a rua.",
            },
    3253 : { QUEST : "Sim, posso ajudá-lo? Estou muito ocupada.\aHã? Quartel de Cogs?\aHã? Besteira. Isto nunca poderia acontecer.\aVocê deve estar enganado. Absurdo.\aHã? Não discuta comigo.\aOk, então, traga alguma prova.\aSe os Robôs Vendedores realmente estão construindo este Quartel de Cogs, qualquer Cog de lá estará carregando mapas.\aCogs amam trabalhar com papelada, sabe?\aDerrote Robôs Vendedores até encontrar os mapas.\aTraga-os aqui, e eu talvez acredite em você.",
            },
    3254 : { QUEST : "Você de novo, hã? Mapas? Você está com eles?\aDeixe-me vê-los! Humm... Uma fábrica?\aDeve ser lá que eles estão construindo os Robôs Vendedores... E o que é isso?\aSim, exatamente como eu suspeitava. Eu sabia o tempo todo.\aEles estão construindo um Quartel de Robôs Vendedores.\aIsso não é bom. Preciso fazer algumas ligações. Estou muito ocupada. Adeus!\aHã? Ah sim, leve estes mapas de volta para a Detetive Linda.\aEla poderá decifrá-los melhor.",
             COMPLETE : "O que a Juíza Gala disse?\aNós tínhamos razão? Ah, não. Vamos ver estes mapas.\aHumm... Parece que os Robôs Vendedores construíram uma fábrica com maquinário para fazer Cogs.\aParece muito perigoso. Fique de fora até que você tenha mais Pontos de risadas.\aQuando você tiver mais Pontos de risadas, teremos muito mais a aprender sobre o Quartel dos Robôs Vendedores.\aAqui está sua recompensa. Bom trabalho!",
            },


    3255 : { QUEST : "_toNpcName_ está investigando o "+lSellbotHQ+".\aVeja se você consegue ajudar._where_" },
    3256 : { QUEST : "_toNpcName_ está investigando o "+lSellbotHQ+".\aVeja se você consegue ajudar._where_" },
    3257 : { QUEST : "_toNpcName_ está investigando o "+lSellbotHQ+".\aVeja se você consegue ajudar._where_" },
    3258 : { QUEST : "Há muita confusão sobre o que os Cogs pretendem com seu novo Quartel.\aPreciso que você traga algumas informações diretamente deles.\aSe nós conseguirmos quatro memorandos internos de Robôs Vendedores dentro de seu Quartel, isso ajudará a esclarecer as coisas.\aTraga o primeiro memorando para mim para que possamos nos informar melhor.",
             },
    3259 : { QUEST : "Demais! Vamos ver o que diz o memorando...\a\"A/C Robôs Vendedores:\"\a\"Estarei em meu escritório no topo das Torres Robôs Vendedores promovendo Cogs a níveis mais altos.\"\a\"Quando você tiver méritos suficientes, entre no elevador do saguão para falar comigo\".\a\"O intervalo chegou ao fim. De volta ao trabalho!\"\a\"Assinado, Robô Vendedor VP\"\aAhá.... Flippy vai querer ver isto. Enviarei a ele imediatamente.\aVá buscar o segundo memorando e traga aqui.",
             },
    3260 : { QUEST : "Que bom, você está de volta. Deixe-me ver o que você encontrou....\a\"A/C Robôs Vendedores:\"\a\"As Torres Robôs Vendedores instalaram um novo sistema de segurança para afastar todos os Toons.\"\a\"Os Toons que forem encontrados nas Torres Robôs Vendedores serão detidos para interrogatório\".\a\"Encontrem-se no saguão para um coquetel, no qual discutiremos o assunto.\"\a\"Assinado, Amizade Fácil\"\aMuito interessante... Passarei imediatamente esta informação adiante.\aTraga o terceiro memorando.",
             },
    3261 : { QUEST : "Excelente trabalho _avName_! O que diz o memorando?\a\"A/C Robôs Vendedores:\"\a\"De algum modo, os Toons encontraram um jeito de se infiltrarem nas Torres Robôs Vendedores.\"\a\"Ligarei para vocês esta noite na hora do jantar para fornecer os detalhes.\"\a\"Assinado, Operador de Telemarketing\"\aHumm... Queria saber como os Toons estão conseguindo se infiltrar....\aTraga mais um memorando e acho que assim teremos informações suficientes.",
             COMPLETE : "Eu sabia que você conseguiria! Ok, o memorando diz...\a\"A/C Robôs Vendedores:\"\a\"Ontem, estava almoçando com Dr. Celebridade.\"\a\"Ele disse que o VP tem estado bastante ocupado nestes dias.\"\a\"Ele só receberá os Cogs que merecem promoção.\"\a\"Esqueci de dizer, o Amigo da Onça jogará golfe comigo no domingo.\"\a\"Assinado, Dr. Sabe-com-quem-está-falando\"\aBem... _avName_, isto foi muito útil.\aAqui está sua recompensa.",
             },

    3262 : { QUEST : "_toNpcName_ tem novas informações sobre a Fábrica do "+lSellbotHQ+".\aVá ver o que ele tem a dizer._where_" },
    3263 : { GREETING : "Olá, parceiro!",
             QUEST : "Eu sou o Treinador Abobrinha, mas você pode me chamar de Treinador A.\aEu sou a favor de treinos com a raquete e alongamento, se é que você me entende.\aOuça, os Robôs Vendedores terminaram uma enorme fábrica para produzir Robôs Vendedores 24 horas por dia.\aReúna um grupo de parceiros Toon e raquetada na fábrica!\aDentro do Quartel do Robô Vendedor, procure pelo túnel que leva até a fábrica e, então, entre no elevador.\aVocê já tem que estar com as piadas e os pontos de risadas completos e ter Toons fortes como guias.\aPara retardar o progresso dos Robôs Vendedores, derrote o Supervisor dentro da fábrica.\aParece um grande exercício, se é que fui bem claro.",
             LEAVING : "Te vejo por aí, parceiro!",
             COMPLETE : "Ei, parceiro, bom trabalho naquela Fábrica!\aParece que você encontrou parte de um terno de Cog.\aDeve ser uma sobra do processo de fabricação de Cogs.\aIsto pode vir a calhar. Continue coletando estas partes quando tiver um tempo livre.\aQuem sabe, quando você coletar um terno de Cog completo, poderá vir a ser útil para alguma coisa....",
             },

    4001 : {GREETING : "",
            QUEST : "Agora, você tem que escolher o próximo tipo de piada que deseja aprender.\aDecida e depois volte aqui quando estiver pronto para escolher.",
            INCOMPLETE_PROGRESS : "Pense bem sobre sua decisão antes de escolher.",
            INCOMPLETE_WRONG_NPC : "Pense bem sobre sua decisão antes de escolher.",
            COMPLETE : "Uma boa decisão...",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "Agora você tem que escolher o próximo tipo de piada que deseja aprender.\aDecida e depois volte aqui quando estiver pronto para escolher.",
            INCOMPLETE_PROGRESS : "Pense bem sobre sua decisão antes de escolher.",
            INCOMPLETE_WRONG_NPC : "Pense bem sobre sua decisão antes de escolher.",
            COMPLETE : "Uma boa decisão...",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "Aposto que o Tom iria gostar de ter alguma ajuda na pesquisa que ele está fazendo._where_",
             },
    4201 : { GREETING: "Tudo certo?",
             QUEST : "Estou bastante preocupado com a onda de roubos de instrumentos musicais.\aEstou conduzindo uma pesquisa com meus amigos comerciantes.\aTalvez seja possível encontrar um padrão para me ajudar a resolver este caso.\aPeça a Tina o controle de estoque de concertina._where_",
             },
    4202 : { QUEST : "Sim, eu falei com Tom nesta manhã.\aO estoque está bem aqui.\aLeve para ele imediatamente, ok?_where_"
             },
    4203 : { QUEST : "Demais! Um a menos...\aAgora peça o da Cavaca._where_",
             },
    4204 : { QUEST : "Ah! O estoque!\aEsqueci completamente.\aAposto que consigo fazer enquanto você derrota 10 cogs.\aPasse por aqui depois, e eu prometo que estará pronto.",
             INCOMPLETE_PROGRESS : "31, 32... DROGA!\aVocê me fez perder a conta!",
             GREETING : "",
             },
    4205 : { QUEST : "Ah, aí está você.\aObrigada por me dar algum tempo.\aLeve isto para o Tom e diga olá por mim._where_",
             },
    4206 : { QUEST : "Humm, muito interessante.\aAgora estamos chegando a algum lugar.\aOk, o último estoque é o da Fifi._where_",
             },
    4207 : { QUEST : "Estoque?\aComo posso fazer o estoque se não tenho o formulário?\aVá até o Clave e veja se ele tem um para mim._where_",
             INCOMPLETE_PROGRESS : "Algum sinal daquele formulário?",
             },
    4208 : { QUEST : "Claro que eu tenho um formulário de estoque, monsenhor!\aMas eles não são de graça, sabe?.\aFaçamos o seguinte. Eu troco por uma torta de creme inteira.",
             GREETING : "Ei, monsenhor!",
             LEAVING : "Boa sorte...",
             INCOMPLETE_PROGRESS : "Um pedaço não adianta.\aEstou com fome, monsenhor. Eu preciso da torta INTEIRA.",
             },
    4209 : { GREETING : "",
             QUEST : "Humm...\aMuito gostoso!\aAqui está o formulário para Fifi._where_",
             },
    4210 : { GREETING : "",
             QUEST : "Valeu, foi uma grande ajuda.\aVamos ver...Violinos: 2\aTudo pronto! Aqui está!",
             COMPLETE : "Bom trabalho, _avName_.\aTenho certeza de que solucionarei este caso agora.\aPor que você não o soluciona?",
             },

    4211 : { QUEST : "Veja, o Dr. Triturador está ligando de cinco em cinco minutos. Você pode conversar com ele e ver qual o problema?_where_",
             },
    4212 : { QUEST : "Puxa! Estou feliz de ver que o Quartel dos Toons finalmente mandou alguém.\aNão tenho um cliente há dias.\aSão estes malditos Destruidores de Números que estão em todo lugar.\aAcho que eles estão ensinando maus hábitos de higiene oral a nossos moradores.\aDerrote dez deles e vamos ver se o negócio anda.",
             INCOMPLETE_PROGRESS : "Ainda sem clientes. Mas continue assim!",
             },
    4213 : { QUEST : "Sabe, talvez não sejam os Destruidores de Números, no final das contas.\aTalvez sejam apenas os Robôs Mercenários em geral.\aDerrote vinte deles e, com alguma sorte, alguém virá, pelo menos, para um check-up.",
             INCOMPLETE_PROGRESS : "Eu sei que vinte é muito. Mas tenho certeza de que vai valer a pena.",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Eu não consigo entender!\aAinda não há UM BENDITO freguês.\aTalvez precisemos ir até a fonte.\aTente recuperar um edifício Cog de Robôs Mercenários.\aIsso deve funcionar...",
             INCOMPLETE_PROGRESS : "Oh, por favor! Apenas um mísero prediozinho...",
             COMPLETE : "Ainda não há uma alma sequer aqui.\aMas, pense bem.\aEu não tinha mesmo clientes antes da invasão dos cogs!\aRealmente agradeço toda a sua ajuda.\aIsto deve ajudar você a prosseguir."
             },

    4215 : { QUEST : "A Ana precisa desesperadamente da ajuda de alguém.\aPor que você não passa lá e vê o que pode fazer?_where_",
             },
    4216 : { QUEST : "Obrigada por chegar tão rápido!\aParece que os cogs sumiram com várias passagens dos meus clientes.\aA Cavaca disse que viu um Amigo da Onça saindo daqui com as garras cheias de passagens.\aVeja se você consegue recuperar a passagem do Alê Nhador para o Alasca.",
             INCOMPLETE_PROGRESS : "Aqueles Amigos da Onça podem estar em qualquer lugar agora...",
             },
    4217 : { QUEST : "Legal! Você encontrou!\aAgora seja um cavalheiro e entregue ao Alê Nhador para mim, está bem?_where_",
             },
    4218 : { QUEST : "Genial, estupendo, fabuloso!\aAlasca, aqui vou eu!\aNão aguento mais esses cogs infernais.\aOlha, acho que a Ana precisa de você de novo._where_",
             },
    4219 : { QUEST : "Exatamente, você adivinhou!\aPreciso de você para derrotar aquelas pestes dos Amigos da Onça para recuperar a passagem da Tábata para o Festival de Jazz.\aVocê sabe como fazer...",
               INCOMPLETE_PROGRESS : "Há mais lá fora, em algum lugar...",
             },
    4220 : { QUEST : "Gracinha!\aVocê poderia entregar este também?_where_",
             },
    4221 : { GREETING : "",
             LEAVING : "Fica frio...",
             QUEST : "Legal, cara!\aAgora estou na cidade dos gordinhos, _avName_.\aAntes de sair fora, é melhor falar com a Ana Banana de novo..._where_",
             },
    4222 : { QUEST : "Este é o último, prometo!\aAgora procure pela passagem do Barry para o grande concurso de cantores.",
             INCOMPLETE_PROGRESS : "Vamos lá, _avName_.\aO Barry está contando com você.",
             },
    4223 : { QUEST : "Isto deve alegrar o Barry._where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "Olá, Olá, OLÁ!\aMagnífico!\aSó conheço eu mesmo e os caras que vão fazer a faxina. \aA Ana disse para você passar lá e pegar a sua recompensa._where_\aTchau, Tchau, TCHAU!",
             COMPLETE : "Obrigado por toda a sua ajuda, _avName_.\aVocê é realmente um tesouro aqui de Toontown.\aFalando em tesouros...",
             },

    902 : { QUEST : "Vá ver o Léo.\aEle precisa de alguém para entregar uma mensagem para ele._where_",
            },
    4903 : { QUEST : "Cara!\aMinhas castanholas estão foscas e tenho um grande show hoje à noite.\aLeve-as para o Carlos e veja se ele pode dar um polimento nelas._where_",
            },
    4904 : { QUEST : "Sim, acho que posso polir esta peça. Mas preciso de alguma tinta azul de lula",
             GREETING : "Olá!",
             LEAVING : "Tchau!",
             INCOMPLETE_PROGRESS : "Você pode achar uma lula perto de algum píer de pesca.",
             },
    4905 : { QUEST : "Claro! Isso mesmo!\aAgora, preciso de um minuto para polir isto. Por que você não trabalha na recuperação de um prédio de um andar enquanto trabalho por aqui?",
             GREETING : "Ola!",
             LEAVING : "Tchau!",
             INCOMPLETE_PROGRESS : "Só mais um minutinho...",
             },
    4906 : { QUEST : "Muito bom!\aAqui estão as castanholas do Léo._onde_",
             },
    4907 : { GREETING : "",
             QUEST : "Maneiro, cara!\aElas estão incríveis!\aAgora preciso que você consiga uma cópia da letra da “Música de Natal” da Heidi._where_",
             },
    4908 : { QUEST: "E aí pessoal!\aHumm, Eu não tenho uma cópia dessa música à mão.\aSe você me der um tempinho, eu posso transcrever de cabeça.\aPor que você não dá uma voltinha e aproveita para recuperar um edifício de dois andares enquanto escrevo?",
             },
    4909 : { QUEST : "Desculpe.\aMinha memória está ficando meio confusa.\aSe você recuperar um edifício de três andares, tenho certeza de que estarei pronta quando voltar...",
             },
    4910 : { QUEST : "Tudo pronto!\aDesculpe a demora.\aLeve isto para o Léo._where_",
             GREETING : "",
             COMPLETE : "Caramba, cara!\aMeu show vai detonar!\aFalando em detonar, você pode detonar alguns cogs com isto..."
             },
    5247 : { QUEST : "Este bairro está ficando perigoso...\aVocê deve estar querendo aprender alguns truques novos.\a_toNpcName_ me ensinou tudo que sei, então, talvez ele possa ajudar você também._where_" },
    5248 : { GREETING : "Ah, sim.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você parece estar empenhado na missão.",
             QUEST : "Ah, bem-vindo, novo aprendiz.\aEu sei de tudo que há para saber sobre o jogo de tortas.\aPorém, antes de começarmos o seu treinamento, é necessário uma pequena demonstração.\aSaia e derrote dez dos maiores Cogs." },
    5249 : { GREETING: "Humm.",
             QUEST : "Excelente!\aAgora demonstre sua habilidade como pescador.\aColoquei ontem três dados de pelúcia no lago.\aPesque-os e traga-os para mim.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Parece que você não é tão hábil com a vara e o molinete." },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahá! Estes dados ficarão ótimos pendurados no retrovisor do meu carro de bois!\aAgora, mostre para mim que você sabe distinguir seus inimigos.\aVolte quando tiver recuperado dois dos edifícios mais altos dos Robôs da Lei.",
             INCOMPLETE_PROGRESS : "Os edifícios deram problema para você?", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahá! Estes dados ficarão ótimos pendurados no retrovisor do meu carro de bois!\aAgora, mostre para mim que você sabe distinguir seus inimigos.\aVolte quando tiver recuperado dois dos edifícios mais altos dos Robôs-chefes.",
             INCOMPLETE_PROGRESS : "Os edifícios deram problema para você?", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahá! Estes dados ficarão ótimos pendurados no retrovisor do meu carro de bois!\aAgora, mostre para mim que você sabe distinguir seus inimigos.\aVolte quando tiver recuperado dois dos edifícios mais altos dos Robôs Mercenários.",
             INCOMPLETE_PROGRESS : "Os edifícios deram problema para você?", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahá! Estes dados ficarão ótimos pendurados no retrovisor do meu carro de bois!\aAgora, mostre para mim que você sabe distinguir seus inimigos.\aVolte quando tiver recuperado dois dos edifícios mais altos dos Robôs Vendedores.",
             INCOMPLETE_PROGRESS : "Os edifícios deram problema para você?", },
    5200 : { QUEST : "Aqueles cogs traiçoeiros estão envolvidos nisto novamente.\a_toNpcName_ percebeu que tem outro item ausente. Pare um pouco aqui e veja se consegue acertar isso._where_" },
    5201 : { GREETING: "",
             QUEST : "Oi, _avName_. Acho que eu devo agradecer a você por ter vindo.\aUm grupo desses Caça-talentos chegou e roubou minha bola de futebol.\aO líder disse que eu tinha que fazer alguns cortes e tomou a bola de mim!\aVocê pode trazer de volta a minha bola?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu achar minha bola de futebol?",
             COMPLETE : "Dez! Encontrei! Olha aqui, tome a sua recompensa...",
             },
    5261 : { GREETING: "",
             QUEST : "Oi, _avName_. Acho que eu devo agradecer a você por ter vindo.\aUm grupo desses Duas Caras chegou e roubou minha bola de futebol.\aO líder disse que eu tinha que fazer alguns cortes e tomou a bola de mim!\aVocê pode trazer de volta a minha bola?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu achar minha bola de futebol?",
             COMPLETE : "Dez! Encontrei! Olha aqui, tome a sua recompensa...",
             },
    5262 : { GREETING: "",
             QUEST : "Oi, _avName_. Acho que eu devo agradecer a você por ter vindo.\aUm grupo desses Sacos de Dinheiro chegou e roubou minha bola de futebol.\aO líder disse que eu tinha que fazer alguns cortes e tomou a bola de mim!\aVocê pode trazer de volta a minha bola?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu achar minha bola de futebol?",
             COMPLETE : "Dez! Encontrei! Olha aqui, tome a sua recompensa...",
             },
    5263 : { GREETING: "",
             QUEST : "Oi, _avName_. Acho que eu devo agradecer a você por ter vindo.\aUm grupo desses Relações Públicas chegou e roubou minha bola de futebol.\aO líder disse que eu tinha que fazer alguns cortes e tomou a bola de mim!\aVocê pode trazer de volta a minha bola?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Conseguiu achar minha bola de futebol?",
             COMPLETE : "Dez! Encontrei! Olha aqui, tome a sua recompensa...",
             },
    5202 : { QUEST : "O Brrrgh foi invadido por alguns dos mais temíveis Cogs já vistos.\aVocê provavelmente desejará carregar mais piadas consigo.\aOuvi falar que _toNpcName_ tem uma sacola grande que você pode usar para carregar mais piadas._where_" },
    5203 : { GREETING: "Hã? Você está no meu time de trenó?",
             QUEST : "O que é isto? Você quer uma bolsa?\aEu tinha uma aqui em algum lugar... Acho que está no meu tobogã?\aSó que... Eu não vejo o meu tobogã desde a grande corrida!\aTalvez um destes Cogs o tenha pego.",
             LEAVING : "Você viu meu tobogã?",
             INCOMPLETE_PROGRESS : "Quem é você novamente? Desculpe, estou meio confuso depois da batida." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Este é o meu tobogã? Não vejo nenhuma sacola aqui.\aAcho que o Cabeção Kika estava na equipe... Será que está com ele?_where_" },
    5205 : { GREETING : "Ai, minha cabeça!",
             LEAVING : "",
             QUEST : "Hã? Tobi? Ah, a bolsa?\aBom, acho que ele estava na nossa equipe de tobogã?\aMinha cabeça dói tanto que não consigo pensar direito.\aVocê consegue para mim alguns cubos de gelo no lago congelado para eu pôr na minha cabeça?",
             INCOMPLETE_PROGRESS : "Aaiii, minha cabeça está me matando! Tem gelo aí?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ahhh, agora me sinto bem melhor!\aEntão você está procurando a bolsa do Tobi, né?\aAcho que ela foi parar na cabeça do Álvaro Asno depois da batida._where_" },
    5207 : { GREETING : "Iiiiiiiiiip!",
             LEAVING : "",
             QUEST : "O que é bolsa? Quem é Cabeção?\aTenho medo de edifícios! Você detona edifício, eu dou bolsa!",
             INCOMPLETE_PROGRESS : "Mais edifícios! Ainda com medo!",
             COMPLETE : "Ooooh! Mim gosta você!" },
    5208 : { GREETING : "",
             LEAVING : "Iiiiiiiiiiik!",
             QUEST : "Ooooh! Mim gosta você!\aVai pra Clínica do Esqui. Sacola lá." },
    5209 : { GREETING : "Valeu, garoto!",
             LEAVING : "Até mais!",
             QUEST : "Cara, o Álvaro Asno é doido!\aSe você fosse maluco que nem o Álvaro, eu daria a bolsa para você, cara.\aVai ensacar uns Cogs para poder pegar a sua sacola, cara! Essa agora!",
             INCOMPLETE_PROGRESS : "Tem certeza de que você é radical o bastante para isso? Vai ensacar mais Cogs.",
             COMPLETE : "Caramba, você é irado! Aquilo foi um bando de Cogs que você ensacou!\aToma a sua bolsa!" },

    5210 : { QUEST : "_toNpcName_ está gamada em alguém do bairro, mas é segredo.\aSe você ajudá-la, ela pode lhe dar uma boa recompensa._where_" },
    5211 : { GREETING: "Buá!",
             QUEST : "Passei a noite passada inteira escrevendo uma carta para o cachorro que eu amo.\aMas, antes mesmo que eu pudesse entregar a ele, um daqueles Cogs asquerosos com bico veio e a tomou de mim.\aVocê consegue pegá-la de volta para mim?",
             LEAVING : "Buá!",
             INCOMPLETE_PROGRESS : "Por favor, encontre minha carta." },
    5264 : { GREETING: "Buá!",
             QUEST : "Passei a noite passada inteira escrevendo uma carta para o cachorro que eu amo.\aMas, antes mesmo que eu pudesse entregar a ele, um daqueles Cogs asquerosos de barbatana veio e a tomou de mim.\aVocê consegue pegá-la de volta para mim?",
             LEAVING : "Buá!",
             INCOMPLETE_PROGRESS : "Por favor, encontre minha carta." },
    5265 : { GREETING: "Buá!",
             QUEST : "Passei a noite passada inteira escrevendo uma carta para o cachorro que eu amo.\aMas, antes mesmo que eu pudesse entregar a ele, um daqueles Cogs asquerosos de Amizade Fácil veio e a tomou de mim.\aVocê consegue pegá-la de volta para mim?",
             LEAVING : "Buá!",
             INCOMPLETE_PROGRESS : "Por favor, encontre minha carta." },
    5266 : { GREETING: "Buá!",
             QUEST : "Passei a noite passada inteira escrevendo uma carta para o cachorro que eu amo.\aMas, antes mesmo que eu pudesse entregar a ele, um daqueles Cogs Aventureiros Corporativos asquerosos veio e a tomou de mim.\aVocê consegue pegá-la de volta para mim?",
             LEAVING : "Buá!",
             INCOMPLETE_PROGRESS : "Por favor, encontre minha carta." },
    5212 : { QUEST : "Oh, obrigada por encontrar a minha carta!\aPor favor, você poderia entregá-la ao cão mais lindo do bairro? Por favor! Por favor!",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você não entregou a minha carta, não é?",
             },
    5213 : { GREETING : "Enfeitiçado, com certeza.",
             QUEST : "Não posso dar atenção à sua carta, sabe.\aTodos os meus cãezinhos foram levados!\aSe você os trouxer de volta, a gente volta a conversar.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tadinhos dos meus cãezinhos!" },
    5214 : { GREETING : "",
             LEAVING : "Tchauzinho!",
             QUEST : "Graças a você minhas belezinhas voltaram.\aVamos ver a carta agora...\nMmmm, parece que tenho outra admiradora secreta.\aIsso exigirá uma visita ao meu querido amigo Carlo.\aAposto como você vai adorá-lo._where_" },
    5215 : { GREETING : "He, he...",
             LEAVING : "Volte aqui, sim, sim.",
             INCOMPLETE_PROGRESS : "Ainda há alguns grandalhões na área. Volte aqui para falar conosco quando eles forem embora.",
             QUEST : "Quem mandou você? Não gostamos muito de Snobs, não...\aMas gostamos menos ainda de Cogs...\aExpulse os grandalhões e ajudaremos vocês, ajudaremos." },
    5216 : { QUEST : "Falamos que ajudaríamos você.\aEntão, pegue este anel e leve à garota.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você ainda está com o anel???",
             COMPLETE : "Oh querrrrido!!! Obrigado!!!\aAh, também tenho algo especial para você.",
             },
    5217 : { QUEST : "Parece que _toNpcName_ pode dar uma ajuda._where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tenho certeza de que há mais Amizades Fáceis por aqui em algum lugar.",
             QUEST : "Socorro!!! Socorro!!! Assim não dá!\aEsses Amizades Fáceis estão me deixando maluco!!!" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não são só estes. Só vi um!!!",
             QUEST : "Ah, obrigado, mas agora são os Aventureiros Corporativos!!!\aVocê tem que me ajudar!!!" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não, não, não, havia um aqui agora mesmo!",
             QUEST : "Agora, eu percebo que são aqueles Agiotas!!!\aPensei que você ia me salvar!!!" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "Sabe de uma coisa, talvez não sejam os Cogs coisa nenhuma!\aVocê pode pedir à Hilária para fazer para mim uma poção calmante? Talvez isto ajude...._where_" },
    5222 : { LEAVING : "",
             QUEST : "Esse Américo é mesmo uma figura!\aVou preparar algo que vai dar jeito nele rapidinho!\aPuxa, parece que estou sem bigodes de sardinha...\aSeja legal comigo e corra lá no lago para pegar alguns para mim.",
             INCOMPLETE_PROGRESS : "Já pegou aqueles bigodes para mim?", },
    5223 : { QUEST : "OK. Obrigada!\aTome, leve agora para o Américo. Isto deve acalmá-lo de uma vez por todas.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vá logo, leve a poção para o Américo.",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vá pegar aqueles Macacos velhos para mim, ok?",
             QUEST : "Puxa vida, graças a Deus você voltou!\aPasse logo para cá esta poção!!!\aGlub, glub, glub...\aQue gosto horrível!\aSabe de uma coisa? Sinto-me bem mais calmo. Agora que eu posso pensar com mais clareza, me toquei que...\aEram os Macacos-velhos que estavam me enlouquecendo todo este tempo!!!",
             COMPLETE : "Nossa! Agora eu posso relaxar!\aTenho certeza de que há alguma coisa aqui que posso dar a você. Aqui, leve isto!" },
    5225 : { QUEST : "Desde o acidente com o pão de nabo, Felipe Nervosinho ficou furioso com _toNpcName_.\aQuem sabe você não consegue ajudar o Pio a acertar os ponteiros entre eles?_where_" },
    5226 : { QUEST : "Isso mesmo, você deve ter ouvido falar que o Felipe Nervosinho está furioso comigo...\aEu estava só tentando ser legal oferecendo o pão de nabo.\aQuem sabe você não consegue alegrá-lo.\aO Felipe detesta aqueles Cogs Robôs Mercenários, principalmente os edifícios deles.\aSe você recuperar alguns edifícios de Robôs Mercenários, talvez ajude.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Quem sabe alguns edifícios a mais?", },
    5227 : { QUEST : "Demais! Vá dizer ao Felipe o que você fez._where_" },
    5228 : { QUEST : "Puxa, ele fez isso mesmo?\aEsse Pio acha que pode se safar fácil, né?\aSó quebrou meu dente, só isso que ele fez, com aquele pão de nabo dele!\aSe você levar o meu dente para o Dr. Ban Guela para mim, quem sabe ele consegue dar jeito.",
             GREETING : "Mmmmrrf.",
             LEAVING : "Resmungo, resmungo.",
             INCOMPLETE_PROGRESS : "Você de novo? Pensei que você estava indo levar meu dente para consertar.",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda estou ajeitando o dente. Vai demorar um pouco.",
             QUEST : "É, este dente parece estar ruim mesmo, mas tudo bem.\aEu acho que posso fazer uma coisa aqui, mas ainda vai demorar um pouco.\aVocê não quer dar cabo de alguns daqueles Cogs Robôs Mercenários das ruas enquanto espera?\aEles estão assustando os meus clientes." },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda estou ajeitando o dente. Vai demorar um pouco.",
             QUEST : "É, este dente parece estar ruim mesmo, mas tudo bem.\aEu acho que posso fazer uma coisa aqui, mas ainda vai demorar um pouco.\aVocê não quer dar cabo de alguns daqueles Cogs Robôs Vendedores das ruas enquanto espera?\aEles estão assustando os meus clientes." },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda estou ajeitando o dente. Vai demorar um pouco.",
             QUEST : "É, este dente parece estar ruim mesmo, mas tudo bem.\aEu acho que posso fazer uma coisa aqui, mas ainda vai demorar um pouco.\aVocê não quer dar cabo de alguns daqueles Cogs Robôs da Lei das ruas enquanto espera?\aEles estão assustando os meus clientes." },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda estou ajeitando o dente. Vai demorar um pouco.",
             QUEST : "É, este dente parece estar ruim mesmo, mas tudo bem.\aEu acho que posso fazer uma coisa aqui, mas ainda vai demorar um pouco.\aVocê não quer dar cabo de alguns daqueles Cogs Robôs-chefe das ruas enquanto espera?\aEles estão assustando os meus clientes." },
    5230 : { GREETING: "",
             QUEST : "Ainda bem que você voltou!\aDesisti de consertar aquele dente velho e, em vez de consertá-lo, fiz um novo dente de ouro para o Felipe.\aSó que um Barão Ladrão entrou aqui e o levou, infelizmente.\aSerá que você não consegue pegá-lo? Vamos, apresse-se!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você já achou aquele dente?" },
    5270 : { GREETING: "",
             QUEST : "Ainda bem que você voltou!\aDesisti de consertar aquele dente velho e, em vez de consertá-lo, fiz um novo dente de ouro para o Felipe.\aSó que um Rei da Cocada Preta entrou aqui e o levou, infelizmente.\aSerá que você não consegue pegá-lo? Vamos, apresse-se!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você já achou aquele dente?" },
    5271 : { GREETING: "",
             QUEST : "Ainda bem que você voltou!\aDesisti de consertar aquele dente velho e, em vez de consertá-lo, fiz um novo dente de ouro para o Felipe.\aSó que o Dr. Celebridade entrou aqui e o levou, infelizmente.\aSerá que você não consegue pegá-lo? Vamos, apresse-se!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você já achou aquele dente?" },
    5272 : { GREETING: "",
             QUEST : "Ainda bem que você voltou!\aDesisti de consertar aquele dente velho e, em vez de consertá-lo, fiz um novo dente de ouro para o Felipe.\aSó que um Figurão entrou aqui e o levou, infelizmente.\aSerá que você não consegue pegá-lo? Vamos, apresse-se!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Você já achou aquele dente?" },
    5231 : { QUEST : "Legal, é este dente mesmo!\aPor que você não corre para levá-lo para o Felipe?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Aposto como o Felipe vai adorar ver o dente novo dele.",
             },
    5232 : { QUEST : "Puxa, obrigado.\aMmmrrrfffffff\aE aí, que tal, hein?\aOk, tudo bem, pode dizer ao Pio que eu o perdôo.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Legal, muito bom saber disso.\aAchei mesmo que meu velho amigo Felipe não podia ficar com raiva de mim.\aPara agradecer e ser gentil, preparei para ele este pão de pinha.\aSerá que você podia correr lá e entregar a ele para mim?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Melhor se apressar. O pão de pinha só é bom quando está quente.",
             COMPLETE : "Puxa, o que é isto? Para mim?\aNham, nham...\aOhhhhhh! Meu dente! Aquele Pio Arrepio!\aTudo bem, não foi sua culpa. Tome aqui, leve isto por todo o trabalho que demos a você.",
             },
    903 : { QUEST : "Você deve se aprontar para ver _toNpcName_, o Mago do Lago Congelado, para o seu teste final._where_", },
    5234 : { GREETING: "",
             QUEST : "Ahá! Você voltou.\aAntes de você começar, precisamos comer.\aTraga para a gente alguns pedaços de coco para o nosso caldo.\aO coco em pedaços só pode ser conseguido nos Cogs Rei da Cocada Preta.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda precisamos de coco em pedaços." },
    5278 : { GREETING: "",
             QUEST : "Ahá! Você voltou.\aAntes de você começar, precisamos comer.\aTraga para a gente caviar para o nosso caldo.\aO caviar só pode ser conseguido nos Cogs Dr. Celebridade.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ainda precisamos de caviar." },
    5235 : { GREETING: "",
             QUEST : "Homens simples comem com colheres simples.\aOs Cogs levaram minha colher simples, por isso, eu simplesmente não posso comer.\aPegue minha colher de volta. Acho que foi um Barão Ladrão.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Eu simplesmente preciso da minha colher." },
    5279 : { GREETING: "",
             QUEST : "Homens simples comem com colheres simples.\aOs Cogs levaram minha colher simples, por isso, eu não posso comer.\aPegue minha colher de volta. Acho que foi um Figurão.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Eu simplesmente preciso da minha colher." },
    5236 : { GREETING: "",
             QUEST : "Muito obrigado.\aSlurp, slurp...\aAhhh, agora, você precisa pegar um sapo falante. Tente pescá-lo no lago.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Cadê o sapo falante?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Você não conseguiu a sobremesa ainda.",
              QUEST : "Ah, isto é, com certeza, um sapo falante. Passe para cá.\aO que você me diz, sapo?\aUh huh.\aUh huh...\aO sapo falou. Precisamos da sobremesa.\aTraga para a gente algumas casquinhas de sorvete da _toNpcName_.\aPor alguma razão, o sapo gosta de sorvete sabor feijão vermelho._where_", },
    5238 : { GREETING: "",
             QUEST : "Então, o mago mandou você aqui. Sinto dizer que acabamos de ficar sem as casquinhas sabor feijão vermelho.\aVocê nem imagina, mas um bando de Cogs entrou aqui e as levou.\aEles disseram que iam levá-las para o Dr. Celebridade, ou alguma baboseira parecida.\aCertamente, apreciaria se você pudesse recuperá-las para mim.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Já achou todas as minhas casquinhas de sorvete?" },
    5280 : { GREETING: "",
             QUEST : "Então, o mago mandou você aqui. Sinto dizer que acabamos de ficar sem as casquinhas sabor feijão vermelho.\aVocê nem imagina, mas um bando de Cogs entrou aqui e as levou.\aEles disseram que iam levá-las para O Rei da Cocada Preta, ou alguma baboseira parecida.\aCertamente, apreciaria se você pudesse recuperá-las para mim.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Já achou todas as minhas casquinhas de sorvete?" },
    5239 : { QUEST : "Obrigado por trazer de volta as minhas casquinhas de sorvete!\aTome uma para o Pequeno Grande Ancião.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "É melhor você levar este sorvete para o Pequeno Grande Ancião antes que ele derreta.", },
    5240 : { GREETING: "",
             QUEST : "Muito bem. Aqui está, sapo...\aSlurp, slurp...\aOk, agora estamos quase prontos.\aSe você pudesse apenas trazer um pozinho para secar as minhas mãos...\aAcho que das perucas daqueles Cogs Figurões às vezes sai pó.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Achou algum pó?" },
    5281 : { GREETING: "",
             QUEST : "Muito bem. Aqui está, sapo...\aSlurp, slurp...\aOk, agora estamos quase prontos.\aSe você pudesse apenas trazer um pozinho para secar as minhas mãos...\aAcho que aqueles Cogs Drs. Celebridades às vezes têm pó para o nariz.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Achou algum pó?" },
    5241 : { QUEST : "Ok.\aComo já disse antes, para lançar uma torta pra valer, não basta jogá-la com a mão...\a...É preciso jogar com a alma.\aNão sei exatamente o que isto significa, portanto, sentarei e contemplarei você em seu trabalho de recuperar edifícios.\aVolte quando tiver concluído a sua tarefa.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sua tarefa ainda não está concluída.", },
    5242 : { GREETING: "",
             QUEST : "Embora eu ainda não saiba sobre o que estou falando, você realmente merece.\aDou a você, então, uma tarefa final...\aO sapo falante precisa de uma namorada.\aAche uma sapa falante. O sapo falou.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Cadê a sapa falante?",
             COMPLETE : "Puxa! Estou cansado com todo esse esforço. Preciso descansar agora.\aAgora, pegue a sua recompensa e saia." },

    5243 : { QUEST : "Soares Suado está começando a feder no início da rua.\aFala com ele para tomar um banho ou algo do gênero?_where_" },
    5244 : { GREETING: "",
             QUEST : "É, acho que suei demais aqui.\aMmmm, se eu pudesse consertar aquele vazamento no encanamento do meu chuveiro...\aAcho que a engrenagem de um daqueles Cogs pequenos bastaria para o conserto.\aVá achar uma engrenagem de um Microempresário para a gente tentar consertar.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Onde está aquela engrenagem que você ia conseguir?" },
    5245 : { GREETING: "",
             QUEST : "É, parece que funcionou.\aMas eu fico solitário quando tomo banho...\aSerá que você poderia pescar um patinho de borracha para me fazer companhia?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não acha o patinho de borracha?" },
    5246 : { QUEST : "O patinho é ótimo, mas...\aTodos aqueles edifícios aqui em volta me deixam com os nervos em frangalhos.\aEu me sentiria bem melhor se houvesse menos edifícios por aqui.",
             LEAVING : "",
             COMPLETE : "Ok, agora eu vou tomar banho. Ah, aqui está uma coisinha para você.",
             INCOMPLETE_PROGRESS : "Ainda estou preocupado com os edifícios.", },
    5251 : { QUEST : "Vítor Vestíbulo devia estar fazendo um show nesta noite.\aOuvi falar que ele estava tendo problemas com o equipamento._where_" },
    5252 : { GREETING: "",
             QUEST : "É isso aí! Seria bom mesmo aceitar a sua ajuda.\aAqueles Cogs entraram aqui e levaram todas as engrenagens do meu equipamento enquanto eu estava descarregando a caminhonete.\aVocê pode me dar uma mãozinha e conseguir de volta o meu microfone?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Cara, eu não consigo cantar sem o microfone." },
    5253 : { GREETING: "",
             QUEST : "Legal, você conseguiu meu microfone de volta.\aValeu, mas...\aEu preciso mesmo do meu teclado para poder fazer um som.\aAcho que um daqueles Aventureiros Corporativos o levaram.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não conseguiu pegar o meu teclado?" },
    5273 : { GREETING: "",
             QUEST : "Legal, você conseguiu meu microfone de volta.\aValeu, mas...\aEu preciso mesmo do meu teclado para poder fazer um som.\aAcho que um daqueles Amizades Fáceis o levaram.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não conseguiu pegar o meu teclado?" },
    5274 : { GREETING: "",
             QUEST : "Legal, você conseguiu meu microfone de volta.\aValeu, mas...\aEu preciso mesmo do meu teclado para poder fazer um som.\aAcho que um daqueles Agiotas o levaram.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não conseguiu pegar o meu teclado?" },
    5275 : { GREETING: "",
             QUEST : "Legal, você conseguiu meu microfone de volta.\aValeu, mas...\aEu preciso mesmo do meu teclado para poder fazer um som.\aAcho que um daqueles Macacos velhos o levaram.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não conseguiu pegar o meu teclado?" },
    5254 : { GREETING: "",
             QUEST : "Tudo em cima! Agora estou na parada.\aSe ao menos eles não tivessem levado meus sapatos de plataforma...\aAqueles sapatos provavelmente acabaram com algum Dr. Celebridade, creio eu.",
             LEAVING : "",
             COMPLETE : "Tudo bem!! Estou pronto agora.\aOlá Brrrgh!!!\aHã? Onde está todo mundo?\aOk, pegue isto e reúna alguns fãs, está bem?",
             INCOMPLETE_PROGRESS : "Não posso me apresentar sem sapatos, né?" },
    5282 : { GREETING: "",
             QUEST : "Tudo em cima! Agora, estou na parada.\aSe ao menos eles não tivessem levado meus sapatos de plataforma...\aAqueles sapatos provavelmente acabaram com algum Rei da Cocada Preta, creio eu.",
             LEAVING : "",
             COMPLETE : "Tudo bem!! Estou pronto agora.\aOlá Brrrgh!!!\aHã? Onde está todo mundo?\aOk, pegue isto e reúna alguns fãs, está bem?",
             INCOMPLETE_PROGRESS : "Não posso me apresentar sem sapatos, né?" },
    5283 : { GREETING: "",
             QUEST : "Tudo em cima! Agora estou na parada.\aSe ao menos eles não tivessem levado meus sapatos de plataforma...\aAqueles sapatos provavelmente acabaram com algum Barão Ladrão, creio eu.",
             LEAVING : "",
             COMPLETE : "Tudo bem!! Estou pronto agora.\aOlá Brrrgh!!!\aHã? Onde está todo mundo?\aOk, pegue isto e reúna alguns fãs, está bem?",
             INCOMPLETE_PROGRESS : "Não posso me apresentar sem sapatos, né?" },
    5284 : { GREETING: "",
             QUEST : "Tudo em cima! Agora, estou na parada.\aSe ao menos eles não tivessem levado meus sapatos de plataforma...\aAqueles sapatos provavelmente acabaram com algum Figurão, creio eu.",
             LEAVING : "",
             COMPLETE : "Tudo bem!! Estou pronto agora.\aOlá Brrrgh!!!\aHã? Onde está todo mundo?\aOk, pegue isto e reúna alguns fãs, está bem?",
             INCOMPLETE_PROGRESS : "Não posso me apresentar sem sapatos, né?" },

    5255 : { QUEST : "Parece que você pode usar mais pontos de risadas.\aTalvez _toNpcName_ entre em um acordo com você.\aNão deixe de firmar o acordo por escrito..._where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Trato é trato.",
             QUEST : "Então, você está atrás de pontos de risadas, né?\aSe eu tenho uma proposta para você!?\aÉ só tomar conta de alguns Cogs Robôs-chefe para mim...\aAí eu dou uma injeção de ânimo nos seus pontos." },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Trato é trato.",
             QUEST : "Então, você está atrás de pontos de risadas, né?\aSe eu tenho uma proposta para você!?\aÉ só tomar conta de alguns Cogs Robôs da Lei para mim...\aAí eu dou uma injeção de ânimo nos seus pontos." },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Ok, mas tenho certeza de que falei para você reunir alguns Cogs Robôs da Lei.\aBom, se você está falando, tudo bem, mas, então, fica me devendo uma.",
             INCOMPLETE_PROGRESS : "Acho que você não terminou ainda.",
             QUEST : "Você está dizendo que acabou? Derrotou todos os Cogs?\aVocê deve ter entendido errado, nosso trato era para os Cogs Robôs Vendedores.\aTenho certeza de que disse para você derrotar alguns Cogs Robôs Vendedores para mim." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Ok, mas tenho certeza de que falei para você reunir alguns Cogs Robôs da Lei.\aBom, se você está falando, tudo bem, mas, então, fica me devendo uma.",
             INCOMPLETE_PROGRESS : "Acho que você não terminou ainda.",
             QUEST : "Você está dizendo que acabou? Derrotou todos os Cogs?\aVocê deve ter entendido errado, nosso trato era para os Cogs Robôs Mercenários.\aTenho certeza de que disse para você derrotar alguns Cogs Robôs Mercenários para mim." },

    # Eddie the will give you laff point for helping him
    5301 : { QUEST : "Eu não posso ajudar com os pontos de Risada, mas talvez _toNpcName_ faça negócio com você.\aMas ele é um pouco temperamental..._where_" },
    5302 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Eu te disse o quê?!?!\aValeu mesmo! Aqui está o seu ponto de Risada!",
             INCOMPLETE_PROGRESS : "Oi!\aO que está fazendo aqui de novo!",
             QUEST : "Um ponto de Risada? Acho que não!\aClaro, mas só se der um jeito em alguns desses Robôs da Lei antes." },

    # Johnny Cashmere will knit you a large bag if...
    5303 : { QUEST : lTheBrrrgh+" está repleto de Cogs perigosos.\aSe fosse você, carregaria mais piadas por aqui.\aOuvi dizer que  _toNpcName_ pode fazer uma bolsa maior para você se estiver a fim de trabalhar._where_" },
    5304 : { GREETING: "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Deve haver bastante Robôs da Lei lá fora.\aEntão mexa-se!" ,
             QUEST : "Uma bolsa maior?\aEu até poderia arranjar uma procê.\aMas vou precisar de fios.\aUns Robôs da Lei roubaram os meus fios ontem de manhã." },
    5305 : { GREETING : "Olá!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vai atacar mais uns cogs.\aEssa cor ainda não pegou.",
             QUEST : "Esse é um fio bom!\aMas não seria a minha primeira escolha de cor.\aVou te dizer...\aVai lá fora e derrote alguns dos cogs mais difíceis...\aE eu começo a a trabalhar em tingir este fio." },
    5306 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Eles têm que estar lá em algum lugar...",
             QUEST : "Bem, este fio está todo tingido. Mas tem um probleminha.\aNão consigo encontrar as minhas agulhas de tricô.\aO último lugar que estavam foi no lago."  },
    5307 : { GREETING : "",
             LEAVING : "Muito obrigado!",
             INCOMPLETE_PROGRESS : "Roma não foi tricotada em um dia!" ,
             QUEST : "Essas são as minhas agulhas.\aEnquanto eu tricoto, que tal fazer uma limpeza em alguns dos prédios grandes?",
             COMPLETE : "Ótimo trabalho!\aE falando em trabalho ótimo...\aAqui está a sua nova bolsa!" },

    # March Harry can also give you max quest = 4.
    5308 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ouvi dizer que _toNpcName_ tem problemas legais.\aVocê pode passar lá e dar uma olhada?_where_"  },
    5309 : { GREETING : "Que bom ver você...",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Rápido, por favor! A rua está transbordando com eles!",
             QUEST : "Os Robôs da Lei tomaram conta daqui.\aTemo que eles vão me levar a julgamento.\aVocê poderia me ajudar a tirá-los desta rua?"  },
    5310 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Acho que os ouço vindo por mim...",
             QUEST : "Obrigado. Sinto-me um pouco melhor agora.\a Mas tem mais uma coisa...\aVocê poderia ir até a casa de  _toNpcName_ e me conseguir um álibi?_where_"  },
    5311 : { GREETING : "O QUEEE!!!!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Não posso ajudá-lo se não encontrar!",
             QUEST : "Álibi?! Mas que ótima ideia!\aE traga duas!\aAposto que um Macaco velho deve ter alguns..."  },
    5312 : { GREETING : "Finalmente!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "",
             COMPLETE : "Ufa! Que alívio é ter isso.\aAqui está a sua recompensa...",
             QUEST : "Súper! É melhor você voltar até _toNpcName_!"  },

    # Powers Erge, though forgetful, will give you an LP boost
    # if you'll defeat some Cogs for him
    6201 : { QUEST : "Elle Étrica precisa de ajuda. Você pode passar lá e dar uma mãozinha a ela?_where_",
             },
    6202 : { GREETING : "",
             LEAVING : "",
             QUEST : "Um cliente! Beleza! Em que posso ajudar?\aComo assim, você me ajudar? AH! Você não é um cliente.\aAgora me lembrei. Você veio para me ajudar com aqueles Cogs horrorosos.\aNa verdade, eu aceitaria sua ajuda, você sendo um cliente ou não.\aSe você fizer uma pequena limpa nas ruas, dou uma coisa a você.",
             INCOMPLETE_PROGRESS : "Se você não quiser eletricidade, não posso ajudar até que derrote aqueles Cogs.",
             COMPLETE : "Bom trabalho com aqueles Cogs, _avName_.\aAgora, você tem certeza de que não quer um choquezinho? Pode ser útil....\aNão? OK, você que sabe.\aHã? Ah sim, lembro. Aqui está. Com certeza, vai ajudar você a deter aqueles Cogs nojentos.\aContinue assim!",
             },

    # Susan Siesta wants to get rich but the Cogs are interfering.
    # Take out some Cog buildings and she'll give you the small backpack
    6206 : { QUEST : "Bem, _avName_, não tenho nada para você agora.\aEspera aí! Acho que a Célia Sesta estava procurando ajuda. Por que não vai encontrá-la?_where_",
             },
    6207 : { GREETING : "",
             LEAVING : "",
             QUEST : "Nunca enriquecerei com aqueles malditos Cogs atrapalhando os meus negócios!\aVocê tem que me ajudar, _avName_.\aElimine alguns edifícios de Cogs para salvar a vizinhança e ajudarei você em sua poupança.",
             INCOMPLETE_PROGRESS : "O que farei agora? Você não conseguiu se livrar dos edifícios?",
             COMPLETE : "Agora, vou entrar na grana! Agora sim!\aVou passar todo o meu tempo livre pescando. Agora, deixe-me enriquecer sua vida um pouquinho.\aLá vai!",
             },

    # Lawful Linda is fixing her answering machine.
    # Help her & she'll give you a 2LP reward.
    6211 : { QUEST : "Oi, _avName_! Ouvi dizer que a Linda Legal estava procurando você.\aPassa lá para fazer uma visitinha a ela._where_",
             },
    6212 : { GREETING : "",
             LEAVING : "",
             QUEST : "E aí! Nossa, como é bom ver você!\aFiquei trabalhando nesta secretária eletrônica nas horas vagas, mas faltam algumas peças.\aPreciso de mais três varas, e as do Conta-moedinha parecem perfeitas.\aVocê poderia tentar encontrar algumas varas de pescar para mim?",
             INCOMPLETE_PROGRESS : "Ainda à procura daquelas varas de pescar?",
             },
    6213 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, estas aqui já ajudam.\aEngraçado. Eu tinha certeza de que havia um cinto de segurança extra por aqui, mas não consigo encontrá-lo.\aVocê pode pegar um de uns Sacos de Dinheiro para mim? Valeu!",
             INCOMPLETE : "Olha, eu só posso ajudar você depois que conseguir aquele cinto de segurança.",
             },
    6214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Agora sim. Vai funcionar que é uma beleza.\aOnde está meu alicate? Não vou poder ajustar isto aqui sem o alicate.\aTalvez as pinças da Mão de vaca ajudem.\aSe você conseguir encontrá-las, dou a você uma coisa que vai ajudar na batalha com os Cogs.",
             INCOMPLETE_PROGRESS : "Nada das pinças ainda, né? Vai procurando.",
             COMPLETE : "Beleza! Agora é só fazer o ajuste aqui.\aParece que agora está funcionando. Estou de novo na ativa!\aNa verdade, falta ainda o telefone. Mas, estou satisfeito com a sua ajuda.\aAcho que isso vai ajudar você com os Cogs. Boa sorte!",
             },

    # Scratch Rocco's back and he'll scratch yours.
    # In fact, he'll give you a 3 LP bonus.
    6221 : { QUEST : "Ouvi dizer que Pedro estava atrás da sua ajuda. Veja o que pode fazer por ele._where_",
             },
    6222 : { GREETING : "",
             LEAVING : "",
             QUEST : "Qualé? Chegou no point certo. Não estou legal.\aÉ isso aí, tava procurando ajuda pra me livrar daqueles Cogs. Eles chegam e ficam mandando em mim.\aBem que você podia mandar aqueles Robôs-chefe se aposentarem. Você não vai se arrepender.",
             INCOMPLETE_PROGRESS : "E aí, _avName_, qual foi?\aVai lá atrás dos Robôs-chefe. A gente tem um trato, falou?\aO Pedro aqui tem palavra.",
             COMPLETE : "Qualé, _avName_! Agora, você está bem na fita.\aQuero ver os Robôs-chefe chefiar agora, né não?\aVamo lá! Um tremendo acréscimo pra você. Agora, vê se não entra em nenhuma fria, falou?",
             },

    # Nat & PJ will get you acquainted with the new
    # HQ. And they'll give you your first suit part
    6231 : { QUEST : "O Zezé ouviu um boato na Alameda do Pijama sobre um Quartel do Robô Mercenário.\aVai lá e veja se consegue ajudá-lo._where_",
             },
    6232 : { GREETING : "",
             LEAVING : "",
             QUEST : "Soube de umas coisas estranhas que estão acontecendo.\aTalvez sejam as pulgas, mas deve ter alguma coisa rolando.\aTodos esses Robôs Mercenários!\aAcho que abriram outro quartel bem na Alameda do Pijama.\aO Py Jama sabe o caminho.\aVá ver _toNpcName_ _where_ Pergunte a ele se viu alguma coisa.",
             INCOMPLETE_PROGRESS : "Ainda não viu o Py Jama? O que você está esperando?\aAi, essas malditas pulgas!",
             },
    6233 : { GREETING : "",
             LEAVING : "",
             QUEST : "E aí, _avName_, para onde você está indo?\aPara o Quartel dos Robôs Mercenários?? Eu não vi nada.\aVocê pode ir até o final da Alameda do Pijama e ver se é verdade?\aEncontre alguns Cogs do Robô Mercenário no quartel, derrote alguns deles e venha me contar.",
             INCOMPLETE_PROGRESS : "Já encontrou o Quartel? Você precisará derrotar alguns Robôs Mercenários para localizá-lo.",
             },
    6234 : { GREETING : "",
             LEAVING : "",
             QUEST : "O quê?! Existe mesmo um Quartel de Robôs Mercenários?\aÉ melhor você ir e contar a Zezé agora mesmo!\aQuem poderia imaginar que existiria um Quartel de Cogs na rua bem em frente a ele?",
             INCOMPLETE_PROGRESS : "O que Zezé disse? Você ainda não o encontrou?",
             },
    6235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Estou tentado para ouvir o que o Py Jamas disse.\aHmm... Precisamos de mais informações sobre esse negócio de Cog, mas preciso me livrar dessas pulgas!\aEu sei! VOCÊ pode descobrir mais coisas!\aVá derrotar os Robôs Mercenários no Quartel até encontrar alguns planos, depois venha direto pra cá!",
             INCOMPLETE_PROGRESS : "Nada ainda? Continue procurando esses Cogs!\aEles devem ter algum plano!",
             COMPLETE : "Você conseguiu os planos?\aExcelente! Vejamos o que diz aqui.\aEntendi... os Robôs Mercenários construíram uma Casa da Moeda para fabricar grana Cog.\aDeve estar CHEIA de Robôs Mercenários. Precisamos averiguar.\aE se você se disfarçasse? Hmmm...Já sei! Acho que tenho uma peça de vestimenta de Cog aqui em algum lugar....\aAqui está! Isto aqui é para compensar o trabalho. Agradeço novamente pela ajuda!",
             },

    # The Countess can't concentrate on counting her sheep with all
    # these Cogs around. Clean up a bit and she'll reward you handsomely.
    # Reward: MaxMoneyReward 705 - 150 jellybeans
    6241 : { QUEST : "A Condessa está procurando você por toda parte! Visite-a logo para que pare de ligar _where_",
             },
    6242 : { GREETING : "",
             LEAVING : "",
             QUEST : "_avName_, conto com a sua ajuda!\aSabe, esses Cogs estão fazendo tanto barulho que eu simplesmente não consigo me concentrar.\aPerco a conta dos carneirinhos a todo instante!\aSe você acabar com esse barulho, te dou uma ajuda! Pode contar com isso!\aMas, onde eu parei mesmo? Ah sim: cento e trinta e seis, cento e trinta e sete....",
             INCOMPLETE_PROGRESS : "Quatrocentos e quarenta e dois... Quatrocentos e quarenta e três...\aO quê? Você já voltou? Mas ainda tem tanto barulho!\aEssa não, perdi a conta novamente.\a Um...dois...três....",
             COMPLETE : "Quinhentos e noventa e três... Quinhentos e noventa e quatro...\aOlá? Ah, eu sabia que poderia contar com a sua ajuda! Agora, o silêncio voltou.\aPegue aqui, por todos esses Destruidores de Números.\aContar? Agora preciso começar a contar tudo outra vez! Um...dois....",
             },

    # Zari needs you to run some errands for her and maybe
    # wipe out some Cogs along the way. She'll make it worthwhile
    # though, she'll give you 4 LP if you run the gauntlet.
    6251 : { QUEST : "Pobre Zéfiro, o zíper dela quebrou e, agora, ela não consegue fazer as entregas de seus clientes. Ela certamente precisa de sua ajuda._where_",
             },
    6252 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oi _avName_. Você está aqui para ajudar com minhas entregas?\aIsso é ótimo! Com esse zíper quebrado é muito difícil fazer as entregas sozinha.\aDeixe-me ver... Ok, vai ser fácil. O Vaqueiro George pediu uma cítara semana passada.\aVocê poderia levá-la para ele? _where_",
             INCOMPLETE_PROGRESS : "Oi! Esqueceu alguma coisa? O Vaqueiro George está esperando pela cítara.",
             },
    6253 : { GREETING : "",
             LEAVING : "",
             QUEST : "Minha cítara! Finalmente! Caramba, mal posso esperar para tocá-la.\aPoderia agradecer à Zéfiro por mim?",
             INCOMPLETE_PROGRESS : "Obrigado novamente pela cítara. A Zéfiro não tem mais entregas para você fazer?",
             },
    6254 : { GREETING : "",
             LEAVING : "",
             QUEST : "Essa foi rápida. Qual será o próximo item da minha lista?\aAh sim! Mestre Mário pediu um Zamboni. Aquele zombeteiro.\aPoderia levar para ele?_where_",
             INCOMPLETE_PROGRESS : "Aquele Zamboni precisa ser levado para o Mestre Mário._where_",
             },
    6255 : { GREETING : "",
             LEAVING : "",
             QUEST : "Tudo certo! O Zamboni que eu pedi!\aAgora, se não houvesse tantos Cogs por aí, eu teria algum tempo para usá-lo.\aSeja gentil e cuide de alguns desses Robôs Mercenários para mim, tudo bem?",
             INCOMPLETE_PROGRESS : "Esses Robôs Mercenários são durões, não são? Assim, eu não consigo testar o meu Zamboni.",
             },
    6256 : { GREETING : "",
             LEAVING : "",
             QUEST : "Excelente! Agora, eu posso testar o meu Zamboni.\aDiga à Zéfiro que eu estarei lá para fazer um outro pedido na próxima semana.",
             INCOMPLETE_PROGRESS : "Por enquanto é só isso. A Zéfiro não está esperando por você?"
             },
    6257 : { GREETING : "",
             LEAVING : "",
             QUEST : "Então, o Mestre Mário ficou satisfeito com o Zamboni? Excelente.\aQuem é o próximo? Ah, o Bob Bocão pediu uma almofada zabuton com listras de zebra.\aAqui está! Poderia ir até a casa dele?_where_",
             INCOMPLETE_PROGRESS : "Acho que o Bob Bocão precisa da almofada zabuton para meditar.",
             },
    6258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, minha almofada zabuton finalmente. Agora, eu posso meditar.\aQuem consegue se concentrar com aquela algazarra? Todos aqueles Cogs!\aJá que você está aqui, poderia cuidar de alguns desses Cogs?\aSó assim eu poderei usar minha almofada zabuton em paz.",
             INCOMPLETE_PROGRESS : "Ainda há muito barulho com esses Cogs! Quem consegue se concentrar?",
             },
    6259 : { GREETING : "",
             LEAVING : "",
             QUEST : "Paz e silêncio afinal. Obrigado, _avName_.\aDiga à Zéfiro que estou muito satisfeito. OM....",
             INCOMPLETE_PROGRESS : "A Zéfiro ligou procurando por você. É melhor você ir ver o que ela precisa.",
             },
    6260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Estou feliz em saber que o Bob Bocão está satisfeito com sua almofada zabuton de zebra.\aAh, estas zínias acabaram de chegar para a Rosa Sonada.\aJá que você parece tão animado para fazer entregas, talvez possa levar essas zínias para ela, não é?_where_",
             INCOMPLETE_PROGRESS : "Essas zínias vão murchar se você não fizer logo a entrega.",
             },
    6261 : { GREETING : "",
             LEAVING : "",
             QUEST : "Que lindas zínias! Certamente que é entrega da Zéfiro.\aQuer dizer, é SUA entrega, _avName_. Agradeça à Zéfiro por mim!",
             INCOMPLETE_PROGRESS : "Não se esqueça de agradecer à Zéfiro pelas zínias!",
             },
    6262 : { GREETING : "",
             LEAVING : "",
             QUEST : "Que bom que voltou, _avName_. Você é bastante veloz.\aVejamos... Qual é o próximo item da lista a ser entregue? Discos de forró para Jatha Cordada._where_",
             INCOMPLETE_PROGRESS : "Tenho certeza de que Jatha Cordada está esperando por esses discos de forró.",
             },
    6263 : { GREETING : "",
             LEAVING : "",
             QUEST : "Discos de forró? Não me lembro de ter pedido discos de forró.\aAh, aposto que foi Denis Nar quem pediu._where_",
             INCOMPLETE_PROGRESS : "Não, esses discos de forró são para Denis Nar._where_",
             },
    6264 : { GREETING : "",
             LEAVING : "",
             QUEST : "Finalmente, meus discos de forró! Pensei que a Zéfiro tivesse se esquecido.\aPoderia levar essa abobrinha para ela? Ela encontrará alguém que esteja querendo uma. Valeu!",
             INCOMPLETE_PROGRESS : "Eu já tenho muitas abobrinhas. Leve esta para Zéfiro.",
             },
    6265 : { GREETING : "",
             LEAVING : "",
             QUEST : "Abobrinha? Hmm. Bem, alguém irá querer, tenho certeza.\aOk, estamos quase terminando com a minha lista. Mais uma entrega a fazer.\aNenê Crespo pediu um paletó zoot._where_",
             INCOMPLETE_PROGRESS : "Se você não entregar esse paletó zoot ao Nenê Crespo,\a ele ficará todo amarrotado.",
             },
    6266 : { GREETING : "",
             LEAVING : "",
             QUEST : "Era uma vez... Ah! Você não está aqui para ouvir uma história, não é?\aÉ a entrega do meu terno zoot? Beleza! Uau, isso aqui é demais.\aEi, poderia dar um recado meu para a Zéfiro? Precisarei de abotoaduras de zircônio para usar com o paletó. Valeu!",
             INCOMPLETE_PROGRESS : "Você deu o meu recado à Zéfiro?",
             COMPLETE : "Abotoaduras de zircônio, certo? Bem, verei o que posso fazer por ele.\aSeja como for, você tem sido muito útil e não posso deixar você ir sem nada.\aAqui está um GRANDE acréscimo para ajudar a derrotar esses Cogs!",
             },

    # Drowsy Dave will give you teleport access to DL
    # if he can stay awake long enough for you to finish.
    6271 : { QUEST : "Solano Sonolento está tendo problemas e você talvez possa ajudá-lo. Por que você não dá uma passada na loja dele?_where_",
             },
    6272 : { GREETING : "",
             LEAVING : "",
             QUEST : "O quê? Hã? Eu devo ter cochilado.\aSabe, esses edifícios de Cogs estão cheios de máquinas que realmente me dão um sono.\aEu ouço esse zumbido o dia inteiro e...\aHã? Ah, sim, está certo. Se você pudesse se livrar de alguns desses edifícios de Cogs, eu conseguiria ficar acordado.",
             INCOMPLETE_PROGRESS : "Zzzzz...hã? Ah, é você, _avName_.\aJá está de volta? Eu só estava tirando uma sonequinha.\aVolte quando acabar com esses edifícios.",
             COMPLETE : "O quê? Eu caí no sono um minutinho.\aAgora que aqueles edifícios de Cogs viraram pó, finalmente posso relaxar.\aValeu pela ajuda, _avName_.\aVejo você depois! Acho que vou tirar uma sonequinha.",
             },

    # Teddy Blair has a piece of a cog suit to give you if you will
    # clear out some cogs. Of course, his ear plugs make it tough.
    6281 : { QUEST : "Vá em frente e ligue para o Ursinho de P. Lúcia. Ele tem um trabalho para você._where_",
             },
    6282 : { GREETING : "",
             LEAVING : "",
             QUEST : "O que você disse? Não, eu não tenho um baralho pra você.\aAh, é um trabalho! Por que você não disse logo? Você precisa falar alto.\aEsses Cogs não me deixam hibernar. Se você ajudar a tornar a Sonholândia mais silenciosa,\aeu lhe darei uma coisinha.",
             INCOMPLETE_PROGRESS: "Você derrotou os bogs? Que bogs?\aAh, os Cogs! Por que você não disse logo?\aHmm, ainda tem barulho. O que acha de derrotar mais alguns?",
             COMPLETE : "Você se divertiu? Hã? Ah!\aVocê conseguiu! Beleza. Muito legal você ter me ajudado.\aEu achei isso nos fundos da loja, mas não tem utilidade para mim.\aTalvez você descubra o que fazer com isso. Até logo, _avName_!",
             },

    # William Teller needs help! Those darn Cashbots swiped his 3
    # money bags to use in the Mint! Retrieve them and he'll give you
    # another cog Suit piece.
    6291 : { QUEST : "Os Cogs arrombaram o Banco A Fraldinha de Dormir! Vá até o Guilherme Sonoleve e veja se você pode ajudá-lo.",
             },
    6292 : { QUEST : "Aqueles malditos Cogs do Robô Mercenário! Eles roubaram meus abajures de leitura!\aEu preciso deles de volta agora mesmo. Você pode procurar por eles?\aSe você encontrar meus abajures, talvez eu possa ajudar a encontrar o Diretor Financeiro.\aDepressa!",
             INCOMPLETE_PROGRESS : "Eu preciso dos abajures de volta. Continue procurando!",
             COMPLETE : "Você voltou! E trouxe meus abajures!\aNão tenho como agradecer o favor, mas posso dar isto a você.",
             },

    # Help Nina Nightlight get a bed in stock -
    # she'll give you a suit part
    7201 : { QUEST : "Nana de Nina estava à sua procura, _avName_. Ela precisa de ajuda._where_",
             },
    7202 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah! Estou tão feliz em ver você, _avName_. Espero que possa me ajudar!\aAqueles malditos Cogs assustaram o pessoal da entrega e não tenho mais camas no estoque.\aPoderia ir ao Pedro Fuso e trazer uma cama para mim?_where_",
             INCOMPLETE_PROGRESS : "O Pedro tinha alguma cama? Tinha certeza de que ele teria uma.",
             COMPLETE : "",
             },
    7203 : { GREETING : "",
             LEAVING : "",
             QUEST : "Uma cama? Isso mesmo, aqui está uma prontinha para viagem.\aEntregue a cama pra Nana por mim, OK? Cama, Nana...\a\"Rimou!\" Há-há!\aMuito engraçado. Não? Bem, mas leve para ela, por favor.",
             INCOMPLETE_PROGRESS : "A Nana gostou da cama?",
             COMPLETE : "",
             },
    7204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Essa cama não está legal. Ela é muito simples.\aVocê poderia ir até lá e ver se ele tem alguma coisa mais sofisticada?\aTenho certeza de que não vai demorar nadinha.",
             INCOMPLETE_PROGRESS : "Estou certa de que o Pedro tem uma cama mais sofisticada.",
             COMPLETE : "",
             },
    7205 : { GREETING : "",
             LEAVING : "",
             QUEST : "Não acertei na mosca com essa cama, não é? Tenho uma aqui que servirá.\aSó tem um pequeno problema: é preciso montá-la primeiro.\aEnquanto eu resolvo esse problema, você pode se livrar de alguns Cogs que estão lá fora?\aAqueles terríveis Cogs jogaram uma chave inglesa nos móveis.\aVolte quando terminar e a cama estará pronta.",
             INCOMPLETE_PROGRESS : "Ainda não terminei a montagem da cama.\aQuando você tiver acabado com os Cogs, ela estará pronta.",
             COMPLETE : "",
             },
    7206 : { GREETING : "",
             LEAVING : "",
             QUEST : "E aí _avName_!\aVocê fez um excelente trabalho com aqueles Cogs.\aA cama já está prontinha. Você pode entregá-la para mim?\aAgora que aqueles Cogs se foram, as coisas estão rápidas por aqui!",
             INCOMPLETE_PROGRESS : "Acho que a Nana está esperando pela entrega da cama.",
             COMPLETE : "Que cama adorável!\aAgora, meus clientes ficarão satisfeitos. Obrigada, _avName_.\aOlha só, talvez você possa usar isto. Alguém deixou isso aqui.",
             },
    7209 : { QUEST : "Vá até a Lua de Mel. Ela precisa de ajuda._where_",
             },
    7210 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah! Estou tão feliz em ver você, _avName_. Eu preciso muito de ajuda!\aNão consigo tirar o meu sono reparador há séculos. Veja você, aqueles Cogs roubaram a minha colcha.\aVocê pode correr e ver se o Marcelo tem alguma coisa em azul?_where_",
             INCOMPLETE_PROGRESS : "O que o Marcelo falou sobre a colcha azul?",
             COMPLETE : "",
             },
    7211 : { GREETING : "",
             LEAVING : "",
             QUEST : "Então, a Mel quer uma colcha, né?\aDe que cor? AZUL?!\aBem, eu terei de fazer uma especialmente para ela. Tudo o que eu tenho aqui é em vermelho.\aEscuta... Se você for derrotar alguns Cogs lá fora, farei uma colcha azul especialmente para ela.\aColchas azuis... O que será da próxima vez?",
             INCOMPLETE_PROGRESS : "Ainda estou trabalhando na colcha azul, _avName_. Continue a derrotar esses Cogs!",
             COMPLETE : "",
             },
    7212 : { GREETING : "",
             LEAVING : "",
             QUEST : "Que bom ver você novamente. Tenho algo pra você!\aAqui está a colcha, e é azul. Ela vai adorar.",
             INCOMPLETE_PROGRESS : "A Mel gostou da colcha?",
             COMPLETE : "",
             },
    7213 : { GREETING : "",
             LEAVING : "",
             QUEST : "Minha colcha? Não, não está legal.\aÉ XADREZ! Como alguém pode dormir com uma estampa tão CHAMATIVA?\aVocê terá que levá-la de volta e trazer uma outra colcha.\aTenho certeza de que ele tem outras.",
             INCOMPLETE_PROGRESS : "Eu simplesmente não vou aceitar uma colcha xadrez. Veja o que Marcelo pode fazer.",
             COMPLETE : "",
             },
    7214 : { GREETING : "",
             LEAVING : "",
             QUEST : "O quê? Ela não gosta de XADREZ?\aHmm... Deixe-me ver o que eu tenho aqui.\aIsso vai levar algum tempo. Por que você não cuida de alguns Cogs enquanto eu tento encontrar algo diferente?\aTerei alguma coisa quando você estiver de volta.",
             INCOMPLETE_PROGRESS : "Ainda estou procurando uma colcha diferente. Como está indo com os Cogs?",
             COMPLETE : "",
             },
    7215 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ei, bom trabalho com os Cogs!\aAqui está, é azul e não é xadrez.\aEspero que ela goste de estampado.\aLeve a colcha para a Mel.",
             INCOMPLETE_PROGRESS : "Isso é tudo o que eu tenho para você agora.\aPor favor, leve esta colcha para a Mel.",
             COMPLETE : "Ah! Que linda! Estampado combina muito bem comigo.\aÉ hora do meu sono reparador! Até logo, _avName_.\aO quê? Você ainda está aqui? Não vê que estou tentando dormir?\aTome isto aqui e me deixe descansar. Devo estar medonha!",
             },

    7218 : { QUEST : "Dafne Sonolinda precisa de ajuda._where_",
             },
    7219 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, _avName_, estou tão feliz em ver você! Aqueles Cogs levaram meus travesseiros.\aVocê pode ver se o Lelê tem alguns travesseiros?_where_\aTenho certeza de que ele pode ajudar.",
             INCOMPLETE_PROGRESS : "O Lelê tem algum travesseiro para mim?",
             COMPLETE : "",
             },
    7220 : { GREETING : "",
             LEAVING : "",
             QUEST : "Como vai? A Dafne precisa de alguns travesseiros, né? Bem, você veio ao lugar certo, parceria!\aHá mais travesseiros aqui do que espinhos em um cacto.\aAqui está, _avName_. Leve estes para Dafne, com os meus cumprimentos.\aÉ sempre um prazer ajudar uma mocinha.",
             INCOMPLETE_PROGRESS : "Os travesseiros eram macios o suficiente para uma pequena dama?",
             COMPLETE : "",
             },
    7221 : { GREETING : "",
             LEAVING : "",
             QUEST : "Você trouxe os travesseiros! Valeu!\aEi, espere um segundo! Esses travesseiros são muito macios.\aMacios demais para mim. Preciso de travesseiros mais duros.\aLeve estes de volta para o Lelê e veja o que mais ele tem. Valeu.",
             INCOMPLETE_PROGRESS : "Não! Muito macios. Peça ao Lelê outros travesseiros.",
             COMPLETE : "",
             },
    7222 : { GREETING : "",
             LEAVING : "",
             QUEST : "Muito macios, né? Bem, deixe-me ver o que tenho....\aHmm... Eu achava que tinha um montão de travesseiros duros. Onde eles estão?\aAh! Lembrei. Eu estava vendo se conseguia devolvê-los, então devem estar no estoque.\aQue tal eliminar alguns desses edifícios de Cogs lá fora enquanto eu pego os travesseiros no estoque, parceria?",
             INCOMPLETE_PROGRESS : "Os edifícios de Cog são duros de roer. Mas esses travesseiros não são.\aContinuarei procurando.",
             COMPLETE : "",
             },
    7223 : { GREETING : "",
             LEAVING : "",
             QUEST : "Já está de volta? Está tudo bem. Veja, encontrei os travesseiros que a Dafne queria.\aAgora é só levar para ela. Eles são duros o suficiente para quebrar um dente!",
             INCOMPLETE_PROGRESS : "É, esses travesseiros são bastante duros. Espero que a Dafne goste deles.",
             COMPLETE : "Eu sabia que o Lelê teria alguns travesseiros mais duros.\aAh sim, estes são perfeitos. Bons e duros.\aPor acaso esta peça de vestimenta de Cog seria útil para você? Pode levar.",
             },

    # Sandy Sandman lost her pajamas but Big Mama
    # and Cat can help her out. If you hang in there,
    # you'll get another Cog Suit part.
    7226 : { QUEST : "Passe lá na Cuca P. Gol. Ela perdeu o pijama._where_",
             },
    7227 : { GREETING : "",
             LEAVING : "",
             QUEST : "Não tenho pijamas! Eles sumiram!\aO que vou fazer? Ah! Já sei!\aVá até a Mama. Ela terá pijamas para mim._where_",
             INCOMPLETE_PROGRESS : "A Mama tem pijamas para mim?",
             COMPLETE : "",
             },
    7228 : { GREETING : "",
             LEAVING : "",
             QUEST : "E aí, pequeno Toon? A Mama tem os melhores pijamas das Bahamas.\aAh, quer algo para a Cuca P. Gol, né? Bem, deixe-me ver o que tenho aqui.\aAqui está. Agora, ela pode dormir com estilo!\aVocê pode correr e levar isso para ela? Não posso deixar a loja sozinha agora.\aObrigada, _avName_. Vejo você por aí!",
             INCOMPLETE_PROGRESS : "Você precisa levar esse pijama para a Cuca P. Gol._where_",
             COMPLETE : "",
             },
    7229 : { GREETING : "",
             LEAVING : "",
             QUEST : "A Mama mandou esse para mim? Ah...\aEla não tem nenhum pijama com pés?\aEu sempre uso pijamas com pés. Todo mundo usa esse tipo de pijama...\aLeve este de volta e peça a ela que encontre um com pés.",
             INCOMPLETE_PROGRESS : "Meu pijama precisa ter pés. Veja o que a Mama pode fazer.",
             COMPLETE : "",
             },
    7230 : { GREETING : "",
             LEAVING : "",
             QUEST : "Pés? Deixe-me pensar....\aEspere aí! Eu tenho um perfeito!\aTchan! Pijama com pés. Um lindo pijama azul com pés. O melhor de toda a face da terra.\aVocê pode levar para ela? Valeu!",
             INCOMPLETE_PROGRESS : "A Cuca P. Gol gostou do pijama azul com pés?",
             COMPLETE : "",
             },
    7231 : { GREETING : "",
             LEAVING : "",
             QUEST : "Bem, este TEM pés, mas não posso usar pijama azul!\aPergunte à Mama se ela tem uma cor diferente.",
             INCOMPLETE_PROGRESS : "Tenho certeza de que a Mama tem pijamas em uma cor diferente e com pés.",
             COMPLETE : "",
             },
    7232 : { GREETING : "",
             LEAVING : "",
             QUEST : "Que pena. Estes são os únicos pijamas com pés que eu tenho.\aAh, tive uma ideia. Vá perguntar à outra Cuca. Ela talvez tenha algum pijama com pés._where_",
             INCOMPLETE_PROGRESS : "Não, aqueles são os únicos que eu tenho. Vá até a outra Cuca para ver o que ela tem._where_",
             COMPLETE : "",
             },
    7233 : { GREETING : "",
             LEAVING : "",
             QUEST : "Pijama com pés? Sem dúvida.\aComo assim, este é azul? Ela não quer azul?\aNossa, vai ser um pouco difícil. Veja, que tal este?\aEle não é azul e TEM pés.",
             INCOMPLETE_PROGRESS : "Eu adoro marrom, você não?\aEspero que a Cuca P. Gol goste....",
             COMPLETE : "",
             },
    7234 : { GREETING : "",
             LEAVING : "",
             QUEST : "Não, este não é azul, mas ninguém com o meu tom de pele poderia usar marrom.\aNão e não. Ele vai fazer o caminho de volta, e você irá com ele! Veja o que mais a Cuca tem.",
             INCOMPLETE_PROGRESS : "A Cuca deve ter mais pijamas. Nada de marrom!",
             COMPLETE : "",
             },
    7235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Não pode ser marrom também. Hmm....\aEu sei que tenho outros.\aVai demorar um pouquinho para encontrá-los. Vamos fazer um trato.\aEu procuro outro pijama se você derrotar alguns desses edifícios de Cog. Eles perturbam demais.\aTerei o pijama quando você voltar, _avName_.",
             INCOMPLETE_PROGRESS : "Você precisa eliminar mais alguns edifícios de Cog enquanto eu procuro outro pijama.",
             COMPLETE : "",
             },
    7236 : { GREETING : "",
             LEAVING : "",
             QUEST : "Você fez um excelente trabalho com esses Cogs! Valeu!\aAchei este pijama para a Cuca P. Gol; espero que ela goste.\aLeve-o para ela. Obrigada.",
             INCOMPLETE_PROGRESS : "A Cuca P. Gol está esperando pelo pijama, _avName_.",
             COMPLETE : "Um pijama fúcsia com pés! Perr-feito!\aAh, agora estou pronta. Vejamos....\aAcho que devo lhe dar alguma coisa por ter me ajudado.\aTalvez você possa usar isto. Alguém deixou aqui.",
             },

    # Smudgy Mascara needs Wrinkle Cream but
    # 39's missing ingredients. Help them out
    # and get a piece of Cog suit
    7239 : { QUEST : "Vá até a Máki Agem. Ela está procurando ajuda._where_",
             },
    7240 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aqueles malditos Cogs levaram meu creme para rugas!\aMeus clientes PRECISAM do creme para rugas enquanto eu trabalho neles.\aVá até o Dedé Descanso e veja se ele tem a minha fórmula especial no estoque._where_",
             INCOMPLETE_PROGRESS : "Eu me recuso a trabalhar em alguém sem o creme para rugas.\aVeja o que o Dedé Descanso tem para mim.",
             },
    7241 : { GREETING : "",
             LEAVING : "",
             QUEST : "A Máki Agem é uma figura exigente. Ela não vai se contentar com a minha fórmula comum.\aIsso significa que eu precisarei de alguns corais de couve-flor, meu ingrediente especial supersecreto. Mas eu não tenho nada no estoque.\aVocê poderia pescar alguns na lagoa? Assim que você conseguir os corais, eu farei um lote de creme para a Máki Agem.",
             INCOMPLETE_PROGRESS : "Precisarei do coral de couve-flor para fazer o lote de creme para rugas.",
             },
    7242 : { GREETING : "",
             LEAVING : "",
             QUEST : "Uau, que belo coral de couve-flor!\aOk, vejamos... Um pouco disto e uma pitada daquilo... Agora, um bocado de alga-marinha.\aEssa não, onde está a alga-marinha? Parece que estou sem alga-marinha também.\aVocê pode voltar à lagoa e pescar uma boa alga-marinha viscosa?",
             INCOMPLETE_PROGRESS : "Nem uma laminazinha de alga-marinha viscosa na loja.\aNão posso fazer o creme sem ela.",
             },
    7243 : { GREETING : "",
             LEAVING : "",
             QUEST : "Aaaah! Que ótima alga-marinha viscosa você trouxe, _avName_.\aAgora, é só espremer algumas pérolas no pilão.\aIh, onde está o meu pilão? Como vou fazer sem o pilão?\aAposto que aquele maldito Agiota o pegou quando esteve aqui!\aVocê precisa me ajudar a encontrá-lo! Ele estava indo ao Quartel do Robô Mercenário!",
             INCOMPLETE_PROGRESS : "Eu simplesmente não consigo triturar as pérolas sem um pilão.\aMalditos Agiotas!",
             },
    7244 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ótimo! Você trouxe o meu pilão!\aAgora voltemos ao trabalho. Triture aqui... Misture lá e...\aPronto! Diga à Máki Agem que é de boa qualidade e está fresquinho.",
             INCOMPLETE_PROGRESS : "Você precisa entregar isso para a Máki Agem enquanto está fresco.\aEla é muito exigente.",
             COMPLETE : "O Dedé Descanso não tinha frasco de creme maior que este? Não?\aBem, acho que vou pedir mais quando o meu acabar.\aAté logo, _avName_.\aO quê? Você ainda está aqui? Não vê que estou tentando trabalhar?\aTome isto aqui.",
             },

    # Lawbot HQ part quests
    11000 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se está interessado em peças de disfarce de Robôs da Lei, visite _toNpcName_.\aOuvi dizer que ele precisa de ajuda na sua pesquisa sobre o clima._where_",
              },
    11001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Sim, sim. Eu tenho peças de disfarce de Robôs da Lei.\aMas não tenho interesse nelas.\aO foco da minha pesquisa são as flutuações na temperatura ambiente de Toontown.\aEu troco com você as minhas peças de disfarce por termômetros de cogs.\aVocê pode começar em %s." % GlobalStreetNames[2100][-1],
              INCOMPLETE_PROGRESS : "Tentou procurar em %s?" % GlobalStreetNames[2100][-1],
              COMPLETE : "Ah, ótimo!\aComo eu temia...\aAh, é! Aqui está a sua peça de disfarce.",
             },

    11002 : { GREETING : "",
              LEAVING : "",
              QUEST : "Para mais peças de disfarce, visite _toNpcName_ de novo.\aOuvi dizer que ele precisa de assistentes de pesquisa._where_",
              },
    11003 : { GREETING : "",
              LEAVING : "",
              QUEST : "Mais peças de disfarce de Robô da Lei?\aBem, se você insiste...\amas eu vou precisar de outro termômetro de Cog.\aDesta vez, procure em %s." % GlobalStreetNames[2200][-1],
              INCOMPLETE_PROGRESS : "Você está procurando em %s, certo?" % GlobalStreetNames[2200][-1],
              COMPLETE : "Obrigado!\aE aqui está a sua peça de disfarce.",
             },
    11004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se precisa de mais peças de disfarce de Robô da Lei, vá falar com o _toNpcName_.\aOuvi que ele ainda precisa de ajuda com a pesquisa sobre o clima._where_",
              },
    11005 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você está me saindo bastante útil!\aVocê pode dar uma ollhada em %s?" % GlobalStreetNames[2300][-1],
              INCOMPLETE_PROGRESS : "Tem certeza de que está procurando em %s?" % GlobalStreetNames[2300][-1],
              COMPLETE : "Humm, não gostei muito da aparência disto...\amas aqui está a sua peça de disfarce...",
             },
    11006 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você-sabe-quem precisa de mais medições de temperatura.\aDê uma passada se quiser mais uma peça de disfarce._where_",
              },
    11007 : { GREETING : "",
              LEAVING : "",
              QUEST : "Já de volta?\aQue dedicação...\aA próxima parada é %s." % GlobalStreetNames[1100][-1],
              INCOMPLETE_PROGRESS : "Você já tentou observar %s?" % GlobalStreetNames[1100][-1],
              COMPLETE : "Isso! Parece que você está pegando o jeito da coisa!\aA sua peça de disfarce...",
             },
    11008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se estiver a fim de mais uma peça de disfarce de Robô da Lei..._where_",
              },
    11009 : { GREETING : "",
              LEAVING : "",
              QUEST : "Engraçado encontrar você aqui!\aAgora, eu preciso de medições em %s." % GlobalStreetNames[1200][-1],
              INCOMPLETE_PROGRESS : "Você está procurando em %s, certo?" % GlobalStreetNames[1200][-1],
              COMPLETE : "Muito obrigado.\aO seu disfarce deve estar quase pronto...",
             },
    11010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Acredito que _toNpcName_ tem mais um trabalho para você._where_",
              },
    11011 : { GREETING : "",
              LEAVING : "",
              QUEST : "Que bom ver você de novo, _avName_!\aVocê pode fazer uma medição em %s, por favor?" % GlobalStreetNames[1300][-1],
              INCOMPLETE_PROGRESS : "Tentou procurar em %s?" % GlobalStreetNames[1300][-1],
              COMPLETE : "Ótimo trabalho!\aAqui está a sua merecida recompensa!",
             },
    11012 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você sabe o que fazer._where_",
              },
    11013 : { GREETING : "",
              LEAVING : "",
              QUEST : "_avName_, meu caro!\aVocê pode ir até %s e encontrar mais um termômetro para mim?" % GlobalStreetNames[5100][-1],
              INCOMPLETE_PROGRESS : "Tem certeza de que está procurando em %s?" % GlobalStreetNames[5100][-1],
              COMPLETE : "Excelente!\aCom a sua ajuda, a minha pesquisa está caminhando!\aAqui está a sua recompensa.",
             },
    11014 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ estava pedindo por você.\aParece que você causou uma boa impressão!_where_",
              },
    11015 : { GREETING : "",
              LEAVING : "",
              QUEST : "Bem-vindo de volta!\aEstive esperando.\aA próxima medição tem que ser em %s." % GlobalStreetNames[5200][-1],
              INCOMPLETE_PROGRESS : "Você está procurando em %s, certo?" % GlobalStreetNames[5200][-1],
              COMPLETE : "Obrigado!\aAqui está sua recompensa.",
             },
    11016 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se precisa completar o seu disfarce de Robô da Lei...\a_toNpcName_ pode ajudar você._where_",
              },
    11017 : { GREETING : "",
              LEAVING : "",
              QUEST : "Olá, Cientista de Pesquisas Iniciante!\aAinda precisamos de medições de %s." % GlobalStreetNames[5300][-1],
              INCOMPLETE_PROGRESS : "Tentou procurar em %s?" % GlobalStreetNames[5300][-1],
              COMPLETE : "Ótimo trabalho!\aAqui está o seu negócio de Robô da Lei...",
             },
    11018 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tem outro trabalho para você.\aSe ainda não tiver se cansado dele..._where_",
              },
    11019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Então.\aPronto para outra recuperação?\aDesta vez, tente %s." % GlobalStreetNames[4100][-1],
              INCOMPLETE_PROGRESS : "Tem certeza de que está procurando em %s?" % GlobalStreetNames[4100][-1],
              COMPLETE : "Mais um!\aNossa, você é a eficiência em pessoa!",
             },
    11020 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ainda está atrás de peças de disfarce de Robô da Lei?_where_",
              },
    11021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você já deve ter adivinhado...\amas eu preciso de medições de %s." % GlobalStreetNames[4200][-1],
              INCOMPLETE_PROGRESS : "Você está procurando em %s, certo?" % GlobalStreetNames[4200][-1],
              COMPLETE : "Quase lá!\aAqui está...",
             },
    11022 : { GREETING : "",
              LEAVING : "",
              QUEST : "Odeio dizer isto, mas..._where_",
              },
    11023 : { GREETING : "",
              LEAVING : "",
              QUEST : "O que acha de %s? Poderia conseguir um termômetro de lá também?" % GlobalStreetNames[4300][-1],
              INCOMPLETE_PROGRESS : "Tentou procurar em %s?" % GlobalStreetNames[4300][-1],
              COMPLETE : "Outro ótimo trabalho, _avName_",
             },
    11024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Vá visitar o Professor se ainda precisar de peças de disfarce._where_",
              },
    11025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Acho que ainda precisamos de uma medição de %s." % GlobalStreetNames[9100][-1],
              INCOMPLETE_PROGRESS : "Tem certeza de que está procurando em %s?" % GlobalStreetNames[9100][-1],
              COMPLETE : "Bom trabalho!\aAcho que estamos chegando perto...",
             },
    11026 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tem uma última missão para você._where_",
              },
    11027 : { GREETING : "",
              LEAVING : "",
              QUEST : "Já de volta?\aA medição final é em %s." % GlobalStreetNames[9200][-1],
              INCOMPLETE_PROGRESS : "Você está procurando em %s, certo?" % GlobalStreetNames[9200][-1],
              COMPLETE : "Está pronto!\aAgora, você já pode se infiltrar no Escritório do Promotor Público e coletar Avisos de Júri.\aBoa sorte e obrigado pela sua ajuda!",
             },
    12000 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se quiser peças de disfarce de Robô Chefe, deve visitar _toNpcName_._where_",
              },
    12001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Sim, posso pegar as suas peças de Robô-Chefe.\aMas vou precisar de sua ajuda para completar a minha coleção de Robô-Chefe.\aVá lá fora e derrote um Puxa-saco.   ",
              INCOMPLETE_PROGRESS : "Não consegue encontrar um Puxa-saco? Que vergonha...",
              COMPLETE : "Você não fracassou, não é?\ aAqui está a sua primeira peça de disfarce. ",
             },
    12002 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ precisa de mais ajuda se você puder._where_ ",
              },
    12003 : { GREETING : "",
              LEAVING : "",
              QUEST : "Outra peça de disfarce?\aCertamente...\aMas só se você derrotar um Rato de Escritório. ",
              INCOMPLETE_PROGRESS : "Os Rato de Escritório podem ser encontrados nas ruas.",
              COMPLETE : "Ele realmente foi um fracote! \ aAqui está sua segunda peça de disfarce.",
             },
    12004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Só há mesmo um lugar onde encontrar peças de Robô-Chefe._where_",
              },
    12005 : { GREETING : "",
              LEAVING : "",
              QUEST : "Agora, preciso de um “Vaquinha de Presépio”...",
              INCOMPLETE_PROGRESS : "O “Vaquinha de Presépio” pode ser encontrado nas ruas.",
              COMPLETE : "Isso! Cara, você é demais.\aAqui está sua terceira peça de disfarce.",
             },
    12006 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tem mais peças para você... ",
              },
    12007 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se você derrotar um Micro\4empresário, darei a você mais uma peça.",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[1100][-1],
              COMPLETE : "Você se saiu muito bem!\aAqui está sua quarta peça de disfarce.",
             },
    12008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Direto para..._where_",
              },
    12009 : { GREETING : "",
              LEAVING : "",
              QUEST : "Agora estou atrás de um Facão...",
              INCOMPLETE_PROGRESS : "Algum problema? Tente procurar em %s" % GlobalStreetNames[3100][-1],
              COMPLETE : "Não foi tão difícil!\aAqui está sua quinta peça de disfarce. ",
             },
    12010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Acho que você sabe aonde ir agora..._where_",
              },
    12011 : { GREETING : "",
              LEAVING : "",
              QUEST : "Um Caça-\4talentos é o próximo da minha lista.",
              INCOMPLETE_PROGRESS : "Você terá mais sorte procurando em edifícios.",
              COMPLETE : "Vejo que não teve problemas para caçar um desses.\aAqui está sua sexta peça de disfarce. ",
             },
    12012 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ precisa de mais Robôs-Chefe. ",
              },
    12013 : { GREETING : "",
              LEAVING : "",
              QUEST : "A seguir, preciso que você localize um Aventureiro Corporativo.",
              INCOMPLETE_PROGRESS : "Você terá mais sorte procurando em edifícios.",
              COMPLETE : "Você leva mesmo jeito para isso!\aAqui está sua sétima peça de disfarce.",
             },
    12014 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se quiser mais peças de disfarce, vá para..._where_",
              },
    12015 : { GREETING : "",
              LEAVING : "",
              QUEST : "Agora, o mais precioso de todos: O um Rei da Cocada Preta!",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Sabia que podia contar com você para cortar...\aAh, não importa.\aAqui está sua próxima peça de disfarce. ",
             },
    12016 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ estava à sua procura...",
              },
    12017 : { GREETING : "",
              LEAVING : "",
              QUEST : "Agora, preciso que você derrote um dos novos e mais traiçoeiros Cogs de Robô-Chefe.",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Eles são mais fortes do que parecem, hein?\aAcho que lhe devo uma peça de disfarce. ",
             },
    12018 : { GREETING : "",
              LEAVING : "",
              QUEST : "Pode dar um giro até..._where_",
              },
    12019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Esses Cogs versão 2.0 são muito interessantes.\aPor favor, derrote mais um.  ",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Valeu!\aMais uma peça de disfarce chegando. ",
             },
    12020 : { GREETING : "",
              LEAVING : "",
              QUEST : "Se tiver a oportunidade, dê uma parada e visite _toNpcName_.",
              },
    12021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Imagino se puderem se regenerar...",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Acho que não.\aAqui está sua peça... ",
             },
    12022 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você sabe..._where",
              },
    12023 : { GREETING : "",
              LEAVING : "",
              QUEST : "Talvez não sejam Robôs-Chefe afinal...",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Hummm, acho que realmente são Robôs-Chefe.\aConsiga mais uma peça. ",
             },
    12024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você provavelmente já sabe o que vou dizer...",
              },
    12025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Talvez, de alguma maneira, estejam relacionados aos Esqueletocogs... ",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Isso foi inconsequente...\aAqui está sua peça de disfarce. ",
             },
    12026 : { GREETING : "",
              LEAVING : "",
              QUEST : "Por favor, visite _toNpcName_ novamente.",
              },
    12027 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ainda tenho dúvidas de que não sejam algum tipo de Esqueletocogs...",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Bem, talvez não.\aAqui está sua próxima peça. ",
             },
    12028 : { GREETING : "",
              LEAVING : "",
              QUEST : "Talvez seja o último lugar a que gostaria de ir. Mas...",
              },
    12029 : { GREETING : "",
              LEAVING : "",
              QUEST : "Esses novos Cogs ainda me deixam dúvidas.\aPoderia derrotar mais um, por favor?",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Fascinante. Simplesmente fascinante.\aUma peça de disfarce pelos inconvenientes. ",
             },
    12030 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ está começando a parecer um disco riscado...",
              },
    12031 : { GREETING : "",
              LEAVING : "",
              QUEST : "Já havia quase descoberto o que são esses novos Cogs.\aSó mais um... ",
              INCOMPLETE_PROGRESS : "Tente procurar em %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Sim, acho que encontrei algo importante.\aAh, sim.\aIsso é para você... ",
             },
    12032 : { GREETING : "",
              LEAVING : "",
              QUEST : "Você precisa contar ao Flippy sobre isso...",
              INCOMPLETE_PROGRESS : "Flippy está no Toon Hall",
              COMPLETE : "Um novo tipo de Cog!\aBom trabalho!\aAqui está sua última peça de disfarce.  ",
              },
 }

# ChatGarbler.py
ChatGarblerDog = ["au", "arf", "grrrr"]
ChatGarblerCat = ["miau", "miu"]
ChatGarblerMouse = ["quick", "quiiii", "quiiiiquiiii"]
ChatGarblerHorse = ["rííírrrr", "brrr"]
ChatGarblerRabbit = ["ick", "iipr", "iipi", "iicki"]
ChatGarblerDuck = ["quá", "quack", "quáááck"]
ChatGarblerMonkey = ["ooh", "ooo", "ahh"]
ChatGarblerBear = ["grrrau", "grrr"]
ChatGarblerPig = ["oinc", "oic", "rrroinc"]
ChatGarblerDefault = ["blá"]

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Procurando detalhes de %s."
AvatarDetailPanelFailedLookup = "Não foi possível obter detalhes de %s."
#AvatarDetailPanelPlayer = "Jogador: %(player)s\nMundo: %(world)s\nLocal: %(location)s"
# sublocation is not working now
AvatarDetailPanelPlayer = "Jogador: %(player)s\nMundo: %(world)s"
AvatarDetailPanelPlayerShort = "%(player)s\nMundo: %(world)s\nLocal: %(location)s"
AvatarDetailPanelRealLife = "Off-line"
AvatarDetailPanelOnline = "Região: %(district)s\nLocal: %(location)s"
AvatarDetailPanelOnlinePlayer = "Região: %(district)s\nLocal: %(location)s\nJogador: %(player)s"
AvatarDetailPanelOffline = "Região: off-line\nLocal: off-line"
AvatarShowPlayer = "Exibir Jogador"
OfflineLocation = "Off-line"

#PlayerDetailPanel
PlayerToonName = "Toon: %(toonname)s"
PlayerShowToon = "Mostrar Toon"
PlayerPanelDetail = "Detalhes do jogador"

# AvatarPanel.py
AvatarPanelFriends = "Amigos"
AvatarPanelWhisper = "Cochichar"
AvatarPanelSecrets = "Segredos"
AvatarPanelGoTo = "Ir para"
AvatarPanelPet = "Mostrar Rabisco"
AvatarPanelIgnore = "Ignorar"
AvatarPanelIgnoreCant = "OK"
AvatarPanelStopIgnoring = "Parar de Ignorar"
AvatarPanelReport = "Relatar"
#AvatarPanelCogDetail = "Dept: %s\nNível: %s\n"
AvatarPanelCogLevel = "Nível: %s"
AvatarPanelCogDetailClose = lClose
AvatarPanelDetail = "Detalhes do Toon"
AvatarPanelGroupInvite = "Convidar para Grupo"
AvatarPanelGroupRetract = "Retirar Convite"
AvatarPanelGroupMember = "Já no Grupo"
AvatarPanelGroupMemberKick = "Remova"

# grouping messages
groupInviteMessage = "%s quer que você entre em seu grupo"


# Report Panel
ReportPanelTitle = "Denunciar um Jogador"
ReportPanelBody = "Este recurso enviará uma denúncia completa a um Moderador. Em vez de denunciar, você pode optar pelo seguinte:\n\n  - Teleportar-se para outra região\n  - Usar \"Ignorar\" no painel do Toon\n\nQuer mesmo denunciar %s para um Moderador?" 
ReportPanelBodyFriends = "Este recurso enviará uma denúncia completa a um Moderador. Em vez de denunciar, você pode optar pelo seguinte:\n\n  - Teleportar-se para outra região\n  - Romper sua amizade\n\nQuer mesmo denunciar %s para um Moderador?\n\n(Isso também vai romper sua amizade)"
ReportPanelCategoryBody = "Você está prestes a denunciar %s. Um Moderador será alertado sobre sua reclamação e tomará medidas apropriadas contra quem estiver quebrando as regras. Escolha o motivo pelo qual está denunciando %s:"
ReportPanelBodyPlayer = "Este recurso ainda está sendo desenvolvido e será disponibilizado em breve. Enquanto isso, você pode fazer o seguinte:\n\n  - Vá até o DXD e termine a amizade por lá.\n – Conte aos pais ou responsáveis o que está acontecendo."

ReportPanelCategoryLanguage = "Linguagem Rude"
ReportPanelCategoryPii = "Compartilhar/Solicitar Informações Pessoais"
ReportPanelCategoryRude = "Comportamento Rude ou Mau"
ReportPanelCategoryName = "Nome Ruim"

ReportPanelConfirmations = (
    "Você está prestes a denunciar que %s usou linguagem obscena, intolerante, preconceituosa ou sexualmente explícita.",
    "Você está prestes a denunciar %s está promovendo insegurança ao divulgar ou solicitar um número de telefone, sobrenome, endereço de e-mail, senha ou nome de conta.",
    "Você está prestes a relatar que %s está importunando, atormentando ou usando de comportamento radical para atrapalhar o jogo.",
    "Você está prestes a relatar que %s criou um nome que não segue as regras da Disney.",
    )

# Put on confirmation screen!
ReportPanelWarning = "Levamos as denúncias muito a sério. Sua denúncia será vista por um Moderador, que tomará medidas contra qualquer um que quebrar nossas regras. Se for descoberto que sua conta também quebrou as regras, ou se você fizer denúncias falsas ou abusar do sistema 'Denunciar um Jogador', um Moderador pode tomar medidas contra sua conta. Tem certeza absoluta de que quer denunciar este jogador?"

ReportPanelThanks = "Obrigado! Sua denúncia foi enviada a um Moderador para análise. Não há necessidade de nos contatarmos novamente sobre o problema. A equipe de moderação tomará medidas adequadas contra um jogador que for descoberto quebrando as regras."

ReportPanelRemovedFriend = "Removemos automaticamente %s da sua Lista de Amigos."
ReportPanelRemovedPlayerFriend = "Removemos automaticamente %s como amigo Jogador, e você não o verá mais como seu amigo em nenhum produto Disney."

ReportPanelAlreadyReported = "Você já denunciou %s nesta sessão. Um Moderador vai analisar sua denúncia anterior."

# Report Panel
IgnorePanelTitle = "Ignorar um Jogador"
IgnorePanelAddIgnore = "Quer ignorar %s pelo restante da sessão?"
IgnorePanelIgnore = "Você agora está ignorando %s."
IgnorePanelRemoveIgnore = "Deseja parar de ignorar %s?"
IgnorePanelEndIgnore = "Você não está mais ignorando %s."
IgnorePanelAddFriendAvatar = "%s está entre seus amigos, você não pode ignorá-lo(la)enquanto forem amigos(as)."
IgnorePanelAddFriendPlayer = "%s (%s)está entre seus amigos, você não pode ignorá-lo(la) enquanto forem amigos(as)."

# PetAvatarPanel.py
PetPanelFeed = "Alimentar"
PetPanelCall = "Chamar"
PetPanelGoTo = "Ir para"
PetPanelOwner = "Mostrar dono"
PetPanelDetail = "Detalhes do bichinho"
PetPanelScratch = "Coçar"

# PetDetailPanel.py
PetDetailPanelTitle = "Adestramento"
# NOTE: these are replicated from OTPLocalizerEnglish sans "!"
PetTrickStrings = {
    0: 'Pular',
    1: 'Dar a pata',
    2: 'Fingir de morto',
    3: 'Rolar',
    4: 'Dar cambalhota',
    5: 'Dançar',
    6: 'Falar',
    }

# PetMood.py
PetMoodAdjectives = {
    'neutral': 'neutro',
    'hunger': 'faminto',
    'boredom': 'chateado',
    'excitement': 'animado',
    'sadness': 'triste',
    'restlessness': 'inquieto',
    'playfulness': 'brincalhão',
    'loneliness': 'solitário',
    'fatigue': 'cansado',
    'confusion': 'confuso',
    'anger': 'zangado',
    'surprise': 'surpreso',
    'affection': 'carinhoso',
    }

SpokenMoods = {
    'neutral': 'neutro',
    'hunger': 'Eu\estou cansado de Balinhas! Que tal me dar uma fatia de torta?',
    'boredom': 'Você não\ achou que eu entenderia, hein?', 
    'excitement': 'Toontástico!',
    'sadness': 'Eu quero ser rabisco de qualidade',
    'restlessness': 'Eu\estou tãooo inquieto',
    'playfulness': 'Brinque comigo ou eu\vou desenterrar algumas flores!',
    'loneliness': 'Quero lutar com os Cogs com você!',
    'fatigue': 'É muito cansativo fazer truques de rabisco! Que\tal dar um tempinho?',
    'confusion': 'Onde estou? Quem é mesmo você?',
    'anger': 'Você sempre me deixa para trás',
    'surprise': 'Opa, de onde você surgiu?',
    'affection': 'Você é um ótimo toon',
    }

# DistributedAvatar.py
DialogExclamation = "!"
DialogQuestion = '?'

# LocalAvatar.py
FriendsListLabel = "Amigos"

# TeleportPanel.py
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = "Tentando ir para %s."
TeleportPanelNotAvailable = "%s está ocupado(a) agora; tente novamente mais tarde."
TeleportPanelIgnored = "%s está ignorando você."
TeleportPanelNotOnline = "%s não está on-line neste momento."
TeleportPanelWentAway = "%s saiu."
TeleportPanelUnknownHood = "Você não sabe ir para %s!"
TeleportPanelUnavailableHood = "%s não está disponível agora; tente novamente mais tarde."
TeleportPanelDenySelf = "Você não pode ir lá por conta própria!"
TeleportPanelOtherShard = "%(avName)s está na região %(shardName)s, e você está na região %(myShardName)s. Deseja ir para %(shardName)s?"
TeleportPanelBusyShard = "%(avName)s está em uma Região lotada. Jogar em uma Região lotada pode afetar severamente o desempenho do jogo. Tem certeza de que quer mudar de região?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Sou o chefe."

# DistributedBattleFactory.py
FactoryBossTaunt = "Sou o Supervisor."
FactoryBossBattleTaunt = "Deixe-me te apresentar ao Supervisor."
MintBossTaunt = "Sou o Supervisor."
MintBossBattleTaunt = "Você precisa falar com o Supervisor."
StageBossTaunt = "A minha Justiça não é Cega"
StageBossBattleTaunt = "Eu estou acima da Lei"
CountryClubBossTaunt = "Sou o Presidente do Clube."
CountryClubBossBattleTaunt = "Você precisa falar com o Presidente do Clube."
ForcedLeaveCountryClubAckMsg = "O Presidente do Clube foi derrotado antes que você pudesse chegar a ele. Você não recuperou nenhuma Ação."

# HealJokes.py
ToonHealJokes = [
    ["O que faz TIQUE-TIQUE-TIQUE-AU?",
     "Um cãonômetro!"],
    ["Por que o louco toma banho com o chuveiro desligado?",
     "Porque ele comprou xampú para cabelos secos!"],
    ["Por que é difícil para o fantasma contar mentiras?",
     "Porque seus pensamentos são transparentes."],
    ["Do que a bailarina é chamada quando machuca o pé e se recusa a dançar?",
     "Pé-nóstica!"],
    ["O que a vaca foi fazer no espaço?",
     "Foi se encontrar com o vácuo!"],
    ["Por que o gato mia para a Lua e a Lua não mia para o gato?",
     "Porque astro-no-mia!"],
    ["Por que as tartarugas não ficam bêbadas?",
     "Porque elas só têm um casco!"],
    ["Por que o elefante usa tênis vermelhos?",
     "Porque os branquinhos sujam muito."],
    ["Por que a galinha atravessa a rua?",
     "Para chegar ao outro lado!"],
    ["Qual é a maior injustiça do Natal?",
     "O peru morre e a missa é do galo."],
    ["Qual é o cúmulo dos trabalhos manuais?",
     "Tricotar com a linha do trem."],
    ["O que é um vulcão?",
     "Uma montanha com soluço."],
    ["O que é um pontinho vermelho, um azul e um rosa em cima de uma árvore?",
     "Um morangotango com urublue num pinkenick."],
    ["Por que o elefante não consegue tirar carteira de motorista?",
     "Porque ele só dá trombada."],
    ["O que um tijolo disse para o outro?",
     "Existe um 'ciumento' entre nós."],
    ["O que a porta disse para a chave?",
     "Vamos dar uma voltinha."],
    ["O que o elétron fala quando atende ao telefone?",
     "Próton!"],
    ["Quem é o rei da horta?",
     "Rei Polho."],
    ["Por que as pilhas são melhores que os políticos?",
     "Porque elas têm, pelo menos, um lado positivo."],
    ["O que Benjamin Franklin disse quando inventou a eletricidade?",
     "Nada. Ele estava em estado de choque."],
    ["Por que o cachorro balança o rabo?",
     "Porque o rabo não tem força para balançar o cachorro."],
    ["Qual é o cúmulo da força?",
     "Dobrar a esquina."],
    ["O que não é de comer, mas dá água na boca?",
     "O copo."],
    ["Quem é a mãe do mingau?",
     "Mãe Zena."],
    ["O que o Batman disse para o Robin na hora em que entraram no carro?",
     "BAT a porta!"],
    ["O que é um pontinho amarelo tomando sol?",
     "É um fandango querendo virar baconzito."],
    ["O que é um pontinho rosa no armário?",
     "É um cupink."],
    ["Quem é o tio da construção?",
     "Tio Jolo."],
    ["O que dá um cruzamento de um dálmata com um canário?",
     "Uma onça pintada da Amazônia."],
    ["O que é uma porção de letras voando?",
     "Um bando de borboletras."],
    ["O que é que viaja o mundo inteiro, mas fica o tempo todo em um canto só?",
     "O selo."],
    ["O que é um pontinho verde em cima de um amarelo no canto da parede?",
     "Uma ervilha de castigo ajoelhada no milho."],
    ["Por que o namoro da goiabada com o queijo não deu certo?",
     "Porque o queijo era fresco."],
    ["O que é um pontinho azul no guarda-roupas?",
     "É uma bluesa."],
    ["O que é um pontinho verde no fundo da piscina?",
     "É uma ervilha... Segurando a respiração!"],
    ["O que é um pontinho vermelho e azul voando de um lado para o outro?",
     "Uma mosca fantasiada de Super-homem."],
    ["Qual é o animal que tem mais de três olhos e menos de quatro?",
     "O pi-olho, ou seja, 3,14."],
    ["O que a aranha faz quando vai para a aula de dança?",
     "Sapa-teia."],
    ["Por que o pato tem ciúmes do cavalo?",
     "Porque ele tem quatro patas."],
    ["Quando você tem certeza de que um ovo não tem um pintinho dentro?",
     "Quando o ovo é de pata."],
    ["Por que ninguém apareceu no enterro do elefante?",
     "Porque ninguém queria carregar o caixão."],
    ["O que é que sempre aumenta, mas nunca diminui?",
     "A idade."],
    ["O que é que tem muitos pés, mas não fica de pé?",
     "A centopéia."],
    ["Em que espécie de mato se senta o elefante quando chove?",
     "Mato molhado."],
    ["Quem é que bate em você, mas você não revida?",
     "O vento."],
    ["O que é o cúmulo do contra-senso?",
     "Na casa de saúde, só haver doentes."],
    ["Quando um jogador de futebol é um literato?",
     "Quando ele faz um gol de letra."],
    ["Onde é que a sereia Ariel vê filmes?",
     "No cinemaré."],
    ["O que é que atravessa a porta, mas nunca entra nem sai?",
     "A fechadura."],
    ["Por que os rios são considerados preguiçosos?",
     "Porque não saem dos seus leitos."],
    ["Qual é a diferença entre a galinha e o tecido?",
     "A galinha bota e o tecido desbota."],
    ["Era uma vez uma orquestra que não tocava nada. Qual o nome do filme?",
     "Os Intocáveis."],
    ["Quando é que um gaúcho é chamado de mineiro?",
     "Quando trabalha em uma mina."],
    ["O que deveríamos colocar embaixo da forca para que o condenado não morra?",
     "Cedilha!"],
    ["O que é que todos nós temos, mas quando precisamos vamos ao mercado comprar?",
     "Canela!"],
    ["O que você faz quando está nadando em um oceano e um crocodilo ataca?",
     "Você acorda."],
    ["Quem é que nasce no rio, vive no rio e morre no rio, mas só se molha se quiser?",
     "O carioca."],
    ["O que é que está no fim de tudo?",
     "A letra O."],
    ["Qual é o único monstro que é bonzinho?",
     "Good-zila."],
    ["O que é a única coisa que o vencedor da maratona perde?",
     "O fôlego."],
    ["O que acontece se você alimentar uma vaca com flores?",
     "Ela dará leite de rosas."],
    ["O que é que tem seis olhos, mas não pode ver?",
     "Três ratinhos cegos."],
    ["Afinal, o que é que sempre encontramos no final do túnel?",
     "A letra L."],
    ["Qual a palavra que tem duas letras e três sílabas?",
     "Arara!"],
    ["Por que os elefantes são encontrados na África?",
     "Porque eles são muito grandes para se esconderem."],
    ["Onde estavam todos os moradores da cidade durante o último apagão?",
     "No escuro."],
    ["Quando é que o cliente fica preso no banco?",
     "Quando fecha a conta-corrente."],
    ["Quem é que vai a todos os casamentos sem ser convidado?",
     "O padre."],
    ["Por que os dinossauros têm pescoços longos?",
     "Porque eles têm chulé."],
    ["Qual é a mulher que sempre aparece antes do nascer do sol?",
     "Aurora."],
    ["Por que os elefantes nunca esquecem?",
     "Porque ninguém nunca fala nada para eles."],
    ["Qual é o país que o criminoso não gosta de visitar?",
     "O Cana-dá."],
    ["Por que o leão é considerado o rei das selvas?",
     "Porque ele é macho; se fosse fêmea, seria rainha."],
    ["O que é um 'fuio'?",
     "É um 'buiaco na paiede'."],
    ["Sou enrolado, tenho a cabeça rachada e vivo apertado?",
     "Parafuso."],
    ["Por que o cachorro rói o osso?",
     "Porque ele não consegue engolir o osso inteiro."],
    ["Como é que você impede um elefante de passar pelo buraco de uma agulha?",
     "Dando um nó no rabo dele."],
    ["Em que lugar do mundo, o sono é mais profundo?",
     "No cemitério."],
    ["O que é que é menor que a boca de uma formiga?",
     "O que ela come."],
    ["Um é pouco, dois é bom, três é demais. O que são quatro e cinco?",
     "Nove."],
    ["Qual é a corrente que, por mais forte que seja, não consegue segurar o navio?",
     "A corrente marinha."],
    ["O que é que tem boca e um só dente e chama a atenção de muita gente?",
     "O sino."],
    ["Qual deve ser o comprimento máximo de uma perna?",
     "O suficiente para alcançar o chão."],
    ["O que é uma molécula?",
     "É uma 'Meninula Sapécula'."],
    ["Como se pode escrever a maior palavra do mundo?",
     "Com a caneta."],
    ["Que refeição é colocada sobre a água e não afunda?",
     "A bóia."],
    ["Qual o melhor castigo para um time de futebol que joga sujo?",
     "Levar um banho de gols."],
    ["Por que os elefantes usam tênis de corrida?",
     "Para fazer cooper, é claro."],
    ["Por que os elefantes são grandes e cinza?",
     "Porque, se eles fossem pequenos e amarelos, seriam canários."],
    ["O que é que tem na árvore, no futebol, no chapéu e na casa?",
     "Copa."],
    ["O que é que deixa um cachorro desconfiado?",
     "Uma pulga atrás da orelha."],
    ["Por que o "+ Donald +" espalhou açúcar no travesseiro?",
     "Porque ele queria ter doces sonhos."],
    ["Por que o "+ Goofy +" levou o pente dele ao dentista?",
     "Porque ele perdeu todos os dentes."],
    ["Por que o "+ Goofy +" usa a camisa no banho?",
     "Porque a etiqueta diz para lavar e usar."],
    ["Qual o país está na granja e a capital está no pomar?",
     "Peru, capital Lima."],
    ["Qual é o prato preferido da maioria das pessoas?",
     "O prato cheio."],
    ["Como você chama uma pessoa que leva outra para almoçar?",
     "Canibal."],
    ["O que é um ponto amarelo no canto da sala?",
     "É milho Santiago."],
    ["O que é um ponto preto dentro do tubo de ensaio?",
     "Uma blacktéria."],
    ["Por que o "+ Pluto +" dorme com uma casca de banana?",
     "Para pular da cama cedo."],
    ["Por que o rato usa tênis marrom?",
     "Porque o branco está lavando."],
    ["O que é que a dentadura tem em comum com as estrelas?",
     "Ela sai à noite."],
    ["O que é um pontinho preto no meio da estrada?",
     "É um calhamblack."],
    ["Por que o arqueólogo foi à falência?",
     "Porque sua carreira estava uma ruína."],
    ["Como é que você ficaria se atravessasse o Atlântico no Titanic?",
     "Ensopado."],
    ["O que é um pontinho amarelo no alto de um prédio?",
     "Um milho suicida."],
    ["Por que é que o milho suicida quer se suicidar?",
     "Porque o lugar onde ele mora é um bagaço."],
    ["O que é um pontinho vermelho lá embaixo do prédio onde está o milho suicida?",
     "Um milho bombeiro para salvar o milho suicida..."],
    ["Qual a cor mais barulhenta?",
     "A corneta."],
    ["O que é que a banana suicida falou?",
     "Macacos me mordam!!!"],
    ["Qual o tipo de alimento de que o político mais gosta?",
     "As massas."],
    ["O que a chaminé grande falou para a chaminé pequena?",
     "Você é muito jovem para fumar."],
    ["O que é um pontinho vermelho no pântano?",
     "É um jacared."],
    ["O que é um pontinho azul no gramado?",
     "Uma formiguinha de calça jeans."],
    ["O que é um ponto brilhante no gramado?",
     "Uma formiguinha de aparelho nos dentes."],
    ["O que é um pontinho marrom na pré-história?",
     "Um browntossauro."],
    ["Como se chama um dinossauro que nunca se atrasa?",
     "Prontossauro."],
    ["O que é um pontinho vermelho num pedacinho de neve?",
     "Uma miniatura da bandeira do Japão."],
    ["O que é um pontinho dourado no gramado?",
     "É uma formiguinha brincando de Jaspion."],
    ["Qual e a comida que liga e desliga ?",
     "O StrogON-OFF."],
    ["Por que o livro de matemática ficou triste?",
     "Porque ele tinha muitos problemas."],
    ["O que o tomate foi fazer no banco?",
     "Foi tirar extrato"],
    ["Como se faz para transformar um giz numa cobra?",
     "É só colocar o giz num copo de água. Aí o 'gizbóia'"],
    ["Qual é o cúmulo da rapidez?",
     "Fechar a gaveta, trancar e jogar a chave dentro."],
    ["Qual é o cúmulo do egoísmo?",
     "Não vou contar, só eu que sei."],
    ["Qual é o cúmulo da revolta?",
     "Morar sozinho, fugir de casa e deixar um bilhete dizendo que não volta mais."],
    ["Qual é o cúmulo do exagero?",
     "Passar manteiga no Pão de Açúcar."],
    ["Qual é o cúmulo do arrependimento do carrasco?",
     "Pois é, sempre que enforco alguém me dá um nó na garganta..."],
    ["Qual é o cúmulo da visão?",
     "Derrubar dez faixas-pretas com um golpe de vista."],
    ["Qual é o cúmulo da sorte?",
     "Ser atropelado por uma ambulância."],
    ["Qual é o cúmulo da maldade?",
     "Colocar tachinhas na cadeira elétrica."],
    ["Qual é o cúmulo da burrice?",
     "Ser reprovado no exame de fezes."],
    ["Qual é o cúmulo da economia?",
     "Usar o papel higiênico dos dois lados."],
    ["Qual é o cúmulo do esquecimento?",
     "Ih! Esqueci!"],
    ["Qual é o cúmulo da sede?",
     "Tomar um ônibus."],
    ["O que que faz ABC...Slurp...DEF...Slurp?",
     "Alguém tomando sopa de letrinhas."],
    ["O que é que é verde e fica saltando sem parar em cima do sofá?",
     "Uma ervilha que saiu do castigo."],
    ["O que é que o tomate foi fazer no banco?",
     "Tirar extrato."],
    ["Por que o médico que trabalha à noite se veste de verde?",
     "Porque ele está de plantão."],
    ["O que é que é branco com pontinhos pretos e vermelhos?",
     "Um dálmata com catapora."],
    ["O que a galinha foi fazer na igreja?",
     "Assistir à missa do galo."],
    ["O que é o que é? Cai em pé e corre deitado?",
     "Não é a chuva não! É uma minhoca de paraquedas."],
    ["Por que é que não é bom guardar o quibe no freezer?",
     "Porque lá dentro ele esfirra."],
    ["O que o advogado do frango foi fazer na delegacia?",
     "Foi soltar a franga"],
    ["Por que o galo canta de olhos fechados?",
     "Porque ele já sabe a música de cor."],
    ["Um peixe foi jogado de cima de um prédio de vinte andares. Que peixe era esse?",
     "Um atum, porque quando ele caiu fez: Aaaaaaaaaaaa Tum!"],
    ["Como se faz omelete de chocolate?",
     "Com ovos de Páscoa."],
    ["Para que servem óculos verdes?",
     "Para verde perto."],
    ["Para que servem óculos vermelhos?",
     "Para 'vermelhor'."],
    ["O que é verde por fora e amarela por dentro?",
     "Uma banana disfarçada de pepino."],
    ["Qual é a parte do carro que se originou no Antigo Egito?",
     "Os faraóis."],
    ["Como é que a bruxa sai na chuva?",
     "De rodo."],
    ["Por que o cachorro entrou na igreja?",
     "Porque ele é um cão pastor."],
    ["Quem é o pai do volante?",
     "O painel."],
    ["Como chamamos uma mulher que visitou uma plantação de uva?",
     "Viúva."],
    ["O que o amendoim falou para o elefante?",
     "Nada, o amendoim não fala."],
    ["O que os elefantes falam quando se esbarram?",
     "Mundo pequeno esse, né?"],
    ["O que o caixa falou para a registradora?",
     "Estou contando com você."],
    ["Por que o caminhão de frigorífico não sobe a ladeira?",
     "Porque 'elinguiça'."],
    ["Qual é a comida que liga e desliga?",
     "É o strogON-OFF."],
    ["O que a vaca foi fazer na Argentina?",
     "Foi ver o Boi nos Ares."],
    ["Qual é o peixe mais salgado que existe?",
     "O sal-mão."],
    ["O que é um cão indeciso?",
     "É um 'cão-fuso'."],
    ["Sabe por que o italiano não come churrasco?",
     "Porque o macarrão não cabe no espeto."],
    ["Qual é o cúmulo da rapidez?",
     "Ir ao enterro de um parente e ainda encontrá-lo vivo."],
    ["Qual é o cúmulo do azar?",
     "Ser atropelado por um carro funerário."],
    ["Por que o jacaré tomou o cartão de crédito do jacarezinho?",
     "Porque o jacarezinho gastou muito e mandou o jacarepaguá."],
    ["Qual é o cúmulo da burrice?",
     "Olhar pelo buraco da fechadura numa porta de vidro."],
    ["Qual é o cúmulo da confiança?",
     "Jogar par-ou-ímpar pelo telefone?"],
    ["Qual é o cúmulo da paciência?",
     "Esvaziar uma piscina com conta-gotas."],
    ["Qual é o cúmulo da traição?",
     "Suicidar-se com uma punhalada nas costas."],
    ["O que uma nuvem disse pra outra?",
     "'Nu-vem' não."],
    ["Qual é o cúmulo da moleza?",
     "Correr sozinho e chegar em segundo."],
    ["Por que o jacaré tirou o jacarezinho da escola?",
     "Porque ele 'reptil'."],
    ["Qual é o fim da picada?",
     "Quando o mosquito vai embora."],
    ["O que o paraquedas disse para o paraquedista?",
     "Tô contigo e não abro."],
    ["Qual é a cor mais barulhenta?",
     "A corneta."],
    ["O que é um pontinho amarelo no céu?",
     "Um yellowcóptero."],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("hmm","hehe","ah","Rá rá")
MovieHealLaughterHits1= ("Ah ah ah","Ri, ri, ri","Ré, ré","Ah, ah")
MovieHealLaughterHits2= ("AH HAH HAH!","HO HO HO!","RÁ RÁ RÁ!")

# MovieSOS.py
MovieSOSCallHelp = "%s SOCORRO!"
MovieSOSWhisperHelp = "%s precisa de ajuda na batalha!"
MovieSOSObserverHelp = "SOCORRO!"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "Oi %s! É uma satisfação ajudar você!"
MovieNPCSOSGoodbye = "Vejo você depois!"
MovieNPCSOSToonsHit = "Os Toons sempre acertam!"
MovieNPCSOSCogsMiss = "Os Cogs sempre erram!"
MovieNPCSOSRestockGags = "Reabastecendo com %s piadas!"
MovieNPCSOSHeal = "Curar"
MovieNPCSOSTrap = "Armadilha"
MovieNPCSOSLure = "Isca"
MovieNPCSOSSound = "Sonora"
MovieNPCSOSThrow = "Lançamento"
MovieNPCSOSSquirt = "Esguicho"
MovieNPCSOSDrop = "Cadente"
MovieNPCSOSAll = "Todos"

# MoviePetSOS.py
MoviePetSOSTrickFail = "Suspiro"
MoviePetSOSTrickSucceedBoy = "Bom garoto!"
MoviePetSOSTrickSucceedGirl = "Boa menina!"

# MovieSuitAttacks.py
MovieSuitCancelled = "CANCELADO\nCANCELADO\nCANCELADO"

# RewardPanel.py
RewardPanelToonTasks = "Tarefas Toon"
RewardPanelItems = "Itens recuperados"
RewardPanelMissedItems = "Itens não-recuperados"
RewardPanelQuestLabel = "Buscar %s"
RewardPanelCongratsStrings = ["É isso aí!", "Parabéns!", "Uau!",
                              "Legal!", "Caraca!", "Toontástico!"]
RewardPanelNewGag = "Nova piada %(gagName)s para %(avName)s!"
RewardPanelUberGag = "%(avName)s ganhou a piada %(gagName)s com %(exp)s pontos de experiência!"
RewardPanelEndTrack = "Oba! %(avName)s chegou ao fim da Trilha de Piadas da piada %(gagName)s!"
RewardPanelMeritsMaxed = "Maximizados"
RewardPanelMeritBarLabels = [ "Bilhetes azuis", "Intimações", "Granas Cog", "Méritos" ]
RewardPanelMeritAlert = "Pronto para a promoção!"

RewardPanelCogPart = "Você ganhou uma parte de disfarce de Cog!"
RewardPanelPromotion = "%s prepare-se para a promoção!"

# Cheesy effect descriptions: (short desc, sentence desc)
CheesyEffectDescriptions = [
    ("Toon normal", "você ficará normal"),
    ("Cabeção", "você ficará com uma cabeça grande"),
    ("Cabecinha", "você ficará com uma cabeça pequena"),
    ("Pernonas", "você ficará com pernas grandes"),
    ("Perninhas", "você ficará com pernas pequenas"),
    ("Toonzão", "você ficará um pouco maior"),
    ("Toonzinho", "você ficará um pouco menor"),
    ("Quadro reto", "você ficará em duas dimensões"),
    ("Perfil reto", "você ficará em duas dimensões"),
    ("Transparente", "você ficará transparente"),
    ("Sem cor", "você ficará sem cor"),
    ("Toon invisível", "você ficará invisível"),
    ]
CheesyEffectIndefinite = "Até que escolha outro efeito, %(effectName)s%(whileIn)s."
CheesyEffectMinutes = "Nos próximos %(time)s minutos, %(effectName)s%(whileIn)s."
CheesyEffectHours = "Nas próximas %(time)s horas, %(effectName)s%(whileIn)s."
CheesyEffectDays = "Nos próximos %(time)s dias, %(effectName)s%(whileIn)s."
CheesyEffectWhileYouAreIn = " enquanto estiver %s"
CheesyEffectExceptIn = ", exceto em %s"


# SuitBattleGlobals.py
SuitFlunky = "Puxa-saco"
SuitPencilPusher = "Rato de Escritório"
SuitYesman = "Vaquinha de Presépio"
SuitMicromanager = "Micro\4empresário"
SuitDownsizer = "Facão"
SuitHeadHunter = "Caça-\4talentos"
SuitCorporateRaider = "Aventureiro Corporativo"
SuitTheBigCheese = "O Rei da Cocada Preta"
SuitColdCaller = "Rei da Incerta"
SuitTelemarketer = "Operador de Tele\4marketing"
SuitNameDropper = "Dr. Sabe-com-\4quem-está-\4falando"
SuitGladHander = "Amigo da Onça"
SuitMoverShaker = "Agitador"
SuitTwoFace = "Duas Caras"
SuitTheMingler = "Amizade Fácil"
SuitMrHollywood = "Dr. Celebridade"
SuitShortChange = "Farsante"
SuitPennyPincher = "Mão de vaca"
SuitTightwad = "Pão-duro"
SuitBeanCounter = "Conta-\4moedinha"
SuitNumberCruncher = "Destruidor de Números"
SuitMoneyBags = "Sacos de Dinheiro"
SuitLoanShark = "Agiota"
SuitRobberBaron = "Barão Ladrão"
SuitBottomFeeder = "Comensal"
SuitBloodsucker = "Sanguessuga"
SuitDoubleTalker = "Duplo Sentido"
SuitAmbulanceChaser = "Perseguidor de Ambulâncias"
SuitBackStabber = "Golpe Sujo"
SuitSpinDoctor = "Relações Públicas"
SuitLegalEagle = "Macaco velho"
SuitBigWig = "Figurão"

# Singular versions (indefinite article)
SuitFlunkyS = "um Puxa-saco"
SuitPencilPusherS = "um Rato de Escritório"
SuitYesmanS = "uma Vaquinha de Presépio"
SuitMicromanagerS = "um Micro\4empresário"
SuitDownsizerS = "um Facão"
SuitHeadHunterS = "um Caça-talentos"
SuitCorporateRaiderS = "um Aventureiro Corporativo"
SuitTheBigCheeseS = "um Rei da Cocada Preta"
SuitColdCallerS = "um Rei da Incerta"
SuitTelemarketerS = "um Operador de Telemarketing"
SuitNameDropperS = "um Dr. Sabe-com-\4quem-está-\4falando"
SuitGladHanderS = "um Amigo da Onça"
SuitMoverShakerS = "um Agitador"
SuitTwoFaceS = "um Duas Caras"
SuitTheMinglerS = "um Amizade Fácil"
SuitMrHollywoodS = "um Dr. Celebridade"
SuitShortChangeS = "um Farsante"
SuitPennyPincherS = "um Mão de vaca"
SuitTightwadS = "um Pão-duro"
SuitBeanCounterS = "um Conta-\4moedinha"
SuitNumberCruncherS = "um Destruidor de Números"
SuitMoneyBagsS = "um Sacos de Dinheiro"
SuitLoanSharkS = "um Agiota"
SuitRobberBaronS = "um Barão Ladrão"
SuitBottomFeederS = "um Comensal"
SuitBloodsuckerS = "um Sanguessuga"
SuitDoubleTalkerS = "um Duplo Sentido"
SuitAmbulanceChaserS = "um Perseguidor de Ambulâncias"
SuitBackStabberS = "um Golpe Sujo"
SuitSpinDoctorS = "um Relações Públicas"
SuitLegalEagleS = "um Macaco velho"
SuitBigWigS = "um Figurão"

# Plural versions
SuitFlunkyP = "Puxa-sacos"
SuitPencilPusherP = "Ratos de Escritório"
SuitYesmanP = "Vaquinhas de Presépio"
SuitMicromanagerP = "Micro\4empresários"
SuitDownsizerP = "Facões"
SuitHeadHunterP = "Caça-\4talentos"
SuitCorporateRaiderP = "Aventureiros Corporativos"
SuitTheBigCheeseP = "Os Reis da Cocada Preta"
SuitColdCallerP = "Reis da Incerta"
SuitTelemarketerP = "Operadores de Tele\4marketing"
SuitNameDropperP = "Drs. Sabe-com-\4quem-está-\4falando"
SuitGladHanderP = "Amigos da Onça"
SuitMoverShakerP = "Agitadores"
SuitTwoFaceP = "Duas Caras"
SuitTheMinglerP = "Amizades Fáceis"
SuitMrHollywoodP = "Drs. Celebridade"
SuitShortChangeP = "Farsantes"
SuitPennyPincherP = "Mãos de vaca"
SuitTightwadP = "Pães-duros"
SuitBeanCounterP = "Conta-\4moedinhas"
SuitNumberCruncherP = "Destruidores de Números"
SuitMoneyBagsP = "Sacos de Dinheiro"
SuitLoanSharkP = "Agiotas"
SuitRobberBaronP = "Barões Ladrões"
SuitBottomFeederP = "Comensais"
SuitBloodsuckerP = "Sanguessugas"
SuitDoubleTalkerP = "Duplos Sentidos"
SuitAmbulanceChaserP = "Perseguidores de Ambulâncias"
SuitBackStabberP = "Golpes Sujos"
SuitSpinDoctorP = "Relações Públicas"
SuitLegalEagleP = "Macacos velhos"
SuitBigWigP = "Figurões"

SuitFaceOffDefaultTaunts = ['Buuuuu!']

SuitAttackDefaultTaunts = ['Pega essa!', 'Pode escrever!']

SuitAttackNames = {
  'Audit' : 'Auditoria!',
  'Bite' : 'Mordida!',
  'BounceCheck' : 'Cheque sem fundos!',
  'BrainStorm' : 'Grande ideia!',
  'BuzzWord' : 'Palavra-chave!',
  'Calculate' : 'Calcular!',
  'Canned' : 'Enlatado!',
  'Chomp' : 'Nhac!',
  'CigarSmoke' : 'Fumaça de charuto!',
  'ClipOnTie' : 'Prendedor de gravata!',
  'Crunch' : 'Triturar!',
  'Demotion' : 'Rebaixar!',
  'Downsize' : 'Reduzir!',
  'DoubleTalk' : 'Duplo sentido!',
  'EvictionNotice' : 'Aviso de despejo!',
  'EvilEye' : 'Mau-olhado!',
  'Filibuster' : 'Enchedor de linguiça!',
  'FillWithLead' : 'Pelotão de frente!',
  'FiveOClockShadow' : "Barba por fazer!",
  'FingerWag' : 'Dedo na cara!',
  'Fired' : 'Fogo!',
  'FloodTheMarket' : 'Invadir o mercado!',
  'FountainPen' : 'Caneta-tinteiro!',
  'FreezeAssets' : 'Bens congelados!',
  'Gavel' : 'Martelo!',
  'GlowerPower' : 'Olhar raivoso!',
  'GuiltTrip' : 'Sentimento de culpa!',
  'HalfWindsor' : 'Nó francês!',
  'HangUp' : 'Desligar!',
  'HeadShrink' : 'Analista!',
  'HotAir' : 'Ar quente!',
  'Jargon' : 'Jargão!',
  'Legalese' : 'Legalês!',
  'Liquidate' : 'Liquidar!',
  'MarketCrash' : 'Queda da Bolsa!',
  'MumboJumbo' : 'Bobeira!',
  'ParadigmShift' : 'Desvio de paradigma!',
  'PeckingOrder' : 'Hierarquia!',
  'PickPocket' : 'Pivete!',
  'PinkSlip' : 'Bilhete azul!',
  'PlayHardball' : 'Jogo duro!',
  'PoundKey' : 'Tecla de Jogo da velha!',
  'PowerTie' : 'Gravata!',
  'PowerTrip' : 'Viajou na autoridade!',
  'Quake' : 'Terremoto!',
  'RazzleDazzle' : 'Agito!',
  'RedTape' : 'Burrocracia!',
  'ReOrg' : 'ReOrg!',
  'RestrainingOrder' : 'Repressão!',
  'Rolodex' : 'Agenda telefônica!',
  'RubberStamp' : 'Carimbo!',
  'RubOut' : 'Apagar!',
  'Sacked' : 'Ensacado!',
  'SandTrap' : 'Trincheira!',
  'Schmooze' : 'Bajula!',
  'Shake' : 'Tremor!',
  'Shred' : 'Retalho!',
  'SongAndDance' : 'Conta prosa!',
  'Spin' : 'Giro!',
  'Synergy' : 'Sinergia!',
  'Tabulate' : 'Tabular!',
  'TeeOff' : 'Tacada!',
  'ThrowBook' : 'Livro de lançamentos!',
  'Tremor' : 'Tremor!',
  'Watercooler' : 'Bebedouro!',
  'Withdrawal' : 'Retirada!',
  'WriteOff' : 'Baixa!',
  }

SuitAttackTaunts = {
    'Audit': ["Seus livros não têm balanço.",
              "Parece que você está no vermelho.",
              "Deixe-me ajudá-lo com esses livros.",
              "Sua coluna de débitos é muito alta.",
              "Vamos verificar os seus bens.",
              "Assim, você vai ficar endividado.",
              "Vamos conferir direitinho o que você deve.",
              "Assim, a sua conta vai ficar zerada.",
              "É hora de você se responsabilizar pelas suas despesas.",
              "Encontrei um erro nos seus livros.",
              ],
    'Bite': ["Quer uma mordida?",
             "Dá uma mordida!",
             "A sua mordida é maior do que você pode mastigar.",
             "Minha mordida é maior do que o meu latido.",
             "Morde logo!",
             "Tome cuidado, eu mordo.",
             "Eu não mordo só quando estou encurralado.",
             "Só vou dar uma mordidinha.",
             "Não dei uma mordida o dia todo.",
             "Só quero uma mordida. É pedir muito?",
             ],
    'BounceCheck': ["Ah, que pena, você não tem graça.",
                    "Você tem uma dívida.",
                    "Acho que este cheque é seu.",
                    "Você me devia isso.",
                    "Estou cobrando esta dívida.",
                    "Este cheque não vai ser mole.",
                    "Você será cobrado por isso.",
                    "Feche a conta.",
                    "Isso terá um custo para você.",
                    "Queria trocar por dinheiro.",
                    "Vou mandar isso de volta para você.",
                    "Esta conta está salgada.",
                    "Estou descontando o serviço.",
                    ],
    'BrainStorm':["Acho que vai chover.",
                  "Espero que você esteja com o guarda-chuva.",
                  "Quero orientar você.",
                  "Que tal uma saraivada básica?",
                  "Cadê o seu brilho agora, Toon?",
                  "Pronto para a chuvarada?",
                  "Vou atacar você como um furacão.",
                  "Chamo isso de ataque-relâmpago.",
                  "Adoro ser um desmancha-prazeres.",
                  ],
    'BuzzWord':["Desculpe-me se estou te aborrecendo.",
                "Ouviu a última?",
                "Veja se você pega esta.",
                "Vamos cantarolar, Toon?",
                "Deixe-me defender você.",
                "Vou \"C\" perfeitamente claro.",
                "Você devia \"C\" mais cuidadoso.",
                "Veja se você consegue desviar desse enxame.",
                "Cuidado, você está prestes a ser picado.",
                "Parece que a sua urticária é séria.",
                ],
    'Calculate': ["Estes números fazem mesmo uma diferença!",
                  "Você contou com isso?",
                  "Faça as contas, você está caindo.",
                  "Deixe-me ajudar você a somar isso.",
                  "Você registrou todas as suas despesas?",
                  "De acordo com os meus cálculos, você não ficará por muito tempo aqui.",
                  "Aqui está o total.",
                  "Uau, a sua conta está se multiplicando.",
                  "Tente brincar com esses números!",
                  Cogs + ": 1 Toons: 0",
                  ],
    'Canned': ["Gosta fora da lata?",
               "\"Lata\" limpo?",
               "Fresquinho, saído da lata!",
               "Já foi atacado alguma vez por enlatados?",
               "Gostaria de doar a você este enlatado!",
               "Prepare-se para o \"Vira-lata\"!",
               "Você acha que pode abrir a lata, na lata.",
               "Vou te jogar na lata!",
               "Vou transformar você em um a-Toon em lata!",
               "Seu gosto não é tão bom fora da lata.",
               ],
    'Chomp': ["Olha só esses comilões!",
              "Nhac, nhac, nhac!",
              "Aqui tem algo para mastigar.",
              "Procurando alguma coisa para mastigar?",
              "Por que você não mastiga um pouco disto?",
              "Eu vou jantar você.",
              "Adoro comer Toons no café da manhã!",
              ],
    'ClipOnTie': ["Melhor se arrumar para a reunião.",
                  "Você não pode SAIR sem a gravata.",
                  "Os  "+ Cogs +" mais bem vestidos usam isto."
                  "Experimente este tamanho.",
                  "Você devia se vestir para arrasar.",
                  "Sem gravata não tem serviço...",
                  "Precisa de ajuda para se vestir?",
                  "Nada é tão poderoso quanto uma boa gravata.",
                  "Vamos ver se serve.",
                  "Esta vai apertar você.",
                  "Você vai querer se vestir antes de SAIR.",
                  "Acho que vou dar uma gravata em você.",
                  ],
    'Crunch': ["Parece que você está espremido contra a parede.",
               "Hora de mexer a mandíbula!",
               "Vou dar alguma coisa para você mascar!",
               "Triture isso!",
               "Mordida para viagem.",
               "Qual você prefere, molinho ou crocante?",
               "Espero que esteja preparado para a hora da mandíbula.",
               "Parece que você está ficando amassadinho!",
               "Vou amassar você como uma latinha."
               ],
    'Demotion': ["Você está descendo os degraus da empresa.",
                 "Vou mandar você de volta para a Expedição.",
                 "Está na hora de virar a sua placa de identificação.",
                 "Você está caidaço, palhaço.",
                 "Parece que você está ferrado.",
                 "Você não vai a lugar nenhum.",
                 "Você está em um beco sem saída.",
                 "Você não vai se mover tão cedo.",
                 "Você não vai a lugar nenhum.",
                 "Vai ficar registrado em seu arquivo permanente.",
                 ],
    'Downsize': ["Desce!",
                 "Sabe como descer?",
                 "Vamos entrar direto no assunto.",
                 "O que houve? Você parece deprimido.",
                 "Decaindo?",
                 "O que é que está caindo? Você!",
                 "Por que não tem alguém do meu tamanho?",
                 "Por que eu não meço você - ou será que é melhor dizer despeço?",
                 "Quer um tamanho menor por apenas mais uma moeda?",
                 "Experimente este tamanho!",
                 "Tem em um tamanho menor.",
                 "Este ataque é tamanho único!",
                 ],
    # Hmmm - where is double talker?
    'EvictionNotice': ["Mudança à vista.",
                       "Arrume as malas, Toon.",
                       "É hora de arrumar outro lugar para morar.",
                       "Considere-se servido.",
                       "O seu aluguel está atrasado.",
                       "Isto vai te torpedear.",
                       "Você está prestes a ser despejado.",
                       "Vou espirrar você daqui.",
                       "Você está deslocado.",
                       "Prepare-se para ser realocado.",
                       "Você está abrigado.",
                       ],
    'EvilEye': ["Estou botando um mau-olhado em você.",
                "Você fica de olho vivo nisso para mim?",
                "Espere. Tem alguma coisa no meu olho.",
                "Estou de olho em você!",
                "Você pode botar o olho nisso aqui para mim?",
                "Tenho um olho gordo danado.",
                "Você vai levar um soco no olho!",
                "Minha crueldade não está de molho, abre o olho!",
                "Vou colocar você no olho do furacão!",
                "Estou dando com os olhos em você.",
                ],
    'Filibuster':["Devo encher?",
                  "Isso vai demorar um pouco.",
                  "Poderia fazer isso o dia todo.",
                  "Não preciso nem respirar fundo.",
                  "Vou fazendo, fazendo, fazendo...",
                  "Nunca fica cansado de fazer isso.",
                  "Posso tagarelar sem parar.",
                  "Tem problema se eu puxar a sua orelha?",
                  "Acho que vou papear à vontade.",
                  "Sempre consigo dar o meu recado.",
                  ],
    'FingerWag': ["Já te disse milhares de vezes.",
                  "Olha aqui, Toon.",
                  "Não me faça rir.",
                  "Não me faça ir até aí.",
                  "Já cansei de repetir.",
                  "Fim de papo, eu já falei.",
                  "\Você não tem respeito por nós,  "+ Cogs +"."
                  "Acho que está na hora de você prestar atenção.",
                  "Blá, Blá, Blá, Blá, Blá.",
                  "Não me obrigue a interromper a reunião.",
                  "Será que eu vou ter que separar vocês?",
                  "Já passamos por isto antes.",
                  ],
    'Fired': ["É fogo! O jeito é fazer um churrasquinho.",
              "Vai esquentar por aqui.",
              "Assim, o frio passa.",
              "Espero que você tenha sangue frio.",
              "Quente, quentão e pelando.",
              "Melhor parar tudo, deitar no chão e rolar!",
              "Você está fora daqui.",
              "O que você acha de \"bem-feito\"?",
              "Pode dizer aí?",
              "Espero que tenha usado protetor solar.",
              "Está se sentindo um pouco tostado?",
              "Você vai arder em chamas.",
              "Você vai ficar aceso que nem fogueira.",
              "Você está frito.",
              "Eu sou fogo na roupa.",
              "Só aticei o fogo um pouquinho, né?",
              "Olha, um churrasquinho crocante.",
              "Você não devia sair por aí malpassado.",
              ],
    'FountainPen': ["Vai deixar mancha.",
                    "Vamos assinar embaixo.",
                    "Esteja preparado para alguns danos irreparáveis.",
                    "Você vai precisar de um bom tintureiro.",
                    "Você devia mudar.",
                    "Esta caneta-tinteiro tem uma tinta legal.",
                    "Aqui, vou usar a minha caneta.",
                    "Você entende a minha letra?",
                    "Isso é que é carregar nas tintas.",
                    "Seu desempenho babou.",
                    "Não é chato quando isso acontece?",
                    ],
    'FreezeAssets': ["Seus bens são meus.",
                     "Está sentindo um vento? É o cheque voador.",
                     "Espero que não tenha planos.",
                     "Isso vai manter você na geladeira.",
                     "Tem uma brisa fria no ar.",
                     "O inverno está chegando mais cedo neste ano.",
                     "Você está sentido um calafrio?",
                     "Vou cristalizar o meu plano.",
                     "Você vai ver, no duro.",
                     "O gelo queima.",
                     "Espero que goste de frios.",
                     "Tenho muito sangue frio.",
                     ],
    'GlowerPower': ["Está olhando para mim?",
                    "Disseram que tenho olhos muito penetrantes.",
                    "Gosto de estar no fio da navalha.",
                    "Caçamba, caramba, meus quatro-olhos não são bambas?",
                    "Estou de olho em você, pirralho.",
                    "Que tal estes olhos expressivos?",
                    "Meus olhos são o meu forte.",
                    "Enche os olhos.",
                    "Estou de olho, piolho.",
                    "Olhe nos meus olhos...",
                    "Podemos dar uma espiada no seu futuro?",
                    ],
    'GuiltTrip': ["Você vai ficar com um baita sentimento de culpa!",
                  "Está se sentindo culpado?",
                  "É tudo culpa sua!",
                  "Sempre ponho a culpa de tudo em você.",
                  "Afogue-se na própria culpa!",
                  "Nunca mais falo contigo!",
                  "É melhor pedir desculpas.",
                  "Só vou perdoar você daqui a um milhão de anos!",
                  "Está preparado para viajar na maionese da culpa?",
                  "Ligue para mim quando voltar de viagem.",
                  "Quando você volta de viagem?",
                  ],
    'HalfWindsor': ["Esta é a gravata mais elegante que você já viu!",
                    "Procure não apertar tanto.",
                    "Você não viu nem metade do nó em que você se meteu.",
                    "Você tem sorte de eu não saber francês.",
                    "Esta gravata é demais para você.",
                    "Aposto como você nunca VIU um nó francês!",
                    "Esta gravata não é para o seu bico.",
                    "Eu não deveria ter gasto esta gravata com você.",
                    "Você não vale nem o nó desta gravata!",
                  ],
    'HangUp': ["Você foi desconectado.",
               "Tchau!",
               "Está na hora de terminar a sua conexão.",
               "...e não ligue de novo!",
               "Clique!",
               "A conversa acabou.",
               "Estou cortando este fio.",
               "Acho que você está meio desligado.",
               "Parece que você está com mau contato.",
               "Seu tempo acabou.",
               "Espero que tenha ouvido em claro e bom som.",
               "Foi engano.",
               ],
    'HeadShrink': ["Parece que você tem ido ao analista.",
                   "Querida, encolhi o analista.",
                   "Espero que não precise analisar o seu amor-próprio.",
                   "Você se abriu?",
                   "Analiso, logo existo.",
                   "Não é nada que faça você perder a cabeça.",
                   "Você vai abrir a cabeça?",
                   "Levanta essa cabeça! Ou será que é melhor abaixar?",
                   "Os objetos podem ser maiores do que parecem.",
                   "Os melhores Toons vêm nos menores frascos.",
                   ],
    'HotAir':["Estamos tendo uma discussão acalorada.",
              "Está rolando uma onda de calor.",
              "Atingi o meu ponto de ebulição.",
              "Que vento cortante.",
              "Odeio ter que te grelhar, mas...",
              "Lembre-se sempre: onde há fumaça, há fogo.",
              "Você parece meio queimadinho.",
              "Outra reunião que virou fumaça.",
              "Acho que está na hora de botar lenha na fogueira.",
              "Deixe-me acender uma relação de trabalho.",
              "Tenho umas observações inflamadas pra você.",
              "Ataque aéreo!!!",
              ],
    'Jargon':["Que besteira.",
              "Veja se você consegue ver algum sentido nisso.",
              "Espero que tenha sido claro como água.",
              "Parece que vou ter que falar mais alto.",
              "Insisto em ter a palavra.",
              "Sou muito direto.",
              "Devo sustentar a minha opinião neste assunto.",
              "Olha, as palavras podem machucar você.",
              "Entendeu o que eu quis dizer?",
              "Palavras, palavras, palavras, palavras, palavras.",
              ],
    'Legalese':["Você deve se conformar e desistir.",
                "Você vai ser derrotado, legalmente falando.",
                "Você está ciente das implicações legais?",
                "Você não está acima da lei!",
                "Devia haver uma lei contra você.",
                "Não há lei marcial comigo!",
                "As opiniões expressadas neste ataque não são compartilhadas pela Toontown On-line da Disney.",
                "Não podemos ser responsabilizados por danos sofridos neste ataque.",
                "Os resultados deste ataque podem variar.",
                "Este ataque não tem validade legal quando proibido.",
                "Você não se enquadra no meu sistema legal!",
                "Você não sabe lidar com assuntos jurídicos.",
                ],
    'Liquidate':["Gosto de manter as coisas fluindo.",
                 "Você está com algum problema de fluxo de caixa?",
                 "Vou ter que lavar os seus bens.",
                 "É hora de você ser levado pelo fluxo.",
                 "Não se esqueça de que fica escorregadio quando está molhado.",
                 "Os números estão correndo.",
                 "Você escorrega que nem sabão.",
                 "Está caindo tudo em cima de você.",
                 "Acho que você vai por ralo abaixo.",
                 "Você tomou uma lavada.",
                 ],
    'MarketCrash':["Vou acabar com a sua festa.",
                   "Você não vai sobreviver à queda.",
                   "Sou mais do que o mercado pode aguentar.",
                   "Tenho uma queda por você!",
                   "Agora eu vou entrar detonando.",
                   "Sou um verdadeiro dragão no mercado.",
                   "Parece que o mercado está em baixa.",
                   "É melhor você sair fora rapidamente!",
                   "Vender! Vender! Vender!",
                   "Devo liderar a recessão?",
                   "Todo mundo está saindo fora, você não vai?",
                   ],
    'MumboJumbo':["Deixe-me explicar melhor.",
                  "É muito simples.",
                  "Vamos fazer desta maneira.",
                  "Deixe-me ampliar para você.",
                  "Você pode chamar isso de baboseira tecnológica.",
                  "Aqui estão meus eufemismos.",
                  "Caramba, isso é que é encher a boca.",
                  "Algumas pessoas me chamam de exagerado.",
                  "Posso me meter?",
                  "Acho que estas são as palavras certas.",
                   ],
    'ParadigmShift':["Cuidado! Eu saio pela tangente.",
                     "Prepare-se para mudar radicalmente!"
                     "Não é uma mudança interessante?"
                     "Você vai ter que desviar de caminho.",
                     "Agora é sua vez de desviar.",
                     "Acabou o desvio!",
                     "Você nunca trabalhou tanto neste desvio.",
                     "Estou transviando você!",
                     "Olhe para o meu rabo de olho!",
                     ],
    'PeckingOrder':["Este aqui é para quem berra mais.",
                    "Prepare-se para o grito de guerra.",
                    "Por falta de um grito, morre um burro no atoleiro.",
                    "Vou ganhar no grito.",
                    "Você está no último grito da hierarquia.",
                    "Se gritos resolvessem, porcos não morreriam!",
                    "A ordem está valendo, no grito!",
                    "Por que não grito com alguém do meu tamanho? Ah!",
                    "Cão que ladra não morde.",
                    ],
    'PickPocket': ["Deixe-me verificar os seus pertences.",
                   "E aí, qual é o pó?",
                   "É mais fácil do que tirar doce de criança.",
                   "Golpe de mestre.",
                   "Deixa que eu seguro para você.",
                   "Não tire os olhos de minhas mãos.",
                   "As mãos são mais rápidas que os olhos.",
                   "Não tenho nada para tirar da manga.",
                   "A gerência não se responsabiliza por extravio de itens.",
                   "Achado não é roubado.",
                   "Você nem vai sentir.",
                   "Dois pra mim, um pra você.",
                   "Está bom assim.",
                   "Você não vai precisar mesmo...",
                   ],
    'PinkSlip': ["Tente imaginar que está tudo azul.",
                 "Tá com medo? Você está azul!",
                 "Com certeza, este bilhete vai fazer você ficar azul.",
                 "Êpa, acho que mudei de cor, né?",
                 "Olha lá, você não quer ficar azul, ou quer?",
                 "Este bilhete não é branco, é azul.",
                 "Estou azul de fome!",
                 "Você se importa que eu passe aí para ver se está tudo azul?",
                 "O azul não é exatamente a sua cor.",
                 "Toma seu bilhete azul e fora daqui!",
                 ],
    'PlayHardball': ["Então você quer jogar bola comigo?",
                     "Você não quer jogar bola comigo.",
                     "Chuta forte!",
                     "Passa, cara, passa!",
                     "Aí está o passe...",
                     "Você vai precisar de um refresco do goleiro.",
                     "Vou jogar você para fora do campo.",
                     "Depois que você se contundir, vai direto para casa.",
                     "São 45 minutos do segundo tempo!",
                     "Você não consegue jogar comigo!",
                     "Vou atingir você.",
                     "Vou dar um chute com efeito na bola!",
                    ],
    'PoundKey': ["É hora de retornar algumas ligações.",
                 "Gostaria de fazer uma ligação a cobrar.",
                 "Trrriiimmm - é para você!",
                 "Você quer brincar com o Jogo da Velha?",
                 "Tenho um método incrível para ganhar.",
                 "Está se sentindo nocauteado?",
                 "Vou dar um golpe neste número.",
                 "Deixe-me ligar para fazer uma surpresinha.",
                 "Vou ligar para você.",
                 "O.K. Toon, é o fim para você.",
                 ],
    'PowerTie': ["Eu ligo mais tarde, você parece enrolado na gravata.",
                 "Você está pronto para uma gravata?",
                 "Senhoras e senhores, esta é a gravata!",
                 "É melhor aprender a dar este nó.",
                 "Vou manter a sua língua dentro do nó!",
                 "É a gravata mais horrível que você já comprou!",
                 "Está sentindo o aperto?",
                 "Minha gravata é muito mais poderosa que a sua!",
                 "Eu tenho o poder do nó!",
                 "Pelos poderes do nó, vou engravatar você.",
                 ],
    'PowerTrip': ["Faça as malas, vamos fazer uma pequena viagem.",
                  "Você fez uma boa viagem?",
                  "Boa viagem, acho que nos veremos na próxima temporada.",
                  "Como foi a viagem?",
                  "Desculpe ter \"viajado\" dessa maneira!",
                  "Você parece viajandão.",
                  "Agora, você sabe quem é a autoridade!",
                  "Tenho muito mais autoridade do que você.",
                  "Quem manda agora?",
                  "Você não pode lutar contra o poder.",
                  "O poder corrompe, principalmente em minhas mãos!",
                  ],
    'Quake': ["Vamos balançar, agitar e rolar.",
              "Tem muita vibração por aqui!",
              "As suas canelas estão tremendo.",
              "Aí vem ele, este é grande!",
              "Este está fora da escala Richter.",
              "Agora é que a terra vai tremer!",
              "E aí, quem é que está agitando? Você!",
              "Já esteve em um terremoto?",
              "Agora, você está em território de tremores!",
              ],
    'RazzleDazzle': ["Leia os meus lábios.",
                     "Que acha da minha dentadura?",
                     "Não acha que tenho charme?",
                     "Vou impressionar você.",
                     "Meu dentista faz um excelente trabalho.",
                     "Cegadores, não acha?",
                     "Não dá nem para acreditar que não é de verdade.",
                     "Chocante, né?",
                     "Vou dar um fim nisso.",
                     "Passo o fio dental após cada refeição.",
                     "Sorria!",
                     ],
    'RedTape': ["Isto deve acalmar o bicho.",
                "Vou te amarrar por um tempo.",
                "Você está acorrentado.",
                "Veja se consegue cortar caminho por aqui.",
                "O bicho vai pegar.",
                "Tomara que você tenha claustrofobia.",
                "Vou me certificar de que você não vai escapulir.",
                "Vou ocupar você com alguma coisa.",
                "Tente desatar o nó.",
                "Espero que você concorde com os tópicos da reunião.",
                ],
'ReOrg': ["Você não gostou da maneira como eu reorganizei as coisas!",
              "Talvez um pouco de organização seja bom.",
              "Você não é tão ruim assim, só precisa se organizar.",
              "Você gosta do meu tino para organização?",
              "Só pensei em dar um novo visual às coisas.",
              "Você precisa se organizar!",
              "Você parece um pouco desorganizado.",
              "Espera um pouco enquanto eu reorganizo os seus pensamentos.",
              "Só vou esperar até que você se organize um pouco mais.",
              "Você se importa se eu só der uma reorganizadinha?",
              ],
    'RestrainingOrder': ["Você precisa levar broncas de vez em quando.",
                         "Estou te jogando na cara uma ordem repressora!",
                         "Você não pode chegar nem um metro e meio perto de mim.",
                         "Talvez seja melhor você manter distância.",
                         "Entre na linha.",
                         Cogs + "! Reprimam este Toon!",
                         "Tente entrar na linha sozinho.",
                         "Espero que eu esteja sendo bem repressor com você.",
                         "Veja se você consegue acabar com essa repressão!",
                         "Estou ordenando que você se reprima!",
                         "Por que não começamos com uma repressão básica?"
                         ],
    'Rolodex': ["O seu cartão está aqui, em algum lugar.",
                "Aqui está o número do dedetizador.",
                "Quero dar o meu cartão a você.",
                "Tenho o seu número bem aqui.",
                "Tenho tudo aqui sobre você, de A a Z.",
                "Você vai se virar com isso.",
                "Dê um giro pelas páginas.",
                "Cuidado com a papelada solta.",
                "Vou apontar o dedo para a letra que desejo.",
                "É assim que eu consigo entrar em contato com você?",
                "Quero ter certeza de que manteremos o contato.",
                ],
    'RubberStamp': ["Eu sempre causo uma boa impressão.",
                    "É importante aplicar uma pressão firme e bem distribuída.",
                    "Impressos perfeitos todas as vezes.",
                    "Quero carimbar você.",
                    "Você precisa ser DEVOLVIDO AO REMETENTE.",
                    "Você foi CANCELADO.",
                    "Você possui uma entrega de PRIORIDADE.",
                    "Vou me certificar de que a minha mensagem foi RECEBIDA.",
                    "Você não vai a lugar nenhum - você tem uma TARIFA POSTAL A PAGAR.",
                    "Preciso de uma resposta IMEDIATA.",
                    ],
    'RubOut': ["E agora, desapareceu!",
               "Sinto que perdi você em algum lugar.",
               "Decidi deixar você de fora.",
               "Eu sempre apago todos os obstáculos.",
               "Vou só apagar este erro.",
               "Posso fazer qualquer perturbação desaparecer.",
               "Gosto das coisas organizadas e limpas.",
               "Tente manter a animação.",
               "Estou vendo você... Agora, não vejo você.",
               "Vai ficar meio esmaecido.",
               "Vou eliminar o problema.",
               "Deixe-me cuidar das suas áreas problemáticas.",
               ],
    'Sacked':["Parece que você foi embrulhado.",
              "Está no saco.",
              "Você foi embolsado.",
              "Papel ou plástico?",
              "Meus inimigos serão ensacados!",
              "Eu tenho o recorde de Toontown de sacos por jogo.",
              "Você não é mais bem-vindo por aqui.",
              "O seu tempo acabou aqui, você vai ser ensacado!",
              "Deixe-me ensacar isto para você.",
              "Nenhuma defesa se iguala ao meu ataque com sacos!",
              ],
    'Schmooze':["Você nunca vai ver quando chega.",
                "Vai ficar legal em você.",
                "Você conseguiu.",
                "Não quero despejar nada em você.",
                "Como puxa-saco, eu vou longe.",
                "Agora, eu vou florear bastante.",
                "É hora de carregar nas tintas.",
                "Vou ressaltar o seu lado bom.",
                "Isso merece um bom tapinha nas costas.",
                "Vou falar bem de você para todo mundo.",
                "Detesto tirá-lo do seu pedestal, mas...",
                ],
    'Shake': ["Você está bem no epicentro.",
              "Você está em cima da falha.",
              "Vai ser um sacolejo só.",
              "Acho que isso é um desastre natural.",
              "É um desastre de proporções sísmicas.",
              "Este está fora da escala Richter.",
              "É hora de entrar na toca.",
              "Você parece perturbado.",
              "Preparado para os solavancos?",
              "Você vai sacolejar, e não centrifugar.",
              "Isso vai agitar você.",
              "Sugiro um bom plano de fuga.",
              ],
    'Shred': ["Preciso me livrar de alguns fragmentos perigosos.",
              "As porções produzidas estão aumentando de quantidade.",
              "Acho que vou dispor de você agora mesmo.",
              "Assim, a prova é eliminada.",
              "Não há como provar isso agora.",
              "Veja se você consegue juntar os pedaços novamente.",
              "Assim, você vai cortar as sobras e ficar do tamanho certo.",
              "Vou retalhar esta ideia todinha.",
              "Não queremos que isto caia nas mãos erradas.",
              "Fácil se tem, fácil se perde.",
              "Não é o seu último fio de esperança?",
              ],
    'Spin': ["O que me diz de sairmos para um giro?",
             "Você usa a centrifugação?",
             "Isto vai fazer a sua cabeça girar de verdade!",
             "Este é o meu giro das coisas.",
             "Vou levar você para uma volta.",
             "Como é que você dá a \"volta\" no seu tempo?",
             "Olha só: você não quer girar até ficar tonto?",
             "Nossa, você está no meio de um furacão!",
             "Meus ataques vão fazer sua cabeça rodar!",
             ],
    'Synergy': ["Vou encaminhar ao comitê.",
                "O seu projeto foi cancelado.",
                "O seu centro de custos será cortado.",
                "Estamos reestruturando o seu setor.",
                "Colocamos em votação, e você perdeu.",
                "Acabei de receber a aprovação final.",
                "Uma boa equipe pode se livrar de qualquer problema.",
                "Já dou um retorno a você sobre isso.",
                "Vamos direto ao que interessa.",
                "Vamos encarar isto como uma crise de sinergia.",
                ],
    'Tabulate': ["Isto não soma em nada.",
                 "Pela minha conta, você perdeu.",
                 "Você está fazendo um bom cálculo.",
                 "Vou fazer o seu total em um minuto.",
                 "Está preparado para estes números?",
                 "Sua conta já está vencida e pode ser paga.",
                 "É hora de calcular.",
                 "Gosto de colocar as coisas em ordem.",
                 "E a contagem é...",
                 "Estes números devem ser muito poderosos.",
                 ],
    'TeeOff': ["Você não vai bem de condições.",
               "Olha a frente!",
               "Confio no meu taco.",
               "Gandula, preciso do meu taco!",
               "Tente evitar este risco.",
               "Dê impulso!",
               "É mesmo um furo dentro do outro.",
               "Você está no meu campo.",
               "Repara só a precisão.",
               "Cuidado com o passarinho!",
               "Fique de olho na bola!",
               "Você se importa se eu continuar a jogar?",
               ],
    'Tremor': ["Você sentiu?",
               "Você não tem medo de um tremorzinho de nada, ou tem?",
               "O tremor é apenas o começo.",
               "Você parece tenso.",
               "Vou agitar as coisas um pouco!",
               "Tudo preparado para retumbar?",
               "O que houve? Você parece balançado.",
               "Tremedeira de medo!",
               "Por que está tremendo de medo?",
               ],
    'Watercooler': ["Certamente, isto vai refrescar você.",
                    "Não é refrescante?",
                    "Faço a entrega.",
                    "Direto da fonte - até a sua boca.",
                    "Qual é o problema, é só uma água de nascente.",
                    "Não se preocupe, é pura.",
                    "Ah, outro cliente satisfeito.",
                    "É hora da entrega diária.",
                    "Espero que as suas cores não desbotem.",
                    "Quer beber?",
                    "Sai tudo na lavagem.",
                    "A bebida é com você.",
                    ],
    'Withdrawal': ["Acho que você está no vermelho.",
                   "Espero que o seu saldo seja o suficiente para cobrir isto.",
                   "Olha que vou cobrar juros.",
                   "O seu saldo está diminuindo.",
                   "Em breve, você vai precisar fazer um depósito.",
                   "Você sofreu um colapso financeiro.",
                   "Acho que você está em baixa.",
                   "Suas finanças decaíram.",
                   "Prevejo um período de vacas magras.",
                   "É uma inversão de valores.",
                   ],
    'WriteOff': ["Deixe-me aumentar as suas perdas.",
                 "Vamos tirar o melhor proveito possível de um mau negócio.",
                 "É hora de fazer o balanço dos caixas.",
                 "Isso não vai ficar bom nos livros-caixa.",
                 "Procuro alguns dividendos.",
                 "Você deve se responsabilizar por suas perdas.",
                 "Pode esquecer o bônus.",
                 "Vou bagunçar todas as suas contas.",
                 "Você está prestes a sofrer algumas perdas.",
                 "Isto vai afetar os seus resultados finais.",
                 ],
    }

# DistributedBuilding.py
BuildingWaitingForVictors = "Aguardando outros jogadores...",

# Elevator.py
ElevatorHopOff = "Descer"
ElevatorStayOff = "Se descer, terá de esperar\naté que o elevador parta ou fique vazio"
ElevatorLeaderOff = "Somente seu líder pode decidir quando deve descer."
ElevatorHoppedOff = "Você precisa esperar o próximo elevador"
ElevatorMinLaff = "Você precisa de %s pontos de risada para poder subir neste elevador"
ElevatorHopOK = "OK"
ElevatorGroupMember = "Somente o líder deste grupo pode\ndecidir quando deve entrar"

# DistributedCogKart.py
KartMinLaff = "Você precisa de %s pontos de risada para poder andar neste carte."

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = ", Ltda."
CogsIncModifier = "%s" + CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Toc, toc."
DoorWhosThere = "Quem é?"
DoorWhoAppendix = " Quem?"
DoorNametag = "Porta"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "Você precisa de piadas! Vá falar com o Tutorial Tom!"
FADoorCodes_DEFEAT_FLUNKY_HQ = "Volte aqui quando tiver derrotado o Puxa-saco!"
FADoorCodes_TALK_TO_HQ = "Vá pegar a sua recompensa com o Haroldo do Quartel!"
FADoorCodes_WRONG_DOOR_HQ = "Porta errada! Vá pela outra porta para o pátio!"
FADoorCodes_GO_TO_PLAYGROUND = "Direção errada! Você precisa ir para o pátio!"
FADoorCodes_DEFEAT_FLUNKY_TOM = "Ande até o Puxa-saco para lutar com ele!"
FADoorCodes_TALK_TO_HQ_TOM = "Vá pegar a sua recompensa no Quartel dos Toons!"
FADoorCodes_SUIT_APPROACHING = None  # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "Cuidado! Tem um COG lá dentro!"
FADoorCodes_SB_DISGUISE_INCOMPLETE = "Você vai ser pego se entrar lá como um Toon! Você precisa completar o seu Disfarce de Cog primeiro!\n\nMonte o seu Disfarce de Cog com pedaços da Fábrica."
FADoorCodes_CB_DISGUISE_INCOMPLETE = "Você vai ser pego se entrar lá como um Toon! Você precisa completar o seu Disfarce de Robô Mercenário primeiro!\n\nMonte o seu Disfarce de Robô Mercenário executando Tarefas Toon na Sonholândia."
FADoorCodes_LB_DISGUISE_INCOMPLETE = "Você vai ser pego se entrar lá como um Toon! Você precisa completar o seu Disfarce de Cog primeiro!\n\nMonte o seu Disfarce de Cog com pedaços da Fábrica."
FADoorCodes_BB_DISGUISE_INCOMPLETE = "Você vai ser pego se entrar lá como Toon! Primeiramente, você precisa concluir seu Disfarce de Robô Chefe!\n\nConstrua seu Disfarce de Robô Chefe cumprindo as TarefasToon depois da Sonholândia do Donald."

# KnockKnock joke contest winners
KnockKnockContestJokes = {
    2100 : ["Jaque",
            "Jaque não está olhando, joga uma torta nele!"],

    # 2009 April fools contest Jokes. First few doors of Loopy lane
    2200 : {28:["Biscuit (Biscoito)",
            "Biscuitos (Biscoitos) me mordam, os Cogs vêm aí!"],
            41:["Dewey",
            "Dewemos ir detonar mais alguns Cogs?"],
            40:["Minnie",
            "Minnie-pessoas falaram comigo, e isso está me enlouquecendo!"], 
##            25:["Biscuit25 (Biscoito25)",
##            "Biscuitos (Biscoitos) me mordam, os Cogs vêm aí!"],
            27:["Disguise",
            "A Disguisetante perseguição aos Cogs!"]}, 

    2300: ["Justa",
           "Justa gora peguei uns dois pedaços de Cogs, pronto!"],

    # Polar Place has multiple jokes so they are in a dict keyed of the propId of the door
    3300: { 10: ["Aladdin",
                   "Aladdinheiro no chão."],
            6 : ["Adon",
                 "Adondé que esses Cogs tão saindo?"],
            30 : ["Bacon",
                  "Bacon uma torta ia bem."],
            28: ["Isaías",
                 "Isaías mas voltou-se."],
            12: ["Julieta",
                 "Julieta me chamando praquele prédio Cog com você pra eu te Toonar."],
            },
     }

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Quem",
    "Aqui tem eco, não?"],

    ["Kika",
    "Kikalor!"],

    ["Joe",
    "Você é Joetromundo?"],

    ["Eudin",
    "Eudinovo por aqui!"],

    ["Silêncio",
    "Pssss!"],

    ["Simbó",
    "Simbora pra praia."],

    ["Takent",
    "Takent ou frio?"],

    ["Noá",
    "Noá de quê."],

    ["Não sei",
    "Nem eu, já te falei."],

    ["Otudo",
    "Otudo ou nada?"],

    ["Totan",
    "Totan feliz que você está aqui!"],

    ["Osmar",
    "Osmartodontes não existem mais!"],

    ["Silem",
    "Silembra de mim?"],

    ["Ostra",
    "Ostra vez?"],

    ["Aimée",
    "Aimée Tida?"],

    ["Zoom",
    "Zooma imediatamente daqui!"],

    ["Aiki",
    "Aiki medo!"],

    ["Quiba",
    "Quibagunça é essa"],

    ["Tasó",
    "Não, tacompanhado."],

    ["Iago",
    "Iagora, José?"],

    ["'Tácom'",
    "'Tácom' tudo, não é?"],

    ["Tádi",
    "Tádi graça, é? Meu nome é  "+Flippy+"."],

    ["Opato",
    "Opato "+Donald+" Deduct."],

     ["Masqui",
    "Masqui coisa, abre a porta logo."],

    ["Nénim.",
    "Nénim guém que te interesse, deixa eu entrar."],

    ["Omos",
    "Omosquito que te picou."],

    ["Colés",
    "Colesterol faz mal, sai fora."],

    ["Breno",
    "Breno que eu te falei que esse cara vinha."],

    ["Kiko",
    "Kiko-losso!"],

    ["Vaivê",
    "Vaivê que eu tô atrasado."],

    ["Quente",
    "Quente viu e quem te vê!"],

    ["Vopri",
    "Vopri-meiro, tô com medo."],

    ["Eunum",
    "Eunum sei. Desculpe!"],

    ["Ubaldo",
    "Ubaldo é o marido da balda?"],

    ["Alfa",
    "Alface ou tomate?"],

    ["Ka",
    "Ka, L, M, N, O, P."],

    ["Justa",
    "Justagora que eu ia jantar."],

    ["Maki",
    "Makiagem é coisa para adultos."],

    ["Loga",
    "Logagora que eu entrei no banho."],

    ["Quessa",
    "Quessa B? Vou me mandar."],

    ["Masqui",
    "Masqui droga - abre a porta e pronto!"],

    ["'Jaques'",
    "'Jaquesou' importante, você deveria falar comigo primeiro."],

    ["Midê",
    "Midêxa em paz!"],

    ["Undi",
    "Undia é da caça outro é do caçador."],

    ["Tudor",
    "Tudor que sobe, desce."],

    ["Acara",
    "Acara-puça serviu, hein?"],

    ["Aispe",
    "Aispe-rança é a última que morre."],

    ["Kênia",
    "Kênia sabe?"],

    ["Bemki",
    "Bemki te vi lá fora."],

    ["Jaca",
    "Jacaré no seco anda?"],

    ["Quenco",
    "Quenco-chicha o rabo espicha."],

    ["Tádi",
    "Tádi brincadeira, né? Deixa eu rir, então."],

    ["Ocessá",
    "Ocessá-be um monte de coisa, né?"],

    ["Temki",
    "Temki ter uma piada melhor que essa."],

    ["Cetá",
    "Cetá pensando que eu sou besta?"],

    ["Vôti",
    "Vôti botar pra correr."],

    ["Donalda",
    "Donalda não... São cinquenta centavos."],

    ["Alface",
    "Alface a face é mais emocionante."],

    ["Ivo",
    "Ivo cê não sabia que não tem ninguém em casa?"],

    ["Quessa",
    "Quessa Bê? Essa brincadeira está um saco."],

    ["Quenfo",
    "Quenfo à roça perdeu a carroça."],

    ["Justa",
    "Justagora que eu ia embora."],

    ["Taca",
    "Taca mãe primeiro!"],

    ["Tanaka",
    "'Tanaka-ra' que você não vai se dar bem!"],

    ["Quenfo",
    "Quenfo ao ar perdeu o lugar!"],

    ["Soé",
    "Soé jeito de falar com um amigo?"],

    ["Daum",
    "'Daum' tempo, pode ser?"],

    ["Isadora",
    "Isadora, o que é que eu faço?"],

    ["Vêssi",
    "'Vêssi' da próxima vez toma mais cuidado!"],

    ["Teá",
    "Teá-doro, mas isso também é demais."],

    ["Carlota",
    "A Carlota está presa na roda?"],

    ["Bu",
    "Eu nem me assustei."],

    ["Tu",
    "Tu, cara de tatu!"],

    ["Pó",
    "Pó-su entrar?"],

    ["Sará",
    "Sará que que tem outro jeito de entrar neste prédio?"],

    ["Mico",
    "Miconta que novidade é essa!"],

    ["Numi",
    "Numi amola e me deixa entrar."],

    ["Miá",
    "Miá-juda, a porta emperrou."],

    ["Nuncre",
    "Nuncre dita em mim?"],

    ["Dianta",
    "não Dianta falar, você não vai abrir a porta..."],

    ["Dorré",
    "Mi, Fá, Sol, Lá, Si!"],

    ["Dexeu",
    "Dexeu ver quem taí."],

    ["Tássia",
    "Tássia-chando, hem? Abre logo."],

    ["Omeu",
    "Omeu Deus do céu!"],

    ["Dizaí",
    "Dizaí o quê?"],

    ["Inter",
    "Interessante esta brincadeira."],

    ["Grato",
    "Não há de quê."],

    ["Quicão",
    "Quicão fusão é essa?"],

    ["Mamão",
    "Mamão mandou bater nesta daqui!"],

    ["Nunci",
    "Nunci deve comer de boca cheia."],

    ["Kiko",
    "E o Kiko eu tenho que saber sobre isso?"],

    ["Silêncio",
    "Pssss!"],

    ["Vossocá",
    "Eu não, por favor."],

    ["Pu",
    "Pu xavida, você me enganou."],

    ["Miá",
    "Miá corda, não me deixa perder o bondinho."],

    ["Nívea",
    "Feliz Niveassário!"],

    ["Sino",
    "O sino faz \"blém\" não \"quem\"."],

    ["Diki",
    "Diki lado você está?"],

    ["Querê",
    "Querê não é podê."],

    ["Frankstein",
    "Frankstein, mas você não tem."],

    ["Pra Z",
    "Pra Z em conhecê-lo."],

    ["Ex-conde",
    "Ex-conde-conde é legal."],

    ["Apri",
    "Apri-ncesa despertou com o beijo do príncipe."],

    ["Quacker",
    "Quacker uma, menos esta!"],

    ["Qualquerco",
    "Qualquerco-isa parecida com isto já vai me ajudar."],

    ["Quiqui",
    "'Quiqui' é isso?"],

    ["Abá",
    "Abá-xaqui, a chave caiu!"],

    ["Póba",
    "Póba-tê, esqueci a piada!"],

    ["Urralo",
    "Urralo-ween já passou!"],

    ["Sará",
    "Sará que tem um médico em casa?"],

    ["Aline",
    "Aline é reta ou curva?"],

    ["Dôdis",
    "Dôdis tômago."],

    ["Dôdi",
    "Dôdi dente."],

    ["Toco",
    "Toco dor de cabeça."],

    ["Atch",
    "Saúde."],

    ["Aumen",
    "Aumen-te o volume, por favor."],

    ["Zupra",
    "Zupra-sumo."],

    ["Tupó",
    "Tupó descer ali comigo?"],
]

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "Oi, %!",
        "Iuhuuu %, legal ver você.",
        "Estou feliz que você esteja aqui hoje!",
        "Bom, oi pessoal, %.",
        ]

SharedChatterComments = [
        "Que nome legal, %.",
        "Gosto do seu nome.",
        "Cuidado com os " + Cogs + "."
        "Parece que o bondinho está chegando!",
        "Preciso jogar um jogo no bondinho para ganhar algumas tortas!",
        "Às vezes, eu me divirto com os jogos no bondinho só para comer a torta de frutas!",
        "Puxa, acabei de deter um bando de " + Cogs + ". Preciso de descanso!",
        "Puxa vida, alguns desses " + Cogs + " são grandalhões!",
        "Você parece estar se divertindo.",
        "Nossa, que dia legal!",
        "Gostei da sua roupa.",
        "Acho que vou pescar esta tarde.",
        "Divirta-se no meu bairro.",
        "Espero que você esteja aproveitando sua estada em Toontown!",
        "Ouvi falar que está nevando no Brrrgh.",
        "Você pegou o bondinho hoje?",
        "Gosto de conhecer pessoas novas.",
        "Uau, há vários  "+ Cogs +" no Brrrgh."
        "Eu adoro brincar de pique. E você?",
        "Os jogos no bondinho são divertidos.",
        "Adoro fazer as pessoas rirem.",
        "É divertido ajudar meus amigos.",
        "Hum-hum, você está perdido? Não se esqueça de que você tem um mapa no Álbum Toon.",
        "Procure não ficar atolado na Burocracia dos " + Cogs + "'.",
        "Ouvi falar que a " + Daisy + " plantou novas flores no jardim.",
        "Se você pressionar a tecla Page Up, poderá ver acima!",
        "Se você ajudar a tomar os edifícios dos Cogs, poderá ganhar uma estrela de bronze!",
        "Se você pressionar a tecla Tab, poderá ver os arredores sob diversos ângulos!",
        "Se você pressionar a tecla Ctrl, poderá descer!",
        ]

SharedChatterGoodbyes = [
        "Tenho que ir agora, tchau!",
        "Acho que vou jogar no bondinho.",
        "Bom, até mais. Vejo você por aí, %!",
        "Melhor eu me apressar e voltar ao trabalho para deter esses "+ Cogs +".",
        "Preciso ir andando.",
        "Desculpe, mas tenho que ir.",
        "Tchau.",
        "Vejo você mais tarde, %!",
        "Acho que vou praticar lançamento de bolinhos.",
        "\Vou me juntar a um grupo para deter alguns  "+Cogs+".",
        "Foi legal ver você hoje, %.",
        "Tenho muito a fazer hoje. É melhor começar logo.",
        ]

# Lines specific to each character.
# If a talking char is mentioned, it cant be shared among them all

MickeyChatter = (
        [ # Greetings specific to Mickey
        "Bem-vindo ao "+lToontownCentral+".",
        "Oi, meu nome é " + Mickey + ". Qual é o seu?",
        ],
        [ # Comments
        "Ei, você viu o "+ Donald +"?",
        "Vou ver o nevoeiro passar no "+lDonaldsDock+".",
        "Se você vir o meu camarada "+Goofy+", dê um oi para ele por mim.",
        "Ouvi falar que a "+Daisy+" plantou novas flores no jardim."
        ],
       [ # Goodbyes
        "\Vou para a Melodilândia ver a "+Minnie+"!",
        "Caramba, estou atrasado para meu encontro com a "+ Minnie +"!",
        "Parece que é hora de "+ Pluto +" jantar.",
        "Acho que vou nadar no "+lDonaldsDock+".",
        "É hora de tirar um cochilo. Vou para a Sonholândia.",
        ]
    )

VampireMickeyChatter = (
        [ # Greetings specific to Vampire Mickey
        "Bem-vindo ao "+lToontownCentral+".",
        "Oi, meu nome é "+Mickey+". Qual é o seu?",
        "Feliz Halloween!",
        "Feliz Halloween, %!",
        "Bem-vindo ao Centro da Cidade Assombrada... quero dizer ao "+lToontownCentral+"!",
        ],
        [ # Comments
        "É divertido se vestir para o Halloween!",
        "Gostou da minha fantasia?",
        "%, cuidado com os  Cogs Sanguessugas!",
        "As decorações de Halloween não são fantásticas?",
        "Cuidado com os gatos pretos",
        "Você viu o Toon com a cabeça de abóbora?",
        "Buu!  Assustei você?",
        "Não se esqueça de escovar suas presas",
        "Não tenha medo, sou um vampiro amigável",
        "Gostou da minha capa?",
        "Assustei você?  Foi a melhor brincadeira da minha vida!",
        "Espero que esteja curtindo nossa festa de Halloween!",
        "Assombroso, está escuro como a noite!", 
        ],
        [ # Goodbyes
        "Vou olhar as decorações curiosas de Halloween.",
        "Vou a Melodilândia fazer uma surpresa à "+Minnie+"!",
        "Vou assustar outro Toon!  Shhh!",
        "Vou brincar de doces ou travessuras!",
        "Shhh, vem comigo.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Bem-vindo à Melodilândia.",
        "Oi, meu nome é "+ Minnie +". Qual é o seu?"
        ],
        [ # Comments
        "As colinas ganham vida com o som da música!",
        # the merry no longer goes round
        #"Não deixe de tentar andar no carrossel gigante!",
        "Sua roupa é legal, %.",
        "Ei, você viu o "+ Mickey +"?",
        "Se você vir meu amigo "+ Goofy +", dê um oi para ele por mim.",
        "Uau, há milhares de "+ Cogs +" perto da "+lDonaldsDreamland+".",
        "Ouvi falar que tem neblina no "+lDonaldsDock+".",
        "Não deixe de experimentar o labirinto dos "+lDaisyGardens+".",
        "Acho que vou catar algumas canções.",
        "Ei, %, olha aquilo lá.",
        "Adoro o som da música.",
        "Aposto que você não sabia que a Melodilândia também é chamada de ToadaTown! Ah, ah, ah!",
        "Adoro jogo da memória. E você?",
        "Gosto de fazer as pessoas rirem.",
        "Cara, andar sobre rodas o dia todo não é moleza para os pés!",
        "Bonita camisa, %.",
        "Aquilo no chão é uma balinha?",
        ],
        [ # Goodbyes
        "Caramba, estou atrasada para o meu encontro com o "+ Mickey +"!",
        "Parece que é hora de "+ Pluto +" jantar.",
        "É hora de tirar um cochilo. Vou para a Sonholândia.",
        ]
    )

DaisyChatter = (
        [ # Greetings
        "Bem-vindo(a) ao meu Jardim!",
        "Olá, meu nome é "+Daisy+". Qual o seu nome?",
        "É muito bom ver você, %!",
        ],
        [ # Comments
        "Minha flor premiada está no centro do labirinto do jardim.",
        "Eu adoro andar pelo labirinto.",
        "Eu não ví o "+Goofy+" hoje.",
        "Eu gostaria de saber onde o "+Goofy+" está.",
        "Você viu o "+Donald+"? Eu não consigo encontrá-lo em lugar algum.",
        "Se você vir minha amiga "+Minnie+", por favor diga \"Oi\" por mim.",
        "Quanto melhor as ferramentas de jardinagem que você tem, melhor será seu jardim.",
        "Existem muitos "+Cogs+" perto do "+lDonaldsDock+".",
        "Regando seu jardim diariamente você deixa suas plantas felizes.",
        "Para cultivar uma Margarida Rosa, plante uma balinha amarela e uma vermelha juntas.",
        "É facil cultivar uma Margarida Amarela. Basta plantar uma balinha amarela.",
        "Se você vir areia embaixo de uma planta, está na hora de regar ou ela morrerá.",
        ],
        [ # Goodbyes
        "Estou indo para Melodilândia para ver %s!" % Minnie,
        "Preciso correr para o meu picnic com %s!" % Donald,
        "Acho que vou nadar no "+lDonaldsDock+".",
        "Oh, estou com sono. Acho que vou para a Sonholândia.",
        ]
    )

ChipChatter = (
        [ # Greetings
        "Boas-vindas a %s!" % lOutdoorZone,
        "Olá, sou " + Chip + ". Qual é o seu nome?",
        "Não, eu sou " + Chip + ".",
        "É tão bom ver você, %!",
        "Somos Tico e Teco!",
        ],
        [ # Comments
        "Gosto de golfe.",
        "Temos as melhores bolotas de Toontown.",
        "Os buracos de golfe com vulcões são os mais desafiadores para mim.",
        ],
        [ # Goodbyes
        "Vamos até " + lTheBrrrgh +" brincar com %s." % Pluto,
        "Vamos visitar %s e dar um jeito nele." % Donald,
        "Acho que vou nadar no " + lDonaldsDock + ".",
        "Oh, estou com sono. Acho que vou até a Sonholândia.",
        ]
    )

# Warning Dale's chatter is dependent on on Chip's, they should match up
DaleChatter = (
        [ # Greetings
        "É tão bom ver você, %!",
        "Olá, sou " + Dale + ". Qual é o seu nome?",
        "Olá, sou " + Chip + ".",
        "Boas-vindas a %s!" % lOutdoorZone,
        "Somos Tico e Teco!",
        ],
        [ # Comments
        "Gosto de piqueniques.",
        "As bolotas são gostosas, experimente.",
        "Aqueles moinhos também são difíceis.",
        ],
        [ # Goodbyes
        "Hihihi, é divertido brincar com " + Pluto + ".",
        "Sim, vamos dar um jeito em %s." % Donald,
        "Ah, seria refrescante dar uma nadada.",
        "Estou ficando cansado, uma boa soneca cairia bem.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Bem-vindo aos "+lDaisyGardens+".",
        "Oi, meu nome é "+ Goofy +". Qual é o seu?",
        "Puxa, muito legal ver você %!",
        ],
        [ # Comments
        "Cara, com certeza é fácil se perder no labirinto do jardim!",
        "Não deixe de tentar entrar no labirinto.",
        "Não vi a "+ Daisy +" o dia todo.",
        "Onde será que a "+ Daisy +" está?",
        "Ei, você viu o "+ Donald +"?",
        "Se você vir o meu amigo "+ Mickey +", dê um oi para ele por mim.",
        "Ah, não! Esqueci de fazer o café da manhã do "+ Mickey +"!",
        "Puxa, com certeza há muitos "+ Cogs +" perto do "+lDonaldsDock+".",
        "Parece que a "+ Daisy +" plantou novas flores no jardim.",
        "Na filial da minha Loja de Piadas no Brrrgh, há Óculos hipnóticos em promoção por apenas uma balinha!",
        "As Lojas de piadas do Pateta oferecem as melhores gozações, truques e comédias de toda Toontown!",
        "Nas Lojas de piadas do Pateta, todas as tortas na cara têm garantia de fazer rir, ou você tem as suas balinhas de volta!",
        ],
        [ # Goodbyes
        "\Vou para Melodilândia para ver a  "+ Minnie +"!",
        "Caramba, estou atrasado para o meu jogo com o  "+ Donald + "!",
        "Acho que vou nadar no Porto do "+lDonaldsDock+".",
        "É hora de tirar um cochilo. Vou para a Sonholândia.",
        ]
    )

GoofySpeedwayChatter = (
        [ # Greetings
        "Bem-vindo a "+lGoofySpeedway+".",
        "Oi, meu nome é "+Goofy+". Qual é o seu?",
        "Puxa, muito legal ver você %!",
        ],
        [ # Comments
        "Cara, assisti a uma corrida maneira hoje.",
        "Cuidado com as cascas de banana na pista!",
        "Você deu uma incrementada no seu kart?",
        "A gente acabou de pegar uns aros novos na loja do kart.",
        "Oi, você viu "+Donald+"?",
        "Se você vir meu amigo "+Mickey+", diz que eu mandei um alô.",
        "Ah, não! Esqueci de preparar para "+Mickey+" o café da manhã!",
        "Puxa, com certeza há muitos "+Cogs+" perto de "+lDonaldsDock+".",
        "Na filial da minha Loja de Piadas no Brrrgh, há Óculos hipnóticos em promoção por apenas uma balinha!",
        "As Lojas de piadas do Pateta oferecem as melhores gozações, truques e comédias de toda Toontown!",
        "Nas Lojas de piadas do Pateta, todas as tortas na cara têm garantia de fazer rir, ou você tem as suas balinhas de volta!"
        ],
        [ # Goodbyes
        "Vou para Melodilândia para ver %s!" % Mickey,
        "Caramba, estou atrasado para o meu jogo com %s!" % Donald,
        "Acho que vou nadar no "+lDonaldsDock+".",
        "É hora de tirar um cochilo. Vou para a Sonholândia.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Bem-vindo à Sonholândia.",
        "Oi, meu nome é "+ Donald +". Qual é o seu?",
        ],
        [ # Comments
        "Às vezes este lugar me dá arrepios.",
        "Não deixe de experimentar o labirinto dos "+lDaisyGardens+".",
        "Nossa, que dia legal!",
        "Ei, você viu o "+ Mickey +"?",
        "Se você vir meu parceiro "+ Goofy +", dê um oi para ele por mim.",
        "Acho que vou pescar esta tarde.",
        "Uau, há um monte de "+ Cogs +" no "+lDonaldsDock+".",
        "Escuta, eu não levei você ainda para um passeio no "+lDonaldsDock+"?",
        "Não vi a "+ Daisy +" o dia todo.",
        "Ouvi falar que a "+ Daisy +" plantou novas flores no jardim.",
        "Quack.",
        ],
        [ # Goodbyes
        "Vou a Melodilândia para ver a "+ Minnie +"!",
        "Ah não, estou atrasado para o meu encontro com a "+ Daisy +"!",
        "Acho que vou nadar no meu cais.",
        "Acho que vou levar meu barco para um giro no meu cais.",
        ]
    )

# April Fools Chatter's
AFMickeyChatter = (
        [ # Greetings specific to Mickey
        "Feliz Semana dos April Toons (Toons de Abril)!",
        "Feliz Semana dos April Toons (Toons de Abril), %!",
        "Oi, meu nome é "+Mickey+". Qual é o seu?",
        ],
        [ # Comments
        "Você viu a Margarida por aí?",
        "Queria desejar uma feliz Semana dos April Toons (Toons de Abril) para a Margarida!",
        "Você ouviu um Rabisco falar?",
        "Oh, essas flores são lindas!",
        "Aposto que a Margarida tem ótimas dicas de Jardinagem!",
        ],
        [ # Goodbyes
        "Oi, estou procurado a Margarida. Você a viu?",
        "É hora de dar uma cochilada. Vou para a Sonholândia.",
        ]
    )

AFMinnieChatter = (
        [ # Greetings
        "Oi, meu nome é "+Minnie+". Qual é o seu?",
        "Feliz Semana dos April Toons (Toons de Abril)!",
        "Feliz Semana dos April Toons (Toons de Abril), %!",
        ],
        [ # Comments
        "Oi, preciso dar de comer ao Pluto. Você o viu?",
        "Queria desejar uma feliz Semana dos April Toons (Toons de Abril) para o Pluto com um biscoito canino!",
        "Você ouviu um Rabisco falar?",
        ],
        [ # Goodbyes
        "Oi, preciso dar de comer ao Pluto. Você o viu?",
        "Nossa, estou atrasada para meu encontro com o %s!" % Mickey,
        ]
    )

AFDaisyChatter = (
        [ # Greetings
        "Oi, sou a "+Daisy+". Qual é o seu nome?",
        "Feliz Semana dos April Toons (Toons de Abril)!",
        "Feliz Semana dos April Toons (Toons de Abril), %!",
        ],
        [ # Comments
        "Queria saber se o Mickey foi combater alguns Cogs?",
        "Você viu o Mickey por aí?",
        "Queria desejar uma feliz Semana dos April Toons (Toons de Abril) para o Mickey!",
        "Você ouviu um Rabisco falar ou estou ouvindo coisas?",
        ],
        [ # Goodbyes
        "Oi, preciso falar com o Micky (Mickey). Você o viu?",
        "Acho que vou nadar no "+lDonaldsDock+".",
        "Oh, estou com soninho. Acho que vou para a Sonholândia",
        ]
    )

AFGoofySpeedwayChatter = (
        [ # Greetings
        "Feliz Semana da Preguiça, hã, dos April Toons (Toons de Abril)!",
        "Feliz Semana dos April Toons (Toons de Abril), %!",
        "Oi, meu nome é "+Goofy+". Qual é o seu?",
        ],
        [ # Comments
        "Ohoh, você viu o Donald? Acho que ele está sonâmbulo novamente",
        "Queria desejar uma feliz Semana dos April Toons (Toons de Abril) para o Donald!",
        "Você ouviu um Rabisco falar ou estou vendo coisas?",
        "Espero que tudo esteja bem no Autódromo.",
        ],
        [ # Goodbyes
        "Ohoh, estou atrasado para meu jogo com o %s!" % Donald,
        ]
    )

AFDonaldChatter = (
        [ # Greetings
        "Feliz Semana da Preguiça, hã, dos April Toons (Toons de Abril)!",
        "Feliz Semana dos April Toons (Toons de Abril), %!",
        "Oi, meu nome é%s. Qual é o seu?" % Donald,
        ],
        [ # Comments
        "Você viu o Pateta por aí?",
        "Queria desejar uma feliz Semana dos April Toons (Toons de Abril) para o Pateta!",
        "Você ouviu um Rabisco falar ou estou sonhando?",
        "De onde surgiu esse kart?",
        ],
        [ # Goodbyes
        "De onde surgiram repentinamente todos esses carros barulhentos?",
        "Vou para Melodilândia ver a %s!" % Minnie,
        ]
    )    

CLGoofySpeedwayChatter = (
        [ # Greetings
        "Bem-vindo ao "+lGoofySpeedway+".",
        "Oi, meu nome é "+Goofy+". Qual é o seu?",
        "Ohoh, que bom ver você %!",
        "Olá!  Perdoe minhas roupas sujas, estava consertando aquele Quadro de Pontuação quebrado.",
        ],
        [ # Comments        
        "É bom que o Quadro de Pontuação esteja funcionando logo, pois o Fim de Semana do Grande Prêmio está chegando!",
        "Alguém quer comprar um kart meio usado? Ele já apareceu no Quadro de Pontuação!", 
        "O Fim de Semana do Grande do Prêmio está chegando, é melhor começar a treinar.",
        "O Fim de Semana do Grande Prêmio será de sexta-feira, 22, a segunda-feira, 25 de maio!",
        "Preciso de uma escada para descer aquele kart.",
        "Aquele Toon realmente queria aparecer no Quadro de Pontuação!",
        "Cara, acabei de ver uma corrida terrível.",
        "Cuidado com as cascas de banana na pista!",
        "Você fez algumas melhorias em seu kart ultimamente?",
        "Precisamos adquirir alguns aros novos na loja de kart.",
        "Ei, você viu o "+Donald+"?",
        "Se vir o meu amigo "+Mickey+", mande lembranças a ele por mim.",
        "Puxa! Esqueci de preparar o café da manhã do "+Mickey+"!",
        "Ohoh, tem um monte de "+Cogs+" perto do "+lDonaldsDock+".",
        "Nos galhos do Brrrgh da minha Loja de Brincadeiras, os Óculos Hipnotizantes estão à venda por apenas 1 balinha!",
        "A Loja de Piadas do Pateta tem as melhores piadas, truques e brincadeiras divertidas de toda Toontown!",
        "Na Loja de Piadas do Pateta, até uma torta na cara é garantia de boas risadas ou você recebe suas balinhas de volta!"
        ],
        [ # Goodbyes
        "É bom eu fazer uma nova pintura no meu kart antes do Fim de Semana do Grande Prêmio.",
        "Caramba, é melhor eu dar um jeito nesse Quadro de Pontuação quebrado!",
        "Espero ver todos vocês no Fim de Semana do Grande Prêmio!  Adeus!",
        "É hora de dar uma cochilada. Vou para a Sonholândia sonhar com a vitória no Grande Prêmio.",
        ]
    )
        

GPGoofySpeedwayChatter = (
        [ # Greetings
        "Bem-vindo ao "+lGoofySpeedway+".",
        "Bem-vindo ao Fim de Semana do Grande Prêmio!", 
        "Oi, meu nome é "+Goofy+". Qual é o seu?",
        "Ohoh, que bom ver você %!",
        ],
        [ # Comments                
        "Você está na expectativa do Fim de Semana do Grande Prêmio?",
        "A boa notícia é que o Quadro de Pontuação está pronto.",
        "Conseguimos consertar o Quadro de Pontuação bem na hora do Fim de Semana do Grande Prêmio!",
        "Nunca encontramos aquele Toon!",
        "Cara, acabei de ver uma corrida terrível.",
        "Cuidado com as cascas de banana na pista!",
        "Você fez algumas melhorias em seu kart ultimamente?",
        "Precisamos comprar alguns aros novos na loja de kart.",
        "Ohoh, você viu o "+Donald+"? Ele disse que estava vindo para o Grande Prêmio!",
        "Se vir o meu amigo "+Mickey+", diga a ele que está perdendo uma corrida incrível!",
        "Puxa! Esqueci de preparar o café da manhã do "+Mickey+"!",
        "Ohoh, tem um monte de "+Cogs+" perto do "+lDonaldsDock+".",
        "Nos galhos do Brrrgh da minha Loja de Brincadeiras, os Óculos Hipnotizantes estão à venda por apenas 1 balinha!",
        "A Loja de Piadas do Pateta tem as melhores piadas, truques e brincadeiras divertidas de toda Toontown!",
        "Na Loja de Piadas do Pateta, até uma torta na cara é garantia de boas risadas ou você recebe suas balinhas de volta!"
        ],
        [ # Goodbyes
        "Boa sorte no Grande Prêmio!",
        "Vou participar da próxima corrida do Grande Prêmio!",
        "Ohoh, acho que a próxima corrida já vai começar!",
        "Puxa, é melhor verificar o novo Quadro de Pontuação e garantir que esteja funcionando bem!", 
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)

# FriendsListPanel.py
FriendsListPanelNewFriend = "Novo amigo"
FriendsListPanelSecrets = "Segredos"
FriendsListPanelOnlineFriends = "AMIGOS\nON-LINE"
FriendsListPanelAllFriends = "TODOS\nOS AMIGOS"
FriendsListPanelIgnoredFriends = "TOONS\nIGNORADOS"
FriendsListPanelPets = "BICHINHOS\nPRÓXIMOS"
FriendsListPanelPlayers = "TODOS OS AMIGOS\nDO JOGADOR"
FriendsListPanelOnlinePlayers = "AMIGOS ONLINE\nDO JOGADOR"

FriendInviterClickToon = "Clique no Toon com o qual você quer fazer amizade.\n\n(Você tem %s amigos)"

# Support DISL account friends
FriendInviterToon = "Toon"
FriendInviterThatToon = "Aquele Toon"
FriendInviterPlayer = "Jogador"
FriendInviterThatPlayer = "Aquele jogador"
FriendInviterBegin = "Que tipo de amigo você quer ter?"
FriendInviterToonFriendInfo = "Um amigo somente em Toontown"
FriendInviterPlayerFriendInfo = "Um amigo em toda a rede Disney.com"
FriendInviterToonTooMany = "Você tem amigos Toons demais para poder acrescentar um agora. Você terá de remover alguns amigos Toons se quiser fazer amizade com %s. Você também pode tentar fazer amizade com seu jogador."
FriendInviterPlayerTooMany = "Você tem amigos jogadores demais para poder acrescentar um agora. Você terá de remover alguns amigos jogadores se quiser fazer amizade com %s. Você também pode tentar fazer amizade com seu Toon."
FriendInviterToonAlready = "%s já é seu amigo Toon."
FriendInviterPlayerAlready = "%s já é seu amigo jogador."
FriendInviterStopBeingToonFriends = "Romper amizade Toon"
FriendInviterStopBeingPlayerFriends = "Romper amizade de jogador"
FriendInviterEndFriendshipToon = "Tem certeza de que quer romper a amizade de Toon com %s?"
FriendInviterEndFriendshipPlayer = "Tem certeza de que quer romper a amizade de jogador com %s?"
FriendInviterRemainToon = "\n(Você vai continuar sendo amigo Toon de %s)"
FriendInviterRemainPlayer = "\n(Você vai continuar sendo amigo jogador de %s)"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Sinto muito, você não pode avançar porque o download de %(phase)s está apenas %(percent)s%% concluído.\n\nTente novamente mais tarde."

# TeaserPanel.py
TeaserTop = ""
TeaserBottom = ""
TeaserDefault = ",\nVocê precisa ser um associado.\nUna-se!"
TeaserOtherHoods = "Visite os 6 bairros exclusivos!"
TeaserTypeAName = "Digite o seu nome favorito para o seu Toon!"
TeaserSixToons = "Crie até 6 Toons em uma só conta!"
TeaserClothing = "Compre roupas exclusivas para personalizar o seu Toon!"
TeaserCogHQ = "Infiltre-se nas\nperigosas áreas avançadas dos Cogs!"
TeaserSecretChat = "Troque segredos\ncom seus amigos conversando on-line com eles!"
TeaserSpecies = "Crie e jogue com Toons Macacos, Cavalos e Ursos!"
TeaserFishing = "Colecione todas as espécies de peixes!"
TeaserGolf = "Jogue em campos de golfe malucos!"
TeaserParties = " Para planear Partes"
TeaserSubscribe = "Assinar"
TeaserContinue = "Continuar na versão gratuita"
TeaserEmotions = "Para fazer seu Toon mais expressivo"
TeaserKarting = "Aposte corridas com outros Toons em karts maneiros!"
TeaserKartingAccessories = "Personalize seu kart com acessórios incríveis."
TeaserGardening = "Plante flores, construa estátuas e cultive árvores em seu terreno."
TeaserHaveFun = "Encontre mais diversão!"
TeaserJoinUs = "Una-se!"

#TeaserCardsAndPosters = ""
#TeaserFurniture = ""
TeaserMinigames = TeaserOtherHoods
#TeaserHolidays = ""
TeaserQuests = TeaserOtherHoods
TeaserOtherGags = TeaserOtherHoods
#TeaserRental = ""
#TeaserBigger = ""
TeaserTricks = TeaserOtherHoods

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "Fazendo download %s"
DownloadWatcherInitializing = "Iniciando Download..."

# Launcher.py
LauncherPhaseNames = {
    0   : "Inicialização",
    1   : "Panda",
    2   : "Motor",
    3   : "Fazer um Toon",
    3.5 : "Toontorial",
    4   : "Parque",
    5   : "Ruas",
    5.5 : "Estados",
    6   : "Bairros I",
    7   : Cog + " Edifícios dos",
    8   : "Bairros II",
    9   : Sellbot + " Quartel dos",
    10  : Cashbot + " Quartel dos",
    11  : Lawbot + " Quartel dos",
    12  : Bossbot + " HQ",
    13  : "Festas",
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)s (%(current)s de %(total)s)"
LauncherStartingMessage = "Iniciando Toontown On-line da Disney..."
LauncherDownloadFile = "Fazendo download da atualização de "+ LauncherProgress +"..."
LauncherDownloadFileBytes = "Fazendo download da atualização de "+ LauncherProgress +": %(bytes)s"
LauncherDownloadFilePercent = "Fazendo download da atualização de "+ LauncherProgress +": %(percent)s%%"
LauncherDecompressingFile = "Descompactando atualização de "+ LauncherProgress +"..."
LauncherDecompressingPercent = "Descompactando atualização de "+ LauncherProgress +": %(percent)s%%"
LauncherExtractingFile = "Extraindo atualização de "+ LauncherProgress +"..."
LauncherExtractingPercent = "Extraindo atualização de "+ LauncherProgress +": %(percent)s%%"
LauncherPatchingFile = "Aplicando atualização de "+ LauncherProgress +"..."
LauncherPatchingPercent = "Aplicando atualização de "+ LauncherProgress +": %(percent)s%%"
LauncherConnectProxyAttempt = "Conectando-se a Toontown: %s (proxy: %s) tentativa: %s"
LauncherConnectAttempt = "Conectando-se a Toontown: %s tentativa %s"
LauncherDownloadServerFileList = "Atualizando Toontown..."
LauncherCreatingDownloadDb = "Atualizando Toontown..."
LauncherDownloadClientFileList = "Atualizando Toontown..."
LauncherFinishedDownloadDb = "Atualizando Toontown..."
LauncherStartingToontown = "Iniciando Toontown..."
LauncherStartingGame = "Iniciando Toontown..."
LauncherRecoverFiles = "Atualizando Toontown. Recuperando arquivos..."
LauncherCheckUpdates = "Verificando atualizações de "+ LauncherProgress
LauncherVerifyPhase = "Atualizando Toontown..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Fazer um\nToon"
AvatarChoicePlayThisToon = "Jogar com\neste Toon"
AvatarChoiceSubscribersOnly = "Assinar\n\n\n\nAgora!"
AvatarChoiceDelete = "Excluir"
AvatarChoiceDeleteConfirm = "Isto fará que %s seja excluído para sempre."
AvatarChoiceNameRejected = "Nome\nrejeitado"
AvatarChoiceNameApproved = "Nome\naprovado!"
AvatarChoiceNameReview = "Em\nrevisão"
AvatarChoiceNameYourToon = "Dar um\nnome ao Toon!"
AvatarChoiceDeletePasswordText = "Cuidado! Isto fará que %s seja excluído para sempre. Para excluir este Toon, insira a sua senha."
AvatarChoiceDeleteConfirmText = "Cuidado! Isto excluirá %(name)s para sempre. Se você tiver certeza de que é isso mesmo que deseja, digite \"%(confirm)s\" e clique em OK."
AvatarChoiceDeleteConfirmUserTypes = "excluir"
AvatarChoiceDeletePasswordTitle = "Excluir Toon?"
AvatarChoicePassword = "Senha"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "Esta senha não parece ser a correta. Para excluir este Toon, insira a sua senha."
AvatarChoiceDeleteWrongConfirm = "Você não digitou corretamente. Para excluir %(name)s, digite \"%(confirm)s\" e clique em OK. Não digite as aspas. Clique em Cancelar se desistir."

# AvatarChooser.py
AvatarChooserPickAToon = "Escolha um Toon para jogar"
AvatarChooserQuit = lQuit

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Ligue para o Atendimento ao Cliente: %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nSe precisar de ajuda, ligue para o Atendimento ao Cliente%s."
TTAccountIntractibleError = "Erro."

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]
DateOfBirthEntryDefaultLabel = "Data de nascimento"


# AchievePage.py
AchievePageTitle = "Realizações\n(em breve)"

# PhotoPage.py
PhotoPageTitle = "Foto\n(em breve)"

# BuildingPage.py
BuildingPageTitle = "Edifícios\n(em breve)"

# InventoryPage.py
InventoryPageTitle = "Piadas"
InventoryPageDeleteTitle = "EXCLUIR PIADAS"
InventoryPageTrackFull = "Você possui todas as piadas do tipo %s."
InventoryPagePluralPoints = "Você obterá uma nova piada de\n%(trackName)s quando\nganhar mais %(numPoints)s pontos de %(trackName)s."
InventoryPageSinglePoint = "Você obterá uma nova piada de\n%(trackName)s quando\nganhar mais %(numPoints)s pontos de %(trackName)s."
InventoryPageNoAccess = "Você ainda não tem acesso ao tipo %s."

# NPCFriendPage.py
NPCFriendPageTitle = "SOS Toons"

# EventsPage.py
PartyDateFormat = "%(mm)s %(dd)d, %(yyyy).4d" # Dec 8, 2008
PartyTimeFormat = "%d:%.2d %s" # 1:45 pm
PartyTimeFormatMeridiemAM = "am"
PartyTimeFormatMeridiemPM = "pm"
PartyCanStart = "É Hora de Festejar! Clique em Start Party (Iniciar Festa) na sua página Shticker Book Hosting (Hospedando do Livro de Brincadeiras)!"
PartyHasStartedAcceptedInvite = '%s, a festa começou!  Clique no anfitrião e em "Ir à Festa" na página Shticker Book Invites (Convites do Livro de Brincadeiras).'
PartyHasStartedNotAcceptedInvite = '%s, a festa começou! Você também pode ir, teletransportando-se para o anfitrião.'

EventsPageName = "Eventos"
EventsPageCalendarTabName = "Calendário"
EventsPageCalendarTabParty = "Festa"
EventsPageToontownTimeIs = "A HORA DE TOONTOWN É"
EventsPageConfirmCancel = "Se cancelar, receberá uma devolução de %d%%. Tem certeza de que quer cancelar sua festa?"
EventsPageCancelPartyResultOk = "Sua festa foi cancelada e você recebeu %d balinhas de volta!"
EventsPageCancelPartyResultError = "Desculpe, sua festa não foi cancelada."
EventsPageTooLateToStart = "Desculpe, tarde demais para começar a sua festa. Você pode cancelá-la e planejar outra."
EventsPagePublicPrivateChange = "Alterando a sua configuração de privacidade de festa..."
EventsPagePublicPrivateNoGo = "Desculpe, você não pode alterar a sua configuração de privacidade de festa agora."
EventsPagePublicPrivateAlreadyStarted = "Desculpe, a sua festa já começou, e você não pode alterar sua configuração de privacidade de festa."
EventsPageHostTabName = "Hospedando" # displayed on the physical tab
EventsPageHostTabTitle = "Minha Próxima Festa" # banner text displayed across the top
EventsPageHostTabTitleNoParties = "Sem Festas"
EventsPageHostTabDateTimeLabel = "Você tem uma festa em %s às %s, Hora de Toontown."
EventsPageHostingTabNoParty = "Vá ao Portão de Festa\nde um pátio para planejar\nsua festa!"
EventsPageHostTabPublicPrivateLabel = "Esta festa é:"
EventsPageHostTabToggleToPrivate = "Particular"
EventsPageHostTabToggleToPublic = "Pública"
EventsPageHostingTabGuestListTitle = "Convidados"
EventsPageHostingTabActivityListTitle = "Atividades"
EventsPageHostingTabDecorationsListTitle = "Decorações"
EventsPageHostingTabPartiesListTitle = "Anfitriões"
EventsPageHostTabCancelButton = "Cancelar Festa"
EventsPageGoButton = "Iniciar\nFesta!"
EventsPageGoBackButton = "Festa\nJá!"
EventsPageInviteGoButton = "Ir para\Festa!"
EventsPageUnknownToon = "Toon Desconhecido"

EventsPageInvitedTabName = "Convites"
EventsPageInvitedTabTitle = "Convites de Festa"
EventsPageInvitedTabInvitationListTitle = "Convites"
EventsPageInvitedTabActivityListTitle = "Atividades"
EventsPageInvitedTabTime = "%s %s Hora de Toontown"

EventsPageNewsTabName = "Notícias"
EventsPageNewsTabTitle = "Notícias"
EventsPageNewsDownloading= "Recuperando Notícias..."
EventsPageNewsUnavailable = "Tico e Teco brincando com a impressora da gráfica. Notícias não disponíveis."
EventsPageNewsPaperTitle = "TOONTOWN TIMES (GAZETA DE TOONTOWN)"
EventsPageNewsLeftSubtitle = "Ainda só por 1 balinha" 
EventsPageNewsRightSubtitle = "Tiragem de nove mil toonplares" 

# InvitationSelection.py
SelectedInvitationInformation = "%s tem uma festa em %s às %s, Hora de Toontown."

# PartyPlanner.py
PartyPlannerNextButton = "Continuar"
PartyPlannerPreviousButton = "Voltar"
PartyPlannerWelcomeTitle = "Planejador de Festas de Toontown"
PartyPlannerInstructions = "Hospedar sua festa é muito divertido!\nComece a planejar com as setas na parte inferior!"
PartyPlannerDateTitle = "Escolha o Dia de Sua Festa"
PartyPlannerTimeTitle = "Escolha a Hora de Sua Festa"
PartyPlannerGuestTitle = "Selecione os Convidados"
PartyPlannerEditorTitle = "Crie Sua Festa\nInsira as Atividades e Decorações"
PartyPlannerConfirmTitle = "Escolha os Convites para Enviar"
PartyPlannerConfirmTitleNoFriends = "Reveja os Detalhes de Sua Festa"
PartyPlannerTimeToontown = "Toontown"
PartyPlannerTimeTime = "Hora"
PartyPlannerTimeRecap = "Dia e Hora da Festa"
PartyPlannerPartyNow = "O Mais Breve Possível"
PartyPlannerTimeToontownTime = "Hora de Toontown:"
PartyPlannerTimeLocalTime = "Hora Local da Festa: "
PartyPlannerPublicPrivateLabel = "A festa será:"
PartyPlannerPublicDescription = "Todos os Toons\npodem vir!"
PartyPlannerPrivateDescription = "Apenas\nToons Convidados\npodem vir!"
PartyPlannerPublic = "Pública"
PartyPlannerPrivate = "Particular"
PartyPlannerCheckAll = "Selecionar\nTudo"
PartyPlannerUncheckAll = "Desmarcar\nTudo"
PartyPlannerDateText = "Data"
PartyPlannerTimeText = "Hora"
PartyPlannerTTTimeText = "Hora de Toontown"
PartyPlannerEditorInstructionsIdle = "Clique na Atividade ou Decoração de Festa que deseja adquirir."
PartyPlannerEditorInstructionsClickedElementActivity = "Clique em Comprar ou Arraste o Ícone da Atividade para o Mapa da Festa"
PartyPlannerEditorInstructionsClickedElementDecoration = "Clique em Comprar ou Arraste o Ícone da Decoração para o Mapa da Festa"
PartyPlannerEditorInstructionsDraggingActivity = "Arraste a Atividade para o Mapa da Festa."
PartyPlannerEditorInstructionsDraggingDecoration = "Arraste a Decoração para o Mapa da Festa."
PartyPlannerEditorInstructionsPartyGrounds = "Clique e Arraste os itens para movê-los pelo Mapa da Festa"
PartyPlannerEditorInstructionsTrash = "Arraste uma Atividade ou Decoração até aqui para removê-la."
PartyPlannerEditorInstructionsNoRoom = "Não há lugar para colocar essa atividade."
PartyPlannerEditorInstructionsRemoved = "%(removed)s removidos(as) desde que %(added)s foram adicionados(as)."
PartyPlannerBeans = "feijões"
PartyPlannerTotalCost = "Custo Total:\n%d feijões"
PartyPlannerSoldOut = "ESGOTADO"
PartyPlannerBuy = "COMPRAR"
PartyPlannerPaidOnly = "SÓ ASSOCIADOS"
PartyPlannerPartyGrounds = "MAPA DA FESTA"
PartyPlannerOkWithGroundsLayout = "Você já terminou de mover suas Atividades e Decorações pelo Mapa da Festa?"
PartyPlannerChooseFutureTime = "Por favor, selecione uma hora futura."
PartyPlannerInviteButton = "Enviar Convites"
PartyPlannerInviteButtonNoFriends = "Planejar Festa"
PartyPlannerBirthdayTheme = "Aniversário"
PartyPlannerGenericMaleTheme = "Estrelas"
PartyPlannerGenericFemaleTheme = "Flores"
PartyPlannerRacingTheme = "Corrida"
PartyPlannerGuestName = "Nome do Convidado"
PartyPlannerClosePlanner = "Fechar Planejador"
PartyPlannerConfirmationAllOkTitle = "Parabéns!"
PartyPlannerConfirmationAllOkText = "Sua festa foi criada e os convites enviados.\nObrigado!"
PartyPlannerConfirmationAllOkTextNoFriends = "Sua festa foi criada!\nObrigado!"
PartyPlannerConfirmationErrorTitle = "Opa."
PartyPlannerConfirmationValidationErrorText = "Desculpe, ocorreu um problema\ncom essa festa.\nPor favor, volte e tente novamente."
PartyPlannerConfirmationDatabaseErrorText = "Desculpe, não foi possível registrar todas as informações.\nPor favor, tente novamente mais tarde.\nNão se preocupe, nenhum feijão foi perdido."
PartyPlannerConfirmationTooManyText = "Desculpe, você já está dando uma festa.\nSe quiser planejar outra, por favor,\ncancele a atual."
PartyPlannerInvitationThemeWhatSentence = "Você está convidado(a) para minha festa de %s! %s!"
PartyPlannerInvitationThemeWhatSentenceNoFriends = "Estou dando uma festa de %s! %s!"
PartyPlannerInvitationThemeWhatActivitiesBeginning = "Terá "
PartyPlannerInvitationWhoseSentence = "Festa de %s"
PartyPlannerInvitationTheme = "Tema"
PartyPlannerInvitationWhenSentence = "Será em %s,\nàs %s, Hora de Toontown.\nEspero que você apareça!"
PartyPlannerInvitationWhenSentenceNoFriends = "Será em %s,\nàs %s, Hora de Toontown.\nToontástico!"
PartyPlannerComingSoon = "Em Breve"
PartyPlannerCantBuy= "Não Pode Comprar"
PartyPlannerGenericName = "Planejador de Festa"

# DistributedPartyJukeboxActivity.py
PartyJukeboxOccupied = "Alguém está usando a jukebox. Tente novamente mais tarde."
PartyJukeboxNowPlaying = "A música que você escolheu já está tocando na jukebox!"

# Jukebox Music
MusicEncntrGeneralBg = "Encontro Com Cogs"
MusicTcSzActivity = "Mistureba de Toontorial"
MusicTcSz = "Passeando Juntos" 
MusicCreateAToon = "Novo Toon na Cidade"
MusicTtTheme = "O Tema de Toontown"
MusicMinigameRace = "Devagar e Firme"
MusicMgPairing = "Você se lembra de Mim?"
MusicTcNbrhood = "Centro de Toontown"
MusicMgDiving = "Cantiga do Tesouro"
MusicMgCannonGame = "Disparar os Canhões!"
MusicMgTwodgame = "Toon Contínuo"
MusicMgCogthief = "Pegue Aquele Cog!"
MusicMgTravel = "Música para Viagem"
MusicMgTugOWar = "Cabo de Guerra"
MusicMgVine = "O Balanço da Selva"
MusicMgIcegame = "Situação Delicada"
MusicMgToontag = "Mistureba de Minijogo"
MusicMMatchBg2 = "Jazz da Minnie"
MusicMgTarget = "Sobrevoando Toontown"
MusicFfSafezone = "A Fazenda Divertida"
MusicDdSz = "O Caminho Tortuoso"
MusicMmNbrhood = "Melodilândia da Minnie"
MusicGzPlaygolf = "Vamos Jogar Golfe!"
MusicGsSz = "Autódromo do Pateta"
MusicOzSz = "Terras do Tico e Teco"
MusicGsRaceCc = "Dirigindo no Centro"
MusicGsRaceSs = "Preparar, Acionar, Vai!"
MusicGsRaceRr = "Rota 66"
MusicGzSz = "A Polca Puf-Puf"
MusicMmSz = "Dançando nas Ruas"
MusicMmSzActivity = "Aí Vem o Soprano"
MusicDdNbrhood = "O Porto do Donald"
MusicGsKartshop = "Sr. Pateta Mãos à Obra"
MusicDdSzActivity = "Cabana da Praia"
MusicEncntrGeneralBgIndoor = "Botando pra Quebrar"
MusicTtElevator = "Subindo?"
MusicEncntrToonWinningIndoor = "Toons Unidos!"
MusicEncntrGeneralSuitWinningIndoor = "Cogtástrofe!"
MusicTbNbrhood = "O Brrrgh"
MusicDlNbrhood = "Sonholândia do Donald"
MusicDlSzActivity = "Contando Ovelhas"
MusicDgSz = "Valsa das Flores"
MusicDlSz = "Sonâmbulo"
MusicTbSzActivity = "Nevasca"
MusicTbSz = "Tremendo e Vibrando"
MusicDgNbrhood = "Jardim da Margarida"
MusicEncntrHallOfFame = "A Galeria da Fama"
MusicEncntrSuitHqNbrhood = "Reais e Centavos"
MusicChqFactBg = "Fábrica de Cogs"
MusicCoghqFinale = "Triunfo dos Toons"
MusicEncntrToonWinning = "Pagando à Vista!"
MusicEncntrSuitWinning = "Vendendo Seu Short"
MusicEncntrHeadSuitTheme = "O Chefão"
MusicLbJurybg = "O Julgamento Começou"
MusicLbCourtyard = "Balançando"
MusicBossbotCeoV2 = "O Gerente"
MusicBossbotFactoryV1 = "Valsa do Cog"
MusicBossbotCeoV1 = "Rodeado de Chefes"
MusicPartyOriginalTheme = "Hora da Festa"
MusicPartyPolkaDance = "Polca de Festa"
MusicPartySwingDance = "Balanço de Festa"
MusicPartyWaltzDance = "Valsa de Festa" 
MusicPartyGenericThemeJazzy = "Jazz de Festa"
MusicPartyGenericTheme = "Jingle de Festa"


# JukeBoxGui
JukeboxAddSong = "Adicionar\nMúsica"
JukeboxReplaceSong = "Trocar\nMúsica"
JukeboxQueueLabel = "Tocar a Seguir:"
JukeboxSongsLabel = "Selecionar Música:"
JukeboxClose = "Pronto"
JukeboxCurrentlyPlaying = "Tocando Agora"
JukeboxCurrentlyPlayingNothing = "Jukebox em pausa."
JukeboxCurrentSongNothing = "Adicionar uma música à lista!"

PartyOverWarningNoName = "A festa acabou! Obrigado por ter vindo!"
PartyOverWarningWithName = "A festa %s de acabou! Obrigado por ter vindo!"
PartyCountdownClockText = "Tempo\n\nRestante"
PartyTitleText = "Festa de %s" # what you see when you enter a party

PartyActivityConjunction = ", e "
# Note : This dictionary is used to show the names of the activities in various
#        contexts.  If PartyGlobals.ActivityIds is changed, this list must be
#        updated with new indices.
PartyActivityNameDict = {
    0 : {
        "generic" : "Jukebox\n20 músicas",
        "invite" : "uma Jukebox de 20 músicas",
        "editor" : "Jukebox de 20",
        "description" : "Ouça música com sua própria jukebox de 20 músicas!"
    },
    1 : {
        "generic" : "Canhões de Festa",
        "invite" : "Canhões de Festa",
        "editor" : "Canhões",
        "description" : "Dispare você mesmo os canhões e divirta-se!"
    },
    2 : {
        "generic" : "Trampolim",
        "invite" : "Trampolim",
        "editor" : "Trampolim",
        "description" : "Pegue balinhas e salte o mais alto possível!"
    },
    3 : {
        "generic" : "Pescaria de Festa", 
        "invite" : "Pescaria de Festa",
        "editor" : "Pescaria de Festa",
        "description" : "Pegue as frutas para ganhar feijões! Desvie-se das bigornas!"
    },
    4 : {
        "generic" : "Pista de Dança\n10 passos",
        "invite" : "uma Pista de Dança com 10 passos",
        "editor" : "Pista de Dança de 10",
        "description" : "Mostre seus 10 passos de dança ao estilo toon!"
    },
    5 : {
        "generic" : "Cabo de Guerra de Festa",
        "invite" : "Cabo de Guerra de Festa",
        "editor" : "Cabo de Guerra",
        "description" : "Até 4 toons de cada lado puxando loucamente!"
    },
    6 : {
        "generic" : "Fogos de Artifício de Festa",
        "invite" : "Fogos de Artifício de Festa",
        "editor" : "Fogos de Artifício",
        "description" : "Lance seu próprio show de fogos de artifício!"
    },
    7 : {
        "generic" : "Relógio de Festa",
        "invite" : "um Relógio de Festa",
        "editor" : "Relógio de Festa",
        "description" : "Faça a contagem regressiva do tempo que resta de sua festa."
    },
    8 : {
        "generic" : "Jukebox\n40 músicas",
        "invite" : "uma Jukebox de 40 músicas",
        "editor" : "Jukebox de 40",
        "description" : "Ouça música com sua própria jukebox de 40 músicas!"
    },
    9 : {
        "generic" : "Pista de Dança\n20 passos",
        "invite" : "uma Pista de Dança de 20 passos",
        "editor" : "Pista de Dança de 20",
        "description" : "Mostre seus 20 passos de dança ao estilo toon!"
    },    
}

# Note : This dictionary is used to show the names of the decorations in various
#        contexts.  If PartyGlobals.DecorationIds is changed, this list must be
#        updated with new indices.
PartyDecorationNameDict = {
    0 : {
        "editor" : "Bigorna de Balões",
        "description" : "Tente evitar que a diversão acabe!",
    },
    1 : {
        "editor" : "Palco de Festa",
        "description" : "Balões, estrelas ou qualquer coisa que desejar",
    },
    2 : {
        "editor" : "Arco de Festa",
        "description" : "Torne a diversão envolvente!",
    },
    3 : {
        "editor" : "Bolo",
        "description" : "Delicioso.",
    },
    4 : {
        "editor" : "Castelo de Festa",
        "description" : "A casa de um Toon é seu castelo.",
    },
    5 : {
        "editor" : "Pilha de Presentes",
        "description" : "Presentes para todos os Toons!",
    },
    6 : {
        "editor" : "Língua de Sogra", 
        "description" : "Esse apito é muito estridente! Serpenteante!",
    },
    7 : {
        "editor" : "Portão de Festa",
        "description" : "Multicolorido e doidinho!",
    },
    8 : {
        "editor" : "Itens Barulhentos",
        "description" : "Piiiiiiiiiiii!",
    },
    9 : {
        "editor" : "Cata-vento",
        "description" : "Giros coloridos para todos!",
    },
    10 : {
        "editor" : "Globo Engraçado",
        "description" : "Globo engraçado e de estrelas criado por Olivea",
    },
    11 : {
        "editor" : "Faixa Feijão",
        "description" : "Uma faixa em forma de balinha criada por Cassidy",
    },
    12 : {
        "editor" : "Bolo Engraçado",
        "description" : "Um bolo engraçado e Caótico criado por Felícia",
    },
}

ActivityLabel = "Custo – Nome da Atividade"
PartyDoYouWantToPlan = "Deseja planejar uma nova festa agora?"
PartyPlannerOnYourWay = "Divirta-se planejando a sua festa!"
PartyPlannerMaybeNextTime = "Talvez da próxima vez.  Tenha um bom-dia!"
PartyPlannerHostingTooMany = "Desculpe, você só pode dar uma festa de cada vez."
PartyPlannerOnlyPaid = "Desculpe, só toons assinantes podem dar uma festa."
PartyPlannerNpcComingSoon = "Em breve surgirão mais festas! Tente novamente mais tarde."
PartyPlannerNpcMinCost = "O custo mínimo para planejar uma festa é de %d balinhas."

# Party Gates
PartyHatPublicPartyChoose = "deseja ir para a primeira festa pública disponível?"
PartyGateTitle = "Festas Públicas"
PartyGateGoToParty = "Ir para\nFesta!"
PartyGatePartiesListTitle = "Anfitriões"
PartyGatesPartiesListToons = "Toons"
PartyGatesPartiesListActivities = "Atividades"
PartyGatesPartiesListMinLeft = "Minutos Restantes"
PartyGateLeftSign = "Venha se Divertir!"
PartyGateRightSign = "Partes público aqui!"
PartyGateTitle = "Festas Públicas Aqui!"
PartyGatePartyUnavailable = "Desculpe. Essa festa não está mais disponível."
PartyGatePartyFull = "Desculpe. Essa festa está lotada."
PartyGateInstructions = 'Clique em um anfitrião e em "Ir para Festa"'

# DistributedPartyActivity.py
PartyActivityWaitingForOtherPlayers = "Aguardando outros jogadores para se juntarem à festa..."
PartyActivityPleaseWait = "Por favor, aguarde..."
DefaultPartyActivityTitle = "Título do Jogo de Festa"
DefaultPartyActivityInstructions = "Instruções do Jogo de Festa"
PartyOnlyHostLeverPull = "Apenas o anfitrião pode iniciar essa atividade. Desculpe."
PartyActivityDefaultJoinDeny = "Você não pode participar dessa atividade no momento. Desculpe."
PartyActivityDefaultExitDeny = "Você não pode sair dessa atividade no momento. Desculpe."

# JellybeanRewardGui.py
PartyJellybeanRewardOK = "OK"

# DistributedPartyCatchActivity.py
PartyCatchActivityTitle = "Atividade Pescaria de Festa"
PartyCatchActivityInstructions = "Pegue o máximo de peças de frutas que puder. Tente não 'pescar' quaisquer %(badThing)s!"
PartyCatchActivityFinishPerfect = "JOGO PERFEITO!"
PartyCatchActivityFinish = "Bom Jogo!"
PartyCatchActivityExit        = 'EXIT'
PartyCatchActivityApples      = 'maçãs'
PartyCatchActivityOranges     = 'laranjas'
PartyCatchActivityPears       = 'peras'
PartyCatchActivityCoconuts    = 'cocos'
PartyCatchActivityWatermelons = 'melancias'
PartyCatchActivityPineapples  = 'abacaxis'
PartyCatchActivityAnvils      = 'bigornas'
PartyCatchStarted = "O jogo começou. Divirta-se."
PartyCatchCannotStart = "O jogo não pode ser iniciado no momento."
PartyCatchRewardMessage = "Peças de frutas coletadas: %s\n\nBalinhas recebidas: %s"

# DistributedPartyDanceActivity.py
PartyDanceActivityTitle = "Pista de Dança de Festa"
PartyDanceActivityInstructions = "Combine 3 ou mais padrões de SETAS para fazer os passos de dança! Há 10 passos de dança disponíveis. Você consegue obter todos?"
PartyDanceActivity20Title = "Pista de Dança de festa"
PartyDanceActivity20Instructions = "Combine 3 ou mais padrões de SETAS para fazer os passos de dança! Há 20 passos de dança disponíveis. Você consegue obter todos?"

DanceAnimRight = "Direita"
DanceAnimReelNeutral = "O Toonpescador"
DanceAnimConked = "O Cabeçamole"
DanceAnimHappyDance = "A Dança Feliz"
DanceAnimConfused = "Vertigem Total"
DanceAnimWalk = "Andando na Lua"
DanceAnimJump = "O Salto!"
DanceAnimFirehose = "O Toonbombeiro"
DanceAnimShrug = "Quem Sabe?"
DanceAnimSlipForward = "A Queda"
DanceAnimSadWalk = "Exaustão"
DanceAnimWave = "Olá, Tchauzinho"
DanceAnimStruggle = "O Pulo Misto"
DanceAnimRunningJump = "O Toon Fugitivo"
DanceAnimSlipBackward = "A Queda de Costas"
DanceAnimDown = "A Descida"
DanceAnimUp = "A Subida"
DanceAnimGoodPutt = "A Tacada"
DanceAnimVictory = "A Dança da Vitória"
DanceAnimPush = "O Toonmímico"
DanceAnimAngry = "Rock'n'Roll"
DanceAnimLeft = "Esquerda"

# DistributedPartyCannonActivity.py
PartyCannonActivityTitle = "Canhões de Festa"
PartyCannonActivityInstructions = "Acerte as nuvens para mudar sua cor e ricochetear no ar! NO AR, você pode USAR AS SETAS para DESLIZAR."
PartyCannonResults = "Você recebeu %d balinhas!\n\nNuvens Atingidas: %d"

# DistributedPartyFireworksActivity.py
FireworksActivityInstructions = "Pressione a tecla \"Page Up\" para visualizar melhor."
FireworksActivityBeginning = "Os fogos de artifício de festa vão ser lançados! Curta o espetáculo!"
FireworksActivityEnding = "Espero que tenha gostado do espetáculo!"
PartyFireworksAlreadyActive = "O espetáculo de fogos de artifício já começou."
PartyFireworksAlreadyDone = "O espetáculo de fogos de artifício acabou."

# DistributedPartyTrampolineActivity.py
PartyTrampolineJellyBeanTitle = "Trampolim de Balinhas"
PartyTrampolineTricksTitle = "Trampolim de Acrobacias"
PartyTrampolineActivityInstructions = "Use a tecla Control para saltar.\n\nSalte quando seu Toon estiver no ponto mais baixo do trampolim para ir bem alto."
PartyTrampolineActivityOccupied = "O trampolim está sendo usado."
PartyTrampolineQuitEarlyButton = "Saltar"
PartyTrampolineBeanResults = "Você recebeu %d balinhas."
PartyTrampolineBonusBeanResults = "Você recebeu %d balinhas, além de mais %d por conseguir o Big Bean (Grande Feijão)."
PartyTrampolineTopHeightResults = "Seu recorde de altura foi %d ft (mt)."
PartyTrampolineTimesUp = "Acabou o Tempo"
PartyTrampolineReady = "Preparar..."
PartyTrampolineGo = "Já!"
PartyTrampolineBestHeight = "Recorde de Altura Até Agora:\n%s\n%d ft (mt)"
PartyTrampolineNoHeightYet = "Quão alto\nvocê pode saltar?"

# DistributedPartyTugOfWarActivity.py
PartyTugOfWarJoinDenied = "Desculpe. Você não pode participar do cabo de guerra no momento."
PartyTugOfWarTeamFull = "Desculpe. Essa equipe já está completa."
PartyTrampolineQuitEarlyButton = "Saltar"
PartyTugOfWarExitButton = "Sair"
PartyTugOfWarWaitingForMore = "Aguardando mais jogadores" # extra spaces on purpose given the blocky font
PartyTugOfWarWaitingToStart = "Aguardando para começar"
PartyTugOfWarWaitingForOtherPlayers = "Aguardando outros jogadores"
PartyTugOfWarReady = "Preparar..."
PartyTugOfWarGo = "JÁ!"
PartyTugOfWarGameEnd = "Bom jogo!"
PartyTugOfWarGameTie = "Você empatou!"
PartyTugOfWarRewardMessage = "você conseguiu %d balinhas. Bom trabalho!"
PartyTugOfWarTitle = "Cabo de Guerra de Festa"

# CalendarGuiMonth.py
CalendarShowAll = "Exibir Tudo"
CalendarShowOnlyHolidays = "Exibir Apenas Feriados"
CalendarShowOnlyParties = "Exibir Apenas Feriados"

# CalendarGuiDay.py
CalendarEndsAt = "Termina em "
CalendarStartedOn = "Iniciada em "
CalendarEndDash = "Final-"
CalendarEndOf = "Final de "
CalendarPartyGetReady = "Prepare-se!"
CalendarPartyGo = "Festejar!"
CalendarPartyFinished = "Acabou..."
CalendarPartyCancelled = "Cancelado."
CalendarPartyNeverStarted = "Nunca Aconteceu."

# NPCFriendPanel.py
NPCFriendPanelRemaining = "Restantes %s"

# PartiesPage.py
PartiesPageTitle = ""
PartiesPageHostTab = ""
PartiesPageInvitedTab = ""
PartiesPageTitleHost = ""
PartiesPageTitleInvited = ""

# MapPage.py
MapPageTitle = "Mapa"
MapPageBackToPlayground = "Voltar para o pátio"
MapPageBackToCogHQ = "Voltar para o Quartel de Cogs"
MapPageGoHome = "Ir para casa"
# hood name, street name
MapPageYouAreHere = "Você está em: %s %s"
MapPageYouAreAtHome = "Você está em\nsua propriedade"
MapPageYouAreAtSomeonesHome = "Você está na propriedade de %s"
MapPageGoTo = "Ir para\n%s"

# OptionsPage.py
OptionsPageTitle = "Opções"
OptionsPagePurchase = "Assine já!"
OptionsPageLogout = "Sair"
OptionsPageExitToontown = "Sair de Toontown"
OptionsPageMusicOnLabel = "A música está ligada."
OptionsPageMusicOffLabel = "A música está desligada."
OptionsPageSFXOnLabel = "Os efeitos sonoros estão ligados."
OptionsPageSFXOffLabel = "Os efeitos sonoros estão desligados."
OptionsPageToonChatSoundsOnLabel = "   Type Chat Sounds are on."
OptionsPageToonChatSoundsOffLabel = "   Type Chat Sounds are off."
OptionsPageFriendsEnabledLabel = "Aceito fazer novas amizades."
OptionsPageFriendsDisabledLabel = "Não aceito fazer amizades."
OptionsPageSpeedChatStyleLabel = "Cor do Chat rápido"
OptionsPageDisplayWindowed = "com janela"
OptionsPageSelect = "Selecionar"
OptionsPageToggleOn = "Ligar"
OptionsPageToggleOff = "Desligar"
OptionsPageChange = "Alterar"
OptionsPageDisplaySettings = "Vídeo: %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Vídeo: %(screensize)s"
OptionsPageExitConfirm = "Sair de Toontown?"

DisplaySettingsTitle = "Configurações de vídeo"
DisplaySettingsIntro = "As configurações a seguir são usadas para determinar a maneira como Toontown é exibida em seu computador. Provavelmente, não será necessário ajustá-las, a menos que você esteja tendo algum problema."
DisplaySettingsIntroSimple = "Você pode ajustar a resolução da tela com um valor maior para melhorar o contraste do texto e dos gráficos em Toontown, mas, dependendo da placa de vídeo do seu computador, alguns valores mais altos podem fazer que o jogo fique lento ou trave."

DisplaySettingsApi = "API de gráfico:"
DisplaySettingsResolution = "Resolução:"
DisplaySettingsWindowed = "Em uma janela"
DisplaySettingsFullscreen = "Tela cheia"
DisplaySettingsApply = "Aplicar"
DisplaySettingsCancel = lCancel
DisplaySettingsApplyWarning = "Quando você pressionar OK, as configurações de vídeo serão alteradas. Se a nova configuração não ficar adequada em seu computador, o vídeo retornará à configuração original após %s segundos."
DisplaySettingsAccept = "Pressione em OK para manter as novas configurações, ou em Cancelar para voltar às anteriores. Se você não pressionar nada, as configurações voltarão em %s segundos automaticamente aos valores anteriores."
DisplaySettingsRevertUser = "As configurações de vídeo anteriores foram restauradas."
DisplaySettingsRevertFailed = "As configurações de vídeo selecionadas não funcionam em seu computador. As configurações de vídeo anteriores foram restauradas."

# TrackPage.py
TrackPageTitle = "Treinamento de tipos de piadas"
TrackPageShortTitle = "Treinamento de piadas"
TrackPageSubtitle = "Execute as Tarefas Toon para aprender a usar novas piadas!"
TrackPageTraining = "Você está treinando para usar as Piadas de %s.\nQuando executar todas as 16 tarefas,\nestará apto a usar as Piadas de %s nas batalhas."
TrackPageClear = "Você não está treinando nenhum tipo de piadas agora."
TrackPageFilmTitle = "Filme de\ntreinamento\nde %s"
TrackPageDone = "FIM"

# QuestPage.py
QuestPageToonTasks = "Tarefas Toon"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageDelivery = "%s\nPara: %s\n  %s\n  %s\n  %s\n\nDe: %s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageVisit = "%s %s\n  %s\n  %s\n  %s\n\nDe: %s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName
# Choose between trackA and trackB.
#
# To choose, go see:
#   Flippy
#   Town Hall
#   Playground
#   Toontown Central
#QuestPageTrackChoice = "%s\n\nPara escolher, selecione:\n  %s\n  %s\n  %s\n  %s"
# questName, npcName, buildingName, streetName, locationName
QuestPageChoose = "Escolha"
QuestPageLocked = "Travado"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = lHQOfficerM
QuestPosterHQBuildingName = lToonHQ
QuestPosterHQStreetName = "Qualquer rua"
QuestPosterHQLocationName = "Qualquer bairro"

QuestPosterTailor = "Costureiro"
QuestPosterTailorBuildingName = "Loja de Roupas"
QuestPosterTailorStreetName = "Qualquer pátio"
QuestPosterTailorLocationName = "Qualquer bairro"
QuestPosterPlayground = "No pátio"
QuestPosterAtHome = "Na "+lMyEstate
QuestPosterInHome = "Em "+lMyEstate
QuestPosterOnPhone = "No seu telefone"
QuestPosterEstate = "Na sua propriedade"
QuestPosterAnywhere = "Qualquer lugar"
QuestPosterAuxTo = "para:"
QuestPosterAuxFrom = "de:"
QuestPosterAuxFor = "para:"
QuestPosterAuxOr = "ou:"
QuestPosterAuxReturnTo = "Retornar\npara:"
QuestPosterLocationIn = ""
QuestPosterLocationOn = ""
QuestPosterFun = "Só de brincadeira!"
QuestPosterFishing = "IR PESCAR"
QuestPosterComplete = "CONCLUIR"

# ShardPage.py
ShardPageTitle = "Regiões"
ShardPageHelpIntro = "Cada Região é uma cópia do mundo de Toontown."
ShardPageHelpWhere = " Você está agora na Região \"%s\"."
ShardPageHelpWelcomeValley = " Você está agora na Região \"Vale Boas-vindas\", em \"%s\"."
ShardPageHelpMove = " Para ir até uma nova Região, clique no nome dela."

ShardPagePopulationTotal = "População Total de Toontown:\n%d"
ShardPageScrollTitle = "Nome População"
ShardPageLow = "Tranquila"
ShardPageMed = "Inteligente"
ShardPageHigh = "Lotada"
ShardPageChoiceReject = "Desculpe, essa Região está lotada. Por favor, tente outra."

# SuitPage.py
SuitPageTitle = "Galeria de Cogs"
SuitPageMystery = DialogQuestion + DialogQuestion + DialogQuestion
SuitPageQuota = "%s de %s"
SuitPageCogRadar = "%s presentes"
SuitPageBuildingRadarS = "%s edifício"
SuitPageBuildingRadarP = "%s edifícios"

# DisguisePage.py
DisguisePageTitle = Cog + "Disfarce"
DisguisePageMeritAlert = "Pronto para a\npromoção!"
DisguisePageCogLevel = "Nível %s"
DisguisePageMeritFull = "Completo"

# FishPage.py
FishPageTitle = "Pescaria"
FishPageTitleTank = "Balde de peixes"
FishPageTitleCollection = "Álbum de peixes"
FishPageTitleTrophy = "Troféus de pesca"
FishPageWeightStr = "Peso: "
FishPageWeightLargeS = "%d Kg "
FishPageWeightLargeP = "%d Kg "
FishPageWeightSmallS = "%d g"
FishPageWeightSmallP = "%d g"
FishPageWeightConversion = 16
FishPageValueS = "Valor: %d balinha"
FishPageValueP = "Valor: %d balinhas"
FishPageCollectedTotal = "Espécies de peixes recolhidas: %d de %d"
FishPageRodInfo = "Vara %s\n%d - %d quilos"
FishPageTankTab = "Balde"
FishPageCollectionTab = "Álbum"
FishPageTrophyTab = "Troféus"

FishPickerTotalValue = "Balde: %s / %s\nValor: %d balinhas"

UnknownFish = DialogQuestion + DialogQuestion + DialogQuestion

FishingRod = "Vara %s"
FishingRodNameDict = {
    0 : "Vareta",
    1 : "Bambu",
    2 : "Madeira de lei",
    3 : "Aço",
    4 : "Dourado",
    }
FishTrophyNameDict = {
    0 : "Peixinhozinho",
    1 : "Peixinho",
    2 : "Peixe",
    3 : "Peixe-voador",
    4 : "Tubarão",
    5 : "Peixe-espada",
    6 : "Baleia assassina",
    }

# GardenPage.py
GardenPageTitle = "Jardinagem"
GardenPageTitleBasket = "Cesto de Flores"
GardenPageTitleCollection = "Álbum de Flores"
GardenPageTitleTrophy = "Troféus de Jardinagem"
GardenPageTitleSpecials = "Especiais de Jardinagem"
GardenPageBasketTab = "Cesto"
GardenPageCollectionTab = "Álbum"
GardenPageTrophyTab = "Troféus"
GardenPageSpecialsTab = "Especiais"
GardenPageCollectedTotal = "Variedades de Flores Colecionadas: %d de %d"
GardenPageValueS = "Valor: %d balinha"
GardenPageValueP = "Valor: %d balinhas"
FlowerPickerTotalValue = "Cesto: %s / %s\nValor: %d balinhas"
GardenPageShovelInfo = "%s Pá: %d / %d\n"
GardenPageWateringCanInfo = "%s Regador: %d / %d"

# KartPage.py
KartPageTitle = "Karts"
KartPageTitleCustomize = "Personalizador de karts"
KartPageTitleRecords = "Melhores recordes pessoais"
KartPageTitleTrophy = "Troféus de corridas"
KartPageCustomizeTab = "Personalizar"
KartPageRecordsTab = "Recordes"
KartPageTrophyTab = "Troféus"
KartPageTrophyDetail = "Troféus %s : %s"
KartPageTickets = "Bilhetes :"
KartPageConfirmDelete = "Excluir acessório?"

#plural
KartShtikerDelete = "Excluir"
KartShtikerSelect = "Selecionar uma categoria"
KartShtikerNoAccessories = "Não possui acessórios"
KartShtikerBodyColors = "Cores de karts"
KartShtikerAccColors = "Cores de acessórios"
KartShtikerEngineBlocks = "Acessórios de capô"
KartShtikerSpoilers = "Acessórios de mala"
KartShtikerFrontWheelWells = "Acessórios de roda dianteira"
KartShtikerBackWheelWells = "Acessórios de roda traseira"
KartShtikerRims = "Acessórios de aro"
KartShtikerDecals = "Acessórios de decalque"
#singluar
KartShtikerBodyColor = "Cor do kart"
KartShtikerAccColor = "Cor do acessório"
KartShtikerEngineBlock = "Capô"
KartShtikerSpoiler = "Mala"
KartShtikerFrontWheelWell = "Roda dianteira"
KartShtikerBackWheelWell = "Roda traseira"
KartShtikerRim = "Aro"
KartShtikerDecal = "Decalque"

KartShtikerDefault = "Padrão %s"
KartShtikerNo = "Nenhum acessório %s"

# QuestChoiceGui.py
QuestChoiceGuiCancel = lCancel

# TrackChoiceGui.py
TrackChoiceGuiChoose = "Escolher"
TrackChoiceGuiCancel = lCancel
TrackChoiceGuiHEAL = 'Toonar permite que você cure outros Toons que estão na batalha.'
TrackChoiceGuiTRAP = 'Armadilhas são piadas poderosas que devem ser usadas com Iscas.'
TrackChoiceGuiLURE = 'Use Iscas para abalar os Cogs ou faça-os cair em armadilhas.'
TrackChoiceGuiSOUND = 'As piadas Sonoras afetam todos os Cogs, mas não são muito poderosas.'
TrackChoiceGuiDROP = "As piadas Cadentes fazem muitos estragos, mas não são muito precisas."

# EmotePage.py
EmotePageTitle = "Expressões / Emoções"
EmotePageDance = "Você montou a seguinte sequência de dança:"
EmoteJump = "Saltitante"
EmoteDance = "Dançante"
EmoteHappy = "Feliz"
EmoteSad = "Triste"
EmoteAnnoyed = "Aborrecido"
EmoteSleep = "Sonolento"

# TIP Page
TIPPageTitle = "DICA"

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nNível %(level)s"

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "Você não pode sair do parque até que o seu Risômetro esteja sorrindo!"

# InventoryNew.py
InventoryTotalGags = "Total de piadas\n%d / %d"
InventroyPinkSlips = "%s Bilhetes Azuis"
InventroyPinkSlip = "1 Bilhete Azul"
InventoryDelete = "EXCLUIR"
InventoryDone = "OK"
InventoryDeleteHelp = "Clique em uma piada para EXCLUIR."
InventorySkillCredit = "Crédito de habilidades:\n%s"
InventorySkillCreditNone = "Crédito de habilidades:\nNenhum"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Precisão: %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryUberTrackExp = "Faltam %(nextExp)s!"
InventoryGuestExp = "Limite de Visitantes"
GuestLostExp = " Acima do Limite de Visitantes"
InventoryAffectsOneCog = "Afeta: Um "+ Cog
InventoryAffectsOneToon = "Afeta: Um Toon"
InventoryAffectsAllToons = "Afeta: Todos os Toons"
InventoryAffectsAllCogs = "Afeta: Todos os "+ Cogs
InventoryHealString = "Toonar"
InventoryDamageString = "Dano"
InventoryBattleMenu = "MENU DE BATALHA"
InventoryRun = "CORRER"
InventorySOS = "SOS"
InventoryPass = "PASSAR"
InventoryFire = "Fogo"
InventoryClickToAttack = "Clique em uma\npiada para\natacar"
InventoryDamageBonus = "(+%d)"

# NPCForceAcknowledge.py
NPCForceAcknowledgeMessage = "Você deve pegar o bondinho antes de sair.\n\n\n\n\nVocê poderá encontrar o bondinho ao lado da Loja de Piadas do Pateta."
NPCForceAcknowledgeMessage2 = "Muito bem! Você completou a busca pelo bondinho!\nVisite o Quartel dos Toons para solicitar a sua recompensa.\n\n\n\n\n\nO Quartel dos Toons localiza-se próximo ao centro do pátio."
NPCForceAcknowledgeMessage3 = "Lembre-se de pegar o bondinho.\n\n\n\nVocê pode encontrar o bondinho ao lado da Loja de Piadas do Pateta."
NPCForceAcknowledgeMessage4 = "Parabéns! Você concluiu a sua primeira Tarefa Toon!\n\n\n\n\n\nVisite o Quartel dos Toons para solicitar a sua recompensa."
NPCForceAcknowledgeMessage5 = "Não se esqueça de sua Tarefa Toon!\n\n\n\n\n\n\n\n\n\n\nVocê pode encontrar Cogs para serem derrotados do outro lado de túneis como este."
NPCForceAcknowledgeMessage6 = "Excelente trabalho derrotando esses Cogs!\n\n\n\n\n\n\n\n\nVolte para o Quartel dos Toons o mais rápido possível."
NPCForceAcknowledgeMessage7 = "Não se esqueça de fazer um amigo!\n\n\n\n\n\n\nClique em outro jogador e use o botão Novo amigo."
NPCForceAcknowledgeMessage8 = "Ótimo! Você fez um novo amigo!\n\n\n\n\n\n\n\n\nAgora, você deve voltar para o Quartel dos Toons."
NPCForceAcknowledgeMessage9 = "Bom trabalho usando o telefone!\n\n\n\n\n\n\n\n\nVolte para o Quartel dos Toons para pedir a sua recompensa."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "Você recebeu 1 ponto de Lançamento! Quando você obtém 10, ganha uma nova piada!"
MovieTutorialReward2 = "Você recebeu 1 ponto de Esguicho! Quando você obtém 10, ganha uma nova piada!"
MovieTutorialReward3 = "Muito bom! Você concluiu a sua primeira Tarefa Toon!"
MovieTutorialReward4 = "Vá para o Quartel dos Toons para pegar a sua recompensa!"
MovieTutorialReward5 = "Divirta-se!"

# ToontownBattleGlobals.py
BattleGlobalTracks = ['toonar', 'armadilha', 'isca', 'sonora', 'lançamento', 'esguicho', 'cadente']
BattleGlobalNPCTracks = ['reabastecer', 'toons atingidos', 'cogs não-atingidos']
BattleGlobalAvPropStrings = (
    ('Pena', 'Megafone', 'Batom', 'Bengala', 'Pó mágico', 'Bolinhas de malabarismo', 'Mergulho Elevado'),
    ('Casca de banana', 'Ancinho', 'Bolas de gude', 'Areia movediça', 'Alçapão', 'TNT', 'Estrada De Ferro'),
    ('Nota de $1', 'Ímã pequeno', 'Nota de $5', 'Ímã grande', 'Nota de $10', 'Óculos hipnóticos', 'Presentação'),
    ('Buzina de bicicleta', 'Apito', 'Trombeta', 'Foooonnnn!', 'Tromba de elefante', 'Buzina', 'Cantor de Ópera'),
    ('Bolinho', 'Fatia de torta de frutas', 'Fatia de torta de creme', 'Torta de frutas inteira', 'Torta de creme inteira', 'Bolo de aniversário', 'Bolo de Casamento'),
    ('Flor com esguicho', 'Copo d\'água', 'Revólver de água', 'Garrafa de água com gás', 'Mangueira de incêndio', 'Nuvem de chuva', 'Gêiser'),
    ('Vaso de flor', 'Saco de areia', 'Bigorna', 'Peso pesado', 'Cofre', 'Piano de cauda', 'Toontanic')
    )
BattleGlobalAvPropStringsSingular = (
    ('uma Pena', 'um Megafone', 'um Batom', 'uma Bengala', 'um Pó mágico', 'um conjunto de Bolinhas de malabarismo', 'um Mergulho Elevado'),
    ('uma Casca de banana', 'um Ancinho', 'um conjunto de Bolas de gude', 'uma poça de Areia movediça', 'um Alçapão', 'um TNT', 'uma Estrada de Ferro'),
    ('uma Nota de $1', 'um Ímã pequeno', 'uma Nota de $5', 'um Ímã grande', 'uma Nota de $10', 'um par de Óculos hipnóticos', 'uma Presentação'),
    ('uma Buzina de bicicleta', 'um Apito', 'uma Trombeta', 'um Foooonnnn!', 'uma Tromba de elefante', 'uma Buzina', 'um Cantor de Ópera'),
    ('um Bolinho', 'uma Fatia de torta de frutas', 'uma Fatia de torta de creme', 'uma Torta de frutas inteira', 'uma Torta de creme inteira', 'um Bolo de Casamento'),
    ('uma Flor com esguicho', 'um Copo d\'água', 'um Revólver de água', 'uma Garrafa de água com gás', 'uma Mangueira de incêndio', 'uma Nuvem de chuva', 'um Gêiser'),
    ('um Vaso de flor', 'um Saco de areia', 'uma Bigorna', 'um Peso pesado', 'um Cofre', 'um Piano de cauda', 'the Toontanic')
    )
BattleGlobalAvPropStringsPlural = (
    ('Penas', 'Megafones', 'Batons', 'Bengalas', 'Pós mágicos', 'conjuntos de Bolinhas de malabarismo', 'Mergulhos Elevados'),
    ('Cascas de banana', 'Ancinhos', 'conjuntos de Bolas de gude', 'poças de Areia movediça', 'Alçapões','TNTs', 'Estradas de Ferro'),
    ('Notas de $1', 'Ímãs pequenos', 'Contas de $5', 'Ímãs grandes','Contas de $10', 'par de Óculos hipnóticos', 'Presentação'),
    ('Buzinas de bicicleta', 'Apitos', 'Trombetas', 'Foooonnnns!', 'Trombas de elefante', 'Buzinas', 'Cantor de Ópera'),
    ('Bolinhos', 'Fatias de torta de frutas', 'Fatias de torta de creme','Tortas de frutas inteiras', 'Tortas de creme inteiras', 'Bolos de aniversário', 'Bolo de Casamento'),
    ('Flores com esguicho', 'Copos d\'água', 'Revólveres de água','Garrafas de água com gás', 'Mangueiras de incêndio', 'Nuvens de chuva', 'Gêiser'),
    ('Vasos de flor', 'Sacos de areia', 'Bigornas', 'Pesos pesados', 'Cofres','Pianos de cauda', 'Transatlânticos')
    )
BattleGlobalAvTrackAccStrings = ("Médio", "Perfeito", "Baixo", "Alto", "Médio", "Alto", "Baixo")
BattleGlobalLureAccLow = "Baixo"
BattleGlobalLureAccMedium = "Médio"

AttackMissed = "PERDEU"

NPCCallButtonLabel = 'CHAMAR'

# ToontownLoader.py
LoaderLabel = "Carregando..."

# PlayGame.py
HeadingToHood = "Indo %(to)s %(hood)s..." # hood name
HeadingToYourEstate = "Indo para a sua propriedade..."
HeadingToEstate = "Indo para a propriedade de %s..."  # avatar name
HeadingToFriend = "Indo para a propriedade do amigo de %s..."  # avatar name

# Hood.py
HeadingToPlayground = "Indo para o Pátio..."
HeadingToStreet = "Indo %(to)s %(street)s..." # Street name

# TownBattle.py
TownBattleRun = "Voltar correndo para o pátio?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "QUAL TOON?"
TownBattleChooseAvatarCogTitle = "QUAL " + string.upper(Cog) + "?"
TownBattleChooseAvatarBack = "VOLTAR"

#firecogpanel
FireCogTitle = "BILHETES AZUIS RESTANTES:%s\nQUAL COG DEMITIR?"
FireCogLowTitle = "BILHETES AZUIS RESTANTES:%s\nSEM BILHETES SUFICIENTES!"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "Não há amigos para chamar!"
TownBattleSOSWhichFriend = "Chamar qual amigo?"
TownBattleSOSNPCFriends = "Toons resgatados"
TownBattleSOSBack = "VOLTAR"

# TownBattleToonPanel.py
TownBattleToonSOS = "SOS"
TownBattleToonFire = "Disparar"
TownBattleUndecided = "?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "Aguardando\noutros jogadores..."
TownSoloBattleWaitTitle = "Aguarde..."
TownBattleWaitBack = "VOLTAR"

# TownBattleSOSPetSearchPanel.py
TownBattleSOSPetSearchTitle = "Procurando rabisco\n%s..."

# TownBattleSOSPetInfoPanel.py
TownBattleSOSPetInfoTitle = "%s está %s"
TownBattleSOSPetInfoOK = lOK

# Trolley.py
TrolleyHFAMessage = "Você não pode embarcar no bondinho até que o seu Risômetro esteja sorrindo."
TrolleyTFAMessage = "\Você não pode embarcar no bondinho até que o " + Mickey +" permita."
TrolleyHopOff = "Descer"

# DistributedFishingSpot.py
FishingExit = "Sair"
FishingCast = "Lançar"
FishingAutoReel = "Molinete automático"
FishingItemFound = "Você pegou:"
FishingCrankTooSlow = "Muito\ndevagar"
FishingCrankTooFast = "Muito\nrápido"
FishingFailure = "Você não pegou nada!"
FishingFailureTooSoon = "Não comece a rebobinar a linha até que você veja uma pequena mordida. Espere a bóia balançar para cima e para baixo rapidamente!"
FishingFailureTooLate = "Rebobine a linha enquanto o peixe ainda está mordendo a isca!"
FishingFailureAutoReel = "O molinete automático não funcionou desta vez. Gire a manivela manualmente, na velocidade certa, para ter mais chance de pegar alguma coisa!"
FishingFailureTooSlow = "Você girou a manivela muito devagar. Alguns peixes são mais rápidos do que outros. Tente manter a barra de velocidade centralizada!"
FishingFailureTooFast = "Você girou a manivela muito rápido. Alguns peixes são mais lentos do que outros. Tente manter a barra de velocidade centralizada!"
FishingOverTankLimit = "O seu balde de pesca está cheio. Vá vender os seus peixes para o Vendedor da Loja de Animais e volte."
FishingBroke = "Você não tem mais balinhas para as iscas! Para ganhar mais balinhas, pegue o bondinho ou venda os peixes para os Vendedores da Loja de Animais."
FishingHowToFirstTime = "Clique e arraste para baixo no botão Lançar. Quanto mais baixo você arrastar, mais forte será o lançamento. Ajuste o ângulo para acertar os alvos dos peixes.\n\nTente agora!"
FishingHowToFailed = "Clique e arraste para baixo no botão Lançar. Quanto mais baixo você arrastar, mais forte será o lançamento. Ajuste o ângulo para acertar os alvos dos peixes.\n\nTente agora de novo!"
FishingBootItem = "Bota velha"
FishingJellybeanItem = "%s balinhas"
FishingNewEntry = "Novas espécies!"
FishingNewRecord = "Novo recorde!"

# FishPoker
FishPokerCashIn = "Morrer\n%s\n%s"
FishPokerLock = "Bloquear"
FishPokerUnlock = "Desbloquear"
FishPoker5OfKind = "5 de um naipe"
FishPoker4OfKind = "4 de um naipe"
FishPokerFullHouse = "Full House"
FishPoker3OfKind = "3 de um naipe"
FishPoker2Pair = "2 pares"
FishPokerPair = "Par"

# DistributedTutorial.py
TutorialGreeting1 = "Oi %s!"
TutorialGreeting2 = "Oi %s!\nVem cá!"
TutorialGreeting3 = "Oi %s!\nVem cá!\nUse as teclas de seta!"
TutorialMickeyWelcome = "Bem-vindo a Toontown!"
TutorialFlippyIntro = "Deixe-me apresentar você ao meu amigo "+ Flippy +"..."
TutorialFlippyHi = "Oi, %s!"
TutorialQT1 = "Você pode conversar usando isto."
TutorialQT2 = "Você pode conversar usando isto.\nClique no item e escolha \"Oi\"."
TutorialChat1 = "Você pode conversar usando qualquer um destes botões."
TutorialChat2 = "O botão azul permite que você converse usando o teclado."
TutorialChat3 = "Cuidado! A maior parte dos outros jogadores não entenderá o que você está dizendo se usar o teclado."
TutorialChat4 = "O botão verde abre o %s."
TutorialChat5 = "Todos entenderão se você usar o %s."
TutorialChat6 = "Tente dizer \"Oi\"."
TutorialBodyClick1 = "Muito bem!"
TutorialBodyClick2 = "Muito prazer! Quer ser meu amigo?"
TutorialBodyClick3 = "Para fazer amizade com "+ Flippy +", clique nele..."
TutorialHandleBodyClickSuccess = "Muito bom!"
TutorialHandleBodyClickFail = "Não é assim. Tente clicar em cima do "+ Flippy +"..."
TutorialFriendsButton = "Agora, clique no botão 'Amigos' abaixo da figura do "+ Flippy +" no canto direito."
TutorialHandleFriendsButton = "Em seguida, clique no botão 'Sim'.."
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = "Você quer fazer amizade com o "+ Flippy +"?"
TutorialFriendsPanelMickeyChat = Flippy + " aceitou ser seu amigo. Clique em 'Ok' para concluir."
TutorialFriendsPanelYes = Flippy + " disse sim!"
TutorialFriendsPanelNo = "Isso não foi muito simpático!"
TutorialFriendsPanelCongrats = "Parabéns! Você fez seu primeiro amigo."
TutorialFlippyChat1 = "Venha me ver quando estiver pronto para a sua primeira Tarefa Toon!"
TutorialFlippyChat2 = "Estarei na PrefeiToona!"
TutorialAllFriendsButton = "Você pode ver todos os seus amigos clicando no botão Amigos. Experimente..."
TutorialEmptyFriendsList = "No momento, a sua lista está vazia porque o "+ Flippy +" não é um jogador real."
TutorialCloseFriendsList = "Clique no botão 'Fechar'\npara fazer que a\nlista desapareça"
TutorialShtickerButton = "O botão do canto direito inferior abre o seu Álbum Toon. Experimente..."
TutorialBook1 = "O álbum contém várias informações úteis, como este mapa de Toontown."
TutorialBook2 = "Você também pode verificar o andamento de suas Tarefas Toon."
TutorialBook3 = "Quando você estiver pronto, clique no botão do álbum novamente, para fechá-lo"
TutorialLaffMeter1 = "Você também precisará disto..."
TutorialLaffMeter2 = "Você também precisará disto...\nÉ o seu Risômetro."
TutorialLaffMeter3 = "Quando os "+ Cogs +" atacarem você, ele diminui."
TutorialLaffMeter4 = "Quando você está em pátios como este, ele volta a subir."
TutorialLaffMeter5 = "Quando concluir as Tarefas Toon, você obterá recompensas, como o aumento do seu Limite de risadas."
TutorialLaffMeter6 = "Cuidado! Se os "+ Cogs +" derrotarem você, perderá todas as suas piadas."
TutorialLaffMeter7 = "Para obter mais piadas, divirta-se com os jogos no bondinho."
TutorialTrolley1 = "Siga-me até o bondinho!"
TutorialTrolley2 = "Pule nele!"
TutorialBye1 = "Brinque com alguns jogos!"
TutorialBye2 = "Divirta-se com alguns jogos!\nCompre algumas piadas!"
TutorialBye3 = "\Vá encontrar o  "+ Flippy +" quando terminar!"# TutorialForceAcknowledge.py

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "\Você está indo na direção errada! \Vá encontrar o  "+ Mickey +"!"# SpeedChat

PetTutorialTitle1 = "O Painel dos Rabiscos"
PetTutorialTitle2 = "Chat rápido dos Rabiscos"
PetTutorialTitle3 = "Gadálogo dos Rabiscos"
PetTutorialNext = "Próxima Página"
PetTutorialPrev = "Página Anterior"
PetTutorialDone = lOK
PetTutorialPage1 = "Clique em um Rabisco para exibir o painel de Rabiscos. Daqui, você pode alimentar, coçar e chamar o Rabisco."
PetTutorialPage2 = "Use a nova área 'Bichinhos' no menu Chat rápido para fazer com que um Rabisco faça um truque. Se ele fizer, recompense-o para ele melhorar ainda mais!"
PetTutorialPage3 = "Compre novos truques de Rabiscos no Gadálogo da Clarabela. Truques melhores produzem Toonar melhores!"
def getPetGuiAlign():
	from pandac.PandaModules import TextNode
	return TextNode.ACenter

GardenTutorialTitle1 = "Jardinagem"
GardenTutorialTitle2 = "Flores"
GardenTutorialTitle3 = "Árvores"
GardenTutorialTitle4 = "Instruções"
GardenTutorialTitle5 = "Estátuas"
GardenTutorialNext = "Próxima Página"
GardenTutorialPrev = "Página Anterior"
GardenTutorialDone = lOK
GardenTutorialPage1 = "Crie o seu próprio jardim botânico!  Você pode plantar flores e árvores, e até erguer estátuas."
GardenTutorialPage2 = "As flores são sensíveis, e você precisa descobrir as suas receitas de balinhas.  Plante todos os tipos para melhorar as risadas, e venda as flores para ganhar balinhas."
GardenTutorialPage3 = "Use uma piada para plantar uma árvore.  Alguns dias depois, essa piada vai melhorar!!  Mas cuide bem da saúde dela, ou a melhoria se vai."
GardenTutorialPage4 = "Para plantar, regar, cavar ou fazer a colheita no seu jardim, ande até estes locais."
GardenTutorialPage5 = "Estátuas podem ser compradas no Catálogo da Clarabela. Aumenta suas habilidades para destravar as estátuas mais extravagantes."

# Playground.py
PlaygroundDeathAckMessage = "Os" + Cogs + " levaram todas as suas piadas!\n\nVocê está triste. Você não pode sair do pátio até ficar feliz."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "O Supervisor da fábrica foi derrotado antes de você alcançá-lo. Você não recuperou nenhuma parte do Cog."

# MintInterior
ForcedLeaveMintAckMsg = "O Supervisor do Andar da Casa da Moeda foi derrotado antes de você alcançá-lo. Você não recuperou nenhuma Grana Cog."

# DistributedFactory.py
HeadingToFactoryTitle = "Dirigindo-se a %s..."
ForemanConfrontedMsg = "%s está lutando com o Supervisor da fábrica!"

# DistributedMint.py
MintBossConfrontedMsg = "%s está lutando com o Supervisor!"

# DistributedStage.py
StageBossConfrontedMsg = "%s está lutando com o Funcionário!"
stageToonEnterElevator = "%s \nentrou no elevador"
ForcedLeaveStageAckMsg = "O Funcionário da Lei foi derrotado antes de você alcançá-lo. Você não recuperou nenhum Aviso de Júri."

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "Aguardando outros jogadores..."
MinigamePleaseWait = "Aguarde..."
DefaultMinigameTitle = "Título do minijogo"
DefaultMinigameInstructions = "Instruções do minijogo"
HeadingToMinigameTitle = "Dirigindo-se a %s..." # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "Medidor de potência"
MinigamePowerMeterTooSlow = "Muito\ndevagar"
MinigamePowerMeterTooFast = "Muito\nrápido"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "Modelo de minijogo"
MinigameTemplateInstructions = "Este é um modelo de minijogo. Use-o para criar novos minijogos."

# DistributedCannonGame.py
CannonGameTitle = "Jogo do canhão"
CannonGameInstructions = "Atire o seu Toon na torre de água o mais rápido que puder. Use o mouse ou as teclas de seta para mirar o canhão. Seja rápido e ganhe uma grande recompensa para todos!"
CannonGameReward = "RECOMPENSA"

# DistributedTwoDGame.py
TwoDGameTitle = "Fuga dos Cartoons"
TwoDGameInstructions = "Fuja dos " + Cog + " o mais rápido que você puder. Use as setas para correr/pular e Ctrl para esguichar " + Cog + ". Colete " + Cog + " tesouros para ganhar mais pontos."
TwoDGameElevatorExit = "SAÍDA"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Cabo de guerra"
TugOfWarInstructions = "Toque alternadamente nas teclas de seta para a esquerda e para a direita rápido o suficiente para alinhar a barra verde com a linha vermelha. Não toque nelas muito devagar, ou você acabará na água!"
TugOfWarGameGo = "COMEÇAR!"
TugOfWarGameReady = "Pronto..."
TugOfWarGameEnd = "Bom jogo!"
TugOfWarGameTie = "Você empatou!"
TugOfWarPowerMeter = "Medidor"

# DistributedPatternGame.py
PatternGameTitle = "Acompanhe a "+ Minnie
PatternGameInstructions = "A " + Minnie + " mostrará uma sequência de dança." + \
                          "Tente repetir a dança da "+ Minnie +" exatamente como você vê usando as teclas de seta!"
PatternGameWatch   = "Observe estes passos de dança..."
PatternGameGo      = "COMEÇAR!"
PatternGameRight   = "Bom, %s!"
PatternGameWrong   = "Ops!"
PatternGamePerfect = "Perfeito, %s!"
PatternGameBye     = "Obrigado por jogar!"
PatternGameWaitingOtherPlayers = "Aguardando outros jogadores..."
PatternGamePleaseWait = "Aguarde..."
PatternGameFaster = "Você foi\nmais rápido!"
PatternGameFastest = "Você foi o\nmais rápido!"
PatternGameYouCanDoIt = "Deixa disso!\nVocê consegue!"
PatternGameOtherFaster = "\nfoi mais rápido!"
PatternGameOtherFastest = "\nfoi o mais rápido!"
PatternGameGreatJob = "Muito bom!"
PatternGameRound = "Rodada %s!" # Round 1! Round 2! ..
PatternGameImprov = "You did great!  Now Improv!"

# DistributedRaceGame.py
RaceGameTitle = "Jogo de corrida"
RaceGameInstructions = "Clique em um número. Escolha bem! Você só avançará se ninguém mais escolher o mesmo número."
RaceGameWaitingChoices = "Esperando os outros jogadores escolherem..."
RaceGameCardText = "%(name)s aposta: %(reward)s"
RaceGameCardTextBeans = "%(name)s recebe: %(reward)s"
RaceGameCardTextHi1 = "%(name)s é um Toon fabuloso!"  # this category might eventually have secret game hints, etc

# RaceGameGlobals.py
RaceGameForwardOneSpace    = " avança 1 espaço"
RaceGameForwardTwoSpaces   = " avança 2 espaços"
RaceGameForwardThreeSpaces = " avança 3 espaços"
RaceGameBackOneSpace    = " recua 1 espaço"
RaceGameBackTwoSpaces   = " recua 2 espaços"
RaceGameBackThreeSpaces = " recua 3 espaços"
RaceGameOthersForwardThree = " todos os outros avançam \n3 espaços"
RaceGameOthersBackThree = "todos os outros recuam \n3 espaços"
RaceGameInstantWinner = "Vencedor imediato!"
RaceGameJellybeans2 = "2 balinhas"
RaceGameJellybeans4 = "4 balinhas"
RaceGameJellybeans10 = "10 balinhas!"

# DistributedRingGame.py
RingGameTitle = "Jogo dos anéis"
# color
RingGameInstructionsSinglePlayer = "Tente nadar através do número máximo de anéis %s que conseguir. Para nadar, use as teclas de seta."
# color
RingGameInstructionsMultiPlayer = "Tente nadar através dos anéis %s. Os outros jogadores tentarão nadar através dos outros anéis coloridos. Para nadar, use as teclas de seta."
RingGameMissed = "PERDEU"
RingGameGroupPerfect = "GRUPO\nPERFEITO!!"
RingGamePerfect = "PERFEITO!"
RingGameGroupBonus = "BÔNUS DO GRUPO"

# RingGameGlobals.py
ColorRed = "vermelhos"
ColorGreen = "verdes"
ColorOrange = "laranja"
ColorPurple = "lilases"
ColorWhite = "brancos"
ColorBlack = "pretos"
ColorYellow = "amarelos"

# DistributedDivingGame.py #localize
DivingGameTitle = "Mergulho pro Tesouro"
# color
DivingInstructionsSinglePlayer = "Tesouros irão aparecer no fundo do lago. Use as setas para nadar. Evite os peixes e leve os tesouros para o barco!"
# color
DivingInstructionsMultiPlayer = " Tesouros irão aparecer no fundo do lago. Use as setas para nadar. Trabalhem juntos para levar os tesouros para o barco!"
DivingGameTreasuresRetrieved = "Tesouros Recuperados"

#Distributed Target Game
TargetGameTitle = "Estilingue do Toon"
TargetGameInstructionsSinglePlayer = "Acerta na velocidade do alvo"
TargetGameInstructionsMultiPlayer = "Acerta quantos alvos conseguir"
TargetGameBoard = "Rodada %s - Mantendo o Melhor Placar"
TargetGameCountdown = "Lançamento forçado em %s segundos"
TargetGameCountHelp = "Bata nas setas esquerda e direita para conseguir potência, pare para lançar"
TargetGameFlyHelp = "Aperte para baixo para abrir o guarda-chuva"
TargetGameFallHelp = "Use as teclas de seta para aterrissar no alvo"
TargetGameBounceHelp = " Bater e quicar pode tirar você do alvo"

#Distributed Photo Game
PhotoGameScoreTaken = "%s: %s\nVocê: %s"
PhotoGameScoreBlank = "Placar: %s"
PhotoGameScoreOther = "\n%s"#"Placar: %s\n%s"
PhotoGameScoreYou = "\nMelhor Bônus!"#"Placar: %s\nMelhor Bônus!"


# DistributedTagGame.py
TagGameTitle = "Jogo de pique"
TagGameInstructions = "Pegue os tesouros. Você não pode pegar os tesouros se o pique estiver com você!"
TagGameYouAreIt = "Está com você!"
TagGameSomeoneElseIsIt = "Está com %s!"

# DistributedMazeGame.py
MazeGameTitle = "Jogo do labirinto"
MazeGameInstructions = "Pegue os tesouros. Tente pegar todos, mas cuidado com os "+ Cogs +"!"# DistributedCatchGame.py

# DistributedCatchGame.py
CatchGameTitle = "Jogo de pegar"
CatchGameInstructions = "Pegue o máximo de %(fruit)s que conseguir. Cuidado com os "+ Cogs +" e tente não 'pegar' nenhuma %(badThing)s!"
CatchGamePerfect = "PERFEITO!"
CatchGameApples      = 'maçãs'
CatchGameOranges     = 'laranjas'
CatchGamePears       = 'pêras'
CatchGameCoconuts    = 'cocos'
CatchGameWatermelons = 'melancias'
CatchGamePineapples  = 'abacaxis'
CatchGameAnvils      = 'bigornas'

# DistributedPieTossGame.py
PieTossGameTitle = "Jogo de lançamento de tortas"
PieTossGameInstructions = "Lance as tortas nos alvos."

# DistributedPhotoGame.py
PhotoGameInstructions = "Tire fotos de acordo com os Toons mostrados na parte de baixo. Mire a câmera usando o mouse, e clique com o botão esquerdo para tirar uma foto. Aperte Ctrl para aumentar ou reduzir o zoom, e olhe em sua volta com as teclas de seta. Fotos com notas maiores ganham mais pontos!"
PhotoGameTitle = "Diversão Fotográfica"
PhotoGameFilm = "FILME"
PhotoGameScore = "Placar da Equipe: %s\n\nMelhores Fotos: %s\n\nPlacar Total: %s"

# DistributedCogThiefGame.py
CogThiefGameTitle = Cog + " Ladrão"
CogThiefGameInstructions = "Impeça que os " + Cogs + " roubem nossos barris! Aperte a tecla Ctrl para atirar uma torta. Use as teclas de seta para se mover. Dica: você pode andar nas diagonais."
CogThiefBarrelsSaved = "%(num)d Barris\nSalvos!"
CogThiefBarrelSaved = "%(num)d Barril\nSalvo!"
CogThiefNoBarrelsSaved = "Nenhum Barril\nSalvo"
CogThiefPerfect = "PERFEITO!!"

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "JOGAR"

# Purchase.py
GagShopName = "Loja de Piadas do Pateta"
GagShopPlayAgain = "JOGAR\nNOVAMENTE"
GagShopBackToPlayground = "SAIR DE NOVO \nPARA O PÁTIO"
GagShopYouHave = "Você tem %s balinhas para gastar"
GagShopYouHaveOne = "Você tem 1 balinha para gastar"
GagShopTooManyProps = "Sinto muito, você tem muitos acessórios"
GagShopDoneShopping = "FIM DAS\nCOMPRAS"
# name of a gag
GagShopTooManyOfThatGag = "Sinto muito, você já tem %s o suficiente"
GagShopInsufficientSkill = "Você não tem muita habilidade para isso ainda"
# name of a gag
GagShopYouPurchased = "Você comprou %s"
GagShopOutOfJellybeans = "Sinto muito, você não tem mais balinhas!"
GagShopWaitingOtherPlayers = "Aguardando outros jogadores..."
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%s desconectou-se"
GagShopPlayerExited = "%s saiu"
GagShopPlayerPlayAgain = "Jogar novamente"
GagShopPlayerBuying = "Comprando"

# MakeAToon.py
GenderShopQuestionMickey = "Para criar um Toon menino, clique em mim!"
GenderShopQuestionMinnie = "Para criar um Toon menina, clique em mim!"
GenderShopFollow = "Siga-me!"
GenderShopSeeYou = "Vejo você depois!"
GenderShopBoyButtonText = "Menino"
GenderShopGirlButtonText = "Menina"

# BodyShop.py
BodyShopHead = "Cabeça"
BodyShopBody = "Corpo"
BodyShopLegs = "Pernas"

# ColorShop.py
ColorShopHead = "Cabeça"
ColorShopBody = "Corpo"
ColorShopLegs = "Pernas"
ColorShopToon = "Toon"
ColorShopParts = "Partes"
ColorShopAll = "Tudo"

# ClothesShop.py
ClothesShopShorts = "Short"
ClothesShopShirt = "Camisa"
ClothesShopBottoms = "Parte de baixo"

# MakeAToon
PromptTutorial = "Parabéns!\nVocê é o(a) mais recente morador(a) de Toontown!\n\nDeseja continuar com o Toontorial ou teletransportar-se diretamente para o Centro de Toontown?"
MakeAToonSkipTutorial = "Pular Toontorial"
MakeAToonEnterTutorial = "Acessar Toontorial"
MakeAToonDone = lOK
MakeAToonCancel = lCancel
MakeAToonNext = lNext
MakeAToonLast = lBack
CreateYourToon = "Clique nas setas para criar o seu Toon."
CreateYourToonTitle = "Crie o seu Toon"
ShapeYourToonTitle = "Selecione o Tipo"
PaintYourToonTitle = "Selecione a Cor"
PickClothesTitle = "Selecione as Roupas"
NameToonTitle = "Selecione o Nome"
CreateYourToonHead = "Clique nas setas da 'cabeça' para escolher animais diferentes."
MakeAToonClickForNextScreen = "Clique na seta abaixo para ir até a próxima tela."
PickClothes = "Clique nas setas para escolher roupas!"
PaintYourToon = "Clique nas setas para pintar o seu toon!"
MakeAToonYouCanGoBack = "Você pode voltar para alterar o corpo também!"
MakeAFunnyName = "Escolha um nome engraçado para o seu Toon com o jogo Escolha um nome!"
MustHaveAFirstOrLast1 = "O seu Toon deve ter um nome ou um sobrenome, não é?"
MustHaveAFirstOrLast2 = "Você não quer que o seu Toon tenha um nome ou um sobrenome?"
ApprovalForName1 = "É isso aí, o seu Toon merece um nome muito legal!"
ApprovalForName2 = "Os nomes de Toons são os nomes mais legais que existem!"
MakeAToonLastStep = "Última etapa antes de ir para Toontown!"
PickANameYouLike = "Escolha o nome que quiser!"
TitleCheckBox = "Título"
FirstCheckBox = "Primeiro"
LastCheckBox = "Último"
RandomButton = "Aleatório"
ShuffleButton = "Misturar"
NameShopSubmitButton = "Enviar"
TypeANameButton = "Digite um nome"
TypeAName = "Não gostou destes nomes?\nClique aqui -->"
PickAName = "Tente usar o jogo Escolha um nome!\nClique aqui -->"
PickANameButton = "Escolha um nome"
RejectNameText = "Este nome não é permitido. Tente novamente."
WaitingForNameSubmission = "Enviando o seu nome..."

# PetshopGUI.py
PetNameMaster = "PetNameMaster_portuguese.txt"
PetshopUnknownName = "Nome: ???"
PetshopDescGender = "Sexo:\t%s"
PetshopDescCost = "Custo:\t%s balinhas"
PetshopDescTrait = "Características:\t%s"
PetshopDescStandard = "Padrão"
PetshopCancel = lCancel
PetshopSell = "Vender peixes"
PetshopAdoptAPet = "Adotar um Rabisco"
PetshopReturnPet = "Devolver o Rabisco"
PetshopAdoptConfirm = "Adotar %s por %d balinhas?"
PetshopGoBack = "Voltar"
PetshopAdopt = "Adotar"
PetshopReturnConfirm = "Devolver %s?"
PetshopReturn = "Devolver"
PetshopChooserTitle = "RABISCOS DE HOJE"
PetshopGoHomeText = 'Deseja ir à sua propriedade para brincar com seu novo Rabisco?'

# NameShop.py
NameShopNameMaster = "NameMaster_portuguese.txt"
NameShopPay = "Assine já!"
NameShopPlay = "Avaliação gratuita"
NameShopOnlyPaid = "Somente usuários pagantes\npodem dar nomes aos seus Toons.\nAté que você se inscreva,\nseu nome será\n"
NameShopContinueSubmission = "Continuar envio"
NameShopChooseAnother = "Escolha outro nome"
NameShopToonCouncil = "O Conselho de Toons\nanalisará o seu\nnome."+ \
                      "A análise pode\nlevar alguns dias.\nEnquanto você espera,\nseu nome será\n"
PleaseTypeName = "Digite o seu nome:"
AllNewNames = "Todos os novos nomes\ndevem ser aprovados\npelo Conselho de Toons."
NameMessages = "Use sua criatividade e lembre-se:\nnada de nomes relacionados com a Disney, por favor."
NameShopNameRejected = "O nome\nenviado foi\nrejeitado."
NameShopNameAccepted = "Parabéns!\nO nome\nenviado foi\naceito!"
NoPunctuation = "Não é permitido usar caracteres de pontuação nos nomes!"
PeriodOnlyAfterLetter = "Você pode usar um ponto no nome, mas apenas depois de uma letra."
ApostropheOnlyAfterLetter = "Você pode usar um apóstrofo no nome, mas apenas depois de uma letra."
NoNumbersInTheMiddle = "Dígitos numéricos podem não aparecer no meio da palavra."
ThreeWordsOrLess = "Seu nome deve ter três palavras ou menos."
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
    "pato donald",
    "patodonald",
    "pluto",
    "goofy",
    "pateta",
    )
NumToColor = ['Branco', 'Pêssego', 'Vermelho vivo', 'Vermelho', 'Castanho',
              'Siena', 'Marrom', 'Canela', 'Coral', 'Laranja',
              'Amarelo', 'Creme', 'Cítrico', 'Limão', 'Verde-água',
              'Verde', 'Azul-claro', 'Verde-azul', 'Azul',
              'Verde-musgo', 'Azul-turquesa', 'Azul cinzento', 'Lilás',
              'Púrpura', 'Rosa']
AnimalToSpecies = {
    'dog'    : 'Cachorro',
    'cat'    : 'Gato',
    'mouse'  : 'Rato',
    'horse'  : 'Cavalo',
    'rabbit' : 'Coelho',
    'duck'   : 'Pato',
    'monkey' : 'Macaco',
    'bear'   : 'Urso',
    'pig'    : 'Porco'
    }
NameTooLong = "Este nome é muito longo. Tente novamente."
ToonAlreadyExists = "Você já tem um Toon com o nome %s!"
NameAlreadyInUse = "Este nome já foi usado!"
EmptyNameError = "Você deve primeiramente inserir um nome."
NameError = "Sinto muito. Este nome não vai funcionar."

# NameCheck.py
NCTooShort = 'Este nome é muito curto.'
NCNoDigits = 'O nome não pode conter números.'
NCNeedLetters = 'Cada palavra do nome deve conter algumas letras.'
NCNeedVowels = 'Cada palavra do nome deve conter algumas vogais.'
NCAllCaps = 'O seu nome não pode estar todo em maiúsculas.'
NCMixedCase = 'Este nome tem muitas letras em maiúsculas.'
NCBadCharacter = "O seu nome não pode conter o caractere '%s'"
NCGeneric = 'Sinto muito, este nome não vai funcionar.'
NCTooManyWords = 'O seu nome não pode ter mais de quatro palavras.'
NCDashUsage = ("Hífens podem ser usados apenas para ligar duas palavras"
               "(como em 'Bu-Bu').")
NCCommaEdge = "O seu nome não pode começar ou terminar com vírgula."
NCCommaAfterWord = "Você não pode começar uma palavra com vírgula."
NCCommaUsage = ('Este nome não usa vírgulas corretamente. As vírgulas devem'
                'juntar duas palavras, como no nome "Dr. Quack, MD".'
                'As vírgulas devem também ser seguidas por um espaço.')
NCPeriodUsage = ('Este nome não usa pontos corretamente. Os pontos são'
                 'permitidos somente em palavras como "Sr.", "Sra.", "J.P.", etc.')
NCApostrophes = 'Este nome tem excesso de apóstrofos.'

# DistributedTrophyMgrAI.py
RemoveTrophy = "Quartel dos Toons: Os "+ Cogs +" dominaram um dos edifícios que você salvou!"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = 'Precisa de mais tempo para pensar?'
STOREOWNER_GOODBYE = 'Vejo você depois!'
STOREOWNER_NEEDJELLYBEANS = 'Você precisa pegar o bondinho para conseguir algumas balinhas.'
STOREOWNER_GREETING = 'Escolha o que deseja comprar.'
STOREOWNER_BROWSING = 'Você pode olhar, mas precisará de um bilhete de roupas para comprar.'
STOREOWNER_NOCLOTHINGTICKET = 'Para comprar roupas, você precisa de um bilhete de roupas.'

STOREOWNER_NOFISH = 'Volte aqui para vender peixes para a loja de animais e ganhar balinhas.'
STOREOWNER_THANKSFISH = 'Valeu! A loja de animais vai adorar estes aqui. Tchau!'
STOREOWNER_THANKSFISH_PETSHOP = "Estes tipos são raros! Valeu."
STOREOWNER_PETRETURNED = "Não se preocupe. Acharemos um bom lar para o seu Rabisco."
STOREOWNER_PETADOPTED = "Parabéns pelo novo Rabisco! Você pode brincar com ele em sua propriedade."
STOREOWNER_PETCANCELED = "Lembre-se, caso veja um Rabisco de seu agrado, adote-o antes que alguém o faça!"

STOREOWNER_NOROOM = "Hmm... Você pode precisar arranjar espaço no seu armário antes de comprar roupas novas.\n"
STOREOWNER_CONFIRM_LOSS = "O seu armário está cheio. Você vai perder as roupas que estava vestindo."
STOREOWNER_OK = lOK
STOREOWNER_CANCEL = lCancel
STOREOWNER_TROPHY = "Uau! Você pegou %s de %s peixe. Merece um troféu e um Acréscimo de risadas!"
# end translate

# NewsManager.py
SuitInvasionBegin1 = lToonHQ+": Foi iniciada uma Invasão de Cogs!!!"
SuitInvasionBegin2 = lToonHQ+": %s dominaram Toontown!!!"
SuitInvasionEnd1 = lToonHQ+": A Invasão de %s terminou!!!"
SuitInvasionEnd2 = lToonHQ+": Mais uma vez os Toons salvaram a pátria!!!"
SuitInvasionUpdate1 = lToonHQ+": A Invasão de Cogs está agora em %s Cogs!!!"
SuitInvasionUpdate2 = lToonHQ+": Precisamos derrotar esses %s!!!"
SuitInvasionBulletin1 = lToonHQ+": Há uma Invasão de Cogs em andamento!!!"
SuitInvasionBulletin2 = lToonHQ+": %s dominaram Toontown!!!"

# DistributedHQInterior.py
LeaderboardTitle = "Pelotão Toon"

# QuestScript.txt
QuestScriptTutorialMickey_1 = "Toontown ganhou um novo cidadão! Você tem piadas de reserva?"
QuestScriptTutorialMickey_2 = "Claro, %s!"
QuestScriptTutorialMickey_3 = "O Tutorial Tom vai contar para você tudo sobre os Cogs.\aTchauzinho!"
QuestScriptTutorialMickey_4 = "Vem cá! Use as teclas de seta para mover-se."

# These are needed to correspond to the Japanese gender specific phrases
QuestScriptTutorialMinnie_1 = "Toontown ganhou um novo cidadão! Você tem piadas de reserva?"
QuestScriptTutorialMinnie_2 = "Claro, %s!"
QuestScriptTutorialMinnie_3 = "O Tutorial Tom vai contar para você tudo sobre os Cogs.\aTchauzinho!"

QuestScript101_1 = "Estes são os COGS. Eles são robôs que estão tentando dominar Toontown."
QuestScript101_2 = "Há vários tipos diferentes de COGS e..."
QuestScript101_3 = "...eles transformam os alegres edifícios dos Toons..."
QuestScript101_4 = "...em horríveis edifícios de Cogs!"
QuestScript101_5 = "Mas os COGS não aguentam piadas!"
QuestScript101_6 = "Uma boa piada os deterá."
QuestScript101_7 = "Há milhares de piadas, mas, para começar, use estas aqui."
QuestScript101_8 = "Ah! Você também vai precisar de um Risômetro!"
QuestScript101_9 = "Se o seu Risômetro estiver baixo, é porque você está triste!"
QuestScript101_10 = "Um Toon feliz é um Toon saudável!"
QuestScript101_11 = "OH NÃO! Há um COG na porta da minha loja!"
QuestScript101_12 = "AJUDE-ME, POR FAVOR! Derrote este COG!"
QuestScript101_13 = "Esta é a sua primeira Tarefa Toon!"
QuestScript101_14 = "Vamos nessa! Vá derrotar aquele Puxa-saco!"

QuestScript110_1 = "Bom trabalho; você derrotou aquele Puxa-saco. Deixe-me dar a você um Álbum Toon..."
QuestScript110_2 = "O livro é cheio de coisas legais."
QuestScript110_3 = "Abra-o para eu mostrar a você."
QuestScript110_4 = "O mapa mostra o local onde você esteve."
QuestScript110_5 = "Vire a página para ver as suas piadas..."
QuestScript110_6 = "Êpa! Você não tem nenhuma piada! Vou passar uma tarefa para você."
QuestScript110_7 = "Vire a página para ver as suas tarefas."
QuestScript110_8 = "Dê uma volta no bondinho para ganhar balinhas e poder comprar piadas!"
QuestScript110_9 = "Para ir até o bondinho, saia pela porta logo atrás de mim e siga até o pátio."
QuestScript110_10 = "Agora, feche o livro e encontre o bondinho!"
QuestScript110_11 = "Volte para o Quartel dos Toons quando já estiver pronto. Tchau!"

QuestScriptTutorialBlocker_1 = "Oi, e aí, pessoal?"
QuestScriptTutorialBlocker_2 = "Alô?"
QuestScriptTutorialBlocker_3 = "Ah! Você não sabe usar o Chat rápido!"
QuestScriptTutorialBlocker_4 = "Clique no botão para dizer algo."
QuestScriptTutorialBlocker_5 = "Muito bom!\aO local para onde você está indo tem um monte de Toons para conversar."
QuestScriptTutorialBlocker_6 = "Se você quiser conversar com seus amigos usando o teclado, há um outro botão que pode ser usado."
QuestScriptTutorialBlocker_7 = "Ele se chama botão \"Conversar\". Você precisa ser um cidadão oficial de Toontown para usá-lo."
QuestScriptTutorialBlocker_8 = "Boa sorte! Vejo você depois!"

"""
GagShopTut

You will also earn the ability to use other types of gags.

"""

QuestScriptGagShop_1 = "Bem-vindo à Loja de Piadas!"
QuestScriptGagShop_1a = "Aqui é o lugar onde os Toons vêm comprar piadas para usar contra os Cogs."
#QuestScriptGagShop_2 = "Este pote mostra quantas balinhas você tem."
#QuestScriptGagShop_3 = "Para comprar piadas, clique em botões de piada. Tente pegar umas agora!"
QuestScriptGagShop_3 = "Para comprar piadas, clique em botões de piada. Tente pegar algumas agora!"
QuestScriptGagShop_4 = "Bom! Você pode usar estas piadas nas batalhas contra os Cogs."
QuestScriptGagShop_5 = "Dê uma olhada para ver como são as piadas avançadas de jogar e de esguichar..."
QuestScriptGagShop_6 = "Depois que terminar de comprar piadas, clique neste botão para retornar ao Pátio."
QuestScriptGagShop_7 = "Normalmente, você pode usar este botão para participar de outro Jogo no Bondinho..."
QuestScriptGagShop_8 = "...Mas não há tempo para outro jogo agora. Estão precisando de você no Quartel dos Toons!"

QuestScript120_1 = "Muito bem, você encontrou o bondinho!\aPor falar nisso, você encontrou o Banqueiro Beto?\aEle é bem guloso por doces.\aPor que você não se apresenta e leva para ele este chocolate de presente."
QuestScript120_2 = "O Banqueiro Beto está lá no Banco de Toontown."

QuestScript121_1 = "Mmm, obrigado pelo chocolate.\aOlha só, se você me ajudar, eu dou a você uma recompensa.\aEsses Cogs roubaram as chaves do meu cofre. Derrote os Cogs para encontrar a chave roubada.\aQuando você encontra-la, traga-a para mim."

QuestScript130_1 = "Muito bem, você encontrou o bondinho!\aPor falar nisso, recebi hoje um pacote para o Professor Paulo.\aDeve ser o novo giz que ele encomendou.\aVocê pode, por favor, levar para ele?\aEle está lá na escola."

QuestScript131_1 = "Ah, obrigado pelo giz.\aO quê?!?\aEsses Cogs roubaram meu quadro-negro. Derrote os Cogs para encontrar meu quadro-negro roubado.\aQuando encontrá-lo, traga de volta para mim."

QuestScript140_1 = "Muito bem, você encontrou o bondinho!\aPor falar nisso, tenho um amigo, o Bibliotecário Bino, que é uma verdadeira traça de livros.\aPeguei este livro para ele da última vez em que estive no Porto do Donald.\aVocê podia levar para ele? Em geral, ele fica na Biblioteca."

QuestScript141_1 = "Ah, sim, este livro vai quase completar a minha coleção.\aDeixe-me ver...\aÊpa...\aOnde é que eu pus os meus óculos agora?\aEu estava com eles um pouco antes de aqueles Cogs invadirem o meu edifício.\aDerrote os Cogs para encontrar meus óculos roubados.\aaQuando encontrá-los, traga de volta para mim para ganhar uma recompensa."

QuestScript145_1 = "Estou vendo que você não teve problemas com o bondinho!\a Olha só, os Cogs roubaram o apagador do nosso quadro-negro.\a Vá para as ruas e lute com os Cogs até recuperar o apagador.\a Para encontrar as ruas, passe por um dos túneis como este:"
QuestScript145_2 = "Quando encontrar nosso apagador, traga-o de volta para cá.\aNão se esqueça, se precisar de piadas, pegue o bondinho.\aE se você precisar recuperar Pontos de risadas, colete casquinhas de sorvete no Pátio."

QuestScript150_1 = "Ah... Esta próxima tarefa talvez seja muito difícil para você executar sozinho!"
QuestScript150_2 = "Para fazer amigos, encontre outro jogador e use o botão Novo amigo."
QuestScript150_3 = "Depois que você tiver arrumado um amigo, volte aqui."
QuestScript150_4 = "Algumas tarefas são muito difíceis de serem executadas sem ajuda!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignore-me"

SellbotBossName = "V. P. Sênior"
CashbotBossName = "Diretor Financeiro"
LawbotBossName = "Juiz-chefe"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "Com isto, você está promovido a %s sênior. Parabéns!"
BossCogDoobersAway = { 's' : "Vai! E faça essa venda!" }
BossCogWelcomeToons = "Bem-vindos, novos Cogs!"
BossCogPromoteToons = "Com isto, você está promovido a %s sênior. Parab--"
CagedToonInterruptBoss = "Oi! Uhuu! E aí pessoal!"
CagedToonRescueQuery = "Então, galera de Toons, vocês vêm me salvar?"
BossCogDiscoverToons = "Hã? Toons! Disfarçar!"
BossCogAttackToons = "Atacar!!"
CagedToonDrop = [
    "Bom trabalho! Ele está ficando exausto!",
    "Fique atrás dele! Ele está fugindo!",
    "Pessoal, vocês estão se saindo muito bem!",
    "Fantástico! Você quase o pegou agora!",
    ]
CagedToonPrepareBattleTwo = "Cuidado, ele está tentando escapar!\aAjudem-me todos! Levantem-se aqui e detenham-no!"
CagedToonPrepareBattleThree = "Maneiro! Estou quase livre!\aAgora, você precisa atacar o Cog V. P. em pessoa.\aTenho um montão de tortas que você pode usar!\aPule e toque na parte inferior da minha cela para que eu lhe dê algumas tortas.\aPressione a tecla Insert para jogar as tortas quando você as pegar!"
BossBattleNeedMorePies = "Você precisa de mais tortas!"
BossBattleHowToGetPies = "Pule para tocar na cela e pegar mais tortas."
BossBattleHowToThrowPies = "Pressione a tecla Insert para jogar tortas!"
CagedToonYippee = "Iupii!!"
CagedToonThankYou = "É ótimo estar livre!\aObrigado por toda a sua ajuda!\aTe devo esta.\aSe, por acaso, você estiver em apuros em alguma batalha, é só me chamar!\aBasta clicar no botão SOS para me chamar."
CagedToonPromotion = "\aOlha só! Aquele Cog V.P. acabou deixando aqui os seus documentos de promoção.\aVou arquivá-los para você na saída, para que pegue a promoção!"
CagedToonLastPromotion = "\aUau, você atingiu o nível %s no processo Cog!\aOs Cogs não têm promoção maior do que esta.\aVocê não pode mais subir no processo Cog, mas certamente pode continuar salvando os Toons!"
CagedToonHPBoost = "\aVocê salvou um monte de Toons neste quartel.\aO Conselho de Toons decidiu dar a você outro Ponto de risadas. Parabéns!"
CagedToonMaxed = "\aVi que você tem o nível %s no processo Cog. Impressionante!\aEm nome do Conselho de Toons, agradeço por retornar para salvar mais Toons!"
CagedToonGoodbye = "Te vejo por aí!"


CagedToonBattleThree = {
    10: "Belo salto, %(toon)s. Tome aqui algumas tortas!",
    11: "Oi, %(toon)s! Pegue algumas tortas!",
    12: "E aí, %(toon)s? Agora, você tem algumas tortas!",

    20: "Olá, %(toon)s! Pule até a minha cela e pegue algumas tortas para jogar!",
    21: "Oi, %(toon)s! Use a tecla Ctrl para pular e tocar a minha cela!",

    100: "Pressione a tecla Insert para jogar uma torta.",
    101: "O medidor de potência azul mostra a altura que a sua torta atinge.",
    102: "Primeiramente, tente jogar uma torta dentro da lataria dele para melecar seus mecanismos.",
    103: "Espere até que a porta se abra para jogar uma torta bem lá dentro.",
    104: "Quando ele estiver tonto, bata na cara ou no peito dele para empurrá-lo para trás!",
    105: "Você saberá se o seu golpe foi bom quando vir o chão colorido.",
    106: "Se você atingir um Toon com uma torta, ele ganhará um Ponto de risadas!",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

CashbotBossHadEnough = "É isso aí! Chega desses Toons irritantes!"
CashbotBossOuttaHere = "Tenho que pegar o trem!"
ResistanceToonName = "Mata Rara"
ResistanceToonCongratulations = "Você conseguiu! Parabéns!\aVocê é um orgulho para a Resistência!\aEsta é uma frase especial que você pode usar quando estiver em apuros:\a%s\aQuando você a pronunciar, %s.\aMas só pode usar uma vez, portanto, escolha a hora certa!"
ResistanceToonToonupInstructions = "todos os Toons próximos a você ganham %s pontos de risadas"
ResistanceToonToonupAllInstructions = "todos os Toons próximos a você ganham pontos de risadas completos"
ResistanceToonMoneyInstructions = "todos os Toons próximos a você ganham %s balinhas"
ResistanceToonMoneyAllInstructions = "todos os Toons próximos a você encherão suas jarras de balinhas"
ResistanceToonRestockInstructions = "todos os Toons próximos a você vão reabastecer suas \"%s\" piadas"
ResistanceToonRestockAllInstructions = "todos os Toons próximos a você vão reabastecer todas as suas piadas"

ResistanceToonLastPromotion = "\aUau, você atingiu o nível %s no processo Cog!\aOs Cogs não têm promoção maior do que esta.\aVocê não pode mais subir no processo Cog, mas, certamente, pode continuar trabalhando para a Resistência!"
ResistanceToonHPBoost = "\aVocê trabalhou muito para a Resistência.\aO Conselho de Toons decidiu dar a você outro Ponto de risadas. Parabéns!"
ResistanceToonMaxed = "\aVejo que você tem o nível %s no processo Cog. Impressionante!\aEm nome do Conselho de Toons, agradeço por retornar para salvar mais Toons!"

CashbotBossCogAttack = "Peguem-nos!!!"
ResistanceToonWelcome = "Você conseguiu! Siga-me até o cofre-forte antes que o Diretor Financeiro nos ache!"
ResistanceToonTooLate = "Droga! Estamos atrasados demais!"
CashbotBossDiscoverToons1 = "Ah-HAH!"
CashbotBossDiscoverToons2 = "Pensei ter farejado um tooninho por aqui! Impostores!"
ResistanceToonKeepHimBusy = "Mantenha-o ocupado! Vou montar uma armadilha!"
ResistanceToonWatchThis = "Olha isso!"
CashbotBossGetAwayFromThat = "Ei! Afaste-se!"
ResistanceToonCraneInstructions1 = "Controle um ímã subindo no pódio."
ResistanceToonCraneInstructions2 = "Use as teclas de setas para mover o guindaste e pressione a tecla Ctrl para pegar um objeto."
ResistanceToonCraneInstructions3 = "Pegue um cofre com o ímã e arranque o capacete de segurança do Diretor Financeiro."
ResistanceToonCraneInstructions4 = "Depois de fazer zunir o capacete, pegue um brutamontes desativado e dê uma pancada na cabeça dele!"
ResistanceToonGetaway = "Ih! Tenho que correr!"
CashbotCraneLeave = "Deixar o guindaste"
CashbotCraneAdvice = "Use as teclas de setas para mover o guindaste de pórtico."
CashbotMagnetAdvice = "Mantenha pressionada a tecla Ctrl para pegar os objetos."
CashbotCraneLeaving = "Deixando o guindaste"

MintElevatorRejectMessage = "Não será possível entrar na Casa da Moeda até que a vestimenta de Cog %s esteja completa."
BossElevatorRejectMessage = "Você não pode pegar este elevador até que tenha recebido uma promoção."
NotYetAvailable = "Este elevador ainda não está disponível."

# Types of catalog items--don't translate yet.
FurnitureTypeName = "Mobília"
PaintingTypeName = "Pintura"
ClothingTypeName = "Roupas"
ChatTypeName = "Frase do Chat rápido"
EmoteTypeName = "Aulas de representação"
BeanTypeName = "Balinhas"
PoleTypeName = "Vara de pescar"
WindowViewTypeName = "Vista da janela"
PetTrickTypeName = 'Treinamento de Rabiscos'
GardenTypeName = 'Materiais de Jardim'
RentalTypeName = 'Item de Aluguel'
GardenStarterTypeName = 'Kit de Jardinagem'
NametagTypeName = "Crachá"


# Make sure numbers match up to CatalogItemTypes.py
CatalogItemTypeNames = {
    0 : "INVALID_ITEM",
    1 : FurnitureTypeName, 
    2 : ChatTypeName, 
    3 : ClothingTypeName, 
    4 : EmoteTypeName, 
    5 : "WALLPAPER_ITEM",
    6 : "WindowViewTypeName",
    7 : "FLOORING_ITEM",
    8 : "MOULDING_ITEM",
    9 : "WAINSCOTING_ITEM",
    10: PoleTypeName, 
    11: PetTrickTypeName, 
    12: BeanTypeName, 
    13: GardenTypeName, 
    14: RentalTypeName, 
    15: GardenStarterTypeName, 
    16: NametagTypeName, 
    17: "TOON_STATUE_ITEM",
    18: "ANIMATED_FURNITURE_ITEM",    
}   


# Make sure this is in sync with ToonDNA.ShirtStyles
ShirtStylesDescriptions = {
    # -------------------------------------------------------------------------
    # Boy styles
    # -------------------------------------------------------------------------
    'bss1' : "básica",
    'bss2' : "uma listra",
    'bss3' : "colarinho",
    'bss4' : "duas listras",
    'bss5' : "listrada",
    'bss6' : "colarinho com bolso",
    'bss7' : "havaiana",
    'bss8' : "colarinho com 2 bolsos",
    'bss9' : "camisa de boliche",
    'bss10' : "colete (especial)",
    'bss11' : "colarinho com franzidos",
    'bss12' : "camiseta de futebol (especial)",
    'bss13' : "camiseta lightning bolt (especial)",
    'bss14' : "camiseta 19 (especial)",
    'bss15' : "camisa panamá",

    # -------------------------------------------------------------------------
    # Girl styles
    # -------------------------------------------------------------------------
    'gss1' : "básica",
    'gss2' : "uma listra",
    'gss3' : "colarinho",
    'gss4' : "duas listras",
    'gss5' : "colarinho com bolso",
    'gss6' : "estampa de flor",
    'gss7' : "bordado de flor (especial)",
    'gss8' : "colarinho feminino com 2 bolsos ",
    'gss9' : "colete de brim (especial)",
    'gss10' : "camponesa", 
    'gss11' : "camponesa com meia listra",
    'gss12' : "camiseta de futebol (especial)",
    'gss13' : "com corações",
    'gss14' : "com estrelas (especial)",
    'gss15' : "com flores",

    # -------------------------------------------------------------------------
    # Special Catalog-only shirts. 
    # -------------------------------------------------------------------------
    # yellow hooded - Series 1
    'c_ss1' : "amarela com capuz - Série 1",
    'c_ss2' : "amarela com palmeira - Série 1",
    'c_ss3' : "roxa com estrelas - Série 2",
    'c_bss1' : "listras azuis (masculina) - Série 1",
    'c_bss2' : "laranja (masculina) - Série 1",
    'c_bss3' : "verde-limão com listra (masculina) - Série 2",
    'c_bss4' : "quimono vermelho com xadrez (masculina) - Série 2",
    'c_gss1' : "azul com listras amarelas (feminina) - Série 1",
    'c_gss2' : "rosa e bege com flor (feminina) - Série 1",
    'c_gss3' : "azul e dourado com listras ondulantes (feminina) - Série 2",
    'c_gss4' : "azul e rosa com arco (feminina) - Série 2",
    'c_gss5' : "quimono azul-piscina com listra (feminina) – NÃO USADO",
    'c_ss4'  : "Camiseta tingida (unissex) - Série 3",
    'c_ss5' : "azul-claro com azul e listra branca (masculina) - Série 3",
    'c_ss6' : "camisa de vaqueiro 1 : Série 4",
    'c_ss7' : "camisa de vaqueiro 2 : Série 4",
    'c_ss8' : "camisa de vaqueiro 3 : Série 4",
    'c_ss9' : "camisa de vaqueiro 4 : Série 4",
    'c_ss10' : "camisa de vaqueiro 5 : Série 4",
    'c_ss11' : "camisa de vaqueiro 6 : Série 4",
    
    # Special Holiday-themed shirts.
    'hw_ss1' : "Fantasma de Halloween",
    'hw_ss2' : "Abóbora de Halloween",
    'wh_ss1' : "Feriado de Inverno 1",
    'wh_ss2' : "Feriado de Inverno 2",
    'wh_ss3' : "Feriado de Inverno 3",
    'wh_ss4' : "Feriado de Inverno 4",

    'vd_ss1' : "Dia dos namorados, rosa com corações vermelhos (feminina)",
    'vd_ss2' : "Dia dos namorados, vermelha com corações brancos",
    'vd_ss3' : "Dia dos namorados, branca com corações alados (masculina)",
    'vd_ss4' : "Dia dos namorados, rosa com corações flamejantes",
    'vd_ss5' : "Dia dos namorados 2009, branca com cupido vermelho",
    'vd_ss6' : "Dia dos namorados 2009, azul com verde e corações vermelhos",
    'sd_ss1' : "Dia de São Patrício, camisa com trevo-de-quatro-folhas",
    'sd_ss2' : "Dia de São Patrício, camisa com pote de ouro",
    'tc_ss1' : "Concurso de Camiseta, Colete de Pesca",
    'tc_ss2' : "Concurso de Camiseta, Aquário",
    'tc_ss3' : "Concurso de Camiseta, Pegada",
    'tc_ss4' : "Concurso de Camiseta, Pegada",
    'tc_ss5' : "Concurso de Camiseta, Shorts de Couro",
    'tc_ss6' : "Concurso de Camiseta, Melancia",
    'tc_ss7' : "Concurso de Camiseta, Camisa de Corrida",
    'j4_ss1' : "Bandeira de 4 de julho",
    'j4_ss2' : "Fogos de Artifício de 4 de julho",
    'c_ss12' : "Catálogo série 7, Verde com botões de amarelos", 
    'c_ss13' : "Catálogo série 7, Roxo com flor grande", 

    'pj_ss1' : "Camisa de Pijama de banana azul", 
    'pj_ss2' : "Camisa de Pijama de chifre vermelho",
    'pj_ss3' : "Camisa de Pijama de óculos roxos",
    
    # Special award clothes
    'sa_ss1' : "Camisa Listrada",
    'sa_ss2' : "Camisa de Pesca 1",
    'sa_ss3' : "Camisa de Pesca 2",
    'sa_ss4' : "Camisa de Jardinagem 1",
    'sa_ss5' : "Camisa de Jardinagem 2",
    'sa_ss6' : "Camisa de Festa 1",
    'sa_ss7' : "Camisa de Festa 2",
    'sa_ss8' : "Camisa de Corrida 1",
    'sa_ss9' : "Camisa de Corrida 2",
    'sa_ss10' : "Camisa de Verão 1",
    'sa_ss11' : "Camisa de Verão 2",

    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    }

# Make sure this is in sync with ToonDNA.BottomStyles
BottomStylesDescriptions = {
    # name : [ bottomIdx, [bottomColorIdx, ...]]
    # -------------------------------------------------------------------------
    # Boy styles (shorts)
    # -------------------------------------------------------------------------
    'bbs1' : "básico com bolsos",
    'bbs2' : "cinto",
    'bbs3' : "cargo",
    'bbs4' : "havaiano",
    'bbs5' : "listras laterais (especial)",
    'bbs6' : "shorts de futebol",
    'bbs7' : "chamas laterais (especial)",
    'bbs8' : "brim",
    'vd_bs1' : "Shorts de dia dos namorados",
    'vd_bs2' : "Verde com coração vermelho",
    'vd_bs3' : "Brim azul com coração verde e vermelho",

    # Catalog only shorts
    'c_bs1' : "Laranja com listras laterais azuis",
    'c_bs2' : "Azul com listras e pregas douradas",
    'c_bs5' : 'Listras verdes - série 7',
    'sd_bs1' : 'Shorts de Duende de São Patrício',
    'pj_bs1' : 'Calça de Pijama de banana azul',
    'pj_bs2' : 'Calça de Pijama de chifre vermelho',
    'pj_bs3' : 'Calça de Pijama de óculos roxos',
    'wh_bs1' : 'Shorts de Feriado de Inverno Estilo 1',
    'wh_bs2' : 'Shorts de Feriado de Inverno Estilo 2',
    'wh_bs3' : 'Shorts de Feriado de Inverno Estilo 3',
    'wh_bs4' : 'Shorts de Feriado de Inverno Estilo 4',
    
    # -------------------------------------------------------------------------
    # Girl styles (shorts and skirts)
    # -------------------------------------------------------------------------
    # skirts
    # -------------------------------------------------------------------------
    'gsk1' : 'básica',
    'gsk2' : 'bolinhas (especial)',
    'gsk3' : 'listras verticais',
    'gsk4' : 'listra horizontal',
    'gsk5' : 'estampa de flor',
    'gsk6' : '2 bolsos (especial)',
    'gsk7' : 'saia de brim',
    
    # shorts
    # -------------------------------------------------------------------------
    'gsh1' : 'básico com bolsos',
    'gsh2' : 'florido',
    'gsh3' : 'shorts de brim',
    # Special catalog-only skirts and shorts.
    'c_gsk1' : 'saia azul com borda bege e botão ',
    'c_gsk2' : 'saia roxa com rosa e fita',
    'c_gsk3' : 'saia violeta com amarelo e estrela',

    # Valentines skirt
    'vd_gs1' : 'Saia vermelha com corações',
    'vd_gs2' : 'Saia rosa com corações',
    'vd_gs3' : 'Saia de brim azul com coração verde e vermelho',
    'c_gsk4' : 'Saia de arco-íris - Série 3',
    'sd_gs1' : 'Shorts de dia de São Patrício',
    'c_gsk5' : 'Saias de vaqueira 1',
    'c_gsk6' : 'Saias de vaqueira 2',
    # Western shorts
    'c_bs3' : 'Shorts de caubói 1',
    'c_bs4' : 'Shorts de caubói 2',
    'j4_bs1' : 'Shorts de 4 de julho',
    'j4_gs1' : 'Saia de 4 de julho',
    'c_gsk7' : 'Azul com flor - série 7',
    'pj_gs1' : 'Calça de Pijama de banana azul',
    'pj_gs2' : 'Calça de Pijama de chifre vermelho',
    'pj_gs3' : 'Calça de Pijama de óculos roxos',
    'wh_gsk1' : 'Saia de Feriado de Inverno Estilo 1',
    'wh_gsk2' : 'Saia de Feriado de Inverno Estilo 2',
    'wh_gsk3' : 'Saia de Feriado de Inverno Estilo 3',
    'wh_gsk4' : 'Saia de Feriado de Inverno Estilo 4',
    
    'sa_bs1' : "Shorts de Pesca",
    'sa_bs2' : "Shorts de Jardinagem",
    'sa_bs3' : "Shorts de Festa",
    'sa_bs4' : "Shorts de Corrida",
    'sa_bs5' : "Shorts de Verão",
    'sa_gs1' : "Saia de Pesca",
    'sa_gs2' : "Saia de Jardinagem",
    'sa_gs3' : "Saia de Festa",
    'sa_gs4' : "Saia de Corrida",
    'sa_gs5' : "Saia de Verão",
    }

AwardMgrBoy = "masculino"
AwardMgrGirl = "feminino"
AwardMgrUnisex = "unissex"
AwardMgrShorts = "shorts"
AwardMgrSkirt = "saia"
AwardMgrShirt = "camisa"

# Special Event Strings to display in  mailbox screen
SpecialEventMailboxStrings = {
    1 : "Um item especial do conselho Toon",
    2 : "Prêmio do Torneio de Pesca de Melville",
    3 : "Prêmio do Torneio de Pesca de Billy Bud",
    }

# Rental items"
RentalHours = "Horas de"
RentalOf = "De"
RentalCannon = "Canhões!"
RentalTime = "Horas de"
RentalGameTable = "Mesa de Jogo!"

EstateCannonGameEnd = "O aluguel do Jogo de Canhão acabou."
GameTableRentalEnd = "O aluguel da Mesa de Jogo acabou."

MessageConfirmRent = "Iniciar o aluguel? Cancele para guardar o aluguel para depois"
MessageConfirmGarden = "Você quer mesmo iniciar um jardim?"

#nametag Names
NametagPaid = "Crachá de Cidadão"
NametagAction = "Crachá de Ação"
NametagFrilly = "Crachá Chique"

FurnitureYourOldCloset = "seu armário velho"
FurnitureYourOldBank = "seu banco velho"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py
FurnitureNames = {
  100 : "Poltrona",
  105 : "Poltrona",
  110 : "Cadeira",
  120 : "Cadeira de escrivaninha",
  130 : "Cadeira de jardim",
  140 : "Cadeira lagosta",
  145 : "Cadeira salva-vidas",
  150 : "Banco de sela",
  160 : "Cadeira nativa",
  170 : "Cadeira-bolinho",
  200 : "Cama",
  205 : "Cama",
  210 : "Cama",
  220 : "Cama banheira",
  230 : "Cama de folhas",
  240 : "Cama-barco",
  250 : "Rede de cáctus",
  260 : "Cama de sorvete",
  270 : "Olivia Erin & Cat's Bed",
  300 : "Pianola",
  310 : "Órgão de tubo",
  400 : "Lareira",
  410 : "Lareira",
  420 : "Lareira redonda",
  430 : "Lareira",
  440 : "Lareira-maçã",
  450 : "Lareira Irlandesa",
  460 : "Lareira Irlandesa Acesa", 
  470 : "Lareira Acesa",
  480 : "Lareira Circular Acesa", 
  490 : "Lareira Acesa",
  491 : "Lareira Acesa",
  492 : "Lareira em Forma de Maçã Acesa",
  500 : "Armário",
  502 : "Armário com 15 itens",
  504 : "Armário com 20 itens",
  506 : "Armário com 25 itens",
  510 : "Armário",
  512 : "Armário com 15 itens",
  514 : "Armário com 20 itens",
  516 : "Armário com 25 itens",
  600 : "Abajur pequeno",
  610 : "Abajur grande",
  620 : "Abajur de mesa",
  625 : "Abajur de mesa",
  630 : "Abajur da Margarida",
  640 : "Abajur da Margarida",
  650 : "Abajur da Água-viva",
  660 : "Abajur da Água-viva",
  670 : "Abajur do vaqueiro",
  700 : "Cadeira estofada",
  705 : "Cadeira estofada",
  710 : "Sofá",
  715 : "Sofá",
  720 : "Sofá de feno",
  730 : "Sofá-torta",
  800 : "Escrivaninha",
  810 : "Mesinha",
  900 : "Porta-guarda-chuva",
  910 : "Cabideiro",
  920 : "Lata de lixo",
  930 : "Cogumelo vermelho",
  940 : "Cogumelo amarelo",
  950 : "Cabideiro",
  960 : "Mesinha-barril",
  970 : "Planta cáctus",
  980 : "Tenda",
  990 : "O Fan (Leque) de Julieta", 
  1000 : "Tapete grande",
  1010 : "Tapete redondo",
  1015 : "Tapete redondo",
  1020 : "Tapete pequeno",
  1030 : "Capacho de folha",
  1100 : "Vitrina",
  1110 : "Vitrina",
  1120 : "Estante alta",
  1130 : "Estante baixa",
  1140 : "Arca-sundae",
  1200 : "Mesinha lateral",
  1210 : "Mesa pequena",
  1215 : "Mesa pequena",
  1220 : "Mesinha de centro",
  1230 : "Mesinha de centro",
  1240 : "Mesa Snorkel",
  1250 : "Mesa-biscoito",
  1260 : "Mesa do quarto",
  1300 : "Banco 1.000 Balas",
  1310 : "Banco 2.500 Balas",
  1320 : "Banco 5.000 Balas",
  1330 : "Banco 7.500 Balas",
  1340 : "Banco 10.000 Balas",
  1399 : "Telefone",
  1400 : "Toon Cezanne",
  1410 : "Flores",
  1420 : "Mickey Moderno",
  1430 : "Toon Rembrandt",
  1440 : "Toonescape",
  1441 : "Cavalo Assobiador",
  1442 : "Estrela Toon",
  1443 : "Não é Torta",
  1450 : "Mickey é Minnie",
  1500 : "Rádio",
  1510 : "Rádio",
  1520 : "Rádio",
  1530 : "Televisão",
  1600 : "Vasinho",
  1610 : "Vaso alto",
  1620 : "Vasinho",
  1630 : "Vaso alto",
  1640 : "Vasinho",
  1650 : "Vasinho",
  1660 : "Vaso Coral",
  1661 : "Vaso de concha",
  1670 : "Rose Vase",
  1680 : "Rose Watercan",
  1700 : "Carrocinha de pipoca",
  1710 : "Joaninha",
  1720 : "Chafariz",
  1725 : "Lavadora de roupa",
  1800 : "Aquário",
  1810 : "Aquário",
  1900 : "Peixe-espada",
  1910 : "Tubarão-martelo",
  1920 : "Chifres de pendurar",
  1930 : "Sombreiro simples",
  1940 : "Sombreiro elegante",
  1950 : "Apanhador de sonhos",
  1960 : "Ferradura",
  1970 : "Retrato de búfalo",
  2000 : "Balanço de doces",
  2010 : "Escorregada de torta",
  3000 : "Banheira banana split",
  10000 : "Moranga",
  10010 : "Abóbora",
  10020 : "Árvore de Natal",
  10030 : "Guirlanda de Natal"
  }

# CatalogClothingItem.py
ClothingArticleNames = (
    "Camisa",
    "Camisa",
    "Camisa",
    "Bermuda",
    "Bermuda",
    "Saia",
    "Bermuda",
    )

ClothingTypeNames = {
    1400 : "Camisa do Mateus",
    1401 : "Camisa da Jéssica",
    1402 : "Camisa da Marisa",
    1600 : "Traje de Armadilha",
    1601 : "Traje de Som",
    1602 : "Traje de Isca",
    1603 : "Traje de Armadilha",
    1604 : "Traje de Som",
    1605 : "Traje de Isca",
    1606 : "Traje de Armadilha",
    1607 : "Traje de Som",
    1608 : "Traje de Isca",
    }

# CatalogSurfaceItem.py
SurfaceNames = (
    "Papel de parede",
    "Moldura do teto",
    "Piso",
    "Lambri",
    "Moldura",
    )

WallpaperNames = {
    1000 : "Pergaminho",
    1100 : "Milão",
    1200 : "Dover",
    1300 : "Vitória",
    1400 : "Newport",
    1500 : "Pastoral",
    1600 : "Arlequim",
    1700 : "Lua",
    1800 : "Estrelas",
    1900 : "Flores",
    2000 : "Jardim de primavera",
    2100 : "Jardim formal",
    2200 : "Dia de corrida",
    2300 : "Gol!",
    2400 : "Nuvem 9",
    2500 : "Trepadeira",
    2600 : "Primavera",
    2700 : "Boneca japonesa",
    2800 : "Arranjo de flores",
    2900 : "Peixe-anjo",
    3000 : "Bolhas",
    3100 : "Bolhas",
    3200 : "Ir pescar",
    3300 : "Parar de pescar",
    3400 : "Cavalo-marinho",
    3500 : "Conchinhas do mar",
    3600 : "Debaixo d'água",
    3700 : "Botinas",
    3800 : "Cáctus",
    3900 : "Chapéu de vaqueiro",
    10100 : "Gatos",
    10200 : "Morcegos",
    11000 : "Flocos de neve",
    11100 : "Folhas de Natal",
    11200 : "Boneco de neve",
    13000 : "Trevo",
    13100 : "Trevo",
    13200 : "Arco-íris",
    13300 : "Trevo",
    }

FlooringNames = {
    1000 : "Tábua-corrida",
    1010 : "Carpete",
    1020 : "Piso em losangos",
    1030 : "Piso em losangos",
    1040 : "Grama",
    1050 : "Tijolinho bege",
    1060 : "Tijolinho vermelho",
    1070 : "Piso quadrado",
    1080 : "Pedra",
    1090 : "Calçada",
    1100 : "Terra",
    1110 : "Sinteco",
    1120 : "Lajota",
    1130 : "Favo",
    1140 : "Água",
    1150 : "Piso praiano",
    1160 : "Piso praiano",
    1170 : "Piso praiano",
    1180 : "Piso praiano",
    1190 : "Areia",
    10000 : "Cubo de gelo",
    10010 : "Iglu",
    11000 : "Trevo",
    11010 : "Trevo",
    }

MouldingNames = {
    1000 : "Nós",
    1010 : "Pintado",
    1020 : "Dental",
    1030 : "Flores",
    1040 : "Flores",
    1050 : "Joaninha",
    }

WainscotingNames = {
    1000 : "Pintado",
    1010 : "Painel de madeira",
    1020 : "Madeira",
    }

# CatalogWindowItem.py--don't translate yet.
WindowViewNames = {
    10 : "Jardim amplo",
    20 : "Jardim selvagem",
    30 : "Jardim grego",
    40 : "Paisagem urbana",
    50 : "Velho Oeste",
    60 : "Fundo do mar",
    70 : "Ilha tropical",
    80 : "Noite estrelada",
    90 : "Piscina Tiki",
    100 : "Fronteira congelada",
    110 : "Fazenda",
    120 : "Campo Nativo",
    130 : "Rua Principal",
    }

# don't translate yet
NewCatalogNotify = "Há novos itens disponíveis para serem encomendados por telefone!"
NewDeliveryNotify = "Chegou correspondência nova em sua caixa de correio!"
CatalogNotifyFirstCatalog = "Seu primeiro catálogo chegou! Você pode usá-lo para encomendar novos itens para uso pessoal ou para casa."
CatalogNotifyNewCatalog = "O seu catálogo No. %s chegou! Você pode fazer os pedidos dos itens do catálogo pelo telefone."
CatalogNotifyNewCatalogNewDelivery = "Chegou correspondência nova em sua caixa de correio! Além disso, o seu catálogo No. %s chegou!"
CatalogNotifyNewDelivery = "Chegou correspondência nova em sua caixa de correio!"
CatalogNotifyNewCatalogOldDelivery = "O seu catálogo No. %s chegou, e ainda há itens aguardando por você em sua caixa de correio!"
CatalogNotifyOldDelivery = "Ainda há itens aguardando por você em sua caixa de correio!"
CatalogNotifyInstructions = "Clique no botão \"Ir para casa\" na Página do mapa em seu Álbum Toon e vá até o telefone que há dentro da sua casa."
CatalogNewDeliveryButton = "Nova\nentrega!"
CatalogNewCatalogButton = "Novo\ncatálogo"
CatalogSaleItem = "À venda!"

# don't translate yet
DistributedMailboxEmpty = "A sua caixa de correio está vazia no momento. Volte aqui para procurar entregas depois que você fizer um pedido pelo telefone!"
DistributedMailboxWaiting = "A sua caixa de correio está vazia no momento, mas o pacote que você encomendou está a caminho. Verifique mais tarde!"
DistributedMailboxReady = "Sua encomenda chegou!"
DistributedMailboxNotOwner = "Sinto muito, esta não é a sua caixa de correio."
DistributedPhoneEmpty = "Você pode usar qualquer telefone para encomendar itens especiais para uso pessoal ou para sua casa. Em breve, haverá novos itens disponíveis para pedidos.\n\nNão há nenhum item disponível para pedidos no momento, mas verifique novamente mais tarde!"

# don't translate yet
Clarabelle = "Clarabela"
MailboxExitButton = "Fechar caixa\nde correio"
MailboxAcceptButton = "Pegar este item"
MailBoxDiscard = "Remover este item"
MailboxAcceptInvite = "Aceitar convite"
MailBoxRejectInvite = "Recusar convite"
MailBoxDiscardVerify = "Você quer mesmo Remover %s?"
MailBoxRejectVerify = "Você quer mesmo Recusar %s?"
MailboxOneItem = "Sua caixa postal contém 1 item."
MailboxNumberOfItems = "Sua caixa postal contém %s itens."
MailboxGettingItem = "Pegando %s da caixa postal."
MailboxGiftTag = "Presente De: %s"
MailboxGiftTagAnonymous = "Anônimo"
MailboxItemNext = "Próximo\nitem"
MailboxItemPrev = "Item\nanterior"
MailboxDiscard = "Remover"
MailboxReject = "Recusar"
MailboxLeave = "Guardar"
CatalogCurrency = "balas"
CatalogHangUp = "Desligar"
CatalogNew = "NOVA"
CatalogBackorder = "ENCOMENDA"
CatalogLoyalty = "ESPECIAL"
CatalogPagePrefix = "Página"
CatalogGreeting = "Olá! Agradecemos sua ligação para o Catálogo da Clarabela. Posso ajudar?"
CatalogGoodbyeList = ["Agora tchau!",
                      "Ligue novamente em breve!",
                      "Agradecemos sua ligação!",
                      "Ok, agora tchau!",
                      "Tchau!",
                      ]
CatalogHelpText1 = "Vire a página para ver os itens à venda."
CatalogSeriesLabel = "Série %s"
CatalogGiftFor = "Comprar Presente para:"
CatalogGiftTo = "Para: %s"
CatalogGiftToggleOn = "Parar de\nPresentear"
CatalogGiftToggleOff = "Comprar\nPresentes"
CatalogGiftToggleWait = "Tentando!..."
CatalogGiftToggleNoAck = "Não Disponível"
CatalogPurchaseItemAvailable = "Parabéns pela nova compra! Você já pode usar o seu produto imediatamente."
CatalogPurchaseGiftItemAvailable = "Ótimo!  %s pode começar a usar o seu presente agora mesmo."
CatalogPurchaseItemOnOrder = "Parabéns! O produto será entregue em sua caixa de correio em breve."
CatalogPurchaseGiftItemOnOrder = "Ótimo! O seu presente para %s será entregue na caixa de correio dele."
CatalogAnythingElse = "Deseja mais alguma coisa hoje?"
CatalogPurchaseClosetFull = "O seu armário está cheio. Apesar disso, você pode comprar este item, mas se comprar, terá que excluir alguma coisa do seu armário para liberar espaço para o novo item, quando ele chegar.\n\nQuer comprar este item mesmo assim?" 
CatalogAcceptClosetFull = "O seu armário está cheio. Entre em casa e exclua alguma coisa do seu armário para liberar espaço para o item antes de retirá-lo da caixa de correio."
CatalogAcceptShirt = "Você está vestindo agora a sua nova camisa. O que você estava vestindo antes foi transferido para o seu armário."
CatalogAcceptShorts = "Você está vestindo agora o seu novo short. O que você estava vestindo antes foi transferido para o seu armário."
CatalogAcceptSkirt = "Você está vestindo agora a sua nova saia. A que você estava vestindo antes foi transferida para o seu armário."
CatalogAcceptPole = "Agora, você está pronto para pescar uns peixes maiores com sua nova vara!"
CatalogAcceptPoleUnneeded = "Você já tem uma vara de pescar melhor do que esta!"
CatalogAcceptChat = "Você ganhou uma nova frase de Chat rápido!"
CatalogAcceptEmote = "Você ganhou uma nova Emoção!"
CatalogAcceptBeans = "Você recebeu algumas balinhas!"
CatalogAcceptRATBeans = "A sua recompensa de recruta Toon chegou!"
CatalogAcceptNametag = "Seu novo crachá chegou!"
CatalogAcceptGarden = "Os seus materiais de jardim chegaram!"
CatalogAcceptPet = "Você ganhou um novo Truque de Rabisco!"
CatalogPurchaseHouseFull = "Sua casa está cheia. Apesar disso, você pode comprar este item, mas se comprar, terá que excluir alguma coisa da sua casa para liberar espaço para o novo item, quando ele chegar.\n\nQuer comprar este item mesmo assim?"
CatalogAcceptHouseFull = "Sua casa está cheia. Entre em casa e exclua alguma coisa de lá para liberar espaço para o item antes de retirá-lo da caixa de correio."
CatalogAcceptInAttic = "O seu novo item está agora no sótão. Você pode colocá-lo em casa entrando lá e clicando no botão \"Mover mobília\"."
CatalogAcceptInAtticP = "Os seus novos itens estão agora no sótão. Você pode colocá-los em casa entrando lá e clicando no botão \"Mover mobília\"."
CatalogPurchaseMailboxFull = "Sua caixa de correio está cheia! Você não poderá comprar este item até retirar alguns itens da caixa de correio para liberar espaço."
CatalogPurchaseGiftMailboxFull = "A caixa de correio de %s está cheia!  Você não pode comprar este item."
CatalogPurchaseOnOrderListFull = "Você tem itens demais encomendados no momento. Você não poderá encomendar mais nenhum item até que cheguem alguns já encomendados."
CatalogPurchaseGiftOnOrderListFull = "%s tem ítens demais encomendados."
CatalogPurchaseGeneralError = "Não foi possível encomendar o item devido a um erro interno no jogo: código de erro %s."
CatalogPurchaseGiftGeneralError = "Não foi possível dar o item de presente a %(friend)s por causa de algum erro interno de jogo: código de erro %(error)s."
CatalogPurchaseGiftNotAGift = "Este item não pôde ser enviado para %s porque seria uma vantagem injusta."
CatalogPurchaseGiftWillNotFit = "Este item não pôde ser enviado para %s porque não vai servir."
CatalogPurchaseGiftLimitReached = "Este item não pôde ser enviado para %s porque ele já o possui."
CatalogPurchaseGiftNotEnoughMoney = "Este item não pôde ser enviado para %s porque ele não pode pagar."
CatalogAcceptGeneralError = "Este item não pôde ser excluído da sua caixa de correio por causa de um erro interno do jogo: código do erro %s."
CatalogAcceptRoomError = "Você não tem espaço para isto. Você vai ter que se livrar de alguma coisa."
CatalogAcceptLimitError = "Você já tem o número máximo possível disto. Você vai ter que se livrar de alguma coisa."
CatalogAcceptFitError = "Isto não serve em você! Você o doa para Toons que precisam."
CatalogAcceptInvalidError = "Este item saiu da moda! Você o doa para Toons que precisam."

MailboxOverflowButtonDicard = "Remover"
MailboxOverflowButtonLeave = "Sair"

HDMoveFurnitureButton = "Mover\nmobília"
HDStopMoveFurnitureButton = "Mudança\nconcluída"
HDAtticPickerLabel = "No sótão"
HDInRoomPickerLabel = "Na sala"
HDInTrashPickerLabel = "Na lixeira"
HDDeletePickerLabel = "Excluir?"
HDInAtticLabel = "Sótão"
HDInRoomLabel = "Sala"
HDInTrashLabel = "Lixo"
HDToAtticLabel = "Enviar\npara o sótão"
HDMoveLabel = "Mover"
HDRotateCWLabel = "Girar para a direita"
HDRotateCCWLabel = "Girar para a esquerda"
HDReturnVerify = "Retornar este item para o sótão?"
HDReturnFromTrashVerify = "Retornar este item para o sótão, da lixeira?"
HDDeleteItem = "Clique em OK para enviar este item para a lixeira ou em Cancelar para mantê-lo."
HDNonDeletableItem = "Você não pode excluir itens deste tipo!"
HDNonDeletableBank = "Você não pode excluir o seu banco!"
HDNonDeletableCloset = "Você não pode excluir o seu armário!"
HDNonDeletablePhone = "Você não pode excluir o seu telefone!"
HDNonDeletableNotOwner = "Você não pode excluir as coisas de %s's!"
HDHouseFull = "Sua casa está cheia. Você precisa excluir algo mais de sua casa ou do sótão antes de recuperar este item da lixeira."

HDHelpDict = {
    "DoneMoving" : "Decoração da sala concluída.",
    "Attic" : "Mostrar lista de itens do sótão. O sótão armazena itens que não estão na sala.",
    "Room" : "Mostrar lista de itens da sala. Útil para encontrar itens perdidos.",
    "Trash" : "Mostrar itens da lixeira. Os itens mais antigos são excluídos após um tempo ou quando a lixeira fica cheia demais.",
    "ZoomIn" : "Tenha uma visão ampliada da sala.",
    "ZoomOut" : "Tenha uma visão reduzida da sala.",
    "SendToAttic" : "Envie o item de mobília atual para o sótão, para armazená-lo.",
    "RotateLeft" : "Vire para a esquerda.",
    "RotateRight" : "Vire para a direita.",
    "DeleteEnter" : "Alterne para o modo de exclusão.",
    "DeleteExit" : "Saia do modo de exclusão.",
    "FurnitureItemPanelDelete" : "Envie o item %s para a lixeira.",
    "FurnitureItemPanelAttic" : "Coloque o item %s na sala.",
    "FurnitureItemPanelRoom" : "Voltar o item %s para o sótão.",
    "FurnitureItemPanelTrash" : "Voltar o item %s para o sótão.",
    }

MessagePickerTitle = "Você tem frases demais. Para comprar o item\n\"%s\"\n você precisa escolher um deles para ser removido:"
MessagePickerCancel = lCancel
MessageConfirmDelete = "Tem certeza de que quer remover \"%s\" do menu de Chat rápido?"

CatalogBuyText = "Comprar"
CatalogRentText = "Alugar"
CatalogGiftText = "Presente"
CatalogOnOrderText = "Encomendado"
CatalogPurchasedText = "Já\ncomprado"
CatalogGiftedText = "Presenteado\nPara Você"
CatalogPurchasedGiftText = "Já\nRecebido"
CatalogMailboxFull = "Sem Espaço"
CatalogNotAGift = "Não é um Presente"
CatalogNoFit = "Não\nServe"
CatalogMembersOnly = "Somente para\nUsuários!"
CatalogSndOnText = "Som Ligado"
CatalogSndOffText = "Som Desligado"
CatalogPurchasedMaxText = "Já\ncomprado o máx."
CatalogVerifyRent = "Alugar %(item)s por %(price)s balinhas?"
CatalogVerifyGift = "Comprar %(item)s por %(price)s balinhas de presente para %(friend)s?"
CatalogVerifyPurchase = "Comprar o item %(item)s por %(price)s balinhas?"
CatalogOnlyOnePurchase = "Você só pode ter um destes itens de cada vez. Se comprar este aqui, ele substituirá os itens %(old)s.\n\nTem certeza de que quer comprar o item %(item)s por %(price)s balinhas?"
CatalogExitButtonText = "Desligar"
CatalogCurrentButtonText = "Para itens atuais"
CatalogPastButtonText = "Para itens antigos"

TutorialHQOfficerName = "Haroldo do Quartel"

# NPCToons.py
NPCToonNames = {
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : "Tom Tutorial",
    999 : "Costureiro Toon",
    1000 : lToonHQ,
    20001 : Flippy,

    #
    # Toontown Central
    #

    # Toontown Central Playground

    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "Banqueiro Beto",
    2003 : "Professor Paulo",
    2004 : "Cora, a Costureira",
    2005 : "Bibliotecário Bino",
    2006 : "Vendedor Alaor",
    2011 : "Vendedora Isadora",
    2007 : lHQOfficerM,
    2008 : lHQOfficerM,
    2009 : lHQOfficerF,
    2010 : lHQOfficerF,
    # NPCFisherman
    2012 : "Vendedor da Loja de Animais",
    2018 : "Estúpi...doo... Homem-DICA",
    # NPCPetClerks
    2013 : "Vendedor Pop",
    2014 : "Vendedora Elétrica",
    2015 : "Vendedor Molenga",
    # NPCPartyPerson
    2016 : "Planejador de Festa Abóbora", 
    2017 : "Planejadora de Festa Polly", 

    # Silly Street
    2101 : "Dentista Daniel",
    2102 : "Delegada Délis",
    2103 : "Gatinho Funga-funga",
    2104 : lHQOfficerM,
    2105 : lHQOfficerM,
    2106 : lHQOfficerF,
    2107 : lHQOfficerF,
    2108 : "Canária Mina de carvão",
    2109 : "Gugu Bolha",
    2110 : "Otto D'or",
    2111 : "Diego Dançante",
    2112 : "Dr. Tom",
    2113 : "Rolo, o Incrível",
    2114 : "Rosabela",
    2115 : "Pati Papel",
    2116 : "Brutus Crespo",
    2117 : "Dona Putrefata",
    2118 : "Bob Bobo",
    2119 : "Renata Rá Rá",
    2120 : "Professor Pimpão",
    2121 : "Madame Risadinha",
    2122 : "Toni Macacada",
    2123 : "Latônia Lata",
    2124 : "Massinha Mode Lar",
    2125 : "Ralf Desocupado",
    2126 : "Professora Gargalhada",
    2127 : "Nico Níquel",
    2128 : "Duda Doidinho",
    2129 : "Franco Furtado",
    2130 : "Felícia Ding-dong",
    2131 : "Espanadora Penas",
    2132 : "Joe Tromundo",
    2133 : "Dr. Fórico",
    2134 : "Simone Silêncio",
    2135 : "Karla Rossel",
    2136 : "Saulo Risadinha",
    2137 : "Alegria Alegre",
    2138 : "João",
    2139 : "Bebê Babá",
    2140 : "Gui Pescador",

    # Loopy Lane
    2201 : "Gerente Gil",
    2202 : "Shirley Vocezomba",
    2203 : lHQOfficerM,
    2204 : lHQOfficerM,
    2205 : lHQOfficerF,
    2206 : lHQOfficerF,
    2207 : "Saulo Sabichão",
    2208 : "Lucas Grude",
    2209 : "Rico Risada",
    2210 : "Chazinha",
    2211 : "Cláudia Cuspinho",
    2212 : "Estêvão Estranho",
    2213 : "Luciana da Roda",
    2214 : "Mano da Mancha",
    2215 : "Bob Bujão",
    2216 : "Kênia Teviu",
    2217 : "João Tubarão",
    2218 : "Hilária Folha",
    2219 : "Chef Cabeça de Vento",
    2220 : "Carlos Cabeça de Ferro",
    2221 : "Flora Canudinho",
    2222 : "Fusível Mirim",
    2223 : "Gláucia Gargalhada",
    2224 : "Fábio Fumacinha",
    2225 : "Corcunda Pescador",

    # Punchline Place
    2301 : "Dr. Puxaperna",
    2302 : "Professor Balanço",
    2303 : "Enfermeira Enferma",
    2304 : lHQOfficerM,
    2305 : lHQOfficerM,
    2306 : lHQOfficerF,
    2307 : lHQOfficerF,
    2308 : "Nancy Veneno",
    2309 : "João Grandão",
    2311 : "Francisco da Graça",
    2312 : "Dra. Sensível",
    2313 : "Lucinda Pinta",
    2314 : "Lúcio Lançador",
    2315 : "Tatá Tasco",
    2316 : "Bárbara Bola",
    2318 : "Ronaldo Engraçaldo",
    2319 : "Tiraldo",
    2320 : "Alfredo Nham",
    2321 : "Bartô Pescador",

    #
    # Donald's Dock
    #

    # Donald's Dock Playground
    1001 : "Vendedor Willy",
    1002 : "Vendedor Billy",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "Betão Calçalongas",
    # NPCFisherman
    1008 : "Vendedor da Loja de Animais",
    # NPCPetClerks
    1009 : "Vendedor Durão",
    1010 : "Vendedora Ron-ron",
    1011 : "Vendedora Blup",
    # NPCPartyPerson
    1012 : "Planejador de Festa Pickles", 
    1013 : "Planejador de Festa Patty", 

    # Barnacle Blvd.
    1101 : "Levi Legal",
    1102 : "Capitão Carlão",
    1103 : "Pedro Peixe",
    1104 : "Doutor Alá",
    1105 : "Almirante Gancho",
    1106 : "Dona Goma",
    1107 : "Carlo Caiado",
    1108 : lHQOfficerM,
    1109 : lHQOfficerF,
    1110 : lHQOfficerM,
    1111 : lHQOfficerF,
    1112 : "Gláucio Glubglub",
    1113 : "Adele Adernada",
    1114 : "Carlos Camarada",
    1115 : "Lúcia Lula",
    1116 : "Carla Craca",
    1117 : "Capitão Blargh",
    1118 : "Marinho Crespo",
    1121 : "Linda Terra Firme",
    1122 : "Salgado Pescado",
    1123 : "Enguia Elétrica",
    1124 : "João Farpa do Cais",
    1125 : "Arlene Além-mar",
    1126 : "Zé Silva Pescador",

    # Seaweed Street
    1201 : "Craca Bárbara",
    1202 : "Mário",
    1203 : "Salgado",
    1204 : "Marco Quebra-mar",
    1205 : lHQOfficerM,
    1206 : lHQOfficerF,
    1207 : lHQOfficerM,
    1208 : lHQOfficerF,
    1209 : "Professora Pranchinha",
    1210 : "Aiki Sopa",
    1211 : "Malo Mala",
    1212 : "Tomás Língua de Trapo",
    1213 : "Bob Botinho",
    1214 : "Kátia Furacão",
    1215 : "Paula Profundeza",
    1216 : "Otto Ostra",
    1217 : "Ciça Caniço",
    1218 : "Toni Pacífico",
    1219 : "Carlos Encalhado",
    1220 : "Carla Canal",
    1221 : "Alan Abrolhos",
    1222 : "Bob Abordo",
    1223 : "Lula Lulu",
    1224 : "Emília Enguia",
    1225 : "Estêvão Estivador",
    1226 : "Pedro Pé na Tábua",
    1227 : "Coral do Recife",
    1228 : "Junqueira Pescador",

    # Lighthouse Lane
    1301 : "Alice",
    1302 : "Moby",
    1303 : "Mário",
    1304 : "Martina",
    1305 : lHQOfficerM,
    1306 : lHQOfficerF,
    1307 : lHQOfficerM,
    1308 : lHQOfficerF,
    1309 : "Esponja do Mar",
    1310 : "Fernando Ferramenta",
    1311 : "Paulinha Ponta Cabeça",
    1312 : "Hélio Hélice",
    1313 : "Wilson Nó",
    1314 : "Fernando Enferrujado",
    1315 : "Doutora Correnteza",
    1316 : "Beth Rodopio",
    1317 : "Paula Poste",
    1318 : "Teófilo Bote",
    1319 : "Estácio Estaleiro",
    1320 : "Caio Calmaria",
    1321 : "Camila Cais",
    1322 : "Rachel Recheio",
    1323 : "Fred Fedido",
    1324 : "Pérola Profunda",
    1325 : "Sérgio Vira-latas",
    1326 : "Felícia Batatinha",
    1327 : "Cíntia Tábua",
    1328 : "Lucas Linguado",
    1329 : "Conchita Alga Marina",
    1330 : "Porta Dor",
    1331 : "Rudy Ridíquilhas",
    1332 : "Polar Pescador",

    #
    # The Brrrgh
    #

    # The Brrrgh Playground
    3001 : "Frida Freezer",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "Vendedor Breno",
    3007 : "Vendedora Brenda",
    3008 : "Paco Pacote",
    # NPCFisherman
    3009 : "Vendedor da Loja de Animais",
    # NPCPetClerks
    3010 : "Vendedor Saltitante",
    3011 : "Vendedora Glub",
    3012 : "Vendedor Kiko",
    # NPCPartyPerson
    3013 : "Planejador de Festa Pedro", 
    3014 : "Planejador de Festa Penny", 

    # Walrus Way
    3101 : "Seu Leão",
    3102 : "Tia Freezer",
    3103 : "Chicó",
    3104 : "Gorrete",
    3105 : "Fred Cavanhaque",
    3106 : "Pio Arrepio",
    3107 : "Patty Passaporte",
    3108 : "Tobi Tobogã",
    3109 : "Kate",
    3110 : "Franguinho",
    3111 : "Cão de Bico",
    3112 : "Pequeno Grande Ancião",
    3113 : "Américo Histérico",
    3114 : "Rico Arriscado",
    3115 : lHQOfficerM,
    3116 : lHQOfficerF,
    3117 : lHQOfficerM,
    3118 : lHQOfficerM,
    3119 : "Carlos K. B. Loempé",
    3120 : "Kiko Quiprocó",
    3121 : "João Eletrochoque",
    3122 : "Luci Lugar",
    3123 : "Francis Quebra Gelo",
    3124 : "Estileto Iceberg",
    3125 : "Coronel Mastiga",
    3126 : "João Jornada",
    3127 : "Aérea Inflada",
    3128 : "Jorge Palitinho",
    3129 : "Fátima Fôrma",
    3130 : "Sandy",
    3131 : "Patrício Preguiça",
    3132 : "Maria Cinza",
    3133 : "Dr. Congelado",
    3134 : "Vítor Vestíbulo",
    3135 : "Ênia Sopada",
    3136 : "Susana Nimada",
    3137 : "Sr. Freezer",
    3138 : "Chefe Sopa Rala",
    3139 : "Vovó Ceroulas",
    3140 : "Luci Pescadora",

    # Sleet Street
    3201 : "Tia Ártica",
    3202 : "Tremendão",
    3203 : "Walter",
    3204 : "Dra. Vai C. V.",
    3205 : "Cabeção Kika",
    3206 : "Vidália VaVum",
    3207 : "Dr. Ban Guela",
    3208 : "Felipe Nervosinho",
    3209 : "Marcos Cem Graça",
    3210 : "Álvaro Asno",
    3211 : "Hilária Freezer",
    3212 : "Rogério Gélido",
    3213 : lHQOfficerM,
    3214 : lHQOfficerF,
    3215 : lHQOfficerM,
    3216 : lHQOfficerM,
    3217 : "Consuelo Suada",
    3218 : "Lu Lazul",
    3219 : "Bob BikeDupla",
    3220 : "Sr. Espirro",
    3221 : "Neli Neve",
    3222 : "Vera Vento Cortante",
    3223 : "Chapa",
    3224 : "Rita Raspadinha",
    3225 : "Foca Fofoca",
    3226 : "Papai Nó El",
    3227 : "Raiomundo de Sol",
    3228 : "Frida Calafrio",
    3229 : "Hermínia Cinta",
    3230 : "Pedro Pedreira",
    3231 : "G. Lopicado",
    3232 : "Pescador Alberto",

    # Polar Place
    3301 : "Remendo Tecidos",
    3302 : "Pedro Urso",
    3303 : "Dr. Olhadelas",
    3304 : "Abrão o Abominável",
    3305 : "Mick Eimei",
    3306 : "Paula Úrsula",
    # NPC Fisherman
    3307 : "Pescadora Frederica",
    3308 : "Roberto Injustus",
    3309 : "Botinha",
    3310 : "Professor Floco",
    3311 : "Connie Feras",
    3312 : "Haroldo Marcha",
    3313 : lHQOfficerM,
    3314 : lHQOfficerF,
    3315 : lHQOfficerM,
    3316 : lHQOfficerF,
    3317 : "Bete Beijoqueira",
    3318 : "João Caxemira",
    3319 : "Reinaldo Retifica",
    3320 : "Ester Espuma",
    3321 : "Paulo Picareta",
    3322 : "Luis Fluis",
    3323 : "Aurora Borealis",
    3324 : "Otto Dentetorto",
    3325 : "Dercy Balançalves",
    3326 : "Blanche",
    3327 : "Cacá Sado",
    3328 : "Sônia Sombria",
    3329 : "Edu Pisada",

    #
    # Minnie's Melody Land
    #

    # Minnie's Melody Land Playground
    4001 : "Mel Odia",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "Vendedora Do-ré-mi",
    4007 : "Vendedor Fá-sol-lá-si",
    4008 : "Costureira Harmonia",
    # NPCFisherman
    4009 : "Vendedor da Loja de Animais",
    # NPCPetClerks
    4010 : "Vendedor Caco",
    4011 : "Vendedor Nilton",
    4012 : "Vendedora Flor do Nordeste",
    # NPCPartyPerson
    4013 : "Planejador de Festa Preston", 
    4014 : "Planejadora de Festa Penélope", 

    # Alto Ave.
    4101 : "Tom",
    4102 : "Fifi",
    4103 : "Dr. Triturador",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "Clave",
    4109 : "Carlos",
    4110 : "Métrica Anã",
    4111 : "Tom Tum",
    4112 : "Fá",
    4113 : "Madame Boa Maneira",
    4114 : "Bino Desafino",
    4115 : "Bárbara de Sevilha",
    4116 : "Flávio Flautim",
    4117 : "Banda Lyn",
    4118 : "Faxineiro Abel",
    4119 : "Moz Arte",
    4120 : "Violante Almofada",
    4121 : "Gegê Menor",
    4122 : "Mentolada do Baixo",
    4123 : "André Raio",
    4124 : "Renato Refrão",
    4125 : "Ondina Musical",
    4126 : "Melô Canto",
    4127 : "Felícia Podos",
    4128 : "Luciano Furo",
    4129 : "Carla Cadência",
    4130 : "Miguel Metal",
    4131 : "Abraão Armário",
    4132 : "Marta Marrom",
    4133 : "Paulo Popeline",
    4134 : "Davi Disco",
    4135 : "Carlo Canoro",
    4136 : "Patrícia Pausa",
    4137 : "Toni Surdo",
    4138 : "Agudo Clave",
    4139 : "Harmonia Decrescente",
    4140 : "Daniel Desajeitado",
    4141 : "Pet Pescador",

    # Baritone Blvd.
    4201 : "Tina",
    4202 : "Barry",
    4203 : "Alê Nhador",
    4204 : lHQOfficerM,
    4205 : lHQOfficerF,
    4206 : lHQOfficerF,
    4207 : lHQOfficerF,
    4208 : "Heidi",
    4209 : "Brega Galopante",
    4211 : "Carlo Concerto",
    4212 : "Detetive Marcha Fúnebre",
    4213 : "Franca Foley",
    4214 : "Paula Meia-ponta",
    4215 : "Mário Marcha a ré",
    4216 : "Bob Buzina",
    4217 : "Toni Bonitão",
    4218 : "Sônia Soprano",
    4219 : "Bruno Barítono",
    4220 : "Dênis Dedus",
    4221 : "Marcos Madrigal",
    4222 : "João da Silva",
    4223 : "Pâmela Ponto",
    4224 : "Jim das Selvas",
    4225 : "Vânia Vaia",
    4226 : "Samantha Garganta",
    4227 : "Cláudia Calada",
    4228 : "Augusto de Sopro",
    4229 : "Júnia Bombom",
    4230 : "Marcelo Martelo",
    4231 : "Stefanie Acordes",
    4232 : "Helder Hino",
    4233 : "Enzo Enjoado",
    4234 : "Mestre Guitarra",
    4235 : "Lauro Pescador",

    # Tenor Terrace
    4301 : "Cavaca",
    4302 : "Ana",
    4303 : "Léo",
    4304 : lHQOfficerM,
    4305 : lHQOfficerF,
    4306 : lHQOfficerF,
    4307 : lHQOfficerF,
    4308 : "Tábata",
    4309 : "Punk Ecas",
    4310 : "Mezza Soprana",
    4311 : "Chica Shake",
    4312 : "Paulo Palheta",
    4313 : "Mário Mudo",
    4314 : "Danuza Uza",
    4315 : "Maritza Tique Ataque",
    4316 : "Toni Tango",
    4317 : "Dedo Curto",
    4318 : "Bob Marlin",
    4319 : "Cátia Zuza",
    4320 : "Roberta P. Rock",
    4321 : "Edinho Verde",
    4322 : "Antoniota Musical",
    4323 : "Bárbara Balado",
    4324 : "Elen",
    4325 : "Ralf Rádio",
    4326 : "Kíria Irrita",
    4327 : "Armínia Arranca Pele",
    4328 : "Wagner",
    4329 : "Teles Prompter",
    4330 : "Quarentino",
    4331 : "Mello Costello",
    4332 : "Ziggy",
    4333 : "Ubaldo",
    4334 : "Estêvão Expresso",
    4335 : "Sílvia Pescadora",

    #
    # Daisy Gardens
    #

    # Daisy Gardens Playground
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "Vendedora Moranguinho",
    5006 : "Vendedor Herbal",
    5007 : "Florinda Flores",
    # NPCFisherman
    5008 : "Vendedor da Loja de Animais",
    # NPCPetClerks
    5009 : "Vendedora Buba Tânica",
    5010 : "Vendedor Tony Grana",
    5011 : "Vendedor Duda Madeira",
    # NPCPartyPerson
    5012 : "Planejador de Festa Pierce", 
    5013 : "Planejadora de Festa Peggy", 

    # Elm Street
    5101 : "Sérgio",
    5102 : "Susana",
    5103 : "Florêncio",
    5104 : "Borba Oleta",
    5105 : "João",
    5106 : "Barbeiro Tosque Ador",
    5107 : "Carteiro Felipe",
    5108 : "Funcionária Janete",
    5109 : lHQOfficerM,
    5110 : lHQOfficerM,
    5111 : lHQOfficerF,
    5112 : lHQOfficerF,
    5113 : "Dra. Ália e Ólea",
    5114 : "Al Fácio Murcho",
    5115 : "Lua de Melão",
    5116 : "Vítor Vegetal",
    5117 : "Pétala",
    5118 : "Pipo K.",
    5119 : "João Medalhão",
    5120 : "Toupeira",
    5121 : "Emília Ervilha",
    5122 : "J. Jardim",
    5123 : "Diana Uva",
    5124 : "Olavo Orvalho",
    5125 : "Chu Chuá",
    5126 : "Madame Calado",
    5127 : "Poliana Pólen",
    5128 : "Suzana Seiva",
    5129 : "Salgueira Pescadora",

    # Maple Street
    5201 : "Joãozinho",
    5202 : "Cíntia",
    5203 : "Lisa",
    5204 : "Ubaldo",
    5205 : "Maurício Leão",
    5206 : "Branco Vinho",
    5207 : "Sofia Seiva",
    5208 : "Samanta Pá",
    5209 : lHQOfficerM,
    5210 : lHQOfficerM,
    5211 : lHQOfficerF,
    5212 : lHQOfficerF,
    5213 : "Nabo Bobo",
    5214 : "Empolada Alérgica",
    5215 : "Clara Caules",
    5216 : "Fernando Fedido",
    5217 : "Vítor do Dedo Verde",
    5218 : "Francisco Framboesa",
    5219 : "Bi Ceps",
    5220 : "Luci Calçola",
    5221 : "Rosinha Flamingo",
    5222 : "Sandra Samambaia",
    5223 : "Paulo Ensopado",
    5224 : "Tio Camponês",
    5225 : "Pâmela Pântana",
    5226 : "Mauro Musgo",
    5227 : "Begônia Malte",
    5228 : "Drago Di Lama",
    5229 : "Lili Pescadora",

    # Oak street
    5301 : lHQOfficerM,
    5302 : lHQOfficerM,
    5303 : lHQOfficerM,
    5304 : lHQOfficerM,
    5305 : "Cristal",
    5306 : "C. Postal",
    5307 : "Mo Fus",
    5308 : "Nely Nervo",
    5309 : "Rô Mann",
    5310 : "Timóteo",
    5311 : "Juíza Gala",
    5312 : "Eugênio",
    5313 : "Treinador Abobrinha",
    5314 : "Tia Miga",
    5315 : "Tio Lama",
    5316 : "Tio Batatinha",
    5317 : "Detetive Linda",
    5318 : "César",
    5319 : "Rose",
    5320 : "Márcia",
    5321 : "Professora Uva",
    5322 : "Rose Pescadora",

    #
    # Goofy's Speedway
    #

    #default  area
    #kart clerk
    8001 : "Grandep Rêmio",
    8002 : "Keruk Orrê",
    8003 : "Precisuv Encer",
    8004 : "En Chaela",

    #
    # Dreamland
    #

    # Dreamland Playground
    9001 : "Susana Pestana",
    9002 : "Dor Minhoco",
    9003 : "Sono Lento",
    9004 : lHQOfficerF,
    9005 : lHQOfficerF,
    9006 : lHQOfficerM,
    9007 : lHQOfficerM,
    9008 : "Vendedora Resona",
    9009 : "Vendedor Kisono",
    9010 : "Ultraje Velho",
    # NPCFisherman
    9011 : "Vendedor da Loja de Animais",
    # NPCPetClerks
    9012 : "Vendedora Sara Soneca",
    9013 : "Vendedora Gata na Lata",
    9014 : "Vendedor Cara Mujo",
    # NPCPartyPerson
    9015 : "Planejador de Festa Pebbles (Pedregulho)", 
    9016 : "Planejadora de Festa Pérola", 

    # Lullaby Lane
    9101 : "Marcelo",
    9102 : "Mama",
    9103 : "Py Jama",
    9104 : "Dulce Lombra",
    9105 : "Professor Bocejo",
    9106 : "Máximo",
    9107 : "Aurora Ninho",
    9108 : "Pedro Pestana",
    9109 : "Dafne Sonolinda",
    9110 : "Gatária Soneca",
    9111 : "Elle Étrica",
    9112 : "Denis Nar",
    9113 : "Tique Eustáquio",
    9114 : "Máki Agem",
    9115 : "Nenê Crespo",
    9116 : "Dança com Carneirinhos",
    9117 : "Aurora Extra",
    9118 : "Celeste Estrelada",
    9119 : "Pedro",
    9120 : "Lúcia Lenta",
    9121 : "Serena Lençol Curto",
    9122 : "Paulo Pregado",
    9123 : "Ursolino de P. Lúcia",
    9124 : "Nana de Nina",
    9125 : "Dr. Turvo",
    9126 : "Jatha Cordada",
    9127 : "Tati U. Nidos",
    9128 : "Pedro Fuso",
    9129 : "Cátia Colcha",
    9130 : "Nico Penico",
    9131 : "Célia Sesta",
    9132 : lHQOfficerF,
    9133 : lHQOfficerF,
    9134 : lHQOfficerF,
    9135 : lHQOfficerF,
    9136 : "Tainha Pescador",

    # Pajama Place
    9201 : "Bernardo",
    9202 : "Carneiro",
    9203 : "Zezé",
    9204 : "Clara da Lua",
    9205 : "Bob Bocão",
    9206 : "Petra Pétala",
    9207 : "Denise Dreno",
    9208 : "Solano Sonolento",
    9209 : "Dr. Sedoso",
    9210 : "Mestre Mário",
    9211 : "Aurora",
    9212 : "Raio de Lua",
    9213 : "Gustavo Galo",
    9214 : "Dr. Soneca",
    9215 : "Dedé Descanso",
    9216 : "Cuca",
    9217 : "Linda Legal",
    9218 : "Matilda Madruga",
    9219 : "Condessa",
    9220 : "Ney Nervoso",
    9221 : "Zéfiro",
    9222 : "Vaqueiro George",
    9223 : "Vado Levado",
    9224 : "Cuca P. Gol",
    9225 : "Henriqueta Inquieta",
    9226 : "Guilherme Sonoleve",
    9227 : "Carlos Cabeceira",
    9228 : "Samuel Suspiro",
    9229 : "Rosa Sonada",
    9230 : "Lelê",
    9231 : "Régis Rede",
    9232 : "Lua de Mel",
    9233 : lHQOfficerM,
    9234 : lHQOfficerM,
    9235 : lHQOfficerM,
    9236 : lHQOfficerM,
    9237 : "Jung Pescador",

    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# These building titles are output from the DNA files
# Run ppython $TOONTOWN/src/dna/DNAPrintTitles.py to generate this list
# DO NOT EDIT THE ENTRIES HERE -- EDIT THE ORIGINAL DNA FILE
zone2TitleDict = {
    # titles for: phase_4/dna/toontown_central_sz.dna
    2513 : ("PrefeiToona", ""),
    2514 : ("Banco de Toontown", ""),
    2516 : ("Escola de Toontown", ""),
    2518 : ("Biblioteca de Toontown", ""),
    2519 : (lGagShop, ""),
    2520 : (lToonHQ, ""),
    2521 : (lClothingShop, ""),
    2522 : (lPetShop, ""),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("Restaurações Dentárias Todo Sorrisos", ""),
    2602 : ("", ""),
    2603 : ("Mineradores Espirituosos", ""),
    2604 : ("Lavanderia Lavou está Novo", ""),
    2605 : ("Fábrica de Sinalização de Toontown", ""),
    2606 : ("", ""),
    2607 : ("Feijões Saltadores", ""),
    2610 : ("Dr. Tom Besteira", ""),
    2611 : ("", ""),
    2616 : ("Loja de Disfarces Bigode Bizarro", ""),
    2617 : ("Feitos Idiotas", ""),
    2618 : ("A Encarnação Deve Continuar", ""),
    2621 : ("Aviões de Papel", ""),
    2624 : ("Brutamontes Felizes", ""),
    2625 : ("Casa da Torta Azeda", ""),
    2626 : ("Restauração de Piadas do Bob", ""),
    2629 : ("A Casa da Risada", ""),
    2632 : ("Curso de Palhaços", ""),
    2633 : ("Casa de Chá Chapinha", ""),
    2638 : ("Casa de Brinquedos de Toontown", ""),
    2639 : ("Truques e Macaquices", ""),
    2643 : ("Conservas Conservadas", ""),
    2644 : ("Pregadinhas de Peça", ""),
    2649 : ("Loja de Diversões e Jogos", ""),
    2652 : ("", ""),
    2653 : ("", ""),
    2654 : ("Curso de Risada", ""),
    2655 : ("Financeira Dinheiro Feliz", ""),
    2656 : ("Carros de Palhaço Usados", ""),
    2657 : ("Pegadinhas do Franco", ""),
    2659 : ("Campainhas Ding-dong para o Mundo", ""),
    2660 : ("Máquinas de Cosquinhas", ""),
    2661 : ("Doces Joe", ""),
    2662 : ("Dr. E. U. Fórico", ""),
    2663 : ("Cinerama de Toontown", ""),
    2664 : ("Mímicas Divertidas", ""),
    2665 : ("Agência de Viagens K. Rossel", ""),
    2666 : ("Posto de Gás Hilariante", ""),
    2667 : ("A Folha da Alegria", ""),
    2669 : ("Balões do João", ""),
    2670 : ("Sopa no Garfo", ""),
    2671 : ("", ""),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("Cinemas Multiplex", ""),
    2705 : ("Instrumentos Barulhentos do Sabichão", ""),
    2708 : ("Cola Azul", ""),
    2711 : ("Correio de Toontown", ""),
    2712 : ("Café do Risada", ""),
    2713 : ("Café da Madrugargalhada", ""),
    2714 : ("CinePlex Lesado", ""),
    2716 : ("Sopas e Surtos", ""),
    2717 : ("Latas engarrafadas", ""),
    2720 : ("Oficina do Chilique", ""),
    2725 : ("", ""),
    2727 : ("Garrafas e Conservas do Gasoso", ""),
    2728 : ("Sorvete Sumiço", ""),
    2729 : ("Peixinhos Dourados Ki-late", ""),
    2730 : ("Notícias Divertidas", ""),
    2731 : ("", ""),
    2732 : ("Espaguete Maluquete", ""),
    2733 : ("Pipas de Ferro", ""),
    2734 : ("Copos de Leite Chupa-chupa", ""),
    2735 : ("Casa do Cabum", ""),
    2739 : ("Restauração de Gargalhadas", ""),
    2740 : ("Rojões Usados", ""),
    2741 : ("", ""),
    2742 : ("", ""),
    2743 : ("Lavagem a Seco Beca", ""),
    2744 : ("", ""),
    2747 : ("Tinta Visível", ""),
    2748 : ("Zombarias para Gargalhadas", ""),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("Estofados Iupii", ""),
    2802 : ("Bolas de Ferro Infláveis", ""),
    2803 : ("Karnaval Kid", ""),
    2804 : ("Dr. Puxaperna, Ortopedista", ""),
    2805 : ("", ""),
    2809 : ("Academia Graça da Piada", ""),
    2814 : ("Teatro de Toontown", ""),
    2818 : ("A Torta Voadora", ""),
    2821 : ("", ""),
    2822 : ("Sanduíches de Frango de Borracha", ""),
    2823 : ("Sorvetes e Sundaes Divertidos", ""),
    2824 : ("Cinema Palácio do Auge da Graça", ""),
    2829 : ("Truques e Trocadilhos", ""),
    2830 : ("Tiradas Rápidas", ""),
    2831 : ("Casa do Sorriso Amarelo do Professor Balanço", ""),
    2832 : ("", ""),
    2833 : ("", ""),
    2834 : ("Sala de Emergência Osso Bom", ""),
    2836 : ("", ""),
    2837 : ("Centro de Estudos Rá Rá Rá", ""),
    2839 : ("Grude Massas", ""),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : (lGagShop, ""),
    1507 : (lToonHQ, ""),
    1508 : (lClothingShop, ""),
    1510 : (lPetShop, ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("Salva-vidas Usados", ""),
    1604 : ("Lavagem a Seco Roupa de Mergulho", ""),
    1606 : ("Conserto de Relógios do Gancho", ""),
    1608 : ("Bugigangas a Vela", ""),
    1609 : ("Iscas e Petiscos", ""),
    1612 : ("Banco Moedinha no Convés", ""),
    1613 : ("Lula Ki Pro Quo, Advogados", ""),
    1614 : ("Butique Unha Afiada", ""),
    1615 : ("E aí, Galera?", ""),
    1616 : ("Salão de Beleza Barba Azul", ""),
    1617 : ("Ótica Olha Lá", ""),
    1619 : ("Arboristas Desembarcar!", ""),
    1620 : ("Da Proa à Popa", ""),
    1621 : ("Academia Castelo de Popa", ""),
    1622 : ("Artigos Elétricos Isca Interruptora", ""),
    1624 : ("Reparos de Pescadas na Hora", ""),
    1626 : ("Roupas de Gala Salmão Encantado", ""),
    1627 : ("Atacado de Bússolas do Levi Legal", ""),
    1628 : ("Pianos Atum", ""),
    1629 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1200.dna
    1701 : ("Creche Peixinho Feliz", ""),
    1703 : ("Restaurante China Prancha", ""),
    1705 : ("Velas à Venda", ""),
    1706 : ("Pasta de Amendoim e Água-viva", ""),
    1707 : ("Presentes Golfinho Fofinho", ""),
    1709 : ("Veleiros e Gelatinas", ""),
    1710 : ("Liquidação das Cracas", ""),
    1711 : ("Restaurante Fundo do Mar", ""),
    1712 : ("Academia da Geração Saúde", ""),
    1713 : ("Mercado Carta Marinha do Mário", ""),
    1714 : ("Hotel do Otto", ""),
    1716 : ("Roupas de Banho Sereias", ""),
    1717 : ("Curso de Navegação Águas do Pacífico", ""),
    1718 : ("Serviços de Táxi Banco de Areia", ""),
    1719 : ("Empresas Correntes do Sul", ""),
    1720 : ("A Loja do Molinete", ""),
    1721 : ("Armarinho Marinho", ""),
    1723 : ("Alga Marinha do Lula", ""),
    1724 : ("A Enguia Moderna", ""),
    1725 : ("Centro de Caranguejos Pré-fabricados do Salgado", ""),
    1726 : ("Cerveja Preta Flutuante", ""),
    1727 : ("Rema aqui, Rema lá", ""),
    1728 : ("Caranguejos-ferradura Boa Sorte", ""),
    1729 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1300.dna
    1802 : ("Nada como Náutica", ""),
    1804 : ("Ginásio Mexilhão da Praia", ""),
    1805 : ("Caixa de Ferramentas Lanches", ""),
    1806 : ("Loja de Chapéus Emborcado", ""),
    1807 : ("Loja do Hélice", ""),
    1808 : ("Nós Samãe", ""),
    1809 : ("Balde Enferrujado", ""),
    1810 : ("Administração de Âncoras", ""),
    1811 : ("Canoa para Lá, Canoa para Cá?", ""),
    1813 : ("Pressão do Pier Consultoria", ""),
    1814 : ("Parada do Ó", ""),
    1815 : ("Qual é, galerinha?", ""),
    1818 : ("Café dos Sete Mares", ""),
    1819 : ("Restaurante Cais", ""),
    1820 : ("Loja de Pegadinhas Linha e Anzol", ""),
    1821 : ("Conservas Rei Netuno", ""),
    1823 : ("Assados Ostra", ""),
    1824 : ("Remo Cachorrinho", ""),
    1825 : ("Mercado de Peixes Cavala Trotante!", ""),
    1826 : ("Armários Embutidos do Mário Metido", ""),
    1828 : ("Mansão da Alice Cascalhão", ""),
    1829 : ("Loja de Esculturas Piscicultura", ""),
    1830 : ("Linguados e Perdidos", ""),
    1831 : ("Alga Mais em sua Casa", ""),
    1832 : ("Hipermercado Mastro do Moby", ""),
    1833 : ("Alfaiataria sob Medida Seu Mastro", ""),
    1834 : ("Ridíquilhas!", ""),
    1835 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : (lGagShop, ""),
    4504 : (lToonHQ, ""),
    4506 : (lClothingShop, ""),
    4508 : (lPetShop, ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Baterias do Tomtom", ""),
    4604 : ("A Quatro Mãos", ""),
    4605 : ("Violinos da Fifi", ""),
    4606 : ("Casa da Castanhola", ""),
    4607 : ("Trajes de Gala Toon", ""),
    4609 : ("Teclas de Piano Dó-ré-mi", ""),
    4610 : ("O Bom Refrão", ""),
    4611 : ("Faqueiros Diapasão", ""),
    4612 : ("Clínica Dentária Dr. Triturador", ""),
    4614 : ("Barbearia Musical", ""),
    4615 : ("Pizza do Flautim", ""),
    4617 : ("Bandolins Animados", ""),
    4618 : ("Banheiros Públicos", ""),
    4619 : ("Mar Cação", ""),
    4622 : ("Travesseiros Descanso de Queixo", ""),
    4623 : ("Afiação Bemol", ""),
    4625 : ("Pasta de Dente Tuba", ""),
    4626 : ("Notas Musicais", ""),
    4628 : ("Seguradora Acidental", ""),
    4629 : ("Pratos de Papel Refrão", ""),
    4630 : ("A Música é o nosso Forte", ""),
    4631 : ("Auxílio Canto Neiras", ""),
    4632 : ("Loja do Rock", ""),
    4635 : ("Notícias do Tenor", ""),
    4637 : ("A Boa Escala", ""),
    4638 : ("Loja do Heavy Metal", ""),
    4639 : ("Antiguidades Oitenta", ""),
    4641 : ("Jornal dos Blues", ""),
    4642 : ("Lavagem a Seco Beca", ""),
    4645 : ("Clube 88", ""),
    4646 : ("", ""),
    4648 : ("Mudanças Carregando Toons", ""),
    4649 : ("", ""),
    4652 : ("Loja de Conveniência Ponto Final", ""),
    4653 : ("", ""),
    4654 : ("Telhados Volume Perfeito", ""),
    4655 : ("Escola de Culinária do Terrível Chef Agudo", ""),
    4656 : ("", ""),
    4657 : ("Barbearia Quarteto", ""),
    4658 : ("Pianos Submersos", ""),
    4659 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("Escola de Dança Jumento Sentimento", ""),
    4702 : ("Timbre! Artigos para Lenhadores", ""),
    4703 : ("A Mala Madeus", ""),
    4704 : ("Concertos de Concertina da Tina", ""),
    4705 : ("Zarpou fora", ""),
    4707 : ("Estúdio de Efeitos Sonoros Doppler", ""),
    4709 : ("Artigos de Montanhismo Pliê", ""),
    4710 : ("Auto-escola Pouca Polca", ""),
    4712 : ("Borracharia Dó do Murcho", ""),
    4713 : ("Moda Fina Masculina Desafina", ""),
    4716 : ("Gaitas de Quatro Segmentos", ""),
    4717 : ("Seguradora de Automóveis Barateira Barítono", ""),
    4718 : ("Peças para Chopp-in e Outros Artigos para Cozinha", ""),
    4719 : ("Casas-móveis Madrigal", ""),
    4720 : ("Dê um Nome a este Toon", ""),
    4722 : ("Substitutos Abertura", ""),
    4723 : ("Artigos para Parquinhos Infantis Ex-condesconde", ""),
    4724 : ("Moda Infantil Inci Dental", ""),
    4725 : ("O Barbeiro Barítono", ""),
    4727 : ("Bordados Corda Vocal", ""),
    4728 : ("Solo Vocal Não dá pra Ouvir", ""),
    4729 : ("Livraria Oboé", ""),
    4730 : ("Sebo de Letras de Músicas", ""),
    4731 : ("Tons dos Toons", ""),
    4732 : ("Companhia Teatral Prega Peça", ""),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("Acorde Não!", ""),
    4736 : ("Planejamento Matrimonial Casal Hino Esperado", ""),
    4737 : ("Lonas Harpa", ""),
    4738 : ("Presentes Cantata do Tatá", ""),
    4739 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("Ponto do Punk", ""),
    4803 : ("Serviços de Governança Que Mezza!", ""),
    4804 : ("Curso de Barman Shake Shake Shake", ""),
    4807 : ("Não Quebre o Braço", ""),
    4809 : ("Não Com Verso!", ""),
    4812 : ("", ""),
    4817 : ("Loja de Animais Trin Canário", ""),
    4819 : ("Cavaquinhos da Cavaca", ""),
    4820 : ("", ""),
    4821 : ("Cruzeiros da Ana", ""),
    4827 : ("Relógios Ritmo Cadente", ""),
    4828 : ("Sapatos Masculinos Rima", ""),
    4829 : ("Bolas de Canhão Vaga Ner", ""),
    4835 : ("Fundamentos Musicais para Felinos Felizes", ""),
    4836 : ("Regalias do Reggae", ""),
    4838 : ("Escola de Música K. Zuza", ""),
    4840 : ("Bebidas Musicais Pop Rock", ""),
    4841 : ("Bandoleiro Bandolins!", ""),
    4842 : ("Corporação Sincopação", ""),
    4843 : ("", ""),
    4844 : ("Motocicletas Com Notação", ""),
    4845 : ("Elegias Elegantes da Elen", ""),
    4848 : ("Financeira Cordas de Dinheiro", ""),
    4849 : ("", ""),
    4850 : ("Hipoteca Cordas Emprestadas", ""),
    4852 : ("Arranca-peles Flauta Florida", ""),
    4853 : ("Para-choques do Léo Guitarra", ""),
    4854 : ("Vídeos de Violinos Vocacionais Wagner", ""),
    4855 : ("Rede de Televisão Teleouvisa", ""),
    4856 : ("", ""),
    4862 : ("Quatrilhos Quintessenciais do Quarentino", ""),
    4867 : ("Celos Amarelos do Costello", ""),
    4868 : ("", ""),
    4870 : ("Zoológico de Ziriguidum do Ziggy", ""),
    4871 : ("Humbuckers Únicos do Ubaldo", ""),
    4872 : ("Braços sem Estresse do Estevão Expresso", ""),
    4873 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : (lGagShop, ""),
    5502 : (lToonHQ, ""),
    5503 : (lClothingShop, ""),
    5505 : (lPetShop, ""),
    # titles for: phase_8/dna/daisys_garden_5100.dna
    5601 : ("Exames de Vista Olho do Alho", ""),
    5602 : ("Gravatas do Sérgio Sufocado", ""),
    5603 : ("Verde que te Quero Verdura", ""),
    5604 : ("Loja de Noivas Mel e Lão", ""),
    5605 : ("Sobre Mesas e Cadeiras", ""),
    5606 : ("Pétalas", ""),
    5607 : ("Correios Adubo Expresso", ""),
    5608 : ("Toca da Pipoca", ""),
    5609 : ("Tesouro dos Dentes de Alho de Ouro", ""),
    5610 : ("Aulas de Boxe da Susana Olhos Negros", ""),
    5611 : ("Piadas do Toupeira", ""),
    5613 : ("Barbeiros Tosa Completa", ""),
    5615 : ("Ração para Pássaros do Florêncio", ""),
    5616 : ("Pousada Pouso da Coruja", ""),
    5617 : ("Borboletas do Borba Oleta", ""),
    5618 : ("Ervilhas e Milhas", ""),
    5619 : ("Pés de feijão do João", ""),
    5620 : ("Pousada Pá de Coisa", ""),
    5621 : ("Uvinhas da Ira", ""),
    5622 : ("Loja de Bicicletas Bem-me-quer", ""),
    5623 : ("Banheiras para Pássaros Bolhinhas Aladas", ""),
    5624 : ("Bico Calado", ""),
    5625 : ("Os Abelhudos", ""),
    5626 : ("Artesanato Pínus", ""),
    5627 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Do Início ao Figo", ""),
    5702 : ("Ancinho do Joãozinho", ""),
    5703 : ("Fotos Cíntia", ""),
    5704 : ("Carros Usados Lisa Lima", ""),
    5705 : ("Móveis Urtigas", ""),
    5706 : ("Joalheiros 14 Ki Latas", ""),
    5707 : ("Fruta Musical", ""),
    5708 : ("Agência de Viagens Erva da Ninha", ""),
    5709 : ("Cortadores de Grama Ré U. Vassintética", ""),
    5710 : ("Academia Durão", ""),
    5711 : ("Roupas Íntimas Jardim de Inverno", ""),
    5712 : ("Estátuas Idiotas", ""),
    5713 : ("Mãos à Obra", ""),
    5714 : ("Água Mineral Chuva de Verão", ""),
    5715 : ("Notícias do Campo", ""),
    5716 : ("Hipotecas Folhas Caídas", ""),
    5717 : ("Seivas Florais", ""),
    5718 : ("Animais Exóticos Mauricinho Leão", ""),
    5719 : ("Investigadores Particulares Cara que Manchão!", ""),
    5720 : ("Moda Masculina Bran Covinho", ""),
    5721 : ("Restaurante Rota 66", ""),
    5725 : ("Cervejaria da Cevada", ""),
    5726 : ("Terra Adubada do Ubaldo", ""),
    5727 : ("Financeira Toupeira Encurralada", ""),
    5728 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : (lToonHQ, ""),
    5804 : ("Vazar ou não Vazar?", ""),
    5805 : ("Correio da Lesma", ""),
    5809 : ("Escola de Palhaços Fungos", ""),
    5810 : ("Mela o Melado", ""),
    5811 : ("Pousada Al Face a Face", ""),
    5815 : ("Rural", ""),
    5817 : ("Maçãs e Laranjas", ""),
    5819 : ("Jeans Vagem Verde", ""),
    5821 : ("Academia Amassado e Esticado", ""),
    5826 : ("Artigos para o Cultivo de Formigas", ""),
    5827 : ("Promoção de Aterrar", ""),
    5828 : ("Móveis Batatinha Quando Nasce", ""),
    5830 : ("Espalhado o Babado", ""),
    5833 : ("Restaurante Saladas", ""),
    5835 : ("Café Colonial Flores do Campo", ""),
    5836 : ("Tubulações e Águas de Márcia", ""),
    5837 : ("Curso de Enólogo", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Biblioteca da Canção de Ninar", ""),
    9503 : ("O Bar da Soneca", ""),
    9504 : (lGagShop, ""),
    9505 : (lToonHQ, ""),
    9506 : (lClothingShop, ""),
    9508 : (lPetShop, ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Pousada A. Ninho", ""),
    9602 : ("Dois Dedos de Prosa com Morfeu pelo Preço de Um", ""),
    9604 : ("Sofá-cama Amarelo do Marcelo", ""),
    9605 : ("Travessa da Canção de Ninar, 323", ""),
    9607 : ("Pijamas Bahamas da Mama", ""),
    9608 : ("Erva-de-gato para Tirar um Cochilo", ""),
    9609 : ("Sono de Pedra por uma Bagatela", ""),
    9613 : ("Relojoeiros das Alturas", ""),
    9616 : ("Companhia Elétrica Luzes Apagadas", ""),
    9617 : ("Travessa da Canção de Ninar, 212", ""),
    9619 : ("Relaxe ao Máximo", ""),
    9620 : ("Serviços de Táxi Py Jama", ""),
    9622 : ("Relógios Sono Atrasado", ""),
    9625 : ("Salão de Beleza Enrolado Crespo", ""),
    9626 : ("Travessa da Canção de Ninar, 818", ""),
    9627 : ("A Tenda dos Sonhos", ""),
    9628 : ("Calendários Já Chega por Hoje", ""),
    9629 : ("Travessa da Canção de Ninar, 310", ""),
    9630 : ("Pedreira Sono de Pedra", ""),
    9631 : ("Conserto de Relógios Inatividade", ""),
    9633 : ("Sala de Projeção da Sonholândia", ""),
    9634 : ("Colchões Descanso da Mente", ""),
    9636 : ("Seguradora Insônia", ""),
    9639 : ("Casa de Hibernação", ""),
    9640 : ("Travessa da Canção de Ninar, 805", ""),
    9642 : ("Serraria Lombeira da Madeira", ""),
    9643 : ("Exames de Vista Olho Fechado", ""),
    9644 : ("Guerras de Travesseiro Noturnas", ""),
    9645 : ("Pousada Unidos Venceremos", ""),
    9647 : ("Loja de Ferragens Faça a sua Cama", ""),
    9649 : ("Ranking do Ronco", ""),
    9650 : ("Travessa da Canção de Ninar, 714", ""),
    9651 : ("Com Muito ou com Ronco", ""),
    9652 : ("", ""),
    # titles for: phase_8/dna/donalds_dreamland_9200.dna
    9703 : ("Agência de Viagens Vôo Noturno", ""),
    9704 : ("Loja de Animais Coruja Noturna", ""),
    9705 : ("Oficina Dormindo ao Volante", ""),
    9706 : ("Clínica Dentária Fada do Dente", ""),
    9707 : ("Centro de Jardinagem Bocejo Matutino", ""),
    9708 : ("Floricultura Leito de Rosas", ""),
    9709 : ("Encanamentos Sonho do Bombeiro", ""),
    9710 : ("Exames de Vista REM", ""),
    9711 : ("Companhia Telefônica Despertador", ""),
    9712 : ("Contagem de Ovelhas - Nós Contamos para Você!", ""),
    9713 : ("Pisca-duro, Pestana e Cabeçada, Advogados", ""),
    9714 : ("Artigos Marítimos Barco dos Sonhos", ""),
    9715 : ("Banco A Fraldinha de Dormir", ""),
    9716 : ("Pipi na Cama Festas", ""),
    9717 : ("Padaria Sonho à Dúzia", ""),
    9718 : ("Sanduíches A Cuca Vai Pegar", ""),
    9719 : ("Fábrica de Travesseiros Tatu", ""),
    9720 : ("Fala Dormindo Fonoaudiólogos", ""),
    9721 : ("Tapetes Aconchego", ""),
    9722 : ("Agência de Talentos Sonho de Menina", ""),
    9725 : ("Pijamas Saco de Gato", ""),
    9727 : ("Cochilou, Dançou", ""),
    9736 : ("Agência de Empregos Trabalho dos Sonhos", ""),
    9737 : ("Escola de Dança Matilda Madruga", ""),
    9738 : ("Casa de Zzzzzs", ""),
    9740 : ("Escola de Esgrima Naná", ""),
    9741 : ("Deu Pulga na Cama Extermínio de Insetos", ""),
    9744 : ("Creme para Rugas Chega de Insônia", ""),
    9752 : ("Petroleira Meia-Noite", ""),
    9753 : ("Sorveteria Luar Gelado", ""),
    9754 : ("Passeios de Pônei Cavalgada Noturna", ""),
    9755 : ("Cinemas Cama Voadora", ""),
    9756 : ("", ""),
    9759 : ("Salão de Beleza Bela Adormecida", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : (lGagShop, ""),
    3508 : (lToonHQ, ""),
    3509 : (lClothingShop, ""),
    3511 : (lPetShop, ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("Companhia Elétrica Esplendor do Norte", ""),
    3602 : ("Gorros do Pólo Norte", ""),
    3605 : ("", ""),
    3607 : ("Mago do Lago Congelado", ""),
    3608 : ("Existe um Lugar", ""),
    3610 : ("Hipermercado de Sapatos de Esquimó Quiprocó", ""),
    3611 : ("Rodinho do Leão Marinho", ""),
    3612 : ("Design de Iglus", ""),
    3613 : ("Cicle Geloso", ""),
    3614 : ("Indústria de Cereais Flocos de Neve", ""),
    3615 : ("Pastéis de Forno Lindo Alasca", ""),
    3617 : ("Passeios de Balão Vento Frio", ""),
    3618 : ("Consultoria de Gestão de Crises Grande Coisa!", ""),
    3620 : ("Clínica do Esqui", ""),
    3621 : ("Sorveteria Gelo Derretido", ""),
    3622 : ("", ""),
    3623 : ("Indústria de Pães Torradinha", ""),
    3624 : ("Sanduicheria Abaixo de Zero", ""),
    3625 : ("Aquecedores Tia Freezer", ""),
    3627 : ("Canil São Bernardo", ""),
    3629 : ("Restaurante Sopa de Ervilhas", ""),
    3630 : ("Agência de Viagens Com Gelo em Londres, Com Gelo na França", ""),
    3634 : ("Teleférico Boa Vista", ""),
    3635 : ("Lenha Usada", ""),
    3636 : ("Promoção de Arrepios", ""),
    3637 : ("Skates da Kate", ""),
    3638 : ("Tobogã da Lã", ""),
    3641 : ("Trenó do Chicó", ""),
    3642 : ("Ótica Olho do Furacão", ""),
    3643 : ("Salão Bola de Neve", ""),
    3644 : ("Cubos de Gelo Derretidos", ""),
    3647 : ("Loja de Smokings Pinguim Animado", ""),
    3648 : ("Sorvete Instantâneo", ""),
    3649 : ("Hambrrrgers", ""),
    3650 : ("Antiguidades Antárctica", ""),
    3651 : ("Salsichas Congeladas do Fred Barbicha", ""),
    3653 : ("Joalheria Cristal do Gelo", ""),
    3654 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3200.dna
    3702 : ("Armazém do Inverno", ""),
    3703 : ("", ""),
    3705 : ("Cicle Pingo Congelado para Dois", ""),
    3706 : ("Fábrica de Refrigerantes Treme-treme", ""),
    3707 : ("Neve Doce Neve", ""),
    3708 : ("Loja do Pluto", ""),
    3710 : ("Temperatura em Queda Refeições", ""),
    3711 : ("", ""),
    3712 : ("Vai por Gelo Abaixo", ""),
    3713 : ("Dentista Abaixo de Zero Tiritante", ""),
    3715 : ("Casa de Sopas Tia Ártica", ""),
    3716 : ("Estrada de Sal e Pimenta", ""),
    3717 : ("A Lasca Verbal", ""),
    3718 : ("Designer de Câmaras de Ar", ""),
    3719 : ("Cubo de Gelo no Palitinho", ""),
    3721 : ("Liquidação de Tobogãs Cabeção", ""),
    3722 : ("Loja de Esquis Coelhinho de Neve", ""),
    3723 : ("Bolas de Neve Tremendão", ""),
    3724 : ("Fatos e Fofocas", ""),
    3725 : ("O Nó do Trenó", ""),
    3726 : ("Cobertores com Energia Solar", ""),
    3728 : ("Tratores de Neve Anta Lenta", ""),
    3729 : ("", ""),
    3730 : ("Compra e Venda de Bonecos de Neve", ""),
    3731 : ("Lareiras Portáteis", ""),
    3732 : ("O Nariz Congelado", ""),
    3734 : ("Exames de Vista C. V. Gelo", ""),
    3735 : ("Capas de Gelo Polar", ""),
    3736 : ("Cubos de Gelo com Zelo", ""),
    3737 : ("Restaurante Montanha Abaixo", ""),
    3738 : ("Aquecimento - Aproveite Enquanto está Quente", ""),
    3739 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3300.dna
    3801 : (lToonHQ, ""),
    3806 : ("Linha de Comida Alpina", ""),
    3807 : ("Sombras de Marmota Usadas", ""),
    3808 : ("A Cabana Suadoura", ""),
    3809 : ("Elvira Tão Bem", ""),
    3810 : ("O Bom Edredom", ""),
    3811 : ("Seu Anjo de Neve", ""),
    3812 : ("Gatinhos de Luvas", ""),
    3813 : ("Botas de Neve Essenciais", ""),
    3814 : ("Banca de Refrigerantes Gás-na-Boca", ""),
    3815 : ("O Chalé da Peruca", ""),
    3816 : ("Viste o Visco", ""),
    3817 : ("Clube de Trilha de Inverno do País das Maravilhas", ""),
    3818 : ("A Barraca das Pás", ""),
    3819 : ("Serviço de Chaminés Sopro Limpo", ""),
    3820 : ("Brancura de Neve", ""),
    3821 : ("Férias Hibernantes", ""),
    3823 : ("Fundações e Precipitações", ""),
    3824 : ("Nozes Assadas na Fogueira", ""),
    3825 : ("Chapéus do Gato Legal", ""),
    3826 : ("Ai, Minhas Galochas!", ""),
    3827 : ("Grinaldas Corais", ""),
    3828 : ("Terra do Boneco de Neve", ""),
    3829 : ("Área dos Pinheiros", ""),
    3830 : ("Desembaçamento de Óculos Espere-e-Veja", ""),
    }

# DistributedCloset.py
ClosetTimeoutMessage = "Sinto muito, o tempo\n acabou."
ClosetNotOwnerMessage = "Este não é o seu armário, mas você pode experimentar as roupas."
ClosetPopupOK = lOK
ClosetPopupCancel = lCancel
ClosetDiscardButton = "Remover"
ClosetAreYouSureMessage = "Você excluiu algumas roupas. Deseja mesmo excluí-las?"
ClosetYes = lYes
ClosetNo = lNo
ClosetVerifyDelete = "Excluir mesmo %s?"
ClosetShirt = "esta camisa"
ClosetShorts = "este short"
ClosetSkirt = "esta saia"
ClosetDeleteShirt = "Excluir\ncamisa"
ClosetDeleteShorts = "Excluir\nshort"
ClosetDeleteSkirt = "Excluir\nsaia"

# EstateLoader.py
EstateOwnerLeftMessage = "Sinto muito, o dono desta propriedade saiu. Você será enviado ao pátio em %s segundos"
EstatePopupOK = lOK
EstateTeleportFailed = "Não foi possível ir para casa. Tente novamente!"
EstateTeleportFailedNotFriends = "Sinto muito, %s fica na propriedade de um toon com o qual você não fez amizade."

# DistributedTarget.py
EstateTargetGameStart = "O jogo do Alvo de Toonar começou!"
EstateTargetGameInst = "Quanto mais acertar no alvo vermelho, mais Toonar você vai receber."
EstateTargetGameEnd = "O jogo de Alvo de Toonar acabou..."

# DistributedHouse.py
AvatarsHouse = "Casa de\n %s"

# BankGui.py
BankGuiCancel = lCancel
BankGuiOk = lOK

# DistributedBank.py
DistributedBankNoOwner = "Sinto muito, este não é o seu banco."
DistributedBankNotOwner = "Sinto muito, este não é o seu banco."

# FishSellGui.py
FishGuiCancel = lCancel
FishGuiOk = "Vender tudo"
FishTankValue = "Oi, %(name)s! Você tem %(num)s peixe(s) em seu balde, que vale(m) o total de %(value)s balinhas. Deseja vender todos eles?"

#FlowerSellGui.py
FlowerGuiCancel = lCancel
FlowerGuiOk = "Vender Tudo"
FlowerBasketValue = "%(name)s, você tem %(num)s flores no seu cesto que valem um total de %(value)s balinhas. Você quer vender todas?"


def GetPossesive(name):
    if name[-1:] == 'de':
        possesive = name + "'"
    else:
        possesive = name + ""
    return possesive

# PetTraits
# VERY_BAD, BAD, GOOD, VERY_GOOD
PetTrait2descriptions = {
    'hungerThreshold': ('Sempre faminto', 'Muito faminto',
                        'Às vezes faminto', 'Raramente faminto',),
    'boredomThreshold': ('Sempre chateado', 'Muito chateado',
                         'Às vezes chateado', 'Raramente chateado',),
    'angerThreshold': ('Sempre irritado', 'Muito irritado',
                       'Às vezes irritado', 'Raramente irritado'),
    'forgetfulness': ('Sempre esquecido', 'Muito esquecido',
                      'Às vezes esquecido', 'Raramente esquecido',),
    'excitementThreshold': ('Muito calmo', 'Bem calmo',
                            'Bem animado', 'Muito animado',),
    'sadnessThreshold': ('Sempre triste', 'Muitas vezes triste',
                         'Às vezes triste', 'Raramente triste',),
    'restlessnessThreshold': ('Sempre inquieto', 'Muito inquieto',
                         'Às vezes inquieto', 'Raramente inquieto',),
    'playfulnessThreshold': ('Raramente brincalhão', 'Às vezes brincalhão',
                         'Muito brincalhão', 'Sempre brincalhão',),
    'lonelinessThreshold': ('Sempre solitário', 'Muito solitário',
                         'Às vezes solitário', 'Raramente solitário',),
    'fatigueThreshold': ('Sempre cansado', 'Muito cansado',
                         'Às vezes cansado', 'Raramente cansado',),
    'confusionThreshold': ('Sempre confuso', 'Muito confuso',
                         'Às vezes confuso', 'Raramente confuso',),
    'surpriseThreshold': ('Sempre surpreso', 'Muito surpreso',
                         'Às vezes surpreso', 'Raramente surpreso',),
    'affectionThreshold': ('Raramente carinhoso', 'Às vezes carinhoso',
                         'Muito carinhoso', 'Sempre carinhoso',),
    }

# end translate

# DistributedFireworkShow.py
FireworksInstructions = lToonHQ+": Pressione a tecla \"Page Up\" para ver melhor."

FireworksValentinesBeginning = ""
FireworksValentinesEnding = ""
FireworksJuly4Beginning = lToonHQ+": Bem-vindo à queima de fogos de verão! Divirta-se com o show!"
FireworksJuly4Ending = lToonHQ+": Espero que tenha gostado do show! Um ótimo verão para você!"
FireworksJuly14Beginning = lToonHQ+""
FireworksJuly14Ending = lToonHQ+""
FireworksOctober31Beginning = ""
FireworksOctober31Ending = ""
FireworksNewYearsEveBeginning = lToonHQ+": Feliz Ano Novo!!!!"
FireworksNewYearsEveEnding = lToonHQ+": Gostou dos Fogos? Logo tem mais!"
FireworksBeginning = lToonHQ+": Bem-vindo à queima de fogos de verão! Divirta-se com o show!"
FireworksEnding = lToonHQ+": Espero que tenha gostado do show! Um ótimo verão para você!"

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
TipTitle = "DICA TOON:"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Verifique com rapidez o andamento da Tarefa Toon mantendo pressionada a tecla \"End\".",
    "Verifique com rapidez a sua Página de piadas mantendo pressionada a tecla \"Home\".",
    "Abra a sua Lista de amigos pressionando a tecla \"F7\".",
    "Abra ou feche o seu Álbum Toon pressionando a tecla \"F8\".",
    "Você pode procurar acima pressionando a tecla \"Page Up\" e abaixo pressionando a tecla \"Page Down\".",
    "Pressione a tecla \"Control\" para pular.",
    "Pressione a tecla \"F9\" para capturar a tela, que será salva na pasta Toontown do seu computador.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "Você pode trocar Códigos de Amigo secreto com alguém conhecido que não seja de Toontown, para permitir um chat aberto com essa pessoa em Toontown.",
    "Você pode alterar a resolução de seu vídeo, ajustar o áudio e controlar outras opções na Página de opções do Álbum Toon.",
    "Experimente as roupas de seus amigos no armário da casa deles.",
    "Você pode ir para casa usando o botão \"Ir para casa\" em seu mapa.",
    "Toda vez que você conclui uma Tarefa Toon, seus Pontos de risadas são automaticamente recarregados.",
    "Você pode procurar a seleção nas lojas de roupas mesmo sem ter um bilhete de roupas.",
    "As recompensas para algumas Tarefas Toon permitem que você carregue mais piadas e balinhas.",
    "Você pode ter até 50 amigos na sua Lista de amigos.",
    "Algumas recompensas das Tarefas Toon permitem que você se teletransporte para os pátios de Toontown usando a Página do mapa do Álbum Toon.",
    "Aumente os seus Pontos de risadas nos pátios, catando tesouros como estrelas e casquinhas de sorvete.",
    "Se você precisar se recuperar rápido após uma batalha difícil, vá para a sua propriedade e recolha casquinhas de sorvete.",
    "Alterne entre os diversos modos de exibição de seu Toon pressionando a tecla Tab.",
    "Algumas vezes, você poderá encontrar várias Tarefas Toon diferentes com a mesma recompensa. Faça sua pesquisa de mercado!",
    "Encontrar amigos com Tarefas Toon semelhantes é uma maneira divertida de progredir no jogo.",
    "Você nunca precisa salvar o seu progresso em Toontown. Os servidores de Toontown salvam continuamente todas as informações necessárias.",
    "Você pode cochichar com outros Toons clicando neles ou selecionando-os em sua Lista de amigos.",
    "Algumas frases do Chat rápido têm animações para indicar o estado de espírito do seu Toon.",
    "Se a área em que você está se encontra lotada, tente mudar de região. Vá para a Página de região do Álbum Toon e selecione uma diferente.",
    "Se você estiver em plena atividade de salvamento de edifícios, ganhará uma estrela de bronze, prata ou ouro, que ficará acima de seu Toon.",
    "Se você salvar um número suficiente de edifícios para obter uma estrela acima da cabeça, seu nome pode estar no quadro-negro de um Quartel Toon.",
    "Os edifícios salvos, às vezes, são recuperados pelos Cogs. A única maneira de manter a sua estrela é sair em campo e salvar mais edifícios!",
    "Os nomes dos seus Amigos secretos aparecerão na cor azul.",
    # Fishing
    "Veja se você consegue pegar todos os peixes de Toontown!",
    "Há peixes diferentes nos diversos lagos. Tente todos!",
    "Quando o seu balde de pesca estiver cheio, venda os peixes para os pescadores dos pátios.",
    "Venda os peixes para o pescador ou dentro das Lojas de Animais.",
    "As varas de pescar mais fortes conseguem pegar peixes mais pesados, mas custam mais balinhas.",
    "Você pode comprar varas de pescar mais fortes no Gadálogo.",
    "Os peixes mais pesados valem mais balinhas na Loja de animais.",
    "Os peixes raros valem mais balinhas na Loja de animais.",
    "Às vezes, você consegue encontrar bolsas de balinhas durante a pesca.",
    "Algumas Tarefas Toon exigem que você pesque itens fora dos lagos.",
    "Os lagos de pesca dos pátios possuem peixes diferentes dos lagos das ruas.",
    "Alguns peixes são realmente raros. Continue pescando até pegar todos!",
    "O lago da sua propriedade possui peixes que só podem ser encontrados lá.",
    "Para cada dez espécies pescadas, você ganhará um troféu de pesca!",
    "Você pode ver qual peixe pescou no Álbum Toon.",
    "Alguns troféus de pesca o recompensam com um Acréscimo de risadas.",
    "A pesca é uma boa maneira de ganhar mais balinhas.",
    # Doodles
    "Adote um Rabisco na Loja de Animais!",
    "As lojas de animais têm Rabiscos novos para vender todos os dias.",
    "Visite as lojas de animais todos os dias para ver que Rabiscos novos elas têm.",
    "Há diferentes Rabiscos para adoção nos diferentes bairros.",
 # Karting
    "Mostre o seu carrão e dê uma turbinada no seu limite de Risadas no Autódromo do Pateta. ",
    "Entre no Autódromo do Pateta pelo túnel em forma de pneu no pátio do Centro de Toontown.",
    "Ganhe pontos de Risada no Autódromo do Pateta.",
    "O Autódromo do Pateta tem seis pistas de corrida diferentes. "
   ),

  TIP_STREET : (
    "Há quatro tipos de Cogs: Robôs da Lei, Robôs Mercenários, Robôs Vendedores e Robôs-chefe.",
    "Cada Método de piadas possui diferentes intensidades de precisão e dano.",
    "As piadas sonoras afetam todos os Cogs, mas acordam qualquer Cog iscado.",
    "Derrotar os Cogs em ordem estratégica pode aumentar bastante as suas chances de vencer as batalhas.",
    "O Método de piadas Toonar permite que você atinja outros Toons na batalha.",
    "Os pontos de experiência das piadas são dobrados durante uma Invasão de Cogs!",
    "Vários Toons podem se reunir em equipes e usar o mesmo Método de piadas na batalha para conseguir danos extras aos Cogs.",
    "Na batalha, as piadas são usadas na ordem de cima para baixo, conforme exibido no Menu de piadas.",
    "A fileira de luzes circulares sobre os elevadores do Edifício dos Cogs mostram quantos andares haverá lá dentro.",
    "Clique em um Cog para ver mais detalhes.",
    "Usar piadas de alto nível contra Cogs de baixo nível não lhe renderá nenhum ponto de experiência.",
    "As piadas que rendem experiência possuem um fundo azul no Menu de piadas da batalha.",
    "A experiência de piadas é multiplicada quando usada dentro dos Edifícios dos Cogs. Os andares mais altos têm multiplicadores maiores.",
    "Quando um Cog é derrotado, cada Toon daquela rodada recebe créditos de Cogs depois que a batalha termina.",
    "Cada rua de Toontown possui níveis e tipos diferentes de Cogs.",
    "As calçadas são locais seguros, sem Cogs.",
    "Nas ruas, as portas laterais contam piadas do tipo toc-toc quando você se aproxima delas.",
    "Algumas Tarefas Toon treinam você em novos Métodos de piadas. Você só pode escolher seis dos sete métodos, portanto, escolha direito!",
    "As armadilhas só terão utilidade se você ou seus amigos coordenarem o uso de iscas na batalha.",
    "As iscas de alto nível têm menos probabilidade de falhar.",
    "As piadas de nível baixo oferecem menor precisão contra os Cogs de alto nível.",
    "Os Cogs não podem atacar depois que forem \"iscados\" para a batalha.",
    "Quando você e seus amigos dominam um Edifício de Cogs, vocês são recompensados com retratos dentro do Edifício dos Toons recuperado.",
    "Usar uma piada Toonar em um Toon que possua um Risômetro cheio não renderá nenhuma experiência de Toonar.",
    "Os Cogs ficarão atordoados por uns momentos quando atingidos por alguma. Assim, aumentam as chances de outras piadas da mesma rodada os atingirem.",
    "As Piadas cadentes têm menos chance de atingir alguém, mas sua precisão aumenta quando os Cogs já tiverem sido atingidos por outra piada na mesma rodada.",
    "Quando você já tiver derrotado um número suficiente de Cogs, use o \"Radar de Cogs\" clicando nos ícones de Cogs da página Galeria de Cogs do seu Álbum Toon.",
    "Durante uma batalha, você tem como saber qual Cog os seus companheiros de equipe estão atacando; basta olhar para os travessões (-) e para os X.",
    "Durante uma batalha, os Cogs carregam uma luz que mostra sua saúde: o verde significa saudável e o vermelho, quase destruído.",
    "No máximo, quatro Toons podem guerrear ao mesmo tempo.",
    "Na rua, os Cogs têm mais probabilidade de entrar em uma briga contra vários Toons do que contra apenas um Toon.",
    "Os dois tipos de Cogs mais difíceis de cada tipo só são encontrados nos edifícios.",
    "As Piadas cadentes nunca funcionam contra Cogs iscados.",
    "Os Cogs tendem a atacar o Toon que lhes causou danos maiores.",
    "As piadas sonoras não rendem danos extras contra Cogs iscados.",
    "Se você esperar muito para atacar um Cog iscado, ele acordará. As iscas de nível mais alto têm duração maior.",
    "Há lagos de pesca em cada rua de Toontown. Algumas ruas possuem peixes exclusivos.",
    ),

  TIP_MINIGAME : (
    "Depois que você preenche a sua jarra de balinhas, qualquer balinha que ganhar nos Jogos no bondinho cairão direto no seu banco.",
    "Você pode usar as teclas de seta em vez de o mouse no Jogo no bondinho \"Acompanhe a Minnie\".",
    "No Jogo do canhão, você pode usar as teclas de seta para mover o seu canhão e pressionar a tecla \"Control\" para atirar.",
    "No Jogo dos anéis, você ganha pontos extras quando todo o grupo consegue nadar com sucesso através dos anéis.",
    "Um jogo perfeito de Acompanhe a Minnie dobrará seus pontos.",
    "No Cabo de guerra, você ganha mais balinhas se jogar contra um Cog forte.",
    "A dificuldade dos Jogos no bondinho varia conforme o bairro; os do Centro de Toontown são os mais fáceis, e os da Sonholândia do Donald são os mais difíceis.",
    "Certos Jogos no bondinho só podem ser em grupo.",
    ),

  TIP_COGHQ : (
    "Você deve completar o seu Disfarce de Robô Vendedor antes de visitar o VP.",
    "Você deve completar o seu Disfarce de Robô Mercenário antes de visitar o Diretor Financeiro.",
    "Você deve completar o seu Disfarce de Robô da Lei antes de visitar o Juiz-chefe.",
    "Você pode pular em cima de cogs Brutamontes para desativá-los por um tempo.",
    "Ganhe Méritos de cogs ao derrotar Robôs Vendedores em batalha.",
    "Ganhe Cograna ao derrotar Robôs Mercenários em batalha.",
    "Ganhe Avisos de Júri ao derrotar Robôs da Lei em batalha.",
    "Você ganha mais Méritos, Cogranas ou Avisos de Júri de Cogs de nível maior.",
    "Quando conseguir juntar Méritos o suficiente para merecer uma promoção, vá ver o VP dos Robôs Vendedores!",
    "Quando conseguir juntar Cogranas o suficiente para merecer uma promoção, vá ver o Diretor Financeiro dos Robôs Mercenários!",
    "Quando conseguir juntar Avisos de Júri o suficiente para merecer uma promoção, vá ver o Juiz-chefe dos Robôs da Lei!",
    "Você pode falar como um Cog quando estiver usando o seu Disfarce de Cog.",
    "Até oito Toons podem lutar juntos contra o VP dos Robôs Vendedores",
    "Até oito Toons podem lutar juntos contra o Diretor Financeiro dos Robôs Mercenários",
    "Até oito Toons podem lutar juntos contra o Juiz-chefe dos Robôs da Lei",
    "Dentro do Quartel dos Cogs, o caminho é subindo as escadas.",
    "Cada vez que lutar numa fábrica do Quartel dos Robôs Vendedores, você vai ganhar uma peça do seu Disfarce de Robô Vendedor.",
    "Você pode verificar o progresso do seu Disfarce no seu Álbum Toon.",
    "Você pode verificar o progresso da sua promoção na Página de Disfarce do seu Álbum Toon.",
    "Certifique-se de estar com as piadas cheias e com o Risômetro cheio antes de ir até um Quartel dos Cogs.",
    "Quando for promovido, seu disfarce de Cog será atualizado.",
    "Você terá que derrotar o "+Foreman+" para recuperar uma peça do Disfarce de Robô Vendedor.",
    "Ganhe peças de disfarce de Robô Mercenário como recompensa de Tarefas Toon na Sonholândia do Donald.",
    "Os Robôs Mercenários produzem e distribuem o seu próprio dinheiro, as Cogranas, de três maneiras - Moeda, Dólar e Barra.",
    "Espere até que o Diretor Financeiro esteja tonto para lançar um cofre, senão ele vai usá-lo como capacete! Acerte o capacete com outro cofre para derrubá-lo.",
    "Ganhe peças de disfarce de Robô da Lei como recompensa de Tarefas Toon pelo Professor Floco.",
    "Vale a pena a confusão: os Cogs virtuais no Quartel dos Robôs da Lei não dão Avisos de Júri de recompensa.",
    " Robô Mercenário produz e distribui a sua própia moeda, Cogbucks, em três formas diferentes: Moedas, Dólar, e lingotes.",
    " Aguarde até que o Diretor Financeiro fique doido para lançar um seguro ou o utilize-o como um capacete! Acerte no capacete com outro seguro para pegá-lo.",
    "O Robô da Lei obtém as partes do traje como recompensa ao concluir a TarefaToon para o Professor Floco.",
    ),
  TIP_ESTATE : (
    # Doodles
    "Os Rabiscos entendem algumas frases do Chat rápido. Experimente!",
    "Use o menu \"Bichinho\" do Chat rápido para pedir a seu Rabisco que faça truques.",
    "Você pode ensinar aos Rabiscos truques com as lições de treinamento do Gadálogo da Clarabela.",
    "Recompense o seu Rabisco pelos truques.",
    "Se você visitar a propriedade de um amigo, o seu Rabisco lhe fará companhia.",
    "Alimente o seu Rabisco com uma balinha quando ele estiver com fome.",
    "Clique em um Rabisco para ver um menu no qual você poderá Alimentar, Coçar e Chamá-lo.",
    "Os Rabiscos adoram companhia. Convide os amigos para brincar!",
    "Todos os Rabiscos possuem personalidades próprias.",
    "Você pode devolver o seu Rabisco e adotar outro nas Lojas de Animais.",
    "Quando um Rabisco faz um truque, os Toons que o cercam se recuperam.",
    "Os Rabiscos ficam ainda melhores nos truques com a prática. Continue assim!",
    "Os truques mais avançados dos Rabiscos recuperam os Toons com mais rapidez.",
    "Rabiscos com mais experiência podem fazer mais truques sem ficar tão cansados.",
    "Veja uma lista de Rabiscos próximos em sua Lista de amigos.",
    # Furniture / Cattlelog
    "Compre móveis usando o Gadálogo da Clarabela e decore a sua casa.",
    "O banco da casa tem mais balinhas.",
    "O armário da casa tem mais roupas.",
    "Vá até a casa do seu amigo e experimente as roupas dele.",
    "Compre varas de pescar melhores no Gadálogo da Clarabela.",
    "Compre bancos maiores no Gadálogo da Clarabela.",
    "Ligue para a Clarabela usando o telefone da casa.",
    "A Clarabela vende um armário maior em que cabem mais roupas.",
    "Reserve espaço no seu armário antes de usar o bilhete de roupas.",
    "A Clarabela vende tudo o que é preciso para decorar a sua casa.",
    "Verifique a sua caixa de correio para ver se há entregas antes de fazer seus pedidos com a Clarabela.",
    "As roupas do Gadálogo da Clarabela levam uma hora para serem entregues.",
    "Os papéis de parede e pisos do Gadálogo da Clarabela levam uma hora para serem entregues.",
    "Os móveis do Gadálogo da Clarabela levam um dia inteiro para serem entregues.",
    "Armazene móveis de reserva no sótão.",
    "Você será avisado pela Clarabela quando um novo Gadálogo estiver disponível.",
    "Você será avisado pela Clarabela quando uma entrega do Gadálogo chegar.",
    "Novos Gadálogos são entregues toda semana.",
    "Procure os produtos promocionais de estoque limitado no Gadálogo.",
    "Mova os móveis indesejados para a lata de lixo.",
    # Fish
    "Alguns peixes, como a Cavala Trotante, são mais comuns nas propriedades de Toons.",
    # Misc
    "Você pode convidar os seus amigos para a sua propriedade usando o Chat rápido.",
    "Você sabia que a cor da sua casa combina com a cor do seu painel Pegar um Toon?",
    ),
   TIP_KARTING : (
    # Goofy Speedway zone specific
    "Compre um Conversível, Utilitário Toon ou Cruzeiro na Loja do Kart do Pateta.",
    "Personalize o seu kart com decalques, calotas e muito mais na Loja do Kart do Pateta.",
    "Ganhe bilhetes correndo de kart no Autódromo do Pateta.",
    "Os bilhetes são a única moeda aceita na Loja do Kart do Pateta.",
    "São necessários bilhetes como depósito antes das corridas.",
    "Uma página especial do seu Álbum Toon permite que você personalize o seu kart.",
    "Uma página especial do seu Álbum Toon permite que você veja os recordes de cada pista.",
    "Uma página especial do seu Álbum Toon permite que você veja seus troféus.",
    "O Estádio dos Nerds é a pista mais fácil do Autódromo do Pateta.",
    "A Pista de Pulos tem o maior número de inclinações e rampas do Autódromo do Pateta.",
    "A Avenida da Neve é a pista mais difícil do Autódromo do Pateta.",
    ),
   TIP_GOLF: (
    # Golfing specific
    "Aperte a tecla Tab para ver de cima o percurso de golfe.",
    "Aperte a tecla de Seta para Cima para se colocar na direção do buraco de golfe.",
    "Balançar o taco é como atirar uma torta.",
    ),
    }

FishGenusNames = {
    0 : "Baiacu",
    2 : "Peixe-gato",
    4 : "Peixe-palhaço",
    6 : "Peixe congelado",
    8 : "Estrela-do-mar",
    10 : "Cavala Trotante!",
    12 : "Cachorra",
    14 : "Enguia Amore",
    16 : "Tubarão-enfermeira",
    18 : "Caranguejo-rei",
    20 : "Peixe-lua",
    22 : "Cavalo-marinho",
    24 : "Tubarão Fera",
    26 : "Barra Cursa",
    28 : "Truta Cicuta",
    30 : "Piano Atum",
    32 : "Manteiga de Amendoim e Água-viva",
    34 : "Raia Jamanta",
    }

FishSpeciesNames = {
    0 : ( "Baiacu",
          "Baiacu Balão de Ar",
          "Baiacu Balão Meteorológico",
          "Baiacu Balão de Água",
          "Baiacu Balão Vermelho",
          ),
    2 : ( "Peixe-gato",
          "Peixe-gato Siamês",
          "Peixe-gato de Rua",
          "Peixe-gato Rajado",
          "Peixe-gato Tonto",
          ),
    4 : ( "Peixe-palhaço",
          "Peixe-palhaço Triste",
          "Peixe-palhaço de Festa",
          "Peixe-palhaço de Circo",
          ),
    6 : ( "Peixe congelado",
          ),
    8 : ( "Estrela-do-mar",
          "Cinco Estrelas-do-mar",
          "Estrela-do-mar do Rock",
          "Estrela-do-mar Cintilante",
          "Estrela-do-mar All Star",
          ),
    10 : ( "Cavala Trotante!",
           ),
    12 : ( "Cachorra",
           "Cachorra Buldogue",
           "Cachorra-quente",
           "Cachorra Dálmata",
           "Cachorrinha",
           ),
    14 : ( "Enguia Amore",
           "Enguia Amore Elétrica",
           ),
    16 : ( "Tubarão-enfermeira",
           "Tubarão-enfermeira Clara",
           "Tubarão-enfermeira Flora",
           ),
    18 : ( "Caranguejo-rei",
           "Caranguejo-rei do Alasca",
           "Caranguejo-rei Velho",
           ),
    20 : ( "Peixe-lua",
           "Peixe-lua Cheia",
           "Peixe Meia-lua",
           "Peixe-lua Nova",
           "Peixe-lua Crescente",
           "Peixe-lua da Colheita",
           ),
    22 : ( "Cavalo-marinho",
           "Cavalo-marinho de Pau",
           "Cavalo-marinho Clydesdale",
           "Cavalo-marinho Árabe",
           ),
    24 : ( "Tubarão-Fera",
           "Tubarãozinho Fera",
           "Tubarão-Fera da Piscina",
           "Tubarão-Fera da Piscina Olímpica",
           ),
    26 : ( "Barra Cursa Marrom",
           "Barra Cursa Preto",
           "Barra Cursa Coala",
           "Barra Cursa de Mel",
           "Barra Cursa Polar",
           "Barra Cursa Panda",
           "Barra Cursa Kodiac",
           "Barra Cursa Grizzly",
           ),
    28 : ( "Truta",
           "Capitão Truta Cicuta",
           "Truta Cicuta Escorbuta",
           ),
    30 : ( "Piano Atum",
           "Grande Piano Atum",
           "Grande Piano Atum Baby",
           "Piano Atum Ereto",
           "Músico de Piano Atum",
           ),
    32 : ( "Manteiga de Amendoim e Água-viva",
           "MA & Água-viva de Uva",
           "MA & Água-viva Crocante",
           "MA & Água-viva de Morango",
           "Concord Grape PB&J Fish",
           ),
    34 : ( "Raia Jamanta",
           ),
    }

CogPartNames = (
    "Perna superior esquerda", "Perna inferior esquerda", "Pé esquerdo",
    "Perna superior direita", "Perna inferior direita", "Pé direito",
    "Ombro esquerdo",  "Ombro direito", "Peito", "Medidor de saúde", "Quadril",
    "Braço superior esquerdo",  "Braço inferior esquerdo", "Mão esquerda",
    "Braço superior direito", "Braço inferior direito", "Mão direita",
    )

CogPartNamesSimple = (
    "Busto superior",
    )

FishFirstNames = (
    "",
    "Anjo",
    "Ártico",
    "Bebê",
    "Bermuda",
    "Grande",
    "Bruna",
    "Bolhas",
    "Detuna",
    "Docinho",
    "Capitão",
    "Tico",
    "Cacho",
    "Coral",
    "Doutor",
    "Arenoso",
    "Imperador",
    "Canino",
    "Gordo",
    "Peixinho",
    "Flipper",
    "Linguado",
    "Sardinha",
    "Mel",
    "João",
    "Rei",
    "Pequeno",
    "Marlin",
    "Senhorita",
    "Senhor",
    "Pêssego",
    "Rosado",
    "Príncipe",
    "Princesa",
    "Professor",
    "Inchadinho",
    "Rainha",
    "Arco-íris",
    "Raio",
    "Rosinha",
    "Ferrugem",
    "Salgado",
    "Samuca",
    "Sandy",
    "Caspa",
    "Tutubarão",
    "Cavalheiro",
    "Saltador",
    "Chinela",
    "Guaiúba",
    "Malhado",
    "Espinho",
    "Pintado",
    "Estrela",
    "Doce",
    "Súper",
    "Tigre",
    "Miúdo",
    "Bigode",
    )

FishLastPrefixNames = (
    "",
    "Praia",
    "Preto",
    "Azul",
    "Porcão",
    "Machão",
    "Gato",
    "Fundo",
    "Duplo",
    "Leste",
    "Chique",
    "Escamoso",
    "Chato",
    "Fresco",
    "Gigante",
    "Ouro",
    "Dourado",
    "Cinza",
    "Verde",
    "Presunto",
    "Mané",
    "Geléia",
    "Dama",
    "Couro",
    "Limão",
    "Comprido",
    "Nordeste",
    "Oceano",
    "Octo",
    "Óleo",
    "Pérola",
    "Cachimbo",
    "Vermelho",
    "Faixa",
    "Rio",
    "Pedra",
    "Rubi",
    "Leme",
    "Sal",
    "Mar",
    "Prata",
    "Snorkel",
    "Só",
    "Sudeste",
    "Espinhoso",
    "Surfe",
    "Espada",
    "Tigre",
    "Triplo",
    "Tropical",
    "Atum",
    "Onda",
    "Fraco",
    "Oeste",
    "Branco",
    "Amarelo",
    )

FishLastSuffixNames = (
    "",
    "bola",
    "baixo",
    "barriga",
    "besouro",
    "gatuno",
    "manteiga",
    "garra",
    "sapateiro",
    "caranguejo",
    "rosnador",
    "tambor",
    "barbatana",
    "peixe",
    "batedor",
    "flipper",
    "fantasma",
    "roncador",
    "cabeça",
    "coroa",
    "saltador",
    "cavala",
    "lua",
    "boca",
    "tainha",
    "pescoço",
    "nariz",
    "galho",
    "bruto",
    "corredor",
    "vela",
    "tubarão",
    "concha",
    "seda",
    "limo",
    "mordedora",
    "fedido",
    "rabo",
    "sapo",
    "truta",
    "água",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "Entrada principal"
SellbotLegFactorySpecLobby = "Salão"
SellbotLegFactorySpecLobbyHallway = "Corredor do salão"
SellbotLegFactorySpecGearRoom = "Sala de engrenagens"
SellbotLegFactorySpecBoilerRoom = "Sala da caldeira"
SellbotLegFactorySpecEastCatwalk = "Passarela leste"
SellbotLegFactorySpecPaintMixer = "Misturador de tinta"
SellbotLegFactorySpecPaintMixerStorageRoom = "Depósito do Misturador de tinta"
SellbotLegFactorySpecWestSiloCatwalk = "Passarela do Silo Oeste"
SellbotLegFactorySpecPipeRoom = "Sala de tubulações"
SellbotLegFactorySpecDuctRoom = "Sala de dutos"
SellbotLegFactorySpecSideEntrance = "Entrada lateral"
SellbotLegFactorySpecStomperAlley = "Beco sinistro"
SellbotLegFactorySpecLavaRoomFoyer = "Antecâmara do Salão de lava"
SellbotLegFactorySpecLavaRoom = "Salão de lava"
SellbotLegFactorySpecLavaStorageRoom = "Depósito de lava"
SellbotLegFactorySpecWestCatwalk = "Passarela oeste"
SellbotLegFactorySpecOilRoom = "Sala de óleo"
SellbotLegFactorySpecLookout = "Vigilância"
SellbotLegFactorySpecWarehouse = "Armazém"
SellbotLegFactorySpecOilRoomHallway = "Corredor da Sala de óleo"
SellbotLegFactorySpecEastSiloControlRoom = "Sala de controle do Silo Leste"
SellbotLegFactorySpecWestSiloControlRoom = "Sala de controle do Silo Oeste"
SellbotLegFactorySpecCenterSiloControlRoom = "Sala de controle do Silo Central"
SellbotLegFactorySpecEastSilo = "Silo Leste"
SellbotLegFactorySpecWestSilo = "Silo Oeste"
SellbotLegFactorySpecCenterSilo = "Silo Central"
SellbotLegFactorySpecEastSiloCatwalk = "Passarela do Silo Leste"
SellbotLegFactorySpecWestElevatorShaft = "Eixo do Elevador Oeste"
SellbotLegFactorySpecEastElevatorShaft = "Eixo do Elevador Leste"

#FISH BINGO
FishBingoBingo = "BINGO!"
FishBingoVictory = "VITÓRIA!!"
FishBingoJackpot = "GRANDE PRÊMIO!"
FishBingoGameOver = "FIM DO JOGO"
FishBingoIntermission = "Intervalo\nTermina em:"
FishBingoNextGame = "Próximo jogo\nComeça em:"
FishBingoTypeNormal = "Clássico"
FishBingoTypeCorners = "Quatro cantos"
FishBingoTypeDiagonal = "Diagonais"
FishBingoTypeThreeway = "Três vias"
FishBingoTypeBlockout = "BLOQUEADO!"
FishBingoStart = "Está na hora do Bingo dos Peixes! Vá para qualquer píer disponível para jogar!"
FishBingoOngoing = "Bem-vindo! O Bingo dos Peixes já está rolando."
FishBingoEnd = "Espero que tenha se divertido no jogo Bingo dos Peixes."
FishBingoHelpMain = "Bem-vindo ao Bingo dos Peixes de Toontown! Todo mundo trabalha em conjunto no lago para preencher a cartela antes de acabar o tempo."
FishBingoHelpFlash = "Quando você pegar um peixe, clique em um dos quadrados piscantes para marcar a cartela."
FishBingoHelpNormal = "É uma cartela de Bingo Clássico. Para ganhar, complete qualquer linha vertical, horizontal ou na diagonal."
FishBingoHelpDiagonals = "Complete as duas diagonais para ganhar."
FishBingoHelpCorners = "Uma cartela de Cantos fácil. Complete todos os quatro cantos para ganhar."
FishBingoHelpThreeway = "Três vias. Complete ambas as diagonais e a linha do meio para ganhar. Esta não é fácil não!"
FishBingoHelpBlockout = "Bloqueado! Complete a cartela inteira para ganhar. Você está competindo contra todos os outros lagos e a bolada é grande!"
FishBingoOfferToSellFish = "O seu balde de pesca está cheio. Quer vender os seus peixes?"
FishBingoJackpotWin = "Ganhe %s balinhas!"
FishBingoJackpot = "Ganhe %s balinhas!"

# ResistanceSCStrings: SpeedChat phrases rewarded for defeating the CFO.
# It is safe to remove entries from this list, which will disable them
# for use from any toons who have already purchased them.  Note that the
# index numbers are stored directly in the database, so once assigned
# to a particular phrase, a given index number should never be
# repurposed to any other phrase.
ResistanceToonupMenu = "Toonar"
ResistanceToonupItem = "%s toonar"
ResistanceToonupItemMax = "Máx."
ResistanceToonupChat = "Toons de todo o mundo: vamos toonar!"
ResistanceRestockMenu = "Doar Piadas"
ResistanceRestockItem = "Doar Piadas %s"
ResistanceRestockItemAll = "Tudo"
ResistanceRestockChat = "Toons de todo o mundo: vamos piadar!"
ResistanceMoneyMenu = "Balinhas"
ResistanceMoneyItem = "%s balinhas"
ResistanceMoneyChat = "Toons de todo o mundo: gastem com consciência!"

# Resistance Emote NPC chat phrases
ResistanceEmote1 = NPCToonNames[9228] + ": Bem-vindo à Resistência!"
ResistanceEmote2 = NPCToonNames[9228] + ": Use a sua nova expressão para se identificar com outros membros."
ResistanceEmote3 = NPCToonNames[9228] + ": Boa sorte!"

# Kart racing
KartUIExit = "Deixar o kart"
KartShop_Cancel = lCancel
KartShop_BuyKart = "Comprar kart"
KartShop_BuyAccessories = "Comprar acessórios"
KartShop_BuyAccessory = "Comprar acessório"
KartShop_Cost = "Custo: %d bilhetes"
KartShop_ConfirmBuy = "Comprar %s por %d bilhetes?"
KartShop_NoAvailableAcc = "Não há acessórios deste tipo"
KartShop_FullTrunk = "A mala está cheia."
KartShop_ConfirmReturnKart = "Tem certeza de que quer devolver o seu kart atual?"
KartShop_ConfirmBoughtTitle = "Parabéns!"
KartShop_NotEnoughTickets = "Não há bilhetes suficientes!"

KartView_Rotate = "Girar"
KartView_Right = "Direita"
KartView_Left = "Esquerda"

# starting block
StartingBlock_NotEnoughTickets = "Você não tem bilhetes suficientes! Experimente participar de um treino."
StartingBlock_NoBoard = "O embarque para esta corrida terminou. Espere o início da próxima corrida."
StartingBlock_NoKart = "Primeiramente, você precisa de um kart! Por que você não pergunta a um dos funcionários da Loja do kart?"
StartingBlock_Occupied = "Este bloco já está ocupado! Procure outro ponto."
StartingBlock_TrackClosed = "Desculpe, esta pista está fechada para reformas."
StartingBlock_EnterPractice = "Deseja participar do treino?"
StartingBlock_EnterNonPractice = "Deseja participar de uma corrida %s por %s bilhetes?"
StartingBlock_EnterShowPad = "Deseja estacionar o seu carro aqui?"
StartingBlock_KickSoloRacer = "As corridas Batalha dos Toons e Grande Prêmio requerem dois ou mais participantes."
StartingBlock_Loading = "Indo para a corrida!"

#stuff for leader boards
LeaderBoard_Time = "Tempo"
LeaderBoard_Name = "Nome do piloto"
LeaderBoard_Daily = "Pontuação diária"
LeaderBoard_Weekly = "Pontuação semanal"
LeaderBoard_AllTime = "Melhor pontuação de todos os tempos"

RecordPeriodStrings = [
    LeaderBoard_Daily,
    LeaderBoard_Weekly,
    LeaderBoard_AllTime,
    ]

KartRace_RaceNames = [
    "Treino",
    "Batalha dos Toons",
    "Torneio",
    ]

from toontown.racing import RaceGlobals

KartRace_Go = "Largar!"
KartRace_Reverse = " Rev"

#needed for leader boards
KartRace_TrackNames = {
  RaceGlobals.RT_Speedway_1     : "Estádio dos Nerds",
  RaceGlobals.RT_Speedway_1_rev : "Estádio dos Nerds" + KartRace_Reverse,
  RaceGlobals.RT_Rural_1        : "Autódromo Rústico",
  RaceGlobals.RT_Rural_1_rev    : "Autódromo Rústico" + KartRace_Reverse,
  RaceGlobals.RT_Urban_1        : "Circuito da Cidade",
  RaceGlobals.RT_Urban_1_rev    : "Circuito da Cidade" + KartRace_Reverse,
  RaceGlobals.RT_Speedway_2     : "Coliseu Saca-Rolhas",
  RaceGlobals.RT_Speedway_2_rev : "Coliseu Saca-Rolhas" + KartRace_Reverse,
  RaceGlobals.RT_Rural_2        : "Pista de Pulos",
  RaceGlobals.RT_Rural_2_rev    : "Pista de Pulos" + KartRace_Reverse,
  RaceGlobals.RT_Urban_2        : "Avenida da Neve",
  RaceGlobals.RT_Urban_2_rev    : "Avenida da Neve" + KartRace_Reverse,
 }

KartRace_Unraced = "N/D"

KartDNA_KartNames = {
    0:"Cruzeiro",
    1:"Conversível",
    2:"Utilitário Toon"
    }

KartDNA_AccNames = {
    #engine block accessory names
    1000: "Filtro de ar",
    1001: "Carburador quádruplo",
    1002: "Águia",
    1003: "Chifres",
    1004: "Seis cilindros",
    1005: "Aerofólio pequeno",
    1006: "Válvulas simples",
    1007: "Aerofólio médio",
    1008: "Carburador simples",
    1009: "Corneta",
    1010: "Aerofólio simétrico",
    #spoiler accessory names
    2000: "Asa",
    2001: "Peça recondicionada",
    2002: "Gaiola",
    2003: "Aleta",
    2004: "Asa dupla",
    2005: "Asa simples",
    2006: "Peça sobressalente padrão",
    2007: "Aleta",
    2008: "ps9",
    2009: "ps10",
    #front wheel well accessory names
    3000: "Buzina dupla",
    3001: "Para-choques do Joe",
    3002: "Estribos de cobalto",
    3003: "Descarga lateral cobra",
    3004: "Descarga lateral reta",
    3005: "Para-choques vazados",
    3006: "Estribos de carbono",
    3007: "Estribos de madeira",
    3008: "fw9",
    3009: "fw10",
    #rear wheel well accessory names (twisty twisty)
    4000: "Canos de descarga traseiros curvos",
    4001: "Para-lamas",
    4002: "Escapamento duplo",
    4003: "Aletas duplas lisas",
    4004: "Para-lamas lisos",
    4005: "Escapamento quadrado",
    4006: "Acabamento duplo",
    4007: "Megaescapamento",
    4008: "Aletas duplas simétricas",
    4009: "Aletas duplas redondas",
    4010: "Para-lamas simétricos",
    4011: "Para-lamas do Mickey",
    4012: "Para-lamas vazados",
    #rim accessoKartRace_Exit = "Sair da Corrida"ry names
    5000: "Turbo",
    5001: "Lua",
    5002: "Emendado",
    5003: "Três raios",
    5004: "Pintura da tampa",
    5005: "Coração",
    5006: "Mickey",
    5007: "Cinco raios",
    5008: "Margarida",
    5009: "Basquete",
    5010: "Hipnótico",
    5011: "Tribal",
    5012: "Diamante",
    5013: "Cinco raios",
    5014: "Roda",
    #decal accessory names
    6000: "Número cinco",
    6001: "Respingo",
    6002: "Quadriculado",
    6003: "Chamas",
    6004: "Corações",
    6005: "Bolhas",
    6006: "Tigre",
    6007: "Flores",
    6008: "Raio",
    6009: "Anjo",
    #paint accessory names
    7000: "Verde-limão",
    7001: "Pêssego",
    7002: "Vermelho vivo",
    7003: "Vermelho",
    7004: "Castanho",
    7005: "Siena",
    7006: "Marrom",
    7007: "Canela",
    7008: "Coral",
    7009: "Laranja",
    7010: "Amarelo",
    7011: "Creme",
    7012: "Cítrico",
    7013: "Limão",
    7014: "Verde-água",
    7015: "Verde",
    7016: "Azul-claro",
    7017: "Verde-azulado",
    7018: "Azul",
    7019: "Verde-musgo",
    7020: "Azul-turquesa",
    7021: "Azul-cinzento",
    7022: "Lilás",
    7023: "Púrpura",
    7024: "Rosa",
    7025: "Ameixa",
    7026: "Preto",
    }

RaceHoodSpeedway = "Autódromo"
RaceHoodRural = "Rural"
RaceHoodUrban = "Urbano"
RaceTypeCircuit = "Torneio"
RaceQualified = "classificado"
RaceSwept = "varrido"
RaceWon = "venceu"
Race = "corrida"
Races = "corridas"
Total = "total"
GrandTouring = "Gran Turismo"

def getTrackGenreString(genreId):
    genreStrings = [ "Autódromo",
                     "País",
                     "Cidade" ]
    return genreStrings[genreId].lower()

def getTunnelSignName(trackId, padId):
    # hack for bad naming!
    if trackId == 2 and padId == 0:
        return "tunne1l_citysign"
    elif trackId == 1 and padId == 0:
        return "tunnel_countrysign1"
    else:
        genreId = RaceGlobals.getTrackGenre(trackId)
        return "tunnel%s_%ssign" % (padId + 1, RaceGlobals.getTrackGenreString(genreId))

# Kart Trophy Descriptions
KartTrophyDescriptions = [
    # qualified race trophies
    RaceHoodSpeedway + " " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceQualified,
    RaceHoodSpeedway + " " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceQualified,
    RaceHoodSpeedway + " " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceQualified,
    RaceHoodRural + " " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceQualified,
    RaceHoodRural + " " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceQualified,
    RaceHoodRural + " " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceQualified,
    RaceHoodUrban + " " + str(RaceGlobals.QualifiedRaces[0]) + " " + Race + " " + RaceQualified,
    RaceHoodUrban + " " + str(RaceGlobals.QualifiedRaces[1]) + " " + Races + " " + RaceQualified,
    RaceHoodUrban + " " + str(RaceGlobals.QualifiedRaces[2]) + " " + Races + " " + RaceQualified,
    str(RaceGlobals.TotalQualifiedRaces) + " " + Total + " " + Races + " " + RaceQualified,
    # won race trophies
    RaceHoodSpeedway + " " + str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceWon,
    RaceHoodSpeedway + " " + str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceWon,
    RaceHoodSpeedway + " " + str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceWon,
    RaceHoodSpeedway + " " + str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceWon,
    RaceHoodRural + " " + str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceWon,
    RaceHoodRural + " " + str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceWon,
    RaceHoodUrban + " " + str(RaceGlobals.WonRaces[0]) + " " + Race + " " + RaceWon,
    RaceHoodUrban + " " + str(RaceGlobals.WonRaces[1]) + " " + Races + " " + RaceWon,
    RaceHoodUrban + " " + str(RaceGlobals.WonRaces[2]) + " " + Races + " " + RaceWon,
    str(RaceGlobals.TotalWonRaces) + " " + Total + " " + Races + " " + RaceWon,
    #qualified circuit races
    str(RaceGlobals.WonCircuitRaces[0]) + " " + RaceTypeCircuit + " " + Race + " " + RaceQualified,
    str(RaceGlobals.WonCircuitRaces[1]) + " " + RaceTypeCircuit + " " + Races + " " + RaceQualified,
    str(RaceGlobals.WonCircuitRaces[2]) + " " + RaceTypeCircuit + " " + Races + " " + RaceQualified,
    # won circuit race trophies
    str(RaceGlobals.WonCircuitRaces[0]) + " " + RaceTypeCircuit + " " + Race + " " + RaceWon,
    str(RaceGlobals.WonCircuitRaces[1]) + " " + RaceTypeCircuit + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonCircuitRaces[2]) + " " + RaceTypeCircuit + " " + Races + " " + RaceWon,
    # swept circuit races
    str(RaceGlobals.SweptCircuitRaces[0]) + " " + RaceTypeCircuit + " " + Race + " " + RaceSwept,
    str(RaceGlobals.SweptCircuitRaces[1]) + " " + RaceTypeCircuit + " " + Races + " " + RaceSwept,
    str(RaceGlobals.SweptCircuitRaces[2]) + " " + RaceTypeCircuit + " " + Races + " " + RaceSwept,
    # NOTE: to be added
    GrandTouring,
    # cups (+1 laff each)
    str(RaceGlobals.TrophiesPerCup) + " Troféus de corrida de kart recebidos! Mais acréscimo de pontos de risada!",
    str(RaceGlobals.TrophiesPerCup * 2) + " Troféus de corrida de kart recebidos! Mais acréscimo de pontos de risada!",
    str(RaceGlobals.TrophiesPerCup * 3) + " Troféus de corrida de kart recebidos! Mais acréscimo de pontos de risada!",
    ]

KartRace_TitleInfo = "Preparar para a corrida"
KartRace_SSInfo = "Bem-vindo ao Estádio dos Nerds!\nPé na tábua e segure firme!"
KartRace_CoCoInfo = "Bem-vindo ao Coliseu Saca-Rolhas!\nUse as curvas inclinadas para manter a velocidade!\n"
KartRace_RRInfo = "Bem-vindo ao Autódromo Rústico!\nPreserve os animais e permaneça na pista!\n"
KartRace_AAInfo = "Bem-vindo à Pista de Pulos!\nSegure firme! O caminho parece acidentado...\n"
KartRace_CCInfo = "Bem-vindo ao Circuito da Cidade!\nCuidado com os pedestres quando passar pelo centro da cidade!\n"
KartRace_BBInfo = "Bem-vindo à Avenida da Neve!\nCuidado com a velocidade. Pode ter gelo na pista.\n"
KartRace_GeneralInfo = "Use Ctrl para lançar as piadas que pegar na pista, e as teclas de setas, para controlar o kart."

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
    RaceGlobals.Daily : 'diariamente',
    RaceGlobals.Weekly : 'semanalmente',
    RaceGlobals.AllTime : 'o tempo todo',
    }

KartRace_FirstSuffix = 'o'
KartRace_SecondSuffix = ' o'
KartRace_ThirdSuffix = ' o'
KartRace_FourthSuffix = ' o'
KartRace_WrongWay = 'Direção\nerrada!'
KartRace_LapText = "Volta %s"
KartRace_FinalLapText = "Volta final!"
KartRace_Exit = "Sair da corrida"
KartRace_NextRace = "Próxima Corrida"
KartRace_Leave = "Deixar a corrida"
KartRace_Qualified = "Classificado!"
KartRace_Record = "Recorde!"
KartRace_RecordString = 'Você bateu um novo recorde %s para %s! Seu bônus é %s bilhetes.'
KartRace_Tickets = "Bilhetes"
KartRace_Exclamations = "!"
KartRace_Deposit = "Depósito"
KartRace_Winnings = "Vitórias"
KartRace_Bonus = "Bônus"
KartRace_RaceTotal = "Total da corrida"
KartRace_CircuitTotal = "Total do Circuito"
KartRace_Trophies = "Troféus"
KartRace_Zero = "0"
KartRace_Colon = ":"
KartRace_TicketPhrase = "%s" + KartRace_Tickets
KartRace_DepositPhrase = KartRace_Deposit + KartRace_Colon + "\n" + KartRace_Tickets
KartRace_QualifyPhrase = "Classificar:\n"
KartRace_RaceTimeout = "Tempo esgotado nesta corrida. Seus bilhetes foram reembolsados. Continue tentando!"
KartRace_RaceTimeoutNoRefund = "O tempo da corrida esgotou.  Seus bilhetes não foram reembolsados porque o Grande Prêmio já começou.  Continue tentando!"
KartRace_RacerTooSlow = "Você demorou demais para terminar a corrida.  Seus bilhetes não foram reembolsados.  Continue tentando!"
KartRace_PhotoFinish = "Foto da chegada!"
KartRace_CircuitPoints = 'Pontos do Circuito'

CircuitRaceStart = "O Grande Prêmio de Toontown está prestes a começar!  Para vencer, ganhe o maior número de pontos em três corridas consecutivas!"
CircuitRaceOngoing = "Olá! O Grande Prêmio de Toontown está acontecendo agora."
CircuitRaceEnd = "E por hoje é só do Grande Prêmio de Toontown no Autódromo do Pateta.  Vejo você na próxima segunda-feira!"

# Trick-or-Treat holiday
TrickOrTreatMsg = 'Você já encontrou\nesta gostosura!'

#temp lawbot boss dialog text
LawbotBossTempIntro0 = "Humm, o que temos na pauta de casos hoje?"
LawbotBossTempIntro1 = "Arrá, temos o julgamento de um Toon!"
LawbotBossTempIntro2 = "O caso da promotoria é forte."
LawbotBossTempIntro3 = "E aqui estão os defensores públicos."
LawbotBossTempIntro4 = "Espere um pouco... Vocês são Toons!"
LawbotBossTempJury1 = "A seleção do júri vai começar agora."
LawbotBossHowToGetEvidence = "Toque na tribuna da testemunha para pegar a evidência."
LawbotBossTrialChat1 = "A sessão da Corte está aberta"
LawbotBossHowToThrowPies = "Aperte a tecla Insert para arremessar a evidência\n nos advogados ou na balança!"
LawbotBossNeedMoreEvidence = "Você precisa de mais evidências!"
LawbotBossDefenseWins1 = "Impossível! A defesa venceu?"
LawbotBossDefenseWins2 = "Não. Eu declaro este julgamento nulo! Um novo julgamento será agendado."
LawbotBossDefenseWins3 = "Humpf. Estarei na minha sala."
LawbotBossProsecutionWins = "Eu julgo em favor do querelante"
LawbotBossReward = "O prêmio é uma promoção e a habilidade de evocar Cogs"
LawbotBossLeaveCannon = "Deixar canhão"
LawbotBossPassExam = "Bah, e daí que você passou no exame da ordem dos advogados?"
LawbotBossTaunts = [
    "%s, eu julgo você em desacato desta corte!",
    "Objeção aceita!",
    "Apague isso dos registros.",
    "Sua apelação foi rejeitada. A sua sentença é a tristeza!",
    "Ordem na corte!",
    ]
LawbotBossAreaAttackTaunt = "Vocês todos estão em desacato da corte!"

WitnessToonName = "Abel Abelhudo"
WitnessToonPrepareBattleTwo = "Oh, não! Eles estão colocando apenas Cogs no júri!\aRápido, use os canhões e atire alguns jurados Toons nas cadeiras do júri.\aPrecisamos de %d para ter uma balança justa."
WitnessToonNoJuror = "Oh-oh, sem jurados Toons. Vai ser um julgamento difícil."
WitnessToonOneJuror = "Legal! Tem 1 Toon no júri!"
WitnessToonSomeJurors = "Legal! Tem %d Toons no júri!"
WitnessToonAllJurors = "Irado! Todos os jurados são Toons!"
WitnessToonPrepareBattleThree = "Rápido, toque na tribuna da testemunha para pegar evidências.\aAperte a tecla Insert para arremessar a evidência nos advogados, ou no prato da defesa."
WitnessToonCongratulations = "Você conseguiu!  Obrigado por uma defesa espetacular!\aAqui ,fique com estes papéis deixados pelo Juiz-chefe.\aCom isto você será capaz de evocar Cogs da sua página Galeria de Cogs."

WitnessToonLastPromotion = "\aUau, você atingiu o nível %s do seu Disfarce de Cog!\aOs Cogs não são promovidos mais que isso.\aVocê não pode mais atualizar o seu Disfarce de Cog, mas ainda pode continuar trabalhando pela Resistência!"
WitnessToonHPBoost = "\aVocê fez muito pela Resistência.\aO Conselho de Toons decidiu lhe dar mais um ponto de Risada. Parabéns!"
WitnessToonMaxed = "\aVejo que tem um Disfarce de Cog nível %s. Impressionante!\aEm nome de todo o Conselho de Toons, obrigado por voltar para defender mais Toons!"
WitnessToonBonus = "Maravilhoso! Todos os advogados estão atordoados. O peso da sua evidência foi %s vezes mais denso por %s segundos"

WitnessToonJuryWeightBonusSingular = {
  6: 'Este caso é difícil. Você sentou %d jurado Toon, então a sua evidência tem um peso-bônus de %d.',
  7: 'Este caso é muito difícil. Você sentou %d jurado Toon, então a sua evidência tem um peso-bônus de %d.',
  8: 'Este caso é o mais difícil. Você sentou %d jurado Toon, então a sua evidência tem um peso-bônus de %d.',
}

WitnessToonJuryWeightBonusPlural = {
  6: 'Este caso é difícil. Você sentou %d jurados Toon, então a sua evidência tem um peso-bônus de %d.',
  7: 'Este caso é muito difícil. Você sentou %d jurados Toon, então a sua evidência tem um peso-bônus de %d.',
  8: 'Este caso é o mais difícil. Você sentou %d jurados Toon, então a sua evidência tem um peso-bônus de %d.',
}

# Cog Summons stuff
IssueSummons = "Evocar"
SummonDlgTitle = "Evocar um Cog"
SummonDlgButton1 = "Evocar um Cog"
SummonDlgButton2 = "Evocar um Prédio Cog"
SummonDlgButton3 = "Evocar uma Invasão Cog"
SummonDlgSingleConf = "Gostaria de evocar um %s?"
SummonDlgBuildingConf = "Gostaria de evocar um %s para um prédio Toon próximo?"
SummonDlgInvasionConf = "Gostaria de evocar uma invasão de %s?"
SummonDlgNumLeft = "Você tem %s sobrando."
SummonDlgDelivering = "Evocando..."
SummonDlgSingleSuccess = "Você evocou o Cog com sucesso."
SummonDlgSingleBadLoc = "Desculpe, mas cogs são proibidos aqui.  Tente em outro lugar."
SummonDlgBldgSuccess = "Você evocou os Cogs com sucesso. %s concordou em deixá-los tomar %s por um tempo!"
SummonDlgBldgSuccess2 = "Você evocou os Cogs com sucesso. Um Dono de Loja concordou em deixá-los tomar o prédio dele por um tempo!"
SummonDlgBldgBadLoc = "Desculpe, não há prédios Toon por perto para os Cogs tomarem."
SummonDlgInvasionSuccess = "Você evocou os Cogs com sucesso. É uma invasão!"
SummonDlgInvasionBusy = "Um %s não pôde ser encontrado.  Tente novamente quando a invasão dos Cogs terminar."
SummonDlgInvasionFail = "Desculpe, a invasão dos Cogs fracassou."
SummonDlgShopkeeper = "O Dono da Loja "

# Polar Place cheesy effect chat phrases
PolarPlaceEffect1 = NPCToonNames[3306] + ": Bem-vindo ao Lugar Polar!"
PolarPlaceEffect2 = NPCToonNames[3306] + ": Tente isto."
PolarPlaceEffect3 = NPCToonNames[3306] + ": A sua nova aparência só vai funcionar em " + lTheBrrrgh + "."

# LaserGrid game Labels
LaserGameMine = "Caça-Caveiras!"
LaserGameRoll = "Combinando"
LaserGameAvoid = "Evite as Caveiras"
LaserGameDrag = "Arraste três da mesma cor em uma fileira"
LaserGameDefault = "Jogo Desconhecido"

# Pinball text
#PinballHiScore = "Maior Pontuação: %d %s\n"
#PinballYourBestScore = "Sua Melhor Pontuação: %d\n"
#PinballScore = "Pontuação: %d x %d : %d"
PinballHiScore = "Maior Pontuação: %s\n"
PinballHiScoreAbbrev = "..."
PinballYourBestScore = "Sua Melhor Pontuação:\n"
PinballScore = "Pontuação:        %d x %d = "
PinballScoreHolder = "%s\n"


# Gardening text
GagTreeFeather = "Árvore de Piada de Pena"
GagTreeJugglingBalls = "Árvore de Piada de Bolinhas de Malabarismo"
StatuaryFountain = "Fonte"
StatuaryToonStatue = "Estátua de Toon"
StatuaryDonald = "Estátua do Donald"
StatuaryMinnie = "Estátua da Minnie"
StatuaryMickey1 = "Estátua do Mickey"
StatuaryMickey2 = "Fonte do Mickey"
StatuaryToon = "Estátua de Toon"
StatuaryToonWave = "Estátua da Onda Toon"
StatuaryToonVictory = "Estátua da Vitória Toon"
StatuaryToonCrossedArms = 'Estátua da Autoridade Toon'
StatuaryToonThinking = 'Estátua do Abraço Toon'
StatuaryMeltingSnowman =' Boneco de neve Derretendo' 
StatuaryGardenAccelerator = "Fertilizante Instantâneo"
#see GardenGlobals.py for corresponding FlowerColors
FlowerColorStrings = ['Vermelha','Laranja','Violeta','Azul','Rosa','Amarela','Branca','Verde']
#see GardenGlobals.py for PlantAttributes, keys must match
FlowerSpeciesNames = {
    49: 'Margarida',
    50: 'Tulipa',
    51: 'Cravo',
    52: 'Lírio',
    53: 'Narciso',
    54: 'Tilápia',
    55: 'Petúnia',
    56: 'Rosa',
    }
#see GardenGlobals.py for PlantAttributes, keys must match, varieties must match
FlowerFunnyNames = {
    49: ('Margarida Lida',
         'Margarida Sumida',
         'Margarida Querida',
         'Margarida Lambida',
         'Margarida Caída',
         'Margarida Subida',
         'Margarida Enlouquecida',
         'Margarida Esclarecida',
         ),
    50:  ('Eulipa',
          'Tulipas',
          'Elelipa',
          ),
    51:  ('Encravou',
          'Cravado',
          'Cravo Híbrido',
          'Cravo de Lado',
          'Cravo Modelo',
          ),
    52: ('De Lírio',
         'Co Lírio',
         'Lírio Selvagem',
         'Lírio Figueiro',
         'Lírio Pimenta',
         'Lírio Bobo',
         'Eclírio',
         'Lírio Dílio',
         ),
    53: ('Nar-sorriso',
         'Nariz Ciso',
         'Narcisudo',
         'Ante Narciso',
         ),
    54: ('Tilápia Pudo',
         'Ene-A-O-Tilápia',
         'Tilapiano',
         'Tilapiada',
         'Tilápia Sábia',
         ),
    55: ('Car Petúnia',
         'Platúnia',
         ),
    56: ("Última Rosa do Verão",
         'Choque de Rosa',
         'Rosa Tinta',
         'Rosa Fedida',
         'Rosa Aindarrosa',
         ),
    }
FlowerVarietyNameFormat = "%s %s"
FlowerUnknown = "????"
ShovelNameDict = {
    0 : "Latão",
    1 : "Bronze",
    2 : "Prata",
    3 : "Ouro",
    }
WateringCanNameDict = {
    0 : "Pequeno",
    1 : "Médio",
    2 : "Grande",
    3 : "Enorme",
    }
GardeningPlant = "Plantar"
GardeningWater = "Regar"
GardeningRemove = "Remover"
GardeningPick = "Colher"
GardeningFull = "Encher"
GardeningSkill = "Habilidade"
GardeningWaterSkill = "Habilidade na Água"
GardeningShovelSkill = "Habilidade com a Pá"
GardeningNoSkill = "Nenhuma Habilidade"
GardeningPlantFlower = "Plantar\nFlor"
GardeningPlantTree = "Plantar\nÁrvore"
GardeningPlantItem = "Plantar\nItem"
PlantingGuiOk = "Plantar"
PlantingGuiCancel = lCancel
PlantingGuiReset = "Restaurar"
GardeningChooseBeans = "Escolha as balinhas que deseja plantar."
GardeningChooseBeansItem  = "Escolha as balinhas / item que deseja plantar."
GardeningChooseToonStatue = "Escolha o Toon do qual deseja criar uma estátua."
GardenShovelLevelUp = "Parabéns, você ganhou uma nova pá!"
GardenShovelSkillLevelUp = "Parabéns! Você atingiu %(oldbeans)d violetas! Para progredir, você deve coletar %(newbeans)d violetas."
GardenShovelSkillMaxed = "Incrível! Você superou sua habilidade com a pá!"

GardenWateringCanLevelUp = "Parabéns, você ganhou um novo regador!"
GardenMiniGameWon = "Parabéns, você regou a planta!"
ShovelTin = "Pá de Latão"
ShovelSteel = "Pá de Aço"
ShovelSilver = "Pá de Prata"
ShovelGold = "Pá de Ouro"
WateringCanSmall = "Regador Pequeno"
WateringCanMedium = "Regador Médio"
WateringCanLarge = "Regador Grande"
WateringCanHuge = "Regador Enorme"
#make sure it matches GardenGlobals.BeanColorLetters
BeanColorWords = ('vermelha', 'verde', 'laranja','lilás','azul','rosa','amarela',
                  'ciano','prata')
PlantItWith = " Plante com %s."
MakeSureWatered = " Primeiramente, certifique-se de que todas as plantas foram regadas."
UseFromSpecialsTab = "Use por meio da guia de especiais na página do jardim."
UseSpecial = "Usar Especial"
UseSpecialBadLocation = 'Você só pode usar isso no seu jardim.'
UseSpecialSuccess = 'Sucesso! Suas plantas regadas acabaram de crescer.'
ConfirmWiltedFlower = "%(plant)s murchou.  Tem certeza de que quer removê-la?  Ela não irá para o seu cesto de flores, e você também não receberá aumento na sua habilidade."
ConfirmUnbloomingFlower = "%(plant)s não está desabrochando.  Tem certeza de que quer removê-la?  Ela não irá para o seu cesto de flores, e você também não receberá aumento na sua habilidade."
ConfirmNoSkillupFlower = "Tem certeza de que quer remover %(plant)s? Ela não irá para o seu cesto de flores, e você também não receberá aumento na sua habilidade."
ConfirmSkillupFlower = "Tem certeza de que quer colher %(plant)s?  Ela irá para o seu cesto de flores. Você vai receber um aumento de habilidade."
ConfirmMaxedSkillFlower = "Tem certeza que quer colher as %(plant)s?  Elas irão para sua cesta de flores. Suas habilidades NÃO aumentarão pois você já atingiu o máximo."
ConfirmBasketFull = "Seu cesto de flores está cheio. Venda algumas flores primeiro."
ConfirmRemoveTree = "Tem certeza de que quer remover %(tree)s?"
ConfirmWontBeAbleToHarvest = " Se você remover esta árvore, você não colherá piadas das árvores mais altas."
ConfirmRemoveStatuary = "Tem certeza de que quer apagar para sempre %(item)s?"
ResultPlantedSomething  = "Parabéns! Você acaba de plantar %s."
ResultPlantedSomethingAn  = "Parabéns! Você acaba de plantar %s."
ResultPlantedNothing = "Isso não funcionou.  Por favor, tente uma combinação diferente de balinhas."

GardenGagTree = "TODO??? "
GardenUberGag = "TODO??? "

def getRecipeBeanText(beanTuple):
    """
    dado um múltiplo de balinhas, ex. (0,6), retorna uma versão de texto para
    ser exibida para o usuário. (ex: uma balinha vermelha e amarela)
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
            retval = "%d %s balinhas" % (len(beanTuple),
                                           BeanColorWords[beanTuple[0]])
        else:
            retval = "uma balinha %s" % BeanColorWords[beanTuple[0]]
    else:
        retval += 'a'
        maxBeans = len(beanTuple)
        for index in range(maxBeans):
            if index == maxBeans - 1:
                retval += " e balinha %s" % BeanColorWords[beanTuple[index]]
            elif index == 0:
                retval += " %s" % BeanColorWords[beanTuple[index]]
            else:
                retval += ", %s" % BeanColorWords[beanTuple[index]]

    return retval
    
GardenTextMagicBeans = "Balas Mágicas"
GardenTextMagicBeansB = "Outras Balas"
GardenSpecialDiscription = "Este texto deveria explicar como usar certo especial do jardim"
GardenSpecialDiscriptionB = "Este texto deveria explicar como usar certo especial do jardim, podicrê!"
GardenTrophyAwarded = "Uau! Você tem %s de %s flores. Isso merece um troféu e uma melhora na Risada!"
GardenTrophyNameDict = {
    0 : "Carrinho de Mão",
    1 : "Pás",
    2 : "Flor",
    3 : "Regador",
    4 : "Tubarão",
    5 : "Peixe-Espada",
    6 : "Baleia Assassina",
    }
SkillTooLow = "Habilidade\nBaixa Demais"
NoGarden = "Nenhum \nJardim"

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
TravelGameTitle = "Trilhos de Bonde"
TravelGameInstructions = "Clique para cima ou para baixo para definir seu número de votos.  Clique no botão votar para lançar os votos. Chegue ao seu objetivo secreto para conseguir balinhas extras. Ganhe mais votos quando se der bem nos outros jogos."
TravelGameRemainingVotes = "Votos Restantes:"
TravelGameUse = "Usar"
TravelGameVotesWithPeriod = "votos."
TravelGameVotesToGo = "votos restantes"
TravelGameVoteToGo = "voto restante"
TravelGameUp = "PARA CIMA."
TravelGameDown = "PARA BAIXO."
TravelGameVoteWithExclamation = "Vote!"
TravelGameWaitingChoices = "Esperando que outros jogadores votem..."
# cross the bridge later when the first choice is different for each node,
# e.g. NorthWest, NorthEast, etc.
TravelGameDirections = ['PARA CIMA', 'PARA BAIXO']
TravelGameTotals = 'Totais '
TravelGameReasonVotesPlural = 'O bonde está indo para %(dir)s, vencendo por %(numVotes)de votos.'
TravelGameReasonVotesSingular = 'O bonde está indo para %(dir)s, vencendo por %(numVotes)de voto.'
TravelGameReasonPlace = '%(name)s desempatou. O bonde está indo para %(dir)s.'
TravelGameReasonRandom = 'O bonde está indo aleatoriamente para %(dir)s.'
TravelGameOneToonVote =   "%(name)s usou %(numVotes)s votos para ir para %(dir)s\n"
TravelGameBonusBeans = "%(numBeans)de Balinhas"
TravelGamePlaying = 'A seguir, o jogo do bonde de %(game)s.'
TravelGameGotBonus = '%(name)s ganhou um bônus de %(numBeans)s balinhas!'
TravelGameNoOneGotBonus = "Ninguém chegou ao seu objetivo secreto.  Todos ganham 1 balinha."
TravelGameConvertingVotesToBeans = "Convertendo alguns votos em balinhas..."
TravelGameGoingBackToShop ="Só resta 1 jogador. Indo para a Loja de Piadas do Pateta."

PairingGameTitle = "Jogo de Memória Toon"
PairingGameInstructions = "Aperte Delete para virar uma carta. Combine 2 cartas iguais para marcar um ponto. Combine cartas com o brilho de bônus e ganhe um ponto extra. Ganhe mais pontos virando poucas vezes."
PairingGameInstructionsMulti = "Aperte Delete para virar uma carta. Aperte Ctrl para fazer o sinal para outro jogador virar uma carta. Combine 2 cartas iguais para marcar um ponto. Combine cartas com o brilho de bônus e ganhe um ponto extra. Ganhe mais pontos virando poucas vezes."
PairingGamePerfect = 'PERFEITO!!'
PairingGameFlips = 'Viradas:'
PairingGamePoints = 'Pontos:'

TrolleyHolidayStart = "Vamos começar com os Trilhos de Bonde!  Para jogar, embarque em qualquer bonde com 2 ou mais Toons."
TrolleyHolidayOngoing = ""
TrolleyHolidayEnd = "Isso é tudo nos Trilhos de Bonde por hoje.  Até a próxima semana!"

TrolleyWeekendStart = "O Fim de Semana dos Trilhos de Bonde vai começar!  Para jogar, embarque em qualquer bonde com 2 ou mais Toons."
TrolleyWeekendEnd = "Terminamos com o Fim de Semana dos Trilhos de Bonde."

VineGameTitle = "Cipós da Selva"
VineGameInstructions = "Chegue ao cipó mais à direita a tempo. Aperte para Cima ou para Baixo para escalar o cipó.  Aperte para Esquerda ou Direita para mudar de direção e pular.  Quanto mais baixo você estiver no cipó, mais rápido poderá saltar dele. Colete as bananas se puder, mas evite os morcegos e aranhas."

# Make sure the golf text matches up with GolfGlobals.py
GolfCourseNames = {
    0: "Tacada e Caminhada",
    1: "Tacadas Divertidas",
    2: "Todas as Tacadas"
    }

GolfHoleNames = {
    0: 'Vitória-em-Uma',
    1: 'Sem Dúvida até o Buraco',
    2: 'Só na Descida',
    3: 'Só Vejo Verde',
    4: 'Tacadas Quentes',
    5: 'É na Manteiga',
    6: 'Balanço do Taco',
    7: 'Na Tacada das Cinco Horas',
    8: 'Diversão no Gramadão',
    9: 'A Bola Cai e a Gente Vibra',
    10: 'Nada de Bogey',
    11: 'Hora do Taco',
    12: 'Santa Tacada!',
    13: 'Só um Birdie, Vai',
    14: 'Correndo para o Buraco',
    15: 'Hora da Tacada',
    16: 'Buraco ao Alcance',
    17: 'Mais um Vento e Chega',
    18: 'Vitória-em-Uma-2',
    19: 'Sem Dúvida, até o Buraco-2',
    20: 'Só na Descida-2',
    21: 'Só Vejo Verde-2',
    22: 'Tacadas Quentes-2',
    23: 'É na Manteiga-2',
    24: 'Balanço do Taco-2',
    25: 'Na Tacada das Cinco Horas-2',
    26: 'Diversão no Gramadão-2',
    27: 'A Bola Cai e a Gente Vibra-2',
    28: 'Nada de Bogey-2',
    29: 'Hora do Taco-2',
    30: 'Santa Tacada!-2',
    31: 'Só um Birdie, Vai-2',
    32: 'Correndo para o Buraco-2',
    33: 'Hora da Tacada-2',
    34: 'Buraco ao Alcance-2',
    35: 'Mais um Vento e Chega-2',
    }

GolfHoleInOne = "Buraco-em-Uma"
GolfCondor = "Condor" # four Under Par
GolfAlbatross = "Albatroz" # three under par
GolfEagle = "Águia" # two under par
GolfBirdie = "Passarinho" # one under par
GolfPar = "Par"
GolfBogey = "Bogey" # one over par
GolfDoubleBogey = "Bogey Duplo" # two over par
GolfTripleBogey = "Bogey Triplo" # three over par

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

CoursesCompleted = "Percursos Concluídos"
CoursesUnderPar = "Percursos Abaixo do Par"
HoleInOneShots = "Jogadas de Buraco-em-Uma"
EagleOrBetterShots = "Jogadas de Eagle ou Melhor"
BirdieOrBetterShots = "Jogadas de Birdie ou Melhor"
ParOrBetterShots = "Jogadas de Par ou Melhor"
MultiPlayerCoursesCompleted = "Concursos Multiplayer Concluídos"
TwoPlayerWins = "Vitórias com Dois Jogadores"
ThreePlayerWins = "Jogadas com Três Jogadores"
FourPlayerWins = "Jogadas com Quatro Jogadores"
CourseZeroWins = GolfCourseNames[0] + " Vitórias"
CourseOneWins = GolfCourseNames[1] + " Vitórias"
CourseTwoWins = GolfCourseNames[2] + " Vitórias"

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
    str(GolfGlobals.TrophiesPerCup) + " Troféus ganhos",
    str(GolfGlobals.TrophiesPerCup * 2) + " Troféus ganhos",
    str(GolfGlobals.TrophiesPerCup * 3) + " Troféus ganhos",
]

GolfAvReceivesHoleBest = "%(name)s marcou um novo recorde de tacadas em %(hole)s!"
GolfAvReceivesCourseBest = "%(name)s marcou um novo recorde de percurso em %(course)s!!"
GolfAvReceivesCup = "%(name)s ganhou a taça %(cup)s!!  Bônus em pontos de risada!"
GolfAvReceivesTrophy = "%(name)s ganhou o troféu %(award)s!!"
GolfRanking = "Posição: \n"
GolfPowerBarText = "%(power)s%%"
GolfChooseTeeInstructions = "Aperte para Esquerda ou Direita para mudar a posição do taco.\nAperte Ctrl para selecionar."
GolfWarningMustSwing = "Atenção: você precisa apertar Ctrl na sua próxima tacada."
GolfAimInstructions = "Aperte para a Esquerda ou Direita para mirar.\nAperte e segure Ctrl para balançar o taco."
GolferExited = "%s saiu do percurso de golfe."
GolfPowerReminder = "Segure Ctrl por Mais Tempo para\nMandar a Bola Mais Longe"


# GolfScoreBoard.py
GolfPar = "Par"
GolfHole = "Buraco"
GolfTotal = "Total"
GolfExitCourse = "Sair do Percurso"
GolfUnknownPlayer = "???"

# GolfPage.py
GolfPageTitle = "Golfe"
GolfPageTitleCustomize = "Personalizador de Golfe"
GolfPageTitleRecords = "Recordes Pessoais"
GolfPageTitleTrophy = "Troféus de Golfe"
GolfPageCustomizeTab = "Personalizar"
GolfPageRecordsTab = "Recordes"
GolfPageTrophyTab = "Troféu"
GolfPageTickets = "Bilhetes: "
GolfPageConfirmDelete = "Apagar Acessório?"
GolfTrophyTextDisplay = "Troféu %(number)s : %(desc)s"
GolfCupTextDisplay = "Taça %(number)s : %(desc)s"
GolfCurrentHistory = "%(historyDesc)s Atual: %(num)s"
GolfTieBreakWinner = "%(name)s venceu o desempate aleatório!"
GolfSeconds = " -  %(time).2f segundos"
GolfTimeTieBreakWinner = "%(name)s venceu o desempate por tempo total de mira!!!"



RoamingTrialerWeekendStart = "Está começando a Tour por Toontown! Jogadores podem entrar em qualquer vizinhança de graça!"
RoamingTrialerWeekendOngoing = "Boas-vindas ao Tour por Toontown! Jogadores podem entrar gratuitamente em qualquer vizinhança!"
RoamingTrialerWeekendEnd = "Terminamos com o Tour por Toontown."

# change double if ToontownBattleGlobals.getMoreXpHolidayMultiplier() changes
MoreXpHolidayStart = "Boas novas! Começou o período de Teste Toon, com o dobro de experiência em piadas."
MoreXpHolidayOngoing = "Olá! Estamos no período de Teste Toon, com o dobro de experiência em piadas."
MoreXpHolidayEnd = "Terminou o período exclusivo de Teste Toon, com o dobro de experiência em piadas. Obrigado por nos ajudar a Testar!"

JellybeanDayHolidayStart = "É Dia das Balinhas! Ganhe prêmios de Balinhas em dobro nas Festas!"
JellybeanDayHolidayEnd = "Acabou o Dia das Balinhas. Vejo você no ano que vem."
PartyRewardDoubledJellybean = "Balinhas em Dobro!"

GrandPrixWeekendHolidayStart = "É o Fim de Semana do Grande Prêmio no Autódromo do Pateta! Quem jogar gratuitamente ou pagando pode obter a maioria dos pontos em três corridas consecutivas."
GrandPrixWeekendHolidayEnd = "O Fim de Semana do Grande Prêmio acabou. Vejo você no ano que vem."

LogoutForced = "Você fez algo errado\n e estamos fazendo seu logout automaticamente,\n sua conta também pode estar congelada.\n Experimente dar uma volta lá fora, é divertido."

# DistributedCountryClub.py
CountryClubToonEnterElevator = "%s \nentrou no carrinho de golfe."
CountryClubBossConfrontedMsg = "%s está lutando com o Presidente do Clube!"

# DistributedElevatorFSM.py
ElevatorBlockedRoom = "Todos os desafios devem ser vencidos antes disso."

# DistributedMolefield.py
MolesLeft = "Toupeiras Restantes: %d"
MolesInstruction = "Pisão nas Toupeiras!\nPule nas toupeiras vermelhas!"
MolesFinished = "Pisão nas Toupeiras vencido!"
MolesRestarted = "Perdeu no Pisão! Recomeçando..."

# DistributedGolfGreenGame.py
BustACogInstruction = "Remova a bola Cog!"
BustACogExit = "Sair por Enquanto"
BustACogHowto = "Como Jogar"
BustACogFailure = "Acabou o Tempo!"
BustACogSuccess = "Sucesso!"

# bossbot golf green games
GolfGreenGameScoreString = "Quebra-Cabeças Restantes: %s"
GolfGreenGamePlayerScore = "Resolveu %s"
GolfGreenGameBonusGag = "Você ganhou %s!"
GolfGreenGameGotHelp = "%s resolveu um Quebra-Cabeça!"

GolfGreenGameDirections = "Dê tacadas nas bolas usando o mouse\n\n\nCombinar três bolas de uma mesma cor as faz cair\n\n\nRemova todas as bolas Cog da tela"

# DistributedMaze.py
enterHedgeMaze = "Corra pela Sebe-Labirinto\n para ganhar bônus de risadas!"
toonFinishedHedgeMaze = "%s \n  terminou em %s lugar!"
hedgeMazePlaces = ["primeiro","segundo","terceiro","quarto"]
mazeLabel = "Corrida no Labirinto!"

# Boarding Group
BoardingPartyReadme = 'Grupo de Abordagem?'
BoardingGroupHide = 'Ocultar'
BoardingGroupShow = 'Exibir Grupo de Abordagem'
BoardingPartyInform = 'Crie um Grupo de Abordagem para o elevador clicando em outro Toon e fazendo um convite.\nNessa área, os Grupos de Abordagem não podem ter mais de %s Toons.'
BoardingPartyTitle = 'Grupo de Abordagem'
QuitBoardingPartyLeader = 'Dispensar'
QuitBoardingPartyNonLeader = 'Deixar'
QuitBoardingPartyConfirm = 'Tem certeza de que quer sair desse Grupo de Abordagem?'
BoardcodeMissing = 'Aconteceu algum erro; tente mais tarde.'
BoardcodeMinLaffLeader = 'Não é possível fazer abordagem com seu grupo porque você tem menos de %s pontos de risada.'
BoardcodeMinLaffNonLeaderSingular = 'Seu grupo não pode fazer abordagem porque %s tem menos de %s pontos de risada.'
BoardcodeMinLaffNonLeaderPlural = 'Seu grupo não pode fazer abordagem porque %s tem menos de %s pontos de risada.'
BoardcodePromotionLeader = 'Seu grupo não pode fazer abordagem porque você não tem méritos de promoção suficientes.'
BoardcodePromotionNonLeaderSingular = 'Seu grupo não pode fazer abordagem porque %s não tem méritos de promoção suficientes.'
BoardcodePromotionNonLeaderPlural = 'Seu grupo não pode fazer abordagem porque %s não tem méritos de promoção suficientes.'
BoardcodeSpace = 'Seu grupo não pode fazer abordagem porque não tem espaço suficiente.'
BoardcodeBattleLeader = 'Seu grupo não pode fazer abordagem porque você está combatendo.'
BoardcodeBattleNonLeaderSingular = 'Seu grupo não pode fazer abordagem porque %s está combatendo.'
BoardcodeBattleNonLeaderPlural = 'Seu grupo não pode fazer abordagem porque %s está combatendo.'
BoardingInviteMinLaffInviter = 'Você precisa de %s Pontos de Risada antes de se tornar associado desse Grupo de Abordagem.'
BoardingInviteMinLaffInvitee = '%s precisa de %s Pontos de Risada antes de se tornar associado desse Grupo de Abordagem.'
BoardingInvitePromotionInviter = 'Você precisa receber uma promoção antes de se tornar associado desse Grupo de Abordagem.'
BoardingInvitePromotionInvitee = '%s precisa receber uma promoção antes de se tornar associado desse Grupo de Abordagem.'
BoardingInviteNotPaidInvitee = '%s precisa ser um Assinante para fazer parte do seu Grupo de Abordagem.'
BoardingInviteeInDiffGroup = '%s já está em outro Grupo de Abordagem.'
BoardingInviteeInKickOutList = '%s foi removido por seu líder. Apenas o líder pode reconvidar associados removidos.'
BoardingInviteePendingIvite = '%s tem um convite pendente; tente novamente mais tarde.'
BoardingInviteeInElevator = '%s está ocupado(a) no momento; tente novamente mais tarde.'
BoardingInviteGroupFull = 'Seu Grupo de Abordagem já está completo'
BoardingAlreadyInGroup = 'Você não pode aceitar esse convite porque já está em outro Grupo de Abordagem.'
BoardingGroupAlreadyFull = 'Você não pode aceitar esse convite porque o grupo já está completo.'
BoardingKickOutConfirm = 'Tem certeza de que quer remover %s?'
BoardingPendingInvite = 'Primeiro você tem de resolver\n o convite pendente.'
BoardingCannotLeaveZone = 'Você não pode deixar essa área porque você faz parte de um Grupo de Abordagem.'
BoardingInviteeMessage = "%s gostaria de se juntar ao seu Grupo de Abordagem."
BoardingInvitingMessage = "Convidando %s para seu Grupo de Abordagem."
BoardingInvitationRejected = "%s recusou se juntar ao seu Grupo de Abordagem."
BoardingMessageKickedOut = "Você foi removido do Grupo de Abordagem."
BoardingMessageInvited = "%s convidou %s para o Grupo de Abordagem."
BoardingMessageLeftGroup = "%s deixou o Grupo de Abordagem."
BoardingMessageGroupDissolved = "Seu Grupo de Abordagem foi dispensado pelo líder do grupo."
BoardingMessageGroupDisbandedGeneric = "Seu Grupo de Abordagem foi dispensado."
BoardingMessageInvitationFailed = "%s tentou convidar você para seu Grupo de Abordagem."
BoardingMessageGroupFull = "%s tentou aceitar seu convite, mas seu grupo estava completo."
BoardingGo = 'IR'
BoardingCancelGo = 'Clique Novamente para\nCancelar o comando Ir'
And = 'e'
BoardingGoingTo = 'Indo Para:'
BoardingTimeWarning = 'Abordando o elevador em '
BoardingMore = 'mais'
BoardingGoShow = 'Indo para\n%s em '
BoardingGoPreShow = 'Confirmando...'

# DistributedBossbotBoss.py
BossbotBossName = "Presidente"
BossbotRTWelcome = "Seus Toons vão precisar de disfarces diferentes."
BossbotRTRemoveSuit = "Primeiramente, tire suas roupas de Cog..."
BossbotRTFightWaiter = "e, então, lute com estes garçons."
BossbotRTWearWaiter = "Bom Trabalho! Agora, coloque as roupas de garçom."
BossbotBossPreTwo1 = "Por que está demorando tanto? "
BossbotBossPreTwo2 = "Vamos, sirva meu banquete!"
BossbotRTServeFood1 = "Hehe, sirva a comida que eu coloco nestas esteiras."
BossbotRTServeFood2 = "Se você servir um Cog três vezes seguidas, ele vai explodir."
BossbotResistanceToonName = "A velha e boa Risada"
BossbotPhase3Speech1 = "O que está acontecendo aqui?!"
BossbotPhase3Speech2 = "Esses garçons são Toons!"
BossbotPhase3Speech3 = "Peguem-nos!!!"
BossbotPhase4Speech1 = "Humpf. Se quero um trabalho bem feito..."
BossbotPhase4Speech2 = "tenho de fazer eu mesmo."
BossbotRTPhase4Speech1 = "Bom Trabalho! Agora, esguiche água no Presidente nas mesas..."
BossbotRTPhase4Speech2 = "ou use bolas de golfe para atrasá-lo."
BossbotPitcherLeave = "Deixar Garrafa"
BossbotPitcherLeaving = "Deixando Garrafa"
BossbotPitcherAdvice = "Use as teclas para esquerda e direita se quiser girar.\nSegure Ctrl para aumentar a força.\nSolte Ctrl para disparar."
BossbotGolfSpotLeave = "Deixar Bola de Golfe"
BossbotGolfSpotLeaving = "Deixando Bola de Golfe"
BossbotGolfSpotAdvice = "Use as teclas para esquerda e direita se quiser girar.\nCtrl dispara."
BossbotRewardSpeech1 = "Não! O Presidente do Conselho não vai gostar disso."
BossbotRewardSpeech2 = "Arrrggghhh!!!!"
BossbotRTCongratulations = "Você conseguiu!  Você rebaixou o Presidente!\aPegue estes bilhetes azuis que o Presidente deixou para trás.\aCom eles, você vai poder disparar contra Cogs em batalha."""
BossbotRTLastPromotion = "\aUau, você chegou ao nível %s com sua Roupa de Cog!\aOs Cogs não conseguem promoções maiores do que essa.\aVocê não pode mais atualizar sua Roupa de Cog, mas, certamente, poderá continuar trabalhando para a Resistência!"
BossbotRTHPBoost = "\aVocê trabalhou bastante para a Resistência.\aO Conselho Toon decidiu lhe dar mais um ponto de Risada. Parabéns!"
BossbotRTMaxed = "\aVejo que você tem uma Roupa de Cog de nível %s. Impressionante!\aEm nome do Conselho Toon, agradeço por voltar para defender mais Toons!"
GolfAreaAttackTaunt = "Bola!"
OvertimeAttackTaunts = [ "É hora de reorganizar.",
                        "Temos gente para demitir."]

#ElevatorDestination Names
ElevatorBossBotBoss = "Batalha do C.E.O."
ElevatorBossBotCourse = "Campo de Golfe Cog"
ElevatorBossBotCourse0 = "O Front Three (Três da Frente)"
ElevatorBossBotCourse1 = "O Middle Six (Seis do Meio)"
ElevatorBossBotCourse2 = "O Back Nine (Nove dos Fundos)"
ElevatorCashBotBoss = "Batalha do C.F.O"
ElevatorCashBotMint0 = "Coin Mint (a Mina de Moedas)"
ElevatorCashBotMint1 = "Dollar Mint (a Mina de Dinheiro)"
ElevatorCashBotMint2 = "Bullion Mint (a Mina de Ouro)"
ElevatorSellBotBoss = "Batalha do Sellbot"
ElevatorSellBotFactory0 = "Entrada Principal"
ElevatorSellBotFactory1 = "Entrada dos Fundos"
ElevatorLawBotBoss = "Batalha do Juiz-Chefe"
ElevatorLawBotCourse0 = "Escritório A"
ElevatorLawBotCourse1 = "Escritório B"
ElevatorLawBotCourse2 = "Escritório C"
ElevatorLawBotCourse3 = "Escritório D"

# CatalogNameTagItem.py
DaysToGo = "Espere\n%s Dias"

# DistributedIceGame.py
IceGameTitle = "Escorregador de Gelo"
IceGameInstructions = "Chegue o mais perto do centro ao final da segunda rodada. Use as teclas de seta para mudar a direção e a força. Aperte Ctrl para lançar seu Toon. Acerte os barris para ganhar mais pontos, e evite a dinamite!"
IceGameInstructionsNoTnt = "Chegue o mais perto do centro ao final da segunda rodada. Use as teclas de seta para mudar a direção e a força. Aperte Ctrl para lançar seu Toon. Acerte os barris para ganhar mais pontos."
IceGameWaitingForPlayersToFinishMove = "Esperando outros jogadores..."
IceGameWaitingForAISync = "Esperando outros jogadores..."
IceGameInfo= "Partida %(curMatch)d/%(numMatch)d, Rodada %(curRound)d/%(numRound)d"
IceGameControlKeyWarning="Lembre-se de apertar a tecla Ctrl!"


#DistributedPicnicTable.py
PicnicTableJoinButton = "Entrar"
PicnicTableObserveButton = "Observar"
PicnicTableCancelButton = "Cancelar"
PicnicTableTutorial = "Como Jogar"
PicnicTableMenuTutorial = "Qual jogo você quer aprender?"
PicnicTableMenuSelect = "Qual jogo você quer jogar?"

#DistributedChineseCheckers.py
ChineseCheckersGetUpButton = "Levantar-se"
ChineseCheckersStartButton = "Iniciar Jogo"
ChineseCheckersQuitButton = "Sair do Jogo"
ChineseCheckersIts = "É a "

ChineseCheckersYourTurn = "Sua Vez"
ChineseCheckersGreenTurn = "Vez do Verde"
ChineseCheckersYellowTurn = "Vez do Amarelo"
ChineseCheckersPurpleTurn = "Vez do Roxo"
ChineseCheckersBlueTurn = "Vez do Azul"
ChineseCheckersPinkTurn = "Vez do Rosa"
ChineseCheckersRedTurn = "Vez do Vermelho"

ChineseCheckersColorG = "Você é o Verde"
ChineseCheckersColorY = "Você é o Amarelo"
ChineseCheckersColorP = "Você é o Roxo"
ChineseCheckersColorB = "Você é o Azul"
ChineseCheckersColorPink = "Você é o Rosa"
ChineseCheckersColorR = "Você é o Vermelho"
ChineseCheckersColorO = "Você está Observando"

ChineseCheckersYouWon = "Você acaba de ganhar uma partida de Xadrez Chinês!"
ChineseCheckers = "Xadrez Chinês."
ChineseCheckersGameOf = " acaba de ganhar uma partida de "

#GameTutorials.py
ChineseTutorialTitle1 = "Objetivo"
ChineseTutorialTitle2 = "Como Jogar"
ChineseTutorialPrev = "Página Anterior"
ChineseTutorialNext = "Próxima Página"
ChineseTutorialDone = "Pronto"
ChinesePage1 = "O objetivo do Xadrez Chinês é ser o primeiro jogador a mover todas as suas peças do triângulo de baixo do tabuleiro até o triângulo do outro lado. O primeiro jogador a conseguir isso vence!"
ChinesePage2 = "Os jogadores se alternam movendo qualquer pedra de sua própria cor.  Uma pedra pode se mover para um buraco ao lado, ou pode saltar por outras pedras. Os saltos devem passar por um mármore e cair em um buraco livre. É possível combinar saltos para andar mais longe!"

CheckersPage1 = "O objetivo das Damas é deixar o oponente sem poder fazer jogadas. Para isso, você pode capturar todas as suas peças, ou bloqueá-las para que não ele não possa movê-las."
CheckersPage2 = "Os jogadores se alternam movendo qualquer pedra de sua própria cor. Uma peça pode se mover para um quadrado diagonal à frente. Uma peça só pode se mover para um quadrado que não esteja ocupado por outra peça. As damas seguem as mesmas regras, mas podem se mover para trás."
CheckersPage3 = "Para capturar uma peça do oponente, você deve saltar sobre ela diagonalmente para o quadrado vazio depois dela. Se você puder fazer alguma captura em sua vez, terá de fazê-la. Você pode combinar capturas, desde que seja com a mesma peça." 
CheckersPage4 = "Uma peça se torna dama quando chegar à última linha do tabuleiro. Uma peça que acaba de se tornar dama não pode saltar de novo até o próximo turno. Além disso, damas podem se mover para todas as direções e podem mudar de direção ao saltar."



#DistributedCheckers.py
CheckersGetUpButton = "Levantar-se"
CheckersStartButton = "Iniciar Jogo"
CheckersQuitButton = "Sair do Jogo"
CheckersIts = "É a "
CheckersYourTurn = "Sua Vez"
CheckersWhiteTurn = "Vez do Branco"
CheckersBlackTurn = "Vez do Preto"
CheckersColorWhite = "Você é o Branco"
CheckersColorBlack = "Você é o Preto"
CheckersObserver = "Você está Observando"
RegularCheckers = "Damas."
RegularCheckersGameOf = " acaba de ganhar uma partida de "
RegularCheckersYouWon = "Você acaba de ganhar uma partida de Damas!"

MailNotifyNewItems = "Chegou correio para você!"
MailNewMailButton = "Correio"
MailSimpleMail = "Bilhete"
MailFromTag = "Bilhete de: %s"

# MailboxScreen.py
InviteInvitation = "o convite"
InviteAcceptInvalidError = "O convite não é mais válido."
InviteAcceptPartyInvalid = "Sua festa foi cancelada."
InviteAcceptAllOk = "O anfitrião recebeu sua resposta."
InviteRejectAllOk = "O anfitrião recebeu sua recusa do convite."


# Note Months is 1 based, to correspond to datetime
Months = {
 1: "JANEIRO",
 2: "FEVEREIRO",
 3: "MARÇO",
 4: "ABRIL",
 5: "MAIO",
 6: "JUNHO",
 7: "JULHO",
 8: "AGOSTO",
 9: "SETEMBRO",
10: "OUTUBRO",
11: "NOVEMBRO",
12: "DEZEMBRO"
}

# Note 0 for Monday to match datetime
DayNames = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo")
DayNamesAbbrev = ("SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM")

# numbers must match holiday ids in ToontownGlobals
HolidayNamesInCalendar = {
    1: ("Fogos de Artifício de Verão", "Comemore o Verão com um espetáculo de fogos de artifício a cada hora em cada pátio!"),
    2: ("Fogos de Artifício de Ano Novo", "Feliz Ano Novo! Curta um espetáculo de fogos de artifício a cada hora em cada pátio!"),
    3: ("Invasão Sanguessuga", "Feliz Halloween! Impeça que os Cogs Sanguessugas invadam Toontown!"),
    4: ("Decoração de Feriados de Inverno", "Comemore os Feriados de Inverno com árvores e postes de iluminação Toontásticos!"),
    5: ("Invasão Skelecog", "Impeça que os Skelecogs invadam Toontown!"),
    6: ("Invasão Dr. Celebridade ", "Impeça que os Cogs  do Dr. Celebridade invadam Toontown!"),
    7: ("Bingo de Peixe", "Quarta-feira do Bingo de Peixe! Todos no lago trabalhando juntos para completar a cartela antes de o tempo esgotar."),
    8: ("Eleição de Espécie de Toon", "Vote na nova espécie de Toon! Será uma Cabra? Será um Porco?"),
    9: ("Dia do Gato Preto", "Feliz Halloween! Crie um Toon Gato Preto Toontástico – Só Hoje!"),
   13: ("Doces ou Travessuras", "Feliz Halloween! Vá atrás das guloseimas por toda Toontown para ganhar uma linda cabeça de abóbora de prêmio!"),
   14: ("Grande Prêmio", "Segunda-feira do Grande Prêmio no autódromo do Pateta! Para vencer, conquiste o maior número de pontos em três corridas consecutivas!"),
   16: ("Fim de Semana do Grande Prêmio", "Quem jogar gratuitamente ou pagando compete nas corridas do Autódromo do Pateta!"),
   17: ("Trilhas do Bondinho", "Quinta-feira das Trilhas do Bondinho! Embarque em qualquer Bondinho para jogar com dois ou mais Toons."),
   19: ("Sábados Engraçados", "Os sábados são engraçados com o Bingo de Peixe, Grande Prêmio e  Trilhas do Bondinho o dia todo!"),
   24: ("Idos de Março", "Cuidado com os Idos de Março! Impeça que os Cogs Golpe Sujo invadam Toontown!"),
   26: ("Decoração de Halloween", "Comemore o Halloween deixando as árvores e  postes de iluminação de Toontown assustadores!"),
   28: ("Invasão de Inverno", "Os sellbots estão à solta espalhando suas táticas de vendas frias!"),
   33: ("Surpresa de Robô Vendedor 1", "Surpresa de Robô Vendedor! Impeça que os Cogs Reis da Incerta invadam Toontown!"),
   34: ("Surpresa de Robô Vendedor 2", "Surpresa de Robô Vendedor! Impeça que os Cogs Sabe-com-quem-está-falando invadam Toontown!"),
   35: ("Surpresa de Robô Vendedor 3", "Surpresa de Robô Vendedor! Impeça que os Cogs Amigos da Onça invadam Toontown!"),
   36: ("Surpresa de Robô Vendedor 4", "Surpresa de Robô Vendedor! Impeça que os Cogs Agitadores invadam Toontown!"),
   37: ("Enigma de Robô Mercenário 1", "Enigma de Robô Mercenário. Impeça que os Cogs Farsantes invadam Toontown!"),
   38: ("Enigma de Robô Mercenário 2", "Enigma de Robô Mercenário. Impeça que os Cogs Mão de Vaca invadam Toontown!"),
   39: ("Enigma de Robô Mercenário 3", "Enigma de Robô Mercenário. Impeça que os Cogs Conta-moedinhas invadam Toontown!"),
   40: ("Enigma de Robô Mercenário 4", "Enigma de Robô Mercenário. Impeça que os Cogs Destruidores de Números invadam Toontown!"),
   41: ("A Estratégia do Robô da Lei 1", "A Estratégia do Robô da Lei. Impeça que os Cogs Comensais invadam Toontown!"),
   42: ("A Estratégia do Robô da Lei 2", "A Estratégia do Robô da Lei. Impeça que os Cogs Duplo Sentido invadam Toontown!"),
   43: ("A Estratégia do Robô da Lei 3", "A Estratégia do Robô da Lei. Impeça que os Cogs Perseguidores de Ambulância invadam Toontown!"),
   44: ("A Estratégia do Robô da Lei 4", "A Estratégia do Robô da Lei. Impeça que os Cogs Golpe Sujo invadam Toontown!"),
   45: ("O Problema Com Robôs Chefes 1", "O Problema Com Robôs Chefes. Impeça que os Cogs Puxa-sacos invadam Toontown!"),
   46: ("O Problema Com Robôs Chefes 2", "O Problema Com Robôs Chefes. Impeça que os Cogs Ratos de Escritório invadam Toontown!"),
   47: ("O Problema Com Robôs Chefes 3", "O Problema Com Robôs Chefes. Impeça que os Cogs Microempresários invadam Toontown!"),
   48: ("O Problema Com Robôs Chefes 4", "O Problema Com Robôs Chefes. Impeça que os Cogs Facões invadam Toontown!"),
   49: ("Dia da Balinha", "Comemore o Dia da Balinha ganhando Balinhas em dobro nas festas!"),
   53: ("Invasão Reis da Incerta", "Impeça que os Cogs  Reis da Incerta invadam Toontown!"),
   54: ("Invasão Conta-moedinha", "Impeça que os Cogs  Conta-moedinhas invadam Toontown!"),
   55: ("Invasão Duplo Sentido", "Impeça que os Cogs  Duplo Sentido invadam Toontown!"),
   56: ("Invasão de Facão", "Impeça que os Cogs Facões invadam Toontown!"),

    }

UnknownHoliday = "Feriado Desconhecido %d"
HolidayFormat = "%m/%d "

# parties/ToontownTimeManager.py
TimeZone = "Brazil/West"
