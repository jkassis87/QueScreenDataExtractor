import requests, json, sqlite3
from datetime import datetime as dt

# ticket stats url = r"https://support.digitalpacific.com.au/api/ticket/filter?id=12"

auth = "vus6=2a0#xb1yu%Eqm7Gz4sB7RwKLCYQ"
psw = "x"
url = r"https://support.digitalpacific.com.au/api/ticket/filter?id=5"

getticketdata = requests.get(url, auth=(auth, psw))
j = json.loads(getticketdata.text)

now = dt.now().replace(second=0, microsecond=0)
sqlite_file = 'sptest.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute(r'CREATE TABLE AllData(Dept Text, Date Text, Type Text, Stat Int);')

tlist = []
tlist.append(['L1', str(now), 'In Queue', j['data'][0]['ticket_count']])
tlist.append(['L2', str(now), 'In Queue', j['data'][2]['ticket_count']])
tlist.append(['L3', str(now), 'In Queue', j['data'][3]['ticket_count']])
tlist.append(['B1', str(now), 'In Queue', j['data'][4]['ticket_count']])
tlist.append(['B2', str(now), 'In Queue', j['data'][5]['ticket_count']])

for x in tlist:
    c.execute('INSERT INTO AllData VALUES (?,?,?,?)', x)
conn.commit()
conn.close()
