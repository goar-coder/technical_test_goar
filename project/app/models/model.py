from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Time,
    Sequence,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class City(Base):
    __tablename__ = "city"

    city_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    stores = relationship("Store", back_populates="city")


class Store(Base):
    __tablename__ = "store"

    store_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    opening_hours = Column(Time, nullable=False)
    city_id = Column(Integer, ForeignKey("city.city_id"), nullable=False)

    __table_args__ = (UniqueConstraint("name", "city_id", name="unique_store_in_city"),)

    city = relationship("City", back_populates="stores")
    prices = relationship("ProductStore", back_populates="store")


class ProductType(Base):
    __tablename__ = "product_type"

    product_type_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    products = relationship("Product", back_populates="product_type")


class Brand(Base):
    __tablename__ = "brand"

    brand_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(
        Integer, ForeignKey("brand.brand_id", ondelete="CASCADE"), nullable=False
    )
    product_type_id = Column(
        Integer,
        ForeignKey("product_type.product_type_id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(100), nullable=False)
    caloric_value = Column(
        Integer,
        CheckConstraint("caloric_value >= 0", name="positive_caloric_value"),
        nullable=False,
    )
    saturated_fat_percentage = Column(
        Integer,
        CheckConstraint(
            "saturated_fat_percentage BETWEEN 0 AND 10000", name="fat_percentage_range"
        ),
        nullable=False,
    )
    sugar_percentage = Column(
        Integer,
        CheckConstraint(
            "sugar_percentage BETWEEN 0 AND 10000", name="sugar_percentage_range"
        ),
        nullable=False,
    )

    brand = relationship("Brand", back_populates="products")
    product_type = relationship("ProductType", back_populates="products")
    prices = relationship("ProductStore", back_populates="product")


class ProductStore(Base):
    __tablename__ = "product_store"

    product_store_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, ForeignKey("product.product_id", ondelete="CASCADE"), nullable=False
    )
    store_id = Column(
        Integer, ForeignKey("store.store_id", ondelete="CASCADE"), nullable=False
    )
    price = Column(
        Float(precision=2),
        CheckConstraint("price >= 0", name="positive_price"),
        nullable=False,
    )
    registration_date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="prices")
    store = relationship("Store", back_populates="prices")
