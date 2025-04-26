from fastsecforge.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_db():
    if settings.DATABASE_TYPE == "sql":
        engine = create_engine(
            settings.DATABASE_URL, 
            connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
    else:
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client[settings.DATABASE_NAME]
    
    try:
        yield db
    finally:
        if settings.DATABASE_TYPE == "sql":
            db.close()