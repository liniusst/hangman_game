from datetime import datetime
from typing import Literal
from typing import Optional

from pydantic import BaseModel


class GameUpdate(BaseModel):
    game_word: Optional[str]
    game_tries: Optional[int]
    game_blanks: Optional[int]
    game_display: Optional[str]
    game_word_set: Optional[str]
    status: Optional[Literal["NEW", "WIN", "LOSS"]]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "game_word": "fantastico",
                "game_tries": 7,
                "game_blanks": 3,
                "game_display": "___",
                "game_word_set": "abcc",
                "status": "WIN",
            }
        }


class GameResponse(BaseModel):
    id: int
    account_id: int
    game_word: str
    game_tries: int
    game_blanks: int
    game_display: str
    game_word_set: str
    status: str
    game_created: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "account_id": 1,
                "game_word": "fantastico",
                "game_tries": 7,
                "game_blanks": 3,
                "game_display": "___",
                "game_word_set": "abc",
                "status": "WIN",
                "game_created": "2023-08-19T20:32:26.29675",
            }
        }


class GameUpdateResponse(BaseModel):
    id: int
    game_word: str
    game_tries: int
    game_blanks: int
    game_display: str
    game_word_set: str
    status: Literal["NEW", "WIN", "LOSS"]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "game_word": "fantastico",
                "game_tries": 7,
                "game_blanks": 3,
                "game_display": "___",
                "game_word_set": "abcc",
                "status": "WIN",
            }
        }


class GameStatsResponse(BaseModel):
    total_games: int
    total_win: int
    total_loss: int
    total_new: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_games": 35,
                "total_win": 10,
                "total_loss": 20,
                "total_new": 5,
            }
        }