from fastapi import Response
from datetime import timedelta
from config import REFRESH_TOKEN_EXPIRE_DAYS

def setResponseRefreshToken(response: Response, refreshToken: str):
    response.set_cookie(
        key="refreshToken",
        value=refreshToken,
        httponly=True,
        secure=False, # Only for local dev in production set True
        samesite="lax", # mb "none" if back and front will on diff domai
        path="/",
        max_age=int(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS).total_seconds())
    ) 