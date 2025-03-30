from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import ProductStoreCreate, ProductStoreOut, ProductOut
from app.cruds import product_store as product_store_crud

router = APIRouter(prefix="/product_store", tags=["Product Store"])


@router.get("/", response_model=List[ProductStoreOut])
async def get_all_product_store(session: AsyncSession = Depends(get_session)):
    return await product_store_crud.get_all_product_store(session)


@router.get("/{product_store_id}", response_model=ProductStoreOut)
async def get_product_store(
    product_store_id: int, session: AsyncSession = Depends(get_session)
):
    product_store = await product_store_crud.get_product_store_by_id(
        session, product_store_id
    )
    if not product_store:
        raise HTTPException(status_code=404, detail="Price not found")
    return product_store


@router.delete("/{product_store_id}")
async def delete_product_store(
    product_store_id: int, session: AsyncSession = Depends(get_session)
):
    product_store = await product_store_crud.delete_product_store(
        session, product_store_id
    )
    if not product_store:
        raise HTTPException(status_code=404, detail="Price not found")
    return {"detail": "Price deleted"}


@router.post(
    "/assign-price/",
    response_model=ProductStoreOut,
    description=(
        "When assigning prices to a product in a store, if the product doesn't exist in the store, "
        "it's created, and if it does, the price is updated. If the registration_date field is passed, "
        "this value is taken as the product's registration date in the store; otherwise, the current date is used."
    ),
)
async def assign_price(
    product_store: ProductStoreCreate, session: AsyncSession = Depends(get_session)
):
    try:
        return await product_store_crud.assign_price(session, product_store)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stores/{store_id}/products/", response_model=List[ProductOut])
async def get_products_by_store(
    store_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        return await product_store_crud.get_products_by_store(session, store_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
