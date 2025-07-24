from service.interfaces.userServiceInterface import IUserService
from service.tokenService import TokenService
from crud.userCRUD import create_user, get_user_by_email, save_user, get_user_by_id
from schemas.userShemas import UserIn, UserOut, UserOutWithToken, UserUpdatePersonalData
from sqlalchemy.ext.asyncio import AsyncSession
import exception.exception as exception

from models.userModel import UserModel



class UserService(IUserService):

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def create_user(self, user: UserIn, db: AsyncSession):
        user = UserModel(email=user.email, password=user.password)
        dbUser= await create_user(user, db)
        if not dbUser:
            raise exception.UserAlreadyExistsError("This email already exist")
        tokens = self.token_service.generate_tokens(dbUser.id)
        return UserOutWithToken(userBaseData=UserOut.model_validate(dbUser), accessToken=tokens["access"]), tokens["refresh"]

    async def login_user(self, user: UserIn, db: AsyncSession):
        dbUser = await get_user_by_email(user.email, user.password, db)
        if not dbUser:
            raise exception.UserNotFoundError(f"User not found")
        if dbUser.password != user.password:
            raise exception.UserPasswordIncorrectError("Incorrect password")
        tokens = self.token_service.generate_tokens(dbUser.id)
        return UserOutWithToken(userBaseData=UserOut.model_validate(dbUser), accessToken=tokens["access"]), tokens["refresh"]

    async def update_personal_data(self, user_id: int, data: UserUpdatePersonalData, db: AsyncSession):
        dbUser = await get_user_by_id(user_id, db)
        if not dbUser:
            raise exception.UserNotFoundError(f"User not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            if hasattr(dbUser, key) and value is not None and value != "":
                setattr(dbUser, key, value)
        updated_user = await save_user(dbUser, db)
        return UserUpdatePersonalData(**{field: getattr(updated_user, field) for field in UserUpdatePersonalData.model_fields})