# test script for getting ticket data when grabbing a date range
# for tab 3 in tstat.py


import csv
from datetime import datetime as dt
from datetime import timedelta

csvext = '.csv'

startg = str('2019-02-13')
endg = str('2019-02-16')

getstartday = int(str(startg[8]) + str(startg[9]))
getendday = int(str(endg[8]) + str(endg[9]))

getstartmon = int(str(startg[5]) + str(startg[6]))
getendmon = int(str(endg[5]) + str(endg[6]))

diffday = getendday - getstartday
diffmon = getendmon - getstartmon

tests = '77'
testr = startg[:8] + tests + startg[9 + 1:] 

comblist = []
f = open(startg + csvext, 'r')
opencsv = csv.reader(f)
addlist = list(opencsv)


while diffmon <= getendday:
    newday = startg[:8] + str(getstartday + 1) + startg[9 + 1:]
    f = open(newday + csvext, 'r')
    opencsv = csv.reader(f)
    
