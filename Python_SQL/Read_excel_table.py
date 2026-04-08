import pandas as pd
#import sqlite3
#from sqlalchemy import create_engine, text

# This is not ideal and can be removed later
import warnings
warnings.filterwarnings("ignore")

# Load Excel (adjust path to your file)
file_path = 'Injection diary.xlsx'
df = pd.read_excel(file_path, sheet_name='All injections Liliom', skiprows=2, header=0)  # Skip notes/headers to reach data
df = df.dropna(how='all')  # Drop empty rows

# This is to cross check how the data read from the excel file looks like
#print(df.head())  # Inspect columns like Animal number, State, OGR number, Injection Date, etc.
#print(df)

# This part is to check if there are any discrepancies between the 'Owner' and 'Injection\nPers.' columns, which should ideally have the same names. This will help us identify any names that need to be added to the name_fixes dictionary in Create_SQLite_engine.py to ensure data consistency when we import it into the database.
# owners = set(df['Owner'].dropna().unique())
# injectors = set(df['Injection\nPers.'].dropna().unique())

# # Show me names in injectors that are NOT in owners
# discrepancies = injectors - owners
# print("Names to add to your name_fixes dictionary:", discrepancies)