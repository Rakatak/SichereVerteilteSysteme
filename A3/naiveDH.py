import base64, smtplib, imaplib, getpass, random, hashlib, hmac
from email.parser import Parser
from email.mime.text import MIMEText
from xtea import *


def main():
    personOne = {"email": "s63570@beuth-hochschule.de", "smtp": {"address": "smtp.beuth-hochschule.de", "port": 587}, "imap": {"address": "imap.beuth-hochschule.de"}}
    personTwo = {"email": "robin-steller@web.de", "smtp": {"address": "smtp.web.de", "port": 587}, "imap": {"address": "imap.web.de"}}

    p = 467
    g = 2

    a = 2
    b = 5

    print "Send public keys..."
    publicKeyA = generateKey(g, a, p)
    sendMail(personOne, personTwo, publicKeyA)

    publicKeyB = generateKey(g, b, p)
    sendMail(personTwo, personOne, publicKeyB)

    print "\nReceive public keys..."
    pubA = receiveMail(personOne, personTwo)
    privateKeyB = generateKey(int(pubA), b, p)

    pubB = receiveMail(personTwo, personOne)
    privateKeyA = generateKey(int(pubB), a, p)

    print "\nSend encrypted message from " + personOne["email"] + " to " + personTwo["email"] + "."
    subject = raw_input("Please enter the subject: ")
    message = raw_input("Please enter the message: ")

    encryptedMessage = encryptionXteaCBCMode(privateKeyA, message)

    print "\nSending message..."
    sendMail(personOne, personTwo, encryptedMessage, subject)

    print "\nReading message..."
    message = receiveMail(personOne, personTwo)
    decryptedMessage = decryptionXteaCBCMode(privateKeyB, message)

    print "\nThe message is:"
    print decryptedMessage


def generateKey(basis, exponent, modulo):
    return str((basis**exponent) % modulo)


def sendMail(sender, receiver, msg, subject="Public key"):
    msg = MIMEText(base64.b64encode(msg) + "\r\n")
    print "Sending..."

    msg['Subject'] = subject
    msg['From'] = sender["email"]
    msg['To'] = receiver["email"]
    print "Sending..."

    s = smtplib.SMTP(sender["smtp"]["address"], sender["smtp"]["port"])
    print "Sending..."

    s.starttls()
    print "Sending..."

    pwd = getpass.getpass(prompt='Please enter the password for ' + sender["email"] + ': ')

    loginSucceeded = False
    while not loginSucceeded:
        try:
            s.login(sender["email"], pwd)
            loginSucceeded = True
        except:
            pwd = getpass.getpass(prompt='Authentication failed. Please enter your password again: ')

    s.sendmail(sender["email"], [receiver["email"]], msg.as_string())
    s.quit()


def receiveMail(sender, receiver):
    mail = imaplib.IMAP4_SSL(receiver["imap"]["address"])
    pwd = getpass.getpass(prompt='Please enter the password for ' + receiver["email"] + ': ')

    loginSucceeded = False
    while not loginSucceeded:
        try:
            mail.login(receiver["email"], pwd)
            loginSucceeded = True
        except:
            pwd = getpass.getpass(prompt='Authentication failed. Please enter your password again: ')

    mail.list()
    mail.select("inbox")

    result, data = mail.search(None, "FROM", sender["email"])

    ids = data[0]
    idList = ids.split()

    latestEmailId = idList[-1]

    result, data = mail.fetch(latestEmailId, "(RFC822)")

    mail.close()
    mail.logout()

    rawEmail = data[0][1]
    emailData = Parser().parsestr(rawEmail)

    body = []
    if emailData.is_multipart():
        for payload in emailData.get_payload():
            body.append(payload.get_payload())
    else:
        body.append(emailData.get_payload())

    body = ''.join(body).split("\r\n")[0]
    body = body.replace("=3D", "=")
    key = base64.b64decode(body).split("\r\n")[0]

    return key


def encryptionXteaCBCMode(key, message):
    hashKey = sha256Hash(key, '')
    hashKey = hashKey[:16]

    originalMessageLength = len(message)
    message = padding(message)

    iv = byteStringToString(charOrIntToByte(random.randrange(0, 2**64-1)).zfill(64))

    encryptedMessage = new(hashKey, mode=MODE_CFB, IV=iv).encrypt(message)
    encryptedMessage = encryptedMessage[:originalMessageLength]
    return iv + encryptedMessage


def decryptionXteaCBCMode(key, cipherMessage):
    hashKey = sha256Hash(key, '')
    hashKey = hashKey[:16]

    iv = cipherMessage[:8]
    message = cipherMessage[8:]
    originalMessageLength = len(message)
    message = padding(message)

    decryptedMessage = new(hashKey, mode=MODE_CFB, IV=iv).decrypt(message)
    decryptedMessage = decryptedMessage[:originalMessageLength]

    return decryptedMessage


def padding(message):
    paddedMessage = stringToByteString(message)
    blockSize = 64
    missingBits = blockSize - (len(paddedMessage) % blockSize)
    if missingBits == 0:
        paddedMessage += '1' + '0'*(blockSize - 1)
    else:
        paddedMessage += '1' + '0'*(missingBits-1)

    paddedMessage = byteStringToString(paddedMessage)
    return paddedMessage


def byteStringToString(byteString):
    return byteArrayToString([byteString[i:i+8] for i in range(0, len(byteString), 8)])


def byteArrayToString(byteArray):
    string = []
    for byte in byteArray:
        ch = chr(int(byte, 2))
        string.append(ch)
    return ''.join(string)


def stringToByteString(string):
    return ''.join(charOrIntToByte(x) for x in string)


def charOrIntToByte(ch):
    if type(ch) is str and len(ch) == 1:
        ch = ord(ch)
    elif type(ch) is not int and type(ch) is not long:
        return 0
    return '{:08b}'.format(ch)


def sha256Hash(key, message):
    return hmac.new(key=key, msg=message, digestmod=hashlib.sha256).digest()


if __name__ == "__main__":
    main()
