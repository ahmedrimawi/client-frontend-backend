from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)


class FormData(Base):

    __tablename__ = "form_data"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Numeric)
    department = Column(String)