from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import datetime
from app.models.model import ProductStore, Product
from app.schemas.schemas import ProductStoreBase


async def get_all_product_store(session: AsyncSession):
    result = await session.execute(select(ProductStore))
    return result.scalars().all()


async def get_product_store_by_id(session: AsyncSession, product_store_id: int):
    result = await session.execute(
        select(ProductStore).where(ProductStore.product_store_id == product_store_id)
    )
    return result.scalar_one_or_none()


async def delete_product_store(session: AsyncSession, product_store_id: int):
    db_price = await get_product_store_by_id(session, product_store_id)
    if db_price:
        await session.delete(db_price)
        await session.commit()
    return db_price


async def assign_price(session: AsyncSession, price: ProductStoreBase):
    stmt = select(ProductStore).where(
        ProductStore.product_id == price.product_id,
        ProductStore.store_id == price.store_id,
    )
    result = await session.execute(stmt)
    db_price = result.scalar_one_or_none()

    registration_date = (
        price.registration_date if price.registration_date else datetime.date.today()
    )

    if db_price:
        db_price.price = price.price
        db_price.registration_date = registration_date
        await session.commit()
        await session.refresh(db_price)
        return db_price
    else:
        new_price = ProductStore(
            product_id=price.product_id,
            store_id=price.store_id,
            price=price.price,
            registration_date=registration_date,
        )
        session.add(new_price)
        await session.commit()
        await session.refresh(new_price)
        return new_price


async def get_products_by_store(session: AsyncSession, store_id: int):
    stmt = select(Product).join(ProductStore).where(ProductStore.store_id == store_id)
    result = await session.execute(stmt)
    return result.scalars().unique().all()
