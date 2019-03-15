# gets the first day of the available ticket data, creates the .sqlite file
# now adds time/date using unix time

import sqlite3, json, requests, time
from datetime import datetime, timedelta, date

# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=2019-1-15')
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)

# empty list to add the data into
tlist = []

# converts unix time to yyyy-mm-dd hh:mm:ss string
def realtime():
    timedatestring = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(idx))))
    return(timedatestring)

# adds data to list
x = 0
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
    x += 1

# name of the sqlite database file
# NOTE: This should be updated with the full directory path of the script
sqlite_file = 'tdatadev.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute(r'''CREATE TABLE AllData(
Team Text,
Brand Text,
Date Int,
Stat Int
);
''')

# puts the data into the db
for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?,?)', x)

# saves the data and closes the sql connection
conn.commit()
conn.close()
