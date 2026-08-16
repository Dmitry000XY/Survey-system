from src.configurations.constants import API_KEY_GENERATION_ATTEMPTS
from src.exceptions import ResourceConflictError, ResourceNotFoundError, ServiceUnavailableError
from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientCreate, ClientInDB, ClientOut, ClientOutWithAPI, ClientUpdate
from src.security import generate_api_key, hash_api_key

from .base import BaseService


class ClientService(BaseService):
    resource_name = "client"

    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository

    async def create_client(self, client: ClientCreate) -> ClientOutWithAPI:
        existing = await self._run(self.client_repository.get_client_by_name(client.client_name))
        if existing is not None:
            raise ResourceConflictError("A client with this name already exists.")

        api_key, api_key_hash = await self._generate_unique_api_key()
        new_client = ClientInDB(client_name=client.client_name, api_key_hash=api_key_hash)
        created = await self._run(
            self.client_repository.create_client(new_client),
            conflict_message="A client with this name already exists.",
        )
        return ClientOutWithAPI(
            client_id=created.client_id,
            client_name=created.client_name,
            time_created=created.time_created,
            api_key=api_key,
        )

    async def get_all_clients(self) -> list[ClientOut]:
        clients = await self._run(self.client_repository.get_all_clients())
        return self._to_schema_list(clients, ClientOut)

    async def get_client(self, client_id: int) -> ClientOut:
        client = await self._run(self.client_repository.get_client(client_id))
        return self._to_schema(self._require(client, details={"client_id": client_id}), ClientOut)

    async def update_client(self, client_id: int, new_data: ClientUpdate) -> ClientOut:
        updated = await self._run(
            self.client_repository.update_client(client_id, new_data),
            conflict_message="A client with this name already exists.",
        )
        return self._to_schema(self._require(updated, details={"client_id": client_id}), ClientOut)

    async def delete_client(self, client_id: int) -> None:
        deleted = await self._run(self.client_repository.delete_client(client_id))
        if not deleted:
            raise ResourceNotFoundError(self.resource_name, details={"client_id": client_id})

    async def _generate_unique_api_key(self) -> tuple[str, str]:
        for _ in range(API_KEY_GENERATION_ATTEMPTS):
            api_key = generate_api_key()
            api_key_hash = hash_api_key(api_key)
            existing = await self._run(self.client_repository.get_client_by_api_key_hash(api_key_hash))
            if existing is None:
                return api_key, api_key_hash
        raise ServiceUnavailableError()
