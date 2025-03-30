from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import ProductCreate, ProductOut
from app.cruds import product as product_crud

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductOut)
async def create_product(
    product: ProductCreate, session: AsyncSession = Depends(get_session)
):
    return await product_crud.create_product(session, product)


@router.get("/", response_model=List[ProductOut])
async def get_products(session: AsyncSession = Depends(get_session)):
    return await product_crud.get_all_products(session)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await product_crud.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product: ProductCreate,
    session: AsyncSession = Depends(get_session),
):
    db_product = await product_crud.update_product(session, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    db_product = await product_crud.delete_product(session, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
