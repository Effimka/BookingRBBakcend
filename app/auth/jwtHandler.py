from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM_JWT, REFRESH_TOKEN_EXPIRE_DAYS

def verify_refresh_token(refreshToken: str):
    try:
        payload = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM_JWT]
        )
        if payload.get("type") != "refresh":
             raise HTTPException(status_code=401, detail="Invalid token type")
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
def verify_access_token(accessToken: str):
    try:
        payload = jwt.decode(accessToken, SECRET_KEY, algorithms=[ALGORITHM_JWT])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM_JWT)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM_JWT)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM_JWT])
        return payload
    except JWTError:
        return None