import json, requests

#imports json and loads it as dict
#user/pass for the ticket history api
ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

#grabs the ticket data and converts it from json to python dict
### need to modify url, create string using datetime to get previos day
getticketdata = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
j = json.loads(getticketdata.text)

#makes list with default values
###need to add list of hours
tlist = [['DPL1'], ['DPL2'], ['DPL3'], ['DPLB'],
         ['CRL1'], ['CRL2'], ['CRL3'], ['CRLB'],
         ['PAL1'], ['PAL2'], ['PAL3'], ['PALB'],
         ['TTL1'], ['TTL2'], ['TTL3'], ['TTLB'],
         ['DFL1', 0], ['DFL2', 0], ['DFL3', 0], ['DFLB', 0]]


#populates list with ticket stats from json
for idx, val in j.items():
    #DPL1.append(val[
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

#calculates totals, appends to list
count = 1
while count < 25:
    tlist[12].append(tlist[0][count] + tlist[4][count] + tlist[8][count])
    tlist[13].append(tlist[1][count] + tlist[5][count] + tlist[9][count])
    tlist[14].append(tlist[2][count] + tlist[6][count] + tlist[10][count])
    tlist[15].append(tlist[3][count] + tlist[7][count] + tlist[11][count])
    count += 1

#calculates difference, appends to list
###need to confirm if last hour gets appended
x = 1
while x < 24:
    z = tlist[12][x] - tlist[12][x + 1]
    tlist[16].append(z)
    z = tlist[13][x] - tlist[13][x + 1]
    tlist[17].append(z)
    z = tlist[14][x] - tlist[14][x + 1]
    tlist[18].append(z)
    z = tlist[15][x] - tlist[15][x + 1]
    tlist[19].append(z)
    x += 1

for item in tlist:
    print(item, end='\n')



