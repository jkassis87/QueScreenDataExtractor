import json, requests
from datetime import datetime, timedelta

# gets the previos day's date in YYYY-MM-DD string
now = datetime.now() - timedelta(1)
yesterday = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))

# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=' + yesterday)

# grabs the ticket data and converts it from json to python dict
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)

# makes list with default values
tlist = [
    ['x', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
     '18', '19', '20', '21', '22', '23', '24'],
    ['DPL1'], ['DPL2'], ['DPL3'], ['DPLB'],
    ['CRL1'], ['CRL2'], ['CRL3'], ['CRLB'],
    ['PAL1'], ['PAL2'], ['PAL3'], ['PALB'],
    ['TTL1'], ['TTL2'], ['TTL3'], ['TTLB'],
    ['DFL1'], ['DFL2'], ['DFL3'], ['DFLB']
    ]

# populates list with ticket stats from json
for idx, val in j.items():
    tlist[1].append(int(val['DP']['L1']))
    tlist[2].append(int(val['DP']['L2']))
    tlist[3].append(int(val['DP']['L3']))
    tlist[4].append(int(val['DP']['Bil']))
    tlist[5].append(int(val['Crucial']['L1']))
    tlist[6].append(int(val['Crucial']['L2']))
    tlist[7].append(int(val['Crucial']['L3']))
    tlist[8].append(int(val['Crucial']['Bil']))
    tlist[9].append(int(val['Panthur']['L1']))
    tlist[10].append(int(val['Panthur']['L2']))
    tlist[11].append(int(val['Panthur']['L3']))
    tlist[12].append(int(val['Panthur']['Bil']))


import gspread
from oauth2client.service_account import ServiceAccountCredentials

# sets the scope/permission level for the API calls
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# authenticates with google API
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# gets day of the month (daynow) and year+month (yearmonth) as a strong
daynow = now.day
yearmonth = (f"{now.year}-{now.month}")
yesterday = datetime.now() - timedelta(days=1)

# opens the current months spreadsheet
sh = client.open(yearmonth)

# shares spreadsheet if it's the first day of the month/new spreadsheet
if daynow == 1:
    sh.share('j17747@gmail.com', perm_type='user', role='writer')

wstoupdate = str(f"{now.day}!A1")

# export list into gsheet
sh.values_update(
    wstoupdate,
    params={'valueInputOption': 'RAW'},
    body={'values': tlist}
)