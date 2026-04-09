import pandas as pd
import os
import re
import difflib
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, Session

# --------------------------
# 1. Setup File Paths & Engine
# --------------------------
# Automatically finds the folder where THIS script is saved
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "injection_diary.db")

# Read the local Excel file (this is the file fetch_excel.py downloads)
excel_path = r"C:\Users\abhrajyoti.chakrabarti\OneDrive - Femtonics Kft\Documents - 2pteam\Tables\Injection diary.xlsx"

engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base = declarative_base()

# --------------------------
# 2. Define ORM Models
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
    animal_id = Column(String, primary_key=True) 
    sex = Column(String)
    line = Column(String)
    arrival_date = Column(Date)
    age_at_arrival = Column(Integer)
    
    owner_id = Column(Integer, ForeignKey("owners.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    owner = relationship("Owner", back_populates="animals")
    project = relationship("Project", back_populates="animals")
    
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
# 3. Initialize Database
# --------------------------
Base.metadata.create_all(engine)
with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON"))

# --------------------------
# 4. Load & Clean Excel Data
# --------------------------
print("Loading Excel data...")
# Make sure your sheet_name and skiprows match your actual Excel file format
df = pd.read_excel(excel_path, sheet_name='All injections Liliom', skiprows=2, header=0)

# Remove unnamed columns and standardize names
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.rename(columns=lambda x: str(x).strip().replace(' ', '_').replace('\n', '_').lower())

if 'animal_number' in df.columns:
    df['animal_number'] = df['animal_number'].astype(str)

# Convert dates
for date_col in ['arrival_date', 'injection_date', 'surgery_date', 'drop_out_date']:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
        
# --- ADD THIS LINE TO FIX THE NaN ERROR ---
df = df.where(pd.notna(df), None)

# --------------------------
# 5. Database Insertion Logic
# --------------------------
print("Processing data into SQLite...")
session = Session(engine)

# 5A. Pre-populate clean owners to establish the "Source of Truth"
owner_cache = {}
raw_excel_owners = df['owner'].dropna().unique()

for name in raw_excel_owners:
    clean_name = str(name).strip()
    if clean_name not in owner_cache:
        # Check if they exist in DB already from a previous run
        existing = session.query(Owner).filter_by(name=clean_name).first()
        if existing:
            owner_cache[clean_name] = existing
        else:
            new_owner = Owner(name=clean_name)
            session.add(new_owner)
            session.flush() 
            owner_cache[clean_name] = new_owner

# 5B. The Automated Matcher (Handles "VK - Varada" logic)
def find_best_owner_match(messy_name):
    if pd.isna(messy_name): return None
    
    clean_input = str(messy_name).strip()
    # Strip prefixes like "LN - " or "VK-"
    if "-" in clean_input:
        clean_input = re.split(r'-\s*', clean_input)[-1].strip()
    
    clean_input = clean_input.title()

    # 1. Check our active cache
    if clean_input in owner_cache: return owner_cache[clean_input]
    
    # 2. Check for substrings
    for cached_name in owner_cache.keys():
        if cached_name in clean_input or clean_input in cached_name:
            return owner_cache[cached_name]
            
    # 3. Fuzzy matching
    matches = difflib.get_close_matches(clean_input, owner_cache.keys(), n=1, cutoff=0.6)
    if matches: return owner_cache[matches[0]]
        
    # 4. NEW SAFETY CHECK: Query the database directly before creating a new person!
    existing_person = session.query(Owner).filter_by(name=clean_input).first()
    if existing_person:
        owner_cache[clean_input] = existing_person
        return existing_person

    # 5. Only if ALL checks fail, create a new person
    new_person = Owner(name=clean_input)
    session.add(new_person)
    session.flush()
    owner_cache[clean_input] = new_person
    return new_person

# 5C. Main Loop
project_cache = {}

for _, row in df.iterrows():
    # Resolve People
    current_owner = find_best_owner_match(row.get('owner'))
    current_staff = find_best_owner_match(row.get('injection_pers.'))

    # Resolve Projects
    proj_name = row.get('project')
    if pd.notna(proj_name) and proj_name not in project_cache:
        existing_proj = session.query(Project).filter_by(name=str(proj_name)).first()
        if existing_proj:
            project_cache[proj_name] = existing_proj
        else:
            new_proj = Project(
                name=str(proj_name), 
                approval_number=str(row.get('project_approval_#')) if pd.notna(row.get('project_approval_#')) else None
            )
            session.add(new_proj)
            session.flush()
            project_cache[proj_name] = new_proj

    # Build Animal
    # Merge occurs here: If Animal_ID exists, update it. If not, create new.
    animal_id_val = str(row['animal_number'])
    animal = session.query(Animal).filter_by(animal_id=animal_id_val).first()
    
    if not animal:
        animal = Animal(animal_id=animal_id_val)
        session.add(animal)
        
    animal.sex = row.get('sex')
    animal.arrival_date = row.get('arrival_date')
    animal.age_at_arrival = row.get('age_(days)')
    animal.owner = current_owner
    animal.project = project_cache.get(proj_name)

    # Build Housing
    if not animal.housing:
        animal.housing = Housing_and_Status(animal_id=animal_id_val)
    animal.housing.state = row.get('state')
    animal.housing.category = row.get('category')
    animal.housing.box_number = str(row.get('box_#')) if pd.notna(row.get('box_#')) else None
    animal.housing.line = row.get('line')

    # Build Injection
    if pd.notna(row.get('vector_1')) or pd.notna(row.get('injection_date')):
        if not animal.injections:
            animal.injections = Injection(animal_id=animal_id_val)
        animal.injections.injection_date = row.get('injection_date')
        animal.injections.vector1 = row.get('vector_1')
        animal.injections.vector2 = row.get('vector_2')
        animal.injections.vector3 = row.get('vector_3')
        animal.injections.depth = str(row.get('depth_(µm)'))
        animal.injections.quantity = str(row.get('quant._(nl)'))
        animal.injections.notes = row.get('note_for_the_injection')
        animal.injections.person = current_staff

# 6. Save everything to disk
session.commit()
print("Database updated successfully!")