from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_OR_CONFLICT_RESPONSES, NOT_FOUND_RESPONSE
from src.dependencies import get_client_service
from src.schemas.clients import ClientCreate, ClientOut, ClientOutWithAPI, ClientUpdate
from src.services.clients import ClientService

clients_router = APIRouter(tags=["Clients"], prefix="/clients")
ClientServiceDependency = Annotated[ClientService, Depends(get_client_service)]
ClientId = Annotated[int, Path(gt=0)]


@clients_router.post(
    "", response_model=ClientOutWithAPI, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE
)
async def create_client(
    client: ClientCreate,
    service: ClientServiceDependency,
    response: Response,
) -> ClientOutWithAPI:
    response.headers["Cache-Control"] = "no-store"
    return await service.create_client(client)


@clients_router.get("", response_model=list[ClientOut], status_code=status.HTTP_200_OK)
async def get_all_clients(service: ClientServiceDependency) -> list[ClientOut]:
    return await service.get_all_clients()


@clients_router.get(
    "/{client_id}", response_model=ClientOut, status_code=status.HTTP_200_OK, responses=NOT_FOUND_RESPONSE
)
async def get_client(client_id: ClientId, service: ClientServiceDependency) -> ClientOut:
    return await service.get_client(client_id)


@clients_router.patch(
    "/{client_id}",
    response_model=ClientOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_OR_CONFLICT_RESPONSES,
)
async def update_client(
    client_id: ClientId,
    new_data: ClientUpdate,
    service: ClientServiceDependency,
) -> ClientOut:
    return await service.update_client(client_id, new_data)


@clients_router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=NOT_FOUND_RESPONSE,
)
async def delete_client(client_id: ClientId, service: ClientServiceDependency) -> Response:
    await service.delete_client(client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
