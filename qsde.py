import requests, json
from flatten_dict import flatten

### 1 - import ticket data into script ###
# flatten will take care of the multidimentional dict problems
# need to convert time from unix to normal, then sydney time, then account for daylight savings

# username and password for the ticket history page
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

# retrieves ticket history and loads json data as python dict
# need to have url appended with date so it get's the previous day's stats each time it runs (at 1am)
getticketdata = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
ticketdata = json.loads(getticketdata.text)

# flattens the 3d dict into a 1d dict
ticketdata = flatten(ticketdata)

# creates a list of just the ticket stats
ticketvalue = []
for idx, itm in ticketdata.items():
    ticketvalue.append(itm)
print(ticketvalue)

### 2 - convert json to list ###

# timestamp is unix time, need to convert to GMT then to AEST + daylight savings



### END 1 ###

### 3 - export data into gsheet ###

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

now = datetime.now()
dayofw = now.day

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sht = client.open('QDSE-Jan-2018')
worksheet = sht.get_worksheet(dayofw)

#writes to sheet
worksheet.update_cell(3, 3, "I just wrote to a spreadsheet using Python!")
