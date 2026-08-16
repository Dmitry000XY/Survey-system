from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.clients import Client
from src.schemas.clients import ClientInDB, ClientUpdate

from .base import BaseRepository


class ClientRepository(BaseRepository):
    entity_name = "client"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_client(self, client: ClientInDB) -> Client:
        new_client = Client(
            client_name=client.client_name,
            api_key_hash=client.api_key_hash,
        )
        self.session.add(new_client)
        await self._flush(operation="create")
        return new_client

    async def get_all_clients(self) -> list[Client]:
        query = select(Client)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_client(self, client_id: int) -> Client | None:
        return await self._get(Client, client_id)

    async def get_client_by_name(self, client_name: str) -> Client | None:
        query = select(Client).where(Client.client_name == client_name)
        result = await self._execute(query, operation="read")
        return result.scalars().first()

    async def get_client_by_api_key_hash(self, api_key_hash: str) -> Client | None:
        query = select(Client).where(Client.api_key_hash == api_key_hash)
        result = await self._execute(query, operation="read")
        return result.scalars().first()

    async def update_client(self, client_id: int, new_data: ClientUpdate) -> Client | None:
        values = new_data.model_dump(exclude_unset=True, exclude_none=True)
        if not values:
            return await self.get_client(client_id)

        query = update(Client).where(Client.client_id == client_id).values(**values).returning(Client)
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_client(self, client_id: int) -> bool:
        client = await self.get_client(client_id)
        if client is None:
            return False
        await self._delete(client)
        return True
