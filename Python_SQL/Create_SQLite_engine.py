from Read_excel_table import df
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, Session

# --------------------------
# 1. Create SQLite engine
# --------------------------
engine = create_engine("sqlite:///injection_diary.db", echo=False)
Base = declarative_base()

# --------------------------
# 2. Define ORM models
# --------------------------
class Animal(Base):
    __tablename__ = "animals"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    #animal_id = Column(String, unique=True, nullable=False)
    animal_id = Column(String, primary_key=True)
    sex = Column(String)
    category = Column(String)

    injections = relationship("Injection", back_populates="animal", cascade="all, delete-orphan")


class Injection(Base):
    __tablename__ = "injections"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    #animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    animal_id = Column(String, ForeignKey("animals.animal_id"), primary_key=True)
    injection_date = Column(Date)
    vector1 = Column(String)
    vector2 = Column(String)
    vector3 = Column(String)

    animal = relationship("Animal", back_populates="injections")

# --------------------------
# 3. Create tables
# --------------------------
Base.metadata.create_all(engine)

# Enable foreign key enforcement in SQLite
with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON"))

# --------------------------
session = Session(engine)

# Example: insert animals from df
for _, row in df.iterrows():
    animal = Animal(
        animal_id=str(row['Animal number']),
        sex=row.get('Sex'),
        category=row.get('Category')
    )
    session.add(animal)

session.commit()
#--------------------------



# # --------------------------
# # 4. Clean DataFrame
# # --------------------------
# # Remove unnamed columns
# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# # Standardize column names
# df = df.rename(columns=lambda x: x.strip().replace(' ', '_').lower())

# # Convert 'Animal number' to string
# if 'animal_number' in df.columns:
#     df['animal_number'] = df['animal_number'].astype(str)

# # Convert date columns safely
# for date_col in ['arrival_date', 'injection_date', 'surgery_date', 'drop_out_date']:
#     if date_col in df.columns:
#         df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# # --------------------------
# # 5. Optional: Load raw data into staging table (preserve raw data)
# # --------------------------
# df.to_sql('raw_animals', engine, if_exists='replace', index=False)

# --------------------------
# 6. Optional: Verify loaded records
# --------------------------
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT COUNT(*) FROM raw_animals")).scalar()
#     print(f"Loaded {result} records into raw_animals.")