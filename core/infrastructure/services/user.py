from core.infrastructure.repositories import UserRepository
from core.infrastructure.database.models import User

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: User):
        await self.repository.upsert_user(user_data)