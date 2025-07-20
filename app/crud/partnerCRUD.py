from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.partnerModel import Partner, AgentPartner
from schemas.partnerShemas import PartnerCreate, AgentPartnerOut

async def create_partner_with_agent(partner_data: PartnerCreate, db: AsyncSession):
    try:
        db_partner = Partner(
            phone_number=partner_data.phone_number,
            lawcode=partner_data.lawcode,
            data_registration=partner_data.data_registration
        )
        db.add(db_partner)
        await db.flush() 

        agent = partner_data.agentPartnerCreateBaseData
        db_agent = AgentPartner(
            partner_id=db_partner.id,
            role_code=agent.role_code,
            email=agent.email,
            password=agent.password, 
            lastname=agent.lastname,
            firstname=agent.firstname
        )
        db.add(db_agent)

        await db.commit()
        await db.refresh(db_agent)

        return AgentPartnerOut.model_validate(db_agent)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists or other constraint failed"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unknown error during partner creation"
        )