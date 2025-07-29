from fastapi import APIRouter, Depends, Response, HTTPException
from service.tokenService import JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencyDB import get_db
from schemas.partnerShemas import PartnerCreate, AgentPartnerOutWhitToken, AgentPartnerLogin
from service.interfaces.partnerServiceInterface import IPartnerService
from Common.CommonToken import setResponseRefreshToken
from service.dependency import get_partner_service
import exception.exception as exception

router = APIRouter()

@router.post("/register/partner", response_model=AgentPartnerOutWhitToken)
async def create_partner_api(AgentPartner: PartnerCreate, response: Response, db: AsyncSession  = Depends(get_db), 
                             partner_service: IPartnerService = Depends(get_partner_service)):
    try:
        agentOutDataWithToken, refreshToken = await partner_service.create_partner(AgentPartner)
        setResponseRefreshToken(response, refreshToken)
        return agentOutDataWithToken
    except exception.PartnerAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error {str(e)}")





@router.post("/login/partner", response_model=AgentPartnerOutWhitToken)
async def login_partner_api(agent: AgentPartnerLogin, response: Response, db: AsyncSession  = Depends(get_db),
                            partner_service: IPartnerService = Depends(get_partner_service)):
    try:
        agentOutDataWithToken, refreshToken = await partner_service.login_partner(agent)
        setResponseRefreshToken(response, refreshToken)
        return agentOutDataWithToken
    except exception.PartnerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exception.PartnerPasswordIncorrectError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error {str(e)}")