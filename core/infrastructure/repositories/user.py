from typing import Optional

from core.infrastructure.database import DatabaseConnector
from core.infrastructure.database.models import User

class UserRepository:
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector

    async def upsert_user(self, user: User) -> None:
        query = """
            INSERT INTO users (id, is_bot, first_name, last_name, username, language_code, is_premium)
            VALUES (:id, :is_bot, :first_name, :last_name, :username, :language_code, :is_premium)
            ON CONFLICT(id) DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                username = EXCLUDED.username,
                last_seen = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
        """
        await self.connector.execute(query, user.model_dump(exclude={'full_name', 'created_at'}))

    async def get_user(self, user_id: int) -> Optional[User]:
        row = await self.connector.fetch_one(
            "SELECT * FROM users WHERE id = :id", 
            {"id": user_id}
        )
        return User.model_validate(dict(row)) if row else None