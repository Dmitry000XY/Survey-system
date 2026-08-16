from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_RESPONSE
from src.dependencies import get_user_client_service
from src.schemas.users_clients import UserClientCreate, UserClientOut
from src.services.users_clients import UserClientService

users_clients_router = APIRouter(tags=["Users clients"], prefix="/users-clients")
UserClientServiceDependency = Annotated[UserClientService, Depends(get_user_client_service)]
ResourceId = Annotated[int, Path(gt=0)]


@users_clients_router.post(
    "", response_model=UserClientOut, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE
)
async def create_user_client(
    user_client: UserClientCreate,
    service: UserClientServiceDependency,
) -> UserClientOut:
    return await service.create_user_client(user_client)


@users_clients_router.get(
    "/{user_id}/{client_id}",
    response_model=UserClientOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_user_client(
    user_id: ResourceId,
    client_id: ResourceId,
    service: UserClientServiceDependency,
) -> UserClientOut:
    return await service.get_user_client(user_id, client_id)


@users_clients_router.delete(
    "/{user_id}/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=NOT_FOUND_RESPONSE,
)
async def delete_user_client(
    user_id: ResourceId,
    client_id: ResourceId,
    service: UserClientServiceDependency,
) -> Response:
    await service.delete_user_client(user_id, client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
