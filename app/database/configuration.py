import os
#creating the configuration for the database, then a function that error checks it (try/finally)
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#load_dotenv()

#DATABASE_URI = os.getenv('DB_URI')
DATABASE_URI = "sqlite:///./sql_app.db"

engine = create_engine(
    DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()