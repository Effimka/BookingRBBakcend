from pydantic import BaseModel
from typing import List
from datetime import date

class Partner(BaseModel):
    phone_number: List[str]
    lawcode: int
    data_registration: date

    class Config:
        from_attributes = True

class AgentPartnerCreate(BaseModel):
    role_code: int
    email: str
    password: str
    lastname: str
    firstname: str

    class Config:
        from_attributes = True

class PartnerCreate(BaseModel):
    phone_number: list[str]
    lawcode: int
    agent_role_code: int
    email: str
    password: str
    last_name: str
    first_name: str
    data_registration: date
    
    class Config:
        from_attributes = True

class AgentPartnerOut(BaseModel):
    role_code: int
    email: str
    lastname: str
    firstname: str

    class Config:
        from_attributes = True 

class AgentPartnerOutWhitToken(BaseModel):
    agentPartnerBaseData: AgentPartnerOut
    accessToken: str

class AgentPartnerLogin(BaseModel):
    email: str
    password: str
    class Config:
        from_attributes = True


