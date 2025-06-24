from sqlalchemy import Column, Integer, SmallInteger, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Partner(Base):
    __tablename__ = "Partner"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(ARRAY(String(30)), nullable=False)
    lawcode = Column(SmallInteger, nullable=False)
    data_registration = Column(Date, nullable=False)

class AgentPartner(Base):
    __tablename__ = "AgentPartner"

    partner_id = Column(Integer, ForeignKey("Partner.id"), primary_key=True)
    role_code = Column(SmallInteger, nullable=False)
    email = Column(String(100, collation="C"), unique=True, nullable=False)
    password = Column(String(30, collation="C"), nullable=False)
    lastname = Column(String(30, collation="C"), nullable=False)
    firstname = Column(String(30, collation="C"), nullable=False)