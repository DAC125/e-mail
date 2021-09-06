from twisted.internet import ssl
from twisted.mail import smtp, maildir
from zope.interface import implementer
from twisted.internet import protocol, reactor, defer
from twisted.python.usage import Options, UsageError
import os
from io import BytesIO
from email.header import Header
import sys

#Clase encargada de guardar el correo recivido en el directorio seleccionado
@implementer(smtp.IMessage)
class MailMessageStorage(object):

    def __init__(self, mail_storage):
        if not os.path.exists(mail_storage): os.mkdir(mail_storage)

        inbox_storage = os.path.join(mail_storage, 'INBOX')
        self.mailbox = maildir.MaildirMailbox(inbox_storage)
        self.lines = []


    def lineReceived(self, line):
        if type(line) != str:
            line = line.decode("utf-8")
        self.lines.append(line)



    def eomReceived(self):
        # message is complete, store it

        print("Message data complete.")

        self.lines.append('') # add a trailing newline
        print(self.lines)
        messageData = '\n'.join(self.lines)
        return self.mailbox.appendMessage(bytes(messageData,"utf-8"))



    def connectionLost(self):

        print("Connection lost unexpectedly!")

        del self.lines



# clase que se encarga de recibir los correos que llegan del cliente
@implementer(smtp.IMessageDelivery)
class LocalDelivery(object):


    def __init__(self, baseDir, validDomains):

        if not os.path.isdir(baseDir):
            raise ValueError( "'%s' is not a directory" % baseDir)

        self.baseDir = baseDir

        self.validDomains = validDomains

    def receivedHeader(self, helo, origin, recipients):

         myHostname, clientIP = helo

         headerValue = "by %s from %s with ESMTP ; %s" % (myHostname.decode(), clientIP.decode(), smtp.rfc822date().decode())

         # email.Header.Header used for automatic wrapping of long lines

         return "Received: %s" % Header(headerValue)



    def validateTo(self, user):
        if not user.dest.domain.decode("utf-8") in self.validDomains:

            raise smtp.SMTPBadRcpt(user)

        print("Accepting mail for %s..." % user.dest)

        return lambda: MailMessageStorage(self._getAddressDir(str(user.dest)))



    def _getAddressDir(self, address):

        return os.path.join(self.baseDir, "%s" % address)



    def validateFrom(self, helo, originAddress):

         # accept mail from anywhere. To reject an address, raise

         # smtp.SMTPBadSender here.

         return originAddress


# esta clase es la encargada de crear e invocar el protocolo SMTP
class SMTPFactory(protocol.ServerFactory):

    def __init__(self, baseDir, validDomains):

        self.baseDir = baseDir

        self.validDomains = validDomains



    def buildProtocol(self, addr):
        delivery = LocalDelivery(self.baseDir, self.validDomains)

        smtpProtocol = smtp.SMTP(delivery)

        smtpProtocol.factory = self

        return smtpProtocol

        return smtpProtocol

class MailClientOptions(Options):
    synopsis = "smptclient.py [options]"

    optParameters = [
        (
            "domains",
            "d",
            None,
            "Los dominios que el servidor va a aceptar para guardar",
        ),
        (
            "mailstorage",
            "s",
            None,
            "Carpeta donde se van a guardar los correos electronicos",
        ),
        (
            "port",
            "p",
            None,
            "puerto de comunicación"
        )
    ]

    def postOptions(self):
        """
        Parse integer parameters, open the message file, and make sure all
        required parameters have been specified.
        """
        if self["domains"] is None:
            raise UsageError("Debe especificar los dominios que el servidor va a aceptar con -d [dominios]")


        if self["mailstorage"] is None:
            raise UsageError("Debe especificar la rura del contenedor de correos con -s [ruta]")


        if self["port"] is None:
            raise UsageError("Debe especificar el numero de puerto en el que el servidor va a trabajar con -p [puerto]")


def GetRecipients(addARR):
    awsr = []
    for i in addARR:
        awsr.append(i[0])
    return awsr



def main(args=None):


    o = MailClientOptions()
    try:
        o.parseOptions(args)
    except UsageError as e:
        raise SystemExit(e)

    port = int(o['port'])
    domains = o["domains"].split(',')
    mailstorage = o["mailstorage"]

    reactor.listenTCP(port, SMTPFactory(mailstorage, domains))
    reactor.run()

if __name__ == "__main__":
    main(sys.argv[1:])


