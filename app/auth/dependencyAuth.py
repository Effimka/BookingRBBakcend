from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwtHandler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    userId = payload.get("sub")
    if not userId:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return int(userId)