import string
from LocalizerCastillianProperty import *

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
ExtraKeySanityCheck = "Ignore me"

InterfaceFont = 'phase_3/models/fonts/ImpressBT.ttf'
SuitFont = 'phase_3/models/fonts/vtRemingtonPortable.ttf'
SignFont = 'phase_3/models/fonts/MickeyFont'
MinnieFont = 'phase_3/models/fonts/MinnieFont'
BuildingNametagFont = 'phase_3/models/fonts/MickeyFont'
BuildingNametagShadow = None

# common names
Mickey = "Mickey"
Minnie = "Minnie"
Donald = "Donald"
Daisy  = "Daisy"
Goofy  = "Goofy"
Pluto  = "Pluto"
Flippy = "Flipi"

# common locations
lTheBrrrgh = 'The Brrrgh'
lDaisyGardens = 'Daisy Gardens'
lDonaldsDock = "Donald's Dock"
lDonaldsDreamland = "Donald's Dreamland"
lMinniesMelodyland = "Minnie's Melodyland"
lToontownCentral = 'Toontown Central'

# common strings
lCancel = 'Cancel'
lClose = 'Close'
lOK = 'OK'
lNext = 'Next'
lNo = 'No'
lQuit = 'Quit'
lYes = 'Yes'

lHQOfficerF = 'HQ Officer'
lHQOfficerM = 'HQ Officer'

MickeyMouse = "Mickey Mouse"

AIStartDefaultDistrict = "Villaboba"

Cog  = "Bot"
Cogs = "Bots"
ACog = "un Bot"
TheCogs = "Los bots"
Skeleton = "esquelebot"
SkeletonP = "esquelebots"
ASkeleton = "un esquelebot"
Foreman = "capataz"
ForemanP = "capataces"
AForeman = "un capataz"
CogVP = Cog + " VIP"
CogVPs = "bots VIPS"
ACogVP = ACog + " un VIP"

# Quests.py
TheFish = "los peces"
AFish = "un pez"
Level = "nivel"
QuestsCompleteString = "Completada"
QuestsNotChosenString = "No está elegida"
Period = "."

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
                         "Greetings _avName_!",
                         )
QuestsDefaultIncomplete = ("¿Qué tal va la tarea, _avName_?",
                           "¡Parece que todavía te queda trabajo por hacer con esa tarea!",
                           "¡Sigue trabajando así, _avName_!",
                           "Intenta terminar la tarea.  ¡Sé que puedes hacerlo!",
                           "¡Sigue intentando terminar la tarea, contamos contigo!",
                           "¡Sigue trabajando en tu dibutarea!",
                           )
QuestsDefaultIncompleteProgress = ("Has venido al lugar adecuado, pero antes tienes que terminar la dibutarea.",
                                   "Cuando hayas terminado con la dibutarea, vuelve por aquí.",
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
QuestsDefaultLeaving = ("¡Chao!",
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
                       "Para averiguar más sobre un " + Cog + " haz clic en él.",
                       "Reúne tesoros en el dibuparque para rellenar el risómetro.",
                       "Edificios" + Cog + " son lugares peligrosos! ¡No entres en ellos solo!",
                       "Cuando pierdas un combate, los " + Cogs + " se llevarán todas tus bromas.",
                       "Para conseguir más bromas, juega a los juegos del tranvía!",
                       "Para conseguir más puntos de risa, completa las dibutareas.",
                       "Todas las dibutareas proporcionan recompensas.",
                       "Algunas recompensas sirven para poder llevar más bromas.",
                       "Si ganas un combate, consigues créditos de dibutareas por cada " + Cog + " derrotado.",
                       "Si recuperas un edificio " + Cog + " vuelve a entrar para ver el agradecimiento especial de su propietario.",
                       "Para mirar hacia arriba, mantén pulsada la tecla Re Pág.",
                       "Si pulsas la tecla Tab, podrás contemplar diferentes vistas de los alrededores.",
                       "Para mostrar lo que piensas a tus amigos secretos, escribe un '.' antes del pensamiento.",
                       "Cuando dejes aturdido a un " + Cog + " le será más difícil esquivar los objetos que caen.",
                       "Cada tipo de edificio " + Cog + " tiene un aspecto distinto.",
                       "Cuando derrotes a los " + Cogs + " de los pisos altos de un edificio, obtendrás habilidades superiores.",
                       )
QuestsDefaultTierNotDone = ("¡Hola, _avName_! Antes de acceder a una nueva dibutarea debes terminar la actual.",
                            "¡Muy buenas! Tienes que terminar las dibutareas actuales para acceder a una nueva.",
                            "¡Buenas, _avName_! Para poderte asignar una nueva dibutarea, tienes que terminar las dibutareas actuales.",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("He oído que _toNpcName_ te anda buscando._where_",
                                 "Déjate caer por donde _toNpcName_ cuando tengas la ocasión._where_",
                                 "Ve a ver a _toNpcName_ cuando pases por allí._where_",
                                 "Si tienes la ocasión, pásate a saludar a _toNpcName_._where_",
                                 "_toNpcName_ te asignará tu próxima dibutarea._where_",
                                 )
# Quest dialog
QuestsLocationArticle = ""
def getLocalNum(num):
    if (num <=9):
        return str(num) + "つ"
    else:
        return str(num)
QuestsItemNameAndNum = "%(num)s %(name)s"

QuestsCogQuestProgress = "%(progress)s de %(numCogs)s derrotados"
QuestsCogQuestHeadline = "SE BUSCA"
QuestsCogQuestSCStringS = "Tengo que derrotar un %(cogName)s%(cogLoc)s."
QuestsCogQuestSCStringP = "Tengo que derrotar algunos %(cogName)s%(cogLoc)s."
QuestsCogQuestDefeat = "Derrotar a %s"
QuestsCogQuestDefeatDesc = "%(numCogs)s %(cogName)s"

QuestsCogNewNewbieQuestObjective = "Ayuda a los dibus con %d puntos de risas o derrota a algunos %s"
QuestsCogNewNewbieQuestCaption = "Ayuda a un nuevo dibu con %d puntos de risas o menos"
QuestsCogOldNewbieQuestObjective = "Help a Toon with %(laffPoints)d Laff or less defeat %(objective)s"
QuestsCogOldNewbieQuestCaption = "Help a Toon %d Laff or less"
QuestsCogNewbieQuestAux = "Derrotar:"
QuestsNewbieQuestHeadline = "Aprendís"

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

QuestsRescueQuestProgress = "%(progress)s de %(numToons)s rescatados"
QuestsRescueQuestHeadline = "RESCATAR"
QuestsRescueQuestSCStringS = "Tengo que rescatar a un dibu%(toonLoc)s."
QuestsRescueQuestSCStringP = "Tengo que rescatar a algunos dibus%(toonLoc)s."
QuestsRescueQuestRescue = "Rescatar a %s"
QuestsRescueQuestRescueDesc = "%(numToons)s dibus"
QuestsRescueQuestToonS = "un dibu"
QuestsRescueQuestToonP = "dibus"
QuestsRescueQuestAux = "Rescatar a:"

QuestsRescueNewbieQuestObjective = "Ayuda a un nuevo dibu a rescatar a %s"
QuestsRescueOldNewbieQuestObjective = "Help a Toon with %(laffPoints)d Laff or less rescue %(objective)s"

QuestCogPartQuestCogPart = "Pieza de traje bot"
QuestsCogPartQuestFactories = "Fábricas"
QuestsCogPartQuestHeadline = "RECUPERAR"
QuestsCogPartQuestProgressString = "%(progress)s de %(num)s recuperadas"
QuestsCogPartQuestString = "Recuperar %s"
QuestsCogPartQuestSCString = "Tengo que recuperar %(objective)s%(location)s."
QuestsCogPartQuestAux = "Recuperar:"

QuestsCogPartQuestDesc = "una pieza de traje bot"
QuestsCogPartQuestDescC = "%(count)s piezas de traje bot "
QuestsCogPartQuestDescI = "algunas piezas de traje bot "

QuestsCogPartNewbieQuestObjective = 'Ayuda a un nuevo dibu a recuperar %s'
QuestsCogPartOldNewbieQuestObjective = 'Help a Toon with %(laffPoints)d Laff or less retrieve %(objective)s'

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
QuestsRecoverItemQuestGoToHQSCString = "Tengo que ir al Cuartel General Dibu."
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

QuestsMailboxQuestHeadline = "MAIL"
QuestsMailboxQuestSCString = "I need to check my mail."
QuestsMailboxQuestString = "Check your mail"

QuestsPhoneQuestHeadline = "CLARABELLE"
QuestsPhoneQuestSCString = "I need to call Clarabelle."
QuestsPhoneQuestString = "Call Clarabelle"

QuestsFriendNewbieQuestString = "Has %d amigos con %d puntos de risa o menos"
QuestsFriendNewbieQuestProgress = "%(progress)s de %(numFriends)s hechos"
QuestsFriendNewbieQuestObjective = "Haste amigo con %d dibus que tengan %d puntos de risa o menos"

QuestsTrolleyQuestHeadline = "TRANVÍA"
QuestsTrolleyQuestSCString = "Tengo que subir al tranvía."
QuestsTrolleyQuestString = "Subir al tranvía."
QuestsTrolleyQuestStringShort = "¿Quieres subir al tranvía?"

QuestsMinigameNewbieQuestString = "%d Minijuegos"
QuestsMinigameNewbieQuestProgress = "%(progress)s of %(numMinigames)s Played"
QuestsMinigameNewbieQuestObjective = "Juega %d minijuegos con Dibus que tienen %d puntos un el risometro o menos."
QuestsMinigameNewbieQuestSCString = "Necesito jugar en los minijuegos con Dibus nuevos."
QuestsMinigameNewbieQuestCaption = "Ayuda a un Dibu Nuevo con %d puntos en el risometro o menos."
QuestsMinigameNewbieQuestAux = "Juega:"

QuestsMaxHpReward = "Tu risómetro ha aumentado en %s."
QuestsMaxHpRewardPoster = "Recompensa: %s punto(s) de aumento en el risómetro"

QuestsMoneyRewardSingular = "Has conseguido 1 gominola."
QuestsMoneyRewardPlural = "Has conseguido %s gominolas."
QuestsMoneyRewardPosterSingular = "Recompensa: 1 gominola"
QuestsMoneyRewardPosterPlural = "Recompensa: %s gominolas"

QuestsMaxMoneyRewardSingular = "Ahora puedes llevar 1 gominola."
QuestsMaxMoneyRewardPlural = "Ahora puedes llevar %s gominolas."
QuestsMaxMoneyRewardPosterSingular = "Recompensa: Llevar 1 gominola"
QuestsMaxMoneyRewardPosterPlural = "Recompensa: Llevar %s gominolas"

QuestsMaxGagCarryReward = "Consigues un %(name)s. Ahora puedes llevar %(num)s bromas."
QuestsMaxGagCarryRewardPoster = "Recompensa: %(name)s (%(num)s)"

QuestsMaxQuestCarryReward = "Ahora puedes tener %s dibutareas."
QuestsMaxQuestCarryRewardPoster = "Recompensa: Tener %s dibutareas"

QuestsTeleportReward = "Ahora puedes teletransportarte a %s."
QuestsTeleportRewardPoster = "Recompensa: Acceso por teletransporte a %s"

QuestsTrackTrainingReward = "Ahora puedes entrenar las bromas de \"%s\"."
QuestsTrackTrainingRewardPoster = "Recompensa: Entrenamiento de bromas"

QuestsTrackProgressReward = "Ahora tienes el fotograma %(frameNum)s de la animación del circuito %(trackName)s."
QuestsTrackProgressRewardPoster = "Recompensa: Fotograma %(frameNum)s de la animación de circuito \"%(trackName)s\""

QuestsTrackCompleteReward = "Ahora puedes llevar y usar las bromas de \"%s\"."
QuestsTrackCompleteRewardPoster = "Recompensa: Entrenamiento de circuito %s final"

QuestsClothingTicketReward = "Puedes cambiarte de ropa"
QuestsClothingTicketRewardPoster = "Recompensa: Ticket de ropa"

QuestsCheesyEffectRewardPoster = "Recompensa: %s"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "en este parque"
QuestsStreetLocationThisStreet = "en esta calle"
QuestsStreetLocationNamedPlayground = "en el parque de %s"
QuestsStreetLocationNamedStreet = "en la %(toStreetName)s de %(toHoodName)s"
QuestsLocationString = "%(string)s%(location)s"
QuestsLocationBuilding = "El edificio de %s se llama"
QuestsLocationBuildingVerb = "el cual está "
QuestsLocationParagraph = "\a%(building)s \"%(buildingName)s\"...\a...%(buildingVerb)s %(street)s."
QuestsGenericFinishSCString = "Necesito terminar la Dibutarea."

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
    5 : ["Chocolatina", "Chocolatinas", "una "],
    6 : ["Tiza", "Tizas", "una "],
    7 : ["Receta", "Recetas", "una "],
    8 : ["Nota", "Notas", "una "],
    9 : ["Calculadora", "Calculadoras", "una "],
    10 : ["Neumático de coche de payasos", "Neumáticos de coche de payasos", "un "],
    11 : ["Bomba de aire", "Bombas de aire", "una "],
    12 : ["Tinta de pulpo", "Tintas de pulpo", "un poco de "],
    13 : ["Paquete", "Paquetes", "un "],
    14 : ["Recibo de pez de acuario", "Recibos de pez de acuario", "un "],
    15 : ["Pez de acuario", "Peces de acuario", "un "],
    16 : ["Aceite", "Aceites", "un poco de "],
    17 : ["Grasa", "Grasas", "un poco de "],
    18 : ["Agua", "Aguas", "un poco de "],
    19 : ["Informe de equipo", "Informes de equipo", "un "],
    20 : ["Blackboard Eraser", "Blackboard Erasers", "a "],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    1000 : ["Ticket de ropa", "Tickets de ropa", "un "],

    # Donald's Dock quest items
    2001 : ["Tubo interno", "Tubos internos", "un "],
    2002 : ["Prescripción de monóculo", "Prescripciones de monóculo", "una "],
    2003 : ["Montura de monóculo", "Monturas de monóculo", "una "],
    2004 : ["Monóculo", "Monóculos", "un "],
    2005 : ["Peluca blanca grande", "Pelucas blancas grandes", "una "],
    2006 : ["Granel de lastre", "Graneles de lastre", "una "],
    2007 : ["Engranaje de bot", "Engranajes de bot", "un "],
    2008 : ["Carta náutica", "Cartas náuticas", "una "],
    2009 : ["Coraza repugnante", "Corazas repugnantes", "un "],
    2010 : ["Coraza limpia", "Corazas limpias", "un "],
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
    4009 : ["Tinta azul de pulpo", "Tintas azules de pulpo", "un poco de "],
    4010 : ["Castañuela transparente", "Castañuelas transparentes", "una "],
    4011 : ["Letra de Leo", "Letras de Leo", ""],

    # Daisy's Gardens quest items
    5001 : ["Corbata de seda", "Corbatas de seda", "una "],
    5002 : ["Traje mil rayas", "Trajes mil rayas", "un "],
    5003 : ["Tijera", "Tijeras", "unas "],
    5004 : ["Postal", "Postales", "una "],
    5005 : ["Pluma", "Plumas", "una "],
    5006 : ["Tintero", "Tinteros", "un "],
    5007 : ["Libreta", "Libretas", "una "],
    5008 : ["Caja de seguridad", "Cajas de seguridad", "una "],
    5009 : ["Bolsa de alpiste", "Bolsas de alpiste", "una "],
    5010 : ["Rueda dentada", "Ruedas dentadas", "una "],
    5011 : ["Ensalada", "Ensaladas", "una "],
    5012 : ["Llave de los Jardines de Daisy", "Llaves de los Jardines de Daisy", "una "],
    5013 : ["planos del cuartel general vendebot", "planos del cuartel general vendebot", "algunos "],
    5014 : ["nota del cuartel general vendebot", "notas del cuartel general vendebot", "una "],
    5015 : ["nota del cuartel general vendebot", "notas del cuartel general vendebot", "una "],
    5016 : ["nota del cuartel general vendebot", "notas del cuartel general vendebot", "una "],
    5017 : ["nota del cuartel general vendebot", "notas del cuartel general vendebot", "una "],

    # The Brrrgh quests
    3001 : ["Balón de fútbol", "Balones de fútbol", "un "],
    3002 : ["Tobogán", "Toboganes", "un "],
    3003 : ["Cubito de hielo", "Cubitos de hielo", "un "],
    3004 : ["Carta de amor", "Cartas de amor", "una "],
    3005 : ["Perrito caliente", "Perritos calientes", "un "],
    3006 : ["Anillo de compromiso", "Anillos de compromiso", "un "],
    3007 : ["Aleta de sardina", "Aletas de sardina", "una "],
    3008 : ["Poción calmante", "Pociones calmantes", "una "],
    3009 : ["Diente roto", "Dientes rotos", "un "],
    3010 : ["Diente de oro", "Dientes de oro", "un "],
    3011 : ["Pan de piñones", "Panes de piñones", "un "],
    3012 : ["Queso abultado", "Quesos abultados", "unos "],
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
    }
QuestsHQOfficerFillin = "Funcionario del cuartel general"
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = "Cuartel General Dibu"
QuestsHQLocationNameFillin = "en cualquier barrio"

QuestsTailorFillin = "Sastre"
QuestsTailorWhereFillin = ""
QuestsTailorBuildingNameFillin = "Tienda de Ropa"
QuestsTailorLocationNameFillin = "en cualquier barrio"
QuestsTailorQuestSCString = "Tengo que ir al sastre."

QuestMovieQuestChoiceCancel = "¡Vuelve más tarde, si necesitas una Dibutarea! ¡Chao!"
QuestMovieTrackChoiceCancel = "Vuelve más tarde, cuando te hayas decidido! ¡Chao!"
QuestMovieQuestChoice = "Elige una Dibutarea."
QuestMovieTrackChoice = "¿Te has decidido? Elige un circuito, o vuelve más tarde."

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
    QUEST : "Ya estás listo.\aSal y ponte a caminar hasta que decidas qué circuito elegir.\aPiénsalo bien, porque éste será tu circuito final.\aCuando estés seguro, vuelve conmigo.",
    INCOMPLETE_PROGRESS : "Piénsalo bien.",
    INCOMPLETE_WRONG_NPC : "Piénsalo bien.",
    COMPLETE : "¡Muy buena elección!",
    LEAVING : "Buena suerte.  Vuelve conmigo cuando tengas dominada tu nueva habilidad.",
    }

QuestDialog_3225 = {
    QUEST : "Gracias por venir, _avName_!\a"+TheCogs+" del vecindario han asustado a mi repartidor.\aNo tengo a nadie que entregue esta ensalada a _toNpcName_!\a¿Puedes encargarte tú? ¡Muchas gracias!_where_"
    }

QuestDialog_2910 = {
    QUEST : "¿Ya has vuelto?\aBuen trabajo con el resorte.\aEl objeto final es un contrapeso.\aPásate a ver a _toNpcName_ y tráete lo que encuentres._where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 jefebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, has derrotado a los jefebots. ¡Ve al cuartel general dibu para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 abogabots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, has derrotado a los abogabots. ¡Ve al cuartel general dibu para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    162 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 chequebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, has derrotado a los chequebots. ¡Ve al cuartel general dibu para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    163 : {GREETING : "",
           QUEST : "Bueno, creo que ya estás listo para algo más complicado.\aDerrota a 3 vendebots.",
           INCOMPLETE_PROGRESS : "Los " + Cogs + " están en las calles, atravesando los túneles.",
           INCOMPLETE_WRONG_NPC : "Muy bien, has derrotado a los vendebots. ¡Ve al cuartel general dibu para recibir una recompensa!",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    164 : {QUEST : "Creo que te vendrán bien unas cuantas bromas nuevas.\aVe a ver a %s, quizá te pueda ayudar._where_" % Flippy },
    165 : {QUEST : "Muy buenas.\aCreo que tienes que practicar con las bromas.\aCada vez que alcances a un bot con una de las bromas, aumentará tu experiencia.\aCuando tengas la suficiente experiencia, podrás usar bromas mejores.\aPractica ahora con tus bromas derrotando a 4 bots."},
    166 : {QUEST : "Te felicito, has derrotado a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 jefebots."},
    167 : {QUEST : "Te felicito, has derrotado a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 abogabots."},
    168 : {QUEST : "Te felicito, has derrotado a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 vendebots."},
    169 : {QUEST : "Te felicito, has derrotado a esos bots.\a¿Sabías que hay cuatro tipos diferentes de bots?\aHay abogabots, chequebots, vendebots y jefebots.\aSe diferencian en el color y en las etiquetas con su nombre.\aEntrénate derrotando a 4 chequebots."},
    170 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; él te aconsejará bien._where_" },
    171 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; él te aconsejará bien._where_" },
    172 : {QUEST : "Muy bien, ya sabes en qué se diferencian los cuatro tipos distintos de bots.\aCreo que ya estás listo para empezar a entrenarte en el tercer circuito de trucos.\aVe a ver a _toNpcName_ para elegir el próximo circuito de trucos; ella te aconsejará bien._where_" },

    175 : {GREETING : "",
           QUEST : "Did you know you have your very own Toon house?\aClarabelle Cow runs a phone catalog where you can order furniture to decorate your house.\aYou can also buy SpeedChat phrases, clothing, and other fun things!\aI'll tell Clarabelle to send you your first catalog now.\aYou get a catalog with new items every week!\aGo to your home and use your phone to call Clarabelle.",
           INCOMPLETE_PROGRESS : "Go home and use your phone to call Clarabelle.",
           COMPLETE : "Hope you have fun ordering things from Clarabelle!\aI just finished redecorating my house. It looks Toontastic!\aKeep doing ToonTasks to get more rewards!",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "Las bromas de lanzamiento y chorro son estupendas, pero te harán falta otras para enfrentarte a los bots de niveles superiores.\aCuando te juntes con otros dibus para luchar contra los bots, podrás combinar ataques para infligirles más daños. \aPrueba con distintas combinaciones de trucos para ver cuáles funcionan mejor.\aEn el siguiente circuito, escoge entre Sonido y Curadibu.\aSonido es una broma especial que causa daños a todos los bots al hacer impacto.\aCuradibu te permite sanar a otros dibus durante el combate.\aCuando te hayas decidido, vuelve para elegir la broma que desees.",
           INCOMPLETE_PROGRESS : "¿Ya has vuelto?  Vale, ¿te has decidido ya?",
           INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
           COMPLETE : "Buena decisión.  Antes de usar esas bromas, deberás entrenarte con ellas.\aEn el entrenamiento tienes que completar una serie de dibutareas.\aCada tarea te proporcionará un fotograma de la animación del ataque con la broma.\aCuando reúnas los 15, conseguirás la tarea final de entrenamiento, que te permitirá usar la nueva broma.\aComprueba cómo vas en el dibucuaderno.",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "Si quieres recorrer la ciudad más fácilmente, ve a ver a _toNpcName_._where_" },
    1040 : { QUEST : "Si quieres recorrer la ciudad más fácilmente, ve a ver a _toNpcName_._where_" },
    1041 : { QUEST : "¡Hola!  ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos, o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amiguete mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1042 : { QUEST : "¡Hola!  ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos, o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amiguete mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1043 : { QUEST : "¡Hola!  ¿Qué te trae por aquí?\aTodo el mundo usa los agujeros portátiles para viajar en Toontown.\aPuedes teletransportarte al lugar donde están tus amigos mediante la Lista de amigos, o a cualquier barrio con el mapa del dibucuaderno.\a¡Desde luego, tendrás que ganártelo!\aActivaré tu acceso por teletransporte al centro de Toontown si ayudas a un amiguete mío.\aParece que los bots están dando guerra en la calle Locuela.  Ve a ver a _toNpcName_._where_" },
    1044 : { QUEST : "Vaya, gracias por pasarte por aquí.  La verdad es que necesito ayuda.\aComo ves, no tengo clientes.\aHe perdido mi libro secreto de recetas y ya nadie viene a mi restaurante.\aLo vi por última vez justo antes de que los bots ocupasen mi edificio.\a¿Puedes ayudarme a recuperar cuatro famosas recetas mías?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mis recetas?" },
    1045 : { QUEST : "¡Muchas gracias!\aEn poco tiempo tendré todo el recetario y podré volver a abrir mi restaurante.\aAh, tengo una nota para ti: algo sobre el teletransporte.\aDice Gracias por ayudar a mi amigo. Entrega esto en el Cuartel General Dibu.\aDe verdad, muchas gracias.\a¡Adiós!",
             LEAVING : "",
             COMPLETE : "Ah, sí, aquí dice que has sido de gran ayuda para algunos de los amigos de la calle Locuela.\aDice que necesitas teletransportarte al centro de Toontown.\aPues bien, eso está hecho.\aAhora puedes teletransportarte para volver al dibuparque desde casi cualquier lugar de Toontown.\aAbre tu mapa y haz clic en Centro de Toontown." },
    1046 : { QUEST : "Los chequebots han estado dando la lata en la Caja de Ahorros Pastagansa.\aPásate por allí para ver si puedes hacer algo._where_" },
    1047 : { QUEST : "Los chequebots se han estado colando en el banco para robar nuestras calculadoras.\aRecupera cinco calculadoras que han robado los chequebots.\aPara no tener que estar yendo y viniendo, tráelas todas de una vez.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Sigues buscando las calculadoras?" },
    1048 : { QUEST : "¡Vaya!  Gracias por recuperar nuestras calculadoras.\aMmm... Están un poco estropeadas.\a¿Puedes llevárselas a _toNpcName_ a su tienda, \"Cosquilladores automáticos\" en esta calle?\aTal vez ella pueda arreglarlas.",
             LEAVING : "", },
    1049 : { QUEST : "¿Qué es eso?  ¿Calculadoras rotas?\a¿Chequebots, dices?\aUm, veamos...\aSí, han quitado los engranajes, pero no me quedan repuestos...\a¿Sabes que podría servirnos? Unos engranajes de bots, grandes, de bots grandotes.\aLos engranajes de bots de nivel 3 valdrán.  Necesito dos para cada máquina, así que son diez en total.\a¡Tráelos enseguida y los arreglaré!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Recuerda que necesito diez engranajes para arreglar las calculadoras." },
    1053 : { QUEST : "Muy bien, con esto seguro que vale.\aTodas arregladas, es gratis.\aDevuélveselas a Pastagansa y salúdales de mi parte.",
             LEAVING : "",
             COMPLETE : "¿Están arregladas todas las calculadoras?\aBuen trabajo.  Seguro que tengo algo por aquí con lo que recompensarte..." },
    1054 : { QUEST : "_toNpcName_ necesita ayuda con sus coches de payasos._where_" },
    1055 : { QUEST : "¡Hola!  ¡No puedo encontrar por ningún sitio los neumáticos de este coche de payasos!\a¿Crees que podrás echarme una mano?\aMe parece que Perico Pirado los ha tirado al estanque del dibuparque del centro de Toontown. \aSi te colocas encima de uno de los amarraderos del estanque podrás intentar pescar los neumáticos para traérmelos.",
             GREETING : "¡Jujujú!",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Algún problemilla pescando los cuatro neumáticos?" },
    1056 : { QUEST : "¡Estupendísimo!  ¡Ahora puedo volver a conducir este viejo coche de payasos!\aEh, creía que tenía una vieja bomba de aire por aquí para inflar estos neumáticos...\a¿Se la habrá llevado prestada _toNpcName_?\a¿Podrías hacerme el favor de pedirle que me la devuelva?_where_",
             LEAVING : "" },
    1057 : { QUEST : "¿Qué tal?\a¿Una bomba de aire, dices?\a¿Sabes lo que te digo? Si me ayudas a limpiar las calles de algunos de esos bots de nivel alto...\aTe daré la bomba de aire.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Eso es todo lo que sabes hacer?" },
    1058 : { QUEST : "Buen trabajo, sabía que lo conseguirías.\aAquí está la bomba.  Seguro que _toNpcName_ se alegra de recuperarla.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "¡Yujuuu!  ¡Ya puedo conducir!\aPor cierto, gracias por ayudarme.\aToma esto." },
    1059 : { QUEST : "_toNpcName_ se está quedando sin suministros.  ¿Puedes echarle una mano?_where_" },
    1060 : { QUEST : "¡Gracias por venir!\aEsos bots han estado robándome la tinta, y casi no me queda nada.\a¿Podrías pescar un poco de tinta de pulpo en el estanque?\aPara pescar, basta con que te sitúes en el amarradero de la orilla.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has tenido problemas para pescar?" },
    1061 : { QUEST : "¡Estupendo, gracias por la tinta!\a¿Sabes qué? Si quitases de en medio a unos cuantos de esos chupatintas...\aNo me quedaría sin tinta tan rápidamente.\aDerrota a seis chupatintas en el centro de Toontown para llevarte una recompensa.",
             LEAVING : "",
             COMPLETE : "¡Gracias!  Te recompensaré por tu ayuda.",
             INCOMPLETE_PROGRESS : "He visto unos cuantos chupatintas más." },
    1062 : { QUEST : "¡Estupendo, gracias por la tinta!\a¿Sabes qué? Si quitases de en medio a unos cuantos de esos chupasangres...\aNo me quedaría sin tinta tan rápidamente.\aDerrota a seis chupasangres en el centro de Toontown para llevarte una recompensa.",
             LEAVING : "",
             COMPLETE : "¡Gracias!  Te recompensaré por tu ayuda.",
             INCOMPLETE_PROGRESS : "He visto unos cuantos chupasangres más." },
    900 : { QUEST : "He oído que _toNpcName_ necesita ayuda con un paquete._where_" },
    1063 : { QUEST : "¡Hola, gracias por venir!\aUn bot me ha robado un paquete muy importante delante de mis narices.\aPor favor, intenta recuperarlo.  Creo que era de nivel 3...\aAsí que tendrás que derrotar a bots de nivel 3 hasta que encuentres mi paquete.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No ha habido suerte con el paquete, ¿eh?" },
    1067 : { QUEST : "¡Ése es, muy bien!\aEh, la dirección está borrosa...\aSólo se lee que es para un doctor, el resto está emborronado.\a¿Será para _toNpcName_?  ¿Puedes llevárselo?_where_",
             LEAVING : "" },
    1068 : { QUEST : "No esperaba ningún paquete.  Quizá sea para el doctor Eufo Rico.\aMi ayudante iba a ir allí hoy de todas formas, así que le diré que se lo pregunte.\aMientras tanto, ¿te importa deshacerte de unos cuantos bots en mi calle?\aDerrota a diez bots en el centro de Toontown.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Mi ayudante no ha vuelto todavía." },
    1069 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un chequebot se lo ha robado a mi ayudante cuando volvía.\a¿Podrías intentar recuperarlo?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No ha habido suerte con el paquete, ¿eh?" },
    1070 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un vendebot se lo ha robado a mi ayudante cuando volvía.\aLo siento, pero tendrás que encontrar a ese vendebot para recuperarlo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No ha habido suerte con el paquete, ¿eh?" },
    1071 : { QUEST : "El doctor Eufo Rico no esperaba un paquete, tampoco.\aPor desgracia, un jefebot se lo ha robado a mi ayudante cuando volvía.\a¿Podrías intentar recuperarlo?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No ha habido suerte con el paquete, ¿eh?" },
    1072 : { QUEST : "¡Estupendo, lo has recuperado!\aDeberías probar con _toNpcName_, puede que sea para él._where_",
             LEAVING : "" },
    1073 : { QUEST : "Oh, gracias por traerme mis paquetes.\aEspera un momento, estaba esperando dos.  ¿Podrías ir a ver a _toNpcName_ para preguntarle si tiene el otro?",
             INCOMPLETE : "¿Has conseguido encontrar mi otro paquete?",
             LEAVING : "" },
    1074 : { QUEST : "¿Ha dicho que había otro paquete?  A lo mejor lo han robado también los bots.\aDerrota a bots hasta que encuentres el segundo paquete.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No ha habido suerte con el otro paquete, ¿eh?" },
    1075 : { QUEST : "¡Al final resulta que sí que había un segundo paquete!\aDeprisa, llévaselo a _toNpcName_ y pídele disculpas de mi parte.",
             COMPLETE : "¡Eh, ha llegado mi paquete!\aComo pareces ser un dibu muy servicial, esto te vendrá bien.",
             LEAVING : "" },
    1076 : { QUEST : "Ha habido problemas en Peces dorados de 14 kilates.\aA _toNpcName_ le vendrá bien una ayudita._where_" },
    1077 : { QUEST : "Gracias por venir. "+TheCogs+" han robado todos mis peces dorados.\aCreo que quieren venderlos para sacar un dinero rápido.\aEsos cinco peces han sido mi única compañía en esta tiendecita durante tantos años...\aSi pudieses hacerme el favor de recuperarlos, te lo agradecería eternamente.\aSeguro que uno de los bots tiene mis peces.\aDerrota a bots hasta que encuentres mis peces.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Por favor, recupera mis peces dorados." },
    1078 : { QUEST : "¡Oh, tienes mis peces!\a¿Eh?  ¿Qué es eso? ¿Un recibo?\aAh, sí son los bots, a fin de cuentas.\aNo consigo averiguar qué diantre es este recibo.  ¿Podrías llevárselo a _toNpcName_ para ver si él lo entiende?_where_",
             INCOMPLETE : "¿Qué ha dicho _toNpcName_ del recibo?",
             LEAVING : "" },
    1079 : { QUEST : "Mmm, déjame ver ese recibo.\a... Ah, sí, dice que un pez dorado fue vendido a un secuaz.\aNo menciona para nada qué ha sido de los otros cuatro peces.\aQuizá debas ponerte a buscar a ese secuaz.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No creo que te pueda ayudar más.\a¿Por qué no te pones a buscar ese pez dorado?" },
    1092 : { QUEST : "Mmm, déjame ver ese recibo.\a... Ah, sí, dice que un pez dorado fue vendido a un calderilla.\aNo menciona para nada qué ha sido de los otros cuatro peces.\aQuizá debas ponerte a buscar a ese calderilla.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No creo que te pueda ayudar más.\a¿Por qué no te pones a buscar ese pez dorado?" },
    1080 : { QUEST : "¡Oh, gracias a Dios!  Has encontrado a Óscar. Es mi favorito.\a¿Qué pasa, Óscar?  Oh, vaya... ¿de verdad? ... ¿Están allí?\aÓscar dice que los otros cuatro escaparon y se metieron en el estanque del dibuparque.\a¿Me haces el favor de ir a recogerlos? \aBasta con que los pesques en el estanque.",
             LEAVING : "",
             COMPLETE : "¡Oooh, qué contento estoy!  ¡Por fin vuelvo a estar junto a mis amiguitos!\a¡Te mereces una estupenda recompensa!",
             INCOMPLETE_PROGRESS : "¿Te está costando encontrar a los peces?" },
    1081 : { QUEST : "Parece ser que _toNpcName_ se encuentra en una situación pegajosa.  Seguro que le vendrá bien una ayudita._where_" },
    1082 : { QUEST : "¡Se me ha derramado el pegamento rápido y me he quedado pegado!\aSi pudiera hacer algo para liberarme...\aSe me ocurre una idea, si te sientes valiente.\aDerrota a unos vendebots y tráeme un poco de aceite.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1083 : { QUEST : "El aceite ha ayudado, pero sigo sin despegarme del todo.\a¿Qué puedo probar?  Nada procede.\aSe me ocurre una idea, por probarla no pasa nada.\aDerrota a unos abogabots y tráeme un poco de grasa.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1084 : { QUEST : "No, no ha servido de nada.  Esto no me divierte.\aHe puesto la grasa y no ha habido suerte.\aSe me ocurre una idea para sacarme de aquí.\aDerrota a unos chequebots y trae agua para mojarme.",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "¡Hurra! Estoy libre de este pegamento rápido.\aComo recompensa, toma este obsequio.\aPodrás disfrutar de una combativa velada...\a¡Oh, no!  ¡He vuelto a quedarme pegado!",
             INCOMPLETE_PROGRESS : "¿Puedes ayudarme a despegarme?" },
    1085 : { QUEST : "_toNpcName_ está llevando a cabo ciertas investigaciones sobre los bots.\aVete a hablar con él si quieres ayudarle._where_" },
    1086 : { QUEST : "Efectivamente, estoy realizando un estudio sobre los bots.\aQuiero saber cómo funcionan.\aMe sería de gran ayuda que consiguieses algunos engranajes de bot.\aAsegúrate de que pertenezcan a bots de nivel 2 al menos, para que tengan el tamaño suficiente para examinarlos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿No puedes conseguir suficientes engranajes?" },
    1089 : { QUEST : "Muy bien, veamos.  ¡Excelentes especímenes!\aMmm...\aDe acuerdo, aquí está mi informe.  Lleva esto enseguida al cuartel general dibu.",
             INCOMPLETE : "¿Has llevado mi informe al cuartel general?",
             COMPLETE : "Buen trabajo, _avName_, a partir de ahora nos ocuparemos nosotros.",
             LEAVING : "" },
    1090 : { QUEST : "_toNpcName_ tiene información útil para ti._where_" },
    1091 : { QUEST : "He oído que en el cuartel general dibu están trabajando en una especie de radar de bots.\aTe permitirá ver dónde están los bots y así poder encontrarlos más fácilmente.\aLa página Bot del dibucuaderno es la clave.\aSi derrotas suficientes bots, podrás sintonizar sus señales y detectar su paradero.\aSigue derrotando a los bots para estar listo.",
             COMPLETE : "¡Buen trabajo!  Seguro que esto te viene bien...",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsatelo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
           INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
           INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
           COMPLETE : "Muy buena decisión...",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "Esos bots tan pesados están dando problemas otra vez.\a_toNpcName_ ha informado de que falta otro objeto. Pásate por allí, a ver si puedes arreglar la situación._where_" },
    2202 : { QUEST : "Hola, _avName_. Gracias a Dios que has venido. Un cacomatraco acaba de pasar por aquí y se ha largado corriendo con un tubo interno.\aTemo que lo usen para sus malvados propósitos.\aPor favor, busca al bot y recupera el tubo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mi tubo interno?",
             COMPLETE : "¡Has encontrado mi tubo interno! Eres SENSACIONAL. Aquí tienes tu recompensa...",
             },
    2203 : { QUEST : TheCogs+" están sembrando el caos en el banco.\aVe a ver al capitán Doblón, a ver qué puedes hacer._where_" },
    2204 : { QUEST : "Bienvenido a bordo, grumete.\a¡Arg! Esa escoria de bots han aplastado mi monóculo y no me puedo apañar sin él.\aSé un buen marinero y lleva esta prescripción al doctor Rompecubiertas para que me haga uno nuevo._where_.",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "¿Qué es esto?\aMe encantaría hacer este monóculo, pero los bots han estado saqueando mis existencias.\aSi consigues arrebatarle las monturas de monóculo a un secuaz, me serás de gran ayuda.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Lo siento. Si no tengo las monturas del secuaz, no hay monóculo.",
             },
    2206: { QUEST : "¡Excelente!\aUn momento...\aAquí tienes el monóculo de la prescripción. Llévaselo al capitán Doblón._where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "¡Avante a toda!\aNo, si al final te vas a ganar los galones y todo.\aAquí tienes.",
            },
    2207 : { QUEST : "¡Perci Percebe tiene un bot en la tienda!\aMás vale que vayas para allá enseguida._where_" },
    2208 : { QUEST : "¡Vaya! Se te acaba de escapar, cariño.\aAquí había un apuñalaespaldas.  Se ha llevado mi peluca blanca grande.\aHa dicho que era para su jefe, y no sé qué sobre un \"precedente legal\".\aSi pudieses recuperarla, te estaría eternamente agradecida.",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "¿Todavía no lo has encontrado?\aEs alto y tiene la cabeza puntiaguda.",
             COMPLETE : "¡La has encontrado!\a¡Eres todo un encanto!\aTe has ganado esto, sin duda...",
             },
    2209 : { QUEST : "Isidoro se está preparando para un viaje importante.\aAcércate a ver en qué puedes ayudarle._where_"},
    2210 : { QUEST : "Puedo utilizar tu ayuda.\aEn el cuartel general dibu me han pedido que haga un viaje para averiguar de dónde proceden los bots.\aNecesito unas cuantas cosas para mi barco, pero ando escaso de gominolas.\aPásate a ver a Pepa Sastre para que te dé algo de lastre. Para conseguirlo, tendrás que hacerle un favor._where_",
             GREETING : "¿Qué hay, _avName_?",
             LEAVING : "",
             },
    2211 : { QUEST : "Así que Isidoro quiere lastre, ¿eh?\aTodavía me debe la última fanega.\aTe la daré si consigues limpiar mi calle de cinco microgerentes.",
             INCOMPLETE_PROGRESS : "¡No, tonto! ¡He dicho CINCO microgerentes!...",
             GREETING : "¿Qué puedo hacer por ti?",
             LEAVING : "",
             },
    2212 : { QUEST : "Un trato es un trato.\aAquí tienes el lastre para ese tacaño de Isidoro._where_",
             GREETING : "Vaya, mira lo que aparece por aquí...",
             LEAVING : "",
             },
    2213 : { QUEST : "Gran trabajo. Sabía que se atendría a razones. \aAhora necesito una carta náutica de Pasma Rote.\aNo creo que me fíen allí tampoco, así que tendrás que llegar a un acuerdo con él._where_.",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "Sí, tengo la carta de navegación que necesita Isidoro.\aY te la daré si estás dispuesto a trabajar para conseguirla.\aEstoy intentando construir un astrolabio para orientarme con las estrellas.\aPara hacerlo necesito tres engranajes de bot.\aVuelve cuando los hayas conseguido.",
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
    2902 : { QUEST : "¿Tú eres el nuevo recluta?\aBien, bien. Tal vez puedas ayudarme.\aEstoy construyendo un gigantesco cangrejo prefabricado para confundir a los bots.\aAunque también me serviría una coraza. Ve a ver a Clodovico Cromañón y pídele una, por favor._where_",
             },
    2903 : { QUEST : "¡Muy buenas!\aSí, he oído hablar del cangrejo gigante en el que trabaja Ajab.\aSin embargo, la mejor coraza que tengo está un poco sucia.\aPórtate bien y llévala a la tintorería antes de entregarla._where_",
             LEAVING : "¡Gracias!"
             },
    2904 : { QUEST : "Debes de ser el que viene de parte de Clodovico.\aCreo que puedo limpiar eso en un santiamén.\aDame un minuto...\aAquí tienes. ¡Como nuevo!\aSaluda a Ajab de mi parte._where_",
             },
    2905 : { QUEST : "Vaya, esto es exactamente lo que andaba buscando.\aYa que estás aquí, también voy a necesitar un resorte de reloj muy grande.\aPásate por la tienda de Garfio para ver si tiene uno._where_",
             },
    2906 : { QUEST : "Un resorte grande, ¿eh?\aLo siento, pero el más grande que tengo es bastante pequeño, en realidad.\aQuizás pueda hacer uno con los resortes de los gatillos de pistola de agua.\aTráeme tres de esos chismes y veré que puedo hacer.",
             },
    2907 : { QUEST : "Veamos...\aImpresionante. Simplemente impresionante.\aA veces me sorprendo a mí mismo.\aAquí tienes: un resorte grande para Ajab._where_",
             LEAVING : "¡Buen viaje!",
             },
    2911 : { QUEST : "Me encantaría ayudar a la causa, _avName_.\aPero me temo que las calles ya no son seguras.\a¿Por qué no acabas con unos cuantos chequebots? Después hablaremos.",
             INCOMPLETE_PROGRESS : "Creo que las calles no son todavía muy seguras que digamos.",
             },
    2916 : { QUEST : "Sí, tengo un contrapeso que le vendría bien a Ajab.\aSin embargo, creo que sería mejor que antes derrotases a un par de vendebots.",
             INCOMPLETE_PROGRESS : "Todavía no. Derrota a unos cuantos vendebots más.",
             },
    2921 : { QUEST : "Mmm, se supone que tengo que darte un contrapeso.\aPero me sentiría mucho más seguro si no hubiese tantos jefebots rondando por aquí.\aDerrota a seis y ven a verme.",
             INCOMPLETE_PROGRESS : "Creo que esta zona todavía no es segura...",
             },
    2925 : { QUEST : "¿Has acabado?\aBien, supongo que la zona ya es bastante segura.\aAquí tienes el contrapeso para Ajab._where_"
             },
    2926 : {QUEST : "Bueno, eso es todo.\aVeamos si funciona.\aMmm, hay un pequeño problema.\aNo puedo encenderlo porque ese edificio bot está tapando mi panel solar.\a¿Puedes hacerme el favor de reconquistarlo?",
            INCOMPLETE_PROGRESS : "Sigo sin tener electricidad. ¿Qué hay de ese edificio?",
            COMPLETE : "¡Estupendo! ¡Se te da de miedo zurrar a los bots! Toma, aquí tienes tu recompensa...",
            },
    3200 : { QUEST : "Acabo de recibir una llamada de _toNpcName_.\aEstá teniendo un día de perros. Tal vez puedas ayudarle.\aPásate por allí para ver qué necesita._where_" },
    3201 : { QUEST : "¡Vaya, gracias por venir!\aNecesito que alguien lleve esta corbata de seda nueva a _toNpcName_.\a¿Me harías tú ese favor?_where_" },
    3203 : { QUEST : "¡Ah, ésta debe de ser la corbata que he encargado! ¡Gracias!\aVa a juego con el traje mil rayas que acabo de terminar, justo ahí.\aEh, ¿qué ha pasado con el traje?\a¡Oh, no! ¡"+TheCogs+" deben de haberme robado el traje nuevo!\aLucha con los bots hasta que encuentres el traje y tráemelo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya mi traje? ¡Seguro que se lo han llevado los bots!",
             COMPLETE : "¡Hurra! ¡Has encontrado mi traje nuevo!\a¿Ves? Te dije que los bots lo tenían. Toma tu recompensa...",
             },

    3204 : { QUEST : "_toNpcName_ acaba de llamar para informar de un robo.\a¿Por qué no te pasas por allí para ver si puedes arreglar la situación?_where_" },
    3205 : { QUEST : "¡Hola, _avName_! ¿Has venido a ayudarme?\aAcabo de ahuyentar a un chupasangres de mi tienda. ¡Guau! Daba mucho miedo.\a¡Pero ahora no puedo encontrar las tijeras! Seguro que se las ha llevado el chupasangres.\aPor favor, busca al chupasangres y recupera las tijeras.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Sigues buscando las tijeras?",
             COMPLETE : "¡Mis tijeras! ¡Muchas gracias! Toma tu recompensa...",
             },

    3206 : { QUEST : "Parece ser que _toNpcName_ está teniendo algún que otro problema con los bots.\aVe a ver si puedes ayudarle._where_" },
    3207 : { QUEST : "¡Buenas, _avName_! ¡Gracias por venir!\aUnos cuantos embaucadores han entrado y se han llevado un taco de postales del mostrador.\a¡Por favor, derrota a esos embaucadores y recupera mis postales!",
             INCOMPLETE_PROGRESS : "¡No hay postales suficientes! ¡Sigue buscando!",
             COMPLETE : "¡Oh, gracias! ¡Ahora puedo entregar el correo a tiempo! Toma tu recompensa...",
             },

    3208 : { QUEST : "Hemos estado recibiendo quejas de los vecinos sobre todos esos gorrones.\aPor favor, intenta derrotar a diez gorrones para ayudar a tus amigos, los dibus de los Jardines de Daisy. " },
    3209 : { QUEST : "¡Gracias por ocuparte de los gorrones!\a¡Pero ahora los televendedores se han desmadrado!\aDerrota a diez televendedores en los Jardines de Daisy y vuelve para llevarte una recompensa." },

    3247 : { QUEST : "Hemos estado recibiendo quejas de los vecinos sobre todos esos chupasangres.\aPor favor, intenta derrotar a veinte chupasangres para ayudar a tus amigos, los dibus de los Jardines de Daisy. " },


    3210 : { QUEST : "¡Oh, no, La flor chorreante, de la calle Arce, se ha quedado sin flores!\aLlévales diez flores chorreantes de las tuyas para ayudarles. \aPrimero comprueba que tienes diez flores chorreantes en el inventario.",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "Necesito diez flores chorreantes. ¡No tienes suficientes!" },
    3211 : { QUEST : "¡Oh, muchas gracias! Esas flores arreglarán la situación.\aPero los bots que hay fuera me dan miedo.\a¿Puedes ayudarme derrotando a unos cuantos?\aVuelve cuando hayas derrotado a veinte bots en esta calle.",
             INCOMPLETE_PROGRESS : "¡Todavía quedan bots ahí fuera!  ¡Sigue luchando!",
             COMPLETE : "¡Oh, gracias! Me has ayudado un montón. Tu recompensa es...",
             },

    3212 : { QUEST : "_toNpcName_ necesita ayuda para encontrar una cosa que ha perdido.\aVe a verla, tal vez puedas ayudarla._where_" },
    3213 : { QUEST : "Hola, _avName_. ¿Puedes ayudarme?\aParece que he perdido mi pluma estilográfica. Creo que se la han llevado unos bots.\aDerrótalos y recupera la pluma, por favor.",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya mi pluma?" },
    3214 : { QUEST : "¡Sí, ésa es! ¡Muchas gracias!\aPero en cuanto te has marchado me he dado cuenta de que también me faltaba el tintero.\aVence a los bots y recupera el tintero, por favor.",
             INCOMPLETE_PROGRESS : "¡Sigo buscando el tintero!" },
    3215 : { QUEST : "¡Fantástico! Ahora he recuperado la pluma y el tintero.\aPero ¿a que no te lo imaginas?\a¡No encuentro la libreta! ¡La deben haber robado también!\aDerrota a los bots hasta que encuentres la libreta y tráemela para que te dé una recompensa.",
             INCOMPLETE_PROGRESS : "¿Alguna novedad sobre la libreta?" },
    3216 : { QUEST : "¡Ésa es mi libreta! ¡Hurra! Tu recompensa es...\a¡Eh! ¿Dónde está?\aTenía tu recompensa justo aquí, en la caja de seguridad. ¡Pero se la han llevado!\a¿Puedes creerlo? ¡"+TheCogs+" han robado tu recompensa!\aVence a los bots para recuperar la caja de seguridad.\aCuando me la traigas, te daré tu recompensa.",
             INCOMPLETE_PROGRESS : "¡Sigue buscando la caja de seguridad!  ¡Tu recompensa está dentro!",
             COMPLETE : "¡Por fin! Tenía tu nueva bolsa de bromas en la caja. Aquí está...",
             },

    3217 : { QUEST : "Hemos estado estudiando la mecánica de los vendebots.\aQueremos estudiar más de cerca algunas piezas.\aTráenos la rueda dentada de un fardoncete.\aPuedes atraparlas cuando los bots estallan." },
    3218 : { QUEST : "¡Buen trabajo! Ahora tenemos que compararla con la rueda dentada de un efusivo.\aEsas ruedas dentadas son más difíciles de atrapar, así que sigue intentándolo." },
    3219 : { QUEST : "¡Fantástico! Ahora sólo necesitamos una rueda dentada más.\aEsta vez necesitamos la rueda de un mandamás.\aPara encontrar a estos bots, tal vez tengas que buscar en el interior de algunos edificios de vendebots.\aCuando la tengas, tráela, y a cambio obtendrás tu recompensa." },

    3244 : { QUEST : "Hemos estado estudiando la mecánica de los abogabots.\aQueremos estudiar más de cerca algunas piezas.\aTráenos la rueda dentada de un persigueambulancias.\aPuedes atraparlas cuando los bots estallan." },
    3245 : { QUEST : "¡Buen trabajo! Ahora tenemos que compararla con la rueda dentada de un apuñalaespaldas.\aEsas ruedas dentadas son más difíciles de atrapar, así que sigue intentándolo." },
    3246 : { QUEST : "¡Fantástico! Ahora sólo necesitamos una rueda dentada más.\aEsta vez necesitamos la rueda de un portavoz.\aCuando la tengas, tráela para obtener a cambio tu recompensa." },

    3220 : { QUEST : "Acabo de oír que _toNpcName_ estaba preguntando por ti.\a¿Por qué no pasas a verla para ver qué quiere?_where_" },
    3221 : { QUEST : "¡Buenas, _avName_! ¡Aquí estás!\aHe oído que eres todo un experto en ataques chorreantes.\aNecesito a alguien que dé un buen ejemplo a todos los dibus de Jardines de Daisy.\aUsa tus ataques chorreantes para derrotar a un montón de bots.\aAnima a tus amigos a usar este tipo de ataques.\aCuando hayas derrotado a veinte bots, vuelve para llevarte una recompensa." },

    3222 : { QUEST : "Ha llegado el momento de demostrar tu dibupuntería.\aSi consigues recuperar cierto número de edificios bot, tendrás el privilegio de asumir tres tareas a la vez.\aPrimero reconquista dos edificios bot cualesquiera.\aLlama a los amigos que quieras para que te ayuden."},
    3223 : { QUEST : "¡Un gran trabajo con los edificios! \aAhora reconquista dos edificios más.\aLos edificios deben de tener al menos dos pisos de altura." },
    3224 : { QUEST : "¡Fantástico!\aAhora basta con que recuperes dos edificios más.\aLos edificios deben tener al menos tres pisos de altura.\aCuando termines, vuelve para obtener tu recompensa.",
             COMPLETE : "¡Lo has conseguido, _avName_!\a¡Has demostrado una dibupuntería increíble!",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_ dice que necesita ayuda.\a¿Por qué no vas a verla para ver en qué la puedes ayudar?_where_" },
    3235 : { QUEST : "¡Ah, ésta debe de ser la ensalada que encargué!\aGracias por traérmela.\aTodos esos bots deben de haber asustado al repartidor habitual de _toNpcName_.\a¿Por qué no nos haces un favor y derrotas a unos cuantos bots de ahí fuera?\aDerrota a diez bots en los Jardines de Daisy y vuelve con _toNpcName_.",
             INCOMPLETE_PROGRESS : "¿No estabas venciendo a los bots por mí?\a¡Maravilloso! ¡Sigue así!",
             COMPLETE : "¡Oh, muchas gracias por derrotar a esos bots!\aAhora quizás pueda seguir con mis repartos normales.\aTu recompensa es...",
             INCOMPLETE_WRONG_NPC : "Informa a _toNpcName_ sobre los bots a los que has derrotado._where_" },

    3236 : { QUEST : "Hay demasiados abogabots allí.\a¡Ayuda en lo que puedas!\aRecupera tres edificios de abogabots." },
    3237 : { QUEST : "¡Un gran trabajo con los edificios de abogabots! \a¡Pero ahora hay demasiados vendebots!\aRecupera tres edificios de vendebots y vuelve a por tu recompensa." },

    3238 : { QUEST : "¡Oh, no! ¡Un bot \"confraternizador\" ha robado la llave de los Jardines de Daisy!\aIntenta recuperarla.\aRecuerda, sólo encontrarás al confraternizador en el interior de edificios de vendebots. " },
    3239 : { QUEST : "Sí, has encontrado una llave, pero no es la correcta.\aNecesitamos la llave de los Jardines de Daisy.\a¡Sigue buscando! ¡La tiene un bot \"confraternizador\"!" },

    3242 : { QUEST : "¡Oh, no! ¡Un bot picapleitos ha robado la llave de Jardines de Daisy!\aIntenta recuperarla.\aRecuerda, sólo encontrarás al picapleitos en el interior de edificios de abogabots. " },
    3243 : { QUEST : "Sí, has encontrado una llave, pero no es la correcta.\aNecesitamos la llave de los Jardines de Daisy.\a¡Sigue buscando! ¡La tiene un bot picapleitos!" },

    3240 : { QUEST : "_toNpcName_ me acaba de decir que un picapleitos le ha robado una bolsa de alpiste.\aDerrota a los picapleitos hasta que encuentres el alpiste de Federico Tilla y llévaselo.\aSólo encontrarás a los picapleitos en el interior de los edificios de abogabots._where_",
             COMPLETE : "¡Oh, muchas gracias por encontrar el alpiste!\aTu recompensa es...",
             INCOMPLETE_WRONG_NPC : "¡Muy bien, has conseguido recuperar el alpiste!\aAhora llévaselo a _toNpcName_._where_",
             },

    3241 : { QUEST : "Algunos edificios bot están creciendo demasiado para nuestro gusto.\aIntenta recuperar algunos de los edificios más altos.\aReconquista cinco edificios de tres plantas o más y vuelve para llevarte una recompensa.",
             },

    3250 : { QUEST : "Doña Citronia ha recibido información sobre la existencia de un cuartel general vendebot en la calle Arce.\aReúnete con ella para investigarlo.",
             },
    3251 : { QUEST : "Aquí se cuece algo.\aHay una barbaridad de vendebots.\aDicen que han construido su propio cuartel general al final de la calle.\aRecórrela a ver si averiguas lo que está pasando.\aBusca vendebots por su cuartel general, derrota a cinco de ellos y regresa.",
             },
    3252 : { QUEST : "Venga, suelta prenda.\a¿Qué dices?\a¿Un cuartel general vendebot? ¡Dios mío! Hay que actuar.\aDebemos poner al corriente a Doña Zanahoria, que seguro que sabe lo que hay que hacer.\aVete corriendo y cuéntale lo que sabes. Está ahí mismo, bajando la calle.",
            },
    3253 : { QUEST : "¿Qué quieres? Estoy muy ocupada.\a¿Cómo? ¿Un cuartel general bot?\aMenuda bobada. Es imposible.\aTe debes haber equivocado. Es inconcebible.\a¿Cómo? No me lo discutas.\aBueno, mira, si quieres, tráeme pruebas.\aSi los vendebots están construyendo su cuartel general, todos los bots que anden por allí llevarán planos.\aA los bots les encanta la burocracia, ¿no sabías? \aVe derrotando vendebots en el lugar que me dices hasta que encuentres los planos.\aLuego me los traes y ya veremos si te creo o no.",
            },
    3254 : { QUEST : "¿Otra vez tú por aquí? ¿Cómo? ¿Planos? ¿Los has conseguido?\aDéjame que los vea. Vaya, ¿una fábrica?\aDebe ser la planta donde construyen los vendebots... ¿Y esto qué es?\aJusto lo que pensaba.\aComo sospechaba, están construyendo un cuartel general vendebot.\aMenudo problema. Voy a tener que hacer unas cuantas llamadas. Mira, estoy muy ocupada. Adiós.\a¿Cómo? Sí, sí. Llévale los planos a Doña Citronia.\aSeguro que ella los entenderá mejor que yo.",
             COMPLETE : "¿Qué te ha dicho Doña Zanahoria?\aEntonces, teníamos razón. Esto es muy peligroso. ¿A ver los planos?\aVaya, parece que los vendebots han construido una planta con maquinaria para la fabricación de bots.\aEsto me huele fatal. Mantente al margen hasta que consigas más puntos de risa.\aCuando reúnas más podremos seguir con la investigación.\aPor ahora, aquí tienes tu recompensa. ¡Muy bien!",
            },


    3255 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3256 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3257 : { QUEST : "_toNpcName_ está investigando el asunto del cuartel general vendebot.\aVete a ver si le puedes prestar tu ayuda._where_" },
    3258 : { QUEST : "No sabemos realmente qué es lo que están tramando los bots en su nuevo cuartel general.\aQuiero que me traigas información, pero obtenida directamente de los propios bots.\aSi conseguimos cuatro notas de oficina de los vendebots sacadas del mismo cuartel, podremos hacernos una idea más clara.\aTráeme la primera nota en cuanto la consigas y así voy estudiando la información a medida que aparezca.",
             },
    3259 : { QUEST : "¡Estupendo! A ver qué dice la nota\a\"Estimados vendebots:\"\a\"Estaré en mi oficina del ático de las torres vendebots ascendiendo bots a niveles superiores.\"\a\"Cuando reúnan los méritos necesarios, suban a mi oficina en el ascensor del vestíbulo de entrada.\"\a\"Se acabó el descanso. ¡A trabajar!\"\a\"Firmado, vendebot VIP\"\aVaya, vaya. A "+Flippy+" le va a interesar esto. Se lo voy a mandar ahora mismo.\aMárchate ya en busca de la segunda nota y tráemela en cuanto la tengas.",
             },
    3260 : { QUEST : "Ya has vuelto, qué bien. A ver qué has encontrado....\a\"Estimados vendebots:\"\a\"Se ha instalado un sistema de seguridad nuevo en las torres vendebots para impedir el acceso a los dibus.\"\a\"Los dibus que se encuentren en las torres serán detenidos para su interrogatorio.\"\a\"Nos reuniremos en el vestíbulo para discutir el asunto durante el aperitivo.\"\a\"Firmado, Confraternizadora\"\aMuy, muy interesante. Tengo que pasar esta información inmediatamente.\aTráeme una tercera nota, por favor.",
             },
    3261 : { QUEST : "¡Muy bien _avName_! ¿Qué dice la nota?\a\"Estimados vendebots:\"\a\"Los dibus se las han ingeniado para infiltrarse en las torres vendebot.\"\a\"Esta noche les llamaré a la hora de la cena para darles más datos.\"\a\"Firmado, Televendedor\"\a¡Vaya! Me pregunto cómo estarán colándose los dibus....\aTráeme una última nota. Creo que con eso bastará para hacerme una idea.",
             COMPLETE : "¡Sabía que lo lograrías! A ver, la nota dice....\a\"Estimados vendebots:\"\a\"Ayer comí con el Sr. Hollywood y me dijo que VIP lleva unos días muy ocupado.\"\a\"Sólo recibirá bots que merezcan un ascenso.\"\a\"Se me olvidaba, he quedado con Efusivo para jugar al golf el domingo.\"\a\"Firmado, Fardoncete\"\aBueno, _avName_, muchas gracias por tu valiosa ayuda.\aToma, aquí tienes tu recompensa.",
             },

    3262 : { QUEST : "_toNpcName_ posee información reciente sobre la fábrica-cuartel general vendebot.\aVe a ver de qué se trata._where_" },
    3263 : { GREETING : "¡Qué pasa, colega!",
             QUEST : "Me llamo Don Silvestre, Silvestre a secas para los amigos.\aVoy al grano, que no me gusta andarme por las ramas.\aMira, los vendebots acaban de construir una gran fábrica para reproducirse como hormigas.\aAgénciate a unos cuantos colegas dibus y destruye la dichosa fábrica.\aDentro del cuartel general vendebot deberás localizar el túnel que lleva a la fábrica y luego subir en el ascensor.\aAntes que nada, comprueba que vas bien cargado de bromas y puntos de risa y que te acompañan unos dibus bien fornidos.\aDerrota al capataz dentro de la fábrica y así detendrás el avance vendebot.\a¡Hala! Ahí tienes tu tablita de ejercicios. Un, dos, un, dos.",
             LEAVING : "¡Nos vemos!",
             COMPLETE : "¿Qué pasa, colega? ¡Qué bien te lo has montado en la fábrica!\aAsí que has pillado una pieza de traje bot.\aDebe ser un excedente de la cadena de montaje bot.\aNos podría venir de perlas. Recoge todas las que puedas siempre que tengas un huequecillo.\aA lo mejor, si consigues un traje completo reuniendo todas las piezas, podemos sacarle algún provecho...."
             },

    4001 : {GREETING : "",
            QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsatelo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
            INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
            INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
            COMPLETE : "Muy buena decisión...",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "Ahora tienes que elegir el nuevo circuito de trucos que quieres aprender.\aPiénsatelo todo lo que quieras y vuelve cuando hayas tomado una decisión.",
            INCOMPLETE_PROGRESS : "Antes de elegir, medita tu decisión.",
            INCOMPLETE_WRONG_NPC : "Antes de elegir, medita tu decisión.",
            COMPLETE : "Muy buena decisión...",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "Seguro que a Ropo Pompón le viene bien un poco de ayuda en su investigación._where_",
             },
    4201 : { GREETING: "¡Hola!",
             QUEST : "Estoy muy preocupado con una racha de robos de instrumentos musicales.\aEstoy llevando a cabo un estudio entre mis compañeros comerciantes.\aTal vez pueda encontrar una pauta que me ayude a resolver el caso.\aPásate por Sonatas y sonatinas para que Tina te dé su inventario de concertinas. _where_",
             },
    4202 : { QUEST : "Sí, he hablado con Ropo esta mañana.\aTengo el inventario aquí mismo.\aLlévaselo, ¿vale?_where_"
             },
    4203 : { QUEST : "¡Fantástico! Uno menos...\aAhora ve a por el de Uki._where_",
             },
    4204 : { QUEST : "¡Oh! ¡El inventario!\aMe había olvidado de él.\aSeguro que lo tengo terminado para cuando hayas derrotado a diez bots.\aPásate por aquí después y te prometo que estará listo.",
             INCOMPLETE_PROGRESS : "31, 32... ¡Vaya!\a¡Me has hecho perder la cuenta!",
             GREETING : "",
             },
    4205 : { QUEST : "Ah, ahí estás.\aGracias por darme algo de tiempo.\aLlévale esto a Ropo y salúdale de mi parte._where_",
             },
    4206 : { QUEST : "Mmm, muy interesante.\aAhora sí que estoy dando con ello.\aMuy bien, el último inventario es el de Bibi._where_",
             },
    4207 : { QUEST : "¿Inventario?\a¿Cómo voy a hacerlo si no tengo el formulario?\aVe a ver si Sordino Quena puede darme uno._where_",
             INCOMPLETE_PROGRESS : "¿Alguna novedad sobre el formulario?",
             },
    4208 : { QUEST : "¡Pues claro que tengo un formulario de inventario!\aPero no es gratis, ¿sabes?\a¿Sabes qué? Te lo daré a cambio de una tarta de nata entera.",
             GREETING : "¡Muy buenas!",
             LEAVING : "Hasta luego...",
             INCOMPLETE_PROGRESS : "No me vale con un trozo.\aMe quedaré con hambre. Quiero TODA la tarta.",
             },
    4209 : { GREETING : "",
             QUEST : "Mmm...\a¡Qué rica!\aAquí tienes el formulario para Bibi._where_",
             },
    4210 : { GREETING : "",
             QUEST : "Gracias. Has sido de gran ayuda.\aVeamos... Violines Bibi: 2\a¡Ya está! ¡Aquí tienes!",
             COMPLETE : "Buen trabajo, _avName_.\aSeguro que ahora llego al fondo de la cuestión de los robos.\a¿Por qué no llegas tú al fondo de esto?",
             },

    4211 : { QUEST : "Mira, el doctor Pavo Rotti está llamando cada cinco minutos. ¿Puedes ir a ver qué problema tiene?_where_",
             },
    4212 : { QUEST : "¡Guau! Me alegro de que el cuartel general haya mandado por fin a alguien.\aNo he tenido un solo cliente durante días.\aSon estos malditos contables que hay por todas partes.\aCreo que están propagando una mala higiene bucal entre los vecinos.\aDerrota a diez de ellos y veamos si el negocio mejora.",
             INCOMPLETE_PROGRESS : "Sigo sin tener clientes. ¡Pero sigue luchando!",
             },
    4213 : { QUEST : "¿Sabes? A lo mejor resulta que los culpables no eran los contables.\aIgual son los chequebots en general.\aAcaba con veinte de ellos y tal vez venga alguien por fin a mi clínica.",
             INCOMPLETE_PROGRESS : "Sé que veinte son muchos. Pero seguro que merece la pena.",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡No lo entiendo!\aSigo sin tener ni un solo cliente.\aA lo mejor hay que atacar al origen del problema.\aIntenta reconquistar un edificio de chequebots.\aEso debería bastar.",
             INCOMPLETE_PROGRESS : "¡Por favor! ¡Sólo un pequeño edificio de nada!...",
             COMPLETE : "Sigue sin venir un alma por aquí.\aPero la verdad es que, pensándolo bien...\a¡Tampoco venían clientes antes de que los bots nos invadiesen!\aSin embargo, aprecio de veras tu ayuda.\aSeguro que esto te viene bien."
             },

    4215 : { QUEST : "Olga necesita desesperadamente a alguien que la ayude.\a¿Por qué no te pasas a verla para ver qué puedes hacer?_where_",
             },
    4216 : { QUEST : "¡Gracias por venir tan pronto!\aParece que los bots se han hecho con muchos de los billetes de crucero de mis clientes.\aUki dice que ha visto a un efusivo irse de aquí con un montón.\aMira a ver si puedes recuperar el billete a Alaska de Chopo Chopín.",
             INCOMPLETE_PROGRESS : "Los efusivos pueden estar ya en cualquier sitio...",
             },
    4217 : { QUEST : "¡Estupendo! ¡Lo has encontrado!\a¿Me harías ahora el favor de llevárselo a Chopo Chopín?_where_",
             },
    4218 : { QUEST : "¡Estupendo, estupendísimo!\a¡Alaska, voy para allá!\aYa no soporto a estos malditos bots.\aOye, creo que Olga te vuelve a necesitar._where_",
             },
    4219 : { QUEST : "Sí, lo has adivinado.\aNecesito que sacudas a los pesados de los efusivos para recuperar el billete de Felisa Felina al festival de Jazz.  \aYa sabes cómo funciona...",
               INCOMPLETE_PROGRESS : "Hay más en alguna parte...",
             },
    4220 : { QUEST : "¡Estupendo!\a¿Podrías llevarle también el billete?_where_",
             },
    4221 : { GREETING : "",
             LEAVING : "Hasta luego...",
             QUEST : "¡Hola!\aMe voy de viaje, _avName_.\aAntes de irte, más vale que te pases de nuevo a ver a Olga..._where_",
             },
    4222 : { QUEST : "¡Éste es el último, lo prometo!\aAhora hay que buscar el billete de Barbo para el gran concurso de canto.",
             INCOMPLETE_PROGRESS : "Vamos, _avName_.\aBarbo cuenta contigo.",
             },
    4223 : { QUEST : "Esto hará que Barbo se alegre mucho._where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Vaya, vaya, VAYA!\a¡Sensacional!\a¿Sabes? Este año, los chicos y yo vamos a barrer en el concurso.\aOlga dice que vuelvas por allí para recoger tu recompensa._where_\a¡Adiós, adiós, ADIÓS!",
             COMPLETE : "Gracias por todo, _avName_.\aEres muy valioso aquí en Toontown.\aHablando de cosas valiosas...",
             },

    902 : { QUEST : "Ve a ver a Leo.\aNecesita que alguien entregue un mensaje._where_",
            },
    4903 : { QUEST : "¡Colega!\aMis castañuelas están empañadas y tengo una gran actuación esta noche.\aLlévaselas a Carlos para ver si las puede limpiar._where_",
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
             QUEST : "¡Muy bien, colega!\aTienen una pinta estupenda.\aAhora necesito que consigas una copia de la letra de \"Navidades felices\" de Lírica Tástrofe._where_",
             },
    4908 : { QUEST: "¡Muy buenas!\aMmm, no tengo un ejemplar de esa letra a mano.\aSi me dieses algo de tiempo, la podría escribir de memoria.\a¿Por qué no te vas a recuperar un edificio de dos plantas mientras la escribo?",
             },
    4909 : { QUEST : "Lo siento.\aMi memoria ya no es lo que era.\aSi vas a recuperar un edificio de tres plantas, seguro que tendré la letra lista para cuando vuelvas.",
             },
    4910 : { QUEST : "¡Ya está!\aSiento haber tardado tanto.\aLlévale esto a Leo._where_",
             GREETING : "",
             COMPLETE : "¡Genial, colega!\a¡Mi concierto va a ser la bomba!\aAh, que no se me olvide. Toma, esto te servirá para los bots."
             },
    5247 : { QUEST : "Este barrio es bastante duro...\aTe vendría bien aprender unos cuantos trucos nuevos.\a_toNpcName_ me enseñó todo lo que sé, así que a lo mejor te puede enseñar a ti también._where_" },
    5248 : { GREETING : "Aah, sí.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Parece que mi tarea te está causando problemas.",
             QUEST : "Aaah, un nuevo aprendiz, bienvenido.\aYo sé todo lo que hay que saber sobre las tartas.\aPero antes de empezar con tu entrenamiento, tienes que hacerme una pequeña demostración.\aSal fuera y derrota a diez de los bots más grandes." },
    5249 : { GREETING: "Mmmmm.",
             QUEST : "¡Excelente!\aAhora, demuéstrame tu habilidad como pescador.\aAyer tiré tres dados de goma al estanque.\aPéscalos y tráemelos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Parece que la caña y el sedal no se te dan tan bien." },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán de miedo colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de abogabots más grandes.",
             INCOMPLETE_PROGRESS : "¿Estás teniendo problemas con los edificios?", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán de miedo colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de jefebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Estás teniendo problemas con los edificios?", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán de miedo colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de chequebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Estás teniendo problemas con los edificios?", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Ajá!  Estos dados quedarán de miedo colgados del retrovisor de mi carreta de bueyes.\aAhora demuéstrame que sabes distinguir a los enemigos.\aVuelve cuando hayas reconquistado dos de los edificios de vendebots más grandes.",
             INCOMPLETE_PROGRESS : "¿Estás teniendo problemas con los edificios?", },
    5200 : { QUEST : "Esos bots tan pesados están otra vez dando problemas.\a_toNpcName_ ha informado de que falta otro objeto. Pásate por allí, a ver si puedes arreglar la situación._where__where_" },
    5201 : { GREETING: "",
             QUEST : "Hola, _avName_.  Creo que debo darte las gracias por venir.\aUn grupo de cazacabezas ha estado aquí y se ha llevado mi balón de fútbol.\a¡Su jefe me ha dicho que tenía que hacer un recorte de plantilla y me lo ha quitado!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mi balón?",
             COMPLETE : "¡Yujuuu!  ¡Lo has encontrado! Aquí tienes tu recompensa...",
             },
    5261 : { GREETING: "",
             QUEST : "Hola, _avName_.  Creo que debo darte las gracias por venir.\aUn grupo de doscaras ha estado aquí y se ha llevado mi balón de fútbol.\a¡Su jefe me ha dicho que tenía que hacer un recorte de plantilla y me lo ha quitado!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mi balón?",
             COMPLETE : "¡Yujuuu!  ¡Lo has encontrado! Aquí tienes tu recompensa...",
             },
    5262 : { GREETING: "",
             QUEST : "Hola, _avName_.  Creo que debo darte las gracias por venir.\aUn grupo de monederos ha estado aquí y se ha llevado mi balón de fútbol.\a¡Su jefe me ha dicho que tenía que hacer un recorte de plantilla y me lo ha quitado!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mi balón?",
             COMPLETE : "¡Yujuuu!  ¡Lo has encontrado! Aquí tienes tu recompensa...",
             },
    5263 : { GREETING: "",
             QUEST : "Hola, _avName_.  Creo que debo darte las gracias por venir.\aUn grupo de portavoces ha estado aquí y se ha llevado mi balón de fútbol.\a¡Su jefe me ha dicho que tenía que hacer un recorte de plantilla y me lo ha quitado!\a¿Puedes recuperar el balón?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar mi balón?",
             COMPLETE : "¡Yujuuu!  ¡Lo has encontrado! Aquí tienes tu recompensa...",
             },
    5202 : { QUEST : "Frescolandia ha sido invadida por los bots más duros de pelar que he visto en mi vida.\aMás vale que cargues más bromas.\aMe han dicho que es posible que _toNpcName_ tenga una bolsa más grande en la que te cabrán más bromas._where_" },
    5203 : { GREETING: "¿Eh?  ¿Estás en mi equipo de trineo?",
             QUEST : "¿Qué?  ¿Quieres una bolsa?\aEl caso es que tenía una por aquí... ¿Estará en mi trineo?\aVaya... ¡No he visto mi trineo desde la gran carrera!\a¿Se lo habrá llevado uno de esos bots?",
             LEAVING : "¿Has visto mi trineo?",
             INCOMPLETE_PROGRESS : "¿Quién decías que eras?  Lo siento, estoy un poco mareado por el choque." },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Es ése mi trineo?  No veo ninguna bolsa por aquí.\aCreo que Perico Arenque estaba en el equipo... ¿La tendrá él?_where_" },
    5205 : { GREETING : "¡Oooh, la cabeza!",
             LEAVING : "",
             QUEST : "¿Eh?  ¿Doroteo qué?   ¿Una bolsa?\aAh, ¿no era miembro de nuestro equipo de trineo?\aMe duele tanto la cabeza que no puedo pensar bien.\a¿Puedes pescar unos cuantos cubitos de hielo en el estanque para que me los ponga en la cabeza?",
             INCOMPLETE_PROGRESS : "¡Ayyy, la cabeza me va a estallar!  ¿Tienes un poco de hielo?", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "¡Aaah, así está mucho mejor!\aAsí que buscas la bolsa de Doroteo, ¿eh?\aCreo que acabó en la cabeza de Nutrio Cenutrio después del choque._where_" },
    5207 : { GREETING : "¡Eeeh!",
             LEAVING : "",
             QUEST : "¿Bolsa?  ¿Quién ser Perico?\a¡Yo tener miedo de edificios!  ¡Tú derrotar edificios, yo darte bolsa!",
             INCOMPLETE_PROGRESS : "¡Más edificios!  ¡Yo todavía tener miedo!",
             COMPLETE : "¡Oooh!  ¡Tú gustarme!" },
    5208 : { GREETING : "",
             LEAVING : "¡Eeeh!",
             QUEST : "¡Oooh!  ¡Tú gustarme!\aTú ir a clínica de esquí. Bolsa allí." },
    5209 : { GREETING : "¡Colega!",
             LEAVING : "¡Nos vemos!",
             QUEST : "¡Tío, ese tal Nutrio Cenutrio está loco!\aColega, si estás loco como Nutrio, la bolsa será tuya.\a¡Embólsate a unos cuantos bots y la bolsa será tuya, colega! ¡Vamos!",
             INCOMPLETE_PROGRESS : "¿Estás seguro de que eres bastante bestiajo?  Anda, vete a zurrar a los bots.",
             COMPLETE : "¡Eh, eres todo un campeón!  ¡Has zurrado de lo lindo a un montón de bots!\a¡Aquí tienes la bolsa!" },

    5210 : { QUEST : "_toNpcName_ está enamorada en secreto de alguien del barrio.\aSi la ayudas, te recompensará de lo lindo._where_" },
    5211 : { GREETING: "¡Buaaaa!",
             QUEST : "Me he pasado toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots con pico ha entrado y se la ha llevado.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5264 : { GREETING: "¡Buaaaa!",
             QUEST : "Me he pasado toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots con aleta ha entrado y se la ha llevado.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5265 : { GREETING: "¡Buaaaa!",
             QUEST : "Me he pasado toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots confraternizadores ha entrado y se la ha llevado.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5266 : { GREETING: "¡Buaaaa!",
             QUEST : "Me he pasado toda la noche escribiendo al perro que amo.\aPero antes de que pudiera entregar la carta, uno de esos apestosos bots corporativistas ha entrado y se la ha llevado.\a¿Me haces el favor de recuperarla?",
             LEAVING : "¡Buaaaa!",
             INCOMPLETE_PROGRESS : "Por favor, encuentra mi carta." },
    5212 : { QUEST : "¡Oh, gracias por encontrar la carta!\aPor favor, ¿podrías entregársela al perro más guapo de todo el barrio?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No has entregado la carta, ¿verdad?",
             },
    5213 : { GREETING : "Encantado de verte.",
             QUEST : "Lo siento, pero no puedo molestarme con tu carta.\a¡Me han quitado a todos mis perritos!\aTráemelos y hablaremos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡Mis pobres perritos!" },
    5214 : { GREETING : "",
             LEAVING : "¡Hasta luego!",
             QUEST : "Gracias por devolverme a mis preciosidades.\aEchemos un vistazo a tu carta...\nMmmm, parece que tengo otra admiradora secreta.\aEsto pide a gritos una visita a mi querido amigo Carlos Congelado.\a¡Seguro que te cae muy bien!_where_" },
    5215 : { GREETING : "Je, je...",
             LEAVING : "Vuelve, sí, sí.",
             INCOMPLETE_PROGRESS : "Todavía quedan unos cuantos grandullones.  Vuelve cuando ya no estén.",
             QUEST : "¿Quién te ha enviado?  No me gustan los forasteros, no...\aPero todavía me gustan menos los bots...\aAcaba con los grandotes y ya veremos si te ayudo." },
    5216 : { QUEST : "Te he dicho que te vamos a ayudar.\aAsí que llévale este anillo a la chica.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡¿Sigues teniendo el anillo?!",
             COMPLETE : "¡Oh, queriiiido! ¡¡¡Gracias!!!\aAh, también tengo algo especial para ti.",
             },
    5217 : { QUEST : "Parece que a _toNpcName_ le vendría bien algo de ayuda._where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguro que hay confraternizadores por algún sitio.",
             QUEST : "¡¡¡Socorro!!! ¡¡¡Socorro!!! ¡Ya no lo aguanto más!\a¡Esos confraternizadores me están volviendo tarumba!" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "No pueden ser todos.  ¡Sólo he visto a uno!",
             QUEST : "¡Vaya, gracias, pero ahora se trata de los corporativistas!\a¡Tienes que ayudarme!" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¡No, no, no, había uno justo aquí!",
             QUEST : "¡Ahora me doy cuenta de que son esos prestamistas despiadados!\a¡Creía que ibas a salvarme!" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "¿Sabes qué? ¡A lo mejor la culpa no es de los bots!\a¿Puedes pedirle a Pega Moide que me prepare una poción calmante?  A lo mejor eso ayuda..._where_" },
    5222 : { LEAVING : "",
             QUEST : "¡El tal Cris Térico es todo un personaje!\a¡Voy a prepararle algo que le pondrá a tono!\aVaya, parece que me he quedado sin aletas de sardina...\aPórtate bien y ve al estanque a pescarme unas cuantas.",
             INCOMPLETE_PROGRESS : "¿Ya has conseguido las aletas?", },
    5223 : { QUEST : "Vale.  Gracias, cariño.\aToma, ahora llévale esto a Cris.  Seguro que se calma enseguida.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Vamos, llévale la poción a Cris.",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Hazme el favor de acabar con los picapleitos ¿vale?",
             QUEST : "¡Oh, gracias a Dios que has vuelto!\a¡¡¡Dame la poción, rápido!!!\aGlu, glu, glu...\a¡Puaj, qué mal sabía!\aPero ¿sabes qué?  Me siento mucho más tranquilo.  Ahora que puedo pensar con claridad, me doy cuenta de que...\a¡¡¡Eran los picapleitos los que me volvían loco todo el rato!!!",
             COMPLETE : "¡Es estupendo!  ¡Ahora puedo relajarme!\aSeguro que por aquí hay algo que pueda darte.  ¡Toma!" },
    5225 : { QUEST : "Desde el incidente del bocadillo de nabos, Felipe el gruñón ha estado enfadado con _toNpcName_. \aA lo mejor puedes ayudar a Frigo a arreglar las cosas entre ellos._where_" },
    5226 : { QUEST : "Sí, seguro que te han contado que Felipe el gruñón está enfadado conmigo...\aSólo intentaba ser amable regalándole un bocadillo de nabos.\aA lo mejor puedes animarle.\aFelipe odia a los chequebots, sobre todo sus edificios. \aSi reconquistas unos cuantos edificios de chequebots, tal vez sirva de algo.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Y si lo intentas con unos cuantos edificios más?", },
    5227 : { QUEST : "¡Es fantástico!  Ve a contar a Felipe lo que has hecho._where_" },
    5228 : { QUEST : "Vaya, eso ha hecho, ¿eh?\aEse Frigo cree que puede arreglarlo todo así de fácil, ¿eh?\a¡Me rompí una muela con ese bocadillo de nabos que me dio!\aQuizá si le llevas la muela al doctor Bocamaraca, él pueda arreglarla.",
             GREETING : "Brrrrr.",
             LEAVING : "Grrñññ, grññññ.",
             INCOMPLETE_PROGRESS : "¿Tú otra vez?  ¡Creía que ibas a arreglarme la muela!",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela.  Tardaré un poquito más.",
             QUEST : "Sí, la muela tiene bastante mala pinta, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos chequebots?\aEstán asustando a mis pacientes." },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela.  Tardaré un poquito más.",
             QUEST : "Sí, la muela tiene bastante mala pinta, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos vendebots?\aEstán asustando a mis pacientes." },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela.  Tardaré un poquito más.",
             QUEST : "Sí, la muela tiene bastante mala pinta, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos abogabots?\aEstán asustando a mis pacientes." },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Sigo trabajando en la muela.  Tardaré un poquito más.",
             QUEST : "Sí, la muela tiene bastante mala pinta, la verdad.\aA lo mejor puedo hacer algo, pero tardaré un poco.\aMientras tanto, ¿podrías limpiar la zona de esos jefebots?\aEstán asustando a mis pacientes." },
    5230 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aHe desistido de intentar arreglar la muela, y en su lugar, le he fabricado a Felipe una nueva, de oro.\aPor desgracia, un barón ladrón me la ha birlado.\aSi te das prisa, a lo mejor consigues atraparle.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya la muela?" },
    5270 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aHe desistido de intentar arreglar la muela, y en su lugar, le he fabricado a Felipe una nueva, de oro.\aPor desgracia, un pez gordo me la ha birlado.\aSi te das prisa, a lo mejor consigues atraparle.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya la muela?" },
    5271 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aHe desistido de intentar arreglar la muela, y en su lugar, le he fabricado a Felipe una nueva, de oro.\aPor desgracia, un Sr. Hollywood me la ha birlado.\aSi te das prisa, a lo mejor consigues atraparle.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya la muela?" },
    5272 : { GREETING: "",
             QUEST : "¡Me alegro de que hayas vuelto!\aHe desistido de intentar arreglar la muela, y en su lugar, le he fabricado a Felipe una nueva, de oro.\aPor desgracia, un pelucón me la ha birlado.\aSi te das prisa, a lo mejor consigues atraparle.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya la muela?" },
    5231 : { QUEST : "¡Estupendo, ésa es la muela!\a¿Por qué no me haces el favor de llevársela a Felipe?",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguro que Felipe está impaciente por ver su nueva muela.",
             },
    5232 : { QUEST : "Oh, gracias.\aUmmmmf\a¿Qué tal estoy, eh?\aBueno, puedes decirle a Frigo que le perdono.",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "Oh, me alegro muchísimo de oír eso.\aMe imaginaba que el cascarrabias de Felipe no podría seguir enfadado conmigo.\aComo gesto de amistad, le he preparado este bocadillo de piñones.\a¿Me haces el favor de llevárselo? ",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Date prisa, por favor.  El bocadillo de piñones está más rico cuando está calentito.",
             COMPLETE : "Vaya, ¿qué es esto?  ¿Es para mí?\aÑam, ñam....\a¡Aaay!  ¡Mi muela!  ¡Ese Frigo Sabañón!\aBueno, vale, no ha sido culpa tuya.  Toma, llévate esto como recompensa por tu esfuerzo.",
             },
    903 : { QUEST : "Creo que estás listo para ir a ver a _toNpcName_, en Ventisca a la vista, para tu prueba final._where_", },
    5234 : { GREETING: "",
             QUEST : "Ah, has vuelto.\aAntes de empezar, tenemos que comer algo.\aTráenos un poco de queso abultado para el caldo.\aEl queso abultado sólo se puede conseguir de los bots peces gordos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguimos necesitando queso abultado." },
    5278 : { GREETING: "",
             QUEST : "Ah, has vuelto.\aAntes de empezar, tenemos que comer algo.\aTráenos un poco de caviar para el caldo.\aEl caviar sólo se puede conseguir de los bots Sr. Hollywood.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Seguimos necesitando caviar." },
    5235 : { GREETING: "",
             QUEST : "Los hombres sencillos comen con cucharas sencillas.\aUn bot se ha llevado mi cuchara sencilla, así que sencillamente, no puedo comer.\aTráeme mi cuchara. Creo que un barón ladrón se la ha llevado.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Es sencillo: debo recuperar la cuchara." },
    5279 : { GREETING: "",
             QUEST : "Los hombres sencillos comen con cucharas sencillas.\aUn bot se ha llevado mi cuchara sencilla, así que no puedo comer.\aTráeme mi cuchara. Creo que un pelucón se la ha llevado.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Es sencillo: debo recuperar la cuchara." },
    5236 : { GREETING: "",
             QUEST : "Oh, gracias.\aSlurp, slurp...\aAaah, ahora tienes que atrapar a un sapo parlanchín.  Ponte a pescar en el estanque.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el sapo parlanchín?" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "Todavía no has conseguido el postre.",
              QUEST : "Vaya, no cabe duda de que es un sapo parlanchín.  Dámelo.\a¿Qué dices, sapo?\aVaya vaya.\aVaya vaya...\aEl sapo ha hablado.  Necesitamos un postre.\aTráenos unos cuantos cucuruchos de helado de _toNpcName_.\aPor algún motivo, al sapo le gusta el helado de judías pintas._where_", },
    5238 : { GREETING: "",
             QUEST : "Así que te ha enviado Fredo Dedo.   Siento decirte que nos hemos quedado sin cucuruchos de helado de judías pintas.\aVerás, un montón de bots ha entrado y se los ha llevado.\aHan dicho que eran para un señor de Hollywood o algo así.\aTe agradecería mucho que los recuperases.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya los cucuruchos de helado?" },
    5280 : { GREETING: "",
             QUEST : "Así que te ha enviado Fredo Dedo.   Siento decirte que nos hemos quedado sin cucuruchos de helado de judías pintas.\aVerás, un montón de bots ha entrado y se los ha llevado.\aHan dicho que eran para el pez gordo o algo así.\aTe agradecería mucho que los recuperases.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado ya los cucuruchos de helado?" },
    5239 : { QUEST : "¡Gracias por recuperar los cucuruchos de helado!\aAquí tienes uno para Fredo Dedo.",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Más vale que le lleves el helado a Fredo Dedo antes de que se derrita.", },
    5240 : { GREETING: "",
             QUEST : "Muy bien.  Aquí tienes, sapo...\aSlurp, slurp...\aMuy bien, estamos casi listos.\aSi pudieses traerme un poco de talco para secarme las manos...\aCreo que los bots pelucones llevan a veces polvos de talco en la peluca.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado talco?" },
    5281 : { GREETING: "",
             QUEST : "Muy bien.  Aquí tienes, sapo...\aSlurp, slurp...\aMuy bien, estamos casi listos.\aSi pudieses traerme un poco de talco para secarme las manos...\aCreo que los bots Sr. Hollywood llevan a veces polvos de talco para empolvarse la nariz.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has encontrado talco?" },
    5241 : { QUEST : "Vale.\aComo dije en su día, para lanzar bien una tarta, no se debe usar la mano...\a... sino con el alma.\aNo sé qué significa eso, así que me sentaré a contemplar cómo reconquistas edificios.\aVuelve cuando hayas terminado tu tarea.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Tu tarea todavía no ha terminado.", },
    5242 : { GREETING: "",
             QUEST : "Aunque sigo sin saber de qué hablo, no cabe duda de que eres de gran valor.\aTe asigno una tarea final...\aAl sapo parlanchín le gustaría tener una novia.\aBusca otro sapo parlanchín.  El sapo ha hablado.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el otro sapo parlanchín?",
             COMPLETE : "¡Guau!  Estoy cansado de todo este esfuerzo.  Voy a descansar.\aToma, ten tu recompensa y márchate." },

    5243 : { QUEST : "Pedro Glaciares está empezando a apestar la calle.\a¿Puedes convencerle de que se dé una ducha?_where_" },
    5244 : { GREETING: "",
             QUEST : "Sí, supongo que suelo sudar bastante aquí.\aMmm, a lo mejor si pudiese arreglar la tubería que gotea en mi ducha...\aSupongo que un engranaje de esos bots diminutos me servirá.\aVe a por un engranaje de un microgerente y lo intentaremos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Dónde está el engranaje ese que me ibas a traer?" },
    5245 : { GREETING: "",
             QUEST : "Sí, parece que eso ha funcionado.\aPero cuando me ducho me siento solo...\a¿Podrías ir a pescarme un patito de goma para que me haga compañía?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar el patito?" },
    5246 : { QUEST : "El patito es estupendo, pero...\aTodos esos edificios alrededor me ponen nervioso.\aMe sentiría mucho más relajado si hubiese menos edificios cerca.",
             LEAVING : "",
             COMPLETE : "Vale, me voy a dar una ducha.  Toma, esto es para ti.",
             INCOMPLETE_PROGRESS : "Siguen preocupándome los edificios.", },
    5251 : { QUEST : "Creo que Pago Gelado va a dar un recital esta noche.\aMe han dicho que el material del concierto le está dando problemas._where_" },
    5252 : { GREETING: "",
             QUEST : "¡Ah, sí!  Pues claro que me viene bien algo de ayuda.\a"+TheCogs+" han venido y me han robado todo el equipo mientras descargaba la furgoneta.\a¿Puedes echarme una mano recuperando el micrófono?",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "Oye, tío, no puedo cantar sin un micrófono." },
    5253 : { GREETING: "",
             QUEST : "¡Sí, ése es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\aLo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo ha llevado uno de esos corporativistas.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar el teclado?" },
    5273 : { GREETING: "",
             QUEST : "¡Sí, ése es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\aLo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo ha llevado uno de esos confraternizadores.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar el teclado?" },
    5274 : { GREETING: "",
             QUEST : "¡Sí, ése es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\aLo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo ha llevado uno de esos prestamistas despiadados.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar el teclado?" },
    5275 : { GREETING: "",
             QUEST : "¡Sí, ése es mi micrófono, muy bien!\aGracias por recuperarlo, pero...\aLo que necesito de verdad es el teclado para poder tocar unas cuantas notas.\aCreo que se lo ha llevado uno de esos picapleitos.",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "¿Has conseguido encontrar el teclado?" },
    5254 : { GREETING: "",
             QUEST : "¡Muy bien!  Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que han terminado en manos de un Sr. Hollywood.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!!  Ahora sí que estoy listo.\a¡Hola, Frescolandia!\a¿Eh?  ¿Dónde está la gente?\aVale, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5282 : { GREETING: "",
             QUEST : "¡Muy bien!  Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que han terminado en manos de un pez gordo.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!!  Ahora sí que estoy listo.\a¡Hola, Frescolandia!\a¿Eh?  ¿Dónde está la gente?\aVale, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5283 : { GREETING: "",
             QUEST : "¡Muy bien!  Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que han terminado en manos de un barón ladrón.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!!  Ahora sí que estoy listo.\a¡Hola, Frescolandia!\a¿Eh?  ¿Dónde está la gente?\aVale, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
             INCOMPLETE_PROGRESS : "No querrás que actúe descalzo, ¿no? " },
    5284 : { GREETING: "",
             QUEST : "¡Muy bien!  Ahora podré actuar.\aSi no se hubiesen llevado mis zapatos de plataforma...\aSeguro que han terminado en manos de un pelucón.",
             LEAVING : "",
             COMPLETE : "¡¡Fantástico!!  Ahora sí que estoy listo.\a¡Hola, Frescolandia!\a¿Eh?  ¿Dónde está la gente?\aVale, toma esto y tráeme unos cuantos fans, ¿de acuerdo?",
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
             COMPLETE : "Vale, pero estoy seguro de que te dije que te ocupases de unos cuantos abogabots.\aBueno, si tú lo dices... Pero me debes una.",
             INCOMPLETE_PROGRESS : "Creo que todavía no has terminado.",
             QUEST : "¿Dices que has terminado?  ¿Has derrotado a todos los bots?\aMe debes de haber entendido mal; nuestro trato se refería a los vendebots.\aEstoy segurísimo de que te dije que te ocupases de unos cuantos vendebots." },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "Vale, pero estoy seguro de que te dije que te ocupases de unos cuantos abogabots.\aBueno, si tú lo dices... Pero me debes una.",
             INCOMPLETE_PROGRESS : "Creo que todavía no has terminado.",
             QUEST : "¿Dices que has terminado?  ¿Has derrotado a todos los bots?\aMe debes de haber entendido mal, nuestro trato se refería a los chequebots.\aEstoy segurísimo de que te dije que te ocupases de unos cuantos chequebots." },
    }

# ChatGarbler.py
ChatGarblerDog = ["guau", "arf", "grrrr"]
ChatGarblerCat = ["miau", "miao"]
ChatGarblerMouse = ["ñic", "ñiiiic", "ñic ñic"]
ChatGarblerHorse = ["relincho", "brrr"]
ChatGarblerRabbit = ["iiik", "ipr", "iiipi", "iiiki"]
ChatGarblerDuck = ["cuac", "cuaaac ", "cuac cuac"]
ChatGarblerMonkey = ["ooh", "ooo", "ahh"]
ChatGarblerDefault = ["bla"]

# AvatarDNA.py
Bossbot = "Jefebot"
Lawbot = "Abogabot"
Cashbot = "Chequebot"
Sellbot = "Vendebot"
BossbotS = "un Jefebot"
LawbotS = "un Abogabot"
CashbotS = "un Chequebot"
SellbotS = "un Vendebot"
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

# AvatarDetailPanel.py
AvatarDetailPanelOK = "Aceptar"
AvatarDetailPanelCancel = "Cancelar"
AvatarDetailPanelClose = "Cerrar"
AvatarDetailPanelLookup = "Buscando detalles de %s."
AvatarDetailPanelFailedLookup = "Imposible obtener detalles de %s."
AvatarDetailPanelOnline = "Distrito: %(district)s\nLocalidad: %(location)s"
AvatarDetailPanelOffline = "Distrito: sin conexión\nLocalidad: sin conexión"

# AvatarPanel.py
AvatarPanelFriends = "Amigos"
AvatarPanelWhisper = "Susurrar"
AvatarPanelSecrets = "Secretos"
AvatarPanelGoTo = "Ir a"
AvatarPanelPet = "Show Doodle"
AvatarPanelIgnore = "No hacer caso"
#AvatarPanelCogDetail = "Depart.: %s\nNivel: %s\n"
AvatarPanelCogLevel = "Nivel: %s"
AvatarPanelCogDetailClose = "Cerrar"

# DistributedAvatar.py
WhisperNoLongerFriend = "%s ha abandonado tu lista de amigos."
WhisperNowSpecialFriend = "¡%s es ahora tu amigo secreto!"
WhisperComingToVisit = "%s viene a verte."
WhisperFailedVisit = "%s ha intentado venir a verte."
WhisperTargetLeftVisit = "%s se ha ido a otro sitio. ¡Prueba de nuevo!"
WhisperGiveupVisit = "%s no ha podido encontrarte porque te estás moviendo."
WhisperIgnored = "¡%s no te está haciendo caso!"
TeleportGreeting = "Hola, %s."
DialogSpecial = "ooo"
DialogExclamation = "!"
DialogQuestion = "?"
# Cutoff string lengths to determine how much barking to play
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# LocalAvatar.py
FriendsListLabel = "Amigos"
#WhisperFriendComingOnline = "¡%s se está conectando!"
#WhisperFriendLoggedOut = "%s ha cerrado la sesión."

# TeleportPanel.py
TeleportPanelOK = "Aceptar"
TeleportPanelCancel = "Cancelar"
TeleportPanelYes = "Sí"
TeleportPanelNo = "No"
TeleportPanelCheckAvailability = "Intentando ir a %s."
TeleportPanelNotAvailable = "%s está ocupado ahora mismo. Inténtalo más tarde."
TeleportPanelIgnored = "%s no te está haciendo caso."
TeleportPanelNotOnline = "%s no está conectado ahora mismo."
TeleportPanelWentAway = "%s se ha marchado."
TeleportPanelUnknownHood = "¡No sabes cómo llegar a %s!"
TeleportPanelUnavailableHood = "%s no está disponible ahora mismo. Inténtalo más tarde."
TeleportPanelDenySelf = "¡No puedes ir tú solo!"
TeleportPanelOtherShard = "%(avName)s está en el distrito %(shardName)s, y tú estás en el distrito %(myShardName)s. ¿Quieres cambiarte a %(shardName)s?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "Soy el jefe."

# DistributedBattleFactory.py
FactoryBossTaunt = "Soy el capataz."
FactoryBossBattleTaunt = "Te presento al capataz."

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
    ["¿Cuál es el hombre que piensa más profundo?",
     "El minero."],
    ["¿Cómo se dice suspense en chino?",
     "¡Cha cha cha chaaaaan!"],
    ["¿Qué le dice el pingüino a la pingüina?",
     "Te quiero como a ningüina."],
    ["¿Qué le dice la pelota a la raqueta? ",
     "Lo nuestro es imposible, siempre me estás pegando..."],
    ["¿Qué le dice un poste a otro poste?",
     "Póstate bien."],
    ["¿Qué le dice un caimán mexicano a otro?",
     "¡Cai-manito!"],
    ["¿Cuál es la sal que peor huele?",
     "La sal-pargatas."],
    ["¿Qué es un punto verde en una esquina?",
     "Un guisante castigado."],
    ["¿Cómo se dice 99 en chino?",
     "Cachi-chien."],
    ["¿Por qué en Lepe ponen ajos en la carretera nacional?",
     "Porque son buenos para la circulación."],
    ["¿Qué es más asqueroso que encontrarse un gusano en una manzana?",
     "Encontrar sólo medio gusano."],
    ["¿Quién invento las fracciones?",
     "Enrique Octavo."],
    ["¿Quién mató al libro de lengua?",
     "El sujeto."],
    ["¿Qué hora es cuando un elefante se sienta en una valla?",
     "La hora de ponerla nueva."],
    ["¿Por qué los elefantes no pueden montar en bicicleta?",
     "Porque no tienen dedo gordo para tocar el timbre."],
    ["¿Cómo se meten cuatro elefantes en un Mini?",
     "Pues dos delante y dos detrás."],
    ["¿Cuántos psicoanalistas hacen falta para cambiar una bombilla?",
     "Uno, pero la bombilla tiene que querer ser cambiada."],
    ["¿Por qué los flamencos se sostienen sobre una sola pata?",
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
     "Si te picas, pierdes."],
    ["¿Qué le dice un ojo a otro?",
     "Estamos separados por narices."],
    ["¿Cuál es el último animal acuático?",
     "El delfín."],
    ["¿Por qué es la cebra el animal más antiguo de la selva?",
     "Porque está en blanco y negro."],
    ["¿Por qué las películas de Chaplin eran mudas?",
     "Porque el director siempre decía: ¡No charles, Chaplin! "],
    ["¿Por qué los perros persiguen a los coches?",
     "Porque llevan un gato en el maletero."],
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
     "- Pues sí, estoy aquí calentito."],
    ["Ring, ring - Hola, ¿está Cholo?",
     "No, estoy acompañado."],
    ["Ring, ring - Hola, ¿está Alberto?",
     "- ¡No, está celado!"],
    ["Ring, ring - Hola, ¿está Conchita?",
     "- No, estoy con Tarzán."],
    ["¿Cuál es el colmo de la lírica?",
     "Haber tenido un plácido domingo."],
    ["¿Cuál es el colmo de un carnicero?",
     "Tener un hijo chuleta."],
    ["¿Cuál es el colmo de un forzudo?",
     "Doblar una esquina."],
    ["¿Cuál es el colmo de un sastre?",
     "Tener un hijo botones que se case con una americana."],
    ["¿Cuál es el colmo de un carpintero?",
     "Tener una hija cómoda y otra coqueta."],
    ["¿Cuál es el colmo de un arquitecto?",
     "Construir castillos en el aire."],
    ["¿Cuál es el colmo de un peluquero?",
     "Perder el tren por los pelos."],
    ["¿Cuál es el colmo de un caballo?",
     "Tener silla y no poder sentarse."],
    ["¿Cuál es el colmo de un albañil?",
     "Tener una hija paleta."],
    ["¿Cuál es el colmo de un fotógrafo?",
     "Que se le rebelen los hijos."],
    ["¿Cuál es el colmo de la pereza?",
     "Levantarse dos horas antes para estar más tiempo sin hacer nada."],
    ["¿Cuál es el colmo de un jardinero?",
     "Que su novia se llame Rosa y lo deje plantado."],
    ["¿Cuál es el colmo de los colmos?",
     "Sentarse en un pajar y pincharse con la aguja."],
    ["¿Cuál es el colmo de un electricista?",
     "Que su mujer se llame Luz y sus hijos le sigan la corriente."],
    ["¿Cuál es el colmo de un libro?",
     "Que en otoño se le caigan las hojas."],
    ["¿Cuál es el colmo de una ballena?",
     "Ir vacía."],
    ["¿Cuál es el colmo de un policía?",
     "Denunciar a un huracán por exceso de velocidad. "],
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
    ["¿Por qué ha llevado Goofy el peine al dentista?",
     "Porque ha perdido todos los dientes."],
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
    ["¿Cuál es el colmo de un charcutero?",
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
    ["¿Por qué era el matemático un infeliz?",
     "Porque tenía muchos problemas."],
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
     "Ponerle una tirita a la leche cortada."],
    ["¿Cuál es el colmo de un camello?",
     "Vivir toda la vida jorobado."],
    ["¿Cuál es colmo de un cementerio?",
     "Estar cerrado por defunción."],
    ["¿Cuál es el colmo de una sardina?",
     "Que le dé lata."],
    ["¿Cuál es el colmo de un cóctel?",
     "Sentirse agitado."],
    ["¿Cuál es el colmo de un granjero?",
     "Dejar abierta la puerta del corral para que se ventile."],
    ["¿Cuál es la palabra más larga del mundo?",
     "Arroz, porque empieza con A y termina con Z."],
    ["¿Cuál es el animal que ve menos?",
     "La venada."],
    ["¿Cuál es el animal más fiero? ",
     "El lopintan, porque no es tan fiero el león como lopintan."],
    ["¿Cuál es el perro más explosivo?",
     "El vol-can."],
    ["¿Cuál es el animal que juega al ajedrez?",
     "El caballo."],
    ["¿Qué es un codo? ",
     "Un gdupo de niñods cantodes."],
    ["¿En que se parece una cueva a un frigorífico? ",
     "La cueva tiene estalactitas y estalagmitas y el frigorífico esta latita de atún, esta latita de anchoas..."],
    ["- Doctor, me siento mal.",
     "- Pues siéntese bien."],
    ["- Hoy tose usted mejor que ayer.",
     "- Sí, doctor... He estado ensayando toda la noche."],
    ["- Doctor, doctor... ¿cómo sé si estoy perdiendo la memoria? ",
     "- Eso ya se lo dije ayer."],
    ["- Doctor, ¿qué me aconseja para evitar resfriarme de nuevo? ",
     "Conservar el resfriado que tiene ahora."],
    ["- Doctor, doctor, sigo pensando que soy invisible.",
     "- ¿Quién ha dicho eso?"],
    ["- Doctor, doctor, el pelo se me está cayendo. ¿Cómo puedo conservarlo?",
     "- Tome una caja de zapatos."],
    ["- Doctor, doctor, hace dos semanas que no como ni duermo. ¿Qué tengo? ",
     "- Seguramente sueño y hambre."],
    ["- Doctor, doctor, vengo a que me reconozca.",
     "- Pues ahora mismo no caigo."],
    ["- Doctor, doctor, es que tengo un hueso fuera...",
     "- Pues dígale que pase."],
    ["- Doctor, doctor que se me juntan las letras.",
     "- Pues páguelas, páguelas..."],
    ["- Doctor, doctor, cuando tomo café se me ponen los ojos morados.",
     "- ¿Ha probado a apartar la cucharilla?"],
    ["- ¡¡Doctor, doctor, vengo a que me osculte!!",
     "- ¡Rápido, detrás del sillón!"],
    ["- Doctor, tengo los dientes muy amarillos, ¿qué me recomienda?",
     "- Una corbata marrón."],
    ["- Mamá, mamá, en el cole me llaman despistado.",
     "- Anda, niño, vete a tu casa."],
    ["- Mamá, mamá, en el colegio me llaman despistado.",
     "- SU TABACO, GRACIAS."],
    ["- Mamá, mamá, ¿cuándo vamos a comer pan de hoy?",
     "- Mañana, hijo, mañana."],
    ["- ¡Mamá, mamá, están golpeando la puerta!",
     "- Déjala que se defienda sola."],
    ["- Mamá, mamá... ¿por qué me llaman pies grandes en el cole?",
     "No lo sé, pero ¿has guardado los zapatos en el garaje?"],
    ["- Mamá, ¿qué es la amnesia?",
     "- ¿Qué? ¿Quién eres?"],
    ["- Camarero, camarero, ¿qué hace esta mosca en mi sopa? ",
     "- Yo diría que braza australiana, señor."],
    ["- Camarero, camarero, ¿me aliña la ensalada? ",
     "- Con el uno pepino, con el dos tomate, con el tres cebolla..."],
    ["- ¿Cómo ha encontrado el señor el solomillo?",
     "- De milagro, oiga, de milagro."],
    ["- Camarero, camarero, está usted metiendo la corbata en mi sopa.",
     "- No se preocupe, señor, no encoge."],
    ["- Camarero, ¡ya le he pedido cien veces un vaso de agua! ",
     "- ¡Cien vasos de agua para el señor!"],
    ["- Camarero, camarero, hay una mosca muerta en mi sopa.",
     "- ¿Y qué esperaba por este precio? ¿Una viva?"],
    ["- Camarero, ¿el pescado viene solo?",
     "- No, se lo traigo yo."],
    ["- Camarero, un café solo, por favor.",
     "- ¡Todo el mundo fuera!"],
    ["- ¡Capitán, capitán, que vamos a pique! ",
     "-¡He dicho yo que vamos a Cádiz y vamos a Cádiz!"],
    ["- Capitán, capitán, ¡nos hundimos!",
     "- ¡Pero bobo, si estamos en un submarino!"],
    ["- ¡Capitán, capitán, hemos perdido la guerra! ",
     "- Pues buscadla enseguida."],
    ["- ¡Soldado, ice la bandera!",
     "- Le felicito mi general, le quedó muy bonita."],
    ["- ¡Soldados, presenten armas!",
     "- Aquí mi general, aquí mi fusil."],
    ["- Mi capitán, los soldados no aguantan más, estamos a 42º a la sombra.",
     "- Está bien sargento, pueden descansar diez minutos al sol."],
    ["- Por favor, ¿la calle Sagasta?",
     "- Hombre, si pisa fuerte..."],
    ["- Oiga, que este reloj no anda.",
     "- Claro, todavía no tiene un año."],
    ["- Camarero, póngame un café corto.",
     "- Se me ha roto la máquina, cambio."],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("ji","je","ja","jua, jua")
MovieHealLaughterHits1= ("Ja, ja, ja","ji, ji","Je, je, je","Ja, ja")
MovieHealLaughterHits2= ("¡JUA, JUA, JUA!","¡JUO, JUO, JUO!","¡JA, JA, JA!")

# MovieSOS.py
MovieSOSCallHelp = "¡SOCORRO %s!"
MovieSOSWhisperHelp = "¡%s necesita que le ayuden en el combate!"
MovieSOSObserverHelp = "¡SOCORRO!"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "¡Hola, %s! ¡Me alegra poder ayudarte!"
MovieNPCSOSGoodbye = "¡Nos vemos!"
MovieNPCSOSToonsHit = "¡Los dibus aciertan siempre!"
MovieNPCSOSCogsMiss = "¡"+TheCogs+" fallan siempre!"
MovieNPCSOSRestockGags = "Reaprovisionamiento de %s bromas"
MovieNPCSOSHeal = "Curadibu"
MovieNPCSOSTrap = "Trampa"
MovieNPCSOSLure = "Cebo"
MovieNPCSOSSound = "Sonido"
MovieNPCSOSThrow = "Lanzamiento"
MovieNPCSOSSquirt = "Chorro"
MovieNPCSOSDrop = "Caída"
MovieNPCSOSAll = "Todo"

# MovieSuitAttacks.py
MovieSuitCancelled = "CANCELADO\nCANCELADO\nCANCELADO"

# RewardPanel.py
RewardPanelToonTasks = "Dibutareas"
RewardPanelItems = "Objetos recuperados"
RewardPanelMissedItems = "Objetos no recuperados"
RewardPanelQuestLabel = "Tarea %s"
RewardPanelCongratsStrings = ["¡Así se hace!", "¡Enhorabuena!", "¡Guau!",
                              "¡Chupi!", "¡Impresionante!", "¡Dibufantástico!"]
RewardPanelNewGag = "¡Nueva broma %(gagName)s para %(avName)s!"
RewardPanelMeritsMaxed = "Máxima puntuación"
RewardPanelMeritBarLabel = "Méritos"
RewardPanelMeritAlert = "¡Listo para un ascenso!"

RewardPanelCogPart = "Has conseguido una pieza de disfraz de bot"

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
CheesyEffectHours = "Durante los próximas %(time)s horas, %(effectName)s%(whileIn)s."
CheesyEffectDays = "Durante los próximos %(time)s días, %(effectName)s%(whileIn)s."
CheesyEffectWhileYouAreIn = " mientras estás en %s"
CheesyEffectExceptIn = ", excepto en %s"


# SuitBattleGlobals.py
SuitFlunky = "Secuaz"
SuitPencilPusher = "Chupatintas"
SuitYesman = "Sonriente"
SuitMicromanager = "Micro\3gerente"
SuitDownsizer = "Regulador de Empleo"
SuitHeadHunter = "Cazacabezas"
SuitCorporateRaider = "Corporati\3vista"
SuitTheBigCheese = "Pez Gordo"
SuitColdCaller = "Gorrón"
SuitTelemarketer = "Tele\3vendedor"
SuitNameDropper = "Fardoncete"
SuitGladHander = "Efusivo"
SuitMoverShaker = "Mandamás"
SuitTwoFace = "Doscaras"
SuitTheMingler = "Confrater\3nizadora"
SuitMrHollywood = "Sr. Hollywood"
SuitShortChange = "Calderilla"
SuitPennyPincher = "Cacomatraco"
SuitTightwad = "Roñoso"
SuitBeanCounter = "Cuenta cuentos"
SuitNumberCruncher = "Contable"
SuitMoneyBags = "Monedero"
SuitLoanShark = "Prestamista Despiadado"
SuitRobberBaron = "Barón ladrón"
SuitBottomFeeder = "Morrudo"
SuitBloodsucker = "Chupa\3sangres"
SuitDoubleTalker = "Embaucador"
SuitAmbulanceChaser = "Persigue Ambulancias"
SuitBackStabber = "Apuña la Espaldas"
SuitSpinDoctor = "Portavoz"
SuitLegalEagle = "Picapleitos"
SuitBigWig = "Pelucón"

# Singular versions (indefinite article)
SuitFlunkyS = "un Secuaz"
SuitPencilPusherS = "un Chupatintas"
SuitYesmanS = "un Sonriente"
SuitMicromanagerS = "una Micro\3gerente"
SuitDownsizerS = "un Regulador de Empleo"
SuitHeadHunterS = "un Cazacabezas"
SuitCorporateRaiderS = "un Corporati\3vista"
SuitTheBigCheeseS = "un Pez gordo"
SuitColdCallerS = "un Gorrón"
SuitTelemarketerS = "un Tele\3vendedor"
SuitNameDropperS = "un Fardoncete"
SuitGladHanderS = "un Efusivo"
SuitMoverShakerS = "un Mandamás"
SuitTwoFaceS = "un Doscaras"
SuitTheMinglerS = "una Confrater\3nizadora"
SuitMrHollywoodS = "un Sr. Hollywood"
SuitShortChangeS = "un Calderilla"
SuitPennyPincherS = "un Cacomatraco"
SuitTightwadS = "un Roñoso"
SuitBeanCounterS = "un Cuenta Cuentos"
SuitNumberCruncherS = "una Contable"
SuitMoneyBagsS = "un Monedero"
SuitLoanSharkS = "un Prestamista Despiadado"
SuitRobberBaronS = "un Barón Ladrón"
SuitBottomFeederS = "un Morrudo"
SuitBloodsuckerS = "un Chupa\3sangres"
SuitDoubleTalkerS = "un Embaucador"
SuitAmbulanceChaserS = "un Persigue Ambulancias"
SuitBackStabberS = "un Apuña la Espaldas"
SuitSpinDoctorS = "un Portavoz"
SuitLegalEagleS = "un Picapleitos"
SuitBigWigS = "un Pelucón"

# Plural versions
SuitFlunkyP = "Secuaces"
SuitPencilPusherP = "Chupatintas"
SuitYesmanP = "Sonrientes"
SuitMicromanagerP = "Micro\3gerentes"
SuitDownsizerP = "Reguladores de Empleo"
SuitHeadHunterP = "Cazacabezas"
SuitCorporateRaiderP = "Corporati\3vistas"
SuitTheBigCheeseP = "Peces Gordos"
SuitColdCallerP = "Gorrones"
SuitTelemarketerP = "Tele\3vendedores"
SuitNameDropperP = "Fardoncetes"
SuitGladHanderP = "Efusivos"
SuitMoverShakerP = "Mandamases"
SuitTwoFaceP = "Doscaras"
SuitTheMinglerP = "Confrater\3nizadoras"
SuitMrHollywoodP = "Sres. Hollywood"
SuitShortChangeP = "Calderillas"
SuitPennyPincherP = "Cacomatracos"
SuitTightwadP = "Roñosos"
SuitBeanCounterP = "Cuenta Cuentos"
SuitNumberCruncherP = "Contables"
SuitMoneyBagsP = "Monederos"
SuitLoanSharkP = "Prestamistas Despiadados"
SuitRobberBaronP = "Barones Ladrones"
SuitBottomFeederP = "Morrudos"
SuitBloodsuckerP = "Chupa\3sangres"
SuitDoubleTalkerP = "Embaucadores"
SuitAmbulanceChaserP = "Persigue Ambulancias"
SuitBackStabberP = "Apuña la Espaldas"
SuitSpinDoctorP = "Portavoces"
SuitLegalEagleP = "Picapleitos"
SuitBigWigP = "Pelucones"

SuitFaceOffDefaultTaunts = ['¡Buuu!']

SuitFaceoffTaunts = {
    'b':  ["¿Me haces una donación?",
           "Te voy a dejar hecho unos zorros.",
           "Te voy a dejar más seco que la mojama.",
           "Hay que ser \"RH positivo\" ante la vida.",
           "Oh, no seas tan \"RH negativo\".",
           "Me sorprende que me hayas encontrado, soy muy escurridizo.",
           "Voy a tener que hacerte una transfusión rápida.",
           "Pronto vas a tener que tomarte un bocadillo y un zumito.",
           "Cuando acabe contigo no vas a poder ni levantarte.",
           "No mires, sólo te pinchará un poquito.",
           "Vas a marearte un poquito.",
           "Justo a tiempo, estaba un poco sediento.",
           ],
    'm':  ["No sabes con quién estás confraternizando.",
           "¿Has confraternizado alguna vez con gente como yo?",
           "Estupendo, confraternicemos pues.",
           "¡Me encanta confraternizar!",
           "Parece un buen sitio para confraternizar.",
           "Qué situación más tierna, ¿no?",
           "Vas a confraternizar con la derrota.",
           "Voy a hacer que confraternices con el suelo.",
           "¿Seguro que quieres confraternizar conmigo?",
           ],
    'ms': ["Prepárate; soy muy mandón.",
           "Más te valdría quitarte de en medio.",
           "Te mando que te largues.",
           "Creo que me toca mandar.",
           "Vas a ver adónde te mando.",
           "Cuando mando, los demás tiemblan.",
           "Hoy me he levantado de lo más mandón.",
           "Cuidado, dibu, te va a caer encima un mandoble.",
           "Te voy a mandar bien lejos.",
           "El corazón me manda que te zurre.",
           "¿Necesitas que te manden un poco?",
           ],
    'hh': ["Te saco una cabeza.",
           "Vas de cráneo, me parece.",
           "Creo que has perdido la cabeza.",
           "Estupendo. Tenía ganas de coleccionar tu cocorota.",
           "Te vas a quedar sin cabeza por esto.",
           "¡Cabeza al frente!",
           "Me parece que la cabeza te ha jugado una mala pasada.",
           "Qué poca cabeza estás teniendo.",
           "Un trofeo perfecto para mi colección.",
           "Vas a tener un buen dolor de cabeza.",
           "¡Cuidado, no pierdas la cabeza!",
           ],
    'tbc': ["Te voy a pescar con las manos.",
            "Puedes llamarme Cachalote.",
            "Ten cuidado.  A veces soy como un tiburón blanco.",
            "Por fin, ya pensaba que me estabas dando sedal.",
            "Voy a cocinarte a la sal.",
            "¿Qué tal me sienta el escabeche?",
            "Ven aquí, voy a quitarte las escamas.",
            "Te va a pasar igual que a Jonás.",
            "Cuidadito, te he preparado un buen cebo.",
            "¿Te gusta que te preparen al pil-pil?",
            "¡Te voy a dar un buen pez-cozón!",
            ],
    'cr': ["¡DESPEDIDO!",
           "No encajas en mi colectivo.",
           "Vas a ser expulsado de la hermandad.",
           "No pareces defender los intereses comunes.",
           "Ese atuendo no es propio de tu colectivo.",
           "Te gusta sacar los pies del tiesto, ¿eh?",
           "Te voy a expulsar del colegio profesional.",
           "Un esquirol, ¿eh? ¡Vas a ver!",
           "No defiendes bien las ideas del colectivo.",
           "Relájate; esto es por el bien del colectivo.",
           ],
    'mh': ["¿Estás listo para mi escena?",
           "¡Luces, cámaras, acción!",
           "¡Estamos rodando!",
           "¡Hoy te toca desempeñar el papel del dibu derrotado!",
           "Por esta escena me van a dar el Oscar.",
           "Acabo de encontrar la inspiración para esta escena.",
           "¿Estás listo para tu escena final?",
           "No vas a aparecer ni en los créditos finales.",
           "No pienso firmarte ni un autógrafo.",
           "Voy a rodar contigo una escena de terror.",
           "¡Me encanta zurrar a los extras como tú!",
           "Espero que no olvides tu parte del guión.",
           ],
    'nc': ["Parece que tu balance no cuadra.",
           "Creo que tienes un déficit enorme.",
           "Déjame que equilibre tus cuentas.",
           "¡Estás en números rojos!",
           "¡Vas a tener que contabilizar tu factura del hospital!",
           "¿En qué columna te pongo? ¿Debe o haber?",
           "Eres un cero a la izquierda.",
           "Tu presupuesto está muy desequilibrado.",
           "Cuando acabe contigo no vas a saber ni contar.",
           "Voy a contar las veces que te machaco.",
           ],
    'ls': ["Es la hora de que pagues tu préstamo.",
           "Te he prestado demasiado tiempo.",
           "Es el momento del vencimiento.",
           "Venga, vamos a saldar cuentas.",
           "Pediste un anticipo y te lo voy a dar.",
           "Vas a pagar por esto.",
           "Llegó el día del ajuste de cuentas.",
           "¿Me prestas una oreja?",
           "Me alegro de que estés aquí; quiero lo que es mío.",
           "Voy a prestarte una paliza.",
           "Te voy a ofrecer un interés especial.",
           ],
    'mb': ["Es la hora de recoger la calderilla.",
           "Eres dinero suelto para mí.",
           "¿En efectivo o con tarjeta?",
           "¿Tienes el recibo?",
           "Recuerda que el dinero no da la felicidad.",
           "Me parece que andas escaso de fondos.",
           "Vas a tener un pequeño problema de efectivo.",
           "Después de esto, te veo pidiendo calderilla.",
           "Soy demasiado rico para mancharme las manos contigo.",
           "¡No hay dinero suficiente para satisfacerme!",
           ],
    'rb': ["Te han robado.",
           "Te voy a robar la victoria.",
           "¡Soy un barón del incordio!",
           "Soy la nobleza avasalladora.",
           "Vas a tener que denunciar este robo.",
           "Tengo la sangre azul... Veamos la tuya.",
           "Soy un rival noble.",
           "Te voy a dejar pelado.",
           "Supongo que esto es un robo a mano desarmada.",
           "¿No sabías que no se debe hablar con desconocidos?",
           ],
    'bs': ["Nunca me des la espalda.",
           "Te voy a dar un buen espaldarazo.",
           "Vas de espaldas por la vida.",
           "Se me da bien cortar el lomo.",
           "¿Te hago la acupuntura en la espalda?",
           "¡De espaldas contra la pared!",
           "¿Quieres que te haga cosquillas en la espalda?",
           "Me encanta jugar con las espalderas.",
           "Deja que te rasque la espalda.",
           "¡Date la vuelta, alguien viene!",
           "¡Mira, a tu espalda!",
           ],
    'bw': ["¿Quieres que te pase el cepillo?",
           "Sólo de verte se me riza el pelo.",
           "Si quieres hacemos esto permanente.",
           "Creo que vas a tener las puntas un poco abiertas.",
           "Creo que estás un poco bisoño.",
           "Te voy a teñir todo el cuerpo de morado.",
           "Has venido justo a tiempo para que te dé un buen repaso.",
           "Se te va a caer el pelo.",
           "Sólo de verte me salen entradas.",
           "Se te va a poner el pelo blanco.",
           ],
    'le': ["Creo que no tienes defensa posible. ",
           "Estoy picado contigo.",
           "Va a caer todo el peso de la ley encima de ti.",
           "Deberías saber que, cuando llevo la toga, soy implacable.",
           "Lo tuyo es un caso perdido de antemano.",
           "Creo que te va a caer cadena perpetua.",
           "Esto es tan divertido que debería ser ilegal.",
           "Lo siento; te tendrás que defender a ti mismo.",
           "Mis honorarios son bastante altos. ¿Podrás permitírtelos?",
           "Te voy a hacer trizas en el estrado.",
           ],
    'sd': ["Voy a anunciar tu fin.",
           "Deja que proclame tu derrota.",
           "El portavoz va anunciar tu desaparición.",
           "El mundo entero va a saber lo acabado que estás.",
           "Te vendría bien alguien que hablase por ti.",
           "¡Uy! ¡Al verte se me corta la voz!",
           "Deja que me aclare la voz un momento.",
           "Cuando acabe contigo no vas a tener voz ni voto.",
           "Podría anunciar mi victoria antes de tiempo.",
           "Damas y caballeros, este dibu es penoso.",
           ],
    'f': ["¡Me voy a chivar al jefe de ti!",
          "¡Soy un secuaz, pero soy muy pertinaz!",
          "Gracias a ti voy a conseguir un ascenso.",
          "No creo que te guste mi forma de trabajar.",
          "El jefe cuenta conmigo para ponerte fin.",
          "Vas a hacer que gane puntos ante el jefe.",
          "Primero tendrás que vértelas conmigo.",
          "Veamos qué te parece mi trabajo.",
          "Se me da de miedo deshacerme de los dibus.",
          "Nunca llegarás a ver a mi jefe.",
          "Te voy a enviar de vuelta al dibuparque.",
          ],
    'p':  ["¡Voy a borrarte de un plumazo!",
           "¡Chúpate ésta, pelele!",
           "¡Voy a cargar las tintas!",
           "Esto está adquiriendo tintes dramáticos...",
           "Deja que te aplique un poco de secante.",
           "Te voy a archivar para siempre.",
           "Deprisa, tengo que fichar pronto.",
           "Habré acabado contigo antes de que la tinta se seque.",
           "¡Nuestro encuentro hará correr ríos de tinta!",
           "Creo que tienes la tinta un poco seca, déjame que te vea.",
           "¡Cuidado, que mancho!",
           ],
    'ym': ["Lástima que esto no te vaya a gustar.",
           "Odio que la gente esté seria.",
           "Sonríe, la vida es bella... Aunque no para ti.  Una sonrisa vale por cien dibus.",
           "Necesitas algo de alegría en tu vida.",
           "Después de esto se te va a quedar sonrisa de tonto.",
           "Mi sonrisa desarma a cualquiera.",
           "Al verte, he sonreído más todavía.",
           "¿Te gusta mi sonrisa? ¡Vas a recordarla mucho tiempo!",
           "Te veo y sonrío para mis adentros.",
           "¿Una sonrisita antes de que acabe contigo?",
           "No sonríes nada... No me extraña.",
           ],
    'mm': ["¡Voy tomar el control de tus negocios!",
           "Las grandes palizas vienen a veces en frasco pequeño.",
           "Ningún reto que queda grande.",
           "Cuando quiero que algo salga bien, lo hago yo mismo.",
           "Necesitas a alguien que te gestione bien.",
           "¡Qué bien, un proyecto!",
           "Te voy a gestionar una buena lección.",
           "Hay que reorganizarte la agenda del día.",
           "Voy a gestionar tu presencia aquí.",
           "Estoy vigilando todos tus movimientos.",
           "¿Seguro que te atreves?",
           "Haremos esto a mi manera.",
           "No te pienso quitar el ojo de encima.",
           "Vas a ver lo que es acoso laboral.",
           ],
    'ds': ["¡Vas a irte a la calle!",
           "Tu puesto de trabajo peligra.",
           "Creo que tu perfil no se ajusta a mis necesidades.",
           "Ya no nos eres de utilidad.",
           "Yo que tú empezaba a pedir entrevistas.",
           "Tendré que hacer algunos ajustes de plantilla.",
           "Tienes poco futuro en mi empresa.",
           "Voy a tener que hacer algunos recortes.",
           ],
    'cc': ["Hola, ¿llevas algo suelto?",
           "Te devolveré lo que te debo mañana sin falta.",
           "¿Me dejas que llame desde tu móvil?",
           "¿Me invitas a comer? Me dejado la cartera en casa.",
           "¿Qué tienes hoy de comida?",
           "Me gusta tu ropa; creo que me la voy a quedar.",
           "Hoy vas a prestarme dinerito, ¿verdad?",
           "No te preocupes; siempre lo devuelvo todo.",
           "Creo que me voy a quedar una semanita en tu casa.",
           "Creo que voy a hacer unos recados en tu coche.",
           "Seguro que tus zapatos me quedan bien.",
           "Me encanta como cocinas; ¡voy a aficionarme a tu casa!",
           "He puesto mi línea telefónica a tu nombre.",
           ],
    'tm': ["Nunca he visto un producto peor que tú.",
           "Con mi superquitamanchas salen borrones como tú.",
           "Te voy a aplastar con mi megabdominator.",
           "Si acabo contigo, me regalo un cuchillo de cocina.",
           "Tu final está disponible con una llamada.  ¡Date prisa! ¡Tu fin está al caer!",
           "Acabe con los dibus molestos con \"zurradibu\".",
           "¡Te voy a poner los superéxitos de los bots!",
           "¿Cansado de tu figura? ¡Yo tengo la solución!",
           "¿No sabes qué hacer con tu pelo? ¡Llámame!",
           "Acepto tarjetas de crédito.",
           "Cuando acabe contigo, no habrás probado nada igual.",
           ],
    'nd': ["Seguro que mi coche corre más que el tuyo. ",
           "Supongo que sabrás que tengo mucho más dinero que tú.",
           "Contigo no tengo ni para empezar.",
           "Venga, deprisa, que tengo que comer con el Sr. Hollywood.",
           "¿Te había dicho que conozco al pez gordo?",
           "Soy íntimo amigo del mandamás.",
           "Conozco a gente que sabría encargarse de ti.",
           "¿Sabes con quién estás hablando?",
           "Acabaré rápidamente contigo; he quedado con gente importante.",
           "Lo siento; no me suelo codear con dibus como tú.",
           ],
    'gh': ["¡Hombre, un dibu! ¡Qué alegría machacarte!",
           "¡Qué bien! ¡Un dibu al que zurrar!",
           "¡Me lo voy a pasar de lo lindo contigo!",
           "¡Yupiii! ¡Tenía ganas de vérmelas con un dibu!",
           "¡Vas a ver lo que es bueno!",
           "¡Cómo me alegro de no volver a verte!",
           "Encantado de conocer... ¡tu fin!",
           "¡Cuánto tiempo sin verte! ¡Y cuánto más va a pasar!",
           "¡He estado años esperando este momento!",
           "¡Me siento feliz de poder zurrarte!",
           "¡Hurra! ¡Un dibu tiernecito!",
           "¡Hoooola! ¿Cómo quieres que acabe contigo?",
           "¡Un dibu! ¡Déjame que te estreche bien la mano!",
           ],
    'sc': ["¡Voy a hacerte calderilla!",
           "Vas a tener un pequeño problema de efectivo.",
           "No acepto tus divisas.",
           "No tengo cambio para ti.",
           "Cuando acabe contigo, no vas a valer ni un céntimo.",
           "Creo que la inflación te va a venir muy mal.",
           "Te voy a depreciar en breve.",
           "Mmm, creo que no llevo dibus sueltos.",
           "Cuando acabe contigo no te va a quedar ni un céntimo.",
           "¿Llevas calderilla para tu vuelta al dibuparque?",
           "No acepto propinas de un dibu.",
           ],
    'pp': ["Espera, te voy a aligerar de peso. ",
           "¿No notas que te falta algo?",
           "Yo que tú guardaría bien la cartera.",
           "¿Te has acordado de cerrar con llave tu casa?",
           "Me encanta tu reloj; creo que me lo voy a quedar.",
           "Vas a volver al dibuparque pelado de gominolas.",
           "Lo siento; tengo que requisarte unas cosillas.",
           "¿Me dejas ver qué llevas en los bolsillos?",
           "¿Algo que declarar?",
           "¡Otro dibu al que desplumar!",
           ],
    'tw': ["No esperes que dé ni los buenos días.",
           "Para ti soy el Sr. Roñoso.",
           "Voy a cortarte los fondos.",
           "¿Es ésa la mejor oferta que tienes?",
           "Venga, deprisa. El tiempo es oro.",
           "¡Soy de la hermandad del puño cerrado!",
           "Creo que tu oferta no me convence.",
           "Vas a tener que ofrecer mucho más, me temo.",
           "A ver si puedes permitirte esto.",
           "No te pienso dar ni una oportunidad.",
           "Voy a pegarles un buen bocado a tus fondos.",
           ],
    'bc': ["Me encanta contar cuentos a los dibus.",
           "Cuenta conmigo para pasarlo mal.",
           "Cuenta con que te voy a zurrar bien.",
           "¿Te cuento un cuento de miedo?",
           "Aquí el que cuenta soy yo.",
           "Cuenta con volver al dibuparque.",
           "Después de esto, no lo vas a contar.",
           "Este cuento va a acabar mal para ti.",
           "No tengas cuento...",
           "Cuando acabe contigo, no te van a salir las cuentas.",
           "Tenía unas cuantas cuentas pendientes contigo...",
           ],
    'bf': ["Todos me dicen que tengo mucho morro.",
           "Siempre le hecho morro a la vida.",
           "Hay que tener morro para venir aquí.",
           "Tienes bastante morro, ¿no crees?",
           "Justo a tiempo, te voy a hinchar los morros.",
           "Tengo un morro que me lo piso.",
           "Para ganarme le vas a tener que echar mucho morro.",
           "Tu morro no está a la altura de las circunstancias.",
           "Te voy a mandar al dibuparque de un morrazo.",
           "Vas a ver mis morros por última vez.",
           ],
    'tf': ["¡Por fin nos vemos las caras!",
           "¡Vas a tener que encarar la derrota!",
           "¿A que no sabes hacia dónde estoy mirando?",
           "Como tengo dos caras, es difícil que me las rompan.",
           "Dos caras son mejor que una.",
           "¿Cuál de mis dos caras te gusta más?",
           "Creo que te llaman en el dibuparque.",
           "¿Qué cara quieres que se encargue de ti?",
           "Tengo bastante más cara que tú.",
           "No sabes la cara que tengo...",
           "Lo mire por donde lo mire, siempre te veo...",
           ],
    'dt': ["Ha llegado el momento de embaucar a alguien.",
           "Oye, hay un elefante detrás de ti.",
           "¿Quieres que le eche un poco de cara al asunto?",
           "¿Cuál de mis dos caras dice la verdad?",
           "Yo que tú encaraba la salida.",
           "No te va a gustar mi doble juego.",
           "Yo que tú me lo pensaba dos veces.",
           "Prepárate para una ración DOBLE.",
           "Vas a ver mis caras en sueños.",
           "Para vencerme hacen falta dos como tú.",
           ],
    'ac': ["¡Te voy a perseguir hasta el dibuparque!",
           "¿No oyes una sirena?",
           "Ja, ja, cómo voy a disfrutar.",
           "Me encanta la emoción de la persecución.",
           "¡Corre, corre, que te pillo!",
           "¿Te has hecho un seguro?",
           "Espero que te hayas traído una camilla.",
           "Dudo que aguantes mi ritmo.",
           "A partir de aquí se te va a hacer todo cuesta arriba.",
           "Pronto vas a necesitar atención médica urgente.",
           "Esto no es para reírse.",
           "Espero que te gusten los hospitales.",
           ]
    }

SuitAttackDefaultTaunts = ['¡Toma ya!!', '¡Fíjate bien en esto!']

SuitAttackNames = {
  'Audit' : '¡Auditoría!',
  'Bite' : '¡Mordisco!',
  'BounceCheck' : 'Cheque sin fondos!',
  'BrainStorm' : '¡Aguacero!',
  'BuzzWord' : '¡Charlatán!',
  'Calculate' : '¡Calculadora!',
  'Canned' : '¡Enlatado!',
  'Chomp' : '¡Zampón!',
  'CigarSmoke' : '¡Humo de Cigarro!',
  'ClipOnTie' : '¡Corbatón!',
  'Crunch' : '¡Crujido!',
  'Demotion' : '¡Degradación!',
  'Downsize' : '¡Recorte de plantilla!',
  'DoubleTalk' : '¡Embaucar!',
  'EvictionNotice' : '¡Deshaucio!',
  'EvilEye' : '¡Mal de ojo!',
  'Filibuster' : '¡Discurso plasta!',
  'FillWithLead' : '¡Lleno de Plomo!',
  'FiveOClockShadow' : "¡Barbudo!",
  'FingerWag' : '¡Regañado!',
  'Fired' : '¡Despedido!',
  'FloodTheMarket' : '¡Saturar el Mercado!',
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
  'PickPocket' : '¡Caco!',
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
  'Sacked' : '¡Al saco!',
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
  'Watercooler' : '¡Nevera!',
  'Withdrawal' : '¡Retidada de fondos!',
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
              "He encontrado un error en tu libro de contabilidad.",
              ],
    'Bite': ["¿Te apetece un mordisquito?",
             "¡Prueba un poco de esto!",
             "Perro ladrador, poco mordedor.",
             "¡Hoy estoy que muerdo!",
             "¡Vas a morder el polvo!",
             "Cuidado, que muerdo.",
             "Muerdo siempre que puedo.",
             "Voy a morderte un poquito.",
             "No me pienso morder la lengua contigo.",
             "Sólo un mordisquito...  ¿Es pedir demasiado?",
             ],
    'BounceCheck': ["Qué lástima, eres un rollo.",
                    "Tienes pendiente un pago.",
                    "Creo que este cheque es tuyo.",
                    "Me debes este cheque.",
                    "Estoy cobrando deudas atrasadas.",
                    "Este cheque está al rojo vivo.",
                    "Te voy a pasar un buen recargo.",
                    "Echa un vistazo a esto.",
                    "Esto te va a costar una buena pasta.",
                    "Me gustaría cobrar esto.",
                    "Voy a devolverte este regalito.",
                    "Éste será tu talón de Aquiles.",
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
                "¿Te has enterado de lo último?",
                "A ver si pillas esto.",
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
                  "¿Has sumado todos tus gastos?",
                  "Según mis cálculos, no estarás aquí mucho tiempo.",
                  "Aquí tienes el total.",
                  "Vaya; tu factura no para de aumentar.",
                  "¡Ponte a sumar esto!",
                  "Bots: 1; Dibus: 0",
                  ],
    'Canned': ["¿Te gustan las conservas?",
               "\"Conserva\" esto como recuerdo.",
               "¡Esto está recién salido de la lata!",
               "¿Te han dado el latazo alguna vez?",
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
                  TheCogs+" elegantes siempre se ponen una de éstas...",
                  "Pruébate ésta, a ver qué tal te queda.",
                  "La imagen es fundamental para tener éxito en la vida.",
                  "Aquí no se admite a nadie sin corbata.",
                  "¿Quieres que te ayude a ponerte esto?",
                  "Una buena corbata dice mucho de ti.",
                  "Veamos qué tal te sienta esto.",
                  "Esto a lo mejor te aprieta un poco.",
                  "Es mejor que te arregles antes de MARCHARTE.",
                  "Toma, con esto serás el dibu más guapo del dibuparque.",
                  ],
    'Crunch': ["Parece que estás un poco crujido.",
               "¡Es hora de crujirse un poco!",
               "Con esto te van a crujir las articulaciones.",
               "¡Mira qué crujido más delicioso!",
               "¿No oyes un crujido?",
               "¿Qué prefieres, blandito o crujiente?",
               "Esto está crujiente y apetitoso.",
               "¡Prepárate para que te crujan los huesos!",
               "¡Me encantan los postres crujientes!"
               ],
    'Demotion': ["Vas a bajar puestos en la empresa. ",
                 "Vas a volver a trabajar de botones.",
                 "Me parece que te has quedado sin despacho.",
                 "¡Majo, vas para abajo!",
                 "Creo que tu puesto peligra.",
                 "Tienes poco futuro en esta empresa.",
                 "Laboralmente, estás en un callejón sin salida.",
                 "Tu puesto en la empresa se está tambaleando.",
                 "Te veo preparando café bien pronto.",
                 "Esto va a ir directo a tu expediente.",
                 ],
    'Downsize': ["¿Qué tal unos cuantos recortes?",
                 "A veces hay que aplicar la tijera.",
                 "Yo que tú iría pidiendo entrevistas de trabajo.",
                 "¿Has guardado el suplemento de empleo de tu periódico?",
                 "¿Nunca te han dicho que eres prescindible?",
                 "Tu perfil no se ajusta a nuestras necesidades actuales.",
                 "¿Has oído hablar de las reestructuraciones?",
                 "Me temo que ya no nos eres útil.",
                 "¿Por qué no te buscas un trabajo en otro sitio?",
                 "Este año no te comes el turrón en esta empresa.",
                 "Me temo que los cambios en la empresa te van a afectar.",
                 "Me temo que nos sobra algo de personal.",
                 ],
    'EvictionNotice': ["¡Ha llegado la hora de la mudanza!",
                       "Haz las maletas, dibu.",
                       "Creo que vas a tener que cambiar de residencia.",
                       "Creo que debajo del puente se está muy bien.",
                       "Me temo que no has pagado el alquiler.",
                       "¿Habías pensado en redecorar tu vivienda?",
                       "A partir de ahora vas a disfrutar del aire libre.",
                       "¿No decías que te gustaban los espacios abiertos?",
                       "¡Estás fuera de lugar!",
                       "Prepárate para ser reubicado.",
                       "Tranquilo; ahora vas a conocer a más gente.",
                       "You're in a hostel position.",
                       ],
    'EvilEye': ["Te voy a echar el mal de ojo.",
                "¿Puedes echarle un ojo a esto?",
                "Espera.  Se me ha metido algo en el ojo.",
                "¡Te he puesto el ojo encima!",
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
    'FingerWag': ["Te lo he dicho un millón de veces.",
                  "Dibu, te estoy hablando a ti.",
                  "No me hagas reír.",
                  "No me hagas ir hasta ahí.",
                  "Estoy harto de repetírtelo.",
                  "Creo que ya te había dicho esto.",
                  "No nos guardas ningún respeto a los bots.",
                  "Es hora de que empieces a prestar atención.",
                  "Bla, bla, bla, bla, bla.",
                  "Voy a tener que aplicarte un correctivo.",
                  "¿Cuántas veces te lo tengo que decir?",
                  "No es la primera vez que pasa esto.",
                  ],
    'Fired': ["Espero que te hayas traído algo para la barbacoa.",
              "Esto va a ponerse calentito.",
              "Seguro que con esto entres en calor.",
              "Espero que seas un animal de sangre fría.",
              "¡Caliente, caliente!",
              "Creo que te va a hacer falta un extintor.",
              "¡Vas a quedarte chamuscado!",
              "¡Vas a quedar muy doradito!",
              "Esto le da otro significado a la expresión \"bien hecho\".",
              "Espero que te hayas puesto protección solar.",
              "Avísame cuando estés crujiente.",
              "La cosa está que arde.",
              "Vas a arder en deseos de volver al dibuparque.",
              "Creo que tienes un temperamento ardiente.",
              "A ver, déjame que te ponga el termómetro...",
              "¡Tienes mucha chispa!",
              "El que juega con fuego...",
              "¿Nunca te han dicho que te sale humo de las orejas?",
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
                    "Me han dicho que tengo una mirada penetrante.",
                    "Mírame fijamente a los ojos...",
                    "¿Te gusta mi caída de ojos?",
                    "Tengo una mirada arrebatadora.",
                    "¿No te parecen unos ojos muy expresivos?",
                    "Siempre me han dicho que tengo unos ojos preciosos.",
                    "El secreto está en la mirada.",
                    "¡Veo, veo! ¡Veo un dibu en apuros!",
                    "Deja que te mire bien...",
                    "¿Echamos una mirada a tu futuro?",
                    ],
    'GuiltTrip': ["¡Vas a cargar con toda la culpa!",
                  "¿Te sientes culpable?",
                  "¡Todo es culpa tuya!",
                  "¡Te pienso culpar por todo!",
                  "¡Has sido declarado culpable!",
                  "¡No pienso volver a hablarte!",
                  "¡Más te valdría pedir perdón!",
                  "¡No te pienso perdonar en la vida!",
                  "¿No crees que te has portado mal?",
                  "¡No intentes echarme la culpa!",
                  "¡Eres un culpable con causa!",
                  ],
    'HalfWindsor': ["¡Ésta es la corbata más bonita que has visto en tu vida!",
                    "Intenta no hacerte un nudo.",
                    "Se te va a poner un nudo en el estómago.",
                    "Tienes suerte de que sea un nudo fácil.",
                    "¿No se te hace un nudo en la garganta?",
                    "¡Seguro que no sabes ni hacerte el nudo!",
                    "¡Después de esto te voy a anudar la lengua!",
                    "No debería malgastar esta corbata contigo.",
                    "¡No te mereces esta corbata tan bonita!",
                  ],
    'HangUp': ["Se ha cortado tu llamada.",
               "¡Adiós!",
               "Es el momento de terminar la conexión.",
               "... ¡Y no vuelvas a llamarme!",
               "¡Clic!",
               "Se acabó la conversación.",
               "Voy a cortar la línea.",
               "Creo que tienes la línea en mal estado.",
               "Me parece que no tienes línea.",
               "Ha finalizado tu llamada.",
               "Espero que me escuches alto y claro.",
               "Te has equivocado de número.",
               ],
    'HeadShrink': ["¿Has estado últimamente en el Amazonas?",
                   "Cariño, he encogido a un dibu.",
                   "Espero que tu orgullo no se quede encogido.",
                   "¿Has encogido en la lavadora?",
                   "Te he dicho que no te laves con agua caliente.",
                   "No pierdas la cabeza por esto.",
                   "¿Es que has perdido la cabeza?",
                   "¡Pero qué poca cabeza tienes!",
                   "¡Eres un cabeza de chorlito!",
                   "No sabía que habías pasado una temporada con los jíbaros.",
                   ],
    'HotAir':["El ambiente se está acalorando.",
              "Vas a sufrir una ola de calor.",
              "He llegado al punto de ebullición.",
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
              "He de pontificar sobre este asunto.",
              "¿Ves? Las palabras pueden hacer daño.",
              "¿Has pillado lo que quiero decir?",
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
    'MarketCrash':["Me parece que tus acciones han caído.",
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
                  "Vaya; se me llena la boca.",
                  "Odio alargarme en mis peroratas.",
                  "Permíteme unas palabrillas.",
                  "Tengo preparado un discursito para ti.",
                  ],
    'ParadigmShift':["¡Cuidado! Hoy estoy de lo más cambiante.",
                     "¡Prepárate para un buen golpe de timón!",
                     "Creo que hay que enderezar tu rumbo.",
                     "Vas a tener un ligero cambio de perspectiva.",
                     "Supongo que no vas a tener cambio para esto.",
                     "¡Has perdido el norte!",
                     "Seguro que nunca has cambiado tanto de orientación.",
                     "¡Creo que no te va a gustar este cambio!",
                     "¡No me hagas cambiar de parecer!",
                     ],
    'PeckingOrder':["Sí; soy todo un pájaro.",
                    "Más vale pájaro en mano...",
                    "Me ha dicho un pajarito que vas a volver de golpe al dibuparque.",
                    "¡No huyas como un gallina!",
                    "Creo que tienes la cabeza llena de pájaros.",
                    "¡Cría cuervos y tendrás muchos!",
                    "¡Ya has volado bastante, pajarito!",
                    "Me encanta salir de picoteo.",
                    "Voy a hacer un buen caldo de gallina contigo.",
                    ],
    'PickPocket': ["Deja que me haga cargo de tus objetos personales.",
                   "¿A ver qué llevas ahí?",
                   "Esto es como quitarle un caramelo a un niño.",
                   "Menudo robo...",
                   "Espera, yo te sujeto eso.",
                   "No pierdas de vista mis manos.",
                   "La mano es más rápida que el ojo...",
                   "Nada por aquí...",
                   "La dirección no se hace responsable de los objetos perdidos.",
                   "Santa Rita, Rita...",
                   "No te vas a dar ni cuenta.",
                   "Te voy a dejar desplumado.",
                   "¿Te importa si me quedo con esto?",
                   "Te voy a aligerar de peso.",
                   ],
    'PinkSlip': ["Tengo algo de correspondencia para ti.",
                 "¿Estás asustado? ¡Te has puesto pálido!",
                 "Esta carta te va a hacer mucha ilusión.",
                 "Vaya; creo que alguien va a tener que hacer las maletas.",
                 "¡Eh, no te vayas sin despedirte!",
                 "¿Te has despedido ya de todo el mundo?",
                 "¡Mira, una carta de amor!",
                 "Creo que este papel es para ti...",
                 "La verdad es que éste color no te favorece.",
                 "¡Aquí tienes tu carta de despido. Largo de aquí!",
                 ],
    'PlayHardball': ["¿Así que quieres jugar al béisbol?",
                     "No te recomiendo que juegues conmigo.",
                     "¡Batea de una vez!",
                     "¡Venga, batea esto!",
                     "¡Y aquí viene el lanzamiento...!",
                     "Vas a tener que mandarla lejos.",
                     "Te voy a sacar del estadio de un batazo.",
                     "Te voy a mandar al dibuparque de un batazo.",
                     "¡Ésta es tu carrera final!",
                     "¡No vas a poder jugar conmigo!",
                     "¡Te voy a poner en órbita!",
                     "¡Vas a ver qué bola te lanzo!",
                    ],
    'PoundKey': ["Es hora de devolver algunas llamadas.",
                 "¿Qué tal una llamada a cobro revertido?",
                 "¡Ring, ring! ¡Es para ti!",
                 "Toma, para que me llames cuando quieras.",
                 "Me sobra una almohadilla...",
                 "Espero que tu teléfono sea de tonos.",
                 "Déjame que marque este número.",
                 "Voy a hacer una llamada por sorpresa.",
                 "Espera, te voy a dar un toque.",
                 "Dibu, vas a poder hacer sólo una llamada.",
                 ],
    'PowerTie': ["Te veré más tarde; parece que se te ha hecho un nudo en la garganta.",
                 "Voy a atar unos cuantos cabos sueltos.",
                 "¡Con esto vas a ir muy elegante!",
                 "Para que vayas practicando los nudos...",
                 "Ya es hora de que empieces a vestir bien.",
                 "¡Ésta es la corbata más fea que has visto en tu vida!",
                 "¿No te sientes importante llevando esto?",
                 "¡Vas a ver cómo cambia tu aspecto!",
                 "¡Nada mejor que una corbata de regalo!",
                 "No sabía qué regalarte, así que ¡toma!",
                 ],
    'PowerTrip': ["Haz las maletas, que nos vamos de excursión.",
                  "¿Has tenido un buen viaje?",
                  "Bonito viaje; te veré el año que viene.",
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
              "Éste se va a salir de la escala Richter.",
              "¡Con esto se van a sacudir los cimientos!",
              "¡Vas a ver qué meneo!",
              "¿Has sufrido alguna vez un terremoto?",
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
                     "Siempre uso seda dental después de comer.",
                     "¡Di \"patata\"!",
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
    'ReOrg': ["¡No te va a gustar la forma en que he reorganizado todo!",
              "Creo que hace falta un poco de reorganización.",
              "No estás tan mal, sólo hay que reorganizarte.",
              "¿Te gusta mi capacidad de reorganización?",
              "He pensado que le iría bien una nueva imagen a todo.",
              "¡Hay que reorganizarte!",
              "Pareces un poco desorganizado.",
              "Espera; voy a reorganizar tus pensamientos.",
              "Voy a esperar a que te reorganices un poco.",
              "¿Te importa si organizo un poco todo esto?",
              ],
    'RestrainingOrder': ["Deberías alejarte un poco.",
                         "¡Me han encargado que te dé una orden de alejamiento!",
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
    'RubberStamp': ["Me gusta dejar siempre una buena impresión.",
                    "Es importante aplicar una presión firme.",
                    "Dejo siempre una buena huella.",
                    "Te voy a dejar más plano que un sello.",
                    "Hay que DEVOLVERTE AL REMITENTE.",
                    "Has sido CANCELADO.",
                    "Voy a mandarte al dibuparque con sello URGENTE.",
                    "Creo que te vas a sentir muy RECHAZADO.",
                    "Para mandarte al dibuparque no hará falta FRANQUEO.",
                    "Vas a ir al dibuparque POR AVIÓN.",
                    ],
    'RubOut': ["Y ahora, la desaparición final.",
               "Me parece que te he perdido.",
               "He decidido que te quedas fuera.",
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
                "¡Te lo has ganado!",
                "No quiero aburrirte con mi discurso.",
                "Adular a la gente me da buenos resultados.",
                "Voy a exagerar un poquito.",
                "Es hora de dorar la píldora un poco.",
                "Ahora hablemos un poco de ti.",
                "Te mereces una palmadita en la espalda.",
                "Ha llegado el momento de alabar tu trayectoria.",
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
    'Shred': ["Tengo que deshacerme de bastante morralla.",
              "Voy a reciclar un poco de papel.",
              "Creo que me voy a deshacer de ti ahora mismo.",
              "Con esto me desharé de las pruebas.",
              "Ya no hay manera de demostrar nada.",
              "A ver si consigues recomponer esto.",
              "Esto te va a hacer trizas.",
              "Voy a triturar esa idea.",
              "No quiero que esto caiga en malas manos.",
              "Adiós a las pruebas.",
              "Creo que ésta era tu última esperanza.",
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
                "Tu proyecto ha sido cancelado.",
                "Hemos cortado tus fondos.",
                "Estamos reestructurando tu división.",
                "Lo he sometido a votación y has perdido.",
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
                 "¿Estás listo para unas cifras de vértigo?",
                 "Es la hora de que pagues la dolorosa.",
                 "Hora de saldar cuentas...",
                 "Me encanta tener las cuentas claras.",
                 "Las cuentas claras y el chocolate oscuro.",
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
    'Tremor': ["¿Has notado eso?",
               "No te dan miedo los temblores, ¿verdad?",
               "Los temblores suelen ser el principio.",
               "Pareces tembloroso. ",
               "¡Voy a agitar un poco las cosas!",
               "¿Estás listo para bailar la rumba?",
               "¿Qué te pasa? Pareces agitado.",
               "¡Tiembla de miedo!",
               "¿Por qué tiemblas de miedo?",
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
    'Withdrawal': ["Creo que te has quedado sin fondos",
                   "Espero que tengas suficientes fondos en tu cuenta.",
                   "¡Toma ya, con intereses!",
                   "Te estás quedando sin liquidez.",
                   "Pronto vas a tener que hacer un ingreso.",
                   "Estás al borde del colapso económico.",
                   "Creo que estás en recesión.",
                   "Tus finanzas se van a ver afectadas.",
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

# DistributedBuilding.py
# DistributedElevatorExt.py
CogsIncExt = ", Inc."
CogsIncModifier = "%s" + CogsIncExt
CogsInc = string.upper(Cogs) + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "Toc, toc."
DoorWhosThere = "¿Quién es?"
DoorWhoAppendix = " qué?"
DoorNametag = "Door"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "¡Tù necesitas bromas! Anda a hablar con Tato Tutorial"
FADoorCodes_DEFEAT_FLUNKY_HQ = "¡Ven devuelta cuando hayas derrotado al Secuaz!"
FADoorCodes_TALK_TO_HQ = "¡Anda y obten tu recompense del funcionario Enrique!"
FADoorCodes_WRONG_DOOR_HQ = "¡Puerta incorrecta! ¡Sal por la otra puerta al Dibuparque!"
FADoorCodes_GO_TO_PLAYGROUND = "¡Salida equivocada! ¡Tù necesitas salir al Dibuparque!"
FADoorCodes_DEFEAT_FLUNKY_TOM = "¡Asércate al Secuaz para combatir con él!"
FADoorCodes_TALK_TO_HQ_TOM = "Ve y obtén tu recompense en el Cuartel General Dibu!"
FADoorCodes_SUIT_APPROACHING = None # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "¡Cuidado! ¡Adentro está un Bot!"
FADoorCodes_DISGUISE_INCOMPLETE = "Si vas de dibu te van a pillar. Reúne primero un disfraz de bot completo.\n\nHáztelo con piezas de la fábrica."

# KnockKnockJokes.py
KnockKnockJokes = [
    ["Aitor ",
    "¡Aitor Tilla de Patatas!"],

    ["Adela",
    "¡Carmelo Cotonenalmíbar!"],

    ["Abraham",
    "¡Abraham Lapuerta!"],

    ["Amira",
    "¡Amira Quienhavenido!"],

    ["Aquiles",
    "¡Aquiles Dejoporhoy!"],

    ["Archibaldo",
    "¡Archibaldo Enlascarpetas!"],

    ["Armando",
    "¡Armando Adistancia!"],

    ["Ariel",
    "¡Ariel Lavamasblanco!"],

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
    "¡Beltrán Chetes de Quesito!"],

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
    "¡Clemente Claraydespejada!"],

    ["Cleopatra",
    "¡Cleopatra Ficoenhorapunta!"],

    ["Clotilde",
    "¡Clotilde Alfinal!"],

    ["Consuelo",
    "¡Consuelo Recienfregado!"],

    ["Crisóstomo",
    "¡Crisóstomo Uncafeconleche!"],

    ["Demetrio",
    "¡Demetrio Doloquetenga!"],

    ["Bernabé",
    "¡Bernabé Averquienés!"],

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
    "¡Florinda Se y Bajelasmanos!"],

    ["Gaspar",
    "¡Gaspar Ecequevallover!"],

    ["Genoveva",
    "¡Genoveva Desabotella!"],

    ["Jairo",
    "¡Jairo Niasdelavida!"],

    ["Jazmín",
    "¡Jazmín Nero del Carbón!"],

    ["Jeremías",
    "¡Jeremías Sonpasiempre!"],

    ["Jessica",
    "¡Jessica Nálisis Gratuito!"],

    ["Jesús",
    "¡Jesús Piros de España!"],

    ["Joaquín",
    "¿Joaquín Havenidoestavez?"],

    ["Kevin",
    "¿Kevin Olesirvo?"],

    ["Leonor",
    "¡Leonor Abuena Porelpremio!"],

    ["Mabel",
    "¡Mabel Siabresdunavez!"],

    ["Macarena",
    "¡Macarena Blanca de la Playa!"],

    ["Magdalena",
    "¡Magdalena Ycafé Conleche!"],

    ["Maite",
    "¡Maite Digoquesoyyó!"],

    ["Marcos",
    "¡Marcos Sacos del Don!"],

    ["Armando",
    "¡Armando de la Tropa!"],

    ["Olimpia",
    "¡Olimpia Fijaydaesplendor!"],

    ["Olivia",
    "¡Olivia Ductoromano!"],

    ["Omar",
    "¡Omar Ejadilla del Cantábrico!"],

    ["Óscar",
    "¡Óscar Naval de Tenerife!"],

    ["Pánfilo",
    "¡Pánfilo de la Navaja!"],

    ["Pascual",
    "¿Pascual Esudireción?"],

    ["Pura",
    "¡Pura Suertehaberloencontrado!"],

    ["Ramiro",
    "¡Raimiro Ynoteveo!"],

    ["Ramona",
    "¡Ramona Vestida de Seda!"],

    ["Raúl",
    "¡Raúl Timo de la Fila!"],

    ["Renato",
    "¡Renato Sigadoportodos!"],

    ["Juan Ricardo",
    "¡Juan Ricardo Borriquero!"],

    ["Rubén",
    "¡Rubén Averloquemehecomprado!"],

    ["Sabina",
    "¡Sabina Questariasaquí!"],

    ["Samanta",
    "¡Samanta de Lanaquehacefrío!"],

    ["Sandra",
    "¡Sandra Josa!"],

    ["Serafín",
    "¡Serafín de la Historia!"],

    ["Serena",
    "¡Serena y Tranquila!"],

    ["Servando",
    "¡Servando Lero de Sierra Morena!"],

    ["Silvestre",
    "¡Silvestre Senunburro!"],

    ["Silvio",
    "¿Silvio Ustedamiperro?"],

    ["Sixta",
    "¡Sixta Vezquevengoaquí!"],

    ["Socorro",
    "¡Socorro Auxílio!"],

    ["Sol",
    "¡Sol Oquieropasar!"],

    ["Soledad",
    "¡Soledad de Tenertentusbrazos!"],

    ["Tadeo",
    "¡Tadeo Graciasadiós!"],

    ["Tamara",
    "¡Tamara Casdemachín!"],

    ["Teobaldo",
    "¡Teobaldo Sas de Cerámica!"],

    ["Ulrico",
    "¡Ulrico Helado, oiga!"],

    ["Virgilio",
    "¡Virgilío Mehasmetido!"],

    ["Vladimir",
    "¡Vladimir Aquienhavenido!"],

    ["Wenceslao",
    "¡Wenceslao de Vainilla!"],

    ["Wenceslao",
    "¡Wenceslao de Chocolate!"],

    ["Amira",
    "¡Amira Quiensoy!"],

    ["Saúl",
    "¡Saúl Timaoportunidadqueledoy!"],

    ["Noé",
    "¡Noé Nadieconocido!"],

    ["Noé",
    "¿Noé Verdadquemesperabas?"],

    ["Nadia",
    "¡Nadia Importante, la verdad!"],

    ["Otto",
    "¡Otto Quenomeconoce!"],

    ["Abel",
    "¡Abel Quienés!"],

    ["Alcira",
    "¡Alcira Esapuertaquehacefrío!"],

    ["Apolo",
    "¡Apolo de Naranja y Limón!"],

    ["Carmelo",
    "¿Carmelo Dicesomelocuentas?"],

    ["Padmé",
    "¿Padmé Dicequehoraes?"],

    ["Eleazar",
    "¡Eleazar Aleatóriez!"],

    ["Elijah",
    "¡Elijah Elquemasleguste!"],

    ["Elmer",
    "¡Elmer Cader de Venecia!"],

    ["Elpida",
    "¡Elpida Loqueleapetezca!"],

    ["Quique",
    "¡Quique Cosasdice, oiga!"],

    ["Euridice",
    "¡Euridice Quelellames!"],

    ["Calvino",
    "¡Calvino Tinto de Verano!"],

    ["Mercedes",
    "¡Mercedes Elpaso!"],

    ["Mercurio",
    "¡Mercurio Soquelopregunte!"],

    ["Merlin",
    "¡Merlin Dacasatieneusted!"],

    ["Minerva",
    "¡Minerva Minfada y Mixaspera!"],

    ["Miranda",
    "¡Miranda Yvetedeunavez!"],

    ["Morgana",
    "¡Morgana Tengodefastidiar!"],

    ["Morfeo",
    "¡Morfeo Quepegarleaunpadre!"],

    ["Pancho",
    "¡Pancho Colate Blanco!"],

    ["Parker",
    "¡Parker Levoyacontar!"],

    ["Pasha",
    "¿Pasha Contigotío?"],

    ["Patty",
    "Patty Todo Noquieronada."],

    ["Stan",
    "¡Stan Todosdetenidos!"],

    ["Pierre",
    "¡Pierre Queerre!"],

    ["Ida",
    "¡Ida Yvuelta!"],

    ["Savannah",
    "¡Savannah de Lino Blanco!"],

    ["Renata",
    "¡Renata Conchocolate!"],
]

# ChatInputNormal.py
ChatInputNormalSayIt = "Decírselo"
ChatInputNormalCancel = "Cancelar"
ChatInputNormalWhisper = "Susurrar"
ChatInputWhisperLabel = "A %s"

# ChatInputSpeedChat.py
SCEmoteNoAccessMsg = "Todavía no tienes acceso\n a este emoticono."
SCEmoteNoAccessOK = "Aceptar"

# ChatManager.py
ChatManagerChat = "Charla"
ChatManagerWhisperTo = "Susurrar a:"
ChatManagerWhisperToName = "Susurrar a:\n%s"
ChatManagerCancel = "Cancelar"
ChatManagerWhisperOffline = "%s está desconectado."
OpenChatWarning = '¡Todavía no tienes "amigos secretos"!  No puedes conversar con otros dibus a menos que sean tus amigos secretos.\n\nPara convertirte en amigo secreto de alguien, haz clic en él y selecciona "Secretos" en el panel de detalles.  No hace falta decir que siempre puedes hablar con quien quieras por medio de la Charla rápida.'
OpenChatWarningOK = "Aceptar"
UnpaidChatWarning = 'Cuando te hayas suscrito, podrás usar este botón para charlar con tus amigos mediante el teclado.  Hasta entonces, deberías usar la herramienta Charla rápida para conversar con los demás dibus.'
UnpaidChatWarningPay = "¡Suscríbete ya!"
UnpaidChatWarningContinue = "Continuar prueba gratuita"
#PaidNoParentPasswordWarning = 'Una vez creada la contraseña parental, podrás activar este botón para charlar con tus amigos mediante el teclado. Hasta entonces, puedes usar la herramienta Charla rápida para conversar con los demás dibus.
#PaidNoParentPasswordWarningSet = "Crear la contraseña parental ahora"
#PaidNoParentPasswordWarningContinue = "Seguir jugando"
NoSecretChatAtAllTitle = "Charla de Amigos secretos"
NoSecretChatAtAll = 'Para charlar con un amigo, la herramienta Amigos secretos debe estar activada.  La herramienta Amigos secretos permite a un miembro charlar con otro gracias al uso de un código secreto que se debe comunicar fuera del juego.\n\nPara activar esta herramienta sal de Toontown y actívala a través de Los Controles Parentales en Conecta Disney'
NoSecretChatAtAllOK = "Aceptar"
NoSecretChatWarningTitle = "Controles parentales"
NoSecretChatWarning = 'Para que sea posible charlar con un amigo, la herramienta Amigos secretos debe estar activada.  Para saber más cosas sobre la herramienta Amigos secretos y acceder a los controles parentales, diles a tus padres que abran la sesión con su contraseña parental.'
NoSecretChatWarningOK = "Aceptar"
NoSecretChatWarningCancel = "Cancelar"
NoSecretChatWarningWrongPassword = 'Esa contraseña no es correcta.  Introduce la contraseña parental que se creó al adquirir esta cuenta.  No se trata de la misma contraseña que se emplea para jugar al juego.'

ActivateChat = """La herramienta Amigos secretos permite a los socios charlar entre sí gracias al uso de un código secreto que se debe comunicar fuera del juego.  Para obtener toda la información, haz clic aquí:

La herramienta Amigos secretos no está moderada ni supervisada.  Si los padres permiten a sus hijos usar su cuenta con la opción Amigos secretos activada, les aconsejamos que los supervisen mientras juegan.  Una vez activada, la herramienta Amigos secretos está disponible hasta que se desactiva.

Al activar la herramienta Amigos secretos, los padres reconocen que existen ciertos riesgos inherentes a la posibilidad de charla de la herramienta y reconocen que han sido informados sobre dichos riesgos y están de acuerdo en aceptarlos."""

ActivateChatYes = "Activar"
ActivateChatNo = "Cancelar"
ActivateChatMoreInfo = "Más información"
ActivateChatPrivacyPolicy = "Normas de confidencialidad"

LeaveToPay = """Para adquirir Toontown, el producto irá a Toontown.com."""
LeaveToPayYes = "Adquirir"
LeaveToPayNo = "Cancelar"

#LeaveToSetParentPassword = """In order to set parent password, the game will exit to Toontown.com."""
#LeaveToSetParentPasswordYes = "Set Password"
#LeaveToSetParentPasswordNo = "Cancel"

ChatMoreInfoOK = "Aceptar"
SecretChatActivated = '¡La herramienta "Amigos secretos" ha sido activada!\n\nSi más tarde cambias de opinión y decides desactivar esta herramienta, haz clic en "Opciones de cuenta" en la página web de Toontown.'
SecretChatActivatedOK = "Aceptar"
ProblemActivatingChat = '¡Vaya!  No hemos podido activar la herramienta de charla "Amigos secretos".\n\n%s\n\nVuelve a intentarlo más tarde.'
ProblemActivatingChatOK = "Aceptar"

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "¡Hola, %!",
        "Eh, %, me alegro de verte.",
        "¡Me alegro de que hayas venido hoy!",
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
        "Parece que te lo pasas pipa.",
        "Caramba, qué buen día estoy teniendo.",
        "Me gusta lo que llevas puesto.",
        "Creo que esta tarde me voy a ir de pesca.",
        "Diviértete en mi barrio.",
        "¡Espero que te lo estés pasando en grande en Toontown!",
        "Me han dicho que en Frescolandia está nevando.",
        "¿Has subido hoy al tranvía?",
        "Me gustaría conocer a más gente.",
        "Caramba, en Frescolandia hay un montón de bots.",
        "Me encanta jugar al \"Tú la llevas\". ¿Y a ti?",
        "Los juegos del tranvía son divertidísimos.",
        "Me encanta hacer que la gente se ría.",
        "Ayudar a los amigos es muy divertido.",
        "Ejem, ¿te has perdido?  No olvides que tienes un mapa en el dibucuaderno.",
        "¡Que no te líen los bots con su cinta roja!",
        "Me han dicho que Daisy ha plantado flores nuevas en su jardín.",
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
        "Es la hora de ponerse en marcha.",
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
        "Bienvenido al Centro de Toontown.",
        "Hola, me llamo Mickey. ¿Cómo te llamas?",
        ],
        [ # Comments
        "Eh, ¿has visto a Donald?",
        "Voy a ver cómo sube la marea en Puerto Donald.",
        "Si ves a mi amiguete Goofy, dale recuerdos de mi parte.",
        "Me han dicho que Daisy ha plantado flores nuevas en su jardín.",
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a Minnie!",
        "¡Dios mío, llego tarde a mi cita con Minnie!",
        "Parece que es la hora de la cena de Pluto.",
        "Creo que voy a Puerto Donald a nadar un poco.",
        "Es la hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "Bienvenido a Melodilandia.",
        "Hola, me llamo Minnie. ¿Cómo te llamas?",
        ],
        [ # Comments
        "¡La música se siente por todas partes!",
        "No te olvides de montarte en el gran tiovivo.",
        "Llevas un disfraz muy chulo, %.",
        "Eh, ¿has visto a Mickey?",
        "Si ves a mi amigo Goofy, dale recuerdos de mi parte.",
        "Caramba, en Sueñolandia de Donald hay un montón de bots.",
        "Me han dicho que en Puerto Donald hay niebla.",
        "No te olvides de probar el laberinto de los Jardines de Daisy.",
        "Creo que voy a escuchar música.",
        "Eh, %, mira eso.",
        "Me encanta la música.",
        "¿A que no sabías que a Melodilandia también la llaman Cancioncity?  ¡Ji, ji!",
        "Me encanta jugar al juego de imitar movimientos. ¿Y a ti?",
        "Me encanta hacer reír a la gente.",
        "¡Uf, andar todo el día con tacones acaba haciendo daño a los pies!",
        "Qué camisa más bonita, %.",
        "¿Eso del suelo es una gominola?",
        ],
        [ # Goodbyes
        "¡Vaya, llego tarde a mi cita con %s!" % Mickey,
        "Parece que es la hora de la cena de %s." % Pluto,
        "Es la hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "Bienvenido a los Jardines de Daisy.",
        "Hola, me llamo Goofy. ¿Y tú?",
        "¡Hola, me alegro de verte, %!",
        ],
        [ # Comments
        "¡Vaya! ¡Cualquiera se pierde en el laberinto del jardín!",
        "No te olvides de ir al laberinto.",
        "No he visto a Daisy en todo el día.",
        "¿Dónde estará Daisy?",
        "Eh, ¿has visto a Donald?",
        "Si ves a mi amigo Mickey, dale recuerdos de mi parte.",
        "¡Oh! ¡Me he olvidado de prepararle el desayuno a Mickey!",
        "Guau, seguro que en Puerto Donald hay un montón de bots.",
        "Parece ser que Daisy ha plantado flores nuevas en su jardín.",
        "¡Las gafas hipnóticas están rebajadas a una gominola en mi tienda de bromas de Frescolandia!",
        "¡Las tiendas de bromas de Goofy tienen las mejores bromas, trucos y gansadas de todo Toontown!",
        "En las tiendas de bromas de Goofy garantizamos que todas las tartas en la cara te harán reír. ¡Si no es así, te devolvemos tus gominolas!"
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a Minnie!",
        "¡Vaya, llego tarde a mi cita con Donald!",
        "Creo que voy a Puerto Donald a nadar un poco.",
        "Es la hora de la siesta. Me voy a Sueñolandia.",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "Bienvenido a Sueñolandia.",
        "Hola, me llamo %s. ¿Y tú?" % Donald,
        ],
        [ # Comments
        "A veces, este sitio me da escalofríos.",
        "No te olvides de probar el laberinto de los Jardines de Daisy.",
        "Caramba, qué buen día estoy teniendo.",
        "Eh, ¿has visto a Mickey?",
        "Si ves a mi buen amigo Goofy, dale recuerdos de mi parte.",
        "Creo que esta tarde me voy a ir de pesca.",
        "Caramba, en Puerto Donald hay un montón de bots.",
        "Eh, ¿no te he llevado en barco en Puerto Donald?",
        "No he visto a Daisy en todo el día.",
        "Me han dicho que "+Daisy+" ha plantado flores nuevas en su jardín.",
        "Cuac.",
        ],
        [ # Goodbyes
        "¡Me voy a Melodilandia a ver a %s!" % Minnie,
        "¡Vaya! ¡Llego tarde a mi cita con %s!" % Daisy,
        "Creo que voy a mi puerto a nadar un poco.",
        "Creo que voy a darme una vuelta en mi barco en Puerto Donald.",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)


# ToontownClientRepository.py
TCRConnecting = "Conectando..."
# host, port
TCRNoConnectTryAgain = "Imposible conectar con %s:%s. ¿Quieres intentarlo de nuevo?"
TCRNoConnectProxyNoPort = "Imposible conectar con %s:%s.\n\nTe estás conectando al Internet a través de un proxy que no permite las conexiones al puerto %s.\n\nPara jugar a Toontown es necesario abrir este puerto o desactivar el proxy.  Si el proxy ha sido suministrado por tu proveedor de Internet, debes ponerte en contacto con él para que abra este puerto."
TCRNoDistrictsTryAgain = "No hay distritos de Toontown disponibles. ¿Deseas intentarlo de nuevo?"
TCRLostConnection = "Tu conexión de Internet a Toontown se ha interrumpido inesperadamente."
TCRBootedReasons = {
    1: "Se ha producido un problema inesperado.  Se ha perdido la conexión, pero deberías poder conectarte de nuevo y volver al juego.",
    100: "Has sido desconectado porque otra persona que ha abierto una sesión con tu cuenta en otro ordenador.",
    120: "Has sido desconectado debido a un problema con tu autorización para usar la charla mediante el teclado.",
    122: "Se ha producido un problema inesperado en la conexión con Toontown.  Ponte en contacto con el Servicio de atención al cliente de Toontown.",
    125: "Tus archivos instalados de Toontown parecen ser incorrectos. Pulsa el botón Jugar de la página web oficial de Toontown para ejecutar el juego.",
    126: "No tienes privilegios de administrador.",
    151: "Tu sesión ha sido cerrada por un administrador de los servidores de Toontown.",
    153: "Se ha reiniciado el distrito de Toontown en el que te hallabas.  Todos los que estaban en ese distrito han sido desconectados.  Sin embargo, deberías poder conectarte de nuevo para volver al juego.",
    288: "Lo sentimos, pero has gastado todos los minutos de que disponías en Toontown este mes.",
    349: "Lo sentimos, pero has gastado todos los minutos de que disponías en Toontown este mes.",
    }
TCRBootedReasonUnknownCode = "Ha surgido un problema inesperado (código de error %s).  Se ha perdido la conexión, pero deberías poder conectarte de nuevo y volver al juego."
TCRTryConnectAgain = "\n\n¿Quieres intentar conectarte de nuevo?"
# avName
TCRTutorialAckQuestion = "%s es nuevo en Toontown.\n\n¿Quieres que Mickey te lo enseñe?"
TCRTutorialAckOk = "Sí"
TCRTutorialAckCancel = "No"
TCRToontownUnavailable = "Toontown no parece estar disponible por el momento; seguimos intentándolo..."
TCRToontownUnavailableCancel = "Cancelar"
TCRNameCongratulations = "¡¡ENHORABUENA!!"
TCRNameAccepted = "Tu nombre ha sido\naprobado por el Consejo Dibu.\n\nA partir de ahora,\nte llamarás\n\"%s\""
TCRServerConstantsProxyNoPort = "Imposible ponerse en contacto con %s.\n\nTe estás conectando al Internet a través de un proxy que no permite conexiones al puerto %s.\n\nPara jugar a Toontown es necesario abrir este puerto o desactivar el proxy.  Si el proxy ha sido suministrado por tu proveedor de Internet, debes ponerte en contacto con él para que abra este puerto."
TCRServerConstantsProxyNoCONNECT = "Imposible ponerse en contacto con %s.\n\nTe estás conectando al Internet a través de un proxy que no es compatible con el método CONNECT.\n\nPara jugar a Toontown es necesario activar esta opción o desactivar el proxy.  Si el proxy ha sido suministrado por tu proveedor de Internet, debes ponerte en contacto con él para activar esta opción."
TCRServerConstantsTryAgain = "Imposible ponerse en contacto con %s.\n\nEl servidor de la cuenta de Toontown podría estar inoperativo en este momento, o puede ser que haya surgido un problema con tu conexión de Internet.\n\n¿Deseas intentarlo de nuevo?"
TCRServerDateTryAgain = "Imposible obtener la fecha del servidor de %s. ¿Deseas intentarlo de nuevo?"
AfkForceAcknowledgeMessage = "A tu dibu le ha entrado sueño y se ha ido a la cama."
PeriodTimerWarning = "¡Tu límite de tiempo en Toontown este mes casi ha terminado!"
PeriodForceAcknowledgeMessage = "Has gastado todos los minutos de que disponías en Toontown este mes.  ¡Ven otra vez a jugar el mes que viene!"
TCREnteringToontown = "Entrando a Toontown..."

# FriendInvitee.py
FriendInviteeTooManyFriends = "%s desea ser tu amigo, pero ya tienes demasiados amigos en tu lista."
FriendInviteeInvitation = "A %s le gustaría ser tu amigo."
FriendInviteeOK = "Aceptar"
FriendInviteeNo = "No"

# FriendInviter.py
FriendInviterOK = "Aceptar"
FriendInviterCancel = "Cancelar"
FriendInviterStopBeingFriends = "Dejar de ser amigo"
FriendInviterYes = "Sí"
FriendInviterNo = "No"
FriendInviterClickToon = "Haz clic en el dibu del que deseas ser amigo."
FriendInviterTooMany = "No puedes añadir más amigos a tu lista porque ya tienes demasiados. Si quieres ser amigo de %s, tendrás que quitar algunos amigos de tu lista."
FriendInviterNotYet = "¿Quieres ser amigo de %s?"
FriendInviterCheckAvailability = "Comprobando si %s está disponible."
FriendInviterNotAvailable = "%s está ocupado ahora mismo. Inténtalo más tarde."
FriendInviterWentAway = "%s se ha marchado."
FriendInviterAlready = "%s ya es tu amigo."
FriendInviterAskingCog = "Preguntando a %s si quiere ser tu amigo."
FriendInviterEndFriendship = "¿Seguro que quieres dejar de ser amigo de %s?"
FriendInviterFriendsNoMore = "%s ya no es tu amigo."
FriendInviterSelf = "¡ Ya eres tu propio amigo!"
FriendInviterIgnored = "%s no te está haciendo caso."
FriendInviterAsking = "Preguntando a %s si quiere ser tu amigo."
FriendInviterFriendSaidYes = "¡%s ha dicho que sí!"
FriendInviterFriendSaidNo = "%s ha dicho que no, gracias."
FriendInviterFriendSaidNoNewFriends = "%s no quiere tener amigos nuevos ahora mismo."
FriendInviterTooMany = "¡%s ya tiene demasiados amigos!"
FriendInviterMaybe = "%s no ha podido responder."
FriendInviterDown = "Imposible hacer amigos ahora."

# FriendSecret.py
FriendSecretNeedsPasswordWarningTitle = "Parental Controls"
FriendSecretNeedsPasswordWarning = """To get or type a secret, you must enter the Parent Password.  You can disable this prompt in Member Services on the Toontown web page."""
FriendSecretNeedsPasswordWarningOK = "OK"
FriendSecretNeedsPasswordWarningCancel = "Cancel"
FriendSecretNeedsPasswordWarningWrongPassword = """That's not the correct password.  Please enter the Parent Password created when purchasing this account.  This is not the same password used to play the game."""
FriendSecretIntro = "Si estás jugando a Disney's Toontown Online con alguien que conozcas en la vida real, los dos pueden convertirse en amigos secretos.  Puedes charlar con tus amigos secretos usando el teclado.  Los demás dibus no entenderán lo que estás diciendo.\n\nPara hacer esto, necesitas obtener un Secreto.  Transmítele el Secreto a tu amigo y a nadie más.  Cuando tu amigo escriba el Secreto en su pantalla, los dos seran amigos secretos en Toontown."
FriendSecretGetSecret = "Obtener Secreto"
FriendSecretEnterSecret = "Si tienes un Secreto de alguien que conozcas, escríbelo aquí."
FriendSecretOK = "Aceptar"
FriendSecretCancel = "Cancelar"
FriendSecretGettingSecret = "Obteniendo Secreto. . ."
FriendSecretGotSecret = "Aquí tienes tu nuevo Secreto.  ¡No te olvides de anotarlo!\n\nPuedes dar este Secreto solamente a una persona.  Cuando alguien escriba tu Secreto, éste no valdrá ya para nadie más.  Si deseas dar un Secreto a alguien más, tienes que pedir otro.\n\nEl Secreto sólo valdrá durante los dos días siguientes.  Tu amigo tendrá que escribirlo antes de que desaparezca, o de lo contrario el proceso no funcionará.\n\nTu Secreto es:"
FriendSecretTooMany = "Lo siento, no puedes tener más Secretos hoy.  ¡Ya has tenido más que suficientes!\n\nPrueba de nuevo mañana."
FriendSecretTryingSecret = "Probando Secreto. . ."
FriendSecretEnteredSecretSuccess = "¡Ya eres amigo secreto de %s!"
FriendSecretEnteredSecretUnknown = "Ése no es el Secreto de nadie.  ¿Seguro que lo has escrito bien?\n\nSi lo has escrito correctamente, tal vez haya caducado.  Pídele a tu amigo que te obtenga un Secreto nuevo (o consigue tú uno y dáselo a tu amigo)."
FriendSecretEnteredSecretFull = "No puedes ser amigo de %s porque uno de los dos tiene demasiados amigos en la lista."
FriendSecretEnteredSecretFullNoName = "No pueden ser amigos porque uno de los dos tiene demasiados amigos en la lista."
FriendSecretEnteredSecretSelf = "¡Acabas de escribir tu propio Secreto!  Ahora, nadie más puede usar ese Secreto."
FriendSecretNowFriends = "¡Ya eres amigo secreto de %s!"
FriendSecretNowFriendsNoName = "¡Ya sois amigos secretos!"

# FriendsListPanel.py
FriendsListPanelNewFriend = "Amigo nuevo"
FriendsListPanelSecrets = "Secretos"
FriendsListPanelOnlineFriends = "AMIGOS\nCONECTADOS"
FriendsListPanelAllFriends = "TODOS LOS\nAMIGOS"
FriendsListPanelIgnoredFriends = "DIBUS NO\nATENDIDOS"
FriendsListPanelPets = "NEARBY\nPETS"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "Lo siento; no puedes avanzar porque la descarga de %(phase)s sólo lleva completada un %(percent)s%%.\n\nVuelve a intentarlo más tarde."

# TeaserPanel.py
TeaserTop = "  Sorry, but you can't do that in the free trial.\n\nSubscribe now and enjoy these great features:"
TeaserOtherHoods = "Visit all 6 unique neighborhoods!"
TeaserTypeAName = "Type in your favorite name for your toon!"
TeaserSixToons = "Create up to 6 Toons on one account!"
TeaserOtherGags = "Collect 6 skill levels in 6 different gag tracks!"
TeaserClothing = "Buy unique clothing items to individualize your toon!"
TeaserFurniture = "Purchase and arrange furniture in your own house!"
TeaserCogHQ = "Infiltrate dangerous advanced Cog areas!"
TeaserSecretChat = "Trade secrets with friends so you can chat with them online!"
TeaserCardsAndPosters = "Collect Toontown trading cards and posters!"
TeaserHolidays = "Participate in exciting special events and holiday celebrations!"
TeaserQuests = "Complete hundreds of ToonTasks to help save Toontown!"
TeaserEmotions = "Purchase emotions to make your Toon more expressive!"
TeaserMinigames = "Play all 8 minigame varieties!"
TeaserSubscribe = "Subscribe Now"
TeaserContinue = "Continue Trial"

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "Descargando %s."
DownloadWatcherInitializing = "Iniciando descarga..."

# Launcher.py
LauncherPhaseNames = {
    0   : "Inicializando",
    3   : "Crear un dibu",
    3.5 : "Dibututorial",
    4   : "Dibuparque",
    5   : "Calles",
    5.5 : "Propiedades",
    6   : "Barrio I",
    7   : "Edificios " + Cog,
    8   : "Barrio II",
    9   : "Cuartel general" + Cog,
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
LauncherStartingToontown = "Iniciando Toontown..."
LauncherRecoverFiles = "Actualizando Toontown. Recuperando archivos..."
LauncherCheckUpdates = "Comprobando actualizaciones para " + LauncherProgress
LauncherVerifyPhase = "Actualizando Toontown..."

# AvatarChoice.py
AvatarChoiceMakeAToon = "Crea un\ndibu"
AvatarChoicePlayThisToon = "Juega con\neste dibu"
AvatarChoiceSubscribersOnly = "Subscribe\n\n\n\nNow!"
AvatarChoiceDelete = "Borrar"
AvatarChoiceDeleteConfirm = "Con esto borrarás a %s para siempre."
AvatarChoiceNameRejected = "Nombre\nrechazado"
AvatarChoiceNameApproved = "¡Nombre\naprobado!"
AvatarChoiceNameReview = "En proceso\nde revisión"
AvatarChoiceNameYourToon = "¡Pon un nombre\na tu dibu!"
AvatarChoiceDeletePasswordText = "¡Cuidado! Con esto borrarás a %s para siempre. Para borrar este dibu, escribe tu contraseña."
AvatarChoiceDeleteConfirmText = "¡Cuidado! Con esto borrarás a %(name)s para siempre.  Para confirmar escribe \"%(confirm)s\" y hace click en Aceptar."
AvatarChoiceDeleteConfirmUserTypes = "Borrar"
AvatarChoiceDeletePasswordTitle = "¿Quieres borrar este dibu?"
AvatarChoicePassword = "Contraseña"
AvatarChoiceDeletePasswordOK = "Aceptar"
AvatarChoiceDeletePasswordCancel = "Cancelar"
AvatarChoiceDeleteWrongPassword = "Esa contraseña no coincide. Para borrar este dibu, escribe tu contraseña."
AvatarChoiceDeleteWrongConfirm = "Tú no has escrito la palabra correcta.  Para borrar a %(name)s, escribe \"%(confirm)s\" y hace click en Aceptar.  No escribas las apóstrofes .  Hace click en Cancelar, si has cambiado de parecer."

# AvatarChooser.py
AvatarChooserPickAToon = "Escoge el dibu con el que vas a jugar"
AvatarChooserQuit = "Salir"

# MultiPageTextFrame.py
MultiPageTextFrameNext = 'Siguiente'
MultiPageTextFramePrev = 'Anterior'
MultiPageTextFramePage = 'Página %s/%s'

# MemberAgreementScreen.py
MemberAgreementScreenTitle = 'Contrato de registro'
MemberAgreementScreenAgree = 'Acepto'
MemberAgreementScreenDisagree = 'No acepto'
MemberAgreementScreenCancel = 'Cancelar'
MemberAgreementScreenWelcome = "¡Bienvenido!"
MemberAgreementScreenOnYourWay = "Se ha iniciado el proceso para que te conviertas en un socio oficial de"
MemberAgreementScreenToontown = "Avance preliminar de Disney's Toontown Online"
MemberAgreementScreenPricing = "El avance preliminar de Disney's Toontown Online cuesta             \nel primer mes. Cada mes adicional es              .\nY el registro es fácil: basta con leer y rellenar la \ninformación que aparece a continuación y ya está."
MemberAgreementScreenCCUpFrontPricing = "Inscríbete ya en la prueba GRATUITA de      días. Puedes cancelar tu suscripción\nen cualquier momento del período gratuito sin coste alguno. Al final del\nperíodo gratuito de prueba, se te facturarán automáticamente            por\nel primer mes, y después,            por cada mes adicional."
MemberAgreementScreenGetParents = "Debes tener al menos 18 años para adquirir Disney's Toontown Online. Pide a tus padres o tutores que te ayuden."
MemberAgreementScreenGetParentsUnconditional = "Debes tener al menos 18 años para adquirir Disney's Toontown Online. Si tienes menos de 18 años, pide ayuda a tus padres o tutores."
MemberAgreementScreenMustBeOlder = "Debes tener al menos 18 años para adquirir Disney's Toontown Online. Pide a tus padres o tutores que te ayuden."
MemberAgreementScreenYouMustAgree = "Para adquirir Disney's Toontown Online, debes aceptar el Contrato de registro."
MemberAgreementScreenYouMustAgreeOk = "Aceptar"
MemberAgreementScreenYouMustAgreeQuit = "Salir"
MemberAgreementScreenAgreementTitle = "Contrato de registro"
MemberAgreementScreenClickNext = "Pulsa \"Siguiente\" para pasar a la página siguiente."
# this is useful for tweaking the member agreement:
#import LocalizerEnglish; import Localizer
#reload(LocalizerEnglish);reload(Localizer);page=toonbase.tcr.memberAgreementScreen.memAgreement.getCurPage();toonbase.tcr.loginFSM.request('freeTimeInform');toonbase.tcr.loginFSM.request('memberAgreement');toonbase.tcr.memberAgreementScreen.memAgreement.setPage(page)
MemberAgreementScreenLegalText = [
"""





""" # spacing for graphics; start next section on a new line (i.e. """\nText)
"""
CONTRATO DE REGISTRO DE TOONTOWN ONLINE DE DISNEY

Bienvenido/a a Toontown Online de Disney (en lo sucesivo, el "Servicio"). LE ROGAMOS QUE LEA ATENTAMENTE ESTE CONTRATO (EN LO SUCESIVO, EL "CONTRATO") ANTES DE UTILIZAR ESTE SERVICIO. Este Servicio es propiedad de Disney Online, el cual se encarga también de su explotación (en la presente, referido como "Disney", "nosotros" o cualquier forma de la primera persona del plural).
""","""
El uso de este Servicio implica la aceptación de estas condiciones, las Cláusulas de utilización y las Normas de la casa que aparecen en nuestro sitio Web. Si no está de acuerdo con todas ellas, le rogamos que se abstenga de utilizar este Servicio. Tenga en cuenta que en este Contrato usted aparecerá como el "Socio". La persona que se registre por primera vez en el Servicio también recibirá la denominación de "Cuenta matriz" en este documento. Por "Cuenta" se entiende la cuenta con la que se ha registrado cualquier socio, en virtud de los procedimientos de registro del Servicio. Las cláusulas de este Contrato serán de aplicación para todos los Socios, conformen éstos o no la Cuenta matriz. El titular de la Cuenta matriz será responsable de hacer que todos los socios de una misma familia (y cualquier otra persona a la que permita jugar mediante la Cuenta) conozcan las condiciones de este Contrato y de garantizar que las cumplan. El titular de la Cuenta matriz de una Cuenta cualquiera será totalmente responsable de todas las actividades que se lleven a cabo mediante dicha Cuenta.
""","""
Nos reservamos el derecho, cuando así lo estimemos oportuno, de cambiar, modificar, agregar o eliminar cualquier parte de este Contrato en cualquier momento. Todas las modificaciones realizadas en él serán notificadas por medio de su publicación en el Servicio o mediante correo electrónico u ordinario.

Si algún cambio futuro en este Contrato resultase inaceptable para usted, o debido a dicho cambio usted no cumpliese dicho Contrato, podrá cancelar su Cuenta. El uso continuado por su parte del Servicio tras haber sido informado de los cambios que se hayan dado en el Contrato (incluidas las Cláusulas de uso y las Normas de la casa) implicará que ha aceptado dichos cambios.
""","""
Nos reservamos el derecho de cambiar, modificar, suspender o interrumpir cualquiera de los aspectos del Servicio en cualquier momento, lo que incluye, entre otros aspectos, la disponibilidad de cualquier Servicio, base de datos o contenido, las horas de disponibilidad y el equipo necesario para acceder al Servicio. También podremos establecer límites sobre algunas funciones concretas o restringir su acceso a parte o la totalidad del Servicio, durante amplios periodos, sin notificación previa y sin que incurramos en ninguna responsabilidad.

El Socio será el único responsable de obtener la conexión telefónica y el equipo necesarios para acceder al Servicio, lo que incluye, entre otras partes del equipo, el software y los medios de a Internet.
""","""
RESTRICCIONES EN EL USO DEL MATERIAL

Todo el material publicado por Disney (incluidos, entre otros, los recursos de información, las fotografías, las imágenes, las ilustraciones y los clips de sonido y de vídeo, denominados de manera colectiva el "Contenido") están protegidos por derechos de copyright y son propiedad de Disney, sus empresas matrices o filiales o cualquier proveedor externo, y están controlados por todos ellos. El socio deberá acatar todas las notificaciones informaciones y restricciones de copyright que aparezca en cualquier Contenido al que tenga acceso mediante el Servicio.
""","""
El Servicio está protegido por derechos de copyright como trabajo colectivo y/o recopilación, en virtud de las leyes estadounidenses de copyright, los convenios internacionales y el resto de las leyes sobre copyright existentes. Queda prohibido copiar, reproducir, volver a publicar, subir a un sitio web, publicar y transmitir cualquier material procedente del Servicio o de cualquier sitio Web que sea propiedad de Disney, que esté explotado o controlado por Disney o sobre el cual Disney posea una licencia; asimismo está prohibido crear y distribuir cualquier trabajo derivado de dicho material, excepto en el caso de la descarga de Internet de una copia del material en un único ordenador para su uso personal no comercial, siempre y cuando cumpla todas las notificaciones de copyright y de propiedad. La utilización de nuestro Contenido para cualquier otro uso constituirá una violación de nuestros derechos de copyright y de propiedad. A efectos de este Contrato, el uso de cualquier parte de nuestro Contenido en cualquier otro sitio web o en cualquier ordenador que esté conectado a una red queda terminantemente prohibido. No está autorizado a vender ni subastar ninguno de los personajes, artículos y material protegidos por los derechos de copyright de Disney.
""","""
Si descarga algún tipo de software del Servicio, dicho software, incluidos todos los archivos, las imágenes que se encuentren en él o que éste genere y todos los datos que acompañen a dicho software (denominados, de manera colectiva, el "Software"), contará con la licencia que le ofrece Disney. Por la presente, le conferimos una licencia no exclusiva para utilizar el Software únicamente en relación con el Servicio a través de una Cuenta autorizada y pagada (o una versión de prueba autorizada). La Cuenta matriz pacta y acuerda que (a) ninguno de los materiales, sea del tipo que sea, que se envíe a través de su Cuenta podrá (i) transgredir, plagiar o infringir en menoscabo de los derechos a terceros, incluidos los derechos de copyright, marca registrada, confidencialidad y cualquier otro tipo de derecho personal o de propiedad, ni (ii) contener material ilegal ni injurioso; (b) el número de la tarjeta de crédito que nos ha facilitado es válido, el titular de la Cuenta matriz tiene la autorización para utilizar dicha tarjeta de crédito y tiene al menos 18 años de edad; (c) podemos cargar pagos en la tarjeta de crédito cuyo número se nos ha proporcionado, tal y como se describe en detalle en la sección llamada "Precios y pagos" que aparece a continuación y (d) el titular de la Cuenta matriz y todos los Socios cumplirán plenamente las cláusulas de este Contrato.
""","""
El titular de la Cuenta matriz, por la presente eximirá a Disney, sus empresas matrices y filiales, y a cualquier empleado, cargo directivo, propietario, agente, proveedor de información, afiliado, licenciatario o concedente (denominados de manera colectiva las "Partes eximidas") de cualquier indemnización por daños y perjuicios en los que hayan incurrido las Partes eximidas en conexión con cualquier reclamación derivada del incumplimiento por parte suya o de cualquier otro Socio. Disney no acuerda ni acepta la exactitud ni la fiabilidad de ningún consejo, opinión, declaración o cualquier otro tipo de información publicada, subida o distribuida mediante el Servicio por parte de cualquier Socio, proveedor de información o cualquier otra persona física o jurídica. Por la presente, el Socio acepta bajo su propio riesgo la fiabilidad de dichas opiniones, consejos, declaraciones, memorandos o información en general. Disney se reserva el derecho, cuando así lo estime oportuno, de corregir cualquier error u omisión en cualquier parte del Servicio.
""","""
EXENCIÓN DE RESPONSABILIDAD

EL MATERIAL QUE APARECE EN ESTE SERVICIO SE OFRECE "TAL Y COMO ESTÁ" Y SIN NINGÚN TIPO DE GARANTÍA, IMPLÍCITA NI EXPLÍCITA. SIEMPRE QUE LA LEY VIGENTE LO PERMITA, DISNEY ESTARÁ EXENTO DE TODAS LAS GARANTÍAS, IMPLÍCITAS O EXPLÍCITAS, INCLUIDAS, ENTRE OTRAS, LAS GARANTÍAS IMPLÍCITAS DE COMERCIALIZACIÓN Y ADECUACIÓN A UN OBJETIVO CONCRETO. DISNEY NO GARANTIZA QUE LAS FUNCIONES QUE APARECEN EN ESTE SERVICIO ESTÉN EXENTAS DE INTERRUPCIONES O ERRORES, QUE SE CORRIJAN TODOS LOS DEFECTOS NI QUE ESTE SERVICIO NI EL SERVIDOR A TRAVÉS DEL QUE FUNCIONA ESTÉN EXENTOS DE VIRUS U OTROS COMPONENTES DAÑINOS. DISNEY NO GARANTIZA TAMPOCO NI ACUERDA NINGUNA CLÁUSULA RESPECTO AL USO O LAS CONSECUENCIAS DEL USO DEL MATERIAL DE ESTE SERVICIO EN CUANTO A SU EXACTITUD, FIABILIDAD, ETC.
""","""
EL SOCIO (Y NO DISNEY) ASUME EL COSTO TOTAL POR CUALQUIER TAREA DE MANTENIMIENTO, REPARACIÓN O CORRECCIÓN. EN CASO DE QUE LA LEY VIGENTE PROHÍBA LA EXCLUSIÓN DE LAS GARANTÍAS IMPLÍCITAS, LA EXCLUSIÓN ANTERIOR PUEDE NO RESULTAR DE APLICACIÓN EN SU CASO.

SIN PERJUICIO DE LO ESTABLECIDO ANTERIORMENTE, EL SOCIO RECONOCE QUE, EN LA CALIDAD DE SERVICIO PARA LOS USUARIOS DEL SERVICIO DE DISNEY, PODEMOS INCLUIR ENLACES A OTROS SITIOS WEB DE INTERNET, Y DISNEY NO TIENE NINGÚN CONTROL NI PACTA NINGÚN TIPO DE GARANTÍA EN RELACIÓN CON EL CONTENIDO O LA ADECUACIÓN DEL CONTENIDO DE DICHOS SITIOS WEB. EL SOCIO, POR LA PRESENTE, NOS EXIME DE MANERA IRREVOCABLE DE CUALQUIER RECLAMACIÓN REFERIDA A DICHOS SITIOS WEB.
""","""
Además, Disney rechaza cualquier responsabilidad relativa a la exactitud, el contenido o la disponibilidad de la información que aparece en los sitios web a los que se acceda a través de Toontown Online de Disney de terceros que no estén asociados con Disney. En Disney le aconsejamos que sea precavido cuando navegue por el Internet, ya se encuentre, utilizando nuestro servicio o el de cualquier otra persona o empresa. Dado que en ocasiones algunos sitios utilizan los resultados de búsquedas automatizadas o bien conducen a sitios web que contienen información que puede ser considerada ofensiva o inadecuada, Disney no se responsabilizará por la exactitud ni por el cumplimiento de los derechos de copyright, legalidad o decencia del material en los sitios Web de terceros, y el socio, por la presente, nos exime de cualquier reclamación contra nosotros en relación con dichos sitios web. Disney no podrá garantizarle que estará satisfecho con los productos o servicios que contrate en un sitio Web de terceros conectado a Toontown Online de Disney, ya que los canales de otros establecimientos son propiedad de otros minoristas que los explotan.
""","""
Disney no garantiza ninguna de las mercancías, ni tampoco confirma la exactitud o la fiabilidad de la información que aparezca en los sitios web de dichas terceras personas. Disney no pacta ni garantiza la seguridad de ningún tipo de información, lo que incluye, entre otras cosas, los datos de su tarjeta de crédito y cualquier otro tipo de información personal que le pida cualquier empresa externa, y el Socio, por la presente, nos exime de cualquier reclamación contra nosotros en relación con dichos sitios web. Le rogamos encarecidamente que efectúe las investigaciones necesarias o que considere adecuadas antes de realizar cualquier transacción a través del Internet o fuera de ella con dichas terceras partes.
""","""
RESPONSABILIDAD LIMITADA

BAJO NINGUNA CIRCUNSTANCIA, INCLUIDA, ENTRE OTRAS, LA NEGLIGENCIA, SERÁ DISNEY RESPONSABLE DE NINGUNA INDEMNIZACIÓN POR DAÑOS Y PERJUICIOS, ESPECIALES O INDIRECTOS, QUE SE DERIVEN DEL USO DE LOS MATERIAL DE ESTE SERVICIO O DE CUALQUIER SITIO WEB, NI DE LA INCAPACIDAD PARA USARLO, NI SIQUIERA EN EL CASO DE QUE DISNEY O UN REPRESENTANTE AUTORIZADO POR DISNEY HAYA SIDO ADVERTIDO DE LA POSIBILIDAD DE DICHA RECLAMACIÓN POR DAÑOS Y PERJUICIOS. ES POSIBLE QUE LA LEGISLACIÓN VIGENTE NO PERMITA LA EXCLUSIÓN O LA LIMITACIÓN DE RESPONSABILIDAD O DE DAÑOS Y PERJUICIOS ACCESORIOS O INDIRECTOS, POR LO CUAL LA LIMITACIÓN O EXCLUSIÓN ANTERIOR PUEDE NO RESULTAR APLICABLE PARA USTED. EN TODO CASO, LA RESPONSABILIDAD TOTAL DE DISNEY FRENTE AL SOCIO POR CUALQUIER INDEMNIZACIÓN POR DAÑOS Y PERJUICIOS, PÉRDIDAS Y ACCIONES LEGALES (YA SEAN CONTRACTUALES O POR ILÍCITO CIVIL INCLUIDA, ENTRE OTRAS, LA NEGLIGENCIA) NO SOBREPASARÁ LA CANTIDAD ABONADA, DE HABERLO HECHO, PARA ACCEDER AL SERVICIO.
""","""
SEGURIDAD

Como parte integrante del proceso de registro, los Socios deberán elegir una contraseña, una contraseña principal y un nombre de socio (en lo sucesivo, el "Nombre de socio"). Deberá proporcionar a Disney información de la Cuenta actualizada, exacta y completa. En caso contrario, estará incumpliendo este Contrato, lo que puede resultar en la cancelación inmediata de su Cuenta. En ningún caso podrá (i) seleccionar o utilizar el Nombre de socio de otra persona con la intención de hacerse pasar por esa persona; (ii) utilizar un nombre que esté sujeto a los derechos de otra persona sin autorización o (iii) utilizar un Nombre de socio que, en opinión de Disney, sea inadecuado u ofensivo.
""","""
En caso de que le conste o sospeche que existe algún usuario no autorizado de su Cuenta, o si conoce algún incumplimiento de la seguridad (o lo sospecha), lo que incluye la pérdida, el robo y la divulgación no autorizada de su contraseña o de la contraseña principal, deberá notificárselo inmediatamente a Disney en la dirección de correo electrónico toontown@disneyonline.com,. La responsabilidad de mantener la confidencialidad de su contraseña y contraseña principal será únicamente suya.

Todos los titulares de las Cuentas matrices deberán tener 18 años de edad o más para poder abrir una Cuenta. Si Disney descubriese que el titular de una Cuenta matriz es menor de 18 años, se reserva el derecho de cancelar dicha Cuenta.

Cualquier actividad fraudulenta, abusiva o que no resulte conforme a derecho puede constituir la base de la cancelación de su Cuenta, y cuando Disney así lo estime oportuno, se pondrá su caso en conocimiento de las instituciones legislativas pertinentes.
""","""
PRECIOS Y PAGOS

Disney se reserva el derecho de cobrar, cuando así lo considere oportuno, cualquier tarifa adicional por el acceso al Servicio. Disney se reserva el derecho de cobrar cualquier cantidad o tarifa por el Servicio y de establecer nuevas tarifas o precios, que entrarán en vigor previa notificación a los Socios. Disney se reserva el derecho de ofrecer el Servicio de manera gratuita por motivos promocionales u otras razones (como, por ejemplo, una versión de prueba).

Los titulares de las Cuentas matrices se comprometen a abonar todos los pagos en que incurra la Cuenta matriz, incluidos los impuestos vigentes, de conformidad con las normas de facturación existentes en el momento en el que la tarifa o el gravamen resulte pagadero. Los titulares de las Cuentas matrices deberán proporcionar a Disney información de la tarjeta de crédito válida, tal y como se solicita durante el proceso de registro.
""","""
Disney pasará el cobro a la tarjeta de crédito del titular de la Cuenta matriz en la fecha en la que éste se suscriba al Servicio. A partir de esa fecha, Disney efectuará, de manera automática, las siguientes acciones y procederá al cobro de la Cuenta matriz como se indica a continuación:

- Cada mes, en concepto del Servicio del mes siguiente para suscripciones mensuales.

- Cada tres (3) meses desde el primer cobro para las suscripciones trimestrales.

- Cada seis (6) meses desde el primer cobro para las suscripciones semestrales.

- Cada año (1) desde el primer cobro para las suscripciones anuales.
""","""
El cargo por renovación será equivalente o inferior al precio de suscripción, a menos que Disney indique previamente lo contrario. Podrá informar a Disney de que desea cancelar su suscripción en cualquier momento. Disney se compromete a cancelar su Cuenta a la recepción de dicha notificación de la Cuenta matriz, tal y como se describe más adelante.

En el caso de las suscripciones mensuales: Si se recibe la notificación de la cancelación durante los 15 días siguientes al cobro inicial, tendrá derecho a que le devuelvan todas las tasas de suscripción del Servicio, pero deberá pagar el resto de los gastos en los que haya incurrido. Si cancela el Servicio después de los 15 días siguientes al cobro inicial, su Cuenta será cancelada al final del período de facturación en curso y no se le devolverá ningún importe por el tiempo en que no lo haya utilizado.
""","""
En el caso de las suscripciones trimestrales: Si se recibe la notificación de la cancelación durante los 30 días siguientes al cobro inicial, tendrá derecho a que le devuelvan todas las tasas de suscripción del Servicio, pero deberá pagar el resto de los gastos en los que haya incurrido. Si cancela el Servicio después de transcurridos 30 días, no se le devolverá ningún importe por el tiempo en que no lo haya utilizado.

En el caso de las suscripciones semestrales: Si se recibe la notificación de la cancelación durante los 30 días siguientes al cobro inicial, tendrá derecho a que le devuelvan todas las tasas de suscripción del Servicio, pero deberá pagar el resto de los gastos en los que haya incurrido. Si cancela el Servicio después de los 30, no se le devolverá ninguna cantidad por el tiempo en que no lo haya utilizado.
""","""
En el caso de las suscripciones anuales: Si se recibe la notificación de la cancelación durante los 30 días siguientes al cobro inicial, tendrá derecho a que le devuelvan todas las tasas de suscripción del Servicio, pero deberá pagar el resto de los gastos en los que haya incurrido. Si cancela el Servicio después de transcurridos 30 días, no se le devolverá ningún importe por el tiempo en que no lo haya utilizado.

Su derecho a utilizar el Servicio está sujeto a los límites que establezca Disney o la entidad emisora de su tarjeta de crédito. Si no se pueden cargar o nos son devueltos los pagos cargados en su tarjeta de crédito, incluido el cargo al usuario, Disney se reserva el derecho de suspender o cancelar su acceso y Cuenta, con lo que quedan rescindidos este Contrato y todas las obligaciones de Disney.
""","""
Si alguna de sus Cuentas de Disney presenta un saldo deudor, el Socio se compromete a que Disney puede cargar estas tarifas morosas en su tarjeta de crédito. Disney se reserva el derecho a establecer un límite crediticio (en lo sucesivo, el "Límite máximo")para cada Socio. Si la Cuenta de un Socio alcanza el Límite máximo en algún momento, Disney cargará todos los pagos morosos de la cuenta en la tarjeta de crédito del Socio. A menos que se especifique lo contrario, el Límite máximo para cada Socio es de 100 dólares estadounidenses.

Si sospecha que su Cuenta no es segura (por ejemplo, en caso de pérdida, robo o divulgación no autorizada de su Nombre de socio, su Contraseña o el número de la tarjeta de crédito o de débito que aparezca en el Servicio), deberá cambiar su Contraseña inmediatamente e informar a Disney del problema (mediante notificación de la forma que se indica en la sección Notificaciones, a continuación) para evitar cualquier posible responsabilidad por cobros no autorizados que se carguen en su Cuenta.
""","""
CONSENTIMIENTO DE LOS PROGENITORES

De acuerdo con la Ley estadounidense para la protección del menor en medios electrónicos (Children's Online Privacy Protection Act, en lo sucesivo "COPPA"), se necesita el consentimiento de los progenitores para la recopilación, el uso y la divulgación de información personal correspondiente a un niño de menos de 13 años. Como parte del proceso de registro del Servicio, el titular de la Cuenta matriz deberá proporcionar una tarjeta de crédito válida. Los progenitores y representantes legales podrán crear un máximo de seis Toons (un Toon es un personaje que el socio crea y utiliza para jugar en el Servicio), todos ellos dentro de la Cuenta matriz. Los niños podrán crear su propio Toon dentro de la Cuenta matriz previo consentimiento del progenitor o el tutor inscrito como titular de la Cuenta matriz.
""","""
Al proporcionar el número de su tarjeta de crédito, el titular de la Cuenta matriz (a) pacta y acuerda ser el progenitor o representante legal de cualquier niño menor de 13 años al que permita utilizar la Cuenta matriz y (b) consiente en que recopilemos, utilicemos y divulguemos la información personal, en conformidad con las Normas de confidencialidad, respecto a cualquier niño menor de 13 años al que el titular de la Cuenta matriz permita utilizar dicha cuenta.

El Servicio incluye una función interactiva que denominados Amigos secretos. El titular de la Cuenta matriz podrá desactivar la función de Amigos secretos una vez que esté dentro del Servicio. La función de Amigos secretos permite a los socios charlar con otros socios mediante un código secreto que se debe comunicar fuera del juego. La función de Amigos secretos no tiene ningún moderador ni supervisor.
""","""
Si el titular de una Cuenta matriz permite a un niño usar su propia cuenta con la función de Amigos secretos activada, le rogamos que supervise a sus hijos mientras juegan con el Servicio. Al activar la función de Amigos secretos, el titular de la Cuenta matriz reconoce que existen riesgos inherentes a dicha función y que ha sido informado y acepta dichos riesgos. Podrá obtener más información de la función de Amigos secretos y la forma de activarla dentro del Servicio.
""","""
NOTIFICACIONES

El titular de la Cuenta matriz enviará y dispondrá de una dirección de correo electrónico correcta, así como otros datos sobre la Cuenta. Podremos realizar las notificaciones al titular de la Cuenta matriz a través de una notificación de tipo general en el Servicio, mediante correo electrónico a la dirección que consta en nuestra información de Cuenta, o mediante carta urgente enviada a la dirección postal que consta en nuestro poder. Puede enviar cualquier notificación a Disney. Dicha notificación se considerará entregada cuando Disney la reciba por correo electrónico en la dirección toontown@disneyonline.com.
""","""
NO TRANSFERIBILIDAD

Disney le otorga una licencia personal, no exclusiva y de no cesión para utilizar y poder ver el Software de Disney en cualquier dispositivo del cual usted sea el principal usuario. La copia no autorizada del Software o la reproducción de cualquier forma del software del programa principal y el software que haya sido modificado, integrado o incluido con el Software, así como la documentación relacionada con él, quedan totalmente prohibidas. Por la presente, el Socio acuerda que no puede ceder esta licencia ni el Software, ni transferirlos, venderlos o cederlos. Cualquier intento de emprender dichas acciones se considera ilegítimo.
""","""
CUESTIONES JURÍDICAS

Este Servicio está controlado y explotado por Disney desde sus oficinas en el estado de California (Estados Unidos). Disney no garantiza que el material que aparece en el Servicio sea adecuado o esté disponible en otros lugares. Las personas que decidan acceder a este Servicio desde otros lugares lo harán por iniciativa propia y serán responsables del cumplimiento de la legislación local aplicable. El Software disponible en este Servicio también está sujeto a los controles de exportación de los Estados Unidos. Está prohibido descargar, exportar o hacer llegar el Software de este Servicio a (i) Cuba, Irak, Libia, Corea del Norte, Irán, Siria (ni a un ciudadano o residente de estos países), a ningún país con el que Estados Unidos mantenga un embargo o (ii) a alguien que aparezca en la lista Specially Designated Nationals (Ciudadanos especialmente mencionados) del Ministerio de Hacienda estadounidense o en la Table of Deny Orders (tabla de denegación de pedidos) del Ministerio de Comercio.
""","""
Al descargar o utilizar el Software, el Socio pacta y conviene que no está situado bajo el control de dichos países, ni es ciudadano o residente de ellos, y asimismo, que no aparece en las listas mencionadas. Algunos tipos de Software que los Socios descargan para usarlo o instalan desde un CD-ROM es "Software restringido a ordenadores". El uso, la copia y la divulgación por parte del gobierno estadounidense están sujetos a las restricciones que se establecen en este Contrato y en las leyes federales DFARS 227.7202-1(a) y 227.7202-3(a) (1995), DFARS 252.227-7013 (Octubre de 1988), FAR 12.212(a) (1995), FAR 52.227-19, o FAR 52.227-14, según sea el caso.
""","""
EXPIRACIÓN DEL SERVICIO

Este Contrato estará en vigencia hasta que sea cancelado por una de las dos partes. Puede cancelar este Contrato y su derecho a utilizar el Servicio cuando lo desee enviando un mensaje de correo electrónico a toontown@disneyonline.com. Disney podrá cancelar su Cuenta o sus derechos de acceso a este Servicio de manera inmediata sin notificación previa si, en opinión de Disney, incumple alguna de las cláusulas de este Contrato (incluidas las Cláusulas de uso y las Normas de la casa). Una vez cancelado el contrato, deberá destruir todo el material que haya obtenido gracias a este Servicio y cualquier copia existente, independientemente de que se hiciera de acuerdo con las cláusulas de este Contrato.
""","""
VARIOS

Este Contrato se regirá e interpretará de conformidad con las leyes del estado de Carolina, sin consideración de ningún principio de conflicto de leyes. Si alguna cláusula del presente Contrato no fuese conforme a derecho, fuese nula o, por alguna razón, no resultara aplicable, dicha cláusula podrá eliminarse de este Contrato y el resto de las cláusulas conservarán su vigencia. El presente Contrato constituye la totalidad del acuerdo entre las partes acerca del objeto que se trata en él y sólo podrá ser modificado por escrito, y siempre de la forma que se describe a continuación.
""","""
CONTRATO COMPLETO

Este Contrato constituye la totalidad del contrato entre las partes respecto al objeto que en él se trata y sustituye a cualquier contrato anterior o actual que exista o haya existido, así como a cualquier propuesta o comunicado, ya sea escrito o verbal, entre los representantes de Disney y el Socio. Disney podrá modificarlo o alterarlo, así como incluir nuevas cláusulas, siempre que lo estime oportuno, previa notificación al Socio, tal y como se describe en el apartado "Notificaciones" anterior. Cualquier uso del Servicio por su parte posterior a dicha notificación constituirá una aceptación implícita de dichas modificaciones, alteraciones o nuevas cláusulas.ÚLTIMA ACTUALIZACIÓN:

LAST UPDATED:
18/10/2002
"""
]

# BillingScreen.py
BillingScreenCCTypeInitialText = 'Elija una opción'
BillingScreenCreditCardTypes = ['Visa', 'American Express', 'MasterCard']
BillingScreenTitle = "Introduzca la información de facturación"
BillingScreenAccountName = "Nombre de la cuenta"
BillingScreenEmail = "Dirección de correo electrónico de los padres para la facturación"
BillingScreenEmailConfirm = "Confirme la dirección de correo electrónico"
BillingScreenCreditCardType = "Tipo de tarjeta de crédito"
BillingScreenCreditCardNumber = "Número de la tarjeta de crédito"
BillingScreenCreditCardExpires = "Fecha de caducidad"
BillingScreenCreditCardName = "Nombre que aparece en la tarjeta de crédito"
#BillingScreenAgreementText = """*Al emplear mi tarjeta de crédito y hacer clic en "Comprar", acepto, de acuerdo con el Contrato de Socio: (1) que pueden cargar gastos en mi tarjeta de crédito y (2) que pueden recopilar, usar y difundir datos personales de mis hijos de acuerdo con las Normas de confidencialidad."""
BillingScreenAgreementText = """Al hacer clic en el botón "Comprar" acepto que, de acuerdo con las Normas de confidencialidad, mis hijos pueden usar las herramientas interactivas autorizadas mediante la contraseña parental que estableceré en la pantalla siguiente."""
BillingScreenBillingAddress = "Dirección de facturación: Calle 1"
BillingScreenBillingAddress2 = "Calle 2 (si procede)"
BillingScreenCity = "Ciudad"
BillingScreenCountry = "País"
BillingScreenState = "Estado"
BillingScreenZipCode = "Código postal"
BillingScreenCAProvince = "Provincia o territorio"
BillingScreenProvince = "Provincia (si procede)"
BillingScreenPostalCode = "Código postal"
BillingScreenPricing = ('              durante el primer mes, después'
                        '              al mes')
BillingScreenSubmit = "Comprar"
BillingScreenCancel = "Cancelar"
BillingScreenConfirmCancel = "¿Desea cancelar la compra?"
BillingScreenConfirmCancelYes = "Sí"
BillingScreenConfirmCancelNo = "No"
BillingScreenPleaseWait = "Espere un momento..."
BillingScreenConnectionErrorSuffix = ".\nVuelva a intentarlo más tarde."
BillingScreenEnterEmail = "Escriba su dirección de correo electrónico."
BillingScreenEnterEmailConfirm = "Vuelva a escribir su dirección de correo electrónico."
BillingScreenEnterValidEmail = "Introduzca una dirección de correo electrónico válida."
BillingScreenEmailMismatch = "Las direcciones de correo electrónico que ha introducido no coinciden. Inténtelo de nuevo."
BillingScreenEnterAddress = "Escriba su dirección de facturación completa."
BillingScreenEnterValidState = "Escriba la abreviatura de dos letras correspondiente al estado."
BillingScreenChooseCreditCardType = "Elija un tipo de tarjeta de crédito."
BillingScreenEnterCreditCardNumber = "Escriba el número de la tarjeta de crédito."
BillingScreenEnterValidCreditCardNumber = "Compruebe el número de la tarjeta de crédito."
BillingScreenEnterValidSpecificCreditCardNumber = "Escriba un número válido de la tarjeta de crédito %s."
BillingScreenEnterValidCreditCardExpDate = "Escriba una fecha de caducidad válida de la tarjeta de crédito."
BillingScreenEnterNameOnCard = "Escriba el nombre que aparece en la tarjeta de crédito."
BillingScreenCreditCardProblem = "Se ha producido un error al procesar la tarjeta de crédito."
BillingScreenTryAnotherCC = "¿Desea probar con otra tarjeta?"
# Fill in %s with phone number from account server
BillingScreenCustomerServiceHelp = "\n\nSi necesita ayuda, póngase en contacto con el Servicio de atención al cliente, en el teléfono %s."
BillingScreenCCProbQuit = "Salir"
BillingScreenWhySafe = "Seguridad de la tarjeta de crédito"
BillingScreenWhySafeTitle = "Seguridad de la tarjeta de crédito"
BillingScreenWhySafeCreditCardGuarantee = "GARANTÍA DE LA TARJETA DE CRÉDITO"
BillingScreenWhySafeJoin = "¡JUEGA EN"
BillingScreenWhySafeToontown = "DISNEY'S TOONTOWN ONLINE"
BillingScreenWhySafeToday = "HOY MISMO!"
BillingScreenWhySafeClose = "Cerrar"
BillingScreenWhySafeText = [
"""




Usamos la tecnología Secure Sockets Layer (SSL) para cifrar la información de la tarjeta de crédito, protegiéndola y garantizando la confidencialidad. Esta tecnología permite introducir y transmitir la información de la tarjeta de crédito por Internet con total seguridad.
Esta tecnología de seguridad protege sus comunicaciones en Internet con:

     Verificación de servidores (impide las suplantaciones)
     Confidencialidad mediante el cifrado (evita la monitorización oculta)
     Integridad de los datos (evita el vandalismo)

Para aumentar más aún la seguridad, todos los números de tarjetas de crédito se almacenan en un ordenador que no está conectado a Internet. Una vez introducido el número completo de la tarjeta de crédito, éste se transfiere a dicho ordenador seguro a través de una conexión no estándar. Los números de las tarjetas de crédito no se almacenan en ningún otro sitio.



Por tanto, la información de su tarjeta de crédito no sólo está a salvo en Disney's Toontown Online, sino que además la garantizamos.
Todas las suscripciones a Disney's Toontown Online están respaldadas por nuestra garantía de tarjetas de crédito. Si en su extracto de cuentas aparecen cargos no autorizados de los que usted no es responsable como resultado directo de haber enviado los datos de su tarjeta de crédito a Disney's Toontown Online, haremos efectiva la cantidad que le reclama su banco hasta un máximo de 50 USD.

Si sospecha que hay un problema, dé parte siguiendo el procedimiento habitual del proveedor de su tarjeta de crédito y póngase en contacto de inmediato con nosotros.  La mayoría de las compañías de tarjetas de crédito se hacen cargo de todos los gastos derivados del uso no autorizado de dichas tarjetas, pero pueden reclamarle el pago de un máximo de 50 USD. Nosotros nos hacemos cargo del pasivo que no esté cubierto por su tarjeta de crédito.
¿Qué significa todo esto? Significa que puede confiar en la seguridad y el servicio proporcionados por Disney's Toontown Online.

¿A qué espera, entonces?
""",
]
BillingScreenPrivacyPolicy = "Normas de confidencialidad"
BillingScreenPrivacyPolicyClose = "Cerrar"
BillingScreenPrivacyPolicyText = [
"""
Normas de confidencialidad

P1 ¿Qué tipo de información recogen los sitios web de WDIG y cómo lo hacen?

La mayoría de los excelentes productos y servicios que se presentan en nuestros sitios web se ofrecen sin necesidad de recabar ningún tipo de información personal de los visitantes. Puede navegar por los sitios web de WDIG y ver una gran parte de nuestro estupendo contenido de forma anónima. Por ejemplo, puede consultar los titulares de última hora en ABCNEWS.com sin por ello tener que facilitar ningún tipo de información de identificación personal.

La información que usted nos proporciona
En nuestros sitios web existen algunas actividades para las cuales resulta necesario recabar información de identificación personal. Entre ellas se incluyen, por ejemplo, la participación en concursos, las compras y los mensajes dirigidos a Disney. Cuando recabemos información de identificación personal usted será consciente de ello, ya que tendrá que rellenar un impreso. Para la mayoría de las actividades sólo se solicitan el nombre, la dirección de correo electrónico, la fecha de nacimiento, el sexo y el código postal. Cuando se efectúa una compra, también se solicitan las direcciones postales de envío y facturación, el número de teléfono y los datos de la tarjeta de crédito. Según lo que se compre, es posible que también se solicite otro tipo de información personal como, por ejemplo, la talla de ropa.
""","""
Información personal recopilada mediante dispositivos tecnológicos
Los sitios web de WDIG recaban algunos datos mediante dispositivos tecnológicos, de tal forma que puede no darse cuenta de que estamos recogiendo dicha información. Por ejemplo, cuando visita nuestro sitio web, se recoge su dirección IP para que sepamos dónde tenemos que enviar la información que está solicitando. Normalmente, la dirección IP está asociada con el lugar desde el que se ha accedido a Internet, como por ejemplo, el proveedor de Internet, la empresa o la universidad. Esta información no le identifica individualmente. Gracias a la información recabada mediante los dispositivos tecnológicos, los sitios web de WDIG resultan más interesantes y útiles para sus visitantes. Esto incluye ayudar a las empresas que se anuncian en nuestro sitio web a diseñar anuncios por los que nuestros visitantes puedan sentirse atraídos. Normalmente no combinamos esta información con los datos personales. No obstante, en caso necesario combinaremos la información de este tipo con los datos personales con el fin de identificar a los visitante para hacer cumplir las normas de la casa o las cláusulas del servicio, así como para proteger el servicio, el sitio web, a los otros visitantes, etc.

¿Qué son las cookies y cómo las utiliza WDIG?
Las cookies son pequeños fragmentos de información que los sitios web visitados envían al ordenador del visitante. Esta información permite al sitio web recordar datos importantes que harán que su uso del sitio sea más útil. WDIG y otras empresas de Internet utilizan cookies por diversos motivos. Por ejemplo, DisneyStore.com utiliza cookies para recordar y procesar los artículos del carro de la compra, y todos los sitios web de WDIG utilizan cookies para asegurarse de que los niños no entran en las salas de conversación que no estén moderadas.

Puede elegir que el ordenador le avise siempre que se envíe una cookie, o puede desactivar todas las cookies. Para ello, es necesario modificar la configuración navegador (como, por ejemplo, Netscape Navigator o Internet Explorer). Todos los navegadores son distintos; por tanto, si desea información sobre la forma de modificar las cookies, consulte el menú Ayuda del programa que utiliza. Si desactiva todas las cookies, no podrá acceder a muchas funciones de WDIG que mejoran su visita a la web sea mejor (como por ejemplo, las funciones que hemos mencionado antes), y no todos nuestros servicios funcionarán correctamente.
""","""
P2 ¿Cómo utiliza WDIG la información de identificación personal recabada?

WDIG utiliza la información de identificación personal en situaciones muy concretas. Los datos se utilizan para llevar a cabo las transacciones. Por ejemplo, si adquiere un equipo de fantasía en ESPN.com, utilizamos su información para procesar el pedido, o si se pone en contacto con nosotros para pedirnos ayuda, utilizamos esa información para ponernos en contacto con usted. Asimismo, utilizaremos la información recogida para comunicarle si ha ganado un juego o concurso. Los datos solicitados también se utilizan para enviarle por correo electrónico actualizaciones y boletines sobre nuestros sitios web, así como sobre las promociones de WDIG y las ofertas especiales de nuestros patrocinadores externos.
""","""
P3 ¿Comparte WDIG en algún caso la información con empresas u otro tipo de organizaciones que no forman parte de su grupo de sitios web?

Nuestros clientes son los activos más importantes de nuestro negocio. No nos dedicamos a vender la información de nuestros visitantes. Sin embargo, cuando esto suponga una ventaja para nuestros visitantes, compartiremos la información que tenemos sobre usted o le enviaremos mensajes de parte de otra empresa, como describimos más adelante. También podemos compartir la información por motivos de seguridad.
Las empresas subyacentes al WDIG
En ocasiones contratamos a otras empresas para la entrega de productos o servicios, como por ejemplo una empresa de envíos que entrega un paquete. En esas ocasiones, nos vemos obligados a compartir la información con ellos. Estas empresas prácticamente son representantes de WDIG, y sólo pueden utilizar la información para entregar el producto o el servicio.
""","""
Empresas que ofrecen promociones, productos o servicios
De vez en cuando, lanzamos promociones, como concursos o suscripciones gratuitas, en colaboración con un patrocinador. Compartiremos la información con los patrocinadores si la necesitan para enviarle un producto, como puede ser la suscripción a una revista. Asimismo, podemos compartir la información con dichos patrocinadores para que puedan ofrecerle sus promociones especiales, pero sólo si usted así lo permite y, en ese caso, la compartiremos sólo con ese patrocinador en concreto.  Además, WDIG puede enviar por correo electrónico a los visitantes promociones de parte de otros patrocinadores. En estos casos, no compartimos su nombre con dichos patrocinadores; lo que hacemos es enviarle los mensajes en su nombre. Únicamente le enviaremos estas promociones si nos ha autorizado para ello.

Colaboradores de contenido
En algunos de nuestros sitios web ofrecemos contenido creado por un sitio web de un colaborador externo. Por ejemplo, ESPN.com ofrece oportunidades de compra en empresas de terceros. En algunos casos, los sitos web de terceros solicitan información con el fin de realizar la transacción o para que el uso de su contenido resulte más productivo y eficaz. En estos casos, la información que se recoge se comparte entre WDIG y los patrocinadores externos.

Anunciadores externos y anunciadores de la red
Con el fin de aumentar la protección de la intimidad de nuestros visitantes, WDIG sólo permite anunciarse en nuestros sitios web a empresas que tienen sus propias normas de confidencialidad. Cuando se hace clic en un anuncio y se abandonan los sitios web de WDIG, nuestras normas de confidencialidad dejan de ser aplicables. Debe leer las normas de confidencialidad de la empresa anunciada para saber cómo se tratará su información personal en su sitio web.
""","""
Además, en nuestro sitio web existen muchos anuncios comerciales gestionados y publicados por empresas externas. Estas empresas reciben el nombre de "anunciadores de la red". Los anunciadores de la red recogen información de carácter no personal cuando se hace clic en sus báners, y en ocasiones, cuando se pasa por encima con el ratón. La información se obtiene por medio de dispositivos tecnológicos, por lo que es posible que no se dé cuenta de que está siendo recogida. Los anunciadores de la red recogen esta información para mostrarle después anuncios que pueden resultarle más interesantes. Si desea obtener más información sobre los anunciadores de la red o no desea que recojan este tipo de información de carácter no personal sobre usted, haga clic aquí.

Compra y venta de negocios
Los negocios en línea se encuentran todavía en una etapa muy temprana, pero están cambiando y evolucionando con mucha rapidez. Como WDIG busca continuamente formas de mejorar nuestro negocio, se puede dar el caso de que compremos o vendamos una empresa. Si compramos o vendemos un negocio, es probable que los nombres recogidos se transfieran como parte de la venta. La información sobre las personas registradas se utilizará en la sociedad constituida. Sin embargo, si compramos un negocio, satisfaremos los deseos de sus clientes en lo que se refiere a comunicaciones por correo electrónico. En caso de que vendamos un negocio, haremos todo lo que esté a nuestro alcance para garantizar que se cumplan las peticiones de comunicaciones por correo electrónico que nos confió.

Organizaciones que ayudan a proteger y salvaguardar la seguridad de nuestros visitantes y nuestros sitios web
Divulgaremos la información personal cuando la legislación así lo requiera, por ejemplo, en cumplimiento de un requerimiento judicial o una cédula de citación; para hacer cumplir nuestras Cláusulas de servicio o las normas del sitio web o de los juegos; o para proteger y salvaguardar la seguridad de los visitantes y de nuestros sitios web.
""","""
P4 ¿Qué opciones tiene el cliente en lo relativo a la información recogida, utilizada y compartida por WDIG?

Puede utilizar gran parte de nuestro sitio web sin darnos ningún tipo de información de identificación personal. Cuando se registre con nosotros o nos proporcione información de identificación personal, tendrá la oportunidad de restringir las comunicaciones por correo electrónico de WDIG y de nuestros colaboradores externos. Puede solicitar en cualquier momento que WDIG deje de enviarle más mensajes de correo electrónico, bien cancelando su suscripción a dicha comunicación, bien poniéndose en contacto con nosotros en la dirección memeberservices@help.go.com. Asimismo, como hemos mencionado anteriormente, existen formas de restringir la información que se recoge a través de nuestros dispositivos tecnológicos, aunque, en ese caso, algunas de nuestras funciones no se podrán utilizar.
""","""
P5 ¿Qué tipo de seguridad ofrece WDIG?

La importancia de la seguridad de toda la información de identificación personal de nuestros visitantes supone nuestra mayor preocupación. WDIG adopta medidas técnicas, contractuales, administrativas y físicas relacionadas con la seguridad, con el fin de proteger los datos de todos los visitantes. Cuando los visitantes proporcionan información relativa a su tarjeta de crédito, nos valemos del cifrado SSL para protegerla. Los visitantes también pueden realizar varias acciones para ayudarnos a proteger la seguridad de su información. Por ejemplo, no divulgue nunca su contraseña, ya que con ella se puede acceder a toda la información de su cuenta. No se olvide tampoco de cerrar la sesión de su cuenta y la ventana del navegador cuando acabe de navegar por la red, de manera que si otra persona utiliza el mismo ordenador no pueda acceder a su información.
""","""
P6 ¿Cómo puedo acceder a la información de mi cuenta?

Puede acceder a la información de identificación personal que nos facilitó durante el proceso de registro en el Centro de opciones de cuentas, disponible en http://play.toontown.com.  Inicie una sesión con su nombre de cuenta y la contraseña principal. En la página de inicio encontrará instrucciones para poder recuperar su contraseña en caso de que la olvide.
Si desea ponerse en contacto con nosotros, haga clic en el enlace "Contact Us" (Contacto) que aparece al pie de todas las páginas de WDIG y seleccione "Registration/Personalization" (Registro/Personalización) en el menú desplegable, o bien envíenos un mensaje de correo electrónico con información que nos ayude a identificar su cuenta con el fin de que podamos ayudarle a resolver el problema.
""","""
P7 ¿Con quién hay que ponerse contacto si surge alguna pregunta o duda sobre estas normas de confidencialidad?

Si necesita más ayuda, le rogamos que nos envíe un mensaje de correo electrónico con sus preguntas y comentarios a memberservices@help.go.com.
También puede escribirnos por correo ordinario a:

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104, Estados Unidos

Walt Disney Internet Group es licenciatario del TRUSTe Privacy Program. Si considera que WDIG no ha contestado a su pregunta o no la ha enfocado de la forma deseada, le rogamos que se ponga en contacto con el programa TRUSTe en http://www.truste.org/users/users_watchdog.html.
*Para llamar a este teléfono es necesario tener 18 años de edad o contar con el permiso de los padres o el tutor.
""","""
Normas de confidencialidad para niños
Somos conscientes de la necesidad de ofrecer servicios adicionales de protección de los datos personales de los niños que visitan nuestros sitios web.

P1 ¿Qué tipo de información recogen los sitios web de WDIG sobre los niños que tienen 12 años o menos?

Los niños pueden navegar por Disney.com u otros sitios web de WDIG, ver distintos contenidos y jugar a algunos juegos sin que se recoja ningún tipo de información de identificación personal. Además, esporádicamente alojamos salas de conversación moderadas en las que no se solicita ni se hace pública información de identificación personal de ningún tipo. No obstante, en algunas zonas es necesario recoger información de identificación personal de los niños para permitir la participación en ciertas actividades (como, por ejemplo, un concurso) o para comunicarse con nuestra comunidad (por correo electrónico o tablones de mensajes).
En WDIG no consideramos adecuado recoger más información de identificación personal de niños de 12 años o menores que la necesaria para que puedan participar en nuestras actividades en línea. Además, se debe tener en cuenta que los sitios web que están dirigidos a niños de 12 años y menores no pueden, por ley, solicitar más información de la necesaria.

La única información de identificación personal que recogemos de los niños es el nombre, la fecha de nacimiento y la dirección de correo electrónico de los padres. La fecha de nacimiento se recoge para comprobar la edad de los visitantes. También podemos solicitar información personal, como por ejemplo el nombre de un animal doméstico, para recordar a los visitantes su nombre de inicio de sesión y su ""","""
contraseña en caso de que los olviden.

También permitimos a los padres solicitar, cuando lo estimen oportuno, la supresión de nuestra base de datos de toda la información que figura sobre sus hijos. Si desea desactivar la cuenta de su hijo, le rogamos que nos lo solicite por medio de un mensaje dirigido a ms_support@help.go.com en el que consten el nombre de inicio de sesión y la contraseña del niño.
""","""
P2 ¿Cómo utiliza y comparte WDIG la información de identificación personal que recabada?

Ningún dato sobre los visitantes de 12 años o menores se utiliza con ningún fin de marketing ni promocional, ni dentro ni fuera de la familia de sitios web del Walt Disney Internet Group.
Los sitios web de WDIG sólo utilizan los datos recogidos sobre los niños de 12 años o menores para ofrecer servicios (como por ejemplo calendarios) o para llevar a cabo algunos juegos o concursos. A pesar de que los visitantes de 12 años y menores pueden participar en algunos concursos en los que se recoge información, las notificaciones y los premios se envían a la dirección de correo electrónico de los padres o tutores que se proporcionó durante el proceso de registro inicial. No se publican el nombre completo, la edad ni las fotos de los ganadores de los concursos para niños de 12 años o menores sin el consentimiento de los padres o el tutor. En ocasiones se publica una forma inidentificable del nombre del niño. En esos casos, es posible que no nos volvamos a poner en contacto con los padres para pedirles permiso.

No permitimos a los niños de 12 años y menores participar en salas de conversación sin moderador.

Facilitaremos la información personal sobre los niños cuando la legislación así lo requiera, por ejemplo, en cumplimiento de un requerimiento judicial o cédula de citación; para hacer cumplir nuestras Cláusulas de servicio, o las normas del sitio web o de los juegos; o para proteger y salvaguardar la seguridad de los visitantes y de nuestros sitios web.
""","""
P3 ¿Se ocupa WDIG de informar a los padres sobre la recogida de información de niños de 12 años o menores?

Siempre que un niño de 12 años o menor se registre en nuestro servicio, se lo notificaremos por correo electrónico a sus padres o a su tutor. Además, solicitamos a los padres que otorguen un permiso explícito para permitir a sus hijos utilizar el correo electrónico, los tableros de mensajes y otras funciones a través de las cuales se puede hacer pública la información de identificación personal en Internet y compartirla con usuarios de todas las edades.
También damos a los padres un plazo de 48 horas para rechazar cualquier registro que sus hijos hayan efectuado para jugar a juegos y concursos. Si no recibimos ningún mensaje en contra, damos por supuesto que no hay ningún problema en que el niño esté registrado en el servicio. Cuando el niño se haya registrado, podrá acceder a cualquier juego y concurso que requiera inscripción, pero no se lo volveremos a notificar a sus padres. En este caso, utilizamos la información recogida únicamente para comunicar a los padres si un niño ha ganado un juego o concurso. No utilizamos esta información con ningún otro fin.
""","""
P4 ¿Cómo pueden acceder los padres a la información de sus hijos?

Existen tres formas de revisar la información que se ha recogido sobre los niños de 12 años o menores.

Cuando los padres proporcionan a sus hijos el acceso a funciones interactivas, como los tableros de mensajes, se les solicita que configuren una cuenta familiar. Cuando la cuenta familiar se encuentre en funcionamiento, el titular de la cuenta principal podrá revisar la información de identificación personal de todas las cuentas de los socios de la familia, incluidas las de los niños. Para acceder a esta información, inicie una sesión en su cuenta familiar en la página de inicio Your Account (Su cuenta).

Si todavía no es socio de un sitio web de WDIG, para revisar la información de identificación personal de su hijo inicie una sesión de su cuenta en la página de inicio Account Options (Opciones de cuenta). Deberá tener el nombre de cuenta y la contraseña de su hijo. En la página de inicio Your Account (Su cuenta) encontrará instrucciones para poder recuperar la contraseña de su hijo en caso de que la olvide.

También puede ponerse en contacto con el Servicio de atención al cliente para ver la información que se ha recogido de su hijo mediante un mensaje dirigido a ms_support@help.go.com. Si todavía no ha establecido una cuenta familiar, deberá tener el nombre de usuario y la contraseña de su hijo. Le rogamos que incluya en el mensaje de correo electrónico datos (nombre de cuenta del niño, dirección de correo electrónico de los padres) que nos permitan identificar la cuenta de su hijo, con el fin de que podamos ayudarle a resolver el problema.
""","""
P5 ¿Qué tipo de seguridad ofrece WDIG?

La importancia de la seguridad de toda la información de identificación personal de nuestros visitantes supone nuestra mayor preocupación. WDIG adopta medidas técnicas, contractuales, administrativas y físicas relacionadas con la seguridad, con el fin de proteger los datos de todos los visitantes. Cuando los visitantes proporcionan información relativa a su tarjeta de crédito, nos valemos del cifrado SSL para protegerla. Los visitantes también pueden realizar varias acciones para ayudarnos a proteger la seguridad de su información. Por ejemplo, no divulgue nunca su contraseña, ya que con ella se puede acceder a toda la información de su cuenta. No se olvide tampoco de cerrar la sesión de su cuenta y la ventana del navegador cuando acabe de navegar por la red, de manera que si otra persona utiliza el mismo ordenador no pueda acceder a su información.
""","""
P6 ¿Cómo se enteran los padres si WDIG modifica estas normas de confidencialidad?

Si WDIG modifica estas normas de confidencialidad, se lo notificaremos a los padres por correo electrónico.

P7 ¿ Con quién hay que ponerse contacto si surge alguna pregunta o duda sobre estas normas de confidencialidad?

Si necesita más ayuda, le rogamos que envíe un mensaje de correo electrónico con sus preguntas o comentarios a ms_support@help.go.com.
También puede escribirnos por correo ordinario a:

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104, Estados Unidos
O llamarnos por teléfono al número 00 (1) (509) 742-4698.

Walt Disney Internet Group es licenciatario del TRUSTe Privacy Program. Si considera que WDIG no ha contestado a su pregunta o no la ha enfocado de la forma deseada, le rogamos que se ponga en contacto con el programa TRUSTe en http://www.truste.org/users/users_watchdog.html.
*Para llamar a este teléfono es necesario tener 18 años de edad o contar con el permiso de los padres o el tutor.
""",
]
BillingScreenCountryNames = {
    "US" : "Estados Unidos de América",
    "CA" : "Canadá",
    "AF" : "Afganistán",
    "AL" : "Albania",
    "DZ" : "Argelia",
    "AS" : "Samoa estadounidense",
    "AD" : "Andorra",
    "AO" : "Angola",
    "AI" : "Anguilla",
    "AQ" : "Antártida",
    "AG" : "Antigua y Barbuda",
    "AR" : "Argentina",
    "AM" : "Armenia",
    "AW" : "Aruba",
    "AU" : "Australia",
    "AT" : "Austria",
    "AZ" : "Azerbaiyán",
    "BS" : "Bahamas",
    "BH" : "Bahréin",
    "BD" : "Bangladesh",
    "BB" : "Barbados",
    "BY" : "Bielorrusia",
    "BE" : "Bélgica",
    "BZ" : "Belice",
    "BJ" : "Benín",
    "BM" : "Bermudas",
    "BT" : "Bután",
    "BO" : "Bolivia",
    "BA" : "Bosnia y Herzegovina",
    "BW" : "Botsuana",
    "BV" : "Isla de Bouvet",
    "BR" : "Brasil",
    "IO" : "Territorio oceánico de las Indias Británicas",
    "BN" : "Brunéi Darussalam",
    "BG" : "Bulgaria",
    "BF" : "Burkina Faso",
    "BI" : "Burundi",
    "KH" : "Camboya",
    "CM" : "Camerún",
    "CV" : "Cabo Verde",
    "KY" : "Islas Caimán",
    "CF" : "República Centroafricana",
    "TD" : "Chad",
    "CL" : "Chile",
    "CN" : "China",
    "CX" : "Isla de Navidad",
    "CC" : "Islas Cocos",
    "CO" : "Colombia",
    "KM" : "Comoras",
    "CG" : "Congo",
    "CK" : "Islas Cook ",
    "CR" : "Costa Rica",
    "CI" : "Costa de Marfil",
    "HR" : "Croacia",
    "CU" : "Cuba",
    "CY" : "Chipre",
    "CZ" : "República Checa",
    "CS" : "Checoslovaquia (anteriormente)",
    "DK" : "Dinamarca",
    "DJ" : "Yibuti",
    "DM" : "Dominica",
    "DO" : "República Dominicana",
    "TP" : "Timor Oriental",
    "EC" : "Ecuador",
    "EG" : "Egipto",
    "SV" : "El Salvador",
    "GQ" : "Guinea Ecuatorial",
    "ER" : "Eritrea",
    "EE" : "Estonia",
    "ET" : "Etiopía",
    "FK" : "Islas Malvinas",
    "FO" : "Islas Feroe",
    "FJ" : "Fiyi",
    "FI" : "Finlandia",
    "FR" : "Francia",
    "FX" : "Francia (Europa)",
    "GF" : "Guyana Francesa",
    "PF" : "Polinesia Francesa",
    "TF" : "Territorios franceses de los Mares del Sur",
    "GA" : "Gabón",
    "GM" : "Gambia",
    "GE" : "Georgia",
    "DE" : "Alemania",
    "GH" : "Ghana",
    "GI" : "Gibraltar",
    "GB" : "Reino Unido",
    "GR" : "Grecia",
    "GL" : "Groenlandia",
    "GD" : "Isla de Granada",
    "GP" : "Guadalupe",
    "GU" : "Guam",
    "GT" : "Guatemala",
    "GN" : "Guinea",
    "GW" : "Guinea-Bissau",
    "GY" : "Guyana",
    "HT" : "Haití",
    "HM" : "Islas Heard y McDonald",
    "HN" : "Honduras",
    "HK" : "Hong Kong",
    "HU" : "Hungría",
    "IS" : "Islandia",
    "IN" : "India",
    "ID" : "Indonesia",
    "IR" : "Irán",
    "IQ" : "Irak",
    "IE" : "Irlanda",
    "IL" : "Israel",
    "IT" : "Italia",
    "JM" : "Jamaica",
    "JP" : "Japón",
    "JO" : "Jordania",
    "KZ" : "Kazajstán",
    "KE" : "Kenia",
    "KI" : "Kiribati",
    "KP" : "Corea del Norte",
    "KR" : "Corea del Sur",
    "KW" : "Kuwait",
    "KG" : "Kirguistán",
    "LA" : "Laos",
    "LV" : "Letonia",
    "LB" : "Líbano",
    "LS" : "Lesoto",
    "LR" : "Liberia",
    "LY" : "Libia",
    "LI" : "Liechtenstein",
    "LT" : "Lituania",
    "LU" : "Luxemburgo",
    "MO" : "Macao",
    "MK" : "Macedonia",
    "MG" : "Madagascar",
    "MW" : "Malawi",
    "MY" : "Malasia",
    "MV" : "Maldivas",
    "ML" : "Malí",
    "MT" : "Malta",
    "MH" : "Islas Marshall",
    "MQ" : "Martinica",
    "MR" : "Mauritania",
    "MU" : "Mauricio",
    "YT" : "Mayotte",
    "MX" : "México",
    "FM" : "Micronesia",
    "MD" : "Moldavia",
    "MC" : "Mónaco",
    "MN" : "Mongolia",
    "MS" : "Montserrat",
    "MA" : "Marruecos",
    "MZ" : "Mozambique",
    "MM" : "Myanmar",
    "NA" : "Namibia",
    "NR" : "Nauru",
    "NP" : "Nepal",
    "NL" : "Países Bajos",
    "AN" : "Antillas Holandesas",
    "NT" : "Zona neutral",
    "NC" : "Nueva Caledonia",
    "NZ" : "Nueva Zelanda",
    "NI" : "Nicaragua",
    "NE" : "Níger",
    "NG" : "Nigeria",
    "NU" : "Niue",
    "NF" : "Isla Norfolk",
    "MP" : "Islas Marianas Septentrionales",
    "NO" : "Noruega",
    "OM" : "Omán",
    "PK" : "Pakistán",
    "PW" : "Paláu",
    "PA" : "Panamá",
    "PG" : "Papua Nueva Guinea",
    "PY" : "Paraguay",
    "PE" : "Perú",
    "PH" : "Filipinas",
    "PN" : "Pitcairn",
    "PL" : "Polonia",
    "PT" : "Portugal",
    "PR" : "Puerto Rico",
    "QA" : "Qatar",
    "RE" : "Reunión",
    "RO" : "Rumanía",
    "RU" : "Federación Rusa",
    "RW" : "Ruanda",
    "GS" : "Islas Meridionales de Georgia y Sandwich",
    "KN" : "Saint Kitts y Nevis",
    "LC" : "Santa Lucía",
    "VC" : "San Vicente y las Granadinas",
    "WS" : "Samoa",
    "SM" : "San Marino",
    "ST" : "Santo Tomé y Príncipe",
    "SA" : "Arabia Saudí ",
    "SN" : "Senegal",
    "SC" : "Seychelles",
    "SL" : "Sierra Leona",
    "SG" : "Singapur",
    "SK" : "República Eslovaca",
    "SI" : "Eslovenia",
    "Sb" : "Islas Salomón",
    "SO" : "Somalia",
    "ZA" : "República Sudafricana",
    "ES" : "España",
    "LK" : "Sri Lanka",
    "SH" : "Santa Elena",
    "PM" : "St. Pierre y Miquelon",
    "SD" : "Sudán",
    "SR" : "Surinam",
    "SJ" : "Islas Svalbard y Jan Mayen",
    "SZ" : "Suazilandia",
    "SE" : "Suecia",
    "CH" : "Suiza",
    "SY" : "Siria",
    "TW" : "Taiwán",
    "TJ" : "Tayikistán",
    "TZ" : "Tanzania",
    "TH" : "Tailandia",
    "TG" : "Togo",
    "TK" : "Tokelau",
    "TO" : "Tonga",
    "TT" : "Trinidad y Tobago",
    "TN" : "Túnez",
    "TR" : "Turquía",
    "TM" : "Turkmenistán",
    "TC" : "Islas Turks y Caicos",
    "TV" : "Tuvalu",
    "UG" : "Uganda",
    "UA" : "Ucrania",
    "AE" : "Emiratos Árabes Unidos",
    "UK" : "Reino Unido",
    "UY" : "Uruguay",
    "UM" : "Islas adyacentes a los EE.UU.",
    "SU" : "URSS (anteriormente)",
    "UZ" : "Uzbekistán",
    "VU" : "Vanuatu",
    "VA" : "Ciudad del Vaticano",
    "VE" : "Venezuela",
    "VN" : "Vietnam",
    "VG" : "Islas Vírgenes Británicas",
    "VI" : "Islas Vírgenes Estadounidenses",
    "WF" : "Islas Wallis y Futuna",
    "EH" : "Sahara Occideental",
    "YE" : "Yemen",
    "YU" : "Yugoslavia",
    "ZR" : "Zaire",
    "ZM" : "Zambia",
    "ZW" : "Zimbabue",
    }
BillingScreenStateNames = {
    "AL" : "Alabama",
    "AK" : "Alaska",
    "AR" : "Arkansas",
    "AZ" : "Arizona",
    "CA" : "California",
    "CO" : "Colorado",
    "CT" : "Connecticut",
    "DE" : "Delaware",
    "FL" : "Florida",
    "GA" : "Georgia",
    "HI" : "Hawai",
    "IA" : "Iowa",
    "ID" : "Idaho",
    "IL" : "Illinois",
    "IN" : "Indiana",
    "KS" : "Kansas",
    "KY" : "Kentucky",
    "LA" : "Lousiana",
    "MA" : "Massachusetts",
    "MD" : "Maryland",
    "ME" : "Maine",
    "MI" : "Míchigan",
    "MN" : "Minnesota",
    "MO" : "Missouri",
    "MS" : "Misisipi",
    "MT" : "Montana",
    "NE" : "Nebraska",
    "NC" : "Carolina del Norte",
    "ND" : "Dakota del Norte ",
    "NH" : "Nuevo Hampshire",
    "NJ" : "Nueva Jersey",
    "NM" : "Nuevo México",
    "NV" : "Nevada",
    "NY" : "Nueva York",
    "OH" : "Ohio",
    "OK" : "Oklahoma",
    "OR" : "Oregón",
    "PA" : "Pensilvania",
    "RI" : "Rhode Island",
    "SC" : "Carolina del Sur ",
    "SD" : "Dakota del Sur ",
    "TN" : "Tennessee",
    "TX" : "Texas",
    "UT" : "Utah",
    "VA" : "Virginia",
    "VT" : "Vermont",
    "WA" : "Washington",
    "WI" : "Wisconsin",
    "WV" : "Virginia Occidental",
    "WY" : "Wyoming",
    "DC" : "Distrito de Columbia",
    "AS" : "Samoa estadounidense",
    "GU" : "Guam",
    "MP" : "Islas Marianas Septentrionales",
    "PR" : "Puerto Rico",
    "VI" : "Islas Vírgenes Estadounidenses",
    "FPO" : ["Isla de Midway",
             "Arrecife Kingman",
             ],
    "APO" : ["Isla Wake",
             "Isla Johnston",
             ],
    "MH" : "Islas Marshall",
    "PW" : "Paláu",
    "FM" : "Micronesia",
    }
BillingScreenCanadianProvinces = {
    'AB' : 'Alberta',
    'BC' : 'Columbia Británica',
    'MB' : 'Manitoba',
    'NB' : 'Nueva Brunswick',
    'NF' : 'Newfoundland',
    'NT' : 'Territorios del Noroeste',
    'NS' : 'Nueva Escocia',
    #'XX' : 'Nunavut',
    'ON' : 'Ontario',
    'PE' : 'Isla Prince Edward',
    'QC' : 'Québec',
    'SK' : 'Saskatchewan',
    'YT' : 'Yukon',
    }

ParentPassword = "Contraseña parental"

# WelcomeScreen.py
WelcomeScreenHeading = "¡Bienvenido!"
WelcomeScreenOk = "¡VAMOS A JUGAR!"
WelcomeScreenSentence1 = "Ahora eres socio oficial de"
WelcomeScreenToontown = "Disney's Toontown Online"
WelcomeScreenSentence2 = "No te olvides de buscar más adelante en el correo electrónico las sorprendentes noticias sobre Disney's Toontown Online."

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Para ponerte en contacto con el Servicio de atención al cliente, llama al %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\n\nSi necesitas ayuda, ponte en contacto con el Servicio de atención al cliente, en el número %s."
TTAccountIntractibleError = "Se ha producido un error."

# LoginScreen.py
LoginScreenUserName = "Nombre de la cuenta"
LoginScreenPassword = "Contraseña"
LoginScreenLogin = "Inicio de sesión"
LoginScreenCreateAccount = "Crear cuenta"
LoginScreenForgotPassword = "¿Has olvidado la contraseña?"
LoginScreenQuit = "Salir"
LoginScreenLoginPrompt = "Introduce un nombre de usuario y una contraseña."
LoginScreenBadPassword = "Contraseña incorrecta.\nInténtalo de nuevo."
LoginScreenInvalidUserName = "Nombre de usuario incorrecto.\nInténtalo de nuevo."
LoginScreenUserNameNotFound = "No se ha encontrado el nombre de usuario.\nInténtalo de nuevo o crea otra cuenta."
LoginScreenPeriodTimeExpired = "Lo sentimos, pero ya has gastado todos los minutos de que disponías en Toontown este mes.  Vuelve a principios del mes que viene."
LoginScreenNoNewAccounts = "Lo sentimos mucho, pero no aceptamos nuevas cuentas en este momento."
LoginScreenTryAgain = "Inténtalo de nuevo"

# NewPlayerScreen.py
NewPlayerScreenNewAccount = "Empezar prueba gratuita"
NewPlayerScreenLogin = "Socio Activo"
NewPlayerScreenQuit = "Salir"

# FreeTimeInformScreen.py
FreeTimeInformScreenDontForget = "No te olvides de que tu prueba gratuita\ncaducará en "
FreeTimeInformScreenNDaysLeft = FreeTimeInformScreenDontForget + "¡sólo %s días!"
FreeTimeInformScreenOneDayLeft = FreeTimeInformScreenDontForget + "¡un día!"
FreeTimeInformScreenNHoursLeft = FreeTimeInformScreenDontForget + "¡sólo %s horas!"
FreeTimeInformScreenOneHourLeft = FreeTimeInformScreenDontForget + "¡una hora!"
FreeTimeInformScreenLessThanOneHourLeft = FreeTimeInformScreenDontForget + "¡menos de una hora!"
FreeTimeInformScreenSecondSentence = "Pero todavía tienes tiempo para hacerte\nsocio oficial de Disney's Toontown Online."
FreeTimeInformScreenOops = "¡VAYA!"
FreeTimeInformScreenExpired = "                 , tu prueba gratuita ha caducado.\n¿Deseas convertirte en socio oficial de Disney's Toontown Online?\n¡Inscríbete ahora y diviértete como nunca!"
FreeTimeInformScreenExpiredQuitText = "¿No puedes hacerlo ahora mismo? No te preocupes, te guardaremos\nel dibu. Pero ¡date prisa! Sólo podemos\nguardarte el dibu durante una semana después\nde que haya caducado tu prueba gratuita."
FreeTimeInformScreenExpiredCCUF = "Todavía no has adquirido Disney's\nToontown Online. Para usar esta cuenta\ndebes registrarte ahora con una tarjeta de crédito.\n¡Inscríbete ahora y vuelve a divertirte como nunca!"
FreeTimeInformScreenExpiredQuitCCUFText = "¿No puedes hacerlo ahora mismo? No te preocupes, te guardaremos\nla cuenta. Pero ¡date prisa! Sólo podemos\nguardarte la cuenta durante una semana."
FreeTimeInformScreenPurchase = "¡Suscríbete ya!"
FreeTimeInformScreenFreePlay = "Continuar prueba gratuita"
FreeTimeInformScreenQuit = "Salir"

# DateOfBirthEntry.py
DateOfBirthEntryMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',]
DateOfBirthEntryDefaultLabel = "Fecha de nacimiento"

# CreateAccountScreen.py
CreateAccountScreenUserName = "Nombre de la cuenta"
CreateAccountScreenPassword = "Contraseña"
CreateAccountScreenConfirmPassword = "Confirmar contraseña"
CreateAccountScreenFree = "GRATIS"
CreateAccountScreenFreeTrialLength = 'Para empezar tu prueba de           %s días\ntienes que crear una cuenta.'
CreateAccountScreenInstructionsUsername = "Escribe el nombre de la cuenta que deseas usar:"
CreateAccountScreenInstructionsPassword = "Escribe una contraseña:"
CreateAccountScreenInstructionsConfirmPassword = "Para asegurarte, escribe de nuevo la contraseña:"
CreateAccountScreenInstructionsDob = "Escribe tu fecha de nacimiento:"
CreateAccountScreenCancel = "Cancelar"
CreateAccountScreenSubmit = "Siguiente"
CreateAccountScreenConnectionErrorSuffix = ".\n\nVuelve a intentarlo más tarde."
CreateAccountScreenNoAccountName = "Escribe un nombre de cuenta."
CreateAccountScreenAccountNameTooShort = "El nombre de cuenta debe tener al menos %s caracteres. Inténtalo de nuevo."
CreateAccountScreenPasswordTooShort = "La contraseña debe tener al menos %s caracteres. Inténtalo de nuevo."
CreateAccountScreenPasswordMismatch = "Las contraseñas que has escrito no coinciden. Inténtalo de nuevo."
CreateAccountScreenInvalidDob = "Escribe tu fecha de nacimiento."
CreateAccountScreenUserNameTaken = "Ese nombre de usuario ya existe. Inténtalo de nuevo."
CreateAccountScreenInvalidUserName = "Nombre de usuario no válido.\nInténtalo de nuevo."
CreateAccountScreenUserNameNotFound = "No se ha encontrado el nombre de usuario.\nInténtalo de nuevo o crea otra cuenta."
CreateAccountScreenEmailInstructions = "Escribe tu dirección de correo electrónico.\n¿Por qué? Por dos razones:\n1. Si olvidas la contraseña, te la podremos enviar.\n2. Podemos enviarte la información más reciente\nsobre Disney's Toontown Online."
CreateAccountScreenEmailInstructionsUnder13 = "Has indicado que tienes menos de 13 años.\nPara crear una cuenta necesitamos la dirección de correo electrónico de tus padres o tu tutor."
CreateAccountScreenEmailConfirm = "Para asegurarte, escribe de nuevo la dirección de correo electrónico."
CreateAccountScreenEmailPanelSubmit = "Siguiente"
CreateAccountScreenEmailPanelCancel = "Cancelar"
CreateAccountScreenInvalidEmail = "Escribe la dirección de correo electrónico completa."
CreateAccountScreenEmailMismatch = "Las direcciones de correo electrónico que has introducido no coinciden. Inténtalo de nuevo."

# SecretFriendsInfoPanel.py
SecretFriendsInfoPanelOk = "Aceptar"
SecretFriendsInfoPanelText = ["""
La herramienta Amigos secretos

La herramienta Amigos secretos permite a los socios conversar directamente entre sí mediante en Disney's Toontown Online (en lo sucesivo, el "Servicio"). Para ello, los socios deben establecer una conexión de Amigos secretos.  Cuando su hijo intente usar la herramienta Amigos secretos, le pediremos que introduzca su contraseña parental para confirmar su consentimiento al uso de dicha herramienta.  A continuación se describe con detalle proceso de creación de una conexión de Amigos secretos entre dos socios imaginarios a los que llamaremos "Susana" y "Miguel".
1. Los padres de Susana y los de Miguel activan la herramienta Amigos secretos, introduciendo sus contraseñas parentales (a) en las Opciones de cuenta del Servicio o (b) cuando el juego se lo requiera en una ventana emergente de Control parental.
2. Susana solicita un Secreto (descrito más adelante) desde dentro del Servicio.
""","""
3. El Secreto de Susana se envía a Miguel fuera del Servicio. (Susana le puede comunicar su Secreto a Miguel directamente o indirectamente, a través de otra persona.)
4. Miguel envía el Secreto de Susana al Servicio en un plazo de 48 horas a partir del momento en que Susana lo ha solicitado.
5. El Servicio comunica a Miguel que Susana se ha convertido en su amiga secreta.  De igual modo, el Servicio notifica a Susana que Miguel se ha convertido en su amigo secreto.
6. Ahora, Susana y Miguel pueden charlar entre sí hasta que uno de ellos decida que el otro deje de ser su amigo secreto o hasta que los padres de Susana o Miguel desactiven la herramienta Amigos secretos.  Por tanto, la conexión Amigos secretos puede ser desactivada en cualquier momento por:
""","""
(a) Un socio que borre a otro de su lista de amigos secretos (de la forma
descrita en el Servicio) o (b) los padres de un socio que desactiven la herramienta Amigos secretos por medio de las Opciones de cuenta del Servicio (siguiendo los pasos allí establecidos).

Un Secreto es un código informático generado al azar y asignado a un socio en concreto. Es necesario usar el Secreto para activar la conexión de Amigos secretos dentro de un plazo de 48 horas a partir del momento de su solicitud. De lo contrario, el Secreto caduca y no se puede utilizar.  Además, un secreto sólo se puede usar para establecer una sola conexión de Amigos Secretos.  Para crear más conexiones de Amigos secretos, el socio debe solicitar un Secreto adicional para cada uno de los nuevos amigos.

Las amistades secretas no se transfieren.  Por ejemplo, si Susana es amiga
""","""
secreta de Miguel y Miguel es amigo secreto de Ana, Susana no se convierte automáticamente en amiga secreta de Ana.  Para que Susana y Ana se hagan
amigas secretas, una de ellas deberá solicitar un nuevo Secreto al Servicio y
comunicárselo a la otra.

Los amigos secretos se comunican entre sí mediante un servicio de conversación interactivo de formato libre.  El contenido de esta conversación es escrito directamente por el socio participante y procesado a través del Servicio, que está gestionado por Walt Disney Internet Group ("WDIG"), 506 2nd Avenue, Suite 2100, Seattle, WA 98104, EE.UU. (teléfono +1 (509) 742-4698; correo electrónico: ms_support@help.go.com).  Aunque aconsejamos a los socios que no intercambien datos personales, como sus nombres y apellidos, direcciones de correo electrónico, direcciones postales o números de teléfono mientras utilizan la herramienta Amigos secretos, no
""","""
podemos garantizar que tales intercambios de información personal no se produzcan. Aunque el servicio de conversación de Amigos secretos tiene un filtro automático de palabras malsonantes y obscenas, no está moderado ni  supervisado por nosotros.  Si los padres permiten a sus hijos usar su cuenta con la opción Amigos secretos activada, les aconsejamos que los supervisen mientras juegan en el Servicio..

WDIG no hace uso del contenido de las conversaciones de Amigos secretos para ningún otro propósito que no sea el de comunicar dicho contenido al amigo secreto del socio, y no divulga ese contenido a terceros excepto en los siguientes casos: (1) Si la ley lo requiere, por ejemplo, para acatar una orden o citación judicial; (2) para hacer cumplir las Condiciones de uso aplicables al Servicio (a las que se puede acceder en la página principal del Servicio); (3) para proteger la seguridad de los socios del Servicio y del Servicio mismo.
""","""
Los padres de un niño pueden, previa petición a WDIG, revisar y borrar el contenido de cualquier conversación mantenida por ese niño, suponiendo que dicho contenido no haya sido ya borrado por WDIG de sus archivos.  Según lo estipulado en la Ley estadounidense para la protección del menor en medios electrónicos (Children's Online Privacy Protection Act), no estamos autorizados a condicionar la participación de un niño en ninguna actividad (lo que incluye Amigos secretos) en base a la revelación por parte del niño de más información personal de la razonablemente necesaria para participar en tal actividad.

Además, tal y como se menciona anteriormente, reconocemos el derecho de los padres a negarse a permitir que el niño siga utilizando la herramienta Amigos secretos. Al activar la herramienta Amigos secretos, los padres reconocen que existen ciertos riesgos inherentes a la posibilidad de charlar de los socios por medio de dicha herramienta, y reconocen que han sido informados sobre dichos riesgos y están de acuerdo en aceptarlos.
"""
]

# ParentPasswordScreen.py
ParentPasswordScreenTitle = "Controles parentales"
ParentPasswordScreenPassword = "Crear contraseña parental"
ParentPasswordScreenConfirmPassword = "Confirmar contraseña parental"
ParentPasswordScreenSubmit = "Establecer contraseña parental"
ParentPasswordScreenConnectionErrorSuffix = ".\nVuelva a intentarlo más tarde."
ParentPasswordScreenPasswordTooShort = "La contraseña debe tener al menos %s caracteres. Inténtelo de nuevo."
ParentPasswordScreenPasswordMismatch = "Las contraseñas que ha escrito no coinciden. Inténtelo de nuevo."
ParentPasswordScreenConnectionProblemJustPaid = "Ha surgido un problema con la conexión con el servidor de la cuenta, pero la adquisición se ha procesado.\n\nLa próxima vez que inicie una sesión se le solicitará que establezca la contraseña parental."
ParentPasswordScreenConnectionProblemJustLoggedIn = "Ha surgido un problema en la conexión con el servidor de la cuenta. Vuelva a intentarlo más tarde."
ParentPasswordScreenSecretFriendsMoreInfo = "Más información"
ParentPasswordScreenInstructions = """Cree una contraseña parental para esta cuenta.  La contraseña parental se le solicitará más adelante:

  1.  Cuando le pidamos consentimiento para que tu hijo
       use ciertas herramientas interactivas de Toontown
       tales como la herramienta "Amigos secretos".  Si desea
       una descripción completa de la herramienta Amigos
       secretos, que permite que sus hijos se
       comuniquen en línea con otros socios de Toontown,
       pulse el botón """+ParentPasswordScreenSecretFriendsMoreInfo+"""', situado debajo. Es necesario que dé su consentimiento
       para activar esta herramienta.


  2. Para actualizar la información sobre la facturación
       y la cuenta desde la página web de Toontown.
"""
ParentPasswordScreenAdvice = "Recuerde que la contraseña parental debe ser confidencial. Mantenerla a salvo es fundamental para conservar el control sobre el uso de las herramientas interactivas de la cuenta por parte de su hijo. "
ParentPasswordScreenPrivacyPolicy = "Normas de confidencialidad"


# ForgotPasswordScreen.py
ForgotPasswordScreenTitle = "Si ha olvidado la contraseña, se la podemos enviar."
ForgotPasswordScreenInstructions = "Introduzca el nombre de su cuenta o la dirección de correo electrónico que nos facilitó."
ForgotPasswordScreenEmailEntryLabel = "Dirección de correo electrónico"
ForgotPasswordScreenOr = "O bien"
ForgotPasswordScreenAcctNameEntryLabel = "Nombre de la cuenta"
ForgotPasswordScreenSubmit = "Enviar"
ForgotPasswordScreenCancel = "Cancelar"
ForgotPasswordScreenEmailSuccess = "Su contraseña ha sido enviada a '%s'."
ForgotPasswordScreenEmailFailure = "Dirección de correo electrónico no encontrada: '%s'."
ForgotPasswordScreenAccountNameSuccess = "Su contraseña ha sido enviada a la dirección de correo electrónico que nos facilitó al crear la cuenta."
ForgotPasswordScreenAccountNameFailure = "Cuenta no encontrada: %s"
ForgotPasswordScreenNoEmailAddress = "Esa cuenta ha sido creada por un menor de 13 años y no tiene una dirección de correo electrónico. No podemos enviarle la contraseña.\n\n¡Cree otra cuenta si lo desea!"
ForgotPasswordScreenInvalidEmail = "Introduzca una dirección de correo electrónico válida."

# GuiScreen.py
GuiScreenToontownUnavailable = "Toontown no parece estar disponible por el momento, seguimos intentándolo..."
GuiScreenCancel = "Cancelar"

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
InventoryPagePluralPoints = "Conseguirás una nueva\nbroma de %(trackName)s cuando\nconsigas %(numPoints)s puntos más de %(trackName)s."
InventoryPageSinglePoint = "Conseguirás una nueva\nbroma de %(trackName)s cuando\nconsigas %(numPoints)s punto más de %(trackName)s."
InventoryPageNoAccess = "Todavía no tienes acceso al circuito %s."

# NPCFriendPage.py
NPCFriendPageTitle = "SOS dibus"

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
OptionsPageFriendsEnabledLabel = "Se aceptan solicitudes de nuevos amigos."
OptionsPageFriendsDisabledLabel = "No se aceptan solicitudes de nuevos amigos."
OptionsPageSpeedChatStyleLabel = "Color para la Charla rápida"
OptionsPageDisplayWindowed = "en ventana"
OptionsPageSelect = "Escoger"
OptionsPageToggleOn = "Activar"
OptionsPageToggleOff = "Desactivar"
OptionsPageChange = "Cambiar"
OptionsPageDisplaySettings = "Pantalla: %(screensize)s, %(api)s"
OptionsPageDisplaySettingsNoApi = "Pantalla: %(screensize)s"
OptionsPageExitConfirm = "¿Quieres salir de Toontown?"

DisplaySettingsTitle = "Configuración de la pantalla"
DisplaySettingsIntro = "Los siguientes parámetros sirven para configurar el aspecto de Toontown en tu ordenador.  Lo más probable es que no haga falta modificarlos a no ser que surja algún problema."
DisplaySettingsIntroSimple = "Usted puede ajustar la resolucion de su pantalla a un valor más alto, para mejorar la claridad gráfica y de texto, pero todo depende de la tarjeta gráfica, un valor más alto puede hacer el juego menos fluido o que no trabaje del todo"

DisplaySettingsApi = "Interfaz gráfica:"
DisplaySettingsResolution = "Resolución:"
DisplaySettingsWindowed = "En ventana"
DisplaySettingsFullscreen = "Pantalla completa"
DisplaySettingsApply = "Aplicar"
DisplaySettingsCancel = "Cancelar"
DisplaySettingsApplyWarning = "Cuando pulses Aceptar cambiará la configuración gráfica.  Si la nueva configuración no se representa correctamente en tu ordenador, la pantalla volverá automáticamente a la configuración original transcurridos %s segundos."
DisplaySettingsAccept = "Pulsa Aceptar para conservar la nueva configuración, o Cancelar para volver a la anterior.  Si no pulsas nada, se volverá a la configuración anterior al cabo de %s segundos."
DisplaySettingsRevertUser = "Se ha restablecido la configuración anterior de la pantalla. "
DisplaySettingsRevertFailed = "La configuración de pantalla seleccionada no funciona en tu ordenador.  Se ha restablecido la configuración anterior de la pantalla. "


# TrackPage.py
TrackPageTitle = "Circuito Entrenador de Bromas"
TrackPageShortTitle = "Entrenador de Bromas"
TrackPageSubtitle = "¡Completa las dibutareas para aprender a usar las bromas nuevas!"
TrackPageTraining = "Estás entrenándote para usar las bromas de %s.\nCuando completes las 16 tareas,\npodrás usar las bromas de %s en los combates."
TrackPageClear = "Ahora mismo no te estás entrenando en ningún circuito de bromas."
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
QuestPageChoose = "Elige"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = "Funcionario del cuartel general"
QuestPosterHQBuildingName = "Cuartel General Dibu"
QuestPosterHQStreetName = "Cualquier calle"
QuestPosterHQLocationName = "Cualquier barrio"

QuestPosterTailor = "Sastre"
QuestPosterTailorBuildingName = "Tienda de Ropa"
QuestPosterTailorStreetName = "Cualquier Dibuparque"
QuestPosterTailorLocationName = "Cualquier barrio"
QuestPosterPlayground = "En el Dibuparque"
QuestPosterAtHome = "At your home"
QuestPosterInHome = "In your home"
QuestPosterOnPhone = "On your phone"
QuestPosterEstate = "At your estate"
QuestPosterAnywhere = "Cualquier parte"
QuestPosterAuxTo = "hacia:"
QuestPosterAuxFrom = "de:"
QuestPosterAuxFor = "para:"
QuestPosterAuxOr = "o:"
QuestPosterAuxReturnTo = "Vuelve a:"
QuestPosterLocationIn = " en "
QuestPosterLocationOn = " en "
QuestPosterFun = "¡Para Divertirse!"
QuestPosterFishing = "Anda a pescar"
QuestPosterComplete = "COMPLETADA"

# ShardPage.py
ShardPageTitle = "Distritos"
ShardPageHelpIntro = "Cada distrito es una copia del mundo de Toontown."
ShardPageHelpWhere = "Ahora tú estás en el distrito \"%s\"."
ShardPageHelpWelcomeValley = "Ahora tú estás en el distrito \"Valle Bienvenido\", dentro de \"%s\"."
ShardPageHelpMove = "Para desplazarte a otro distrito, haz clic en su nombre."

ShardPagePopulationTotal = "N.º total de habitantes de Toontown:\n%d"
ShardPageScrollTitle = "Nombre            Habitantes"

# SuitPage.py
SuitPageTitle = "Galería de bots"
SuitPageMystery = DialogQuestion + DialogQuestion + DialogQuestion
SuitPageQuota = "%s de %s"
SuitPageCogRadar = "%s presente"
SuitPageBuildingRadarS = "%s edificio"
SuitPageBuildingRadarP = "%s edificios"

# DisguisePage.py
DisguisePageTitle = "Disfraces de" + Cog
DisguisePageMeritAlert = "¡Listo para un ascenso!"
DisguisePageCogLevel = "Nivel %s"
DisguisePageMeritFull = "Lleno"
DisguisePageMeritBar = "Merit Progress"
DisguisePageCogPartRatio = "%d / %d"

# FishPage.py
FishPageTitle = "Pecera"
FishPageTitleTank = "Cubo para los peces"
FishPageTitleCollection = "Álbum de peces"
FishPageTitleTrophy = "Trofeos de pesca"
FishPageWeightStr = "Peso: "
FishPageWeightLargeS = "%d kg. "
FishPageWeightLargeP = "%d kg. "
FishPageWeightSmallS = "%d gr."
FishPageWeightSmallP = "%d gr."
FishPageWeightConversion = 16
FishPageValueS = "Valor: %d gominola"
FishPageValueP = "Valor: %d gominolas"
FishPageTotalValue = ""
FishPageCollectedTotal = "Especies de peces recogidas: %d de %d"
FishPageRodInfo = "%s Caña de\n%d - %d kilos"
FishPageTankTab = "Cubo"
FishPageCollectionTab = "Álbum"
FishPageTrophyTab = "Trofeos"

FishPickerTotalValue = "Cubo: %s / %s\nValor: %d gominolas"

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
    }

# QuestChoiceGui.py
QuestChoiceGuiCancel = "Cancelar"

# TrackChoiceGui.py
TrackChoiceGuiChoose = "Elige"
TrackChoiceGuiCancel = "Cancelar"
TrackChoiceGuiHEAL = 'Curadibu te permite sanar a otros dibus durante el combate.'
TrackChoiceGuiTRAP = 'Las trampas son potentes bromas que se deben usar con cebos.'
TrackChoiceGuiLURE = 'los cebos permiten aturdir a los bots y atraerlos a las trampas.'
TrackChoiceGuiSOUND = 'Las bromas de sonido afectan a todos los bots, pero no son muy potentes.'
TrackChoiceGuiDROP = "Las bromas de caída causan un montón de daños, pero no son muy precisas."

# EmotePage.py
EmotePageTitle = "Expresiones / Emociones"
EmotePageDance = "Has creado la siguiente secuencia de baile:"
EmoteJump = "Saltar"
EmoteDance = "Bailar"
EmoteHappy = "Feliz"
EmoteSad = "Triste"
EmoteAnnoyed = "Fastidiado"
EmoteSleep = "Soñoliento"

# Emote.py
# List of emotes in the order they should appear in the SpeedChat.
# Must be in the same order as the function list (EmoteFunc) in Emote.py
EmoteList = [
    "Saludar",
    "Contento",
    "Triste",
    "Enfadado",
    "Soñoliento",
    "Encoger hombros",
    "Bailar",
    "Guiñar ojo",
    "Aburrido",
    "Aplaudir",
    "Sorprendido",
    "Confundido",
    "Mofarse",
    "Inclinarse",
    "Muy triste",
    "Hola",
    "Adiós",
    "Sí",
    "No",
    "Vale",
    ]

EmoteWhispers = [
    "%s Saluda.",
    "%s esta contento.",
    "%s esta triste.",
    "%s esta enfadado.",
    "%s esta soñoliento.",
    "%s se encoge de hombros.",
    "%s baila.",
    "%s guiña un ojo.",
    "%s esta aburrido.",
    "%s aplaude.",
    "%s esta sorprendido.",
    "%s esta confundido.",
    "%s se mofa de tí.",
    "%s te hace una reverencia.",
    "%s esta muy triste.",
    "%s dice 'Hola'.",
    "%s dice 'Adiós'.",
    "%s dice 'Sí'.",
    "%s dice 'No'.",
    "%s dice 'Vale'.",
    ]

# Reverse lookup:  get the index from the name.
EmoteFuncDict = {
  "saludar"   : 0,
  "contento"  : 1,
  "triste"    : 2,
  "enfadado"  : 3,
  "soñoliento" : 4,
  "reír"     : 5,
  "bailar"    : 6,
  "guiñar ojo": 7,
  "aburrido"  : 8,
  "aplaudir"  : 9,
  "sorprendido" : 10,
  "confundido" : 11,
  "mofarse"   : 12,
  "inclinarse" : 13,
  "muy triste" : 14,
  "hola"      : 15,
  "adiós"    : 16,
  "sí"       : 17,
  "no"        : 18,
  "vale"      : 19,
  }

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nNivel %(level)s"

# SuitDialog.py
SuitBrushOffs = {
    'f':  ["Llego tarde a una reunión",
           ],
    'p':  ["Lárgate",
           ],
    'ym': ['Al sonriente no le hace gracia',
           ],
    None: ["Es mi día libre",
           "Creo que te has equivocado de despacho",
           "Que tu secretaria llame a la mía",
           "No tengo tiempo para reunirme contigo",
           "Habla con mi ayudante"]
    }

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "¡No puedes irte del dibuparque hasta que tu risómetro esté sonriendo!"

# InventoryNew.py
InventoryTotalGags = "Bromas totales\n%d / %d"
InventoryDelete = "BORRAR"
InventoryDone = "HECHO"
InventoryDeleteHelp = "Haz clic en una broma para BORRARLA."
InventorySkillCredit = "Habilidad: %s"
InventorySkillCreditNone = "Habilidad: Ninguna"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "Precisión: %(accuracy)s\n%(damageString)s: %(damage)d\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryAffectsOneCog = "Afecta a: Un " + Cog
InventoryAffectsOneToon = "Afecta a: Un dibu"
InventoryAffectsAllToons = "Afecta a: Todos los dibus"
InventoryAffectsAllCogs = "Afecta a: Todos los " + Cogs
InventoryHealString = "Curadibu"
InventoryDamageString = "Daños"
InventoryBattleMenu = "MENÚ DE COMBATE"
InventoryRun = "CORRER"
InventorySOS = "S.O.S."
InventoryPass = "PASAR"
InventoryClickToAttack = "Haz clic en \nuna broma \npara atacar"

# NPCForceAcknowledge.py
#NPCForceAcknowledgeMessage = "Visit " + Flippy + " to get your first ToonTask before leaving.\n\n\n\nYou can find\n" + Flippy + " inside\nToonHall."
NPCForceAcknowledgeMessage = "Antes de marcharte debes subirte en el tranvia.\n\n\n\n\n\nEl tranvia esta al lado de la tienda de bromas de Goofy."
NPCForceAcknowledgeMessage2 = "!Enhorabuena por completar tu tarea del tranvia!\nVe al cuartel general dibu para recibir tu recompensa.\n\n\n\n\n\n\nEl cuartel general dibu esta cerca del centro del dibuparque."
NPCForceAcknowledgeMessage3 = "Recuerda que tienes que subirte en el tranvia.\n\n\n\n\n\nEl tranvia esta al lado de la tienda de bromas de Goofy."
NPCForceAcknowledgeMessage4 = "!Enhorabuena!  !Has completado la primera dibutarea!\n\n\n\n\n\nVe al cuartel general dibu para recibir tu recompensa."
NPCForceAcknowledgeMessage6 = "Great job defeating those Cogs!\n\n\n\n\n\n\n\n\nHead back to Toon Headquarters as soon as possible."
NPCForceAcknowledgeMessage7 = "Don't forget to make a friend!\n\n\n\n\n\n\nClick on another player and use the New Friend button."
NPCForceAcknowledgeMessage8 = "Great! You made a new friend!\n\n\n\n\n\n\n\n\nYou should go back at Toon Headquarters now."
NPCForceAcknowledgeMessage9 = "Good job using the phone!\n\n\n\n\n\n\n\n\nReturn to Toon Headquarters to claim your reward."

# Toon.py
ToonSleepString = ". . . ZZZ . . ."

# Movie.py
MovieTutorialReward1 = "¡Has recibido 1 punto de lanzamiento! ¡Cuando hayas recibido 10, recibiras una broma nueva!"
MovieTutorialReward2 = "¡Has recibido 1 punto de chorro! Cuando hayas recibido 10, recibiras una broma nueva!"
MovieTutorialReward3 = "¡Buen trabajo! ¡Has completado tu primera Dibutarea!"
MovieTutorialReward4 = "¡Anda al Cuartel General para recibir tu premio!"
MovieTutorialReward5 = "¡Que te entretengas!"

# ToontownBattleGlobals.py
BattleGlobalTracks = ['curadibu', 'trampa', 'cebo', 'sonido', 'lanzamiento', 'chorro', 'caída']
BattleGlobalNPCTracks = ['reaprovisionamiento', 'dibus aciertan', 'bots fallan']
BattleGlobalAvPropStrings = (
    ('Pluma', 'Megáfono', 'Pintalabios', 'Caña de bambú', 'Polvo de hadas', 'Bolas de malabarista'),
    ('Cascara de Plátano', 'Rastrillo', 'Canicas', 'Arena movediza', 'Trampilla', 'TNT'),
    ('Billete de 10 euros', 'Imán pequeño', 'Billete de 20 euros', 'Imán grande', 'Billete de 50 euros', 'Gafas hipnóticas'),
    ('Bocina de bicicleta', 'Silbato', 'Corneta', 'Sirena', 'Trompa de elefante', 'Sirena de niebla'),
    ('Magdalena', 'Trozo de tarta de frutas', 'Trozo de tarta de nata', 'Tarta de frutas entera', 'Tarta de nata entera', 'Tarta de cumpleaños'),
    ('Flor chorreante', 'Vaso de agua', 'Pistola de agua', 'Botella de soda', 'Manguera', 'Nube tormentosa'),
    ('Maceta', 'Saco de arena', 'Yunque', 'Pesa grande', 'Caja fuerte', 'Piano de cola')
    )
BattleGlobalAvPropStringsSingular = (
    ('una Pluma', 'un Megáfono', 'un Pintalabios', 'una Caña de bambú', 'un Polvo de hadas', 'unas Bolas de malabarista'),
    ('una Cascara de Plátano', 'un Rastrillo', 'unas Canicas', 'una Arena movediza', 'una Trampilla', 'un TNT'),
    ('un Billete de 10 euros', 'un Imán pequeño', 'un Billete de 20 euros', 'un Imán grande', 'un Billete de 50 euros', 'unas Gafas hipnóticas'),
    ('una Bocina de bicicleta', 'un Silbato', 'una Corneta', 'una Sirena', 'una Trompa de elefante', 'una Sirena de niebla'),
    ('una Magdalena', 'un Trozo de tarta de frutas', 'un Trozo de tarta de nata', 'una Tarta de frutas entera', 'una Tarta de nata entera', 'una Tarta de cumpleaños'),
    ('una Flor chorreante', 'un Vaso de agua', 'una Pistola de agua', 'una Botella de soda', 'una Manguera', 'una Nube tormentosa'),
    ('una Maceta', 'un Saco de arena', 'un Yunque', 'una Pesa grande', 'una Caja fuerte', 'un Piano de cola')
    )
BattleGlobalAvPropStringsPlural = (
    ('Plumas', 'Megáfonos', 'Pintalabios', 'Cañas de bambú', 'Polvos de hadas', 'Bolas de malabarista'),
    ('Cascaras de Plátano', 'Rastrillos', 'Canicas', 'Arenas movedizas', 'Trampillas','TNT'),
    ('Billetes de 10 euros', 'Imanes pequeños', 'Billetes de 20 euros', 'Imanes grandes','Billetes de 50 euros', 'Gafas hipnóticas'),
    ('Bocinas de bicicleta', 'Silbatos', 'Cornetas', 'Sirenas', 'Trompas de elefante', 'Sirenas de niebla'),
    ('Magdalenas', 'Trozos de tarta de frutas', 'Trozos de tarta de nata','Tartas de frutas enteras', 'Tartas de nata enteras', 'Tartas de cumpleaños'),
    ('Flores chorreantes', 'Vasos de agua', 'Pistolas de agua','Botellas de soda', 'Mangueras', 'Nubes tormentosas'),
    ('Macetas', 'Sacos de arena', 'Yunques', 'Pesas grandes', 'Cajas fuertes','Pianos de cola')
    )
BattleGlobalAvTrackAccStrings = ("Media", "Perfecta", "Baja", "Alta", "Media", "Alta", "Baja")

AttackMissed = "Erraste"

NPCCallButtonLabel = 'LLAMAR'

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
    4000  : ("al",   "", "Dibuparque"),
    4100  : ("a la", "", "Travesía de la Melodía"),
    4200  : ("al",   "", "Bulevar del Barítono"),
    4300  : ("a la", "", "Calle del Tenor"),
    5000  : ("al",   "", "Dibuparque"),
    5100  : ("a la", "", "Calle del Chopo"),
    5200  : ("a la", "", "Calle Arce"),
    5300  : ("a la", "", "Calle de Los Robles"),         # translate
    9000  : ("al",   "", "Dibuparque"),
    9100  : ("a la", "", "Avenida de la Nana"),
    10000 : ("al",   "", "cuartel general jefebot"),
    10100 : ("al",   "", "vestíbulo del cuartel general jefebot"),
    11000 : ("al",   "", "patio del cuartel general vendebot"),
    11100 : ("al",   "", "vestíbulo del cuartel general vendebot"),
    11200 : ("a la", "", "fábrica vendebot"),
    11500 : ("a la", "", "fábrica vendebot"),
    12000 : ("al",   "", "cuartel general chequebot"),
    12100 : ("al",   "", "vestíbulo del cuartel general chequebot"),
    13000 : ("al",   "", "cuartel general abogabot"),
    13100 : ("al",   "", "vestíbulo del cuartel general abogabot"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("a",    "", "Puerto Donald")
ToontownCentral   = ("al",   "", "Centro de Toontown")
TheBrrrgh         = ("a",    "", "Frescolandia")
MinniesMelodyland = ("a",    "", "Melodilandia de Minnie")
DaisyGardens      = ("a",    "", "los Jardines de Daisy")
ConstructionZone  = ("a la", "", "Zona de obras")
FunnyFarm         = ("a la", "", "Granja Jolgorio")
GoofyStadium      = ("al",   "", "Estadio Goofy")
DonaldsDreamland  = ("a",    "", "Sueñolandia de Donald")
BossbotHQ         = ("al",   "", "Cuartel general jefebot")
SellbotHQ         = ("al",   "", "Cuartel general vendebot")
CashbotHQ         = ("al",   "", "Cuartel general chequebot")
LawbotHQ          = ("al",   "", "Cuartel general abogabot")
Tutorial          = ("al",   "", "Dibututorial")
MyEstate          = ("a",    "", "Tu casa")
WelcomeValley     = ("a",    "", "Valle Bienvenido")

Factory = 'Fábrica'
Headquarters = 'Cuartel general'
SellbotFrontEntrance = 'Entrada principal'
SellbotSideEntrance = 'Entrada de servicio'

FactoryNames = {
    0 : 'Maqueta de la fábrica',
    11500 : 'Fábrica de bots vendebot',
    }

FactoryTypeLeg = 'Pierna'
FactoryTypeArm = 'Brazo'
FactoryTypeTorso = 'Torso'

# ToontownLoader.py
LoaderLabel = "Cargando..."

# PlayGame.py
HeadingToHood = "Entrando %(to)s %(hood)s..." # to phrase, hood name
HeadingToYourEstate = "Entrando a tú propiedad..."
HeadingToEstate = "Entrando a la propiedad %s..."  # avatar name
HeadingToFriend = "Entrando a la propiedad del amigo %s..."  # avatar name

# Hood.py
HeadingToPlayground = "Entrando al Dibuparque..."
HeadingToStreet = "Entrando %(to)s %(street)s..." # to phrase, street name

# ToontownDialog.py
ToontownDialogOK = "Aceptar"
ToontownDialogCancel = "Cancelar"
ToontownDialogYes = "Sí"
ToontownDialogNo = "No"

# TownBattle.py
TownBattleRun = "¿Quieres volver corriendo al dibuparque?"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "¿QUÉ DIBU?"
TownBattleChooseAvatarCogTitle = "¿CUÁL " + string.upper(Cog) + "?"
TownBattleChooseAvatarBack = "ATRÁS"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "¡No tienes amigos a los que llamar!"
TownBattleSOSWhichFriend = "¿A qué amigo quieres llamar?"
TownBattleSOSNPCFriends = "Dibus rescatados"
TownBattleSOSBack = "ATRÁS"

# TownBattleToonPanel.py
TownBattleToonSOS = "S.O.S."
TownBattleUndecided = "?"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "Esperando a\notros jugadores..."
TownSoloBattleWaitTitle = "Espera..."
TownBattleWaitBack = "ATRÁS"

# Trolley.py
TrolleyHFAMessage = "No puedes subirte al tranvía hasta que el risómetro esté sonriendo."
TrolleyTFAMessage = "No puedes subirte al tranvía hasta que lo diga Mickey."
TrolleyHopOff = "Bajarse"

# DistributedFishingSpot.py
FishingExit = "Hecho"
FishingCast = "Lanzar"
FishingAutoReel = "Carrete automático"
FishingItemFound = "Has pescado:"
FishingCrankTooSlow = "Muy\nlento"
FishingCrankTooFast = "Muy\nrápido"
FishingFailure = "¡No has pescado nada!"
FishingFailureTooSoon = "No empieces a enrollar el carrete hasta que veas que pican.  ¡Espera a que la boya se mueva hacia arriba y abajo rápidamente!"
FishingFailureTooLate = "¡Es importante que enrolles el sedal mientras el pez está mordiendo el anzuelo!"
FishingFailureAutoReel = "El carrete automático no ha funcionado esta vez.  Enrolla a mano el carrete a la velocidad correcta para poder pescar algo."
FishingFailureTooSlow = "Has enrollado el carrete demasiado despacio.  Algunos peces son más rápidos que otros.  ¡Intenta mantener centrada la barra de velocidad!"
FishingFailureTooFast = "Has enrollado el carrete demasiado deprisa.  Algunos peces son más lentos que otros.  ¡Intenta mantener centrada la barra de velocidad!"
FishingOverTankLimit = "El cubo de peces está lleno. Vende unos cuantos peces y vuelve."
FishingBroke = "¡No tienes nada que poner en el anzuelo!  Súbete al tranvía para conseguir más gominolas."
FishingHowToFirstTime = "Pulsa el botón Lanzar y arrastra hacia abajo. Cuanto más lejos arrastres, más fuerte será el lanzamiento. Ajusta el ángulo para acertar en los peces.\n\n¡Pruébalo ya!"
FishingHowToFailed = "Pulsa el botón para Lanzar y arrastra hacia abajo. Cuanto más lejos arrastres, más fuerte será el lanzamiento. Ajusta el ángulo para acertar en los peces.\n\n¡Prueba de nuevo!"
FishingBootItem = "Una bota vieja"
FishingJellybeanItem = "%s gominolas"
FishingNewEntry = "¡Una nueva especie!"
FishingNewRecord = "¡Nuevo récord!"

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
TutorialChat3 = "¡Ten cuidado!  Muchos de los jugadores no entenderán lo que dices si usas el teclado."
TutorialChat4 = "El botón verde abre el %s."
TutorialChat5 = "Todos entienden lo que dices cuando usas el %s."
TutorialChat6 = "Prueba a decir \"Hola\"."
TutorialBodyClick1 = "¡Muy bien!"
TutorialBodyClick2 = "¡Encantado de conocerte! ¿Quieres ser mi amigo?"
TutorialBodyClick3 = "Para ser amigo de %s, haz clic en él..." % Flippy
TutorialHandleBodyClickSuccess = "¡Buen trabajo!"
TutorialHandleBodyClickFail = "Todavía no. Prueba a hacer clic en %s..." % Flippy
TutorialFriendsButton = "Ahora pulsa el botón \"Amigos\", situado debajo de la imagen de %s, en la esquina derecha." % Flippy
TutorialHandleFriendsButton = "Después, pulsa el botón \"Sí\"."
TutorialOK = "Aceptar"
TutorialYes = "Sí"
TutorialNo = "No"
TutorialFriendsPrompt = "¿Quieres ser amigo de %s?" % Flippy
TutorialFriendsPanelMickeyChat = "%s ha accedido a ser tu amigo. Pulsa \"Aceptar\" para terminar." % Flippy
TutorialFriendsPanelYes = "¡%s ha dicho que sí!" % Flippy
TutorialFriendsPanelNo = "¡No es que seas muy amable!"
TutorialFriendsPanelCongrats = "¡Enhorabuena! Acabas de hacer tu primer amigo."
TutorialFlippyChat1 = "Ven a verme cuando estés preparado para tu primera dibutarea."
TutorialFlippyChat2 = "Estaré en el Ayuntamiento."
TutorialAllFriendsButton = "Para ver a todos tus amigos, haz clic en el botón Amigos. Pruébalo..."
TutorialEmptyFriendsList = "Ahora mismo la lista está vacía porque %s no es un jugador de verdad." % Flippy
TutorialCloseFriendsList = "Pulsa el botón\nCerrar para que la\nlista se cierre."
TutorialShtickerButton = "El botón de la esquina inferior derecha sirve para abrir el dibucuaderno.  Prúebalo..."
TutorialBook1 = "El dibucuaderno contiene un montón de información útil, como este mapa de Toontown."
TutorialBook2 = "También puedes ver cómo van tus dibutareas."
TutorialBook3 = "Cuando hayas terminado, vuelve a pulsar el botón del libro para que se cierre."
TutorialLaffMeter1 = "También vas a necesitar esto..."
TutorialLaffMeter2 = "También vas a necesitar esto...\nEs tu risómetro."
TutorialLaffMeter3 = "Cuando los bots te ataquen, irá disminuyendo."
TutorialLaffMeter4 = "Cuando estés en dibuparques como éste, subirá de nuevo."
TutorialLaffMeter5 = "Cuando completes dibutareas obtendrás recompensas, como por ejemplo un aumento del límite del risómetro."
TutorialLaffMeter6 = "¡Ten cuidado! Si los bots te vencen, perderás todas las bromas."
TutorialLaffMeter7 = "Para conseguir más bromas, juega a los juegos del tranvía."
TutorialTrolley1 = "¡Sígueme hasta el tranvía!"
TutorialTrolley2 = "¡Súbete!"
TutorialBye1 = "¡Juega a unos cuantos juegos!"
TutorialBye2 = "¡Juega a unos cuantos juegos!\n¡Compra unas cuantas bromas!"
TutorialBye3 = "Cuando hayas terminado, ve a ver a %s" % Flippy

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "¡Vas en dirección contraria! ¡Ve a buscar a %s!" % Mickey

# SpeedChat

# Used several places in the game. Defined globally because
# we keep changing the name
GlobalSpeedChatName = "Charla rápida"

SCMenuEmotions  = "EMOCIONES"
SCMenuCustom    = "MIS FRASES"
SCMenuCog       = "COG SPEAK"
SCMenuHello     = "HOLA"
SCMenuBye       = "ADIÓS"
SCMenuHappy     = "FELIZ"
SCMenuSad       = "TRISTE"
SCMenuFriendly  = "AMIGABLE"
SCMenuSorry     = "LO SIENTO"
SCMenuStinky    = "FÉTIDO"
SCMenuPlaces    = "LUGARES"
SCMenuToontasks = "DIBUTAREAS"
SCMenuBattle    = "COMBATE"
SCMenuGagShop   = "BROMAS"
SCMenuFactory   = "FABRICA"
SCMenuFactoryMeet = "ENCUENTRO"
SCMenuFriendlyYou = "Eres..."
SCMenuFriendlyILike = "me gusta..."
SCMenuPlacesLetsGo  = "Vamos a..."
SCMenuToontasksMyTasks = "Mis tareas"
SCMenuToontasksYouShouldChoose = "Creo que deberias escoger..."
SCMenuBattleLetsUse = "Vamos a usar..."

# These are all the standard SpeedChat phrases.
# The indices must fit into 16 bits (0..65535)
SpeedChatStaticText = {
    # top-level
    1 : 'Sí',
    2 : 'No',
    3 : 'Aceptar',

    # Hello
    100 : "¡Buenas!",
    101 : "¡Hola!",
    102 : "¡Muy Buenas!",
    103 : "¡Eh!",
    104 : "¿Qué hay?",
    105 : "¡Hola a todos!",
    106 : "¡Bienvenido a Toontown!",
    107 : "¿Qué tal?",
    108 : "¿Cómo estás?",
    109 : "¿Hola?",

    # Bye
    200 : "¡Chao!",
    201 : "¡Nos vemos!",
    202 : "¡Hasta la vista!",
    203 : "¡Que pases un buen día!",
    204 : "¡Diviértete!",
    205 : "¡Buena suerte!",
    206 : "Vuelvo enseguida.",
    207 : "Tengo que irme.",

    # Happy
    300 : ":-)",
    301 : "¡Hey!",
    302 : "¡Hurra!",
    303 : "¡chupi!",
    304 : "¡Yujuuu!",
    305 : "¡Sí!",
    306 : "¡Ja, ja!",
    307 : "¡Ji, ji!",
    308 : "¡Guau!",
    309 : "¡Fantástico!",
    310 : "¡Yepaa!",
    311 : "¡Estupendo!",
    312 : "¡Yupii!",
    313 : "¡Yipee!",
    314 : "¡Yiii ja!",
    315 : "¡Dibufantástico!",

    # Sad
    400 : ":-(",
    401 : "¡Oh no!",
    402 : "¡Oh oh!",
    403 : "¡Caramba!",
    404 : "¡Vaya!",
    405 : "¡Ay!",
    406 : "¡Uf!",
    407 : "¡¡¡No!!!",
    408 : "¡Auuu!",
    409 : "¿Eh?",
    410 : "Necesito más puntos de risa.",

    # Friendly
    500 : "¡Gracias!",
    501 : "No hay de qué.",
    502 : "¡De nada!",
    503 : "¡A tu disposición!",
    504 : "No, gracias a ti.",
    505 : "¡Buen trabajo en equipo!",
    506 : "¡Qué divertido!",
    507 : "¡Sé mi amigo!",
    508 : "¡Trabajemos en equipo!",
    509 : "¡Sois estupendos!",
    510 : "¿Eres nuevo aquí?",
    511 : "¿Has ganado?",
    512 : "Creo que esto es demasiado para ti.",
    513 : "¿Quieres que te ayude?",
    514 : "¿Puedes ayudarme?",

    # Friendly "You..."
    600 : "Pareces simpático.",
    601 : "¡Eres genial!",
    602 : "¡Eres la bomba!",
    603 : "¡Eres sensacional!",

    # Friendly "I like..."
    700 : "Me gusta tu nombre.",
    701 : "Me gusta tu aspecto.",
    702 : "Me gusta tu camiseta.",
    703 : "Me gusta tu falda.",
    704 : "Me gustan tus shorts.",
    705 : "¡Me gusta este juego!",

    # Sorry
    800 : "¡Lo siento!",
    801 : "¡Vaya!",
    802 : "¡Lo siento, estoy peleando con los bots!",
    803 : "¡Lo siento, estoy obteniendo gominolas!",
    804 : "¡Lo siento, estoy haciendo una dibutarea!",
    805 : "Lo siento, he tenido que marcharme repentinamente.",
    806 : "Discúlpame, me retrasé.",
    807 : "Lo siento, no puedo.",
    808 : "No he podido esperar más.",
    809 : "No te entiendo.",
    810 : "Usa la %s." % GlobalSpeedChatName,

    # Stinky
    900 : "¡Eh!",
    901 : "¡Vete de aquí!",
    902 : "¡Deja de hacer eso!",
    903 : "¡Eso es mala educación!",
    904 : "¡No seas malo!",
    905 : "¡Hueles mal!",
    906 : "Envía un informe de error.",
    907 : "No me puedo mover, porque hay un error.",

    # Places
    1000 : "¡Vamos!",
    1001 : "¿Puedes teletransportarte a donde estoy?",
    1002 : "¿Nos vamos?",
    1003 : "¿Adónde deberíamos ir?",
    1004 : "¿Por qué camino?",
    1005 : "Por aquí.",
    1006 : "Sígueme.",
    1007 : "¡Espérame!",
    1008 : "Vamos a esperar a mi amigo.",
    1009 : "Vamos a buscar a otros dibus.",
    1010 : "Espera aquí.",
    1011 : "Espera un momento.",
    1012 : "Nos encontraremos aquí.",
    1013 : "¿Puedes venir a mi casa?",

    # Places "Let's go..."
    1100 : "¡Vámonos en el tranvía!",
    1101 : "¡Vamos a volver al dibuparque!",
    1102 : "¡Vamos a luchar contra los %s!" % Cogs,
    1103 : "¡Vamos a tomar un edificio %s!" % Cog,
    1104 : "¡Vamos al ascensor!",
    1105 : "¡Vamos al Centro de Toontown!",
    1106 : "¡Vamos a Puerto Donald!",
    1107 : "¡Vamos a Melodilandia de Minnie!",
    1108 : "¡Vamos a los Jardines de Daisy!",
    1109 : "¡Vamos a Frescolandia!",
    1110 : "¡Vamos a Sueñolandia de Donald!",
    1111 : "¡Vamos a mi casa!",

    # Toontasks
    1200 : "¿En qué dibutarea estás trabajando?",
    1201 : "Ocupémonos de eso.",
    1202 : "Esto no es lo que busco.",
    1203 : "Voy a buscar eso.",
    1204 : "No está en esta calle.",
    1205 : "Todavía no lo he encontrado.",
    1299 : "Necesito que me asignen una dibutarea.",

    # Toontasks "I think you should choose..."
    1300 : "Creo que debes usarun curadibu.",
    1301 : "Creo que debes usar un sonido.",
    1302 : "Creo que debes usar una caída.",
    1303 : "Creo que debes usar un cebo.",
    1304 : "Creo que debes usar una trampa.",

    # Battle
    1400 : "¡Deprisa!",
    1401 : "¡Buen Disparo!",
    1402 : "¡Buena Broma!",
    1403 : "¡No me has dado!",
    1404 : "¡Lo has conseguido!",
    1405 : "¡Lo hemos hecho!",
    1406 : "¡Sigue así!",
    1407 : "¡Está chupado!",
    1408 : "¡Qué facil!",
    1409 : "¡Corre!",
    1410 : "¡Socorro!",
    1411 : "¡Uf!",
    1412 : "Tenemos problemas.",
    1413 : "Necesito más bromas.",
    1414 : "Necesito un curadibu.",
    1415 : "Deberías pasar.",

    # Battle "Let's use..."
    1500 : "¡Usemos un curadibu!",
    1501 : "¡Usemos una trampa!",
    1502 : "¡Usemos un cebo!",
    1503 : "¡Usemos un sonido!",
    1504 : "¡Usemos un lanzamiento!",
    1505 : "¡Usemos un chorro!",
    1506 : "¡Usemos una caida!",

    # Gag Shop
    1600 : "Tengo suficientes bromas.",
    1601 : "Necesito más gominolas.",
    1602 : "Yo también.",
    1603 : "¡Deprisa!",
    1604 : "¿Una más?",
    1605 : "¿Quieres jugar otra vez?",
    1606 : "Jugemos de nuevo.",

    # Factory
    1700 : "Separémonos.",
    1701 : "No nos separemos.",
    1702 : "Vamos a luchar contra los bots.",
    1703 : "Salta encima del interruptor.",
    1704 : "Atraviesa la puerta.",

    # Sellbot Factory
    1803 : "Estoy en la entrada principal.",
    1804 : "Estoy en el vestíbulo.",
    1805 : "Estoy en la entrada que da al vestíbulo.",
    1806 : "Estoy en la entrada que da al vestíbulo.",
    1807 : "Estoy en la sala de máquinas.",
    1808 : "Estoy en la sala de calderas.",
    1809 : "Estoy en la pasarela este.",
    1810 : "Estoy en la mezcladora de pintura.",
    1811 : "Estoy en la sala donde se guarda la mezcladora de pintura.",
    1812 : "Estoy en la pasarela del silo oeste.",
    1813 : "Estoy en la sala de tuberías.",
    1814 : "Estoy en las escaleras que dan a la sala de tuberías.",
    1815 : "Estoy en la sala de conductos.",
    1816 : "Estoy en la entrada de servicio.",
    1817 : "Estoy en el callejón del Pisotón.",
    1818 : "Estoy fuera de la sala de la lava.",
    1819 : "Estoy en la sala de la lava.",
    1820 : "Estoy en la sala donde se guarda la lava.",
    1821 : "Estoy en la pasarela oeste.",
    1822 : "Estoy en la sala del aceite.",
    1823 : "Estoy en la cabina de vigilancia del almacén.",
    1824 : "Estoy en el almacén.",
    1825 : "Estoy fuera de la mezcladora de pintura.",
    1827 : "Estoy fuera de la sala del aceite.",
    1830 : "Estoy en la sala de control del silo este.",
    1831 : "Estoy en la sala de control del silo oeste.",
    1832 : "Estoy en la sala de control del silo central.",
    1833 : "Estoy en el silo este.",
    1834 : "Estoy en el silo oeste.",
    1835 : "Estoy en el silo central.",
    1836 : "Estoy en el silo oeste.",
    1837 : "Estoy en el silo este.",
    1838 : "Estoy en la pasarela del silo este.",
    1840 : "Estoy encima del silo oeste.",
    1841 : "Estoy encima del silo este.",
    1860 : "Estoy en el ascensor del silo oeste.",
    1861 : "Estoy en el ascensor del silo este.",
    # Sellbot Factory continued
    1903 : "Reunámonos en la entrada principal.",
    1904 : "Reunámonos en el vestíbulo.",
    1905 : "Reunámonos en la entrada que da al vestíbulo.",
    1906 : "Reunámonos en la entrada que da al vestíbulo.",
    1907 : "Reunámonos en la sala de máquinas.",
    1908 : "Reunámonos en la sala de calderas.",
    1909 : "Reunámonos en la pasarela este.",
    1910 : "Reunámonos en la mezladora de pintura.",
    1911 : "Reunámonos en la sala donde se guarda la mezcladora de pintura.",
    1912 : "Reunámonos en la pasarela del silo oeste.",
    1913 : "Reunámonos en la sala de tuberías.",
    1914 : "Reunámonos en las escaleras que dan a la sala de tuberías.",
    1915 : "Reunámonos en la sala de conductos.",
    1916 : "Reunámonos en la entrada de servicio.",
    1917 : "Reunámonos en el callejón del Pisotón.",
    1918 : "Reunámonos fuera de la sala de la lava.",
    1919 : "Reunámonos en la sala de la lava.",
    1920 : "Reunámonos en la sala donde se guarda la lava.",
    1921 : "Reunámonos en la pasarela oeste.",
    1922 : "Reunámonos en la sala del aceite.",
    1923 : "Reunámonos en la cabina de vigilancia del almacén.",
    1924 : "Reunámonos en el almacén.",
    1925 : "Reunámonos fuera de la mezcladora de pintura.",
    1927 : "Reunámonos fuera de la sala del aceite.",
    1930 : "Reunámonos en la sala de control del silo este.",
    1931 : "Reunámonos en la sala de control del silo oeste.",
    1932 : "Reunámonos en la sala de control del silo central.",
    1933 : "Reunámonos en el silo este.",
    1934 : "Reunámonos en el silo oeste.",
    1935 : "Reunámonos en el silo central.",
    1936 : "Reunámonos en el silo oeste.",
    1937 : "Reunámonos en el silo este.",
    1938 : "Reunámonos en la pasarela del silo este.",
    1940 : "Reunámonos encima del silo oeste.",
    1941 : "Reunámonos encima del silo este.",
    1960 : "Reunámonos en el ascensor del silo oeste.",
    1961 : "Reunámonos en el ascensor del silo este.",

    # These are used only for the style settings in the OptionsPage
    # These should never actually be spoken or listed on the real speed chat
    2000 : "Morado",
    2001 : "Azul",
    2002 : "Añil",
    2003 : "Aguamarina",
    2004 : "Verde",
    2005 : "Amarillo",
    2006 : "Naranja",
    2007 : "Rojo",
    2008 : "Rosa",
    2009 : "Marrón",

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
    10 : "Está bien.",
    20 : "¿Porque no?",
    30 : "¡Naturalmente!",
    40 : "Esa es la manera de hacerlo.",
    50 : "¡Exacto!",
    60 : "¿Que pasa?",
    70 : "¡Por supuesto!",
    80 : "Bingo!",
    90 : "Debes de estar bromeando...",
    100 : "Me suena bien.",
    110 : "¡Qué locura!",
    120 : "¡Impresionante!",
    130 : "¡Por amor de Dios!",
    140 : "No te preocupes.",
    150 : "¡Grrrr!",
    160 : "¿Alguna novedad?",
    170 : "¡Eh, eh, eh!",
    180 : "Hasta mañana.",
    190 : "Hasta otra vez.",
    200 : "Nos vemos.",
    210 : "Hasta la vista.",
    220 : "Tengo que irme pronto.",
    230 : "¡No sé nada de esto!",
    240 : "¡Largo de aquí!",
    250 : "¡Ay! ¡Cómo duele!",
    260 : "¡Te tengo!",
    270 : "¡Por favor!",
    280 : "¡Mil gracias!",
    290 : "¡Me encanta cómo vas!",
    300 : "¡Perdona!",
    310 : "¿Te puedo ayudar?",
    320 : "¡A eso me refería!",
    330 : "Si no aguantas el calor, no te acerques al horno.",
    340 : "¡Truenos y relampagos!",
    350 : "¡Pero qué cosa más especial!",
    360 : "¡Deja de enredar!",
    370 : "¿Te ha comido la lengua el gato?",
    380 : "¡Estás metido en un buen lío!",
    390 : "Pero mira lo que tenemos aquí...",
    400 : "Tengo que ir a ver a un dibu.",
    410 : "¡No te enfades!",
    420 : "¡No seas gallina!",
    430 : "Eres un blanco fácil.",
    440 : "¡Lo que sea!",
    450 : "¡Totalmente!",
    460 : "¡Estupendo!",
    470 : "¡Fantástico!",
    480 : "¡Por supuesto!",
    490 : "¡A que no me pillas!",
    500 : "Primero tienes que curarte.",
    510 : "Necesitas más puntos de risa.",
    520 : "Vuelvo en un momento.",
    530 : "Tengo hambre.",
    540 : "¡Sí, claro!",
    550 : "Tengo sueño.",
    560 : "¡Estoy listo!",
    570 : "Estoy aburrido.",
    580 : "¡Me encanta!",
    590 : "¡Qué emocionante!",
    600 : "¡Salta!",
    610 : "¿Tienes bromas?",
    620 : "¿Qué pasa?",
    630 : "Poco a poco.",
    640 : "Despacito y buena letra.",
    650 : "¡Gol!",
    660 : "¡Prepararse!",
    670 : "¡Listos!",
    680 : "¡Ya!",
    690 : "¡Vamos por aquí!",
    700 : "¡Has ganado!",
    710 : "Yo voto que sí.",
    720 : "Yo voto que no.",
    730 : "Cuenta conmigo.",
    740 : "No cuentés conmigo.",
    750 : "Quédate aquí, vuelvo enseguida.",
    760 : "¡Qué rápido!",
    770 : "¿Has visto eso?",
    780 : "¿A qué huele eso?",
    790 : "¡Qué hediondo!",
    800 : "No me importa.",
    810 : "Justo lo que el medico ordenó.",
    820 : "¡Que empiece la fiesta!",
    830 : "¡Por aquí todos!",
    840 : "¿Qué pasa?",
    850 : "El cheque está en el correo.",
    860 : "¡Te he oído!",
    870 : "¿Me estas hablando?",
    880 : "Gracias, estaré aquí toda la semana.",
    890 : "Mmm.",
    900 : "Yo me ocupo de éste.",
    910 : "¡Lo tengo!",
    920 : "¡Es mio!",
    930 : "Por favor, toma esto.",
    940 : "No te acerques; esto puede ser peligroso.",
    950 : "¡No te preocupes!",
    960 : "¡Vaya!",
    970 : "¡Guau!",
    980 : "¡Uuuuuu!",
    990 : "¡Todos a bordo!",
    1000 : "¡Que fantastico!",
    1010 : "La curiosidad mató al gato.",
    # Series 2
    2000 : "¡Vamos, no seas infantil!",
    2010 : "¡Qué alegría de verte!",
    2020 : "No faltaba más.",
    2030 : "No te habrás metido en líos, ¿verdad?",
    2040 : "¡Mejor tarde que nunca!",
    2050 : "¡Bravo!",
    2060 : "No, en serio, amigos...",
    2070 : "¿Te animas?",
    2080 : "¡Nos vemos luego!",
    2090 : "¿Has cambiado de idea?",
    2100 : "¡Si lo quieres, ven a cogerlo!",
    2110 : "¡Ay, dios mío!",
    2120 : "Encantado de conocerte.",
    2130 : "¡No hagas nada que yo no haría!",
    2140 : "¡Ni se te ocurra!",
    2150 : "¡No tires la toalla!",
    2160 : "Mejor espera sentado.",
    2170 : "No preguntes.",
    2180 : "Para ti todo es muy fácil.",
    2190 : "¡Ya está bien!",
    2200 : "¡Estupendo!",
    2210 : "¡Vaya, qué casualidad!",
    2220 : "¡Déjame en paz!",
    2230 : "Y yo que me alegro.",
    2240 : "Venga, que me voy a divertir un rato.",
    2250 : "¡A por todas!",
    2260 : "¡Bien hecho!",
    2270 : "¡Qué alegría de verte!",
    2280 : "Me tengo que pirar.",
    2290 : "Me tengo que largar.",
    2300 : "Espera.",
    2310 : "Un momento.",
    2320 : "¡Disfruta como un loco!",
    2330 : "¡Diviértete!",
    2340 : "Oye, que no tengo todo el día…",
    2350 : "¡Un momento!",
    2360 : "¡Qué pamplinas!",
    2370 : "¡No me lo puedo creer!",
    2380 : "Lo dudo mucho.",
    2390 : "Te debo una.",
    2400 : "Te oigo perfectamente.",
    2410 : "Creo que sí.",
    2420 : "Creo que deberías pasar.",
    2430 : "Ya lo podía haber dicho yo.",
    2440 : "Ni se te ocurra.",
    2450 : "¡Por mí, encantado!",
    2460 : "Estoy ayudando a mi amigo.",
    2470 : "Me quedo toda la semana.",
    2480 : "¡Imagínate!",
    2490 : "Justo a tiempo...",
    2500 : "Todavía no ha acabado la cosa.",
    2510 : "Estaba pensando en voz alta.",
    2520 : "No te pierdas; llama de vez en cuando.",
    2530 : "¡Garbanzos en remojo!",
    2540 : "¡Muévete!",
    2550 : "Ponte cómodo.",
    2560 : "En otro momento, quizás.",
    2570 : "¿Interrumpo?",
    2580 : "¡Menuda choza!",
    2590 : "Bueno, una charla muy agradable.",
    2600 : "Sin lugar a dudas.",
    2610 : "¡No me digas!",
    2620 : "Ni por asomo.",
    2630 : "¡Qué cara!",
    2640 : "Por mí, vale.",
    2650 : "¡Vale!",
    2660 : "¡Sonrían, por favor!",
    2670 : "¿Qué?",
    2680 : "¡Pachán!",
    2690 : "Tómatelo con calma.",
    2700 : "¡Chao!",
    2710 : "Gracias, pero mejor no.",
    2720 : "¡Esto es el acabóse!",
    2730 : "Qué bueno.",
    2740 : "¡Justo lo que necesitaba!",
    2750 : "¡"+TheCogs+" nos invaden!",
    2760 : "¡Arrivederci!",
    2770 : "¡Cuidado!",
    2780 : "¡Muy bien!",
    2790 : "¿Qué se cuece?",
    2800 : "¿Qué pasa?",
    2810 : "Por mí, vale.",
    2820 : "Sí, señor.",
    2830 : "Por supuesto.",
    2840 : "Haz el cálculo.",
    2850 : "¿Ya te vas?",
    2860 : "¡No me hagas reír!",
    2870 : "Vete por la derecha.",
    2880 : "¡Despídete de este mundo!",
    # Series 3
    3000 : "Lo que tú digas.",
    3010 : "¿Molesto?",
    3020 : "La cuenta, por favor.",
    3030 : "Yo no estaría tan seguro.",
    3040 : "No te voy a decir que no.",
    3050 : "Tampoco te partas la crisma…",
    3060 : "Lo sabes muy bien.",
    3070 : "Yo, como si no estuviera.",
    3080 : "¡Eureka!",
    3090 : "¡Imagínate!",
    3100 : "¡Ni lo sueñes!",
    3110 : "¿Vienes conmigo?",
    3120 : "¡Muy bien!",
    3130 : "¡Por dios!",
    3140 : "¡Que disfrutes!",
    3150 : "¡Ánimo!",
    3160 : "Otra vez.",
    3170 : "¡Toma ya!",
    3180 : "¡Ahí tienes!",
    3190 : "Eso creo.",
    3200 : "Ni de broma.",
    3210 : "Luego te contesto.",
    3220 : "Soy todo oídos.",
    3230 : "Estoy ocupado.",
    3240 : "¡Que no estoy de broma!",
    3250 : "Me he quedado de una piedra.",
    3260 : "Venga, ánimo.",
    3270 : "¡Mantenme al corriente!",
    3280 : "¡Lluvia de tartas!",
    3290 : "Lo mismo digo.",
    3300 : "¡Andando, que es gerundio!",
    3310 : "El tiempo vuela.",
    3320 : "Sin comentarios.",
    3330 : "¡Así se habla!",
    3340 : "Por mí, bien.",
    3350 : "Encantado.",
    3360 : "Vale.",
    3370 : "Claro que sí.",
    3380 : "Muchísimas gracias.",
    3390 : "Así me gusta.",
    3400 : "¡Así se hace!",
    3410 : "Me voy para el catre.",
    3420 : "¡Hazme caso!",
    3430 : "Hasta la próxima.",
    3440 : "¡Espera un momentito!",
    3450 : "¡Así se hace!",
    3460 : "¿Cómo tú por aquí?",
    3470 : "¿Qué ha pasado?",
    3480 : "¿Ahora qué?",
    3490 : "Después de ti.",
    3500 : "Vete por la izquierda.",
    3510 : "¡Eso es lo que tú querrías!",
    3520 : "¡Date por muerto!",
    3530 : "¡Menudo eres tú!",

    # Halloween
    10000 : "Esto es una ciudad fantasma.",
    10001 : "¡Bonito disfraz!",
    10002 : "Creo que esto está embrujado.",
    10003 : "¡Chuches o venganza!",
    10004 : "¡Buuu!",
    10005 : "¡Feliz embrujamiento!",
    10006 : "¡Feliz Halloween!",
    10007 : "Es la hora de convertirme en una calabaza.",
    10008 : "¡Fantasmástico!",
    10009 : "¡Espeluznante!",
    10010 : "¡Qué miedo da!",
    10011 : "¡Odio las arañas!",
    10012 : "¿Has oído eso?",
    10013 : "¡Tienes menos posibilidades que un fantasma!",
    10014 : "¡Me has asustado!",
    10015 : "¡Qué susto!",
    10016 : "¡Qué monstruoso!",
    10017 : "Eso ha sido muy raro...",
    10018 : "¿Habrán esqueletos en el armario?",
    10019 : "¿Te he asustado?",

    # Fall Festivus
    11000 : "Anda, que estás más relleno que un pavo en Navidad",
    11001 : "¡No me vengas con pucheros!",
    11002 : "¡Brrr!",
    11003 : "¡Tranqui, colega!",
    11004 : "¡Ven a por ello!",
    11005 : "Qué pavo eres.",
    11006 : "¡glu, glu, glu!",
    11007 : "¡Felices vacaciones!",
    11008 : "¡Feliz año nuevo!",
    11009 : "Sé bueno que los Reyes Magos lo ven todo.",
  # 11010 : "¡Feliz pavo!",
    11011 : "¡No te atragantes con las uvas!",
    11012 : "Estás más ilocalizable que Papá Noel en Nochebuena.",
    11013 : "Va más rápido que las campanadas de Fin de Año.",
    11014 : "¡Que nieve!",
    11015 : "Trae para acá.",
    11016 : "¡Felices Fiestas!",
    11017 : "Estoy más mosqueado que un pavo oyendo panderetas.",
    11018 : "¡Nevando voy, nevando vengo!",
    11019 : "¡Te vas a arrepentir, tronco!",

    # Valentines
  # 12000 : "Si el mundo fuera un pañuelo…, serías mi moco preferido.",
    12001 : "¡Te quieroooooooo!",
    12002 : "¡Feliz día de San Valentín!",
    12003 : "Oooh, qué bonito.",
    12004 : "Me gustas un montón.",
    12005 : "Amor incondicional.",
    12006 : "¡Te quiero! ¿Me oyes?",
    12007 : "¿Quedamos por San Valentín?",
    12008 : "Gracias, mi vida.",
    12009 : "Gracias, cariñín.",
    12010 : "Qué guapo eres.",
    12011 : "Qué guapa eres.",
    12012 : "¡Estupendo!",
    12013 : "¡Qué bien!",
    12014 : "Las rosas son rojas...",
    12015 : "Las violetas azuladas...",
    12016 : "¡Qué bonito!",

    # St. Patricks Day
    13000 : "Llegó el verano y los mosquitos mueren entre aplausos.",
    13001 : "¡Feliz veraneo!",
    13002 : "¡Con las chanclas y a la playa!",
    13003 : "Si la piscina es honda… ¿El mar es toyota?",
    13004 : "Tengo más problemas que las Vacaciones Santillana.",
    13005 : "Buen viaje, y si el avión viene demorado, tú ponte “deverde”.",
    13006 : "¡Te repites más que Verano Azul!",
    13007 : "¡Que disfrutes del sol!",
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
PlaygroundDeathAckMessage = "¡"+TheCogs+" se han llevado todas tus bromas!\n\nEstás triste. No puedes irte del dibuparque hasta que estés feliz."

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "El capataz de la fábrica ha sido derrotado antes de que llegaras. No has recuperado ninguna pieza bot."

# DistributedFactory.py
HeadingToFactoryTitle = "De camino a %s..."
ForemanConfrontedMsg = "¡%s está luchando contra el capataz de la fábrica!"

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "Esperando a que se unan otros jugadores..."
MinigamePleaseWait = "Espera..."
DefaultMinigameTitle = "Título del minijuego"
DefaultMinigameInstructions = "Instrucciones del minijuego"
HeadingToMinigameTitle = "Entrando al %s..." # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "Indicador\nde fuerza"
MinigamePowerMeterTooSlow = "Muy\nlento"
MinigamePowerMeterTooFast = "Muy\nrápido"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "Plantilla del minijuego"
MinigameTemplateInstructions = "Ésta es una plantilla de minijuegos. Úsala para crear nuevos minijuegos."

# DistributedCannonGame.py
CannonGameTitle = "Juego El Cañón"
CannonGameInstructions = "Dispara a tu dibu para meterlo en el depósito de agua tan rápido como puedas. Usa el ratón o las teclas de flecha para apuntar el cañón. ¡Date prisa y consigue una gran recompensa para todos!"
CannonGameReward = "RECOMPENSA"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "Juego La Cuerda"
TugOfWarInstructions = "Pulsa alternativamente las teclas de flecha izquierda y derecha con la suficiente rapidez para alinear la barra verde con la línea roja. ¡No pulses demasiado deprisa ni demasiado despacio, o acabarás en el agua!"
TugOfWarGameGo = "¡YA!"
TugOfWarGameReady = "Listo..."
TugOfWarGameEnd = "¡Muy bien!"
TugOfWarGameTie = "¡Has empatado!"
TugOfWarPowerMeter = "Indicador de fuerza"

# DistributedPatternGame.py
PatternGameTitle = "Imita a %s" % Minnie
PatternGameInstructions = Minnie + " te enseñará una secuencia de baile " + \
                          "Intenta repetir con las teclas de flecha el baile de "+Minnie+" justo igual que lo hace ella."
PatternGameWatch   = "Observa estos pasos de baile..."
PatternGameGo      = "¡YA!"
PatternGameRight   = "¡Bien, %s!"
PatternGameWrong   = "¡Vaya!"
PatternGamePerfect = "¡Ha sido perfecto, %s!"
PatternGameBye     = "¡Gracias por jugar!"
PatternGameWaitingOtherPlayers = "Esperando a otros jugadores..."
PatternGamePleaseWait = "Espera..."
PatternGameFaster = "¡Has sido\nmuy rápido!"
PatternGameFastest = "¡Has sido\nel más rápido!"
PatternGameYouCanDoIt = "¡Vamos!\n¡Puedes hacerlo!"
PatternGameOtherFaster = "\nha sido más rápido."
PatternGameOtherFastest = "\nha sido el más rápido."
PatternGameGreatJob = "¡Buen trabajo!"
PatternGameRound = "¡Asalto nº %s!" # Round 1! Round 2! ..

# DistributedRaceGame.py
RaceGameTitle = "Juego La Carrera"
RaceGameInstructions = "Haz clic en un número. ¡Piénsalo bien! Sólo avanzarás si nadie más ha escogido ese mismo número."
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
RaceGameOthersBackThree = "todos los demás, atrás \n3 espacios"
RaceGameInstantWinner = "¡Ganador instantáneo!"
RaceGameJellybeans2 = "2 gominolas"
RaceGameJellybeans4 = "4 gominolas"
RaceGameJellybeans10 = "¡10 gominolas!"

# DistributedRingGame.py
RingGameTitle = "Juego Los Anillos"
# color
RingGameInstructionsSinglePlayer = "Intenta atravesar nadando todos los anillos que puedas de color %s. Usa las teclas de flecha para nadar."
# color
RingGameInstructionsMultiPlayer = "Intenta atravesar nadando los anillos de color %s.  Los demás jugadores intentarán atravesar el resto de los anillos.  Usa las flechas del teclado para nadar."
RingGameMissed = "FALLO"
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

# DistributedTagGame.py
TagGameTitle = "Tú la llevas"
TagGameInstructions = "Recoge los tesoros. ¡No puedes recoger tesoros cuando LA LLEVES!"
TagGameYouAreIt = "¡Tú la LLEVAS!"
TagGameSomeoneElseIsIt = "¡%s la LLEVA!"

# DistributedMazeGame.py
MazeGameTitle = "Juego El Laberinto"
MazeGameInstructions = "Recoge los tesoros. ¡Intenta recogerlos todos, pero ten cuidado con los bots!"

# DistributedCatchGame.py
CatchGameTitle = "Juego Atrapa las frutas"
CatchGameInstructions = "Atrapa %(fruit)s que puedas. Cuidado con los " + Cogs + ", y trata de no ‘atrapar’ ningún %(badThing)s!"
CatchGamePerfect = "¡PERFECTO!"
CatchGameApples      = 'todas las manzanas'
CatchGameOranges     = 'todas las naranjas'
CatchGamePears       = 'todas las peras'
CatchGameCoconuts    = 'todos los cocos'
CatchGameWatermelons = 'todas las sandìas'
CatchGamePineapples  = 'todas las piñas'
CatchGameAnvils      = 'yunque'

# DistributedPieTossGame.py
PieTossGameTitle = "Juego Lanzatartas"
PieTossGameInstructions = "Prueba tu puntería lanzando tartas."

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "JUGAR"

# Purchase.py
GagShopName = "Tienda de bromas de Goofy"
GagShopPlayAgain = "JUGAR\nOTRA VEZ"
GagShopBackToPlayground = "VOLVER AL\nDIBUPARQUE"
GagShopYouHave = "Tienes %s gominolas para gastar"
GagShopYouHaveOne = "Tienes 1 gominola para gastar"
GagShopTooManyProps = "Lo siento, tienes demasiados accesorios"
GagShopDoneShopping = "COMPRAS\nFINALIZADAS"
# name of a gag
GagShopTooManyOfThatGag = "Lo siento, ya tienes suficientes %s."
GagShopInsufficientSkill = "Todavía no tienes suficiente habilidad para eso"
# name of a gag
GagShopYouPurchased = "Has comprado %s"
GagShopOutOfJellybeans = "¡Lo siento, te has quedado sin gominolas!"
GagShopWaitingOtherPlayers = "Esperando a otros jugadores..."
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%s se ha desconectado"
GagShopPlayerExited = "%s se ha marchado"
GagShopPlayerPlayAgain = "Jugar de nuevo"
GagShopPlayerBuying = "Comprando"

# MakeAToon.py
#
# The voices for GenderShopQuestionMickey and Minnie should not be played simultaneously.
# Options are as follows:
# 1: Mickey first and Minnie follow in a few second.
# 2: When player moves cursor onto the character, the voice to be played.
#    But the voice shouldn't be played while other character is talking.
# Please choose whichever feasible.
#
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
ColorShopHead = "Cabeza"
ColorShopBody = "Cuerpo"
ColorShopLegs = "Piernas"
ColorShopToon = "Dibu"
ColorShopParts = "Partes"
ColorShopAll = "Todo"

# ClothesShop.py
ClothesShopShorts = "Shorts"
ClothesShopShirt = "Camiseta"
ClothesShopBottoms = "Falda"

# MakeAToon
MakeAToonDone = "Hecho"
MakeAToonCancel = "Cancelar"
MakeAToonNext = "Siguiente"
MakeAToonLast = "Atrás"
CreateYourToon = "Haz clic en las flechas para crear a tu dibu."
CreateYourToonTitle = "Crea a tu dibu"
CreateYourToonHead = "Haz clic en las flechas de la \"cabeza\" para escoger diferentes animales."
MakeAToonClickForNextScreen = "Haz clic en la flecha situada abajo para ir a la pantalla siguiente."
PickClothes = "¡Haz clic en las flechas para escoger prendas!"
PickClothesTitle = "Escoge tus prendas"
PaintYourToon = "¡Haz clic en las flechas para pintar a tu dibu!"
PaintYourToonTitle = "Pinta a tu dibu"
MakeAToonYouCanGoBack = "¡También puedes volver para cambiar tu cuerpo!"
MakeAFunnyName = "¡Elige un nombre divertido para el dibu con el juego de los nombres!"
MustHaveAFirstOrLast1 = "Tu dibu debería tener un nombre o un apellido, ¿no crees?"
MustHaveAFirstOrLast2 = "¿No quieres que tu dibu tenga un nombre o un apellido?"
ApprovalForName1 = "¡Eso es, tu dibu se merece un gran nombre!"
ApprovalForName2 = "¡Los nombres de dibus son los mejores!"
MakeAToonLastStep = "¡Último paso antes de ir a Toontown!"
PickANameYouLike = "¡Escoge un nombre que te guste!"
NameToonTitle = "Pon un nombre a tu dibu"
TitleCheckBox = "Título"
FirstCheckBox = "Nombre"
LastCheckBox = "Apellido"
RandomButton = "Al azar"
NameShopSubmitButton = "Enviar"
TypeANameButton = "Escribe un nombre"
TypeAName = "¿No te gustan estos nombres?\nHaz clic aquí -->"
PickAName = "¡Prueba con el juego de los nombres!\nHaz clic aquí -->"
PickANameButton = "Juego de los nombres"
RejectNameText = "Ese nombre no está permitido. Inténtalo de nuevo."
WaitingForNameSubmission = "Se está enviando tu nombre..."

# NameShop.py
NameShopNameMaster = "NameMasterCastillian.txt"
NameShopPay = "¡Suscríbete ya!"
NameShopPlay = "Prueba gratuita"
NameShopOnlyPaid = "Sólo los usuarios abonados\npueden poner nombre a sus dibus.\nHasta que te suscribas,\ntu nombre será\n"
NameShopContinueSubmission = "Continuar envío"
NameShopChooseAnother = "Elegir otro nombre"
NameShopToonCouncil = "El Consejo Dibu\nrevisará tu\nnombre.  " + \
                      "La revisión puede\ntardar unos días.\nMientras esperas,\ntu nombre será\n "
PleaseTypeName = "Escribe tu nombre:"
AllNewNames = "Todos los nombres nuevos\ndeben ser aprobados\npor el Consejo Dibu."
NameShopNameRejected = "El nombre que has\nenviado ha sido\nrechazado."
NameShopNameAccepted = "¡Enhorabuena!\nEl nombre que has\nenviado ha sido\naceptado."
NoPunctuation = "¡No puedes usar signos de puntuación en tu nombre!"
PeriodOnlyAfterLetter = "Tu nombre puede incluir un punto, pero sólo después de una letra."
ApostropheOnlyAfterLetter = "Tu nombre puede incluir un apóstrofo, pero sólo después de una letra."
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
    "donald duck",
    "donaldduck",
    "pluto",
    "goofy",
    )
NumToColor = ['Blanco', 'Melocotón', 'Rojo brillante', 'Rojo', 'Castaño',
              'Siena', 'Marrón', 'Marrón claro', 'Coral', 'Naranja',
              'Amarillo', 'Crema', 'Topacio', 'Lima', 'Verde mar',
              'Verde', 'Azul claro', 'Aguamarina', 'Azul',
              'Hierba', 'Azul marino', 'Azul pizarra', 'Morado',
              'Lavanda', 'Rosa']
AnimalToSpecies = {
    'dog'    : 'Perro',
    'cat'    : 'Gato',
    'mouse'  : 'Ratón',
    'horse'  : 'Caballo',
    'rabbit' : 'Conejo',
    'duck'   : 'Pato',
    }
NameTooLong = "Ese nombre es demasiado largo. Inténtalo de nuevo."
ToonAlreadyExists = "¡Ya tienes un dibu llamado %s!"
NameAlreadyInUse = "¡Ese nombre ya ha sido usado!"
EmptyNameError = "Primero debes introducir un nombre."
NameError = "Lo siento. Ese nombre no sirve."

# NameCheck.py
NCTooShort = 'Ese nombre es demasiado corto.'
NCNoDigits = 'Tu nombre no puede contener números.'
NCNeedLetters = 'Todas las palabras de tu nombre deben contener letras.'
NCNeedVowels = 'Todas las palabras de tu nombre deben contener vocales.'
NCAllCaps = 'Tu nombre no puede estar por completo en mayúsculas.'
NCMixedCase = 'Ese nombre tiene demasiadas mayúsculas.'
NCBadCharacter = "Tu nombre no puede contener el carácter '%s'"
NCGeneric = 'Lo siento, ese nombre no sirve.'
NCTooManyWords = 'Tu nombre no puede tener más de cuatro palabras.'
NCDashUsage = ("Sólo puedes usar los guiones para unir dos palabras "
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
RemoveTrophy = "Cuartel general dibu: ¡"+TheCogs+" han tomado el control de uno de los edificios que has recuperado!"

# toon\DistributedNPCTailor/Clerk.py
STOREOWNER_TOOKTOOLONG = '¿Necesitas más tiempo para pensártelo?'
STOREOWNER_GOODBYE = '¡Hasta luego!'
STOREOWNER_NEEDJELLYBEANS = 'Tienes que subir al tranvía para conseguir gominolas.'
STOREOWNER_GREETING = 'Elige lo que quieras comprar.'
STOREOWNER_BROWSING = 'Puedes mirar, pero para comprar necesitas un tícket de ropa.'
STOREOWNER_NOCLOTHINGTICKET = 'Para comprar prendas necesitas un tícket de ropa.'
# translate
STOREOWNER_NOFISH = 'Vuelve aquí para vender peces a la tienda de animales a cambio de gominolas.'
STOREOWNER_THANKSFISH = '¡Gracias! A la tienda de animales le van a encantar. ¡Adiós!'

STOREOWNER_NOROOM = "Mmm...tienes que tener mas sitio en tu clóset antes de comprar mas ropa.\n"
STOREOWNER_CONFIRM_LOSS = "Tú closet esta lleno. Tú vas a perder la ropa que estabas usando."
STOREOWNER_OK = "Muy bien"
STOREOWNER_CANCEL = "Cancelar"
STOREOWNER_TROPHY = "Wow! You collected %s of %s fish. That deserves a trophy and a LaffBoost!"
# end translate

# NewsManager.py
SuitInvasionBegin1 = "Cuartel general: ¡¡Hay una invasión de bots!!"
SuitInvasionBegin2 = "Cuartel general: ¡¡Los %s han tomado Toontown!!!"
SuitInvasionEnd1 = "Cuartel general: ¡¡¡La invasión de %s ha terminado!!!"
SuitInvasionEnd2 = "Cuartel general: ¡¡¡Los dibus han vuelto a salvarnos!!!"
SuitInvasionUpdate1 = "Cuartel general: ¡¡¡La invasión de bots consta ahora de %s bots!!!"
SuitInvasionUpdate2 = "Cuartel general: ¡¡¡Debemos derrotar a esos %s!!!"
SuitInvasionBulletin1 = "Cuartel general: ¡¡¡Se está produciendo una invasión de bots!!!"
SuitInvasionBulletin2 = "Cuartel general: ¡¡Los %s han tomado Toontown!!!"

# DistributedHQInterior.py
LeaderboardTitle = "Pelotón de dibus"
# QuestScript.txt
QuestScriptTutorialMickey_1 = "¡Toontown tiene un nuevo habitante! ¿Tienes alguna broma de sobra?"
QuestScriptTutorialMickey_2 = "¡Claro, %s!"
QuestScriptTutorialMickey_3 = "Tato Tutorial te lo explicará todo sobre los bots.\a¡Tengo que irme!"
QuestScriptTutorialMickey_4 = "¡Ven aquí! Usa las flechas del teclado para moverte."

# These are needed to correspond to the Japanese gender specific phrases
#
#QuestScriptTutorialMinnie_1 = "¡Toontown tiene un nuevo habitante! ¿Tienes alguna broma de sobra?"
#QuestScriptTutorialMinnie_2 = "¡Claro, %s!"
#QuestScriptTutorialMinnie_3 = "Tato Tutorial te lo explicará todo sobre los bots.\a¡Tengo que irme!"
#

#
# If there is "\a" between the sentense, we would like to have one of the following sequence.
# 1: display 1st text with 1st voice -> when voice finished, arrow appear. -> if player pushes the arrow button, display 2nd text with 2nd voice.
# 2: display 1st text with 1st voice and altomatically display 2nd text with 2nd voice.
# 3: display 1st text and play 1st voice (arrow is displayed) -> whenever player pushes the button, the voice will be skipped and display 2nd text with 2nd voice.
# Anyway, we need to have some "Skip" rule while playing the voice because from DCV(Disney Character Voice)'s view, it is not preferrable to have voice skipped.
#

QuestScript101_1 = "Ésos son los BOTS. Son robots que intentan tomar el control de Toontown."
QuestScript101_2 = "Hay muchos tipos distintos de BOTS, que..."
QuestScript101_3 = "...convierten los alegres edificios de los dibus..."
QuestScript101_4 = "...¡en horribles edificios bot!"
QuestScript101_5 = "¡Pero los BOTS no aguantan las bromas!"
QuestScript101_6 = "Una buena broma acaba con ellos."
QuestScript101_7 = "Hay un montón de bromas, pero puedes empezar con éstas."
QuestScript101_8 = "¡Oh! ¡También necesitas un risómetro!"
QuestScript101_9 = "Si tu risómetro disminuye demasiado, te pondrás triste."
QuestScript101_10 = "¡Cuanto más contento está un dibu, más sano está!"
QuestScript101_11 = "¡OH, NO! ¡Hay un BOT fuera de la tienda!"
QuestScript101_12 = "¡AYÚDAME, POR FAVOR! ¡Derrota a ese BOT!"
QuestScript101_13 = "¡Aquí tienes tu primera dibutarea!"
QuestScript101_14 = "¡Deprisa! ¡Derrota a ese secuaz!"

QuestScript110_1 = "Gracias por derrotar a ese secuaz. Te voy a dar un dibucuaderno..."
QuestScript110_2 = "Es un cuaderno lleno de cosas chulas."
QuestScript110_3 = "Ábrelo y te iré enseñando cosas."
QuestScript110_4 = "El mapa te muestra dónde has estado."
QuestScript110_5 = "Pasa la página para ver tus bromas..."
QuestScript110_6 = "¡Vaya! ¡No tienes bromas! Te voy a asignar una tarea."
QuestScript110_7 = "Pasa la página para ver las tareas."
QuestScript110_8 = "Para comprar bromas tienes que subirte al tranvía y conseguir gominolas."
QuestScript110_9 = "Para subirte al tranvía, sal por la puerta que hay detrás de mí y dirígete al dibuparque."
QuestScript110_10 = "Ahora, cierra el dibucuaderno y busca el tranvía."
QuestScript110_11 = "Vuelve al cuartel general cuando hayas terminado. ¡Chao!"

QuestScriptTutorialBlocker_1 = "¡Eh, hola!"
QuestScriptTutorialBlocker_2 = "¿Hola?"
QuestScriptTutorialBlocker_3 = "¡Oh! ¡No sabes cómo se usa la Charla rápida!"
QuestScriptTutorialBlocker_4 = "Haz clic en el botón para decir algo."
QuestScriptTutorialBlocker_5 = "¡Muy bien!\aEn el sitio al que vas hay muchos dibus con los que puedes hablar."
QuestScriptTutorialBlocker_6 = "Si quieres charlar con tus amigos mediante el teclado, tienes que usar otro botón."
QuestScriptTutorialBlocker_7 = "Es el botón \"Charla\". Para poder usarlo tienes que ser habitante oficial de Toontown."
QuestScriptTutorialBlocker_8 = "¡Buena suerte! ¡Hasta luego!"

"""
GagShopTut

You will also earn the ability to use other types of gags.

"""

QuestScriptGagShop_1 = "Welcome to the Gag Shop!"
QuestScriptGagShop_1a = "This is where Toons come to buy gags to use against the Cogs."
#QuestScriptGagShop_2 = "This jar shows how many jellybeans you have."
QuestScriptGagShop_3 = "To buy a gag, click on a gag button. Try it now!"
QuestScriptGagShop_4 = "Good! You can use these gags in battle against the Cogs."
QuestScriptGagShop_5 = "Here's a peek at the advanced throw and squirt gags..."
QuestScriptGagShop_6 = "When you're done buying gags, click this button to return to the Playground."
QuestScriptGagShop_7 = "Normally you can use this button to play another Trolley Game..."
QuestScriptGagShop_8 = "...but there's no time for another game right now. You're needed in Toon HQ!"

QuestScript120_1 = "¡Que bueno, encontraste el tranvía!\aPor cierto, ¿conoces ya a Pecunio el banquero?\aEs bastante goloso.\a¿Por qué no te presentas llevándole esta chocolatina como regalo?"
QuestScript120_2 = "Pecunio el banquero está en el Banco de Toontown."

QuestScript121_1 = "Mmm, gracias por la chocolatina.\aOye, si me ayudas, te daré una recompensa.\a"+TheCogs+" han robado las llaves de mi caja fuerte. Derrota a los bots hasta recuperar la llave robada.\aCuando encuentres la llave, tráemela."

QuestScript130_1 = "¡Que bueno, encontraste el tranvía!\aPor cierto, hoy he recibido un paquete para Pedro el maestro.\aDeben de ser las nuevas tizas que ha encargado.\a¿Puedes llevárselas?\aEstá en el colegio."

QuestScript131_1 = "Oh, gracias por las tizas.\a¡¿Qué?!\a"+TheCogs+" me han robado la pizarra. Derrótales y recupera mi pizarra.\aCuando la encuentres, tráemela."

QuestScript140_1 = "¡Que bueno, encontraste el tranvía!\aPor cierto, mi amigo Leopoldo es todo un devorador de libros.\aLa última vez que estuve en Puerto Donald le recogí este libro.\a¿Podrías llevárselo? Suele estar en la biblioteca."

QuestScript141_1 = "Oh, sí, con este libro casi completaré mi colección.\aDéjame ver...\aVaya...\a¿Dónde habré puesto las gafas?\aLas tenía justo antes de que los bots ocupasen mi edificio.\aDerrótales y recupera mis gafas.\aCuando las encuentres, tráemelas y te daré una recompensa."

QuestScript145_1 = "I see you had no problem with the trolley!\aListen, the Cogs have stolen our blackboard eraser.\aGo into the streets and fight Cogs until you recover the eraser.\aTo reach the streets go through one of the tunnels like this:"
QuestScript145_2 = "When you find our eraser, bring it back here.\aDon't forget, if you need gags, ride the trolley.\aAlso, if you need to recover Laff Points, collect ice cream cones in the Playground."

QuestScript150_1 = "Oh... ¡Es posible que la tarea siguiente sea demasiado difícil para que la hagas solo!"
QuestScript150_2 = "Para hacerte amigo de alguien, busca a otro jugador y pulsa el botón Amigo nuevo."
QuestScript150_3 = "Cuando tengas un amigo nuevo, vuelve aquí."
QuestScript150_4 = "¡Algunas tareas son demasiado difíciles para hacerlas solo!"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignore me"

BossCogName = "VIP mayor."
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "Os declaro ascendidos a %s hechos y derechos. ¡Enhorabuena!"
BossCogDoobersAway = { 's' : "¡Adiós! ¡Y a cerrar ventas!" }
BossCogWelcomeToons = "¡Bienvenidos, bots nuevos!"
BossCogPromoteToons = "Os declaro ascendidos a %s hechos y derechos. Enhora--"
CagedToonInterruptBoss = "¡Eh! ¡Oye! ¡Oye, aquí!"
CagedToonRescueQuery = "¡Eh, dibus! ¿Habéis venido a rescatarme?"
BossCogDiscoverToons = "¿Cómo? ¡Dibus disfrazados!"
BossCogAttackToons = "¡Al ataque!"
CagedToonDrop = [
    "¡Muy bien! ¡Estáis a punto de acabar con él!",
    "¡Seguidlo! ¡Que se da a la fuga!",
    "¡Sois estupendos!",
    "¡Así, así! ¡Ya es prácticamente vuestro!",
    ]
CagedToonPrepareBattleTwo = "¡Cuidado, que se escapa!\aAyudadme todos: ¡subid y detenedlo!"
CagedToonPrepareBattleThree = "¡Yupii, ya me estoy viendo libre!\aAhora ataca al bot VIP directamente.\aTengo aquí un montón de tartas que puedes lanzarle.\aSalta y toca la base de la jaula para que te las dé.\aPulsa la tecla Insertar para lanzar las tartas una vez que las tengas."
BossBattleNeedMorePies = "¡Necesitas más tartas!"
BossBattleHowToGetPies = "Salta para tocar la jaula y conseguir tartas."
BossBattleHowToThrowPies = "Pulsa la tecla Insertar para lanzar las tartas!"
CagedToonYippee = "¡Hurra!"
CagedToonThankYou = "¡Por fin libre!\a¡Muchísimas gracias por tu ayuda!\aEstoy en deuda contigo.\aSi alguna vez necesitas que te eche una mano luchando, no dudes en llamarme con el botón SOS."
CagedToonPromotion = "\a¡Eh! Ese bot VIP se ha dejado los documentos de tu ascenso.\aLos archivaré a la salida para que no te quedes sin el ascenso."
CagedToonLastPromotion = "\¡Hala!, has alcanzado el nivel %s de traje bot.\aEs el máximo en la escala de ascensos bot.\aYa no puedes seguir mejorando el traje, pero sí que puedes seguir rescatando dibus."
CagedToonHPBoost = "\aHas rescatado a un montón de dibus de este cuartel general.\aEl Consejo Dibu ha decidido darte otro punto de risa. ¡Enhorabuena!"
CagedToonMaxed = "\aVeo que tienes un traje bot del nivel %s. Estamos muy impresionados.\aEn nombre del Consejo Dibu, te damos las gracias por regresar para rescatar más dibus."
CagedToonGoodbye = "¡Nos vemos!"


CagedToonBattleThree = {
    10: "¡Qué salto, %(toon)s! Aquí tienes las tartas.",
    11: "¡Hola, %(toon)s! Ahí van las tartas.",
    12: "¡Oye, %(toon)s! Mira la de tartas que tienes ahora.",

    20: "¡Oye, %(toon)s! Salta a la jaula que te doy unas tartitas para que las tires.",
    21: "¡Hola, %(toon)s! Dale a la tecla Ctrl para saltar y tocar la jaula.",

    100: "Pulsa la tecla Insertar para lanzar las tartas.",
    101: "El contador azul indica a qué altura llegará la tarta.",
    102: "Primero, intenta colarle una tarta dentro del mecanismo de las piernas para bloquearlo.",
    103: "Espera a que se abra la puerta y lanza la tarta por el hueco.",
    104: "Cuando esté mareado, túmbalo dándole en la cara o el pecho.",
    105: "Si la tarta salpica en colores, es que el tiro ha sido perfecto.",
    106: "Si le das a un dibu con una tarta, recibirá un punto de risa.",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

BossElevatorRejectMessage = "No puedes montarte en este ascensor hasta que no te merezcas un ascenso."

# Types of catalog items
FurnitureTypeName = "Mueble"
PaintingTypeName = "Cuadro"
ClothingTypeName = "Ropa"
ChatTypeName = "Frase de Charla rápida"
EmoteTypeName = "Clases de teatro"
PoleTypeName = "Caña de pescar"
WindowViewTypeName = "Vista desde la ventana"

FurnitureYourOldCloset = "tu antiguo armario"
FurnitureYourOldBank = "tu antigua hucha"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py
FurnitureNames = {
  100 : "Sillón",
  110 : "Silla",
  120 : "Silla de escritorio",
  130 : "Silla de troncos",
  140 : "Silla de langosta",
  145 : "Silla de chaleco salvavidas",
  150 : "Saddle Stool",
  200 : "Cama",
  210 : "Cama",
  220 : "Cama de bañera",
  230 : "Cama de hoja",
  240 : "Cama de barco",
  250 : "Cactus Hammock",
  300 : "Pianola",
  310 : "Órgano de iglesia",
  400 : "Chimenea",
  410 : "Chimenea",
  420 : "Chimenea redonda",
  430 : "Chimenea",
  500 : "Armario",
  502 : "Armario con 15 prendas",
  510 : "Armario",
  512 : "Armario con 15 prendas",
  600 : "Lámpara baja",
  610 : "Lámpara alta",
  620 : "Lámpara de mesa",
  630 : "Lámpara de Daisy?",
  640 : "Lámpara de Daisy?",
  650 : "Lámpara de medusa",
  660 : "Lámpara de medusa",
  700 : "Butaca",
  710 : "Sofá",
  720 : "Hay Couch",
  800 : "Escritorio",
  810 : "Escritorio de troncos",
  900 : "Paragüero",
  910 : "Perchero",
  920 : "Cubo de basura",
  930 : "Taburete rojo",
  940 : "Taburete amarillo",
  950 : "Perchero",
  960 : "Barrel Stand",
  970 : "Cactus",
  1000 : "Alfombra grande",
  1010 : "Alfombra redonda",
  1020 : "Alfombra pequeña",
  1030 : "Felpudo de hoja",
  1100 : "Vitrina",
  1110 : "Vitrina",
  1120 : "Estantería alta",
  1130 : "Estantería baja",
  1200 : "Mesita lateral",
  1210 : "Mesita",
  1220 : "Mesa de centro",
  1230 : "Mesa de centro",
  1240 : "Mesa de buceador",
  1300 : "Hucha para 1.000 gominolas",
  1310 : "Hucha para 2.500 gominolas",
  1320 : "Hucha para 5.000 gominolas",
  1399 : "Teléfono",
  1400 : "Dibu Cezanne",
  1410 : "Flores",
  1420 : "Mickey moderno",
  1430 : "Dibu Rembrandt",
  1440 : "Paisaje dibu",
  1441 : "Escena hípica",
  1442 : "Estrella dibu",
  1443 : "¿No es una tarta?",
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
  1700 : "Carrito de palomitas",
  1710 : "Mariquita",
  1720 : "Fuente",
  1725 : "Lavadora",
  1800 : "Pecera",
  1810 : "Pecera",
  1900 : "Pez espada",
  1910 : "Pez martillo",
  1920 : "Hanging Horns",
  1930 : "Simple Sombrero",
  1940 : "Fancy Sombrero",
  10000 : "Calabaza pequeña",
  10010 : "Calabaza alargada",
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
    1400 : "Matthew's Shirt",
    1401 : "Jessica's Shirt",
    1402 : "Marissa's Shirt",
    }

# CatalogSurfaceItem.py
SurfaceNames = (
    "Papel pintado",
    "Moldura",
    "Suelo",
    "Revestimiento de pared",
    "Cenefa",
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
    10100 : "Gatos",
    10200 : "Murciélagos",
    11000 : "Copos de nieve",
    11100 : "Hoja de acebo",
    11200 : "Muñeco de nieve",
    13000 : "Trébol",
    13100 : "Trébol",
    13200 : "Arco iris",
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
    1130 : "Nido de abeja",
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
    }

NewCatalogNotify = "Han llegado artículos nuevos que puedes pedir llamando desde tu teléfono."
NewDeliveryNotify = "Te acaba de llegar un pedido al buzón."
CatalogNotifyFirstCatalog = "¡Te ha llegado el primer catálogo Tolón-tolón! Lo puedes usar para hacer pedidos de artículos nuevos para ti o para la casa."
CatalogNotifyNewCatalog = "¡Te ha llegado el catálogo Tolón-tolón nº #%s! Haz pedidos llamando desde tu teléfono."
CatalogNotifyNewCatalogNewDelivery = "Te acaba de llegar un pedido al buzón. También ha llegado el catálogo Tolón-tolón nº #%s."
CatalogNotifyNewDelivery = "Te acaba de llegar un pedido al buzón."
CatalogNotifyNewCatalogOldDelivery = "Te ha llegado el catálogo Tolón-tolón nº #%s, pero todavía tienes pedidos en el buzón esperando a que los recojas."
CatalogNotifyOldDelivery = "Todavía tienes pedidos en el buzón esperando a que los recojas."
CatalogNotifyInstructions = "Haz clic en el botón \"Ir a casa\" de la página del libro de pegatinas donde aparece el plano y vete al teléfono de tu casa."
CatalogNewDeliveryButton = "¡Nueva\nentrega!"
CatalogNewCatalogButton = "¡Nuevo\ncatálogo Tolón-tolón!"

DistributedMailboxEmpty = "El buzón está vacío. Vuelve después de haber hecho pedidos por teléfono para recogerlos."
DistributedMailboxWaiting = "El buzón está vacío, pero el pedido que hiciste ya está de camino. Vuelve más tarde."
DistributedMailboxReady = "¡Te ha llegado el pedido!"
DistributedMailboxNotOwner = "Me temo que éste no es tu buzón."
DistributedPhoneEmpty = "Puedes pedir artículos especiales para ti o para la casa desde cualquier teléfono. Cada cierto tiempo irán apareciendo artículos nuevos para pedir.\n\nAhora mismo no puedes pedir ningún artículo. Vuelve a intentarlo más tarde."

Clarabelle = "Clarabella"
MailboxExitButton = "Cerrar buzón"
MailboxAcceptButton = "Recoger este artículo"
MailboxOneItem = "Tienes 1 artículo en el buzón."
MailboxNumberOfItems = "Tienes %s artículos en el buzón."
MailboxGettingItem = "Recogiendo %s del buzón."
MailboxItemNext = "Artículo\nsiguiente"
MailboxItemPrev = "Artículo\nanterior"
CatalogCurrency = "gominolas"
CatalogHangUp = "Colgar"
CatalogNew = "NUEVO"
CatalogBackorder = "PEDIDO PENDIENTE"
CatalogPagePrefix = "Página"
CatalogGreeting = "¡Buenas! Gracias por llamar al catálogo Tolón-tolón de Clarabella. ¿Qué deseas?"
CatalogGoodbyeList = ["¡Adiós!",
                      "Esperamos tu próxima llamada.",
                      "Gracias por llamarnos.",
                      "Muy bien. Hasta luego.",
                      "¡Adiós!",
                      ]
CatalogHelpText1 = "Pasa la página para ver los artículos que están a la venta."
CatalogSeriesLabel = "Serie %s"
CatalogPurchaseItemAvailable = "¡Que disfrutes de tu compra!  Puedes empezar a usarla ahora mismo."
CatalogPurchaseItemOnOrder = "Muy bien. En breve enviaremos tu compra al buzón."
CatalogAnythingElse = "¿Quieres alguna otra cosa?"
CatalogPurchaseClosetFull = "Tienes el armario lleno. Puedes comprar esta prenda, pero tendrás que deshacerte de otra del armario para poder meterla cuando la recibas.\n\n¿Seguro que quieres comprarla?"
CatalogAcceptClosetFull = "Tienes el armario lleno. Antes de recoger este artículo del buzón tendrás que abrirlo y deshacerte de una de las prendas para que quepa la nueva."
CatalogAcceptShirt = "Llevas una camisa nueva. La que llevabas antes está ahora en tu armario."
CatalogAcceptShorts = "Llevas un pantalón corto nuevo. Lo que llevabas antes está ahora en tu armario."
CatalogAcceptSkirt = "Llevas una falda nueva. Lo que llevabas antes está ahora en tu armario."
CatalogAcceptPole = "Ahora, con tu caña nueva ya puedes pescar a lo grande."
CatalogAcceptPoleUnneeded = "La caña de pescar que tienes es mejor que ésta."
CatalogPurchaseHouseFull = "Tienes la casa llena. Puedes comprar este artículo, pero tendrás que deshacerte de otro de la casa para poder meterlo cuando lo recibas.\n\n¿Seguro que quieres comprarlo?"
CatalogAcceptHouseFull = "Tienes la casa llena. Antes de recoger este artículo del buzón tendrás que entrar en la casa y deshacerte de uno de los artículos para que quepa el nuevo."
CatalogAcceptInAttic = "El artículo recién adquirido está en el desván de tu casa. Para colocarlo en la casa, entra y dale al botón \"Cambiar mobiliario de sitio\"."
CatalogAcceptInAtticP = "Los artículos recién adquiridos están en el desván de tu casa. Para colocarlos en la casa, entra y dale al botón \"Cambiar mobiliario de sitio\"."
CatalogPurchaseMailboxFull = "¡Tienes el buzón lleno! No puedes comprar este artículo hasta que no saques algo del buzón para dejar hueco."
CatalogPurchaseOnOrderListFull = "Ya has pedido muchos artículos. No puedes pedir más hasta que no te lleguen los que están pendientes de entrega."
CatalogPurchaseGeneralError = "No has podido comprar el artículo debido a un error interno del juego: código de error %s."
CatalogAcceptGeneralError = "No se ha podido sacar el artículo del buzón debido a un error interno del juego: código de error %s."

HDMoveFurnitureButton = "Cambiar\nmobiliario\nde sitio"
HDStopMoveFurnitureButton = "Mobiliario\ncambiado"
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
HDDeleteItem = "Haz clic en Aceptar para tirar este artículo a la basura, o en Cancelar para no tirarlo."
HDNonDeletableItem = "No puedes deshacerte de este tipo de artículo."
HDNonDeletableBank = "No puedes deshacerte de la hucha."
HDNonDeletableCloset = "No puedes deshacerte del armario."
HDNonDeletablePhone = "No puedes deshacerte del teléfono."
HDNonDeletableNotOwner = "No puedes deshacerte de las cosas de %s."
HDHouseFull = "Tienes la casa llena. Antes de rescatar este artículo de la basura tendrás que deshacerte de otra cosa de la casa o el desván."

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



MessagePickerTitle = "Tienes demasiadas frases. Si quieres comprar \n\"%s\"\n debes elegir una para borrarla:"
MessagePickerCancel = "Cancelar"
MessageConfirmDelete = "¿Seguro que quieres borrar \"%s\" del menú de Charla rápida?"


CatalogBuyText = "Comprar"
CatalogOnOrderText = "Ya pedido"
CatalogPurchasedText = "Ya comprado"
CatalogPurchasedMaxText = "Máximo permitido\nya comprado"
CatalogVerifyPurchase = "¿Quieres comprar %(item)s por %(price)s gominolas?"
CatalogOnlyOnePurchase = "Sólo puedes tener uno de estos artículos a la vez. Si compras éste, sustituirá a %(old)s.\n\n¿Seguro que quieres comprar %(item)s por %(price)s gominolas?"

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
    1000 : "Cuartel General Dibu",
    20001 : Flippy,

    # Toontown Central Fisherman
    # Toontown Central
    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "Pecunio el banquero",
    2003 : "Pedro el maestro",
    2004 : "Calixta la modista",
    2005 : "Leopoldo el bibliotecario",
    2006 : "Dependiente Vicente",
    2011 : "Dependienta Vicenta",
    2007 : "Funcionario del cuartel general",
    2008 : "Funcionario del cuartel general",
    2009 : "Funcionaria del cuartel general",
    2010 : "Funcionaria del cuartel general",
    # NPCFisherman
    2012 : "Dependiente de la tienda de animales",

    # Silly Street
    2101 : "Bautista el dentista",
    2102 : "Lucía la policía",
    2103 : "Camaleón Atuéndez",
    2104 : "Funcionario del cuartel general",
    2105 : "Funcionario del cuartel general",
    2106 : "Funcionaria del cuartel general",
    2107 : "Funcionaria del cuartel general",
    2108 : "Fagucia Carasucia",
    2109 : "Burbujo Irujo",
    2110 : "Óscar Tel",
    2111 : "Agustín el bailarín",
    2112 : "Dr. Tomás",
    2113 : "El increíble Esnafro",
    2114 : "Chiquito Lepero",
    2115 : "Flexia Papírez",
    2116 : "Pepe Puños",
    2117 : "Facta Putre ",
    2118 : "Inocencio Santos",
    2119 : "Hilaria Jajá",
    2120 : "Profesor Nino",
    2121 : "Sra. Orni Mans",
    2122 : "Orán Guto",
    2123 : "Marivi Guasona",
    2124 : "Bromi Stilla",
    2125 : "Morgan Dul",
    2126 : "Profesor Carcajada",
    2127 : "Mauro Euro",
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

    # Loopy Lane
    2201 : "Pepe el cartero",
    2202 : "Jocosa Risa",
    2203 : "Funcionario del cuartel general",
    2204 : "Funcionario del cuartel general",
    2205 : "Funcionaria del cuartel general",
    2206 : "Funcionaria del cuartel general",
    2207 : "Cholo Calandracas",
    2208 : "Luisillo Pegajosillo",
    2209 : "Chancho La Monda",
    2210 : "Pirulí",
    2211 : "Carca Ajada ",
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

    # Punchline Place
    2301 : "Dr. Tronchaespinazo",
    2302 : "Profesor Cosquillas",
    2303 : "Enfermera Mondi",
    2304 : "Funcionario del cuartel general",
    2305 : "Funcionario del cuartel general",
    2306 : "Funcionaria del cuartel general",
    2307 : "Funcionaria del cuartel general",
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

    # Donald's Dock
    1001 : "Dependiente Pipe",
    1002 : "Dependiente Pape",
    1003 : "Funcionario del cuartel general",
    1004 : "Funcionaria del cuartel general",
    1005 : "Funcionario del cuartel general",
    1006 : "Funcionaria del cuartel general",
    1007 : "Fifo Pretaporter",
    1008 : "Pet Shop Clerk",

    # Barnacle Blvd.
    1101 : "Beto Buque",
    1102 : "Capitán Doblón",
    1103 : "Raspo Espínez",
    1104 : "Dr. Rompecubiertas",
    1105 : "Almirante Garfio",
    1106 : "Sra. Almidónez",
    1107 : "Nemo Mancuerna",
    1108 : "Funcionario del cuartel general",
    1109 : "Funcionaria del cuartel general",
    1110 : "Funcionario del cuartel general",
    1111 : "Funcionaria del cuartel general",
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

    # Seaweed Street
    1201 : "Perci Percebe",
    1202 : "Pasma Rote",
    1203 : "Ajab",
    1204 : "Claus Anclas",
    1205 : "Funcionario del cuartel general",
    1206 : "Funcionaria del cuartel general",
    1207 : "Funcionario del cuartel general",
    1208 : "Funcionaria del cuartel general",
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
    1221 : "Blasco Báñez",
    1222 : "Alberto Abordaje",
    1223 : "Sepio Calamárez",
    1224 : "Emilia Anguila",
    1225 : "Gonzo Friegacubiertas",
    1226 : "Izo Velamen",
    1227 : "Coral Bisturí",

    # Lighthouse Lane
    1301 : "Pepa Sastre",
    1302 : "Isidoro Subemástiles",
    1303 : "Clodovico Cromañón",
    1304 : "Santiaguiña Nécorez",
    1305 : "Funcionario del cuartel general",
    1306 : "Funcionaria del cuartel general",
    1307 : "Funcionario del cuartel general",
    1308 : "Funcionaria del cuartel general",
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

    # The Brrrgh
    3001 : "Adela Dita",
    3002 : "Funcionario del cuartel general",
    3003 : "Funcionaria del cuartel general",
    3004 : "Funcionario del cuartel general",
    3005 : "Funcionario del cuartel general",
    3006 : "Dependiente Poli",
    3007 : "Dependienta Pili",
    3008 : "Giorgio Armiño",
    # NPCFisherman
    3009 : "Dependiente de la tienda de animales",

    # Walrus Way
    3101 : "Juanjo Escárchez",
    3102 : "Tía Ritona",
    3103 : "Pepe Tundra",
    3104 : "Geli da Pinto",
    3105 : "Pipe Pelado",
    3106 : "Frigo Sabañón",
    3107 : "Maite Aterida",
    3108 : "Doroteo Escarcha",
    3109 : "Pati",
    3110 : "Lucas Friolero",
    3111 : "Kevin Kelvin",
    3112 : "Fredo Dedo",
    3113 : "Cris Térico",
    3114 : "Beto Tomba",
    3115 : "Funcionario del cuartel general",
    3116 : "Funcionaria del cuartel general",
    3117 : "Funcionario del cuartel general",
    3118 : "Funcionario del cuartel general",
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
    3129 : "Dina Frigomiga",
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
    3211 : "Pega Moide",
    3212 : "Federico Gelado",
    3213 : "Funcionario del cuartel general",
    3214 : "Funcionaria del cuartel general",
    3215 : "Funcionario del cuartel general",
    3216 : "Funcionario del cuartel general",
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

    # Minnie's Melody Land
    4001 : "Moli Melódica",
    4002 : "Funcionario del cuartel general",
    4003 : "Funcionaria del cuartel general",
    4004 : "Funcionaria del cuartel general",
    4005 : "Funcionaria del cuartel general",
    4006 : "Dependienta Dina",
    4007 : "Dependiente Dino",
    4008 : "Modista Armonía",
    4009 : "Dependiente de la tienda de animales",

    # Alto Ave.
    4101 : "Ropo Pompom",
    4102 : "Bibi",
    4103 : "Dr. Pavo Rotti",
    4104 : "Funcionario del cuartel general",
    4105 : "Funcionaria del cuartel general",
    4106 : "Funcionaria del cuartel general",
    4107 : "Funcionaria del cuartel general",
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
    4125 : "Clinia Eastwood",
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
    4137 : "Roy Bate",
    4138 : "Octavo Seisillo",
    4139 : "Ada Gio",
    4140 : "Trémolo Torpe",

    # Baritone Blvd.
    4201 : "Tina Sonatina",
    4202 : "Barbo",
    4203 : "Chopo Chopín",
    4204 : "Funcionario del cuartel general",
    4205 : "Funcionaria del cuartel general",
    4206 : "Funcionaria del cuartel general",
    4207 : "Funcionaria del cuartel general",
    4208 : "Lírica Tástrofe",
    4209 : "Sissy de Triana",
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

    # Tenor Terrace
    4301 : "Uki",
    4302 : "Juanola",
    4303 : "Leo",
    4304 : "Funcionario del cuartel general",
    4305 : "Funcionaria del cuartel general",
    4306 : "Funcionaria del cuartel general",
    4307 : "Funcionaria del cuartel general",
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

    # Daisy Gardens
    5001 : "Funcionario del cuartel general",
    5002 : "Funcionario del cuartel general",
    5003 : "Funcionaria del cuartel general",
    5004 : "Funcionaria del cuartel general",
    5005 : "Dependienta Azucena",
    5006 : "Dependiente Jacinto",
    5007 : "Florinda Rosales",
    5008 : "Dependiente de la tienda de animales",

    # Elm Street
    5101 : "Pepe Pino",
    5102 : "Alca Chofa",
    5103 : "Federico Tilla",
    5104 : "Polillo Maripósez",
    5105 : "Comino Pérez Gil",
    5106 : "Patillo Siegacogotes",
    5107 : "Cartero Felipe",
    5108 : "Posadera Piti",
    5109 : "Funcionario del cuartel general",
    5110 : "Funcionario del cuartel general",
    5111 : "Funcionaria del cuartel general",
    5112 : "Funcionaria del cuartel general",
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

    # Maple Street
    5201 : "Pulgarcillo",
    5202 : "Edel Weiss",
    5203 : "Campanilla",
    5204 : "Pipe Barroso",
    5205 : "León Mondadientes",
    5206 : "Cardo Borriquero",
    5207 : "Flor Chorro",
    5208 : "Lisa Buesa",
    5209 : "Funcionario del cuartel general",
    5210 : "Funcionario del cuartel general",
    5211 : "Funcionaria del cuartel general",
    5212 : "Funcionaria del cuartel general",
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

    # Oak street
    5301 : "Funcionario del cuartel general",
    5302 : "Funcionario del cuartel general",
    5303 : "Funcionario del cuartel general",
    5304 : "Funcionario del cuartel general",
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

    # Dreamland
    9001 : "Belinda Traspuesta",
    9002 : "Bello Durmiente",
    9003 : "Plancho Rejas",
    9004 : "Funcionaria del cuartel general",
    9005 : "Funcionaria del cuartel general",
    9006 : "Funcionario del cuartel general",
    9007 : "Funcionario del cuartel general",
    9008 : "Dependienta Modorra",
    9009 : "Dependiente Modorro",
    9010 : "Almohado Edredón",
    9011 : "Dependiente de la tienda de animales",

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
    9111 : "Apagón Plómez",
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

    9132 : "Funcionaria del cuartel general",
    9133 : "Funcionaria del cuartel general",
    9134 : "Funcionaria del cuartel general",
    9135 : "Funcionaria del cuartel general",

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
    2520 : ("Cuartel General Dibu", "el"),
    2521 : ("Tienda de Ropa de Toontown", "la"),
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
    2655 : ("Caja de Ahorros Pastagansa", "la"),
    2656 : ("Coches Usados de Payasos", "los"),
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
    2671 : ("Cuartel General Dibu", "el"),
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
    2729 : ("Peces Dorados de 14 Kilates", "los"),
    2730 : ("Noticias Jocosas", "las"),
    2731 : ("", ""),
    2732 : ("Pasta Pánfilo", "la"),
    2733 : ("Cometas de Plomo", "los"),
    2734 : ("Platillos y Ventosas", "los"),
    2735 : ("Detonaciones a Domicilio", "las"),
    2739 : ("Reparación de Chistes", "las"),
    2740 : ("Petardos Usados", "los"),
    2741 : ("", ""),
    2742 : ("Cuartel General Dibu", "el"),
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
    2814 : ("Un Dia De Atasco", ""),
    2818 : ("Tartas Volantes", "las"),
    2821 : ("", ""),
    2822 : ("Sándwiches de Pollo de Goma", "los"),
    2823 : ("Heladería El Cucurucho Agudo", "la"),
    2824 : ("Las Locuras De Mickey", ""),
    2829 : ("Salchichones y Chichones", "los"),
    2830 : ("Melodías de Zipi", "las"),
    2831 : ("Casa de las Risillas del Profesor Cosquillas", "la"),
    2832 : ("Cuartel General Dibu", "el"),
    2833 : ("", ""),
    2834 : ("Sala de Traumatología del Hueso de la Risa", "la"),
    2836 : ("", ""),
    2837 : ("Seminarios Sobre Risa Persistente", "los"),
    2839 : ("Pasta Pastosa", "la"),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : ("Tienda de Bromas", "la"),
    1507 : ("Cuartel General Dibu", "el"),
    1508 : ("Tienda de Ropa", "la"),
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
    1629 : ("Cuartel General Dibu", "el"),
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
    1729 : ("Cuartel General Dibu", "el"),
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
    1821 : ("Fábrica de Conservas Dibuque", "la"),
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
    1835 : ("Cuartel General Dibu", "el"),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : ("Tienda de Bromas", "la"),
    4504 : ("Cuartel General Dibu", "el"),
    4506 : ("Tienda de Ropa de Toontown", "la"),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("Tambores Ropopompom", "los"),
    4604 : ("Compás de Dos por Cuatro", "el"),
    4605 : ("Violines Bibi", "los"),
    4606 : ("Casa de las Castañuelas", "la"),
    4607 : ("Dibumoda Septiminod", "la"),
    4609 : ("Teclas de Piano Dorremí", "las"),
    4610 : ("No Pierdan los Estribillos", ""),
    4611 : ("A Bombo y Platillos Volantes", ""),
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
    4659 : ("Cuartel General Dibu", "el"),
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
    4717 : ("Seguros de Coches Un Acordeón en la Guantera", "los"),
    4718 : ("Utensilios de Cocina Cascanueces", "los"),
    4719 : ("Caravanas Madrigal", "las"),
    4720 : ("Tararea esa Dibucanción", "la"),
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
    4739 : ("Cuartel General Dibu", "el"),
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
    4873 : ("Cuartel General Dibu", "el"),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : ("Tienda de Bromas", "la"),
    5502 : ("Cuartel General Dibu", "el"),
    5503 : ("Tienda de Ropa", "la"),
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
    5615 : ("Semillas para Cotillas", "las"),
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
    5627 : ("Cuartel General Dibu", "el"),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("Espinacas de Diseño", "las"),
    5702 : ("Rastrillos Miga de Pan", "los"),
    5703 : ("Fotografía La Flor de un Día", "la"),
    5704 : ("Coches Usados Campanilla", "los"),
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
    5728 : ("Cuartel General Dibu", "el"),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : ("Cuartel General Dibu", "el"),
    5804 : ("Just Vase It", ""),
    5805 : ("Snail Mail", ""),
    5809 : ("Fungi Clown School", ""),
    5810 : ("Honeydew This", ""),
    5811 : ("Lettuce Inn", ""),
    5815 : ("Grass Roots", ""),
    5817 : ("Apples and Oranges", ""),
    5819 : ("Green Bean Jeans", ""),
    5821 : ("Squash and Stretch Gym", ""),
    5826 : ("Ant Farming Supplies", ""),
    5827 : ("Dirt. Cheap.", ""),
    5828 : ("Couch Potato Furniture", ""),
    5830 : ("Spill the Beans", ""),
    5833 : ("The Salad Bar", ""),
    5835 : ("Flower Bed and Breakfast", ""),
    5836 : ("April’s Showers and Tubs", ""),
    5837 : ("School of Vine Arts", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("Biblioteca Sobetotal", "la"),
    9503 : ("Bar La Cabezadita Tonta", "el"),
    9504 : ("Tienda de Bromas", "la"),
    9505 : ("Cuartel General Dibu", "el"),
    9506 : ("Tienda de Ropa de Toontown", "la"),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("Posada Pluma de Ganso", "la"),
    9602 : ("Siestas a Domicilio", "las"),
    9604 : ("Fundas Nórdicas para Pinreles", "las"),
    9605 : ("Avenida de la Canción de Cuna, 323", "la"),
    9607 : ("Pijamas de Plomo para Dormir de Pie", "el"),
    9608 : ("", ""),
    9609 : ("Arrullos a Granel", "los"),
    9613 : ("Los Limpiadores Del Reloj", ""),
    9616 : ("Compañía Eléctrica Luces Fuera", "la"),
    9617 : ("Avenida de la Canción de Cuna, 212", "la"),
    9619 : ("Sopas Soporíferas", "las"),
    9620 : ("Servicio de Taxis Insomnes", "el"),
    9622 : ("Relojería El Cuco Dormido", "la"),
    9625 : ("Salón de Belleza El Ronquido Alegre", "el"),
    9626 : ("Avenida de la Canción de Cuna, 818", "la"),
    9627 : ("Mecedoras Automáticas", "las"),
    9628 : ("Calendarios Nocturnos", "los"),
    9629 : ("Avenida de la Canción de Cuna, 310", "la"),
    9630 : ("Serrería Como un Tronco", "la"),
    9631 : ("Arreglo de Relojes Estoysopa", "el"),
    9633 : ("La Siesta De Pluto", ""),
    9634 : ("Colchones La Pluma Audaz", "los"),
    9636 : ("Seguro Contra Insomnios", "el"),
    9639 : ("Conservas Ultrahibernadas", "las"),
    9640 : ("Avenida de la Canción de Cuna, 805", "la"),
    9642 : ("Ganadería Cuentaovejas", "la"),
    9643 : ("Óptica Nopegojo", "la"),
    9644 : ("Peleas de Almohadas Organizadas", "las"),
    9645 : ("Posada Todos al Sobre", "la"),
    9647 : ("¡Hazte la cama! Ferretería", ""),
    9649 : ("Ronquidos Lejanos", "los"),
    9650 : ("Avenida de la Canción de Cuna, 714", "la"),
    9651 : ("Martillos para Despertadores", "los"),
    9652 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : ("Tienda de Bromas", "la"),
    3508 : ("Cuartel General Dibu", "el"),
    3509 : ("Tienda de Ropa", "la"),
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
    3624 : ("Bocadillos Bajocero", "los"),
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
    3651 : ("Perritos Helados Pipe", "los"),
    3653 : ("Joyería Frío como el Diamante", "la"),
    3654 : ("Cuartel General Dibu", "el"),
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
    3739 : ("Cuartel General Dibu", "el"),
    }

# DistributedCloset.py
ClosetTimeoutMessage = "Lo siento, el tiempo se\n te ha acabado."
ClosetNotOwnerMessage = "Este no es tu clóset, pero te puedes probar la ropa."
ClosetPopupOK = "Muy bien"
ClosetPopupCancel = "Cancelar"
ClosetDiscardButton = "Remover"
ClosetAreYouSureMessage = "Tú has borrado algunas prendas. ¿Realmente quieres borrarlas?"
ClosetYes = "Sí"
ClosetNo = "No"
ClosetVerifyDelete = "Borrar %s?"
ClosetShirt = "Esta camiseta"
ClosetShorts = "Estos shorts"
ClosetSkirt = "Esta falda"
ClosetDeleteShirt = "Borrar\ncamiseta"
ClosetDeleteShorts = "Borrar\nshorts"
ClosetDeleteSkirt = "Borrar\nfalda"

# EstateLoader.py
EstateOwnerLeftMessage = "Lo siento, el dueño de esta propiedad se ha ido.  Tú vas a ser enviado al dibuparque en %s segundos"
EstatePopupOK = "Muy bien"
EstateTeleportFailed = "No pude irme a la casa. ¡Trata de nuevo!"
EstateTeleportFailedNotFriends = "Lo siento, %s esta en una propiedad en la cual tú no tienes amigos."

# DistributedHouse.py
AvatarsHouse = "Casa %s"

# BankGui.py
BankGuiCancel = "Cancelar"
BankGuiOk = "Aceptar"

# DistributedBank.py
DistributedBankNoOwner = "Lo siento, este no es tú banco."
DistributedBankNotOwner = "Lo siento, este no es tú banco."

# FishSellGui.py
FishGuiCancel = "Cancelar"
FishGuiOk = "Vender todo"
FishTankValue = "¡Hola, %(name)s! En el cubo llevas %(num)s peces, que tienen un valor total de %(value)s gominolas. ¿Quieres venderlos todos?"

def GetPossesive(name):
    if name[-1:] == 's':
        possesive = name + "'"
    else:
        possesive = name + "'s"
    return possesive

# end translate

# DistributedFireworkShow.py
FireworksInstructions = "Cuartel general: Para ver mejor, pulsa la tecla \"Re Pág\". "

FireworksJuly4Beginning = "Cuartel general: ¡Bienvenido a los fuegos artificiales de verano! ¡Disfruta del espectáculo!"
FireworksJuly4Ending = "Cuartel general: ¡Esperamos que te haya gustado! ¡Que pases un verano estupendo!"
FireworksNewYearsEveBeginning = "Cuartel general: ¡Feliz Año! ¡Bienvenido a los fuegos artificiales del año nuevo! ¡Disfruta del espectáculo!"
FireworksNewYearsEveEnding = "Cuartel general: ¡Esperamos que te haya gustado! ¡Feliz Año 2005!"
FireworksBeginning = "Cuartel general: ¡Feliz Año! ¡Bienvenido a los fuegos artificiales del año nuevo! ¡Disfruta del espectáculo!"
FireworksEnding = "Cuartel general: ¡Esperamos que te haya gustado! ¡Feliz Año 2005!"

# ToontownLoadingScreen.py

TIP_NONE = 0
TIP_GENERAL = 1
TIP_STREET = 2
TIP_MINIGAME = 3
TIP_COGHQ = 4

# As of 8/5/03, ToonTips shouldn't exceed 130 characters in length
TipTitle = "UN DIBUCONSEJO:"
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "Para comprobar rápidamente el estado de tu dibutarea, pulsa la tecla \"Fin\".",
    "Para echar un vistazo rápido a tu página de bromas, pulsa la tecla la tecla \"Inicio\".",
    "Pulsa la tecla \"F7\" para abrir la Lista de amigos.",
    "Para abrir o cerrar el dibucuaderno, pulsa la tecla \"F8\".",
    "Para mirar hacia arriba, pulsa la tecla \"Re Pág\", y para mirar hacia abajo, pulsa la tecla \"Av Pág\".",
    "Pulsa la tecla \"Control\" para saltar.",
    "Si pulsas la tecla \"F9\", obtendrás una captura de pantalla que quedará almacenada en la carpeta Toontown de tu ordenador.",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "Puedes intercambiar códigos de Amigos secretos con personas que conozcas en la vida real para poder charlar con ellas en Toontown.",
    "En la página Opciones del dibucuaderno podrás cambiar la resolución de la pantalla, modificar el sonido y ajustar otras opciones.",
    "Pruébate la ropa de tus amigos en el armario de su casa.",
    "Para ir a tu casa, usa el botón \"Ir a casa\" del mapa.",
    "Cada vez que completes una dibutarea, tus puntos de risa se rellenarán automáticamente.",
    "Puedes examinar el surtido de las tiendas de ropa sin necesidad de tener un ticket de ropa.",
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
    "Algunas frases de Charla rápida hacen que tu dibu muestre emociones.",
    "Si la zona en la que estás está demasiado llena, trata de cambiar de distrito. Acude a la página de Distritos del dibucuaderno y selecciona otro distrito.",
    "Si recuperas edificios aparecerá una estrella de bronce, plata u oro sobre tu dibu.",
    "Si recuperas los edificios suficientes para conseguir que aparezca una estrella sobre tu cabeza, quizá veas tu nombre escrito en la pizarra de un cuartel general dibu.",
    "A veces, los bots vuelven a capturar edificios recuperados. ¡La única manera de conservar tu estrella consiste en ir a recuperar más edificios!",
    "Los nombres de tus amigos secretos aparecen en azul.",
    # Fishing
    "¡A ver si consigues pescar todos los peces de Toontown!",
    "Cada estanque tiene peces diferentes. ¡Prueba con todos!",
    "Cuando tengas el cubo lleno de peces, véndeselos al dependiente de la tienda de animales que hay en el dibuparque.",
    "Las cañas más resistentes sirven para pescar peces más gordos, pero para usarlas hay que gastar más gominolas.",
    "Puedes comprar cañas más resistentes en el Vacatálogo.",
    "Mientras más grande sean los peces, más gominolas te dará la tienda de animales por ellos.",
    "Mientras menos comunes sean los peces, más gominolas te dará la tienda de animales por ellos.",
    "A veces encontrarás bolsas de gominolas mientras pescas.",
    "En algunas dibutareas tendrás que pescar objetos en los estanques.",
    "Los estanques de los dibuparques tienen peces diferentes de los de los estanques de las calles.",
    "Algunos peces son muy raros. Mantente pescando hasta que los obtengas todos.",
    "El estanque de tu propiedad tiene peces que solo se encuentran allí.",
    "¡Por cada 10 especies que pesques conseguirás un trofeo de pesca!",
    "En el dibucuaderno podrás ver qué peces has pescado.",
    "Algunos trofeos de pesca te dan un aumento de risómetro.",
    "La pesca es un método estupendo para conseguir más gominolas.",
    ),

  TIP_STREET : (
    "Hay cuatro tipos de bots: Abogabots, chequebots, vendebots y jefebots.",
    "Cada circuito de bromas tiene diferentes cantidades de precisión y daños.",
    "Las bromas de sonido afectan a todos los bots, pero despiertan a los bots que siguen cebos.",
    "Derrota a los bots siguiendo un orden estratégico, aumentara tús posibilidades en ganar los combates.",
    "El circuito de broma curadibu te permite sanar a otros dibus durante los combates.",
    "¡Durante las invasiones de bots, los puntos de experiencia de bromas se duplican!",
    "Si formas un equipo con otros dibus y usas el mismo circuito de bromas en el combate, conseguirás una bonificación de daños a los bots.",
    "Las bromas se usan por orden, de arriba a abajo, según aparecen en el menú de bromas del combate.",

    "La fila de luces circulares que hay sobre los ascensores de los edificios bot muestra cuántos pisos tienen.",
    "Haz clic en un bot para ver más detalles sobre él.",
    "Si usas bromas de alto nivel contra bots de bajo nivel no conseguirás puntos de experiencia.",
    "Las bromas que te dan experiencia tienen un fondo azul en el menú de bromas del combate.",
    "La experiencia que te dan las bromas se multiplica en el interior de los edificios bot. Mientras más elevado sea el piso, mayor será el factor de multiplicación.",
    "Al ganar a un bot, todos los dibus que hayan participado conseguirán puntos cuando termine el combate.",
    "Todas las calles de Toontown tienen distintos tipos y niveles de bots.",
    "En las aceras estarás a salvo de los bots.",
    "En las calles, las puertas de las casas cuentan chistes cuando te acercas.",
    "Algunas dibutareas te proporcionan entrenamiento para nuevos circuitos de bromas. ¡Solo podrás escoger seis de los siete circuitos de bromas, así que elige con cuidado!",
    "Las trampas solo son útiles cuando tú coordines con tus amigos el uso de los cebos en el combate.",
    "Los cebos de alto nivel tienen menos posibilidades de fallar.",
    "Las bromas de bajo nivel tienen poca precisión contra los bots de alto nivel.",
    TheCogs+" no pueden atacar cuando han seguido un cebo en un combate.",
    "Cuando tus amigos y tú recuperen un edificio bot, ustedes serán recompensados con retratos dentro del edificio rescatado.",
    "Si usas una broma curadibu en un dibu que tenga el risómetro completo, no conseguirás experiencia de curadibu.",
    TheCogs+" quedarán aturdidos durante un instante al ser alcanzados por cualquier broma. Esto aumenta la probabilidad de que otras bromas los alcancen en la misma ronda.",
    "Las bromas de caída tienen menos probabilidad de alcanzar su objetivo, pero su precisión aumenta cuando el bot ha sido alcanzado antes por otra broma en la misma ronda.",
    "Cuando hayas derrotado suficientes bots, podrás usar el \"radar de bots\" haciendo clic en los iconos de bots de la página Galería de bots del dibucuaderno.",
    "Durante los combates podrás saber a qué bot tus compañeros de equipo están atacando, mirando a los guiones (-) y a las X.",
    "Durante los combates, los bots llevan una luz que indica su estado de salud: verde significa que está sano y rojo que casi está destruido.",
    "Solo pueden combatir a la vez un máximo de cuatro dibus.",
    "En la calle, los bots tienen más tendencia a luchar contra varios dibus que contra uno solo.",
    "Los últimos dos bots de cada tipo que son más difíciles de encontrar, los encuentrarás en el interior de los edificios.",
    "Las bromas de caída no funcionan contra los bots que siguen un cebo.",
    TheCogs+" tienden a atacar al dibu que les ha causado más daños.",
    "Las bromas de sonido no dan bonificación por daños contra los bots que siguen cebos.",
    "Si esperas demasiado para atacar a un bot que sigue un cebo, se despertará. Mientras mayor sea el nivel del cebo, mayor será su duración.",
    ),

  TIP_MINIGAME : (
     "Cuando tengas llena la jarra de gominolas, las que consigas en los Juegos del tranvía irán a parar directamente a tu banco.",
    "Puedes usar las teclas de flecha en lugar del ratón en el Juego del tranvía \"Imita a Minnie\".",
    "En el juego del cañón, usa las teclas de flecha para mover el cañón y pulsa la tecla \"Control\" para disparar.",
    "En el juego de los anillos, conseguirás puntos de bonificación cuando todo el grupo consiga atravesar sus anillos.",
    "Si juegas perfectamente a Imita a Minnie, duplicarás los puntos.",
    "En el juego de la cuerda, conseguirás más gominolas si te enfrentas a un bot más grande.",
    "La dificultad de los Juegos del tranvía varían según el barrio: En el Centro de Toontown están los más fáciles, y en Sueñolandia de Donald, los más difíciles.",
    "A algunos Juegos del tranvía solo se pueden jugar en grupo.",
   ),

  TIP_COGHQ : (
    "Antes de entrar en el edificio jefe debes acabar de reunir todo el disfraz de bot.",
    "Puedes saltar encima de los matones bots para dejarlos temporalmente incapacitados.",
    "Reúne méritos bot luchando contra bots y venciéndolos.",
    "Se te otorgarán más méritos si luchas contra bots de mayor nivel.",
    "Cuando reúnas los méritos bot necesarios para recibir un ascenso, vete a ver al VIP vendebot.",
    "Cuando llevas el disfraz de bot puedes hablar como uno de ellos.",
    "Hasta ocho dibus pueden unirse para luchar contra el VIP vendebot.",
    "El VIP vendebot está en el ático del cuartel general bot.",
    "Una vez dentro de las fábricas bot, sube las escaleras hasta llegar al capataz.",
    "A medida que luchas en la fábrica vas ganando piezas del disfraz bot.",
    "Puedes comprobar cuánto te falta para completar el disfraz bot con el libro de pegatinas.",
    "Puedes comprobar cuántos méritos llevas en la página del disfraz del libro de pegatinas.",
    "Antes de enfrentarte al VIP, comprueba que vas bien cargado de bromas y puntos de risa.",
    "El disfraz de bot irá cambiando a medida que  recibas ascensos.",
    "Debes derrotar al capataz de la fábrica para recuperar una pieza del disfraz de bot.",
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
          "Estrella marina de cinco puntas",
          "Estrella marina de rock",
          "Estrella marina del alba",
          "Estrella marina fugaz",
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
           "Principe Centollo",
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
           "Concord Grape PB&J Fish",
           ),
    34 : ( "Raya diablo",
          ),
    }

FishFirstNames = (
    "",
    "Anchoa",
    "Anguilo",
    "Anzuela",
    "Arenquilla",
    "Besuguete",
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
    "Trucho",
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
    "Bonito",
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
    "LagunaRojo",
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
    "Ria",
    "Ribera",
    "RocaSaludar",
    "Salta",
    "Sirena",
    "Vela",
    "Zambullida",
    )

FishLastSuffixNames = (
    "",
    "del norte",
    "del sur",
    "afilada",
    "ahumada",
    "apestosa",
    "arénquez",
    "atigrada",
    "azul",
    "besúguez",
    "blanca",
    "doble",
    "dorada",
    "fantasma",
    "fina",
    "fresca",
    "frita",
    "gállez",
    "gato",
    "gorda",
    "gris",
    "limón",
    "lubinez",
    "morada",
    "moteada",
    "naranja",
    "occidental",
    "oriental",
    "plana",
    "plateada",
    "profunda",
    "rraya",
    "rrayada",
    "rrodaballez",
    "rroja",
    "rrosa",
    "salada",
    "surfera",
    "tropical",
    "trúchez",
    "verde",
   )


CogPartNames = (
    "Muslo izquierdo ", "Pantorrilla izquierda", "Pie izquierdo",
    "Muslo derecho", "Pantorrilla derecha", "Pie derecho",
    "Hombro izquierdo",  "Hombro derecho", "Pecho", "Indicador de salud", "Caderas",
    "Brazo izquierdo",  "Antebrazo izquierdo", "Mano izquierda",
    "Brazo derecho", "Antebrazo derecho", "Mano derecha",
    )

CogPartNamesSimple = (
    "Torso superior",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "Entrada Principal"
SellbotLegFactorySpecLobby = "Vestíbulo"
SellbotLegFactorySpecLobbyHallway = "Entrada del Vestíbulo"
SellbotLegFactorySpecGearRoom = "Sala de Máquinas"
SellbotLegFactorySpecBoilerRoom = "Sala de Calderas"
SellbotLegFactorySpecEastCatwalk = "Pasarela Este"
SellbotLegFactorySpecPaintMixer = "Mezcladora de Pintura"
SellbotLegFactorySpecPaintMixerStorageRoom = "Sala de la Mezcladora de Pintura"
SellbotLegFactorySpecWestSiloCatwalk = "Pasarela del Silo Oeste"
SellbotLegFactorySpecPipeRoom = "Sala de Tuberías"
SellbotLegFactorySpecDuctRoom = "Sala de Conductos"
SellbotLegFactorySpecSideEntrance = "Entrada de Servicio"
SellbotLegFactorySpecStomperAlley = "Callejón del Pisotón"
SellbotLegFactorySpecLavaRoomFoyer = "Entrada a la Sala de la Lava"
SellbotLegFactorySpecLavaRoom = "Sala de la Lava"
SellbotLegFactorySpecLavaStorageRoom = "Sala donde se guarda la Lava"
SellbotLegFactorySpecWestCatwalk = "Pasarela Oeste"
SellbotLegFactorySpecOilRoom = "Sala del Aceite"
SellbotLegFactorySpecLookout = "Cabina de Vigilancia"
SellbotLegFactorySpecWarehouse = "Almacén"
SellbotLegFactorySpecOilRoomHallway = "Entrada a la Sala del Aceite"
SellbotLegFactorySpecEastSiloControlRoom = "Sala de Control del Silo Este"
SellbotLegFactorySpecWestSiloControlRoom = "Sala de Control del Silo Oeste"
SellbotLegFactorySpecCenterSiloControlRoom = "Sala de Control del Silo Central"
SellbotLegFactorySpecEastSilo = "Silo Este"
SellbotLegFactorySpecWestSilo = "Silo Oeste"
SellbotLegFactorySpecCenterSilo = "Silo Central"
SellbotLegFactorySpecEastSiloCatwalk = "Pasarela del Silo Este"
SellbotLegFactorySpecWestElevatorShaft = "Hueco del Ascensor del Silo Oeste"
SellbotLegFactorySpecEastElevatorShaft = "Hueco del Ascensor del Silo Este"

