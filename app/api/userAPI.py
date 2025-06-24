from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencyDB import get_db
from schemas.userShemas import UserCreate, UserOutWithToken
from crud.userCRUD import create_user, get_user_by_email
from auth.jwtHandler import create_access_token, create_refresh_token
from Common.CommonToken import setResponseRefreshToken

router = APIRouter()

@router.post("/register-common", response_model=UserOutWithToken)
async def create_user_api(user: UserCreate, response: Response, db: AsyncSession  = Depends(get_db)):
    userId, userOutData = await create_user(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return UserOutWithToken(userOutData, accesToken)

@router.post("/login-common", response_model=UserOutWithToken)
async def login_user_api(user: UserCreate, response: Response, db: AsyncSession  = Depends(get_db)):
    userId, userOutData = await get_user_by_email(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return UserOutWithToken(userOutData, accesToken)