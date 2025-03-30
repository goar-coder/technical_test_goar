from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.model import City
from app.schemas.schemas import CityCreate


async def create_city(session: AsyncSession, city: CityCreate):
    new_city = City(name=city.name)
    session.add(new_city)
    await session.commit()
    await session.refresh(new_city)
    return new_city


async def get_all_cities(session: AsyncSession):
    result = await session.execute(select(City))
    return result.scalars().all()


async def get_city_by_id(session: AsyncSession, city_id: int):
    result = await session.execute(select(City).where(City.city_id == city_id))
    return result.scalar_one_or_none()


async def update_city(session: AsyncSession, city_id: int, city: CityCreate):
    db_city = await get_city_by_id(session, city_id)
    if db_city:
        db_city.name = city.name
        await session.commit()
        await session.refresh(db_city)
    return db_city


async def delete_city(session: AsyncSession, city_id: int):
    db_city = await get_city_by_id(session, city_id)
    if db_city:
        await session.delete(db_city)
        await session.commit()
    return db_city
