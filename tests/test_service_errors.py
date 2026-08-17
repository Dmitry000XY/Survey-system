import asyncio

import pytest

from src.exceptions import RepositoryConflictError, RepositoryError, ResourceConflictError, ServiceUnavailableError
from src.models.clients import Client
from src.repositories.clients import ClientRepository
from src.schemas.clients import ClientCreate
from src.services.clients import ClientService


class _UnavailableClientRepositoryStub(ClientRepository):
    def __init__(self) -> None:
        pass

    async def get_client_by_name(self, client_name: str):
        del client_name
        raise RepositoryError("client", "read")


class _ConflictingClientRepositoryStub(ClientRepository):
    def __init__(self) -> None:
        pass

    async def get_client_by_name(self, client_name: str):
        del client_name
        return None

    async def get_client_by_api_key_hash(self, api_key_hash: str) -> Client | None:
        del api_key_hash
        return None

    async def create_client(self, client):
        del client
        raise RepositoryConflictError("client", "create")


class _CollidingKeyClientRepositoryStub(ClientRepository):
    def __init__(self) -> None:
        self.lookup_count = 0

    async def get_client_by_name(self, client_name: str):
        del client_name
        return None

    async def get_client_by_api_key_hash(self, api_key_hash: str) -> Client | None:
        self.lookup_count += 1
        return Client(client_name="existing", api_key_hash=api_key_hash)


def test_repository_failure_is_translated_to_safe_service_error() -> None:
    service = ClientService(_UnavailableClientRepositoryStub())

    with pytest.raises(ServiceUnavailableError, match="temporarily unavailable"):
        asyncio.run(service.create_client(ClientCreate(client_name="telegram")))


def test_repository_conflict_is_translated_to_domain_conflict() -> None:
    service = ClientService(_ConflictingClientRepositoryStub())

    with pytest.raises(ResourceConflictError, match="already exists"):
        asyncio.run(service.create_client(ClientCreate(client_name="telegram")))


def test_api_key_generation_stops_after_repeated_hash_collisions() -> None:
    repository = _CollidingKeyClientRepositoryStub()
    service = ClientService(repository)

    with pytest.raises(ServiceUnavailableError, match="temporarily unavailable"):
        asyncio.run(service.create_client(ClientCreate(client_name="telegram")))

    assert repository.lookup_count == 3
