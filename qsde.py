import requests, json

### 1 - import ticket data into script ###

# need to convert time from unix to normal, then sydney time, then account for daylight savings

ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

getticketdata = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
ticketdata = json.loads(getticketdata.txt)

### 2 - convert json to list ###

# timestamp is unix time, need to convert to GMT then to AEST + daylight savings



### END 1 ###

### 3 - export data into gsheet ###

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#code should open "current month" create it if it doesn't exist
sheet = client.open("Jan2018").sheet1

#writes to sheet
sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")
## dummy data ##


#update specific sheet, get_worksheet(int/index)
ws = sheet.get_worksheet(1)
ws.update_acell('C3', 'Gspreadit')
## dummy data ##


