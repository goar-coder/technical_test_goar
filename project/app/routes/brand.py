from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import BrandCreate, BrandOut
from app.cruds import brand as brand_crud

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post("/", response_model=BrandOut)
async def create_brand(
    brand: BrandCreate, session: AsyncSession = Depends(get_session)
):
    return await brand_crud.create_brand(session, brand)


@router.get("/", response_model=List[BrandOut])
async def get_brands(session: AsyncSession = Depends(get_session)):
    return await brand_crud.get_all_brands(session)


@router.get("/{brand_id}", response_model=BrandOut)
async def get_brand(brand_id: int, session: AsyncSession = Depends(get_session)):
    brand = await brand_crud.get_brand_by_id(session, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.put("/{brand_id}", response_model=BrandOut)
async def update_brand(
    brand_id: int, brand: BrandCreate, session: AsyncSession = Depends(get_session)
):
    db_brand = await brand_crud.update_brand(session, brand_id, brand)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand


@router.delete("/{brand_id}")
async def delete_brand(brand_id: int, session: AsyncSession = Depends(get_session)):
    db_brand = await brand_crud.delete_brand(session, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"detail": "Brand deleted"}
