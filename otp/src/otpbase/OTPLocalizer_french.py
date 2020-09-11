import string
from otp.otpbase.OTPLocalizer_french_Property import *

# common locations
lTheBrrrgh = 'Le Glagla'
lDaisyGardens = 'Le Jardin de Daisy'
lDonaldsDock = "Quais Donald"
lDonaldsDreamland = "Le Pays des Rêves de Donald"
lMinniesMelodyland = "Le Pays Musical de Minnie"
lToontownCentral = 'Toontown Centre'
lGoofySpeedway = "Circuit Dingo"

# common strings
lCancel = 'Annuler'
lClose = 'Fermer'
lOK = 'OK'
lNext = 'Suivant'
lNo = 'Non'
lQuit = 'Quitter'
lYes = 'Oui'

Cog  = "Cog"
Cogs = "Cogs"

# OTPDialog.py
DialogOK = lOK
DialogCancel = lCancel
DialogYes = lYes
DialogNo = lNo

# DistributedAvatar.py
WhisperNoLongerFriend = "%s a quitté ta liste d'amis."
WhisperNowSpecialFriend = "%s est maintenant ton ami(e) secret(e) !"
WhisperComingToVisit = "%s vient te voir."
WhisperFailedVisit = "%s a essayé de venir te voir."
WhisperTargetLeftVisit = "%s est parti ailleurs. Essaie encore !"
WhisperGiveupVisit = "%s n'a pas pu te trouver parce que tu te déplaces !"
WhisperIgnored = "%s t'ignore !"
TeleportGreeting = "Salut, %s."
WhisperFriendComingOnline = "%s se connecte !"
WhisperFriendLoggedOut = "%s s'est déconnecté."

# ChatInputNormal.py
ChatInputNormalSayIt = "Dis-le"
ChatInputNormalCancel = "Annuler"
ChatInputNormalWhisper = "Chuchoter"
ChatInputWhisperLabel = "À %s"

# ChatInputSpeedChat.py
SCEmoteNoAccessMsg = "Tu n'as pas encore accès\nà cette émotion."
SCEmoteNoAccessOK = "OK"

ParentPassword = "Mot de passe parent"

# ChatGarbler.py
ChatGarblerDefault = ["blah"]

# ChatManager.py
ChatManagerChat = "Chat"
ChatManagerWhisperTo = "Chuchoter à :"
ChatManagerWhisperToName = "Chuchoter à :\n%s"
ChatManagerCancel = "Annuler"
ChatManagerWhisperOffline = "%s est déconnecté(e)."
OpenChatWarning = "Tu n'as pas encore d' \"amis secrets\" ! Tu ne peux pas discuter avec les autres Toons s'ils ne sont pas tes amis secrets.\n\nPour devenir ami(e) secret(e) avec quelqu'un, clique sur lui ou sur elle, et sélectionne \"Secrets\" dans le panneau d'informations. Bien entendu, tu peux toujours parler à n'importe qui avec le Chat rapide."
OpenChatWarningOK = "OK"
UnpaidChatWarning = "Une fois que tu es inscrit(e), tu peux utiliser ce bouton pour discuter avec tes amis à l'aide du clavier. Avant cela, tu dois discuter avec les autres Toons à l'aide du Chat rapide."
UnpaidChatWarningPay = "S'inscrire maintenant !"
UnpaidChatWarningContinue = "Continuer l'essai gratuit"
PaidNoParentPasswordWarning = "Une fois que tu as choisi un mot de passe \"parent\", tu peux utiliser ce bouton pour discuter avec tes amis à l'aide du clavier. Avant cela, tu dois discuter avec les autres Toons à l'aide du Chat rapide."
PaidNoParentPasswordWarningSet = "Établir le mot de passe \"parent\" !"
PaidNoParentPasswordWarningContinue = "Continuer à jouer"
PaidParentPasswordUKWarning = "Une fois le Chat activé vous pourrez discuter avec vos amis en utilisant le clavier. Si vous décidez de ne pas activer le Chat vous pourrez continuer à utiliser le Chat Rapide pour discuter avec les autres Toons."
PaidParentPasswordUKWarningSet = "Activer le Chat !"
PaidParentPasswordUKWarningContinue = "Continuer à jouer"
NoSecretChatWarningTitle = "Contrôle parental"
NoSecretChatWarning = "Pour discuter avec un ami, la fonction \"amis secrets\" doit être activée. Les enfants doivent demander à leurs parents de s'identifier avec leur mot de passe \"parent\" pour en savoir plus sur la fonction \"amis secrets\" et avoir accès au contrôle parental."
RestrictedSecretChatWarning = 'Pour obtenir ou entrer un secret, vous devez entrer votre mot de passe \"parent\". Vous pouvez désactiver ceci par une simple modification de vos options.'
NoSecretChatWarningOK = "OK"
NoSecretChatWarningCancel = "Annuler"
NoSecretChatWarningWrongPassword = "Le mot de passe n'est pas correct. Veuillez entrer le mot de passe \"parent\" créé lorsque vous avez acheté ce compte. Ce mot de passe n'est pas celui utilisé pour jouer."
NoSecretChatAtAllTitle = "Chat \"amis secrets\"."
# not sure what this should do in the new world order
NoSecretChatAtAll = "Pour discuter avec un(e) ami(e), la fonction \"amis secrets\" doit être activée. La fonction \"amis secrets\" permet à un membre de discuter avec un autre membre uniquement à l'aide d'un code secret qui doit être communiqué en dehors du jeu.\n\nPour activer cette fonction ou pour en savoir plus à propos de son fonctionnement, sortez du jeu Toontown et cliquez \"Options de compte\" sur la page Internet de Toontown."
NoSecretChatAtAllOK = "OK"
ChangeSecretFriendsOptions = "Changer les options d' amis secrets"
ChangeSecretFriendsOptionsWarning = "\nMerci d'entrer le mot de passe \"parent\" pour changer les options d' \"amis secrets\"."
ActivateChatTitle = "Options amis secrets"

from pandac.PandaModules import TextProperties
from pandac.PandaModules import TextPropertiesManager

shadow = TextProperties()
shadow.setShadow(-0.025, -0.025)
shadow.setShadowColor(0,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('ombre', shadow)

red = TextProperties()
red.setTextColor(1,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('rouge', red)

ActivateChat = """La fonction "amis secrets" permet à un membre de discuter avec un autre membre uniquement à l'aide d'un code secret qui doit être communiqué en dehors du jeu. Pour une description complète, cliquez ici : La fonction "amis secrets" n'est ni modérée ni surveillée. Si les parents autorisent leurs enfants à utiliser leur compte avec la fonction "amis secrets" activée, nous les encourageons à surveiller leurs enfants lorsqu'ils jouent. Une fois activée, la fonction "amis secrets" est disponible jusqu'à ce qu'elle soit désactivée. En activant la fonction "amis secrets", vous reconnaissez qu'elle comporte des risques inhérents, que vous avez été informés de ceux-ci, et que vous acceptez lesdits risques."""
















ActivateChatYes = "Activer"
ActivateChatNo = lCancel
ActivateChatMoreInfo = "Plus d'infos"

# SecretFriendsInfoPanel.py
SecretFriendsInfoPanelOk = "Ok"
SecretFriendsInfoPanelClose = lClose
SecretFriendsInfoPanelText = ["""Caractéristiques de la fonction "amis secrets"."""
]

LeaveToPay = """De manière à pouvoir effectuer votre achat, vous allez automatiquement quitter le jeu et être redirigé sur le site Toontown."""
LeaveToPayYes = "Acheter"
LeaveToPayNo = lCancel

LeaveToSetParentPassword = """Afin de définir votre mot de passe "parent", vous allez automatiquement quitter le jeu et être redirigé(e) sur le site Toontown."""
LeaveToSetParentPasswordYes = "Définir le mot de passe."
LeaveToSetParentPasswordNo = lCancel

LeaveToEnableChatUK = """Pour activer le Chat le jeu devra quitter le site Toontown."""
LeaveToEnableChatUKYes = "Activer le Chat !"
LeaveToEnableChatUKNo = lCancel

ChatMoreInfoOK = lOK
SecretChatDeactivated = 'La fonction "amis secrets" a été désactivée.'
RestrictedSecretChatActivated = 'La fonction "Restriction des amis secrets" est activée !'
SecretChatActivated = "La fonction \"amis secrets\" a été activée !\n\nSi vous changez d'avis et décidez de désactiver cette fonction ultérieurement, cliquez sur \"Options de compte\" sur la page Internet de Toontown."
SecretChatActivatedOK = lOK
SecretChatActivatedChange = "Modifier les options"
ProblemActivatingChat = "Désolé ! Nous n'avons pas pu activer la fonction de chat \"amis secrets\".n\n%s\n\nRessayez plus tard."
ProblemActivatingChatOK = lOK

# MultiPageTextFrame.py
MultiPageTextFrameNext = 'Suivant'
MultiPageTextFramePrev = 'Précédent'
MultiPageTextFramePage = 'Page %s/%s'

# GuiScreen.py
GuiScreenToontownUnavailable = "Toontown semble momentanément indisponible, nouvelle tentative..."
GuiScreenCancel = lCancel


# CreateAccountScreen.py
CreateAccountScreenUserName = "Nom du compte"
CreateAccountScreenPassword = "Mot de passe"
CreateAccountScreenConfirmPassword = "Confirmation du mot de passe"
CreateAccountScreenCancel = "Annuler"
CreateAccountScreenSubmit = "Suivant"
CreateAccountScreenConnectionErrorSuffix = ".\n\nRessayez plus tard."
CreateAccountScreenNoAccountName = "Choisissez un nom de compte."
CreateAccountScreenAccountNameTooShort = "Le nom de votre compte doit comporter au moins %s caractères. Ressayez."
CreateAccountScreenPasswordTooShort = "Votre mot de passe doit comporter au moins %s caractères. Ressayez."
CreateAccountScreenPasswordMismatch = "Les mots de passe que vous avez entrés ne sont pas identiques. Ressayez."
CreateAccountScreenUserNameTaken = "Ce nom d'utilisateur est déjà pris. Ressayez."
CreateAccountScreenInvalidUserName = "Nom d'utilisateur incorrect.\nRessayez."
CreateAccountScreenUserNameNotFound = "Nom d'utilisateur introuvable.\nRessayez ou créez un nouveau compte."

# ToontownClientRepository.py
CRConnecting = "En cours de connexion..."
# host, port
CRNoConnectTryAgain = "Impossible de se connecter à %s:%s. Ressayer?"
CRNoConnectProxyNoPort = "Impossible de se connecter à %s:%s.\n\nVous êtes connecté(e) à Internet par un proxy, mais ce proxy ne permet pas les connexions par le port %s.\n\nVous devez ouvrir ce port ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'ouvrir ce port."
CRMissingGameRootObject = "Certains objets de la racine du jeu n'ont pu être trouvés. (Il s'agit peut-être d'un échec de connexion au réseau). Sortie du jeu."
CRNoDistrictsTryAgain = "Aucun district de Toontown n'est disponible. Ressayer ?"
CRRejectRemoveAvatar = " Le Toon n'a pas pu être supprimé, essaie à nouveau."
CRLostConnection = "Votre connexion Internet à Toontown s'est inopinément interrompue."
CRBootedReasons = {
    1: "Un problème inattendu est survenu. Votre connexion est perdue, mais vous devriez pouvoir vous reconnecter et retourner directement dans le jeu.",
    100: "Vous avez été déconnecté(e) parce que quelqu'un d'autre vient d'ouvrir une session avec votre compte sur un autre ordinateur.",
    120: "Vous avez été déconnecté du fait d'un problème avec votre autorisation d'utilisation du chat \"clavier\".",
    122: "Un problème inattendu est survenu lors de votre connexion à Toontown. Veuillez contacter le service clients de Toontown.",
    125: "Vos fichiers Toontown installés ne sont pas valides. Utilisez le bouton \"Jouer\" sur le site officiel de Toontown pour lancer Toontown.",
    126: "Vous n'êtes pas autorisé(e) à utiliser les fonctions réservées aux administrateurs.",
    151: "Vous avez été déconnecté(e) par un administrateur travaillant sur les serveurs de Toontown.",
    153: "Le district de Toontown sur lequel vous étiez en train de jouer a été réinitialisé. Toutes les personnes jouant dans ce district ont été déconnectées. Vous devriez toutefois pouvoir vous reconnecter et revenir directement dans le jeu.",
    288: "Désolé, vous avez utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci.",
    349: "Désolé, vous avez utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci.",
    }
CRBootedReasonUnknownCode = "Un problème inattendu s'est produit (code d'erreur %s). Votre connexion est perdue, mais vous devriez pouvoir vous reconnecter et retourner directement dans le jeu."
CRTryConnectAgain = "\n\nEssayer de se reconnecter ?"
# avName
CRToontownUnavailable = "Toontown est momentanément indisponible, nouvelle tentative..."
CRToontownUnavailableCancel = "Annuler"
CRNameCongratulations = "FÉLICITATIONS !!"
CRNameAccepted = "Ton nom a été\napprouvé par le Conseil de Toontown.\n\nÀ partir de ce jour\ntu t'appelleras\n\"%s\""
CRServerConstantsProxyNoPort = "Impossible de contacter %s.\n\nVous êtes connecté à Internet par un proxy, mais ce proxy ne permet pas les connexions par le port %s.\n\nVous devez ouvrir ce port ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'ouvrir ce port."
CRServerConstantsProxyNoCONNECT = "Impossible de contacter %s.\n\nVous êtes connecté(e) à Internet par un proxy, mais ce proxy ne prend pas en charge la méthode CONNECT.\n\nVous devez activer cette fonction ou désactiver votre proxy pour pouvoir jouer à Toontown. Si votre proxy vous est fourni par votre fournisseur d'accès, contactez ce dernier et demandez-lui d'activer cette méthode."
CRServerConstantsTryAgain = "Impossible de contacter %s.\n\nLe serveur de comptes de Toontown peut être temporairement hors service, ou votre connexion Internet est défaillante.\n\nRessayer ?"
CRServerDateTryAgain = "Impossible de trouver la date du serveur depuis %s. Ressayer ?"
AfkForceAcknowledgeMessage = "Ton Toon s'est assoupi et est parti au lit."
PeriodTimerWarning = "Ta limite de temps dans Toontown pour ce mois-ci est presque atteinte !"
PeriodForceAcknowledgeMessage = "Tu as utilisé toutes tes minutes disponibles dans Toontown pour ce mois-ci. Reviens jouer de nouveau le mois prochain !"
CREnteringToontown = "Accès à Toontown..."

# LoginScreen.py
LoginScreenUserName = "Nom du compte"
LoginScreenPassword = "Mot de passe"
LoginScreenLogin = "Ouvrir une session"
LoginScreenCreateAccount = "Créer un compte"
LoginScreenQuit = "Quitter"
LoginScreenLoginPrompt = "Entrez un nom d'utilisateur et un mot de passe."
LoginScreenBadPassword = "Mot de passe erroné.\nRessayez."
LoginScreenInvalidUserName = "Nom d'utilisateur incorrect.\nRessayez."
LoginScreenUserNameNotFound = "Utilisateur introuvable.\nRessayez ou créez un nouveau compte."
LoginScreenPeriodTimeExpired = "Désolé, vous avez déjà utilisé toutes vos minutes disponibles dans Toontown pour ce mois-ci. Revenez au début du mois prochain."
LoginScreenNoNewAccounts = "Nous sommes désolés, nous n'acceptons pas de nouveaux comptes pour le moment."
LoginScreenTryAgain = "Ressayez"


# SpeedChat

# Avatar.py
DialogSpecial = "ooo"
DialogExclamation = "!"
DialogQuestion = "?"
# Cutoff string lengths to determine how much barking to play
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# Used several places in the game. Defined globally because
# we keep changing the name
GlobalSpeedChatName = "Chat rapide"

# Toontown Speedchat
SCMenuPromotion  = "Promotionnel"
SCMenuElection  = "ÉLECTIONS"
SCMenuEmotions  = "ÉMOTIONS"
SCMenuCustom    = "MES EXPRESSIONS"
SCMenuResistance = "UNITÉ !"
SCMenuPets      = "ANIMAUX FAMILIERS"
SCMenuPetTricks = "TOURS"
SCMenuCog       = "COGGERIES"
SCMenuHello     = "BONJOUR"
SCMenuBye       = "AU REVOIR"
SCMenuHappy     = "HEUREUX"
SCMenuSad       = "TRISTE"
SCMenuFriendly  = "SYMPA"
SCMenuSorry     = "DÉSOLÉ"
SCMenuStinky    = "DÉSAGRÉABLE"
SCMenuPlaces    = "ENDROITS"
SCMenuToontasks = "DÉFITOONS"
SCMenuBattle    = "COMBAT"
SCMenuGagShop   = "BOUTIQUE A GAGS"
SCMenuFactory   = "USINE"
SCMenuKartRacing   = "KARTING"
SCMenuFactoryMeet = "RENCONTRE"
SCMenuCFOBattle = "Directeur Financier"
SCMenuCFOBattleCranes = "GRUES"
SCMenuCFOBattleGoons = "GOONS"
SCMenuCJBattle = "CHIEF JUSTICE"
SCMenuPlacesPlayground           = "TERRAIN DE JEUX"
SCMenuPlacesEstate               = "PROPRIÉTÉ"
SCMenuPlacesCogs                 = "COGS"
SCMenuPlacesWait                 = "ATTENDS"
SCMenuFriendlyYou                = "Tu..."
SCMenuFriendlyILike              = "J'aime..."
SCMenuPlacesLetsGo               = "Allons..."
SCMenuToontasksMyTasks           = "MES DÉFITOONS"
SCMenuToontasksYouShouldChoose   = "Je crois que tu devrais choisir..."
SCMenuBattleGags                 = "GAGS"
SCMenuBattleTaunts               = "MOQUERIES"
SCMenuBattleStrategy             = "STRATÉGIE"

# FriendSecret.py
FriendSecretNeedsPasswordWarningTitle = "Contrôles parentaux"
FriendSecretNeedsPasswordWarning = """Pour obtenir ou saisir un secret, tu dois entrer le mot de passe parent. Tu peux désactiver cet avertissement dans la zone "Member Services (Services aux membres)" du site Internet de Toontown."""
FriendSecretNeedsPasswordWarningOK = lOK
FriendSecretNeedsPasswordWarningCancel = lCancel
FriendSecretNeedsPasswordWarningWrongPassword = """Ce mot de passe est incorrect. Saisis le mot de passe "parent" créé lorsque tu as acheté ce compte. Ce n'est pas le même mot de passe que celui utilisé pour jouer."""
FriendSecretIntro = "Si tu joues à Toontown en ligne de Disney avec quelqu'un que tu connais réellement, vous pouvez devenir amis secrets. Tu peux communiquer avec tes amis secrets à l'aide du clavier. Les autres Toons ne comprendront pas ce que vous êtes en train de dire.\n\nPour cela, il faut échanger un secret. Dis le secret à ton ami(e), mais à personne d'autre. Lorsque ton ami(e) écrit ton secret sur son écran, vous pourrez être amis secrets dans Toontown !"
FriendSecretGetSecret = "Obtenir un secret"
FriendSecretEnterSecret = "Si quelqu'un t'a donné un secret, écris-le ici."
FriendSecretOK = "OK"
FriendSecretEnter = "Entrer Secret"
FriendSecretCancel = "Annuler"
FriendSecretGettingSecret = "Recherche du secret..."
FriendSecretGotSecret = "Voilà ton nouveau secret. N'oublie pas de l'écrire !\n\nTu ne peux donner ce secret qu'à une seule personne. Une fois que quelqu'un aura écrit ton secret, il ne pourra fonctionner pour personne d'autre. Si tu veux donner un secret à plus d'une personne, demande un autre secret.\n\nLe secret ne fonctionnera que dans les deux jours suivants. Ton ami(e) devra l'entrer sur son écran avant la fin de cette période pour qu'il puisse fonctionner.\n\nTon secret est :"
FriendSecretTooMany = "Désolé, tu ne peux plus avoir de secrets aujourd'hui. Tu en as déjà eu assez !n\nEssaie encore demain."
FriendSecretTryingSecret = "Recherche du secret..."
FriendSecretEnteredSecretSuccess = "Tu es maintenant ami(e) secret(e) avec %s !"
FriendSecretEnteredSecretUnknown = "Ce n'est le secret de personne. Es-tu certain(e) de l'avoir épelé correctement ?\n\nSi tu l'as épelé correctement, il peut être périmé. Demande un nouveau secret à ton ami(e), ou prends-en un nouveau toi-même et donne-le à ton ami(e)."
FriendSecretEnteredSecretFull = "Tu ne peux pas être ami(e) avec %s parce que l'un(e) de vous a déjà trop d'amis sur sa liste."
FriendSecretEnteredSecretFullNoName = "Vous ne pouvez pas être amis parce que l'un de vous a déjà trop d'amis sur sa liste."
FriendSecretEnteredSecretSelf = "Tu viens juste d'écrire ton propre secret ! Maintenant, personne d'autre ne peut plus utiliser ce secret."
FriendSecretNowFriends = "Tu es maintenant ami(e) secret(e) avec %s !"
FriendSecretNowFriendsNoName = "Vous êtes maintenant amis secrets !"

# FriendInvitee.py
FriendInviteeTooManyFriends = "%s voudrait être ton ami(e) mais tu as déjà trop d'amis sur ta liste !"
FriendInviteeInvitation = "%s voudrait être ton ami(e)."
FriendInviteeOK = "OK"
FriendInviteeNo = "Non"

# FriendInviter.py
FriendInviterOK = "OK"
FriendInviterCancel = "Annuler"
FriendInviterStopBeingFriends = "Arrêter d'être ami(e)."
FriendInviterYes = "Oui"
FriendInviterNo = "Non"
FriendInviterClickToon = "Clique sur le Toon avec lequel tu voudrais devenir ami(e)."
FriendInviterTooMany = "Tu as trop d'amis sur ta liste pour pouvoir en ajouter un de plus maintenant. Tu vas devoir retirer des amis de ta liste si tu veux devenir ami(e) avec %s."
FriendInviterNotYet = "Veux-tu devenir ami(e) avec %s ?"
FriendInviterCheckAvailability = "Recherche de la disponibilité de %s."
FriendInviterNotAvailable = "%s est occupé(e) en ce moment, ressaie plus tard."
FriendInviterWentAway = "%s est parti(e)."
FriendInviterAlready = "%s est déjà ton ami(e)."
FriendInviterAlreadyInvited = "%s a déjà été invité."
FriendInviterAskingCog = "Demande à %s d'être ton ami(e)."
FriendInviterAskingPet = "%s saute, tourne en rond et te lèche le visage."
FriendInviterAskingMyPet = "%s est déjà ton MEILLEUR ami."
FriendInviterEndFriendship = "Es-tu certain de vouloir cesser d'être ami(e) avec %s ?"
FriendInviterFriendsNoMore = "%s n'est plus ton ami(e)."
FriendInviterSelf = "Tu es déjà \"ami(e)\" avec toi-même !"
FriendInviterIgnored = "%s t'ignore."
FriendInviterAsking = "Demande à %s d'être ton ami(e)."
FriendInviterFriendSaidYes = "%s a dit oui !"
FriendInviterFriendSaidNo = "%s a dit non, merci."
FriendInviterFriendSaidNoNewFriends = "%s ne cherche pas de nouveaux amis pour l'instant."
FriendInviterTooMany = "%s a déjà trop d'amis !"
FriendInviterMaybe = "%s n'a pas pu répondre."
FriendInviterDown = "Ne peut pas se faire d'amis pour l'instant."

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
    "Recul",
    "A plat ventre",
    "Moquerie",
    "Révérence",
    "Peau de banane",
    "Salut de la Résistance",
    "Rire",
    "Oui",
    "Non",
    "OK",
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
    "%s recule.",
    "%s tombe à plat ventre.",
    "%s te fait une révérence.",
    "%s glisse sur une peau de banane.",
    "%s fait le salut de la Résistance.",
    "%s sourit.",
    "%s rit.",
    "%s dit \"oui\".",
    "%s dit \"non\".",
    "%s dit \"OK\".",
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
    "Recul" : 10,
    "Désorienté(e)"  : 11,
    "A plat ventre" : 12,
    "Révérence"    : 13,
    "Peau de banane" : 14,
    "Salut de la Résistance" : 15,
    "Rire" : 16,
    "Oui"    : 17,
    "Non"     : 18,
    "OK"     : 19,
    }

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

SuitFaceoffTaunts = {
    'b':  ["Est-ce que tu as un don à me faire ?",
           "Je vais faire de toi un mauvais perdant.",
           "Je vais te mettre à sec.",
           "Je suis \"A-Positif\", je vais gagner.",
           "Ne sois pas si \"O-Négatif\".",
           "Je suis surpris que tu m'aies trouvé, je suis très mobile.",
           "Je vais devoir te faire une addition rapide.",
           "Tu vas bientôt avoir besoin d'un en-cas.",
           "Quand j'aurai fini tu auras une grosse fatigue.",
           "Ça ne fait mal qu'un instant.",
           "Je vais te faire tourner la tête.",
           "Tu arrives à point, je suis en hypo.",
           ],
    'm':  ["Circule, y'a rien à voir.",
           "Tu fréquentes les gens comme moi ?",
           "Bien, il faut être deux pour avoir de la compagnie.",
           "Allons voir la compagnie.",
           "Cela a l'air d'un bon endroit pour voir du monde.",
           "Bon, est-ce qu'on n'est pas bien ici ?",
           "Tu frôles la défaite.",
           "Je vais me mêler de tes affaires.",
           "Est-ce que tu es sûr de vouloir voir du monde ?",
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
           "Alors, tu trembles ?",
           ],
    'hh': ["Je suis bien en tête.",
           "Tu t'entêtes à tort.",
           "Tu as la tête dure.",
           "Oh, bien, je te cherchais.",
           "J'aurai ta tête.",
           "Relève la tête !",
           "On dirait que tu as une tête à chercher les ennuis.",
           "Tu te payes ma tête ?",
           "Un trophée parfait pour ma collection.",
           "Tu vas avoir un vrai mal de tête.",
           "Ne perds pas la tête à cause de moi.",
           ],
    'tbc': ["Attention, je vais te faire fondre.",
            "Je fais partie du gratin.",
            "Je t'ai gru, hier. Je peux être un roc fort quelquefois.",
            "Ah, finalement j'avais peur que tu en fasses tout un fromage.",
            "Je vais t'écrémer.",
            "Tu ne penses pas que je vieillis bien ?",
            "Je vais te transformer en pâte à tartiner.",
            "On me dit que je suis très fort.",
            "Fais attention, je connais ta date de péremption.",
            "Fais attention, ma force est mon état mental.",
            "Je vais te mouler à la louche.",
            ],
    'cr': ["À L'ATTAQUE !",
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
    'mh': ["Tu es prêt pour la prise ?",
           "Lumières, action !",
           "Silence, on tourne.",
           "Aujourd'hui le rôle du Toon vaincu sera joué par - TOI !",
           "Cette scène va être coupée au montage.",
           "J'ai déjà une idée de ma motivation pour cette scène.",
           "Tu es prêt pour ta scène finale ?",
           "Je suis prêt à signer ton générique de fin.",
           "Je t'ai dit de ne pas m'appeler.",
           "Que le spectacle continue !",
           "C'est un métier en or !",
           "J'espère que tu n'as pas oublié ton texte.",
           ],
    'nc': ["On dirait que ton numéro est terminé.",
           "J'espère que tu préfères les soustractions.",
           "Maintenant tu es vraiment en infériorité numérique.",
           "C'est déjà l'heure des comptes ?",
           "Nous comptons sur quelque chose.",
           "Sur quoi voudrais-tu compter aujourd'hui ?",
           "Ce que tu dis a de l'intérêt.",
           "Ça ne va pas être une opération facile.",
           "Vas-y, choisis un nombre.",
           "Je me contenterai d'un bon chiffre.",
           ],
    'ls': ["C'est le moment de payer tes mensualités.",
           "Tu vis sur un emprunt.",
           "Ton prêt arrive à échéance.",
           "C'est le moment de payer.",
           "Tu as demandé une avance et elle est accordée.",
           "Tu vas payer ça cher.",
           "Il est temps de rembourser.",
           "Épargne-moi tes simagrées !",
           "C'est bien que tu sois là, je suis dans tous mes états.",
           "On en prend un pourcentage ?",
           "Laisse-moi en profiter.",
           ],
    'mb': ["Par ici la monnaie.",
           "Je peux empocher ça.",
           "Papier ou plastique ?",
           "Tu as ta sacoche ?",
           "N'oublie pas, l'argent ne fait pas le bonheur.",
           "Attention, j'ai de la réserve.",
           "Tu vas avoir des ennuis d'argent.",
           "L'argent fait tourner le monde.",
           "Je suis trop riche pour ton cholestérol.",
           "On n'a jamais trop d'argent !",
           ],
    'rb': ["Tu t'es fait voler.",
           "Je te dépouillerai de cette victoire.",
           "Je t'ennuie royalement !",
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
           "Tu vas me mettre à dos !",
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
           "C'est à ton tour de te faire teindre.",
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
           "Tu veux faire quelques tours avec moi ?",
           "J'ai un tour de main particulier.",
           ],
    'f': ["Je vais parler de toi au patron !",
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
           "Je suis un numéro 2 !",
           "Je vais te supprimer de mes listes.",
           "Je vais te l'écrire plus clairement.",
           "Allons droit au but.",
           "Dépêchons-nous, je fais rapidement des taches.",
           "Je m'inscris en faux.",
           "Tu veux t'inscrire ?",
           "Tu m'as inscrit sur la liste ?",
           "Attention, je peux laisser des taches.",
           ],
    'ym': ["Je suis certain que tu ne vas pas aimer ça.",
           "Je ne connais pas la signification du mot \"non\".",
           "Tu veux me voir ? C'est quand tu veux.",
           "Tu as besoin d'une mise à exécution positive.",
           "Je vais te faire une impression positive.",
           "Je n'ai encore jamais eu tort.",
           "Oui, je suis prêt pour toi.",
           "C'est vraiment ce que tu veux ?",
           "Je suis certain de terminer ça sur une note positive.",
           "Je confirme notre rendez-vous.",
           "Je n'accepte pas les refus.",
           ],
    'mm': ["Je vais me mêler de tes affaires !",
           "Quelquefois les gros ennuis ont l'air tout petits.",
           "Il n'y a pas de trop petit travail pour moi.",
           "Je veux que le travail soit bien fait, donc je le ferai moi-même.",
           "Tu as besoin de quelqu'un pour s'occuper de ton capital.",
           "Oh, bien, un projet.",
           "Chapeau, tu as réussi à me trouver.",
           "Je crois que tu as besoin d'un peu de gestion.",
           "Je vais m'occuper de toi dans peu de temps.",
           "Je surveille le moindre de tes mouvements.",
           "C'est vraiment ce que tu veux faire ?",
           "On va faire ça à ma façon.",
           "Je vais espionner tout ce que tu fais.",
           "Je peux être très intimidant.",
           ],
    'ds': ["Tu descends !",
           "Tu as de moins en moins d'options.",
           "Attends-toi à des bénéfices en diminution.",
           "Tu viens juste de devenir réductible.",
           "Ne me demande pas de licencier.",
           "Je vais devoir faire quelques coupes claires.",
           "Les choses n'ont pas l'air d'aller bien fort pour toi.",
           "Tu as l'air tout ratatiné !",
           ],
    'cc': ["Surpris de me voir ?",
           "Tu as appelé ?",
           "Tu te prépares à accepter ma facture ?",
           "Ce Casse-pieds ramasse toujours.",
           "Je suis un petit malin.",
           "Reste en ligne - je suis là.",
           "Tu attendais mon appel ?",
           "J'espérais que tu répondrais à mon appel.",
           "Je vais te faire une impression du diable.",
           "J'appelle toujours directement.",
           "Eh bien, ta ligne a été transférée.",
           "Cet appel va te coûter cher.",
           "Il y a de la friture sur la ligne.",
           ],
    'tm': ["Je crains que ça ne soit peu pratique pour toi.",
           "Est-ce que mon contrat d'assurance pourrait t'intéresser ?",
           "Tu n'aurais pas dû répondre.",
           "Tu ne pourras pas te débarrasser de moi comme ça.",
           "Un moment difficile ? Bien.",
           "J'avais l'intention de te rencontrer.",
           "Je vais t'appeler en PCV.",
           "J'ai des articles coûteux pour toi aujourd'hui.",
           "Dommage pour toi - je démarche à domicile.",
           "Je suis préparé à conclure cette affaire rapidement.",
           "Je vais utiliser une bonne partie de tes ressources.",
           ],
    'nd': ["Je vais traîner ton nom dans la boue.",
           "J'espère que tu ne m'en voudras pas si je donne ton nom.",
           "On ne s'est pas déjà rencontrés ?",
           "Dépêchons-nous, je mange avec M. Hollywood.",
           "Je t'ai déjà dit que je connaissais Le Circulateur ?",
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
           "Tu veux des vêtements de deuxième main ?",
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
           "Tu ne veux pas garder ta chance rien que pour toi !",
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
           "C'est ce que tu peux offrir de mieux ?",
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
           "Il y a quoi au menu ?",
           "J'en pince pour toi.",
           "Tu vas te faire pincer.",
           ],
    'bf': ["On dirait que ton moral est bas.",
           "Je suis prêt à m'envoler !",
           "Je suis un pigeon pour les Toons.",
           "Oh, un vol-au-vent pour déjeuner.",
           "Ça suffira, j'ai un appétit de moineau.",
           "J'ai besoin d'un retour sur mes performances.",
           "Parlons un peu du fond de la question.",
           "Tu te rendras compte que mes talents sont insondables.",
           "Bien, j'ai besoin d'un petit remontant.",
           "J'aimerais bien t'avoir pour déjeuner.",
           ],
    'tf': ["C'est le moment de se dévoiler !",
           "Tu ferais mieux de regarder la défaite en face.",
           "Prépare-toi à faire face à ton pire cauchemar !",
           "Regarde-le en face, je suis meilleur que toi.",
           "Deux têtes valent mieux qu'une.",
           "Il faut être deux pour danser, tu veux danser ?",
           "Tu es sur le point d'avoir deux fois plus d'ennuis.",
           "Quelle joue veux-tu tendre en premier ?",
           "Je suis deux de trop pour toi.",
           "Tu ne sais pas qui tu as en face de toi.",
           "Tu te prépares à regarder ton destin en face ?",
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
           "Garçon, la même chose !",
           ],
    'ac': ["Je vais te chasser de la ville !",
           "Tu entends la sirène ?",
           "Ça va me plaire.",
           "J'aime l'ambiance de la chasse.",
           "Laisse-moi t'épuiser.",
           "Tu as une assurance ?",
           "J'espère que tu as apporté une civière avec toi.",
           "Je doute que tu puisses te mesurer à moi.",
           "Ça grimpe à partir d'ici.",
           "Tu vas bientôt avoir besoin de soins.",
           "Il n'y a pas de quoi rire.",
           "Je vais te donner de quoi t'occuper.",
           ]
    }

# These are all the standard SpeedChat phrases.
# The indices must fit into 16 bits (0..65535)
SpeedChatStaticText = {
    # top-level
    1 : 'Oui',
    2 : 'Non',
    3 : 'OK',

    # Hello
    100 : "Salut !",
    101 : "Bonjour !",
    102 : "Salut la compagnie !",
    103 : "Hé !",
    104 : "Coucou !",
    105 : "Salut tout le monde !",
    106 : "Bienvenue à Toontown !",
    107 : "Quoi de neuf ?",
    108 : "Comment ça va ?",
    109 : "Y a quelqu'un ?",

    # Bye
    200 : "Au revoir !",
    201 : "À plus !",
    202 : "À la prochaine !",
    203 : "Bonne journée !",
    204 : "Amuse-toi bien !",
    205 : "Bonne chance !",
    206 : "Je reviens tout de suite.",
    207 : "Je dois m'en aller.",
    208 : "Je reviens plus tard !",
    209 : "Je n'ai que quelques minutes.",

    # Happy
    300 : ":-)",
    301 : "Haaa !",
    302 : "Hourra !",
    303 : "Sympa !",
    304 : "Youhouu !",
    305 : "Ouais !",
    306 : "Ha ha !",
    307 : "Hi hi !",
    308 : "Waou !",
    309 : "Super !",
    310 : "Ouiii !",
    311 : "Ouh la !",
    312 : "Youpi !",
    313 : "Génial !",
    314 : "Hop-là !",
    315 : "Toontastique !",

    # Sad
    400 : ":-(",
    401 : "Oh non !",
    402 : "Oh oh !",
    403 : "Zut !",
    404 : "Mince !",
    405 : "Aïe !",
    406 : "Ffff !",
    407 : "Non !!!",
    408 : "Aïe aïe aïe !",
    409 : "Eh ?",
    410 : "J'ai besoin de plus de rigolpoints.",

    # Friendly
    500 : "Merci !",
    501 : "De rien.",
    502 : "Je t'en prie !",
    503 : "Quand tu veux !",
    504 : "Non merci.",
    505 : "Bon travail d'équipe !",
    506 : "C'était amusant !",
    507 : "Sois mon ami(e) s'il te plaît.",
    508 : "Faisons équipe !",
    509 : "Vous êtes super les copains !",
    510 : "Tu viens d'arriver par ici ?",
    511 : "Tu as gagné ?",
    512 : "Je crois que c'est trop risqué pour toi.",
    513 : "Tu veux de l'aide ?",
    514 : "Peux-tu m'aider ?",
    515 : "Tu es déja venu ici avant ?",

    # Friendly "Toi..."
    600 : "Tu as l'air sympa.",
    601 : "Tu es adorable !",
    602 : "Tu assures !",
    603 : "Quel génie !",

    # Friendly "J'aime bien..."
    700 : "J'aime bien ton nom.",
    701 : "J'aime bien ton look.",
    702 : "J'aime bien ta chemise.",
    703 : "J'aime bien ta jupe.",
    704 : "J'aime bien ton short.",
    705 : "J'aime bien ce jeu !",

    # Sorry
    800 : "Désolé(e) !",
    801 : "Aïe !",
    802 : "Désolé(e), je suis occupé(e) à combattre les Cogs !",
    803 : "Désolé(e), je suis occupé(e) à trouver des bonbons !",
    804 : "Désolé(e), je suis occupé(e) à terminer un défitoon !",
    805 : "Désolé(e), j'ai dû partir à l'improviste.",
    806 : "Désolé(e), j'ai été retardé(e).",
    807 : "Désolé(e), je ne peux pas.",
    808 : "Je ne pouvais plus attendre.",
    809 : "Je ne te comprends pas.",
    810 : "Utilise le %s." % GlobalSpeedChatName,
    811 : "Désolé, je suis en train de pêcher !",
    812 : "Désolé, je suis dans un bâtiment !",
    813 : "Désolé, j'aide un(e) ami(e) !",
    814 : "Désolé, je suis en pleine course de kart !",
    815 : "Désolé, je suis en train de jardiner !",

    # Stinky
    900 : "Hé !",
    901 : "S'il te plaît va t'en !",
    902 : "Arrête ça !",
    903 : "Ca n'est pas très gentil !",
    904 : "Ne sois pas méchant(e) !",
    905 : "Tu es nul(le) !",
    906 : "Envoie un rapport d'erreur.",
    907 : "Je suis coincé(e).",

    # Places
    1000 : "Allons-y !",
    1001 : "Peux-tu me téléporter ?",
    1002 : "On y va ?",
    1003 : "Où devons-nous aller ?",
    1004 : "Par quel chemin ?",
    1005 : "Par là.",
    1006 : "Suis-moi.",
    1007 : "Attends-moi !",
    1008 : "Attendons mon ami(e).",
    1009 : "Trouvons d'autres Toons.",
    1010 : "Attends ici.",
    1011 : "Attends une minute.",
    1012 : "Retrouvons-nous ici.",
    1013 : "Veux-tu venir chez moi ?",
    1014 : "Ne m'attends pas.",
    1015 : "Attends !",
    1016 : "Come check out my garden.",

    # Places "Allons-y..."
    1100 : "Allons faire un tour de tramway !",
    1101 : "Retournons au terrain de jeux !",
    1102 : "Allons combattre les %s !" % Cogs,
    1103 : "Allons reprendre un bâtiment %s !" % Cog,
    1104 : "Allons dans l'ascenseur !",
    1105 : "Allons à Toontown centre !",
    1106 : "Allons aux quais Donald !",
    1107 : "Allons au Pays musical de Minnie !",
    1108 : "Allons au Jardin de Daisy !",
    1109 : "Allons au Glagla !",
    1110 : "Allons au Pays des rêves de Donald !",
    1111 : "Allons chez moi !",
    1112 : "Allons chez toi !",
    1113 : "Allons au QG Vendibot !",
    1114 : "Allons combattre le Vice-Président !",
    1115 : "Allons dans l'usine !",
    1116 : "Allons à la pêche !",
    1117 : "Allons pêcher chez moi !",
    1118 : "Allons au QG Caissbot [FB1] !",
    1119 : "Allons combattre le Directeur Financier !",
    1120 : "Allons à la Fabrique à Sous !",
    1121 : "Allons à la Fabrique à Sous !",
    1122 : "Allons au QG des Loibots !",
    1123 : "Allons combattre le juge !",
    1124 : "Allons au bureau du Procureur !",

    # Toontasks
    1200 : "Quel défitoon dois-tu accomplir ?",
    1201 : "Occupons-nous de ça.",
    1202 : "Ce n'est pas ce que je cherche.",
    1203 : "Je vais aller chercher ça.",
    1204 : "Ce n'est pas dans cette rue.",
    1205 : "Je ne l'ai pas encore trouvé.",
    1206 : "J'ai besoin de plus de mérites Cogs.",
    1207 : "J'ai besoin de plus de pièces de costume de Cog.",
    1208 : "Ce n'est pas ce dont tu as besoin.",
    1209 : "J'ai trouvé ce dont tu as besoin.",
    1210 : "J'ai besoin de plus d'euros Cog.",
    1211 : "J'ai besoin de plus de convocations du jury.",
    1213 : "J'ai besoin de plus de pièces de costume de Caissbot.",
    1214 : "J'ai besoin de plus de pièces de costume de Loibot.",

    1299 : "Je dois avoir un défitoon.",

    # Toontasks "Je crois que tu devrais choisir..."
    1300 : "Je crois que tu devrais choisir un Toonique.",
    1301 : "Je crois que tu devrais choisir un Tapage.",
    1302 : "Je crois que tu devrais choisir une Chute.",
    1303 : "Je crois que tu devrais choisir un Piégeage.",
    1304 : "Je crois que tu devrais choisir un Leurre.",

    # Battle
    1400 : "Dépêche-toi !",
    1401 : "Joli coup !",
    1402 : "Sympa ce gag !",
    1403 : "Loupé !",
    1404 : "Tu as réussi !",
    1405 : "On a réussi !",
    1406 : "Amène ça !",
    1407 : "Du gâteau !",
    1408 : "C'était facile !",
    1409 : "Cours !",
    1410 : "À l'aide !",
    1411 : "Ouf !",
    1412 : "On a des ennuis.",
    1413 : "J'ai besoin de plus de gags.",
    1414 : "J'ai besoin d'un Toonique.",
    1415 : "Tu devrais passer.",
    1416 : "On peut le faire !",

    # Battle "Utilisons..."
    1500 : "Utilisons un toonique !",
    1501 : "Utilisons un piège !",
    1502 : "Utilisons un leurre !",
    1503 : "Utilisons un tapage !",
    1504 : "Lançons quelque chose !",
    1505 : "Utilisons une éclaboussure !",
    1506 : "Utilisons une chute !",

    # Battle TAUNTS
    1520 : "Rock and roll !",
    1521 : "Ça va faire mal.",
    1522 : "Attrapé !",
    1523 : "Livraison spéciale !",
    1524 : "Tu es toujours là ?",
    1525 : "J'ai VRAIMENT peur !",
    1526 : "Ça va faire une marque !",

    # Battle STRATEGY
    1550 : "Je vais utiliser le piégeage.",
    1551 : "Je vais utiliser le leurre.",
    1552 : "Je vais utiliser la chute.",
    1553 : "Tu devrais utiliser un gag différent.",
    1554 : "Tous sur le même Cog.",
    1555 : "Tu devrais choisir un Cog différent.",
    1556 : "Prenons le Cog le plus faible d'abord.",
    1557 : "Prenons le Cog le plus fort d'abord.",
    1558 : "Économise tes gags puissants.",
    1559 : "N'utilise pas le tapage sur les Cogs leurrés.",

    # Gag Shop
    1600 : "J'ai assez de gags.",
    1601 : "J'ai besoin de plus de bonbons.",
    1602 : "Moi aussi.",
    1603 : "Dépêche-toi !",
    1604 : "Un de plus ?",
    1605 : "Tu veux rejouer ?",
    1606 : "Jouons encore.",

    # Factory
    1700 : "Séparons-nous.",
    1701 : "Restons ensemble !",
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

    # CFO battle
    2100 : "Déplace la grue.",
    2101 : "Je peux déplacer la grue ?",
    2102 : "Je dois m'entraîner à déplacer la grue.",
    2103 : "Attrape un goon désactivé.",
    2104 : "Jette le goon sur le Directeur Financier.",
    2105 : "Lance un coffre-fort maintenant !",
    2106 : "Ne lance pas le coffre-fort maintenant !",
    2107 : "Le coffre-fort fera tomber son casque.",
    2108 : "Le coffre-fort sera son nouveau casque.",
    2109 : "Je n'arrive pas à atteindre un coffre-fort.",
    2110 : "Je n'arrive pas à atteindre un goon.",

    2120 : "Désactive les goons s'il te plaît.",
    2121 : "Je préfèrerais désactiver les goons.",
    2122 : "Je dois m'entraîner à désactiver les goons.",
    2123 : "Reste là s'il te plaît.",
    2124 : "Continue à bouger.",
    2125 : "Je dois continuer à bouger.",
    2126 : "Trouve quelqu'un qui a besoin d'aide.",

    2130 : "Sauve le trésor.",
    2131 : "Prends le trésor.",
    2132 : "J'ai besoin du trésor !",
    2133 : "Attention !",

    # CJ battle
    2200 : "Tu dois atteindre la balance.",
    2201 : "Je vais atteindre la balance.",
    2202 : "J'ai besoin d'aide pour la balance !",
    2203 : "Tu dois paralyser les Cogs.",
    2204 : "Je vais paralyser les Cogs.",
    2205 : "J'ai besoin d'aide avec les Cogs !",
    2206 : "J'ai besoin de plus de preuves.",
    2207 : "Je tire sur les chaises de la rangée du haut.",
    2208 : "Je tire sur les chaises de la rangée du bas.",
    2209 : "Ne reste pas dans le passage ! Nous n'arrivons pas à atteindre la casserole.",
    2210 : "Je vais nous faire des tooniques.",
    2211 : "Je n'ai pas de bonus de poids.",
    2212 : "Mon bonus de poids est de 1.",
    2213 : " Mon bonus de poids est de 2.",
    2214 : " Mon bonus de poids est de 3.",
    2215 : " Mon bonus de poids est de 4.",
    2216 : " Mon bonus de poids est de 5.",
    2217 : " Mon bonus de poids est de 6.",
    2218 : " Mon bonus de poids est de 7.",
    2219 : " Mon bonus de poids est de 8.",
    2220 : " Mon bonus de poids est de 9.",
    2221 : " Mon bonus de poids est de 10.",
    2222 : " Mon bonus de poids est de 11.",
    2223 : " Mon bonus de poids est de 12.",

    #Kart Racing Phrases
    #IMPORTANT: if you change numbers or add/subtract lines here than be
    # sure to adjust the kart racing menu guid dict below
    # Invites/Destinations
    3010 : "Quelqu'un veut faire la course ?",
    3020 : "Faisons la course !",
    3030 : "Tu veux faire la course ?",
    3040 : "Frimons avec nos karts !",
    3050 : "Je n'ai pas assez de tickets.",
    3060 : "Faisons encore une course !",
    3061 : "Tu veux faire une autre course ?",


    #Places
    3150 : "Je dois aller au magasin des karts.",
    3160 : "Allons sur les pistes !",
    3170 : "Allons sur la ligne des stands pour frimer avec nos karts !",
    3180 : "Je vais sur la ligne des stands pour frimer avec mon kart !",
    3190 : "Retrouve-moi sur les pistes !",
    3110 : "Retrouvons-nous près du magasin des karts !",
    3130 :  "Où va-t-on se retrouver ?",
    
    #Races
    3200 : "Où veux-tu faire la course ?",
    3201 : "Choisissons une autre course.",
    3210 : "Faisons une course d'entraînement." ,
    3211 : "Faisons un duel.",
    3220 : "J'aime la course du stade Cinglette !",
    3221 : "J'aime la course de la piste Champêtre !",
    3222 : "J'aime la course du circuit de la Ville !",
    3223 : " J'aime la course du Colisée Tortillé !",
    3224 : " J'aime la course des Landes légères !",
    3225 : " J'aime la course du Boulevard du Blizzard !",
    3230 : "Faisons la course au stade Cinglette !",
    3231 : "Faisons la course sur la piste Champêtre !",
    3232 : "Faisons la course sur le circuit de la Ville !",
    3233 : "Faisons la course au Colisée Tortillé !",
    3234 : "Faisons la course aux Landes légères !",
    3235 : "Faisons la course au Boulevard du Blizzard !",

    #Tracks
    3600 : "Sur quelle piste veux-tu que l'on fasse la course ?",
    3601 : "Choisis une piste !",
    3602 : "Est-ce qu'on pourrait faire la course sur une autre piste ?",
    3603 : "Choisissons une autre piste !",
    3640 : "Je veux faire la course sur la première piste !",
    3641 : "Je veux faire la course sur la deuxième piste !",
    3642 : "Je veux faire la course sur la troisième piste !",
    3643 : "Je veux faire la course sur la quatrième piste !",
    3660 : "Je ne veux pas faire la course sur la première piste !",
    3661 : "Je ne veux pas faire la course sur la deuxième piste !",
    3662 : "Je ne veux pas faire la course sur la troisième piste !",
    3663 : "Je ne veux pas faire la course sur la quatrième piste !",

    #Compliments
    3300 : "Wow ! Tu vas VITE !",
    3301 : "Tu es trop rapide pour moi !",
    3310 : "Belle course !",
    3320 : "J'aime beaucoup ton kart !",
    3330 : "Jolie course !",
    3340 : "Ton kart est chouette !",
    3350 : "Ton kart est super !",
    3360 : "Ton kart est génial !",

    #Taunts (commented out taunts are for possible purchase lines)
    #3400 : "Eat my dust!",
    3400 : "Tu as peur de faire la course avec moi ?",
    3410 : "On se retrouve sur la ligne d'arrivée !",
    #3420 : "You're slow as molasses!",
    3430 : "Je suis rapide comme l'éclair !",
    #3440 : "I'm faster than the speed of light!",
    3450 : "Tu ne m'attraperas jamais !",
    3451 : "Tu ne me battras jamais !",
    3452 : "Personne ne peut battre mon temps !",
    3453 : "Allez, on se dépêche !",
    3460 : "J'en veux encore !",
    3461 : "Tu as eu de la chance !",
    3462 : "Ooooh ! C'était pas loin !",
    3470 : "Waouh, j'ai cru que tu allais me battre !",
    #3500 : "Check out my ride!",
    #3510 : "Look at my wheels!",
    #3540 : "Vroom! Vroom!",
    #3560 : "I've seen Cogs move faster!",
    #3600 : "I'm the fastest of the fast!",



    # Promotional Considerations
    10000 : "A toi de choisir !",
    10001 : "Tu votes pour qui ?",
    10002 : "Pour moi ce sera Poulet !",
    10003 : "Vote maintenant ! Vote Vache !",
    10004 : "Perds la tête ! Vote Singe !",
    10005 : "Reste dans la course ! Vote Ours !",
    10006 : "Sois fort ! Vote Porc !",
    10007 : "Vote Chèvre - le sourire aux lèvres !",

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

    # Pets/Doodles
    21000: 'Par ici mon petit gars !',
    21001: 'Par ici ma fifille !',
    21002: 'Reste là.',
    21003: 'Un bon petit gars !',
    21004: 'Une bonne fifille !',
    21005: 'Gentil Doudou.',

    # Pet/Doodle Tricks
    21200: 'Saute !',
    21201: 'Fais le beau !',
    21202: 'Fais le mort !',
    21203: 'Roule-toi par terre !',
    21204: 'Fais une culbute !',
    21205: 'Danse !',
    21206: 'Parle !',

    # PIRATES
    50001 : 'Ouais',
    50002 : 'Nan',
    50003 : 'Grrr !',
    50004 : "Aye, aye Captain!",

    # Common Expressions
    50100 : "Ohé !",
    50101 : "Ohé, du bateau !",
    50102 : "Tiens bon !",
    50103 : "Dégagez le pont !",
    50104 : "Bon sang !",
    50105 : "Tous aux écoutilles !",
    50106 : "Yo-ho-ho !",
    50107 : "Oui mon capitaine !",
    50108 : "Accroche-toi à l'épave !",
    50109 : "Viens par là !",
    50110 : "Les morts ne mentent pas...",

    # Insults
    50200 : "Rat de cale !",
    50201 : "Espèce de fripon !",
    50202 : "On te retrouvera au fond de l'océan !",
    50203 : "Vaurien !",
    50204 : "Espèce de terrien !",

    # Compliments
    50300 : "Bien joué, matelot !",
    50301 : "Et voilà un coup bien placé !",
    50302 : "Joli coup !",
    50303 : "Bien fait !",
    50304 : "On leur a donné une bonne leçon !",
    50305 : "T'es pas si mal non plus !",
    50306 : "Une bien belle prise !",

    # Places
    50400 : "T'es où ?",
    50401 : "Allons faire une virée en ville.",
    50402 : "Allons vers les quais !",
    50403 : "Mettons les voiles.",
    50404 : "Allons au bar !",

    # Adventures
    50500 : "On met les voiles !",
    50501 : "Tous à bord ! On quitte le port !",
    50502 : "À l'abordaaage !",
    50503 : "On file vers l'île du Caïman !",
    50504 : "Filons vers la rade de la Tortue !",
    50505 : "Utilisons une carte au trésor !",
    50506 : "On retourne au port !",

    # Ships
    50600 : "Bâbord ! (gauche)",
    50601 : "Tribord ! (droite)",
    50602 : "Feu ennemi !",
    50603 : "Feu de batterie ! Tous à couvert !",
    50604 : "Chargez vos canons !",
    50605 : "Ouvrez le feu !",
    50606 : "Cessez le feu !",
    50607 : "Visez les mâts !",
    50608 : "Visez la coque !",
    50609 : "Préparez-vous à l'abordage !",
    50610 : "Elle arrive !",
    50611 : "Lâchez une bordée !",
    50612 : "On charge vite les canons !",
    50613 : "Grrr ! On y va !",
    50614 : "On les rattrape !",
    50615 : "Voie d'eau !",
    50616 : "On n'en peut plus !",
    50617 : "Il faut qu'on répare !",
    50618 : "Retraite !",
    50619 : "Un homme à la mer !",
    50620 : "Halte-là ! Une mauvaise barcasse !",

    # Greetings
    60100 : "Salut !",
    60101 : "Bonjour !",
    60102 : "Hé !",
    60103 : "Youhou !",
    60104 : "Salut tout le monde !",
    60105 : "Comment ça va ?",
    60106 : "Quoi de neuf ?",

    # Bye
    60200 : "Salut !",
    60201 : "A plus !",
    60202 : "A la prochaine !",
    60203 : "Je reviens tout de suite.",
    60204 : "Je dois y aller.",

    # Happy
    60300 : ":-)",
    60301 : "Ça, c'est super !",
    60302 : "Ouais !",
    60303 : "Hé hé !",
    60304 : "Génial !",
    60305 : "Ouais !",
    60306 : "Ça le fait !",
    60307 : "Cool !",
    60308 : "Génial !",
    60309 : "Oh la la !",

    # Sad
    60400 : ":-(",
    60401 : "Bouh !",
    60402 : "Oh, ben !",
    60403 : "Aïe !",
    60404 : "Poisse !",

    # Places
    60500 : "Où es-tu ?",
    60501 : "Allons à la boutique du passage !",
    60502 : "Allons à la salle Disco !",
    60503 : "Allons à Toontown.",
    60504 : "Allons aux Pirates des Caraïbes.",
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
    20 : "Pourquoi pas ?",
    30 : "Naturellement !",
    40 : "C'est comme ça que je fais.",
    50 : "Tout juste !",
    60 : "Qu'est-ce qui se passe ?",
    70 : "Mais bien sûr !",
    80 : "Bingo !",
    90 : "Tu plaisantes...",
    100 : "Ça m'a l'air bien.",
    110 : "C'est loufoque !",
    120 : "Atmosphérique !",
    130 : "Bon sang !",
    140 : "Ne t'en fais pas.",
    150 : "Grrrr !",
    160 : "Quoi de neuf ?",
    170 : "Hé hé hé !",
    180 : "À demain.",
    190 : "À la prochaine fois.",
    200 : "À plus tard, lézard.",
    210 : "Dans un moment, caïman.",
    220 : "Je dois m'en aller d'ici peu.",
    230 : "Je n'en sais rien !",
    240 : "Tu es déjà parti !",
    250 : "Aïe, ça pique !",
    260 : "Je t'ai eu !",
    270 : "S'il te plaît !",
    280 : "Merci vraiment beaucoup !",
    290 : "Tu te débrouilles bien !",
    300 : "Excuse-moi !",
    310 : "Puis-je t'aider ?",
    320 : "C'est ce que je dis !",
    330 : "Si tu as peur de te brûler, évite la cuisine.",
    340 : "Mille sabords !",
    350 : "Est-ce que ce n'est pas spécial ?",
    360 : "Arrête de chahuter !",
    370 : "Le chat a mangé ta langue ?",
    380 : "Maintenant tu es mal vu(e) !",
    390 : "Eh bien, regarde ce qui arrive là.",
    400 : "Je dois aller voir un Toon.",
    410 : "Ne t'énerve pas !",
    420 : "Ne te dégonfle pas !",
    430 : "Tu es une proie facile.",
    440 : "Peu importe !",
    450 : "Complètement !",
    460 : "Adorable !",
    470 : "C'est super !",
    480 : "Ouais, mon chou !",
    490 : "Attrape-moi si tu peux !",
    500 : "Il faut d'abord que tu te soignes.",
    510 : "Tu as besoin de plus de rigolpoints.",
    520 : "Je reviens dans une minute.",
    530 : "J'ai faim.",
    540 : "Ouais, t'as raison !",
    550 : "J'ai sommeil.",
    560 : "Je suis prêt(e) maintenant !",
    570 : "Ça m'ennuie.",
    580 : "J'adore ça !",
    590 : "C'était sensationnel !",
    600 : "Saute !",
    610 : "Tu as des gags ?",
    620 : "Qu'est-ce qui ne va pas ?",
    630 : "Doucement.",
    640 : "Qui va lentement va sûrement.",
    650 : "Marqué !",
    660 : "Prêt ?",
    670 : "À vos marques !",
    680 : "Partez !",
    690 : "Allons par là !",
    700 : "Tu as gagné !",
    710 : "Je vote oui.",
    720 : "Je vote non.",
    730 : "J'en suis.",
    740 : "Je n'en suis pas.",
    750 : "On ne bouge pas, je reviens.",
    760 : "C'était rapide !",
    770 : "Qu'est-ce que c'est que ça ?",
    780 : "Qu'est-ce que c'est que cette odeur ?",
    790 : "Ça pue !",
    800 : "Je m'en fiche.",
    810 : "C'est exactement ce qu'il fallait.",
    820 : "Commençons la fête !",
    830 : "Par ici tout le monde !",
    840 : "Quoi de neuf ?",
    850 : "Le chèque est parti.",
    860 : "J'ai entendu ce que tu as dit !",
    870 : "Tu me parles ?",
    880 : "Merci, je serai ici toute la semaine.",
    890 : "Hmm.",
    900 : "Je prends celui-là.",
    910 : "Je l'ai !",
    920 : "C'est à moi !",
    930 : "S'il te plaît, prends-le.",
    940 : "On ne s'approche pas, ça pourrait être dangereux.",
    950 : "Pas de soucis !",
    960 : "Oh, non !",
    970 : "Houlala !",
    980 : "Youhouuu !",
    990 : "Tout le monde à bord !",
    1000 : "Nom d'un chien !",
    1010 : "La curiosité est un vilain défaut.",
    # Series 2
    2000 : "Ne fais pas le bébé !",
    2010 : "Si je suis content(e) de te voir !",
    2020 : "Je t'en prie.",
    2030 : "Tu as évité les ennuis ?",
    2040 : "Mieux vaut tard que jamais !",
    2050 : "Bravo !",
    2060 : "Sérieusement, les copains...",
    2070 : "Tu veux te joindre à nous ?",
    2080 : "À plus tard !",
    2090 : "Changé d'avis ?",
    2100 : "Viens le prendre !",
    2110 : "Oh là là !",
    2120 : "Ravi(e) de faire ta connaissance.",
    2130 : "Ne fais rien que je ne ferai pas !",
    2140 : "N'y pense pas !",
    2150 : "N'abandonne pas le navire !",
    2160 : "Ne retiens pas ta respiration.",
    2170 : "Sans commentaire.",
    2180 : "C'est facile à dire.",
    2190 : "Assez c'est assez !",
    2200 : "Excellent !",
    2210 : "Content de te trouver ici !",
    2220 : "Arrête un peu.",
    2230 : "Content d'entendre ça.",
    2240 : "Continue, ça m'amuse !",
    2250 : "Vas-y !",
    2260 : "Bon travail !",
    2270 : "Content de te voir !",
    2280 : "Il faut que je bouge.",
    2290 : "Il faut que je m'en aille.",
    2300 : "Attends là.",
    2310 : "Attends une seconde.",
    2320 : "Va t'éclater !",
    2330 : "Amuse-toi !",
    2340 : "Je n'ai pas toute la journée !",
    2350 : "Retiens la vapeur !",
    2360 : "Nom d'un petit bonhomme !",
    2370 : "Je n'y crois pas !",
    2380 : "J'en doute.",
    2390 : "Je t'en dois un.",
    2400 : "Je te reçois 5 sur 5.",
    2410 : "Je crois aussi.",
    2420 : "Je crois que tu devrais passer un tour.",
    2430 : "C'est moi qui voulais le dire.",
    2440 : "Je ne ferais pas ça si j'étais toi.",
    2450 : "Ce serait avec plaisir !",
    2460 : "J'aide mon ami(e).",
    2470 : "Je suis là toute la semaine.",
    2480 : "Imagine ça !",
    2490 : "Juste à temps...",
    2500 : "Tant que ce n'est pas fini, ce n'est pas fini.",
    2510 : "Je pense tout haut.",
    2520 : "On reste en contact.",
    2530 : "Quel temps de chien !",
    2540 : "Et que ça saute !",
    2550 : "Fais comme chez toi.",
    2560 : "Une autre fois peut-être.",
    2570 : "Je peux me joindre à vous ?",
    2580 : "C'est sympa ici.",
    2590 : "Je suis content de te parler.",
    2600 : "Ça ne fait aucun doute.",
    2610 : "Sans blague !",
    2620 : "Ni de près ni de loin.",
    2630 : "Quel culot !",
    2640 : "OK pour moi.",
    2650 : "D'accord.",
    2660 : "Dis \"Cheese !\"",
    2670 : "Tu dis quoi ?",
    2680 : "Ta-daa !",
    2690 : "Doucement.",
    2700 : "À plus !",
    2710 : "Merci, mais non.",
    2720 : "C'est le bouquet !",
    2730 : "C'est marrant.",
    2740 : "Voilà exactement ce qu'il faut !",
    2750 : "Il y a une invasion de Cogs !",
    2760 : "Salut.",
    2770 : "Fais attention !",
    2780 : "Bravo !",
    2790 : "Qu'est-ce qui se prépare ?",
    2800 : "Qu'est-ce qui se passe ?",
    2810 : "Ça marche pour moi.",
    2820 : "Oui monseigneur.",
    2830 : "Tu paries.",
    2840 : "Tu fais le calcul.",
    2850 : "Tu t'en vas déjà ?",
    2860 : "Tu me fais rire !",
    2870 : "Ça va bien.",
    2880 : "Tu descends !",
    # Series 3
    3000 : "Tout ce que tu diras.",
    3010 : "Je pourrais venir ?",
    3020 : "Vérifie, s'il te plaît.",
    3030 : "Ne sois pas trop certain.",
    3040 : "Ça ne te fait rien si je le fais.",
    3050 : "Pas de panique !",
    3060 : "Tu ne le savais pas !",
    3070 : "Ne t'occupe pas de moi.",
    3080 : "Eureka !",
    3090 : "Voyez-vous ça !",
    3100 : "Oublie ça !",
    3110 : "Tu vas dans la même direction ?",
    3120 : "Content(e) pour toi !",
    3130 : "Mon Dieu !",
    3140 : "Passe un bon moment !",
    3150 : "Réfléchissons !",
    3160 : "Et ça recommence.",
    3170 : "Et voilà !",
    3180 : "Ça te plaît ?",
    3190 : "Je crois aussi.",
    3200 : "Je ne crois pas.",
    3210 : "Je te recontacte.",
    3220 : "Je suis toute ouïe.",
    3230 : "Je suis occupé(e).",
    3240 : "Je ne blague pas !",
    3250 : "J'en suis baba.",
    #3260 : "Garde le sourire.",
    3270 : "Tiens-moi au courant !",
    3280 : "Laisse faire !",
    3290 : "De même, certainement.",
    3300 : "Remue-toi !",
    3310 : "Oh là là, comme le temps passe.",
    3320 : "Sans commentaire.",
    3330 : "Ah, on y vient !",
    3340 : "OK pour moi.",
    3350 : "Ravi(e) de te rencontrer.",
    3360 : "D'accord.",
    3370 : "Sûrement.",
    3380 : "Merci vraiment beaucoup.",
    3390 : "C'est plutôt ça.",
    3400 : "Voilà ce qu'il faut !",
    3410 : "C'est l'heure pour moi d'aller faire un somme.",
    3420 : "Crois-moi !",
    3430 : "Jusqu'à la prochaine fois.",
    3440 : "Ne t'endors pas !",
    3450 : "C'est comme ça qu'il faut faire !",
    3460 : "Qu'est-ce qui t'amène ?",
    3470 : "Qu'est-ce qui s'est passé ?",
    3480 : "Et quoi maintenant ?",
    3490 : "Toi d'abord.",
    3500 : "Tu prends à gauche.",
    3510 : "Tu parles !",
    3520 : "Tu es grillé(e) !",
    3530 : "Tu es trop !",

    # Series 4
    4000 : "Vive les Toons !",
    4010 : "Les Cogs en sont baba !",
    4020 : "Tous les Toons du monde ensemble !",
    4030 : "Salut, mon pote !",
    4040 : "Merci beaucoup.",
    4050 : "Fiche le camp, l'ami.",
    4060 : "J'en peux plus, je vais dormir.",
    4070 : "J'en croque un morceau !",
    4080 : "La ville n'est pas assez grande pour nous deux !",
    4090 : "En selle !",
    4100 : "Dégaine !!!",
    4110 : "Y'a bon... Tout ça pour moi !",
    4120 : "Bonne route !",
    4130 : "Et là, je m'en vais droit vers l'horizon...",
    4140 : "On fiche le camp !",
    4150 : "C'est une idée fixe ?",
    4160 : "Bon sang !",
    4170 : "Impeccable.",
    4180 : "Je crois bien.",
    4190 : "Taillons-nous !",
    4200 : "Eh, va savoir !",
    4210 : "Coucou, me revoilou !",
    4220 : "Comme on se retrouve...",
    4230 : "Allez, hue !",
    4240 : "Haut les mains.",
    4250 : "J'y compte bien.",
    4260 : "Retiens la vapeur !",
    4270 : "Je raterais un éléphant dans un couloir.",
    4280 : "À la prochaine.",
    4290 : "C'est vraiment impressionnant !",
    4300 : "Ne nous dis pas que tu as la trouille.",
    4310 : "Tu crois que tu as de la chance ?",
    4320 : "Bon sang, mais qu'est-ce qui se passe ici ?",
    4330 : "Tu peux bien rouler des mécaniques !",
    4340 : "Eh bien ça, c'est le bouquet.",
    4350 : "C'est un vrai régal pour les yeux !",
    4360 : "Quel trou à rats !",
    4370 : "Ne t'en fais pas.",
    4380 : "Quelle tronche !",
    4390 : "Ça t'apprendra !",
    # Series 6
    6000 : "Je veux des friandises !",
    6010 : "J'ai un faible pour le sucré.",
    6020 : "Ce n'est pas assez cuit.",
    6030 : "C'est comme faucher les jouets d'un enfant !",
    6040 : "Et treize à la douzaine.",
    6050 : "Ils en ont voulu, ils en auront !",
    6060 : "C'est la cerise sur le gâteau.",
    6070 : "On ne peut pas avoir le beurre et l'argent du beurre.",
    6080 : "J'ai l'impression d'être un enfant dans un magasin de bonbons.",
    6090 : "Six de celui-là, une demi-douzaine de l'autre...",
    6100 : "Disons-le avec des mots tendres.",
    6110 : "Concentre-toi sur ta pâte à gâteau.",
    6120 : "Tu voudrais que j'avale ça ?",
    6130 : "C'est mince comme du papier alu.",
    6140 : "Fais péter les cahuètes !",
    6150 : "Tu es un dur à cuire !",
    6160 : "Et voilà, c'est la déconfiture.",
    6170 : "C'est comme l'eau et l'huile.",
    6180 : "Tu me prends pour une poire ?",
    6190 : "Avec du miel, ça passera mieux.",
    6200 : "Tu es fait de ce que tu manges !",
    6210 : "C'est de la tarte !",
    6220 : "Ne fais pas l'andouille !",
    6230 : "Du sucre, de la cannelle et ce sera nickel.",
    6240 : "C'est de la crème !",
    6250 : "C'est le gâteau !",
    6260 : "Y'en aura pour tout le monde !",
    6270 : "C'est pas la peine d'en rajouter une couche.",
    6280 : "Toc, toc...",
    6290 : "Qui est là ?",
    # Series 7
    7000 : "Arrête de faire des singeries !",
    7010 : "C'est vraiment mettre des bâtons dans les roues.",
    7020 : "Tu singes tout.",
    7030 : "Tu deviens espiègle comme un singe.",
    7040 : "Ça sent la monnaie de singe.",
    7050 : "Je te cherche les poux.",
    7060 : "Qui est-ce qui fait le singe au milieu ?",
    7070 : "Tu m'enlèves une épine du pied...",
    7080 : "C'est plus marrant qu'une armée de singes !",
    7090 : "Sans rire...",
    7100 : "Je suis malin comme un singe.",
    7110 : "Et qu'est-ce qu'il a, le pingouin ?",
    7120 : "Je n'entends rien de mal.",
    7130 : "Je ne vois rien de mal.",
    7140 : "Je ne dis rien de mal.",
    7150 : "Encore un truc à la noix de coco, on se casse.",
    7160 : "C'est la jungle par ici.",
    7170 : "T'es au top du top.",
    7180 : "Ça c'est super !",
    7190 : "Je deviens dingue !",
    7200 : "Entrons dans la danse !",
    7210 : "Ça swingue par ici !",
    7220 : "Je vais prendre racine.",
    7230 : "On nous tourne en bourrique.",
    7230 : "Allez, salut la compagnie.",
    7240 : "Les bonbons ne poussent pas sur les cocotiers !",

    # Halloween
    10000 : "Cet endroit est une ville fantôme.",
    10001 : "Joli costume !",
    10002 : "Je crois que cet endroit est hanté.",
    10003 : "Une farce ou des friandises !",
    10004 : "Bouh !",
    10005 : "Ici trouille !",
    10006 : "Joyeux Halloween !",
    10007 : "Je vais me transformer en citrouille.",
    10008 : "Fantômtastique !",
    10009 : "Sinistre !",
    10010 : "Ça fait froid dans le dos !",
    10011 : "Je déteste les araignées !",
    10012 : "Tu as entendu ça ?",
    10013 : "Tu n'as pas l'ombre d'une chance !",
    10014 : "Tu m'as fait peur !",
    10015 : "C'est sinistre !",
    10016 : "C'est effrayant !",
    10017 : "C'était étrange....",
    10018 : "Des squelettes dans ton placard ?",
    10019 : "Je t'ai fait peur ?",

    # Fall Festivus
    11000 : "Bah! Balivernes !",
    11001 : "Mieux vaut ne pas bouder !",
    11002 : "Brrr !",
    11003 : "Glaçant !",
    11004 : "Viens le prendre !",
    11005 : "Ne prends pas cet air glacé.",
    11006 : "À la Sainte-Catherine, tout arbre prend racine !",
    11007 : "Bon réveillon !",
    11008 : "Bonne année !",
    11009 : "Chaud les marrons !",
    11010 : "Bon appétit pour la dinde !",
    11011 : "Ho ! Ho ! Ho !",
    11012 : "Ce neige pas un problème.",
    11013 : "Ce neige pas un mystère.",
    11014 : "Et que ça neige !",
    11015 : "On va en faire une pelletée de neige.",
    11016 : "Meilleures vœux !",
    11017 : "Je n'en neige aucun doute !",
    11018 : "Jusque là, la neige est bonne !",
    11019 : "Tu vas le regretter !",

    # Valentines
    12000 : "Reste avec moi !",
    12001 : "Sois mon chouchou !",
    12002 : "Bonne Saint Valentin !",
    12003 : "Ooh, comme c'est mignon.",
    12004 : "J'ai le béguin pour toi.",
    12005 : "C'est une amourette.",
    12006 : "Je t'adore !",
    12007 : "C'est la Saint Valentin ?",
    12008 : "Tu es un amour !",
    12009 : "Tu es mon canard en sucre.",
    12010 : "Tu es adorable.",
    12011 : "Tu as besoin d'un câlin.",
    12012 : "Adorable !",
    12013 : "C'est si mignon !",
    12014 : "Mignonne allons voir si la rose...",
    12015 : "Qui ce matin était éclose...",
    12016 : "C'est mignon !",

    # St. Patricks Day
    13000 : "Mes salutations fleuries !",
    13001 : "Vive le printemps !",
    13002 : "Tu n'es pas très printanier !",
    13003 : "C'est la chance qui éclôt.",
    13004 : "Je suis vert d'envie.",
    13005 : "Sacré veinard !",
    13006 : "Tu es mon trèfle à quatre feuilles !",
    13007 : "Tu es mon porte-bonheur !",
    #Potential racing phrases for purchase

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


# Pirates Speedchat
PSCMenuExpressions  = "EXPRESSIONS"
PSCMenuInsults    = "INSULTES"
PSCMenuCompliments = "COMPLIMENTS"
PSCMenuPlaces     = "ENDROITS"
PSCMenuAdventures = "ADVENTURE"
PSCMenuShips      = "SHIPS"

# Gateway Speedchat
GWSCMenuHello     = "SALUTATIONS"
GWSCMenuBye       = "AU REVOIR"
GWSCMenuHappy     = "HEUREUX"
GWSCMenuSad       = "TRISTE"
GWSCMenuPlaces     = "ENDROITS"

# NamePanel.py - PickAName/TypeAName
RandomButton = "Aléatoire"
TypeANameButton = "Entre un nom"
PickANameButton = "Choisis un nom"
NameShopSubmitButton = "Envoyer"
RejectNameText = "Ce nom n'est pas autorisé. Essaie encore."
WaitingForNameSubmission = "Envoi de ton nom..."

NameShopNameMaster = "NameMaster_french.txt"
NameShopPay = "Inscris-toi !"
NameShopPlay = "Essai gratuit"
NameShopOnlyPaid = "Seuls les utilisateurs payants\npeuvent donner un nom à leurs Toons.\nJusqu'à ce que tu t'inscrives,\nton nom sera\n"
NameShopContinueSubmission = "Continuer l'envoi"
NameShopChooseAnother = "Choisir un autre nom"
NameShopToonCouncil = "Le Conseil de Toontown\nva examiner ton\nnom."+ \
                       "L'examen peut\nprendre quelques jours.\nPendant que tu attends,\nton nom sera\n"
PleaseTypeName = "Entre ton nom :"
AllNewNames = "Tous les noms\ndoivent être approuvés\npar le Conseil de Toontown."
NameShopNameRejected = "Le nom que tu as\nenvoyé a été refusé."
NameShopNameAccepted = "Félicitations !\nLe nom que tu as\nenvoyé a\nété accepté !"
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
                 "seulement autorisés dans des mots tels que \"M.\", \"doct.\", \"prof.\", etc.")
NCApostrophes = "Ton nom a trop d'apostrophes."

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "Change les informations sur %s."
AvatarDetailPanelFailedLookup = "Impossible d'obtenir les informations pour %s."
AvatarDetailPanelOnline = "District: %(district)s\nEmplacement: %(location)s"
AvatarDetailPanelOffline = "District: offline\nEmplacement: offline"

# AvatarPanel.py
AvatarPanelFriends = "Amis"
AvatarPanelWhisper = "Murmmurer"
AvatarPanelSecrets = "Secrets"
AvatarPanelGoTo = "Vas à"
AvatarPanelIgnore = "Ignore"
#AvatarPanelCogDetail = "Dept: %s\nLevel: %s\n"
AvatarPanelCogLevel = "Niveau : %s"
AvatarPanelCogDetailClose = lClose

# TeleportPanel.py
TeleportPanelOK = "OK"
TeleportPanelCancel = "Annuler"
TeleportPanelYes = "Oui"
TeleportPanelNo = "Non"
TeleportPanelCheckAvailability = "Essaie d'aller à %s."
TeleportPanelNotAvailable = "%s est occupé(e) en ce moment, ressaie plus tard."
TeleportPanelIgnored = "%s t'ignore"
TeleportPanelNotOnline = "%s n'est pas en ligne en ce moment."
TeleportPanelWentAway = "%s est parti(e)."
TeleportPanelUnknownHood = "Tu ne sais pas aller jusqu'à %s !"
TeleportPanelUnavailableHood = "%s est occupé(e) en ce moment, ressaie plus tard."
TeleportPanelDenySelf = "Tu ne peux pas aller te voir toi-même !"
TeleportPanelOtherShard = "%(avName)s est dans le district %(shardName)s, et tu es dans le district %(myShardName)s. Veux-tu aller à %(shardName)s ?"

KartRacingMenuSections = [
 -1,
 "PLACES",
 "COURSES",
 "PISTES",
 "COMPLIMENTS",
 "MOQUERIE"

]

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Appelez le Service clients au %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "Si vous avez besoin d'aide, vous pouvez contacter par email le service clients à %s."
TTAccountIntractibleError = "Une erreur s'est produite."

# OTPGLobals stuff
def getSignFontLocale():
    return getSignFont()



