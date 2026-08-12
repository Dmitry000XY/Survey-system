from sqlalchemy import select, update
from src.models.clients import Client
from src.schemas.clients import ClientInDB, ClientUpdate


class ClientRepository:
    def __init__(self, session):
        self.session = session

    async def create_client(self, client: ClientInDB):
        new_client = Client(
            client_name=client.client_name,
            api_key_hash=client.api_key_hash,
        )
        self.session.add(new_client)
        await self.session.flush()
        return new_client

    async def get_all_clients(self):
        query = select(Client)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_client(self, client_id: int):
        return await self.session.get(Client, client_id)

    async def get_client_by_name(self, client_name: str):
        query = select(Client).where(Client.client_name == client_name)
        res = await self.session.execute(query)
        return res.scalars().first()

    async def update_client(self, client_id: int, new_data: ClientUpdate):
        values = new_data.model_dump(exclude_unset=True)
        if not values:
            return await self.get_client(client_id)

        query = update(Client).where(Client.client_id == client_id).values(**values).returning(Client)
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_client(self, client_id: int):
        client = await self.get_client(client_id)
        if client:
            await self.session.delete(client)
