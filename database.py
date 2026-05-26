import os 
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

#DATABASE_URL = "postgresql://uruk:123456@localhost/client_dashboard"
#DATABASE_URL = "postgresql://postgres:!39QHA&U-*/qPPf@db.ypyryqegoarpdeztpddy.supabase.co:5432/postgres"
#DATABASE_URL = "postgresql://postgres:!39QHA&U-*/qPPf@db.ypyryqegoarpdeztpddy.supabase.co:5432/postgres"

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL,pool_pre_ping=True, connect_args={ "sslmode": "require" })

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()