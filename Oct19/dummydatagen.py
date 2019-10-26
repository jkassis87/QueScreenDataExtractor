# generates a years worth of dummy data for this project
# Needs a db named gettest and a table named all data with these colums
# ID TStampt TBrand Team TixNew TixAnswered TixWaiting WaitUnder3h Wait3hto12h Wait12hto24h WaitOver24h

import pymysql, random
from datetime import datetime as dt
from datetime import timedelta, date

# empty list to add the data into
tlist = []
teams = ['L1', 'L1', 'L1', 'L2', 'L2', 'L2', 'Bil', 'Bil', 'Bil']
brands = ['DP', 'CR', 'PAN', 'DP', 'CR', 'PAN', 'DP', 'CR', 'PAN']



# defines first day that data exists for, and current date
start_date = dt(2018, 6, 1)
end_date = dt(2019, 5, 30)
id = 0
tid = 0
bid = 0

# adds data to list

while start_date <= end_date:
    id += 1

    tlist.append([
        str(id), # table ID
        str(start_date), # table TStamp
        teams[tid], # table team
        brands[bid], # table brand
        str(random.randint(0,10)), # table TixNew
        str(random.randint(0, 10)), # table TixAnswered
        str(random.randint(0, 100)), # table TixWaiting
        str(random.randint(0, 10)), # table WaitUnder3h
        str(random.randint(0, 10)), # table Wait3hto12h
        str(random.randint(0, 10)), # table Wait12hto24h
        str(random.randint(0, 10)), # table WaitOver24h
    ])

    if tid == 8:
        tid = 0
    else:
        tid += 1

    if bid == 8:
        bid = 0
    else:
        bid += 1

    start_date += timedelta(minutes=5)

for x in tlist:
    print(x)


db = pymysql.connect("localhost","larauser","password","gettest" )
c = db.cursor()
c.executemany("INSERT INTO alldata(ID, TStamp, Brand, Team, TixNew, TixAnswered, TixWaiting, WaitUnder3h, Wait3hto12h, Wait12hto24h, WaitOver24h) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (tlist))
db.commit()

db.close()
