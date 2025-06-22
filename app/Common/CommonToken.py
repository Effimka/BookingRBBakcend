from fastapi import Response


def setResponseRefreshToken(response: Response, refreshToken: str):
    response.set_cookie(
        key="refreshToken",
        value=refreshToken,
        httponly=True,
        secure=False, # Only for local dev in production set True
        samesite="lax" # mb "none" if back and front will on diff domain
    ) 