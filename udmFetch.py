import requests
import smtplib

import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_secrets():
    with open('environment.json') as secrets_file:
        secrets = json.load(secrets_file)

    return secrets

secrets = get_secrets()

API_KEY = secrets["API_Key"]
email_user = secrets["email_user"]
email_pass = secrets["email_pass"]
mail_to_user = secrets["mail_to"]
smtp_server = secrets["smtp_server"]
smtp_port = secrets["smtp_port"]

username = email_user
password = email_pass
mail_from = email_user
mail_to = mail_to_user
mail_subject = "Offline UDMs"
mail_body = "Test message"


response = requests.get('https://api.ui.com/ea/devices', headers={'X-API-KEY': API_KEY})

devices = response.json()


mail_msg = ''
count = 0
hostName = ''
deviceName = ''
deviceStatus = ''
deviceModel = ''
prevHN = ''

for model in devices['data']:
        
        for thismodel in model['devices']:
            deviceStatus = thismodel['status']
           
            
            if deviceStatus == "offline":
                
                try:
                    hostName = model['hostName']
                except:
                    hostName = 'No hostname'
                    pass
                
                deviceName = thismodel['name']
                deviceModel = thismodel['model']
                
                if prevHN != hostName:
                    
                    print("\n")
                    mail_msg += "\n"
                    print("Hostname:", hostName)
                    mail_msg += "Hostname: " + hostName + '\n'
                print("Name: ",deviceName,"     Model: ",deviceModel,"     Status: ",deviceStatus)
                mail_msg += "Name: " + deviceName + "     Model: " + deviceModel + "     Status: " + deviceStatus + '\n'
                prevHN = hostName
                
        count += 1
# html += '</body></html>'
mimemsg = MIMEMultipart()
mimemsg['From'] = mail_from
mimemsg['To'] = mail_to
mimemsg['Subject'] = mail_subject
mimemsg.attach(MIMEText(mail_msg, 'plain'))
connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
connection.starttls()
connection.login(username, password)
connection.send_message(mimemsg)
connection.quit()
print(count)
