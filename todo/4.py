import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

#sets all relevant email details/items

email = 'pytest@yourdomain.net.au'
password = '0ognxm1uv3bu'
send_to_email = 'jay.kassis@hostopia.com.au'
subject = 'Ticket Board Stats for Today Test2'
message = 'Please see attached csv for ticket stats'
file_location = 'C:\\pytest\\2csv.csv'

#MIME formatting for email

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('vmcp24.digitalpacific.com.au', 587)
#server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()

print("done")
