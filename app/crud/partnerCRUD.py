from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.partnerModel import Partner, AgentPartner
from schemas.partnerShemas import PartnerCreate, AgentPartnerOut, AgentPartnerLogin
from sqlalchemy import select
import traceback

async def create_partner_with_agent(db_partner : Partner, db_agent : AgentPartner, db: AsyncSession):
    try:

        db.add(db_partner)
        await db.flush() 

        db.add(db_agent)

        await db.commit()
        await db.refresh(db_agent)

        return db_agent.partner_id, AgentPartnerOut.model_validate(db_agent)

    except IntegrityError:
        await db.rollback()

    except Exception:
        traceback.print_exc() 
        await db.rollback()
    
async def get_partner_by_email(user: AgentPartnerLogin, db: AsyncSession):
        
    stmt = select(AgentPartner).where(AgentPartner.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    return existing_user.id, AgentPartnerOut.model_validate(existing_user)