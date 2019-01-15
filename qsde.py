import requests, json
from flatten_dict import flatten

ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

getticketdata = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
ticketdata = json.loads(getticketdata.text)

ticketdata = flatten(ticketdata)
ticketvalue = []
for idx, itm in ticketdata.items():
    ticketvalue.append(itm)
print(ticketvalue)

###############################################################

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

now = datetime.now()
dayonsheet = now.day - 1

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sht = client.open('QDSE-Jan-2018')
worksheet = sht.get_worksheet(dayonsheet)

#writes to sheet
worksheet.update_cell(4, 4, "awwwwwyeah")
