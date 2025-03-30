from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import ProductType
from app.schemas.schemas import ProductTypeCreate


async def create_product_type(session: AsyncSession, product_type: ProductTypeCreate):
    new_type = ProductType(name=product_type.name)
    session.add(new_type)
    await session.commit()
    await session.refresh(new_type)
    return new_type


async def get_all_product_types(session: AsyncSession):
    result = await session.execute(select(ProductType))
    return result.scalars().all()


async def get_product_type_by_id(session: AsyncSession, product_type_id: int):
    result = await session.execute(
        select(ProductType).where(ProductType.product_type_id == product_type_id)
    )
    return result.scalar_one_or_none()


async def update_product_type(
    session: AsyncSession, product_type_id: int, product_type: ProductTypeCreate
):
    db_type = await get_product_type_by_id(session, product_type_id)
    if db_type:
        db_type.name = product_type.name
        await session.commit()
        await session.refresh(db_type)
    return db_type


async def delete_product_type(session: AsyncSession, product_type_id: int):
    db_type = await get_product_type_by_id(session, product_type_id)
    if db_type:
        await session.delete(db_type)
        await session.commit()
    return db_type
