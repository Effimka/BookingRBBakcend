from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: str
    viewname: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True