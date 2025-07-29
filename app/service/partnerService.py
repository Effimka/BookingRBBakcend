from service.interfaces.partnerServiceInterface import IPartnerService
from service.tokenService import TokenService
from crud.partnerCRUD import create_partner_with_agent, get_partner_by_email
from schemas.partnerShemas import AgentPartnerOut, AgentPartnerOutWhitToken, AgentPartnerLogin, PartnerCreate
from sqlalchemy.ext.asyncio import AsyncSession
import exception.exception as exception

from models.partnerModel import Partner, AgentPartner

class PartnerService(IPartnerService):

    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def create_partner(self, partner_data: PartnerCreate, db: AsyncSession):
        db_partner = Partner(
            phone_number=partner_data.phone_number,
            lawcode=partner_data.lawcode,
            data_registration=partner_data.data_registration
        )
        db_agent = AgentPartner(
            partner_id=db_partner.id,
            role_code=partner_data.agent_role_code,
            email=partner_data.email,
            password=partner_data.password, 
            lastname=partner_data.last_name,
            firstname=partner_data.first_name
        )
        dbAgentPartner= await create_partner_with_agent(db_partner, db_agent, db)
        if not dbAgentPartner:
            raise exception.UserAlreadyExistsError("This email already exist")
        tokens = self.token_service.generate_tokens(dbAgentPartner.id)
        return AgentPartnerOutWhitToken(agentPartnerBaseData=AgentPartnerOut.model_validate(dbAgentPartner), accessToken=tokens["access"]), tokens["refresh"]

    async def login_agent(self, agent: AgentPartnerLogin, db: AsyncSession):
        dbAgent = await get_partner_by_email(agent.email, agent.password, db)
        if not dbAgent:
            raise exception.PartnerNotFoundError(f"User not found")
        if agent.password != agent.password:
            raise exception.PartnerPasswordIncorrectError("Incorrect password")
        tokens = self.token_service.generate_tokens(dbAgent.id)
        return AgentPartnerOutWhitToken(agentPartnerBaseData=AgentPartnerOut.model_validate(dbAgent), accessToken=tokens["access"]), tokens["refresh"]