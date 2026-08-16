from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users_clients import UserClient
from src.schemas.users_clients import UserClientCreate

from .base import BaseRepository


class UserClientRepository(BaseRepository):
    entity_name = "user-client link"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_user_client(self, user_client: UserClientCreate) -> UserClient:
        new_user_client = UserClient(
            user_id=user_client.user_id,
            client_id=user_client.client_id,
            user_client_id=user_client.user_client_id,
        )
        self.session.add(new_user_client)
        await self._flush(operation="create")
        return new_user_client

    async def get_user_client(self, user_id: int, client_id: int) -> UserClient | None:
        return await self._get(UserClient, (user_id, client_id))

    async def delete_user_client(self, user_id: int, client_id: int) -> bool:
        user_client = await self.get_user_client(user_id, client_id)
        if user_client is None:
            return False
        await self._delete(user_client)
        return True
