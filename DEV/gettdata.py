# gets ticket data, using unix time

import sqlite3, json, requests, time
from datetime import datetime, timedelta, date

# gets date for urltoget, currently messy
now = datetime.now() - timedelta(1)
nowst = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
yesterday = (datetime.strftime(now, '%Y') + '-' + datetime.strftime(now, '%m') + '-' + datetime.strftime(now, '%d'))

# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=' + yesterday)
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)

# empty list to add the data into
tlist = []

# converts unix time to yyyy-mm-dd hh:mm:ss string
def realtime():
    timedatestring = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(idx))))
    return(timedatestring)

# adds data to list
for idx, val in j.items():
    tlist.append(['L1', 'DP', realtime(), int(val['DP']['L1'])])
    tlist.append(['L2', 'DP', realtime(), int(val['DP']['L2'])])
    tlist.append(['L3', 'DP', realtime(), int(val['DP']['L3'])])
    tlist.append(['Bil', 'DP', realtime(), int(val['DP']['Bil'])])
    tlist.append(['L1', 'CR', realtime(), int(val['Crucial']['L1'])])
    tlist.append(['L2', 'CR', realtime(), int(val['Crucial']['L2'])])
    tlist.append(['L3', 'CR', realtime(), int(val['Crucial']['L3'])])
    tlist.append(['Bil', 'CR', realtime(), int(val['Crucial']['Bil'])])
    tlist.append(['L1', 'PA', realtime(), int(val['Panthur']['L1'])])
    tlist.append(['L2', 'PA', realtime(), int(val['Panthur']['L2'])])
    tlist.append(['L3', 'PA', realtime(), int(val['Panthur']['L3'])])
    tlist.append(['Bil', 'PA', realtime(), int(val['Panthur']['Bil'])])

# name of the sqlite database file
sqlite_file = 'tdatadev.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# adds list into sqlite file
for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?,?)', x)

# saves the changes and closes the sqlite connection
conn.commit()
conn.close()
