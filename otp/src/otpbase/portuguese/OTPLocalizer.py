import string
from otp.otpbase.portuguese.OTPLocalizer_Property import *

# common locations
lTheBrrrgh = 'O Brrrgh'
lDaisyGardens = 'Jardim da Margarida'
lDonaldsDock = "Porto do Donald"
lDonaldsDreamland = "Sonholândia do Donald"
lMinniesMelodyland = "Melodilândia da Minnie"
lToontownCentral = 'Centro de Toontown'
lGoofySpeedway = "Autódromo do Pateta"
lOutdoorZone = "Chip 'n Dale's Acorn Acres"
lGolfZone = "Chip 'n Dale's MiniGolf"

# common strings
lCancel = 'Cancelar'
lClose = 'Fechar'
lOK = 'OK'
lNext = 'Próximo'
lNo = 'Não'
lQuit = 'Sair'
lYes = 'Sim'

Cog  = "Cog"
Cogs = "Cogs"

# OTPDialog.py
DialogOK = lOK
DialogCancel = lCancel
DialogYes = lYes
DialogNo = lNo

# DistributedAvatar.py
WhisperNoLongerFriend = "%s saiu da sua lista de amigos."
WhisperNowSpecialFriend = "%s agora é seu amigo secreto!"
WhisperComingToVisit = "%s está vindo visitar você."
WhisperFailedVisit = "%s tentou visitar você."
WhisperTargetLeftVisit = "%s foi para algum outro lugar. Tente novamente!"
WhisperGiveupVisit = "%s não conseguiu encontrá-lo porque você está se movendo!"
WhisperIgnored = "%s está ignorando você!"
TeleportGreeting = "Oi, %s."
WhisperFriendComingOnline = "%s está entrando on-line!"
WhisperFriendLoggedOut = "%s fez logout."
WhisperPlayerOnline = "%s logged into %s"
WhisperPlayerOffline = "%s is offline."

DialogSpecial = "ooo"
DialogExclamation = "!"
DialogQuestion = "?"

# Cutoff string lengths to determine how much barking to play
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# ChatInputNormal.py
ChatInputNormalSayIt = "Dizer"
ChatInputNormalCancel = lCancel
ChatInputNormalWhisper = "Cochichar"
ChatInputWhisperLabel = "Com %s"

# ChatInputSpeedChat.py
SCEmoteNoAccessMsg = "Você não tem acesso\na esta emoção ainda."
SCEmoteNoAccessOK = lOK

ParentLogin = "Parent Login"
ParentPassword = "Senha de pais"

# ChatGarbler.py
ChatGarblerDefault = ["blá"]

# ChatManager.py
ChatManagerChat = "Chat"
ChatManagerWhisperTo = "Cochichar com:"
ChatManagerWhisperToName = "Cochichar com:\n%s"
ChatManagerCancel = lCancel
ChatManagerWhisperOffline = "%s está off-line."
OpenChatWarning = 'Você ainda não tem nenhum "Amigo secreto"! Você não pode conversar com outros Toons a menos que eles sejam seus Amigos secretos.\n\nPara se tornar Amigo secreto de alguém, clique na pessoa e selecione "Segredos" no painel de detalhes. É claro que você sempre poderá conversar com alguém pelo Chat rápido.'
OpenChatWarningOK = lOK
UnpaidChatWarning = 'Depois que você assinar o serviço, poderá ativar este botão para conversar com seus amigos usando o teclado. Até lá, você deve conversar com os outros Toons usando o Chat rápido.'
UnpaidChatWarningPay = "Assine já!"
UnpaidChatWarningContinue = "Continuar avaliação gratuita"
PaidNoParentPasswordWarning = 'Depois que você definir a sua senha de pais, poderá ativar este botão para conversar com seus amigos usando o teclado. Até lá, você deve conversar com os outros Toons usando o Chat rápido.'
PaidNoParentPasswordWarningSet = "Definir senha de pais agora!"
PaidNoParentPasswordWarningContinue = "Continuar jogando"
PaidParentPasswordUKWarning = 'Depois que o Chat estiver ativado, você poderá usar este botão para conversar com seus amigos usando o teclado. Até lá, você deve conversar com os outros Toons usando o Chat rápido.'
PaidParentPasswordUKWarningSet = "Ativar Chat agora!"
PaidParentPasswordUKWarningContinue = "Continuar jogando"
NoSecretChatWarningTitle = "Controles disponíveis aos pais"
NoSecretChatWarning = 'Para conversar com um amigo, o recurso Amigos secretos deve estar ativado. As crianças precisam que seus pais façam login e insiram a senha de pais para conhecer o recurso Amigos secretos.'
RestrictedSecretChatWarning = 'Para pegar ou digitar um segredo, você deve inserir a Senha de pais. Você pode desativar esta solicitação alterando as suas opções de Amigos secretos.'
NoSecretChatWarningOK = lOK
NoSecretChatWarningCancel = lCancel
NoSecretChatWarningWrongPassword = 'Esta não é a senha correta. Insira a senha de pais criada na compra desta conta. Não é a mesma senha usada para os jogos.'
NoSecretChatAtAllTitle = "Chat de Amigos secretos"
NoSecretChatAtAll = 'Para conversar com um amigo, o recurso Amigos secretos deve estar ativado. O recurso Amigos secretos só permite que um membro converse com outro mediante um código secreto que deve ser comunicado fora do jogo.\n\nPara ativar este recurso ou para aprender mais sobre ele, saia de Toontown e clique em "Opções da conta" na página da web de Toontown.'
NoSecretChatAtAllOK = lOK
ChangeSecretFriendsOptions = "Alterar opções de Amigos secretos"
ChangeSecretFriendsOptionsWarning = "\nInsira a senha de pais para alterar suas opções de Amigos secretos."
ActivateChatTitle = "Opções de Amigos secretos"

WhisperToFormat = "To %s %s"
WhisperToFormatName = "To %s"
WhisperFromFormatName = "%s whispers"

from pandac.PandaModules import TextProperties
from pandac.PandaModules import TextPropertiesManager

shadow = TextProperties()
shadow.setShadow(-0.025, -0.025)
shadow.setShadowColor(0,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('sombra', shadow)

red = TextProperties()
red.setTextColor(1,0,0,1)
TextPropertiesManager.getGlobalPtr().setProperties('vermelho', red)

ActivateChat = """O recurso Amigos secretos só permite que um associado converse com outro mediante um código secreto que deve ser comunicado fora do jogo. Para obter uma descrição completa do recurso, clique aqui: O recurso Amigos secretos não é moderado nem supervisionado. Se os pais deixarem seus filhos usarem a conta com o recurso Amigos secretos ativado, aconselhamos que eles mesmos supervisionem os filhos durante a brincadeira. Depois que for ativado, o recurso Amigos secretos ficará disponível até que alguém o desative. Ao ativar o recurso Amigos secretos, você reconhece que, apesar de haver alguns riscos inerentes a ele, você foi informado de todos os riscos mencionados aqui, concordando em aceitá-los."""

###

PrivacyPolicyClose = lClose
PrivacyPolicyText_Intro = [
"""
There are four different Privacy Policies.

The Privacy Policy that applies to each person will depend on when they agreed to the Privacy Policy and their age.

Version 1 is for persons who agreed before 11/06/2003.
Version 2 is for persons who agreed after that date.

The "for children" versions are for children under the age of 13; while the "for non-children" version is for everyone else.
"""
]

ActivateChatPrivacyPolicy_Button1A = "Version 1 for non-children"
ActivateChatPrivacyPolicy_Button1K = "Version 1 for children"
ActivateChatPrivacyPolicy_Button2A = "Version 2 for non-children"
ActivateChatPrivacyPolicy_Button2K = "Version 2 for children"

PrivacyPolicyText_1A = [
"""
Privacy Policy

Q1 What types of information are WDIG sites collecting, and how are the sites collecting it?

The majority of great products and services on our sites are offered without our collecting any personally identifiable information from you. You can surf WDIG's Web sites and view much of our terrific content anonymously. For instance, you can view news headlines at ABCNEWS.com without giving out any personally identifiable information.

Information You Provide
There are a few activities on our sites where the collection of personally identifiable information is necessary. Those activities include things like entering a contest or sweepstakes, making a purchase, or contacting us. When personally identifiable information is collected, you will know because you will have to fill out a form. For most activities, we collect only your name, e-mail address, birth date, gender, and zip code. When you make a purchase, we also collect your street and billing addresses, your phone number, and credit card information. Depending on what you purchase, we may also need to collect other personal information, like your clothing size.
""","""
Information Collected from You with Technology
WDIG sites collect some information about you using technology, so it may not be readily apparent to you that it is being collected. For instance, when you come to our site your IP address is collected so that we know where to send information you are requesting. An IP address is often associated with the place from which you enter the Internet like your ISP (Internet service provider), your company, or your university. This information is not personally identifiable. WDIG sites use information collected through technology to make our sites more interesting and useful to you. This includes helping advertisers on our site design advertisements our Guests might like. We normally don't combine this type of information with personally identifiable information. However, we will combine this information with personally identifiable information to identify a visitor in order to enforce compliance with our house rules or terms of service or to protect our service, site, Guests, or others.

What Are Cookies, and How Does WDIG Use Them?
Cookies are pieces of information that a Web site sends to your computer while you are viewing the Web site. These pieces of information allow the Web site to remember important information that will make your use of that site more useful. WDIG and other Internet companies use cookies for a variety of purposes. For instance, DisneyStore.com uses cookies to remember and process the items in your shopping cart, and all WDIG sites use cookies to make sure kids don't enter unmoderated chat rooms.

You can choose to have your computer warn you each time a cookie is being sent, or you can choose to turn off all cookies. You do this through your browser (like Netscape Navigator or Internet Explorer) settings. Each browser is a little different, so look at your browser Help menu to learn the correct way to modify your cookies. If you turn cookies off, you won't have access to many WDIG features that make your Web experience more efficient -- like the features mentioned above -- and some of our services will not function properly.
""","""
Q2 How does WDIG use the personally identifiable information that has been collected?

WDIG uses personally identifiable information in a limited number of ways. We use the information to complete transactions. For instance, if you purchase a fantasy team on ESPN.com, we use your information to process your order, or if you contact us for help we will use the information to contact you. We use information collected to notify you if you've won a game or contest. Information we collect is used to send you e-mail updates and newsletters about our sites. We also use the information you provide to send you WDIG e-mail promotions and special offers from our third-party sponsors.
""","""
Q3 Does WDIG share information with companies or other organizations that are not part of the WDIG family of sites?

One of the most valuable assets of our business is you. We aren't in the business of selling information about our Guests. However, if there is a value for our Guests, we will share your information or send you messages on behalf of another company as described below. We will also share information for security reasons.
Companies That Are "Standing in the Shoes" of WDIG
Sometimes we hire companies to help us deliver products or services, like a shipping company that delivers a package. In those instances, we need to share your information with them. These companies are basically "standing in the shoes" of WDIG, and they are allowed to use the information only to deliver the product or service.
""","""
Companies Offering Promotions, Products, or Services
On occasion, we offer promotions -- like sweepstakes or free subscriptions -- in conjunction with a sponsor. We will share your information with the sponsors if they need it to send you a product, such as a magazine subscription. We may share your information with those sponsors so that they can send you other special promotions they offer, but only if you give us your permission to do so, and we will share it only with that specific sponsor. In addition, WDIG occasionally sends e-mail promotions out to our Guests on behalf of third-party sponsors. In this instance, we don't share your name with the third party -- we do the mailing for them. Again, we only send these promotions to you if you've given your permission.

Content Partners
On some of our sites, we provide content that is created by a third-party partner Web site. For instance, ESPN.com provides shopping opportunities with third parties. In some instances the third-party sites will collect information in order to facilitate the transaction or to make the use of their content more productive and efficient. In these circumstances the information collected is shared between WDIG and our third-party sponsors.

Third-Party Advertisers and Network Advertisers
To help increase privacy protections for our Guests, WDIG allows advertising on our sites from only those companies that have their own privacy policy. Once you've clicked on an advertisement and have left WDIG sites, our privacy policy no longer applies. You must read the privacy policy of the advertiser to see how your personal information will be handled on their site.
""","""
In addition, many business advertisements are managed and placed on our site by third-party companies. These companies are called "network advertisers." Network advertisers collect non-personally identifiable information when you click on or scan one of their banner advertisements. The information is collected using technology, so you may not realize it's being collected. The network advertisers collect this information so that they can show you ads that are more relevant and interesting to you. If you would like to read more about network advertisers or do not want network advertisers to collect this non-personally identifiable information about you, click here.

Purchase or Sale of Businesses
Online business is still in a very early stage and is changing and evolving rapidly. As WDIG continually looks for ways to improve our business, we may buy or sell a company. If we buy or sell a business, the names collected will likely be transferred as a part of the sale. Information about registrants will be used in the aggregate. However, if we buy a business, we will honor the requests that customers made of that business regarding e-mail communications. In the event that we sell a business, we will do everything in our power to ensure that the e-mail communications requests you made of us are honored.

Organizations That Help Protect the Security and Safety of Our Guests and Our Sites
We will give out personal information as required by law, for example, to comply with a court order or subpoena; to enforce our Terms of Service, or site or game rules; or to protect the safety and security of Guests and our sites.
""","""
Q4 What choices do I have about WDIG collecting, using, and sharing my information?

It is possible for you to use much of our site without giving us any personally identifiable information. When you do register with us or give us personally identifiable information, you will have an opportunity at the time we collect your information -- to limit e-mail communications from WDIG and from our third-party partners. You can request at any time that WDIG not send future e-mail to you either by unsubscribing from the communication or by contacting us at memberservices@help.go.com. Also, as mentioned above, there are ways to limit the information collected through technology -- though some of our features won't work if you decide to do this.
""","""
Q5 What type of security does WDIG provide?

The importance of security for all personally identifiable information associated with our Guests is of utmost concern to us. WDIG takes technical, contractual, administrative, and physical security steps to protect all visitors' information. When you provide credit card information, we use secure socket layer (SSL) encryption to protect it. There are some things that you can do to help protect the security of your information as well. For instance, never give out your Password, since this is what is used to access all of your account information. Also remember to sign out of your account and close your browser window when you finish surfing the Web, so that other people using the same computer won't have access to your information.
""","""
Q6 How can I access my account information?

You can access the personally identifiable information you gave us during registration at our Account Options center available from (http://play.toontown.com).  Log-in with your account name and parent password. There are instructions on the start page to help you recover your password if you've forgotten it.
You can also contact us by clicking "Contact Us" in the footer on any WDIG page and selecting "Registration/Personalization" in the drop down box, or send an e-mail directly to memberservices@help.go.com. Please include information in the e-mail that will help us identify your account so we can assist you with your inquiry or request.
""","""
Q7 Whom do I contact with questions or concerns about this privacy policy?

If you need further assistance, please send an e-mail with your questions or comments to memberservices@help.go.com
write us at:

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104

Walt Disney Internet Group is a licensee of the TRUSTe Privacy Program. If you believe that WDIG has not responded to your inquiry or your inquiry has not been satisfactorily addressed, please contact TRUSTe http://www.truste.org/users/users_watchdog.html.
*You must be 18 or have the permission of your parent or guardian to dial this number.
""",
]
PrivacyPolicyText_1K = [
"""
Kids' Privacy Policy:
We recognize the need to provide additional privacy protections for kids who visit our sites.

Q1 What types of information are WDIG sites collecting about kids who are 12 and younger?

Children can surf Disney.com or other WDIG sites, view content, and play some games without any personally identifiable information being collected. In addition, we occasionally do host some moderated chat rooms where no personally identifiable information is collected or posted. However, in some areas it is necessary to collect personally identifiable information from kids to allow participation in an activity (like entering a contest) or to communicate with our community (via e-mail or message boards).
WDIG believes it is good policy not to collect more personally identifiable information from kids 12 and younger than is necessary for them to participate in our online activities. In addition, be aware that all sites that are targeted to children 12 and younger are prohibited by law from collecting more information than they need.

The only personally identifiable information we collect from kids is first name, parent's e-mail address, and child's birth date. We collect birth date to validate a Guest's age. We may also collect personal information, like a pet's name, to help Guests remember their Log-in Name and Password if they forget them.

We also allow parents to request at any time that the information collected about their child be removed from our database. If you would like to deactivate your child's account, please send an e-mail message to ms_support@help.go.com with your child's Log-in Name and Password requesting that the account be cancelled.
""","""
Q2 How does WDIG use and share the personally identifiable information that has been collected?

No information collected from Guests 12 and younger is used for any marketing or promotional purposes whatsoever, either inside or outside Walt Disney Internet Group's family of sites.
The information collected about kids 12 and younger is used only by WDIG Web sites to provide services (such as calendars) or to conduct some games or contests. Although Guests 12 and younger may be allowed to participate in some contests where information is collected, notification and prizes are sent to the parents' or guardians' e-mail address provided during the initial registration process. Publication of contest winners' full names, ages, or images for individuals 12 and younger require parental or guardian consent. Sometimes a nonidentifiable version of a child's name will be published. In those circumstances, parents may not be contacted again for permission.

We do not allow kids 12 and younger to participate in unmoderated chat rooms.

We will give out personal information about kids if required by law, for example, to comply with a court order or subpoena; to enforce our Terms of Service, or site or game rules; or to protect the safety and security of Guests and our sites.
""","""
Q3 Does WDIG notify parents about the collection of information on kids 12 and younger?

Any time children 12 and younger register with us, we send an e-mail notification to their parent or guardian. In addition, we require parents to give express permission before we will allow their children to use e-mail, message boards, and other features where personally identifiable information can be made public to the Internet and shared with users of all ages.
We also give parents 48 hours to refuse any registrations kids make in order to play games and contests. If we don't hear back, we assume it's ok for a child to be registered with us. Once a child has registered, he or she will be allowed to enter any future registration-based games and contests, and parents aren't notified again. In this instance, we use the information collected only to notify parents when a child has won a game or contest. We don't use this information for any other purpose.
""","""
Q4 How do parents access information about their kids?

Here are three methods to review the information that has been collected about children who are 12 and younger.

When parents give their children access to interactive features like message boards, they are required to establish a family account. Once a family account is established, the primary account holder can review the personally identifiable information of all family member accounts including a child's. You can access this information by logging in to your family account at the Your Account home page.

If you are not already a member of any of the WDIG sites, you can review your child's personally identifiable information by logging in to your child's account at the Account Options Home Page. You will need to have your child's account name and password. There are instructions on the Your Account home page to help you recover your child's password if they've forgotten it.

You can also contact Customer Service to view the information that has been collected from or about your child by sending an e-mail to ms_support@help.go.com. If you have not yet established a family account, you will need to have your child's user name and password. Please include information (child's account name, parent email address) in the email that will help us identify your child's account so we can assist you with your inquiry or request.
""","""
Q5 What type of security does WDIG provide?

The importance of security for all personally identifiable information associated with our guests is of utmost concern to us. WDIG takes technical, contractual, administrative, and physical security steps to protect all visitors' information. When you provide credit card information, we use secure socket layer (SSL) encryption to protect it. There are some things that you can do to help protect the security of your information as well. For instance, never give out your Password, since this is what is used to access all of your account information. Also remember to sign out of your account and close your browser window when you finish surfing the Web so that other people using the same computer won't have access to your information.
""","""
Q6 How will WDIG notify parents if this privacy policy changes?

If WDIG changes this privacy policy, we will notify parents via e-mail.

Q7 Whom do I contact with questions or concerns about this privacy policy?

If you need further assistance, please send an e-mail with your questions or comments to ms_support@help.go.com
write us at:

Member Services
Walt Disney Internet Group
506 2nd Avenue
Suite 2100
Seattle, WA 98104
or call us at (509) 742-4698

Walt Disney Internet Group is a licensee of the TRUSTe Privacy Program. If you believe that WDIG has not responded to your inquiry or your inquiry has not been satisfactorily addressed, please contact TRUSTe http://www.truste.org/users/users_watchdog.html.
*You must be 18 or have the permission of your parent or guardian to dial this number.
""",
]
PrivacyPolicyText_2A = [
"""
Updated: 11/06/2003

When you registered with our site, we pledged to handle the personal information you provided safely and with great respect, including being clear about how we collect and use your personal information. As part of this commitment, we want to advise you of important changes we are making to our general privacy policy. These changes will apply to personal information you provided in the past as well as any personal information you may provide in the future. A separate FAQ page is available providing a summary of the key changes. We are also making changes in the form of our Kids' privacy policy. We encourage you to review the updated privacy policies in their entirety.

You may accept, or "opt in" to, the terms of the updated general privacy policy in multiple ways: you may accept through an e-mail, at log-in, or through the privacy policy links, such as this, on one of our family of sites; alternatively, you may accept the updated privacy policy as part of a purchase on one of our family of sites. If you decide not to accept the updated general privacy policy, your data will continue to be handled under the previous privacy policy, your access to certain services within our sites will be limited, and you will continue to receive emails from us in accordance with your existing contact permissions.

Please note that all guests who register after November 5, 2003, will automatically be covered by the updated privacy policy and no further action is required.  
 
 
If you are an existing member and wish to accept, or OPT IN to, the changes, please select the ACCEPT Button. 
""","""
For over 75 years, The Walt Disney Company has taken great pride in the relationships that it has developed with its guests. In keeping with this tradition, we at the Walt Disney Internet Group are dedicated to protecting your privacy and handling any personal information we obtain from you with care and respect. This Privacy Policy is designed to answer your questions regarding our privacy policies and principles. 

Kids' Privacy Policy:

We recognize the need to provide additional privacy protections for children who visit our sites. To read about our protections for kids who are under the age of 13, click here.


Q1 What information does this Privacy Policy cover? 
Q2 What types of personally identifiable information do we collect about our guests?  
Q3 How is your personally identifiable information used and shared? 
Q4 What choices do you have about the collection, use, and sharing of your personally identifiable information? 
Q5 What kinds of security measures do we take to safeguard your personally identifiable information? 
Q6 How can you update your contact information and opt-out choices 
Q7 How can you ask questions, or send us comments, about this Privacy Policy?  
Q8 How will you know if we amend this Privacy Policy? 
""","""
Q1 What information does this Privacy Policy cover? 
A1 Except as specifically described below in A2 and A6, this Privacy Policy applies only to personally identifiable information collected on the Web sites where this Privacy Policy is posted and does not apply to any other information collected by The Walt Disney Family of Companies through any other means. This Privacy Policy applies to use and sharing of personally identifiable information collected on and after the date that this Privacy Policy is posted. However, for guests who registered on our Web sites prior to the date that this Privacy Policy is posted, we will apply this Privacy Policy to personally identifiable information associated with that account only if the guest accepts the terms and conditions of this Privacy Policy. Once the guest has accepted these terms and conditions, this Privacy Policy will also apply to personally identifiable information collected from that guest prior to the date that this Privacy Policy is posted. In a similar fashion, we will apply this Privacy Policy to personally identifiable information collected in the course of Non-Registered Transactions (as defined in A3 below) that occurred prior to the date that this Privacy Policy is posted, but only if the guest accepts the terms and conditions of this Privacy Policy.
""","""
As used in this Privacy Policy, "The Walt Disney Family of Companies" includes The Walt Disney Company and all of its subsidiary and affiliated entities, including companies such as ABC and ESPN that generally do not offer their products and services under the "Disney" brand name, as well as companies that generally do offer their products and services under the "Disney" brand name. (At times, our Web sites refer to The Walt Disney Family of Companies as "The Walt Disney family of companies.") The Walt Disney Internet Group is a member of The Walt Disney Family of Companies, and is referred to in this Privacy Policy as "we," "us," "our," and "ourselves." 
""","""
In keeping with the traditions of The Walt Disney Company, we refer to customers of The Walt Disney Family of Companies as "guests." When this Privacy Policy uses the term "personally identifiable information," we mean information that identifies a particular individual, such as the individual's name, postal address, e-mail address, and telephone number. When other information, such as, for example, consumer product preferences, or number of children, is directly associated with personally identifiable information, this other information also becomes personally identifiable information for purposes of this Privacy Policy. Personally identifiable information is sometimes referred to in this Privacy Policy as "personal information." Finally, the terms of this Privacy Policy are subject to all applicable laws.
""","""
Q2 What types of personally identifiable information do we collect about our guests? 
A2 We collect several types of personally identifiable information about our guests.

Information You Provide to Us 

Much of the personally identifiable information we receive comes directly from guests who are interested in obtaining various products and services from us. Typically, this information includes the guest's name, postal address, e-mail address, and telephone number. We may also collect other types of information such as gender, age, number of children, and personal interests, which we may associate with personally identifiable information. If you purchase products or services from us, we'll note, for example, credit card information, the type of services or products ordered or purchased, and the date of the order or purchase. We collect personal information when you register on, log on, or visit our Web sites, including when you participate in activities on our Web sites, such as sweepstakes, contests, games and promotional offers.
""","""
Information Collected Through Technology 

We collect information through technology to make our sites more interesting and useful to you. For instance, when you come to one of our sites, we collect your IP address. An IP address is often associated with the portal through which you enter the Internet, like your ISP (Internet service provider), your company, or your university. Standing alone, your IP address is not personally identifiable. At times, we also use IP addresses to collect information regarding the frequency with which our guests visit various parts of our sites. We may combine this information with personally identifiable information.

Our Web sites also use cookies. Cookies are pieces of information that a Web site sends to your computer while you are viewing the Web site. We and other companies use cookies for a variety of purposes. For instance, when you return to one of our sites after logging in, cookies provide information to the site so that the site will remember who you are. You can choose to have your computer warn you each time a cookie is being sent, or you can choose to turn off all cookies. You do this through your browser (like Netscape Navigator or Internet Explorer) settings. Each browser is a little different, so look at your browser Help menu to learn the correct way to modify your cookies. If you turn cookies off, you won't have access to many features that make your Web experience smoother, like the features mentioned above, and some of our services will not function properly. 
""","""
Our Web sites use a variety of technical methods for tracking purposes, including Web beacons. Web beacons are small pieces of data that are embedded in images on the pages of Web sites. We also use these technical methods to analyze the traffic patterns on our Web sites, such as the frequency with which our users visit various parts of our Web sites. These technical methods may involve the transmission of information either directly to us or to another party authorized by us to collect information on our behalf. We also use these technical methods in HTML e-mails that we send our guests to determine whether our guests have opened those e-mails and/or clicked on links in those e-mails. The information from use of these technical methods may be collected in a form that is personally identifiable.

Many advertisements are managed and placed on our Web sites by third parties. These companies are called "network advertisers." Network advertisers who place advertisements on our Web sites may also use cookies and Web beacons to collect non-personally identifiable information when you click on or move your cursor over one of their banner advertisements. You may not realize this information is being collected. In some cases, we may have access to information from Web beacons and cookies used by network advertisers on our sites and this information may permit us to identify other sites that you have visited that are also associated with the network advertiser. Finally, once you've clicked on an advertisement and have left our Web sites, our Privacy Policy no longer applies and you must read the privacy policy of the advertiser to see how your personal information will be handled on their site.
""","""
Information That We Collect from Others 

We may supplement personally identifiable information that we have collected directly from our guests with other information that we obtain from third parties and other members of The Walt Disney Family of Companies. In addition, we may obtain information about individuals who are not yet users of our Web sites or guests of The Walt Disney Family of Companies. In addition, When we associate information that we obtain from third parties or other members of The Walt Disney Family of Companies with personally identifiable information that we have collected under this Privacy Policy, we will treat the acquired information like the information that we collected ourselves and, except as permitted by this Privacy Policy, the information will not be shared with third parties.
""","""
Q3 How is your personally identifiable information used and shared? 
A3 As described in detail below, The Walt Disney Family of Companies may use your personally identifiable information in many ways, including sending you promotional materials, and sharing your information with third parties so that these third parties can send you promotional materials. (By "promotional materials," we mean communications that directly promote the use of our Web sites, or the purchase of products or services.) As outlined below in A4, you may "opt-out" of certain uses of your personal information.
""","""
Disney Family of Companies, Licensees and Co-Branding Participants 

Personally identifiable information collected under this Privacy Policy is shared among and used by The Walt Disney Family of Companies for many purposes. For example, The Walt Disney Family of Companies may use your personal information to send you promotional materials about goods and services (including special offers and promotions) either offered by The Walt Disney Family of Companies or offered by third parties. These promotional materials may be sent to you by postal mail, e-mail or other means. You may opt out of receiving these communications as provided in A4 below. Please keep in mind, however, that when you purchase or request products or services from The Walt Disney Family of Companies, promotional materials may accompany delivery of that product or service. We refer to sending you promotional materials in these circumstances as "Fulfillment Uses" of your personal information. Because these promotional materials accompany products or services that you have requested, your opt-outs for Individual Disney Companies and The Walt Disney Family of Companies under A4 below will not apply to any of these Fulfillment Uses.
""","""
The Walt Disney Family of Companies may also use your personal information for many purposes other than sending you promotional materials. (We refer to all of these types of uses of your personal information that do not involve the sending of promotional materials as "Operational Uses.") For example, we may use your information to complete transactions requested by you (such as your purchase of a product or service offered on our Web sites), or to send you administrative communications either about your account with us or about features of our Web sites, including any future changes to this Privacy Policy. As another example of Operational Uses, we may share your personal information with the Walt Disney World  Resort telephone reservations center so that the reservations center operators are able to respond immediately to your questions or requests when you call, rather than asking you to provide your information a second time. Because these uses of your personal information do not involve sending you promotional materials, your opt-outs for Individual Disney Companies and The Walt Disney Family of Companies under A4 below will not apply to any of these Operational Uses. 
""","""
In addition to using your personal information within The Walt Disney Family of Companies, The Walt Disney Family of Companies may share your personal information with companies that offer products and/or services under brand names of The Walt Disney Family of Companies. These companies are called "licensees." For example, a company that publishes and sells books under the "Disney" brand would be such a licensee. The Walt Disney Family of Companies may also share your information with companies that offer products and/or services that are co-branded using brand names of The Walt Disney Family of Companies. These companies are called "co-branding participants." For example, the Disney's Visa Card is co-branded with the bank that issues that credit card. When The Walt Disney Family of Companies shares personal information with third parties acting as licensees and co-branding participants, these licensees and co-branding participants are restricted by contract from using the personal information for any marketing or promotional purpose that is not related to a licensed or co-branded product or service. Finally, to further protect your privacy, these licensees and co-branding participants' use of personal information shared with them under this Privacy Policy is subject to the same opt-out rights (and limitations upon those rights) that apply to use of personal information by members of The Walt Disney Family of Companies under A4 below.
""","""
You may engage in transactions (such as purchasing products or services) without registering and logging on our Web sites. These transactions may be either with us or with other members of The Walt Disney Family of Companies. (We refer to all of these transactions that you engage in without registering and logging on our Web sites as "Non-Registered Transactions.") An example of a Non-Registered Transaction would be when you purchase items from the DisneyStore.com without registering and logging on that Web site. When you engage in Non-Registered Transactions, the opt-out choices described in A4 below will not be available to you, but your information will not be shared with third parties, and will not be used by any member of The Walt Disney Family of Companies to send you promotional materials other than the member involved in your transaction, except as separately permitted by other provisions of this Privacy Policy.
""","""
Finally, The Walt Disney Family of Companies may take your personally identifiable information and make it non-personally identifiable, either by combining it with information about other individuals (aggregating your information with information about other individuals), or by removing characteristics (such as your name) that make the information personally identifiable to you (de-personalizing your information). Given the nature of this information, there are no restrictions under this Privacy Policy upon the right of The Walt Disney Family of Companies to aggregate or de-personalize your personal information, and The Walt Disney Family of Companies may use and/or share with third parties the resulting non-personally identifiable information in any way.
""","""
Third Parties Offering Promotions, Products, or Services 

Subject to your opt-out choices (see A4 below), The Walt Disney Family of Companies may share your personal information with selected third parties so that they can send you promotional materials about goods and services (including special offers and promotions) offered by them. (We call this type of sharing "promotional sharing" or sharing for "promotional purposes.") When sharing your information for promotional purposes, The Walt Disney Family of Companies attempts to select only reputable companies that offer high quality products and services. Moreover, The Walt Disney Family of Companies will not share your e-mail address with third parties for promotional purposes, except when you consent to such sharing in the course of your participation in a Sponsored Activity as described below. When The Walt Disney Family of Companies shares your personal information with a third party under any circumstance described in this "Third Parties Offering Promotions, Products, or Services" section, your personal information will become permanently subject to the information use and sharing practices of the third party, and the third party will not be restricted by this Privacy Policy with respect to its use and further sharing of your personal information.
""","""
In addition to the promotional sharing that is subject to your opt-out choices under A4 below, The Walt Disney Family of Companies may also share your information when you engage in certain activities on our sites that are sponsored by third parties, such as purchasing products or services offered by a third party, electing to receive information or communications from a third party, or electing to participate in contests, sweepstakes, games or other programs sponsored in whole or in part by a third party. The Walt Disney Family of Companies may also share your personal information when you respond to promotional materials from The Walt Disney Family of Companies and authorize a third party to use your personal information for purposes such as, for example, sending you additional promotional materials, providing you a product or service, or entering you in a contest, sweepstakes or game. (We refer to all of these activities and requests as "Sponsored Activities.") When you participate in Sponsored Activities, you will either be required or requested to agree that the sponsor or business associate may use your personal information (including, in some cases, your e-mail address) in accordance with the sponsor or business associate's privacy practices. Since you will have consented to this specific instance of sharing of your personal information, the opt-out choice for "Third Parties" described in A4 below will not apply.
""","""
Companies That Facilitate Communications and Transactions with You

Sometimes The Walt Disney Family of Companies hires companies to help deliver products or services, like a shipping company that delivers a package or a company that helps fulfill prizes for a sweepstakes. In those instances, there is a need to share your information with these companies. Sometimes The Walt Disney Family of Companies also works with other companies who help either gather your information or communicate with you. Your opt-out choices under A4 below will not apply to sharing by The Walt Disney Family of Companies of your personal information with any of these companies. Nonetheless, except as separately permitted by other provisions of this Privacy Policy, these companies are allowed to gather, receive, and use your information only for the purposes described in this paragraph or as required by law.
""","""
Companies That You Previously Authorized to Obtain Your Information 

In certain circumstances, your dealings with a third party may have authorized that third party to obtain your personal information from The Walt Disney Family of Companies and to use that information in accordance with the third party's own privacy practices and policies. For example, in using an online shopping service (such as the shopping services offered by Internet portals that refer the portal's users to third-party merchants), you may have authorized that shopping service to obtain from the service's participating third-party merchants (including The Walt Disney Family of Companies) information about your purchases conducted through the shopping service. In such circumstances, your opt-out elections under A4 below will not apply to sharing of your personal information by The Walt Disney Family of Companies. Nonetheless, The Walt Disney Family of Companies will provide such companies only the information that you authorized (except as separately permitted under other provisions of this Privacy Policy). In the example given above, the shopping service would be provided only information concerning purchases you made from The Walt Disney Family of Companies through that shopping service, and would not be provided any other information concerning you, unless any additional sharing of your personal information were separately permitted under another provision of this Privacy Policy.
""","""
Purchase or Sale of Businesses 

From time to time, we may purchase a business or sell one or more of our businesses and your personally identifiable information may be transferred as a part of the purchase or sale. In the event that we purchase a business, the personally identifiable information received with that business would be treated in accordance with this Privacy Policy, if it is practicable and permissible to do so. In the event that we sell a business, we will include provisions in the selling contract requiring the purchaser to treat your personally identifiable information in the same manner required by this Privacy Policy (including any amendments to this Privacy Policy). In light of this protection, your opt-out choices under A4 will not affect our right to transfer your information to a purchaser in these circumstances. The provisions of this paragraph will also apply in the event that one or more businesses of any other member of The Walt Disney Family of Companies are sold and personal information subject to this Privacy Policy is transferred to a purchaser of those businesses.

Disclosures Required By Law and Disclosures to Help Protect the Security and Safety of Our Web Sites, The Walt Disney Family of Companies and Others 

Regardless of any opt-out choices that you make under A4, The Walt Disney Family of Companies will disclose personal information when it believes in good faith that such disclosures (a) are required by law, including, for example, to comply with a court order or subpoena, or (b) will help to: enforce our Terms of Use; enforce contest, sweepstakes, promotions, and/or game rules; protect your safety or security, including the safety and security of property that belongs to you; and/or, protect the safety and security of our Web sites, The Walt Disney Family of Companies, and/or third parties, including the safety and security of property that belongs to The Walt Disney Family of Companies or third parties.
""","""
Q4 What choices do you have about the collection, use, and sharing of your personally identifiable information? 
A4 With regard to personal information that you have provided under this Privacy Policy, there are three separate opt-out choices available to you. These opt-out choices are the means by which you give us, or decline to give us, your consent to use your personal information for the purposes covered by these opt-out choices. Some of our Web sites may not present you all three opt-out choices described below. Please be assured, however, that if any one of these opt-out choices is not presented to you on a Web site, personal information collected from you on that site will not be used for the purposes covered by that opt-out choice. There are several methods by which you can exercise your opt-out choices: (a) during the registration process on our Web sites; (b) after registration, by logging on our Web sites, clicking on our Privacy Policy links, going to a site's Guest Services center (sometimes called a site's "Member Services" or "Preference" center), and following the opt-out directions; and (c) as described below in A6. Each of these opt-out choices is subject to the exceptions described further below in this A4.
""","""
Your three opt-out choices are:

Third Parties: You may choose to opt-out of receiving promotional materials from third parties. If you do not choose this opt-out, The Walt Disney Family of Companies may share your personal information so that third parties can send you these promotional materials. Your opt-out choices for third parties are specific to the particular Web sites where you make these choices. Thus, if you want to opt out of all uses of your personal information covered by the "Third Parties" opt-out, you must consistently elect that opt-out at each of our Web sites where you either register, or log in and visit the Guest Services center. If you want to make a change in your "Third Parties" opt-out choices, you will need to make that change at each of our Web sites where you previously made a different choice. Please bear in mind that this opt-out choice for "Third Parties" will not apply to the licensees and co-branding participants described above in A3.
""","""
The Walt Disney Family of Companies: You may choose to opt-out of receiving promotional materials from members of The Walt Disney Family of Companies, including the licensees and co-branding participants described above in A3. This opt-out choice is found on each of our Web sites. For your convenience, when you make a choice regarding this "The Walt Disney Family of Companies" opt-out at any one of our Web sites, we will treat that choice as replacing any other choices regarding that opt-out that that you may previously have made. Thus, if you want to make a change in your "The Walt Disney Family of Companies" opt-out choice, you can make that change by visiting the Guest Services center at any one of our Web sites. Your election to choose this "The Walt Disney Family of Companies" opt-out will not, however, override your consent to receive promotional materials from a specific member of The Walt Disney Family of Companies. As described in the following paragraph, you provide this consent when you visit the Guest Services center of the Web site for a specific member of The Walt Disney Family of Companies and choose not to opt-out of receiving promotional materials from that specific member.
""","""
Individual Disney Companies: You may choose to opt-out of receiving promotional materials directly from a specific member of The Walt Disney Family of Companies. To do so, you must visit the Guest Services center of the Web site for this specific member and opt-out of receiving promotional materials from this member. However, if you do not also opt-out of receiving promotional materials from "The Walt Disney Family of Companies" as described in the preceding paragraph, you may still receive promotional materials from this specific member of The Walt Disney Family of Companies.
""","""
Please keep in mind that any opt-out choices you make will not apply in situations where (a) you either have made, simultaneously make, or later make a specific request for information from a member of The Walt Disney Family of Companies, (b) The Walt Disney Family of Companies uses your personal information for either "Operational Uses" or "Fulfillment Uses" (as described above in A3), (c) you either have engaged, simultaneously engage, or later engage in either Non-Registered Transactions or Sponsored Activities (as described above in A3), or (d) The Walt Disney Family of Companies shares your personal information under the provisions of A3 above with respect to "Companies That Facilitate Communications and Transactions With You," "Companies That You Previously Authorized to Obtain Your Information," "Third Party Advertisers and Network Advertisers," "Purchase or Sale of Businesses," or "Disclosures Required By Law and Disclosures to Help Protect the Security and Safety of Our Web Sites, The Walt Disney Family of Companies and Others."
""","""
Finally, if you do not exercise your opt-out choices upon registration or initial log-in at our Web sites, it may take up to ninety (90) days for your opt-out choices to be fully effective. Our systems require time to update, and promotional mailings using personal information shared before your opt-out may already be in process. Thus, you might continue to receive promotional materials from The Walt Disney Family of Companies based upon the personal information you have provided under this Privacy Policy for up to ninety (90) days. For similar reasons, your personal information might continue to be shared with third parties for promotional purposes for up to ninety (90) days.
""","""
Q5 What kinds of security measures do we take to safeguard your personally identifiable information? 
A5 The security and confidentiality of your information is extremely important to us. We have implemented technical, administrative, and physical security measures to protect guest information from unauthorized access and improper use. From time to time, we review our security procedures in order to consider appropriate new technology and methods. Please be aware though that, despite our best efforts, no security measures are perfect or impenetrable.
""","""
Q6 How can you update your contact information and opt out choices? 
A6 You can access and update the contact information you gave us during registration (that is, your postal address, e-mail address, or any other information that would directly enable us to contact you), or modify your opt-out choices, by going to our member services centers. Simply click on this link http://register.go.com/go/memberservices/home, or go to the Guest Services centers on our Web sites, and then log in with your member name and password. There are instructions on the start page of the link above to help you recover your password if you've forgotten it. If you need to recover your password, you can also contact us via e-mail at ms_support@help.go.com. Please include information in the e-mail that will help us identify your account so we can assist you with your request. We may also provide you an opportunity to update your contact information and/or modify your opt-out choices by sending you an e-mail or other communication that invites your response. Finally, you may unsubscribe from certain e-mail communications by clicking on unsubscribe links in those e-mails.
""","""
Q7 How can you ask questions, or send us comments, about this Privacy Policy? 
A7 If you have questions or wish to send us comments about this Privacy Policy, please send an e-mail with your questions or comments to ms_support@help.go.com or write us:

  Member Services
  WDIG
  500 S. Buena Vista St.
  Mail Code 7716
  Burbank, CA 91521-7716, USA

Please be assured that any personal information that you provide in communications to the above e-mail and postal mail addresses will not be used to send you promotional materials, unless you so request.
""","""
Q8 How will you know if we amend this Privacy Policy? 
A8 We may amend this Privacy Policy at any time. If we make any material changes in the way we collect, use, and/or share your personal information, we will notify you by sending you an e-mail at the last e-mail address that you provided us, and/or by prominently posting notice of the changes on the Web sites covered by this Privacy Policy. Any material changes to this Privacy Policy will be effective upon the earlier of thirty (30) calendar days following our dispatch of an e-mail notice to you or thirty (30) calendar days following our posting of notice of the changes on the Web sites covered by this Privacy Policy. Please note that, at all times, you are responsible for updating your personal information to provide us your current e-mail address. In the event that the last e-mail address that you have provided us is not valid, or for any other reason is not capable of delivering to you the notice described above, our dispatch of the e-mail containing such notice will nonetheless constitute effective notice of the changes described in the notice. In any event, changes to this Privacy Policy may affect our use of personal information that you provided us prior to our notification to you of the changes. If you do not wish to permit changes in our use of your information, you must notify us prior to the effective date of the changes that you wish to deactivate your account with us.

The Walt Disney Internet Group is a licensee of the TRUSTe Privacy Program. If you believe that we have not responded to your inquiry or your inquiry has not been satisfactorily addressed, please contact TRUSTe at http://www.truste.org/users/users_watchdog.html.
""",
]
PrivacyPolicyText_2K = [
"""
Updated: 11/06/2003

For over than 75 years, The Walt Disney Company has taken great pride in the relationships that it has developed with its guests. In keeping with this tradition, we at the Walt Disney Internet Group are dedicated to protecting your privacy and handling any personal information we obtain from you with care and respect. This Kids' Privacy Policy is designed to answer your questions regarding our privacy policies and principles with respect to children under the age of 13.

Building on our general Privacy Policy, we recognize the need to provide additional privacy protections when children visit the sites on which this Kids' Privacy Policy is posted. We explain those additional protections here in this Kids' Privacy Policy. For your convenience, this Kids' Privacy Policy uses terms that are defined in our general Privacy Policy.

The Children's Online Privacy Protection Act ("COPPA") requires that we inform parents and legal guardians about how we collect, use, and disclose personal information from children under 13 years of age; and that we obtain the consent of parents and guardians in order for children under 13 years of age to use certain features of our Web sites. Below we explain how we do that for these "kids." Also, when we use the term "parent" below, we mean to include legal guardians. 
""","""
Q1 What types of personal information do we collect about kids? 
Q2 How do we use and share the personal information that we have collected from kids?  
Q3 How do we notify and obtain consent from parents for the collection of personal information from their kids? 
Q4 How can parents access, change or delete personal information about their kids? 
Q5 How will we notify parents if our Kids' Privacy Policy changes? 
Q6 Who do guests contact with questions or concerns about our Kids' Privacy Policy? 
""","""
Q1 What types of information do we collect about kids? 
A1 Kids can surf Disney.com and other WDIG sites, view content, and play many games without any personal information being collected. We do not collect personal information from kids unless they register on WDIG sites. Typically, kids will register in order to participate in sweepstakes or contests or to participate in a special activity. The only information we collect from kids during our registration process is a kid's first name, parent's e-mail address, kid's birth date, member name, and password. We collect birth dates to validate the ages of our guests, including kids. We do not collect any other personally identifiable information from kids during our registration process. We also will collect a kid's e-mail address from a parent for the purpose of sending the kid e-mail related to a subscription. For example, we would send Disney's Blast Gazette to a kid directly at the request of the kid's parent. Note that all sites that are directed to children under 13 are prohibited by law from conditioning a kid's participation in an online activity on the kid's providing more personal information than is reasonably necessary. 
""","""
We may collect personal information from parents in order to allow kids to participate in certain features located on our Web sites and within our kids' subscription products, such as Disney's Blast and Disney's Toontown Online (see A3 below for details). These features may include instant message chatting (for example, Secret Friends in Disney's Toontown Online), sending e-mail, posting on message boards, interacting with pen-pals, and other similar activities. In the course of a kid's participation in these features, a kid may also provide us additional information about himself or herself, such as the contents of his or her chat or message board postings. If a parent allows us to collect personal information about their kid, we may link certain information collected through technology (see the "Information Collected Through Technology" section of A2 of our general Privacy Policy) to that personal information.
""","""
Q2 How do we use and share the personally identifiable information that we have collected about kids? 
A2 If a kid registers for a sweepstakes or contest, we use the parent's e-mail address to notify the parent of the kid's registration request (as described in detail below in A3). To personalize communications to a kid regarding a specific product (such as Disney's Blast), we may use the kid's first name combined with the parent's last name and a mailing address provided by the parent when signing up for that specific product. We may collect a kid's e-mail address from the parent in order to send the kid a newsletter, such as Disney's Blast Gazette. In addition, personal information regarding a kid may be disclosed in the course of a kid's participation in certain interactive features such as message boards and pen pal services. 
""","""
We do not share any information about a kid with any other member of The Walt Disney Family of Companies or with any third parties unless the disclosure is reasonably necessary: to comply with law, including, for example, to comply with a court order or subpoena; to enforce our Terms of Service, or site or game rules; or to protect the safety and security of our Guests and our Web sites.
""","""
Q3 How do we notify and obtain consent from parents for the collection of information from their kids? 
A3 We send parents an e-mail when their kid registers and enters a sweepstakes or contest and we provide parents 48 hours to refuse their kid's registration and entry in the sweepstakes or contest. If the parent refuses to allow the kid's registration and entry, we delete the kid's information from our database. If we don't hear back from the parent, we assume it is acceptable for the kid to be registered and entered in the sweepstakes or contest. Once a parent permits a kid to register, the kid will be able to enter future registration-based sweepstakes or contests without any further notification to the parent. If a kid wins a sweepstakes or contest, we notify the parent at the parent's e-mail address provided to us during the registration process and request that the parent provide their postal address for purposes of delivering the prize. We may publish a winner's first name, first initial of last name, city, and state of residence on our Web sites. 
""","""
Before allowing a kid to use a feature of our Web sites that might result in the disclosure of the kid's information to third parties on the Internet, we require a parent's name and credit card information to confirm that the parent has given permission for the kid's participation in such features. The credit card will be charged only if the parent is signing up for a subscription service and has authorized us to charge their credit card. Otherwise the credit card information is used for real-time verification purposes to confirm that an adult is authorizing the kid's participation. The credit card information is archived in a secure manner and retained by us as evidence that we received parental consent.
""","""
Q4 How can parents access, change or delete personally identifiable information about their kids? 
A4 At any time parents can refuse to permit us to collect further personal information from their kid and can request that any personal information we have collected be deleted from our records. We use two methods to allow parents to access, change, or delete the personally identifiable information that we have collected from their kids. 
""","""
A parent can access, change, or delete his or her kid's personal information by logging on to the kid's account at the Member Services Home Page located at http://register.go.com/go/memberservices/home. The parent will need to have their kid's member name and password. There are instructions on the Your Account home page explaining how to recover a password if the kid has forgotten it. 
""","""
A parent can contact our customer service department to access, change, or delete the personal information that we have collected from his or her kid by sending an e-mail to ms_support@help.go.com. Please include the kid's member name and the parent's e-mail address in the e-mail so that we can better assist you with your inquiry or request. 
""","""
Q5 How will we notify parents if our Kids' Privacy Policy changes? 
A5 We may amend our Kids' Privacy Policy at any time. We will provide parents notice by e-mail of any material changes in the way we intend to collect, use, and/or share kids' personal information. Please note that, at all times, parents should update their personal information to provide us current e-mail addresses. We will apply material changes in our Kids' Privacy Policy only in conformance with applicable law, including any applicable provisions of COPPA that require parental consent.
""","""
Q6 Who do guests contact with questions or concerns about our Kids' Privacy Policy? 
A6 If you need further assistance, please send an e-mail with your questions or comments to ms_support@help.go.com or write us at: 

  Member Services
  Walt Disney Internet Group
  500 S. Buena Vista Street
  Mail Code 7716
  Burbank, CA 91521-7716, USA
  You may also telephone us at 1-(877) 466-6669. (If you are not 18 years of age or older, you must have your parent or guardian's permission to call this number.) 

The Walt Disney Internet Group is a licensee of the TRUSTe Privacy Program. If you believe that we have not responded to your inquiry or your inquiry has not been satisfactorily addressed, please contact TRUSTe http://www.truste.org/users/users_watchdog.html. 
""",
]

ActivateChatYes = "Ativar"
ActivateChatNo = lCancel
ActivateChatMoreInfo = "Mais informações"
ActivateChatPrivacyPolicy = "Privacy Policy"

# SecretFriendsInfoPanel.py
SecretFriendsInfoPanelOk = lOK
SecretFriendsInfoPanelClose = lClose
SecretFriendsInfoPanelText = [""" O recurso Amigos secretos O recurso Amigos secretos permite que um membro converse diretamente com outro no Toontown On-line da Disney (o "Serviço") depois que os membros estabelecerem uma conexão de Amigos secretos. Quando o seu filho tentar usar o recurso Amigos secretos, solicitaremos que você insira a sua Senha de pais para indicar seu consentimento para que a criança use o recurso. Esta é uma descrição detalhada do processo de criação de uma conexão de Amigos secretos entre os membros fictícios chamados "Sandra" e "Marcos". 1. O responsável por Sandra e o responsável por Marcos ativam o recurso Amigos secretos inserindo suas respectivas Senhas de pais (a) nas áreas de Opções da conta do Serviço ou (b) quando for solicitado no jogo, em uma janela pop-up de Controles disponíveis aos pais. 2. Sandra pede um Segredo (descrito abaixo) no Serviço.""",""" 3. O Segredo de Sandra é comunicado a Marcos fora do Serviço. (O Segredo de Sandra pode ser comunicado a Marcos diretamente por Sandra ou indiretamente, se Sandra revelar o Segredo a outra pessoa.) 4. Marcos envia o Segredo de Sandra ao Serviço dentro de 48 horas a partir da hora em que Sandra solicitou o Segredo ao Serviço. 5. Em seguida, o Serviço notifica Marcos de que Sandra tornou-se sua Amiga secreta. Da mesma forma, o Serviço notifica Sandra de que Marcos tornou-se seu Amigo secreto. 6. Sandra e Marcos podem agora conversar diretamente um com o outro até um deles escolher cancelar o seu relacionamento como Amigo secreto, ou até que o recurso de Amigos secretos seja desativado para Sandra ou Marcos por um dos responsáveis por essas crianças. Então, a conexão de Amigos secretos pode ser desativada a qualquer momento: (a) por um membro, que remove o Amigo secreto de sua lista de amigos (conforme descrito no Serviço), ou (b) pelo responsável pelo membro, que desativa o recurso Amigos secretos na área Opções da conta do Serviço, seguindo as etapas definidas no recurso.""",""" O Segredo é um código aleatório, gerado por computador, que é atribuído a um membro específico. O Segredo precisa ser usado para ativar a conexão de Amigo secreto dentro de 48 horas a partir da hora em que o membro solicitou o Segredo; caso contrário, o Segredo expirará e não poderá ser usado. Além disso, só se pode usar um único Segredo para estabelecer uma conexão de Amigo secreto. Para fazer conexões adicionais de Amigos secretos, o membro precisará solicitar mais segredos, um para cada Amigo secreto que quiser incluir. As Amizades secretas não podem ser transferidas. Por exemplo, se Sandra se tornar Amiga secreta de Marcos, e Marcos se tornar Amigo secreto de Jéssica, Sandra não se tornará automaticamente Amiga secreta de Jéssica. Para que Sandra e Jéssica se tornem Amigas secretas, uma delas terá que solicitar um novo Segredo ao Serviço e comunicar à outra.""",""" Os Amigos secretos se comunicam entre si por meio de uma conversa interativa em formato livre. O conteúdo da conversa é inserido diretamente pelo membro participante e é processado pelo Serviço, cuja operação é realizada pelo Walt Disney Internet Group ("WDIG"), 506 2nd Avenue, Suite 2100, Seattle, WA 98104, EUA (telefone +1 (509) 742-4698; e-mail ms_support@help.go.com). Apesar de recomendarmos aos membros não trocarem com outros membros informações pessoais como nome e sobrenome, e-mails, endereço postal ou números de telefone ao usarem o recurso Amigos secretos, não podemos garantir que os membros seguirão a recomendação e que tais informações sejam preservadas. Embora o chat Amigos secretos seja automaticamente filtrado para evitar o uso da maioria dos palavrões, não há moderação nem supervisão de nossa parte. Se os pais deixarem seus filhos usarem a conta com o recurso Amigos secretos ativado no Serviço, aconselhamos que eles mesmos supervisionem os filhos durante a brincadeira.""",""" O WDIG não usa o conteúdo do chat Amigos secretos para nenhum fim que não seja a comunicação do conteúdo ao amigo secreto do membro, e não revela tal conteúdo a terceiros, exceto: (1) se exigido por lei; por exemplo, para cumprir uma ordem ou intimação judicial; (2) para fazer com que os Termos de Uso aplicáveis ao Serviço (que podem ser acessados na página principal do Serviço) sejam respeitados; ou (3) para proteger a segurança dos Membros do Serviço e o Serviço propriamente dito. Mediante solicitação ao WDIG, o responsável por uma criança-membro pode analisar e mandar apagar qualquer conteúdo do recurso de chat Amigos secretos fornecidos pela criança em questão, desde que tal conteúdo já não tenha sido excluído dos registros pelo WDIG. Obedecendo à Children's Online Privacy Protection Act, uma lei americana de proteção à privacidade on-line para as crianças, estamos proibidos de condicionar a participação da criança em qualquer tipo de atividade (inclusive o recurso Amigos secretos) ao fornecimento, por parte da criança, de mais informações pessoais do que o estritamente necessário para que ela participe de tais atividades.""",""" Além disso, conforme observado acima, reconhecemos o direito do responsável pela criança de não permitir que continuemos a deixar que a criança use o recurso Amigos secretos. Ao ativar o recurso Amigos secretos, você reconhece que há alguns riscos inerentes ao chat, no qual os membros podem conversar uns com os outros usando o recurso Amigos secretos, sendo que você foi informado de todos os riscos mencionados aqui, concordando em aceitá-los."""
]

LeaveToPay = """Para efetuar a compra, o jogo sairá para Toontown.com.br"""
LeaveToPayYes = "Comprar"
LeaveToPayNo = lCancel

LeaveToSetParentPassword = """Para configurar a Senha de pais, o jogo sairá para Toontown.com.br"""
LeaveToSetParentPasswordYes = "Definir senha"
LeaveToSetParentPasswordNo = lCancel

LeaveToEnableChatUK = """Para ativar o chat, o jogo sairá para o site Toontown."""
LeaveToEnableChatUKYes = "Ativar chat"
LeaveToEnableChatUKNo = lCancel

ChatMoreInfoOK = lOK
SecretChatDeactivated = 'O recurso "Amigos secretos" foi desativado.'
RestrictedSecretChatActivated = 'O recurso "Amigos secretos restritos" foi ativado!'
SecretChatActivated = 'O sistema "Amigos secretos" foi ativado!\n\nSe você mudar de idéia e decidir desativar este recurso mais tarde, clique em "Opções da conta" na página da web de Toontown.'
SecretChatActivatedOK = lOK
SecretChatActivatedChange = "Alterar Opções"
ProblemActivatingChat = 'Ops! Não foi possível ativar o recurso de chat "Amigos secretos".\n\n%s\n\nTente novamente mais tarde.'
ProblemActivatingChatOK = lOK

# MultiPageTextFrame.py
MultiPageTextFrameNext = lNext
MultiPageTextFramePrev = 'Anterior'
MultiPageTextFramePage = 'Página %s/%s'

# GuiScreen.py
GuiScreenToontownUnavailable = "Toontown parece estar temporariamente indisponível, ainda tentando..."
GuiScreenCancel = lCancel


# CreateAccountScreen.py
CreateAccountScreenUserName = "Nome da conta"
CreateAccountScreenPassword = "Senha"
CreateAccountScreenConfirmPassword = "Confirmar senha"
CreateAccountScreenCancel = lCancel
CreateAccountScreenSubmit = "Enviar"
CreateAccountScreenConnectionErrorSuffix = ".\n\nTente novamente mais tarde."
CreateAccountScreenNoAccountName = "Insira o nome da conta."
CreateAccountScreenAccountNameTooShort = "O nome da conta deve ter, pelo menos, %s caracteres. Tente novamente."
CreateAccountScreenPasswordTooShort = "A senha deve ter, pelo menos, %s caracteres. Tente novamente."
CreateAccountScreenPasswordMismatch = "As senhas inseridas não combinam. Tente novamente."
CreateAccountScreenUserNameTaken = "Este nome de usuário já existe. Tente novamente."
CreateAccountScreenInvalidUserName = "Nome de usuário inválido.\nTente novamente."
CreateAccountScreenUserNameNotFound = "Nome de usuário não encontrado.\nTente novamente ou crie uma nova conta."

# ToontownClientRepository.py
CRConnecting = "Conectando..."
# host, port
CRNoConnectTryAgain = "Não foi possível conectar-se a %s:%s. Tentar novamente?"
CRNoConnectProxyNoPort = "Não foi possível conectar-se a %s:%s.\n\nVocê está se comunicando com a Internet por via proxy, mas o seu proxy não permite conexões na porta %s.\n\nVocê deve abrir esta porta, ou desativar o proxy, para poder jogar na Toontown. Se o proxy foi fornecido pelo seu provedor, é preciso entrar em contato com ele para abrir esta porta."
CRMissingGameRootObject = "Há alguns objetos do jogo raiz ausentes. (A causa pode ser uma conexão de rede com falhas). Saindo do jogo."
CRNoDistrictsTryAgain = "Não há Regiões de Toontown disponíveis. Tentar novamente?"
CRRejectRemoveAvatar = "O Toon não pôde ser excluído, tente novamente mais tarde."
CRLostConnection = "A sua conexão de Internet à Toontown foi interrompida inesperadamente."
CRBootedReasons = {
    1: "Houve um problema inesperado. A conexão falhou, mas você ainda deve conseguir conectar-se novamente para voltar ao jogo.",
    100: "Você foi desconectado porque outra pessoa acabou de fazer login usando a sua conta em outro computador.",
    120: "Você foi desconectado porque houve um problema com sua autorização para usar o chat de teclado.",
    122: "Houve um problema inesperado quando você fez login na Toontown. Entre em contato com o Suporte ao Cliente da Toontown.",
    125: "Os arquivos da Toontown que você tem instalados parecem ser inválidos. Use o botão Jogar, no site da web oficial da Toontown, para executar a Toontown.",
    126: "Você não está autorizado a usar privilégios administrativos.",
    151: "O administrador responsável pelos servidores de Toontown fez logout na sua conta.",
    153: "A região de Toontown em que você estava jogando foi reiniciada. Todas as pessoas que estavam jogando nesta região foram desconectadas. Entretanto, você poderá conectar-se novamente e voltar direto ao jogo.",
    288: "Sinto muito, mas você usou todos os seus minutos disponíveis deste mês na Toontown.",
    349: "Sinto muito, mas você usou todos os seus minutos disponíveis deste mês na Toontown.",
    }
CRBootedReasonUnknownCode = "Houve um problema inesperado (código de erro %s). A conexão falhou, mas você ainda deve conseguir conectar-se novamente para voltar ao jogo."
CRTryConnectAgain = "\n\nTentar conectar-se novamente?"
# avName
CRToontownUnavailable = "Toontown parece estar temporariamente indisponível, ainda tentando..."
CRToontownUnavailableCancel = lCancel
CRNameCongratulations = "PARABÉNS!!"
CRNameAccepted = "O seu nome foi\naprovado pelo Conselho de Toons.\n\nA partir de agora,\nvocê terá o nome\n\"%s\""
CRServerConstantsProxyNoPort = "Não foi possível contatar %s.\n\nVocê está se comunicando com a Internet por via proxy, mas o seu proxy não permite conexões na porta %s.\n\nVocê deve abrir esta porta, ou desativar o proxy, para poder jogar na Toontown. Se o proxy foi fornecido pelo seu provedor, é preciso entrar em contato com ele para abrir esta porta."
CRServerConstantsProxyNoCONNECT = "Não foi possível contatar %s.\n\nVocê está se comunicando com a Internet por via proxy, mas o seu proxy não permite o método CONECTAR.\n\nVocê deve ativar este recurso, ou desativar o proxy, para poder jogar na Toontown. Se o proxy foi fornecido pelo seu provedor, é preciso entrar em contato com ele para abrir esta porta."
CRServerConstantsTryAgain = "Não foi possível contatar %s.\n\nO servidor de contas da Toontown deve estar temporariamente fora do ar ou deve haver algum problema na conexão de Internet.\n\nTentar novamente?"
CRServerDateTryAgain = "Não foi possível obter a data do servidor de %s. Tentar novamente?"
AfkForceAcknowledgeMessage = "O seu Toon ficou com sono e foi para a cama."
PeriodTimerWarning = "O seu limite de tempo em Toontown neste mês está quase no fim!"
PeriodForceAcknowledgeMessage = "Você usou todos os seus minutos disponíveis em Toontown neste mês. Volte e jogue mais no próximo mês!"
CREnteringToontown = "Entrando em Toontown..."

# DownloadWatcher.py
# phase, percent
DownloadWatcherUpdate = "Downloading %s"
DownloadWatcherInitializing = "Download Initializing..."

# LoginScreen.py
LoginScreenUserName = "Nome da Conta"
LoginScreenPassword = "Senha"
LoginScreenLogin = "Login"
LoginScreenCreateAccount = "Criar Conta"
LoginScreenQuit = lQuit
LoginScreenLoginPrompt = "Por favor, digite um nome de usuário e uma senha."
LoginScreenBadPassword = "Senha errada.\nTente novamente."
LoginScreenInvalidUserName = "Nome de usuário inválido.\nTente novamente."
LoginScreenUserNameNotFound = "Nome de usuário não encontrado.\nTente novamente ou crie uma nova conta."
LoginScreenPeriodTimeExpired = "Sinto muito, mas você já usou todos os seus minutos disponíveis deste mês. Volte no início do próximo mês."
LoginScreenNoNewAccounts = "Sinto muito, no momento não estamos aceitando novas contas."
LoginScreenTryAgain = "Tente novamente"


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
GlobalSpeedChatName = "Chat rápido"

# Toontown Speedchat
SCMenuPromotion  = "PROMOCIONAL"
SCMenuElection  = "ESCOLHA"
SCMenuEmotions  = "EMOÇÕES"
SCMenuCustom    = "MINHAS FRASES"
SCMenuResistance = "UNIR!"
SCMenuPets      = "BICHINHOS"
SCMenuPetTricks = "TRUQUES"
SCMenuCog       = "FALAS DE COGS"
SCMenuHello     = "OLÁ"
SCMenuBye       = "TCHAU"
SCMenuHappy     = "FELIZ"
SCMenuSad       = "TRISTE"
SCMenuFriendly  = "AMIGÁVEL"
SCMenuSorry     = "DESCULPE"
SCMenuStinky    = "FEDIDO"
SCMenuPlaces    = "LUGARES"
SCMenuToontasks = "TAREFAS TOON"
SCMenuBattle    = "BATALHA"
SCMenuGagShop   = "LOJA DE PIADAS"
SCMenuFactory   = "FÁBRICA"
SCMenuKartRacing   = "CORRIDA"
SCMenuFactoryMeet = "ENCONTRO"
SCMenuCFOBattle = "DIRETOR FINANCEIRO"
SCMenuCFOBattleCranes = "GUINDASTES"
SCMenuCFOBattleGoons = "BRUTAMONTES"
SCMenuCJBattle = "JUIZ-CHEFE"
SCMenuGolf   = "GOLF"
SCMenuWhiteList = "WHITELIST"
SCMenuPlacesPlayground           = "PÁTIO"
SCMenuPlacesEstate               = "PROPRIEDADE"
SCMenuPlacesCogs                 = "COGS"
SCMenuPlacesWait                 = "ESPERE"
SCMenuFriendlyYou                = "Você..."
SCMenuFriendlyILike              = "Eu gosto de..."
SCMenuPlacesLetsGo               = "Vamos..."
SCMenuToontasksMyTasks           = "MINHAS TAREFAS"
SCMenuToontasksYouShouldChoose   = "Eu acho que você deveria escolher..."
SCMenuBattleGags                 = "PIADAS"
SCMenuBattleTaunts               = "PROVOCAÇÕES"
SCMenuBattleStrategy             = "ESTRATÉGIA"

# FriendSecret.py
FriendSecretNeedsPasswordWarningTitle = "Controles disponíveis aos pais"
FriendSecretNeedsPasswordWarning = """Para pegar ou digitar um segredo, você deve inserir a Senha de pais. Você pode desativar esta solicitação alterando as suas opções de Amigos secretos."""
FriendSecretNeedsPasswordWarningOK = lOK
FriendSecretNeedsPasswordWarningCancel = lCancel
FriendSecretNeedsPasswordWarningWrongPassword = """Esta não é a senha correta. Insira a Senha de pais criada na compra desta conta. Não é a mesma senha usada para os jogos."""
FriendSecretIntro = "Se você estiver jogando Toontown Online da Disney com alguém que conhece no mundo real, poderá tornar-se Amigo secreto dessa pessoa. Você pode conversar com seus Amigos secretos usando o teclado. Os outros Toons não entenderão o que vocês estiverem falando.\n\nVocê pode conseguir isto obtendo um segredo. Conte o segredo só ao seu amigo, e a mais ninguém. Quando o seu amigo digitar o seu segredo na tela, vocês dois serão Amigos secretos em Toontown!"
FriendSecretGetSecret = "Obter um segredo"
FriendSecretEnterSecret = "Se você tiver um segredo de alguém conhecido, digite-o aqui."
FriendSecretOK = lOK
FriendSecretEnter = "Inserir segredo"
FriendSecretCancel = lCancel
FriendSecretGettingSecret = "Obtendo segredo. . ."
FriendSecretGotSecret = "Este é o seu novo segredo. Não deixe de anotá-lo em algum lugar!\n\nVocê só pode dar este segredo a uma pessoa. Depois que alguém digitar o seu segredo, ele não funcionará para nenhuma outra pessoa. Se você quiser dar um segredo para mais de uma pessoa, obtenha outro.\n\nO segredo só funcionará nos próximos dois dias. O seu amigo terá que digitá-lo antes que expire, caso contrário, não funcionará.\n\nO segredo é:"
FriendSecretTooMany = "Sinto muito, você não pode ter mais segredos hoje. Você já obteve mais do que a parte que lhe cabia!\n\nTente novamente amanhã."
FriendSecretTryingSecret = "Tentando usar segredo. . ."
FriendSecretEnteredSecretSuccess = "Agora, você é Amigo secreto de %s!"
FriendSecretEnteredSecretUnknown = "Este segredo não existe. Tem certeza de que digitou certo?\n\nSe você tiver digitado certo, ele pode ter expirado. Peça ao seu amigo para pegar outro segredo para você (ou pegue um novo você mesmo e dê ao seu amigo)."
FriendSecretEnteredSecretFull = "Você não pode fazer amizade com %s porque um de vocês dois possui amigos demais na lista."
FriendSecretEnteredSecretFullNoName = "Vocês não podem fazer amizade porque um de vocês dois possui amigos demais na lista."
FriendSecretEnteredSecretSelf = "Você acabou de digitar seu próprio segredo! Agora, ninguém mais poderá usar este segredo."
FriendSecretEnteredSecretWrongProduct = "You have entered the wrong type of True Friend Code.\nThis game uses codes that begin with '%s'."
FriendSecretNowFriends = "Agora, você é Amigo secreto de %s!"
FriendSecretNowFriendsNoName = "Agora, vocês são Amigos secretos!"
FriendSecretDetermineSecret = "What type of True Friend would you like to make?"
FriendSecretDetermineSecretAvatar = "Avatar"
FriendSecretDetermineSecretAvatarRollover = "A friend only in this game"
FriendSecretDetermineSecretAccount = "Account"
FriendSecretDetermineSecretAccountRollover = "A friend across the Disney.com network"

# FriendInvitee.py
FriendInviteeTooManyFriends = "%s quer fazer amizade com você, mas você já tem muitos amigos em sua lista!"
FriendInviteeInvitation = "%s quer fazer amizade com você."
FriendInviteeOK = lOK
FriendInviteeNo = "Não"

# FriendInviter.py
FriendOnline = "has come online."
FriendOffline = "has gone offline."
FriendInviterOK = lOK
FriendInviterCancel = lCancel
FriendInviterStopBeingFriends = "Interromper amizade"
FriendInviterYes = lYes
FriendInviterNo = lNo
FriendInviterClickToon = "Clique no Toon com o qual deseja fazer amizade."
FriendInviterTooMany = "Você tem amigos demais na lista e não pode adicionar mais nenhum agora. Você terá que remover alguns amigos se desejar fazer amizade com %s."
FriendInviterNotYet = "Deseja fazer amizade com %s?"
FriendInviterCheckAvailability = "Verificando se %s está disponível."
FriendInviterNotAvailable = "%s está ocupado(a) agora; tente novamente mais tarde."
FriendInviterNotOpen = "%s does not have open chat, use secrets to make friends"
FriendInviterWentAway = "%s saiu."
FriendInviterAlready = "%s já é seu(sua) amigo(a)."
FriendInviterAlreadyInvited = "%s já recebeu o convite."
FriendInviterAskingCog = "Pedindo a %s para fazer amizade com você."
FriendInviterAskingPet = "%s pula à sua volta, corre em círculos e lambe seu rosto."
FriendInviterAskingMyPet = "%s já é seu(sua) MELHOR amigo(a)."
FriendInviterEndFriendship = "Tem certeza de que você deseja interromper a amizade com %s?"
FriendInviterFriendsNoMore = "%s não é mais seu(sua) amigo(a)."
FriendInviterSelf = "Você já tem amizade com você mesmo(a)!"
FriendInviterIgnored = "%s está ignorando você."
FriendInviterAsking = "Pedindo a %s para fazer amizade com você."
FriendInviterFriendSaidYes = "%s disse sim!"
FriendInviterFriendSaidNo = "%s disse não, valeu."
FriendInviterPlayerFriendSaidYes = "You are now friends with %s's player, %s!"
FriendInviterFriendSaidNo = "%s said no, thank you."
FriendInviterFriendSaidNoNewFriends = "%s não está procurando novos amigos no momento."
FriendInviterTooMany = "%s já tem amigos demais!"
FriendInviterMaybe = "%s não conseguiu responder."
FriendInviterDown = "Não foi possível fazer amizade agora."

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
    "Aceno",
    "Feliz",
    "Triste",
    "Raivoso",
    "Sonolento",
    "Dar de ombros",
    "Dançante",
    "Piscar",
    "Entediado",
    "Palmas",
    "Surpreso",
    "Confuso",
    "Debochar",
    "Saudar",
    "Muito triste",
    "Sorrisão",
    "Risada",
    lYes,
    lNo,
    lOK,
    ]

EmoteWhispers = [
    "%s acena.",
    "%s está feliz.",
    "%s está triste.",
    "%s está furioso.",
    "%s está sonolento.",
    "%s dá de ombros.",
    "%s dança.",
    "%s pisca.",
    "%s está entediado.",
    "%s aplaude.",
    "%s está surpreso.",
    "%s está confuso.",
    "%s debocha de você.",
    "%s saúda você.",
    "%s está muito triste.",
    "%s sorri.",
    "%s dá risada.",
    "%s diz '"+lYes+"'.",
    "%s diz '"+lNo+"'.",
    "%s diz '"+lOK+"'.",
    ]

# Reverse lookup:  get the index from the name.
EmoteFuncDict = {
    "Aceno"   : 0,
    "Feliz"  : 1,
    "Triste"    : 2,
    "Raivoso"  : 3,
    "Sonolento" : 4,
    "Dar de ombros"  : 5,
    "Dançante"  : 6,
    "Piscar"   : 7,
    "Entediado"  : 8,
    "Palmas" : 9,
    "Surpreso" : 10,
    "Confuso"  : 11,
    "Debochar"  : 12,
    "Saudar"    : 13,
    "Muito triste" : 14,
    "Sorrisão"    : 15,
    "Risada" : 16,
    lYes    : 17,
    lNo     : 18,
    lOK     : 19,
    }

# SuitDialog.py
SuitBrushOffs = {
    'f':  ["Estou atrasado para uma reunião.",
           ],
    'p':  ["Sai fora.",
           ],
    'ym': ['As vaquinhas de presépio dizem NÃO.',
           ],
    None: ["É o meu dia de folga.",
           "Acho que você está no escritório errado.",
           "Fale para o seu pessoal falar com o meu.",
           "Você não tem cacife para se encontrar comigo.",
           "Fale com o meu assistente."]
    }

SuitFaceoffTaunts = {
    'b':  ["Você tem uma doação para mim?",
           "Você vai detestar perder a parada.",
           "Você não vai ter salvação.",
           "Sou \"A Positivo\", portanto, vou ganhar.",
           "\"O\"não seja tão \"Negativo\".",
           "É uma surpresa você ter me achado; não tenho parada.",
           "Vou precisar fazer uma rápida contagem em você.",
           "Em breve, você vai precisar comer biscoito e tomar um suco.",
           "Quando eu terminar, você vai precisar dar uma descansada.",
           "Só vai doer um pouquinho.",
           "Vou deixar você tonto.",
           "Na hora certa, só estou um pouquinho abaixo.",
           ],
    'm':  ["Você não sabe com quem está se metendo.",
           "Nunca se meteu com alguém da minha turma?",
           "Isso é bom, quando um não quer dois não se misturam.",
           "Vamos fazer amizade.",
           "Parece um bom lugar para confraternizar.",
           "Não é confortável?",
           "Vocês estão se unindo com a derrota.",
           "Vou me juntar a você no negócio.",
           "Tem certeza de que está pronto para a união?",
           ],
    'ms': ["Prepare-se para uma sacudida.",
           "Melhor você sair do caminho.",
           "Olha a frente.",
           "Acho que é minha vez.",
           "Isso deve agitar você.",
           "Prepare-se para ser movido.",
           "Estou pronto para dar o meu passo.",
           "Cuidado Toon, você está em terreno instável.",
           "Este deve ser um momento de movimento.",
           "Sinto um impulso de derrotar você.",
           "Você ainda está tremendo?",
           ],
    'hh': ["Estou na sua frente nesta caçada.",
           "Você está caçando encrenca da grande.",
           "A sua cabeça está na mira do caçador de cabeças.",
           "Que bom, estava atrás de você.",
           "Vou perseguir você por isto.",
           "Fique de olho!",
           "Parece que você está perdido nesta caçada.",
           "Está indo pela mesma trilha que eu?",
           "Um troféu perfeito para a minha coleção.",
           "Você vai ter uma dor de cabeça...",
           "Não perca o rumo comigo.",
           ],
    'tbc': ["Cuidado, vou adoçar você.",
            "Pode me chamar de Coquinho.",
            "Tem certeza? Às vezes ajo como um Cãocadão.",
            "Finalmente, estava achando que você ia me deixar aqui à mercê das formigas.",
            "Vou queimar o seu coco.",
            "Não acha que eu sou um docinho de coco?",
            "Você vai virar cocada comigo.",
            "As pessoas me acham durão.",
            "Cuidado, eu sei a sua data de validade.",
            "Cuidado, sou uma fera neste jogo.",
            "Bater você vai ser mole.",
            ],
    'cr': ["ATAQUE!",
           "Você não é adequado para a minha corporação.",
           "Prepare-se para ser atacado.",
           "Parece que você está preparado para assumir o comando da aventura.",
           "Esta roupa não é apropriada para ambientes corporativos.",
           "Você parece estar bem vulnerável.",
           "É hora de botar os bens em seu nome.",
           "Estou em uma cruzada a favor da eliminação dos Toons.",
           "Você fica sem defesa contra as minhas idéias.",
           "Relaxa, você vai ver que vai ser melhor assim.",
           ],
    'mh': ["Está preparado para a minha tomada?",
           "Luz, câmera, ação!",
           "Vai começar a rodar.",
           "Hoje o papel do Toon derrotado será feito por - VOCÊ!",
           "Esta cena vai ser cortada.",
           "Já sei qual vai ser a minha motivação para esta cena.",
           "Está preparado para a sua cena final?",
           "Estou pronto para passar os seus créditos no final.",
           "Eu disse para você não me chamar.",
           "O show tem que continuar.",
           "Não tem negócio igual a este!",
           "Espero que você não se esqueça das suas falas.",
           ],
    'nc': ["Parece que o seu número está em alta.",
           "Prefere ser destruído com ou sem cobertura crocante?",
           "Agora, você está destruído.",
           "Já está na hora de dizimar todos estes números?",
           "Vamos fazer uma matemática.",
           "Onde você gostaria de fazer uma subtração hoje?",
           "Você me deu uma coisa para calcular!",
           "Não vai ser fácil.",
           "Vai em frente, pegue um número qualquer.",
           "Vou destruir você com os meus cálculos.",
           ],
    'ls': ["É hora de recolher o seu empréstimo.",
           "Você tem estado na pior.",
           "O empréstimo agora tem que ser pago.",
           "Hora de liquidar a dívida.",
           "Bom, você queria um adiantamento e conseguiu.",
           "Você terá que pagar por isso.",
           "É hora de devolver o que pegou.",
           "Pode me dar uma mãozinha?",
           "Ainda bem que você está aqui, isto está uma loucura.",
           "Podemos fazer um lanchinho?",
           "Deixe-me dar um tasco.",
           ],
    'mb': ["Está na hora de trazer os sacos.",
           "Posso ensacar isso.",
           "Papel ou plástico?",
           "Você tem o tíquete da bagagem?",
           "Lembre-se de que o dinheiro não vai fazer você feliz.",
           "Cuidado, tenho muita bagagem.",
           "Você está prestes a ficar no vermelho.",
           "O dinheiro vai fazer o seu mundo girar.",
           "Sou muito rico para o seu bico.",
           "Você nunca poderá ter tanto dinheiro!",
           ],
    'rb': ["Você foi roubado.",
           "Vou roubar esta vitória de você.",
           "Sou um chato de galochas!",
           "Espero que você ainda possa sorrir para o barão.",
           "Você terá que denunciar este roubo.",
           "Mãos ao alto.",
           "Sou um adversário nobre.",
           "Vou levar tudo o que você tem.",
           "Você pode chamar isto de roubo no bairro.",
           "Você já devia saber que não se fala com estranhos.",
           ],
    'bs': ["Nunca vire as costas para mim.",
           "Você não vai voltar mesmo.",
           "Retire o que disse, ou então...!",
           "Sou bom em cortar custos.",
           "Tenho as costas quentes.",
           "Agora, não dá mais para voltar atrás.",
           "Sou o melhor e posso provar.",
           "Ôôô, parado aí, Toon.",
           "Deixe-me dar cobertura a você.",
           "Você vai ter uma dor de cabeça infernal.",
           "Tenho um golpe perfeito.",
           ],
    'bw': ["Quero sair bem na foto.",
           "Você me arrepia os cabelos.",
           "Posso deixar assim para sempre, se quiser.",
           "Parece que você vai ficar com a cara boa.",
           "Você não consegue encarar a verdade.",
           "Acho que é sua vez de mudar de cor.",
           "Estou tão feliz que você chegou na hora de mudar o visual.",
           "Você está encrencado.",
           "Vou deixar você doidão.",
           "Sou um baita de um Toonzinho.",
           ],
    'le': ["Cuidado, sou legal mas nem tanto.",
           "Eu pulo de galho em galho, mas alguns quebram.",
           "Vou fazer a lei chegar até você.",
           "Você já devia saber que tenho instintos criminosos.",
           "Vou fazer você ter pesadelos jurídicos.",
           "Você não vai ganhar esta batalha.",
           "Isto é tão divertido que deveria ser proibido por lei.",
           "Legalmente falando, você é muito pequeno para lutar comigo.",
           "Não há limites para os meus botes.",
           "Chamo isso de prisão de cidadão.",
           ],
    'sd': ["Você nunca saberá quando vou parar.",
           "Deixe-me levar você para uma volta.",
           "Vida social é comigo mesmo.",
           "Vou colocar você em um agito.",
           "Você parece precisar de animação.",
           "A festa está rolando, mas Toons não entram.",
           "Você não vai gostar do meu pitaco nisto.",
           "Você vai ficar fora de controle.",
           "Você se importa de dar umas voltinhas comigo?",
           "Tenho minha própria teoria sobre o assunto.",
           ],
    'f': ["Vou falar sobre você com o chefe!",
          "Posso ser apenas um puxa-saco, mas sou demais.",
          "Estou usando você para subir os vários degraus dentro da empresa.",
          "Você não vai gostar do jeito como eu trabalho.",
          "O chefe está contando comigo para deter você.",
          "Você vai ficar bonito no meu currículo.",
          "Você terá que passar por cima de mim primeiro.",
          "Vamos ver como você classifica meu desempenho funcional.",
          "Eu me sobressaio na eliminação de Toons.",
          "Você jamais conhecerá o meu chefe.",
          "Vou mandar você de volta para o Pátio.",
          ],
    'p':  ["Eu vou apagar você!",
           "Ei, você não pode ficar mandando em mim.",
           "Sou o número 2!",
           "Vou cortar você.",
           "Vou ter que me fazer mais claro.",
           "Deixe-me ir direto ao ponto.",
           "Rápido, eu fico irritado com facilidade.",
           "Odeio quando as coisas ficam bobas.",
           "Então, você quer arriscar a própria sorte?",
           "Você me passou o lápis?",
           "Cuidado, posso deixar uma marca.",
           ],
    'ym': ["Concordo com tudo.",
           "Não sei o que significa não.",
           "Quer me conhecer? Eu digo sim sempre.",
           "Você precisa de uma força positiva.",
           "Vou deixar uma impressão positiva.",
           "Ainda não me enganei.",
           "Sim, estou pronto para você.",
           "Acha mesmo que quer fazer isto?",
           "Você certamente terminará com saldo positivo nessa.",
           "Confirmando a hora da sua reunião.",
           "Não aceito não como resposta.",
           ],
    'mm': ["Vou entrar neste negócio.",
           "Às vezes, os piores venenos vêm em pequenos frascos.",
           "Nenhum trabalho é insignificante para mim.",
           "Quero o trabalho feito direito, por isso eu mesmo o faço.",
           "Você precisa de alguém para gerenciar os seus bens.",
           "Que bom, um projeto.",
           "Bem, você conseguiu me achar.",
           "Acho que você precisa de alguma organização.",
           "Vou cuidar de você em dois tempos.",
           "Estou observando tudo que você faz.",
           "Tem certeza de que deseja fazer isto?",
           "Vamos fazer da minha maneira.",
           "Vou estar na sua cola.",
           "Posso ser bem intimidador.",
           ],
    'ds': ["Você está caindo no meu golpe!",
           "Você vai encolher com meu ataque.",
           "Espere retornos minúsculos.",
           "Você vai deixar de existir.",
           "Não me peça nenhuma dispensa.",
           "Vou precisar fazer alguns cortes.",
           "As coisas parecem estar despedaçadas para você.",
           "Por que você parece tão machucado?",
           ],
    'cc': ["Surpreso de saber de mim?",
           "Você ligou?",
           "Está pronto para aceitar as minhas tarifas?",
           "Este aqui sempre recolhe alguma coisa.",
           "Eu opero bem as linhas.",
           "Espere um segundo, estou aqui.",
           "Estava esperando a minha ligação?",
           "Estava torcendo para você atender a minha ligação.",
           "Vou deixar uma sensação tocante.",
           "Sempre faço ligações diretas.",
           "Cara, tem boi na linha.",
           "Esta ligação terá um custo para você.",
           "Você tem um pepino nesta linha.",
           ],
    'tm': ["Meu plano é tornar isto inconveniente para você.",
           "Posso incluir você em um seguro?",
           "Você não deveria ter me atendido.",
           "Você não vai conseguir se livrar de mim agora.",
           "Tá chateado? Que bom.",
           "Estava pensando em atropelar você.",
           "Vou inverter as cobranças desta ligação.",
           "Tenho alguns itens bem caros para você hoje.",
           "Se deu mal, eu faço ligações locais.",
           "Estou preparado para fechar este negócio rapidinho.",
           "Vou usar um monte de recursos seus.",
           ],
    'nd': ["Na minha opinião, seu nome está na lama.",
           "Espero que não se importe se eu jogar o seu nome na boca das matildes.",
           "A gente já não se conhece?",
           "Depressa, vou almoçar com o Dr. Celebridade.",
           "Eu falei que conheço o Amizade Fácil?",
           "Você nunca vai me esquecer.",
           "Conheço todas as pessoas certas para detonar você.",
           "Acho que vou passar aí.",
           "Estou a fim de detonar alguns Toons.",
           "Eu te disse, detonei.",
           ],
    'gh': ["Diz aí, Toon.",
           "O bicho vai pegar.",
           "Vou gostar disso.",
           "Você vai acabar vendo as minhas garras.",
           "Vamos assinar embaixo.",
           "Vamos direto ao que interessa.",
           "Não cutuca a onça com vara curta, ou você vai acabar mal.",
           "Você vai acabar gostando da minha pinta.",
           "Olha que eu viro uma onça.",
           "Você não vai escapar das minhas garras.",
           "Você quer que eu safe a onça?",
           "Se ficar o bicho come, se correr o bicho pega.",
           "As marcas das minhas unhas afiadas estão na parede.",
           ],
    'sc': ["Vamos logo acabar com esta farsa.",
           "Você está prestes a ficar no vermelho.",
           "Você está prestes a pagar taxas abusivas.",
           "O projeto vai ser de fachada.",
           "Esta fraude vai ser moleza.",
           "Logo, logo você vai cair na minha arapuca.",
           "Vamos embromar um pouquinho.",
           "Veio cedo para ver o meu truque, né?",
           "Tenho pavio curto com Toons.",
           "Logo vou armar minha armadilha para você.",
           "Você está prestes a cair na minha lábia.",
           ],
    'pp': ["Meu aperto de mão é forte.",
           "Minha mão é de ferro.",
           "Você não quer que a vaca vá pro brejo, ou quer?",
           "Seu sorriso vai ficar pálido como leite.",
           "Tenho um lugar para você, mas não pense que sou mão-aberta.",
           "Deixe e pagar na mesma moeda.",
           "Dou tchau com a mão fechada.",
           "Vou provar que você não está sonhando.",
           "Cabeças vão rolar, e eu vou ganhar.",
           "Dou uma moedinha pelas suas piadas.",
           ],
    'tw': ["Vamos ter que dar duro.",
           "É o Pão-duro.",
           "Vou ter que cortar a sua verba.",
           "É a melhor oferta que você pode fazer?",
           "Vamos logo. Tempo é dinheiro.",
           "Você vai descobrir como dou duro.",
           "Você está na corda bamba.",
           "Prepare-se para a dureza.",
           "Você não conhece o pão que o diabo amassou.",
           "Vou ter que apertar o cinto.",
           "Vou fazer um rombo no seu orçamento.",
           ],
    'bc': ["Adoro subtrair Toons.",
           "Pode contar comigo para fazer você pagar.",
           "O negócio é contar as moedinhas.",
           "Contar é comigo mesmo.",
           "Sou um contador de balinhas.",
           "Sua planilha de gastos está excedendo o limite.",
           "É hora de fazer uma auditoria.",
           "Vamos entrar no meu escritório.",
           "Onde você estava? Eu contava com você.",
           "Estou esperando por você há um milhão de horas.",
           "Você não vale um níquel.",
           ],
    'bf': ["Parece que você chegou na hora do lanche.",
           "Estou pronto para o banquete.",
           "Sou um comedor de Toons.",
           "Êba, hora do almoço.",
           "Na hora certa! Preciso de um lanchinho.",
           "Gostaria de alguma opinião sobre o meu desempenho.",
           "Vamos falar sobre o que interessa.",
           "Você vai descobrir que tenho um talento imensurável.",
           "Bom, preciso de um pequeno estímulo.",
           "Adoraria se você almoçasse comigo.",
           ],
    'tf': ["Está na hora de nosso duelo!",
           "Melhor encarar a derrota.",
           "Prepare-se para enfrentar o seu pior pesadelo!",
           "Encare os fatos: eu sou melhor que você.",
           "Duas cabeças pensam melhor que uma.",
           "Se um não quer, dois não brigam. Quer brigar?",
           "Você está duplamente encrencado.",
           "Qual face você quer que o derrote?",
           "Eu sou demais para você.",
           "Você não sabe com quem está se metendo.",
           "Você está preparado para encarar sua derrota?",
           ],
    'dt': ["Você terá trabalho em dobro comigo.",
           "Veja se você consegue enfrentar meu golpe duplo.",
           "Trabalho para um ARMÁRIO 4x4 muito mau.",
           "Está na hora de um golpe duplo.",
           "Meu plano é ter duas FONTES.",
           "Você não vai gostar do meu jogo duplo.",
           "Talvez queira pensar duas vezes nisso.",
           "Prepare-se para uma LIGAÇÃO dupla.",
           "Talvez queira aplicar uma dose dupla contra mim.",
           "Duplas, alguém??",
           ],
    'ac': ["Eu vou botar você prá correr desta cidade!",
           "Está ouvindo uma sirene?",
           "Vou gostar disso.",
           "Adoro a emoção da perseguição.",
           "Vou dar um passa-fora.",
           "Você tem seguro?",
           "Espero que tenha trazido uma maca.",
           "Duvido que você possa comigo.",
           "É só ralação a partir daqui.",
           "Em breve você vai precisar de uma ambulância.",
           "Não é piada.",
           "Vou passar a parada para você.",
           ]
    }

# These are all the standard SpeedChat phrases.
# The indices must fit into 16 bits (0..65535)
SpeedChatStaticText = {
    # top-level
    1 : lYes,
    2 : lNo,
    3 : lOK,

    # Hello
    100 : "Oi!",
    101 : "Olá!",
    102 : "E aí?",
    103 : "Ôpa!",
    104 : "Tudo certo?",
    105 : "Oi, pessoal!",
    106 : "Bem-vindo a Toontown!",
    107 : "Tudo em cima?",
    108 : "Tudo bem?",
    109 : "Alô?",

    # Bye
    200 : "Tchau!",
    201 : "Até mais!",
    202 : "Te vejo por aí!",
    203 : "Bom dia pra você!",
    204 : "Divirta-se!",
    205 : "Boa sorte!",
    206 : "Já volto.",
    207 : "Tenho que ir.",
    208 : "Eu volto já!",
    209 : "Eu só tenho alguns minutos.",

    # Happy
    300 : ":-)",
    301 : "Valeu!",
    302 : "Maneiro!",
    303 : "Legal!",
    304 : "Iuhuu!",
    305 : "É isso aí!",
    306 : "Ah, ah!",
    307 : "He, he!",
    308 : "Uau!",
    309 : "Demais!",
    310 : "Iahuuuuu!",
    311 : "Nossa!",
    312 : "Uhuu!",
    313 : "Iupii!!",
    314 : "Dez!",
    315 : "Toontástico!",

    # Sad
    400 : ":-(",
    401 : "Ah, não!",
    402 : "Êpa!",
    403 : "Droga!",
    404 : "Ai, ai, ai!",
    405 : "Ahhh!",
    406 : "Puxa!",
    407 : "Não!!!",
    408 : "Pôxa vida!",
    409 : "Hã?",
    410 : "Preciso de mais pontos de Risadas.",

    # Friendly
    500 : "Valeu!",
    501 : "Sem problemas.",
    502 : "De nada!",
    503 : "Sempre que quiser!",
    504 : "Não, obrigado.",
    505 : "Bom trabalho de equipe!",
    506 : "Isso foi divertido!",
    507 : "Vamos ser amigos!",
    508 : "Vamos trabalhar juntos!",
    509 : "Vocês são demais!",
    510 : "Você é novo aqui?",
    511 : "Ganhou?",
    512 : "Acho arriscado prá você.",
    513 : "Quer ajuda?",
    514 : "Você me ajuda?",
    515 : "Você já veio aqui antes?",

    # Friendly "Você..."
    600 : "Você parece legal.",
    601 : "Você é incrível!",
    602 : "Você é maneiro!",
    603 : "Você é um gênio!",

    # Friendly "Gosto..."
    700 : "Gosto do seu nome.",
    701 : "Gosto do seu jeito.",
    702 : "Gosto da sua camisa.",
    703 : "Gosto da sua saia.",
    704 : "Gosto do seu short.",
    705 : "Gosto deste jogo!",

    # Sorry
    800 : "Desculpe!",
    801 : "Ops!",
    802 : "Desculpe, agora estou lutando com Cogs!",
    803 : "Desculpe, agora estou conseguindo balinhas!",
    804 : "Desculpe, agora estou completando uma Tarefa Toon!",
    805 : "Desculpe, tive que sair de repente.",
    806 : "Desculpe, fiquei preso.",
    807 : "Desculpe, não posso.",
    808 : "Não pude esperar mais.",
    809 : "Não entendi.",
    810 : "Use o %s." % GlobalSpeedChatName,
    811 : "Desculpe, estou ocupado pescando!",
    812 : "Desculpe, estou dentro de um prédio!",
    813 : "Desculpe, estou ajudando um amigo!",
    814 : "Desculpe, estou ocupado numa corrida de kart!",
    815 : "Sorry, I'm busy gardening!",

    # Stinky
    900 : "Ôpa!",
    901 : "Vá embora!!",
    902 : "Pare com isso!",
    903 : "Isso não foi legal!",
    904 : "Não seja mau!",
    905 : "Você é nojento!",
    906 : "Envie um relatório de problemas.",
    907 : "Estou atolado.",

    # Places
    1000 : "Vamos!",
    1001 : "Você pode se teletransportar até a mim?",
    1002 : "Podemos ir?",
    1003 : "Para onde devemos ir?",
    1004 : "Em que direção?",
    1005 : "Esta direção.",
    1006 : "Siga-me.",
    1007 : "Espere por mim!",
    1008 : "Vamos esperar pelo meu amigo.",
    1009 : "Vamos encontrar outros toons.",
    1010 : "Espere aqui.",
    1011 : "Espere um minuto.",
    1012 : "Vamos nos encontrar aqui.",
    1013 : "Você pode ir até a minha casa?",
    1014 : "Não espere por mim.",
    1015 : "Espere!",
    1016 : "Come check out my garden.",

    # Places "Vamos..."
    1100 : "Vamos pegar o bondinho!",
    1101 : "Vamos voltar para o pátio!",
    1102 : "Vamos lutar com %s!" % Cogs,
    1103 : "Vamos tomar um edifício %s!" % Cog,
    1104 : "Vamos entrar no elevador!",
    1105 : "Vamos para o Centro de Toontown!",
    1106 : "Vamos para o Porto do Donald!",
    1107 : "Vamos para a Melodilândia da Minnie!",
    1108 : "Vamos para os Jardins da Margarida!",
    1109 : "Vamos para O Brrrgh!",
    1110 : "Vamos para a Sonholândia do Donald!",
    1111 : "Vamos para a minha casa!",
    1112 : "Vamos para a minha casa!",
    1113 : "Vamos para a sua casa!",
    1114 : "Vamos para o Quartel do Robô Vendedor!",
    1115 : "Vamos lutar com o VP!",
    1116 : "Vamos entrar na Fábrica!",
    1117 : "Vamos pescar!",
    1118 : "Vamos pescar na minha casa!",
    1119 : "Vamos para o Quartel do Robô Mercenário!",
    1120 : "Vamos lutar com o Diretor Financeiro!",
    1121 : "Vamos entrar na Casa da Moeda!",
    1122 : "Vamos para o Quartel do Robô da Lei!",
    1123 : "Vamos lutar com o Juiz Chefe!",
    1124 : "Vamos para o Escritório do Promotor Público!",

    # Toontasks
    1200 : "Em que Tarefa Toon você está trabalhando?",
    1201 : "Vamos trabalhar nisto.",
    1202 : "Isto não é o que estou procurando.",
    1203 : "Vou procurar isto.",
    1204 : "Não está nesta rua.",
    1205 : "Não encontrei ainda.",
    1206 : "Preciso de mais Méritos por Cogs.",
    1207 : "Preciso de mais peças de vestimentas de Cogs.",
    1208 : "Não é disso que você precisa.",
    1209 : "Achei o que você precisa.",
    1210 : "Eu preciso de mais Cograna.",
    1211 : "Eu preciso de mais Avisos ao Júri.",
    1213 : "Eu preciso de mais Peças de Vestimenta de Robô Mercenário.",
    1214 : "Eu preciso de mais Peças de Vestimenta de Robô da Lei.",

    1299 : "Preciso pegar uma Tarefa Toon.",

    # Toontasks "Acho que você devia escolher..."
    1300 : "Acho que você devia escolher Toonar.",
    1301 : "Acho que você devia escolher Sonora.",
    1302 : "Acho que você devia escolher Cadente.",
    1303 : "Acho que você devia escolher Armadilha.",
    1304 : "Acho que você devia escolher Isca.",

    # Battle
    1400 : "Anda!",
    1401 : "Que tiro!",
    1402 : "Que piada!",
    1403 : "Não me acertou!",
    1404 : "Conseguiu!",
    1405 : "Conseguimos!",
    1406 : "Ataque!",
    1407 : "Moleza!",
    1408 : "Esta foi fácil!",
    1409 : "Corre!",
    1410 : "Socorro!",
    1411 : "Ufa!",
    1412 : "Estamos em apuros.",
    1413 : "Preciso de mais piadas.",
    1414 : "Preciso de uma Toonar.",
    1415 : "Você deve passar.",
    1416 : "Vamos conseguir!",

    # Battle "Vamos usar..."
    1500 : "Vamos usar toonar!",
    1501 : "Vamos usar armadilha!",
    1502 : "Vamos usar isca!",
    1503 : "Vamos usar sonora!",
    1504 : "Vamos usar lançamento!",
    1505 : "Vamos usar esguicho!",
    1506 : "Vamos usar cadente!",

    # Battle TAUNTS
    1520 : "É hora do Rock!",
    1521 : "Isso deve doer.",
    1522 : "Pegue!",
    1523 : "Entrega especial!",
    1524 : "Você ainda está aqui?",
    1525 : "Ai, que medo!",
    1526 : "Esta vai deixar cicatriz!",

    # Battle STRATEGY
    1550 : "Vou usar uma armadilha.",
    1551 : "Vou usar uma isca.",
    1552 : "Vou usar uma cadente.",
    1553 : "Você devia usar uma piada diferente.",
    1554 : "Vamos todos no mesmo Cog.",
    1555 : "Você devia escolher um Cog diferente.",
    1556 : "Vá no Cog mais fraco primeiro.",
    1557 : "Vá no Cog mais forte primeiro.",
    1558 : "Economize as piadas mais poderosas.",
    1559 : "Não use som em Cogs dominados por iscas.",

    # Gag Shop
    1600 : "Tenho piadas suficientes.",
    1601 : "Preciso de mais balinhas.",
    1602 : "Eu também.",
    1603 : "Vamos nessa!",
    1604 : "Mais um?",
    1605 : "Jogar de novo?",
    1606 : "Vamos jogar de novo.",

    # Factory
    1700 : "Vamos nos separar.",
    1701 : "Vamos ficar juntos.",
    1702 : "Vamos lutar com os Cogs.",
    1703 : "Pise no interruptor.",
    1704 : "Passe pela porta.",

    # Sellbot Factory
    1803 : "Estou na Entrada principal.",
    1804 : "Estou no Salão.",
    1805 : "Estou no corredor fora do Salão.",
    1806 : "Estou no corredor fora do Salão.",
    1807 : "Estou na Sala de engrenagens.",
    1808 : "Estou na Sala da caldeira.",
    1809 : "Estou na Passarela leste.",
    1810 : "Estou no Misturador de tinta.",
    1811 : "Estou no Depósito do Misturador de tinta.",
    1812 : "Estou na Passarela do Silo Oeste.",
    1813 : "Estou na Sala de tubulações.",
    1814 : "Estou nas escadas da Sala de tubulações.",
    1815 : "Estou na Sala de dutos.",
    1816 : "Estou na Entrada lateral.",
    1817 : "Estou no Beco sinistro.",
    1818 : "Estou fora do Salão de lava.",
    1819 : "Estou no Salão de lava.",
    1820 : "Estou no Depósito de lava.",
    1821 : "Estou na Passarela oeste.",
    1822 : "Estou na Sala de óleo.",
    1823 : "Estou na Vigilância do Armazém.",
    1824 : "Estou no Armazém.",
    1825 : "Estou fora do Misturador de tinta.",
    1827 : "Estou fora da Sala de óleo.",
    1830 : "Estou na Sala de controle do Silo Leste.",
    1831 : "Estou na Sala de controle do Silo Oeste.",
    1832 : "Estou na Sala de controle do Silo Central.",
    1833 : "Estou no Silo Leste.",
    1834 : "Estou no Silo Oeste.",
    1835 : "Estou no Silo Central.",
    1836 : "Estou no Silo Oeste.",
    1837 : "Estou no Silo Leste.",
    1838 : "Estou na Passarela do Silo Leste.",
    1840 : "Estou no topo do Silo Oeste.",
    1841 : "Estou no topo do Silo Leste.",
    1860 : "Estou no Elevador do Silo Oeste.",
    1861 : "Estou no Elevador do Silo Leste.",

    # Sellbot Factory continued
    1903 : "Vamos nos encontrar na Entrada principal.",
    1904 : "Vamos nos encontrar no Salão.",
    1905 : "Vamos nos encontrar no corredor fora do salão.",
    1906 : "Vamos nos encontrar no corredor fora do salão.",
    1907 : "Vamos nos encontrar na Sala de engrenagens.",
    1908 : "Vamos nos encontrar na Sala da caldeira.",
    1909 : "Vamos nos encontrar na Passarela leste.",
    1910 : "Vamos nos encontrar no Misturador de tinta.",
    1911 : "Vamos nos encontrar no Depósito do Misturador de tinta.",
    1912 : "Vamos nos encontrar na Passarela do Silo Oeste.",
    1913 : "Vamos nos encontrar na Sala de tubulações.",
    1914 : "Vamos nos encontrar nas escadas da Sala de tubulações.",
    1915 : "Vamos nos encontrar na Sala de dutos.",
    1916 : "Vamos nos encontrar na Entrada lateral.",
    1917 : "Vamos nos encontrar no Beco sinistro.",
    1918 : "Vamos nos encontrar fora do Salão de lava.",
    1919 : "Vamos nos encontrar no Salão de lava.",
    1920 : "Vamos nos encontrar no Depósito de lava.",
    1921 : "Vamos nos encontrar na Passarela oeste.",
    1922 : "Vamos nos encontrar na Sala de óleo.",
    1923 : "Vamos nos encontrar na Vigilância do Armazém.",
    1924 : "Vamos nos encontrar no Armazém.",
    1925 : "Vamos nos encontrar fora do Misturador de tinta.",
    1927 : "Vamos nos encontrar fora da Sala de óleo.",
    1930 : "Vamos nos encontrar na Sala de controle do Silo Leste.",
    1931 : "Vamos nos encontrar na Sala de controle do Silo Oeste.",
    1932 : "Vamos nos encontrar na Sala de controle do Silo Central.",
    1933 : "Vamos nos encontrar no Silo Leste.",
    1934 : "Vamos nos encontrar no Silo Oeste.",
    1935 : "Vamos nos encontrar no Silo Central.",
    1936 : "Vamos nos encontrar no Silo Oeste.",
    1937 : "Vamos nos encontrar no Silo Leste.",
    1938 : "Vamos nos encontrar na Passarela do Silo Leste.",
    1940 : "Vamos nos encontrar no topo do Silo Oeste.",
    1941 : "Vamos nos encontrar no topo do Silo Leste.",
    1960 : "Vamos nos encontrar no Elevador do Silo Oeste.",
    1961 : "Vamos nos encontrar no Elevador do Silo Leste.",

    # These are used only for the style settings in the OptionsPage
    # These should never actually be spoken or listed on the real speed chat
    2000 : "Lilás",
    2001 : "Azul",
    2002 : "Ciano",
    2003 : "Azul petróleo",
    2004 : "Verde",
    2005 : "Amarelo",
    2006 : "Laranja",
    2007 : "Vermelho",
    2008 : "Rosa",
    2009 : "Marrom",

    # CFO battle
    2100 : "Opere o guindaste.",
    2101 : "Posso operar o guindaste?",
    2102 : "Preciso de prática para operar o guindaste.",
    2103 : "Escolha um brutamontes desativado.",
    2104 : "Jogue o brutamontes no Diretor Financeiro.",
    2105 : "Agora jogue um cofre!",
    2106 : "Não jogue o cofre agora!",
    2107 : "O cofre vai derrubar o capacete dele.",
    2108 : "O cofre vai virar o novo capacete dele.",
    2109 : "Não consigo chegar a nenhum cofre.",
    2110 : "Não consigo chegar a nenhum brutamontes.",

    2120 : "Desative os brutamontes.",
    2121 : "Prefiro desativar os brutamontes.",
    2122 : "Preciso de prática para desativar brutamontes.",
    2123 : "Fique por perto.",
    2124 : "Fique circulando.",
    2125 : "Preciso circular.",
    2126 : "Procure alguém que precise de ajuda.",

    2130 : "Guarde os tesouros.",
    2131 : "Pegue os tesouros.",
    2132 : "Preciso de tesouros!",
    2133 : "Cuidado!",

    # CJ battle
    2200 : "Você precisa acertar a balança.",
    2201 : "Eu vou acertar a balança.",
    2202 : "Eu preciso de ajuda com a balança!",
    2203 : "Você precisa atordoar os Cogs.",
    2204 : "Eu vou atordoar os Cogs.",
    2205 : "Eu preciso de ajuda com os Cogs!",
    2206 : "Eu preciso de mais evidências.",
    2207 : "Eu fico com as cadeiras da fileira de cima.",
    2208 : "Eu fico com as cadeiras da fileira de baixo.",
    2209 : "Saia da frente! Não podemos atingir o prato.",
    2210 : "Eu faço as piadas Toonar.",
    2211 : "Eu não tenho peso bônus.",
    2212 : "Eu tenho peso bônus de 1.",
    2213 : "Eu tenho peso bônus de 2.",
    2214 : "Eu tenho peso bônus de 3.",
    2215 : "Eu tenho peso bônus de 4.",
    2216 : "Eu tenho peso bônus de 5.",
    2217 : "Eu tenho peso bônus de 6.",
    2218 : "Eu tenho peso bônus de 7.",
    2219 : "Eu tenho peso bônus de 8.",
    2220 : "Eu tenho peso bônus de 9.",
    2221 : "Eu tenho peso bônus de 10.",
    2222 : "Eu tenho peso bônus de 11.",
    2223 : "Eu tenho peso bônus de 12.",

    #Kart Racing Phrases
    #IMPORTANT: if you change numbers or add/subtract lines here than be
    # sure to adjust the kart racing menu guid dict below
    # Invites/Destinations
    3010 : "Alguém quer apostar corrida?",
    3020 : "Vamos apostar corrida!",
    3030 : "Quer apostar corrida?",
    3040 : "Vamos mostrar nossos karts!",
    3050 : "Não tenho tíquetes suficientes.",
    3060 : "Vamos apostar outra corrida!",
    3061 : "Quer apostar outra corrida?",


    #Places
    3150 : "Preciso ir à Loja do kart.",
    3160 : "Vamos para a pista de corrida!",
    3170 : "Vamos para a largada para mostrar nossos karts!",
    3180 : "Vou para a largada mostrar meu kart!",
    3190 : "A gente se encontra na pista de corrida!",
    3110 : "O ponto de encontro é a Loja do kart!",
    3130 :  "Onde a gente se encontra?",

    #Races
    3200 : "Onde você quer correr?",
    3201 : "Vamos escolher uma corrida diferente.",
    3210 : "Vamos fazer uma corrida de aquecimento." ,
    3211 : "Vamos fazer um campeonato de corrida.",
    3220 : "Eu gosto da corrida do Estádio dos Nerds!",
    3221 : "Eu gosto da corrida do Autódromo Rústico!",
    3222 : "Eu gosto da corrida do Circuito da Cidade!",
    3223 : "Eu gosto da corrida do Coliseu Saca-Rolhas!",
    3224 : "Eu gosto da corrida da Pista de Pulos!",
    3222 : "Eu gosto da corrida do Circuito da Cidade!",
    3230 : "Vamos correr no Estádio dos Nerds!",
    3231 : "Vamos correr no Autódromo Rústico!",
    3232 : "Vamos correr no Circuito da Cidade!",
    3233 : "Vamos correr no Coliseu Saca-Rolhas!",
    3234 : "Vamos correr na Pista de Pulos!",
    3235 : "Vamos correr na Avenida da Neve!",

    #Tracks
    3600 : "Em que pista você quer correr?",
    3601 : "Escolha uma pista!",
    3602 : "A gente pode correr em uma pista diferente?",
    3603 : "Vamos escolher uma pista diferente!",
    3640 : "Quero correr na primeira pista!",
    3641 : "Quero correr na segunda pista!",
    3642 : "Quero correr na terceira pista!",
    3643 : "Quero correr na quarta pista!",
    3660 : "Não quero correr na primeira pista!",
    3661 : "Não quero correr na segunda pista!",
    3662 : "Não quero correr na terceira pista!",
    3663 : "Não quero correr na quarta pista!",

    #Compliments
    3300 : "Uau! Você é RÁPIDO!",
    3301 : "Você é muito rápido para mim!",
    3310 : "Boa corrida!",
    3320 : "Eu me amarrei no seu kart!",
    3330 : "Uma corrida maravilhosa!",
    3340 : "Seu kart é muito maneiro!",
    3350 : "Seu kart é incrível!",
    3360 : "Seu kart é maravilhoso!",

    #Taunts (commented out taunts are for possible purchase lines)
    #3400 : "Coma a minha poeira!",
    3400 : "Tá com medo de me enfrentar?",
    3410 : "Vejo você na linha de chegada!",
    #3420 : "Você é mais devagar que tartaruga!",
    3430 : "Sou rápido como um raio!",
    #3440 : "Sou mais veloz que a luz!",
    3450 : "Você nunca vai me alcançar!",
    3451 : "Você nunca vai me derrotar!",
    3452 : "Ninguém consegue bater o meu tempo!",
    3453 : "Vamos embora, molenga!",
    3460 : "Me dá outra chance!",
    3461 : "Foi sorte a sua!",
    3462 : "Uh-huu! Essa foi perto!",
    3470 : "Uau, pensei que você tinha me vencido!",
    #3500 : "Dá uma olhada na minha máquina!",
    #3510 : "Olha só as minhas rodas!",
    #3540 : "Vruum! Vruum!",
    #3560 : "Eu já vi Cogs mais rápidos que isso!",
    #3600 : "Sou o mais rápido dos mais rápidos!",

    # Promotional Considerations
    10000 : "A escolha é sua!",
    10001 : "Você vai votar em quem?",
    10002 : "A minha candidata é a Galinha!",
    10003 : "Nada de caca! Vote na Vaca!",
    10004 : "Não fique no vácuo! Vote no Macaco!",
    10005 : "Mantenha o curso! Vote no Urso!",
    10006 : "Pense gordo! Vote no Porco!",
    10007 : "Vote no Bode - com ele a gente pode!",

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
    21000: 'Aqui, amigão!',
    21001: 'Aqui, amigona!',
    21002: 'Parado.',
    21003: 'Bom garoto!',
    21004: 'Boa menina!',
    21005: 'Rabisco bonzinho.',

    # Pet/Doodle Tricks
    21200: 'Pula!',
    21201: 'Dá a pata!',
    21202: 'Finge de morto!',
    21203: 'Rola!',
    21204: 'Faz cambalhota!',
    21205: 'Dança!',
    21206: 'Fala!',

    # PIRATES
#    50001 : 'Sim',
#    50002 : 'Não',
#    50003 : 'Arrr!',
#    50004 : "Aye, aye Captain!",

    # Common Expressions
#    50100 : "Todos a bordo!",
#    50101 : "Ei, marujo!",
#    50102 : "Alto lá!",
#    50103 : "Abram caminho!",
#    50104 : "Caramba!",
#    50105 : "Me explodiram!",
#    50106 : "Ei, você!",
#    50107 : "Claro, claro, Capitão!",
#    50108 : "Ande na prancha!",
#    50109 : "Continue!",
#    50110 : "Não vai sobrar ninguém para contar a história....",

    # Insults
#    50200 : "Seu rato de porão!",
#    50201 : "Seu cão sarnento!",
#    50202 : "Te vejo no fundo do mar!",
#    50203 : "Patife!",
#    50204 : "Marujo de terra firme!",

    # Places
#    50300 : "Cadê ocê?",
#    50301 : "Vamos invadir a cidade!",
#    50302 : "Vamos para as docas!",
#    50303 : "Vamos navegar!",
#    50304 : "Vamos para o bar.",

    # Greetings
    60100 : "Oi",
    60101 : "Olá!",
    60102 : "Oi!",
    60103 : "Ei!",
    60104 : "Oi pessoal!",
    60105 : "Como é que tá?",
    60106 : "Qual é?",

    # Bye
    60200 : "Tchau!",
    60201 : "Até mais!",
    60202 : "Te vejo por aí!",
    60203 : "Volto já!",
    60204 : "Tenho que ir.",

    # Happy
    60300 : ":-)",
    60301 : "Legal!",
    60302 : "É isso aí!",
    60303 : "Ha ha!",
    60304 : "Que fofo!",
    60305 : "É isso aí!",
    60306 : "Que maneiro!",
    60307 : "Irado!",
    60308 : "Incrível!",
    60309 : "Uau!",

    # Sad
    60400 : ":-(",
    60401 : "Aahh!",
    60402 : "Pôxa, cara!",
    60403 : "Ai!",
    60404 : "Pôxa!",

    # Places
    60500 : "Cadê você?",
    60501 : "Vamos para a Loja da Entrada!",
    60502 : "Vamos para a Discoteca!",
    60503 : "Vamos para Toontown.",
    60504 : "Vamos para os Piratas do Caribe!",
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
    10 : "Bom...",
    20 : "Por que não?",
    30 : "Claro!",
    40 : "É assim que se faz isso.",
    50 : "Maravilha!",
    60 : "E aí?",
    70 : "Mas claro!",
    80 : "Bingo!",
    90 : "Você só pode estar brincando...",
    100 : "Parece legal.",
    110 : "Que loucura!",
    120 : "Caramba!",
    130 : "Que confusão!",
    140 : "Não se preocupe.",
    150 : "Grrrr!",
    160 : "Qual é a boa?",
    170 : "Ei, ei, ei!",
    180 : "Vejo você amanhã.",
    190 : "Até a próxima.",
    200 : "Tchau-tchau, pica-pau.",
    210 : "Até outra hora, galinha d'angola.",
    220 : "Vou precisar ir daqui a pouco.",
    230 : "Não conheço isso!",
    240 : "Você está fora daqui!",
    250 : "Ai, isso dói!",
    260 : "Peguei você!",
    270 : "Por favor!",
    280 : "Obrigadíssimo!",
    290 : "Você está ditando moda!",
    300 : "Dá licença!",
    310 : "Posso ajudar?",
    320 : "É o que eu estou falando!",
    330 : "Jabuti perde tempo querendo aprender lição de águia.",
    340 : "Macacos me mordam!",
    350 : "Isso é especial!",
    360 : "Vamos parar de fazer bagunça!",
    370 : "O gato comeu sua língua?",
    380 : "Agora é com você!",
    390 : "Feio que dói.",
    400 : "Preciso ver um Toon.",
    410 : "Não dei a mínima!",
    420 : "Não vai amarelar!",
    430 : "Você é uma isca fácil.",
    440 : "Sei lá!",
    450 : "Tudo a ver!",
    460 : "Gracinha!",
    470 : "Você que manda!",
    480 : "É isso aí, garoto!",
    490 : "Vem me pegar, se você conseguir!",
    500 : "Você precisa se recuperar antes.",
    510 : "Você precisa de mais Pontos de risadas.",
    520 : "Estou de volta em um minuto.",
    530 : "Estou com fome.",
    540 : "Isso mesmo!",
    550 : "Estou com sono.",
    560 : "Estou pronto!",
    570 : "Estou de aborrecido.",
    580 : "Amo isso!",
    590 : "Isso foi muito legal!",
    600 : "Pule!",
    610 : "Ganhou piadas?",
    620 : "O que houve?",
    630 : "Vai devagar.",
    640 : "Devagar e sempre.",
    650 : "Gol!",
    660 : "Pronto?",
    670 : "Tudo OK!",
    680 : "Vai!",
    690 : "Vamos por aqui!",
    700 : "Você ganhou!",
    710 : "Meu voto é sim.",
    720 : "Meu voto é não.",
    730 : "Me inclui nessa.",
    740 : "Me inclui fora dessa.",
    750 : "Fica aqui, eu volto.",
    760 : "Rapidinho!",
    770 : "Você viu aquilo?",
    780 : "O que foi isso?",
    790 : "Nojento!",
    800 : "Não ligo.",
    810 : "Justo o que eu precisava.",
    820 : "Vamos botar lenha na fogueira!",
    830 : "Por aqui, galera!",
    840 : "Que coisa é essa?",
    850 : "A sorte está lançada.",
    860 : "Eu ouvi isso!",
    870 : "Você está falando comigo?",
    880 : "Valeu, vou estar por aqui por uma semana.",
    890 : "Hmm.",
    900 : "Eu pego este.",
    910 : "Peguei!",
    920 : "É meu!",
    930 : "Toma pra você.",
    940 : "Afaste-se, pode ser perigoso.",
    950 : "Não esquenta!",
    960 : "Minha nossa!",
    970 : "Puxa!",
    980 : "Uuuuhuuu!",
    990 : "Todos a bordo!",
    1000 : "Caramba!",
    1010 : "A curiosidade matou o gato.",
    # Series 2
    2000 : "Tome juízo!",
    2010 : "Que bom ver você!",
    2020 : "Você que sabe.",
    2030 : "Está se saindo bem?",
    2040 : "Antes tarde do que nunca!",
    2050 : "Bravo!",
    2060 : "Mas, falando sério, pessoal...",
    2070 : "Está a fim de se juntar a nós?",
    2080 : "Te pego depois!",
    2090 : "Mudou de idéia?",
    2100 : "Vem pegar!",
    2110 : "Ai, meu Deus!",
    2120 : "Prazer em conhecer.",
    2130 : "Não faça nada que eu não faria!",
    2140 : "Nem pense nisso!",
    2150 : "Não abandone o barco!",
    2160 : "Não segura a respiração.",
    2170 : "Nem me fale.",
    2180 : "É fácil falar.",
    2190 : "Já chega!",
    2200 : "Excelente!",
    2210 : "Incrível encontrar você aqui!",
    2220 : "Dá um tempo.",
    2230 : "Gostei de saber.",
    2240 : "Vai em frente que eu quero ver!",
    2250 : "Vai em frente!",
    2260 : "Muito bom!",
    2270 : "Legal ver você!",
    2280 : "Tenho que me mandar.",
    2290 : "Tenho que ir embora.",
    2300 : "Agüenta firme.",
    2310 : "Espera um segundo.",
    2320 : "Curta bastante!",
    2330 : "Divirta-se!",
    2340 : "Não tenho o dia todo!",
    2350 : "Segura a onda!",
    2360 : "Viajou!",
    2370 : "Não acredito!",
    2380 : "Duvido.",
    2390 : "Devo essa a você.",
    2400 : "Estou lendo sua mente, você é claro como água.",
    2410 : "Eu acho isso.",
    2420 : "Acho que você devia passar.",
    2430 : "Quem dera ter dito isso.",
    2440 : "Se eu fosse você não faria isso.",
    2450 : "Seria ótimo!",
    2460 : "Estou ajudando meu amigo.",
    2470 : "Estou aqui a semana toda.",
    2480 : "Imagina só!",
    2490 : "Na hora H...",
    2500 : "O que tiver de ser, será.",
    2510 : "Só estou pensando alto.",
    2520 : "Mantenha o contato.",
    2530 : "Depois da tempestade vem o lamaçal!",
    2540 : "Rapidinho!",
    2550 : "Sinta-se em casa.",
    2560 : "Talvez outra hora.",
    2570 : "Posso me juntar a vocês?",
    2580 : "Que lugar legal, o seu.",
    2590 : "Foi ótimo falar com você.",
    2600 : "Sem dúvida.",
    2610 : "Sem brincadeira!",
    2620 : "Nem por um decreto.",
    2630 : "Tenha a santa paciência!",
    2640 : "Por mim tudo bem.",
    2650 : "Tá legal.",
    2660 : "Sorria!",
    2670 : "O que você disse?",
    2680 : "Tchaaaan!",
    2690 : "Calma aí.",
    2700 : "Até prá vocês!",
    2710 : "Quem desdenha quer comprar.",
    2720 : "Muito maneiro!",
    2730 : "Muito engraçado.",
    2740 : "O truque é esse!",
    2750 : "Está acontecendo uma invasão de Cogs!",
    2760 : "Vacilo.",
    2770 : "Cuidado!",
    2780 : "Bem feito!",
    2790 : "O que está acontecendo?",
    2800 : "O que está havendo?",
    2810 : "Para mim está certo.",
    2820 : "Certo, chefe.",
    2830 : "Pode apostar.",
    2840 : "Faça as contas.",
    2850 : "Por que está saindo tão cedo?",
    2860 : "Você me faz rir!",
    2870 : "Vai direto.",
    2880 : "Você está decaindo!",
    # Series 3
    3000 : "O que quiser.",
    3010 : "Você se importa se eu me juntar a vocês?",
    3020 : "Verifique, OK?",
    3030 : "Não esteja tão certo disso.",
    3040 : "Não liga se eu fizer isso.",
    3050 : "Não sacrifica!",
    3060 : "Você não conhece?",
    3070 : "Não liga para mim.",
    3080 : "Descobri!",
    3090 : "Imagine só!",
    3100 : "Pode esquecer!",
    3110 : "Está indo para o mesmo lugar que eu?",
    3120 : "Melhor para você!",
    3130 : "Que coisa.",
    3140 : "Aproveita!",
    3150 : "Fica de olho!",
    3160 : "E lá vamos nós de novo.",
    3170 : "Que tal essa!",
    3180 : "Que você acha?",
    3190 : "Eu acho que sim.",
    3200 : "Acho que não.",
    3210 : "Dou uma resposta mais tarde.",
    3220 : "Sou todo ouvidos.",
    3230 : "Agora não dá.",
    3240 : "Não estou brincando!",
    3250 : "Estou de queixo caído.",
    3260 : "Continue sorrindo.",
    3270 : "Depois me fala!",
    3280 : "Deixa a torta voar!",
    3290 : "Eu também tenho certeza.",
    3300 : "Pare de demorar!",
    3310 : "Caramba, o tempo voou.",
    3320 : "Sem comentários.",
    3330 : "Agora você está falando minha língua!",
    3340 : "Por mim tudo bem.",
    3350 : "Bom conhecer você.",
    3360 : "Tá legal.",
    3370 : "Com certeza.",
    3380 : "Valeu mesmo.",
    3390 : "É por aí.",
    3400 : "É isso!",
    3410 : "Hora de dormir.",
    3420 : "Confie em mim!",
    3430 : "Até a próxima.",
    3440 : "Espere acordado!",
    3450 : "Muito bem!",
    3460 : "O que traz você aqui?",
    3470 : "O que aconteceu?",
    3480 : "E agora?",
    3490 : "Você primeiro.",
    3500 : "Pegue a esquerda.",
    3510 : "Bem que você queria!",
    3520 : "Você está com problemas!",
    3530 : "Você é demais!",

    # Series 4
    4000 : "Os toons mandam na área!",
    4010 : "Besteirol de Cog!",
    4020 : "Toons de todo o mundo, uni-vos!",
    4030 : "E aí, parceiro!",
    4040 : "Muitíssimo obrigado.",
    4050 : "Vamos lá, novato.",
    4060 : "Tô indo pra caminha.",
    4070 : "Tô doido pra ir!",
    4080 : "Esta cidade é pequena demais para nós dois!",
    4090 : "Vá embora!",
    4100 : "Puxa!!!",
    4110 : "É ouro!",
    4120 : "Boa viagem!",
    4130 : "Tá na hora de sumir...",
    4140 : "Debandar!",
    4150 : "Ficou com a pulga atrás da orelha?",
    4160 : "Me poupe!",
    4170 : "Perfeito.",
    4180 : "Aposto.",
    4190 : "Pé na estrada!",
    4200 : "Então, adivinha!",
    4210 : "Tô de novo na ativa!",
    4220 : "Procure os suspeitos de sempre.",
    4230 : "Vamos agitar!",
    4240 : "O céu é o limite.",
    4250 : "Estou me preparando.",
    4260 : "Segura a onda!",
    4270 : "Não acerto uma.",
    4280 : "Voltem todos agora.",
    4290 : "É uma verdadeira lavada!",
    4300 : "Não vai amarelar.",
    4310 : "Tá se achando?",
    4320 : "Que bagunça é essa aqui?",
    4330 : "Vamos parar com esta preguiça!",
    4340 : "Só não vê quem não quer.",
    4350 : "É um colírio para os olhos!",
    4360 : "Nossas opções estão acabando.",
    4370 : "Tire esse peso das costas.",
    4380 : "Que paisagem maravilhosa!",
    4390 : "Você vai ver só!",
    # Series 6
    6000 : "Quero doce!",
    6010 : "Sou que nem formiga com doce.",
    6020 : "Foi feito no grito.",
    6030 : "Fácil como tirar doce de criança!",
    6040 : "Leve três e pague um.",
    6050 : "Eles vão sentir o gostinho!",
    6060 : "É a parte ruim da história.",
    6070 : "Você não pode assobiar e chupar cana.",
    6080 : "Tô me sentindo como uma criança em uma loja de doces.",
    6090 : "Seis deste, meia dúzia do outro...",
    6100 : "Rapadura é doce mas não é mole não.",
    6110 : "Tem que fritar o peixe de olho no gato.",
    6120 : "É sopa no mel.",
    6130 : "Mas temos que pisar em ovos.",
    6140 : "Vamos melar os trabalhos!",
    6150 : "Você é um coco duro de quebrar!",
    6160 : "É assim que o bolo desanda.",
    6170 : "Café com leite.",
    6180 : "Tá tentando adoçar a minha boca?",
    6190 : "Tem que tomar água pra ajudar a descer.",
    6200 : "Você é o que você come!",
    6210 : "É mamão com açúcar!",
    6220 : "Deixa de ser bananão!",
    6230 : "Azedinho doce.",
    6240 : "Molezinha!",
    6250 : "Olha o bicho-papão!",
    6260 : "Olha o sorvete aí, gente!",
    6270 : "Não vamos enfeitar o bolo não.",
    6280 : "Toc, toc, toc...",
    6290 : "Quem é?",
    # Series 7
    7000 : "Pára de macaquice!",
    7010 : "Entrou areia.",
    7020 : "Macaco de imitação.",
    7030 : "Eles te passaram a perna.",
    7040 : "Parece história pra boi dormir.",
    7050 : "Só tô de palhaçada contigo.",
    7060 : "Quem quer ser a bola da vez?",
    7070 : "É papagaio de pirata...",
    7080 : "Uma macacada só!",
    7090 : "Macacos me mordam!",
    7100 : "Cada macaco no seu galho.",
    7110 : "E a beca?",
    7120 : "Não ouço.",
    7130 : "Não vejo.",
    7140 : "Não falo.",
    7150 : "Cada um para um lado, macacada.",
    7160 : "Lá fora é uma selva.",
    7170 : "Você é o rei da selva!",
    7180 : "Tudo ótimo!",
    7190 : "Tô enlouquecendo!",
    7200 : "Vamos entrar no ritmo!",
    7210 : "Este lugar está muito cheio!",
    7220 : "Adeus, vida cruel.",
    7230 : "Acabei numa furada.",
    7230 : "Pé na tábua.",
    7240 : "Balinhas não crescem em árvores!",

    # Halloween
    10000 : "Este lugar é uma cidade-fantasma.",
    10001 : "Bonita roupa!",
    10002 : "Acho que este lugar é assombrado.",
    10003 : "Gostosuras ou travessuras!",
    10004 : "Buuuuu!",
    10005 : "Feliz Assombração!",
    10006 : "Feliz Dia das Bruxas!",
    10007 : "Está na hora de eu virar uma abóbora.",
    10008 : "Fantasmático!",
    10009 : "Sinistro!",
    10010 : "Isso é horripilante!",
    10011 : "Detesto aranhas!",
    10012 : "Você ouviu?",
    10013 : "Você não tem nem uma sombra de chance!",
    10014 : "Me assustou!",
    10015 : "Horrível!",
    10016 : "Bizarro!",
    10017 : "Isso foi muito estranho....",
    10018 : "Esqueletos no seu armário?",
    10019 : "Assustei você?",

    # Fall Festivus
    11000 : "Ah! Marmelada!",
    11001 : "Melhor desamarrar a cara!",
    11002 : "Brrr!",
    11003 : "Fica calmo!",
    11004 : "Vem pegar!",
    11005 : "Não dá uma de peru, para morrer de véspera.",
    11006 : "Glu-glu-glu!",
    11007 : "Boas Festas!",
    11008 : "Feliz Ano Novo!",
    11009 : "Um bom feriado para você!",
    11010 : "Feliz Dia do Peru!",
    11011 : "Ho! Ho! Ho!",
    11012 : "\"Noel\" problema.",
    11013 : "\"Noel\" surpresa nenhuma.",
    11014 : "Deixa bater o sino, pequenino!",
    11015 : "Raspa o tacho.",
    11016 : "Feliz Natal!",
    11017 : "Com \"nataleza\"!",
    11018 : "Até o Natal, tudo bem!",
    11019 : "Você vai se \"arrenapender\"!",

    # Valentines
    12000 : "Fica comigo!",
    12001 : "Vem ser meu amorzinho!",
    12002 : "Feliz Dia dos Namorados!",
    12003 : "Ahhh, que bonitinho.",
    12004 : "Estou apaixonado por você.",
    12005 : "Amor de pombinhos.",
    12006 : "Te amo!",
    12007 : "Quer ser meu amor?",
    12008 : "Você é uma graça.",
    12009 : "Você é doce como mel.",
    12010 : "Fofura.",
    12011 : "Você precisa de um abraço.",
    12012 : "Muito fofo!",
    12013 : "Que fofo!",
    12014 : "Batatinha quando nasce...",
    12015 : "Esparrama pelo chão...",
    12016 : "Que gracinha!",

    # St. Patricks Day
    13000 : "Tenho você no coração!",
    13001 : "Feliz Páscoa!",
    13002 : "Você não está vestindo marrom-chocolate!",
    13003 : "Sorte de iniciante marrom-chocolate.",
    13004 : "Estou chocolate de inveja.",
    13005 : "Seu sortudo!",
    13006 : "Você é o meu trevo de quatro folhas!",
    13007 : "Você é o meu talismã!",
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
PSCMenuExpressions  = "EXPRESSÕES"
PSCMenuInsults    = "INSULTOS"
PSCMenuPlaces     = "LUGARES"

# Gateway Speedchat
GWSCMenuHello     = "CUMPRIMENTOS"
GWSCMenuBye       = "DESPEDIDAS"
GWSCMenuHappy     = "FELIZ"
GWSCMenuSad       = "TRISTE"
GWSCMenuPlaces     = "LUGARES"

# NamePanel.py - PickAName/TypeAName
RandomButton = "Aleatório"
TypeANameButton = "Digite um nome"
PickANameButton = "Escolha um nome"
NameShopSubmitButton = "Enviar"
RejectNameText = "Este nome não é permitido. Tente novamente."
WaitingForNameSubmission = "Enviando o seu nome..."

NameShopNameMaster = "NameMaster_portuguese.txt"
NameShopPay = "Assine já!"
NameShopPlay = "Avaliação gratuita"
NameShopOnlyPaid = "Somente usuários pagantes\npodem dar nomes aos seus Toons.\nAté que você se inscreva\nseu nome será\n"
NameShopContinueSubmission = "Continuar envio"
NameShopChooseAnother = "Escolha outro nome"
NameShopToonCouncil = "O Conselho de Toons\nanalisará o seu\nnome."+ \
                      "A análise pode\nlevar alguns dias.\nEnquanto você espera\nseu nome será\n"
PleaseTypeName = "Digite o seu nome:"
AllNewNames = "Todos os novos nomes\ndevem ser aprovados\npelo Conselho de Toons."
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
    "pateta",
    )

# NameCheck.py
NCTooShort = 'Este nome é muito curto.'
NCNoDigits = 'O nome não pode conter números.'
NCNeedLetters = 'Cada palavra do nome deve conter algumas letras.'
NCNeedVowels = 'Cada palavra do nome deve conter algumas vogais.'
NCAllCaps = 'O seu nome não pode estar todo em maiúscula.'
NCMixedCase = 'Este nome tem muitas letras em minúscula.'
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
                 'permitidos somente em palavras como "Sr.", "Sra.", "J.P." etc.')
NCApostrophes = 'Este nome tem muitos apóstrofos.'

# AvatarDetailPanel.py
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = "Fechar"
AvatarDetailPanelLookup = "Procurando detalhes de %s."
AvatarDetailPanelFailedLookup = "Não foi possível obter detalhes de %s."
AvatarDetailPanelPlayer = "Player: %(player)s\nWorld: %(world)s\nLocation: %(location)s"
AvatarDetailPanelOnline = "Região: %(district)s\nLocation: %(location)s"
AvatarDetailPanelOffline = "Região: off-line\nLocal: off-line"

# AvatarPanel.py
AvatarPanelFriends = "Amigos"
AvatarPanelWhisper = "Cochichar"
AvatarPanelSecrets = "Segredos"
AvatarPanelGoTo = "Ir para"
AvatarPanelIgnore = "Ignorar"
AvatarPanelStopIgnore = "Stop Ignoring"
AvatarPanelEndIgnore = "End Ignore"
AvatarPanelTrade = "Trade"
#AvatarPanelCogDetail = "Dept: %s\nNível: %s\n"
AvatarPanelCogLevel = "Nível: %s"
AvatarPanelCogDetailClose = "Fechar"

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

KartRacingMenuSections = [
 -1,
 "LUGARES",
 "CORRIDAS",
 "PISTAS",
 "ELOGIOS",
 "PROVOCAÇÕES"
]

GolfMenuSections = [
 -1,
 "COURSES",
 "TIPS",
 "COMMENTS",
]

WhiteListMenu = [
-1,
"WHITELIST"
]

# TTAccount.py
# Fill in %s with phone number from account server
TTAccountCallCustomerService = "Favor entrar em contato com o Atendimento ao Consumidor em %s."
# Fill in %s with phone number from account server
TTAccountCustomerServiceHelp = "\nSe precisar de ajuda, favor entrar em contato com o Atendimento ao Comsumidor em %s."
TTAccountIntractibleError = "Um erro ocorreu."


