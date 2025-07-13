from schemas.userShemas import UserCreate, UserOut
from models.userModel import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select

async def create_user(user: UserCreate, db: AsyncSession):
    try:
        db_user = UserModel(email=user.email, password=user.password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user.id, UserOut.model_validate(db_user)
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This email already exist"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unknown error"
        )

async def get_user_by_email(user: UserCreate, db: AsyncSession):
    try:
        stmt = select(UserModel).where(UserModel.email == user.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user.password != user.password:
            raise HTTPException(
                status_code=404,
                detail="User not found or incorrect password"
            )
        
        return existing_user.id, UserOut.model_validate(existing_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error when searching for a user"
        )
    
async def update_user_personal_data(userId: int, data: dict, db: AsyncSession):
    try:
        stmt = select(UserModel).where(UserModel.id == userId)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None
        for key, value in data.items():
            if hasattr(user, key) and value is not None and value is not "":
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        
        return user
    except Exception as e:
        await db.rollback()
        #TODO add logger
        return None