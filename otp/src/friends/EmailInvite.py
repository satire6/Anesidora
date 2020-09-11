from otp.distributed import OtpDoGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify

import smtplib, socket
from email import MIMEImage
from email import MIMEMultipart
from email import MIMEText

class EmailInvite:
    # System for sending an email invite

    notify = directNotify.newCategory('EmailInvite')

    def __init__(self, smtpHost, emailTemplate):
        self.smtpAvailable = uber.smtpAvailable
        if not self.smtpAvailable:
            self.notify.debug('SMTP Server not available')
            return

        self.smtpHost = smtpHost
        self.emailTemplate = emailTemplate
        self.mailServer = smtplib.SMTP(smtpHost)

        # Stitch together an email to send to the toAddr
        # Open the email template

        fhndl = open(self.emailTemplate, 'rb')
        self.messageBody = fhndl.read()
        fhndl.close()

        # Try opening a connection to the server

        self.connect()

    def connect(self):
        if not self.smtpAvailable:
            return
        try:
            self.mailServer.connect()
        except socket.error:
            self.notify.warning('Failed to connect to SMTP server at %s. E-Mailing invites disabled.' % (self.smtpHost))
            self.smtpAvailable = 0

    def disconnect(self):
        if not self.smtpAvailable:
            return
        self.mailServer.close()

    def sendEmailInvite(self, fromAddr, toAddr, subject, fromAvName, inviteCode):
        if not self.smtpAvailable:
            self.notify.warning('sendEmailInvite called, but SMTP is not available')
            return
        
        msg = MIMEText.MIMEText(self.messageBody % (fromAvName, inviteCode))

        # Set the Subject field
        msg['Subject'] = subject
        # Set the From Field
        msg['From'] = fromAddr
        # Set the To Field
        msg['To'] = toAddr

        # Now send the message
        outbound = msg.as_string()
        print 'The ougoing message is: %s' % (outbound)

        try:
             self.mailServer.sendmail(fromAddr, [toAddr], outbound)
        except SMTPServerDisconnected:
            # Server is disconnected. Reconnect to server and try request again
            self.notify.warning('SMTP Server Disconnected, Trying to send again')
            self.connect()
            self.sendEmailInvite(fromAddr, toAddr, subject, fromUserName, inviteCode)
        except SMTPRecipientsRefused:
            # Recipient Address Refused.
            self.notify.warning('SMTP Recipent(s) Refused: %s' % toAddr)

        except SMTPSenderRefused:
            # Sender or data is considered bad
            self.notify.warning('SMTP Sender or Data Refused: %s' % fromAddr)

        except SMTPHeloError:
            # The server refused our "HELO" message
            self.notify.warning('The server refused our "HELO" message')

        except SMTPException:
             self.notify.warning('SMTP Failed, Trying to send again')
             self.sendEmailInvite(fromAddr, toAddr, subject, fromUserName, inviteCode)
