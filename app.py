import datetime
import csv
import PySimpleGUI as sg
from makepdf import HTML2PDF, cert
from sendemail import *
import os

defaultNamelist = os.getcwd()
defaultCert = os.getcwd()
defaultOutput = os.getcwd()
defaultEmail = 'email@example.com'
defaultPercentage = 0
version = '1.0.0'
sender = 'NO_REPLY@YOURDOMAIN.COM' # Change this according to your requirements
mailserver = 'SMTP.YOURDOMAIN.COM' # Change this according to your requirements


def scrLog(text):
    currentDT = datetime.datetime.now()
    print( '['+str(currentDT)+'] ' + text)

layout = [
            [sg.Text('Put in the following details:')],
            [sg.Text('Name List', size=(16, 1)), sg.InputText(str(defaultNamelist),key='list'), sg.FileBrowse()],
            [sg.Text('Certificate', size=(16, 1)), sg.InputText(str(defaultCert), key='cert'), sg.FileBrowse()],
            [sg.Text('Output Directory', size=(16, 1)), sg.InputText(str(defaultOutput),key='out'), sg.FolderBrowse()],
            [sg.Radio('Generate Certificate', "RADIO1", size=(20, 1) ,default=True), sg.Radio('Generate Certificate and Send Email', "RADIO1")],
            [sg.Text('Bcc Email', size=(16, 1)), sg.InputText(str(defaultEmail), key='email')],
            [sg.Text('Email Subject', size=(16, 1)), sg.InputText(str('Training Certificate'), key='Subject')],
            [sg.Text('Mesage Body', size=(16, 1)), sg.Multiline(str('Attached is your Certificate for attending our workshop. Thank you!'), size=(45, 8), key='Body')],
            [sg.Text(' ', size=(16, 1))],
            [sg.Text('Status :', size=(16, 1))],
            [sg.ProgressBar(100, orientation='h', size=(42, 20), key='progressbar'), sg.Text(str(defaultPercentage)+' %', key='percentageNumber')],
            [sg.Output(size=(72, 10))],
            [sg.Text(' ', size=(16, 1))],
            [sg.Submit('Start'), sg.Cancel('Quit'), sg.Button('About')]
        ]

window = sg.Window(
    title='Certificate Generator',
    disable_close=True,
    icon='certificate.ico'
    ).Layout(layout)
progress_bar = window.FindElement('progressbar')

while True:
    (event, values) = window.Read()

    if event == 'EXIT' or event == 'Quit'  or event is None:
        break # exit button clicked

    if event == 'Start':
        emailCounter = 0
        pdfCounter = 0
        errorEmailCounter = 0
        errorPdfCounter = 0

        nameList = values['list']
        certTemplate = values['cert']
        outputDir = values['out']
        certOnly = values[0]
        sendEmail = values[1]
        cc = values['email']

        subject = values['Subject']
        msgbody = values['Body']
        if (msgbody != 'Do not reply to this email. This is a system generated message!'):
            msgbody = values['Body']+'\nDo not reply to this email. This is a system generated message!'

        scrLog('opening ' +nameList)

        try :
            row_count = sum(1 for row in csv.reader( open(nameList) ) )
        except:
            scrLog('Error opening ' +nameList)

        try:
            with open(nameList, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    filename = row['name'] + '_' +row['date'] + '_' + row['course']
                    filename = filename.replace(" ", "")+".pdf"
                    recipients = row['email']
                    scrLog('Creating certificate '+filename)
                    result = cert(row['name'], row['course'], row['date'],certTemplate, filename, row['location'], row['serialnumber'], outputDir)
                    if result == 'Success':
                        scrLog('[success] '+ filename + ' was created')
                        pdfCounter += 1
                        if sendEmail == True:
                            scrLog('Sending '+filename+' to '+recipients)
                            emailed = email(sender,recipients,subject,filename,msgbody,mailserver,outputDir, cc)
                            if emailed == 'sent':
                                scrLog('[success] '+'Notification Sent for ' + filename + ' to ' + recipients)
                                emailCounter += 1

                            else:
                                scrLog('Error Sending certificate ('+ filename +') to '+recipients)
                                errorEmailCounter +=1

                    elif result == 'Error':
                        scrLog('[Error] '+ filename + ' file not created')
                        errorPdfCounter += 1

                    if sendEmail == True:
                        percentage = (((emailCounter + pdfCounter + errorPdfCounter + errorEmailCounter))/((row_count-1)*2))*100
                    else:
                        percentage = (((pdfCounter + errorPdfCounter))/(row_count-1))*100

                    progress_bar.UpdateBar(percentage)
                    values['percentageNumber'] = str(int(percentage)) + ' %'
                    window.FindElement('percentageNumber').Update(values['percentageNumber'])
                    window.FindElement('list').Update(values['list'])
                    window.FindElement('cert').Update(values['cert'])
                    window.FindElement('out').Update(values['out'])
                    window.FindElement('email').Update(values['email'])
                    window.FindElement('Body').Update(values['Body'])
                    window.FindElement('Subject').Update(values['Subject'])
        except:
            scrLog('Error opening File!')
            window.FindElement('list').Update(values['list'])
            window.FindElement('cert').Update(values['cert'])
            window.FindElement('out').Update(values['out'])
            window.FindElement('email').Update(values['email'])
            window.FindElement('Body').Update(values['Body'])
            window.FindElement('Subject').Update(values['Subject'])

        scrLog('Email :'+ str(emailCounter) +' = Sent. '+ str(errorEmailCounter) +' = Error sending')
        scrLog('PDF : '+ str(pdfCounter) +' = Created. '+ str(errorPdfCounter) +' = Error Creation')
        scrLog('Done!')

    elif event == 'Quit':
        scrLog('Quit...\nBye!')

    elif event == 'About':
        window.FindElement('list').Update(values['list'])
        window.FindElement('cert').Update(values['cert'])
        window.FindElement('out').Update(values['out'])
        window.FindElement('email').Update(values['email'])
        window.FindElement('Body').Update(values['Body'])
        window.FindElement('Subject').Update(values['Subject'])
        sg.Popup('Ron Bulaon\nRonWork.com\ninfo@ronwork.com\n\nVersion '+version, icon='certificate.ico', title='About')
