from fastapi import HTTPException, status
from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate):
        if await self.user_repository.get_user(user.user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists."
            )
        return await self.user_repository.create_user(user)

    async def get_all_users(self):
        return await self.user_repository.get_all_users()

    async def get_user(self, user_id: int):
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return user

    async def update_user(self, user_id: int, new_data: UserUpdate):
        if await self.user_repository.get_user(user_id):
            return await self.user_repository.update_user(user_id, new_data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    async def delete_user(self, user_id: int):
        if await self.user_repository.get_user(user_id):
            await self.user_repository.delete_user(user_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
