from fastapi import HTTPException, status
from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientInDB
from src.configurations.constants import generate_api_key


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    async def create_client(self, client):
        if await self.client_repository.get_client_by_name(client.client_name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client already exists.")
        generated_api_key = generate_api_key()
        client_data = client.dict()
        client_data["api_key"] = generated_api_key
        new_client = ClientInDB(**client_data)
        created_client = await self.client_repository.create_client(new_client)
        # Replace hashed API key with the generated (plain) one for the response.
        created_client.api_key = generated_api_key
        return created_client

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
