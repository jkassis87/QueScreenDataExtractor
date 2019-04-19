# gets the first day of the available ticket data, creates the .sqlite file
# used if sqlite file is lost

import sqlite3, json, requests, time
from datetime import datetime as dt
from datetime import timedelta, date

# empty list to add the data into
tlist = []

# converts unix time to yyyy-mm-dd hh:mm:ss string
def realtime():
    timedatestring = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(idx))))
    return(timedatestring)

# defines first day that data exists for, and current date
start_date = dt(2019, 1, 15)
end_date = dt.now() - timedelta(days=1)

# adds data to list

while start_date <= end_date:
    if start_date != dt(2019, 2, 20):
        ruser = 'X'
        rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
        start_str = start_date.strftime("%Y-%m-%d")
        urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=' + start_str)
        getticketdata = requests.get(urltoget, auth=(ruser, rpass))
        j = json.loads(getticketdata.text)
        if start_date == dt(2019, 1, 15):
            sqlite_file = 'tdatadev.sqlite'
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute(r'''CREATE TABLE AllData(
            Brand Text,
            Date Int,
            Stat Int
            );
            ''')
            conn.commit()
            conn.close()
        for idx, val in j.items():
            tlist.append(
                ['L1', realtime(), int(val['DP']['L1']) + int(val['Crucial']['L1']) + int(val['Panthur']['L1'])])
            tlist.append(
                ['L2', realtime(), int(val['DP']['L2']) + int(val['Crucial']['L2']) + int(val['Panthur']['L2'])])
            tlist.append(
                ['L3', realtime(), int(val['DP']['L3']) + int(val['Crucial']['L3']) + int(val['Panthur']['L3'])])
            tlist.append(
                ['Bil', realtime(), int(val['DP']['Bil']) + int(val['Crucial']['Bil']) + int(val['Panthur']['Bil'])])
    start_date += timedelta(days=1)

# name of the sqlite database file
# NOTE: This should be updated with the full directory path of the script
sqlite_file = 'tdatadev.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# puts the data into the db
for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?)', x)

# saves the data and closes the sql connection
conn.commit()
conn.close()
