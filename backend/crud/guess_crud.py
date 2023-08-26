from backend.logs.logger import logger
from datetime import datetime
from backend.models.game import Game
from backend.models.guess import Guess
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
            logger.error(NoResultFound)
            raise NoResultFound("Game not found for guess creation")
    except TypeError as error:
        logger.exception(error)
        raise TypeError("Game not found for guess creation")
    except Exception as error:
        logger.exception(error)
        db.rollback()
        return None


def get_guesses_by_game_id(db: Session, game_id: int) -> Guess:
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
        if game:
            return game.guesses
        else:
            logger.error(NoResultFound)
            raise NoResultFound("Game not found for guesses retrieval")
    except Exception as error:
        logger.exception(error)
        return []
