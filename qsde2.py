import json

f = open('tdata.json', 'r')
j = json.load(f)

tlist = [['DPL1'], ['DPL2'], ['DPL3'], ['DPLB'],
         ['CRL1'], ['CRL2'], ['CRL3'], ['CRLB'],
         ['PAL1'], ['PAL2'], ['PAL3'], ['PALB'],
         ['TTL1'], ['TTL2'], ['TTL3'], ['TTLB'],
         ['DFL1'], ['DFL2'], ['DFL3'], ['DFLB']]

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

count = 1
while count < 13:
    tlist[12].append(tlist[0][count] + tlist[4][count] + tlist[8][count])
    tlist[13].append(tlist[1][count] + tlist[5][count] + tlist[9][count])
    tlist[14].append(tlist[2][count] + tlist[6][count] + tlist[10][count])
    tlist[15].append(tlist[3][count] + tlist[7][count] + tlist[11][count])
    count += 1


