import gspread
from oauth2client.service_account import ServiceAccountCredentials

#note 1: need to enable drive and sheet in google api then wait 30min
#note 2: g-api > credentials > create credential > service account > create it
# name: anything, role: project > project editor > download json
# rename to client_secret.json
#note 3: in client_secrets.json find client_email share spreadsheet with this emain in gsheeds gui
#note 4: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Legislators2017").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

#writes to sheet
sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")

#pulls data from sheet
sheet.row_values(1)
sheet.col_values(1)
sheet.cell(1, 1).value

#insert row into sheet
row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
index = 1
sheet.insert_row(row, index)

#delete row from sheet
sheet.delete_row(1)

#get row count
sheet.row_count
sheet.delete_row(1)