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

    status_id = Column(Integer, default=1)

    created_on = Column(DateTime, default=datetime.utcnow)

    last_login = Column(DateTime, nullable=True)


class UserStatus(Base):

    __tablename__ = "user_statuses"

    id = Column(Integer, primary_key=True)
    status_name = Column(String)

class Roles(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(String)


class FormData(Base):

    __tablename__ = "form_data"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Numeric)
    department = Column(String)