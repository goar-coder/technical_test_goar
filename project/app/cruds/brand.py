from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import Brand
from app.schemas.schemas import BrandCreate


async def create_brand(session: AsyncSession, brand: BrandCreate):
    new_brand = Brand(name=brand.name)
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)
    return new_brand


async def get_all_brands(session: AsyncSession):
    result = await session.execute(select(Brand))
    return result.scalars().all()


async def get_brand_by_id(session: AsyncSession, brand_id: int):
    result = await session.execute(select(Brand).where(Brand.brand_id == brand_id))
    return result.scalar_one_or_none()


async def update_brand(session: AsyncSession, brand_id: int, brand: BrandCreate):
    db_brand = await get_brand_by_id(session, brand_id)
    if db_brand:
        db_brand.name = brand.name
        await session.commit()
        await session.refresh(db_brand)
    return db_brand


async def delete_brand(session: AsyncSession, brand_id: int):
    db_brand = await get_brand_by_id(session, brand_id)
    if db_brand:
        await session.delete(db_brand)
        await session.commit()
    return db_brand
