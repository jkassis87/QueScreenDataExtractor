# run this script first, once. Gets the oldest ticket stats available (Jan 15 2019)
# this is needed for difference to calculate on all other days

import json, requests, csv
from datetime import datetime, timedelta

# gets the previous day's date in YYYY-MM-DD string
now = datetime.now() - timedelta(27)
yesterday = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))

# user/pass and URL for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'
urltoget = (r'http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php?date=2019-1-15' + yesterday)

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

# calculates totals TTL
x = 1
while x < 25:
    tlist[13].append(tlist[1][x] + tlist[5][x] + tlist[9][x])
    tlist[14].append(tlist[2][x] + tlist[6][x] + tlist[10][x])
    tlist[15].append(tlist[3][x] + tlist[7][x] + tlist[11][x])
    tlist[16].append(tlist[4][x] + tlist[8][x] + tlist[12][x])
    x += 1

# prints the data to be saved to a csv, for self checking only
for x in tlist:
    print(x, end='\n')

# writes new csv file with all relevant data
with open(str(yesterday + '.csv'),'w', newline= '') as f:
    writer = csv.writer(f)
    writer.writerows(tlist)
