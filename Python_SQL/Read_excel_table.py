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
