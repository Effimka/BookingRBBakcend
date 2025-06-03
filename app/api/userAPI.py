from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependency import get_db
from schemas.userShemas import UserCreate, UserOut
from crud.userCRUD import create_user, get_user_by_email


router = APIRouter()

@router.post("/register-common", response_model=UserOut)
async def create_user_api(user: UserCreate, db: AsyncSession  = Depends(get_db)):
    return await create_user(user, db)

@router.post("/login-common", response_model=UserOut)
async def login_user_api(user: UserCreate, db: AsyncSession  = Depends(get_db)):
    return await get_user_by_email(user, db)
