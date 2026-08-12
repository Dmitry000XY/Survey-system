import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import cast

from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientCreate, ClientInDB
from src.security import verify_api_key
from src.services.clients import ClientService


class _ClientRepositoryStub:
    stored_client: ClientInDB | None = None

    async def get_client_by_name(self, client_name: str):
        return None

    async def create_client(self, client: ClientInDB):
        self.stored_client = client
        return SimpleNamespace(
            client_id=1,
            client_name=client.client_name,
            time_created=datetime.now(UTC),
        )


def test_client_service_returns_api_key_once_and_stores_only_hash() -> None:
    repository = _ClientRepositoryStub()
    service = ClientService(cast(ClientRepository, repository))

    result = asyncio.run(service.create_client(ClientCreate(client_name="telegram")))

    assert repository.stored_client is not None
    assert verify_api_key(result.api_key, repository.stored_client.api_key_hash)
    assert result.api_key != repository.stored_client.api_key_hash
