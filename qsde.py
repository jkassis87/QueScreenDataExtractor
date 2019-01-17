import requests, json
from flatten_dict import flatten

# user/pass for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

# grabs the ticket data and converts it from json to python dict
getticketdata = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
ticketdata = json.loads(getticketdata.text)

# flatens the ticket data from a 3D dict to a 1D list
ticketdata = flatten(ticketdata)
ticketvalue = []
for idx, itm in ticketdata.items():
    ticketvalue.append(itm)
print(ticketvalue)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# sets the scope/permission level for the API calls
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# authenticates with google API
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# gets day of the month (daynow) and year+month (yearmonth) as a strong
now = datetime.now()
daynow = now.day
yearmonth = (f"{now.year}-{now.month}")

#needed to initialize the sheet access, qsde_init will forever be blank
sh = client.open('qsde_init')

# creates a new spreadsheet if its the 1st day of the month, shares with specific people
### potentially need to add sheet "0" for csv template
if now.day == 1:
    sh.client.create(yearmonth)
    sh = client.open(yearmonth)
    # may need to update permissions on gogle api/auth end or generate new client_secrets
    sh.share('gaetano.egisto@hostopia.com.au', perm_type='user', role='writer')

# opens the correct spreadsheet
sh = client.open(yearmonth)

# adds a new worksheet
sh.add_worksheet(title=str(daynow), rows="17", cols="25")

# imports the template from a csv file. Currently only does the first sheet
#    need to figure out how to select a sheet when doing this
# sheet it (sh.id) needed when importing csv)
csv_template = open('qsdetemplate.csv', 'r').read()
shid = sh.id
client.import_csv(shid, csv_template)

# assigns worksheet to the specific sheet for entering data into
worksheet = sh.get_worksheet(str(daynow))

# adds ticket data into the correct worksheet
# still need to calculate totals
r = 2
c = 2
tcount = 0
ttimer = 0
for x in ticketvalue:
    if tcount < 11:
        worksheet.update_cell(r, c, x)
        r += 1
        tcount += 1
        ttimer += 1
    elif tcount == 11:
        r = 2
        c += 1
        worksheet.update_cell(r, c, x)
        tcount = 0
        ttimer += 1

# potentially email people saying script was ran succesfully, or they can check themselves???

# closes the script once it's all done
import sys
sys.exit()
