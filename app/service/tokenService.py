from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM_JWT, REFRESH_TOKEN_EXPIRE_DAYS

class TokenService:
    def generate_tokens(self, user_id: int):
        return {
            "access": self.create_access_token(data={"sub": str(user_id)}),
            "refresh": self.create_refresh_token(data={"sub": str(user_id)})
        }
    
    def verify_refresh_token(self, refreshToken: str):
        payload = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM_JWT]
        )
        if payload.get("type") != "refresh":
                raise JWTError("Incorrect Type for refresh token")
        return payload
    
    def verify_access_token(self, accessToken: str):
        payload = jwt.decode(accessToken, SECRET_KEY, algorithms=[ALGORITHM_JWT])
        if payload.get("type") != "access":
            raise JWTError("Incorrect Type for access token")
        return payload

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM_JWT)

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM_JWT)