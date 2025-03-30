from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import CityCreate, CityOut
from app.cruds import city as city_crud

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityOut)
async def create_city(city: CityCreate, session: AsyncSession = Depends(get_session)):
    return await city_crud.create_city(session, city)


@router.get("/", response_model=List[CityOut])
async def get_cities(session: AsyncSession = Depends(get_session)):
    return await city_crud.get_all_cities(session)


@router.get("/{city_id}", response_model=CityOut)
async def get_city(city_id: int, session: AsyncSession = Depends(get_session)):
    city = await city_crud.get_city_by_id(session, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityOut)
async def update_city(
    city_id: int, city: CityCreate, session: AsyncSession = Depends(get_session)
):
    db_city = await city_crud.update_city(session, city_id, city)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}")
async def delete_city(city_id: int, session: AsyncSession = Depends(get_session)):
    db_city = await city_crud.delete_city(session, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted"}
