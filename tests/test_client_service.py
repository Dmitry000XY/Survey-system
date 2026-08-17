import asyncio
from datetime import UTC, datetime

from src.models.clients import Client
from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientCreate, ClientInDB
from src.security import verify_api_key
from src.services.clients import ClientService


class _ClientRepositoryStub(ClientRepository):
    stored_client: ClientInDB | None = None

    def __init__(self) -> None:
        pass

    async def get_client_by_name(self, client_name: str) -> Client | None:
        del client_name
        return None

    async def get_client_by_api_key_hash(self, api_key_hash: str) -> Client | None:
        del api_key_hash
        return None

    async def create_client(self, client: ClientInDB) -> Client:
        self.stored_client = client
        return Client(
            client_id=1,
            client_name=client.client_name,
            time_created=datetime.now(UTC),
        )


def test_client_service_returns_api_key_once_and_stores_only_hash() -> None:
    repository = _ClientRepositoryStub()
    service = ClientService(repository)

    result = asyncio.run(service.create_client(ClientCreate(client_name="telegram")))

    assert repository.stored_client is not None
    assert verify_api_key(result.api_key, repository.stored_client.api_key_hash)
    assert result.api_key != repository.stored_client.api_key_hash
