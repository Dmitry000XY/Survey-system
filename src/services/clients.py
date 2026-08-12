from fastapi import HTTPException, status
from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientInDB, ClientOutWithAPI
from src.configurations.constants import generate_api_key
from src.security import hash_api_key


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def create_client(self, client):
        if await self.client_repository.get_client_by_name(client.client_name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists.")
        generated_api_key = generate_api_key()
        new_client = ClientInDB(
            client_name=client.client_name,
            api_key_hash=hash_api_key(generated_api_key),
        )
        created_client = await self.client_repository.create_client(new_client)
        return ClientOutWithAPI(
            client_id=created_client.client_id,
            client_name=created_client.client_name,
            time_created=created_client.time_created,
            api_key=generated_api_key,
        )

    async def get_all_clients(self):
        return await self.client_repository.get_all_clients()

    async def get_client(self, client_id: int):
        client = await self.client_repository.get_client(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
        return client

    async def update_client(self, client_id: int, new_data):
        if await self.client_repository.get_client(client_id):
            return await self.client_repository.update_client(client_id, new_data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    async def delete_client(self, client_id: int):
        if await self.client_repository.get_client(client_id):
            await self.client_repository.delete_client(client_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
