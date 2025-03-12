from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_user_client_service
from src.schemas.users_clients import UserClientCreate, UserClientOut
from src.services.users_clients import UserClientService

users_clients_router = APIRouter(tags=["Users clients"], prefix="/users-clients")
user_client_service = Annotated[UserClientService, Depends(get_user_client_service)]


@users_clients_router.post("/", response_model=UserClientOut, status_code=status.HTTP_201_CREATED)
async def create_user_client(user_client: Annotated[UserClientCreate, Depends()], service: user_client_service):
    return await service.create_user_client(user_client)


@users_clients_router.get("/{user_id}/{client_id}", response_model=UserClientOut)
async def get_user_client(user_id: int, client_id: int, service: user_client_service):
    uc = await service.get_user_client(user_id, client_id)
    if uc:
        return uc
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@users_clients_router.delete("/{user_id}/{client_id}")
async def delete_user_client(user_id: int, client_id: int, service: user_client_service):
    await service.delete_user_client(user_id, client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
