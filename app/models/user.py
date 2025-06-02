from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "User"  
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    viewname = Column(String(30), nullable=True)
    phone_number = Column(String(30), nullable=True)
