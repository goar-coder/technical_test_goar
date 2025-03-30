from fastapi import FastAPI, HTTPException
from app.database import engine
from app.models.model import Base
from app.routes import city, store, product_type, brand, product, product_store
from app.config import DB_CONFIG


from app.load import load_data


app = FastAPI(title="FastAPI Project for the test of Locker in The City")

# Include routers
app.include_router(city.router)
app.include_router(store.router)
app.include_router(product_type.router)
app.include_router(brand.router)
app.include_router(product.router)
app.include_router(product_store.router)


@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    except Exception as e:
        print(f"Error during startup: {e}")
        raise


@app.post("/load_data")
async def load_data_endpoint():
    try:
        load_data(DB_CONFIG)
        return {"message": "Data loaded successfully"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
