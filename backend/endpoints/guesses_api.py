import backend.crud.game_crud as game_crud
import backend.crud.guess_crud as guess_crud
from backend.logs.logger import logger
from backend.database import get_db
from backend.schemas.guess_schemas import Guess
from backend.schemas.guess_schemas import GuessResponse
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create/", response_model=GuessResponse)
def create_guess(guess: Guess, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, guess.game_id)
    if db_game is None:
        logger.error("Game not found")
        raise HTTPException(status_code=404, detail="Game not found")
    return create_guess(db, game_id=guess.game_id, letter=guess.guess_letter)


@router.get("/game_guesses/{game_id}", response_model=list[GuessResponse])
def get_game_guesses(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id)
    if db_game is None:
        logger.error("Game not found")
        raise HTTPException(status_code=400, detail="Game not found")
    return guess_crud.get_guesses_by_game_id(db, db_game.id)
