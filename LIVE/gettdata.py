import sqlite3, json, requests, csv
from datetime import datetime, timedelta, date

# gets timestamps to use
now = datetime.now() - timedelta(1)
nowst = datetime.strftime(now, '%Y-%m-%d')
yesterday = (datetime.strftime(now, '%Y') + '-' + datetime.strftime(now, '%m') + '-' + datetime.strftime(now, '%d'))

# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=' + yesterday)
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)

# creates initial lists
thour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
tlist = []

# adds values to list
x = 0
for idx, val in j.items():
    tlist.append(['L1', 'DP', yesterday, thour[x], int(val['DP']['L1'])])
    tlist.append(['L2', 'DP', yesterday, thour[x], int(val['DP']['L2'])])
    tlist.append(['L3', 'DP', yesterday, thour[x], int(val['DP']['L3'])])
    tlist.append(['BL', 'DP', yesterday, thour[x], int(val['DP']['Bil'])])
    tlist.append(['L1', 'CR', yesterday, thour[x], int(val['Crucial']['L1'])])
    tlist.append(['L2', 'CR', yesterday, thour[x], int(val['Crucial']['L2'])])
    tlist.append(['L3', 'CR', yesterday, thour[x], int(val['Crucial']['L3'])])
    tlist.append(['BL', 'CR', yesterday, thour[x], int(val['Crucial']['Bil'])])
    tlist.append(['L1', 'PA', yesterday, thour[x], int(val['Panthur']['L1'])])
    tlist.append(['L2', 'PA', yesterday, thour[x], int(val['Panthur']['L2'])])
    tlist.append(['L3', 'PA', yesterday, thour[x], int(val['Panthur']['L3'])])
    tlist.append(['BL', 'PA', yesterday, thour[x], int(val['Panthur']['Bil'])])
    x += 1

# name of the sqlite database file
sqlite_file = '/home/tstatsdp/public_html/live/tdatadb.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# add data to db file
for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?,?,?)', x)

conn.commit()
conn.close()
