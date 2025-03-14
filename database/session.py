from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

# Import models to ensure they are registered with Base
from models.car import Car
from models.customer import Customer
from models.rental import Rental

# SQLite database file
DATABASE_URL = "sqlite:///car_rental.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()