from abc import ABC, abstractmethod
from schemas.userShemas import UserIn, UserOut, UserOutWithToken, UserUpdatePersonalData
from sqlalchemy.ext.asyncio import AsyncSession

class IUserService(ABC):
    @abstractmethod
    async def create_user(self, user_in: UserIn, db: AsyncSession) -> UserOutWithToken:
        pass

    @abstractmethod
    async def login_user(self, user_in: UserIn, db: AsyncSession) -> UserOutWithToken:
        pass

    @abstractmethod
    async def update_personal_data(self, user_id: int, data: UserUpdatePersonalData, db: AsyncSession) -> UserUpdatePersonalData:
        pass