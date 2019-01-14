import requests

# http://docs.python-requests.org/en/master/user/quickstart/
# need to convert time from unix to normal, then sydney time, then account for daylight savings

ruser = 'X'
rpass = '5rsMThTeZ22p3MqGpz2xRPGY5hAWrwmx'

r = requests.get('http://pbx02.apdcsy1.digitalpacific.com.au/tickethistory_api.php', auth=(ruser, rpass))
#r.json()
print(r.json())
