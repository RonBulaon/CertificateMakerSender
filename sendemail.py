import sys
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

def email(senders,recipients,subject,filename,emailBody,mailserver,outputDir,cc):
    sender = senders
    recipient = recipients
    filename = (outputDir+'/'+filename)
    emails = [cc , recipients]

    # Create the enclosing (emailMsg) message
    emailMsg = MIMEMultipart()
    emailMsg['Subject'] = subject
    # emailMsg['To'] = COMMASPACE.join(recipients)
    emailMsg['To'] = recipients
    emailMsg['From'] = sender
    emailMsg['bcc'] = cc
    emailMsg.attach(MIMEText(emailBody))

    # List of attachments
    attachments = [filename]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            emailMsg.attach(msg)
        except:
            print('Unable to open one of the attachments. Error: ', sys.exc_info()[0])
            raise

    composed = emailMsg.as_string()

    # Send the email
    try:
        with smtplib.SMTP(mailserver, 25) as s:
            s.ehlo()
            s.sendmail(sender, emails, composed)
            s.close()
        return('sent')
    except:
        return('Unable to send the email. Error: ', sys.exc_info()[0])
        raise
