from abc import ABC, abstractmethod
from schemas.partnerShemas import PartnerCreate, AgentPartnerOutWhitToken, AgentPartnerLogin
from sqlalchemy.ext.asyncio import AsyncSession

class IPartnerService(ABC):
    @abstractmethod
    async def create_partner(self, partner_data: PartnerCreate, db: AsyncSession) -> AgentPartnerOutWhitToken:
        pass

    @abstractmethod
    async def login_partner(self, user_in: AgentPartnerLogin, db: AsyncSession) -> AgentPartnerOutWhitToken:
        pass
