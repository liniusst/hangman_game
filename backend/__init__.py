import sys
import os
from .database import Base
from .database import engine
from .router.router import api_router
from fastapi import FastAPI


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
