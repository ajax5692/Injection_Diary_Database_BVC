from Read_excel_table import df
#import sqlite3
import pandas as pd
from sqlalchemy import create_engine


# Create SQLite engine
engine = create_engine('sqlite:///injection_diary.db')

# Clean and prepare data (fix dates, drop unnamed columns)
df['Animal number'] = df['Animal number'].astype(str)  # Ensure ID is string/key
df.to_sql('animals', engine, if_exists='replace', index=False)

# Verify
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT COUNT(*) FROM animals")).scalar()
#     print(f"Loaded {result} records.")  # Expect ~100 mice[file:1]

aa = 'stopStringForTesting'