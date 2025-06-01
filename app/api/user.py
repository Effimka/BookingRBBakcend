from fastapi import APIRouter
from schemas.userShemas import UserCreate, UserOut

router = APIRouter()

@router.post("/api/auth/register", response_model=UserOut)
async def create_user_api(user: UserCreate):
    print(f"User comming email = {user.email} pass = {user.password}")