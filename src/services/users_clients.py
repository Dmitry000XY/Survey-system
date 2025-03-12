from fastapi import Response, status
from src.repositories.users_clients import UserClientRepository


class UserClientService:
    def __init__(self, user_client_repository: UserClientRepository):
        self.user_client_repository = user_client_repository

    async def create_user_client(self, user_client):
        return await self.user_client_repository.create_user_client(user_client)

    async def get_user_client(self, user_id: int, client_id: int):
        uc = await self.user_client_repository.get_user_client(user_id, client_id)
        if not uc:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return uc

    async def delete_user_client(self, user_id: int, client_id: int):
        if await self.user_client_repository.get_user_client(user_id, client_id):
            await self.user_client_repository.delete_user_client(user_id, client_id)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
