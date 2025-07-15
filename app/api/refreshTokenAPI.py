from fastapi import HTTPException, APIRouter, Request, Depends
from service.dependency import get_token_service
from service.tokenService import TokenService, JWTError, ExpiredSignatureError

router = APIRouter()

@router.post("/auth/token/refresh")
async def refresh_token_api(request: Request, token_service: TokenService = Depends(get_token_service)):
    try:
        refreshToken = request.cookies.get("refreshToken")
        payload = token_service.verify_refresh_token(refreshToken)  
        new_access_token = token_service.create_access_token(data={"sub": payload["sub"]})
        return {"access_token": new_access_token}
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")