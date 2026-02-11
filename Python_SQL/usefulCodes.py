#shows all the tables in the database, which can be useful for understanding the database structure and available data.
pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", engine)

#shows full table structure, including column names and types
pd.read_sql("PRAGMA table_info(animals)", engine)

#shows all the unique owners in the database, which can be useful for filtering or analysis.
pd.read_sql("SELECT [Owner] FROM animals", engine)

#shows all the animal numbers owned by Abhrajyoti Chakrabarti, which can be useful for filtering or analysis.
pd.read_sql("SELECT [Animal number] FROM animals WHERE [Owner] = 'Abhrajyoti Chakrabarti'", engine)

#shows the first two rows of the DataFrame, which can be useful for quickly inspecting the data and understanding
#its structure.
top2Results = df.head(2)

#shows the first row and first three columns of the DataFrame, which can be useful for quickly inspecting specific
#data points or understanding the structure of the DataFrame.
firstRowOnlyThreeColumns = df.iloc[:1, :3]

#shows the value in the first row and first column of the DataFrame, which can be useful for quickly inspecting a specific
#data point or understanding the structure of the DataFrame.
print(df.iloc[0,0])

#shows all the unique owners in the database, which can be useful for filtering or analysis.
users = pd.read_sql("SELECT DISTINCT [Owner] FROM animals", engine)