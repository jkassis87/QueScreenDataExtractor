#note1: needs pydrive module installed
#note2: need to go to "https://console.developers.google.com/apis/credentials"
# create  credentials > download json > place it in same folder as .py
# rename it client_secrets.json (secrets, not secret)

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

file1 = drive.CreateFile()
file1.SetContentFile('2csv.csv')
file1.Upload()