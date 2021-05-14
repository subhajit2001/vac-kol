from datetime import timedelta, date
import requests
import jsons
from json2html import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

start_date = date(2021, 5, 14)
end_date = date(2021, 6, 14)
mail_content = ""
count = 0

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

for single_date in daterange(start_date, end_date):
    
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=725&date='+single_date.strftime("%d-%m-%Y")
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        #c = '''Vaccines Available : ''' + single_date.strftime("%d-%m-%Y") + '''\n'''
        #mail_content = mail_content + c
        data = response.text
        parsed = jsons.loads(data)
        if parsed['sessions']!=[]:
            mail_content = mail_content + '<h2><b>Vaccines Available : ' + single_date.strftime("%d-%m-%Y") + '</b></h2><br><br>'
            mail_content = mail_content + json2html.convert(json = data) + '<br><br>'
            count+=1
            print("Success")

if count>0:
    #The mail addresses and password
    sender_address = 'subhajit.earth@gmail.com'
    sender_pass = 'subhajit2001'
    receiver_address = 'subhajit.asia@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Vaccine Slot Alert!!!'   #The subject line

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
else:
    print('Failure!!! No Slots Available...')