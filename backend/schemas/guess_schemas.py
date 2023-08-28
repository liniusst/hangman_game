from datetime import datetime

from pydantic import BaseModel


class Guess(BaseModel):
    game_id: int
    guess_letter: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "game_id": 1,
                "guess_letter": "a",
            }
        }


class GuessResponse(BaseModel):
    id: int
    game_id: int
    guess_letter: str
    guess_created: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "game_id": 1,
                "guess_letter": "a",
                "guess_created": "2023-08-19T20:32:26.29675",
            }
        }
