from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_OR_CONFLICT_RESPONSES, NOT_FOUND_RESPONSE
from src.dependencies import get_user_service
from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.services.users import UserService

users_router = APIRouter(tags=["Users"], prefix="/users")
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserId = Annotated[int, Path(gt=0)]


@users_router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE)
async def create_user(user: UserCreate, service: UserServiceDependency) -> UserOut:
    return await service.create_user(user)


@users_router.get("", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(service: UserServiceDependency) -> list[UserOut]:
    return await service.get_all_users()


@users_router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK, responses=NOT_FOUND_RESPONSE)
async def get_user(user_id: UserId, service: UserServiceDependency) -> UserOut:
    return await service.get_user(user_id)


@users_router.patch(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_OR_CONFLICT_RESPONSES,
)
async def update_user(user_id: UserId, new_data: UserUpdate, service: UserServiceDependency) -> UserOut:
    return await service.update_user(user_id, new_data)


@users_router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, responses=NOT_FOUND_RESPONSE
)
async def delete_user(user_id: UserId, service: UserServiceDependency) -> Response:
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
