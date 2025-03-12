import json
from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from src.dependencies.dependencies import get_client_service
from src.schemas.clients import ClientCreate, ClientOut, ClientUpdate, ClientOutWithAPI
from src.services.clients import ClientService

clients_router = APIRouter(tags=["Clients"], prefix="/clients")
client_service = Annotated[ClientService, Depends(get_client_service)]


@clients_router.post(
    "/",
    response_model=ClientOutWithAPI,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Client successfully created."},
        409: {"description": "Client already exists."},
    }
)
async def create_client(client: Annotated[ClientCreate, Depends()], service: client_service):
    return await service.create_client(client)


@clients_router.get(
    "/",
    response_model=list[ClientOut],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of clients returned."}
    }
)
async def get_all_clients(service: client_service):
    return await service.get_all_clients()


@clients_router.get(
    "/{client_id}",
    response_model=ClientOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Client returned."},
        404: {"description": "Client not found."}
    }
)
async def get_client(client_id: int, service: client_service):
    client = await service.get_client(client_id)
    if client:
        return client
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")


@clients_router.put(
    "/{client_id}",
    response_model=ClientOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Client successfully updated."},
        404: {"description": "Client not found."}
    }
)
async def update_client(client_id: int, new_data: Annotated[ClientUpdate, Depends()], service: client_service):
    updated = await service.update_client(client_id, new_data)
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")


@clients_router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Client successfully deleted."},
        404: {"description": "Client not found."}
    }
)
async def delete_client(client_id: int, service: client_service):
    await service.delete_client(client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT,
                    content=json.dumps({"message": "Client successfully deleted."}))
