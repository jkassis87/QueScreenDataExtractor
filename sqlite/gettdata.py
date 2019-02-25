import sqlite3, json, requests, csv
from datetime import datetime, timedelta, date

now = datetime.now() - timedelta(1)
nowst = datetime.strftime(now, '%Y-%m-%d')
yesterday = (datetime.strftime(now, '%Y') + '-' + datetime.strftime(now, '%m') + '-' + datetime.strftime(now, '%d'))
dayname = now.strftime("%A")


# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=2019-1-15')
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)

thour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
tlist = []

x = 0
for idx, val in j.items():
    tlist.append(['L1', 'DP', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L1'])])
    tlist.append(['L2', 'DP', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L2'])])
    tlist.append(['L3', 'DP', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L3'])])
    tlist.append(['BL', 'DP', yesterday, dayname, thour[x], 'tcount', int(val['DP']['Bil'])])
    tlist.append(['L1', 'CR', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L1'])])
    tlist.append(['L2', 'CR', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L2'])])
    tlist.append(['L3', 'CR', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L3'])])
    tlist.append(['BL', 'CR', yesterday, dayname, thour[x], 'tcount', int(val['DP']['Bil'])])
    tlist.append(['L1', 'PA', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L1'])])
    tlist.append(['L2', 'PA', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L2'])])
    tlist.append(['L3', 'PA', yesterday, dayname, thour[x], 'tcount', int(val['DP']['L3'])])
    tlist.append(['BL', 'PA', yesterday, dayname, thour[x], 'tcount', int(val['DP']['Bil'])])
    tlist.append(['L1', 'TT', yesterday, dayname, thour[x], 'tcount', int(tlist[x][-1] + tlist[x + 3][-1] + tlist[x + 7][-1])])
    tlist.append(['L2', 'TT', yesterday, dayname, thour[x], 'tcount', int(tlist[x][-1] + tlist[x + 4][-1] + tlist[x + 8][-1])])
    tlist.append(['L3', 'TT', yesterday, dayname, thour[x], 'tcount', int(tlist[x][-1] + tlist[x + 5][-1] + tlist[x + 9][-1])])
    tlist.append(['BL', 'TT', yesterday, dayname, thour[x], 'tcount', int(tlist[x][-1] + tlist[x + 6][-1] + tlist[x + 10][-1])])
    x += 1


sqlite_file = 'tdata2.sqlite'    # name of the sqlite database file


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute(r'''CREATE TABLE AllData(
Team Text,
Brand Text,
Date Text,
Day Text,
Hour Int,
Type Text,
Stat Int
);
''')

for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?,?,?,?,?)', x)

conn.commit()
conn.close()
