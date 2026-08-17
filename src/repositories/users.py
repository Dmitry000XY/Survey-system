from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate

from .base import BaseRepository


class UserRepository(BaseRepository):
    entity_name = "user"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_user(self, user: UserCreate) -> User:
        new_user = User(
            user_id=user.user_id,
            login=user.login,
            password=user.password_hash.get_secret_value(),
        )
        self.session.add(new_user)
        await self._flush(operation="create")
        return new_user

    async def get_all_users(self) -> list[User]:
        query = select(User)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_user(self, user_id: int) -> User | None:
        return await self._get(User, user_id)

    async def update_user(self, user_id: int, new_data: UserUpdate) -> User | None:
        values = new_data.model_dump(exclude_unset=True, exclude_none=True)
        if "password_hash" in values:
            password_hash = new_data.password_hash
            if password_hash is not None:
                values["password"] = password_hash.get_secret_value()
            del values["password_hash"]
        if not values:
            return await self.get_user(user_id)

        query = update(User).where(User.user_id == user_id).values(**values).returning(User)
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if user is None:
            return False
        await self._delete(user)
        return True
