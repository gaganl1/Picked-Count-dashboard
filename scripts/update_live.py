import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Read current month from GSheet
sheet = client.open("Flag by date").worksheet("July")  # update month name as needed
df = pd.DataFrame(sheet.get_all_records())

# Aggregate
df['date'] = pd.to_datetime(df['mp_received_at_origin_date_key']).dt.strftime('%Y-%m-%d')
df = df[df['Flag'].isin(['Past', 'Present', 'Future'])]
agg = df.groupby(['date','GM','Zone','name','Stack','Flag'], as_index=False)['Picked_count'].sum()
agg.columns = ['date','gm','zone','name','stack','flag','picked_count']

agg.to_csv('data/jul_2026.csv', index=False)
print(f"Done: {len(agg)} rows written to data/jul_2026.csv")
