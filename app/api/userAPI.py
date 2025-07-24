from fastapi import APIRouter, Depends, Response, HTTPException
from schemas.userShemas import UserIn, UserOutWithToken, UserUpdatePersonalData
from service.interfaces.userServiceInterface import IUserService
from service.tokenService import JWTError, ExpiredSignatureError
from Common.CommonToken import setResponseRefreshToken
from auth.dependencyAuth import get_userId_from_token
from sqlalchemy.ext.asyncio import AsyncSession
import exception.exception as exception
from db.dependencyDB import get_db
from service.dependency import get_user_service

router = APIRouter()

@router.post("/register/common", response_model=UserOutWithToken)
async def register_user(user: UserIn, response: Response, db: AsyncSession  = Depends(get_db), 
                        user_service: IUserService = Depends(get_user_service)):
    try:
        userOutDataWithToken, refreshToken = await user_service.create_user(user, db)
        setResponseRefreshToken(response, refreshToken)
        return userOutDataWithToken
    except exception.UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error {str(e)}")

@router.post("/login/common", response_model=UserOutWithToken)
async def login_user(user: UserIn, response: Response, db: AsyncSession  = Depends(get_db),
                     user_service: IUserService = Depends(get_user_service)):
    try:
        userOutDataWithToken, refreshToken = await user_service.login_user(user, db)
        setResponseRefreshToken(response, refreshToken)
        return userOutDataWithToken
    except exception.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exception.UserPasswordIncorrectError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error {str(e)}")

@router.patch("/users/me/personal-data", response_model=UserUpdatePersonalData)
async def update_personal_data(personalData: UserUpdatePersonalData, db: AsyncSession = Depends(get_db),
                               current_user_id: int = Depends(get_userId_from_token),
                               user_service: IUserService = Depends(get_user_service)):
    try:
        return await user_service.update_personal_data(current_user_id, personalData, db)
    except exception.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error {str(e)}")
        