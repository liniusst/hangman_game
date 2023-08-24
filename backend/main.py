from app.database import Base
from app.database import engine
from app.router.router import api_router
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")