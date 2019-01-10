import itertools, csv

#opens the txt as f and converts to list
f = open('C:\\pytest\\qs1020.txt', 'r').readlines()

#extracts ticket count into list, removes unneeded data
new_data = []
for idx, val in enumerate(f):
    if idx > 24 and idx < 29:
        new_data.append(val.split())
        
# removes level/team name and number from new_data
for val in new_data:
    del(val[0])
    if len(val) == 5:
        del(val[0])

#flatts list from 2d > 1d, as every 4 val's are for dp/cr/pa/tl, this makes the end result easier
new_data = list(itertools.chain.from_iterable(new_data))

# list of headers (column titles)
new_head = [
    '00', '01', '02', '03', '04', '05',
    '06', '07', '08', '09', '10', '11',
    '12', '13', '14', '15', '16', '17',
    '18', '19', '20', '21', '22', '23',
    ]

# list of rows (row titles)
new_body = [
  ["DP-L1"], ["CR-L1"], ["PA-L1"], ["TL-L1"],
  ["DP-L2"], ["CR-L2"], ["PA-L2"], ["TL-L2"],
  ["DP-L3"], ["CR-L3"], ["PA-L3"], ["TL-L3"],
  ["DP-Bi"], ["Cr-Bi"], ["PA-Bi"], ["TL-Bi"],
    ]

#print(new_data)

for valx, valy in zip(new_data, new_body):
    valy.append(valx)
    
print(new_body)

#formats list, this needs work

for idx1, val1 in enumerate(new_body):
    for idx2, val2 in enumerate(val1):
        new_body[idx1][idx2] = new_body[idx1][idx2].replace('\n', '')

# writes list to existing csvfile, this needs work

with open('C:\\pytest\\2csv.csv', 'w', newline='') as f:
    writer=csv.writer(f)
