import datetime

from sqlalchemy import Column, DateTime, Integer, String, Numeric
from database import Base
from datetime import datetime

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(200), nullable=False)

    email = Column(String(200), unique=True, index=True, nullable=False)

    password = Column(String(255), nullable=False)

    role_id = Column(Integer, nullable=False)

    status_id = Column(Integer, default="Active")

    created_on = Column(DateTime, default=datetime.utcnow)

    last_login = Column(DateTime, nullable=True)


class FormData(Base):

    __tablename__ = "form_data"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Numeric)
    department = Column(String)