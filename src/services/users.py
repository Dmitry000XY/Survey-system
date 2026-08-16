from src.exceptions import ResourceConflictError, ResourceNotFoundError
from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserOut, UserUpdate

from .base import BaseService


class UserService(BaseService):
    resource_name = "user"

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserOut:
        existing = await self._run(self.user_repository.get_user(user.user_id))
        if existing is not None:
            raise ResourceConflictError("A user with this ID already exists.")
        created = await self._run(
            self.user_repository.create_user(user),
            conflict_message="A user with this ID or login already exists.",
        )
        return self._to_schema(created, UserOut)

    async def get_all_users(self) -> list[UserOut]:
        users = await self._run(self.user_repository.get_all_users())
        return self._to_schema_list(users, UserOut)

    async def get_user(self, user_id: int) -> UserOut:
        user = await self._run(self.user_repository.get_user(user_id))
        return self._to_schema(self._require(user, details={"user_id": user_id}), UserOut)

    async def update_user(self, user_id: int, new_data: UserUpdate) -> UserOut:
        updated = await self._run(
            self.user_repository.update_user(user_id, new_data),
            conflict_message="A user with this login already exists.",
        )
        return self._to_schema(self._require(updated, details={"user_id": user_id}), UserOut)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self._run(self.user_repository.delete_user(user_id))
        if not deleted:
            raise ResourceNotFoundError(self.resource_name, details={"user_id": user_id})
