from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import ProductTypeCreate, ProductTypeOut
from app.cruds import product_type as product_type_crud

router = APIRouter(prefix="/product-types", tags=["Product Types"])


@router.post("/", response_model=ProductTypeOut)
async def create_product_type(
    product_type: ProductTypeCreate, session: AsyncSession = Depends(get_session)
):
    return await product_type_crud.create_product_type(session, product_type)


@router.get("/", response_model=List[ProductTypeOut])
async def get_product_types(session: AsyncSession = Depends(get_session)):
    return await product_type_crud.get_all_product_types(session)


@router.get("/{product_type_id}", response_model=ProductTypeOut)
async def get_product_type(
    product_type_id: int, session: AsyncSession = Depends(get_session)
):
    product_type = await product_type_crud.get_product_type_by_id(
        session, product_type_id
    )
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type


@router.put("/{product_type_id}", response_model=ProductTypeOut)
async def update_product_type(
    product_type_id: int,
    product_type: ProductTypeCreate,
    session: AsyncSession = Depends(get_session),
):
    db_type = await product_type_crud.update_product_type(
        session, product_type_id, product_type
    )
    if not db_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return db_type


@router.delete("/{product_type_id}")
async def delete_product_type(
    product_type_id: int, session: AsyncSession = Depends(get_session)
):
    db_type = await product_type_crud.delete_product_type(session, product_type_id)
    if not db_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return {"detail": "Product type deleted"}
