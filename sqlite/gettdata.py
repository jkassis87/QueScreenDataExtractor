import sqlite3, json, requests, csv
from datetime import datetime, timedelta, date
from os.path import isdir
from os import mkdir, makedirs


# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=2019-1-15')

# grabs the ticket data and converts it from json to python dict
getticketdata = requests.get(urltoget, auth=(ruser, rpass))
j = json.loads(getticketdata.text)
tlist = [[], [], [], [], [], [], [], [], [], [], [], []]

for idx, val in j.items():
    tlist[0].append(int(val['DP']['L1']))
    tlist[1].append(int(val['DP']['L2']))
    tlist[2].append(int(val['DP']['L3']))
    tlist[3].append(int(val['DP']['Bil']))
    tlist[4].append(int(val['Crucial']['L1']))
    tlist[5].append(int(val['Crucial']['L2']))
    tlist[6].append(int(val['Crucial']['L3']))
    tlist[7].append(int(val['Crucial']['Bil']))
    tlist[8].append(int(val['Panthur']['L1']))
    tlist[9].append(int(val['Panthur']['L2']))
    tlist[10].append(int(val['Panthur']['L3']))
    tlist[11].append(int(val['Panthur']['Bil']))


sqlite_file = 'tdata.sqlite'    # name of the sqlite database file


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute(r'''CREATE TABLE JanOne(
DPL1 Int,
DPL2 Int,
DPL3 Int,
DPBL Int,
CRL1 Int,
CRL2 Int,
CRL3 Int,
CRBL Int,
PAL1 Int,
PAL2 Int,
PAL3 Int,
PABL Int,
TTL1 Int,
TTL2 Int,
TTL3 Int,
TTBL Int,
DFL1 Int,
DFL2 Int,
DFL3 Int,
DFBL Int
);
''')

for i in range(len(tlist)):
    c.execute("INSERT INTO JanOne (DPL1, DPL2, DPL3, DPBL, CRL1, CRL2, CRL3, CRBL, PAL1, PAL2, PAL3, PABL,)"
              " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (tlist[0][i], tlist[1][i], tlist[2][i], tlist[3][i], tlist[4][i], tlist[5][i], tlist[6][i], tlist[7][i], tlist[8][i], tlist[9][i], tlist[10][i], tlist[11][i],))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
