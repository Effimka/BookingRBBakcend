from fastapi import HTTPException, APIRouter, Request
from auth.jwtHandler import create_access_token, verify_refresh_token

router = APIRouter()

@router.post("/refresh-token")
async def refresh_token_api(request: Request):
    try:
        refreshToken = request.cookies.get("refreshToken")
        payload = verify_refresh_token(refreshToken)  
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token. Need ")