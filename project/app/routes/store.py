from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.schemas.schemas import StoreCreate, StoreOut, ProductOut
from app.cruds import store as store_crud

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/", response_model=StoreOut)
async def create_store(
    store: StoreCreate, session: AsyncSession = Depends(get_session)
):
    return await store_crud.create_store(session, store)


@router.get("/", response_model=List[StoreOut])
async def get_stores(session: AsyncSession = Depends(get_session)):
    return await store_crud.get_all_stores(session)


@router.get("/{store_id}", response_model=StoreOut)
async def get_store(store_id: int, session: AsyncSession = Depends(get_session)):
    store = await store_crud.get_store_by_id(session, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=StoreOut)
async def update_store(
    store_id: int, store: StoreCreate, session: AsyncSession = Depends(get_session)
):
    db_store = await store_crud.update_store(session, store_id, store)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.delete("/{store_id}")
async def delete_store(store_id: int, session: AsyncSession = Depends(get_session)):
    db_store = await store_crud.delete_store(session, store_id)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"detail": "Store deleted"}


@router.get("/{store_id}/products/", response_model=List[ProductOut])
async def get_products_by_store(
    store_id: int, session: AsyncSession = Depends(get_session)
):
    store = await store_crud.get_store_by_id(session, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return await store_crud.get_products_by_store(session, store_id)
