# import time
#
# import requests as requests
#
# start = time.time()
# r = requests.post('http://localhost:8000/user/address',
#                   json={'address': '134'})
# print(r.text, time.time() - start)

import smtplib


email = 'souldev.web3@gmail.com'
pasw = 'zzolvnzkmvkywerq'
TO = ['agibalov1294@gmail.com']
SUBJECT = 'TEST'
TEXT = 'TEST BOBA'

# Prepare actual message
message = """From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (email, ", ".join(TO), SUBJECT, TEXT)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(email, pasw)
server.sendmail(email, TO, message)
server.close()
print('successfully sent the mail')
