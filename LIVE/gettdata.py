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
tlist = []

# adds values to list
for idx, val in j.items():
    tlist.append(
        ['L1', realtime(), int(val['DP']['L1']) + int(val['Crucial']['L1']) + int(val['Panthur']['L1'])])
    tlist.append(
        ['L2', realtime(), int(val['DP']['L2']) + int(val['Crucial']['L2']) + int(val['Panthur']['L2'])])
    tlist.append(
        ['L3', realtime(), int(val['DP']['L3']) + int(val['Crucial']['L3']) + int(val['Panthur']['L3'])])
    tlist.append(
        ['Bil', realtime(), int(val['DP']['Bil']) + int(val['Crucial']['Bil']) + int(val['Panthur']['Bil'])])

# name of the sqlite database file
sqlite_file = '/home/tstatsdp/public_html/live/tdatadb.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# add data to db file
for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?)', x)

conn.commit()
conn.close()
