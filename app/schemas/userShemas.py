from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    email: str
    viewname: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

class UserOutWithToken(BaseModel):
    userBaseData: UserOut
    accessToken: str

class UserUpdatePersonalData(BaseModel):
    display_name: Optional[str]
    email: str
    phone: Optional[str]
    passport_data: Optional[str] #TODO stucture