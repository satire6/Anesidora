import string
import time
from toontown.toonbase.TTLocalizer_japanese_Property import *

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
ExtraKeySanityCheck = "Ignore me"

InterfaceFont = 'phase_3/models/fonts/HGHeiseiMarugothictaiW8.ttc'
ToonFont = 'phase_3/models/fonts/HGHeiseiMarugothictaiW8.ttc'
SuitFont = 'phase_3/models/fonts/HGHanKointai.ttc'
SignFont = 'phase_3/models/fonts/MickeyFont.bam'
MinnieFont = 'phase_3/models/fonts/MickeyFont.bam'
FancyFont = 'phase_3/models/fonts/Comedy'
NametagFonts = ('phase_3/models/fonts/DFKyG7.ttc:1',      #0 *
                'phase_3/models/fonts/DCCry5.ttc:1',      #1 *
                'phase_3/models/fonts/DCInl5.ttc:1',      #2 *
                'phase_3/models/fonts/DFCry5.ttc:1',      #3 *
                'phase_3/models/fonts/DFKai3.ttc:1',      #4 *
                'phase_3/models/fonts/DFLis6.ttc:1',      #5 *
                'phase_3/models/fonts/DFMimP3.ttc:1',     #6 *
                'phase_3/models/fonts/DFMrg2.ttc:1',      #7 *
                'phase_3/models/fonts/DFMrm5.ttc:1',      #8 *
                'phase_3/models/fonts/DFPocl7.ttc:1',     #9 *
                'phase_3/models/fonts/DFPococ.ttc:1',     #10 *
                'phase_3/models/fonts/DFPost7.ttc:1',     #11 *
                'phase_3/models/fonts/DFRys9.ttc:1',      #12 *
                'phase_3/models/fonts/DFSht5.ttc:1',      #13 *
                )
NametagFontNames = ('ﾌﾘｰ・ﾌﾟﾗﾝ',      #0 *
                'クリスタル',       #1 *
                'しろぬき',           #2 *
                'かくもじ',           #3 *
                'まじめ',           #4 *
                'ナチュラル',            #5 *
                'しんぶん',       #6 *
                'シンプル',        #7 *
                'まるもじ',       #8 *
                'クリップ',          #9 *
                'ポップ',          #10 *
                'フロッグ',          #11 *
                'せきひ',       #12 *
                'エイジア',         #13 *
                )

NametagLabel = "ﾈｰﾑﾀｸﾞ"

UnpaidNameTag = "シャドー"

BuildingNametagFont = 'phase_3/models/fonts/DFKyG7.ttc:1'
BuildingNametagShadow = (0.05, 0.05)

# Product prefix
ProductPrefix = 'TT'

# common names
Mickey = "ミッキー"
VampireMickey = "VampireMickey"
Minnie = "ミニー"
Donald = "ドナルド"
Daisy  = "デイジー"
Goofy  = "グーフィー"
Pluto  = "プルート"
Flippy = "フリッピー"
Chip   = "チップ"
Dale   = "デール"

# common locations
lTheBrrrgh = 'ブルブルランド'
lDaisyGardens = 'デイジーガーデン'
lDonaldsDock = "ドナルドのハトバ"
lDonaldsDreamland = "ドナルドのドリームランド"
lMinniesMelodyland = "ミニーのメロディーランド"
lToontownCentral = 'トゥーンタウンセントラル'
lToonHQ = 'トゥーンＨＱ'
lSellbotHQ = "セルボットほんぶ"
lGoofySpeedway = "グーフィー・サーキット"
lOutdoorZone = "チップとデールのドングリひろば"
lGolfZone = "チップとデールのミニ・ゴルフ"
lPartyHood = "パーティー会場"

lGagShop = 'ギャグショップ'
lClothingShop = 'ようふくや'
lPetShop = 'ペットショップ'

# common strings
lCancel = 'キャンセル'
lClose = 'とじる'
lOK = 'ＯＫ'
lNext = 'つぎへ'
lQuit = 'やめる'
lYes = 'はい'
lNo = 'いいえ'
lBack = '戻る'

sleep_auto_reply = "%s is sleeping right now"
lHQ = '本部'

lHQOfficerF = 'ＨＱスタッフ'
lHQOfficerM = 'ＨＱスタッフ'

MickeyMouse = "ミッキーマウス"

AIStartDefaultDistrict = "シリーヴィル"

Cog  = "コグ"
Cogs = "コグ"
ACog = "コグ"
TheCogs = "コグ"
ASkeleton = "ガイコグ"
Skeleton = "ガイコグ"
SkeletonP = "ガイコグ"
Av2Cog = "a Version 2.0 Cog"
v2Cog = "Version 2.0 Cog"
v2CogP = "Version 2.0 Cogs"
ASkeleton = "a Skelecog"
Foreman = "工場長"
ForemanP = "工場長"
AForeman = "工場長"
CogVP = "コグゼキュティブ"
CogVPs = "コグゼキュティブの"
ACogVP = "コグゼキュティブ"
Supervisor = "金庫番"
SupervisorP = "金庫番"
ASupervisor = "金庫番"
CogCFO = "マネーマネー"
CogCFOs = "マネーマネーの"
ACogCFO = "マネーマネー"

# AvatarDNA.py
Bossbot = "ボスボット"
Lawbot = "ロウボット"
Cashbot = "マネーボット"
Sellbot = "セルボット"
BossbotS = "ボスボット"
LawbotS = "ロウボット"
CashbotS = "マネーボット"
SellbotS = "セルボット"
BossbotP = "ボスボット"
LawbotP = "ロウボット"
CashbotP = "マネーボット"
SellbotP = "セルボット"
BossbotSkelS = BossbotS+" "+Skeleton
LawbotSkelS = LawbotS+" "+Skeleton
CashbotSkelS = CashbotS+" "+Skeleton
SellbotSkelS = SellbotS+" "+Skeleton
BossbotSkelP = Bossbot+" "+Skeleton
LawbotSkelP = Lawbot+" "+Skeleton
CashbotSkelP = Cashbot+" "+Skeleton
SellbotSkelP = Sellbot+" "+Skeleton
SkeleRevivePostFix = " v2.0"

lBossbotHQ = Bossbot+lHQ
lLawbotHQ = Lawbot+lHQ
lCashbotHQ = Cashbot+lHQ
lSellbotHQ = Sellbot+lHQ
lTutorial = 'トゥーントリアル'
lMyEstate = 'キミのおうち'
lWelcomeValley = 'ｳｪﾙｶﾑﾊﾞﾚｰ'

# ToontownGlobals.py

# (to, in, location)
# reference the location name as [-1]; it's guaranteed to be the last entry
# This table may contain names for hood zones (N*1000) that are not
# appropriate when referring to the hood as a whole. See the list of
# names below this table for hood names.
GlobalStreetNames = {
    20000 : ("", "", "チュートリアル・テラス"),# Tutorial
    1000 : ("", "", "プレイグラウンド"),
    1100 : ("", "", "バーナクル・ストリート"),
    1200 : ("", "", "シーウィード・ストリート"),
    1300 : ("", "", "ライトハウス・レーン"),
    2000 : ("", "", "プレイグラウンド"),
    2100 : ("", "", "シリー・ストリート"),
    2200 : ("", "", "ルーピー・ストリート"),
    2300 : ("", "", "パンチライン・ストリート"),
    3000 : ("", "", "プレイグラウンド"),
    3100 : ("", "", "セイウチ・ストリート"),
    3200 : ("", "", "スリート・ストリート"),
    3300  : ("", "", "ポーラープレイス"),
    4000 : ("", "", "プレイグラウンド"),
    4100 : ("", "", "アルト・アベニュー"),
    4200 : ("", "", "バリトン・ストリート"),
    4300 : ("", "", "テナー・ストリート"),
    5000 : ("", "", "プレイグラウンド"),
    5100 : ("", "", "エルム・ストリート"),
    5200 : ("", "", "メイプル・ストリート"),
    5300 : ("", "", "オーク・ストリート"),
    9000 : ("", "", "プレイグラウンド"),
    9100 : ("", "", "ララバイ・ストリート"),
    9200  : ("", "", "パジャマ・プレイス"),
    10000 : ("","", ""),
    10100 : ("","", lBossbotHQ+'ロビー'),
    10200 : ("", "", "クラブハウス"),
    10500 : ("", "", "フロント３"),
    10600 : ("", "", "ミドル６"),
    10700 : ("", "", "バック９"),
    11000 : ("","", ""),
    11100 : ("","", lSellbotHQ+'ロビー'),
    11200 : ("","", Sellbot+'ファクトリー'),
    11500 : ("","", Sellbot+'ファクトリー'),
    12000 : ("","", ""),
    12100 : ("","", lCashbotHQ+'ロビー'),
    12500 : ("","", Cashbot+' コイン工場'),
    12600 : ("","", Cashbot+' ドル工場'),
    12700 : ("","", Cashbot+' ゴールド工場'),
    13000 : ("","", ""),
    13100 : ("","", lLawbotHQ+'ロビー'),
    13200 : ("", "", "裁判所ロビー"),
    13300 : ("", "", "ロウボットＡオフィス"),
    13400 : ("", "", "ロウボットＢオフィス"),
    13500 : ("", "", "ロウボットＣオフィス"),
    13600 : ("", "", "ロウボットＤオフィス"),
    }

# reference the location name as [-1]; it's guaranteed to be the last entry
DonaldsDock       = ("", "", lDonaldsDock)
ToontownCentral   = ("", "", lToontownCentral)
TheBrrrgh         = ("", "", lTheBrrrgh)
MinniesMelodyland = ("", "", lMinniesMelodyland)
DaisyGardens      = ("", "", lDaisyGardens)
OutdoorZone       = ("", "", lOutdoorZone)
FunnyFarm         = ("", "", "ファニー・ファーム")
GoofySpeedway     = ("", "", lGoofySpeedway)
DonaldsDreamland  = ("", "", lDonaldsDreamland)
BossbotHQ         = ("", "", "ボスボットほんぶ")
SellbotHQ         = ("", "", "セルボットほんぶ")
CashbotHQ         = ("", "", "マネーボットほんぶ")
LawbotHQ          = ("", "", "ロウボットほんぶ")
Tutorial          = ("", "", "トゥーントリアル")
MyEstate          = ("", "", "キミのおうち")
WelcomeValley     = ("", "", "ｳｪﾙｶﾑﾊﾞﾚｰ")
GolfZone          = ("", "", lGolfZone)
PartyHood         = ("", "", lPartyHood)

Factory = 'コグファクトリー'
Headquarters = '本部'
SellbotFrontEntrance = 'ファクトリー入口'
SellbotSideEntrance = 'ファクトリー裏口'
Office = '事務所'

FactoryNames = {
    0 : '工場の模型',
    11500 : 'セルボット コグファクトリー',
    13300 : 'ロウボットコグオフィス', #remove me JML
    }

FactoryTypeLeg = 'レッグ'
FactoryTypeArm = 'アーム'
FactoryTypeTorso = 'ボディ'

MintFloorTitle = '%s階'

# Quests.py
TheFish = "魚"
AFish = "魚"
Level = "レベル"
QuestsCompleteString = "コンプリート"
QuestsNotChosenString = "選択されていません"
Period = "。"

Laff = "ｹﾞﾗｹﾞﾗﾎﾟｲﾝﾄ"

QuestInLocationString = " %(inPhrase)s %(location)s"

# _avName_ gets replaced with the avatar (player's) name
# _toNpcName_ gets replaced with the npc's name we are being sent to
# _where_ gets replaced with a description of where to find the npc, with a leading \a
QuestsDefaultGreeting = ("こんにちは、 _avName_！",
                         "やあ、 _avName_！",
                         "_avName_！",
                         "_avName_ じゃないか！",
                         "いらっしゃい、 _avName_！",
                         "ハロー、 _avName_！",
                         "ごきげんいかがかな、 _avName_？",
                         "あっ、 _avName_！",
                         )
QuestsDefaultIncomplete = ("タスクは進んでるかい、_avName_？",
                           "そのタスクが終わるまで、まだまだみたいだね。",
                           "がんばってね、_avName_！",
                           "最後までがんばってね、君ならきっと大丈夫！",
                           "タスクをコンプリートするまでがんばってね、応援してるよ！",
                           "トゥーンタスクが終わるまで、がんばれ！",
                           )
QuestsDefaultIncompleteProgress = ("ここに来たのは正解だけど、まずはトゥーンタスクを終わらせなきゃね。",
                                   "そのトゥーンタスクが終わってからここに戻っておいで。",
                                   "トゥーンタスクが終わったらここに戻ってきてね。",
                                   )
QuestsDefaultIncompleteWrongNPC = ("よく出来たね。次は_toNpcName_のところに行ってね。_where_",
                                   "そのトゥーンタスクもそろそろ終わりかな。_toNpcName_に会うといい。_where_",
                                   "_toNpcName_に会って、タスクを終わらせておいで。_where_",
                                   )
QuestsDefaultComplete = ("よくやったね！\nこれは君へのごほうびだよ。",
                         "やったね、_avName_！ はい、ごほうびだよ。",
                         "素晴らしい出来だね、_avName_! これをごほうびにあげるよ。",
                         )
QuestsDefaultLeaving = ("バイバイ!",
                        "さよなら！",
                        "じゃあね、_avName_",
                        "またね、_avName_！",
                        "がんばってね！",
                        "トゥーンタウンで楽しんでいってね！",
                        "それじゃまたね！",
                        )
QuestsDefaultReject = ("こんにちは。",
                       "いらっしゃいませ。",
                       "調子はどう？",
                       "今日もいい天気ですね。",
                       "今ちょっと忙しいんですよ、_avName_さん。",
                       "はい？",
                       "こんにちは、 _avName_！",
                       "_avName_、 いらっしゃい！",
                       "あ、_avName_！ こんにちは！",
                       # Game Hints
                       "トゥーンガイドを開くにはＦ８ボタンを押せばいいって知ってた？",
                       "地図を使うと、遊び場にワープすることができるよ！",
                       "他のプレイヤーと友達になりたかったら、彼らをクリックしてみるといいよ。",
                       "" + Cog + "をクリックすると、そいつの情報を得られるよ。",
                       "ゲラゲラメーターをいっぱいにするには遊び場でトレジャーを集めよう。",
                       "" + Cog + "の建物は危険だから、一人で行かないようにね。",
                       "バトルで負けちゃうと、" + Cogs + "がキミのギャグをぜんぶ持っていっちゃうんだ。",
                       "トロリーゲームをプレイするとギャグが集まりやすいよ！",
                       "トゥーンタスクを完了するとゲラゲラポイントをもらえるよ。",
                       "トゥーンタスクを終わらせるごとにごほうびがもらえるよ。",
                       "ギャグをもっと運べるようになる「ごほうび」もあるんだって",
                       "バトルで勝ったら、倒した" + Cog + "の数に応じてトゥーンタスクのポイントがもらえるのさ。",
                       "" + Cog + " の建物を奪回したら、中に入ってみよう。建物の所有者が感謝のことばを伝えてくれるよ。",
                       "PageUpボタンを押していると、上を見上げることができるよ！",
                       "Tabボタンを押すと、周りを違った視点から見ることができるよ。",
                       "自分の考えを友達にだけ伝えたかったら、発言の前に'.'をつけてね。",
                       "" + Cog + "がスタン状態になっていると、落下物をよけられなくなるらしいよ。",
                       "" + Cog + "の建物はひとつとして同じ外観のものがないんだって",
                       "建物の上の階にいる" + Cogs + "を倒すと、バトル後のスキルレベルがもっと高くなるよ。",
                       )
QuestsDefaultTierNotDone = ("こんにちは、_avName_！新しいトゥーンタスクを始める前に、今のタスクを終わらせてね。",
                            "やあ！今もってるタスクを終わらせてから新しいトゥーンタスクをスタートしてね。",
                            "やあ、_avName_！ 今もってるタスクを終わらせたら、新しいタスクをあげるよ。",
                            )
# The default string gets replaced with the quest getstring
QuestsDefaultQuest = None
QuestsDefaultVisitQuestDialog = ("_toNpcName_がキミを探してるらしいよ。_where_",
                                 "時間がある時にでも_toNpcName_に会ってみて。_where_",
                                 "もし_toNpcName_のいる方に行くことがあったら、会ってあげて。_where_",
                                 "_toNpcName_に会いに行くといいよ。_where_",
                                 "_toNpcName_が新しいタスクをくれるよ。_where_",
                                 )
# Quest dialog
QuestsLocationArticle = "で"
def getLocalNum(num):
	if (num <=9):
		return str(num) + "つ"
	else:
                return str(num)
QuestsItemNameAndNum = "%(name)s %(num)s" #★１月２４日新規修正 by Gregさん

QuestsCogQuestProgress = "倒した数：%(progress)s / %(numCogs)s"
QuestsCogQuestHeadline = "ウォンテッド"
QuestsCogQuestSCStringS = "%(cogLoc)s%(cogName)sを倒さなくちゃ！" #★「の」がAnywhereのときに不要
QuestsCogQuestSCStringP = "%(cogLoc)s%(cogName)sを倒さなくちゃ！" #★「の」がAnywhereのときに不要
QuestsCogQuestDefeat = "%sを倒す"
QuestsCogQuestDefeatDesc = "%(cogName)s%(numCogs)s体"

QuestsCogNewNewbieQuestObjective = "新しいトゥーンを助けて、%sをやっつけよう！"
QuestsCogNewNewbieQuestCaption = "ゲラゲラポイントが%d以下の新しいトゥーンを助けよう！"
QuestsCogOldNewbieQuestObjective = "ｹﾞﾗｹﾞﾗﾎﾟｲﾝﾄが%(laffPoints)d以下のﾄｩｰﾝを助けて%(objective)sをやっつける"
QuestsCogOldNewbieQuestCaption = "ゲラゲラポイントが%d以下のトゥーンを助けよう！"
QuestsCogNewbieQuestAux = "倒す相手："
QuestsNewbieQuestHeadline = "みならい"

QuestsCogTrackQuestProgress = "倒した数：%(progress)s / %(numCogs)s"
QuestsCogTrackQuestHeadline = "ウォンテッド"
QuestsCogTrackQuestSCStringS = "%(cogLoc)s%(cogText)sを倒さなくちゃ！" #★「の」がAnywhereのときに不要
QuestsCogTrackQuestSCStringP = "%(cogLoc)s%(cogText)sを倒さなくちゃ！" #★「の」がAnywhereのときに不要
QuestsCogTrackQuestDefeat = "%sを倒す"
QuestsCogTrackDefeatDesc = "%(trackName)s%(numCogs)s体" #★新規修正（１月２０日）

QuestsCogLevelQuestProgress = "倒した数：%(progress)s / %(numCogs)s"
QuestsCogLevelQuestHeadline = "ウォンテッド"
QuestsCogLevelQuestDefeat = "%sを倒す"
QuestsCogLevelQuestDesc = "レベル%(level)s以上の%(name)s"
QuestsCogLevelQuestDescC = "レベル%(level)s以上の%(name)s%(count)s体"
QuestsCogLevelQuestDescI = "レベル%(level)s以上の%(name)s"
QuestsCogLevelQuestSCString = "%(location)s%(objective)sを倒さなくちゃ！" #★「で」がAnywhereのときに不要

QuestsBuildingQuestFloorNumbers = ('', '２階建以上の', '３階建て以上の', '４階建て以上の', '５階建て以上の')
QuestsBuildingQuestBuilding = "ビル"
QuestsBuildingQuestBuildings = "ビル"
QuestsBuildingQuestHeadline = "とりもどす"
QuestsBuildingQuestProgressString = "とりもどした数：%(progress)s / %(num)s"
QuestsBuildingQuestString = "%sを倒す"
QuestsBuildingQuestSCString = "%(location)s%(objective)sを倒さなくちゃ！" #★「で」がAnywhereのときに不要

QuestsBuildingQuestDesc = "%(type)sビル"
QuestsBuildingQuestDescF = "%(floors)s%(type)sビル"
QuestsBuildingQuestDescC = "%(type)sビル×%(count)s軒"
QuestsBuildingQuestDescCF = "%(floors)s%(type)sビル×%(count)s軒"
QuestsBuildingQuestDescI = "%(type)sビル数軒"
QuestsBuildingQuestDescIF = "%(floors)s%(type)sビル数軒"

QuestFactoryQuestFactory = "コグファクトリー"
QuestsFactoryQuestFactories = "コグファクトリー"
QuestsFactoryQuestHeadline = "やっつける"
QuestsFactoryQuestProgressString = "やっつけた数：%(progress)s / %(num)s"
QuestsFactoryQuestString = "%sを倒す"
QuestsFactoryQuestSCString = "%(location)s%(objective)sを倒さなくちゃ！"

QuestsFactoryQuestDesc = "%(type)s 工場"
QuestsFactoryQuestDescC = "%(type)s 工場×%(count)s"
QuestsFactoryQuestDescI = "%(type)s 工場を数軒"

QuestMintQuestMint = "マネーファクトリー"
QuestsMintQuestMints = "マネーファクトリー"
QuestsMintQuestHeadline = "やっつける"
QuestsMintQuestProgressString = "やっつけた数：%(progress)s / %(num)s"
QuestsMintQuestString = "%sを倒す"
QuestsMintQuestSCString = "%(objective)s%(location)sを倒さなくちゃ！"

QuestsMintQuestDesc = "マネーファクトリー"
QuestsMintQuestDescC = "マネーファクトリー×%(count)s"
QuestsMintQuestDescI = "マネーファクトリー"

QuestsRescueQuestProgress = "助けた数：%(progress)s / %(numToons)s"
QuestsRescueQuestHeadline = "たすける"
QuestsRescueQuestSCStringS = "%(toonLoc)sのトゥーンを助けなくちゃ！"
QuestsRescueQuestSCStringP = "%(toonLoc)sのトゥーンを何人か助けなくちゃ！"
QuestsRescueQuestRescue = "%sを助ける"
QuestsRescueQuestRescueDesc = "トゥーン%(numToons)s人"
QuestsRescueQuestToonS = "トゥーン"
QuestsRescueQuestToonP = "トゥーン"
QuestsRescueQuestAux = "たすける："

QuestsRescueNewNewbieQuestObjective = "新しいトゥーンの仲間と一緒に%sを助けよう！"
QuestsRescueOldNewbieQuestObjective = "ゲラゲラポイント%(laffPoints)d以下のトゥーンと%(objective)sを助けよう！"

QuestCogPartQuestCogPart = "コグスーツの部品"
QuestsCogPartQuestFactories = "コグファクトリー"
QuestsCogPartQuestHeadline = "取り戻す"
QuestsCogPartQuestProgressString = "取り戻した数：%(progress)s / %(num)s"
QuestsCogPartQuestString = "%sを取り戻す"
QuestsCogPartQuestSCString = "%(location)sの%(objective)sを取り戻さなくちゃ！"
QuestsCogPartQuestAux = "取り戻す："

QuestsCogPartQuestDesc = "コグスーツの部品"
QuestsCogPartQuestDescC = "コグスーツの部品×%(count)sつ"
QuestsCogPartQuestDescI = "コグスーツの部品をいくつか"

QuestsCogPartNewNewbieQuestObjective = '新しいトゥーンの仲間と一緒に%sを取り戻そう！'
QuestsCogPartOldNewbieQuestObjective = 'ゲラゲラポイント%(laffPoints)d以下のトゥーンと%(objective)sを取り戻そう！'

QuestsDeliverGagQuestProgress = "デリバリーされた数：%(progress)s / %(numGags)s"
QuestsDeliverGagQuestHeadline = "デリバリー"
QuestsDeliverGagQuestToSCStringS = "%(gagName)sをデリバリーしなくちゃ！"
QuestsDeliverGagQuestToSCStringP = "%(gagName)sをデリバリーしなくちゃ！"
QuestsDeliverGagQuestSCString = "デリバリーしなくちゃ！"
QuestsDeliverGagQuestString = "%sをデリバリーする"
QuestsDeliverGagQuestStringLong = "%sを_toNpcName_にデリバリーする"
QuestsDeliverGagQuestInstructions = "アクセスを許可されたら、このギャグをギャグショップで買うことができるようになるよ。"

QuestsDeliverItemQuestProgress = ""
QuestsDeliverItemQuestHeadline = "デリバリー"
QuestsDeliverItemQuestSCString = "%(article)s%(itemName)sをデリバリーしなくちゃ！"
QuestsDeliverItemQuestString = "%sをデリバリーする"
QuestsDeliverItemQuestStringLong = "%sを_toNpcName_にデリバリーする"

QuestsVisitQuestProgress = ""
QuestsVisitQuestHeadline = "あいにいく"
QuestsVisitQuestStringShort = "あいにいく"
QuestsVisitQuestStringLong = "_toNpcName_に会いに行く"
QuestsVisitQuestSeeSCString = "%sに会いに行かなくちゃ！"
QuestsRecoverItemQuestProgress = "取り返した数：%(progress)s / %(numItems)s"
QuestsRecoverItemQuestHeadline = "とりかえす"
QuestsRecoverItemQuestSeeHQSCString = lHQOfficerM+"に会いに行かなくちゃ。"
QuestsRecoverItemQuestReturnToHQSCString = lHQOfficerM+"に%sを返しに行かなくちゃ。"
QuestsRecoverItemQuestReturnToSCString = "%(npcName)sに%(item)sを返しに行かなくちゃ。"
QuestsRecoverItemQuestGoToHQSCString = "%sに行かなくちゃ。" % lToonHQ
QuestsRecoverItemQuestGoToPlaygroundSCString = "%sのプレイグラウンドに行かなくちゃ。"
QuestsRecoverItemQuestGoToStreetSCString = "%(hood)sの%(street)s%(to)sに行かなくちゃ。" #★
QuestsRecoverItemQuestVisitBuildingSCString = "%s%sに行かなくちゃ。"
QuestsRecoverItemQuestWhereIsBuildingSCString = "%s%sはどこですか？"
QuestsRecoverItemQuestRecoverFromSCString = "%(loc)s%(holder)sから%(item)sを取り返さなくちゃ。"
QuestsRecoverItemQuestString = "%(holder)sから%(item)sを取り返す。"
QuestsRecoverItemQuestHolderString = "%(level)s %(holder)d以上 %(cogs)s"
QuestsTrackChoiceQuestHeadline = "えらぶ"
QuestsTrackChoiceQuestSCString = "%(trackA)sと%(trackB)sのどっちかを選ばなくちゃ"
QuestsTrackChoiceQuestMaybeSCString = "%sにしようかな"
QuestsTrackChoiceQuestString = "%(trackA)sと%(trackB)sのどちらかを選ぶ"
QuestsFriendQuestHeadline = "ともだち"
QuestsFriendQuestSCString = "ともだちを作らなくちゃ"
QuestsFriendQuestString = "ともだちを作る"
QuestsMailboxQuestHeadline = "メール"
QuestsMailboxQuestSCString = "メールをチェックしなくちゃ！"
QuestsMailboxQuestString = "メールをチェックする"
QuestsPhoneQuestHeadline = "クララベル"
QuestsPhoneQuestSCString = "クララベルに電話しなくちゃ！"
QuestsPhoneQuestString = "クララベルに電話する"
QuestsFriendNewbieQuestString = "ゲラゲラポイント%d以下のトゥーン%d人とともだちになる。"
QuestsFriendNewbieQuestProgress = "ともだちの数：%(progress)s / %(numFriends)s"
QuestsFriendNewbieQuestObjective = "ゲラゲラポイント%d以下のトゥーン%d人とともだちになる。"

QuestsTrolleyQuestHeadline = "トロリー"
QuestsTrolleyQuestSCString = "トロリーに乗らなくちゃ"
QuestsTrolleyQuestString = "トロリーに乗る"
QuestsTrolleyQuestStringShort = "トロリーに乗る"
QuestsMinigameNewbieQuestString = "%dミニゲーム"
QuestsMinigameNewbieQuestProgress = "あそんだ数：%(progress)s / %(numMinigames)s"
QuestsMinigameNewbieQuestObjective = "ゲラゲラポイント%d以下のトゥーンと%d回、ミニゲームをする。"
QuestsMinigameNewbieQuestSCString = "新しいトゥーンとミニゲームをしなくちゃ！"
QuestsMinigameNewbieQuestCaption = "ゲラゲラポイント%d以下の新しいトゥーンを助ける。"
QuestsMinigameNewbieQuestAux = "あそぶ："

QuestsMaxHpReward = "ゲラゲラリミットが%sポイントふえました。"
QuestsMaxHpRewardPoster = "ごほうび：%sポイントのゲラゲラブースト"

QuestsMoneyRewardSingular = "ジェリービーンを\n1コゲット"
QuestsMoneyRewardPlural = "ジェリービーンを\n%sコゲット！"
QuestsMoneyRewardPosterSingular = "ごほうび：ジェリービーン1コ"
QuestsMoneyRewardPosterPlural = "ごほうび：ジェリービーン%sコ"

QuestsMaxMoneyRewardSingular = "ジェリービーン1コを持てるようになったよ。"
QuestsMaxMoneyRewardPlural = "ジェリービーン%sコ持てるようになったよ。"
QuestsMaxMoneyRewardPosterSingular = "ごほうび：ジェリービーン１コを持てる"
QuestsMaxMoneyRewardPosterPlural = "ごほうび：ジェリービーン%sコを持てる"

QuestsMaxGagCarryReward = "%(name)sをゲット。ギャグを%(num)sコ持てるようになったよ。"
QuestsMaxGagCarryRewardPoster = "ごほうび：%(name)s (%(num)s)"

QuestsMaxQuestCarryReward = "トゥーンタスクを%sつ持てるようにしよう。"
QuestsMaxQuestCarryRewardPoster = "ごほうび：トゥーンタスクを%sつ持てる"

QuestsTeleportReward = "%sへのワープアクセスをゲット"
QuestsTeleportRewardPoster = "ごほうび：%sへのワープアクセス"

QuestsTrackTrainingReward = "\"%s\"のギャグの練習ができるようになったよ。"
QuestsTrackTrainingRewardPoster = "ごほうび：ギャグの練習"

QuestsTrackProgressReward = "\"%(trackName)s\"のアニメーション %(frameNum)sコマ目をゲット"
QuestsTrackProgressRewardPoster = "ごほうび：\"%(trackName)s\"のアニメーション %(frameNum)sコマ目"

QuestsTrackCompleteReward = "ギャグ\"%s\"を使えるようになったよ。"
QuestsTrackCompleteRewardPoster = "ごほうび：最終トラック%sの練習"

QuestsClothingTicketReward = "服を着替えられるようになったよ。"
QuestsClothingTicketRewardPoster = "ごほうび：ようふく券"

QuestsCheesyEffectRewardPoster = "ごほうび：%s"

QuestsCogSuitPartReward = "コグスーツの部品：%(cogTrack)sの%(part)sをゲット！ "
QuestsCogSuitPartRewardPoster = "ごほうび: %(cogTrack)sの%(part)sパーツ"

# Quest location dialog text
QuestsStreetLocationThisPlayground = "このプレイグラウンドにあるよ。"
QuestsStreetLocationThisStreet = "このストリートにあるよ。"
QuestsStreetLocationNamedPlayground = "%sのプレイグラウンドにあるよ。"
QuestsStreetLocationNamedStreet = "%(toHoodName)sの%(toStreetName)sだよ。"
QuestsLocationString = "%(location)s%(string)s"
QuestsLocationBuilding = "%sの建物は"
QuestsLocationBuildingVerb = "それは"
QuestsLocationParagraph = "\a%(building)s%(buildingName)sだよ。\a%(buildingVerb)s%(street)s"
QuestsGenericFinishSCString = "トゥーンタスクを終わらせなくちゃ。"

# MaxGagCarryReward names
QuestsMediumPouch = "中くらいの袋"
QuestsLargePouch = "大きい袋"
QuestsSmallBag = "小さい袋"
QuestsMediumBag = "中くらいのバッグ"
QuestsLargeBag = "大きいバッグ"
QuestsSmallBackpack = "小さいリュック"
QuestsMediumBackpack = "中くらいのリュック"
QuestsLargeBackpack = "大きいリュック"
QuestsItemDict = {
    1 : ["めがね", "めがね", ""],
    2 : ["かぎ", "かぎ", ""],
    3 : ["こくばん", "こくばん", ""],
    4 : ["ほん", "ほん", ""],
    5 : ["チョコレート", "チョコレート", ""],
    6 : ["チョーク", "チョーク", ""],
    7 : ["レシピ", "レシピ", ""],
    8 : ["ノート", "ノート", ""],
    9 : ["ＡＴＭ", "ＡＴＭ", ""],
    10 : ["ピエロ車のタイヤ", "ピエロ車のタイヤ", ""],
    11 : ["くうきいれ", "くうきいれ", ""],
    12 : ["タコのすみ", "タコのすみ", ""],
    13 : ["つつみ", "つつみ", ""],
    14 : ["きんぎょのレシート", "きんぎょのレシート", ""],
    15 : ["きんぎょ", "きんぎょ", ""],
    16 : ["オイル", "オイル", ""],
    17 : ["あぶら", "あぶら", ""],
    18 : ["みず", "みず", ""],
    19 : ["ギアレポート", "ギアレポート", ""],
    20 : ["黒板消し", "黒板消し", ""],

    # This is meant to be delivered to NPCTailors to complete
    # ClothingReward quests
    110 : ["ようふくのチケット", "ようふくのチケット", "    "],
    1000 : ["ようふく券", "ようふく券", ""],

    # Donald's Dock quest items
    2001 : ["インナーチューブ", "インナーチューブ", ""],
    2002 : ["かためがねの処方せん", "かためがねの処方せん", ""],
    2003 : ["めがねのフレーム", "めがねのフレーム", ""],
    2004 : ["かためがね", "かためがね", ""],
    2005 : ["しろいカツラ", "しろいカツラ", ""],
    2006 : ["たくさんのじゃり", "たくさんのじゃり", ""],
    2007 : ["コグ・ギア", "コグ・ギア", ""],
    2008 : ["かいず", "かいず", ""],
    2009 : ["よごれたクロヴィス", "よごれたクロヴィス", ""],
    2010 : ["きれいなクロヴィス", "きれいなクロヴィス", ""],
    2011 : ["とけいのばね", "とけいのばね", ""],
    2012 : ["カウンターウェイト", "カウンターウェイト", ""],

    # Minnie's Melodyland quest items
    4001 : ["ティナのもくろく", "ティナのもくろく", ""],
    4002 : ["ユキのもくろく", "ユキのもくろく", ""],
    4003 : ["もくろくひょう", "もくろくひょう", ""],
    4004 : ["バイオレットのもくろく", "バイオレットのもくろく", ""],
    4005 : ["モックンのチケット", "モックンのチケット", ""],
    4006 : ["タバサのチケット", "タバサのチケット", ""],
    4007 : ["バリーのチケット", "バリーのチケット", ""],
    4008 : ["くもったカスタネット", "くもったカスタネット", ""],
    4009 : ["あおいイカのすみ", "あおいイカのすみ", ""],
    4010 : ["とうめいなカスタネット", "とうめいなカスタネット", ""],
    4011 : ["レオの歌詞カード", "レオの歌詞カード", ""],

    # Daisy's Gardens quest items
    5001 : ["シルクのネクタイ", "シルクのネクタイ", ""],
    5002 : ["しましまのスーツ", "しましまのスーツ", ""],
    5003 : ["はさみ", "はさみ", ""],
    5004 : ["はがき", "はがき", ""],
    5005 : ["ペン", "ペン", ""],
    5006 : ["インクつぼ", "インクつぼ", ""],
    5007 : ["メモちょう", "メモちょう", ""],
    5008 : ["かぎばこ", "かぎばこ", ""],
    5009 : ["とりのえさ", "とりのえさ", ""],
    5010 : ["スプロケット", "スプロケット", ""],
    5011 : ["サラダ", "サラダ", ""],
    5012 : [lDaisyGardens+"のかぎ", lDaisyGardens+"のかぎ", ""],
    5013 : [lSellbotHQ+' 設計図', lSellbotHQ+' 設計図', ''],
    5014 : [lSellbotHQ+'のメモ', lSellbotHQ+'のメモ', ''],
    5015 : [lSellbotHQ+'のメモ', lSellbotHQ+'のメモ', ''],
    5016 : [lSellbotHQ+'のメモ', lSellbotHQ+'のメモ', ''],
    5017 : [lSellbotHQ+'のメモ', lSellbotHQ+'のメモ', ''],

    # The Brrrgh quests
    3001 : ["サッカーボール", "サッカーボール", ""],
    3002 : ["そり", "そり", ""],
    3003 : ["こおり", "こおり", ""],
    3004 : ["ラブレター", "ラブレター", ""],
    3005 : ["ダックスフント", "ダックスフント", ""],
    3006 : ["こんやくゆびわ", "こんやくゆびわ", ""],
    3007 : ["いわしのひげ", "いわしのひげ", ""],
    3008 : ["いたみどめ", "いたみどめ", ""],
    3009 : ["ぬけおちた歯", "ぬけおちた歯", ""],
    3010 : ["きんの歯", "きんの歯", ""],
    3011 : ["まつぼっくりパン", "まつぼっくりパン", ""],
    3012 : ["でこぼこチーズ", "でこぼこチーズ", ""],
    3013 : ["ふつうのスプーン", "ふつうのスプーン", ""],
    3014 : ["しゃべるカエル", "しゃべるカエル", ""],
    3015 : ["アイスクリーム", "アイスクリーム", ""],
    3016 : ["カツラのこな", "カツラのこな", ""],
    3017 : ["アヒルのにんぎょう", "アヒルのにんぎょう", ""],
    3018 : ["もこもこサイコロ", "もこもこサイコロ", ""],
    3019 : ["マイクロフォン", "マイクロフォン", ""],
    3020 : ["キーボード", "キーボード", ""],
    3021 : ["あつぞこのくつ", "あつぞこのくつ", ""],
    3022 : ["キャビア", "キャビア", ""],
    3023 : ["メイクのこな", "メイクのこな", ""],
    3024 : ["毛糸", "毛糸", "" ],
    3025 : ["あみ針", "あみ針", ""],
    3026 : ["アリバイ", "アリバイ", ""],
    3027 : ["気温センサー", "気温センサー", ""],
    
    #Dreamland Quests
    6001 : ["マネーボット本部プラン", "マネーボット本部プラン", ""],
    6002 : ["ロッド", "ロッド", ""],
    6003 : ["自動車のベルト", "自動車のベルト", ""],
    6004 : ["ペンチ", "ペンチ", ""],
    6005 : ["読書ランプ", "読書ランプ", ""],
    6006 : ["シタール", "シタール", ""],
    6007 : ["せいひょうき", "せいひょうき", ""],
    6008 : ["しまうまのざぶとん", "しまうまのざぶとん", ""],
    6009 : ["ひゃくにちそう", "ひゃくにちそう", ""],
    6010 : ["ザイデコのレコード", "ザイデコのレコード", ""],
    6011 : ["ズッキーニ", "ズッキーニ", ""],
    6012 : ["ズート･スーツ", "ズート･スーツ", ""],
    
    #Dreamland+1 quests
    7001 : ["プレーンベッド", "プレーンベッド", ""],
    7002 : ["ファンシーベッド", "ファンシーベッド", ""],
    7003 : ["青いベッドカバー", "青いベッドカバー", ""],
    7004 : ["ペーズリーのベッドカバー", "ペーズリーのベッドカバー", ""],
    7005 : ["まくら", "まくら", ""],
    7006 : ["かたいまくら", "かたいまくら", ""],
    7007 : ["パジャマ", "パジャマ", ""],
    7008 : ["足つきパジャマ", "足つきパジャマ", ""],
    7009 : ["赤の足つきパジャマ", "赤の足つきパジャマ", ""],
    7010 : ["ピンクの足つきパジャマ", "ピンクの足つきパジャマ", ""],
    7011 : ["カリフラワーサンゴ", "カリフラワーサンゴ", ""],
    7012 : ["ねばねばコンブ", "ねばねばコンブ", ""],
    7013 : ["ごますり棒", "ごますり棒", ""],
    7014 : ["しわのばしクリーム", "しわのばしクリーム", ""],
    }
QuestsHQOfficerFillin = lHQOfficerM
QuestsHQWhereFillin = ""
QuestsHQBuildingNameFillin = lToonHQ
QuestsHQLocationNameFillin = "どのエリアでも"

QuestsTailorFillin = "ようふく屋"
QuestsTailorWhereFillin = ""
QuestsTailorBuildingNameFillin = "ようふく屋"
QuestsTailorLocationNameFillin = "どんなエリアでも"
QuestsTailorQuestSCString = "ようふく屋に行かなくちゃ"

QuestMovieQuestChoiceCancel = "トゥーンタスクが必要ならまた後で来てね！じゃあね！"
QuestMovieTrackChoiceCancel = "決められるようになったらまた来てね！バイバイ！"
QuestMovieQuestChoice = "トゥーンタスクを選んでね。"
QuestMovieTrackChoice = "トラックを選んだかい？選べないならまた後でおいで！"

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
    QUEST : "準備は整った。\aさあ、選びたいトラックがわかるまで世界中を旅してみよう。\aキミにとって最後のトラックになるから、良いものを選んでね。\aトラックを選んだらまたここに戻っておいで。！",
    INCOMPLETE_PROGRESS : "良いものを選んだほうがいいよ。",
    INCOMPLETE_WRONG_NPC : "良いものを選んだほうがいいよ。",
    COMPLETE : "いい選択だ！",
    LEAVING : "新しいスキルをマスターしたらまたおいで。幸運を祈ってるよ！",
    }

QuestDialog_3225 = {
    QUEST : "ああ、_avName_！\aこのサラダを_toNpcName_にデリバリーしなくちゃいけないのに、配達人がコグ達のせいで逃げ帰ってしまったんだ。\aキミにデリバリーをお願いしてもいいかな？助かるよ！_where_"
    }

QuestDialog_2910 = {
    QUEST : "ずいぶん早かったね。\aバネの件、本当によくやった。\a最後のアイテムはカウンターウェイトだ。\a_toNpcName_のところに寄って、持って帰れるものを持って帰ってきてくれ。_where_"
    }

QuestDialogDict = {
    160 : {GREETING : "",
           QUEST : "今のキミならもっと難しいものにチャレンジできるだろう。\aボスボットを３体退治してきてくれ。",
           INCOMPLETE_PROGRESS : "" + Cogs + "達はトンネルの向こうのストリートあたりにいるよ。",
           INCOMPLETE_WRONG_NPC : "うまくボスボットを退治できたね。さ、トゥーンＨＱに行ってごほうびをもらってこよう！",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    161 : {GREETING : "",
           QUEST : "今のキミならもっと難しいものにチャレンジできるだろう。\aロウボットを３体退治してきてくれ。",
           INCOMPLETE_PROGRESS : "" + Cogs + "達はトンネルの向こうのストリートあたりにいるよ。",
           INCOMPLETE_WRONG_NPC : "うまくロウボットを退治できたね。さ、トゥーンＨＱに行っててごほうびをもらってこよう！",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    162 : {GREETING : "",
           QUEST : "今のキミならもっと難しいものにチャレンジできるだろう。\aマネーボットを３体退治してきてくれ。",
           INCOMPLETE_PROGRESS : "" + Cogs + "達はトンネルの向こうのストリートあたりにいるよ。",
           INCOMPLETE_WRONG_NPC : "うまくマネーボットを退治できたね。さ、トゥーンＨＱに行ってごほうびをもらってこよう！",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    163 : {GREETING : "",
           QUEST : "今のキミならもっと難しいものにチャレンジできるだろう。\aセルボットを３体退治してきてくれ。",
           INCOMPLETE_PROGRESS : "" + Cogs + "達はトンネルの向こうのストリートあたりにいるよ。",
           INCOMPLETE_WRONG_NPC : "うまくセルボットを退治できたね。さ、トゥーンＨＱに行ってごほうびをもらってこよう！",
           COMPLETE : QuestsDefaultComplete,
           LEAVING : QuestsDefaultLeaving,
           },
    164 : {QUEST : "そろそろ新しいギャグが必要ってとこかな？\aフリッピーなら手伝ってくれるかもしれないよ。_where_" },
    165 : {QUEST : "持ってるギャグの練習が必要みたいだね。\aコグにギャグをくらわせるたびにキミの経験値はあがるんだ。\a十分に経験をつんだらもっといいギャグを使えるようになるよ。\aまずはコグを４体やっつけて、ギャグの練習をしよう。"},
    166 : {QUEST : "うまくコグを倒すことができたね。\aところで、コグにはロウボット・マネーボット・セルボット・ボスボットの４種類があるって知ってた？\aコグの種類は色と名前のラベルでわかるよ。\aまずは練習に４体のボスボットを倒してみよう。"},
    167 : {QUEST : "うまくコグを倒すことができたね。\aところで、コグにはロウボット・マネーボット・セルボット・ボスボットの４種類があるって知ってた？\aコグの種類は色と名前のラベルでわかるよ。\aまずは練習に４体のロウボットを倒してみよう。"},
    168 : {QUEST : "うまくコグを倒すことができたね。\aところで、コグにはロウボット・マネーボット・セルボット・ボスボットの４種類があるって知ってた？\aコグの種類は色と名前のラベルでわかるよ。\aまずは練習に４体のセルボットを倒してみよう。"},
    169 : {QUEST : "うまくコグを倒すことができたね。\aところで、コグにはロウボット・マネーボット・セルボット・ボスボットの４種類があるって知ってた？\aコグの種類は色と名前のラベルでわかるよ。\aまずは練習に４体のマネーボットを倒してみよう。"},
    170 : {QUEST : "よくやったね、これでキミも４種類のコグとその違いがわかったはずだ。\aさて、キミもそろそろ３つめのギャグトラックの練習を始められそうだね。\a_toNpcName_なら次のギャグトラックを選ぶにあたって良いアドバイスをしてくれるよ。_where_" },
    171 : {QUEST : "よくやったね、これでキミも４種類のコグとその違いがわかったはずだ。\aさて、キミもそろそろ３つめのギャグトラックの練習を始められそうだね。\a_toNpcName_なら次のギャグトラックを選ぶにあたって良いアドバイスをしてくれるよ。_where_" },
    172 : {QUEST : "よくやったね、これでキミも４種類のコグとその違いがわかったはずだ。\aさて、キミもそろそろ３つめのギャグトラックの練習を始められそうだね。\a_toNpcName_なら次のギャグトラックを選ぶにあたって良いアドバイスをしてくれるよ。_where_" },

    175 : {GREETING : "",
           QUEST : "キミのトゥーン専用のおうちがあるって知ってた？\a牛のクララベルは電話のショッピングカタログで、キミのおうちをかざる家具を売ってるよ。\aスピードチャットのセリフや服、他にもたくさんの楽しいアイテムを買えるよ。\aクララベルに最初のカタログを送るように言っておくね。\a毎週、新しいアイテムのカタログが届くよ。\aおうちへ帰って、クララベルに電話してみよう！",
           INCOMPLETE_PROGRESS : "おうちへ帰って、クララベルに電話してね。",
           COMPLETE : "お買い物、楽しかったでしょ！\aわたしもちょうど、自分のおうちの模様替えをしたところなんだ。\aトゥーンタスクをこなして、もっとごほうびをもらおう！",
           LEAVING : QuestsDefaultLeaving,
           },

    400 : {GREETING : "",
           QUEST : "「なげる」と「みずでっぽう」もおもしろいけど、レベルの高いコグと戦うにはギャグがもっと必要だね。\a他のトゥーンと組んでコンビアタックをすればダメージも増大するよ。\aいろんなギャグのコンビネーションを試してみて、何が一番効果的か見てみるといい。\a次のトラックでは「サウンド」と「トゥーンナップ」から選んでみたらどうかな。\a「サウンド」は１回でその場にいる全てのコグにダメージを与えられるし、「トゥーンアップ」はバトル中に他のトゥーンを回復してあげられるよ。\aキミの決心がついたら、またここに戻ってきてね。",
           INCOMPLETE_PROGRESS : "ずいぶん早かったね！どれにするか決めたかい？",
           INCOMPLETE_WRONG_NPC : "選択する前に、もう一度よく考えてね。",
           COMPLETE : "いい選択だ。そのギャグを使えるようになるには練習が必要だ。\a練習が出来るようになるのはトゥーンタスクをいくつかこなしてから。\aタスクひとつでギャグアタックのアニメーション１コマが与えられる。\a１５個すべてをそろえたら、新しいギャグが使えるようになる『最後のギャグ練習』のタスクがもらえるよ。\aトゥーンガイドで進行ぐあいをチェックしよう。",
           LEAVING : QuestsDefaultLeaving,
           },
    1039 : { QUEST : "街でもっと動けるようになりたかったら、_toNpcName_に会うといい。_where_" },
    1040 : { QUEST : "街でもっと動けるようになりたかったら、_toNpcName_に会うといい。_where_" },
    1041 : { QUEST : "おや、お客かい？\aトゥーンタウンでの移動にはワープホールというものが便利だよ。\aそれを使えば、ともだちリストで選んだ友達やトゥーンガイドの地図で選んだエリアにワープできるんだ。\aそうだ、ぼくの友達を助けてくれたらキミのトゥーンタウンセントラルへのワープアクセスを可能にしてあげるよ。\aルーピー・ストリートでコグ達がトラブルを起こしてるみたい。_toNpcName_に会ってきてくれ。_where_" },
    1042 : { QUEST : "おや、お客かい？\aトゥーンタウンでの移動にはワープホールというものが便利だよ。\aそれを使えば、ともだちリストで選んだともだちやトゥーンガイドの地図で選んだエリアにワープできるんだ。\aそうだ、ぼくの友達を助けてくれたらキミのトゥーンタウンセントラルへのワープアクセスを可能にしてあげるよ。\aルーピー・ストリートでコグ達がトラブルを起こしてるみたい。_toNpcName_に会ってきてくれ。_where_" },
    1043 : { QUEST : "おや、お客かい？\aトゥーンタウンでの移動にはワープホールというものが便利だよ。\aそれを使えば、ともだちリストで選んだともだちやトゥーンガイドの地図で選んだエリアにワープできるんだ。\aそうだ、ぼくの友達を助けてくれたらキミのトゥーンタウンセントラルへのワープアクセスを可能にしてあげるよ。\aルーピー・ストリートでコグ達がトラブルを起こしてるみたい。_toNpcName_に会ってきてくれ。_where_" },
    1044 : { QUEST : "来てくれてありがとな、実は今助けが必要なんだ。\a見ての通り、ウチの店には客がいない。\a実は秘伝のレシピが盗まれてしまって、おかげでそれからお客が来なくなちゃったんだ。\a最後に見たのは、ぼくのビルがコグ達に乗っ取られる直前。\aお願いだ、ぼくの秘伝のレシピを取り返してくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "レシピは見つかったかい？" },
    1045 : { QUEST : "ああ、ありがとう！\aきっと近いうちに全部取り返してレストランを再開するよ。\aそうそう、キミにメモがあるんだった…ワープアクセスだっけ。\a『友達を助けてくれてありがとう、これをトゥーンＨＱに持って行ってくれ』だって。\a本当に助かったよ、じゃあね！",
             LEAVING : "",
             COMPLETE : "ふむ、なるほど、キミはルーピー・ストリートの住民の手助けをしてくれたようだな。\aトゥーンタウンセントラルへのワープアクセスが欲しいとの事だが、宜しい。\aアクセスを与えよう。\aこれからはトゥーンタウンのほとんどどこからでもプレイグラウンドにワープできるようになる。\a地図をひらいてトゥーンタウンセントラルをクリックするだけで移動できるようになるぞ。" },
    1046 : { QUEST : "ここのところ、ファニマニ銀行はマネーボット達に悩まされている。\aもし良かったらそこに行って助けてやってくれないか。_where_" },
    1047 : { QUEST : "マネーボット達が、銀行にこっそり入ってうちの機械を盗んでいるんです。\aお願い、ＡＴＭを５台、マネーボット達から取り返してきて。\a何回も往復しなくて済むように、一度に全部持ってきてくれるといいわ",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "まだＡＴＭを探してるの？" },
    1048 : { QUEST : "マシンを探してくれたのね、ありがとう！\aえーと…少しキズがついてるみたい。\aねえ、これを\"くすぐりマシーン\"にいる_toNpcName_のところに持っていってもらえるかな。彼女なら直せるかもしれない。",
             LEAVING : "", },
    1049 : { QUEST : "こわれたＡＴＭ?\aマネーボットにやられた？\aま、とにかく見てみようか。\aなるほど、ギアが取れてる…しかもウチには在庫がないわ。\a大きなコグ達が持ってるコグ・ギアなら使えるかもしれない。\aそうね、レベル３のコグ・ギアをマシン１台につき２つ使うから、全部で１０コ取ってきて。\a一度に全部持ってきてね、マシンを一気に直してあげるわ",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "マシンを直すには１０コのギアが必要よ、忘れないようにね！" },
    1053 : { QUEST : "いっちょあがり！\aさ、マシンも全部直ったわよ。お代はけっこう。\aこいつらをファニマニバンクに持ってった時に私からもヨロシク言っといて",
             LEAVING : "",
             COMPLETE : "ＡＴＭが全部直ったって？\aありがとう。ええと、なにかお礼にあげるものがあるといいんだけど…" },
    1054 : { QUEST : "_toNpcName_がピエロ車のヘルプを欲しがっているみたいだよ。_where_" },
    1055 : { QUEST : "オウノウ！ボクの愛しいピエロ車のタイヤがみつからないよ！\aねえキミ、ちょっと助けてくれないかい？\aもしかしたらルーピー・ボブがトゥーンタウンセントラルの遊び場の池に投げちゃったかも…\aどこかのドックに行ってつり上げてみてくれないかな？",
             GREETING : "イヤッホーイ！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "タイヤを４つともつり上げるのはやっぱりむずかしい？" },
    1056 : { QUEST : "ウワオ、ワンダフル！おかげでこのピエロ車もまた路上で走ることができるよ。\aん？この辺に空気ポンプがあると思ったんだけど…\a_toNpcName_が借りていったのかな？\a彼が持ってるかどうか、聞いてきてくれないかい？_where_",
             LEAVING : "" },
    1057 : { QUEST : "よう！\aえ、空気ポンプ？\aそうだな、じゃあキミがこのへんのストリートを荒らしてるハイレベルのコグを倒してくれたら渡すってのはどうだい？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キミの実力はそんなものなのか？" },
    1058 : { QUEST : "やったな！キミなら出来ると思ったよ。\aほら、約束の空気ポンプだ。_toNpcName_も喜ぶだろう。",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "ヤッホウ！旅立ちの時は来た！\aああそうだ、助けてくれてほんとうにありがとう。\aこれをあげるよ。" },
    1059 : { QUEST : "_toNpcName_の店だが、在庫が足りなくて困っているらしい。助けてやってみるのも悪くないんじゃないか？_where_" },
    1060 : { QUEST : "来てくれてありがとう！\aあのコグのやつらめ、私のインクを盗んでいってるので店の在庫がすごく減ってきてしまっているんだ。\a池のタコからスミをとってきてくれないか？タコをつる時は池の近くのドックに立つといい。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "釣りは苦手なのかい？" },
    1061 : { QUEST : "おお、スミだ、助かった！\aそうだ、これからもインクに困ることがないようにするためにもカリカリン達を退治してくれないか？\aトゥーンタウンセントラルでカリカリンを６体退治してくれたらお礼をあげるよ。",
             LEAVING : "",
             COMPLETE : "ありがとう！これはお礼だよ。",
             INCOMPLETE_PROGRESS : "カリカリンがまだいるのを見たんだが…" },
    1062 : { QUEST : "おお、スミだ、助かった！\aそうだ、これからもインクに困ることがないようにするためにもガッツキー達を退治してくれないか？\aトゥーンタウンセントラルでガッツキーを６体退治してくれたらお礼をあげるよ。",
             LEAVING : "",
             COMPLETE : "ありがとう！これはお礼だよ。",
             INCOMPLETE_PROGRESS : "ガッツキーがまだいるのを見たんだが…" },
    900 : { QUEST : "_toNpcName_が配達物で困ってるって聞いたよ。_where_" },
    1063 : { QUEST : "やあ、来てくれてありがとう。\a実は手元にあった包みがコグに盗まれてしまったんだ。\a取り返してくれると助かるよ。\aやつはレベル３みたいだったから、包みが見つかるまでレベル３のコグを退治するといいだろう。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "なかなか見つけられないみたいだね。" },
    1067 : { QUEST : "ああ、これだ！ありがとう！\aっと、送り先が汚れちゃったな…\aナントカ博士あてだって事しか読み取れない。\a_toNpcName_のことかな、配達してくれないか？_where_",
             LEAVING : "" },
    1068 : { QUEST : "私に配達が来るはずはないんだが…ドクター・ハッピーの間違いじゃないかい？\a私の助手があちらに行く予定だから、その時にでも聞いてもらおう。\aところで、このストリートにいるコグを少々退治してもらって良いかな？\aトゥーンタウンセントラルにいるコグ１０体ほどでも助かるよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "助手がまだ戻ってきていないんだ" },
    1069 : { QUEST : "ドクター・ハッピーにも配達がある予定ではなかったそうだ。\aしかも、マネーボットが助手の手から包みを奪ってしまったらしい…\a取り戻してくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "なかなか見つけられないみたいだね。" },
    1070 : { QUEST : "ドクター・ハッピーにも配達がある予定ではなかったそうだ。\aしかも、セルボットが助手の手から包みを奪ってしまったらしい…\a申し訳ないが、そのセルボットを見つけて包みを取り返してくれないか。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "なかなか見つけられないみたいだね。" },
    1071 : { QUEST : "ドクター・ハッピーにも配達がある予定ではなかったそうだ。\aしかも、ボスボットが助手の手から包みを奪ってしまったらしい…\a取り戻してくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "なかなか見つけられないみたいだね。" },
    1072 : { QUEST : "取り戻せたんだね、すばらしい！\aその包みはもしかしたら_toNpcName_に持って行くべきものかもしれないね。_where_",
             LEAVING : "" },
    1073 : { QUEST : "ああ、包みを持ってきてくれてありがとう。\aん？包みの数は２つだったはずだが…_toNpcName_がもうひとつを持っているか聞いてきてくれると助かるよ。",
             INCOMPLETE : "もうひとつの包み、見つかったかい？",
             LEAVING : "" },
    1074 : { QUEST : "もうひとつあるはずだって？それもコグに盗まれたのかなぁ。\aコグを退治しつづけたらそのうち見つかるだろう。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "もうひとつの包みもなかなか見つけられないみたいだね。" },
    1075 : { QUEST : "やっぱりふたつ目もあったんだなぁ。\aさ、急いでこれを_toNpcName_に届けてくれ、私の謝罪の言葉もそえて",
             COMPLETE : "やっと届いた！\aキミは心優しいトゥーンだね。これをあげよう。きっと役に立つよ。",
             LEAVING : "" },
    1076 : { QUEST : "14金魚の店で何かあったようだ。\a_toNpcName_も助けが必要だろう。_where_" },
    1077 : { QUEST : "ああ、来てくれてありがとう。コグが私の金魚をみんな盗んで行ってしまったんだ！\aあいつら、盗んだ金魚を売りさばいて小銭稼ぎするつもりなんだ。\aあの５匹の金魚は、この小さな店で私と何年も共に過ごした相棒達なんだ。\a取り返してくれると本当に、本当に助かるよ。\a１体のコグが５匹とも運んでいるだろう。\a金魚を見つけるまでコグをやっつけてくれ！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "金魚を取り返してくれ～" },
    1078 : { QUEST : "金魚が見つかったのか！？\aえ？これは…レシート？\aはぁ…コグのやつらめ。\aでもこれじゃ何が書いてあるかわからんな。_toNpcName_のところにこれを持って行って、読めるかどうか聞いてきてくれ。_where_",
             INCOMPLETE : "_toNpcName_はなんて言ってた？",
             LEAVING : "" },
    1079 : { QUEST : "まずそのレシートを見せてくれ。\aふむ…なるほど、ここには１匹の金魚がオベッカーに買い取られた、とあるな。\a他の４匹のことは書いてないから、このオベッカーを見つけて問いただした方がよかろう。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "私に出来ることはもうないよ。金魚を探しに行った方がいいんじゃないかね？" },
    1092 : { QUEST : "まずそのレシートを見せてくれ。\aふむ…なるほど、ここには１匹の金魚がチョロマカシーに買い取られた、とあるな。\a他の４匹のことは書いてないから、このチョロマカシーを見つけて問いただした方がよかろう。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "私に出来ることはもうないよ。金魚を探しに行った方がいいんじゃないかね？" },
    1080 : { QUEST : "ああ、神様！オスカーを見つけてくれたんだね、彼は私の一番のお気に入りなんだ。\aえ、なんだって、オスカー？…そうなのか？\aオスカーが言うには、他の４匹遊び場の池に逃げたらしい。\a池に行って彼らを集めてくれないか？釣り上げるだけでいいはずだ。",
             LEAVING : "",
             COMPLETE : "ああ、なんと幸せなことなんだ！大事な大事な、小さな友達が帰ってきた！\aキミにはきちんとお礼をするべきだな。",
             INCOMPLETE_PROGRESS : "金魚が見つからないのかい？" },
    1081 : { QUEST : "どうやら_toNpcName_が面倒なシチュエーションにあるようだ。ねえ、良かったら彼女に手を貸してやってくれないか。_where_" },
    1082 : { QUEST : "何が起こったって、速乾性のノリをこぼしちゃってこんなことになっちゃったのよ。\aこのシチュエーションをなんとかする手があったら聞いてみたいわよ。\a…あ、そうだわ、手伝ってくれない？\aセルボットを何体か倒してオイルを持ってきてちょうだい。",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "このべたべた地獄から助けて～" },
    1083 : { QUEST : "うーん、オイルもあんまり役にたたないみたい…\a一体どうすればいいのかしら。\aあとは…そうね、アレならなんとかなるかも。\aロウボットを何体か倒して、油を持ってきてちょうだい。",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "このべたべた地獄から助けて～" },
    1084 : { QUEST : "ああ、これもだめだわ！んもう！\a油に賭けてたのに…\aん？賭け？ねえ、思いついたわ。\aマネーボットを何体か倒して、お水を持ってきてちょうだい。",
             LEAVING : "",
             GREETING : "",
             COMPLETE : "やったわ、速乾ノリ地獄から脱出よ！\aありがとう、これはお礼よ。\nこれはバトル中にもうちょっと笑う時間が長く…\aあらやだ！またくっついちゃったわ！",
             INCOMPLETE_PROGRESS : "このべたべた地獄から助けて～" },
    1085 : { QUEST : "_toNpcName_がコグについての研究をしているわ。\a助けたいなら彼に話してみるべきね。_where_" },
    1086 : { QUEST : "いかにも、私はコグについての研究をしている。\a彼らがどのような作りになっているかを知りたいんだ。\aキミにコグのギアをいくつか集めてもらえると助かるんだがね。\a研究には大きめのギアが必要だから、レベル２以上で頼むよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "なかなか数が集まらないみたいだね？" },
    1089 : { QUEST : "よし、さっそく見てみよう。ふむ、これは素晴らしいサンプルだ！\aふむふむ…\aさ、レポートができたぞ。これをトゥーンＨＱに大至急持って行ってくれ。",
             INCOMPLETE : "私のレポートをトゥーンＨＱに持って行ってくれたかね？",
             COMPLETE : "ありがとう、_avName_。ここからは我々に任せてくれ。",
             LEAVING : "" },
    1090 : { QUEST : "キミにとって役立ちそうな情報を_toNpcName_が持っているよ。_where_" },
    1091 : { QUEST : "トゥーンＨＱは、いわゆるコグ・レーダーのようなものを開発しているらしい。\aそれを使えばコグを見つけるのも簡単になるってわけだ。\aキミのトゥーンガイドの中のコグページが重要なんだ。\aコグ達をある程度やっつけたら、コグのシグナルが入って来るようになる。 どこにいるかわかるようになるんだ。\aがんばってコグ達の退治を続けていれば、出来るようになるぞ。",
             COMPLETE : "よくやった！これはきっとキミの役に立つだろう。",
             LEAVING : "" },
    401 : {GREETING : "",
           QUEST : "次に覚えたいギャグを選ぼう。\aじっくり考えてから決めてね。\a決める準備ができたらここに戻っておいで。",
           INCOMPLETE_PROGRESS : "選択する前に、もう一度よく考えてね。",
           INCOMPLETE_WRONG_NPC : "選択する前に、もう一度よく考えてね。",
           COMPLETE : "いい選択だ。",
           LEAVING : QuestsDefaultLeaving,
           },
    2201 : { QUEST : "コグのやつらめ、またやってくれたようだ。\a_toNpcName_がアイテムの盗難を報告してきたんだ、解決してやってくれないか。_where_" },
    2202 : { QUEST : "こんにちは、_avName_。キミが来てくれて本当によかったよ！\a怖いツラしたセコビッチがついさっき、ボクのインナーチューブを盗んで走り去っていってしまったんだ。\aもしかしたらあいつらの悪巧みに使われてしまうかもしれない。\aお願いだ、どうか探し出して持ってきてほしい。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "ボクのインナーチューブ、見つかった？",
             COMPLETE : "見つけてくれたんだね、ボクのインナーチューブ！ほんとに腕がいいんだねぇ。はい、これはボクのキモチだよ。",
             },
    2203 : { QUEST : "コグ達が銀行で大暴れしてるらしい。\aキャプテン・カールがそこにいるから、何か手助けできるか聞いてあげて。_where_" },
    2204 : { QUEST : "おお、ちょうどいいところに来てくれたな！\aあんのにっくきクズ鉄のガラクタ達め、我輩の片めがねを壊しおった！おかげで小銭が数えられなくなってしまったわい。\aそこでだ。キミにはドクター・キーケグにこの処方箋を持っていって、新しい片めがねを持ってきてもらいたいのだ。_where_",
             GREETING : "",
             LEAVING : "",
             },
    2205 : { QUEST : "おお、これはこれは。\aこの処方箋の対処をしたいのはやまやまなんだが、コグ達が私のモノを盗んでいっていてな…\aオベッカーからめがねのフレームを取ってこられるのであれば、なんとかしてやれるかもしれないが。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "オベッカーのフレームがなけりゃ片めがねも作れんよ。",
             },
    2206: { QUEST : "持ってきたか、すばらしい！\aちょっとそこで待っていなさい…\aさ、処方箋通りに作ったぞ。さっそくキャプテン・カールに持って行ってやりなさい。_where_",
            GREETING : "",
            LEAVING : "",
            COMPLETE : "ほほう！\aこれはまことにありがたい。\aこれは我輩の気持ちだ、受け取ってくれい。",
            },
    2207 : { QUEST : "バーバラ・シェルの店にコグが出た！\aさくっと行ってさくっとやっつけてやってくれ。_where_" },
    2208 : { QUEST : "あらン、今ちょうど逃げてっちゃったのよね。\aウラギリンが入ってきて、あたしの白いカツラを盗んで逃げていったの。\aボスのためだとか、法的な先例だとかなんとか言ってたわよ。\a取り返してきてくれたらすっごぉく嬉しい！",
             LEAVING : "",
             GREETING : "",
             INCOMPLETE_PROGRESS : "まだ見つかってないのぉ？\aええとね、あいつは背が高くて頭がとんがってたわよ。",
             COMPLETE : "見つかったのぉ！？\aああん、バーバラうれしい！\aこんなものじゃお礼にならないかもしれないけど…",
             },
    2209 : { QUEST : "メルヴィルが大事な航海にむけて準備中だって。\a忙しいだろうから、行って手伝ってあげて。_where_"},
    2210 : { QUEST : "今、まさにネコの手も借りたい状態だよ。\aわしはコグ達が一体どこから来ているのかを調べるようトゥーンＨＱに依頼されたんだ\a船に必要なものがまだまだあるんだが、何しろジェリービーンが足らなくてな。\aアリスのところから砂利を持ってきてくれんか？もちろんタダじゃもらえんだろうが…頼む。_where_",
             GREETING : "やあ、_avName_",
             LEAVING : "",
             },
    2211 : { QUEST : "メルヴィルが砂利を欲しがってるって？\aったく、前回の分もまだ支払ってないのにさ。\aこのストリートでガミガミーナを５体やっつけたら砂利をあげるよ。",
             INCOMPLETE_PROGRESS : "５体よ、ご・た・い。",
             GREETING : "いらっしゃい！",
             LEAVING : "",
             },
    2212 : { QUEST : "よし、追い払ってくれたね。\aほれ、この砂利をあのケチくさメルヴィルに持っていってやんな。_where_",
             GREETING : "あれまあ、誰かと思ったら…",
             LEAVING : "",
             },
    2213 : { QUEST : "思ったとおりだ、すばらしい。彼女も聞く耳を持ってるじゃないか。\aさて、次は海図だ。これはアートのところだな。\aここでもわしの評判はよくないだろうから、またタダ働きするはめになると思うが…。_where_",
             GREETING : "",
             LEAVING : "",
             },
    2214 : { QUEST : "海図？ああ、持ってるよ。\aメルヴィルなんかのために働いてやるってんなら、その報酬に海図を渡してあげる。\a僕はいま、星空をたよりに航海できるよう天体観測儀を作っているところなんだ。\aコグ・ギアが３つ必要だから、それを取ってきてくれ。",
             INCOMPLETE_PROGRESS: "３つのコグ・ギア、集められそうかい？",
             GREETING : "いらっしゃい！",
             LEAVING : "幸運を祈ってるよ！",
             },
    2215 : { QUEST : "うん！これならきっといいものが出来るよ。\aはい、これが海図だよ。メルヴィルに渡してやってくれ。_where_",
             GREETING : "",
             LEAVING : "",
             COMPLETE : "よーし、これで準備は整ったぞ。旅立ちの時は来た！\aキミが経験者だったらこの旅に連れていくところだがな。かわりにこれを受け取ってくれ。",
             },
    901 : { QUEST : "エイハブが何か手助けを必要としているらしいぞ、キミにガッツがあるなら行ってみるがいい。_where_",
            },
    2902 : { QUEST : "おまえが例の新入りか？\aよろしい、ちょうど人手が必要だったところだ。\a私は今、コグ達をかくらんするのに使う巨大なカニのはりぼてを造っているんだ。\aクロヴィスが必要なんだが、ひとつクラッガーから借りてきてくれんか。_where_",
             },
    2903 : { QUEST : "いらっしゃい！\aああ、ボクもエイハブのカニのはりぼての事は聞いてるよ。\aでも、うちにあクロヴィスで一番いいものはちょっと汚れちゃってるんだ。\aまずこれをクリーニングに出してくれないかな、頼むよ。_where_",
             LEAVING : "ありがとうね！"
             },
    2904 : { QUEST : "キミがクラッガーのおつかいのコだね。\aそれならすぐにきれいにクリーニングできるよ。\aちょっと待ってて…\aさ、できたよ。ぴっかぴかだ！\aエイハブによろしくね。_where_",
             },
    2905 : { QUEST : "これこれ、私が欲しかったのはまさにこれだよ。\aせっかく手伝ってくれてるんだ、次は大きな時計のバネを取ってきてもらおうか。\aフックの元へ行って、バネを持っているかどうか聞いてきてくれ。_where_",
             },
    2906 : { QUEST : "大きなバネねぇ。\aすまないが、うちにあるのは小さいものばかりだよ。\aでも、もしかしたら水鉄砲の引き金のバネをいくつか使って作れるかもしれないな。\a水鉄砲を３つ持ってきてくれ、なんとかやってみよう。",
             },
    2907 : { QUEST : "どれどれ…\aうーん、最高だね！これはいい！\aもう自分でもびっくりのいい出来だよ。\aはい、エイハブさまご注文の大きなバネだ。_where_",
             LEAVING : "行ってらっしゃい！",
             },
    2911 : { QUEST : "手伝いたいのはやまやまだけど…\aこの辺はもう安全じゃなくなってしまったんだよ、_avName_。\aとりあえずマネーボットを何体か退治してくれないかな、話はそのあとだ。",
             INCOMPLETE_PROGRESS : "まだまだ通りは危険だよ…",
             },
    2916 : { QUEST : "ああ、エイハブにあげられるような錘があるよ。\aでも、まずはセルボットを何体かやっつけた方が帰り道も安全なんじゃないかな。",
             INCOMPLETE_PROGRESS : "まだまだセルボットがいるよ、倒したほうがいいよ。",
             },
    2921 : { QUEST : "まぁ、ひとつぐらいなら錘をあげてもいいかな。\aまわりでうろうろしているボスボット共をなんとかしてくれたら助かるけど。\a６体やっつけたらまた来てくれないかな。",
             INCOMPLETE_PROGRESS : "うーん、まだ身の危険を感じるよ…",
             },
    2925 : { QUEST : "終わったかい？\aそうだね、もう危険は感じないかもしれない。\aこの錘をエイハブに持っていってくれ。_where_"
             },
    2926 : {QUEST : "よーし、航海に必要なものはすべてそろったぞ。\aうまくいくかな？……\aうむむ、問題がひとつだけあるな…\a船にエネルギーがないらしい。コグビルのせいでソーラーパネルに日光が来ていないんだな。\aちょっと奪回してきてくれんか？",
            INCOMPLETE_PROGRESS : "まだエネルギーが来ないな。あっちの建物はどうだろう？",
            COMPLETE : "おお！たいしたコグ退治の腕前だ。これはほんのお礼だよ。",
            },
    3200 : { QUEST : "たった今、_toNpcName_から連絡があったんだ。\aなんだかえらく大変そうなんだ、手伝ってあげてくれないか？_where_" },
    3201 : { QUEST : "来てくれてありがとう！\aこのシルクネクタイを_toNpcName_に届けてくれないかな。\aお願いしてもいいかい？_where_" },
    3203 : { QUEST : "おや、これは私が以前オーダーしたネクタイだね。ありがとう。\a私が仕立てたばっかりのあのしましまスーツにぴったりなん…\aあれ、スーツがないぞ。\aまさか！コグに盗まれてしまったのか！？\aやられた！\aスーツが見つかるまでコグを退治してくれ、頼んだぞ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "スーツは見つかったか？コグ達が盗んだに違いないんだ！",
             COMPLETE : "ばんざい！大事な新品のスーツが戻ってきた！\aやっぱりあいつらの仕業だったんだな。これは取り返してきてくれたお礼だよ。",
             },

    3204 : { QUEST : "_toNpcName_がついさっき電話してきて、盗難に遭ったそうだ。\aちょっと様子を見てきてやってくれ。" },
    3205 : { QUEST : "こんにちは、_avName_。助けにきてくれたのですね。\a今ちょうどガッツキーを店から追い出したところなんです…ふぅ。怖かったですよ。\aでも、混乱の中ハサミを無くしてしまいました。さっきのガッツキーが持って行ったに違いありません！\aお願いです、どうかハサミを取り返してください！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "ハサミはまだ見つかっていないのですか？",
             COMPLETE : "ああ、ハサミだ！見つかったんだね、ありがとう！どうかこのお礼を受け取ってください！",
             },

    3206 : { QUEST : "_toNpcName_がコグに悩まされてるみたいです。\a良かったら手助けしてあげてください。_where_" },
    3207 : { QUEST : "やあ_avName_！来てくれてありがとな！\aニマイジタンの一団がやってきて、オレの担当カウンターからはがきを一山持ってっちまったんだよ。\aあいつらを全部やっつけて、はがきを取り返してきてくれ！",
             INCOMPLETE_PROGRESS : "まだまだ取り残しがあるよ！",
             COMPLETE : "サンキュー！これで時間通りにはがきを配達できるよ。これはお礼だ、受け取ってくれ。",
             },

    3208 : { QUEST : "最近、デイジー・ガーデンでブアイソンについての苦情が出ているんだ。\a住民の安全のためにも、１０体のブアイソンを倒してきてくれ" },
    3209 : { QUEST : "ブアイソン退治、感謝しているよ。\aだが、今度はツーハーン達が暴れ始めてしまった。\aデイジー・ガーデンで１０体のツーハーンを倒してきてくれれば、報酬を出す。頼んだよ。" },

    3247 : { QUEST : "最近、デイジー・ガーデンでガッツキーについての苦情が出ているんだ。\a住民の安全のためにも、２０体のガッツキーを倒してきてくれ" },


    3210 : { QUEST : "ありゃりゃ、メイプルストリートにあるフラワー・スプラッシュが品切れになってしまったみたいだぞ。\a自分で集めたフラワー・スプラッシュを持っていってやってくれないか。\a自分のもくろくにフラワー・スプラッシュが１０本入っていることを確認してから行くんだぞ。",
             LEAVING: "",
             INCOMPLETE_PROGRESS : "それじゃ足りないわ、必要なのは１０本のフラワー・スプラッシュよ。" },
    3211 : { QUEST : "ああよかった、１０本あれば今日はなんとかなるわ！ありがとう！\aでも、コグが外をうろついているのはやっぱり怖いわ。\aコグを２０体ばかりやっつけてくれないかしら？",
             INCOMPLETE_PROGRESS : "まだまだコグ達がいるわよ、やっつけて！お願い！",
             COMPLETE : "よかったわ、これで少し安心よ。あなたへのお礼は…",
             },

    3212 : { QUEST : "_toNpcName_が何か大事なものを無くしちゃったらしいの。\a探すのを手伝ってあげてくれない？_where_" },
    3213 : { QUEST : "いらっしゃい、_avName_。\aペンが１本見当たらないんだが、もしかしたらコグが持って行ってしまったのではと思ってるんだ。\a探すのを手伝ってくれるかい？\aコグ達を倒してペンを見つけ出しておくれ。",
             INCOMPLETE_PROGRESS : "ペンは見つかったかね？" },
    3214 : { QUEST : "そうそう、それが私のペンだよ！感謝する！\aただね、キミがいない間にインクつぼも無いことに気付いて…\aコグ達をやっつけていけばきっと見つかるだろう。",
             INCOMPLETE_PROGRESS : "インクつぼ、見つからないね…" },
    3215 : { QUEST : "おお、これでペンとインクつぼが揃った！\aだがねキミ、実は…\a今度はメモ帳がなくなってしまったんだ。まったく、油断も隙もないね。\aメモ帳をコグ達から取り返してきてくれたら、お礼を差し上げるよ。",
             INCOMPLETE_PROGRESS : "メモ帳は見つかった？" },
    3216 : { QUEST : "ああ、メモ帳が見つかったんだね、やった！さて、キミへのお礼は…\aあれ？見当たらないぞ？\aオフィスのロックボックスの中に入れておいたのに、ロックボックスそのものがない！\aまったく信じられないな…コグのやつら、キミへのお礼まで盗んでいってしまったようだ。\aすまないが、ロックボックスを取り返してきてくれ。\aお礼はその後差し上げるよ。",
             INCOMPLETE_PROGRESS : "ロックボックスを探し出してくれよ、キミへのお礼の品も入ってるんだから！",
             COMPLETE : "やっと見つかったね、お疲れさま！このロックボックスにはキミにあげる新しいギャグバッグが入っているんだよ。",
             },

    3217 : { QUEST : "我々はセルボットの構造について研究している者である。\aだがまだまだ詳細を知らない部分もある。\aそこでキミにはタッシャーナのスプロケットを採取してきてもらいたい！\aコグが爆発している時に入手できるようだ、任せたぞ。" },
    3218 : { QUEST : "よくやった。今度はオオゲーサのスプロケットを比較材料として取ってきてくれ。\a先ほどより入手が難しいだろうから、根性で入手してきてくれ" },
    3219 : { QUEST : "すばらしい！よし、あともうひとつ集めるだけだ。\a今度はクロマクールのスプロケットである。\aこやつらを見つけるにはセルボットビルの中を捜すのが良かろう。\aひとつ持って帰ってきてくれればキミにお礼を差し上げよう。" },

    3244 : { QUEST : "我々はロウボットの構造について研究している者である。\aだがまだまだ詳細を知らない部分もある。\aそこでキミにはツケコミンのスプロケットを採取してきてもらいたい！\aコグが爆発している時に入手できるようだ、任せたぞ。" },
    3245 : { QUEST : "よくやった。今度はオオゲーサのスプロケットを比較材料として取ってきてくれ。\a先ほどより入手が難しいだろうから、根性で入手してきてくれ" },
    3246 : { QUEST : "すばらしい！よし、あともうひとつ集めるだけだ。\a今度はドクター・トラブルのスプロケットである。\aこやつらを見つけるにはセルボットビルの中を捜すのが良かろう。\aひとつ持って帰ってきてくれればキミにお礼を差し上げよう。" },

    3220 : { QUEST : "ついさっき耳に入ったんだが、_toNpcName_がキミを探しているらしい。\a何事か聞いてみるとよかろう。_where_" },
    3221 : { QUEST : "あら、_avName_!やっといたわ！\aあたし、あなたがみずでっぽう攻撃 のプロだって聞いたわ。\aデイジー・ガーデンのトゥーン達に自己防衛のいい例を見せてあげたいの。\aみずでっぽう攻撃でコグをたくさんやっつけてくれないかしら。\aそうすれば住民達もきっとみずでっぽうで反撃し始めるわ！\a２０体のコグをやっつけてきたらお礼をあげるわ、がんばってね。" },

    3222 : { QUEST : "キミのトゥーン魂を見せてほしい。\aコグに占領された建物を何棟か奪回してくれたら、クエストを３つ持てるようにしてやろう。\aまず、どれか２つのコグビルを奪い返してくれ。\a友達に協力してもらうのもよかろう。"},
    3223 : { QUEST : "よくやった。\aさあ、あと２棟だ。\a２階以上あるものを奪回してきなさい" },
    3224 : { QUEST : "すばらしい！\aさあ、あと２棟だ。\a３階以上あるものを奪回してきなさい。\a終わったら戻っておいで、報酬が待っているよ。",
             COMPLETE : "最後までやりとげたな、_avName_！\aキミのトゥーン魂、しかと見せてもらったぞ。",
             GREETING : "",
             },

    3225 : { QUEST : "_toNpcName_がヘルプを探しているらしいよ。\aキミならきっと彼女を助けられるだろう。_where_" },
    3235 : { QUEST : "そう、これが私のオーダーしたサラダよ。\a持ってきてくれてありがとう。\aきっとコグ達が_toNpcName_の配達人を怯えさせてしまったのね。\aねえ、私達のために外を徘徊してるコグを倒していただけない？\aデイジー・ガーデンにいるコグを１０体倒したら、_toNpcName_に報告してくださいな。",
             INCOMPLETE_PROGRESS : "ボクのためにコグを倒しているんだって？\aありがたいよ、どんどん退治してくれ！",
             COMPLETE : "コグ達を倒してくれてありがとう！\aこれで以前のように配達することが出来るよ。\aこれはお礼の気持ちさ。",
             INCOMPLETE_WRONG_NPC : "コグ退治のことは_toNpcName_に伝えてあげてね。_where_" },

    3236 : { QUEST : "ここらでロウボットを倒そうにも、数が多すぎて！\aキミも手伝ってくれない？\aロウボットビルを３棟奪回してくれればいい" },
    3237 : { QUEST : "よくやった！\aだが今度はセルボットが増えてきてしまったようだ。\aセルボットビルを３棟奪回して戻ってきてくれれば、お礼ははずむよ。" },

    3238 : { QUEST : "なんてこった！デイジー・ガーデンのカギが\"オマカセンヌ\"にぬすまれたらしい。\a取り返してきてくれるかい？\aそうそう、オマカセンヌはセルボットビルの中にしかいないから、覚えておいてね。" },
    3239 : { QUEST : "あれれ、間違ったカギを持ってきてしまったみたいだよ。\aひつようなのはデイジー・ガーデンのカギ。\aがんばって探してね！持っているのは\"オマカセンヌ\"だよ！" },

    3242 : { QUEST : "なんてこった！デイジー・ガーデンのカギがホウノトリにぬすまれたらしい。\a取り返してきてくれるかい？\aそうそう、ホウノトリはロウボットビルの中にしかいないから、覚えておいてね。" },
    3243 : { QUEST : "あれれ、間違ったカギを持ってきてしまったみたいだよ。\aひつようなのはデイジー・ガーデンのカギ。\aがんばって探してね！持っているのはホウノトリだよ！" },

    3240 : { QUEST : "_toNpcName_が言ってたんだけど、ホウノトリが彼の店の鳥のエサを盗んでいってしまったんだって。\aサッサの商品を持ってるホウノトリが見つかるまで、ホウノトリ達をやっつけてくれないかな。\aホウノトリがいるのはロウボットビルの中だけだよ。_where_",
             COMPLETE : "ああ、僕の商品を見つけてくれたんだね、ありがとう！\aお礼にこれをあげるね。",
             INCOMPLETE_WRONG_NPC : "鳥のエサを取り返すことができたね、ごくろうさま！\aさあ、今度はそれを_toNpcName_に持っていってあげてね。_where_",
             },

    3241 : { QUEST : "この辺のコグビルは背が高くなりすぎて、なんだかこわいよ。\aそこでキミには背の高いビルを何棟かくずすことをお願いしたいんだ。\a３階建てのビルを５棟とりもどしたらごほうびをあげるよ。",
             },

    3250 : { QUEST : "オークストリートにいるたんていのメイが「セルボット本部」の報告書の話を聞いたみたいなんだ。\aちょっと彼女のところに行って、彼女を手伝ってもらえないかな？",
             },
    3251 : { QUEST : "最近、この近所の様子がなんだか変なのよ！\aセルボット達がやたらにうろついてると思わない？\aこのストリートの先にコグたちが本部を作ったって話も聞いたし…\a悪いんだけど、ストリートの先に行って、何かヒントをつかんでくれないかしら。\aコグ本部にいるセルボットを見つけて、５体やっつけたら報告してちょうだい。",
             },
    3252 : { QUEST : "それじゃあ、教えてもらおうかしら！\aえっ、何ですって！！\aセルボット本部？？\nそんなぁ！\n何とかしなくちゃ！\aミスター・ジャッジに急いで知らせないと！彼ならどうすればよいかを教えてくれるはず！\aすぐに行って、伝えてあげて！彼はこの先をちょっと行ったところにいるわよ！",
            },
    3253 : { QUEST : "ん？何かお困りかな？\nごらんの通り、私は忙しい…\aは？\nコグ本部？\aお？\nそれはありえん。\aきっとキミが間違っているのだ。\nまったくもってばかげた話だ。\aほ？\n私と議論してもムダだ。\aそれならば、証拠を見せてもらわなくては。\aもしセルボット達が本当にコグ本部を作っているのならば、設計図をもっているはずだ！\aなにしろコグたちはペーパーワークが好きだからな！\aその本部とやらにいるコグ達をやっつけて、設計図を持ってきたら、議論してやってもいいぞ。",
            },
    3254 : { QUEST : "また、キミか！\n設計図？ 持ってきたのか？\aどれどれ…\nん？ 工場？\aセルボット達を作るところに違いない… む？ これは何だ？\aほう、思ったとおりだ。\a彼らはセルボットのコグ本部を建設中なのだ。\aこれは良くないな！ 電話をしないと！ あー忙しい、忙しい。それじゃあな！\aお？ そうそう、たんていのメイのところに設計図を持っていってくれ。\a彼女ならなんらかのヒントがわかるかもしれん。",
             COMPLETE : "ミスター・ジャッジは何だって？\a思ったとおりだったわけね。 どうしましょう？ 設計図を見せて。\aふーん…\nコグを大量生産する工場を作っているって訳ね。\aとても危険そうね。\nゲラゲラメーターが増えるまでは立ち寄らないほうがよさそうね。\aゲラゲラポイントがたくさん増えるまでは、いろいろとコグ本部についていろいろ調べたほうが良さそうね。\a本当にありがとう。これはごほうびよ！",
            },


    3255 : { QUEST : "_toNpcName_がセルボット本部の調査をしているよ！\a行って手伝ってあげたら？_where_" },
    3256 : { QUEST : "_toNpcName_がセルボット本部の調査をしているよ！\a行って手伝ってあげたら？_where_" },
    3257 : { QUEST : "_toNpcName_がセルボット本部の調査をしているよ！\a行って手伝ってあげたら？_where_" },
    3258 : { QUEST : "コグたちが本部の中で何をたくらんでるかわからなくて、みんな混乱しているんだ。\a彼らのところに行って直接、何か情報を取ってきてほしいんだ。\aもし、コグ本部の中でセルボット達からメモを４つ取ってきてくれれば、少しは混乱がなくなるんじゃないかな？\a最初のメモを手に入れたら、ここに持ってきてくれないかな？そうしたら何かわかるかもしれないし。",
             },
    3259 : { QUEST : "すばらしい！\nさてさて、メモには何て書いてあるかな…\a「セルボット達へ：」a\「私はセルボットのタワーの一番上のオフィスにいて、キミたちコグのレベルを『格上げ』する業務をしている。」\a「キミたちが『メリット』をたくさん集めたら、ロビーにあるエレベーターに乗って私に会いに着なさい。」\a「休み時間は終わりだ。さっさと仕事に戻りなさい！\a「セルボット\nコグゼキュティブ\nより」\aははーん。フリッピーにこれを見せないと！\a今すぐ、僕から送っておくから、キミは２番目のメモを取りにいってね。",
             },
    3260 : { QUEST : "ああ、よかった。\n戻ってきてくれて！\aえーと、次のメモには…\a\「セルボット達へ：」\a「セルボットのタワーはこの度、トゥーンを寄せ付けないために新しいセキュリティーシステムを導入したわ。」\a「セルボットタワーで捕まったトゥーン達は尋問のためにとらわれるようになったのよ。」\a「続きはロビーで会って、話し合いましょう！」\a「オマカセンヌより」\a非常に興味深い…\nさっそく、フリッピーに送らないと…\aキミは３番目のメモをよろしく頼むよ！",
             },
    3261 : { QUEST : "_avName_！\nメモは、っと。\a\「セルボット達へ：」\a「どうやらトゥーン達がセルボットタワーに入る方法を見つけたようだ。」\a「今晩の打ち合わせのときに詳しく話すことにするよ。」\a「ツーハーンより」\aほほう、色々わかってきたぞ！\aもう１つメモがあれば、十分な情報が集められるからよろしく頼むよ！",
             COMPLETE : "キミならやれると信じてたよ！\nふむふむ、\a「セルボット達へ：」\a「昨日、ビッグスマイルとランチオンミーティングをしたよ。」\a「彼は、最近とても忙しいコグゼキュティブについて話をしてくれたんだけど、」\a「どうやら一生懸命働いて『格上げ』されたコグとしか会ってくれないらしいよ。」\a「あ、そうそう。\nオオゲーサと日曜日にゴルフに行くんだ。」\a「タッシャーナより」\aうーん、_avName_。これは非常に助かる情報だったね。\aこれはキミへのごほうびだよ。",
             },

    3262 : { QUEST : "_toNpcName_ がセルボット本部の工場について何か新しい情報をつかんだみたいだよ。\a彼に会って、確認するといいよ！_where_" },
    3263 : { GREETING : "やあ！",
             QUEST : "わたしがコーチのヨーガだ。\aいいか、よーく聞いてくれ！\nセルボット達がとてつもなく大きな工場を完成させたみたいだ。１日２４時間、セルボットを作り続けるつもりらしい。\aキミのトゥーン仲間たちと一緒に工場をたたきつぶしにいってくれ！\aセルボット本部の中で、工場へのトンネルを探し出し、工場のエレベーターに乗ってくれ！\aギャグやゲラゲラメーターを一杯にしてから、強いトゥーンたちと一緒に立ち向かおう！\a中にいる工場長を倒せば、セルボットの生産がきっと遅れるはずだ！\aどうだ？キミにできるかな？",
             LEAVING : "それじゃあな！",
             COMPLETE : "おー！やるじゃないか！\aちゃんとコグのパーツの一部を見つけたようだな。\aコグを作る途中で出来たものに違いない！\a持ち運びも出来る大きさだから、時間があるときに集めてみると良いかもな。\aひょっとしたら、コグのスーツのパーツ全てが集まるかもしれないしな。何かに使えるかもしれんし…",
             },
    
    4001 : {GREETING : "",
            QUEST : "次に覚えたいギャグトラックを選ぼう。\aじっくり考えてから決めてね。\a決める準備ができたらここに戻っておいで。",
            INCOMPLETE_PROGRESS : "選択する前に、もう一度よく考えてね。",
            INCOMPLETE_WRONG_NPC : "選択する前に、もう一度よく考えてね。",
            COMPLETE : "いい選択だ。",
            LEAVING : QuestsDefaultLeaving,
            },

    4002 : {GREETING : "",
            QUEST : "次に覚えたいギャグトラックを選ぼう。\aじっくり考えてから決めてね。\a決める準備ができたらここに戻っておいで。",
            INCOMPLETE_PROGRESS : "選択する前に、もう一度よく考えてね。",
            INCOMPLETE_WRONG_NPC : "選択する前に、もう一度よく考えてね。",
            COMPLETE : "いい選択だ。",
            LEAVING : QuestsDefaultLeaving,
            },
    4200 : { QUEST : "トムの研究の手助けをしてあげるのもいいんじゃないかな？_where_",
             },
    4201 : { GREETING: "やあっ！",
             QUEST : "最近、楽器がよく盗まれるようになってしまっていてね。\a店オーナーの仲間とちょっとした調査をしているんだ。\aどういう手口で行われているか解明できるかもしれない。\aティナの店に寄って、コンチェルティナのもくろくのことを聞いてくれないかな。_where_",
             },
    4202 : { QUEST : "うん、トムとは今朝会ったわ。\aもくろくならここにあるわよ。\aすぐに彼に持っていってあげてね。_where_"
             },
    4203 : { QUEST : "おお、さすがだね！これでひとつそろった。\a次はユキのところへ行って、彼女のもくろくを持ってきてくれ。_where_",
             },
    4204 : { QUEST : "ああ、もくろくね！\aすっかり忘れちゃってたわ。\aキミが１０体のコグを倒している間に作り終えることができると思うんだけど…\aそれをやったらまた来てみて",
             INCOMPLETE_PROGRESS : "３１、３２…ああっ！\aわからなくなっちゃったじゃない！",
             GREETING : "",
             },
    4205 : { QUEST : "ああ、いたいた。\a時間かかっちゃってごめんね。\aこれをトムに持っていってあげてね。私からもよろしくって。_where_",
             },
    4206 : { QUEST : "ふむ、これはおもしろい。\aこれでなんとかなるかも…\aよし、あとはバイオレットのもくろくだけだ。_where_",
             },
    4207 : { QUEST : "え、もくろく？\aもくろくなんて、もくろく帳がなくちゃ作れないわよ。\aクレフのところに行って、もくろく帳を持っているか聞いてみて。_where_",
             INCOMPLETE_PROGRESS : "もくろく帳はあったの？",
             },
    4208 : { QUEST : "もくろく帳？おれ様の店ならあるに決まってるよ～。\aでもタダじゃやれねえな～。\aどうだ、クリームパイまるごと１個と交換ってのは。",
             GREETING : "いよう！",
             LEAVING : "去る者は追わずってやつさ。",
             INCOMPLETE_PROGRESS : "ひときれじゃあダメだ。\aおれ様はハラがへってんのよ。まるごとじゃなきゃあダメだ。",
             },
    4209 : { GREETING : "",
             QUEST : "うぅ～ん！\aやっぱりうまいね～！\aほれ、約束のもくろく帳だ、バイオレットに持ってってやんな。_where_",
             },
    4210 : { GREETING : "",
             QUEST : "ありがとう、これで何とかなりそうよ。\aさて、と…「バイオリン: ２」\aはい、できたわよ！",
             COMPLETE : "おお、ありがとう、_avName_。\aこれで盗人たちをなんとかふんじばれるかも知れない。\aどうだ、もっと協力しないか？",
             },

    4211 : { QUEST : "そういえばドクター・アイタタがひっきりなしに電話をかけてきてるんだ。いったいどうしたのか、聞いてきてくれないか？_where_",
             },
    4212 : { QUEST : "おやおや、トゥーンＨＱもやっと誰かよこしてくれたんだね。\aうちにはもう何日も患者が来ていないんだ。\aスウジスキーのやつらがうようよしているせいさ。\aこの辺の住民にもカネ至上主義の影響を与えかねんしな。\aスウジスキーを１０体やっつけくれないか、患者が戻ってくるか試してみたいんだよ。",
             INCOMPLETE_PROGRESS : "まだまだ患者が来ないなぁ。がんばってくれ！",
             },
    4213 : { QUEST : "もしかしたら原因はスウジスキーじゃないのかもしれんな。\aマネーボット全体がいかんのだろう。\aマネーボットを２０体おっぱらってくれたら誰かが診療に来るかも…",
             INCOMPLETE_PROGRESS : "２０体はたしかに多いが、きっとなにかの結果を出してくれるだろう。",
             },
    4214 : { GREETING : "",
             LEAVING : "",
             QUEST : "まったくもって理解できん！やっぱり患者が１人も来ないんだよ。\aこうなったら大元をたたくしかないのか…\aためしにマネーボットビルを倒してみてくれ。\aそれでダメならあきらめるさ。",
             INCOMPLETE_PROGRESS : "マネーボットビルひと棟でいいんだ！たのむ！",
             COMPLETE : "やっぱりだめだ、１人も来ない…\aだがな、ひとつ気がついたことがある。\a私の診療所には、コグが来る前にも患者が来たことがなかったのさ。\aだがあいつらをおっぱらってくれて感謝しているよ。\aお礼にこれをあげよう、きっと役にたつよ。"
             },

    4215 : { QUEST : "どうやらアンナが困っているらしい。\a行って助けてあげてくれないか。_where_",
             },
    4216 : { QUEST : "さっそく来てくれてうれしいわ！\aどうやらコグが私のお客のクルーズチケットを盗んでいってしまったみたいなの。\aオオゲーサがチケットをたんまり持ってここから出て行くのをユキが見たらしいわ。\aモックンのアラスカ旅行のチケットを取り戻してくれないかしら",
             INCOMPLETE_PROGRESS : "そろそろオオゲーサが出てくるんじゃないかしら…",
             },
    4217 : { QUEST : "まあ、みつけたのね！\aじゃあ、ついでにこれをモックンのところに届けてくれないかしら？_where_",
             },
    4218 : { QUEST : "うわぁ、ぼくのアラスカ旅行のチケットじゃないか！\aやった～！\aもうコグのやつらにはうんざりだよ。\aああそうだ、またアンナがキミの手をかりたいみたいだけど。_where_",
             },
    4219 : { QUEST : "オオゲーサのやつ！\a今度はタバサのジャズフェスティバルチケットを取り返してほしいの。\aさっきと同じようにさくっと、ね！",
               INCOMPLETE_PROGRESS : "オオゲーサならそこら辺にいるはずよ。",
             },
    4220 : { QUEST : "やったわね！\aこれタバサのところにもっていってくれない？_where_",
             },
    4221 : { GREETING : "",
             LEAVING : "気をつけてね～",
             QUEST : "イエーイ！やった！\aさーてジャズフェスタで踊りまくってやるわよ。\aそうそう、キミもどこかに行っちゃう前にまたアンナのとこに行ったほうがいいと思うよ。_where_",
             },
    4222 : { QUEST : "お願い、これで最後だから！\aこんどはバリーの歌唱コンクールのチケットを取り返してきてくれないかしら",
             INCOMPLETE_PROGRESS : "お願いよ、_avName_。\aバリーも困ってるのよ～",
             },
    4223 : { QUEST : "よかった、これでバリーも安心して行けるわ！_where_",
             },
    4224 : { GREETING : "",
             LEAVING : "",
             QUEST : "いやぁ、助かったよ！\aありがとう！\a今年こそ私達が１位をとれる気がするよ。\aアンナからの伝言だ、お礼をしたいので来てくれ、と。_where_\aそれではね、ありがと～う！",
             COMPLETE : "助けてくれて本当にありがとう、_avName_。\aあなたはトゥーンタウンの宝だわ。\aそうそう、お宝といえば…",
             },

    902 : { QUEST : "レオに会いに行ってあげて。\aメッセージの配達をしてくれる人を探しているみたいなの。_where_",
            },
    4903 : { QUEST : "いよっす！\aおれっちのカスタネットがなんだかくもっちまって、今夜のショーがうまく行くか心配なんだ。\aカルロスのところに持っていって、みがいてくれるかどうか聞いてみてくんないかな。_where_",
             },
    4904 : { QUEST : "エエ、みがけると思いマスよ。\aでもソレにはイカからとった青いインクが必要なんデス",
             GREETING : "コニチハー！",
             LEAVING : "サヨナーラ！",
             INCOMPLETE_PROGRESS : "イカは、つり場があるトコロならドコでも見つけられマスよ。",
             },
    4905 : { QUEST : "エエ、これデス！\aサテ、あとはみがくジカンが必要なダケ…\aアナタ、どうせ待つならコグビルをヒトツたおしてきてみてはどーデスカ？",
             GREETING : "コニチハー！",
             LEAVING : "サヨナーラ！",
             INCOMPLETE_PROGRESS : "ウーン、まだマダ…",
             },
    4906 : { QUEST : "ヨーシ！\aレオのカスタネット、みがきオワリましたヨ。_where_",
             },
    4907 : { GREETING : "",
             QUEST : "やったー！\aいいカンジじゃーん！\aあとは…'ビート・クリスマス' の歌詞カードをヘイディからもらってこなきゃいけないんだ。_where_",
             },
    4908 : { QUEST: "こんにちは！\aうーん、その歌詞カードはウチにはないなぁ。\aちょっと時間をくれたら暗記してある歌詞を書き出せるんだけど。\aぼくがそれをやっている間、コグビルを２棟取り返すっていうのはどうだい？",
             },
    4909 : { QUEST : "うぅ～ん…\a思ったよりハッキリ覚えてないみたいだ。\a３階建てのコグビルを倒している間になんとかなりそうだと思うんだけど…",
             },
    4910 : { QUEST : "できたよ！\a待たせてしまってごめんね。\aこれをレオに持っていってあげて。_where_",
             GREETING : "",
             COMPLETE : "やったー！いいカンジじゃーん！\aこれでおれっちのショーもいいカンジじゃーん！\aそうそう、アンタにはお礼をしなきゃな"
             },
    5247 : { QUEST : "ここらも最近荒れてきてしまって…\aキミもいくつか新しい「トリック」を覚えたほうがいいよ。\a_toNpcName_が私にいろいろ教えてくれたんだけど、キミも会ってみるといいよ。_where_" },
    5248 : { GREETING : "ああ、こんにちは…",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キミへの宿題は、ちょっと難しかったかな？",
             QUEST : "ああ、いらっしゃい、みならいくん。\aパイゲームのことなら私にまかせたまえ。\aだが訓練を始める前に、ちょっとキミの力をみせてくれ。\a外にいる一番おおきいコグを１０体やっつけてみなさい" },
    5249 : { GREETING: "ふむ…",
             QUEST : "すばらしい。\a今度は釣り人としてのスキルを見せてくれ。\aきのう、池に３つのもこもこサイコロを落としておいた。\aそれらを釣って私に持ってきなさい。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "釣竿の扱いはまだまだらしいな" },
    5250 : { GREETING : "",
             LEAVING : "",
             QUEST : "おお。このダイス、私の水牛車のミラーにつけたらかっこいいのであろうな。\aさあ、今度はキミの敵の見分けがつくかを見てみよう。\a一番背の高いロウボットビルを２棟取り返してみせなさい。",
             INCOMPLETE_PROGRESS : "建物は苦手か？", },
    5258 : { GREETING : "",
             LEAVING : "",
             QUEST : "おお。このダイス、私の水牛車のミラーにつけたらかっこいいのであろうな。\aさあ、今度はキミの敵の見分けがつくかを見てみよう。\a一番背の高いボスボットビルを２棟取り返してみせなさい。",
             INCOMPLETE_PROGRESS : "建物は苦手か？", },
    5259 : { GREETING : "",
             LEAVING : "",
             QUEST : "おお。このダイス、私の水牛車のミラーにつけたらかっこいいのであろうな。\aさあ、今度はキミの敵の見分けがつくかを見てみよう。\a一番背の高いマネーボットビルを２棟取り返してみせなさい。",
             INCOMPLETE_PROGRESS : "建物は苦手か？", },
    5260 : { GREETING : "",
             LEAVING : "",
             QUEST : "おお。このダイス、私の水牛車のミラーにつけたらかっこいいのであろうな。\aさあ、今度はキミの敵の見分けがつくかを見てみよう。\a一番背の高いセルボットビルを２棟取り返してみせなさい。",
             INCOMPLETE_PROGRESS : "建物は苦手か？", },
    5200 : { QUEST : "コグめ、また悪さをしておる。\a_toNpcName_がコグに何かを盗まれたらしい。行って手助けしてやってくれ。_where_" },
    5201 : { GREETING: "",
             QUEST : "やあ、_avName_。来てくれてありがとう。\aついさっきヘッドハンターの一団が押し入って来て、僕のサッカーボールを持っていってしまったんだ。\aカットバックをしろだとか何とか言いながら。\aボールを取り返してきてくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "サッカーボールは見つかったかい？",
             COMPLETE : "やったあ、見つかったんだね！ありがとう、これはお礼だよ。",
             },
    5261 : { GREETING: "",
             QUEST : "やあ、_avName_。来てくれてありがとう。\aついさっきアイソマンの一団が押し入って来て、僕のサッカーボールを持っていってしまったんだ。\aカットバックをしろだとか何とか言いながら。\aボールを取り返してきてくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "サッカーボールは見つかったかい？",
             COMPLETE : "やったあ、見つかったんだね！ありがとう、これはお礼だよ。",
             },
    5262 : { GREETING: "",
             QUEST : "やあ、_avName_。来てくれてありがとう。\aついさっきカネモッチンの一団が押し入って来て、僕のサッカーボールを持っていってしまったんだ。\aカットバックをしろだとか何とか言いながら。\aボールを取り返してきてくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "サッカーボールは見つかったかい？",
             COMPLETE : "やったあ、見つかったんだね！ありがとう、これはお礼だよ。",
             },
    5263 : { GREETING: "",
             QUEST : "やあ、_avName_。来てくれてありがとう。\aついさっきドクター・トラブルの一団が押し入って来て、僕のサッカーボールを持っていってしまったんだ。\aカットバックをしろだとか何とか言いながら。\aボールを取り返してきてくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "サッカーボールは見つかったかい？",
             COMPLETE : "やったあ、見つかったんだね！ありがとう、これはお礼だよ。",
             },
    5202 : { QUEST : "最近、ブルブルタウンが見たこともないような屈強なコグ達に襲われているんだ。\a危ないから、キミももっとギャグを持ち歩いていたほうがいいよ。\a_toNpcName_がもっとギャグを入れることができるふくろを持っているらしいから、相談してみたらどうかな。_where_" },
    5203 : { GREETING: "ああん？キミ、私のソリチームにいたっけ？",
             QUEST : "なんだって、ふくろが欲しい？\aうーん、この辺にあったような気がするんだが…トボガンに入ってるかもしれないなあ。\aだが、ずっと前のレース以降あのトボガンを見てないしなあ。\aもしかしたらコグにとられたのかもしれん。",
             LEAVING : "私のトボガンを見かけたかい？",
             INCOMPLETE_PROGRESS : "えーっと、キミは誰だったっけ？すまんね、事故にあって以来ちょっと記憶が怪しくてな～" },
    5204 : { GREETING : "",
             LEAVING : "",
             QUEST : "ああ、これが私のトボガンだよ。だがふくろが見当たらんなあ。\aバンピー・ノギンがチームメイトだったんだが、彼が持ってるのかもな。_where_" },
    5205 : { GREETING : "あああ、頭が～！",
             LEAVING : "",
             QUEST : "ああ？テッドだって？ふくろ？\aあー、もしかしたらそんなのが私のトボガンチームにいたかも知れんな。\aうう、なんとも頭が痛くてろくに考え事もできんわい。\a凍った池から氷を少し釣りあげてくれんか？",
             INCOMPLETE_PROGRESS : "あうう、頭が痛い～！氷をくれ～！", },
    5206 : { GREETING : "",
             LEAVING : "",
             QUEST : "ああ、ずいぶん楽になったわい。\aえーと、それでキミはテッドのふくろを探しているんだったっけな。\aあれはレースでの事故の時にシミアン・サムの頭にかぶさってたぞ。_where_" },
    5207 : { GREETING : "Eeeep!",
             LEAVING : "",
             QUEST : "ふくろ？バンピー？\aワタシはビルが怖いのヨ！ビルを崩したらふくろあげるヨ！",
             INCOMPLETE_PROGRESS : "もっともっと！ビル倒して、怖いのヨ！",
             COMPLETE : "オーウ！スバラシーイ！" },
    5208 : { GREETING : "",
             LEAVING : "キャー！！!",
             QUEST : "オーウ！スバラシーイ！\aふくろはスキー・クリニックにあるヨ" },
    5209 : { GREETING : "ちーす！",
             LEAVING : "じゃあな！",
             QUEST : "あのサム・シミアンもおもしろいキャラだよなあ。\aあんたもあいつぐらいワイルドだってんならふくろをあげてやってもいいぜ。\aコグを何体かやっつけてきな。じゃあな、行ってらっしゃい！",
             INCOMPLETE_PROGRESS : "そんなんで満足しちゃいけねえよ！もっと倒してこなきゃダメだ。",
             COMPLETE : "ふぅん、なかなか悪くねえな。かなりの数のコグをやっつけたじゃねえか。\aほい、やくそくのふくろだぜ" },

    5210 : { QUEST : "_toNpcName_がこの辺のだれかに恋してるらしいんだ。\a彼女の恋の手助けをしてやったら、お礼がもらえるかもな。_where_" },
    5211 : { GREETING: "しくしく…",
             QUEST : "昨日の夜、愛するワンちゃんにラブレターを書いていたの。\aでも持っていこうとした時にクチバシのあるコグが入ってきて持っていっちゃったのよ！\aお願い、取り返してきて！",
             LEAVING : "しくしく…",
             INCOMPLETE_PROGRESS : "手紙を取り返してきて、お願い" },
    5264 : { GREETING: "しくしく…",
             QUEST : "昨日の夜、愛するワンちゃんにラブレターを書いていたの。\aでも持っていこうとした時にヒレのあるコグが入ってきて持っていっちゃったのよ！\aお願い、取り返してきて！",
             LEAVING : "しくしく…",
             INCOMPLETE_PROGRESS : "手紙を取り返してきて、お願い" },
    5265 : { GREETING: "しくしく…",
             QUEST : "昨日の夜、愛するワンちゃんにラブレターを書いていたの。\aでも持っていこうとした時にオマカセンヌが入ってきて持っていっちゃったのよ！\aお願い、取り返してきて！",
             LEAVING : "しくしく…",
             INCOMPLETE_PROGRESS : "手紙を取り返してきて、お願い" },
    5266 : { GREETING: "Boo hoo.",
             QUEST : "昨日の夜、愛するワンちゃんにラブレターを書いていたの。\aでも持っていこうとした時にデッパラーダが入ってきて持っていっちゃったのよ！\aお願い、取り返してきて！",
             LEAVING : "Boo hoo.",
             INCOMPLETE_PROGRESS : "手紙を取り返してきて、お願い" },
    5212 : { QUEST : "手紙をみつけてくれたのね、ありがとう！\aそれでね、あのう、ここらで一番ハンサムなワンちゃんに届けてくれないかしら…お願い！",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "手紙を届けてくれなかったのね…",
             },
    5213 : { GREETING : "あら、こんにちは。",
             QUEST : "今手紙を持ってこられても困るんだよね。\aボクのワンちゃん達はみんなどこかに連れ去られてしまったから。\a全員連れて帰ってきてくれたら受け取ってあげてもいいけど",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "ああ、かわいそうなワンちゃんたち！" },
    5214 : { GREETING : "",
             LEAVING : "ごきげんよう！",
             QUEST : "ボクの粒ぞろいのワンちゃん達を連れ戻してくれてありがとう。\aそれではその手紙を見てみようか。なになに…\nおやおや、ボクに思いを寄せる人がまたひとり…か。\aキミにはボクのともだち、カールの所へ行ってもらいたい。\aキミもきっと彼を気に入るさ。_where_" },
    5215 : { GREETING : "エッヘッヘ…",
             LEAVING : "また来なさい、ね。",
             INCOMPLETE_PROGRESS : "デカいやつらがまだいるから、そいつらをおっぱらったらまた来なさい。",
             QUEST : "いったい誰がキミをここに送り込んだのだね？タカビシャな人間はどうも気にくわんのだよ。\aだがコグのほうがよっぽど気にくわん。\a特にデカいコグたちを追っ払ってきたら手伝ってやろう。" },
    5216 : { QUEST : "やくそく通りキミを手伝ってやろう。\aこのゆびわを彼女のもとに持っていってやれ。",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "まーだゆびわを持っていってないのかい？",
             COMPLETE : "きゃああ！すごいわすごいわ！ありがとう！\aそうだわ、お礼にこれをあなたにあげたいの。もらってくれる？",
             },
    5217 : { QUEST : "_toNpcName_がなんだか困っているらしいわよ。_where_" },
    5218 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "この辺にもっとオマカセンヌがいると思うんだが…",
             QUEST : "たすけてくれぇー！もう耐えられない！\aオマカセンヌのせいでもう気が狂いそうだ！" },
    5219 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "まだまだだよ、さっきこのへんで１体見たんだ！",
             QUEST : "ありがとう。でも、こんどはデッパラーダ達が問題なのよ。\aお願い、なんとかして！" },
    5220 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "まだまだだよ、さっきこのへんで１体見たんだ！",
             QUEST : "わかったぞ、問題はシャークロンなんだ！絶対そうだ！\a手伝ってくれるんだろう？" },
    5221 : { GREETING : "",
             LEAVING : "",
             QUEST : "もしかするともしかするんだけど、問題はコグじゃないのかも…。\aファニーにすっきりするポーションを作ってきてもらえないかな、それで解決するかも。_where_" },
    5222 : { LEAVING : "",
             QUEST : "まーったくもう、ハリーもすぐああなるんだから。\aアレを直すやつを作ってあげるから、ちょっと待っててね。\aあら、イワシのヒゲがないわ…\a池に行って少し釣ってきてくれない？",
             INCOMPLETE_PROGRESS : "イワシのヒゲ、見つかった？", },
    5223 : { QUEST : "よーっし、これでＯＫよ。\aはい、これをハリーに持っていってあげて。彼の興奮状態をすぐに落ち着かせるから",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "ほらほら、早くそのポーションをハリーに届けてやんな。",
             },
    5224 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "頼むよ、早くホウノトリたちをおっぱらってくれー！",
             QUEST : "ああ、やっと戻ってきた！\aそのポーションをおくれ、早く！\aゴクゴクゴク…\aうええっ、まずい！\aでも…不思議だなぁ、なんだか落ち着いた気がするよ。これでやっとちゃんと考えられる気がする。\aそう、問題のコグはホウノトリだったんだ！",
             COMPLETE : "やったぁ！これでリラックスできるよ！\aえーと、たくさんがんばってくれたお礼に…これこれ、これをあげるよ。" },
    5225 : { QUEST : "あのだいこんパン事件以来、グランピー・フィルは_toNpcName_に対して怒ってるんだ。\aマモルだったら仲直りさせてあげられるかも…_where_" },
    5226 : { QUEST : "キミも、グランピー・フィルが私に対して怒ってるのを聞いたみたいだね。\a私はただ、あのだいこんパンの件で私は悪気はなかったんだけど…\aキミなら彼をはげましてあげられるかもしれない。\aフィルはマネーボットがきらいで、特にやつらのビルは耐えられないらしい。\aマネーボットビルをいくつか倒したら少しはよくなるかも",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "あと何棟かやってみてくれないか？", },
    5227 : { QUEST : "すごいぞ！さ、フィルに報告してやってくれ。_where_" },
    5228 : { QUEST : "ああ、そうなのかい。\aマモルのやつ、そんな事で許されると思ってんのかい。\aあいつのだいこんパンで歯が欠けたんだぞ！\aドクター・シンキクサーイだったら治せるかもしれんから、持っていってみてくれ。",
             GREETING : "むにゃむにゃむにゃ",
             LEAVING : "もごもごもご",
             INCOMPLETE_PROGRESS : "またあんたかい。わしの歯を治してくれるんじゃなかったのかい。",
             },
    5229 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯はまだ治している最中だ。もうちょっと時間がかかってしまうな。",
             QUEST : "そうだね、その歯はちょっとひどい状態だね。\aなんとかしてみせたいが、時間が必要だ。\a待ってる間にそこらのマネーボットをおいはらってくれないかい？\a患者がこわがって診療に来れなくなってしまったんだよ。" },
    5267 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯はまだ治している最中だ。もうちょっと時間がかかってしまうな。",
             QUEST : "そうだね、その歯はちょっとひどい状態だね。\aなんとかしてみせたいが、時間が必要だ。\a待ってる間にそこらのセルボットをおいはらってくれないかい？\a患者がこわがって診療に来れなくなってしまったんだよ。" },
    5268 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯はまだ治している最中だ。もうちょっと時間がかかってしまうな。",
             QUEST : "そうだね、その歯はちょっとひどい状態だね。\aなんとかしてみせたいが、時間が必要だ。\a待ってる間にそこらのロウボットをおいはらってくれないかい？\a患者がこわがって診療に来れなくなってしまったんだよ。" },
    5269 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯はまだ治している最中だ。もうちょっと時間がかかってしまうな。",
             QUEST : "そうだね、その歯はちょっとひどい状態だね。\aなんとかしてみせたいが、時間が必要だ。\a待ってる間にそこらのボスボットをおいはらってくれないかい？\a患者がこわがって診療に来れなくなってしまったんだよ。" },
    5230 : { GREETING: "",
             QUEST : "やあ、戻って来たね！\aあの古い歯を治すのはあきらめて、代わりに新しい金の歯を作ってみたよ。\aだが、ドロビッグが来て盗んで行ってしまったんだ。\a急いで追いかければ捕まえられるかもしれない。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯は見つかったかい？" },
    5270 : { GREETING: "",
             QUEST : "やあ、戻って来たね！\aあの古い歯を治すのはあきらめて、代わりに新しい金の歯を作ってみたよ。\aだが、ビッグチーズが来て盗んで行ってしまったんだ。\a急いで追いかければ捕まえられるかもしれない。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯は見つかったかい？" },
    5271 : { GREETING: "",
             QUEST : "やあ、戻って来たね！\aあの古い歯を治すのはあきらめて、代わりに新しい金の歯を作ってみたよ。\aだが、ビッグスマイルが来て盗んで行ってしまったんだ。\a急いで追いかければ捕まえられるかもしれない。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯は見つかったかい？?" },
    5272 : { GREETING: "",
             QUEST : "やあ、戻って来たね！\aあの古い歯を治すのはあきらめて、代わりに新しい金の歯を作ってみたよ。\aだが、ビッグホワイトが来て盗んで行ってしまったんだ。\a急いで追いかければ捕まえられるかもしれない。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "歯は見つかったかい？" },
    5231 : { QUEST : "そうそう、それだよ！\aさっそくフィルに持っていってあげてくれないか。",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "早くフィルに歯を持っていってあげてくれ。",
             },
    5232 : { QUEST : "おう、ありがとな。\aんむぐぐ…\aよし、これでどうだ！\aそうだな、うん。マモルを許してやってもいいかな。",
             LEAVING : "",
             GREETING : "", },
    5233 : { QUEST : "ああ、よかった。\aフィルがずっと怒りっぱなしでいるとは思わなかったけど…安心したよ。\a友情の証として、フィルにまつぼっくりパンを焼いたんだ。持っていってくれるかい？",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "急いでおくれよ、まつぼっくりパンはあったかいほうがおいしいんだ。",
             COMPLETE : "んん、これは何だね？わしにかい？\aむしゃむしゃ…\aあいたたた！は、歯が！まったく、あのマモルめが！\aいやしかし、キミのせいではないしな。ほれ、これはおだちんだよ。",
             },
    903 : { QUEST : "キミもそろそろブリザード・ウィザードの_toNpcName_の最後のテストに挑んでもいいかも知れないね。_where_", },
    5234 : { GREETING: "",
             QUEST : "おっ、戻ってきたね。\a始める前にまずは食事といこうか。\aスープに合うでこぼこのチーズを持ってきてくれ。\aでこぼこチーズはコグのビッグチーズからしか得られないよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "でこぼこチーズが必要だよ。" },
    5278 : { GREETING: "",
             QUEST : "おっ、戻ってきたね。\a始める前にまずは食事といこうか。\aスープに合うキャビアを持ってきてくれ。\aキャビアはコグのビッグスマイルからしか得られないよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キャビアが必要だよ。" },
    5235 : { GREETING: "",
             QUEST : "ふつうの人間はふつうの食器を使うべきだ。\aコグが私の「ふつうのスプーン」を取っていってしまったからスープも食べられない。\aスプーンを取り返してきてくれ、持っているのはたぶんドロビッグだ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "スプーンがなきゃ食べられないよ。" },
    5279 : { GREETING: "",
             QUEST : "ふつうの人間はふつうの食器を使うべきだ。\aコグが私の「ふつうのスプーン」を取っていってしまったからスープも食べられない。\aスプーンを取り返してきてくれ、持っているのはたぶんビッグホワイトだ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "スプーンがなきゃ食べられないよ。" },
    5236 : { GREETING: "",
             QUEST : "ありがとう、ありがとう。\aズズッ、ゴクン…\aああ、うまい。さて、こんどはしゃべるカエルを池から獲ってきてくれ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "しゃべるカエルは見つかったかい？" },

    5237 : {  GREETING : "",
              LEAVING : "",
              INCOMPLETE_PROGRESS : "まだデザートを持ってきていないね。",
              QUEST : "ほほう、それはたしかにしゃべるカエルだね。こっちにおくれ。\aなんだって、カエルくん？\aうんうん。\aふむふむ。\aカエルは言う、「デザートが必要だ」と。\aというわけで_toNpcName_のところからアイスクリームをいくつか持ってきてくれ。\aカエルくんはアズキ味をご所望らしい…_where_", },
    5238 : { GREETING: "",
             QUEST : "なるほど、魔術師がキミをここに送ったのだな。申し訳ないが、アズキ味は売り切れてしまった。\aというより、コグの一団が持っていってしまったのだ。\aビッグスマイルのためだとか何とか言っていたな。\a取り返してきてくれると助かるよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "アイスクリームは見つかったかい？" },
    5280 : { GREETING: "",
             QUEST : "なるほど、魔術師がキミをここに送ったのだな。申し訳ないが、アズキ味は売り切れてしまった。\aというより、コグの一団が持っていってしまったのだ。\aビッグチーズのためだとか何とか言っていたな。\a取り返してきてくれると助かるよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "アイスクリームは見つかったかい？" },
    5239 : { QUEST : "取り返してきてくれてありがとう！\aはい、これがミニおじさんの分だよ。",
             GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "とけてしまう前にそれをミニおじさんに持っていったほうがいいよ。", },
    5240 : { GREETING: "",
             QUEST : "よろしい、よろしい。ほれ、カエルくんも。\aペロリ、ペロリ。\aよし、準備もあともう少しで整いそうだ。\a手をかわかす粉を持ってきてくれ。\aビッグホワイト達がカツラのメンテに使っている粉が良いから、それを取ってきてくれ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "粉は見つかったかね？" },
    5281 : { GREETING: "",
             QUEST : "よろしい、よろしい。ほれ、カエルくんも。\aペロリ、ペロリ。\aよし、準備もあともう少しで整いそうだ。\a手をかわかす粉を持ってきてくれ。\aビッグスマイル達が鼻のテカリをかくすために使っている粉が良いから、それを取ってきてくれ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "粉は見つかったかね？" },
    5241 : { QUEST : "よし。\a前も言ったように、パイを投げるには手を使ってはいけないのだ。\a魂をこめて、念で投げる。\aこれは実に深い。深すぎて考える時間が必要だから、キミはコグビルをいくつか倒してきなさい。\aタスクが終わったらここに戻ってきなさい。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キミのタスクはまだ終わっていないよ。", },
    5242 : { GREETING: "",
             QUEST : "まだ考えがうまくまとまらない状態だが、キミが最終テストにふさわしい事はわかった。\aしゃべるカエルは言う、「ガールフレンドが欲しい」と。\a行ってしゃべるカエルちゃんを探してきなさい。それが最終タスクだ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "しゃべるカエルちゃんはどうしたんだ？",
             COMPLETE : "ふぅ！考えすぎてなんだか疲れてしまった。\aほれ、これをごほうびにあげるから私を休ませてくれ" },

    5243 : { QUEST : "あせかきピートのせいでここいらがくさくなってきちゃったんだよ。\aおふろに入るよう彼を説得してくれないか？_where_" },
    5244 : { GREETING: "",
             QUEST : "そうだねぇ、ボクは確かによく汗をかくかも。\aでもねぇ、うちのシャワーのこわれたパイプを直さなきゃ体も洗えないよ。\aちっちゃいコグならパイプを直せるギアを持っているかもね。\aガミガミーナからひとつ取ってきてくれない？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "ギアは見つかったの？" },
    5245 : { GREETING: "",
             QUEST : "うん、これなら何とかなるかも。\aでも、一人でお風呂に入るのはさみしいよ…\a池にいって、アヒルの人形をひとつ取ってきてくれない？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "アヒルは見つかったの？" },
    5246 : { QUEST : "アヒルちゃんを取ってきてくれてうれしいけど…\aうちのまわりの建物がこわくて落ち着かないよ。\aもう少し建物の数が少なかったら安心できるんだけど…",
             LEAVING : "",
             COMPLETE : "うん、じゃあお風呂に入ることにするよ。これはキミにあげる。",
             INCOMPLETE_PROGRESS : "まだ建物の存在がこわいよ…", },
    5251 : { QUEST : "ラウンジ・ラッサーが今夜、ショーをやるんだって。\aでもなんだかトラブルがあってこまってるみたい。_where_" },
    5252 : { GREETING: "",
             QUEST : "おおっと、手伝いにきてくれたのかい？\aバンから機材を下ろしていたらコグどもがギアを持っていっちまったんだよ。\a盗まれたマイクを取り返してきてくれないか？",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "おいおい、マイクなしじゃ歌えないよ。" },
    5253 : { GREETING: "",
             QUEST : "これだよ、俺のマイクは。\a取り返してくれてサンキュー。でも…\aキーボードもとられちまったんだよ、あれも必要なんだ。\aデッパラーダが持ってったと思うんだ、頼む！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キーボード、まだ見つかってないのか…" },
    5273 : { GREETING: "",
             QUEST : "これだよ、俺のマイクは。\a取り返してくれてサンキュー。でも…\aキーボードもとられちまったんだよ、あれも必要なんだ。\aオマカセンヌが持ってったと思うんだ、頼む！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キーボード、まだ見つかってないのか…" },
    5274 : { GREETING: "",
             QUEST : "これだよ、俺のマイクは。\a取り返してくれてサンキュー。でも…\aキーボードもとられちまったんだよ、あれも必要なんだ。\aシャークロンが持ってったと思うんだ、頼む！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キーボード、まだ見つかってないのか…" },
    5275 : { GREETING: "",
             QUEST : "これだよ、俺のマイクは。\a取り返してくれてサンキュー。でも…\aキーボードもとられちまったんだよ、あれも必要なんだ。\aホウノトリが持ってったと思うんだ、頼む！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キーボード、まだ見つかってないのか…" },
    5254 : { GREETING: "",
             QUEST : "やったぜ、ありがとな！\aでもなぁ、俺の厚底シューズがなきゃイマイチ決まんないんだよなぁ。\a俺のカンでは、持ってったのはビッグスマイルだな。",
             LEAVING : "",
             COMPLETE : "イエー！これでステージに立てるぜ！\aブルブルタウンのみんなー、元気かーい！？\a…ん？客がいないぞ？\aしょうがないな、これで客を集めてくれないか？",
             INCOMPLETE_PROGRESS : "はだしでステージになんか立てないよ。なぁ？" },
    5282 : { GREETING: "",
             QUEST : "やったぜ、ありがとな！\aでもなぁ、俺の厚底シューズがなきゃイマイチ決まんないんだよなぁ。\a俺のカンでは、持ってったのはビッグチーズだな。",
             LEAVING : "",
             COMPLETE : "イエー！これでステージに立てるぜ！\aブルブルタウンのみんなー、元気かーい！？\a…ん？客がいないぞ？\aしょうがないな、これで客を集めてくれないか？",
             INCOMPLETE_PROGRESS : "はだしでステージになんか立てないよ。なぁ？" },
    5283 : { GREETING: "",
             QUEST : "やったぜ、ありがとな！\aでもなぁ、俺の厚底シューズがなきゃイマイチ決まんないんだよなぁ。\a俺のカンでは、持ってったのはドロビッグだな。",
             LEAVING : "",
             COMPLETE : "イエー！これでステージに立てるぜ！\aブルブルタウンのみんなー、元気かーい！？\a…ん？客がいないぞ？\aしょうがないな、これで客を集めてくれないか？",
             INCOMPLETE_PROGRESS : "はだしでステージになんか立てないよ。なぁ？" },
    5284 : { GREETING: "",
             QUEST : "やったぜ、ありがとな！\aでもなぁ、俺の厚底シューズがなきゃイマイチ決まんないんだよなぁ。\a俺のカンでは、持ってったのはビッグホワイトだな。",
             LEAVING : "",
             COMPLETE : "イエー！これでステージに立てるぜ！\aブルブルタウンのみんなー、元気かーい！？\a…ん？客がいないぞ？\aしょうがないな、これで客を集めてくれないか？",
             INCOMPLETE_PROGRESS : "はだしでステージになんか立てないよ。なぁ？" },

    5255 : { QUEST : "あんた、もうちょっとゲラゲラポイントがあってもいいみたいだな。\a_toNpcName_なら安くしてくれるかもしれないぜ。\aちゃんと書き出してもらえよ。_where_" },
    5256 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "約束は守ってくださいよ。",
             QUEST : "ゲラゲラポイントがほしいって？\aウチに来て正解ですよ、お客さん！\aボスボットを何体かたおしてくれたら…\aサービスしますよ。" },
    5276 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "約束は守ってくださいよ。",
             QUEST : "ゲラゲラポイントがほしいって？\aウチに来て正解ですよ、お客さん！\aロウボットを何体かたおしてくれたら…\aサービスしますよ。" },
    5257 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "え？ロウボットをやっつけるようにお願いしませんでしたか？\aまあいいでしょう、でもこれであなたには私に借りができましたからね。",
             INCOMPLETE_PROGRESS : "まだ終わっていませんよ。",
             QUEST : "え、終わった？すべてのコグをやっつけた？\a何かの聞き間違いでしょう、私はセルボットを倒してくれと言ったのです。" },
    5277 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "え？ロウボットをやっつけるようにお願いしませんでしたか？\aまあいいでしょう、でもこれであなたには私に借りができましたからね。",
             INCOMPLETE_PROGRESS : "まだ終わっていませんよ。",
             QUEST : "え、終わった？すべてのコグをやっつけた？\a何かの聞き間違いでしょう、私はマネーボットを倒してくれと言ったのです。" },

    # Eddie the will give you laff point for helping him
    5301 : { QUEST : "ゲラゲラポイントs, でもひょっとしたら_toNpcName_が手伝ってくれるかも。\a彼はちょっと気むずかしいところがあるんだけどね。_where_" }, 
    5302 : { GREETING : "",
             LEAVING : "",
             COMPLETE : "思ったとおりだ！\aありがとな！ゲラゲラポイントだ！",
             INCOMPLETE_PROGRESS : "やあ！\aここでまた何しているんだい。",
             QUEST : "ゲラゲラポイントが欲しいって？\aまず最初に悪いロウボット達をやっつけてからにしてくれ。" },
    
    # Johnny Cashmere will knit you a large bag if...
    5303 : { QUEST : lTheBrrrgh+"が危険なコグ達であふれかえっているんだ。\aもし僕がキミなら、ここではギャグをもっと持ち歩くね。\aもしキミが足を棒にして働くんだったら、_toNpcName_が大きいバッグを作ることができるみたいだよ。_where_" },
    5304 : { GREETING: "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "まだロウボット達がそこら中にうようよしている。\aやっつけてくれ！" ,
             QUEST : "大きいバッグ？\aキミのために一つ作ってあげられるかも。\a毛糸が必要だけど、\a残念ながら、昨日の朝、ロウボット達に盗まれたんだ。" },
    5305 : { GREETING : "やあ！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "コグ達をもっとやっつけて！\aまだ毛糸がたりないよ。",
             QUEST : "上質の毛糸だね。\a色はちょっと好みじゃないけど。\aじゃあ、こうしよう。\aキミがもっと強いコグ達をやっつける間に、\a僕がこの毛糸を染めるね。" },
    5306 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "もっとやっつけてくれないと！",
             QUEST : "毛糸が全て染まったよ。でもちょとした問題があるんだ。\aあみ針がどこにも見つからないんだ。\a確か最後に見たのは池だったけなぁ。"  },
    5307 : { GREETING : "",
             LEAVING : "本当に助かるよ！",
             INCOMPLETE_PROGRESS : "ローマは一日にして編めず" ,
             QUEST : "確かに僕のあみ針だ。\aあみものをしている間に、コグビルをやっつけてくれないかい？",
             COMPLETE : "本当にすごいね、キミは！\aそしてこれもすごいよ…\aキミの新しいバッグだよ！" },

    # March Harry can also give you max quest = 4. 
    5308 : { GREETING : "",
             LEAVING : "",
             QUEST : "_toNpcName_が何か問題をかかえてるみたいなんだ。\aちょっと立ち寄って聞いてきてくれない？_where_"  },
    5309 : { GREETING : "来てくれて本当にうれしいよ。",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "急いで！ストリートにコグがあふれてるんだ！",
             QUEST : "ロウボット達が乗っ取りを始めているんだ。\aひょっとしたら僕をサイバンショに連れて行くんじゃないかと心配なんだ。\aあいつらを街から追い出してくれないかい？"  },
    5310 : { GREETING : "",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "彼らはきっと僕を連れてこうとしているんだ…",
             QUEST : "ありがとう。ちょっと気が楽になったよ。\aでもまだ、もうひとつやることがあるんだ。\a_toNpcName_のところに行って、アリバイをゲットしてきてくれないかい？_where_"  },
    5311 : { GREETING : "ヤッター！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "キミが見つけないと彼を助けてあげられないよ。",
             QUEST : "アリバイ？！それはいいアイデアだね！\aホウノトリがきっともっているはず。"  },
    5312 : { GREETING : "ついに！",
             LEAVING : "",
             INCOMPLETE_PROGRESS : "",
             COMPLETE : "ほっ。気持ちがようやく落ち着いたよ。\aこれがキミへのごほうびだ。",
             QUEST : "ほんとうにすばらしい！\a_toNpcName_のところへ急いでいってあげて！"  },

    # Powers Erge, though forgetful, will give you an LP boost
    # if you'll defeat some Cogs for him
    6201 : { QUEST : "テティ・テーデンが助けを必要としてるみたい。彼女に手を貸してあげて？_where_",
             },
    6202 : { GREETING : "",
             LEAVING : "",
             QUEST : "いらっしゃいませ！\aあら、お客様じゃないのね。\aわかった、恐ろしいコグたちから助けてくれるためにきてくれたのよね。\aもしコグたちからこの街を少し救ってくれたら、わたしが電気の力でキミのために何かしてあげられるんだけどな…。",
             INCOMPLETE_PROGRESS : "コグたちをやっつけてくれないと、お手伝いできないのよね。よろしくね！",
             COMPLETE : "_avName_、コグたちをやっつけてくれて、ありがとう！\aこれで電気が使えるわ。\aちょっと待ってね。この電気でキミを…。ビビビビビ！\aどう？ちょっとパワーアップした？これからもがんばってね！",
             },

    # Susan Siesta wants to get rich but the コグたち are interfering.
    # Take out some Cog buildings and she'll give you the small backpack
    6206 : { QUEST : "やあ, _avName_, 今すぐには何もないよ。\aあ、ちょっと待って！スーザン・シエスタが助けが欲しいって言ってたよ。なんで、彼女に会いにいかないの？_where_",
             },
    6207 : { GREETING : "",
             LEAVING : "",
             QUEST : "まったく！コグたちのせいで、商売があがったりなの。\a_avName_、助けてくれる？ \aいくつかのコグビルを取り返してくれたら、ごほうびをあげるわ。",
             INCOMPLETE_PROGRESS : "がっかり…。まだコグビルを取り返してないの？",
             COMPLETE : "ありがとう！これで商売もうまくいくはず！そんな気がする。\aこれで楽しみな釣りの時間も取れるわ。じゃあ、キミの人生をちょっと豊かにしてあげるね。\aはい、これをどうぞ！",
             },

    # Lawful Linda is fixing her answering machine.
    # Help her & she'll give you a 2LP reward.
    6211 : { QUEST : "こんにちは _avName_！ ロウフル・リンダ があなたをさがしてたって聞いたよ。.\aちょっと立ち寄って、あいさつしてみなよ。_where_",
             },
    6212 : { GREETING : "",
             LEAVING : "",
             QUEST : "こんにちは！ ワオ、キミに会えてうれしいよ！\a今、るすばんでんわを直している最中なんだけど、部品が足りないんだ。\a３つの棒が必要なんだけど、１つはカッチリンが持っているみたいなんだ。「ロッド」を持ってきてくれる？",
             INCOMPLETE_PROGRESS : "まだ、「ロッド」を探しているの？",
             },
    6213 : { GREETING : "",
             LEAVING : "",
             QUEST : "これでよし、っと！\a「自動車のベルト」のスペアのもっていたはずなんだけど見つからないなぁ。\aカネモッチンからベルトをひとつ、もってきてくれないかな？ありがとう！",
             INCOMPLETE : "うーん。自動車のベルトを持ってきてくれないと、キミを助けられないよ。",
             },
    6214 : { GREETING : "",
             LEAVING : "",
             QUEST : "これこれ！これでチチンプイプイ！ちゃんと動くはず。\aあれ、でも道具がないや。\aセコビッチを倒して、「ペンチ」を持ってきてくれないかな？\aそうしてくれれば、コグたちをやっつける手助けができるんだけどな。よろしくね。",
             INCOMPLETE_PROGRESS : "ペンチはまだかい？探しつづけてね！",
             COMPLETE : "すばらしい！ペンチでここをしめつけて、っと！\a直ったみたいだね。仕事に戻らないと！\aそういえば、電話がないけど、まあいいか。\aこれはお礼のしるし。グッド、ラック!",
             },

    # Scratch Rocco's back and he'll scratch yours.
    # In fact, he'll give you a 3 LP bonus.
    6221 : { QUEST : "ロッコが助けが必要だって聞いたよ。彼を手伝ってあげられる？_where_",
             },
    6222 : { GREETING : "",
             LEAVING : "",
             QUEST : "よぉっ！ちょ～どい～とこにきたね～。ごきげんだね！\aオォ、イェ～っ！コグたちにこまってるんだよね～。ボスボット、やっつけてくれるとハッピ～なんだけど、できそ？",
             INCOMPLETE_PROGRESS : "やぁ、_avName_。\aボスボット、ど～だい？やくそくしたろ～？\aロッコ、やくそくまもる。これ、きまり～。",
             COMPLETE : "よぉ、_avName_！これでボスボットもいばらなくなったかもね～！\aほ～らよっと！どでかいごほうびだ！トラブルにはまきこまれるなよ～！",
             },

    # Nat & PJ will get you acquainted with the new 
    # HQ. And they'll give you your first suit part
    6231 : { QUEST : "パジャマ・プレイスにいるナットがマネーボット本部のうわさを聞いたって。\aちょっと手伝えるかどうか彼のところに向かってくれる？ where_",
             },
    6232 : { GREETING : "",
             LEAVING : "",
             QUEST : "ちょっと変なうわさを小耳にはさんだんだよね。\aでもひょっとしたらデマかもしれないけど、きっと何かは起こっているんだよ。\aあのマネーボットたちのことさ！\aパジャマ・プレイスのすぐ近くに新しい本部を作ったみたいなんだよね。\aP.J.が知っているみたいなんだよね。\a_toNpcName_に会ってみて！_where_\aで、何か知らないか聞いてみて！",
             INCOMPLETE_PROGRESS : "まだP.J.に会ってないの？\a何か別の用事でもあるの？",
             },
    6233 : { GREETING : "",
             LEAVING : "",
             QUEST : "やあ、_avName_。どこにいたんだい？\aえっ、マネーボット本部？！何も見てないけどなぁ～。\aパジャマ・プレイスの奥まで行って本当かどうか見てきてくれない？\a本部があったら、中のマネーボットたちを倒して、戻ってきてよ。",
             INCOMPLETE_PROGRESS : "マネーボット本部は見つけた？様子を知るために、中のコグたちをやっつけてよ。",
             },
    6234 : { GREETING : "",
             LEAVING : "",
             QUEST : "えっ？！マネーボット本部が実在するって？\aナットに今すぐ伝えてくれない？\a彼のいるすぐ近くにコグ本部があっただなんて信じられる？",
             INCOMPLETE_PROGRESS : "ナットはなんて言うかな？まだ彼に会ってないんでしょ？",
             },
    6235 : { GREETING : "",
             LEAVING : "",
             QUEST : "P.J.のいうことは聞きあきたんだよね。\aもっとちゃんとした情報がほしいなぁ。その前に、このノミたちをなんとかしないと。\aわかった！もう一回、やっつけに行って「マネーボット本部プラン」を取ってきてよ。\aそしたら信じるよ。",
             INCOMPLETE_PROGRESS : "「プラン」はまだ？本部にいるコグたちならきっともっているはず！",
             COMPLETE : "えっ、「プラン」を持ってきたって！\aすばらしい！ふむふむ…。\aマネーボットがお金工場で「コグドル」を作っているって！\aきっとマネーボットだらけなんだろうね！でもより深く調べないと！\aコグに変装できればなぁ…。ちょっと待てよ。どこかにコグスーツのパーツがあったはずなんだけど…。\aあった！これを持っていけば何か役に立つはず。手伝ってくれてありがとう！",
             },

    # The Countess can't concentrate on counting her sheep with all 
    # these Cogs around. Clean up a bit and she'll reward you handsomely.
    # Reward: MaxMoneyReward 705 - 150 jellybeans
    6241 : { QUEST : "カウンテスがキミのことを探し回っていたよ。彼女のところにいって声をかけてあげて！_where_",
             },
    6242 : { GREETING : "",
             LEAVING : "",
             QUEST : "_avName_ね。きっと私のことを助けてくれると信じているわ。\aコグたちがさわがしくて集中できないの。\aいつも寝る前にひつじを数えるんだけど、うるさくていつも数え間違えちゃうのよ。\aもしコグたちをやっつけてくれたら、キミを助けてあげられるんだけど。まかせて！\aで、何匹数えたっけ？あっ、そうそう。ひつじが１３６匹、ひつじが１３７匹、…。",
             INCOMPLETE_PROGRESS : "ひつじが４４２匹、ひつじが４４３、…\aえっ？もう、戻ったの？でもまだ外はうるさいじゃない！\aあーっ、また忘れちゃった！\aひつじが１匹、ひつじが２匹、…",
             COMPLETE : "ひつじが５９３匹、ひつじが５９４匹、…\aあら？どうやら私の目にくるいはなかったようね。このしずけさ…。\aはい、スウジスキーなわたしからどうぞ。\aスウジ？あらやだ、また忘れちゃった。ひつじが１匹、ひつじが２匹、…",
             },

    # Zari needs you to run some errands for her and maybe
    # wipe out some Cogs along the way. She'll make it worthwhile
    # though, she'll give you 4 LP if you run the gauntlet.
    6251 : { QUEST : "かわいそうなザリがお客さんに配達をすることができないみたいなんだ。キミならきっと助けてあげられるはず。_where_",
             },
    6252 : { GREETING : "",
             LEAVING : "",
             QUEST : "こんにちは _avName_！ 配達を手伝ってくれるの？\aすごい！配達する機械がこわれて動けないの。\aちょっと待ってね。これならすぐできるはず！カウボーイ・ジョージが先週、「シタール」を注文したのよ。\a本当に悪いわね。彼に届けてくれる？_where_",
             INCOMPLETE_PROGRESS : "うーん、何か忘れてな？ カウボーイ・ジョージは「シタール」を待ってるよ。",
             },
    6253 : { GREETING : "",
             LEAVING : "",
             QUEST : "ぼくのシタール！ あー、はやく曲をひきたいなぁ。\aザリにありがとうって伝えてくれない？",
             INCOMPLETE_PROGRESS : "シタールを見つけてくれてありがとう！ザリがほかに何か手伝ってもらいたいたいと思ってるはすだよ。",
             },
    6254 : { GREETING : "",
             LEAVING : "",
             QUEST : "早かったわね。次は何をすれば良いかって？\aオッケー。マスター･マイクが「せいひょうき」を注文したのよ。\a今度はこれをよろしくね！_where_",
             INCOMPLETE_PROGRESS : "「せいひょうき」をマスター･マイクへ持っていてくれないと。_where_",
             },
    6255 : { GREETING : "",
             LEAVING : "",
             QUEST : "やったね！僕が注文した「せいひょうき」だ！\aそこらじゅうにコグたちがいなければ使えるんだけど…、マネーボットをちょっとやっつけてくれない？",
             INCOMPLETE_PROGRESS : "マネーボットのやつらはてごわいでしょ。早く「せいひょうき」を使いたいなぁ。",
             },
    6256 : { GREETING : "",
             LEAVING : "",
             QUEST : "すごいね！これで「せいひょうき」を動かせるよ。.\aザリに来週、また注文するって伝えてくれない？お願い！",
             INCOMPLETE_PROGRESS : "今は特に用事はないけど、ザリがキミを待ってるんじゃない？"
             },
    6257 : { GREETING : "",
             LEAVING : "",
             QUEST : "で、マスター･マイクが、「せいひょうき」、よろこんでたんだ～。よかったわ！\a次は、えっと…。そうだ、ゼン・グレンが「しまうまのざぶとん」を注文したの。\aはい、どうぞ！彼のところにさっと届けにいってくれる？_where_",
             INCOMPLETE_PROGRESS : "ゼン・グレンがきっと、その「しまうまのざぶとん」。待ちこがれていると思うよ。",
             },
    6258 : { GREETING : "",
             LEAVING : "",
             QUEST : "ついに「しまうまのざぶとん」が手に入った！ これでやっとメイソウができる。\a………………\aだけどコグたちがさわがしくて集中できやしない！\aコグたちをやっつけてくれるよね？\a幸せにメイソウしたいなぁ～。",
             INCOMPLETE_PROGRESS : "まだコグたちがうるさいなぁ！キミはメイソウできる？",
             },
    6259 : { GREETING : "",
             LEAVING : "",
             QUEST : "んー。「平和」と「しずけさ」。キミにも幸せがおとずれるよ、_avName_。\aザリに僕がどれだけ喜んでたか伝えてね。ありがとう！ ",
             INCOMPLETE_PROGRESS : "ザリから電話があって、キミを探してるってさ。会いに行って何が欲しいか聞いてきなよ。",
             },
    6260 : { GREETING : "",
             LEAVING : "",
             QUEST : "「しまうまのざぶとん」、ゼン・グレンがよろこんでくれたんだって！うれしいよ！\aおっと、ちょうど「ひゃくにちそう」が届いたよ。\aローズ・ペタルが待ちわびてるみたいだから、悪いんだけど彼女に届けてあげて！_where_",
             INCOMPLETE_PROGRESS : "はやく届けないと「ひゃくにちそう」がかれちゃうよ。",
             },
    6261 : { GREETING : "",
             LEAVING : "",
             QUEST : "何て素敵な「ひゃくにちそう」なの！ザリならきっと届けてくれると思った！\aいや、_avName_ならきっと！ってね。ザリにありがとうって伝えて！",
             INCOMPLETE_PROGRESS : "ザリに「ひゃくにちそう」のお礼をちゃんと言ってね！",
             },
    6262 : { GREETING : "",
             LEAVING : "",
             QUEST : "_avName_、よく戻ってくれたわ。いつも本当にありがとう！キミは本当に元気よね！\さてリストにはなんて書いてあるかしら…。\aこれこれ！この「ザイデコのレコード」をアイ・パチーリに届けてくれる？_where_",
             INCOMPLETE_PROGRESS : "きっとアイ・パチーリがザイデコのレコードを待ってるよ。",
             },
    6263 : { GREETING : "",
             LEAVING : "",
             QUEST : "ザイデコのレコード？ ザイデコのレコードを頼んだのを覚えてないよ。\aひょっとしたらララバイ・ルーが頼んだのかもしれないね。_where_",
             INCOMPLETE_PROGRESS : "きっとザイデコのレコードはララバイ・ルーのものだよ。_where_",
             },
    6264 : { GREETING : "",
             LEAVING : "",
             QUEST : "ザイデコのレコード！ ザリが忘れてたかと思ってた。\a彼女にこの「ズッキーニ」を持って行ってくれる？ 彼女なら誰がこれを必要としているか、わかるはず。ありがと！",
             INCOMPLETE_PROGRESS : "「ズッキーニ」ならたくさん持ってるわ。ザリにひとつもっていってあげて！",
             },
    6265 : { GREETING : "",
             LEAVING : "",
             QUEST : "ズッキーニ？ きっと誰かがほしいはずね。.\a配達リストもあと少しね。\aベイビーフェイス・マクドゥーガルが「ズート･スーツ」を注文してたわ。よろしくお願いね。_where_",
             INCOMPLETE_PROGRESS : "申し訳ないんだけど「ズート･スーツ」を早く届けないとしわくちゃになっちゃうわ。",
             },
    6266 : { GREETING : "",
             LEAVING : "",
             QUEST : "むかしむかし、あるところに。おじいさんと…。おっと、むかし話を聞きにきたようではないね。\a「ズート･スーツ」を届けにきてくれたんだね。すばらしい！ワオ！\aザリに伝言をお願いできるかな？このスーツにあうジルコンのカフスボタンが欲しいって！",
             INCOMPLETE_PROGRESS : "ザリにメッセージを伝えてくれた？",
             COMPLETE : "ジルコンのカフスボタン？ そうねぇ…。ちょっと探してみるわ。\aとにかく、とにかく！\aコグたちに立ち向かうのには、大きなゲラゲラポイントが必要ね！本当にいろいろ手伝ってくれてありがとう！はい、これが感謝の気持ち！",
             },

    # Drowsy Dave will give you teleport access to DL
    # if he can stay awake long enough for you to finish.
    6271 : { QUEST : "ドロジー・デイブが困っているみたい。キミならきっと助けてあげられるはず。彼の店に立ち寄ってあげて！_where_",
             },
    6272 : { GREETING : "",
             LEAVING : "",
             QUEST : "Zzzzz...\aZz、何？えっ？寝てないよ！たぶん…\a知ってる？コグビルの中には僕を眠くさせる機械がたくさんあるって。\a耳をかたむけると、ほら。\a………………\aはっ！そうそう。眠くならないようにコグビルをやっつけてくれない？",
             INCOMPLETE_PROGRESS : "Zzzzz...はっ！キミかぁ、_avName_。\a早かったね。ちょっと昼寝をしていたんだ。\aコグビルをやっつけてくれないと………。Zzzzz...",
             COMPLETE : "あれっ！あれれれれっ！\aコグビルがなくなって、ようやくリラックスできるよ。\a_avName_、本当にありがとう。\aまたね。リラックスしたらおかげで昼寝したくなったよ。",
             },

    # Teddy Blair has a piece of a cog suit to give you if you will
    # clear out some cogs. Of course, his ear plugs make it tough. 
    6281 : { QUEST : "テディ・ブレアのところに行って、キミの仕事をもらおう！_where_",
             },
    6282 : { GREETING : "",
             LEAVING : "",
             QUEST : "何だって？キミの仕事なんてないよ。\a仕事！どうしてそう言ってくれなかったんだ！もっとちゃんと言ってれなきゃ。\aコグたちがじゃまして冬眠ができないんだ。もしキミがドリームランドを静かにしてくれたら、\aちょっとした何かをあげるよ。",
             INCOMPLETE_PROGRESS: "「ゴグ」をやっつけた？「ゴグ」って何かって？\aああ、「コグ」ね！ そうしてそう言ってくれなかったんだ！\aまだ静かになってないから、もう少しやっつけてくれないかい？",
             COMPLETE : "たのしかった？えっ？「たおした」って？\aやったね。本当に助けてくれてありがとう！\a部屋の奥にあったんだけど、使わないからどうぞ！\aきっと何かのパーツだから、他のパーツと一緒に使うんじゃない？ありがとう、_avName_！",
             },    
    
    # William Teller needs help! Those darn Cashbots swiped his 3
    # money bags to use in the Mint! Retrieve them and he'll give you
    # another cog Suit piece.
    6291 : { QUEST : "コグたちが第一ねんねタオル銀行に押し入ったんだ！ウィリアム・テラーの所に行って助けてあげて！",
             },
    6292 : { QUEST : "まったくマネーボットのやつらといったら！やつらは私の大切な読書ランプをぬすんでいった！\a今すぐ取り戻さないと。何とか取り戻してくれないか？\aもし読書ランプを取り戻してくれたら、私が「マネーマネー」に会えるようにしてあげよう。\a早く！",
             INCOMPLETE_PROGRESS : "ランプが必要なんだ！お願いだから探し続けて！",
             COMPLETE : "よく戻ったね！それに読書ランプも！\a感謝しつくしてもし尽くせないけど、お礼にこれをあげよう！",
             },
    
    # Help Nina Nightlight get a bed in stock -
    # she'll give you a suit part
    7201 : { QUEST : "ニーナ・ナイトライトがキミを探してたよ、_avName_。彼女が助けが必要だって。_where_",
             },
    7202 : { GREETING : "",
             LEAVING : "",
             QUEST : "わー！ 会えてうれしいわ、_avName_。さっそくなんだけど、助けてくれない？\aコグたちがじゃまして、私の倉庫に商品のベッドのざいこがなくなっちゃってるの。\aハーディ・トゥールのところにいってベッドをもってきてくれる？_where_ ",
             INCOMPLETE_PROGRESS : "ハーディからベッドを受け取った？彼女ならきっと持っているはず。",
             COMPLETE : "",
             },
    7203 : { GREETING : "",
             LEAVING : "",
             QUEST : "ベッド？もちろん、ここにあるわよ。\aニーナに届けてくれる？わかったかしら？\aニーナにな！ってね。\aジョーク、ジョーク！よろしく頼むわ。",
             INCOMPLETE_PROGRESS : "ニーナはよろこんでくれた？",
             COMPLETE : "",
             },
    7204 : { GREETING : "",
             LEAVING : "",
             QUEST : "残念ながらこのベッドじゃないの。こんなシンプルなベッドじゃなくて、もうすこしファンシーなベッドなのよ。\aそんなに時間はかからないと思うからよろしくね。",
             INCOMPLETE_PROGRESS : "ハーディーならきっともっとファンシーなベッドを持っているはずよ。",
             COMPLETE : "",
             },
    7205 : { GREETING : "",
             LEAVING : "",
             QUEST : "どうやらお気にめさなかったようね。でもきっとこれなら大丈夫。\aでもちょっとした問題があるの。実はまだ出来上がってないのよ。\a外にいるコグたちをやっつけている間に完成させるから、よろしく頼むわ。",
             INCOMPLETE_PROGRESS : "ベッドを作るにはまだ外がうるさいようね。\aやっつけたときが、ベッドの出来上がり！",
             COMPLETE : "",
             },
    7206 : { GREETING : "",
             LEAVING : "",
             QUEST : "おまたせ、_avName_！\aコグたちをやっつけてくれたおかげでベッドが出来たわ！\aニーナによろしくね。キミのおかげで仕事がはかどるわ！ありがとう！",
             INCOMPLETE_PROGRESS : "ニーナに早くベッドを届けてあげて！",
             COMPLETE : "なんて素敵なベッドなの！\aこれでお客さんも大満足間違いなし。_avName_、本当にありがとう！\aきっとキミならこれを使えるはず。ずっと前に誰かがわすれていったものみたい。",
             },
    7209 : { QUEST : "ハニー・ムーンに会いにいってごらん。手助けしてほしいみたいだよ。_where_",
             },
    7210 : { GREETING : "",
             LEAVING : "",
             QUEST : "おー、_avName_！キミの助けが必要なのよ！\a長い間、ゆっくり眠れないの。それもコグたちが私の大切なベッドカバーをうばっていったからなの。\aねぇ、ふとんやトニーに会って、青いベッドカバーがないか聞いてきてくれない？_where_",
             INCOMPLETE_PROGRESS : "トニーに青いベッドカバーのこと、聞いてくれた？",
             COMPLETE : "",
             },
    7211 : { GREETING : "",
             LEAVING : "",
             QUEST : "ハニーがベッドカバーを欲しいって？\a何色？青だって？！\a今、手持ちなのは全部、「赤」だから特別に作らないと。\a外にいるコグたちをやっつけてくれたら、作ってあげるよ。",
             INCOMPLETE_PROGRESS : "まだ青いベッドカバーを作っているんだ、_avName_。コグたちをやっつけて！",
             COMPLETE : "",
             },
    7212 : { GREETING : "",
             LEAVING : "",
             QUEST : "また会えてうれしいよ！ちょっとまってね…。\aはい、ベッドカバー。青だよ。彼女も間違いなく気に入るよ！",
             INCOMPLETE_PROGRESS : "ハニーはベッドカバーを気に入ってくれた？",
             COMPLETE : "",
             },
    7213 : { GREETING : "",
             LEAVING : "",
             QUEST : "私のベッドカバー？違うわ、これじゃないの。\a「しましまもよう」のが欲しいの！こんなデザインじゃ、落ち着いて眠れないわ。\aこれを彼に返して、しましまのをお願い。\aきっとあるはずよ。",
             INCOMPLETE_PROGRESS : "「しましまもよう」なの。トニーにお願いって伝えて！",
             COMPLETE : "",
             },
    7214 : { GREETING : "",
             LEAVING : "",
             QUEST : "なんだって！「しましまもよう」じゃ、だめだって？\aそっか…。何があるか調べてみるね。\aちょっと時間かかりそうだから、その間、コグたちの相手をしてもらっていいかな？\aキミが戻るころには、何か見つかるはずだから…。",
             INCOMPLETE_PROGRESS : "まだ他のベッドカバーを探している最中さ。コグたちの様子はどう？",
             COMPLETE : "",
             },
    7215 : { GREETING : "",
             LEAVING : "",
             QUEST : "よくコグたちの相手をしてくれたね！\aどうぞ！彼女もきっと気に入る青くてしましまのカバーさ！\a早くハニーにこれを届けてあげてよ。",
             INCOMPLETE_PROGRESS : "これ以上のものはないよ。\aハニーがきっと待ってるよ。",
             COMPLETE : "あら、まあ！なんてすてきなの！やっぱりこのデザインじゃないと！\aじゃあ、すてきな夢でもみるかしらね。じゃあね、_avName_。\aなあに？まだいるの？レディーが寝ようとしてるのがわからない？\aどうぞ、これを受け取って、私を休ませて。おやすみなさい！",
             },
 
    7218 : { QUEST : "ドリーミー・ダフネが「誰かに手伝ってもらいたい」って言ってたよ。_where_",
             },
    7219 : { GREETING : "",
             LEAVING : "",
             QUEST : "やあ、_avName_。会えてうれしいな！ コグたちが「まくら」をうばっていったの。\aテックスのところに「まくら」がないか見てきてくれません？_where_\aきっとあるはずなんだけどな？お願いします。",
             INCOMPLETE_PROGRESS : "テックスから「まくら」を受け取っていただけました？",
             COMPLETE : "",
             },
    7220 : { GREETING : "",
             LEAVING : "",
             QUEST : "元気？ダフネが「まくら」を欲しいって？そりゃまさにここだよ、キミ。\aはいどうぞ、_avName_！ダフネのところに持っていってあげな！それからよろしく伝えてくれよ！\a女の子を助けるのが生きがいなんでね。",
             INCOMPLETE_PROGRESS : "渡した「まくら」は女の子に合ってたのかな？",
             COMPLETE : "",
             },
    7221 : { GREETING : "",
             LEAVING : "",
             QUEST : "「まくら」だわ！\aあれっ、ちょっと待ってくださる？このまくら、やわらかすぎるわ。\aもっとかたいまくらがいいのですが…。\a申し訳ありませんがテックスにこれを返して、違うまくらを持ってないかきいてくれません？おねがいします。",
             INCOMPLETE_PROGRESS : "残念ながら違うの。やわらかすぎてしまって。テックスに違うまくらをたのんでください。",
             COMPLETE : "",
             },
    7222 : { GREETING : "",
             LEAVING : "",
             QUEST : "やわらかすぎるって？ちょっと考えさせて…\aそういや倉庫にかたいまくらがあったはずだったかな？\a後で取りに行くから、ここいらのコグたちをそうじしておいてくれるかな？",
             INCOMPLETE_PROGRESS : "倉庫に行くためにもコグをやっつけて！",
             COMPLETE : "",
             },
    7223 : { GREETING : "",
             LEAVING : "",
             QUEST : "もう戻ったの？すんばらしい！ダフネが探している「まくら」を取ってきたよ。\a早くこれを届けてあげてね。まかせたよ！",
             INCOMPLETE_PROGRESS : "このまくら、とってもかたいよ！ダフネもとっても気に入るはず。",
             COMPLETE : "きっとテックスならかたいまくらを持っているって信じてたわ。\aさわりごこちといい、かたさといいパーフェクト！\aこのコグスーツのパーツを受け取ってくれるかしら。",
             },
 
    # Sandy Sandman lost her pajamas but Big Mama
    # and Cat can help her out. If you hang in there,
    # you'll get another Cog Suit part.
    7226 : { QUEST : "サンディ・サンドマンのところによってあげて。彼女のパジャマがなくなって困っているみたいだよ。_where_",
             },
    7227 : { GREETING : "",
             LEAVING : "",
             QUEST : "あらっ、パジャマがない！なくなっちゃった！\aどうしたらいいの？あっ、わかった！\aビッグ・ママに会いに行ってくれない？きっとパジャマがあるはずよ。_where_",
             INCOMPLETE_PROGRESS : "ビッグ・ママからパジャマを受け取った？",
             COMPLETE : "",
             },
    7228 : { GREETING : "",
             LEAVING : "",
             QUEST : "まぁ、可愛いトゥーンね！ビッグ・ママのパジャマはバハマから取り寄せた最高のものよ。\aサンディ・サンドマンのパジャマね？ちょっとまってね。これかな？あれかな？\aはい、どうぞ。これで彼女もおしゃれに安心して眠れるわね。\a私の代わりに走って彼女に渡してくれる？今は、お店から出ることができないのよ。\a本当にありがとうね、_avName_。また、会いましょう！",
             INCOMPLETE_PROGRESS : "サンディーのためにパジャマを持っていかないと！_where_",
             COMPLETE : "",
             },
    7229 : { GREETING : "",
             LEAVING : "",
             QUEST : "ビッグ・ママがわたしにこれを？あらまぁ。\a足がついてないじゃない…\a私はいつも足つきパジャマを着て寝るのよ。みんなはどう？\a悪いけどこれを戻して足つきのやつをお願いできるかしら？",
             INCOMPLETE_PROGRESS : "私のパジャマは足がついてないとだめなの。ビッグ・ママに相談して！",
             COMPLETE : "",
             },
    7230 : { GREETING : "",
             LEAVING : "",
             QUEST : "足つきだって？ちょっと考えさせて。\aこれじゃないし、あれじゃないし…\aジャーン！足つきパジャマ！きれいな青のパジャマパジャマよ。他でさがそうったって、なかなか見つからないんだから！\a彼女に届けてあげて！ありがとう！",
             INCOMPLETE_PROGRESS : "サンディーは青い足つきパジャマを気に入ってくれた？",
             COMPLETE : "",
             },
    7231 : { GREETING : "",
             LEAVING : "",
             QUEST : "たしかに足はついてるけど、青いパジャマは着れないわ！\aビッグ・ママに色違いがあるか聞いてくれる？",
             INCOMPLETE_PROGRESS : "ビッグ・ママならきっと、色の違う足つきパジャマを持ってるはず。",
             COMPLETE : "",
             },
    7232 : { GREETING : "",
             LEAVING : "",
             QUEST : "それは残念ねぇ。足つきパジャマは青しか持ってないのよ。\aでもひょっとしてキャットならいくつか色のバリエーションを持ってるはずよ。_where_",
             INCOMPLETE_PROGRESS : "手持ちのパジャマはこれらしかないのよ。キャットのところに行ってみなさいよ。_where_",
             COMPLETE : "",
             },
    7233 : { GREETING : "",
             LEAVING : "",
             QUEST : "足つきパジャマ？もちろん！\aサンディーは青じゃだめなの？\aちょっとやっかいね。これはどうかしら？\a青じゃないし、ちゃんと足もついてるし。",
             INCOMPLETE_PROGRESS : "わたしは赤が好きよ。あなたは？\aサンディーも気に入ってくれるとうれしいんだけど。",
             COMPLETE : "",
             },
    7234 : { GREETING : "",
             LEAVING : "",
             QUEST : "いやよ。たしかに青じゃないけど、私の顔の色でこんな色のパジャマはきれると思う？\aそんなわけないわ。キャットに別の色をたのんで、お願い！",
             INCOMPLETE_PROGRESS : "キャットならもっといろいろパジャマを持ってるはず。わたしには赤は似合わないの。",
             COMPLETE : "",
             },
    7235 : { GREETING : "",
             LEAVING : "",
             QUEST : "ふーん、赤でもないと…。\aふむふむ。僕のひげによると、他にもあるらしい。\aもうちょっと考えてみるけど、取引しよう。\a僕が別のパジャマをみつけるから、かわりにコグビルをやっつけてよ。不安なんだ。\aパジャマを探しておくからよろしくね、_avName_。",
             INCOMPLETE_PROGRESS : "パジャマのためにも、ちゃんとコグビルをやっつけて。",
             COMPLETE : "",
             },
    7236 : { GREETING : "",
             LEAVING : "",
             QUEST : "コグたちをやっつけてくれてありがとう！\aサンディーのためのパジャマをみつけたよ。彼女が気に入ってくれるといいんだけど。\a急いで彼女に持っていってあげて。ありがとう！",
             INCOMPLETE_PROGRESS : "ねぇ、_avName_。サンディーがきっと首を長くしてパジャマを待ってるよ、",
             COMPLETE : "足つきのピンクのパジャマ！ かーんぺき！\aそれにサイズもぴったし。\a手伝ってくれた御礼をしないとね！\aこれなんてどうかしら？道でひろったんだけどね。",
             },
 
    # Smudgy Mascara needs Wrinkle Cream but
    # 39's missing ingredients. Help them out
    # and get a piece of Cog suit
    7239 : { QUEST : "スウィート・リップスのところに行こう！助けを必要としているよ。_where_",
             },
    7240 : { GREETING : "",
             LEAVING : "",
             QUEST : "にっくきコグたちが大切な「しわのばしクリーム」をうばっていったのよ！\aお客様の大切なものなのに…。\aリップのところに行って、特別なクリームの予備がないか見てくれる？ _where_",
             INCOMPLETE_PROGRESS : "「しわのばしクリーム」がないと仕事ができないの。\aリップが何を持ってるか聞いてくれる。",
             },
    7241 : { GREETING : "",
             LEAVING : "",
             QUEST : "ああ、クリームね。リップスからの特別なお願いだから、ふつうの作り方ではできないんだ。\aトップシークレットの材料のカリフラワーサンゴが必要なんだけど、あいにくざいこぎれでね…。\a釣りに行って、池から見つけてくれないかな？サンゴを見つけたらすぐにおいでよ。",
             INCOMPLETE_PROGRESS : "カリフラワーサンゴを特別なレシピで「しわのばしクリーム」にするのさ！",
             },
    7242 : { GREETING : "",
             LEAVING : "",
             QUEST : "ワオ、これはいい「カリフラワーサンゴ」だね！\aオッケー、こうして、ああして。そしてコンブをひとさじっと。\aあれコンブがないぞ？コンブもいるなぁ。\a悪いけどもう一度池に行って、「ねばねばコンブ」を取ってきてよ。",
             INCOMPLETE_PROGRESS : "「ねばねばコンブ」はお店じゃ売ってないんだ。\aクリームを作るのにかかせないのさ。",
             },
    7243 : { GREETING : "",
             LEAVING : "",
             QUEST : "おおおおっと。これはとってもねばねばなコンブだね。ありがとう、_avName_！\aそれじゃあ、シンジュをすりばちと「ごますり棒」で…。\aおや、今度は「ごますり棒」が見つからないぞ？棒がなきゃ、すりばちの意味がない…。\aきっとこの間、シャークロンが押し入ったときに取っていったのかも。\aマネーボット本部に行って「ごますり棒」を取り返してきて！",
             INCOMPLETE_PROGRESS : "だから「ごますり棒」がないと、シンジュをすりつぶせないよ。\aまったくシャークロンのやつらといったら！",
             },
    7244 : { GREETING : "",
             LEAVING : "",
             QUEST : "そうそう、これこれ！\aこれですりつぶして、かきまぜて…。\aはい、出来上がり！この出来立てフレッシュなクリームをスウィート・リップスに届けてあげて！",
             INCOMPLETE_PROGRESS : "彼女はいろいろこだわりがあるから早く、早く！",
             COMPLETE : "もっと大きい「しわのばしクリーム」はなかったの？\a今度はちゃんと多くたのまないとね。すぐなくなっちゃうから。\aまたね、_avName_！\aなあに？まだ何かようかしら？今から大忙し。\aはい、これを受け取って！",
             },

    # Lawbot HQ part quests
    11000 : { GREETING : "",
              LEAVING : "",
              QUEST : "もしロウボット変装パーツに興味があるなら、_toNpcName_をたずねてみて。\a彼は天気の研究の助けが必要みたいなんだ。_where_",
              },
    11001 : { GREETING : "",
              LEAVING : "",
              QUEST : "はい、はい。確かにロウボット変装パーツなら持ってますよ。\a僕にとっては興味がないものなんですがね。\a僕はトゥーンタウン全体の天気の変化について研究をしているんだ。\aコグの持っている気温センサーとだったら、喜んで変装パーツと交換するよ。\aまずは%sから始めたらどうかな？" % GlobalStreetNames[2100][-1],
              INCOMPLETE_PROGRESS : "ちゃんと%sを調べたかい？" % GlobalStreetNames[2100][-1],
              COMPLETE : "これはすばらしい！\a恐れていた通りだ…\aあ、そうそう。これが変装パーツだよ。",
             },

    11002 : { GREETING : "",
              LEAVING : "",
              QUEST : "もっとロウボット変装パーツがいるなら、_toNpcName_にもう一度、たずねてごらん。\a彼の研究のアシスタントが必要みたいなんだ。_where_",
              },
    11003 : { GREETING : "",
              LEAVING : "",
              QUEST : "ロウボット変装パーツがまだ必要だって？\aキミがそこまで言うのなら…\aでももう一つセンサーが必要なんだ。\a今度は%sのを探してみて。" % GlobalStreetNames[2200][-1],
              INCOMPLETE_PROGRESS : "キミは%sを調べているんだよね？" % GlobalStreetNames[2200][-1],
              COMPLETE : "ありがとう！\a変装パーツをどうぞ！",
             },
    11004 : { GREETING : "",
              LEAVING : "",
              QUEST : "ロウボット変装パーツがさらに必要なら_toNpcName_のところに戻ってみたら？\a天気の研究、まだ手助けがいるみたいだよ。_where_",
              },
    11005 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミは本当に優秀だね！\a今度は%sを調べてみてくれないかい？" % GlobalStreetNames[2300][-1],
              INCOMPLETE_PROGRESS : "ちゃんと%sを調べているのかい？" % GlobalStreetNames[2300][-1],
              COMPLETE : "ふーん、それにしてもこのセンサー見た目はあまりよくないが…\aありがとう。これがキミへのごほうびのパーツだ。",
             },
    11006 : { GREETING : "",
              LEAVING : "",
              QUEST : "さらに変装パーツが必要なんだよね。\a気温のデータがYou-know-who needs more temperature readings._where_",
              },
    11007 : { GREETING : "",
              LEAVING : "",
              QUEST : "また戻ったのかい？\a非常に熱心だね。\a次の場所は%sだ。" % GlobalStreetNames[1100][-1],
              INCOMPLETE_PROGRESS : "%sを探しているんだよね？" % GlobalStreetNames[1100][-1],
              COMPLETE : "おみごと！じゅんびがととのったね。\aほら、へんそうパーツだよ！",
             },
    11008 : { GREETING : "",
              LEAVING : "",
              QUEST : "ロウボット変装パーツをお探しなら…。_where_",
              },
    11009 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミに会えてうれしいよ。\a次は%sのデータが欲しいんだ。お願いできるかな？" % GlobalStreetNames[1200][-1],
              INCOMPLETE_PROGRESS : "ちゃんと%sを調べたのかい" % GlobalStreetNames[1200][-1],
              COMPLETE : "どうもありがとう！\a変装パーツももうすぐ完成だね。",
             },
    11010 : { GREETING : "",
              LEAVING : "",
              QUEST : "きっと_toNpcName_がもっと仕事があるみたい。_where_",
              },
    11011 : { GREETING : "",
              LEAVING : "",
              QUEST : "また会えてうれしいよ、_avName_！\a%sのデータを取ってきてもらえるかな？" % GlobalStreetNames[1300][-1],
              INCOMPLETE_PROGRESS : "ちゃんと%sを調べたのかい？" % GlobalStreetNames[1300][-1],
              COMPLETE : "すばらしい仕事だったね。\aよくがんばったキミへのごほうびだよ。",
             },
    11012 : { GREETING : "",
              LEAVING : "",
              QUEST : "もうわかっているよね。_where_",
              },
    11013 : { GREETING : "",
              LEAVING : "",
              QUEST : "_avName_、僕の大切な友達！\a今度は%sへ行って別の温度センサーを見つけてくれないかい？" % GlobalStreetNames[5100][-1],
              INCOMPLETE_PROGRESS : "%sを探しているんだよね？?" % GlobalStreetNames[5100][-1],
              COMPLETE : "すばらしい！\aキミのおかげで研究が本当にはかどるよ！\aはい、ごほうび！",
             },
    11014 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_がキミを名差しでお願いしてきたよ。\aキミが頑張っているのが街のウワサになってるんだね。_where_",
              },
    11015 : { GREETING : "",
              LEAVING : "",
              QUEST : "よく戻ってきたね！\aキミのことを待っていたんだよ。\a次に必要なのが%sのデータさ。" % GlobalStreetNames[5200][-1],
              INCOMPLETE_PROGRESS : "キミは%sを調べているんだよね？" % GlobalStreetNames[5200][-1],
              COMPLETE : "ありがとう！\aはい、キミへのごほうび！",
             },
    11016 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミがロウボットにちゃんと変装したければ、\a_toNpcName_が助けになるはず。_where_",
              },
    11017 : { GREETING : "",
              LEAVING : "",
              QUEST : "やあ、研究者みならい君！\aさらに%sのデータが必要なんだよね。" % GlobalStreetNames[5300][-1],
              INCOMPLETE_PROGRESS : "%sだからね。" % GlobalStreetNames[5300][-1],
              COMPLETE : "すばらしい仕事だったね！\aはい、ロウボットのパーツをどうぞ。",
             },
    11018 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_がキミに別の仕事があるってさ。\a気に入ってくれるといいんだけど。_where_",
              },
    11019 : { GREETING : "",
              LEAVING : "",
              QUEST : "そっか…。\aさらに必要なんだね。\aそれなら今度は%sを試してみて！" % GlobalStreetNames[4100][-1],
              INCOMPLETE_PROGRESS : "%sを探しているんだよね？" % GlobalStreetNames[4100][-1],
              COMPLETE : "もうひとつ！\aキミはとってもスマートだね。",
             },
    11020 : { GREETING : "",
              LEAVING : "",
              QUEST : "ロウボット変装パーツを探しているのかい？_where_",
              },
    11021 : { GREETING : "",
              LEAVING : "",
              QUEST : "大体、察しがついているとは思うけど、\a今度は%sのデータが必要なんだ。" % GlobalStreetNames[4200][-1],
              INCOMPLETE_PROGRESS : "キミは%sを調べているんだよね？" % GlobalStreetNames[4200][-1],
              COMPLETE : "あとちょっとだね！\aはいどうぞ。",
             },
    11022 : { GREETING : "",
              LEAVING : "",
              QUEST : "ほんとうは言いたくないんだけど。。。_where_",
              },
    11023 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミは%sのことどう思う？センサーをゲットできると思う？" % GlobalStreetNames[4300][-1],
              INCOMPLETE_PROGRESS : "ちゃんと%sを調べた？" % GlobalStreetNames[4300][-1],
              COMPLETE : "またいい仕事をしたね、_avName_。",
             },
    11024 : { GREETING : "",
              LEAVING : "",
              QUEST : "もしまだ変装パーツが必要なら、教授のところにいってみたら？_where_",
              },
    11025 : { GREETING : "",
              LEAVING : "",
              QUEST : "残念ながら、%sのデータがまだ入手できてないんだ。" % GlobalStreetNames[9100][-1],
              INCOMPLETE_PROGRESS : "キミは%sをちゃんと調べているんだよね？" % GlobalStreetNames[9100][-1],
              COMPLETE : "いい仕事をしたね。\aあともうちょっとのところだね。",
             },
    11026 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミへの最後のミッションの内容は_toNpcName_が知ってるよ。_where_",
              },
    11027 : { GREETING : "",
              LEAVING : "",
              QUEST : "すぐもどってきたね。\a最後のデータは%s。" % GlobalStreetNames[9200][-1],
              INCOMPLETE_PROGRESS : "%sだからね。" % GlobalStreetNames[9200][-1],
              COMPLETE : "全部終わったね！\aこれでケンサツキョクに行って、ショウカンジョーを集められることができるね！\a今まで本当にありがとう。そして気をつけて！",
             },
    12000 : { GREETING : "",
              LEAVING : "",
              QUEST : "もしもボスボットのパーツにきょうみがあるなら_toNpcName_._where_に聞くといいかも。",
              },
    12001 : { GREETING : "",
              LEAVING : "",
              QUEST : "ボスボットのパーツかい？\aじゃぁ、ボスボット･コレクションに協力してくれるかな？\aなずはオベッカーからたのむよ。",
              INCOMPLETE_PROGRESS : "オベッカーが見つからない？ そんなはずないだろ…？",
              COMPLETE : "もうたおしたのかい？\aほら、さいしょのへんそうパーツだ。",
             },
    12002 : { GREETING : "",
              LEAVING : "",
              QUEST : "もっとパーツが必要ならやはり_toNpcName_に聞くべきだよ。_where_",
              },
    12003 : { GREETING : "",
              LEAVING : "",
              QUEST : "もう一つパーツが必要なのかい？\aもちろん...\aカリカリンを倒してきたらあげるよ。",
              INCOMPLETE_PROGRESS : "カリカリンはそのへんのストリートにいるだろうね。",
              COMPLETE : "朝メシ前だっただろ？\aさぁ、二つ目のパーツだよ。",
             },
    12004 : { GREETING : "",
              LEAVING : "",
              QUEST : "ボスボットのパーツなら…もうわかるよね？_where_",
              },
    12005 : { GREETING : "",
              LEAVING : "",
              QUEST : "次はイエスマンだ…。",
              INCOMPLETE_PROGRESS : "イエスマンもそのへんのストリートにいるだろう。",
              COMPLETE : "イエス！なかなかやるね。\aさぁ、三つ目のパーツだ。",
             },
    12006 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_がまだまだパーツを持ってるよ...",
              },
    12007 : { GREETING : "",
              LEAVING : "",
              QUEST : "ガミガミーナを倒したら次のをあげるよ。",
              INCOMPLETE_PROGRESS : "%sを探してみたかい？" % GlobalStreetNames[1100][-1],
              COMPLETE : "おみごと！\a四つ目のへんそうパーツだよ。",
             },
    12008 : { GREETING : "",
              LEAVING : "",
              QUEST : "次も...だね。_where_",
              },
    12009 : { GREETING : "",
              LEAVING : "",
              QUEST : "次はリストラマンだ。",
              INCOMPLETE_PROGRESS : "見つからないのかい？%sを探してごらん。" % GlobalStreetNames[3100][-1],
              COMPLETE : "やつはめんどうだったかい？\a五つ目のへんそうパーツだよ。",
             },
    12010 : { GREETING : "",
              LEAVING : "",
              QUEST : "キミ、…もうわかってるでしょ？_where_",
              },
    12011 : { GREETING : "",
              LEAVING : "",
              QUEST : "え～と、私のリストでは次はヘッドハンターだ。",
              INCOMPLETE_PROGRESS : "こいつの場合はビルの中を探すほうがいいかも。",
              COMPLETE : "早かったね！\aほら、六つ目のパーツだよ。",
             },
    12012 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_がもっとボスボットがひつようだって…。",
              },
    12013 : { GREETING : "",
              LEAVING : "",
              QUEST : "次はデッパラーダをつかまえてくれないか？",
              INCOMPLETE_PROGRESS : "こいつもやはりビルの中だろうな。",
              COMPLETE : "キミもなかなかやるねぇ。\a六つ目のパーツだ！",
             },
    12014 : { GREETING : "",
              LEAVING : "",
              QUEST : "もっとパーツが必要なんだろ？さ、行っておいで..._where_",
              },
    12015 : { GREETING : "",
              LEAVING : "",
              QUEST : "さぁ、とどめだ！ビッグチーズを！！",
              INCOMPLETE_PROGRESS : "%sにいるはずだぞ。" % GlobalStreetNames[10000][-1],
              COMPLETE : "キミはきたい通りのチーズ好き…\aあぁ、いや、なんでもない。\a次のへんそうパーツはこれだ。",
             },
    12016 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_がさがしてましたよ...",
              },
    12017 : { GREETING : "",
              LEAVING : "",
              QUEST : "実はキミに新しくてずるがしこいボスボットを倒してほしいんだ。",
              INCOMPLETE_PROGRESS : "%sをさがしてみてくれ。" % GlobalStreetNames[10000][-1],
              COMPLETE : "ヤツらは見た目よりつよいようだな。\aさぁ、へんそうパーツが必要なんだろ？",
             },
    12018 : { GREETING : "",
              LEAVING : "",
              QUEST : "さぁ、行っていって..._where_",
              },
    12019 : { GREETING : "",
              LEAVING : "",
              QUEST : "このバージョン2.0コグはとてもきょうみ深い。\aもっとさがしてきてくれるかい？",
              INCOMPLETE_PROGRESS : "%sにならいるだろう。" % GlobalStreetNames[10000][-1],
              COMPLETE : "ありがとう！\aジャジャーン、へんそうパーツをどうぞ！",
             },
    12020 : { GREETING : "",
              LEAVING : "",
              QUEST : "ついででいいんだけど、_toNpcName_のトコに行ってくれる？",
              },
    12021 : { GREETING : "",
              LEAVING : "",
              QUEST : "ヤツらはもしかしてどんどん強くなっているのか？",
              INCOMPLETE_PROGRESS : "%sを探してみてくれ。" % GlobalStreetNames[10000][-1],
              COMPLETE : "アレ？ヤツらそんなに強くはないの？\aそら、いつものだ。",
             },
    12022 : { GREETING : "",
              LEAVING : "",
              QUEST : "え～と..._where_",
              },
    12023 : { GREETING : "",
              LEAVING : "",
              QUEST : "た～ぶ～ん、ヤツらはボスボットじゃなくってなんか別のぉ...",
              INCOMPLETE_PROGRESS : "こいつらは%sにいるぞ。" % GlobalStreetNames[10000][-1],
              COMPLETE : "あ、これはやっぱボスボットだわ。\aふむ、へんそうパーツはそこにあるから…",
             },
    12024 : { GREETING : "",
              LEAVING : "",
              QUEST : "え～と、ちゃんと言わないとわかりませんか？",
              },
    12025 : { GREETING : "",
              LEAVING : "",
              QUEST : "いや、た～ぶ～んなんだけど、…ヤツらってガイコグ系じゃない？",
              INCOMPLETE_PROGRESS : "%sにいるだろう。" % GlobalStreetNames[10000][-1],
              COMPLETE : "う～む、どうもはっきりしないなあ。\aあ、へんそうパーツを持っていってね。",
             },
    12026 : { GREETING : "",
              LEAVING : "",
              QUEST : "フゥ～、_toNpcName_がよんでいますよ。",
              },
    12027 : { GREETING : "",
              LEAVING : "",
              QUEST : "どうもまだヤツらがガイコグのナカマなのかわからなくってねぇ。",
              INCOMPLETE_PROGRESS : "%sをさがすといいよ。" % GlobalStreetNames[10000][-1],
              COMPLETE : "あぁ～っと、ちがう…かな？\a…はい、次のパーツ！",
             },
    12028 : { GREETING : "",
              LEAVING : "",
              QUEST : "多分、もうここはうんざりだと思いますけど…。",
              },
    12029 : { GREETING : "",
              LEAVING : "",
              QUEST : "いやぁ、スマン！ヤツらの事でなやんでしまっていてね。\aもう一体だけたのめないかな？",
              INCOMPLETE_PROGRESS : "やはり%sにいるだろう。" % GlobalStreetNames[10000][-1],
              COMPLETE : "「すばらしい!」の一言につきるよ！\aへんそうパーツだ。受け取ってくれ。",
             },
    12030 : { GREETING : "",
              LEAVING : "",
              QUEST : "_toNpcName_はもうこわれたレコード…って、意味わかります？",
              },
    12031 : { GREETING : "",
              LEAVING : "",
              QUEST : "もうヤツらの事はなんでも私に聞いてくれ！\aところでそうだんなんだけど…",
              INCOMPLETE_PROGRESS : "きっと%sにならいるんじゃないか？" % GlobalStreetNames[10000][-1],
              COMPLETE : "よし、思った通りだ！\aあぁ、そうそう。\aこれはキミにだよ。",
             },
    12032 : { GREETING : "",
              LEAVING : "",
              QUEST : "フリッピーにこの事を伝えてくれる？",
              INCOMPLETE_PROGRESS : "フリッピーはトゥーンホールにいるよ。",
              COMPLETE : "新しいコグだって?!\a教えてくれてありがとう。\aお礼にさいごのへんそうパーツをあげるよ！",
              },
    }

# ChatGarbler.py
ChatGarblerDog = ["わんわん", "きゅう～ん", "わふわふ"]
ChatGarblerCat = ["にゃ～", "みゃ～"]
ChatGarblerMouse = ["チュ～チュ～", "チチッ", "チュ～"]
ChatGarblerHorse = ["ひひひん", "ぶるるん"]
ChatGarblerRabbit = ["チチッ", "ふんふんふん", "くんかくんか", "チッチッ"]
ChatGarblerDuck = ["グワッ", "グワワ～", "グワグワッ"]
ChatGarblerMonkey = ["ウキッ", "キー", "ウッキー"]
ChatGarblerBear = ["ガウ～", "ガルルル"]
ChatGarblerPig = ["ブヒブヒ！", "ブーッ！", "ブホブホッ！"]
ChatGarblerDefault = ["フガー"]

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = ""
AvatarDetailPanelClose = "閉じる"
AvatarDetailPanelLookup = "%s の状態を調べています…"
AvatarDetailPanelFailedLookup = "%s の状態を調べられませんでした。"
#AvatarDetailPanelPlayer = "Player: %(player)s\nWorld: %(world)s\nLocation: %(location)s"
# sublocation is not working now
AvatarDetailPanelPlayer = "ﾌﾟﾚｲﾔｰ: %(player)s\nﾜｰﾙﾄﾞ: %(world)s\nﾛｹｰｼｮﾝ: %(location)s"
AvatarDetailPanelPlayerShort = "%(player)s\nワールド: %(world)s\nﾛｹｰｼｮﾝ: %(location)s"
AvatarDetailPanelRealLife = "ｵﾌﾗｲﾝ"
AvatarDetailPanelOnline = "ﾛﾋﾞｰ: %(district)s\nｴﾘｱ: %(location)s"
AvatarDetailPanelOnlinePlayer = "ﾃﾞｨｽﾄﾘｸﾄ: %(district)s\nﾛｹｰｼｮﾝ: %(location)s\nﾌﾟﾚｲﾔｰ: %(player)s"
AvatarDetailPanelOffline = "ﾛﾋﾞｰ: オフライン\nｴﾘｱ: オフライン"
AvatarShowPlayer = "ﾌﾟﾚｲﾔｰをみる"
OfflineLocation = "Offline"

#PlayerDetailPanel
PlayerToonName = "ﾄｩｰﾝ: %(toonname)s"
PlayerShowToon = "ﾄｩｰﾝをみる"
PlayerPanelDetail = "詳細"


# AvatarPanel.py
AvatarPanelFriends = "ともだち"
AvatarPanelWhisper = "ささやく"
AvatarPanelSecrets = "ひみつ"
AvatarPanelGoTo = "ワープ"
AvatarPanelPet = "ﾄﾞｩｰﾄﾞｩﾙを見る"#▲
AvatarPanelIgnore = "むしする"
AvatarPanelIgnoreCant = lOK
AvatarPanelStopIgnoring = "むしをやめる"
AvatarPanelReport = "ほうこくする"
#AvatarPanelCogDetail = "部署: %s\nレベル: %s\n"
AvatarPanelCogLevel = "レベル：%s"
AvatarPanelCogDetailClose = "閉じる"
AvatarPanelDetail = "トゥーン情報"#▲
AvatarPanelGroupInvite = "グループに招待する"
AvatarPanelGroupRetract = "招待をやめる"
AvatarPanelGroupMember = "メンバー"
AvatarPanelGroupMemberKick = "おことわり"

# grouping messages
groupInviteMessage = "%sがグループに招待したいって"


# Report Panel
ReportPanelTitle = "めいわくトゥーン"
ReportPanelBody = "This feature will send a complete report to a Moderator. Instead of sending a report, you might choose to do one of the following:\n\n  - Teleport to another district\n  - Use \"Ignore\" on the toon's panel\n\nDo you really want to report %s to a Moderator?"
ReportPanelBodyFriends = "This feature will send a complete report to a Moderator. Instead of sending a report, you might choose to do one of the following:\n\n  - Teleport to another district\n  - Break your friendship\n\nDo you really want to report %s to a Moderator?\n\n(This will also break your friendship)"
ReportPanelCategoryBody = "You are about to report %s. A Moderator will be alerted to your complaint and will take appropriate action for anyone breaking our rules. Please choose the reason you are reporting %s:"
ReportPanelBodyPlayer = "This feature is stilling being worked on and will be coming soon. In the meantime you can do the following:\n\n  - Go to DXD and break the friendship there.\n - Tell a parent about what happened."

ReportPanelCategoryLanguage = "Foul Language"
ReportPanelCategoryPii = "Sharing/Requesting Personal Info"
ReportPanelCategoryRude = "Rude or Mean Behavior"
ReportPanelCategoryName = "Bad Name"

ReportPanelConfirmations = (
    "You are about to report that %s has used obscene, bigoted or sexually explicit language.",
    "You are about to report that %s is being unsafe by giving out or requesting a phone number, address, last name, email address, password or account name.",
    "You are about to report that %s is bullying, harassing, or using extreme behavior to disrupt the game.",
    "You are about to report that %s has created a name that does not follow Disney's House Rules.",
    )

# Put on confirmation screen!
ReportPanelWarning = "We take reporting very seriously. Your report will be viewed by a Moderator who will take appropriate action for anyone breaking our rules. If your account is found to have participated in breaking the rules, or if you make false reports or abuse the 'Report a Player' system, a Moderator may take action against your account. Are you absolutely sure you want to report this player?"

ReportPanelThanks = "Thank you! Your report has been sent to a Moderator for review. There is no need to contact us again about the issue. The moderation team will take appropriate action for a player found breaking our rules."

ReportPanelRemovedFriend = "We have automatically removed %s from your Toon Friends List."
ReportPanelRemovedPlayerFriend = "We have automatically removed %s as a Player friend so as such you will not see them as your friend in any Disney product."

ReportPanelAlreadyReported = "You have already reported %s during this session. A Moderator will review your previous report."

# Report Panel
IgnorePanelTitle = "このトゥーンをむしする"
IgnorePanelAddIgnore = "今回のログインセッションの間は%sをむししますか？"
IgnorePanelIgnore = "%sをむししています"
IgnorePanelRemoveIgnore = "%sをむしするのをやめますか?"
IgnorePanelEndIgnore = " %sをむしするのをやめました"
IgnorePanelAddFriendAvatar = "%sはあなたのともだちです。ともだちをむしする事はできません。"
IgnorePanelAddFriendPlayer = "%s (%s)はあなたのともだちです。ともだちをむしする事はできません。"

# PetAvatarPanel.py
PetPanelFeed = "えさをあげる"
PetPanelCall = "よぶ"
PetPanelGoTo = "行く"
PetPanelOwner = "かいぬし"
PetPanelDetail = "ペットの状態"
PetPanelScratch = "スクラッチ"

# PetDetailPanel.py
PetDetailPanelTitle = "トリックの練習"
# NOTE: these are replicated from OTPLocalizerEnglish sans "!"
PetTrickStrings = {
    0: 'ジャンプ',
    1: 'おじぎ',
    2: 'しんだふり',
    3: 'ころがる',
    4: 'ちゅうがえり',
    5: 'ダンス',
    6: 'はなす',
    }


# PetMood.py
PetMoodAdjectives = {
    'neutral': 'ふつう',
    'hunger': 'おなかがすいた',
    'boredom': 'たいくつしている',
    'excitement': 'こうふんしている',
    'sadness': 'かなしんでいる',
    'restlessness': 'おちつかない',
    'playfulness': 'ようきな',
    'loneliness': 'さびしがっている',
    'fatigue': 'つかれている',
    'confusion': 'こんらんしている',
    'anger': 'おこっている',
    'surprise': 'おどろいている',
    'affection': 'ラブラブ',
    }

SpokenMoods = {
    'neutral': 'ふつう',
    'hunger': 'ジェリービーンはあきちゃったかも。パイは食べちゃだめ？',
    'boredom': 'ペットはなんにもわかってないと思ってるでしょ？',
    'excitement': 'トゥーンタスティック！',
    'sadness': 'なにかイイ事ないかなぁ…',
    'restlessness': 'なんだか落ち着かないよ',
    'playfulness': '遊んでくれないと花だんをほっちゃうゾ！',
    'loneliness': 'いっしょにコグを倒しに行こうよ～',
    'fatigue': 'トリックの練習は大変なんだよ。きゅうけいさせて！',
    'confusion': 'ん？あなたダレ？ここはドコ？？？',
    'anger': 'いつも私をおいて遊びに行っちゃうでしょ！',
    'surprise': 'ワオッ！いつ帰ってきたの?!',
    'affection': 'いっしょにいられてうれしいよ！',
    }

# DistributedAvatar.py
DialogExclamation = "!"
DialogQuestion = '?'

# LocalAvatar.py
FriendsListLabel = "ともだち"

# TeleportPanel.py
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = "%s に行こうとしています。"
TeleportPanelNotAvailable = "%s はいそがしいようです。またあとでトライしてね。"
TeleportPanelIgnored = "%s があなたをむししています！"
TeleportPanelNotOnline = "%s はオンラインにいません。"
TeleportPanelWentAway = "%s は行ってしまいました。"
TeleportPanelUnknownHood = "%sへの行き方がわかりません！"
TeleportPanelUnavailableHood = "%s はいそがしいようです。またあとでトライしてね。"
TeleportPanelDenySelf = "自分をみつけられません！"
TeleportPanelOtherShard = "%(avName)s は%(shardName)sにいて、キミは%(myShardName)sにいるよ。%(shardName)sに移動する？"
TeleportPanelBusyShard = "%(avName)sは今こんざつしているロビーにいるよ。こんでいるロビーではゲームの反応がおそかったり安定しない場合があるけど、それでもワープする?"

# DistributedBattleBldg.py
BattleBldgBossTaunt = "私がボスだ！"

# DistributedBattleFactory.py
FactoryBossTaunt = "私が工場長だ！"
FactoryBossBattleTaunt = "われらの工場長を紹介しよう！"
MintBossTaunt = "私が金庫番だ！"
MintBossBattleTaunt = "われらの金庫番に話をしてもらおう！"
StageBossTaunt = "私が本当のせいぎなのだ！"
StageBossBattleTaunt = "私がほうりつなのだ！"
CountryClubBossTaunt = "私がこのクラブのオーナーだ！"
CountryClubBossBattleTaunt = "クラブのオーナーに会わせてやる。"
ForcedLeaveCountryClubAckMsg = "クラブのオーナーはキミがたどり着く前に倒されました。カイコツウチはもらえません。"

# HealJokes.py
ToonHealJokes = [
    ["となりの家に囲いができたんだってなぁ",
     "かっこいいー！"],
    ["田んぼに稲を植えました",
     "い～ね～"],
    ["屋根が落ちてきたんだって",
     "や～ね～"],
    ["その和紙は誰のだ？",
     "わしのだ"],
    ["この植物臭わない",
     "草っ！"],
    ["橋のどこを走るんだい？",
     "はしに決まってるじゃん！"],
    ["牛はどこだ？",
     "ウシろ～！"],
    ["牛が笑った",
     "ウシシシシ！"],
    ["パンダが好きな食べ物は？",
     "パンだ！"],
    ["アシカの世話は誰がするの？",
     "あっしか！？"],
    ["誰にやってもらおう？",
     "サイにまかせなサイ！"],
    ["テントウ虫のけがの原因は？",
     "転倒です"],
    ["白鳥のくしゃみは？",
     "ハクチョーン！"],
    ["鮭が叫んだ！",
     "裂ける～！"],
    ["サバをさばけないのです…",
     "サバイバルには向いてないな"],
    ["なんの魚を食べようかなぁ？",
     "タラでも食べタラ？"],
    ["イルカは逆立ちすると空を飛べるらしいよ！",
     "カルイってか！"],
    ["イカダに乗って、何を釣ってるの？",
     "イカだ！"],
    ["このイカ、くさってるよね？",
     "うーん、いかがわしい"],
    ["彼が作ったカレーの味はどう？",
     "かれぇ～！"],
    ["バナナが青いんだけど…",
     "そんなバナナな！？"],
    ["いちじくは何時に食べる？",
     "１時（に）食う！."],
    ["このワインは誰の？",
     "ワイんのだぁ～"],
    ["ソースの総数はたくさんあるらしいよ。",
     "へぇ、そーすか."],
    ["アメの味はどう？",
     "あめ～."],
    ["谷が深くて、",
     "困っタニ～"],
    ["虹を見たのは何時だろ？",
     "２時だろ？"],
    ["キミに借りた斧を折っちゃった…",
     "オーノー！"],
    ["石が落ちたんだってさ",
     "ストーンと…"],
    ["リスの話を聞こうよ！",
     "Listen!"],
    ["この蕎麦はおいしくないなぁ",
     "So bad！"],
    ["送った紙はいつ届くの？",
     "カミング・スーン"],
    ["卵が泣いてるようだ…",
     "エッグ、エッグ"],
    ["重量級の赤ちゃんだね。",
     "まさしくヘビー(ベビー)！"],
    ["鴨が言った",
     "カモーン！"],
    ["あの塔が倒れてしまったよ。",
     "そりゃ困っタワー."],
    ["シェフが時間ギリギリに間に合った",
     "シェーフ！！"],
    ["カッターを買ったら高かった",
     "じゃあ店は儲かったね。"],
    ["あのコック、居眠りしてるよ。",
     "コックりコックり"],
    ["このカレンダーは誰んだー",
     "俺んだー"],
    ["行き過ぎてしまった、どうしよう？",
     "大丈夫、モノレールでもどれーるよ！"],
    ["このお面誰の？",
     "おめぇんのだよ！"],
    ["涼しくなる楽器は？",
     "鈴～！"],
    ["もれる～！",
     "じゃあトイレに行っといれ"],
    ["スイマーも睡魔に負けた…",
     "すいません"],
    ["後ろに何か来てないか？",
     "じゃあ、バックミラーで見てみら～！"],
    ["床って、ゆーかー！",
     "ゆかいだな、キミは"],
    ["あなたは配送業ですか？?",
     "はい、そうです"],
    ["馬が、",
     "ウマれた！"],
    ["馬は走るのが、",
     "ウマい！"],
    ["猫が風邪で、",
     "ねこんだ"],
    ["逃げた虎を",
     "捕らえた"],
    ["豚が",
     "ぶたれた?"],
    ["犬が",
     "いぬる"],
    ["ラクダに乗ると",
     "楽だ"],
    ["象だ",
     "ゾウー！?"],
    ["トドが動物園に",
     "トドいた"],
    ["熊を",
     "かくまう！"],
    ["カバを",
     "かばった"],
    ["あのカバ、",
     "かばいい！"],
    ["ロバは",
     "こロバない"],
    ["ワニが",
     "わになって遊んでる～"],
    ["ネズミが",
     "寝ずに（ネズミ）番をした"],
    ["サルも",
     "リハーサルをしてます"],
    ["サルが",
     "去る"],
    ["かめない",
     "亀"],
    ["カエルが",
     "池にカエル"],
    ["ハチと",
     "ハチ合わせ！"],
    ["アブは",
     "あぶない！"],
    ["コウモリも",
     "子守でたいへん！"],
    ["ハエが",
     "はえ～"],
    ["鳥がエサを",
     "トリ返した"],
    ["カモメがこっちに",
     "来るかもめ！"],
    ["コンドルが",
     "飛んどる"],
    ["ハトが豆鉄砲うたれて",
     "ハッとした！"],
    ["アジを刺身を",
     "アジわおう！"],
    ["ヒラメが",
     "ヒラメいた！"],
    ["かれいに泳ぐ",
     "カレイ"],
    ["冷めてる",
     "サメ"],
    ["こぶりな",
     "ブリ"],
    ["マグロを焦がして",
     "マッグロにしちゃった"],
    ["鯛は",
     "めでタイ！"],
    ["コイも",
     "恋するらしいよ！"],
    ["フナも",
     "船酔いするんだって！"],
    ["カニは",
     "いるかに？"],
    ["貝は",
     "おいしいカイ？"],
    ["いかした",
     "イカ～"],
    ["イカの料理は、",
     "イカがですか？"],
    ["イクラは",
     "いくら？"],
    ["うめぼしが",
     "うめ～！"],
    ["のりを食べて…",
     "ノリノリだぜ～！"],
    ["ワカメは",
     "よくかめ！"],
    ["肉が",
     "ニクい～！"],
    ["このみそを",
     "食べてみそ！"],
    ["コーラを",
     "コオラした"],
    ["抹茶がしぶくて、",
     "こまっちゃう…"],
    ["プリンを食べて",
     "しらんプリン！"],
    ["栗にさわって",
     "びっクリ！"],
    ["ネギを",
     "ねぎった！"],
    ["秋の味覚は、",
     "いつ食べてもアキないね～"],
    ["暑さでビールの売り上げも、",
     "のビール！"],
    ["チョコを",
     "ちょこっと食べる"],
    ["コショウで",
     "故障"],
    ["ダイコン売り場は",
     "いつもだいこんざつ！"],
    ["稲をかるのに",
     "誰もイネー"],
    ["サクラが",
     "さくらしい！"],
    ["球があたって",
     "タマげた！"],
    ["棚が落ちてきて",
     "まいっタナ～"],
    ["板がぶつかってきて",
     "イタかった…"],
    ["アメリカの雨は",
     "アメージング！"],
    ["綱引きの勝負は、どろですべって",
     "ドロー！"],
    ["そりがぶつかて、",
     "アイムソーリー！"],
    ["月を見てうなった、",
     "「ム～～ン」"],
    ["これじゃ火星を見るのは、",
     "マ～ズむり！"],
    ["太陽が",
     "サンサンと輝いている"],
    ["台所は",
     "キッチンとせいりせいとん！"],
    ["マスカットを、",
     "まずカット！"],
    ["油だって日が経つと",
     "老いる(オイル)"],
    ["夏じゃなきゃ、",
     "サマー(様)になんないよ"],
    ["和尚が２人揃って、",
     "オショウガツー！！"],
    ["アリが十匹揃って",
     "「ありがとう～！」"],
    ["盲腸は",
     "もう超ツライ。"],
    ["ハサミの",
     "ギャグはさみ"],
    ["Ｎｏ！と言える",
     "ノート"],
    ["自称",
     "辞書マニア"],
    ["カサが多すぎて",
     "カサばっちゃう"],
    ["箱を",
     "ハコんだ！"],
    ["電話に",
     "誰も出んわ～"],
    ["時計は！",
     "ほっとけい"],
    ["僕さぁ",
     "ボクサーなんだ"],
    ["バスが凄いスピードで",
     "すっ飛ばす"],
    ["ライター工場で",
     "はたライター"],
    ["布団が",
     "ふっとんだっ！"],
    ["靴にガムが",
     "くっついた"],
    ["靴を脱いで",
     "くつろいだ"],
    ["下駄で",
     "笑い転げた"],
    ["ボートに乗って",
     "ボーッとする"],
    ["タイヤが当たると",
     "痛いやー。"],
    ["コロンを付けてて",
     "転んだ"],
    ["帽子で！",
     "日焼け防止"],
    ["このイス、",
     "いーっすねぇ！"],
    ["漢文は",
     "チンプンカンブンですよ"],
    ["ボスが",
     "水をこぼす"],
    ["奇怪な",
     "機械…"],
    ["銅像を",
     "どうぞ～"],
    ["内臓が",
     "無いぞう…"],
    ["魚の気持ちを",
     "サカナでしないようにね"],
    ["小判を交番に届けるのを",
     "拒んだ"],
    ["映画を",
     "観に行ってもええが?"],
    ["スキーが",
     "好き～！"],
    ["太陽出ないと",
     "冷たいよう"],
    ["月で",
     "もちつき！"],
    ["火星の",
     "家政婦！？"],
    ["岩は…",
     "なにもイワン"],
    ["池に",
     "行け！"],
    ["バレーで",
     "頑張れ～！"],
    ["鏡を見て、",
     "かがみこんだ"],
    ["窓が多いと",
     "とまどう…"],
    ["左遷だけは、",
     "させん！"],
    ["イカイヨウが",
     "いたいよう！"],
    ["うちの家内は～",
     "おっかないよ"],
    ["王子が",
     "相談に応じた"],
    ["マイルが貯まって、",
     "スマイル！"],
    ["紅葉を見に",
     "行こうよう"],
    ["メールが",
     "読めーる！"],
    ["最近はなんでもメールでさぁ、",
     "全く気が滅入るよね"],
    ["ラブレターが",
     "破られたー"],
    ["メーカーに聞かないと",
     "だめーかー"],
    ["デールが",
     "呼んでーる"],
    ["ドナルドだって、",
     "怒鳴るど～！！"],
    ["ドナルドダックが",
     "汗だっく"],
    ["イーヨーは",
     "かっこいーよー！"],
    ["プーさんが、",
     "ハチミツをミツけた"],
    ["サリーはいつも、",
     "さりー気ないよね"],
    ["ニューヨークで",
     "入浴だってさ"],
    ["隣の客はよく",
     "ギャグ言う客だ"],
    ["畑でレタスが",
     "取れたっす！"],
    ["そのつまらないギャグに、",
     "ギャグ切れだ～！?"],
    ]

# MovieHeal.py
MovieHealLaughterMisses = ("う～む…","…さむいかも。","あいたた…","イマイチ！")
MovieHealLaughterHits1= ("はははっ！","えへへっ！","ププッ…","あははっ！")
MovieHealLaughterHits2= ("わっはっは！","あっはっは！","がっはっは！")

# MovieSOS.py
MovieSOSCallHelp = "%s たすけて！"
MovieSOSWhisperHelp = "%sがバトルで助けが必要だって！"
MovieSOSObserverHelp = "たすけて！"

# MovieNPCSOS.py
MovieNPCSOSGreeting = "おまたせ%s!\n手助けするよ！"
MovieNPCSOSGoodbye = "また後で！"
MovieNPCSOSToonsHit = "ギャグがきまるよ！"
MovieNPCSOSCogsMiss = "コグはミスするよ！"
MovieNPCSOSRestockGags = "%sのギャグをチャージするよ！"
MovieNPCSOSHeal = "トゥーンアップ"
MovieNPCSOSTrap = "トラップ"
MovieNPCSOSLure = "おとり"
MovieNPCSOSSound = "サウンド"
MovieNPCSOSThrow = "なげる"
MovieNPCSOSSquirt = "みずでっぽう"
MovieNPCSOSDrop = "ドロップ"
MovieNPCSOSAll = "すべて"

# MoviePetSOS.py
MoviePetSOSTrickFail = "あ～あ！"
MoviePetSOSTrickSucceedBoy = "よくやったね！"
MoviePetSOSTrickSucceedGirl = "いいこ、いいこ！"

# MovieSuitAttacks.py
MovieSuitCancelled = "中止\n中止\n中止"

# RewardPanel.py
RewardPanelToonTasks = "トゥーン・タスク"
RewardPanelItems = "とりかえしたアイテム"
RewardPanelMissedItems = "まだとりかえしていないアイテム"
RewardPanelQuestLabel = "クエスト：%s"
RewardPanelCongratsStrings = ["やったね！", "おめでとう！", "いいかんじ！",
                              "よくやったね！", "サイコー！", "かっこいいよ！"]
RewardPanelNewGag = "%(avName)sに新しいギャグ、\n%(gagName)sのごほうび！"
RewardPanelUberGag = "%(avName)sは %(gagName)sのギャグを%(exp)sのけいけんちでゲット!"
RewardPanelEndTrack = "やったね! %(avName)sは%(gagName)sのギャグを全部ゲットしたよ!"
RewardPanelMeritsMaxed = "まんたん"
RewardPanelMeritBarLabels = [ "カイコツウチ", "ショーカンジョー", "コグドル", "メリット" ] #▲あとで要チェック★★★★★★★★★★★★★★★★★★★★★
RewardPanelMeritAlert = "格上げの準備ＯＫ！"

RewardPanelCogPart = "コグ変装グッズをゲット！"
RewardPanelPromotion = "%sトラックで\n格上げ準備オーケー！"

# Cheesy effect descriptions: (short desc, sentence desc)
CheesyEffectDescriptions = [
    ("ノーマル・トゥーン", "ふつうのトゥーンです。"),
    ("ビッグ・ヘッド", "頭が大きくなります。"),
    ("スモール・ヘッド", "頭が小さくなります。"),
    ("ビッグ・レッグ", "がっしりとした足になります。"),
    ("スモール・レッグ", "ほそい足になります。"),
    ("ビッグ・トゥーン", "からだが少しおおきくなります。"),
    ("スモール・トゥーン", "からだが少しちいさくなります。"),
    ("ぺらぺらポートレート", "からだが平べったくなります。"),
    ("ぺらぺらプロフィール", "かおが平べったくになります。"),
    ("クリア", "ガラスのようにとうめいになります"),
    ("ノーカラー", "無色になります"),
    ("とうめい", "他の人から見えなくなります"),
    ]
CheesyEffectIndefinite = "他のエフェクトを選択するまで、%(whileIn)s%(effectName)s"
CheesyEffectMinutes = "あと%(time)s分間、%(whileIn)s%(effectName)s"
CheesyEffectHours = "あと%(time)s時間、%(whileIn)s%(effectName)s"
CheesyEffectDays = "あと%(time)s日間、%(whileIn)s%(effectName)s"
CheesyEffectWhileYouAreIn = "%sにいる間だけ"
CheesyEffectExceptIn = "%s以外で"


# SuitBattleGlobals.py
SuitFlunky = "オベッカー"
SuitPencilPusher = "カリカリン"
SuitYesman = "イエスマン"
SuitMicromanager = "ガミガミーナ"
SuitDownsizer = "リストラマン"
SuitHeadHunter = "ヘッドハンター"
SuitCorporateRaider = "デッパラーダ"
SuitTheBigCheese = "ビッグチーズ"
SuitColdCaller = "ブアイソン"
SuitTelemarketer = "ツーハーン"
SuitNameDropper = "タッシャーナ"
SuitGladHander = "オオゲーサ"
SuitMoverShaker = "クロマクール"
SuitTwoFace = "アイソマン"
SuitTheMingler = "オマカセンヌ"
SuitMrHollywood = "ビッグスマイル"
SuitShortChange = "チョロマカシー"
SuitPennyPincher = "セコビッチ"
SuitTightwad = "ドケッチオ"
SuitBeanCounter = "カッチリン"
SuitNumberCruncher = "スウジスキー"
SuitMoneyBags = "カネモッチン"
SuitLoanShark = "シャークロン"
SuitRobberBaron = "ドロビッグ"
SuitBottomFeeder = "タイコモチー"
SuitBloodsucker = "ガッツキー"
SuitDoubleTalker = "ニマイジタン"
SuitAmbulanceChaser = "ツケコミン"
SuitBackStabber = "ウラギリン"
SuitSpinDoctor = "ドクター・\nトラブル"
SuitLegalEagle = "ホウノトリ"
SuitBigWig = "ビッグホワイト"

# Singular versions (indefinite article)
SuitFlunkyS = "オベッカー"
SuitPencilPusherS = "カリカリン"
SuitYesmanS = "イエスマン"
SuitMicromanagerS = "ガミガミーナ"
SuitDownsizerS = "リストラマン"
SuitHeadHunterS = "ヘッドハンター"
SuitCorporateRaiderS = "デッパラーダ"
SuitTheBigCheeseS = "ビッグチーズ"
SuitColdCallerS = "ブアイソン"
SuitTelemarketerS = "ツーハーン"
SuitNameDropperS = "タッシャーナ"
SuitGladHanderS = "オオゲーサ"
SuitMoverShakerS = "クロマクール"
SuitTwoFaceS = "アイソマン"
SuitTheMinglerS = "オマカセンヌ"
SuitMrHollywoodS = "ビッグスマイル"
SuitShortChangeS = "チョロマカシー"
SuitPennyPincherS = "セコビッチ"
SuitTightwadS = "ドケッチオ"
SuitBeanCounterS = "カッチリン"
SuitNumberCruncherS = "スウジスキー"
SuitMoneyBagsS = "カネモッチン"
SuitLoanSharkS = "シャークロン"
SuitRobberBaronS = "ドロビッグ"
SuitBottomFeederS = "タイコモチー"
SuitBloodsuckerS = "ガッツキー"
SuitDoubleTalkerS = "ニマイジタン"
SuitAmbulanceChaserS = "ツケコミン"
SuitBackStabberS = "ウラギリン"
SuitSpinDoctorS = "ドクター・トラブル"
SuitLegalEagleS = "ホウノトリ"
SuitBigWigS = "ビッグホワイト"

# Plural versions
SuitFlunkyP = "オベッカー"
SuitPencilPusherP = "カリカリン"
SuitYesmanP = "イエスマン"
SuitMicromanagerP = "ガミガミーナ"
SuitDownsizerP = "リストラマン"
SuitHeadHunterP = "ヘッドハンター"
SuitCorporateRaiderP = "デッパラーダ"
SuitTheBigCheeseP = "ビッグチーズ"
SuitColdCallerP = "ブアイソン"
SuitTelemarketerP = "ツーハーン"
SuitNameDropperP = "タッシャーナ"
SuitGladHanderP = "オオゲーサ"
SuitMoverShakerP = "クロマクール"
SuitTwoFaceP = "アイソマン"
SuitTheMinglerP = "オマカセンヌ"
SuitMrHollywoodP = "ビッグスマイル"
SuitShortChangeP = "チョロマカシー"
SuitPennyPincherP = "セコビッチ"
SuitTightwadP = "ドケッチオ"
SuitBeanCounterP = "カッチリン"
SuitNumberCruncherP = "スウジスキー"
SuitMoneyBagsP = "カネモッチン"
SuitLoanSharkP = "シャークロン"
SuitRobberBaronP = "ドロビッグ"
SuitBottomFeederP = "タイコモチー"
SuitBloodsuckerP = "ガッツキー"
SuitDoubleTalkerP = "ニマイジタン"
SuitAmbulanceChaserP = "ツケコミン"
SuitBackStabberP = "ウラギリン"
SuitSpinDoctorP = "ドクター・トラブル"
SuitLegalEagleP = "ホウノトリ"
SuitBigWigP = "ビッグホワイト"

SuitFaceOffDefaultTaunts = ['ワッ！']

SuitAttackDefaultTaunts = ['これでもくらえ！', '私の前から消えろ！']

SuitAttackNames = {
  'Audit' : 'カンサ！',
  'Bite' : 'ガブット！',
  'BounceCheck' : 'フワタリコギッテ！',
  'BrainStorm' : 'ブレインストーム！',
  'BuzzWord' : 'リュウコウゴ！',
  'Calculate' : 'ケイサン！',
  'Canned' : 'カンヅメ！',
  'Chomp' : 'ムシャムシャ！',
  'CigarSmoke' : 'ハマキ！',
  'ClipOnTie' : 'クリップネクタイ！',
  'Crunch' : 'キンユウキキ！',
  'Demotion' : 'コウカク！',
  'Downsize' : 'シュクショウ！',
  'DoubleTalk' : 'オセジ！',
  'EvictionNotice' : 'オイタテツウチ！',
  'EvilEye' : 'コワイシセン！',
  'Filibuster' : 'ボウガイ！',
  'FillWithLead' : 'エンピツゼメ！',
  'FiveOClockShadow' : "ブショウヒゲ！",
  'FingerWag' : 'チッチッ！',
  'Fired' : 'ヒノクルマ！',
  'FloodTheMarket' : 'シジョウハンラン！',
  'FountainPen' : 'マンネンヒツ！',
  'FreezeAssets' : 'オサムイフトコロ！',
  'Gavel' : 'コヅチ！',
  'GlowerPower' : 'スルドイシセン！',
  'GuiltTrip' : 'ザイアクカン！',
  'HalfWindsor' : 'ハーフウィンザー！',
  'HangUp' : 'ガチャギリ！',
  'HeadShrink' : 'マメアタマ！',
  'HotAir' : 'ネップウ！',
  'Jargon' : 'センモンヨウゴ！',
  'Legalese' : 'ホウリツヨウゴ！',
  'Liquidate' : 'ミズノアワ',
  'MarketCrash' : 'ケイザイシンブン！',
  'MumboJumbo' : 'ミツダン！',
  'ParadigmShift' : 'パラダイムシフト！',
  'PeckingOrder' : 'ピーチクパーチク！',
  'PickPocket' : 'スティール！',
  'PinkSlip' : 'カイコツウチ！',
  'PlayHardball' : 'チョッキュウショウブ！',
  'PoundKey' : 'シャープキー！',
  'PowerTie' : 'チョウネクタイ！',
  'PowerTrip' : 'ショッケンランヨウ！',
  'Quake' : 'ジシン！',
  'RazzleDazzle' : 'ビジネススマイル！',
  'RedTape' : 'ガンジガラメ！',
  'ReOrg' : 'サイヘンセイ！',
  'RestrainingOrder' : 'キンシメイレイ！',
  'Rolodex' : 'ローロデックス！',
  'RubberStamp' : 'ハンコ！',
  'RubOut' : 'ナカッタコトニ！',
  'Sacked' : 'フクロヅメ！',
  'SandTrap' : 'ドロヌマ！',
  'Schmooze' : 'ホメゴロシ！',
  'Shake' : 'シェイク！',
  'Shred' : 'シュレッダー！',
  'SongAndDance' : 'ウタッテオドッテ！',
  'Spin' : 'スピン！',
  'Synergy' : 'シナジー！',
  'Tabulate' : 'データサクセイ！',
  'TeeOff' : 'セッタイゴルフ！',
  'ThrowBook' : 'ロッポウゼンショ！',
  'Tremor' : 'シンドウ',
  'Watercooler' : 'ウォータークーラー！',
  'Withdrawal' : 'ザンダカショウカイ！',
  'WriteOff' : 'チョウケシ！',
  }

SuitAttackTaunts = {
    'Audit': ["帳簿と数字が合っていませんよ～",
              "おやおや、 赤字ですか？",
              "帳簿なら私におまかせを。",
              "負債が大きすぎるんじゃないですか～？",
              "まずあなたの資産を見てみましょうか？",
              "負債というものがなんだか知っていますか？",
              "さーて、 あなたの負債は？",
              "口座をスッカラカンにしてやる！",
              "ムダ遣いは いけませんねぇ。",
              "おや、帳簿にミスがありますよ。",
              ],
    'Bite': ["かまれるのは好きかい？",
             "こいつにかまれると痛いよ！",
             "がっつくのは良くありませんよ。",
             "行くよ、ガブガブアタック！",
             "これでも食らいな！",
             "気をつけな、ボットだってかむんだぜ。",
             "ガブっといってやる！",
             "腹へったな～！",
             "今日はおながペコペコだ！",
             "一口だけでも食わせてくれよ。",
             ],
    'BounceCheck': ["こぎって小切手？",
                    "お支払いの徴収に参りました。",
                    "この小切手はあなたのですね？",
                    "あなた、私に借りがあるんですよ。",
                    "借金の徴収に来ましたよ。",
                    "この小切手、使えませんよ。",
                    "罰金です！",
                    "あなたに払いきれますかねぇ。",
                    "これは高くつきますよ。",
                    "これを現金化したいんです。",
                    "小切手を使うなんて、なまいきな！",
                    "手切れ金のつもりかな？",
                    "このサービス料は高くつくよ。",
                    ],
    'BrainStorm':["今日の予報：大雨！",
                  "カサは持ってきましたか？",
                  "ピカッとひとつ来そうだ！",
                  "ひと降りきたみたいだな。",
                  "落雷注意報だ！",
                  "雲行きが怪しくなってきたよ。",
                  "いいこと思いついたぞ！",
                  "電光石火とはこのことだ！",
                  "濡れるのはお好きかい？",
                  ],
    'BuzzWord':["この言葉を知ってるかな？",
                "最新の流行語を聞いた？",
                "さすがのキミもこれは知らんだろう。",
                "キミ、遅れてるよ～。",
                "耳をちょっと貸しなさい。",
                "情報収集はちゃんとやらねば！",
                "そんなんじゃ付いていけないよ？",
                "遅れてるキミに情報のプレゼントだ！",
                "これぐらい知ってなきゃダメだよ。",
                "キミ、これぐらい知ってなきゃ～",
                ],
    'Calculate': ["総額が大変なことになってますね。",
                  "ちゃんと計算しないとダメですよ。",
                  "数字をバカにしちゃいけませんね。",
                  "計算のひとつも出来ないようじゃダメだよ。",
                  "使ったお金はちゃんと記録したかい？",
                  "私の計算によれば…キミはもうおしまいだ！",
                  "これがあなたの負債総額です！",
                  "おやおや、ちょっと浪費しすぎなんじゃない？",
                  "数字遊びはお好きかい？",
                  Cogs + "＝∞ トゥーン＝０",
                  ],
    'Canned': ["カンヅメは好き？",
               "どっ「カーン」！",
               "私は生よりカンヅメが好きなのだよ。",
               "カンヅメにされたことはあるかい？",
               "このカンをキミにプレゼントだ！",
               "カンケリゲームのスタートだ！",
               "カンカンカン！",
               "まるくてかたくてつめたいもの、なーんだ？",
               "カンヅメ作業は得意だぜ。",
               "キミはカンヅメにしてもまずそうだねぇ。",
               ],
    'Chomp': ["どうだ、このりっぱな歯！",
              "ムシャムシャムシャ！",
              "食べるときはゴーカイに！",
              "いただきまーす！",
              "これでも食らえ！",
              "キミが私のディナーさ！",
              "トゥーンは私の大好物さ！",
              ],
    'ClipOnTie': ["正装こそ、できる人間のたしなみさ。",
                  "勝負の場ではネクタイをつけなきゃね。",
                  "おしゃれな" + Cogs + "にネクタイは不可欠！",
                  "これでも試しに着けてみな。",
                  "サクセスストーリーは一本のネクタイから。",
                  "ネクタイなしじゃみっともないよ。",
                  "これをつけるのを手伝ってあげるよ。",
                  "ネクタイと書いて権力と読むのさ！",
                  "さて、キミにはこのサイズかな？",
                  "おやおや、これじゃ首がしまってしまうね。",
                  "その格好、ラフすぎるね。",
                  "ネクタイでクタクタにしてやる！",
                  ],
    'Crunch': ["キミ、危なっかしいなぁ。",
               "金融危機の波が来る！",
               "札束の味は苦い味！",
               "危機がきた！",
               "これを生き残れるかな？",
               "これでキミも一文無しだ！",
               "備えあれば憂いなし！",
               "キミは危機に強いほうかい？",
               "キミのお先は真っ暗さ！"
               ],
    'Demotion': ["一直線に下っ端行きだ！",
                 "キミには日のよく当たる席を用意したよ。",
                 "威張れる肩書きもなくなったね。",
                 "キミを蹴落としてみせる！",
                 "おやおや、 行き詰まりかい？",
                 "あっという間に行き場なし！",
                 "キミの人生、 行き止まりさ！",
                 "しばらくそこであがいてなさい。",
                 "運も才能のうちってやつさ。",
                 "キミの履歴書、見ていて恥ずかしいよ。",
                 ],
    'Downsize': ["ちっちゃくなーれ。",
                 "くらえ、 縮小ショック！",
                 "これ、英語ではダウンサイズっていうんだよ。",
                 "見苦しいなぁ、ちょっと小さくなってくれ。",
                 "キミ、ちょっと態度が大きいんじゃないかい？",
                 "目障りだなぁ…",
                 "私はちっちゃい人間を見下すのがだーいすき！",
                 "おやゆび姫って聞いたことある？",
                 "お客様、５０円増しでＳサイズにできますが？",
                 "私はちいさい人が好きなんだよね。",
                 "もっと小さくすることだってできるんだよ？",
                 "このアタックの対象はフリーサイズだ！",
                 ],
    # Hmmm - where is double talker?
    'EvictionNotice': ["はいはい、どいたどいた！",
                       "あんたの肩書きにさようなら、だ！",
                       "そろそろ安アパートに引越しだ。",
                       "クビにならなかっただけマシだよ。",
                       "まったく…キミにはこれしかないみたいだね。",
                       "キミにこれをつきつけるのは心苦しいなぁ。",
                       "出直してきな！",
                       "そろそろキミにもさよならだ。",
                       "キミの居場所はもうないよ。",
                       "左遷だ！",
                       "今のキミはギリギリの状態にあるんだよ？",
                       ],
    'EvilEye': ["悪い子には大目玉くらわせるぞ！",
                "私の目が黒いうちは好きにさせん！",
                "ああ、何かが眼に入ってしまったようだ。",
                "私はキミに眼を付けていたのさ！",
                "眼力なら負けないぞ！",
                "私はコワいものが大好き！",
                "キミはどこに目がついてるんだ？",
                "あなたは私がコワくなーる、コワくなーる。",
                "「台風の目」に巻き込んでやる！",
                "あー、眼がゴロゴロしてきた。",
                ],
    'Filibuster':["ボーガイボーガイ！てっていそしだ！",
                  "こうなったら牛歩だ！",
                  "私は妨害がだーいすきなんだ。",
                  "キミの進路を妨害してやる！",
                  "どんな手を使ってでも妨害する！",
                  "しゃべってしゃべって邪魔してやる！",
                  "このヤジに耐えられるかな？",
                  "あげあし取りならまかせろ！",
                  "口げんかなら負けないぞ！",
                  "妨害なら私にまかせなさい。",
                  ],
    'FingerWag': ["ふん、まだまだだな。",
                  "ちょっとキミ、そこに座りなさい。",
                  "笑わせてくれるねえ、まったく。",
                  "この私を怒らせるなよ。",
                  "何度も同じ事を言わせるな！",
                  "人の話は聞くものだよ。",
                  "キミ、われわれ" + Cogs + "に対して失礼なんじゃないかい？",
                  "そろそろ私の言うことに耳を傾けなさい。",
                  "ペラペラペラペラ…よくしゃべるね、まったく。",
                  "そんな考えは通用しないよ。",
                  "だからキミは半人前なんだよ。",
                  "まったく、未熟者だねぇ。",
                  ],
    'Fired': ["バーベキューは好きかい？",
              "私は熱いほうが好きなんだよ。",
              "ちょっと寒くないかい？",
              "ファイヤーーー！",
              "ホット！ホット！",
              "ホットでジューシーに仕上げてやるよ。",
              "ジュッとコゲちゃえ！",
              "焼きかげんはウェルダンで？",
              "燃え尽きちゃった？",
              "日焼け止めは塗ったかい？",
              "コンガリ焼いてやる！",
              "ハデに炎上と行こうぜ！",
              "灰になれ！",
              "キミ、けっこう熱いね。",
              "頭から火が出そうだよ。",
              "ここは強火で行ってみよう！",
              "コンガリトゥーン、いっちょあがり！",
              "ナマ焼けは身体によくないよ。",
              ],
    'FountainPen': ["シミ抜きの準備はいいかい？",
                    "私のペンは書き味ばつぐん！",
                    "このシミは絶対抜けないよ～",
                    "失礼、インクの出が悪いようだ。",
                    "着替えは持ってきたかい？",
                    "えーと、どこにサインしたらいいのかな？",
                    "ほら、私のペンをお使いなさい。",
                    "私の字、読めるかな？",
                    "書き味はどうかな？",
                    "「万年」ヒラにはこれがお似合いさ！",
                    "おっと、インクを入れすぎちゃったようだ。",
                    ],
    'FreezeAssets': ["ふところが寒いようだねぇ。",
                     "なんだか寒くないかい？",
                     "私はぬくぬく、キミは寒々。",
                     "景気が冷え込んでますね。",
                     "お寒い世の中ですな。",
                     "世間の風は冷たいもんだよ。",
                     "景気も人も冷えきってるね。",
                     "こう見えて私はけっこうクールなのさ。",
                     "これで凍えてしまいなさい。",
                     "凍傷ってなんだか知ってるかい？",
                     "寒さで震えあがっちゃうね。",
                     "私はいわゆる「冷」血漢らしいんだよ。",
                     ],
    'GlowerPower': ["なにガンくれてやがんでぇ。",
                    "私の視線は鋭いらしい。",
                    "突き刺すような視線ってこういうことさ。",
                    "私のチャームポイントはこの目！",
                    "チラっと見じゃものたりないな。",
                    "ごらん、表情豊かな目だろ？",
                    "何見てんだよ！",
                    "見～～た～～な～～～",
                    "あっかんべー！",
                    "私の目をよーく見てみなさい。",
                    "あなたの未来が見える…それは絶望！",
                    ],
    'GuiltTrip': ["謝るまでせめ続けてやる！",
                  "ほんとに悪いトゥーンだね！",
                  "全部キミのせいだ！",
                  "まったく、キミときたらいつもいつも…",
                  "キミには罪の意識ってものがないのかい？",
                  "キミなんて嫌いだ、もう話さない！",
                  "「ごめん」と一言言ったらどうなんだ？",
                  "百年経ってもキミのことは許さないよ！",
                  "泣いて謝ってもダメだからね。",
                  "キミはひどいトゥーンだね。",
                  "キミはもっとできると思ってたよ。",
                  ],
    'HalfWindsor': ["こんなハデなネクタイ、見たことないだろう？",
                    "ハイハイ、巻きこまれすぎないようにね。",
                    "しめつけちゃうよ！",
                    "ネクタイのしめかたも知らないのか？",
                    "キミにこのネクタイを買う金はないだろうな。",
                    "トゥーンもたまにはネクタイをしてみなさい。",
                    "キミにはもったいない気もするが…",
                    "まったく、キミ相手に使うことになるとはね。",
                    "キミにはちょっと早すぎるかな。",
                  ],
    'HangUp': ["接続が切れました！",
               "バイバイ！",
               "そろそろキミとのつながりを切ろうかな。",
               "もう電話してこないで！",
               "ガチャン！",
               "キミと話すことはもうない！",
               "私の時間のムダだ！",
               "はい、さよーなら！",
               "ん？接続が弱いみたいだね？",
               "ハイ、時間切れでーす。",
               "ハッキリ聞こえるようにしてやろう。",
               "間違い電話です！",
               ],
    'HeadShrink': ["よくも私の顔をつぶしてくれたな！",
                   "ミクロキッズならぬミクロトゥーンだ！",
                   "プライドも一緒にちっちゃくなるか？",
                   "せんたくしたらいつもこうなるの？",
                   "「わがはいは縮小されている。名前はもうない」",
                   "大きいのは図体だけか！",
                   "キミ、頭がどうかしちゃってるんじゃないか？",
                   "考えが足りないのはいけないよ。",
                   "キミはスケールの小さいトゥーンだね。",
                   "トゥーンは小さければ小さいほどいいんだってよ？",
                   ],
    'HotAir':["だんだん議論が過熱してまいりました！",
              "あー、あついあつい。",
              "沸点を迎えそうだ！",
              "くらえ、熱風！",
              "熱く語り合おうじゃないか。",
              "火がないところに煙はたたないってよ？",
              "ヒートアップしてきたね。",
              "思ったよりアツいヤツだな。",
              "私の怒りに火を注いだね？",
              "私はこの仕事に燃えてるんだ！",
              "トゥーン相手にはつい熱くなってしまうな。",
              "ゴミは燃やさなきゃね。",
              ],
    'Jargon':["キミ、こんなことも知らないのかい。",
              "私はその道のプロなんだよ。",
              "プロがしゃべるとこうなる！",
              "わからずやには言い聞かせてやる！",
              "私は自己主張がはげしいらしいんだが…",
              "私にヘタな言い訳は通用しないよ。",
              "ま、キミにはわからないだろうけどね。",
              "ほら、言葉で人は傷つくんだよ。",
              "私の言いたいこと、理解できるかな？",
              "言葉の戦いなら負けん！",
              ],
    'Legalese':["無駄な抵抗はおやめなさい。",
                "法律上、あなたは負けるのです。",
                "規約をよくお読みになりましたか？",
                "キミは法の下に管理されている！",
                "キミを罰する法律があったはずだ。",
                "私に過失はない！",
                "この攻撃にて見られる表現はディズニー・トゥーンタウン・オンラインの意見ではありません。",
                "この攻撃で生じたダメージに関して、当社は一切の責任を持たないものとします。",
                "この攻撃による結果は抽選で決定させていただきます。",
                "この攻撃は当社指定の場所以外では無効です。",
                "キミの行いは認めるわけにはいかない！",
                "法律ごとを知らんお前には負けない！",
                ],
    'Liquidate':["今回の件はお流れですな。",
                 "時代の流れが読めないとおぼれますよ。",
                 "水に流してしまいますよ。",
                 "ムダな努力を…！",
                 "おおっと危ない、濡れちまうよ。",
                 "気をつけていないと呑まれるよ。",
                 "きれいさっぱり流れてしまえ。",
                 "沈んでしまえ！",
                 "ではスッキリ水に流しましょうかね。",
                 "ムダな努力はやめておきなさい。",
                 ],
    'MarketCrash':["情報収集はこまめにやらねば！",
                   "この重さに耐えられるかな？",
                   "新聞くらい毎日読まなきゃダメじゃないか。",
                   "これは大事件だ！",
                   "せめてこれぐらいは読んでおけ！",
                   "売りに出たほうがいいらしいぞ！",
                   "私のコラムも読みたまえ！",
                   "ほれ、一年分だ。",
                   "これはキミの専門外かな？",
                   "テレビ欄以外もちゃんと読みなさい。",
                   "今日の４コマ、おもしろいぞ！",
                   ],
    'MumboJumbo':["ごにょごにょごにょ…",
                  "ひそひそひそ…",
                  "もにょもにょもにょ…",
                  "もごもごもご…",
                  "こしょこしょこしょ…",
                  "むにゃむにゃむにゃ…",
                  "ぼそぼそぼそ…",
                  "もそもそもそ…",
                  "こそこそこそ…",
                  "…というわけでひとつよろしくお願いしますよ。",
                   ],
    'ParadigmShift':["時空のシフトを引き起こすぞ！",
                     "異世界への旅へご案内しますぞ！",
                     "ふむ、おもしろいパラダイムだ。",
                     "キミの知らない世界へつれていってあげよう。",
                     "行ってらっしゃーい！",
                     "こんな世界があるって知ってたかい？",
                     "これは生まれて始めてかな？",
                     "さあ、行った行った！",
                     "この世界にキミの居場所はないんだよ。",
                     ],
    'PeckingOrder':["小鳥たちよ、おいで！",
                    "鳥たちと和むのもたまには必要だよ。",
                    "みんな、かかれー！",
                    "幸せの青い鳥につつかれたい？",
                    "騒いでごまかすのもひとつの方法さ。",
                    "落し物に注意！",
                    "議会ではたまにこのくらいうるさくなるんだよ。",
                    "ピーピー！ピーチクパーチク！",
                    "一石二鳥を狙うならこいつらはどうだ？",
                    ],
    'PickPocket': ["いただき！",
                   "おっ、ちょっとアレ見てみなよ。",
                   "ちょろいもんだ。",
                   "重いだろ？持つのを手伝ってあげよう。",
                   "私は手が早いので有名なんだ。",
                   "私は手ぐせが悪くてね。",
                   "脇が甘い！",
                   "無用心だなぁ。",
                   "なくし物には気をつけな。",
                   "キミのモノは私のモノ！",
                   "おっ、いいもの持ってるじゃないか。",
                   "サンキュー！",
                   "ちょっと失礼。",
                   "これ、どうせいらないだろう？",
                   ],
    'PinkSlip': ["おおっと、ついに来たか！",
                 "だから言わんこっちゃない。",
                 "元気でな！",
                 "これで二度と会うことはないだろうな。",
                 "残念だったね。",
                 "気を落とすなよ。",
                 "これでキミも終わりだな。",
                 "人生どこで転ぶかわからないものだね。",
                 "さよ～なら～～",
                 "キミの運もつきたってことさ。",
                 ],
    'PlayHardball': ["ではストレートに言おう！",
                     "直球勝負なら負けん！",
                     "バッターアップ！",
                     "ねらうならど真ん中！",
                     "ピッチャー、投げました！",
                     "リリーフピッチャーが必要なんじゃないか？",
                     "打ち取ってやるさ。",
                     "真っ向勝負といこうじゃないか。",
                     "２アウト２ストライク！もう後はない！",
                     "キミなんかに変化球はもったいないね。",
                     "何事もストレートに！",
                     "私はまがったことが嫌いなんだ。",
                    ],
    'PoundKey': ["これがキミへの伝言だ！",
                 "コレクトコールをかけたいんだが～",
                 "おっ、キミにいたずら電話だぞ。",
                 "私はなんでもシャープなものが好きなのさ。",
                 "このシャープさは痛いかもな。",
                 "メッセージは一件あります。",
                 "キーはたたくものなんだよ！",
                 "こんな攻撃、見たことないだろ？",
                 "サイゴニ「＃」ヲオシテクダサイ。",
                 "電話代はちゃんと払ってるかい？",
                 ],
    'PowerTie': ["蝶々はお好きかな？",
                 "チョーいいネクタイでしょう、これ。",
                 "おしゃれな" + Cogs + "に蝶ネクタイは不可欠！",
                 "これでも試しに着けてみな。",
                 "サクセスストーリーは一本のネクタイから…",
                 "ネクタイなしじゃみっともないよ。",
                 "これをつけるのを手伝ってあげるよ。",
                 "ネクタイと書いて権力と読む！",
                 "さて、キミにはこの色かな？",
                 "こいつみたいにねじまげてやる！",
                 ],
    'PowerTrip': ["とばされたいのか？",
                  "遠いところはお好きかな？",
                  "弱肉強食だよ。",
                  "トゥーンは私に勝てんよ。",
                  "権力の前にひれ伏せ！",
                  "それ、接待費で落とすから。",
                  "逆らったら左遷だぞ！",
                  "チカラを持っているのは私なんだよ。",
                  "逆らうのか？",
                  "私に逆らったらあとがコワいぞ～",
                  "身の程知らずなトゥーンだね。",
                  ],
    'Quake': ["グラグラっとくる時のこの興奮！たまらんね。",
              "こんな地震は初めてかい？",
              "キミを見てるとぐらっと来るよ。",
              "おや、これはキミが震えてるのかい？",
              "こりゃいったい震度いくつだろ？",
              "すべてを揺るがしてやる！",
              "立っていられるかな？",
              "これでもまだ耐えるっていうのか？",
              "足元からくずしてやる！",
              ],
    'RazzleDazzle': ["私の唇の動きをよーく読んで。",
                     "カチカチカチ！",
                     "やっぱり私の歯、最高にかっこいいよね。",
                     "これを見て驚くなよ～",
                     "やっぱり歯がきれいじゃないとね～",
                     "え、きれいすぎてまぶしい？",
                     "これが本物だなんて信じられないでしょう。",
                     "びっくりした？",
                     "どうだ、強くてたくましいこの歯！",
                     "毎食後の歯磨きがひけつさ！",
                     "はい、笑って笑って～！",
                     ],
    'RedTape': ["決まりは決まり。言うことを聞け！",
                "規則でがんじがらめにしてやる。",
                "しばらく静かになってもらおう。",
                "これから抜け出せるかな？",
                "べたべたなシチュエーションかも知れないね。",
                "閉所恐怖症だって？そいつは好都合だ。",
                "刃向かえるものなら刃向かってみろ。",
                "しばりつけてやる。",
                "ほどけるもんならほどいてみな。",
                "手も足も出まい！",
                ],
    'ReOrg': ["散らかっているのが嫌いでね。",
              "このまちはトゥーンだらけで整理が必要だ。",
              "ちょっと身の回りを整頓してみたらどうだ。",
              "キミのようなゴミが嫌いなんだよ。",
              "手始めにキミから整頓しよう。",
              "身辺整理をしてみたら？",
              "まったく、トゥーンばかりごちゃごちゃと…",
              "年に一度の大掃除だ！",
              "キミ、ジャマなんだよ。",
              "まずはキミから掃除してやる！",
              ],
    'RestrainingOrder': ["私を傷つける行為は禁止！",
                         "やっていい事とわるい事があるだろう！",
                         "私の３メートル以内に近づくことを禁止する！",
                         "距離を保ちなさい。",
                         "命令だ！",
                         Cogs + "！そのトゥーンを捕まえなさい！",
                         "あれもこれも、それもしちゃダメ！",
                         "禁止！",
                         "これには逆らえまい！",
                         "トゥーンはおとなしくしていなさい！",
                         "だめ！"
                         ],
    'Rolodex': ["キミの名刺、このへんに入ってたんだが…",
                "よろしくお願いいたします。",
                "ほれ、私の名刺だ。",
                "私はこういうモノだが。",
                "はじめまして！",
                "今後もよろしくお見知りおきを。",
                "どーも、どーも。",
                "こいつらは切れ味するどいよ。",
                "何かあったらいつでもこちらへどうぞ。",
                "私の顔を知らないとは！",
                "キミ、名刺すら持ってないのかい。",
                ],
    'RubberStamp': ["どこに押せばいいのかな？",
                    "ハイハイ、どんどん書類持ってきて～",
                    "認め印でいい？",
                    "「たいへんよくできました」",
                    "「もっとがんばりましょう」",
                    "「あとすこしです」",
                    "「ふつうです」",
                    "「よくできました」",
                    "特別に押してやろう！",
                    "ポンポンっとな。",
                    ],
    'RubOut': ["おおっと、間違いまちがい。",
               "んん？どこ行った？",
               "間違いは誰にでもあるものだよ。",
               "私の邪魔になるものは消す！",
               "間違いはすぐに消す主義なんだ。",
               "キミの存在を消しちゃうよ。",
               "ゴミはいらないんだよ。",
               "消えてなくなれ！",
               "あれ、さっきは姿が見えたのに…まぁいいか。",
               "フェードアウトってやつ？",
               "問題解決にはこれがいちばん！",
               "おっと、しまったしまった。",
               ],
    'Sacked':["さーて、どこに送ってやろうか。",
              "リボンもつけてやろうか。",
              "袋だたきにしてやる。",
              "ビニール袋と紙袋、どっちがいい？",
              "私の前から消えなさい！",
              "二度とその顔を見せるな！",
              "キミのことはもう要らんのさ。",
              "キミにもう用はないのさ、達者でな！",
              "たしか明日がゴミの日だったな。",
              "うーむ、これって生ゴミになるのかな。",
              ],
    'Schmooze':["ああ、キミはトゥーンの鑑だ！",
                "キミ、本当にサイコー！",
                "あなたにお会いできて光栄です～！",
                "まったくキミは素晴らしい！",
                "すごいねキミ、いやホント！",
                "いやはや、恐れいりました～！",
                "いやいや、あなたにはかないませんよ！",
                "いや、まったくもってうらやましいですな！",
                "あなたのお噂はかねがね！",
                "感激のあまり涙がとまりませ～ん！",
                "ああ、神様トゥーン様！",
                ],
    'Shake': ["シェイクする時のこの興奮！最高だね。",
              "こんなシェイクは初めてかい？",
              "キミを見てるとぐらっと来るよ。",
              "おや、これはキミが震えてるのかい？",
              "こりゃいったい震度いくつだろ？",
              "すべてをシェイクしてやる！",
              "立っていられるかな？",
              "これでもまだ耐えるっていうのか？",
              "足元からくずしてやる！",
              "シェイクシェイク！",
              "私はシェイクが大好きでね。",
              "ちょっと体重が増えたみたいだな。",
              ],
    'Shred': ["こいつは極秘資料だからね。",
              "キミに見られるわけにはいかないんだ。",
              "処分しなくては。",
              "見たな！？",
              "証拠インメツだ！",
              "もみ消しは手際が大事なんだよ。",
              "キミのアイデア、使えないね～",
              "コマギレにしてやる！",
              "キミみたいなのが外に漏れるわけにはいかないんだ。",
              "シュレッドしたらリサイクル。",
              "「社外秘」",
              ],
    'Spin': ["グルグル～～",
             "まったく、目が回るようじゃないか！",
             "回れ回れ～～",
             "え、何？回りたい？",
             "バレリーナも真っ青だな！",
             "さあ、何回まわれるかな？",
             "もう首がまわらないんじゃないか？",
             "おお、コマのようだな。",
             "いつもより多く回しております。",
             ],
    'Synergy': ["役員会に連れて行く。",
                "キミのプロジェクトは 中止だ。",
                "キミの予算は カットされたよ。",
                "キミのチームは 他チームに吸収だ。",
                "賛成多数で キミの降格が決定した。",
                "組織とは シビアなものなんだよ。",
                "チームにとってのガンは早めに取り除かんと。",
                "まあ、これについては また後日。",
                "残念ながらキミの チカラにはなれないよ。",
                "多少の犠牲は やむを得んだろうな。",
                ],
    'Tabulate': ["おや、計算が合わないな。",
                 "計算上、キミは負ける。",
                 "こんなデータ、見たことない！",
                 "今キミのデータを計測中だ。",
                 "データを見てみるかい？",
                 "損得勘定は大事だよ。",
                 "データ命！",
                 "私は計算しなくては気が済まないんだ。",
                 "出たぞ、計測結果は…。",
                 "ふむ、素晴らしいデータだ。",
                 ],
    'TeeOff': ["いやいや、今日は天気もいいですなぁ。",
               "ファ～～～～！",
               "ナイスショット！",
               "キャディーさん、１番アイアン！",
               "ハザードは避けなきゃな…",
               "よっと！",
               "ホールインワン目指しますよ～～！",
               "いやー、私なんぞはまだまだ。",
               "ドラコン賞はいただき！",
               "池ポチャかな～",
               "風向きヨシ！",
               "もう１ラウンド行きますか？",
               ],
    'Tremor': ["まさかこれしきの震動がこわいとか？",
              "今の感じたかい？",
              "今のは余震にすぎないよ。",
              "おや、これはキミが震えてるのかい？",
              "こりゃいったい震度いくつだろ？",
              "恐怖に震えてるのか？",
              "立っていられるかな？",
              "これでもまだ耐えるっていうのか？",
              "足元からくずしてやる！",
               ],
    'Watercooler': ["これで頭を冷やしな！",
                    "顔洗って出直してこい！",
                    "みっともない、これできれいにしな！",
                    "ばっしゃーん！",
                    "シャワーでも浴びな。",
                    "心配しないで大丈夫、 ろ過してあるから。",
                    "ちゃんとお風呂入ってるのかい？",
                    "ちゃんと洗濯してるかい？",
                    "水遊びは好き？",
                    "ノド乾いてるんだろ？",
                    "服が色落ちしちゃうね。",
                    "水分補給が必要だな。",
                    ],
    'Withdrawal': ["もう残金がありませんよ。",
                   "口座にお金は残っていますか～？",
                   "利子が倍返しになるよ。",
                   "借金地獄になっちゃうよ。",
                   "そろそろ振り込みをしないとあぶないよ。",
                   "家計がまずいことになってるんじゃないか？",
                   "もしかして、赤字？",
                   "お買い物は計画的に！",
                   "破産が近いんじゃない？",
                   "口座がなくなっちゃうよ。",
                   ],
    'WriteOff': ["損失をチェックしてみようか。",
                 "こりゃー、分が悪い取引をしちゃってるね。",
                 "給料が来月出るかもあやしいかもね。",
                 "これはひどいな。",
                 "キミの負債を算出してるんだが…",
                 "生じた損害には責任を持ってもらう。",
                 "ボーナスのことは忘れたほうがいいね。",
                 "キミのアカウントを見てみよう。",
                 "全てはやりくり次第だよ。",
                 "限界ギリギリまで行くね、これは。",
                 ],
    }

# DistributedBuilding.py
BuildingWaitingForVictors = "他のプレイヤーを待っています…",

# Elevator.py
ElevatorHopOff = "おりる"
ElevatorStayOff = "一度おりたら、みんなもおりるのを待つか\n次のエレベーターを待ってね。"
ElevatorLeaderOff = "おりるタイミングはリーダーにまかせてね。"
ElevatorHoppedOff = "次のエレベーターを待ってね。"
ElevatorMinLaff = "このエレベーターに乗るにはゲラゲラポイントが%s必要です。"
ElevatorHopOK = "OK"
ElevatorGroupMember = "のるタイミングは\nリーダーにまかせてね。"

# DistributedCogKart.py
KartMinLaff = "このカートに乗るには\nゲラゲラメーターが%s必要です。"

# DistributedBuilding.py　★
# DistributedElevatorExt.py　★
CogsIncExt = "・インク"
CogsIncModifier = "%s" + CogsIncExt
CogsInc = Cogs.upper() + CogsIncExt

# DistributedKnockKnockDoor.py
DoorKnockKnock = "コンコン！"
DoorWhosThere = "そこにいるのはだーれ？"
DoorWhoAppendix = "ってだーれ？"
DoorNametag = "ドア"

# FADoorCodes.py
# Strings associated with codes
FADoorCodes_UNLOCKED = None
FADoorCodes_TALK_TO_TOM = "ギャグが必要だよ！チュートリアル・トムに話しかけてみてね。"
FADoorCodes_DEFEAT_FLUNKY_HQ = "オベッカーを倒したらまた来てね！"
FADoorCodes_TALK_TO_HQ = "ごほうびがＨＱスタッフのハリーからもらえるよ！"
FADoorCodes_WRONG_DOOR_HQ = "間違い！プレイグラウンドに行くドアはもうひとつの方だよ。"
FADoorCodes_GO_TO_PLAYGROUND = "間違い! プレイグランドに行かなくちゃ！"
FADoorCodes_DEFEAT_FLUNKY_TOM = "バトルをはじめるには、オベッカーに近づいてみて！"
FADoorCodes_TALK_TO_HQ_TOM = "トゥーンＨＱでごほうびがもらえるよ！"
FADoorCodes_SUIT_APPROACHING = None  # no message, just refuse entry.
FADoorCodes_BUILDING_TAKEOVER = "気をつけて！そこには「コグ」がいるよ！"
FADoorCodes_SB_DISGUISE_INCOMPLETE = "トゥーンの姿のままで入るとつかまるから、ちゃんとコグに変装しよう！\n\nコグファクトリーからパーツを手に入れて変装しよう！"
FADoorCodes_CB_DISGUISE_INCOMPLETE = "トゥーンの姿のままで入るとつかまるから、ちゃんとマネーボットに変装しよう！\n\nドリームランド内のタスクをして変装パーツを手に入よう！"
FADoorCodes_LB_DISGUISE_INCOMPLETE = "トゥーンの姿のままで入るとつかまるから、ちゃんとロウボットに変装しよう！\n\nドリームランド内のタスクをして変装パーツを手に入よう！"
FADoorCodes_BB_DISGUISE_INCOMPLETE = "トゥーンのままだとつかまっちゃうよ！まずコグの変装パーツを集めよう。\n\nドナルドのドリームランドでもらえるトゥーンタスクをやるとロウボットの変装ができるよ。"

# KnockKnock joke contest winners ▲
KnockKnockContestJokes = {
    2100 : ["ハイドン",
            "こんな名前だけど音楽は苦手なんだ～"],

    # 2009 April fools contest Jokes. First few doors of Loopy lane
    2200 : {28:["Biscuit",
            "Biscuit out of here the Cogs are coming!"],
            41:["Dewey",
            "Dewey want to go defeat some more Cogs?"],
            40:["Minnie",
            "Minnie people have asked that, and it's driving me crazy!"],
##            25:["Biscuit25",
##            "Biscuit out of here the Cogs are coming!"],
            27:["Disguise",
            "Disguise where the Cogs fly!"]},

    2300: ["ジャスティン",
            "間にあったね。ジャスト・イン・タイム！"],

    # Polar Place has multiple jokes so they are in a dict keyed of the propId of the door
    3300: { 10: ["Aladdin",
                   "Aladdin HQ wants a word with you."],
            6 : ["Weirdo",
                 "Weirdo all these Cogs come from?"],
            30 : ["Bacon",
                  "Bacon a cake to throw at the Cogs."],
            28: ["Isaiah",
                 "Isaiah we go ride the trolley."],
            12: ["Juliet",
                 "Juliet me in that Cog building with you and I'll give you a Toon-Up."],
            },
     }

# KnockKnockJokes.py
KnockKnockJokes = [
#    ["ダズンDozen",
#    ""],

#    ["フレディ",
#    "Freddie or not, here I come."],

#    ["ディッシュDishes",
#    "Dishes your friend, let me in."],

    ["ウッディーだよ",
    "でも金物屋なんだ。"],

#    ["ベティBetty",
#    "Betty doesn't know who I am."],

#    ["ケントKent",
#    "Kent you tell?"],

#    ["ノアNoah",
#    "Noah don't know who either."],

#    ["しらないI don't know",
#    "Neither do I, I keep telling you that."],

#    ["ハワードHoward",
#    "Howard I know?"],

#    ["エマEmma",
#    "Emma so glad you asked me that."],

#    ["オートAuto",
#    "Auto know, but I've forgotten."],

#    ["ジェスJess",
#    "Jess me and my shadow."],

#    ["ワンOne",
#    "One-der why you keep asking that?"],

#    ["アルマAlma",
#    "Alma not going to tell you!"],

#    ["ズームZoom",
#    "Zoom do you expect?"],

#    ["エイミーAmy",
#    "Amy fraid I've forgotten."],

#    ["アーファーArfur",
#    "Arfur got."],

#    ["ユアンEwan",
#    "No, just me"],

#    ["コージーCozy",
#    "Cozy who's knocking will you?"],

    ["サムだよ",
    "でも本当はあつがりなんだ…"],

#    ["フォジーFozzie",
#    "Fozzie hundredth time, my name is " + Flippy + "."],

#    ["ディダクトDeduct",
#    Donald + " Deduct."],

#    ["マックスMax",
#    "Max no difference, just open the door."],

#    ["Ｎ．Ｅ．N.E.",
#    "N.E. body you like, let me in."],

#    ["アモス（エイモス）Amos",
#    "Amos-quito bit me."],

#    ["アルマAlma",
#    "Alma candy's gone."],

    ["ブルースだよ",
    "ジャズが大好きなブルースだよ。"],

#    ["コリーンColleen",
#    "Colleen up your room, it's filthy."],

#    ["エルシーElsie",
#    "Elsie you later."],

#    ["ヒューHugh",
#    "Hugh is going to let me in?"],

#    ["ヒューゴHugo",
#    "Hugo first - I'm scared."],

#    ["アイダIda",
#    "Ida know.  Sorry!"],

#    ["イサベルIsabel",
#    "Isabel on a bike really necessary?"],

#    ["ジョアンJoan",
#    "Joan call us, we'll call you."],

    ["ケイだよ",
    "ケイ、エル、エム、オー、ピー…"],

    ["ジャスティンだよ",
    "間にあったね。ジャスト・イン・タイム！"],

#    ["ライザLiza",
#    "Liza wrong to tell."],

#    ["ルークLuke",
#    "Luke and see who it is."],

#    ["マンディMandy",
#    "Mandy the lifeboats, we're sinking."],

    ["マックスだよ",
    "そんなにマクスたてないで～"],

#    ["ネッティNettie",
#    "Nettie as a fruitcake."],

#    ["オリビア",
#    "へぇ～！"],

#    ["オスカーOscar",
#    "Oscar stupid question, you get a stupid answer."],

#    ["パッツィPatsy",
#    "Patsy dog on the head, he likes it."],

#    ["ポールPaul",
#    "Paul hard, the door's stuck again."],

#    ["テアThea",
#    "Thea later, alligator."],

#    ["タイローンTyrone",
#    "Tyrone shoelaces, you're old enough."],

#    ["ステラStella",
#    "Stella no answer at the door."],

#    ["ユリアUriah",
#    "Keep Uriah on the ball."],

#    ["ドゥエインDwayne",
#    "Dwayne the bathtub.  I'm drowning."],

#    ["ディスメイDismay",
#    "Dismay be a joke, but it didn't make me laugh."],

#    ["オセロットOcelot",
#    "Ocelot of questions, don't you?"],

#   ["テルモスThermos",
#    "Thermos be a better knock knock joke than this."],

#    ["スルタンSultan",
#    "Sultan Pepper."],

#    ["ヴォーンVaughan",
#    "Vaughan day my prince will come."],

#    ["ドナルドDonald",
#    "Donald come baby, cradle and all."],

#    ["レタスLettuce",
#    "Lettuce in, won't you?"],

#    ["イヴォールIvor",
#    "Ivor sore hand from knocking on your door!"],

#    ["イサベルIsabel",
#    "Isabel broken, because I had to knock."],

#    ["ヘイウッド、ヒュー、、ハリーHeywood, Hugh, Harry",
#    "Heywood Hugh Harry up and open this door."],

#    ["フアンJuan",
#    "Juan of this days you'll find out."],

    ["アールさ",
    "なくてもア～ル！"],

    ["ジミーだよ。",
    "でもハデ好きなんだ！"],

#    ["アボットAbbot",
#    "Abbot time you opened this door!"],

#    ["ファーディーFerdie",
#    "Ferdie last time, open the door!"],

#    ["ドンDon",
#    "Don mess around, just open the door."],

#    ["シスSis",
#    "Sis any way to treat a friend?"],

#    ["イサドアIsadore",
#    "Isadore open or locked?"],

    ["ハリーです",
    "でもよくのんきだねって言われるんだ…"],

#    ["テオドアTheodore",
#    "Theodore wasn't open so I knocked-knocked."],

#    ["ケンKen",
#    "Ken I come in?"],

#    ["ブーBoo",
#    "There's no need to cry about it."],

#    ["ユーYou",
#    "You who!  Is there anybody there?"],

#    ["アイスクリームIce cream",
#    "Ice cream if you don't let me in."],

#    ["サラSarah",
#    "Sarah 'nother way into this building?"],

#    ["マイキーMikey",
#    "Mikey dropped down the drain."],

#    ["ドリスDoris",
#    "Doris jammed again."],

#    ["イエルプYelp",
#    "Yelp me, the door is stuck."],

#    ["スコルドScold",
#    "Scold outside."],

#    ["ダイアナDiana",
#    "Diana third, can I have a drink please?"],

#    ["ドリスDoris",
#    "Doris slammed on my finger, open it quick!"],

#    ["レタスLettuce",
#    "Lettuce tell you some knock knock jokes."],

#    ["イージーだよ",
#    "！"],

#    ["オマー",
#    "Omar goodness gracious - wrong door!"],

    ["セズだよ",
    "道草セズに来たよ～"],

#    ["ダックDuck",
#    "Just duck, they're throwing things at us."],

#    ["タンクTank",
#    "You're welcome."],

#    ["アイズEyes",
#    "Eyes got loads more knock knock jokes for you."],

#    ["ピザ",
#    "宅配じゃないよ、ぼくだよ～"],

#    ["クロージュアClosure",
#    "Closure mouth when you eat."],

#    ["ハリエットHarriet",
#    "Harriet all my lunch, I'm starving."],

#    ["ウッデンWooden",
#    "Wooden you like to know?"],

#    ["パンチPunch",
#    "Not me, please."],

    ["リッチで～す",
    "お金持ちじゃないけど…"],

#    ["ジュピターJupiter",
#    "Jupiter hurry, or you'll miss the trolley."],

#    ["ベルタBertha",
#    "Happy Bertha to you!"],

#    ["カウCows",
#    "Cows go \"moo\" not \"who.\""],

#    ["マグロ（ツナフィッシュ）Tuna fish",
#    "You can tune a piano, but you can't tuna fish."],

#    ["コンサンプション（タベル）Consumption",
#    "Consumption be done about all these knock knock jokes?"],

#    ["バナナBanana",
#    "Banana spilt so ice creamed."],

#    ["エックスX",
#    "X-tremely pleased to meet you."],

    ["ハイドンだよ",
    "こんな名前だけど音楽は苦手なんだ～"],

#    ["ローダRhoda",
#    "Rhoda boat as fast as you can."],

#    ["グワグワQuacker",
#    "Quacker 'nother bad joke and I'm off!"],

    ["ナナよ",
    "ラッキー！"],

#    ["エーテルEther",
#    "Ether bunny."],

#    ["オバサンLittle old lady",
#    "My, you're good at yodelling!"],

#    ["ビートBeets",
#    "Beets me, I forgot the joke."],

#    ["ハルHal",
#    "Halloo to you too!"],

#    ["サラSarah",
#    "Sarah doctor in the house?"],

#    ["アイリーンAileen",
#    "Aileen Dover and fell down."],

#    ["アトミックAtomic",
#    "Atomic ache"],

#    ["アガサAgatha",
#    "Agatha headache.  Got an aspirin?"],

#    ["スタンStan",
#    "Stan back, I'm going to sneeze."],

#    ["ハッチHatch",
#    "Bless you."],

#    ["アイダIda",
#    "It's not Ida who, it's Idaho."],

#    ["ジッピーZippy",
#    "Mrs. Zippy."],

#    ["ユーコンYukon",
#    "ユウコじゃなくてユーコン！"],
]

# CChatChatter.py

# Shared Chatter

SharedChatterGreetings = [
        "こんにちは、%！",
        "%、会えてうれしいよ。",
        "会いに来てくれてありがとう！",
        "来てくれたんだね、%！",
        ]

SharedChatterComments = [
        "%って、ステキななまえだね！",
        "ステキななまえだね。",
        "" + Cogs + "に気をつけてね！",
        "トロリーが来たみたいだよ。",
        "トロリーゲームをプレイして、パイを集めたいんだ。",
        "フルーツパイが食べたくてトロリーゲームをプレイするんだ～",
        "" + Cogs + "の一団を追い払ってきたとこなんだ。ひとやすみしようっと！",
        "" + Cogs + "の中にも大きいのがいるね、たいへんだ！",
        "楽しんでるみたいだね。",
        "ああ、今日はさいこうに楽しいなぁ！",
        "すてきな服だね。",
        "今日は釣りに行ってこようかな。",
        "ウチの近所で楽しんでいってね！",
        "トゥーンタウンでの生活、楽しんでる？",
        "ブルブルランドで雪がふってるらしいよ。",
        "今日、トロリーに乗った？",
        "あたらしいともだちを作るのは楽しいよ。",
        "ブルブルランドにたくさんの" + Cogs + "がいるんだって！",
        "鬼ゴッコって楽しいよね！キミは鬼ゴッコ、好き？",
        "トロリーゲームって楽しいな～！",
        "他のひとを笑わせるのが好きなんだ。",
        "ともだちを助けるのって楽しいよ。",
        "ええっと、迷子になったの？トゥーンガイドに地図があるから見てみてね。",
        "" + Cogs + "の「ガンジガラメ」こうげきはやっかいだよ～",
        "" + Daisy + "がガーデンに新しい花を植えたんだって！",
        "PageUpキーを押し続けると、上を向けるよ！",
        "コグビルをたおすと、ブロンズの星がもらえるよ！",
        "Tabキーを押し続けると、周りを自分の視点で見られるよ！",
        "Ctrlキーを押すと、ジャンプできるよ！",
        ]

SharedChatterGoodbyes = [
        "そろそろ行かなきゃ。じゃあね！",
        "トロリーゲームでもやってこようかな～",
        "じゃあ、またね、%！",
        "" + Cogs + "をやっつけてこなくちゃ…",
        "そろそろ行かなくちゃ。またね。",
        "じゃあね、また会おう！",
        "バイバイ！",
        "またね、%！",
        "カップケーキ投げのれんしゅうをしてこようかな。",
        "" + Cogs + "をそしするためにも、グループに入ってくるね。",
        "会えて嬉しかったよ、%",
        "今日はすっごくいそがしいんだ、行かなくちゃ！",
        ]

# Lines specific to each character.
# If a talking char is mentioned, it cant be shared among them all

MickeyChatter = (
        [ # Greetings specific to Mickey
        lToontownCentral+"へようこそ！", #CC_mickey_chatter_greetings01.mp3
        "こんにちは！僕の名前は" + Mickey + "マウス。君の名前は？", #CC_mickey_chatter_greetings02.mp3
        ],
        [ # Comments
        "ねぇ、キミ！" + Donald + "を見かけなかった？", #CC_mickey_chatter_comments01.mp3
        "これから、うっすらと霧の立ち込めた、"+lDonaldsDock+"に行こうと思うんだ！", #CC_mickey_chatter_comments02.mp3
        "もし僕の友達の" + Goofy + "に会ったら、よろしく言っておいてね。", #CC_mickey_chatter_comments03.mp3
        "ははっ！どうやら" + Daisy + "がお庭に新しいお花を植えたらしいよ。", #CC_mickey_chatter_comments04.mp3
        ],
        [ # Goodbyes
        "これから、" + Minnie + "に会いにメロディーランドに行こうかなぁ。", #CC_mickey_chatter_goodbyes01.mp3
        "ああっ、" + Minnie + "とのデートにおくれちゃうよ！", #CC_mickey_chatter_goodbyes02.mp3
        "そろそろ" + Pluto + "に晩御飯の準備をしないと…", #CC_mickey_chatter_goodbyes03.mp3
        "キミは"+lDonaldsDock+"に泳ぎに行ったことある？", #CC_mickey_chatter_goodbyes04.mp3
        "ドリームランドにおひるねしに行こうかなぁ…", #CC_mickey_chatter_goodbyes05.mp3
        ]
    )

VampireMickeyChatter = (
        [ # Greetings specific to Vampire Mickey
        ""+lToontownCentral+"へようこそ！",
        "ボクのなまえは"+Mickey+"。キミのなまえは？",
        "ハッピー・ハロウィーン！",
        "楽しいハロウィーンになるといいね、%！",
        "今年も"+lToontownCentral+"がくろねこトゥーンでいっぱいになるよ！",
        ],
        [ # Comments
        "ハロウィーンって楽しいよね！",
        "このコスチューム、どうかなぁ？",
        "%もガッツキーには気をつけてね！",
        "ハロウィーンのデコレーション、気に入ってくれた？",
        "くろねこトゥーン達とはなかよしなんだ♪",
        "ねぇ、カボチャ頭のトゥーンを見た？",
        "バァーッ！ハハッ、おどろいた？",
        "ちゃんとキバを歯ブラシでみがこうね☆",
        "だいじょうぶ。ボクはフレンドリーなドラキュラだから♪",
        "ボクのマント、かっこいいでしょ？",
        "おどろいた？ボクのセンス、なかなかでしょ？",
        "トゥーンタウンのハロウィーンを楽しんでいってね！",
        "今夜はきっともりあがるだろうね。",
        ],
        [ # Goodbyes
        "ハロウィーンのすてきなデコレーションをみにゆこうよ。",
        ""+Minnie+"をおどろかしにメロディーランドに行ってこようかな。",
        "しぃ～、これから他のトゥーンをおどろかすんだ！",
        "トリック・オア・トリート！",
        "いっしょにみんなをおどろかしに行こうよ♪",
        ]
    )

MinnieChatter = (
        [ # Greetings
        "メロディランドへようこそ！", #CC_minnie_chatter_greetings01.mp3
        "私は" + Minnie + "マウスよ。あなたのお名前は？", #CC_minnie_chatter_greetings02.mp3
        ],
        [ # Comments
        "ここはいろいろな楽器の音色であふれてるのよ！", #CC_minnie_chatter_comments01.mp3
        # the merry no longer goes round
        #"大きなメリーゴーランドを是非試してみてね！", #CC_minnie_chatter_comments02.mp3
        "あら！おしゃれなお洋服ね！", #CC_minnie_chatter_comments03.mp3
        "ねぇ、" + Mickey + "を見かけなかった？", #CC_minnie_chatter_comments04.mp3
        "" + Goofy + "に会ったら、よろしくね。", #CC_minnie_chatter_comments05.mp3
        "たくさんの" + Cogs + "が" + Donald + "のドリームランドまわりにいるらしいわ。", #CC_minnie_chatter_comments06.mp3
        lDonaldsDock+"には霧が立ち込めているみたいよ。", #CC_minnie_chatter_comments07.mp3
        lDaisyGardens+"の迷路も試してみてね。", #CC_minnie_chatter_comments08.mp3
        "私も楽器を演奏してみようかしら。", #CC_minnie_chatter_comments091.mp3
        "ねぇ、あれを見て！", #CC_minnie_chatter_comments10.mp3
        "楽器の音色ってほんと素敵よね。", #CC_minnie_chatter_comments11.mp3
        "メロディーランドはトゥーンじゃなくてチューンタウンなの。うふっ。", #CC_minnie_chatter_comments12.mp3
        "マッチングゲームって面白いわよね。そう思わない？", #CC_minnie_chatter_comments13.mp3
        "みんなが笑ってくれるとわたし、とってもうれしいわ！", #CC_minnie_chatter_comments14.mp3
        "ねぇ、歩き回ってつかれたんじゃなぁーい？", #CC_minnie_chatter_comments15.mp3
        "まぁ。素敵なシャツね！", #CC_minnie_chatter_comments16.mp3
        "あらっ、そこにあるのはゼリービーンかしら？", #CC_minnie_chatter_comments17.mp3
        ],
        [ # Goodbyes
        "いっけなーい、" + Mickey + "と会う約束をしてたんだ。", #CC_minnie_chatter_goodbyes01.mp3
        "そろそろ" + Pluto + "の夕飯のしたくする時間だわっ。", #CC_minnie_chatter_goodbyes02.mp3
        "ふぁーっ、ドリームランドに行こうかしら？", #CC_minnie_chatter_goodbyes03.mp3
        ]
    )
    
DaisyChatter = (
        [ # Greetings
        "マイガーデンへようこそ！",
        "こんにちは！わたしは"+Daisy+"。あなたの名前をおしえてちょうだい。",
        "あなたにお会いできてうれしいわ！",
        ],
        [ # Comments
        "賞品のお花は庭の迷路の中にあるわよ。",
        "迷路をぶらぶら散歩するのが好きなの。",
        "ずっと"+Goofy+"グーフィーを見てないのよね。",
        "一体、"+Goofy+"はどこにいるのかしら？",
        "ねぇ、"+Donald+"を見かけなかった？どこ探しても見つからないのよ。",
        "私の友達の"+Minnie+"を見かけたら、よろしくって伝えてくださらない？",
        "いいガーデニングツールがあれば、植物もよく育つのよ。",
        "たくさんの"+Cogs+"が"+lDonaldsDock+"にいるらしいのよ。",
        "毎日の水やりは植木をハッピーにするのよ！",
        "ピンクデイジーを育てたければ、黄色と赤のジェリービーンを植えてね。",
        "イエローデイジーを育てるには、黄色のジェリービーンを植えてね。",
        "もし植木の下に砂が見えたら、水をあげてね。でないと、植木がかれちゃうよ！"
        ],
        [ # Goodbyes
        "メロディーランドに%sに会いに行くところよ。" % Minnie,
        "%sとのピクニックに遅れちゃうわ～！" % Donald,
        "これから"+lDonaldsDock+"に泳ぎに行こうかしら。",
        "ふぁ～っ。ちょっと眠くなったから、ドリームランドに行こうかしら。",
        ]
    )

ChipChatter = (
        [ # Greetings
        "%sにようこそ!" % lOutdoorZone,
        "やぁ、僕は" + Chip + "。キミの名前は？",
        "僕が" + Chip + "だよ！",
        "%、会えてほんとうにうれしいよ！",
        "僕たちはチップとデールだよ！",
        ],
        [ # Comments
        "ゴルフが大好きなんだ！",
        "ここのドングリはトゥーンタウンで一番なのさ。",
        "火山があるゴルフコースが一番むずかしいとおもうよ。",
        ],
        [ # Goodbyes
        "これから" + lTheBrrrgh +"に行って%sとあそぶんだ！" % Pluto,
        "これから%sに会いに行ってくるんだ。" % Donald,
        "今日は" + lDonaldsDock + "までおよぎに行こうかなぁ♪",
        "なんだかねむいなぁ…。ドリームランドでひとねむりしようかな。",
        ]
    )

# Warning Dale's chatter is dependent on on Chip's, they should match up
DaleChatter = (
        [ # Greetings
        "%、よくきてくれたね！",
        "こんにちは、僕" + Dale + "だよ。キミの名前は？",
        "僕は" + Chip + "だよ。",
        "%sへようこそ！" % lOutdoorZone,
        "僕たちがチップとデールだよ。",
        ],
        [ # Comments
        "ピクニックって楽しいよね。",
        "ここのドングリはおいしいんだよ。",
        "そこの風車はもうためした？",
        ],
        [ # Goodbyes
        "ヒヒヒ、" + Pluto + "は遊びともだちなんだ！",
        "よし、%sに行くじゅんびをしよう！" % Donald,
        "のんびりと泳ぎにゆきたいなあ。",
        "うん、そろそろつかれてきたからきゅうけいしようよ。",
        ]
    )

GoofyChatter = (
        [ # Greetings
        "ようこそ、"+lDaisyGardens+"へ！", #CC_goofy_chatter_greetings01.mp3
        "僕の名前は" + Goofy + "。よろしくね。キミの名前は？", #CC_goofy_chatter_greetings02.mp3
        "おひょっ。キミにあえてうれしいよ。", #CC_goofy_chatter_greetings03.mp3
        ],
        [ # Comments
        "迷路に迷わないように気をつけてね。", #CC_goofy_chatter_comments01.mp3
        "キミもここの迷路を試してみない？楽しいよ！", #CC_goofy_chatter_comments02.mp3
        "ねぇ、キミ。" + Daisy + "を見かけなかった？", #CC_goofy_chatter_comments03.mp3
        "ありゃま、" + Daisy + "はどこに行ったのかなぁ。", #CC_goofy_chatter_comments04.mp3
        "ねぇ、" + Donald + "はどこにいるか知ってる？知ってたら教えてね。", #CC_goofy_chatter_comments05.mp3
        "もし僕の親友の" + Mickey + "にあったらよろしくね。", #CC_goofy_chatter_comments06.mp3
        "おなかすいたなぁ。", #CC_goofy_chatter_comments07.mp3
        "この街の外にはね。" + Cogs + "がたくさんいるんだよ。", #CC_goofy_chatter_comments08.mp3
        "ねぇ、見て見て。" + Daisy + "がお花を植えたのかなぁ。", #CC_goofy_chatter_comments09.mp3
        "おひょっ。いろんな種類のギャグがあるから集めてごらん。", #CC_goofy_chatter_comments10.mp3
        "街には必ずギャグショップがあるよ。楽しいよ。", #CC_goofy_chatter_comments11.mp3
        "ギャグショップにはたっくさんギャグがあるよ。笑い過ぎないように気をつけてね。" #CC_goofy_chatter_comments12.mp3
        ],
        [ # Goodbyes
        "これから、" + Minnie + "に会いに、メロディーランドに行くところなんだ。", #CC_goofy_chatter_goodbyes01.mp3
        "オヒョッ！急がないと遅れちゃう！" + Donald + "と約束してたんだ！", #CC_goofy_chatter_goodbyes02.mp3
        lDonaldsDock+"に泳ぎに行こうかなぁ。", #CC_goofy_chatter_goodbyes03.mp3
        "ふああ…お昼寝の時間みたい。ドリームランドに行かなくちゃ。", #CC_goofy_chatter_goodbyes04.mp3
        ]
    )



GoofySpeedwayChatter = (
        [ # Greetings
        "ようこそ！"+lGoofySpeedway+"へ！",
        "やあ、僕の名前は"+Goofy+"だよ。キミの名前を教えてよ。",
        "オヒョッ！キミに会えてうれしいよ%!",
        ],
        [ # Comments
        "さっきすごいレースを見たんだよ！",
        "コースにあるバナナの皮に気をつけてね！",
        "最近、キミのカートをアップグレードしたかな？",
        "カートショップに新しいパーツが入ったみたいだよ！",
        "ねぇ、ちょっと！"+Donald+"を見なかった？",
        "おっと！"+Mickey+"の朝ごはんの準備をするのをすっかり忘れてたよ！",
        "もし僕のともだちの"+Mickey+"に会ったら、よろしく伝えてよ！",
        "オヒョッ！"+lDonaldsDock+"に"+Cogs+"たちが、うようよしてるって！",
        "ブルブルランドのギャグショップでは、ぐるぐるめがねがなんと１ジェリービーンで売ってるよ！",
        "ボクのギャグショップではトゥーンタウン中で一番のジョークや笑いのたねを取りそろえてるんだよ！",
        "ギャグショップのパイは笑いの保障つき！笑わなかったらジェリービーンをちゃんとキミに返すよ！"
        ],
        [ # Goodbyes
        "ちょっと%sに会いにメロディーランドに行ってくるよ。" % Mickey,
        "オヒョッ！%sとのゲームの約束におくれちゃう！" % Donald,
        "ねえねえ、キミ！"+lDonaldsDock+"で泳ぎに行こうかな？",
        "あっ、お昼寝の時間だ！ドリームランドに行こうかなー。",
        ]
    )

DonaldChatter = (
        [ # Greetings
        "ドリームランドへようこそ！", #CC_donald_chatter_greeting01.mp3
        "僕は" + Donald + "！君の名前は？", #CC_donald_chatter_greeting02.mp3
        ],
        [ # Comments
        "ここではたまにこわいことがあるんだよ。", #CC_donald_chatter_comments01.mp3
        "ねぇ、"+lDaisyGardens+"に行った？", #CC_donald_chatter_comments02.mp3
        "今日もいい日だねっ！", #CC_donald_chatter_comments03.mp3
        "ねぇ、" + Mickey + "を見なかった？", #CC_donald_chatter_comments041.mp3
        "" + Goofy + "によろしくね。", #CC_donald_chatter_comments05.mp3
        "釣りに行こうかなぁ", #CC_donald_chatter_comments06.mp3
        "わぉ、町の外に、コグたちがたくさんいるよ。" #CC_donald_chatter_comments07.mp3
        "もうボートには乗った？", #CC_donald_chatter_comments08.mp3
        "" + Daisy + "を見なかった？", #CC_donald_chatter_comments09.mp3
        "" + Daisy + "がお庭にお花を植えたみたいだよ。", #CC_donald_chatter_comments10.mp3
        "クワッ！", #CC_donald_chatter_comments11.mp3
        ],
        [ # Goodbyes
        "" + Minnie + "に会いに行こうかな？", #CC_donald_chatter_goodbyes01.mp3
        "" + Daisy + "とのデートに遅れちゃう…", #CC_donald_chatter_goodbyes02.mp3
        "よおっし、ちょっと泳ごうかなぁ…", #CC_donald_chatter_goodbyes03.mp3
        "ボートは楽しいな！", #CC_donald_chatter_goodbyes04.mp3
        ]
    )

# April Fools Chatter's
AFMickeyChatter = (
        [ # Greetings specific to Mickey
        "Happy April Toons' Week!",        
        "Happy April Toons' Week, %!",
        "Hi, my name is "+Mickey+". What's yours?",
        ],
        [ # Comments
        "Have you seen Daisy around?",
        "I want to wish Daisy a happy April Toons' Week!",
        "Did you hear a Doodle talk?",
        "My, aren't these flowers nice!",
        "I bet Daisy has some great Gardening tips!",
        ],
        [ # Goodbyes
        "Hi, I am looking for Daisy. Have you seen her?",
        "It's time for a nap. I'm going to Dreamland.",
        ]
    )

AFMinnieChatter = (
        [ # Greetings
        "Hi, my name is "+Minnie+". What's yours?",        
        "Happy April Toons' Week!",        
        "Happy April Toons' Week, %!",
        ],
        [ # Comments
        "Hi, I need to give Pluto his lunch. Have you seen him?",
        "I want to wish Pluto a happy April Toons' Week with a doggie treat!",
        "Did you hear a Doodle talk?",
        ],
        [ # Goodbyes
        "Hi, I need to give Pluto his lunch. Have you seen him?",
        "Gosh, I'm late for my date with %s!" % Mickey,
        ]
    )

AFDaisyChatter = (
        [ # Greetings
        "Hello, I'm "+Daisy+". What's your name?",
        "Happy April Toons' Week!",        
        "Happy April Toons' Week, %!",
        ],
        [ # Comments
        "I wonder if Mickey went to fight some Cogs?",
        "Have you seen Mickey around?",
        "I want to wish Mickey a happy April Toons' Week!",
        "Did you hear a Doodle talk, or am I hearing things?",
        ],
        [ # Goodbyes
        "Hi, I need to talk with Micky. Have you seen him?",
        "I think I'll go swimming at "+lDonaldsDock+".",
        "Oh, I'm a little sleepy. I think I'll go to Dreamland.",
        ]
    )

AFGoofySpeedwayChatter = (
        [ # Greetings
        "Happy Sleepy, er, April Toons' Week!",
        "Happy April Toons' Week, %!",
        "Hi, my name is "+Goofy+". What's yours?",
        ],
        [ # Comments
        "Gawrsh, have you seen Donald? I think he's been sleep walking again.",
        "I want to wish Donald a happy April Toons' Week!",
        "Did you hear a Doodle talk, or am I seeing things?",
        "I hope everything is okay at the Speedway.",
        ],
        [ # Goodbyes
        "Gawrsh, I'm late for my game with %s!" % Donald,
        ]
    )

AFDonaldChatter = (
        [ # Greetings
        "Happy Sleepy, er, April Toons' Week!",
        "Happy April Toons' Week, %!",
        "Hi, my name is %s. What's yours?" % Donald,
        ],
        [ # Comments
        "Have you seen Goofy around?",
        "I want to wish Goofy a happy April Toons' Week!",
        "Did you hear a Doodle talk, or am I dreaming?",
        "Where did the kart come from?",
        ],
        [ # Goodbyes
        "Where are all those loud car noises suddenly coming from?",
        "I'm going to Melody Land to see %s!" % Minnie,
        ]
    )    

CLGoofySpeedwayChatter = (
        [ # Greetings
        "Welcome to "+lGoofySpeedway+".",
        "Hi, my name is "+Goofy+". What's yours?",
        "Gawrsh, it's nice to see you %!",
        "Hi there!  Pardon my dusty clothes I've been busy fixin' that broken Leaderboard.",
        ],
        [ # Comments        
        "We better get this Leaderboard working soon, Grand Prix Weekend is coming up!",
        "Does anybody want to buy a slightly used kart? It's only been through the Leaderboard once!",
        "Grand Prix Weekend is coming, better get to practicing.",
        "Grand Prix Weekend will be here on Friday, May 22 through Monday, May 25!",
        "I'm gonna need a ladder to get that kart down.",
        "That Toon really wanted to get on the Leaderboard!",
        "Boy, I saw a terrific race earlier.",
        "Watch out for banana peels on the race track!",
        "Have you upgraded your kart lately?",
        "We just got in some new rims at the kart shop.",
        "Hey, have you seen "+Donald+"?",
        "If you see my friend "+Mickey+", say hi to him for me.",
        "D'oh! I forgot to fix "+Mickey+"'s breakfast!",
        "Gawrsh there sure are a lot of "+Cogs+" near "+lDonaldsDock+".",
        "At the Brrrgh branch of my Gag Shop, Hypno-Goggles are on sale for only 1 jellybean!",
        "Goofy's Gag Shops offer the best jokes, tricks, and funnybone-ticklers in all of Toontown!",
        "At Goofy's Gag Shops, every pie in the face is guaranteed to make a laugh or you get your jellybeans back!"
        ],
        [ # Goodbyes
        "I better go get my kart a new paint job for the upcoming Grand Prix Weekend.",
        "Gosh, I better get workin' on this broken Leaderboard!",
        "Hope I'll see y'all on Grand Prix Weekend!  Goodbye!",
        "It's time for a nap. I'm going to Dreamland to dream about winnin' the Grand Prix.",
        ]
    )
        

GPGoofySpeedwayChatter = (
        [ # Greetings
        "Welcome to "+lGoofySpeedway+".",        
        "Welcome to Grand Prix Weekend!",
        "Hi, my name is "+Goofy+". What's yours?",
        "Gawrsh, it's nice to see you %!",
        ],
        [ # Comments                
        "Are you excited about the Grand Prix Weekend?",
        "Good thing we got the Leaderboard fixed.",
        "We got the Leaderboard fixed just in time for Grand Prix Weekend!",
        "We never did find that Toon!",
        "Boy, I saw a terrific race earlier.",
        "Watch out for banana peels on the race track!",
        "Have you upgraded your kart lately?",
        "We just got in some new rims at the kart shop.",
        "Hey, have you seen "+Donald+"? He said he was gonna come watch the Grand Prix!",
        "If you see my friend "+Mickey+", tell him he's missing some great racing!",
        "D'oh! I forgot to fix "+Mickey+"'s breakfast!",
        "Gawrsh there sure are a lot of "+Cogs+" near "+lDonaldsDock+".",
        "At the Brrrgh branch of my Gag Shop, Hypno-Goggles are on sale for only 1 jellybean!",
        "Goofy's Gag Shops offer the best jokes, tricks, and funnybone-ticklers in all of Toontown!",
        "At Goofy's Gag Shops, every pie in the face is guaranteed to make a laugh or you get your jellybeans back!"
        ],
        [ # Goodbyes
        "Good luck in the Grand Prix!",
        "I'm going to catch the next race in the Grand Prix!",
        "Gawrsh I think the next race is about to start!",
        "Gosh, I better go check on the new Leaderboard and make sure it is working right!",
        ]
    )

for chatter in [MickeyChatter,DonaldChatter,MinnieChatter,GoofyChatter]:
    chatter[0].extend(SharedChatterGreetings)
    chatter[1].extend(SharedChatterComments)
    chatter[2].extend(SharedChatterGoodbyes)

# FriendsListPanel.py
FriendsListPanelNewFriend = "新しいともだち"
FriendsListPanelSecrets = "ひみつリスト"
FriendsListPanelOnlineFriends = "オンラインの\nともだち"
FriendsListPanelAllFriends = "すべての\nともだち"
FriendsListPanelIgnoredFriends = "むしする\nトゥーン"
FriendsListPanelPets = "となりの\nペット"
FriendsListPanelPlayers = "すべての\nともだち"
FriendsListPanelOnlinePlayers = "オンラインの\nともだち"

FriendInviterClickToon = "ともだちになりたいトゥーンをクリックしてね。\n\n(げんざいの友だち%s人)"

# Support DISL account friends
FriendInviterToon = "トゥーン"
FriendInviterThatToon = "このトゥーン"
FriendInviterPlayer = "プレイヤー"
FriendInviterThatPlayer = "このプレイヤー"
FriendInviterBegin = "どのともだちタイプにする？"
FriendInviterToonFriendInfo = "トゥーンタウンだけのともだち"
FriendInviterPlayerFriendInfo = "Disney.jpのともだち"
FriendInviterToonTooMany = "あなたのおともだちがおおすぎてついかできません。%sをついかするには、ほかのトゥーンをさくじょしなくてはなりません。プレイヤーのともだちになれるときもあるのでためしてね。"
FriendInviterPlayerTooMany = "あなたのおともだちがおおすぎてついかできません。%sをついかするには、ほかのプレイヤーともだちをさくじょしなくてはなりません。トゥーンのともだちになれるときもあるのでためしてね。"
FriendInviterToonAlready = "%sはすでにキミのともだちです。"
FriendInviterPlayerAlready = "%sはすでにキミのともだちです。"
FriendInviterStopBeingToonFriends = "ともだちをやめる"
FriendInviterStopBeingPlayerFriends = "ともだちをやめる"
FriendInviterEndFriendshipToon = "ほんとうに%sのともだちをやめてもいいかい？"
FriendInviterEndFriendshipPlayer = "ほんとうに%sのともだちをやめてもいいかい？"
FriendInviterRemainToon = "\n(%sとはまだおともだちトゥーンです。)"
FriendInviterRemainPlayer = "\n(%sとはまだおともだちプレイヤーです。)"

# DownloadForceAcknowledge.py
# phase, percent
DownloadForceAcknowledgeMsg = "%(phase)sのダウンロードが%(percent)s%%しかされていないので、先に進めません。\n\n後で再試行してください"

# TeaserPanel.py
TeaserTop = ""
TeaserBottom = ""
TeaserDefault = "\nフルアクセス専用だよ。\n登録しよう！"
TeaserOtherHoods = "７つの変わったエリアで楽しもう！"
TeaserTypeAName = "自分のトゥーンに好きな名前をつけよう！"
TeaserSixToons = "１つのアカウントでトゥーンを６つ作れるよ！"
TeaserClothing = "ユニークなアイテムでキミのトゥーンを目立たせよう！"
TeaserCogHQ = "強いコグたちの危険なエリアに忍び込もう！"
TeaserSecretChat = "ともだちとパスワードを交換して、オンラインでチャットしよう！"
TeaserSpecies = "サルやウマ、クマのトゥーンを作って遊ぼう！"
TeaserFishing = "全種類のサカナを集めてみよう！"
TeaserGolf = "しかけが一杯のゴルフコースで楽しもう！"
TeaserParties = "パーティーを開こう"
TeaserSubscribe = "今すぐ申し込む"
TeaserContinue = "お試し体験を続ける"
TeaserEmotions = "カタログでは「手をふる」、「ほめる」といったトゥーンの\n  表現も買うことができるよ。表現ゆたかなトゥーンにしよう！"
TeaserKarting = "ともだちのカートと一緒に楽しくレースしよう！"
TeaserKartingAccessories = "かっこいいアクセサリーで、キミのカートをカスタマイズしよう!"
TeaserGardening = "キミのおうちの庭を花や像やギャグの木できれいにかざろう！"
TeaserHaveFun = "楽しんでね！"
TeaserJoinUs = "登録しよう！"

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
DownloadWatcherUpdate = "%sをﾀﾞｳﾝﾛｰﾄﾞ中…"
DownloadWatcherInitializing = "ﾀﾞｳﾝﾛｰﾄﾞを始めます…"

# Launcher.py
LauncherPhaseNames = {
    0   : "初期化中",
    1   : "パンダ",
    2   : "エンジン",
    3   : "ﾄｩｰﾝ",
    3.5 : "ﾄｩｰﾝﾄﾘｱﾙ",
    4   : "ﾌﾟﾚｲｸﾞﾗｳﾝﾄﾞ",
    5   : "ｽﾄﾘｰﾄ",
    5.5 : "おうち",
    6   : "ｴﾘｱ①",
    7   : Cog,
    8   : "ｴﾘｱ②",
    9   : Cog + lHQ,
    10  : lCashbotHQ,
    11  : lLawbotHQ,
    12  : Bossbot + " HQ",
    13  : "ﾊﾟｰﾃｨｰ",
    }

# Lets make these messages a little more friendly
LauncherProgress = "%(name)sの (%(current)s/%(total)s)"
LauncherStartingMessage = "ﾄｩｰﾝﾀｳﾝをｽﾀｰﾄしています…"
LauncherDownloadFile = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄ中…"
LauncherDownloadFileBytes = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄをﾀﾞｳﾝﾛｰﾄﾞ中: %(bytes)s"
LauncherDownloadFilePercent = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄをﾀﾞｳﾝﾛｰﾄﾞ中: %(percent)s%%"
LauncherDecompressingFile = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを解凍中…"
LauncherDecompressingPercent = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを解凍中: %(percent)s%%"
LauncherExtractingFile = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを抽出中…"
LauncherExtractingPercent = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを抽出中: %(percent)s%%"
LauncherPatchingFile = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを適用中…"
LauncherPatchingPercent = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを適用中: %(percent)s%%"
LauncherConnectProxyAttempt = "ﾄｩｰﾝﾀｳﾝに接続中： %s (proxy: %s) 試行中: %s"
LauncherConnectAttempt = "ﾄｩｰﾝﾀｳﾝに接続中: %s attempt %s"
LauncherDownloadServerFileList = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄ中…"
LauncherCreatingDownloadDb = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄ中…"
LauncherDownloadClientFileList = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄ中…"
LauncherFinishedDownloadDb = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄ中…"
LauncherStartingToontown = "ﾄｩｰﾝﾀｳﾝをスタート中…"
LauncherStartingGame = "ﾄｩｰﾝﾀｳﾝをスタート中…"
LauncherRecoverFiles = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄしています。ﾌｧｲﾙをﾘｶﾊﾞﾘｰ中…"
LauncherCheckUpdates = LauncherProgress + "のｱｯﾌﾟﾃﾞｰﾄを確認中…"
LauncherVerifyPhase = "ﾄｩｰﾝﾀｳﾝをｱｯﾌﾟﾃﾞｰﾄ中…"

# AvatarChoice.py
AvatarChoiceMakeAToon = "トゥーンを\nつくろう！"
AvatarChoicePlayThisToon = "このトゥーンを\nえらぶ"
AvatarChoiceSubscribersOnly = "\nいますぐ\nメンバーに\nなろう！" #★
AvatarChoiceDelete = "消す"
AvatarChoiceDeleteConfirm = "%s が削除されるよ。いいのかな？"
AvatarChoiceNameRejected = "なまえが\n使えないよ！"
AvatarChoiceNameApproved = "なまえが\n使えるよ！"
AvatarChoiceNameReview = "なまえを\nチエック中"
AvatarChoiceNameYourToon = "なまえを\nつけよう！"
AvatarChoiceDeletePasswordText = "%s が完全に削除されてしまうよ。 このトゥーンを削除する場合は、 パスワードを入力してね。"
AvatarChoiceDeleteConfirmText = "%(name)s が完全に削除されてしまうよ。このトゥーンを削除したい場合は、\"%(confirm)s\"と入力してから「ＯＫ」をクリックしてね。"
AvatarChoiceDeleteConfirmUserTypes = "削除"
AvatarChoiceDeletePasswordTitle = "このトゥーンを削除しますか？"
AvatarChoicePassword = "パスワード"
AvatarChoiceDeletePasswordOK = lOK
AvatarChoiceDeletePasswordCancel = lCancel
AvatarChoiceDeleteWrongPassword = "パスワードが合っていないようだよ。このトゥーンを削除したい場合は、キミのパスワードを入力してね。"
AvatarChoiceDeleteWrongConfirm = "入力されたものは間違っているよ。%(name)sを削除したい場合は\"%(confirm)s\"と入力してから「ＯＫ」をクリックしてね。引用符（" "）は入力しないでください。削除したくなくなった場合は「キャンセル」をクリックしてね。"

# AvatarChooser.py
AvatarChooserPickAToon = "プレイするトゥーンをえらぶ"
AvatarChooserQuit = lQuit

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "ディズニー・インターネット・グループ・カスタマーセンター（%s）にごれんらくください。"
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nお問い合わせ等は、ディズニー・インターネット・グループ・カスタマーセンター（%s）までお願いします。"
TTAccountIntractibleError = "エラーが発生しました。"

# DateOfBirthEntry.py　★「月」だけでなく「年」や「日」にも単位をつけたい
DateOfBirthEntryMonths = ['1月', '2月', '3月', '4月', '5月', '6月',
                          '7月', '8月', '9月', '10月', '11月', '12月',]
DateOfBirthEntryDefaultLabel = "生年月日"


# AchievePage.py
AchievePageTitle = "アチーブメント\n(近日公開予定)"

# PhotoPage.py
PhotoPageTitle = "写真\n(近日公開予定)"

# BuildingPage.py
BuildingPageTitle = "ビル\n(近日公開予定)"

# InventoryPage.py
InventoryPageTitle = "ギャグ"
InventoryPageDeleteTitle = "ギャグを削除する"
InventoryPageTrackFull = "%sのギャグトラックはすべてそろってます。"
InventoryPagePluralPoints = "%(trackName)sのポイントを%(numPoints)sかせげば、新しい\n%(trackName)sのギャグを得ることができます。"
InventoryPageSinglePoint = "%(trackName)sのポイントを%(numPoints)sかせげば、新しい\n%(trackName)sのギャグを得ることができます。"
InventoryPageNoAccess = "まだ%sのトラックにはアクセスできません。"

# NPCFriendPage.py
NPCFriendPageTitle = "ＳＯＳトゥーン"

# NPCFriendPanel.py
NPCFriendPanelRemaining = "のこり%s回"

# EventsPage.py
#もともとMonthsに“1月”という表現だったので画面上で「1月月」と
#ならないようフォーマットを変更しました。2009年11月19日
PartyDateFormat = "%(yyyy).4d年%(mm)s%(dd)d日"
PartyTimeFormat = "%d:%.2d %s" # 1:45 pm
PartyTimeFormatMeridiemAM = "AM"
PartyTimeFormatMeridiemPM = "PM"
PartyCanStart = "パーティータイム！トゥーンガイドのしゅさい者ページを開いて「パーティーを始める」をクリック！"
PartyHasStartedAcceptedInvite = '%s パーティーが始まったよ！トゥーンガイドの参加者ページを開いて「パーティーにゆく」をクリック！'
PartyHasStartedNotAcceptedInvite = '%s パーティーが始まったよ！しゅさい者にワープしても参加できるよ。'

EventsPageName = "イベント"
EventsPageCalendarTabName = "カレンダー"
EventsPageCalendarTabParty = "パーティー"
EventsPageToontownTimeIs = "トゥーンタウン時間"
EventsPageConfirmCancel = "キャンセルするとジェリービーン%d%%が返ってきます。本当にパーティーをキャンセルする？"
EventsPageCancelPartyResultOk = "キミのパーティーはキャンセルされました。ジェリービーン%dが返ってきました。"
EventsPageCancelPartyResultError = "残念、キミのパーティーはキャンセルされませんでした。"
EventsPageTooLateToStart = "残念、パーティーを始めるにはおそすぎたよ。キャンセルして次のプランを立てよう。"
EventsPagePublicPrivateChange = "キミのパーティーのプライバシー設定を変えるよ..."
EventsPagePublicPrivateNoGo = "ごめんね、今はパーティーのプライバシー設定は変えられません。"
EventsPagePublicPrivateAlreadyStarted = "ごめんね、キミのパーティーはもう始まっているからプライバシー設定は変えられません。"
EventsPageHostTabName = "しゅさい者" # displayed on the physical tab
EventsPageHostTabTitle = "次のパーティー" # banner text displayed across the top
EventsPageHostTabTitleNoParties = "次のパーティー　なし"
EventsPageHostTabDateTimeLabel = "次のパーティーは%s、トゥーンタウン時間の%sからです。"
EventsPageHostingTabNoParty = "パーティーを開くには\nプレイグラウンドの\nパーティーゲートにゆこう！"
EventsPageHostTabPublicPrivateLabel = "このパーティーは："
EventsPageHostTabToggleToPrivate = "プライベート"
EventsPageHostTabToggleToPublic = "だれでも"
EventsPageHostingTabGuestListTitle = "ゲスト"
EventsPageHostingTabActivityListTitle = "アクティビティ"
EventsPageHostingTabDecorationsListTitle = "デコレーション"
EventsPageHostingTabPartiesListTitle = "しゅさい者"
EventsPageHostTabCancelButton = "パーティーをキャンセル"
EventsPageGoButton = "パーティーを\n始める"
EventsPageGoBackButton = "パーティーに\nようこそ!"
EventsPageInviteGoButton = "パーティーに\n行こう！"
EventsPageUnknownToon = "知らないトゥーン"

EventsPageInvitedTabName = "招待"
EventsPageInvitedTabTitle = "招待状"
EventsPageInvitedTabInvitationListTitle = "招待リスト"
EventsPageInvitedTabActivityListTitle = "アクティビティ"
EventsPageInvitedTabTime = "トゥーンタウン時間　%s %s"

EventsPageNewsTabName = "ニュース"
EventsPageNewsTabTitle = "ニュース"
EventsPageNewsDownloading= "ニュースをひょうじ中..."
EventsPageNewsUnavailable = "チップとデールがいんさつきをこわしちゃった！ニュースはとどかないよ。"
EventsPageNewsPaperTitle = "トゥーンタウン・マガジン"
EventsPageNewsLeftSubtitle = "ジェリービーンで買える！"
EventsPageNewsRightSubtitle = "トゥーン暦 2009年　創刊"

# InvitationSelection.py
SelectedInvitationInformation = "%sが %sのトゥーンタウン時間の%sからパーティーを開くよ。"

# PartyPlanner.py
PartyPlannerNextButton = "つづける"
PartyPlannerPreviousButton = "もどる"
PartyPlannerWelcomeTitle = "トゥーンタウン パーティープランナー"
PartyPlannerInstructions = "パーティーを開こう！まずは下の矢印からプランを立ててみよう。"
PartyPlannerDateTitle = "パーティーの日付は？"
PartyPlannerTimeTitle = "パーティーは何時から？"
PartyPlannerGuestTitle = "ゲストを選んでね"
PartyPlannerEditorTitle = "パーティーの場所・デコレーション\n・アクティビティを決めよう"
PartyPlannerConfirmTitle = "招待状をえらんでね"
PartyPlannerConfirmTitleNoFriends = "キミのパーティープラン"
PartyPlannerTimeToontown = "トゥーンタウン"
PartyPlannerTimeTime = "時刻"
PartyPlannerTimeRecap = "パーティーの日時"
PartyPlannerPartyNow = "今すぐ"
PartyPlannerTimeToontownTime = "トゥーンタウン時間："
PartyPlannerTimeLocalTime = "日本時間："
PartyPlannerPublicPrivateLabel = "このパーティーは…"
PartyPlannerPublicDescription = "だれでも\n参加できます"
PartyPlannerPrivateDescription = "招待された\nトゥーンだけ\n参加できます"
PartyPlannerPublic = "パブリック"
PartyPlannerPrivate = "プライベート"
PartyPlannerCheckAll = "全部\nえらぶ"
PartyPlannerUncheckAll = "全部\nやめる"
PartyPlannerDateText = "日付"
PartyPlannerTimeText = "時刻"
PartyPlannerTTTimeText = "トゥーンタウン時刻"
PartyPlannerEditorInstructionsIdle = "買いたいアクティビティやデコレーションをクリックしてね。"
PartyPlannerEditorInstructionsClickedElementActivity = "「買う」をクリックするか、ほしいアクティビティをマップにドラッグしてね。"
PartyPlannerEditorInstructionsClickedElementDecoration = "「買う」をクリックするか、ほしいデコレーションをマップにドラッグしてね。"
PartyPlannerEditorInstructionsDraggingActivity = "ほしいアクティビティをマップにドラッグしてね。"
PartyPlannerEditorInstructionsDraggingDecoration = "ほしいデコレーションをマップにドラッグしてね。"
PartyPlannerEditorInstructionsPartyGrounds = "アイテムを動かすには、マップ上でドラッグしてね。"
PartyPlannerEditorInstructionsTrash = "アクティビティやデコレーションをさくじょする時は、ここにドラッグしてね"
PartyPlannerEditorInstructionsNoRoom = "そのアクティビティに十分なスペースがありません。"
PartyPlannerEditorInstructionsRemoved = "%(removed)sは%(added)sが追加されたので削除されました。"
PartyPlannerBeans = "ビーン"
PartyPlannerTotalCost = "トータルコスト:\n%d ビーン"
PartyPlannerSoldOut = "売切れ"
PartyPlannerBuy = "買う"
PartyPlannerPaidOnly = "フルアクセス専用"
PartyPlannerPartyGrounds = "パーティー・グラウンド・マップ"
PartyPlannerOkWithGroundsLayout = "パーティーのアクティビティやデコレーションのプランはこれでOKかな？"
PartyPlannerChooseFutureTime = "今より先の時間を指定してね。"
PartyPlannerInviteButton = "招待状を送る"
PartyPlannerInviteButtonNoFriends = "パーティーを計画する"
PartyPlannerBirthdayTheme = "誕生日"
PartyPlannerGenericMaleTheme = "スター"
PartyPlannerGenericFemaleTheme = "フラワー"
PartyPlannerRacingTheme = "レーシング"
PartyPlannerGuestName = "ゲスト名"
PartyPlannerClosePlanner = "プランナーを閉じる"
PartyPlannerConfirmationAllOkTitle = "おめでとう！"
PartyPlannerConfirmationAllOkText = "キミのパーティーが設定されて、招待状が送られました。\n楽しみだね！"
PartyPlannerConfirmationAllOkTextNoFriends = "キミのパーティーが設定されました。\n楽しみだね！"
PartyPlannerConfirmationErrorTitle = "あれれ…"
PartyPlannerConfirmationValidationErrorText = "あれれ…、このパーティー設定には問題があるみたい。\n戻ってもう一度かくにんしてみてね。"
PartyPlannerConfirmationDatabaseErrorText = "ごめん、キミの情報が正しくほぞんできなかったみたい。\n後でもう一度ためしてね。\nジェリービーンはそのままだよ。"
PartyPlannerConfirmationTooManyText = "すでにパーティーを設定ずみみたい…。\nもし新しいパーティーを開きたい時は、\n先に今あるパーティーをキャンセルしてね。"
PartyPlannerInvitationThemeWhatSentence = "%sパーティーに招待するよ！来てくれるかい、%s"
PartyPlannerInvitationThemeWhatSentenceNoFriends = "%sパーティーを開くんだ！来てくれるかい、%s"
PartyPlannerInvitationThemeWhatActivitiesBeginning = "アクティビティ　"
PartyPlannerInvitationWhoseSentence = "%sのパーティー"
PartyPlannerInvitationTheme = "テーマ"
PartyPlannerInvitationWhenSentence = "%s、\n トゥーンタウン時間の%sからスタート！\n来てくれたらうれしいな♪"
PartyPlannerInvitationWhenSentenceNoFriends = "%s、\n トゥーンタウン時間の%sからスタート！\nみんなで楽しもう♪"
PartyPlannerComingSoon = "近日公開"
PartyPlannerCantBuy= "買えないよ"
PartyPlannerGenericName = "パーティープランナー"

# DistributedPartyJukeboxActivity.py
PartyJukeboxOccupied = "まだだれかがジュークボックスを使用中。また後でためそう…"
PartyJukeboxNowPlaying = "その曲は今流れている曲だよ"

# Jukebox Music
MusicEncntrGeneralBg = "コグとのそうぐう"
MusicTcSzActivity = "トゥーントリアル・メドレー"
MusicTcSz = "タウンのさんぽ"
MusicCreateAToon = "タウンとニュー・トゥーン"
MusicTtTheme = "トゥーンタウンのテーマ"
MusicMinigameRace = "ゆっくり、しっかり…"
MusicMgPairing = "おぼえてる？"
MusicTcNbrhood = "トゥーンタウン・セントラル"
MusicMgDiving = "宝のララバイ"
MusicMgCannonGame = "キャノン砲、発射！"
MusicMgTwodgame = "ランニング・トゥーン"
MusicMgCogthief = "コグをとらえろ！"
MusicMgTravel = "トラベリング・ミュージック"
MusicMgTugOWar = "ひっぱれ！"
MusicMgVine = "ジャングル・ジャンプ"
MusicMgIcegame = "止まらない～！"
MusicMgToontag = "トロリーゲーム・メドレー"
MusicMMatchBg2 = "マッチ・ミニー"
MusicMgTarget = "ただ今タウン上空…"
MusicFfSafezone = "ファニー・ファーム"
MusicDdSz = "ワドリング・ウェイ"
MusicMmNbrhood = "ミニーのメロディーランド"
MusicGzPlaygolf = "今週末どうですか！"
MusicGsSz = "グーフィー・スピードウェイ"
MusicOzSz = "ドングリひろば"
MusicGsRaceCc = "ダウンタウン・ドライビング"
MusicGsRaceSs = "レディ、セット、Go！"
MusicGsRaceRr = "ルート66"
MusicGzSz = "パット・パット・ポルカ"
MusicMmSz = "ストリート・ダンサー"
MusicMmSzActivity = "ソプラノはまかせて"
MusicDdNbrhood = "ドナルドのハトバ"
MusicGsKartshop = "Mr. グーフィーレンチ"
MusicDdSzActivity = "海辺の小屋"
MusicEncntrGeneralBgIndoor = "ビルの中"
MusicTtElevator = "上へまいりま～す"
MusicEncntrToonWinningIndoor = "トゥーンよ、集結せよ"
MusicEncntrGeneralSuitWinningIndoor = "コグタストロフ！"
MusicTbNbrhood = "ブルルル…"
MusicDlNbrhood = "ドナルドのドリームランド"
MusicDlSzActivity = "ヒツジがいっぴき…"
MusicDgSz = "花のワルツ"
MusicDlSz = "ねてる…よね？"
MusicTbSzActivity = "ス・ノープロブレム！"
MusicTbSz = "がたがた、ブルブル…"
MusicDgNbrhood = "デイジー・ガーデン"
MusicEncntrHallOfFame = "めいよトゥーン！"
MusicEncntrSuitHqNbrhood = "ダラーズ アンド センツ"
MusicChqFactBg = "コグ・ファクトリー"
MusicCoghqFinale = "トゥーン達の勝利"
MusicEncntrToonWinning = "おいくら？"
MusicEncntrSuitWinning = "お値引きします…"
MusicEncntrHeadSuitTheme = "ビッグ・ボス"
MusicLbJurybg = "せいしゅくに！"
MusicLbCourtyard = "バランスをとって"
MusicBossbotCeoV2 = "コグの指導者"
MusicBossbotFactoryV1 = "コグ・ワルツ"
MusicBossbotCeoV1 = "こまった上司"
MusicPartyOriginalTheme = "パーティー・タイム"
MusicPartyPolkaDance = "パーティー・ポルカ"
MusicPartySwingDance = "パーティー・スウィング"
MusicPartyWaltzDance = "パーティー・ワルツ"
MusicPartyGenericThemeJazzy = "パーティー・ジャズ"
MusicPartyGenericTheme = "パーティー・ジャングル"


# JukeBoxGui
JukeboxAddSong = "曲を\nついか"
JukeboxReplaceSong = "曲の\nいれかえ"
JukeboxQueueLabel = "次をプレイ："
JukeboxSongsLabel = "曲を選ぶ："
JukeboxClose = "OK"
JukeboxCurrentlyPlaying = "今、再生中…"
JukeboxCurrentlyPlayingNothing = "ジュークボックス 一時停止"
JukeboxCurrentSongNothing = "プレイリストに曲を追加"

PartyOverWarningNoName = "パーティーが終了しました。来てくれてありがとう！"
PartyOverWarningWithName = "%sのパーティーが終了しました。来てくれてありがとう！"
PartyCountdownClockText = "残り\n\n時間"
PartyTitleText = "%sのパーティー！" # what you see when you enter a party

PartyActivityConjunction = ", "
# Note : This dictionary is used to show the names of the activities in various
#        contexts.  If PartyGlobals.ActivityIds is changed, this list must be
#        updated with new indices.
PartyActivityNameDict = {
    0 : {
        "generic" : "20曲入り\nジュークボックス",
        "invite" : "20曲入りジュークボックス",
        "editor" : "ジュークボックス - 20",
        "description" : "キミだけの20曲入りジュークボックスを楽しもう！"
    },
    1 : {
        "generic" : "パーティー・キャノン",
        "invite" : "パーティー・キャノン",
        "editor" : "キャノン",
        "description" : "みんなでキャノンゲームを楽しもう♪"
    },
    2 : {
        "generic" : "トランポリン",
        "invite" : "トランポリン",
        "editor" : "トランポリン",
        "description" : "ジェリービーンを集めながらどこまでもジャンプ！"
    },
    3 : {
        "generic" : "パーティー・キャッチ",
        "invite" : "パーティー・キャッチ",
        "editor" : "パーティー・キャッチ",
        "description" : "いたぁ～いカナドコをよけて、甘～いフルーツをキャッチ！"
    },
    4 : {
        "generic" : "10ムーブ\nダンスフロア",
        "invite" : "10ムーブダンスフロア",
        "editor" : "ダンスフロア - 10",
        "description" : "10種類のムーブをくみあわせてスタイリッシュにダンス♪"
    },
    5 : {
        "generic" : "パーティー・つなひき",
        "invite" : "パーティー・つなひき",
        "editor" : "つなひき",
        "description" : "最大４対４のつなひきマッドネス！"
    },
    6 : {
        "generic" : "プレイベート花火大会",
        "invite" : "プレイベート花火大会",
        "editor" : "花火大会",
        "description" : "あこがれのプライベート花火大会を開こう！"
    },
    7 : {
        "generic" : "パーティー・クロック",
        "invite" : "パーティー・クロック",
        "editor" : "パーティー・クロック",
        "description" : "パーティーの残り時間をカウントダウンしてくれるよ。"
    },
    8 : {
        "generic" : "40曲入り\nジュークボックス",
        "invite" : "20曲入りジュークボックス",
        "editor" : "ジュークボックス - 40",
        "description" : "40曲入りなら大好きな曲を全部カバーできるね！"
    },
    9 : {
        "generic" : "20ムーブ\nダンスフロア",
        "invite" : "20ムーブダンスフロア",
        "editor" : "ダンスフロア - 20",
        "description" : "20種類のムーブを使いこなせば、キミはもうダンスマスター♪"
    },    
}

# Note : This dictionary is used to show the names of the decorations in various
#        contexts.  If PartyGlobals.DecorationIds is changed, this list must be
#        updated with new indices.
PartyDecorationNameDict = {
    0 : {
        "editor" : "ふうせん用のおもり",
        "description" : "飛んでいっちゃったらイヤだものね！",
    },
    1 : {
        "editor" : "メイン・ステージ",
        "description" : "ふうせん、ホシ、他にほしいものは？",
    },
    2 : {
        "editor" : "パーティー用リボン",
        "description" : "パーティーではやっぱりおしゃれに☆",
    },
    3 : {
        "editor" : "ケーキ",
        "description" : "おいしいヨ♪",
    },
    4 : {
        "editor" : "パーティー・キャッスル",
        "description" : "トゥーンのおうちがお城に…！？",
    },
    5 : {
        "editor" : "山積みのギフト",
        "description" : "本日のお土産で～す。",
    },
    6 : {
        "editor" : "ストリーマー・ホーン",
        "description" : "ゆかいで楽しいホーンだよ。",
    },
    7 : {
        "editor" : "パーティー・ゲート",
        "description" : "カラフル＆ポップ！もりあがるよね♪",
    },
    8 : {
        "editor" : "ノイズ・メーカー",
        "description" : "ぺちゃくちゃ、ざわざわ…！",
    },
    9 : {
        "editor" : "かざぐるま",
        "description" : "みんなが大好きなカラフルなかざぐるま。",
    },
    10 : {
        "editor" : "ギャグ・グローブ",
        "description" : "デザインがすばらしいギャグと星のグローブ",
    },
    11 : {
        "editor" : "JBバナー",
        "description" : "ジェリービーンのバナーも一味違っていい感じ☆",
    },
    12 : {
        "editor" : "ギャグのケーキ",
        "description" : "これがないとパーティーがもりあがらないよね。",
    },
}

ActivityLabel = "コスト - アクティビティ名"
PartyDoYouWantToPlan = "新しくパーティーを\n設定する？"
PartyPlannerOnYourWay = "楽しいパーティーにしてみんなともりあがろう！"
PartyPlannerMaybeNextTime = "また次のきかいに設定しよう。またね！"
PartyPlannerHostingTooMany = "一度に１つのパーティーしかプランできません。"
PartyPlannerOnlyPaid = "パーティーのプランはフルアクセス・メンバー専用です。"
PartyPlannerNpcComingSoon = "もうすぐパーティーが設定できるようになるよ。"
PartyPlannerNpcMinCost = "パーティーのプランには、最低%dコのジェリービーンが必要です。"

# Party Gates
PartyHatPublicPartyChoose = "次のパブリック・パーティー(参加自由)に行ってみる？"
PartyGateTitle = "パブリック\n・パーティー"
PartyGateGoToParty = "パーティーに\n行く！"
PartyGatePartiesListTitle = "しゅさい者"
PartyGatesPartiesListToons = "トゥーン"
PartyGatesPartiesListActivities = "アクティビティ"
PartyGatesPartiesListMinLeft = "残り時間(分)"
PartyGateLeftSign = "いらっしゃい！"
PartyGateRightSign = "パブリック\n・パーティー"
PartyGatePartyUnavailable = "残念、そのパーティーにはもう参加できないよ。"
PartyGatePartyFull = "残念、そのパーティーはもう満席だよ。"
PartyGateInstructions = 'しゅさい者をクリックして、"パーティーに行く！"をクリックしてね。'

# DistributedPartyActivity.py
PartyActivityWaitingForOtherPlayers = "他のトゥーンが参加するのを待っています..."
PartyActivityPleaseWait = "ちょっと待ってね ..."
DefaultPartyActivityTitle = "パーティー・ゲーム名"
DefaultPartyActivityInstructions = "パーティー・ゲーム あそび方"
PartyOnlyHostLeverPull = "しゅさい者しかこのゲームを開始できません。"
PartyActivityDefaultJoinDeny = "残念、今は参加できません。"
PartyActivityDefaultExitDeny = "今はこのクティビティを中止できません。"

# JellybeanRewardGui.py
PartyJellybeanRewardOK = "OK"

# DistributedPartyCatchActivity.py
PartyCatchActivityTitle = "パーティー・キャッチ アクティビティ"
PartyCatchActivityInstructions = "たくさんのフルーツをキャッチしよう。%(badThing)sには気をつけてね。"
PartyCatchActivityFinishPerfect = "パーフェクト・ゲーム！"
PartyCatchActivityFinish = "よくやったね！"
PartyCatchActivityExit 	      = '終了'
PartyCatchActivityApples      = 'リンゴ'
PartyCatchActivityOranges     = 'オレンジ'
PartyCatchActivityPears       = '西洋ナシ'
PartyCatchActivityCoconuts    = 'ココナツ'
PartyCatchActivityWatermelons = 'スイカ'
PartyCatchActivityPineapples  = 'パイナップル'
PartyCatchActivityAnvils      = 'カナドコ'
PartyCatchStarted = "ゲームが始まってるよ。いそごう！"
PartyCatchCannotStart = "ゲームが開始されませんでした。"
PartyCatchRewardMessage = "キャッチしたフルーツ： %s\n\nジェリービーン: %sコ"

# DistributedPartyDanceActivity.py
PartyDanceActivityTitle = "パーティー ダンス・フロア"
PartyDanceActivityInstructions = "3つ以上の矢印キーの組合せでムーブをきめよう！ムーブは10種類あるよ。全部見つけてみよう。"
PartyDanceActivity20Title = "パーティー ダンス・フロア"
PartyDanceActivity20Instructions = "3つ以上の矢印キーの組合せでムーブをきめよう！ムーブは20種類あるよ。全部見つけてみよう。"

DanceAnimRight = "ライト"
DanceAnimReelNeutral = "フィッシャー・トゥーン"
DanceAnimConked = "ヘッドボブ"
DanceAnimHappyDance = "ハッピーダンス"
DanceAnimConfused = "ベリー・ディジー"
DanceAnimWalk = "ムーン・ウォーキング"
DanceAnimJump = "ジャンプ！"
DanceAnimFirehose = "ファイヤートゥーン"
DanceAnimShrug = "フー・ノウズ？"
DanceAnimSlipForward = "フォール"
DanceAnimSadWalk = "タイアード"
DanceAnimWave = "ハロー・グッドバイ！"
DanceAnimStruggle = "シャッフル・ホップ"
DanceAnimRunningJump = "ランニング・トゥーン"
DanceAnimSlipBackward = "バック・フォール"
DanceAnimDown = "ダウン"
DanceAnimUp = "アップ"
DanceAnimGoodPutt = "パット"
DanceAnimVictory = "ビクトリー・ダンス"
DanceAnimPush = "マイム・トゥーン"
DanceAnimAngry = "ロックンロール"
DanceAnimLeft = "レフト"

# DistributedPartyCannonActivity.py
PartyCannonActivityTitle = "パーティー・キャノン"
PartyCannonActivityInstructions = "雲に当たると色が変わってはね返されるよ。飛んでる間は矢印キーでコントロールしてみてね。"
PartyCannonResults = "%dコのジェリービーンをゲット！\n\nヒットした雲の数： %d"

# DistributedPartyFireworksActivity.py
FireworksActivityInstructions = "\"Page Up(PgUp)キー\"を押すと空を見上げられるよ。"
FireworksActivityBeginning = "プライベート花火大会が始まるよ！楽しんでね！！"
FireworksActivityEnding = "楽しんでもらえたかな！"
PartyFireworksAlreadyActive = "花火大会がもう始まってるよ。"
PartyFireworksAlreadyDone = "花火大会が終了しました。"

# DistributedPartyTrampolineActivity.py
PartyTrampolineJellyBeanTitle = "ジェリービーン・トランポリン"
PartyTrampolineTricksTitle = "トリック・トランポリン"
PartyTrampolineActivityInstructions = "コントロール(Ctrl)キーでジャンプ。\n\nトゥーンが一番低い位置に来た時にジャンプするとより高くとべるよ。"
PartyTrampolineActivityOccupied = "トランポリンは使用中です。"
PartyTrampolineQuitEarlyButton = "おりる"
PartyTrampolineBeanResults = "ジェリービーンを%dコかくとく"
PartyTrampolineBonusBeanResults = "ジェリービーンを%dコ ＋ %dコ(ビッグ・ビーン　ボーナス)をかくとく"
PartyTrampolineTopHeightResults = "キミのベスト・ジャンプ： %dメートル"
PartyTrampolineTimesUp = "ゲーム終了！"
PartyTrampolineReady = "ようい..."
PartyTrampolineGo = "スタート！"
PartyTrampolineBestHeight = "今までのベスト・ジャンプ： \n%s\n%dメートル"
PartyTrampolineNoHeightYet = "どこまで高く\nとべるかな？"

# DistributedPartyTugOfWarActivity.py
PartyTugOfWarJoinDenied = "ごめん、今はつなひきには参加できないよ。"
PartyTugOfWarTeamFull = "残念、このチームはもう満員です。"
PartyTugOfWarExitButton = "おりる"
PartyTugOfWarWaitingForMore = "他のトゥーンを待っています。" # extra spaces on purpose given the blocky font
PartyTugOfWarWaitingToStart = "スタート待ち…"
PartyTugOfWarWaitingForOtherPlayers = "他のトゥーンを待っています。"
PartyTugOfWarReady = "ようい..."
PartyTugOfWarGo = "スタート！"
PartyTugOfWarGameEnd = "良い  ゲームだったね！"
PartyTugOfWarGameTie = "ひき  わけ！"
PartyTugOfWarRewardMessage = "ジェリービーン%dコかくとく。やったね！"
PartyTugOfWarTitle = "パーティー・つなひき"

# CalendarGuiMonth.py
CalendarShowAll = "ぜんぶ見る"
CalendarShowOnlyHolidays = "お休みだけ見る"
CalendarShowOnlyParties = "パーティーだけ見る"

# CalendarGuiDay.py
CalendarEndsAt = "おわる時間 "
CalendarStartedOn = "はじまる時間 "
CalendarEndDash = "おわり-"
CalendarEndOf = "おわりは "
CalendarPartyGetReady = "じゅんびしよう！"
CalendarPartyGo = "パーティーだ♪"
CalendarPartyFinished = "おわりだよ..."
CalendarPartyCancelled = "中止"
CalendarPartyNeverStarted = "スタートできません"

# MapPage.py
MapPageTitle = "地図"
MapPageBackToPlayground = "プレイグラウンドに戻る"
MapPageBackToCogHQ = "コグ本部に戻る"
MapPageGoHome = "家に帰る"
# hood name, street name
MapPageYouAreHere = " %s\n%s"
MapPageYouAreAtHome = "\n自分のおうちにいます"
MapPageYouAreAtSomeonesHome = "%s のおうちにいます"
MapPageGoTo = "%s\nへ行く"

# OptionsPage.py
OptionsPageTitle = "オプション"
OptionsPagePurchase = "今すぐ申し込む"
OptionsPageLogout = "ログアウト"
OptionsPageExitToontown = "ゲームを終了する"
OptionsPageMusicOnLabel = "おんがく： あり"
OptionsPageMusicOffLabel = "おんがく： なし"
OptionsPageSFXOnLabel = "こうかおん： あり"
OptionsPageSFXOffLabel = "こうかおん： なし"
OptionsPageToonChatSoundsOnLabel = "チャットおん： あり"
OptionsPageToonChatSoundsOffLabel = "チャットおん： なし"
OptionsPageFriendsEnabledLabel = "ともだち：うけつける"
OptionsPageFriendsDisabledLabel = "ともだち：うけつけない"
OptionsPageSpeedChatStyleLabel = "スピードチャットの色"
OptionsPageDisplayWindowed = "ウインドウ・モード"
OptionsPageSelect = "選択する"
OptionsPageToggleOn = "きりかえ"
OptionsPageToggleOff = "きりかえ"
OptionsPageChange = "へんこう"
OptionsPageDisplaySettings = "かいぞうど： %(screensize)s、 %(api)s"
OptionsPageDisplaySettingsNoApi = "かいぞうど: %(screensize)s"
OptionsPageExitConfirm = "トゥーンタウン・\nオンラインを\n終了しますか？"

DisplaySettingsTitle = "がめんひょうじせってい"
DisplaySettingsIntro = "トゥーンタウン・オンラインのひょうじのせっていをします。（おうちのひとと見てね）\nトゥーンタウン・オンラインでのテキストやグラフィックレベルを向上するため、画面解像度を高めに設定してもかまいませんが、ご使用のグラフィックカードにより、いくつかの設定でゲームのスピードが遅くなったり、全く動かなくなったりする可能性がありますのであらかじめご了承ください。 "
DisplaySettingsIntroSimple = "トゥーンタウンでのテキストやグラフィックレベルを向上するため、画面解像度を高めに設定してもかまいませんが、ご使用のグラフィックカードにより、いくつかの設定は、ゲームのスピードが遅くなったり、全く動かなくなったりする可能性があります。"

DisplaySettingsApi = "グラフィックス API:"
DisplaySettingsResolution = "かいぞうど："
DisplaySettingsWindowed = "ウインドウ・モード"
DisplaySettingsFullscreen = "フルスクリーン・モード"
DisplaySettingsApply = "OK"
DisplaySettingsCancel = "キャンセル"
DisplaySettingsApplyWarning = "ＯＫボタンを押すと、表示設定が変わります。 新しい設定がコンピュータ上で正常に表示されない場合、自動的に%s秒後、元の状態に戻ります。"
DisplaySettingsAccept = "これでよろしければＯＫボタンを押してください。何も押さないと、%s秒後に自動的に変更する前の設定に戻ります。"
DisplaySettingsRevertUser = "前の表示設定に戻しました。"
DisplaySettingsRevertFailed = "選択された表示設定はお客様のコンピュータでは作動しません。前の表示設定が復帰しました。"

# TrackPage.py
TrackPageTitle = "ギャグ・トラック・トレーニング"
TrackPageShortTitle = "ギャグ\nトレーニング"
TrackPageSubtitle = "トゥーンタスクをこなして、新しい種類のギャグをおぼえよう！"
TrackPageTraining = "%s ギャグを使用するトレーニングをしています。\n１６コマ分のタスクをすべて終了すると、\n バトルで%sギャグを使えるようになります。"
TrackPageClear = "現在、どのトラックのトレーニングも始めていません。"
TrackPageFilmTitle = "%s\nトレーニング\nフィルム"
TrackPageDone = "おわり"

# QuestPage.py
QuestPageToonTasks = "トゥーンタスク"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageDelivery = "%s\nへ： %s\n  %s\n  %s\n  %s\n\nから： %s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName, npcName
#QuestPageVisit = "%s %s\n  %s\n  %s\n  %s\n\nから：%s"
# questName, toNpcName, toNpcBuilding, toNpcStreetName, toNpcLocationName
# Choose between trackA and trackB.
#
# To choose, go see:
#   Flippy
#   Town Hall
#   Playground
#   Toontown Central
#QuestPageTrackChoice = "%s\n\n選びに、 \n  %s\n  %s\n  %s\n  %sn　%sへ行ってね。"
# questName, npcName, buildingName, streetName, locationName
QuestPageChoose = "選んでね"
QuestPageLocked = "へいさ中"
# building name, street name, Npc location
QuestPageDestination = "%s\n%s\n%s"
# npc name, building name, street name, Npc location
QuestPageNameAndDestination = "%s\n%s\n%s\n%s"

QuestPosterHQOfficer = lHQOfficerM
QuestPosterHQBuildingName = lToonHQ
QuestPosterHQStreetName = "どの通りでも"
QuestPosterHQLocationName = "どのエリアでも"

QuestPosterTailor = "したてやさん"
QuestPosterTailorBuildingName = "ようふくや"
QuestPosterTailorStreetName = "どのプレイグラウンドでも"
QuestPosterTailorLocationName = "どのエリアでも"
QuestPosterPlayground = "プレイグラウンドで"
QuestPosterAtHome = "おうちで"
QuestPosterInHome = "おうちの中で"
QuestPosterOnPhone = "電話で"
QuestPosterEstate = "おうちで"
QuestPosterAnywhere = "どこでも" #★
QuestPosterAuxTo = "→"
QuestPosterAuxFrom = "←"
QuestPosterAuxFor = "" #★
QuestPosterAuxOr = "または"
QuestPosterAuxReturnTo = "" #★
QuestPosterLocationIn = " in "
QuestPosterLocationOn = " in "
QuestPosterFun = "楽しいよ！"
QuestPosterFishing = "つりにいく"
QuestPosterComplete = "完了"

# ShardPage.py
ShardPageTitle = "ロビー"
ShardPageHelpIntro = "それぞれのロビーは、\nトゥーンタウンの世界の\nコピーなんだ。"
ShardPageHelpWhere = "いま、君は\"%s\" にいるよ。"
ShardPageHelpWelcomeValley = "いま、君は\"%s\"の\"ｳｪﾙｶﾑﾊﾞﾚｰ\"にいるよ。"
ShardPageHelpMove = "\n\n新しいロビーに行くには、ロビーの名前をクリックしてね。"

ShardPagePopulationTotal = "全トゥーンタウンの人口:\n%d"
ShardPageScrollTitle = "名前            人口"
ShardPageLow = "すいてる"
ShardPageMed = "てきせつ"
ShardPageHigh = "こんざつ"
ShardPageChoiceReject = "このロビーはこんざつしています。他をえらんで下さい。"

# SuitPage.py
SuitPageTitle = Cog + "ギャラリー"
SuitPageMystery = "???"
SuitPageQuota = "%s / %s"
SuitPageCogRadar = "%s体発見！" #★
SuitPageBuildingRadarS = "%s 建物"
SuitPageBuildingRadarP = "%s 建物"

# DisguisePage.py
DisguisePageTitle = Cog + "へんそう\nパーツ"
DisguisePageMeritAlert = "いよいよ昇格！"
DisguisePageCogLevel = "レベル%s"
DisguisePageMeritFull = "満タン"

# FishPage.py
FishPageTitle = "魚のタンク"
FishPageTitleTank = "魚のタンク"
FishPageTitleCollection = "魚のコレクション"
FishPageTitleTrophy = "トロフィー"
FishPageWeightStr = "重さ: "
FishPageWeightLargeS = "%dﾊﾟｳﾝﾄﾞ"
FishPageWeightLargeP = "%dﾊﾟｳﾝﾄﾞ"
FishPageWeightSmallS = "%dｵﾝｽ"
FishPageWeightSmallP = "%dｵﾝｽ"
FishPageWeightConversion = 16
FishPageValueS = "ジェリービーン%d個分"
FishPageValueP = FishPageValueS
FishPageCollectedTotal = "集めた魚: %d / %d種類"
FishPageRodInfo = "%s釣りざお：\n%d～%dパウンドの\n重さまでＯＫ"
FishPageTankTab = "タンク"
FishPageCollectionTab = "アルバム"
FishPageTrophyTab = "トロフィー"

FishPickerTotalValue = "バケツ：%s / %s匹\nジェリービーン%d個相当"

UnknownFish = "？？？"

FishingRod = "%s釣りざお"
FishingRodNameDict = {
    0 : "小枝の",
    1 : "竹の",
    2 : "木の",
    3 : "鉄の",
    4 : "金の",
    }
FishTrophyNameDict = {
    0 : "クマノミ",
    1 : "キンギョ",
    2 : "コイ",
    3 : "トビウオ",
    4 : "サメ",
    5 : "カジキ",
    6 : "シャチ",
    }

# GardenPage.py #localize
GardenPageTitle = "ガーデニング"
GardenPageTitleBasket = "フラワー・バスケット"
GardenPageTitleCollection = "フラワー・アルバム"
GardenPageTitleTrophy = "ガーデニング・トロフィー"
GardenPageTitleSpecials = "スペシャル"
GardenPageBasketTab = "バスケット"
GardenPageCollectionTab = "アルバム"
GardenPageTrophyTab = "トロフィー"
GardenPageSpecialsTab = "スペシャル"
GardenPageCollectedTotal = "あつめた花の種類: %d ／ %d"
GardenPageValueS = "かち: ジェリービーン%dコ分"
GardenPageValueP = "かち: ジェリービーン%dコ分"
FlowerPickerTotalValue = "バスケット: %s / %s\nかち： ジェリービーン%dコ分"
GardenPageShovelInfo = "ショベル%s: %d / %d\n"
GardenPageWateringCanInfo = "ジョウロ%s: %d / %d"

# KartPage.py
KartPageTitle = "カート"
KartPageTitleCustomize = "カートカスタマイズ"
KartPageTitleRecords = "個人ベスト"
KartPageTitleTrophy = "レーストロフィー"
KartPageCustomizeTab = "カスタマイズ"
KartPageRecordsTab = "レコード"
KartPageTrophyTab = "トロフィー"
KartPageTrophyDetail = "トロフィー %s : %s"
KartPageTickets = "チケット : "
KartPageConfirmDelete = "アクセサリーをけす？"

#plural
KartShtikerDelete = "さくじょ"
KartShtikerSelect = "カテゴリーをえらぶ"
KartShtikerNoAccessories = "アクセサリーなし"
KartShtikerBodyColors = "カートの色"
KartShtikerAccColors = "アクセサリーの色"
KartShtikerEngineBlocks = "ボンネットアクセサリー"
KartShtikerSpoilers = "トランクアクセサリー"
KartShtikerFrontWheelWells = "ぜんりんアクセサリー"
KartShtikerBackWheelWells = "こうりんアクセサリー"
KartShtikerRims = "リムアクセサリー"
KartShtikerDecals = "デカールアクセサリー"
#singluar
KartShtikerBodyColor = "カートの色"
KartShtikerAccColor = "アクセサリーの色"
KartShtikerEngineBlock = "ボンネット"
KartShtikerSpoiler = "トランク"
KartShtikerFrontWheelWell = "ぜんりん"
KartShtikerBackWheelWell = "こうりん"
KartShtikerRim = "リム"
KartShtikerDecal = "デカール"

KartShtikerDefault = "ひょうじゅん %s"
KartShtikerNo = "%s アクセサリーなし"

# QuestChoiceGui.py
QuestChoiceGuiCancel = lCancel

# TrackChoiceGui.py
TrackChoiceGuiChoose = "選ぶ"
TrackChoiceGuiCancel = "やめる"
TrackChoiceGuiHEAL = 'トゥーンアップ はバトルで他のトゥーンを元気にすることができるよ。'
TrackChoiceGuiTRAP = 'トラップは、おとりと一緒に使われる強力なギャグだよ。'
TrackChoiceGuiLURE = 'コグを気絶かトラップに引き込むため、おとりを使って。'
TrackChoiceGuiSOUND = 'サウンドは、コグすべてに効くけど、そんなに強力じゃないんだ。'
TrackChoiceGuiDROP = "ドロップ・ギャグは、大きなダメージを与えるけど、そんなに正確じゃないんだ。"

# EmotePage.py
EmotePageTitle = "表現・感情"
EmotePageDance = "次のダンスフォームをつくったよ:"
EmoteJump = "ジャンプする"
EmoteDance = "おどる"
EmoteHappy = "たのしい"
EmoteSad = "かなしい"
EmoteAnnoyed = "いらいらする"
EmoteSleep = "ねむい"

# TIP Page
TIPPageTitle = "TIP"

# SuitBase.py
SuitBaseNameWithLevel = "%(name)s\n%(dept)s\nレベル %(level)s"

# HealthForceAcknowledge.py
HealthForceAcknowledgeMessage = "ゲラゲラメーターがいっぱいになるまで、プレイグラウンドから出ることはできないよ！"

# InventoryNew.py
InventoryTotalGags = "ギャグごうけい\n%d / %d"
InventroyPinkSlips = "カイコツウチ %s 枚"
InventroyPinkSlip = "カイコツウチ１枚"
InventoryDelete = "すてる"
InventoryDone = "もどる"
InventoryDeleteHelp = "すてるギャグをクリックしてね。"
InventorySkillCredit = "スキルポイント: %s"
InventorySkillCreditNone = "スキルポイント: なし"
InventoryDetailAmount = "%(numItems)s / %(maxItems)s"
# acc, damage_string, damage, single_or_group
InventoryDetailData = "めいちゅうりつ: %(accuracy)s\n%(damageString)s: %(damage)s\n%(singleOrGroup)s"
InventoryTrackExp = "%(curExp)s / %(nextExp)s"
InventoryUberTrackExp = "あと%(nextExp)s!"
InventoryGuestExp = "ゲスト・リミット"
GuestLostExp = "ゲスト・リミットです。"
InventoryAffectsOneCog = "たいしょう:" + Cog +"一体"
InventoryAffectsOneToon = "たいしょう: 仲間一人"
InventoryAffectsAllToons = "たいしょう: 仲間全員"
InventoryAffectsAllCogs = "たいしょう:" + Cogs +"全体"
InventoryHealString = "かいふく"
InventoryDamageString = "ダメージ"
InventoryBattleMenu = "バトルメニュー"
InventoryRun = "にげる"
InventorySOS = "ＳＯＳ"
InventoryPass = "パス"
InventoryFire = "クビ"
InventoryClickToAttack = "使いたい\nギャグを\nクリック\nしてね！"
InventoryDamageBonus = "(+%d)"

# NPCForceAcknowledge.py
NPCForceAcknowledgeMessage = "終了する前にトロリーに乗らなきゃ！\n\n\n\n\n\n\nトロリーは、グーフィーのギャグショップのとなりだよ。"
NPCForceAcknowledgeMessage2 = "トロリーをよく見つけられたね！\nトゥーンＨＱに行ってごほうびをもらってね。\n\n\n\n\n\n\n\nトゥーンＨＱは、プレイグラウンドのまんなか近くにあるよ。"
NPCForceAcknowledgeMessage3 = "トロリーに乗るのをわすれないでね！\n\n\n\n\nグーフィーのギャグショップのとなりにあるからね！"
NPCForceAcknowledgeMessage4 = "おめでとう！最初のトゥーンタスク完了だよ！\n\n\n\n\n\n\nトゥーンＨＱに行ってごほうびをもらってね。"
NPCForceAcknowledgeMessage5 = "キミのトゥーンタスクを忘れずに！\n\n\n\n\n\n\n\n\n\n\nコグたちは、トンネルのむこうにもいるよ。"
NPCForceAcknowledgeMessage6 = "よくコグをやっつけたね！\n\n\n\n\n\n\n\n\n早くトゥーン本部に戻ろう！"
NPCForceAcknowledgeMessage7 = "ともだちを作るのを忘れずに！\n\n\n\n\n\n\n他のトゥーンをクリックして、ともだちボタンを押そう！"
NPCForceAcknowledgeMessage8 = "そう、それでＯＫ！新しいともだちを作ったね。\n\n\n\n\n\n\n\n\n今すぐトゥーン本部に戻ろう！"
NPCForceAcknowledgeMessage9 = "電話はそんな感じに使うんだよ。\n\n\n\n\n\n\n\n\nトゥーン本部に戻って、ごほうびをもらおう！"

# Toon.py
ToonSleepString = "…ぐ～ぐ～…"

# Movie.py
MovieTutorialReward1 = "「なげる」ポイントを１つゲットしたね！\n１０ポイントためると、\n次のレベルのギャグが手に入るよ！"
MovieTutorialReward2 = "「みずでっぽう」ポイントも１つ、ゲットしたね！\nこうやってコグを倒してポイントを貯めてギャグを\nレベルアップしよう！"
MovieTutorialReward3 = "よくやったね！最初のトゥーンタスク完了だよ！" #CC_tom_movie_tutorial_reward01.mp3
MovieTutorialReward4 = "「トゥーンＨＱ」に\n行って、ごほうびをもらってね！" #CC_tom_movie_tutorial_reward02.mp3
MovieTutorialReward5 = "楽しんでね！" #CC_tom_movie_tutorial_reward03.mp3

# ToontownBattleGlobals.py
BattleGlobalTracks = ['トゥーンアップ', 'トラップ', 'おとり', 'サウンド', 'なげる', 'みずでっぽう', 'ドロップ']
BattleGlobalNPCTracks = ['かいふく', 'ﾄｩｰﾝ→ﾋｯﾄ', 'ｺｸﾞ→ﾐｽ']
BattleGlobalAvPropStrings = (
    ('まほうのはね', 'メガホン', 'まほうのリップ', 'まほうのステッキ', 'ピクシー・ダスト', 'ジャグリング・ボール', 'けっしのダイブ'),
    ('バナナのかわ', 'くまで', 'ビーだま', 'ありじごく', 'しかけドア', 'ダイナマイト', 'ぼうそう機関車'),
    ('１ドルさつ', 'ちいさなマグネット', '５ドルさつ', 'おおきなマグネット', '１０ドルさつ', 'グルグルめがね', 'プレゼン'),
    ('スモール・ホーン', 'ホイッスル', 'ラッパ', 'ミドル・ホーン', 'エレファント・ホーン', 'ビッグ・ホーン', 'オペラ歌手'),
    ('カップケーキ', 'フルーツパイひときれ', 'クリームパイひときれ', 'まるごとフルーツパイ', 'まるごとクリームパイ', 'バースデー・ケーキ', 'ウェディングケーキ'),
    ('フラワー・スプラッシュ', 'コップのみず', 'みずでっぽう', 'ペットボトル', 'しょうかホース', 'カミナリぐも', 'かんけつせん'),
    ('うえきばち', 'サンドバッグ', 'かなとこ', '１００キロ', 'きんこ', 'グランドピアノ', 'トゥーンタニック')
    )
BattleGlobalAvPropStringsSingular = (
    ('まほうのはね', 'メガホン', 'まほうのリップ', 'まほうのステッキ', 'ピクシー・ダスト', 'ジャグリング・ボールのセット', 'けっしのダイブ'),
    ('バナナのかわ', 'くまで', 'ビーだま', 'ありじごく', 'しかけドア', 'ダイナマイト', 'ぼうそう機関車'),
    ('１ドルさつ', 'ちいさなマグネット', '５ドルさつ', 'おおきなマグネット', '１０ドルさつ', 'グルグルめがね', 'プレゼン'),
    ('スモール・ホーン', 'ホイッスル', 'ラッパ', 'ミドル・ホーン', 'エレファント・ホーン', 'ビッグ・ホーン', 'オペラ歌手'),
    ('カップケーキ', 'フルーツパイひときれ', 'クリームパイひときれ', 'まるごとフルーツパイ', 'まるごとクリームパイ', 'バースデー・ケーキ', 'ウェディングケーキ'),
    ('フラワー・スプラッシュ', 'コップのみず', 'みずでっぽう', 'ペットボトル', 'しょうかホース', 'カミナリぐも', 'かんけつせん'),
    ('うえきばち', 'サンドバッグ', 'かなとこ', '１００キロ', 'きんこ ', 'グランドピアノ', 'トゥーンタニック')
    )
BattleGlobalAvPropStringsPlural = (
    ('まほうのはね', 'メガホン', 'まほうのリップ', 'まほうのステッキ', 'ピクシー・ダスト', 'ジャグリング・ボールのセット', 'けっしのダイブ'),
    ('バナナのかわ', 'くまで', 'ビーだま', 'ありじごく', 'しかけドア','ダイナマイト', 'ぼうそう機関車'),
    ('１ドルさつ', 'ちいさなマグネット', '５ドルさつ', 'おおきなマグネット','１０ドルさつ', 'グルグルめがね', 'プレゼン'),
    ('スモール・ホーン', 'ホイッスル', 'ラッパ', 'ミドル・ホーン', 'エレファント・ホーン', 'ビッグ・ホーン', 'オペラ歌手'),
    ('カップケーキ', 'フルーツパイひときれ', 'クリームパイひときれ','まるごとフルーツパイ', 'まるごとクリームパイ', 'バースデー・ケーキ', 'ウェディングケーキ'),
    ('フラワー・スプラッシュ', 'コップの水', 'みずでっぽう','ペットボトル', 'しょうかホース', 'カミナリぐも', 'かんけつせん'),
    ('うえきばち', 'サンドバッグ', 'かなとこ', '１００キロ', 'きんこ','グランドピアノ', 'トゥーンタニック')
    )
BattleGlobalAvTrackAccStrings = ("ふつう", "100％", "ひくい", "たかい", "ふつう", "たかい", "ひくい")
BattleGlobalLureAccLow = "ひくい"
BattleGlobalLureAccMedium = "ふつう"

AttackMissed = "しっぱい！"

NPCCallButtonLabel = "よぶ"

# ToontownLoader.py
LoaderLabel = "読み込み中…"

# PlayGame.py
HeadingToHood = "%(hood)s%(to)sへ向かっているよ…" # hood name
HeadingToYourEstate = "キミのおうちに向かっているよ…"
HeadingToEstate = "%sのおうちに向かっているよ…"  # avatar name
HeadingToFriend = "%sの友だちの土地に向かっているよ…"  # avatar name

# Hood.py
HeadingToPlayground = "プレイグラウンドに向かっているよ…"
HeadingToStreet = " %(street)s%(to)sへ向かっているよ…" #Street name

# TownBattle.py
TownBattleRun = "さっきいたプレイグラウンドへ戻る？"

# TownBattleChooseAvatarPanel.py
TownBattleChooseAvatarToonTitle = "どのトゥーン？"
TownBattleChooseAvatarCogTitle = "どの " + string.upper(Cog) + "？"
TownBattleChooseAvatarBack = lBack

#firecogpanel
FireCogTitle = "かいこ通知の数:%s\nどのコグをクビにする?"
FireCogLowTitle = "かいこ通知の数:%s\nたりないよ！"

# TownBattleSOSPanel.py
TownBattleSOSNoFriends = "電話する友だちがいないよ！"
TownBattleSOSWhichFriend = "どの友だちに電話する？"
TownBattleSOSNPCFriends = "助けたトゥーンたち"
TownBattleSOSBack = lBack

# TownBattleToonPanel.py
TownBattleToonSOS = "ＳＯＳ"
TownBattleToonFire = "クビ"
TownBattleUndecided = "？"
TownBattleHealthText = "%(hitPoints)s/%(maxHit)s"

# TownBattleWaitPanel.py
TownBattleWaitTitle = "他のプレイヤー\nを待ってます…"
TownSoloBattleWaitTitle = "待っててね…"
TownBattleWaitBack = lBack

# TownBattleSOSPetSearchPanel.py
TownBattleSOSPetSearchTitle = "ドゥードゥルを探しています\n%s..."

# TownBattleSOSPetInfoPanel.py
TownBattleSOSPetInfoTitle = "%sは%s " 
TownBattleSOSPetInfoOK = lOK

# Trolley.py
TrolleyHFAMessage = "ゲラゲラメーターが笑うまで、トロリーには乗れないんだ。"
TrolleyTFAMessage = Mickey + "がＯＫを出すまで、トロリーに乗っちゃだめだよ。"
TrolleyHopOff = "おりる"

# DistributedFishingSpot.py
FishingExit = "終了"
FishingCast = "キャスト"
FishingAutoReel = "オートリール"
FishingItemFound = "釣ったのは…"
FishingCrankTooSlow = "おそ\すぎる!"
FishingCrankTooFast = "はや\nすぎる!"
FishingFailure = "何も釣れなかったよ！"
FishingFailureTooSoon = "食いつきがあるまで、釣り糸を巻いちゃだめだよ。 うきがぴくぴく上下にすばやく動くまで待って！"
FishingFailureTooLate = "魚が食いついている間に、釣り糸を巻くんだよ！"
FishingFailureAutoReel = "今回はオートリールが動かなかったね。釣り上げる一番のタイミングに、ちょうどいい速さで手でクランクを回して！"
FishingFailureTooSlow = "クランクを回すのがおそすぎるよ。他の魚よりもすばしっこい魚もいるからね。スピードバーを中心にしておいてみて！"
FishingFailureTooFast = "クランクを回すのがはやすぎるよ。他の魚よりものろい魚もいるからね。スピードバーを中心にしておいてみて！"
FishingOverTankLimit = "タンクが一杯だよ。\n魚を売ってから\nもう一度きてね！"
FishingBroke = "釣り針につけるものがなくなっちゃったよ!  トロリーにのって、ジェリービーンをもっとあつめてきてね！"
FishingHowToFirstTime = "キャストボタンをクリックして、下の方向にドラッグしてね。ドラッグすればするほど、より遠くに投げることができるよ。ターゲットに向けて角度も調節しよう。\n\n今すぐ、試そう！"
FishingHowToFailed = "キャストボタンをクリックして、下の方向にドラッグしてね。ドラッグすればするほど、より遠くに投げることができるよ。ターゲットに向けて角度も調節しよう。\n\nもう一度、試してみよう！"
FishingBootItem = "ボロぐつ"
FishingJellybeanItem = "%s ジェリービーン"
FishingNewEntry = "新種発見！"
FishingNewRecord = "新記録！"

# FishPoker
FishPokerCashIn = "かけビーン\n%s\n%s"
FishPokerLock = "選ぶ"
FishPokerUnlock = "戻す"
FishPoker5OfKind = "５カード"
FishPoker4OfKind = "４カード"
FishPokerFullHouse = "フルハウス"
FishPoker3OfKind = "３カード"
FishPoker2Pair = "２ペア"
FishPokerPair = "１ペア"

# DistributedTutorial.py　★台本チェック★
TutorialGreeting1 = "やあ %s！"
TutorialGreeting2 = "やあ %s！\nこっちにおいでよ！"
TutorialGreeting3 = "やあ %s！\nこっちにおいでよ！\nやじるしキーを使ってね！"
TutorialMickeyWelcome = "トゥーンタウンへようこそ！"
TutorialFlippyIntro = "友だちの" + Flippy + "を紹介するよ。"
TutorialFlippyHi = "やあ、 %s！"
TutorialQT1 = "これを使って話してね。"
TutorialQT2 = "これを使って話せるよ。\nクリックして、\"やあ！\"を選んでね。"
TutorialChat1 = "ボタンのどちらかを使って話してね。"
TutorialChat2 = "あおいボタンは、キーボードを使ったチャット用だよ。"
TutorialChat3 = "気をつけて！  キーボードを使ってる時、他のほとんどのプレイヤーは、キミの言ってることがわからないよ。"
TutorialChat4 = "みどりのボタンは、%sをひらくよ。"
TutorialChat5 = "%sを使えば、みんながキミのことわかってくれるようになるよ。"
TutorialChat6 = "\"やあ！\"って言ってみてごらん！"
TutorialBodyClick1 = "じょうずにできたね！"
TutorialBodyClick2 = "よろしくね！ねえ、ともだちにならない？"
TutorialBodyClick3 = Flippy + "と友だちになるには、その子をクリックしてね。"
TutorialHandleBodyClickSuccess = "いいカンジだね！"
TutorialHandleBodyClickFail = "まだまだだね。" + Flippy + "の真上をクリックして…"
TutorialFriendsButton = "右かどの"+ Flippy + "の下の'ともだち' ボタンをクリックして…"
TutorialHandleFriendsButton = "そして'はい' のボタンを押してね。"
TutorialOK = lOK
TutorialYes = lYes
TutorialNo = lNo
TutorialFriendsPrompt = Flippy + "とともだちになりたい？"
TutorialFriendsPanelMickeyChat = Flippy + " は、キミのともだちになりたいって。'ＯＫ' をクリックして終了してね。"
TutorialFriendsPanelYes = Flippy + "は、いいよって言ってるよ！"
TutorialFriendsPanelNo = "あんまり感じよくないね！"
TutorialFriendsPanelCongrats = "おめでとう！最初のともだちができたよ！"
TutorialFlippyChat1 = "最初のトゥーンタスクの準備ができたら、会いにきてね!"
TutorialFlippyChat2 = "タウンホールにいるね！"
TutorialAllFriendsButton = "ともだちボタンをクリックすると、キミの友だち全員をみることができるよ。やってみて…"
TutorialEmptyFriendsList = Flippy + " は実際のプレイヤーじゃないから、キミのリストは今からっぽだよ。"
TutorialCloseFriendsList = "リストを消すには、\n'閉じる'\nボタン をクリックしてね。"
TutorialShtickerButton = "下の右のかどのボタンは、トゥーンガイドを開くよ。 やってみて…"
TutorialBook1 = "このトゥーンガイドには、トゥーンタウンの地図のようにとっても役立つ情報がたくさん入っているんだ"
TutorialBook2 = "キミのトゥーンタスクの進歩もチェックできるよ。"
TutorialBook3 = "使い終わったら、とらの巻ボタンをもう一度クリックして、閉じておいてね。"
TutorialLaffMeter1 = "これも必要だよ…"
TutorialLaffMeter2 = "これも必要だよ…\nキミのゲラゲラメーター！"
TutorialLaffMeter3 = Cogs + "がキミを攻撃すると、ポイントが低くなっちゃうんだ"
TutorialLaffMeter4 = "こんな具合にプレイグラウンドにいると、ポイントが回復するよ。"
TutorialLaffMeter5 = "トゥーンタスクが終わったら、キミのゲラゲラリミットが上がったりするごほうびがもらえるよ。"
TutorialLaffMeter6 = "気をつけて！ もし" + Cogs + "にたおされたら、そいつにキミの持ってるギャグが全部持っていかれちゃうんだ！"
TutorialLaffMeter7 = "トロリーゲームをして、ギャグをもっとゲットしよう！"
TutorialTrolley1 = "トロリーに行くから、ついてきて!"
TutorialTrolley2 = "乗るよ!"
TutorialBye1 = "ゲームをしよう！"
TutorialBye2 = "ゲームをしよう！\nギャグを買おう！"
TutorialBye3 = "終わったら、" + Flippy + " に会いにいこう!"

# TutorialForceAcknowledge.py
TutorialForceAcknowledgeMessage = "行き先がちがうよ！　" + Mickey + "をさがしにいって!"

PetTutorialTitle1 = "ドゥードゥル パネル"
PetTutorialTitle2 = "ドゥードゥル スピードチャット"
PetTutorialTitle3 = "ドゥードゥル カタログ"
PetTutorialNext = "次のページ"
PetTutorialPrev = "前のページ"
PetTutorialDone = "ＯＫ"
PetTutorialPage1 = "ドゥードゥルをクリックすると、ドゥードゥルパネルが表示されるよ。 エサをあげたり、なでたり、呼び出すことができるんだ。"
PetTutorialPage2 = "ドゥードゥルに「トリック」をさせたければ、スピードチャットの「ペット」の項目を使ってね。 「トリック」をしたら、ちゃんとごほうびをあげればごきげんになるよ。"
PetTutorialPage3 = "クララベルのショッピングカタログからドゥードゥルの新しい「トリック」を買ってね。 より良い「トリック」はより多くのトゥーンアップができるよ。"
def getPetGuiAlign():
	from pandac.PandaModules import TextNode
	return TextNode.ALeft

GardenTutorialTitle1 = "ガーデニング" #localize
GardenTutorialTitle2 = "花"
GardenTutorialTitle3 = "木"
GardenTutorialTitle4 = "育て方"
GardenTutorialTitle5 = "ステータス"
GardenTutorialNext = "次ページ"
GardenTutorialPrev = "前ページ"
GardenTutorialDone = "わかった"
GardenTutorialPage1 = "キミのおうちをガーデニングでトゥーンアップ！お花や木を育ててデコレーションして、強力なギャグをしゅうかくしよう！"
GardenTutorialPage2 = "花の育ち方はジェリービーンのびみょうなまぜ方で決まるよ。うまく育ったらキミの庭にある手押し車で売りに行こう。続けるといいことがあるよ！"
GardenTutorialPage3 = "キミのもっているギャグを使って木をうえよう。何日かたつと、そのギャグが強力になってるよ!でも、その木の世話をしないとギャグはまたもとにもどっちゃうよ。"
GardenTutorialPage4 = "キミのおうちのまわりで花や木を育ててしゅうかくしてね。"
GardenTutorialPage5 = "花のぞうは、クララベルのカタログで買えるよ。スキルをあげて、もっとステキな花のぞうを手に入れよう！"

# Playground.py
PlaygroundDeathAckMessage = "あーあ、 " + Cogs + "がキミの持ってたギャグを取ってっちゃったよ！\nゲラゲラメーターが笑うまではプレイグラウンドから出られないよ。"

# FactoryInterior.py
ForcedLeaveFactoryAckMsg = "工場長が倒されたので、コグパーツを手に入れることができませんでした。"

# MintInterior
ForcedLeaveMintAckMsg = "金庫番が倒されたので、コグドルを手に入れることができませんでした。" #▲要チェック▲

# DistributedFactory.py
HeadingToFactoryTitle = "%sへ向かっているよ…"
ForemanConfrontedMsg = "%sは今、工場長と戦っているよ！"

# DistributedMint.py
MintBossConfrontedMsg = "%sは今、金庫番と戦っているよ！"

# DistributedStage.py #localize
StageBossConfrontedMsg = "%sがクラークとバトル中!"
stageToonEnterElevator = "%s \nがエレベーターにのったよ。"
ForcedLeaveStageAckMsg = "ロウクラークはキミがたどりつく前にたおされました。ショーカンジョーを取りもどせませんでした。"

# DistributedMinigame.py
MinigameWaitingForOtherPlayers = "他のプレイヤーを待っています…"
MinigamePleaseWait = "…"
DefaultMinigameTitle = "ミニゲームのタイトル"
DefaultMinigameInstructions = "ミニゲームの説明"
HeadingToMinigameTitle = "%sをしよう！" # minigame title

# MinigamePowerMeter.py
MinigamePowerMeterLabel = "パワーメーター"
MinigamePowerMeterTooSlow = "おそ\nすぎる"
MinigamePowerMeterTooFast = "はや\nすぎる"

# DistributedMinigameTemplate.py
MinigameTemplateTitle = "ミニゲームのテンプレート"
MinigameTemplateInstructions = "ミニゲームのテンプレートだよ。これを使って新しいミニゲームを作成してね。"

# DistributedCannonGame.py
CannonGameTitle = "キャノンゲーム"
CannonGameInstructions = "キミのトゥーンを発射して、できるだけ早く給水塔に入れてあげてね。マウスかやじるしキーを使って目標をさだめられるよ。早く入れれば、みんなが大きなごほうびをもらえるからがんばろう！"
CannonGameReward = "ごほうび"

# DistributedTwoDGame.py
TwoDGameTitle = "トゥーン・エスケープ"
TwoDGameInstructions = "いそいでコグの隠れ家から逃げるんだ！矢印キーで移動とジャンプ、Ctrlキーでみずでっぽうを発射できるよ。コグ・コインを集めるとボーナスポイントがつくよ。"
TwoDGameElevatorExit = "出口"

# DistributedTugOfWarGame.py
TugOfWarGameTitle = "つなひきゲーム"
TugOfWarInstructions = "右と左のやじるしキーをちょうどいい速さで交互にたたいて、あかい線といっしょにみどりのバーをおいてね。たたく速さがおそすぎたり、はやすぎたりすると水のなかに落っこちて終わっちゃうよ！"
TugOfWarGameGo = "スタート！"
TugOfWarGameReady = "よおい…"
TugOfWarGameEnd = "がんばったね！"
TugOfWarGameTie = "ひきわけ！"
TugOfWarPowerMeter = "パワーメーター"

# DistributedPatternGame.py
PatternGameTitle = Minnie + "のダンスゲーム"
PatternGameInstructions = Minnie + " が、ダンスをみせてくれるよ。" + \
                          "やじるしキーを使って、" + Minnie + "のダンスをいま見たようにやってみてね！"
PatternGameWatch   = "ダンスステップをみて…"
PatternGameGo      = "スタート！"
PatternGameRight   = "じょうずね、%s！"
PatternGameWrong   = "あ～あ！"
PatternGamePerfect = "かんぺきだったわ、%s！"
PatternGameBye     = "ごくろうさま！"
PatternGameWaitingOtherPlayers = "他のプレイヤーを待っててね…"
PatternGamePleaseWait = "ちょっと待っててね…"
PatternGameFaster = "はやすぎちゃった！"
PatternGameFastest = "キミが\n一番はやかったわよ！"
PatternGameYouCanDoIt = "さぁ！\nキミならできるわよ！"
PatternGameOtherFaster = "\nがはやかったわね！"
PatternGameOtherFastest = "\nが一番はやかったよ！"
PatternGameGreatJob = "よくやったわ！"
PatternGameRound = "ラウンド%s！"
PatternGameImprov = "すばらしかったわ！次もがんばってね！"

# DistributedRaceGame.py
RaceGameTitle = "きょうそうゲーム"
RaceGameInstructions = "数字をじょうずにえらんでクリックしてね。他にだれもえらんでない数字を選ばないと、先にいけないよ！"
RaceGameWaitingChoices = "他のプレイヤーを待っててね…"
RaceGameCardText = "%(name)sがゲットしたのは: %(reward)s"
RaceGameCardTextBeans = "%(name)s がもらえるごほうび: %(reward)s"
RaceGameCardTextHi1 = "すっごいね、%(name)s！"  # this category might eventually have secret game hints, etc

# RaceGameGlobals.py
RaceGameForwardOneSpace    = "１マスすすむ"
RaceGameForwardTwoSpaces   = "２マスすすむ"
RaceGameForwardThreeSpaces = "３マスすすむ"
RaceGameBackOneSpace    = "１マスもどる"
RaceGameBackTwoSpaces   = "２マスもどる"
RaceGameBackThreeSpaces = "３マスもどる"
RaceGameOthersForwardThree = " 他のひとたちは全員\n３マスすすめているよ。"
RaceGameOthersBackThree = "他のひとたちは全員\n３マス戻っているよ。"
RaceGameInstantWinner = "一気に勝ちをきめたー！"
RaceGameJellybeans2 = "ジェリービーン２コ"
RaceGameJellybeans4 = "ジェリービーン４コ"
RaceGameJellybeans10 = "ジェリービーン１０コ！"

# DistributedRingGame.py
RingGameTitle = "リングゲーム"
# color
RingGameInstructionsSinglePlayer = "できるだけ多くの%sうきわをくぐって泳いでみて！ やじるしキーを使って泳いでね。"
# color
RingGameInstructionsMultiPlayer = " %sうきわをくぐって泳いでみて。ほかのプレイヤーはちがう色のうきわに挑戦するよ。 やじるしキーを使って泳いでね。"
RingGameMissed = "失敗"
RingGameGroupPerfect = "パーフェクト\nチームワーク！"
RingGamePerfect = "パーフェクト！"
RingGameGroupBonus = "グループボーナス"

# RingGameGlobals.py
ColorRed = "あかい"
ColorGreen = "みどり色の"
ColorOrange = "オレンジ色の"
ColorPurple = "むらさき色の"
ColorWhite = "しろい"
ColorBlack = "くろい"
ColorYellow = "きいろの"

# DistributedDivingGame.py #localize
DivingGameTitle = "ダイビングゲーム"
# color
DivingInstructionsSinglePlayer = "たからものはみずうみのそこにあるよ。矢印キーを使っておよいでね。サカナをさけながら、ボートまでたからをはこぼう!"
# color
DivingInstructionsMultiPlayer = "たからものはみずうみのそこにあるよ。矢印キーを使っておよいでね。みんなで力をあわせてボートまでたからものをはこぼう!"
DivingGameTreasuresRetrieved = "たからの数"

#Distributed Target Game
TargetGameTitle = "スリング・ショット"
TargetGameInstructionsSinglePlayer = "発射の方向とスピードがポイントだよ。"
TargetGameInstructionsMultiPlayer = "まとの中心を目指して着地しよう！"
TargetGameBoard = "ラウンド%s - がんばってね！"
TargetGameCountdown = "%s秒でじどう的にはっしゃ！"
TargetGameCountHelp = "左右の矢印キーをこうごに連打してパワーを調節。やめると発射だよ。"
TargetGameFlyHelp = "下向き矢印でカサを開いてね。"
TargetGameFallHelp = "ターゲットには矢印キーでコントロールしながら着地しよう！"
TargetGameBounceHelp = "地面ではねるとターゲットからはずれちゃうかも。"

#Distributed Photo Game
PhotoGameScoreTaken = "%s: %s\nキミ: %s"
PhotoGameScoreBlank = "スコア: %s"
PhotoGameScoreOther = "\n%s"#"スコア: %s\n%s"
PhotoGameScoreYou = "\nベスト・ボーナス!"#"スコア: %s\nベスト・ボーナス!"


# DistributedTagGame.py
TagGameTitle = "おにごっこゲーム"
TagGameInstructions = "できるだけ多くのアイスクリームを取ろう！ オニになるとアイスは取れなくなるからね！"
TagGameYouAreIt = "キミがオニだよ！"
TagGameSomeoneElseIsIt = "%s がオニだよ！"

# DistributedMazeGame.py
MazeGameTitle = "メイズゲーム"
MazeGameInstructions = "ミッキーマークをできるだけあつめよう！\nでも、" + Cogs + "には気をつけてね!"

# DistributedCatchGame.py
CatchGameTitle = "キャッチゲーム"
CatchGameInstructions = "できるだけ多くの%(fruit)sを" + Cogs + "に気をつけながらキャッチして。 %(badThing)sはキャッチしないようにね！"
CatchGamePerfect = "パーフェクト！"
CatchGameApples      = 'りんご'
CatchGameOranges     = 'オレンジ'
CatchGamePears       = 'ようナシ'
CatchGameCoconuts    = 'ココナッツ'
CatchGameWatermelons = 'すいか'
CatchGamePineapples  = 'バイナップル'
CatchGameAnvils      = 'かなとこ'

# DistributedPieTossGame.py
PieTossGameTitle = "パイ投げゲーム"
PieTossGameInstructions = "ターゲットにパイを投げよう！"

# DistributedPhotoGame.py
PhotoGameInstructions = "下のトゥーン達を撮ろう！マウスでフレームを動かして左クリックで撮影だよ。Ctrlキーでズーム調整して、矢印キーで周りをみわたせるよ。☆の数が多い程高いポイントをゲット！"
PhotoGameTitle = "パパラトゥーン！"
PhotoGameFilm = "フィルム"
PhotoGameScore = "チームスコア: %s\n\nベストフォト: %s\n\nトータルスコア: %s"

# DistributedCogThiefGame.py
CogThiefGameTitle = Cog + "バレル・スティール"
CogThiefGameInstructions = "コグ達からギャグ・バレルを守れ！矢印キーでトゥーンを操作して、Ctrlキーでパイを投げつけよう。ななめにも進めるよ！"
CogThiefBarrelsSaved = "%(num)d個のバレルを\n守った！"
CogThiefBarrelSaved = "%(num)d個のバレルを\n守った！"
CogThiefNoBarrelsSaved = "ぜんぶ\n盗まれちゃった…"
CogThiefPerfect = "パーフェクト!"

# MinigameRulesPanel.py
MinigameRulesPanelPlay = "プレイ"

# Purchase.py
GagShopName = "グーフィーの ギャグショップ"
GagShopPlayAgain = "もういちど\nプレイする"
GagShopBackToPlayground = "プレイグラウ\nンドにもどる"
GagShopYouHave = "使えるジェリービーンは%sコだよ。"
GagShopYouHaveOne = "使えるジェリービーンは１コだよ。"
GagShopTooManyProps = "もうこれ以上もてないよ。"
GagShopDoneShopping = "ショッピング\n終了"
# name of a gag
GagShopTooManyOfThatGag = "すでに%sをたくさん持ってるよ。"
GagShopInsufficientSkill = "まだ使えないよ。"
# name of a gag
GagShopYouPurchased = "%sをゲット！"
GagShopOutOfJellybeans = "ジェリービーンがないよ！"
GagShopWaitingOtherPlayers = "他のプレイヤーを待っててね…"
# these show up on the avatar panels in the purchase screen
GagShopPlayerDisconnected = "%sは、接続を切りました。"
GagShopPlayerExited = "%s は、店をでたよ。"
GagShopPlayerPlayAgain = "もう１回！"
GagShopPlayerBuying = "お買い物中"

# MakeAToon.py
GenderShopQuestionMickey = "男の子のトゥーンをつくるには、\nぼくをおしてね！" #CC_mickey_create01.mp3
GenderShopQuestionMinnie = "女の子のトゥーンをつくるには、わたしをおしてね！" #CC_minnie_create01.mp3
GenderShopFollow = "ついてきて！" #CC_mickey_create02.mp3 (if Mickey)
GenderShopSeeYou = "またね！"#CC_mickey_create03.mp3 (if Mickey)
GenderShopBoyButtonText = "男の子"
GenderShopGirlButtonText = "女の子"

# BodyShop.py
BodyShopHead = "あたま"
BodyShopBody = "おなか"
BodyShopLegs = "あし"

# ColorShop.py
ColorShopHead = "あたま"
ColorShopBody = "おなか"
ColorShopLegs = "あし"
ColorShopToon = "いろ"
ColorShopParts = "パーツ"
ColorShopAll = "すべて"

# ClothesShop.py
ClothesShopShorts = "ズボン"
ClothesShopShirt = "シャツ"
ClothesShopBottoms = "ボトム"

# MakeAToon
PromptTutorial = "おめでとう！\nキミはトゥーンタウンで一番新しい住民だよ！\n\nこのままトゥーントリアルに進む？それともトゥーンタウンセントラルにワープする？"
MakeAToonSkipTutorial = "ﾄｩｰﾝﾄﾘｱﾙをやめる"
MakeAToonEnterTutorial = "ﾄｩｰﾝﾄﾘｱﾙに進む"
MakeAToonDone = "けってい"
MakeAToonCancel = "とりけす"
MakeAToonNext = "つぎへ"
MakeAToonLast = "もどる"
CreateYourToon = "左右のやじるしをクリックしてパーツを選んでね。"
CreateYourToonTitle = "トゥーンをつくる"
ShapeYourToonTitle = "しゅるいをえらんでね"
PaintYourToonTitle = "どんないろがいい？"
PickClothesTitle = "ようふくをえらぼう"
NameToonTitle = "なまえをきめよう"
CreateYourToonHead = "他のトゥーンを選ぶには、'あたま' のやじるしをクリックしてね。"
MakeAToonClickForNextScreen = "次のステップに進むには、右下のやじるしをクリックしてね。"
PickClothes = "やじるしをクリックして、ようふくを選んでね。"
PaintYourToon = "やじるしをクリックして、トゥーンに色をつけてね。"
MakeAToonYouCanGoBack = "前の画面に戻ってパーツを選び直すこともできるよ！"
MakeAFunnyName = "キミのトゥーン\nにおもしろい名\n前をつけよう！"
MustHaveAFirstOrLast1 = "トゥーンにはなまえかみょうじが必要だとおもわない？"
MustHaveAFirstOrLast2 = "キミのトゥーンになまえかみょうじほしくないの？"
ApprovalForName1 = "そうだよ、キミのトゥーンはすごくいいなまえをもつ価値があるよ！"
ApprovalForName2 = "トゥーンのなまえは、いいものしかそろえてないよ！"
MakeAToonLastStep = "トゥーンタウンへ行く前の最後のステップだからね！"
PickANameYouLike = "すきななまえを選んでね！"
TitleCheckBox = "かたがき"
FirstCheckBox = "なまえ"
LastCheckBox = "みょうじ"
RandomButton = "ランダム"
ShuffleButton = "シャッフル"
NameShopSubmitButton = "名前を申込む"
TypeANameButton = "なまえを入力"
TypeAName = "ここにあるなまえはすきじゃない？\nここをクリックして -->"
PickAName = "なまえをえらぼうゲームをやってみて！\nここをクリックして -->"
PickANameButton = "なまえをえらぶ"
RejectNameText = "このなまえは使えないよ。もういちどトライしてね。"
WaitingForNameSubmission = "名前を登録します..."

# PetshopGUI.py
PetNameMaster = "PetNameMaster_japanese.txt"
PetshopUnknownName = "名前: ???"
PetshopDescGender = "せいべつ:\t%s"
PetshopDescCost = "かかく:\t%sジェリービーン"
PetshopDescTrait = "とくせい:\t%s"
PetshopDescStandard = "スタンダード"
PetshopCancel = lCancel
PetshopSell = "魚を売る"
PetshopAdoptAPet = "ドゥードゥルを飼う"
PetshopReturnPet = "ドゥードゥルを返す"
PetshopAdoptConfirm = "%sを飼う（%dジェリービーン）"
PetshopGoBack = lBack
PetshopAdopt = "飼う"
PetshopReturnConfirm = "%sを返しますか？"
PetshopReturn = "返す"
PetshopChooserTitle = "今日のドゥードゥル"
PetshopGoHomeText = 'おうちに戻って、新しいドゥードゥルと遊びに行きたいですか？'

# NameShop.py
NameShopNameMaster = "NameMaster_japanese.txt"
NameShopPay = "今すぐお申しこみを!"
NameShopPlay = "登録無料"
NameShopOnlyPaid = "フルアクセスメンバーだけが、\nトゥーンのなまえを変えることができるんだ。\nキミが申しこみするまでの\nトゥーンのなまえは\nだよ。"
NameShopContinueSubmission = "なまえをとどける"
NameShopChooseAnother = "なまえをつける"
NameShopToonCouncil = "キミのなまえが\n使えるかどうか調べるんだ\n" + \
                      "調べるのには数日かかるよ。\nそれまでのなまえは：\n"
PleaseTypeName = "トゥーンになまえをつけてあげてね:"
AllNewNames = "全ての新しいなまえは、\nトゥーン評議会のＯＫが\n必要なんだよ。"
NameMessages = ""
NameShopNameRejected = "申込んだ\nなまえは\nだめだって。"
NameShopNameAccepted = "おめでとう！\n申込んだ\nなまえが\n使えるよ。"
NoPunctuation = "なまえに句読点や記号（。、・等）は使えないよ！"
PeriodOnlyAfterLetter = "なまえでは、文字のあと以外、ピリオド(.)は使えないよ。"
ApostropheOnlyAfterLetter = "なまえでは、文字のあと以外、アポストロフィー( ' )は使えないよ。"
NoNumbersInTheMiddle = "言葉の間に数字があるのはだめだよ。"
ThreeWordsOrLess = "キミのなまえは３つの言葉かそれ以下じゃないとだめだよ。"
CopyrightedNames = (
    "ミッキー",
    "ミッキー・マウス",
    "ミッキーマウス",
    "ミニー",
    "ミニー・マウス",
    "ミニーマウス",
    "ドナルド",
    "ドナルド・ダッグ",
    "ドナルドダッグ",
    "プルート",
    "グーフィー",
    )
NumToColor = ['ﾎﾜｲﾄ', 'ﾋﾟｰﾁ', 'ﾌﾞﾗｲﾄﾚｯﾄﾞ', 'ﾚｯﾄﾞ', 'ﾏﾙｰﾝ',
              'ｼｴﾝﾅ', 'ﾌﾞﾗｳﾝ', 'ﾀﾝ', 'ｺｰﾗﾙ', 'ｵﾚﾝｼﾞ',
              'ｲｴﾛｰ', 'ｸﾘｰﾑ', 'ｼﾄﾘｰﾝ', 'ﾗｲﾑ', 'ｼｰｸﾞﾘｰﾝ',
              'ｸﾞﾘｰﾝ', 'ﾗｲﾄﾌﾞﾙｰ', 'ｱｸｱ', 'ﾌﾞﾙｰ',
              'ﾍﾟﾘｳｨﾝｸﾙ', 'ﾛｲﾔﾙﾌﾞﾙｰ', 'ｽﾚｰﾄﾌﾞﾙｰ', 'ﾊﾟｰﾌﾟﾙ',
              'ﾗﾍﾞﾝﾀﾞｰ', 'ﾋﾟﾝｸ']
AnimalToSpecies = {
    'dog': 'イヌ',
    'cat' : 'ネコ',
    'mouse' : 'ネズミ',
    'horse' : 'ウマ',
    'rabbit' : 'ウサギ',
    'duck' : 'アヒル',
    'monkey' : 'サル',
    'bear'   : 'クマ',
    'pig'    : 'ブタ'	
    }
NameTooLong = "なまえは全角8文字までだよ。もう一度入力してね。"
ToonAlreadyExists = "もうトゥーン名%sができてるよ！"
NameAlreadyInUse = "そのなまえはもう使われているよ！"
EmptyNameError = "なまえを先に入力してね。"
NameError = "ごめん、そのなまえじゃだめみたい"

# NameCheck.py
NCTooShort = 'なまえは全角2文字以上にしてね'
NCNoDigits = 'なまえには数字をいれないでね。'
NCNeedLetters = 'なまえのそれぞれの言葉には、文字をいれてね。'
NCNeedVowels = 'なまえのそれぞれの言葉には、母音をいれてね。'
NCAllCaps = 'なまえは全部大文字にしないでね。'
NCMixedCase = 'なまえに大文字がおおすぎるね。'
NCBadCharacter = "なまえには'%s'をいれないでね。\n\n漢字・記号・ABC…は使わないでね。"
NCGeneric = 'ごめん、このなまえじゃだめみたい。\n\nなまえは全角8文字以下にしてね。'
NCTooManyWords = '半角スペースは三つまでにしてね。'
NCDashUsage = ("なまえにハイフン(-)は使えないよ。"
               "")
NCCommaEdge = "なまえにコンマ(,)は使えないよ。"
NCCommaAfterWord = "なまえにコンマ(,)は使えないよ。"
NCCommaUsage = ('なまえにコンマ(,)は使えないよ。'
                ''
                '')
NCPeriodUsage = ('なまえにピリオド(.)は使えないよ。'
                 '')
NCApostrophes = "なまえにアポストロフィー(')は使えないよ。"

# DistributedTrophyMgrAI.py
RemoveTrophy = lToonHQ+"：キミが救った建物のひとつを" + Cogs + " にのっとられた！"

# toon\DistributedNPCTailor/Clerk/Fisherman.py
STOREOWNER_TOOKTOOLONG = 'もっと考える時間がほしい？'
STOREOWNER_GOODBYE = 'またね！'
STOREOWNER_NEEDJELLYBEANS = 'ジェリービーンをとりにいくには、トロリーに乗らなきゃね。'
STOREOWNER_GREETING = '買いたいものを選んでね。'
STOREOWNER_BROWSING = 'ウィンドウショッピングもできるけど、ようふくを買うにはようふく券が必要だよ。'
STOREOWNER_NOCLOTHINGTICKET = 'ようふくを買うにはようふく券が必要だよ。'

STOREOWNER_NOFISH = 'ここに戻って、釣った魚をジェリービーンと交換しよう！'
STOREOWNER_THANKSFISH = 'ありがとう！ペットショップがきっとよろこんでくれるよ。バイバイ！'
STOREOWNER_THANKSFISH_PETSHOP = "おっ、いい種類の魚がいるね。ありがとう！"
STOREOWNER_PETRETURNED = "安心して、僕たちがキミのドゥードゥルのためのおうちを探してあげるから！"
STOREOWNER_PETADOPTED = "新しいドゥードゥル、おめでとう！ キミのおうちで一緒にあそべるよ。"
STOREOWNER_PETCANCELED = "もしお気に入りのドゥードゥルを見つけたら、ほかのトゥーンが飼う前にキミが飼おう！"

STOREOWNER_NOROOM = "うーん…あたらしいようふくを買うまえに、キミはクローゼットの中を整理したほうがいいね。"
STOREOWNER_CONFIRM_LOSS = "キミのクローゼットはいっぱいだ！前にキミが着ていたようふくはなくなるよ。"
STOREOWNER_OK = lOK
STOREOWNER_CANCEL = lCancel
STOREOWNER_TROPHY = "ワオ！キミは%s匹の魚（%s匹中）を釣ったね。ごほうびにトロフィーとゲラゲラブーストをあげよう！"
# end translate

# NewsManager.py
SuitInvasionBegin1 = lToonHQ+"： コグの侵略がはじまった！！！"
SuitInvasionBegin2 = lToonHQ+"： %s にトゥーンタウンをのっとられた！！！"
SuitInvasionEnd1 = lToonHQ+"： %s の侵略はおわった！！！"
SuitInvasionEnd2 = lToonHQ+"： トゥーンがまた今日という日を救った！！！"
SuitInvasionUpdate1 = lToonHQ+"： コグの侵略はいま%sコグになっている！！！"
SuitInvasionUpdate2 = lToonHQ+"： %sを倒さねば！！！"
SuitInvasionBulletin1 = lToonHQ+"： コグの侵略が進行中！！！"
SuitInvasionBulletin2 = lToonHQ+"： %s にトゥーンタウンをのっとられた！！！"

# DistributedHQInterior.py
LeaderboardTitle = "トゥーン・プラトゥーン"
# QuestScript.txt
QuestScriptTutorialMickey_1 = "こんにちは、トム！\nトゥーンタウンの新しい住人になにか面白いギャグ、持ってない？" #CC_mickey_tutorial02.mp3　***DELETED "CC_mickey_tutorial01.mp3"***
QuestScriptTutorialMickey_2 = "もちろん、%s！" #CC_tom_tutorial_mickey01.mp3
QuestScriptTutorialMickey_3 = "彼がコグについて\nいろいろ教えてくれるって！\aそれじゃあ、\nまた後でね～！" #CC_mickey_tutorial03.mp3 \a CC_mickey_tutorial05.mp3　***DELETED "CC_mickey_tutorial04.mp3"***
QuestScriptTutorialMickey_4 = "やじるしキーを使ってこっちにおいで！" #CC_tom_tutorial_mickey02.mp3

# These are needed to correspond to the Japanese gender specific phrases
QuestScriptTutorialMinnie_1 = "こんにちは、トム！\nトゥーンタウンの新しい住人になにか面白いギャグ、持ってない？" #CC_minnie_tutorial02.mp3　***DELETED "CC_minnie_tutorial01.mp3"***
QuestScriptTutorialMinnie_2 = "もちろん、%s！" #CC_tom_tutorial_minnie01.mp3
QuestScriptTutorialMinnie_3 = "彼がコグについて\nいろいろ教えてくれるのよ！\aそれじゃあ、\nまたね～！" #CC_minnie_tutorial03.mp3 \a CC_minnie_tutorial05.mp3 *** DELETED "CC_minnie_tutorial04.mp3"***

QuestScript101_1 = "これらが「コグ」って言うんだ！\nトゥーンタウンをのっとろうとしているロボットたちなんだ。" #Please play "CC_tom_tutorial_questscript01.mp3" only / "CC_tom_tutorial_questscript02.mp3" is included.
QuestScript101_2 = "たくさんの種類のコグがいるんだけど…" #CC_tom_tutorial_questscript03.mp3
QuestScript101_3 = "…ハッピーな\nトゥーンビルをね…" #CC_tom_tutorial_questscript041.mp3
QuestScript101_4 = "…みにくいコグのビルにしてしまうんだ！" #CC_tom_tutorial_questscript05.mp3
QuestScript101_5 = "でも頭のかったーいコグはギャグをまったく理解することができないんだ！" #CC_tom_tutorial_questscript06.mp3
QuestScript101_6 = "だからトゥーンのおもしろいギャグで、 コグの動きを止めることができるんだよ。" #CC_tom_tutorial_questscript07.mp3
QuestScript101_7 = "たくさんのギャグがあるけど、まずはこれとこれかな…" #CC_tom_tutorial_questscript08.mp3
QuestScript101_8 = "そうだ、ゲラゲラメーターも必要だね！" #CC_tom_tutorial_questscript09.mp3
QuestScript101_9 = "ゲラゲラメーターが低すぎると、かなしくなって落ち込んじゃうんだよ。" #CC_tom_tutorial_questscript10.mp3
QuestScript101_10 = "つまりハッピーだと、トゥーンは健康ってことなんだ！" #CC_tom_tutorial_questscript11.mp3
QuestScript101_11 = "あーっ！ ぼくの店の外にコグがいる！" #CC_tom_tutorial_questscript12.mp3
QuestScript101_12 = "たすけて、おねがい！ コグをやっつけて！" #CC_tom_tutorial_questscript13.mp3
QuestScript101_13 = "キミに最初のトゥーンタスクをあげるね！\n　" #CC_tom_tutorial_questscript14.mp3　***DELETED "CC_tom_tutorial_questscript15.mp3"***
QuestScript101_14 = "外にいるオベッカーを倒そう！いそいで！" #CC_tom_tutorial_questscript16.mp3

QuestScript110_1 = "よくひとりでオベッカーを倒したね。 それじゃあ、ごほうびにトゥーンガイドをあげよう…" #CC_harry_tutorial_questscript01.mp3
QuestScript110_2 = "トゥーンガイドには、たくさんの情報がはいってるよ。" #CC_harry_tutorial_questscript02.mp3
QuestScript110_3 = "それを開いてごらん！ぼくがいろいろ教えてあげよう。" #CC_harry_tutorial_questscript03.mp3
QuestScript110_4 = "地図はキミが行ったところを示してるんだ。" #CC_harry_tutorial_questscript04.mp3
QuestScript110_5 = "ページをめくるとキミのギャグが…" #CC_harry_tutorial_questscript05.mp3
QuestScript110_6 = "ん～！ギャグが残ってないね！ キミに新しいタスクをあげよう。" #CC_harry_tutorial_questscript06.mp3
QuestScript110_7 = "キミのやらなきゃいけないタスクは次のページに書いてあるよ。" #CC_harry_tutorial_questscript07.mp3
QuestScript110_8 = "それじゃあトロリーに乗って、ギャグを買うためのジェリービーンを稼ぎに行こう！" #CC_harry_tutorial_questscript08.mp3
QuestScript110_9 = "まずはトロリー乗り場に行こう。ぼくの後ろのドアからプレイグラウンドへ出られるよ。" #CC_harry_tutorial_questscript09.mp3
QuestScript110_10 = "さぁ、トゥーンガイドをとじてトロリーをみつけて！" #CC_harry_tutorial_questscript10.mp3
QuestScript110_11 = "それがすんだら、トゥーンＨＱに戻るんだ。 じゃあね！" #CC_harry_tutorial_questscript11.mp3

QuestScriptTutorialBlocker_1 = "やぁ、こんにちは！" #CC_flippy_tutorial_blocker01.mp3
QuestScriptTutorialBlocker_2 = "あのぅ… こんにちは？？" #CC_flippy_tutorial_blocker02.mp3
QuestScriptTutorialBlocker_3 = "あ～、そうか！ スピードチャットの使い方がわからないんだね！" #CC_flippy_tutorial_blocker03.mp3
QuestScriptTutorialBlocker_4 = "そのボタンをクリックして、なにか言ってみて。" #CC_flippy_tutorial_blocker04.mp3
QuestScriptTutorialBlocker_5 = "その調子！！\aキミがこれから行くところには、話せるトゥーンがたくさんいるからね。"  #CC_flippy_tutorial_blocker05.mp3 \a CC_flippy_tutorial_blocker06.mp3
QuestScriptTutorialBlocker_6 = "キミの友だちとキーボードを使ってチャットしたい場合は、となりの青いボタンをつかうんだよ。" #CC_flippy_tutorial_blocker07.mp3
QuestScriptTutorialBlocker_7 = "\"チャット\"ボタンっていうんだけどこれを使うには、トゥーンタウンのオフィシャルメンバーになる必要があるんだ。" #CC_flippy_tutorial_blocker08.mp3
QuestScriptTutorialBlocker_8 = "がんばって！ じゃあまたあとでね！" #CC_flippy_tutorial_blocker09.mp3

"""
GagShopTut

違うタイプのギャグを使う能力をかせぐこともできるぞ。

"""

QuestScriptGagShop_1 = "ギャグショップへようこそ！"
QuestScriptGagShop_1a = "ここはトゥーンがコグと戦うためのギャグを買いに来る場所だよ。"
#QuestScriptGagShop_2 = "これはキミが持っているジェリービーンの数。"
#QuestScriptGagShop_3 = "ギャグを買うには、ギャグのボタンをクリックしてね。さっそくやってみて！"
QuestScriptGagShop_3 = "ギャグのボタンをクリックすれば、そのギャグを買えるよ！できるかな？"
QuestScriptGagShop_4 = "いいね！買ったギャグはコグと戦っているときに使えるよ！"
QuestScriptGagShop_5 = "「なげる」と「みずでっぽう」のレベルの高いギャグだよ！" #★
QuestScriptGagShop_6 = "ギャグの買い物が終わったら、このボタンを押してプレイグラウンドに戻ろう！"
QuestScriptGagShop_7 = "普段ならこのボタンを押すと、もう一度トロリーゲームで楽しめるんだけど…"
QuestScriptGagShop_8 = "…今回は時間がないから、今度ためしてみよう。トゥーンHQに向かってね！"

QuestScript120_1 = "よくトロリーをみつけたね！\aところで、銀行員のボブにあった？\aきれいな歯をしてるんだよ。\aこのチョコレートをおみやげに、彼に話しかけて自己紹介してみたら？"
QuestScript120_2 = "銀行員のボブは、トゥーンタウンバンクにいるよ。"

QuestScript121_1 = "おいしいチョコレートをありがとう！\aねぇ、ぼくを助けてくれたらごほうびをあげるよ。\aコグのやつら、ぼくのきんこのかぎを盗んだんだ。\aコグたちを倒して、盗まれたかぎをみつけておくれよ。\aかぎをみつけたら、ぼくに持ってきて！"

QuestScript130_1 = "よくトロリーをみつけたね！\aところで、今日ピート教授への荷物を受けとったんだ。\a彼が注文した新しいチョークにちがいないとおもうよ。\a彼にそれをとどけてくれないかなぁ？\a彼はスクールハウスにいるよ。"

QuestScript131_1 = "ああ、チョークありがとう。\aなんだ！？！\aああ、コグたちがわたしの黒板を盗んでいってしまったのか…。コグたちを倒して、盗まれた黒板をみつけてくれないか。\aみつけたら、わたしに持ってきてくれ。"

QuestScript140_1 = "よくトロリーをみつけたね！\aところで、ぼくにはかなりの読書中毒のとしょかんいんのラリーという友だちがいるんだ。\aこの間、ドナルドのハトバにいるとき、この本をひろったんだ。\a彼にこれを渡してくれないかい？彼はだいたいトゥーンタウンライブラリーにいるよ。"

QuestScript141_1 = "ありがとう、この本でぼくのコレクションはだいぶそろったな。\aどれどれ…\aんー、あれー…\aめがねどこにおいたかなぁ？\aあのコグたちがぼくんちの建物をのっとる前まではあったんだ。\aコグを倒して、ぼくの盗まれためがねをみつけてくれよ。\aみつけてもってきてくれたら、ごほうびをあげる！"

QuestScript145_1 = "トロリーは大丈夫だったみたいだね。\aよく聞いて！コグたちに「黒板消し」を盗まれてしまったんだ！\aストリートに出て、コグと戦って黒板消しを取り戻してくれない？\aストリートに行くにはこんな感じのトンネルを通ってね。"
QuestScript145_2 = "もし黒板消しを見つけたら、ここにもってきてくれないかな？\aギャグが必要だったら、トロリーに乗るんだよ。忘れないでね。\aそれと、ゲラゲラメーターをまんたんにしたかったら、プレイグラウンドのアイテムをひろってね！"

QuestScript150_1 = "あー… つぎのタスクはキミひとりではむずかしすぎるなぁ！"
QuestScript150_2 = "友だちをつくるには、他のプレイヤーをみつけて、あたらしい友だちボタンを使って"
QuestScript150_3 = "友だちをつくったらすぐ、ここに戻ってきてね。"
QuestScript150_4 = "いくつかのタスクは、ひとりでやるのにはむずかしすぎるよ！"

# To make sure the language checker is working
# DO NOT TRANSLATE THIS
MissingKeySanityCheck = "Ignore me"

SellbotBossName = "ｼﾆｱ ｺｸﾞｾﾞｷｭﾃｨﾌﾞ"
CashbotBossName = "マネーマネー"
LawbotBossName = "ﾁｰﾌ ｼﾞｬｽﾃｨｽ"
BossCogNameWithDept = "%(name)s\n%(dept)s"
BossCogPromoteDoobers = "キミは「格上げ」した！%s  おめでとう！"
BossCogDoobersAway = { 's' : "さあ、急いでウリアゲを上げて！" }
BossCogWelcomeToons = "ようこそ、新しいコグの仲間達！"
BossCogPromoteToons = "キミは「格上げ」した！%s  おめでとう！"
CagedToonInterruptBoss = "ねぇねぇ！\nこっちだよ！"
CagedToonRescueQuery = "キミたちは助けに来てくれたの？"
BossCogDiscoverToons = "は？ トゥーンめが！ ヘンソウしたってお見通しさ！"
BossCogAttackToons = "いざ！"
CagedToonDrop = [
    "やったね！彼を追い詰めたね。",
    "彼の後を追いかけて！  逃げようとしているよ！",
    "キミたちは本当にすごいね！",
    "ファンタスティック！  彼をやっつけたも\n同然だね！",
    ]
CagedToonPrepareBattleTwo = "ねぇ見て！ 彼が逃げようとしているぞ！\aみんな、助けて！彼を止めて！"
CagedToonPrepareBattleThree = "ふーっ、\nもうすぐ自由だ！\aコグゼキュティブを\n直接、攻撃しよう！\aキミが使えるパイをたくさん手に入れたよ！\aジャンプして、オリの底にさわればキミにパイを渡せるんだ！\aパイを手に入れたら\nInsertキーを押してみよう！\aパイを投げることが出来るよ！"
BossBattleNeedMorePies = "もっとパイが必要だよ！"
BossBattleHowToGetPies = "オリのところまでジャンプして、パイを手に入れよう！"
BossBattleHowToThrowPies = "Insertキーを押すとパイを投げるぞ！"
CagedToonYippee = "いやっほう！"
CagedToonThankYou = "やった～！自由になったぞ！\a本当にありがとう！\a大きな借りができたね。\aもしバトルで助けが必要になったら、電話して！\aＳＯＳボタンを押せば、呼ぶことができるよ！"
CagedToonPromotion = "\aコグゼキュティブがキミの「格上げ」の紙を置き忘れたみたいだよ。\aキミのために取っておくから、後で「格上げ」されるはずだよ！"
CagedToonLastPromotion = "\aワオ！キミのコグスーツ、とうとうレベル%sまできたね。\aそれ以上は格上げされないよ。\aこれ以上はスーツをアップグレードできないけど、もちろんトゥーンを助けに行けるよ。"
CagedToonHPBoost = "\aキミはこの本部からたくさんのトゥーンの仲間達を助けたね！\aトゥーン本部はキミにさらなるゲラゲラブーストをあげることにしたよ！おめでとう！"
CagedToonMaxed = "\aコグのスーツがレベル%sに達したね。本当に素晴らしい！\aトゥーン本部に代わって、もっとトゥーンを助けに戻ってきてくれたことに感謝するよ！"
CagedToonGoodbye = "それでは！"


CagedToonBattleThree = {
    10: "いいジャンプだよ、%(toon)s。  パイをどうぞ！",
    11: "やあ、%(toon)s！  パイをどうぞ！",
    12: "こんにちは、%(toon)s！  パイを手に入れたよ！",
    
    20: "ねぇ、%(toon)s！  オリのところまでジャンプして、パイを投げて！",
    21: "おーい、%(toon)s!  Ctrlキーを使ってジャンプして、オリをさわって！",
    
    100: "Insertキーを押すとパイを投げるよ！",
    101: "パイがどのくらい飛ぶかは青いパワーメーターでわかるよ！",
    102: "まず彼の土台に向けてパイを投げて、彼の動きを狂わせよう！",
    103: "ドアが開くのを待って、中にパイを投げ込もう！",
    104: "彼がうろたえているときに、顔をねらうか、おなかをねらってあとずさりさせよう！",
    105: "当たったときの色をみればちゃんとギャグが決まったかがわかるよ！",
    106: "トゥーンにパイがあたると、トゥーンのゲラゲラメーターが回復するよ！",
    }
CagedToonBattleThreeMaxGivePies = 12
CagedToonBattleThreeMaxTouchCage = 21
CagedToonBattleThreeMaxAdvice = 106

CashbotBossHadEnough = "ええい！しぶといトゥーン達にはもううんざりだ！"
CashbotBossOuttaHere = "電車の時間に間に合わないから帰るぞ！！"
ResistanceToonName = "マタ・ヘアリー"
ResistanceToonCongratulations = "やったね！おめでとう！\aレジスタンスの仲間入りだ！\aピンチの時のあいことばを教えてあげるね。\a%s\a「%s」\a一度しか使えないから、ちゃんとタイミング考えよう！"
ResistanceToonToonupInstructions = "キミの近くのトゥーンみんなが%sゲラゲラポイントをゲット！"
ResistanceToonToonupAllInstructions = "キミの近くのトゥーンみんなのゲラゲラポイントが回復！"
ResistanceToonMoneyInstructions = "キミの近くのトゥーンみんなが%sジェリービーンをゲット！"
ResistanceToonMoneyAllInstructions = "キミの近くのトゥーンみんなのジェリービーンをゲット！"
ResistanceToonRestockInstructions = "キミの近くのトゥーンみんなの\"%s\"ギャグが回復！"
ResistanceToonRestockAllInstructions = "キミの近くのトゥーンみんなのギャグが回復！"

ResistanceToonLastPromotion = "\aワオ！コグスーツがレベル%sになったね！\aコグは今のレベル以上にはなれないんだ。\aだからコグスーツのレベルも上がらないんだけど、レジスタンスのためにこれからもがんばって！"
ResistanceToonHPBoost = "\aレジスタンスのために本当にがんばってくれているね！\aトゥーンひょうぎかいがキミにゲラゲラポイントをあげるって！おめでとう！"
ResistanceToonMaxed = "\aレベル%sのコグスーツを手に入れたんだね！すばらしいよ！\aトゥーンひょうぎかいにかわって、トゥーン達を助けにもどってくれたことに心からかんしゃします！"

CashbotBossCogAttack = "つかまえろ！！"
ResistanceToonWelcome = "キミ、やったね！マネーマネーが僕らを見つける前に金庫室まで行こう！"
ResistanceToonTooLate = "ちぇっ、おそすぎた！"
CashbotBossDiscoverToons1 = "クンクン…！"
CashbotBossDiscoverToons2 = "はーはっは！思ったとおりだ！トゥーンのにおいがしたんだよ。にせものめ！"
ResistanceToonKeepHimBusy = "マネーマネーの気をそらして！これからワナをしかけるから！"
ResistanceToonWatchThis = "よーく、見ててね！"
CashbotBossGetAwayFromThat = "ねぇ！それからはなれて！"
ResistanceToonCraneInstructions1 = "台にのぼって、じしゃくをコントロールしよう！"
ResistanceToonCraneInstructions2 = "やじるしキーを使ってクレーンを動かして、Ctrlキーでモノをつかめるよ。"
ResistanceToonCraneInstructions3 = "じしゃくで金庫をつかんで、マネーマネーの安全ヘルメットをはずそう！"
ResistanceToonCraneInstructions4 = "ヘルメットが取れたら、動かなくなったグーンをつかんで頭にあてよう！"
ResistanceToonGetaway = "おーっと！にげろ！"
CashbotCraneLeave = "クレーンからはなれる"
CashbotCraneAdvice = "やじるしキーを使うとクレーンのあたまが動くよ。"
CashbotMagnetAdvice = "CTRLキーを押すとモノをつかめるよ。"
CashbotCraneLeaving = "クレーンからはなれているところ"

MintElevatorRejectMessage = "キミの%sコグスーツを完成させるまでは、中に入れないよ！"
BossElevatorRejectMessage = "キミのトゥーンが「格上げ」されるまでは、このエレベーターに乗ることはできません。"
NotYetAvailable = "このエレベーターにはまだ乗れないよ"

# Types of catalog items--don't translate yet.
FurnitureTypeName = "家具"
PaintingTypeName = "絵"
ClothingTypeName = "洋服"
ChatTypeName = "新しいフレーズ"
EmoteTypeName = "演技のレッスン"
BeanTypeName = "ジェリービーン"
PoleTypeName = "釣りざお"
WindowViewTypeName = "窓の景色"
PetTrickTypeName = "ﾄﾞｩｰﾄﾞｩﾙ\nﾄﾚｰﾆﾝｸﾞ"
GardenTypeName = "ガーデンアイテム"
RentalTypeName = "レンタルアイテム"
GardenStarterTypeName = "ガーデニングキット"
NametagTypeName = "ネームタグ"


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
    'bss1' : "むじ",
    'bss2' : "ｽﾄﾗｲﾌﾟ",
    'bss3' : "ﾎﾟﾛｼｬﾂ",
    'bss4' : "ﾀﾞﾌﾞﾙ ｽﾄﾗｲﾌﾟ",
    'bss5' : "しまもよう",
    'bss6' : "ﾎﾟｹｯﾄﾎﾟﾛ",
    'bss7' : "ﾊﾜｲｱﾝ",
    'bss8' : "2 ﾎﾟｹｯﾄﾎﾟﾛ",
    'bss9' : "ﾎﾞｰﾘﾝｸﾞｼｬﾂ",
    'bss10' : "ﾍﾞｽﾄ(ｽﾍﾟｼｬﾙ)",
    'bss11' : "ﾗｯﾌﾙ ﾎﾟﾛ",
    'bss12' : "ｻｯｶｰ ｼﾞｬｰｼﾞ(ｽﾍﾟｼｬﾙ)",
    'bss13' : "ﾗｲﾄﾆﾝｸﾞ(ｽﾍﾟｼｬﾙ)",
    'bss14' : "19ｼﾞｬｰｼﾞ(ｽﾍﾟｼｬﾙ)",
    'bss15' : "ﾒｷｼｶﾝ",

    # -------------------------------------------------------------------------
    # Girl styles
    # -------------------------------------------------------------------------
    'gss1' : "むじ",
    'gss2' : "ｽﾄﾗｲﾌﾟ",
    'gss3' : "ﾎﾟﾛｼｬﾂ",
    'gss4' : "ﾀﾞﾌﾞﾙｽﾄﾗｲﾌﾟ",
    'gss5' : "ﾎﾟｹｯﾄﾎﾟﾛ",
    'gss6' : "ﾌﾗﾜｰﾌﾟﾘﾝﾄ",
    'gss7' : "はながら(ｽﾍﾟｼｬﾙ)",
    'gss8' : "2ﾎﾟｹｯﾄﾎﾟﾛ",
    'gss9' : "ﾃﾞﾆﾑﾍﾞｽﾄ(ｽﾍﾟｼｬﾙ)",
    'gss10' : "ﾁｭﾆｯｸ",
    'gss11' : "ｽﾄﾗｲﾌﾟ ﾁｭﾆｯｸ",
    'gss12' : "ｻｯｶｰｼﾞｬｰｼﾞ(ｽﾍﾟｼｬﾙ)",
    'gss13' : "ﾊｰﾄ",
    'gss14' : "ｽﾀｰ(ｽﾍﾟｼｬﾙ)",
    'gss15' : "ﾌﾗﾜｰ",

    # -------------------------------------------------------------------------
    # Special Catalog-only shirts. 
    # -------------------------------------------------------------------------
    # yellow hooded - Series 1
    'c_ss1' : "ｼﾘｰｽﾞ1 ﾊﾟｰｶｰ",
    'c_ss2' : "ｼﾘｰｽﾞ1 やしの木",
    'c_ss3' : "ｼﾘｰｽﾞ2 ｽﾀｰ",
    'c_bss1' : "ｼﾘｰｽﾞ1 ｽﾄﾗｲﾌﾟ(男の子)",
    'c_bss2' : "ｼﾘｰｽﾞ1 ｵﾚﾝｼﾞ (男の子) ",
    'c_bss3' : "ｼﾘｰｽﾞ2 ｽﾄﾗｲﾌﾟ(男の子)",
    'c_bss4' : "ｼﾘｰｽﾞ2 ﾁｪｯｸ(男の子)",
    'c_gss1' : "ｼﾘｰｽﾞ1 ｽﾄﾗｲﾌﾟ(女の子)",
    'c_gss2' : "ｼﾘｰｽﾞ1 ﾌﾗﾜｰ(女の子)",
    'c_gss3' : "ｼﾘｰｽﾞ2 ｳｪｰﾌﾞ(女の子)",
    'c_gss4' : "ｼﾘｰｽﾞ2 ﾘﾎﾞﾝ(女の子)",
    'c_gss5' : "ｱｸｱｽﾄﾗｲﾌﾟ(女の子)",
    'c_ss4'  : "ｼﾘｰｽﾞ3 ﾀｲﾀﾞｲ",
    'c_ss5' : "ｼﾘｰｽﾞ3 ｽﾄﾗｲﾌﾟ(男の子)",
    'c_ss6' : "ｼﾘｰｽﾞ4 ｶｳﾎﾞｰｲｼｬﾂ1",
    'c_ss7' : "ｼﾘｰｽﾞ4 ｶｳﾎﾞｰｲｼｬﾂ 2",
    'c_ss8' : "ｼﾘｰｽﾞ4 ｶｳﾎﾞｰｲｼｬﾂ 3",
    'c_ss9' : "ｼﾘｰｽﾞ4 ｶｳﾎﾞｰｲｼｬﾂ 4",
    'c_ss10' : "ｼﾘｰｽﾞ4 ｶｳﾎﾞｰｲｼｬﾂ 5",
    'c_ss11' : "ｼﾘｰｽﾞ 4 ｶｳﾎﾞｰｲｼｬﾂ 6",
    
    # Special Holiday-themed shirts.
    'hw_ss1' : "ｺﾞｰｽﾄ",
    'hw_ss2' : "ﾊﾟﾝﾌﾟｷﾝ",
    'wh_ss1' : "ｳｨﾝﾀｰﾎﾘﾃﾞｰ 1",
    'wh_ss2' : "ｳｨﾝﾀｰﾎﾘﾃﾞｰ 2",
    'wh_ss3' : "ｳｨﾝﾀｰﾎﾘﾃﾞｰ 3",
    'wh_ss4' : "ｳｨﾝﾀｰﾎﾘﾃﾞｰ 4",

    'vd_ss1' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ 赤いﾊｰﾄ(女の子)",
    'vd_ss2' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ 白いﾊｰﾄ",
    'vd_ss3' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ はね付きﾊｰﾄ(男の子)",
    'vd_ss4' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ 炎のﾊｰﾄ",
    'vd_ss5' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ ｷｭｰﾋﾟｯﾄﾞ",
    'vd_ss6' : "ﾊﾞﾚﾝﾀｲﾝﾃﾞｰ､ 緑と赤のﾊｰﾄ",
    'sd_ss1' : "ｾﾝﾄ ﾊﾟﾄﾘｯｸﾃﾞｰ､ 四葉のｸﾛｰﾊﾞ",
    'sd_ss2' : "ｾﾝﾄ ﾊﾟﾄﾘｯｸﾃﾞｰ､ 金のつぼ",
    'tc_ss1' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ ﾌｨｯｼﾝｸﾞﾍﾞｽﾄ",
    'tc_ss2' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ 金魚ばち",
    'tc_ss3' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ 足あと",
    'tc_ss4' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ ﾊﾞｯｸﾊﾟｯｸ",
    'tc_ss5' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ 短パン",
    'tc_ss6' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ ｽｲｶ",
    'tc_ss7' : "T-ｼｬﾂ ｺﾝﾃｽﾄ､ ﾚｰｽ",
    'j4_ss1' : "July 4th, ﾌﾗｯｸﾞ",
    'j4_ss2' : "July 4th, 花火",
    'c_ss12' : "ｶﾀﾛｸﾞｼﾘｰｽﾞ7, 黄ﾎﾞﾀﾝ",
    'c_ss13' : "ｶﾀﾛｸﾞｼﾘｰｽﾞ7, ﾋﾞｯｸﾞ ﾌﾗﾜｰ",

    'pj_ss1' : "青 ﾊﾞﾅﾅｼｬﾂ",
    'pj_ss2' : "赤 ﾎｰﾝｼｬﾂ",
    'pj_ss3' : "紫 ﾒｶﾞﾈｼｬﾂ",
    
    # Special award clothes
    'sa_ss1' : "ｽﾄﾗｲﾌﾟ ｼｬﾂ",
    'sa_ss2' : "ﾌｨｯｼﾝｸﾞ ｼｬﾂ1",
    'sa_ss3' : "ﾌｨｯｼﾝｸﾞ ｼｬﾂ 2",
    'sa_ss4' : "ｶﾞｰﾃﾞﾆﾝｸﾞ ｼｬﾂ 1",
    'sa_ss5' : "ｶﾞｰﾃﾞﾆﾝｸﾞ ｼｬﾂ 2",
    'sa_ss6' : "ﾊﾟｰﾃｨｰ ｼｬﾂ 1",
    'sa_ss7' : "ﾊﾟｰﾃｨｰ ｼｬﾂ 2",    
    'sa_ss8' : "ﾚｰｼﾝｸﾞ ｼｬﾂ 1",    
    'sa_ss9' : "ﾚｰｼﾝｸﾞ ｼｬﾂ 2",    
    'sa_ss10' : "ｻﾏｰ ｼｬﾂ 1",    
    'sa_ss11' : "ｻﾏｰ ｼｬﾂ 2",    

    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    }

# Make sure this is in sync with ToonDNA.BottomStyles
BottomStylesDescriptions = {
    # name : [ bottomIdx, [bottomColorIdx, ...]]
    # -------------------------------------------------------------------------
    # Boy styles (shorts)
    # -------------------------------------------------------------------------
    'bbs1' : "ﾎﾟｹｯﾄ付き",
    'bbs2' : "ﾍﾞﾙﾄ",
    'bbs3' : "ｶｰｺﾞ",
    'bbs4' : "ﾊﾜｲｱﾝ",
    'bbs5' : "ｻｲﾄﾞ ｽﾄﾗｲﾌﾟ (ｽﾍﾟｼｬﾙ)",
    'bbs6' : "ｻｯｶｰ ｼｬﾂ",
    'bbs7' : "ｻｲﾄﾞ ﾌﾚｲﾑ (ｽﾍﾟｼｬﾙ)",
    'bbs8' : "ﾃﾞﾆﾑ",
    'vd_bs1' : "ﾊﾞﾚﾝﾀｲﾝ ｼｮｰﾄﾊﾟﾝﾂ",
    'vd_bs2' : "赤 ﾊｰﾄ",
    'vd_bs3' : "ﾃﾞﾆﾑ 緑・赤ﾊｰﾄ",

    # Catalog only shorts
    'c_bs1' : "ﾌﾞﾙｰのｻｲﾄﾞ ｽﾄﾗｲﾌﾟ",
    'c_bs2' : "ｺﾞｰﾙﾄﾞ ｶﾌｽ ｽﾄﾗｲﾌﾟ",
    'c_bs5' : 'ｼﾘｰｽﾞ7  - ｸﾞﾘｰﾝｽﾄﾗｲﾌﾟ',
    'sd_bs1' : 'ﾚﾌﾟﾗｺｰﾝ ﾊﾟﾝﾂ',
    'pj_bs1' : 'ﾊﾞﾅﾅ ﾊﾟｼﾞｬﾏ ﾊﾟﾝﾂ',
    'pj_bs2' : 'ﾎｰﾝ ﾊﾟｼﾞｬﾏ ﾊﾟﾝﾂ',
    'pj_bs3' : 'ﾒｶﾞﾈ ﾊﾟｼﾞｬﾏ ﾊﾟﾝﾂ',
    'wh_bs1' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ 短パン1',
    'wh_bs2' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ 短パン2',
    'wh_bs3' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ 短パン3',
    'wh_bs4' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ 短パン4',

    
    # -------------------------------------------------------------------------
    # Girl styles (shorts and skirts)
    # -------------------------------------------------------------------------
    # skirts
    # -------------------------------------------------------------------------
    'gsk1' : '無地',
    'gsk2' : 'ﾎﾟﾙｶ ﾄﾞｯﾄ(ｽﾍﾟｼｬﾙ)',
    'gsk3' : 'ﾀﾃｼﾏ',
    'gsk4' : 'ﾖｺｼﾏ',
    'gsk5' : 'ﾌﾗﾜｰ',
    'gsk6' : '2-ﾎﾟｹｯﾄ(ｽﾍﾟｼｬﾙ) ',
    'gsk7' : 'ﾃﾞﾆﾑ ｽｶｰﾄ',
    
    # shorts
    # -------------------------------------------------------------------------
    'gsh1' : 'ポケット付',
    'gsh2' : 'ﾌﾗﾜｰ',
    'gsh3' : 'ﾃﾞﾆﾑ 短パン',
    # Special catalog-only skirts and shorts.
    'c_gsk1' : 'ﾎﾞｰﾀﾞｰ&ﾎﾞﾀﾝ付',
    'c_gsk2' : 'ﾘﾎﾞﾝ付',
    'c_gsk3' : '星',

    # Valentines skirt
    'vd_gs1' : 'ハート',
    'vd_gs2' : 'ﾎﾟﾙｶ ﾊｰﾄ',
    'vd_gs3' : '緑・赤のﾊｰﾄ',
    'c_gsk4' : 'ﾚｲﾝﾎﾞｰ ? ｼﾘｰｽﾞ3',
    'sd_gs1' : 'St. ﾊﾟﾄﾘｯｸ 短パン',
    'c_gsk5' : 'ｳｴｽﾀﾝ ｽｶｰﾄ1',
    'c_gsk6' : 'ｳｴｽﾀﾝ ｽｶｰﾄ2',
    # Western shorts
    'c_bs3' : 'ｳｴｽﾀﾝ 短パン1',
    'c_bs4' : 'ｳｴｽﾀﾝ 短パン 2',
    'j4_bs1' : 'July 4th 短パン',
    'j4_gs1' : 'July 4th ｽｶｰﾄ',
    'c_gsk7' : 'ﾌﾗﾜｰ ? ｼﾘｰｽﾞ7',
    'pj_gs1' : 'ﾊﾞﾅﾅ ﾊﾟｼﾞｬﾏ ﾊﾟﾝﾂ',
    'pj_gs2' : 'ﾎｰﾝ ﾊﾟｼﾞｬﾏ ﾊﾟﾝﾂ',
    'pj_gs3' : 'ﾒｶﾞﾈ ﾊﾟｼﾞｬﾏ  ﾊﾟﾝﾂ',
    'wh_gsk1' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ ｽｶｰﾄ1',
    'wh_gsk2' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ ｽｶｰﾄ2',
    'wh_gsk3' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ ｽｶｰﾄ3',
    'wh_gsk4' : 'ｳｨﾝﾀｰﾎﾘﾃﾞｰ ｽｶｰﾄ4',
    
    'sa_bs1' : "ﾌｨｯｼﾝｸﾞ 短パン",
    'sa_bs2' : "ｶﾞｰﾃﾞﾆﾝｸﾞ 短パン",
    'sa_bs3' : "ﾊﾟｰﾃｨｰ 短パン",
    'sa_bs4' : "ﾚｰｼﾝｸﾞ 短パン",
    'sa_bs5' : "ｻﾏｰ 短パン",
    'sa_gs1' : "ﾌｨｯｼﾝｸﾞ ｽｶｰﾄ",
    'sa_gs2' : "ｶﾞｰﾃﾞﾆﾝｸﾞ  ｽｶｰﾄ",    
    'sa_gs3' : "ﾊﾟｰﾃｨｰｽｶｰﾄ",    
    'sa_gs4' : "ﾚｰｼﾝｸﾞ ｽｶｰﾄ",    
    'sa_gs5' : "ｻﾏｰ ｽｶｰﾄ",
    }

AwardMgrBoy = "男の子"
AwardMgrGirl = "女の子"
AwardMgrUnisex = "男女"
AwardMgrShorts = "短パン"
AwardMgrSkirt = "スカート"
AwardMgrShirt = "シャツ"

# Special Event Strings to display in  mailbox screen
SpecialEventMailboxStrings = {
    1 : "トゥーン評議会からのスペシャルアイテム",
    2 : "メルビルのフィッシングトーナメントの賞品",
    3 : "ビリー・バドのフィッシングトーナメントの商品",    
    }

#rental names
RentalHours = "時間"
RentalOf = "の"
RentalCannon = "ﾚﾝﾀﾙｷｬﾉﾝ"
RentalGameTable = "ｹﾞｰﾑ・ﾃｰﾌﾞﾙ!"

EstateCannonGameEnd = "キャノンのレンタルが終わりました。"
GameTableRentalEnd = "ゲーム・テーブルのレンタルが終わりました。"

MessageConfirmRent = "レンタルする？後でレンタルしたければキャンセルしてね。"
MessageConfirmGarden = "ガーデニングするかい？"

#nametag Names
NametagPaid = "シチズン・ネームタグ"
NametagAction = "デザイン・ネームタグ"
NametagFrilly = "ポップ・ネームタグ"

MessageConfirmRent = "レンタルする？後でレンタルしたければキャンセルしてね。"
MessageConfirmGarden = "ガーデニングするかい？"

FurnitureYourOldCloset = "キミの古いクローゼット"
FurnitureYourOldBank = "キミの古い銀行"

# How to put quotation marks around chat items--don't translate yet.
ChatItemQuotes = '"%s"'

# CatalogFurnitureItem.py--don't translate yet.
FurnitureNames = {
  100 : "ひじかけいす",
  105 : "ひじかけいす",
  110 : "いす",
  120 : "ﾃﾞｽｸﾁｪｱ",
  130 : "ﾛｸﾞﾁｪｱ",
  140 : "ﾛﾌﾞｽﾀｰﾁｪｱ",
  145 : "ﾗｲﾌｼﾞｬｹｯﾄﾁｪｱ",
  150 : "サドルスツール",
  160 : "ﾈｲﾃｨﾌﾞﾁｪｱー",
  170 : "ｶｯﾌﾟｹｰｷﾁｪｱｰ",
  200 : "ベッド",
  205 : "ベッド",
  210 : "ベッド",
  220 : "バスタブベッド",
  230 : "はっぱのベッド",
  240 : "ボートのベッド",
  250 : "ﾄｹﾞﾄｹﾞﾊﾝﾓｯｸ",
  260 : "ｱｲｽｸﾘｰﾑﾍﾞｯﾄﾞ",
  270 : "エリンとネコのベッド",
  300 : "プレイヤーピアノ",
  310 : "パイプオルガン",
  400 : "だんろ",
  410 : "だんろ",
  420 : "まるいだんろ",
  430 : "だんろ",
  440 : "りんごのだんろ",
  450 : "エリンのだんろ",
  500 : "クローゼット",
  502 : "クローゼット(15)",
  504 : "クローゼット(20)",
  506 : "クローゼット(25)",
  510 : "クローゼット",
  512 : "クローゼット(15)",
  514 : "クローゼット(20)",
  516 : "クローゼット(25)",
  600 : "小さいスタンド",
  610 : "大きいスタンド",
  620 : "テーブルライト",
  625 : "テーブルライト",
  630 : "ひなぎくのランプ",
  640 : "ひなぎくのランプ",
  650 : "くらげのランプ",
  660 : "くらげのランプ",
  670 : "カウボーイランプ",
  700 : "ふかふかのいす",
  705 : "ふかふかのいす",
  710 : "ソファ",
  715 : "ソファ",
  720 : "わらのカウチ",
  730 : "ｼｮｰﾄｹｰｷｶｳﾁ",
  800 : "つくえ",
  810 : "ログデスク",
  900 : "かさたて",
  910 : "コートかけ",
  920 : "ごみばこ",
  930 : "赤いキノコ",
  940 : "黄色いキノコ",
  950 : "コート掛け",
  960 : "タルのスタンド",
  970 : "サボテン",
  980 : "テント小屋",
  990 : "ジュリエットのせんす",
  1000 : "大きなじゅうたん",
  1010 : "丸いじゅうたん",
  1015 : "丸いじゅうたん",
  1020 : "小さいじゅうたん",
  1030 : "葉っぱのマット",
  1100 : "かざりだな",
  1110 : "かざりだな",
  1120 : "背のたかい本だな",
  1130 : "背のひくい本だな",
  1140 : "サンデーチェスト",
  1200 : "サイドテーブル",
  1210 : "小さいテーブル",
  1215 : "小さいテーブル",
  1220 : "コーヒーテーブル",
  1230 : "コーヒーテーブル",
  1240 : "ｼｭﾉｰｹﾙﾃｰﾌﾞﾙ",
  1250 : "クッキーテーブル",
  1260 : "ﾍﾞｯﾄﾞﾙｰﾑﾃｰﾌﾞﾙ",
  1300 : "1000コ貯ビーン箱",
  1310 : "2500コ貯ビーン箱",
  1320 : "5000コ貯ビーン箱",
  1330 : "7500コ貯ビーン箱",
  1340 : "10000コ貯ビーン箱",
  1399 : "電話",
  1400 : "ｾｻﾞﾝﾇ･ﾄｩｰﾝの絵",
  1410 : "お花",
  1420 : "モダン・ミッキー",
  1430 : "ﾚﾝﾌﾞﾗﾝﾄ･ﾄｩｰﾝの絵",
  1440 : "トゥーンスケープ",
  1441 : "ホイッスルホース",
  1442 : "トゥーンスター",
  1443 : "「パイじゃない」",
  1500 : "ラジオ",
  1510 : "ラジオ",
  1520 : "ラジオ",
  1530 : "テレビ",
  1600 : "背のひくい花びん",
  1610 : "背のたかい花びん",
  1620 : "背のひくい花びん",
  1630 : "背のたかい花びん",
  1640 : "花びん",
  1650 : "花びん",
  1660 : "サンゴの花びん",
  1661 : "貝がらの花びん",
  1700 : "ﾎﾟｯﾌﾟｺｰﾝｶｰﾄ",
  1710 : "てんとう虫",
  1720 : "ふんすい",
  1725 : "洗濯機",
  1800 : "キンギョばち",
  1810 : "キンギョばち",
  1900 : "メカジキ",
  1910 : "シュモクザメ",
  1920 : "ツノのかべかけ",
  1930 : "ｼﾝﾌﾟﾙ･ｿﾝﾌﾞﾚﾛ",
  1940 : "ﾌｧﾝｼｰ･ｿﾝﾌﾞﾚﾛ",
  1950 : "ﾄﾞﾘｰﾑｷｬｯﾁｬｰ",
  1960 : "ひづめ",
  1970 : "バイソンの絵",
  2000 : "ｷｬﾝﾃﾞｨｰｽｳｨﾝｸﾞｾｯﾄ",
  2010 : "ケーキスライド",
  3000 : "ﾊﾞﾅﾅｽﾌﾟﾘｯﾄﾀﾌﾞ",
  10000 : "丸いかぼちゃ",
  10010 : "細長いかぼちゃ",
  10020 : "ｳｨﾝﾀｰ・ﾂﾘｰ",
  10030 : "ｳｨﾝﾀｰ・ﾘｰｽ"
  }

# CatalogClothingItem.py--don't translate yet.
ClothingArticleNames = (
    "シャツ",
    "シャツ",
    "シャツ",
    "短パン",
    "短パン",
    "スカート",
    "短パン",
    )

ClothingTypeNames = {
    1400 : "ﾏｼｭｰのｼｬﾂ",
    1401 : "ｼﾞｪｼｶのｼｬﾂ",
    1402 : "ﾏﾘｯｻのｼｬﾂ",
    1600 : "ワナの洋服",
    1601 : "サウンドの洋服",
    1602 : "おとりの洋服",
    1603 : "ワナの洋服",
    1604 : "サウンドの洋服",
    1605 : "おとりの洋服",
    1606 : "ワナの洋服",
    1607 : "サウンドの洋服",
    1608 : "おとりの洋服",
    }

# CatalogSurfaceItem.py--don't translate yet.
SurfaceNames = (
    "かべがみ",
    "いがた",
    "床",
    "腰板",
    "へり",
    )

WallpaperNames = {
    1000 : "パーチメント",
    1100 : "ミラノ",
    1200 : "ドーバー",
    1300 : "ビクトリア",
    1400 : "ニューポート",
    1500 : "パストラル",
    1600 : "ハーレクイン",
    1700 : "ムーン",
    1800 : "スター",
    1900 : "フラワー",
    2000 : "ｽﾌﾟﾘﾝｸﾞｶﾞｰﾃﾞﾝ",
    2100 : "ﾌｫｰﾏﾙｶﾞｰﾃﾞﾝ",
    2200 : "勝負の日",
    2300 : "タッチダウン！",
    2400 : "くも",
    2500 : "つた",
    2600 : "春",
    2700 : "こけし",
    2800 : "花束",
    2900 : "ｴﾝｾﾞﾙﾌｨｯｼｭ",
    3000 : "バブル",
    3100 : "バブル",
    3200 : "ｺﾞｰﾌｨｯｼｭ",
    3300 : "ｽﾄｯﾌﾟﾌｨｯｼｭ",
    3400 : "たつのおとしご",
    3500 : "貝がら",
    3600 : "深海",
    3700 : "ブーツ",
    3800 : "さぽてん",
    3900 : "ｶｳﾎﾞｰｲﾊｯﾄ",
    10100 : "ねこ",
    10200 : "こうもり",
    11000 : "雪のけっしょう",
    11100 : "葉っぱ",
    11200 : "雪だるま",
    13000 : "クローバー",
    13100 : "クローバー",
    13200 : "レインボー",
    13300 : "クローバー",
    }

FlooringNames = {
    1000 : "ウッドフロア",
    1010 : "カーペット",
    1020 : "ﾀﾞｲﾔﾓﾝﾄﾞﾀｲﾙ",
    1030 : "ﾀﾞｲﾔﾓﾝﾄﾞﾀｲﾙ",
    1040 : "しばふ",
    1050 : "茶色いレンガ",
    1060 : "赤いレンガ",
    1070 : "四角いタイル",
    1080 : "石",
    1090 : "遊歩道",
    1100 : "つち",
    1110 : "木のタイル",
    1120 : "タイル",
    1130 : "ハチの巣",
    1140 : "みず",
    1150 : "ビーチタイル",
    1160 : "ビーチタイル",
    1170 : "ビーチタイル",
    1180 : "ビーチタイル",
    1190 : "すな",
    10000 : "アイスキューブ",
    10010 : "イグルー",
    11000 : "クローバー",
    11010 : "クローバー",
    }

MouldingNames = {
    1000 : "節目",
    1010 : "クラシック",
    1020 : "ぼこぼこ",
    1030 : "花がら",
    1040 : "花がら",
    1050 : "てんとうむし",
    }

WainscotingNames = {
    1000 : "ペンキ",
    1010 : "木のパネル",
    1020 : "木",
    }

# CatalogWindowItem.py--don't translate yet.
WindowViewNames = {
    10 : "おおきな庭",
    20 : "ワイルドな庭",
    30 : "ギリシャ風の庭",
    40 : "都市の風景",
    50 : "ウェスタン",
    60 : "水中",
    70 : "ﾄﾛﾋﾟｶﾙｱｲﾗﾝﾄﾞ",
    80 : "星空",
    90 : "チキプール",
    100 : "南極",
    110 : "農場",
    120 : "キャンプ",
    130 : "大通り",
    }


# don't translate yet
NewCatalogNotify = "電話で注文できる新しい品物があるわよ！"
NewDeliveryNotify = "キミのメールボックスに荷物が届いているわよ。"
CatalogNotifyFirstCatalog = "最初のカタログが届いたわよ！ 楽しいアイテムでおしゃれしたり、家の模様替えができるわよ。"
CatalogNotifyNewCatalog = "カタログVol%sが届いたわよ！ 電話で商品を注文してね。"
CatalogNotifyNewCatalogNewDelivery = "注文した商品がメールボックスに 届いたわよ！ カタログＶＯＬ%sも届いているわよ！"
CatalogNotifyNewDelivery = "注文した商品がメールボックスに届いたわよ！"
CatalogNotifyNewCatalogOldDelivery = "カタログVol%sが届いたわよ！注文した商品がまだメールボックスに残っているわよ！"
CatalogNotifyOldDelivery = "注文した商品がまだメールボックスに残っているわよ！"
CatalogNotifyInstructions = "トゥーンガイドの\"家に帰る\"ボタンを押して、おうちの電話まで行ってね！"
CatalogNewDeliveryButton = "商品が\n届いたよ"
CatalogNewCatalogButton = "新しい\nカタログ"
CatalogSaleItem = ""

# don't translate yet
DistributedMailboxEmpty = "いまキミのメールボックスはからっぽだよ。電話注文したあとに、荷物をチェックしにここへ戻ってきて！"
DistributedMailboxWaiting = "いまキミのメールボックスはからっぽだけど、キミの注文した荷物はこちらに向かっているよ。あとでまたチェックしてみて！"
DistributedMailboxReady = "キミの注文したものがとどいたよ！"
DistributedMailboxNotOwner = "ごめん、これはキミのメールボックスじゃないね。"
DistributedPhoneEmpty = "キミとキミの家向けの特別品は、どの電話からでも注文できるよ。あたらしい品物は営業時間外に注文することができるんだ。\n\n今すぐ注文できるものはないので、あとでチェックしにきてね！"

# don't translate yet
Clarabelle = "クララベル"
MailboxExitButton = "メールボックスを閉じる"
MailboxAcceptButton = "荷物をうけとる"
MailBoxDiscard = "このアイテムをすてる" #localize
MailboxAcceptInvite = "さんかする"
MailBoxRejectInvite = "さんかしない"
MailBoxDiscardVerify = "本当に %s をすててもいい?"
MailBoxRejectVerify = "Are you sure you want to Reject %s?"
MailboxOneItem = "品物が1つ届いています。"
MailboxNumberOfItems = "品物が%sつ届いています。"
MailboxGettingItem = "%s\nを取り出しました。"
MailboxGiftTag = "%s からのおくりもの"
MailboxGiftTagAnonymous = "とくめい"
MailboxItemNext = "次の\nアイテム"
MailboxItemPrev = "前の\nアイテム"
MailboxDiscard = "すてる"
MailboxReject = "Reject"
MailboxLeave = "とっておく"
CatalogCurrency = "ジェリービーン"
CatalogHangUp = "電話を切る"
CatalogNew = "しんせいひん"
CatalogBackorder = "バックオーダー"
CatalogLoyalty = "スペシャル"
CatalogPagePrefix = "ページ"
CatalogGreeting = "お電話ありがとうございます。\nクララベルのショッピングカタログです。ご注文は？"
CatalogGoodbyeList = ["それじゃ！",
                      "またお電話くださいね！",
                      "お電話ありがとう！",
                      "またどうぞ～！",
                      "ありがとうございました～！",
                      ]
CatalogHelpText1 = "ページをめくって買いたい商品を見てね。"
CatalogSeriesLabel = "シリーズ%s"
CatalogGiftFor = "ギフトを送る相手:"
CatalogGiftTo = "ギフトを送る相手: %s"
CatalogGiftToggleOn = "ギフトをやめる"
CatalogGiftToggleOff = "ギフトを買う"
CatalogGiftToggleWait = "配達中 ..."
CatalogGiftToggleNoAck = "配達できません"
CatalogPurchaseItemAvailable = "お買いあげありがとう！ これはすぐに使うことができるわね。"
CatalogPurchaseGiftItemAvailable = "すばらしい! %sはすぐにこのギフトをつかえそうだね。"
CatalogPurchaseItemOnOrder = "お買いあげありがとうございます！ご注文の商品はキミのメールボックスに届きます！\n\nメールボックスを後でチェックしてみてね。"
CatalogPurchaseGiftItemOnOrder = "かしこまりました! %sへのギフトはうけとり人のメールボックスに配達されます。"
CatalogAnythingElse = "ほかの商品はよろしいですか？"
CatalogPurchaseClosetFull = "キミのクローゼットはいっぱいだね。 この品物を購入してもいいけど、もしかしたらこの品物が到着した時に、クローゼットのスペースにあきをもたせるため、なにかをすてる必要がでてくるよ。\n\nまだこの品物を購入したい？"
CatalogAcceptClosetFull = "キミのクローゼットはいっぱいだね。この品物をメールボックスからとってくる前に、それ用にスペースにあきをもたせるため、クローゼットにはいってなにかを削除しなきゃね。"
CatalogAcceptShirt = "あたらしいシャツを着るよ。今まで着ていたのはキミのクローゼットに入っているよ。"
CatalogAcceptShorts = "あたらしい短パンをはくよ。今まではいてたのはキミのクローゼットに入っているよ。"
CatalogAcceptSkirt = "あたらしいスカートをはくよ。今まではいてたのはキミのクローゼットに入っているよ。"
CatalogAcceptPole = "あたらしい釣ざおでもっと大きな魚を釣りに行こう！"
CatalogAcceptPoleUnneeded = "これよりも良い釣りざおを持っているよ！"
CatalogAcceptChat = "新しいスピードチャットのせりふを手に入れました!"
CatalogAcceptEmote = "新しい“きもち”を手に入れました!"
CatalogAcceptBeans = "ジェリービーンを受け取りました!"
CatalogAcceptRATBeans = "トゥーン・リクルートのごほうびが届きました!"
CatalogAcceptNametag = "新しいネーム・タグが届いたよ！"
CatalogAcceptGarden = "ガーデニングの道具が届いたよ!"
CatalogAcceptPet = "キミのペットの新しいトリックを受け取りました!"
CatalogPurchaseHouseFull = "おうちの中が荷物でいっぱいよ。この品物を購入してもいいけど、もしかしたらこの品物が到着した時に、おうちのスペースにあきをもたせるため、なにかをすてる必要がでてくるわよ。\n\nまだこの品物を購入したい？ "
CatalogAcceptHouseFull = "おうちの中が荷物でいっぱいよ。この品物をメールボックスからとってくる前に、それ用にスペースにあきをもたせるため、おうちの中のなにかを捨てなきゃね。"
CatalogAcceptInAttic = "新しい品物は今キミの屋根裏にあるよ。  中にはいって、\"模様替え\"ボタンをクリックすると、キミの家の中におくことができるよ。"
CatalogAcceptInAtticP = "新しい品物は今キミの屋根裏にあるよ。  中にはいって、\"模様替え\"ボタンをクリックすると、キミの家の中におくことができるよ。"
CatalogPurchaseMailboxFull = "キミのメールボックスはいっぱいだね！ 品物をいくつかとりだしてスペースにあきをもたせるまで、この品物を購入することはできないよ。"
CatalogPurchaseGiftMailboxFull = "%sのメールボックスはもういっぱいです!このアイテムは買えません。"
CatalogPurchaseOnOrderListFull = "いま注文している品物が多すぎるよ。すでに注文したものがいくつか届くまで、キミはこれ以上なにも注文することはできないよ。"
CatalogPurchaseGiftOnOrderListFull = "%sは、げんざい注文しすぎです。"
CatalogPurchaseGeneralError = "ゲーム内のエラーにより、この品物は購入できません：エラーコード %s"
CatalogPurchaseGiftGeneralError = "ゲームエラーのため、%(friend)sにこのアイテムをおくれませんでした: エラーコード %(error)s"
CatalogPurchaseGiftNotAGift = "このアイテムは%sにはもったいないのでおくれません。"
CatalogPurchaseGiftWillNotFit = "このアイテムは%sにはにあわないからおくれません。"
CatalogPurchaseGiftLimitReached = "このアイテムはもう持っているのでおくれません。"
CatalogPurchaseGiftNotEnoughMoney = "このアイテムはキミには高すぎて%sにはおくれないよ。"
CatalogAcceptGeneralError = "ゲーム内のエラーにより、この品物はメールボックスから削除することはできません：エラーコード %s"
CatalogAcceptRoomError = "置き場所がたりません。先になにかをすてなきゃネ!"
CatalogAcceptLimitError = "もう持ちきれないよ。先になにかをすてなきゃネ!"
CatalogAcceptFitError = "これはキミのサイズとちがうよ!他のトゥーンにあげよう。"
CatalogAcceptInvalidError = "このアイテムはなんだかイケてないね…。他のトゥーンにあげよう!"

MailboxOverflowButtonDicard = "すてる"
MailboxOverflowButtonLeave = "そのまま"

HDMoveFurnitureButton = "模様替え"
HDStopMoveFurnitureButton = "移動\n終了"
HDAtticPickerLabel = "屋根裏の中"
HDInRoomPickerLabel = "部屋の中"
HDInTrashPickerLabel = "ゴミ箱の中"
HDDeletePickerLabel = "削除する？"
HDInAtticLabel = "屋根裏"
HDInRoomLabel = "部屋"
HDInTrashLabel = "ゴミ箱"
HDToAtticLabel = "屋根裏に\n置く"
HDMoveLabel = "動かす"
HDRotateCWLabel = "右に回転"
HDRotateCCWLabel = "左に回転"
HDReturnVerify = "このアイテムを屋根裏に戻しますか？"
HDReturnFromTrashVerify = "このアイテムをゴミ箱から屋根裏に戻しますか？"
HDDeleteItem = "ＯＫを押すとこのアイテムをゴミ箱に送るよ\nキャンセルを押すと取っておくよ。"
HDNonDeletableItem = "この種類の品物は削除できないよ！"
HDNonDeletableBank = "キミの銀行は削除できないよ！"
HDNonDeletableCloset = "キミのクローゼットは削除できないよ！"
HDNonDeletablePhone = "キミの電話は削除できないよ！"
HDNonDeletableNotOwner = "キミは%s'sのものを削除できないよ！"
HDHouseFull = "キミのうちが荷物でいっぱいだよ。部屋か屋根裏のアイテムを何か捨ててね。"

HDHelpDict = {
    "DoneMoving" : "部屋の模様替えをやめる",
    "Attic" : "屋根裏にあるアイテムを\n表示します。\n部屋にまだ置いていない\nアイテムがあります。",
    "Room" : "部屋の中にあるアイテムを表示します。\nさがしものをするのに便利です。",
    "Trash" : "ゴミ箱が一杯になったり、\n捨ててから時間が経つと、\n古いアイテムから順番になくなります。",
    "ZoomIn" : "部屋を拡大して見る",
    "ZoomOut" : "部屋を縮小して見る",
    "SendToAttic" : "アイテムを屋根裏にとって置きます。",
    "RotateLeft" : "左に回転",
    "RotateRight" : "右に回転",
    "DeleteEnter" : "「すてるモード」に切り替えます。",
    "DeleteExit" : "「すてるモード」を終わります。",
    "FurnitureItemPanelDelete" : "%sをゴミ箱に入れる",
    "FurnitureItemPanelAttic" : "%sを部屋に置く",
    "FurnitureItemPanelRoom" : "%sを屋根裏に戻す。",
    "FurnitureItemPanelTrash" : "%sを屋根裏に戻す。",
    }


MessagePickerTitle = "フレーズがおおすぎるね。 \n\"%s\"\nを購入するには、なにか削除するものを選択しなきゃならないよ。"
MessagePickerCancel = "取り消す"
MessageConfirmDelete = "ほんとうに\"%s\"をキミのスピードチャットメニューから削除してもいいの？"

CatalogBuyText = "買う"
CatalogRentText = "かりる"
CatalogGiftText = "ギフト"
CatalogOnOrderText = "注文済"
CatalogPurchasedText = "持ってるよ"
CatalogGiftedText = "ギフトが\n届いたよ"
CatalogPurchasedGiftText = "持ってるよ"
CatalogMailboxFull = "もういっぱい"
CatalogNotAGift = "ギフトじゃないよ"
CatalogNoFit = "コレはにあわないよ"
CatalogMembersOnly = "ﾌﾙｱｸｾｽ\nﾒﾝﾊﾞｰ用"
CatalogSndOnText = "ｻｳﾝﾄﾞ"
CatalogSndOffText = "ﾐｭｰﾄ"
CatalogPurchasedMaxText = "これ以上、買えないよ！"
CatalogVerifyPurchase = "ジェリービーン%(price)s個で%(item)sを買いますか？"
CatalogVerifyRent = "%(item)sをジェリービーン%(price)s個でかりますか?"
CatalogVerifyGift = "%(friend)sへのギフトとして%(item)sをジェリービーン%(price)s個で買いますか?"
CatalogOnlyOnePurchase = "この商品は一度にひとつしか持てないんだ。この品物を購入したら、%(old)sはなくなっちゃうんだ。\n\nほんとうにジェリービーン%(price)sの%(item)sを買う？"
CatalogExitButtonText = "電話を切る"
CatalogCurrentButtonText = "今もっている品物へ"
CatalogPastButtonText = "前にもっていた品物へ"

TutorialHQOfficerName = "ＨＱスタッフのハリー"

# NPCToons.py
NPCToonNames = {
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : "チュートリアルのトム",
    999 : "トゥーン・テイラー",
    1000 : lToonHQ,
    20001 : Flippy,

    #
    # Toontown Central
    #

    # Toontown Central Playground

    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    2001 : Flippy,
    2002 : "ぎんこういんのボブ",
    2003 : "ピートきょうじゅ",
    2004 : "したてやタミー",
    2005 : "としょかんいんのラリー",
    2006 : "てんいんの\nクラーク",
    2011 : "てんいんの\nクララ",
    2007 : lHQOfficerM,
    2008 : lHQOfficerM,
    2009 : lHQOfficerF,
    2010 : lHQOfficerF,
    # NPCFisherman
    2012 : "りょうしのフレディー",
    2018 : "Duff..err..TIP Man",
    # NPCPetClerks
    2013 : "てんいんの\nポッピー",
    2014 : "てんいんの\nペッピー",
    2015 : "てんいんの\nパッピー",
    # NPCPartyPerson
    2016 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾊﾟﾝﾌﾟｷﾝ",
    2017 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾎﾟﾘｰ",

    # Silly Street
    2101 : "はいしゃのダニエル",
    2102 : "けいさつかんのシェリー",
    2103 : "ヘクション・キティー",
    2104 : lHQOfficerM,
    2105 : lHQOfficerM,
    2106 : lHQOfficerF,
    2107 : lHQOfficerF,
    2108 : "カナリア・コールマイン",
    2109 : "バブル・ブローハード",
    2110 : "ビル・ボード",
    2111 : "ダンシング・ディエゴ",
    2112 : "ドクター・トム",
    2113 : "スバラシイローロ",
    2114 : "ロズ・ベリー",
    2115 : "パティ・ペーパーカット",
    2116 : "ブル・マクドナル",
    2117 : "ママ・ズイーナ",
    2118 : "ピエロのドッケ",
    2119 : "ハニー・ハハ",
    2120 : "ビンキーきょうじゅ",
    2121 : "ホッホふじん",
    2122 : "おサルのハリー",
    2123 : "ナンデ・ボトルニスキー",
    2124 : "オヤジモ・コケール",
    2125 : "ナマケルスキイー",
    2126 : "ガハハきょうじゅ",
    2127 : "ウッディ・コゼーニ",
    2128 : "ピエロのピエール",
    2129 : "フランク・フルター",
    2130 : "ジョイ・バズ",
    2131 : "フェザー・コーチョチョ",
    2132 : "クレージー・ドン",
    2133 : "ドクター・ハッピー",
    2134 : "サイレント・シモーヌ",
    2135 : "メアリ",
    2136 : "サル・クスクス",
    2137 : "ハッピー・ヘイキュン",
    2138 : "マルドゥーン",
    2139 : "ポール・ポタポッター",
    2140 : "りょうしのビリー",

    # Loopy Lane
    2201 : "ゆうびんきょくちょうのユーゴ",
    2202 : "シャーリー・ジョーダン",
    2203 : lHQOfficerM,
    2204 : lHQOfficerM,
    2205 : lHQOfficerF,
    2206 : lHQOfficerF,
    2207 : "ノイ・ワイズメーカー",
    2208 : "ステイッキー・ルー",
    2209 : "チャーリー・ケラリン",
    2210 : "ヒッヒ",
    2211 : "サリー・ピッチャー",
    2212 : "ワーレン・ボトラー",
    2213 : "ルーシー・タイヤ",
    2214 : "シュミット・シミー",
    2215 : "シド・ビンカーン",
    2216 : "ノナ・クリア",
    2217 : "シャーキー・ジョーンズ",
    2218 : "ファニー・ペイジ",
    2219 : "シェフ・ビーダマー",
    2220 : "リック・ガンセキー",
    2221 : "ペルニラ・ペッタラ",
    2222 : "ショーティ・フューズ",
    2223 : "サーシャ・ビリリン",
    2224 : "スモーキー・ジョー",
    2225 : "りょうしのドゥルーピー",

    # Punchline Place
    2301 : "ドクター・ポッキン",
    2302 : "ギグルきょうじゅ",
    2303 : "ナースのナンシー",
    2304 : lHQOfficerM,
    2305 : lHQOfficerM,
    2306 : lHQOfficerF,
    2307 : lHQOfficerF,
    2308 : "ナンシー・ガス",
    2309 : "ブルース・ブー",
    2311 : "フランツ・クビマガラーン",
    2312 : "ドクター・センシティブ",
    2313 : "シーラ・シミアトン",
    2314 : "ネッド・ナゲット",
    2315 : "グニー・カメナイン",
    2316 : "シンディ・スプリンクル",
    2318 : "トニー・トニン",
    2319 : "ジッピー",
    2320 : "アル・カチーノ",
    2321 : "りょうしのパンチー",

    #
    # Donald's Dock
    #

    # Donald's Dock Playground
    1001 : "てんいんの\nウィリー",
    1002 : "てんいんの\nビリー",
    1003 : lHQOfficerM,
    1004 : lHQOfficerF,
    1005 : lHQOfficerM,
    1006 : lHQOfficerF,
    1007 : "スタン・ステテコ",
    # NPCFisherman
    1008 : "りょうしのファーボール",
    # NPCPetClerks
    1009 : "てんいんの\nバーキー",
    1010 : "てんいんの\nパー",
    1011 : "てんいんの\nブループ",
    # NPCPartyPerson
    1012 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾋﾟｸﾙｽ",
    1013 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾊﾟｯﾃｨｰ",

    # Barnacle Blvd.
    1101 : "ビリー・バッド",
    1102 : "キャプテン・カール",
    1103 : "レイ・シャケスーツ",
    1104 : "ドクター・メガリス",
    1105 : "フックていとく",
    1106 : "ノーリーふじん",
    1107 : "カル・プープデック",
    1108 : "ＨＱスタッフ",
    1109 : "ＨＱスタッフ",
    1110 : "ＨＱスタッフ",
    1111 : "ＨＱスタッフ",
    1112 : "ゲリー・ガボガボ",
    1113 : "エノラ・ゲラゲーラ",
    1114 : "チャーリー・チッチャ",
    1115 : "シーラ・イーカン",
    1116 : "ベッシー・シェル",
    1117 : "キャプテン・オット",
    1118 : "チョビー・ヒゲール",
    1121 : "リンダ・ツリーラバー",
    1122 : "スタン・ショッペー",
    1123 : "ビリット・クルール",
    1124 : "フリッピー・スピーディー",
    1125 : "アイリーン・ポロポロン",
    1126 : "りょうしのバーニー",

    # Seaweed Street
    1201 : "バーバラ・シェル",
    1202 : "アート",
    1203 : "エイハブ",
    1204 : "ロッキー・ムッキ",
    1205 : lHQOfficerM,
    1206 : lHQOfficerF,
    1207 : lHQOfficerM,
    1208 : lHQOfficerF,
    1209 : "ブイきょうじゅ",
    1210 : "ギャング・アルネ",
    1211 : "ウィン・バッグ",
    1212 : "トビー・トングスティンガー",
    1213 : "ダンテ・ドルフィン",
    1214 : "ケイト・ヒュー",
    1215 : "ダイナ・ダウン",
    1216 : "ロッド・リール",
    1217 : "シーシー・ワカメイン",
    1218 : "ティム・カンダイスキー",
    1219 : "ブライアン・ビーチヘッド",
    1220 : "カーラ・スイモン",
    1221 : "ブッキー・マッキー",
    1222 : "ヨー・オーイ",
    1223 : "シド・イーカン",
    1224 : "エミリー・ヌルール",
    1225 : "ボンゾ・ボソール",
    1226 : "モッチ・ホー",
    1227 : "ミス・サンゴ",
    1228 : "りょうしのリード",

    # Lighthouse Lane
    1301 : "アリス",
    1302 : "メルヴィル",
    1303 : "クラッガー",
    1304 : "スヴェトラーナ",
    1305 : lHQOfficerM,
    1306 : lHQOfficerF,
    1307 : lHQOfficerM,
    1308 : lHQOfficerF,
    1309 : "シーフォーム",
    1310 : "テッド・タックル",
    1311 : "サカ・サマール",
    1312 : "イーサン・コッツ",
    1313 : "アーリー・サンモン",
    1314 : "サビータ・ラルフ",
    1315 : "ドクター・ユラー",
    1316 : "ヒルマ・イルマー",
    1317 : "ポーラ・ストレス",
    1318 : "ダン・ドンダン",
    1319 : "オーライ・ドライ",
    1320 : "タイヘイ・ヨー",
    1321 : "ダイナ・ドッカー",
    1322 : "ブーブー・クッション",
    1323 : "スティンキー・ネッド",
    1324 : "パール・ダイバー",
    1325 : "ネッド・ビーグル",
    1326 : "フェリシア・チップス",
    1327 : "シンディ・チズル",
    1328 : "フレッド・フランダー",
    1329 : "シェリィ・シーウィード",
    1330 : "ポーター・ホール",
    1331 : "ルディ・ラダー",
    1332 : "りょうしのシェーン",

    #
    # The Brrrgh
    #

    # The Brrrgh Playground
    3001 : "ベティ・フリーズ",
    3002 : lHQOfficerM,
    3003 : lHQOfficerF,
    3004 : lHQOfficerM,
    3005 : lHQOfficerM,
    3006 : "てんいんの\nレニー",
    3007 : "てんいんの\nペニー",
    3008 : "ウォーレン・ボタン",
    # NPCFisherman
    3009 : "りょうしのフリジー",
    # NPCPetClerks
    3010 : "てんいんの\nスキップ",
    3011 : "てんいんの\nディップ",
    3012 : "てんいんの\nキップ",
    # NPCPartyPerson
    3013 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾋﾟｰﾄ",
    3014 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾍﾟﾆｰ",

    # Walrus Way
    3101 : "ウシおじさん",
    3102 : "フリーズおばさん",
    3103 : "フレッド",
    3104 : "ハッティ",
    3105 : "フロスティ・フレディ",
    3106 : "マモル・トリハダ",
    3107 : "パティ・パスポート",
    3108 : "トボガン・テッド",
    3109 : "ケイト",
    3110 : "チキン・ボーイ",
    3111 : "シンジン",
    3112 : "ミニおじさん",
    3113 : "ヒステリー・ハリー",
    3114 : "ヘンリー・ハザード",
    3115 : lHQOfficerM,
    3116 : lHQOfficerF,
    3117 : lHQOfficerM,
    3118 : lHQOfficerM,
    3119 : "クリーピー・カール",
    3120 : "マイク・テブクロン",
    3121 : "ジョー・ショック",
    3122 : "ルーシー・リュージュ",
    3123 : "フランク・ロイド・アイス",
    3124 : "ランス・アイスバーグ",
    3125 : "カーネル・クランチ",
    3126 : "コレスト・ローラー",
    3127 : "オチルーラ",
    3128 : "スティッキィ・ジョージ",
    3129 : "パンやのブリジット",
    3130 : "サンディ",
    3131 : "レイジー・ロレンゾ",
    3132 : "Mr.ハイ",
    3133 : "フリーズフレームはかせ",
    3134 : "ラウンジ・ラッサー",
    3135 : "メルティ・ニール",
    3136 : "ハッピー・スー",
    3137 : "Mr.フリーズ",
    3138 : "シェフ・バンブルスープ",
    3139 : "ツララばあちゃん",
    3140 : "りょうしのルシール",

    # Sleet Street
    3201 : "アークティックおばさん",
    3202 : "シェイキー",
    3203 : "ウォルト",
    3204 : "ドクター・アイシィ",
    3205 : "バンピー・ノギン",
    3206 : "セクシー・ヴィダリア",
    3207 : "ドクター・シンキクサーイ",
    3208 : "グランピー・フィル",
    3209 : "ギグル・マギー",
    3210 : "シミアン・サム",
    3211 : "ファニー・フリーズ",
    3212 : "フロスティ・フレッド",
    3213 : lHQOfficerM,
    3214 : lHQOfficerF,
    3215 : lHQOfficerM,
    3216 : lHQOfficerM,
    3217 : "あせかきピート",
    3218 : "ブルー・ルー",
    3219 : "トム・フロスト",
    3220 : "Mr.ヘックショイ",
    3221 : "ネリー・スノウ",
    3222 : "ミンディ・トーショウ",
    3223 : "チャッピー",
    3224 : "フリーダ・フロストバイト",
    3225 : "ブレイク・アイス",
    3226 : "サンタ・ポーズ",
    3227 : "ソーラー・レイ",
    3228 : "ウィン・チル",
    3229 : "ヘルニア・ベルト",
    3230 : "ハゲのハーゲン",
    3231 : "チョッピ",
    3232 : "りょうしのアルバート",

    # Polar Place
    3301 : "ペイズリー・パッチ",
    3302 : "ビヨン・ボード",
    3303 : "ミエールきょうじゅ",
    3304 : "エディー・イエティ",
    3305 : "マック・ラメイ",
    3306 : "ポーラ・ベアー",
    # NPC Fisherman
    3307 : "つりびとのフレドリカ", 
    3308 : "ドナルド・フランプ",
    3309 : "ブーツィー",
    3310 : "フレークきょうじゅ",
    3311 : "コニー・フェリス",
    3312 : "マーチ・ハリー",
    3313 : lHQOfficerM,
    3314 : lHQOfficerF,
    3315 : lHQOfficerM,
    3316 : lHQOfficerF,
    3317 : "キッシー・クリッシー",
    3318 : "ジョニー・カシミア",
    3319 : "サム・ステットソン",
    3320 : "フィジー・リジー",
    3321 : "ポール・ツルハシー",
    3322 : "フルー・ルー",
    3323 : "ダラス・ボレアリス",
    3324 : "じまん屋のストゥー",
    3325 : "グルービー・ガーランド",
    3326 : "ブリーチ",
    3327 : "チャック・ロースト",
    3328 : "シェイディー・サディー",
    3329 : "トレディング・エド",

    #
    # Minnie's Melody Land
    #

    # Minnie's Melody Land Playground
    4001 : "ミンディ・マンデー",
    4002 : lHQOfficerM,
    4003 : lHQOfficerF,
    4004 : lHQOfficerF,
    4005 : lHQOfficerF,
    4006 : "てんいんのド",
    4007 : "てんいんのレ",
    4008 : "したてやハーモニー",
    # NPCFisherman
    4009 : "りょうしのファニー",
    # NPCPetClerks
    4010 : "てんいんの\nクリス",
    4011 : "てんいんの\nネール",
    4012 : "てんいんの\nウェスティンガール",
    # NPCPartyPerson
    4013 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾌﾟﾚｽﾄﾝ",
    4014 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾍﾟﾈﾛﾍﾟ",

    # Alto Ave.
    4101 : "トム",
    4102 : "バイオレット",
    4103 : "ドクター・アイタタ",
    4104 : lHQOfficerM,
    4105 : lHQOfficerF,
    4106 : lHQOfficerF,
    4107 : lHQOfficerF,
    4108 : "クレフ",
    4109 : "カルロス",
    4110 : "メトラ・ノーム",
    4111 : "トム・ハム",
    4112 : "ファー",
    4113 : "マダム・マナーズ",
    4114 : "オフキー・エリック",
    4115 : "バーバラ・セヴィル",
    4116 : "ピッコロ",
    4117 : "マンディ・リン",
    4118 : "アテンダントのエイブ",
    4119 : "モー・ツァールト",
    4120 : "ヴィオラ・フカフーカ",
    4121 : "ジー・マイナー",
    4122 : "ミッコ・ミント",
    4123 : "カミナリ・テッド",
    4124 : "リフラフ",
    4125 : "メロディ・ウェーバー",
    4126 : "メル・カント",
    4127 : "ハッピー・タップ",
    4128 : "スクープ・ルチアーノ",
    4129 : "トゥッツィー・ツーステップ",
    4130 : "メタルマイク",
    4131 : "アブラハム・アーマー",
    4132 : "ジャジー・サリー",
    4133 : "スコット・ポプリン",
    4134 : "ディスコ・デイビッド",
    4135 : "ルーニー・ルンルン",
    4136 : "パティ・ポーズ",
    4137 : "トニー・イヤプラグ",
    4138 : "シェフ・トレモロ",
    4139 : "ハーモニー・スウェル",
    4140 : "ネッド・ブキヨン",
    4141 : "りょうしのジェッド",

    # Baritone Blvd.
    4201 : "ティナ",
    4202 : "バリー",
    4203 : "モックン",
    4204 : lHQOfficerM,
    4205 : lHQOfficerF,
    4206 : lHQOfficerF,
    4207 : lHQOfficerF,
    4208 : "ヘイディ",
    4209 : "シュマルツ・ワルツ",
    4211 : "カール・コンチェルト",
    4212 : "ハイドンたんてい",
    4213 : "フラン・フォリー",
    4214 : "ティナ・ビート",
    4215 : "ティム・タム",
    4216 : "ガミー・ホイッスル",
    4217 : "ハンサム・アントン",
    4218 : "ウィルマ・ウィンド",
    4219 : "シド・ソナタ",
    4220 : "ミミ・ショパン",
    4221 : "モー・マドリガル",
    4222 : "ソラ・シド",
    4223 : "ペニー・プロンプター",
    4224 : "ジャングル・ジム",
    4225 : "ホーリー・ヒス",
    4226 : "オクタヴィア・オクターブ",
    4227 : "フランチェスカ・ヒソヒッソ",
    4228 : "オーガスト・ウィンド",
    4229 : "ジューン・ルーン",
    4230 : "マシュー・エチュード",
    4231 : "ステフィ・チロル",
    4232 : "ヘドリー・キンコン",
    4233 : "チャーリー・カープ",
    4234 : "リード・ギター",
    4235 : "りょうしのラリー",

    # Tenor Terrace
    4301 : "ユキ",
    4302 : "アンナ",
    4303 : "レオ",
    4304 : lHQOfficerM,
    4305 : lHQOfficerF,
    4306 : lHQOfficerF,
    4307 : lHQOfficerF,
    4308 : "タバサ",
    4309 : "マーシャル",
    4310 : "メロディ・メロン",
    4311 : "シャンティ・バッハッハ",
    4312 : "マーク・パッサージュ",
    4313 : "ホワイティ・ウィッグ",
    4314 : "ダナ・ダンダー",
    4315 : "カレン・グルック",
    4316 : "シェーン・シューマン",
    4317 : "スタッビィ・パッヘルベル",
    4318 : "ボブ・マーリン",
    4319 : "リンキー・ディンク",
    4320 : "キャミー・コーダ",
    4321 : "ルーク・リュート",
    4322 : "ランディ・リズム",
    4323 : "ハンナ・プチ",
    4324 : "エリィ",
    4325 : "ぎんこういんのブラン",
    4326 : "フラン・フレット",
    4327 : "ワンバ・サンバ",
    4328 : "ワグナー",
    4329 : "テリィ・プロンプター",
    4330 : "クエンティン",
    4331 : "メロウ・コステロ",
    4332 : "ジギー",
    4333 : "ハリー",
    4334 : "フレディ・マーズ",
    4335 : "りょうしのウォルデン",

    #
    # Daisy Gardens
    #

    # Daisy Gardens Playground
    5001 : lHQOfficerM,
    5002 : lHQOfficerM,
    5003 : lHQOfficerF,
    5004 : lHQOfficerF,
    5005 : "てんいんの\nピーチ",
    5006 : "てんいんの\nハーブ",
    5007 : "ボニー・ブロッソム",
    # NPCFisherman
    5008 : "りょうしのフローラ",
    # NPCPetClerks
    5009 : "てんいんの\nボー・タニー",
    5010 : "てんいんの\nトム・ドー",
    5011 : "てんいんの\nダグ・ウッド",
    # NPCPartyPerson
    5012 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾋﾟｱｽ",
    5013 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾍﾟｷﾞｰ",

    # Elm Street
    5101 : "クータ",
    5102 : "スージー",
    5103 : "サッサ",
    5104 : "ランラン",
    5105 : "ジャック",
    5106 : "さんぱつやビョーン",
    5107 : "ゆうびんきょくいんのフェリペ",
    5108 : "おかみのジャネット",
    5109 : lHQOfficerM,
    5110 : lHQOfficerM,
    5111 : lHQOfficerF,
    5112 : lHQOfficerF,
    5113 : "ドングリン",
    5114 : "フニャリン",
    5115 : "ハニー・メロン",
    5116 : "ビッグ・グリーン",
    5117 : "ペタル",
    5118 : "ポップ・コーン",
    5119 : "バリー・メドレー",
    5120 : "ゴーファー",
    5121 : "ポーラ・ピース",
    5122 : "ジミー・モミジ",
    5123 : "ソー・セキ",
    5124 : "ビアンキ・コスモス",
    5125 : "サンジェイ・スプラッシュ",
    5126 : "マダム・コギク",
    5127 : "ポリーせんせい",
    5128 : "ケイト・ケイトウ",
    5129 : "りょうしのサリー",

    # Maple Street
    5201 : "ジェイク",
    5202 : "シンシア",
    5203 : "リサ",
    5204 : "バート",
    5205 : "ダンディ・タンポポ",
    5206 : "ブル・グリーン",
    5207 : "ソフィ・テッポー",
    5208 : "サマンサ・スペード",
    5209 : lHQOfficerM,
    5210 : lHQOfficerM,
    5211 : lHQOfficerF,
    5212 : lHQOfficerF,
    5213 : "ビッグ・マヨ",
    5214 : "ガッチィ・リー",
    5215 : "イモーナ・コロリン",
    5216 : "スティンキー・ジム",
    5217 : "フランク・フラワー",
    5218 : "ロッキーじいさん",
    5219 : "ビッグ・タジャーン",
    5220 : "シルキー・レイス",
    5221 : "ピンク・フラミンゴ",
    5222 : "ハッピー・タヌキン",
    5223 : "ウェット・ウィリー",
    5224 : "つるまきおじさん",
    5225 : "ナナ・グリーン",
    5226 : "ピート・モス",
    5227 : "ピーチ・ホップ",
    5228 : "ダグラス・シルバー",
    5229 : "りょうしのリリー",

    # Oak street
    5301 : lHQOfficerM,
    5302 : lHQOfficerM,
    5303 : lHQOfficerM,
    5304 : lHQOfficerM,
    5305 : "クリスタル",
    5306 : "エス・カルゴ",
    5307 : "マッシュ・ルーム",
    5308 : "ブンブン",
    5309 : "ロー・メイン",
    5310 : "パット・パター",
    5311 : "ミスター・ジャッジ",
    5312 : "ビーン・ビーン",
    5313 : "コーチのヨーガ",
    5314 : "ミセス・ウエスタン",
    5315 : "マッドおじさん",
    5316 : "ソファおじさん",
    5317 : "タンテイのメイ",
    5318 : "シーザー",
    5319 : "ローズ",
    5320 : "フリージア",
    5321 : "パインきょうじゅ",
    5322 : "りょうしのローズ",

    #
    # Goofy's Speedway
    #

    #default  area
    #kart clerk
    8001 : "グラハム・プーリー", # "Graham Pree"
    8002 : "イボナ・レース", # "Ivona Race"
    8003 : "アニータ・カッツ", # "Anita Winn"
    8004 : "フィル・ゴール", # "Phil Errup"

    #
    # Dreamland
    #

    # Dreamland Playground
    9001 : "スーザン・ムーニャ",
    9002 : "スリーピー・トム",
    9003 : "トビー・アクビー",
    9004 : lHQOfficerF,
    9005 : lHQOfficerF,
    9006 : lHQOfficerM,
    9007 : lHQOfficerM,
    9008 : "てんいんの\nジル",
    9009 : "てんいんの\nフィル",
    9010 : "よれよれジョニー",
    # NPCFisherman
    9011 : "りょうしのフロイト",
    # NPCPetClerks
    9012 : "てんいんの\nサラ・スヌーズ",
    9013 : "てんいんの\nキャット・ナップ",
    9014 : "てんいんの\nリンクル",
    # NPCPartyPerson
    9015 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾍﾟﾌﾞﾙｽ",
    9016 : "ﾊﾟｰﾃｨｰﾌﾟﾗﾝﾅｰの\nﾊﾟｰﾙ",

    # Lullaby Lane
    9101 : "ふとんやトニー",
    9102 : "ビッグ・ママ",
    9103 : "P.J.",
    9104 : "スウィーティ",
    9105 : "アクビはかせ",
    9106 : "マックス・スマイル",
    9107 : "スピカ",
    9108 : "ウィルバー・ウィンク",
    9109 : "ドリーミー・ダフネ",
    9110 : "マティ・タビー",
    9111 : "テティ・テーデン",
    9112 : "ララバイ・ルー",
    9113 : "ジャック・クロック",
    9114 : "スウィート・リップス",
    9115 : "ベイビーフェイス・マクドゥーガル",
    9116 : "スティーブ・スリープ",
    9117 : "アフタ・アワーズ",
    9118 : "スター・ナイト",
    9119 : "ロッコ",
    9120 : "サラ・グースカ",
    9121 : "セレナ・ハッピー",
    9122 : "ハレー・ボッタイ",
    9123 : "テディ・ブレア",
    9124 : "ニーナ・ナイトライト",
    9125 : "ドクター・ウッツラ",
    9126 : "アイ・パチーリ",
    9127 : "タビー・タッカー",
    9128 : "ハーディ・トゥール",
    9129 : "ベルサねえさん",
    9130 : "チャーリー・シーツ",
    9131 : "スーザン・シエスタ",
    9132 : lHQOfficerF,
    9133 : lHQOfficerF,
    9134 : lHQOfficerF,
    9135 : lHQOfficerF,
    9136 : "りょうしのテーラー",

    # Pajama Place
    9201 : "バーニー",
    9202 : "オービ",
    9203 : "ナット",
    9204 : "クレア",
    9205 : "ゼン・グレン",
    9206 : "スキニー・ジニー",
    9207 : "ジェーン・ドレイン",
    9208 : "ドロジー・デイブ",
    9209 : "ドクター・フロス",
    9210 : "マスター・マイク",
    9211 : "ドーン",
    9212 : "ムーン・ビーム",
    9213 : "ルースター・リック",
    9214 : "ドクター・ブリンキィ",
    9215 : "リップ",
    9216 : "キャット",
    9217 : "ロウフル・リンダ",
    9218 : "ワルツ・マチルダ",
    9219 : "カウンテス",
    9220 : "グランピィ・ゴードン",
    9221 : "ザリ",
    9222 : "カウボーイ・ジョージ",
    9223 : "マーク・ザ・ラーク",
    9224 : "サンディ・サンドマン",
    9225 : "フィジェティ・ブリジェッド",
    9226 : "ウィリアム・テラー",
    9227 : "ベッド・ヘッド・テッド",
    9228 : "ウィスパリング・ウィロー",
    9229 : "ローズ・ペタル",
    9230 : "テックス",
    9231 : "ハリー・ハンモック",
    9232 : "ハニー・ムーン",
    9233 : lHQOfficerM,
    9234 : lHQOfficerM,
    9235 : lHQOfficerM,
    9236 : lHQOfficerM,
    9237 : "りょうしのジャン",

    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# These building titles are output from the DNA files
# Run ppython $TOONTOWN/src/dna/DNAPrintTitles.py to generate this list
# DO NOT EDIT THE ENTRIES HERE -- EDIT THE ORIGINAL DNA FILE
zone2TitleDict = {
    # titles for: phase_4/dna/toontown_central_sz.dna
    2513 : ("トゥーンホール", ""),
    2514 : ("トゥーンタウン バンク", ""),
    2516 : ("トゥーンタウン スクールハウス", ""),
    2518 : ("トゥーンタウン ライブラリー", ""),
    2519 : (lGagShop, ""),
    2520 : (lToonHQ, ""),
    2521 : (lClothingShop, ""),
    2522 : (lPetShop, ""),
    # titles for: phase_5/dna/toontown_central_2100.dna
    2601 : ("ニコニコ はいしゃ", ""),
    2602 : ("", ""),
    2603 : ("カナリア さいくつ屋", ""),
    2604 : ("ブーブー ドライ クリーニング", ""),
    2605 : ("トゥーンタウン カンバン工房", ""),
    2606 : ("", ""),
    2607 : ("踊る大まめ屋", ""),
    2610 : ("ドクター トム フォーリー", ""),
    2611 : ("", ""),
    2616 : ("ヘンチク チクチク へんそう ショップ", ""),
    2617 : ("おまぬけ スタント", ""),
    2618 : ("笑われ ダンス スタジオ", ""),
    2621 : ("空とぶ 紙ひこうき屋", ""),
    2624 : ("ハッピー フーリガンの お店", ""),
    2625 : ("まさかの パイショップ", ""),
    2626 : ("ドッケの ジョーク リペア", ""),
    2629 : ("ワハハ プレイス", ""),
    2632 : ("ピエロ スクール", ""),
    2633 : ("ヒッヒの ティーショップ", ""),
    2638 : ("トゥーンタウン プレイハウス", ""),
    2639 : ("モンキー トリック ショップ", ""),
    2643 : ("ボトルニスキーの カンヅメ屋", ""),
    2644 : ("笑えない ジョーク ショップ", ""),
    2649 : ("スーパー ゲームショップ", ""),
    2652 : ("", ""),
    2653 : ("", ""),
    2654 : ("ワハハ きょうしつ", ""),
    2655 : ("ファニー マニ バンク", ""),
    2656 : ("中古ピエロ車 はんばい", ""),
    2657 : ("フランクの ジョークショップ", ""),
    2659 : ("有名な ジョイ バズの店", ""),
    2660 : ("くすぐり マシーンズ", ""),
    2661 : ("クレージー ダフィー", ""),
    2662 : ("ドクター ハッピー しんりょうじょ", ""),
    2663 : ("トゥーンタウン シネラマ", ""),
    2664 : ("マイム マイム", ""),
    2665 : ("メアリーのワールド トラベル", ""),
    2666 : ("ケラケラ ガス ステーション", ""),
    2667 : ("ハッピー タイムズ", ""),
    2669 : ("マルドゥーン バルーン", ""),
    2670 : ("スープ・フォーク", ""),
    2671 : ("", ""),
    # titles for: phase_5/dna/toontown_central_2200.dna
    2701 : ("", ""),
    2704 : ("ムービー マルチプレックス", ""),
    2705 : ("ワイズエイカーの ノイズメーカー", ""),
    2708 : ("ブルー グルー", ""),
    2711 : ("トゥーンタウン ゆうびんきょく", ""),
    2712 : ("ワハハハハ カフェ", ""),
    2713 : ("スマイルアワー カフェ", ""),
    2714 : ("クーキー シネプレックス", ""),
    2716 : ("スープ アンド クランクアップ", ""),
    2717 : ("ボトル ＆ カンショップ", ""),
    2720 : ("クランクアップ じどうしゃ しゅうり", ""),
    2725 : ("", ""),
    2727 : ("セルツァー ヘブンの びんショップ", ""),
    2728 : ("とうめい クリームショップ", ""),
    2729 : ("１４金魚 ショップ", ""),
    2730 : ("ワクワク ニュース", ""),
    2731 : ("", ""),
    2732 : ("グーフボール スパゲッティ", ""),
    2733 : ("ヘビー級 タコショップ", ""),
    2734 : ("キュウバン ＆ ソーサー", ""),
    2735 : ("ザ うちあげ ショップ", ""),
    2739 : ("チョットビリット しゅうりてん", ""),
    2740 : ("中古 バクチク屋", ""),
    2741 : ("", ""),
    2742 : ("", ""),
    2743 : ("ジャズ ドライ クリーニング", ""),
    2744 : ("", ""),
    2747 : ("シュミシミ インク", ""),
    2748 : ("シャーリーの ギャグショップ", ""),
    # titles for: phase_5/dna/toontown_central_2300.dna
    2801 : ("ブーブー クッション ソファ", ""),
    2802 : ("プー パチン ボールショップ", ""),
    2803 : ("カーニバル キッド", ""),
    2804 : ("ポキポキ カイロ プラクティック", ""),
    2805 : ("", ""),
    2809 : ("ザ パンチライン ジム", ""),
    2814 : ("トゥーンタウン シアター", ""),
    2818 : ("ザ フライング パイ", ""),
    2821 : ("", ""),
    2822 : ("ゴム・チキン サンドイッチ", ""),
    2823 : ("ユースクリーム アイスクリーム", ""),
    2824 : ("パンチライン ムービー パレス", ""),
    2829 : ("いかさま屋", ""),
    2830 : ("ハッピー ジッピー ショップ", ""),
    2831 : ("ギグルの ヒヒヒハウス", ""),
    2832 : ("", ""),
    2833 : ("", ""),
    2834 : ("ケラケラ きゅうきゅう びょういん", ""),
    2836 : ("", ""),
    2837 : ("ハディハッハ セミナー", ""),
    2839 : ("パスパスパスタ", ""),
    2841 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_sz.dna
    1506 : (lGagShop, ""),
    1507 : (lToonHQ, ""),
    1508 : (lClothingShop, ""),
    1510 : (lPetShop, ""),
    # titles for: phase_6/dna/donalds_dock_1100.dna
    1602 : ("中古 ライフセーバー ショップ", ""),
    1604 : ("ウェット スーツ ドライ クリーニング", ""),
    1606 : ("フックの 時計しゅうり店", ""),
    1608 : ("ゲラゲラ ボートグッズ", ""),
    1609 : ("マメつりえさ ショップ", ""),
    1612 : ("ダイム＆デック バンク", ""),
    1613 : ("イーカン ほうりつ じむしょ", ""),
    1614 : ("マキガイ ネイルサロン", ""),
    1615 : ("オットの ヨットショップ", ""),
    1616 : ("チョビヒゲ ビューティー サロン", ""),
    1617 : ("メガリスの めがねショップ", ""),
    1619 : ("木の おいしゃさん", ""),
    1620 : ("あさから ばんまで", ""),
    1621 : ("ポート デッキ ジム", ""),
    1622 : ("アメとムチ でんき店", ""),
    1624 : ("クイックリペア サービス", ""),
    1626 : ("シャケ チャント れいふく屋", ""),
    1627 : ("バーゲン ビン バーン", ""),
    1628 : ("センリツ！？ ピアノちょうきょうし", ""),
    1629 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1200.dna
    1701 : ("ブイと カモメの かんごスクール", ""),
    1703 : ("テツナベ クイジーン", ""),
    1705 : ("ヨットを 売るよっと ショップ", ""),
    1706 : ("クラクラ クラゲショップ", ""),
    1707 : ("ザブント ギフト ショップ", ""),
    1709 : ("ジェットカイト ショップ", ""),
    1710 : ("バーバラの バーゲン ショップ", ""),
    1711 : ("ディープ シー ダイナー", ""),
    1712 : ("ムキムキ ジム", ""),
    1713 : ("アートの スマート チャート マート", ""),
    1714 : ("くるくる ホテル", ""),
    1716 : ("マーメイド スイムウェア", ""),
    1717 : ("ヒロク カンガエヨウ 屋", ""),
    1718 : ("ガッチャン タクシー", ""),
    1719 : ("ダック バック ウォーター社", ""),
    1720 : ("リール ディール ショップ", ""),
    1721 : ("海のなんでも屋", ""),
    1723 : ("イーカンの イカリ屋", ""),
    1724 : ("にゅるにゅる ウナギ モーレイ", ""),
    1725 : ("プレハブ シークラブ センター", ""),
    1726 : ("ソーダ フロート ショップ", ""),
    1727 : ("オール オア ナッシング", ""),
    1728 : ("これでいい カニ屋", ""),
    1729 : ("", ""),
    # titles for: phase_6/dna/donalds_dock_1300.dna
    1802 : ("海の もくず屋", ""),
    1804 : ("ショーナン ビーチ ジム", ""),
    1805 : ("タックル 宅配ランチ", ""),
    1806 : ("ピグミー ハット ストア", ""),
    1807 : ("リュウ骨 コッツ", ""),
    1808 : ("スピード ノット", ""),
    1809 : ("サビータ バケツ店", ""),
    1810 : ("イカリ カンリじむしょ", ""),
    1811 : ("カヌー しようよ？", ""),
    1813 : ("サンバシ サンザン カウンセリング", ""),
    1814 : ("あっち 向いて ホイショップ", ""),
    1815 : ("どうした ドック？", ""),
    1818 : ("セブン シー カフェ", ""),
    1819 : ("ドッカーズ ダイナー", ""),
    1820 : ("イタズラ ギア ショップ", ""),
    1821 : ("ネプトゥーン カンヅメ工房", ""),
    1823 : ("ハマグリ ダイナー", ""),
    1824 : ("イヌカキ屋", ""),
    1825 : ("めでタイ さかな市場", ""),
    1826 : ("クラッガーの クレバー クロビス クローゼット", ""),
    1828 : ("アリスの 砂のお城", ""),
    1829 : ("かもめの ちょうこく屋", ""),
    1830 : ("おとしもの かいしゅう所", ""),
    1831 : ("海の メイドさん", ""),
    1832 : ("がっしり がんがん マート", ""),
    1833 : ("カッチリ テーラー", ""),
    1834 : ("ルディーの おもしろ ショップ", ""),
    1835 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_sz.dna
    4503 : (lGagShop, ""),
    4504 : (lToonHQ, ""),
    4506 : (lClothingShop, ""),
    4508 : (lPetShop, ""),
    # titles for: phase_6/dna/minnies_melody_land_4100.dna
    4603 : ("トムトムの ドラム", ""),
    4604 : ("カッチコッチ タイム", ""),
    4605 : ("バイオレットの バイオリン店", ""),
    4606 : ("カーサ デ カスタネット", ""),
    4607 : ("パラレル アパレル", ""),
    4609 : ("ドレミ ピアノ ギャラリー", ""),
    4610 : ("キチント教室", ""),
    4611 : ("ジャスト ちょうりつ師", ""),
    4612 : ("アイタタ 歯科", ""),
    4614 : ("ようきな ひげそり びようしつ", ""),
    4615 : ("ピッコロの ピザパーラー", ""),
    4617 : ("ハッピー マンドリン", ""),
    4618 : ("レストルーム", ""),
    4619 : ("スコア！ スポーツ グッズ店", ""),
    4622 : ("すやすや マクラ", ""),
    4623 : ("フラット シャープ", ""),
    4625 : ("ミッコの はみがきこ", ""),
    4626 : ("スラスラ本舗", ""),
    4628 : ("うっかり 保険", ""),
    4629 : ("リフラフ 紙コップ屋", ""),
    4630 : ("フォルテ ミュージック", ""),
    4631 : ("ポエム ブックショップ", ""),
    4632 : ("チクタク クロック ショップ", ""),
    4635 : ("テノール しんぶんしゃ", ""),
    4637 : ("ピッタンコ あなたサイズ テーラー", ""),
    4638 : ("ハードロック ショップ", ""),
    4639 : ("ニュー アンティーク屋", ""),
    4641 : ("ブルース ニュース", ""),
    4642 : ("ラグタイム クリーニング ショップ", ""),
    4645 : ("クラブ８８", ""),
    4646 : ("", ""),
    4648 : ("ルンタッタ ひっこし屋", ""),
    4649 : ("", ""),
    4652 : ("フルストップ ショップ", ""),
    4653 : ("", ""),
    4654 : ("われがね 屋根がわら店", ""),
    4655 : ("トレモロ クッキング スクール", ""),
    4656 : ("", ""),
    4657 : ("いっぱつ さんぱつ屋", ""),
    4658 : ("ガタゴト ピアノ店", ""),
    4659 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4200.dna
    4701 : ("シュワルツ ワルツの ダンススクール", ""),
    4702 : ("モックンの 木材店", ""),
    4703 : ("コンチェルト トラベルショップ", ""),
    4704 : ("コンチェルティーナ コンサート 紹介サービス", ""),
    4705 : ("おいどん ハイドン たんてい社", ""),
    4707 : ("ドップラー効果 スタジオ", ""),
    4709 : ("アップビート 登山グッズ", ""),
    4710 : ("スローテンポ ドライビング スクール", ""),
    4712 : ("パンクパンク タイヤしゅうり店", ""),
    4713 : ("シャープな メンズ ファッション", ""),
    4716 : ("吹いてみるか ハーモニカ店", ""),
    4717 : ("ソナタ そんがい保険", ""),
    4718 : ("ショパン 食パン 工房", ""),
    4719 : ("マドリガル トレーラー ディーラー", ""),
    4720 : ("ドレミファ がっき店", ""),
    4722 : ("ぜんそう曲 代行屋", ""),
    4723 : ("プレイグラウンド ようひん店", ""),
    4724 : ("よいこの 学生服", ""),
    4725 : ("バリトン ヘアサロン", ""),
    4727 : ("オクタヴィアの ミュージック ショップ", ""),
    4728 : ("ソロで歌って", ""),
    4729 : ("オカリナ 書店", ""),
    4730 : ("ブレーメンの おんがく屋", ""),
    4731 : ("トゥーン チューンズ", ""),
    4732 : ("劇団エチュード シェイクス ピアリアン シアター", ""),
    4733 : ("", ""),
    4734 : ("", ""),
    4735 : ("チロリアン アコーディオン", ""),
    4736 : ("キンコンカン ウェディング", ""),
    4737 : ("ハープ タープ", ""),
    4738 : ("ロックンローリー ギフトショップ", ""),
    4739 : ("", ""),
    # titles for: phase_6/dna/minnies_melody_land_4300.dna
    4801 : ("マーシャルの パンケーキ ショップ", ""),
    4803 : ("メロディ メイドさん サービス", ""),
    4804 : ("バッハッハ バーテンダー スクール", ""),
    4807 : ("マッサージの パッサージュ", ""),
    4809 : ("バロック ほんやく サービス", ""),
    4812 : ("", ""),
    4817 : ("トランペット ペットショップ", ""),
    4819 : ("ユキの ウクレレ ショップ", ""),
    4820 : ("", ""),
    4821 : ("アンナの 旅行代理店", ""),
    4827 : ("グルック クロック", ""),
    4828 : ("シューマンの シューズ ショップ", ""),
    4829 : ("パッヘルベル キャノン ボール店", ""),
    4835 : ("タバサの マウスピース店", ""),
    4836 : ("レゲエ レガリア", ""),
    4838 : ("シャコンヌ 音楽学校", ""),
    4840 : ("コーダコーラ ショップ", ""),
    4841 : ("ライアー うそ発見 サービス", ""),
    4842 : ("シンコペー ション コーポレー ション", ""),
    4843 : ("", ""),
    4844 : ("バイクショップ ピアニッシモ", ""),
    4845 : ("エリーの エレガント エレジー", ""),
    4848 : ("シルバー ハーブ 銀行", ""),
    4849 : ("", ""),
    4850 : ("Ｇマイナー セブン質屋", ""),
    4852 : ("サンバ セーター ショップ", ""),
    4853 : ("レオの フェンダー ショップ", ""),
    4854 : ("ワーグナーの ビデオショップ", ""),
    4855 : ("エレジー ＴＶ ネットワーク", ""),
    4856 : ("", ""),
    4862 : ("クエンティンの クアドリーユ", ""),
    4867 : ("コステロの チェロ工房", ""),
    4868 : ("", ""),
    4870 : ("ジギーズ ジグショップ", ""),
    4871 : ("ハーモニー ハンバーガー", ""),
    4872 : ("フレディーの ギターショップ", ""),
    4873 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_sz.dna
    5501 : (lGagShop, ""),
    5502 : (lToonHQ, ""),
    5503 : (lClothingShop, ""),
    5505 : (lPetShop, ""),
    # titles for: phase_8/dna/daisys_garden_5100.dna
    5601 : ("どんぐりまなこ メガネ店", ""),
    5602 : ("クタクタ ネクタイ店", ""),
    5603 : ("もりもり サラダバー", ""),
    5604 : ("メロメロン ブライダル", ""),
    5605 : ("みどりの おやゆび 家具店", ""),
    5606 : ("フラワー ペダル", ""),
    5607 : ("チューリップ ポストオフィス", ""),
    5608 : ("ポップコーン ショップ", ""),
    5609 : ("落ち葉 アンティーク店", ""),
    5610 : ("黒目スージーのボクシングジム事務所", ""),
    5611 : ("ゴーファーギャグ", ""),
    5613 : ("高枝バサミ さんぱつ屋", ""),
    5615 : ("アラエッサッサ 鳥のエサ店", ""),
    5616 : ("つゆくさ ホテル", ""),
    5617 : ("ランランの ちょうちょう ショップ", ""),
    5618 : ("グリーンピース 専門店", ""),
    5619 : ("ジャックの豆の木店", ""),
    5620 : ("もみじ ホテル", ""),
    5621 : ("わが輩は エコショップ", ""),
    5622 : ("くるくる 自転車店", ""),
    5623 : ("ことりの おふろやさん", ""),
    5624 : ("マダムに おまかせ", ""),
    5625 : ("ハチノコ ほいくえん", ""),
    5626 : ("ケイトウ けいと店", ""),
    5627 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5200.dna
    5701 : ("グリーン サラダバー", ""),
    5702 : ("ジェイクの くまで店", ""),
    5703 : ("クスノキ カメラショップ", ""),
    5704 : ("リサ・レモンの中古車店", ""),
    5705 : ("だいこく 家具店", ""),
    5706 : ("ジュエリー コロリン", ""),
    5707 : ("ミュージカル フルーツ レストラン", ""),
    5708 : ("フラフラ フラワーショップ", ""),
    5709 : ("おじいさんの 芝刈り サービス", ""),
    5710 : ("ジャングル ジム", ""),
    5711 : ("シルキー ストッキング ショップ", ""),
    5712 : ("ストーン アニマル", ""),
    5713 : ("ブンブック ちゃがま ブックショップ", ""),
    5714 : ("スプリング レイン ペットボトル", ""),
    5715 : ("はなしのタネ新聞", ""),
    5716 : ("ななくさ 質屋", ""),
    5717 : ("テッポウギクの 水でっぽう", ""),
    5718 : ("森の ペット屋さん", ""),
    5719 : ("根ほり葉ほり タンテイ事務所", ""),
    5720 : ("メンズ ファッション あおむし", ""),
    5721 : ("みちくさ食堂", ""),
    5725 : ("ホップス カフェ", ""),
    5726 : ("バートの ダート", ""),
    5727 : ("シルバーグラス バンク", ""),
    5728 : ("", ""),
    # titles for: phase_8/dna/daisys_garden_5300.dna
    5802 : (lToonHQ, ""),
    5804 : ("どびん 花びん ちょびんショップ", ""),
    5805 : ("でんでん はいたつ屋", ""),
    5809 : ("きのこ のこのこ スクール", ""),
    5810 : ("はちみつドロップ ショップ", ""),
    5811 : ("レタス ホテル", ""),
    5815 : ("グリーン パットゴルフ", ""),
    5817 : ("白黒 はっきり屋", ""),
    5819 : ("グリーン ビーン ジーンズ", ""),
    5821 : ("スカッシュ＆ ストレッチ ジム", ""),
    5826 : ("カントリー ファーム ショップ", ""),
    5827 : ("どろんこ ディスカウント", ""),
    5828 : ("カウチ・ポテト インテリア", ""),
    5830 : ("とりこぼし タンテイ ジムショ", ""),
    5833 : ("ザ サラダバー", ""),
    5835 : ("フラワーベッド ブレックファスト", ""),
    5836 : ("エイプリル シャワーショップ", ""),
    5837 : ("ぼんさい スクール", ""),
    # titles for: phase_8/dna/donalds_dreamland_sz.dna
    9501 : ("ララバイ ライブラリー", ""),
    9503 : ("バー こもりうた", ""),
    9504 : (lGagShop, ""),
    9505 : (lToonHQ, ""),
    9506 : (lClothingShop, ""),
    9508 : (lPetShop, ""),
    # titles for: phase_8/dna/donalds_dreamland_9100.dna
    9601 : ("ほしぞらホテル", ""),
    9602 : ("ウィンク まばたき ショップ", ""),
    9604 : ("ふかふかふとん店", ""),
    9605 : ("ララバイ ストリート 323番地", ""),
    9607 : ("ビッグママの ジャマイカ パジャマ", ""),
    9608 : ("ペットショップ またたび", ""),
    9609 : ("正しいスイミン教室", ""),
    9613 : ("クロック クリーナー", ""),
    9616 : ("テーデン家電店", ""),
    9617 : ("ララバイ ストリート 212番地", ""),
    9619 : ("にこにこ リラクゼーション センター", ""),
    9620 : ("いねむり タクシー サービス", ""),
    9622 : ("チクタク トケイ店", ""),
    9625 : ("スイートドリーム ビューティー パーラー", ""),
    9626 : ("ララバイ ストリート 818番地", ""),
    9627 : ("スリーピー ハウス", ""),
    9628 : ("ダレンダー カレンダー ショップ", ""),
    9629 : ("ララバイ ストリート 310番地", ""),
    9630 : ("うたたね サイクツ屋", ""),
    9631 : ("グースカ トケイ しゅうり店", ""),
    9633 : ("ドリームランド 上映室", ""),
    9634 : ("ジュクスイ マットレス", ""),
    9636 : ("フミン症保険", ""),
    9639 : ("トウミンの ススメ", ""),
    9640 : ("ララバイ ストリート 805番地", ""),
    9642 : ("ぐっすり ベッドギャラリー", ""),
    9643 : ("うつらうつら メガネ店", ""),
    9644 : ("まくら投げ ショップ", ""),
    9645 : ("ぬくぬく ホテル", ""),
    9647 : ("ベッドポスト 工具店", ""),
    9649 : ("いびき ねびき ベッド", ""),
    9650 : ("ララバイ ストリート 714番地", ""),
    9651 : ("うたたね いびき 研究所", ""),
    9652 : ("", ""),
    # titles for: phase_8/dna/donalds_dreamland_9200.dna
    9703 : ("ユメの旅行代理店", ""),
    9704 : ("夜のふくろう ペットショップ", ""),
    9705 : ("いねむり 自動車修理工場", ""),
    9706 : ("歯の妖精 デンタルクリニック", ""),
    9707 : ("夜明けのあくび ガーデンセンター", ""),
    9708 : ("バラのベットの フラワーショップ", ""),
    9709 : ("夢見がちパイプ屋", ""),
    9710 : ("レムすいみん眼科", ""),
    9711 : ("モーニングコール カンパニー", ""),
    9712 : ("ヒツジ数えます屋", ""),
    9713 : ("うとうと弁護士事務所", ""),
    9714 : ("ドリームボート マリーンショップ", ""),
    9715 : ("第一ねんね タオル銀行", ""),
    9716 : ("どっちらけパーティー 企画会社", ""),
    9717 : ("いねむりパン屋のドーナツ", ""),
    9718 : ("ねむりの精の サンドイッチ屋", ""),
    9719 : ("アルマジロまくら店", ""),
    9720 : ("ねごと発声教室", ""),
    9721 : ("ぬくぬく じゅうたん販売店", ""),
    9722 : ("寝ぼけタレント事務所", ""),
    9725 : ("猫の高級 パジャマ屋", ""),
    9727 : ("いびき帽子屋", ""),
    9736 : ("ドリームエージェンシー", ""),
    9737 : ("ワルツ・マチルダ ダンススクール", ""),
    9738 : ("いびきの館", ""),
    9740 : ("おやすみ フェンシングスクール", ""),
    9741 : ("ベッドの虫 くじょサービス", ""),
    9744 : ("三年寝太郎の しわのばしクリーム", ""),
    9752 : ("夜通し ガス会社", ""),
    9753 : ("月明かり アイスクリーム", ""),
    9754 : ("眠らない乗馬場", ""),
    9755 : ("ベッドかざりと ほうきの映画館", ""),
    9756 : ("", ""),
    9759 : ("眠れる美女パーラー", ""),
    # titles for: phase_8/dna/the_burrrgh_sz.dna
    3507 : (lGagShop, ""),
    3508 : (lToonHQ, ""),
    3509 : (lClothingShop, ""),
    3511 : (lPetShop, ""),
    # titles for: phase_8/dna/the_burrrgh_3100.dna
    3601 : ("ノーザン ライト エレクトリックス", ""),
    3602 : ("北のご婦人 ぼうし屋", ""),
    3605 : ("", ""),
    3607 : ("ブリザード ウィザード", ""),
    3608 : ("ルージュ リュージュ", ""),
    3610 : ("ぬくぬく ムクルク ショップ", ""),
    3611 : ("うしおじさんの 雪かき屋", ""),
    3612 : ("イグルー デザイン ファクトリー", ""),
    3613 : ("アイシクル バイシクル", ""),
    3614 : ("シャキシャキ スノウ フレーク シリアル社", ""),
    3615 : ("さくさく しゃけ焼き亭", ""),
    3617 : ("冷気球 カンパニー", ""),
    3618 : ("イカリも トウケツ！ コンサルティング", ""),
    3620 : ("スキー クリニック", ""),
    3621 : ("どろどろ アイスクリーム バー", ""),
    3622 : ("", ""),
    3623 : ("カチコチ パン屋", ""),
    3624 : ("コールド サンドウィッチ ショップ", ""),
    3625 : ("フリーズ おばさんの ラジエータ屋", ""),
    3627 : ("セントバーナード ケンネル", ""),
    3629 : ("ピースープ カフェ", ""),
    3630 : ("オーロラ トラベル エージェンシー", ""),
    3634 : ("安楽リフト", ""),
    3635 : ("中古のマキ屋", ""),
    3636 : ("ゾクゾク トリハダ屋", ""),
    3637 : ("ケイトの スケート ショップ", ""),
    3638 : ("トボガン ソリ ショップ", ""),
    3641 : ("フレッドの スレッド ベッド", ""),
    3642 : ("タイフウの メガネ ショップ", ""),
    3643 : ("スノウボール ホール", ""),
    3644 : ("とろける アイスキューブ", ""),
    3647 : ("ザ ペンギン タキシード ショップ", ""),
    3648 : ("インスタント アイスキューブ", ""),
    3649 : ("ブルブル バーガー ショップ", ""),
    3650 : ("アンチフリーズ アンティーク", ""),
    3651 : ("フローズン ホットドッグ", ""),
    3653 : ("アイスハウス ジュエリー", ""),
    3654 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3200.dna
    3702 : ("ウィンター ストレージ", ""),
    3703 : ("", ""),
    3705 : ("ツララ スティック ショップ", ""),
    3706 : ("シェイク シェイク！ ショップ", ""),
    3707 : ("あったか ホーム 家具店", ""),
    3708 : ("プルート プレイス", ""),
    3710 : ("ヒョウテンカ ダイナー", ""),
    3711 : ("", ""),
    3712 : ("トウケツも おまかせ 配管工", ""),
    3713 : ("ガタガタ 歯科", ""),
    3715 : ("アークティック おばさんの スープショップ", ""),
    3716 : ("ゆきどけ パウダー ショップ", ""),
    3717 : ("ジュノー セミナー", ""),
    3718 : ("インナーチューブ ギャラリー", ""),
    3719 : ("ナイス アイスキューブ", ""),
    3721 : ("トボガン バーゲン ショップ", ""),
    3722 : ("ユキうさぎ スキーショップ", ""),
    3723 : ("スノウ グローブ屋", ""),
    3724 : ("ガチガチ クロニクル", ""),
    3725 : ("それのれ ソリ屋", ""),
    3726 : ("ソーラー パワー ブランケット", ""),
    3728 : ("雪かき 工房", ""),
    3729 : ("", ""),
    3730 : ("雪だるま 質屋", ""),
    3731 : ("ポータブル だんろ工房", ""),
    3732 : ("ザ フローズン ノーズ", ""),
    3734 : ("冷たいシセン 眼科", ""),
    3735 : ("アイス＆キャップ", ""),
    3736 : ("キュートな アイスキューブ ショップ", ""),
    3737 : ("ダウンヒル ダイナー", ""),
    3738 : ("イマノウチ だんぼう屋", ""),
    3739 : ("", ""),
    # titles for: phase_8/dna/the_burrrgh_3300.dna
    3801 : ("トゥーンHQ", ""),
    3806 : ("てぐすねカフェテリア", ""),
    3807 : ("中古かげ絵店", ""),
    3808 : ("セーター・ロッジ", ""),
    3809 : ("みたみた！話し相手サービス", ""),
    3810 : ("ふわふわキルト", ""),
    3811 : ("雪の天使商会", ""),
    3812 : ("ネコ用てぶくろ屋", ""),
    3813 : ("なぜかはきたい雪ぐつ屋", ""),
    3814 : ("リジーのソーダ・ショップ", ""),
    3815 : ("シャレのかつら店", ""),
    3816 : ("キッスィーの雪かざり", ""),
    3817 : ("雪のワンダーランド旅行社", ""),
    3818 : ("物置きかいたい屋", ""),
    3819 : ("エントツそうじ屋さん", ""),
    3820 : ("『白雪』ひょうはく店", ""),
    3821 : ("とうみんツアー", ""),
    3823 : ("大急ぎファンデーション", ""),
    3824 : ("直火やきぐり屋", ""),
    3825 : ("イケてるぼうし店", ""),
    3826 : ("げきおもクツ店", ""),
    3827 : ("歌うはなわ商会", ""),
    3828 : ("雪おとこカフェ", ""),
    3829 : ("コニーのマツボックリ店", ""),
    3830 : ("じきに見えるくもりどめ店", ""),
    }

# DistributedCloset.py
ClosetTimeoutMessage = "ごめん、\n時間切れだ！"
ClosetNotOwnerMessage = "キミのクローゼットじゃないけど、 ようふくを試着できるよ。"
ClosetPopupOK = lOK
ClosetPopupCancel = "取り消し"
ClosetDiscardButton = "すてる"
ClosetAreYouSureMessage = "何枚かようふくをすてるよ。ほんとにすてていい？"
ClosetYes = lYes
ClosetNo = lNo
ClosetVerifyDelete = "ほんとにほんとに%sをすてていいの？"
ClosetShirt = "このシャツ"
ClosetShorts = "この短パン"
ClosetSkirt = "このスカート"
ClosetDeleteShirt = "シャツを\nすてる"
ClosetDeleteShorts = "ズボンを\nすてる"
ClosetDeleteSkirt = "ボトムを\nすてる"

# EstateLoader.py
EstateOwnerLeftMessage = "ごめん、おうちの持ち主がいなくなっちゃった。 キミは%s秒以内にプレイグランドにワープするよ。"
EstatePopupOK = lOK
EstateTeleportFailed = "家へ帰れない？\nもう一度やってみて！"
EstateTeleportFailedNotFriends = "%sはキミの知らないトゥーンの家にいるよ。"

# DistributedTarget.py
EstateTargetGameStart = "トゥーンアップ ターゲットゲーム、スタート！"
EstateTargetGameInst = "赤いまとにたくさん当てるとトゥーンアップできるよ。"
EstateTargetGameEnd = "トゥーンアップ ターゲットゲーム、おしまい..."

# DistributedCannon.py
EstateCannonGameEnd = "キャノンゲームのレンタルは終わったよ。"

# DistributedHouse.py
AvatarsHouse = "%s\nおうち"

# BankGui.py
BankGuiCancel = lCancel
BankGuiOk = lOK

# DistributedBank.py
DistributedBankNoOwner = "ごめん、これはキミの貯ビーン箱じゃないんだ。"
DistributedBankNotOwner = "ごめん、これはキミの貯ビーン箱じゃないんだ。"

# FishSellGui.py
FishGuiCancel = lCancel
FishGuiOk = lOK
FishTankValue = "やぁ、%(name)s！\n%(num)s匹の魚がいるね。ジェリービーン%(value)s個分だけど。\nもしよかったら魚を全部、買い取ろうか？"

#FlowerSellGui.py
FlowerGuiCancel = lCancel
FlowerGuiOk = "ぜんぶうる"
FlowerBasketValue = "やぁ%(name)s、キミのバスケットにはジェリービーン%(value)sコ分の花が%(num)s本入ってるね。全部売っててくれるかい？"


def GetPossesive(name):
    if name[-1:] == 's':
        possesive = name + ""
    else:
        possesive = name + "の"
    return possesive

# PetTraits
# VERY_BAD, BAD, GOOD, VERY_GOOD
PetTrait2descriptions = {
    'hungerThreshold': ('いつもくうふく', 'しばしばくうふく',
                        'ときどきくうふく', 'まれにくうふく',),
    'boredomThreshold': ('いつもたいくつ', 'しばしばたいくつ',
                         'ときどきたいくつ', 'まれにたいくつ',),
    'angerThreshold': ('いつもふきげん', 'しばしばふきげん',
                       'ときどきふきげん', 'ときどきふきげん'),
    'forgetfulness': ('いつもわすれる', 'しばしばわすれる',
                      'ときどきわすれる', 'まれにわすれる',),
    'excitementThreshold': ('とてもうきうき', 'まあまあれいせい',
                            'ちょっとうきうき', 'とってもうきうき',),
    'sadnessThreshold': ('とってもかなしい', 'しばしばかなしい',
                         'ときどきかなしい', 'まれにかなしい',),
    'restlessnessThreshold': ('いつもおちつかない', 'しばしばおちつかない',
                         'ときどきおちつかない', 'おちついている',),
    'playfulnessThreshold': ('ほとんどはしゃがない', 'ときどきはしゃぐ',
                         'しばしばはしゃぐ', 'いつもはしゃぐ',),
    'lonelinessThreshold': ('いつもさびしい', 'しばしばさびしい',
                         'ときどきさびしい', 'さびしくない',),
    'fatigueThreshold': ('いつもつかれた', 'しばしばつかれた',
                         'ときどきつかれた', 'まれにつかれた',),
    'confusionThreshold': ('いつもこんらん', 'しばしばこんらん',
                         'ときどきこんらん', 'まれにこんらん',),
    'surpriseThreshold': ('いつもびっくり', 'しばしばびっくり',
                         'ときどきびっくり', 'まれにびっくり',),
    'affectionThreshold': ('まれにラブラブ', 'ときどきラブラブ',
                         'しばしばラブラブ', 'いつもラブラブ',),
    }


# end translate

# DistributedFireworkShow.py
FireworksInstructions = lToonHQ+"：\"PageUp\"キーを押すと、よく見えるよ。"

FireworksValentinesBeginning = ""
FireworksValentinesEnding = ""
FireworksJuly4Beginning = "トゥーンHQ：夏の花火大会へようこそ！楽しんでいってね！"
FireworksJuly4Ending = "トゥーンHQ：花火楽しんでくれたかな？すてきな夏をすごしてね！"
FireworksJuly14Beginning = lToonHQ+""
FireworksJuly14Ending = lToonHQ+""
FireworksOctober31Beginning = lToonHQ+""
FireworksOctober31Ending = lToonHQ+""
FireworksNewYearsEveBeginning = lToonHQ+"：冬の花火大会へようこそ！"
FireworksNewYearsEveEnding = lToonHQ+"：明けましておめでとう！2010年もいっしょにサイコーの一年にしようね！"
FireworksBeginning = "トゥーンＨＱ：夏の花火へようこそ！楽しんでいってね！"
FireworksEnding = "トゥーンＨＱ：花火楽しんでくれたかな？すてきな夏をすごしてね！"

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
TipTitle = "トゥーンアドバイス："
TipDict = {
    TIP_NONE : (
    "",
    ),

    TIP_GENERAL : (
    "\"End\"キーを押している間、 トゥーンタスクの進み具合をチェックできるよ。",
    "ギャグページは、\"Home\"キーを押したままにするとすぐチェックできるよ。",
    "\"PageUp\"キーを押すと、\n見上げることができ、\n\"PageDown\"キーを押すと、見おろすことができるよ。",
    "ジャンプするには、 \"Control\"キーを押してね。",
    "\"Ｆ８\"キーを押すと、 トゥーンガイドを開け閉めできるよ。",
    "トゥーンタウンの外で誰か知ってる人と「ひみつのともだち」の暗号を交換すると、自由にチャットができるようになるよ。",
    "\"Ｆ９\"キーを押すと、画面の写真がとれるよ。写真はトゥーンタウンのフォルダに保存されるよ。",
    # This one makes me nervous without mentioning Parent Passwords - but that would be too long
    # "You can exchange Secret Friend Codes with somebody you know outside Toontown to enable open chat with them in Toontown.",
    "トゥーンガイドのオプションページで、画面の解像度を変えたり、音の調整などの設定ができるよ。",
    "キミの友だちの家のクローゼットにあるようふくをためすことができるよ。",
    "トゥーンガイドの地図にある「家に戻る」ボタンを押すと、おうちに帰れるよ。",
    "トゥーンタスクをクリアすると、キミのゲラゲラメーターが自動的に補充されるよ。",
    "ようふく券がなくても、ようふくを試着できるよ。",
    "トゥーンタスクのごほうびとして、もっとたくさんのギャグやジェリービーンをもてるようになることがあるよ。",
    "ともだちリストには、ともだちを５０人まで書き込むことができるよ。",
    "いくつかトゥーンタスクは、キミがトゥーンタウンのプレイグラウンドへワープできるようにするんだ。トゥーンガイドにある地図のページを使えばテレポートできるよ。",
    "プレイグラウンドでは、その地域のまわりにあらわれるアイスクリームといったアイテムをとると、はやくパワーが戻るよ。",
    "バトルの後に体力を早く回復させたいときには、おうちに戻ってアイスクリームを集めよう！",
    "\"TAB\"キーを押すと、キミのトゥーンの視点をいろいろ変えることができるよ。",
    "ときどき同じごほうびをくれるちがうトゥーンタスクをみつけることがあるよ。いろいろ行ってみて！",
    "おなじようなトゥーンタスクのともだちをみつければ、一緒に楽しみながらゲームも上達できるよ！",
    "トゥーンタウンでしたことはセーブしなくても大丈夫だよ。トゥーンタウンのサーバーがすべての状況をちゃんと保存してるからね。",
    "トゥーンをクリックするか、ともだちリストから選ぶと、他のトゥーンとないしょ話ができるよ。",
    "スピードチャットのセリフの中には、体の動きがついているものもあるよ。",
    "もしキミのいる場所が混みすぎていたら、 トゥーンガイドを使って、ロビーを変えてみて。",
    "たくさんの建物をコグ達から取り戻すと、 トゥーンの頭の上に 金、銀、銅の星が付くよ！",
    "ある程度の建物を取り戻すと、トゥーンＨＱの黒板にキミの名前がのるかもね。",
    "コグから取り戻したビルが、再びコグに奪われることがあるよ。トゥーンの頭の上の星を維持するには、どんどんビルを取り戻そう！",
    "ひみつの友達の名前は青色の文字で表示されるよ。",
    # Fishing
    "キミはトゥーンタウンにいる全ての魚を集められるかな？",
    "池が違うと魚も違うよ。全ての池で釣りをしてみよう！",
    "魚のバケツが一杯になったらプレイグラウンドにいるペットショップのてんいんに売ろう！",
    "釣った魚は釣り人かペットショップで売ろう！",
    "強い釣りざおは、より重い魚を釣ることができるけど、買うのにより多くのジェリービーンが必要になるよ。",
    "より強い釣りざおはクララベルからカタログで購入できるよ。",
    "ペットショップにとって魚は、重ければ重いほど価値があるよ。",
    "珍しい魚はペットショップがより多いジェリービーンと交換してくれるよ。",
    "釣りをしているとたまにジェリービーンが入ったバッグを見つけることがあるよ。",
    "トゥーンタスクの中には池の中からあるアイテムを釣りあげるものがあるよ。",
    "プレイグラウンドの池とストリートの池では釣れる魚が違うよ。",
    "魚の中には本当に珍しい種類がいるよ。全部集めるまで釣り続けよう！",
    "キミのおうちの近くにある池では、そこでしか釣れない魚がいるよ。",
    "１０種類の魚を釣るごとに、トロフィーがもらえるよ！",
    "トゥーンガイドを見れば、どんな魚を釣ったかを見ることができるよ。",
    "トロフィーの中にはゲラゲラメーターをアップさせるものがあるよ。",
    "たくさんのジェリービーンを稼ぎたいなら、釣りがお勧めだよ！",
    # Doodles
    "ペットショップでドゥードゥルを手に入れよう！",
    "ペットショップでは毎日、新しいドゥードゥルが売ってるよ！",
    "どんなドゥードゥルがいるか、毎日ペットショップをチェックしに行ってみよう！",
    "ロビーが違うと、そこにいるドゥードゥルも違うよ。",
    # Karting
    "スピードウェイでキミのホットロッドを展示してレース相手を探そう!",
    "トゥーンタウン・セントラルのタイヤがたのトンネルから、グーフィー・サーキットに行こう!",
    "グーフィー・サーキットでゲラゲラポイントをゲットしよう!", 
    "グーフィー・サーキットには、６つのレーストラックがあるよ。 "
    ),

  TIP_STREET : (
    "コグにはロウボット、マネーボット、セルボット、ボスボットの４種類があるんだ。",
    "各ギャグトラックは、「めいちゅうりつ」と「ダメージ」がそれぞれ決まっているよ。",
    "「サウンド」ギャグは、すべてのコグにダメージをあたえるけど、「おとり」にはまったコグを逃してしまうよ。",
    "よく考えて、戦略的な順番でコグをたおすと、バトルで勝つチャンスがすごく増えるよ。",
    "「トゥーンアップ」はバトルの間、他のトゥーンのゲラゲラメーターを回復することができるよ。",
    "ギャグのスキルポイントは、「コグ侵略中」だと２倍になるよ。",
    "たくさんのトゥーンがバトルで同じギャグトラックを使うと、与えられるダメージが大きくなるよ。",
    "バトル中のギャグは、メニューに表示されている順番で上から下の順で使われるよ。",
    "コグに乗っ取られたビルのエレベーターの上のランプは、そのビルが何階建てかを示しているんだ。",
    "コグをクリックすると、もっと詳しい情報が見れるよ。",
    "高いレベルのギャグを低いレベルのコグに使っても、スキルレベルは増えないよ。",
    "バトル中のギャグのメニューで青い背景のギャグは、スキルレベルをかせぐことができるよ。",
    "コグのビルの中にいると、スキルレベルが増えるんだ。高い階ほど、たくさん増えるよ。",
    "コグが倒されると、バトルが終わった時まわりにいるトゥーンたちはみなそのコグに対するクレジットがもらえるんだ。",
    "トゥーンタウンの通りはそれぞれ、いろいろな種類やレベルのコグがまじっているよ。",
    "歩道にいれば、コグから攻撃はされないよ。",
    "通りでは、カンバンのないドアに近づくと、そのドアがジョークを言うんだ。",
    "トゥーンタスクを完了するうちに、キミは新しいギャグトラックで練習することになるんだ。７つのギャグトラックのうち６つを選ぶことになるから、気をつけて選んでね！",
    "「トラップ」は、バトルでキミかキミのともだちが「おとり」を使うようにする時だけ効果があるよ。",
    "高いレベルの「おとり」は、成功する確率が高いよ。",
    "低いレベルの「おとり」は、高いレベルのコグに対してあんまり効果がないよ。",
    "バトルで「おとり」にはまっていたら、コグは攻撃できないんだ。",
    "コグに乗っ取られたビルを取り戻すと、ごほうびで、キミたちが救ったトゥーンのビルの中に肖像画がかざられるよ。",
    "ゲラゲラメーターがすでにいっぱいのトゥーンをトゥーンアップしても、体力は回復しないよ。",
    "コグはどんなギャグにでも決まると簡単に気絶しちゃうんだ、だから同じラウンドで他のギャグが当たるチャンスが増えるんだよ。",
    "「ドロップ」ギャグは当たる確率は低いけど、同じラウンドで他のギャグが決まると、より当たりやすくなるんだ。",
    "コグをたくさん倒すと、トゥーンガイドのコグページを使って \"コグレーダー\"ができるようになるよ。",
    "バトル中に仲間のトゥーンがどのコグを攻撃しているかは\"-\"や\"X\"マークが教えてくれるよ。",
    "バトル中のコグ達の胸の場所にあるライトは、彼らの体力を表しているよ：\n緑は健康で、赤はこわれる寸前。",
    "バトルで同時に戦えるのは、最大４人のトゥーンまでだからね。",
    "ストリートでは、コグは一人のトゥーンよりも大勢のトゥーンたちのバトルに参加したがるよ。",
    "コグの種類の中でも強い２体は乗っ取られたビルの中にしか出てこないよ。",
    "「ドロップ」ギャグは「おとり」にハマったコグには通用しないよ。",
    "コグは最も大きなダメージを与えたトゥーンを攻撃する傾向があるよ。",
    "「サウンド」ギャグは「おとり」にハマったコグに対してはボーナスダメージが与えられないんだ。",
    "「おとり」にハマったコグを長い時間待たせると、目覚めてしまうよ。レベルの高い「おとり」だと効果がより長く持続するよ。",
    "池はトゥーンタウンのどのストリートにもあるよ。中には変わった魚もいるから色々ためしてみてね。",
    ),

  TIP_MINIGAME : (
    "ジェリービーンのびんがいっぱいになると、トロリーゲームで稼いだジェリービーンは全部自動的にキミの銀行からこぼれでちゃうよ。",
    "\"マッチミニーゲーム\"では、マウスのかわりにやじるしキーを使えるよ。",
    "\"たいほうゲーム\"では、やじるしキーを使って大砲を動かして、コントロールキーを押すと発砲できるよ。",
    "\"リングゲーム\"では、チームの全員がうきわをくぐって泳ぐのに成功するとボーナスポイントがもらえるよ。",
    "\"マッチミニーゲーム\"でかんぺきな踊りをすると、ジェリービーンを２倍もらえるよ。",
    "\"つなひきゲーム\"ではより強いコグに勝つと、より多いジェリービーンがもらえるよ。",
    "トロリーゲームの難しさは遊ぶ場所によって変わるよ：トゥーンタウンセントラルが一番簡単でドナルドのドリームランドが一番難しいよ。",
    "トロリーゲームのいくつかは仲間で参加しないと遊べないものがあるよ。",
    ),

  TIP_COGHQ : (
    "コグへの変装をコンプリートしないと、ボスのビルに入れないよ！",
    "警備兵の上にジャンプすると、しばらくの間、動きが止まるよ！",
    "コグをたくさん倒して、コグのメリットを集めよう！",
    "レベルの高いコグからは、より多くのメリットを手に入れることが出来るよ！",
    "コグのメリットを集めると「格上げ」されて、セルボットのコグゼキュティブに会いに行けるようになるよ！",
    "コグに変装しているときには、コグのように話すことが出来るよ！",
    "セルボットのコグゼキュティブとのバトルには最大８トゥーンまで参加できるよ！",
    "セルボットのコグゼキュティブは、コグ本部の一番上にいるよ！",
    "コグ工場の中では、階段に沿っていくことで工場長の所までたどり着くことができるよ！",
    "工場でのバトルごとに、コグへの変装パーツを１つ手に入れることができるよ！",
    "トゥーンガイドでコグへの変装の度合いをチェックすることができるよ！",
    "トゥーンガイドの変装のページで「メリット」の進行度合いをチェックできるよ！",
    "コグゼキュティブに会うときには、ギャグとゲラゲラメーターがまんたんかどうかをちゃんとチェックしてね。",
    "格上げされると、コグ変装グッズがアップデートされるよ。",
    "工場長を倒さないとコグに変装するパーツを手に入れることはできないよ。",
    "ドナルドのドリームランドでトゥーンタスクをやると、マネーボットのへんそうスーツがゲットできるよ!",
    "マネーボットほんぶには、コイン・ドル・ゴールドの3つの工場があるよ。",
    "マネーマネーがフラフラの時にきんこを投げないと、ヘルメットがわりにとられちゃうよ!きんこを当てて、ヘルメットをはじき飛ばそう!",
    "バトルでロウボットを倒してショウカンジョーを集めよう。",
    "レベルの高いコグを倒すとより多くのメリットが得られるよ。",
    "ショウカンジョーを集めてじゅうぶん格上げされたら、ロウボット本部のサイバンチョーにちょうせんだ！",
    "サイバンチョーにちょうせんするには、ロウボットのへんそうパーツがひつようだよ。",
    "サンバンチョーには同時に８人までいっしょにちょうせんできるよ。",
    "パズルにちょうせん！しっぱいするとバーチャル・コグがキミのショウカンをじゃまするよ。 ",
    "",
    "",
    "",
    "",
    "",
    "",
    ),
  TIP_ESTATE : (
    # Doodles #★
    "ドゥードゥルはスピードチャットのいくつかのセリフがわかるから試してみよう！",
    "スピードチャットの\"ペット\"の項目からドゥードゥルに「トリック」をさせよう！",
    "クララベルのショッピングカタログのアイテムでドゥードゥルに「トリック」を教えることができるぞ！",
    "ドゥードゥルが「トリック」をしたら、ごほうびをあげよう！",
    "友達のおうちに遊びにいくと、キミのドゥードゥルもついてくるよ。",
    "ドゥードゥルが「くうふく」のときにはジェリービーンをあげよう。",
    "ドゥードゥルをクリックすればパネルが開くよ。そうしたら、エサをあげたり、なでたり、呼んでみよう。",
    "ドゥードゥルは集まるのが好き。友達を呼んで、一緒に遊ぼう！",
    "全てのドゥードゥルはそれぞれ違う個性をもっているよ。",
    "キミのドゥードゥルをペットショップに返して、新しいドゥードゥルを手に入れることもできるぞ。",
    "ドゥードゥルが「トリック」をつかうと、そのまわりにいるトゥーンがトゥーンアップするぞ。",
    "練習すればするほどドゥードゥルの「トリック」がうまくなるから、がんばってみよう。",
    "上達したドゥードゥルの「トリック」は、トゥーンアップの効果も大きいぞ。",
    "「トリック」をするとドゥードゥルは疲れるけど、経験のあるドゥードゥルはより多くできるぞ！",
    "トゥーンの近くにいるドゥードゥルのリストは、ともだちリストの場所でみることができるぞ。",
    # Furniture / Cattlelog
    "クララベルのカタログから家具を買って、おうちのインテリアをコーディネートしよう。",
    "貯ビーン箱にはもっとジェリービーンをたくわえこむことができるぞ。",
    "クローゼットにはキミの着ていないようふくを入れておけるよ。たまには着替えて出かけよう！",
    "ともだちのおうちに遊びに行ったら、ようふくを試着させてもらおう！",
    "カタログからより良いつりざおを買って、変わった魚を釣ろう！",
    "大きな貯ビーン箱を買えばもっとジェリービーンをとっておけるぞ！",
    "クララベルに連絡したいときには、おうちの電話をつかってね。",
    "より大きなクローゼットもクララベルのカタログから買うことができるよ。",
    "「ようふく券」を使うときには、クローゼットに空きを作っておこう。",
    "キミのおうちをおしゃれにする色々なアイテムを扱ってるよ！",
    "クララベルに注文をしたら、キミのおうちの前のポストをチェックしてみよう！",
    "カタログでようふくを注文すると、１時間でポストに届くよ。",
    "かべ紙や床のフローリングは注文してから１時間かかるよ。",
    "買った家具がおうちに届くには丸１日かかるよ。",
    "屋根裏に余った家具をとっておこう。",
    "クララベルから連絡があると、それは新しい商品カタログがついたってこと。",
    "ショッピングカタログが届くと、クララベルから連絡がくるよ！",
    "新しいショッピングカタログは毎週届くよ！",
    "カタログのある時期にしか売ってないアイテムの中でも、１年中使えるものがあるから探してみよう！",
    "いらない家具はごみ箱に移そう。",
    # Fish
    "ホーレーマカレルのようなサカナは、キミのおうちの近くの池のほうが、よく見かけるらしい。",
    # Misc
    "スピードチャットを使って、ともだちをキミのおうちに呼ぼう！",
    "キミのおうちの色は最初にトゥーンを作ったときのパネルの色と同じだって知ってた？",
    ),
   TIP_KARTING : (
    # Goofy Speedway zone specific
    "グーフィーのオートショップで、ロードスターやトゥーンヴィークルや、クルーザーを買おう。", 
    "グーフィーのオートショップで、キミのカートの色やパーツをカスタムしよう。", 
    "グーフィー・サーキットでレースをして、チケットをゲットしよう。",
    "グーフィーのオートショップで買い物をする時は、チケットを使うんだ。",
    "レース参加に使うデポジットは、レースのあとに返ってくるよ。",
    "トゥーンガイドのステッカーブックで、キミのカートをカスタムしよう。", 
    "トゥーンガイドのステッカーブックで、キミのカートでのベストラップがみれるよ。", 
    "トゥーンガイドのステッカーブックで、キミがレースでゲットしたトロフィーが見れるよ。", 
    "スクリュースタジアムがグーフィー・サーキットで一番かんたんなコースだよ。", 
    "エアボーン・エーカースはグーフィー・サーキットで一番ジャンプが多いコースだよ。", 
    "ブリザード・ブルバードはグーフィー・サーキットで一番むずかしいんだ。", 
    ),
    TIP_GOLF: (
    # Golfing specific
    "コースを上から見る時はTabキーを押してね。",
    "パットの方向をカップにまっすぐにするには、上矢印(↑)キーを押してね。",
    "クラブのスイングのコントロールはパイ投げと同じだよ。",
    ),
    }

FishGenusNames = {
    0 : "ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
    2 : "ｷｬｯﾄ ﾌｨｯｼｭ",
    4 : "ｸﾗｳﾝ ﾌｨｯｼｭ",
    6 : "ﾌﾛｰｽﾞﾝ ﾌｨｯｼｭ",
    8 : "ｽﾀｰ ﾌｨｯｼｭ",
    10 : "ﾎｰﾚｰ ﾏｶﾚﾙ",
    12 : "ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
    14 : "ｱﾓｰﾚ ｲｰﾙ",
    16 : "ﾅｰｽ ｼｬｰｸ",
    18 : "ｷﾝｸﾞ ｸﾗﾌﾞ",
    20 : "ﾑｰﾝ ﾌｨｯｼｭ",
    22 : "ｼｰ ﾎｰｽ",
    24 : "ﾌﾟｰﾙ ｼｬｰｸ",
    26 : "ﾍﾞｱ ｱｷｭｰﾀﾞ",
    28 : "ｶｯﾄｽﾛｰﾄ ﾄﾗｳﾄ",
    30 : "ﾋﾟｱﾉ ﾂﾅ",
    32 : "PB&J ﾌｨｯｼｭ",
    34 : "ﾃﾞﾋﾞﾙ ﾚｲ",
    }

FishSpeciesNames = {
    0 : ( "ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
          "ﾎｯﾄｴｱｰ ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
          "ｳｪｻﾞｰ ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
          "ｳｫｰﾀｰ ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
          "ﾚｯﾄﾞ ﾊﾞﾙｰﾝ ﾌｨｯｼｭ",
          ),
    2 : ( "ｷｬｯﾄ ﾌｨｯｼｭ",
          "ｼｬﾑ ｷｬｯﾄ ﾌｨｯｼｭ",
          "ｱﾚｰ ｷｬｯﾄ ﾌｨｯｼｭ",
          "ﾀﾋﾞｰ ｷｬｯﾄ ﾌｨｯｼｭ",
          "ﾄﾑ ｷｬｯﾄ ﾌｨｯｼｭ",
          ),
    4 : ( "ｸﾗｳﾝ ﾌｨｯｼｭ",
          "ｻｯﾄﾞ ｸﾗｳﾝ ﾌｨｯｼｭ",
          "ﾊﾟｰﾃｨｰ ｸﾗｳﾝ ﾌｨｯｼｭ",
          "ｻｰｶｽ ｸﾗｳﾝ ﾌｨｯｼｭ",
          ),
    6 : ( "ﾌﾛｰｽﾞﾝ ﾌｨｯｼｭ",
          ),
    8 : ( "ｽﾀｰ ﾌｨｯｼｭ",
          "ﾌｧｲﾌﾞ ｽﾀｰ ﾌｨｯｼｭ",
          "ﾛｯｸ ｽﾀｰ ﾌｨｯｼｭ",
          "ｼｬｲﾆﾝｸﾞ ｽﾀｰ ﾌｨｯｼｭ",
          "ｵｰﾙ ｽﾀｰ ﾌｨｯｼｭ",
          ),
    10 : ( "ﾎｰﾚｰ ﾏｶﾚﾙ",
           ),
    12 : ( "ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
           "ﾌﾞﾙ ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
           "ﾎｯﾄ ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
           "ﾀﾞﾙﾒｼｱ ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
           "ﾊﾟﾋﾟｰ ﾄﾞｯｸﾞ ﾌｨｯｼｭ",
           ),
    14 : ( "ｱﾓｰﾚ ｲｰﾙ",
           "ｴﾚｸﾄﾘｯｸ ｱﾓｰﾚ ｲｰﾙ",
           ),
    16 : ( "ﾅｰｽ ｼｬｰｸ",
           "ｸﾗﾗ ﾅｰｽ ｼｬｰｸ",
           "ﾌﾛｰﾚﾝｽ ｼｬｰｸ ",
           ),
    18 : ( "ｷﾝｸﾞ ｸﾗﾌﾞ",
           "ｱﾗｽｶ ｷﾝｸﾞ ｸﾗﾌﾞ",
           "ｵｰﾙﾄﾞ ｷﾝｸﾞ ｸﾗﾌﾞ",
           ),
    20 : ( "ﾑｰﾝ ﾌｨｯｼｭ",
           "ﾌﾙﾑｰﾝ ﾌｨｯｼｭ",
           "ﾊｰﾌﾑｰﾝ ﾌｨｯｼｭ",
           "ﾆｭｰﾑｰﾝ ﾌｨｯｼｭ",
           "ｸﾚｾﾝﾄﾑｰﾝ ﾌｨｯｼｭ",
           "ﾊｰﾍﾞｽﾄﾑｰﾝ ﾌｨｯｼｭ",
           ),
    22 : ( "ｼｰ ﾎｰｽ",
           "ﾛｯｷﾝｸﾞ ｼｰ ﾎｰｽ",
           "ｸﾗｲｽﾞﾃﾞｰﾙ ｼｰ ﾎｰｽ",
           "ｱﾗﾋﾞｱﾝ ｼｰ ﾎｰｽ",
           ),
    24 : ( "ﾌﾟｰﾙ ｼｬｰｸ",
           "ｷﾃﾞｨｰ ﾌﾟｰﾙ ｼｬｰｸ",
           "ｽｲﾐﾝｸﾞ ﾌﾟｰﾙ ｼｬｰｸ",
           "ｵﾘﾝﾋﾟｯｸ ﾌﾟｰﾙ ｼｬｰｸ",
           ),
    26 : ( "ﾌﾞﾗｳﾝ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ﾌﾞﾗｯｸ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ｺｱﾗ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ﾊﾆｰ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ﾎﾟｰﾗｰ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ﾊﾟﾝﾀﾞ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ｺﾃﾞｨｱｯｸ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           "ｸﾞﾘｽﾞﾘｰ ﾍﾞｱｰ ｱｷｭｰﾀﾞ",
           ),
    28 : ( "ｶｯﾄｽﾛｰﾄ ﾄﾗｳﾄ",
           "ｷｬﾌﾟﾃﾝ ｶｯﾄｽﾛｰﾄ ﾄﾗｳﾄ",
           "ｽｶｰﾋﾞｰ ｶｯﾄｽﾛｰﾄ ﾄﾗｳﾄ",
           ),
    30 : ( "ﾋﾟｱﾉ ﾂﾅ",
           "ｸﾞﾗﾝﾄﾞﾋﾟｱﾉ ﾂﾅ",
           "ﾍﾞﾋﾞｰ ｸﾞﾗﾝﾄﾞﾋﾟｱﾉ ﾂﾅ",
           "ｱｯﾌﾟﾗｲﾄ ﾋﾟｱﾉ ﾂﾅ",
           "ﾌﾟﾚｲﾔｰ ﾋﾟｱﾉ ﾂﾅ",
           ),
    32 : ( "PB&J ﾌｨｯｼｭ",
           "ｸﾞﾚｰﾌﾟ PB&J ﾌｨｯｼｭ",
           "ｸﾗﾝﾁｰ PB&J ﾌｨｯｼｭ",
           "ｽﾄﾛﾍﾞﾘｰ PB&J ﾌｨｯｼｭ",
           "ｺﾝｺﾙﾄﾞ ｸﾞﾚｰﾌﾟ PB&J ﾌｨｯｼｭ",
           ),
    34 : ( "ﾃﾞﾋﾞﾙ･ﾚｲ",
           ),
    }

CogPartNames = (
    "左レッグ①", "左レッグ②", "左フット",
    "右レッグ①", "右レッグ②", "右フット",
    "左ショルダー",  "右ショルダー", "ボディ①", "コグメーター", "ボディ②",
    "左アーム①",  "左アーム②", "左ハンド",
    "右アーム①", "右アーム②", "右ハンド",
    )

CogPartNamesSimple = (
    "ボディ上",
    )

FishFirstNames = (
    "",
    "ｴﾝｼﾞｪﾙ",
    "ｱｰﾃｨｯｸ",
    "ﾍﾞｲﾋﾞｰ",
    "ﾊﾞﾐｭｰﾀﾞ",
    "ﾋﾞｯｸﾞ",
    "ﾌﾞﾙｰｸ",
    "ﾊﾞﾌﾞﾙｽ",
    "ﾊﾞｽﾀｰ",
    "ｷｬﾝﾃﾞｨｰ",
    "ｷｬﾌﾟﾃﾝ",
    "ﾁｯﾌﾟ",
    "ﾁｬﾌﾞ",
    "ｺｰﾗﾙ",
    "ﾄﾞｸﾀｰ",
    "ﾀﾞｽﾃｨｰ",
    "ｴﾝﾍﾟﾗｰ",
    "ﾌｧﾝｸﾞｽ",
    "ﾌｧｯﾄ",
    "ﾌｨｯｼｰ",
    "ﾌﾘｯﾊﾟｰ",
    "ﾌﾗｳﾝﾀﾞｰ",
    "ﾌﾚｯｸﾙ",
    "ﾊﾆｰ",
    "ｼﾞｬｯｸ",
    "ｷﾝｸﾞ",
    "ﾘﾄﾙ",
    "ﾏｰﾘﾝ",
    "ﾐｽ",
    "ﾐｽﾀｰ",
    "ﾋﾟｰﾁ",
    "ﾋﾟﾝｷｰ",
    "ﾌﾟﾘﾝｽ",
    "ﾌﾟﾘﾝｾｽ",
    "ﾌﾟﾛﾌｪｯｻｰ",
    "ﾊﾟﾌｨｰ",
    "ｸｨｰﾝ",
    "ﾚｲﾝﾎﾞｰ",
    "ﾚｲ",
    "ﾛｰｼﾞｰ",
    "ﾗｽﾃｨｰ",
    "ｿﾙﾃｨｰ",
    "ｻﾑ",
    "ｻﾝﾃﾞｨｰ",
    "ｽｹｰﾙｽ",
    "ｼｬｰｷｰ",
    "ｻｰ",
    "ｽｷｯﾋﾟｰ",
    "ｽｷｯﾊﾟｰ",
    "ｽﾅｯﾊﾟｰ",
    "ｽﾍﾟｯｸ",
    "ｽﾊﾟｲｸ",
    "ｽﾎﾟｯﾃｨｰ",
    "ｽﾀｰ",
    "ｼｭｶﾞｰ",
    "ｽｰﾊﾟｰ",
    "ﾀｲｶﾞｰ",
    "ﾀｲﾆｰ",
    "ｳｨｽｶｰｽﾞ",
    )

FishLastPrefixNames = (
    "",
    "ﾋﾞｰﾁ",
    "ﾌﾞﾗｯｸ",
    "ﾌﾞﾙｰ",
    "ﾎﾞｱ",
    "ﾌﾞﾙ",
    "ｷｬｯﾄ",
    "ﾃﾞｨｰﾌﾟ",
    "ﾀﾞﾌﾞﾙ",
    "ｲｰｽﾄ",
    "ﾌｧﾝｼｰ",
    "ﾌﾚｰｷｰ",
    "ﾌﾗｯﾄ",
    "ﾌﾚｯｼｭ",
    "ｼﾞｬｲｱﾝﾄ",
    "ｺﾞｰﾙﾄﾞ",
    "ｺﾞｰﾙﾃﾞﾝ",
    "ｸﾞﾚｲ",
    "ｸﾞﾘｰﾝ",
    "ﾎｸﾞ",
    "ｼﾞｬﾊﾞｰ",
    "ｼﾞｪﾘｰ",
    "ﾚﾃﾞｨｰ",
    "ﾚｻﾞｰ",
    "ﾚﾓﾝ",
    "ﾛﾝｸﾞ",
    "ﾉｰｻﾞﾝ",
    "ｵｰｼｬﾝ",
    "ｵｸﾄ",
    "ｵｲﾙ",
    "ﾊﾟｰﾙ",
    "ﾊﾟﾌ",
    "ﾚｯﾄﾞ",
    "ﾘﾎﾞﾝ",
    "ﾘﾊﾞｰ",
    "ﾛｯｸ",
    "ﾙﾋﾞｰ",
    "ﾗﾀﾞｰ",
    "ｿﾙﾄ",
    "ｼｰ",
    "ｼﾙﾊﾞｰ",
    "ｼｭﾉｰｹﾙ",
    "ｿｰﾙ",
    "ｻｻﾞﾝ",
    "ｽﾊﾟｲｷｰ",
    "ｻｰﾌ",
    "ｿｰﾄﾞ",
    "ﾀｲｶﾞｰ",
    "ﾄﾘﾌﾟﾙ",
    "ﾄﾛﾋﾟｶﾙ",
    "ﾂﾅ",
    "ｳｪｰﾌﾞ",
    "ｳｨｰｸ",
    "ｳｴｽﾄ",
    "ﾎﾜｲﾄ",
    "ｲｴﾛｰ",
    )

FishLastSuffixNames = (
    "",
    "ﾎﾞｰﾙ",
    "ﾊﾞｽ",
    "ﾍﾞﾘｰ",
    "ﾊﾞｸﾞ",
    "ﾊﾞｰｸﾞﾗｰ",
    "ﾊﾞﾀｰ",
    "ｸﾛｰ",
    "ｺﾌﾞﾗｰ",
    "ｸﾗﾌﾞ",
    "ｸﾛｰｶｰ",
    "ﾄﾞﾗﾑ",
    "ﾌｨﾝ",
    "ﾌｨｯｼｭ",
    "ﾌﾗｯﾊﾟｰ",
    "ﾌﾘｯﾊﾟｰ",
    "ｺﾞｰｽﾄ",
    "ｸﾞﾗﾝﾄ",
    "ﾍｯﾄﾞ",
    "ｼﾞｬｹｯﾄ",
    "ｼﾞｬﾝﾊﾟｰ",
    "ﾏｶﾚﾙ",
    "ﾑｰﾝ",
    "ﾏｳｽ",
    "ﾐｭﾚｰ",
    "ﾈｯｸ",
    "ﾉｰｽﾞ",
    "ﾊﾟｰﾁ",
    "ﾗﾌｨｰ",
    "ﾗﾝﾅｰ",
    "ｾｲﾙ",
    "ｼｬｰｸ",
    "ｼｪﾙ",
    "ｼﾙｸ",
    "ｽﾗｲﾑ",
    "ｽﾅｯﾊﾟｰ",
    "ｽﾃｨﾝｸ",
    "ﾃｲﾙ",
    "ﾄｰﾄﾞ",
    "ﾄﾗｳﾄ",
    "ｳｫｰﾀｰ",
    )

# SellbotLegFactorySpec.py

SellbotLegFactorySpecMainEntrance = "メインゲート"
SellbotLegFactorySpecLobby = "ロビー"
SellbotLegFactorySpecLobbyHallway = "廊下"
SellbotLegFactorySpecGearRoom = "ギヤルーム"
SellbotLegFactorySpecBoilerRoom = "ボイラールーム"
SellbotLegFactorySpecEastCatwalk = "東の通路"
SellbotLegFactorySpecPaintMixer = "ペンキルーム"
SellbotLegFactorySpecPaintMixerStorageRoom = "ペンキルーム倉庫"
SellbotLegFactorySpecWestSiloCatwalk = "西タワー通路"
SellbotLegFactorySpecPipeRoom = "パイプルーム"
SellbotLegFactorySpecDuctRoom = "ダクトルーム"
SellbotLegFactorySpecSideEntrance = "サイドゲート"
SellbotLegFactorySpecStomperAlley = "プレスルーム"
SellbotLegFactorySpecLavaRoomFoyer = "ヨウガンルーム"
SellbotLegFactorySpecLavaRoom = "ヨウガンルーム"
SellbotLegFactorySpecLavaStorageRoom = "ヨウガンルーム倉庫"
SellbotLegFactorySpecWestCatwalk = "西の通路"
SellbotLegFactorySpecOilRoom = "オイルルーム"
SellbotLegFactorySpecLookout = "見張り台"
SellbotLegFactorySpecWarehouse = "倉庫"
SellbotLegFactorySpecOilRoomHallway = "オイルルーム入口"
SellbotLegFactorySpecEastSiloControlRoom = "東コントロールルーム"
SellbotLegFactorySpecWestSiloControlRoom = "西コントロールルーム"
SellbotLegFactorySpecCenterSiloControlRoom = "工場長の部屋"
SellbotLegFactorySpecEastSilo = "東タワー屋上"
SellbotLegFactorySpecWestSilo = "西タワー屋上"
SellbotLegFactorySpecCenterSilo = "メインタワー屋上"
SellbotLegFactorySpecEastSiloCatwalk = "東タワー通路"
SellbotLegFactorySpecWestElevatorShaft = "西エレベーター"
SellbotLegFactorySpecEastElevatorShaft = "東エレベーター"

#FISH BINGO
FishBingoBingo = "ビンゴ！"
FishBingoVictory = "やったね！"
FishBingoJackpot = "ジャックポット！"
FishBingoGameOver = "ゲームオーバー"
FishBingoIntermission = "お休み終了まで\nあと"
FishBingoNextGame = "ゲーム開始まで\nあと"
FishBingoTypeNormal = "クラシック"
FishBingoTypeCorners = "4コーナー"
FishBingoTypeDiagonal = "ななめ"
FishBingoTypeThreeway = "3ウェイ！"
FishBingoTypeBlockout = "ブロックアウト！"
FishBingoStart = "「魚でビンゴ！」の時間です！ 遊びたい人は好きな橋に立ってね。"
FishBingoOngoing = "フィッシュビンゴをかいさい中だよ！"
FishBingoEnd = "魚でビンゴ！、楽しかった？"
FishBingoHelpMain = "「魚でビンゴ！」へようこそ！ 時間内にみんなで協力して、ビンゴカードをマークしよう！"
FishBingoHelpFlash = "魚を釣ったら、点滅している場所のひとつをクリックしてカードにマークしてね。"
FishBingoHelpNormal = "これは普通のビンゴカードだよ。たて、よこ、ななめ一列にマークがつけば勝ち！"
FishBingoHelpDiagonals = "ななめに２本、バッテンになるようにマークしたら勝ち！"
FishBingoHelpCorners = "簡単なコーナーカード。４つのコーナーをマークしたら勝ち！"
FishBingoHelpThreeway = "3ウェイ！  ななめ２本と真ん中の横ラインをマークしたら勝ち！なかなか難しいぞ！"
FishBingoHelpBlockout = "ブロックアウト！ 全ての場所をマークすれば勝ち。他の全ての池にいるトゥーンと競ってジャックポットを目指そう！"
FishBingoOfferToSellFish = "キミのバケツが一杯だよ。魚を売りますか？"
FishBingoJackpotWin = "%s　ジェリービーン　ゲット!"

# ResistanceSCStrings: SpeedChat phrases rewarded for defeating the CFO.
# It is safe to remove entries from this list, which will disable them
# for use from any toons who have already purchased them.  Note that the
# index numbers are stored directly in the database, so once assigned
# to a particular phrase, a given index number should never be
# repurposed to any other phrase.
ResistanceToonupMenu = "ﾄｩｰﾝｱｯﾌﾟ"
ResistanceToonupItem = "%s ﾄｩｰﾝｱｯﾌﾟ"
ResistanceToonupItemMax = "さいだい"
ResistanceToonupChat = "トゥーン最高！ﾄｩｰﾝｱｯﾌﾟ!" #▲
ResistanceRestockMenu = "ｷﾞｬｸﾞｱｯﾌﾟ"
ResistanceRestockItem = "%s ｷﾞｬｸﾞｱｯﾌﾟ"
ResistanceRestockItemAll = "すべて"
ResistanceRestockChat = "笑って！ｷﾞｬｸﾞｱｯﾌﾟ！" #▲
ResistanceMoneyMenu = "ｼﾞｪﾘｰﾋﾞｰﾝ"
ResistanceMoneyItem = "ｼﾞｪﾘｰﾋﾞｰﾝ %s個"
ResistanceMoneyChat = "かしこく使おう！トゥーン最高！" #▲

# Resistance Emote NPC chat phrases #localize
ResistanceEmote1 = NPCToonNames[9228] + ": レジスタンスへようこそ！"
ResistanceEmote2 = NPCToonNames[9228] + ": 新しい'きもち'を使ってじぶんをひょうげんしてみよう。"
ResistanceEmote3 = NPCToonNames[9228] + ": がんばってね！"

# Kart racing
KartUIExit = "おりる"
KartShop_Cancel = lCancel
KartShop_BuyKart = "かう"
KartShop_BuyAccessories = "アクセサリーをかう"
KartShop_BuyAccessory = "アクセサリーをかう"
KartShop_Cost = "ねだん: %d チケット"
KartShop_ConfirmBuy = "%sを%dチケットでかう？"
KartShop_NoAvailableAcc = "この種類のアクセサリーはダメだよ。"
KartShop_FullTrunk = "キミのトランクがいっぱいだよ。"
KartShop_ConfirmReturnKart = "本当にキミのカートを返してもいい？"
KartShop_ConfirmBoughtTitle = "おめでとう！"
KartShop_NotEnoughTickets = "じゅうぶんなチケットがありません。"

KartView_Rotate = "かいてん"
KartView_Right = "右"
KartView_Left = "左"

# starting block
StartingBlock_NotEnoughTickets = "チケットが足りないよ。かわりにれんしゅうのレースに出よう！"
StartingBlock_NoBoard = "今回のレースは申し込みがおわったよ。次のレースまで待っててね。"
StartingBlock_NoKart = "まずはカートが必要だね！カートショップのてんいんに聞いてみよう。"
StartingBlock_Occupied = "この場所はすでにうまっています。ほかの場所をためしてね。"
StartingBlock_TrackClosed = "ごめんね、このレーストラックは工事中です。"
StartingBlock_EnterPractice = "れんしゅうのレースに出ますか？"
StartingBlock_EnterNonPractice = "%sのレースにチケット%s枚で参加しますか？"
StartingBlock_EnterShowPad = "ここにキミのカートを止めますか？"
StartingBlock_KickSoloRacer = "トゥーンバトルレースはひとりではできないよ。"
StartingBlock_Loading = "レースに行く!"

#stuff for leader boards
LeaderBoard_Time = "タイム"
LeaderBoard_Name = "レーサー名"
LeaderBoard_Daily = "ほんじつのベストタイム"
LeaderBoard_Weekly = "しゅうかんベストタイム"
LeaderBoard_AllTime = "ベストタイムのでんどう"

RecordPeriodStrings = [
    LeaderBoard_Daily,
    LeaderBoard_Weekly,
    LeaderBoard_AllTime,
    ]

KartRace_RaceNames = [
    "れんしゅう",
    "トゥーンバトル",
    "トーナメント",
    ]

from toontown.racing import RaceGlobals

KartRace_Go = "スタート！"
KartRace_Reverse = "リバース "

#needed for leader boards
KartRace_TrackNames = {
  RaceGlobals.RT_Speedway_1     : "スクリュースタジアム",
  RaceGlobals.RT_Speedway_1_rev : KartRace_Reverse + "スクリュースタジアム",
  RaceGlobals.RT_Rural_1        : "さびさびレースウェイ",
  RaceGlobals.RT_Rural_1_rev    : KartRace_Reverse + "さびさびレースウェイ",
  RaceGlobals.RT_Urban_1        : "シティーサーキット",
  RaceGlobals.RT_Urban_1_rev    : KartRace_Reverse + "シティーサーキット",
  RaceGlobals.RT_Speedway_2     : "きりもみコロシアム",
  RaceGlobals.RT_Speedway_2_rev : KartRace_Reverse + "きりもみコロシアム",
  RaceGlobals.RT_Rural_2        : "エアボーンエーカース",
  RaceGlobals.RT_Rural_2_rev    : KartRace_Reverse + "エアボーンエーカース",
  RaceGlobals.RT_Urban_2        : "ブリザードブルバード",
  RaceGlobals.RT_Urban_2_rev    : KartRace_Reverse + "ブリザードブルバード",
  }

KartRace_Unraced = "N/A"

KartDNA_KartNames = {
    0:"ｸﾙｰｻﾞｰ",
    1:"ﾛｰﾄﾞｽﾀｰ",
    2:"ﾄｩｰﾝﾋﾞｰｸﾙ"
    }

KartDNA_AccNames = {
    #engine block accessory names
    1000: "ｴｱｰｸﾘｰﾅｰ",
    1001: "4ﾊﾞﾚﾙ",
    1002: "ﾌﾗｲﾝｸﾞｲｰｸﾞﾙ",
    1003: "ｽﾃｱ ﾎｰﾝ",
    1004: "ｽﾄﾚｰﾄ6",
    1005: "ｽﾓｰﾙ ｽｸｰﾌﾟ",
    1006: "ｼﾝｸﾞﾙ ｵｰﾊﾞｰﾍｯﾄﾞ",
    1007: "ﾐﾃﾞｨｱﾑ ｽｸｰﾌﾟ",
    1008: "ｼﾝｸﾞﾙ ﾊﾞﾚﾙ",
    1009: "ﾌﾗｸﾞﾙ ﾎｰﾝ",
    1010: "ｽﾄﾗｲﾌﾟ ｽｸｰﾌﾟ",
    #spoiler accessory names
    2000: "ｽﾍﾟｰｽ ｳｨﾝｸﾞ",
    2001: "ﾂｷﾞﾊｷﾞ ｽﾍﾟｱ",
    2002: "ﾛｰﾙ ｹｰｼﾞ",
    2003: "ｼﾝｸﾞﾙ ﾌｨﾝ",
    2004: "ﾀﾞﾌﾞﾙﾃﾞｯｶｰ ｳｨﾝｸﾞ",
    2005: "ｼﾝｸﾞﾙ ｳｲﾝｸﾞ",
    2006: "ｽﾀﾝﾀﾞｰﾄﾞ ｽﾍﾟｱ",
    2007: "ｼﾝｸﾞﾙ ﾌｨﾝ",
    2008: "sp9",
    2009: "sp10",
    #front wheel well accessory names
    3000: "ｹｯﾄｰ ﾎｰﾝ",
    3001: "ﾌﾚﾃﾞｨｰ ﾌｪﾝﾀﾞｰ",
    3002: "ｺﾊﾞﾙﾄ ｽﾃｯﾌﾟ",
    3003: "ｺﾌﾞﾗ ｻｲﾄﾞﾊﾟｲﾌﾟ",
    3004: "ｽﾄﾚｰﾄ ｻｲﾄﾞﾊﾟｲﾌﾟ",
    3005: "ﾎﾀﾃ ﾌｪﾝﾀﾞｰ",
    3006: "ｶｰﾎﾞﾝ ｽﾃｯﾌﾟ",
    3007: "ｳｯﾄﾞ ｽﾃｯﾌﾟ",
    3008: "fw9",
    3009: "fw10",
    #rear wheel well accessory names (twisty twisty)
    4000: "ｸﾙｸﾙ ﾃｰﾙﾊﾟｲﾌﾟ",
    4001: "ｽﾌﾟﾗｯｼｭ ﾌｪﾝﾀﾞｰ",
    4002: "ﾃﾞｭｱﾙ ｴｸﾞｿﾞｰｽﾄ",
    4003: "ﾌﾟﾚｰﾝ ﾃﾞｭｱﾙﾌｨﾝ",
    4004: "ﾌﾟﾚｰﾝ ﾄﾞﾛﾖｹ",
    4005: "ｸｱｯﾄﾞ ｴｸﾞｿﾞｰｽﾄ",
    4006: "ﾃﾞｭｱﾙ ﾌﾚｱｰ",
    4007: "ﾒｶﾞ ｴｸﾞｿﾞｰｽﾄ",
    4008: "ｽﾄﾗｲﾌﾟ ﾃﾞｭｱﾙﾌｨﾝ",
    4009: "ﾊﾞﾌﾞﾙ ﾃﾞｭｱﾙﾌｨﾝ",
    4010: "ｽﾄﾗｲﾌﾟ ﾄﾞﾛﾖｹ",
    4011: "ﾐｯｷｰ ﾄﾞﾛﾖｹ",
    4012: "ﾎﾀﾃ ﾄﾞﾛﾖｹ",
    #rim accessoKartRace_Exit = "Leave Race"ry names
    5000: "ﾀｰﾎﾞ",
    5001: "ﾑｰﾝ",
    5002: "ﾂｷﾞﾊｷﾞ",
    5003: "3ｽﾎﾟｰｸ",
    5004: "ﾍﾟｲﾝﾄﾘｯﾄﾞ",
    5005: "ﾊｰﾄ",
    5006: "ﾐｯｷｰ",
    5007: "5ﾎﾞﾙﾄ",
    5008: "ﾃﾞｲｼﾞｰ",
    5009: "ﾊﾞｽｹｯﾄﾎﾞｰﾙ",
    5010: "ﾋﾌﾟﾉ",
    5011: "ﾄﾗｲﾊﾞﾙ",
    5012: "ｼﾞｪﾑｽﾄｰﾝ",
    5013: "5ｽﾎﾟｰｸ",
    5014: "ﾉｯｸｵﾌ",
    #decal accessory names
    6000: "ﾅﾝﾊﾞｰ5",
    6001: "ｽﾌﾟﾗｯﾀｰ",
    6002: "ﾁｪｯｶｰﾎﾞｰﾄﾞ",
    6003: "ﾌﾚｲﾑ",
    6004: "ﾊｰﾂ",
    6005: "ﾊﾞﾌﾞﾙｽ",
    6006: "ﾀｲｶﾞｰ",
    6007: "ﾌﾗﾜｰ",
    6008: "ﾗｲﾄﾆﾝｸﾞ",
    6009: "ｴﾝｼﾞｴﾙ",
    #paint accessory names
    7000: "ｼｬﾙﾄﾙｰｽﾞ",
    7001: "ﾋﾟｰﾁ",
    7002: "ﾌﾞﾗｲﾄﾚｯﾄﾞ",
    7003: "ﾚｯﾄﾞ",
    7004: "ﾏﾙｰﾝ",
    7005: "ｼｴﾅ",
    7006: "ﾌﾞﾗｳﾝ",
    7007: "ﾀﾝ",
    7008: "ｺｰﾗﾙ",
    7009: "ｵﾚﾝｼﾞ",
    7010: "ｲｴﾛｰ",
    7011: "ｸﾘｰﾑ",
    7012: "ｼﾄﾘｰﾝ",
    7013: "ﾗｲﾑ",
    7014: "ｼｰｸﾞﾘｰﾝ",
    7015: "ｸﾞﾘｰﾝ",
    7016: "ﾗｲﾄﾌﾞﾙｰ",
    7017: "ｱｸｱ",
    7018: "ﾌﾞﾙｰ",
    7019: "ﾍﾟﾘｳｨﾝｸﾙ",
    7020: "ﾛｲﾔﾙﾌﾞﾙ-",
    7021: "ｽﾚｰﾄﾌﾞﾙｰ",
    7022: "ﾊﾟｰﾌﾟﾙ",
    7023: "ﾗﾍﾞﾝﾀﾞｰ",
    7024: "ﾋﾟﾝｸ",
    7025: "ﾌﾟﾗﾑ",
    7026: "ﾌﾞﾗｯｸ",
    }

RaceHoodSpeedway = "スピードウェイ"
RaceHoodRural = "なごやか"
RaceHoodUrban = "アーバン"
RaceTypeCircuit = "トーナメント"
RaceQualified = "よせんつうか"
RaceSwept = "ぜんしょう!"
RaceWon = "かち"
Race = "レース"
Races = "レース"
Total = "合計"
GrandTouring = "グランドツーリング"

def getTrackGenreString(genreId):
    genreStrings = [ "Speedway",
                     "Country",
                     "City" ]
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
    str(RaceGlobals.TrophiesPerCup) + " カートレースのトロフィーゲット！\nゲラゲラポイント、アップ！",
    str(RaceGlobals.TrophiesPerCup * 2) + " カートレースのトロフィーゲット！\nゲラゲラポイント、アップ！",
    str(RaceGlobals.TrophiesPerCup * 3) + " カートレースのトロフィーゲット！\nゲラゲラポイント、アップ！",
    ]

KartRace_TitleInfo = "レースの準備はいいかな？"
KartRace_SSInfo = "スクリュースタジアムへようこそ！\nエンジンをふかして、ハンドルをにぎりしめて！\n"
KartRace_CoCoInfo = "きりもみコロシアムにようこそ!\nスピードを落さないように、バンクをうまく使ってね。\n"
KartRace_RRInfo = "さびさびレースウェイへようこそ！\nコースをよーく見て！ライバルにおてやわらかに！\n"
KartRace_AAInfo = "エアボーン・エーカースにようこそ!\nアップ・ダウンのはげしいコースに注意してね!\n"
KartRace_CCInfo = "シティーサーキットへようこそ！\nダウンタウンを通りぬけるときには、ほこうしゃに気をつけて！\n"
KartRace_BBInfo = "ブリザード・ブルバードにようこそ!\nスピード出しすぎ注意!道路がこおってるかも!?\n"
KartRace_GeneralInfo = "方向キーでカートをコントロールしよう！コース上でひろったギャグはコントロールキーで投げられるよ！"

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
    RaceGlobals.Daily : 'ほんじつの',
    RaceGlobals.Weekly : 'こんしゅうの',
    RaceGlobals.AllTime : 'れきだいの',
    }
    
KartRace_FirstSuffix = '位'
KartRace_SecondSuffix = '位'
KartRace_ThirdSuffix = '位'
KartRace_FourthSuffix = '位'
KartRace_WrongWay = '逆方向!'
KartRace_LapText = "ラップ %s"
KartRace_FinalLapText = "ファイナルラップ！"
KartRace_Exit = "レースしゅうりょう"
KartRace_NextRace = "次のレース" 
KartRace_Leave = "レースをやめる"
KartRace_Qualified = "よせんつうか！"
KartRace_Record = "しんきろく！"
KartRace_RecordString = '%sしんきろく！\n%sから\nチケット%s枚のボーナス！'
KartRace_Tickets = "チケット"
KartRace_Exclamations = "!"
KartRace_Deposit = "デポジット"
KartRace_Winnings = "しょうり"
KartRace_Bonus = "ボーナス"
KartRace_RaceTotal = "レーストータル"
KartRace_CircuitTotal = "サーキットトータル"
KartRace_Trophies = "トロフィー"
KartRace_Zero = "0"
KartRace_Colon = ":"
KartRace_TicketPhrase = "%s " + KartRace_Tickets
KartRace_DepositPhrase = KartRace_Deposit + KartRace_Colon + "\n"
KartRace_QualifyPhrase = "よせんつうか:\n"
KartRace_RaceTimeout = "タイムアップ！キミのチケットはもどったよ。がんばって！"
KartRace_RaceTimeoutNoRefund = "じかんぎれです。グランプリはもう始まってしまったからチケットはもどらないよ。次は頑張ってね！"
KartRace_RacerTooSlow = "ざんねん!じかんぎれです。デポジットはかえってこないけど、あきらめずにがんばってね!"
KartRace_PhotoFinish = "フォト・フィニッシュ！"
KartRace_CircuitPoints = 'サーキットポイント'

CircuitRaceStart = "グーフィー・サーキットでトゥーンタウン・グランプリが始まるよ！3つのレースにさんかして、一番ポイントをゲットしたらチャンピオンに!!"
CircuitRaceOngoing = "トゥーンタウン・グランプリをかいさい中だよ！"
CircuitRaceEnd = "本日のトゥーンタウン・グランプリは終了しました。また来週月曜日に！"

# Trick-or-Treat holiday
TrickOrTreatMsg = 'キミはすでにこのトリートを\nみつけているよ！'

#temp lawbot boss dialog text
LawbotBossTempIntro0 = "ふーむ。今日のサイバンリストは…"
LawbotBossTempIntro1 = "ほー。トゥーンがサイバンに来ているのか！"
LawbotBossTempIntro2 = "ケンサツ側は強いぞ。"
LawbotBossTempIntro3 = "そしてこちらがベンゴニン。"
LawbotBossTempIntro4 = "ちょっと待てよ…おまえらもトゥーンじゃないか！"
LawbotBossTempJury1 = "バイシンインの選定を始めます。"
LawbotBossHowToGetEvidence = "ショウコを手に入れるにはショウゲンダイに触れてください。"
LawbotBossTrialChat1 = "これからサイバンを始めます。"
LawbotBossHowToThrowPies = "Insertキーを押すと、ベンゴシや「はかり」に向けてショウコを投げることができるよ！"
LawbotBossNeedMoreEvidence = "もっとショウコが必要だよ！"
LawbotBossDefenseWins1 = "ありえない！ヒコクニンが勝つなんて！"
LawbotBossDefenseWins2 = "いや。このハンケツは間違っている！もう一度、新しいサイバンを開こう。"
LawbotBossDefenseWins3 = "はぁ～っ。疲れたので部屋で休むとするか。"
LawbotBossProsecutionWins = "ケンサツ側の勝ちとします。"
LawbotBossReward = "格上げとコグをショウカンできるようになったぞ。"
LawbotBossLeaveCannon = "キャノンから去る"
LawbotBossPassExam = "ほう、シホウシケンを通ったのか。"
LawbotBossTaunts = [
    "%s、ホウテイブジョクザイにあたりますぞ！",
    "イギをみとめます！",
    "今の内容を記録から消すように。",
    "訴えをキャッカします。あなたに悲しみをセンコクします！",
    "ホウテイのルールを守るように！",
    ]
LawbotBossAreaAttackTaunt = "ホウテイをブジョクするつもりか！"

WitnessToonName = "ﾊﾞﾝﾋﾟｰ ﾊﾞﾝﾌﾞﾙﾍﾞｱ"
WitnessToonPrepareBattleTwo = "な、なんと。コグのバイシンインしかいないじゃないか！\a急いで、キャノンを使ってトゥーンのバイシンインを送り込もう！\a「はかり」を合わせるのに%d人、必要だよ。"
WitnessToonNoJuror = "がーん。トゥーンのバイシンインが一人もいない！これではサイバンが大変になるぞ。"
WitnessToonOneJuror = "よかった！トゥーンのバイシンインが一人いるね。"
WitnessToonSomeJurors = "いーねー！トゥーンのバイシンインが%d人いるね。"
WitnessToonAllJurors = "すごいね！全員、トゥーンのバイシンインだね。"
WitnessToonPrepareBattleThree = "急いで、ショウゲンダイを触ってショウコをゲットしてね。\aベンゴシや「はかり」に向けてショウコを投げるにはInsertキーを押してね！"
WitnessToonCongratulations = "やったね！ すばらしいベンゴだったね。\aサイバンチョーが残していった書類を受け取って！\aこれがあれば、トゥーンガイドのコグのページでコグをショウカンできるぞ。"

WitnessToonLastPromotion = "\aワオ！コグスーツのレベルが%sになったよ。\aこれ以上は「格上げ」できないんだ。\aでも是非、レジスタンスのためにこれからもがんばってください！"
WitnessToonHPBoost = "\aキミはレジスタンスのために本当に一杯がんばってくれているね。\aトゥーン評議会がキミのゲラゲラポイントをアップさせるよ。おめでとう！"
WitnessToonMaxed = "\aキミはレベル%sのコグのスーツを着ているね。とてもいいよ！\aまた、トゥーンを助けるために戻ってきてくれたことに、トゥーン評議会にかわって、お礼します！"
WitnessToonBonus = "ワンダフル！全てのベンゴシがキゼツしたよ。キミのショウコの重さが%s倍になるぞ！（%s秒間）"

WitnessToonJuryWeightBonusSingular = {
  6: 'これは大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
  7: 'これはとっても大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
  8: 'これは今までにない大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
}

WitnessToonJuryWeightBonusPlural = {
  6: 'これは大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
  7: 'これはとっても大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
  8: 'これは今までにない大変な事件だ。%d人のバイシンインがいるから、キミのショウコは「%dボーナスウエイト」分の重みがあるね。',
}

# Cog Summons stuff
IssueSummons = "ショウカン"
SummonDlgTitle = "ショウカンジョーを出す"
SummonDlgButton1 = "コグをショウカン"
SummonDlgButton2 = "コグビルをショウカン"
SummonDlgButton3 = "コグの侵略をショウカン"
SummonDlgSingleConf = "%sをショウカンしますか？"
SummonDlgBuildingConf = "トゥーンビルの近くで%sをショウカンしますか？"
SummonDlgInvasionConf = "%sの侵略をショウカンしますか？"
SummonDlgNumLeft = "あと%s、残ってます"
SummonDlgDelivering = "ショウカン中…"
SummonDlgSingleSuccess = "コグのショウカンに成功しました。"
SummonDlgSingleBadLoc = "ごめんね。ここではコグは呼べません。別の場所を試してね。"
SummonDlgBldgSuccess = "コグのショウカンに成功しました。 %sが%sを乗っ取ります。"
SummonDlgBldgSuccess2 = "コグのショウカンに成功しました。店主もちょっとだけコグに乗っ取ることをＯＫしました！"
SummonDlgBldgBadLoc = "ごめんね！コグが乗っ取れるトゥーンビルが近くにありません。"
SummonDlgInvasionSuccess = "コグのショウカンに成功しました。コグの侵略がはじまった！"
SummonDlgInvasionBusy = "%sが見つかりません。コグの侵略が終わったら、もう一度試してね。"
SummonDlgInvasionFail = "ごめんね。コグの侵略が失敗しました。"
SummonDlgShopkeeper = "店主 "

# Polar Place cheesy effect chat phrases
PolarPlaceEffect1 = NPCToonNames[3306] + ": ポーラープレイスへようこそ！"
PolarPlaceEffect2 = NPCToonNames[3306] + ": ちょっとこれを着てサイズを見てくれる？"
PolarPlaceEffect3 = NPCToonNames[3306] + ": このかっこうは " + lTheBrrrgh + "でしか、着れないけどねー"

# LaserGrid game Labels
LaserGameMine = "ガイコツを探せ！"
LaserGameRoll = "マッチゲーム！"
LaserGameAvoid = "ガイコツを避けてボタンへ！"
LaserGameDrag = "同じ色を３つ並べよう！"
LaserGameDefault = "知らないゲーム"

# Pinball text
#PinballHiScore = "ﾊｲｽｺｱ： %d %s\n"
#PinballYourBestScore = "ﾍﾞｽﾄｽｺｱ： %d\n"
#PinballScore = "ｽｺｱ： %d x %d：%d" 
PinballHiScore = "ﾊｲｽｺｱ： %s\n"
PinballHiScoreAbbrev = "…"
PinballYourBestScore = "ﾍﾞｽﾄｽｺｱ： \n"
PinballScore = "ｽｺｱ： %d x %d = "
PinballScoreHolder = "%s\n"


# Gardening text
GagTreeFeather = "ちょいギャグの木"
GagTreeJugglingBalls = "ジャグリングボール"
StatuaryFountain = "噴水"
StatuaryToonStatue = "トゥーンの像"
StatuaryDonald = "ドナルドの像"
StatuaryMinnie = "ミニーの像"
StatuaryMickey1 = "ミッキーの像１"
StatuaryMickey2 = "ミッキーの像２"
StatuaryToon = "トゥーンの像"
StatuaryToonWave = "手をふる像"
StatuaryToonVictory = "勝利の像"
StatuaryToonCrossedArms = '権威の像'
StatuaryToonThinking = '喜びの像'
StatuaryMeltingSnowman = 'とける雪だるま像'
StatuaryGardenAccelerator = "ﾖｸｿﾀﾞｰﾂ"
#see GardenGlobals.py for corresponding FlowerColors
FlowerColorStrings = ['ﾚｯﾄﾞ','ｵﾚﾝｼﾞ','ﾊﾞｲｵﾚｯﾄ','ﾌﾞﾙｰ','ﾋﾟﾝｸ','ｲｴﾛｰ','ﾎﾜｲﾄ','ｸﾞﾘｰﾝ']
#see GardenGlobals.py for PlantAttributes, keys must match
FlowerSpeciesNames = {
    49: 'ﾃﾞｲｼﾞｰ',
    50: 'ﾁｭｰﾘｯﾌﾟ',
    51: 'ｶｰﾈｰｼｮﾝ',
    52: 'ﾘﾘｰ',
    53: 'ﾀﾞﾌｫﾃﾞｨﾙ',
    54: 'ﾊﾟﾝｼﾞｰ',
    55: 'ﾍﾟﾁｭﾆｱ',
    56: 'ﾛｰｽﾞ',    
    }
#see GardenGlobals.py for PlantAttributes, keys must match, varieties must match
FlowerFunnyNames = {
    49: ('ｽｸｰﾙﾃﾞｲｼﾞｰ',
         'ﾚｲｼﾞｰﾃﾞｲｼﾞｰ',
         'ｻﾏｰﾃﾞｲｼﾞｰ',
         'ﾘﾌﾚｯｼｭﾃﾞｲｼﾞｰ',
         'ｳｰﾋﾟｰﾃﾞｲｼﾞｰ',
         'ｱｯﾌﾟｼﾞｰﾃﾞｲｼﾞｰ',
         'ｸﾚｲｼﾞｰﾃﾞｲｼﾞｰ',
         'ﾍｲｼﾞｰﾃﾞｲｼﾞｰ',
         ),
    50:  ('ﾜﾝﾘｯﾌﾟ',
          'ﾂｰﾘｯﾌﾟ',
          'ｽﾘｰﾘｯﾌﾟ',
          ),
    51:  ('ﾜｯﾄｲﾝｶｰﾈｰｼｮﾝ',
          'ｲﾝｽﾀﾝﾄｶｰﾈｰｼｮﾝ',
          'ﾊｲﾌﾞﾘｯﾄﾞｶｰﾈｰｼｮﾝ',
          'ｻｲﾄﾞｶｰﾈｰｼｮﾝ',
          'ﾓﾃﾞﾙｶｰﾈｰｼｮﾝ',
          ),
    52: ('ﾘﾘｰｵﾌﾞｼﾞｱﾘｰ',
         'ﾘﾘｰﾊﾟｯﾄﾞ',
         'ﾀｲｶﾞｰﾘﾘｰ',
         'ﾘﾊﾞｰﾄﾞﾘﾘｰ',
         'ﾁﾘｰﾘﾘｰ',
         'ｼﾘｰﾘﾘｰ',
         'ﾀﾌﾞﾘﾘｰ',
         'ﾃﾞｨﾘｰﾘﾘｰ',
         ),
    53: ('ﾗﾌｫﾃﾞｨﾙ',
         'ﾀﾞﾌｨｰﾃﾞｨﾙ',
         'ｼﾞﾗﾌｫﾃﾞｨﾙ',
         'ﾀｲﾑｱﾝﾄﾞｱﾊｰﾌｫﾃﾞｨﾙ',
         ),
    54: ('ﾀﾞﾝﾃﾞｨｰﾊﾞﾝｼﾞｰ',
         'ﾁﾝﾊﾟﾝｼﾞｰ',
         'ﾎﾟｯﾂｪﾝﾊﾟﾝｼﾞｰ',
         'ﾏﾙﾁﾊﾟﾝｼﾞｰ',
         'ｽﾏｰﾃｨｰﾊﾟﾝｼﾞｰ'
         ),
    55: ('ｶｰﾍﾟﾁｭﾆｱ',
         'ﾌﾟﾗﾄｰﾆｱ',
         ),
    56: ("ｻﾏｰｽﾞﾗｽﾄﾛｰｽﾞ",
         'ｺｰﾝﾛｰｽﾞ',
         'ﾃｨﾝﾄﾛｰｽﾞ',
         'ｽﾃｨﾝｷﾝｸﾞﾛｰｽﾞ',
         'ｲｽﾃｨﾗﾛｰｽﾞ',         
         ),
    }
FlowerVarietyNameFormat = "%s %s"
FlowerUnknown = "????"
ShovelNameDict = {
    0 : "(スズ)",
    1 : "(銅)",
    2 : "(銀)",
    3 : "(金)",
    }
WateringCanNameDict = {
    0 : "(小)",
    1 : "(中)",
    2 : "(大)",
    3 : "(特大)",
    }
GardeningPlant = "植物"
GardeningWater = "水"
GardeningRemove = "やめる"
GardeningPick = "しゅう\nかく"
GardeningFull = "いっぱい"
GardeningSkill = "スキル"
GardeningWaterSkill = "水スキル"
GardeningShovelSkill = "ショベルスキル"
GardeningNoSkill = "スキルアップなし"
GardeningPlantFlower = "花を\nうえる"
GardeningPlantTree = "木を\nうえる"
GardeningPlantItem = "アイテムを\nうえる"
PlantingGuiOk = "うえる"
PlantingGuiCancel = "ｷｬﾝｾﾙ"
PlantingGuiReset = "リセット"
GardeningChooseBeans = "うえたいジェリービーンを選んでね。"
GardeningChooseBeansItem  = "うえたいジェリービーンか\nアイテムを選んでね。"
GardeningChooseToonStatue = "キミのトゥーンで像を作れるよ。どのトゥーンで作る？"
GardenShovelLevelUp = "おめでとう！%(shovel)sをゲット！ %(oldbeans)dのビーンフラワーをマスターしました。次に進むには%(newbeans)dのビーンフラワーを取ろう。"
GardenShovelSkillLevelUp = "おめでとう！%(oldbeans)dのビーンフラワーをマスターしました。次に進むには%(newbeans)dのビーンフラワーを取ろう。"
GardenShovelSkillMaxed = "すごいねー！キミのショベルスキルが最大になったよ！"

GardenWateringCanLevelUp = "おめでとう！あたらしいジョウロをゲットしたよ！"
GardenMiniGameWon = "やったね！ちゃんと水をあげられたね！"
ShovelTin = "ショベル(スズ)"
ShovelSteel = "ショベル(銅)"
ShovelSilver = "ショベル(銀)"
ShovelGold = "ショベル(金)"
WateringCanSmall = "ジョウロ(小)"
WateringCanMedium = "ジョウロ(中)"
WateringCanLarge = "ジョウロ(大)"
WateringCanHuge = "ジョウロ(特大)"
#make sure it matches GardenGlobals.BeanColorLetters
BeanColorWords = ('ﾚｯﾄﾞ', 'ｸﾞﾘｰﾝ', 'ｵﾚﾝｼﾞ','ﾊﾞｲｵﾚｯﾄ','ﾌﾞﾙｰ','ﾋﾟﾝｸ','ｲｴﾛｰ',
                  'ｼｱﾝ','ｼﾙﾊﾞｰ')
PlantItWith = "%sを与える"
MakeSureWatered = " まずきちんとすべての植木に水を与えましょう。"
UseFromSpecialsTab = "ガーデンページのスペシャルのタブから使いましょう。"
UseSpecial = "スペシャルを使う"
UseSpecialBadLocation = 'キミのガーデンでしか使えません。'
UseSpecialSuccess = 'うまくいったね！植木が育ちました。'
ConfirmWiltedFlower = "%(plant)sがしぼんでいます。バスケットにも残らないし、スキルも上がりません。"
ConfirmUnbloomingFlower = "まだ%(plant)sは咲いてませんが、つみとりますか？バスケットにも残らないしスキルも上がりません。"
ConfirmNoSkillupFlower = "%(plant)sをつみとって、キミの花のバスケットに入れますか？残念だけどスキルは上がらないよ。"
ConfirmSkillupFlower = "%(plant)sをしゅうかくして、キミの花のバスケットに入れますか？またスキルが上がるよ。"
ConfirmMaxedSkillFlower = "%(plant)sをしゅうかくして、キミの花のバスケットに入れますか？もうスキルが最大だからスキルは上がらないよ。"
ConfirmBasketFull = "キミのバスケットは一杯だよ。花を売るにはテオシグルマに行こう。"
ConfirmRemoveTree = "%(tree)sを抜いてもいいかな？"
ConfirmWontBeAbleToHarvest = "もしこの木を抜くと、高いレベルの木からギャグを育てることができなくなるよ。"
ConfirmRemoveStatuary = "本当に%(item)sがなくなるけど、いいかな？?"
ResultPlantedSomething  = "おめでとう！%sを植えました。"
ResultPlantedSomethingAn  = "おめでとう！%sを植えました。"
ResultPlantedNothing = "うまくいかなかったね。違うジェリービーンの組み合わせを試してね。"

GardenGagTree = "ギャグの木"
GardenUberGag = "レベル７ギャグ"

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
            retval = "%d %s ジェリービーン" % (len(beanTuple),
                                           BeanColorWords[beanTuple[0]])
        else:
            retval = "a %s ジェリービーン" % BeanColorWords[beanTuple[0]]
    else:
        retval += 'a'
        maxBeans = len(beanTuple)
        for index in range(maxBeans):
            if index == maxBeans - 1:
                retval += " そして %s ジェリービーン" % BeanColorWords[beanTuple[index]]
            elif index == 0:
                retval += " %s" % BeanColorWords[beanTuple[index]]
            else:
                retval += ", %s" % BeanColorWords[beanTuple[index]]

    return retval
    
GardenTextMagicBeans = "マジックビーン"
GardenTextMagicBeansB = "ふつうのビーン"
GardenSpecialDiscription = "この文章はどのようにガーデンスペシャルを使うかを説明するものです。"
GardenSpecialDiscriptionB = "この文章はどのようにガーデンスペシャルを使うかを説明するものです。" 
GardenTrophyAwarded = "ワオ！花、%s輪（%s輪のうち）をゲット！トロフィーとゲラゲラポイントアップ！"
GardenTrophyNameDict = {
    0 : "ﾃｵｼｸﾞﾙﾏ",
    1 : "ｼｮﾍﾞﾙ",
    2 : "ﾌﾗﾜｰ",
    3 : "ｼﾞｮｳﾛ",
    4 : "ｻﾒ",
    5 : "ﾒｶｼﾞｷ",
    6 : "ｼｬﾁ",
    }
SkillTooLow = "スキルが\n足りません"
NoGarden = "ガーデンが\nありません"

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
TravelGameTitle = "『ターン・テーブル』"
TravelGameInstructions = "キミのヒミツのゴールにたどり着くようにとうひょう数を決めよう。決めたら“とうひょう”ボタンをクリック。うまくゆけばボーナスをゲット！他のゲームも頑張るととうひょうできる数が増えるよ。"
TravelGameRemainingVotes = "とうひょうできる数:"
TravelGameUse = "つかう"
TravelGameVotesWithPeriod = "とうひょう"
TravelGameVotesToGo = "のこり"
TravelGameVoteToGo = "のこり"
TravelGameUp = "もっと！"
TravelGameDown = "へらす。"
TravelGameVoteWithExclamation = "とうひょう!"
TravelGameWaitingChoices = "他のプレイヤーがとうひょうするのを待っています..."
# cross the bridge later when the first choice is different for each node,
# e.g. NorthWest, NorthEast, etc.
TravelGameDirections = ['上へ', '下へ']
TravelGameTotals = 'ごうけい '
TravelGameReasonVotesPlural = 'とうひょう数%(numVotes)dで、トロリーは%(dir)s！'
TravelGameReasonVotesSingular = 'とうひょう数%(numVotes)dで、トロリーは%(dir)s！'
TravelGameReasonPlace = '%(name)sとどうてん！トロリーは%(dir)sすすむよ！'
TravelGameReasonRandom = 'トロリーは%(dir)sかってにすすむよ。'
TravelGameOneToonVote =   "%(name)sが%(dir)s\nすすめるように%(numVotes)sとうひょうしました。"
TravelGameBonusBeans = "%(numBeans)dボーナスジェリービーン！"
TravelGamePlaying = 'つぎのトロリーゲームは%(game)sだよ。'
TravelGameGotBonus = '%(name)sが%(numBeans)sボーナスジェリービーンをゲット！'
TravelGameNoOneGotBonus = "だれもヒミツのゴールにたどりつけなかったよ。みんなジェリービーン１つずつゲット。"
TravelGameConvertingVotesToBeans = "とうひょうをジェリービーンにこうかんする"
TravelGameGoingBackToShop ="プレイヤーが１人しかいないからグーフィーのギャグショップへ…。"

PairingGameTitle = "トゥーンしんけいすいじゃく"
PairingGameInstructions = "Deleteキーでカードをオープン。２枚そろえば得点。ボーナスマークは追加ポイントに！なるべく少ない回数でクリアしよう！"
PairingGameInstructionsMulti = "Deleteキーでカードをオープン。Controlキーで他のプレイヤーにじゅんばんを知らせよう。２枚そろえば得点。ボーナスマークは追加ポイントに！なるべく少ない回数でクリアしよう"
PairingGamePerfect = 'パーフェクト!!'
PairingGameFlips = 'オープン回数:'
PairingGamePoints = 'ポイント:'

TrolleyHolidayStart = "『ターン・テーブル』が始まるよ!２人いじょうでトロリーに乗ってね。"
TrolleyHolidayOngoing = "ようこそ!『ターン・テーブル』をかいさいちゅうだよ。"
TrolleyHolidayEnd = "『ターン・テーブル』をしゅうりょうします！また来週ね！！"

TrolleyWeekendStart = "『ターン・テーブル』ウィークが始まるよ!２人いじょうでトロリーに乗ってね。"
TrolleyWeekendEnd = "『ターン・テーブル』ウィークをしゅうりょうします。"

VineGameTitle = "『ジャングル・ジャンプ』"
VineGameInstructions = "せいげん時間までにゴールを目指そう！矢印キーの上(↑)と下(↓)で高さをちょうせつ。右(→)と左(←)で向きを変えてジャンプ！低いところからだとスピードアップ。バナナを集めながらコウモリとクモのこうげきをかわそう。"

# Make sure the golf text matches up with GolfGlobals.py
GolfCourseNames = {
    0: "ウォーク・イン・パー",
    1: "ホール・サム・ファン",
    2: "ザ・ホール・カブードル"
    }

GolfHoleNames = {
    0: 'ホール・イン・ウィン',
    1: 'ノー・パット・アバウト・イット',
    2: 'ダウン・ザ・ハッチ',
    3: 'シーイング・グリーン',
    4: 'ホット・リンクス',
    5: 'ピーナツ・パター',
    6: 'スィング・ア・ロング',
    7: 'アフタヌーン・ティー',
    8: 'ホール・イン・ファン',
    9: 'ロックンロール・イン',
    10: 'ボギー・ナイツ',
    11: 'ティー・オフ・タイム',
    12: 'ホーリー・マカレル!',
    13: 'ワン・リトル・バーディー',
    14: 'ザ・ドライブ・イン',
    15: 'スィング・タイム',
    16: 'ホール・オン・ザ・レンジ',
    17: 'セカンド・ウィンド',
    18: 'ホール・イン・ウィン-2',
    19: 'ノー・パット・アバウト・イット-2',
    20: 'ダウン・ザ・ハッチ-2',
    21: 'シーイング・グリーン-2',
    22: 'ホット・リンクス-2',
    23: 'ピーナツ・パター-2',
    24: 'スィング・ア・ロング-2',
    25: 'アフタヌーン・ティー-2',
    26: 'ホール・イン・ファン-2',
    27: 'ロックンロール・イン-2',
    28: 'ボギー・ナイツ-2',
    29: 'ティー・オフ・タイム-2',
    30: 'ホーリー・マカレル!-2',
    31: 'ワン・リトル・バーディー-2',
    32: 'ザ・ドライブ・イン-2',
    33: 'スィング・タイム-2',
    34: 'ホール・オン・ザ・レンジ-2',
    35: 'セカンド・ウィンド-2',
    }

GolfHoleInOne = "ホール・イン・ワン"
GolfCondor = "コンドル" # four Under Par
GolfAlbatross = "アルバトロス" # three under par
GolfEagle = "イーグル" # two under par
GolfBirdie = "バーディー" # one under par
GolfPar = "パー"
GolfBogey = "ボギー" # one over par
GolfDoubleBogey = "ダブル・ボギー" # two over par
GolfTripleBogey = "トリプル・ボギー" # three over par

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

CoursesCompleted = "コース、1人で完了"
CoursesUnderPar = "コース、アンダー・パー"
HoleInOneShots = "ホール・イン・ワン"
EagleOrBetterShots = "イーグル以上"
BirdieOrBetterShots = "バーディー以上"
ParOrBetterShots = "パー以上"
MultiPlayerCoursesCompleted = "コース パーティーで完了"
TwoPlayerWins = "２プレイヤーで勝利"
ThreePlayerWins = "３プレイヤーで勝利"
FourPlayerWins = "４プレイヤーで勝利"
CourseZeroWins = GolfCourseNames[0] + " Wins"
CourseOneWins = GolfCourseNames[1] + " Wins"
CourseTwoWins = GolfCourseNames[2] + " Wins"

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
    str(GolfGlobals.TrophiesPerCup) + "個のトロフィー",
    str(GolfGlobals.TrophiesPerCup * 2) + "個のトロフィー",
    str(GolfGlobals.TrophiesPerCup * 3) + "個のトロフィー",
]

GolfAvReceivesHoleBest = "%(name)sが%(hole)sでホールレコードをこうしん!"
GolfAvReceivesCourseBest = "%(name)sが%(course)sのコースレコードをこうしん!"
GolfAvReceivesCup = "%(name)sが%(cup)s杯をかくとく！賞品はｹﾞﾗｹﾞﾗﾌﾞｰｽﾄだ！！"
GolfAvReceivesTrophy = "%(name)sが%(award)sのトロフィーをかくとく！"
GolfRanking = "ランキング: \n"
GolfPowerBarText = "%(power)s%%"
GolfChooseTeeInstructions = "左・右の矢印キーでティーの位置をへんこう。\nCtrlキーで決定。"
GolfWarningMustSwing = "注意: 次のスィングではちゃんとCtrlキーを使ってね。"
GolfAimInstructions = "左・右の矢印キーで方向を決めて、\nCtrlキーを長押ししてスィングの強さをコントロールしよう。"
GolferExited = "%sがゴルフコースから出ました。"
GolfPowerReminder = "ボールをもっと遠くに打つには、\nCtrlキーをもっと長く押し続けよう。"


# GolfScoreBoard.py
GolfPar = "パー"
GolfHole = "ホール"
GolfTotal = "トータル"
GolfExitCourse = "ホールアウト"
GolfUnknownPlayer = ""

# GolfPage.py
GolfPageTitle = "ゴルフ"
GolfPageTitleCustomize = "ゴルフのカスタマイズ"
GolfPageTitleRecords = "自己ベスト"
GolfPageTitleTrophy = "ゴルフ・トロフィー"
GolfPageCustomizeTab = "カスタマイズ"
GolfPageRecordsTab = "レコード"
GolfPageTrophyTab = "トロフィー"
GolfPageTickets = "チケット: "
GolfPageConfirmDelete = "アクセサリーを削除する？"
GolfTrophyTextDisplay = "トロフィー%(number)s個 : %(desc)s"
GolfCupTextDisplay = "カップ%(number)s個 : %(desc)s"
GolfCurrentHistory = "現在%(historyDesc)s : %(num)s"
GolfTieBreakWinner = "%(name)sがランダムでタイブレークに勝利！"
GolfSeconds = " -  %(time).2f秒"
GolfTimeTieBreakWinner = "%(name)sが最短時間でタイブレークに勝利!!"



RoamingTrialerWeekendStart = "ツアー・トゥーンタウンが始まるよ！フリー・プランの入場制限が解除されるよ！"
RoamingTrialerWeekendOngoing = "ツアー・トゥーンタウンへようこそ！フリー・プランの入場制限が解除されるよ！"
RoamingTrialerWeekendEnd = "ツアー・トゥーンタウンは終了しました。"
# change double if ToontownBattleGlobals.getMoreXpHolidayMultiplier() changes
MoreXpHolidayStart = "Good news! Exclusive Test Toon double gag experience time has started."
MoreXpHolidayOngoing = "Welcome! Exclusive Test Toon double gag experience time is currently ongoing."
MoreXpHolidayEnd = "Exclusive Test Toon double gag experience time has ended. Thanks for helping us Test things!"

JellybeanDayHolidayStart = "今日はジェリービーン・デーだよ！パーティーでいつもの二倍のジェリービーンをもらおう！"
JellybeanDayHolidayEnd = "ジェリービーン・デーは終了しました。また次回に会おうね。"
PartyRewardDoubledJellybean = "ダブル・ジェリービーン!!"

GrandPrixWeekendHolidayStart = "グーフィーサーキットでグランプリウィークエンド開催中！ ダレでも３連戦参加で大量ポイントゲットのチャンス！"
GrandPrixWeekendHolidayEnd = "グランプリウィークエンドは終了しました。また次回に会おう！"

LogoutForced = "You have done something wrong\n and are being logged out automatically,\n additionally your account may be frozen.\n Try going on a walk outside, it is fun."

# DistributedCountryClub.py
CountryClubToonEnterElevator = "%s \nがゴルフカートにのったよ"
CountryClubBossConfrontedMsg = "%sがクラブのオーナーとバトルちゅうだよ!"

# DistributedElevatorFSM.py
ElevatorBlockedRoom = "さきにたおすあいてがいるみたいだよ。"

# DistributedMolefield.py
MolesLeft = "のこりのモグラ: %d"
MolesInstruction = "モール・ストンプ！\nあかいモグラのうえにとびのろう！"
MolesFinished = "モール・ストンプをクリア！"
MolesRestarted = "モール・ストンプにしっぱい！もういちど・・・"

# DistributedGolfGreenGame.py
BustACogInstruction = "コグボールをねらってね！"
BustACogExit = "いまはやめとく"
BustACogHowto = "あそびかた"
BustACogFailure = "じかんぎれ！"
BustACogSuccess = "だいせいこう！"

# bossbot golf green games
GolfGreenGameScoreString = "のこりのパズル: %s"
GolfGreenGamePlayerScore = "クリアのかず %s"
GolfGreenGameBonusGag = "ボーナス！%sかくとく"
GolfGreenGameGotHelp = "%s パズルをクリア!"

GolfGreenGameDirections = "マウスをつかってボールをねらってね！\n三つ同じ色をそろえるとボールが消せるよ。\nボードから全てのコグボールを消そう！"

# DistributedMaze.py
enterHedgeMaze = "さいしょにめいろをクリアして\nポイントをゲットしよう!"
toonFinishedHedgeMaze = "%s \n  が %s でゴール!"
hedgeMazePlaces = ["1ばん","2ばん","3ばん","4ばん"]
mazeLabel = "めいろでレース！"

# Boarding Group
BoardingPartyReadme = 'ボーディング・グループ?'
BoardingGroupHide = 'かくす'
BoardingGroupShow = 'ボーディング・グループを見る'
BoardingPartyInform = '他のトゥーンをクリックしてエレベータ・ボーディング・グループに招待しよう。\nここではボーディング・グループは%s以下で作れます。'
BoardingPartyTitle = 'ボーディング・グループ'
QuitBoardingPartyLeader = 'かいさんする'
QuitBoardingPartyNonLeader = 'やめる'
QuitBoardingPartyConfirm = '本当にこのボーディング・グループをやめる？'
BoardcodeMissing = 'あれれ、トラブルかな？後でもう一度ためしてね。'
BoardcodeMinLaffLeader = 'キミのゲラゲラメーターが%s以下なので、キミのグループは参加できません。'
BoardcodeMinLaffNonLeaderSingular = '%sのゲラゲラメーターが%s以下なので、このグループは参加できません。'
BoardcodeMinLaffNonLeaderPlural = '%sのゲラゲラメーターが%s以下なので、キミのグループは参加できません。'
BoardcodePromotionLeader = 'メリットが足りないからキミのグループは参加できません。'
BoardcodePromotionNonLeaderSingular = '%sはメリットが足りないのでキミのグループは参加できません。'
BoardcodePromotionNonLeaderPlural = '%sのメリットが足りないので、キミのグループは参加できません。'
BoardcodeSpace = 'キミのグループは大きすぎて参加できません。'
BoardcodeBattleLeader = 'バトル中はキミのグループは参加できません。'
BoardcodeBattleNonLeaderSingular = '%sがバトル中なので、キミのグループは参加できません。'
BoardcodeBattleNonLeaderPlural = '%sがバトル中なので、キミのグループは参加できません。'
BoardingInviteMinLaffInviter = 'このボーディング・グループに入るには、ゲラゲラメーターが%s必要です。'
BoardingInviteMinLaffInvitee = '%sがこのボーディング・グループに入るには、ゲラゲラメーターが%s必要です。'
BoardingInvitePromotionInviter = 'このボーディング・グループに入るには格上げが必要だよ。'
BoardingInvitePromotionInvitee = '%sがこのボーディング・グループに入るには格上げが必要だよ。'
BoardingInviteNotPaidInvitee = '%sはフルアクセス・メンバーではないのでキミのボーディング・グループには入れないよ。'
BoardingInviteeInDiffGroup = '%sはもう他のボーディング・グループのメンバーです。'
BoardingInviteeInKickOutList = '%sはキミのリーダーがさくじょしました。リーダーしか招待できません。'
BoardingInviteePendingIvite = '%sは別の招待を保留中です。後でまた試してね。'
BoardingInviteeInElevator = '%sは今忙しいみたい…。後でまた試してね。'
BoardingInviteGroupFull = 'キミのボーディング・グループはもういっぱいです。'
BoardingAlreadyInGroup = 'キミはもう他のボーディング・グループに入っているのでこの招待は受けられません。'
BoardingGroupAlreadyFull = 'このグループはもういっぱいなので、この招待は受けられません。'
BoardingKickOutConfirm = '本当に%sを削除してもいい？'
BoardingPendingInvite = '先に保留中の招待に\n返事をしようね。'
BoardingCannotLeaveZone = 'ボーディング・グループに参加しているから今はだめだよ。'
BoardingInviteeMessage = "%sがキミのボーディング・グループに入ってほしいって。"
BoardingInvitingMessage = "%sをキミのボーディング・グループにさそっています。"
BoardingInvitationRejected = "%sが今回はキミのグループへの参加をみおくりました。"
BoardingMessageKickedOut = "ボーディング・グループから削除されました。"
BoardingMessageInvited = "%sが%sをボーディング・グループに招待しました。"
BoardingMessageLeftGroup = "%sがボーディング・グループからはずれました。"
BoardingMessageGroupDissolved = "キミのボーディング・グループはリーダーによって解散しました。"
BoardingMessageGroupDisbandedGeneric = "キミのボーディング・グループは解散しました。"
BoardingMessageInvitationFailed = "%sがボーディング・グループに招待しようとしていました。"
BoardingMessageGroupFull = "%sが参加しようとしましたが、あなたのグループはもういっぱいでした。"
BoardingGo = '行く'
BoardingCancelGo = '中止は<行く>を\n再クリック'
And = '＋'
BoardingGoingTo = '行き先'
BoardingTimeWarning = 'エレベーターにのるまで '
BoardingMore = 'もっと'
BoardingGoShow = '%sに行くまで'
BoardingGoPreShow = '確認中...'

# DistributedBossbotBoss.py
BossbotBossName = "チーフ・ボスゼキュティブ"
BossbotRTWelcome = "ここでは別のへんそうパーツがひつようなんだ。"
BossbotRTRemoveSuit = "まずはコグ・スーツをぬいで..."
BossbotRTFightWaiter = "ここのウェイターたちとたたかおう！"
BossbotRTWearWaiter = "やったね! さぁ、ウェイターのようふくをきてみよう。"
BossbotBossPreTwo1 = "おい、まだか？ぐずぐずするな"
BossbotBossPreTwo2 = "楽しいえんかいのスタートだ。テキパキとたのむぞ!"
BossbotRTServeFood1 = "さぁ、コンベアーにおいた料理をどんどんはこんでくれ。"
BossbotRTServeFood2 = "３回つづけて同じコグにはこぶと、ばくはつするしかけなんだ。"
BossbotResistanceToonName = "グッドール・ジル・ギグルス"
BossbotPhase3Speech1 = "なんだ、どうなってるんだ！？"
BossbotPhase3Speech2 = "お、おまえたちは…あぁっ、トゥーンじゃないか！"
BossbotPhase3Speech3 = "つかまえろ！！"
BossbotPhase4Speech1 = "まったくだらしないやつらだ。ならば..."
BossbotPhase4Speech2 = "わたしがあいてになってやる！"
BossbotRTPhase4Speech1 = "いいぞ！こんどはテーブルの上の水でっぽうでボスゼキュティブをこうげきしよう。"
BossbotRTPhase4Speech2 = "それから、ゴルフボールを当てるとボスゼキュティブの動きがおそくなるよ。"
BossbotPitcherLeave = "やめる"
BossbotPitcherLeaving = "いどう中"
BossbotPitcherAdvice = "左右のキーで向きをかえられるよ。\nCtrlキーを押してパワーをためて、はなすとはっしゃ"
BossbotGolfSpotLeave = "やめる"
BossbotGolfSpotLeaving = "いどう中"
BossbotGolfSpotAdvice = "左右のキーで向きをかえられるよ。\nCtrlキーではっしゃ"
BossbotRewardSpeech1 = "なんてことを！おまえたち、わたしのカオをまるつぶれにしてくれたな！"
BossbotRewardSpeech2 = "ガルルルッ！！"
BossbotRTCongratulations = "すごいすごい!あのボスゼキュティブをついにたおしたぞ！\aさぁ、ボスゼキュティブが忘れていったカイコツウチだよ。\aこれでバトル中のコグをクビにできるんだ。"""
BossbotRTLastPromotion = "\aおぉ！キミのコグスーツはレベル%sになったよ！\aほんもののコグたちもそれ以上シュッセできないんだ。\aスーツのアップグレードはここまでだけど、レジスタンスを続けるとボーナスがもらえるんだ☆"
BossbotRTHPBoost = "\aキミの日ごろのかつやくには目をみはるものがある！\aトゥーンひょうぎ会はそのえいよをたたえ、キミにｹﾞﾗｹﾞﾗﾎﾟｲﾝﾄをあたえる事にした。おめでとう！！"
BossbotRTMaxed = "\aレベル%sのコグスーツを持っているんだね。キミに会えてこうえいだよ！\aトゥーンひょうぎ会にかわって、キミのトゥーン・レジスタンスへのこうけんにかんしゃするよ！"
GolfAreaAttackTaunt = "ファ～ッ!"
OvertimeAttackTaunts = [ "今のそしきではだめだ。",
                        "ダメなコグをリストラしたらまた相手をしてやる！"]

#ElevatorDestination Names
ElevatorBossBotBoss = "ボスゼキュティブ戦"
ElevatorBossBotCourse = ""
ElevatorBossBotCourse0 = "フロント・スリー"
ElevatorBossBotCourse1 = "ミドル・シックス"
ElevatorBossBotCourse2 = "バック・ナイン"
ElevatorCashBotBoss = "マネーマネー戦"
ElevatorCashBotMint0 = "コイン工場"
ElevatorCashBotMint1 = "ドル工場"
ElevatorCashBotMint2 = "ゴールド工場"
ElevatorSellBotBoss = "コグゼキュティブ戦"
ElevatorSellBotFactory0 = "正面入り口"
ElevatorSellBotFactory1 = "裏口"
ElevatorLawBotBoss = "チーフ・ジャスティス戦"
ElevatorLawBotCourse0 = "オフィスA"
ElevatorLawBotCourse1 = "オフィスB"
ElevatorLawBotCourse2 = "オフィスC"
ElevatorLawBotCourse3 = "オフィスD"

# CatalogNameTagItem.py
DaysToGo = "あと\n%s日"

# DistributedIceGame.py
IceGameTitle = "アイス・スライド"
IceGameInstructions = "第２ラウンドが終わるまでになるべく中心にたどり着こう。矢印キーで方向と強さを変えてね。Ctrlキーでトゥーンを発射！ドラム缶に当たるとボーナスポイント。でもTNTには当てちゃだめだよ！"
IceGameInstructionsNoTnt = "第２ラウンドが終わるまでになるべく中心にたどり着こう。矢印キーで方向と強さを変えてね。Ctrlキーでトゥーンを発射！ドラム缶に当たるとボーナスポイント。"
IceGameWaitingForPlayersToFinishMove = "他のプレイヤーを待っています..."
IceGameWaitingForAISync = "他のプレイヤーを待っています..."
IceGameInfo= "マッチ %(curMatch)d/%(numMatch)d, ラウンド %(curRound)d/%(numRound)d"
IceGameControlKeyWarning="Ctrlキーで発射だよ！"


#DistributedPicnicTable.py
PicnicTableJoinButton = "参加する"
PicnicTableObserveButton = "みるだけ"
PicnicTableCancelButton = "キャンセル"
PicnicTableTutorial = "遊び方"
PicnicTableMenuTutorial = "どのゲームの説明？"
PicnicTableMenuSelect = "どのゲームをプレイする？"

#DistributedChineseCheckers.py
ChineseCheckersGetUpButton = "席を立つ"
ChineseCheckersStartButton = "ゲーム開始！"
ChineseCheckersQuitButton = "ゲーム終了！"
ChineseCheckersIts = "It's "

ChineseCheckersYourTurn = "キミの番だよ"
ChineseCheckersGreenTurn = "緑の番だよ"
ChineseCheckersYellowTurn = "黄色の番だよ"
ChineseCheckersPurpleTurn = "紫の番だよ"
ChineseCheckersBlueTurn = "青の番だよ"
ChineseCheckersPinkTurn = "ピンクの番だよ"
ChineseCheckersRedTurn = "赤の番だよ"

ChineseCheckersColorG = "キミは緑だよ"
ChineseCheckersColorY = "キミは黄色だよ"
ChineseCheckersColorP = "キミは紫だよ"
ChineseCheckersColorB = "キミは青だよ"
ChineseCheckersColorPink = "キミはピンクだよ"
ChineseCheckersColorR = "キミは赤だよ"
ChineseCheckersColorO = "キミはみているだけだよ"

ChineseCheckersYouWon = "おめでとう！ダイヤモンドゲームに勝利！！"
ChineseCheckers = "ダイヤモンドゲーム"
ChineseCheckersGameOf = " が勝ったゲーム： "

#GameTutorials.py
ChineseTutorialTitle1 = "ゲームについて"
ChineseTutorialTitle2 = "遊び方"
ChineseTutorialPrev = "前のページ"
ChineseTutorialNext = "次のページ"
ChineseTutorialDone = "閉じる"
ChinesePage1 = "『ダイヤモンドゲーム』は、下の三角形にあるコマを他のプレイヤーより先に上の三角形に移動させるゲームだよ。先に移動し終わったプレイヤーが勝ちだよ！"
ChinesePage2 = "順番に自分の色のコマを移動します。コマはとなりあった穴か、他のコマを一つだけとびこえて空いている穴に移動(ホップ)してもＯＫ。コマの移動先でもホップの条件が続いてそろう時は、遠くまで移動できるチェーンホップが有効だよ！"

CheckersPage1 = "『チェッカー』は、相手のコマの動きを止めると勝ちなんだ。そのためには、相手のコマを全部とってしまうか、相手のコマが進んでいいところを先にうばってしまう方法があるよ。"
CheckersPage2 = "順番に自分の色のコマを動かします。各コマは、マスが空いている限りななめに一コマ、または前に一コマずつ進めます。キングも同じ動きと、さらに後ろに戻る事もできるんだ。"
CheckersPage3 = "ななめに相手のコマをとびこえてその先の空いているマスに進むと、とびこえた相手のコマをとることができるよ(ジャンプ)。もしも自分の番の時に相手のコマがとれる(ジャンプできる)時は、必ず一つはとらなければならないから注意してね。連続のジャンプは同じコマでだけできるからがんばってみよう。"
CheckersPage4 = "全てのコマは、ボードのさいごの列についたらキングにかわるんだ！キングになったばかりのコマは、次の順番まではジャンプできないよ。それから、キングは全ての方向に動けるし、ジャンプの途中で方向をかえる事もできるからためしてね！"



#DistributedCheckers.py
CheckersGetUpButton = "席を立つ"
CheckersStartButton = "ゲーム開始！"
CheckersQuitButton = "ゲーム終了！"
CheckersIts = "次は"
CheckersYourTurn = "キミの番だよ"
CheckersWhiteTurn = "シロの番だよ"
CheckersBlackTurn = "クロの番だよ"
CheckersColorWhite = "キミはシロだよ"
CheckersColorBlack = "キミはクロだよ"
CheckersObserver = "けんがくちゅう…"
RegularCheckers = "チェッカー"
RegularCheckersGameOf = " が勝ったゲーム： "
RegularCheckersYouWon = "おめでとう！チェッカーに勝利!"

MailNotifyNewItems = "メールがとどいたよ！"
MailNewMailButton = "メール"
MailSimpleMail = "ノート"
MailFromTag = "ノート: %sから"

# MailboxScreen.py
InviteInvitation = "しょうたい状"
InviteAcceptInvalidError = "このしょうたい状はもう使えません。"
InviteAcceptPartyInvalid = "このパーティーはキャンセルされました。"
InviteAcceptAllOk = "あなたの返事はしゅさい者にとどきました。"
InviteRejectAllOk = "しゅさい者にキミの欠席の知らせがとどきました。"


# Note Months is 1 based, to correspond to datetime
Months = {
 1: "1月",
 2: "2月",
 3: "3月",
 4: "4月",
 5: "5月",
 6: "6月",
 7: "7月",
 8: "8月",
 9: "9月",
10: "10月",
11: "11月",
12: "12月"
}

# Note 0 for Monday to match datetime
DayNames = ("月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日")
DayNamesAbbrev = ("月", "火", "水", "木", "金", "土", "日")

# numbers must match holiday ids in ToontownGlobals
HolidayNamesInCalendar = {
    1: ("夏の花火大会", "プレイグラウンドで1時間おきに開かれる花火大会をお友達といっしょに楽しもう！ "),
    2: ("新年の花火", "明けましておめでとう！プレイグラウンドで1時間おきにあがる花火でいっしょにお祝いしよう！"),
    3: ("ガッツキーのしんりゃく", "ハッピー・ハロウィーン! 吸血鬼顔のガッツキーのしんりゃくをくい止めろ! "),
    4: ("ウィンターデコレーション", "ムードたっぷりのストリートや木々のデコレーションをお楽しみください♪"),
    5: ("ガイコグのしんりゃく", "キミ達の力でガイコグのしんりゃくをくい止めよう！ "),
    6: ("ビッグスマイルの侵略", "ビッグスマイルの侵略をくいとめろ！"),
    7: ("フィッシュビンゴ", "今日はフィッシュビンゴの日！なかまたちと“ビンゴ！”をめざそう。 "),
    8: ("新種トゥーン投票", "キミはどんな新種トゥーンがいいと思う？ヤギ？ライオン？好きな新種に投票しよう！ "),
    9: ("くろねこトゥーン！", "ハッピー・ハロウィーン！キミもくろねこトゥーン！を作ってみよう。10/31限定だよ！"),
   13: ("トリック・オア・トリート", "ハッピー・ハロウィーン！ハロウィーンのパンプキンヘッドをもらおう！ "),
   14: ("グランプリ", "グーフィーサーキットでグランプリ開催中！3連勝してチャンピオンを目指そう。"),
   16: ("グランプリ・ウィークエンド", "フリー・プラン会員もレースに参加できるよ！ "),
   17: ("トロリー・トラック", "今日はトロリー・トラックの日。二人以上でトロリーに乗ってトロリー・トラックを楽しもう！ "),
   19: ("満タン・サタデー", "土曜日は一日中フィッシュビンゴにグランプリ、それからトロリー・トラックで楽しもう！ "),
   24: ("3月ツキナカ", "3月15日を警戒せよ！ウラギリンの侵略からトゥーンタウンを守れ！"),
   26: ("ハロウィーン デコレ", "おばけの木とデコレーションでさまがわりしたトゥーンタウンをお楽しみあれ！"),
   28: ("おし売りおことわり！", "セルボット達のしつこいセールス戦略には、バトルで“No”と言おう！"),
   33: ("セルボット・サプライズ１", "セルボット・サプライズ！ブアイソン達の侵略からトゥーンタウンを守れ！ "),
   34: ("セルボット・サプライズ２", "セルボット・サプライズ！タッシャーナ達の侵略からトゥーンタウンを守れ！ "),
   35: ("セルボット・サプライズ３", "セルボット・サプライズ！オオゲーサの侵略からトゥーンタウンを守れ！"),
   36: ("セルボット・サプライズ４", "セルボット・サプライズ！クロマクールの侵略からトゥーンタウンを守れ！ "),
   37: ("マネーボット・スクランブル１", "マネーボット・スクランブル！チョロマカシー達の侵略からトゥーンタウンを守れ！ "),
   38: ("マネーボット・スクランブル２", "マネーボット・スクランブル！セコビッチ達の侵略からトゥーンタウンを守れ！"),
   39: ("マネーボット・スクランブル３", "マネーボット・スクランブル！カッチリン達の侵略からトゥーンタウンを守れ！ "),
   40: ("マネーボット・スクランブル４", "マネーボット・スクランブル！スウジスキー達の侵略からトゥーンタウンを守れ！ "),
   41: ("ロウボット・チャージ１", "ロウボット・チャージ！タイコモチー達の侵略からトゥーンタウンを守れ！"),
   42: ("ロウボット・チャージ２", "ロウボット・チャージ！ニマイジタン達の侵略からトゥーンタウンを守れ！"),
   43: ("ロウボット・チャージ３", "ロウボット・チャージ！ツケコミン達の侵略からトゥーンタウンを守れ！"),
   44: ("ロウボット・チャージ４", "ロウボット・チャージ！ウラギリン達の侵略からトゥーンタウンを守れ！ "),
   45: ("ボスボット・リベンジ１", "ボスボット・リベンジ！オベッカー達の侵略からトゥーンタウンを守れ！"),
   46: ("ボスボット・リベンジ２", "ボスボット・リベンジ！カリカリン達の侵略からトゥーンタウンを守れ！"),
   47: ("ボスボット・リベンジ３", "ボスボット・リベンジ！ガミガミーナ達の侵略からトゥーンタウンを守れ！"),
   48: ("ボスボット・リベンジ４", "ボスボット・リベンジリストラマン達の侵略からトゥーンタウンを守れ！"),
   49: ("ジェリービーン・デー", "今日はパーティーに参加するとごほうびのジェリービーンがいつもの二倍もらえるよ！ "),
   53: ("ブアイソンの侵略", "ブアイソン達の侵略からトゥーンタウンを守れ！"),
   54: ("カッチリンの侵略", "カッチリン達の侵略からトゥーンタウンを守れ！"),
   55: ("ニマイジタンの侵略", "ニマイジタン達の侵略からトゥーンタウンを守れ！"),
   56: ("リストラマンの侵略", "リストラマンの侵略からトゥーンタウンを守れ！"),    

    }

UnknownHoliday = "未知の休日 %d"
HolidayFormat = "%m/%d "

# parties/ToontownTimeManager.py
TimeZone = "Japan"
