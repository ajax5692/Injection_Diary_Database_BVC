# This script creates a SQLite database and populates it with data from an Excel file.
# It defines the database schema using SQLAlchemy ORM models, establishes relationships
# between tables, and includes a data cleaning function to handle discrepancies in owner
# and staff names, ensuring a consistent dataset.

from Read_excel_table import df
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, Session
# import difflib
import re

# --------------------------
# 1. Create SQLite engine
# --------------------------
engine = create_engine("sqlite:///injection_diary.db", echo=False)
Base = declarative_base()

# --------------------------
# 2. Define ORM models
# --------------------------
class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    animals = relationship("Animal", back_populates="owner")
    injections_performed = relationship("Injection", back_populates="person")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    approval_number = Column(String)
    
    animals = relationship("Animal", back_populates="project")

class Animal(Base):
    __tablename__ = "animals"
    # Set to String in case your IDs have letters (e.g., "M123")
    animal_id = Column(String, primary_key=True) 
    sex = Column(String)
    line = Column(String)
    arrival_date = Column(Date)
    age_at_arrival = Column(Integer)
    
    owner_id = Column(Integer, ForeignKey("owners.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    owner = relationship("Owner", back_populates="animals")
    project = relationship("Project", back_populates="animals")
    
    # uselist=False forces a 1:1 relationship
    housing = relationship("Housing_and_Status", back_populates="animal", uselist=False)
    injections = relationship("Injection", back_populates="animal", cascade="all, delete-orphan", uselist=False)

class Injection(Base):
    __tablename__ = "injections"
    animal_id = Column(String, ForeignKey("animals.animal_id"), primary_key=True)
    injection_date = Column(Date)
    vector1 = Column(String)
    vector2 = Column(String)
    vector3 = Column(String)
    depth = Column(String)
    quantity = Column(String) 
    notes = Column(String)
    
    person_id = Column(Integer, ForeignKey("owners.id"))
    
    animal = relationship("Animal", back_populates="injections")
    person = relationship("Owner", back_populates="injections_performed")

class Housing_and_Status(Base):
    __tablename__ = "housing_and_status"
    animal_id = Column(String, ForeignKey("animals.animal_id"), primary_key=True)
    state = Column(String)
    category = Column(String)
    box_number = Column(String)
    
    animal = relationship("Animal", back_populates="housing")

# --------------------------
# 3. Create tables
# --------------------------
Base.metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON"))

# --------------------------
# 4. Clean DataFrame (Run this BEFORE inserting)
# --------------------------
# Remove unnamed columns and standardize names to lowercase with underscores
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.rename(columns=lambda x: x.strip().replace(' ', '_').replace('\n', '_').lower())

# Ensure primary keys are strings
if 'animal_number' in df.columns:
    df['animal_number'] = df['animal_number'].astype(str)

# Convert dates to actual Python Date objects
for date_col in ['arrival_date', 'injection_date', 'surgery_date', 'drop_out_date']:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date

# --------------------------
# 5. Insert Data via ORM
# --------------------------
session = Session(engine)

# 5A. Pre-populate the cache with CLEAN owners from the 'owner' column
# This ensures these names are the "Source of Truth"
owner_cache = {}
raw_excel_owners = df['owner'].dropna().unique()

for name in raw_excel_owners:
    clean_name = str(name).strip()
    if clean_name not in owner_cache:
        new_owner = Owner(name=clean_name)
        session.add(new_owner)
        session.flush() 
        owner_cache[clean_name] = new_owner

# 5B. Automated Mapping Function with Prefix Cleaning
def find_best_owner_match(messy_name):
    if pd.isna(messy_name): 
        return None
    
    # 1. CLEANING LOGIC
    # This regex looks for any characters followed by a hyphen and optional spaces
    # It turns "LN-lenkey Nora" or "LN - lenkey Nora" into "lenkey Nora"
    clean_input = str(messy_name).strip()
    if "-" in clean_input:
        clean_input = re.split(r'-\s*', clean_input)[-1].strip()
    
    # Fix capitalization (e.g., 'lenkey Nora' -> 'Lenkey Nora')
    clean_input = clean_input.title()

    # 2. CHECK CACHE
    # First, try to match what we already have
    if clean_input in owner_cache: 
        return owner_cache[clean_input]
    
    # 3. SUBSTRING/FUZZY CHECK
    # Check if 'Lenkey Nora' is already in our cache under a slightly different name
    for cached_name in owner_cache.keys():
        if cached_name in clean_input or clean_input in cached_name:
            return owner_cache[cached_name]
            
    # 4. CREATE NEW ENTRY
    # If we get here, the name is truly new. Add it using the CLEAN name.
    new_person = Owner(name=clean_input)
    session.add(new_person)
    session.flush()
    owner_cache[clean_input] = new_person
    return new_person

project_cache = {}

# --- MAIN LOOP ---
for _, row in df.iterrows():
    
    # --- 5C. Handle Owners & Staff AUTOMATICALLY ---
    # We use the function for BOTH to ensure they link to the same records
    current_owner = find_best_owner_match(row.get('owner'))
    current_staff = find_best_owner_match(row.get('injection_pers.'))

    # --- 5D. Handle Unique Projects ---
    proj_name = row.get('project')
    if pd.notna(proj_name) and proj_name not in project_cache:
        new_proj = Project(
            name=str(proj_name), 
            approval_number=str(row.get('project_approval_#')) if pd.notna(row.get('project_approval_#')) else None
        )
        session.add(new_proj)
        session.flush()
        project_cache[proj_name] = new_proj

    # --- 5E. Create the Animal ---
    animal = Animal(
        animal_id=str(row['animal_number']),
        sex=row.get('sex'),
        line=row.get('line'),
        arrival_date=row.get('arrival_date'),
        age_at_arrival=row.get('age_(days)'),
        owner=current_owner, # Use the object returned by the function
        project=project_cache.get(proj_name)
    )

    # --- 5F. Attach Housing & Status ---
    animal.housing = Housing_and_Status(
        state=row.get('state'),
        category=row.get('category'),
        box_number=str(row.get('box_#')) if pd.notna(row.get('box_#')) else None,
    )

    # --- 5G. Attach Injection ---
    if pd.notna(row.get('vector_1')) or pd.notna(row.get('injection_date')):
        animal.injections = Injection(
            injection_date=row.get('injection_date'),
            vector1=row.get('vector_1'),
            vector2=row.get('vector_2'),
            vector3=row.get('vector_3'),
            depth=str(row.get('depth_(µm)')), 
            quantity=str(row.get('quant._(nl)')),
            notes=row.get('note_for_the_injection'),
            person=current_staff # Use the object returned by the function
        )

    session.add(animal)

session.commit()
print("Data migration complete!")