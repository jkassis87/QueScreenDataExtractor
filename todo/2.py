import csv

#opens the txt as f and converts to list
f = open('C:\\pytest\\qs1020.txt', 'r').readlines()

#extracts ticket count into list, removes unneeded data
new = []
for idx, val in enumerate(f):
    if idx > 23 and idx < 29:
        new.append(val.split())

# list of headers (column titles)
new_head = [
    '00', '01', '02', '03', '04', '05',
    '06', '07', '08', '09', '10', '11',
    '12', '13', '14', '15', '16', '17',
    '18', '19', '20', '21', '22', '23',
    ]

# list of rows (row titles)
new_body = [
  ["DP-L1"], ["DP-L2"], ["DP-L3/4"], ["DP-Billing"], ["DP-Total"],
  ["CR-L1"], ["CR-L2"], ["CR-L3/4"], ["CR-Billing"], ["CR-Total"],
  ["PA-L1"], ["PA-L2"], ["PA-L3/4"], ["PA-Billing"], ["PA-Total"],
  ["TL-L1"], ["TL-L2"], ["TL-L3/4"], ["TL-Billing"], ["TL-ALL"],
    ]
