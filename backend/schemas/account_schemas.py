from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class AccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "destroyeris3000",
                "email": "destroyer@gmail.com",
                "password": "d3str03r",
            }
        }


class AccountResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_active: bool
    created: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "destroyeris3000",
                "email": "destroyer@gmail.com",
                "password": "d3str03r",
                "is_active": True,
                "created": "2023-08-19T20:32:26.29675",
            }
        }


class AccountUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None