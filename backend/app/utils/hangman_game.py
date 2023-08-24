import logging
from datetime import datetime

from app.crud.game_crud import get_game
from app.crud.guess_crud import create_guess
from app.models.game import Game
from random_word import RandomWords
from sqlalchemy.orm import Session


class Base:
    def __init__(self) -> None:
        self.game_word = ""
        self.word_set = "abcdefghijklmnopqrstuvwxyz"
        self.game_display = ""
        self.tries = 0
        self.game_blanks = 0
        self.max_tries = 7
        self.now = datetime.now()

    def get_random_word(self) -> str:
        try:
            random_word = RandomWords()
            self.game_word = random_word.get_random_word()
            return self.game_word
        except ConnectionError:
            logging.error(f"Can't connect RandomWords(): {error}")
            return None
        except Exception as error:
            logging.error(f"Can't get_random_word: {error}")
            return None

    def get_game_word_display(self) -> str:
        if self.game_word is None:
            raise ValueError("No game_word")
        try:
            self.game_display = ""
            for char in self.game_word:
                if char == " ":
                    self.game_display += " "
                else:
                    self.game_display += "_"
            return self.game_display
        except Exception as error:
            logging.error(f"Can't get_game_word_display: {error}")
            return None

    def get_game_word_blanks(self) -> int:
        if self.game_word is None:
            raise ValueError("No game_word")
        try:
            self.game_blanks = 0
            for char in self.game_word:
                if char != " ":
                    self.game_blanks += 1
            return self.game_blanks
        except Exception as error:
            logging.error(f"Can't get_game_word_blanks: {error}")
            return None

    def create_game(self, db: Session, account_id: int):
        self.get_random_word()
        self.get_game_word_display()
        self.get_game_word_blanks()
        try:
            game_data = Game(
                account_id=account_id,
                game_word=self.game_word,
                game_display=self.game_display,
                game_blanks=self.game_blanks,
                game_word_set=self.word_set,
                game_created=self.now,
            )
            db.add(game_data)
            db.commit()
            db.refresh(game_data)
            return game_data
        except Exception as error:
            db.rollback()
            logging.error(f"Can't create_game: {error}")
            return None


class Hangman(Base):
    def play_game(self, db: Session, game_id: int, letter: str):
        game_data = get_game(db, game_id)

        game_word = game_data.game_word
        game_display_list = list(game_data.game_display)
        game_blanks = game_data.game_blanks
        game_word_set = game_data.game_word_set
        game_tries = game_data.game_tries
        game_status = game_data.status

        guess = create_guess(db, game_id, letter)

        guessed_in_word = False

        for num, char in enumerate(game_word):
            if char == guess.guess_letter:
                guessed_in_word = True
                game_display_list[num] = letter
                game_blanks -= 1

        game_word_set = game_word_set.replace(letter, "")
        game_display = "".join(game_display_list)

        if guessed_in_word == False:
            game_tries += 1
            if game_tries == self.max_tries:
                game_status = "LOSS"

        if game_blanks == 0:
            game_status = "WIN"

        update_game_data = {
            "game_blanks": game_blanks,
            "game_display": game_display,
            "game_tries": game_tries,
            "game_word": game_word,
            "game_word_set": game_word_set,
            "status": game_status,
        }

        for key, value in update_game_data.items():
            setattr(game_data, key, value)
        db.commit()

        return game_data