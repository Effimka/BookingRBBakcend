from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencyDB import get_db
from schemas.partnerShemas import PartnerCreate, AgentPartnerOutWhitToken, AgentPartnerLogin
from crud.partnerCRUD import create_partner_with_agent, get_partner_by_email
from auth.jwtHandler import create_access_token, create_refresh_token
from Common.CommonToken import setResponseRefreshToken

router = APIRouter()

@router.post("/register-partner", response_model=AgentPartnerOutWhitToken)
async def create_partner_api(user: PartnerCreate, response: Response, db: AsyncSession  = Depends(get_db)):
    print(user)
    userId, userOutData = await create_partner_with_agent(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return AgentPartnerOutWhitToken(userBaseData=userOutData, accessToken=accesToken)

@router.post("/login-partner", response_model=AgentPartnerOutWhitToken)
async def login_partner_api(user: AgentPartnerLogin, response: Response, db: AsyncSession  = Depends(get_db)):
    print(user)
    userId, userOutData = await get_partner_by_email(user, db)
    accesToken = create_access_token(data={"sub":str(userId)})
    refreshToken = create_refresh_token(data={"sub":str(userId)})
    setResponseRefreshToken(response, refreshToken)
    return AgentPartnerOutWhitToken(userBaseData=userOutData, accessToken=accesToken)