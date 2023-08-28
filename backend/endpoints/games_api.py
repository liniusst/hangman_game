import crud.account_crud as account_crud
import crud.game_crud as game_crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from logs.logger import logger
from schemas.games_schemas import GameResponse, GameStatsResponse, GameUpdate
from schemas.guess_schemas import Guess
from sqlalchemy.orm import Session
from utils.hangman_game import Hangman

router = APIRouter()


@router.post("/create/{account_id}", response_model=GameResponse)
def create_game(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Acount not found")
    hang = Hangman()
    logger.info("create_game endpoint returned")
    return hang.create_game(db, db_account.id)


@router.get("/game_data/{game_id}", response_model=GameResponse)
def get_game_by_game_id(game_id: int, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id)
    if db_game is None:
        logger.error("Game not found")
        raise HTTPException(status_code=404, detail="Game not found")
    logger.info("get_game_by_game_id endpoint returned")
    return db_game


@router.get("/{account_id}", response_model=list[GameResponse])
def get_user_games(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Acount not found")
    logger.info("get_user_games endpoint returned")
    return game_crud.get_games_by_user_id(db, db_account.id)


@router.get("/stats/{account_id}", response_model=GameStatsResponse)
def get_user_games_stats(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Acount not found")
    logger.info("get_user_games_stats endpoint returned")
    return game_crud.get_user_games_stats(db, db_account.id)


@router.get("/stats/lasts/{account_id}", response_model=list[GameResponse])
def get_user_last_five_games(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Acount not found")
    logger.info("get_user_last_five_games endpoint returned")
    return game_crud.get_user_last_five_games(db, db_account.id)


@router.post("/play/{game_id}", response_model=GameUpdate)
def play_game(guess: Guess, db: Session = Depends(get_db)):
    hang = Hangman()
    set_play_game = hang.play_game(db, game_id=guess.game_id, letter=guess.guess_letter)
    if set_play_game is None:
        logger.error("Can't start new game")
        raise HTTPException(status_code=400, detail="Can't start new game")
    return set_play_game


@router.patch("/update/{game_id}", response_model=GameUpdate)
def update_game(game_id: int, game: GameUpdate, db: Session = Depends(get_db)):
    db_game = game_crud.get_game(db, game_id)
    if db_game is None:
        logger.error("Game not found")
        raise HTTPException(status_code=404, detail="Game not found")
    logger.info("update_game endpoint returned")
    return update_game(db, db_game.id, game)
