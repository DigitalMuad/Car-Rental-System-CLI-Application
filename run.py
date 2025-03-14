from database.session import engine, Base

def create_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    print("Running script...")
    create_database()
    print("Database created successfully!")