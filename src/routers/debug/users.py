import json
from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from src.dependencies.dependencies import get_user_service
from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.services.users import UserService

users_router = APIRouter(tags=["Users"], prefix="/users")
user_service = Annotated[UserService, Depends(get_user_service)]


@users_router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully created."},
        409: {"description": "User already exists."},
    }
)
async def create_user(user: Annotated[UserCreate, Depends()], service: user_service):
    return await service.create_user(user)


@users_router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of users returned."}
    }
)
async def get_all_users(service: user_service):
    return await service.get_all_users()


@users_router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User returned."},
        404: {"description": "User not found."}
    }
)
async def get_user(user_id: int, service: user_service):
    user = await service.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@users_router.put(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User successfully updated."},
        404: {"description": "User not found."}
    }
)
async def update_user(user_id: int, new_data: Annotated[UserUpdate, Depends()], service: user_service):
    updated = await service.update_user(user_id, new_data)
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User successfully deleted."},
        404: {"description": "User not found."}
    }
)
async def delete_user(user_id: int, service: user_service):
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT,
                    content=json.dumps({"message": "User successfully deleted."}))
