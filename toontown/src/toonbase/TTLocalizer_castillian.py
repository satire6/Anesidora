import string
import time
from toontown.toonbase.TTLocalizer_castillian_Property import *

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
NametagFontNames = ('Miembro',      #0 *
                'Tembloroso',      #1 *
                'Agitado',   #2 *
                'Elegante',        #3 *
                'Absurdo',    #4 *
                'Estrafalario',          #5 *
                'Práctico',        #6 *
                'Náutico',         #7 *
                'Enigmático',        #8 *
                'Espeluznante',        #9 *
                'Acción',          #10 *
                'Poético',            #11 *
                'Paseo marítimo',       #12 *
                'Oeste',    #13 *
                )

NametagLabel = " Etiqueta del nombre"

UnpaidNameTag = "Básica"

BuildingNametagFont = 'phase_3/models/fonts/MickeyFont'
BuildingNametagShadow = None

# Product prefix
ProductPrefix = 'TT'

# common names
Mickey = "Mickey"
VampireMickey = "VampiroMickey"
Minnie = "Minnie"
Donald = "Donald"
Daisy  = "Daisy"
Goofy  = "Goofy"
Pluto  = "Pluto"
Flippy = "Flipi"
Chip   = "Chip"
Dale   = "Dale"

# common locations
lTheBrrrgh = 'Frescolandia'
lDaisyGardens = 'Jardines de Daisy'
lDonaldsDock = "Puerto de Donald"
lDonaldsDreamland = "Sueñolandia de Donald"
lMinniesMelodyland = "Melodilandia de Minnie"
lToontownCentral = 'Centro de Toontown'
lToonHQ = 'Cuartel general'
lSellbotHQ = 'Cuartel general vendebot'
lGoofySpeedway = "Estadio de Goofy"
lOutdoorZone = "Acres de bellota de Chip y Dale"
lGolfZone = "Minigolf de Chip y Dale"
lPartyHood = "Dibuparque de la fiesta"
lToonHQfull = 'Cuartel general'

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("a la", "", "Calle del Tutorial"), # Tutorial
    1000  : ("al",   "", "Dibuparque"),
    1100  : ("al",   "", "Paseo del Percebe"),
    1200  : ("a la", "", "Avenida de las Algas"),
    1300  : ("a la", "", "Calle del Faro"),
    2000  : ("al",   "", "Dibuparque"),
    2100  : ("a la", "", "Calle Boba"),
    2200  : ("a la", "", "Calle Locuela"),
    2300  : ("a la", "", "Avenida del Chiste"),
    3000  : ("al",   "", "Dibuparque"),
    3100  : ("a la", "", "Calle de la Morsa"),
    3200  : ("a la", "", "Travesía del Trineo"),
    3300  : ("al",     "en el",     "Punto Polar"),
    4000  : ("al",   "", "Dibuparque"),
    4100  : ("a la", "", "Travesía de la Melodía"),
    4200  : ("al",   "", "Boulevard del Barítono"),
    4300  : ("a la", "", "Calle del Tenor"),
    5000  : ("al",   "", "Dibuparque"),
    5100  : ("a la", "", "Calle del Chopo"),
    5200  : ("a la", "", "Calle Arce"),
    5300  : ("a la", "", "Calle de Los Robles"),         # translate
    9000  : ("al",   "", "Dibuparque"),
    9100  : ("a la", "", "Avenida de la Nana"),
    9200  : ("al",     "en el",     "Centro Pijama"),
    10000 : ("al",   "", "Cuartel general jefebot"),
    10100 : ("al",   "", "vestíbulo del cuartel general jefebot"),
    10200 : ("a la", "en la", "Casa de Mickey Mouse"),
    10500 : ("al", "en el", "El Tres Frontal"),
    10600 : ("al", "en el", "El Seis Central"),
    10700 : ("al", "en el", "El Nueve Trasero"),
    11000 : ("al",   "", "patio del cuartel general vendebot"),
    11100 : ("al",   "", "vestíbulo del cuartel general vendebot"),
    11200 : ("a la", "", "fábrica vendebot"),
    11500 : ("a la", "", "fábrica vendebot"),
    12000 : ("al",   "", "cuartel general chequebot"),
    12100 : ("al",   "", "vestíbulo del cuartel general chequebot"),
    12500 : ("a la", "en la", "Fabrica de moneditas Chequebot"),
    12600 : ("a la", "en la", "Fabrica de dólares Chequebot"),
    12700 : ("a la", "en la", "Fabrica de lingotes Chequebot"),
    13000 : ("al",   "", "cuartel general abogabot"),
    13100 : ("al",   "", "vestíbulo del cuartel general abogabot"),
    13200 : ("al", "en el", "vestíbulo de la oficina del fiscal del distrito"),
    13300 : ("a la", "en la", "Oficina del abogabot A"),
    13400 : ("a la", "en la", "Oficina del abogabot B"),
    13500 : ("a la", "en la", "Oficina del abogabot C"),
    13600 : ("a la", "en la", "Oficina del abogabot D"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("a",    "", lDonaldsDock)
ToontownCentral   = ("al",   "", lToontownCentral)
TheBrrrgh         = ("a",    "", lTheBrrrgh)
MinniesMelodyland = ("a",    "", lMinniesMelodyland)
DaisyGardens      = ("a",    "", "los %s" % lDaisyGardens)
OutdoorZone       = ("a los",     "en los", lOutdoorZone)
FunnyFarm         = ("a la", "", "Granja Jolgorio")
GoofySpeedway     = ("al",   "", "Estadio de Goofy")
DonaldsDreamland  = ("a",    "", lDonaldsDreamland)
BossbotHQ         = ("al",   "", lToonHQ+" jefebot")
SellbotHQ         = ("al",   "", lToonHQ+" vendebot")
CashbotHQ         = ("al",   "", lToonHQ+" chequebot")
LawbotHQ          = ("al",   "", lToonHQ+" abogabot")
Tutorial          = ("al",   "", "Dibututorial")
MyEstate          = ("a",    "", "Tu hacienda")
WelcomeValley     = ("a",    "", "Valle Bienvenido")
GolfZone          = ("al", "en el", lGolfZone)
PartyHood         = ("al", "en el", lPartyHood)

Factory = 'Fábrica'
Headquarters = 'Cuartel general'
SellbotFrontEntrance = 'Entrada principal'
SellbotSideEntrance = 'Entrada de servicio'
Office = 'Oficina'

FactoryNames = {
    0 : 'Maqueta de la fábrica',
    11500 : 'Fábrica de bots vendebot',
    13300 : 'Oficina de bots abogabots', #remove me JML
    }

FactoryTypeLeg = 'Pierna'
FactoryTypeArm = 'Brazo'
FactoryTypeTorso = 'Torso'

MintFloorTitle = 'Planta %s'

# common strings
lCancel = 'Cancelar'
lClose = 'Cerrar'
lOK = 'Ok'
lNext = 'Siguiente'
lQuit = 'Salir'
lYes = 'Sí'
lNo = 'No'
lBack = 'Atrás'
lHQ = ""

sleep_auto_reply = "%s está durmiendo"

lHQOfficerF = 'Funcionaria del cuartel general'
lHQOfficerM = 'Funcionario del cuartel general'

MickeyMouse = "Mickey Mouse"

AIStartDefaultDistrict = "Villaboba"

Cog  = "Bot"
Cogs = "Bots"
ACog = "un bot"
TheCogs = "Los bots"
ASkeleton = "un esquelebot"
Skeleton = "esquelebot"
SkeletonP = "esquelebots"
Av2Cog = "un bot versión 2.0"
v2Cog = "Bot versión 2.0"
v2CogP = "Bots versión 2.0"
ASkeleton = "un esquelebot"
Foreman = "capataz de la fábrica"
ForemanP = "capataces"
AForeman = "un capataz"
CogVP = Cog + " VIP"
CogVPs = "bots VIPS"
ACogVP = ACog + " un VIP"
Supervisor = "Supervisor de la fabrica"
SupervisorP = "Supervisores de la fabrica"
ASupervisor = "un supervisor de la fabrica"
CogCFO = Cog + " Director financiero"
CogCFOs = "Director financiero bot"
ACogCFO = ACog + " Director financiero"

# Quests.py
TheFish = "los peces"
AFish = "un pez"
Level = "nivel"
QuestsCompleteString = "Completada"
QuestsNotChosenString = "No está elegida"
Period = "."

Laff = "Risa"

QuestInLocationString = " %(inPhrase)s %(location)s"

# _avName_ gets replaced with the avatar (player's) name
# _toNpcName_ gets replaced with the npc's name we are being sent to
# _where_ gets replaced with a description of where to find the npc, with a leading \a
QuestsDefaultGreeting = ("¡Hola, _avName_!",
                         "¡Buenas, _avName_!",
                         "¿Qué tal, _avName_?",
                         "¿Qué tal todo, _avName_?",
                         "¿Cómo te va, _avName_?",
                         "¿Qué hay, _avName_?",
                         "¿Cómo estás, _avName_?",
                         "Saludos _avName_!",
                         )
QuestsDefaultIncomplete = ("¿Qué tal va la tarea, _avName_?",
                           "¡Parece que todavía te queda trabajo por hacer con esa tarea!",
                           "¡Sigue trabajando así, _avName_!",
                           "Intenta terminar la tarea.  ¡Sé que puedes hacerlo!",
                           "¡Sigue intentando terminar la tarea, contamos contigo!",
                           "¡Sigue trabajando en tu dibutarea!",
                           )
QuestsDefaultIncompleteProgress = ("Viniste al lugar adecuado, pero antes tienes que terminar la dibutarea.",
                                   "Cuando hayas terminado con la dibutarea, vuelve aquí.",
                                   "Vuelve cuando hayas terminado la dibutarea.",
                                   )
QuestsDefaultIncompleteWrongNPC = ("Buen trabajo con esa dibutarea. Deberías ir a ver a _toNpcName_._where_",
                                   "Parece que estás a punto de acabar tu dibutarea. Ve a ver a _toNpcName_._where_.",
                                   "Ve a ver a _toNpcName_ para terminar la dibutarea._where_",
                                   )
QuestsDefaultComplete = ("¡Buen trabajo! Aquí está tu recompensa...",
                         "¡Buen trabajo, _avName_! Toma, tu recompensa...",
                         "¡Muy bien, _avName_!  Aquí está tu recompensa...",
                         )
QuestsDefaultLeaving = ("¡Ciao!",
                        "¡Adiós!",
                        "Nos vemos, _avName_.",
                        "¡Hasta la vista, _avName_!",
                        "¡Buena suerte!",
                        "¡Diviértete en Toontown!",
                        "¡Hasta luego!",
                        )
QuestsDefaultReject = ("Hola.",
                       "¿En qué puedo ayudarte?",
                       "¿Cómo estás?",
                       "Muy buenas.",
                       "Ahora estoy un poco ocupado, _avName_.",
                       "¿Sí?",
                       "¿Qué hay, _avName_?",
                       "¿Cómo te va, _avName_?",
                       "¡Eh, _avName_! ¿Cómo va todo?",
                       # Game Hints
                       "¿Sabías que puedes abrir el dibucuaderno pulsando la tecla F8?",
                       "¡Puedes usar el mapa para teletransportarte de vuelta al dibuparque!",
                       "Para hacerte amigo de otros jugadores, haz clic en ellos.",
                       "Para averiguar más sobre un " + Cog + ", haz clic en él.",
                       "Reúne tesoros del dibuparque para llenar el risómetro.",
                       "¡Los edificios" + Cog + " son lugares peligrosos! ¡No entres en ellos solo!",
                       "Cuando pierdas un combate, los " + Cogs + " se llevarán todas tus bromas.",
                       "¡Para conseguir más bromas, juega a los juegos del tranvía!",
                       "Para conseguir más puntos de risa, completa las dibutareas.",
                       "Todas las dibutareas proporcionan recompensas.",
                       "Algunas recompensas sirven para poder llevar más bromas.",
                       "Si ganas un combate, consigues créditos de dibutareas por cada " + Cog + " derrotado.",
                       "Si recuperas un edificio " + Cog + " vuelve a entrar para ver el agradecimiento especial de su propietario.",
                       "Para mirar hacia arriba, mantén pulsada la tecla Re Pág.",
                       "Si pulsas la tecla Tab, podrás contemplar diferentes vistas de los alrededores.",
                       "Para mostrar lo que piensas a tus amigos secretos, escribe un '.' antes del pensamiento.",
                       "Cuando aturdas a un " + Cog + ", le será más difícil esquivar los objetos que caen.",
                       "Cada tipo de edificio " + Cog + " tiene un aspecto distinto.",
                       "Cuando derrotes a los " + Cogs + " de los pisos altos de un edificio, obtendrás habilidades superiores.",
                       )
QuestsDefaultTierNotDone = ("¡Hola, _avName_! Antes de acceder a una nueva dibutarea debes terminar la actual.",
                            "¡Muy buenas! Tienes que terminar las dibutareas actuales para acceder a una nueva.",
                            "¡Buenas, _avName_! Para poderte asignar una nueva dibutarea, tienes que terminar las dibutareas actuales.",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("Dicen que _toNpcName_ te anda buscando._where_",
                                 "Visita a _toNpcName_ cuando tengas la ocasión._where_",
                                 "Ve a ver a _toNpcName_ cuando pases por ahí._where_",
                                 "Si tienes la ocasión, pásate a saludar a _toNpcName_._where_",
                                 "_toNpcName_ te asignará tu próxima dibutarea._where_",
                                 )
# Quest dialog
QuestsLocationArticle = ""
def getLocalNum(num):
    return str(num)
QuestsItemNameAndNum = "%(num)s %(name)s"

QuestsCogQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogQuestHeadline = "SE BUSCA"
QuestsCogQuestSCStringS = "Tengo que derrotar a %(cogName)s%(cogLoc)s."
QuestsCogQuestSCStringP = "Tengo que derrotar algunos %(cogName)s%(cogLoc)s."
QuestsCogQuestDefeat = "Derrotar a %s"
QuestsCogQuestDefeatDesc = "%(numCogs)s %(cogName)s"

QuestsCogNewNewbieQuestObjective = "Ayuda a los dibus con %d puntos de risas o derrota a algunos %s"
QuestsCogNewNewbieQuestCaption = "Ayuda a un nuevo dibu con %d puntos de risas o menos"
QuestsCogOldNewbieQuestObjective = "Ayuda a un dibu con %(laffPoints)d puntos de risa o menos a derrotar a %(objective)s"
QuestsCogOldNewbieQuestCaption = "Ayuda a un dibu con %d puntos de risa o menos"
QuestsCogNewbieQuestAux = "Derrotar:"
QuestsNewbieQuestHeadline = "Aprendiz"

QuestsCogTrackQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogTrackQuestHeadline = "SE BUSCA"
QuestsCogTrackQuestSCStringS = "Tengo que derrotar un %(cogText)s%(cogLoc)s."
QuestsCogTrackQuestSCStringP = "Tengo que derrotar algunos %(cogText)s%(cogLoc)s."
QuestsCogTrackQuestDefeat = "Derrotar a %s"
QuestsCogTrackDefeatDesc = "%(numCogs)s %(trackName)s"

QuestsCogLevelQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogLevelQuestHeadline = "SE BUSCA"
QuestsCogLevelQuestDefeat = "Derrotar a %s"
QuestsCogLevelQuestDesc = "un " + Cog + " de nivel %(level)s+"
QuestsCogLevelQuestDescC = "%(count)s " + Cogs + " de nivel %(level)s+"
QuestsCogLevelQuestDescI = "algunos " + Cogs + " de nivel %(level)s+"
QuestsCogLevelQuestSCString = "Tengo que derrotar %(objective)s%(location)s."

QuestsBuildingQuestFloorNumbers = ('', 'dos+', 'tres+', 'cuatro+', 'cinco+')
QuestsBuildingQuestBuilding = "Edificio"
QuestsBuildingQuestBuildings = "Edificios"
QuestsBuildingQuestHeadline = "DERROTAR"
QuestsBuildingQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsBuildingQuestString = "Derrotar a %s"
QuestsBuildingQuestSCString = "Tengo que derrotar %(objective)s%(location)s."

QuestsBuildingQuestDesc = "un edificio %(type)s"
QuestsBuildingQuestDescF = "un edificio %(type)s de %(floors)s pisos"
QuestsBuildingQuestDescC = "%(count)s edificios %(type)s"
QuestsBuildingQuestDescCF = "%(count)s edificios %(type)s de %(floors)s pisos"
QuestsBuildingQuestDescI = "algunos edificios %(type)s"
QuestsBuildingQuestDescIF = "algunos edificios %(type)s de %(floors)s pisos"

QuestFactoryQuestFactory = "Fábrica"
QuestsFactoryQuestFactories = "Fábricas"
QuestsFactoryQuestHeadline = "DERROTAR"
QuestsFactoryQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsFactoryQuestString = "Derrotar a %s"
QuestsFactoryQuestSCString = "Tengo que derrotar a %(objective)s%(location)s."

QuestsFactoryQuestDesc = "una fábrica %(type)s"
QuestsFactoryQuestDescC = "%(count)s fábricas %(type)s"
QuestsFactoryQuestDescI = "algunas fábricas %(type)s"

QuestMintQuestMint = "Fabrica de monedas"
QuestsMintQuestMints = "Fabrica de monedas"
QuestsMintQuestHeadline = "DERROTAR"
QuestsMintQuestProgressString = "%(progress)s de %(num)s derrotados"
QuestsMintQuestString = "Derrotar %s"
QuestsMintQuestSCString = "Necesito derrotar %(objective)s%(location)s."

QuestsMintQuestDesc = "moneda bot"
QuestsMintQuestDescC = "%(count)s fabrica de monedas bot"
QuestsMintQuestDescI = "algunas fabrica de monedas bot"

QuestsRescueQuestProgress = "%(progress)s de %(numToons)s rescatados"
QuestsRescueQuestHeadline = "RESCATAR"
QuestsRescueQuestSCStringS = "Tengo que rescatar a un dibu %(toonLoc)s."
QuestsRescueQuestSCStringP = "Tengo que rescatar a algunos dibus %(toonLoc)s."
QuestsRescueQuestRescue = "Rescatar a %s"
QuestsRescueQuestRescueDesc = "%(numToons)s dibus"
QuestsRescueQuestToonS = "un dibu"
QuestsRescueQuestToonP = "dibus"
QuestsRescueQuestAux = "Rescatar a:"

QuestsRescueNewNewbieQuestObjective = "Ayuda a un nuevo dibu a rescatar a %s"
QuestsRescueOldNewbieQuestObjective = "Ayuda a un dibu con %(laffPoints)d puntos de risa o menos a rescatar a %(objective)s"

QuestCogPartQuestCogPart = "Pieza de traje bot"
QuestsCogPartQuestFactories = "Fábricas"
QuestsCogPartQuestHeadline = "RECUPERAR"
QuestsCogPartQuestProgressString = "%(progress)s de %(num)s recuperadas"
QuestsCogPartQuestString = "Recuperar %s"
QuestsCogPartQuestSCString = "Tengo que recuperar %(objective)s%(location)s."
QuestsCogPartQuestAux = "Recuperar:"

QuestsCogPartQuestDesc = "una pieza de traje bot"
QuestsCogPartQuestDescC = "%(count)s piezas de traje bot"
QuestsCogPartQuestDescI = "algunas piezas de traje bot"

QuestsCogPartNewNewbieQuestObjective = 'Ayuda a un nuevo dibu a recuperar %s'
QuestsCogPartOldNewbieQuestObjective = 'Ayuda a un dibu con %(laffPoints)d puntos de risa o menos a conseguir %(objective)s'

QuestsDeliverGagQuestProgress = "%(progress)s de %(numGags)s entregados"
QuestsDeliverGagQuestHeadline = "ENTREGAR"
QuestsDeliverGagQuestToSCStringS = "Tengo que entregar %(gagName)s."
QuestsDeliverGagQuestToSCStringP = "Tengo que entregar algunos %(gagName)s."
QuestsDeliverGagQuestSCString = "Tengo que hacer una entrega."
QuestsDeliverGagQuestString = "Entregar %s"
QuestsDeliverGagQuestStringLong = "Entregar %s a _toNpcName_."
QuestsDeliverGagQuestInstructions = "Tú puedes comprar esta broma en la Tienda de Bromas una vez que tengas acceso a la broma."

QuestsDeliverItemQuestProgress = ""
QuestsDeliverItemQuestHeadline = "ENTREGAR"
QuestsDeliverItemQuestSCString = "Tengo que entregar %(article)s%(itemName)s."
QuestsDeliverItemQuestString = "Entregar %s"
QuestsDeliverItemQuestStringLong = "Entregar %s a _toNpcName_."

QuestsVisitQuestProgress = ""
QuestsVisitQuestHeadline = "VISITAR"
QuestsVisitQuestStringShort = "Visitar"
QuestsVisitQuestStringLong = "Ir a ver a _toNpcName_"
QuestsVisitQuestSeeSCString = "Tengo que ver a %s."

QuestsRecoverItemQuestProgress = "%(progress)s de %(numItems)s recuperados"
QuestsRecoverItemQuestHeadline = "RECUPERAR"
QuestsRecoverItemQuestSeeHQSCString = "Tengo que ver a un funcionario del cuartel general."
QuestsRecoverItemQuestReturnToHQSCString = "Tengo que devolver %s a un funcionario del cuartel general."
QuestsRecoverItemQuestReturnToSCString = "Tengo que devolver %(item)s a %(npcName)s."
QuestsRecoverItemQuestGoToHQSCString = "Tengo que ir al cuartel general."
QuestsRecoverItemQuestGoToPlaygroundSCString = "Tengo que ir al dibuparque %s."
QuestsRecoverItemQuestGoToStreetSCString = "Tengo que ir %(to)s %(street)s en %(hood)s."
QuestsRecoverItemQuestVisitBuildingSCString = "Tengo que ir a %s %s."
QuestsRecoverItemQuestWhereIsBuildingSCString = "¿Dónde está %s %s?"
QuestsRecoverItemQuestRecoverFromSCString = "Tengo que recuperar: %(item)s de %(holder)s%(loc)s."
QuestsRecoverItemQuestString = "Recuperar %(item)s de %(holder)s"
QuestsRecoverItemQuestHolderString = "%(level)s %(holder)d+ %(cogs)s"

QuestsTrackChoiceQuestHeadline = "ELIGE"
QuestsTrackChoiceQuestSCString = "Tengo que escoger entre %(trackA)s y %(trackB)s."
QuestsTrackChoiceQuestMaybeSCString = "Quizá deba escoger %s."
QuestsTrackChoiceQuestString = "Elige entre %(trackA)s y %(trackB)s"

QuestsFriendQuestHeadline = "AMIGO"
QuestsFriendQuestSCString = "Necesito hacer amigos."
QuestsFriendQuestString = "Hacer un amigo"

QuestsMailboxQuestHeadline = "CORREO"
QuestsMailboxQuestSCString = "Necesito leer mi correo."
QuestsMailboxQuestString = "Lee tu correo"

QuestsPhoneQuestHeadline = "CLARABEL"
QuestsPhoneQuestSCString = "Necesito llamar a Clarabel."
QuestsPhoneQuestString = "Llamar a Clarabel"

QuestsFriendNewbieQuestString = "Haz %d amigos con %d puntos de risa o menos"
QuestsFriendNewbieQuestProgress = "%(progress)s de %(numFriends)s hechos"
QuestsFriendNewbieQuestObjective = "Hazte amigo de %d dibus que tengan %d puntos de risa o menos"

QuestsTrolleyQuestHeadline = "TRANVÍA"
QuestsTrolleyQuestSCString = "Tengo que subir al tranvía."
QuestsTrolleyQuestString = "Subir al tranvía."
QuestsTrolleyQuestStringShort = "¿Quieres subir al tranvía?"

QuestsMinigameNewbieQuestString = "%d Minijuegos"
QuestsMinigameNewbieQuestProgress = "%(progress)s de %(numMinigames)s jugados"
QuestsMinigameNewbieQuestObjective = "Juega %d minijuegos con dibus que tienen %d puntos en el risómetro o menos."
QuestsMinigameNewbieQuestSCString = "Necesito jugar en los minijuegos con dibus nuevos."
QuestsMinigameNewbieQuestCaption = "Ayuda a un dibu Nuevo con %d puntos en el risómetro o menos."
QuestsMinigameNewbieQuestAux = "Juega:"

QuestsMaxHpReward = "Tu risómetro aumentó en %s."
QuestsMaxHpRewardPoster = "Recompensa: %s punto(s) de aumento en el risómetro"

QuestsMoneyRewardSingular = "Conseguiste 1 golosina."
QuestsMoneyRewardPlural = "Conseguiste %s golosinas."
QuestsMoneyRewardPosterSingular = "Recompensa: 1 golosina"
QuestsMoneyRewardPosterPlural = "Recompensa: %s golosinas"

QuestsMaxMoneyRewardSingular = "Ahora puedes llevarte 1 golosina."
QuestsMaxMoneyRewardPlural = "Ahora puedes llevarte %s golosinas."
QuestsMaxMoneyRewardPosterSingular = "Recompensa: 1 golosina"
QuestsMaxMoneyRewardPosterPlural = "Recompensa: %s golosinas"

QuestsMaxGagCarryReward = "Consigues un %(name)s. Ahora puedes llevarte %(num)s bromas."
QuestsMaxGagCarryRewardPoster = "Recompensa: %(name)s (%(num)s)"

QuestsMaxQuestCarryReward = "Ahora puedes tener %s dibutareas."
QuestsMaxQuestCarryRewardPoster = "Recompensa: %s dibutareas"

QuestsTeleportReward = "Ahora puedes teletransportarte a %s."
QuestsTeleportRewardPoster = "Recompensa: Acceso por teletransporte a %s"

QuestsTrackTrainingReward = "Ahora puedes entrenar las bromas de \"%s\"."
QuestsTrackTrainingRewardPoster = "Recompensa: Entrenamiento de bromas"

QuestsTrackProgressReward = "Ahora tienes el fotograma %(frameNum)s de la animación del circuito %(trackName)s."
QuestsTrackProgressRewardPoster = "Recompensa: Fotograma %(frameNum)s de la animación de circuito \"%(trackName)s\""

QuestsTrackCompleteReward = "Ahora puedes llevarte y usar las bromas de \"%s\"."
QuestsTrackCompleteRewardPoster = "Recompensa: Entrenamiento de circuito %s final"

QuestsClothingTicketReward = "Puedes cambiarte de ropa"
QuestsClothingTicketRewardPoster = "Recompensa: boleto de ropa"

QuestsCheesyEffectRewardPoster = "Recompensa: %s"

QuestsCogSuitPartReward = "Ahora tienes una pieza %(part)s del traje de bot de %(cogTrack)s."
QuestsCogSuitPartRewardPoster = "Recompensa: Pieza %(cogTrack)s %(part)s"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "en este parque"
QuestsStreetLocationThisStreet = "en esta calle"
QuestsStreetLocationNamedPlayground = "en el parque de %s"
QuestsStreetLocationNamedStreet = "en %(toStreetName)s de %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "El edificio de %s se llama"
QuestsLocationBuildingVerb = "el cual está "
QuestsLocationParagraph = "\a%(building)s \"%(buildingName)s\"...\a...%(buildingVerb)s %(street)s."
QuestsGenericFinishSCString = "Necesito terminar la dibutarea."

# MaxGagCarryReward names
QuestsMediumPouch = "Bolsita mediana"
QuestsLargePouch = "Bolsita grande"
QuestsSmallBag = "Bolsa pequeña"
QuestsMediumBag = "Bolsa mediana"
QuestsLargeBag = "Bolsa grande"
QuestsSmallBackpack = "Mochila pequeña"
QuestsMediumBackpack = "Mochila mediana"
QuestsLargeBackpack = "Mochila grande"
QuestsItemDict = {
    1 : ["Gafas", "Gafas", "unas "],
    2 : ["Llave", "Llaves", "una "],
    3 : ["Pizarra", "Pizarras", "una "],
    4 : ["Libro", "Libros", "un "],
    5 : ["Chocolate", "Chocolates", "un "],
    6 : ["Tiza", "Tizas", "una "],
    7 : ["Receta", "Recetas", "una "],
    8 : ["Nota", "Notas", "una "],
    9 : ["Calculadora", "Calculadoras", "una "],
    10 : ["Neumático de auto de payasos", "Neumáticos de auto de payasos", "un "],
    11 : ["Bomba de aire", "Bombas de aire", "una "],
    12 : ["Tinta de pulpo", "Tinta de pulpo", "un poco de "],
    13 : ["Paquete", "Paquetes", "un "],
    14 : ["Recibo de pez de acuario", "Recibos de pez de acuario", "un "],
    15 : ["Pez dorado", "Peces dorados", "un "],
    16 : ["Aceite", "Aceite", "un poco de "],
    17 : ["Grasa", "Grasas", "un poco de "],
    18 : ["Agua", "Aguas", "un poco de "],
    19 : ["Informe de equipo", "Informes de equipo", "un "],
    20 : ["Borrador de pizarra ", "Borrador de pizarra", "un "],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    110 : ["TIP Clothing Ticket", "Clothing Tickets", "a "],
    1000 : ["Boleto de ropa", "Boletos de ropa", "un "],

    # Donald's Dock quest items
    2001 : ["Tubo interno", "Tubos internos", "un "],
    2002 : ["Prescripción de monóculo", "Prescripciones de monóculo", "una "],
    2003 : ["Montura de monóculo", "Monturas de monóculo", "una "],
    2004 : ["Monóculo", "Monóculos", "un "],
    2005 : ["Peluca blanca grande", "Pelucas blancas grandes", "una "],
    2006 : ["Granel de lastre", "Graneles de lastre", "una "],
    2007 : ["Engranaje de bot", "Engranajes de bot", "un "],
    2008 : ["Carta náutica", "Cartas náuticas", "una "],
    2009 : ["Coraza repugnante", "Corazas repugnantes", "una "],
    2010 : ["Coraza limpia", "Corazas limpias", "una "],
    2011 : ["Resorte de reloj", "Resortes de reloj", "un "],
    2012 : ["Contrapeso", "Contrapesos", "un "],

    # Minnie's Melodyland quest items
    4001 : ["Inventario de Tina", "Inventarios de Tina", ""],
    4002 : ["Inventario de Uki", "Inventarios de Uki", ""],
    4003 : ["Formulario de inventario", "Formularios de inventario", "un "],
    4004 : ["Inventario de Bibi", "Inventarios de Bibi", ""],
    4005 : ["Billete de Chopo Chopín", "Billetes de Chopo Chopín", ""],
    4006 : ["Billete de Felisa Felina", "Billetes de Felisa Felina", ""],
    4007 : ["Billete de Barbo", "Billetes de Barbo", ""],
    4008 : ["Castañuela sucia", "Castañuelas sucias", ""],
    4009 : ["Tinta azul de pulpo", "Tinta azul de pulpo", "un poco de "],
    4010 : ["Castañuela transparente", "Castañuelas transparentes", "una "],
    4011 : ["Letra de Leo", "Letras de Leo", ""],

    # Daisy's Gardens quest items
    5001 : ["Corbata de seda", "Corbatas de seda", "una "],
    5002 : ["Traje mil rayas", "Trajes mil rayas", "un "],
    5003 : ["Tijeras", "Tijeras", "unas "],
    5004 : ["Postal", "Postales", "una "],
    5005 : ["Pluma", "Plumas", "una "],
    5006 : ["Tintero", "Tinteros", "un "],
    5007 : ["Libreta", "Libretas", "una "],
    5008 : ["Caja de seguridad", "Cajas de seguridad", "una "],
    5009 : ["Bolsa de alpiste", "Bolsas de alpiste", "una "],
    5010 : ["Rueda dentada", "Ruedas dentadas", "una "],
    5011 : ["Ensalada", "Ensaladas", "una "],
    5012 : ["Llave de los "+lDaisyGardens, "Llaves de los "+lDaisyGardens, "una "],
    5013 : ["Planos del cuartel general vendebot", "Planos del cuartel general vendebot", "unos "],
    5014 : ["Nota del cuartel general vendebot", "Notas del cuartel general vendebot", "una "],
    5015 : ["Nota del cuartel general vendebot", "Notas del cuartel general vendebot", "una "],
    5016 : ["Nota del cuartel general vendebot", "Notas del cuartel general vendebot", "una "],
    5017 : ["Nota del cuartel general vendebot", "Notas del cuartel general vendebot", "una "],

    # The Brrrgh quests
    3001 : ["Balón de fútbol", "Balones de fútbol", "un "],
    3002 : ["Tobogán", "Toboganes", "un "],
    3003 : ["Cubito de hielo", "Cubitos de hielo", "un "],
    3004 : ["Carta de amor", "Cartas de amor", "una "],
    3005 : ["Dibuperrito caliente", "Dibuperritos calientes", "un "],
    3006 : ["Anillo de compromiso", "Anillos de compromiso", "un "],
    3007 : ["Aleta de sardina", "Aletas de sardina", "una "],
    3008 : ["Poción calmante", "Pociones calmantes", "una "],
    3009 : ["Diente roto", "Dientes rotos", "un "],
    3010 : ["Diente de oro", "Dientes de oro", "un "],
    3011 : ["Pan de piñones", "Panes de piñones", "un "],
    3012 : ["Queso abultado", "Quesos abultados", "un "],
    3013 : ["Cuchara sencilla", "Cucharas sencillas", "una "],
    3014 : ["Sapo parlanchín", "Sapos parlanchines", "un "],
    3015 : ["Helado de cucurucho", "Helados de cucurucho ", "un "],
    3016 : ["Talco para peluca", "Talco para pelucas", "un poco de "],
    3017 : ["Patito de goma", "Patitos de goma", "un "],
    3018 : ["Dados de goma", "Dados de goma", "unos "],
    3019 : ["Micrófono", "Micrófonos", "un "],
    3020 : ["Teclado electrónico", "Teclados electrónicos", "un "],
    3021 : ["Zapatos con plataforma", "Zapatos con plataforma", "unos "],
    3022 : ["Caviar", "Caviar", "un poco de "],
    3023 : ["Maquillaje", "Maquillaje", "un poco de "],
    3024 : ["Hilo", " Hilo", "un poco de " ],
    3025 : ["Aguja de punto", "Agujas de punto", "una "],
    3026 : ["Coartada", "Coartadas", "una "],
    3027 : ["Sensor de temperatura exterior", "Sensores de temperatura exterior", "un "],

    #Dreamland Quests
    6001 : ["Planos del cuartel general chequebot", "Planos del cuartel general chequebot", "unos "],
    6002 : ["Caña", "Cañas", "una "],
    6003 : ["Correa de transmisión", "Correas de transmisión", "una "],
    6004 : ["Tenazas", " Tenazas", "unas "],
    6005 : ["Lámpara portátil", "Lámparas portátiles", "una "],
    6006 : ["Banjo", "Banjos", "un "],    
    6007 : ["Pulidora de hielo", "Pulidoras de hielo", "un "],    
    6008 : ["Esterilla cebra", "Esterilla cebra", "una "],
    6009 : ["Zinnias", "Zinnias", "unas "],
    6010 : ["Discos de Zydeco", "Discos de Zydeco", "algunos "],
    6011 : ["Calabacín", "Calabacines", "un "],
    6012 : ["Traje de remo", "Trajes de remo", "un "],

    #Dreamland+1 quests
    7001 : ["Cama básica", "Camas básicas", "una "],
    7002 : ["Cama sofisticada", "Camas sofisticadas", "una "],
    7003 : ["Colcha azul", " Colchas azules", "una "],
    7004 : ["Colcha de cachemir", "Colchas de cachemir", "una "],    
    7005 : ["Almohada", "Almohadas", "una "],   
    7006 : ["Almohada dura", " Almohadas duras", "una "], 
    7007 : ["Pijama", "Pijamas", "un "],    
    7008 : ["Pijama con pies", "Pijamas con pies", "un "],    
    7009 : ["Pijama colorado con pies", "Pijamas colorado con pies", "un "], 
    7010 : ["Pijama fucsia con pies", "Pijamas fucsia con pies", "un "],     
    7011 : ["Coral coliflor", " Corales coliflor", "un "],      
    7012 : ["Alga pegajosa", "Algas pegajosas", "un "],   
    7013 : ["Mazo de mortero", " Mazos de mortero", "una "],
    7014 : ["Tarro de crema antiarrugas ", " Tarro de crema antiarrugas", "un "],
    }
QuestsHQOfficerFillin = lHQOfficerM
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = lToonHQfull
QuestsHQLocationNameFillin = "en cualquier barrio"

QuestsTailorFillin = "Sastre"
QuestsTailorWhereFillin = ""
QuestsTailorBuildingNameFillin = "Tienda de Ropa"
QuestsTailorLocationNameFillin = "en cualquier barrio"
QuestsTailorQuestSCString = "Tengo que ir al sastre."

QuestMovieQuestChoiceCancel = "¡Vuelve más tarde si necesitas una dibutarea! ¡Ciao!"
QuestMovieTrackChoiceCancel = "¡Vuelve más tarde cuando te hayas decidido! ¡Ciao!"
QuestMovieQuestChoice = "Elige una dibutarea."
QuestMovieTrackChoice = "¿Te decidiste? Elige un circuito o vuelve más tarde."

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
    QUEST : "Ya estás listo.\aSal y ponte a caminar hasta que decidas qué circuito elegir.\aPiénsalo bien, porque este será tu circuito final.\aCuando estés seguro, vuelve conmigo.",
    INCOMPLETE_PROGRESS : "Piénsalo bien.",
    INCOMPLETE_WRONG_NPC : "Piénsalo bien.",
    COMPLETE : "¡Muy buena elección!",
    LEAVING : "Buena suerte.  Vuelve conmigo cuando tengas dominada tu nueva habilidad.",
    }

QuestDialog_3225 = {
    QUEST : "¡Gracias por venir, _avName_!\a"+TheCogs+" del vecindario asustaron a mi repartidor.\a¡No tengo a nadie que entregue esta ensalada a _toNpcName_!\a¿Puedes encargarte tú? ¡Muchas gracias!_where_"
    }

QuestDialog_2910 = {
    QUEST : "¿Ya regresaste?\aBuen trabajo con el resorte.\aEl objeto final es un contrapeso.\aPásate a ver a _toNpcName_ y tráete lo que encuentres._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 jefebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, derrotaste a los jefebots. ¡Ve al cuartel general para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 abogabots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, derrotaste a los abogabots. ¡Ve al cuartel general para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    162 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 chequebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, derrotaste a los chequebots. ¡Ve al cuartel general para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    163 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 vendebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, derrotaste a los vendebots. ¡Ve al cuartel general para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    164 : {QUEST : "Creo que te vendrán bien unas cuantas bromas nuevas.\aVe a ver a %s, quizá te pueda ayudar._where_" % Flippy },
    165 : {QUEST : "Muy buenas.\aCreo que tienes que practicar con las bromas.\aCada vez que alcances a un bot con una de las bromas, aumentará tu experiencia.\aCuando tengas la suficiente experiencia, podrás usar bromas mejores.\aPractica ahora con tus bromas derrotando a 4 bots."},
    166 : {QUEST : "Te felicito, derrotaste a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 jefebots."},
    167 : {QUEST : "Te felicito, derrotaste a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 abogabots."},
    168 : {QUEST : "Te felicito, derrotaste a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 vendebots."},
    169 : {QUEST : "Te felicito, derrotaste a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 chequebots."},
    170 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; él te aconsejará bien._where_" },
    171 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; él te aconsejará bien._where_" },
    172 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; ella te aconsejará bien._where_" },

    175 : {GREETING : "",
           QUEST : "¿Sabías que tienes tu propia casa dibu?\aLa vaca Clarabel lleva un catálogo telefónico donde puedes encargar muebles para decorar tu casa.\a¡También puedes comprar frases, ropa y otros artículos divertidos de SpeedChat!\aLe diré a Clarabel que te mande tu primer catálogo.\a¡Recibirás cada semana una catálogo de novedades!\aVete a casa y usa el teléfono para llamar a Clarabel.",
           INCOMPLETE_PROGRESS : "Vete a casa y usa el teléfono para llamar a Clarabel.",
           COMPLETE : "¡Que te diviertas encargándole cosas a Clarabel!\aAcabo de terminar de redecorar mi casa. ¡Quedó dibufantástica!\a¡Sigue haciendo dibutareas para conseguir más recompensas!",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "Las bromas de lanzamiento y chorro son estupendas, pero te harán falta otras para enfrentarte a los bots de niveles superiores.\aCuando te juntes con otros dibus para luchar contra los bots, podrás combinar ataques para infligirles más daños. \aPrueba con distintas combinaciones de trucos para ver cuáles funcionan mejor.\aEn el siguiente circuito, escoge entre Sonido y Curadibu.\aSonido es una broma especial que causa daños a todos los bots al hacer impacto.\aCuradibu te permite sanar a otros dibus durante el combate.\aCuando te hayas decidido, regresa para elegir la broma que desees.",
           INCOMPLETE_PROGRESS : "¿Ya regresaste?  Ok, ¿te decidiste ya?",
           INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
           COMPLETE : "Buena decisión.  Antes de usar esas bromas, deberás entrenarte con ellas.\aEn el entrenamiento tienes que completar una serie de dibutareas.\aCada tarea te proporcionará un fotograma de la animación del ataque con la broma.\aCuando reúnas los 15, conseguirás la tarea final de entrenamiento, que te permitirá usar la nueva broma.\aRevisa cómo vas en el dibucuaderno.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Si quieres recorrer la ciudad más fácilmente, ve a ver a _toNpcName_._where_" },
    1040 : { QUEST : "Si quieres recorrer la ciudad más fácilmente, ve a ver a _toNpcName_._where_" },
    1041 : { QUEST : "¡Hola! ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amigo mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1042 : { QUEST : "¡Hola! ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amigo mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1043 : { QUEST : "¡Hola! ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amigo mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1044 : { QUEST : "Ey, gracias por pasar por aquí.  La verdad es que necesito ayuda.\aComo ves, no tengo clientes.\aPerdí mi libro secreto de recetas y ya nadie viene a mi restaurante.\aLo vi por última vez justo antes de que los bots ocupasen mi edificio.\a¿Puedes ayudarme a recuperar cuatro de mis famosas recetas?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Conseguiste encontrar mis recetas?" },
    1045 : { QUEST : "¡Muchas gracias!\aEn poco tiempo tendré todo el recetario y podré volver a abrir mi restaurante.\aAh, tengo una nota para ti: algo sobre el teletransporte.\aDice 'Gracias por ayudar a mi amigo. Entrega esto en el cuartel general'.\aDe verdad, muchas gracias.\a¡Adiós!",
             LEAVING : "",
             COMPLETE : "Ah, sí, aquí dice que fuiste de gran ayuda para algunos de los amigos de la calle Locuela.\aDice que necesitas teletransportarte al centro de Toontown.\aPues bien, eso está hecho.\aAhora puedes teletransportarte para volver al dibuparque desde casi cualquier lugar de Toontown.\aAbre tu mapa y haz clic en "+lToontownCentral+"." },
    1046 : { QUEST : "Los chequebots estuvieron dando la lata en la Caja de Ahorros Dine Rodríguez.\aPásate por ahí para ver si puedes hacer algo._where_" },
    1047 : { QUEST : "Los chequebots entraron en el banco para robar nuestras calculadoras.\aRecupera cinco calculadoras que robaron los chequebots.\aPara no tener que estar yendo y viniendo, tráelas todas de una vez.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Sigues buscando las calculadoras?" },
    1048 : { QUEST : "¡Uau!  Gracias por recuperar nuestras calculadoras.\aMmm... Están un poco estropeadas.\a¿Puedes llevárselas a _toNpcName_ a su tienda, \"Cosquilladores automáticos\", en esta calle?\aTal vez las pueda arreglar.",
             LEAVING : "", },
    1049 : { QUEST : "¿Qué es eso? ¿Calculadoras rotas?\a¿Chequebots, dices?\aUm, veamos...\aSí, quitaron los engranajes, pero no me quedan repuestos...\a¿Sabes qué podría servirnos? Unos engranajes de bots, grandes, de bots grandotes.\aLos engranajes de bots de nivel 3 valdrán.  Necesito dos para cada máquina, así que son diez en total.\a¡Tráelos enseguida y las arreglaré!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Recuerda que necesito diez engranajes para arreglar las calculadoras." },
    1053 : { QUEST : "Muy bien, con esto seguro que vale.\aTodas arregladas, sin cargo.\aDevuélveselas a Dine Rodríguez y dale un saludo de mi parte.",
             LEAVING : "",
             COMPLETE : "¿Están arregladas todas las calculadoras?\aBuen trabajo.  Seguro que tengo algo por aquí para recompensarte..." },
    1054 : { QUEST : "_toNpcName_ necesita ayuda con sus autos de payasos._where_" },
    1055 : { QUEST : "¡Hola! ¡No puedo encontrar por ningún sitio los neumáticos de este auto de payasos!\a¿Crees que podrás echarme una mano?\aMe parece que Perico Pirado los tiró al estanque del dibuparque del centro de Toontown. \aSi te colocas encima de uno de los amarraderos del estanque podrás intentar pescar los neumáticos para traérmelos.",
             GREETING : "¡Jujujú!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Algún problemita pescando los cuatro neumáticos?" },
    1056 : { QUEST : "¡Estupendísimo! ¡Ahora puedo volver a conducir este viejo auto de payasos!\aEh, creía que tenía una vieja bomba de aire por aquí para inflar estos neumáticos...\a¿Se la habrá llevado prestada _toNpcName_?\a¿Podrías hacerme el favor de pedirle que me la devuelva?_where_",
             LEAVING : "" },
    1057 : { QUEST : "¿Qué tal?\a¿Una bomba de aire, dices?\a¿Sabes qué? Si me ayudas a limpiar las calles de algunos de esos bots de nivel alto...\ate daré la bomba de aire.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Eso es todo lo que sabes hacer?" },
    1058 : { QUEST : "Buen trabajo, sabía que lo conseguirías.\aAquí está la bomba. Seguro que _toNpcName_ se alegra de recuperarla.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "¡Yujuuu! ¡Ya puedo conducir!\aPor cierto, gracias por ayudarme.\aToma esto." },
    1059 : { QUEST : "_toNpcName_ se está quedando sin suministros. ¿Puedes echarle una mano?_where_" },
    1060 : { QUEST : "¡Gracias por venir!\aEsos bots me robaron la tinta y casi no me queda nada.\a¿Podrías pescar un poco de tinta de pulpo en el estanque?\aPara pescar, basta con que te sitúes en el amarradero de la orilla.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Tuviste problemas para pescar?" },
    1061 : { QUEST : "¡Estupendo, gracias por la tinta!\a¿Sabes qué? Si quitases de en medio a unos cuantos de esos chupatintas...\ano me quedaría sin tinta tan rápidamente.\aDerrota a seis chupatintas en el centro de Toontown para llevarte una recompensa.",
             LEAVING : "",
             COMPLETE : "¡Gracias!  Te recompensaré por tu ayuda.",
             INCOMPLETE_PROGRESS : "Vi unos cuantos chupatintas más." },
    1062 : { QUEST : "¡Estupendo, gracias por la tinta!\a¿Sabes qué? Si quitases de en medio a unos cuantos de esos chupasangres...\ano me quedaría sin tinta tan rápidamente.\aDerrota a seis chupasangres en el centro de Toontown para llevarte una recompensa.",
             LEAVING : "",
             COMPLETE : "¡Gracias!  Te recompensaré por tu ayuda.",
             INCOMPLETE_PROGRESS : "Vi unos cuantos chupasangres más." },
    900 : { QUEST : "Dicen que _toNpcName_ necesita ayuda con un paquete._where_" },
    1063 : { QUEST : "¡Hola, gracias por venir!\aUn bot me robó un paquete muy importante delante de mis narices.\aPor favor, intenta recuperarlo.  Creo que era de nivel 3...\aAsí que tendrás que derrotar a bots de nivel 3 hasta que encuentres mi paquete.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No hubo suerte con el paquete, ¿eh?" },
    1067 : { QUEST : "¡Ese es, muy bien!\aEh, la dirección está borrosa...\aSolo se lee que es para un doctor, el resto está emborronado.\a¿Será para _toNpcName_?  ¿Puedes llevárselo?_where_",
             LEAVING : "" },
    1068 : { QUEST : "No esperaba ningún paquete.  Quizá sea para el doctor Eufo Rico.\aMi ayudante iba a ir ahí hoy de todas formas, así que le diré que se lo pregunte.\aMientras tanto, ¿te importa deshacerte de unos cuantos bots en mi calle?\aDerrota a diez bots en el centro de Toontown.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mi ayudante no volvió todavía." },
    1069 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un chequebot se lo robó a mi ayudante cuando volvía.\a¿Podrías intentar recuperarlo?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No hubo suerte con el paquete, ¿eh?" },
    1070 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un vendebot se lo robó a mi ayudante cuando volvía.\aLo siento, pero tendrás que encontrar a ese vendebot para recuperarlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No hubo suerte con el paquete, ¿eh?" },
    1071 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un jefebot se lo robó a mi ayudante cuando volvía.\a¿Podrías intentar recuperarlo?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No hubo suerte con el paquete, ¿eh?" },
    1072 : { QUEST : "¡Estupendo, lo recuperaste!\aDeberías probar con _toNpcName_, tal vez sea para él._where_",
             LEAVING : "" },
    1073 : { QUEST : "Oh, gracias por traerme mis paquetes.\aEspera un momento, estaba esperando dos.  ¿Podrías ir a ver a _toNpcName_ para preguntarle si tiene el otro?",
             INCOMPLETE : "¿Conseguiste encontrar mi otro paquete?",
             LEAVING : "" },
    1074 : { QUEST : "¿Dijiste que había otro paquete? A lo mejor lo robaron también los bots.\aDerrota a los bots hasta que encuentres el segundo paquete.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No hubo suerte con el otro paquete, ¿eh?" },
    1075 : { QUEST : "¡Al final resulta que sí había un segundo paquete!\aDeprisa, llévaselo a _toNpcName_ y pídele disculpas de mi parte.",
             COMPLETE : "¡Eh, llegó mi paquete!\aComo pareces ser un dibu muy servicial, esto te vendrá bien.",
             LEAVING : "" },
    1076 : { QUEST : "Hubo problemas en Peces Dorados, 14.\aA _toNpcName_ le vendrá bien una ayudita._where_" },
    1077 : { QUEST : "Gracias por venir. "+TheCogs+" robaron todos mis peces dorados.\aCreo que quieren venderlos para sacar un dinero rápido.\aEsos cinco peces fueron mi única compañía en esta tiendita durante tantos años...\aSi pudieses hacerme el favor de recuperarlos, te lo agradecería eternamente.\aSeguro que uno de los bots tiene mis peces.\aDerrota a los bots hasta que encuentres mis peces.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Por favor, recupera mis peces dorados." },
    1078 : { QUEST : "¡Oh, tienes mis peces!\a¿Eh? ¿Qué es eso? ¿Un recibo?\aAh, sí son los bots, a fin de cuentas.\aNo consigo averiguar qué diantre es este recibo. ¿Podrías llevárselo a _toNpcName_ para ver si él lo entiende?_where_",
             INCOMPLETE : "¿Qué dijo _toNpcName_ del recibo?",
             LEAVING : "" },
    1079 : { QUEST : "Mmm, déjame ver ese recibo.\a... Ah, sí, dice que le vendieron un pez dorado a un secuaz.\aNo menciona para nada qué fue de los otros cuatro peces.\aQuizá debas ponerte a buscar a ese secuaz.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No creo que te pueda ayudar más.\a¿Por qué no te pones a buscar ese pez dorado?" },
    1092 : { QUEST : "Mmm, déjame ver ese recibo.\a... Ah, sí, dice que le vendieron un pez dorado a un moneditas.\aNo menciona para nada qué fue de los otros cuatro peces.\aQuizá debas ponerte a buscar a ese moneditas.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No creo que te pueda ayudar más.\a¿Por qué no te pones a buscar ese pez dorado?" },
    1080 : { QUEST : "¡Oh, gracias a Dios! Encontraste a Oscar. Es mi favorito.\a¿Qué pasa, Oscar?  Oh, vaya... ¿De verdad? ... ¿Están ahí?\aOscar dice que los otros cuatro escaparon y se metieron en el estanque del dibuparque.\a¿Me haces el favor de ir a recogerlos? \aBasta con que los pesques en el estanque.",
             LEAVING : "",
             COMPLETE : "¡Oooh, qué contento estoy! ¡Por fin vuelvo a estar junto a mis amiguitos!\a¡Te mereces una estupenda recompensa!",
             INCOMPLETE_PROGRESS : "¿Te está costando encontrar a los peces?" },
    1081 : { QUEST : "Parece ser que _toNpcName_ se encuentra en una situación pegajosa.  Seguro que le vendrá bien una ayudita._where_" },
    1082 : { QUEST : "¡Se me derramó el pegamento rápido y me quedé pegado!\aSi pudiera hacer algo para liberarme...\aSe me ocurre una idea, si te sientes valiente.\aDerrota a unos vendebots y tráeme un poco de aceite.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1083 : { QUEST : "El aceite resultó útil, pero sigo sin despegarme del todo.\a¿Qué puedo probar? Nada funciona.\aSe me ocurre una idea, no pierdo nada probándola.\aDerrota a unos abogabots y tráeme un poco de grasa.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1084 : { QUEST : "No, no sirvió de nada. Esto no me hace gracia.\aPuse la grasa y no hubo suerte.\aSe me ocurre una idea para sacarme de aquí.\aDerrota a unos chequebots y trae agua para mojarme.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "¡Hurra! Me libré de ese pegamento rápido.\aComo recompensa, toma este obsequio.\aPodrás disfrutar de una combativa velada...\a¡Oh, no! ¡Volví a quedarme pegado!",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1085 : { QUEST : "_toNpcName_ está llevando a cabo ciertas investigaciones sobre los bots.\aVete a hablar con él si quieres ayudarle._where_" },
    1086 : { QUEST : "Efectivamente, estoy realizando un estudio sobre los bots.\aQuiero saber cómo funcionan.\aMe sería de gran ayuda que consiguieses algunos engranajes de bot.\aAsegúrate de que pertenezcan a bots de nivel 2 al menos, para que tengan el tamaño suficiente para examinarlos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿No pudiste conseguir suficientes engranajes?" },
    1089 : { QUEST : "Muy bien, veamos. ¡Excelentes especímenes!\aMmm...\aDe acuerdo, aquí está mi informe. Llévalo al cuartel general de inmediato.",
             INCOMPLETE : "¿Llevaste mi informe al cuartel general?",
             COMPLETE : "Buen trabajo, _avName_, a partir de ahora nos ocuparemos nosotros.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ tiene información útil para ti._where_" },
    1091 : { QUEST : "Dicen que en el cuartel general están trabajando en una especie de radar de bots.\aTe permitirá ver dónde están los bots y así poder encontrarlos más fácilmente.\aLa página Bot del dibucuaderno es la clave.\aSi derrotas suficientes bots, podrás sintonizar sus señales y detectar su paradero.\aSigue derrotando a los bots para estar listo.",
             COMPLETE : "¡Buen trabajo!  Seguro que esto te viene bien...",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsalo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
           INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
           INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
           COMPLETE : "Muy buena decisión...",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "Esos bots tan pesados están dando problemas otra vez.\a_toNpcName_ comunicó que falta otro objeto. Pásate por ahí, a ver si puedes arreglar la situación._where_" },
    2202 : { QUEST : "Hola, _avName_. Menos mal que viniste. Un cacomatraco acaba de pasar por aquí y se largó corriendo con un tubo interno.\aTemo que lo usen para sus malvados propósitos.\aPor favor, busca al bot y recupera el tubo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Conseguiste encontrar mi tubo interno?",
             COMPLETE : "¡Encontraste mi tubo interno! Eres SENSACIONAL. Aquí tienes tu recompensa...",
             },
    2203 : { QUEST : TheCogs+" están sembrando el caos en el banco.\aVe a ver al capitán Doblón, a ver qué puedes hacer._where_" },
    2204 : { QUEST : "Bienvenido a bordo, grumete.\a¡Arg! Esa escoria de bots aplastaron mi monóculo y no me puedo apañar sin él.\aSé un buen marinero y lleva esta prescripción al doctor Rompecubiertas para que me haga uno nuevo._where_.",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "¿Qué es esto?\aMe encantaría hacer este monóculo, pero los bots saquearon mis pertenencias.\aSi consigues arrebatarle las monturas de monóculo a un secuaz, me serás de gran ayuda.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Lo siento. Sin las monturas del secuaz, no hay monóculo.",
             },
    2206: { QUEST : "¡Excelente!\aUn momento...\aAquí tienes el monóculo de la receta. Llévaselo al capitán Doblón._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "¡Viento en popa!\aNo, si al final te vas a ganar los galones y todo.\aAquí tienes.",
            },
    2207 : { QUEST : "¡Perci Percebe tiene un bot en la tienda!\aMás vale que vayas para allá enseguida._where_" },
    2208 : { QUEST : "¡Vaya! Se te acaba de escapar, cariño.\aAquí había un apuñalaespaldas.  Se llevó mi peluca blanca grande.\aDijo que era para su jefe y no sé qué sobre un \"precedente legal\".\aSi pudieses recuperarla, te estaría eternamente agradecida.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Todavía no la encontraste?\aEs alta y puntiaguda.",
             COMPLETE : "¡La encontraste!\a¡Eres todo un encanto!\aTe ganaste esto, no hay duda...",
             },
    2209 : { QUEST : "Isidoro se está preparando para un viaje importante.\aAcércate a ver en qué puedes ayudarle._where_"},
    2210 : { QUEST : "Me vendrá bien tu ayuda.\aEn el cuartel general me pidieron que haga un viaje para averiguar de dónde proceden los bots.\aNecesito unas cuantas cosas para mi barco, pero ando escaso de golosinas.\aPásate a ver a Pepa Sastre para que te dé algo de lastre. Para conseguirlo, tendrás que hacerle un favor._where_",
             GREETING : "¿Qué hay, _avName_?",
             LEAVING : "",
             },
    2211 : { QUEST : "Así que Isidoro quiere lastre, ¿eh?\aTodavía me debe la última fanega.\aTe la daré si consigues limpiar mi calle de cinco microgerentes.",
             INCOMPLETE_PROGRESS : "¡No, necio! ¡Dije CINCO microgerentes!",
             GREETING : "¿Qué puedo hacer por ti?",
             LEAVING : "",
             },
    2212 : { QUEST : "Un trato es un trato.\aAquí tienes el lastre para ese tacaño de Isidoro._where_",
             GREETING : "Vaya, mira lo que aparece por aquí...",
             LEAVING : "",
             },
    2213 : { QUEST : "Buen trabajo. Sabía que se atendría a razones. \aAhora necesito una carta náutica de Pasma Rote.\aNo creo que me fíen ahí tampoco, así que tendrás que llegar a un acuerdo con él._where_.",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Sí, tengo la carta de navegación que necesita Isidoro.\aY te la daré si estás dispuesto a trabajar para conseguirla.\aEstoy intentando construir un astrolabio para orientarme con las estrellas.\aPara hacerlo, necesito tres engranajes de bot.\aVuelve cuando los hayas conseguido.",
             INCOMPLETE_PROGRESS: "¿Qué tal te va con los engranajes de bot?",
             GREETING : "¡Bienvenido!",
             LEAVING : "¡Buena suerte!",
             },
    2215 : { QUEST : "¡Oooh! Estos engranajes me vendrán muy bien.\aAquí tienes la carta. Dásela a Isidoro, y dale recuerdos._where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "Bueno, esto es todo. ¡Estoy listo para zarpar!\aTe dejaría acompañarme si no estuvieses tan verde. A cambio, toma esto.",
             },
    901 : { QUEST : "Si estás disponible, a Ajab le vendría bien una ayuda._where_",
            },
    2902 : { QUEST : "¿Tú eres el nuevo recluta?\aBien, bien. Tal vez puedas ayudarme.\aEstoy construyendo un cangrejo prefabricado gigante para confundir a los bots.\aAunque también me serviría una coraza. Ve a ver a Clodovico Cromañón y pídele una, por favor._where_",
             },
    2903 : { QUEST : "¡Muy buenas!\aSí, oí hablar del cangrejo gigante en el que trabaja Ajab.\aSin embargo, la mejor coraza que tengo está un poco sucia.\aPórtate bien y llévala a la tintorería antes de entregarla._where_",
             LEAVING : "¡Gracias!"
             },
    2904 : { QUEST : "Debes de ser el que viene de parte de Clodovico.\aCreo que puedo limpiar eso en un santiamén.\aDame un minuto...\aAquí tienes. ¡Como nuevo!\aSaluda a Ajab de mi parte._where_",
             },
    2905 : { QUEST : "Vaya, esto es exactamente lo que andaba buscando.\aYa que estás aquí, también voy a necesitar un resorte de reloj muy grande.\aPásate por la tienda de Garfio para ver si tiene uno._where_",
             },
    2906 : { QUEST : "Un resorte grande, ¿eh?\aLo siento, pero el más grande que tengo es bastante pequeño, en realidad.\aQuizás pueda hacer uno con los resortes de los gatillos de pistola de agua.\aTráeme tres de esas y veré qué puedo hacer.",
             },
    2907 : { QUEST : "Veamos...\aImpresionante. Simplemente impresionante.\aA veces me sorprendo a mí mismo.\aAquí tienes: un resorte grande para Ajab._where_",
             LEAVING : "¡Buen viaje!",
             },
    2911 : { QUEST : "Me encantaría contribuir a la causa, _avName_.\aPero me temo que las calles ya no son seguras.\a¿Por qué no acabas con unos cuantos chequebots? Después hablaremos.",
             INCOMPLETE_PROGRESS : "Creo que las calles todavía no son muy seguras.",
             },
    2916 : { QUEST : "Sí, tengo un contrapeso que le vendría bien a Ajab.\aSin embargo, creo que sería mejor que antes derrotases a un par de vendebots.",
             INCOMPLETE_PROGRESS : "Todavía no. Derrota a unos cuantos vendebots más.",
             },
    2921 : { QUEST : "Mmm, se supone que tengo que darte un contrapeso.\aPero me sentiría mucho más seguro si no hubiese tantos jefebots rondando por aquí.\aDerrota a seis y ven a verme.",
             INCOMPLETE_PROGRESS : "Creo que esta zona todavía no es segura...",
             },
    2925 : { QUEST : "¿Acabaste?\aBien, supongo que la zona ya es bastante segura.\aAquí tienes el contrapeso para Ajab._where_"
             },
    2926 : {QUEST : "Bueno, eso es todo.\aVeamos si funciona.\aMmm, hay un pequeño problema.\aNo puedo encenderlo porque ese edificio bot está tapando mi panel solar.\a¿Puedes hacerme el favor de reconquistarlo?",
            INCOMPLETE_PROGRESS : "Sigo sin tener electricidad. ¿Qué hay de ese edificio?",
            COMPLETE : "¡Estupendo! ¡Tienes talento para romper bots! Toma, aquí tienes tu recompensa...",
            },
    3200 : { QUEST : "Acabo de recibir una llamada de _toNpcName_.\aEstá teniendo un día de perros. Tal vez puedas ayudarle.\aPásate por ahí para ver qué necesita._where_" },
    3201 : { QUEST : "¡Ey, gracias por venir!\aNecesito que alguien lleve esta corbata de seda nueva a _toNpcName_.\a¿Me harías tú ese favor?_where_" },
    3203 : { QUEST : "¡Ah, esta debe de ser la corbata que encargué! ¡Gracias!\aHace juego con el traje mil rayas que acabo de terminar, ese de ahí.\aEh, ¿qué pasó con el traje?\a¡Oh, no! ¡"+TheCogs+" deben de haberme robado el traje nuevo!\aLucha con los bots hasta que encuentres el traje y tráemelo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya mi traje? ¡Seguro que se lo llevaron los bots!",
             COMPLETE : "¡Hurra! ¡Encontraste mi traje nuevo!\a¿Ves? Te dije que los bots lo tenían. Toma tu recompensa...",
             },

    3204 : { QUEST : "_toNpcName_ acaba de llamar para comunicar un robo.\a¿Por qué no te pasas por ahí para ver si puedes arreglar la situación?_where_" },
    3205 : { QUEST : "¡Hola, _avName_! ¿Viniste a ayudarme?\aAcabo de ahuyentar a un chupasangres de mi tienda. ¡Guau! Daba mucho miedo.\a¡Pero ahora no encuentro las tijeras! Seguro que se las llevó el chupasangres.\aPor favor, busca al chupasangres y recupera las tijeras.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Sigues buscando las tijeras?",
             COMPLETE : "¡Mis tijeras! ¡Muchas gracias! Toma tu recompensa...",
             },

    3206 : { QUEST : "Parece ser que _toNpcName_ está teniendo algún que otro problema con los bots.\aVe a ver si puedes ayudarle._where_" },
    3207 : { QUEST : "¡Buenas, _avName_! ¡Gracias por venir!\aUnos cuantos embaucadores entraron y se llevaron un taco de postales del mostrador.\a¡Por favor, derrota a esos embaucadores y recupera mis postales!",
             INCOMPLETE_PROGRESS : "¡No hay postales suficientes! ¡Sigue buscando!",
             COMPLETE : "¡Oh, gracias! ¡Ahora puedo entregar el correo a tiempo! Toma tu recompensa...",
             },

    3208 : { QUEST : "Recibimos quejas de los vecinos por todos esos gorrones.\aPor favor, intenta derrotar a diez aprovechados para ayudar a tus amigos, los dibus de los "+lDaisyGardens+". " },
    3209 : { QUEST : "¡Gracias por ocuparte de los gorrones!\a¡Ahora se desmadraron los televendedores!\aDerrota a diez televendedores en los "+lDaisyGardens+" y vuelve para llevarte una recompensa." },

    3247 : { QUEST : "Recibimos quejas de los vecinos sobre todos esos chupasangres.\aPor favor, intenta derrotar a veinte chupasangres para ayudar a tus amigos, los dibus de los "+lDaisyGardens+". " },


    3210 : { QUEST : "¡Oh, no, la flor chorreante de la calle Arce se quedó sin flores!\aLlévales diez flores chorreantes de las tuyas para ayudarles. \aPrimero comprueba que tienes diez flores chorreantes en el inventario.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "Necesito diez flores chorreantes. ¡No tienes suficientes!" },
    3211 : { QUEST : "¡Oh, muchas gracias! Esas flores arreglarán la situación.\aPero los bots que hay fuera me dan miedo.\a¿Puedes ayudarme derrotando a unos cuantos?\aVuelve cuando hayas derrotado a veinte bots en esta calle.",
             INCOMPLETE_PROGRESS : "¡Todavía quedan bots ahí fuera! ¡Sigue luchando!",
             COMPLETE : "¡Oh, gracias! Me fuiste de gran ayuda. Tu recompensa es...",
             },

    3212 : { QUEST : "_toNpcName_ necesita ayuda para encontrar una cosa que perdió.\aVe a verla, tal vez puedas ayudarle._where_" },
    3213 : { QUEST : "Hola, _avName_. ¿Puedes ayudarme?\aParece que perdí mi pluma estilográfica. Creo que se la llevaron unos bots.\aDerrótalos y recupera la pluma, por favor.",
             INCOMPLETE_PROGRESS : "¿Encontraste ya mi pluma?" },
    3214 : { QUEST : "¡Sí, es esa! ¡Muchas gracias!\aPero en cuanto te marchaste me di cuenta de que también me faltaba el tintero.\aVence a los bots y recupera el tintero, por favor.",
             INCOMPLETE_PROGRESS : "¡Sigo buscando el tintero!" },
    3215 : { QUEST : "¡Fantástico! Ya recuperé la pluma y el tintero.\aPero ¿a que no te lo imaginas?\a¡No encuentro la libreta! ¡La deben de haber robado también!\aDerrota a los bots hasta que encuentres la libreta y tráemela para que te dé una recompensa.",
             INCOMPLETE_PROGRESS : "¿Alguna novedad sobre la libreta?" },
    3216 : { QUEST : "¡Esa es mi libreta! ¡Hurra! Tu recompensa es...\a¡Eh! ¿Dónde está?\aTenía tu recompensa justo aquí, en la caja de seguridad. ¡Se la llevaron !\a¿Puedes creerlo? ¡"+TheCogs+" robaron tu recompensa!\aVence a los bots para recuperar la caja de seguridad.\aCuando me la traigas, te daré tu recompensa.",
             INCOMPLETE_PROGRESS : "¡Sigue buscando la caja de seguridad!  ¡Tu recompensa está dentro!",
             COMPLETE : "¡Por fin! Tenía tu nueva bolsa de bromas en la caja. Aquí está...",
             },

    3217 : { QUEST : "Estuvimos estudiando la mecánica de los vendebots.\aQueremos estudiar más de cerca algunas piezas.\aTráenos la rueda dentada de un fanfarrón.\aPuedes atraparlas cuando los bots estallan." },
    3218 : { QUEST : "¡Buen trabajo! Ahora tenemos que compararla con la rueda dentada de un efusivo.\aEsas ruedas dentadas son más difíciles de atrapar, así que sigue intentándolo." },
    3219 : { QUEST : "¡Fantástico! Ahora sólo necesitamos una rueda dentada más.\aEsta vez necesitamos la rueda de un mandamás.\aPara encontrar a estos bots, tal vez tengas que buscar en el interior de algunos edificios de vendebots.\aCuando la tengas, tráela y a cambio obtendrás tu recompensa." },

    3244 : { QUEST : "Estuvimos estudiando la mecánica de los abogabots.\aQueremos estudiar más de cerca algunas piezas.\aTráenos la rueda dentada de un persigueambulancias.\aPuedes atraparla cuando los bots estallan." },
    3245 : { QUEST : "¡Buen trabajo! Ahora tenemos que compararla con la rueda dentada de un apuñalaespaldas.\aEsas ruedas dentadas son más difíciles de atrapar, así que sigue intentándolo." },
    3246 : { QUEST : "¡Fantástico! Ahora sólo necesitamos una rueda dentada más.\aEsta vez necesitamos la rueda de un portavoz.\aCuando la tengas, tráela para obtener a cambio tu recompensa." },

    3220 : { QUEST : "Acabo de oír que _toNpcName_ estuvo preguntando por ti.\a¿Por qué no pasas a verla para ver qué quiere?_where_" },
    3221 : { QUEST : "¡Buenas, _avName_! ¡Aquí estás!\aHe oído que eres todo un experto en ataques chorreantes.\aNecesito a alguien que dé un buen ejemplo a todos los dibus de "+lDaisyGardens+".\aUsa tus ataques chorreantes para derrotar a un montón de bots.\aAnima a tus amigos a usar este tipo de ataques.\aCuando hayas derrotado a veinte bots, vuelve para llevarte una recompensa." },

    3222 : { QUEST : "Llegó el momento de demostrar tu dibupuntería.\aSi consigues recuperar cierto número de edificios bot, tendrás el privilegio de asumir tres tareas a la vez.\aPrimero, reconquista dos edificios bot cualesquiera.\aLlama a los amigos que quieras para que te ayuden."},
    3223 : { QUEST : "¡Un gran trabajo con los edificios! \aAhora reconquista dos edificios más.\aLos edificios deben de tener al menos dos pisos de altura." },
    3224 : { QUEST : "¡Fantástico!\aAhora basta con que recuperes dos edificios más.\aLos edificios deben tener al menos tres pisos de altura.\aCuando termines, vuelve para obtener tu recompensa.",
             COMPLETE : "¡Lo lograste, _avName_!\a¡Tienes una dibupuntería increíble!",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ dice que necesita ayuda.\a¿Por qué no vas a verla para ver en qué la puedes ayudar?_where_" },
    3235 : { QUEST : "¡Ah, esta debe de ser la ensalada que encargué!\aGracias por traérmela.\aTodos esos bots deben de haber asustado al repartidor habitual de _toNpcName_.\a¿Por qué no nos haces un favor y derrotas a unos cuantos bots de ahí fuera?\aDerrota a diez bots en los "+lDaisyGardens+" y vuelve con _toNpcName_.",
             INCOMPLETE_PROGRESS : "¿No estabas venciendo a los bots por mí?\a¡Maravilloso! ¡Sigue así!",
             COMPLETE : "¡Oh, muchas gracias por derrotar a esos bots!\aAhora quizás pueda seguir con mis repartos normales.\aTu recompensa es...",
             INCOMPLETE_WRONG_NPC : "Informa a _toNpcName_ sobre los bots a los que derrotate._where_" },

    3236 : { QUEST : "Hay demasiados abogabots ahí.\a¡Ayuda en lo que puedas!\aRecupera tres edificios de abogabots." },
    3237 : { QUEST : "¡Un gran trabajo con los edificios de abogabots! \a¡Pero ahora hay demasiados vendebots!\aRecupera tres edificios de vendebots y vuelve a buscar tu recompensa." },

    3238 : { QUEST : "¡Oh, no! ¡Un bot \"confraternizador\" robó la llave de los "+lDaisyGardens+"!\aIntenta recuperarla.\aRecuerda, sólo encontrarás al confraternizador en el interior de edificios de vendebots. " },
    3239 : { QUEST : "Sí, encontraste una llave, pero no es la correcta.\aNecesitamos la llave de los "+lDaisyGardens+".\a¡Sigue buscando! ¡La tiene un bot \"confraternizador\"!" },

    3242 : { QUEST : "¡Oh, no! ¡Un bot picapleitos robó la llave de "+lDaisyGardens+"!\aIntenta recuperarla.\aRecuerda, solo encontrarás al picapleitos en el interior de edificios de abogabots. " },
    3243 : { QUEST : "Sí, encontraste una llave, pero no es la correcta.\aNecesitamos la llave de los "+lDaisyGardens+".\a¡Sigue buscando! ¡La tiene un bot picapleitos!" },

    3240 : { QUEST : "_toNpcName_ me acaba de decir que un picapleitos le robó una bolsa de alpiste.\aDerrota a los picapleitos hasta que encuentres el alpiste de Federico Tilla y llévaselo.\aSólo encontrarás a los picapleitos en el interior de los edificios de abogabots._where_",
             COMPLETE : "¡Oh, muchas gracias por encontrar el alpiste!\aTu recompensa es...",
             INCOMPLETE_WRONG_NPC : "¡Muy bien, lograste recuperar el alpiste!\aAhora llévaselo a _toNpcName_._where_",
             },

    3241 : { QUEST : "Algunos edificios bot están creciendo demasiado para nuestro gusto.\aIntenta recuperar algunos de los edificios más altos.\aReconquista cinco edificios de tres plantas o más y vuelve para llevarte una recompensa.",
             },

    3250 : { QUEST : "Doña Citronia recibió información sobre la existencia de un cuartel general vendebot en la calle Arce.\aReúnete con ella para investigarlo.",
             },
    3251 : { QUEST : "Aquí se cuece algo.\aHay muchísimos vendebots.\aDicen que construyeron su propio cuartel general al final de la calle.\aRecórrela a ver si averiguas lo que está pasando.\aBusca vendebots por su cuartel general, derrota a cinco de ellos y regresa.",
             },
    3252 : { QUEST : "Vamos, suéltala.\a¿Qué dices?\a¿Un cuartel general vendebot? ¡Dios mío! Hay que actuar.\aDebemos poner al corriente a Doña Zanahoria, ella sabrá qué hacer.\aVete corriendo y cuéntale lo que sabes. Está ahí mismo, bajando la calle.",
            },
    3253 : { QUEST : "¿Qué quieres? Estoy muy ocupada.\a¿Cómo? ¿Un cuartel general bot?\aQué bobada. Es imposible.\aTiene que ser un error. Es inconcebible.\a¿Cómo? No me lo discutas.\aBueno, mira, si quieres, tráeme pruebas.\aSi los vendebots están construyendo su cuartel general, todos los bots que anden por ahí llevarán planos.\aA los bots les encanta la burocracia, ¿no sabías? \aVe derrotando vendebots en el lugar que me dices hasta que encuentres los planos.\aLuego me los traes y ya veremos si te creo o no.",
            },
    3254 : { QUEST : "¿Otra vez tú por aquí? ¿Cómo? ¿Planos? ¿Los conseguiste?\aDéjame que los vea. Vaya, ¿una fábrica?\aDebe de ser la planta donde construyen los vendebots... ¿Y esto qué es?\aJusto lo que pensaba.\aComo sospechaba, están construyendo un cuartel general vendebot.\aQué problema. Voy a tener que hacer unas cuantas llamadas. Mira, estoy muy ocupada. Adiós.\a¿Cómo? Sí, sí. Llévale los planos a Doña Citronia.\aSeguro que ella los entenderá mejor que yo.",
             COMPLETE : "¿Qué te dijo Doña Zanahoria?\aEntonces, teníamos razón. Esto es muy peligroso. ¿A ver los planos?\aVaya, parece que los vendebots construyeron una planta con maquinaria para la fabricación de bots.\aEsto me huele muy mal. Mantente al margen hasta que consigas más puntos de risa.\aCuando reúnas más podremos seguir con la investigación.\aPor ahora, aquí tienes tu recompensa. ¡Muy bien!",
            },


    3255 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3256 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3257 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3258 : { QUEST : "No sabemos realmente qué es lo que están tramando los bots en su nuevo cuartel general.\aQuiero que me traigas información, pero obtenida directamente de los propios bots.\aSi conseguimos cuatro notas de oficina de los vendebots sacadas del mismo cuartel, podremos hacernos una idea más clara.\aTráeme la primera nota en cuanto la consigas así voy estudiando la información a medida que aparezca.",
             },
    3259 : { QUEST : "¡Estupendo! A ver qué dice la nota.\a\"Estimados vendebots:\"\a\"Estaré en mi oficina del penthouse de las torres vendebots ascendiendo bots a niveles superiores.\"\a\"Cuando reúnan los méritos necesarios, suban a mi oficina en el ascensor del vestíbulo de entrada.\"\a\"Se acabó el descanso. ¡A trabajar!\"\a\"Firmado, vendebot VIP\"\a¡Ajá! A "+Flippy+" le va a interesar esto. Se lo voy a mandar ahora mismo.\aMárchate ya en busca de la segunda nota y tráemela en cuanto la tengas.",
             },
    3260 : { QUEST : "Ya regresaste, qué bien. A ver qué encontraste...\a\"Estimados vendebots:\"\a\"Se instaló un sistema de seguridad nuevo en las torres vendebots para impedir el acceso a los dibus.\"\a\"Los dibus que se encuentren en las torres serán detenidos para su interrogatorio.\"\a\"Nos reuniremos en el vestíbulo para discutir el asunto durante el aperitivo.\"\a\"Firmado, Confraternizador\"\aMuy, muy interesante. Tengo que pasar esta información inmediatamente.\aTráeme una tercera nota, por favor.",
             },
    3261 : { QUEST : "¡Muy bien _avName_! ¿Qué dice la nota?\a\"Estimados vendebots:\"\a\"Los dibus se las ingeniaron para infiltrarse en las torres vendebot.\"\a\"Esta noche los llamaré a la hora de la cena para darles más datos.\"\a\"Firmado, Televendedor\"\aMmm, Me pregunto cómo estarán colándose los dibus....\aTráeme una última nota. Creo que con eso bastará para hacerme una idea.",
             COMPLETE : "¡Sabía que lo lograrías! A ver, la nota dice...\a\"Estimados vendebots:\"\a\"Ayer comí con el Sr. Hollywood y me dijo que VIP ha estado muy ocupado.\"\a\"Sólo recibirá bots que merezcan un ascenso.\"\a\"Se me olvidaba, quedé con Efusivo para jugar al golf el domingo.\"\a\"Firmado, Fanfarrón\"\aBueno, _avName_, muchas gracias por tu valiosa ayuda.\aToma, aquí tienes tu recompensa.",
             },

    3262 : { QUEST : "_toNpcName_ posee información reciente sobre la fábrica-cuartel general vendebot.\aVe a ver de qué se trata._where_" },
    3263 : { GREETING : "¡Qué hay de nuevo, camarada!",
             QUEST : "Me llamo Don Silvestre, Silvestre para los amigos.\aVoy al grano, no me gusta andarme por las ramas.\aMira, los vendebots acaban de construir una gran fábrica para reproducirse como hormigas.\aÚnete a unos cuantos camaradas dibus y destruye la dichosa fábrica.\aDentro del cuartel general vendebot podrás localizar el túnel que lleva a la fábrica y luego subir en el ascensor.\aAntes que nada, comprueba que vas bien cargado de bromas y puntos de risa y que te acompañan unos dibus bien fornidos.\aDerrota al capataz dentro de la fábrica y así detendrás el avance vendebot.\a¡Vamos! Ahí tienes tu tablita de ejercicios. Un, dos, un, dos.",
             LEAVING : "¡Nos vemos!",
             COMPLETE : "¿Qué hay de nuevo, camarada? ¡Haz hecho un buen trabajo en la fábrica!\aAsí que encontraste una pieza de traje bot.\aDebe de ser un excedente de la cadena de montaje bot.\aNos podría venir de lujo. Recoge todas las que puedas siempre que tengas un huequito.\aA lo mejor, si consigues un traje completo reuniendo todas las piezas, podemos sacarle algún provecho...."
             },

    4001 : {GREETING : "",
            QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsalo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
            INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
            INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
            COMPLETE : "Muy buena decisión...",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsalo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
            INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
            INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
            COMPLETE : "Muy buena decisión...",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "Seguro que a Ropo Pompón le viene bien un poco de ayuda en su investigación._where_",
             },
    4201 : { GREETING: "¡Hola!",
             QUEST : "Estoy muy preocupado con una racha de robos de instrumentos musicales.\aEstoy llevando a cabo un estudio entre mis compañeros comerciantes.\aTal vez pueda encontrar una pauta que me ayude a resolver el caso.\aPásate por Sonatas y Sonatinas para que Tina te dé su inventario de concertinas. _where_",
             },
    4202 : { QUEST : "Sí, hablé con Ropo esta mañana.\aTengo el inventario aquí mismo.\aLlévaselo, ¿sí?_where_"
             },
    4203 : { QUEST : "¡Fantástico! Uno menos...\aAhora ve a buscar el de Uki._where_",
             },
    4204 : { QUEST : "¡Oh! ¡El inventario!\aMe olvidé de él.\aSeguro que lo tengo terminado para cuando hayas derrotado a diez bots.\aPásate por aquí después y te prometo que estará listo.",
             INCOMPLETE_PROGRESS : "31, 32... ¡Uy!\a¡Me hiciste perder la cuenta!",
             GREETING : "",
             },
    4205 : { QUEST : "Ah, ahí estás.\aGracias por darme algo de tiempo.\aLlévale esto a Ropo y salúdalo de mi parte._where_",
             },
    4206 : { QUEST : "Mmm, muy interesante.\aAhora sí que estoy encaminado.\aMuy bien, el último inventario es el de Bibi._where_",
             },
    4207 : { QUEST : "¿Inventario?\a¿Cómo voy a hacerlo si no tengo el formulario?\aVe a ver si Sordino Quena puede darme uno._where_",
             INCOMPLETE_PROGRESS : "¿Alguna novedad sobre el formulario?",
             },
    4208 : { QUEST : "¡Pues claro que tengo un formulario de inventario!\aPero no es gratis, ¿sabes?\a¿Sabes qué? Te lo daré a cambio de una tarta de nata entera.",
             GREETING : "¡Muy buenas!",
             LEAVING : "Hasta luego...",
             INCOMPLETE_PROGRESS : "No me alcanza con un trozo.\aMe quedaré con hambre. Quiero TODA la tarta.",
             },
    4209 : { GREETING : "",
             QUEST : "Mmm...\a¡Qué rica!\aAquí tienes el formulario para Bibi._where_",
             },
    4210 : { GREETING : "",
             QUEST : "Gracias. Fuiste de gran ayuda.\aVeamos... Violines Bibi: 2\a¡Ya está! ¡Aquí tienes!",
             COMPLETE : "Buen trabajo, _avName_.\aSeguro que ahora llego al fondo de la cuestión de los robos.\a¿Por qué no llegas tú al fondo de esto?",
             },

    4211 : { QUEST : "Mira, el doctor Pavo Rotti está llamando cada cinco minutos. ¿Puedes ir a ver qué problema tiene?_where_",
             },
    4212 : { QUEST : "¡Guau! Me alegro de que el cuartel general mandara por fin a alguien.\aNo tuve un solo cliente durante días.\aSon estos malditos contables que hay por todas partes.\aCreo que están propagando una mala higiene bucal entre los vecinos.\aDerrota a diez de ellos y veamos si el negocio mejora.",
             INCOMPLETE_PROGRESS : "Sigo sin tener clientes. ¡Pero sigue luchando!",
             },
    4213 : { QUEST : "¿Sabes? A lo mejor resulta que los culpables no eran los contables.\aIgual son los chequebots en general.\aAcaba con veinte de ellos y tal vez venga alguien a mi clínica de una vez.",
             INCOMPLETE_PROGRESS : "Sé que veinte son muchos. Pero seguro que valdrá la pena.",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡No lo entiendo!\aSigo sin tener ni un solo cliente.\aA lo mejor hay que atacar a la raíz del problema.\aIntenta reconquistar un edificio de chequebots.\aEso debería bastar.",
             INCOMPLETE_PROGRESS : "¡Por favor! ¡Sólo un pequeño edificio nomás!",
             COMPLETE : "Sigue sin venir un alma por aquí.\aPero la verdad es que, pensándolo bien...\a¡Tampoco venían clientes antes de que los bots nos invadiesen!\aSin embargo, aprecio de veras tu ayuda.\aSeguro que esto te viene bien."
             },

    4215 : { QUEST : "Olga necesita desesperadamente a alguien que la ayude.\a¿Por qué no pasas a verla para ver qué puedes hacer?_where_",
             },
    4216 : { QUEST : "¡Gracias por venir tan pronto!\aParece que los bots se hicieron con muchos de los billetes de crucero de mis clientes.\aUki dice que vio a un efusivo irse de aquí con un montón.\aTrata de recuperar el billete a Alaska de Chopo Chopín.",
             INCOMPLETE_PROGRESS : "Los efusivos podrían estar en cualquier sitio ya...",
             },
    4217 : { QUEST : "¡Estupendo! ¡Lo encontraste!\a¿Ahora me harías el favor de llevárselo a Chopo Chopín?_where_",
             },
    4218 : { QUEST : "¡Estupendo, estupendísimo!\a¡Alaska, voy para allá!\aYa no soporto a estos malditos bots.\aOye, creo que Olga te vuelve a necesitar._where_",
             },
    4219 : { QUEST : "Sí, lo adivinaste.\aNecesito que sacudas a los pesados de los efusivos para recuperar el boleto de Felisa Felina al festival de Jazz.  \aYa sabes cómo funciona...",
               INCOMPLETE_PROGRESS : "Hay más en alguna parte...",
             },
    4220 : { QUEST : "¡Estupendo!\a¿Podrías alcanzarle el boleto también?_where_",
             },
    4221 : { GREETING : "",
             LEAVING : "Hasta luego...",
             QUEST : "¡Hola!\aMe voy de viaje, _avName_.\aAntes de irte, más vale que te pases de nuevo a ver a Olga..._where_",
             },
    4222 : { QUEST : "¡Este es el último, lo prometo!\aAhora hay que buscar el boleto de Barbo para el gran concurso de canto.",
             INCOMPLETE_PROGRESS : "Vamos, _avName_.\aBarbo cuenta contigo.",
             },
    4223 : { QUEST : "Esto hará que Barbo se alegre mucho._where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Sí, sí, SÍ!\a¡Sensacional!\a¿Sabes? Este año, los chicos y yo vamos a arrasar en el concurso.\aOlga dice que vuelvas por ahí para recoger tu recompensa._where_\a¡Adiós, adiós, ADIÓS!",
             COMPLETE : "Gracias por todo, _avName_.\aEres muy valioso aquí en Toontown.\aHablando de cosas valiosas...",
             },

    902 : { QUEST : "Ve a ver a Leo.\aNecesita que alguien entregue un mensaje._where_",
            },
    4903 : { QUEST : "¡Amigo!\aMis castañuelas están empañadas y tengo una gran actuación esta noche.\aLlévaselas a Carlos para ver si las puede limpiar._where_",
             },
    4904 : { QUEST : "Sí, creo que puedo limpiarlas.\aPero necesito un poco de tinta azul de un pulpo.",
             GREETING : "¡Hola!",
             LEAVING : "¡Adiós!",
             INCOMPLETE_PROGRESS : "Los pulpos están cerca de los amarraderos.",
             },
    4905 : { QUEST : "¡Sí! ¡Eso es!\aAhora necesito un poco de tiempo para limpiarlas.\a¿Por qué no vas a recuperar un edificio de un piso mientras trabajo?",
             GREETING : "¡Hola!",
             LEAVING : "¡Adiós!",
             INCOMPLETE_PROGRESS : "Sólo un poco más...",
             },
    4906 : { QUEST : "¡Muy bien!\aAquí tienes las castañuelas para Leo._where_",
             },
    4907 : { GREETING : "",
             QUEST : "¡Muy bien, amigo!\aTienen una pinta estupenda.\aAhora necesito que consigas una copia de la letra de \"Navidades felices\" de Lírica Tástrofe._where_",
             },
    4908 : { QUEST: "¡Muy buenas!\aMmm, no tengo un ejemplar de esa letra a mano.\aSi me dieses algo de tiempo, la podría escribir de memoria.\a¿Por qué no te vas a recuperar un edificio de dos plantas mientras la escribo?",
             },
    4909 : { QUEST : "Lo siento.\aMi memoria ya no es lo que era.\aSi vas a recuperar un edificio de tres plantas, seguro que tendré la letra lista para cuando vuelvas.",
             },
    4910 : { QUEST : "¡Ya está!\aSiento haber tardado tanto.\aLlévasela a Leo._where_",
             GREETING : "",
             COMPLETE : "¡Genial, amigo!\a¡Mi concierto va a ser la bomba!\aAh, que no se me olvide. Toma, esto te servirá para los bots."
             },
    5247 : { QUEST : "Este barrio es bastante duro...\aTe vendría bien aprender unos cuantos trucos nuevos.\a_toNpcName_ me enseñó todo lo que sé, así que a lo mejor te puede enseñar a ti también._where_" },
    5248 : { GREETING : "Aah, sí.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Parece que mi tarea te está causando problemas.",
             QUEST : "Aaah, un nuevo aprendiz, bienvenido.\aYo sé todo lo que hay que saber sobre tartas.\aPero antes de empezar con tu entrenamiento, tienes que hacerme una pequeña demostración.\aSal fuera y derrota a diez de los bots más grandes." },
    5249 : { GREETING: "Mmmmm.",
             QUEST : "¡Excelente!\aAhora, demuéstrame tu habilidad como pescador.\aAyer tiré tres dados de goma al estanque.\aPéscalos y tráemelos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Parece que la caña y y la línea no son tu fuerte." },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán estupendos colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de abogabots más grandes.",
             INCOMPLETE_PROGRESS : "¿Tienes problemas con los edificios?", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán excelentes colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de jefebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Tienes problemas con los edificios?", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán excelentes colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de chequebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Tienes problemas con los edificios?", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán excelentes colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de vendebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Tienes problemas con los edificios?", },
    5200 : { QUEST : "Esos bots tan pesados están otra vez dando problemas.\a_toNpcName_ dijo que falta otro objeto. Pásate por ahí, a ver si puedes arreglar la situación._where__where_" },
    5201 : { GREETING: "",
             QUEST : "Hola, _avName_. Creo que debo darte las gracias por venir.\aUn grupo de cazacabezas estuvo aquí y se llevó mi balón de fútbol.\a¡Su jefe me dijo que tenía que hacer un recorte de plantilla y me lo quitó!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Lograste encontrar mi balón?",
             COMPLETE : "¡Yujuuu! ¡Lo lograste! Aquí tienes tu recompensa...",
             },
    5261 : { GREETING: "",
             QUEST : "Hola, _avName_. Creo que debo darte las gracias por venir.\aUn grupo de doscaras estuvo aquí y se llevó mi balón de fútbol.\a¡Su jefe me dijo que tenía que hacer un recorte de plantilla y me lo quitó!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Lograste encontrar mi balón?",
             COMPLETE : "¡Yujuuu! ¡Lo lograste! Aquí tienes tu recompensa...",
             },
    5262 : { GREETING: "",
             QUEST : "Hola, _avName_. Creo que debo darte las gracias por venir.\aUn grupo de monederos estuvo aquí y se llevó mi balón de fútbol.\a¡Su jefe me dijo que tenía que hacer un recorte de plantilla y me lo quitó!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Lograste encontrar mi balón?",
             COMPLETE : "¡Yujuuu! ¡Lo lograste! Aquí tienes tu recompensa...",
             },
    5263 : { GREETING: "",
             QUEST : "Hola, _avName_. Creo que debo darte las gracias por venir.\aUn grupo de portavoces estuvo aquí y se llevó mi balón de fútbol.\a¡Su jefe me dijo que tenía que hacer un recorte de plantilla y me lo quitó!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Lograste encontrar mi balón?",
             COMPLETE : "¡Yujuuu! ¡Lo lograste! Aquí tienes tu recompensa...",
             },
    5202 : { QUEST : lTheBrrrgh+" fue invadida por los bots más duros de pelar que vi en mi vida.\aMás vale que cargues más bromas.\aMe dijeron que es posible que _toNpcName_ tenga una bolsa más grande en la que te cabrán más bromas._where_" },
    5203 : { GREETING: "¿Eh? ¿Estás en mi equipo de trineo?",
             QUEST : "¿Qué? ¿Quieres una bolsa?\aEl caso es que tenía una por aquí... ¿Estará en mi trineo?\aPero... ¡No veo mi trineo desde la gran carrera!\a¿Se lo habrá llevado uno de esos bots?",
             LEAVING : "¿Viste mi trineo?",
             INCOMPLETE_PROGRESS : "¿Quién decías que eras? Lo siento, estoy un poco mareado por el choque." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Es ese mi trineo? No veo ninguna bolsa por aquí.\aCreo que Perico Arenque estaba en el equipo... ¿La tendrá él?_where_" },
    5205 : { GREETING : "¡Oooh, la cabeza!",
             LEAVING : "",
             QUEST : "¿Eh? ¿Doroteo qué? ¿Una bolsa?\aAh, ¿no era miembro de nuestro equipo de trineo?\aMe duele tanto la cabeza que no puedo pensar bien.\a¿Puedes pescar unos cuantos cubitos de hielo en el estanque para que me los ponga en la cabeza?",
             INCOMPLETE_PROGRESS : "¡Ayyy, la cabeza me va a estallar! ¿Tienes un poco de hielo?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Aaah, mucho mejor!\aAsí que buscas la bolsa de Doroteo, ¿eh?\aCreo que terminó en la cabeza de Nutrio Cenutrio después del choque._where_" },
    5207 : { GREETING : "¡Eeeh!",
             LEAVING : "",
             QUEST : "¿Bolsa? ¿Quién ser Perico?\a¡Yo tener miedo de edificios! ¡Tú derrotar edificios, yo darte bolsa!",
             INCOMPLETE_PROGRESS : "¡Más edificios! ¡Yo todavía tener miedo!",
             COMPLETE : "¡Oooh! ¡Tú gustarme!" },
    5208 : { GREETING : "",
             LEAVING : "¡Eeeh!",
             QUEST : "¡Oooh! ¡Tú gustarme!\aTú ir a clínica de esquí. Bolsa ahí." },
    5209 : { GREETING : "¡Amigo!",
             LEAVING : "¡Nos vemos!",
             QUEST : "¡Amigo, ese tal Nutrio Cenutrio está loco!\aCompadre, si estás loco como Nutrio, la bolsa será tuya.\a¡Embólsate a unos cuantos bots y te harás con la bolsa, compañero! ¡Vamos!",
             INCOMPLETE_PROGRESS : "¿Estás seguro de que eres bastante salvaje? Ve a destruir a los bots.",
             COMPLETE : "¡Eh, eres todo un campeón! ¡Les diste de lo lindo a un montón de bots!\a¡Aquí tienes la bolsa!" },

    5210 : { QUEST : "_toNpcName_ está enamorada en secreto de alguien del barrio.\aSi la ayudas, te recompensará de lo lindo._where_" },
    5211 : { GREETING: "¡Buaaaa!",
             QUEST : "Me pasé toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots con pico entró y se la llevó.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5264 : { GREETING: "¡Buaaaa!",
             QUEST : "Me pasé toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots con aleta entró y se la llevó.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5265 : { GREETING: "¡Buaaaa!",
             QUEST : "Me pasé toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots confraternizadores entró y se la llevó.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5266 : { GREETING: "¡Buaaaa!",
             QUEST : "Me pasé toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots corporativistas entró y se la llevó.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5212 : { QUEST : "¡Oh, gracias por encontrar la carta!\aPor favor, ¿podrías entregársela al perro más bonito de todo el barrio?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No entregaste la carta, ¿verdad?",
             },
    5213 : { GREETING : "Encantado de verte.",
             QUEST : "Lo siento, pero no puedo molestarme con tu carta.\a¡Me quitaron a todos mis dibuperritos!\aTráemelos y hablaremos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡Mis pobres dibuperritos!" },
    5214 : { GREETING : "",
             LEAVING : "¡Hasta luego!",
             QUEST : "Gracias por devolverme a mis preciosidades.\aEchemos un vistazo a tu carta...\nMmmm, parece que tengo otra admiradora secreta.\aEsto pide a gritos una visita a mi querido amigo Carlos Congelado.\a¡Seguro que te cae muy bien!_where_" },
    5215 : { GREETING : "Je, je...",
             LEAVING : "Vuelve, sí, sí.",
             INCOMPLETE_PROGRESS : "Todavía quedan unos cuantos grandullones.  Vuelve cuando ya no estén.",
             QUEST : "¿Quién te envió?  No me gustan los forasteros, no...\aPero menos me gustan los bots...\aAcaba con los grandotes y ya veremos si te ayudo." },
    5216 : { QUEST : "Te dije que te vamos a ayudar.\aAsí que llévale este anillo a la chica.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡¿Sigues teniendo el anillo?!",
             COMPLETE : "¡Oh, queriiiido! ¡¡¡Gracias!!!\aAh, también tengo algo especial para ti.",
             },
    5217 : { QUEST : "Parece que a _toNpcName_ le vendría bien algo de ayuda._where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguro que hay confraternizadores por algún sitio.",
             QUEST : "¡¡¡Socorro!!! ¡¡¡Socorro!!! ¡Ya no lo aguanto más!\a¡Esos confraternizadores me están enloqueciendo!" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No pueden ser todos. ¡Sólo vi a uno!",
             QUEST : "¡Ey, gracias, pero ahora son los corporativistas!\a¡Tienes que ayudarme!" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡No, no, no, había uno justo aquí!",
             QUEST : "¡Ahora me doy cuenta de que son esos prestamistas despiadados!\a¡Creía que ibas a salvarme!" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Sabes qué? ¡Tal vez la culpa no es de los bots!\a¿Puedes pedirle a Pega Moide que me prepare una poción calmante? A lo mejor eso ayuda..._where_" },
    5222 : { LEAVING : "",
             QUEST : "¡El tal Cris Térico es todo un personaje!\a¡Voy a prepararle algo que le pondrá a tono!\aVaya, parece que me quedé sin aletas de sardina...\aPórtate bien y ve al estanque a pescarme unas cuantas.",
             INCOMPLETE_PROGRESS : "¿Ya conseguiste las aletas?", },
    5223 : { QUEST : "Bien. Gracias, cariño.\aToma, ahora llévale esto a Cris. Seguro que se calma enseguida.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vamos, llévale la poción a Cris.",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hazme el favor de acabar con los picapleitos ¿sí?",
             QUEST : "¡Oh, gracias a Dios que regresaste!\a¡¡¡Dame la poción, rápido!!!\aGlu, glu, glu...\a¡Puaj, qué mal sabía!\aPero ¿sabes qué?  Me siento mucho más tranquilo.  Ahora que puedo pensar con claridad, me doy cuenta de que...\a¡¡¡Eran los picapleitos los que me volvían loco todo el rato!!!",
             COMPLETE : "¡Es estupendo!  ¡Ahora puedo relajarme!\aSeguro que por aquí hay algo que pueda darte.  ¡Toma!" },
    5225 : { QUEST : "Desde el incidente del sándwich de nabos, Felipe el Gruñón estuvo enojado con _toNpcName_. \aA lo mejor puedes ayudar a Frigo a arreglar las cosas entre ellos._where_" },
    5226 : { QUEST : "Sí, seguro que te contaron que Felipe el gruñón está enojado conmigo...\aSolo intentaba ser amable regalándole un sándwich de nabos.\aA lo mejor puedes animarle.\aFelipe odia a los chequebots, sobre todo sus edificios. \aSi reconquistas unos cuantos edificios de chequebots, tal vez sirva de algo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Y si lo intentas con unos cuantos edificios más?", },
    5227 : { QUEST : "¡Es fantástico! Ve a contar a Felipe lo que hiciste._where_" },
    5228 : { QUEST : "¿Eso hizo?\aEse Frigo cree que puede arreglarlo todo así de fácil, ¿eh?\a¡Me rompí una muela con ese sándwich de nabos que me dio!\aQuizá si le llevas la muela al doctor Bocamaraca, él pueda arreglarla.",
             GREETING : "Brrrrr.",
             LEAVING : "Grrñññ, grññññ.",
             INCOMPLETE_PROGRESS : "¿Tú otra vez? ¡Creía que ibas a arreglarme la muela!",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela. Tardaré un poquito más.",
             QUEST : "Sí, la muela está bastante mal, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos chequebots?\aEstán asustando a mis pacientes." },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela. Tardaré un poquito más.",
             QUEST : "Sí, la muela está bastante mal, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos vendebots?\aEstán asustando a mis pacientes." },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela. Tardaré un poquito más.",
             QUEST : "Sí, la muela está bastante mal, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos abogabots?\aEstán asustando a mis pacientes." },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela. Tardaré un poquito más.",
             QUEST : "Sí, la muela está bastante mal, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos jefebots?\aEstán asustando a mis pacientes." },
    5230 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas regresado!\aDesistí de intentar arreglar la muela y, en su lugar, le fabriqué a Felipe una nueva, de oro.\aPor desgracia, un barón ladrón me la robó.\aSi te das prisa, a lo mejor consigues atraparlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya la muela?" },
    5270 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aDesistí de intentar arreglar la muela y, en su lugar, le fabriqué a Felipe una nueva, de oro.\aPor desgracia, un pez gordo me la robó.\aSi te das prisa, a lo mejor consigues atraparlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya la muela?" },
    5271 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aHe desistido de intentar arreglar la muela y, en su lugar, le fabriqué a Felipe una nueva, de oro.\aPor desgracia, un Sr. Hollywood me la robó.\aSi te das prisa, a lo mejor consigues atraparlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya la muela?" },
    5272 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aDesistí de intentar arreglar la muela y, en su lugar, le fabriqué a Felipe una nueva, de oro.\aPor desgracia, un pelucón me la robó.\aSi te das prisa, a lo mejor consigues atraparlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya la muela?" },
    5231 : { QUEST : "¡Estupendo, esa es la muela!\a¿Por qué no me haces el favor de llevársela a Felipe?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguro que Felipe está impaciente por ver su nueva muela.",
             },
    5232 : { QUEST : "Oh, gracias.\aUmmmmf\a¿Qué tal estoy, eh?\aBueno, puedes decirle a Frigo que le perdono.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Oh, me alegro muchísimo de oír eso.\aMe imaginaba que el cascarrabias de Felipe no podría seguir enojado conmigo.\aComo gesto de amistad, le preparé este sándwich de piñones.\a¿Me haces el favor de llevárselo? ",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Date prisa, por favor.  El sándwich de piñones está más rico cuando está calentito.",
             COMPLETE : "Vaya, ¿qué es esto? ¿Es para mí?\aÑam, ñam....\a¡Aaay! ¡Mi muela! ¡Ese Frigo Sabañón!\aBueno, no fue culpa tuya. Toma, llévate esto como recompensa por tu esfuerzo.",
             },
    903 : { QUEST : "Creo que estás listo para ir a ver a _toNpcName_, en Ventisca a la Vista, para tu prueba final._where_", },
    5234 : { GREETING: "",
             QUEST : "Ah, regresaste.\aAntes de empezar, tenemos que comer algo.\aTráenos un poco de queso abultado para el caldo.\aEl queso abultado sólo se puede conseguir de los bots peces gordos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguimos necesitando queso abultado." },
    5278 : { GREETING: "",
             QUEST : "Ah, regresaste.\aAntes de empezar, tenemos que comer algo.\aTráenos un poco de caviar para el caldo.\aEl caviar sólo se puede conseguir de los bots Sr. Hollywood.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguimos necesitando caviar." },
    5235 : { GREETING: "",
             QUEST : "Los hombres sencillos comen con cucharas sencillas.\aUn bot se llevó mi cuchara sencilla, así que sencillamente, no puedo comer.\aTráeme mi cuchara. Creo que un barón ladrón se la llevó.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Es sencillo: debo recuperar la cuchara." },
    5279 : { GREETING: "",
             QUEST : "Los hombres sencillos comen con cucharas sencillas.\aUn bot se llevó mi cuchara sencilla, así que no puedo comer.\aTráeme mi cuchara. Creo que un pelucón se la llevó.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Es sencillo: debo recuperar la cuchara." },
    5236 : { GREETING: "",
             QUEST : "Oh, gracias.\aSlurp, slurp...\aAaah, ahora tienes que atrapar a un sapo parlanchín. Ponte a pescar en el estanque.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el sapo parlanchín?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Todavía no conseguiste el postre.",
              QUEST : "Vaya, no cabe duda de que es un sapo parlanchín. Dámelo.\a¿Qué dices, sapo?\aAjá.\aEntiendo...\aEl sapo habló. Necesitamos un postre.\aTráenos unos cuantos cucuruchos de helado de _toNpcName_.\aPor algún motivo, al sapo le gusta el helado de judías pintas._where_", },
    5238 : { GREETING: "",
             QUEST : "Así que te envía Fredo Dedo. Siento decirte que nos quedamos sin cucuruchos de helado de judías pintas.\aVerás, un grupo de bots entró y se los llevó.\aDijeron que eran para un señor de Hollywood o algo así.\aTe agradecería mucho que los recuperases.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya los cucuruchos de helado?" },
    5280 : { GREETING: "",
             QUEST : "Así que te envía Fredo Dedo. Siento decirte que nos quedamos sin cucuruchos de helado de judías pintas.\aVerás, un grupo de bots entró y se los llevó.\aDijeron que eran para el pez gordo o algo así.\aTe agradecería mucho que los recuperases.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste ya los cucuruchos de helado?" },
    5239 : { QUEST : "¡Gracias por recuperar los cucuruchos de helado!\aAquí tienes uno para Fredo Dedo.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Más vale que le lleves el helado a Fredo Dedo antes de que se derrita.", },
    5240 : { GREETING: "",
             QUEST : "Muy bien. Aquí tienes, sapo...\aSlurp, slurp...\aMuy bien, estamos casi listos.\aSi pudieses traerme un poco de talco para secarme las manos...\aCreo que los bots pelucones llevan a veces polvos de talco en la peluca.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el talco?" },
    5281 : { GREETING: "",
             QUEST : "Muy bien. Aquí tienes, sapo...\aSlurp, slurp...\aMuy bien, estamos casi listos.\aSi pudieses traerme un poco de talco para secarme las manos...\aCreo que los bots Sr. Hollywood llevan a veces polvos de talco para empolvarse la nariz.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el talco?" },
    5241 : { QUEST : "Está bien.\aComo dije en su día, para lanzar bien una tarta, no se debe usar la mano...\a... sino el alma.\aNo sé qué significa eso, así que me sentaré a contemplar cómo reconquistas edificios.\aVuelve cuando hayas terminado tu tarea.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu tarea todavía no terminó.", },
    5242 : { GREETING: "",
             QUEST : "Aunque sigo sin saber de qué hablo, no cabe duda de que eres de gran valor.\aTe asigno una tarea final...\aAl sapo parlanchín le gustaría tener una novia.\aBusca otro sapo parlanchín. El sapo ha hablado.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el otro sapo parlanchín?",
             COMPLETE : "¡Uau! Estoy cansado de todo este esfuerzo. Voy a descansar.\aToma, ten tu recompensa y vete." },

    5243 : { QUEST : "Pedro Glaciares está empezando a apestar la calle.\a¿Puedes convencerle de que se dé una ducha?_where_" },
    5244 : { GREETING: "",
             QUEST : "Sí, supongo que suelo sudar bastante.\aMmm, a lo mejor si pudiese arreglar la tubería que gotea en mi ducha...\aSupongo que un engranaje de esos bots diminutos me servirá.\aVe a buscar un engranaje de un microgerente y lo intentaremos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el engranaje ese que me ibas a traer?" },
    5245 : { GREETING: "",
             QUEST : "Sí, parece que eso funcionó.\aPero cuando me ducho me siento solo...\a¿Podrías ir a pescarme un patito de goma para que me haga compañía?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el patito?" },
    5246 : { QUEST : "El patito es estupendo, pero...\atodos esos edificios alrededor me ponen nervioso.\aMe sentiría mucho más relajado si hubiese menos edificios cerca.",
             LEAVING : "",
             COMPLETE : "Bueno, me voy a dar una ducha. Toma, esto es para ti.",
             INCOMPLETE_PROGRESS : "Siguen preocupándome los edificios.", },
    5251 : { QUEST : "Creo que Pago Gelado va a dar un recital esta noche.\aMe dijeron que el material del concierto le está dando problemas._where_" },
    5252 : { GREETING: "",
             QUEST : "¡Ah, sí! Pues claro que me viene bien algo de ayuda.\a"+TheCogs+" vinieron y me robaron todo el equipo mientras descargaba la furgoneta.\a¿Puedes echarme una mano recuperando el micrófono?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Oye, compañero, no puedo cantar sin un micrófono." },
    5253 : { GREETING: "",
             QUEST : "¡Sí, ese es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\alo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo llevó uno de esos corporativistas.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el teclado?" },
    5273 : { GREETING: "",
             QUEST : "¡Sí, ese es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\alo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo llevó uno de esos confraternizadores.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el teclado?" },
    5274 : { GREETING: "",
             QUEST : "¡Sí, ese es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\alo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo llevó uno de esos prestamistas despiadados.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el teclado?" },
    5275 : { GREETING: "",
             QUEST : "¡Sí, ese es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\alo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo llevó uno de esos picapleitos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Encontraste el teclado?" },
    5254 : { GREETING: "",
             QUEST : "¡Muy bien! Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que acabaron en manos de un tal Sr. Hollywood.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!! Ahora sí que estoy listo.\a¡Hola, "+lTheBrrrgh+"!\a¿Eh? ¿Dónde está la gente?\aBueno, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5282 : { GREETING: "",
             QUEST : "¡Muy bien! Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que acabaron en manos de un pez gordo.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!! Ahora sí que estoy listo.\a¡Hola, "+lTheBrrrgh+"!\a¿Eh? ¿Dónde está la gente?\aBueno, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5283 : { GREETING: "",
             QUEST : "¡Muy bien! Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que acabaron en manos de un barón ladrón.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!! Ahora sí que estoy listo.\a¡Hola, "+lTheBrrrgh+"!\a¿Eh? ¿Dónde está la gente?\aBueno, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5284 : { GREETING: "",
             QUEST : "¡Muy bien! Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que acabaron en manos de un pelucón.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!! Ahora sí que estoy listo.\a¡Hola, "+lTheBrrrgh+"!\a¿Eh? ¿Dónde está la gente?\aBueno, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },

    5255 : { QUEST : "Creo que te vendrían bien más puntos de risa.\aQuizá puedas hacer un trato con _toNpcName_.\aNo te olvides de ponerlo por escrito..._where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un trato es un trato.",
             QUEST : "Así que quieres puntos de risa, ¿eh?\a¡Te propongo un trato!\aSi te ocupas de unos cuantos jefebots...\aYo te recompensaré por ello." },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Un trato es un trato.",
             QUEST : "Así que quieres puntos de risa, ¿eh?\a¡Te propongo un trato!\aSi te ocupas de unos cuantos abogabots...\aYo te recompensaré por ello." },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Bueno, pero estoy seguro de que te dije que te ocupases de unos cuantos abogabots.\aBueno, si tú lo dices... Pero me debes una.",
             INCOMPLETE_PROGRESS : "Creo que todavía no terminaste.",
             QUEST : "¿Dices que terminaste? ¿Derrotaste a todos los bots?\aMe entenderías mal; nuestro trato se refería a los vendebots.\aEstoy segurísimo de que te dije que te ocupases de unos cuantos vendebots." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Bueno, pero estoy seguro de que te dije que te ocupases de unos cuantos abogabots.\aBueno, si tú lo dices... Pero me debes una.",
             INCOMPLETE_PROGRESS : "Creo que todavía no terminaste.",
             QUEST : "¿Dices que terminaste? ¿Derrotaste a todos los bots?\aMe entenderías mal, nuestro trato se refería a los chequebots.\aEstoy segurísimo de que te dije que te ocupases de unos cuantos chequebots." },

    # Eddie the will give you laff point for helping him
    5301 : { QUEST : "No puedo ayudarte con puntos de risa, pero quizás _toNpcName_ haga un trato contigo.\aAunque es un poco temperamental..._where_" },
    5302 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "¡¿Que yo te dije... qué?!\a¡Muchas gracas! ¡Toma tu punto de risa!",
             INCOMPLETE_PROGRESS : "¡Hola!\a¿Qué haces aquí otra vez?",
             QUEST : "¿Un punto de risa? ¡No lo creo!\aClaro, pero solo si antes quitas de en medio a unos cuantos de estos abogabots tan molestos." },

    # Johnny Cashmere will knit you a large bag if...
    5303 : { QUEST : lTheBrrrgh+" se está aliando con bots muy peligrosos.\aYo en tu lugar, llevaría más bromas.\aDicen que _toNpcName_ puede conseguirte una bolsa grande si estás dispuesto a hacer el trabajo._where_" },
    5304 : { GREETING: "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tiene que haber muchos abogabots ahí fuera.\a¡Vamos!" ,
             QUEST : "¿Una bolsa más grande?\aProblemente te pueda conseguir una.\aPero voy a necesitar hilo.\aUnos abogabots se llevaron el mío ayer por la mañana." },
    5305 : { GREETING : "¡Ah, del barco!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Ve a buscar más bots.\aEste color todavía no se filtró.",
             QUEST : "¡Qué hilo tan bueno!\aAunque el color no sea precisamente mi favorito.\aTe diré una cosa...\aSal y derrota a algunos de esos bots tan duros...\aY yo me pondré a teñir el hilo." },
    5306 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tienen que estar por aquí abajo...",
             QUEST : "Bueno, el hilo ya está teñido. Pero tenemos un pequeño problema.\aNo encuentro mis agujas de punto.\aLa última vez que las vi estaban en el estanque."  },
    5307 : { GREETING : "",
             LEAVING : "¡Será un placer!",
             INCOMPLETE_PROGRESS : "¡Roma no se construyó en un día!" ,
             QUEST : "Esas son mis agujas.\aMientras hilo, ¿por qué no vas a eliminar algunos de esos edificios grandes?",
             COMPLETE : "¡Buen trabajo!\aY hablando de buen trabajo...\a¡Toma tu nueva bolsa!" },

    # March Harry can also give you max quest = 4.
    5308 : { GREETING : "",
             LEAVING : "",
             QUEST : "Dicen que _toNpcName_ tiene problemas legales.\a¿Puedes pasarte a ver de qué se trata?_where_"  },
    5309 : { GREETING : "Me alegro de que estés aquí...",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡Date prisa! ¡Las calles están llenas!",
             QUEST : "Los abogabots se hicieron con todo ahí fuera.\aMe temo que me van a llevar a juicio.\a¿Crees que podrías ayudar a sacarlos de esta calle?"  },
    5310 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Creo que los oigo como vienen a por mí...",
             QUEST : "Gracias. Me siento un poco mejor.\a Pero hay una cosa más...\a¿Puedes ir a ver a _toNpcName_ y conseguirme una coartada?_where_"  },
    5311 : { GREETING : "¡¡¡UAAAAA!!!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡Si no lo encuentras, no puedo ayudarle!",
             QUEST : "¡¿Coartada?! ¡Qué idea tan buena!\a¡Mejor que sean dos!\aSeguro que el picapleitos tiene unas cuantas..."  },
    5312 : { GREETING : "¡Por fin!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "",
             COMPLETE : "¡Uf! Qué alivio contar con esto.\aToma tu recompensa...",
             QUEST : "¡Fantástico! ¡Será mejor que se las lleves a _toNpcName_!"  },

    # Powers Erge, though forgetful, will give you an LP boost
    # if you'll defeat some Cogs for him
    6201 : { QUEST : "Apagona Plómez necesita ayuda. ¿Puedes pasarte a echarle una mano?_where_",
             },
    6202 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Oh, un cliente! ¡Estupendo! ¿Qué puedo hacer por ti?\a¿Qué quieres decir con eso de qué puedes hacer por mí? ¡OH! Si no eres un cliente.\aAhora recuerdo. Viniste a ayudar con esos horribles bots.\aBueno, me vendría muy bien la ayuda, aunque no seas un cliente.\aSi limpias un poco las calles, tengo una cosita para ti.",
             INCOMPLETE_PROGRESS : "Si no quieres electricidad, no puedo ayudarte hasta que derrotes a esos bots.",
             COMPLETE : "Buen trabajo con esos bots, _avName_.\a¿Seguro que no quieres un poco de electricidad? Podría resultarte útil....\a¿No? OK, como quieras.\a¿Eh? Oh sí, ya recuerdo. Toma. Seguro que te resulta útil con esos bots tan horribles.\a¡Sigue así!",
             },

    # Susan Siesta wants to get rich but the Cogs are interfering.
    # Take out some Cog buildings and she'll give you the small backpack
    6206 : { QUEST : "Bueno, _avName_, en este momento no tengo nada para ti.\a¡Espera! Creo que Susana Siesta buscaba ayuda. ¿Por qué no vas a verla?_where_",
             },
    6207 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Nunca haré plata con todos esos malditos bots espantándome clientes!\aTienes que ayudarme, _avName_.\aElimina algunos edificios bot por el bien del vecindario y yo contribuiré a tu riqueza.",
             INCOMPLETE_PROGRESS : "¡Pobre de mí! ¿No puedes deshacerte de esos edificios?",
             COMPLETE : "¡Voy a hacer mucho dinero! ¡Ahora lo veo!\a¡Pasaré todo mi tiempo pescando. Deja que enriquezca un poco tu vida.\a¡Toma!",
             },

    # Lawful Linda is fixing her answering machine.
    # Help her & she'll give you a 2LP reward.
    6211 : { QUEST : "¡Eh, _avName_! Dicen que Linda Legal te buscaba.\aDeberías hacerle una visita._where_",
             },
    6212 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Hola! ¡Qué alegría verte!\aEn mi tiempo libre, estoy trabajando con esta contestadora, pero me faltan un par de piezas.\aNecesito tres barras más y los de agarrados funcionan muy bien.\a¿Podías conseguirme algunos?",
             INCOMPLETE_PROGRESS : "¿Todavía estás intentando encontrar las barras?",
             },
    6213 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, esto me será muy útil.\aQué raro, seguro que tenía una correa de transmisión por aquí, pero no la encuentro.\a¿Podrías conseguir una de un monedero? ¡Gracias!",
             INCOMPLETE : "Bueno, no te puedo ayudar hasta que consiga la correa de transmisión.",
             },
    6214 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, eso es. Ahora irá como la seda.\a¿Dónde está mi pinza? No puedo apretar esto sin pinza.\aA lo mejor las tenazas de un cacomatraco servirán.\aSi las encuentras, te daré algo para ayudarte con esos bots.",
             INCOMPLETE_PROGRESS : "¿Todavía no tienes las tenazas? Sigue buscando.",
             COMPLETE : "¡Genial! Ahora solo tengo que apretar esto.\aParece que ya funciona. ¡El negocio vuelve a funcionar!\aBueno, excepto que no tenemos teléfono. De todas formas, gracias por tu ayuda.\aCreo que esto te ayudará con esos bots. ¡Suerte!",
             },

    # Scratch Rocco's back and he'll scratch yours.
    # In fact, he'll give you a 3 LP bonus.
    6221 : { QUEST : "Dicen que Tronco Sópez buscaba ayuda. Ve a ver qué puedes hacer por él._where_",
             },
    6222 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Eh! Viniste al lugar perfesto. No me van mu' bien las cosas.\aSí, necesito un poco d’ayuda con esos bots. Siempre vienen y me menean pá aquí y pá allá.\aSi pués quitarme a unos cuantos de esos jefebots, te recompensaré.",
             INCOMPLETE_PROGRESS : "Eh, _avName_, ¿qué pasa contigo?\aTienes que perserguí a esos jefebots. Tenemos un trato, ¿t'acuerdas?\aTronco Sópez es un tipo de honor.",
             COMPLETE : "¡Eh, _avName_! Estás en mi lista de güenos.\aLos jefebots esos ya no son tan pesaos, ¿eh?\a¡Toma! Esto te vendrá que ni pintao. ¡Y no te metas en líos, diantre!",
             },

    # Nat & PJ will get you acquainted with the new 
    # HQ. And they'll give you your first suit part
    6231 : { QUEST : "Nat, en el Centro Pijama, oyó rumores sobre un Cuartel General chequebot.\aVete para allá a ver si puedes ayudarle._where_",
             },
    6232 : { GREETING : "",
             LEAVING : "",
             QUEST : "Tengo la sensación de que pasa algo extraño.\aQuizás sean las pulgas, pero bueno, algo pasa.\a¡Todos estos chequebots!\aCreo que abrieron otro cuartel general justo a las afueras de Centro Pijama.\aP.J. conoce la zona.\aVe a ver a _toNpcName_ _where_ Pregúntale si sabe algo.",
             INCOMPLETE_PROGRESS : "¿Todavía no fuiste a ver a P.J.? ¿A qué esperas?\a¡Oh, malditas pulgas!",
             },
    6233 : { GREETING : "",
             LEAVING : "",
             QUEST : "Eh, _avName_, ¿a dónde vas?\a¿Al cuartel general de los chequebots? Yo no vi nada.\a¿Podrías ir al final de Centro Pijama a ver si es cierto?\aBusca chequebots en su cuartel general, derrota a unos cuantos y regresa a contármelo.",
             INCOMPLETE_PROGRESS : "¿Ya encontraste el cuartel general? Para poder investigarlo, tendrás que derrotar a unos cuantos chequebots.", 
             },
    6234 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡¿Qué?! ¿Es VERDAD que existe un cuartel general de chequebot?\a¡Ve inmediatamente a contárselo a Nat!\a¿Quién le iba a decir que tendría un cuartel general de bots tan cerca?",
             INCOMPLETE_PROGRESS : "¿Qué dijo Natsay? ¿Todavía no le viste?",
             },
    6235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Me muero de ganas por saber lo que dijo P.J.\aUmm... ¡necesitamos más información sobre ese asunto de los bots, pero todavía tengo que deshacerme de estas pulgas!\a¡Ya sé! ¡TÚ puedes ir a investigar!\a¡Ve al cuartel general, derrota a unos cuantos chequebots, encuentra unos planos y regresa!",
             INCOMPLETE_PROGRESS : "¿Todavía no tienes los planos? ¡Sigue buscando!\a¡Tienen que tener algunos planos!",
             COMPLETE : "¿Ya tienes los planos?\a¡Fantástico! A ver que dicen.\aYa veo... los chequebots construyeron una fabrica de monedas para fabricar botdólares.\aDebe de estar llena de chequebots. Tenemos que investigar más.\aQuizás, si fueras disfrazado... ¡Espera! Creo que tengo parte de un traje bot por alguna parte...\a¡Ya lo tengo! ¿Por qué no aceptas esto, por las molestias? ¡Y gracias de nuevo por tu ayuda!",
             },

    # The Countess can't concentrate on counting her sheep with all 
    # these Cogs around. Clean up a bit and she'll reward you handsomely.
    # Reward: MaxMoneyReward 705 - 150 jellybeans
    6241 : { QUEST : "¡La condesa te estuvo buscando por todas partes! Por favor, ve a visitarla para que deje de llamar._where_",
             },
    6242 : { GREETING : "",
             LEAVING : "",
             QUEST : "_avName_, ¡cuento con tu ayuda!\aVerás, estos bots están haciendo tanto ruido que no me puedo concentrar.\a¡Todo el rato pierdo la cuenta de mis ovejas!\a¡Si consigues reducir el ruido, yo también te ayudaré! ¡Cuenta con ello!\aEeh... ¿por dónde iba? Ah, sí: ciento treinta y seis, ciento treinta y siete...",
             INCOMPLETE_PROGRESS : "Cuatrocientos cuarenta y dos... cuatrocientos cuarenta y tres...\a¿Qué? ¿Ya estás de vuelta? ¡Pero si todavía hay mucho ruido!\aOh no, volví a desconcentrarme.\a Uno... dos... tres....",
             COMPLETE : "Quinientos noventa y tres... quinientos noventa y cuatro...\a¿Hola? Oh, ¡sabía que podía contar contigo! Ahora está todo mucho más tranquilo.\aToma, por todos esos contables.\a¿Números? ¡Oh, ahora tengo que volver a empezar desde el principio! Uno... dos...",
             },

    # Zari needs you to run some errands for her and maybe
    # wipe out some Cogs along the way. She'll make it worthwhile
    # though, she'll give you 4 LP if you run the gauntlet.
    6251 : { QUEST : "La pobre Zari tiene el vehículo estropeado y ahora no puede hacer entregas a sus clientes. Le vendría bien un poco de ayuda._where_",
             },
    6252 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, hola, _avName_. ¿Viniste a ayudarme con las entregas?\a¡Fantástico! Con este trasto estropeado es difícil moverse por ahí.\aDéjame ver... ok, esto parece fácil. Cowboy Jorge encargó un banjo la semana pasada.\a¿Podrías llevárselo? _where_",
             INCOMPLETE_PROGRESS : "¡Oh, hola! ¿Olvidaste algo? Cowboy Jorge está esperando su banjo.",
             },
    6253 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Mi banjo! ¡Por fin! Estoy deseando empezar a tocar.\aDale las gracias a Zari de mi parte, ¿quieres?",
             INCOMPLETE_PROGRESS : "Gracias otra vez por el banjo. ¿Zari no tiene más entregas para ti?",
             },
    6254 : { GREETING : "",
             LEAVING : "",
             QUEST : "Qué rápido. ¿Qué es lo siguiente de mi lista?\aAh, sí. El Maestro Marcos encargó una pulidora de hielo. Qué tipo tan estrafalario.\a¿Podrías llevarle esto, por favor?_where_",
             INCOMPLETE_PROGRESS : "Esa pulidora de hielo es para el Maestro Marcos._where_",
             },
    6255 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Bien! ¡La pulidora de hielo que encargué!\aSi no hubiera tantos bots por ahí, tendría tiempo de usarla.\aVamos, sé bueno y encárgate de unos cuantos de estos chequebots, ¿quieres?",
             INCOMPLETE_PROGRESS : "Esos chequebots son duros, ¿eh? Me va a ser difícil probar la pulidora de hielo.",
             },
    6256 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Extupendo! Ya puedo probar mi pulidora de hielo.\aDile a Zari que la semana que viene iré a hacer mi siguiente encargo.",
             INCOMPLETE_PROGRESS : "Eso es todo por ahora. ¿No te está esperando Zari?"
             },
    6257 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Quedó satisfecho el Maestro Marcos con su pulidora de hielo? Bien.\a¿Quién va ahora? Ah, Zen Glen encargó un esterilla cebra.\a¡Aquí está! ¿Podrías pasar por su casa, por favor?_where_",
             INCOMPLETE_PROGRESS : "Creo que Zen Glen necesita esa esterilla para meditar.",
             },
    6258 : { GREETING : "",
             LEAVING : "",
             QUEST : "Ah, por fin, mi esterilla. Ahora ya puedo meditar.\aPero, ¿quién se puede concentrar con todo ese ruido? ¡Tantos bots!\aYa que estás aquí, quizás puedas encargarte de unos cuantos...\aAsí podré usar mi esterilla tranquilamente.",
             INCOMPLETE_PROGRESS : "Esos bots todavía hacen mucho ruido. ¿Quién se puede concentrar así?",
             },
    6259 : { GREETING : "",
             LEAVING : "",
             QUEST : "Por fin, un poco de calma. Gracias, _avName_.\aPor favor, dile a Zari que estoy feliz. Estoy en paz. OM....",
             INCOMPLETE_PROGRESS : "Zari llamó, te andaba buscando. Deberías ir a ver qué necesita.",
             },
    6260 : { GREETING : "",
             LEAVING : "",
             QUEST : "Me alegra escuchar que Zen Glen está contento con su esterilla cebra.\aOh, esas zinnias acaban de entrar para Rosa Pétalo.\aYa que eres tan bueno para las entregas, quizás no te importaría ir a llevárselas..._where_",
             INCOMPLETE_PROGRESS : "Si no llevas las zinnias pronto, empezarán a marchitarse.",
             },
    6261 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Qué zinnias tan lindas! Zari tiene buen género.\aOh, bueno, TÚ eres quien hace las entregas, _avName_. ¡Por favor, dale las gracias a Zari de mi parte!",
             INCOMPLETE_PROGRESS : "¡No olvides darle las gracias a Zari por las zinnias!",
             },
    6262 : { GREETING : "",
             LEAVING : "",
             QUEST : "Hola otra vez, _avName_. Eres rápido.\aVeamos... ¿qué es lo siguiente en mi lista de entregas? Discos de Zydeco para Pluma Oca._where_",
             INCOMPLETE_PROGRESS : "Seguro que Pluma Oca está esperando esos discos de Zydeco.",
             },
    6263 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Discos de Zydeco? No recuerdo haber pedido discos de Zydeco.\aOh, seguro que los encargó el Marqués de la Nana._where_",
             INCOMPLETE_PROGRESS : "No, esos discos de Zydeco son para el Marqués de la Nana._where_",
             },
    6264 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Por fin, mis discos de Zydeco! Pensé que Zari se había olvidado.\a¿Podrías llevarle este calabacín? Encontrará a alguien que quiera uno. ¡Gracias!",
             INCOMPLETE_PROGRESS : "Oh, ya tengo muchos calabacines. Llévale ese a Zari.",
             },
    6265 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Calabacín? Umm. Bueno, alguien lo querrá, estoy segura.\aOk, la lista está casi completa. Sólo falta una entrega.\aHiberno Cuandoquiero encargó un traje de remo._where_",
             INCOMPLETE_PROGRESS : "Si no le entregas ese traje de remo a Hiberno Cuandoquiero,\a se arrugará todo.",
             },
    6266 : { GREETING : "",
             LEAVING : "",
             QUEST : "Érase una vez... ¡oh! No viniste por el cuento, ¿verdad?\a¿Traes mi traje de remo? ¡Estupendo! Uau, es muy lindo.\aEh, ¿podrías darle a Zari un mensaje de mi parte? Necesito gemelos de zircón para el traje. ¡Gracias!",
             INCOMPLETE_PROGRESS : "¿Le diste mi mensaje a Zari?",
             COMPLETE : "Gemelos de zircón, ¿eh? Bueno, veré qué puedo hacer por él.\aFuiste todo un modelo de atenciones, y no puedo dejarte marchar sin nada.\a¡Toma, una GRAN ayuda para acabar con esos bots!",
             },

    # Drowsy Dave will give you teleport access to DL
    # if he can stay awake long enough for you to finish.
    6271 : { QUEST : "David Modorra tiene problemas y quizás tú puedas ayudarle. ¿Por qué no pasas por su tienda?_where_",
             },
    6272 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Qué? ¿Eh? Oh, me quedé dormido.\aEsos edificios bot están llenos de máquinas y el ruido me da mucho sueño.\aTodo el día están con ese ronroneo y...\a¿Eh? Oh, sí, claro. Si pudieras deshacerte de algunos de esos edificios bot, podría mantenerme despierto.",
             INCOMPLETE_PROGRESS : "Zzzzz... ¿eh? Ah, eres tú, _avName_.\a¿Ya regresaste? Estaba echando una siesta.\aVuelve cuando termines con esos edificios.",
             COMPLETE : "¿Qué? Me quedé dormido un minuto.\aAhora que esos edificios bot ya no están, por fin puedo relajarme.\aGracias a ti, _avName_.\a¡Hasta luego! Creo que voy a echar una siesta.",
             },

    # Teddy Blair has a piece of a cog suit to give you if you will
    # clear out some cogs. Of course, his ear plugs make it tough. 
    6281 : { QUEST : "Ve a hacerle una visita a Teddy Blair. Tiene un trabajo para ti._where_",
             },
    6282 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Qué dijiste? Pero no, cómo voy a tener un tabaco para ti.\a¡Oh, un trabajo! ¿Por qué no lo dijiste antes? Tienes que hablar más alto.\aCon esos bots, resulta difícil hibernar.  Si me ayudas a hacer que Sueñolandia sea un lugar más tranquilo,\ate daré una cosa.",
             INCOMPLETE_PROGRESS: "¿Derrotaste a los botas? ¿Qué botas?\a¡Ah, los bots! ¿Por qué no lo dijiste antes?\aUmm, todavía hay mucho ruido. ¿Qué te parece si derrotas a unos cuantos más?",
             COMPLETE : "¿Te divertiste? ¿Eh? ¡Oh!\a¡Terminaste! Fantástico. Eres muy amable.\aEncontré esto en el galpón, pero a mí no me sirve para nada.\aA lo mejor a ti te resulta útil. ¡Hasta otra, _avName_!",
             },    
    
    # William Teller needs help! Those darn Cashbots swiped his 3
    # money bags to use in the Mint! Retrieve them and he'll give you
    # another cog Suit piece.
    6291 : { QUEST : "Los bots entraron en el Banco Tupido Velo! ¡Ve a ver a Mostra Dor a ver si puedes ayudar.",
             },
    6292 : { QUEST : "¡Esos malditos chequebots! ¡Me robaron las lámparas de lectura!\aNecesito recuperarlas inmediatamente. ¿Puedes ir a buscarlas?\aSi recuperas mis lámparas, quizás pueda hacer algo para que veas al director financiero.\a¡Apresúrate!",
             INCOMPLETE_PROGRESS : "Necesito recuperar las lámparas. ¡Sigue buscando!",
             COMPLETE : "¡Ya regresaste! ¡Y con mis lámparas!\aNo sé cómo agradecértelo, pero sí sé que puedo darte esto.",
             },
    
    # Help Nina Nightlight get a bed in stock -
    # she'll give you a suit part
    7201 : { QUEST : "Vela Zascandil te andaba buscando, _avName_. Necesita ayuda._where_",
             },
    7202 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Oh! Cuánto me alegro de verte, _avName_. ¡Me vendría bien un poco de ayuda!\aEsos malditos bots no permiten que lleguen los muchachos del reparto y no me quedan camas en stock.\a¿Podrías ir a ver a Juanjo Manitas y traerme una cama?_where_ ",
             INCOMPLETE_PROGRESS : "¿Juanjo tenía camas? Estaba segura de que tendría una.",
             COMPLETE : "",
             },
    7203 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Una cama? Claro, ésta está lista para salir.\aLlévasela de mi parte, ¿tienes madera de transportista? ¿Entiendes?\a¡\"MADERA\" de transportista! ¡Je je!\aMuy gracioso. ¿No? Bueno, llévasela de todas formas, por favor.",
             INCOMPLETE_PROGRESS : "¿Le gustó la cama a Vela?",
             COMPLETE : "",
             },
    7204 : { GREETING : "",
             LEAVING : "",
             QUEST : "Esta cama no me sirve. Es demasiado básica.\aVe a ver si tiene algo más sofisticado, ¿ok?\aSeguro que no te lleva más de un minuto.",
             INCOMPLETE_PROGRESS : "Seguro que Juanjo tiene una cama más sofisticada.",
             COMPLETE : "",
             },
    7205 : { GREETING : "",
             LEAVING : "",
             QUEST : "No acertamos con esa cama, ¿eh? Tengo aquí una que servirá.\aPero hay un pequeño problema: primero hay que armarla.\aMientras yo lo arreglo con el martillo, ¿puedes deshacerte de algunos de esos bots de ahí fuera?\aEsos horribles bots están haciendo de las suyas.\aVuelve cuando termines y la cama estará lista.",
             INCOMPLETE_PROGRESS : "Todavía no terminé con la cama.\aCuando acabes con los bots, estará preparada.",
             COMPLETE : "",
             },
    7206 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Eh, _avName_!\aHiciste un gran trabajo con esos bots.\aLa cama está lista. ¿Podrías entregarla de mi parte?\aAhora que no están los bots, seguro que el negocio es un éxito.",
             INCOMPLETE_PROGRESS : "Creo que Vela está esperando la cama.",
             COMPLETE : "¡Qué cama tan linda!\aAhora, mis clientes estarán contentos. Gracias, _avName_.\aEsto quizás te resulte útil. Alguien se lo olvidó aquí.",
             },
    7209 : { QUEST : "Ve a ver a Luna Miel. Necesita ayuda._where_",
             },
    7210 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Oh! Cuánto me alegro de verte, _avName_. ¡Necesito ayuda!\aHace mucho tiempo que no consigo hacer mi cura de belleza y sueño. Verás, esos bots me robaron la colcha.\a¿Podrías ir a ver si Vito tiene algo en azul?_where_",
             INCOMPLETE_PROGRESS : "¿Tenía Vito una colcha azul?",
             COMPLETE : "",
             },
    7211 : { GREETING : "",
             LEAVING : "",
             QUEST : "Así que Luna quiere una colcha, ¿eh?\a¿De qué color? ¡¿AZUL?!\aTendré que fabricársela especialmente. Todo lo que tengo es rojo.\aTe diré lo que haremos... si te encargas de algunos de esos bots de ahí fuera, yo le fabricaré una colcha azul especial.\aColchas azules... ¿Con qué me saldrán luego?",
             INCOMPLETE_PROGRESS : "Todavía estoy trabajando en la colcha, _avName_. ¡Sigue con los bots!",
             COMPLETE : "",
             },
    7212 : { GREETING : "",
             LEAVING : "",
             QUEST : "Me alegra volver a verte. ¡Tengo algo para ti!\aToma la colcha, es azul. Le encantará.",
             INCOMPLETE_PROGRESS : "¿Le gustó la colcha a Luna?",
             COMPLETE : "",
             },
    7213 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Mi colcha? No, no es lo que quería.\a¡Es a CUADROS! ¿Cómo va alguien a dormir con un diseño tan llamativo?\aTendrás que devolverla y traerme otra.\aSeguro que tiene más.",
             INCOMPLETE_PROGRESS : "Me niego a aceptar una colcha a cuadros. Ve a ver qué puede hacer Vito.",
             COMPLETE : "",
             },
    7214 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Qué? ¿Que no le gustan los CUADROS?\aUmm... veamos qué tenemos aquí.\aEsto me tomará un poco de tiempo. ¿Por qué no vas y te encargas de unos cuantos bots mientras busco otra cosa?\aCuando vuelvas, tendré algo para ti.",
             INCOMPLETE_PROGRESS : "Todavía estoy buscando otra colcha. ¿Qué tal con los bots?",
             COMPLETE : "",
             },
    7215 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Buen trabajo con los bots!\aAquí tienes, es azul y no lleva cuadros.\aEspero que le guste el cachemir.\aLlévale la colcha a Luna.",
             INCOMPLETE_PROGRESS : "Es todo lo que tengo en estos momentos.\aPor favor, llévale esa colcha a Luna.",
             COMPLETE : "¡Oh! ¡Qué lindo! El cachemir me encanta.\a¡Y ahora, mi cura de belleza y sueño! Hasta otra, _avName_.\a¿Qué? ¿Sigues aquí? ¿No ves que estoy intentando dormir?\aToma, llévate esto y déjame descansar. ¡Debo de estar horrorosa!",
             },
 
    7218 : { QUEST : "A Dafne Marmota le vendría bien una ayudita._where_",
             },
    7219 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, _avName_, ¡me alegro de verte! Esos bots se llevaron mis almohadas.\a¿Puedes ir a ver si Tex tiene alguna?_where_\aEstoy segura de que me podrá ayudar.",
             INCOMPLETE_PROGRESS : "¿Tenía Tex alguna almohada? ",
             COMPLETE : "",
             },
    7220 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ah, del barco! Dafne necesita almohadas, ¿eh? Bueno, has venido al lugar perfecto, marinero.\aAquí hay más almohadas que pinchos tiene un cactus.\aToma, _avName_. Llévaselas a Dafne y salúdala de mi parte.\aEs un placer ayudar a una señorita.",
             INCOMPLETE_PROGRESS : "¿Las almohadas eran lo bastante mullidas para la dama?",
             COMPLETE : "",
             },
    7221 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Tienes las almohadas! ¡Fantástico!\a¡Eh, espera un momento! Estas almohadas son demasiado mullidas.\aDemasiado blandas para mí. Necesito almohadas más duras.\aDevuélvele estas a Tex a ver qué más tiene. Gracias.",
             INCOMPLETE_PROGRESS : "¡No! Demasiado blandas. Dile a Tex que te dé otras almohadas.",
             COMPLETE : "",
             },
    7222 : { GREETING : "",
             LEAVING : "",
             QUEST : "Demasiado blandas, ¿eh? Bueno, veamos qué tenemos aquí...\aUmm... yo tenía un lote entero de almohadas duras. ¿Dónde estarán?\a¡Oh! Ya lo recuerdo. Iba a devolverlas, así que estarán en el almacén.\a¿Qué tal si tú destruyes algunos de esos edificios bot de ahí fuera mientras las saco, marinero?",
             INCOMPLETE_PROGRESS : "Los edificios bot son duros, pero estas almohadas no.\aSeguiré buscando.",
             COMPLETE : "",
             },
    7223 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Ya regresaste? Bueno, perfecto. Encontré las almohadas que Dafne quería.\aLlévaselas, ¡son tan duras que podrían usarse para picar almendras!",
             INCOMPLETE_PROGRESS : "Sí, estas almohadas son durísimas. Espero que a Dafne le gusten.",
             COMPLETE : "Sabía que Tex tendría almohadas más duras.\aOh sí, son perfectas. Duras y cómodas.\a¿Te sirve de algo una pieza de traje bot? Bueno, llévatela por si acaso.",
             },
 
    # Sandy Sandman lost her pajamas but Big Mama
    # and Cat can help her out. If you hang in there,
    # you'll get another Cog Suit part.
    7226 : { QUEST : "Ve a visitar a Sandra Salamandra. Perdió su pijama._where_",
             },
    7227 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡No tengo pijama! ¡Desapareció!\a¿Qué voy a hacer? ¡Oh! ¡Ya lo sé!\aVe a ver a Plúmbea Triz. Seguro que tiene un pijama para mí._where_",
             INCOMPLETE_PROGRESS : "¿Tenía Plúmbea Triz pijamas?",
             COMPLETE : "",
             },
    7228 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Eh, pequeño dibu! Plúmbea Triz tiene los mejores pijamas de todas las Bahamas.\aOh, algo para Sandra Salamandra, ¿eh? Veamos qué tenemos por aquí.\aAquí hay algo. ¡Un modelo con mucho estilo!\a¿Podrías ir a llevárselo de mi parte? Ahora no puedo dejar la tienda.\aGracias, _avName_. ¡Nos vemos!",
             INCOMPLETE_PROGRESS : "Tienes que llevarle este pijama a Sandra._where_",
             COMPLETE : "",
             },
    7229 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Plúmbea Triz me envió esto? Oh...\a¿Es que no tiene pijamas con pies?\aYo siempre uso pijamas con pies. ¿No lo hace así todo el mundo?\aDevuélvelo y dile que busque unos con pies.",
             INCOMPLETE_PROGRESS : "Mi pijama tiene que tener pies. Ve a ver qué puede hacer Plúmbea Triz.",
             COMPLETE : "",
             },
    7230 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Pies? Déjame pensar...\a¡Espera! ¡Tengo uno perfecto!\a¡Taráaan! Pijama con pies. Un lindo pijama azul con pies. De los mejores de la isla.\aLlévaselo, por favor. ¡Gracias!",
             INCOMPLETE_PROGRESS : "¿Le gustó a Sandra el pijama con pies?",
             COMPLETE : "",
             },
    7231 : { GREETING : "",
             LEAVING : "",
             QUEST : "Pues sí, estos tienen pies, ¡pero no puedo ponerme un pijama azul!\aPregúntale a Plúmbea Triz si tiene otro color.",
             INCOMPLETE_PROGRESS : "Seguro que Plúmbea Triz tiene pijamas con pies de otro color.",
             COMPLETE : "",
             },
    7232 : { GREETING : "",
             LEAVING : "",
             QUEST : "Qué pena. Es el único pijama con pies que tengo.\aOh, tengo una idea. Ve a preguntarle a Cato. A lo mejor ella tiene pijamas con pies._where_",
             INCOMPLETE_PROGRESS : "No, este es el único pijama que tengo. Ve a ver lo que tiene Cato._where_",
             COMPLETE : "",
             },
    7233 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Un pijama con pies? Por supuesto.\a¿Qué quieres decir con que son azules? ¿No le gusta el azul?\aOh, eso es un poco más complicado. Toma, prueba con este.\aNo es azul y tiene pies.",
             INCOMPLETE_PROGRESS : "Me encanta el color rojo, ¿a ti no?\aEspero que a Sandra le guste...",
             COMPLETE : "",
             },
    7234 : { GREETING : "",
             LEAVING : "",
             QUEST : "No, este no es azul, pero nadie con esta complexión se atrevería a ponerse algo rojo.\aDe ninguna manera. ¡Devuélvelo! A ver qué más tiene Cato.",
             INCOMPLETE_PROGRESS : "Seguro que Cato tiene más pijamas. ¡Y nada rojo!",
             COMPLETE : "",
             },
    7235 : { GREETING : "",
             LEAVING : "",
             QUEST : "Rojo tampoco. Umm....\aBueno, estoy segura de que tengo más.\aTardaré un poco en encontrarlos. Hagamos un trato.\aYo busco otro pijama y tú te deshaces de algunos de esos edificios bot. Me alteran mucho.\aEl pijama estará listo cuando vuelvas, _avName_.",
             INCOMPLETE_PROGRESS : "Tienes que eliminar más edificios bot mientras busco otro pijama.",
             COMPLETE : "",
             },
    7236 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Hiciste un gran trabajo con esos bots! ¡Gracias!\aEncontré el pijama para Sandra; espero que le guste.\aLlévaselo. Gracias.",
             INCOMPLETE_PROGRESS : "Sandra está esperando el pijama, _avName_.",
             COMPLETE : "¡Un pijama fucsia con pies! ¡Perrrrfecto!\aAh, se acabó el problema. Veamos...\aOh, supongo que debería darte algo por ayudarme.\aQuizás esto te resulte útil. Alguien lo olvidó aquí.",
             },
 
    # Smudgy Mascara needs Wrinkle Cream but
    # 39's missing ingredients. Help them out
    # and get a piece of Cog suit
    7239 : { QUEST : "Ve a ver a Máscara Pepínez. Dijo que necesitaba ayuda._where_",
             },
    7240 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Esos malditos se llevaron mi crema antiarrugas!\aMis clientes NECESITAN crema antiarrugas.\aVe a ver a Ripón a ver si tiene en stock mi fórmula especial._where_",
             INCOMPLETE_PROGRESS : "Me niego a trabajar si no tengo crema antiarrugas.\aVe a ver lo que Ripón puede ofrecerme.",
             },
    7241 : { GREETING : "",
             LEAVING : "",
             QUEST : "Oh, esa Máscara es muy molesta. No se conforma con mi fórmula habitual.\aEso significa que necesitaré coral de coliflor, mi ingrediente súper especial, pero no me queda nada.\a¿Podrías ir a pescarlo en el estanque? En cuanto tengas el coral, haré un preparado para Máscara.",
             INCOMPLETE_PROGRESS : "Necesito ese coral de coliflor para hacer un preparado de crema antiarrugas.",
             },
    7242 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Qué coral de coliflor tan hermoso!\aOk, veamos... un poco de esto y unas gotas de lo otro... y ahora, una cucharada de algas.\aVaya, ¿dónde están las algas? Tampoco me quedan.\a¿Puedes bajar al lago y buscar unas lindas algas pegajosas?",
             INCOMPLETE_PROGRESS : "En la tienda no quedan algas pegajosas.\aSin ellas no puedo preparar la crema.",
             },
    7243 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Oooh! Qué algas tan pegajosas tienes ahí, _avName_.\aAhora solo tengo que moler unas perlas con el mortero.\aPero, ¿dónde está el mazo? ¿De qué me sirve un mortero sin mazo?\a¡Seguro que ese maldito prestamista despiadado se lo llevó cuando vino!\a¡Tienes que ayudarme a encontrarlo! ¡Iba en dirección al cuartel general chequebot!",
             INCOMPLETE_PROGRESS : "No puedo moler las perlas sin el mazo de mortero.\a¡Malditos prestamistas despiadados!",
             },
    7244 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Estupendo! ¡Tienes mi mazo de mortero!\aYa podemos poner manos a la obra. Picamos eso... lo movemos un poco y...\a¡ya está! Dile a Máscara que está recién preparada.",
             INCOMPLETE_PROGRESS : "Deberías llevárselo a Máscara mientras esté fresca.\aEs muy quisquillosa.",
             COMPLETE : "¿Es que Ripón no tenía un bote de crema antiarrugas más grande? ¿No?\aBueno, ya encargaré más cuando se termine.\aHasta luego, _avName_.\a¿Qué? ¿Sigues ahí? ¿No ves que estoy intentando trabajar?\aToma, llévate esto.",
             },

    # Lawbot HQ part quests
    11000 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si te interesan piezas de disfraz de abogabot, deberías visitar a _toNpcName_.\aDicen que necesita ayuda con sus investigaciones sobre el clima._where_",
              },
    11001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Sí, sí. Tengo piezas para disfraz de abogabot.\aPero a mí no me interesan.\aEl tema de mi investigación es la fluctuación de la temperatura ambiental en Toontown.\aSerá un placer intercambiar piezas de disfraz por sensores de temperatura bot.\aPuedes empezar en %s." % GlobalStreetNames[2100][-1],
              INCOMPLETE_PROGRESS : "¿Miraste en %s?" % GlobalStreetNames[2100][-1],
              COMPLETE : "¡Ah, excelente!\aJusto como me temía...\a¡Oh, sí! Toma tu pieza del disfraz.",
             },

    11002 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si quieres más piezas de disfraz de abogabot, visita otra vez a _toNpcName_.\aDicen que necesita más ayudantes de investigación._where_",
              },
    11003 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Más piezas de disfraz de abogabot?\aBueno, si insistes...\apero necesitaré otro sensor de temperatura bot.\aEsta vez, quiero que mires en %s." % GlobalStreetNames[2200][-1],
              INCOMPLETE_PROGRESS : "Estás buscando en %s, ¿verdad?" % GlobalStreetNames[2200][-1],
              COMPLETE : "¡Gracias!\aToma tu pieza de disfraz.",
             },
    11004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si necesitas más piezas de disfraz de abogabot, visita otra vez a _toNpcName_.\aDicen que todavía necesita ayuda con su investigación climática._where_",
              },
    11005 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡Has probado ser de gran utilidad!\a¿Puedes echar un vistazo en %s?" % GlobalStreetNames[2300][-1],
              INCOMPLETE_PROGRESS : "¿Seguro que estás buscando por %s?" % GlobalStreetNames[2300][-1],
              COMPLETE : "Ummm, esto no me gusta...\apero toma, tu pieza de disfraz...",
             },
    11006 : { GREETING : "",
              LEAVING : "",
              QUEST : "'Tú sabes quién' necesita más sensores de temperatura.\aPásate a verle si quieres otra pieza de disfraz._where_",
              },
    11007 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Regresaste otra vez?\aEres muy persistente...\aLa próxima parada es %s." % GlobalStreetNames[1100][-1],
              INCOMPLETE_PROGRESS : "¿Miraste en %s?" % GlobalStreetNames[1100][-1],
              COMPLETE : "¡Bien! ¡Parece que ya dominas la situación!\aTu pieza de disfraz...",
             },
    11008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si quieres otra pieza de disfraz..._where_",
              },
    11009 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡Me alegro de verte!\aAhora, necesito lecturas de %s." % GlobalStreetNames[1200][-1],
              INCOMPLETE_PROGRESS : "Estás buscando por %s, ¿verdad?" % GlobalStreetNames[1200][-1],
              COMPLETE : "Muchas gracias.\aTu disfraz debe de estar ya bastante completo...",
             },
    11010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Creo que _toNpcName_ tiene más trabajo para ti._where_",
              },
    11011 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡Me alegra volver a verte, _avName_!\a¿Puedes conseguirme un sensor de %s?" % GlobalStreetNames[1300][-1],
              INCOMPLETE_PROGRESS : "¿Miraste en %s?" % GlobalStreetNames[1300][-1],
              COMPLETE : "¡Buen trabajo!\a¡Toma tu recompensa, te la ganaste!",
             },
    11012 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ya sabes cómo es esto._where_",
              },
    11013 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡_avName_, querido amigo!\a¿Puedes ir a %s a buscar otro sensor de temperatura?" % GlobalStreetNames[5100][-1],
              INCOMPLETE_PROGRESS : "¿Seguro que estás buscando por %s?" % GlobalStreetNames[5100][-1],
              COMPLETE : "¡Excelente!\aCon tu ayuda, ¡mi investigación avanza rápidamente!\aToma, tu recompensa.",
             },
    11014 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ te ha estado buscnado mucho.\a¡Parece qué le dejaste una buena impresión!_where_",
              },
    11015 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡Hola otra vez!\aTe estaba esperando.\aLa siguiente lectura está en %s." % GlobalStreetNames[5200][-1],
              INCOMPLETE_PROGRESS : "Estás mirando en %s, ¿verdad?" % GlobalStreetNames[5200][-1],
              COMPLETE : "¡Gracias!\aToma, tu recompensa.",
             },
    11016 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si necesitas terminar tu disfraz de abogabot...\a_toNpcName_ puede ayudarte._where_",
              },
    11017 : { GREETING : "",
              LEAVING : "",
              QUEST : "¡Hola, aprendiz de científico!\aTodavía necesitamos lecturas de %s." % GlobalStreetNames[5300][-1],
              INCOMPLETE_PROGRESS : "¿Miraste en %s?" % GlobalStreetNames[5300][-1],
              COMPLETE : "¡Un trabajo excelente!\aAquí tienes tu coso de abogabot...",
             },
    11018 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tiene otro trabajo para ti.\aSi no te hartaste aún de él..._where_",
              },
    11019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Bueno.\a¿Estás listo para otro hallazgo?\aEsta vez, prueba en %s." % GlobalStreetNames[4100][-1],
              INCOMPLETE_PROGRESS : "¿Seguro que estás buscando en %s?" % GlobalStreetNames[4100][-1],
              COMPLETE : "¡Otro!\a¡Eres un auténtico sabueso!",
             },
    11020 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Sigues buscando piezas de disfraz de abogabot?_where_",
              },
    11021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Seguramente ya lo sabrás...\apero necesito lecturas de %s." % GlobalStreetNames[4200][-1],
              INCOMPLETE_PROGRESS : "Estás buscando en %s, ¿verdad?" % GlobalStreetNames[4200][-1],
              COMPLETE : "¡Ya casi está!\aToma...",
             },
    11022 : { GREETING : "",
              LEAVING : "",
              QUEST : "Odio admitirlo, pero..._where_",
              },
    11023 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Qué piensas de %s? ¿Puedes conseguir ahí también un sensor?" % GlobalStreetNames[4300][-1],
              INCOMPLETE_PROGRESS : "¿Miraste en %s?" % GlobalStreetNames[4300][-1],
              COMPLETE : "Otro trabajo excelente, _avName_",
             },
    11024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si todavía necesitas piezas de disfraz, ve a visitar al Profesor._where_",
              },
    11025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Creo que todavía necesitamos lecturas de %s." % GlobalStreetNames[9100][-1],
              INCOMPLETE_PROGRESS : "¿Seguro que estás mirando en %s?" % GlobalStreetNames[9100][-1],
              COMPLETE : "¡Buen trabajo!\aCreo que estamos muy cerca...",
             },
    11026 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tiene una última misión para ti._where_",
              },
    11027 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Ya regresaste?\aLa lectura final está en %s." % GlobalStreetNames[9200][-1],
              INCOMPLETE_PROGRESS : "Estás buscando en %s, ¿verdad?" % GlobalStreetNames[9200][-1],
              COMPLETE : "¡Ya terminaste!\aYa estás listo para infiltrarte en la oficina del fiscal del distrito y recoger Notificaciones del tribunal.\a¡Buena suerte y gracias por tu ayuda!",
             },

    12000 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si te interesan las piezas de disfraz de jefebot, deberías visitar a _toNpcName_._where_",
              },
    12001 : { GREETING : "",
              LEAVING : "",
              QUEST : "Sí, puedo conseguirte piezas de jefebot.\aPero necesito que me ayudes a completar mi colección jefebot.\aSal y derrota a un secuaz.",
              INCOMPLETE_PROGRESS : "¿No encuentras a un secuaz? Qué vergüenza...",
              COMPLETE : "No fallaste, ¿verdad?\aToma, tu primera pieza del disfraz.",
             },
    12002 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ necesita más ayuda, si quieres._where_",
              },
    12003 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Otra pieza de disfraz?\aPor supuesto...\apero solo si derrotas a un chupatintas.",
              INCOMPLETE_PROGRESS : "Los chupatintas están por las calles.",
              COMPLETE : "¡Fue muy fácil!\aAquí tienes la segunda pieza de tu disfraz.",
             },
    12004 : { GREETING : "",
              LEAVING : "",
              QUEST : "Para conseguir piezas de jefebot, solo hay un sitio donde buscar._where_",
              },
    12005 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ahora, necesito un sonriente...",
              INCOMPLETE_PROGRESS : "Los sonrientes se pueden encontrar por las calles.",
              COMPLETE : "¡Sí! Eres un as.\aToma, la tercera pieza de tu disfraz.",
             },
    12006 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ tiene más piezas para ti...",
              },
    12007 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si derrotas a un microgerente, te daré otra pieza.",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[1100][-1],
              COMPLETE : "¡Te salió bastante bien!\aToma, la cuarta pieza de tu disfraz.",
             },
    12008 : { GREETING : "",
              LEAVING : "",
              QUEST : "Dirígete a..._where_",
              },
    12009 : { GREETING : "",
              LEAVING : "",
              QUEST : "Estoy buscando a un regulador de empleo...",
              INCOMPLETE_PROGRESS : "¿Tienes problemas? Prueba buscando en %s" % GlobalStreetNames[3100][-1],
              COMPLETE : "¡No fue fácil!\aToma, tu quinta pieza de disfraz.",
             },
    12010 : { GREETING : "",
              LEAVING : "",
              QUEST : "Creo que ya sabes dónde ir..._where_",
              },
    12011 : { GREETING : "",
              LEAVING : "",
              QUEST : "Lo siguiente en mi lista Cazacabezas.",
              INCOMPLETE_PROGRESS : "Creo que tendrás más suerte si miras en los edificios.",
              COMPLETE : "Veo que no tuviste problemas para encontrar uno.\aToma, la sexta pieza del disfraz.",
             },
    12012 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ necesita más jefebots.",
              },
    12013 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ahora necesito que encuentres a un corporativista.",
              INCOMPLETE_PROGRESS : "Creo que tendrás más suerte si miras en los edificios.",
              COMPLETE : "¡Tú sí que estás hecho todo un corporativista!\aToma, la séptima pieza del disfraz.",
             },
    12014 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si quieres más piezas de disfraz, ve a..._where_",
              },
    12015 : { GREETING : "",
              LEAVING : "",
              QUEST : "Y ahora, el broche de oro: ¡el pez gordo!",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Sabía que podía contar contigo para cortar...\aAh, da igual.\aToma, la siguiente pieza del disfraz.",
             },
    12016 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ te andaba buscando...",
              },
    12017 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ahora necesito que derrotes a uno de los nuevos jefebots; son más peligrosos.",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Son más duros de lo que parecen, ¿eh?\aSupongo que te debo una pieza de disfraz.",
             },
    12018 : { GREETING : "",
              LEAVING : "",
              QUEST : "¿Podrías pasar por..._where_?",
              },
    12019 : { GREETING : "",
              LEAVING : "",
              QUEST : "Estos bots versión 2.0 son muy interesantes.\aPor favor, ve y derrota a uno.",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "¡Gracias!\aMarche otra pieza de disfraz.",
             },
    12020 : { GREETING : "",
              LEAVING : "",
              QUEST : "Si tienes la ocasión, pasa a ver a _toNpcName_.",
              },
    12021 : { GREETING : "",
              LEAVING : "",
              QUEST : "Me pregunto si pueden seguir regenerándose...",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Supongo que no.\aToma, tu pieza...",
             },
    12022 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ya sabes..._where_",
              },
    12023 : { GREETING : "",
              LEAVING : "",
              QUEST : "Quizá ni siquiera sean jefebots...",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Ummm, parece que, después de todo, sí que son jefebots.\aToma otra pieza.",
             },
    12024 : { GREETING : "",
              LEAVING : "",
              QUEST : "Seguramente ya sabrás lo que te voy a decir...",
              },
    12025 : { GREETING : "",
              LEAVING : "",
              QUEST : "Quizás estén relacionados con los esquelebots...",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "El resutlado no fue concluyente...\aToma, otra pieza de disfraz.",
             },
    12026 : { GREETING : "",
              LEAVING : "",
              QUEST : "Por favor, ve a ver a _toNpcName_ otra vez.",
              },
    12027 : { GREETING : "",
              LEAVING : "",
              QUEST : "Aún pienso que podría tratarse de algún tipo de esquelebot...",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Bueno, quizás no.\aToma la pieza siguiente.",
             },
    12028 : { GREETING : "",
              LEAVING : "",
              QUEST : "Seguramente es el último sitio al que te gustaría ir, pero...",
              },
    12029 : { GREETING : "",
              LEAVING : "",
              QUEST : "Estos nuevos bots todavía me alteran un poco.\a¿Podrías derrotar a otro, por favor?",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Fascinante. Simplemente, fascinante.\aUna pieza del disfraz, por las molestias.",
             },
    12030 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_ empieza a sonar como un disco rallado...",
              },
    12031 : { GREETING : "",
              LEAVING : "",
              QUEST : "Ya casi decidí lo que son esos nuevos bots.\aSólo uno más...",
              INCOMPLETE_PROGRESS : "Busca en %s" % GlobalStreetNames[10000][-1],
              COMPLETE : "Sí, creo que descubrí algo.\aAh, sí.\aEsto es para ti...",
             },
    12032 : { GREETING : "",
              LEAVING : "",
              QUEST : "Tienes que ir a contarle esto a Flipi...",
              INCOMPLETE_PROGRESS : "Encontrarás a Flipi en el Ayuntamiento",
              COMPLETE : "¡Un nuevo tipo de bot!\a¡Buen trabajo!\aToma, la última pieza de tu disfraz.",
              },
 }

# ChatGarbler.py
ChatGarblerDog = ["guau", "arf", "grrrr"]
ChatGarblerCat = ["miau", "miao"]
ChatGarblerMouse = ["ñic", "ñiiiic", "ñic ñic"]
ChatGarblerHorse = ["Yiiiijijii", "brrr"]
ChatGarblerRabbit = ["iiik", "ipr", "iiipi", "iiiki"]
ChatGarblerDuck = ["cuac", "cuaaac ", "cuac cuac"]
ChatGarblerMonkey = ["ooh", "ooo", "ahh"]
ChatGarblerBear = ["Grraaargg", "grrr"]
ChatGarblerPig = ["oink", "oik", "resoplido"]
ChatGarblerDefault = ["bla"]

# AvatarDNA.py
Bossbot = "Jefebot"
Lawbot = "Abogabot"
Cashbot = "Chequebot"
Sellbot = "Vendebot"
BossbotS = "un jefebot"
LawbotS = "un abogabot"
CashbotS = "un chequebot"
SellbotS = "un vendebot"
BossbotP = "Jefebots"
LawbotP = "Abogabots"
CashbotP = "Chequebots"
SellbotP = "Vendebots"
BossbotSkelS = "un esquelebot jefebot"
LawbotSkelS = "un esquelebot abogabot"
CashbotSkelS = "un esquelebot chequebot"
SellbotSkelS = "un esquelebot vendebot"
BossbotSkelP = "esquelebots jefebots"
LawbotSkelP = "esquelebots abogabots"
CashbotSkelP = "esquelebots chequebots"
SellbotSkelP = "esquelebots vendebots"
SkeleRevivePostFix = " v2.0"

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Buscando datos de %s."
AvatarDetailPanelFailedLookup = "Imposible obtener datos de %s."
#AvatarDetailPanelPlayer = "Jugador: %(player)s\nMundo: %(world)s\nLugar: %(location)s"
# sublocation is not working now
AvatarDetailPanelPlayer = "Jugador: %(player)s\nMundo: %(world)s"
AvatarDetailPanelPlayerShort = "%(player)s\nMundo: %(world)s\nLugar: %(location)s"
AvatarDetailPanelRealLife = "Sin conexión"
AvatarDetailPanelOnline = "Distrito: %(district)s\nLugar: %(location)s"
AvatarDetailPanelOnlinePlayer = "Distrito: %(district)s\nLugar: %(location)s\nPlayer: %(player)s"
AvatarDetailPanelOffline = "Distrito: sin conexión\nLocalidad: sin conexión"
AvatarShowPlayer = "Mostrar jugador"
OfflineLocation = "Sin conexión"

#PlayerDetailPanel
PlayerToonName = "Dibu: %(toonname)s"
PlayerShowToon = "Mostrar dibu"
PlayerPanelDetail = "Datos del jugador"


# AvatarPanel.py
AvatarPanelFriends = "Amigos"
AvatarPanelWhisper = "Susurrar"
AvatarPanelSecrets = "Secretos"
AvatarPanelGoTo = "Ir a"
AvatarPanelPet = "Mostrar dibuperrito"
AvatarPanelIgnore = "Ignorar"
AvatarPanelIgnoreCant = "Okay"
AvatarPanelStopIgnoring = "Dejar de ignorar"
AvatarPanelReport = "Informar"
#AvatarPanelCogDetail = "Dept: %s\nNivel: %s\n"
AvatarPanelCogLevel = "Nivel: %s"
AvatarPanelCogDetailClose = lClose
AvatarPanelDetail = "Datos del dibu"
AvatarPanelGroupInvite = "Invitar"
AvatarPanelGroupRetract = "Retirar invitación"
AvatarPanelGroupMember = "Ya está en el grupo"
AvatarPanelGroupMemberKick = "Eliminar"

# Report Panel
ReportPanelTitle = "Informar sobre un jugador"
ReportPanelBody = "Esta función enviará un informe completo a un moderador. En lugar de enviar un informe, quizás prefieras una de las siguientes opciones:\n\n  - Teletransportarte a otro distrito\n  - Usar \"Ignorar\" en el panel del dibu \n\n¿Seguro que quieres informar sobre %s al moderador?"
ReportPanelBodyFriends = "Esta función enviará un informe completo a un moderador. En lugar de enviar un informe, quizás prefieras una de las siguientes opciones:\n\n  - Teletransportarte a otro distrito\n  - Romper la amistad\n\n¿Seguro que quieres informar sobre %s al moderador?\n\n(Al hacerlo, también se romperá tu amistad)"
ReportPanelCategoryBody = "Estás a punto de enviar un informe sobre %s. Un moderador será informado de tu queja y tomará las medidas correspondientes para casos en que alguien infringe las reglas. Por favor, elige los motivos por los que quieres presentar un informe sobre %s:"
ReportPanelBodyPlayer = "Está función todavía está en proceso de desarrollo; pronto podrás acceder a ella. Mientras tanto, puedes elegir una de las siguientes opciones:\n\n  - Ve a DXD y rompe con la amistad.\n – Habla con uno de tus padres y explícale lo que sucedió."

ReportPanelCategoryLanguage = "Malas palabras"
ReportPanelCategoryPii = "Compartir/solicitar datos personales"
ReportPanelCategoryRude = "Comportamiento grosero o incorrecto"
ReportPanelCategoryName = "Insulto"

ReportPanelConfirmations = (
    "Estás a punto de informar de que %s utilizó un lenguaje obsceno, discriminatorio o explícitamente sexual.",
    "Estás a punto de informar de que %s no cumple las normas de seguridad al proporcionar o solicitar un número de teléfono, dirección, apellido, dirección de e-mail, contraseña o nombre de cuenta.",
    "Estás a punto de informar de que %s está acosando a alguien o comportándose de un modo extremo y alterando el juego.",
    "Estás a punto de informar de que %s creó un nombre que no respeta las reglas de Disney's House.",
    )

# Put on confirmation screen!
ReportPanelWarning = "Nos tomamos las quejas muy en serio. Tu informe será revisado por un moderador, quien tomará las medidas adecuadas para los casos en que alguien infringe nuestras normas. Si se descubre que tu cuenta está involucrada en uno de estos casos, o si presentas informes falsos o haces un uso abusivo de del sistema Informar sobre un jugador, el moderador podría tomar medidas contra tu cuenta. ¿Estás totalmente seguro de que quieres presentar un informe sobre este jugador?"

ReportPanelThanks = "¡Gracias! Tu informe fue enviado a un moderador para proceder a su revisión. No es necesario que te vuelvas a poner en contacto en relación a este asunto. El equipo moderador tomará las medidas apropiadas para los casos en que un jugador infringe las normas."

ReportPanelRemovedFriend = "%s fue eliminado automáticamente de tu lista de amigos."
ReportPanelRemovedPlayerFriend = "%s fue eliminado automáticamente de tus amigos jugadores para que ya no aparezca como amigo tuyo en ningún producto de Disney."

ReportPanelAlreadyReported = "Ya presentaste un informe sobre %s durante esta sesión. El moderador revisará tu informe anterior."

# Report Panel
IgnorePanelTitle = "Ignorar a un jugador"
IgnorePanelAddIgnore = "¿Quieres ignorar a %s durante el resto de esta sesión?"
IgnorePanelIgnore = "Estás ignorando a %s."
IgnorePanelRemoveIgnore = "¿Quieres dejar de ignorar a %s?"
IgnorePanelEndIgnore = "Ya no estás ignorando a %s."
IgnorePanelAddFriendAvatar = "%s es tu amigo o amiga, no puedes ignorarle mientras sean amigos."
IgnorePanelAddFriendPlayer = "%s (%s)es tu amigo o amiga, no puedes ignorarle mientras sean amigos."

# PetAvatarPanel.py
PetPanelFeed = "Alimentar"
PetPanelCall = "Llamar"
PetPanelGoTo = "Ir a"
PetPanelOwner = "Mostrar propietario"
PetPanelDetail = "Datos de la mascota"
PetPanelScratch = "Rascar"

# PetDetailPanel.py
PetDetailPanelTitle = "Entrenamiento de acrobacias"
# NOTE: these are replicated from OTPLocalizerEnglish sans "!"
PetTrickStrings = {
    0: 'Saltar',
    1: 'Pedir',
    2: 'Hacerse el muerto',
    3: 'Rodar',
    4: 'Hacer voltereta',
    5: 'Saltar',
    6: 'Hablar',
    }


# PetMood.py
PetMoodAdjectives = {
    'neutral': 'neutral',
    'hunger': 'hambriento',
    'boredom': 'aburrido',
    'excitement': 'emocionado',
    'sadness': 'triste',
    'restlessness': 'inquieto',
    'playfulness': 'jueguetón',
    'loneliness': 'solo',
    'fatigue': 'cansado',
    'confusion': 'confundido',
    'anger': 'enfadado',
    'surprise': 'sorprendido',
    'affection': 'cariñoso',
    }

SpokenMoods = {
    'neutral': 'neutral',
    'hunger': 'Estoy harto de las golosinas. ¿Por qué no me das un trozo de tarta?',
    'boredom': 'No pensarás que te entendí, ¿verdad?',
    'excitement': '¡Toontástico!',
    'sadness': 'Quiero pasar tiempo con mi dibuperrito',
    'restlessness': 'Estoy muy inquieto',
    'playfulness': '¡Juega conmigo o empezaré a escarbar en las flores!',
    'loneliness': '¡Quiero ir contigo a luchar contra los bots!',
    'fatigue': '¡Las acrobacias de Dibuperrito son agotadoras! ¿Por qué no descansamos?',
    'confusion': '¿Dónde estoy? ¿Dónde estás?',
    'anger': 'Siempre me dejas atrás',
    'surprise': 'Uau, ¿de dónde saliste?',
    'affection': '¡Eres un dibu estupendo!',
    }

# DistributedAvatar.py
DialogQuestion = '?'

# LocalAvatar.py
FriendsListLabel = "Amigos"

# TeleportPanel.py
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = "Intentando ir a %s."
TeleportPanelNotAvailable = "%s está ocupado en este momento. Inténtalo más tarde."
TeleportPanelIgnored = "%s te está ignorando."
TeleportPanelNotOnline = "%s no está conectado en este momento."
TeleportPanelWentAway = "%s se marchó."
TeleportPanelUnknownHood = "¡No sabes cómo llegar a %s!"
TeleportPanelUnavailableHood = "%s no está disponible en este momento. Inténtalo más tarde."
TeleportPanelDenySelf = "¡No puedes ir tú solo!"
TeleportPanelOtherShard = "%(avName)s está en el distrito %(shardName)s, y tú estás en el distrito %(myShardName)s. ¿Quieres cambiarte a %(shardName)s?"
TeleportPanelBusyShard = "%(avName)s está en un distrito lleno. Jugar en un distrito lleno puede ralentizar notablemente el rendimiento del juego. ¿Seguro que quieres intercambiar distritos?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Soy el jefe."

# DistributedBattleFactory.py
FactoryBossTaunt = "Soy el capataz."
FactoryBossBattleTaunt = "Te presento al capataz."
MintBossTaunt = "Soy el supervisor."
MintBossBattleTaunt = "Necesitas hablar con el supervisor."
StageBossTaunt = "Mi justicia no es igual para todos."
StageBossBattleTaunt = "Estoy por encima de la ley."
CountryClubBossTaunt = "Soy el presidente del club."
CountryClubBossBattleTaunt = "Necesitas hablar con el presidente del club."
ForcedLeaveCountryClubAckMsg = "El presidente del club fue derrotado antes de que pudieras llegar a él. No recuperaste ninguna acción."

# HealJokes.py
ToonHealJokes = [
    ["¿Qué le dice un dos a un cero?",
     "¡Vente conmigo! "],
    ["¿Qué es una brújula?",
     "Una viéjula montada en una escóbula."],
    ["Qué es un lóbulo?",
     "Un perro grándulo que se come a las ovéjulas."],
    ["¿Qué es una orilla?",
     "Sesenta minutillos."],
    ["¿Qué es una oreja?",
     "Sesenta minutejos."],
    ["¿Qué es un código?",
     "Por donde se dobla el brácigo."],
    ["¿Qué le dice un cero a otro cero?",
     "No valemos nada."],
    ["¿Qué le dice un jaguar a otro?",
     "¿Jaguar you?"],
    ["¿Cuántos astrónomos hacen falta para cambiar una bombilla?",
     "Ninguno, los astrónomos prefieren la oscuridad."],
    ["¿Cuál es el hombre con pensamientos más profundo?",
     "El minero."],
    ["¿Cómo se dice suspenso en chino?",
     "¡Cha cha cha chaaaaan!"],
    ["¿Qué le dice el pingüino a la pingüina?",
     "Te quiero como a ningüina."],
    ["¿Qué le dice la pelota a la raqueta?",
     "Lo nuestro es imposible, siempre me estás pegando..."],
    ["¿Qué le dice un poste a otro poste?",
     "Póstate bien."],
    ["¿Qué le dice un caimán mexicano a otro?",
     "¡Cai-manito!"],
    ["¿Cuál es la sal que peor huele?",
     "La sal-pargatas."],
    ["¿Qué es un punto verde en un rincón?",
     "Un guisante castigado."],
    ["¿Cómo se dice 99 en chino?",
     "Cachi-chien."],
    ["¿Por qué los gallegos ponen ajos en la carretera nacional?",
     "Porque son buenos para la circulación."],
    ["¿Qué es más asqueroso que encontrarse un gusano en una manzana?",
     "Encontrar sólo medio gusano."],
    ["¿Quién inventó las fracciones?",
     "Enrique Octavo."],
    ["¿Quién mató al libro de lengua?",
     "El sujeto."],
    ["¿Qué hora es cuando un elefante se sienta en una valla?",
     "Hora de cambiar la valla."],
    ["¿Por qué los elefantes no pueden montar en bicicleta?",
     "Porque no tienen dedo gordo para tocar la campanita."],
    ["¿Cómo se meten cuatro elefantes en un Mini?",
     "Pues dos delante y dos detrás."],
    ["¿Cuántos psicoanalistas hacen falta para cambiar una bombilla?",
     "Uno, pero la bombilla tiene que querer ser cambiada."],
    ["¿Por qué los flamencos se paran sobre una pata?",
     "Porque si no se caen."],
    ["¿Cuál es la patrona de los informáticos? ",
     "Santa Tecla."],
    ["¿Cuál es el patrón de los náufragos?",
     "San Están Aislados de la Costa."],
    ["¿Quién es el patrón de los profesores de educación física?",
     "San Gimnasio de Loyola."],
    ["¿Cuál es el grupo musical más oscuro? ",
     "Estatos Qúo."],
    ["¿Cuál es el vaquero más sucio del Oeste?",
     "Johny Melabo."],
    ["¿Cuál es el queso favorito de Sherlock Holmes?",
     "El emmental, querido Watson."],
    ["¿En qué se parece un elefante a una cama?",
     "En que el elefante es paquidermo y la cama paquiduermas."],
    ["¿En qué se parece una camisa vieja a un hotel barato? ",
     "En que ninguno tiene botones."],
    ["¿En qué se parece un boxeador a un telescopio?",
     "En que los dos hacen ver las estrellas."],
    ["¿En que se parece una diligencia a una silla?",
     "La diligencia va para Kansas City y la silla es para \"siti\" cansas."],
    ["¿En qué se parecen una escopeta y una gata?",
     "En que las dos tienen gatillos."],
    ["¿En qué se parecen un panadero y un político?",
     "En que los dos mueven masas."],
    ["¿En qué se parece una bruja a un fin de semana?",
     "En que los dos pasan volando."],
    ["¿En que se parecen los limones a los terratenientes?",
     "En que los dos tienen muchas propiedades."],
    ["¿En qué se parece una casa incendiándose a una casa vacía?",
     "En que de la casa incendiándose \"salen llamas\" y en la casa vacía \"llamas y nadie sale\"."],
    ["¿En qué se parece una pistola a un panadero?",
     "En que los dos hacen pan."],
    ["¿En qué se parece un ladrón a una pulga?",
     "En que la pulga salta y el ladrón asalta."],
    ["¿En qué se parece una estufa a un avión?",
     "En que los dos tienen piloto."],
    ["¿Qué le dice un chinche a una chinche?",
     "Te amo chincheramente."],
    ["¿Qué le dice un semáforo a otro?",
     "No me mires que me estoy cambiando."],
    ["¿Qué le dice el número 3 al número 30?",
     "Para ser como yo, tienes que ser sincero."],
    ["¿Qué le dice un semáforo a otro?",
     "No me mires que me pongo rojo."],
    ["¿Qué le dice el timbre al dedo?",
     "Si me tocas, grito."],
    ["¿Qué le dice un zapato al otro?",
     "¡Qué vida más arrastrada llevamos!"],
    ["¿Qué le dice un diente a otro?",
     "Ojo por ojo y hoy por ti, mañana por mí."],
    ["¿Qué le dice un ojo a otro?",
     "Si este tipo fuera bizco te extrañaría menos."],
    ["¿Cuál es el último animal acuático?",
     "El delfín."],
    ["¿Por qué es la cebra el animal más antiguo de la selva?",
     "Porque está en blanco y negro."],
    ["¿Por qué las películas de Chaplin eran mudas?",
     "Porque el director siempre decía: ¡No charles, Chaplin! "],
    ["¿Por qué los perros persiguen a los autos?",
     "Porque llevan un gato en el portaequipaje."],
    ["¿Por qué los franceses comen caracoles? ",
     "Porque no les gusta la comida rápida."],
    ["¿Por qué se esconden los animales de la selva? ",
     "Porque los elefantes están haciendo paracaidismo."],
    ["Ring, ring - Muy buenas, ¿es el uno-uno-uno-uno-uno-uno? ",
     "- No, éste es el once-once-once."],
    ["Ring, ring - Oiga, ¿es la Real Academia de la Lengua? ",
     "- No, pero como si lo seriese."],
    ["Ring, ring - ¿Es Otto? ",
     "- No, soy el de siempre."],
    ["Ring, ring - Hola, ¿está Agustín?",
     "- Pues sí, estoy aquí calentito y cómodo."],
    ["Ring, ring - Hola, ¿está Cholo?",
     "No, estoy acompañado."],
    ["Ring, ring - Hola, ¿está Alberto?",
     "- ¡No, está celado!"],
    ["Ring, ring - Hola, ¿ahí lavan la ropa?",
     "- No. - Pues qué sucios."],
    ["¿Cuál es el colmo de la lírica?",
     "Haber tenido un plácido domingo."],
    ["¿Cuál es el colmo de un carnicero?",
     "Tener un hijo chorizo."],
    ["¿Cuál es el colmo de un forzudo?",
     "Doblar una esquina."],
    ["¿Cuál es el colmo de un sastre?",
     "Tener un hijo botones."],
    ["¿Cuál es el colmo de un carpintero?",
     "Tener una hija cómoda."],
    ["¿Cuál es el colmo de un arquitecto?",
     "Construir castillos en el aire."],
    ["¿Cuál es el colmo de un peluquero?",
     "Perder el tren por los pelos."],
    ["¿Cuál es el colmo de un caballo?",
     "Tener silla y no poder sentarse."],
    ["¿Cuál es el colmo de los colmos?",
     "Que un mudo le diga a un sordo que un ciego lo está mirando feo."],
    ["¿Cuál es el colmo de un fotógrafo?",
     "Que se le rebelen los hijos."],
    ["¿Cuál es el colmo de la pereza?",
     "Levantarse dos horas antes para estar más tiempo sin hacer nada."],
    ["¿Cuál es el colmo de un jardinero?",
     "Que su novia se llame Rosa y lo deje plantado."],
    ["¿Cuál es el colmo de los colmos?",
     "Sentarse en un pajar y pincharse con la aguja."],
    ["¿Cuál es el colmo de un electricista?",
     "Que su mujer se llame Luz y sus hijos no le sigan la corriente."],
    ["¿Cuál es el colmo de un libro?",
     "Que en otoño se le caigan las hojas."],
    ["¿Cuál es el colmo de una ballena?",
     "Ir vacía."],
    ["¿Cuál es el colmo de un policía?",
     "Detener a un huracán por exceso de velocidad. "],
    ["¿Cuál es el colmo de un robot?",
     "Tener nervios de acero."],
    ["¿Cuál es el colmo de una jirafa?",
     "Tener dolor de garganta."],
    ["¿Cuál es el colmo de un pez?",
     "Quejarse porque no llueve."],
    ["¿Cuál es el colmo de Aladino?",
     "Tener mal genio."],
    ["¿Cuál es el colmo de un astronauta?",
     "Quejarse de no tener espacio."],
    ["¿Cuál es el colmo de un dinamitero?",
     "Que lo exploten en su trabajo."],
    ["¿Cuál es el colmo de los colmos?",
     "Que dos palomas de la paz se peleen por la ramita de olivo."],
    ["¿Cuál es el colmo de Santa Claus?",
     "No poder bajar por la chimenea debido a la claustrofobia."],
    ["¿Por qué echa Donald azúcar en la almohada?",
     "Porque quiere tener dulces sueños."],
    ["¿Por qué llevó Goofy el peine al dentista?",
     "Porque perdió todos los dientes."],
    ["¿Por qué se sienta Goofy en la última fila de los cines?",
     "Porque el que ríe el último, ríe mejor."],
    ["¿Cuál es el colmo de un escritor?",
     "Que su esposa le dé sopa de letras."],
    ["¿Cuál es el colmo de un calvo?",
     "Tener ideas descabelladas."],
    ["¿Cuál es el colmo de una maleta?",
     "Pedir vacaciones porque está cansada de tanto viajar."],
    ["¿Cuál es el colmo de un gallo?",
     "Que se le ponga la piel de gallina."],
    ["¿Cuál es el colmo de un carnicero?",
     "Tener un perro salchicha."],
    ["¿Cuál es el colmo de una silla? ",
     "Tener patas y no poder caminar."],
    ["¿Cuál es el colmo de un gato?",
     "Vivir una vida de perros."],
    ["¿Cuál es el colmo más pequeño?",
     "El colmillo."],
    ["¿Cuál es el colmo de un paracaidista?",
     "Tener la moral por los suelos."],
    ["¿Cuál es el colmo de la tacañería?",
     "Contarse los dedos cada vez que se le da la mano a alguien."],
    ["¿Cuál es el colmo de un dálmata?",
     "Que le saquen una foto y salga en blanco y negro."],
    ["¿Cuál es el colmo de un pastor?",
     "Quedarse dormido contando ovejas."],
    ["¿Cuál es el colmo de un vidriero?",
     "Que quiebre su negocio."],
    ["¿Cuál es el colmo de un cerrajero? ",
     "Dejarse las llaves dentro de casa."],
    ["¿Cuál es el colmo de la paciencia?",
     "Tirar una moneda al agua y esperar a que la cara pida socorro."],
    ["¿Cuál es colmo de una costurera?",
     "Perder el hilo de la conversación."],
    ["¿Cuál es el colmo de un escritor?",
     "Querer poner siempre punto final a todas las reuniones."],
    ["¿Cuál es el colmo de un leñador?",
     "Dormir como un tronco."],
    ["¿Cuál es el colmo de un músico?",
     "Que su hijo dé la nota."],
    ["¿Cuál es el colmo de Saturno?",
     "Tener anillos y no tener dedos."],
    ["¿Cuál es el colmo de un comediante?",
     "Que le digan que es un artista serio."],
    ["¿Cuál es el colmo de un vanidoso?",
     "Que su juego favorito sea el yo-yo."],
    ["¿Cuál es el colmo de un plumero?",
     "Ser alérgico al polvo."],
    ["¿Cuál es el colmo de una cocinera?",
     "Llamar a la policía porque los fideos se están pegando."],
    ["¿Cuál es el colmo de un dinamitero?",
     "Que lo exploten en su trabajo."],
    ["¿Cuál es el colmo de un dentista?",
     "Quitarle los dientes a un serrucho."],
    ["¿Cuál es el colmo de un matemático?",
     "Tener muchos problemas."],
    ["¿Cuál es el colmo de un pez?",
     "Morir ahogado."],
    ["¿Cuál es el colmo de un cazador?",
     "Querer cazar la Osa Mayor."],
    ["¿Cuál es el colmo de un bombero?",
     "Llevarse trabajo a casa."],
    ["¿Cual es el colmo de la paciencia?",
     "Meter una zapatilla en una jaula y esperar a que cante."],
    ["¿Cuál es el colmo de un desdentado? ",
     "Estar armado hasta los dientes."],
    ["¿Cuál es el colmo de una enfermera?",
     "Llamarse Dolores de Cabeza."],
    ["¿Cuál es el colmo de un cobarde? ",
     "Salirse de la cocina cuando se pegan los fideos."],
    ["¿Cuál es el colmo de Pinocho?",
     "No tener madera de estudiante."],
    ["¿Cuál es el colmo de una enfermera?",
     "Ponerle un apósito a la leche cortada."],
    ["¿Cuál es el colmo de un camello?",
     "Vivir toda la vida jorobado."],
    ["¿Cuál es colmo de un cementerio?",
     "Estar cerrado por luto."],
    ["¿Cuál es el colmo de una sardina?",
     "Que le den lata."],
    ["¿Cuál es el colmo de un cóctel?",
     "Sentirse agitado."],
    ["¿Cuál es el colmo de un granjero?",
     "Dejar abierta la puerta del corral para que se ventile."],
    ["¿Cuál es la palabra más larga del mundo?",
     "Arroz, porque empieza con A y termina con Z."],
    ["¿Cuál es el animal que ve menos?",
     "La venada."],
    ["¿Cuál es el animal más fiero? ",
     "El lopintan, porque el león no es tan fiero como lopintan."],
    ["¿Cuál es el perro más explosivo?",
     "El vol-can."],
    ["¿Cuál es el animal que juega al ajedrez?",
     "El caballo."],
    ["¿Qué es un codo? ",
     "Un gdupo de niñods cantodes."],
    ["¿En que se parece una cueva a una alacena? ",
     "La cueva tiene estalactitas y estalagmitas y la alacena esta latita de atún, esta latita de anchoas..."],
    ["- Doctor, me siento mal.",
     "- Pues siéntese bien."],
    ["- Hoy tose usted mejor que ayer.",
     "- Sí, doctor... Estuve ensayando toda la noche."],
    ["- Doctor, doctor... ¿cómo sé si estoy perdiendo la memoria? ",
     "- Eso ya se lo dije ayer."],
    ["- Doctor, ¿qué me aconseja para evitar resfriarme de nuevo? ",
     "Conservar el resfriado que tiene ahora."],
    ["- Doctor, doctor, sigo pensando que soy invisible.",
     "- ¿Quién dijo eso?"],
    ["- Doctor, doctor, el pelo se me está cayendo. ¿Cómo puedo conservarlo?",
     "- Use una caja de zapatos."],
    ["- Doctor, doctor, hace dos semanas que no como ni duermo. ¿Qué tengo? ",
     "- Seguramente sueño y hambre."],
    ["- Doctor, doctor, vengo a que me haga una revisión completa.",
     "- ¿Le cambio el aceite también?"],
    ["- Doctor, doctor, es que tengo un hueso fuera...",
     "- Pues dígale que pase."],
    ["- Doctor, doctor tengo paperas.",
     "- Tome algo de plata y ya tiene pa platanos..."],
    ["- Doctor, doctor, cuando tomo café me duele un ojo.",
     "- ¿Probó a apartar la cucharilla?"],
    ["- ¡¡Doctor, doctor, vengo a que me osculte!!",
     "- ¡Rápido, detrás del sillón!"],
    ["- Doctor, tengo los dientes muy amarillos, ¿qué me recomienda?",
     "- Una corbata marrón."],
    ["- Mamá, mamá, en el cole me llaman despistado.",
     "- Tú vives en la casa de al lado, niñito."],
    ["- Mamá, mamá, en el colegio me llaman despistado.",
     "- Reza dos Ave marías y ve con Dios, amén."],
    ["- Mamá, mamá, ¿cuándo vamos a comer pan de hoy?",
     "- Mañana, hijo, mañana."],
    ["- ¡Mamá, mamá, están golpeando la puerta!",
     "- Déjala que se defienda sola."],
    ["- Mamá, mamá... ¿por qué me llaman pie grande en el cole?",
     "No lo sé, pero ¿guardaste los zapatos en el garaje?"],
    ["- Mamá, ¿qué es la amnesia?",
     "- ¿Qué? ¿Y tú quién eres?"],
    ["- Camarero, hay una mosca en mi sopa.",
     "- ¿Y cuánto pudo haber bebido una mosquita?"],
    ["- Camarero, tráigame un té sin leche.",
     "- Disculpe, no tenemos leche, ¿qué le parece un té sin crema?"],
    ["- ¿Cómo encontró el señor el solomillo?",
     "- Pues levanté un guisante y ahí estaba."],
    ["- Camarero, camarero, está usted metiendo la corbata en mi sopa.",
     "- No se preocupe, señor, no encoge."],
    ["- Camarero, ¡ya le pedí cien veces un vaso de agua! ",
     "- ¡Cien vasos de agua para el señor!"],
    ["- Camarero, camarero, hay una mosca muerta en mi sopa.",
     "- ¿Y qué esperaba por este precio? ¿Una viva?"],
    ["- Camarero, ¿el pescado viene solo?",
     "- No, se lo traigo yo."],
    ["- Camarero, un café solo, por favor.",
     "- ¡Todo el mundo fuera!"],
    ["- ¡Capitán, capitán, que vamos a pique! ",
     "-¡Dije yo que vamos a Acapulco y allí es donde vamos!"],
    ["- Capitán, capitán, ¡nos hundimos!",
     "- ¡Pero bobo, si estamos en un submarino!"],
    ["- ¡Capitán, capitán, perdimos la guerra! ",
     "- Pues búsquenla enseguida."],
    ["- ¡Soldado, ice la bandera!",
     "- Le felicito mi general, le quedó muy hermosa."],
    ["- ¡Soldados, presenten armas!",
     "- Mi general: Mi fusil. Mi fusil: mi general."],
    ["- Mi capitán, los soldados no soportan más, estamos a 42º a la sombra.",
     "- Está bien sargento, pueden descansar diez minutos al sol."],
    ["- Por favor, ¿la calle Sagasta?",
     "- Y... Si pisa fuerte..."],
    ["- Pero este reloj no anda.",
     "- Claro, todavía no tiene ni un año."],
    ["- Camarero, ¿tiene emparedado de hipopótamo?",
     "- No, lo siento. Se nos acabó el pan."],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("ji","je","ja","jua, jua")
MovieHealLaughterHits1= ("Ja, ja, ja","ji, ji","Je, je, je","Ja, ja")
MovieHealLaughterHits2= ("¡JUA, JUA, JUA!","¡JUO, JUO, JUO!","¡JA, JA, JA!")

# MovieSOS.py
MovieSOSCallHelp = "¡SOCORRO, %s!"
MovieSOSWhisperHelp = "¡%s necesita que le ayuden en el combate!"
MovieSOSObserverHelp = "¡SOCORRO!"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "¡Hola, %s! ¡Me alegra poder ayudarte!"
MovieNPCSOSGoodbye = "¡Nos vemos!"
MovieNPCSOSToonsHit = "¡Los dibus aciertan siempre!"
MovieNPCSOSCogsMiss = "¡"+TheCogs+" fallan siempre!"
MovieNPCSOSRestockGags = "Reaprovisionamiento de bromas %s"
MovieNPCSOSHeal = "Curadibu"
MovieNPCSOSTrap = "Trampa"
MovieNPCSOSLure = "Cebo"
MovieNPCSOSSound = "Sonido"
MovieNPCSOSThrow = "Lanzamiento"
MovieNPCSOSSquirt = "Chorro"
MovieNPCSOSDrop = "Caída"
MovieNPCSOSAll = "Todo"

# MoviePetSOS.py
MoviePetSOSTrickFail = "Suspiro"
MoviePetSOSTrickSucceedBoy = "¡Buen chico!"
MoviePetSOSTrickSucceedGirl = "¡Buena chica!"

# MovieSuitAttacks.py
MovieSuitCancelled = "CANCELADO\nCANCELADO\nCANCELADO"

# RewardPanel.py
RewardPanelToonTasks = "Dibutareas"
RewardPanelItems = "Objetos recuperados"
RewardPanelMissedItems = "Objetos no recuperados"
RewardPanelQuestLabel = "Tarea %s"
RewardPanelCongratsStrings = ["¡Así se hace!", "¡Felicitaciones!", "¡Guau!",
                              "¡Chupi!", "¡Impresionante!", "¡Dibufantástico!"]
RewardPanelNewGag = "¡Nueva broma %(gagName)s para %(avName)s!"
RewardPanelUberGag = "¡%(avName)s consiguió la broma %(gagName)s con %(exp)s puntos de experiencia!"
RewardPanelEndTrack = "¡Sí! ¡%(avName)s llegó al final del circuito de %(gagName)s!"
RewardPanelMeritsMaxed = "Máximo puntaje"
RewardPanelMeritBarLabels = [ "Cartas de despido", "Citaciones", "Botdólares", "Méritos" ]
RewardPanelMeritAlert = "¡Listo para un ascenso!"

RewardPanelCogPart = "Conseguiste una pieza de disfraz de bot"

# Cheesy effect descriptions: (short desc, sentence desc)
CheesyEffectDescriptions = [
    ("Dibu normal", "serás normal"),
    ("Cabezota grande", "tendrás la cabeza grande"),
    ("Cabecita pequeña", "tendrás la cabeza pequeña"),
    ("Piernotas grandes", "tendrás las piernas grandes"),
    ("Piernecitas pequeñas", "tendrás las piernas pequeñas"),
    ("Dibu grandote", "serás un poco más grande"),
    ("Dibu pequeñito", "serás un poco más pequeño"),
    ("Imagen plana", "tendrás sólo dos dimensiones"),
    ("Perfil plano", "tendrás sólo dos dimensiones"),
    ("Transparente", "serás transparente"),
    ("Incoloro", "no tendrás color"),
    ("Dibu invisible", "serás invisible"),
    ]
CheesyEffectIndefinite = "hasta que elijas otro efecto, %(effectName)s%(whileIn)s."
CheesyEffectMinutes = "Durante los próximos %(time)s minutos, %(effectName)s%(whileIn)s."
CheesyEffectHours = "Durante las próximas %(time)s horas, %(effectName)s%(whileIn)s."
CheesyEffectDays = "Durante los próximos %(time)s días, %(effectName)s%(whileIn)s."
CheesyEffectWhileYouAreIn = " mientras estás en %s"
CheesyEffectExceptIn = ", excepto en %s"


# SuitBattleGlobals.py
SuitFlunky = "Secuaz"
SuitPencilPusher = "Chupatintas"
SuitYesman = "Sonriente"
SuitMicromanager = "Microgerente"
SuitDownsizer = "Regulador de empleo"
SuitHeadHunter = "Cazacabezas"
SuitCorporateRaider = "Corporativista"
SuitTheBigCheese = "Pez gordo"
SuitColdCaller = "Aprovechado"
SuitTelemarketer = "Televendedor"
SuitNameDropper = "Fanfarrón"
SuitGladHander = "Efusivo"
SuitMoverShaker = "Mandamás"
SuitTwoFace = "Doscaras"
SuitTheMingler = "Confraternizador"
SuitMrHollywood = "Sr. Hollywood"
SuitShortChange = "Moneditas"
SuitPennyPincher = "Cacomatraco"
SuitTightwad = "Roñoso"
SuitBeanCounter = "Agarrado"
SuitNumberCruncher = "Contable"
SuitMoneyBags = "Monedero"
SuitLoanShark = "Prestamista despiadado"
SuitRobberBaron = "Barón ladrón"
SuitBottomFeeder = "Caradura"
SuitBloodsucker = "Chupasangres"
SuitDoubleTalker = "Embaucador"
SuitAmbulanceChaser = "Persigueambulancias"
SuitBackStabber = "Apuñalaespaldas"
SuitSpinDoctor = "Portavoz"
SuitLegalEagle = "Picapleitos"
SuitBigWig = "Pelucón"

# Singular versions (indefinite article)
SuitFlunkyS = "un secuaz"
SuitPencilPusherS = "un chupatintas"
SuitYesmanS = "un sonriente"
SuitMicromanagerS = "un microgerente"
SuitDownsizerS = "un regulador de empleo"
SuitHeadHunterS = "un cazacabezas"
SuitCorporateRaiderS = "un corporativista"
SuitTheBigCheeseS = "un pez gordo"
SuitColdCallerS = "un aprovechado"
SuitTelemarketerS = "un televendedor"
SuitNameDropperS = "un fanfarrón"
SuitGladHanderS = "un efusivo"
SuitMoverShakerS = "un mandamás"
SuitTwoFaceS = "un doscaras"
SuitTheMinglerS = "un confraternizador"
SuitMrHollywoodS = "un Sr. Hollywood"
SuitShortChangeS = "un moneditas"
SuitPennyPincherS = "un cacomatraco"
SuitTightwadS = "un roñoso"
SuitBeanCounterS = "un agarrado"
SuitNumberCruncherS = "un contable"
SuitMoneyBagsS = "un monedero"
SuitLoanSharkS = "un prestamista despiadado"
SuitRobberBaronS = "un barón ladrón"
SuitBottomFeederS = "un caradura"
SuitBloodsuckerS = "un chupasangres"
SuitDoubleTalkerS = "un embaucador"
SuitAmbulanceChaserS = "un persigueambulancias"
SuitBackStabberS = "un apuñalaespaldas"
SuitSpinDoctorS = "un portavoz"
SuitLegalEagleS = "un picapleitos"
SuitBigWigS = "un pelucón"

# Plural versions
SuitFlunkyP = "Secuaces"
SuitPencilPusherP = "Chupatintas"
SuitYesmanP = "Sonrientes"
SuitMicromanagerP = "Microgerentes"
SuitDownsizerP = "Reguladores de empleo"
SuitHeadHunterP = "Cazacabezas"
SuitCorporateRaiderP = "Corporativistas"
SuitTheBigCheeseP = "Peces Gordos"
SuitColdCallerP = "Aprovechados"
SuitTelemarketerP = "Televendedores"
SuitNameDropperP = "Fanfarrones"
SuitGladHanderP = "Efusivos"
SuitMoverShakerP = "Mandamases"
SuitTwoFaceP = "Doscaras"
SuitTheMinglerP = "Confraternizador"
SuitMrHollywoodP = "Sres. Hollywood"
SuitShortChangeP = "Moneditas"
SuitPennyPincherP = "Cacomatracos"
SuitTightwadP = "Roñosos"
SuitBeanCounterP = "Agarrados"
SuitNumberCruncherP = "Contables"
SuitMoneyBagsP = "Monederos"
SuitLoanSharkP = "Prestamistas despiadados"
SuitRobberBaronP = "Barones ladrones"
SuitBottomFeederP = "Caraduras"
SuitBloodsuckerP = "Chupasangres"
SuitDoubleTalkerP = "Embaucadores"
SuitAmbulanceChaserP = "Persigueambulancias"
SuitBackStabberP = "Apuñalaespaldas"
SuitSpinDoctorP = "Portavoces"
SuitLegalEagleP = "Picapleitos"
SuitBigWigP = "Pelucones"

SuitFaceOffDefaultTaunts = ['¡Buuu!']

SuitAttackDefaultTaunts = ['¡¡Toma esto!!', '¡Fíjate bien en esto!']

SuitAttackNames = {
  'Audit' : '¡Auditoría!',
  'Bite' : '¡Mordisco!',
  'BounceCheck' : 'Cheque sin fondos!',
  'BrainStorm' : '¡Aguacero!',
  'BuzzWord' : '¡Charlatán!',
  'Calculate' : '¡Calculadora!',
  'Canned' : '¡Enlatado!',
  'Chomp' : '¡Zampón!',
  'CigarSmoke' : '¡Humo de cigarro!',
  'ClipOnTie' : '¡Corbatón!',
  'Crunch' : '¡Crujido!',
  'Demotion' : '¡Degradación!',
  'Downsize' : '¡Recorte de plantilla!',
  'DoubleTalk' : '¡Embaucar!',
  'EvictionNotice' : '¡Deshaucio!',
  'EvilEye' : '¡Mal de ojo!',
  'Filibuster' : '¡Discurso plasta!',
  'FillWithLead' : '¡Lleno de plomo!',
  'FiveOClockShadow' : "¡Barbudo!",
  'FingerWag' : '¡Regañado!',
  'Fired' : '¡Despedido!',
  'FloodTheMarket' : '¡Saturar el mercado!',
  'FountainPen' : '¡Manchón de tinta!',
  'FreezeAssets' : '¡Activos congelados!',
  'Gavel' : '¡Martillo!',
  'GlowerPower' : '¡Mirada feroz!',
  'GuiltTrip' : '¡Culpable!',
  'HalfWindsor' : '¡Nudo imposible!',
  'HangUp' : '¡Corte de línea!',
  'HeadShrink' : '¡Reducción de cabeza!',
  'HotAir' : '¡Aire caliente!',
  'Jargon' : '¡Jerga jurídica!',
  'Legalese' : '¡Parrafada legal!',
  'Liquidate' : '¡Liquidación!',
  'MarketCrash' : '¡Desplome de bolsa!',
  'MumboJumbo' : '¡Rollo total!',
  'ParadigmShift' : '¡Cambio de rumbo!',
  'PeckingOrder' : '¡Pajarraco!',
  'PickPocket' : '¡Ladrón!',
  'PinkSlip' : '¡Carta de despido!',
  'PlayHardball' : '¡Última partida!',
  'PoundKey' : '¡Factura de teléfono!',
  'PowerTie' : '¡Corbata feroz!',
  'PowerTrip' : '¡Viajecito!',
  'Quake' : '¡Terremoto!',
  'RazzleDazzle' : '¡Sonrisote!',
  'RedTape' : '¡Cinta roja!',
  'ReOrg' : '¡Reorganización!',
  'RestrainingOrder' : '¡Orden de alejamiento!',
  'Rolodex' : '¡Agenda!',
  'RubberStamp' : '¡Sellazo!',
  'RubOut' : '¡Borrado!',
  'Sacked' : '¡TeSaco!',
  'SandTrap' : '¡Arenas movedizas!',
  'Schmooze' : '¡Adulación!',
  'Shake' : '¡Sacudida!',
  'Shred' : '¡Triturador!',
  'SongAndDance' : '¡Canto y danza!',
  'Spin' : '¡Giro loco!',
  'Synergy' : 'Sinergia!',
  'Tabulate' : '¡Contabilidad!',
  'TeeOff' : '¡Bolazo!',
  'ThrowBook' : '¡Tirar el libro!',
  'Tremor' : '¡Trepidación!',
  'Watercooler' : '¡Bidón de agua!',
  'Withdrawal' : '¡Retirada de fondos!',
  'WriteOff' : '¡Agujero contable!',
  }

SuitAttackTaunts = {
    'Audit': ["Creo que no te cuadran las cuentas.",
              "Parece que estás en números rojos.",
              "Deja que te ayude con la contabilidad.",
              "Tu columna de débito está por las nubes. ",
              "Voy a echar un vistazo a tus activos.",
              "Esto te va a desequilibrar las cuentas.",
              "Voy a examinar de cerca lo que debes.",
              "Con esto voy a dejar tu cuenta a cero.",
              "Es la hora de contabilizar tus gastos.",
              "Encontré un error en tu libro de contabilidad.",
              ],
    'Bite': ["¿Te apetece un mordisquito?",
             "¡Prueba un poco de esto!",
             "Perro ladrador, poco mordedor.",
             "¡Hoy estoy que muerdo!",
             "¡Vas a morder el polvo!",
             "Cuidado que muerdo.",
             "Muerdo siempre que puedo.",
             "Voy a morderte un poquito.",
             "No me pienso morder la lengua contigo.",
             "Sólo un mordisquito...  ¿Es pedir demasiado?",
             ],
    'BounceCheck': ["Qué lástima, no tienes fondo.",
                    "Tienes pendiente un pago.",
                    "Creo que este cheque es tuyo.",
                    "Me debes este cheque.",
                    "Estoy cobrando deudas atrasadas.",
                    "Este cheque está al rojo vivo.",
                    "Te voy a pasar un buen recargo.",
                    "Echa un vistazo a esto.",
                    "Esto te va a costar carísimo.",
                    "Me gustaría cobrar esto.",
                    "Voy a devolverte este regalito.",
                    "Este cheque será tu perdición.",
                    "Voy a incluir una penalización.",
                    ],
    'BrainStorm':["Mi predicción es que va a llover.",
                  "Espero que lleves paraguas.",
                  "Voy a remojarte un poco.",
                  "¿Qué te parecen unas cuantas GOTITAS?",
                  "Ya no hace un día tan bueno, ¿eh, dibu?",
                  "¿Estás listo para un aguacero?",
                  "Vas a ver lo que es una buena tormenta.",
                  "A esto lo llamo ataque relámpago.",
                  "Me encanta ser un aguafiestas.",
                  ],
    'BuzzWord':["Deja que te diga unas palabras.",
                "¿Te enteraste de lo último?",
                "A ver si entiendes esto.",
                "Intenta pronunciar esto, dibu.",
                "Deja que te ponga los puntos sobre las íes.",
                "Te doy mi palabra de que seré claro.",
                "Deberías medir mejor tus palabras.",
                "A ver cómo esquivas esto.",
                "Cuidado, esto no es un juego de palabras.",
                "Déjate de palabrería y prueba esto.",
                ],
    'Calculate': ["¡Con esto te van a salir las cuentas!",
                  "¿Habías contado con esto?",
                  "Suma y sigue; estás acabado.",
                  "Espera; te voy a ayudar a sumar esto.",
                  "¿Sumaste todos tus gastos?",
                  "Según mis cálculos, no estarás aquí mucho tiempo.",
                  "Aquí tienes el total.",
                  "Vaya; tu factura no para de aumentar.",
                  "¡Ponte a sumar esto!",
                  Cogs + ": 1; Dibus: 0",
                  ],
    'Canned': ["¿Te gustan las conservas?",
               "\"Conserva\" esto como recuerdo.",
               "¡Esto está recién salido de la lata!",
               "¿Te dijeron lo bien que te conservas?",
               "¡Voy a hacerte una donación de alimentos en conserva!",
               "¡Prepárate para una buena lata!",
               "Me gusta que \"conserves\" todos tus ánimos.",
               "¡Te voy a poner en conserva!",
               "¡El menú de hoy va a ser dibu enlatado!",
               "\"Conserva\" esto para el recuerdo...",
               ],
    'Chomp': ["¿Quieres hacer el favor de masticar bien?",
              "¡Ñam, ñam, ñam!",
              "No te olvides de cerrar la boca al comer.",
              "¿Tienes ganas de masticar algo?",
              "Prueba a masticar esto.",
              "¡Vas a ser mi cena!",
              "¡Me encantan las dietas a base de dibus!",
              ],
    'ClipOnTie': ["¿Por qué no te arreglas un poco?",
                  "¡Tienes que llevar corbata a las reuniones!",
                  TheCogs + "elegantes siempre se ponen una de éstas...",
                  "Pruébate ésta, a ver qué tal te queda.",
                  "La imagen es fundamental para tener éxito en la vida.",
                  "Aquí no se admite a nadie sin corbata.",
                  "¿Quieres que te ayude a ponerte esto?",
                  "Una buena corbata dice mucho de ti.",
                  "Veamos qué tal te queda esto.",
                  "Esto a lo mejor te aprieta un poco.",
                  "Es mejor que te arregles antes de MARCHARTE.",
                  "Toma, con esto serás el dibu más apuesto del dibuparque.",
                  ],
    'Crunch': ["Parece que estás un poco crujido.",
               "¡Es hora de crujirse un poco!",
               "Con esto te van a crujir las articulaciones.",
               "¡Mira qué crujiente tan delicioso!",
               "¿No oyes un crujido?",
               "¿Qué prefieres, blandito o crujiente?",
               "Esto está crujiente y apetitoso.",
               "¡Prepárate para que te crujan los huesos!",
               "¡Me encantan los postres crujientes!"
               ],
    'Demotion': ["Vas a bajar puestos en la empresa. ",
                 "Vas a volver a trabajar de botones.",
                 "Me parece que te quedaste sin despacho.",
                 "¡Amigo, vas para abajo!",
                 "Creo que tu puesto peligra.",
                 "Tienes poco futuro en esta empresa.",
                 "Laboralmente, estás en un callejón sin salida.",
                 "Tu puesto en la empresa se está tambaleando.",
                 "Te veo preparando café bien pronto.",
                 "Esto va a ir directo a tu expediente.",
                 ],
    'Downsize': ["¿Qué tal unos cuantos recortes?",
                 "A veces hay que aplicar las tijeras.",
                 "Yo que tú iría pidiendo entrevistas de trabajo.",
                 "¿Guardaste el suplemento de empleo de tu periódico?",
                 "¿Nunca te dijeron que eres prescindible?",
                 "Tu perfil no se ajusta a nuestras necesidades actuales.",
                 "¿Oíste hablar de las reestructuraciones?",
                 "Me temo que ya no nos eres útil.",
                 "¿Por qué no te buscas un trabajo en otro sitio?",
                 "No pasas de este año en esta empresa.",
                 "Me temo que los cambios en la empresa te van a afectar.",
                 "Me temo que nos sobra algo de personal.",
                 ],
    'EvictionNotice': ["¡Llegó la hora de la mudanza!",
                       "Haz las maletas, dibu.",
                       "Creo que vas a tener que cambiar de residencia.",
                       "Dicen que debajo del puente se está muy bien.",
                       "Me temo que no pagaste el alquiler.",
                       "¿Habías pensado en redecorar tu vivienda?",
                       "A partir de ahora vas a disfrutar del aire libre.",
                       "¿No decías que te gustaban los espacios abiertos?",
                       "¡Estás fuera de lugar!",
                       "Prepárate para ser reubicado.",
                       "Tranquilo; ahora vas a conocer a más gente.",
                       "Vas a hacer un tour de hostales.",
                       ],
    'EvilEye': ["Te voy a echar el mal de ojo.",
                "¿Puedes echarle un ojo a esto?",
                "Espera.  Se me metió algo en el ojo.",
                "¡Te eché el ojo!",
                "En la vida hay que tener ojo para todo.",
                "Tengo mucho ojo para el mal.",
                "¡Te voy a meter el dedo en el ojo!",
                "¡Ten mucho ojo conmigo!",
                "¡Te voy a meter en el ojo del huracán!",
                "¡No te pienso quitar ojo!",
                ],
    'Filibuster':["¿Te gustan los discursos?",
                  "Esto va a durar un ratito.",
                  "Podría estar así todo el día.",
                  "No me hace falta tomarme ni un respiro.",
                  "Puedo seguir y seguir.",
                  "Nunca me canso de hacer esto.",
                  "Soy capaz de aburrir a las ovejas.",
                  "¿Te importa si digo unas palabras?",
                  "Creo que voy a soltar un discursito.",
                  "Tengo preparadas unas frases para ti.",
                  ],
    'FingerWag': ["Te lo dije un millón de veces.",
                  "Dibu, te estoy hablando a ti.",
                  "No me hagas reír.",
                  "No me hagas ir hasta ahí.",
                  "Estoy harto de repetírtelo.",
                  "Creo que ya te dije esto.",
                  "No nos tienes ningún respeto a los bots.",
                  "Es hora de que empieces a prestar atención.",
                  "Bla, bla, bla, bla, bla.",
                  "Voy a tener que aplicarte un correctivo.",
                  "¿Cuántas veces te lo tengo que decir?",
                  "No es la primera vez que pasa esto.",
                  ],
    'Fired': ["Espero que te trajeras algo para la barbacoa.",
              "Esto va a ponerse calentito.",
              "Seguro que con esto entras en calor.",
              "Espero que seas un animal de sangre fría.",
              "¡Caliente, caliente!",
              "Creo que te va a hacer falta un extintor.",
              "¡Vas a quedarte chamuscado!",
              "¡Vas a quedar muy doradito!",
              "Esto le da otro significado a la expresión \"a punto\".",
              "Espero que te pusieras protección solar.",
              "Avísame cuando estés crujiente.",
              "La cosa está que arde.",
              "Vas a arder en deseos de volver al dibuparque.",
              "Creo que tienes un temperamento ardiente.",
              "A ver, déjame que te ponga el termómetro...",
              "¡Tienes mucha chispa!",
              "El que juega con fuego...",
              "¿Nunca te dijeron que te sale humo de las orejas?",
              ],
    'FountainPen': ["Esta mancha no va a salir. ",
                    "Vas a tener que ir a la tintorería.",
                    "Prepárate para comprar detergente.",
                    "Esto no es precisamente tinta invisible.",
                    "Vas a tener que cambiarte de ropa.",
                    "La tinta de esta pluma no se acaba nunca.",
                    "Toma, usa mi pluma.",
                    "¿Lees bien mi letra?",
                    "Ya no hacen plumas como las de antes.",
                    "Vaya, hay un borrón en tu expediente.",
                    "Te dije que no cargaras las tintas.",
                    ],
    'FreezeAssets': ["¿Te sirvo un poco de hielo?",
                     "Te voy a juzgar por tus acciones.",
                     "Me parece que voy a pasar a la acción.",
                     "Voy a congelar la imagen.",
                     "El ambiente está muy frío.",
                     "Este año se va a adelantar el invierno.",
                     "Esto te enfriará los ánimos.",
                     "Mi plan está a punto de cristalizar.",
                     "Te vas a quedar petrificado.",
                     "Se te van a congelar las ideas.",
                     "¿Te gustan las cenas frías?",
                     "Voy a refrescarte la memoria.",
                     ],
    'GlowerPower': ["¿Me miras a mí?",
                    "Me dijeron que tengo una mirada penetrante.",
                    "Mírame fijamente a los ojos...",
                    "¿Te gusta mi caída de ojos?",
                    "Tengo una mirada arrebatadora.",
                    "¿No te parecen unos ojos muy expresivos?",
                    "Siempre me dijeron que tengo unos ojos preciosos.",
                    "El secreto está en la mirada.",
                    "¡Veo, veo! ¡Veo un dibu en apuros!",
                    "Deja que te mire bien...",
                    "¿Echamos una mirada a tu futuro?",
                    ],
    'GuiltTrip': ["¡Vas a cargar con toda la culpa!",
                  "¿Te sientes culpable?",
                  "¡Todo es culpa tuya!",
                  "¡Te pienso culpar por todo!",
                  "¡Declarado culpable!",
                  "¡No pienso volver a hablarte!",
                  "¡Más te valdría pedir perdón!",
                  "¡No te pienso perdonar en la vida!",
                  "¿No crees que te portaste mal?",
                  "¡No intentes echarme la culpa!",
                  "¡Eres un culpable con causa!",
                  ],
    'HalfWindsor': ["¡Esta es la corbata más hermosa que jamás viste!",
                    "Intenta no hacerte un nudo.",
                    "Se te va a hacer un nudo en el estómago.",
                    "Tienes suerte de que sea un nudo fácil.",
                    "¿No se te hace un nudo en la garganta?",
                    "¡Seguro que no sabes ni hacerte el nudo!",
                    "¡Después de esto te voy a anudar la lengua!",
                    "No debería malgastar esta corbata contigo.",
                    "¡No te mereces esta corbata tan linda!",
                  ],
    'HangUp': ["Se cortó tu llamada.",
               "¡Adiós!",
               "Es el momento de terminar la conexión.",
               "¡...Y no vuelvas a llamarme!",
               "¡Clic!",
               "Se acabó la conversación.",
               "Voy a cortar la línea.",
               "Creo que tienes la línea en mal estado.",
               "Me parece que no tienes línea.",
               "Finalizó tu llamada.",
               "Espero que me escuches alto y claro.",
               "Te equivocaste de número.",
               ],
    'HeadShrink': ["¿Estuviste recientemente en el Amazonas?",
                   "Cariño, encogí a un dibu.",
                   "Espero que tu orgullo no se quede encogido.",
                   "¿Encogiste en la lavadora?",
                   "Te dije que no te laves con agua caliente.",
                   "No pierdas la cabeza por esto.",
                   "¿Es que perdiste la cabeza?",
                   "¡Pero qué poca cabeza tienes!",
                   "¡Eres un cabeza de chorlito!",
                   "No sabía que pasaste una temporada con los jíbaros.",
                   ],
    'HotAir':["El ambiente se está acalorando.",
              "Vas a sufrir una ola de calor.",
              "Llegué al punto de ebullición.",
              "Me parece que te vas a achicharrar un poco.",
              "Vas a quedar un poco doradito...",
              "Recuerda: si ves humo, es que hay fuego.",
              "Te veo un poco quemado.",
              "Creo que hoy va a haber fumata blanca.",
              "Supongo que es la hora de avivar un poco el fuego.",
              "Permíteme que encienda la llama del amor.",
              "¡Esto se va a poner al rojo vivo!",
              "¿Te seco un poco el pelo?",
              ],
    'Jargon':["Qué cantidad de tonterías se dicen...",
              "A ver si adivinas qué significa esto.",
              "Espero que me recibas alto y claro.",
              "Me parece que voy a tener que hablar más alto.",
              "Insisto; es mi turno para hablar.",
              "Te voy a ser muy sincero.",
              "Debo pontificar sobre este asunto.",
              "¿Ves? Las palabras pueden hacer daño.",
              "¿Comprendiste lo que quiero decir?",
              "Palabras, palabras, palabras...",
              ],
    'Legalese':["Debes cejar en tu empeño.",
                "En términos legales, vas a perder el juicio.",
                "¿Estás al tanto de las connotaciones legales?",
                "¡No puedes situarte al margen de la ley!",
                "Deberían hacer una ley expresamente contra ti.",
                "Me reservo el derecho de modificar tu contrato.",
                "Las opiniones expresadas en este ataque no coinciden con las de Toontown Online.",
                "No me hago responsable de los daños derivados de este ataque.",
                "Vas a asumir los costes directos e indirectos de este ataque.",
                "Me reservo el derecho de prolongar este ataque.",
                "¡Estás fuera de mi sistema legal!",
                "No vas a poder asumir los costes legales de este ataque.",
                ],
    'Liquidate':["Me encanta que nuestra relación sea fluida.",
                 "¿Estás teniendo problemas de liquidez?",
                 "Voy a tener que ponerte en remojo.",
                 "Hay que dar fluidez a este proceso.",
                 "¡Recuerda que el suelo está resbaladizo!",
                 "Tu dinero es papel mojado.",
                 "En esta vida hay que mojarse un poco.",
                 "Te voy a poner en venta al 50 %.",
                 "Te vas a diluir un poco...",
                 "Me apetece un dibu pasado por agua.",
                 ],
    'MarketCrash':["Me parece que tus acciones se desplomaron.",
                   "No vas a sobrevivir al cierre de sesión.",
                   "Tus valores caen en picado.",
                   "Tu cartera de acciones va a quedarse temblando.",
                   "Va a ser todo un lunes negro para ti.",
                   "Hoy estoy de lo más alcista.",
                   "Creo que me voy a desprender de tus acciones.",
                   "¡Más vale que vendas todo pronto!",
                   "¡Vende, rápido!",
                   "Vas a iniciar una tendencia bajista.",
                   "El mercado se va a desplomar encima de ti.",
                   ],
    'MumboJumbo':["Voy a ver si me expreso con claridad.",
                  "Es así de sencillo.",
                  "Te voy a explicar cómo vamos a resolver esto.",
                  "Permíteme que te resuma esto.",
                  "A lo mejor esto te suena a discurso.",
                  "No quiero soltarte una parrafada, pero...",
                  "Uy, se me llena la boca.",
                  "Odio alargarme en mis peroratas.",
                  "Permíteme unas palabritas.",
                  "Tengo preparado un discursito para ti.",
                  ],
    'ParadigmShift':["¡Cuidado! Hoy estoy de lo más cambiante.",
                     "¡Prepárate para un buen golpe de timón!",
                     "Creo que hay que enderezar tu rumbo.",
                     "Vas a tener un ligero cambio de perspectiva.",
                     "Acabarás cambiando de lugar.",
                     "¡Perdiste el norte!",
                     "Seguro que nunca cambiaste tanto de orientación.",
                     "¡Creo que no te va a gustar este cambio!",
                     "¡No me hagas cambiar de parecer!",
                     ],
    'PeckingOrder':["Sí; soy todo un pájaro.",
                    "Más vale pájaro en mano...",
                    "Me dijo un pajarito que vas a volver de un golpe al dibuparque.",
                    "¡No huyas como un gallina!",
                    "Creo que tienes la cabeza llena de pájaros.",
                    "¡Cría cuervos y tendrás muchos!",
                    "¡Ya volaste bastante, pajarito!",
                    "Me encanta salir a picar algo.",
                    "Voy a hacer un buen caldo de gallina contigo.",
                    ],
    'PickPocket': ["Deja que me haga cargo de tus objetos personales.",
                   "¿A ver qué llevas ahí?",
                   "Esto es como quitarle un caramelo a un niño.",
                   "Qué robo...",
                   "Espera, yo te lo tengo.",
                   "No pierdas de vista mis manos.",
                   "La mano es más rápida que el ojo...",
                   "Nada por aquí...",
                   "La dirección no se hace responsable de los objetos perdidos.",
                   "Santa Rita, Rita...",
                   "No te vas a dar ni cuenta.",
                   "Te voy a dejar en cueros.",
                   "¿Te importa si me quedo con esto?",
                   "Te voy a aligerar de peso.",
                   ],
    'PinkSlip': ["Tengo algo de correspondencia para ti.",
                 "¿Estás asustado? ¡Te pusiste pálido!",
                 "Esta carta te va a hacer mucha ilusión.",
                 "Vaya; creo que alguien va a tener que hacer las maletas.",
                 "¡Eh, no te vayas sin despedirte!",
                 "¿Te despediste ya de todo el mundo?",
                 "¡Mira, una carta de amor!",
                 "Creo que este papel es para ti...",
                 "Qué tristes son las despedidas.",
                 "¡Aquí tienes tu carta de despido. Largo de aquí!",
                 ],
    'PlayHardball': ["¿Así que quieres jugar al béisbol?",
                     "No te recomiendo que juegues conmigo.",
                     "¡Batea de una vez!",
                     "¡Vamos, batea esto!",
                     "¡Y aquí viene el lanzamiento...!",
                     "Vas a tener que mandarla lejos.",
                     "Te voy a sacar del estadio de un batazo.",
                     "Te voy a mandar al dibuparque de un batazo.",
                     "¡Esta es tu carrera final!",
                     "¡No vas a poder jugar conmigo!",
                     "¡Te voy a poner en órbita!",
                     "¡Vas a ver qué bola te lanzo!",
                    ],
    'PoundKey': ["Es hora de devolver algunas llamadas.",
                 "¿Qué tal una llamada gratis?",
                 "¡Ring, ring! ¡Es para ti!",
                 "Toma, para que me llames cuando quieras.",
                 "Me sobra una almohadilla...",
                 "Espero que tu teléfono sea de tonos.",
                 "Déjame que marque este número.",
                 "Voy a hacer una llamada sorpresa.",
                 "Espera, te voy a dar un toque.",
                 "Dibu, sólo puedes hacer una llamada.",
                 ],
    'PowerTie': ["Te veré más tarde; parece que se te hizo un nudo en la garganta.",
                 "Voy a atar unos cuantos cabos sueltos.",
                 "¡Con esto vas a estar muy elegante!",
                 "Para que vayas practicando los nudos...",
                 "Ya es hora de que empieces a vestir bien.",
                 "¡Esta es la corbata más fea que jamás viste!",
                 "¿No te sientes importante usando esto?",
                 "¡Vas a ver cómo cambia tu aspecto!",
                 "¡Nada mejor que una corbata de regalo!",
                 "No sabía qué regalarte, así que ¡toma!",
                 ],
    'PowerTrip': ["Haz las maletas, que nos vamos de excursión.",
                  "¿Tuviste un buen viaje?",
                  "Lindo viaje; te veré el año que viene.",
                  "¿Qué tal tu viaje?",
                  "¡Siento que hayas tenido que venir hasta aquí!",
                  "¡Me parece que vas a irte de viaje!",
                  "¡Vas a ver lo que es viajar!",
                  "¿Te gusta la astrología?",
                  "¿Quieres tener una experiencia astral?",
                  "¡Vas a ver las estrellas!",
                  "Prepara las maletas, te vas de viaje... ¡astral!",
                  ],
    'Quake': ["¿Qué tal una sacudidita de tierra?",
              "Me encantan los modelos a escala... Richter.",
              "Eres todo un terremoto, ¿eh?",
              "¿A que no sabes dónde está el epicentro?",
              "Este se va a salir de la escala Richter.",
              "¡Con esto se van a sacudir los cimientos!",
              "¡Vas a ver qué sacudón!",
              "¿Estuviste alguna vez en un terremoto?",
              "¡Cuidado; la tierra se agita bajo tus pies!",
              ],
    'RazzleDazzle': ["Léeme los labios.",
                     "¿Te gustan mis dientes?",
                     "¿No te parezco encantador?",
                     "Disfruta de mi encantadora sonrisa...",
                     "Mi dentista es un gran profesional.",
                     "Una sonrisa cegadora, ¿eh?",
                     "Parece mentira que sean postizos, ¿eh?",
                     "Una sonrisa arrebatadora, ¿eh?",
                     "Suelo anunciar dentífricos, ¿sabes?",
                     "Siempre uso hilo dental después de comer.",
                     "¡Di \"Whisky \"!",
                     ],
    'RedTape': ["Te voy a envolver para regalo.",
                "Voy a dejar todo atado y bien atado.",
                "¡Cómo te enrollas!",
                "A ver si puedes cortar esta cinta roja.",
                "Vas a estar un poco estrecho ahí.",
                "Espero que no tengas claustrofobia.",
                "Me aseguraré de que no vayas a ninguna parte.",
                "Espera; te voy a aislar.",
                "¡Vamos a inaugurar un nuevo dibu!",
                "Quiero que sientas apego por mí.",
                ],
    'ReOrg': ["¡No te va a gustar la forma en que lo reorganicé todo!",
              "Creo que hace falta un poco de reorganización.",
              "No estás tan mal, sólo hay que reorganizarte.",
              "¿Te gusta mi capacidad de reorganización?",
              "Pensé que le iría bien una nueva imagen a todo.",
              "¡Hay que reorganizarte!",
              "Pareces un poco desorganizado.",
              "Espera; voy a reorganizar tus pensamientos.",
              "Voy a esperar a que te reorganices un poco.",
              "¿Te importa si organizo un poco todo esto?",
              ],
    'RestrainingOrder': ["Deberías alejarte un poco.",
                         "¡Me encargaron que te dé una orden de alejamiento!",
                         "No te puedes acercar a menos de dos metros de mí.",
                         "Creo que deberías guardar las distancias.",
                         "Debería alejarte para siempre.",
                         "¡Hay que alejar a este dibu!",
                         "Intenta alejar tu mente de todo esto.",
                         "Espero que todo esto no te aleje demasiado de la realidad.",
                         "¡A ver si consigues acercarte ahora!",
                         "¡Te ordeno que te alejes!",
                         "¿Por qué no empezamos por alejar posiciones?"
                         ],
    'Rolodex': ["Tengo tu dirección en algún sitio.",
                "Aquí tengo el número de la perrera. ",
                "Espera; te voy a dar mi tarjeta.",
                "Tengo tu número aquí mismo.",
                "Te tengo controlado de la A a la Z.",
                "Te tengo más que fichado.",
                "¡Esquiva esto!",
                "Cuidado; no te cortes con los bordes.",
                "Voy a darte unas cuantas direcciones útiles.",
                "Toma; llámame a estos números.",
                "Quiero asegurarme de que sigamos en contacto.",
                ],
    'RubberStamp': ["Me gusta dar siempre una buena impresión.",
                    "Es importante aplicar una presión firme.",
                    "Dejo siempre una buena huella.",
                    "Te voy a dejar más plano que un sello.",
                    "Hay que DEVOLVERTE AL REMITENTE.",
                    "Fuiste CANCELADO.",
                    "Voy a mandarte al dibuparque con sello URGENTE.",
                    "Creo que te vas a sentir muy RECHAZADO.",
                    "Para mandarte al dibuparque no hará falta FRANQUEO.",
                    "Vas a ir al dibuparque POR AVIÓN.",
                    ],
    'RubOut': ["Y ahora, la desaparición final.",
               "Me parece que te perdí.",
               "Decidí que te quedas fuera.",
               "Siempre elimino todos los obstáculos.",
               "Vaya; voy a borrar este error.",
               "Me gusta que todo lo molesto desaparezca.",
               "Me gusta que todo esté limpio y ordenado.",
               "Por favor, intenta seguir animado.",
               "Ahora te veo... Ahora no te veo.",
               "Creo que vas a ponerte borroso.",
               "Voy a eliminar el problema.",
               "Me voy a ocupar de tus áreas problemáticas.",
               ],
    'Sacked':["Cuidado; viene el hombre del saco.",
              "¡Te tengo en el saco!",
              "¿Te apetece echar una carrera de sacos?",
              "¿Sacas tú o saco yo?",
              "¡Voy a ponerte a buen recaudo!",
              "Tengo el récord de carreras de sacos.",
              "Te voy a sacar de aquí...",
              "¡Se acabó; te voy a meter en el saco!",
              "¡No nos metas a todos los bots en el mismo saco!",
              "Todos me dicen que tengo un buen saque.",
              ],
    'Schmooze':["Seguro que no te esperabas esto.",
                "Esto te va a quedar muy bien.",
                "¡Te lo ganaste!",
                "No quiero aburrirte con mi discurso.",
                "Adular a la gente me da buenos resultados.",
                "Voy a exagerar un poquito.",
                "Es hora de animar un poco al personal.",
                "Ahora hablemos un poco de ti.",
                "Te mereces una palmadita en la espalda.",
                "Llegó el momento de alabar tu trayectoria.",
                "Siento tener que bajarte de tu pedestal, pero...",
                ],
    'Shake': ["Estás justo en el epicentro.",
              "Estás pisando una falla.",
              "Esto va a estar movidito...",
              "Creo que va a ocurrir un desastre natural.",
              "Es un desastre de proporciones sísmicas.",
              "Éste se va a salir de la escala Richter.",
              "Es hora de ponerse a cubierto.",
              "Pareces alterado.",
              "¿Listo para bailar el meneíto?",
              "No te agites demasiado, por favor.",
              "Esto te va a poner patas arriba.",
              "Te recomiendo un buen plan de escape.",
              ],
    'Shred': ["Tengo que deshacerme de bastante basura.",
              "Voy a reciclar un poco de papel.",
              "Creo que me voy a deshacer de ti ahora mismo.",
              "Con esto me desharé de las pruebas.",
              "Ya no hay manera de demostrar nada.",
              "A ver si consigues recomponer esto.",
              "Esto te va a hacer trizas.",
              "Voy a triturar esa idea.",
              "No quiero que esto caiga en malas manos.",
              "Adiós a las pruebas.",
              "Creo que esta era tu última esperanza.",
              ],
    'Spin': ["¿Te apetece ir a dar una vuelta?",
             "¿Qué tal si te centrifugo un poco?",
             "¡Tu cabeza va a dar vueltas con esto!",
             "Voy a dar otra vuelta de tuerca.",
             "Te voy a dar una vuelta.",
             "Yo siempre estoy de vuelta de todo.",
             "Cuidado.  La vida da muchas vueltas.",
             "¡Vamos a hacer un doble giro mortal!",
             "Un poco más y de vuelta al dibuparque.",
             ],
    'Synergy': ["Voy a presentar esto en el comité.",
                "Tu proyecto fue cancelado.",
                "Cortamos tus fondos.",
                "Estamos reestructurando tu división.",
                "Lo sometí a votación y perdiste.",
                "Acabo de recibir la aprobación final.",
                "Un buen equipo puede superar cualquier problema.",
                "Luego me ocuparé de esto contigo.",
                "Vamos a ir al grano.",
                "Considera esto una crisis sinergética.",
                ],
    'Tabulate': ["Esto no me cuadra.",
                 "No te salen las cuentas.",
                 "Te va a salir una cuenta enorme.",
                 "Voy a desglosarte en un momento.",
                 "¿Estás listo para unas cifras aterradoras?",
                 "Es hora de que pagues la dolorosa.",
                 "Hora de saldar cuentas...",
                 "Me encanta tener las cuentas claras.",
                 "Las cuentas claras conservan la enemistad.",
                 "Estos números van a dejarte con la boca abierta.",
                 ],
    'TeeOff': ["Tienes un par nefasto.",
               "¡Bola!",
               "Vas a ver qué bien le pego.",
               "¡Caddie, dame un hierro!",
               "A ver si mejoras este golpe.",
               "¡Mira qué swing!",
               "Ésta bola va a entrar de un solo golpe.",
               "Estás pisando mi green.",
               "Fíjate qué buen grip tengo.",
               "¡Mira qué birdie!",
               "¡No pierdas de vista la bola!",
               "¿Te importa si juego un poco?",
               ],
    'Tremor': ["¿Sentiste eso?",
               "No te dan miedo los temblores, ¿verdad?",
               "Los temblores suelen ser el principio.",
               "Pareces tembloroso.",
               "¡Voy a agitar un poco las cosas!",
               "¿Estás listo para bailar la rumba?",
               "¿Qué te pasa? Pareces agitado.",
               "¡Tiembla de miedo!",
               "¿Por qué tiemblas?",
               ],
    'Watercooler': ["Esto te refrescará un poco.",
                    "¿No es refrescante?",
                    "Venía a entregar un pedido.",
                    "¡Pruébala; está fresquita!",
                    "¿Qué pasa? ¡Es sólo agua!",
                    "No te preocupes; es agua potable.",
                    "Qué bien; otro cliente satisfecho.",
                    "Es la hora de entregar el pedido diario.",
                    "Espero que no destiñas.",
                    "¿Te apetece un trago?",
                    "Hay que dar de beber al sediento.",
                    "¿No tenías sed? ¡Pues toma!",
                    ],
    'Withdrawal': ["Creo que te quedaste sin fondos",
                   "Espero que tengas suficientes fondos en tu cuenta.",
                   "¡Toma, con intereses!",
                   "Te estás quedando sin liquidez.",
                   "Pronto vas a tener que hacer un depósito.",
                   "Estás al borde del colapso económico.",
                   "Creo que estás en recesión.",
                   "Tus números se van a ver afectados.",
                   "Preveo una crisis inminente.",
                   "¡Vas a tener un agujero en tu cuenta!",
                   ],
    'WriteOff': ["Permíteme que incremente tus deudas.",
                 "Vamos a intentar sanear tu situación.",
                 "Es hora de hacer el balance de tus cuentas.",
                 "Esto no va a quedar nada bien en tu libro de contabilidad.",
                 "Estoy buscando dividendos.",
                 "¿Por qué no haces balance de tus pérdidas?",
                 "Olvídate de la gratificación que te toca.",
                 "Voy a poner patas arriba tus cuentas.",
                 "Creo que tus pérdidas van a ser cuantiosas.",
                 "Tu saldo se va a ver un poco afectado.",
                 ],
    }

# DistributedBuilding.py
BuildingWaitingForVictors = "Esperando a otros jugadores...",

# Elevator.py
ElevatorHopOff = "Bajarse"
ElevatorStayOff = "Si te bajas, tendrás que esperar\na que el ascensor marche o se vacíe."
ElevatorLeaderOff = "Sólo tu líder puede decidir cuándo bajarse."
ElevatorHoppedOff = "Tienes que esperar al siguiente ascensor."
ElevatorMinLaff = "Necesitas %s puntos de risa para viajar en este ascensor."
ElevatorHopOK = "OK"
ElevatorGroupMember = "Sólo tu líder de grupo puede\n decidir cuando subir."

# DistributedCogKart.py
KartMinLaff = "Necesitas %s puntos de risa para subirte a este kart"

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = ", Inc."
CogsIncModifier = "%s" + CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Toc, toc."
DoorWhosThere = "¿Quién es?"
DoorWhoAppendix = " qué?"
DoorNametag = "Puerta"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "¡Tú necesitas bromas! Ve a hablar con Tato Tutorial"
FADoorCodes_DEFEAT_FLUNKY_HQ = "¡Vuelve cuando hayas derrotado al Secuaz!"
FADoorCodes_TALK_TO_HQ = "¡Ve y consigue tu recompensa del funcionario Enrique!"
FADoorCodes_WRONG_DOOR_HQ = "¡Puerta incorrecta! ¡Sal por la otra puerta al dibuparque!"
FADoorCodes_GO_TO_PLAYGROUND = "¡Salida equivocada! ¡Necesitas salir al dibuparque!"
FADoorCodes_DEFEAT_FLUNKY_TOM = "¡Acércate al Secuaz para combatir con él!"
FADoorCodes_TALK_TO_HQ_TOM = "¡Ve y consigue tu recompensa en el cuartel general!"
FADoorCodes_SUIT_APPROACHING = None # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "¡Cuidado! ¡Hay un bot dentro!"
FADoorCodes_SB_DISGUISE_INCOMPLETE = "Si vas como dibu te van a pescar. Primero tendrás que armarte un disfraz de bot completo.\n\nHáztelo con piezas de la fábrica."
FADoorCodes_CB_DISGUISE_INCOMPLETE = "¡Si vas como dibu te van a pescar! ¡Primero, necesitas completar tu disfraz de chequebot!\n\nCrea tu disfraz de chequebot haciendo las dibutareas en Sueñolandia de Donald."
FADoorCodes_LB_DISGUISE_INCOMPLETE = "¡Si vas como dibu te van a pescar! ¡Primero, necesitas completar tu disfraz de abogabot!\n\nCrea tu disfraz de abogabot haciendo las dibutareas después de Sueñolandia de Donald."
FADoorCodes_BB_DISGUISE_INCOMPLETE = "¡Si vas como dibu te van a pescar! ¡Primero, necesitas completar tu disfraz de jefebot!\n\nCrea tu disfraz de jefebot haciendo las dibutareas después de Sueñolandia de Donald."

# KnockKnock joke contest winners
KnockKnockContestJokes = {
    2100 : ["Eloy",
            "¡Eloy es importante, el mañana también!"],

    # 2009 April fools contest Jokes. First few doors of Loopy lane
    2200 : {28:["Pasta",
            "¡Pasta de bromas, que vienen los bots!"],
            41:["Tomas",
            "¿Qué es de Tomas? ¿Qué Tomas? Un café."],
            40:["Mickey",
            "¡Mickedado sin nada, es una locura!"],
##            25:["Pasta25",
##            "¡Pasta de bromas, que vienen los bots!"],
            27:["Traje",
            "¡Yo no traje traje!"]},

    2300: ["Carlos",
           "¡A los bots, hay que bus-Carlos por todas partes!"],

    # Polar Place has multiple jokes so they are in a dict keyed of the propId of the door
    3300: { 10: ["Aladino",
                   "Hasta A-la-dino sauria le llegó su hora."],
            6 : ["Tipo",
                 "¿Tipo nemos más piezas de bot?"],
            30 : ["Mesa",
                  "Mesa caído un trozo de tarta."],
            28: ["Tele",
                 "¿Tele vas a comer?"],
            12: ["Harta",
                 "¿Harta donde vamos a llegar con esto?"],
            },
     }

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Aitor ",
    "¡Aitor Tilla de Patatas!"],

    ["Adela",
    "¡Adela Miendo!"],

    ["Abraham",
    "¡Abraham Lapuerta!"],

    ["Amira",
    "¡Amira Quienhavenido!"],

    ["Aquiles",
    "¡Aquiles Dejoporhoy!"],

    ["Archibaldo",
    "¡Archibaldo Enlascarpetas!"],

    ["Armando",
    "¡Armando Lío!"],

    ["Alicia",
    "Alicia Nuro"],

    ["Augusto",
    "¡Augusto de Conocerle!"],

    ["Azucena",
    "¡Azucena Estaservida!"],

    ["Baldomero",
    "¡Baldomero Alaplancha!"],

    ["Baltasar",
    "¡Baltasar Ysecayó!"],

    ["Belinda",
    "¡Belinda Flordeljardín!"],

    ["Beltrán",
    "¡Beltrán Kilo!"],

    ["Bernabé",
    "¡Bernabé Abrirlapuerta!"],

    ["Blasa",
    "¿Blasa Brironó?"],

    ["Carmen",
    "¡Carmen Tolada y Fresca!"],

    ["Calixto",
    "¡Calixto Queesuno!"],

    ["Camila",
    "¡Camila Groquehayavenido!"],

    ["Cintia",
    "¡Cintia Palpelo!"],

    ["Clemente",
    "¡Clemente Privilegiada!"],

    ["Cleopatra",
    "¡Cleopatra Jeado!"],

    ["Clotilde",
    "¡Clotilde Monio!"],

    ["Consuelo",
    "¡Consuelo Fregado!"],

    ["Crisóstomo",
    "¡Crisóstomo Uncafeconleche!"],

    ["Demetrio",
    "¡Demetrio Doloquetenga!"],

    ["Bernabé",
    "¡Bernabé Quiénvino!"],

    ["Edmundo",
    "¡Edmundo Esunpañuelo!"],

    ["Engracia",
    "¡Engracia Porabrirlapuerta!"],

    ["Estela",
    "¡Estela Marinera!"],

    ["Eugenio",
    "¡Eugenio de la Lámpara!"],

    ["Ezequiel",
    "¿Ezequiel Es?"],

    ["Fabiola",
    "¡Fabiola Iadiós!"],

    ["Filomeno",
    "Filomeno Malquehellegado."],

    ["Florinda",
    "¡Florinda Se y Arribalasmanos!"],

    ["Gaspar",
    "¡Gaspar Ecequevallover!"],

    ["Genoveva",
    "¡Genoveva Desabotella!"],

    ["Jairo",
    "¡Jairo Níasdelavida!"],

    ["Jazmín",
    "¡Jazmín Nero del Carbón!"],

    ["Jeremías",
    "¡Jeremías Sonpasiempre!"],

    ["Jessica",
    "¡Jessica Nálisis Gratuito!"],

    ["Jesús",
    "¡Jesús Piros Románticos!"],

    ["Rafa",
    "Rafa Bricante"],

    ["Kevin",
    "¿Kevin Olesirvo?"],

    ["Leonor",
    "¡Leonor Gulloso de su Melena!"],

    ["Menchu",
    "Menchu Letón"],

    ["Macarena",
    "¡Macarena Blanca de la Playa!"],

    ["Magdalena",
    "¡Magdalena Ycafé Conleche!"],

    ["Maite",
    "¡Maite Digoquesoyyó!"],

    ["Marcos",
    "¡Marcos Tilla!"],

    ["Armando",
    "¡Armando de la Tropa!"],

    ["Olimpia",
    "¡Olimpia Osevá!"],

    ["Olivia",
    "¡Olivia Tuabuela!"],

    ["Omar",
    "¡Omar Ejada!"],

    ["Oscar",
    "¡Oscar Naval de Río!"],


    ["Pánfilo",
    "¡Pánfilo de la Navaja!"],

    ["Pascual",
    "¿Pascual Esugracia?"],

    ["Luisa",
    "Luisa Belotodo"],

    ["Ramiro",
    "¡Raimiro Ynoteveo!"],

    ["Ramona",
    "¡Ramona Vestida de Seda!"],

    ["Raúl",
    "¡Raúl Timo de la Fila!"],

    ["Renato",
    "¡Renato Londrado!"],

    ["Juan Ricardo",
    "¡Juan Ricardo Borriquero!"],

    ["Rubén",
    "Rubén Tana"],

    ["Sabina",
    "Sabina Gre"],

    ["Samanta",
    "¡Samanta de Lana!"],

    ["Sandra",
    "¡Sandra Josa!"],

    ["Serafín",
    "¡Serafín de la Historia!"],

    ["Serena",
    "¡Serena y Tranquila!"],


    ["Servando",
    "¡Servando Lero!"],

    ["Silvio",
    "¡Silvio Lento!"],

    ["Jacobo",
    "Jacobo Rego"],

    ["Elena",
    "Elena Nomaldito"],

    ["Socorro",
    "¡Socorro Carreras!"],

    ["Gala",
    "¡Gala Rdonado!"],



    ["Soledad",
    "¡Soledad y Compañía!"],

    ["Enrique",
    "¡Enrique Cimiento!"],

    ["Tamara",
    "¡Tamara Villosa!"],

    ["Teobaldo",
    "¡Teobaldo Mingo!"],

    ["Ulices",
    "¡Ulices Todepapel!"],

    ["Virgilio",
    "¡Virgilío Mehasmetido!"],

    ["Vladimir",
    "¡Vladimir Ador!"],

    ["Wenceslao",
    "¡Wenceslao de Vainilla!"],

    ["Wenceslao",
    "¡Wenceslao de Chocolate!"],

    ["Amira",
    "¡Amira Quiensoy!"],

    ["Saúl",
    "¡Saúl Timavezquetellamo!"],

    ["Noé",
    "¡Noé Nadieconocido!"],

    ["Noé",
    "¿Noé Verdad?"],

    ["Nadia",
    "¡Nadia Importante!"],

    ["Otto",
    "¡Otto Quenomeconoce!"],

    ["Abel",
    "¡Abel Quienés!"],

    ["Aitana",
    "¡Aitana Sustao!"],

    ["Apolo",
    "¡Apolo Menosavisa!"],

    ["Romualdo",
    "¿Romualdo Lordecabeza?"],


    ["Dolores",
    "¿Dolores Fuertes?"],


    ["Eleazar",
    "¡Eleazar Aleatóriez!"],

    ["Elijah",
    "¡Elijah Elquemasleguste!"],

    ["Elmer",
    "¡Elmer Cader de Venecia!"],

    ["Elpida",
    "¡Elpida Loqueleapetezca!"],

    ["Quique",
    "¡Quique Cosasdice!"],

    ["Euridice",
    "¡Euridice Quelellames!"],

    ["Calvino",
    "¡Calvino Tinto de Verano!"],

    ["Mercedes",
    "¡Mercedes Elpaso!"],

    ["Antón",
    "¡Antón Tería!"],

    ["Merlín",
    "¡Merlin Gote!"],

    ["Minerva",
    "¡Minerva Minfada y Mixaspera!"],

    ["Miranda",
    "¡Miranda Paraotrolado!"],

    ["Morgana",
    "¡Morgana Unoacero!"],

    ["Morfeo",
    "¡Morfeo Quelainjusticia!"],

    ["Pancho",
    "¡Pancho Colate!"],

    ["Parker",
    "¡Parker Levoyacontar!"],

    ["Pasha",
    "¿Pasha Contigo?"],

    ["Patty",
    "Patty Todo Noquieronada."],

    ["Stan",
    "¡Stan Todosdetenidos!"],

    ["Pierre",
    "¡Pierre Naspacorrer!"],

    ["Ida",
    "¡Ida Yvuelta!"],

    ["Savannah",
    "¡Savannah de Lino Blanco!"],

    ["Renata",
    "¡Renata Conchocolate!"],
]

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "¡Hola, %!",
        "Eh, %, me alegro de verte.",
        "¡Me alegro de que vinieras hoy!",
        "¿Cómo estás, %?",
        ]

SharedChatterComments = [
        "Es un nombre estupendo, %.",
        "Me gusta tu nombre.",
        "Cuidado con los bots.",
        "¡Parece que llega el tranvía!",
        "¡Tengo que subir al tranvía para jugar y conseguir tartas!",
        "A veces me subo al tranvía sólo para conseguir la tarta de frutas.",
        "Guau, acabo de deshacerme de un montón de bots. ¡Necesito descansar un poco!",
        "¡Vaya, hay algunos bots que son muy grandotes!",
        "Parece que la pasas muy bien.",
        "Caramba, qué buen día estoy teniendo.",
        "Me gusta lo que llevas puesto.",
        "Creo que esta tarde me voy a ir de pesca.",
        "Diviértete en mi barrio.",
        "¡Espero que lo estés pasando en grande en Toontown!",
        "Me dijeron que en "+lTheBrrrgh+" está nevando.",
        "¿Subiste hoy al tranvía?",
        "Me gustaría conocer a más gente.",
        "Caramba, en "+lTheBrrrgh+" hay un montón de bots.",
        "Me encanta jugar a \"Las traes\". ¿Y a ti?",
        "Los juegos del tranvía son divertidísimos.",
        "Me encanta hacer que la gente se ría.",
        "Ayudar a los amigos es muy divertido.",
        "Ejem, ¿te perdiste?  No olvides que tienes un mapa en el dibucuaderno.",
        "¡Que no te enrieden los bots con su cinta roja!",
        "Me dijeron que Daisy plantó flores nuevas en su jardín.",
        "¡Para mirar hacia arriba, mantén pulsada la tecla Re Pág!",
        "¡Si ayudas a reconquistar los edificios bot, podrás ganar una estrella de bronce!",
        "Si pulsas la tecla Tab, podrás contemplar diferentes vistas de los alrededores.",
        "¡Si pulsas la tecla Ctrl, podrás saltar!",
        ]

SharedChatterGoodbyes = [
        "Me tengo que ir; adiós.",
        "Creo que voy a subir al tranvía para jugar.",
        "Bueno, hasta otra. Te veo luego, %.",
        "Más me vale darme prisa para acabar con los bots.",
        "Es hora de ponerse en marcha.",
        "Lo siento, pero tengo que irme.",
        "Adiós.",
        "¡Hasta luego, %!",
        "Creo que voy a practicar el lanzamiento de magdalenas.",
        "Voy a unirme a un grupo para acabar con unos cuantos bots.",
        "Me alegro de haberte visto hoy, %.",
        "Hoy tengo mucho que hacer. Voy a ponerme en marcha.",
        ]

# Lines specific to each character.
# If a talking char is mentioned, it cant be shared among them all

MickeyChatter = (
        [ # Greetings specific to Mickey
        "Bienvenido al "+lToontownCentral+".",
        "Hola, me llamo "+Mickey+". ¿Cómo te llamas?",
        ],
        [ # Comments
        "Eh, ¿viste a "+Donald+"?",
        "Voy a ver cómo sube la marea en "+lDonaldsDock+".",
        "Si ves a mi amiguito "+Goofy+", dale recuerdos de mi parte.",
        "Me dijeron que "+Daisy+" plantó flores nuevas en su jardín.",
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a "+Minnie+"!",
        "¡Dios mío, llego tarde a mi cita con "+Minnie+"!",
        "Parece que es hora de darle de comer a "+Pluto+".",
        "Creo que voy a "+lDonaldsDock+" a nadar un poco.",
        "Es la hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

VampireMickeyChatter = (
        [ # Greetings specific to Vampire Mickey
        "Bienvenido al "+lToontownCentral+".",
        "Hola, me llamo "+Mickey+". ¿Cómo te llamas?",
        "¡Feliz día de Halloween!",
        "¡Feliz día de Halloween, %!",
        "Bienvenido al Centro del Miedo... Digo... ¡al "+lToontownCentral+"!",
        ],
        [ # Comments
        "¡Qué divertido es disfrazarse para Halloween!",
        "¿Te gusta mi traje?",
        "¡%, cuidado con los bots chupasangres!",
        "¿No te encantan los adornos de Halloween?",
        "¡Cuidado con los gatos negros!",
        "¿Viste al dibu con la cabeza de calabaza?",
        "¡Buuu! ¿Te asusté?",
        "¡No olvides cepillarte los colmillos!",
        "¡No te asustes, es un vampiro amigo!",
        "¿Te gusta mi capa?",
        "¿Te asusté? ¡Es la mejor broma que tengo!",
        "¡Espero que estés disfrutando nuestro Halloween!",
        "¡Qué espeluznante, está tan oscuro como la noche!",
        ],
        [ # Goodbyes
        "Voy a ver esos adornos tan lindos de Halloween.",
        "¡Voy a Melodilandia a sorprender a "+Minnie+"!",
        "¡Voy a darle un susto a otro dibu! ¡Shhh!",
        "¡Voy a hacer truco o trato!",
        "Chsss, ven a asustar gente conmigo.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Bienvenido a Melodilandia.",
        "Hola, me llamo "+Minnie+". ¿Cómo te llamas?",
        ],
        [ # Comments
        "¡La música se siente por todas partes!",
        "No te olvides de montarte en el gran tiovivo.",
        "Llevas un disfraz muy lindo, %.",
        "Eh, ¿viste a "+Mickey+"?",
        "Si ves a mi amigo "+Goofy+", dale recuerdos de mi parte.",
        "Caramba, en Sueñolandia de "+Donald+" hay un montón de "+Cogs+".",
        "Me dijeron que en "+lDonaldsDock+" hay niebla.",
        "No te olvides de probar el laberinto de los "+lDaisyGardens+".",
        "Creo que voy a escuchar música.",
        "Eh, %, mira eso.",
        "Me encanta la música.",
        "¿A que no sabías que a Melodilandia también la llaman Cancioncity?  ¡Ji, ji!",
        "Me encanta jugar al juego de imitar movimientos. ¿Y a ti?",
        "Me encanta hacer reír a la gente.",
        "¡Uf, andar todo el día con tacones acaba haciendo daño a los pies!",
        "Qué camisa más linda, %.",
#        "¿No te encanta el juego de imitar movimientos?",   # minnie prefers the Match game of course!
        "¿Eso del suelo es una golosina?",
        ],
        [ # Goodbyes
        "¡Vaya, llego tarde a mi cita con %s!" % Mickey,
        "Creo que es hora de darle de comer a %s." % Pluto,
        "Es la hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

DaisyChatter = (
        [ # Greetings
        "¡Bienvenido a mi jardín!",
        "Hola, soy "+Daisy+". ¿Cómo te llamas?",
        "¡Me alegro de verte, %!",
        ],
        [ # Comments
        "Mi flor premiada está en el centro del laberinto del jardín.",
        "Me encanta pasear por el laberinto.",
        "No vi a "+Goofy+" en todo el día.",
        "Me pregunto dónde estará "+Goofy+".",
        "¿Viste a "+Donald+"? No lo encuentro.",
        "Si ves a mi amiga "+Minnie+", salúdala de mi parte.",
        "Cuanto mejor sean tus herramientas de jardinería, mejores serán tus plantas.",
        "Hay demasiados "+Cogs+" cerca de "+lDonaldsDock+".",
        "Si riegas tu jardín todos los días, las plantas estarán felices.",
        "Para cultivar una margarita rosa, planta juntas una golosina roja y otra amarilla.",
        "Las margaritas amarillas son fáciles de cultivar, solo tienes que plantar una golosina amarilla.",
        "¡Si hay arena debajo de una planta es porque tienes que regarla para que no se marchite!"
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a %s!" % Minnie,
        "¡Llego tarde a mi picnic con %s!" % Donald,
        "Creo que iré a nadar a "+lDonaldsDock+".",
        "Oh, tengo sueño. Me voy a Sueñolandia.",
        ]
    )

ChipChatter = (
        [ # Greetings
        "¡Bienvenido a %s!" % lOutdoorZone,
        "Hola, me llamo" + Chip + ". ¿Cómo te llamas?",
        "No, yo soy" + Chip + ".",
        "¡Me alegro de verte, %!",
        "¡Somos Chip y Dale!",
        ],
        [ # Comments
        "Me gusta el golf.",
        "Tenemos las mejores bellotas de todo Toontown.",
        "Los hoyos de golf con volcanes son todo un reto.",
        ],
        [ # Goodbyes
        "Nos vamos a " + lTheBrrrgh +" a jugar con %s." % Pluto,
        "Vamos a visitar a %s y a arreglarle las cosas." % Donald,
        "Creo que me voy a ir a nadar a " + lDonaldsDock + ".",
        "Oh, tengo sueño. Me voy a Sueñolandia.",
        ]
    )

# Warning Dale's chatter is dependent on on Chip's, they should match up
DaleChatter = (
        [ # Greetings
        "¡Qué alegría verte, %!",
        "hola, me llamo " + Dale + ". ¿Cómo te llamas?",
        "Hola, soy " + Chip + ".",
        "¡Bienvenido a los %s!" % lOutdoorZone,
        "¡Somos Chip y Dale!",
        ],
        [ # Comments
        "Me gustan los picnics.",
        "Las bellotas están muy ricas, pruébalas.",
        "Esos molinos de viento también pueden resultar difíciles.",
        ],
        [ # Goodbyes
        "Jijiji " + Pluto + " es un compañero de juegos divertido.",
        "Sí, vamos a arreglar a %s." % Donald,
        "Nadar, qué agradable.",
        "Necesito descansar, quizás me eche una siesta.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Bienvenido a "+lDaisyGardens+".",
        "Hola, me llamo "+Goofy+". ¿Cómo te llamas?",
        "¡Me alegro de verte %!",
        ],
        [ # Comments
        "¡Qué fácil es perderse en el laberinto del jardín!",
        "Tienes que probar este laberinto.",
        "Hace mucho rato que no veo a "+Daisy+".",
        "Me pregunto dónde estará "+Daisy+".",
        "Eh, ¿viste a "+Donald+"?",
        "Si ves a mi amigo "+Mickey+", salúdale de mi parte.",
        "¡Se me olvidó prepararle el desayuno a "+Mickey+"!",
        "Hay un montón de "+Cogs+" cerca de "+lDonaldsDock+".",
        "Parece que "+Daisy+" plantó flores nuevas en su jardín.",
        "¡En la sección Frescolandia de mi tienda de bromas, las gafas hipnóticas cuestan solo 1 golosina!",
        "¡Las tiendas de bromas de Goofy tienen los mejores chistes, trucos y gracias de todo Toontown!",
        "¡En las tiendas de bromas de Goofy, te garantizamos una buena dosis de risa por cada tarta en la cara o te devolvemos tus golosinas!"
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a %s!" % Mickey,
        "¡Llego tarde a jugar con %s!" % Donald,
        "Creo que me iré a nadar a "+lDonaldsDock+".",
        "Es hora de la siesta. Me voy a Sueñolandia.",
        ]
    )



GoofySpeedwayChatter = (
        [ # Greetings
        "Bienvenido a "+lGoofySpeedway+".",
        "Hola, me llamo "+Goofy+". ¿Cómo te llamas?",
        "¡Me alegro de verte %!",
        ],
        [ # Comments
        "Chico, hoy vi una carrera fantástica.",
        "¡Cuidado con las cáscaras de banana en el circuito!",
        "¿Actualizaste tu kart recientemente?",
        "Acabamos de comprar nuevas llantas en la tienda de karts.",
        "¿Eh, viste a "+Donald+"?",
        "Si ves a mi amigo "+Mickey+", salúdale de mi parte.",
        "¡Olvidé preparar el desayuno de "+Mickey+"!",
        "¡Hay un montón de "+Cogs+" cerca del "+lDonaldsDock+".",
        "¡En la sección Frescolandia de mi tienda de bromas, las gafas hipnóticas cuestan solo 1 golosina!",
        "¡Las tiendas de bromas de Goofy tienen los mejores chistes, trucos y gracias de todo Toontown!",
        "¡En las tiendas de bromas de Goofy, te garantizamos una buena dosis de risa por cada tarta en la cara o te devolvemos tus golosinas!"
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a %s!" % Mickey,
        "¡Llego tarde a jugar con %s!" % Donald,
        "Creo que me iré a nadar a "+lDonaldsDock+".",
        "Es hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Bienvenido a Sueñolandia.",
        "Hola, me llamo %s. ¿Y tú?" % Donald,
        ],
        [ # Comments
        "A veces, este sitio me da escalofríos.",
        "No te olvides de probar el laberinto de los "+lDaisyGardens+".",
        "Caramba, qué buen día estoy teniendo.",
        "Eh, ¿viste a "+Mickey+"?",
        "Si ves a mi buen amigo "+Goofy+", dale recuerdos de mi parte.",
        "Creo que esta tarde me voy a ir de pesca.",
        "Caramba, en "+lDonaldsDock+" hay un montón de "+Cogs+".",
        "Eh, ¿no te llevé en barco en "+lDonaldsDock+"?",
        "No vi a "+Daisy+" en todo el día.",
        "Me dijeron que "+Daisy+" plantó flores nuevas en su jardín.",
        "Cuac.",
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a %s!" % Minnie,
        "¡Vaya! ¡Llego tarde a mi cita con %s!" % Daisy,
        "Creo que voy a mi puerto a nadar un poco.",
        "Creo que voy a darme una vuelta en mi barco en "+lDonaldsDock+".",
        ]
    )

# April Fools Chatter's
AFMickeyChatter = (
        [ # Greetings specific to Mickey
        "¡Feliz Semana de los Dibus Inocentes!",        
        "¡Feliz Semana de los Dibus Inocentes, %!",
        "Hola, me llamo "+Mickey+". ¿y tú?",
        ],
        [ # Comments
        "¿Viste a Daisy?",
        "¡Quiero saludar a Daisy por la Semana de los Dibus Inocentes!",
        "¿Escuchaste hablar al dibuperrito?",
        "¡Qué lindas son estas flores!",
        "¡Daisy debe saberse unos buenos trucos de jardinería!",
        ],
        [ # Goodbyes
        "Hola, estoy buscando a Daisy. ¿La viste?",
        "Es hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

AFMinnieChatter = (
        [ # Greetings
        "Hola, me llamo "+Minnie+". ¿Y tú?",        
        "¡Feliz Semana de los Dibus Inocentes!",        
        "¡Feliz Semana de los Dibus Inocentes, %!",
        ],
        [ # Comments
        "Hola. Tengo que darle la comida a Pluto. ¿Lo viste?",
        "¡Quiero saludar a Pluto por la Semana delos Dibus Inocentes con un obsequio especial!",
        "¿Escuchaste hablar a un dibuperrito?",
        ],
        [ # Goodbyes
        "Hola. Tengo que darle la comida a Pluto. ¿Lo viste?",
        "¡Llego tarde a mi cita con %s!" % Mickey,
        ]
    )

AFDaisyChatter = (
        [ # Greetings
        "Hola, soy "+Daisy+". ¿Y tú?",
        "¡Feliz Semana de los Dibus Inocentes!",        
        "¡Feliz Semana de los Dibus Inocentes, %!",
        ],
        [ # Comments
        "Me pregunto si Mickey se habrá ido a luchar contra los bots.",
        "¿Viste a Mickey?",
        "Quiero saludar a Mickey por la Semana de los Dibus Inocentes!",
        "¿Escuchaste a un dibuperrito hablar o me pareció a mí?",
        ],
        [ # Goodbyes
        "Hola, necesito hablar con Mickey. ¿Lo viste?",
        "Creo que me iré a nadar a "+lDonaldsDock+".",
        "Oh, tengo un poco de sueño. Creo que me iré a Sueñolandia.",
        ]
    )

AFGoofySpeedwayChatter = (
        [ # Greetings
        "¡Feliz Sueño... esto... Semana de los Dibus Inocentes!",
        "¡Feliz Semana de los Dibus Inocentes, %!",
        "Hola, me llamo "+Goofy+". ¿Y tú?",
        ],
        [ # Comments
        "¿Viste a Donald? Creo que volvió a andar sonámbulo.",
        "¡Quiero saludar a Donald por la Semana de los Dibus Inocentes!",
        "¿Escuchaste a un dibuperrito hablar, o es que veo cosas?",
        "Espero que todo vaya bien en el Estadio.",
        ],
        [ # Goodbyes
        "¡Llego tarde a la partida con %s!" % Donald,
        ]
    )

AFDonaldChatter = (
        [ # Greetings
        "¡Feliz Sueño... esto... Semana de los Inocentes dibu!",
        "¡Feliz Semana de los Inocentes dibu, %!",
        "Hola, me llamo %s. ¿Y tú?" % Donald,
        ],
        [ # Comments
        "¿Viste a Goofy?",
        "¡Quiero saludar a Goofy por la Semana de los Dibus Inocentes!",
        "¿Escuchaste a un dibuperrito hablar, o es que estoy soñando?",
        "¿De dónde salió ese kart?",
        ],
        [ # Goodbyes
        "¿De dónde vienen de repente todos esos ruidos de autos?",
        "¡Me voy a Melodilandia a ver a %s!" % Minnie,
        ]
    )    

CLGoofySpeedwayChatter = (
        [ # Greetings
        "Bienvenido a "+lGoofySpeedway+".",
        "Hola, me llamo "+Goofy+". ¿Y tú?",
        "¡Me alegro de verte %!",
        "¡Hola! Perdona que lleve tanto polvo, estuve arreglando el marcador roto.",
        ],
        [ # Comments        
        "Será mejor que arreglemos pronto el marcador, ¡se acerca el fin de semana Grand Prix!",
        "¿Alguien quiere comprar un kart un poco usado? ¡Sólo pasó una vez por el marcador!",
        "Se acerca el fin de semana Grand Prix, conviene practicar.",
        "¡El fin de semana Grand Prix empieza el viernes 22 de mayo y termina el lunes 25 de mayo!",
        "Voy a necesitar una escalera para bajar ese kart.",
        "¡Ese dibu estaba desesperado por llegar al marcador!",
        "Chico, hoy vi una carrera fabulosa.",
        "¡Cuidado con las cáscaras de banana en el circuito!",
        "¿Actualizaste recientemente tu kart?",
        "Acabamos de comprar nuevas llantas en la tienda de karts.",
        "Eh, ¿viste a "+Donald+"?",
        "Si ves a mi amigo "+Mickey+", salúdale de mi parte.",
        "¡Uau! ¡Olvidé prepararle el desayuno a "+Mickey+"!",
        "Hay un montón de "+Cogs+" cerca del "+lDonaldsDock+".",
        "¡En la sección Frescolandia de mi tienda de bromas, las gafas hipnóticas cuestan solo 1 golosina!",
        "¡Las tiendas de bromas de Goofy tienen los mejores chistes, trucos y gracias de todo Toontown!",
        "¡En las tiendas de bromas de Goofy, te garantizamos una buena dosis de risa por cada tarta en la cara o te devolvemos tus golosinas!"
        ],
        [ # Goodbyes
        "Conviene que pinte mi kart para el próximo fin de semana Grand Prix.",
        "¡Será mejor que me ponga a trabajar con este marcador roto!",
        "¡Espero verte el fin de semana Grand Prix! ¡Adiós!",
        "Es hora de la siesta. Me voy a Sueñolandia a soñar con el Grand Prix.",
        ]
    )
        

GPGoofySpeedwayChatter = (
        [ # Greetings
        "Bienvenido al "+lGoofySpeedway+".",        
        "¡Bienvenido al fin de semana Grand Prix!",
        "Hola, me llamo "+Goofy+". ¿Y tú?",
        "¡Me alegro de verte, %!",
        ],
        [ # Comments                
        "¿Estás nervioso por el fin de semana Grand Prix?",
        "Menos mal que arreglaste el marcador.",
        "¡Arreglamos el marcador justo a tiempo para el fin de semana Grand Prix!",
        "¡Nunca encontramos a ese dibu!",
        "Chico, hoy vi una carrera fantástica.",
        "¡Cuidado con las cáscaras de banana del circuito!",
        "¿Actualizaste tu kart recientemente?",
        "Acabamos de comprar nuevas llantas en la tienda de karts.",
        "Eh, ¿viste a "+Donald+"? ¡Dijo que vendría a ver el Grand Prix!",
        "Si ves a mi amigo "+Mickey+", ¡dile que se está perdiendo unas carreras estupendas!",
        "¡Olvidé prepararle el dessayuno a "+Mickey+"!",
        "¡Hay un montón de "+Cogs+" cerca del "+lDonaldsDock+".",
        "¡En la sección Frescolandia de mi tienda de bromas, las gafas hipnóticas cuestan solo 1 golosina!",
        "¡Las tiendas de bromas de Goofy tienen los mejores chistes, trucos y gracias de todo Toontown!",
        "¡En las tiendas de bromas de Goofy, te garantizamos una buena dosis de risa por cada tarta en la cara o te devolvemos tus golosinas!"
        ],
        [ # Goodbyes
        "¡Suerte en el Grand Prix!",
        "¡Voy a ver la siguiente carrera del Grand Prix!",
        "¡Creo que la próxima carrera está a punto de comenzar!",
        "¡Será mejor que vaya a ver si el nuevo marcador funciona bien!",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)

# FriendsListPanel.py
FriendsListPanelNewFriend = "Amigo nuevo"
FriendsListPanelSecrets = "Secretos"
FriendsListPanelOnlineFriends = "AMIGOS\nCONECTADOS"
FriendsListPanelAllFriends = "TODOS LOS\nAMIGOS"
FriendsListPanelIgnoredFriends = "DIBUS\nIGNORADOS"
FriendsListPanelPets = "MASCOTAS\nCERCANAS"
FriendsListPanelPlayers = "TODOS LOS JUGADORES\nAMIGOS"
FriendsListPanelOnlinePlayers = "AMIGOS JUGADORES\nONLINE"

FriendInviterClickToon = "Haz clic en el dibu del que quieres hacerte amigo.\n\n(Tienes %s amigos)"

# Support DISL account friends
FriendInviterToon = "Dibu"
FriendInviterThatToon = "Ese dibu"
FriendInviterPlayer = "Jugador"
FriendInviterThatPlayer = "Ese jugador"
FriendInviterBegin = "¿Qué tipo de amigo quieres tener?"
FriendInviterToonFriendInfo = "Un amigo sólo de Toontown"
FriendInviterPlayerFriendInfo = "Un amigo en la red Disney.com"
FriendInviterToonTooMany = "Tienes demasiados amigos dibu para añadir otro. Para hacerte amigo de %s, tendrás que eliminar a algún amigo dibu. También puedes intentar hacerte amigo jugador."
FriendInviterPlayerTooMany = "Tienes demasiados amigos jugador para añadir otro. Para hacerte amigo de %s, tendrás que eliminar a algún amigo jugador. También puedes intentar hacerte amigo dibu."
FriendInviterToonAlready = "%s ya es tu amigo dibu."
FriendInviterPlayerAlready = "%s ya es tu amigo jugador."
FriendInviterStopBeingToonFriends = "Dejar de ser amigos dibus"
FriendInviterStopBeingPlayerFriends = "Dejar de ser amigos jugadores"
FriendInviterEndFriendshipToon = "¿Seguro que quieres dejar de ser amigo dibu de %s?"
FriendInviterEndFriendshipPlayer = "Seguro que quieres dejar de ser amigo jugador de %s?"
FriendInviterRemainToon = "\n(Seguirás siendo amigo dibu de %s)"
FriendInviterRemainPlayer = "\n(Seguirás siendo amigo jugador de %s)"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Lo siento, no puedes avanzar porque de la descarga de %(phase)s sólo se completó un %(percent)s%%.\n\nVuelve a intentarlo más tarde."

# TeaserPanel.py
TeaserTop = ""
TeaserBottom = ""
TeaserDefault = ",\nyou need to become a Member.\n\nJoin us!"
TeaserOtherHoods = "Visita los 6 extraordinarios barrios."
TeaserTypeAName = "Ponle a tu dibu el nombre que más te guste."
TeaserSixToons = "Crea hasta 6 dibus distintos en una sola cuenta."
TeaserClothing = "Compra ropa exclusiva para darle un toque único a tu dibu."
TeaserCogHQ = "Infíltrate en zonas bot superpeligrosas."
TeaserSecretChat = "Intercambia secretos con amigos\ncharlando con ellos en línea."
TeaserSpecies = "Para elegir este tipo de dibu"
TeaserFishing = "Para pescar en los 6 barrios"
TeaserGolf = "Para jugar al minigolf dibu"
TeaserParties = "Para organizar una fiesta"
TeaserSubscribe = "Suscríbete"
TeaserContinue = "Continuar"
TeaserEmotions = "Compra emociones para dotar a tu dibu de más expresividad."
TeaserKarting = "Para acceder a carreras de kart ilimitadas"
TeaserKartingAccessories = "Para personalizar tu kart"
TeaserGardening = "Para seguir practicando jardinería en tu casa dibu"
TeaserHaveFun = "Have more fun!"
TeaserJoinUs = "Join us!"

#TeaserCardsAndPosters = ""
#TeaserFurniture = ""
TeaserMinigames = TeaserOtherHoods
#TeaserHolidays = ""
TeaserQuests = TeaserOtherHoods
TeaserOtherGags = TeaserOtherHoods
#TeaserRental = ""
#TeaserBigger = ""
TeaserTricks = TeaserOtherHoods

# Launcher.py
LauncherPhaseNames = {
    0   : "Iniciando",
    1   : "Panda",
    2   : "Motor",
    3   : "Crear un dibu",
    3.5 : "Dibututorial",
    4   : "Dibuparque",
    5   : "Calles",
    5.5 : "Propiedades",
    6   : "Barrio I",
    7   : "Edificios " + Cog,
    8   : "Barrio II",
    9   : lToonHQ + " " + Cog,
    10  : Cashbot + " Cuartel general",
    11  : Lawbot + " Cuartel general",
    12  : Bossbot + " Cuartel general",
    13  : "Fiestas",
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)s (%(current)s de %(total)s)"
LauncherStartingMessage = "Iniciando Disney's Toontown Online... "
LauncherDownloadFile = "Descargando actualización para " + LauncherProgress + "..."
LauncherDownloadFileBytes = "Descargando actualización para " + LauncherProgress + ": %(bytes)s"
LauncherDownloadFilePercent = "Descargando actualización para " + LauncherProgress + ": %(percent)s%%"
LauncherDecompressingFile = "Descomprimiendo actualización para " + LauncherProgress + "..."
LauncherDecompressingPercent = "Descomprimiendo actualización para " + LauncherProgress + ": %(percent)s%%"
LauncherExtractingFile = "Extrayendo actualización para " + LauncherProgress + "..."
LauncherExtractingPercent = "Extrayendo actualización para " + LauncherProgress + ": %(percent)s%%"
LauncherPatchingFile = "Aplicando actualización para " + LauncherProgress + "..."
LauncherPatchingPercent = "Aplicando actualización para " + LauncherProgress + ": %(percent)s%%"
LauncherConnectProxyAttempt = "Conectando con Toontown: %s (proxy: %s) intento: %s"
LauncherConnectAttempt = "Conectando con Toontown: %s intento %s"
LauncherDownloadServerFileList = "Actualizando Toontown..."
LauncherCreatingDownloadDb = "Actualizando Toontown..."
LauncherDownloadClientFileList = "Actualizando Toontown..."
LauncherFinishedDownloadDb = "Actualizando Toontown... "
LauncherStartingGame = "Iniciando Toontown..."
LauncherRecoverFiles = "Actualizando Toontown... Recuperando archivos..."
LauncherCheckUpdates = "Comprobando actualizaciones para " + LauncherProgress + "..."
LauncherVerifyPhase = "Actualizando Toontown..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Crea un\ndibu"
AvatarChoicePlayThisToon = "Juega con\neste dibu"
AvatarChoiceSubscribersOnly = "¡Suscríbete\n\n\n\nya mismo!"
AvatarChoiceDelete = "Borrar"
AvatarChoiceDeleteConfirm = "Con esto borrarás a %s para siempre."
AvatarChoiceNameRejected = "Nombre\nrechazado"
AvatarChoiceNameApproved = "¡Nombre\naprobado!"
AvatarChoiceNameReview = "En proceso\nde revisión"
AvatarChoiceNameYourToon = "¡Pon un nombre\na tu dibu!"
AvatarChoiceDeletePasswordText = "¡Cuidado! Con esto borrarás a %s para siempre. Para borrar este dibu, escribe tu contraseña."
AvatarChoiceDeleteConfirmText = "¡Cuidado! Con esto borrarás a %(name)s para siempre.  Para confirmar esto, escribe \"%(confirm)s\" y haz clic en OK."
AvatarChoiceDeleteConfirmUserTypes = "Borrar"
AvatarChoiceDeletePasswordTitle = "¿Quieres borrar este dibu?"
AvatarChoicePassword = "Contraseña"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "La contraseña no coincide. Para borrar este dibu, escribe tu contraseña."
AvatarChoiceDeleteWrongConfirm = "No escribiste la palabra correcta. Para borrar a %(name)s, escribe \"%(confirm)s\" y haz clic en OK. No escribas los apóstrofes. Haz clic en Cancelar si cambiaste de parecer."

# AvatarChooser.py
AvatarChooserPickAToon = "Elige el dibu con el que vas a jugar"
AvatarChooserQuit = lQuit


# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Para ponerte en contacto con el Servicio de atención al cliente, llama al %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\n\nSi necesitas ayuda, ponte en contacto con el Servicio de atención al cliente, en el número %s."
TTAccountIntractibleError = "Se produjo un error."

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                          'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic',]
DateOfBirthEntryDefaultLabel = "Fecha de nacimiento"


# AchievePage.py
AchievePageTitle = "Logros\n(próximamente)"

# PhotoPage.py
PhotoPageTitle = "Foto\n(próximamente)"

# BuildingPage.py
BuildingPageTitle = "Edificios\n(próximamente)"

# InventoryPage.py
InventoryPageTitle = "Bromas"
InventoryPageDeleteTitle = "BORRAR BROMAS"
InventoryPageTrackFull = "Tienes todas las bromas del circuito %s. "
InventoryPagePluralPoints = "Conseguirás una \nbroma nueva de %(trackName)s cuando\nconsigas %(numPoints)s puntos más de %(trackName)s."
InventoryPageSinglePoint = "Conseguirás una \nbroma nueva de %(trackName)s cuando\nconsigas %(numPoints)s punto más de %(trackName)s."
InventoryPageNoAccess = "Todavía no tienes acceso al circuito %s."

# NPCFriendPage.py
NPCFriendPageTitle = "SOS dibus"

# EventsPage.py
PartyDateFormat = "%(mm)s %(dd)d, %(yyyy).4d" # Dec 8, 2008
PartyTimeFormat = "%d:%.2d %s" # 1:45 pm
PartyTimeFormatMeridiemAM = "am"
PartyTimeFormatMeridiemPM = "pm"
PartyCanStart = "¡Llegó la fiesta, haz clic en Comenzar fiesta en tu dibucuaderno!"
PartyHasStartedAcceptedInvite = '¡La fiesta de %s ya comenzó! Haz clic en el anfitrión y después en "Ir a la fiesta" en la página de invitaciones del dibucuaderno.'
PartyHasStartedNotAcceptedInvite = '¡La fiesta de %s ya comenzó! Todavía estás a tiempo de llegar si te teletransportas hasta el anfitrión'

EventsPageName = "Eventos"
EventsPageCalendarTabName = "Calendario"
EventsPageCalendarTabParty = "Fiesta"
EventsPageToontownTimeIs = "LA HORA TOONTOWN ES"
EventsPageConfirmCancel = "Si cancelas, recibirás un reembolso de %d%%. ¿Seguro que quieres cancelar la fiesta?"
EventsPageCancelPartyResultOk = "¡Tu fiesta fue cancelada y recibiste un reembolso de %d golosinas!"
EventsPageCancelPartyResultError = "Lo siento, tu fiesta no fue cancelada."
EventsPageTooLateToStart = "Lo siento, es demasiado tarde para empezar tu fiesta. Puedes cancelarla y organizar otra."
EventsPagePublicPrivateChange = "Modificando configuración de privacidad de tu fiesta..."
EventsPagePublicPrivateNoGo = "Lo siento, en este momento no puedes cambiar la configuración de privacidad de tu fiesta."
EventsPagePublicPrivateAlreadyStarted = "Lo siento, tu fiesta ya comenzó, por lo que no puedes cambiar la configuración de privacidad de la misma."
EventsPageHostTabName = "Anfitrión" # displayed on the physical tab
EventsPageHostTabTitle = "Mi próxima fiesta" # banner text displayed across the top
EventsPageHostTabTitleNoParties = "Ninguna fiesta"
EventsPageHostTabDateTimeLabel = "Vas a celebrar una fiesta en %s a la hora Toontown %s."
EventsPageHostingTabNoParty = "¡Ve al portón de fiestas\ndel dibuparque para organizar\ntu propia fiesta!"
EventsPageHostTabPublicPrivateLabel = "Esta fiesta es:"
EventsPageHostTabToggleToPrivate = "Privada"
EventsPageHostTabToggleToPublic = "Pública"
EventsPageHostingTabGuestListTitle = "Invitados"
EventsPageHostingTabActivityListTitle = "Actividades"
EventsPageHostingTabDecorationsListTitle = "Adornos"
EventsPageHostingTabPartiesListTitle = "Anfitriones"
EventsPageHostTabCancelButton = "Cancelar fiesta"
EventsPageGoButton = "¡Comenzar\nfiesta!"
EventsPageGoBackButton = "¡Fiesta\nya!"
EventsPageInviteGoButton = "¡Ir a la\nfiesta!"
EventsPageUnknownToon = "Dibu desconocido"

EventsPageInvitedTabName = "Invitaciones"
EventsPageInvitedTabTitle = "Invitaciones a fiestas"
EventsPageInvitedTabInvitationListTitle = "Invitaciones"
EventsPageInvitedTabActivityListTitle = "Actividades"
EventsPageInvitedTabTime = "%s %s Hora Toontown"

EventsPageNewsTabName = "Noticias"
EventsPageNewsTabTitle = "Noticias"
EventsPageNewsDownloading= "Retrieving News..."
EventsPageNewsUnavailable = "Chip and Dale played with the printing press. News not available."
EventsPageNewsPaperTitle = "TOONTOWN TIMES"
EventsPageNewsLeftSubtitle = "Still only 1 jellybean"
EventsPageNewsRightSubtitle = "Established toon-thousand nine"

# InvitationSelection.py
SelectedInvitationInformation = "%s va a celebrar una fiesta en %s a las %s hora Toontown."

# PartyPlanner.py
PartyPlannerNextButton = "Continuar"
PartyPlannerPreviousButton = "Volver"
PartyPlannerWelcomeTitle = "Organizador de fiestas Toontown"
PartyPlannerInstructions = "¡Celebrar tu propia fiesta es muy divertido!\n¡Empieza a organizarla con las flechas de abajo!"
PartyPlannerDateTitle = "Elige un día para tu fiesta"
PartyPlannerTimeTitle = "Elige una hora para tu fiesta"
PartyPlannerGuestTitle = "Elige a tus invitados"
PartyPlannerEditorTitle = "Diseña tu fiesta:\nlugar, actividades y adornos"
PartyPlannerConfirmTitle = "Elige las invitaciones que vas a enviar"
PartyPlannerConfirmTitleNoFriends = "Comprueba la organización de tu fiesta"
PartyPlannerTimeToontown = "Toontown"
PartyPlannerTimeTime = "Hora"
PartyPlannerTimeRecap = "Fecha y hora de la fiesta"
PartyPlannerPartyNow = "Lo antes posible"
PartyPlannerTimeToontownTime = "hora Toontown:"
PartyPlannerTimeLocalTime = "Hora local de la fiesta: "
PartyPlannerPublicPrivateLabel = "Esta fiesta será:"
PartyPlannerPublicDescription = "¡Todos los dibus\nson bienvenidos!"
PartyPlannerPrivateDescription = "¡Solo pueden\nvenir dibus\ninvitados!"
PartyPlannerPublic = "Pública"
PartyPlannerPrivate = "Privada"
PartyPlannerCheckAll = "Marcar\ntodos"
PartyPlannerUncheckAll = "Desmarcar\ntodos"
PartyPlannerDateText = "Fecha"
PartyPlannerTimeText = "Hora"
PartyPlannerTTTimeText = "Hora Toontown"
PartyPlannerEditorInstructionsIdle = "Haz clic en la actividad o adorno de fiesta que quieres comprar."
PartyPlannerEditorInstructionsClickedElementActivity = "Haz clic en comprar o arrastra el icono de la actividad a el plano"
PartyPlannerEditorInstructionsClickedElementDecoration = "Haz clic en comprar o arrastra el adorno hasta el plano del lugar de la fiesta"
PartyPlannerEditorInstructionsDraggingActivity = "Arrastra el adorno hasta el plano del lugar de la fiesta"
PartyPlannerEditorInstructionsDraggingDecoration = "Arrastra la actividad hasta el plano del lugar de la fiesta."
PartyPlannerEditorInstructionsPartyGrounds = "Haz clic sobre los objetos y arrástralos para moverlos por el lugar de la fiesta"
PartyPlannerEditorInstructionsTrash = "Arrastra una actividad o un adorno hasta aquí para eliminarlo."
PartyPlannerEditorInstructionsNoRoom = "No hay espacio para colocar esa actividad."
PartyPlannerEditorInstructionsRemoved = "%(removed)s eliminado desde que se añadió %(added)s."
PartyPlannerBeans = "golosinas"
PartyPlannerTotalCost = "Coste total:\n%d golosinas"
PartyPlannerSoldOut = "AGOTADO"
PartyPlannerBuy = "COMPRAR"
PartyPlannerPaidOnly = "SOLO MIEMBROS"
PartyPlannerPartyGrounds = "PLANO DEL LUGAR DE LA FIESTA"
PartyPlannerOkWithGroundsLayout = "¿Terminaste de mover las actividades y los adornos de tu fiesta por el plano del lugar de la fiesta?"
PartyPlannerChooseFutureTime = "Elige una hora futura."
PartyPlannerInviteButton = "Enviar invitaciones"
PartyPlannerInviteButtonNoFriends = "Organizar fiesta"
PartyPlannerBirthdayTheme = "Cumpleaños"
PartyPlannerGenericMaleTheme = "Estrella"
PartyPlannerGenericFemaleTheme = "Flor"
PartyPlannerRacingTheme = "Carrera"
PartyPlannerGuestName = "Nombre del invitado"
PartyPlannerClosePlanner = "Cerrar organizador"
PartyPlannerConfirmationAllOkTitle = "¡Felicidades!"
PartyPlannerConfirmationAllOkText = "La fiesta fue creada y las invitaciones fueron enviadas.\n¡Gracias!"
PartyPlannerConfirmationAllOkTextNoFriends = "¡Tu fiesta fue creada!\n¡Gracias!"
PartyPlannerConfirmationErrorTitle = "Uy."
PartyPlannerConfirmationValidationErrorText = "Lo siento, hay un\nproblema con la fiesta.\nVuelve atrás e inténtalo de nuevo."
PartyPlannerConfirmationDatabaseErrorText = "Lo siento, no se pudo registrar toda la información.\nInténtalo de nuevo más tarde.\nNo te preocupes, no perdiste golosinas."
PartyPlannerConfirmationTooManyText = "Ya eres el anfitrión de una fiesta.\nSi quieres organizar otra fiesta,\ncancela tu fiesta actual."
PartyPlannerInvitationThemeWhatSentence = "¡Estás invitado a mi fiesta %s! ¡%s!"
PartyPlannerInvitationThemeWhatSentenceNoFriends = "¡Voy a celebrar una fiesta %s! ¡%s!"
PartyPlannerInvitationThemeWhatActivitiesBeginning = "Voy a tener "
PartyPlannerInvitationWhoseSentence = "Fiesta %s"
PartyPlannerInvitationTheme = "Tema"
PartyPlannerInvitationWhenSentence = "Será %s,\na las %s Hora Toontown.\n¡Espero que puedas venir!"
PartyPlannerInvitationWhenSentenceNoFriends = "Será %s,\na las %s Hora Toontown.\n¡Dibugnífico!"
PartyPlannerComingSoon = "Muy pronto"
PartyPlannerCantBuy= "No se puede comprar"
PartyPlannerGenericName = "Organizador de fiestas"

# DistributedPartyJukeboxActivity.py
PartyJukeboxOccupied = "Alguien está utilizando el Tocadiscos. Inténtalo más tarde."
PartyJukeboxNowPlaying = "¡La canción que elegiste está sonando en el Tocadiscos!"

# Jukebox Music
MusicEncntrGeneralBg = "Encuentro con bots"
MusicTcSzActivity = "Popurrí Dibutorial"
MusicTcSz = "Paseando"
MusicCreateAToon = "Nuevo dibu en la ciudad"
MusicTtTheme = "Tema de Toontown"
MusicMinigameRace = "Lento y pausado"
MusicMgPairing = "¿Me recuerdas?"
MusicTcNbrhood = "Centro de Toontown"
MusicMgDiving = "Nana del tesoro"
MusicMgCannonGame = "¡Disparen los cañones!"
MusicMgTwodgame = "Dibu al mando"
MusicMgCogthief = "¡Atrapa al bot!"
MusicMgTravel = "Música viajera"
MusicMgTugOWar = "Juego de la cuerda"
MusicMgVine = "El swing de la selva"
MusicMgIcegame = "Situación dudosa"
MusicMgToontag = "Popurrí de minijuegos"
MusicMMatchBg2 = "Minnie Jazz"
MusicMgTarget = "Sobrevolando Toontown"
MusicFfSafezone = "La granja divertida"
MusicDdSz = "Camino del ánade"
MusicMmNbrhood = "Melodilandia de Minnie"
MusicGzPlaygolf = "¡Jugiemos al golf!"
MusicGsSz = "Estadio de Goofy"
MusicOzSz = "Acres de Chip y Dale"
MusicGsRaceCc = "Conducir por la ciudad"
MusicGsRaceSs = "¡Preparados, listos, ya!"
MusicGsRaceRr = "Ruta 66"
MusicGzSz = "La polka del hoyo"
MusicMmSz = "Bailando en las calles"
MusicMmSzActivity = "Aquí llega el trío"
MusicDdNbrhood = "Puerto de Donald"
MusicGsKartshop = "Don Goofytuercas"
MusicDdSzActivity = "Saloma Marina"
MusicEncntrGeneralBgIndoor = "Acumulando emoción"
MusicTtElevator = "¿Subes?"
MusicEncntrToonWinningIndoor = "¡Dibus, únanse!"
MusicEncntrGeneralSuitWinningIndoor = "¡Catástrofe bot!"
MusicTbNbrhood = "Frescolandia"
MusicDlNbrhood = "Sueñolandia de Donald"
MusicDlSzActivity = "Contar ovejas"
MusicDgSz = "Vals de las flores"
MusicDlSz = "Sonámbulo"
MusicTbSzActivity = "Problema de nieve"
MusicTbSz = "Temblores y Amores"
MusicDgNbrhood = "Jardín de Daisy"
MusicEncntrHallOfFame = "El salón de la fama"
MusicEncntrSuitHqNbrhood = "Dólares y centavos"
MusicChqFactBg = "Fábrica bot"
MusicCoghqFinale = "Triunfo de los dibus"
MusicEncntrToonWinning = "¡Canjear!"
MusicEncntrSuitWinning = "¡No te hace justicia!"
MusicEncntrHeadSuitTheme = "El gran jefe"
MusicLbJurybg = "Sesión judicial"
MusicLbCourtyard = "Acta de equilibrio"
MusicBossbotCeoV2 = "Jefazo"
MusicBossbotFactoryV1 = "Vals bot"
MusicBossbotCeoV1 = "Dominando"
MusicPartyOriginalTheme = "Fiesta"
MusicPartyPolkaDance = "Polka de fiesta"
MusicPartySwingDance = "Swing de fiesta"
MusicPartyWaltzDance = "Vals de fiesta"
MusicPartyGenericThemeJazzy = "Jazz de fiesta"
MusicPartyGenericTheme = "Tintineo de fiesta"


# JukeBoxGui
JukeboxAddSong = "Añadir\ncanción"
JukeboxReplaceSong = "Sustituir\ncanción"
JukeboxQueueLabel = "Siguiente canción:"
JukeboxSongsLabel = "Elige una canción:"
JukeboxClose = "Completado"
JukeboxCurrentlyPlaying = "Está sonando"
JukeboxCurrentlyPlayingNothing = "Tocadiscos en pausa"
JukeboxCurrentSongNothing = "¡Añade una canción a la lista!"

PartyOverWarningNoName = "¡La fiesta terminó! ¡Gracias por venir!"
PartyOverWarningWithName = "¡La Fiesta de %s ha terminado! ¡Gracias por participar!"
PartyCountdownClockText = "Tiempo\n\nrestante"
PartyTitleText = "Fiesta %s" # what you see when you enter a party

PartyActivityConjunction = " y"
# Note : This dictionary is used to show the names of the activities in various
#        contexts.  If PartyGlobals.ActivityIds is changed, this list must be
#        updated with new indices.
PartyActivityNameDict = {
    0 : {
        "generic" : "Tocadiscos\n20 canciones",
        "invite" : "un Tocadiscos de 20 canciones",
        "editor" : "Tocadiscos - 20",
        "description" : "¡Escucha música con tu propio Tocadiscos de 20 canciones!"
    },
    1 : {
        "generic" : "Cañones de fiesta",
        "invite" : "Cañones de fiesta",
        "editor" : "Cañones",
        "description" : "¡Lánzate con los cañones directo a la diversión!"
    },
    2 : {
        "generic" : "Trampolín",
        "invite" : "Trampolín",
        "editor" : "Trampolín",
        "description" : "¡Recoge golosinas y salta más alto que nadie!"
    },
    3 : {
        "generic" : "Atrápalo",
        "invite" : "Atrápalo",
        "editor" : "Atrápalo",
        "description" : "¡Atrapa la fruta para ganar golosinas! ¡Tienes que esquivar los yunques!"
    },
    4 : {
        "generic" : "Pista de baile\n10 pasos",
        "invite" : "una pista de baile de 10 pasos",
        "editor" : "Pista de baile - 10",
        "description" : "¡Demuestra tu arte con los 10 pasos al auténtico estilo dibu!"
    },
    5 : {
        "generic" : "Juego de la cuerda",
        "invite" : "Juego de la cuerda",
        "editor" : "Juego de la cuerda",
        "description" : "¡A tirar de la cuerda como locos, 4 contra 4 dibus máximo!"
    },
    6 : {
        "generic" : "Fuegos artificiales",
        "invite" : "Fuegos artificiales",
        "editor" : "Fuegos artificiales",
        "description" : "¡Lanza tu propio espectáculo de fuegos artificiales!"
    },
    7 : {
        "generic" : "El reloj",
        "invite" : "un reloj",
        "editor" : "El reloj",
        "description" : "Cuenta atrás del tiempo que le queda a tu fiesta."
    },
    8 : {
        "generic" : "Tocadiscos\n40 canciones",
        "invite" : "un Tocadiscos de 40 canciones",
        "editor" : "Tocadiscos - 40",
        "description" : "¡Escucha música con tu propio Tocadiscos de 40 canciones!"
    },
    9 : {
        "generic" : "Pista de baile\n20 pasos",
        "invite" : "una pista de baile para 20 pasos",
        "editor" : "Pista de baile - 20",
        "description" : "¡¡Demuestra tu arte con los 20 pasos al auténtico estilo dibu!"
    },    
}

# Note : This dictionary is used to show the names of the decorations in various
#        contexts.  If PartyGlobals.DecorationIds is changed, this list must be
#        updated with new indices.
PartyDecorationNameDict = {
    0 : {
        "editor" : "Yunque y globos",
        "description" : "¡Intenta evitar que la diversión se escape volando!",
    },
    1 : {
        "editor" : "Escenario de fiesta",
        "description" : "Globos, estrellas, ¿qué más se puede pedir?",
    },
    2 : {
        "editor" : "Lazo festivo",
        "description" : "¡Envuelve la diversión!",
    },
    3 : {
        "editor" : "Pastel",
        "description" : "Delicioso.",
    },
    4 : {
        "editor" : "Castillo",
        "description" : "El hogar de todo dibu es su castillo.",
    },
    5 : {
        "editor" : "Montón de regalos",
        "description" : "¡Regalos para todos los dibus!",
    },
    6 : {
        "editor" : "Matasuegras",
        "description" : "¡Este matasuegras es la bomba!",
    },
    7 : {
        "editor" : "Portón de fiesta",
        "description" : "¡Multicolor, una locura!",
    },
    8 : {
        "editor" : "Pitos",
        "description" : "¡Prrriiiiii!",
    },
    9 : {
        "editor" : "Molinillo",
        "description" : "¡Vueltas de color para todos!",
    },
    10 : {
        "editor" : "Globo de bromas",
        "description" : "Globo de bromas y estrellas diseñado por Olivea",
    },
    11 : {
        "editor" : "Póster de golosinas",
        "description" : "Un póster de golosinas diseñado por Cassidy",
    },
    12 : {
        "editor" : "Pastel de bromas",
        "description" : "Un pastel de bromas del revés diseñado por Felicia",
    },
}

ActivityLabel = "Precio – Nombre de la actividad"
PartyDoYouWantToPlan = "¿Quieres organizar una fiesta nueva ahora?"
PartyPlannerOnYourWay = "¡Que te diviertas organizando tu fiesta!"
PartyPlannerMaybeNextTime = "Otra vez será. ¡Que pases un buen día!"
PartyPlannerHostingTooMany = "Sólo puedes ser el anfitrión de una fiesta a la vez."
PartyPlannerOnlyPaid = "Sólo los dibus pagados pueden organizar fiestas."
PartyPlannerNpcComingSoon = "¡Pronto se celebrarán otras fiestas! Inténtalo más tarde."
PartyPlannerNpcMinCost = "Organizar una fiesta cuesta un mínimo de %d golosinas."

# Party Gates
PartyHatPublicPartyChoose = "¿Quieres ir a la 1ª fiesta pública disponible?"
PartyGateTitle = "Fiestas públicas"
PartyGateGoToParty = "¡Ir a la\nfiesta!"
PartyGatePartiesListTitle = "Anfitriones"
PartyGatesPartiesListToons = "Dibus"
PartyGatesPartiesListActivities = "Actividades"
PartyGatesPartiesListMinLeft = "Minutos restantes"
PartyGateLeftSign = "¡Entra!"
PartyGateRightSign = "¡Fiestas públicas!"
PartyGatePartyUnavailable = "Lo siento, esa fiesta ya no está disponible."
PartyGatePartyFull = "Lo siento, esa fiesta está llena."
PartyGateInstructions = 'Haz clic sobre un anfitrión y después sobre "¡Ir a la fiesta!"'

# DistributedPartyActivity.py
PartyActivityWaitingForOtherPlayers = "Esperando a que otros jugadores se unan al juego de la fiesta..."
PartyActivityPleaseWait = "Espera un momento..."
DefaultPartyActivityTitle = "Título del juego de la fiesta"
DefaultPartyActivityInstructions = "Instrucciones del juego de la fiesta"
PartyOnlyHostLeverPull = "El anfitrión es el único que puede iniciar esta actividad."
PartyActivityDefaultJoinDeny = "En este momento no puedes unirte a esta actividad."
PartyActivityDefaultExitDeny = "En este momento no puedes abandonar esta actividad."

# JellybeanRewardGui.py
PartyJellybeanRewardOK = "OK"

# DistributedPartyCatchActivity.py
PartyCatchActivityTitle = "Actividad Atrápalo"
PartyCatchActivityInstructions = "Atrapa todas las piezas de fruta que puedas. ¡Intenta no 'atrapar' %(badThing)s!"
PartyCatchActivityFinishPerfect = "¡PERFECTO!"
PartyCatchActivityFinish = "¡Bien!"
PartyCatchActivityExit        = 'EXIT'
PartyCatchActivityApples      = 'manzanas'
PartyCatchActivityOranges     = 'naranjas'
PartyCatchActivityPears       = 'peras'
PartyCatchActivityCoconuts    = 'cocos'
PartyCatchActivityWatermelons = 'sandías'
PartyCatchActivityPineapples  = 'piñas'
PartyCatchActivityAnvils      = 'yunques'
PartyCatchStarted = "El juego ya empezó. Ve a jugar."
PartyCatchCannotStart = "El juego no pudo iniciarse en este momento."
PartyCatchRewardMessage = "Piezas de fruta atrapadas: %s\n\nGolosinas ganadas: %s"

# DistributedPartyDanceActivity.py
PartyDanceActivityTitle = "Pista de baile"
PartyDanceActivityInstructions = "¡Combina 3 o más dibujos con las TECLAS DE FLECHA para hacer pasos de baile! Hay 10 pasos de baile diferentes. ¿Podrás encontrarlos todos?"
PartyDanceActivity20Title = "Pista de baile"
PartyDanceActivity20Instructions = "¡Combina 3 o más dibujos con las TECHAS DE FLECHA para hacer pasos de baile! Hay 20 pasos de baile diferentes. ¿Podrás encontrarlos todos?"

DanceAnimRight = "Derecha"
DanceAnimReelNeutral = "El dibu pescador"
DanceAnimConked = "El saludo"
DanceAnimHappyDance = "El baile feliz"
DanceAnimConfused = "Mareado"
DanceAnimWalk = "Paseo lunar"
DanceAnimJump = "¡El salto!"
DanceAnimFirehose = "El dibu de fuego"
DanceAnimShrug = "¿Quién sabe?"
DanceAnimSlipForward = "La caída"
DanceAnimSadWalk = "Cansado"
DanceAnimWave = "Hola y adiós"
DanceAnimStruggle = "El salto arrastrado"
DanceAnimRunningJump = "Carrera dibu"
DanceAnimSlipBackward = "Caída hacia atrás"
DanceAnimDown = "Abajo"
DanceAnimUp = "Arriba"
DanceAnimGoodPutt = "El golpe"
DanceAnimVictory = "El baile de la victoria"
DanceAnimPush = "Dibu mimo"
DanceAnimAngry = "Rock n' Roll"
DanceAnimLeft = "Izquierda"

# DistributedPartyCannonActivity.py
PartyCannonActivityTitle = "Cañones"
PartyCannonActivityInstructions = "¡Golpea las nubes para que cambien de color y reboten en el aire! Desde EL AIRE, puedes usar las TECLAS DE FLECHA para DESLIZARTE."
PartyCannonResults = "¡Recogiste %d golosinas!\n\nNúmero de nubes golpeadas: %d"

# DistributedPartyFireworksActivity.py
FireworksActivityInstructions = "Pulsa la tecla \"Repág.\" para ver mejor."
FireworksActivityBeginning = "¡Los fuegos artificiales están a punto de comenzar! ¡Que disfrutes del despectáculo!"
FireworksActivityEnding = "¡Espero que te haya gustado el espectáculo!"
PartyFireworksAlreadyActive = "El espectáculo de fuegos artificiales ya comenzó."
PartyFireworksAlreadyDone = "El espectáculo de fuegos artificiales ya terminó."

# DistributedPartyTrampolineActivity.py
PartyTrampolineJellyBeanTitle = "Trampolín de golosinas"
PartyTrampolineTricksTitle = "Trampolín de acrobacias"
PartyTrampolineActivityInstructions = "Utiliza la tecla Control para saltar.\n\nSalta cuando tu dibu esté en el punto más bajo del trampolín para saltar más alto."
PartyTrampolineActivityOccupied = "Trampolín ocupado."
PartyTrampolineQuitEarlyButton = "Salir"
PartyTrampolineBeanResults = "Conseguiste %d golosinas."
PartyTrampolineBonusBeanResults = "Conseguiste %d golosinas, más %d extra por conseguir la Gran Golosina."
PartyTrampolineTopHeightResults = "La altura máxima fue de %d pies."
PartyTrampolineTimesUp = "Se acabó el tiempo"
PartyTrampolineReady = "Preparado..."
PartyTrampolineGo = "¡Ya!"
PartyTrampolineBestHeight = "Mejor altura hasta ahora:\n%s\n%d pies"
PartyTrampolineNoHeightYet = "¿Hasta dónde\npuedes saltar?"

# DistributedPartyTugOfWarActivity.py
PartyTugOfWarJoinDenied = "Lo siento, en este momento no puedes unirte al juego de la cuerda."
PartyTugOfWarTeamFull = "Lo siento, este equipo está completo."
PartyTugOfWarExitButton = "Salir"
PartyTugOfWarWaitingForMore = "Esperando a más jugadores" # extra spaces on purpose given the blocky font
PartyTugOfWarWaitingToStart = "Esperando para comenzar"
PartyTugOfWarWaitingForOtherPlayers = "Esperando a otros jugadores"
PartyTugOfWarReady = "Preparados..."
PartyTugOfWarGo = "¡YA!"
PartyTugOfWarGameEnd = "¡Bien!"
PartyTugOfWarGameTie = "¡Empate!"
PartyTugOfWarRewardMessage = "Conseguiste %d golosinas. ¡Buen trabajo!"
PartyTugOfWarTitle = "Juego de la cuerda"

# CalendarGuiMonth.py
CalendarShowAll = "Mostrar todos"
CalendarShowOnlyHolidays = "Sólo mostrar festivos"
CalendarShowOnlyParties = "Sólo mostrar fiestas"

# CalendarGuiDay.py
CalendarEndsAt = "Termina en "
CalendarStartedOn = "Comenzó en "
CalendarEndDash = "Final de "
CalendarEndOf = "Final de "
CalendarPartyGetReady = "¡Prepárate!"
CalendarPartyGo = "¡Fiesta!"
CalendarPartyFinished = "Se acabó..."
CalendarPartyCancelled = "Cancelada."
CalendarPartyNeverStarted = "Nunca comenzó."

# NPCFriendPanel.py
NPCFriendPanelRemaining = "Te restan %s"

# MapPage.py
MapPageTitle = "Mapa"
MapPageBackToPlayground = "Volver al dibuparque"
MapPageBackToCogHQ = "Regresar al cuartel general bot"
MapPageGoHome = "Ir a casa"
# hood name, street name
MapPageYouAreHere = "Estás en: %s\n%s"
MapPageYouAreAtHome = "Estás en\ntu propiedad"
MapPageYouAreAtSomeonesHome = "Estás en\nla propiedad %s"
MapPageGoTo = "Ir a\n%s"

# OptionsPage.py
OptionsPageTitle = "Opciones"
OptionsPagePurchase = "¡Suscríbete ya!"
OptionsPageLogout = "Cerrar sesión"
OptionsPageExitToontown = "Salir de Toontown"
OptionsPageMusicOnLabel = "La música está activada."
OptionsPageMusicOffLabel = "La música está desactivada."
OptionsPageSFXOnLabel = "Los efectos de sonido están activados."
OptionsPageSFXOffLabel = "Los efectos de sonido están desactivados."
OptionsPageToonChatSoundsOnLabel = "Los sonidos del chat están activados."
OptionsPageToonChatSoundsOffLabel = "Los sonidos del chat están desactivados."
OptionsPageFriendsEnabledLabel = "Se aceptan solicitudes de nuevos amigos."
OptionsPageFriendsDisabledLabel = "No se aceptan solicitudes de nuevos amigos."
OptionsPageSpeedChatStyleLabel = "Color para SpeedChat"
OptionsPageDisplayWindowed = "en ventana"
OptionsPageSelect = "Escoger"
OptionsPageToggleOn = "Activar"
OptionsPageToggleOff = "Desactivar"
OptionsPageChange = "Cambiar"
OptionsPageDisplaySettings = "Pantalla: %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Pantalla: %(screensize)s"
OptionsPageExitConfirm = "¿Quieres salir de Toontown?"

DisplaySettingsTitle = "Configuración de la pantalla"
DisplaySettingsIntro = "Los siguientes parámetros sirven para configurar el aspecto de Toontown en tu computadora. Lo más probable es que no haga falta modificarlos a no ser que surja algún problema."
DisplaySettingsIntroSimple = "Puedes ajustar la resolución de la pantalla a un valor más alto para mejorar la claridad gráfica y de texto, pero todo depende de tu tarjeta de video: un valor más alto puede hacer que el juego vaya menos fluido o que no funcione."

DisplaySettingsApi = "Interfaz gráfica:"
DisplaySettingsResolution = "Resolución:"
DisplaySettingsWindowed = "En ventana"
DisplaySettingsFullscreen = "Pantalla completa"
DisplaySettingsApply = "Aplicar"
DisplaySettingsCancel = lCancel
DisplaySettingsApplyWarning = "Cuando pulses OK cambiará la configuración gráfica. Si la nueva configuración no se representa correctamente en tu computadora, la pantalla volverá automáticamente a la configuración original transcurridos %s segundos."
DisplaySettingsAccept = "Pulsa OK para conservar la nueva configuración o Cancelar para volver a la anterior. Si no pulsas nada, se volverá a la configuración anterior pasados %s segundos."
DisplaySettingsRevertUser = "Se restableció la configuración anterior de la pantalla. "
DisplaySettingsRevertFailed = "La configuración de pantalla seleccionada no funciona en tu computadora. Se restableció la configuración anterior de la pantalla. "

# TrackPage.py
TrackPageTitle = "Circuito Entrenador de Bromas"
TrackPageShortTitle = "Entrenador de Bromas"
TrackPageSubtitle = "¡Completa las dibutareas para aprender a usar las bromas nuevas!"
TrackPageTraining = "Estás entrenándote para usar las bromas de %s.\nCuando completes las 16 tareas,\npodrás usar las bromas de %s en los combates."
TrackPageClear = "En este momento no te estás entrenando en ningún circuito de bromas."
TrackPageFilmTitle = "%s\nPelícula de\nentrenamiento"
TrackPageDone = "FIN"

# QuestPage.py
QuestPageToonTasks = "Dibutareas"
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
#QuestPageTrackChoice = "%s\n\nPara elegir, ve a:\n  %s\n  %s\n  %s\n  %s"
# questName, npcName, buildingName, streetName, locationName
QuestPageChoose = "Elegir"
QuestPageLocked = "Bloqueado"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = lHQOfficerM
QuestPosterHQBuildingName = lToonHQfull
QuestPosterHQStreetName = "Cualquier calle"
QuestPosterHQLocationName = "Cualquier barrio"

QuestPosterTailor = "Sastre"
QuestPosterTailorBuildingName = "Tienda de ropa"
QuestPosterTailorStreetName = "Cualquier dibuparque"
QuestPosterTailorLocationName = "Cualquier barrio"
QuestPosterPlayground = "En el dibuparque"
QuestPosterAtHome = "En tu casa"
QuestPosterInHome = "En tu casa"
QuestPosterOnPhone = "En tu teléfono"
QuestPosterEstate = "En tu hacienda"
QuestPosterAnywhere = "Cualquier parte"
QuestPosterAuxTo = "hacia:"
QuestPosterAuxFrom = "de:"
QuestPosterAuxFor = "para:"
QuestPosterAuxOr = "o:"
QuestPosterAuxReturnTo = "Vuelve a:"
QuestPosterLocationIn = " en "
QuestPosterLocationOn = " en "
QuestPosterFun = "¡Diviértete!"
QuestPosterFishing = "Ve a pescar"
QuestPosterComplete = "COMPLETADA"

# ShardPage.py
ShardPageTitle = "Distritos"
ShardPageHelpIntro = "Cada distrito es una copia del mundo de Toontown."
ShardPageHelpWhere = "Ahora estás en el distrito \"%s\"."
ShardPageHelpWelcomeValley = "Ahora estás en el distrito \"Valle Bienvenido\", dentro de \"%s\"."
ShardPageHelpMove = "Para desplazarte a otro distrito, haz clic en su nombre."

ShardPagePopulationTotal = "N.º total de habitantes de Toontown:\n%d"
ShardPageScrollTitle = "Nombre            Habitantes"
ShardPageLow = "Tranquilo"
ShardPageMed = "Ideal"
ShardPageHigh = "Lleno"
ShardPageChoiceReject = "Ese distrito está lleno. Prueba con otro."

# SuitPage.py
SuitPageTitle = "Galería de bots"
SuitPageMystery = "???"
SuitPageQuota = "%s de %s"
SuitPageCogRadar = "%s presente"
SuitPageBuildingRadarS = "%s edificio"
SuitPageBuildingRadarP = "%s edificios"

# DisguisePage.py
DisguisePageTitle = "Disfraces de" + Cog
DisguisePageMeritAlert = "¡Listo para un ascenso!"
DisguisePageCogLevel = "Nivel %s"
DisguisePageMeritFull = "Lleno"

# FishPage.py
FishPageTitle = "Pecera"
FishPageTitleTank = "Cubeta para los peces"
FishPageTitleCollection = "Álbum de peces"
FishPageTitleTrophy = "Trofeos de pesca"
FishPageWeightStr = "Peso: "
FishPageWeightLargeS = "%d kg. "
FishPageWeightLargeP = "%d kg. "
FishPageWeightSmallS = "%d gr."
FishPageWeightSmallP = "%d gr."
FishPageWeightConversion = 16
FishPageValueS = "Valor: %d golosina"
FishPageValueP = "Valor: %d golosinas"
FishPageCollectedTotal = "Especies de peces recogidas: %d de %d"
FishPageRodInfo = "Caña de %s\n%d - %d kilos"
FishPageTankTab = "Cubeta"
FishPageCollectionTab = "Álbum"
FishPageTrophyTab = "Trofeos"

FishPickerTotalValue = "Cubeta: %s / %s\nValor: %d golosinas"

UnknownFish = "???"

FishingRod = "Caña de %s"
FishingRodNameDict = {
    0 : "rama",
    1 : "bambú",
    2 : "madera",
    3 : "acero",
    4 : "oro",
    }
FishTrophyNameDict = {
    0 : "Boquerón",
    1 : "Salmonete",
    2 : "Merluza",
    3 : "Pez volador",
    4 : "Tiburón",
    5 : "Pez espada",
    6 : "Ballena asesina",
    }

# GardenPage.py
GardenPageTitle = "Jardinería"
GardenPageTitleBasket = "Cesta de flores"
GardenPageTitleCollection = "Álbum de flores"
GardenPageTitleTrophy = "Trofeos de jardinería"
GardenPageTitleSpecials = "Especiales de jardinería"
GardenPageBasketTab = "Cesta"
GardenPageCollectionTab = "Álbum"
GardenPageTrophyTab = "Trofeos"
GardenPageSpecialsTab = "Especiales"
GardenPageCollectedTotal = "Variedades de flores recogidas: %d of %d"
GardenPageValueS = "Valor: %d golosinas"
GardenPageValueP = "Valor: %d golosinas"
FlowerPickerTotalValue = "Cesta: %s / %s\nValor: %d golosinas"
GardenPageShovelInfo = "%s Pala: %d / %d\n"
GardenPageWateringCanInfo = "%s Regadera: %d / %d"

# KartPage.py
KartPageTitle = "Karts" 
KartPageTitleCustomize = "Personalizador de kart"
KartPageTitleRecords = "Récords personales"
KartPageTitleTrophy = "Trofeos de carreras" 
KartPageCustomizeTab = "Personalizar"
KartPageRecordsTab = "Récords"
KartPageTrophyTab = "Trofeo"
KartPageTrophyDetail = "Trofeo %s : %s"
KartPageTickets = "Boletos : "
KartPageConfirmDelete = "¿Borrar accesorio?" 

#plural
KartShtikerDelete = "Borrar"
KartShtikerSelect = "Selecciona una categoría"
KartShtikerNoAccessories = "No tienes accesorios"
KartShtikerBodyColors = "Colores de karts"
KartShtikerAccColors = "Colores de accesorios"
KartShtikerEngineBlocks = "Colores del capó"
KartShtikerSpoilers = "Colores de los portaequipaje"
KartShtikerFrontWheelWells = "Accesorios rueda delantera"
KartShtikerBackWheelWells = "Accesorios rueda trasera"
KartShtikerRims = "Accesorios llantas"
KartShtikerDecals = "Accesorios adhesivos"
#singluar
KartShtikerBodyColor = "Color del kart"
KartShtikerAccColor = "Color del accesorio"
KartShtikerEngineBlock = "Capó"
KartShtikerSpoiler = "Portaequipaje"
KartShtikerFrontWheelWell = "Rueda delantera"
KartShtikerBackWheelWell = "Rueda trasera"
KartShtikerRim = "Llanta"
KartShtikerDecal = "Adhesivo"

KartShtikerDefault = "%s predeterminado"
KartShtikerNo = "No hay accesorios de %s"

# QuestChoiceGui.py
QuestChoiceGuiCancel = lCancel

# TrackChoiceGui.py
TrackChoiceGuiChoose = "Elige"
TrackChoiceGuiCancel = lCancel
TrackChoiceGuiHEAL = "El curadibu te permite sanar a otros dibus durante el combate."
TrackChoiceGuiTRAP = "Las trampas son potentes bromas que se deben usar con cebos."
TrackChoiceGuiLURE = "Los cebos permiten aturdir a los bots y atraerlos a las trampas."
TrackChoiceGuiSOUND = "Las bromas de sonido afectan a todos los bots, pero no son muy potentes."
TrackChoiceGuiDROP = "Las bromas de caída causan un montón de daños, pero no son muy precisas."

# EmotePage.py
EmotePageTitle = "Expresiones / Emociones"
EmotePageDance = "Creaste la siguiente secuencia de baile:"
EmoteJump = "Saltar"
EmoteDance = "Bailar"
EmoteHappy = "Feliz"
EmoteSad = "Triste"
EmoteAnnoyed = "Fastidiado"
EmoteSleep = "Soñoliento"

# TIP Page
TIPPageTitle = "TIP"

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nNivel %(level)s"

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "¡No puedes irte del dibuparque hasta que tu risómetro esté sonriendo!"

# InventoryNew.py
InventoryTotalGags = "Bromas totales\n%d / %d"
InventroyPinkSlips = "%s Cartas de despido"
InventroyPinkSlip = "1 carta de despido"
InventoryDelete = "BORRAR"
InventoryDone = "LISTO"
InventoryDeleteHelp = "Haz clic en una broma para BORRARLA."
InventorySkillCredit = "Habilidad: %s"
InventorySkillCreditNone = "Habilidad: Ninguna"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Precisión: %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryUberTrackExp = "¡Quedan %(nextExp)s!"
InventoryGuestExp = "Límite de invitados"
GuestLostExp = "Por encima del límite de invitados"
InventoryAffectsOneCog = "Afecta a: un " + Cog
InventoryAffectsOneToon = "Afecta a: un dibu"
InventoryAffectsAllToons = "Afecta a: todos los dibus"
InventoryAffectsAllCogs = "Afecta a: todos los " + Cogs
InventoryHealString = "Curadibu"
InventoryDamageString = "Daños"
InventoryBattleMenu = "MENÚ DE COMBATE"
InventoryRun = "CORRER"
InventorySOS = "S.O.S."
InventoryPass = "PASE"
InventoryFire = "DISPARO"
InventoryClickToAttack = "Haz clic en \nuna broma \npara atacar"
InventoryDamageBonus = "(+%d)"

# NPCForceAcknowledge.py
NPCForceAcknowledgeMessage = "Antes de marcharte debes subirte al tranvía.\n\n\n\n\n\nEl tranvía esta al lado de la tienda de bromas de Goofy."
NPCForceAcknowledgeMessage2 = "¡Felicitaciones por completar tu tarea del tranvía!\nVe al cuartel general para recibir tu recompensa.\n\n\n\n\n\n\nEl cuartel general esta cerca del centro del dibuparque."
NPCForceAcknowledgeMessage3 = "Recuerda que tienes que subirte al tranvía.\n\n\n\n\n\nEl tranvía esta al lado de la tienda de bromas de Goofy."
NPCForceAcknowledgeMessage4 = "!Felicitaciones! ¡Completaste la primera dibutarea!\n\n\n\n\n\nVe al cuartel general para recibir tu recompensa."
NPCForceAcknowledgeMessage5 = "No olvides tu dibutarea!\n\n\n\n\n\n\n\n\n\n\nAl otro lado de túneles como este, encontrarás bots que podrás derrotar."
NPCForceAcknowledgeMessage6 = "Buen trabajo, derrotaste a esos bots!\n\n\n\n\n\n\n\n\nRegresa al cuartel general lo antes posible."
NPCForceAcknowledgeMessage7 = "¡No olvides hacerte amigo de alguien!\n\n\n\n\n\n\nHaz clic en otro jugador y utiliza el botón Amigo Nuevo."
NPCForceAcknowledgeMessage8 = "¡Fantástico! ¡Tienes un amigo nuevo!\n\n\n\n\n\n\n\n\nAhora debes regresar al cuartel general."
NPCForceAcknowledgeMessage9 = "¡Usaste bien el teléfono!\n\n\n\n\n\n\n\n\nRegresa al cuartel general para pedir tu recompensa."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "¡Recibiste 1 punto de lanzamiento! ¡Cuando hayas recibido 10, tendrás una broma nueva!"
MovieTutorialReward2 = "¡Recibiste 1 punto de chorro! ¡Cuando hayas recibido 10, tendrás una broma nueva!"
MovieTutorialReward3 = "¡Buen trabajo! ¡Completaste tu primera dibutarea!"
MovieTutorialReward4 = "¡Ve al cuartel general para recibir tu premio!"
MovieTutorialReward5 = "¡Que te diviertas!"

# ToontownBattleGlobals.py
BattleGlobalTracks = ['curadibu', 'trampa', 'cebo', 'sonido', 'lanzamiento', 'chorro', 'caída']
BattleGlobalNPCTracks = ['reaprovisionamiento', 'dibus aciertan', 'bots fallan']
BattleGlobalAvPropStrings = (
    ('Pluma', 'Megáfono', 'Pintalabios', 'Caña de bambú', 'Polvo de hadas', 'Bolas de malabarista', 'Salto vertical'),
    ('Cáscara de banana', 'Rastrillo', 'Canicas', 'Arena movediza', 'Trampilla', 'TNT', 'Ferrocarril'),
    ('Billete de 1 dólar', 'Imán pequeño', 'Billete de 5 dólares', 'Imán grande', 'Billete de 10 dólares', 'Gafas hipnóticas', 'Presentación'),
    ('Bocina de bicicleta', 'Silbato', 'Corneta', 'Sirena', 'Trompa de elefante', 'Sirena de niebla', 'Cantante de ópera'),
    ('Magdalena', 'Trozo de tarta de frutas', 'Trozo de tarta de nata', 'Tarta de frutas entera', 'Tarta de nata entera', 'Tarta de cumpleaños', 'Tarta nupcial'),
    ('Flor chorreante', 'Vaso de agua', 'Pistola de agua', 'Botella de soda', 'Manguera', 'Nube tormentosa', 'Géiser'),
    ('Maceta', 'Saco de arena', 'Yunque', 'Pesa grande', 'Caja fuerte', 'Piano de cola', 'Dibutanic')
    )
BattleGlobalAvPropStringsSingular = (
    ('una pluma', 'un megáfono', 'un pintalabios', 'una caña de bambú', 'un polvo de hadas', 'unas bolas de malabarista', 'un salto vertical'),
    ('una cáscara de banana', 'un rastrillo', 'unas canicas', 'una arena movediza', 'una trampilla', 'un TNT', 'un ferrocarril'),
    ('un billete de 1 dólar', 'un imán pequeño', 'un billete de 5 dólares', 'un imán grande', 'un billete de 10 dólares', 'unas gafas hipnóticas', 'una presentación'),
    ('una bocina de bicicleta', 'un silbato', 'una corneta', 'una sirena', 'una trompa de elefante', 'una sirena de niebla', 'un cantante de ópera'),
    ('una magdalena', 'un trozo de tarta de frutas', 'un trozo de tarta de nata', 'una tarta de frutas entera', 'una tarta de nata entera', 'una tarta de cumpleaños', 'una tarta nupcial'),
    ('una flor chorreante', 'un vaso de agua', 'una pistola de agua', 'una botella de soda', 'una manguera', 'una nube tormentosa', 'un géiser'),
    ('una maceta', 'un saco de arena', 'un yunque', 'una pesa grande', 'una caja fuerte', 'un piano de cola', 'el Dibutanic')
    )
BattleGlobalAvPropStringsPlural = (
    ('Plumas', 'Megáfonos', 'Pintalabios', 'Cañas de bambú', 'Polvos de hadas', 'Bolas de malabarista', 'Saltos verticales'),
    ('Cáscaras de banana', 'Rastrillos', 'Canicas', 'Arenas movedizas', 'Trampillas','TNT', 'Ferrocarriles'),
    ('Billetes de 1 dólar', 'Imanes pequeños', 'Billetes de 5 dólares', 'Imanes grandes','Billetes de 10 dólares', 'Gafas hipnóticas', 'Presentaciones'),
    ('Bocinas de bicicleta', 'Silbatos', 'Cornetas', 'Sirenas', 'Trompas de elefante', 'Sirenas de niebla', 'Cantantes de ópera'),
    ('Magdalenas', 'Trozos de tarta de frutas', 'Trozos de tarta de nata','Tartas de frutas enteras', 'Tartas de nata enteras', 'Tartas de cumpleaños', 'Tartas nupciales'),
    ('Flores chorreantes', 'Vasos de agua', 'Pistolas de agua','Botellas de soda', 'Mangueras', 'Nubes tormentosas', 'Géisers'),
    ('Macetas', 'Sacos de arena', 'Yunques', 'Pesas grandes', 'Cajas fuertes','Pianos de cola', 'Trasatlánticos')
    )
BattleGlobalAvTrackAccStrings = ("Media", "Perfecta", "Baja", "Alta", "Media", "Alta", "Baja")
BattleGlobalLureAccLow = "Baja"
BattleGlobalLureAccMedium = "Media"

AttackMissed = "Fallaste"

NPCCallButtonLabel = 'LLAMAR'

# ToontownLoader.py
LoaderLabel = "Cargando..."

# PlayGame.py
HeadingToHood = "Entrando %(to)s %(hood)s..." # to phrase, hood name
HeadingToYourEstate = "Entrando a tu propiedad..."
HeadingToEstate = "Entrando a la propiedad de %s..."  # avatar name
HeadingToFriend = "Entrando a la propiedad del amigo %s..."  # avatar name

# Hood.py
HeadingToPlayground = "Entrando al dibuparque..."
HeadingToStreet = "Entrando %(to)s %(street)s..." # to phrase, street name

# TownBattle.py
TownBattleRun = "¿Quieres volver corriendo al dibuparque?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "¿QUÉ DIBU?"
TownBattleChooseAvatarCogTitle = "¿QUÉ " + string.upper(Cog) + "?"
TownBattleChooseAvatarBack = "ATRÁS"

#firecogpanel
FireCogTitle = "CARTAS DE DESPIDO RESTANTES:%s\n¿DISPARAR A QUÉ BOT?"
FireCogLowTitle = "CARTAS DE DESPIDO RESTANTES:%s\n¡NO HAY SUFICIENTES CARTAS!"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "¡No tienes amigos a los que llamar!"
TownBattleSOSWhichFriend = "¿A qué amigo quieres llamar?"
TownBattleSOSNPCFriends = "Dibus rescatados"
TownBattleSOSBack = "ATRÁS"

# TownBattleToonPanel.py
TownBattleToonSOS = "S.O.S."
TownBattleToonFire = "Disparo"
TownBattleUndecided = "¿?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "Esperando a\notros jugadores..."
TownSoloBattleWaitTitle = "Espera..."
TownBattleWaitBack = "ATRÁS"

# TownBattleSOSPetSearchPanel.py
TownBattleSOSPetSearchTitle = "Buscando al Dibuperrito\n%s..." 

# TownBattleSOSPetInfoPanel.py
TownBattleSOSPetInfoTitle = "%s es %s" 
TownBattleSOSPetInfoOK = lOK

# Trolley.py
TrolleyHFAMessage = "No puedes subirte al tranvía hasta que el risómetro esté sonriendo."
TrolleyTFAMessage = "No puedes subirte al tranvía hasta que lo diga Mickey."
TrolleyHopOff = "Bajarse"

# DistributedFishingSpot.py
FishingExit = "Listo"
FishingCast = "Lanzar"
FishingAutoReel = "Carrete automático"
FishingItemFound = "Pescaste:"
FishingCrankTooSlow = "Muy\nlento"
FishingCrankTooFast = "Muy\nrápido"
FishingFailure = "¡No pescaste nada!"
FishingFailureTooSoon = "No empieces a enrollar el carrete hasta que veas que pican. ¡Espera a que la boya se mueva hacia arriba y abajo rápidamente!"
FishingFailureTooLate = "¡Es importante que enrolles la línea mientras el pez está mordiendo el anzuelo!"
FishingFailureAutoReel = "El carrete automático no funcionó esta vez. Enrolla a mano el carrete a la velocidad correcta para poder pescar algo."
FishingFailureTooSlow = "Enrollaste el carrete demasiado despacio. Algunos peces son más rápidos que otros. ¡Intenta mantener centrada la barra de velocidad!"
FishingFailureTooFast = "Enrollaste el carrete demasiado deprisa. Algunos peces son más lentos que otros. ¡Intenta mantener centrada la barra de velocidad!"
FishingOverTankLimit = "La cubeta de peces está lleno. Vende unos cuantos peces y vuelve."
FishingBroke = "¡No tienes nada que poner en el anzuelo! Súbete al tranvía para conseguir más golosinas."
FishingHowToFirstTime = "Pulsa el botón Lanzar y arrastra hacia abajo. Cuanto más lejos arrastres, más fuerte será el lanzamiento. Ajusta el ángulo para acertar en los peces.\n\n¡Pruébalo ya!"
FishingHowToFailed = "Pulsa el botón para Lanzar y arrastra hacia abajo. Cuanto más lejos arrastres, más fuerte será el lanzamiento. Ajusta el ángulo para acertar en los peces.\n\n¡Prueba de nuevo!"
FishingBootItem = "Una bota vieja"
FishingJellybeanItem = "%s golosinas"
FishingNewEntry = "¡Una nueva\nespecie!"
FishingNewRecord = "¡Nuevo\nrécord!"

# FishPoker
FishPokerCashIn = "Canjear\n%s\n%s"
FishPokerLock = "Fijar"
FishPokerUnlock = "Liberar"
FishPoker5OfKind = "Escalera de color"
FishPoker4OfKind = "Póquer"
FishPokerFullHouse = "Full"
FishPoker3OfKind = "Trío"
FishPoker2Pair = "Doble pareja"
FishPokerPair = "Pareja"

# DistributedTutorial.py
TutorialGreeting1 = "¡Hola, %s!"
TutorialGreeting2 = "¡Hola, %s!\n¡Ven aquí!"
TutorialGreeting3 = "¡Hola, %s!\n¡Ven aquí!\n¡Usa las flechas del teclado!"
TutorialMickeyWelcome = "¡Bienvenido a Toontown!"
TutorialFlippyIntro = "Te voy a presentar a mi amigo %s." % Flippy
TutorialFlippyHi = "¡Hola, %s!"
TutorialQT1 = "Puedes usar esto para hablar."
TutorialQT2 = "Puedes usar esto para hablar.\nHaz clic y elige \"Hola\"."
TutorialChat1 = "Puedes hablar con cualquiera de estos botones."
TutorialChat2 = "El botón azul te permite charlar en línea por medio del teclado."
TutorialChat3 = "¡Ten cuidado! Muchos de los jugadores no entenderán lo que dices si usas el teclado."
TutorialChat4 = "El botón verde abre: %s."
TutorialChat5 = "Todos entienden lo que dices cuando usas: %s."
TutorialChat6 = "Prueba decir \"Hola\"."
TutorialBodyClick1 = "¡Muy bien!"
TutorialBodyClick2 = "¡Encantado de conocerte! ¿Quieres ser mi amigo?"
TutorialBodyClick3 = "Para ser amigo de %s, haz clic en él..." % Flippy
TutorialHandleBodyClickSuccess = "¡Buen trabajo!"
TutorialHandleBodyClickFail = "Todavía no. Prueba a hacer clic en %s..." % Flippy
TutorialFriendsButton = "Ahora pulsa el botón \"Amigos\", situado debajo de la imagen de %s, en la esquina derecha." % Flippy
TutorialHandleFriendsButton = "Después, pulsa el botón \"Sí\"."
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = "¿Quieres ser amigo de %s?" % Flippy
TutorialFriendsPanelMickeyChat = "%s aceptó ser tu amigo. Pulsa \"Ok\" para terminar." % Flippy
TutorialFriendsPanelYes = "¡%s dijo que sí!" % Flippy
TutorialFriendsPanelNo = "¡No es que seas muy amable!"
TutorialFriendsPanelCongrats = "¡Felicitaciones! Acabas de hacer tu primer amigo."
TutorialFlippyChat1 = "Ven a verme cuando estés preparado para tu primera dibutarea."
TutorialFlippyChat2 = "Estaré en el Ayuntamiento."
TutorialAllFriendsButton = "Para ver a todos tus amigos, haz clic en el botón Amigos. Pruébalo..."
TutorialEmptyFriendsList = "Ahora mismo la lista está vacía porque %s no es un jugador de verdad." % Flippy
TutorialCloseFriendsList = "Pulsa el botón\nCerrar para que la\nlista se cierre."
TutorialShtickerButton = "El botón de la esquina inferior derecha sirve para abrir el dibucuaderno. Prúebalo..."
TutorialBook1 = "El dibucuaderno contiene un montón de información útil, como este mapa de Toontown."
TutorialBook2 = "También puedes ver cómo van tus dibutareas."
TutorialBook3 = "Cuando termines, vuelve a pulsar el botón del libro para que se cierre."
TutorialLaffMeter1 = "También vas a necesitar esto..."
TutorialLaffMeter2 = "También vas a necesitar esto...\nEs tu risómetro."
TutorialLaffMeter3 = "Cuando los bots te ataquen, irá disminuyendo."
TutorialLaffMeter4 = "Cuando estés en dibuparques como este, subirá de nuevo."
TutorialLaffMeter5 = "Cuando completes dibutareas obtendrás recompensas, como por ejemplo un aumento del límite del risómetro."
TutorialLaffMeter6 = "¡Ten cuidado! Si los bots te vencen, perderás todas las bromas."
TutorialLaffMeter7 = "Para conseguir más bromas, juega a los juegos del tranvía."
TutorialTrolley1 = "¡Sígueme hasta el tranvía!"
TutorialTrolley2 = "¡Súbete!"
TutorialBye1 = "¡Juega a unos cuantos juegos!"
TutorialBye2 = "¡Juega a unos cuantos juegos!\n¡Compra unas cuantas bromas!"
TutorialBye3 = "Cuando termines, ve a ver a %s" % Flippy

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "¡Vas en dirección contraria! ¡Ve a buscar a %s!" % Mickey

PetTutorialTitle1 = "El panel Dibuperrito"
PetTutorialTitle2 = "Dibuperrito de SpeedChat"
PetTutorialTitle3 = "Catálogo tolón-tolón"
PetTutorialNext = "Página siguiente"
PetTutorialPrev = "Página anterior"
PetTutorialDone = "Completado"
PetTutorialPage1 = "Haz clic en un Dibuperrito para abrir el panel Dibuperrito. Desde aquí, podrás alimentar, rascar y llamar al Dibuperrito."
PetTutorialPage2 = "Utiliza la nueva zona 'Mascotas' en el menú SpeedChat para hacer que un Doodle haga una acrobacia. Si la hace, ¡dale un premio y aprenderá a hacerlo mejor!"
PetTutorialPage3 = "Compra nuevas acrobacias para el Dibuperrito desde el catálogo tolón-tolón de Clarabel. ¡Las mejores acrobacias dan mejores curadibus!"
def getPetGuiAlign():
	from pandac.PandaModules import TextNode
	return TextNode.ACenter

GardenTutorialTitle1 = "Jardinería"
GardenTutorialTitle2 = "Flores"
GardenTutorialTitle3 = "Árboles"
GardenTutorialTitle4 = "Cómo hacerlo"
GardenTutorialTitle5 = "Estatuas"
GardenTutorialNext = "Página siguiente"
GardenTutorialPrev = "Página anterior"
GardenTutorialDone = "Completado"
GardenTutorialPage1 = "¡Mejora tu hacienda con un jardín! ¡Puedes plantar flores, árboles, cultivar bromas súper poderosas y decorarlo con estatuas!"
GardenTutorialPage2 = "Las flores son complicadas y necesitan exclusivas recetas de golosina. Cuando crezcan, colócalas en la carretilla para venderlas y conseguir más subidas del risómetro."
GardenTutorialPage3 = "Utiliza una broma de tu inventario para plantar un árbol. Pasados unos días, ¡la broma provocará más daños! Recuerda que tiene que estar fuerte y sana para que no desaparezca el aumento de daños."
GardenTutorialPage4 = "Camina hasta estos puntos para plantar, regar, cavar o recolectar tu jardín."
GardenTutorialPage5 = "Las estatuas se pueden comprar en el catálogo tolón-tolón de Clarabel. Mejora tu habilidad para desbloquear las estatuas más extravagantes."

# Playground.py
PlaygroundDeathAckMessage = "¡"+TheCogs+" se llevaron todas tus bromas!\n\nEstás triste. No puedes irte del dibuparque hasta que estés feliz."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "El "+Foreman+" fue derrotado antes de que llegaras. No recuperaste ninguna pieza bot."

# MintInterior
ForcedLeaveMintAckMsg = "El supervisor de planta de la fabrica de monedas fue derrotado antes de que llegaras hasta él. No recuperaste ningún botdólar."

# DistributedFactory.py
HeadingToFactoryTitle = "De camino a %s..."
ForemanConfrontedMsg = "¡%s está luchando contra el "+Foreman+"!"

# DistributedMint.py
MintBossConfrontedMsg = "¡%s está luchando contra el supervisor!"

# DistributedStage.py
StageBossConfrontedMsg = "¡%s está luchando contra el empleado!"
stageToonEnterElevator = "%s \nentró en el ascensor"
ForcedLeaveStageAckMsg = "El empleado legal fue derrotado antes de que llegaras a él. No recuperaste ninguna Notificación del tribunal."


# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "Esperando a que se unan otros jugadores..."
MinigamePleaseWait = "Espera..."
DefaultMinigameTitle = "Título del minijuego"
DefaultMinigameInstructions = "Instrucciones del minijuego"
HeadingToMinigameTitle = "Entrando a: %s..." # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "Indicador\nde fuerza"
MinigamePowerMeterTooSlow = "Muy\nlento"
MinigamePowerMeterTooFast = "Muy\nrápido"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "Plantilla del minijuego"
MinigameTemplateInstructions = "Esto es una plantilla de minijuegos. Úsala para crear nuevos minijuegos."

# DistributedCannonGame.py
CannonGameTitle = "El Cañón"
CannonGameInstructions = "Dispara a tu dibu para meterlo en el depósito de agua tan rápido como puedas. Usa el mouse o las teclas de flecha para apuntar el cañón. ¡Date prisa y consigue una gran recompensa para todos!"
CannonGameReward = "RECOMPENSA"

# DistributedTwoDGame.py
TwoDGameTitle = "Dibuevasión"
TwoDGameInstructions = "Escapa de la guarida " + Cog + " en cuanto puedas. Usa las teclas de flecha para correr/saltar y Ctrl para mojar a un " + Cog + ". Recoge tesoros " + Cog + " para conseguir más puntos."
TwoDGameElevatorExit = "SALIR"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Juego de la Cuerda"
TugOfWarInstructions = "Pulsa alternativamente las teclas de flecha izquierda y derecha con la suficiente rapidez para alinear la barra verde con la línea roja. ¡No pulses demasiado deprisa ni demasiado despacio o acabarás en el agua!"
TugOfWarGameGo = "¡YA!"
TugOfWarGameReady = "Listo..."
TugOfWarGameEnd = "¡Muy bien!"
TugOfWarGameTie = "¡Empate!"
TugOfWarPowerMeter = "Indicador de fuerza"

# DistributedPatternGame.py
PatternGameTitle = "Imita a %s" % Minnie
PatternGameInstructions = Minnie + " te enseñará una secuencia de baile " + \
                          "Intenta repetir con las teclas de flecha el baile de "+Minnie+" justo igual que lo hace ella."
PatternGameWatch   = "Observa estos pasos de baile..."
PatternGameGo      = "¡YA!"
PatternGameRight   = "¡Bien, %s!"
PatternGameWrong   = "¡Vaya!"
PatternGamePerfect = "¡Perfecto, %s!"
PatternGameBye     = "¡Gracias por jugar!"
PatternGameWaitingOtherPlayers = "Esperando a otros jugadores..."
PatternGamePleaseWait = "Espera..."
PatternGameFaster = "¡Fuiste\nmuy rápido!"
PatternGameFastest = "¡Fuiste\nel más rápido!"
PatternGameYouCanDoIt = "¡Vamos!\n¡Puedes hacerlo!"
PatternGameOtherFaster = "\nfue más rápido."
PatternGameOtherFastest = "\nfue el más rápido."
PatternGameGreatJob = "¡Buen trabajo!"
PatternGameRound = "¡Asalto nº %s!" # Round 1! Round 2! ..
PatternGameImprov = "¡Lo hiciste muy bien! ¡Ahora, supérate!"

# DistributedRaceGame.py
RaceGameTitle = "Carrera"
RaceGameInstructions = "Haz clic en un número. ¡Piénsalo bien! Sólo avanzarás si nadie más escogió ese mismo número."
RaceGameWaitingChoices = "Esperando a que elijan otros jugadores..."
RaceGameCardText = "%(name)s saca: %(reward)s"
RaceGameCardTextBeans = "%(name)s recibe: %(reward)s"
RaceGameCardTextHi1 = "¡%(name)s es un dibu fabuloso!"  # this category might eventually have secret game hints, etc

# RaceGameGlobals.py
RaceGameForwardOneSpace    = " adelante 1 espacio"
RaceGameForwardTwoSpaces   = " adelante 2 espacios"
RaceGameForwardThreeSpaces = " adelante 3 espacios"
RaceGameBackOneSpace    = " atrás 1 espacio"
RaceGameBackTwoSpaces   = " atrás 2 espacios"
RaceGameBackThreeSpaces = " atrás 3 espacios"
RaceGameOthersForwardThree = " todos los demás, adelante \n3 espacios"
RaceGameOthersBackThree = " todos los demás, atrás \n3 espacios"
RaceGameInstantWinner = "¡Ganador instantáneo!"
RaceGameJellybeans2 = "2 golosinas"
RaceGameJellybeans4 = "4 golosinas"
RaceGameJellybeans10 = "¡10 golosinas!"

# DistributedRingGame.py
RingGameTitle = "Los anillos"
# color
RingGameInstructionsSinglePlayer = "Intenta atravesar nadando todos los anillos que puedas de color %s. Usa las flechas del teclado para nadar."
# color
RingGameInstructionsMultiPlayer = "Intenta atravesar nadando los anillos de color %s. Los demás jugadores intentarán atravesar el resto de los anillos. Usa las flechas del teclado para nadar."
RingGameMissed = "FALLÓ"
RingGameGroupPerfect = "GRUPO\n¡¡PERFECTO!!"
RingGamePerfect = "¡PERFECTO!"
RingGameGroupBonus = "BONIFICACIÓN POR GRUPO"

# RingGameGlobals.py
ColorRed = "rojo"
ColorGreen = "verde"
ColorOrange = "naranja"
ColorPurple = "morado"
ColorWhite = "blanco"
ColorBlack = "negro"
ColorYellow = "amarillo"

# DistributedDivingGame.py
DivingGameTitle = "Inmersión del tesoro"
# color
DivingInstructionsSinglePlayer = "Irán apareciendo tesoros en el fondo del lago. Utiliza las techas de flechas para nadar. ¡Esquiva los peces y sube los tesoros al barco!"
# color
DivingInstructionsMultiPlayer = "Irán apareciendo tesoros en el fondo del lago. Utiliza las techas de flechas para nadar. ¡Se debe trabajar en equipo para subir los tesoros al barco!"
DivingGameTreasuresRetrieved = "Tesoros conseguidos"

#Distributed Target Game
TargetGameTitle = "Catapulta dibu"
TargetGameInstructionsSinglePlayer = "Aterriza sobre los objetivos para conseguir puntos"
TargetGameInstructionsMultiPlayer = "Aterriza sobre los objetivos para conseguir puntos"
TargetGameBoard = "Ronda %s: mantener el mejor puntaje"
TargetGameCountdown = "Lanzamiento forzado en %s segundos"
TargetGameCountHelp = "Oprime repetidas veces las flechas izquierda y derecha\npara ganar potencia y suelta para lanzar"
TargetGameFlyHelp = "Pulsa abajo para abrir el paraguas"
TargetGameFallHelp = "Utiliza las teclas de flecha para aterrizar sobre el objetivo"
TargetGameBounceHelp = "Rebotar puede hacer que falles el objetivo"

#Distributed Photo Game
PhotoGameScoreTaken = "%s: %s\nTú: %s"
PhotoGameScoreBlank = "Puntaje: %s"
PhotoGameScoreOther = "\n%s"#"Puntaje: %s\n%s"
PhotoGameScoreYou = "\n¡Mejor bonificación!"#"Puntaje: %s\n¡Mejor bonificación!"


# DistributedTagGame.py
TagGameTitle = "Las traes"
TagGameInstructions = "Recoge los tesoros. ¡No podrás recoger tesoros cuando LAS TRAIGAS!"
TagGameYouAreIt = "¡Tú las TRAES!"
TagGameSomeoneElseIsIt = "¡%s LAS TRAE!"

# DistributedMazeGame.py
MazeGameTitle = "El laberinto"
MazeGameInstructions = "Recoge los tesoros. ¡Intenta recogerlos todos, pero ten cuidado con los bots!"

# DistributedCatchGame.py
CatchGameTitle = "Atrápalo"
CatchGameInstructions = "Atrapa todas las piezas de %(fruit)s que puedas. ¡Ten cuidado con los " + Cogs + " e intenta no ‘atrapar’ %(badThing)s!"
CatchGamePerfect = "¡PERFECTO!"
CatchGameApples      = 'todas las manzanas'
CatchGameOranges     = 'todas las naranjas'
CatchGamePears       = 'todas las peras'
CatchGameCoconuts    = 'todos los cocos'
CatchGameWatermelons = 'todas las sandías'
CatchGamePineapples  = 'todas las piñas'
CatchGameAnvils      = 'yunque'

# DistributedPieTossGame.py
PieTossGameTitle = "Lanzatartas"
PieTossGameInstructions = "Prueba tu puntería lanzando tartas."

# DistributedPhotoGame.py
PhotoGameInstructions = "Toma fotografías que coincidan con los dibus que se muestran abajo. Dirige la cámara con el mouse y haz clic con el botón izquierdo para tomar una fotografía. Pulsa Ctrl para acercar o alejar la imagen y mira a tu alrededor con las teclas de flecha. ¡Las fotografías con una calificación más alta te darán más puntos!"
PhotoGameTitle = "Diver Foto"
PhotoGameFilm = "PELÍCULA"
PhotoGameScore = "Puntaje del equipo: %s\n\nMejores fotos: %s\n\nPuntaje total: %s"

# DistributedCogThiefGame.py
CogThiefGameTitle = Cog + " Ladrón"
CogThiefGameInstructions = "¡Impide que los " + Cogs + " roben los barriles de bromas! Pulsa la tecla Ctrl para lanzar una tarta. Utiliza las teclas de flecha para moverte. Consejo: te puedes mover en diagonal."
CogThiefBarrelsSaved = "¡%(num)d barriles\nsalvados!"
CogThiefBarrelSaved = "¡%(num)d barril\nsalvado!"
CogThiefNoBarrelsSaved = "¡Ningún barril\nsalvado"
CogThiefPerfect = "¡PERFECTO!"

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "JUGAR"

# Purchase.py
GagShopName = "Tienda de bromas de Goofy"
GagShopPlayAgain = "JUGAR\nOTRA VEZ"
GagShopBackToPlayground = "VOLVER AL\nDIBUPARQUE"
GagShopYouHave = "Tienes %s golosinas para gastar"
GagShopYouHaveOne = "Tienes 1 golosina para gastar"
GagShopTooManyProps = "Lo siento, tienes demasiados accesorios"
GagShopDoneShopping = "COMPRAS\nFINALIZADAS"
# name of a gag
GagShopTooManyOfThatGag = "Lo siento, ya tienes suficientes %s."
GagShopInsufficientSkill = "Todavía no tienes suficiente habilidad para eso"
# name of a gag
GagShopYouPurchased = "Compraste %s"
GagShopOutOfJellybeans = "¡Lo siento, te quedaste sin golosinas!"
GagShopWaitingOtherPlayers = "Esperando a otros jugadores..."
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%s se desconectó"
GagShopPlayerExited = "%s se marchó"
GagShopPlayerPlayAgain = "Jugar de nuevo"
GagShopPlayerBuying = "Comprando"

# MakeAToon.py
GenderShopQuestionMickey = "¡Para crear un dibuchico, haz clic en mí!"
GenderShopQuestionMinnie = "¡Para crear una dibuchica, haz clic en mí!"
GenderShopFollow = "¡Sígueme!"
GenderShopSeeYou = "¡Hasta luego!"
GenderShopBoyButtonText = "Chico"
GenderShopGirlButtonText = "Chica"

# BodyShop.py
BodyShopHead = "Cabeza"
BodyShopBody = "Cuerpo"
BodyShopLegs = "Piernas"

# ColorShop.py
ColorShopToon = "Color del dibu"
ColorShopHead = "Cabeza"
ColorShopBody = "Cuerpo"
ColorShopLegs = "Piernas"
ColorShopParts = "Multicolor"
ColorShopAll = "Un color"

# ClothesShop.py
ClothesShopShorts = "shorts"
ClothesShopShirt = "Camiseta"
ClothesShopBottoms = "Falda"

# MakeAToon
PromptTutorial = "¡¡Felicidades!!\n¡Eres el nuevo ciudadano de Toontown!\n\n¿Quieres continuar el Dibututorial o teletransportarte directamente al Centro de Toontown?"
MakeAToonSkipTutorial = "Omitir Dibututorial"
MakeAToonEnterTutorial = "Acceder al Dibututorial"
MakeAToonDone = "Listo"
MakeAToonCancel = lCancel
MakeAToonNext = lNext
MakeAToonLast = "Atrás"
CreateYourToon = "Haz clic en las flechas para crear a tu dibu."
CreateYourToonTitle = "Crea a tu dibu"
ShapeYourToonTitle = "Elige tu tipo"
PaintYourToonTitle = "Elige tu color"
PickClothesTitle = "Elige tu ropa"
NameToonTitle = "Elige tu nombre"
CreateYourToonHead = "Haz clic en las flechas de la \"cabeza\" para escoger diferentes animales."
MakeAToonClickForNextScreen = "Haz clic en la flecha de abajo para ir a la pantalla siguiente."
PickClothes = "¡Haz clic en las flechas para escoger prendas!"
PaintYourToon = "¡Haz clic en las flechas para pintar a tu dibu!"
MakeAToonYouCanGoBack = "¡También puedes volver para cambiar tu cuerpo!"
MakeAFunnyName = "¡Elige un nombre divertido para el dibu con el juego de los nombres!"
MustHaveAFirstOrLast1 = "Tu dibu debería tener un nombre o un apellido, ¿no crees?"
MustHaveAFirstOrLast2 = "¿No quieres que tu dibu tenga un nombre o un apellido?"
ApprovalForName1 = "¡Eso es, tu dibu se merece un gran nombre!"
ApprovalForName2 = "¡Los nombres de dibus son los mejores!"
MakeAToonLastStep = "¡Último paso antes de ir a Toontown!"
PickANameYouLike = "¡Escoge un nombre que te guste!"
TitleCheckBox = "Título"
FirstCheckBox = "Nombre"
LastCheckBox = "Apellido"
RandomButton = "Al azar"
ShuffleButton = "Mezclar"
NameShopSubmitButton = "Enviar"
TypeANameButton = "Escribe un nombre"
TypeAName = "¿No te gustan estos nombres?\nHaz clic aquí -->"
PickAName = "¡Prueba con el juego de los nombres!\nHaz clic aquí -->"
PickANameButton = "Juego de los nombres"
RejectNameText = "Ese nombre no está permitido. Inténtalo de nuevo."
WaitingForNameSubmission = "Se está enviando tu nombre..."

# PetshopGUI.py
PetNameMaster = "PetNameMasterEnglish.txt"
PetshopUnknownName = "Nombre: ???"
PetshopDescGender = "Género:\t%s"
PetshopDescCost = "Precio:\t%s golosinas"
PetshopDescTrait = "Premios:\t%s"
PetshopDescStandard = "Estándar"
PetshopCancel = lCancel
PetshopSell = "Vender pez"
PetshopAdoptAPet = "Adoptar a un Dibuperrito"
PetshopReturnPet = "Devolver a tu Dibuperrito"
PetshopAdoptConfirm = "¿Adoptar una mascota %s por %d golosinas?"
PetshopGoBack = "Volver"
PetshopAdopt = "Adoptar"
PetshopReturnConfirm = "¿Devolver a tu %s?"
PetshopReturn = "Regresar"
PetshopChooserTitle = "PERRITOS DE HOY"
PetshopGoHomeText = '¿Quieres ir a tu hacienda a jugar con tu nuevo Dibuperrito?'

# NameShop.py
NameShopNameMaster = "NameMaster_castillian.txt"
NameShopPay = "¡Suscríbete ya!"
NameShopPlay = "Prueba gratuita"
NameShopOnlyPaid = "Solo los usuarios abonados\npueden poner nombre a sus dibus.\nHasta que te suscribas,\ntu nombre será\n"
NameShopContinueSubmission = "Continuar envío"
NameShopChooseAnother = "Elegir otro nombre"
NameShopToonCouncil = "El Consejo Dibu\nrevisará tu\nnombre.  " + \
                      "La revisión puede\ntardar unos días.\nMientras esperas,\ntu nombre será\n "
PleaseTypeName = "Escribe tu nombre:"
AllNewNames = "Todos los nombres nuevos\ndeben ser aprobados\npor el Consejo Dibu."
NameMessages = "Sé creativo y recuerda:\nningún nombre relacionado con Disney."
NameShopNameRejected = "El nombre que \nenviaste fue \nrechazado."
NameShopNameAccepted = "¡Felicitaciones!\nEl nombre que \nenviaste fue \naceptado."
NoPunctuation = "¡No puedes usar signos de puntuación en tu nombre!"
PeriodOnlyAfterLetter = "Tu nombre puede incluir un punto, pero solo después de una letra."
ApostropheOnlyAfterLetter = "Tu nombre puede incluir un apóstrofo, pero solo después de una letra."
NoNumbersInTheMiddle = "Es posible que los números no aparezcan si están en medio de una palabra."
ThreeWordsOrLess = "Tu nombre debe tener un máximo de tres palabras."
CopyrightedNames = (
    "mickey",
    "mickey mouse",
    "mickeymouse",
    "minnie",
    "minnie mouse",
    "minniemouse",
    "donald",
    "pato donald",
    "patodonald",
    "pluto",
    "goofy",
    )
NumToColor = ['Blanco', 'Melocotón', 'Rojo brillante', 'Rojo', 'Castaño',
              'Siena', 'Café', 'Café claro', 'Coral', 'Naranja',
              'Amarillo', 'Crema', 'Topacio', 'Lima', 'Verde mar',
              'Verde', 'Azul claro', 'Aguamarina', 'Azul',
              'Hierba', 'Azul marino', 'Azul pizarra', 'Morado',
              'Lavanda', 'Rosa', 'Ciruela', 'Negro']
AnimalToSpecies = {
    'dog'    : 'Perro',
    'cat'    : 'Gato',
    'mouse'  : 'Ratón',
    'horse'  : 'Caballo',
    'rabbit' : 'Conejo',
    'duck'   : 'Pato',
     'monkey' : 'Mono',
    'bear'   : 'Oso',
    'pig'    : 'Cerdo'
    }
NameTooLong = "Ese nombre es demasiado largo. Inténtalo de nuevo."
ToonAlreadyExists = "¡Ya tienes un dibu llamado %s!"
NameAlreadyInUse = "¡Ese nombre ya está seleccionado!"
EmptyNameError = "Primero debes introducir un nombre."
NameError = "Lo siento. Ese nombre no sirve."

# NameCheck.py
NCTooShort = 'Ese nombre es demasiado corto.'
NCNoDigits = 'Tu nombre no puede contener números.'
NCNeedLetters = 'Todas las palabras de tu nombre deben contener letras.'
NCNeedVowels = 'Todas las palabras de tu nombre deben contener vocales.'
NCAllCaps = 'Tu nombre no puede estar por completo en mayúsculas.'
NCMixedCase = 'Ese nombre tiene demasiadas mayúsculas.'
NCBadCharacter = "Tu nombre no puede contener el caracter '%s'"
NCGeneric = 'Lo siento, ese nombre no sirve.'
NCTooManyWords = 'Tu nombre no puede tener más de cuatro palabras.'
NCDashUsage = ("Solo puedes usar los guiones para unir dos palabras "
               "(como en \"Bu-bu\").")
NCCommaEdge = "Tu nombre no puede comenzar ni terminar con una coma."
NCCommaAfterWord = "No puedes comenzar una palabra con una coma."
NCCommaUsage = ('Ese nombre no emplea las comas correctamente. Las comas deben '
                'unir dos palabras, como en el nombre \"Dr. Pato, cirujano\"". '
                'Además, las comas deben ir seguidas por un espacio.')
NCPeriodUsage = ('Ese nombre no emplea los puntos correctamente. Sólo se permiten '
                 'los puntos en palabras como \"Sr.\", \"Sra.\", \"J.T.\", etc.')
NCApostrophes = 'Ese nombre tiene demasiados apóstrofos.'

# DistributedTrophyMgrAI.py
RemoveTrophy = lToonHQ+" dibu: ¡"+TheCogs+" tomaron el control de uno de los edificios que recuperaste!"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = '¿Necesitas más tiempo para pensarlo?'
STOREOWNER_GOODBYE = '¡Hasta luego!'
STOREOWNER_NEEDJELLYBEANS = 'Tienes que subir al tranvía para conseguir golosinas.'
STOREOWNER_GREETING = 'Elige lo que quieras comprar.'
STOREOWNER_BROWSING = 'Puedes mirar pero para comprar necesitas un boleto de ropa.'
STOREOWNER_NOCLOTHINGTICKET = 'Para comprar prendas necesitas un boleto de ropa.'

STOREOWNER_NOFISH = 'Vuelve aquí para vender peces a la tienda de animales a cambio de golosinas.'
STOREOWNER_THANKSFISH = '¡Gracias! A la tienda de animales le van a encantar. ¡Adiós!'
STOREOWNER_THANKSFISH_PETSHOP = "¡Qué especímenes tan interesantes! Gracias."
STOREOWNER_PETRETURNED = "No te preocupes. Encontraremos un hogar lindo para tu Dibuperrito."
STOREOWNER_PETADOPTED = "¡Felicidades por tu nuevo Dibuperrito! Puedes jugar con él en tu hacienda."
STOREOWNER_PETCANCELED = "Recuerda, si ves un Dibuperrito que te guste, ¡adóptalo antes de que lo haga otro!"

STOREOWNER_NOROOM = "Mmm... Tienes que tener mas sitio en tu clóset antes de comprar mas ropa.\n"
STOREOWNER_CONFIRM_LOSS = "Tu closet esta lleno. Vas a perder la ropa que estabas usando."
STOREOWNER_OK = "Muy bien"
STOREOWNER_CANCEL = lCancel
STOREOWNER_TROPHY = "¡Uau! Conseguiste %s de %s peces. ¡Te mereces un trofeo y una subida del risómetro!"
# end translate

# NewsManager.py
SuitInvasionBegin1 = lToonHQ+": ¡¡Hay una invasión de bots!!"
SuitInvasionBegin2 = lToonHQ+": ¡¡Los %s tomaron Toontown!!!"
SuitInvasionEnd1 = lToonHQ+": ¡¡¡La invasión de %s terminó!!!"
SuitInvasionEnd2 = lToonHQ+": ¡¡¡Los dibus volvieron a salvarnos!!!"
SuitInvasionUpdate1 = lToonHQ+": ¡¡¡La invasión de bots consta ahora de %s bots!!!"
SuitInvasionUpdate2 = lToonHQ+": ¡¡¡Debemos derrotar a esos %s!!!"
SuitInvasionBulletin1 = lToonHQ+": ¡¡¡Se está produciendo una invasión de bots!!!"
SuitInvasionBulletin2 = lToonHQ+": ¡¡Los %s tomaron Toontown!!!"

# DistributedHQInterior.py
LeaderboardTitle = "Pelotón de dibus"
# QuestScript.txt
QuestScriptTutorialMickey_1 = "¡Toontown tiene un nuevo habitante! ¿Tienes alguna broma de sobra?"
QuestScriptTutorialMickey_2 = "¡Claro, %s!"
QuestScriptTutorialMickey_3 = "Tato Tutorial te explicará todo sobre los bots.\a¡Tengo que irme!"
QuestScriptTutorialMickey_4 = "¡Ven aquí! Usa las flechas del teclado para moverte."

# These are needed to correspond to the Japanese gender specific phrases
QuestScriptTutorialMinnie_1 = "¡Toontown tiene un nuevo habitante! ¿Tienes alguna broma de sobra?"
QuestScriptTutorialMinnie_2 = "¡Claro, %s!"
QuestScriptTutorialMinnie_3 = "Tato Tutorial te explicará todo sobre los bots.\a¡Tengo que irme!"

QuestScript101_1 = "Esos son los BOTS. Son robots que intentan tomar el control de Toontown."
QuestScript101_2 = "Hay muchos tipos distintos de BOTS, que..."
QuestScript101_3 = "...convierten los alegres edificios de los dibus..."
QuestScript101_4 = "...¡en horribles edificios bot!"
QuestScript101_5 = "¡Pero los BOTS no soportan las bromas!"
QuestScript101_6 = "Una buena broma acaba con ellos."
QuestScript101_7 = "Hay un montón de bromas, pero puedes empezar con estas."
QuestScript101_8 = "¡Oh! ¡También necesitas un risómetro!"
QuestScript101_9 = "Si tu risómetro disminuye demasiado, te pondrás triste."
QuestScript101_10 = "¡Cuanto más contento está un dibu, más sano está!"
QuestScript101_11 = "¡OH, NO! ¡Hay un BOT fuera de la tienda!"
QuestScript101_12 = "¡AYÚDAME, POR FAVOR! ¡Derrota a ese BOT!"
QuestScript101_13 = "¡Aquí tienes tu primera dibutarea!"
QuestScript101_14 = "¡Deprisa! ¡Derrota a ese secuaz!"

QuestScript110_1 = "Gracias por derrotar a ese bot. Te daré un dibucuaderno..."
QuestScript110_2 = "Es un cuaderno lleno de cosas lindas."
QuestScript110_3 = "Ábrelo y te iré enseñando cosas."
QuestScript110_4 = "El mapa te muestra dónde estuviste."
QuestScript110_5 = "Pasa la página para ver tus bromas..."
QuestScript110_6 = "¡Uy! ¡No tienes bromas! Te voy a asignar una tarea."
QuestScript110_7 = "Pasa la página para ver las tareas."
QuestScript110_8 = "Para comprar bromas tienes que subirte al tranvía y conseguir golosinas."
QuestScript110_9 = "Para subirte al tranvía, sal por la puerta que hay detrás de mí y dirígete al dibuparque."
QuestScript110_10 = "Ahora, cierra el dibucuaderno y busca el tranvía."
QuestScript110_11 = "Vuelve al cuartel general cuando termines. ¡Adiós!"

QuestScriptTutorialBlocker_1 = "¡Eh, hola!"
QuestScriptTutorialBlocker_2 = "¿Hola?"
QuestScriptTutorialBlocker_3 = "¡Oh! ¡No sabes cómo se usa SpeedChat!"
QuestScriptTutorialBlocker_4 = "Haz clic en el botón para decir algo."
QuestScriptTutorialBlocker_5 = "¡Muy bien!\aEn el sitio al que vas hay muchos dibus con los que puedes hablar."
QuestScriptTutorialBlocker_6 = "Si quieres charlar con tus amigos mediante el teclado, tienes que usar otro botón."
QuestScriptTutorialBlocker_7 = "Es el botón \"Charla\". Para poder usarlo tienes que ser ciudadano de Toontown."
QuestScriptTutorialBlocker_8 = "¡Buena suerte! ¡Hasta luego!"

"""
GagShopTut

You will also earn the ability to use other types of gags.

"""

QuestScriptGagShop_1 = "¡Bienvenido a la tienda de bromas!"
QuestScriptGagShop_1a = "Aquí es donde vienen los dibus a comprar bromas para usar contra los bots."
#QuestScriptGagShop_2 = "En este bote se muestran las golosinas que tienes."
#QuestScriptGagShop_3 = "Para comprar una broma, haz clic sobre el botón de una broma. ¡Prueba ahora!"
QuestScriptGagShop_3 = "Para comprar bromas, haz clic sobre los botones de bromas. ¡Intenta conseguir algunas ahora!"
QuestScriptGagShop_4 = "¡Bien! Puedes usar estas bromas en las batallas contra los bots."
QuestScriptGagShop_5 = "Echa un vistazo a las bromas avanzadas de lanzamiento y chorro..."
QuestScriptGagShop_6 = "Cuando termines de comprar bromas, haz clic en este botón para regresar al dibuparque."
QuestScriptGagShop_7 = "Normalmente, puedes utilizar este botón para jugar otro juego del tranvía..."
QuestScriptGagShop_8 = "...pero ahora no hay tiempo para otro juego. ¡Te necesitan en el cuartel general!"

QuestScript120_1 = "¡Qué bien, encontraste el tranvía!\aPor cierto, ¿conoces ya a Billetón el banquero?\aEs bastante goloso.\a¿Por qué no te presentas llevándole este chocolate como regalo?"
QuestScript120_2 = "Billetón el banquero está en el Banco de Toontown."

QuestScript121_1 = "Mmm, gracias por el chocolate.\aOye, si me ayudas, te daré una recompensa.\a"+TheCogs+" robaron las llaves de mi caja fuerte. Derrota a los bots hasta recuperar la llave robada.\aCuando encuentres la llave, tráemela."

QuestScript130_1 = "¡Que bien, encontraste el tranvía!\aPor cierto, hoy recibí un paquete para Pedro el maestro.\aDeben de ser las nuevas tizas que encargó.\a¿Puedes llevárselas?\aEstá en el colegio."

QuestScript131_1 = "Oh, gracias por las tizas.\a¡¿Qué?!\a"+TheCogs+" me robaron la pizarra. Véncelos y recupera mi pizarra.\aCuando la encuentres, tráemela."

QuestScript140_1 = "¡Que bien, encontraste el tranvía!\aPor cierto, mi amigo Leopoldo es todo un devorador de libros.\aLa última vez que estuve en "+lDonaldsDock+" traje este libro para él.\a¿Podrías llevárselo? Suele estar en la biblioteca."

QuestScript141_1 = "Oh, sí, con este libro casi completaré mi colección.\aDéjame ver...\aEy...\a¿Dónde dejé las gafas?\aLas tenía justo antes de que los bots ocupasen mi edificio.\aDerrótales y recupera mis gafas.\aCuando las encuentres, tráemelas y te daré una recompensa."

QuestScript145_1 = "¡Veo que no tuviste problemas con el tranvía!\aEscucha, los bots nos robaron el borrador de la pizarra.\aSal a la calle y lucha contra los bots hasta que recuperes el borrador.\aPara llegar a las calles, atraviesa uno de los túneles del siguiente modo:"
QuestScript145_2 = "Cuando encuentres nuestro borrador, tráelo aquí.\aNo olvides que, si necesitas bromas, tienes que subir al tranvía.\aAdemás, si necesitas recuperar puntos de risa, consigue conos de helado en el dibuparque."

QuestScript150_1 = "Oh... ¡Es posible que la tarea siguiente sea demasiado difícil para que la hagas solo!"
QuestScript150_2 = "Para hacerte amigo de alguien, busca a otro jugador y pulsa el botón Amigo nuevo."
QuestScript150_3 = "Cuando tengas un amigo nuevo, vuelve aquí."
QuestScript150_4 = "¡Algunas tareas son demasiado difíciles para hacerlas solo!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignórame"

SellbotBossName = "VIP mayor."
CashbotBossName = "C. F. O."
LawbotBossName = "Juez"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "Los declaro ascendidos a %s hechos y derechos. ¡Felicitaciones!"
BossCogDoobersAway = { 's' : "¡Adiós! ¡Y a cerrar ventas!" }
BossCogWelcomeToons = "¡Bienvenidos, bots nuevos!"
BossCogPromoteToons = "Los declaro ascendidos a %s hechos y derechos. Felicit--"
CagedToonInterruptBoss = "¡Eh! ¡Oye! ¡Oye, aquí!"
CagedToonRescueQuery = "¡Eh, dibus! ¿Vinieron a rescatarme?"
BossCogDiscoverToons = "¿Cómo? ¡Dibus disfrazados!"
BossCogAttackToons = "¡Al ataque!"
CagedToonDrop = [
    "¡Muy bien! ¡Casi está destruido!",
    "¡Hay que seguirlo! ¡Se escapa!",
    "¡Genial!",
    "¡Así, así! ¡Ya casi está!",
    ]
CagedToonPrepareBattleTwo = "¡Cuidado, se escapa!\aAyuda: ¡Hay que subir y detenerlo!"
CagedToonPrepareBattleThree = "¡Yupii, ya me estoy viendo libre!\aAhora ataca al bot VIP directamente.\aTengo aquí un montón de tartas que puedes lanzarle.\aSalta y toca la base de la jaula para que te las dé.\aPulsa la tecla Borrar para lanzar las tartas una vez las tengas."
BossBattleNeedMorePies = "¡Necesitas más tartas!"
BossBattleHowToGetPies = "Salta para tocar la jaula y conseguir tartas."
BossBattleHowToThrowPies = "Pulsa la tecla Borrar para lanzar las tartas!"
CagedToonYippee = "¡Hurra!"
CagedToonThankYou = "¡Por fin libre!\a¡Muchísimas gracias por tu ayuda!\aEstoy en deuda contigo.\aSi alguna vez necesitas que te eche una mano luchando, no dudes en llamarme con el botón SOS."
CagedToonPromotion = "\a¡Eh! Ese bot VIP se olvidó los documentos de tu ascenso.\aLos archivaré a la salida para que no te quedes sin el ascenso."
CagedToonLastPromotion = "\¡Bien! Alcanzaste el nivel %s de traje bot.\aEs el máximo en la escala de ascensos bot.\aYa no puedes seguir mejorando el traje, pero sí puedes seguir rescatando dibus."
CagedToonHPBoost = "\aHas rescatado a un montón de dibus de este cuartel general.\aEl Consejo Dibu decidió darte otro punto de risa. ¡Felicitaciones!"
CagedToonMaxed = "\aVeo que tienes un traje bot nivel %s. Estamos muy impresionados.\aEn nombre del Consejo Dibu, te damos las gracias por regresar para rescatar más dibus."
CagedToonGoodbye = "¡Nos vemos!"


CagedToonBattleThree = {
    10: "¡Qué salto, %(toon)s! Aquí tienes las tartas.",
    11: "¡Hola, %(toon)s! Ahí van las tartas.",
    12: "¡Oye, %(toon)s! Mira cuántas tartas que tienes ahora.",

    20: "¡Oye, %(toon)s! Salta a la jaula que te doy unas tartitas para que las tires.",
    21: "¡Hola, %(toon)s! Dale a la tecla Ctrl para saltar y tocar la jaula.",

    100: "Pulsa la tecla Borrar para lanzar las tartas.",
    101: "El contador azul indica a qué altura llegará la tarta.",
    102: "Primero, intenta colarle una tarta dentro del mecanismo de las piernas para bloquearlo.",
    103: "Espera a que se abra la puerta y lanza la tarta por el hueco.",
    104: "Cuando esté mareado, túmbalo dándole en la cara o el pecho.",
    105: "Si la tarta salpica en colores, es que el tiro fue perfecto.",
    106: "Si le das a un dibu con una tarta, recibirá un punto de risa.",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

CashbotBossHadEnough = "Ya está bien. ¡Me harté de esos dibus tan molestos!"
CashbotBossOuttaHere = "¡Tengo que tomar un tren!"
ResistanceToonName = "Mata Hairy"
ResistanceToonCongratulations = "¡Lo lograste! ¡Felicidades!\a¡Tu ayuda mejorará la Resistencia!\aToma esta frase especial que puedes usar en un punto difícil:\a%s\aCuando la digas, %s.\aPero sólo puedes usarla una vez,´¡así que elige bien el momento!"
ResistanceToonToonupInstructions = "todos los dibus que estén cerca ganarán %s puntos de risa"
ResistanceToonToonupAllInstructions = "todos los dibus que estén cerca ganarán el máximo de puntos de risa"
ResistanceToonMoneyInstructions = "todos los dibus que estén cerca ganarán %s golosinas"
ResistanceToonMoneyAllInstructions = "todos los dibus que estén cerca llenarán sus tarros de golosinas"
ResistanceToonRestockInstructions = "todos los dibus que estén cerca se reabastecerán de bromas \"%s\""
ResistanceToonRestockAllInstructions = "todos los dibus que estén cerca reabastecerán todas sus bromas"

ResistanceToonLastPromotion = "\a¡Uau, alcanzaste el nivel %s con tu traje bot!\aLos bots no pueden ascender más alto.\aYa no puedes mejorar más tu traje bot ¡pero puedes seguir trabajando para la Resistencia!"
ResistanceToonHPBoost = "\aHas trabajado mucho para la Resistencia.\aEl Consejo Dibu decidió darte otro punto de risa. ¡Felicidades!"
ResistanceToonMaxed = "\aVeo que tienes un traje bot de nivel %s. ¡Impresionante!\aEn nombre del Consejo Dibu, ¡gracias por volver a rescatar más dibus!"

CashbotBossCogAttack = "¡¡¡A ellos!!!"
ResistanceToonWelcome = "¡Lo lograste! ¡Sígueme hasta la cámara principal antes de que nos encuentre el director financiero!"
ResistanceToonTooLate = "¡Rayos!¡Es demasiado tarde!"
CashbotBossDiscoverToons1 = "¡A-JÁ!"
CashbotBossDiscoverToons2 = "¡Ya me parecía que aquí olía a dibu! ¡Impostores!"
ResistanceToonKeepHimBusy = "¡Mantenlo ocupado! ¡Voy a preparar una trampa!"
ResistanceToonWatchThis = "¡Cuidado con esto!"
CashbotBossGetAwayFromThat = "¡Eh! ¡Aléjate de eso!"
ResistanceToonCraneInstructions1 = "Controla un imán subiendo a un podio."
ResistanceToonCraneInstructions2 = "Usa las teclas de flecha para mover la grúa y pulsa la tecla Ctrl para tomar un objeto."
ResistanceToonCraneInstructions3 = "Toma una caja fuerte con un imán y haz que se caiga el casco de seguridad del director financiero."
ResistanceToonCraneInstructions4 = "¡Una vez quitado el casco, toma un matón desactivado y dále en la cabeza!"
ResistanceToonGetaway = "¡Uff! ¡Tengo que correr!"
CashbotCraneLeave = "Salir de la grúa"
CashbotCraneAdvice = "Usa las teclas de flecha para mover la grúa."
CashbotMagnetAdvice = "Mantén pulsada la tecla Ctrl para agarrar cosas."
CashbotCraneLeaving = "Saliendo de la grúa..."

MintElevatorRejectMessage = "No puedes entrar a las fabrica de monedas hasta haber completado tu traje bot %s." 
BossElevatorRejectMessage = "No puedes subir a este ascensor hasta que no te merezcas un ascenso."
NotYetAvailable = "Este ascensor todavía no está disponible."

# Types of catalog items--don't translate yet.
FurnitureTypeName = "Mueble"
PaintingTypeName = "Cuadro"
ClothingTypeName = "Ropa"
ChatTypeName = "Frase de SpeedChat"
EmoteTypeName = "Clases de teatro"
BeanTypeName = "Golosinas"
PoleTypeName = "Caña de pescar"
WindowViewTypeName = "Vista desde la ventana"
PetTrickTypeName = "Entrenamiento de Dibuperrito"
GardenTypeName = "Suministros para el jardín"
RentalTypeName = "Objeto de alquiler"
GardenStarterTypeName = "Kit de jardinería"
NametagTypeName = "Etiqueta para el nombre"

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
    10 : PoleTypeName, 
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
    'bss1' : "solid",
    'bss2' : "single stripe",
    'bss3' : "collar",
    'bss4' : "double stripe",
    'bss5' : "multiple stripes",
    'bss6' : "collar w/ pocket",
    'bss7' : "hawaiian",
    'bss8' : "collar w/ 2 pockets",
    'bss9' : "bowling shirt",
    'bss10' : "vest (special)",
    'bss11' : "collar w/ ruffles",
    'bss12' : "soccer jersey (special)",
    'bss13' : "lightning bolt (special)",
    'bss14' : "jersey 19 (special)",
    'bss15' : "guayavera",

    # -------------------------------------------------------------------------
    # Girl styles
    # -------------------------------------------------------------------------
    'gss1' : "girl solid",
    'gss2' : "girl single stripe",
    'gss3' : "girl collar",
    'gss4' : "girl double stripes",
    'gss5' : "girl collar w/ pocket",
    'gss6' : "girl flower print",
    'gss7' : "girl flower trim (special)",
    'gss8' : "girl collar w/ 2 pockets",
    'gss9' : "girl denim vest (special)",
    'gss10' : "girl peasant",
    'gss11' : "girl peasant w/ mid stripe",
    'gss12' : "girl soccer jersey (special)",
    'gss13' : "girl hearts",
    'gss14' : "girl stars (special)",
    'gss15' : "girl flower",

    # -------------------------------------------------------------------------
    # Special Catalog-only shirts. 
    # -------------------------------------------------------------------------
    # yellow hooded - Series 1
    'c_ss1' : "yellow hooded - Series 1",
    'c_ss2' : "yellow with palm tree - Series 1",
    'c_ss3' : "purple with stars - Series 2",
    'c_bss1' : "blue stripes (boys only) - Series 1",
    'c_bss2' : "orange (boys only) - Series 1",
    'c_bss3' : "lime green with stripe (boys only) - Series 2",
    'c_bss4' : "red kimono with checkerboard (boys only) - Series 2",
    'c_gss1' : "girl blue with yellow stripes (girls only) - Series 1",
    'c_gss2' : "girl pink and beige with flower (girls only) - Series 1",
    'c_gss3' : "girl Blue and gold with wavy stripes (girls only) - Series 2",
    'c_gss4' : "girl Blue and pink with bow (girls only) - Series 2",
    'c_gss5' : "girl Aqua kimono white stripe (girls only) - UNUSED",
    'c_ss4'  : "Tie dye shirt (boys and girls) - Series 3",
    'c_ss5' : "light blue with blue and white stripe (boys only) - Series 3",
    'c_ss6' : "cowboy shirt 1 : Series 4",
    'c_ss7' : "cowboy shirt 2 : Series 4",
    'c_ss8' : "cowboy shirt 3 : Series 4",
    'c_ss9' : "cowboy shirt 4 : Series 4",
    'c_ss10' : "cowboy shirt 5 : Series 4",
    'c_ss11' : "cowboy shirt 6 : Series 4",
    
    # Special Holiday-themed shirts.
    'hw_ss1' : "Halloween ghost",
    'hw_ss2' : "Halloween pumpkin",
    'wh_ss1' : "Winter Holiday 1",
    'wh_ss2' : "Winter Holiday 2",
    'wh_ss3' : "Winter Holiday 3",
    'wh_ss4' : "Winter Holiday 4",

    'vd_ss1' : "girl Valentines day, pink with red hearts (girls)",
    'vd_ss2' : "Valentines day, red with white hearts",
    'vd_ss3' : "Valentines day, white with winged hearts (boys)",
    'vd_ss4' : " Valentines day, pink with red flamed heart",
    'vd_ss5' : "2009 Valentines day, white with red cupid",
    'vd_ss6' : "2009 Valentines day, blue with green and red hearts",
    'sd_ss1' : "St Pat's Day, four leaf clover shirt",
    'sd_ss2' : "St Pat's Day, pot o gold shirt",
    'tc_ss1' : "T-Shirt Contest, Fishing Vest",
    'tc_ss2' : "T-Shirt Contest, Fish Bowl",
    'tc_ss3' : "T-Shirt Contest, Paw Print",
    'tc_ss4' : "T-Shirt Contest, Backpack",
    'tc_ss5' : "T-Shirt Contest, Lederhosen ",
    'tc_ss6' : "T-Shirt Contest, Watermelon  ",
    'tc_ss7' : "T-Shirt Contest, Race Shirt",
    'j4_ss1' : "July 4th, Flag",
    'j4_ss2' : "July 4th, Fireworks",
    'c_ss12' : "Catalog series 7, Green w/ yellow buttons",
    'c_ss13' : "Catalog series 7, Purple w/ big flower",

    'pj_ss1' : "Blue Banana Pajama shirt",
    'pj_ss2' : "Red Horn Pajama shirt",
    'pj_ss3' : "Purple Glasses Pajama shirt",
    
    # Special award clothes
    'sa_ss1' : "Striped Shirt",
    'sa_ss2' : "Fishing Shirt 1",
    'sa_ss3' : "Fishing Shirt 2",
    'sa_ss4' : "Gardening Shirt 1",
    'sa_ss5' : "Gardening Shirt 2",
    'sa_ss6' : "Party Shirt 1",
    'sa_ss7' : "Party Shirt 2",    
    'sa_ss8' : "Racing Shirt 1",    
    'sa_ss9' : "Racing Shirt 2",    
    'sa_ss10' : "Summer Shirt 1",    
    'sa_ss11' : "Summer Shirt 2",    

    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    }

# Make sure this is in sync with ToonDNA.BottomStyles
BottomStylesDescriptions = {
    # name : [ bottomIdx, [bottomColorIdx, ...]]
    # -------------------------------------------------------------------------
    # Boy styles (shorts)
    # -------------------------------------------------------------------------
    'bbs1' : "plain w/ pockets",
    'bbs2' : "belt",
    'bbs3' : "cargo",
    'bbs4' : "hawaiian",
    'bbs5' : "side stripes (special)",
    'bbs6' : "soccer shorts",
    'bbs7' : "side flames (special)",
    'bbs8' : "denim",
    'vd_bs1' : "Valentines shorts",
    'vd_bs2' : "Green with red heart",
    'vd_bs3' : "Blue denim with green and red heart",

    # Catalog only shorts
    'c_bs1' : "Orange with blue side stripes",
    'c_bs2' : "Blue with gold cuff stripes",
    'c_bs5' : 'Green stripes - series 7',
    'sd_bs1' : 'St. Pats leprechaun shorts',
    'pj_bs1' : 'Blue Banana Pajama pants',
    'pj_bs2' : 'Red Horn Pajama pants',
    'pj_bs3' : 'Purple Glasses Pajama pants',
    'wh_bs1' : 'Winter Holiday Shorts Style 1',
    'wh_bs2' : 'Winter Holiday Shorts Style 2',
    'wh_bs3' : 'Winter Holiday Shorts Style 3',
    'wh_bs4' : 'Winter Holiday Shorts Style 4',
    
    # -------------------------------------------------------------------------
    # Girl styles (shorts and skirts)
    # -------------------------------------------------------------------------
    # skirts
    # -------------------------------------------------------------------------
    'gsk1' : 'solid',
    'gsk2' : 'polka dots (special)',
    'gsk3' : 'vertical stripes',
    'gsk4' : 'horizontal stripe',
    'gsk5' : 'flower print',
    'gsk6' : '2 pockets (special) ',
    'gsk7' : 'denim skirt',
    
    # shorts
    # -------------------------------------------------------------------------
    'gsh1' : 'plain w/ pockets',
    'gsh2' : 'flower',
    'gsh3' : 'denim shorts',
    # Special catalog-only skirts and shorts.
    'c_gsk1' : 'blue skirt with tan border and button',
    'c_gsk2' : 'purple skirt with pink and ribbon',
    'c_gsk3' : 'teal skirt with yellow and star',

    # Valentines skirt
    'vd_gs1' : 'red skirt with hearts',
    'vd_gs2' : 'Pink flair skirt with polka hearts',
    'vd_gs3' : 'Blue denim skirt with green and red heart',
    'c_gsk4' : 'rainbow skirt - Series 3',
    'sd_gs1' : 'St. Pats day shorts',
    'c_gsk5' : 'Western skirts 1',
    'c_gsk6' : 'Western skirts 2',
    # Western shorts
    'c_bs3' : 'Western shorts 1',
    'c_bs4' : 'Western shorts 2',
    'j4_bs1' : 'July 4th shorts',
    'j4_gs1' : 'July 4th Skirt',
    'c_gsk7' : 'Blue with flower - series 7',
    'pj_gs1' : 'Blue Banana Pajama pants',
    'pj_gs2' : 'Red Horn Pajama pants',
    'pj_gs3' : 'Purple Glasses Pajama pants',
    'wh_gsk1' : 'Winter Holiday Skirt Style 1',
    'wh_gsk2' : 'Winter Holiday Skirt Style 2',
    'wh_gsk3' : 'Winter Holiday Skirt Style 3',
    'wh_gsk4' : 'Winter Holiday Skirt Style 4',
    
    'sa_bs1' : "Fishing Shorts",
    'sa_bs2' : "Gardening Shorts",
    'sa_bs3' : "Party Shorts",
    'sa_bs4' : "Racing Shorts",
    'sa_bs5' : "Summer Shorts",
    'sa_gs1' : "Fishing Skirt",
    'sa_gs2' : "Gardening Skirt",    
    'sa_gs3' : "Party Skirt",    
    'sa_gs4' : "Racing Skirt",    
    'sa_gs5' : "Summer Skirt",
    }

AwardMgrBoy = "boy"
AwardMgrGirl = "girl"
AwardMgrUnisex = "unisex"
AwardMgrShorts = "shorts"
AwardMgrSkirt = "skirt"
AwardMgrShirt = "shirt"

# Special Event Strings to display in  mailbox screen
SpecialEventMailboxStrings = {
    1 : "A special item from the Toon council",
    2 : "Prize for Melville's Fishing Tournament",
    3 : "Prize for Billy Bud's Fishing Tournament",    
    }

# Rental items
RentalHours = "Horas"
RentalOf = "De"
RentalCannon = "¡Cañones!"
RentalTime = "Horas de"

EstateCannonGameEnd = "The Cannon Game rental is over."
GameTableRentalEnd = "The Game Table rental is over."

MessageConfirmRent = "¿Iniciar alquiler? Cancela y el alquiler se pospondrá para más tarde"
MessageConfirmGarden = "¿Seguro que quieres empezar un jardín?"

#nametag Names
NametagPaid = "Etiqueta para el nombre del ciudadano"
NametagAction = "Etiqueta para el nombre de la acción"
NametagFrilly = "Etiqueta para el nombre del adorno"

FurnitureYourOldCloset = "tu clóset antiguo"
FurnitureYourOldBank = "tu alcancía antigua"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py
FurnitureNames = {
  100 : "Sillón",
  105 : "Sillón",
  110 : "Silla",
  120 : "Silla de escritorio",
  130 : "Silla de troncos",
  140 : "Silla de langosta",
  145 : "Silla de chaleco salvavidas",
  150 : "Taburete de montar",
  160 : "Silla indígena",
  170 : "Silla de magdalena",
  200 : "Cama",
  205 : "Cama",
  210 : "Cama",
  220 : "Cama de bañera",
  230 : "Cama de hoja",
  240 : "Cama de barco",
  250 : "Hamaca de cactus",
  260 : "Cama de helado",
  270 : "Cama de Erin y el gato",
  300 : "Pianola",
  310 : "Órgano de iglesia",
  400 : "Chimenea",
  410 : "Chimenea",
  420 : "Chimenea redonda",
  430 : "Chimenea",
  440 : "Chimenea de manzana",
  450 : "Chimenea de Erin",
  460 : "Chimenea encendida de Erin",
  470 : "Chimenea encendida",
  480 : "Chimenea redonda encendida",
  490 : "Chimenea encendida",
  491 : "Chimenea encendida",
  492 : "Chimenea encendida manzana",
  500 : "Clóset",
  502 : "Clóset con 15 prendas",
  504 : "Clóset con 20 prendas",
  506 : "Clóset con 25 prendas",
  510 : "Clóset",
  512 : "Clóset con 15 prendas",
  514 : "Clóset con 20 prendas",
  516 : "Clóset con 25 prendas",
  600 : "Lámpara baja",
  610 : "Lámpara alta",
  620 : "Lámpara de mesa",
  625 : "Lámpara de mesa",
  630 : "Lámpara de Daisy",
  640 : "Lámpara de Daisy",
  650 : "Lámpara de medusa",
  660 : "Lámpara de medusa",
  670 : "Lámpara de vaquero",
  700 : "Butaca",
  705 : "Butaca",
  710 : "Sofá",
  715 : "Sofá",
  720 : "Sofá de heno",
  730 : "Sofá de tarta de fruta",
  800 : "Escritorio",
  810 : "Escritorio de troncos",
  900 : "Paragüero",
  910 : "Perchero",
  920 : "Cubo de basura",
  930 : "Taburete rojo",
  940 : "Taburete amarillo",
  950 : "Perchero",
  960 : "Perchero de barril",
  970 : "Cactus",
  980 : "Tipi",
  990 : "Ventilador de Julieta",
  1000 : "Alfombra grande",
  1010 : "Alfombra redonda",
  1015 : "Alfombra redonda",
  1020 : "Alfombra pequeña",
  1030 : "Felpudo de hoja",
  1100 : "Vitrina",
  1110 : "Vitrina",
  1120 : "Estantería alta",
  1130 : "Estantería baja",
  1140 : "Cómoda de copa de helado",
  1200 : "Mesita lateral",
  1210 : "Mesita",
  1215 : "Mesita",
  1220 : "Mesa de centro",
  1230 : "Mesa de centro",
  1240 : "Mesa de buceador",
  1250 : "Mesa de galleta",
  1260 : "Mesita de noche",
  1300 : "Alcancía para 1.000 golosinas",
  1310 : "Alcancía para 2.500 golosinas",
  1320 : "Alcancía para 5.000 golosinas",
  1330 : "Alcancía para 7.500 golosinas",
  1340 : "Alcancía para 10.000 golosinas",
  1399 : "Teléfono",
  1400 : "Dibu Cezanne",
  1410 : "Flores",
  1420 : "Mickey moderno",
  1430 : "Dibu Rembrandt",
  1440 : "Paisaje dibu",
  1441 : "Escena hípica",
  1442 : "Estrella dibu",
  1443 : "¿No es una tarta?",
  1450 : "Mickey y Minnie",
  1500 : "Radio",
  1510 : "Radio",
  1520 : "Radio",
  1530 : "Televisión",
  1600 : "Jarrón pequeño",
  1610 : "Jarrón alto",
  1620 : "Jarrón pequeño",
  1630 : "Jarrón alto",
  1640 : "Jarrón pequeño",
  1650 : "Jarrón pequeño",
  1660 : "Jarrón de coral",
  1661 : "Jarrón de concha",
  1670 : "Jarrón de rosa",
  1680 : "Regadera de rosa",
  1700 : "Carrito de palomitas",
  1710 : "Mariquita",
  1720 : "Fuente",
  1725 : "Lavadora",
  1800 : "Pecera",
  1810 : "Pecera",
  1900 : "Pez espada",
  1910 : "Pez martillo",
  1920 : "Percha de cuernos",
  1930 : "Sombrero sencillo",
  1940 : "Sombrero adornado",
  1950 : "Atrapasueños",
  1960 : "Herradura",
  1970 : "Retrato de bisonte",
  2000 : "Columpios de caramelo",
  2010 : "Tobogán de tarta",
  3000 : "Bañera de banana split",
  10000 : "Calabaza pequeña",
  10010 : "Calabaza alargada",
  10020 : "Árbol de invierno",
  10030 : "Guirnalda de invierno"
  }

# CatalogClothingItem.py
ClothingArticleNames = (
    "Camisa",
    "Camisa",
    "Camisa",
    "Pantalón corto",
    "Pantalón corto",
    "Falda",
    "Pantalón corto",
    )

ClothingTypeNames = {
    1400 : "Camisa de Mateo",
    1401 : "Camisa de Jessica",
    1402 : "Camisa de Marisa",
    1600 : "Traje trampa",
    1601 : "Traje sonido",
    1602 : "Traje cebo",
    1603 : "Traje trampa",
    1604 : "Traje sonido",
    1605 : "Traje cebo",
    1606 : "Traje trampa",
    1607 : "Traje sonido",
    1608 : "Traje cebo",
    }

# CatalogSurfaceItem.py
SurfaceNames = (
    "Papel de pared",
    "Moldura",
    "Suelo",
    "Revestimiento de pared",
    "Borde",
    )

WallpaperNames = {
    1000 : "Pergamino",
    1100 : "Milán",
    1200 : "Marítimo",
    1300 : "Victoria",
    1400 : "Puerto Nuevo",
    1500 : "Pastoral",
    1600 : "Arlequín",
    1700 : "Luna",
    1800 : "Estrellas",
    1900 : "Flores",
    2000 : "Jardín de primavera",
    2100 : "Jardín ornamental",
    2200 : "Un día en las carreras",
    2300 : "Rugby",
    2400 : "Nube 9",
    2500 : "Parras",
    2600 : "Primavera",
    2700 : "Muñequitas japonesas",
    2800 : "Ramilletes",
    2900 : "Tiburón angelote",
    3000 : "Pompas",
    3100 : "Pompas",
    3200 : "Adelante pez",
    3300 : "Detente pez",
    3400 : "Caballito de mar",
    3500 : "Conchas marinas",
    3600 : "Mundo submarino",
    3700 : "Botas",
    3800 : "Cactus",
    3900 : "Sombrero de vaquero",
    10100 : "Gatos",
    10200 : "Murciélagos",
    11000 : "Copos de nieve",
    11100 : "Hoja de acebo",
    11200 : "Muñeco de nieve",
    13000 : "Trébol",
    13100 : "Trébol",
    13200 : "Arcoiris",
    13300 : "Trébol",
    }

FlooringNames = {
    1000 : "Madera",
    1010 : "Moqueta",
    1020 : "Baldosas romboides",
    1030 : "Baldosas romboides",
    1040 : "Hierba",
    1050 : "Ladrillos grises",
    1060 : "Ladrillos rojos",
    1070 : "Baldosas cuadradas",
    1080 : "Piedra",
    1090 : "Tarima",
    1100 : "Tierra",
    1110 : "Parqué",
    1120 : "Baldosas",
    1130 : "Colmena",
    1140 : "Agua",
    1150 : "Baldosas de playa",
    1160 : "Baldosas de playa",
    1170 : "Baldosas de playa",
    1180 : "Baldosas de playa",
    1190 : "Arena",
    10000 : "Cubito de hielo",
    10010 : "Iglú",
    11000 : "Trébol",
    11010 : "Trébol",
    }

MouldingNames = {
    1000 : "Nudos",
    1010 : "Pintada",
    1020 : "Dientes",
    1030 : "Flores",
    1040 : "Flores",
    1050 : "Mariquita",
    }

WainscotingNames = {
    1000 : "Pintado",
    1010 : "Paneles de madera",
    1020 : "Madera",
    }

# CatalogWindowItem.py
WindowViewNames = {
    10 : "Jardín grande",
    20 : "Jardín agreste",
    30 : "Jardín griego",
    40 : "Paisaje urbano",
    50 : "Oeste americano",
    60 : "Mundo submarino",
    70 : "Isla tropical",
    80 : "Noche estrellada",
    90 : "Piscina con toboganes",
    100 : "Paisaje polar",
    110 : "Tierras de labranza",
    120 : "Campamento indígena",
    130 : "Calle principal",
    }

# don't translate yet
NewCatalogNotify = "Llegaron artículos nuevos que puedes pedir llamando desde tu teléfono."
NewDeliveryNotify = "Te acaba de llegar un pedido al buzón."
CatalogNotifyFirstCatalog = "¡Te llegó el primer catálogo tolón-tolón! Lo puedes usar para hacer pedidos de artículos nuevos para ti o para la casa."
CatalogNotifyNewCatalog = "¡Te llegó el catálogo tolón-tolón nº #%s! Haz pedidos llamando desde tu teléfono."
CatalogNotifyNewCatalogNewDelivery = "Te acaba de llegar un pedido al buzón. También llegó el catálogo tolón-tolón nº #%s."
CatalogNotifyNewDelivery = "Te acaba de llegar un pedido al buzón."
CatalogNotifyNewCatalogOldDelivery = "Te llegó el catálogo tolón-tolón nº #%s, pero todavía tienes pedidos en el buzón esperando a que los recojas."
CatalogNotifyOldDelivery = "Todavía tienes pedidos en el buzón esperando a que los recojas."
CatalogNotifyInstructions = "Haz clic en el botón \"Ir a casa\" de la página del dibucuaderno donde aparece el plano y vete al teléfono de tu casa."
CatalogNewDeliveryButton = "¡Nueva\nentrega!"
CatalogNewCatalogButton = "¡Nuevo\ncatálogo\ntolón-tolón!"
CatalogSaleItem = "¡Oferta!  "

# don't translate yet
DistributedMailboxEmpty = "El buzón está vacío. Vuelve después de hacer pedidos por teléfono para recogerlos."
DistributedMailboxWaiting = "El buzón está vacío, pero el pedido que hiciste ya está de camino. Vuelve más tarde."
DistributedMailboxReady = "¡Te llegó el pedido!"
DistributedMailboxNotOwner = "Me temo que este no es tu buzón."
DistributedPhoneEmpty = "Puedes pedir artículos especiales para ti o para la casa desde cualquier teléfono. Cada tanto irán apareciendo artículos nuevos para pedir.\n\nAhora mismo no puedes pedir ningún artículo. Vuelve a intentarlo más tarde."

# don't translate yet
Clarabelle = "Clarabel"
MailboxExitButton = "Cerrar buzón"
MailboxAcceptButton = "Recoger este artículo"
MailBoxDiscard = "Descartar este artículo"
MailboxAcceptInvite = "Aceptar esta invitación"
MailBoxRejectInvite = "Rechazar esta invitación"
MailBoxDiscardVerify = "¿Seguro que quieres descartar: %s?"
MailBoxRejectVerify = "Seguro que quieres rechazar: %s?"
MailboxOneItem = "Tienes 1 artículo en el buzón."
MailboxNumberOfItems = "Tienes %s artículos en el buzón."
MailboxGettingItem = "Recogiendo %s del buzón."
MailboxGiftTag = "Regalo de: %s"
MailboxGiftTagAnonymous = "Anónimo"
MailboxItemNext = "Artículo\nsiguiente"
MailboxItemPrev = "Artículo\nanterior"
MailboxDiscard = "Descartar"
MailboxReject = "Rechazar"
MailboxLeave = "Conservar"
CatalogCurrency = "golosinas"
CatalogHangUp = "Colgar"
CatalogNew = "NUEVO"
CatalogBackorder = "PEDIDO PENDIENTE"
CatalogLoyalty = "ESPECIAL"
CatalogPagePrefix = "Página"
CatalogGreeting = "¡Hola! Gracias por llamar al catálogo tolón-tolón de Clarabel. ¿Qué deseas?"
CatalogGoodbyeList = ["¡Adiós!",
                      "Esperamos tu próxima llamada.",
                      "Gracias por llamarnos.",
                      "Muy bien. Hasta luego.",
                      "¡Adiós!",
                      ]
CatalogHelpText1 = "Pasa la página para ver los artículos que están a la venta."
CatalogSeriesLabel = "Serie %s"
CatalogGiftFor = "Comprar regalo para:"
CatalogGiftTo = "Para: %s"
CatalogGiftToggleOn = "Dejar de regalar"
CatalogGiftToggleOff = "Comprar regalos"
CatalogGiftToggleWait = "¡Intentándolo...!"
CatalogGiftToggleNoAck = "No disponible"
CatalogPurchaseItemAvailable = "¡Que disfrutes de tu compra! Puedes empezar a usar el artículo ahora mismo."
CatalogPurchaseGiftItemAvailable = "¡Excelente! %s puede empezar a utilizar tu regalo inmediatamente."
CatalogPurchaseItemOnOrder = "Muy bien. En breve enviaremos tu compra al buzón."
CatalogPurchaseGiftItemOnOrder = "¡Excelente! Tu regalo para %s será enviado a su buzón."
CatalogAnythingElse = "¿Quieres alguna otra cosa?"
CatalogPurchaseClosetFull = "Tienes el clóset lleno. Puedes comprar esta prenda, pero tendrás que deshacerte de otra del clóset para poder meterla cuando la recibas.\n\n¿Seguro que quieres comprarla?"
CatalogAcceptClosetFull = "Tienes el clóset lleno. Antes de recoger este artículo del buzón tendrás que abrir el clóset y deshacerte de una de las prendas para que quepa la nueva."
CatalogAcceptShirt = "Tienes puesta una camisa nueva. La que tenías antes está ahora en tu clóset."
CatalogAcceptShorts = "Tienes puesto un pantalón corto nuevo. Lo que tenías antes está ahora en tu clóset."
CatalogAcceptSkirt = "Tienes puesto una falda nueva. Lo que tenías antes está ahora en tu clóset."
CatalogAcceptPole = "Ahora, con tu caña nueva ya puedes pescar a lo grande."
CatalogAcceptPoleUnneeded = "La caña de pescar que tienes es mejor que ésta."
CatalogAcceptChat = "¡Tienes un nuevo SpeedChat!"
CatalogAcceptEmote = "¡Tienes una nueva Emoción!"
CatalogAcceptBeans = "¡Recibiste golosinas!"
CatalogAcceptRATBeans = "¡Llegó tu premio por reclutar dibus!"
CatalogAcceptNametag = "¡Llegó la nueva etiqueta de tu nombre!"
CatalogAcceptGarden = "¡Llegaron los suministros para el jardín!"
CatalogAcceptPet = "¡Tienes una nueva acrobacia de mascota!"
CatalogPurchaseHouseFull = "Tienes la casa llena. Puedes comprar este artículo, pero tendrás que deshacerte de otro de la casa para poder meterlo cuando lo recibas.\n\n¿Seguro que quieres comprarlo?"
CatalogAcceptHouseFull = "Tienes la casa llena. Antes de recoger este artículo del buzón tendrás que entrar en la casa y deshacerte de uno de los artículos para que quepa el nuevo."
CatalogAcceptInAttic = "El artículo recién adquirido está en el desván de tu casa. Para colocarlo en la casa, entra y dale al botón \"Cambiar mobiliario de sitio\"."
CatalogAcceptInAtticP = "Los artículos recién adquiridos están en el desván de tu casa. Para colocarlos en la casa, entra y dale al botón \"Cambiar mobiliario de sitio\"."
CatalogPurchaseMailboxFull = "¡Tienes el buzón lleno! No puedes comprar este artículo hasta que no saques algo del buzón para hacer espacio."
CatalogPurchaseGiftMailboxFull = "¡El buzón de %s está lleno! No puedes comprar este artículo."
CatalogPurchaseOnOrderListFull = "Ya pediste muchos artículos. No puedes pedir más hasta que no te lleguen los que están pendientes de entrega."
CatalogPurchaseGiftOnOrderListFull = "%s tiene demasiados pedidos de artículos."
CatalogPurchaseGeneralError = "No pudiste comprar el artículo debido a un error interno del juego: código de error %s."
CatalogPurchaseGiftGeneralError = "El artículo no se le pudo regalar a %(friend)s por un error interno del juego: código de error %(error)s."
CatalogPurchaseGiftNotAGift = "El artículo no se le pudo enviar a %s porque supondría una desventaja injusta."
CatalogPurchaseGiftWillNotFit = "El artículo no se le pudo enviar a %s porque no le cabe."
CatalogPurchaseGiftLimitReached = "El artículo no se le pudo enviar a %s porque ya lo tiene."
CatalogPurchaseGiftNotEnoughMoney = "El artículo no se le pudo enviar a %s porque no te lo puedes permitir."
CatalogAcceptGeneralError = "No se pudo sacar el artículo del buzón debido a un error interno del juego: código de error %s."
CatalogAcceptRoomError = "No tienes espacio para colocar esto. Tendrás que deshacerte de algo."
CatalogAcceptLimitError = "Ya tienes el máximo posible de artículos de este tipo. Tendrás que deshacerte de algo."
CatalogAcceptFitError = "¡Esto no te cabe! Dónalo a dibus necesitados."
CatalogAcceptInvalidError = "¡Este objeto está pasado de moda! Dónalo a dibus necesitados."

MailboxOverflowButtonDicard = "Descartar"
MailboxOverflowButtonLeave = "Dejar"

# don't translate yet
HDMoveFurnitureButton = "Cambiar\nmobiliario\nde sitio"
HDStopMoveFurnitureButton = "Cambio de\nmobiliario"
HDAtticPickerLabel = "En el desván"
HDInRoomPickerLabel = "En la habitación"
HDInTrashPickerLabel = "En la basura"
HDDeletePickerLabel = "¿Eliminar?"
HDInAtticLabel = "Desván"
HDInRoomLabel = "Habitación"
HDInTrashLabel = "Basura"
HDToAtticLabel = "Llevar\nal desván"
HDMoveLabel = "Mover"
HDRotateCWLabel = "Girar a la derecha"
HDRotateCCWLabel = "Girar a la izquierda"
HDReturnVerify = "¿Quieres llevar este artículo de nuevo al desván?"
HDReturnFromTrashVerify = "¿Quieres rescatar este artículo de la basura y llevarlo de nuevo al desván?"
HDDeleteItem = "Haz clic en OK para tirar este artículo a la basura o en Cancelar para no tirarlo."
HDNonDeletableItem = "No puedes deshacerte de este tipo de artículo."
HDNonDeletableBank = "No puedes deshacerte de la alcancía."
HDNonDeletableCloset = "No puedes deshacerte del clóset."
HDNonDeletablePhone = "No puedes deshacerte del teléfono."
HDNonDeletableNotOwner = "No puedes deshacerte de las cosas de %s."
HDHouseFull = "Tienes la casa llena. Antes de rescatar este artículo de la basura, tendrás que deshacerte de otra cosa de la casa o el desván."

HDHelpDict = {
    "DoneMoving" : "Acaba de decorar la habitación.",
    "Attic" : "Muestra una lista de los objetos del desván. En el desván se guardan los objetos que no están en tu habitación.",
    "Room" : "Muestra una lista de los objetos de tu habitación. Resulta práctico para encontrar objetos perdidos.",
    "Trash" : "Muestra los objetos de la basura. Los objetos más antiguos desaparecen al cabo del tiempo o cuando la basura empieza a rebosar.",
    "ZoomIn" : "Para ver la habitación desde más cerca.",
    "ZoomOut" : "Para ver la habitación desde más lejos.",
    "SendToAttic" : "Para guardar un mueble en el desván.",
    "RotateLeft" : "Para girar a la izquierda.",
    "RotateRight" : "Para girar a la derecha.",
    "DeleteEnter" : "Para cambiar al modo de eliminar.",
    "DeleteExit" : "Para salir del modo de eliminar.",
    "FurnitureItemPanelDelete" : "Para tirar %s a la basura.",
    "FurnitureItemPanelAttic" : "Para colocar %s en la habitación.",
    "FurnitureItemPanelRoom" : "Para devolver %s al desván.",
    "FurnitureItemPanelTrash" : "Para devolver %s al desván.",
    }



# don't translate yet
MessagePickerTitle = "Tienes demasiadas frases. Si quieres comprar \n\"%s\"\n debes elegir una y borrarla:"
MessagePickerCancel = lCancel
MessageConfirmDelete = "¿Seguro que quieres borrar \"%s\" del menú de SpeedChat?"


# don't translate yet
CatalogBuyText = "Comprar"
CatalogRentText = "Alquilar"
CatalogGiftText = "Regalar"
CatalogOnOrderText = "Ya pedido"
CatalogPurchasedText = "Ya comprado"
CatalogGiftedText = "Recibido\nde regalo"
CatalogPurchasedGiftText = "Ya en\npropiedad"
CatalogMailboxFull = "No hay espacio"
CatalogNotAGift = "No es un regalo"
CatalogNoFit = "No\ncabe"
CatalogMembersOnly = "¡Solo\nmiembros!"
CatalogSndOnText = "Snd Sí"
CatalogSndOffText = "Snd No"

CatalogPurchasedMaxText = "Máximo permitido\nya comprado"
CatalogVerifyPurchase = "¿Quieres comprar %(item)s por %(price)s golosinas?"
CatalogVerifyRent = "¿Alquilar %(item)s por %(price)s golosinas?"
CatalogVerifyGift = "¿Comprar %(item)s por %(price)s golosinas para hacerle un regalo a %(friend)s?"
CatalogOnlyOnePurchase = "Solo puedes tener uno de estos artículos a la vez. Si compras este, sustituirá a %(old)s.\n\n¿Seguro que quieres comprar %(item)s por %(price)s golosinas?"

# don't translate yet
CatalogExitButtonText = "Colgar"
CatalogCurrentButtonText = "Ir a artículos actuales"
CatalogPastButtonText = "Ir a artículos antiguos"

TutorialHQOfficerName = "Funcionario Enrique"

# NPCToons.py
NPCToonNames = {
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : "Tato Tutorial",
    999 : "Dibu Sastre",
    1000 : lToonHQfull,
    20001 : Flippy,

    #
    # Toontown Central
    #

    # Toontown Central Playground

    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "Billetón el banquero",
    2003 : "Pedro el maestro",
    2004 : "Calixta la modista",
    2005 : "Leopoldo el bibliotecario",
    2006 : "Dependiente Vicente",
    2011 : "Dependiente Vicenta",
    2007 : lHQOfficerM,
    2008 : lHQOfficerM,
    2009 : lHQOfficerF,
    2010 : lHQOfficerF,
    # NPCFisherman
    2012 : "Dependiente de la tienda de animales",
    2018 : "Duff..err..TIP Man",
    # NPCPetClerks
    2013 : "Dependiente Papo",
    2014 : "Dependiente Pepo",
    2015 : "Dependiente Pino",
    # NPCPartyPerson
    2016 : "Calabaza organizadora de fiestas",
    2017 : "Trini la organizadora de fiestas",

    # Silly Street
    2101 : "Bautista el dentista",
    2102 : "Lucía la policía",
    2103 : "Camaleón Atuéndez",
    2104 : lHQOfficerM,
    2105 : lHQOfficerM,
    2106 : lHQOfficerF,
    2107 : lHQOfficerF,
    2108 : "Fagucia Carasucia",
    2109 : "Burbujo Irujo",
    2110 : "Oscar Tel",
    2111 : "Agustín el bailarín",
    2112 : "Dr. Tomás",
    2113 : "El increíble Esnafro",
    2114 : "Chiquito Gallego",
    2115 : "Flexia Papírez",
    2116 : "Pepe Puños",
    2117 : "Facta Putre ",
    2118 : "Inocencio Santos",
    2119 : "Hilaria Jajá",
    2120 : "Profesor Nino",
    2121 : "Sra. Risita",
    2122 : "Orán Guto",
    2123 : "Marivi Guasona",
    2124 : "Bromi Stilla",
    2125 : "Morgan Dul",
    2126 : "Profesor Carcajada",
    2127 : "Mauro Peso",
    2128 : "Luis el Chiflado",
    2129 : "Carmelo Cotón",
    2130 : "Calambrita Ampérez",
    2131 : "Cosquilla Plumón",
    2132 : "Chucho Chúchez",
    2133 : "Dr. Rico",
    2134 : "Mónica Llada",
    2135 : "María Corremillas",
    2136 : "Dexter Nillo",
    2137 : "Mari Fe Liz",
    2138 : "Pepote Cobos",
    2139 : "Dani Dea",
    2140 : "Basilio Pescador",

    # Loopy Lane
    2201 : "Pepe el cartero",
    2202 : "Jocosa Risa",
    2203 : lHQOfficerM,
    2204 : lHQOfficerM,
    2205 : lHQOfficerF,
    2206 : lHQOfficerF,
    2207 : "Cholo Calandracas",
    2208 : "Luisillo Pegajosillo",
    2209 : "Chancho La Monda",
    2210 : "Pirulí",
    2211 : "Carca Ajada",
    2212 : "Roque Raro",
    2213 : "Pepi Bielas",
    2214 : "Pancho Quemancho",
    2215 : "Benito Latónez",
    2216 : "Noa Ynada",
    2217 : "Tiburcio Algas",
    2218 : "Mari Jo Cosa",
    2219 : "Chef Pánfilo",
    2220 : "Tancredo Cabezarroca",
    2221 : "Clovinia Dherente",
    2222 : "Corto Méchez",
    2223 : "Guasa Tomasa",
    2224 : "Sacha Muscado",
    2225 : "Jorobádez Pescador",

    # Punchline Place
    2301 : "Dr. Tronchaespinazo",
    2302 : "Profesor Cosquillas",
    2303 : "Enfermera Mondi",
    2304 : lHQOfficerM,
    2305 : lHQOfficerM,
    2306 : lHQOfficerF,
    2307 : lHQOfficerF,
    2308 : "Mullida Mullídez",
    2309 : "Desmoño Ruinez",
    2311 : "Paco Gotazo",
    2312 : "Dra. Sensible",
    2313 : "Lila Lamparón",
    2314 : "Disco Bolo",
    2315 : "Francisco Reoso",
    2316 : "Cindi Charachera",
    2318 : "Toni Chichón",
    2319 : "Zipi",
    2320 : "Alfredo Pastosi",
    2321 : "Fescor Pescador",

    #
    # Donald's Dock
    #

    # Donald's Dock Playground
    1001 : "Dependiente Pipe",
    1002 : "Dependiente Pape",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "Fifo Pretaporter",
    # NPCFisherman
    1008 : "Dependiente de la tienda de animales",
    # NPCPetClerks
    1009 : "Dependiente Guaguau",
    1010 : "Dependiente MiauMiau",
    1011 : "Dependiente Blop",
    # NPCPartyPerson
    1012 : "Tremadal el Organizador de fiestas",
    1013 : "Parti la organizadora de fiestas",

    # Barnacle Blvd.
    1101 : "Beto Buque",
    1102 : "Capitán Doblón",
    1103 : "Raspo Espínez",
    1104 : "Dr. Rompecubiertas",
    1105 : "Almirante Garfio",
    1106 : "Sra. Almidónez",
    1107 : "Nemo Mancuerna",
    1108 : lHQOfficerM,
    1109 : lHQOfficerF,
    1110 : lHQOfficerM,
    1111 : lHQOfficerF,
    1112 : "Pepe Glubglub",
    1113 : "Chiqui Quillas",
    1114 : "Magdaleno Yapican",
    1115 : "Abogada Tentácula Calamar",
    1116 : "Pili Percebe",
    1117 : "Billy Yates",
    1118 : "Nelson Tintes",
    1121 : "Lisa Mástiles",
    1122 : "Titánico Iceberg",
    1123 : "Electra Anguílez",
    1124 : "Astillo Muéllez",
    1125 : "Tunanta Estribor",
    1126 : "Bartolo Pescador",

    # Seaweed Street
    1201 : "Perci Percebe",
    1202 : "Pasma Rote",
    1203 : "Ajab",
    1204 : "Claus Anclas",
    1205 : lHQOfficerM,
    1206 : lHQOfficerF,
    1207 : lHQOfficerM,
    1208 : lHQOfficerF,
    1209 : "Profesor Curasardinas",
    1210 : "Pong Peyeng",
    1211 : "Velo Dromo",
    1212 : "Pico Tazos",
    1213 : "Rémoro Tiburcio ",
    1214 : "Catalina Timoneles",
    1215 : "María del Mar Salada",
    1216 : "Carrete Cañas",
    1217 : "Marina Naval",
    1218 : "Paco Pacífico",
    1219 : "Alvar Cabeza de Playa",
    1220 : "Isabel Segunda",
    1221 : "Blasco Sido",
    1222 : "Alberto Abordaje",
    1223 : "Sepio Calamárez",
    1224 : "Emilia Anguila",
    1225 : "Gonzo Friegacubiertas",
    1226 : "Izo Velamen",
    1227 : "Coral Bisturí",
    1228 : "Cañero Pescador",

    # Lighthouse Lane
    1301 : "Pepa Sastre",
    1302 : "Isidoro Subemástiles",
    1303 : "Clodovico Cromañón",
    1304 : "Santiaguiña Nécorez",
    1305 : lHQOfficerM,
    1306 : lHQOfficerF,
    1307 : lHQOfficerM,
    1308 : lHQOfficerF,
    1309 : "Mar Océana",
    1310 : "Trucho Cañete",
    1311 : "Goyo Gorrotocho",
    1312 : "Quillo Quilla",
    1313 : "Gordi Gordios",
    1314 : "Jorge Rumbre",
    1315 : "Catedrático Áncora",
    1316 : "Canuta Canoas",
    1317 : "Juana Salvadora Gaviota",
    1318 : "Salva Vidas",
    1319 : "Quique Diqueseco",
    1320 : "Mario Almejo",
    1321 : "Dina Atraque",
    1322 : "Estibora Pópez",
    1323 : "Pericles Cabezabuque",
    1324 : "Concha Coquínez ",
    1325 : "Vaporeto Misisipi",
    1326 : "Jurela Besúguez",
    1327 : "Gabi Ota",
    1328 : "Carlitos Lenguado",
    1329 : "Flora Marínez",
    1330 : "Fredo Barbarrala",
    1331 : "Timón Bocanegra",
    1332 : "Samuel Pescador",

    #
    # The Brrrgh
    #

    # The Brrrgh Playground
    3001 : "Adela Dita",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "Dependiente Poli",
    3007 : "Dependiente Pili",
    3008 : "Giorgio Armiño",
    # NPCFisherman
    3009 : "Dependiente de la tienda de animales",
    # NPCPetClerks
    3010 : "Dependiente Tito",
    3011 : "Dependiente Tuto",
    3012 : "Dependiente Tato",
    # NPCPartyPerson
    3013 : "Pedro el organizador de fiestas",
    3014 : "Pedra la organizadora de fiestas",

    # Walrus Way
    3101 : "Juanjo Escárchez",
    3102 : "Tía Ritona",
    3103 : "Pepe Tundra",
    3104 : "Geli da Pinto",
    3105 : "Pipe Pelado",
    3106 : "Fríguez Sabañón",
    3107 : "Maite Aterida",
    3108 : "Doroteo Escarcha",
    3109 : "Pati",
    3110 : "Lucas Friolero",
    3111 : "Kevin Kelvin",
    3112 : "Fredo Dedo",
    3113 : "Cris Térico",
    3114 : "Beto Tomba",
    3115 : lHQOfficerM,
    3116 : lHQOfficerF,
    3117 : lHQOfficerM,
    3118 : lHQOfficerM,
    3119 : "Carlos Congelado",
    3120 : "Mito Mitón",
    3121 : "Voltio Ampérez",
    3122 : "Bebé Bob",
    3123 : "Ricardo Bofrigo",
    3124 : "Manfredo Carámbanez",
    3125 : "Tiritono Quelog",
    3126 : "Pescanovo Martínez",
    3127 : "Popoco Mecaigo",
    3128 : "Pipo Polar",
    3129 : "Dina Fríomiga",
    3130 : "Roberta",
    3131 : "Lorenzo Rascafría",
    3132 : "Cenicilla",
    3133 : "Dr. Congelaimagen",
    3134 : "Paco Gelado",
    3135 : "Empa Pada",
    3136 : "Felicia Simpática",
    3137 : "Kevin Ator",
    3138 : "Chef Sopacarámbano ",
    3139 : "Abuelita Polosur",
    3140 : "Lucilia Pescador",

    # Sleet Street
    3201 : "Tía Ártica",
    3202 : "Antonio Tiritonio",
    3203 : "Eugenio Criogenio",
    3204 : "Dra. Soplillos",
    3205 : "Perico Arenque",
    3206 : "Fernando Anchoa",
    3207 : "Dr. Bocamaraca",
    3208 : "Felipe el gruñón",
    3209 : "Garmillo Panterquircho",
    3210 : "Nutrio Cenutrio",
    3211 : "Pega Pegón",
    3212 : "Federico Gelado",
    3213 : lHQOfficerM,
    3214 : lHQOfficerF,
    3215 : lHQOfficerM,
    3216 : lHQOfficerM,
    3217 : "Pedro Glaciares",
    3218 : "Pepe Napiazul",
    3219 : "Tomás Bufandilla",
    3220 : "Estornio Atchís",
    3221 : "Inés Carcha",
    3222 : "Ventiscona Copogordo",
    3223 : "Macario Ajillo",
    3224 : "Madame Glacé",
    3225 : "Gregorio Sabañón ",
    3226 : "Papá Noés",
    3227 : "Solario Ráyez",
    3228 : "Escalo Frío",
    3229 : "Hernia Tarúguez",
    3230 : "Optimisto Peláez ",
    3231 : "Pedro Picahielo",
    3232 : "Alberto Pescador",

    # Polar Place
    3301 : "Parchesa Cachemira",
    3302 : "Conge Ladito",
    3303 : "Dr. Muñón",
    3304 : "Eduardo el Yeti",
    3305 : "Emilio Bilio",
    3306 : "Paula Iglulas",
    # NPC Fisherman
    3307 : "Federica Pescador",
    3308 : "Espantajo Donaldo",
    3309 : "Piperín",
    3310 : "Profesor Copos",
    3311 : "Carla Ferrán",
    3312 : "Juan Marzo",
    3313 : lHQOfficerM,
    3314 : lHQOfficerF,
    3315 : lHQOfficerM,
    3316 : lHQOfficerF,
    3317 : "Besina Besón",
    3318 : "Juanito Cachemir",
    3319 : "Mateo Reo",
    3320 : "Luisa Brisa",
    3321 : "Pablo Hachazo",
    3322 : "Pili Broviejo",
    3323 : "Dallas Borealis",
    3324 : "Esteban Colibre",
    3325 : "Fiestona Casona",
    3326 : "Blanch",
    3327 : "Marco Milona",
    3328 : "Sandra Sabores",
    3329 : "Eusebio Talón",

    #
    # Minnie's Melody Land
    #

    # Minnie's Melody Land Playground
    4001 : "Moli Melódica",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "Dependiente Dina",
    4007 : "Dependiente Dino",
    4008 : "Modista Armonía",
    # NPCFisherman
    4009 : "Dependiente de la tienda de animales",
    # NPCPetClerks
    4010 : "Dependiente Cristian",
    4011 : "Dependiente Nacho",
    4012 : "Dependiente Romualda",
    # NPCPartyPerson
    4013 : "Ignacio el organizador de fiestas",
    4014 : "Penélope la organizadora de fiestas",

    # Alto Ave.
    4101 : "Ropo Pompom",
    4102 : "Bibi",
    4103 : "Dr. Pavo Rotti",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "Sordino Quena",
    4109 : "Carlos",
    4110 : "Metrónoma Diapasón",
    4111 : "Camilo Séptimo",
    4112 : "Fa",
    4113 : "Madame Modales",
    4114 : "Dum Dúmez",
    4115 : "Bárbara Sevilla",
    4116 : "Pizzicato",
    4117 : "Lina Mando",
    4118 : "Rapsodio Sonata",
    4119 : "Beto Ven",
    4120 : "Tara Reo",
    4121 : "Bemolio Sostenido",
    4122 : "Noa Ybemoles",
    4123 : "Cornetín Gaita",
    4124 : "Rifi Rafe",
    4125 : "Notas Peinao",
    4126 : "Tortillo Tenorio",
    4127 : "Vivaracho Vivaldi",
    4128 : "Plácido Lunes",
    4129 : "Fina Desafinada",
    4130 : "Ironio Máidez",
    4131 : "Abraham Zambomba",
    4132 : "Teresa Benicanta",
    4133 : "Impo Luto",
    4134 : "DJ Diborio",
    4135 : "Teresito Sopranillo",
    4136 : "Fusa Patidifusa",
    4137 : "Rafael Sostenido",
    4138 : "Octavo Seisillo",
    4139 : "Ada Gio",
    4140 : "Trémolo Torpe",
    4141 : "Juanito Pescador",

    # Baritone Blvd.
    4201 : "Tina Sonatina",
    4202 : "Barbo",
    4203 : "Chopo Chopín",
    4204 : lHQOfficerM,
    4205 : lHQOfficerF,
    4206 : lHQOfficerF,
    4207 : lHQOfficerF,
    4208 : "Lírica Tástrofe",
    4209 : "Sissy Samba",
    4211 : "José Carrerilla",
    4212 : "Filarmonio Opereto",
    4213 : "Ambulancio Raudo",
    4214 : "Arnesia Mifasol",
    4215 : "Corneto Claxon",
    4216 : "Amadeo Parche",
    4217 : "Juan Strauss",
    4218 : "Octava Pianola",
    4219 : "Trombón Charango",
    4220 : "Sartenio Batuta",
    4221 : "Pipo Madrigal",
    4222 : "Fulano de Tal",
    4223 : "Felisa Obelisco",
    4224 : "Jonás Clarinete",
    4225 : "Cuchi Cheo",
    4226 : "Paca Canora",
    4227 : "Betina Trompetilla",
    4228 : "Nabuco Donosor",
    4229 : "Melodia Pasón",
    4230 : "Rigo Letto",
    4231 : "Acordia Deona",
    4232 : "Fígaro Casamentero",
    4233 : "Arpo Marx",
    4234 : "Coro Vocález",
    4235 : "Lorenzo Pescador",

    # Tenor Terrace
    4301 : "Uki",
    4302 : "Juanola",
    4303 : "Leo",
    4304 : lHQOfficerM,
    4305 : lHQOfficerF,
    4306 : lHQOfficerF,
    4307 : lHQOfficerF,
    4308 : "Felisa Felina",
    4309 : "Isidoro Tápiez",
    4310 : "Marta Falla",
    4311 : "Corneta Camarera",
    4312 : "Horacio Pianola",
    4313 : "Renato Enquequedamos",
    4314 : "Vilma Mascota",
    4315 : "Rola Roles",
    4316 : "Pachi Zapatillo",
    4317 : "Piero Pereta",
    4318 : "Bob Marlene",
    4319 : "Urraca Grájez",
    4320 : "Irene Fervescente",
    4321 : "Pepe Palmira",
    4322 : "Aitor Poloneso",
    4323 : "Ana Balada",
    4324 : "Elisa",
    4325 : "Banquero Ramón",
    4326 : "Morlana Chicharra",
    4327 : "Flautilla Hamelín",
    4328 : "Wagner",
    4329 : "Maruja Televenta",
    4330 : "Maestro Soniquete",
    4331 : "Celo Costelo",
    4332 : "Tato Timbal",
    4333 : "Chiflo Chiflete",
    4334 : "Maraco Marchoso",
    4335 : "Gualdo Pescador",

    #
    # Daisy Gardens
    #

    # Daisy Gardens Playground
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "Dependiente Azucena",
    5006 : "Dependiente Jacinto",
    5007 : "Florinda Rosales",
    # NPCFisherman
    5008 : "Dependiente de la tienda de animales",
    # NPCPetClerks
    5009 : "Dependiente Botánica",
    5010 : "Dependiente Tomás Ablanda",
    5011 : "Dependiente Tomás Adura",
    # NPCPartyPerson
    5012 : "Ramón el organizador de fiestas",
    5013 : "Felisa la organizadora de fiestas",

    # Elm Street
    5101 : "Pepe Pino",
    5102 : "Alca Chofa",
    5103 : "Federico Tilla",
    5104 : "Polillo Maripósez",
    5105 : "Comino Pérez Gil",
    5106 : "Patillo Siegacogotes",
    5107 : "Cartero Felipe",
    5108 : "Posadera Piti",
    5109 : lHQOfficerM,
    5110 : lHQOfficerM,
    5111 : lHQOfficerF,
    5112 : lHQOfficerF,
    5113 : "Dr. Zanahorio",
    5114 : "Marchito Mate",
    5115 : "Mimosa Nomeolvides",
    5116 : "Lucho Borrajo",
    5117 : "Pétalo",
    5118 : "Palomo Maíz",
    5119 : "Seto Podal",
    5120 : "Cardamomo",
    5121 : "Grosella Falsa",
    5122 : "Trufo Champiñón",
    5123 : "Tempranilla Móstez",
    5124 : "Hinojo Hinault",
    5125 : "Burbujo Chof",
    5126 : "Madre Selva",
    5127 : "Pili Polen",
    5128 : "Barba Coa",
    5129 : "Sabina Pescador",

    # Maple Street
    5201 : "Pulgarcillo",
    5202 : "Edel Weiss",
    5203 : "Campanilla",
    5204 : "Pipe Barroso",
    5205 : "León Mondadientes",
    5206 : "Cardo Borriquero",
    5207 : "Flor Chorro",
    5208 : "Lisa Buesa",
    5209 : lHQOfficerM,
    5210 : lHQOfficerM,
    5211 : lHQOfficerF,
    5212 : lHQOfficerF,
    5213 : "Al Cornoque",
    5214 : "Hortensia Comopincha",
    5215 : "Josefa Repera",
    5216 : "Luisillo Membrillo",
    5217 : "Aníbal Nomeolvides",
    5218 : "Rufo Segadora",
    5219 : "Sacha Cachas",
    5220 : "Lenti Juela",
    5221 : "Flamenca Rosa",
    5222 : "Belladona Jazmín",
    5223 : "Frido Quememojo",
    5224 : "Guido Castañapilonga",
    5225 : "Pipa Girasólez",
    5226 : "Rumio Cuentauvas",
    5227 : "Petunia Barricarroble",
    5228 : "Prior Primo Prelado",
    5229 : "Lirio Pescador",

    # Oak street
    5301 : lHQOfficerM,
    5302 : lHQOfficerM,
    5303 : lHQOfficerM,
    5304 : lHQOfficerM,
    5305 : "Doña Hortensia",
    5306 : "Cartero don Lentejo",
    5307 : "Cris Antemo",
    5308 : "Juanita Pimentón",
    5309 : "Marga y Rita",
    5310 : "Narciso",
    5311 : "Doña Zanahoria",
    5312 : "Eugenio",
    5313 : "Don Silvestre",
    5314 : "Tía Petunia",
    5315 : "Tío Calabacín",
    5316 : "Tío Jacinto",
    5317 : "Doña Citronia",
    5318 : "Don Lirio",
    5319 : "Malva Rosa",
    5320 : "Doña Azucena",
    5321 : "Profesor Hiedra",
    5322 : "Rosa Pescador",

    #
    # Goofy's Speedway
    #
    
    #default  area
    #kart clerk
    8001 : "Enrique Motores",
    8002 : "Ivón Carreras",
    8003 : "Victoria Repetidez",
    8004 : "Fabio Gas",
   
    #
    # Dreamland
    #
    
    # Dreamland Playground
    9001 : "Belinda Traspuesta",
    9002 : "Bello Durmiente",
    9003 : "Plancho Rejas",
    9004 : lHQOfficerF,
    9005 : lHQOfficerF,
    9006 : lHQOfficerM,
    9007 : lHQOfficerM,
    9008 : "Dependiente Modorra",
    9009 : "Dependiente Modorro",
    9010 : "Almohado Edredón",
    # NPCFisherman
    9011 : "Dependiente de la tienda de animales",
    # NPCPetClerks
    9012 : "Dependiente Sasasueños",
    9013 : "Dependiente Sista Siesta",
    9014 : "Dependiente Sisto Siesto",
    # NPCPartyPerson
    9015 : "Paco el organizador de fiestas",
    9016 : "Diamante la organizadora de fiestas",

    # Lullaby Lane
    9101 : "Vito",
    9102 : "Plúmbea Triz",
    9103 : "Cafeíno Paloseco ",
    9104 : "Copito de Nieve",
    9105 : "Profesor Bostezo",
    9106 : "Soporífero Indolente",
    9107 : "Acurruco Paloma",
    9108 : "Soño Liento",
    9109 : "Dafne Marmota",
    9110 : "Adela Duermevela",
    9111 : "Apagona Plómez",
    9112 : "Marqués de la Nana",
    9113 : "Jaime Cuco",
    9114 : "Máscara Pepínez",
    9115 : "Hiberno Cuandoquiero",
    9116 : "Mariano Cuentaovejas",
    9117 : "Madrugona Grogui",
    9118 : "Estrella Vespertina",
    9119 : "Tronco Sópez",
    9120 : "Lirona Frita",
    9121 : "Serena Vigilia",
    9122 : "Trasnocho Pocho",
    9123 : "Osito Pelúchez",
    9124 : "Vela Zascandil",
    9125 : "Dr. Vigíliez",
    9126 : "Pluma Oca",
    9127 : "Pili Piltra",
    9128 : "Juanjo Manitas",
    9129 : "Beltrán Puesto",
    9130 : "Siesto Buenasnóchez",
    9131 : "Letárgica Catorcehoras",
    9132 : lHQOfficerF,
    9133 : lHQOfficerF,
    9134 : lHQOfficerF,
    9135 : lHQOfficerF,
    9136 : "Pablo Pescador",

    # Pajama Place
    9201 : "Bernat",
    9202 : "Oniro",
    9203 : "Nat",
    9204 : "Clara de Luna",
    9205 : "Zen Ben",
    9206 : "Domi Lona",
    9207 : "Juana Pijama",
    9208 : "David Modorra",
    9209 : "Dr. Seda",
    9210 : "Maestro Marcos",
    9211 : "Amanecer",
    9212 : "Rayo de luna",
    9213 : "Ricardo Gallón",
    9214 : "Dr. Legañas",
    9215 : "Ripón",
    9216 : "Cato",
    9217 : "Linda Legal",
    9218 : "Matilda Vals",
    9219 : "La condesa",
    9220 : "Fabián Gruñón",
    9221 : "Zari",
    9222 : "Cowboy Jorge",
    9223 : "Ramón el Guasón",
    9224 : "Sandra Salamandra",
    9225 : "Martina Cocina",
    9226 : "Mostra Dor",
    9227 : "Teterín Soporín",
    9228 : "Sauce Susurros",
    9229 : "Rosa Pétalo",
    9230 : "Tex",
    9231 : "Harry Hamaca",
    9232 : "Luna Miel",
    9233 : lHQOfficerM,
    9234 : lHQOfficerM,
    9235 : lHQOfficerM,
    9236 : lHQOfficerM,
    9237 : "Patricio Pescador",

    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# These building titles are output from the DNA files
# Run ppython $TOONTOWN/src/dna/DNAPrintTitles.py to generate this list
# DO NOT EDIT THE ENTRIES HERE -- EDIT THE ORIGINAL DNA FILE
zone2TitleDict = {
    # titles for: phase_4/dna/toontown_central_sz.dna
    2513 : ("Ayuntamiento", "el"),
    2514 : ("Banco de Toontown", "el"),
    2516 : ("Colegio de Toontown", "el"),
    2518 : ("Biblioteca de Toontown", "la"),
    2519 : ("Tienda de Bromas", "la"),
    2520 : ("Cuartel general", "el"),
    2521 : ("Tienda de Ropa de Toontown", "la"),
    2522 : ("Tienda de animales", "la"),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("Clínica Dental Piñatasana", "la"),
    2602 : ("", ""),
    2603 : ("Mineros Carboneros", "los"),
    2604 : ("Limpiezas por Piezas", "las"),
    2605 : ("Fábrica de Carteles de Toontown", "la"),
    2606 : ("", ""),
    2607 : ("Habas Saltarinas", "las"),
    2610 : ("Dr. Tomás Todonte", "el"),
    2611 : ("", ""),
    2616 : ("Tienda de Disfraces Barbarrara", "la"),
    2617 : ("Acrobacias a Granel", "las"),
    2618 : ("Chistes Lepetitivos", "los"),
    2621 : ("Aviones de Papel", "los"),
    2624 : ("Perros Gamberros", "los"),
    2625 : ("Pastelería Moho Feliz", "la"),
    2626 : ("Reparación de Bromas", "las"),
    2629 : ("El Rincón de la Risa", "el"),
    2632 : ("Academia de Payasos", "la"),
    2633 : ("Salón de Té La Tetera", "el"),
    2638 : ("Willie, el Barco de Vapor", ""),
    2639 : ("Travesuras Simiescas", "las"),
    2643 : ("Botellas Enlatadas", "las"),
    2644 : ("Bromas Ligeras", "las"),
    2649 : ("Tienda de Juegos", "la"),
    2652 : ("", ""),
    2653 : ("", ""),
    2654 : ("Clases de Reír", "las"),
    2655 : ("Caja de Ahorros Dine Rodríguez", "la"),
    2656 : ("Autos Usados de Payasos", "los"),
    2657 : ("Bromas a Tutiplén", "las"),
    2659 : ("Calambres Reunidos Ampérez", "los"),
    2660 : ("Cosquilladores Automáticos", "los"),
    2661 : ("Chuches Chucho", ""),
    2662 : ("Dr. Eufo Rico", "el"),
    2663 : ("Don Ratón Se Va De Vacaciones", ""),
    2664 : ("Mimos Mimosos", "los"),
    2665 : ("Agencia de Viajes Corremillas", "la"),
    2666 : ("Gasolinera Desternillante", "la"),
    2667 : ("Tiempos Felices", "los"),
    2669 : ("Globos Cobos", "los"),
    2670 : ("Tenedores de Sopa", "los"),
    2671 : ("Cuartel general", "el"),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("Un Marinerito Valiente", ""),
    2705 : ("Matracas Calandracas", "las"),
    2708 : ("Cola Azul", "la"),
    2711 : ("Oficina de Correos de Toontown", "la"),
    2712 : ("Café La Monda", "el"),
    2713 : ("Café Chachi", "el"),
    2714 : ("Un Tranvía En Apuros", ""),
    2716 : ("Calditos Carcajada", "los"),
    2717 : ("Latas Embotelladas", "las"),
    2720 : ("Taller Despilporre", "el"),
    2725 : ("", ""),
    2727 : ("Botellas y Latas Latónez", "las"),
    2728 : ("Nata Invisible", "la"),
    2729 : ("Peces Dorados, 14", "los"),
    2730 : ("Noticias Jocosas", "las"),
    2731 : ("", ""),
    2732 : ("Pasta Pánfilo", "la"),
    2733 : ("Cometas de Plomo", "los"),
    2734 : ("Platillos y Ventosas", "los"),
    2735 : ("Detonaciones a Domicilio", "las"),
    2739 : ("Reparación de Chistes", "las"),
    2740 : ("Petardos Usados", "los"),
    2741 : ("", ""),
    2742 : ("Cuartel general", "el"),
    2743 : ("Limpieza En Seco En Un Minueto", "la"),
    2744 : ("", ""),
    2747 : ("Tinta Visible", "la"),
    2748 : ("Risa Deprisa", "la"),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("Cojines Mullídez", "los"),
    2802 : ("Bolas de Demolición Inflables", "las"),
    2803 : ("El Chico Del Carnaval", ""),
    2804 : ("Clínica de Fisioterapia Tronchalomo", "la"),
    2805 : ("", ""),
    2809 : ("Gimnasio Capirotazo", "el"),
    2814 : ("Un Día De Atasco", ""),
    2818 : ("Tartas Volantes", "las"),
    2821 : ("", ""),
    2822 : ("Sándwiches de Pollo de Goma", "los"),
    2823 : ("Heladería El Cucurucho Agudo", "la"),
    2824 : ("Las Locuras De %s" % Mickey, ""),
    2829 : ("Salchichones y Chichones", "los"),
    2830 : ("Melodías de Zipi", "las"),
    2831 : ("Casa de las Risillas del Profesor Cosquillas", "la"),
    2832 : ("Cuartel general", "el"),
    2833 : ("", ""),
    2834 : ("Sala de Traumatología del Hueso de la Risa", "la"),
    2836 : ("", ""),
    2837 : ("Seminarios Sobre Risa Persistente", "los"),
    2839 : ("Pasta Pastosa", "la"),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : ("Tienda de Bromas", "la"),
    1507 : ("Cuartel general", "el"),
    1508 : ("Tienda de Ropa", "la"),
    1510 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("Flotadores Usados", "los"),
    1604 : ("Limpieza en Seco de Ropa Chorreantes", "la"),
    1606 : ("Relojería Garfio", "la"),
    1608 : ("Quillas y Cosquillas", "las"),
    1609 : ("Echa el Cebo Magdaleno", ""),
    1612 : ("Banco Galeón Hundido", "el"),
    1613 : ("Bufete Calamar, Pulpo & Sepia", "el"),
    1614 : ("Boutique Uña Deslumbrante", "la"),
    1615 : ("Yates Todo a cien", "el"),
    1616 : ("Salón de Belleza Barbanegra", "el"),
    1617 : ("Óptica El Vigía Miope", "la"),
    1619 : ("Clínica Quirúrgica de Arboles", "la"),
    1620 : ("De Popa a Proa", ""),
    1621 : ("Gimnasio Estibadores Fornidos", "el"),
    1622 : ("Accesorios Eléctricos Rayas y Centollos", "los"),
    1624 : ("Reparación de Suelas de Buque", "la"),
    1626 : ("Ropa de etiqueta El Salmón Coqueto", "la"),
    1627 : ("Surtido de Bitácoras de Beto Buque", "el"),
    1628 : ("Atún de la Tuna", "el"),
    1629 : ("Cuartel general", "el"),
    # titles for: phase_6/dna/donalds_dock_1200.dna
    1701 : ("Escuela de Enfermería La Boya Pocha", "la"),
    1703 : ("Restaurante Chino Cocochas de Dragón", "el"),
    1705 : ("Velas y Bielas", "las"),
    1706 : ("Medusas para Bañeras", "las"),
    1707 : ("Regalos Tiburcio", "los"),
    1709 : ("Cata de Maranes", "la"),
    1710 : ("Surtido de Percebes", "el"),
    1711 : ("Restaurante Sal Gorda", "el"),
    1712 : ("Gimnasio Levad Anclas", "el"),
    1713 : ("Mapas Pasma", "las"),
    1714 : ("Posada Suelta el Carrete", "la"),
    1716 : ("Bañadores La Sirena con Piernas", "las"),
    1717 : ("Telas y Botones Océano Pacífico", "las"),
    1718 : ("Servicio de Taxi Callo Encallado", "el"),
    1719 : ("Compañía de Aguas Lomo de Pato", "la"),
    1720 : ("Cañas y Barro", "las"),
    1721 : ("A Toda Máquina", ""),
    1723 : ("Algas Sepio", "las"),
    1724 : ("Anguilas Gustativas", "las"),
    1725 : ("Cangrejos y Aparejos Ajab", "los"),
    1726 : ("Con Cien Gaseosas por Banda", ""),
    1727 : ("Los Remos del Volga", ""),
    1728 : ("Centollos El Meollo", "los"),
    1729 : ("Cuartel general", "el"),
    # titles for: phase_6/dna/donalds_dock_1300.dna
    1802 : ("Náutico y Aséptico", "el"),
    1804 : ("Gimnasio El Crustáceo Cachas", "el"),
    1805 : ("Comidas El Carrete Audaz", "las"),
    1806 : ("Sombrerería Gorrotocho", "la"),
    1807 : ("Quillas al Pil Pil", "las"),
    1808 : ("Nudos Imposibles", "los"),
    1809 : ("Cubos Oxidados", "los"),
    1810 : ("Máster en Gestión de Anclas", "el"),
    1811 : ("Canoas y Anchoas", "las"),
    1813 : ("Asesoría Vuela más Alto", "la"),
    1814 : ("Apeadero Amarras Salvajes", "el"),
    1815 : ("Consulta del Dr. Diqueseco", "la"),
    1818 : ("Cafetería Los Siete Mares", "la"),
    1819 : ("El Estibador Gourmet", ""),
    1820 : ("Artículos de Broma El Simpático Maremoto", "los"),
    1821 : ("Fábrica de Conservas dibuque", "la"),
    1823 : ("Restaurante El Molusco Feroz", "el"),
    1824 : ("Paletas y Maletas", "las"),
    1825 : ("Caballas Pura Sangre Pescadería", "las"),
    1826 : ("Sastrería Cromañón", "la"),
    1828 : ("Lastre Pepa Sastre", "el"),
    1829 : ("Estatuas de Gaviotas", "las"),
    1830 : ("Objetos Náuticos Perdidos", "los"),
    1831 : ("Algas de Compañía", "las"),
    1832 : ("Surtido de Mástiles", "el"),
    1833 : ("Trajes a Medida El Corsario Elegante", "los"),
    1834 : ("Timones de diseño", "los"),
    1835 : ("Cuartel general", "el"),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : ("Tienda de Bromas", "la"),
    4504 : ("Cuartel general", "el"),
    4506 : ("Tienda de Ropa de Toontown", "la"),
    4508 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Tambores Ropopompom", "los"),
    4604 : ("Compás de Dos por Cuatro", "el"),
    4605 : ("Violines Bibi", "los"),
    4606 : ("Casa de las Castañuelas", "la"),
    4607 : ("Dibumoda Septiminod", "la"),
    4609 : ("Teclas de Piano Dorremí", "las"),
    4610 : ("No Pierdan los Estribillos", ""),
    4611 : ("A Bombo y Platillos Voladores", ""),
    4612 : ("Clínica Dental Rotti", "la"),
    4614 : ("Peluquería de Corcheas", "la"),
    4615 : ("Pizzería Pizzicato", "la"),
    4617 : ("Mandolinas Mandonas", "las"),
    4618 : ("Cuartos para Cuartetos", "los"),
    4619 : ("Pentagramas a la Carta", "los"),
    4622 : ("Almohadas Acompasadas", "las"),
    4623 : ("Bemoles a Cien", "los"),
    4625 : ("Tuba de Pasta de Dientes", "la"),
    4626 : ("Solfeo a Granel", ""),
    4628 : ("Seguros a Tercetos", "los"),
    4629 : ("Platillos de Papel", "los"),
    4630 : ("Tocata y Fuga de Alcatraz", "la"),
    4631 : ("Tocatas de Tortilla", "las"),
    4632 : ("Tienda Abierta los 24 Tiempos", "la"),
    4635 : ("Tenores de Alquiler", "los"),
    4637 : ("Afinado de Platillos", "el"),
    4638 : ("Cuartetos de Heavy Metal", "los"),
    4639 : ("Antigüedades La Flauta de Noé", "las"),
    4641 : ("Noticiero La Voz de la Soprano", "el"),
    4642 : ("Limpieza en Seco en un Minueto", "la"),
    4645 : ("Dibudisco", "el"),
    4646 : ("", ""),
    4648 : ("Mudanzas Berganza", "las"),
    4649 : ("", ""),
    4652 : ("Regalos Clave de Luna", "los"),
    4653 : ("", ""),
    4654 : ("Puertas Tannhäuser", "las"),
    4655 : ("Escuela de Cocina Sonata a la Sal", "la"),
    4656 : ("", ""),
    4657 : ("Barbería El Cuarteto Afeitador", "la"),
    4658 : ("Pianos en Caída Libre", "los"),
    4659 : ("Cuartel general", "el"),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("Escuela de Baile El Pasodoble Zapateado", "la"),
    4702 : ("¡Más Madera! Leñadores Melódicos", ""),
    4703 : ("Tenor al por Menor", "el"),
    4704 : ("Sonatas y Sonatinas", "las"),
    4705 : ("Cítaras al Peso", "las"),
    4707 : ("Estudio de Efectos Doppler", "el"),
    4709 : ("Escala Escalada Aparejos de Escalada", "la"),
    4710 : ("Escuela de Conducción Marcha y Contrafuga", "la"),
    4712 : ("Reparación de Pinchazos de Oboes", "la"),
    4713 : ("Vaqueros Strauss", "los"),
    4716 : ("Armónicas Polifónicas", "las"),
    4717 : ("Seguros de Auto Un Acordeón en la Guantera", "los"),
    4718 : ("Utensilios de Cocina Cascanueces", "los"),
    4719 : ("Caravanas Madrigal", "las"),
    4720 : ("Tararea esa dibucanción", "la"),
    4722 : ("Oberturas para Oboe", "las"),
    4723 : ("Juguetería El Xilófono de Plastilina", "la"),
    4724 : ("Cacofonías a Domicilio", "las"),
    4725 : ("El Barbero Barítono", ""),
    4727 : ("Planchado de Cuerdas Vocales", "el"),
    4728 : ("Ablandamiento de Oídos Duros", "el"),
    4729 : ("Librería El Violoncelo Celoso", "la"),
    4730 : ("Letras Patéticas", "las"),
    4731 : ("Melodibus", "los"),
    4732 : ("Compañía de Teatro El Flautín de Venecia", "la"),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("Acordeones para Amenizar Reuniones", "las"),
    4736 : ("Bodas Fígaro", "las"),
    4737 : ("Arpas de Esparto", "las"),
    4738 : ("Regalos La Balalaica Silvestre", "los"),
    4739 : ("Cuartel general", "el"),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("Organillos en Estéreo", "los"),
    4803 : ("Floristería El Sombrero de Tres Ficus", "la"),
    4804 : ("Escuela de Hostelería El Platillo Danzarín", "la"),
    4807 : ("Trémolos Embotellados", "los"),
    4809 : ("Allegros Tristes", "los"),
    4812 : ("", ""),
    4817 : ("Pajarería Pedro y el Lobo", "la"),
    4819 : ("Ukeleles de Uki", "los"),
    4820 : ("", ""),
    4821 : ("Gramolas Juanola", "las"),
    4827 : ("Relojería La Danza de las Horas", "la"),
    4828 : ("Zapatería Masculina Claqué para Ciempies", "la"),
    4829 : ("Cañones Pachelbel", "los"),
    4835 : ("Cascabeles para Gatos", "los"),
    4836 : ("Regalos Reggae", "los"),
    4838 : ("Academia de Canto Grájez", "la"),
    4840 : ("Bebidas Musicales Cocapiano Cola", "las"),
    4841 : ("Liras Palmira", "las"),
    4842 : ("Síncopas Hechas a Mano", "las"),
    4843 : ("", ""),
    4844 : ("Motocicletas Harley Mendelson", "las"),
    4845 : ("Elegías Elegantes de Elisa", "las"),
    4848 : ("Caja de ahorros Guita Ramón", "la"),
    4849 : ("", ""),
    4850 : ("Empeños La Cuerda Prestada", "los"),
    4852 : ("Fundas para Flautas", "las"),
    4853 : ("Guitarras a Vapor Leo", "las"),
    4854 : ("Vídeos de Valquirias y Violines", "los"),
    4855 : ("Címbalos a Domicilio", "los"),
    4856 : ("", ""),
    4862 : ("Pasodobles, Pasotriples y Pasocuádruples", "los"),
    4867 : ("Liquidación de Violoncelos", "la"),
    4868 : ("", ""),
    4870 : ("Timbales y Tambores de Titanio", "los"),
    4871 : ("Clarines, Clarinetes y Chifletes", "los"),
    4872 : ("Marimbas, Matracas y Maracas", "las"),
    4873 : ("Cuartel general", "el"),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : ("Tienda de Bromas", "la"),
    5502 : ("Cuartel general", "el"),
    5503 : ("Tienda de Ropa", "la"),
    5505 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5100.dna
    5601 : ("Óptica Zanahoria a Tutiplén", "la"),
    5602 : ("Corbatas Pino", "las"),
    5603 : ("Lechuga a Granel", "la"),
    5604 : ("Listas de Bodas Nomeolvides", "las"),
    5605 : ("Compañía de Aguas de Borrajas", "la"),
    5606 : ("Pétalos", "los"),
    5607 : ("Correos Florestales", "los"),
    5608 : ("Palomitas y Palomitos de Maíz", "las"),
    5609 : ("Enredaderas de Compañía", "las"),
    5610 : ("Betunes El Tulipán Negro", "los"),
    5611 : ("Bromas Cardamomo", "las"),
    5613 : ("Peluqueros Siegacogotes", "los"),
    5615 : ("Semillas con Coronilla", "las"),
    5616 : ("Posada Coli Flor de Pitiminí", "la"),
    5617 : ("Mariposas de Encargo", "las"),
    5618 : ("Guisantes Farsantes", "los"),
    5619 : ("Comino Importante", "el"),
    5620 : ("Hierbabuenas Tardes", "las"),
    5621 : ("Viñas Lejanas", "las"),
    5622 : ("Bicicletas Hinojo Hinault", "las"),
    5623 : ("Jacuzzis para Gorriones", "los"),
    5624 : ("Madreselva Tropical", "la"),
    5625 : ("Pañales para Panales", "los"),
    5626 : ("Zarzaparrillas de Carbón", "las"),
    5627 : ("Cuartel general", "el"),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Espinacas de Diseño", "las"),
    5702 : ("Rastrillos Miga de Pan", "los"),
    5703 : ("Fotografía La Flor de un Día", "la"),
    5704 : ("Autos Usados Campanita", "los"),
    5705 : ("Colchones Suavecáctus", "los"),
    5706 : ("Joyería La Pulsera de Chopo", "la"),
    5707 : ("Fruta Musical", "la"),
    5708 : ("Agencia de Viajes Villadiego", "la"),
    5709 : ("Cortacésped Amor de Hortelano", "el"),
    5710 : ("Gimnasio Espantalobos", "el"),
    5711 : ("Calcetería Lentejuela Guisada", "la"),
    5712 : ("Estatuas Bobas", "las"),
    5713 : ("Jabones de Higo Chumbo", "los"),
    5714 : ("Agua de Lluvia Embotellada", "el"),
    5715 : ("Noticiario Telecastaña", "el"),
    5716 : ("Caja de Ahorros y Monte de Orégano", "la"),
    5717 : ("La Flor Chorreante", ""),
    5718 : ("Animales Exóticos Diente de León", "los"),
    5719 : ("Agencia de Detectives Azotalenguas", "la"),
    5720 : ("Ropa Masculina Borriquero", "la"),
    5721 : ("Comidas Alfalfa Romeo", "las"),
    5725 : ("Destilería Malta Cibelina", "la"),
    5726 : ("Barro a Granel", "el"),
    5727 : ("Préstamos y Empréstitos Praderas Primitivas", "los"),
    5728 : ("Cuartel general", "el"),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : ("Cuartel general", ""),
    5804 : ("Jarrones Porrones", ""),
    5805 : ("Correo Caracol", ""),
    5809 : ("Escuela de Payasos Champi", ""),
    5810 : ("Rocío la Miel", ""),
    5811 : ("Posada Lechuga", ""),
    5815 : ("Raíces de Césped", ""),
    5817 : ("Manzanas y Naranjas", ""),
    5819 : ("Tejanos Hermanos", ""),
    5821 : ("Gimnasio Tira y Afloja", ""),
    5826 : ("Suministros Granjeros la Hormiga", ""),
    5827 : ("Baratijas Pijas", ""),
    5828 : ("Muebles el Comodín", ""),
    5830 : ("Judías Pintas", ""),
    5833 : ("El Bar Verde", ""),
    5835 : ("Hostal YCual", ""),
    5836 : ("Duchas y Baños los Caños", ""),
    5837 : ("Escuela de Parra y Jarra", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Biblioteca Sabetotal", "la"),
    9503 : ("Bar La Cabezadita Tonta", "el"),
    9504 : ("Tienda de Bromas", "la"),
    9505 : ("Cuartel general", "el"),
    9506 : ("Tienda de Ropa de Toontown", "la"),
    9508 : ("", ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Posada Pluma de Ganso", "la"),
    9602 : ("Siestas a Domicilio", "las"),
    9604 : ("Fundas Nórdicas para Pinreles", "las"),
    9605 : ("Diseño Séptimo Cielo", ""),
    9607 : ("Pijamas de Plomo para Dormir de Pie", "el"),
    9608 : ("", ""),
    9609 : ("Arrullos a Granel", "los"),
    9613 : ("Los Limpiadores Del Reloj", ""),
    9616 : ("Compañía Eléctrica Luces Fuera", "la"),
    9617 : ("Notas de Cuna - Música para Descansar", ""),
    9619 : ("Sopas Soporíferas", "las"),
    9620 : ("Servicio de Taxis Insomnes", "el"),
    9622 : ("Relojería El Cuco Dormido", "la"),
    9625 : ("Salón de Belleza El Ronquido Alegre", "el"),
    9626 : ("Cuentos para Dormir", " "),
    9627 : ("Mecedoras Automáticas", "las"),
    9628 : ("Calendarios Nocturnos", "los"),
    9629 : ("Joyería Sábanas de Oro", "la"),
    9630 : ("Serrería Como un Tronco", "la"),
    9631 : ("Arreglo de Relojes Estoysopa", "el"),
    9633 : ("La Siesta De Pluto", ""),
    9634 : ("Colchones La Pluma Audaz", "los"),
    9636 : ("Seguro Contra Insomnios", "el"),
    9639 : ("Conservas Ultrahibernadas", "las"),
    9640 : ("Muebles Soporte Total", ""),
    9642 : ("Ganadería Cuentaovejas", "la"),
    9643 : ("Óptica Nopegojo", "la"),
    9644 : ("Peleas de Almohadas Organizadas", "las"),
    9645 : ("Posada Todos al Sobre", "la"),
    9647 : ("¡Hazte la cama! Ferretería", ""),
    9649 : ("Ronquidos Lejanos", "los"),
    9650 : ("Reparaciones Amanecer", ""),
    9651 : ("Martillos para Despertadores", "los"),
    9652 : ("", ""),
    # titles for: phase_8/dna/donalds_dreamland_9200.dna
    9703 : ("Agencia de Viajes Vuelos Cruzados", ""),
    9704 : ("Tienda de Animales la Lechuza", ""),
    9705 : ("Taller Dormido al Volante", ""),
    9706 : ("Dentista Ratoncito Pérez", ""),
    9707 : ("Jardinería Flor de Primavera", ""),
    9708 : ("Floristería Comes Flores", ""),
    9709 : ("Fontanería Tubo Tubular", ""),
    9710 : ("Óptica REM", ""),
    9711 : ("Telefonía Llamada Perdida", ""),
    9712 : ("Cuenta Ovejas, ¡para que tú no tengas que hacerlo!", ""),
    9713 : ("Cintio, Lucio y Picio, Abogados de Oficio", ""),
    9714 : ("Suministros Marinos Barcaza", ""),
    9715 : ("Banco el Gigante Caja Fuerte", ""),
    9716 : ("Organizadores de Fiestas la Guirnalda Mojada", ""),
    9717 : ("Panadería el Bollo Tostado", ""),
    9718 : ("Sándwiches Suela Sandalio", ""),
    9719 : ("Tienda de Almohadas Armadillo", ""),
    9720 : ("Entrenamiento de Voz Profunda", ""),
    9721 : ("Tienda de Alfombras la Sombra", ""),
    9722 : ("Agencia de Talentos Lentos", ""),
    9725 : ("Pijamas el Gato", ""),
    9727 : ("Si Duermes Pierdes", ""),
    9736 : ("Agencia de Empleo el Trabajo Ideal", ""),
    9737 : ("Escuela de Baile el Vals de Matilde", ""),
    9738 : ("Casa de Zzzzzs", ""),
    9740 : ("Escuela Esgrima el Filo", ""),
    9741 : ("Exterminadores la Pulga Saltarina", ""),
    9744 : ("Crema Antiarrugas la Arruga es Bella", ""),
    9752 : ("Comañía de Gas la Ciudad", ""),
    9753 : ("Helados el Frío Polar", ""),
    9754 : ("Excursiones en Poni el Estribo", ""),
    9755 : ("Productora de Cine Palomitas", ""),
    9756 : ("", ""),
    9759 : ("Centro de Belleza la Bella Durmiente", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : ("Tienda de Bromas", "la"),
    3508 : ("Cuartel general", "el"),
    3509 : ("Tienda de Ropa", "la"),
    3511 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("Compañía Eléctrica Polo Norte", "la"),
    3602 : ("Gorros de Nieve Geli", "los"),
    3605 : ("", ""),
    3607 : ("Ventisca a la Vista", "la"),
    3608 : ("Bobsled para Lactantes", ""),
    3610 : ("Hipermercado Esquimal de Mito", "el"),
    3611 : ("Quitanieves Escárchez", "la"),
    3612 : ("Diseño de Iglús", "el"),
    3613 : ("Bicicletas Carámbanez", "las"),
    3614 : ("Cereales Copos de Nieve", "los"),
    3615 : ("Arenques en Almíbar", "los"),
    3617 : ("Dirigibles de Aire Frío", "los"),
    3618 : ("¿Avalancha? Sin Problemas Gestión de Crisis", "la"),
    3620 : ("Clínica de Esquí", "la"),
    3621 : ("Bar El Deshielo", "el"),
    3622 : ("", ""),
    3623 : ("Panes Criogenizados Frigomiga", "los"),
    3624 : ("Sándwiches Bajocero", "los"),
    3625 : ("Radiadores de la Tía Ritona", "los"),
    3627 : ("Adiestramiento de San Bernardos", "el"),
    3629 : ("Cafetería El Braserillo que Ríe", "la"),
    3630 : ("Agencia de Viajes Témpano Tenaz", "la"),
    3634 : ("Remontes Rascafría", "los"),
    3635 : ("Leña Usada", "la"),
    3636 : ("Surtido de Sabañones", "el"),
    3637 : ("Patines Pati", "los"),
    3638 : ("Trineos y Cuatrineos", "los"),
    3641 : ("Camas Heladas Pepe Tundra", "las"),
    3642 : ("Óptica El Yeti Tuerto", "la"),
    3643 : ("Salón de la Bola de Nieve", "el"),
    3644 : ("Cubitos de Hielo Fundidos", "los"),
    3647 : ("Alquiler de Chaqués El Pingüino Beduino", "el"),
    3648 : ("Hielo Instantáneo", "el"),
    3649 : ("Hambrrrrguesas", "las"),
    3650 : ("Antigüedades Antárticas", "las"),
    3651 : ("Dibuperritos Helados Pipe", "los"),
    3653 : ("Joyería Frío como el Diamante", "la"),
    3654 : ("Cuartel general", "el"),
    # titles for: phase_8/dna/the_burrrgh_3200.dna
    3702 : ("Almacén de Invierno", "el"),
    3703 : ("", ""),
    3705 : ("Carámbanos a Granel", "los"),
    3706 : ("Batidos El Tembleque", "los"),
    3707 : ("Hogar, Gélido Hogar", ""),
    3708 : ("Plutón en tu Casa", ""),
    3710 : ("Comidas Alaska en Enero", "las"),
    3711 : ("", ""),
    3712 : ("Tuberías Muy Muy Frías", "las"),
    3713 : ("Dentista El Castañeteo Perpetuo", "el"),
    3715 : ("Surtido de Sopitas de la Tía Ártica", "el"),
    3716 : ("Sal Gorda para Carreteras", "la"),
    3717 : ("Polos y Helados Variados", "los"),
    3718 : ("Calefacción a Domicilio", "la"),
    3719 : ("Paté de Cubitos", "el"),
    3721 : ("Trineos de Ocasión", "los"),
    3722 : ("Tienda de Esquí Anchoa", "la"),
    3723 : ("Guantes de Nieve Tiritonio", "los"),
    3724 : ("La Voz de la Tundra", "la"),
    3725 : ("Me Mareo en Trineo", ""),
    3726 : ("Mantas Eléctricas Solares", "las"),
    3728 : ("Quitanieves Cenutrio", "el"),
    3729 : ("", ""),
    3730 : ("Desguace de Muñecos de Nieve", "el"),
    3731 : ("Chimeneas Portátiles", "las"),
    3732 : ("La Nariz Helada", ""),
    3734 : ("Tímpanos como Témpanos Otorrino", "los"),
    3735 : ("Forros Polares de Papel", "los"),
    3736 : ("Cucuruchos de Hielo Picado", "los"),
    3737 : ("Comidas Eslalon", "las"),
    3738 : ("Escondites Frío Frío", "los"),
    3739 : ("Cuartel general", "el"),
    # titles for: phase_8/dna/the_burrrgh_3300.dna
    3801 : ("Cuartel general", ""),
    3806 : ("Alimentos Alpinos", ""),
    3807 : ("Sombras de la Marmota", ""),
    3808 : ("El Sweater No Es Eterno", ""),
    3809 : ("Hel-lado Equivocado", ""),
    3810 : ("Edredón Algodón", ""),
    3811 : ("Ángel de Nieve", ""),
    3812 : ("Mitones para Ratones", ""),
    3813 : ("Botas de Nieve para Nueve", ""),
    3814 : ("Sodas el Buen Trago", ""),
    3815 : ("El Chalet Tupé", ""),
    3816 : ("Muérdago Dragón", ""),
    3817 : ("Club de Montaña el Bello Invierno", ""),
    3818 : ("El Local de las Palas", ""),
    3819 : ("Servicio de Limpieza el Esplendor", ""),
    3820 : ("Blancura de Nieve", ""),
    3821 : ("Vacación e Hibernación", ""),
    3823 : ("Cimientos Aspavientos", ""),
    3824 : ("Castañas Asadas la Hoguera", ""),
    3825 : ("Elegantes Sombreros el Gatito", ""),
    3826 : ("¡Mis Chanclas!", ""),
    3827 : ("Coronas de Coral", ""),
    3828 : ("El Hombre de las Nieves", ""),
    3829 : ("Terreno de las Piñas", ""),
    3830 : ("Desempañado de Gafas Tolomiro", ""),
    }

# translate
# DistributedCloset.py
ClosetTimeoutMessage = "Lo siento, el tiempo se\n acabó."
ClosetNotOwnerMessage = "Este no es tu clóset, pero te puedes probar la ropa."
ClosetPopupOK = "Muy bien"
ClosetPopupCancel = lCancel
ClosetDiscardButton = "Rechazar"
ClosetAreYouSureMessage = "Borraste algunas prendas. ¿Realmente quieres eliminarlas?"
ClosetYes = lYes
ClosetNo = lNo
ClosetVerifyDelete = "¿Borrar %s?"
ClosetShirt = "Esta camiseta"
ClosetShorts = "Este pantalón corto"
ClosetSkirt = "Esta falda"
ClosetDeleteShirt = "Borrar\ncamiseta"
ClosetDeleteShorts = "Borrar\npantalón corto"
ClosetDeleteSkirt = "Borrar\nfalda"

# EstateLoader.py
EstateOwnerLeftMessage = "Lo siento, el dueño de esta propiedad se marchó. Serás enviado al dibuparque en %s segundos"
EstatePopupOK = "Muy bien"
EstateTeleportFailed = "No pudiste irte a casa. ¡Inténtalo de nuevo!"
EstateTeleportFailedNotFriends = "Lo siento, %s está en una dibuhacienda que no es amiga tuya."

# DistributedTarget.py
EstateTargetGameStart = "¡El juego del objetivo curadibu ya comenzó!"
EstateTargetGameInst = "Cuanto más golpees el objetivo rojo, mejor será tu nivel de mejora curadibu."
EstateTargetGameEnd = "El juego del objetivo curadibu ya terminó..."

# DistributedCannon.py
EstateCannonGameEnd = "El alquiler del juego de Cañones ya terminó."

# DistributedHouse.py
AvatarsHouse = "Casa de %s"

# BankGui.py
BankGuiCancel = lCancel
BankGuiOk = lOK

# DistributedBank.py
DistributedBankNoOwner = "Lo siento, este no es tu banco."
DistributedBankNotOwner = "Lo siento, este no es tú banco."

# FishSellGui.py
FishGuiCancel = lCancel
FishGuiOk = "Vender todo"
FishTankValue = "¡Hola, %(name)s! En la cubeta llevas %(num)s peces, que tienen un valor total de %(value)s golosinas. ¿Quieres venderlos todos?"

#FlowerSellGui.py
FlowerGuiCancel = lCancel
FlowerGuiOk = "Vender todo"
FlowerBasketValue = "%(name)s, tienes %(num)s flores en tu cesta por un valor total de %(value)s golosinas. ¿Quieres venderlas todas?"


def GetPossesive(name):
    if name[-1:] == 's':
        possesive = name + "'"
    else:
        possesive = name + ""
    return possesive

# PetTraits
# VERY_BAD, BAD, GOOD, VERY_GOOD
PetTrait2descriptions = {
    'hungerThreshold': ('Siempre hambriento', 'A menudo hambriento',
                        'A veces hambriento', 'Raramente hambriento',),
    'boredomThreshold': ('Siempre aburrido', 'A menudo aburrido',
                         'A veces aburrido', 'Raramente aburrido',),
    'angerThreshold': ('Siempre gruñón', 'A menudo gruñón',
                       'A veces gruñón', 'Raramente gruñón'),
    'forgetfulness': ('Siempre olvida', 'A menudo olvida',
                      'A veces olvida', 'Raramente olvida',),
    'excitementThreshold': ('Muy tranquilo', 'Bastante tranquilo',
                            'Bastante nervioso', 'Muy nervioso',),
    'sadnessThreshold': ('Siempre triste', 'A menudo triste',
                         'A veces triste', 'Raramente triste',),
    'restlessnessThreshold': ('Siempre inquieto', 'A menudo inquieto',
                         'A veces inquieto', 'Raramente inquieto',),
    'playfulnessThreshold': ('Raramente juguetón', 'A veces juguetón',
                         'A menudo juguetón', 'Siempre juguetón',),
    'lonelinessThreshold': ('Siempre solitario', 'A menudo solitario',
                         'A veces solitario', 'Raramente solitario',),
    'fatigueThreshold': ('Siempre cansado', 'A menudo cansado',
                         'A veces cansado', 'Raramente cansado',),
    'confusionThreshold': ('Siempre confundido', 'A menudo confundido',
                         'A veces confundido', 'Raramente confundido',),
    'surpriseThreshold': ('Siempre sorprendido', 'A menudo sorprendido',
                         'A veces sorprendido', 'Raramente sorprendido',),
    'affectionThreshold': ('Raramente cariñoso', 'A veces cariñoso',
                         'A menudo cariñoso', 'Siempre cariñoso',),
    }
    

# end translate

# DistributedFireworkShow.py
FireworksInstructions = lToonHQ+": Para ver mejor, pulsa la tecla \"Re Pág\". "

FireworksJuly4Beginning = lToonHQ+": ¡Bienvenido a los fuegos artificiales de verano! ¡Disfruta del espectáculo!"
FireworksJuly4Ending = lToonHQ+": ¡Espero que te haya gustado el espectáculo! ¡Que pases un buen verano!"
FireworksNewYearsEveBeginning = lToonHQ+": ¡Feliz año nuevo! ¡Que disfrutes de los fuegos artificiales!"
FireworksNewYearsEveEnding = lToonHQ+": ¡Espero que te haya gustado el espectáculo! ¡Feliz año nuevo!"

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
TipTitle = "UN DIBUCONSEJO:"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Para comprobar rápidamente el estado de tu dibutarea, pulsa la tecla \"Fin\".",
    "Para echar un vistazo rápido a tu página de bromas, pulsa la tecla \"Inicio\".",
    "Pulsa la tecla \"F7\" para abrir la Lista de amigos.",
    "Para abrir o cerrar el dibucuaderno, pulsa la tecla \"F8\".",
    "Para mirar hacia arriba, pulsa la tecla \"Re Pág\" y para mirar hacia abajo, pulsa la tecla \"Av Pág\".",
    "Pulsa la tecla \"Control\" para saltar.",
    "Si pulsas la tecla \"F9\", obtendrás una captura de pantalla que quedará almacenada en la carpeta Toontown de tu ordenador.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "Puedes intercambiar códigos de Amigos secretos con personas que conozcas en la vida real para poder charlar con ellas en Toontown.",
    "En la página Opciones del dibucuaderno podrás cambiar la resolución de la pantalla, modificar el sonido y ajustar otras opciones.",
    "Pruébate la ropa de tus amigos en el clóset de su casa.",
    "Para ir a tu casa, usa el botón \"Ir a casa\" del mapa.",
    "Cada vez que completes una dibutarea, tus puntos de risa se rellenarán automáticamente.",
    "Puedes examinar el surtido de las tiendas de ropa sin necesidad de tener un boleto de ropa.",
    "Las recompensas de ciertas dibutareas te permiten llevar más bromas y golosinas.",
    "En tu Lista de amigos puedes tener hasta 50 usuarios.",
    "Algunas recompensas de dibutareas te permitirán teletransportarte a los dibuparques de Toontown con la página del mapa del dibucuaderno.",
    "Para aumentar tus puntos de risa en los dibuparques, reúne tesoros, como estrellas y cucuruchos de helado.",
    "Si tienes prisa para curarte después de un duro combate, ve a tu propiedad y recoge cucuruchos de helado.",
    "Para cambiar las vistas de tu dibu, pulsa la tecla Tab.",
    "A veces verás que varias dibutareas distintas ofrecen la misma recompensa. ¡Compáralas!",
    "Una forma divertida de avanzar en el juego consiste en buscar amigos que tengan dibutareas parecidas.",
    "Nunca te hará falta guardar la partida en Toontown. Los servidores de Toontown almacenan toda la información necesaria de manera continua.",
    "Si quieres susurrar a otros dibus, haz clic en ellos o selecciónalos en tu Lista de amigos.",
    "Algunas frases de SpeedChat hacen que tu dibu muestre emociones.",
    "Si la zona en la que estás está demasiado llena, trata de cambiar de distrito. Acude a la página de Distritos del dibucuaderno y selecciona otro distrito.",
    "Si recuperas edificios aparecerá una estrella de bronce, plata u oro sobre tu dibu.",
    "Si recuperas edificios suficientes para conseguir que aparezca una estrella sobre tu cabeza, quizá veas tu nombre escrito en la pizarra de un cuartel general.",
    "A veces, los bots vuelven a capturar edificios recuperados. ¡La única manera de conservar tu estrella consiste en ir a recuperar más edificios!",
    "Los nombres de tus amigos secretos aparecen en azul.",
    # Fishing
    "¡A ver si puedes conseguir todos los peces de Toontown!",
    "En cada estanque hay peces distintos. ¡Prueba en todos!",
    "Cuando tu cubeta de pesca esté llena, vende tus peces a los pescadores de los dibuparques.",
    "Puedes vender tus peces a los pescadores o en las tiendas de animales.",
    "Las cañas de pescar más pesadas pescan peces más pesados, pero para usarlas necesitas gastar más golosinas.",
    "Puedes comprar cañas de pescar más fuertes en el catálogo tolón-tolón.",
    "Con los peces más pesados, conseguirás más golosinas en la tienda de animales.",
    "Con los peces más extraños, conseguirás más golosinas en la tienda de animales.",
    "Al pescar, a veces puedes encontrar bolsas de golosinas.",
    "En algunas dibutareas hay que pescar objetos de los estanques.",
    "Los estanques de pesca de los dibuparques tienen peces diferentes a los de los estanques de las calles.",
    "Algunos peces son muy poco comunes. ¡Sigue pescando hasta que los tengas todos!",
    "El estanque de tu hacienda tiene peces que solo se pueden pescar ahí.",
    "¡Por cada 10 especies que pesques recibirás un trofeo de pesca!",
    "En el dibucuaderno podrás ver los peces que pescaste.",
    "Algunos trofeos de pesca te premian con una subida del risómetro.",
    "Pescar es una manera muy buena de conseguir más golosinas.",
    # Doodles
    "¡Adopta un Dibuperrito en la tienda de animales!",
    "Las tiendas de animales reciben cada día nuevos Dibuperritos para vender.",
    "Visita las tiendas de animales cada día para ver los nuevos Dibuperritos que recibieron.",
    "Diferentes barrios tienen Dibuperritos distintos en adopción.",
    # Karting
    "Demuestra tu estilo al volante y aumenta tu límite de puntos de risa en el Estadio de Goofy.",
    "Accede al Estadio de Goofy a través del túnel en forma de neumático del dibuparque del Centro de Toontown.",
    "Consigue puntos de risa en el Estadio de Goofy.",
    "El estadio de Goofy tiene seis circuitos de carreras distintos. "
    ),

  TIP_STREET : (
    "Hay cuatro tipos de bots: abogabots, chequebots, vendebots y jefebots.",
    "Cada circuito de bromas tiene distintas cantidades de precisión y daños.",
    "Las bromas de sonido afectan a todos los bots, pero despiertan a los bots que persiguen cebos.",
    "Derrota a los bots siguiendo un orden estratégico: aumentará tus posibilidades en ganar los combates.",
    "El circuito de broma curadibu te permite sanar a otros dibus durante los combates.",
    "¡Durante las invasiones de bots, los puntos de experiencia de bromas se duplican!",
    "Si formas un equipo con otros dibus y usas el mismo circuito de bromas en el combate, conseguirás una bonificación por daños a los bots.",
    "Las bromas se usan por orden, de arriba abajo, según aparecen en el menú de bromas del combate.",

    "La fila de luces circulares que hay sobre los ascensores de los edificios bot muestra cuántos pisos tienen.",
    "Haz clic en un bot para ver más detalles sobre él.",
    "Si usas bromas de alto nivel contra bots de bajo nivel, no conseguirás puntos de experiencia.",
    "Las bromas que te dan experiencia tienen un fondo azul en el menú de bromas del combate.",
    "La experiencia que te dan las bromas se multiplica en el interior de los edificios bot. Cuanto más elevado sea el piso, mayor será el factor de multiplicación.",
    "Al ganarle a un bot, todos los dibus que hayan participado conseguirán puntos cuando termine el combate.",
    "Todas las calles de Toontown tienen distintos tipos y niveles de bots.",
    "En las aceras estarás a salvo de los bots.",
    "En las calles, las puertas de las casas cuentan chistes cuando te acercas.",
    "Algunas dibutareas te proporcionan entrenamiento para nuevos circuitos de bromas. ¡Sólo podrás escoger seis de los siete circuitos de bromas, así que elige con cuidado!",
    "Las trampas solo son útiles cuando tú coordines con tus amigos el uso de los cebos en el combate.",
    "Los cebos de alto nivel tienen menos posibilidades de fallar.",
    "Las bromas de bajo nivel tienen poca precisión contra los bots de alto nivel.",
    TheCogs+" no pueden atacar cuando siguieron un cebo hasta un combate.",
    "Cuando tus amigos y tú recuperen un edificio bot, serán recompensados con retratos dentro del edificio rescatado.",
    "Si usas una broma curadibu en un dibu que tenga el risómetro completo, no conseguirás experiencia de curadibu.",
    TheCogs+" quedarán aturdidos durante un instante al ser alcanzados por cualquier broma. Esto aumenta la probabilidad de que otras bromas los alcancen en la misma ronda.",
    "Las bromas de caída tienen menos probabilidad de alcanzar su objetivo, pero su precisión aumenta cuando el bot fue alcanzado antes por otra broma en la misma ronda.",
    "Cuando hayas derrotado suficientes bots, podrás usar el \"radar de bots\" haciendo clic en los iconos de bots de la página galería de bots del dibucuaderno.",
    "Durante los combates, podrás saber a qué bot están atacando tus compañeros de equipo mirando los guiones (-) y las X.",
    "Durante los combates, los bots llevan una luz que indica su estado de salud: verde significa que está sano y rojo que casi está destruido.",
    "Solo pueden combatir a la vez un máximo de cuatro dibus.",
    "En la calle, los bots tienen más tendencia a luchar contra varios dibus que contra uno solo.",
    "Los dos bots más difíciles de cada tipo se encuentran en el interior de los edificios.",
    "Las bromas de caída no funcionan contra los bots que siguen un cebo.",
    TheCogs+" tienden a atacar al dibu que les causó más daños.",
    "Las bromas de sonido no dan bonificación por daños contra los bots que siguen cebos.",
    "Si esperas demasiado para atacar a un bot que sigue un cebo, se despertará. Cuanto mayor sea el nivel del cebo, mayor será su duración.",
    ),

  TIP_MINIGAME : (
     "Cuando tengas llena la jarra de golosinas, las que consigas en los juegos del tranvía irán a parar directamente a tu banco.",
    "Puedes usar las teclas de flecha en lugar del mouse en el juego del tranvía \"Imita a Minnie\".",
    "En el juego del cañón, usa las teclas de flecha para mover el cañón y pulsa la tecla \"Control\" para disparar.",
    "En el juego de los anillos, conseguirás puntos de bonificación cuando todo el grupo consiga atravesar sus anillos.",
    "Si juegas perfectamente a Imita a Minnie, duplicarás los puntos.",
    "En el juego de la cuerda, conseguirás más golosinas si te enfrentas a un bot más grande.",
    "La dificultad de los juegos del tranvía varían según el barrio: en el "+lToontownCentral+" están los más fáciles, y en "+lDonaldsDreamland+", los más difíciles.",
    "En algunos juegos del tranvía sólo se puede jugar en grupo.",
   ),

  TIP_COGHQ : (
    "Antes de entrar en el edificio jefe debes completar el disfraz de bot.",
    "Antes de visitar al director financiero debes completar el disfraz de chequebot.",
    "Antes de visitar al Juez debes completar el disfraz de abogabot.",
   "Puedes saltar encima de los matones bots para dejarlos temporalmente incapacitados.",
    "Reúne méritos bot luchando contra bots y venciéndolos.",
    "Recoge botdólares derrotando chequebots en batalla.",
    "Recoge Notificaciones del tribunal derrotando abogabots en batalla.",
    "Recoge acciones derrotando jefebots en batalla.",
    "Se te otorgarán más méritos si luchas contra bots de mayor nivel.",
    "Cuando reúnas los méritos bot necesarios para recibir un ascenso, vete a ver al vendebot VIP.",
    "Cuando consigas suficientes botdólares para ganarte un ascenso, ve a ver al director financiero chequebot.",
    "Cuando consigas suficientes Notificaciones del tribunal para ganarte un ascenso, ve a ver al Juez abogabot!",
    "Cuando consigas suficientes acciones para ganarte un ascenso, ve a ver al director general jefebot!",
    "Cuando llevas el disfraz de bot puedes hablar como uno de ellos.",
    "Hasta ocho dibus pueden unirse para luchar contra el vendebot VIP.",
    "Hasta ocho dibus pueden unirse para luchar contra el director financiero chequebot",
    "Hasta ocho dibus pueden unirse para luchar contra el Juez abogabot.",
    "Hasta ocho dibus pueden unirse para luchar contra el director general jefebot.",
    "Una vez dentro del cuartel general bot, sube las escaleras hasta llegar al capataz.",
    "Cada vez que luches en el cuartel general vendebot recibirás una pieza del disfraz de vendebot.",
    "Puedes comprobar cuánto te falta para completar el disfraz bot con el dibucuaderno.",
    "Puedes comprobar cuántos méritos llevas en la página del disfraz del dibucuaderno.",
    "Antes de enfrentarte al VIP, comprueba que vas bien cargado de bromas y puntos de risa.",
    "El disfraz de bot irá cambiando a medida que recibas ascensos.",
    "Debes derrotar al "+Foreman+" para obtener una pieza del disfraz de bot.",
    "Consigue piezas del disfraz de chequebot como recompensa por completar dibutareas en Sueñolandia de Donald.",
    "Los chequebots fabrican y distribuyen su moneda, los botdólares, en tres fabricas de monedas: Moneditas, Dólar y Lingote.",
    "Espera a que el director financiero esté mareado para lanzar una caja fuerte, ¡si no esperas la usará de casco! Golpea el casco con otra caja fuerte para quitárselo.",
    "Consigue piezas del disfraz de abogabot como recompensa por completar dibutareas para el Profesor Copos.",
    "Sorprenderse tiene sus ventajas: los bots virtuales del cuartel general abogabot no te recompensarán con Notificaciones del tribunal.",
    ),
  TIP_ESTATE : (
    # Doodles
    "Los Dibuperritos entienden algunas frases de SpeedChat. ¡Pruébalas!",
    "Utiliza el menú \"Mascota\" de SpeedChat para decirle a tu Dibuperrito que haga acrobacias.",
    "Puedes enseñarles a los Dibuperritos a hacer acrobacias con clases del catálogo tolón-tolón de Clarabel.",
    "Premia a tu Dibuperrito cuando haga una acrobacia.",
    "Si visitas la hacienda de un amigo, tu Dibuperrito también irá.",
    "Cuando tu Dibuperrito tenga hambre, dale una golosina.",
    "Haz clic sobre un Dibuperrito para acceder a un menú donde podrás alimentarlo, rascarlo y llamarlo.",
    "A los Dibuperritos les encanta la compañía. ¡Invita a tus amigos a jugar!",
    "Cada Dibuperrito tiene su propia personalidad.",
    "Puedes devolver a tu Dibuperrito y adoptar a otro en la tienda de animales.",
    "Cuando un Dibuperrito haga una actobacia, los dibus de alrededor se curarán.",
    "Los Dibuperritos hacen las acrobacias mejor cuando practican. ¡Insiste!",
    "Las acrobacias más avanzadas de tu Dibuperrito curan a los dibus más rápido.",
    "Los Dibuperritos más experimentados pueden hacer más acrobacias y tardan más en cansarse.",
    "En tu lista de amigos podrás ver una lista con los Dibuperritos más cercanos.",
    # Furniture / Cattlelog
    "Compra muebles del catálogo tolón-tolón de Clarabel para decorar tu casa.",
    "En el banco que tienes dentro de tu casa hay más golosinas.",
    "En el clóset dentro de tu casa hay más ropa.",
    "Ve a la casa de tu amigo y pruébate su ropa.",
    "Compra cañas de pescar mejores en el catálogo tolón-tolón de Clarabel.",
    "Compra bancos más grandes en el catálogo tolón-tolón de Clarabel.",
    "Llama a Clarabel con el teléfono que tienes en tu casa.",
    "Clarabel vende clósets más grandes donde cabe más ropa.",
    "Antes de usar un Boleto de ropa, haz lugar en tu clóset.",
    "Clarabel vende todo lo que necesitas para decorar tu casa.",
    "Busca en tu buzón los paquetes con encargos que le hayas hecho a Clarabel.",
    "La ropa del catálogo tolón-tolón de Clarabel tarda una hora en llegar.",
    "El papel de pared y el suelo del catálogo tolón-tolón de Clarabel tardan una hora en llegar.",
    "Los muebles del catálogo tolón-tolón de Clarabel tardan un día entero en llegar.",
    "Almacena los muebles que te sobren en el desván.",
    "Cuando salga un nuevo catálogo tolón-tolón, recibirás un aviso de Clarabel.",
    "Cuando llegue una entrega del catálogo tolón-tolón de Clarabel, recibirás un aviso.",
    "Cada semana salen nuevos catálogos tolón-tolón.",
    "Busca los artículos de vacaciones de edición limitada en el catálogo tolón-tolón.",
    "Lleva los muebles que no quieras a la papelera.",
    # Fish
    "Algunos peces, como la merluza de colar, son más comunes en las haciendas dibu.",
    # Misc
    "Puedes invitar a tus amigos a tu hacienda utilizando SpeedChat.",
    "¿Sabías que el color de tu casa coincide con el color de tu panel Eligedibu?",
    ),
   TIP_KARTING : (
    # Goofy Speedway zone specific
    "Compra un kart Roadster, Utilitario dibu o Cruiser en la tienda de autos de Goofy.",
    "Personaliza tu kart con adhesivos, llantas y más cosas en la tienda de autos de Goofy.",
    "Consigue boletos compitiendo con otros karts en el Estadio de Goofy.",
    "Los boletos son la única moneda de cambio que se acepta en la tienda de autos de Goofy.",
    "Para competir, deben entregarse boletos como depósito.",
    "Una página especial del dibucuaderno te permite personalizar tu kart.",
    "Una página especial del dibucuaderno te permite ver los récords en cada circuito.",
    "Una página especial del dibucuaderno te permite exhibir tus trofeos.",
    "El Estadio Bola Loca es el circuito más sencillo del Estadio de Goofy.",
    "Acres Aéreos tiene más colinas y saltos que ningún otro circuito del Estadio de Goofy.",
    "Boulevard Ventisca es el circuito más difícil del Estadio de Goofy.",
    ),
    TIP_GOLF: (
    # Golfing specific
    "Pulsa la tecla Tab para ver una imagen aérea del campo de golf.",
    "Pulsa la tecla de flecha arriba para colocarte en dirección al hoyo de golf.",
    "El palo de golf se mueve igual que se lanza una tarta.",
    ),
    }

FishGenusNames = {
    0 : "Pez globo",
    2 : "Pez gato",
    4 : "Pez payaso",
    6 : "Pez congelado",
    8 : "Estrella de mar",
    10 : "Merluza de colar",
    12 : "Pez perro",
    14 : "Anguila amorosa",
    16 : "Tiburón matrona",
    18 : "Rey centollo",
    20 : "Pez luna",
    22 : "Caballito de mar",
    24 : "Tiburón billarista",
    26 : "Barboso",
    28 : "Trucha pirata",
    30 : "Atún piano",
    32 : "Bocadidusa",
    34 : "Raya diablo",
    }

FishSpeciesNames = {
    0 : ( "Pez globo",
          "Pez globo aerostático",
          "Pez globo meteorológico",
          "Pez globo de agua",
          "Pez globo rojo",
          ),
    2 : ( "Pez gato",
          "Pez gato siamés",
          "Pez gato callejero",
          "Pez gato atigrado",
          "Pez gato montés",
          ),
    4 : ( "Pez payaso",
          "Pez payaso triste",
          "Pez payaso cumpleañero",
          "Pez payaso circense",
          ),
    6 : ( "Pez congelado",
          ),
    8 : ( "Estrella de mar",
          "Estrella de mar de 5 puntas",
          "Estrella de mar de rock",
          "Estrella de mar del alba",
          "Estrella de mar fugaz",
          ),
    10 : ( "Merluza de colar",
           ),
    12 : ( "Pez perro",
           "Pez perro de presa",
           "Pez perro caliente",
           "Pez perro dálmata",
           "Pez perro cachorro",
           ),
    14 : ( "Anguila amorosa",
           "Anguila eléctrica amorosa",
           ),
    16 : ( "Tiburón matrona",
           "Tiburón matrona Clara",
           "Tiburón matrona Feliciana",
           ),
    18 : ( "Rey Centollo",
           "Príncipe Centollo",
           "Regente Centollo",
           ),
    20 : ( "Pez luna",
           "Pez luna llena",
           "Pez media luna",
           "Pez luna nueva",
           "Pez luna creciente",
           "Pez luna de miel",
           ),
    22 : ( "Caballito de mar",
           "Caballito de Troya de mar",
           "Caballito percherón de mar",
           "Caballito árabe de mar",
           ),
    24 : ( "Tiburón billarista",
           "Tiburón billarista aprendiz",
           "Tiburón billarista experto",
           "Tiburón billarista olímpico",
           ),
    26 : ( "Barboso pardo",
           "Barboso negro",
           "Barboso koala",
           "Barboso madroñero",
           "Barboso polar",
           "Barboso panda",
           "Barboso pardo",
           "Barboso gris",
           ),
    28 : ( "Trucha pirata",
           "Trucha pirata corsaria",
           "Trucha pirata bucanera",
           ),
    30 : ( "Atún piano",
           "Atún piano de cola",
           "Atún clavicordio",
           "Atún piano vertical",
           "Atún piano eléctrico",
           ),
    32 : ( "Bocadidusa",
           "Bocadidusa de queso",
           "Bocadidusa crujiente",
           "Bocadidusa de mermelada",
           "Bocadidusa de uva",
           ),
    34 : ( "Raya diablo",
           ),
    }

FishFirstNames = (
    "",
    "Anchoa",
    "Anguila",
    "Anzuela",
    "Arenquilla",
    "Besuguito",
    "Beto",
    "Bocartín",
    "Brequita",
    "Caballero",
    "Castañeta",
    "Cazonio",
    "Chicharra",
    "Chicho",
    "Congriano",
    "Corroncho",
    "Curro",
    "Deslenguada",
    "Don",
    "Doña",
    "Dorada",
    "Emperadora",
    "Escarcho",
    "Escorpina",
    "Escualo",
    "Esturiona",
    "Fanequillo",
    "Florinda",
    "Ilustrísima",
    "Jurelio",
    "Kiko",
    "Lisa",
    "Lubino",
    "Lucio",
    "Nelson",
    "Nemo",
    "Neptuno",
    "Nina",
    "Palmira",
    "Palometa",
    "Perco",
    "Pintarroja",
    "Rapero",
    "Robaldiño",
    "Salmonillo",
    "Sardino",
    "Sargonete",
    "Señora",
    "Señorita",
    "Simbad",
    "Su Eminencia",
    "Su Excelencia",
    "Su Majestad",
    "Tintorero",
    "Tita",
    "Torpedo",
    "Tritón",
    "Trucha",
    "Zompo",
    )

FishLastPrefixNames = (
    "",
    "Agalla",
    "Agua",
    "Aleta",
    "Alga",
    "Ancla",
    "Angula",
    "Arena",
    "Bahía",
    "Ballena",
    "Banda",
    "Barbilla",
    "Boca",
    "Lindo",
    "Branquia",
    "Cabeza",
    "Caña",
    "Cara",
    "Carnaza",
    "Chalupa",
    "Chepa",
    "Cinta",
    "Cococha",
    "Concha",
    "Corbeta",
    "Corriente",
    "Curricana",
    "Escama",
    "Espalda",
    "Espina",
    "Fragata",
    "Gaviota",
    "Laguna Rojo",
    "Mar",
    "Marejada",
    "Medusa",
    "Merluza",
    "Nariz",
    "Ola",
    "Orilla",
    "Panza",
    "Pecera",
    "Pescadilla",
    "Pinza",
    "Plancton",
    "Playa",
    "Raspa",
    "Raya",
    "Rémora",
    "Ría",
    "Ribera",
    "Roca Saludar",
    "Salta",
    "Sirena",
    "Vela",
    "Zambullida",
    )

FishLastSuffixNames = (
    "",
    "del norte",
    "del sur",
    "con filo",
    "en ahumado",
    "de olor",
    "arénquez",
    "atigrado",
    "azul",
    "besúguez",
    "en blanco",
    "doble",
    "oro",
    "fantasma",
    "finura",
    "frescor",
    "en frito",
    "gállez",
    "gato",
    "gordura",
    "gris",
    "limón",
    "lubinez",
    "en morado",
    "a motas",
    "naranja",
    "occidental",
    "oriental",
    "en plano",
    "plata",
    "profundidad",
    "raya",
    "a rayas",
    "rrodabállez",
    "rroja",
    "rrosa",
    "en sal",
    "surf",
    "tropical",
    "trúchez",
    "verde",
    )

CogPartNames = (
    "Muslo izquierdo", "Pantorrilla izquierda", "Pie izquierdo",
    "Muslo derecho", "Pantorrilla derecha", "Pie derecho",
    "Hombro izquierdo",  "Hombro derecho", "Pecho", "Indicador de salud", "Caderas",
    "Brazo izquierdo",  "Antebrazo izquierdo", "Mano izquierda",
    "Brazo derecho", "Antebrazo derecho", "Mano derecha",
    )

CogPartNamesSimple = (
    "Torso",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "Entrada principal"
SellbotLegFactorySpecLobby = "Vestíbulo"
SellbotLegFactorySpecLobbyHallway = "Entrada del vestíbulo"
SellbotLegFactorySpecGearRoom = "Sala de máquinas"
SellbotLegFactorySpecBoilerRoom = "Sala de calderas"
SellbotLegFactorySpecEastCatwalk = "Pasarela este"
SellbotLegFactorySpecPaintMixer = "Mezcladora de pintura"
SellbotLegFactorySpecPaintMixerStorageRoom = "Sala de la mezcladora de pintura"
SellbotLegFactorySpecWestSiloCatwalk = "Pasarela del silo oeste"
SellbotLegFactorySpecPipeRoom = "Sala de tuberías"
SellbotLegFactorySpecDuctRoom = "Sala de conductos"
SellbotLegFactorySpecSideEntrance = "Entrada de servicio"
SellbotLegFactorySpecStomperAlley = "Callejón del pisotón"
SellbotLegFactorySpecLavaRoomFoyer = "Entrada a la sala de la lava"
SellbotLegFactorySpecLavaRoom = "Sala de la lava"
SellbotLegFactorySpecLavaStorageRoom = "Sala donde se guarda la lava"
SellbotLegFactorySpecWestCatwalk = "Pasarela oeste"
SellbotLegFactorySpecOilRoom = "Sala del aceite"
SellbotLegFactorySpecLookout = "Cabina de vigilancia"
SellbotLegFactorySpecWarehouse = "Almacén"
SellbotLegFactorySpecOilRoomHallway = "Entrada a la sala del aceite"
SellbotLegFactorySpecEastSiloControlRoom = "Sala de control del silo este"
SellbotLegFactorySpecWestSiloControlRoom = "Sala de control del silo oeste"
SellbotLegFactorySpecCenterSiloControlRoom = "Sala de control del silo central"
SellbotLegFactorySpecEastSilo = "Silo este"
SellbotLegFactorySpecWestSilo = "Silo oeste"
SellbotLegFactorySpecCenterSilo = "Silo central"
SellbotLegFactorySpecEastSiloCatwalk = "Pasarela del silo este"
SellbotLegFactorySpecWestElevatorShaft = "Hueco del ascensor del silo oeste"
SellbotLegFactorySpecEastElevatorShaft = "Hueco del ascensor del silo este"

#FISH BINGO
FishBingoBingo = "¡BINGO!"
FishBingoVictory = "¡¡VICTORIA!!"
FishBingoJackpot = "¡POZO!"
FishBingoGameOver = "FIN DEL JUEGO"
FishBingoIntermission = "Descanso\ntermina en:"
FishBingoNextGame = "Siguiente juego\nempieza en:"
FishBingoTypeNormal = "Clásico"
FishBingoTypeCorners = "Cuatro esquinas"
FishBingoTypeDiagonal = "Diagonales"
FishBingoTypeThreeway = "A tres líneas"
FishBingoTypeBlockout = "¡COMPLETO!"
FishBingoStart = "¡Es hora de jugar al bingo de los peces! ¡Ve a cualquier muelle disponible para jugar!"
FishBingoOngoing = "¡Bienvenido! El bingo de los peces ya comenzó."
FishBingoEnd = "Espero que te hayas divertido con el bingo de los peces."
FishBingoHelpMain = "¡Bienvenido al bingo de los peces de Toontown! En el estanque, todo el mundo colabora para llenar la tarjeta antes de que se acabe el tiempo."
FishBingoHelpFlash = "Cuando atrapes un pez, haz clic en una de las casillas que parpadean para marcar la tarjeta."
FishBingoHelpNormal = "Esto es una tarjeta de bingo clásica. Marca cualquier casilla en vertical, horizontal o diagonal para ganar."
FishBingoHelpDiagonals = "Marca las dos diagonales para ganar."
FishBingoHelpCorners = "Una tarjeta sencilla de esquinas. Marca las cuatro esquinas para ganar."
FishBingoHelpThreeway = "Tres líneas. Marca las dos diagonales y la fila del medio para ganar. ¡Esta no es fácil!"
FishBingoHelpBlockout = "¡Completo! Marca toda la tarjeta para ganar. ¡Compites con el resto de estanques para hacerte con un gran premio!"
FishBingoOfferToSellFish = "Tu cubeta de peces está lleno. ¿Quieres vender tus peces?"
FishBingoJackpotWin = "¡Gana %s golosinas!"

# ResistanceSCStrings: SpeedChat phrases rewarded for defeating the CFO.
# It is safe to remove entries from this list, which will disable them
# for use from any toons who have already purchased them.  Note that the
# index numbers are stored directly in the database, so once assigned
# to a particular phrase, a given index number should never be
# repurposed to any other phrase.
ResistanceToonupMenu = "Curadibu"
ResistanceToonupItem = "Curadibu %s"
ResistanceToonupItemMax = "Máx."
ResistanceToonupChat = "¡Dibus del mundo, al curadibu!"
ResistanceRestockMenu = "Mejorar broma"
ResistanceRestockItem = "Mejorar broma %s"
ResistanceRestockItemAll = "Todo"
ResistanceRestockChat = "¡Dibus del mundo, a mejorar esas bromas!"
ResistanceMoneyMenu = "golosinas"
ResistanceMoneyItem = "%s golosinas"
ResistanceMoneyChat = "¡Dibus del mundo, a gastar con cabeza!"

# Resistance Emote NPC chat phrases
ResistanceEmote1 = NPCToonNames[9228] + ": ¡Bienvenido a la resistencia!"
ResistanceEmote2 = NPCToonNames[9228] + ": Utiliza tu nuevo emoticono para identificarte ante el resto de miembros."
ResistanceEmote3 = NPCToonNames[9228] + ": ¡Buena suerte!"

# Kart racing
KartUIExit = "Dejar el kart"
KartShop_Cancel = lCancel
KartShop_BuyKart = "Comprar kart"
KartShop_BuyAccessories = "Comprar accesorios"
KartShop_BuyAccessory = "Comprar accesorio"
KartShop_Cost = "Precio: %d boletos"
KartShop_ConfirmBuy = "¿Comprar %s por %d boletos?"
KartShop_NoAvailableAcc = "No hay accesorios de este tipo disponibles"
KartShop_FullTrunk = "Tienes el portaequipaje lleno."
KartShop_ConfirmReturnKart = "¿Seguro que quieres devolver tu kart?"
KartShop_ConfirmBoughtTitle = "¡Felicidades!"
KartShop_NotEnoughTickets = "¡No tienes suficientes boletos!"

KartView_Rotate = "Girar"
KartView_Right = "Derecha"
KartView_Left = "Izquierda"

# starting block
StartingBlock_NotEnoughTickets = "¡No tienes suficientes boletos! Puedes probar una carrera de práctica."
StartingBlock_NoBoard = "Ya no se aceptan participantes para esta carrera. Espera a que comience la siguiente."
StartingBlock_NoKart = "¡Primero necesitas un kart! Habla con uno de los dependientes de la tienda de karts."
StartingBlock_Occupied = "¡Este bloque está ocupado! Prueba en otro lugar."
StartingBlock_TrackClosed = "Este circuito está cerrado por reformas."
StartingBlock_EnterPractice = "¿Quieres participar en una carrera de práctica?"
StartingBlock_EnterNonPractice = "¿Quieres participar en una carrera por %s boletos?"
StartingBlock_EnterShowPad = "¿Quieres aparcar aquí tu auto?"
StartingBlock_KickSoloRacer = "Para las carreras Batalla Dibu y Grand Prix se necesitan dos o más corredores."
StartingBlock_Loading = "¡A la carrera!"

#stuff for leader boards
LeaderBoard_Time = "Tiempo"
LeaderBoard_Name = "Nombre del piloto"
LeaderBoard_Daily = "Puntuaciones diarias"
LeaderBoard_Weekly = "Puntuaciones semanales"
LeaderBoard_AllTime = "Récords generales"

RecordPeriodStrings = [
    LeaderBoard_Daily,
    LeaderBoard_Weekly,
    LeaderBoard_AllTime,
    ]

KartRace_RaceNames = [
    "Práctica",
    "Batalla Dibu",
    "Grand Prix",
    ]

from toontown.racing import RaceGlobals

KartRace_Go = "¡Ya!"
KartRace_Reverse = " Rev"

#needed for leader boards
KartRace_TrackNames = {
  RaceGlobals.RT_Speedway_1     : "Estadio Bola Loca",
  RaceGlobals.RT_Speedway_1_rev : "Estadio Bola Loca" + KartRace_Reverse,
  RaceGlobals.RT_Rural_1        : "Circuito Rústico",
  RaceGlobals.RT_Rural_1_rev    : "Circuito Rústico" + KartRace_Reverse,
  RaceGlobals.RT_Urban_1        : "Circuito Urbano",
  RaceGlobals.RT_Urban_1_rev    : "Circuito Urbano" + KartRace_Reverse,
  RaceGlobals.RT_Speedway_2     : "Coliseo Sacacorchos",
  RaceGlobals.RT_Speedway_2_rev : "Coliseo Sacacorchos" + KartRace_Reverse,
  RaceGlobals.RT_Rural_2        : "Acres Aéreos",
  RaceGlobals.RT_Rural_2_rev    : "Acres Aéreos" + KartRace_Reverse,
  RaceGlobals.RT_Urban_2        : "Boulevard Ventisca",
  RaceGlobals.RT_Urban_2_rev    : "Boulevard Ventisca" + KartRace_Reverse,
  }

KartRace_Unraced = "N/A"

KartDNA_KartNames = {
    0:"Cruiser",
    1:"Roadster",
    2:"Utilitario dibu"
    }

KartDNA_AccNames = {
    #engine block accessory names
    1000: "Filtro de aire",
    1001: "Cuatro barriles",
    1002: "Águila voladora",
    1003: "Cono de dirección",
    1004: "Seis directa",
    1005: "Pala pequeña",
    1006: "Cubierta simple",
    1007: "Pala mediana",
    1008: "Barril simple",
    1009: "Corneta",
    1010: "Pala a rayas",
    #spoiler accessory names
    2000: "Ala espacial",
    2001: "Repuesto parche",
    2002: "Jaula rodillo",
    2003: "Aleta simple",
    2004: "Ala doble",
    2005: "Ala simple",
    2006: "Repuesto estándar",
    2007: "Aleta simple",
    2008: "sp9",
    2009: "sp10",
    #front wheel well accessory names
    3000: "Cono de duelo",
    3001: "Guardabarros Freddie",
    3002: "Estribos de cobalto",
    3003: "Tubos laterales Cobra",
    3004: "Tubos laterales rectos",
    3005: "Guardabarros festoneados",
    3006: "Estribos de carbón",
    3007: "Estribos de madera",
    3008: "rd9",
    3009: "rd10",
    #rear wheel well accessory names (twisty twisty)
    4000: "Tubos de escape enrulado",
    4001: "Guardabarros splash",
    4002: "Tubo de escape doble",
    4003: "Aletas dobles sin adorno",
    4004: "Faldones sin adornos",
    4005: "Tubo de escape quad",
    4006: "Extensiones dobles",
    4007: "Mega tubo de escape",
    4008: "Aletas dobles a rayas",
    4009: "Aletas dobles burbuja",
    4010: "Faldones a rayas",
    4011: "Faldones Mickey",
    4012: "Faldones festoneados",
    #rim accessoKartRace_Exit = "Leave Race"ry names
    5000: "Turbo",
    5001: "Luna",
    5002: "Parches",
    5003: "Tres radios",
    5004: "Tapa de pintura",
    5005: "Corazón",
    5006: "Mickey",
    5007: "Cinco rayos",
    5008: "Daisy",
    5009: "Basket",
    5010: "Hipno",
    5011: "Tribal",
    5012: "Piedra preciosa",
    5013: "Cinco radios",
    5014: "Derribo",
    #decal accessory names
    6000: "Número cinco",
    6001: "Salpicado",
    6002: "Ajedrez",
    6003: "Llamas",
    6004: "Corazones",
    6005: "Burbujas",
    6006: "Tigre",
    6007: "Flores",
    6008: "Rayo",
    6009: "Ángel",
    #paint accessory names
    7000: "Chartreuse",
    7001: "Melocotón",
    7002: "Rojo brillante",
    7003: "Rojo",
    7004: "Granate",
    7005: "Siena",
    7006: "Marrón",
    7007: "Tostado",
    7008: "Coral",
    7009: "Naranja",
    7010: "Amarillo",
    7011: "Crema",
    7012: "Citrina",
    7013: "Lima",
    7014: "Verde marino",
    7015: "Verde",
    7016: "Azul claro",
    7017: "Aqua",
    7018: "Azul",
    7019: "Violeta",
    7020: "Azul real",
    7021: "Azul pizarra",
    7022: "Morado",
    7023: "Lavanda",
    7024: "Rosa",
    7025: "Ciruela",
    7026: "Negro",
    }

RaceHoodSpeedway = "Estadio"
RaceHoodRural = "Rural"
RaceHoodUrban = "Urbano"
RaceTypeCircuit = "Campeonato"
RaceQualified = "clasificado"
RaceSwept = "barrido"
RaceWon = "ganado"
Race = "carrera"
Races = "carreras"
Total = "total"
GrandTouring = "Grand Tour"

def getTrackGenreString(genreId):
    genreStrings = [ "Estadio",
                     "Campo",
                     "Ciudad" ]
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
    str(RaceGlobals.QualifiedRaces[0]) + " " + RaceHoodSpeedway + " " + Race + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[1]) + " " + RaceHoodSpeedway + " " + Races + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[2]) + " " + RaceHoodSpeedway + " " + Races + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[0]) + " " + RaceHoodRural + " " + Race + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[1]) + " " + RaceHoodRural + " " + Races + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[2]) + " " + RaceHoodRural + " " + Races + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[0]) + " " + RaceHoodUrban + " " + Race + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[1]) + " " + RaceHoodUrban + " " + Races + " " + RaceQualified,
    str(RaceGlobals.QualifiedRaces[2]) + " " + RaceHoodUrban + " " + Races + " " + RaceQualified,
    str(RaceGlobals.TotalQualifiedRaces) + " " + Total + " " + Races + " " + RaceQualified,
    # won race trophies
    str(RaceGlobals.WonRaces[0]) + " " + RaceHoodSpeedway + " " + Race + " " + RaceWon,
    str(RaceGlobals.WonRaces[1]) + " " + RaceHoodSpeedway + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonRaces[2]) + " " + RaceHoodSpeedway + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonRaces[0]) + " " + RaceHoodRural + " " + Race + " " + RaceWon,
    str(RaceGlobals.WonRaces[1]) + " " + RaceHoodRural + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonRaces[2]) + " " + RaceHoodRural + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonRaces[0]) + " " + RaceHoodUrban + " " + Race + " " + RaceWon,
    str(RaceGlobals.WonRaces[1]) + " " + RaceHoodUrban + " " + Races + " " + RaceWon,
    str(RaceGlobals.WonRaces[2]) + " " + RaceHoodUrban + " " + Races + " " + RaceWon,
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
    str(RaceGlobals.TrophiesPerCup) + " trofeos de carreras de kart conseguidos! ¡Aumento del risómetro!",
    str(RaceGlobals.TrophiesPerCup * 2) + " trofeos de carreras de kart conseguidos! ¡Aumento del risómetro!",
    str(RaceGlobals.TrophiesPerCup * 3) + " trofeos de carreras de kart conseguidos! ¡Aumento del risómetro!",
    ]

KartRace_TitleInfo = "Prepárate para la carrera"
KartRace_SSInfo = "¡Bienvenido al Estadio Bola Loca!\n¡Pisa a fondo y agárrate fuerte!\n"
KartRace_CoCoInfo = "¡Bienvenido al Coliseo Sacacorchos!\n¡Apovecha los giros inclinados para mantener tu aceleración!\n"
KartRace_RRInfo = "¡Bienvenido al Circuito Rústico!\n¡Sé amable con la fauna y no te salgas del circuito!\n"
KartRace_AAInfo = "¡Bienvenido a Acres Aéreos!\n¡Agárrate fuerte! Esto está lleno de baches...\n"
KartRace_CCInfo = "¡Bienvenido al Circuito Urbano!\n¡Cuidado con los peatones cuando atravieses la ciudad como un rayo!\n"
KartRace_BBInfo = "¡Bienvenido al Boulevard Ventisca!\nVigila tu velocidad. Podría haber placas de hielo.\n"
KartRace_GeneralInfo = "Utiliza Control para lanzar las bromas que recoges en el circuito y las teclas de flecha para controlar tu kart."

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
    RaceGlobals.Daily : 'diario',
    RaceGlobals.Weekly : 'semanal',
    RaceGlobals.AllTime : 'todo el tiempo',
    }

KartRace_FirstSuffix = 'º'
KartRace_SecondSuffix = '    º'
KartRace_ThirdSuffix = '  º'
KartRace_FourthSuffix = '   º'
KartRace_WrongWay = '¡Dirección\nEquivocada!'
KartRace_LapText = "Vuelta %s"
KartRace_FinalLapText = "¡Úlitma vuelta!"
KartRace_Exit = "Salir de la carrera"
KartRace_NextRace = "Siguiente carrera"
KartRace_Leave = "Abandonar la carrera"
KartRace_Qualified = "¡Clasificaste!"
KartRace_Record = "¡Récord!"
KartRace_RecordString = '¡Batiste un nuevo récord %s para %s! Recibes una bonificación de %s boletos.'
KartRace_Tickets = "Boletos"
KartRace_Exclamations = "¡!"
KartRace_Deposit = "Depósito"
KartRace_Winnings = "Ganancias"
KartRace_Bonus = "Bonificación"
KartRace_RaceTotal = "Total de la carrera"
KartRace_CircuitTotal = "Total del circuito"
KartRace_Trophies = "Trofeos"
KartRace_Zero = "0"
KartRace_Colon = ":"
KartRace_TicketPhrase = "%s " + KartRace_Tickets
KartRace_DepositPhrase = KartRace_Deposit + KartRace_Colon + "\n"
KartRace_QualifyPhrase = "Clasificación:\n"
KartRace_RaceTimeout = "Se te agotó el tiempo de espera en la carrera. Tus boletos fueron devueltos. ¡Sigue intentándolo!"
KartRace_RaceTimeoutNoRefund = "Se te agotó el tiempo de espera en la carrera. Tus boletos no fueron devueltos porque el Grand Prix ya había comenzado. ¡Sigue intentándolo!"
KartRace_RacerTooSlow = "Tardaste demasiado en completar la carrera. Tus boletos no fueron devueltos. ¡Sigue intentándolo!"
KartRace_PhotoFinish = "¡Final fotográfico!"
KartRace_CircuitPoints = "Puntos del circuit"

CircuitRaceStart = "El Grand Prix de Toontown en el Estadio de Goofy está a punto de comenzar! ¡Para ganar, obtén más puntos que nadie en tres carreras consecutivas!"
CircuitRaceOngoing = "¡Bienvenido! El Grand Prix de Toontown ya comenzó."
CircuitRaceEnd = "Eso es todo por hoy en el Grand Prix de Toontown del Estadio de Goofy. ¡Hasta la semana que viene!"

# Trick-or-Treat holiday
TrickOrTreatMsg = '¡Ya encontraste este\npremio!'

#temp lawbot boss dialog text
LawbotBossTempIntro0 = "Veamos, ¿qué tenemos hoy en la lista?"
LawbotBossTempIntro1 = "¡Ajá, tenemos a un dibu procesado!"
LawbotBossTempIntro2 = "La acusación tiene buenos argumentos."
LawbotBossTempIntro3 = "Y aquí está el jurado."
LawbotBossTempIntro4 = "Un momento... ¡Son dibus!"
LawbotBossTempJury1 = "A continuación, se inicia la selección del jurado."
LawbotBossHowToGetEvidence = "Toca la tribuna de testigos para conseguir pruebas."
LawbotBossTrialChat1 = "La sesión del juicio comenzó"
LawbotBossHowToThrowPies = "¡Pulsa la tecla Borrar para lanzar las pruebas\n a los abogados o sobre la balanza!"
LawbotBossNeedMoreEvidence = "¡Necesitas conseguir más pruebas!"
LawbotBossDefenseWins1 = "¡Imposible! ¿La defensa ganó?"
LawbotBossDefenseWins2 = "No. ¡Se anula el juicio! Se programará uno nuevo."
LawbotBossDefenseWins3 = "Ummm, estaré en mi despacho."
LawbotBossProsecutionWins = "Fallo a favor del demandante"
LawbotBossReward = "Concedo un ascenso y la capacidad para invocar bots"
LawbotBossLeaveCannon = "Salir del cañón"
LawbotBossPassExam = "Bah, así que pasaste el examen de letrados."
LawbotBossTaunts = [
    "¡%s, te acuso de desacato al tribunal!",
    "¡Protesta aceptada!",
    "Que eso no conste en acta.",
    "Tu apelación fue rechazada. ¡Te condeno a la tristeza!",
    "¡Orden en la sala!",
    ]
LawbotBossAreaAttackTaunt = "¡Desacato al tribunal!"


WitnessToonName = "Golpetón Agitado"
WitnessToonPrepareBattleTwo = "¡Oh no! ¡En el jurado son todos bots!\a¡Rápido, utiliza los cañones y lanza a algunos dibus hacia las sillas del jurado.\aNecesitamos %d para equilibrar la balanza."
WitnessToonNoJuror = "Oh oh, no hay dibus en el jurado. El juicio va a estar difícil."
WitnessToonOneJuror = "¡Genial! ¡Hay 1 dibu en el jurado!"
WitnessToonSomeJurors = "¡Genial! ¡Hay %d dibus en el jurado!"
WitnessToonAllJurors = "¡Fantástico! ¡Todos los miembros del jurado son dibus!"
WitnessToonPrepareBattleThree = "Rápido, toca la tribuna de testigos para conseguir pruebas.\aPulsa la tecla Borrar para lanzar las pruebas hacia los abogados, o hacia el panel de defensa."
WitnessToonCongratulations = "¡Lo lograste! ¡Gracias por esa defensa tan espectacular!\aToma, llévate estos papeles que se dejó el Juez.\aTe permitirán invocar bots de tu página de galería de bots."

WitnessToonLastPromotion = "\a¡Uau, alcanzaste el nivel %s con tu traje bot!\aLos bots no pueden ascender más alto.\aYa no puedes mejorar tu traje de bot, ¡pero puedes seguir trabajando para la Resistencia!"
WitnessToonHPBoost = "\aHiciste un gran trabajo para la Resistencia.\aEl Consejo Dibu decidió concederte otro punto de risa. ¡Felicidades!"
WitnessToonMaxed = "\aVeo que tienes un traje de bot de nivel %s. ¡Impresionante!\a¡En nombre del Consejo Dibu: gracias por regresar para defender a más dibus!"
WitnessToonBonus = "¡Fantástico! Todos los abogados están aturdidos. El peso de tus pruebas es %s veces más pesado durante %s segundos"

WitnessToonJuryWeightBonusSingular = {
  6: 'Este es un caso difícil. Sentaste a %d dibu en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
  7: 'Este es un caso muy difícil. Sentaste a %d dibu en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
  8: 'Este es el caso más difícil. Sentaste a %d dibu en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
}

WitnessToonJuryWeightBonusPlural = {
  6: 'Este es un caso difícil. Sentaste a %d dibus en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
  7: 'Este es un caso muy difícil. Sentaste a %d dibus en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
  8: 'Este es el caso más difícil. Sentaste a %d dibus en el jurado, por lo que tus pruebas tienen una bonificación de peso de %d.',
}

# Cog Summons stuff
IssueSummons = "Invocar"
SummonDlgTitle = "Iniciar una invocación bot"
SummonDlgButton1 = "Invocar a un bot"
SummonDlgButton2 = "Invocar un edificio bot"
SummonDlgButton3 = "Invocar una invasión bot"
SummonDlgSingleConf = "¿Quieres iniciar una invocación para %s?"
SummonDlgBuildingConf = "¿Quieres invocar a un %s en un edificio dibu cercano?"
SummonDlgInvasionConf = "¿Quieres invocar una invasión %s?"
SummonDlgNumLeft = "Te quedan %s."
SummonDlgDelivering = "Entregando invocaciones..."
SummonDlgSingleSuccess = "Lograste invocar al bot."
SummonDlgSingleBadLoc = "Lo siento, aquí no se permite la presencia de un bot. Prueba en otro sitio."
SummonDlgBldgSuccess = "Lograste invocar a los bots. ¡%s aceptó dejarles ocupar %s temporalmente!"
SummonDlgBldgSuccess2 = "Lograste invocar a los bots. ¡Un dependiente aceptó dejarles ocupar su edificio temporalmente!"
SummonDlgBldgBadLoc = "Lo siento, no hay edificios dibu cerca que puedan ocupar los bots."
SummonDlgInvasionSuccess = "Lograste invocar a los bots. ¡Es una invasión!"
SummonDlgInvasionBusy = "No se encontró ningún %s. Inténtalo de nuevo cuando haya terminado la invasión bot."
SummonDlgInvasionFail = "La invasión bot fracasó."
SummonDlgShopkeeper = "El dependiente "

# Polar Place cheesy effect chat phrases
PolarPlaceEffect1 = NPCToonNames[3306] + ": ¡Bienvenido al Punto Polar!"
PolarPlaceEffect2 = NPCToonNames[3306] + ": Prueba el tamaño de este."
PolarPlaceEffect3 = NPCToonNames[3306] + ": Tu nueva imagen sólo funcionará en " + lTheBrrrgh + "."

# LaserGrid game Labels
LaserGameMine = "¡Busca cráneos!"
LaserGameRoll = "Coincidencia"
LaserGameAvoid = "Evita los cráneos"
LaserGameDrag = "Arrastra en fila tres de un color"
LaserGameDefault = "Juego desconocido"

# Pinball text
#PinballHiScore = "Récord: %d %s\n"
#PinballYourBestScore = "Tu mejor puntaje: %d\n"
#PinballScore = "Puntaje: %d x %d : %d"
PinballHiScore = "Récord:     %s\n"
PinballHiScoreAbbrev = "..."
PinballYourBestScore = "Tu mejor puntaje:\n"
PinballScore = "Puntaje:            %d x %d = "
PinballScoreHolder = "%s\n"


# Gardening text
GagTreeFeather = "Árbol de bromas emplumado"
GagTreeJugglingBalls = "Árbol de bromas malabarista"
StatuaryFountain = "Fuente"
StatuaryDonald = "Estatua de Donald"
StatuaryMinnie = "Estatua de Minnie"
StatuaryMickey1 = "Estatua de Mickey"
StatuaryMickey2 = "Fuente de Mickey"
StatuaryToon = "Estatua dibu"
StatuaryToonWave = "Estatua ola dibu"
StatuaryToonVictory = "Estatua victoria dibu"
StatuaryToonCrossedArms = 'Estatua autoridad dibu'
StatuaryToonThinking = 'Estatua abrazo dibu'
StatuaryMeltingSnowman = 'Muñeco de nieve derretido'
StatuaryGardenAccelerator = "Fertilizante instantáneo"
#see GardenGlobals.py for corresponding FlowerColors
FlowerColorStrings = ['Rojo','Naranja','Morado','Azul','Rosa','Amarillo','Blanco','Verde']
#see GardenGlobals.py for PlantAttributes, keys must match
FlowerSpeciesNames = {
    49: 'Margarita',
    50: 'Tulipán',
    51: 'Clavel',
    52: 'Lirio',
    53: 'Narciso',
    54: 'Pensamiento',
    55: 'Petunia',
    56: 'Rosa',
    }
#see GardenGlobals.py for PlantAttributes, keys must match, varieties must match
FlowerFunnyNames = {
    49: ('Margarita Escolar',
         'Margarita Perezosa',
         'Margarita Veraniega',
         'Margarita Frescura',
         'Margarita Rita',
         'Margarita Pajarita',
         'Margarita Pita',
         'Marga Larga',
         ),
    50:  ('Tulipano',
          'Tulidós',
          'Tulitres',
          ),
    51:  ('Clavelito',
          'Clavel de un Día',
          'Clavel Híbrido',
          'Clavel Clavón',
          'Clavel Modelo',
          ),
    52: ('Lirio Cirio',
         'Lirio Lirondo',
         'Lirio Lírico',
         'Lirio Hepático',
         'Lirio Picante',
         'Lirio De-Lirio',
         'Lirió Mucho',
         'Lirio Martirio',
         ),
    53: ('Narciso Narcisista',
         'Narciso Omiso',
         'Nardo Narciso',
         'Cenar-Ciso',
         ),
    54: ('Pensamiento Pasajero',
         'Pensa Miento',
         'Pensamiento Impuro',
         'Pienso Momento',
         'Pensamiento Talmente'
         ),
    55: ('Petunia Petón',
         'Platunia',
         ),
    56: ("Última Rosa del Verano",
         'Rosa Lía',
         'Olo Rosa',
         'Rosa Aromática',
         'Amo Rosa',
         ),
    }
FlowerVarietyNameFormat = "%s %s"
FlowerUnknown = "????"
ShovelNameDict = {
    0 : "Hojalata",
    1 : "Bronce",
    2 : "Plata",
    3 : "Oro",
    }
WateringCanNameDict = {
    0 : "Pequeña",
    1 : "Mediana",
    2 : "Grande",
    3 : "Enorme",
    }
GardeningPlant = "Plantar"
GardeningWater = "Regar"
GardeningRemove = "Eliminar"
GardeningPick = "Agarrar"
GardeningFull = "Lleno"
GardeningSkill = "Habilidad"
GardeningWaterSkill = "Habilidad de riego"
GardeningShovelSkill = "Habilidad con la pala"
GardeningNoSkill = "No mejora de habilidad"
GardeningPlantFlower = "Plantar\nflor"
GardeningPlantTree = "Plantar\nárbol"
GardeningPlantItem = "Plantar\nobjeto"
PlantingGuiOk = "Plantar"
PlantingGuiCancel = "Cancelar"
PlantingGuiReset = "Restablecer"
GardeningChooseBeans = "Elige las golosinas que quieres plantar."
GardeningChooseBeansItem  = "Elige las golosinas / el objeto que quieras plantar."
GardeningChooseToonStatue = "Elige el dibu al que quieras hacerle una estatua."
GardenShovelLevelUp = "¡Felicidades, te ganaste una %(shovel)s! ¡Dominaste la flor de la golosina %(oldbeans)d! Para progresar, deberías recoger %(newbeans)d flores de golosina."
GardenShovelSkillLevelUp = "¡Felicidades! ¡Dominaste la flor de la golosina %(oldbeans)d! Para progresar, deberías recoger %(newbeans)d flores de golosina."
GardenShovelSkillMaxed = "¡Increíble! ¡Lograste el máximo nivel de habilidad con la pala!"

GardenWateringCanLevelUp = "¡Felicitaciones, ganaste una regadera nueva!"
GardenMiniGameWon = "¡Felicitaciones, regaste la planta!"
ShovelTin = "Pala de hojalata"
ShovelSteel = "Pala de bronce"
ShovelSilver = "Pala de plata"
ShovelGold = "Pala de oro"
WateringCanSmall = "Regadera pequeña"
WateringCanMedium = "Regadera mediana"
WateringCanLarge = "Regadera grande"
WateringCanHuge = "Regadera enorme"
#make sure it matches GardenGlobals.BeanColorLetters
BeanColorWords = ('roja', 'verde', 'naranja','morada','azul','rosa','amarilla',
                  'celeste','plateada')
PlantItWith = " Plantar con %s."
MakeSureWatered = " Asegúrate primero de que todas tus plantas están regadas."
UseFromSpecialsTab = " Úsalo desde la pestaña de objetos especiales de la página del jardín."
UseSpecial = "Usar objeto especial"
UseSpecialBadLocation = 'Eso sólo lo puedes usar en tu jardín.'
UseSpecialSuccess = '¡Conseguido! Las plantas que regaste acaban de crecer.'
ConfirmWiltedFlower = "%(plant)s se marchitó. ¿Seguro que quieres retirarla? No irá a tu cesta de flores ni mejorará tu habilidad."
ConfirmUnbloomingFlower = "%(plant)s no está floreciendo. ¿Seguro que quieres quitarla? No irá a tu cesta de flores ni mejorará tu habilidad."
ConfirmNoSkillupFlower = "¿Seguro que quieres quitar el ejemplar de %(plant)s? Irá a tu cesta de flores, pero NO mejorará tu habilidad."
ConfirmSkillupFlower = "¿Seguro que quieres quitar el ejemplar de %(plant)s? Irá a tu cesta de flores, y mejorará tu habilidad."
ConfirmMaxedSkillFlower = "¿Seguro que quieres quitar el ejemplar de %(plant)s? Irá a tu cesta de flores. NO mejorará tu habilidad, pues ya está al máximo nivel."
ConfirmBasketFull = "Tu cesta de flores está llena. Vende primero algunas flores."
ConfirmRemoveTree = "¿Seguro que quieres quitar el árbol %(tree)s?"
ConfirmWontBeAbleToHarvest = " Si quitas este árbol, no podrás recolectar bromas de los árboles de mayor nivel."
ConfirmRemoveStatuary = "¿Seguro que quieres eliminar permanentemente el objeto %(item)s?"
ResultPlantedSomething  = "¡Felicitaciones! Acabas de plantar un ejemplar de %s."
ResultPlantedSomethingAn  = "¡Felicitaciones! Acabas de plantar un ejemplar de %s."
ResultPlantedNothing = "No funcionó. Prueba con una combinación de golosinas distinta."

GardenGagTree = " Árbol de bromas"
GardenUberGag = "Súper broma"

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
            retval = "%d %s golosinas" % (len(beanTuple),
                                           BeanColorWords[beanTuple[0]])
        else:
            retval = "a %s golosina" % BeanColorWords[beanTuple[0]]
    else:
        retval += 'un'
        maxBeans = len(beanTuple)
        for index in range(maxBeans):
            if index == maxBeans - 1:
                retval += " y %s golosina" % BeanColorWords[beanTuple[index]]
            elif index == 0:
                retval += " %s" % BeanColorWords[beanTuple[index]]
            else:
                retval += ", %s" % BeanColorWords[beanTuple[index]]

    return retval

GardenTextMagicBeans = "Golosinas mágicas"
GardenTextMagicBeansB = "Otras golosinas"
GardenSpecialDiscription = "Este texto explica cómo utilizar un objeto especial de jardín determinado"
GardenSpecialDiscriptionB = "Este texto explica cómo utilizar un objeto especial de jardín determinado."
GardenTrophyAwarded = "¡Uau! Recogiste %s de %s flores. ¡Eso se merece un trofeo y una aumento en el risómetro!"
GardenTrophyNameDict = {
    0 : "Carretilla",
    1 : "Palas",
    2 : "Flor",
    3 : "Regadera",
    4 : "Tiburón",
    5 : "Pez espada",
    6 : "Ballena asesina",
    }
SkillTooLow = "Habilidad\ndemasiando baja"
NoGarden = "Ningún\njardín"

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
TravelGameTitle = "Circuito del tranvía"
TravelGameInstructions = "Haz clic arriba o abajo para definir tu número de votos. Haz clic en el botón del voto para canjearlo. Alcanza tu objetivo secreto para recibir bonificaciones de golosinas. Consigue más votos logrando buenos resultados en los otros juegos."
TravelGameRemainingVotes = "Votos restantes:"
TravelGameUse = "Usar"
TravelGameVotesWithPeriod = "votos."
TravelGameVotesToGo = "votos que faltan"
TravelGameVoteToGo = "votos que faltan"
TravelGameUp = "ARRIBA."
TravelGameDown = "ABAJO."
TravelGameVoteWithExclamation = "¡Vota!"
TravelGameWaitingChoices = "Esperando a que voten los otros jugadores..."
# cross the bridge later when the first choice is different for each node,
# e.g. NorthWest, NorthEast, etc.
TravelGameDirections = ['ARRIBA', 'ABAJO']
TravelGameTotals = 'Totales '
TravelGameReasonVotesPlural = 'El tranvía se está moviendo hacia %(dir)s, ganando por %(numVotes)d votos.'
TravelGameReasonVotesSingular = 'El tranvía se está moviendo hacia %(dir)s, ganando por %(numVotes)d voto.'
TravelGameReasonPlace = '%(name)s desempata. El tranvía se está moviendo hacia %(dir)s.'
TravelGameReasonRandom = 'El tranvía se está moviendo al azar hacia %(dir)s.'
TravelGameOneToonVote =   "%(name)s utilizó %(numVotes)s votos para ir hacia %(dir)s\n"
TravelGameBonusBeans = "%(numBeans)d golosinas"
TravelGamePlaying = 'A continuación, el juego del tranvía %(game)s.'
TravelGameGotBonus = '¡%(name)s tiene una bonificación de %(numBeans)s golosinas!'
TravelGameNoOneGotBonus = "Nadie alcanzó su objetivo secreto. Cada uno recibe 1 golosina."
TravelGameConvertingVotesToBeans = "Transformando votos en golosinas..."
TravelGameGoingBackToShop ="Queda 1 jugador. Accediendo a la tienda de bromas de Goofy."

PairingGameTitle = "Juego de memoria dibu"
PairingGameInstructions = "Pulsa la tecla Borrar para dar vuelta una carta. Encuentra 2 cartas iguales para ganar un punto. Si haces que coincida la que tiene el brillo de bonificación, ganarás un punto extra. Cuantas menos cartas des vuelta, más puntos ganarás."
PairingGameInstructionsMulti = "Pulsa la tecla Borrar para dar vuelta una carta. Pulsa Control para decirle a otro jugador que de vuelta una carta. Encuentra 2 cartas iguales para conseguir un punto. Si haces que coincida la que tiene el brillo de bonificación, ganarás un punto extra. Cuantas menos cartas des vuelta, más puntos ganarás."
PairingGamePerfect = '¡¡PERFECTO!!'
PairingGameFlips = 'Giros:'
PairingGamePoints = 'Puntos:'

TrolleyHolidayStart = "¡Está a punto de comenzar el Circuito del tranvía! Para jugar, súbete cualquier tranvía con 2 dibus o más."
TrolleyHolidayOngoing = "¡Bienvenido! El Circuito del tranvía ya comenzó."
TrolleyHolidayEnd = "Eso es todo por hoy en el Circuito del tranvía. ¡Hasta la semana que viene!"

TrolleyWeekendStart = "¡El fin de semana del Circuito del tranvía está a punto de comenzar! Para jugar, súbete a cualquier tranvía con 2 dibus o más."
TrolleyWeekendEnd = "Eso es todo en el fin de semana del Circuito del tranvía."

VineGameTitle = "Parras de la selva"
VineGameInstructions = "Llega a tiempo a la viña que está a la derecha. Pulsa arriba o abajo para subir por la viña. Pulsa izquierda o derecha para cambiar de dirección y saltar. Cuanto más abajo de la viña estés, más rápido saltarás. Si puedes, recoge las bananas pero esquiva a los murciélagos y las arañas."

# Make sure the golf text matches up with GolfGlobals.py
GolfCourseNames = {
    0: "Para por el par",
    1: "El hoyo del bollo",
    2: "El palo palomino"
    }

GolfHoleNames = {
    0: 'Tres bajo par-tida',
    1: 'Caddie día algo nuevo',
    2: 'Alcance en trance',
    3: 'Vista en verde',
    4: 'Recorrido barrido',
    5: 'Put Trefacción',
    6: 'Lanza balanza',
    7: 'Para Tee',
    8: 'Arroyo del hoyo',
    9: 'Rueda y ruega',
    10: 'Noches de Bogey',
    11: 'Saque mate',
    12: '¡Olla al hoyo!',
    13: 'El tope del topo',
    14: 'Pali troque',
    15: 'Swing',
    16: 'Hoyo seguido',
    17: 'Segunda ala',
    18: 'Tres bajo par-tida-2',
    19: 'Caddie día algo nuevo-2',
    20: 'Alcance en trance-2',
    21: 'Vista en verde-2',
    22: 'Recorrido barrido-2',
    23: 'Put trefacción-2',
    24: 'Lanza balanza-2',
    25: 'Para Tee-2',
    26: 'Arroyo del hoyo-2',
    27: 'Rueda y ruega-2',
    28: 'Noches de Bogey-2',
    29: 'Saque mate-2',
    30: '¡Olla al hoyo!-2',
    31: 'El tope del topo-2',
    32: 'Pali troque-2',
    33: 'Swing-2',
    34: 'Hoyo seguido-2',
    35: 'Segunda ala-2',
    }

GolfHoleInOne = "Hoyo en uno"
GolfCondor = "Cóndor" # four Under Par
GolfAlbatross = "Albatros" # three under par
GolfEagle = "Águila" # two under par
GolfBirdie = "Pájaro" # one under par
GolfPar = "Par"
GolfBogey = "Bogey" # one over par
GolfDoubleBogey = "Bogey doble" # two over par
GolfTripleBogey = "Bogey triple" # three over par

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

CoursesCompleted = "Recorridos completados"
CoursesUnderPar = "Recorridos bajo par"
HoleInOneShots = "Tiros de hoyo en uno"
EagleOrBetterShots = "Tiros águila o mejores"
BirdieOrBetterShots = "Tiros pájaro o mejores"
ParOrBetterShots = "Tiros par o mejores"
MultiPlayerCoursesCompleted = "Recorridos multijugador completados"
TwoPlayerWins = "Victorias dos jugadores"
ThreePlayerWins = "Victorias tres jugadores"
FourPlayerWins = "Victorias cuatro jugadores"
CourseZeroWins = GolfCourseNames[0] + " Victorias"
CourseOneWins = GolfCourseNames[1] + " Victorias"
CourseTwoWins = GolfCourseNames[2] + " Victorias"

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
    str(GolfGlobals.TrophiesPerCup) + " Trofeos ganados",
    str(GolfGlobals.TrophiesPerCup * 2) + " Trofeos ganados",
    str(GolfGlobals.TrophiesPerCup * 3) + " Trofeos ganados",
]

GolfAvReceivesHoleBest = "¡%(name)s logró un nuevo récord de hoyo en %(hole)s!"
GolfAvReceivesCourseBest = "%(name)s logró un nuevo récord de recorrido en %(course)s!"
GolfAvReceivesCup = "¡%(name)s recibe la copa %(cup)s! ¡Aumento en el risómetro!"
GolfAvReceivesTrophy = "¡%(name)s recibe el trofeo %(award)s!"
GolfRanking = "Ranking: \n"
GolfPowerBarText = "%(power)s%%"
GolfChooseTeeInstructions = "Pulsa izquierda o derecha para cambiar el punto de tee.\nPulsa Control para seleccionar."
GolfWarningMustSwing = "Advertencia: debes pulsar Control en tu próximo swing."
GolfAimInstructions = "Pulsa izquierda o derecha para apuntar.\nPulsa y mantén Control pulsado para hacer el swing."
GolferExited = "%s abandonó el campo de golf."
GolfPowerReminder = "Mantén Control pulsado más tiempo para\nque la pelota llegue más lejos"


# GolfScoreBoard.py
GolfPar = "Par"
GolfHole = "Hoyo"
GolfTotal = "Total"
GolfExitCourse = "Salir del recorrido"
GolfUnknownPlayer = "???"

# GolfPage.py
GolfPageTitle = "Golf"
GolfPageTitleCustomize = "Personalizador de golf"
GolfPageTitleRecords = "Récords personales"
GolfPageTitleTrophy = "Trofeos de golf"
GolfPageCustomizeTab = "Personalizar"
GolfPageRecordsTab = "Récords"
GolfPageTrophyTab = "Trofeo"
GolfPageTickets = "Boletos : "
GolfPageConfirmDelete = "¿Borrar accesorio?"
GolfTrophyTextDisplay = "Trofeo %(number)s : %(desc)s"
GolfCupTextDisplay = "Copa %(number)s : %(desc)s"
GolfCurrentHistory = "%(historyDesc)s actual : %(num)s"
GolfTieBreakWinner = "¡%(name)s gana el desempate aleatorio!"
GolfSeconds = " -  %(time).2f segundos"
GolfTimeTieBreakWinner = "¡¡¡%(name)s gana el desempate de tiempo total de puntería!!!"



RoamingTrialerWeekendStart = "¡Empieza el Tour Toontown! ¡Los jugadores libres ya pueden acceder a cualquier barrio!"
RoamingTrialerWeekendOngoing = "¡Bienvenido al Tour Toontown! ¡Los jugadores libres ya puedne acceder a cualquier barrio!"
RoamingTrialerWeekendEnd = "Eso es todo en Tour Toontown."

# change double if ToontownBattleGlobals.getMoreXpHolidayMultiplier() changes
MoreXpHolidayStart = "¡Buenas noticias! Ya comenzó la experiencia por el doble de bromas Test Toon."
MoreXpHolidayOngoing = "¡Bienvenido! La experiencia exclusiva por el doble de bromas Test Toon está en marcha."
MoreXpHolidayEnd = "La experiencia exclusiva por el doble de bromas Test Toon ya finalizó. ¡Gracias por ayudarnos con los tests!"

JellybeanDayHolidayStart = "¡Es el Día de la Golosina! ¡Consigue el doble de golosinas en las fiestas!"
JellybeanDayHolidayEnd = "Eso es todo en el Día de la Golosina. Hasta el año que viene."
PartyRewardDoubledJellybean = "¡El doble de golosinas!"

GrandPrixWeekendHolidayStart = "¡Empieza el fin de semana Grand Prix en el Estadio de Goofy! Los jugadores libres y los pagados acumulan la mayor cantidad de puntos en tres carreras consecutivas."
GrandPrixWeekendHolidayEnd = "Eso es todo en el fin de semana Grand Prix. Hasta el año que viene."

LogoutForced = "Hiciste algo indebido\n y serás desconectado automáticamente;\n además, es posible que tu cuenta sea congelada.\n Sal a dar un paseo, será divertido."

# DistributedCountryClub.py
CountryClubToonEnterElevator = "%s \nsaltó al carrito de golf."
CountryClubBossConfrontedMsg = "¡%s se está peleando con el presidente del club!"

# DistributedElevatorFSM.py
ElevatorBlockedRoom = "Primero hay que superar todos los desafíos."

# DistributedMolefield.py
MolesLeft = "Topos restantes: %d"
MolesInstruction = "¡Pisotón de topo!\n¡Salta sobre los topos rojos!"
MolesFinished = "¡Pisotón de topo conseguido!"
MolesRestarted = "¡Fallo en el Pisotón! Reiniciando..."

# DistributedGolfGreenGame.py
BustACogInstruction = "¡Quita la bola bot!"
BustACogExit = "Salir por ahora"
BustACogHowto = "Cómo se juega"
BustACogFailure = "¡Se acabó el tiempo!"
BustACogSuccess = "¡Conseguido!"

# bossbot golf green games
GolfGreenGameScoreString = "Instancias de ingenio restantes: %s"
GolfGreenGamePlayerScore = "Resuelto %s"
GolfGreenGameBonusGag = "¡Ganaste %s!"
GolfGreenGameGotHelp = "¡%s resolvió una instancia de ingenio!"

GolfGreenGameDirections = "Dispara bolas utilizando el mouse\n\n\nAl juntar tres del mismo color, las bolas caerán\n\n\nQuita todas las bolas bot del tablero"

# DistributedMaze.py
enterHedgeMaze = "¡Compite a través del Laberinto\n para conseguir bonificaciones de risa!"
toonFinishedHedgeMaze = "¡%s \n  terminó en el %s puesto!"
hedgeMazePlaces = ["primer","segundo","tercer","cuarto"]
mazeLabel = "¡Laberinto!"

# Boarding Group
BoardingPartyReadme = '¿Grupo de embarque?'
BoardingGroupHide = 'Ocultar'
BoardingGroupShow = 'Mostrar grupo de embarque'
BoardingPartyInform = 'Crea un grupo de embarque para el ascensor haciendo clic sobre otro dibu e invitándolo.\nEn esta área, los grupos de embarque no pueden tener más de %s dibus.'
BoardingPartyTitle = 'Grupo de embarque'
QuitBoardingPartyLeader = 'Disolver'
QuitBoardingPartyNonLeader = 'Abandonar'
QuitBoardingPartyConfirm = '¿Seguro que quieres salir de este grupo de embarque?'
BoardcodeMissing = 'Algo falló; inténtalo de nuevo más tarde.'
BoardcodeMinLaffLeader = 'Tu grupo no puede embarcar porque tienes menos de %s puntos de risa.'
BoardcodeMinLaffNonLeaderSingular = 'Tu grupo no puede embarcar porque %s tiene menos de %s puntos de risa.'
BoardcodeMinLaffNonLeaderPlural = 'Tu grupo no puede embarcar porque %s tienen menos de %s puntos de risa.'
BoardcodePromotionLeader = 'Tu grupo no puede embarcar porque no tienes suficientes méritos de ascenso.'
BoardcodePromotionNonLeaderSingular = 'Tu grupo no puede embarcar porque %s no tiene suficientes méritos de ascenso.'
BoardcodePromotionNonLeaderPlural = 'Tu grupo no puede embarcar porque %s no tienen suficientes méritos de ascenso.'
BoardcodeSpace = 'Tu grupo no puede embarcar porque no hay espacio suficiente.'
BoardcodeBattleLeader = 'Tu grupo no puede embarcar porque estás en una batalla.'
BoardcodeBattleNonLeaderSingular = 'Tu grupo no puede embarcar porque %s está en una batalla.'
BoardcodeBattleNonLeaderPlural = 'Tu grupo no puede embarcar porque %s están en una batalla.'
BoardingInviteMinLaffInviter = 'Necesitas %s puntos de risa para poder ser miembro de este grupo de embarque.'
BoardingInviteMinLaffInvitee = '%s necesita %s puntos de risa para poder ser miembro de este grupo de embarque.'
BoardingInvitePromotionInviter = 'Necesitas conseguir un ascenso para poder ser miembro de este grupo de embarque.'
BoardingInvitePromotionInvitee = '%s necesita conseguir un ascenso para poder ser miembro de este grupo de embarque.'
BoardingInviteNotPaidInvitee = '%s necesita ser miembro pagado para formar parte de tu grupo de embarque.'
BoardingInviteeInDiffGroup = '%s ya está en otro grupo de embarque.'
BoardingInviteeInKickOutList = '%s fue expulsado por tu líder. El líder es el único que puede volver a invitar a miembros expulsados'
BoardingInviteePendingIvite = '%s tiene una invitación pendiente; inténtalo de nuevo más tarde.'
BoardingInviteeInElevator = '%s está ocupado; inténtalo de nuevo más tarde.'
BoardingInviteGroupFull = 'Tu grupo de embarque ya está lleno.'
BoardingAlreadyInGroup = 'No puedes aceptar esta invitación porque formas parte de otro grupo de embarque.'
BoardingGroupAlreadyFull = 'No puedes aceptar esta invitación porque el grupo ya está lleno.'
BoardingKickOutConfirm = '¿Seguro que quieres expulsar a %s?'
BoardingPendingInvite = 'Primero tienes que resolver la\n invitación pendiente.'
BoardingCannotLeaveZone = 'No puedes salir de esta zona porque formas parte de un grupo de embarque.'
BoardingInviteeMessage = "%s quiere que te unas a su grupo de embarque."
BoardingInvitingMessage = "Invitando a %s a tu grupo de embarque."
BoardingInvitationRejected = "%s rechazó unirse a tu grupo de embarque."
BoardingMessageKickedOut = "Fuiste expulsado del grupo de embarque."
BoardingMessageInvited = "%s invitó a %s al grupo de embarque."
BoardingMessageLeftGroup = "%s abandonó el grupo de embarque."
BoardingMessageGroupDissolved = "Tu grupo de embarque fue disuelto por el líder del grupo."
BoardingMessageGroupDisbandedGeneric = "Tu grupo de embarque fue disuelto."
BoardingMessageInvitationFailed = "%s intentó invitarte a su grupo de embarque."
BoardingMessageGroupFull = "%s intentó aceptar tu invitación, pero tu grupo estaba lleno."
BoardingGo = 'IR'
BoardingCancelGo = 'Haz clic otra vez\npara cancelar Ir'
And = 'y'
BoardingGoingTo = 'En dirección a:'
BoardingTimeWarning = 'Embarcando al ascensor en '
BoardingMore = 'más'
BoardingGoShow = 'En dirección a\n%s en '
BoardingGoPreShow = 'Confirmando...'

# DistributedBossbotBoss.py
BossbotBossName = "Director general"
BossbotRTWelcome = "Tus dibus necesitarán disfraces diferentes."
BossbotRTRemoveSuit = "Primero hay que quitarse los trajes de bot..."
BossbotRTFightWaiter = "y después luchar contra estos camareros."
BossbotRTWearWaiter = "¡Buen trabajo! Ahora, a colocarse la ropa de los camareros."
BossbotBossPreTwo1 = "¿A qué se debe tanta tardanza?"
BossbotBossPreTwo2 = "¡Vamos, sírvanme el banquete!"
BossbotRTServeFood1 = "Jeje, hay que servir la comida que coloco en estas cintas transportadoras."
BossbotRTServeFood2 = "Si sirves a un bot tres veces seguidas, explotará."
BossbotResistanceToonName = "El Viejo Aletas"
BossbotPhase3Speech1 = "¡¿Qué está pasando aquí?!"
BossbotPhase3Speech2 = "¡Estos camareros son dibus!"
BossbotPhase3Speech3 = "¡¡¡A ellos!!!"
BossbotPhase4Speech1 = "Grrrr. Si necesitas que algo se haga bien..."
BossbotPhase4Speech2 = "Tienes que hacerlo tú mismo."
BossbotRTPhase4Speech1 = "¡Buen trabajo! Ahora, a mojar al director general con el agua de las mesas..."
BossbotRTPhase4Speech2 = "o se pueden usar las bolas de golf para frenarle."
BossbotPitcherLeave = "Dejar botella"
BossbotPitcherLeaving = "Dejando botella..."
BossbotPitcherAdvice = "Usa las teclas izquierda y derecha para girar.\nMantén Ctrl pulsado para aumentar la potencia.\nSuelta Ctrl para disparar."
BossbotGolfSpotLeave = "Dejar bola de golf"
BossbotGolfSpotLeaving = "Dejando bola de golf..."
BossbotGolfSpotAdvice = "Usa las teclas izquierda y derecha para girar.\nCtrl para disparar."
BossbotRewardSpeech1 = "¡No! Al presidente no le va a gustar esto."
BossbotRewardSpeech2 = "¡¡¡Arrrggghhh!!!"
BossbotRTCongratulations = "¡Lo lograste! ¡Bajaste de categoría al director general!\aToma estos papeles rosas que se dejó el director general.\aCon ellos, podrás disparar contra los bots en batalla."""
BossbotRTLastPromotion = "\a¡Uau, alcanzaste el nivel %s con tu traje bot!\aLos bots no pueden ascender más de nivel.\aYa no puedes mejorar tu traje bot, ¡pero puedes seguir trabajando para la Resistencia!"
BossbotRTHPBoost = "\aHiciste un gran trabajo para la Resistencia.\aEl Consejo Dibu decidió concederte otro punto de risa. ¡Felicitaciones!"
BossbotRTMaxed = "\aVeo que tienes un traje de bot de nivel %s. ¡Impresionante!\aEn nombre del Consejo Dibu, ¡gracias por regresar a defender a más dibus!"
GolfAreaAttackTaunt = "¡Adelante!"
OvertimeAttackTaunts = [ "Es hora de reorganizarse.",
                        "Es hora de reducir el personal."]

#ElevatorDestination Names
ElevatorBossBotBoss = "Batalla del director general"
ElevatorBossBotCourse0 = "Los tres delanteros"
ElevatorBossBotCourse1 = "Los seis centrales"
ElevatorBossBotCourse2 = "Los nueve traseros"
ElevatorCashBotBoss = "Batalla del director financiero"
ElevatorCashBotMint0 = "Fabrica de moneditas"
ElevatorCashBotMint1 = "Fabrica de dólares"
ElevatorCashBotMint2 = "Fabrica de lingotes"
ElevatorSellBotBoss = "Batalla del vicepresidente"
ElevatorSellBotFactory0 = "Entrada delantera"
ElevatorSellBotFactory1 = "Entrada de servicio"
ElevatorLawBotBoss = "Batalla del Juez"
ElevatorLawBotCourse0 = "Oficina A"
ElevatorLawBotCourse1 = "Oficina B"
ElevatorLawBotCourse2 = "Oficina C"
ElevatorLawBotCourse3 = "Oficina D"



# CatalogNameTagItem.py
DaysToGo = "Espera\n%s días"

# DistributedIceGame.py
IceGameTitle = "Tobogán de hielo"
IceGameInstructions = "Acércate todo lo que puedas al centro antes de que finalice la segunda ronda. Utiliza las teclas de flecha para cambiar la dirección y la fuerza. Pulsa Ctrl para lanzar a tu dibu. ¡Conseguirás más puntos si golpeas los barriles y evitas el TNT!"
IceGameInstructionsNoTnt = "Acércate todo lo que puedas al centro antes de que finalice la segunda ronda. Utiliza las teclas de flecha para cambiar la dirección y la fuerza. Pulsa Ctrl para lanzar a tu dibu. Golpea barriles y conseguirás puntos extra."
IceGameWaitingForPlayersToFinishMove = "Esperando a otros jugadores..."
IceGameWaitingForAISync = "Esperando a otros jugadores..."
IceGameInfo= "Partida %(curMatch)d/%(numMatch)d, Ronda %(curRound)d/%(numRound)d"
IceGameControlKeyWarning="¡No olvides pulsar la tecla Ctrl!"


#DistributedPicnicTable.py
PicnicTableJoinButton = "Unirse"
PicnicTableObserveButton = "Observar"
PicnicTableCancelButton = "Cancelar"
PicnicTableTutorial = "Cómo se juega"
PicnicTableMenuTutorial = "¿Qué juego quieres aprender?"
PicnicTableMenuSelect = "¿A qué juego quieres jugar?"

#DistributedChineseCheckers.py
ChineseCheckersGetUpButton = "Levantarse"
ChineseCheckersStartButton = "Empezar a jugar"
ChineseCheckersQuitButton = "Abandonar el juego"
ChineseCheckersIts = "Es "

ChineseCheckersYourTurn = "Tu turno"
ChineseCheckersGreenTurn = "Turno de las verdes"
ChineseCheckersYellowTurn = "Turno de las amarillas"
ChineseCheckersPurpleTurn = "Turno de las moradas"
ChineseCheckersBlueTurn = "Turno de las azules"
ChineseCheckersPinkTurn = "Turno de las rosas"
ChineseCheckersRedTurn = "Turno de las rojas"

ChineseCheckersColorG = "Eres las verdes"
ChineseCheckersColorY = "Eres las amarillas"
ChineseCheckersColorP = "Eres las moradas"
ChineseCheckersColorB = "Eres las azules"
ChineseCheckersColorPink = "Eres las rosas"
ChineseCheckersColorR = "Eres las rojas"
ChineseCheckersColorO = "Estás de observador"

ChineseCheckersYouWon = "¡Acabas de ganar una partida de Damas chinas!"
ChineseCheckers = "Damas chinas."
ChineseCheckersGameOf = " acaba de ganar una partida de "

#GameTutorials.py
ChineseTutorialTitle1 = "Objetivo"
ChineseTutorialTitle2 = "Cómo se juega"
ChineseTutorialPrev = "Página anterior"
ChineseTutorialNext = "Página siguiente"
ChineseTutorialDone = "Completado"
ChinesePage1 = "El objetivo de las Damas chinas es ser el primero en mover todas tus canicas desde tu triángulo a través del tablero hasta el triángulo opuesto al tuyo. ¡Gana el primer jugador que lo logre!"
ChinesePage2 = "Por turnos, los jugadores van moviendo cualquier canica de su color. Las canicas pueden moverse a cualquier hoyo vacío contiguo o pueden saltar sobre otras canicas. Los saltos deben hacerse siempre sobre una canica y terminar en un hoyo vacío. ¡Se pueden hacer saltos en cadena para avanzar más!"

CheckersPage1 = "El objetivo de las Damas es dejar al contrario sin movimientos. Para ello, puedes capturar todas sus fichas o bloquearle el paso de manera que no pueda mover."
CheckersPage2 = "Por turnos, los jugadores van moviendo cualquier ficha de su color. Las fichas se mueven de a un casillero en diagonal y hacia delante. Una ficha sólo podrá moverse a un casillero que no esté ocupado por otra ficha. Las reinas se rigen por las mismas reglas pero también se mueven hacia atrás."
CheckersPage3 = "Para capturar una ficha contraria, tu ficha deberá saltar sobre ella en diagonal y colocarse en el casillero vacío siguiente. Si tienes la posibilidad de saltar durante tu turno, estás obligado a hacerlo. Puedes hacer saltos en cadena siempre que los hagas con la misma ficha y en la misma dirección."
CheckersPage4 = "Una ficha se convierte en reina cuando llega a la última fila del tablero. Cuando una ficha se convierte en reina no podrá seguir saltando hasta el siguiente turno. Además, las reinas pueden moverse en cualquier dirección y pueden cambiar de dirección durante los saltos."



#DistributedCheckers.py
CheckersGetUpButton = "Levantarse"
CheckersStartButton = "Empezar partida"
CheckersQuitButton = "Abandonar partida"

CheckersIts = "It's "
CheckersYourTurn = "Tu turno"
CheckersWhiteTurn = "Turno de las blancas"
CheckersBlackTurn = "Turno de las negras"

CheckersColorWhite = "Eres las blancas"
CheckersColorBlack = "Eres las negras"
CheckersObserver = "Estás de observador"
RegularCheckers = "Damas."
RegularCheckersGameOf = " ganó una partida de "
RegularCheckersYouWon = "¡Ganaste una partida de Damas!"

MailNotifyNewItems = "¡Tienes correo!"
MailNewMailButton = "Correo"
MailSimpleMail = "Nota"
MailFromTag = "Nota de: %s"

# MailboxScreen.py
InviteInvitation = "la invitación"
InviteAcceptInvalidError = "La invitación ya no es válida."
InviteAcceptPartyInvalid = "La fiesta fue cancelada."
InviteAcceptAllOk = "El anfitrión fue informado de tu respuesta."
InviteRejectAllOk = "El anfitrión fue informado de que rechazaste la invitación."


# Note Months is 1 based, to correspond to datetime
Months = {
 1: "ENERO",
 2: "FEBRERO",
 3: "MARZO",
 4: "ABRIL",
 5: "MAYO",
 6: "JUNIO",
 7: "JULIO",
 8: "AGOSTO",
 9: "SEPTIEMBRE",
10: "OCTUBRE",
11: "NOVIEMBRE",
12: "DICIEMBRE"
}

# Note 0 for Monday to match datetime
DayNames = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
DayNamesAbbrev = ("LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM")

# numbers must match holiday ids in ToontownGlobals
HolidayNamesInCalendar = {
    1: ("Fuegos artificiales de verano", "¡Celebra el verano con un espectáculo de fuegos artificiales por hora en todos los dibuparques!"),
    2: ("Fuegos artificiales de Año Nuevo", "¡Feliz Año Nuevo! ¡Disfruta de un espectáculo de fuegos artificiales por hora en todos los dibuparques!"),
    3: ("Invasión Chupasangres", "¡Feliz día de Halloween! ¡Evita que los bots chupasangres invadan Toontown!"),
    4: ("Adornos de invierno", "¡Celebra las vacaciones de invierno con árboles y luces dibufantásticas!"),
    5: ("Invasión esquelebot", "¡Impide que los esquelebots invadan Toontown!"),
    6: ("Invasión del Sr. Hollywood", "Impide que los bots del Sr. Hollywood invadan Toontown!"),
    7: ("Bingo de peces", "¡Miércoles de bingo de peces! En el estanque, todos trabajan juntos para completar la tarjeta antes de que se agote el tiempo."),
    8: ("Elección especies dibu", "¡Vota por la nueva especie de dibu! ¿Será una cabra? ¿Será un cerdo?"),
    9: ("Día del gato negro", "¡Feliz día de Halloween! Crea un dibufantástico dibu gato negro, ¡sólo por hoy!"),
   13: ("Truco o trato", "¡Feliz día de Halloween! ¡Pasea por todo Toontown haciendo truco o trato y consigue una calabaza de Halloween genial!"),
   14: ("Grand Prix", "¡Lunes Grand Prix en el Estadio de Goofy! ¡Para ganar, consigue más puntos que nadie en tres carreras consecutivas!"),
   16: ("Fin de semana Grand Prix", "¡Jugadores libres y pagados compiten en las carreras del circuito del Estadio de Goofy!"),
   17: ("Circuito del tranvía", "¡Jueves de Circuito del tranvía! Para jugar, súbete a cualquier tranvía con dos o más dibus."),
   19: ("Sábados absurdos", "¡El sábado es un día loco, pues se celebra durante todo el día el bingo de peces, el Grand Prix y el Circuito del tranvía!"),
   24: ("Idus de marzo", "¡Cuidado con los idus de marzo! ¡Impide que los bots apuñalaespaldas invadan Toontown!"),
   26: ("Adornos de Halloween", "¡Celebra Halloween transformando Toontown con árboles y luces escalofriantes!"),
   28: ("Invasión de invierno", "¡Los vendebots andan sueltos, esparciendo sus frías tácticas de venta!"),
   33: ("Sorpresa vendebot 1", "¡Sorpresa vendebot! ¡Impide que los bots aprovechados invadan Toontown!"),
   34: ("Sorpresa vendebot 2", "¡Sorpresa vendebot! ¡Impide que los bots fanfarrones invadan Toontown!"),
   35: ("Sorpresa vendebot 3", "¡Sorpresa vendebot! ¡Impide que los bots efusivos invadan Toontown!"),
   36: ("Sorpresa vendebot 4", "¡Sorpresa vendebot! ¡Impide que los bots mandamases invadan Toontown!"),
   37: ("Enigma chequebot 1", "Un enigma chequebot. ¡Impide que los bots modeditas invadan Toontown!"),
   38: ("Enigma chequebot 2", "Un enigma chequebot. ¡Impide que los bots cacomatracos invadan Toontown!"),
   39: ("Enigma chequebot 3", "Un enigma chequebot. ¡Impide que los bots agarrados invadan Toontown!"),
   40: ("Enigma chequebot 4", "Un enigma chequebot. ¡Impide que los bots contables invadan Toontown!"),
   41: ("Táctica abogabot 1", "La táctica abogabot. ¡Impide que los bots caraduras invadan Toontown!"),
   42: ("Táctica abogabot 2", "La táctica abogabot. ¡Impide que los bots embaucadores invadan Toontown!"),
   43: ("Táctica abogabot 3", "La táctica abogabot. ¡Impide que los bots persigueambulancias invadan Toontown!"),
   44: ("Táctica abogabot 4", "La táctica abogabot. ¡Impide que los bots apuñalaespaldas invadan Toontown!"),
   45: ("Problema con jefebots 1", "El problema con los jefebots. ¡Impide que los bots secuaces invadan Toontown!"),
   46: ("Problema con jefebots 2", "El problema con los jefebots. ¡Impide que los bots chupatintas invadan Toontown!"),
   47: ("Problema con jefebots 3", "El problema con los jefebots. ¡Impide que los microgerentes invadan Toontown!"),
   48: ("Problema con jefebots 4", "El problema con los jefebots. ¡Impide que los bots reguladores de empleo invadan Toontown!"),
   49: ("Día de la Golosina", "¡Celebra el día de la golosina recibiendo como recompensa el doble de golosinas en las fiestas!"),
   53: ("Invasión de los aprovechados", "¡Impide que los bots aprovechados invadan Toontown!"),
   54: ("Invasión de los agarrados", "¡Impide que los bots agarrados invadan Toontown!"),
   55: ("Invasión de los embaucadores", "¡Impide que los bots embaucadores invadan Toontown!"),
   56: ("Invasión de los reguladores de empleo", "¡Impide que los bots reguladores de empleo invadan Toontown!"),    

    }

UnknownHoliday = "Celebración desconocida %d"
HolidayFormat = "%m/%d "

# parties/ToontownTimeManager.py
TimeZone = "US/Pacific"
