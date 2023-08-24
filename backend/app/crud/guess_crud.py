import logging
from datetime import datetime

from app.models.game import Game
from app.models.guess import Guess
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def create_guess(db: Session, game_id: int, letter: str) -> Guess:
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
        now = datetime.now()
        if game:
            user_guess = Guess(
                game_id=game.id,
                guess_letter=letter,
                guess_created=now,
            )
            db.add(user_guess)
            db.commit()
            db.refresh(user_guess)
            return user_guess
        else:
            raise NoResultFound("Game not found for guess creation")
    except TypeError:
        raise TypeError("Game not found for guess creation")
    except Exception as error:
        logging.error(error)
        db.rollback()
        return None


def get_guesses_by_game_id(db: Session, game_id: int) -> Guess:
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
        if game:
            return game.guesses
        else:
            raise NoResultFound("Game not found for guesses retrieval")
    except Exception as error:
        logging.error(error)
        return []