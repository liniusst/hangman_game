import backend.crud.account_crud as account_crud
import backend.crud.game_crud as game_crud
from backend.database import get_db
from backend.schemas.games_schemas import GameStatsResponse
from backend.schemas.games_schemas import GameResponse
from backend.schemas.games_schemas import GameUpdate
from backend.schemas.guess_schemas import Guess
from backend.utils.hangman_game import Hangman
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create/{account_id}", response_model=GameResponse)
def create_game(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Acount not found")
    hang = Hangman()
    return hang.create_game(db, db_account.id)


@router.get("/game_data/{game_id}", response_model=GameResponse)
def get_game_by_game_id(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@router.get("/{account_id}", response_model=list[GameResponse])
def get_user_games(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Acount not found")
    return game_crud.get_games_by_user_id(db, db_account.id)


@router.get("/stats/{account_id}", response_model=GameStatsResponse)
def get_user_games_stats(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Acount not found")
    return game_crud.get_user_games_stats(db, db_account.id)


@router.get("/stats/lasts/{account_id}", response_model=list[GameResponse])
def get_user_last_five_games(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Acount not found")
    return game_crud.get_user_last_five_games(db, db_account.id)


@router.post("/play/{game_id}", response_model=GameUpdate)
def play_game(guess: Guess, db: Session = Depends(get_db)):
    hang = Hangman()
    set_play_game = hang.play_game(db, game_id=guess.game_id, letter=guess.guess_letter)
    if set_play_game is None:
        raise HTTPException(status_code=400, detail="Can't start new game")
    return set_play_game


@router.patch("/update/{game_id}", response_model=GameUpdate)
def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return update_game(db, db_game.id, game)
