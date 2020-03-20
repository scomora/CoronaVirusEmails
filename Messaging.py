
from os import environ
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = environ["GMAIL_EMAIL"]
password = environ["GMAIL_PASSWORD"]

msg = MIMEMultipart('alternative')


class Session:
    def __init__(self):
        self.email = email
        self.password = password
        self.smtpserver = smtplib.SMTP("smtp.gmail.com", 587) #TODO: fix this. should not have to construct here

    def getEmail(self):
        return self.email

    def login(self):
        self.smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtpserver.starttls()
        self.smtpserver.ehlo()
        self.smtpserver.login(self.email, self.password)

    def sendMessage(self, destAddress, msg):
        self.login()
        msg['To'] = destAddress
        self.smtpserver.sendmail(self.email, destAddress, msg.as_string())

    def sendMessageToContacts(self, contacts, msgContent):
        """

        """
        msg['Subject'] = "Your Daily Coronavirus Update (from Spencer Comora)"
        msg['From'] = self.getEmail()
        msgContent = MIMEText(msgContent, 'html')
        print(msgContent)
        msg.attach(msgContent)


        for contact in contacts:
            self.sendMessage(contact, msg)
            print("Message sent to {}".format(contact))
