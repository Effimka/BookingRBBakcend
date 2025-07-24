from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.partnerModel import Partner, AgentPartner
from schemas.partnerShemas import PartnerCreate, AgentPartnerOut, AgentPartnerLogin
from sqlalchemy import select
import traceback

async def create_partner_with_agent(partner_data: PartnerCreate, db: AsyncSession):
    try:
        db_partner = Partner(
            phone_number=partner_data.phone_number,
            lawcode=partner_data.lawcode,
            data_registration=partner_data.data_registration
        )
        db.add(db_partner)
        await db.flush() 

        db_agent = AgentPartner(
            partner_id=db_partner.id,
            role_code=partner_data.agent_role_code,
            email=partner_data.email,
            password=partner_data.password, 
            lastname=partner_data.last_name,
            firstname=partner_data.first_name
        )
        db.add(db_agent)

        await db.commit()
        await db.refresh(db_agent)

        return db_agent.partner_id, AgentPartnerOut.model_validate(db_agent)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists or other constraint failed"
        )
    except Exception:
        traceback.print_exc() 
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unknown error during partner creation"
        )
    
async def get_user_by_email(user: AgentPartnerLogin, db: AsyncSession):
    try:
        print("existing_user try to get from db")
        print(user)

        stmt = select(AgentPartner).where(AgentPartner.email == user.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user.password != user.password:
            raise HTTPException(
                status_code=404,
                detail="User not found or incorrect password"
            )
        
        return existing_user.id, AgentPartnerOut.model_validate(existing_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error when searching for a user"
        )