from sqlalchemy import select
from src.models.users_clients import UserClient


class UserClientRepository:
    def __init__(self, session):
        self.session = session

    async def create_user_client(self, user_client):
        new_user_client = UserClient(
            user_id=user_client.user_id,
            client_id=user_client.client_id,
            user_client_id=user_client.user_client_id
        )
        self.session.add(new_user_client)
        await self.session.flush()
        return new_user_client

    async def get_user_client(self, user_id: int, client_id: int):
        return await self.session.get(UserClient, (user_id, client_id))

    async def delete_user_client(self, user_id: int, client_id: int):
        uc = await self.get_user_client(user_id, client_id)
        if uc:
            await self.session.delete(uc)
