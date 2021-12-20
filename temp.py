import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file=r'C:\Users\ASER\Documents\GitHub\pars_project_vfat\crafty-ensign-334507-b0a14a1f80f2.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('try python')

#select the first sheet
wks = sh[0]

#update the first sheet with df, starting at cell B2.
wks.set_dataframe(df,(1,1))