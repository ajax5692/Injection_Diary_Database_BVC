# Database Import Method 2: The Pandas Way (Best for Viewing & Analysis)

import pandas as pd
from sqlalchemy import create_engine

# Connect to the database file
engine = create_engine("sqlite:///injection_diary.db")


# SQL data query examples:
# Load the entire 'animals' table into a Pandas DataFrame
df_animals = pd.read_sql_table("animals", con=engine)

# Load the 'owners' table
df_owners = pd.read_sql_table("owners", con=engine)

# Write the SQL JOIN query
query = """
    SELECT 
        animals.animal_id, 
        animals.owner_id, 
        owners.name AS owner_name
    FROM animals
    LEFT JOIN owners ON animals.owner_id = owners.id
"""

# Load the result directly into a Pandas DataFrame
df_joined = pd.read_sql_query(query, con=engine)

# View the first 10 rows
print(df_joined.head(10))
##

aa = []