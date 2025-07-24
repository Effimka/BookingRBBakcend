from service.userService import UserService
from service.tokenService import TokenService
from service.interfaces.userServiceInterface import IUserService
from fastapi import Depends

def get_token_service():
    return TokenService()

def get_user_service(token_service: TokenService = Depends(get_token_service)) -> IUserService:
    return UserService(token_service=token_service)