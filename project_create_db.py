import pandas as pd
import sqlite3

EXCEL_FILE = "Enhanced_Placement_Data_Project.xlsx"
DB_FILE = "placements.db"

df = pd.read_excel(EXCEL_FILE)

conn = sqlite3.connect(DB_FILE)
df.to_sql("placements", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")
