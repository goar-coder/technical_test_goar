from pydantic import BaseModel
from typing import List, Optional
import datetime


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityOut(CityBase):
    city_id: int

    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    name: str
    address: str
    opening_hours: datetime.time
    city_id: int


class StoreCreate(StoreBase):
    pass


class StoreOut(StoreBase):
    store_id: int

    class Config:
        orm_mode = True


class ProductTypeBase(BaseModel):
    name: str


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeOut(ProductTypeBase):
    product_type_id: int

    class Config:
        orm_mode = True


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandOut(BrandBase):
    brand_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    brand_id: int
    product_type_id: int
    name: str
    caloric_value: float
    saturated_fat_percentage: float
    sugar_percentage: float


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    product_id: int

    class Config:
        orm_mode = True


class ProductStoreBase(BaseModel):
    product_id: int
    store_id: int
    price: float


class ProductStoreCreate(ProductStoreBase):
    registration_date: Optional[datetime.date] = None


class ProductStoreOut(ProductStoreBase):
    product_store_id: int
    registration_date: datetime.date

    class Config:
        orm_mode = True
