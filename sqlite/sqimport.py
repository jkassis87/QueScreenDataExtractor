# test for playing with data from sqlite file

import sqlite3
import pandas as pd
conn = sqlite3.connect("tdata3.sqlite")

rr = "SELECT Stat FROM AllData WHERE Team = 'L1' AND Brand = 'DP';"

df = pd.read_sql_query(rr, conn)

tlist0 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
tlist1 = list(df["Stat"])

for x in range(len(tlist0)):
    print(tlist1[x], ' ', tlist0[x])
