from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import Product
from app.schemas.schemas import ProductCreate


async def create_product(session: AsyncSession, product: ProductCreate):
    new_product = Product(**product.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def get_all_products(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(session: AsyncSession, product_id: int):
    result = await session.execute(
        select(Product).where(Product.product_id == product_id)
    )
    return result.scalar_one_or_none()


async def update_product(
    session: AsyncSession, product_id: int, product: ProductCreate
):
    db_product = await get_product_by_id(session, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        await session.commit()
        await session.refresh(db_product)
    return db_product


async def delete_product(session: AsyncSession, product_id: int):
    db_product = await get_product_by_id(session, product_id)
    if db_product:
        await session.delete(db_product)
        await session.commit()
    return db_product
