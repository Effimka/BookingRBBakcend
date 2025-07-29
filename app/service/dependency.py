from service.userService import UserService
from service.partnerService import PartnerService
from service.tokenService import TokenService
from service.interfaces.userServiceInterface import IUserService
from service.interfaces.partnerServiceInterface import IPartnerService
from fastapi import Depends

def get_token_service():
    return TokenService()

def get_user_service(token_service: TokenService = Depends(get_token_service)) -> IUserService:
    return UserService(token_service=token_service)

def get_partner_service(token_service: TokenService = Depends(get_token_service)) -> IPartnerService:
    return PartnerService(token_service=token_service)