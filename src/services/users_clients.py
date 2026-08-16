from src.exceptions import ResourceNotFoundError
from src.repositories.users_clients import UserClientRepository
from src.schemas.users_clients import UserClientCreate, UserClientOut

from .base import BaseService


class UserClientService(BaseService):
    resource_name = "user-client link"

    def __init__(self, user_client_repository: UserClientRepository) -> None:
        self.user_client_repository = user_client_repository

    async def create_user_client(self, user_client: UserClientCreate) -> UserClientOut:
        created = await self._run(
            self.user_client_repository.create_user_client(user_client),
            conflict_message="This user-client link or external client identity already exists.",
        )
        return self._to_schema(created, UserClientOut)

    async def get_user_client(self, user_id: int, client_id: int) -> UserClientOut:
        user_client = await self._run(self.user_client_repository.get_user_client(user_id, client_id))
        return self._to_schema(
            self._require(user_client, details={"user_id": user_id, "client_id": client_id}),
            UserClientOut,
        )

    async def delete_user_client(self, user_id: int, client_id: int) -> None:
        deleted = await self._run(self.user_client_repository.delete_user_client(user_id, client_id))
        if not deleted:
            raise ResourceNotFoundError(
                self.resource_name,
                details={"user_id": user_id, "client_id": client_id},
            )
