from typing import Optional
from aiogram import types
from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    
    full_name: Optional[str] = None
    
    @classmethod
    def from_telegram(cls, user: types.User):
        return cls(
            id=user.id,
            is_bot=user.is_bot,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
            is_premium=bool(user.is_premium)
        )