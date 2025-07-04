from schemas.partnerShemas import PartnerCreate, AgentPartnerOut
from models.partnerModel import Partner, AgentPartner
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select

async def create_partner(partner: PartnerCreate, db: AsyncSession):
    try:
        db_partner = 