# This script runs 1hr after the data gets colected, calcs averages over past 6
# of the same day, emails team leaders if most recent tcount was 50% greater than average

import sqlite3, smtplib, ssl
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

start_date = dt.now() - timedelta(days=1)
start_str = dt.strftime(start_date, '%Y-%m-%d')
end_date = dt.now() - timedelta(days=43)
end_str = dt.strftime(end_date, '%Y-%m-%d')
dayofweek = start_date.today().weekday()

# template ticket for last 6wks of data
tdata = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
         [], [], [], []]


# this function pulls ticket data from the db, calcs totals and returns the list
def gettdata(date):
    conn = sqlite3.connect("tdatamaster.sqlite")
    tlist1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    tteams = ["L1", "L2", "L3", "Bil"]
    for y in tteams:
        tstatadd = []
        for x in range(len(tlist1[0])):
            rr = "SELECT Stat FROM AllData WHERE Team = '" + y + "' AND Hour = " + str(
                x) + " AND Date = '" + date + "';"
            df = pd.read_sql_query(rr, conn)
            tlistdata = list(df["Stat"])
            tcount = sum(tlistdata)
            tstatadd.append(tcount)

        tlist1.append(tstatadd)

    return (tlist1)


# gets ticket data for yesterday
tdata_today = gettdata(start_str)

# gets ticket data for the last 6wks of yesterday's day
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


# averages are calulated here and added to a dict
def average(thedata):
    return (sum(thedata) / len(thedata))


average_stats = {'sixweeks': {'L1': average(tdata[1]), 'L2': average(tdata[2]),
                              'L3': average(tdata[3]), 'Bil': average(tdata[4])},
                 'yesterday': {'L1': average(tdata_today[1]), 'L2': average(tdata_today[2]),
                               'L3': average(tdata_today[3]), 'Bil': average(tdata_today[4])}
                 }

# dict containing team leader names, department name, and email address
team_leaders = {'L1': {'name': 'Rajan', 'dept': 'Level 1', 'email': 'rajan.shrestha@hostopia.com.au'},
                'L2': {'name': 'Gaetano', 'dept': 'Level 2', 'email': 'gaetano.egisto@hostopia.com.au'},
                'Bil': {'name': 'Cameron', 'dept': 'Billing', 'email': 'cameron.muir@hostopia.com.au'}
                }


def send_email(to_email, name, dept, av_six, av_today):
    # details for the email to send from
    from_email = 'pytest@yourdomain.net.au'
    email_pw = '0ognxm1uv3bu'
    smtp_server = 'mail.yourdomain.net.au'
    port = 465

    email_message = """Hello {},
                Tickets yesterday were higher than average for {}.
        
                Average for past 6wks: {}
                Average yesterday: {}
        
                Regards,""".format(name, dept, av_six, av_today)

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(from_email, email_pw)
        server.sendmail(from_email, to_email, email_message)



if average_stats['yesterday']['L1'] < (average_stats['sixweeks']['L1'] * 1.3):
    send_email(team_leaders['Bil']['email'], team_leaders['L1']['name'], team_leaders['L1']['dept'],
               average_stats['sixweeks']['L1'], average_stats['yesterday']['L1'])

if average_stats['yesterday']['L2'] < (average_stats['sixweeks']['L2'] * 1.3):
    send_email(team_leaders['Bil']['email'], team_leaders['L2']['name'], team_leaders['L2']['dept'],
               average_stats['sixweeks']['L2'], average_stats['yesterday']['L2'])

if average_stats['yesterday']['Bil'] < (average_stats['sixweeks']['Bil'] * 1.3):
    send_email(team_leaders['Bil']['email'], team_leaders['Bil']['name'], team_leaders['Bil']['dept'],
               average_stats['sixweeks']['Bil'], average_stats['yesterday']['Bil'])
