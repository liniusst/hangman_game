from endpoints import accounts_api, games_api, guesses_api
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(accounts_api.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(games_api.router, prefix="/games", tags=["games"])
api_router.include_router(guesses_api.router, prefix="/guesses", tags=["guesses"])
