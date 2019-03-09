# This script runs 1hr after the data gets colected, calcs averages over past 6
# of the same day, emails team leaders if most recent tcount was 50% greater than average
import dash, dash_auth, re, csv, sqlite3
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

start_date = dt.now() - timedelta(days=1)
start_str = dt.strftime(start_date, '%Y-%m-%d')
end_date = dt.now() - timedelta(days=43)
end_str = dt.strftime(end_date, '%Y-%m-%d')
dayofweek = start_date.today().weekday()


tdata = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
         [], [], [], [], [], [], [], [], []]

def gettdata(date):
    conn = sqlite3.connect("tdatamaster.sqlite")
    tlist1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    tteams = ["L1", "L2", "L3", "Bil"]
    for y in tteams:
        tstatadd = []
        for x in range(len(tlist1[0])):
            rr = "SELECT Stat FROM AllData WHERE Team = '" + y + "' AND Hour = " + str(x) + " AND Date = '" + date + "';"
            df = pd.read_sql_query(rr, conn)
            tlistdata = list(df["Stat"])
            tcount = sum(tlistdata)
            tstatadd.append(tcount)

        tlist1.append(tstatadd)

    return (tlist1)

tdata_today = gettdata(start_str)

while end_date <= start_date:
    if end_date.today().weekday() == dayofweek:
        end_str = dt.strftime(end_date, '%Y-%m-%d')
        tdatax = gettdata(end_str)
        tdata[0].extend(tdatax[0])
        tdata[1].extend(tdatax[1])
        tdata[2].extend(tdatax[2])
        tdata[3].extend(tdatax[3])
        tdata[4].extend(tdatax[4])

    end_date += timedelta(days=1)

for x in tdata_today:
    print(x, end='\n')
