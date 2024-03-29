from typing import Dict

from logs.logger import logger
from models.account import Account
from models.game import Game
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def get_game(db: Session, game_id: int) -> Game:
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
    except NoResultFound:
        return None
    except Exception as error:
        logger.exception(error)
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
            logger.debug("Last 5 games returned")
            return games
        else:
            logger.error(NoResultFound)
            raise NoResultFound("User not found")
    except Exception as error:
        logger.exception(error)
        return []


def get_games_by_user_id(db: Session, user_id: int) -> list[Game]:
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            games = (
                db.query(Game)
                .filter(Game.account_id == user_id)
                .order_by(desc(Game.game_created))
                .all()
            )
            logger.debug("Games by user_id returned")
            return games
        else:
            logger.error(NoResultFound)
            raise NoResultFound("User not found")
    except Exception as error:
        logger.exception(error)
        return []


def get_user_games_stats(db: Session, user_id: int) -> Dict:
    win_games = []
    loss_games = []
    new_games = []
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            games = user.games
        else:
            logger.error(NoResultFound)
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
        logger.debug("Games stats returned")
        return stats
    except Exception as error:
        logger.error(error)
        return None
