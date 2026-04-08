# This file contains the core functions to create the database schema and import data from the Excel file into the SQLite database.
# It defines the SQLAlchemy models for each table, establishes relationships between them, and includes functions to read the Excel
# data and populate the database accordingly. The code is structured to ensure data integrity and consistency, with checks for
# discrepancies in owner and injector names to maintain a clean dataset.


from Read_excel_table import df
from Create_SQLite_engine import engine
import pandas as pd