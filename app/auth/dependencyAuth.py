from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from service.dependency import get_token_service
from service.tokenService import TokenService, JWTError, ExpiredSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_userId_from_token(token: str = Depends(oauth2_scheme), token_service: TokenService = Depends(get_token_service)):
    try:
        payload = token_service.verify_access_token(token)
        userId = payload.get("sub")
        if not userId:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return int(userId)
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")