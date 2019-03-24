App for graphing ticket stats got Hostopia L1 / L2 /L3 /Billing

Requires Python 3.5+


=====3rd Party Modules Required=====
dash
dash_auth
dash_core_components
dash_html_components
numpy
pandas
dateutil


=====Install Guide=====

1)  Download all files into a folder then run getalldata.py
    This will create the .sqlite database and download all
    existing data

2)  Update the line under "# name of the sqlite database file" in gettdata.py
    with the full dir of the .sqlite file. Do the same for "conn = sqlite3.connect"
    in the tstats.py file

3)  Create the following 2 crons:

0	2	*	*	*	/home/tstatsdp/public_html/live/bin/python3.5 /home/tstatsdp/public_html/live/gettdata.py	    
0	6	*	*	*	/home/tstatsdp/public_html/live/bin/python3.5 /home/tstatsdp/public_html/live/tstats.py

NOTE1: The first cron insert's the previous day's ticket data into the .sqlite file
NOTE2: The second cron runs/restarts the front end

3)  Once the tstats.py file is running, visit tstats.digitalpacific.com.au:8050 to access the app
    If needed, the hostname can be changed by modifying the "app.run_server(host=" line in tstats.py

