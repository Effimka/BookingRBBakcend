from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.dependency import get_db
from schemas.userShemas import UserCreate, UserOut
from models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def create_user_api(user: UserCreate):
    print(f"User comming email = {user.email} pass = {user.password}")
    return {"id": 1, "name": "tix", "email" : user.email}

@router.post("/login", response_model=UserOut)
async def login_user_api(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found placiPlaci")
    if user.password != existing_user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return existing_user
