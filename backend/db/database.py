from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings
# from backend.core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # so models can inherit from base clase

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
