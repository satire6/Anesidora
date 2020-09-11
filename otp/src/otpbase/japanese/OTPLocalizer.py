import string
from otp.otpbase.japanese.OTPLocalizer_Property import *

# common locations
lTheBrrrgh = 'ブルブルランド'
lDaisyGardens = 'デイジーガーデン'
lDonaldsDock = "ドナルドのハトバ"
lDonaldsDreamland = "ドナルドのドリームランド"
lMinniesMelodyland = "ミニーのメロディーランド"
lToontownCentral = 'トゥーンタウンセントラル'
lGoofySpeedway = "グーフィーサーキット"
lOutdoorZone = "チップとデールのドングリ広場"
lGolfZone = "チップとデールのミニゴルフ"

# common strings
lCancel = 'キャンセル'
lClose = 'とじる'
lOK = 'ＯＫ'
lNext = 'つぎへ'
lNo = 'いいえ'
lQuit = 'やめる'
lYes = 'はい'

Cog  = "コグ"
Cogs = "コグ"

# OTPDialog.py
DialogOK = lOK
DialogCancel = lCancel
DialogYes = lYes
DialogNo = lNo
DialogDoNotShowAgain = "次から\n表示しない"

# DistributedAvatar.py
WhisperNoLongerFriend = "%sが ともだちリストから抜けました。"
WhisperNowSpecialFriend = "%sが ないしょのともだちになりました！"
WhisperComingToVisit = "%sが 会いにきます。"
WhisperFailedVisit = "%sが 会いに来ようとしましたが、失敗しました。"
WhisperTargetLeftVisit = "%sは 別の場所にいったようです。またトライしてください"
WhisperGiveupVisit = "%sが 動き回るキミを見つけられなかったようです。"
WhisperIgnored = "%sが キミをむししています！"
TeleportGreeting = "やあ、%s"
WhisperFriendComingOnline = "%sが オンラインにやってきます。"
WhisperFriendLoggedOut = "%sが ログアウトしました。"
WhisperPlayerOnline = "%sが%sにログインしました"
WhisperPlayerOffline = "%sはオフラインです"
WhisperUnavailable = "このプレイヤーにはもうひそひそ話が使えません。"

DialogSpecial = "おお～"
DialogExclamation = "!"
DialogQuestion = "?"

# ChatInputNormal.py
ChatInputNormalSayIt = "しゃべる"
ChatInputNormalCancel = "閉じる"
ChatInputNormalWhisper = "ひそひそ話"
ChatInputWhisperLabel = "%sに"

# ChatInputSpeedChat.py
SCEmoteNoAccessMsg = "この表現にはまだアクセスできないよ。"
SCEmoteNoAccessOK = lOK

ParentLogin = "保護者のログイン"
ParentPassword = "保護者パスワード"

# ChatGarbler.py
ChatGarblerDefault = ["フガー"]

# ChatManager.py
ChatManagerChat = "チャット"
ChatManagerWhisperTo = "ささやく→"
ChatManagerWhisperToName = "\n%sに ささやく"
ChatManagerCancel = lCancel
ChatManagerWhisperOffline = "%sはオフラインだよ。"
OpenChatWarning = 'まだ"ひみつのともだち"がいないよ。\nひみつのともだちではないトゥーンとは\nチャットはできないんだ。\n\nひみつのともだちになりたいトゥーンが\nいたら、クリックしてウィンドウから\n「ひみつ」を選んでね。\nもちろん、スピードチャットなら他の誰とでも話せるよ！'
OpenChatWarningOK = lOK
UnpaidChatWarning = '購読を申し込んだ後は、このボタンを押せばキーボードを使ってともだちとチャットできるよ。でも、それまではスピードチャットで他のトゥーンと話してね'
UnpaidChatWarningPay = "購読を申し込む"
UnpaidChatWarningContinue = "無料お試し版で続ける"
PaidNoParentPasswordWarning = '保護者パスワードをセットすると、このボタンでキミの友達とチャットすることができるようになるよ。それまではスピードチャットでお話をしてね。'
UnpaidNoParentPasswordWarning = 'Once you have set your parent password, you can enable this button to chat with your friends using the keyboard. To set your parent password, exit Toontown and then click on "Preferences" under Member Services on the Toontown web page. Until then, you should chat with other Toons using SpeedChat.'
PaidNoParentPasswordWarningSet = "保護者パスワードを設定しましょう！"
PaidNoParentPasswordWarningContinue = "ゲームを続ける"
PaidParentPasswordUKWarning = 'チャットを有効にすると、キーボードでともだちとチャットするボタンが使えるようになります。それまではスピードチャットを使ってともだちと話そう！'
PaidParentPasswordUKWarningSet = "チャットを始めよう！"
PaidParentPasswordUKWarningContinue = "ゲームを続ける"
NoSecretChatWarningTitle = "保護者管理ツール"
NoSecretChatWarning = 'ともだちとチャットしたい場合は、 「ひみつのともだち」をオンにしてね。  プレイヤーのキミ達へ： 「ひみつのともだち」や保護者コントロールの事をもっと知りたかったら、保護者の方に保護者パスワードを入力してもらってね'
RestrictedSecretChatWarning = '「ひみつ」を入手するか、入力するためには「保護者パスワード」を入力する必要があります。「ひみつのともだち」オプションを変更することで、この画面を無効にすることができます。'
NoSecretChatWarningOK = lOK
NoSecretChatWarningCancel = lCancel
NoSecretChatWarningWrongPassword = 'パスワードが正しくありません。 このアカウントを作成する時に登録した 保護者パスワードを入力してください。 なお、この保護者パスワードはゲームプレイ時に必要なパスワードとは違うものです'
NoSecretChatAtAllTitle = "ひみつのともだちチャット"
# not sure what this should do in the new world order
NoSecretChatAtAll = 'ともだちとチャットしたい場合は、「ひみつのともだち」をオンにしてね。  「ひみつのともだち」にはゲームの外の世界でひみつのパスワードをお互いに知らせることが出来ないとダメなんだ。これが出来なければ「ひみつのともだち」チャットはできないよ。\n\nこの機能をオンにしたい場合、またはもっと知りたい場合はトゥーンタウンを一度終了して、トゥーンタウンのホームページにある「アカウントオプション」をクリックしてね。'
NoSecretChatAtAllAndNoWhitelistTitle = "Chat button"
# not sure what this should do in the new world order
NoSecretChatAtAllAndNoWhitelist = 'You can use the blue Chat button to communicate with other Toons by using Speechat Plus or Open Chat with True Friends.\n\nSpeedchat Plus is a form of type chat that allows users to communicate by using the Disney SpeedChat Plus dictionary.\n\nOpen Chat with True Friends is a form of type chat that allows real-life friends to communicate openly with each other by means of a True Friend Code that must be communicated outside of the game.\n\nTo activate either of thse features, or to learn more about them, exit Toontown and then click on "Preferences" under Member Services on the Toontown Web site.'
NoSecretChatAtAllOK = lOK
ChangeSecretFriendsOptions = "「ひみつのともだち」オプションを変更する"
ChangeSecretFriendsOptionsWarning = '\n「保護者パスワード」を入力して「ひみつのともだち」オプションを変更してください。'
ActivateChatTitle = "「ひみつのともだち」オプション" #▲

WhisperToFormat = "To %s %s"
WhisperToFormatName = "To %s"
WhisperFromFormatName = "%sからのひそひそ話"

from pandac.PandaModules import TextProperties
from pandac.PandaModules import TextPropertiesManager

shadow = TextProperties()
shadow.setShadow(-0.025, -0.025)
shadow.setShadowColor(0,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('shadow', shadow)

red = TextProperties()
red.setTextColor(1,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('red', red)

green = TextProperties()
green.setTextColor(0,1,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('green', green)

yellow = TextProperties()
yellow.setTextColor(1,1,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('yellow', yellow)

midgreen = TextProperties()
midgreen.setTextColor(0.2,1,0.2,1)
TextPropertiesManager.getGlobalPtr().setProperties('midgreen', midgreen)

blue = TextProperties()
blue.setTextColor(0,0,1,1)
TextPropertiesManager.getGlobalPtr().setProperties('blue', blue)

white = TextProperties()
white.setTextColor(1,1,1,1)
TextPropertiesManager.getGlobalPtr().setProperties('white', white)

black = TextProperties()
black.setTextColor(0,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('black', black)

grey = TextProperties()
grey.setTextColor(0.5, 0.5, 0.5, 1)
TextPropertiesManager.getGlobalPtr().setProperties('grey', grey)

ActivateChat = """自由にチャットするには、ゲームの外の世界で友達と秘密のパスワードを交換しなくてはなりません。

「ひみつのともだち」はプレイヤーに自由なやりとりをさせるものであり、監視されるものではありません。保護者がユーザーであるお子様が「ひみつのともだち」機能を付加させたゲームをプレイする際は、保護者監視を推奨します。この機能は、解除されるまで有効であるとします。
















「ひみつのともだち」機能が有効に設定されているゲームプレイに伴うリスクが存在すること、有効に設定することによりこのようなリスクの存在とそれに関する情報をあらかじめ了承していることに同意します。"""

ActivateChatYes = "有効にする"
ActivateChatNo = lCancel
ActivateChatMoreInfo = "詳細"
ActivateChatPrivacyPolicy = "プライバシーポリシー"

# SecretFriendsInfoPanel.py
SecretFriendsInfoPanelOk = lOK
SecretFriendsInfoPanelClose = lClose
SecretFriendsInfoPanelText = ["""
「ひみつのともだち」機能

「ひみつのともだち」は、トゥーンタウン・オンライン（以下、「サービス」）上で他の会員と直接チャットができるようにする機能です。お子様が「ひみつのともだち」機能をご利用されようとする際、お子様の保護者パスワードの入力よる本機能のご使用に対し、保護者の同意が必要となります。「サリー」と「マイク」と呼ばれる会員間での「ひみつのともだち」コネクションの詳しい作成手順は、以下の通りです。
１．サリーの保護者とマイクの保護者はそれぞれ、(a)本サービス内のアカウントオプションのページまたは(b) 保護者管理ツールのポップアップのいずれかで各自の保護者パスワードを入力することにより、「ひみつのともだち」機能を可能にすることができます。
２．サリーは本サービス内から、（後述の）「ひみつ」を要求することができます。
""","""
３．サリーの「ひみつ」は、本サービス上にいないマイクに伝えられます。（サリーのひみつは、直接サリー、またはサリーがひみつを打ちあけた他の会員によって間接的にマイクに伝えられます。）
４．マイクは、サリーが本サービスから「ひみつ」を要求した４８時間以内に、サリーのひみつを本サービスに提出します。
５．そして、本サービスは、マイクにサリーが彼の「ひみつのともだち」になったことを知らせます。同様に、サリーにもマイクが彼女の「ひみつのともだち」になったことを知らせます。
６．これでお互い、どちらかが相手を今後「ひみつのともだち」としないことを選択、または、いずれかの保護者により「ひみつのともだち」機能をできないようににされるまで、サリーとマイクは直接チャットすることができるようになります。「ひみつのともだち」コネクションは、このように（a）（本サービス内で記述されているように）自分の友だちリストから「ひみつのともだち」を削除する会員、（b）本サービス内のお支払い関連のページに行きその手順に従って「ひみつのともだち」機能をできないようにする保護者、のいずれかにより、いつでも使用できないようにすることが可能です。
""","""
「ひみつ」は、特定の会員に割り当てられるコンピュータ生成されたランダムな暗号です。「ひみつ」は、会員が「ひみつ」を要求してから４８時間内にその「ひみつのともだち」コネクションを作るために使用されます；そうでないと、その「ひみつ」は期限切れになり、使用できなくなります。ひとつの「ひみつ」は、ひとつの「ひみつのともだち」コネクションを設立するためだけに使用されます。「ひみつのともだち」コネクションを追加するには、会員は各々の追加「ひみつのともだち」に対し追加「ひみつ」を要求しなければなりません。

「ひみつのともだちの輪」は、転送されません。例えば、サリーがマイクの「ひみつのともだち」になり、マイクがジェシカの「ひみつのともだち」になる場合、サリーが自動的にジェシカの「ひみつのともだち」になることはありません。サリーとジェシカが「ひみつのともだち」になるには、２人のうちどちらかが本サービスから新しい「ひみつ」を要求し、それを相手に伝える必要があります。
""","""
「ひみつのともだち」は、お互い自由な形式でのインタラクティブチャットでやりとりをします。このチャットの内容は、参加する会員により直接入力され、ウォルト・ディズニー・インターネット・グループ（ＷＤＩＧ）により運営されている本サービスを通じて処理されます。当社では、個人情報を交換する状況が起きないという保証はできませんので、会員に氏名、Ｅメールアドレス、住所又は電話番号等の個人情報は交換しないようお勧めしています。「ひみつのともだち」のチャットは、そこで使われる悪い言葉のほとんどには自動的にフィルターをかけられますが、当社が調整したり、管理することはありません。保護者がお子様に「ひみつのともだち」の機能をできるようにして自身のアカウントを使用させる際には、本サービス内でプレイしている間お子様を保護者が管理することを、当社は強くお勧めします。
""","""
ＷＤＩＧは、「ひみつのともだち」のチャットの内容をその会員の「ひみつのともだち」に内容を伝達する以外の目的で一切使用することはなく、(1)法律により要請された場合、例えば、裁判所の命令または召集に応じて；(2)（本サービスのホームページ上で接続可能な）サービスでの適切な使用条件を実施するため、（3)本サービスの会員と本サービスの安全保障と安全保護のため、以外の場合、第三者に公開することはありません。ＷＤＩＧへの要請によりお子様の保護者は、お子様が作成し、そのファイルからＷＤＩＧが未削除のいかなる「ひみつのともだち」チャットの内容を検閲、削除することができます。子供オンラインプライバシー保護法に従い、当社は、お子様の（「ひみつのともだち」を含む）いかなる活動への参加、これらの活動に参加するために必要なもの以上に詳細な個人情報の公開における調整は禁じられており、一切調整はしません。
""","""
さらに、前述のように、当社は、お子様の「ひみつのともだち」機能使用における当社の許可を打ち切る保護者の権利も認識しております。「ひみつのともだち」機能を使えるようにすることは、その機能を通じ、他人とチャットする会員の能力には免れないリスクがあるという情報を認識し、これらのリスクの受け入れを承諾することになります。
"""
]

LeaveToPay = """購入するにあたり、一旦ウェブサイトに戻ります。"""
LeaveToPayYes = "購入"
LeaveToPayNo = lCancel

LeaveToSetParentPassword = """保護者パスワードを設定するために、ゲームから出ます。"""
LeaveToSetParentPasswordYes = "パスワードを設定"
LeaveToSetParentPasswordNo = lCancel

LeaveToEnableChatUK = """チャットを有効にするために、一旦ゲームから出ます。"""
LeaveToEnableChatUKYes = "チャットを有効にする"
LeaveToEnableChatUKNo = lCancel

ChatMoreInfoOK = lOK
SecretChatDeactivated = '「ひみつのともだち」機能がオフになりました。'
RestrictedSecretChatActivated = '制限つき「ひみつのともだち」機能がオンになりました。'
SecretChatActivated = '「ひみつのともだち」機能がオンになりました。\n\nオフにしたい場合はトゥーンタウンのウェブページにある「アカウントオプション」をクリックしてください。'
SecretChatActivatedOK = lOK
SecretChatActivatedChange = "オプションを変更"
ProblemActivatingChat = '「ひみつのともだち」チャットが起動できません！\n\n%s\n\nリトライしてみてください'
ProblemActivatingChatOK = lOK

# MultiPageTextFrame.py
MultiPageTextFrameNext = lNext
MultiPageTextFramePrev = 'まえ'
MultiPageTextFramePage = '%s/%sページ'

# GuiScreen.py
GuiScreenToontownUnavailable = "トゥーンタウンは一時的に利用できなくなっています。引き続き呼び出し中です…"
GuiScreenCancel = lCancel


# CreateAccountScreen.py
CreateAccountScreenUserName = "アカウント名"
CreateAccountScreenPassword = "パスワード"
CreateAccountScreenConfirmPassword = "パスワード確認"
CreateAccountScreenCancel = lCancel
CreateAccountScreenSubmit = "次へ"
CreateAccountScreenConnectionErrorSuffix = ".\n\nあとでもう一度やりなおしてください"
CreateAccountScreenNoAccountName = "アカウント名を入力してください"
CreateAccountScreenAccountNameTooShort = "アカウント名には最低%s文字入力必要です。もう一度入力してください。"
CreateAccountScreenPasswordTooShort = "パスワードは最低%s文字必要です。もう一度入力してください。"
CreateAccountScreenPasswordMismatch = "パスワードが間違っています。もう一度入力してください。"
CreateAccountScreenUserNameTaken = "このユーザー名は既に使用されています。 もう一度別の名前を入力してください。"
CreateAccountScreenInvalidUserName = "無効なユーザー名です。\nもう一度入力してください。"
CreateAccountScreenUserNameNotFound = "ユーザー名がみつかりません。\nもう一度入力するか、新規アカウントを作成してください。"

# ToontownClientRepository.py
CRConnecting = "接続中…"
# host, port
CRNoConnectTryAgain = "%s:%sに接続できませんでした。\n再試行しますか？"
CRNoConnectProxyNoPort = "%s:%sに接続できませんでした。\n\nあなたのインターネット接続はプロキシ経由で行われていますが、プロキシが%sポートへの接続を拒否しています。\n\nトゥーンタウンをプレイする場合は、このポートをオープンにするか、プロキシの設定をはずしてください。プロキシがＩＳＰによって供給されている場合は、プロキシが使用できるようにＩＳＰに申し出てください。"
CRMissingGameRootObject = "（ネットワーク回線の不具合により）いくつかのゲームファイルが足りません。ゲームを終了します。"
CRNoDistrictsTryAgain = "現在、トゥーンタウンに空いているロビーがありません。\n再試行しますか？"
CRRejectRemoveAvatar = "このトゥーンは削除できませんでした。また後で試してね。"
CRLostConnection = "トゥーンタウンへの接続が切れました。"
CRBootedReasons = {
    1: "予想外の問題が発生しました。接続が切断されましたが、すぐにゲームに戻ることが出来ます。",
    100: "他のユーザーが他のコンピュータからあなたのアカウントを使用してログインしたため、接続が切れました。",
    120: "キーボード使用のチャットとその認証に関する問題が発生したため、接続が切れました。",
    122: "トゥーンタウンへのログインに際し問題が発生しました。ディズニー・インターネット・グループ・カスタマーセンターにご連絡ください。",
    125: "インストールされたトゥーンタウンのファイルが有効ではありません。トゥーンタウンで遊ぶためにはオフィシャルウェブサイト上のプレイボタンを押してください。",
    126: "管理者の権限を行使する資格がありません。",
    151: "トゥーンタウンのサーバー管理者により、ログアウトされました。",
    152: "There has been a reported violation of our Terms of Use connected to '%(name)s'が関わる使用条件、またはハウスルールの違反が報告されています。ねんのため、このアカウントを一時的に無効にしました。詳しくは'%(name)s'の登録時に入力したEmailアドレスに送られたメッセージをご確認下さい。",
    153: "あなたがプレイしていたトゥーンタウンのロビーがリセットされました。同じロビーの参加者は全員接続が切られましたが、接続を再試行後ゲームに戻ることが可能です。",
    288: "今月分のトゥーンタウンプレイ時間いっぱいになりましたので、接続を切断いたしました。",
    349: "今月分のトゥーンタウンプレイ時間いっぱいになりましたので、接続を切断いたしました。",
    }
CRBootedReasonUnknownCode = "予想外の問題が発生しました (エラーコード：%s)。接続が切断されましたが、接続を再試行後ゲームに戻ることが可能です。"
CRTryConnectAgain = "\n\n接続を再試行しますか？"
# avName
CRToontownUnavailable = "トゥーンタウンはこの時間接続ができないようです。現在接続トライ中…"
CRToontownUnavailableCancel = "キャンセル"
CRNameCongratulations = "おめでとう！"
CRNameAccepted = "キミのトゥーンの名前が\nトゥーンタウン事務局によって\n承認されたよ。\n\n今日からキミのトゥーンの名前は\n\"%s\"！"
CRServerConstantsProxyNoPort = "%sに接続できませんでした。\n\nあなたのインターネット接続はプロキシ経由で行われていますが、プロキシが%sポートへの接続を拒否しています。\n\nトゥーンタウンをプレイする場合は、このポートをオープンにするか、プロキシの設定をはずしてください。プロキシがＩＳＰによって供給されている場合は、プロキシが使用できるようにＩＳＰに申し出てください。"
CRServerConstantsProxyNoCONNECT = "%sに接続できませんでした。\n\nあなたのインターネット接続はプロキシ経由で行われていますが、プロキシがCONNECTモードに対応していません。\n\nトゥーンタウンをプレイする場合は、このモードを有効にするか、プロキシの設定をはずしてください。プロキシがＩＳＰによって供給されている場合は、プロキシが使用できるようにＩＳＰに申し出てください。"
CRServerConstantsTryAgain = "%sに接続できませんでした。\n\nトゥーンタウンのアカウントサーバが落ちている、またはインターネット接続に問題がある可能性があります。\n\n再試行しますか？"
CRServerDateTryAgain = "%sでサーバ日時が発見できませんでした。\n再試行しますか？"
AfkForceAcknowledgeMessage = "あなたのトゥーンは、 眠くなったのでベッドに 行きました。"
PeriodTimerWarning = "今月分のトゥーンタウンプレイ時間がもうすぐいっぱいです！"
PeriodForceAcknowledgeMessage = "今月分のトゥーンタウンプレイ時間がいっぱいになりました。また来月遊びに来てね！"
CREnteringToontown = "トゥーンタウンに入ります…"

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "ダウンロード中 %s"
DownloadWatcherInitializing = "準備中..."

# LoginScreen.py
LoginScreenUserName = "アカウント名"
LoginScreenPassword = "パスワード"
LoginScreenLogin = "ログイン"
LoginScreenCreateAccount = "アカウント作成"
LoginScreenQuit = "中止する"
LoginScreenLoginPrompt = "ユーザー名とパスワードを入力してください。"
LoginScreenBadPassword = "パスワードが間違っています。\nもう一度入力してください。"
LoginScreenInvalidUserName = "ユーザー名が間違っています。\nもう一度入力してください。"
LoginScreenUserNameNotFound = "ユーザー名が見つかりません。\nもう一度入力してください。"
LoginScreenPeriodTimeExpired = "今月分のトゥーンタウンプレイ時間がいっぱいになりました。また来月遊びに来てね！"
LoginScreenNoNewAccounts = "ごめんなさい！今、新規アカウントは受け付けていません"
LoginScreenTryAgain = "もう一度やりなおしてください。"


# SpeedChat

# Avatar.py
DialogSpecial = "おお～"
DialogExclamation = "!"
DialogQuestion = "?"
# Cutoff string lengths to determine how much barking to play
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# Used several places in the game. Defined globally because
# we keep changing the name
GlobalSpeedChatName = "スピードチャット"

# Toontown Speedchat
SCMenuPromotion  = "格上げ"
SCMenuElection  = "人気投票" #★
SCMenuEmotions  = "きもち"
SCMenuCustom    = "自分のフレーズ"
SCMenuResistance = "力をあわせて！"
SCMenuPets      = "ペット"
SCMenuPetTricks = "トリック"
SCMenuCog       = "コグ"
SCMenuHello     = "こんにちは"
SCMenuBye       = "さようなら"
SCMenuHappy     = "たのしい"
SCMenuSad       = "かなしい"
SCMenuFriendly  = "感じいい"
SCMenuSorry     = "ごめん"
SCMenuStinky    = "感じわるい"
SCMenuPlaces    = "場所"
SCMenuToontasks = "トゥーンタスク"
SCMenuBattle    = "バトル"
SCMenuGagShop   = "ギャグショップ"
SCMenuFactory   = "工場"
SCMenuKartRacing   = "カートレース"
SCMenuFactoryMeet = "合う"
SCMenuCFOBattle = "マネーマネー"
SCMenuCFOBattleCranes = "クレーン"
SCMenuCFOBattleGoons = "グーン"
SCMenuCJBattle = "ﾁｰﾌ ｼﾞｬｽﾃｨｽ"
SCMenuCEOBattle = "C.E.O."
SCMenuGolf   = "ゴルフ"
SCMenuWhiteList = "ホワイトリスト"
SCMenuPlacesPlayground           = "プレイグラウンド"
SCMenuPlacesEstate               = "おうち"
SCMenuPlacesCogs                 = "コグ"
SCMenuPlacesWait                 = "待って"
SCMenuFriendlyYou                = "キミは…"
SCMenuFriendlyILike              = "…が好きだよ"
SCMenuPlacesLetsGo               = "…へ行こうよ"
SCMenuToontasksMyTasks           = "自分のタスク"
SCMenuToontasksYouShouldChoose   = "…を選んだ方がいいよ"
SCMenuToontasksINeedMore         = "I need more..."
SCMenuBattleGags                 = "ギャグ"
SCMenuBattleTaunts               = "コグへのセリフ" #★
SCMenuBattleStrategy             = "作戦" #★
SCMenuBoardingGroup              = "BOARDING"
SCMenuParties                    = "PARTIES"

# FriendSecret.py
FriendSecretNeedsPasswordWarningTitle = "保護者管理画面"
FriendSecretNeedsParentLoginWarning = """ひみつのことばを手に入れるには、保護者の方の承認が必要です。ひみつのともだちの設定は、トゥーンタウン・オンラインのWebサイトにあるメンバー向けサービスページにあります。"""
FriendSecretNeedsPasswordWarning = """「ひみつ」機能を利用するには、保護者パスワードを入力してください。解除するにはトゥーンタウン・オンラインのウェブサイトにアクセスして設定をしてください。"""
FriendSecretNeedsPasswordWarningOK = lOK
FriendSecretNeedsPasswordWarningCancel = lCancel
FriendSecretNeedsPasswordWarningWrongUsername = """That's not the correct username.  Please enter the username of the parental account.  This is not the same username used to play the game."""
FriendSecretNeedsPasswordWarningWrongPassword = """入力されたパスワードが正しくありません。ゲームを遊ぶためのパスワードではなく、トゥーンタウン・オンラインを購入した際に作成された「保護者パスワード」を入力してください。"""
FriendSecretIntro = "現実世界で知っている人とディズニーのトゥーンタウン・オンラインをプレイしているなら、「ひみつのともだち」になる事ができます。「ひみつのともだち」になると、キーボードを使ったチャットが出来るようになり、他のトゥーンにチャット内容が知られることはありません。\n\n「ひみつのともだち」になりたい人だけに「ひみつ」を知らせ、その人がスクリーンでその内容を入力すると、トゥーンタウンで「ひみつのともだち」になる事が出来ます。"
FriendSecretGetSecret = "「ひみつ」ゲット"
FriendSecretEnterSecret = "知り合いからの「ひみつ」を持っている人は、こちらに入力してください"
FriendSecretOK = lOK
FriendSecretEnter = "「ひみつ」を入力"
FriendSecretCancel = lCancel
FriendSecretGettingSecret = "「ひみつ」を入手しています…"
FriendSecretGotSecret = "「ひみつのことば」をゲットしたよ！\nともだちに伝えられるように\nかならず書きとめておいてね！\n\n※まんなかにスペースがあるからちゅういしてね。\n\nこのことばは１人のともだちにだけ知らせてね。\nそのともだちが入力したあとは、他の誰も使えないよ。\n別のともだちと話をしたかったら、\n別の「ひみつのことば」をゲットしよう。\n\nこの「ひみつ」は２日間だけ使えます。この間にともだちが画面に入力しなかった場合は使えなくなるよ。\n\n「ひみつのことば」は："
FriendSecretTooMany = "今日はこれ以上「ひみつのことば」を持つことができません！\n\nまた明日試してみてね。"
FriendSecretTryingSecret = "「ひみつのことば」を確認中…"
FriendSecretTimeOut = "もうしわけありません。現在ひみつのともだちが設定できません。"
FriendSecretEnteredSecretSuccess = "%sと「ひみつのともだち」になりました！"
FriendSecretEnteredSecretUnknown = "これは誰の「ひみつ」でもないようです。つづりが間違っていないか確認してね。\n\n正しいつづりであれば、有効期限が切れたかもしれないよ。ともだちに新しい「ひみつ」を作ってもらうか、キミが「ひみつ」を作ってともだちに教えてあげてね。"
FriendSecretEnteredSecretFull = "%sとともだちになれません！どちらかのともだちリストがいっぱいすぎるみたいだよ。"
FriendSecretEnteredSecretFullNoName = "どちらかのともだちリストがいっぱいすぎて、ともだちになれません。"
FriendSecretEnteredSecretSelf = "キミ自身の「ひみつ」を入力してしまったみたいだよ。他の人が入力することが出来なくなってしまいました！"
FriendSecretEnteredSecretWrongProduct = "You have entered the wrong type of True Friend Code.\nThis game uses codes that begin with '%s'."
FriendSecretNowFriends = "%sと「ひみつのともだち」になりました！"
FriendSecretNowFriendsNoName = "「ひみつのともだち」になりました！"
FriendSecretDetermineSecret = "どのしゅるいのひみつのともだちになりたい？"
FriendSecretDetermineSecretAvatar = "トゥーンの時だけ"
FriendSecretDetermineSecretAvatarRollover = "ゲームの中だけ"
FriendSecretDetermineSecretAccount = "アカウントレベルで"
FriendSecretDetermineSecretAccountRollover = "Disney.jpのサービス全般を通して"

# GuildMember.py
GuildMemberTitle = "Member Options"
GuildMemberPromote = "Make Officer"
GuildMemberGM = "Make Guildmaster"
GuildMemberDemote = "Demote"
GuildMemberKick = "Eject Member"
GuildMemberCancel = "Cancel"
GuildMemberOnline = "has come online."
GuildMemberOffline = "has gone offline."
GuildPrefix = "(G):"
GuildNewMember = "New Guild Member"

# GuildInvitee.py
GuildInviteeOK = lOK
GuildInviteeNo = lNo
GuildInviteeInvitation = "%s is inviting you to join %s."

GuildRedeemErrorInvalidToken = "Sorry, that code is invalid. Please try again."
GuildRedeemErrorGuildFull = "Sorry, this guild has too many members already."

# FriendInvitee.py
FriendInviteeTooManyFriends = "%sが キミとともだちになりたいみたいだよ。 でもキミのともだちリストはもういっぱいです！"
FriendInviteeInvitation = "%sが キミとともだちになりたいみたいだよ。"
FriendNotifictation = "%s is now your friend."
FriendInviteeOK = lYes
FriendInviteeNo = lNo
GuildInviterWentAway = "%s is no longer present."
GuildInviterAlready = "%s is already in a guild."
GuildInviterBusy = "%s is busy right now."
GuildInviterNotYet = "Invite %s to join your guild?"
GuildInviterCheckAvailability = "Inviting %s to join your guild."
GuildInviterOK = lOK
GuildInviterNo = lNo
GuildInviterCancel = lCancel
GuildInviterYes = lYes
GuildInviterTooFull = "Guild has reached maximum size."
GuildInviterNo = lNo
GuildInviterClickToon = "Click on the pirate you would like to invite."
GuildInviterTooMany = "This is a bug"
GuildInviterNotAvailable = "%s is busy right now; try again later."
GuildInviterGuildSaidNo = "%s does not wish to join."
GuildInviterAlreadyInvited = "%s has already been invited."
GuildInviterEndGuildship = "Eject %s from the guild?"
GuildInviterFriendsNoMore = "%s has left the guild."
GuildInviterSelf = "You are already in the guild!"
GuildInviterIgnored = "%s is ignoring you."
GuildInviterAsking = "Asking %s to join the guild."
GuildInviterGuildSaidYes = "%s will join!"

# FriendInviter.py
FriendOnline = "%s has come online."
FriendOffline = "%s has gone offline."
FriendInviterOK = lOK
FriendInviterCancel = lCancel
FriendInviterStopBeingFriends = "ともだちをやめる"
FriendInviterYes = lYes
FriendInviterNo = lNo
FriendInviterClickToon = "ともだちになりたい トゥーンをクリックしてね。"
FriendInviterTooMany = "ともだちリストがいっぱいで、新しいともだちを作れないよ。 %sと ともだちになりたいのなら、だれかをリストから削除しないといけないよ。"
FriendInviterToonTooMany = "You have too many toon friends on your list to add another one now. You will have to remove some toon friends if you want to make friends with %s."
FriendInviterPlayerTooMany = "You have too many player friends on your list to add another one now. You will have to remove some player friends if you want to make friends with %s."
FriendInviterNotYet = "%sと ともだちになりますか？"
FriendInviterCheckAvailability = "%sと ともだちになれるか、調べています。"
FriendInviterNotAvailable = "%sは いそがしいようです：また後でトライしてみてね。"
FriendInviterNotOpen = "%s does not have open chat, use secrets to make friends"
FriendInviterWentAway = "%sは 行ってしまいました。"
FriendInviterAlready = "%sは ともだちです。"
FriendInviterAlreadyInvited = "%s has already been invited."
FriendInviterAskingCog = "%sに ともだちになってくれるよう聞いています。"
FriendInviterAskingPet = "%sが クルクル、まわりでジャンプしながらキミの顔をなめているよ。"
FriendInviterAskingMyPet = "%sは 既にキミとともだちだよ。"
FriendInviterEndFriendship = "本当に%sと ともだちをやめてもいいのかな？"
FriendInviterFriendsNoMore = "%sは ともだちではなくなりました。"
FriendInviterSelf = "キミはもうキミ自身の「ともだち」だよ！"
FriendInviterIgnored = "%sが キミをむししています。"
FriendInviterAsking = "%sに ともだちになってくれるよう聞いています。"
FriendInviterFriendSaidYes = "%sが ともだちになってくれるそうです！"
FriendInviterPlayerFriendSaidYes = "You are now friends with %s's player, %s!"
FriendInviterFriendSaidNo = "%sが 「ごめんね」と言っています。"
FriendInviterFriendSaidNoNewFriends = "%sは 今、あたらしいともだちを作っていないそうです。"
FriendInviterTooMany = "%sは もうともだちがいっぱいいるそうです！"
FriendInviterMaybe = "%s のコメントは得られませんでした。"
FriendInviterDown = "今、ともだちをつくることは出来ません"

#Talk Path Labels
TalkGuild = "G"
TalkParty = "P"
TalkPVP = "PVP"

#Spam Blocked Message
AntiSpamInChat = "***Spamming***"

#IgnoreConfirm.py
IgnoreConfirmOK = lOK
IgnoreConfirmCancel = lCancel
IgnoreConfirmYes = lYes
IgnoreConfirmNo = lNo
IgnoreConfirmNotYet = "Would you like to Ignore %s?"
IgnoreConfirmAlready = "You are already ignoring %s."
IgnoreConfirmSelf = "You cannot ignore yourself!"
IgnoreConfirmNewIgnore = "You are ignoring %s."
IgnoreConfirmEndIgnore = "You are no longer ignoring %s."
IgnoreConfirmRemoveIgnore = "Stop ignoring %s?"

# Emote.py
# List of emotes in the order they should appear in the SpeedChat.
# Must be in the same order as the function list (EmoteFunc) in Emote.py
EmoteList = [
    "手をふる",
    "たのしい",
    "かなしい",
    "おこる",
    "ねむい",
    "かたをすくめる",
    "おどる",
    "考える",
    "たいくつする",
    "ほめる",
    "すくむ",
    "こんがらがる",
    "すべりこむ",
    "おじぎする",
    "バナナの皮",
    "ケイレイ",#▲
    "笑う",
    lYes,
    lNo,
    lOK,
    "おどろく",
    "なく",
    "よろこぶ",
    "どうようする",
    "わらう"
    ]

EmoteWhispers = [
    "%sが、手をふっているよ。",
    "%sは、うれしいって。",
    "%sは、かなしいって。",
    "%sが、おこっているよ。",
    "%sが、ねむいって。",
    "%sが、かたをすくめているよ。",
    "%sが、おどっているよ。",
    "%sが、考えてるよ。",
    "%sが、たいくつしているよ。",
    "%sが、ほめてるよ。",
    "%sが、すくんでいるよ。",
    "%sは、こんがらがってるって。",
    "%sが、すべりこみしているよ。",
    "%sが、キミにおじぎしているよ。",
    "%sが、バナナの皮ですべっているよ。",
    "%sが、ケイレイしているよ。",#▲
    "%sが、笑っているよ。",
    "%sが、「はい」って言ってるよ。",
    "%sが、「いいえ」って言ってるよ。",
    "%sが、「ＯＫ」って言ってるよ。",
    "%sがおどろいているよ。",
    "%sがないているよ。",
    "%sがよろこんでるよ。",
    "%sがどうようしているよ。",
    "%sがわらっているよ。",
    ]

# Reverse lookup:  get the index from the name.
EmoteFuncDict = {
    "Wave"   : 0,
    "Happy"  : 1,
    "Sad"    : 2,
    "Angry"  : 3,
    "Sleepy" : 4,
    "Shrug"  : 5,
    "Dance"  : 6,
    "Think"   : 7,
    "Bored"  : 8,
    "Applause" : 9,
    "Cringe" : 10,
    "Confused"  : 11,
    "Belly Flop"  : 12,
    "Bow"    : 13,
    "Banana Peel" : 14,
    "Resistance Salute" : 15,
    "Laugh" : 16,
    lYes    : 17,
    lNo     : 18,
    lOK     : 19,
    "Surprise" : 20,
    "Cry" : 21,
    "Delighted" : 22,
    "Furious" : 23,
    "Laugh" : 24,
    }

# SuitDialog.py
SuitBrushOffs = {
    'f':  ["会議に遅れた。",
           ],
    'p':  ["その場をはなれる。",
           ],
    'ym': ['イエスマンがノーと言っている。',
           ],
    None: ["今日は休みだ。",
           "キミ、オフィスがちがうよ。",
           "キミの部下に私の部下を呼びにやらせてくれ。",
           "キミでは役不足だ。",
           "私の秘書に話してくれ。"]
    }

SuitFaceoffTaunts = {
    'b':  ["私への献金は\nあるのかね？",
           "逆らってみろ、\n痛い目にあわせてやる。",
           "しぼりにしぼってやるぞ！",
           "次の選挙では\n私が必ず勝つ！",
           "積極的にがっつくのも\n大事な手腕だよ。",
           "キミは私のサポーター\nなのかな？",
           "キミ、私のサポーター\nになりたまえ。",
           "ぜひとも私にキミの\n一票を！ぜひ！ぜひ！",
           "企業献金はいつでも\n受け付けているよ。",
           "政治活動はハラが\nへるものなのさ。",
           "おお、うまそうな\nトゥーンだな。",
           "もらえるものは\nもらっておくよ。",
           ],
    'm':  ["私に任せておけば\n間違いないよ。",
           "キミの運命、\n私に任せてみない？",
           "バトルなら\n負けないよ！",
           "話し合いの余地は\nないのかい。",
           "ダメージも利息も\n倍返しさ！",
           "まずは営業スマイル、っと！",
           "スマイルだけなら\n０円だよ。",
           "バトルの仕切りは\n私にお任せ。",
           "私がキミを排除する！",
           ],
    'ms': ["すべて私の思い通りってわけさ。",
           "みんな私のあやつり\n人形ってわけさ。",
           "これは私の仮の姿\nなのだよ。",
           "私が動けば世の中も\n動くのだ。",
           "すべては私の指先で\nコントロールしているのさ！",
           "私に従いなさい。",
           "私に従えばいい思いをさせてやるぞ！",
           "金も人も私が動かしているのだよ。",
           "私に逆らおうと\nいうのか？",
           "表に立つのは\n他のやつらで十分さ。",
           "私の力を思い知れ！",
           ],
    'hh': ["頭上注意！",
           "キミの頭を私のコレクションに加えてやろう。",
           "頭を狩られるだけじゃ\n済まんぞ！",
           "キミ、こっち側に\n寝返らないか？",
           "ウチは他よりも給料が高いぞ～！",
           "ウチにはやりがいのある仕事があるぞ～！",
           "転職を\n考えてるのかい？",
           "キミのスキルなら\nウチでうまくやれるぞ！",
           "ウチは倍、出すよ～！",
           "キミは現状に満足しているかい？",
           "頭痛のタネを\nとりのぞいてやろう。",
           ],
    'tbc': ["かかってこい、\nカモーン！\nなんちゃって。",
            "持ちつモッツァレラつつ、\nなんちゃって。",
            "スライスしてやろうか？なんちゃって。",
            "なにごともプロセスが大事なのさ、\nなんちゃって。",
            "私のあだなは\nジャック！",
            "じゅくせいすると私のようないい男になるのだよ、なんちゃって。",
            "何てやチェダー！何てやつだー！わかった？",
            "おや、キミ、賞味期限が近いんじゃない？",
            "このデコボコが私らしい味を出してるんだよ。",
            "どうした、ブルーチーズのように青ざめてるじゃないか。",
            "久しブリー！\nなんちゃって。",
            ],
    'cr': ["行くぞゥ！",
           "キサマの会社をのっとってやる！",
           "オマエも私の肥やしにしてやる！",
           "オマエも私の一部になれ！",
           "私が勝ったらお宝はいただくぞ！",
           "私は他人のものが欲しくなるタチでね。",
           "何でも自分のものにしなくちゃ気がすまないんだ。",
           "ただいまトゥーンを\n駆除中だ。",
           "人のものを奪うのは\nたまらんね。",
           "ハデに行こうじゃないか！",
           ],
    'mh': ["わはは、キミにはかなわんな。",
           "この笑顔で人はダマされるのだよ！",
           "食べたあとは必ず歯磨き！",
           "まあまあ、そうコワい顔をしちゃいかんよ。",
           "ニカッ！",
           "見よ、この輝くような笑顔！",
           "わっはっはっは！",
           "あー、さすがにちょっと顔が引きつってきたな！",
           "笑いながら仕事をビシビシとやるのが男さ。",
           "何事も笑顔でなんとかなるものだ。",
           "私、もしかしたらショービジネスに行けるかも。",
           "やあやあ、バトルと行きますか？",
           ],
    'nc': ["数字をあなどっちゃ\nイカンよ～。",
           "食べちゃいたいぐらい好きだ！",
           "数字命！",
           "電卓、そろばん、なんでもござれだ！",
           "暗算なら私におまかせあれ。",
           "すべては計算ずみだ。",
           "私の計算によると…\nキミの負けだ！",
           "私の計算はぜったいに間違っていない！",
           "計算勝負してみるか？",
           "世の中に割り切れないものはない！",
           ],
    'ls': ["カネのハンターに\nケンカを売るのか？",
           "金の匂いがするぞ～",
           "くんくんくん！カネの匂いだ！",
           "あんた、カネ持ってるな？",
           "小銭あまってない？",
           "電話代貸してくれないかい？",
           "キミのようなヤツがいると私の取り分が減るんだよ。",
           "キミのようなザコは私のごちそうなのさ。",
           "一円を笑うモノは一円に泣く！",
           "カネ出しな！",
           "じゃまするな！",
           ],
    'mb': ["ああ、金が入って入ってしょうがないよ～",
           "世の中、\nカネ、カネ、カネ！",
           "キミ、カネの素晴らしさを知らないね？",
           "もっともっと稼ぐつもりだよ。",
           "ノンストップ、\n金もうけ！",
           "スーツの下は札束が\nかくれてたりして。",
           "マネートラブル？\n私には無縁だね。",
           "ハイリスク、\nハイリターンがおもしろいのさ。",
           "いつもはキミみたいなヤツは相手にしないんだがね。",
           "カネはいくらあっても足りないね！",
           ],
    'rb': ["今いくら持ってる？",
           "私が勝ったらキミの有り金ぜんぶいただくよ。",
           "私に盗めないモノはない！",
           "キミが何を持ってるか見てみようか？",
           "カネを出せ！",
           "手をあげろ！",
           "人のものを奪うのはクセになるね。",
           "有り金ぜんぶ置いていきな！",
           "見知らぬ人に話しかけるなと教わらなかったのか？",
           "おっ、\nもうひと仕事入ったか。",
           ],
    'bs': ["そんなにコワい顔をしないで、仲良くしよう。",
           "大丈夫、私を信用しなさい。",
           "この目がウソを言っているように見えるかい？",
           "私を信じてついてきなさい。",
           "いやー、本当はこんな事したくないんだよ。",
           "これも仕事なんだよ、わかってくれるかい？",
           "私のことをうらまないでくれよ。",
           "きっと、私とキミはこうなる運命だったんだよ。",
           "キミが悪いんだよ。",
           "私はこんな事はしたくないんだが、命令で…",
           "長いものには巻かれろってやつさ。",
           ],
    'bw': ["恐怖で髪が白くならんようにな。",
           "この髪は、\n私の自慢でね。",
           "このシルキーな\n髪の手触り！\n美しいだろう？",
           "おおっと、風で髪が\n乱れてしまった。",
           "は？いや、私は作曲家ではないよ。",
           "キミもホワイトヘアーにしてみないかい？",
           "ビッグなコグには\nビッグな髪型さ。",
           "私の髪を乱すな！",
           "白髪鬼とは、\n私のことだ！",
           "私もダテに、年をきざんだわけじゃないのだよ！",
           ],
    'le': ["法に従わないものは私が罰する！",
           "キミをトリにがすわけには行かん！",
           "トリしまるぞ！",
           "トゥーンをトリしまるのが私のつとめ。",
           "キミは私に勝てっこないよ。",
           "トゥーンタウンの法をトリ戻す！",
           "私が正義だ！",
           "どんな小さな悪もトリこぼさん！",
           "この街の法律は私がトリしきる！",
           "まあそんなにトリみだすな、みっともない。",
           ],
    'sd': ["トラブルシューティングなら私に任せろ。",
           "トラブルの元凶は排除する！",
           "法の破れ目は\n私が直す。",
           "ケガしたら私が診てあげましょう。",
           "急所ははずしてあげますよ。",
           "私は高いですよ。",
           "どこが悪いのかな？",
           "キミのようなトゥーンにはお灸をすえねば。",
           "悪いトゥーンには注射するぞ。",
           "トゥーンの身体のしくみに興味あるんだよ。",
           ],
    'f': ["ボスに言いつけてやるぞ！",
          "私を痛い目にあわせたら許さないぞ～",
          "キミを踏み台にして出世してやる！",
          "私の働きっぷりは気に入らない？",
          "ボスに期待されてるんだ、キミを倒してみせる！",
          "トゥーンを倒してボスに認めてもらう！",
          "まずは私を倒すことだな！",
          "トゥーンのくせになまいきだ！",
          "トゥーン排除なら\n得意さ！",
          "まあキミが、私のボスに会うことはないだろう。",
          "トゥーンはのんびり\nプレイグラウンドで\n遊んでいればいいんだよ。",
          ],
    'p':  ["このバトルの結果を書きとめたいものだ。",
           "芯のないヤツはきらいだ！",
           "用があるならさっさと言え、急いでるんだ！",
           "丸くおさめようったってそうはいかないよ。",
           "今、ちょっと神経がとがっているんだよ。",
           "感覚は常にとぎすませているべきだね。",
           "早く終わらせろ、私は気が短いんだ！",
           "言いたいことがあるならさっさと言え！",
           "キミのことは私の心に書き留めておこう。",
           "都合が悪いことは書き換えてしまえばいいのさ。",
           "キミの芯を折ってやるぞ！",
           ],
    'ym': ["私の辞書に「ノー」の言葉はないのさ。",
           "ボスの言う通りにしていれば間違いない。",
           "バトルかい？答えはもちろん「イエス」だ！",
           "ボスの命令は絶対だ！",
           "キミは「ノー」と言えるトゥーンかい？",
           "ボスが間違ったことは一度もないのさ。",
           "イエース！私がイエスマンだ！",
           "言いなりはラクでいいよ～",
           "私は赤ちゃんのころから「ハイハイ」が上手だったんだ。",
           "ボスに命令されたら逆らえないんだよ、悪いな。",
           "「ノー」は受け付けないぞ。",
           ],
    'mm': ["他人事にクチを突っ込むのが私の仕事！",
           "ちょっとあんた、何様のつもりだい！",
           "ケンカ売ってるのかい！",
           "ああ、また仕事が増えたよ。",
           "最近キミみたいなのが増えてきて困るんだよ。",
           "まったく、困るんだよねぇ。",
           "これだからトゥーンは…",
           "ろくなことも出来ないくせに！",
           "まったく、礼儀ってものを知らないのかい？",
           "私のジャマはしないでおくれよ。",
           "出すぎたことをすると怒るよ。",
           "まったく、使えないトゥーンだね！",
           "コグを見た目で判断してると痛い目にあうよ！",
           "いつまでもうろついてるんじゃないよ、目障りだ！",
           ],
    'ds': ["キミのようなヤツはクビだ！",
           "キミのようなトゥーンはいらないのだよ。",
           "ムダなモノは切り捨てねば。",
           "ムダなトゥーンが多すぎるな。",
           "リストラされたいのかい？",
           "まったく、損な役回りだよ。",
           "わかってくれ、私も辛いんだ。",
           "悪く思わんでくれ。",
           ],
    'cc': ["なんだ、キミは。",
           "邪魔だ。",
           "めざわりだ。",
           "失せな…",
           "消えな…",
           "ふん。",
           "…",
           "………",
           "……………",
           "どうなっても知らんぞ。",
           "別にかまわんが。",
           "手加減はしないぞ。",
           "ザコが…",
           ],
    'tm': ["ダブルポイントキャンペーン中だぜ。",
           "ツケは払ってもらうよ。",
           "お支払いはジェリービーンで？",
           "パンチのきいた贈り物はいかがかな？",
           "むしゃくしゃしてるんだ、近寄るとあぶないぜ。",
           "絶好のターゲットだな。",
           "いいものいっぱいあるよ、見せてあげようか？",
           "今日はいいものがたくさんあるよ。",
           "技のラインナップを見てみますかね？",
           "次の獲物を見つけなくちゃいかんな。",
           "市場リサーチに協力してもらえませんかね？",
           ],
    'nd': ["ああよかった、話し相手が欲しかったんだよ。",
           "ペラペラペラペラ！",
           "話術なら負けないよ。",
           "今日のランチはビッグスマイル氏となのさ！",
           "私、あのオマカセンヌと友達なのよ～",
           "ブアイソンはビジネスマンとしてどうかねぇ。",
           "オオゲーサは調子ばっかりいいだけさ。",
           "クロマクールは毎朝ヒゲの手入れしてるらしいよ。",
           "アイソマンは怒らせたくない相手だよ。",
           "ツーハーンは押しが強いんだよねぇ。",
           ],
    'gh': ["やあやあこんにちは。",
           "この笑顔にだまされなかったのか。",
           "キミと私はともだち！ね、そうだろう？",
           "そんなコワいカオしないでよ～",
           "私はあなたのいいパートナーになりますよ～",
           "そこのキミ！私とビジネスしませんか～？",
           "仲良くしましょうよ～",
           "私を敵にまわしたくないんじゃない～？",
           "はいはい、友情のあくしゅ！",
           "握手しよう、友よ！",
           "いやー、キミもいい笑顔してるね！",
           "その笑顔、私に負けてないよ！",
           "わっはっはっはっは。",
           ],
    'sc': ["バレてないと思ってたのにな。",
           "少し多めに請求するのがコツさ。",
           "トゥーンからは高くしぼるよ。",
           "チリも積もれば山となるのさ。",
           "チョロっと負かしてやるよ。",
           "私にはカンタンに勝てると思ってるだろ？",
           "頭がよくなきゃできないのさ、これ。",
           "すばやく確実に、が極意さ。",
           "スーツの下に隠してたの、バレた？",
           "隠しダネ勝負なら負けん！",
           "極意は、すばやく確実に！",
           ],
    'pp': ["キミの相手をしてる時間はないんだよ。",
           "これをキミに使うの、もったいないよ。",
           "ああもう、時間がもったいない！",
           "当然ワリカンだよね～",
           "時はカネなり！もったいないな～",
           "キミにはこの攻撃、もったいないよ。",
           "貴重な時間を割かせないでくれ。",
           "そうでなくても今月はムダが多いのに！",
           "キミに使うアタックの分、あとで請求しなくちゃ。",
           "時給を割り増ししてもらわなきゃな。",
           ],
    'tw': ["キミの資金源をストップさせてやる。",
           "これがキミのオファーなのかい？",
           "ほらほら、さっさと決着つけようよ。",
           "モタモタしてないで終わらせよう。",
           "素手の勝負ならカネがかからないな。",
           "私はサイフのヒモもこぶしもかたいよ～",
           "キミに大損害を与えてやる！",
           "損害補償に入ってるかい？",
           "私の攻撃は高いよ～",
           "ムダ使いは敵！",
           "キミの予算に打撃を与えてやる！",
           ],
    'bc': ["トゥーンを引き算するのは楽しいですよ。",
           "キミもカンペキに倒してやる！",
           "キッチリとカタをつけてやる！",
           "おカタいのは性格だけじゃないですよ。",
           "私に抜かりはない！",
           "１００％確実に仕事しますよ。",
           "身の程を知ったほうがいいですよ。",
           "外見も仕事もきっちりかっちり！",
           "ムダは排除してやる！",
           "ジャマするな！",
           "笑ってばかりいないでかちっとしろ！",
           ],
    'bf': ["よっ！大将！",
           "キミをボスに連れていけばごほうびもらえるかな？",
           "一生ついて\n行きますよ～",
           "うーん、キミ、おいしそうだね。",
           "腹へってきてたんだよね～",
           "これぞタイコモチーのタイコっ腹！",
           "いよっ！\nトゥーンの鑑！",
           "いやー、さすがアナタは目の付け所が違いますね～",
           "台詞が思い浮かばない時にエンカウントされた！",
           "キミをランチにいただいてもいいかな？",
           ],
    'tf': ["私はこれで今まで食ってきたんだ。",
           "フェイス…オフ！なんてね。",
           "私のジャマをするとはいい度胸だ！",
           "キミは私の本当の顔を知らない。",
           "いや～、近頃のトゥーンは強くて困りましたよ～",
           "表情の使い分けは大事だよ。",
           "私に挑むとは、ダイタンですね。",
           "どちらの顔で倒そうかな。",
           "私を怒らせないようにね。",
           "大胆不敵というか、なんというか。",
           "笑顔のウラを見たいのか？",
           ],
    'dt': ["ダブルトラブルを与えてやる！",
           "顔がふたつならクチもふたつ！",
           "ダブルのものが大好き！",
           "パンチもダブルでお見舞いしようか？",
           "ダブルプレイと行こうか。",
           "バトルは苦手なんだがね…なーんて、ウソ！",
           "舌は多いほうがいいのさ。",
           "舌戦なら負けないさ。",
           "だまされる前にキミをだますよ！",
           "ダブルスに挑みますか？",
           ],
    'ac': ["この間のテストの結果、黙っていてほしければ…",
           "人の弱みをつかむのは最高だ！",
           "私ならトラブルシューティングをお手伝いできますよ。",
           "今日はどうしました？",
           "あやしい者ではありませんよ。",
           "笑ってる場合ではありませんよ。",
           "病院送りにしてやる。",
           "救急車を呼んでおいた方がいいんじゃないか？",
           "逃げ場がなくなるまでつけ込みますよ。",
           "ウデのいい医者、知ってるといいんだが。",
           "その笑顔をなくしてやるぞ。",
           "",
           ]
    }

# These are all the standard SpeedChat phrases.
# The indices must fit into 16 bits (0..65535)
SpeedChatStaticText = {
    # top-level
    1 : lYes,
    2 : lNo,
    3 : lOK,
    4 : "SPEEDCHAT PLUS",

    # Hello
    100 : "やあ！",
    101 : "こんにちは！",
    102 : "こんばんは！",
    103 : "おーい！",
    104 : "げんき！",
    105 : "やあ、みんな！",
    106 : "トゥーンタウンへようこそ！",
    107 : "調子はどう？",
    108 : "元気にしてる？",
    109 : "どうも！",

    # Bye
    200 : "バイバイ！",
    201 : "またあとでね！",
    202 : "またね！",
    203 : "よい一日を！",
    204 : "たのしんでね！",
    205 : "がんばってね！",
    206 : "すぐ戻ってくるね。",
    207 : "行かなきゃ！",
    208 : "後でまた戻るね！",
    209 : "あと２、３分しかないんだ。",

    # Happy
    300 : "(^-^)",
    301 : "イエイ！",
    302 : "ヤッホー！",
    303 : "いいねー！",
    304 : "いやっほーう！",
    305 : "イェ―イ！",
    306 : "それ見ろ！",
    307 : "えへへ！",
    308 : "ワーオ！",
    309 : "すごーい！",
    310 : "うわーい！",
    311 : "やったね！",
    312 : "やったー！",
    313 : "きゃー!",
    314 : "サイコー!",
    315 : "くろねこトゥーン！",

    # Sad
    400 : "(--;)",
    401 : "しまった！",
    402 : "ああっ！",
    403 : "ちぇっ!",
    404 : "まったく～…",
    405 : "いたっ！",
    406 : "ゲフッ。",
    407 : "いやだ～！！！",
    408 : "あ～あ！",
    409 : "うそぉ！",
    410 : "もっとゲラゲラポイントが必要かも",

    # Friendly
    500 : "ありがとう!",
    501 : "なんてことないよ。",
    502 : "どういたしまして！",
    503 : "いつでもどーぞ！",
    504 : "だいじょうぶだよ。",
    505 : "これぞチームワーク！",
    506 : "おもしろーい！",
    507 : "友だちになって！",
    508 : "いっしょにやろうよ！",
    509 : "いつもありがとう。",
    510 : "今来たばっかり？",
    511 : "勝ったの？",
    512 : "これはキミにとって危険すぎるよ。",
    513 : "助けはいる？",
    514 : "たすけてくれる？",
    515 : "キミはここにきたのは初めて？",

    # Friendly "You…"
    600 : "いいカンジだね。",
    601 : "すごいね！",
    602 : "すばらしいね！",
    603 : "天才なんじゃない！？",

    # Friendly "I like…"
    700 : "いい名前だね。",
    701 : "かっこいいね。",
    702 : "すてきなシャツだね。",
    703 : "すてきなスカートだね。",
    704 : "すてきな短パンだね。",
    705 : "このゲーム、さいこうだね！",

    # Sorry
    800 : "ごめん！",
    801 : "おっと！",
    802 : "ごめん、今バトルでいそがしいんだ。",
    803 : "ごめんね、今ちょっといそがしいんだ。",
    804 : "ごめん、トゥーンタスクを終わらせるのにいそがしいんだ！",
    805 : "ごめん、急に行かなくちゃいけなくなっちゃった。",
    806 : "ごめん、手間取っちゃった。",
    807 : "ごめん、できないよ。",
    808 : "ごめん、もう待てなくって…。",
    809 : "キミのことがわからないよ。",
    810 : "%sを使ってね。" % GlobalSpeedChatName,
    811 : "ごめん、つりにいそがしいんだ！",
    812 : "ごめん、今ビルの中にいるんだ。",
    813 : "ごめん、今ちょっとともだちをたすけているんだ。",
    814 : "ごめん、今カートレース中なんだ。",
    815 : "ごめん、今ガーデニングをしてるんだ。",
    816 : "ごめん、エレベーターに乗れないみたい。",
    817 : "ごめん、今ゴルフ中なんだ。",
    818 : "ごめんね、ともだちリストがいっぱいなんだ。",

    # Stinky
    900 : "ちょっと！",
    901 : "コグはあっちへいってよ！",
    902 : "やめてよ！",
    903 : "そんなことしちゃだめ！",
    904 : "いじわるしないで！",
    905 : "やさしくしてよ！",
    906 : "バグレポートを送って",
    907 : "先にすすめないよ～",

    # Places
    1000 : "行こう！",
    1001 : "こっちにワープできる？",
    1002 : "じゃ、行こうか！",
    1003 : "どこに行こうか？",
    1004 : "どっち？",
    1005 : "こっち！",
    1006 : "ついてきて",
    1007 : "待って～！",
    1008 : "友だちを待ってるんだ！",
    1009 : "他のトゥーンをさがそう！",
    1010 : "ここで待ってて！",
    1011 : "ちょっと待って！",
    1012 : "ここで会おうね。",
    1013 : "うちに一緒に来れる？",
    1014 : "待たないでいいからね。",
    1015 : "ねぇ、待って！",
    1016 : "マイガーデンに遊びに来てよ！",
    1017 : "次のをまとうね。",

    # Places "Let's go..."
    1100 : "トロリーに乗ろう！",
    1101 : "プレイグラウンドに戻ろう！",
    1102 : "%sと戦おう！" % Cogs,
    1103 : "%sのビルを乗っ取ろう！" % Cog,
    1104 : "エレベーターに乗ろう！",
    1105 : "%sへ行こう！" % lToontownCentral,
    1106 : "%sへ行こう！" % lDonaldsDock,
    1107 : "%sへ行こう！" % lMinniesMelodyland,
    1108 : "%sへ行こう！" % lDaisyGardens,
    1109 : "%sへ行こう！" % lTheBrrrgh,
    1110 : "%sへ行こう！" % lDonaldsDreamland,
    1111 : "%sへ行こう！" % lGoofySpeedway,
    1112 : "キミのおうちに行こう！",
    1113 : "セルボット本部に行こう！",
    1114 : "コグゼキュティブをやっつけよう！",
    1115 : "コグの工場に行こう！",
    1116 : "つりに行こう！",
    1117 : "おうちのまわりでつりしよう！",
    1118 : "マネーボット本部に行こう！",
    1119 : "マネーマネーをやっつけよう！",
    1120 : "マネーファクトリーへ行こう！",
    1121 : "マネーファクトリーの中に入るよ！",
    1122 : "ロウボットＨＱへ行こう！",
    1123 : "サイバンチョーと戦いに行こう！",
    1124 : "ケンサツキョクに行こう！",
    1125 : "%sに行こう！" % lOutdoorZone,    
    1126 : "%sに行こう！" % lGolfZone,
    1127 : "ボスボット本部に行こう！",
    1128 : "CEOとたたかおう!",
    1129 : "コグ・ゴルフをやろう!",

    # Toontasks
    1200 : "どのトゥーンタスクをやってるの？",
    1201 : "そのタスクをやろう。",
    1202 : "これはさがしていたものじゃないよ。",
    1203 : "さがしに行くね。",
    1204 : "このストリートにはないな。",
    1205 : "まだ見つけてないよ。",
    1206 : "コグのメリットが足りないんだよ。",
    1207 : "もっとコグスーツのパーツが必要なんだ！",
    1208 : "これはキミが必要なものじゃないね。",
    1209 : "キミが必要なものを見つけたよ。",
    1210 : "コグドルをもっと集めないと。",
    1211 : "ショウカンジョーが必要なんだ。",
    1212 : "もっとストック・オプションが必要なんだ。",
    1213 : "マネーボットスーツの部品が必要なんだ。",
    1214 : "ロウボットスーツの部品が必要なんだ。",
    1215 : "ボスボットスーツの部品が必要なんだ。",

    1299 : "トゥーンタスクをゲットしなくちゃ。",

    # Toontasks "I think you should choose…"
    1300 : "トゥーンアップを選ぶべきだよ。",
    1301 : "サウンドを選ぶべきだよ。",
    1302 : "ドロップを選ぶべきだよ。",
    1303 : "トラップを選ぶべきだよ。",
    1304 : "おとりを選ぶべきだよ。",

    # Battle
    1400 : "いそごう！",
    1401 : "ナイスショット！",
    1402 : "ナイスギャグ！",
    1403 : "はずれたよ！",
    1404 : "キミ、やったね！",
    1405 : "やった！",
    1406 : "かかってこーい！",
    1407 : "おちゃのこさいさい！",
    1408 : "カンタンカンタン！",
    1409 : "はしれ！",
    1410 : "たすけて！",
    1411 : "危ない危ない！",
    1412 : "まずいことになっちゃった…",
    1413 : "もっとギャグが必要だね。",
    1414 : "トゥーンアップが必要だね。",
    1415 : "このバトル、パスしたほうがいいんじゃない？",
    1416 : "このチームなら大丈夫！",

    # Battle GAGS
    1500 : "トゥーンアップを使おう！",
    1501 : "トラップを使おう！",
    1502 : "おとりを使おう！",
    1503 : "サウンドを使おう！",
    1504 : "投げを使おう！",
    1505 : "みずでっぽうを使おう！",
    1506 : "ドロップを使おう!",

    # Battle TAUNTS
    1520 : "ロックンロール♪",
    1521 : "きっと痛いんだろうね。",
    1522 : "そうれっ！",
    1523 : "お届けもので～す！",
    1524 : "まだだいじょうぶなの？！",
    1525 : "おー、こわいこわい。",
    1526 : "へぇー、そうくるんだ。",

    # Battle STRATEGY
    1550 : "トラップを使うよ！",
    1551 : "おとりを使うよ！",
    1552 : "ドロップを使うよ！",
    1553 : "違うギャグを使ったほうがいいよ。",
    1554 : "みんなで同じコグを狙おう！",
    1555 : "違うコグを選んだほうがいいよ。",
    1556 : "一番弱いコグから先に倒そう！",
    1557 : "先に手ごわいコグをやっつけよう！",
    1558 : "パワフルなギャグは後に取っておいたら？",
    1559 : "おとりにかかっているコグに「サウンド」は使わないで！",

    # Gag Shop
    1600 : "ギャグはじゅうぶんある。",
    1601 : "もっとジェリービーンが必要なんだ。",
    1602 : "同感！",
    1603 : "急いで！",
    1604 : "もうひとつ？",
    1605 : "またプレイするの？",
    1606 : "またプレイしよう！",

    # Factory
    1700 : "ひとまず分かれよう！",
    1701 : "みんな一緒にいよう！",
    1702 : "コグたちをやっつけよう！",
    1703 : "スイッチの上に乗って！",
    1704 : "ドアの先に進んで！",

    # Sellbot Factory
    1803 : "今、メインゲートにいるよ！",
    1804 : "今、ロビーにいるよ！",
    1805 : "ロビーの先にいるよ。",
    1806 : "ロビーの前にいるよ。",
    1807 : "ギアルームにいるよ。",
    1808 : "ボイラールームにいるよ！",
    1809 : "東の細い通路にいるよ！",
    1810 : "ペンキルームにいるよ！",
    1811 : "ペンキルームの奥の倉庫にいるよ！",
    1812 : "西の細い通路にいるよ！",
    1813 : "パイプルームにいるよ！",
    1814 : "パイプルームの近くにいるよ！",
    1815 : "ダクトルームにいるよ！",
    1816 : "サイドゲートにいるよ！",
    1817 : "廊下にいるよ！",
    1818 : "ヨウガンルームの手前にいるよ！",
    1819 : "ヨウガンルームにいるよ！",
    1820 : "ヨウガンルームの倉庫にいるよ！",
    1821 : "西の細い通路にいるよ！",
    1822 : "オイルルームにいるよ！",
    1823 : "倉庫の見張り台にいるよ！",
    1824 : "倉庫にいるよ！",
    1825 : "ペンキルームの外にいるよ！",
    1827 : "オイルルームの外にいるよ！",
    1830 : "東コントロールルームだよ！",
    1831 : "西コントロールルームだよ！",
    1832 : "工場長のところにいるよ！",
    1833 : "東のサイロにいるよ！",
    1834 : "西のサイロの上にいるよ！",
    1835 : "中央のサイロにいるよ！",
    1836 : "西のサイロにいるよ！",
    1837 : "東のサイロの上にいるよ！",
    1838 : "東タワーの通路にいるよ！",
    1840 : "西タワーの屋上にいるよ！",
    1841 : "東タワーの屋上にいるよ！",
    1860 : "西エレベーターのところにいるよ！",
    1861 : "東エレベーターのところにいるよ！",

    # Sellbot Factory continued
    1903 : "メインゲートで会おう！",
    1904 : "ロビーで会おうよ！",
    1905 : "ロビーの先で会おう！",
    1906 : "ロビーの手前で会おう！",
    1907 : "ギアルームで会おう！",
    1908 : "ボイラールームで会おう！",
    1909 : "東の細い通路で会おう！",
    1910 : "ペンキルームで会おう！",
    1911 : "ペンキルーム倉庫で会おう！",
    1912 : "西の細い通路で会おう！",
    1913 : "パイプルームで会おう！",
    1914 : "パイプルームの階段で会おう！",
    1915 : "ダクトルームで会おう！",
    1916 : "サイドゲートで会おう！",
    1917 : "廊下で会おう！",
    1918 : "ヨウガンルームの手前で会おう！",
    1919 : "ヨウガンルームの中で会おう！",
    1920 : "ヨウガンルームの倉庫で会おう！",
    1921 : "西の細い通路で会おう！",
    1922 : "オイルルームで会おう！",
    1923 : "倉庫の見張台で会おう！",
    1924 : "倉庫で会おうよ！",
    1925 : "ペンキルームの外で会おう！",
    1927 : "オイルルームの外で会おう！",
    1930 : "東タワーのコントロールルームに来て！",
    1931 : "西タワーのコントロールルームに来て！",
    1932 : "メインタワーのコントロールルームに来て！",
    1933 : "東タワーで会おう！",
    1934 : "西タワーの上で会おう！",
    1935 : "メインタワーの屋上で会おう！",
    1936 : "西タワーで会おう！",
    1937 : "東タワーで会おう！",
    1938 : "東タワーの通路で会おう！",
    1940 : "西タワーの屋上で会おう！",
    1941 : "東タワーの屋上で会おう！",
    1960 : "西タワーのエレベーターで会おう！",
    1961 : "東タワーのエレベーターで会おう！",

    # These are used only for the style settings in the OptionsPage
    # These should never actually be spoken or listed on the real speed chat
    2000 : "むらさき",
    2001 : "あお",
    2002 : "うすちゃ",
    2003 : "あおみどり",
    2004 : "みどり",
    2005 : "きいろ",
    2006 : "オレンジ",
    2007 : "あか",
    2008 : "ピンク",
    2009 : "ちゃいろ",

    # CFO battle
    2100 : "クレーンを操作しよう！",
    2101 : "クレーンを操作してもいい？",
    2102 : "クレーンの練習をしないと。",
    2103 : "動いていないグーンをひろおう！",
    2104 : "マネーマネーにグーンを投げよう。",
    2105 : "金庫を投げて！今だ！",
    2106 : "今は金庫を投げないで！",
    2107 : "金庫は彼のヘルメットを落とすよ！",
    2108 : "金庫は彼の新しいヘルメットになるよ。",
    2109 : "金庫に近づけないよ。",
    2110 : "グーンに近づけないよ。",

    2120 : "グーンを止めて！",
    2121 : "グーンの動きを止めるね。",
    2122 : "グーンを止める練習をしないと。",
    2123 : "近くにいてね。",
    2124 : "動きつづけて！",
    2125 : "動きつづけないと。",
    2126 : "助けが必要なトゥーンを探して！",

    2130 : "たからものをキープして。",
    2131 : "たからものを取って！",
    2132 : "たからものが必要だ。",
    2133 : "気をつけて！",

    # CJ battle
    2200 : "「てんびん」をねらおうね！",
    2201 : "こっちで「てんびん」をねらうね。",
    2202 : "「てんびん」をねらうの、手伝って！",
    2203 : "コグ達を気絶させないと。",
    2204 : "コグを気絶させるね。",
    2205 : "コグを相手にするの、手伝って！",
    2206 : "もっと「ショウコ」が必要なんだ！",
    2207 : "上の段のイスをねらうね！",
    2208 : "下の段のイスをねらうね！",
    2209 : "ねらえないから、ちょっとどいてくれるかな？",
    2210 : "みんなにトゥーンアップするね。",
    2211 : "ボーナスウエイトがないんだ！",
    2212 : "１ボーナスウエイトを持ってるよ。",
    2213 : "２ボーナスウエイトを持ってるよ。",
    2214 : "３ボーナスウエイトを持ってるよ。",
    2215 : "４ボーナスウエイトを持ってるよ。",
    2216 : "５ボーナスウエイトを持ってるよ。",
    2217 : "６ボーナスウエイトを持ってるよ。",
    2218 : "７ボーナスウエイトを持ってるよ。",
    2219 : "８ボーナスウエイトを持ってるよ。",
    2220 : "９ボーナスウエイトを持ってるよ。",
    2221 : "１０ボーナスウエイトを持ってるよ。",
    2222 : "１１ボーナスウエイトを持ってるよ。",
    2223 : "１２ボーナスウエイトを持ってるよ。",
    
    # CEO battle
    2300 : "左側のコグたちにはこんでくれる？",
    2301 : "左側のコグたちにはこぶね。",
    2302 : "右側のコグたちにはこんでくれる？",
    2303 : "左側のコグたちにはこぶね。",
    2304 : "前の方のコグたちにはこんでくれる？",
    2305 : "前の方のコグたちにはこぶね。",
    2306 : "後の方のコグたちにはこんでくれる？",
    2307 : "後の方のコグたちにはこぶね。",
    2308 : "ボトルでこうげきしてくれる？",
    2309 : "ボトルでこうげきするよ。",
    2310 : "ゴルフでこうげきしてくれる？",
    2311 : "ゴルフでこうげきするよ。",
    2312 : "このテーブルはまかせて！",
    2313 : "このテーブルをお願い！",
    2314 : "いつも同じコグにはこんでみよう。",
    2315 : "いそごう、コグがハラペコだ～！",
    2316 : "ゲラがひくいナカマにスナックをとっておこう。",
    2317 : "落っこちちゃう前にスナックをとっておこう。",
    
    
    #Kart Racing Phrases
    #IMPORTANT: if you change numbers or add/subtract lines here than be
    # sure to adjust the kart racing menu guid dict below
    # Invites/Destinations
    3010 : "誰かレースしたい？",
    3020 : "レースしよう！",
    3030 : "レースしたい？",
    3040 : "さあ、カートをみせびらかそう！",
    3050 : "チケットがないんだ…",
    3060 : "もう一度レースしよう！",
    3061 : "またレースしない？",

    #Places
    3150 : "カートショップに行かないと！",
    3160 : "レーストラックに行こう！",
    3170 : "ピットにいって一緒にカートを見せびらかそう！",
    3180 : "これからピットにいってカートを見せるんだ！",
    3190 : "レース場に集まろう！",
    3110 : "カートショップに集まろう！",
    3130 : "どこで集まろうか？",
    
    #Races
    3200 : "どこでレースがしたい？",
    3201 : "違うレースを選ぼう！",
    3210 : "練習のレースをしょう！" ,
    3211 : "さあ、バトルレースのはじまり！", 
    3220 : "スクリュースタジアムのレースがいいなぁ。",
    3221 : "さびさびレースウェイのレースがいいなぁ。",
    3222 : "やっぱシティーサーキットでレースでしょ。",
    3223 : "きりもみコロシアムが好き!",
    3224 : "エアボーン・エーカースが好き!",
    3225 : "ブリザード・ブルバードが好き!",
    3230 : "スクリュースタジアムでレースしよう！",
    3231 : "さびさびレースウェイでレースしよう！",
    3232 : "シティーサーキットでレースしよう！",    
    3233 : "きりもみコロシアムでレースしよう!",
    3234 : "エアボーン・エーカースでレースしよう!",
    3235 : "ブリザード・ブルバードでレースしよう!",    
    
    #Tracks    
    3600 : "どのトラックでレースしたい？",
    3601 : "トラックを選んで！",
    3602 : "違うトラックでレースできる？",
    3603 : "同じトラックはやめようか。",
    3640 : "１番トラックでレースしたいな。",
    3641 : "２番トラックでレースしたいな。",
    3642 : "３番トラックでレースしたいな。",
    3643 : "４番トラックでレースしたいな。",
    3660 : "１番トラックではレースしたくないな。",
    3661 : "２番トラックではレースしたくないな。",
    3662 : "３番トラックではレースしたくないな。",
    3663 : "４番トラックではレースしたくないな。",            
    
    #Compliments
    3300 : "ワオ！キミって速いねー！",
    3301 : "キミの速さにはかなわないや！",
    3310 : "いいレースだったね！",
    3320 : "キミのカートはとってもいいね。",
    3330 : "いいレースだったよ。",
    3340 : "キミのカートはかっこいいね！",
    3350 : "キミのカートはすばらしいね！",
    3360 : "本当におしゃれなカートだね！",

    #Taunts (commented out taunts are for possible purchase lines)
    #3400 : "けむりまみれだね！",
    3400 : "レースするのがこわいかな？",
    3410 : "ゴールで会おう！",
    #3420 : "キミはとってものんびりだね。",
    3430 : "イナズマのように速いのさ！",
    #3440 : "光より速く走れるのさ！",
    3450 : "キミはきっと追いつかないよ！",
    3451 : "キミには負けないよ！",
    3452 : "だれも追いつけないのさ！",
    3453 : "のんびりさん、もっと急いで！",
    3460 : "もう一度、トライする？",
    3461 : "キミ、ついてるねー！",
    3462 : "おーっと！あぶなかった！",
    3470 : "ワオ！キミに負けるかと思ったよ！",
    #3500 : "この走りを見ててね！",
    #3510 : "タイヤを見てごらん！",
    #3540 : "ブルン、ブルーン！",
    #3560 : "コグたちのほうが速いんじゃないの？",
    #3600 : "わーい、一番早いぞ！",


    # Golf phrases

    # Play
    4000 : "Let's play minigolf!",
    4001 : "Let's play again!",
    4002 : "Want to golf?",

    # Courses
    4100 : "『ウォーク・イン・パー』でプレイしよう。",
    4101 : "『ホール・サム・ファン』でプレイしよう。",
    4102 : "『ザ・ホール・カブードル』でプレイしよう。",
    4103 : "このコースはかんたんすぎるかも。",
    4104 : "このコースはむずかしすぎるかも。",
    4105 : "うん、このコースはちょうどいいね。",

    # Tips
    4200 : "もっと左側に立ってごらん。",
    4201 : "もっと右側に立ってごらん。",
    4202 : "まんなかに立つとイイみたいだよ。",
    4203 : "強めに打ってごらん。",
    4204 : "軽めに打ってごらん。",
    4205 : "もうちょっと左だよ。",
    4206 : "もうちょっと右だよ。",
    4207 : "そのまま正面に向けて打てばイイかも。",

    # Comments
    4300 : "うぁ～、おしい！",
    4301 : "ナイスショット！",
    4302 : "今のはラッキーだったね☆",
    4303 : "やりなおしたいよ・・・",
    4304 : "オッケーだよね？",
    4305 : "ふぁ～～～っ！！",
    4306 : "お静かにねがいます。",
    4307 : "いい試合だったね☆",
    
    
    # Promotional Considerations
    10000 : "キミの一票が大事さ！",
    10001 : "だれに投票しているの？",
    10002 : "そりゃあ、ニワトリ！",
    10003 : "えっ、誰かって？ウッシッシ…",
    10004 : "サルに投票スル？",
    10005 : "はちみつが好きだから、クマに投票するよ！",
    10006 : "ブタってかわいいよね！",#Think big! Vote Pig!
    10007 : "ヤギにしよう！",#Vote Goat - and that's all she wrote!

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
    21000: 'おーい、こっちこっち！',
    21001: 'こっちにおいで！',
    21002: 'まて！',
    21003: 'いいぞ！',
    21004: 'いいこだね！',
    21005: 'よくやった！',
    21006: 'ちょっと待ってね・・・',

    # Pet/Doodle Tricks
    21200: 'ジャンプ！',
    21201: '立って！',
    21202: 'やられた！',
    21203: 'ごろごろ！',
    21204: '宙返り', #★backflip
    21205: 'ダンス！',
    21206: 'おしゃべり！',

    # PIRATES
    50001 : 'オウ！',
    50002 : 'ンヤ！',
    50003 : 'アーッ！',#★Arr
    50004 : "アイ、アイ、キャプテン！",
    50005 : 'Ok',

    # EXPRESSIONS
    50100 : "アホイ！",
    50101 : "お～い！",
    50102 : "待て！",
    50103 : "どいたどいたっ！",
    50104 : "しまった！",
    50105 : "そりゃないよ！",#Well blow me down!
    50106 : "ヨーホーホー！",
    50107 : "アイ、アイ、キャプテン！",
    50108 : "度胸あるな！",#Walk the plank!
    50109 : "かかってこい！",#Come about!
    50110 : "死人に口なし…",
    

    # EXPRESSIONS - GREETINGS
    50700 : "Ahoy!",
    50701 : "Ahoy, mate!",
    50702 : "Yo-Ho-Ho",
    50703 : "Avast!",
    50704 : "Hey Bucko.",

    # EXPRESSIONS - GOODBYES
    50800 : "Until next time.",
    50801 : "May fair winds find ye.",
    50802 : "Godspeed.",


    # EXPRESSIONS - FRIENDLY
    50900 : "How are ye, mate?",
    50901 : "",

    # EXPRESSIONS - HAPPY
    51000 : "It's like the sky is raining gold doubloons!",
    51001 : "May a stiff wind be at our backs, the sun on our faces and our cannons fire true!",

    # EXPRESSIONS - SAD
    51100 : "I be sailing some rough waters today.",

    # EXPRESSIONS - SORRY
    51200 : "Me apologies, mate.",
    51201 : "Sorry.",
    51202 : "Sorry, I was busy before.",
    51203 : "Sorry, I already have plans.",
    51204 : "Sorry, I don't need to do that.",

    # COMBAT
    51300 : "Attack the weakest one!",
    51301 : "Attack the strongest one!",
    51302 : "Attack me target!",
    51303 : "I be needing help!",
    51304 : "I can't do any damage!",
    51305 : "I think we be in trouble.",
    51306 : "Surround the most powerful one.",
    51307 : "We should retreat.",
    51308 : "Run for it!",

    # SEA COMBAT
    51400 : "Fire a Broadside!",
    51401 : "Port Side! (left)",
    51402 : "Starboard Side! (right)",
    51403 : "Incoming!",
    51404 : "Come about!",
    51405 : "Broadside! Take Cover!",
    51406 : "To the Cannons!",
    51407 : "Open fire!",
    51408 : "Hold yer fire!",
    51409 : "Aim for the masts!",
    51410 : "Aim for the hull!",
    51411 : "Prepare to board!",
    51412 : "She's coming about.",
    51413 : "Ramming speed!",
    51414 : "We've got her on the run.",
    51415 : "We be taking on water!",
    51416 : "We can't take anymore!",
    51417 : "I don't have a shot!",
    51418 : "Let's find port for repair.",
    51419 : "Man overboard!",
    51420 : "Enemy spotted.",
    51421 : "Handsomely now, mates!",

    # PLACES
    50400 : "Let's set sail.",
    50401 : "Let's get out of here.",


    # PLACES - LETS SAIL...
    51500 : "Let's sail to Port Royal.",
    51501 : "Let's sail to Tortuga.",
    51502 : "Let's sail to Padres Del Fuego.",
    51503 : "Let's sail to Devil's Anvil.",
    51504 : "Let's sail to Kingshead.",
    51505 : "Let's sail to Isla Perdida.",
    51506 : "Let's sail to Cuba.",
    51507 : "Let's sail to Tormenta.",
    51508 : "Let's sail to Outcast Isle.",
    51509 : "Let's sail to Driftwood.",
    51510 : "Let's sail to Cutthroat.",
    51511 : "Let's sail to Rumrunner's Isle.",
    51512 : "Let's sail to Isla Cangrejos.",
    
    # PLACES - LETS HEAD TO...
    51600 : "Let's head into town.",
    51601 : "Let's go to the docks.",
    51602 : "Let's head to the tavern.",    

    # PLACES - LETS HEAD TO... - PORT ROYAL
    51800 : "Let's go to Fort Charles.",
    51801 : "Let's go to the Governor's Mansion.",

    # PLACES - WHERE IS ..?
    52500 : "Where be I, mate?",

    # DIRECTIONS
    51700 : "Yer already there.",
    51701 : "I don't know.",
    51702 : "Yer on the wrong island.",
    51703 : "That's in town.",
    51704 : "Look just outside of town.",
    51705 : "Ye will have to search through the jungle.",
    51706 : "Deeper inland.",
    51707 : "Oh, that be by the coast.",

    # Insults
    50200 : "このドブネズミ！",
    50201 : "落ち着きねえな！",
    50202 : "カンオケで会おう！",
    50203 : "ふらちな奴め！",
    50204 : "この「ぬすっと」が！", #Land lubber
    50205 : "Addle-minded fool!",
    50206 : "You need a sharp sword and sharper wits.",
    50207 : "Ye be one doubloon short of a full hull mate!",
    50208 : "Watch yer tongue or I'll pickle it with sea salt!",

    # Compliments
    50300 : "Nice shootin' matie!",
    50301 : "A well placed blow!",
    50302 : "Nice shot!",
    50303 : "Well met!",
    50304 : "We showed them!",
    50305 : "Yer not so bad yerself!",
    50306 : "A fine plunder haul!",

    # Places
    50400 : "ここはどこだ？！",
    50401 : "町に向かおう！",
    50402 : "港に出向こう！",
    50403 : "出港の準備をしよう！",
    50404 : "バーに行こう！",

    # Adventures
    50500 : "Let's set sail!",
    50501 : "Get onboard!  We're leaving port!",
    50502 : "Let's get to plunderin!",
    50503 : "Let's sail to Bilgewater!",
    50504 : "Let's sail to Port Royale!",
    50505 : "Let's use a Treasure Map!",
    50506 : "Let's head back to Port!",

    # Ships
    50600 : "Port side! (left)",
    50601 : "Starboard side! (right)",
    50602 : "Incoming!",
    50603 : "Broadside! Take cover!",
    50604 : "Arm your cannons!",
    50605 : "Open fire!",
    50606 : "Hold your fire!",
    50607 : "Aim for the masts!",
    50608 : "Aim for the hull!",
    50609 : "Prepare to board!",
    50610 : "She's comin' about!",
    50611 : "Fire a broadside!",
    50612 : "Ramming speed!",
    50613 : "Arrr! We're going in!",
    50614 : "We've got her on the run!",
    50615 : "We're taking on water!",
    50616 : "We can't take anymore!",
    50617 : "We need to repair!",
    50618 : "Retreat!",
    50619 : "Man overboard!",
    50620 : "Avast! A dirty Navy Clipper!",

    # Greetings
    60100 : "ハーイ！",
    60101 : "ハロー！",
    60102 : "ヘイ！",
    60103 : "ヨッ！",
    60104 : "ハーイ、みんな！",
    60105 : "元気？",
    60106 : "調子はどう？",

    # Bye
    60200 : "バーイ！",
    60201 : "後で！",
    60202 : "またな！",
    60203 : "すぐ戻るからな！",
    60204 : "行かないと！",

    # Happy
    60300 : ":-)",
    60301 : "クール！",
    60302 : "イェーッ！",
    60303 : "ハハッ！",
    60304 : "いいねぇ～！",
    60305 : "オー、イェー！",
    60306 : "いかしてるねぇ！",
    60307 : "ファンキー！",
    60308 : "すんげぇー！",
    60309 : "ワオ！",

    # Sad
    60400 : ":-(",
    60401 : "ちぇっ！",
    60402 : "くっそー！",
    60403 : "痛っ！",
    60404 : "こいつー！",

    # Places
    60500 : "キミはどこにいるの～？",
    60501 : "ゲートウェイストアに行くぞ！", #★
    60502 : "ディスコホールに行くぞ！",
    60503 : "トゥーンタウンに行くぞ！",
    60504 : "カリブの海賊に行くぞ！", #★

    # Animated Emotes
    60505 : "Flip coin",
    60506 : "Dance",
    60507 : "Chant 1",
    60508 : "Chant 2",
    60509 : "Dance a jig",
    60510 : "Sleep",
    60511 : "Flex",
    60512 : "Play Lute",
    60513 : "Play Flute",
    60514 : "Frustrated",
    60515 : "Searching",
    60516 : "Yawn",
    60517 : "Kneel",
    60518 : "Sweep",
    60519 : "Primp",
    60520 : "Yawn",
    60521 : "Dance",
    60522 : "No",
    60523 : "Yes",
    60524 : "Laugh",
    60525 : "Clap",
    60526 : "Smile",
    60527 : "Anger",
    60528 : "Fear",
    60529 : "Sad",
    60530 : "Celebrate",
    60668 : "Celebrate",
    60669 : "Sleep",
    60602 : "Angry",
    60614 : "Clap",
    60622 : "Scared",
    60640 : "Laugh",
    60652 : "Sad",
    60657 : "Smile",
    60664 : "Wave",
    60665 : "Wink",
    60666 : "Yawn",
    60669 : "Sleep",
    60670 : "Dance",
    60676 : "Flirt",
    60677 : "Zombie dance",
    60678 : "Noisemaker",

    # Valentines day emote string options
    60671 : "Hello, Im a Pirate, and Im here to steal your heart.",
    60672 : "I just found the treasure Ive been searching for.",
    60673 : "If you were a booger, Id pick you first.",
    60674 : "Come to Tortuga often?",
    60675 : "Do you have a map?  I just keep getting lost in your eyes.",

    65000 : "Yes",
    65001 : "No",
    }

# Emote IDs - These are used in SC to determine if a msg is a animated emote
Emotes_Root = "EMOTES"
Emotes_Dances = "Dances"
Emotes_General = "General"
Emotes_Music = "Music"
Emotes_Expressions = "Emotions"
Emote_ShipDenied = "Cannot emote while sailing."
Emote_MoveDenied = "Cannot emote while moving." 
Emote_CombatDenied = "Cannot emote while in combat."
Emote_CannonDenied = "Cannot emote while using a cannon."
Emote_SwimDenied = "Cannot emote while swimming."
Emote_ParlorGameDenied = "Cannot emote while playing a parlor game."
Emotes = (60505, 60506, 60509, 60510, 60511, 60516, 60519, 60520, 60521, 60522, 60523, 60524, 60525, 60526, 60527, 60528, 60529, 60530, 60602, 60668, 60614, 60622, 60640, 60644, 60652, 60657, 60664, 60665, 60666, 60669, 60612, 60661, 60645, 60629, 60641, 60654, 60630, 60670, 60633,
          # Valentines Day Emote
          60676,
          # Halloween Emote
          60677,
          # Yes/No
          65000, 65001,
          # Kneel
          60517,
          # New Years Emote
          60678,
          )

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
    10 : "しょうがないね。",
    20 : "あたりまえさ！",
    30 : "それはまあ当然でしょ！",
    40 : "よっしゃー！",
    50 : "ドンピシャ！",
    60 : "どうした？",
    70 : "もっちろん！",
    80 : "やったあ！",
    90 : "うっそぉ！",
    100 : "いいんじゃない？",
    110 : "へんなの！",
    120 : "すごい!",
    130 : "マジで～！？",
    140 : "心配ないよ。",
    150 : "グルルルルル～!",    
    160 : "なんか新しいものない？",
    170 : "おおっとお！",
    180 : "またあしたね。",
    190 : "またこんどね。",
    200 : "またね！",
    210 : "それでは、まったね～",
    220 : "そろそろ行かなくっちゃ。",
    230 : "どうかなぁ…",
    240 : "なんだこりゃ！",
    250 : "おおっ、それはいいね！",
    260 : "やったぜ！",
    270 : "おねがい！",
    280 : "ほんとにほんとにありがとう！",
    290 : "おしゃれだね！",
    300 : "しつれい！",
    310 : "やぁ、いらっしゃいませ～",
    320 : "それそれ、それだよ！",
    330 : "かっちょいい！",
    340 : "うぅ～～ん！シビれるぅ！",
    350 : "おおお！すごいね！",
    360 : "ふざけるのもいいかげんにしてよ！",
    370 : "どうしたの～？",
    380 : "おや、トラブルかな？",
    390 : "おっ、ダレかと思えばキミかぁ。",
    400 : "楽しいイベントを見にいかなくちゃ！",
    410 : "もう、おどかさないでよ。",
    420 : "あきらめちゃだめだよ！",
    430 : "キミはカモネギだよ、ほんと。",
    440 : "はぁ～？",
    450 : "まったくだよ！",
    460 : "かーわいーい！",
    470 : "それ、サイコー！",
    480 : "イェイ、ベイベ！",
    490 : "できるもんなら、つかまえてごらん！",
    500 : "はじめにパワーをもらわなくちゃ。",
    510 : "もっとゲラゲラポイントが必要だよ。",
    520 : "すぐ戻ってくるね。",
    530 : "おなかすいたよ。",
    540 : "ハイハイ！",
    550 : "ねむいよ…",
    560 : "準備ＯＫ！",
    570 : "たいくつだよ～",
    580 : "これ好き！",
    590 : "面白ろかったね！",
    600 : "ジャンプ！",
    610 : "ギャグある？",
    620 : "どうかしたの？",
    630 : "ゆっくりやろうね。",
    640 : "勝つには、ゆっくり、かくじつに！",
    650 : "タッチダウン！",
    660 : "レディ？",
    670 : "セット！",
    680 : "ゴー！",
    690 : "こっちへ行こう！",
    700 : "キミの勝ち！",
    710 : "さんせ～い。",
    720 : "はんた～い。",
    730 : "仲間にいれて！",
    740 : "私はいいや、やらない。",
    750 : "ここにいてね、戻ってくるから。",
    760 : "はやかったね！",
    770 : "あれ見た？",
    780 : "あのにおいは何？",
    790 : "やなかんじ！",
    800 : "気にしないよ。",
    810 : "まさに必要としてるものだよ。",
    820 : "よーし、おっぱじめちゃうぞ～！",
    830 : "こっちだよ、みんな！",
    840 : "はぁ？",
    850 : "行きますよ～",
    860 : "聞こえたよ！",
    870 : "え、私に話してるの？",
    880 : "ありがとう。今週はずっとここにいるよ。",
    890 : "う～む",
    900 : "これがいい。",
    910 : "やった！",
    920 : "それは自分のだよ！",
    930 : "とっておいて",
    940 : "さがって、これは危険かもしれない。",
    950 : "心配ないよ！",
    960 : "あーあ！",
    970 : "ヒュー！",
    980 : "おおっ！",
    990 : "乗って、乗って！",
    1000 : "かっちょいーね！",
    1010 : "しないほうがいいんじゃない？",
    # Series 2
    2000 : "いい年して!",
    2010 : "会えてうれしいよ！",
    2020 : "どうぞごえんりょなく。",
    2030 : "トラブルをさけてるの？",
    2040 : "おそくなっても、来てくれたらうれしいな!",
    2050 : "ブラボー!",
    2060 : "でもみんな、マジでさ...",
    2070 : "仲間に入る？",
    2080 : "またあとでね!",
    2090 : "気が変わっちゃったの?",
    2100 : "さあ、来い!",
    2110 : "わあ、大変だ!",
    2120 : "お知り合いになれて、光栄です。",
    2130 : "やりたくないから、やらないよ！",
    2140 : "そうはさせないよ！",
    2150 : "見捨てないで！",
    2160 : "あまり期待しないでね。",
    2170 : "知らないよ！",
    2180 : "簡単に言うね。",
    2190 : "いいかげんにして！",
    2200 : "すばらしい！",
    2210 : "こんなところで会うなんて！",
    2220 : "勘弁してよ～！",
    2230 : "そういってくれると、うれしいよ！",
    2240 : "やれるもんなら、やってみな！",
    2250 : "行け～！",
    2260 : "よくできました！",
    2270 : "会えてうれしいよ！",
    2280 : "もう行かなくちゃ。",
    2290 : "先を急がなきゃ。",
    2300 : "そこにいてね。",
    2310 : "ちょっと待っててね。",
    2320 : "楽しんできてね！",
    2330 : "楽しんでね！",
    2340 : "時間がないよ！",
    2350 : "もう少しのしんぼうだよ！",
    2360 : "たわごとを！",
    2370 : "信じらんなーい！",
    2380 : "それはどうかなー。",
    2390 : "すまないね。",
    2400 : "キミの気持ちはよくわかった。",
    2410 : "たぶんね。",
    2420 : "やめたほうが、いいんじゃない？",
    2430 : "そのセリフ、いいねー。",
    2440 : "やめとけば？",
    2450 : "よろこんで！",
    2460 : "友達を助けてるの。",
    2470 : "ずっと待ってるんだ。",
    2480 : "想像してみて！",
    2490 : "間一髪...",
    2500 : "まだまだ続くよ。",
    2510 : "ガンガンいこうよ！",
    2520 : "仲良くしようね。",
    2530 : "あいにくの空模様だね。",
    2540 : "サッサとやっちゃおう！",
    2550 : "くつろいでいって。",
    2560 : "またの機会にね。",
    2570 : "仲間に入れてくれる？",
    2580 : "いいところだね。",
    2590 : "お話してくれて、ありがとう。",
    2600 : "まちがいないね。",
    2610 : "うそでしょ！",
    2620 : "ありえない！",
    2630 : "頭来ちゃう！",
    2640 : "かまわないよ。",
    2650 : "ようし！",
    2660 : "ハイ、チーズ！",
    2670 : "なんだって？",
    2680 : "ジャジャーン！",
    2690 : "無理しないでね。",
    2700 : "バイバイ、またね！",
    2710 : "ありがとう。でも遠慮しとくね。",
    2720 : "やってくれたね！",
    2730 : "ハハハ、それおもしろい。",
    2740 : "そのとおり！",
    2750 : "コグが侵入したぞ！",
    2760 : "じゃあね、バイバイ。",
    2770 : "気をつけて！",
    2780 : "よくできたね！",
    2790 : "どうなってる？",
    2800 : "何かあったの？",
    2810 : "構わないよ。",
    2820 : "了解しました！",
    2830 : "わかった。",
    2840 : "たのんだよ。",
    2850 : "もう行っちゃうの？",
    2860 : "笑えるねー！",
    2870 : "右をお願い。",
    2880 : "もう終わりだよ！",
    # Series 3
    3000 : "おっしゃるとおり。",
    3010 : "仲間に入ってもいい？",
    3020 : "お勘定おねがいします。",
    3030 : "安心できないね。",
    3040 : "やってもいい？",
    3050 : "気にしないで！",
    3060 : "知らないのー？",
    3070 : "おかまいなく。",
    3080 : "見つけた！",
    3090 : "オシャレだね！",
    3100 : "気にしないで！",
    3110 : "ついてくる？",
    3120 : "よかったね！",
    3130 : "やれやれ。",
    3140 : "またね！",
    3150 : "しっかり！",
    3160 : "あー、まただ。",
    3170 : "どう？",
    3180 : "よかった？",
    3190 : "そう思う。",
    3200 : "ちがうと思うよ。",
    3210 : "あとで連絡するよ。",
    3220 : "ねぇ、教えてよ！",
    3230 : "いそがしいの。",
    3240 : "うそじゃないって！",
    3250 : "開いた口がふさがらない。",
    3260 : "元気出して！",
    3270 : "教えてね！",
    3280 : "それ行けー！",
    3290 : "確かに、同感。",
    3300 : "てきぱきしてる！",
    3310 : "あっというまだったね。",
    3320 : "ノーコメント。",
    3330 : "そう来なくちゃ！",
    3340 : "かまわないよ。",
    3350 : "会えてうれしいよ。",
    3360 : "よーし！",
    3370 : "もちろん。",
    3380 : "ほんとにありがとう。",
    3390 : "そっちのほうがいいかな。",
    3400 : "そいつはいい！",
    3410 : "とうとう自分の出番かな！",
    3420 : "信じて！",
    3430 : "また次回に。",
    3440 : "ちょっと待って！",
    3450 : "やってくれるね！",
    3460 : "どうしてここに？",
    3470 : "どうしたの？",
    3480 : "なにかニュースは？",
    3490 : "お先にどうぞ。",
    3500 : "左をお願い。",
    3510 : "お望みどおり！",
    3520 : "キミはもうおしまいだ！",
    3530 : "いいかげんにして！",

    # Series 4
    4000 : "トゥーンはサイコー！",
    4010 : "コグはサイテー！",
    4020 : "トゥーンはナカマ！",
    4030 : "どうよ、調子は！",
    4040 : "かたじけない。",
    4050 : "ワンちゃん、ついてきて！",
    4060 : "おひるね、するよ！",
    4070 : "ちょっとイライラしてたんだ…",
    4080 : "このマチはふたりには小さいかも！",
    4090 : "気を引きしめて！",
    4100 : "引き分け！",
    4110 : "ひょっとしたらイイことあるかも。",
    4120 : "シアワセがつづきますように！",
    4130 : "ここでボーッとするのが好きなんだ。",
    4140 : "いそいで逃げろ！",
    4150 : "何か気になることでもあるの？",
    4160 : "落ち着くなぁ～。",
    4170 : "すっかり元気だよ！",
    4180 : "そうだと思うよ！",
    4190 : "乗りこもう！",
    4200 : "ワイルドに行こう！",
    4210 : "久しぶりにマチに戻ったよ！",
    4220 : "悪いヤツらをつかまえよう！",
    4230 : "おてあげ！",
    4240 : "空に手をのばして！",
    4250 : "準備はバッチリだよ！",
    4260 : "しっかり手綱をにぎって！",
    4270 : "そいつはできない相談だよ。",
    4280 : "すぐに戻ってくるさ！",
    4290 : "それはややこしい問題だね。",
    4300 : "まあ、そんな落ち込まないで。",
    4310 : "ツイてる？",
    4320 : "いったい何がおこっているの？",
    4330 : "うれしいんだ！",
    4340 : "まあ、何とかなるから安心して。",
    4350 : "これでもせいいっぱい、がんばってるよ。",
    4360 : "ちょっとずるいよ～。",
    4370 : "さあ、まったりしよう！",
    4380 : "しっかり見て！",
    4390 : "そのうち、わかるよ！",
    # Series 6
    6000 : "キャンディー、チョーだい！",
    6010 : "実はとっても「あまとう」なんだ。",
    6020 : "ケーキ、まだ焼きあがってないよ。",
    6030 : "キャンディー、カンでいい？",
    6040 : "まとめ買いしちゃうの？",
    6050 : "ケーキをごちそうしちゃおう！",
    6060 : "ちゃんとケーキにデコレーションした？",
    6070 : "ケーキを２つ一緒には食べれないよ！",
    6080 : "ウキウキするなぁ～！",
    6090 : "にたりよったりだよ。",
    6100 : "ようするに甘ければいいのさ。",
    6110 : "ドーナッツみたいな目をしてどうしたの？",
    6120 : "あっ！パイが空を飛んでる！",
    6130 : "ウエハースみたいにひらべったいね。",
    6140 : "だれだ！ガムをくっつけたのは！",
    6150 : "あれ、クッキーが割れないよ。",
    6160 : "クッキーがボロボロになちゃった。",
    6170 : "チョコレート、食べたーい。",
    6180 : "そんなにアマいコトバにだまされないよ。",
    6190 : "おちこんだときにはあまいものが一番！",
    6200 : "たべちゃうぞ～！",
    6210 : "かんたんなもんさ！",
    6220 : "しつこくしないでよ！",
    6230 : "「おかし」と「えがお」があればすべてがうまくいくよ！",
    6240 : "バターみたい！",
    6250 : "アメちゃん、大好き！",
    6260 : "アイ、スクリーム？キャー！",
    6270 : "シュガ、シュガー♪",
    6280 : "コンコン…！",
    6290 : "どちらさまですか？",
    # Series 7
    7000 : "キーキーしないで！",
    7010 : "モンキーレンチって知ってる？",
    7020 : "見よう見まねでやってみて！",
    7030 : "サルっぽいね！",
    7040 : "サル知恵をはたらかそう！",
    7050 : "ウッキーウッキーしてるの。",
    7060 : "サルがさる。",
    7070 : "おっと、背中にサルが…",
    7080 : "１サル、２サル、３サル…",
    7090 : "バナナのためならエーンヤコラ！",
    7100 : "頭の中がサルでイッパイ！",
    7110 : "サルのきぐるみ、着てるの？",
    7120 : "きかザル！",
    7130 : "みザル！",
    7140 : "いわザル！",
    7150 : "バナナでスプリット！",
    7160 : "ジャングル、ぐるぐる！",
    7170 : "バナナ♪バナナ♪バーナーナッ♪",
    7180 : "チョコバナナ！",
    7190 : "くるっちゃいそう！",
    7200 : "ぶらん、ぶら～ん！",
    7210 : "ここでブラブラするのっていいよね！",
    7220 : "ア～アア～～！",
    7230 : "木のぼりしたくなるよ！",
    7230 : "スルスルスルスル～ッと",
    7240 : "ジェリービーンは木に生えないよ。",

    # Halloween
    10000 : "ゴーストタウンだね。",
    10001 : "ステキなコスチュームだね。",
    10002 : "おばけがいるみたいだよ。",
    10003 : "トリック・オア・トリート！",
    10004 : "バア！",
    10005 : "タタリじゃー！",
    10006 : "ハッピー・ハロウィン！",
    10007 : "カボチャになっちゃうぞ！",
    10008 : "おばけだぞ～！",
    10009 : "おばけみたい！",
    10010 : "気味悪い！",
    10011 : "クモはきらい！",
    10012 : "ねえ、ちょっと聞こえた？",
    10013 : "まったくついてないねぇ。",
    10014 : "びっくりした～！",
    10015 : "不気味だね！",
    10016 : "こわいよ～！",
    10017 : "何か、変な....。",
    10018 : "ガイコツがいるの？",
    10019 : "おどかしちゃった？",

    # Fall Festivus
    11000 : "べろべろば～！",
    11001 : "すねないでよ！",
    11002 : "バア～！",
    11003 : "落ち着いて！",
    11004 : "つかまえてみな！",
    11005 : "しっかりして！",
    11006 : "ガツガツ！",
    11007 : "よい休日を！",
    11008 : "あけましておめでとう！",
    11009 : "ハッピーサンクスギビング！",
    11010 : "七面鳥の日さ！",
    11011 : "いやあ、いい子にしてたかな？",
    11012 : "\"スノー\"プロブレム！",
    11013 : "イェイ、イェイ、イェーイ！",
    11014 : "雪だ！もっとふれ！",
    11015 : "集めてみよう。",
    11016 : "いい季節だね！",
    11017 : "まちがいない！",
    11018 : "順調、順調！",
    11019 : "びっくりしないでね。",

    # Valentines
    12000 : "好きです！",
    12001 : "大好きです！",
    12002 : "ハッピーバレンタインデー！",
    12003 : "なんてかわいいんだろう。",
    12004 : "きみに首ったけさ！",
    12005 : "ラブラブ！",
    12006 : "好きだよ！",
    12007 : "つきあってくれる？",
    12008 : "仲良しだよね。",
    12009 : "キミはやさしいね。",
    12010 : "かわいいね。",
    12011 : "ねぇ、ハグしてくれる？",
    12012 : "かわいい！",
    12013 : "いとしい人！",
    12014 : "バラは赤いのさ…",
    12015 : "きみはすみれのようだね。",
    12016 : "うれしい！",

    # St. Patricks Day
    13000 : "すがすがしい朝だね！",
    13001 : "セント・パトリックデーだね。",
    13002 : "緑色の洋服じゃないじゃん！",
    13003 : "アイルランドのおまじないだよ。",
    13004 : "緑の服、いいでしょ！",
    13005 : "ラッキーだね！",
    13006 : "ヨツバのクローバーだね！",
    13007 : "キミは幸運の女神だ！",

    # Summer Estate Party phrases (seasonal catalog)
    14000 : "おうちでサマー・パーティーをやろう！",
    14001 : "レッツ・パーティー！",
    14002 : "一番最後まで池にいるのはだ～れだ♪",
    14003 : "みんなでドゥードゥルのトレーニングをしよう！",
    14004 : "ドゥードゥル トレーニング開始～！",
    14005 : "キミのドゥードゥルかわいいね！",
    14006 : "キミのドゥードゥルどんなトリックができるの？",
    14007 : "キャノン・ピンボールの時間で～す♪",
    14008 : "キャノン・ピンボールは楽しいね！",
    14009 : "キミのおうち、とてもイイね！",
    14010 : "キミの庭、とてもイイね！",
    14011 : "おうちも庭もすごくイイね！",




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
PSCMenuExpressions  = "きもち"
PSCMenuGreetings = "GREETINGS"
PSCMenuGoodbyes = "GOODBYES"
PSCMenuFriendly = "FRIENDLY"
PSCMenuHappy = "HAPPY"
PSCMenuSad = "SAD"
PSCMenuSorry = "SORRY"
PSCMenuCombat = "COMBAT"
PSCMenuSeaCombat     = "SEA COMBAT"
PSCMenuPlaces     = "場所"
PSCMenuLetsSail = "LET\'S SAIL..."
PSCMenuLetsHeadTo = "LET\'S HEAD TO..."
PSCMenuHeadToPortRoyal = "PORT ROYAL"
PSCMenuWhereIs = "WHERE IS ..?"
PSCMenuWhereIsPortRoyal = "PORT ROYAL"
PSCMenuWhereIsTortuga = "TORTUGA"
PSCMenuWhereIsPadresDelFuego = "PADRES DEL FUEGO"
PSCMenuWhereIsLasPulgas = "LAS PULGAS"
PSCMenuWhereIsLosPadres = "LOS PADRES"
PSCMenuDirections = "DIRECTIONS"
PSCMenuInsults    = "いばる"
PSCMenuCompliments = "COMPLIMENTS" # TODO
PSCMenuCardGames  = "CARD GAMES"
PSCMenuPoker = "POKER"
PSCMenuBlackjack = "BLACKJACK"
PSCMenuInvitations = "INVITATIONS"
PSCMenuVersusPlayer = "VERSUS"
PSCMenuHunting = "HUNTING"
PSCMenuQuests = "QUESTS"
PSCMenuGM = "GM"



# Grandfathered Speedchat Headers
PSCMenuShips      = "SHIPS"
PSCMenuAdventures = "ADVENTURE"


# Gateway Speedchat
GWSCMenuHello     = "あいさつ"
GWSCMenuBye       = "さようなら"
GWSCMenuHappy     = "たのしい"
GWSCMenuSad       = "かなしい"
GWSCMenuPlaces     = "場所"

# NamePanel.py - PickAName/TypeAName
RandomButton = "ランダム"
TypeANameButton = "なまえをつける"
PickANameButton = "なまえをえらぶ"
NameShopSubmitButton = "提出する"
RejectNameText = "この名前は使えないよ。もう一度トライしてね。"
WaitingForNameSubmission = "キミの名前を提出しています。"

NameShopNameMaster = "NameMaster_japanese.txt"
NameShopPay = "今すぐお申しこみを!"
NameShopPlay = "無料体験"
NameShopOnlyPaid = "フルアクセスメンバーだけが、\nトゥーンのなまえを変えることができるんだ。\nキミが申しこみするまで\nキミのなまえは\nだよ。"
NameShopContinueSubmission = "なまえを申込む"
NameShopChooseAnother = "なまえをえらぶ"
NameShopToonCouncil = "キミのなまえが\n使えるかどうか調べるんだ\n" + \
                      "調べるのには数日かかるよ。\nそれまでのキミのなまえは：\n"
PleaseTypeName = "キミのなまえを入力してね:"
AllNewNames = "全ての新しいなまえは、\nトゥーン評議会のＯＫが\n必要なんだよ。"
NameShopNameRejected = "申込んだ\nなまえは\nだめだって。"
NameShopNameAccepted = "おめでとう！\n申込んだ\nなまえが\n使えるよ。"
NoPunctuation = "なまえにくとうてん（。、）は使えないよ！"
PeriodOnlyAfterLetter = "なまえでは、文字のあと以外、ピリオド(.)は使えないよ。"
ApostropheOnlyAfterLetter = "なまえでは、文字のあと以外、アポストロフィー( ' )は使えないよ。"
NoNumbersInTheMiddle = "言葉の間に数字があるのはだめだよ。"
ThreeWordsOrLess = "キミのなまえは３つの言葉かそれ以下じゃないとだめだよ。"
CopyrightedNames = (
    "ミッキー",
    "ミッキー・マウス",
    "ミニーマウス",
    "ミニー",
    "ミニー・マウス",
    "ミニーマウス",
    "ドナルド",
    "ドナルド・ダッグ",
    "ドナルドダッグ",
    "プルート",
    "グーフィー",
    )

# NameCheck.py
NCTooShort = 'なまえは全角2文字以上にしてね'
NCNoDigits = 'なまえには数字をいれないでね。'
NCNeedLetters = 'なまえのそれぞれの言葉には、文字をいれてね。'
NCNeedVowels = 'なまえのそれぞれの言葉には、母音をいれてね。'
NCAllCaps = 'なまえは全部大文字にしないでね。'
NCMixedCase = 'なまえに大文字がおおすぎるね。'
NCBadCharacter = "なまえには'%s'をいれないでね。\n\n漢字・記号・ABC…は使わないでね。"
NCRepeatedChar = "Your name has too many of the character '%s'"
NCGeneric = 'ごめん、このなまえじゃだめみたい。\n\nなまえは全角8文字以下にしてね。'
NCTooManyWords = '半角スペースは三つまでにしてね。'
NCDashUsage = "なまえにハイフン(-)は使えないよ。"
NCCommaEdge = "なまえにコンマ(,)は使えないよ。"
NCCommaAfterWord = "なまえにコンマ(,)は使えないよ。"
NCCommaUsage = 'なまえにコンマ(,)は使えないよ。'
NCPeriodUsage = 'なまえにピリオド(.)は使えないよ。'
NCApostrophes = "なまえにアポストロフィー(')は使えないよ。"

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = "%s の状態を調べています…"
AvatarDetailPanelFailedLookup = "%s の状態を調べられませんでした。"
AvatarDetailPanelPlayer = "Player: %(player)s\nWorld: %(world)s\nLocation: %(location)s"
AvatarDetailPanelOnline = "ﾛﾋﾞｰ: %(district)s\nｴﾘｱ: %(location)s"
AvatarDetailPanelOffline = "ﾛﾋﾞｰ: オフライン\nｴﾘｱ: オフライン"

# AvatarPanel.py
AvatarPanelFriends = "ともだち"
AvatarPanelWhisper = "ささやく"
AvatarPanelSecrets = "ひみつ"
AvatarPanelGoTo = "ワープ"
AvatarPanelIgnore = "むくち"
AvatarPanelStopIgnore = "Stop Ignoring"
AvatarPanelEndIgnore = "End Ignore"
AvatarPanelTrade = "Trade"
#AvatarPanelCogDetail = "部署: %s\nレベル: %s\n"
AvatarPanelCogLevel = "レベル：%s"
AvatarPanelCogDetailClose = lClose

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

KartRacingMenuSections = [
 -1,
 "場所",
 "レース",
 "トラック",
 "おせじ",
 "やじ"
]

GolfMenuSections = [
 -1,
 "コース",
 "ヒント",
 "コメント",
]

BoardingMenuSections = [
-1,
"Let's go to...",
"We're going to...",
]

WhiteListMenu = [
-1,
"WHITELIST"
]


# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "ディズニー・インターネット・グループ・カスタマーセンター（%s）に電話してください。"
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nお問い合わせ等は、ディズニー・インターネット・グループ・カスタマーセンター（%s）にお電話ください。"
TTAccountIntractibleError = "エラーが発生しました。"


def timeElapsedString(timeDelta):
    timeDelta = abs(timeDelta)
    if timeDelta.days > 0:
        if timeDelta.days == 1:
            return "1 day ago"
        else:
            return "%s days ago" % timeDelta.days

    elif timeDelta.seconds / 3600 > 0:
        if timeDelta.seconds / 3600 == 1:
            return "1 hour ago"
        else:
            return "%s hours ago" % (timeDelta.seconds / 3600)

    else:
        if timeDelta.seconds / 60 < 2:
            return "1 minute ago"
        else:
            return "%s minutes ago" % (timeDelta.seconds / 60)

# OTPGLobals stuff
def getSignFontLocale():
    return getSignFont()
