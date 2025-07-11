from fastapi import APIRouter, Depends, Response, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencyDB import get_db
from schemas.userShemas import UserCreate, UserOutWithToken, UserUpdatePersonalData
from crud.userCRUD import create_user, get_user_by_email, update_user_personal_data
from auth.jwtHandler import create_access_token, create_refresh_token
from Common.CommonToken import setResponseRefreshToken
from auth.dependencyAuth import get_current_user

router = APIRouter()

@router.post("/register-common", response_model=UserOutWithToken)
async def create_user_api(user: UserCreate, response: Response, db: AsyncSession  = Depends(get_db)):
    userId, userOutData = await create_user(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return UserOutWithToken(userBaseData=userOutData, accessToken=accesToken)

@router.post("/login-common", response_model=UserOutWithToken)
async def login_user_api(user: UserCreate, response: Response, db: AsyncSession  = Depends(get_db)):
    userId, userOutData = await get_user_by_email(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return UserOutWithToken(userBaseData=userOutData, accessToken=accesToken)

@router.patch("/users/me/personal-data", response_model=UserUpdatePersonalData)
async def update_personal_data(personalData: UserUpdatePersonalData, db: AsyncSession = Depends(get_db),
                               current_user_id: int = Depends(get_current_user)):
    user = await update_user_personal_data(current_user_id, personalData.model_dump(exclude_unset=True), db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    return UserUpdatePersonalData(**{field: getattr(user, field) for field in UserUpdatePersonalData.model_fields})