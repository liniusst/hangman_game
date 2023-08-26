import logging
from typing import Optional
import backend.schemas.games_schemas as game_schemas
from backend.models.account import Account
from backend.models.game import Game
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def get_game(db: Session, game_id: int) -> Game:
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
    except NoResultFound:
        return None
    except Exception as error:
        logging.error(error)
        return None
    return game


def get_user_last_five_games(db: Session, user_id: int) -> list[Game]:
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            games = (
                db.query(Game)
                .filter(Game.account_id == user_id)
                .order_by(desc(Game.game_created))
                .limit(5)
                .all()
            )
            return games
        else:
            raise NoResultFound("User not found")
    except Exception as error:
        logging.error(error)
        return []


def get_games_by_user_id(db: Session, user_id: int) -> Account:
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            return user.games
        else:
            raise NoResultFound("User not found")
    except Exception as error:
        logging.error(error)
        return []


def get_user_games_stats(db: Session, user_id: int):
    win_games = []
    loss_games = []
    new_games = []
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            games = user.games
        else:
            raise NoResultFound("User not found")

        for game in games:
            if game.status == "WIN":
                win_games.append(game)
            if game.status == "LOSS":
                loss_games.append(game)
            if game.status == "NEW":
                new_games.append(game)

        stats = {
            "total_games": len(games),
            "total_win": len(win_games),
            "total_loss": len(loss_games),
            "total_new": len(new_games),
        }
        return stats

    except Exception as error:
        logging.error(error)
        return None


def update_game(
    db: Session, game_id: int, game: game_schemas.GameUpdate
) -> Optional[Game]:
    try:
        db_game = get_game(db, game_id)
        if db_game:
            game_data = game.model_dump(exclude_unset=True)
            for key, value in game_data.items():
                setattr(db_game, key, value)
            db.commit()
            return db_game
        else:
            raise NoResultFound("Game not found for update")
    except Exception as error:
        logging.error(error)
        db.rollback()
        return None
