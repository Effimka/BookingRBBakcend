from models.userModel import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

async def create_user(user: UserModel, db: AsyncSession):
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        return None
    except Exception as e:
        await db.rollback()
        return None

async def get_user_by_email(email, password, db: AsyncSession):
    stmt = select(UserModel).where(UserModel.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()    

async def get_user_by_id(user_id: int, db: AsyncSession):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()    
    

async def save_user(user: UserModel, db: AsyncSession):
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        await db.rollback()
        raise