from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import Store, Product, ProductStore
from app.schemas.schemas import StoreCreate


async def create_store(session: AsyncSession, store: StoreCreate):
    new_store = Store(**store.dict())
    session.add(new_store)
    await session.commit()
    await session.refresh(new_store)
    return new_store


async def get_all_stores(session: AsyncSession):
    result = await session.execute(select(Store))
    return result.scalars().all()


async def get_store_by_id(session: AsyncSession, store_id: int):
    result = await session.execute(select(Store).where(Store.store_id == store_id))
    return result.scalar_one_or_none()


async def update_store(session: AsyncSession, store_id: int, store: StoreCreate):
    db_store = await get_store_by_id(session, store_id)
    if db_store:
        for key, value in store.dict().items():
            setattr(db_store, key, value)
        await session.commit()
        await session.refresh(db_store)
    return db_store


async def delete_store(session: AsyncSession, store_id: int):
    db_store = await get_store_by_id(session, store_id)
    if db_store:
        await session.delete(db_store)
        await session.commit()
    return db_store


async def get_products_by_store(session: AsyncSession, store_id: int):
    stmt = select(Product).join(ProductStore).where(ProductStore.store_id == store_id)
    result = await session.execute(stmt)
    return result.scalars().unique().all()
