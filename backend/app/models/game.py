from app.database import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    game_word = Column(String)
    game_tries = Column(Integer, default=0)
    game_blanks = Column(Integer, default=0)
    game_display = Column(String)
    game_word_set = Column(String, default="abcdefghijklmnopqrstuvwxyz")
    status = Column(String, default="NEW")
    game_created = Column(DateTime)

    account = relationship("Account", back_populates="games")
    guesses = relationship("Guess", back_populates="game")